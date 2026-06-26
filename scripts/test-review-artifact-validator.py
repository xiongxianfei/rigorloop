#!/usr/bin/env python3
"""Fixture-driven tests for review artifact validation."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from review_artifact_validation import finding_closure_state
from review_artifact_validation import summarize_review_evidence
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
    path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")


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


def run_cli(change_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args, str(change_root)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def read_repo_file(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


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


def review_text(
    *,
    review_id: str,
    stage: str,
    status: str,
    finding_id: str | None = None,
) -> str:
    finding_block = (
        f"""
        ## Findings

        Finding ID: {finding_id}
        Severity: major
        Evidence: `specs/formal-review-recording.md` requires upstream review evidence.
        Required outcome: Preserve the material upstream review finding.
        Safe resolution: Record traceable review-resolution disposition.
        """
        if finding_id
        else """
        ## Findings

        No material findings.
        """
    )
    return f"""
    # {stage} R1

    Review ID: {review_id}
    Stage: {stage}
    Round: 1
    Reviewer: Codex review artifact validator test
    Target: docs/changes/example
    Status: {status}

    {finding_block}
    """


def implementation_profile_review_text(finding_fields: str) -> str:
    return f"""
    # Code Review R1

    Review ID: code-review-r1
    Stage: code-review
    Round: 1
    Reviewer: Codex code-review skill
    Target: implementation-through-verify correction surface
    Status: changes-requested
    Autoprogression profile: implementation-through-verify

    ## Findings

    Finding ID: CR1-F1
    Evidence: The implementation-profile correction loop needs structured reviewer authority.
    Required outcome: The finding must be structurally bounded before automatic correction.
    Safe resolution: Follow the reviewer-declared auto-fix classification.
    {finding_fields}
    """


def test_spec_review_text(
    *,
    review_status: str = "approved",
    immediate_next_stage: str = "implement",
    implementation_handoff: str = "allowed",
    status: str = "approved",
) -> str:
    return f"""
    # Test Spec Review R1

    Review ID: test-spec-review-r1
    Stage: test-spec-review
    Round: 1
    Reviewer: Codex test-spec-review skill
    Target: specs/example.test.md
    Status: {status}
    Review status: {review_status}
    Immediate next stage: {immediate_next_stage}
    Implementation handoff: {implementation_handoff}

    ## Findings

    No material findings.
    """


def valid_automated_review_text(extra_fields: str = "") -> str:
    extra = f"\n{extra_fields.strip()}\n" if extra_fields.strip() else ""
    return f"""
    # Code Review R1

    Review ID: code-review-r1
    Stage: code-review
    Round: 1
    Reviewer: Codex code-review skill
    Target: git diff main...HEAD
    Status: clean-with-notes
    Automated review: yes
    Native review status: clean-with-notes
    Review gate outcome: advance
    Independence level: L1
    Author context ID: author-ctx-1
    Reviewer context ID: reviewer-ctx-1
    Context separation mechanism: fresh-context-same-model
    Risk tier: standard
    Risk-tier triggers: none
    Risk-tier classifier: deterministic-paths
    Governing artifacts: specs/review-independence-and-criticality.md; docs/plans/example.md
    Formal criteria: R1; R3; R13
    Initial packet inventory: specs/review-independence-and-criticality.md@abc123#sha256:1111111111111111111111111111111111111111111111111111111111111111; docs/plans/example.md@abc123#sha256:2222222222222222222222222222222222222222222222222222222222222222
    Prompt template version: code-review-template-v1
    Initial packet hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    Manifest owner: orchestrator
    Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
    Affected behavior: automated review handoff
    Highest-impact failure modes: author-context continuation; validation anchoring
    Changed boundaries: review invocation manifest and clean handoff
    Evidence expected: manifest fixture and validator result
    Areas requiring direct inspection: review record fields
    Areas intentionally out of scope: hosted review service
    Risk classes considered: contract mismatch=applicable; security/privacy boundary=not-applicable:no secret surface
    Falsifiable review questions: Does L0 fail closed? Does missing packet hash fail closed?
    Clean-review sufficiency receipt: yes
    Review target identity: git diff main...HEAD
    Governing artifacts inspected: specs/review-independence-and-criticality.md; docs/plans/example.md
    Adversarial hypotheses tested: same-context review fails closed; tests-only clean receipt fails closed
    Direct proofs performed: review artifact validator fixture
    Validation evidence challenged: validator only proves selected checks; receipt records evidence adequacy
    Unreviewed surfaces: hosted publication path
    Confidence: high
    No-finding rationale: Independent review gate fixture covers manifest, packet, phase, and sufficiency receipt fields.
    {extra}

    ## Findings

    No material findings.
    """


def valid_calibration_record_fields(extra_fields: str = "") -> str:
    extra = f"\n{extra_fields.strip()}\n" if extra_fields.strip() else ""
    return f"""
    Calibration record: yes
    Calibration record ID: calibration-code-review-standard-r1
    Review skill: code-review
    Fixture mode: public-defect-class
    Fixture corpus scope: defect-class-example-not-measured-corpus
    Sampling phase: rollout
    Sample rate: 20%
    Standard clean outcomes independently reviewed: 10
    Sample-rate reduction requested: no
    Second reviewer type: separate-agent
    Second review required: no
    Second-review disagreement: none
    Automatic continuation: no
    Critical authority kind: n/a
    Critical authority satisfied: no
    Recurrence detection: detected
    Novel defect detection: not-applicable
    Material disagreements: 0
    Severity disagreements: 0
    Evidence gaps: none
    Downstream escape: no
    False-positive rate: 0%
    Inconclusive rate: 0%
    Receipt quality: complete
    Review duration: PT12M
    {extra}
    """


def valid_requirement_compression_calibration_fields(extra_fields: str = "") -> str:
    extra = f"\n{extra_fields.strip()}\n" if extra_fields.strip() else ""
    return valid_calibration_record_fields(
        f"""
        Seeded defect family: requirement-compression
        Corpus iteration ID: rfg-compression-iteration-001
        Seed types covered: A+B+C compressed to A+B; N surfaces compressed to N-1; closed enum compressed; normative verbs compressed; multi-surface asymmetry; validator mirrors implementation
        Seed defect count: 6
        Expected finding IDs: R26-missing-recorded; N-surfaces-minus-one; closed-enum-six-of-seven; verbs-require-reject-without-record; surface-two-weakens-contract; validator-mirrors-approved-current
        Canonical R26 missing-recorded seed: yes
        Calibration result iteration ID: rfg-compression-iteration-001
        Sampling reason: reviewer-authored-decomposition
        Applicable receipt sample rate: 30%
        Reviewer-authored decomposition sample rate: 30%
        Not-applicable receipt sample rate: 5%
        Steady-state baseline sample rate: 5%
        Steady-state reviewer-authored sample rate: 15%
        Follow-on sampling amendment: none
        Not-applicable receipts in cycle: 5
        Not-applicable sampling proportional: yes
        Original not-applicable reason: change unrelated to normative contracts
        Audit outcome: correct
        Corrective action: none
        Rotation trigger: complete-defect-set-exposure
        Previous iteration ID: rfg-compression-iteration-000
        Next iteration ID: rfg-compression-iteration-002
        Rotated by: calibration-corpus-maintainer
        Rotation date: 2026-06-26
        {extra}
        """
    )


def valid_requirement_fidelity_fields(extra_fields: str = "") -> str:
    extra = f"\n{extra_fields.strip()}\n" if extra_fields.strip() else ""
    return f"""
    Requirement-fidelity gate: required
    Requirement-fidelity applicability: applicable
    Requirement-fidelity affected paths: skills/code-review/SKILL.md; scripts/test-review-artifact-validator.py
    Requirement-fidelity matched path triggers: skills/; scripts/*validator*
    Requirement-fidelity matched category triggers: skill instructions derived from specs; review-recording contracts
    Requirement-fidelity review stage: code-review
    Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence > prior findings
    Requirement-property decomposition evidence: present
    Requirement-fidelity receipt: yes
    Relevant spec clauses decomposed: yes
    Property matrix complete: yes
    Multi-surface contracts identified: yes
    Validator assertions checked against spec: yes
    Compressed requirement risk: none found
    Requirement-fidelity no-finding rationale: Decomposition and property matrix were checked against the cited spec clauses.
    {extra}
    """


T1_VALID_CASES = (
    ("l1-standard", "valid-automated-review-gate-l1"),
    ("l2-elevated", "valid-automated-review-gate"),
    ("l3-critical-internal", "valid-automated-review-gate-l3"),
)

T1_INVALID_CASES = (
    (
        "missing-context-separation",
        "invalid-missing-context-separation",
        "automated review gate missing required field Context separation mechanism",
    ),
    (
        "unsupported-independence-level",
        "invalid-unsupported-independence-level",
        "unsupported independence level 'L4'",
    ),
    (
        "unknown-native-review-status",
        "invalid-unknown-native-review-status",
        "unsupported native review status 'rubber-stamp'",
    ),
    (
        "missing-reviewer-context-id-unverifiable",
        "invalid-missing-reviewer-context-id-unverifiable-platform",
        "reviewer-context-id-required-on-unverifiable-platform",
    ),
)


def review_log_text(
    *,
    review_id: str,
    stage: str,
    status: str,
    detailed_record: str,
    material_findings: str = "None",
    open_findings: str = "None",
    round_value: str = "1",
) -> str:
    return f"""
    # Review Log

    ### Review entry
    Review ID: {review_id}
    Stage: {stage}
    Round: {round_value}
    Status: {status}
    Detailed record: {detailed_record}
    Resolution: review-resolution.md#{review_id}
    Material findings: {material_findings}
    Open findings: {open_findings}
    """


def resolution_text(*, review_id: str, finding_id: str) -> str:
    return f"""
    # Review Resolution

    Closeout status: open

    ### {review_id}

    Finding ID: {finding_id}
    Disposition: accepted
    Owner: implementer
    Owning stage: implement
    Chosen action: Preserve the upstream formal review record.
    Rationale: The finding changes tracked workflow evidence.
    Validation target: Run review artifact validator tests.
    """


def accepted_closed_resolution_text() -> str:
    return """
    # Review Resolution

    Closeout status: closed
    Review closeout: code-review-r1

    ### code-review-r1

    Finding ID: CR1-F1
    Disposition: accepted
    Owner: implementer
    Owning stage: implement
    Chosen action: Add direct validator coverage for the missing resolution entry case.
    Rationale: The review evidence identified a material Finding ID without guaranteed traceability.
    Validation target: Run the focused review artifact validator tests.
    Validation evidence: `python scripts/test-review-artifact-validator.py` passed.
    """


def accepted_closed_resolution_without_validation_text() -> str:
    return """
    # Review Resolution

    Closeout status: closed
    Review closeout: code-review-r1

    ### code-review-r1

    Finding ID: CR1-F1
    Disposition: accepted
    Owner: implementer
    Owning stage: implement
    Chosen action: Add direct validator coverage for the missing resolution entry case.
    Rationale: The review evidence identified a material Finding ID without guaranteed traceability.
    Validation target: Run the focused review artifact validator tests.
    """


def accepted_closed_resolution_with_disposition_text(disposition: str | None, *, duplicate: bool = False) -> str:
    disposition_block = "" if disposition is None else f"Disposition: {disposition}\n"
    duplicate_block = "Disposition: accepted\n" if duplicate else ""
    return f"""
    # Review Resolution

    Closeout status: closed
    Review closeout: code-review-r1

    ### code-review-r1

    Finding ID: CR1-F1
    {disposition_block}{duplicate_block}Owner: implementer
    Owning stage: implement
    Chosen action: Add direct validator coverage for malformed disposition state.
    Rationale: The review evidence identified a material Finding ID without guaranteed traceability.
    Validation target: Run the focused review artifact validator tests.
    Validation evidence: `python scripts/test-review-artifact-validator.py` passed.
    """


def accepted_resolution_without_closeout_status_text() -> str:
    return """
    # Review Resolution

    Review closeout: code-review-r1

    ### code-review-r1

    Finding ID: CR1-F1
    Disposition: accepted
    Owner: implementer
    Owning stage: implement
    Chosen action: Add direct validator coverage for malformed closeout state.
    Rationale: The review evidence identified a material Finding ID without guaranteed traceability.
    Validation target: Run the focused review artifact validator tests.
    Validation evidence: `python scripts/test-review-artifact-validator.py` passed.
    """


def scan_first_closed_resolution_text() -> str:
    return """
    # Review Resolution: Example Change

    ## Summary

    Closeout status: closed

    Review closeout: code-review-r1

    - Reviews covered: `code-review-r1`
    - Findings resolved: 1
    - Unresolved findings: 0
    - Final result: material code-review findings were accepted, resolved, and validated.

    ## Resolution Overview

    | Finding ID | Disposition | Status | Resolution summary |
    |---|---|---|---|
    | CR1-F1 | accepted | resolved | Added direct validator coverage for the missing resolution entry case. |

    ## Common Resolution Metadata

    - Owner: implementer
    - Owning stage: implement
    - Validation target: Run focused review artifact validator tests.
    - Validation evidence: `python scripts/test-review-artifact-validator.py` passed.

    ## Finding Details

    ### code-review-r1

    #### CR1-F1 - Missing resolution entry

    Finding ID: CR1-F1
    Disposition: accepted
    Status: resolved
    Owner: implementer
    Owning stage: implement
    Chosen action: Add direct validator coverage for the missing resolution entry case.
    Rationale: The review evidence identified a material Finding ID without guaranteed traceability.
    Validation target: Covered by common resolution metadata.
    Validation evidence: Covered by shared validation evidence.

    ## Shared Validation Evidence

    | Validation area | Result | Notes |
    |---|---|---|
    | Review artifact validator | pass | `python scripts/test-review-artifact-validator.py` passed. |

    ## Closeout Checklist

    - [x] Every material finding has a disposition.
    - [x] Every accepted finding has a chosen action.
    - [x] Every accepted finding has validation evidence.
    - [x] No findings remain open.
    """


def rejected_closed_resolution_text() -> str:
    return """
    # Review Resolution

    Closeout status: closed

    ### code-review-r1

    Finding ID: CR1-F1
    Disposition: rejected
    Owner: maintainer
    Owning stage: code-review
    Stop state: no change required
    Rationale: The finding is already satisfied by existing validator coverage.
    Expected proof: Reviewer confirms the cited coverage exists.
    """


def deferred_closed_resolution_text() -> str:
    return """
    # Review Resolution

    Closeout status: closed

    ### code-review-r1

    Finding ID: CR1-F1
    Disposition: deferred
    Owner: maintainer
    Owning stage: follow-up
    Stop state: deferred to a separate change
    Rationale: The finding is useful but outside this milestone.
    Validation target: Follow-up issue records owner and scope.
    """


def partially_accepted_closed_resolution_text() -> str:
    return """
    # Review Resolution

    Closeout status: closed

    ### code-review-r1

    Finding ID: CR1-F1
    Disposition: partially-accepted
    Owner: implementer
    Owning stage: implement
    Accepted portion: Add focused validator coverage.
    Rejected or deferred portion: Defer broad historical artifact migration.
    Rationale: Historical migration is outside this milestone.
    Validation target: Focused validator tests and recorded follow-up rationale.
    Validation evidence: `python scripts/test-review-artifact-validator.py` passed.
    """


class ReviewArtifactValidatorFixtureTests(unittest.TestCase):
    maxDiff = None

    def addCleanupTree(self, path: Path) -> None:
        self.addCleanup(lambda: shutil.rmtree(path, ignore_errors=True))

    def validate(self, change_root: Path):
        return validate_change_root(change_root, mode="structure")

    def validateCloseout(self, change_root: Path):
        return validate_change_root(change_root, mode="closeout")

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

    def assertCloseoutPasses(self, change_root: Path) -> None:
        result = self.validateCloseout(change_root)
        self.assertFalse(
            result.blocking_findings,
            msg="\n".join(f.message for f in result.blocking_findings),
        )

    def assertCloseoutFails(self, change_root: Path, expected_text: str) -> None:
        result = self.validateCloseout(change_root)
        combined = "\n".join(f.message for f in result.blocking_findings)
        self.assertTrue(result.blocking_findings, msg="expected closeout validation to fail")
        self.assertIn(expected_text, combined)

    def fixture(self) -> Path:
        root = copy_fixture()
        self.addCleanupTree(root)
        return root

    def clean_receipt_fixture(self) -> Path:
        root = copy_fixture("valid-clean-receipt-root")
        self.addCleanupTree(root)
        return root

    def write_closure_fixture(
        self,
        root: Path,
        *,
        log_open: bool = False,
        resolution_text_value: str | None = None,
        later_reopen: bool = False,
    ) -> None:
        write_text(
            root / "reviews" / "code-review-r1.md",
            review_text(
                review_id="code-review-r1",
                stage="code-review",
                status="changes-requested",
                finding_id="CR1-F1",
            ),
        )
        log_text = valid_log_text(open_findings="CR1-F1" if log_open else "None")
        if later_reopen:
            log_text += """

            ### Review entry
            Review ID: code-review-r2
            Stage: code-review
            Round: 2
            Status: changes-requested
            Detailed record: reviews/code-review-r2.md
            Resolution: review-resolution.md#code-review-r2
            Material findings: CR1-F1
            Open findings: CR1-F1
            """
            write_text(
                root / "reviews" / "code-review-r2.md",
                review_text(
                    review_id="code-review-r2",
                    stage="code-review",
                    status="changes-requested",
                    finding_id="CR1-F1",
                ),
            )
        write_text(root / "review-log.md", log_text)
        write_text(root / "review-resolution.md", resolution_text_value or accepted_closed_resolution_text())

    def assertSummaryOpen(self, root: Path) -> None:
        summary = summarize_review_evidence(root)
        self.assertEqual(summary.open_finding_ids, ("CR1-F1",))

    def assertSummaryClosed(self, root: Path) -> None:
        summary = summarize_review_evidence(root)
        self.assertEqual(summary.open_finding_ids, ())
        self.assertEqual(summary.closed_count, 1)

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

    def test_closed_status_missing_validation_keeps_finding_open(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-closed-missing-validation-"))
        self.addCleanupTree(root)
        self.write_closure_fixture(
            root,
            log_open=True,
            resolution_text_value=accepted_closed_resolution_without_validation_text(),
        )

        self.assertSummaryOpen(root)
        self.assertCloseoutFails(root, "accepted finding missing validation evidence")

    def test_accepted_resolution_missing_action_keeps_finding_open(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-accepted-missing-action-"))
        self.addCleanupTree(root)
        self.write_closure_fixture(root, resolution_text_value=accepted_closed_resolution_text().replace(
            "Chosen action: Add direct validator coverage for the missing resolution entry case.\n",
            "",
        ))

        self.assertSummaryOpen(root)
        self.assertCloseoutFails(root, "accepted finding missing chosen action")

    def test_missing_disposition_keeps_finding_open(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-missing-disposition-"))
        self.addCleanupTree(root)
        self.write_closure_fixture(
            root,
            resolution_text_value=accepted_closed_resolution_with_disposition_text(None),
        )

        self.assertSummaryOpen(root)
        self.assertCloseoutFails(root, "resolution entry missing disposition")

    def test_unsupported_disposition_keeps_finding_open(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-unsupported-disposition-"))
        self.addCleanupTree(root)
        self.write_closure_fixture(
            root,
            resolution_text_value=accepted_closed_resolution_with_disposition_text("deferred-to-next-quarter"),
        )

        self.assertSummaryOpen(root)
        self.assertCloseoutFails(root, "unsupported disposition")

    def test_multiple_dispositions_keep_finding_open(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-duplicate-disposition-"))
        self.addCleanupTree(root)
        self.write_closure_fixture(
            root,
            resolution_text_value=accepted_closed_resolution_with_disposition_text("accepted", duplicate=True),
        )

        self.assertSummaryOpen(root)
        self.assertCloseoutFails(root, "disposition must appear exactly once")

    def test_missing_closeout_status_keeps_finding_open(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-missing-closeout-status-"))
        self.addCleanupTree(root)
        self.write_closure_fixture(root, resolution_text_value=accepted_resolution_without_closeout_status_text())

        self.assertSummaryOpen(root)
        self.assertCloseoutFails(root, "closeout status is missing or invalid")

    def test_all_blockers_surface_in_one_round(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-all-blockers-"))
        self.addCleanupTree(root)
        resolution_text_value = accepted_closed_resolution_with_disposition_text(None).replace(
            "Validation evidence: `python scripts/test-review-artifact-validator.py` passed.\n",
            "",
        )
        self.write_closure_fixture(root, resolution_text_value=resolution_text_value)

        result = self.validateCloseout(root)
        combined = "\n".join(f.message for f in result.blocking_findings)
        self.assertIn("resolution entry missing disposition", combined)
        self.assertIn("finding closeout missing validation evidence", combined)

    def test_later_review_reopen_overrides_closed_status(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-later-reopen-"))
        self.addCleanupTree(root)
        self.write_closure_fixture(root, later_reopen=True)

        self.assertSummaryOpen(root)
        self.assertCloseoutFails(root, "review-log Open findings must be empty for closed closeout")

    def test_full_closeout_summary_passes(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-full-closeout-"))
        self.addCleanupTree(root)
        self.write_closure_fixture(root)

        self.assertSummaryClosed(root)
        self.assertCloseoutPasses(root)

    def test_predicate_parity_with_closeout_mode(self) -> None:
        cases = [
            ("missing-validation", True, accepted_closed_resolution_without_validation_text(), False),
            (
                "missing-action",
                False,
                accepted_closed_resolution_text().replace(
                    "Chosen action: Add direct validator coverage for the missing resolution entry case.\n",
                    "",
                ),
                False,
            ),
            ("missing-disposition", False, accepted_closed_resolution_with_disposition_text(None), False),
            (
                "unsupported-disposition",
                False,
                accepted_closed_resolution_with_disposition_text("deferred-to-next-quarter"),
                False,
            ),
            ("duplicate-disposition", False, accepted_closed_resolution_with_disposition_text("accepted", duplicate=True), False),
            ("missing-closeout-status", False, accepted_resolution_without_closeout_status_text(), False),
            ("later-reopen", False, accepted_closed_resolution_text(), True),
            ("full-closeout", False, accepted_closed_resolution_text(), False),
        ]
        for name, log_open, resolution_text_value, later_reopen in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-parity-{name}-"))
                self.addCleanupTree(root)
                self.write_closure_fixture(
                    root,
                    log_open=log_open,
                    resolution_text_value=resolution_text_value,
                    later_reopen=later_reopen,
                )
                closeout = self.validateCloseout(root)
                summary = summarize_review_evidence(root)
                state = "open" if summary.open_finding_ids else "closed"
                self.assertEqual(
                    state,
                    "open" if closeout.blocking_findings else "closed",
                    msg="\n".join(f.message for f in closeout.blocking_findings),
                )

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

    def test_clean_receipt_table_log_passes_without_resolution(self) -> None:
        root = self.clean_receipt_fixture()
        result = self.validate(root)
        self.assertFalse(result.blocking_findings)
        self.assertEqual(result.review_count, 1)
        self.assertEqual(result.finding_count, 0)
        self.assertEqual(result.review_log_entry_count, 1)
        self.assertEqual(result.resolution_entry_count, 0)

        cli_result = run_cli(root)
        self.assertEqual(
            cli_result.returncode,
            0,
            msg=f"stdout:\n{cli_result.stdout}\nstderr:\n{cli_result.stderr}",
        )

    def test_clean_receipt_table_requires_matching_record_and_zero_material_count(self) -> None:
        root = self.clean_receipt_fixture()
        log_text = (root / "review-log.md").read_text(encoding="utf-8")
        (root / "review-log.md").write_text(
            log_text.replace("reviews/spec-review-r1.md", "reviews/missing.md"),
            encoding="utf-8",
        )
        self.assertFails(root, "Record does not match review file")

        root = self.clean_receipt_fixture()
        log_text = (root / "review-log.md").read_text(encoding="utf-8")
        (root / "review-log.md").write_text(
            log_text.replace("| approved | 0 | recorded |", "| approved | 1 | recorded |"),
            encoding="utf-8",
        )
        self.assertFails(root, "clean receipt Material findings must be 0")

    def test_clean_receipt_table_requires_recorded_status(self) -> None:
        root = self.clean_receipt_fixture()
        log_text = (root / "review-log.md").read_text(encoding="utf-8")
        (root / "review-log.md").write_text(
            log_text.replace("| approved | 0 | recorded |", "| approved | 0 | blocked |"),
            encoding="utf-8",
        )
        self.assertFails(root, "clean receipt Recording must be recorded")

    def test_clean_receipt_review_file_requires_receipt_metadata(self) -> None:
        root = self.clean_receipt_fixture()
        drop_field(root / "reviews" / "spec-review-r1.md", "Reviewed artifact")
        self.assertFails(root, "clean receipt missing required field Reviewed artifact")

        root = self.clean_receipt_fixture()
        replace_field(root / "reviews" / "spec-review-r1.md", "Recording status", "blocked")
        self.assertFails(root, "clean receipt Recording status must be recorded")

    def test_automated_review_gate_manifest_and_clean_receipt_passes(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-gate-valid-"))
        self.addCleanupTree(root)
        write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text())
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )

        self.assertPasses(root)

    def test_review_gate_rejects_missing_native_review_status(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-missing-native-status-"))
        self.addCleanupTree(root)
        review = "\n".join(
            line
            for line in valid_automated_review_text().splitlines()
            if not line.strip().startswith("Native review status:")
        )
        write_text(root / "reviews" / "code-review-r1.md", review)
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        self.assertFails(root, "automated review gate missing required field Native review status")

    def test_review_gate_rejects_empty_native_review_status(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-empty-native-status-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "code-review-r1.md",
            valid_automated_review_text().replace("Native review status: clean-with-notes", "Native review status:"),
        )
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        self.assertFails(root, "automated review gate missing required field Native review status")

    def test_review_gate_rejects_mismatched_native_and_derived_status(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-native-derived-mismatch-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "code-review-r1.md",
            valid_automated_review_text().replace("Review gate outcome: advance", "Review gate outcome: stop"),
        )
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        self.assertFails(root, "R12-mismatch")

    def test_review_gate_rejects_unknown_native_review_status(self) -> None:
        for native_status in ("rubber-stamp", "lgtm", "bogus"):
            with self.subTest(native_status=native_status):
                root = Path(tempfile.mkdtemp(prefix="review-artifact-unknown-native-status-"))
                self.addCleanupTree(root)
                write_text(
                    root / "reviews" / "code-review-r1.md",
                    valid_automated_review_text().replace(
                        "Native review status: clean-with-notes",
                        f"Native review status: {native_status}",
                    ),
                )
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, f"unsupported native review status '{native_status}'")

    def test_review_gate_unknown_native_status_error_lists_allowed_values(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-unknown-native-status-allowed-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "code-review-r1.md",
            valid_automated_review_text().replace(
                "Native review status: clean-with-notes",
                "Native review status: rubber-stamp",
            ),
        )
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        for allowed in ("approved", "blocked", "changes-requested", "clean-with-notes", "inconclusive"):
            self.assertFails(root, allowed)

    def test_automated_review_gate_fixtures_cover_valid_and_fail_closed_paths(self) -> None:
        valid_root = copy_fixture("valid-automated-review-gate")
        self.addCleanupTree(valid_root)
        self.assertPasses(valid_root)

        invalid_root = copy_fixture("invalid-automated-review-gate-l0")
        self.addCleanupTree(invalid_root)
        self.assertFails(invalid_root, "automated review gate cannot advance with L0")
        self.assertFails(invalid_root, "reviewer_context_id must differ from author_context_id")
        self.assertFails(invalid_root, "phase receipt evidence-menu-released appears before required predecessor risk-map-recorded")

        missing_fidelity_root = copy_fixture("invalid-workflow-managed-missing-fidelity-applicability")
        self.addCleanupTree(missing_fidelity_root)
        self.assertFails(missing_fidelity_root, "fidelity-applicability-missing")

    def test_t1_valid_independence_levels_pass(self) -> None:
        for name, fixture in T1_VALID_CASES:
            with self.subTest(name=name):
                root = copy_fixture(fixture)
                self.addCleanupTree(root)
                self.assertPasses(root)

    def test_t1_invalid_independence_cases_fail_closed(self) -> None:
        for name, fixture, expected in T1_INVALID_CASES:
            with self.subTest(name=name):
                root = copy_fixture(fixture)
                self.addCleanupTree(root)
                self.assertFails(root, expected)

    def test_automated_review_gate_rejects_invalid_independence_and_packet_evidence(self) -> None:
        cases = [
            (
                "l0-advance",
                "Independence level: L1",
                "Independence level: L0",
                "automated review gate cannot advance with L0",
            ),
            (
                "same-context",
                "Reviewer context ID: reviewer-ctx-1",
                "Reviewer context ID: author-ctx-1",
                "reviewer_context_id must differ from author_context_id",
            ),
            (
                "missing-inventory",
                "Initial packet inventory: specs/review-independence-and-criticality.md@abc123#sha256:1111111111111111111111111111111111111111111111111111111111111111; docs/plans/example.md@abc123#sha256:2222222222222222222222222222222222222222222222222222222222222222\n",
                "",
                "automated review gate missing required field Initial packet inventory",
            ),
            (
                "missing-packet-hash",
                "Initial packet hash: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n",
                "",
                "automated review gate missing required field Initial packet hash",
            ),
            (
                "attestation-only",
                "Initial packet inventory: specs/review-independence-and-criticality.md@abc123#sha256:1111111111111111111111111111111111111111111111111111111111111111; docs/plans/example.md@abc123#sha256:2222222222222222222222222222222222222222222222222222222222222222",
                "Author context excluded: true",
                "author_context_excluded is not sufficient initial-packet proof",
            ),
        ]
        for name, old, new, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-gate-{name}-"))
                self.addCleanupTree(root)
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text().replace(old, new))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_automated_review_gate_rejects_forbidden_context_and_bad_phase_order(self) -> None:
        cases = [
            (
                "forbidden-label",
                None,
                "Author self-assessment: looks correct",
                "forbidden automated-review context field Author self-assessment",
            ),
            (
                "forbidden-initial-packet-token",
                None,
                "Initial packet contains: validation-result summaries",
                "initial packet contains prohibited context validation-result summaries",
            ),
            (
                "bad-phase-order",
                "Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded",
                "Phase receipts: evidence-menu-released > risk-map-recorded > evidence-results-released > prior-findings-released > verdict-recorded",
                "phase receipt evidence-menu-released appears before required predecessor risk-map-recorded",
            ),
            (
                "unbounded-manifest-notes",
                None,
                "Manifest notes: " + ("x" * 300),
                "automated review gate field Manifest notes is too long",
            ),
        ]
        for name, old, extra, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-gate-{name}-"))
                self.addCleanupTree(root)
                review_text_value = valid_automated_review_text(extra if old is None else "")
                if old is not None:
                    review_text_value = review_text_value.replace(old, extra)
                write_text(root / "reviews" / "code-review-r1.md", review_text_value)
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_automated_clean_review_requires_sufficiency_receipt_fields(self) -> None:
        cases = [
            ("Risk classes considered", "clean sufficiency receipt missing required field Risk classes considered"),
            ("Adversarial hypotheses tested", "clean sufficiency receipt missing required field Adversarial hypotheses tested"),
            ("Direct proofs performed", "clean sufficiency receipt missing required field Direct proofs performed"),
            ("Validation evidence challenged", "clean sufficiency receipt missing required field Validation evidence challenged"),
            ("Unreviewed surfaces", "clean sufficiency receipt missing required field Unreviewed surfaces"),
            ("No-finding rationale", "clean sufficiency receipt missing required field No-finding rationale"),
        ]
        for field, expected in cases:
            with self.subTest(field=field):
                root = Path(tempfile.mkdtemp(prefix="review-artifact-clean-receipt-"))
                self.addCleanupTree(root)
                review = "\n".join(
                    line
                    for line in valid_automated_review_text().splitlines()
                    if not line.strip().startswith(f"{field}:")
                )
                write_text(root / "reviews" / "code-review-r1.md", review)
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_requirement_fidelity_applicable_clean_review_receipt_passes(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-rfg-valid-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "code-review-r1.md",
            valid_automated_review_text(valid_requirement_fidelity_fields()),
        )
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )

        self.assertPasses(root)

    def test_requirement_fidelity_gate_in_force_requires_applicability(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-rfg-missing-applicability-"))
        self.addCleanupTree(root)
        fidelity = valid_requirement_fidelity_fields()
        review = "\n".join(
            line
            for line in valid_automated_review_text(fidelity).splitlines()
            if not line.strip().startswith("Requirement-fidelity applicability:")
        )
        write_text(root / "reviews" / "code-review-r1.md", review)
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )

        self.assertFails(root, "fidelity-applicability-missing")

    def test_requirement_fidelity_manifest_unknown_values_fail_closed(self) -> None:
        cases = [
            (
                "unknown-gate-marker",
                "Requirement-fidelity gate: required",
                "Requirement-fidelity gate: optional",
                "unsupported requirement-fidelity gate marker 'optional'",
            ),
            (
                "unknown-applicability",
                "Requirement-fidelity applicability: applicable",
                "Requirement-fidelity applicability: maybe",
                "unsupported requirement-fidelity applicability 'maybe'",
            ),
            (
                "unknown-path-trigger",
                "Requirement-fidelity matched path triggers: skills/; scripts/*validator*",
                "Requirement-fidelity matched path triggers: random/",
                "unsupported requirement-fidelity path trigger 'random/'",
            ),
            (
                "unknown-category-trigger",
                "Requirement-fidelity matched category triggers: skill instructions derived from specs; review-recording contracts",
                "Requirement-fidelity matched category triggers: vibes",
                "unsupported requirement-fidelity category trigger 'vibes'",
            ),
            (
                "unknown-override-direction",
                None,
                "Requirement-fidelity override direction: shrug",
                "unsupported requirement-fidelity override direction 'shrug'",
            ),
            (
                "free-form-not-applicable",
                "Requirement-fidelity applicability: applicable",
                "Requirement-fidelity applicability: not-applicable\nRequirement-fidelity not-applicable reason: just docs",
                "unsupported requirement-fidelity not-applicable reason 'just docs'",
            ),
        ]
        for name, old, new, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-rfg-{name}-"))
                self.addCleanupTree(root)
                extra = valid_requirement_fidelity_fields()
                review = valid_automated_review_text(extra)
                if old is None:
                    review = valid_automated_review_text(extra + "\n" + new)
                else:
                    review = review.replace(old, new)
                write_text(root / "reviews" / "code-review-r1.md", review)
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_requirement_fidelity_applicable_review_requires_spec_first_and_receipt_evidence(self) -> None:
        cases = [
            (
                "implementation-first",
                "Requirement-fidelity packet order: spec clause > decomposition > expected surfaces > implementation diff > validator assertions > validation evidence > prior findings",
                "Requirement-fidelity packet order: implementation diff > spec clause > validator assertions",
                "requirement-fidelity packet order must start with spec clause",
            ),
            (
                "missing-decomposition-evidence",
                "Requirement-property decomposition evidence: present\n",
                "",
                "requirement-fidelity receipt says clauses were decomposed but decomposition evidence is missing",
            ),
            (
                "validator-not-compared",
                "Validator assertions checked against spec: yes",
                "Validator assertions checked against spec: no",
                "requirement-fidelity receipt field Validator assertions checked against spec must be yes",
            ),
            (
                "missing-no-finding-rationale",
                "Requirement-fidelity no-finding rationale: Decomposition and property matrix were checked against the cited spec clauses.\n",
                "",
                "requirement-fidelity receipt missing required field Requirement-fidelity no-finding rationale",
            ),
        ]
        for name, old, new, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-rfg-{name}-"))
                self.addCleanupTree(root)
                write_text(
                    root / "reviews" / "code-review-r1.md",
                    valid_automated_review_text(valid_requirement_fidelity_fields()).replace(old, new),
                )
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_requirement_fidelity_not_applicable_requires_closed_reason_and_skips_clean_receipt(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-rfg-not-applicable-"))
        self.addCleanupTree(root)
        fidelity = """
        Requirement-fidelity applicability: not-applicable
        Requirement-fidelity affected paths: docs/example.md
        Requirement-fidelity matched path triggers: none
        Requirement-fidelity matched category triggers: none
        Requirement-fidelity review stage: code-review
        Requirement-fidelity not-applicable reason: change unrelated to normative contracts
        """
        write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(fidelity))
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )

        self.assertPasses(root)

    def test_calibration_record_shape_and_sampling_fields_pass(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-valid-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "code-review-r1.md",
            valid_automated_review_text(valid_calibration_record_fields()),
        )
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        self.assertPasses(root)

    def test_calibration_public_defect_class_fixture_passes(self) -> None:
        root = copy_fixture("valid-calibration-public-defect-class")
        self.addCleanupTree(root)
        self.assertPasses(root)

    def test_requirement_compression_public_calibration_fixture_passes(self) -> None:
        root = copy_fixture("valid-requirement-compression-calibration")
        self.addCleanupTree(root)
        self.assertPasses(root)

    def test_calibration_record_requires_metric_fields_by_skill_and_tier(self) -> None:
        cases = (
            ("Review skill", "calibration record missing required field Review skill"),
            ("Recurrence detection", "calibration record missing required field Recurrence detection"),
            ("Novel defect detection", "calibration record missing required field Novel defect detection"),
            ("Second-review disagreement", "calibration record missing required field Second-review disagreement"),
            ("Downstream escape", "calibration record missing required field Downstream escape"),
            ("False-positive rate", "calibration record missing required field False-positive rate"),
            ("Inconclusive rate", "calibration record missing required field Inconclusive rate"),
            ("Receipt quality", "calibration record missing required field Receipt quality"),
            ("Review duration", "calibration record missing required field Review duration"),
        )
        for field, expected in cases:
            with self.subTest(field=field):
                root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-missing-"))
                self.addCleanupTree(root)
                calibration = "\n".join(
                    line
                    for line in valid_calibration_record_fields().splitlines()
                    if not line.strip().startswith(f"{field}:")
                )
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_calibration_record_rejects_unknown_skill_and_risk_tier(self) -> None:
        cases = (
            (
                "unknown-review-skill",
                "Review skill: code-review",
                "Review skill: rubber-stamp-review",
                "unsupported calibration review skill 'rubber-stamp-review'",
            ),
            (
                "unknown-risk-tier",
                "Risk tier: standard",
                "Risk tier: ambiguous",
                "unsupported calibration risk tier 'ambiguous'",
            ),
        )
        for name, old, new, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-calibration-{name}-"))
                self.addCleanupTree(root)
                review = valid_automated_review_text(valid_calibration_record_fields()).replace(old, new)
                write_text(root / "reviews" / "code-review-r1.md", review)
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_calibration_record_rejects_sampling_floor_and_early_reduction(self) -> None:
        cases = (
            (
                "below-standard-rollout-rate",
                valid_calibration_record_fields().replace("Sample rate: 20%", "Sample rate: 19%"),
                "standard-risk rollout sample rate must be at least 20%",
            ),
            (
                "early-sample-rate-reduction",
                valid_calibration_record_fields()
                .replace("Standard clean outcomes independently reviewed: 10", "Standard clean outcomes independently reviewed: 9")
                .replace("Sample-rate reduction requested: no", "Sample-rate reduction requested: yes"),
                "standard-risk sampling reduction requires at least 10 independently reviewed clean outcomes",
            ),
        )
        for name, calibration, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-calibration-{name}-"))
                self.addCleanupTree(root)
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_calibration_record_rejects_elevated_clean_without_second_review(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-elevated-no-second-"))
        self.addCleanupTree(root)
        calibration = valid_calibration_record_fields().replace("Second review required: no", "Second review required: no")
        review = valid_automated_review_text(calibration).replace("Risk tier: standard", "Risk tier: elevated")
        write_text(root / "reviews" / "code-review-r1.md", review)
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        self.assertFails(root, "elevated-risk clean review requires second review at 100%")

    def test_calibration_record_rejects_critical_authority_gaps(self) -> None:
        cases = (
            (
                "critical-internal-without-authority",
                valid_automated_review_text(valid_calibration_record_fields())
                .replace("Risk tier: standard", "Risk tier: critical-internal")
                .replace("Independence level: L2", "Independence level: L1"),
                "calibration-authority-missing",
            ),
            (
                "irreversible-external-with-l3-only",
                valid_automated_review_text(valid_calibration_record_fields())
                .replace("Risk tier: standard", "Risk tier: irreversible-external-action")
                .replace("Critical authority kind: n/a", "Critical authority kind: L3")
                .replace("Critical authority satisfied: no", "Critical authority satisfied: yes"),
                "calibration-authority-kind-insufficient",
            ),
            (
                "invalid-authority-kind",
                valid_automated_review_text(valid_calibration_record_fields())
                .replace("Risk tier: standard", "Risk tier: critical-internal")
                .replace("Critical authority kind: n/a", "Critical authority kind: banana")
                .replace("Critical authority satisfied: no", "Critical authority satisfied: yes"),
                "calibration-authority-kind-invalid",
            ),
            (
                "standard-authority-kind-not-applicable",
                valid_automated_review_text(valid_calibration_record_fields())
                .replace("Critical authority kind: n/a", "Critical authority kind: L3")
                .replace("Critical authority satisfied: no", "Critical authority satisfied: yes"),
                "calibration-authority-kind-not-applicable",
            ),
        )
        for name, calibration, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-calibration-{name}-"))
                self.addCleanupTree(root)
                write_text(root / "reviews" / "code-review-r1.md", calibration)
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

        for name, calibration in (
            (
                "critical-internal-with-l3",
                valid_automated_review_text(valid_calibration_record_fields())
                .replace("Risk tier: standard", "Risk tier: critical-internal")
                .replace("Independence level: L2", "Independence level: L3")
                .replace("Critical authority kind: n/a", "Critical authority kind: L3")
                .replace("Critical authority satisfied: no", "Critical authority satisfied: yes"),
            ),
            (
                "irreversible-external-with-human",
                valid_automated_review_text(valid_calibration_record_fields())
                .replace("Risk tier: standard", "Risk tier: irreversible-external-action")
                .replace("Critical authority kind: n/a", "Critical authority kind: human")
                .replace("Critical authority satisfied: no", "Critical authority satisfied: yes"),
            ),
        ):
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-calibration-{name}-"))
                self.addCleanupTree(root)
                write_text(root / "reviews" / "code-review-r1.md", calibration)
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertPasses(root)

    def test_calibration_boolean_fields_reject_unsupported_values(self) -> None:
        for field in (
            "Sample-rate reduction requested",
            "Second review required",
            "Automatic continuation",
            "Critical authority satisfied",
        ):
            with self.subTest(field=field):
                root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-boolean-"))
                self.addCleanupTree(root)
                calibration = valid_calibration_record_fields().replace(f"{field}: no", f"{field}: banana")
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, f"calibration-control-value-invalid: {field}")

    def test_calibration_boolean_fields_report_each_invalid_value(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-booleans-"))
        self.addCleanupTree(root)
        calibration = (
            valid_calibration_record_fields()
            .replace("Sample-rate reduction requested: no", "Sample-rate reduction requested: banana")
            .replace("Second review required: no", "Second review required: maybe")
            .replace("Automatic continuation: no", "Automatic continuation: 1")
            .replace("Critical authority satisfied: no", "Critical authority satisfied: later")
        )
        write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        result = self.validate(root)
        combined = "\n".join(f.message for f in result.blocking_findings)
        for field in (
            "Sample-rate reduction requested",
            "Second review required",
            "Automatic continuation",
            "Critical authority satisfied",
        ):
            self.assertIn(f"calibration-control-value-invalid: {field}", combined)

    def test_calibration_authority_fixtures_cover_valid_and_fail_closed_paths(self) -> None:
        for fixture in (
            "valid-calibration-critical-internal-l3",
            "valid-calibration-irreversible-external-human",
        ):
            with self.subTest(fixture=fixture):
                self.assertPasses(FIXTURES / fixture)
        for fixture, expected in (
            ("invalid-calibration-critical-internal-missing-authority", "calibration-authority-missing"),
            ("invalid-calibration-irreversible-external-l3-only", "calibration-authority-kind-insufficient"),
            ("invalid-calibration-critical-internal-authority-kind-banana", "calibration-authority-kind-invalid"),
        ):
            with self.subTest(fixture=fixture):
                self.assertFails(FIXTURES / fixture, expected)

    def test_calibration_authority_kind_invalid_does_not_emit_missing(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-authority-kind-invalid-"))
        self.addCleanupTree(root)
        review = (
            valid_automated_review_text(valid_calibration_record_fields())
            .replace("Risk tier: standard", "Risk tier: critical-internal")
            .replace("Critical authority kind: n/a", "Critical authority kind: banana")
            .replace("Critical authority satisfied: no", "Critical authority satisfied: yes")
        )
        write_text(root / "reviews" / "code-review-r1.md", review)
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        result = self.validate(root)
        combined = "\n".join(f.message for f in result.blocking_findings)
        self.assertIn("calibration-authority-kind-invalid", combined)
        self.assertNotIn("calibration-authority-missing", combined)
        self.assertNotIn("calibration-authority-kind-insufficient", combined)

    def test_calibration_record_rejects_second_review_disagreement_continuation(self) -> None:
        for disagreement in ("material-finding", "blocked", "inconclusive"):
            with self.subTest(disagreement=disagreement):
                root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-disagreement-"))
                self.addCleanupTree(root)
                calibration = (
                    valid_calibration_record_fields()
                    .replace("Second-review disagreement: none", f"Second-review disagreement: {disagreement}")
                    .replace("Automatic continuation: no", "Automatic continuation: yes")
                )
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, "second-review disagreement prevents automatic continuation")

    def test_calibration_record_requires_downstream_escape_details(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-escape-"))
        self.addCleanupTree(root)
        calibration = valid_calibration_record_fields().replace("Downstream escape: no", "Downstream escape: yes")
        write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        self.assertFails(root, "downstream escape record missing required field Downstream escape stage")
        self.assertFails(root, "downstream escape record missing required field Downstream escape analysis")

    def test_calibration_public_fixture_declares_not_measured_corpus(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-calibration-public-scope-"))
        self.addCleanupTree(root)
        calibration = "\n".join(
            line
            for line in valid_calibration_record_fields().splitlines()
            if not line.strip().startswith("Fixture corpus scope:")
        )
        write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )
        self.assertFails(root, "public calibration fixture must declare defect-class-example-not-measured-corpus")

    def test_requirement_compression_calibration_record_passes(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-rfg-calibration-valid-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "code-review-r1.md",
            valid_automated_review_text(valid_requirement_compression_calibration_fields()),
        )
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )

        self.assertPasses(root)

    def test_requirement_compression_calibration_rejects_incomplete_corpus(self) -> None:
        cases = (
            (
                "too-few-defects",
                "Seed defect count: 6",
                "Seed defect count: 5",
                "requirement-compression corpus iteration must contain at least six defects",
            ),
            (
                "too-few-seed-types",
                (
                    "Seed types covered: A+B+C compressed to A+B; N surfaces compressed to N-1; "
                    "closed enum compressed; normative verbs compressed; multi-surface asymmetry; "
                    "validator mirrors implementation"
                ),
                (
                    "Seed types covered: A+B+C compressed to A+B; N surfaces compressed to N-1; "
                    "closed enum compressed"
                ),
                "requirement-compression corpus iteration must span at least four seed types",
            ),
            (
                "unknown-seed-type",
                "validator mirrors implementation",
                "validator agrees with vibes",
                "unsupported requirement-compression seed type 'validator agrees with vibes'",
            ),
            (
                "missing-canonical-r26",
                "Canonical R26 missing-recorded seed: yes",
                "Canonical R26 missing-recorded seed: no",
                "requirement-compression corpus must include canonical R26 missing-recorded seed",
            ),
        )
        for name, old, new, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-rfg-calibration-{name}-"))
                self.addCleanupTree(root)
                calibration = valid_requirement_compression_calibration_fields().replace(old, new)
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_requirement_compression_calibration_rejects_sampling_floor_gaps(self) -> None:
        cases = (
            (
                "baseline-below-phase-b-floor",
                "Applicable receipt sample rate: 30%",
                "Applicable receipt sample rate: 9%",
                "applicable fidelity receipt sample rate must be at least 10% during Phase B",
            ),
            (
                "reviewer-authored-below-phase-b-floor",
                "Reviewer-authored decomposition sample rate: 30%",
                "Reviewer-authored decomposition sample rate: 29%",
                "reviewer-authored decomposition sample rate must be at least 30% during Phase B",
            ),
            (
                "not-applicable-below-floor",
                "Not-applicable receipt sample rate: 5%",
                "Not-applicable receipt sample rate: 4%",
                "not-applicable receipt sample rate must be at least 5% during Phase B",
            ),
            (
                "steady-baseline-below-floor",
                "Steady-state baseline sample rate: 5%",
                "Steady-state baseline sample rate: 4%",
                "steady-state baseline sample rate cannot drop below 5% without follow-on amendment",
            ),
            (
                "steady-reviewer-authored-below-floor",
                "Steady-state reviewer-authored sample rate: 15%",
                "Steady-state reviewer-authored sample rate: 14%",
                "steady-state reviewer-authored sample rate cannot drop below 15% without follow-on amendment",
            ),
        )
        for name, old, new, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-rfg-sampling-{name}-"))
                self.addCleanupTree(root)
                calibration = valid_requirement_compression_calibration_fields().replace(old, new)
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_requirement_compression_calibration_rejects_unknown_closed_values(self) -> None:
        cases = (
            (
                "unknown-sampling-reason",
                "Sampling reason: reviewer-authored-decomposition",
                "Sampling reason: vibes",
                "unsupported requirement-compression sampling reason 'vibes'",
            ),
            (
                "unknown-audit-outcome",
                "Audit outcome: correct",
                "Audit outcome: maybe",
                "unsupported requirement-compression audit outcome 'maybe'",
            ),
            (
                "unknown-rotation-trigger",
                "Rotation trigger: complete-defect-set-exposure",
                "Rotation trigger: vibes",
                "unsupported requirement-compression rotation trigger 'vibes'",
            ),
        )
        for name, old, new, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-rfg-closed-{name}-"))
                self.addCleanupTree(root)
                calibration = valid_requirement_compression_calibration_fields().replace(old, new)
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_requirement_compression_misclassified_audit_rejects_trivial_corrective_action(self) -> None:
        cases = (
            ("none", "Corrective action: none", "Corrective action: none"),
            ("empty", "Corrective action: none", "Corrective action:"),
            ("missing", "Corrective action: none\n", ""),
            ("whitespace-cased-none", "Corrective action: none", "Corrective action:   None  "),
            ("n-a", "Corrective action: none", "Corrective action: N/A"),
        )
        for name, old, new in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-rfg-corrective-{name}-"))
                self.addCleanupTree(root)
                calibration = (
                    valid_requirement_compression_calibration_fields()
                    .replace("Audit outcome: correct", "Audit outcome: misclassified-should-have-applied")
                    .replace(old, new)
                )
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(
                    root,
                    "requirement-compression misclassified audit requires corrective action",
                )

    def test_requirement_compression_misclassified_audit_accepts_real_corrective_action(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-rfg-corrective-real-"))
        self.addCleanupTree(root)
        calibration = (
            valid_requirement_compression_calibration_fields()
            .replace("Audit outcome: correct", "Audit outcome: misclassified-should-have-applied")
            .replace(
                "Corrective action: none",
                (
                    "Corrective action: Re-classified receipt R-2026-06-22-014 "
                    "and routed to corpus rotation under RFG-CAL-014."
                ),
            )
        )
        write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )

        self.assertPasses(root)

    def test_requirement_compression_correct_audit_allows_none_corrective_action(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-rfg-corrective-correct-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "code-review-r1.md",
            valid_automated_review_text(valid_requirement_compression_calibration_fields()),
        )
        write_text(
            root / "review-log.md",
            valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
        )

        self.assertPasses(root)

    def test_requirement_compression_calibration_requires_iteration_and_rotation_fields(self) -> None:
        cases = (
            ("Corpus iteration ID", "requirement-compression calibration missing required field Corpus iteration ID"),
            ("Calibration result iteration ID", "requirement-compression calibration missing required field Calibration result iteration ID"),
            ("Previous iteration ID", "requirement-compression calibration missing required field Previous iteration ID"),
            ("Next iteration ID", "requirement-compression calibration missing required field Next iteration ID"),
            ("Rotated by", "requirement-compression calibration missing required field Rotated by"),
            ("Rotation date", "requirement-compression calibration missing required field Rotation date"),
        )
        for field, expected in cases:
            with self.subTest(field=field):
                root = Path(tempfile.mkdtemp(prefix="review-artifact-rfg-required-field-"))
                self.addCleanupTree(root)
                calibration = "\n".join(
                    line
                    for line in valid_requirement_compression_calibration_fields().splitlines()
                    if not line.strip().startswith(f"{field}:")
                )
                write_text(root / "reviews" / "code-review-r1.md", valid_automated_review_text(calibration))
                write_text(
                    root / "review-log.md",
                    valid_log_text("None", "None").replace("changes-requested", "clean-with-notes"),
                )
                self.assertFails(root, expected)

    def test_requirement_fidelity_spec_rejects_unquantified_soft_normative_must_terms(self) -> None:
        spec = read_repo_file("specs/requirement-fidelity-gate.md")
        soft_terms = ("high-risk", "periodically", "higher", "appropriate", "sufficient", "reasonable")
        offenders: list[str] = []
        for line_number, line in enumerate(spec.splitlines(), start=1):
            if "MUST" not in line:
                continue
            lowered = line.lower()
            for term in soft_terms:
                if term in lowered:
                    offenders.append(f"specs/requirement-fidelity-gate.md:{line_number}: {term}: {line}")
        self.assertEqual(offenders, [])

    def test_clean_receipt_root_requires_change_metadata_contract(self) -> None:
        cases = [
            (
                "  reviewed_artifact: specs/example.md\n",
                "",
                "review.reviewed_artifact is required for clean receipt roots",
            ),
            (
                "  review_log: tests/fixtures/review-artifacts/valid-clean-receipt-root/review-log.md\n",
                "",
                "review.review_log is required for clean receipt roots",
            ),
            (
                "  status: clean\n",
                "",
                "review.status must identify clean receipt root status",
            ),
            (
                "  status: clean\n",
                "  status: approved\n",
                "review.status must be 'clean' for clean receipt roots",
            ),
            (
                "  status: clean\n",
                "  status: changes-requested\n",
                "review.status must be 'clean' for clean receipt roots",
            ),
            (
                "  unresolved_items: 0\n",
                "",
                "review.unresolved_items must be 0 for clean receipt roots",
            ),
            (
                "  unresolved_items: 0\n",
                "  unresolved_items: 1\n",
                "review.unresolved_items must be 0 for clean receipt roots",
            ),
        ]
        for old, new, expected in cases:
            with self.subTest(expected=expected):
                root = self.clean_receipt_fixture()
                metadata_path = root / "change.yaml"
                metadata_path.write_text(
                    metadata_path.read_text(encoding="utf-8").replace(old, new),
                    encoding="utf-8",
                )
                self.assertFails(root, expected)

    def test_clean_receipt_root_rejects_empty_resolution_file(self) -> None:
        root = self.clean_receipt_fixture()
        write_text(
            root / "review-resolution.md",
            """
            # Review Resolution

            Closeout status: closed
            """,
        )
        self.assertFails(root, "clean receipt root must not include review-resolution.md without material findings")

    def test_all_formal_lifecycle_stages_are_supported_and_pr_review_is_rejected(self) -> None:
        for stage in [
            "proposal-review",
            "spec-review",
            "architecture-review",
            "plan-review",
            "test-spec-review",
            "code-review",
        ]:
            with self.subTest(stage=stage):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-{stage}-"))
                self.addCleanupTree(root)
                review_id = f"{stage}-r1"
                review_path = f"reviews/{review_id}.md"
                write_text(
                    root / review_path,
                    test_spec_review_text()
                    if stage == "test-spec-review"
                    else review_text(review_id=review_id, stage=stage, status="approved"),
                )
                write_text(
                    root / "review-log.md",
                    review_log_text(
                        review_id=review_id,
                        stage=stage,
                        status="approved",
                        detailed_record=review_path,
                    ),
                )
                self.assertPasses(root)

        root = Path(tempfile.mkdtemp(prefix="review-artifact-pr-review-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "pr-review-r1.md",
            review_text(review_id="pr-review-r1", stage="pr-review", status="approved"),
        )
        write_text(
            root / "review-log.md",
            review_log_text(
                review_id="pr-review-r1",
                stage="pr-review",
                status="approved",
                detailed_record="reviews/pr-review-r1.md",
            ),
        )
        self.assertFails(root, "unknown review stage 'pr-review'")

    def test_test_spec_review_result_fields_validate_status_handoff_and_next_stage(self) -> None:
        valid_cases = [
            ("approved", "implement", "allowed"),
            ("changes-requested", "test-spec revision", "not-allowed"),
            ("changes-requested", "review-resolution", "not-allowed"),
            ("blocked", "spec revision", "not-allowed"),
            ("blocked", "architecture revision", "not-allowed"),
            ("blocked", "plan revision", "not-allowed"),
            ("blocked", "none", "not-allowed"),
            ("inconclusive", "none", "not-allowed"),
        ]
        for review_status, immediate_next_stage, implementation_handoff in valid_cases:
            with self.subTest(
                review_status=review_status,
                immediate_next_stage=immediate_next_stage,
                implementation_handoff=implementation_handoff,
            ):
                root = Path(tempfile.mkdtemp(prefix="review-artifact-test-spec-review-valid-"))
                self.addCleanupTree(root)
                write_text(
                    root / "reviews" / "test-spec-review-r1.md",
                    test_spec_review_text(
                        review_status=review_status,
                        immediate_next_stage=immediate_next_stage,
                        implementation_handoff=implementation_handoff,
                        status=review_status,
                    ),
                )
                write_text(
                    root / "review-log.md",
                    review_log_text(
                        review_id="test-spec-review-r1",
                        stage="test-spec-review",
                        status=review_status,
                        detailed_record="reviews/test-spec-review-r1.md",
                    ),
                )
                self.assertPasses(root)

    def test_test_spec_review_result_fields_reject_unknown_values_before_consistency(self) -> None:
        cases = [
            ("unknown_value_review_status", {"review_status": "rubber-stamp"}, "unsupported test-spec-review Review status"),
            ("unknown_value_next_stage", {"immediate_next_stage": "ship-it"}, "unsupported test-spec-review Immediate next stage"),
            ("unknown_value_handoff", {"implementation_handoff": "maybe"}, "unsupported test-spec-review Implementation handoff"),
        ]
        for name, kwargs, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-test-spec-review-{name}-"))
                self.addCleanupTree(root)
                write_text(
                    root / "reviews" / "test-spec-review-r1.md",
                    test_spec_review_text(**kwargs),
                )
                write_text(
                    root / "review-log.md",
                    review_log_text(
                        review_id="test-spec-review-r1",
                        stage="test-spec-review",
                        status="approved",
                        detailed_record="reviews/test-spec-review-r1.md",
                    ),
                )
                self.assertFails(root, expected)

    def test_test_spec_review_result_fields_reject_inconsistent_combinations(self) -> None:
        cases = [
            (
                "changes_requested_allowed",
                {"review_status": "changes-requested", "implementation_handoff": "allowed"},
                "requires Implementation handoff: not-allowed",
            ),
            (
                "approved_not_allowed",
                {"implementation_handoff": "not-allowed"},
                "requires Implementation handoff: allowed",
            ),
            (
                "approved_revision_stage",
                {"immediate_next_stage": "test-spec revision"},
                "does not allow Immediate next stage: test-spec revision",
            ),
            (
                "inconclusive_implement",
                {
                    "review_status": "inconclusive",
                    "immediate_next_stage": "implement",
                    "implementation_handoff": "not-allowed",
                },
                "does not allow Immediate next stage: implement",
            ),
        ]
        for name, kwargs, expected in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-test-spec-review-{name}-"))
                self.addCleanupTree(root)
                write_text(
                    root / "reviews" / "test-spec-review-r1.md",
                    test_spec_review_text(**kwargs),
                )
                write_text(
                    root / "review-log.md",
                    review_log_text(
                        review_id="test-spec-review-r1",
                        stage="test-spec-review",
                        status=kwargs.get("review_status", "approved"),
                        detailed_record="reviews/test-spec-review-r1.md",
                    ),
                )
                self.assertFails(root, expected)

    def test_formal_review_examples_are_not_selected_as_active_review_roots(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "select-validation.py"),
                "--mode",
                "explicit",
                "--path",
                "docs/examples/formal-review-recording/clean-review-receipt-root.md",
                "--path",
                "docs/examples/formal-review-recording/material-finding-location-examples.md",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertNotIn("review_artifacts.validate", {check["id"] for check in payload["selected_checks"]})

    def test_upstream_material_review_traceability_is_validated(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-upstream-material-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "spec-review-r1.md",
            review_text(
                review_id="spec-review-r1",
                stage="spec-review",
                status="changes-requested",
                finding_id="SR1-F1",
            ),
        )
        write_text(
            root / "review-log.md",
            review_log_text(
                review_id="spec-review-r1",
                stage="spec-review",
                status="changes-requested",
                detailed_record="reviews/spec-review-r1.md",
                material_findings="SR1-F1",
                open_findings="SR1-F1",
            ),
        )
        write_text(root / "review-resolution.md", resolution_text(review_id="spec-review-r1", finding_id="SR1-F1"))
        self.assertPasses(root)

        missing_resolution = Path(tempfile.mkdtemp(prefix="review-artifact-upstream-material-missing-"))
        self.addCleanupTree(missing_resolution)
        shutil.copytree(root, missing_resolution, dirs_exist_ok=True)
        (missing_resolution / "review-resolution.md").unlink()
        self.assertFails(missing_resolution, "material findings require review-resolution.md")

        unknown_finding = Path(tempfile.mkdtemp(prefix="review-artifact-upstream-material-unknown-"))
        self.addCleanupTree(unknown_finding)
        shutil.copytree(root, unknown_finding, dirs_exist_ok=True)
        write_text(
            unknown_finding / "review-resolution.md",
            resolution_text(review_id="spec-review-r1", finding_id="SR1-F99"),
        )
        self.assertFails(unknown_finding, "review-resolution.md references unknown Finding ID")

    def test_no_material_plan_review_rethink_passes_structure_without_resolution(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-plan-rethink-"))
        self.addCleanupTree(root)
        write_text(
            root / "reviews" / "plan-review-r1.md",
            review_text(review_id="plan-review-r1", stage="plan-review", status="rethink"),
        )
        write_text(
            root / "review-log.md",
            review_log_text(
                review_id="plan-review-r1",
                stage="plan-review",
                status="rethink",
                detailed_record="reviews/plan-review-r1.md",
            ),
        )
        result = self.validate(root)
        self.assertFalse(result.blocking_findings)
        self.assertEqual(result.review_count, 1)
        self.assertEqual(result.finding_count, 0)
        self.assertEqual(result.review_log_entry_count, 1)
        self.assertEqual(result.resolution_entry_count, 0)

    def test_implementation_profile_missing_auto_fix_class_is_rejected(self) -> None:
        root = self.fixture()
        write_text(root / "reviews" / "code-review-r1.md", implementation_profile_review_text(""))
        self.assertFails(root, "implementation-profile code-review finding missing auto_fix_class")

    def test_implementation_profile_auto_fix_class_values_are_closed(self) -> None:
        root = self.fixture()
        write_text(
            root / "reviews" / "code-review-r1.md",
            implementation_profile_review_text("auto_fix_class: obvious"),
        )
        self.assertFails(root, "unsupported auto_fix_class")

    def test_mechanical_auto_fix_requires_closed_kind_and_authority_fields(self) -> None:
        root = self.fixture()
        write_text(
            root / "reviews" / "code-review-r1.md",
            implementation_profile_review_text(
                """
                auto_fix_class: mechanical
                auto_fix_kind: simple-cleanup
                affected_paths: scripts/example.py
                deterministic_authority: ruff --fix
                required_validation: python -m pytest tests/example.py
                """
            ),
        )
        self.assertFails(root, "unsupported auto_fix_kind")

        root = self.fixture()
        write_text(
            root / "reviews" / "code-review-r1.md",
            implementation_profile_review_text(
                """
                auto_fix_class: mechanical
                auto_fix_kind: formatter-output
                affected_paths: scripts/example.py
                deterministic_authority: ruff --fix
                """
            ),
        )
        self.assertFails(root, "mechanical auto-fix missing required_validation")

        root = self.fixture()
        write_text(
            root / "reviews" / "code-review-r1.md",
            implementation_profile_review_text(
                """
                auto_fix_class: mechanical
                auto_fix_kind: formatter-output
                affected_paths: scripts/example.py
                deterministic_authority: ruff --fix
                required_validation: python -m pytest tests/example.py
                """
            ),
        )
        self.assertPasses(root)

    def test_declared_safe_auto_fix_requires_complete_recipe_and_behavior_proof(self) -> None:
        root = self.fixture()
        write_text(
            root / "reviews" / "code-review-r1.md",
            implementation_profile_review_text(
                """
                auto_fix_class: declared-safe
                affected_paths: scripts/example.py
                resolution_recipe: Apply the named parser branch change.
                named_inputs: approved spec R1
                named_outputs: parser result
                forbidden_paths: specs/
                acceptance_criteria: focused regression passes
                required_validation_commands: python -m pytest tests/example.py
                production_code_change: yes
                """
            ),
        )
        self.assertFails(root, "declared-safe auto-fix missing scope_preservation_rule")

        root = self.fixture()
        write_text(
            root / "reviews" / "code-review-r1.md",
            implementation_profile_review_text(
                """
                auto_fix_class: declared-safe
                affected_paths: scripts/example.py
                resolution_recipe: Apply the named parser branch change.
                named_inputs: approved spec R1
                named_outputs: parser result
                forbidden_paths: specs/
                acceptance_criteria: focused regression passes
                required_validation_commands: python -m pytest tests/example.py
                scope_preservation_rule: no new public interface or dependency
                production_code_change: yes
                """
            ),
        )
        self.assertFails(root, "declared-safe production-code change missing behavior proof")

        root = self.fixture()
        write_text(
            root / "reviews" / "code-review-r1.md",
            implementation_profile_review_text(
                """
                auto_fix_class: declared-safe
                affected_paths: scripts/example.py
                resolution_recipe: Apply the named parser branch change.
                named_inputs: approved spec R1
                named_outputs: parser result
                forbidden_paths: specs/
                acceptance_criteria: focused regression passes
                required_validation_commands: python -m pytest tests/example.py
                scope_preservation_rule: no new public interface or dependency
                production_code_change: yes
                behavior_test: tests/example.py::test_parser_branch
                """
            ),
        )
        self.assertPasses(root)

    def test_stage_owned_non_approval_closeout_includes_rethink_and_inconclusive(self) -> None:
        for status in ["rethink", "inconclusive"]:
            with self.subTest(status=status):
                root = Path(tempfile.mkdtemp(prefix=f"review-artifact-{status}-closeout-"))
                self.addCleanupTree(root)
                write_text(
                    root / "reviews" / "plan-review-r1.md",
                    review_text(review_id="plan-review-r1", stage="plan-review", status=status),
                )
                write_text(
                    root / "review-log.md",
                    review_log_text(
                        review_id="plan-review-r1",
                        stage="plan-review",
                        status=status,
                        detailed_record="reviews/plan-review-r1.md",
                    ),
                )
                self.assertCloseoutFails(root, "blocking review outcome requires same-stage re-review or explicit closeout")

                write_text(
                    root / "reviews" / "plan-review-r2.md",
                    review_text(review_id="plan-review-r2", stage="plan-review", status="approved").replace(
                        "Round: 1",
                        "Round: 2",
                    ),
                )
                with (root / "review-log.md").open("a", encoding="utf-8") as handle:
                    handle.write(
                        review_log_text(
                            review_id="plan-review-r2",
                            stage="plan-review",
                            status="approved",
                            detailed_record="reviews/plan-review-r2.md",
                            round_value="2",
                        )
                    )
                self.assertCloseoutPasses(root)

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

        root = self.fixture()
        replace_field(root / "reviews" / "code-review-r1.md", "Finding ID", "")
        self.assertFails(root, "Finding ID must be a stable ASCII identifier")

    def test_material_finding_identity_label_is_parser_owned(self) -> None:
        root = self.fixture()
        review_path = root / "reviews" / "code-review-r1.md"
        text = review_path.read_text(encoding="utf-8")
        review_path.write_text(text.replace("Finding ID: CR1-F1", "Finding: CR1-F1"), encoding="utf-8")
        self.assertFails(root, "review-log Material findings reference unknown Finding ID")

    def test_non_enum_severity_is_not_structure_validated(self) -> None:
        root = self.fixture()
        review_path = root / "reviews" / "code-review-r1.md"
        text = review_path.read_text(encoding="utf-8")
        self.assertIn("Finding ID: CR1-F1", text)
        self.assertNotIn("Severity:", text)
        review_path.write_text(
            text.replace("Finding ID: CR1-F1", "Finding ID: CR1-F1\nSeverity: not-a-current-enum"),
            encoding="utf-8",
        )
        self.assertPasses(root)

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

        root = self.fixture()
        replace_field(root / "review-log.md", "Resolution", "other-resolution.md#code-review-r1")
        self.assertFails(root, "Resolution must be review-resolution.md#<Review ID>")

        root = self.fixture()
        replace_field(root / "review-log.md", "Resolution", "review-resolution.md#wrong-review")
        self.assertFails(root, "Resolution must be review-resolution.md#<Review ID>")

        root = self.fixture()
        with (root / "review-log.md").open("a", encoding="utf-8") as handle:
            handle.write("\nResolution: review-resolution.md#duplicate\n")
        self.assertFails(root, "review-log entry must contain exactly one Resolution")

        root = self.fixture()
        resolution = (root / "review-resolution.md").read_text(encoding="utf-8")
        resolution = resolution.replace("### code-review-r1", "### wrong-review")
        (root / "review-resolution.md").write_text(resolution, encoding="utf-8")
        self.assertFails(root, "Resolution Review ID not found in review-resolution.md")

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

        ### code-review-r1

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

        ### code-review-r1

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

    def test_closeout_mode_passes_closed_review_resolution(self) -> None:
        root = self.fixture()
        write_text(root / "review-resolution.md", accepted_closed_resolution_text())
        write_text(
            root / "review-log.md",
            valid_log_text(open_findings="None").replace("changes-requested", "approved"),
        )
        replace_field(root / "reviews" / "code-review-r1.md", "Status", "approved")

        self.assertCloseoutPasses(root)
        cli_result = run_cli(root, "--mode", "closeout")
        self.assertEqual(
            cli_result.returncode,
            0,
            msg=f"stdout:\n{cli_result.stdout}\nstderr:\n{cli_result.stderr}",
        )
        self.assertIn("mode=closeout", cli_result.stdout)

    def test_scan_first_review_resolution_passes_closeout(self) -> None:
        root = self.fixture()
        write_text(root / "review-resolution.md", scan_first_closed_resolution_text())
        write_text(
            root / "review-log.md",
            valid_log_text(open_findings="None").replace("changes-requested", "approved"),
        )
        replace_field(root / "reviews" / "code-review-r1.md", "Status", "approved")

        self.assertCloseoutPasses(root)

    def test_table_only_review_resolution_does_not_satisfy_material_finding_traceability(self) -> None:
        root = self.fixture()
        write_text(
            root / "review-resolution.md",
            """
            # Review Resolution

            Closeout status: closed

            | Finding ID | Disposition | Status |
            |---|---|---|
            | CR1-F1 | accepted | resolved |
            """,
        )
        self.assertFails(root, "missing from review-resolution.md")

    def test_scan_first_review_resolution_template_preserves_required_fields(self) -> None:
        template_path = ROOT / "templates" / "review-resolution.md"
        self.assertTrue(template_path.exists(), "templates/review-resolution.md must exist")
        template = template_path.read_text(encoding="utf-8")

        required_terms = [
            "## Summary",
            "Closeout status:",
            "Reviews covered:",
            "Findings resolved:",
            "Unresolved findings:",
            "Final result:",
            "## Resolution Overview",
            "| Finding ID | Disposition | Status | Resolution summary |",
            "## Common Resolution Metadata",
            "## Finding Details",
            "Finding ID:",
            "Disposition:",
            "Owner:",
            "Owning stage:",
            "Chosen action:",
            "Rationale:",
            "Validation target:",
            "Validation evidence:",
            "## Shared Validation Evidence",
            "## Closeout Checklist",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, template)

    def test_closeout_mode_preserves_clean_review_lightweight_path(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="review-artifact-empty-closeout-"))
        self.addCleanupTree(root)
        self.assertCloseoutPasses(root)

        root = Path(tempfile.mkdtemp(prefix="review-artifact-clean-closeout-"))
        self.addCleanupTree(root)
        write_text(root / "reviews" / "code-review-r1.md", valid_clean_review_text())
        write_text(root / "review-log.md", valid_log_text("None", "None").replace("changes-requested", "approved"))
        self.assertCloseoutPasses(root)

    def test_closeout_mode_blocks_open_or_needs_decision_records(self) -> None:
        root = self.fixture()
        self.assertCloseoutFails(root, "Closeout status must be closed")

        root = self.fixture()
        write_text(
            root / "review-resolution.md",
            accepted_closed_resolution_text().replace("Closeout status: closed", "Closeout status: open")
            + "\nReview closeout: code-review-r1",
        )
        replace_field(root / "review-log.md", "Open findings", "None")
        self.assertCloseoutFails(root, "Closeout status must be closed")

        root = self.fixture()
        write_text(
            root / "review-resolution.md",
            accepted_closed_resolution_text() + "\n    Review closeout: code-review-r1",
        )
        self.assertCloseoutFails(root, "review-log Open findings must be empty for closed closeout")

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
        self.assertCloseoutFails(root, "needs-decision is not a final disposition")

    def test_closeout_mode_validates_accepted_closeout_fields(self) -> None:
        root = self.fixture()
        write_text(root / "review-resolution.md", accepted_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Chosen action")
        self.assertCloseoutFails(root, "accepted finding missing chosen action")

        root = self.fixture()
        write_text(root / "review-resolution.md", accepted_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Validation evidence")
        self.assertCloseoutFails(root, "accepted finding missing validation evidence")

    def test_closeout_mode_validates_rejected_deferred_and_partial_fields(self) -> None:
        root = self.fixture()
        write_text(root / "review-resolution.md", rejected_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Rationale")
        self.assertCloseoutFails(root, "rejected finding missing rationale")

        root = self.fixture()
        write_text(root / "review-resolution.md", deferred_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Rationale")
        self.assertCloseoutFails(root, "deferred finding missing rationale")

        root = self.fixture()
        write_text(root / "review-resolution.md", deferred_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Owning stage")
        self.assertCloseoutFails(root, "deferred finding missing follow-up owner, owning stage, or no-follow-up reason")

        root = self.fixture()
        write_text(root / "review-resolution.md", partially_accepted_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Rejected or deferred portion")
        self.assertCloseoutFails(root, "partially-accepted finding missing rejected or deferred portion")

        root = self.fixture()
        write_text(root / "review-resolution.md", partially_accepted_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Validation evidence")
        self.assertCloseoutFails(root, "partially-accepted finding missing validation evidence")

    def test_closeout_mode_blocks_blocking_review_without_rerun(self) -> None:
        root = self.fixture()
        write_text(root / "review-resolution.md", accepted_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Review closeout")
        replace_field(root / "review-log.md", "Open findings", "None")
        self.assertCloseoutFails(root, "blocking review outcome requires same-stage re-review or explicit closeout")

        root = self.fixture()
        write_text(root / "review-resolution.md", accepted_closed_resolution_text())
        replace_field(root / "review-log.md", "Open findings", "None")
        self.assertCloseoutPasses(root)

        root = self.fixture()
        write_text(root / "review-resolution.md", accepted_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Review closeout")
        replace_field(root / "review-log.md", "Open findings", "None")
        second_review = (root / "reviews" / "code-review-r1.md").read_text(encoding="utf-8")
        second_review = second_review.replace("Review ID: code-review-r1", "Review ID: code-review-r2")
        second_review = second_review.replace("Status: changes-requested", "Status: approved")
        second_review = second_review.replace("Finding ID: CR1-F1", "")
        write_text(root / "reviews" / "code-review-r2.md", second_review)
        with (root / "review-resolution.md").open("a", encoding="utf-8") as handle:
            handle.write("\n### code-review-r2\n\nNo material findings.\n")
        with (root / "review-log.md").open("a", encoding="utf-8") as handle:
            handle.write(
                valid_log_text("None", "None")
                .replace("Review ID: code-review-r1", "Review ID: code-review-r2")
                .replace("Status: changes-requested", "Status: approved")
                .replace("Detailed record: reviews/code-review-r1.md", "Detailed record: reviews/code-review-r2.md")
                .replace("Resolution: review-resolution.md#code-review-r1", "Resolution: review-resolution.md#code-review-r2")
            )
        self.assertCloseoutFails(root, "blocking review outcome requires same-stage re-review or explicit closeout")

        root = self.fixture()
        write_text(root / "review-resolution.md", accepted_closed_resolution_text())
        drop_field(root / "review-resolution.md", "Review closeout")
        replace_field(root / "review-log.md", "Open findings", "None")
        second_review = (root / "reviews" / "code-review-r1.md").read_text(encoding="utf-8")
        second_review = second_review.replace("Review ID: code-review-r1", "Review ID: code-review-r2")
        second_review = second_review.replace("Round: 1", "Round: 2")
        second_review = second_review.replace("Status: changes-requested", "Status: approved")
        second_review = second_review.replace("Finding ID: CR1-F1", "")
        write_text(root / "reviews" / "code-review-r2.md", second_review)
        with (root / "review-resolution.md").open("a", encoding="utf-8") as handle:
            handle.write("\n### code-review-r2\n\nNo material findings.\n")
        with (root / "review-log.md").open("a", encoding="utf-8") as handle:
            handle.write(
                valid_log_text("None", "None")
                .replace("Review ID: code-review-r1", "Review ID: code-review-r2")
                .replace("Round: 1", "Round: 2")
                .replace("Status: changes-requested", "Status: approved")
                .replace("Detailed record: reviews/code-review-r1.md", "Detailed record: reviews/code-review-r2.md")
                .replace("Resolution: review-resolution.md#code-review-r1", "Resolution: review-resolution.md#code-review-r2")
            )
        self.assertCloseoutPasses(root)

    def test_ci_script_invokes_review_artifact_checks_for_changed_roots(self) -> None:
        ci_script = (ROOT / "scripts" / "ci.sh").read_text(encoding="utf-8")
        self.assertIn("test-review-artifact-validator.py", ci_script)
        self.assertIn("validate-review-artifacts.py", ci_script)
        self.assertIn("docs/changes/", ci_script)

    def test_workflow_guidance_names_expanded_review_resolution_contract(self) -> None:
        required_terms = [
            "partially-accepted",
            "needs-decision",
            "Closeout status: closed",
            "Closeout status: open",
            "review-resolution.md",
        ]
        for path in [
            "specs/rigorloop-workflow.md",
            "docs/workflows.md",
            "CONSTITUTION.md",
            "AGENTS.md",
        ]:
            with self.subTest(path=path):
                content = read_repo_file(path)
                for term in required_terms:
                    self.assertIn(term, content)

    def test_review_stage_skills_align_with_review_resolution_contract(self) -> None:
        for path in [
            "skills/proposal-review/SKILL.md",
            "skills/spec-review/SKILL.md",
            "skills/architecture-review/SKILL.md",
            "skills/plan-review/SKILL.md",
            "skills/code-review/SKILL.md",
        ]:
            with self.subTest(path=path):
                review_skill = read_repo_file(path)
                for term in ["evidence", "required outcome", "safe resolution", "needs-decision", "review-resolution.md"]:
                    self.assertIn(term, review_skill)

        verify = read_repo_file("skills/verify/SKILL.md")
        self.assertNotIn("validate-review-artifacts.py --mode closeout", verify)
        for term in [
            "project's review-artifact closeout validation",
            "closeout validation passes",
            "Closeout status: open",
            "needs-decision",
            "Validation evidence",
            "review-resolution.md",
        ]:
            self.assertIn(term, verify)

        explain_change = read_repo_file("skills/explain-change/SKILL.md")
        for term in ["review-resolution.md", "concise", "link", "duplicate transcript"]:
            self.assertIn(term, explain_change)

        pr = read_repo_file("skills/pr/SKILL.md")
        for term in ["counts by disposition", "review-resolution.md", "needs-decision", "duplicate every detailed finding"]:
            self.assertIn(term, pr)

        workflow = read_repo_file("skills/workflow/SKILL.md")
        for term in ["partially-accepted", "needs-decision", "Closeout status: closed", "review-resolution.md"]:
            self.assertIn(term, workflow)


if __name__ == "__main__":
    unittest.main(verbosity=2)
