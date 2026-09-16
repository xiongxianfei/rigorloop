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

PROFILES = {
    "route": ("governed-lifecycle-routing.md", "governed_change_context"),
    "verify": ("governed-verification-recording.md", "adopted recording authority"),
    "pr": ("governed-pr-readiness.md", "PR1-governed"),
    "design-review": ("design-review-recording-and-settlement.md", "durable or formal review"),
    "delivery-review": ("delivery-review-recording-and-settlement.md", "durable or formal review"),
    "plan": ("governed-plan-authoring.md", "valid governed plan authority"),
    "implement": ("governed-implementation-recording.md", "governed_recording_context"),
    "code-review": ("governed-code-review-recording.md", "governed_recording_context"),
    "proposal": ("governed-proposal-authoring.md", "governed_proposal_candidate_context"),
    "proposal-review": ("proposal-review-recording-and-settlement.md", "durable_recording_context"),
}
PROFILE = """## Explicit recording
rigorloop-records-v3
record contract
rigorloop context
subject inspect
record_contract
expected_revision
targeted
does not approve
Do not migrate
"""


@contextmanager
def recording_profile(name):
    reference, trigger = PROFILES[name]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name / "SKILL.md"
        resource = path.parent / "references" / reference
        resource.parent.mkdir(parents=True)
        resource.write_text(PROFILE, encoding="utf-8")
        body = (f"## Recording boundary\nUse the selected profile.\n"
                f"## Invocation classification\n{trigger}\n"
                f"## Resource map\nREAD `references/{reference}` when {trigger}.\n")
        path.write_text(body, encoding="utf-8")
        yield path, body, resource, trigger


def replace_once(text, old, new):
    if old not in text:
        raise AssertionError("fixture mutation must affect the intended input")
    result = text.replace(old, new, 1)
    if result == text:
        raise AssertionError("fixture mutation must change the input")
    return result


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


class RecordingReferenceContractTests(unittest.TestCase):
    def test_missing_recording_boundary_rejects(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, _, _trigger):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                body = replace_once(body, "## Recording boundary", "## Unknown boundary")
                errors = skill_validation.validate_targeted_recording_profile(path, body)
                assert_diagnostic(
                    self, errors, path,
                    "missing body recording boundary",
                )

    def test_missing_classification_trigger_rejects(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, _, trigger):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                body = replace_once(body, f"classification\n{trigger}", "classification\nunknown_value")
                errors = skill_validation.validate_targeted_recording_profile(path, body)
                assert_diagnostic(
                    self, errors, path,
                    f"selected recording reference requires its body classification and load trigger: {trigger}",
                )

    def test_missing_load_trigger_rejects(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, _, trigger):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                body = replace_once(body, f"when {trigger}", "when unknown_value")
                errors = skill_validation.validate_targeted_recording_profile(path, body)
                assert_diagnostic(
                    self, errors, path,
                    f"selected recording reference requires its body classification and load trigger: {trigger}",
                )

    def test_missing_primary_token_rejects(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, resource, _):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                resource.write_text(replace_once(PROFILE, "expected_revision", "unknown_value"), encoding="utf-8")
                errors = skill_validation.validate_targeted_recording_profile(path, body)
                assert_diagnostic(
                    self, errors, path,
                    "explicit recording profile missing primary contract token: expected_revision",
                )

    def test_missing_selected_resource_cannot_use_unrelated_or_inline_profile(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, resource, _):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                resource.unlink()
                resource.with_name("unrelated.md").write_text(PROFILE, encoding="utf-8")
                errors = skill_validation.validate_targeted_recording_profile(path, body + "\n" + PROFILE)
                assert_diagnostic(
                    self, errors, path,
                    f"selected recording reference unreadable: references/{resource.name}: FileNotFoundError",
                )

    def test_selected_resource_outside_skill_rejects(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, resource, _):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                outside = path.parent.parent / "outside.md"
                outside.write_text(PROFILE, encoding="utf-8")
                resource.unlink()
                resource.symlink_to(outside)
                errors = skill_validation.validate_targeted_recording_profile(path, body)
                assert_diagnostic(
                    self, errors, path,
                    f"selected recording reference escapes skill root: references/{resource.name}",
                )

    def test_undecodable_selected_resource_rejects(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, resource, _):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                resource.write_bytes(b"\xff")
                errors = skill_validation.validate_targeted_recording_profile(path, body)
                assert_diagnostic(
                    self, errors, path,
                    f"selected recording reference unreadable: references/{resource.name}: UnicodeDecodeError",
                )

    def test_wrong_reference_selection_rejects(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, resource, _):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                body = replace_once(body, resource.name, "unknown_value.md")
                errors = skill_validation.validate_targeted_recording_profile(path, body)
                assert_diagnostic(
                    self, errors, path,
                    f"selected recording reference must be mapped: references/{resource.name}",
                )

    def test_missing_profile_heading_rejects(self):
        for name in PROFILES:
            with self.subTest(skill=name), recording_profile(name) as (path, body, resource, _):
                self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
                resource.write_text(replace_once(PROFILE, "## Explicit recording", "## Other profile"), encoding="utf-8")
                errors = skill_validation.validate_targeted_recording_profile(path, body)
                assert_diagnostic(
                    self, errors, path,
                    f"selected recording reference missing Explicit recording profile: references/{resource.name}",
                )


class RelocatedPlanSurfaceTests(unittest.TestCase):
    def test_plan_current_paths_without_inline_recording(self):
        path = Path("/tmp/plan/SKILL.md")
        body = "## Recording boundary\n" + "\n".join((
            "docs/plan.md", "docs/plans/YYYY-MM-DD-slug.md",
            "docs/changes/<change-id>/change.json", "docs/changes/<change-id>/",
            "[Title](plans/YYYY-MM-DD-slug.md)"))
        self.assertEqual(skill_validation.validate_installed_skill_plan_surface_contract(path, "plan", body), [])
        self.assertTrue(skill_validation.validate_installed_skill_plan_surface_contract(path, "plan", body.replace("change.json", "change.yaml")))

    def test_implement_current_plan_paths_without_inline_recording(self):
        path = Path("/tmp/implement/SKILL.md")
        body = "## Recording boundary\n" + "\n".join((
            "docs/plan.md", "docs/plans/YYYY-MM-DD-slug.md",
            "docs/changes/<change-id>/change.json", "docs/changes/<change-id>/"))
        self.assertEqual(skill_validation.validate_installed_skill_plan_surface_contract(path, "implement", body), [])
        self.assertTrue(skill_validation.validate_installed_skill_plan_surface_contract(path, "implement", body.replace("change.json", "change.yaml")))


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
