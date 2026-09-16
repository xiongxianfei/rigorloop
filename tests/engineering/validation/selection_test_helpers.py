#!/usr/bin/env python3
"""Isolated test setup and independent selection expectations; no discovery registry."""

from __future__ import annotations

import json
import os
import re
import shutil
import signal
import shlex
import subprocess
import sys
import tempfile
import time
import unittest
from dataclasses import dataclass
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

SELECTOR = ROOT / "scripts" / "select-validation.py"
CI = ROOT / "scripts" / "ci.sh"
CHANGE_METADATA_TEST = ROOT / "tests" / "engineering" / "validation" / "test-change-metadata-validator.py"
README_VALIDATOR = ROOT / "scripts" / "validate-readme.py"

from lib.validation.validation_selection import (  # noqa: E402
    CHECK_CATALOG, MODE_CHECK_IDS,
    catalog_command,
    build_repository_preflight_context,
    SelectionRequest,
    normalize_path,
    select_validation,
)


ADAPTER_REGRESSION_COMMAND = (
    "python tests/engineering/packaging/test-adapter-distribution.py "
    "AdapterDistributionTests.test_adapter_generation_creates_independent_packages_and_thin_entrypoints "
    "AdapterDistributionTests.test_adapter_generation_drift_check_detects_stale_and_unexpected_files "
    "AdapterDistributionTests.test_validate_adapters_cli_rejects_retired_repository_output "
    "AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives "
    "AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root "
    "AdapterDistributionTests.test_current_candidate_metadata_matches_generated_route_only_archives AdapterDistributionTests.test_metadata_unknown_value_profile_fails_before_metadata_reads "
    "AdapterDistributionTests.test_distribution_archives_have_independent_complete_resource_inventory "
    "AdapterDistributionTests.test_distribution_generation_rejects_source_and_active_output_roots AdapterDistributionTests.test_distribution_generation_preserves_runtime_under_output_parent_and_symlinks AdapterDistributionTests.test_distribution_generated_skill_structure_is_validated_independently "
    "AdapterDistributionTests.test_validate_adapter_output_rejects_stale_mapped_resource_hashes "
    "AdapterDistributionTests.test_validate_adapter_output_rejects_missing_mapped_resource "
    "AdapterDistributionTests.test_validate_adapter_output_rejects_missing_or_malformed_canonical_skills"
)

# Independently named current mode populations: producer omissions must not
# shrink the catalog oracle. Ordering is part of the invocation contract.
EXPECTED_MODE_CHECK_IDS = {
    "broad-smoke": (
        "current_records.validate", "skills.validate", "skills.regression",
        "change_metadata.regression", "selector.regression", "validation_execution.regression",
        "adapters.full_regression", "broad_smoke.adapters.build_archives",
        "broad_smoke.adapters.validate_archives", "broad_smoke.review_artifacts.changed_roots",
    ),
    "main": (
        "boundary_first.validate", "skills.validate", "skills.regression",
        "change_metadata.regression", "release_transaction.regression",
        "readme.validate", "readme.vision_markers", "markdown_readability.regression",
        "guide_system.regression", "guide_system.validate", "rigorloop_cli.test",
        "governed_lifecycle_cli_wrapper.test", "adapters.full_regression",
        "main.adapters.build_archives", "main.adapters.validate_archives",
        "main.governed_lifecycle_cli.validate",
    ),
}


