"""Focused and boundary composition, deduplication and prerequisites."""

from __future__ import annotations

import sys
from pathlib import Path
import dataclasses
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.validation_execution import CheckPlan, run_scheduled_checks, validate_plans
from lib.validation.validation_selection import CHECK_CATALOG


class CompositionTests(unittest.TestCase):
    def coverage_plan(self, key, **changes):
        import shlex
        entry = CHECK_CATALOG[key]
        return dataclasses.replace(CheckPlan(key, entry.command_template, shlex.split(entry.command_template),
            key+' reason', 'focused', entry.parallel_safe, entry.dependencies, entry.constraints.demand), **changes)

    def test_authored_coverage_retains_narrow_only_and_required_full_scope(self):
        from lib.validation.validation_execution import allocate_coverage
        pairs = [('adapters.full_regression', 'adapters.regression'),
                 ('adapters.regression', 'adapters.drift'), ('adapters.regression', 'adapters.validate'),
                 ('rigorloop_cli.test', 'record_retirement.regression')]
        for full, narrow in pairs:
            with self.subTest(full=full, narrow=narrow):
                first = self.coverage_plan(narrow)
                self.assertEqual(allocate_coverage([first]), [first])
                plans = allocate_coverage([first, self.coverage_plan(full, phase='boundary')])
                self.assertEqual({p.check_id for p in plans}, {full})
                self.assertEqual([p.phase for p in plans], ['focused','boundary'])
                self.assertTrue(all(p.args == self.coverage_plan(full).args for p in plans))
        plans = allocate_coverage([self.coverage_plan(k) for k in
            ('adapters.drift','adapters.regression','adapters.full_regression')])
        self.assertEqual({p.check_id for p in plans}, {'adapters.full_regression'})

    def test_authored_coverage_rejects_stale_configuration_and_preserves_prerequisites(self):
        from lib.validation.validation_execution import allocate_coverage
        full = self.coverage_plan('adapters.full_regression')
        narrow = self.coverage_plan('adapters.drift')
        for changes in ({'args':narrow.args+['--different']}, {'demand':2}, {'parallel_safe':False}):
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'coverage basis'):
                allocate_coverage([full,dataclasses.replace(narrow,**changes)])
        entry = CHECK_CATALOG[narrow.check_id]
        for changes in ({'dependencies':('skills.validate',)},
                        {'constraints':dataclasses.replace(entry.constraints,basis='changed')}):
            with patch.dict(CHECK_CATALOG,{narrow.check_id:dataclasses.replace(entry,**changes)}):
                with self.assertRaisesRegex(ValueError,'coverage basis'):
                    allocate_coverage([full,narrow])
        prep=CheckPlan('prep','fixture',['true'],None,'preflight',True)
        consumer=CheckPlan('consumer','fixture',['true'],None,'boundary',True,(narrow.check_id,))
        plans=allocate_coverage([prep,dataclasses.replace(narrow,dependencies=('prep',)),full,consumer])
        self.assertTrue(all(p.dependencies==('prep',) for p in plans if p.check_id==full.check_id))
        self.assertEqual(plans[-1].dependencies,(full.check_id,))
        from lib.validation.validation_execution import expand_groups
        with tempfile.TemporaryDirectory() as temporary:
            cyclic=expand_groups([dataclasses.replace(narrow,dependencies=(full.check_id,)),full],Path(temporary))
        with self.assertRaisesRegex(ValueError, 'dependency cycle'): validate_plans(cyclic,jobs=2)
        separate=self.coverage_plan('adapters.validate',check_id='fresh-observation')
        self.assertEqual(allocate_coverage([full,separate]),[full,separate])

    def test_authored_coverage_runs_once_and_failed_focus_blocks_boundary(self):
        from lib.validation.validation_execution import expand_groups
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            narrow=self.coverage_plan('adapters.drift',dependencies=('prep',))
            full=self.coverage_plan('adapters.full_regression',phase='boundary')
            prep=CheckPlan('prep','fixture',[sys.executable,'-c','raise SystemExit(7)'],None,'preflight',True)
            tail=CheckPlan('tail','fixture',[sys.executable,'-c','pass'],None,'boundary',True)
            plans=expand_groups([prep,narrow,full,tail],root)
            self.assertEqual([p.check_id for p in plans],['prep',full.check_id,'tail'])
            self.assertEqual(plans[1].phase,'focused')
            self.assertIn(narrow.reason,plans[1].reason)
            self.assertIn(full.reason,plans[1].reason)
            marker=root/'ran'
            plans[1].args=[sys.executable,'-c',f'from pathlib import Path; Path({str(marker)!r}).touch()']
            results=run_scheduled_checks(plans,jobs=2,timeout_seconds=5,fail_fast=False,scratch=root/'run')
            self.assertEqual([r.exit_code for r in results],[7,125,125])
            self.assertFalse(marker.exists())
            plans[0].args=[sys.executable,'-c','pass']
            plans[1].args=[sys.executable,'-c',f'from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+"x" if p.exists() else "x")']
            results=run_scheduled_checks(plans,jobs=2,timeout_seconds=5,fail_fast=False,scratch=root/'success')
            self.assertEqual([r.exit_code for r in results],[0,0,0])
            self.assertEqual(marker.read_text(),'x')

    def test_canonical_overlap_runs_once_with_reasons_and_failure_gate(self):
        from lib.validation.validation_execution import expand_groups
        for diagnostic in (False, True):
            with self.subTest(diagnostic=diagnostic), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                marker = root/'executions'
                args = [sys.executable, '-c', f'from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+"x" if p.exists() else "x")']
                shared = CheckPlan('shared', 'fixture', args, 'focused reason', 'focused', True)
                failed = CheckPlan('failed', 'fixture', [sys.executable,'-c','raise SystemExit(7)'], None, 'focused', True)
                tail = CheckPlan('tail', 'fixture', [sys.executable,'-c','pass'], None, 'focused', True)
                group = CheckPlan('broad_smoke.repo', 'fixture', ['unused'], 'boundary reason', 'boundary', False)
                with patch('lib.validation.validation_execution.compose_mode', return_value=[dataclasses.replace(shared,reason='catalog reason'),tail]):
                    plans = expand_groups([shared,failed,group],root,diagnostic=diagnostic)
                self.assertEqual([p.check_id for p in plans],['shared','failed','tail'])
                self.assertEqual(plans[0].phase,'focused')
                for reason in ('focused reason','boundary reason','catalog reason'):
                    self.assertIn(reason,plans[0].reason)
                results = run_scheduled_checks(plans,jobs=2,timeout_seconds=5,fail_fast=False,scratch=root/'run')
                self.assertEqual(marker.read_text(),'x')
                self.assertEqual([r.exit_code for r in results],[0,7,0 if diagnostic else 125])
                import io
                from contextlib import redirect_stdout
                from lib.validation.validation_execution import print_summary
                output = io.StringIO()
                with redirect_stdout(output):
                    # The boundary may contain only already-run overlap.
                    print_summary(results[:2],boundary_required=True)
                self.assertIn('Boundary scope: unsuccessful',output.getvalue())

    def test_overlap_preserves_preparation_and_distinct_observations(self):
        from lib.validation.validation_execution import expand_groups
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prep = CheckPlan('prep','fixture',[sys.executable,'-c','raise SystemExit(9)'],None,'focused',True)
            shared = CheckPlan('shared','fixture',[sys.executable,'-c','pass'],None,'focused',True,('prep',))
            separate = dataclasses.replace(shared,check_id='separate')
            group = CheckPlan('broad_smoke.repo','fixture',['unused'],None,'boundary',False)
            with patch('lib.validation.validation_execution.compose_mode',return_value=[dataclasses.replace(shared),separate]):
                plans = expand_groups([prep,shared,group],root)
            self.assertEqual([p.check_id for p in plans],['prep','shared','separate'])
            self.assertIn('prep',plans[1].dependencies)
            results=run_scheduled_checks(plans,jobs=1,timeout_seconds=5,fail_fast=False,scratch=root/'run')
            self.assertEqual([r.exit_code for r in results],[9,125,125])

    def test_conflicting_same_id_arguments_or_constraints_reject_before_launch(self):
        from lib.validation.validation_execution import expand_groups
        first=CheckPlan('same','fixture',[sys.executable,'-c','pass'],None,'focused',True)
        for changes in ({'args':[sys.executable,'-c','raise SystemExit(7)']},
                        {'demand':2},{'demand':True},{'parallel_safe':False},{'parallel_safe':1},{'dependencies':('prep',)}):
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as temporary:
                with self.assertRaisesRegex(ValueError,'conflicting.*same'):
                    expand_groups([first,dataclasses.replace(first,**changes)],Path(temporary))

    def test_boundary_only_and_new_invocation_execute_again(self):
        from lib.validation.validation_execution import expand_groups
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            marker=root/'count'
            args=[sys.executable,'-c',f'from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+"x" if p.exists() else "x")']
            shared=CheckPlan('shared','fixture',args,None,'focused',True)
            group=CheckPlan('broad_smoke.repo','fixture',['unused'],None,'boundary',False)
            for index in range(2):
                with patch('lib.validation.validation_execution.compose_mode',return_value=[dataclasses.replace(shared)]):
                    plans=expand_groups([group],root)
                results=run_scheduled_checks(plans,jobs=1,timeout_seconds=5,fail_fast=False,scratch=root/str(index))
                self.assertEqual([r.exit_code for r in results],[0])
            self.assertEqual(marker.read_text(),'xx')

    def test_pr_snapshot_and_broad_discovery_compose_as_distinct_checks(self):
        # Real selector + real catalog composition: neither the exact commit
        # snapshot nor current-worktree discovery may overwrite the other.
        import shlex
        from lib.validation.validation_execution import expand_groups
        from lib.validation.validation_selection import SelectionRequest, select_validation
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary) / 'repository'
            repo.mkdir()
            def git(*args):
                return subprocess.check_output(['git', '-C', str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()
            git('init', '--quiet')
            (repo / 'README.md').write_text('# Original\n')
            git('add', '.')
            commit = ('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '-qm')
            git(*commit, 'Original')
            base = git('rev-parse', 'HEAD')
            (repo / 'README.md').write_text('# Changed\n')
            git('add', '.')
            git(*commit, 'Changed')
            head = git('rev-parse', 'HEAD')
            selected = select_validation(SelectionRequest(mode="pr", base=base, head=head, repo_root=repo, broad_smoke=True))
            self.assertEqual(selected.status, "ok", selected.blocking_results)
            checks = [c for c in selected.selected_checks if c['id'] == 'broad_smoke.repo' or '--revision' in shlex.split(c['command'])]
            self.assertEqual(len(checks), 2)
            plans = [CheckPlan(c['id'], c['command'], shlex.split(c['command']), c.get('reason'), c['phase'], False) for c in checks]
            composed = expand_groups(plans, Path(temporary))
        record_checks = [p for p in composed if 'scripts/validate-governed-lifecycle-cli.py' in p.args]
        self.assertEqual(len(record_checks), 2)
        self.assertEqual(len({p.check_id for p in record_checks}), 2)
        self.assertEqual({tuple(p.args[2:]) for p in record_checks}, {(), ('--revision', head)})

    def test_catalog_composes_broad_and_main_with_distinct_preserved_package_versions(self):
        from lib.validation.validation_execution import compose_mode
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
            self.assertIn('rigorloop_cli.test',{p.check_id for p in plans})
            self.assertIn('main.governed_lifecycle_cli.validate',{p.check_id for p in plans})
            self.assertIn('governed_lifecycle_cli_wrapper.test',{p.check_id for p in plans})

    def test_unknown_value_composed_mode_rejects(self):
        from lib.validation.validation_execution import compose_mode
        with tempfile.TemporaryDirectory() as temporary, self.assertRaises(ValueError):
            compose_mode('unknown_value',Path(temporary))

    def test_retired_classification_override_rejects_before_work(self):
        env = dict(os.environ,RIGORLOOP_BROAD_SMOKE_CLASSIFICATION='/no/retired/classification')
        result = subprocess.run(['bash','scripts/ci.sh','--mode','broad-smoke','--jobs','2'],env=env,cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,4)
        self.assertIn('retired',result.stderr)
        self.assertNotIn('==>',result.stdout)
