"""Small authority and real Git identity fixtures."""
import subprocess
from pathlib import Path
from lib.release.release_execution import environment_identity

def authority_fixture():
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
            'protection_rules': []},
        'branch': {'name': 'main', 'protected': True}}

    candidate['initiation'] = {'policy': 'workflow-start-v1', 'run_id': 12}
    candidate['release_environment_identity'] = environment_identity(facts['environment'])

    return candidate, binding, facts

def make_tag_identity_repo(root: Path) -> str:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "RigorLoop Test"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
    (root / "README.md").write_text("release\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "release"], check=True)
    return subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

REQUIRED_PROFILE_FIELD_CASES = (
    ("invalid-missing-release-tag.yaml", "release_tag"),
    ("invalid-missing-package-version.yaml", "package_version"),
    ("invalid-missing-npm-dist-tag.yaml", "npm_dist_tag"),
    ("invalid-missing-npm-package.yaml", "npm_package"),
    ("invalid-missing-targets.yaml", "targets"),
    ("invalid-missing-adapter-artifacts.yaml", "adapter_artifacts"),
    ("invalid-missing-publication.yaml", "publication"),
    ("invalid-missing-evidence.yaml", "evidence"),
    ("invalid-missing-validation.yaml", "validation"),
)
