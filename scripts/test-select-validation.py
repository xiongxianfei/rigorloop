#!/usr/bin/env python3
"""Fixture-driven tests for validation selection."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / "scripts" / "select-validation.py"
CI = ROOT / "scripts" / "ci.sh"
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
                "status": "blocked",
                "blocking_code": "manual-routing-required",
            },
            {
                "path": "CONSTITUTION.md",
                "category": "governance",
                "status": "blocked",
                "blocking_code": "manual-routing-required",
            },
            {
                "path": "schemas/change.schema.json",
                "category": "schemas",
                "status": "blocked",
                "blocking_code": "manual-routing-required",
            },
            {
                "path": "templates/example.md",
                "category": "templates",
                "status": "blocked",
                "blocking_code": "manual-routing-required",
            },
            {
                "path": "scripts/build-adapters.py",
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
                "category": "script-unsupported",
                "status": "blocked",
                "blocking_code": "manual-routing-required",
            },
            {
                "path": "scripts/ci.sh",
                "category": "ci-wrapper",
                "status": "ok",
                "checks": {"selector.regression"},
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
        self.assertIn("command is unavailable: scripts/validate-release.py", output)

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
