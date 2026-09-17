"""Project-map inputs, output structure and follow-up ownership boundaries.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import re
import unittest
import shutil
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
FIXTURES = ROOT / "tests" / "fixtures" / "skills"
from lib.validation import skill_validation
from skill_cli_tests import run_validator
from skill_guidance_helpers import (
    extract_markdown_block,
)
from skill_fixture_helpers import (
    assert_contract_errors,
    assert_validation_passes,
    project_map_contract_fixture_errors,
)


def map_fixture_bytes(root: Path) -> dict[str, bytes]:
    """Snapshot the private package without deriving expectations from its validator."""
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


class ProjectMapInputTests(unittest.TestCase):
    maxDiff = None

    def test_project_map_contract_valid_controlled_fixture_passes(self) -> None:
        result = run_validator(FIXTURES / "project-map-contract/valid")
        assert_validation_passes(self, result)
        errors = project_map_contract_fixture_errors(
            FIXTURES / "project-map-contract" / "valid"
        )
        self.assertEqual([], errors)

    def test_project_map_contract_fixture_rejects_missing_baseline(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(text.replace("- Baseline\n", ""), encoding="utf-8")

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = Path(temporary) / "project-map-contract"
            shutil.copytree(FIXTURES / "project-map-contract" / "valid", skill_dir)
            self.assertEqual([], project_map_contract_fixture_errors(skill_dir))
            valid_bytes = map_fixture_bytes(skill_dir)
            mutate(skill_dir)
            fault_bytes = map_fixture_bytes(skill_dir)
            self.assertNotEqual(valid_bytes, fault_bytes, "the defining fault must change the input")
            errors = project_map_contract_fixture_errors(skill_dir)
            self.assertEqual(fault_bytes, map_fixture_bytes(skill_dir))
            assert_contract_errors(self, errors, "project-map contract missing map metadata field 'Baseline'")

    def test_project_map_contract_fixture_rejects_missing_mode(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(text.replace("- `audit`\n", ""), encoding="utf-8")

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = Path(temporary) / "project-map-contract"
            shutil.copytree(FIXTURES / "project-map-contract" / "valid", skill_dir)
            self.assertEqual([], project_map_contract_fixture_errors(skill_dir))
            valid_bytes = map_fixture_bytes(skill_dir)
            mutate(skill_dir)
            fault_bytes = map_fixture_bytes(skill_dir)
            self.assertNotEqual(valid_bytes, fault_bytes, "the defining fault must change the input")
            errors = project_map_contract_fixture_errors(skill_dir)
            self.assertEqual(fault_bytes, map_fixture_bytes(skill_dir))
            assert_contract_errors(self, errors, "project-map contract missing operation 'audit'")

    def test_project_map_contract_fixture_requires_skeleton_copy_entry(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace(
                    "- COPY `assets/project-map-skeleton.md`",
                    "- READ `assets/project-map-skeleton.md`",
                ),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = Path(temporary) / "project-map-contract"
            shutil.copytree(FIXTURES / "project-map-contract" / "valid", skill_dir)
            self.assertEqual([], project_map_contract_fixture_errors(skill_dir))
            valid_bytes = map_fixture_bytes(skill_dir)
            mutate(skill_dir)
            fault_bytes = map_fixture_bytes(skill_dir)
            self.assertNotEqual(valid_bytes, fault_bytes, "the defining fault must change the input")
            errors = project_map_contract_fixture_errors(skill_dir)
            self.assertEqual(fault_bytes, map_fixture_bytes(skill_dir))
            assert_contract_errors(self, errors, "Resource map entry for 'assets/project-map-skeleton.md' must use literal COPY")

    def test_project_map_contract_fixture_rejects_skeleton_hidden_policy(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skeleton_path = skill_dir / "assets" / "project-map-skeleton.md"
            text = skeleton_path.read_text(encoding="utf-8")
            skeleton_path.write_text(
                text + "\nSource-rank rules: source code outranks plans.\n",
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = Path(temporary) / "project-map-contract"
            shutil.copytree(FIXTURES / "project-map-contract" / "valid", skill_dir)
            self.assertEqual([], project_map_contract_fixture_errors(skill_dir))
            valid_bytes = map_fixture_bytes(skill_dir)
            mutate(skill_dir)
            fault_bytes = map_fixture_bytes(skill_dir)
            self.assertNotEqual(valid_bytes, fault_bytes, "the defining fault must change the input")
            errors = project_map_contract_fixture_errors(skill_dir)
            self.assertEqual(fault_bytes, map_fixture_bytes(skill_dir))
            assert_contract_errors(self, errors, "project-map skeleton must not own evidence-ranking or source-rank policy")

    def test_project_map_canonical_contract_passes(self) -> None:
        result = run_validator(ROOT / "skills" / "project-map" / "SKILL.md")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected canonical project-map skill to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_project_map_canonical_contract_rejects_missing_workflow_role(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                re.sub(
                    r"\n## Workflow role\n.*?(?=\n## )",
                    "\n",
                    text,
                    count=1,
                    flags=re.DOTALL,
                ),
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = Path(temporary) / "skills" / "project-map"
            shutil.copytree(ROOT / "skills" / "project-map", skill_dir)
            self.assertEqual([], project_map_contract_fixture_errors(skill_dir))
            valid_bytes = map_fixture_bytes(skill_dir)
            mutate(skill_dir)
            fault_bytes = map_fixture_bytes(skill_dir)
            self.assertNotEqual(valid_bytes, fault_bytes, "the defining fault must change the input")
            metadata, body = skill_validation.load_skill_file(skill_dir / "SKILL.md")
            errors = skill_validation.validate_project_map_contract_fixture(
                skill_dir / "SKILL.md", metadata, body, diagnostic_subject="contract"
            )
            self.assertEqual(fault_bytes, map_fixture_bytes(skill_dir))
            assert_contract_errors(self, errors, "project-map contract missing Workflow role")

    def test_project_map_canonical_contract_requires_mapped_skeleton(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skeleton_path = skill_dir / "assets" / "project-map-skeleton.md"
            skeleton_path.unlink(missing_ok=True)

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = Path(temporary) / "skills" / "project-map"
            shutil.copytree(ROOT / "skills" / "project-map", skill_dir)
            self.assertEqual([], project_map_contract_fixture_errors(skill_dir))
            valid_bytes = map_fixture_bytes(skill_dir)
            mutate(skill_dir)
            fault_bytes = map_fixture_bytes(skill_dir)
            self.assertNotEqual(valid_bytes, fault_bytes, "the defining fault must change the input")
            metadata, body = skill_validation.load_skill_file(skill_dir / "SKILL.md")
            errors = skill_validation.validate_project_map_contract_fixture(
                skill_dir / "SKILL.md", metadata, body, diagnostic_subject="contract"
            )
            self.assertEqual(fault_bytes, map_fixture_bytes(skill_dir))
            assert_contract_errors(self, errors, "mapped project-map skeleton asset 'assets/project-map-skeleton.md' must exist")

    def test_project_map_canonical_contract_rejects_hidden_skeleton_policy(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skeleton_path = skill_dir / "assets" / "project-map-skeleton.md"
            skeleton_path.parent.mkdir(parents=True, exist_ok=True)
            text = (
                skeleton_path.read_text(encoding="utf-8")
                if skeleton_path.is_file()
                else ""
            )
            skeleton_path.write_text(
                text + "\nRefresh triggers: this policy belongs in SKILL.md.\n",
                encoding="utf-8",
            )

        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = Path(temporary) / "skills" / "project-map"
            shutil.copytree(ROOT / "skills" / "project-map", skill_dir)
            self.assertEqual([], project_map_contract_fixture_errors(skill_dir))
            valid_bytes = map_fixture_bytes(skill_dir)
            mutate(skill_dir)
            fault_bytes = map_fixture_bytes(skill_dir)
            self.assertNotEqual(valid_bytes, fault_bytes, "the defining fault must change the input")
            metadata, body = skill_validation.load_skill_file(skill_dir / "SKILL.md")
            errors = skill_validation.validate_project_map_contract_fixture(
                skill_dir / "SKILL.md", metadata, body, diagnostic_subject="contract"
            )
            self.assertEqual(fault_bytes, map_fixture_bytes(skill_dir))
            assert_contract_errors(self, errors, "project-map skeleton must not own refresh triggers")

    def test_project_map_representative_outputs_cover_m3_contract(self) -> None:
        proof_path = (
            ROOT
            / "docs"
            / "changes"
            / "2026-06-23-evidence-bound-incremental-project-map"
            / "representative-project-map-outputs.md"
        )
        proof = proof_path.read_text(encoding="utf-8")

        required_terms = [
            "Representative fixture excerpts, not claims about this repository.",
            "Map status: current",
            "Baseline: abc1234+dirty",
            "Inspected uncommitted paths:",
            "Parent map: not-applicable",
            "Parent map: docs/project-map.md",
            "Durable-boundary rationale:",
            "Overlap owner:",
            "Observed:",
            "Inference:",
            "Unknown:",
            "Configured command, not executed in this mapping session",
            "Executed command:",
            "Exit code: 0",
            "Correction note:",
            "wrong at the previous baseline",
            "Planned state:",
            "Current state:",
            "not represented as deployed",
            "statically traced",
            "demonstrated by tests",
            "partially inferred",
            "Diagram evidence:",
            "inferred edge",
            "Placeholder audit: passed",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, proof)

        for heading in skill_validation.PROJECT_MAP_REQUIRED_OUTPUT_SECTIONS:
            with self.subTest(heading=heading):
                self.assertIn(f"## {heading}", proof)
        self.assertIn("## Area maps", proof)

        for column in skill_validation.PROJECT_MAP_AREA_REGISTRATION_COLUMNS:
            with self.subTest(column=column):
                self.assertIn(column, proof)

        self.assertNotRegex(proof, r"<[^>\n]+>|\[FILL IN\]|\bTODO\b|\bTBD\b")

    def test_follow_up_ownership_m1_project_map_skill_boundary(self) -> None:
        project_map = (ROOT / "skills" / "project-map" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        required_terms = [
            "## Follow-up boundary",
            "`project-map` may record risks and open questions for orientation.",
            "It does not own deferred execution or act as a backlog.",
            "route it through the appropriate owner surface:",
            "`docs/follow-ups.md` or another project-local follow-up artifact according to workflow guidance",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, project_map)

        forbidden_terms = [
            "| Follow-up type | Owner |",
            "Active implementation follow-up",
            "Review finding follow-up",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, project_map)

    def test_follow_up_ownership_register_absent_or_valid_and_no_shared_block(self) -> None:
        follow_up_shared_blocks = [
            path
            for path in (ROOT / "templates" / "shared").glob("*")
            if "follow" in path.name.lower()
        ]
        self.assertEqual([], follow_up_shared_blocks)

        register_path = ROOT / "docs" / "follow-ups.md"
        if not register_path.exists():
            return

        register = register_path.read_text(encoding="utf-8")
        required_terms = [
            "# Follow-ups",
            "This file tracks deferred work that is not owned by an active plan",
            "## Open follow-ups",
            "| ID | Title | Source | Owner stage | Owner surface | Status | Next action |",
            "## Closed follow-ups",
            "| ID | Title | Closed by | Notes |",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, register)

        allowed_statuses = {"open", "planned", "blocked", "done", "superseded", "deferred"}
        open_section = extract_markdown_block(register, "Open follow-ups")
        rows = [
            line
            for line in open_section.splitlines()
            if line.startswith("|")
            and not re.match(r"^\|\s*-+\s*\|", line)
            and "ID | Title | Source" not in line
        ]
        self.assertGreater(len(rows), 0, "docs/follow-ups.md must not be empty")

        for row in rows:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            self.assertEqual(7, len(cells), row)
            self.assertTrue(all(cells), row)
            self.assertIn(cells[5], allowed_statuses, row)
