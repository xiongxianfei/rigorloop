#!/usr/bin/env python3
"""Fixture-driven tests for review artifact validation."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from review_artifact_validation import validate_change_root


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-review-artifacts.py"
FIXTURES = ROOT / "tests" / "fixtures" / "review-artifacts"


def copy_fixture(relative_path: str = "valid-open-resolution") -> Path:
    temp_root = Path(tempfile.mkdtemp(prefix="review-artifact-fixture-"))
    shutil.copytree(FIXTURES / relative_path, temp_root, dirs_exist_ok=True)
    return temp_root


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def drop_field(path: Path, field: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    kept = [line for line in lines if not line.startswith(f"{field}:")]
    path.write_text("\n".join(kept) + "\n", encoding="utf-8")


def replace_field(path: Path, field: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    replaced: list[str] = []
    changed = False
    for line in lines:
        if line.startswith(f"{field}:") and not changed:
            replaced.append(f"{field}: {value}")
            changed = True
        else:
            replaced.append(line)
    path.write_text("\n".join(replaced) + "\n", encoding="utf-8")


def run_cli(change_root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(change_root)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def valid_clean_review_text() -> str:
    return """
    # Code Review R1

    Review ID: code-review-r1
    Stage: code-review
    Round: 1
    Reviewer: Codex code-review skill
    Target: git diff main...HEAD
    Status: approved

    ## Findings

    No material findings.
    """


def valid_log_text(material_findings: str = "CR1-F1", open_findings: str = "CR1-F1") -> str:
    return f"""
    # Review Log

    ### Review entry
    Review ID: code-review-r1
    Stage: code-review
    Round: 1
    Status: changes-requested
    Detailed record: reviews/code-review-r1.md
    Resolution: review-resolution.md#code-review-r1
    Material findings: {material_findings}
    Open findings: {open_findings}
    """


class ReviewArtifactValidatorFixtureTests(unittest.TestCase):
    maxDiff = None

    def addCleanupTree(self, path: Path) -> None:
        self.addCleanup(lambda: shutil.rmtree(path, ignore_errors=True))

    def validate(self, change_root: Path):
        return validate_change_root(change_root, mode="structure")

    def assertPasses(self, change_root: Path) -> None:
        result = self.validate(change_root)
        self.assertFalse(
            result.blocking_findings,
            msg="\n".join(f.message for f in result.blocking_findings),
        )

    def assertFails(self, change_root: Path, expected_text: str) -> None:
        result = self.validate(change_root)
        combined = "\n".join(f.message for f in result.blocking_findings)
        self.assertTrue(result.blocking_findings, msg="expected validation to fail")
        self.assertIn(expected_text, combined)

    def fixture(self) -> Path:
        root = copy_fixture()
        self.addCleanupTree(root)
        return root

    def test_valid_structure_fixture_passes_module_and_cli(self) -> None:
        root = self.fixture()
        result = self.validate(root)
        self.assertFalse(result.blocking_findings)
        self.assertEqual(result.review_count, 1)
        self.assertEqual(result.finding_count, 1)
        self.assertEqual(result.review_log_entry_count, 1)
        self.assertEqual(result.resolution_entry_count, 1)

        cli_result = run_cli(root)
        self.assertEqual(
            cli_result.returncode,
            0,
            msg=f"stdout:\n{cli_result.stdout}\nstderr:\n{cli_result.stderr}",
        )
        self.assertIn("mode=structure", cli_result.stdout)

    def test_no_review_artifacts_passes_without_boilerplate(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-empty-"))
        self.addCleanupTree(root)
        self.assertPasses(root)

    def test_clean_review_with_log_passes_without_resolution(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-clean-"))
        self.addCleanupTree(root)
        write_text(root / "reviews" / "code-review-r1.md", valid_clean_review_text())
        write_text(root / "review-log.md", valid_log_text("None", "None").replace("changes-requested", "approved"))
        self.assertPasses(root)

    def test_reviews_directory_requires_review_log(self) -> None:
        root = self.fixture()
        (root / "review-log.md").unlink()
        self.assertFails(root, "reviews/ exists without review-log.md")

    def test_detailed_review_required_fields_are_validated(self) -> None:
        for field in ["Stage", "Round", "Reviewer", "Target", "Status"]:
            with self.subTest(field=field):
                root = self.fixture()
                drop_field(root / "reviews" / "code-review-r1.md", field)
                self.assertFails(root, f"missing required field {field}")

    def test_review_id_count_and_uniqueness_are_validated(self) -> None:
        root = self.fixture()
        drop_field(root / "reviews" / "code-review-r1.md", "Review ID")
        self.assertFails(root, "must contain exactly one Review ID")

        root = self.fixture()
        replace_field(root / "reviews" / "code-review-r1.md", "Review ID", "bad id")
        self.assertFails(root, "Review ID must be a stable ASCII identifier")

        root = self.fixture()
        with (root / "reviews" / "code-review-r1.md").open("a", encoding="utf-8") as handle:
            handle.write("\nReview ID: duplicate-event\n")
        self.assertFails(root, "must contain exactly one Review ID")

        root = self.fixture()
        shutil.copyfile(root / "reviews" / "code-review-r1.md", root / "reviews" / "code-review-r2.md")
        with (root / "review-log.md").open("a", encoding="utf-8") as handle:
            handle.write(valid_log_text().replace("reviews/code-review-r1.md", "reviews/code-review-r2.md"))
        self.assertFails(root, "duplicate Review ID")

    def test_review_stage_and_finding_id_stability_are_validated(self) -> None:
        root = self.fixture()
        replace_field(root / "reviews" / "code-review-r1.md", "Stage", "casual-review")
        self.assertFails(root, "unknown review stage")

        root = self.fixture()
        replace_field(root / "reviews" / "code-review-r1.md", "Finding ID", "CR1 F1")
        self.assertFails(root, "Finding ID must be a stable ASCII identifier")

    def test_review_log_canonical_blocks_are_required(self) -> None:
        for field in ["Review ID", "Stage", "Round", "Status", "Detailed record", "Resolution", "Material findings", "Open findings"]:
            with self.subTest(field=field):
                root = self.fixture()
                drop_field(root / "review-log.md", field)
                self.assertFails(root, f"review-log entry missing required field {field}")

        root = self.fixture()
        write_text(
            root / "review-log.md",
            """
            # Review Log

            The review code-review-r1 happened and had material findings.
            """,
        )
        self.assertFails(root, "missing from review-log.md")

        root = self.fixture()
        replace_field(root / "review-log.md", "Review ID", "missing-review-r1")
        self.assertFails(root, "review-log references unknown Review ID")

        root = self.fixture()
        replace_field(root / "review-log.md", "Detailed record", "reviews/missing-review.md")
        self.assertFails(root, "Detailed record does not match review file")

        root = self.fixture()
        with (root / "review-log.md").open("a", encoding="utf-8") as handle:
            handle.write("\nReview ID: duplicate-inside-same-entry\n")
        self.assertFails(root, "review-log entry must contain exactly one Review ID")

        root = self.fixture()
        with (root / "review-log.md").open("a", encoding="utf-8") as handle:
            handle.write(valid_log_text())
        self.assertFails(root, "duplicate Review ID in review-log.md")

    def test_finding_traceability_is_validated(self) -> None:
        root = self.fixture()
        extra_review = (root / "reviews" / "code-review-r2.md")
        extra_text = (root / "reviews" / "code-review-r1.md").read_text(encoding="utf-8")
        extra_text = extra_text.replace("Review ID: code-review-r1", "Review ID: code-review-r2")
        write_text(extra_review, extra_text)
        with (root / "review-log.md").open("a", encoding="utf-8") as handle:
            handle.write(
                valid_log_text()
                .replace("Review ID: code-review-r1", "Review ID: code-review-r2")
                .replace("Detailed record: reviews/code-review-r1.md", "Detailed record: reviews/code-review-r2.md")
            )
        self.assertFails(root, "duplicate Finding ID")

        root = self.fixture()
        (root / "review-resolution.md").unlink()
        self.assertFails(root, "material findings require review-resolution.md")

        root = self.fixture()
        (root / "review-resolution.md").write_text("Closeout status: open\n", encoding="utf-8")
        self.assertFails(root, "missing from review-resolution.md")

        root = self.fixture()
        with (root / "review-resolution.md").open("a", encoding="utf-8") as handle:
            handle.write(
                """

