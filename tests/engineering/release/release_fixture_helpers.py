"""Fresh release inputs, explicit preparation operations and observed error invariants."""

from __future__ import annotations

import sys
from pathlib import Path
import shutil
import json
import subprocess

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import close_release_publication, prepare_release
from lib.release.release_execution import environment_identity
from release_provider_fixtures import RecordingPublicEvidenceProvider


FIXTURES = ROOT / "tests/fixtures/release-transaction"
PROFILE_FIXTURES = FIXTURES / "profiles"
CHANGE_ROOT = ROOT / "docs/changes/2026-06-29-release-transaction-automation"

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


def make_release_repo(root: Path) -> None:
    profile_dir = root / "docs" / "releases" / "profiles"
    profile_dir.mkdir(parents=True)
    shutil.copy2(PROFILE_FIXTURES / "valid-routine-v0.3.5.yaml", profile_dir / "v0.3.5.yaml")
    package_root = root / "packages" / "rigorloop"
    package_root.mkdir(parents=True)
    (package_root / "package.json").write_text(
        json.dumps(
            {
                "name": "@xiongxianfei/rigorloop",
                "version": "0.3.4",
                "files": ["dist/", "package.json", "README.md", "LICENSE"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (package_root / "README.md").write_text(
        "Pinned example:\n\n"
        "```bash\n"
        "npx @xiongxianfei/rigorloop@0.3.4 init codex --json\n"
        "```\n",
        encoding="utf-8",
    )
    metadata_dir = package_root / "dist" / "metadata"
    metadata_dir.mkdir(parents=True)
    (metadata_dir / "releases.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "releases": {
                    "v0.3.4": {
                        "source_repository": "xiongxianfei/rigorloop",
                        "release_tag": "v0.3.4",
                        "bundled_metadata": "adapter-artifacts-v0.3.4.json",
                        "bundled_metadata_sha256": "abc",
                    }
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    release_dir = root / "docs" / "releases" / "v0.3.5"
    release_dir.mkdir(parents=True)
    (release_dir / "release-notes.md").write_text(
        "# RigorLoop v0.3.5\n\n"
        "Human-authored opening narrative.\n\n"
        "<!-- rigorloop:generated:start release-transaction surface=release-metadata profile=docs/releases/profiles/v0.3.5.yaml -->\n"
        "stale generated content\n"
        "<!-- rigorloop:generated:end release-transaction surface=release-metadata -->\n\n"
        "Human-authored closing notes.\n",
        encoding="utf-8",
    )
    historical_dir = root / "docs" / "releases" / "v0.3.4"
    historical_dir.mkdir(parents=True)
    (historical_dir / "release.yaml").write_text("version: v0.3.4\n", encoding="utf-8")
    manifest_path = root / "dist" / "adapters" / "manifest.yaml"
    manifest_path.parent.mkdir(parents=True)
    shutil.copy2(ROOT / "dist" / "adapters" / "manifest.yaml", manifest_path)


def make_prepared_release(root: Path) -> Path:
    make_release_repo(root)
    prepare_release("v0.3.5", root=root)
    return root / "docs" / "releases" / "v0.3.5" / "npm-publication.md"


def relative_file_texts(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


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


def init_release_git_fixture(root: Path) -> None:
    subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def valid_timing_text(*, preflight_duration: int = 12) -> str:
    return (
        "schema_version: release-timing-v1\n"
        "release_tag: v0.3.5\n"
        "release_profile: docs/releases/profiles/v0.3.5.yaml\n"
        "created_at: 2026-06-29T00:00:00Z\n"
        "\n"
        "phases:\n"
        "  - id: prepare_release\n"
        "    command: python scripts/prepare-release.py v0.3.5\n"
        "    duration_seconds: 10\n"
        "    result: pass\n"
        "  - id: preflight\n"
        "    command: python scripts/release-preflight.py v0.3.5\n"
        f"    duration_seconds: {preflight_duration}\n"
        "    result: pass\n"
        "  - id: local_release_verify\n"
        "    command: bash scripts/release-verify.sh v0.3.5\n"
        "    duration_seconds: 180\n"
        "    result: pass\n"
        "  - id: ci_release_verify\n"
        "    command: bash scripts/release-verify.sh v0.3.5\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "  - id: publication_wait\n"
        "    command: external GitHub and npm publication wait\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "  - id: public_closeout\n"
        "    command: python scripts/close-release-publication.py v0.3.5\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "\n"
        "checks:\n"
        "  - id: adapter_distribution.regression\n"
        "    command: python tests/engineering/packaging/test-adapter-distribution.py\n"
        "    phase: local_release_verify\n"
        "    duration_seconds: 120\n"
        "    result: pass\n"
    )


def write_timing(root: Path, text: str) -> Path:
    timing = root / "docs" / "releases" / "v0.3.5" / "timing.yaml"
    timing.parent.mkdir(parents=True, exist_ok=True)
    timing.write_text(text, encoding="utf-8")
    return timing


def public_evidence_text(*, command_prefix: str = "npx", tree_hash: str = "sha256:codextree") -> str:
    return (
        "schema_version: release-public-evidence-v1\n"
        "release_tag: v0.3.5\n"
        "package: \"@xiongxianfei/rigorloop\"\n"
        "version: \"0.3.5\"\n"
        "github_release_url: \"https://github.com/xiongxianfei/rigorloop/releases/tag/v0.3.5\"\n"
        "npm_package_url: \"https://www.npmjs.com/package/@xiongxianfei/rigorloop/v/0.3.5\"\n"
        "npm_integrity: \"sha512-fixture\"\n"
        "npm_tarball: \"https://registry.npmjs.org/@xiongxianfei/rigorloop/-/rigorloop-0.3.5.tgz\"\n"
        "published_at: \"2026-06-29T00:00:00Z\"\n"
        "dist_tag_latest: \"0.3.5\"\n"
        "version_command: \"npx @xiongxianfei/rigorloop@0.3.5 version\"\n"
        "version_result: pass\n"
        "version_output_summary: \"0.3.5\"\n"
        "\n"
        "github_assets:\n"
        "  - target: codex\n"
        "    url: \"https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.5/rigorloop-adapter-codex-v0.3.5.zip\"\n"
        "    sha256: \"sha256:codexarchive\"\n"
        "  - target: claude\n"
        "    url: \"https://github.com/xiongxianfei/rigorloop/releases/download/v0.3.5/rigorloop-adapter-claude-v0.3.5.zip\"\n"
        "    sha256: \"sha256:claudearchive\"\n"
        "\n"
        "target_init_smoke:\n"
        "  - target: codex\n"
        f"    command: \"{command_prefix} @xiongxianfei/rigorloop@0.3.5 init codex\"\n"
        "    result: pass\n"
        "    output_summary: \"created codex adapter\"\n"
        f"    tree_hashes: \"{tree_hash}\"\n"
        "    file_counts: \"12\"\n"
        "  - target: claude\n"
        "    command: \"npx @xiongxianfei/rigorloop@0.3.5 init claude\"\n"
        "    result: pass\n"
        "    output_summary: \"created claude adapter\"\n"
        "    tree_hashes: \"sha256:claudetree\"\n"
        "    file_counts: \"13\"\n"
    )


def write_public_evidence(root: Path, text: str | None = None) -> Path:
    path = root / "tests" / "fixtures" / "release-transaction" / "public-evidence-v0.3.5.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text is not None else public_evidence_text(), encoding="utf-8")
    return path


def make_recorded_release(root):
    # Owned synthetic report: compatibility parsing never reads a completed release.
    make_prepared_release(root)
    result = close_release_publication("v0.3.5", root=root, provider=RecordingPublicEvidenceProvider())
    assert result.errors == (), result.errors
    profile = root / "docs/releases/profiles/v0.3.5.yaml"
    profile.write_text(profile.read_text().replace("- claude", "- claude\n  - opencode"))
    timing = root / "docs/releases/v0.3.5/timing.yaml"
    timing.write_text(valid_timing_text())
    published = root / "docs/releases/v0.3.5/npm-publication.md"
    text = published.read_text()
    row = text.split("  claude:\n", 1)[1].split("```", 1)[0]
    row = ("  opencode:\n" + row).replace("claude", "opencode")
    table = next(line for line in text.splitlines() if line.startswith("| claude |"))
    table = table.replace("claude", "opencode")
    text = text.replace("\n```\n\n| Target", "\n" + row + "```\n\n| Target") + table + "\n"
    # Root-qualified multi-root fields are a distinct retained report grammar.
    text = text.replace("sha256:provider-opencode-tree", ".opencode/skills=sha256:skills;.opencode/commands=sha256:commands")
    published.write_text(text)
    return profile


def profile_fixture(name: str) -> Path:
    return PROFILE_FIXTURES / name


def surface_inventory_fixture(name: str) -> Path:
    return FIXTURES / "surface-inventory" / name


def literal_audit_fixture(name: str) -> Path:
    return FIXTURES / "literal-audit" / name


def assert_errors_contain(case, errors, *needles):
    """Observe already-returned diagnostics; perform no validation or mutation."""
    case.assertTrue(any(all(needle in error for needle in needles) for error in errors), errors)


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
