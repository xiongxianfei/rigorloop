"""Installed review-record placement and plan navigation input contracts.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
import textwrap
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation


class InstalledSkillPlacementTests(unittest.TestCase):
    maxDiff = None

    def test_installed_skill_artifact_placement_contract_helper_accepts_compliant_review_skills(
        self,
    ) -> None:
        def review_skill_placement_fixture(skill_name: str) -> str:
            return textwrap.dedent(
                f"""\
                # {skill_name}

                ## Artifact placement

                Formal {skill_name} records go under:
                `docs/changes/<change-id>/reviews/{skill_name}-r<n>.md`

                Record the review-log entry in:
                `docs/changes/<change-id>/review-log.md`

                Use `docs/changes/<change-id>/review-resolution.md` only when material
                findings, blocking outcomes, or accepted dispositions require it.

                If this is a formal lifecycle review and no change pack exists, create
                or request `docs/changes/<change-id>/` before claiming `Recording status:
                recorded`.

                If the user requested an isolated advisory review and no formal recording
                is required, do not create lifecycle artifacts unless explicitly asked.
                """
            )

        for skill_name in ("proposal-review",):
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    skill_validation.validate_installed_skill_artifact_placement_contract(
                        Path(f"skills/{skill_name}/SKILL.md"),
                        skill_name,
                        review_skill_placement_fixture(skill_name),
                    ),
                    [],
                )

    def test_installed_skill_artifact_placement_contract_helper_rejects_wrong_record_type(
        self,
    ) -> None:
        def review_skill_placement_fixture(
            *,
            skill_name: str,
            record_type_name: str,
        ) -> str:
            return textwrap.dedent(
                f"""\
                # {skill_name}

                ## Artifact placement

                Formal {record_type_name} records go under:
                `docs/changes/<change-id>/reviews/{skill_name}-r<n>.md`

                Record the review-log entry in:
                `docs/changes/<change-id>/review-log.md`

                Use `docs/changes/<change-id>/review-resolution.md` only when material
                findings, blocking outcomes, or accepted dispositions require it.

                If this is a formal lifecycle review and no change pack exists, create
                or request `docs/changes/<change-id>/` before claiming `Recording status:
                recorded`.

                If the user requested an isolated advisory review and no formal recording
                is required, do not create lifecycle artifacts unless explicitly asked.
                """
            )

        cases = (
            (
                "proposal-review",
                "spec-review",
                "skills/proposal-review/SKILL.md: installed-skill placement contract names the wrong stage-owned record type spec-review records",
            ),
        )

        for skill_name, record_type_name, expected_error in cases:
            with self.subTest(skill=skill_name):
                errors = skill_validation.validate_installed_skill_artifact_placement_contract(
                    Path(f"skills/{skill_name}/SKILL.md"),
                    skill_name,
                    review_skill_placement_fixture(
                        skill_name=skill_name,
                        record_type_name=record_type_name,
                    ),
                )

                self.assertIn(expected_error, errors)

    def test_installed_skill_artifact_placement_contract_helper_rejects_missing_record_type(
        self,
    ) -> None:
        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/proposal-review/SKILL.md"),
            "proposal-review",
            textwrap.dedent(
                """\
                # Spec review

                ## Artifact placement

                Formal review records go under:
                `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`

                Record the review-log entry in:
                `docs/changes/<change-id>/review-log.md`

                Use `docs/changes/<change-id>/review-resolution.md` only when material
                findings, blocking outcomes, or accepted dispositions require it.

                If this is a formal lifecycle review and no change pack exists, create
                or request `docs/changes/<change-id>/` before claiming `Recording status:
                recorded`.

                If the user requested an isolated advisory review and no formal recording
                is required, do not create lifecycle artifacts unless explicitly asked.
                """
            ),
        )

        self.assertIn(
            "skills/proposal-review/SKILL.md: installed-skill placement contract must state the stage-owned record type proposal-review record(s)",
            errors,
        )

    def test_installed_skill_artifact_placement_contract_helper_rejects_wrong_record_type_in_artifact_placement_only(
        self,
    ) -> None:
        body = textwrap.dedent(
            """\
            # Spec review

            Mentioning proposal-review records outside the placement block does not
            satisfy the placement contract.

            ## Artifact placement

            Formal spec-review records go under:
            `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`

            Record the review-log entry in:
            `docs/changes/<change-id>/review-log.md`

            Use `docs/changes/<change-id>/review-resolution.md` only when material
            findings, blocking outcomes, or accepted dispositions require it.

            If this is a formal lifecycle review and no change pack exists, create
            or request `docs/changes/<change-id>/` before claiming `Recording status:
            recorded`.

            If the user requested an isolated advisory review and no formal recording
            is required, do not create lifecycle artifacts unless explicitly asked.
            """
        )

        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/proposal-review/SKILL.md"),
            "proposal-review",
            body,
        )

        self.assertIn(
            "skills/proposal-review/SKILL.md: installed-skill placement contract names the wrong stage-owned record type spec-review records",
            errors,
        )

    def test_installed_skill_artifact_placement_contract_helper_rejects_missing_review_path(
        self,
    ) -> None:
        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/proposal-review/SKILL.md"),
            "proposal-review",
            textwrap.dedent(
                """\
                # Proposal review

                ## Artifact placement

                Formal review records go under `docs/changes/<change-id>/reviews/<stage>-r<n>.md`.
                Record the review-log entry in `docs/changes/<change-id>/review-log.md`.
                Use `docs/changes/<change-id>/review-resolution.md` only when material findings require it.
                If no change pack exists, create or request `docs/changes/<change-id>/` before claiming `Recording status: recorded`.
                If this is an isolated advisory review, do not create lifecycle artifacts unless explicitly asked.
                """
            ),
        )

        self.assertIn(
            "skills/proposal-review/SKILL.md: installed-skill placement contract missing default formal review record path docs/changes/<change-id>/reviews/proposal-review-r<n>.md",
            errors,
        )

    def test_installed_skill_artifact_placement_contract_helper_rejects_missing_change_pack_behavior(
        self,
    ) -> None:
        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/proposal-review/SKILL.md"),
            "proposal-review",
            textwrap.dedent(
                """\
                # Spec review

                ## Artifact placement

                Formal proposal-review records go under `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`.
                Record the review-log entry in `docs/changes/<change-id>/review-log.md`.
                Use `docs/changes/<change-id>/review-resolution.md` only when material findings require it.
                Isolated advisory reviews do not create lifecycle artifacts unless explicitly asked.
                """
            ),
        )

        self.assertIn(
            "skills/proposal-review/SKILL.md: installed-skill placement contract must state create-or-request change-pack behavior before claiming Recording status: recorded",
            errors,
        )

    def test_installed_skill_plan_surface_contract_helper_rejects_ambiguous_plan_wording(
        self,
    ) -> None:
        errors = skill_validation.validate_installed_skill_plan_surface_contract(
            Path("skills/plan/SKILL.md"),
            "plan",
            textwrap.dedent(
                """\
                # Plan

                Update the plan before continuing.
                """
            ),
        )

        self.assertIn(
            "skills/plan/SKILL.md: installed-skill plan surface contract must distinguish docs/plan.md, docs/plans/YYYY-MM-DD-slug.md, docs/changes/<change-id>/change.yaml, and docs/changes/<change-id>/",
            errors,
        )
        self.assertIn(
            "skills/plan/SKILL.md: installed-skill plan surface contract must tell plan authors to use clickable relative Markdown links like [Title](plans/YYYY-MM-DD-slug.md) in docs/plan.md",
            errors,
        )

    def test_installed_skill_plan_surface_contract_helper_accepts_explicit_surfaces(
        self,
    ) -> None:
        body = textwrap.dedent(
            """\
            # Plan

            Update the plan index at `docs/plan.md`.
            Update the plan body at `docs/plans/YYYY-MM-DD-slug.md`.
            Use change metadata at `docs/changes/<change-id>/change.yaml`.
            Record review evidence under `docs/changes/<change-id>/`.
            Write index links as `[Title](plans/YYYY-MM-DD-slug.md)`.
            """
        )

        self.assertEqual(
            skill_validation.validate_installed_skill_plan_surface_contract(
                Path("skills/plan/SKILL.md"),
                "plan",
                body,
            ),
            [],
        )

    def test_installed_skill_plan_surface_contract_canonical_plan_skill(self) -> None:
        path = ROOT / "skills" / "plan" / "SKILL.md"
        body = path.read_text(encoding="utf-8")

        self.assertEqual(
            skill_validation.validate_installed_skill_plan_surface_contract(
                path.relative_to(ROOT),
                "plan",
                body,
            ),
            [],
        )
