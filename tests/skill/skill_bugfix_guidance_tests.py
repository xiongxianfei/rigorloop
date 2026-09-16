"""Bugfix guidance.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


class BugfixSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "docs" / "changes" / "2026-08-20-bugfix-skill-simplification"
        self.skill_dir = ROOT / "skills" / "bugfix"
        self.skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")


    def test_bugfix_package_keeps_supported_resources_and_complete_behavior(self):
        files = sorted(path.relative_to(self.skill_dir).as_posix() for path in self.skill_dir.rglob("*") if path.is_file())
        self.assertEqual(files, ["SKILL.md", "references/test-maintenance.md", "references/test-quality.md"])
        self.assertIn("Keep required behavior complete", self.skill)
        self.assertNotIn("Report before/after LF-normalized words", self.skill)

    def test_meaningful_legacy_rules_remain_executable(self) -> None:
        for phrase in (
            "unexpected behavior, failing evidence, incident, regression, or bug report",
            "governing behavior, current code and tests, available bug evidence",
            "smallest reliable reproduction",
            "Assess blast radius and inspect nearby code for the same pattern",
            "Fix the supported root cause with the smallest scoped change",
            "Do not refactor unrelated code",
        ):
            self.assertIn(phrase, self.skill)

    def test_evidence_vocabularies_and_proof_table_are_complete(self) -> None:
        for value in (
            "reproduced",
            "not-established",
            "settled",
            "resolvable-restoration",
            "behavior-change-request",
            "feasible",
            "infeasible-with-rationale",
            "unresolved",
            "failing-automated-test",
            "deterministic-alternative",
            "missing",
            "conflicting",
            "supported",
            "uncertain",
        ):
            self.assertIn(value, self.skill)
        for required_row in (
            "Any recognized | failing-automated-test | apply-production-correction",
            "Any recognized | conflicting | stop-blocked",
            "feasible | missing or deterministic-alternative | author-automated-proof",
            "unresolved | missing or deterministic-alternative | resolve-test-feasibility",
            "infeasible-with-rationale | complete deterministic-alternative | apply-production-correction",
            "infeasible-with-rationale | missing | stop-blocked",
        ):
            self.assertIn(required_row, self.skill)

        table = self.skill.split("Use this exhaustive proof-action table:", 1)[1].split("Before production mutation", 1)[0]
        rows = []
        for line in table.splitlines():
            if not line.startswith("|") or "---" in line or "Test feasibility" in line:
                continue
            rows.append(tuple(cell.strip() for cell in line.strip("|").split("|")))
        self.assertEqual(len(rows), 6)

        feasibilities = ("feasible", "unresolved", "infeasible-with-rationale")
        proofs = ("failing-automated-test", "conflicting", "missing", "deterministic-alternative")
        for feasibility in feasibilities:
            for proof in proofs:
                matches = []
                for row_feasibility, row_proof, action in rows:
                    feasibility_matches = row_feasibility == "Any recognized" or row_feasibility == feasibility
                    proof_matches = proof in tuple(part.strip() for part in row_proof.replace("complete ", "").split(" or "))
                    if feasibility_matches and proof_matches:
                        matches.append(action)
                self.assertEqual(
                    len(matches),
                    1,
                    f"expected one proof action for {feasibility}/{proof}, got {matches}",
                )

    def test_edge_classification_prevents_action_overlap(self) -> None:
        self.assertIn("without one concrete defect returns `blocked`", self.skill)
        self.assertIn("incomplete claimed deterministic alternative as `missing`", self.skill)
        self.assertIn("cross-axis inconsistency", self.skill)
        self.assertIn("contract basis value `conflicting` routes under the next rule", self.skill)

    def test_operation_command_and_write_authority_are_independent(self) -> None:
        for value in (
            "diagnose-only",
            "current-bounded",
            "portable-request-bound",
            "governed-scope-bound",
            "invalid-or-ambiguous",
            "one concrete defect",
            "rerun preflight",
        ):
            self.assertIn(value, self.skill)

    def test_proof_authoring_precedes_production_correction(self) -> None:
        for value in (
            "proof-authoring",
            "production-correction",
            "failing-automated-test",
            "infeasible-with-rationale",
            "deterministic-alternative",
            "proof identity",
        ):
            self.assertIn(value, self.skill)
        self.assertLess(self.skill.index("proof-authoring"), self.skill.index("production-correction"))
        self.assertIn("post-fix-validation", self.skill)

    def test_action_precedence_protects_completed_and_failed_corrections(self) -> None:
        for value in (
            "stop-blocked",
            "route-owner",
            "continue-diagnosis",
            "complete-diagnosis",
            "resolve-test-feasibility",
            "author-automated-proof",
            "apply-production-correction",
            "run-post-fix-validation",
            "complete-fix",
        ):
            self.assertIn(value, self.skill)
        completed = self.skill.index("correction exists and all required checks pass")
        eligible = self.skill.index("eligible fix without correction")
        self.assertLess(completed, eligible)

    def test_causes_and_terminal_results_are_closed(self) -> None:
        for value in (
            "implementation-defect",
            "contract-gap",
            "integration-mismatch",
            "data-or-migration",
            "race-or-timing",
            "configuration-or-environment",
            "external-dependency",
            "test-defect",
            "unknown",
            "diagnosis-complete",
            "diagnosis-incomplete",
            "fix-applied",
            "routed-to-owner",
            "blocked",
        ):
            self.assertIn(value, self.skill)

    def test_governed_signals_and_write_owners_fail_closed(self) -> None:
        for value in (
            "no-governed-signal",
            "single-governed-candidate",
            "invalid-or-ambiguous-governed-signal",
            "never fall back",
            "change.json",
            "read-only",
            "do not invent",
        ):
            self.assertIn(value, self.skill)
        for required_row in (
            "Portable diagnose-only | None",
            "Portable proof-authoring | Request-bound tests, fixtures, test-only helpers, and controlled reproduction artifacts",
            "Portable production-correction | Request-bound implementation and explicitly scoped non-authoritative documentation or examples",
            "Governed diagnose-only | None",
            "Governed proof-authoring | Exact governed proof surfaces and one existing authorized evidence destination",
            "Governed production-correction | Exact governed implementation, existing authorized evidence, and only scope-named non-authoritative documentation",
        ):
            self.assertIn(required_row, self.skill)

    def test_result_and_handoff_claims_are_bounded(self) -> None:
        for value in (
            "commands actually run",
            "unexecuted checks",
            "changed surfaces",
            "code-review",
            "no stage continues automatically",
            "PR readiness",
            "lifecycle completion",
            "Unexpected mutation",
            "repository and defect",
            "proof identity",
            "next owner",
        ):
            self.assertIn(value, self.skill)
