#!/usr/bin/env python3
"""Real process, graph and catalog boundary proof for the internal executor."""
from __future__ import annotations

import dataclasses
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from validation_execution import CheckPlan, run_scheduled_checks, validate_plans, selected_main
from validation_selection import CHECK_CATALOG, ExecutionConstraints, validate_catalog


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
                        {'dependencies': ('a', 'a')}, {'parallel_safe': 'yes'}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate_plans([dataclasses.replace(self.plan('a'), **changes)], jobs=2)

    def test_reverse_completion_keeps_order_and_separate_streams(self):
        results = self.run_plans([self.plan('slow', 'import time; time.sleep(.15); print("one")'),
                                  self.plan('fast', 'import sys; print("two", file=sys.stderr)')])
        self.assertEqual([r.plan.check_id for r in results], ['slow', 'fast'])
        self.assertEqual([r.exit_code for r in results], [0, 0])
        self.assertEqual(results[0].stdout_path.read_text(), 'one\n')
        self.assertEqual(results[1].stderr_path.read_text(), 'two\n')
        self.assertLess(results[1].elapsed_seconds, results[0].elapsed_seconds)

    def test_independent_failure_continues_and_dependency_failure_prevents_launch(self):
        marker = self.root / 'forbidden'
        results = self.run_plans([self.plan('failed', 'raise SystemExit(7)'),
            self.plan('dependent', f'open({str(marker)!r}, "w").close()', dependencies=('failed',)),
            self.plan('independent', 'print("ran")')])
        self.assertEqual([r.exit_code for r in results], [7, 125, 0])
        self.assertIn('failed', results[1].exit_reason)
        self.assertFalse(marker.exists())

    def test_parallel_tasks_actually_overlap_with_bounded_workers(self):
        gate = self.root / 'gate'
        gate.mkdir()
        body = ('import pathlib,time; p=pathlib.Path(%r); (p/%r).touch(); '
                'deadline=time.monotonic()+2\nwhile %r and len(list(p.iterdir()))<2:\n'
                ' if time.monotonic()>deadline: raise SystemExit(8)\n time.sleep(.01)')
        results = self.run_plans([self.plan('a', body % (str(gate), 'a', int(os.environ.get('RIGORLOOP_VALIDATION_WORKERS','2'))>1)),
                                  self.plan('b', body % (str(gate), 'b', int(os.environ.get('RIGORLOOP_VALIDATION_WORKERS','2'))>1))])
        self.assertEqual([r.exit_code for r in results], [0, 0])

    def test_serial_barrier_and_queue_time_excluded(self):
        gate = self.root / 'gate'
        body = f'import pathlib,time; p=pathlib.Path({str(gate)!r}); assert not p.exists(); p.touch(); time.sleep(.12); p.unlink()'
        plans = [self.plan('a', body), dataclasses.replace(self.plan('serial', body), parallel_safe=False), self.plan('b', body)]
        results = self.run_plans(plans)
        self.assertEqual([r.exit_code for r in results], [0, 0, 0])
        self.assertLess(results[2].elapsed_seconds, .3)

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
        with patch('validation_execution.os.name', 'nt'), self.assertRaisesRegex(ValueError, 'POSIX'):
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
                  "from validation_execution import CheckPlan,run_scheduled_checks; "
                  f"p=CheckPlan('owned','fixture',[sys.executable,'-c',{body!r}],None,'focused',True); "
                  f"r=run_scheduled_checks([p],jobs=1,timeout_seconds=10,fail_fast=False,scratch=Path({str(self.root / 'scratch')!r})); "
                  f"Path({str(result_file)!r}).write_text(json.dumps([x.exit_code for x in r]))")
        process = subprocess.Popen([sys.executable, '-c', driver])
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


class CatalogTests(unittest.TestCase):
    def test_catalog_is_valid_and_unassessed_commands_are_serial(self):
        validate_catalog()
        self.assertIsNone(CHECK_CATALOG['selector.regression'].constraints)

    def test_unknown_value_units_modes_fields_and_stale_basis_reject(self):
        entry = CHECK_CATALOG['skills.regression']
        for changes in ({'unit':'unknown_value'}, {'mode':'unknown_value'},
                        {'demand':0}, {'shared_writes':True}, {'basis':'stale'},
                        {'isolation':''}):
            candidate = dataclasses.replace(entry, constraints=dataclasses.replace(entry.constraints, **changes))
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate_catalog({entry.id:candidate})
        with self.assertRaises(TypeError):
            ExecutionConstraints(unknown_value=True)
        with self.assertRaisesRegex(ValueError,'mode membership'):
            validate_catalog({entry.id:dataclasses.replace(entry,modes=('unknown_value',))})
        candidate = dataclasses.replace(entry, command_template=entry.command_template+' --changed')
        with self.assertRaisesRegex(ValueError, 'basis'):
            validate_catalog({entry.id:candidate})


class CompositionTests(unittest.TestCase):
    def test_catalog_composes_broad_and_main_with_distinct_preserved_package_versions(self):
        from validation_execution import compose_mode
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for mode,version in [('broad-smoke','v0.1.3'),('main','v0.1.5')]:
                plans = compose_mode(mode,root,base='before',head='after')
                build = next(p for p in plans if p.check_id.endswith('adapters.build_archives'))
                check = next(p for p in plans if p.check_id.endswith('adapters.validate_archives'))
                self.assertIn(version,build.args)
                self.assertIn(version,check.args)
                output = build.args[build.args.index('--output-dir')+1]
                self.assertIn(output,check.args)
                self.assertIn(build.check_id,check.dependencies)
                self.assertFalse(any(p.args[:2] == ['bash','scripts/ci.sh'] for p in plans))
            self.assertIn('main.rigorloop_cli.test',{p.check_id for p in plans})
            self.assertIn('main.workflow_automation.engine_regression',{p.check_id for p in plans})

    def test_unknown_value_composed_mode_rejects(self):
        from validation_execution import compose_mode
        with tempfile.TemporaryDirectory() as temporary, self.assertRaises(ValueError):
            compose_mode('unknown_value',Path(temporary))

    def test_retired_classification_override_rejects_before_work(self):
        env = dict(os.environ,RIGORLOOP_BROAD_SMOKE_CLASSIFICATION='/no/retired/classification')
        result = subprocess.run(['bash','scripts/ci.sh','--mode','broad-smoke','--jobs','2'],env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,4)
        self.assertIn('retired',result.stderr)
        self.assertNotIn('==>',result.stdout)


if __name__ == '__main__':
    unittest.main()
