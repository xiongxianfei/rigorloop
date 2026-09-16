"""Published guidance excludes required checkout-only inputs and retired routes.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_guidance_helpers import (
    CUSTOMER_PORTABLE_M2_SKILLS,
    CUSTOMER_PORTABLE_REQUIRED_INTERNAL_DEPENDENCY_PATTERNS,
    PUBLISHED_SKILL_FORBIDDEN_INTERNAL_PATTERNS,
    RETIRED_PUBLIC_ROUTE_PATTERNS,
    extract_markdown_block,
    has_customer_portable_guard,
    iter_public_workflow_and_skill_surfaces,
    iter_published_skill_text_surfaces,
)


class SkillPortabilityTests(unittest.TestCase):
    maxDiff = None

    def test_customer_portable_public_skills_define_project_local_evidence_contract(self) -> None:
        for skill_name in CUSTOMER_PORTABLE_M2_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            if skill_name == "design":
                self.assertIn("Missing, stale, conflicting, escaped or malformed governed signals", body)
                self.assertIn("without lifecycle claims", body)
                self.assertIn("portable default", body)
                continue
            block = extract_markdown_block(body, "Project-local evidence")

            required_terms = [
                "customer-project mode by default",
                "project-local",
                "RigorLoop repository-internal",
                "portable defaults",
                "block on ambiguity",
                "authoritative CLI workflow context",
            ]
            for term in required_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, block)

    def test_project_map_treats_local_orientation_inputs_as_optional(self) -> None:
        project_map = (ROOT / "skills" / "project-map" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        block = extract_markdown_block(project_map, "Customer-project orientation")

        required_terms = [
            "customer-project mode by default",
            "optional project-local orientation inputs",
            "absence is normal",
            "Do not search for RigorLoop originals",
            "`AGENTS.md`",
            "`CONSTITUTION.md`",
            "`docs/`",
            "`specs/`",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, block)

    def test_customer_portable_required_internal_dependency_detector_examples(self) -> None:
        forbidden_examples = [
            "must read RigorLoop specs/ before drafting",
            "required: read RigorLoop CONSTITUTION.md",
            "must first read RigorLoop AGENTS.md",
            "read the RigorLoop workflow spec before proceeding",
            "required: docs/reports/token-cost/releases/latest.md",
        ]
        for example in forbidden_examples:
            with self.subTest(example=example):
                self.assertTrue(
                    any(
                        pattern.search(example)
                        for pattern in CUSTOMER_PORTABLE_REQUIRED_INTERNAL_DEPENDENCY_PATTERNS.values()
                    )
                )
                self.assertFalse(has_customer_portable_guard(example))

        allowed_examples = [
            "Read local specs/ if present and relevant.",
            "Use project-local `CONSTITUTION.md` when governing project docs exist.",
            "Use RigorLoop repository docs when operating inside the RigorLoop repository.",
            "Read `AGENTS.md` when this file is the review target.",
            "Use `docs/workflows.md` when the user provided this path.",
            "Use RigorLoop specs/ only when the file is the direct target.",
        ]
        for example in allowed_examples:
            with self.subTest(example=example):
                matched = any(
                    pattern.search(example)
                    for pattern in CUSTOMER_PORTABLE_REQUIRED_INTERNAL_DEPENDENCY_PATTERNS.values()
                )
                self.assertFalse(matched and not has_customer_portable_guard(example))

    def test_published_skill_surfaces_block_required_rigorloop_internal_dependencies(self) -> None:
        for path in iter_published_skill_text_surfaces():
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in CUSTOMER_PORTABLE_REQUIRED_INTERNAL_DEPENDENCY_PATTERNS.items():
                for match in pattern.finditer(body):
                    start = max(match.start() - 160, 0)
                    end = min(match.end() + 160, len(body))
                    surrounding = body[start:end]
                    with self.subTest(path=str(relative_path), forbidden=label):
                        self.assertTrue(has_customer_portable_guard(surrounding))

    def test_public_workflow_and_skill_surfaces_block_retired_route_vocabulary(self) -> None:
        """Public workflow and shipped skill surfaces must not restore retired lane wording."""

        for path in iter_public_workflow_and_skill_surfaces():
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in RETIRED_PUBLIC_ROUTE_PATTERNS.items():
                with self.subTest(path=str(relative_path), pattern=label):
                    self.assertIsNone(pattern.search(body))

    def test_published_skill_surfaces_block_internal_repository_details(self) -> None:
        """Published skill text must stay portable across projects."""

        for path in iter_published_skill_text_surfaces():
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in PUBLISHED_SKILL_FORBIDDEN_INTERNAL_PATTERNS.items():
                with self.subTest(path=str(relative_path), pattern=label):
                    self.assertIsNone(pattern.search(body))
