#!/usr/bin/env python3
"""Fixture-driven tests for validation selection."""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / "scripts" / "select-validation.py"
CI = ROOT / "scripts" / "ci.sh"
README_VALIDATOR = ROOT / "scripts" / "validate-readme.py"
sys.path.insert(0, str(ROOT / "scripts"))

from validation_selection import (  # noqa: E402
    CHECK_CATALOG,
    SelectionRequest,
    normalize_path,
    select_validation,
)


EXPECTED_CATALOG = {
    "skills.validate": "python scripts/validate-skills.py",
    "skills.regression": "python scripts/test-skill-validator.py",
    "skills.drift": "python scripts/build-skills.py --check",
    "adapters.regression": "python scripts/test-adapter-distribution.py",
    "adapters.drift": "python scripts/build-adapters.py --version <adapter-version> --check",
    "adapters.validate": "python scripts/validate-adapters.py --version <adapter-version>",
    "review_artifacts.regression": "python scripts/test-review-artifact-validator.py",
    "review_artifacts.validate": "python scripts/validate-review-artifacts.py <change-root>...",
    "artifact_lifecycle.regression": "python scripts/test-artifact-lifecycle-validator.py",
    "artifact_lifecycle.validate": "python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <path>...",
    "change_metadata.regression": "python scripts/test-change-metadata-validator.py",
    "change_metadata.validate": "python scripts/validate-change-metadata.py <change-yaml>...",
    "release.validate": "python scripts/validate-release.py --version <version>",
    "readme.validate": "python scripts/validate-readme.py README.md",
    "readme.vision_markers": "python scripts/validate-readme.py README.md --vision-markers",
    "selector.regression": "python scripts/test-select-validation.py",
    "broad_smoke.repo": "bash scripts/ci.sh --mode broad-smoke",
}


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


