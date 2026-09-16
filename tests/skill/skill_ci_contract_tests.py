"""CI-maintenance resource/schema and safety-guardrail input validation.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_cli_tests import run_validator
from skill_fixture_helpers import (
    assert_validation_fails,
    copy_ci_maintenance_fixture,
)


class CiMaintenanceInputTests(unittest.TestCase):
    maxDiff = None

    def test_ci_maintenance_contract_validates_canonical_skill(self) -> None:
        result = run_validator(ROOT / "skills" / "ci-maintenance" / "SKILL.md")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected canonical ci-maintenance skill to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_ci_maintenance_contract_rejects_stale_identifier_surfaces(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace("role_name: ci-maintenance", "role_name: ci"),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = copy_ci_maintenance_fixture(Path(temporary))
            mutate(skill_dir)
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "stale ci-maintenance identifier")

    def test_ci_maintenance_contract_rejects_missing_schema_version(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace("schema-version: skill-readability-v1\n", ""),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = copy_ci_maintenance_fixture(Path(temporary))
            mutate(skill_dir)
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "ci-maintenance frontmatter must include schema-version")

    def test_ci_maintenance_contract_requires_resource_map_verbs(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace(
                    "- READ `references/risk-to-check-map.md`",
                    "- COPY `references/risk-to-check-map.md`",
                ),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = copy_ci_maintenance_fixture(Path(temporary))
            mutate(skill_dir)
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "Resource map entry for 'references/risk-to-check-map.md' must use literal READ")

    def test_ci_maintenance_contract_requires_skeleton_defaults(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skeleton_path = skill_dir / "assets" / "github-workflow-skeleton.yml"
            text = skeleton_path.read_text(encoding="utf-8")
            skeleton_path.write_text(
                text.replace("permissions:\n  contents: read\n\n", ""),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = copy_ci_maintenance_fixture(Path(temporary))
            mutate(skill_dir)
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "workflow skeleton must include least-privilege permissions")

    def test_ci_maintenance_contract_requires_risk_map_split_and_fail_safe(self) -> None:
        def mutate(skill_dir: Path) -> None:
            risk_map_path = skill_dir / "references" / "risk-to-check-map.md"
            text = risk_map_path.read_text(encoding="utf-8")
            risk_map_path.write_text(
                text.replace(
                    "Unmapped changed surfaces are not no-risk surfaces. Stop for reviewer judgment, route to a conservative boundary check, or both. Missing, stale, incomplete, or conflicting command and placement evidence blocks coverage-sensitive work.\n\n",
                    "",
                ),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = copy_ci_maintenance_fixture(Path(temporary))
            mutate(skill_dir)
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "risk map must include unmapped-surface fail-safe")

    def test_ci_maintenance_contract_requires_review_guardrails_and_command_blocker(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace("overbroad permissions", "permission concerns").replace(
                    "report a blocker instead of guessing",
                    "continue with a likely command",
                ),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = copy_ci_maintenance_fixture(Path(temporary))
            mutate(skill_dir)
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "ci-maintenance must flag overbroad permissions during workflow review")

    def test_ci_maintenance_contract_requires_bounded_pr_repair_guardrails(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace(
                    "Use `bounded-pr-ci-repair` only for an already-open PR with an exact failing run and head",
                    "Use repair mode for a failing PR",
                ),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = copy_ci_maintenance_fixture(Path(temporary))
            mutate(skill_dir)
            result = run_validator(skill_dir)
            assert_validation_fails(self, result, "ci-maintenance must flag bounded PR repair eligibility")
