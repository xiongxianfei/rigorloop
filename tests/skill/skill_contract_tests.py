"""Recording-profile component rules; canonical content is checked separately.

TEST-SR-04/05/18: each fault starts with a valid minimal profile and asserts its
specific diagnostic. The selected recording profiles are independent contract inputs,
not copied from the validator's lookup table or canonical prose.
"""
from contextlib import contextmanager
from pathlib import Path
import sys
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation

def replace_once(text, old, new):
    if text.count(old) != 1:
        raise AssertionError("fixture mutation must identify exactly one input")
    return text.replace(old,new,1)


# Independent required CI assemblies; never derive expectations from the validator.
CI_ASSEMBLIES = (
    "CIM0-narrow-review", "CIM1-coverage-review",
    "CIM2-ordinary-github-create", "CIM3-narrow-github-revise",
    "CIM4-coverage-github-revise", "CIM5-structural-github-revise",
    "CIM6-project-native-authoring", "CIM7-privileged-approved-create",
    "CIM8-privileged-approved-revise",
)


def ci_assembly_input(names=None, declaration=None):
    path = ROOT / "skills/ci-maintenance/SKILL.md"
    body = path.read_text(encoding="utf-8")
    if declaration is None:
        declaration = "| Assembly | Selection | Resources |\n| --- | --- | --- |\n"
        declaration += "".join(f"| `{name}` | selected | required |\n"
                               for name in (CI_ASSEMBLIES if names is None else names))
    body, count = re.subn(r"(?ms)^## Assemblies\n.*?(?=^## )",
                         lambda _: "## Assemblies\n\n" + declaration + "\n", body)
    if count != 1:
        raise AssertionError("fixture must replace exactly the declaration section")
    metadata = {"name": "ci-maintenance", "version": "1.0.0",
                "schema-version": "skill-readability-v1"}
    return path, metadata, body


def assert_diagnostic(case, errors, path, expected):
    case.assertEqual(errors, [f"{path}: {expected}"])


class CiAssemblyDeclarationTests(unittest.TestCase):
    """Protect the Design's closed declaration, not prose selection semantics."""

    # Independent contract inputs; do not import the production vocabulary.
    NAMES = CI_ASSEMBLIES

    def test_valid_complete_declaration(self):
        path, metadata, body = ci_assembly_input()
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        self.assertEqual(errors, [])

    def test_unknown_rejected_before_missing_and_duplicate_checks(self):
        path, metadata, body = ci_assembly_input(names=("CIM9-unknown", self.NAMES[0], self.NAMES[0]))
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        assert_diagnostic(
            self, errors, path,
            "unknown CI assembly: CIM9-unknown",
        )

    def test_legacy_short_label_rejected(self):
        path, metadata, body = ci_assembly_input(names=("CIM1",) + self.NAMES[1:])
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        assert_diagnostic(
            self, errors, path,
            "unknown CI assembly: CIM1",
        )

    def test_missing_known_assembly_rejected(self):
        path, metadata, body = ci_assembly_input(names=self.NAMES[:4] + self.NAMES[5:])
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        assert_diagnostic(
            self, errors, path,
            "missing CI assembly: CIM4-coverage-github-revise",
        )

    def test_duplicate_assembly_rejected(self):
        path, metadata, body = ci_assembly_input(names=self.NAMES + (self.NAMES[0],))
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        assert_diagnostic(
            self, errors, path,
            "duplicate CI assembly: CIM0-narrow-review",
        )

    def test_missing_table_rejected(self):
        path, metadata, body = ci_assembly_input(declaration="Select one assembly from the supported values.")
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        assert_diagnostic(
            self, errors, path,
            "Assemblies must declare the nine CI assemblies in a table",
        )


    def test_fenced_table_is_not_a_declaration(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        path, metadata, body = ci_assembly_input(declaration="```text\n" + table + "```\n")
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        assert_diagnostic(
            self, errors, path,
            "Assemblies must declare the nine CI assemblies in a table",
        )

    def test_fenced_negative_example_does_not_override_declaration(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        # The example heading must not truncate the normative section either.
        example = "```text\n## Assemblies\n| CIM9-unknown | invalid | none |\n```\n"
        path, metadata, body = ci_assembly_input(declaration=example + table)
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        self.assertEqual(errors, [])


    def test_tilde_fences_are_examples(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        path, metadata, body = ci_assembly_input(declaration="~~~text\n" + table + "~~~\n")
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        assert_diagnostic(
            self, errors, path,
            "Assemblies must declare the nine CI assemblies in a table",
        )
        path, metadata, body = ci_assembly_input(declaration=table +
                         "~~~text\n| CIM9-unknown | invalid | none |\n~~~\n")
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        self.assertEqual(errors, [])

    def test_only_matching_marker_and_length_close_examples(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        for opener, wrong_close in (("````", "```"), ("~~~", "```"), ("```", "~~~")):
            with self.subTest(opener=opener, wrong_close=wrong_close):
                path, metadata, body = ci_assembly_input(declaration=opener + "text\n" + wrong_close + "\n" +
                                  table + opener + "\n")
                errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
                assert_diagnostic(
                    self, errors, path,
                    "Assemblies must declare the nine CI assemblies in a table",
                )

    def test_longer_matching_close_restores_normative_rows(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        example = "~~~text `example`\n| CIM9-unknown | invalid | none |\n~~~~\n"
        path, metadata, body = ci_assembly_input(declaration=example + table)
        errors = skill_validation.validate_ci_maintenance_contract(path, metadata, body)
        self.assertEqual(errors, [])


class WorkflowRoleStageTests(unittest.TestCase):
    def test_empty_stage_rejects_before_role_consistency(self):
        # An explicitly empty value is not any member of the closed stage set.
        path = ROOT / "tests/fixtures/skills/skill-readability/valid-pilot/SKILL.md"
        metadata, body = skill_validation.load_skill_file(path)
        self.assertEqual([], skill_validation.validate_readability_contract(path, metadata, body))
        for role in ("valid-pilot", "another-skill"):
            with self.subTest(role=role):
                candidate = replace_once(body, "stage: authoring", "stage: ")
                if role != "valid-pilot":
                    candidate = replace_once(candidate, "role_name: valid-pilot", f"role_name: {role}")
                errors = skill_validation.validate_readability_contract(path, metadata, candidate)
                assert_diagnostic(self, errors, path,
                    "workflow role stage must be one of authoring, execution, handoff, periodic, review, support, verification")
