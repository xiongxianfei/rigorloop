"""Execution cost, incomplete scope and owned result publication (VAL-SR-36–38)."""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from lib.validation import validation_execution as execution


class ReportingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='validation-report-test-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.destination = self.root / 'result.json'
        self.environment = patch.dict(os.environ, {}, clear=False)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        for key in ('RIGORLOOP_VALIDATION_RESULT_JSON', 'RIGORLOOP_BROAD_SMOKE_RESULT_JSON'):
            os.environ.pop(key, None)

    def result(self, name, seconds=1.25, *, status='passed', code=0):
        plan = execution.CheckPlan(name, 'python -c pass', ['python', '-c', 'pass'],
                                   None, 'focused', True, rerun=['python', '-c', 'pass'])
        return execution.CheckResult(plan, status, 'ok' if code == 0 else 'fixture failure',
                                     seconds, None, None, code)

    def write(self, rows=(), *, mode='explicit'):
        execution._write_mode_result(list(rows), mode=mode, jobs=2, elapsed=2,
                                     code=next((r.exit_code for r in rows if r.exit_code), 0),
                                     skip_diff_scoped=False)

    def test_generic_report_supports_all_modes_and_preserves_legacy_envelope(self):
        os.environ['RIGORLOOP_VALIDATION_RESULT_JSON'] = str(self.destination)
        for mode in ('local', 'explicit', 'pr', 'main', 'broad-smoke', 'release'):
            with self.subTest(mode=mode):
                self.write([self.result('fixture')], mode=mode)
                report = json.loads(self.destination.read_text())
                self.assertEqual(report['mode'], mode)
                self.assertEqual(report['parallel']['jobs'], 2)
                self.assertEqual(report['parallel']['total_duration_ms'], 2000)
                row, = report['parallel']['child_durations']
                self.assertEqual(row['check_id'], 'fixture')
                self.assertEqual(row['duration_ms'], 1250)
                self.assertTrue(row['started'])
                self.assertIsNone(row['case_id'])
                self.assertEqual(row['status'], 'passed')
                self.assertEqual(row['rerun'], 'python -c pass')
                for key in ('environment', 'repository_state', 'baseline', 'delta', 'preservation'):
                    self.assertIn(key, report)
                self.assertIn('measurement', report)
                self.assertIn('scope', report)
                if mode == 'broad-smoke':
                    self.assertEqual(report['scenario'], 'broad-smoke-safe-parallelism')

    def test_legacy_destination_remains_ignored_outside_broad_smoke(self):
        os.environ['RIGORLOOP_BROAD_SMOKE_RESULT_JSON'] = str(self.destination)
        self.write()
        self.assertFalse(self.destination.exists())
        self.write(mode='broad-smoke')
        self.assertTrue(self.destination.is_file())

    def test_equal_destinations_write_once_and_conflicting_destinations_preserve_both(self):
        os.environ['RIGORLOOP_VALIDATION_RESULT_JSON'] = str(self.destination)
        os.environ['RIGORLOOP_BROAD_SMOKE_RESULT_JSON'] = str(self.root / '.' / 'result.json')
        self.write(mode='broad-smoke')
        before = self.destination.read_bytes()
        other = self.root / 'other.json'
        other.write_bytes(b'other sentinel')
        os.environ['RIGORLOOP_BROAD_SMOKE_RESULT_JSON'] = str(other)
        with self.assertRaisesRegex(ValueError, 'conflict|different'):
            self.write(mode='broad-smoke')
        self.assertEqual(self.destination.read_bytes(), before)
        self.assertEqual(other.read_bytes(), b'other sentinel')

    def test_unsafe_destinations_preserve_the_original_object(self):
        original = self.root / 'original.json'
        original.write_bytes(b'original sentinel')
        symlink = self.root / 'symlink.json'
        symlink.symlink_to(original)
        hardlink = self.root / 'hardlink.json'
        os.link(original, hardlink)
        directory = self.root / 'directory'
        directory.mkdir()
        for destination in (symlink, hardlink, directory, ROOT, self.root / 'missing' / 'out.json',
                            ROOT / 'scripts/lib/validation/validation_execution.py'):
            with self.subTest(destination=destination):
                os.environ['RIGORLOOP_VALIDATION_RESULT_JSON'] = str(destination)
                with self.assertRaises((ValueError, OSError)):
                    self.write()
                self.assertEqual(original.read_bytes(), b'original sentinel')
        self.assertTrue(symlink.is_symlink())
        self.assertTrue(directory.is_dir())

    def test_failed_atomic_replacement_preserves_prior_bytes_and_cleans_owned_files(self):
        self.destination.write_bytes(b'prior report')
        os.environ['RIGORLOOP_VALIDATION_RESULT_JSON'] = str(self.destination)
        before = set(self.root.iterdir())
        with patch.object(execution.os, 'replace', side_effect=OSError('replacement denied')):
            with self.assertRaises(OSError):
                self.write()
        self.assertEqual(self.destination.read_bytes(), b'prior report')
        self.assertEqual(set(self.root.iterdir()), before)

    def test_unknown_mode_and_status_reject_before_destination_consistency(self):
        os.environ['RIGORLOOP_VALIDATION_RESULT_JSON'] = str(self.root / 'absent' / 'out.json')
        with self.assertRaisesRegex(ValueError, 'mode'):
            self.write(mode='unknown_value')
        with self.assertRaisesRegex(ValueError, 'status'):
            self.write([self.result('bad', status='unknown_value')])
        self.assertFalse((self.root / 'absent').exists())

    def test_never_started_work_remains_unmeasured_and_unsuccessful(self):
        os.environ['RIGORLOOP_VALIDATION_RESULT_JSON'] = str(self.destination)
        row = execution._not_started(self.result('queued').plan, 'failed prerequisite: first')
        self.write([row])
        report = json.loads(self.destination.read_text())
        actual, = report['parallel']['child_durations']
        self.assertFalse(actual['started'])
        self.assertEqual(actual['duration_ms'], 0)
        self.assertEqual(actual['status'], 'not started')
        self.assertNotEqual(actual['exit_code'], 0)
        self.assertFalse(report['scope']['complete'])

    def test_public_empty_selection_report_and_duration_argument(self):
        selection = self.root / 'selection.json'
        selection.write_text(json.dumps(dict(mode='explicit', status='ok', changed_paths=[],
            classified_paths=[], unclassified_paths=[], selected_checks=[], affected_roots=[],
            broad_smoke_required=False, blocking_results=[], preflight_results=[], rationale=[])))
        env = {**os.environ, 'RIGORLOOP_SELECTOR_FIXTURE':str(selection),
               'RIGORLOOP_VALIDATION_RESULT_JSON':str(self.destination)}
        result = subprocess.run(['bash','scripts/ci.sh','--mode','explicit','--durations','0'],
                                cwd=ROOT, env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(self.destination.read_text())['parallel']['child_durations'], [])
        before = self.destination.read_bytes()
        for value in ('-1', 'unknown_value', '1.5', ''):
            result = subprocess.run(['bash','scripts/ci.sh','--mode','explicit','--durations',value],
                                    cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('duration', result.stderr.lower())
            self.assertEqual(self.destination.read_bytes(), before)


    def start_composed(self, body, *, destination=None, second_body=None, fail_fast=False, fail_report=False, timeout=20):
        # Replace only scope selection. Native scheduler, workers, report ownership
        # and finalization remain real; this does not certify actual mode membership.
        code = """import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from lib.validation import validation_execution as e
body, second, fast, report_fault, timeout=json.loads(sys.argv[2])
if report_fault:
    def deny_replace(*args, **kwargs): raise OSError("fixture replacement denied")
    e.os.replace=deny_replace
def scope(*args, **kwargs):
    plans=[e.CheckPlan('first','fixture',[sys.executable,'-c',body],None,'focused',True)]
    if second is not None:
        plans.append(e.CheckPlan('second','fixture',[sys.executable,'-c',second],None,'focused',True,('first',)))
    return plans
e.compose_mode=scope
try:
    e.composed_main(['broad-smoke','1',str(timeout),str(int(fast)),'0','','','1'])
except (ValueError,OSError,TypeError,KeyError) as exc:
    print(str(exc),file=sys.stderr);raise SystemExit(4)
"""
        env = {**os.environ, 'RIGORLOOP_VALIDATION_RESULT_JSON':str(destination or self.destination)}
        process = subprocess.Popen([sys.executable,'-c',code,str(ROOT/'scripts'),
                                    json.dumps([body,second_body,fail_fast,fail_report,timeout])],
                                   cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        def cleanup():
            if process.poll() is None:
                process.terminate()
                try:
                    process.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill();process.communicate()
        self.addCleanup(cleanup)
        return process

    def test_invocation_reserves_destination_before_workers_and_preserves_concurrent_owner(self):
        entered, release, forbidden = [self.root / n for n in ('entered','release','forbidden')]
        self.destination.write_bytes(b'prior report')
        body = (f'from pathlib import Path; import time; Path({str(entered)!r}).touch(); '
                f'p=Path({str(release)!r}); end=time.monotonic()+15\n'
                'while not p.exists() and time.monotonic()<end: time.sleep(.02)\n'
                'assert p.exists()')
        first = self.start_composed(body)
        deadline = time.monotonic()+10
        while not entered.exists() and first.poll() is None and time.monotonic()<deadline:
            time.sleep(.02)
        self.assertTrue(entered.exists(), 'first worker never entered')
        second = self.start_composed(f'from pathlib import Path; Path({str(forbidden)!r}).touch()')
        out, err = second.communicate(timeout=10)
        self.assertNotEqual(second.returncode, 0, out+err)
        self.assertRegex((out+err).lower(), 'conflict|reserved|owner|busy')
        self.assertFalse(forbidden.exists())
        self.assertEqual(self.destination.read_bytes(), b'prior report')
        release.touch()
        out, err = first.communicate(timeout=20)
        self.assertEqual(first.returncode, 0, out+err)
        rows=json.loads(self.destination.read_text())['parallel']['child_durations']
        self.assertEqual([r['check_id'] for r in rows], ['first'])
        self.assertEqual(set(p.name for p in self.root.iterdir()), {'entered','release','result.json'})

    def test_failed_worker_preserves_exit_and_reports_blocked_dependent_without_launch(self):
        forbidden=self.root/'forbidden'
        process=self.start_composed('raise SystemExit(7)', second_body=
            f'from pathlib import Path; Path({str(forbidden)!r}).touch()')
        out,err=process.communicate(timeout=20)
        self.assertEqual(process.returncode,7,out+err)
        self.assertFalse(forbidden.exists())
        report=json.loads(self.destination.read_text())
        first,second=report['parallel']['child_durations']
        self.assertTrue(first['started'])
        self.assertFalse(second['started'])
        self.assertEqual(first['exit_code'],7)
        self.assertEqual(second['status'],'not started')
        self.assertGreater(first['duration_ms'],0)
        self.assertFalse(report['scope']['complete'])

    def test_both_parent_destinations_are_removed_from_real_worker_environment(self):
        legacy=self.root/'legacy.json'
        legacy.write_bytes(b'legacy sentinel')
        os.environ['RIGORLOOP_BROAD_SMOKE_RESULT_JSON']=str(self.destination)
        os.environ['REPORT_UNRELATED']='preserved'
        process=self.start_composed('import os; '
            'assert "RIGORLOOP_VALIDATION_RESULT_JSON" not in os.environ; '
            'assert "RIGORLOOP_BROAD_SMOKE_RESULT_JSON" not in os.environ; '
            'assert os.environ["REPORT_UNRELATED"] == "preserved"; '
            'assert os.environ["RIGORLOOP_VALIDATION_WORKERS"] == "1"')
        out,err=process.communicate(timeout=20)
        self.assertEqual(process.returncode,0,out+err)
        self.assertEqual(legacy.read_bytes(),b'legacy sentinel')


    def test_duration_view_sorts_ties_without_mutating_results_and_excludes_unstarted(self):
        rows=[self.result('fast-a-case', 1), self.result('slow-c-case', 2),
              self.result('slow-b-case', 2, status='exited', code=7),
              execution._not_started(self.result('never-dispatched').plan, 'failed prerequisite')]
        original=[row.plan.check_id for row in rows]
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            execution.print_durations(rows, 0)
        text=output.getvalue()
        self.assertLess(text.index('slow-b-case'), text.index('slow-c-case'))
        self.assertLess(text.index('slow-c-case'), text.index('fast-a-case'))
        self.assertNotIn('never-dispatched', text)
        self.assertEqual([row.plan.check_id for row in rows], original)
        output=io.StringIO()
        with contextlib.redirect_stdout(output):
            execution.print_durations(rows, 2)
        self.assertNotIn('fast-a-case', output.getvalue())
        self.assertIn('exited', output.getvalue())
        self.assertRegex(output.getvalue().lower(), 'unstarted|not.started|unmeasured')
        for invalid in (-1, True, 'unknown_value', 1.5):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                execution.print_durations(rows, invalid)

    def test_failed_launch_records_measured_attempt_overhead(self):
        plan=execution.CheckPlan('missing-command', 'missing command',
            ['rigorloop-nonexistent-case-command'], None, 'focused', True)
        ticks=iter(range(100))
        with patch.object(execution.time, 'monotonic', side_effect=lambda:next(ticks)):
            row,=execution.run_scheduled_checks([plan], jobs=1, timeout_seconds=5,
                fail_fast=False, scratch=self.root/'worker')
        self.assertEqual(row.status, 'unavailable')
        self.assertEqual(row.exit_code, 127)
        self.assertGreater(row.elapsed_seconds, 0)


    def test_report_failure_changes_success_to_one_but_preserves_existing_failure(self):
        for worker_code, expected in ((0,1),(7,7)):
            with self.subTest(worker_code=worker_code):
                self.destination.write_bytes(b'prior report')
                process=self.start_composed(f'raise SystemExit({worker_code})', fail_report=True)
                out,err=process.communicate(timeout=20)
                self.assertEqual(process.returncode,expected,out+err)
                self.assertIn('report', (out+err).lower())
                self.assertEqual(self.destination.read_bytes(),b'prior report')
                self.assertEqual(set(self.root.iterdir()),{self.destination})

    def test_failed_serialization_preserves_prior_report_and_reservation_cleanup(self):
        self.destination.write_bytes(b'prior report')
        os.environ['RIGORLOOP_VALIDATION_RESULT_JSON']=str(self.destination)
        with patch.object(execution.json,'dumps',side_effect=ValueError('serialization fault')):
            with self.assertRaises(ValueError):
                self.write()
        self.assertEqual(self.destination.read_bytes(),b'prior report')
        self.assertEqual(set(self.root.iterdir()),{self.destination})


    def test_selection_input_collision_rejects_without_overwriting_the_fixture(self):
        selection=self.root/'selection.json'
        contents=json.dumps(dict(mode='explicit',status='ok',changed_paths=[],classified_paths=[],
            unclassified_paths=[],selected_checks=[],affected_roots=[],broad_smoke_required=False,
            blocking_results=[],preflight_results=[],rationale=[]))
        selection.write_text(contents)
        env={**os.environ,'RIGORLOOP_SELECTOR_FIXTURE':str(selection),
             'RIGORLOOP_VALIDATION_RESULT_JSON':str(selection)}
        result=subprocess.run(['bash','scripts/ci.sh','--mode','explicit'],cwd=ROOT,env=env,
                              capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(selection.read_text(),contents)

    def test_late_selected_input_collision_preserves_bytes_and_releases_reservation(self):
        selection = self.root / 'selection.json'
        payload = dict(mode='local', status='ok', changed_paths=[], classified_paths=[],
                       unclassified_paths=[], selected_checks=[], affected_roots=[],
                       broad_smoke_required=False, blocking_results=[], preflight_results=[],
                       rationale=[])
        env = {**os.environ, 'RIGORLOOP_SELECTOR_FIXTURE': str(selection),
               'RIGORLOOP_VALIDATION_RESULT_JSON': str(self.destination)}
        selection.write_text(json.dumps(payload))
        control = subprocess.run(['bash', 'scripts/ci.sh', '--mode', 'local'],
                                 cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(control.returncode, 0, control.stdout + control.stderr)
        self.assertTrue(json.loads(self.destination.read_text())['scope']['complete'])
        sentinel = b'selected input must remain unchanged\n'
        self.destination.write_bytes(sentinel)
        payload['changed_paths'] = [str(self.destination)]
        selection.write_text(json.dumps(payload))
        result = subprocess.run(['bash', 'scripts/ci.sh', '--mode', 'local'],
                                cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertIn('collides with selected input', result.stderr)
        self.assertEqual(self.destination.read_bytes(), sentinel)
        self.assertFalse(list(self.root.glob('.*rigorloop-report*')))
        # Inspect dispatch separately: the same public coordinator must stop
        # before entering the scheduler when selection reveals this collision.
        with patch.dict(os.environ, env), \
             patch.object(execution, 'run_scheduled_checks') as dispatch, \
             self.assertRaises(SystemExit) as outcome:
            execution.ci_main(['local','1','10','0','0','','','0','','0','','0',
                               '--mode','local'])
        self.assertEqual(outcome.exception.code, 4)
        dispatch.assert_not_called()
        self.assertEqual(self.destination.read_bytes(), sentinel)

    def test_late_plan_or_scratch_collision_revokes_publication(self):
        os.environ['RIGORLOOP_VALIDATION_RESULT_JSON'] = str(self.destination)
        for collision in (self.destination, self.root):
            with self.subTest(collision=collision):
                self.destination.write_bytes(b'protected bytes')
                with execution.ReportDestination('explicit') as owner:
                    with self.assertRaisesRegex(ValueError, 'collides'):
                        owner.reject_collisions([collision])
                    with self.assertRaisesRegex(ValueError, 'collision|invalid|revok'):
                        owner.publish({'must': 'not replace protected bytes'})
                self.assertEqual(self.destination.read_bytes(), b'protected bytes')
                self.assertFalse(list(self.root.glob('.*rigorloop-report*')))

    def test_handled_interruption_publishes_known_partial_results_and_releases_owner(self):
        entered=self.root/'entered'
        process=self.start_composed(f'from pathlib import Path; import time; Path({str(entered)!r}).touch(); time.sleep(60)',
                                   second_body='raise SystemExit(99)')
        deadline=time.monotonic()+10
        while not entered.exists() and process.poll() is None and time.monotonic()<deadline:
            time.sleep(.02)
        self.assertTrue(entered.exists())
        process.terminate()
        out,err=process.communicate(timeout=20)
        self.assertEqual(process.returncode,143,out+err)
        report=json.loads(self.destination.read_text())
        first,second=report['parallel']['child_durations']
        self.assertTrue(first['started'])
        self.assertEqual(first['status'],'killed')
        self.assertFalse(second['started'])
        self.assertFalse(report['scope']['complete'])
        self.assertEqual(set(p.name for p in self.root.iterdir()),{'entered','result.json'})


    def test_prepared_ci_handoff_limits_report_environment_to_final_child(self):
        import tarfile
        from types import SimpleNamespace
        from lib.release import release_candidate as candidate
        source=self.root/'source'
        (source/'packages/rigorloop').mkdir(parents=True)
        (source/'packages/rigorloop/package.json').write_text(json.dumps({
            'name':'@xiongxianfei/rigorloop','version':'0.5.1'}))
        (source/'docs/releases').mkdir(parents=True)
        (source/'docs/releases/v0.5.1.md').write_text(
            '# Release v0.5.1\n\n## Version Decision\n\n'
            '- Version decision: patch\n- Change summary: Fix candidate integrity checks.\n'
            '- Status: pending-publication\n')
        private=self.root/'prepared-child.json'
        keys=('RIGORLOOP_CI_PREPARED_RESULT_JSON','RIGORLOOP_VALIDATION_RESULT_JSON',
              'RIGORLOOP_BROAD_SMOKE_RESULT_JSON')
        original=dict(zip(keys,(str(private),str(self.destination),str(self.destination))))
        os.environ.update(original)
        os.environ['REPORT_UNRELATED']='preserved'
        observed=[]
        def clean_preparation():
            self.assertTrue(all(key not in os.environ for key in keys))
            self.assertEqual(os.environ['REPORT_UNRELATED'],'preserved')
        def run(command, root):
            clean_preparation()
            observed.append(command)
            return '' if command[:2]==['git','diff'] else 'a'*40
        def prepare(root, head, ref, previous, output, **kwargs):
            clean_preparation()
            output.mkdir()
            with tarfile.open(output/'package.tgz','w:gz'):
                pass
            return {'tarball':'package.tgz','prepared_commit':'b'*40,'candidate_id':'c'*64}
        with patch.object(candidate,'run',side_effect=run), \
             patch.object(candidate,'prepare_candidate',side_effect=prepare), \
             patch.object(candidate,'ci_subject'), \
             patch.object(candidate.subprocess,'run',return_value=SimpleNamespace(returncode=0)) as dispatch:
            self.assertEqual(candidate.check_ci(['--mode','pr','--base','base','--head','head',
                                                 '--durations','0'],source),0)
            args=dispatch.call_args.args[0]
            env=dispatch.call_args.kwargs['env']
            self.assertEqual(args[args.index('--durations')+1],'0')
            self.assertEqual(args[args.index('--head')+1],'b'*40)
            self.assertEqual(env['RIGORLOOP_VALIDATION_RESULT_JSON'],str(private))
            self.assertNotIn('RIGORLOOP_BROAD_SMOKE_RESULT_JSON',env)
            self.assertNotIn('RIGORLOOP_CI_PREPARED_RESULT_JSON',env)
        self.assertTrue(observed)
        self.assertEqual({key:os.environ[key] for key in keys},original)


    def test_prepared_report_adoption_preserves_actual_subject_and_failure(self):
        os.environ['RIGORLOOP_VALIDATION_RESULT_JSON'] = str(self.destination)
        self.write([self.result('prepared-case')], mode='main')
        seed = json.loads(self.destination.read_text())
        seed['repository_state'] = {'head': 'prepared-head'}
        seed['scope'].update(requested_paths=['prepared-path'], base='prepared-base',
                             head='prepared-head', complete=True)
        for outer_code, child_code, expected in ((0, 0, 0), (9, 0, 9), (0, 7, 7)):
            with self.subTest(outer=outer_code, child=child_code):
                payload = json.loads(json.dumps(seed))
                payload['parallel']['exit_code'] = child_code
                observed = []
                def dispatch(command, **kwargs):
                    self.assertIn('check-ci', command)
                    env = kwargs['env']
                    self.assertNotIn('RIGORLOOP_VALIDATION_RESULT_JSON', env)
                    self.assertNotIn('RIGORLOOP_BROAD_SMOKE_RESULT_JSON', env)
                    private = Path(env['RIGORLOOP_CI_PREPARED_RESULT_JSON'])
                    self.assertNotEqual(private, self.destination)
                    private.write_text(json.dumps(payload))
                    observed.append(private)
                    return subprocess.CompletedProcess(command, outer_code)
                with patch.object(execution.subprocess, 'run', side_effect=dispatch), \
                     self.assertRaises(SystemExit) as outcome:
                    execution.ci_main(['main','1','10','0','0','source-base','source-head',
                                       '0','','0','','1','source-path','--mode','main'])
                self.assertEqual(outcome.exception.code, expected)
                report = json.loads(self.destination.read_text())
                self.assertEqual(report['repository_state'], seed['repository_state'])
                self.assertEqual(report['scope']['head'], 'prepared-head')
                self.assertEqual(report['scope']['requested_paths'], ['prepared-path'])
                self.assertEqual(report['preparation'], {
                    'requested_mode':'main', 'requested_paths':['source-path'],
                    'requested_base':'source-base', 'requested_head':'source-head'})
                self.assertEqual(report['parallel']['exit_code'], expected)
                self.assertEqual(report['parallel']['child_durations'],
                                 payload['parallel']['child_durations'])
                self.assertTrue(observed)
                self.assertTrue(all(not path.exists() for path in observed))
                if expected:
                    self.assertFalse(report['scope']['complete'])


    def test_worker_cost_includes_final_capture_validation_after_poll(self):
        original_clock=time.monotonic
        original_decoder=execution.codecs.getincrementaldecoder
        offset=[0]
        def decoder_factory(encoding):
            build=original_decoder(encoding)
            def create(*args, **kwargs):
                decoder=build(*args, **kwargs)
                class TimedDecoder:
                    def decode(self, data, final=False):
                        result=decoder.decode(data, final=final)
                        if final:
                            offset[0]+=100
                        return result
                return TimedDecoder()
            return create
        plan=execution.CheckPlan('capture-finalization','fixture',
            [sys.executable,'-c','print("captured output")'],None,'focused',True)
        with patch.object(execution.time,'monotonic',side_effect=lambda:original_clock()+offset[0]), \
             patch.object(execution.codecs,'getincrementaldecoder',side_effect=decoder_factory):
            row,=execution.run_scheduled_checks([plan],jobs=1,timeout_seconds=10,
                fail_fast=False,scratch=self.root/'worker')
        self.assertEqual(row.exit_code,0,row.exit_reason)
        self.assertEqual(offset[0],200)
        self.assertGreaterEqual(row.elapsed_seconds,200)


    def test_invalid_report_destination_rejects_before_real_worker_launch(self):
        marker=self.root/'forbidden'
        process=self.start_composed(f'from pathlib import Path; Path({str(marker)!r}).touch()',
                                   destination=self.root)
        out,err=process.communicate(timeout=20)
        self.assertNotEqual(process.returncode,0,out+err)
        self.assertFalse(marker.exists())
        self.assertTrue(self.root.is_dir())

    def test_timeout_cost_and_unstarted_dependency_remain_in_report(self):
        process=self.start_composed('import time; time.sleep(60)',second_body='pass',timeout=1)
        out,err=process.communicate(timeout=20)
        self.assertEqual(process.returncode,124,out+err)
        report=json.loads(self.destination.read_text())
        first,second=report['parallel']['child_durations']
        self.assertEqual(first['status'],'timed out')
        self.assertGreaterEqual(first['duration_ms'],1000)
        self.assertTrue(first['started'])
        self.assertFalse(second['started'])
        self.assertFalse(report['scope']['complete'])

    def test_controlled_selection_failures_publish_honest_empty_partial_reports(self):
        selection=self.root/'selection.json'
        env={**os.environ,'RIGORLOOP_SELECTOR_FIXTURE':str(selection),
             'RIGORLOOP_VALIDATION_RESULT_JSON':str(self.destination)}
        for status,code in (('blocked',2),('fallback',3),('error',4)):
            with self.subTest(status=status):
                selection.write_text(json.dumps(dict(mode='explicit',status=status,changed_paths=[],
                    classified_paths=[],unclassified_paths=[],selected_checks=[],affected_roots=[],
                    broad_smoke_required=False,blocking_results=[{'code':'fixture-blocker'}],
                    preflight_results=[],rationale=[])))
                result=subprocess.run(['bash','scripts/ci.sh','--mode','explicit'],cwd=ROOT,env=env,
                                      capture_output=True,text=True)
                self.assertEqual(result.returncode,code,result.stdout+result.stderr)
                report=json.loads(self.destination.read_text())
                self.assertEqual(report['parallel']['exit_code'],code)
                self.assertEqual(report['parallel']['child_durations'],[])
                self.assertFalse(report['scope']['complete'])

    def test_discovery_failure_retains_known_cases_without_inventing_unknown_population(self):
        valid=self.root/'valid.py'
        invalid=self.root/'invalid.py'
        marker=self.root/'forbidden'
        valid.write_text('import unittest\nfrom pathlib import Path\nclass Good(unittest.TestCase):\n'
            f'    def test_ok(self): Path({str(marker)!r}).touch()\n'
            'if __name__ == "__main__": unittest.main()\n')
        invalid.write_text('raise RuntimeError("fixture discovery failure")\n')
        code="""import sys,json
sys.path.insert(0,sys.argv[1])
from lib.validation import validation_execution as e
paths=json.loads(sys.argv[2])
e.compose_mode=lambda *a,**k:[e.CheckPlan(key,'fixture',[sys.executable,path],None,'focused',True)
 for key,path in zip(('skills.regression','change_metadata.regression'),paths)]
try:e.composed_main(['broad-smoke','1','20','0','0','','','1'])
except (ValueError,OSError,TypeError,KeyError) as exc:
 print(str(exc),file=sys.stderr);raise SystemExit(4)
"""
        result=subprocess.run([sys.executable,'-c',code,str(ROOT/'scripts'),json.dumps([str(valid),str(invalid)])],
            cwd=ROOT,env={**os.environ,'RIGORLOOP_VALIDATION_RESULT_JSON':str(self.destination)},
            capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,4,result.stdout+result.stderr)
        self.assertIn('fixture discovery failure',result.stdout+result.stderr)
        self.assertFalse(marker.exists())
        report=json.loads(self.destination.read_text())
        self.assertFalse(report['scope']['complete'])
        cases=[r for r in report['parallel']['child_durations'] if r['case_id'] is not None]
        self.assertEqual([r['case_id'] for r in cases],['Good.test_ok'])
        self.assertTrue(all(not r['started'] for r in cases))


if __name__ == '__main__':
    unittest.main()
