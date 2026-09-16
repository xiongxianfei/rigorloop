"""Native Node discovery, named cases, hooks and exact reruns."""

from __future__ import annotations

import sys
from pathlib import Path
import json
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.validation_execution import CheckPlan, run_scheduled_checks


class NodeCaseAdapterTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def fixture(self, body):
        path = self.root/'suite.test.mjs'
        path.write_text("import test, {describe, before, beforeEach, afterEach} from 'node:test';\n"
                        "import assert from 'node:assert/strict';\n"+body)
        return path

    def collect(self, path):
        from lib.validation.validation_execution import discover_node_cases
        return discover_node_cases(['node','--test',str(path)],self.root/'collect',jobs=1,timeout=10)

    def run_cases(self, path, groups):
        from lib.validation.validation_execution import node_case_plans
        args=['node','--test',str(path)]
        parent=CheckPlan('node-suite','native fixture',args,None,'focused',True)
        plans=node_case_plans(parent,groups,self.root/'cases')
        return run_scheduled_checks(plans,jobs=2,timeout_seconds=10,fail_fast=False,scratch=self.root/'run')

    def test_native_default_named_dynamic_declarations_and_suite_hooks(self):
        marker=self.root/'collection-side-effect'
        path=self.fixture("import {writeFileSync} from 'node:fs';\n"
            f"let ready=false; beforeEach(()=>{{ready=true;writeFileSync({str(marker)!r}+process.pid,'hook')}});\n"
            "afterEach(()=>assert.equal(ready,true));\n"
            f"describe('parent',()=>{{before(()=>writeFileSync({str(marker)!r}+process.pid,'suite hook'));for(const name of ['a.+','b']) test(name,()=>assert.equal(ready,true));}});\n")
        groups=self.collect(path)
        self.assertEqual(groups,[{'file':str(path),'ids':['parent a.+','parent b']}])
        self.assertEqual(list(self.root.glob('collection-side-effect*')),[],'collection must not run bodies or hooks')
        results=self.run_cases(path,groups)
        self.assertEqual([r.exit_code for r in results],[0,0],[(r.exit_reason,r.stderr_path.read_text()) for r in results])
        for r in results:
            receipt=json.loads(r.plan.case_receipt.read_text())
            self.assertEqual(receipt['started'],[r.plan.case_id])
            self.assertEqual(receipt['completed'],[r.plan.case_id])
            self.assertEqual(subprocess.run(r.plan.rerun,capture_output=True).returncode,0)

    def test_zero_duplicate_ambiguous_and_nested_worker_collection_reject(self):
        for body in ["", "test('same',()=>{});test('same',()=>{});",
                     "test('parent leaf',()=>{});describe('parent',()=>test('leaf',()=>{}));",
                     "test('pool',{concurrency:2},()=>{});", "throw Error('load failed')"]:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.collect(self.fixture(body))

    def test_skipped_todo_assertion_zero_and_dynamic_subcases_cannot_pass(self):
        for body in ["test('required',{skip:true},()=>{});", "test.todo('required');",
                     "test('required',()=>assert.fail('actual failure'));",
                     "test('required',async t=>{await t.test('hidden',()=>{});});"]:
            with self.subTest(body=body):
                path=self.fixture(body);groups=self.collect(path)
                result=self.run_cases(path,groups)[0]
                self.assertNotEqual(result.exit_code,0,result.stderr_path.read_text())
        path=self.fixture("test('required',()=>{});");groups=self.collect(path)
        path.write_text("import {test} from 'node:test';test('different',()=>{});")
        self.assertNotEqual(self.run_cases(path,groups)[0].exit_code,0)

    def test_native_scope_and_adapter_modes_fail_closed(self):
        from lib.validation.validation_execution import discover_node_cases, _node_command
        path=self.fixture("test('required',()=>{});")
        for args in [['node','--test','--unknown_value',str(path)],['node','--test'],['npm','run','other']]:
            with self.subTest(args=args),self.assertRaises(ValueError):
                discover_node_cases(args,self.root/'invalid',jobs=1,timeout=10)
        result=subprocess.run(_node_command('unknown_value',self.root/'receipt',{'files':[str(path)]}),capture_output=True,text=True)
        self.assertEqual(result.returncode,4)
        self.assertIn('unknown Node adapter mode',result.stderr)


    def test_package_native_glob_and_rerun_preserve_working_directory(self):
        from lib.validation.validation_execution import discover_node_cases,node_case_plans
        package=self.root/'package';(package/'test/nested').mkdir(parents=True)
        (package/'package.json').write_text(json.dumps({'type':'module','scripts':{'test':'node --test "test/**/*.test.js"'}}))
        path=package/'test/nested/actual.test.js'
        path.write_text("import test from 'node:test';import assert from 'node:assert/strict';"
                        f"test('cwd',()=>assert.equal(process.cwd(),{str(package)!r}));")
        (package/'test/helper.mjs').write_text("throw Error('helper is not a test entrypoint');")
        args=['npm','test','--prefix',str(package)]
        groups=discover_node_cases(args,self.root/'package-collect',jobs=1,timeout=10)
        self.assertEqual(groups,[{'file':str(path),'ids':['cwd']}])
        parent=CheckPlan('native-package','fixture',args,None,'focused',True)
        plans=node_case_plans(parent,groups,self.root/'package-cases')
        result=run_scheduled_checks(plans,jobs=1,timeout_seconds=10,fail_fast=False,scratch=self.root/'package-run')[0]
        self.assertEqual(result.exit_code,0,result.stderr_path.read_text())
        self.assertEqual(subprocess.run(plans[0].rerun,capture_output=True).returncode,0)
        (package/'package.json').write_text(json.dumps({'scripts':{'test':'node --test'}}))
        with self.assertRaisesRegex(ValueError,'assessed native glob'):
            discover_node_cases(args,self.root/'stale',jobs=1,timeout=10)
