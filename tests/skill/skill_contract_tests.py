"""Recording-profile component rules; canonical content is checked separately.

TEST-SR-04/05/18: each fault starts with a valid minimal profile and asserts its
specific diagnostic. The selected pilot selectors are independent contract inputs,
not copied from the validator's lookup table or canonical prose.
"""
from contextlib import contextmanager
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation

PILOTS = {
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
    def test_implement_current_plan_paths_without_inline_recording(self):
        path = Path("/tmp/implement/SKILL.md")
        body = "## Recording boundary\n" + "\n".join((
            "docs/plan.md", "docs/plans/YYYY-MM-DD-slug.md",
            "docs/changes/<change-id>/change.json", "docs/changes/<change-id>/"))
        self.assertEqual(skill_validation.validate_installed_skill_plan_surface_contract(path, "implement", body), [])
        self.assertTrue(skill_validation.validate_installed_skill_plan_surface_contract(path, "implement", body.replace("change.json", "change.yaml")))
