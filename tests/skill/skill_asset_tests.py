"""Asset metadata, required structure and canonical/generated resource presence.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
import tempfile
import textwrap
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
FIXTURES = ROOT / "tests" / "fixtures" / "skills"
from lib.validation import skill_validation
from skill_cli_tests import run_validator
from skill_fixture_helpers import (
    assert_validation_fails,
    assert_validation_passes,
    asset_text,
    proposal_family_asset_text,
    review_family_asset_text,
    write_asset_fixture,
)


class SkillAssetContractTests(unittest.TestCase):
    maxDiff = None

    def test_published_design_plan_asset_pilot_valid_fixture_passes(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-valid")
        assert_validation_passes(self, result)

    def test_published_design_plan_asset_count_is_exact(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-missing-approved-asset")
        assert_validation_fails(self, result, "plan asset pilot must ship exactly approved assets")

    def test_published_design_plan_asset_metadata_required(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-missing-metadata")
        assert_validation_fails(self, result, "asset metadata missing required field 'Template'")

    def test_published_design_plan_asset_status_must_be_normative(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-optional-status")
        assert_validation_fails(self, result, "plan asset pilot asset 'assets/milestone.md' must use normative status")

    def test_published_design_plan_asset_resource_map_requires_copy(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-non-copy-verb")
        assert_validation_fails(self, result, "Resource map entry for 'assets/milestone.md' must use literal COPY")

    def test_published_design_plan_asset_resource_map_requires_trigger_and_fields(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-missing-fields")
        assert_validation_fails(self, result, "Resource map entry for 'assets/milestone.md' must name fields or structures to fill")

    def test_published_design_plan_asset_resource_map_requires_every_asset(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-missing-resource-map-entry")
        assert_validation_fails(self, result, "Resource map must name packaged resource 'assets/decision-log-row.md'")

    def test_published_design_plan_asset_placeholders_required(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-missing-placeholder")
        assert_validation_fails(self, result, "asset 'assets/milestone.md' must include a visible placeholder")

    def test_published_design_plan_asset_root_dependency_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-root-dependency")
        assert_validation_fails(self, result, "asset 'assets/milestone.md' must not require repository-root dependency")

    def test_published_design_plan_asset_fingerprint_mismatch_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-fingerprint-mismatch")
        assert_validation_fails(self, result, "asset 'assets/milestone.md' structural fingerprint mismatch")

    def test_published_design_plan_skeleton_section_set_mismatch_fails(self) -> None:
        result = run_validator(FIXTURES / "published-design/plan-assets-section-mismatch")
        assert_validation_fails(self, result, "plan-skeleton section set does not match SKILL.md expected sections")

    def test_published_plan_inlines_stable_handoff_pointer(self) -> None:
        plan_dir = ROOT / "skills" / "plan"
        skeleton = (plan_dir / "assets" / "plan-skeleton.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("## Current Handoff Summary", skeleton)
        self.assertIn(
            "- Owning change record: <docs/changes/change-id/change.json>",
            skeleton,
        )
        self.assertFalse((plan_dir / "assets" / "current-handoff-summary.md").exists())

    def test_current_generated_asset_presence_passes_for_complete_output(self) -> None:
        fixture = FIXTURES / "published-design/generated-output-presence/valid"
        errors = skill_validation.validate_generated_asset_presence(
            skill_name="proposal",
            canonical_skill_dir=fixture / "canonical/proposal",
            generated_skill_dir=fixture / "generated/proposal",
            surface_label="generated skill mirror",
        )

        self.assertEqual(errors, [])

    def test_current_generated_asset_presence_fails_for_missing_generated_asset(self) -> None:
        fixture = FIXTURES / "published-design/generated-output-presence/missing-asset"
        errors = skill_validation.validate_generated_asset_presence(
            skill_name="proposal",
            canonical_skill_dir=fixture / "canonical/proposal",
            generated_skill_dir=fixture / "generated/proposal",
            surface_label="generated skill mirror",
        )

        self.assertEqual(
            errors,
            [
                "Generated output for skill 'proposal' is missing mapped asset "
                "'assets/proposal-skeleton.md' in generated skill mirror"
            ],
        )

    def test_current_generated_asset_presence_names_adapter_surface(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical_skill_dir = write_asset_fixture(
                root / "canonical",
                "code-review",
                {
                    "assets/review-result-skeleton.md": asset_text(
                        template="code-review-result-skeleton-v1",
                        skill="code-review",
                        body="## Result\n\n- Review status: <review status>\n",
                    ),
                    "assets/material-finding.md": asset_text(
                        template="code-review-material-finding-v1",
                        skill="code-review",
                        body="## Finding <finding id>\n\n- Finding ID: <finding id>\n- Severity: <severity>\n",
                    ),
                },
            )
            generated_skill_dir = root / "generated-adapter" / "code-review"
            generated_asset = generated_skill_dir / "assets/review-result-skeleton.md"
            generated_asset.parent.mkdir(parents=True, exist_ok=True)
            generated_asset.write_text("generated result skeleton", encoding="utf-8")

            errors = skill_validation.validate_generated_asset_presence(
                skill_name="code-review",
                canonical_skill_dir=canonical_skill_dir,
                generated_skill_dir=generated_skill_dir,
                surface_label="generated adapter output",
            )

            self.assertEqual(
                errors,
                [
                    "Generated output for skill 'code-review' is missing mapped asset "
                    "'assets/material-finding.md' in generated adapter output"
                ],
            )

    def test_proposal_family_asset_valid_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_asset_fixture(
                root,
                "proposal",
                {
                    "assets/proposal-skeleton.md": proposal_family_asset_text(
                        template="proposal-skeleton-v1",
                        skill="proposal",
                        body=(
                            "## Status\n\n<status>\n\n"
                            "## Conditional sections\n\n"
                            "- Initial intent preservation: include when triggered by SKILL.md.\n"
                            "- Scope budget: include when triggered by SKILL.md.\n"
                        ),
                    ),
                },
            )
            write_asset_fixture(
                root,
                "proposal-review",
                {
                    "assets/review-result-skeleton.md": proposal_family_asset_text(
                        template="proposal-review-result-skeleton-v1",
                        skill="proposal-review",
                        body=(
                            "## Result\n\n"
                            "- Skill: proposal-review\n"
                            "- Review status: <review status>\n"
                            "- Material findings: <material findings>\n"
                            "- Recording status: <recording status>\n"
                            "- Recording blocker: <recording blocker>\n"
                            "- Review record: <review record>\n"
                            "- Review log: <review log>\n"
                            "- Review resolution: <review resolution>\n"
                            "- Open blockers: <open blockers>\n"
                            "- Immediate next stage: <immediate next stage>\n"
                            "- Review dimensions: <review dimensions>\n"
                            "- Scope-preservation result: <scope-preservation result>\n"
                            "- Recommended edits: <recommended edits>\n"
                            "- Recommendation: <recommendation>\n"
                        ),
                    ),
                    "assets/material-finding.md": proposal_family_asset_text(
                        template="proposal-review-material-finding-v1",
                        skill="proposal-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding ID: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                            "- needs-decision rationale: <needs-decision rationale>\n"
                        ),
                    ),
                },
            )

            # Asset fixtures must also carry the current selected recording package.
            for name in ("proposal", "proposal-review"):
                relative = skill_validation.RECORDING_REFERENCES[name]
                resource = root / name / relative
                resource.parent.mkdir(parents=True, exist_ok=True)
                resource.write_bytes((ROOT / "skills" / name / relative).read_bytes())
                entry = root / name / "SKILL.md"
                trigger = "governed_proposal_candidate_context" if name == "proposal" else "durable_recording_context"
                body = entry.read_text().replace("## Resource map", f"## Resource map\n\n- READ `{relative}` when `{trigger}` is true.")
                body += f"\n## Invocation classification\n\nClassify `{trigger}` before recording.\n"
                entry.write_text(body + "\n## Recording boundary\n\nRequire the selected reference before governed work.\n")

            result = run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_proposal_review_result_skeleton_preserves_baseline_result_block(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_asset_fixture(
                root,
                "proposal-review",
                {
                    "assets/review-result-skeleton.md": proposal_family_asset_text(
                        template="proposal-review-result-skeleton-v1",
                        skill="proposal-review",
                        body=(
                            "# Result\n\n"
                            "- Review status: <review status>\n"
                            "- Material findings: <material findings>\n"
                            "- Recording status: <recording status>\n"
                        ),
                    ),
                    "assets/material-finding.md": proposal_family_asset_text(
                        template="proposal-review-material-finding-v1",
                        skill="proposal-review",
                        body="- Severity: <severity>\n",
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            output = result.stdout + result.stderr
            self.assertIn(
                "proposal-review review-result-skeleton must include baseline heading: ## Result",
                output,
            )
            self.assertIn(
                "proposal-review review-result-skeleton must include baseline field: Skill",
                output,
            )

    def test_proposal_review_simplification_package_contract(self) -> None:
        skill_dir = ROOT / "skills" / "proposal-review"
        skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        recording = (skill_dir / "references" / "proposal-review-recording-and-settlement.md").read_text(encoding="utf-8")
        gates = (skill_dir / "references" / "conditional-proposal-gates.md").read_text(encoding="utf-8")
        result = (skill_dir / "assets" / "review-result-skeleton.md").read_text(encoding="utf-8")
        for value in ("none", "advisory-durable", "formal-lifecycle", "manual", "workflow-managed-automated"):
            self.assertIn(value, skill_text)
        for assembly in ("PRR0-core", "PRR0G-context-gated", "PRR1-recorded", "PRR1G-recorded-context-gated"):
            self.assertIn(assembly, skill_text)
        for predicate in ("vision_exception_context", "standing_artifact_context", "scope_budget_context"):
            self.assertIn(predicate, skill_text)
            self.assertIn(predicate, gates)
        self.assertIn("Select the exact change", recording)
        self.assertIn("Do not edit reviewed content", recording)
        self.assertIn("## Specialized-gate group", result)
        self.assertIn("## Durable-recording group", result)
        self.assertIn("## Formal-review group", result)
        self.assertIn("## Automated-review group", result)
        self.assertNotIn("what review status means", result.lower())

    def test_proposal_family_asset_rejects_unapproved_asset_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_asset_fixture(
                root,
                "proposal",
                {
                    "assets/proposal-skeleton.md": proposal_family_asset_text(
                        template="proposal-skeleton-v1", skill="proposal"
                    ),
                    "assets/scope-budget-row.md": proposal_family_asset_text(
                        template="proposal-scope-budget-row-v1", skill="proposal"
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "proposal-family asset rollout must ship exactly approved assets",
                result.stdout + result.stderr,
            )

    def test_proposal_family_asset_resource_map_requires_copy_and_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_asset_fixture(
                root,
                "proposal",
                {
                    "assets/proposal-skeleton.md": proposal_family_asset_text(
                        template="proposal-skeleton-v1", skill="proposal"
                    ),
                },
                resource_entries=textwrap.dedent(
                    """\
                    - READ `assets/proposal-skeleton.md` when creating a proposal.
                      Do not emit unfilled placeholders.
                    """
                ),
            )

            result = run_validator(root)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Resource map entry for 'assets/proposal-skeleton.md' must use literal COPY",
                output,
            )
            self.assertIn(
                "Resource map entry for 'assets/proposal-skeleton.md' must name fields or structures to fill",
                output,
            )

    def test_proposal_family_asset_metadata_status_and_placeholder_required(self) -> None:
        cases = [
            (
                "missing metadata",
                proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    include_metadata=False,
                ),
                "asset metadata missing required field 'Template'",
            ),
            (
                "invalid status",
                proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    status="example",
                ),
                "proposal-family asset 'assets/proposal-skeleton.md' Template status must be one of normative, optional",
            ),
            (
                "missing placeholder",
                proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    body="## Status\n\nStatus field.\n",
                ),
                "asset 'assets/proposal-skeleton.md' must include a visible placeholder",
            ),
            (
                "filler prose",
                proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    body="your text here\n",
                ),
                "asset 'assets/proposal-skeleton.md' must not use filler placeholder text",
            ),
            (
                "root dependency",
                proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    body="Run scripts/internal-check.py before filling <field>.\n",
                ),
                "asset 'assets/proposal-skeleton.md' must not require repository-root dependency",
            ),
        ]

        for name, asset_text, expected in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                write_asset_fixture(
                    root,
                    "proposal",
                    {
                        "assets/proposal-skeleton.md": asset_text,
                    },
                )

                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_proposal_review_asset_policy_field_labels_fail(self) -> None:
        for forbidden_label in (
            "Severity policy",
            "Material-finding sufficiency",
            "Safe-resolution decision rule",
            "Recording-status rules",
            "Scope-preservation rules",
            "Scope-budget review",
            "Vision fit review",
            "Standing artifact gate review",
            "Review dimension guidance",
        ):
            with self.subTest(forbidden_label=forbidden_label):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    write_asset_fixture(
                        root,
                        "proposal-review",
                        {
                            "assets/review-result-skeleton.md": proposal_family_asset_text(
                                template="proposal-review-result-skeleton-v1",
                                skill="proposal-review",
                                body=f"- {forbidden_label}: <policy>\n",
                            ),
                            "assets/material-finding.md": proposal_family_asset_text(
                                template="proposal-review-material-finding-v1",
                                skill="proposal-review",
                                body="- Severity: <severity>\n",
                            ),
                        },
                    )

                    result = run_validator(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "proposal-review asset 'assets/review-result-skeleton.md' must not contain review-policy labels or guidance",
                        result.stdout + result.stderr,
                    )

    def test_proposal_review_asset_non_allowlisted_field_labels_fail(self) -> None:
        for label in (
            "Architecture impact",
            "Testability notes",
            "Rollout realism",
            "Strategic value",
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                write_asset_fixture(
                    root,
                    "proposal-review",
                    {
                        "assets/review-result-skeleton.md": proposal_family_asset_text(
                            template="proposal-review-result-skeleton-v1",
                            skill="proposal-review",
                            body=f"- {label}: <notes>\n",
                        ),
                        "assets/material-finding.md": proposal_family_asset_text(
                            template="proposal-review-material-finding-v1",
                            skill="proposal-review",
                            body="- Severity: <severity>\n",
                        ),
                    },
                )

                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "proposal-review asset 'assets/review-result-skeleton.md' field label is not in the approved structural-label allowlist: "
                    + label,
                    result.stdout + result.stderr,
                )

    def test_proposal_review_asset_policy_prose_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_asset_fixture(
                root,
                "proposal-review",
                {
                    "assets/review-result-skeleton.md": proposal_family_asset_text(
                        template="proposal-review-result-skeleton-v1",
                        skill="proposal-review",
                        body="This asset MUST define severity policy for reviewers.\n<field>\n",
                    ),
                    "assets/material-finding.md": proposal_family_asset_text(
                        template="proposal-review-material-finding-v1",
                        skill="proposal-review",
                        body="- Severity: <severity>\n",
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "proposal-review asset 'assets/review-result-skeleton.md' must not contain review-policy labels or guidance",
                result.stdout + result.stderr,
            )

    def test_proposal_family_generated_asset_presence_names_adapter_surface(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical_skill_dir = write_asset_fixture(
                root / "canonical",
                "proposal-review",
                {
                    "assets/review-result-skeleton.md": proposal_family_asset_text(
                        template="proposal-review-result-skeleton-v1",
                        skill="proposal-review",
                        body="- Review status: <review status>\n",
                    ),
                    "assets/material-finding.md": proposal_family_asset_text(
                        template="proposal-review-material-finding-v1",
                        skill="proposal-review",
                        body="- Severity: <severity>\n",
                    ),
                },
            )
            generated_skill_dir = root / "generated-adapter" / "proposal-review"
            generated_asset = generated_skill_dir / "assets/review-result-skeleton.md"
            generated_asset.parent.mkdir(parents=True, exist_ok=True)
            generated_asset.write_text("generated result skeleton", encoding="utf-8")

            errors = skill_validation.validate_generated_asset_presence(
                skill_name="proposal-review",
                canonical_skill_dir=canonical_skill_dir,
                generated_skill_dir=generated_skill_dir,
                surface_label="generated adapter output",
            )

            self.assertEqual(
                errors,
                [
                    "Generated output for skill 'proposal-review' is missing mapped asset "
                    "'assets/material-finding.md' in generated adapter output"
                ],
            )

    def test_review_family_asset_resource_map_requires_finding_id_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_asset_fixture(
                root,
                "code-review",
                {
                    "assets/material-finding.md": review_family_asset_text(
                        template="code-review-material-finding-v1",
                        skill="code-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding ID: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                            "- needs-decision rationale: <needs-decision rationale>\n"
                        ),
                    ),
                    "assets/review-result-skeleton.md": review_family_asset_text(
                        template="code-review-result-skeleton-v1",
                        skill="code-review",
                        body="- Review status: <review status>\n",
                    ),
                },
                resource_entries=textwrap.dedent(
                    """\
                    - COPY `assets/material-finding.md` when recording each material finding.
                      Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path.
                      Do not emit unfilled placeholders.
                    - COPY `assets/review-result-skeleton.md` when recording the review result.
                      Fill: review result fields.
                      Do not emit unfilled placeholders.
                    """
                ),
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Resource map entry for 'assets/material-finding.md' must instruct agents to confirm the literal Finding ID line before linking",
                result.stdout + result.stderr,
            )

    def test_code_review_family_assets_are_installed_and_preserve_status_vocabulary(self) -> None:
        skills_dir = ROOT / "skills"
        skill_path = skills_dir / "code-review" / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8")

        self.assertIn("- COPY `assets/material-finding.md`", skill_text)
        self.assertIn("- COPY `assets/review-result-skeleton.md`", skill_text)
        self.assertIn("Finding ID:", skill_text)

        material_finding = (skills_dir / "code-review" / "assets" / "material-finding.md").read_text(
            encoding="utf-8"
        )
        for label in [
            "Finding ID:",
            "Severity:",
            "Location:",
            "Evidence:",
            "Required outcome:",
            "Safe resolution path:",
            "needs-decision rationale:",
        ]:
            self.assertIn(label, material_finding)

        result_skeleton = (
            skills_dir / "code-review" / "assets" / "review-result-skeleton.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "approved | changes-requested | blocked | inconclusive",
            result_skeleton,
        )
        self.assertIn("- Reviewed milestone:", result_skeleton)
        self.assertIn("- Milestone closeout:", result_skeleton)
        self.assertNotIn("clean-with-notes", result_skeleton)

    def test_proposal_review_family_assets_preserve_gate_status_vocabulary(self) -> None:
        skills_dir = ROOT / "skills"
        skill_text = (skills_dir / "proposal-review" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("- COPY `assets/material-finding.md`", skill_text)
        self.assertIn("- COPY `assets/review-result-skeleton.md`", skill_text)
        self.assertIn("Finding ID:", skill_text)

        material_finding = (
            skills_dir / "proposal-review" / "assets" / "material-finding.md"
        ).read_text(encoding="utf-8")
        code_review_finding = (
            skills_dir / "code-review" / "assets" / "material-finding.md"
        ).read_text(encoding="utf-8")
        for label in [
            "Finding ID:",
            "Severity:",
            "Location:",
            "Evidence:",
            "Required outcome:",
            "Safe resolution path:",
            "needs-decision rationale:",
        ]:
            self.assertIn(label, material_finding)
        self.assertEqual(
            skill_validation._review_family_material_finding_field_block(material_finding),
            skill_validation._review_family_material_finding_field_block(code_review_finding),
        )

        result_skeleton = (
            skills_dir / "proposal-review" / "assets" / "review-result-skeleton.md"
        ).read_text(encoding="utf-8")
        self.assertIn("approved | changes-requested | blocked | inconclusive", result_skeleton)
        self.assertNotIn("clean-with-notes", result_skeleton)

    def test_review_family_material_finding_requires_parser_owned_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_asset_fixture(
                root,
                "code-review",
                {
                    "assets/material-finding.md": review_family_asset_text(
                        template="code-review-material-finding-v1",
                        skill="code-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                        ),
                    ),
                    "assets/review-result-skeleton.md": review_family_asset_text(
                        template="code-review-result-skeleton-v1",
                        skill="code-review",
                        body="- Review status: <review status>\n",
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "review-family material-finding must include parser-owned label 'Finding ID:'",
                result.stdout + result.stderr,
            )

    def test_review_family_material_finding_field_block_must_match_across_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common_finding = (
                "## Finding <finding id>\n\n"
                "- Finding ID: <finding id>\n"
                "- Severity: <severity>\n"
                "- Location: <location>\n"
                "- Evidence: <evidence>\n"
                "- Required outcome: <required outcome>\n"
                "- Safe resolution path: <safe resolution path>\n"
                "- needs-decision rationale: <needs-decision rationale>\n"
            )
            changed_finding = common_finding.replace(
                "- Evidence: <evidence>\n- Required outcome: <required outcome>\n",
                "- Required outcome: <required outcome>\n- Evidence: <evidence>\n",
            )
            for skill_name, finding_body in (
                ("code-review", common_finding),
                ("proposal-review", changed_finding),
            ):
                result_body = "- Review status: <review status>\n"
                if skill_name == "proposal-review":
                    result_body = "## Result\n\n- Skill: proposal-review\n- Review status: <review status>\n"
                write_asset_fixture(
                    root,
                    skill_name,
                    {
                        "assets/material-finding.md": review_family_asset_text(
                            template=f"{skill_name}-material-finding-v1",
                            skill=skill_name,
                            body=finding_body,
                        ),
                        "assets/review-result-skeleton.md": review_family_asset_text(
                            template=f"{skill_name}-result-skeleton-v1",
                            skill=skill_name,
                            body=result_body,
                        ),
                    },
                )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "review-family material-finding parser-owned field block must be byte-identical across first-slice review skills",
                result.stdout + result.stderr,
            )

    def test_review_family_asset_policy_field_labels_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_asset_fixture(
                root,
                "code-review",
                {
                    "assets/material-finding.md": review_family_asset_text(
                        template="code-review-material-finding-v1",
                        skill="code-review",
                        body="- Severity: <severity>\n",
                    ),
                    "assets/review-result-skeleton.md": review_family_asset_text(
                        template="code-review-result-skeleton-v1",
                        skill="code-review",
                        body="- Severity policy: <policy>\n",
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "review-family asset 'assets/review-result-skeleton.md' must not contain review-policy labels or guidance",
                result.stdout + result.stderr,
            )
