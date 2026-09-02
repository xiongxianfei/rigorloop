#!/usr/bin/env python3
"""Regression tests for current route and contributor-guide validation."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-guide-system.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_guide_system", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load route guide validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_validator()


class RouteGuideValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="route-guide-validator-")
        self.repo = Path(self.temp.name)
        for path in (
            "README.md",
            "AGENTS.md",
            "CONSTITUTION.md",
            "docs/project-map.md",
            "docs/plan.md",
            "specs/rigorloop-workflow.md",
            "specs/skill-contract.md",
            "skills/route/SKILL.md",
        ):
            source = ROOT / path
            target = self.repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_current_repository_contract_passes(self) -> None:
        self.assertEqual(validator.validate(self.repo).messages, ())

    def test_retained_historical_guide_is_ignored_only_outside_current_path(self) -> None:
        historical = self.repo / "docs/history/workflows.md"
        historical.parent.mkdir(parents=True, exist_ok=True)
        historical.write_text("# Historical workflow guide\n", encoding="utf-8")
        self.assertEqual(validator.validate(self.repo).messages, ())

    def test_current_workflow_guide_fails(self) -> None:
        (self.repo / "docs/workflows.md").write_text("# Workflow guide\n", encoding="utf-8")
        self.assertTrue(any("ROUTE-GUIDE-003" in item for item in validator.validate(self.repo).messages))

    def test_old_or_mixed_skill_inventory_fails(self) -> None:
        old = self.repo / "skills/workflow/SKILL.md"
        old.parent.mkdir(parents=True)
        old.write_text("---\nname: workflow\n---\n", encoding="utf-8")
        self.assertTrue(any("ROUTE-GUIDE-004" in item for item in validator.validate(self.repo).messages))

    def test_guide_only_route_resource_fails(self) -> None:
        retired = self.repo / "skills/route/references/workflow-guide-authoring.md"
        retired.parent.mkdir(parents=True, exist_ok=True)
        retired.write_text("retired\n", encoding="utf-8")
        self.assertTrue(any("ROUTE-GUIDE-005" in item for item in validator.validate(self.repo).messages))

    def test_current_surface_cannot_restore_retired_authority(self) -> None:
        agents = self.repo / "AGENTS.md"
        agents.write_text(agents.read_text(encoding="utf-8") + "\nUse docs/workflows.md.\n", encoding="utf-8")
        self.assertTrue(any("ROUTE-GUIDE-006" in item for item in validator.validate(self.repo).messages))

    def test_current_skill_cannot_restore_semantic_workflow_guide_fallback(self) -> None:
        skill = self.repo / "skills/example/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("Resolve placement from the project workflow guide.\n", encoding="utf-8")
        self.assertTrue(any("ROUTE-GUIDE-009" in item for item in validator.validate(self.repo).messages))

    def test_current_skill_cannot_name_workflow_as_semantic_actor(self) -> None:
        skill = self.repo / "skills/example/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("Return control to workflow, which chooses continuation.\n", encoding="utf-8")
        self.assertTrue(any("ROUTE-GUIDE-010" in item for item in validator.validate(self.repo).messages))


if __name__ == "__main__":
    unittest.main(verbosity=2)
