"""Recording-profile component rules; canonical content is checked separately.

TEST-SR-04/05/18: each fault starts with a valid minimal profile and asserts its
specific diagnostic. The selected pilot selectors are independent contract inputs,
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

PILOTS = {
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


class RecordingReferenceContractTests(unittest.TestCase):
    @contextmanager
    def valid_profile(self, name):
        reference, trigger = PILOTS[name]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / name / "SKILL.md"
            resource = path.parent / "references" / reference
            resource.parent.mkdir(parents=True)
            resource.write_text(PROFILE, encoding="utf-8")
            body = (f"## Recording boundary\nUse the selected profile.\n"
                    f"## Invocation classification\n{trigger}\n"
                    f"## Resource map\nREAD `references/{reference}` when {trigger}.\n")
            path.write_text(body, encoding="utf-8")
            self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body), [])
            yield path, body, resource, trigger

    def replace_once(self, text, old, new):
        self.assertIn(old, text, "fixture mutation must affect the intended input")
        result = text.replace(old, new, 1)
        self.assertNotEqual(text, result)
        return result

    def assert_diagnostic(self, path, body, diagnostic):
        self.assertEqual(skill_validation.validate_targeted_recording_profile(path, body),
                         [f"{path}: {diagnostic}"])

    def test_missing_recording_boundary_rejects(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, _, _trigger):
                body = self.replace_once(body, "## Recording boundary", "## Unknown boundary")
                self.assert_diagnostic(path, body, "missing body recording boundary")

    def test_missing_classification_trigger_rejects(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, _, trigger):
                body = self.replace_once(body, f"classification\n{trigger}", "classification\nunknown_value")
                self.assert_diagnostic(path, body,
                    f"selected recording reference requires its body classification and load trigger: {trigger}")

    def test_missing_load_trigger_rejects(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, _, trigger):
                body = self.replace_once(body, f"when {trigger}", "when unknown_value")
                self.assert_diagnostic(path, body,
                    f"selected recording reference requires its body classification and load trigger: {trigger}")

    def test_missing_primary_token_rejects(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, resource, _):
                resource.write_text(self.replace_once(PROFILE, "expected_revision", "unknown_value"), encoding="utf-8")
                self.assert_diagnostic(path, body, "explicit recording profile missing primary contract token: expected_revision")

    def test_missing_selected_resource_cannot_use_unrelated_or_inline_profile(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, resource, _):
                resource.unlink()
                resource.with_name("unrelated.md").write_text(PROFILE, encoding="utf-8")
                self.assert_diagnostic(path, body + "\n" + PROFILE,
                    f"selected recording reference unreadable: references/{resource.name}: FileNotFoundError")

    def test_selected_resource_outside_skill_rejects(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, resource, _):
                outside = path.parent.parent / "outside.md"
                outside.write_text(PROFILE, encoding="utf-8")
                resource.unlink()
                resource.symlink_to(outside)
                self.assert_diagnostic(path, body,
                    f"selected recording reference escapes skill root: references/{resource.name}")

    def test_undecodable_selected_resource_rejects(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, resource, _):
                resource.write_bytes(b"\xff")
                self.assert_diagnostic(path, body,
                    f"selected recording reference unreadable: references/{resource.name}: UnicodeDecodeError")

    def test_wrong_reference_selection_rejects(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, resource, _):
                body = self.replace_once(body, resource.name, "unknown_value.md")
                self.assert_diagnostic(path, body,
                    f"selected recording reference must be mapped: references/{resource.name}")

    def test_missing_profile_heading_rejects(self):
        for name in PILOTS:
            with self.subTest(skill=name), self.valid_profile(name) as (path, body, resource, _):
                resource.write_text(self.replace_once(PROFILE, "## Explicit recording", "## Other profile"), encoding="utf-8")
                self.assert_diagnostic(path, body,
                    f"selected recording reference missing Explicit recording profile: references/{resource.name}")


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
    NAMES = (
        "CIM0-narrow-review", "CIM1-coverage-review",
        "CIM2-ordinary-github-create", "CIM3-narrow-github-revise",
        "CIM4-coverage-github-revise", "CIM5-structural-github-revise",
        "CIM6-project-native-authoring", "CIM7-privileged-approved-create",
        "CIM8-privileged-approved-revise",
    )

    def check_declaration(self, names=None, declaration=None):
        path = ROOT / "skills/ci-maintenance/SKILL.md"
        body = path.read_text(encoding="utf-8")
        if declaration is None:
            declaration = "| Assembly | Selection | Resources |\n| --- | --- | --- |\n"
            declaration += "".join(f"| `{name}` | selected | required |\n"
                                   for name in (self.NAMES if names is None else names))
        body, count = re.subn(r"(?ms)^## Assemblies\n.*?(?=^## )",
                             lambda _: "## Assemblies\n\n" + declaration + "\n", body)
        self.assertEqual(count, 1, "fixture must replace exactly the declaration section")
        metadata = {"name": "ci-maintenance", "version": "1.0.0",
                    "schema-version": "skill-readability-v1"}
        return skill_validation.validate_ci_maintenance_contract(path, metadata, body)

    def assert_error(self, expected, **kwargs):
        path = ROOT / "skills/ci-maintenance/SKILL.md"
        self.assertEqual(self.check_declaration(**kwargs), [f"{path}: {expected}"])

    def test_valid_complete_declaration(self):
        self.assertEqual(self.check_declaration(), [])

    def test_unknown_rejected_before_missing_and_duplicate_checks(self):
        self.assert_error("unknown CI assembly: CIM9-unknown",
                          names=("CIM9-unknown", self.NAMES[0], self.NAMES[0]))

    def test_legacy_short_label_rejected(self):
        self.assert_error("unknown CI assembly: CIM1", names=("CIM1",) + self.NAMES[1:])

    def test_missing_known_assembly_rejected(self):
        self.assert_error("missing CI assembly: CIM4-coverage-github-revise",
                          names=self.NAMES[:4] + self.NAMES[5:])

    def test_duplicate_assembly_rejected(self):
        self.assert_error("duplicate CI assembly: CIM0-narrow-review",
                          names=self.NAMES + (self.NAMES[0],))

    def test_missing_table_rejected(self):
        self.assert_error("Assemblies must declare the nine CI assemblies in a table",
                          declaration="Select one assembly from the supported values.")


    def test_fenced_table_is_not_a_declaration(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        self.assert_error("Assemblies must declare the nine CI assemblies in a table",
                          declaration="```text\n" + table + "```\n")

    def test_fenced_negative_example_does_not_override_declaration(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        # The example heading must not truncate the normative section either.
        example = "```text\n## Assemblies\n| CIM9-unknown | invalid | none |\n```\n"
        self.assertEqual(self.check_declaration(declaration=example + table), [])


    def test_tilde_fences_are_examples(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        self.assert_error("Assemblies must declare the nine CI assemblies in a table",
                          declaration="~~~text\n" + table + "~~~\n")
        self.assertEqual(self.check_declaration(declaration=table +
                         "~~~text\n| CIM9-unknown | invalid | none |\n~~~\n"), [])

    def test_only_matching_marker_and_length_close_examples(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        for opener, wrong_close in (("````", "```"), ("~~~", "```"), ("```", "~~~")):
            with self.subTest(opener=opener, wrong_close=wrong_close):
                self.assert_error("Assemblies must declare the nine CI assemblies in a table",
                                  declaration=opener + "text\n" + wrong_close + "\n" +
                                  table + opener + "\n")

    def test_longer_matching_close_restores_normative_rows(self):
        table = "".join(f"| `{name}` | selected | required |\n" for name in self.NAMES)
        example = "~~~text `example`\n| CIM9-unknown | invalid | none |\n~~~~\n"
        self.assertEqual(self.check_declaration(declaration=example + table), [])
