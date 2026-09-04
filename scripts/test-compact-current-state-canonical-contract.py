#!/usr/bin/env python3
"""Regression checks for compact current-state canonical guidance."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CompactCanonicalContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_governance_names_compact_owners_and_no_external_dependency(self) -> None:
        for relative in ("CONSTITUTION.md", "AGENTS.md", "README.md", "specs/rigorloop-workflow.md"):
            with self.subTest(path=relative):
                text = self.read(relative)
                self.assertIn("compact-current-state-v1", text)
                self.assertIn("material-decisions.md", text)
                self.assertIn("evidence.yaml", text)
                self.assertIn("stable current review", text.lower())
                self.assertIn("without Git", text)
                self.assertIn("without PR", text)

    def test_current_workflow_scopes_history_heavy_rules_to_legacy(self) -> None:
        text = self.read("specs/rigorloop-workflow.md")
        self.assertIn("Compact current-state amendment (preactivation)", text)
        self.assertIn("Successful Verify establishes compact lifecycle completion", text)
        self.assertIn("transient operation request", text)
        self.assertIn("historical contracts only", text)

    def test_stage_skills_use_bounded_compact_projection(self) -> None:
        skills = (
            "route", "proposal", "proposal-review", "architecture", "spec",
            "design-review", "plan", "delivery-review", "implement", "code-review", "verify",
        )
        for skill in skills:
            relative = f"skills/{skill}/SKILL.md"
            with self.subTest(path=relative):
                text = self.read(relative)
                self.assertIn("compact-current-state-v1", text)
                self.assertIn("bounded", text.lower())
                self.assertIn("stable current review", text.lower())
                self.assertNotIn("Compact changes require `review-log.md`", text)

    def test_activation_remains_withheld_in_m4(self) -> None:
        workflow_context = self.read("packages/rigorloop/dist/lib/workflow-context.js")
        self.assertIn('activation_state: "candidate", authority: "withheld"', workflow_context)


if __name__ == "__main__":
    unittest.main()