Finding ID: CR1-F99
Disposition: accepted
Owner: implementer
Owning stage: implement
Chosen action: Add proof.
Rationale: Present for structure validation.
Validation target: Run tests.
"""
            )
        self.assertFails(root, "review-resolution.md references unknown Finding ID")

    def test_resolution_structure_and_dispositions_are_validated(self) -> None:
        for field, expected in [
            ("Owner", "missing owner"),
            ("Owning stage", "missing owning stage"),
            ("Validation target", "missing validation target or expected proof"),
            ("Chosen action", "missing chosen action or stop state"),
            ("Rationale", "missing rationale"),
        ]:
            with self.subTest(field=field):
                root = self.fixture()
                drop_field(root / "review-resolution.md", field)
                self.assertFails(root, expected)

        root = self.fixture()
        replace_field(root / "review-resolution.md", "Closeout status", "almost-closed")
        self.assertFails(root, "invalid closeout status")

        root = self.fixture()
        replace_field(root / "review-resolution.md", "Disposition", "maybe")
        self.assertFails(root, "unsupported disposition")

    def test_needs_decision_and_final_action_labels_are_valid_structure(self) -> None:
        root = self.fixture()
        resolution = """
        # Review Resolution

        Closeout status: open

        Finding ID: CR1-F1
        Disposition: needs-decision
        Decision owner: maintainer
        Decision needed: Decide whether this follow-up is in scope.
        Owning stage: plan
        Stop state: blocked until owner decision
        Validation target: Owner decision recorded or finding deferred.
        """
        write_text(root / "review-resolution.md", resolution)
        self.assertPasses(root)

        root = self.fixture()
        resolution = """
        # Review Resolution

        Closeout status: open

        Finding ID: CR1-F1
        Disposition: accepted
        Owner: implementer
        Owning stage: implement
        Suggested resolution: Add direct coverage.
        Final action: Added narrower direct coverage than the reviewer suggested.
        Rationale: Structure is present; the validator does not judge quality.
        Expected proof: Focused validator tests pass.
        """
        write_text(root / "review-resolution.md", resolution)
        self.assertPasses(root)

    def test_reconstructed_review_metadata_is_validated(self) -> None:
        root = self.fixture()
        review_path = root / "reviews" / "code-review-r1.md"
        lines = review_path.read_text(encoding="utf-8").splitlines()
        insert_at = lines.index("Status: changes-requested") + 1
        lines[insert_at:insert_at] = [
            "Record mode: reconstructed",
            "Original review source: chat transcript",
            "Original review evidence: durable copied summary in this file",
            "Created after fixes began: yes",
            "Loss of fidelity: none",
        ]
        review_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertPasses(root)

        root = self.fixture()
        review_path = root / "reviews" / "code-review-r1.md"
        lines = review_path.read_text(encoding="utf-8").splitlines()
        insert_at = lines.index("Status: changes-requested") + 1
        lines[insert_at:insert_at] = [
            "Record mode: reconstructed",
            "Original review source: chat transcript",
            "Created after fixes began: yes",
            "Loss of fidelity: none",
        ]
        review_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertFails(root, "missing reconstructed metadata field Original review evidence")

    def test_cli_failure_output_is_actionable_and_structural(self) -> None:
        root = self.fixture()
        drop_field(root / "review-resolution.md", "Owner")

        result = run_cli(root)
        combined = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("review-resolution.md", combined)
        self.assertIn("mode=structure", combined)
        self.assertIn("Finding ID=CR1-F1", combined)
        self.assertIn("missing owner", combined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
