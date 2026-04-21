#!/usr/bin/env python3
"""Fixture-driven tests for the artifact lifecycle validator."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from artifact_lifecycle_validation import validate_repository


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-artifact-lifecycle.py"
FIXTURES = ROOT / "tests" / "fixtures" / "artifact-lifecycle"


def copy_fixture(relative_path: str) -> Path:
    temp_root = Path(tempfile.mkdtemp(prefix="artifact-lifecycle-fixture-"))
    shutil.copytree(FIXTURES / relative_path, temp_root, dirs_exist_ok=True)
    return temp_root


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


class ArtifactLifecycleValidatorFixtureTests(unittest.TestCase):
    maxDiff = None

    def addCleanupTree(self, path: Path) -> None:
        self.addCleanup(lambda: shutil.rmtree(path, ignore_errors=True))

    def validate_fixture(
        self,
        relative_fixture: str,
        *,
        mode: str,
        paths: list[str] | None = None,
        pr_body_file: str | None = None,
    ):
        fixture_root = copy_fixture(relative_fixture)
        self.addCleanupTree(fixture_root)
        return validate_repository(
            fixture_root,
            mode=mode,
            paths=paths or [],
            pr_body_file=pr_body_file,
        )

    def assertFixturePasses(self, relative_fixture: str, path: str) -> None:
        result = self.validate_fixture(
            relative_fixture,
            mode="explicit-paths",
            paths=[path],
        )
        self.assertFalse(
            result.blocking_findings,
            msg=f"expected fixture '{relative_fixture}' to pass, got blockers: {result.blocking_findings}",
        )

    def assertFixtureFails(self, relative_fixture: str, path: str, expected_text: str) -> None:
        result = self.validate_fixture(
            relative_fixture,
            mode="explicit-paths",
            paths=[path],
        )
        combined_messages = "\n".join(f.message for f in result.blocking_findings)
        self.assertTrue(result.blocking_findings, msg=f"expected fixture '{relative_fixture}' to fail")
        self.assertIn(expected_text, combined_messages)

    def test_valid_proposal_passes(self) -> None:
        self.assertFixturePasses(
            "valid-proposal",
            "docs/proposals/2026-04-20-valid-proposal.md",
        )

    def test_valid_draft_proposal_passes(self) -> None:
        self.assertFixturePasses(
            "valid-draft-proposal",
            "docs/proposals/2026-04-20-draft-proposal.md",
        )

    def test_valid_spec_passes(self) -> None:
        self.assertFixturePasses("valid-spec", "specs/valid-spec.md")

    def test_valid_test_spec_passes(self) -> None:
        self.assertFixturePasses("valid-test-spec", "specs/valid-feature.test.md")

    def test_valid_architecture_passes(self) -> None:
        self.assertFixturePasses(
            "valid-architecture",
            "docs/architecture/2026-04-20-valid-architecture.md",
        )

    def test_valid_adr_passes(self) -> None:
        self.assertFixturePasses(
            "valid-adr",
            "docs/adr/ADR-20260420-valid-decision.md",
        )

    def test_reviewed_status_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-reviewed-spec",
            "specs/invalid-reviewed.md",
            "invalid status 'reviewed'",
        )

    def test_complete_test_spec_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-complete-test-spec",
            "specs/invalid-complete.test.md",
            "invalid status 'complete'",
        )

    def test_empty_follow_on_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-empty-follow-on",
            "specs/invalid-empty-follow-on.test.md",
            "Follow-on artifacts section must not be empty",
        )

    def test_empty_next_artifacts_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-empty-next-artifacts",
            "docs/proposals/2026-04-20-empty-next-artifacts.md",
            "Next artifacts section must not be empty",
        )

    def test_superseded_without_pointer_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-superseded-without-pointer",
            "docs/architecture/2026-04-20-old-architecture.md",
            "superseded artifacts must identify a replacement",
        )

    def test_placeholder_text_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-placeholder",
            "docs/proposals/2026-04-20-placeholder-proposal.md",
            "placeholder text is not allowed",
        )

    def test_invalid_proposal_filename_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-proposal-name",
            "docs/proposals/not-date-prefixed.md",
            "invalid proposal identifier",
        )

    def test_invalid_spec_filename_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-spec-name",
            "specs/InvalidSpec.md",
            "invalid top-level spec identifier",
        )

    def test_invalid_adr_filename_fails(self) -> None:
        self.assertFixtureFails(
            "invalid-adr-name",
            "docs/adr/ADR-20260420-InvalidDecision.md",
            "invalid ADR identifier",
        )

    def test_duplicate_spec_identifier_fails(self) -> None:
        result = self.validate_fixture(
            "duplicate-spec-identifier",
            mode="explicit-paths",
            paths=[
                "specs/alpha/shared-spec.md",
                "specs/beta/shared-spec.md",
            ],
        )
        combined_messages = "\n".join(f.message for f in result.blocking_findings)
        self.assertTrue(result.blocking_findings)
        self.assertIn("duplicate spec identifier: shared-spec", combined_messages)

    def test_generated_output_path_is_rejected(self) -> None:
        result = self.validate_fixture(
            "invalid-generated-source",
            mode="explicit-paths",
            paths=[".codex/skills/proposal/SKILL.md"],
        )
        combined_messages = "\n".join(f.message for f in result.blocking_findings)
        self.assertTrue(result.blocking_findings)
        self.assertIn("generated output path must not be treated as authored source of truth", combined_messages)

    def test_explicit_paths_ignore_unrelated_invalid_fixture_files(self) -> None:
        result = self.validate_fixture(
            "explicit-scope",
            mode="explicit-paths",
            paths=["docs/proposals/2026-04-20-valid-proposal.md"],
        )
        self.assertFalse(result.blocking_findings)
        checked_paths = {path.as_posix() for path in result.checked_artifacts}
        self.assertIn("docs/proposals/2026-04-20-valid-proposal.md", checked_paths)
        self.assertNotIn("specs/invalid-reviewed.md", checked_paths)

    def test_specs_docs_are_not_classified_as_behavior_specs(self) -> None:
        result = self.validate_fixture(
            "spec-docs-only",
            mode="explicit-paths",
            paths=["specs/README.md"],
        )
        self.assertFalse(result.blocking_findings)
        self.assertFalse(result.warning_findings)
        self.assertEqual([], result.checked_artifacts)

    def test_change_yaml_explain_change_plan_and_pr_body_expand_related_scope(self) -> None:
        fixture_root = copy_fixture("related-scope")
        self.addCleanupTree(fixture_root)
        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=[
                "docs/changes/0002-lifecycle/change.yaml",
                "docs/explain/2026-04-20-related-change.md",
                "docs/plans/2026-04-20-related-plan.md",
            ],
            pr_body_file="pr-body.md",
        )
        self.assertFalse(result.blocking_findings)
        checked_paths = {path.as_posix() for path in result.checked_artifacts}
        self.assertIn("docs/proposals/2026-04-20-related-proposal.md", checked_paths)
        self.assertIn("specs/related-spec.md", checked_paths)
        self.assertIn("docs/architecture/2026-04-20-related-architecture.md", checked_paths)

    def test_local_mode_blocks_related_and_warns_unrelated_baseline(self) -> None:
        fixture_root = copy_fixture("local-scope")
        self.addCleanupTree(fixture_root)
        subprocess.run(["git", "init"], cwd=fixture_root, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "config", "user.email", "tester@example.com"],
            cwd=fixture_root,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture Tester"],
            cwd=fixture_root,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(["git", "add", "."], cwd=fixture_root, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "fixture baseline"],
            cwd=fixture_root,
            check=True,
            capture_output=True,
            text=True,
        )
        related_path = fixture_root / "docs" / "proposals" / "2026-04-20-related-proposal.md"
        related_path.write_text(related_path.read_text(encoding="utf-8") + "\nChanged locally.\n", encoding="utf-8")

        result = validate_repository(fixture_root, mode="local")
        blocking_paths = {f.path.name for f in result.blocking_findings}
        warning_paths = {f.path.name for f in result.warning_findings}
        self.assertIn("2026-04-20-related-proposal.md", blocking_paths)
        self.assertIn("2026-04-20-unrelated-proposal.md", warning_paths)

    def test_local_mode_blocks_duplicate_identifier_when_any_participant_is_related(self) -> None:
        fixture_root = copy_fixture("duplicate-spec-identifier")
        self.addCleanupTree(fixture_root)
        subprocess.run(["git", "init"], cwd=fixture_root, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "config", "user.email", "tester@example.com"],
            cwd=fixture_root,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture Tester"],
            cwd=fixture_root,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(["git", "add", "."], cwd=fixture_root, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "fixture baseline"],
            cwd=fixture_root,
            check=True,
            capture_output=True,
            text=True,
        )
        related_path = fixture_root / "specs" / "alpha" / "shared-spec.md"
        related_path.write_text(related_path.read_text(encoding="utf-8") + "\nChanged locally.\n", encoding="utf-8")

        result = validate_repository(fixture_root, mode="local")
        blocking_paths = {f.path.relative_to(fixture_root).as_posix() for f in result.blocking_findings}
        self.assertIn("specs/alpha/shared-spec.md", blocking_paths)
        self.assertIn("specs/beta/shared-spec.md", blocking_paths)

    def test_cli_requires_pr_ci_and_push_ci_inputs(self) -> None:
        pr_result = run_cli("--mode", "pr-ci")
        self.assertNotEqual(pr_result.returncode, 0)
        self.assertIn("requires --base and --head", pr_result.stderr + pr_result.stdout)

        push_result = run_cli("--mode", "push-main-ci")
        self.assertNotEqual(push_result.returncode, 0)
        self.assertIn("requires --before and --after", push_result.stderr + push_result.stdout)

    def test_cli_requires_explicit_paths(self) -> None:
        result = run_cli("--mode", "explicit-paths")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires at least one --path", result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
