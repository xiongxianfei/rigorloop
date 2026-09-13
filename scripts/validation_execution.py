"""Internal catalog execution shared by repository CI entrypoints.

No public runner CLI, result cache, lifecycle transition or publication authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import ctypes
import codecs
import json
import os
import platform
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import tempfile
import time
import shutil

from validation_selection import (CHECK_CATALOG, MODE_CHECK_IDS, BOUNDARY_CHECK_IDS, DEFAULT_ADAPTER_VERSION, catalog_command,
                                  is_parallel_safe_check, validate_catalog)


def fail(message, code=4):
    print(message, file=sys.stderr)
    raise SystemExit(code)


@dataclass
class CheckPlan:
    check_id: str
    command: str
    args: list[str]
    reason: str | None
    phase: str
    parallel_safe: bool
    dependencies: tuple[str, ...] = ()
    demand: int = 1
    after: tuple[str, ...] = ()


@dataclass
class CheckResult:
    plan: CheckPlan
    status: str
    exit_reason: str
    elapsed_seconds: float
    stdout_path: Path | None
    stderr_path: Path | None
    exit_code: int


def validate_plans(plans, *, jobs):
    if type(jobs) is not int or jobs < 1:
        raise ValueError('jobs must be a positive integer')
    ids = [p.check_id for p in plans]
    if any(not isinstance(x,str) or not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError('duplicate or invalid task identity')
    for p in plans:
        if p.phase not in {'preflight', 'focused', 'boundary'}:
            raise ValueError(f'unknown phase: {p.phase}')
        if type(p.parallel_safe) is not bool or type(p.demand) is not int or p.demand < 1:
            raise ValueError(f'invalid resource constraints: {p.check_id}')
        if not isinstance(p.args,list) or not p.args or any(not isinstance(x,str) or '\0' in x for x in p.args):
            raise ValueError(f'invalid argv: {p.check_id}')
        if not isinstance(p.dependencies,tuple) or len(set(p.dependencies)) != len(p.dependencies):
            raise ValueError(f'invalid dependencies: {p.check_id}')
        if any(d not in ids for d in p.dependencies):
            raise ValueError(f'missing dependency: {p.check_id}')
    for p in plans:
        if not isinstance(p.after,tuple) or len(set(p.after)) != len(p.after) or any(d not in ids for d in p.after):
            raise ValueError(f"invalid diagnostic ordering: {p.check_id}")
    graph = {p.check_id:(*p.dependencies,*p.after) for p in plans}
    visiting, visited = set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError(f'dependency cycle: {key}')
        if key in visited:
            return
        visiting.add(key)
        for d in graph[key]:
            visit(d)
        visiting.remove(key)
        visited.add(key)
    for key in graph:
        visit(key)


def _enable_child_ownership():
    if os.name != 'posix' or not hasattr(os, 'killpg'):
        raise ValueError('POSIX process-group ownership is required; run domain validators directly on this platform')
    if not sys.platform.startswith('linux') or not Path('/proc/self/stat').is_file():
        raise ValueError('POSIX execution requires Linux /proc descendant ownership on this implementation; run domain validators directly')
    if sys.platform.startswith('linux'):
        # Adopt orphaned descendants so the owning invocation can reap them.
        if ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) != 0:
            raise ValueError('unable to establish Linux descendant ownership')


def _process_snapshot():
    """PID -> (parent, birth identity); /proc avoids spawning another child."""
    processes = {}
    for directory in Path('/proc').iterdir():
        if not directory.name.isdigit():
            continue
        try:
            fields = (directory/'stat').read_text().rsplit(')',1)[1].split()
            processes[int(directory.name)] = (int(fields[1]), fields[19])
        except (FileNotFoundError, ProcessLookupError):
            continue
        except PermissionError:
            # Other users' processes are not children of this invocation.
            continue
    return processes


def _discover_owned(running, snapshot):
    for task in running.values():
        owned = task['owned']
        known = {pid for pid, birth in owned.items() if snapshot.get(pid, (None,None))[1] == birth}
        changed = True
        while changed:
            changed = False
            for pid, (parent, birth) in snapshot.items():
                if parent in known and pid not in known:
                    owned[pid] = birth
                    known.add(pid)
                    changed = True


def _signal_owned(task, value, snapshot):
    _signal_group(task['process'].pid, value)
    for pid, birth in task['owned'].items():
        if snapshot.get(pid,(None,None))[1] != birth:
            continue
        try:
            os.kill(pid, value)
        except ProcessLookupError:
            pass


def _reap_owned(task):
    for pid in task['owned']:
        if pid == task['process'].pid:
            continue
        try:
            os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            pass


def _owned_alive(task, snapshot):
    return any(snapshot.get(pid,(None,None))[1] == birth for pid,birth in task['owned'].items())


def _signal_group(pid, value):
    try:
        os.killpg(pid, value)
    except ProcessLookupError:
        pass


def _reap_group(pid):
    while True:
        try:
            child, _ = os.waitpid(-pid, os.WNOHANG)
        except ChildProcessError:
            return
        if child == 0:
            return


def _group_exists(pid):
    try:
        os.killpg(pid, 0)
        return True
    except ProcessLookupError:
        return False


def _not_started(plan, reason):
    return CheckResult(plan, 'not started', reason, 0, None, None, 125)


def supervise(notice_path, args):
    """One task's adoption boundary; never relies on child environment tokens.

    Each supervisor adopts only its own task's orphans, including double forks
    and new sessions with a replaced environment. It remains alive until they
    are reaped. The parent scheduler sees the early outcome during cleanup.
    """
    _enable_child_ownership()
    interrupted = 0
    def stop(number, frame):
        nonlocal interrupted
        interrupted = number
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    notice = Path(notice_path)
    def publish(code, error=None):
        temporary = notice.with_suffix('.pending')
        temporary.write_text(json.dumps({'returncode':code,'launch_error':error})+'\n')
        os.replace(temporary, notice)
    try:
        process = subprocess.Popen(args)
    except OSError as exc:
        publish(127, f'command unavailable: {exc.filename}')
        return
    owned = {}
    ending = None
    published = False
    while True:
        snapshot = _process_snapshot()
        known = {pid for pid,birth in owned.items() if snapshot.get(pid,(None,None))[1] == birth}
        known.add(os.getpid())
        changed = True
        while changed:
            changed = False
            for pid, (parent,birth) in snapshot.items():
                if parent in known and pid not in known:
                    owned[pid] = birth
                    known.add(pid)
                    changed = True
        code = process.poll()
        if code is not None and not published:
            publish(code)
            published = True
        now = time.monotonic()
        if (interrupted or code is not None) and ending is None:
            ending = now
        if ending is not None:
            # The outer scheduler allows five seconds. Finish the supervisor's
            # grace slightly earlier so it can reap before the outer kill.
            sig = signal.SIGKILL if now-ending >= 4 else signal.SIGTERM
            for pid,birth in owned.items():
                if snapshot.get(pid,(None,None))[1] != birth:
                    continue
                try:
                    os.kill(pid,sig)
                except ProcessLookupError:
                    pass
        for pid in owned:
            if pid == process.pid:
                continue
            try:
                os.waitpid(pid,os.WNOHANG)
            except ChildProcessError:
                pass
        snapshot = _process_snapshot()
        if process.poll() is not None and not any(snapshot.get(pid,(None,None))[1] == birth for pid,birth in owned.items()):
            if not published:
                publish(process.returncode)
            return
        time.sleep(.01)


def run_scheduled_checks(plans, *, jobs, timeout_seconds, fail_fast, scratch):
    validate_plans(plans, jobs=jobs)
    if 'RIGORLOOP_VALIDATION_WORKERS' in os.environ:
        parent = os.environ['RIGORLOOP_VALIDATION_WORKERS']
        if not parent.isascii() or not parent.isdigit() or int(parent) < 1:
            raise ValueError('parent worker allocation must be a positive integer')
        jobs = min(jobs, int(parent))
    if type(timeout_seconds) is not int or timeout_seconds < 1:
        raise ValueError('timeout must be a positive integer')
    if type(fail_fast) is not bool:
        raise ValueError('fail_fast must be boolean')
    _enable_child_ownership()
    scratch.mkdir(parents=True, exist_ok=True)
    results = {}
    pending = list(plans)
    running = {}
    stopped = False
    interrupted = 0
    previous_handlers = {}
    def interrupt(number, frame):
        nonlocal interrupted
        interrupted = number
    try:
        for number in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[number] = signal.signal(number, interrupt)
        while pending or running:
            now = time.monotonic()
            snapshot = _process_snapshot()
            _discover_owned(running, snapshot)
            for key, task in list(running.items()):
                process = task['process']
                supervisor_code = process.poll()
                observed = None
                if task['notice'].exists():
                    try:
                        observed = json.loads(task['notice'].read_text())
                        if set(observed) != {'returncode', 'launch_error'} or type(observed['returncode']) is not int or not isinstance(observed['launch_error'], (str,type(None))):
                            raise ValueError('malformed task outcome')
                    except (ValueError, OSError, TypeError):
                        observed = {'returncode':4,'launch_error':'invalid task outcome'}
                returncode = observed['returncode'] if observed else (4 if supervisor_code is not None else None)
                if fail_fast and observed and observed['returncode'] != 0:
                    stopped = True
                if fail_fast and returncode is not None and returncode != 0:
                    stopped = True
                if returncode is not None:
                    _reap_group(process.pid)
                if task['stop'] is None:
                    if interrupted:
                        task['stop'] = now
                        task['outcome'] = ('killed', f'interrupted by {signal.Signals(interrupted).name}', 128 + interrupted)
                    elif now - task['start'] >= timeout_seconds and returncode is None:
                        task['stop'] = now
                        task['outcome'] = ('timed out', f'timeout after {timeout_seconds}s', 124)
                        if fail_fast:
                            stopped = True
                    elif returncode is not None:
                        task['outcome'] = ('passed', 'ok', 0) if returncode == 0 else (
                            ('killed', f'signal {signal.Signals(-returncode).name} ({-returncode})',128-returncode)
                            if returncode < 0 else ('exited',f'exit code {returncode}',returncode))
                        if observed and observed['launch_error']:
                            task['outcome'] = ('unavailable' if observed['returncode'] == 127 else 'runner error', observed['launch_error'], observed['returncode'])
                        elif not observed:
                            task['outcome'] = ('runner error', 'missing task outcome', 4)
                        task['stop'] = now
                    if task['stop'] is not None:
                        _signal_owned(task, signal.SIGTERM, snapshot)
                if task['stop'] is not None and now - task['stop'] >= 5:
                    _signal_owned(task, signal.SIGKILL, snapshot)
                if process.poll() is not None:
                    _reap_group(process.pid)
                    _reap_owned(task)
                    if not _owned_alive(task, _process_snapshot()) and not _group_exists(process.pid):
                        for stream in task['streams']:
                            stream.close()
                        status, reason, code = task['outcome']
                        for label, path in zip(('stdout','stderr'),task['paths']):
                            try:
                                decoder = codecs.getincrementaldecoder('utf-8')()
                                with path.open('rb') as capture:
                                    while chunk := capture.read(65536):
                                        decoder.decode(chunk)
                                    decoder.decode(b'', final=True)
                            except UnicodeDecodeError:
                                reason += f'; {label} decode error'
                                if code == 0:
                                    status, code = 'runner error', 4
                            except OSError:
                                reason += f'; missing {label} capture'
                                status, code = 'runner error', 4
                        results[key] = CheckResult(task['plan'], status, reason, now-task['start'], *task['paths'], code)
                        del running[key]
                        if fail_fast and code:
                            stopped = True
            if interrupted:
                stopped = True
            for plan in list(pending):
                if stopped:
                    results[plan.check_id] = _not_started(plan, 'interrupted queue' if interrupted else 'fail-fast cancelled remaining queue')
                    pending.remove(plan)
                    continue
                failed = [d for d in plan.dependencies if d in results and results[d].exit_code]
                if failed:
                    results[plan.check_id] = _not_started(plan, 'failed prerequisite: ' + ', '.join(failed))
                    pending.remove(plan)
                    continue
                if any(d not in results for d in (*plan.dependencies,*plan.after)):
                    continue
                demand = min(plan.demand, jobs) if plan.parallel_safe else jobs
                used = sum(t['demand'] for t in running.values())
                # A serial entry is an ordering barrier for later independent work.
                if not plan.parallel_safe and running:
                    break
                if used + demand > jobs:
                    break
                directory = Path(tempfile.mkdtemp(prefix='task-', dir=scratch))
                paths = (directory/'stdout', directory/'stderr')
                streams = [p.open('wb') for p in paths]
                env = os.environ.copy()
                env['RIGORLOOP_VALIDATION_WORKERS'] = str(demand)
                env['PYTHONDONTWRITEBYTECODE'] = '1'
                # Native Node tests cannot create an independent CPU-sized pool.
                args = list(plan.args)
                if plan.check_id == 'broad_smoke.repo':
                    args.extend(['--jobs', str(demand), '--timeout', str(timeout_seconds)])
                if args[0] == 'npm' and 'test' in args:
                    args.extend(['--', f'--test-concurrency={demand}'])
                if args[0] == 'node' and '--test' in args:
                    args.insert(args.index('--test')+1, f'--test-concurrency={demand}')
                plan.args = args
                started = time.monotonic()
                try:
                    if args[0] in {'python','bash'} and len(args)>1 and args[1].startswith('scripts/') and not Path(args[1]).exists():
                        raise FileNotFoundError(2, 'script missing', args[1])
                    if shutil.which(args[0]) is None:
                        raise FileNotFoundError(2, 'executable missing', args[0])
                    bootstrap = "import sys; sys.path.insert(0,sys.argv[1]); from validation_execution import supervise; supervise(sys.argv[2],sys.argv[3:])"
                    supervisor = [sys.executable, '-c', bootstrap, str(Path(__file__).resolve().parent), str(directory/'outcome.json'), *args]
                    process = subprocess.Popen(supervisor, stdout=streams[0], stderr=streams[1], env=env, start_new_session=True)
                except OSError as exc:
                    for stream in streams:
                        stream.close()
                    results[plan.check_id] = CheckResult(plan, 'unavailable',f'command unavailable: {exc.filename}',0,*paths,127)
                    if fail_fast:
                        stopped = True
                else:
                    running[plan.check_id] = dict(plan=plan, process=process, streams=streams, paths=paths,
                        start=started, demand=demand, stop=None, outcome=None,
                        owned={process.pid:_process_snapshot().get(process.pid,(None,None))[1]},
                        notice=directory/'outcome.json')
                pending.remove(plan)
                if not plan.parallel_safe:
                    break
            if pending or running:
                time.sleep(.01)
    finally:
        # Defensive failures retain the same descendant ownership and grace.
        snapshot = _process_snapshot()
        _discover_owned(running, snapshot)
        for task in running.values():
            _signal_owned(task, signal.SIGTERM, snapshot)
        deadline = time.monotonic()+5
        while running and time.monotonic()<deadline:
            snapshot = _process_snapshot()
            _discover_owned(running, snapshot)
            for task in running.values():
                task['process'].poll()
                _reap_owned(task)
            if not any(_owned_alive(t, snapshot) for t in running.values()):
                break
            time.sleep(.01)
        for task in running.values():
            _signal_owned(task, signal.SIGKILL, _process_snapshot())
            task['process'].wait()
            deadline = time.monotonic()+1
            while _owned_alive(task, _process_snapshot()) and time.monotonic()<deadline:
                _reap_owned(task)
                time.sleep(.01)
            for stream in task['streams']:
                stream.close()
        for number, handler in previous_handlers.items():
            signal.signal(number, handler)
    if len(results) != len(plans):
        raise RuntimeError('missing required task result')
    return [results[p.check_id] for p in plans]


def command_display(args):
    return shlex.join(args)


def print_summary(results):
    print('Selected CI check summary:')
    print('check ID | status | exit reason | elapsed')
    for r in results:
        print(f'{r.plan.check_id} | {r.status} | {r.exit_reason} | {r.elapsed_seconds:.2f}s')
    print('Selected CI check phases:')
    print('check ID | phase')
    totals = {}
    for r in results:
        print(f'{r.plan.check_id} | {r.plan.phase}')
        totals[r.plan.phase] = totals.get(r.plan.phase,0) + r.elapsed_seconds
    print('Selected CI phase timing summary:')
    for phase in sorted(totals):
        print(f'{phase} | {totals[phase]:.2f}s')


def print_result_output(results, *, verbose):
    print('Selected check output:' if verbose else 'Failed selected check output:')
    for r in results:
        if not verbose and r.status == 'passed':
            continue
        print(f'==> {r.plan.check_id} ({r.status})')
        print('Command: ' + command_display(r.plan.args))
        print('Re-run: ' + command_display(r.plan.args))
        captured = False
        for label, path in [('stdout',r.stdout_path), ('stderr',r.stderr_path)]:
            if path is None:
                continue
            if not path.exists():
                print(f'missing {label} capture for {r.plan.check_id}')
                r.status, r.exit_code = 'runner error', 4
                continue
            if path.stat().st_size:
                captured = True
                diagnostic = ' (decode error; replacement text)' if f'{label} decode error' in r.exit_reason else ''
                print(f'--- {label}{diagnostic} ---')
                last = ''
                with path.open(encoding='utf-8',errors='replace') as stream:
                    while chunk := stream.read(65536):
                        print(chunk,end='')
                        last = chunk[-1]
                if last != '\n':
                    print()

        if not captured:
            print('(no captured output)')


def _git(*args, optional=False):
    result = subprocess.run(['git',*args],capture_output=True,text=True,timeout=300)
    if result.returncode:
        if optional:
            return ''
        raise ValueError('unable to resolve validation scope: '+result.stderr.strip())
    return result.stdout.rstrip('\n')


def _current_roots(paths):
    roots = []
    for raw in paths:
        parts = Path(raw).parts
        if len(parts)<4 or parts[:2] != ('docs','changes'):
            continue
        directory = Path(*parts[:3])
        manifest = directory/'change.json'
        relative = '/'.join(parts[3:])
        reserved = relative in {'change.json','evidence.json','material-decisions.json','verify-report.json'} or (relative.startswith('reviews/') and relative.endswith('.json'))
        if not manifest.exists() and not manifest.is_symlink() and not directory.is_symlink() and directory.is_dir() and os.access(directory,os.R_OK|os.X_OK) and not reserved:
            continue
        if str(manifest) not in roots:
            roots.append(str(manifest))
    return roots


def compose_mode(mode, scratch, *, base='', head='', skip_diff_scoped=False):
    validate_catalog()
    if mode not in MODE_CHECK_IDS:
        raise ValueError(f'unknown composed mode: {mode}')
    if 'RIGORLOOP_BROAD_SMOKE_CLASSIFICATION' in os.environ:
        raise ValueError('RIGORLOOP_BROAD_SMOKE_CLASSIFICATION is retired; current catalog owns constraints')
    if mode == 'broad-smoke' and os.environ.get('RIGORLOOP_CI_BROAD_SMOKE_STUB') == '1':
        print('Broad smoke stub (test fixture; no validation evidence)')
        return []
    output = str(scratch / ('adapters-'+mode))
    values = {'<adapter-output>':[output]}
    roots = []
    if os.environ.get('RIGORLOOP_CI_DIRECT_DRY_RUN') != '1':
        from validation_selection import _preflight_results, _git_local_changed_paths
        checks = _preflight_results(_git_local_changed_paths(Path.cwd()),repo_root=Path.cwd())
        blocked = [item for item in checks if item.get('result') == 'blocked']
        if blocked:
            fail('Preflight blocked: '+json.dumps(blocked),2)
    if mode == 'main':
        if not base or not head:
            base,head = _git('rev-parse','--verify','HEAD~1'),_git('rev-parse','--verify','HEAD')
        values.update({'<base>':[base],'<head>':[head]})
    else:
        dirty = _git('diff','--name-only','-z','--diff-filter=ACMRT','HEAD','--','.').split('\0')
        dirty = [x for x in dirty if x]
        previous = _git('rev-parse','--verify','HEAD~1',optional=True)
        if not skip_diff_scoped:
            if os.environ.get('REVIEW_ARTIFACT_ROOTS'):
                roots = [x.rstrip('/')+'/change.json' for x in os.environ['REVIEW_ARTIFACT_ROOTS'].split()]
            else:
                changed = dirty or (_git('diff','--name-only','-z','--diff-filter=ACMRT','HEAD~1','HEAD','--','.').split('\0') if previous else [])
                roots = _current_roots(changed)
        authored = [x for x in dirty if not x.startswith(('.codex/skills/','dist/adapters/'))]
        if authored and (not skip_diff_scoped or not previous):
            lifecycle = ['--mode','explicit-paths']
            for path in authored:
                lifecycle.extend(['--path',path])
        elif previous:
            lifecycle = ['--mode','push-main-ci','--before',previous,'--after',_git('rev-parse','--verify','HEAD')]
        else:
            raise ValueError('Unable to determine artifact lifecycle validation scope')
        values.update({'<roots>':roots,'<lifecycle-args>':lifecycle})
    plans = []
    for key in MODE_CHECK_IDS[mode]:
        if key.endswith('review_artifacts.changed_roots') and not roots:
            continue
        entry = CHECK_CATALOG[key]
        args = []
        for token in shlex.split(entry.command_template):
            if token.startswith('<') and token.endswith('>'):
                if token not in values:
                    raise ValueError(f'unresolved catalog scope: {token}')
                args.extend(values[token])
            else:
                args.append(token)
        constraints = entry.constraints
        plans.append(CheckPlan(key,command_display(args),args,entry.label,'focused',entry.parallel_safe,
            entry.dependencies,constraints.demand if constraints else 1))
    preflight = [p for p in plans if p.check_id.endswith('review_artifacts.changed_roots')]
    for plan in preflight:
        plan.phase = 'preflight'
    for plan in plans:
        if plan not in preflight:
            plan.dependencies = tuple(dict.fromkeys((*plan.dependencies,*(p.check_id for p in preflight))))
    return preflight + [p for p in plans if p not in preflight]


def expand_groups(plans, scratch, *, diagnostic=False):
    expanded = []
    aliases = {}
    for plan in plans:
        if plan.check_id != 'broad_smoke.repo':
            expanded.append(plan)
            continue
        children = compose_mode('broad-smoke',scratch,skip_diff_scoped=True)
        aliases[plan.check_id] = tuple(child.check_id for child in children)
        for child in children:
            child.phase = plan.phase
            if diagnostic:
                child.after = plan.dependencies
            else:
                child.dependencies = tuple(dict.fromkeys((*child.dependencies,*plan.dependencies)))
            child.reason = '; '.join(x for x in (plan.reason,child.reason) if x)
        expanded.extend(children)
    for plan in expanded:
        plan.dependencies = tuple(dict.fromkeys(d for dependency in plan.dependencies for d in aliases.get(dependency,(dependency,))))
    return expanded


def _write_mode_result(results, *, mode, jobs, elapsed, code, skip_diff_scoped):
    destination = os.environ.get('RIGORLOOP_BROAD_SMOKE_RESULT_JSON')
    if mode != 'broad-smoke' or not destination:
        return
    children = [dict(check_id=r.plan.check_id,command=command_display(r.plan.args),duration_ms=round(r.elapsed_seconds*1000),
        phase='parallel' if r.plan.parallel_safe and jobs>1 else 'sequential',
        result='passed' if r.exit_code==0 else 'failed',exit_code=r.exit_code,
        output_bytes=sum(p.stat().st_size for p in (r.stdout_path,r.stderr_path) if p and p.exists()),
        cache_status='not-applicable',status=r.status,exit_reason=r.exit_reason) for r in results]
    payload = dict(scenario='broad-smoke-safe-parallelism',
        command=f'bash scripts/ci.sh --mode broad-smoke '+('--skip-diff-scoped ' if skip_diff_scoped else '')+f'--jobs {jobs}',
        environment=dict(os=platform.platform(),shell=os.environ.get('SHELL','unknown'),cpu_class=f'{os.cpu_count() or 1} logical CPUs',local_or_ci='ci' if os.environ.get('CI') else 'local'),
        repository_state=dict(head=_git('rev-parse','HEAD',optional=True),worktree_state='dirty' if _git('status','--short',optional=True) else 'clean'),
        baseline=dict(total_duration_ms=None,child_durations=[]),
        parallel=dict(jobs=jobs,total_duration_ms=round(elapsed*1000),exit_code=code,child_durations=children),
        delta=dict(duration_ms=None,percent=None),
        preservation=dict(child_set_preserved=True,exit_behavior_preserved=code==0,diagnostics_preserved=True,output_order_preserved=True),
        notes=dict(variance='Current invocation only; historical baseline unavailable by design.',low_confidence_children=[],
            sequential_only_children=[r.plan.check_id for r in results if not r.plan.parallel_safe or jobs==1],default_promotion_decision='assessed_independent_work_uses_shared_budget'))
    Path(destination).write_text(json.dumps(payload,indent=2)+'\n')


def composed_main(argv):
    mode, jobs, timeout, fast, verbose, base, head, skip = argv
    jobs,timeout,fast,verbose,skip = int(jobs),int(timeout),bool(int(fast)),bool(int(verbose)),bool(int(skip))
    with tempfile.TemporaryDirectory(prefix='rigorloop-validation-') as temporary:
        scratch = Path(temporary)
        plans = compose_mode(mode,scratch,base=base,head=head,skip_diff_scoped=skip)
        validate_plans(plans,jobs=jobs)
        if mode == 'main':
            print(f'Direct deterministic product and governance gates ({mode})')
        if os.environ.get('RIGORLOOP_CI_DIRECT_DRY_RUN') == '1':
            for plan in plans:
                print('==> '+(plan.reason or plan.check_id))
                print('+ '+command_display(plan.args))
            print('[PASS] direct gate graph selected without execution')
            return
        started = time.monotonic()
        results = run_scheduled_checks(plans,jobs=jobs,timeout_seconds=timeout,fail_fast=fast,scratch=scratch)
        for result in results:
            if result.exit_code or verbose:
                label = result.plan.reason or result.plan.check_id
                if result.exit_code:
                    print(f'[FAIL] {result.plan.check_id} / {label}: exit {result.exit_code} in {result.elapsed_seconds:.2f}s')
                    print('Check ID:\n'+result.plan.check_id)
                    print('Command:\n'+command_display(result.plan.args))
                    print('Execution phase:\n'+('parallel' if result.plan.parallel_safe and jobs>1 else 'sequential'))
                    print('Captured output:')
                    print('Re-run:\n'+command_display(result.plan.args))
                else:
                    print(f'==> {label} (passed)')
                print_result_output([result],verbose=True)
        code = next((r.exit_code for r in results if r.exit_code),0)
        if code or verbose or mode == "main":
            print_summary(results)
        _write_mode_result(results,mode=mode,jobs=jobs,elapsed=time.monotonic()-started,code=code,skip_diff_scoped=skip)
        if not code:
            print(f'[PASS] {mode}: {len(results)} checks passed in {time.monotonic()-started:.2f}s')
        raise SystemExit(code)


def selected_main(argv):
    selector_output = Path(argv[0])
    selector_exit = int(argv[1])
    timeout_seconds = int(argv[2])
    verbose = bool(int(argv[3]))
    jobs = int(argv[4])
    fail_fast = bool(int(argv[5]))
    requested_mode, requested_base, requested_head = argv[6:9]
    print(f"Worker budget: {jobs}")
    try:
        payload = json.loads(selector_output.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Malformed selector JSON: {exc}")

    required_fields = {
        "mode",
        "status",
        "changed_paths",
        "classified_paths",
        "unclassified_paths",
        "selected_checks",
        "affected_roots",
        "broad_smoke_required",
        "blocking_results",
        "preflight_results",
        "rationale",
    }

    if not isinstance(payload,dict):
        fail("Selector JSON must be an object")
    missing = sorted(required_fields - set(payload))
    if missing:
        fail(f"Selector JSON missing required fields: {', '.join(missing)}")

    if not isinstance(payload.get("broad_smoke",{}),dict) or not isinstance(payload.get("broad_smoke",{}).get("sources",[]),list):
        fail("Invalid broad_smoke metadata")
    mode = payload["mode"]
    if mode not in {"local", "explicit", "pr", "main", "release"}:
        fail(f"Unknown selector mode: {mode}")
    if requested_mode == "pr" and mode != requested_mode:
        fail("Selector mode does not match requested PR mode")
    status = payload["status"]
    print(f"Selector mode: {mode}")
    print(f"Selector status: {status}")
    if payload.get("changed_paths"):
        print("Changed paths: " + ", ".join(payload["changed_paths"]))
    if payload.get("affected_roots"):
        print("Affected roots: " + ", ".join(payload["affected_roots"]))
    if payload.get("broad_smoke_required"):
        print("Broad smoke required: true")
        for source in payload.get("broad_smoke", {}).get("sources", []):
            print(f"Broad smoke source: {source}")
    if payload.get("preflight_results"):
        print("Preflight results:")
        for result in payload["preflight_results"]:
            line = f"- {result.get('check')}: {result.get('result')}"
            if result.get("path"):
                line += f" ({result.get('path')})"
            if result.get("corrective_action"):
                line += f"; action: {result.get('corrective_action')}"
            print(line)

    diagnostic = any(source == {"type":"explicit_flag","value":"--broad-smoke"} for source in payload.get("broad_smoke",{}).get("sources",[]))
    if status == "blocked":
        for result in payload["blocking_results"]:
            print(f"Blocking result: {result}", file=sys.stderr)
        if diagnostic:
            print('Diagnostic broad smoke: original selector blocker remains unsuccessful.')
            try:
                composed_main(['broad-smoke',str(jobs),str(timeout_seconds),str(int(fail_fast)),str(int(verbose)),requested_base,requested_head,'1'])
            except (Exception,SystemExit) as exc:
                print(f'Diagnostic scope completed or blocked: {exc}')
        raise SystemExit(2)
    if status == "fallback":
        print("Selector status: fallback; fallback execution is not supported in v1.", file=sys.stderr)
        raise SystemExit(3)
    if status == "error":
        for result in payload["blocking_results"]:
            print(f"Selector error: {result}", file=sys.stderr)
        raise SystemExit(4)
    if status != "ok":
        fail(f"Unsupported selector status: {status}")
    if selector_exit != 0:
        fail(f"Selector exited {selector_exit} while reporting status ok")

    selected_checks = payload["selected_checks"]
    if not isinstance(selected_checks, list):
        fail('selected_checks must be an array')
    validate_catalog()
    if not selected_checks:
        print("No selected checks to run.")
        raise SystemExit(0)

    validate_catalog()
    plans: list[CheckPlan] = []
    if not isinstance(selected_checks, list):
        fail('selected_checks must be an array')
    for check in selected_checks:
        if not isinstance(check, dict) or set(check) - {'id','command','reason','phase','cache_status','paths','changed_sections','affected_roots','versions'}:
            fail('Unknown selected check fields')
        if check.get('cache_status', 'not-applicable') != 'not-applicable':
            fail('Unknown selected cache_status label')
        for field in ('paths','changed_sections','affected_roots','versions'):
            if not isinstance(check.get(field,[]),list) or any(not isinstance(x,str) for x in check.get(field,[])):
                fail(f'Invalid selected {field}')
        check_id = check.get("id")
        if not isinstance(check_id, str):
            fail(f"Selected check missing string id: {check}")
        paths = tuple(check.get("paths", []))
        changed_sections = tuple(check.get("changed_sections", []))
        affected_roots = tuple(check.get("affected_roots", []))
        versions = tuple(check.get("versions", []))
        try:
            expected_command = catalog_command(
                check_id,
                paths=paths,
                changed_sections=changed_sections,
                affected_roots=affected_roots,
                versions=versions,
                adapter_version=DEFAULT_ADAPTER_VERSION,
                mode=requested_mode,
                base=requested_base,
                head=requested_head,
            )
        except ValueError as exc:
            fail(f"Selected check {check_id} cannot be converted to a trusted command: {exc}")

        command = check.get("command")
        if command != expected_command:
            fail(
                f"Selected check {check_id} command does not match catalog: "
                f"expected {expected_command!r}, got {command!r}"
            )

        args = shlex.split(expected_command)
        reason = check.get("reason")
        expected_phase = "boundary" if check_id in BOUNDARY_CHECK_IDS else "focused"
        phase = check.get("phase", expected_phase)
        if phase not in {"preflight", "focused", "boundary"}:
            fail(f"Selected check {check_id} has unsupported phase: {phase!r}")
        if phase != expected_phase:
            fail(f"Selected check {check_id} phase does not match catalog")
        plans.append(
            CheckPlan(
                check_id=check_id,
                command=expected_command,
                args=args,
                reason=reason if isinstance(reason, str) else None,
                phase=phase,
                parallel_safe=is_parallel_safe_check(check_id),
                dependencies=CHECK_CATALOG[check_id].dependencies,
                demand=CHECK_CATALOG[check_id].constraints.demand if CHECK_CATALOG[check_id].constraints else 1,
            )
        )

    # Phases are dependencies, not labels: cheap failures block boundary work.
    prior = [p.check_id for p in plans if p.phase == "preflight"]
    focused = [p.check_id for p in plans if p.phase == "focused"]
    for plan in plans:
        if plan.phase == "focused":
            plan.dependencies = tuple(dict.fromkeys((*plan.dependencies, *prior)))
        elif plan.phase == "boundary":
            plan.dependencies = tuple(dict.fromkeys((*plan.dependencies, *prior, *focused)))
    validate_plans(plans, jobs=jobs)
    for plan in plans:
        if not plan.parallel_safe:
            print(f"Serial: {plan.check_id}: " + (CHECK_CATALOG[plan.check_id].constraints.isolation if CHECK_CATALOG[plan.check_id].constraints else "isolation/nested demand not yet assessed"))
        print(f"==> Run selected check: {plan.check_id}")
        print(f"Phase: {plan.phase}")
        if plan.reason:
            print(f"Reason: {plan.reason}")
        if plan.check_id != "broad_smoke.repo":
            print("+ " + command_display(plan.args))

    with tempfile.TemporaryDirectory(prefix="rigorloop-validation-") as temporary:
        plans = expand_groups(plans,Path(temporary),diagnostic=diagnostic)
        results = run_scheduled_checks(
            plans,
            jobs=jobs,
            timeout_seconds=timeout_seconds,
            fail_fast=fail_fast,
            scratch=Path(temporary),
        )

        print_summary(results)
        print_result_output(results, verbose=verbose)

        failed_results = [result for result in results if result.status != "passed"]
        if failed_results:
            for result in failed_results:
                print(f"Selected check {result.plan.check_id} failed: {result.exit_reason}", file=sys.stderr)
            raise SystemExit(failed_results[0].exit_code)

        print("Selected CI checks passed.")
