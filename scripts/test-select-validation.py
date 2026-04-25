#!/usr/bin/env python3
"""Fixture-driven tests for validation selection."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / "scripts" / "select-validation.py"
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

    def select(self, paths: list[str], *, mode: str = "explicit", **kwargs):
        return select_validation(SelectionRequest(mode=mode, paths=tuple(paths), repo_root=ROOT, **kwargs))

    def test_catalog_matches_v1_contract(self) -> None:
        self.assertEqual(set(CHECK_CATALOG), set(EXPECTED_CATALOG))
        for check_id, command in EXPECTED_CATALOG.items():
            with self.subTest(check_id=check_id):
                self.assertEqual(CHECK_CATALOG[check_id].command_template, command)
                self.assertTrue(CHECK_CATALOG[check_id].category)

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

    def test_selector_and_validation_script_paths_select_regressions(self) -> None:
        result = self.select(["scripts/select-validation.py", "scripts/validate-review-artifacts.py"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertIn("review_artifacts.regression", selected_ids(payload))

    def test_governance_paths_block_with_manual_routing_instead_of_empty_ok(self) -> None:
        result = self.select(["AGENTS.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "blocked")
        self.assertIn({"path": "AGENTS.md", "category": "governance"}, payload["classified_paths"])
        self.assertIn("manual-routing-required", {item["code"] for item in payload["blocking_results"]})

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
