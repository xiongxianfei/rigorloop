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


class CaseAdapterTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def fixture(self, body):
        path = self.root/'suite.py'
        path.write_text('import unittest\n'+body+'\nif __name__ == "__main__": unittest.main()\n')
        return path

    def test_real_discovery_duplicate_zero_and_loader_error_reject_before_cases(self):
        from validation_execution import discover_cases
        for body in ['class Empty(unittest.TestCase): pass',
                     'raise RuntimeError("collection failed")',
                     'class Example(unittest.TestCase):\n def test_one(self): pass\n'
                     'def load_tests(loader,tests,pattern):\n return unittest.TestSuite([Example("test_one"),Example("test_one")])']:
            with self.subTest(body=body), self.assertRaises(ValueError):
                discover_cases([sys.executable,str(self.fixture(body))], self.root/'collect', jobs=1, timeout=5)

    def test_actual_worker_rejects_skipped_missing_and_disagreeing_receipts(self):
        from validation_execution import discover_cases, case_plans
        path = self.fixture('class Example(unittest.TestCase):\n @unittest.skip("required proof unavailable")\n def test_one(self): pass')
        args = [sys.executable,str(path)]
        ids = discover_cases(args,self.root/'collect',jobs=1,timeout=5)
        self.assertEqual(ids,['Example.test_one'])
        parent = CheckPlan('suite',' '.join(args),args,None,'focused',True)
        plans = case_plans(parent,ids,self.root/'cases')
        results = run_scheduled_checks(plans,jobs=1,timeout_seconds=5,fail_fast=False,scratch=self.root/'run')
        self.assertNotEqual(results[0].exit_code,0)
        self.assertIn('required case receipt',results[0].stderr_path.read_text())
        path.write_text('raise SystemExit(0)')
        results = run_scheduled_checks(plans,jobs=1,timeout_seconds=5,fail_fast=False,scratch=self.root/'missing')
        self.assertNotEqual(results[0].exit_code,0)
        path.write_text('import unittest\nclass Other(unittest.TestCase):\n def test_two(self): pass\nunittest.main()')
        results = run_scheduled_checks(plans,jobs=1,timeout_seconds=5,fail_fast=False,scratch=self.root/'disagree')
        self.assertNotEqual(results[0].exit_code,0)
    def test_missing_or_unknown_value_receipt_cannot_reuse_a_previous_pass(self):
        from validation_execution import case_plans
        path = self.fixture('class Example(unittest.TestCase):\n def test_one(self): pass')
        args = [sys.executable,str(path)]
        parent = CheckPlan('suite',' '.join(args),args,None,'focused',True)
        plan = case_plans(parent,['Example.test_one'],self.root/'cases')[0]
        first = run_scheduled_checks([plan],jobs=1,timeout_seconds=5,fail_fast=False,scratch=self.root/'first')[0]
        self.assertEqual(first.exit_code,0,first.stderr_path.read_text())
        valid = json.loads(plan.case_receipt.read_text())
        counterfeit = dataclasses.replace(plan,args=[sys.executable,'-c','pass'])
        result = run_scheduled_checks([counterfeit],jobs=1,timeout_seconds=5,fail_fast=False,scratch=self.root/'missing')[0]
        self.assertEqual(result.exit_code,4)
        self.assertIn('required case receipt',result.exit_reason)
        for field,value in [('mode','unknown_value'),('completed',[]),('tests_run',True),('extra','unknown_value')]:
            payload = {**valid,field:value}
            args = [sys.executable,'-c',f'from pathlib import Path; Path({str(plan.case_receipt)!r}).write_text({json.dumps(payload)!r})']
            counterfeit = dataclasses.replace(plan,args=args)
            result = run_scheduled_checks([counterfeit],jobs=1,timeout_seconds=5,fail_fast=False,scratch=self.root/field)[0]
            self.assertEqual(result.exit_code,4,result.exit_reason)

    def test_unknown_adapter_mode_rejects_before_script_execution(self):
        from validation_execution import _case_command
        marker = self.root/'forbidden'
        path = self.fixture(f'open({str(marker)!r},"w").close()')
        command = _case_command('unknown_value',self.root/'receipt',[sys.executable,str(path)])
        result = subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(result.returncode,4,result.stdout+result.stderr)
        self.assertFalse(marker.exists())

    def test_expansion_keeps_all_case_dependencies_and_failed_case_blocks_consumer(self):
        from validation_execution import expand_cases
        from validation_selection import CheckCatalogEntry, command_basis
        path = self.fixture('class Example(unittest.TestCase):\n def test_a(self): pass\n def test_b(self): self.fail("required failure")')
        args = [sys.executable,str(path)]
        command = __import__('shlex').join(args)
        entry = CheckCatalogEntry('suite',command,'fixture',parallel_safe=True,
            constraints=ExecutionConstraints(unit='python-unittest',mode='bounded',
                isolation='Owned proof fixture',basis=command_basis(command,'python-unittest')))
        parent = CheckPlan('suite',command,args,None,'focused',True)
        marker = self.root/'forbidden'
        child_args = [sys.executable,'-c',f'open({str(marker)!r},"w").close()']
        child = CheckPlan('consumer','consumer',child_args,None,'boundary',True,('suite',))
        with patch.dict(CHECK_CATALOG, {'suite':entry}):
            plans = expand_cases([parent,child],self.root/'expand',jobs=2,timeout=5)
        self.assertEqual(plans[-1].dependencies,('suite::Example.test_a','suite::Example.test_b'))
        results = run_scheduled_checks(plans,jobs=2,timeout_seconds=5,fail_fast=False,scratch=self.root/'execute')
        self.assertEqual([r.exit_code for r in results],[0,1,125])
        self.assertFalse(marker.exists())

    def test_normal_custom_patterns_and_dynamic_fixture_discovery_are_preserved(self):
        from validation_execution import discover_cases
        path = Path(__file__).resolve().parent/'test-change-metadata-validator.py'
        args = [sys.executable,str(path)]
        ids = discover_cases([*args,'-k','test_recording_v3_full_set'],self.root/'pattern',jobs=1,timeout=10)
        self.assertEqual(ids,['ExplicitRecordingMetadataTests.test_recording_v3_full_set_and_unknown_value_version_fail_closed'])
        with patch.dict(os.environ, {'RIGORLOOP_CHANGE_METADATA_FAILURE_FIXTURE':'1'}):
            ids = discover_cases(args,self.root/'dynamic',jobs=1,timeout=10)
        self.assertIn('ChangeMetadataValidatorFixtureTests.test_output_contract_fixture_failure',ids)
        self.assertEqual(len(ids),8)

    def test_real_wrapper_expands_selected_metadata_into_actual_cases(self):
        payload = dict(mode='explicit',status='ok',changed_paths=[],classified_paths=[],
            unclassified_paths=[],affected_roots=[],broad_smoke_required=False,
            blocking_results=[],preflight_results=[],rationale=[],selected_checks=[
                dict(id='change_metadata.regression',command='python scripts/test-change-metadata-validator.py')])
        fixture = self.root/'selection.json'
        fixture.write_text(json.dumps(payload))
        env = dict(os.environ,RIGORLOOP_SELECTOR_FIXTURE=str(fixture))
        result = subprocess.run(['bash','scripts/ci.sh','--mode','explicit','--path',
            'scripts/test-change-metadata-validator.py','--jobs','2'],env=env,capture_output=True,text=True,
            cwd=Path(__file__).resolve().parents[1])
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        lines = [line for line in result.stdout.splitlines()
                 if line.startswith('change_metadata.regression::') and ' | passed | ok | ' in line]
        self.assertEqual(len(lines),7,result.stdout)
        self.assertIn('change_metadata.regression::ExplicitRecordingMetadataTests.test_explicit_recording_unknown_value_and_mixed_contract_fail_closed',result.stdout)

    def test_case_expansion_preserves_declared_serial_resource_constraint(self):
        from validation_execution import case_plans
        marker = self.root/'exclusive'
        body = (f'class Example(unittest.TestCase):\n'
                f' def setUp(self):\n  from pathlib import Path\n  self.marker=Path({str(marker)!r})\n'
                ' def test_a(self):\n  import time\n  self.marker.mkdir()\n  time.sleep(.1)\n  self.marker.rmdir()\n'
                ' def test_b(self): self.test_a()')
        path = self.fixture(body)
        args = [sys.executable,str(path)]
        parent = CheckPlan('suite',' '.join(args),args,None,'focused',False,demand=2)
        plans = case_plans(parent,['Example.test_a','Example.test_b'],self.root/'cases')
        self.assertTrue(all(not p.parallel_safe and p.demand==2 for p in plans))
        results = run_scheduled_checks(plans,jobs=2,timeout_seconds=5,fail_fast=False,scratch=self.root/'run')
        self.assertEqual([r.exit_code for r in results],[0,0])

    def exercise_real_suite(self, name):
        from validation_execution import discover_cases, case_plans, _case_command
        args = [sys.executable, str(Path(__file__).resolve().parent/name)]
        ids = discover_cases(args,self.root/'discovery',jobs=2,timeout=300)
        baseline = self.root/'baseline.json'
        command = _case_command('observe',baseline,args)
        parent = CheckPlan('suite',' '.join(args),args,None,'focused',True)
        direct = CheckPlan('direct',' '.join(args),command,None,'focused',False)
        result = run_scheduled_checks([direct],jobs=2,timeout_seconds=300,fail_fast=False,scratch=self.root/'direct')[0]
        self.assertEqual(result.exit_code,0,result.stdout_path.read_text()+result.stderr_path.read_text())
        receipt = json.loads(baseline.read_text())
        self.assertTrue(receipt['successful'])
        self.assertEqual(receipt['discovered'],ids)
        self.assertEqual(receipt['started'],ids)
        self.assertEqual(receipt['completed'],ids)
        self.assertEqual(receipt['tests_run'],len(ids))
        for jobs in (1,2):
            scope = self.root/f'jobs-{jobs}'
            plans = case_plans(parent,list(reversed(ids)) if jobs==2 else ids,scope/'cases')
            results = run_scheduled_checks(plans,jobs=jobs,timeout_seconds=300,fail_fast=False,scratch=scope/'run')
            for result in results:
                self.assertEqual(result.exit_code,0,result.plan.command+'\n'+result.stdout_path.read_text()+result.stderr_path.read_text())
            self.assertEqual(sorted(r.plan.case_id for r in results),sorted(ids))
            receipts = [json.loads(r.plan.case_receipt.read_text()) for r in results]
            started = sorted(x['started'][0] for x in receipts)
            completed = sorted(x['completed'][0] for x in receipts)
            self.assertEqual(started,sorted(ids))
            self.assertEqual(completed,sorted(ids))
            intervals = sorted((x['started_at'],x['completed_at']) for x in receipts)
            overlap = any(start < earlier_end for (_,earlier_end),(start,_) in zip(intervals,intervals[1:]))
            available = min(jobs,int(os.environ.get('RIGORLOOP_VALIDATION_WORKERS',str(jobs))))
            self.assertEqual(overlap,available>1, f'{name}: expected actual case overlap only with multiple workers')
            print(f'CASE POPULATION {name}: jobs={available} discovered={len(ids)} started={len(started)} completed={len(completed)} overlap={overlap}',flush=True)
        print('CASE IDS '+json.dumps({'suite':name,'ids':ids}),flush=True)

    def test_real_selector_cases_match_direct_sequential_and_reverse_parallel(self):
        self.exercise_real_suite('test-select-validation.py')

    def test_real_lifecycle_cases_match_direct_sequential_and_reverse_parallel(self):
        self.exercise_real_suite('test-artifact-lifecycle-validator.py')

    def test_real_metadata_cases_match_direct_sequential_and_reverse_parallel(self):
        self.exercise_real_suite('test-change-metadata-validator.py')


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
                        {'dependencies': ('a', 'a')}, {'parallel_safe': 'yes'}, {'case_id':'unpaired'}):
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
        self.assertIsNone(CHECK_CATALOG['review_artifacts.regression'].constraints)
        self.assertEqual(CHECK_CATALOG['selector.regression'].constraints.unit,'python-unittest')

    def test_case_unit_rejects_contradictory_command_before_launch(self):
        from validation_selection import command_basis
        entry = CHECK_CATALOG['selector.regression']
        for command in ['bash scripts/test-select-validation.py','python -c pass']:
            candidate = dataclasses.replace(entry,command_template=command,
                constraints=dataclasses.replace(entry.constraints,basis=command_basis(command,'python-unittest')))
            with self.assertRaisesRegex(ValueError,'case command'):
                validate_catalog({entry.id:candidate})

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


class ImmediateFailureResult(unittest.TextTestResult):
    # The outer CI timeout may terminate this integration suite before unittest
    # prints its final summary. Preserve the original traceback as it happens.
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(self.failures[-1][1])
        self.stream.flush()

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(self.errors[-1][1])
        self.stream.flush()


class ImmediateFailureRunner(unittest.TextTestRunner):
    resultclass = ImmediateFailureResult


if __name__ == '__main__':
    unittest.main(testRunner=ImmediateFailureRunner)
