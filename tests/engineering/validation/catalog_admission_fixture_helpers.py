"""Private document packages with independently declared expectations."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
PACKAGES = {
    'release': ('docs/design/engineering/release/release.md', 'docs/design/engineering/release/test-design',
                'tests/engineering/release/test-release-transaction.py', 'REL-SR-01',
                ('profile-input', 'preparation', 'preflight', 'candidate-identity', 'approval-recovery', 'evidence-closeout', 'maintenance-review')),
    'skill': ('docs/design/skill/skill.md', 'docs/design/skill/test-design',
              'tests/skill/test-skill-validator.py', 'SKL-SR-01',
              ('capability-contract', 'resource-contract', 'recording-composition', 'implementation-handoffs', 'capability-composition')),
    'authoring': ('docs/design/skill/authoring/authoring.md', 'docs/design/skill/authoring/test-design',
                  'tests/skill/test-skill-validator.py', 'AUTH-SR-01',
                  ('refinement', 'scope-handoff', 'correction-reconciliation')),
}

def write(root, path, content):
    destination = root / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content)
    return destination

def write_json(root, path, value):
    return write(root, path, json.dumps(value, indent=2) + '\n')

def model_text(requirement):
    dimensions = ('Input domain', 'State/lifecycle', 'Identity/authority', 'Composition/path',
                  'Temporal/retry', 'Failure/recovery', 'Compatibility/migration', 'External/environment')
    return ('# Fixture model\n\nModel validation contract: model-document-v1\n\n'
            '## Requirements\n\n| ID | Required behavior |\n| --- | --- |\n'
            f'| {requirement} | Protect the current outcome. |\n\n'
            '### Boundary scan and acceptance scenarios\n\n'
            '| Dimension | Requirement basis | Distinct outcome to demonstrate |\n| --- | --- | --- |\n'
            + ''.join(f'| {d} | {requirement} | Observe the protected outcome. |\n' for d in dimensions))

def package(root, model='release'):
    owner_path, directory, entrypoint, requirement, groups = PACKAGES[model]
    owner = {'model': model, 'design': owner_path, 'test_design': directory+'/test-design.md'}
    write(root, owner_path, model_text(requirement))
    write(root, owner['test_design'], '# Test design\n\n## Catalog contract\n\nFixture strategy.\n')
    if model == 'authoring':
        write(root, PACKAGES['skill'][1]+'/test-design.md', '# Shared field contract\n\n## Catalog contract\n\nShared structure.\n')
    write(root, 'scripts/example.py', 'def operation():\n    return 1\n')
    write(root, entrypoint, '''import unittest
class ScenarioTests(unittest.TestCase):
    def test_accepts(self):
        raise AssertionError("catalog collection executed a test body")
if __name__ == "__main__":
    unittest.main()
''')
    index = {
        'format': model+'-test-catalog-draft', 'format_version': 2, 'owner': owner,
        'scope': {'model': model, 'boundary': 'Current outcome.', 'entrypoint': entrypoint, 'coverage_claim': 'One illustrative outcome.'},
        'fixture_rules': {key: 'Fresh independent fixture.' for key in ('isolation','independent_expectations','negative_setup','version_roles','resource_boundary')},
        'groups': [{'id': group, 'title': group, 'path': directory+'/cases/'+group+'.json'} for group in groups],
    }
    write_json(root, directory+'/test-cases.json', index)
    for number, group in enumerate(index['groups']):
        review = model == 'authoring'
        case = {'id': f'Case-{number}', 'title': 'Protect the outcome', 'requirements': [requirement],
                'technique': 'walkthrough' if review else 'equivalence-partition', 'risk': 'Accept a broken outcome.',
                'method': 'independent-review' if review else 'automated-test', 'boundary': 'review' if review else 'contract',
                'target': {'path': owner_path, 'section': 'Requirements'} if review else {'path': 'scripts/example.py', 'symbol': 'operation'},
                'given': {'fixture': 'baseline', 'conditions': ['Valid input.']}, 'when': ['Inspect the result.'], 'then': ['Reject the fault.'],
                'realization': {'state': 'proposed' if review else 'existing',
                                'tests': [] if review else [{'path': entrypoint, 'symbol': 'ScenarioTests.test_accepts'}],
                                'gaps': ['Pending independent assessment.'] if review else []}}
        write_json(root, group['path'], {'format': model+'-test-cases-draft', 'format_version': 2, 'owner': owner,
                  'scope': {'group': group['id'], 'title': group['title'], 'boundary': 'Current outcome.'},
                  'fixtures': [{'id': 'baseline', 'initial_state': ['Valid private input.']}], 'cases': [case]})
    return index


def current_documents(root):
    """Current model grammar plus complete synthetic declared test detail."""
    from boundary_fixture_helpers import EXPECTED_MODEL_PATHS
    for relative in EXPECTED_MODEL_PATHS:
        write(root, relative, (ROOT/relative).read_text())
    details = {'docs/design/test-design/README.md', 'docs/design/test-design/rules.md'}
    write(root, 'docs/design/system.md', model_text('SYS-SR-01'))
    for path in details:
        write(root, path, '# Shared test guidance\n\nCurrent rules.\n')
    for model in PACKAGES:
        index = package(root, model)
        details.update((index['owner']['test_design'], PACKAGES[model][1]+'/test-cases.json'))
        details.update(group['path'] for group in index['groups'])
    return details
