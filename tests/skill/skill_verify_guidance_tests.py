"""Verify guidance.

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


class VerifySkillSimplificationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "verify"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")

    def test_verify_simplification_maps_exact_resources(self) -> None:
        for relative_path in (
            "references/boundary-first-method-v1.md",
            "references/branch-readiness-verification.md",
        ):
            self.assertTrue((self.root / relative_path).is_file())
            self.assertIn(f"- READ `{relative_path}`", self.skill)

    def test_verify_simplification_declares_closed_outcomes_profiles_and_modes(self) -> None:
        for value in ("scoped-verification", "branch-readiness", "workflow-final-verification"):
            self.assertIn(value, self.skill)
        for value in ("VP0-scoped", "VP0B-scoped-boundary", "VP1-final-readiness", "VP1B-final-readiness-boundary"):
            self.assertIn(value, self.skill)
        for value in ("isolated", "governed-final"):
            self.assertIn(value, self.skill)

    def test_verify_simplification_keeps_item_evidence_and_claim_safety_inline(self) -> None:
        for phrase in (
            "passed`, `failed`, `skipped`, `pending`, `not-run`, and `unknown",
            "configured command is not an actual run",
            "local validation is not observed hosted CI",
            "current from stale evidence",
            "generated-output currency",
            "manual proof",
            "branch-ready",
            "pr-body-ready",
            "pr-open-ready",
        ):
            self.assertIn(phrase, self.skill)

    def test_verify_simplification_reference_owns_aggregation_not_item_meaning(self) -> None:
        reference = (self.root / "references" / "branch-readiness-verification.md").read_text(encoding="utf-8")
        for phrase in ("Final-readiness prerequisites", "Final evidence composition", "blocker aggregation", "Verdict and completion"):
            self.assertIn(phrase, reference)
        for forbidden in ("defines the meaning of `passed`", "owns workflow stage order", "authorizes `pr`"):
            self.assertNotIn(forbidden, reference)

    def test_verify_simplification_fails_safe_on_missing_triggered_resource(self) -> None:
        for phrase in (
            "missing or unreadable triggered reference",
            "stop before dependent interpretation, verdict, recording, or handoff",
            "must not reconstruct",
            "untriggered reference does not load",
        ):
            self.assertIn(phrase, self.skill)


class ExplainChangeSkillRetirementTests(unittest.TestCase):
    def test_standalone_skill_is_absent_and_verify_owns_explanation(self) -> None:
        self.assertFalse((ROOT / "skills" / "explain-change").exists())
        verify = (ROOT / "skills" / "verify" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("final durable explanation", verify)
        manifest = (ROOT / "dist" / "adapters" / "manifest.yaml").read_text(encoding="utf-8")
        self.assertNotIn("name: explain-change", manifest)


class FinalVerificationPackageParityM4Tests(unittest.TestCase):

    def test_verify_has_no_preverification_explanation_dependency(self) -> None:
        body = (ROOT / "skills/verify/SKILL.md").read_text(encoding="utf-8")
        for forbidden in (
            "after `explain-change`",
            "explain-change artifact",
            "current explanation",
            "rationale to `explain-change`",
        ):
            self.assertNotIn(forbidden, body)
        self.assertIn("final explanation only after successful final readiness", body)


    def test_scoped_verify_does_not_load_final_impact_or_explanation_resources(self) -> None:
        body = (ROOT / "skills/verify/SKILL.md").read_text(encoding="utf-8")
        scoped = body.split("### Final-readiness profile", 1)[1].split("## Execution authority", 1)[0]
        self.assertIn("Scoped verification loads none of those final-closeout resources", scoped)
        self.assertNotIn("VP0-scoped` | yes", body)
        self.assertIn("only after a selected final-readiness attempt has succeeded", body)
