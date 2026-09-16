"""Real process scheduling, worker budgets, failures and owned-child cleanup."""

from __future__ import annotations

import sys
from pathlib import Path
import dataclasses
import json
import os
import signal
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.validation_execution import CheckPlan, run_scheduled_checks, validate_plans, selected_main
from lib.validation.validation_selection import CHECK_CATALOG


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def plan(self, name, body='pass', **kwargs):
        args = [sys.executable, '-c', body]
        return CheckPlan(name, ' '.join(args), args, None, 'focused', True, **kwargs)

    def run_plans(self, plans, **kwargs):
        return run_scheduled_checks(plans, jobs=kwargs.pop('jobs', 2),
                                    timeout_seconds=kwargs.pop('timeout_seconds', 5),
                                    fail_fast=kwargs.pop('fail_fast', False), scratch=self.root, **kwargs)

    def test_parent_report_destination_is_private_and_nested_reports_are_owned(self):
        from lib.validation.validation_execution import _write_mode_result
        parent = self.root/'parent.json'
        nested = self.root/'nested.json'
        parent.write_text('parent sentinel')
        body = ('import os,sys; from pathlib import Path; '
                f'sys.path.insert(0,{str(ROOT / "scripts")!r}); '
                'inherited=os.environ.get("RIGORLOOP_BROAD_SMOKE_RESULT_JSON"); '
                'Path(inherited).write_text("overwritten") if inherited else None; '
                'assert os.environ["RIGORLOOP_VALIDATION_WORKERS"] == "1"; '
                'assert os.environ["OWNED_REPORT_FIXTURE"] == "preserved"; '
                f'os.environ["RIGORLOOP_BROAD_SMOKE_RESULT_JSON"]={str(nested)!r}; '
                'from lib.validation.validation_execution import _write_mode_result; '
                '_write_mode_result([],mode="broad-smoke",jobs=1,elapsed=.1,code=0,skip_diff_scoped=True)')
        with patch.dict(os.environ, {'RIGORLOOP_BROAD_SMOKE_RESULT_JSON':str(parent),
                                     'OWNED_REPORT_FIXTURE':'preserved'}):
            results=self.run_plans([self.plan('child',body)])
            self.assertEqual([r.exit_code for r in results],[0])
            self.assertEqual(parent.read_text(),'parent sentinel')
            self.assertEqual(json.loads(nested.read_text())['parallel']['jobs'],1)
            _write_mode_result(results,mode='broad-smoke',jobs=2,elapsed=.2,code=0,skip_diff_scoped=True)
            self.assertEqual(os.environ['RIGORLOOP_BROAD_SMOKE_RESULT_JSON'],str(parent))
        report=json.loads(parent.read_text())
        self.assertEqual(report['parallel']['jobs'],2)
        self.assertEqual([r['check_id'] for r in report['parallel']['child_durations']],['child'])

    def test_nested_budget_caps_actual_children_and_unknown_value_rejects_before_launch(self):
        gate = self.root/'active'
        body = (f'import os,pathlib,time; p=pathlib.Path({str(gate)!r}); '
                'assert os.environ["RIGORLOOP_VALIDATION_WORKERS"] == "1"; '
                'p.mkdir(); time.sleep(.1); p.rmdir()')
        with patch.dict(os.environ, {'RIGORLOOP_VALIDATION_WORKERS':'1'}):
            results = self.run_plans([self.plan('a',body),self.plan('b',body)],jobs=8)
        self.assertEqual([r.exit_code for r in results],[0,0])
        for value in ['0','-1','unknown_value','']:
            with patch.dict(os.environ, {'RIGORLOOP_VALIDATION_WORKERS':value}), self.assertRaises(ValueError):
                self.run_plans([self.plan('forbidden',f'open({str(gate)!r},"w").close()')])
            self.assertFalse(gate.exists())

    def test_complete_graph_rejects_before_any_launch(self):
        marker = self.root / 'launched'
        first = self.plan('first', f'open({str(marker)!r}, "w").close()')
        for bad in ([first, self.plan('bad', dependencies=('missing',))],
                    [first, self.plan('first')],
                    [first, self.plan('a', dependencies=('b',)), self.plan('b', dependencies=('a',))]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.run_plans(bad)
            self.assertFalse(marker.exists())

    def test_selector_cannot_relabel_boundary_phase(self):
        payload = dict(mode='explicit', status='ok', changed_paths=[], classified_paths=[],
            unclassified_paths=[], affected_roots=[], broad_smoke_required=False,
            blocking_results=[], preflight_results=[], rationale=[], selected_checks=[
                dict(id='broad_smoke.repo',command=CHECK_CATALOG['broad_smoke.repo'].command_template,
                     phase='focused')])
        path = self.root/'selection.json'
        path.write_text(json.dumps(payload))
        with self.assertRaises(SystemExit) as raised:
            selected_main([str(path),'0','10','0','2','0','explicit','',''])
        self.assertEqual(raised.exception.code,4)

    def test_unknown_value_phase_and_resource_constraints_reject(self):
        for changes in ({'phase': 'unknown_value'}, {'demand': 0}, {'demand': True},
                        {'dependencies': ('a', 'a')}, {'parallel_safe': 'yes'}, {'case_id':'unpaired'}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate_plans([dataclasses.replace(self.plan('a'), **changes)], jobs=2)

    def test_independent_failure_continues_and_dependency_failure_prevents_launch(self):
        marker = self.root / 'forbidden'
        results = self.run_plans([self.plan('failed', 'raise SystemExit(7)'),
            self.plan('dependent', f'open({str(marker)!r}, "w").close()', dependencies=('failed',)),
            self.plan('independent', 'print("ran")')])
        self.assertEqual([r.exit_code for r in results], [7, 125, 0])
        self.assertIn('failed', results[1].exit_reason)
        self.assertFalse(marker.exists())

    def test_parallel_tasks_actually_overlap_with_bounded_workers(self):
        from lib.validation.validation_execution import CheckResult
        gate = self.root / 'gate'
        gate.mkdir()
        parallel = int(os.environ.get('RIGORLOOP_VALIDATION_WORKERS', '2')) > 1
        observed = []
        body = """import pathlib, sys, time
p = pathlib.Path({gate!r})
name = {name!r}
(p / name).touch()
deadline = time.monotonic() + 10
while {parallel!r} and (not (p / 'a').exists() or not (p / 'b').exists()
                       or (name == 'a' and not (p / 'b-observed').exists())):
    if time.monotonic() > deadline:
        raise SystemExit(8)
    time.sleep(.01)
print(name + '-stdout')
print(name + '-stderr', file=sys.stderr)
"""

        def observe_result(*args, **kwargs):
            result = CheckResult(*args, **kwargs)
            observed.append(result.plan.check_id)
            if result.plan.check_id == 'b':
                (gate / 'b-observed').touch()
            return result

        # Both children rendezvous; a can finish only after the real scheduler
        # records b. The deadline bounds a broken handshake, not relative speed.
        with patch('lib.validation.validation_execution.CheckResult', side_effect=observe_result):
            results = self.run_plans([
                self.plan(name, body.format(gate=str(gate), name=name, parallel=parallel))
                for name in ('a', 'b')
            ], timeout_seconds=15)
        self.assertEqual(observed, ['b', 'a'] if parallel else ['a', 'b'])
        self.assertEqual([r.plan.check_id for r in results], ['a', 'b'])
        self.assertEqual([r.exit_code for r in results], [0, 0])
        for result in results:
            name = result.plan.check_id
            self.assertEqual(result.stdout_path.read_text(), name + '-stdout\n')
            self.assertEqual(result.stderr_path.read_text(), name + '-stderr\n')

    def test_serial_barrier_and_queue_time_excluded(self):
        gate = self.root / 'gate'
        body = f'import pathlib,time; p=pathlib.Path({str(gate)!r}); assert not p.exists(); p.touch(); time.sleep(.12); p.unlink()'
        plans = [self.plan('a', body), dataclasses.replace(self.plan('serial', body), parallel_safe=False), self.plan('b', body)]
        from lib.validation.validation_execution import CheckResult
        clock_reads, launches, completions = [], [], []
        popen = subprocess.Popen

        def observe_clock():
            clock_reads.append(time.monotonic())
            return clock_reads[-1]

        def observe_launch(*args, **kwargs):
            launches.append(clock_reads[-1])
            return popen(*args, **kwargs)

        def observe_result(*args, **kwargs):
            completions.append(clock_reads[-1])
            return CheckResult(*args, **kwargs)

        # Observe the scheduler clock and real launch boundaries. Process startup
        # and cleanup may take any duration; queue time must still be excluded.
        with patch('lib.validation.validation_execution.time') as clock, patch(
                'lib.validation.validation_execution.subprocess.Popen', side_effect=observe_launch), patch(
                'lib.validation.validation_execution.CheckResult', side_effect=observe_result):
            clock.monotonic.side_effect = observe_clock
            clock.sleep.side_effect = time.sleep
            results = self.run_plans(plans)
        self.assertEqual([r.exit_code for r in results], [0, 0, 0])
        self.assertEqual(len(launches), 3)
        self.assertGreater(launches[2], clock_reads[0])
        self.assertEqual(len(completions), 3)
        self.assertEqual(results[2].elapsed_seconds, completions[2] - launches[2])

    def test_fail_fast_awaits_started_failure_and_marks_every_queued_task(self):
        results = self.run_plans([self.plan('a', 'raise SystemExit(7)'),
            self.plan('b', 'import time; time.sleep(.1); raise SystemExit(9)'),
            self.plan('queued')], fail_fast=True)
        self.assertEqual([r.exit_code for r in results], [7, 9 if int(os.environ.get("RIGORLOOP_VALIDATION_WORKERS","2"))>1 else 125, 125])
        self.assertIn('fail-fast', results[2].exit_reason)

    def test_timeout_terminates_descendant_that_ignores_term_and_retry_is_fresh(self):
        marker = self.root / 'late-write'
        pid_file = self.root / 'child-pid'
        child = f'import os,signal,time,pathlib; pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid())); signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(7); pathlib.Path({str(marker)!r}).touch()'
        body = f'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",{child!r}]); time.sleep(20)'
        result = self.run_plans([self.plan('timeout', body)], timeout_seconds=1)[0]
        self.assertEqual(result.exit_code, 124)
        self.assertFalse(marker.exists())
        with self.assertRaises(ProcessLookupError):
            os.kill(int(pid_file.read_text()), 0)
        self.assertLess(result.elapsed_seconds, 7)
        self.assertEqual(self.run_plans([self.plan('timeout')])[0].exit_code, 0)

    def test_failed_parent_stops_queue_during_descendant_cleanup(self):
        marker = self.root/'queued'
        child = 'import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(20)'
        body = f'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",{child!r}]); time.sleep(.2); raise SystemExit(7)'
        results = self.run_plans([self.plan('failed',body),
            self.plan('peer','import time; time.sleep(.5)'),
            self.plan('queued',f'open({str(marker)!r},"w").close()')],timeout_seconds=10,fail_fast=True)
        self.assertEqual([r.exit_code for r in results],[7,0 if int(os.environ.get("RIGORLOOP_VALIDATION_WORKERS","2"))>1 else 125,125])
        self.assertFalse(marker.exists())

    def test_timeout_reaps_descendant_in_new_session(self):
        pid_file = self.root/'escaped-pid'
        child = f'import os,pathlib,time; pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid())); time.sleep(20)'
        body = f'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",{child!r}],start_new_session=True); time.sleep(20)'
        result = self.run_plans([self.plan('escaped',body)],timeout_seconds=1)[0]
        self.assertEqual(result.exit_code,124)
        with self.assertRaises(ProcessLookupError):
            os.kill(int(pid_file.read_text()),0)

    def test_observed_outcome_survives_cleanup_past_execution_timeout(self):
        child = 'import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(20)'
        for expected in (0,7):
            with self.subTest(expected=expected):
                body = f'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",{child!r}]); time.sleep(.2); raise SystemExit({expected})'
                result = self.run_plans([self.plan('cleanup',body)],timeout_seconds=1)[0]
                self.assertEqual(result.exit_code,expected)
                self.assertGreater(result.elapsed_seconds,1)

    def test_fast_orphan_with_replaced_environment_is_reaped_without_touching_unrelated_child(self):
        pid_file = self.root/'orphan-pid'
        child = f'import os,pathlib,time; pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid())); time.sleep(20)'
        body = f'import subprocess,sys,pathlib; p=subprocess.Popen([sys.executable,"-c",{child!r}],start_new_session=True,env={{}}); pathlib.Path({str(pid_file)!r}).write_text(str(p.pid))'
        unrelated = subprocess.Popen([sys.executable,'-c','import time; time.sleep(20)'])
        try:
            result = self.run_plans([self.plan('orphan',body)],timeout_seconds=2)[0]
            self.assertEqual(result.exit_code,0)
            deadline = time.monotonic()+1
            while not pid_file.exists() and time.monotonic()<deadline:
                time.sleep(.01)
            self.assertIsNone(unrelated.poll())
            with self.assertRaises(ProcessLookupError):
                os.kill(int(pid_file.read_text()),0)
        finally:
            unrelated.terminate()
            unrelated.wait()
            if pid_file.exists():
                try:
                    os.kill(int(pid_file.read_text()), signal.SIGKILL)
                    os.waitpid(int(pid_file.read_text()),0)
                except (ProcessLookupError,ChildProcessError):
                    pass

    def test_malformed_empty_selection_and_unknown_value_labels_reject(self):
        payload = dict(mode='explicit',status='ok',changed_paths=[],classified_paths=[],unclassified_paths=[],
            affected_roots=[],broad_smoke_required=False,blocking_results=[],preflight_results=[],rationale=[])
        cases = [{},None,'']
        cases.append([dict(id='skills.regression',command=CHECK_CATALOG['skills.regression'].command_template,cache_status='unknown_value')])
        for selected in cases:
            path = self.root/'selection.json'
            path.write_text(json.dumps(dict(payload,selected_checks=selected)))
            with self.subTest(selected=selected), self.assertRaises(SystemExit) as raised:
                selected_main([str(path),'0','10','0','2','0','explicit','',''])
            self.assertEqual(raised.exception.code,4)

    def test_signal_and_unavailable_command_are_distinct(self):
        missing = dataclasses.replace(self.plan('missing'), args=['/no-such-rigorloop-executable'])
        results = self.run_plans([self.plan('signal', 'import os,signal; os.kill(os.getpid(), signal.SIGTERM)'), missing])
        self.assertEqual([r.exit_code for r in results], [128 + signal.SIGTERM, 127])
        self.assertEqual([r.status for r in results], ['killed', 'unavailable'])

    def test_unsupported_platform_rejects_before_launch(self):
        with patch('lib.validation.validation_execution.os.name', 'nt'), self.assertRaisesRegex(ValueError, 'POSIX'):
            self.run_plans([self.plan('a')])

    def test_budget_and_timeout_overrides_reject_invalid_values(self):
        for value in (0, -1, True, '2'):
            for key in ('jobs', 'timeout_seconds'):
                with self.subTest(value=value,key=key), self.assertRaises(ValueError):
                    self.run_plans([self.plan('a')], **{key:value})


    def test_interrupt_reaps_started_processes_and_retains_unfinished_results(self):
        pid_file = self.root / 'owned-pid'
        result_file = self.root / 'results'
        body = f'import os,time,pathlib; pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid())); time.sleep(20)'
        driver = ("import sys,json; from pathlib import Path; sys.path.insert(0,'scripts'); "
                  "from lib.validation.validation_execution import CheckPlan,run_scheduled_checks; "
                  f"p=CheckPlan('owned','fixture',[sys.executable,'-c',{body!r}],None,'focused',True); "
                  f"r=run_scheduled_checks([p],jobs=1,timeout_seconds=10,fail_fast=False,scratch=Path({str(self.root / 'scratch')!r})); "
                  f"Path({str(result_file)!r}).write_text(json.dumps([x.exit_code for x in r]))")
        process = subprocess.Popen([sys.executable, '-c', driver], cwd=ROOT)
        try:
            deadline = time.monotonic()+3
            while not pid_file.exists() and time.monotonic()<deadline:
                time.sleep(.01)
            self.assertTrue(pid_file.exists())
            process.send_signal(signal.SIGTERM)
            process.wait(timeout=7)
            self.assertEqual(result_file.read_text(), '[143]')
            with self.assertRaises(ProcessLookupError):
                os.kill(int(pid_file.read_text()),0)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

    def test_invalid_success_output_cannot_hide_decoding_failure(self):
        result = self.run_plans([self.plan('bytes', 'import os; os.write(1, bytes([255]))')])[0]
        self.assertEqual(result.exit_code, 4)
        self.assertIn('stdout decode error', result.exit_reason)

    def test_missing_capture_is_runner_failure(self):
        body = "import os; os.unlink(os.readlink('/proc/self/fd/1'))"
        result = self.run_plans([self.plan('lost',body)])[0]
        self.assertEqual(result.exit_code,4)
        self.assertIn('missing stdout', result.exit_reason)
