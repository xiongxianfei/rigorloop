"""Declared package admission through the real document command."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from catalog_admission_fixture_helpers import ROOT, PACKAGES, package, write_json

class TestDesignAdmissionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def validate(self, *paths):
        command = [sys.executable, '-B', str(ROOT/'scripts/validate-boundary-first.py'), '--check', '--root', str(self.root)]
        for path in paths:
            command += ['--path', path]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertTrue(result.stdout.strip(), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_declared_packages_accept_without_executing_linked_bodies(self):
        for model in PACKAGES:
            with self.subTest(model=model):
                index = package(self.root, model)
                for path in (index['owner']['design'], index['owner']['test_design'], PACKAGES[model][1]+'/test-cases.json', index['groups'][0]['path']):
                    code, result = self.validate(path)
                    self.assertEqual(code, 0, result)

    def test_unknown_method_precedes_missing_fixture(self):
        index = package(self.root)
        path = index['groups'][0]['path']
        code, result = self.validate(path)
        self.assertEqual(code, 0, result)
        group = json.loads((self.root/path).read_text())
        group['cases'][0]['method'] = 'unknown_value'
        group['cases'][0]['given']['fixture'] = 'missing'
        write_json(self.root, path, group)
        code, result = self.validate(path)
        self.assertEqual(code, 1)
        self.assertTrue(all(i['check_id'] == 'BFR-TEST-SHAPE' for i in result['issues']), result)
        self.assertIn('method', result['issues'][0]['message'])

    def test_generic_flat_models_retain_existing_grammar(self):
        from catalog_admission_fixture_helpers import model_text, write
        for model in ('release', 'skill', 'authoring'):
            with self.subTest(model=model):
                path = f'docs/design/{model}.md'
                write(self.root, path, model_text('LOCAL-SR-01'))
                code, result = self.validate(path)
                self.assertEqual(code, 0, result)
                self.assertEqual(result['paths'], [path])
                write(self.root, path, '# Invalid model\n')
                self.assertEqual(self.validate(path)[0], 1)

    def test_structural_unknowns_precede_missing_references(self):
        variants = (
            ('format', ('format',), 'unknown_value'),
            ('version', ('format_version',), 99),
            ('boolean-version', ('format_version',), True),
            ('owner-model', ('owner', 'model'), 'unknown_value'),
            ('boundary', ('cases', 0, 'boundary'), 'unknown_value'),
            ('technique', ('cases', 0, 'technique'), 'unknown_value'),
            ('state', ('cases', 0, 'realization', 'state'), 'unknown_value'),
            ('extra-group-field', ('unknown_value',), True),
            ('extra-target-field', ('cases', 0, 'target', 'unknown_value'), True),
            ('extra-given-field', ('cases', 0, 'given', 'unknown_value'), True),
            ('wrong-type', ('cases', 0, 'when'), 'not-an-array'),
        )
        for name, route, value in variants:
            with self.subTest(variant=name), tempfile.TemporaryDirectory() as temporary:
                self.root = Path(temporary)
                index = package(self.root)
                path = index['groups'][0]['path']
                code, result = self.validate(path)
                self.assertEqual(code, 0, result)
                group = json.loads((self.root/path).read_text())
                group['cases'][0]['given']['fixture'] = 'missing'
                target = group
                for key in route[:-1]:
                    target = target[key]
                target[route[-1]] = value
                write_json(self.root, path, group)
                code, result = self.validate(path)
                self.assertEqual(code, 1)
                self.assertTrue(all(i['check_id'] == 'BFR-TEST-SHAPE' for i in result['issues']), result)

    def test_json_syntax_duplicate_keys_and_nonfinite_values_reject(self):
        for fault in ('syntax', 'duplicate-key', 'descriptive-duplicate', 'nonfinite', 'overflow'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temporary:
                self.root = Path(temporary)
                index = package(self.root)
                path = self.root/index['groups'][0]['path']
                self.assertEqual(self.validate(str(path.relative_to(self.root)))[0], 0)
                body = path.read_text()
                if fault == 'syntax':
                    body = '{'
                elif fault == 'duplicate-key':
                    body = body.replace('"format_version": 2', '"format_version": 2, "format_version": 2')
                else:
                    value = {'descriptive-duplicate': '{"x":1,"x":2}', 'nonfinite': '{"x":NaN}', 'overflow': '{"x":1e999}'}[fault]
                    body = body.replace('"initial_state":', '"facts": '+value+', "initial_state":')
                path.write_text(body)
                code, result = self.validate(str(path.relative_to(self.root)))
                self.assertEqual(code, 1)
                self.assertEqual(result['issues'][0]['check_id'], 'BFR-TEST-READ', result)

    def test_identity_reference_and_realization_faults_reject(self):
        for fault in ('requirement', 'fixture', 'cycle', 'symbol', 'undiscovered', 'wrong-source', 'state-gap',
                      'duplicate-case', 'duplicate-variant', 'review-tests', 'review-section', 'owner', 'group-path', 'duplicate-group'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temporary:
                self.root = Path(temporary)
                index = package(self.root)
                path = index['groups'][0]['path']
                self.assertEqual(self.validate(path)[0], 0)
                group = json.loads((self.root/path).read_text())
                case = group['cases'][0]
                expected = fault
                if fault == 'requirement':
                    case['requirements'] = ['Missing-SR-01']
                elif fault == 'fixture':
                    case['given']['fixture'] = 'missing'
                elif fault == 'cycle':
                    group['fixtures'][0]['extends'] = 'baseline'
                    expected = 'cyclic'
                elif fault == 'symbol':
                    case['target']['symbol'] = 'missing'
                    expected = 'callable'
                elif fault == 'undiscovered':
                    case['realization']['tests'][0]['symbol'] = 'ScenarioTests.test_missing'
                    expected = 'not natively discovered'
                elif fault == 'wrong-source':
                    case['realization']['tests'][0]['path'] = 'scripts/example.py'
                    expected = 'not natively discovered'
                elif fault == 'state-gap':
                    case['realization']['gaps'] = ['Unproved.']
                    expected = 'inconsistent realization'
                elif fault == 'duplicate-case':
                    other_path = index['groups'][1]['path']
                    other = json.loads((self.root/other_path).read_text())
                    other['cases'][0]['id'] = case['id']
                    write_json(self.root, other_path, other)
                    expected = 'duplicate case'
                elif fault == 'duplicate-variant':
                    case['variants'] = [{'id': 'same', 'parameters': {'input': 1}}, {'id': 'same', 'parameters': {'input': 2}}]
                    expected = 'duplicate id'
                elif fault.startswith('review-'):
                    case.update(method='independent-review', boundary='review', target={'path': index['owner']['design'], 'section': 'Missing'})
                    if fault == 'review-section':
                        case['realization'] = {'state': 'proposed', 'tests': [], 'gaps': ['Pending.']}
                        expected = 'missing review target section'
                    else:
                        expected = 'review requires'
                elif fault == 'owner':
                    group['owner']['design'] = 'scripts/example.py'
                elif fault == 'group-path':
                    index['groups'][0]['path'] = 'docs/design/other/cases/extra.json'
                    expected = 'membership'
                elif fault == 'duplicate-group':
                    index['groups'].append(index['groups'][0])
                    expected = 'duplicate'
                write_json(self.root, path, group)
                write_json(self.root, PACKAGES['release'][1]+'/test-cases.json', index)
                before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
                code, result = self.validate(path)
                self.assertEqual(code, 1)
                self.assertIn(expected, '\n'.join(i['message'] for i in result['issues']), result)
                after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
                self.assertEqual(before, after)

    def test_missing_symlinked_unindexed_and_mixed_inputs_fail(self):
        for fault in ('missing', 'symlink-file', 'symlink-parent', 'unindexed', 'mixed', 'escape', 'old-owner'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temporary:
                self.root = Path(temporary)
                index = package(self.root)
                path = index['groups'][0]['path']
                self.assertEqual(self.validate(path)[0], 0)
                selected = [path]
                target = self.root/path
                if fault == 'missing':
                    target.unlink()
                elif fault == 'symlink-file':
                    target.unlink()
                    target.symlink_to(Path(index['groups'][1]['path']).name)
                elif fault == 'symlink-parent':
                    directory = target.parent
                    moved = directory.with_name('moved')
                    directory.rename(moved)
                    directory.symlink_to(moved.name, target_is_directory=True)
                elif fault == 'unindexed':
                    target.with_name('extra.json').write_text('{}')
                elif fault == 'mixed':
                    selected.append('docs/design/extra/unrecognized.json')
                elif fault == 'escape':
                    index['groups'][0]['path'] = '../escape.json'
                    write_json(self.root, PACKAGES['release'][1]+'/test-cases.json', index)
                else:
                    old = self.root/'docs/design/engineering/release.md'
                    old.write_text((self.root/index['owner']['design']).read_text())
                    selected = ['docs/design/engineering/release.md']
                code, result = self.validate(*selected)
                self.assertEqual(code, 1, result)
                self.assertTrue(result['issues'])

    def test_shared_guidance_pairs_system_and_checks_local_references(self):
        from catalog_admission_fixture_helpers import model_text, write
        write(self.root, 'docs/design/system.md', model_text('SYS-SR-01'))
        readme = 'docs/design/test-design/README.md'
        rules = 'docs/design/test-design/rules.md'
        write(self.root, readme, '# Navigation\n\n[Rules](rules.md).\n')
        write(self.root, rules, '# Rules\n\nCurrent rules.\n')
        code, result = self.validate(readme)
        self.assertEqual(code, 0, result)
        self.assertEqual(set(result['paths']), {readme, rules, 'docs/design/system.md'})
        write(self.root, rules, '# Rules\n\n[Missing](missing.md).\n')
        code, result = self.validate(readme)
        self.assertEqual(code, 1)
        self.assertEqual(result['issues'][0]['check_id'], 'BFR-TEST-MARKDOWN')

    def test_generated_native_method_is_reachable_at_its_real_source(self):
        from catalog_admission_fixture_helpers import write
        index = package(self.root)
        entrypoint = index['scope']['entrypoint']
        write(self.root, entrypoint, '''import unittest
class ScenarioTests(unittest.TestCase):
    pass
def generated(self):
    raise AssertionError("body must not execute")
ScenarioTests.test_accepts = generated
if __name__ == "__main__":
    unittest.main()
''')
        code, result = self.validate(index['groups'][0]['path'])
        self.assertEqual(code, 0, result)

    def test_authoring_bindings_reject_automation_before_missing_fixture(self):
        for field, value in (('method', 'automated-test'), ('boundary', 'contract'),
                             ('technique', 'property'), ('state', 'existing')):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                self.root = Path(temporary)
                index = package(self.root, 'authoring')
                path = index['groups'][0]['path']
                self.assertEqual(self.validate(path)[0], 0)
                group = json.loads((self.root/path).read_text())
                case = group['cases'][0]
                case['given']['fixture'] = 'missing'
                target = case['realization'] if field == 'state' else case
                target[field] = value
                write_json(self.root, path, group)
                code, result = self.validate(path)
                self.assertEqual(code, 1)
                self.assertTrue(all(i['check_id'] == 'BFR-TEST-SHAPE' for i in result['issues']), result)
                self.assertIn(field, result['issues'][0]['message'])

    def test_markdown_reference_links_and_pre_normalization_symlinks_reject(self):
        from catalog_admission_fixture_helpers import model_text, write
        for fault in ('reference-link', 'undefined-reference', 'symlink-before-parent'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as temporary:
                self.root = Path(temporary)
                write(self.root, 'docs/design/system.md', model_text('SYS-SR-01'))
                readme = 'docs/design/test-design/README.md'
                rules = 'docs/design/test-design/rules.md'
                write(self.root, readme, '# Navigation\n\n[Rules][rules]\n\n[rules]: rules.md\n')
                write(self.root, rules, '# Rules\n\nCurrent rules.\n')
                self.assertEqual(self.validate(readme)[0], 0)
                if fault == 'reference-link':
                    write(self.root, readme, '# Navigation\n\n[Missing][bad]\n\n[bad]: missing.md\n')
                elif fault == 'undefined-reference':
                    write(self.root, readme, '# Navigation\n\n[Missing][undefined]\n')
                else:
                    # Normalizing hop/.. must not conceal traversal of a symlink.
                    (self.root/'docs/design/test-design/hop').symlink_to(self.root.parent, target_is_directory=True)
                    write(self.root, readme, '# Navigation\n\n[Rules](hop/../rules.md)\n')
                code, result = self.validate(readme)
                self.assertEqual(code, 1, result)
                self.assertEqual(result['issues'][0]['check_id'], 'BFR-TEST-MARKDOWN')
