#!/usr/bin/env python3
"""Regression tests for guide-system validation."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-guide-system.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_guide_system", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load guide-system validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class GuideSystemValidatorTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="guide-system-validator-")
        self.repo = Path(self.temp_dir.name)
        self.write_valid_repo()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, relative: str, text: str) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_valid_repo(self) -> None:
        self.write(
            "README.md",
            """# RigorLoop

## Where to go next

| Need | Read |
|---|---|
| Understand project direction | [VISION.md](VISION.md) |
| Understand governance | [CONSTITUTION.md](CONSTITUTION.md) |
| See workflow and artifact paths | [docs/workflows.md](docs/workflows.md) |
| Orient to repository structure | [docs/project-map.md](docs/project-map.md) |
| See current work | [docs/plan.md](docs/plan.md) |
| Use a specific workflow stage | [skills/](skills/) |
""",
        )
        self.write("VISION.md", "# Vision\n")
        self.write("CONSTITUTION.md", "# Constitution\n")
        self.write(
            "docs/workflows.md",
            """# Workflow guide

## Artifact registry

```yaml
artifact_locations:
  proposal:
    owner: proposal
    path: docs/proposals/<change-id>.md
  plan_index:
    owner: plan
    path: docs/plan.md
  change_plan:
    owner: plan
    path: docs/plans/YYYY-MM-DD-slug.md
  formal_review_record:
    owner: review skills
    path: docs/changes/<change-id>/reviews/<stage>-r<n>.md
```

## Guide ownership

| Question | Primary guide | Secondary source | Owner |
|---|---|---|---|
| How do I perform one stage? | `skills/<stage>/SKILL.md` | workflow guide | owning stage skill |

Stage skills own artifact content and portable defaults. The workflow guide routes
project-local artifact placement without replacing the owning stage skill.

## Artifact locations

| Artifact | Path |
|---|---|
| Proposal | `docs/proposals/<change-id>.md` |
| Plan body | `docs/plans/YYYY-MM-DD-slug.md` |

Learn sessions are historical rationale, not live routing authority.
""",
        )
        self.write(
            "docs/project-map.md",
            """# Project map

This map orients readers to repository structure and boundaries. It does not own
workflow stage order, exact lifecycle artifact placement, or current milestone state.
""",
        )
        self.write(
            "docs/plan.md",
            """# Plan

`docs/plan.md` is the bounded lifecycle index, not a plan body.

## Active

None.

## Blocked

None.

## Done (recent)

None.

## Superseded

None.
""",
        )
        self.write(
            "docs/learn/sessions/2026-06-18-example.md",
            "# Learn session\n\nHistorical rationale only.\n",
        )
        self.write(
            "skills/workflow/SKILL.md",
            """# Workflow

Use project-local guidance when present. Use `docs/plans/YYYY-MM-DD-slug.md`
for the detailed plan body and `docs/plan.md` for the lifecycle index.
`docs/changes/<change-id>/plan.md` is non-canonical unless a future approved
workflow-map contract changes the path.
""",
        )
        self.write(
            "skills/plan/SKILL.md",
            """# Plan

Plan index: `docs/plan.md`.
Plan body: `docs/plans/YYYY-MM-DD-slug.md`.
""",
        )

    def result(self):
        validator = load_validator()
        return validator.validate(self.repo)

    def assertFailsWith(self, check_id: str) -> None:
        result = self.result()
        self.assertFalse(result.ok, result.messages)
        self.assertTrue(
            any(message.startswith(f"{check_id}:") for message in result.messages),
            result.messages,
        )

    def test_valid_fixture_passes(self) -> None:
        result = self.result()
        self.assertTrue(result.ok, result.messages)

    def test_missing_readme_guide_link_fails(self) -> None:
        self.write(
            "README.md",
            """# RigorLoop

## Where to go next

[VISION.md](VISION.md)
""",
        )

        self.assertFailsWith("GUIDE-001")

    def test_workflow_guide_missing_ownership_fails(self) -> None:
        self.write("docs/workflows.md", "# Workflow guide\n\n## Artifact locations\n")

        self.assertFailsWith("GUIDE-002")

    def test_project_map_cannot_own_workflow_stage_order(self) -> None:
        self.write(
            "docs/project-map.md",
            "# Project map\n\nThis file owns workflow stage order and artifact placement.\n",
        )

        self.assertFailsWith("GUIDE-004")

    def test_plan_index_rejects_plan_body_headings(self) -> None:
        self.write(
            "docs/plan.md",
            """# Plan

## Active

## Blocked

## Done (recent)

## Superseded

## Milestones
""",
        )

        self.assertFailsWith("GUIDE-005")

    def test_learn_session_cannot_be_live_routing_authority(self) -> None:
        self.write(
            "docs/learn/sessions/2026-06-18-example.md",
            "# Learn session\n\nThis session is live routing authority for plan placement.\n",
        )

        self.assertFailsWith("GUIDE-006")

    def test_workflow_skill_plan_path_contradiction_fails(self) -> None:
        self.write(
            "skills/workflow/SKILL.md",
            "# Workflow\n\nDetailed plans belong in `docs/changes/<change-id>/plan.md`.\n",
        )

        self.assertFailsWith("GUIDE-007")

    def test_artifact_registry_is_not_duplicated_outside_workflows(self) -> None:
        self.write(
            "docs/project-map.md",
            """# Project map

This map orients readers to repository structure and boundaries. It does not own
workflow stage order, exact lifecycle artifact placement, or current milestone state.

```yaml
artifact_locations:
  proposal:
    path: docs/proposals/<change-id>.md
```
""",
        )

        self.assertFailsWith("GUIDE-008")


if __name__ == "__main__":
    unittest.main(verbosity=2)
