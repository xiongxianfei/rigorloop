"""Skill metadata/readability acceptance and intended rejection diagnostics.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_cli_tests import run_validator
from skill_fixture_helpers import (
    FIXTURES,
    assert_validation_fails,
    assert_validation_passes,
)


class SkillMetadataTests(unittest.TestCase):
    maxDiff = None

    def test_valid_skill_passes(self) -> None:
        result = run_validator(FIXTURES / "valid-basic")
        assert_validation_passes(self, result)

    def test_missing_name_fails(self) -> None:
        result = run_validator(FIXTURES / "missing-name")
        assert_validation_fails(self, result, "name: missing required field")

    def test_missing_description_fails(self) -> None:
        result = run_validator(FIXTURES / "missing-description")
        assert_validation_fails(self, result, "description: missing required field")

    def test_missing_title_fails(self) -> None:
        result = run_validator(FIXTURES / "missing-title")
        assert_validation_fails(self, result, "expected exactly one top-level # title")

    def test_missing_expected_output_fails(self) -> None:
        result = run_validator(FIXTURES / "missing-expected-output")
        assert_validation_fails(self, result, "missing required '## Expected output' section")

    def test_missing_skill_file_fails(self) -> None:
        result = run_validator(FIXTURES / "missing-skill-file")
        assert_validation_fails(self, result, "empty-skill/SKILL.md: missing required skill file")

    def test_duplicate_name_fails(self) -> None:
        result = run_validator(FIXTURES / "duplicate-name")
        assert_validation_fails(self, result, "duplicate skill name: duplicate-name")

    def test_placeholder_text_fails(self) -> None:
        result = run_validator(FIXTURES / "placeholder-text")
        assert_validation_fails(self, result, "placeholder text is not allowed")

    def test_skill_readability_valid_fixture_passes(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/valid-pilot")
        assert_validation_passes(self, result)

    def test_skill_readability_missing_version_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/missing-version")
        assert_validation_fails(self, result, "version: missing required readability contract field")

    def test_skill_readability_invalid_schema_version_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/invalid-schema-version")
        assert_validation_fails(self, result, "schema-version must be 'skill-readability-v1'")

    def test_skill_readability_missing_workflow_role_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/missing-workflow-role")
        assert_validation_fails(self, result, "missing required '## Workflow role' section")

    def test_skill_readability_missing_workflow_role_field_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/missing-workflow-role-field")
        assert_validation_fails(self, result, "Workflow role missing required field 'downstream'")

    def test_skill_readability_invalid_stage_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/invalid-stage")
        assert_validation_fails(self, result, "workflow role stage must be one of")

    def test_skill_readability_missing_output_skeleton_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/missing-output-skeleton")
        assert_validation_fails(self, result, "missing required '## Output skeleton' section")

    def test_skill_readability_output_skeleton_without_placeholder_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/output-skeleton-without-placeholder")
        assert_validation_fails(self, result, "Output skeleton must include fillable placeholders")

    def test_skill_readability_required_internal_reference_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/required-internal-reference")
        assert_validation_fails(self, result, "required unavailable internal reference")

    def test_skill_readability_duplicate_closed_enum_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/duplicate-closed-enum")
        assert_validation_fails(self, result, "duplicate closed enum block")

    def test_published_design_description_too_long_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/description-too-long")
        assert_validation_fails(self, result, "description must be 1024 characters or fewer")

    def test_published_design_when_to_use_cannot_replace_description(self) -> None:
        result = run_validator(FIXTURES / "published-design/when-to-use-replaces-description")
        assert_validation_fails(self, result, "when_to_use must not replace description")

    def test_skill_readability_pilot_pair_opts_into_contract(self) -> None:
        for skill_name in ("proposal", "proposal-review"):
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            result = run_validator(skill_path)
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=(
                        f"expected {skill_name} to satisfy the readability contract\n"
                        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                    ),
                )
                body = skill_path.read_text(encoding="utf-8")
                self.assertIn("schema-version: skill-readability-v1", body)
                self.assertIn("## Workflow role", body)
                self.assertIn("## Output skeleton", body)

    def test_skill_readability_execution_review_opts_into_contract(self) -> None:
        for skill_name in ("implement", "code-review"):
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            result = run_validator(skill_path)
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=(
                        f"expected {skill_name} to satisfy the readability contract\n"
                        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                    ),
                )
                body = skill_path.read_text(encoding="utf-8")
                self.assertIn("schema-version: skill-readability-v1", body)
                self.assertIn("## Workflow role", body)
                self.assertIn("## Output skeleton", body)

    def test_generated_output_path_is_rejected(self) -> None:
        result = run_validator(ROOT / ".codex" / "skills")
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("generated output path must not be used as authored source of truth", combined_output)