EXPECTED_CATALOG = {
    "current_records.validate": "python scripts/validate-governed-lifecycle-cli.py",
    "current_records.snapshot": "python scripts/validate-governed-lifecycle-cli.py --revision <head>",
    "release_evidence.validate": "python scripts/release_evidence.py <path>...",
    "validation_execution.regression": "python tests/engineering/validation/test-validation-execution.py",
    "record_store.schema": "node scripts/build-record-store-schema.mjs --check",
    "model.validate": "python scripts/validate-boundary-first.py --check --path docs/design/skill/workflow.md --path docs/design/cli/cli.md --path docs/design/cli/records.md",
    "record_retirement.regression": "node --test packages/rigorloop/test/record-retirement.test.js",
    "boundary_first.validate": "python scripts/validate-boundary-first.py --check",
    "boundary_first.reference_regression": "python tests/engineering/validation/test-boundary-first-reference.py",
    "boundary_first.regression": "python tests/engineering/validation/test-boundary-first-validation.py",
    "skills.validate": "python scripts/validate-skills.py",
    "skills.regression": "python tests/skill/test-skill-validator.py",
    "adapters.regression": ADAPTER_REGRESSION_COMMAND,
    "adapters.drift": "python tests/engineering/packaging/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives",
    "adapters.validate": "python tests/engineering/packaging/test-adapter-distribution.py AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root",
    "change_metadata.regression": "python tests/engineering/validation/test-change-metadata-validator.py",
    "change_metadata.validate": "python scripts/validate-change-metadata.py <change.json>...",
    "release.validate": "python scripts/validate-release.py --recorded-source-auto --version <version>",
    "release_transaction.regression": "python tests/engineering/release/test-release-transaction.py",
    "readme.validate": "python scripts/validate-readme.py README.md",
    "readme.vision_markers": "python scripts/validate-readme.py README.md --vision-markers",
    "markdown_readability.validate": "python scripts/validate-markdown-readability.py <path>... [--changed-section PATH:START:END ...]",
    "markdown_readability.regression": "python tests/engineering/validation/test-markdown-readability-validator.py",
    "guide_system.regression": "python tests/engineering/validation/test-guide-system-validator.py",
    "guide_system.validate": "python scripts/validate-guide-system.py",
    "documentation_prose.enforce": "python scripts/validate-documentation-prose.py --mode enforce --path <path>...",
    "documentation_prose.audit": "python scripts/validate-documentation-prose.py --mode audit --path <path>...",
    "documentation_prose.regression": "python tests/engineering/validation/test-documentation-prose-validator.py",
    "selector.regression": "python tests/engineering/validation/test-select-validation.py",
    "broad_smoke.repo": "bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped",
    "rigorloop_cli.test": "npm test --prefix packages/rigorloop",
    "governed_lifecycle_cli_wrapper.test": "python tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
    "npm_package_publication.test": "python tests/engineering/packaging/test-npm-package-publication.py",
}

CHANGE_METADATA_PASSING_TEST = "ExplicitRecordingMetadataTests.test_explicit_recording_metadata_accepts_structure_without_stage_eligibility"
CHANGE_METADATA_FAILING_TEST = "ChangeMetadataValidatorFixtureTests.test_output_contract_fixture_failure"


