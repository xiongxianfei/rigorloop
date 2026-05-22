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


def write_minimal_test_spec(root: Path, readiness: str) -> Path:
    target = root / "specs" / "workflow-state.test.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"""# Workflow State Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/workflow-state.md`
- Plan: `docs/plans/2026-05-09-workflow-state.md`

## Testing strategy

- Validate readiness wording.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1` | `T1` | integration | readiness wording |

## Test cases

### T1. Readiness wording

- Covers: `R1`
- Level: integration
- Fixture/setup:
- Steps:
- Expected result:
- Failure proves:
- Automation location:

## Readiness

{readiness}
""",
        encoding="utf-8",
    )
    return target


def init_git_fixture(path: Path) -> str:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "config", "user.email", "tester@example.com"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Fixture Tester"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(["git", "add", "."], cwd=path, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "commit", "-m", "fixture baseline"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def commit_fixture_change(
    path: Path,
    relative_path: str,
    message: str,
    *,
    extra_paths: list[str] | None = None,
) -> str:
    target = path / relative_path
    target.write_text(target.read_text(encoding="utf-8") + f"\n{message}\n", encoding="utf-8")
    add_paths = [relative_path, *(extra_paths or [])]
    subprocess.run(["git", "add", *add_paths], cwd=path, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def checkout_fixture_branch(path: Path, branch: str, *, create: bool = False) -> None:
    command = ["git", "checkout"]
    if create:
        command.append("-b")
    command.append(branch)
    subprocess.run(command, cwd=path, check=True, capture_output=True, text=True)


def current_fixture_branch(path: Path) -> str:
    return subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


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

    def assertFixtureWarns(self, relative_fixture: str, path: str, expected_text: str) -> None:
        result = self.validate_fixture(
            relative_fixture,
            mode="explicit-paths",
            paths=[path],
        )
        combined_warnings = "\n".join(f.message for f in result.warning_findings)
        self.assertFalse(
            result.blocking_findings,
            msg=f"expected fixture '{relative_fixture}' to warn without blocking, got blockers: {result.blocking_findings}",
        )
        self.assertTrue(result.warning_findings, msg=f"expected fixture '{relative_fixture}' to warn")
        self.assertIn(expected_text, combined_warnings)

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

    def test_title_case_proposal_headings_pass(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix="artifact-lifecycle-title-case-"))
        self.addCleanupTree(fixture_root)
        target = fixture_root / "docs" / "proposals" / "2026-04-20-title-case-proposal.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            """# Title Case Proposal

## Status

draft

## Problem

The validator should accept common formal document heading style.

## Goals

- Allow title-case lifecycle headings.

## Non-Goals

- Change lifecycle status semantics.

## Recommended Direction

Match headings case-insensitively for lifecycle validation.

## Next Artifacts

- proposal-review

## Follow-on Artifacts

None yet

## Readiness

Ready for proposal-review.
""",
            encoding="utf-8",
        )

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=[target.relative_to(fixture_root).as_posix()],
        )

        self.assertFalse(result.blocking_findings)

    def test_valid_spec_passes(self) -> None:
        self.assertFixturePasses("valid-spec", "specs/valid-spec.md")

    def test_valid_test_spec_passes(self) -> None:
        self.assertFixturePasses("valid-test-spec", "specs/valid-feature.test.md")

    def test_active_test_spec_may_delegate_live_state_to_current_handoff_summary(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix="artifact-lifecycle-readiness-"))
        self.addCleanupTree(fixture_root)
        target = write_minimal_test_spec(
            fixture_root,
            "Active proof surface for implementation. The active plan `Current Handoff Summary` owns the next workflow action.",
        )

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=[target.relative_to(fixture_root).as_posix()],
        )

        self.assertFalse(result.blocking_findings)

    def test_active_test_spec_stale_implementation_readiness_fails(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix="artifact-lifecycle-readiness-"))
        self.addCleanupTree(fixture_root)
        target = write_minimal_test_spec(
            fixture_root,
            "Ready for `implement M1`.",
        )

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=[target.relative_to(fixture_root).as_posix()],
        )

        combined_messages = "\n".join(f.message for f in result.blocking_findings)
        self.assertTrue(result.blocking_findings)
        self.assertIn("status and readiness disagree", combined_messages)

    def test_valid_architecture_passes(self) -> None:
        self.assertFixturePasses(
            "valid-architecture",
            "docs/architecture/2026-04-20-valid-architecture.md",
        )

    def test_valid_canonical_arc42_architecture_passes(self) -> None:
        self.assertFixturePasses(
            "valid-canonical-arc42-architecture",
            "docs/architecture/system/architecture.md",
        )

    def test_canonical_architecture_compatibility_does_not_enforce_package_shape(self) -> None:
        self.assertFixturePasses(
            "canonical-architecture-lifecycle-only",
            "docs/architecture/system/architecture.md",
        )

    def test_canonical_arc42_contract_is_path_scoped(self) -> None:
        self.assertFixtureFails(
            "invalid-canonical-arc42-legacy-path",
            "docs/architecture/2026-04-20-canonical-shaped-architecture.md",
            "missing required 'Related artifacts' section",
        )

    def test_valid_adr_passes(self) -> None:
        self.assertFixturePasses(
            "valid-adr",
            "docs/adr/ADR-20260420-valid-decision.md",
        )

    def test_valid_active_adr_passes(self) -> None:
        self.assertFixturePasses(
            "valid-active-adr",
            "docs/adr/ADR-20260420-active-decision.md",
        )

    def test_valid_deprecated_adr_passes(self) -> None:
        self.assertFixturePasses(
            "valid-deprecated-adr",
            "docs/adr/ADR-20260420-deprecated-decision.md",
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

    def test_docs_examples_plan_is_not_active_lifecycle_state(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix="artifact-lifecycle-examples-"))
        self.addCleanupTree(fixture_root)
        example_plan = fixture_root / "docs" / "examples" / "plans" / "example-plan.md"
        example_plan.parent.mkdir(parents=True)
        example_plan.write_text(
            """# Example Plan

- Status: active

## Readiness

- Ready for `implement M1`.
""",
            encoding="utf-8",
        )

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=["docs/examples/plans/example-plan.md"],
        )

        self.assertFalse(result.blocking_findings)

    def test_docs_examples_formal_review_records_are_not_active_lifecycle_state(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix="artifact-lifecycle-review-examples-"))
        self.addCleanupTree(fixture_root)
        review_like_example = fixture_root / "docs" / "examples" / "formal-review-recording" / "clean-review-receipt-root.md"
        review_like_example.parent.mkdir(parents=True)
        review_like_example.write_text(
            """# Clean Review Receipt Root

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Status: approved
Recording status: recorded

## Review Entries

This is an example, not active lifecycle state.
""",
            encoding="utf-8",
        )

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=["docs/examples/formal-review-recording/clean-review-receipt-root.md"],
        )

        self.assertFalse(result.blocking_findings)
        self.assertEqual(result.checked_artifacts, [])

    def test_retained_skill_validator_fixture_readme_documents_non_active_status(self) -> None:
        fixture_readme = ROOT / "docs" / "changes" / "0001-skill-validator" / "README.md"
        text = fixture_readme.read_text(encoding="utf-8")

        self.assertIn("retained validator fixture", text)
        self.assertIn("not an active change root", text)
        self.assertIn("not the universal template", text)
        self.assertIn("does not block the v0.1.2 archive-introduction release", text)
        self.assertIn("docs/examples/changes/skill-validator/", text)

    def test_dist_adapters_generated_output_path_is_rejected(self) -> None:
        fixture_root = copy_fixture("invalid-generated-source")
        self.addCleanupTree(fixture_root)
        generated = fixture_root / "dist" / "adapters" / "codex" / "AGENTS.md"
        generated.parent.mkdir(parents=True)
        generated.write_text("# Generated adapter\n", encoding="utf-8")

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=["dist/adapters/codex/AGENTS.md"],
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

    def test_change_local_markdown_refs_do_not_recursively_expand_related_scope(self) -> None:
        fixture_root = copy_fixture("related-scope")
        self.addCleanupTree(fixture_root)

        change_yaml = fixture_root / "docs" / "changes" / "0002-lifecycle" / "change.yaml"
        change_yaml.write_text(
            """change_id: 0002-lifecycle
title: Related scope fixture
classification: default
risk: low
artifacts:
  proposal: docs/proposals/2026-04-20-related-proposal.md
  spec: specs/related-spec.md
  architecture: docs/architecture/2026-04-20-related-architecture.md
  verify_report: docs/changes/0002-lifecycle/verify-report.md
""",
            encoding="utf-8",
        )

        verify_report = fixture_root / "docs" / "changes" / "0002-lifecycle" / "verify-report.md"
        verify_report.write_text(
            """# Related verify report

- `docs/plans/2026-04-20-nested-plan.md`
""",
            encoding="utf-8",
        )

        nested_plan = fixture_root / "docs" / "plans" / "2026-04-20-nested-plan.md"
        nested_plan.write_text(
            """# Nested plan

## Source artifacts

- Proposal: `docs/proposals/2026-04-20-unrelated-proposal.md`
""",
            encoding="utf-8",
        )

        unrelated_proposal = fixture_root / "docs" / "proposals" / "2026-04-20-unrelated-proposal.md"
        unrelated_proposal.write_text(
            """# Unrelated proposal

## Status
- draft
""",
            encoding="utf-8",
        )

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
        self.assertNotIn("docs/plans/2026-04-20-nested-plan.md", checked_paths)
        self.assertNotIn("docs/proposals/2026-04-20-unrelated-proposal.md", checked_paths)

    def test_plan_scope_uses_current_context_refs_but_ignores_future_milestone_targets(self) -> None:
        fixture_root = copy_fixture("related-scope")
        self.addCleanupTree(fixture_root)
        current_context = fixture_root / "specs" / "related-history.test.md"
        current_context.write_text(
            """# Related history test spec

## Status

- active

## Related spec and plan

- Spec: `specs/related-spec.md`
- Plan: `docs/plans/2026-04-20-related-plan.md`

## Testing strategy

- Keep the fixture valid.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1` | `T1` | integration | plan-wide path extraction |

