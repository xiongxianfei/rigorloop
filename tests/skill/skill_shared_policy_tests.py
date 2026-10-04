"""Shared policy.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import shutil
import unittest
from unittest import mock
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation


# Current adopted resource owners, inspected against each published Resource map.
# Keep the expected domain independent of the validator's selected consumers.
DELIVERY_CONSUMERS = frozenset({
    "requirement-analysis", "requirement-review", "design-review", "plan",
    "delivery-review", "code-review", "verify",
})
REVIEW_CONSUMERS = frozenset({
    "requirement-review", "design-review", "delivery-review", "code-review",
    "plan", "route", "verify", "pr", "implement", "ci-maintenance",
})
ASSESSMENT_CONSUMERS = frozenset({
    "requirement-review", "design-review", "delivery-review", "code-review",
})
QUALITY_CONSUMERS = frozenset({
    "system-design", "architecture-design", "bugfix", "ci-maintenance", "code-review", "delivery-review",
    "design-review", "implement", "plan", "route", "verify",
})
MAINTENANCE_CONSUMERS = frozenset({
    "bugfix", "ci-maintenance", "code-review", "delivery-review",
    "implement", "plan", "route", "verify",
})


class RequirementDeliveryModelM3Tests(unittest.TestCase):
    def test_m3_all_nine_consumers_match_canonical_bytes(self) -> None:
        # Retain the historical selector; the current adopted domain has seven owners.
        self.assertEqual(skill_validation.REQUIREMENT_DELIVERY_MODEL_CONSUMERS, DELIVERY_CONSUMERS)
        canonical = ROOT / "templates" / "shared" / "requirement-to-delivery-model.md"
        for skill_name in sorted(DELIVERY_CONSUMERS):
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    skill_validation.validate_requirement_delivery_model_copy(skill_path, skill_name),
                    [],
                )
                self.assertEqual(
                    (skill_path.parent / "references" / "requirement-to-delivery-model.md").read_bytes(),
                    canonical.read_bytes(),
                )

    def test_m3_missing_and_drifted_copy_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = root / "canonical.md"
            canonical.write_text("canonical\n", encoding="utf-8")
            skill_path = root / "skills" / "requirement-analysis" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text("# Proposal\n", encoding="utf-8")
            missing = skill_validation.validate_requirement_delivery_model_copy(
                skill_path, "requirement-analysis", canonical_path=canonical
            )
            self.assertIn("is missing", missing[0])
            local = skill_path.parent / "references" / "requirement-to-delivery-model.md"
            local.parent.mkdir()
            local.write_text("drifted\n", encoding="utf-8")
            drifted = skill_validation.validate_requirement_delivery_model_copy(
                skill_path, "requirement-analysis", canonical_path=canonical
            )
            self.assertIn("differs from canonical", drifted[0])

    def test_m3_public_validator_rejects_missing_mapped_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skills_root = root / "skills"
            shutil.copytree(ROOT / "skills" / "requirement-analysis", skills_root / "requirement-analysis")
            missing = skills_root / "requirement-analysis" / "references" / "requirement-to-delivery-model.md"
            missing.unlink()
            with mock.patch.object(skill_validation, "CANONICAL_SKILLS_DIR", skills_root), mock.patch.object(
                skill_validation,
                "REQUIREMENT_DELIVERY_MODEL_SOURCE",
                ROOT / "templates" / "shared" / "requirement-to-delivery-model.md",
            ):
                result = skill_validation.validate_skill_tree(skills_root / "requirement-analysis")
            self.assertTrue(
                any("mapped requirement-to-delivery reference is missing" in error for error in result.errors),
                result.errors,
            )


class ReviewCloseoutResourceTests(unittest.TestCase):
    def test_unknown_value_consumer_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "missing/SKILL.md"
            with mock.patch.object(Path, "open", side_effect=AssertionError("unexpected resource read")):
                errors = skill_validation.validate_review_closeout_copies(skill, "unknown_value")
            self.assertEqual(errors, [f"{skill}: unknown review-closeout consumer 'unknown_value'"])

    def test_missing_drifted_and_valid_resources(self):
        for name in ("review-assessment", "review-reliance"):
            for fault in ("missing-copy", "missing-source", "drift"):
                with self.subTest(resource=name, fault=fault), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    source = root / "source"
                    source.mkdir()
                    skill = root / "skills" / "code-review" / "SKILL.md"
                    references = skill.parent / "references"
                    references.mkdir(parents=True)
                    for resource in ("review-assessment", "review-reliance"):
                        (source / f"{resource}.md").write_bytes((resource + "\n").encode())
                        shutil.copyfile(source / f"{resource}.md", references / f"{resource}.md")
                    self.assertEqual([], skill_validation.validate_review_closeout_copies(
                        skill, "code-review", source=source))
                    before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                    local = references / f"{name}.md"
                    canonical = source / f"{name}.md"
                    if fault == "missing-copy":
                        local.unlink()
                    elif fault == "missing-source":
                        canonical.unlink()
                    else:
                        local.write_bytes(local.read_bytes() + b"drift\n")
                    expected = (f"{local}: review-closeout reference differs from canonical source"
                                if fault == "drift" else
                                f"{local}: review-closeout reference is missing (source {canonical})")
                    fault_tree = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
                    self.assertNotEqual(before, fault_tree)
                    self.assertEqual([expected], skill_validation.validate_review_closeout_copies(
                        skill, "code-review", source=source))
                    self.assertEqual(fault_tree,
                        {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()})

    def test_all_selected_consumers_carry_exact_resources(self):
        self.assertEqual(skill_validation.REVIEW_CLOSEOUT_CONSUMERS, REVIEW_CONSUMERS)
        self.assertEqual(skill_validation.REVIEW_ASSESSMENT_CONSUMERS, ASSESSMENT_CONSUMERS)
        for name in sorted(REVIEW_CONSUMERS):
            with self.subTest(skill=name):
                root = ROOT / "skills" / name
                errors = skill_validation.validate_review_closeout_copies(root / "SKILL.md", name)
                self.assertEqual([], errors)
                resources = ["review-reliance"]
                if name in ASSESSMENT_CONSUMERS:
                    resources.append("review-assessment")
                for resource in resources:
                    self.assertEqual(
                        (root / "references" / f"{resource}.md").read_bytes(),
                        (ROOT / "templates" / "shared" / f"{resource}.md").read_bytes(),
                    )


class TestPolicyResourceTests(unittest.TestCase):
    def test_unknown_value_test_policy_consumer_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "missing/SKILL.md"
            with mock.patch.object(Path, "open", side_effect=AssertionError("unexpected resource read")):
                errors = skill_validation.validate_test_policy_copies(skill, "unknown_value")
            self.assertEqual(errors, [f"{skill}: unknown test-policy consumer 'unknown_value'"])

    def test_test_policy_missing_and_drifted_resources_reject(self):
        for name in ("test-quality", "test-maintenance"):
            for fault in ("missing-copy", "missing-source", "drifted-copy"):
                with self.subTest(resource=name, fault=fault), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    source = root / "shared"
                    source.mkdir()
                    skill = root / "implement" / "SKILL.md"
                    refs = skill.parent / "references"
                    refs.mkdir(parents=True)
                    for resource in ("test-quality", "test-maintenance"):
                        (source / f"{resource}.md").write_text("criterion\n")
                        (refs / f"{resource}.md").write_text("criterion\n")
                    self.assertEqual([], skill_validation.validate_test_policy_copies(
                        skill, "implement", source=source))
                    canonical = source / f"{name}.md"
                    local = refs / f"{name}.md"
                    if fault == "missing-copy":
                        local.unlink()
                    elif fault == "missing-source":
                        canonical.unlink()
                    else:
                        local.write_text("changed\n")
                    expected = (f"{local}: test-policy reference differs from canonical source"
                                if fault == "drifted-copy" else
                                f"{local}: test-policy reference is missing (source {canonical})")
                    self.assertEqual([expected], skill_validation.validate_test_policy_copies(
                        skill, "implement", source=source))
                    sibling = "test-maintenance" if name == "test-quality" else "test-quality"
                    self.assertEqual((refs / f"{sibling}.md").read_bytes(), b"criterion\n")

    def test_test_policy_canonical_copies_and_conditional_resources(self):
        self.assertEqual(skill_validation.TEST_QUALITY_CONSUMERS, QUALITY_CONSUMERS)
        self.assertEqual(skill_validation.TEST_MAINTENANCE_CONSUMERS, MAINTENANCE_CONSUMERS)
        for name in sorted(QUALITY_CONSUMERS):
            with self.subTest(name=name):
                path = ROOT / "skills" / name / "SKILL.md"
                self.assertEqual([], skill_validation.validate_test_policy_copies(path, name))
                self.assertIn("READ `references/test-quality.md`", path.read_text())
                resources = ["test-quality"]
                if name in MAINTENANCE_CONSUMERS:
                    self.assertIn("READ `references/test-maintenance.md`", path.read_text())
                    resources.append("test-maintenance")
                for resource in resources:
                    self.assertEqual(
                        (path.parent / "references" / f"{resource}.md").read_bytes(),
                        (ROOT / "templates" / "shared" / f"{resource}.md").read_bytes(),
                    )
