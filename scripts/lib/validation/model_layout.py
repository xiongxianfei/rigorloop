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
    "release": "docs/design/engineering/release/release.md",
    "skill": "docs/design/skill/skill.md",
    "cli": "docs/design/cli/cli.md",
    "engineering": "docs/design/engineering/engineering.md"
}

# Exact supporting-document declarations, not prefix-based model authority.
SHARED_TEST_DESIGN_PATHS = (
    'docs/design/test-design/README.md',
    'docs/design/test-design/rules.md',
)
TEST_DESIGN_PACKAGES = {
    'release': {
        'directory': 'docs/design/engineering/release/test-design',
        'entrypoint': 'tests/engineering/release/test-release-transaction.py',
        'groups': ('profile-input', 'preparation', 'preflight', 'candidate-identity',
                   'approval-recovery', 'evidence-closeout', 'maintenance-review'),
    },
    'skill': {
        'directory': 'docs/design/skill/test-design',
        'entrypoint': 'tests/skill/test-skill-validator.py',
        'groups': ('capability-contract', 'resource-contract', 'recording-composition',
                   'implementation-handoffs', 'capability-composition'),
    },
    'authoring': {
        'directory': 'docs/design/skill/authoring/test-design',
        'entrypoint': 'tests/skill/test-skill-validator.py',
        'groups': ('refinement', 'scope-handoff', 'correction-reconciliation'),
    },
}


def test_design_paths(model):
    package = TEST_DESIGN_PACKAGES[model]
    directory = package['directory']
    return (PROJECT_MODEL_PATHS[model], directory+'/test-design.md', directory+'/test-cases.json',
            *(directory+'/cases/'+group+'.json' for group in package['groups']))