## Test cases

### T1. Plan-wide extraction fixture

- Covers: R1
- Level: integration
- Fixture/setup:
- Steps:
- Expected result:
- Failure proves:
- Automation location:
""",
            encoding="utf-8",
        )
        future_target = fixture_root / "specs" / "future-stale.test.md"
        future_target.write_text(
            """# Future stale test spec

## Status

- active

## Related spec and plan

- Spec: `specs/related-spec.md`
- Plan: `docs/plans/2026-04-20-related-plan.md`

## Testing strategy

- Keep the fixture valid.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1` | `T2` | integration | future milestone target |

## Test cases

### T2. Future milestone target fixture

- Covers: R1
- Level: integration
- Fixture/setup:
- Steps:
- Expected result:
- Failure proves:
- Automation location:
""",
            encoding="utf-8",
        )
        plan_path = fixture_root / "docs" / "plans" / "2026-04-20-related-plan.md"
        plan_path.write_text(
            plan_path.read_text(encoding="utf-8")
            + "\n## Related artifacts\n\n- `specs/related-history.test.md`\n"
            + "\n## Context and orientation\n\n- `specs/future-stale.test.md`\n"
            + "\n## Milestones\n\n### M4. Future migration\n\n- `specs/future-stale.test.md`\n",
            encoding="utf-8",
        )

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=["docs/plans/2026-04-20-related-plan.md"],
        )
        self.assertFalse(result.blocking_findings)
        checked_paths = {path.as_posix() for path in result.checked_artifacts}
        self.assertIn("docs/proposals/2026-04-20-related-proposal.md", checked_paths)
        self.assertIn("specs/related-history.test.md", checked_paths)
        self.assertNotIn("specs/future-stale.test.md", checked_paths)

    def test_plan_index_context_expands_to_workflow_authority_artifacts(self) -> None:
        fixture_root = copy_fixture("related-scope")
        self.addCleanupTree(fixture_root)
        plan_index = fixture_root / "docs" / "plan.md"
        plan_index.write_text(
            """# Plan index

## Active
- [Related plan](plans/2026-04-20-related-plan.md)
""",
            encoding="utf-8",
        )
        test_spec = fixture_root / "specs" / "related-spec.test.md"
        test_spec.write_text(
            """# Related test spec

## Status

- active

## Related spec and plan

- Spec: `specs/related-spec.md`
- Plan: `docs/plans/2026-04-20-related-plan.md`

## Testing strategy

- Validate the workflow authority chain.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1` | `T1` | integration | plan authority expansion |

