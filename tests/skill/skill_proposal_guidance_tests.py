"""Proposal guidance.

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


class ProposalSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "proposal"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        governed_path = self.root / "references" / "governed-proposal-authoring.md"
        strategic_path = self.root / "references" / "strategic-and-scope-gates.md"
        self.governed = governed_path.read_text(encoding="utf-8") if governed_path.is_file() else ""
        self.strategic = strategic_path.read_text(encoding="utf-8") if strategic_path.is_file() else ""
        self.skeleton = (self.root / "assets" / "proposal-skeleton.md").read_text(encoding="utf-8")

    def test_package_assemblies_and_resource_ownership_are_closed(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["governed-proposal-authoring.md", "requirement-to-delivery-model.md", "strategic-and-scope-gates.md"])
        for assembly in ("PA0-portable", "PA0G-portable-gated", "PA1-governed", "PA1G-governed-gated"):
            self.assertIn(assembly, self.skill)
        self.assertIn("READ `references/governed-proposal-authoring.md`", self.skill)
        self.assertIn("READ `references/strategic-and-scope-gates.md`", self.skill)
        self.assertIn("COPY `assets/proposal-skeleton.md`", self.skill)
        self.assertIn("must not reconstruct", self.skill.lower())

    def test_portable_and_governed_operation_authority_is_separate(self) -> None:
        for operation in ("create-primary-proposal", "revise-primary-proposal"):
            self.assertIn(operation, self.skill)
        self.assertIn("change link", self.governed)
        for phrase in (
            "governed_proposal_candidate_context",
            "Conversational wording alone does not establish",
            "does not grant mutation authority",
            "must not fall back to portable",
            "Portable authoring writes only the proposal artifact",
        ):
            self.assertIn(phrase.lower(), self.skill.lower())
        for phrase in ("review readiness", "Conflict requires rereading", "downstream reliance", "prior subject identities"):
            self.assertIn(phrase.lower(), self.governed.lower())

    def test_governed_retry_and_authorized_reset_fail_closed(self) -> None:
        for phrase in ("Conflict requires rereading and reassessment", "stop on ambiguous outcome", "Preserve partial evidence", "Do not settle review"):
            self.assertIn(phrase, self.governed)

    def test_specialized_predicates_and_scope_budget_vocabulary_are_closed(self) -> None:
        for predicate in ("vision_exception_context", "standing_artifact_context", "initial_intent_table_context", "scope_budget_context"):
            self.assertIn(predicate, self.skill)
            self.assertIn(predicate, self.strategic)
        self.assertIn("semantic proposal judgment", self.skill.lower())
        self.assertIn("loads exactly once", self.skill.lower())
        for value in ("in scope", "out of scope", "deferred follow-up", "rejected option", "open question", "core to this proposal", "first-slice candidate", "same-slice dependency", "separate implementation slice", "deferable follow-up", "separate proposal"):
            self.assertIn(value, self.strategic)

    def test_skeleton_owns_exact_direction_sections_and_one_conditional_section(self) -> None:
        headings = [
            line.removeprefix("## ")
            for line in self.skeleton.splitlines()
            if line.startswith("## ")
        ]
        self.assertEqual(
            headings,
            [
                "Challenge",
                "Goals",
                "Scope and non-goals",
                "Governing principle",
                "Proposed direction",
                "Feasibility",
                "Impact and major trade-offs",
                "Decision requested",
            ],
        )
        self.assertIn("otherwise omit this section", self.skeleton)
        self.assertIn("Omit the material-impact section when it is not needed", self.skill)
        self.assertIn("inside an allowed section", self.skill)

    def test_references_have_non_overlapping_policy_owners(self) -> None:
        self.assertIn("governed proposal authoring", self.governed.lower())
        self.assertIn("strategic and scope gates", self.strategic.lower())
        self.assertNotIn("scope budget treatment", self.governed.lower())
        self.assertNotIn("change.yaml", self.strategic)
        self.assertNotIn("review-required", self.strategic)