def parse_stdout(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - failure helper
        raise AssertionError(f"selector stdout was not JSON:\n{result.stdout}") from exc


def selected_ids(result: dict[str, object]) -> set[str]:
    return {check["id"] for check in result["selected_checks"]}  # type: ignore[index]


class ValidationSelectionTests(unittest.TestCase):
    maxDiff = None

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
            "rationale": [],
        }

    def make_ci_workspace(self) -> Path:
        workspace = Path(tempfile.mkdtemp(prefix="validation-selection-ci-workspace-"))
        self.addCleanupTree(workspace)
        (workspace / "scripts").mkdir()
        shutil.copy2(CI, workspace / "scripts" / "ci.sh")
        shutil.copy2(ROOT / "scripts" / "validation_selection.py", workspace / "scripts" / "validation_selection.py")
        return workspace

    def write_fake_script(self, workspace: Path, relative_path: str, body: str) -> Path:
        script = workspace / relative_path
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text(body, encoding="utf-8")
        return script

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
        return select_validation(SelectionRequest(mode=mode, paths=tuple(paths), repo_root=ROOT, **kwargs))

    def test_catalog_matches_v1_contract(self) -> None:
        self.assertEqual(set(CHECK_CATALOG), set(EXPECTED_CATALOG))
        for check_id, command in EXPECTED_CATALOG.items():
            with self.subTest(check_id=check_id):
                self.assertEqual(CHECK_CATALOG[check_id].command_template, command)
                self.assertTrue(CHECK_CATALOG[check_id].category)

    def test_catalog_records_initial_parallel_safe_allowlist(self) -> None:
        from validation_selection import is_parallel_safe_check

        expected_parallel_safe = {
            "adapters.regression",
            "artifact_lifecycle.regression",
            "change_metadata.regression",
            "review_artifacts.regression",
            "selector.regression",
            "skills.regression",
        }

        self.assertEqual(
            {check_id for check_id in CHECK_CATALOG if is_parallel_safe_check(check_id)},
            expected_parallel_safe,
        )
        for check_id, entry in CHECK_CATALOG.items():
            with self.subTest(check_id=check_id):
                self.assertIsInstance(entry.parallel_safe, bool)
                self.assertEqual(entry.parallel_safe, check_id in expected_parallel_safe)

    def test_cli_outputs_json_for_classified_skill_path(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "skills/code-review/SKILL.md")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["mode"], "explicit")
        self.assertEqual(payload["status"], "ok")
        for field in (
            "changed_paths",
            "classified_paths",
            "unclassified_paths",
            "selected_checks",
            "affected_roots",
            "broad_smoke_required",
            "blocking_results",
            "rationale",
        ):
            self.assertIn(field, payload)
        self.assertIn(
            {"path": "skills/code-review/SKILL.md", "category": "skills"},
            payload["classified_paths"],
        )
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"skills.validate", "skills.regression", "skills.drift"}.issubset(selected_ids(payload)))
        self.assertIn("adapters.drift", selected_ids(payload))

    def test_missing_mode_specific_inputs_return_json_error(self) -> None:
        result = run_selector("--mode", "pr", "--base", "HEAD~1")
        self.assertEqual(result.returncode, 4)
        payload = parse_stdout(result)
        self.assertEqual(payload["status"], "error")
        self.assertIn("invalid-invocation", {item["code"] for item in payload["blocking_results"]})

    def test_unclassified_path_blocks_without_fail_open(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "experimental/runtime/example.txt")
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["unclassified_paths"], ["experimental/runtime/example.txt"])
        self.assertIn("unclassified-path", {item["code"] for item in payload["blocking_results"]})
        self.assertNotEqual(payload["status"], "ok")

    def test_mixed_classified_and_unclassified_paths_block_partial_execution(self) -> None:
        result = run_selector(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            "--path",
            "experimental/runtime/example.txt",
        )
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertIn("skills.validate", selected_ids(payload))
        self.assertEqual(payload["unclassified_paths"], ["experimental/runtime/example.txt"])

    def test_change_metadata_paths_select_multi_file_validator(self) -> None:
        result = self.select(
            [
                "docs/changes/2026-04-25-a/change.yaml",
                "docs/changes/2026-04-25-b/change.yaml",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("change_metadata.validate", selected_ids(payload))
        self.assertIn("change_metadata.regression", selected_ids(payload))
        self.assertEqual(
            payload["affected_roots"],
            ["docs/changes/2026-04-25-a/", "docs/changes/2026-04-25-b/"],
        )
        validate_check = next(check for check in payload["selected_checks"] if check["id"] == "change_metadata.validate")
        self.assertEqual(
            validate_check["command"],
            "python scripts/validate-change-metadata.py docs/changes/2026-04-25-a/change.yaml docs/changes/2026-04-25-b/change.yaml",
        )

    def test_review_lifecycle_and_release_paths_select_scoped_validators(self) -> None:
        result = self.select(
            [
                "docs/changes/2026-04-25-example/review-resolution.md",
                "specs/test-layering-and-change-scoped-validation.test.md",
                "docs/releases/v0.1.1/release.yaml",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("review_artifacts.validate", selected_ids(payload))
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertIn("release.validate", selected_ids(payload))
        self.assertIn("docs/changes/2026-04-25-example/", payload["affected_roots"])
        release_check = next(check for check in payload["selected_checks"] if check["id"] == "release.validate")
        self.assertEqual(release_check["command"], "python scripts/validate-release.py --version v0.1.1")

    def test_release_path_without_version_directory_blocks(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "docs/releases/release-notes.md")
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertIn({"path": "docs/releases/release-notes.md", "category": "release"}, payload["classified_paths"])
        self.assertIn(
            "release-version-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertNotIn("release.validate", selected_ids(payload))

    def test_first_slice_representative_categories_route_or_block_safely(self) -> None:
        cases = [
            {
                "path": "dist/adapters/opencode/AGENTS.md",
                "category": "generated-adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": ".codex/skills/code-review/SKILL.md",
                "category": "generated-skills",
                "status": "ok",
                "checks": {"skills.drift"},
            },
            {
                "path": "docs/workflows.md",
                "category": "workflow-guidance",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": "CONSTITUTION.md",
                "category": "governance",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": "schemas/change.schema.json",
                "category": "schemas",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "templates/example.md",
                "category": "templates",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": "scripts/build-adapters.py",
                "category": "adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": "scripts/test-adapter-distribution.py",
                "category": "adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": "scripts/validate-skills.py",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression"},
            },
            {
                "path": "scripts/validate-release.py",
                "category": "release-script",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "scripts/ci.sh",
                "category": "ci-wrapper",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": ".github/workflows/ci.yml",
                "category": "ci-workflow",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": "docs/plan.md",
                "category": "plan-index",
                "status": "blocked",
                "blocking_code": "manual-routing-required",
            },
            {
                "path": "docs/changes/2026-04-25-example/explain-change.md",
                "category": "change-local-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/architecture.md",
                "category": "change-local-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/diagrams/context.mmd",
                "category": "change-local-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/architecture/system/diagrams/context.mmd",
                "category": "architecture-diagram",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "tests/fixtures/artifact-lifecycle/valid-canonical-arc42-architecture/docs/architecture/system/architecture.md",
                "category": "artifact-lifecycle-fixtures",
                "status": "ok",
                "checks": {"artifact_lifecycle.regression"},
            },
        ]

        for case in cases:
            with self.subTest(path=case["path"]):
                result = self.select([case["path"]])
                payload = result.to_json_dict()

                self.assertEqual(result.status, case["status"])
                self.assertIn({"path": case["path"], "category": case["category"]}, payload["classified_paths"])
                if case.get("checks"):
                    self.assertTrue(case["checks"].issubset(selected_ids(payload)))
                if case.get("blocking_code"):
                    self.assertIn(
                        case["blocking_code"],
                        {item["code"] for item in payload["blocking_results"]},
                    )

    def test_learn_artifact_paths_are_known_lightweight_paths(self) -> None:
        paths = [
            "docs/learn/README.md",
            "docs/learn/sessions/2026-05-04-example.md",
            "docs/learn/topics/verification.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        for path in paths:
            with self.subTest(path=path):
                self.assertIn({"path": path, "category": "learn-artifact"}, payload["classified_paths"])

        self.assertNotIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertEqual(payload["selected_checks"], [])

    def test_selector_and_validation_script_paths_select_regressions(self) -> None:
        result = self.select(["scripts/select-validation.py", "scripts/validate-review-artifacts.py"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertIn("review_artifacts.regression", selected_ids(payload))

    def test_governance_paths_select_deterministic_proof_instead_of_empty_ok(self) -> None:
        result = self.select(["AGENTS.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "AGENTS.md", "category": "governance"}, payload["classified_paths"])
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertFalse(payload["blocking_results"])

    def test_readme_path_selects_lightweight_readme_validation(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-no-markers-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text("# Example\n\nNo generated vision marker block.\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertIn("readme.validate", selected_ids(payload))
        self.assertNotIn("readme.vision_markers", selected_ids(payload))
        self.assertFalse(payload["blocking_results"])

    def test_readme_marker_validation_is_selected_for_marker_block_or_vision_scope(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-markers-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )

        marker_result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        marker_payload = marker_result.to_json_dict()

        self.assertEqual(marker_result.status, "ok")
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(marker_payload)))

        scoped_result = self.select(["README.md", "skills/vision/SKILL.md"])
        scoped_payload = scoped_result.to_json_dict()

        self.assertEqual(scoped_result.status, "ok")
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(scoped_payload)))
        self.assertFalse(scoped_payload["unclassified_paths"])
        self.assertFalse(scoped_payload["blocking_results"])

    def test_root_vision_path_selects_marker_validation_without_unclassified_block(self) -> None:
        for path in ("vision.md", "VISION.md"):
            with self.subTest(path=path):
                result = self.select([path])
                payload = result.to_json_dict()

                self.assertEqual(result.status, "ok")
                self.assertIn({"path": path, "category": "vision"}, payload["classified_paths"])
                self.assertEqual(payload["unclassified_paths"], [])
                self.assertIn("readme.vision_markers", selected_ids(payload))
                self.assertFalse(payload["blocking_results"])

    def test_root_vision_path_conflict_blocks_validation(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-vision-conflict-"))
        self.addCleanupTree(temp_root)
        (temp_root / "vision.md").write_text("# Legacy Vision\n", encoding="utf-8")
        (temp_root / "VISION.md").write_text("# Canonical Vision\n", encoding="utf-8")

        for path in ("vision.md", "VISION.md"):
            with self.subTest(path=path):
                result = select_validation(
                    SelectionRequest(mode="explicit", paths=(path,), repo_root=temp_root)
                )
                payload = result.to_json_dict()

                self.assertEqual(result.status, "blocked")
                self.assertIn({"path": path, "category": "vision"}, payload["classified_paths"])
                self.assertEqual(payload["unclassified_paths"], [])
                self.assertIn("readme.vision_markers", selected_ids(payload))
                self.assertIn("vision-path-conflict", {item["code"] for item in payload["blocking_results"]})

    def test_root_vision_path_conflict_blocks_unrelated_changed_path(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-vision-conflict-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )
        (temp_root / "vision.md").write_text("# Legacy Vision\n", encoding="utf-8")
        (temp_root / "VISION.md").write_text("# Canonical Vision\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "blocked")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
        self.assertIn("vision-path-conflict", {item["code"] for item in payload["blocking_results"]})

    def test_pr_handoff_surfaces_select_deterministic_checks(self) -> None:
        result = self.select(
            [
                ".github/workflows/ci.yml",
                "docs/workflows.md",
                "docs/plan.md",
                "docs/changes/2026-04-25-example/explain-change.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["unclassified_paths"])
        self.assertFalse(payload["blocking_results"])
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))

    def test_architecture_support_paths_route_without_manual_blocks(self) -> None:
        result = self.select(
            [
                "docs/architecture/system/diagrams/context.mmd",
                "docs/architecture/system/diagrams/container.mmd",
                "docs/changes/2026-04-25-example/architecture.md",
                "docs/changes/2026-04-25-example/diagrams/context.mmd",
                "tests/fixtures/artifact-lifecycle/valid-canonical-arc42-architecture/docs/architecture/system/architecture.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["unclassified_paths"])
        self.assertFalse(payload["blocking_results"])
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertIn("artifact_lifecycle.regression", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertIn("docs/architecture/system/architecture.md", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/change.yaml", lifecycle_check["paths"])

    def test_workflow_refactor_surface_set_selects_expected_checks(self) -> None:
        paths = [
            "CONSTITUTION.md",
            "AGENTS.md",
            "README.md",
            "docs/workflows.md",
            "docs/plan.md",
            "docs/plans/2026-05-03-workflow-refactor.md",
            "docs/proposals/2026-05-01-workflow-refactor.md",
            "specs/rigorloop-workflow.md",
            "specs/rigorloop-workflow.test.md",
            "skills/workflow/SKILL.md",
            ".codex/skills/workflow/SKILL.md",
            "dist/adapters/codex/.agents/skills/workflow/SKILL.md",
            "scripts/test-select-validation.py",
            "scripts/test-artifact-lifecycle-validator.py",
            "scripts/test-skill-validator.py",
            "docs/changes/2026-05-03-workflow-refactor/change.yaml",
            "docs/changes/2026-05-03-workflow-refactor/explain-change.md",
            "docs/changes/2026-05-03-workflow-refactor/review-log.md",
            "docs/changes/2026-05-03-workflow-refactor/review-resolution.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        expected_categories = {
            "CONSTITUTION.md": "governance",
            "AGENTS.md": "governance",
            "README.md": "readme",
            "docs/workflows.md": "workflow-guidance",
            "docs/plan.md": "plan-index",
            "docs/plans/2026-05-03-workflow-refactor.md": "lifecycle",
            "docs/proposals/2026-05-01-workflow-refactor.md": "lifecycle",
            "specs/rigorloop-workflow.md": "lifecycle",
            "specs/rigorloop-workflow.test.md": "lifecycle",
            "skills/workflow/SKILL.md": "skills",
            ".codex/skills/workflow/SKILL.md": "generated-skills",
            "dist/adapters/codex/.agents/skills/workflow/SKILL.md": "generated-adapters",
            "scripts/test-select-validation.py": "selector",
            "scripts/test-artifact-lifecycle-validator.py": "validator-artifact-lifecycle",
            "scripts/test-skill-validator.py": "validator-skills",
            "docs/changes/2026-05-03-workflow-refactor/change.yaml": "change-metadata",
            "docs/changes/2026-05-03-workflow-refactor/explain-change.md": "change-local-lifecycle",
            "docs/changes/2026-05-03-workflow-refactor/review-log.md": "review-artifacts",
            "docs/changes/2026-05-03-workflow-refactor/review-resolution.md": "review-artifacts",
        }
        for path, category in expected_categories.items():
            with self.subTest(path=path):
                self.assertIn({"path": path, "category": category}, payload["classified_paths"])

        self.assertTrue(
            {
                "skills.validate",
                "skills.regression",
                "skills.drift",
                "adapters.regression",
                "adapters.drift",
                "adapters.validate",
                "review_artifacts.validate",
                "artifact_lifecycle.regression",
                "artifact_lifecycle.validate",
                "change_metadata.regression",
                "change_metadata.validate",
                "readme.validate",
                "readme.vision_markers",
                "selector.regression",
            }.issubset(selected_ids(payload))
        )
        self.assertFalse(payload["broad_smoke_required"])
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertIn("docs/plan.md", lifecycle_check["paths"])
        self.assertIn("docs/plans/2026-05-03-workflow-refactor.md", lifecycle_check["paths"])
        self.assertIn("docs/proposals/2026-05-01-workflow-refactor.md", lifecycle_check["paths"])
        self.assertIn("specs/rigorloop-workflow.md", lifecycle_check["paths"])
        self.assertIn("specs/rigorloop-workflow.test.md", lifecycle_check["paths"])

    def test_broad_smoke_sources_are_attributed(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-broad-smoke-"))
        self.addCleanupTree(temp_root)
        plan_path = temp_root / "docs" / "plans" / "active.md"
        plan_path.parent.mkdir(parents=True)
        plan_path.write_text("broad_smoke_required: true\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("skills/code-review/SKILL.md",),
                broad_smoke=True,
                trigger_context_paths=(str(plan_path),),
                repo_root=temp_root,
            )
        )
        payload = result.to_json_dict()

        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        sources = payload["broad_smoke"]["sources"]
        self.assertIn({"type": "explicit_flag", "value": "--broad-smoke"}, sources)
        self.assertIn({"type": "active_plan", "path": "docs/plans/active.md"}, sources)

    def test_broad_smoke_sources_include_test_spec_and_review_resolution_context(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-broad-smoke-"))
        self.addCleanupTree(temp_root)
        context_files = {
            "docs/plans/active.md": "broad_smoke_required: true\n",
            "specs/example.test.md": "- broad smoke required before final verify\n",
            "docs/changes/example/review-resolution.md": "- broad smoke required by review closeout\n",
        }
        for relative_path, content in context_files.items():
            target = temp_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("skills/code-review/SKILL.md",),
                trigger_context_paths=tuple(context_files),
                repo_root=temp_root,
            )
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        sources = payload["broad_smoke"]["sources"]
        self.assertIn({"type": "active_plan", "path": "docs/plans/active.md"}, sources)
        self.assertIn({"type": "test_spec", "path": "specs/example.test.md"}, sources)
        self.assertIn(
            {"type": "review_resolution", "path": "docs/changes/example/review-resolution.md"},
            sources,
        )

    def test_release_mode_selects_release_validation_and_broad_smoke(self) -> None:
        result = run_selector("--mode", "release", "--release-version", "v0.1.1")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertIn("release.validate", selected_ids(payload))
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn({"type": "mode", "value": "release"}, payload["broad_smoke"]["sources"])
        self.assertIn(
            {"type": "release_metadata", "path": "docs/releases/v0.1.1/release.yaml"},
            payload["broad_smoke"]["sources"],
        )

    def test_valid_pr_and_main_modes_use_git_range(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "skills" / "workflow" / "SKILL.md").write_text("# Workflow\n\nChanged\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "change skill"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        pr_result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(pr_result.returncode, 0, msg=pr_result.stderr)
        pr_payload = parse_stdout(pr_result)
        self.assertEqual(pr_payload["mode"], "pr")
        self.assertEqual(pr_payload["changed_paths"], ["skills/workflow/SKILL.md"])
        self.assertIn("skills.validate", selected_ids(pr_payload))
        self.assertFalse(pr_payload["broad_smoke_required"])

        main_result = run_selector("--mode", "main", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(main_result.returncode, 0, msg=main_result.stderr)
        main_payload = parse_stdout(main_result)
        self.assertEqual(main_payload["mode"], "main")
        self.assertEqual(main_payload["changed_paths"], ["skills/workflow/SKILL.md"])
        self.assertIn("skills.validate", selected_ids(main_payload))
        self.assertIn("broad_smoke.repo", selected_ids(main_payload))
        self.assertTrue(main_payload["broad_smoke_required"])
        self.assertIn({"type": "mode", "value": "main"}, main_payload["broad_smoke"]["sources"])

    def test_pr_mode_routes_adapter_distribution_test_script_to_adapter_checks(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "scripts").mkdir()
        adapter_test = repo / "scripts" / "test-adapter-distribution.py"
        adapter_test.write_text("print('adapter tests')\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add adapter test"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["changed_paths"], ["scripts/test-adapter-distribution.py"])
        self.assertIn(
            {"path": "scripts/test-adapter-distribution.py", "category": "adapters"},
            payload["classified_paths"],
        )
        self.assertTrue(
            {"adapters.regression", "adapters.drift", "adapters.validate"}.issubset(selected_ids(payload))
        )
        self.assertFalse(payload["blocking_results"])

    def test_pr_mode_routes_readme_without_unclassified_block(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "README.md").write_text("# Example\n\nVision ownership wording.\n", encoding="utf-8")
        (repo / "skills" / "vision").mkdir(parents=True)
        (repo / "skills" / "vision" / "SKILL.md").write_text("# Vision\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add readme and vision skill"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
        self.assertFalse(payload["blocking_results"])

    def test_pr_mode_routes_root_vision_without_unclassified_block(self) -> None:
        for path in ("vision.md", "VISION.md"):
            with self.subTest(path=path):
                repo = self.make_git_repo()
                base = self.git_output(repo, "rev-parse", "HEAD")
                (repo / "README.md").write_text(
                    "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
                    encoding="utf-8",
                )
                (repo / path).write_text("# Project Vision\n\n## Pitch\n\nExample vision.\n", encoding="utf-8")
                subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
                subprocess.run(
                    ["git", "commit", "-m", "add root vision"],
                    cwd=repo,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                head = self.git_output(repo, "rev-parse", "HEAD")

                result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
                self.assertEqual(result.returncode, 0, msg=result.stderr)
                payload = parse_stdout(result)

                self.assertEqual(payload["status"], "ok")
                self.assertIn({"path": path, "category": "vision"}, payload["classified_paths"])
                self.assertEqual(payload["unclassified_paths"], [])
                self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
                self.assertFalse(payload["blocking_results"])

    def test_pr_mode_blocks_reintroduced_legacy_vision_without_unclassified_block(self) -> None:
        repo = self.make_git_repo()
        (repo / "VISION.md").write_text("# Project Vision\n\n## Pitch\n\nExample vision.\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add canonical vision"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "vision.md").write_text("# Legacy Vision\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "reintroduce legacy vision"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 2, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertIn({"path": "vision.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertIn("readme.vision_markers", selected_ids(payload))
        self.assertIn("vision-path-conflict", {item["code"] for item in payload["blocking_results"]})

    def test_readme_validator_accepts_absent_or_valid_standalone_marker_block(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-validator-"))
        self.addCleanupTree(temp_root)
        readme = temp_root / "README.md"
        readme.write_text(
            "# Example\n\nInline `<!-- vision:start -->` text is not a generated marker block.\n",
            encoding="utf-8",
        )

        absent = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(absent.returncode, 0, msg=absent.stdout + absent.stderr)

        readme.write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )
        valid = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(valid.returncode, 0, msg=valid.stdout + valid.stderr)

        readme.write_text("# Example\n\n<!-- vision:start -->\nMissing end.\n", encoding="utf-8")
        malformed = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(malformed.returncode, 0)

    def test_ci_wrapper_executes_selector_selected_path_and_root_checks(self) -> None:
        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md",
            "--path",
            "specs/test-layering-and-change-scoped-validation.md",
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertIn("Selector mode: explicit", output)
        self.assertIn("Run selected check: review_artifacts.validate", output)
        self.assertIn("Run selected check: artifact_lifecycle.validate", output)
        self.assertIn(
            "python scripts/validate-review-artifacts.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/",
            output,
        )
        self.assertIn(
            "python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/test-layering-and-change-scoped-validation.md",
            output,
        )

    def test_ci_wrapper_fails_on_blocked_selector_without_partial_execution(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                status="blocked",
                selected_checks=[
                    {
                        "id": "review_artifacts.validate",
                        "command": "python scripts/validate-review-artifacts.py docs/changes/example/",
                        "reason": "must not run when selector is blocked",
                        "affected_roots": ["docs/changes/example/"],
                    }
                ],
                blocking_results=[
                    {
                        "code": "unclassified-path",
                        "path": "experimental/runtime/example.txt",
                        "message": "changed path is not classified by the v1 selector",
                    }
                ],
            )
        )

        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "experimental/runtime/example.txt",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture), "RIGORLOOP_SELECTOR_FIXTURE_EXIT": "2"},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Selector status: blocked", output)
        self.assertIn("unclassified-path", output)
        self.assertNotIn("Run selected check: review_artifacts.validate", output)

    def test_ci_wrapper_rejects_fallback_and_malformed_selector_output(self) -> None:
        fallback_fixture = self.write_selector_fixture(self.minimal_selector_payload(status="fallback"))
        fallback = run_ci(
            "--mode",
            "explicit",
            "--path",
            "experimental/runtime/example.txt",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fallback_fixture), "RIGORLOOP_SELECTOR_FIXTURE_EXIT": "3"},
        )
        fallback_output = fallback.stdout + fallback.stderr

        self.assertNotEqual(fallback.returncode, 0)
        self.assertIn("Selector status: fallback", fallback_output)
        self.assertIn("fallback execution is not supported in v1", fallback_output)

        malformed_fixture = self.write_selector_fixture("not json")
        malformed = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(malformed_fixture)},
        )
        malformed_output = malformed.stdout + malformed.stderr

        self.assertNotEqual(malformed.returncode, 0)
        self.assertIn("Malformed selector JSON", malformed_output)

    def test_ci_wrapper_rejects_selector_command_mismatch(self) -> None:
        marker_root = Path(tempfile.mkdtemp(prefix="validation-selection-command-mismatch-"))
        self.addCleanupTree(marker_root)
        marker = marker_root / "executed"
        tampered_command = (
            f"{sys.executable} -c "
            f"\"from pathlib import Path; Path({str(marker)!r}).write_text('ran')\""
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "skills.validate",
                        "command": tampered_command,
                        "reason": "tampered selector command must not be trusted",
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("command does not match catalog", output)
        self.assertNotIn("Run selected check: skills.validate", output)
        self.assertFalse(marker.exists())

    def test_ci_wrapper_preserves_selected_command_failure(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "release.validate",
                        "command": "python scripts/validate-release.py --version missing-version",
                        "reason": "fixture release version should fail validation",
                        "versions": ["missing-version"],
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "release",
            "--release-version",
            "missing-version",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Run selected check: release.validate", output)
        self.assertIn("Selected check release.validate failed", output)

    def test_ci_wrapper_jobs_one_uses_stable_summary_and_hides_success_output(self) -> None:
        workspace = self.make_ci_workspace()
        order_file = workspace / "order.txt"
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import os
import sys
from pathlib import Path

with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("skills-start\\n")
print("SKILLS_STDOUT")
print("SKILLS_STDERR", file=sys.stderr)
with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("skills-end\\n")
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            """
import os
import sys
from pathlib import Path

with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("adapters-start\\n")
print("ADAPTERS_STDOUT")
print("ADAPTERS_STDERR", file=sys.stderr)
with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("adapters-end\\n")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", "python scripts/test-adapter-distribution.py"),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            env={"ORDER_FILE": str(order_file)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(
            order_file.read_text(encoding="utf-8").splitlines(),
            ["skills-start", "skills-end", "adapters-start", "adapters-end"],
        )
        self.assertIn("Selected CI check summary:", output)
        self.assertIn("skills.regression | passed | ok |", output)
        self.assertIn("adapters.regression | passed | ok |", output)
        self.assertLess(
            output.index("skills.regression | passed | ok |"),
            output.index("adapters.regression | passed | ok |"),
        )
        self.assertNotIn("SKILLS_STDOUT", output)
        self.assertNotIn("ADAPTERS_STDERR", output)
        self.assertIn("Selected CI checks passed.", output)

    def test_ci_wrapper_run_to_completion_reports_failed_output_after_summary(self) -> None:
        workspace = self.make_ci_workspace()
        marker = workspace / "second-ran.txt"
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import sys

print("FIRST_STDOUT")
print("FIRST_STDERR", file=sys.stderr)
raise SystemExit(7)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            """
import os
from pathlib import Path

Path(os.environ["SECOND_MARKER"]).write_text("ran", encoding="utf-8")
print("SECOND_STDOUT")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", "python scripts/test-adapter-distribution.py"),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            env={"SECOND_MARKER": str(marker)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(marker.exists(), msg=output)
        self.assertIn("skills.regression | exited | exit code 7 |", output)
        self.assertIn("adapters.regression | passed | ok |", output)
        self.assertLess(output.index("Selected CI check summary:"), output.index("Failed selected check output:"))
        self.assertIn("==> skills.regression (exited)", output)
        self.assertIn("--- stdout ---", output)
        self.assertIn("FIRST_STDOUT", output)
        self.assertIn("--- stderr ---", output)
        self.assertIn("FIRST_STDERR", output)
        self.assertNotIn("SECOND_STDOUT", output)

    def test_ci_wrapper_verbose_prints_successful_output_in_stable_order(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            "import sys\nprint('SKILL_VERBOSE_STDOUT')\nprint('SKILL_VERBOSE_STDERR', file=sys.stderr)\n",
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            "print('ADAPTER_VERBOSE_STDOUT')\n",
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", "python scripts/test-adapter-distribution.py"),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            "--verbose",
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertIn("Selected check output:", output)
        self.assertLess(output.index("==> skills.regression (passed)"), output.index("==> adapters.regression (passed)"))
        self.assertIn("SKILL_VERBOSE_STDOUT", output)
        self.assertIn("SKILL_VERBOSE_STDERR", output)
        self.assertIn("ADAPTER_VERBOSE_STDOUT", output)

    def test_ci_wrapper_reports_decode_failures_without_emitting_invalid_bytes(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import sys

sys.stdout.buffer.write(b"valid-before-stdout\\n")
sys.stdout.buffer.write(b"bad-stdout-\\xff\\n")
sys.stderr.buffer.write(b"bad-stderr-\\xfe\\n")
raise SystemExit(1)
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            text=False,
        )
        assert isinstance(result.stdout, bytes)
        combined = result.stdout + result.stderr
        output = combined.decode("utf-8")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skills.regression | exited | exit code 1; stdout decode error; stderr decode error |", output)
        self.assertIn("--- stdout (decode error; replacement text) ---", output)
        self.assertIn("bad-stdout-", output)
        self.assertIn("--- stderr (decode error; replacement text) ---", output)
        self.assertIn("bad-stderr-", output)

    def test_ci_wrapper_timeout_and_signal_failures_have_distinct_statuses(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            "import time\nprint('before-timeout', flush=True)\ntime.sleep(5)\n",
        )
        timeout_fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                ]
            )
        )

        timed_out = self.run_workspace_ci(
            workspace,
            timeout_fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            "--timeout",
            "1",
        )
        assert isinstance(timed_out.stdout, str)
        timeout_output = timed_out.stdout + timed_out.stderr

        self.assertNotEqual(timed_out.returncode, 0)
        self.assertIn("skills.regression | timed out | timeout after 1s |", timeout_output)
        self.assertIn("before-timeout", timeout_output)

        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            f"import os, signal\nos.kill(os.getpid(), {signal.SIGTERM})\n",
        )
        signal_fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                ]
            )
        )

        killed = self.run_workspace_ci(
            workspace,
            signal_fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
        )
        assert isinstance(killed.stdout, str)
        signal_output = killed.stdout + killed.stderr

        self.assertNotEqual(killed.returncode, 0)
        self.assertIn("skills.regression | killed | signal SIGTERM (15) |", signal_output)

    def test_ci_wrapper_reports_unavailable_selected_command(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-ci-missing-"))
        self.addCleanupTree(temp_root)
        (temp_root / "scripts").mkdir()
        shutil.copy2(CI, temp_root / "scripts" / "ci.sh")
        shutil.copy2(ROOT / "scripts" / "validation_selection.py", temp_root / "scripts" / "validation_selection.py")
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "release.validate",
                        "command": "python scripts/validate-release.py --version v0.1.1",
                        "reason": "fixture command should be unavailable in the temporary workspace",
                        "versions": ["v0.1.1"],
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "release",
            "--release-version",
            "v0.1.1",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
            script=temp_root / "scripts" / "ci.sh",
            cwd=temp_root,
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Run selected check: release.validate", output)
        self.assertIn("release.validate | unavailable | command unavailable: scripts/validate-release.py |", output)

    def test_ci_wrapper_forwards_mode_arguments_to_selector(self) -> None:
        fixture = self.write_selector_fixture(self.minimal_selector_payload())
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-trace-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            (
                ["--mode", "pr", "--base", "base-sha", "--head", "head-sha"],
                ["--mode", "pr", "--base", "base-sha", "--head", "head-sha"],
            ),
            (
                ["--mode", "main", "--base", "before-sha", "--head", "after-sha"],
                ["--mode", "main", "--base", "before-sha", "--head", "after-sha"],
            ),
            (
                ["--mode", "release", "--release-version", "v0.1.1"],
                ["--mode", "release", "--release-version", "v0.1.1"],
            ),
            (
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md", "--broad-smoke"],
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md", "--broad-smoke"],
            ),
        ]

        for args, expected in cases:
            with self.subTest(args=args):
                trace.write_text("", encoding="utf-8")
                result = run_ci(
                    *args,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                    },
                )
                output = result.stdout + result.stderr

                self.assertEqual(result.returncode, 0, msg=output)
                traced = trace.read_text(encoding="utf-8").splitlines()
                self.assertEqual(traced[-len(expected) :], expected)

    def test_ci_wrapper_accepts_execution_flags_without_forwarding_to_selector(self) -> None:
        fixture = self.write_selector_fixture(self.minimal_selector_payload())
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-flags-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            (
                [
                    "--mode",
                    "explicit",
                    "--path",
                    "skills/code-review/SKILL.md",
                    "--jobs",
                    "2",
                    "--timeout",
                    "60",
                    "--fail-fast",
                    "--verbose",
                ],
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md"],
            ),
            (
                [
                    "--mode",
                    "pr",
                    "--base",
                    "base-sha",
                    "--head",
                    "head-sha",
                    "--jobs",
                    "1",
                    "--timeout",
                    "120",
                ],
                ["--mode", "pr", "--base", "base-sha", "--head", "head-sha"],
            ),
            (
                [
                    "--mode",
                    "main",
                    "--base",
                    "before-sha",
                    "--head",
                    "after-sha",
                    "--verbose",
                ],
                ["--mode", "main", "--base", "before-sha", "--head", "after-sha"],
            ),
            (
                [
                    "--mode",
                    "release",
                    "--release-version",
                    "v0.1.1",
                    "--fail-fast",
                    "--jobs",
                    "3",
                ],
                ["--mode", "release", "--release-version", "v0.1.1"],
            ),
        ]

        for args, expected in cases:
            with self.subTest(args=args):
                trace.write_text("", encoding="utf-8")
                result = run_ci(
                    *args,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                    },
                )
                output = result.stdout + result.stderr

                self.assertEqual(result.returncode, 0, msg=output)
                traced = trace.read_text(encoding="utf-8").splitlines()
                self.assertEqual(traced[-len(expected) :], expected)

        broad_smoke = run_ci(
            "--mode",
            "broad-smoke",
            "--jobs",
            "1",
            "--timeout",
            "60",
            "--fail-fast",
            "--verbose",
            env={"RIGORLOOP_CI_BROAD_SMOKE_STUB": "1"},
        )
        self.assertEqual(broad_smoke.returncode, 0, msg=broad_smoke.stdout + broad_smoke.stderr)
        self.assertIn("Broad smoke stub", broad_smoke.stdout + broad_smoke.stderr)

    def test_ci_wrapper_rejects_invalid_execution_flags_before_selector(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "broad_smoke.repo",
                        "command": "bash scripts/ci.sh --mode broad-smoke",
                        "reason": "must not run when wrapper arguments are invalid",
                    }
                ]
            )
        )
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-invalid-flags-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            ("--jobs", "0"),
            ("--jobs", "-1"),
            ("--jobs", "abc"),
            ("--jobs", ""),
            ("--jobs", "unlimited"),
            ("--timeout", "0"),
            ("--timeout", "-1"),
            ("--timeout", "abc"),
            ("--timeout", ""),
        ]

        for flag, value in cases:
            with self.subTest(flag=flag, value=value):
                if trace.exists():
                    trace.unlink()
                result = run_ci(
                    "--mode",
                    "explicit",
                    "--path",
                    "skills/code-review/SKILL.md",
                    flag,
                    value,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                        "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
                    },
                )
                output = result.stdout + result.stderr

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"Invalid {flag}", output)
                self.assertFalse(trace.exists(), msg=output)
                self.assertNotIn("Selector mode:", output)
                self.assertNotIn("Run selected check:", output)

    def test_ci_wrapper_delegates_broad_smoke_non_recursively(self) -> None:
        malformed_fixture = self.write_selector_fixture("not json")
        direct = run_ci(
            "--mode",
            "broad-smoke",
            env={
                "RIGORLOOP_SELECTOR_FIXTURE": str(malformed_fixture),
                "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
            },
        )
        direct_output = direct.stdout + direct.stderr

        self.assertEqual(direct.returncode, 0, msg=direct_output)
        self.assertIn("Broad smoke stub", direct_output)
        self.assertNotIn("Malformed selector JSON", direct_output)

        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "broad_smoke.repo",
                        "command": "bash scripts/ci.sh --mode broad-smoke",
                        "reason": "Broad smoke is required by an authoritative source.",
                    }
                ]
            )
        )
        selected = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            "--verbose",
            env={
                "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
            },
        )
        selected_output = selected.stdout + selected.stderr

        self.assertEqual(selected.returncode, 0, msg=selected_output)
        self.assertIn("Run selected check: broad_smoke.repo", selected_output)
        self.assertIn("Broad smoke stub", selected_output)

    def test_workflow_guidance_aligns_with_validation_layering_contract(self) -> None:
        expectations = {
            "specs/rigorloop-workflow.md": [
                "targeted proof",
                "broad smoke",
                "manual proof",
                "scripts/select-validation.py",
                "broad_smoke_required",
                "skills.validate",
                "broad_smoke.repo",
            ],
            "docs/workflows.md": [
                "targeted proof",
                "broad smoke",
                "scripts/select-validation.py",
                "scripts/ci.sh --mode explicit",
                "scripts/ci.sh --mode broad-smoke",
                "skills.validate",
                "review_artifacts.validate",
                "broad_smoke.repo",
                "does not imply broad smoke for every PR",
            ],
            "skills/implement/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "scripts/select-validation.py",
                "selected checks",
                "skills.validate",
            ],
            "skills/code-review/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "selected checks",
                "direct proof",
            ],
            "skills/verify/SKILL.md": [
                "verify-report.md",
                "manual by design",
                "manual proof",
                "release metadata",
                "not-run",
                "bash scripts/ci.sh --mode broad-smoke",
                "broad_smoke_required",
            ],
            "skills/workflow/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "manual proof",
                "broad_smoke.sources",
                "verify-report.md",
            ],
        }

        for path, required_terms in expectations.items():
            with self.subTest(path=path):
                content = (ROOT / path).read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, content)

    def test_local_mode_discovers_tracked_and_untracked_git_paths(self) -> None:
        repo = self.make_git_repo()
        (repo / "skills" / "workflow" / "SKILL.md").write_text("# Workflow\n\nChanged\n", encoding="utf-8")
        (repo / "docs" / "changes" / "2026-04-25-local").mkdir(parents=True)
        (repo / "docs" / "changes" / "2026-04-25-local" / "change.yaml").write_text(
            "change_id: 2026-04-25-local\n",
            encoding="utf-8",
        )

        result = select_validation(SelectionRequest(mode="local", repo_root=repo))
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("skills/workflow/SKILL.md", payload["changed_paths"])
        self.assertIn("docs/changes/2026-04-25-local/change.yaml", payload["changed_paths"])
        self.assertIn("skills.validate", selected_ids(payload))
        self.assertIn("change_metadata.validate", selected_ids(payload))

    def test_normalize_path_rejects_outside_repository_paths(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-paths-"))
        self.addCleanupTree(temp_root)
        outside = temp_root.parent / "outside.txt"

        normalized = normalize_path(str(outside), repo_root=temp_root)
        self.assertFalse(normalized.ok)
        self.assertEqual(normalized.blocking_code, "outside-repository-path")


if __name__ == "__main__":
    unittest.main(verbosity=2)