## Test cases

### T1. Plan authority expansion

- Covers: R1
- Level: integration
- Fixture/setup:
- Steps:
- Expected result:
- Failure proves:
- Automation location:
""",
            encoding="utf-8",
        )
        plan_path = fixture_root / "docs" / "plans" / "2026-04-20-related-plan.md"
        plan_path.write_text(
            plan_path.read_text(encoding="utf-8")
            + "\n- Test spec: `specs/related-spec.test.md`\n",
            encoding="utf-8",
        )

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=[
                "docs/plan.md",
                "docs/plans/2026-04-20-related-plan.md",
            ],
        )

        self.assertFalse(result.blocking_findings)
        checked_paths = {path.as_posix() for path in result.checked_artifacts}
        self.assertIn("docs/proposals/2026-04-20-related-proposal.md", checked_paths)
        self.assertIn("specs/related-spec.md", checked_paths)
        self.assertIn("specs/related-spec.test.md", checked_paths)
        self.assertIn("docs/architecture/2026-04-20-related-architecture.md", checked_paths)

    def test_plan_context_blocks_invalid_referenced_workflow_authority(self) -> None:
        fixture_root = copy_fixture("related-scope")
        self.addCleanupTree(fixture_root)
        spec_path = fixture_root / "specs" / "related-spec.md"
        spec_path.write_text(
            spec_path.read_text(encoding="utf-8").replace("- approved", "- reviewed", 1),
            encoding="utf-8",
        )

        result = validate_repository(
            fixture_root,
            mode="explicit-paths",
            paths=["docs/plans/2026-04-20-related-plan.md"],
        )

        self.assertTrue(result.blocking_findings)
        self.assertTrue(
            any(
                finding.path.as_posix().endswith("specs/related-spec.md")
                and "invalid status 'reviewed' for spec" in finding.message
                for finding in result.blocking_findings
            )
        )

    def test_plan_done_under_active_index_fails(self) -> None:
        self.assertFixtureFails(
            "plan-index-completed-under-active",
            "docs/plans/2026-05-01-completed-plan.md",
            "completed, blocked, or superseded plan must not be listed under Active",
        )

    def test_plan_index_change_validates_linked_plan_body(self) -> None:
        self.assertFixtureFails(
            "plan-index-completed-under-active",
            "docs/plan.md",
            "completed, blocked, or superseded plan must not be listed under Active",
        )

    def test_plan_done_under_active_and_done_index_fails(self) -> None:
        self.assertFixtureFails(
            "plan-index-completed-under-active-and-done",
            "docs/plans/2026-05-01-completed-plan.md",
            "completed, blocked, or superseded plan must not be listed under Active",
        )

    def test_plan_index_and_body_status_disagreement_fails(self) -> None:
        self.assertFixtureFails(
            "plan-index-body-disagreement",
            "docs/plans/2026-05-01-active-plan.md",
            "docs/plan.md lists plan as done but plan body status is active",
        )

    def test_terminal_plan_with_active_readiness_fails(self) -> None:
        self.assertFixtureFails(
            "plan-terminal-stale-readiness",
            "docs/plans/2026-05-01-stale-readiness-plan.md",
            "terminal plan readiness still describes active or in-progress work",
        )

    def test_active_plan_with_true_downstream_event_passes(self) -> None:
        self.assertFixturePasses(
            "plan-downstream-active",
            "docs/plans/2026-05-01-downstream-plan.md",
        )

    def test_merge_dependent_lifecycle_language_warns_without_blocking(self) -> None:
        self.assertFixtureWarns(
            "merge-dependent-language-warning",
            "docs/plans/2026-05-01-merge-language-plan.md",
            "merge-dependent lifecycle language requires reviewer attention",
        )

    def test_local_mode_blocks_related_and_warns_unrelated_baseline(self) -> None:
        fixture_root = copy_fixture("local-scope")
        self.addCleanupTree(fixture_root)
        init_git_fixture(fixture_root)
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
        init_git_fixture(fixture_root)
        related_path = fixture_root / "specs" / "alpha" / "shared-spec.md"
        related_path.write_text(related_path.read_text(encoding="utf-8") + "\nChanged locally.\n", encoding="utf-8")

        result = validate_repository(fixture_root, mode="local")
        blocking_paths = {f.path.relative_to(fixture_root).as_posix() for f in result.blocking_findings}
        self.assertIn("specs/alpha/shared-spec.md", blocking_paths)
        self.assertIn("specs/beta/shared-spec.md", blocking_paths)

    def test_pr_ci_mode_uses_explicit_diff_range(self) -> None:
        fixture_root = copy_fixture("local-scope")
        self.addCleanupTree(fixture_root)
        init_git_fixture(fixture_root)
        main_branch = current_fixture_branch(fixture_root)
        checkout_fixture_branch(fixture_root, "feature", create=True)
        checkout_fixture_branch(fixture_root, main_branch)
        base = commit_fixture_change(
            fixture_root,
            "docs/proposals/2026-04-20-unrelated-proposal.md",
            "base-only unrelated change",
        )
        checkout_fixture_branch(fixture_root, "feature")
        head = commit_fixture_change(
            fixture_root,
            "docs/proposals/2026-04-20-related-proposal.md",
            "fixture PR change",
        )

        result = validate_repository(fixture_root, mode="pr-ci", base=base, head=head)
        blocking_paths = {f.path.name for f in result.blocking_findings}
        warning_paths = {f.path.name for f in result.warning_findings}
        self.assertIn("2026-04-20-related-proposal.md", blocking_paths)
        self.assertIn("2026-04-20-unrelated-proposal.md", warning_paths)
        self.assertNotIn("2026-04-20-unrelated-proposal.md", blocking_paths)

    def test_pr_ci_mode_ignores_generated_outputs_in_diff(self) -> None:
        fixture_root = copy_fixture("local-scope")
        self.addCleanupTree(fixture_root)
        generated = fixture_root / ".codex" / "skills" / "proposal" / "SKILL.md"
        generated.parent.mkdir(parents=True, exist_ok=True)
        generated.write_text("generated output\n", encoding="utf-8")
        base = init_git_fixture(fixture_root)
        generated.write_text("generated output updated\n", encoding="utf-8")
        head = commit_fixture_change(
            fixture_root,
            "docs/proposals/2026-04-20-related-proposal.md",
            "fixture PR change with generated output",
            extra_paths=[".codex/skills/proposal/SKILL.md"],
        )

        result = validate_repository(fixture_root, mode="pr-ci", base=base, head=head)
        blocking_paths = {f.path.relative_to(fixture_root).as_posix() for f in result.blocking_findings}
        warning_paths = {f.path.relative_to(fixture_root).as_posix() for f in result.warning_findings}
        self.assertIn("docs/proposals/2026-04-20-related-proposal.md", blocking_paths)
        self.assertIn("docs/proposals/2026-04-20-unrelated-proposal.md", warning_paths)
        self.assertNotIn(".codex/skills/proposal/SKILL.md", blocking_paths)

    def test_pr_ci_mode_ignores_untracked_baseline_artifacts(self) -> None:
        fixture_root = copy_fixture("local-scope")
        self.addCleanupTree(fixture_root)
        base = init_git_fixture(fixture_root)
        head = commit_fixture_change(
            fixture_root,
            "docs/proposals/2026-04-20-related-proposal.md",
            "fixture PR change",
        )
        untracked = fixture_root / "docs" / "proposals" / "2026-04-20-untracked-proposal.md"
        untracked.write_text(
            """# Untracked stale proposal