def run_selector(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SELECTOR), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def run_ci(
    *args: str,
    env: dict[str, str] | None = None,
    script: Path = CI,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[str]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    return subprocess.run(
        ["bash", str(script), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=run_env,
    )


def run_ci_bytes(
    *args: str,
    env: dict[str, str] | None = None,
    script: Path = CI,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[bytes]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    return subprocess.run(
        ["bash", str(script), *args],
        cwd=cwd,
        capture_output=True,
        env=run_env,
    )


def run_change_metadata_test(
    *args: str,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    return subprocess.run(
        [sys.executable, str(CHANGE_METADATA_TEST), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=run_env,
    )


def parse_stdout(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - failure helper
        raise AssertionError(f"selector stdout was not JSON:\n{result.stdout}") from exc


def selected_ids(result: dict[str, object]) -> set[str]:
    return {check["id"] for check in result["selected_checks"]}  # type: ignore[index]


def allocated_workers(requested: int) -> int:
    """Nested proof uses the outer invocation's actual allocation."""
    return min(requested, int(os.environ.get('RIGORLOOP_VALIDATION_WORKERS', requested)))


class SelectionFixtures:
    def recording_repo(self):
        repo = self.make_git_repo()
        shutil.copyfile(ROOT / ".gitignore", repo / ".gitignore")
        (repo / "docs/changes").mkdir(parents=True)
        templates = json.loads((ROOT / "tests/fixtures/rigorloop-records-v3/records.json").read_text())
        change = templates["change"]
        records = {"reviews/design-review.json": ("review", templates["review"]),
                   "evidence.json": ("evidence", templates["evidence"]),
                   "material-decisions.json": ("decisions", templates["decisions"]),
                   "verify-report.json": ("verify", templates["verify"])}
        prefix = "docs/changes/example/"
        change["records"] = [{"path": prefix + name, "kind": kind} for name, (kind, _) in records.items()]
        change["applicability"] = [{"path": entry["path"], "value": "current",
                                    "actor": {"id": "fixture", "role": "support"},
                                    "reason": "Structural selector fixture, not an actual approval"}
                                   for entry in change["records"]]
        writes = [{"path": prefix + "change.json", "expected_identity": None,
                   "content": json.dumps(change) + "\n"}]
        for name, (kind, record) in records.items():
            content = json.dumps(record) + "\n"
            writes.append({"path": prefix + name, "expected_identity": None, "content": content})
        request = {"schema_version": 2, "contract": "rigorloop-records-v3", "change_id": "example",
                   "expected_revision": None, "reads": [], "writes": writes}
        # Supported synthetic fixture.
        for write in request["writes"]:
            destination = repo / write["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(write["content"])
        return repo, tuple(write["path"] for write in writes)


    def supporting_subject_repo(self, path="docs/changes/example/evidence/notes.md"):
        repo, _ = self.recording_repo()
        evidence = repo / "docs/changes/example/evidence.json"
        value = json.loads(evidence.read_text())
        value["checks"][0]["subjects"].append({"path": path, "identity": "sha256:" + "a" * 64})
        evidence.write_text(json.dumps(value) + "\n")
        subject = repo / path
        subject.parent.mkdir(parents=True, exist_ok=True)
        subject.write_text("# Supporting observation\n")
        return repo, path, evidence


    def addCleanupTree(self, path: Path) -> None:
        self.addCleanup(lambda: shutil.rmtree(path, ignore_errors=True))


    def make_git_repo(self) -> Path:
        repo = Path(tempfile.mkdtemp(prefix="validation-selection-git-"))
        self.addCleanupTree(repo)
        subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "config", "user.email", "tester@example.com"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture Tester"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        (repo / "skills" / "workflow").mkdir(parents=True)
        (repo / "skills" / "workflow" / "SKILL.md").write_text("# Workflow\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "baseline"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        return repo


    def git_output(self, repo: Path, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()


    def write_selector_fixture(self, payload: object | str) -> Path:
        fixture = Path(tempfile.mkdtemp(prefix="validation-selection-fixture-")) / "selector.json"
        self.addCleanupTree(fixture.parent)
        if isinstance(payload, str):
            fixture.write_text(payload, encoding="utf-8")
        else:
            fixture.write_text(json.dumps(payload), encoding="utf-8")
        return fixture


    def minimal_selector_payload(
        self,
        *,
        mode: str = "explicit",
        status: str = "ok",
        selected_checks: list[dict[str, object]] | None = None,
        blocking_results: list[dict[str, str]] | None = None,
    ) -> dict[str, object]:
        return {
            "mode": mode,
            "status": status,
            "changed_paths": [],
            "classified_paths": [],
            "unclassified_paths": [],
            "selected_checks": selected_checks or [],
            "affected_roots": [],
            "broad_smoke_required": False,
            "broad_smoke": {"required": False, "sources": []},
            "blocking_results": blocking_results or [],
            "preflight_results": [],
            "rationale": [],
        }


    def make_ci_workspace(self) -> Path:
        workspace = Path(tempfile.mkdtemp(prefix="validation-selection-ci-workspace-"))
        self.addCleanupTree(workspace)
        (workspace / "scripts").mkdir()
        shutil.copy2(CI, workspace / "scripts" / "ci.sh")
        shutil.copytree(ROOT / "scripts/lib", workspace / "scripts/lib", ignore=shutil.ignore_patterns("__pycache__"))
        # These fixtures provide controlled command bodies, not unittest suites.
        # Keep that distinction explicit in the fixture's trusted catalog.
        with (workspace/'scripts/lib/validation/validation_selection.py').open('a') as catalog:
            catalog.write("\nfor key in (*_CASE_ASSESSMENTS, *_NODE_ASSESSMENTS):\n"
                          " entry = CHECK_CATALOG[key]\n"
                          " CHECK_CATALOG[key] = replace(entry,constraints=replace(entry.constraints,unit='command',basis=command_basis(entry.command_template,'command')))\n"
                          "for key in COVERAGE_BASES:\n"
                          " COVERAGE_BASES[key] = (CHECK_CATALOG[key].constraints.basis, 'command')\n")
        return workspace


    def make_broad_smoke_workspace(
        self,
        *,
        failing_child: str | None = None,
        failing_children: set[str] | None = None,
        active_counter_children: set[str] | None = None,
        child_bodies: dict[str, str] | None = None,
        sleep_seconds: float = 0.2,
    ) -> Path:
        workspace = self.make_ci_workspace()
        all_failing_children = set(failing_children or set())
        if failing_child is not None:
            all_failing_children.add(failing_child)
        active_counter_children = set(active_counter_children or set())
        child_bodies = dict(child_bodies or {})
        child_scripts = [
            "tests/engineering/validation/test-select-validation.py",
            "tests/engineering/validation/test-validation-execution.py",
            "scripts/validate-skills.py",
            "tests/skill/test-skill-validator.py",
            "tests/engineering/packaging/test-adapter-distribution.py",
            "scripts/build-adapters.py",
            "scripts/validate-adapters.py",
            "tests/engineering/validation/test-change-metadata-validator.py",
            "tests/engineering/validation/test-governed-lifecycle-cli-validator.py",
            "scripts/validate-governed-lifecycle-cli.py",
            "scripts/validate-change-metadata.py",
        ]
        for relative_path in child_scripts:
            name = Path(relative_path).name
            exit_code = 7 if relative_path in all_failing_children else 0
            if relative_path in child_bodies:
                self.write_fake_script(workspace, relative_path, child_bodies[relative_path])
                continue
            if relative_path in active_counter_children:
                self.write_active_counter_script(
                    workspace,
                    relative_path,
                    name,
                    sleep_seconds=sleep_seconds,
                    exit_code=exit_code,
                )
                continue
            self.write_fake_script(
                workspace,
                relative_path,
                f"""
import sys

print("{name} STDOUT marker", flush=True)
print("{name} STDERR marker", file=sys.stderr)
raise SystemExit({exit_code})
""".lstrip(),
            )

        change_json = workspace / "docs" / "changes" / "example" / "change.json"
        change_json.parent.mkdir(parents=True)
        change_json.write_text('{"change_id":"example"}\n', encoding="utf-8")
        subprocess.run(["git", "init"], cwd=workspace, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "config", "user.email", "tester@example.com"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture Tester"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(["git", "add", "."], cwd=workspace, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "baseline"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )
        change_json.write_text('{"change_id":"example","fixture":"changed"}\n', encoding="utf-8")
        return workspace


    def write_fake_script(self, workspace: Path, relative_path: str, body: str) -> Path:
        script = workspace / relative_path
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text(body, encoding="utf-8")
        return script


    def write_active_counter_script(
        self,
        workspace: Path,
        relative_path: str,
        check_name: str,
        *,
        sleep_seconds: float = 0.2,
        exit_code: int = 0,
    ) -> Path:
        return self.write_fake_script(
            workspace,
            relative_path,
            f"""
import fcntl
import os
import time
from pathlib import Path

active_dir = Path(os.environ["ACTIVE_DIR"])
active_dir.mkdir(parents=True, exist_ok=True)
name = "{check_name}"
lock_path = active_dir / "lock"
active_path = active_dir / f"active-{{name}}"
max_path = active_dir / "max-active.txt"
events_path = active_dir / "events.txt"

with lock_path.open("a+", encoding="utf-8") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    active_path.write_text("active", encoding="utf-8")
    active_count = len(list(active_dir.glob("active-*")))
    previous_max = int(max_path.read_text(encoding="utf-8")) if max_path.exists() else 0
    if active_count > previous_max:
        max_path.write_text(str(active_count), encoding="utf-8")
    with events_path.open("a", encoding="utf-8") as events:
        events.write(f"{{name}} start {{active_count}}\\n")
    fcntl.flock(lock, fcntl.LOCK_UN)

expected_overlap = int(os.environ.get("EXPECTED_ACTIVE_OVERLAP", "1"))
if expected_overlap > 1:
    deadline = time.monotonic() + 10
    while True:
        with lock_path.open("a+", encoding="utf-8") as lock:
            fcntl.flock(lock, fcntl.LOCK_SH)
            observed = int(max_path.read_text(encoding="utf-8"))
            fcntl.flock(lock, fcntl.LOCK_UN)
        if observed >= expected_overlap:
            break
        if time.monotonic() > deadline:
            raise SystemExit("active-child rendezvous did not complete")
        time.sleep(.01)
else:
    time.sleep({sleep_seconds!r})

with lock_path.open("a+", encoding="utf-8") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    active_path.unlink(missing_ok=True)
    with events_path.open("a", encoding="utf-8") as events:
        events.write(f"{{name}} end\\n")
    fcntl.flock(lock, fcntl.LOCK_UN)

print(f"{{name}} done")
raise SystemExit({exit_code})
""".lstrip(),
        )


    def read_max_active(self, active_dir: Path) -> int:
        max_path = active_dir / "max-active.txt"
        if not max_path.exists():
            return 0
        return int(max_path.read_text(encoding="utf-8"))


    def selected_check(self, check_id: str, command: str, **extra: object) -> dict[str, object]:
        check: dict[str, object] = {
            "id": check_id,
            "command": command,
            "reason": f"{check_id} fixture",
        }
        check.update(extra)
        return check


    def run_workspace_ci(
        self,
        workspace: Path,
        fixture: Path,
        *args: str,
        text: bool = True,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
        run_env = {"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)}
        if env:
            run_env.update(env)
        if text:
            return run_ci(
                *args,
                env=run_env,
                script=workspace / "scripts" / "ci.sh",
                cwd=workspace,
            )
        return run_ci_bytes(
            *args,
            env=run_env,
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )


    def select(self, paths: list[str], *, mode: str = "explicit", **kwargs):
        kwargs.setdefault("preflight_context", self.root_preflight_context)
        return select_validation(SelectionRequest(mode=mode, paths=tuple(paths), repo_root=ROOT, **kwargs))
