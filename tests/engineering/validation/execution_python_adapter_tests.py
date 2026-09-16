"""Normal Python discovery, filters, hooks and isolated case receipts."""

from __future__ import annotations

import sys
from pathlib import Path
import dataclasses
import json
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.validation_execution import CheckPlan, run_scheduled_checks
from lib.validation.validation_selection import CHECK_CATALOG, ExecutionConstraints


class CaseAdapterTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def fixture(self, body):
        path = self.root/'suite.py'
        path.write_text('import unittest\n'+body+'\nif __name__ == "__main__": unittest.main()\n')
        return path

    def test_imported_cases_keep_normal_script_imports_selection_and_hooks(self):
        from lib.validation.validation_execution import discover_cases, case_plans
        helper = self.root/'fixture_cases.py'
        helper.write_text('import unittest\nclass ImportedCases(unittest.TestCase):\n'
            ' def setUp(self): self.value = "ready"\n'
            ' def test_ready(self): self.assertEqual(self.value,"ready")\n')
        path = self.fixture('from fixture_cases import ImportedCases')
        args = [sys.executable,str(path)]
        direct = subprocess.run(args,capture_output=True,text=True)
        self.assertEqual(direct.returncode,0,direct.stdout+direct.stderr)
        ids = discover_cases(args,self.root/'collection',jobs=1,timeout=10)
        self.assertEqual(ids,['ImportedCases.test_ready'])
        parent=CheckPlan('imported','fixture',args,None,'focused',True)
        plans=case_plans(parent,ids,self.root/'cases')
        result=run_scheduled_checks(plans,jobs=2,timeout_seconds=10,fail_fast=False,scratch=self.root/'run')[0]
        self.assertEqual(result.exit_code,0,result.stderr_path.read_text())
        # A class exported only under a different name is not addressable by
        # the selected normal TestCase.method identity; never silently omit it.
        path=self.fixture('from fixture_cases import ImportedCases as Alias')
        with self.assertRaisesRegex(ValueError,'addressable'):
            discover_cases(args,self.root/'alias',jobs=1,timeout=10)

    def test_selected_methods_classes_and_filter_values_expand_to_one_case(self):
        from lib.validation.validation_execution import discover_cases, case_plans
        path=self.fixture('class Example(unittest.TestCase):\n def test_a(self): pass\n def test_b(self): pass')
        scopes = (
            (["Example.test_a", "Example.test_b"], ["Example.test_a", "Example.test_b"]),
            (["-k", "Example.test_a", "Example"], ["Example.test_a"]),
            (["--verbose", "Example"], ["Example.test_a", "Example.test_b"]),
        )
        for index, (scope, expected) in enumerate(scopes):
            with self.subTest(scope=scope):
                root=self.root/str(index)
                args=[sys.executable,str(path),*scope]
                ids=discover_cases(args,root/'collect',jobs=2,timeout=5)
                self.assertEqual(ids, expected)
                parent=CheckPlan('selected','fixture',args,None,'focused',True)
                plans=case_plans(parent,ids,root/'cases')
                results=run_scheduled_checks(plans,jobs=2,timeout_seconds=5,fail_fast=False,scratch=root/'run')
                self.assertEqual([r.exit_code for r in results],[0]*len(ids),
                    '\n'.join(r.stderr_path.read_text() for r in results))

    def test_real_discovery_duplicate_zero_and_loader_error_reject_before_cases(self):
        from lib.validation.validation_execution import discover_cases
        for body in ['class Empty(unittest.TestCase): pass',
                     'raise RuntimeError("collection failed")',
                     'class Example(unittest.TestCase):\n def test_one(self): pass\n'
                     'def load_tests(loader,tests,pattern):\n return unittest.TestSuite([Example("test_one"),Example("test_one")])']:
            with self.subTest(body=body), self.assertRaises(ValueError):
                discover_cases([sys.executable,str(self.fixture(body))], self.root/'collect', jobs=1, timeout=5)

    def test_actual_worker_rejects_skipped_missing_and_disagreeing_receipts(self):
        from lib.validation.validation_execution import discover_cases, case_plans
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
        from lib.validation.validation_execution import case_plans
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
        from lib.validation.validation_execution import _case_command
        marker = self.root/'forbidden'
        path = self.fixture(f'open({str(marker)!r},"w").close()')
        command = _case_command('unknown_value',self.root/'receipt',[sys.executable,str(path)])
        result = subprocess.run(command,capture_output=True,text=True)
        self.assertEqual(result.returncode,4,result.stdout+result.stderr)
        self.assertFalse(marker.exists())

    def test_expansion_keeps_all_case_dependencies_and_failed_case_blocks_consumer(self):
        from lib.validation.validation_execution import expand_cases
        from lib.validation.validation_selection import CheckCatalogEntry, command_basis
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
        from lib.validation.validation_execution import discover_cases
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
                dict(id='change_metadata.regression',command='python tests/engineering/validation/test-change-metadata-validator.py')])
        fixture = self.root/'selection.json'
        fixture.write_text(json.dumps(payload))
        env = dict(os.environ,RIGORLOOP_SELECTOR_FIXTURE=str(fixture))
        result = subprocess.run(['bash','scripts/ci.sh','--mode','explicit','--path',
            'tests/engineering/validation/test-change-metadata-validator.py','--jobs','2'],env=env,capture_output=True,text=True,
            cwd=ROOT)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        lines = [line for line in result.stdout.splitlines()
                 if line.startswith('change_metadata.regression::') and ' | passed | ok | ' in line]
        self.assertEqual(len(lines),7,result.stdout)
        self.assertIn('change_metadata.regression::ExplicitRecordingMetadataTests.test_explicit_recording_unknown_value_and_mixed_contract_fail_closed',result.stdout)

    def test_case_expansion_preserves_declared_serial_resource_constraint(self):
        from lib.validation.validation_execution import case_plans
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

    def test_normal_and_isolated_fixture_preserve_hooks_population_and_parallelism(self):
        path = self.fixture('class Example(unittest.TestCase):\n'
            ' def setUp(self):\n  import tempfile\n  self.root=tempfile.TemporaryDirectory()\n  self.addCleanup(self.root.cleanup)\n'
            ' def test_a(self):\n  from pathlib import Path\n  import os,time\n  p=Path(self.root.name)/"owned"\n  self.assertFalse(p.exists())\n  p.touch()\n'
            '  gate=os.environ.get("RIGORLOOP_CASE_RENDEZVOUS")\n'
            '  if gate:\n   gate=Path(gate)\n   (gate/self._testMethodName).touch()\n   deadline=time.monotonic()+10\n'
            '   while not all((gate/name).exists() for name in ("test_a","test_b")):\n'
            '    if time.monotonic()>deadline: self.fail("case rendezvous did not complete")\n'
            '    time.sleep(.01)\n'
            ' def test_b(self): self.test_a()')
        self.exercise_fixture(path)

    def exercise_fixture(self, path):
        from lib.validation.validation_execution import discover_cases, case_plans, _case_command
        args = [sys.executable, str(path)]
        ids = discover_cases(args,self.root/'discovery',jobs=2,timeout=300)
        baseline = self.root/'baseline.json'
        command = _case_command('observe',baseline,args)
        parent = CheckPlan('suite',' '.join(args),args,None,'focused',True)
        direct = CheckPlan('direct',' '.join(args),command,None,'focused',False)
        with patch.dict(os.environ, {'RIGORLOOP_CASE_RENDEZVOUS': ''}):
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
            available = min(jobs,int(os.environ.get('RIGORLOOP_VALIDATION_WORKERS',str(jobs))))
            gate = scope/'rendezvous'
            gate.mkdir(parents=True)
            # Shared markers belong to this synthetic concurrency scenario only.
            # A deadline bounds a broken handshake; it is not a speed assertion.
            with patch.dict(os.environ, {'RIGORLOOP_CASE_RENDEZVOUS': str(gate) if available > 1 else ''}):
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
            self.assertEqual(overlap,available>1, f'{path.name}: expected actual case overlap only with multiple workers')
            print(f'CASE POPULATION {path.name}: jobs={available} discovered={len(ids)} started={len(started)} completed={len(completed)} overlap={overlap}',flush=True)
        print('CASE IDS '+json.dumps({'suite':path.name,'ids':ids}),flush=True)