## Status
- accepted

## Problem

This local draft should not affect diff-based CI validation.

## Goals

- Stay out of tracked baseline scope.

## Non-goals

- none

## Recommended direction

Leave this draft stale.

## Readiness

- ready for proposal-review
""",
            encoding="utf-8",
        )

        result = validate_repository(fixture_root, mode="pr-ci", base=base, head=head)
        finding_paths = {f.path.name for f in (*result.blocking_findings, *result.warning_findings)}
        self.assertNotIn("2026-04-20-untracked-proposal.md", finding_paths)

    def test_push_main_ci_mode_uses_explicit_diff_range(self) -> None:
        fixture_root = copy_fixture("local-scope")
        self.addCleanupTree(fixture_root)
        before = init_git_fixture(fixture_root)
        after = commit_fixture_change(
            fixture_root,
            "docs/proposals/2026-04-20-related-proposal.md",
            "fixture push change",
        )

        result = validate_repository(fixture_root, mode="push-main-ci", before=before, after=after)
        blocking_paths = {f.path.name for f in result.blocking_findings}
        warning_paths = {f.path.name for f in result.warning_findings}
        self.assertIn("2026-04-20-related-proposal.md", blocking_paths)
        self.assertIn("2026-04-20-unrelated-proposal.md", warning_paths)

    def test_push_main_ci_mode_ignores_untracked_baseline_artifacts(self) -> None:
        fixture_root = copy_fixture("local-scope")
        self.addCleanupTree(fixture_root)
        before = init_git_fixture(fixture_root)
        after = commit_fixture_change(
            fixture_root,
            "docs/proposals/2026-04-20-related-proposal.md",
            "fixture push change",
        )
        untracked = fixture_root / "docs" / "proposals" / "2026-04-20-untracked-proposal.md"
        untracked.write_text(
            """# Untracked stale proposal

## Status
- accepted

## Problem

This local draft should not affect diff-based CI validation.

## Goals

- Stay out of tracked baseline scope.

## Non-goals

- none

## Recommended direction

Leave this draft stale.

## Readiness

- ready for proposal-review
""",
            encoding="utf-8",
        )

        result = validate_repository(fixture_root, mode="push-main-ci", before=before, after=after)
        finding_paths = {f.path.name for f in (*result.blocking_findings, *result.warning_findings)}
        self.assertNotIn("2026-04-20-untracked-proposal.md", finding_paths)

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
