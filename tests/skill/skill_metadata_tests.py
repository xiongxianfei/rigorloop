"""Skill metadata/readability acceptance and intended rejection diagnostics.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
from contextlib import contextmanager
import shutil
import tempfile
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


@contextmanager
def metadata_fixture(relative):
    """Private valid input; each case keeps its defining mutation visible."""
    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / Path(relative).name
        shutil.copytree(FIXTURES / relative, target)
        yield target / "SKILL.md"


def replace_fixture_text(path, old, new):
    before = path.read_text(encoding="utf-8")
    if before.count(old) != 1 or old == new:
        raise AssertionError("mutation must change exactly one defining input")
    path.write_text(before.replace(old, new, 1), encoding="utf-8")


def assert_exact_rejection(case, result, path, diagnostic):
    case.assertEqual(result.returncode, 1, result.stdout + result.stderr)
    case.assertEqual((result.stdout + result.stderr).strip(),
                     f"Gate A (canonical skill integrity): {path}: {diagnostic}")


class SkillMetadataTests(unittest.TestCase):
    maxDiff = None

    def test_valid_skill_passes(self) -> None:
        result = run_validator(FIXTURES / "valid-basic")
        assert_validation_passes(self, result)

    def test_missing_name_fails(self) -> None:
        with metadata_fixture('valid-basic') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, 'name: valid-basic\n', '')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, 'name: missing required field')
            self.assertEqual(path.read_bytes(), fault_bytes)

    def test_missing_description_fails(self) -> None:
        with metadata_fixture('valid-basic') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, 'description: >\n  Valid fixture skill for first-release structural validation tests.\n', '')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, 'description: missing required field')
            self.assertEqual(path.read_bytes(), fault_bytes)

    def test_missing_title_fails(self) -> None:
        with metadata_fixture('valid-basic') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, '# Valid basic fixture\n', '')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, 'expected exactly one top-level # title, found 0')
            self.assertEqual(path.read_bytes(), fault_bytes)

    def test_missing_expected_output_fails(self) -> None:
        with metadata_fixture('valid-basic') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, '## Expected output', '## Other output')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, "missing required '## Expected output' section")
            self.assertEqual(path.read_bytes(), fault_bytes)

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
        with metadata_fixture('skill-readability/valid-pilot') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, 'version: 0.0.0-test\n', '')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, 'version: missing required readability contract field')
            self.assertEqual(path.read_bytes(), fault_bytes)

    def test_skill_readability_invalid_schema_version_fails(self) -> None:
        with metadata_fixture("skill-readability/valid-pilot") as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, "schema-version: skill-readability-v1", "schema-version: unknown_value")
            # Unknown schema must reject before the competing role consistency fault.
            replace_fixture_text(path, "role_name: valid-pilot", "role_name: another-skill")
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, "schema-version must be 'skill-readability-v1'")

    def test_skill_readability_missing_workflow_role_fails(self) -> None:
        with metadata_fixture('skill-readability/valid-pilot') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, '## Workflow role', '## Other role')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, "missing required '## Workflow role' section")
            self.assertEqual(path.read_bytes(), fault_bytes)

    def test_skill_readability_missing_workflow_role_field_fails(self) -> None:
        with metadata_fixture('skill-readability/valid-pilot') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, '- downstream: review\n', '')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, "Workflow role missing required field 'downstream'")
            self.assertEqual(path.read_bytes(), fault_bytes)

    def test_skill_readability_invalid_stage_fails(self) -> None:
        for role in ("valid-pilot", "another-skill"):
            with self.subTest(role=role), metadata_fixture("skill-readability/valid-pilot") as path:
                assert_validation_passes(self, run_validator(path.parent))
                replace_fixture_text(path, "stage: authoring", "stage: unknown_value")
                if role != "valid-pilot":
                    replace_fixture_text(path, "role_name: valid-pilot", f"role_name: {role}")
                fault_bytes = path.read_bytes()
                result = run_validator(path.parent)
                assert_exact_rejection(self, result, path,
                    "workflow role stage must be one of authoring, execution, handoff, periodic, review, support, verification")
                self.assertEqual(path.read_bytes(), fault_bytes)

    def test_skill_readability_missing_output_skeleton_fails(self) -> None:
        with metadata_fixture('skill-readability/valid-pilot') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, '## Output skeleton', '## Other skeleton')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, "missing required '## Output skeleton' section")
            self.assertEqual(path.read_bytes(), fault_bytes)

    def test_skill_readability_output_skeleton_without_placeholder_fails(self) -> None:
        with metadata_fixture('skill-readability/valid-pilot') as path:
            assert_validation_passes(self, run_validator(path.parent))
            replace_fixture_text(path, 'Title: <title>\n\n## Status\n\n<draft|accepted>', 'Title: Fixed\n\n## Status\n\ndraft')
            fault_bytes = path.read_bytes()
            result = run_validator(path.parent)
            assert_exact_rejection(self, result, path, 'Output skeleton must include fillable placeholders')
            self.assertEqual(path.read_bytes(), fault_bytes)

    def test_skill_readability_required_internal_reference_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/required-internal-reference")
        assert_validation_fails(self, result, "required unavailable internal reference")

    def test_skill_readability_duplicate_closed_enum_fails(self) -> None:
        result = run_validator(FIXTURES / "skill-readability/duplicate-closed-enum")
        assert_validation_fails(self, result, "duplicate closed enum block")

    def test_published_design_description_too_long_fails(self) -> None:
        for size in (1023, 1024, 1025):
            with self.subTest(characters=size), metadata_fixture("valid-basic") as path:
                assert_validation_passes(self, run_validator(path.parent))
                replace_fixture_text(path,
                    "Valid fixture skill for first-release structural validation tests.", "x" * size)
                result = run_validator(path.parent)
                if size <= 1024:
                    assert_validation_passes(self, result)
                else:
                    assert_exact_rejection(self, result, path, "description must be 1024 characters or fewer")

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
