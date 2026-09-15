"""Declared repository model paths; no validator or runtime dependencies."""

# Explicit repository layout owned by System. Portable model paths remain valid.
PROJECT_MODEL_PATHS = {
    "system": "docs/design/system.md",
    "authoring": "docs/design/skill/authoring/authoring.md",
    "proposal": "docs/design/skill/authoring/proposal.md",
    "design": "docs/design/skill/authoring/design.md",
    "plan": "docs/design/skill/authoring/plan.md",
    "project-foundations": "docs/design/skill/project-foundations/project-foundations.md",
    "vision": "docs/design/skill/project-foundations/vision.md",
    "constitution": "docs/design/skill/project-foundations/constitution.md",
    "project-map": "docs/design/skill/project-foundations/project-map.md",
    "discovery": "docs/design/skill/discovery/discovery.md",
    "explore": "docs/design/skill/discovery/explore.md",
    "research": "docs/design/skill/discovery/research.md",
    "learning": "docs/design/skill/learning.md",
    "delivery-handoff": "docs/design/skill/delivery-handoff.md",
    "workflow": "docs/design/skill/workflow.md",
    "review-closeout": "docs/design/skill/assessment.md",
    "record-format": "docs/design/cli/records.md",
    "installation": "docs/design/cli/installation.md",
    "validation": "docs/design/engineering/validation.md",
    "packaging": "docs/design/engineering/packaging.md",
    "release": "docs/design/engineering/release.md",
    "skill": "docs/design/skill/skill.md",
    "cli": "docs/design/cli/cli.md",
    "engineering": "docs/design/engineering/engineering.md"
}

# Selection aliases for absent retired paths only, never accepted model locations.
RETIRED_MODEL_PATHS = {
    "docs/design/skill/design.md": "design",
}
