"""Internal catalog execution shared by repository CI entrypoints.

No public runner CLI, result cache, lifecycle transition or publication authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
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
import stat

from lib.validation.validation_selection import (CHECK_CATALOG, MODE_CHECK_IDS, BOUNDARY_CHECK_IDS, DEFAULT_ADAPTER_VERSION, catalog_command,
                                  is_parallel_safe_check, validate_catalog, COVERING_CHECK_IDS, COVERAGE_BASES, command_basis)


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
    case_receipt: Path | None = None
    case_id: str | None = None
    rerun: list[str] | None = None


@dataclass
class CheckResult:
    plan: CheckPlan
    status: str
    exit_reason: str
    elapsed_seconds: float
    stdout_path: Path | None
    stderr_path: Path | None
    exit_code: int
    output_bytes: int | None = None


def validate_plans(plans, *, jobs):
    if type(jobs) is not int or jobs < 1:
        raise ValueError('jobs must be a positive integer')
    ids = [p.check_id for p in plans]
    if any(not isinstance(x,str) or not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError('duplicate or invalid task identity')
    for p in plans:
        if (p.case_receipt is None) != (p.case_id is None):
            raise ValueError(f'incomplete case identity: {p.check_id}')
        if p.case_receipt is not None and (not isinstance(p.case_receipt,Path) or not isinstance(p.case_id,str) or not p.case_id):
            raise ValueError(f'invalid case identity: {p.check_id}')
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


class ExecutionFailure(RuntimeError):
    def __init__(self, message, results):
        super().__init__(message)
        self.results = results


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
    failure = None
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
                if observed and observed['returncode'] == 0:
                    try:
                        _validate_case_receipt(task['plan'])
                    except ValueError as exc:
                        observed = {'returncode':4,'launch_error':str(exc)}
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
                        results[key] = CheckResult(task['plan'], status, reason, time.monotonic()-task['start'], *task['paths'], code)
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
                # Only this invocation's final writer owns its report destination.
                # Nested checks may explicitly select a new destination of their own.
                env.pop('RIGORLOOP_BROAD_SMOKE_RESULT_JSON', None)
                env.pop('RIGORLOOP_VALIDATION_RESULT_JSON', None)
                env.pop('RIGORLOOP_CI_PREPARED_RESULT_JSON', None)
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
                if plan.case_receipt is not None:
                    plan.case_receipt.unlink(missing_ok=True)
                started = time.monotonic()
                try:
                    if args[0] in {'python','bash'} and len(args)>1 and args[1].startswith('scripts/') and not Path(args[1]).exists():
                        raise FileNotFoundError(2, 'script missing', args[1])
                    if shutil.which(args[0]) is None:
                        raise FileNotFoundError(2, 'executable missing', args[0])
                    bootstrap = "import sys; sys.path.insert(0,sys.argv[1]); from lib.validation.validation_execution import supervise; supervise(sys.argv[2],sys.argv[3:])"
                    supervisor = [sys.executable, '-c', bootstrap, str(Path(__file__).resolve().parents[2]), str(directory/'outcome.json'), *args]
                    process = subprocess.Popen(supervisor, stdout=streams[0], stderr=streams[1], env=env, start_new_session=True)
                except OSError as exc:
                    for stream in streams:
                        stream.close()
                    results[plan.check_id] = CheckResult(plan, 'unavailable',f'command unavailable: {exc.filename}',time.monotonic()-started,*paths,127)
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
    except Exception as exc:
        failure = exc
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
            status, reason, code = task['outcome'] or ('runner error', str(failure or 'scheduler stopped'), 4)
            if code == 0:
                status, reason, code = 'runner error', str(failure or 'scheduler stopped'), 4
            results[task['plan'].check_id] = CheckResult(task['plan'], status, reason,
                time.monotonic()-task['start'], *task['paths'], code)
        for number, handler in previous_handlers.items():
            signal.signal(number, handler)
    if failure is not None:
        for plan in pending:
            results[plan.check_id] = _not_started(plan, 'scheduler stopped before dispatch')
        raise ExecutionFailure(str(failure), [results[p.check_id] for p in plans]) from failure
    if len(results) != len(plans):
        raise RuntimeError('missing required task result')
    return [results[p.check_id] for p in plans]


def command_display(args):
    return shlex.join(args)


def print_summary(results, *, boundary_required=False):
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
    if boundary_required:
        if any(r.status != 'passed' and r.plan.phase in {'preflight','focused'} for r in results):
            print('Boundary scope: unsuccessful; prerequisite scope failed, including during diagnostic execution.')
        elif any(r.status != 'passed' for r in results):
            print('Boundary scope: unsuccessful; required work failed or is incomplete.')
        else:
            print('Boundary scope: passed.')


def print_result_output(results, *, verbose):
    print('Selected check output:' if verbose else 'Failed selected check output:')
    for r in results:
        if not verbose and r.status == 'passed':
            continue
        print(f'==> {r.plan.check_id} ({r.status})')
        print('Command: ' + command_display(r.plan.args))
        print('Re-run: ' + command_display(r.plan.rerun or r.plan.args))
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


def unittest_adapter(mode, destination, command, expected=None, *, case_observer=None):
    """Run the original script/main, intercepting only its outer unittest runner.

    Collection uses the normal entrypoint, including load_tests and custom name
    hooks. Each execution is a fresh process; nested test runners are untouched.
    """
    import runpy
    import unittest
    import re
    if mode not in {'collect','case','observe'}:
        raise ValueError('unknown unittest adapter mode')
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    original = unittest.TextTestRunner.run
    called = False
    def identifier(test):
        cls = type(test)
        name = cls.__name__ + '.' + str(getattr(test,'_testMethodName',''))
        if (not re.fullmatch(r'[A-Za-z_]\w*\.[A-Za-z_]\w*',name)
            or '_FailedTest' in test.id() or test.id() != cls.__module__ + '.' + name):
            raise ValueError('invalid collected case: '+test.id())
        if getattr(sys.modules['__main__'],cls.__name__,None) is not cls:
            raise ValueError('case is not addressable through the normal entrypoint: '+test.id())
        if case_observer is not None:
            case_observer(test)
        return name
    def identifiers(suite):
        found = []
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                found.extend(identifiers(test))
            else:
                found.append(identifier(test))
        return found
    def save(payload):
        temporary = destination.with_suffix('.pending')
        temporary.write_text(json.dumps(payload)+'\n')
        temporary.replace(destination)
    def run(runner, suite):
        nonlocal called
        called = True
        # Tests may themselves run unittest; those runs are not this receipt.
        unittest.TextTestRunner.run = original
        ids = identifiers(suite)
        if not ids or len(ids) != len(set(ids)):
            raise ValueError('zero or duplicate discovered cases')
        if mode == 'collect':
            save({'mode':'collect','ids':ids})
            result = unittest.TestResult()
            result.testsRun = len(ids)
            return result
        if mode == 'case' and ids != [expected]:
            raise ValueError('worker discovery disagrees with required case')
        started, completed = [], []
        base = runner.resultclass
        class Result(base):
            def startTest(self, test):
                started.append(identifier(test))
                super().startTest(test)
            def stopTest(self, test):
                completed.append(identifier(test))
                super().stopTest(test)
        runner.resultclass = Result
        started_at = time.monotonic()
        result = original(runner, suite)
        completed_at = time.monotonic()
        save({'mode':mode,'discovered':ids,'started':started,'completed':completed,
              'started_at':started_at,'completed_at':completed_at,
              'tests_run':result.testsRun,'skipped':[t.id() for t,_ in result.skipped],
              'successful':result.wasSuccessful() and not result.expectedFailures and not result.skipped})
        return result
    unittest.TextTestRunner.run = run
    sys.argv = command
    # Match `python path/to/suite.py`: sibling imports belong to that script.
    sys.path.insert(0,str(Path(command[0]).resolve().parent))
    try:
        runpy.run_path(command[0], run_name='__main__')
    except SystemExit as exc:
        if exc.code not in (None,0):
            raise
    finally:
        unittest.TextTestRunner.run = original
    if not called:
        raise ValueError('entrypoint did not run its normal unittest loader')
    if mode != 'collect':
        payload = json.loads(destination.read_text())
        if not payload['successful'] or payload['started'] != payload['discovered'] or payload['completed'] != payload['discovered'] or payload['tests_run'] != len(payload['discovered']):
            raise ValueError('required case receipt is incomplete, skipped or failed')


def _case_command(mode, receipt, args, expected=None):
    bootstrap = ('import sys; sys.path.insert(0,sys.argv[1]); '
                 'from lib.validation.validation_execution import unittest_adapter\n'
                 'try: unittest_adapter(sys.argv[2],sys.argv[3],sys.argv[5:],sys.argv[4] or None)\n'
                 'except (ValueError,OSError,TypeError,KeyError) as exc:\n'
                 ' print(str(exc),file=sys.stderr); raise SystemExit(4)')
    return [args[0], '-B', '-c', bootstrap, str(Path(__file__).resolve().parents[2]),
            mode, str(receipt), expected or '', *args[1:]]


def discover_cases(args, scratch, *, jobs, timeout):
    """Isolated normal-loader collection; collection is never passing test proof."""
    scratch.mkdir(parents=True, exist_ok=True)
    receipt = scratch/'collection.json'
    receipt.unlink(missing_ok=True)
    command = _case_command('collect',receipt,args)
    plan = CheckPlan('collection',command_display(command),command,'normal loader collection','focused',True)
    result = run_scheduled_checks([plan],jobs=jobs,timeout_seconds=timeout,fail_fast=False,scratch=scratch)[0]
    if result.exit_code:
        with result.stderr_path.open(encoding='utf-8',errors='replace') as stream:
            detail = stream.read(4000)
        raise ValueError(f'case collection failed: {result.exit_reason}\n{detail}')
    try:
        payload = json.loads(receipt.read_text())
        ids = payload['ids']
        if set(payload) != {'mode','ids'} or payload['mode'] != 'collect' or not isinstance(ids,list) or not ids or any(not isinstance(x,str) or not x for x in ids) or len(ids)!=len(set(ids)):
            raise ValueError('invalid collection receipt')
        return ids
    except (OSError, KeyError, TypeError) as exc:
        raise ValueError('missing or invalid collection receipt') from exc


def case_plans(parent, ids, scratch):
    scratch.mkdir(parents=True, exist_ok=True)
    plans = []
    # Narrow original native positional selectors, rather than appending a
    # second selection to an already selected suite. Preserve options/values;
    # the original entrypoint parser still owns their vocabulary and meaning.
    targets = set(ids) | {name.split('.')[0] for name in ids}
    switches = {'-v','--verbose','-q','--quiet','--locals','-f','--failfast',
                '-c','--catch','-b','--buffer','--'}
    scoped_args = parent.args[:2]
    option_value = False
    for argument in parent.args[2:]:
        if option_value:
            scoped_args.append(argument)
            option_value = False
        elif argument.startswith('-'):
            scoped_args.append(argument)
            option_value = (argument not in switches and '=' not in argument
                            and not (argument.startswith('-k') and len(argument)>2))
        elif argument not in targets:
            scoped_args.append(argument)
    for index, name in enumerate(ids):
        args = [*scoped_args, name]
        receipt = scratch/f'case-{index}.json'
        plans.append(CheckPlan(parent.check_id+'::'+name,command_display(args),
            _case_command('case',receipt,args,name), parent.reason, parent.phase, parent.parallel_safe,
            parent.dependencies, parent.demand, parent.after, receipt, name, args))
    return plans


def _validate_case_receipt(plan):
    if plan.case_receipt is None:
        return
    try:
        data = json.loads(plan.case_receipt.read_text())
        if (set(data) != {'mode','discovered','started','completed','tests_run','skipped','successful','started_at','completed_at'}
            or data['mode'] != 'case' or data['successful'] is not True
            or type(data['tests_run']) is not int or data['tests_run'] != 1
            or type(data['started_at']) not in (int,float) or type(data['completed_at']) not in (int,float)
            or not 0 < data['started_at'] <= data['completed_at']
            or data['skipped'] != []
            or any(data[k] != [plan.case_id] for k in ('discovered','started','completed'))):
            raise ValueError('missing, skipped or disagreeing required case receipt')
    except (OSError, TypeError, KeyError, ValueError) as exc:
        raise ValueError('invalid required case receipt: '+str(exc)) from exc


def _node_command(mode, receipt, scope, expected=None):
    return ['node',str(Path(__file__).with_name('validation_node_adapter.mjs')),
            mode,str(receipt),json.dumps(scope),expected or '']


def _node_scope(args):
    if len(args)>2 and args[:2]==['node','--test'] and all(not x.startswith('-') and Path(x).is_file() for x in args[2:]):
        return {'files':[str(Path(x).resolve()) for x in args[2:]]}
    if len(args)==4 and args[:3]==['npm','test','--prefix']:
        root=Path(args[3]).resolve()
        package=json.loads((root/'package.json').read_text())
        command=shlex.split(package.get('scripts',{}).get('test',''))
        if command!=['node','--test','test/**/*.test.js']:
            raise ValueError('Node package test entrypoint requires assessed native glob')
        return {'cwd':str(root),'globPatterns':['test/**/*.test.js']}
    raise ValueError('unsupported native Node case command')


def discover_node_cases(args, scratch, *, jobs, timeout):
    scope=_node_scope(args)
    scratch.mkdir(parents=True,exist_ok=True)
    receipt=scratch/'node-collection.json'
    receipt.unlink(missing_ok=True)
    # No collection state from a previous attempt may survive a missing child.
    shutil.rmtree(str(receipt)+'.declarations',ignore_errors=True)
    command=_node_command('collect',receipt,scope)
    plan=CheckPlan('node-collection',command_display(command),command,'native Node collection','focused',True)
    result=run_scheduled_checks([plan],jobs=jobs,timeout_seconds=timeout,fail_fast=False,scratch=scratch)[0]
    if result.exit_code:
        raise ValueError('Node collection failed: '+result.stderr_path.read_text()[:4000])
    try:
        data=json.loads(receipt.read_text());groups=data['groups']
        if set(data)!={'mode','groups'} or data['mode']!='collect' or not isinstance(groups,list) or not groups:
            raise ValueError('invalid Node collection receipt')
        files=[]
        for group in groups:
            if set(group)!={'file','ids'} or not isinstance(group['file'],str) or not Path(group['file']).is_absolute():
                raise ValueError('invalid Node file identity')
            files.append(group['file']);ids=group['ids']
            if not isinstance(ids,list) or not ids or any(not isinstance(x,str) or not x for x in ids) or len(ids)!=len(set(ids)):
                raise ValueError('zero or duplicate Node case identity')
        if len(files)!=len(set(files)):
            raise ValueError('duplicate Node file identity')
        if 'files' in scope and set(files)!=set(scope['files']):
            raise ValueError('Node file discovery disagrees with required files')
        return groups
    except (OSError,KeyError,TypeError) as exc:
        raise ValueError('missing or invalid Node collection receipt') from exc


def node_case_plans(parent, groups, scratch):
    import re
    scope=_node_scope(parent.args)
    scratch.mkdir(parents=True,exist_ok=True)
    plans=[]
    for group in groups:
        file=group['file']
        label=os.path.relpath(file,Path.cwd())
        for name in group['ids']:
            native=['node','--test','--test-concurrency=1','--test-name-pattern=^'+re.sub(r'([.*+?^${}()|\[\]\\])',r'\\\1',name)+'$',file]
            rerun=native
            if 'cwd' in scope:
                rerun=['bash','-c','cd '+shlex.quote(scope['cwd'])+' && exec '+shlex.join(native)]
            receipt=scratch/f'case-{len(plans)}.json'
            selected={'files':[file],**({'cwd':scope['cwd']} if 'cwd' in scope else {})}
            plans.append(CheckPlan(parent.check_id+'::'+label+'::'+name,command_display(rerun),
                _node_command('case',receipt,selected,name),parent.reason,parent.phase,parent.parallel_safe,
                parent.dependencies,parent.demand,parent.after,receipt,name,rerun))
    return plans


class DiscoveryFailure(ValueError):
    def __init__(self, message, plans, unexpanded):
        super().__init__(message)
        self.plans, self.unexpanded = plans, unexpanded


def expand_cases(plans, scratch, *, jobs, timeout):
    """Replace only catalog-adopted suites and rebind all group dependencies."""
    validate_catalog()
    validate_plans(plans,jobs=jobs)
    groups = {}
    for index, plan in enumerate(plans):
        entry = CHECK_CATALOG.get(plan.check_id)
        try:
            if entry and entry.constraints and entry.constraints.unit == 'python-unittest':
                owned = scratch/f'suite-{index}'
                ids = discover_cases(plan.args,owned/'collection',jobs=jobs,timeout=timeout)
                groups[plan.check_id] = case_plans(plan,ids,owned/'cases')
            elif entry and entry.constraints and entry.constraints.unit == 'node-test':
                owned = scratch/f'suite-{index}'
                population = discover_node_cases(plan.args,owned/'collection',jobs=jobs,timeout=timeout)
                groups[plan.check_id] = node_case_plans(plan,population,owned/'cases')
            else:
                groups[plan.check_id] = [plan]
        except (ValueError, OSError, ExecutionFailure) as exc:
            known = [p for group in groups.values() for p in group] + list(plans[index:])
            raise DiscoveryFailure(f'{plan.check_id}: {exc}', known,
                                   [p.check_id for p in plans[index:]]) from exc
    expanded = [p for group in groups.values() for p in group]
    for plan in expanded:
        plan.dependencies = tuple(p.check_id for old in plan.dependencies for p in groups[old])
        plan.after = tuple(p.check_id for old in plan.after for p in groups[old])
    validate_plans(expanded,jobs=jobs)
    return expanded


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
        from lib.validation.validation_selection import _preflight_results, _git_local_changed_paths
        checks = _preflight_results(_git_local_changed_paths(Path.cwd()),repo_root=Path.cwd())
        blocked = [item for item in checks if item.get('result') == 'blocked']
        if blocked:
            fail('Preflight blocked: '+json.dumps(blocked),2)
    if mode == 'main':
        if not base or not head:
            base,head = _git('rev-parse','--verify','HEAD~1'),_git('rev-parse','--verify','HEAD')
        values.update({'<base>':[base],'<head>':[head]})
    else:
        dirty = _git('diff','--name-only','-z','--no-renames','--diff-filter=ACDMRT','HEAD','--','.').split('\0')
        dirty = [x for x in dirty if x]
        previous = _git('rev-parse','--verify','HEAD~1',optional=True)
        if not skip_diff_scoped:
            if os.environ.get('REVIEW_ARTIFACT_ROOTS'):
                roots = [x.rstrip('/')+'/change.json' for x in os.environ['REVIEW_ARTIFACT_ROOTS'].split()]
            else:
                changed = dirty or (_git('diff','--name-only','-z','--no-renames','--diff-filter=ACDMRT','HEAD~1','HEAD','--','.').split('\0') if previous else [])
                roots = _current_roots(changed)
        values.update({'<roots>': roots})
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


def allocate_coverage(plans):
    """Apply only reviewed, already-required catalog coverage; infer no equivalence."""
    present = {p.check_id for p in plans}
    mapping = {key: next((target for target in targets if target in present), key)
               for key, targets in COVERING_CHECK_IDS.items() if key in present}
    mapping = {key: target for key, target in mapping.items() if key != target}
    if not mapping:
        return plans
    participants = set(mapping) | set(mapping.values())
    originals = {}
    for plan in plans:
        if plan.check_id not in participants:
            continue
        entry = CHECK_CATALOG[plan.check_id]
        c = entry.constraints
        expected = COVERAGE_BASES[plan.check_id]
        if (c is None or (command_basis(entry.command_template, c.unit), c.unit) != expected
                or c.basis != expected[0] or c.mode != 'bounded' or c.demand != 1
                or c.shared_writes or not entry.parallel_safe or entry.dependencies
                or plan.args != shlex.split(entry.command_template)
                or plan.parallel_safe is not True or type(plan.demand) is not int or plan.demand != 1
                or plan.case_id is not None or plan.case_receipt is not None or plan.rerun is not None):
            raise ValueError(f'incompatible or stale coverage basis: {plan.check_id}')
        previous = originals.setdefault(plan.check_id, plan)
        if previous.dependencies != plan.dependencies or previous.after != plan.after:
            raise ValueError(f'conflicting prerequisites for canonical check {plan.check_id}')
    prerequisites = {}
    for plan in plans:
        key = mapping.get(plan.check_id, plan.check_id)
        fields = prerequisites.setdefault(key, {'dependencies': [], 'after': []})
        for field in fields:
            fields[field].extend(mapping.get(value, value) for value in getattr(plan, field))
    result = []
    for plan in plans:
        key = mapping.get(plan.check_id, plan.check_id)
        template = originals[key] if plan.check_id in mapping else plan
        fields = prerequisites[key] if key in mapping.values() else {
            field: [mapping.get(value, value) for value in getattr(plan, field)]
            for field in ('dependencies', 'after')}
        result.append(replace(template, reason=plan.reason, phase=plan.phase,
            **{field: tuple(dict.fromkeys(values)) for field, values in fields.items()}))
    return result


def expand_groups(plans, scratch, *, diagnostic=False):
    """Compose canonical IDs once, then apply the focused/boundary gate."""
    expanded, groups = [], {}
    for original in plans:
        plan = replace(original)
        if plan.check_id != 'broad_smoke.repo':
            expanded.append(plan)
            continue
        children = compose_mode('broad-smoke',scratch,skip_diff_scoped=True)
        groups[plan.check_id] = tuple(child.check_id for child in children)
        for original_child in children:
            child = replace(original_child, phase=plan.phase)
            child.dependencies = tuple(dict.fromkeys((*child.dependencies,*plan.dependencies)))
            child.after = tuple(dict.fromkeys((*child.after,*plan.after)))
            child.reason = '; '.join(x for x in (plan.reason,child.reason) if x)
            expanded.append(child)
    for plan in expanded:
        for field in ('dependencies','after'):
            setattr(plan,field,tuple(dict.fromkeys(d for key in getattr(plan,field) for d in groups.get(key,(key,)))))
    expanded = allocate_coverage(expanded)
    retained = {}
    for plan in expanded:
        if plan.phase not in {'preflight','focused','boundary'}:
            raise ValueError(f'unknown phase: {plan.phase}')
        previous = retained.get(plan.check_id)
        if previous is None:
            retained[plan.check_id] = plan
            continue
        # Same ID is an authored contract, never inferred command equivalence.
        for field in ('args','parallel_safe','demand','dependencies','after','case_receipt','case_id','rerun'):
            if type(getattr(previous,field)) is not type(getattr(plan,field)) or getattr(previous,field) != getattr(plan,field):
                raise ValueError(f'conflicting {field} for canonical check {plan.check_id}')
        previous.reason = '; '.join(dict.fromkeys(x for x in (previous.reason,plan.reason) if x)) or None
        previous.phase = min((previous.phase,plan.phase),key=('preflight','focused','boundary').index)
    result = list(retained.values())
    preflight = [p.check_id for p in result if p.phase == 'preflight']
    focused = [p.check_id for p in result if p.phase == 'focused']
    for plan in result:
        if plan.phase == 'focused':
            plan.dependencies = tuple(dict.fromkeys((*plan.dependencies,*preflight)))
        elif plan.phase == 'boundary':
            plan.dependencies = tuple(dict.fromkeys((*plan.dependencies,*preflight)))
            field = 'after' if diagnostic else 'dependencies'
            setattr(plan,field,tuple(dict.fromkeys((*getattr(plan,field),*focused))))
    return result


REPORT_MODES = frozenset({'local', 'explicit', 'pr', 'main', 'broad-smoke', 'release'})
RESULT_STATUSES = frozenset({'passed', 'exited', 'killed', 'timed out', 'unavailable', 'runner error', 'not started'})
REPORT_VARIABLES = ('RIGORLOOP_VALIDATION_RESULT_JSON', 'RIGORLOOP_BROAD_SMOKE_RESULT_JSON')


def _validate_report_values(mode, results):
    # Closed values precede path access and all consistency checks.
    if mode not in REPORT_MODES:
        raise ValueError(f'unknown validation report mode: {mode}')
    for result in results:
        if result.status not in RESULT_STATUSES:
            raise ValueError(f'unknown validation report status: {result.status}')
    identities = [r.plan.check_id for r in results]
    if any(not isinstance(value, str) or not value for value in identities) or len(set(identities)) != len(identities):
        raise ValueError('duplicate or invalid report check identity')


def _validate_durations(limit):
    if limit is not None and (type(limit) is not int or limit < 0):
        raise ValueError('durations must be a nonnegative decimal integer')


def print_durations(results, limit):
    """A sorted view of observed workers; never reorder the authoritative rows."""
    _validate_durations(limit)
    if limit is None:
        return
    measured = sorted((r for r in results if r.status != 'not started'),
                      key=lambda r: (-r.elapsed_seconds, r.plan.check_id))
    print('Slowest dispatched workers (elapsed includes startup, fixtures and cleanup):')
    for result in measured[:limit or None]:
        kind = 'case' if result.plan.case_id is not None else 'check'
        print(f'{result.elapsed_seconds:.3f}s | {kind} {result.plan.check_id} | {result.status}')
        print('Re-run: ' + command_display(result.plan.rerun or result.plan.args))
    unstarted = sum(r.status == 'not started' for r in results)
    if unstarted:
        print(f'{unstarted} unstarted workers excluded: unmeasured; required scope is incomplete.')


class ReportDestination:
    """Own a destination through dispatch and atomic publication, without lock stealing."""
    def __init__(self, mode, *, forbidden=()):
        _validate_report_values(mode, [])
        generic = os.environ.get(REPORT_VARIABLES[0])
        legacy = os.environ.get(REPORT_VARIABLES[1]) if mode == 'broad-smoke' else None
        self.path = None
        self.directory_fd = self.lock_fd = None
        self.lock_name = None
        self.lock_identity = None
        self.publication_revoked = False
        for value in (generic, legacy):
            if not value:
                continue
            supplied = Path(value)
            if '..' in supplied.parts:
                raise ValueError('unsafe traversal in report destination')
            supplied = Path(os.path.abspath(supplied))
            if any(parent.is_symlink() for parent in (*supplied.parents, supplied)):
                raise ValueError('report destination or parent is a symlink')
        if generic and legacy and Path(generic).resolve() != Path(legacy).resolve():
            raise ValueError('conflicting validation report destinations')
        destination = generic or legacy
        if not destination:
            return
        path = Path(destination)
        path = Path(os.path.abspath(path))
        if not path.parent.is_dir():
            raise ValueError('report destination parent must already exist')
        if path.name.endswith('.rigorloop-report.lock') or path.name.startswith('.rigorloop-report-'):
            raise ValueError('report destination collides with an owned output')
        self.path = path
        self.reject_collisions(forbidden)
        repository = Path(__file__).resolve().parents[3]
        if path.is_relative_to(repository):
            relative = path.relative_to(repository)
            if not relative.parts:
                raise ValueError('report destination must be an absent or regular single-link file')
            # Absent source paths are protected too, not only tracked files.
            if relative.parts[0] in {'scripts', 'tests', 'skills', 'schemas', 'templates', 'packages', 'docs', 'dist', '.git', '.agents', '.github', '.codex'}:
                raise ValueError('report destination collides with repository source')
            tracked = subprocess.run(['git', 'ls-files', '--error-unmatch', '--', str(relative)],
                                     cwd=repository, capture_output=True).returncode == 0
            if tracked:
                raise ValueError('report destination collides with repository source')
        self.directory_fd = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
        try:
            for part in path.parent.parts[1:]:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=self.directory_fd)
                os.close(self.directory_fd)
                self.directory_fd = child
        except BaseException:
            self.close()
            raise
        try:
            self._check_target()
            self.lock_name = '.' + path.name + '.rigorloop-report.lock'
            try:
                self.lock_fd = os.open(self.lock_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                       0o600, dir_fd=self.directory_fd)
            except FileExistsError as exc:
                raise ValueError('validation report destination is reserved by another owner') from exc
            self.lock_identity = os.fstat(self.lock_fd)
        except BaseException:
            self.close()
            raise

    def reject_collisions(self, paths):
        if self.path is None:
            return
        for value in paths:
            if not value:
                continue
            other = Path(value).resolve()
            if self.path == other or (other.is_dir() and self.path.is_relative_to(other)):
                self.publication_revoked = True
                raise ValueError(f'report destination collides with selected input or owned output: {value}')

    def _check_target(self):
        try:
            target = os.stat(self.path.name, dir_fd=self.directory_fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        if not stat.S_ISREG(target.st_mode) or target.st_nlink != 1:
            raise ValueError('report destination must be an absent or regular single-link file')

    def publish(self, payload):
        if self.publication_revoked:
            raise ValueError('report publication revoked after destination collision')
        if self.path is None:
            return
        # Serialization precedes temp creation and replacement, preserving old bytes.
        encoded = (json.dumps(payload, indent=2) + '\n').encode('utf-8')
        self._check_target()
        # The parent descriptor pins every operation even if an ancestor is renamed.
        name = '.rigorloop-report-' + os.urandom(12).hex()
        descriptor = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600, dir_fd=self.directory_fd)
        try:
            with os.fdopen(descriptor, 'wb') as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
            self._check_target()
            os.replace(name, self.path.name, src_dir_fd=self.directory_fd, dst_dir_fd=self.directory_fd)
        finally:
            try:
                os.unlink(name, dir_fd=self.directory_fd)
            except FileNotFoundError:
                pass

    def close(self):
        if self.lock_fd is not None:
            try:
                current = os.stat(self.lock_name, dir_fd=self.directory_fd, follow_symlinks=False)
                if (current.st_dev, current.st_ino) == (self.lock_identity.st_dev, self.lock_identity.st_ino):
                    os.unlink(self.lock_name, dir_fd=self.directory_fd)
            except FileNotFoundError:
                pass
            finally:
                os.close(self.lock_fd)
                self.lock_fd = None
        if self.directory_fd is not None:
            os.close(self.directory_fd)
            self.directory_fd = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def _output_bytes(result):
    if result.output_bytes is not None:
        return result.output_bytes
    return sum(p.stat().st_size for p in (result.stdout_path, result.stderr_path) if p and p.exists())


def _write_mode_result(results, *, mode, jobs, elapsed, code, skip_diff_scoped,
                       scope=None, report_owner=None, command=None):
    _validate_report_values(mode, results)
    if report_owner is None:
        with ReportDestination(mode) as owner:
            return _write_mode_result(results, mode=mode, jobs=jobs, elapsed=elapsed, code=code,
                                      skip_diff_scoped=skip_diff_scoped, scope=scope,
                                      report_owner=owner, command=command)
    if report_owner.path is None:
        return
    children = [dict(check_id=r.plan.check_id, command=command_display(r.plan.args),
        duration_ms=max(0, round(r.elapsed_seconds*1000)) if r.status != 'not started' else 0,
        case_id=r.plan.case_id, started=r.status != 'not started',
        rerun=command_display(r.plan.rerun or r.plan.args),
        phase='parallel' if r.plan.parallel_safe and jobs>1 else 'sequential',
        result='passed' if r.exit_code==0 else 'failed', exit_code=r.exit_code,
        output_bytes=_output_bytes(r), cache_status='not-applicable', status=r.status,
        exit_reason=r.exit_reason) for r in results]
    scope = dict(scope or dict(requested_paths=[], base='', head='',
        selected_check_ids=[r.plan.check_id for r in results], collection_complete=False,
        unexpanded_checks=[], limits=['Direct result writer has no selector/discovery receipt.']))
    expected = scope.get('expected_worker_ids')
    accounted = (isinstance(expected, list) and len(expected) == len(results)
                 and set(expected) == {r.plan.check_id for r in results})
    scope['complete'] = bool(accounted and scope.get('collection_complete') and not scope.get('unexpanded_checks')
                             and not code and all(r.status == 'passed' and r.exit_code == 0 for r in results))
    node = subprocess.run(['node', '--version'], text=True, capture_output=True) if shutil.which('node') else None
    payload = dict(scenario='broad-smoke-safe-parallelism' if mode == 'broad-smoke' else f'{mode}-validation',
        mode=mode, scope=scope,
        command=command or f'bash scripts/ci.sh --mode {mode} '+('--skip-diff-scoped ' if skip_diff_scoped else '')+f'--jobs {jobs}',
        measurement=dict(worker='Monotonic launch attempt through result and owned-process cleanup; excludes queue and discovery.',
            wall='Monotonic case discovery through scheduled work and owned-process cleanup; excludes selection, preflight and report formatting/I/O.',
            summed_worker_time='Occupied worker time, not CPU usage, wall time or a speedup estimate.',
            unstarted='Zero duration with started=false is an unmeasured placeholder.'),
        environment=dict(os=platform.platform(), shell=os.environ.get('SHELL','unknown'),
            cpu_class=f'{os.cpu_count() or 1} logical CPUs', local_or_ci='ci' if os.environ.get('CI') else 'local',
            python=platform.python_version(), node=node.stdout.strip() if node and node.returncode == 0 else None,
            worker_budget=jobs),
        repository_state=dict(head=_git('rev-parse','HEAD',optional=True),worktree_state='dirty' if _git('status','--short',optional=True) else 'clean'),
        baseline=dict(total_duration_ms=None,child_durations=[]),
        parallel=dict(jobs=jobs,total_duration_ms=max(0,round(elapsed*1000)),exit_code=code,child_durations=children),
        delta=dict(duration_ms=None,percent=None),
        preservation=dict(child_set_preserved=bool(accounted and scope.get('collection_complete') and not scope.get('unexpanded_checks')),
            exit_behavior_preserved=scope['complete'],diagnostics_preserved=accounted,output_order_preserved=accounted),
        notes=dict(variance='Current invocation only; historical baseline unavailable by design.',low_confidence_children=[],
            sequential_only_children=[r.plan.check_id for r in results if not r.plan.parallel_safe or jobs==1],default_promotion_decision='assessed_independent_work_uses_shared_budget'))
    report_owner.publish(payload)


class _ReportingRun:
    def __init__(self, mode, jobs, *, base='', head='', paths=(), skip=False, durations=None, owner=None):
        _validate_report_values(mode, [])
        _validate_durations(durations)
        if type(jobs) is not int or jobs < 1:
            raise ValueError('jobs must be a positive integer')
        if 'RIGORLOOP_VALIDATION_WORKERS' in os.environ:
            parent = os.environ['RIGORLOOP_VALIDATION_WORKERS']
            if not parent.isascii() or not parent.isdigit() or int(parent) < 1:
                raise ValueError('parent worker allocation must be a positive integer')
            jobs = min(jobs, int(parent))
        self.mode, self.jobs, self.skip, self.durations, self.owner = mode, jobs, skip, durations, owner
        self.scope = dict(requested_paths=list(paths), base=base, head=head, selected_check_ids=[],
                          collection_complete=False, unexpanded_checks=[], limits=[])
        self.results, self.plans = [], []
        self.started_at = None
        self.elapsed = 0
        self.prepared_payload = None
        self.selection_recorded = False

    def selected(self, plans):
        self.plans = plans
        if not self.selection_recorded:
            self.scope['selected_check_ids'] = [p.check_id for p in plans]
            self.selection_recorded = True
        self.scope['unexpanded_checks'] = [p.check_id for p in plans]
        self.owner.reject_collisions([value for p in plans for value in p.args if value and not value.startswith('-')])

    def execute(self, plans, scratch, *, timeout, fast):
        self.owner.reject_collisions([scratch])
        self.selected(plans)
        self.started_at = time.monotonic()
        try:
            self.plans = expand_cases(plans, scratch, jobs=self.jobs, timeout=timeout)
        except DiscoveryFailure as exc:
            self.plans = exc.plans
            self.scope['unexpanded_checks'] = exc.unexpanded
            raise
        self.scope['collection_complete'] = True
        self.scope['unexpanded_checks'] = []
        self.scope['expected_worker_ids'] = [p.check_id for p in self.plans]
        try:
            self.results = run_scheduled_checks(self.plans, jobs=self.jobs, timeout_seconds=timeout,
                                                fail_fast=fast, scratch=scratch)
            if (len(self.results) != len(self.plans)
                    or {r.plan.check_id for r in self.results} != set(self.scope['expected_worker_ids'])):
                raise ExecutionFailure('missing or unexpected required worker results', self.results)
        except ExecutionFailure as exc:
            self.results = exc.results
            raise
        finally:
            self.elapsed = time.monotonic() - self.started_at
            for result in self.results:
                result.output_bytes = _output_bytes(result)
        return self.results

    def finish(self, code, diagnostic=None):
        if self.prepared_payload is not None:
            code = code or self.prepared_payload['parallel']['exit_code']
            self.prepared_payload['parallel']['exit_code'] = code
            if code:
                self.prepared_payload['scope']['complete'] = False
                self.prepared_payload['preservation']['exit_behavior_preserved'] = False
            try:
                self.owner.publish(self.prepared_payload)
            except (OSError, ValueError, TypeError) as exc:
                print(f'Validation report publication failed: {exc}', file=sys.stderr)
                return code or 1
            return code
        if diagnostic:
            self.scope['limits'].append(str(diagnostic))
        if not self.scope['collection_complete']:
            self.scope['limits'].append('Selection/preflight or native collection did not complete; undiscovered cases have no fabricated rows.')
        known = {r.plan.check_id for r in self.results}
        self.results.extend(_not_started(p, 'invocation stopped before dispatch') for p in self.plans if p.check_id not in known)
        if self.started_at is not None and not self.elapsed:
            self.elapsed = time.monotonic() - self.started_at
        print_durations(self.results, self.durations)
        try:
            _write_mode_result(self.results, mode=self.mode, jobs=self.jobs, elapsed=self.elapsed,
                code=code, skip_diff_scoped=self.skip, scope=self.scope, report_owner=self.owner)
        except (OSError, ValueError, TypeError) as exc:
            print(f'Validation report publication failed: {exc}', file=sys.stderr)
            return code or 1
        return code


def _reported_call(callback, run, *, forbidden=()):
    owned = run.owner is None
    if owned:
        run.owner = ReportDestination(run.mode, forbidden=forbidden)
    else:
        run.owner.reject_collisions(forbidden)
    code, diagnostic, pending = 0, None, None
    previous_handlers = {}
    def interrupt(number, frame):
        raise SystemExit(128 + number)
    try:
        for number in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[number] = signal.signal(number, interrupt)
        callback(run)
    except SystemExit as exc:
        code = exc.code or 0
    except (Exception, KeyboardInterrupt) as exc:
        code = next((r.exit_code for r in run.results if r.exit_code),
                    130 if isinstance(exc, KeyboardInterrupt) else 4)
        diagnostic, pending = str(exc), exc
    finally:
        try:
            code = run.finish(code, diagnostic)
        finally:
            try:
                if owned:
                    run.owner.close()
            finally:
                for number, handler in previous_handlers.items():
                    signal.signal(number, handler)
    if pending is not None:
        print(f'Invalid validation execution: {pending}', file=sys.stderr)
    raise SystemExit(code)

def composed_main(argv, *, durations=None, report_owner=None):
    mode, jobs, timeout, fast, verbose, base, head, skip = argv
    run = _ReportingRun(mode, int(jobs), base=base, head=head, skip=bool(int(skip)),
                        durations=durations, owner=report_owner)
    return _reported_call(lambda session: _composed_main(argv, session), run)


def _composed_main(argv, run):
    mode, jobs, timeout, fast, verbose, base, head, skip = argv
    jobs,timeout,fast,verbose,skip = int(jobs),int(timeout),bool(int(fast)),bool(int(verbose)),bool(int(skip))
    jobs = run.jobs
    with tempfile.TemporaryDirectory(prefix='rigorloop-validation-') as temporary:
        scratch = Path(temporary)
        plans = compose_mode(mode,scratch,base=base,head=head,skip_diff_scoped=skip)
        validate_plans(plans,jobs=jobs)
        run.selected(plans)
        if mode == 'main':
            print(f'Direct deterministic product and governance gates ({mode})')
        if os.environ.get('RIGORLOOP_CI_DIRECT_DRY_RUN') == '1':
            for plan in plans:
                print('==> '+(plan.reason or plan.check_id))
                print('+ '+command_display(plan.args))
            print('[PASS] direct gate graph selected without execution')
            run.scope['limits'].append('Dry run selected checks without discovery or dispatch.')
            return
        results = run.execute(plans, scratch, timeout=timeout, fast=fast)
        for result in results:
            if result.exit_code or verbose:
                label = result.plan.reason or result.plan.check_id
                if result.exit_code:
                    print(f'[FAIL] {result.plan.check_id} / {label}: exit {result.exit_code} in {result.elapsed_seconds:.2f}s')
                    print('Check ID:\n'+result.plan.check_id)
                    print('Command:\n'+command_display(result.plan.args))
                    print('Execution phase:\n'+('parallel' if result.plan.parallel_safe and jobs>1 else 'sequential'))
                    print('Captured output:')
                    print('Re-run:\n'+command_display(result.plan.rerun or result.plan.args))
                else:
                    print(f'==> {label} (passed)')
                print_result_output([result],verbose=True)
        code = next((r.exit_code for r in results if r.exit_code),0)
        if code or verbose or mode == "main":
            print_summary(results)
        if not code:
            print(f'[PASS] {mode}: {len(results)} checks passed in {run.elapsed:.2f}s')
        raise SystemExit(code)


def selected_main(argv, *, durations=None, report_owner=None):
    run = _ReportingRun(argv[6], int(argv[4]), base=argv[7], head=argv[8], paths=argv[9:],
                        durations=durations, owner=report_owner)
    return _reported_call(lambda session: _selected_main(argv, session), run,
                          forbidden=[argv[0], *argv[9:]])


def _selected_main(argv, run):
    selector_output = Path(argv[0])
    selector_exit = int(argv[1])
    timeout_seconds = int(argv[2])
    verbose = bool(int(argv[3]))
    jobs = run.jobs
    fail_fast = bool(int(argv[5]))
    requested_mode, requested_base, requested_head = argv[6:9]
    requested_paths = argv[9:]
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
    if status not in {'ok', 'blocked', 'fallback', 'error'}:
        fail(f"Unsupported selector status: {status}")
    run.scope['selector_status'] = status
    run.scope['selection_diagnostics'] = dict(blocking_results=payload['blocking_results'],
                                             preflight_results=payload['preflight_results'])
    run.owner.reject_collisions(payload['changed_paths'])
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
                _composed_main(['broad-smoke',str(jobs),str(timeout_seconds),str(int(fail_fast)),str(int(verbose)),requested_base,requested_head,'1'], run)
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
        run.scope['collection_complete'] = True
        run.scope['expected_worker_ids'] = []
        print("No selected checks to run.")
        raise SystemExit(0)

    validate_catalog()
    plans: list[CheckPlan] = []
    run.plans = plans
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
        run.scope['selected_check_ids'] = [plan.check_id for plan in plans]
        run.scope['unexpanded_checks'] = list(run.scope['selected_check_ids'])

    for plan in plans:
        if not plan.parallel_safe:
            print(f"Serial: {plan.check_id}: " + (CHECK_CATALOG[plan.check_id].constraints.isolation if CHECK_CATALOG[plan.check_id].constraints else "isolation/nested demand not yet assessed"))
        print(f"==> Run selected check: {plan.check_id}")
        print(f"Phase: {plan.phase}")
        if plan.reason:
            print(f"Reason: {plan.reason}")
        if plan.check_id != "broad_smoke.repo":
            print("+ " + command_display(plan.args))

    boundary_required = any(p.phase == "boundary" for p in plans)
    run.selected(plans)
    with tempfile.TemporaryDirectory(prefix="rigorloop-validation-") as temporary:
        plans = expand_groups(plans,Path(temporary),diagnostic=diagnostic)
        results = run.execute(plans, Path(temporary), timeout=timeout_seconds, fast=fail_fast)

        print_summary(results, boundary_required=boundary_required)
        print_result_output(results, verbose=verbose)

        failed_results = [result for result in results if result.status != "passed"]
        if failed_results:
            for result in failed_results:
                print(f"Selected check {result.plan.check_id} failed: {result.exit_reason}", file=sys.stderr)
            raise SystemExit(failed_results[0].exit_code)

        print("Selected CI checks passed.")


def ci_main(argv):
    """Keep shell selection/preparation inside the same report ownership lifetime."""
    mode, jobs, timeout, fast, verbose, base, head, skip, release, broad, durations, count = argv[:12]
    paths = argv[12:12+int(count)]
    original = argv[12+int(count):]
    limit = None if durations == '' else int(durations)
    run = _ReportingRun(mode, int(jobs), base=base, head=head, paths=paths,
                        skip=bool(int(skip)), durations=limit)
    fixture = os.environ.get('RIGORLOOP_SELECTOR_FIXTURE')
    argv_file = os.environ.get('RIGORLOOP_CI_SELECTOR_ARGV_FILE')

    def invoke(session):
        with tempfile.TemporaryDirectory(prefix='rigorloop-ci-selection-') as temporary:
            scratch = Path(temporary)
            session.owner.reject_collisions([scratch])
            if mode in {'pr', 'main'} and os.environ.get('RIGORLOOP_CI_DIRECT_DRY_RUN') != '1' and not fixture:
                child_report = scratch / 'prepared-result.json'
                env = os.environ.copy()
                for key in (*REPORT_VARIABLES, 'RIGORLOOP_CI_PREPARED_RESULT_JSON'):
                    env.pop(key, None)
                if session.owner.path is not None:
                    env['RIGORLOOP_CI_PREPARED_RESULT_JSON'] = str(child_report)
                result = subprocess.run([sys.executable, 'scripts/release-coordinator.py', 'check-ci', *original], env=env)
                if result.returncode != 3:
                    code = result.returncode
                    if session.owner.path is not None and child_report.is_file():
                        payload = json.loads(child_report.read_text())
                        if not isinstance(payload, dict) or payload.get('mode') != mode:
                            raise ValueError('prepared validation report mode disagrees with invocation')
                        rows = payload['parallel']['child_durations']
                        if not isinstance(rows, list) or any(row.get('status') not in RESULT_STATUSES for row in rows):
                            raise ValueError('unknown prepared validation report status')
                        payload['preparation'] = dict(requested_mode=mode, requested_paths=list(paths),
                                                      requested_base=base, requested_head=head)
                        session.prepared_payload = payload
                    elif session.owner.path is not None:
                        session.scope['limits'].append('Prepared validation did not supply its private report; no prepared case observations are available.')
                        code = code or 1
                    raise SystemExit(code)
            if mode in {'main', 'broad-smoke'}:
                return _composed_main([mode,jobs,timeout,fast,verbose,base,head,skip], session)
            selector = ['python', 'scripts/select-validation.py', '--mode', mode]
            for path in paths:
                selector.extend(['--path', path])
            for option, value in (('--base', base), ('--head', head), ('--release-version', release)):
                if value:
                    selector.extend([option, value])
            if broad == '1':
                selector.append('--broad-smoke')
            if argv_file:
                Path(argv_file).write_text('\n'.join(selector) + '\n')
            output = scratch / 'selection.json'
            if fixture:
                shutil.copyfile(fixture, output)
                selector_exit = int(os.environ.get('RIGORLOOP_SELECTOR_FIXTURE_EXIT', '0'))
            else:
                env = os.environ.copy()
                for key in (*REPORT_VARIABLES, 'RIGORLOOP_CI_PREPARED_RESULT_JSON'):
                    env.pop(key, None)
                with output.open('wb') as handle:
                    selector_exit = subprocess.run(selector, stdout=handle, env=env).returncode
            return _selected_main([str(output),str(selector_exit),timeout,verbose,jobs,fast,mode,base,head,*paths], session)
    return _reported_call(invoke, run, forbidden=[fixture, argv_file, *paths])
