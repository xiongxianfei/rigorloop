"""Fresh release fixture values shared without TestCase lifecycle coupling."""
from lib.release.release_execution import environment_identity


def approval_fixture():
    """Return independently owned candidate, binding and inspected provider facts."""
    candidate = {'candidate_id': 'a' * 64, 'source_commit': 'b' * 40,
        'source_ref': 'refs/heads/main', 'repository': 'xiongxianfei/rigorloop'}
    binding = {'run_id': 12, 'artifact_id': 13, 'artifact_digest': 'sha256:' + 'c' * 64,
        'candidate_id': 'a' * 64, 'environment': 'release', 'artifact_name': 'release-candidate-12'}
    facts = {
        'repository': {'full_name': 'xiongxianfei/rigorloop', 'id': 7, 'default_branch': 'main'},
        'run': {'id': 12, 'event': 'push', 'head_sha': 'b' * 40, 'head_branch': 'main',
            'path': '.github/workflows/release.yml', 'status': 'in_progress', 'run_attempt': 1},
        'artifact': {'id': 13, 'name': 'release-candidate-12', 'digest': binding['artifact_digest'],
            'expired': False, 'workflow_run': {'id': 12, 'head_sha': 'b' * 40, 'repository_id': 7, 'head_repository_id': 7}},
        'environment': {'id': 9, 'name': 'release', 'deployment_branch_policy': {'protected_branches': True, 'custom_branch_policies': False},
            'protection_rules': [{'type': 'required_reviewers', 'reviewers': [{'type': 'User', 'reviewer': {'id': 2}}]}]},
        'approvals': [{'state': 'approved', 'environments': [{'id': 9, 'name': 'release'}], 'user': {'id': 2, 'login': 'maintainer'}}]}

    candidate['approval_environment_identity'] = environment_identity(facts['environment'])

    return candidate, binding, facts
