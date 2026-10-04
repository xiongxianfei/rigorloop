"""Declared supporting contract paths; keys are validation identities, not REM Modules."""

# Exact subordinate contract layout owned by design/support/ownership.md.
# Source-qualified contract keys and customer portable model paths remain valid.
PROJECT_MODEL_PATHS = {
    "system": "design/architecture/composition.md",
    "authoring": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/authoring.md",
    "proposal": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/requirement-analysis.md",
    "design": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md",
    "plan": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/planning.md",
    "project-foundations": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/project-foundations.md",
    "vision": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/vision.md",
    "constitution": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/constitution.md",
    "project-map": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/project-map.md",
    "discovery": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/discovery.md",
    "explore": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/explore.md",
    "research": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/research.md",
    "learning": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-009-engineering-learning/learning.md",
    "delivery-handoff": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/delivery-handoff.md",
    "workflow": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md",
    "review-closeout": "design/architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md",
    "record-format": "design/architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md",
    "installation": "design/architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md",
    "validation": "design/support/validation.md",
    "packaging": "design/architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md",
    "release": "design/architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/release.md",
    "skill": "design/architecture/modules/MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/capability-contract.md",
    "cli": "design/architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md",
    "engineering": "design/support/development.md"
}

# Exact supporting-document declarations, not prefix-based model authority.
SHARED_TEST_DESIGN_PATHS = (
    'design/support/test-design/README.md',
    'design/support/test-design/rules.md',
)
TEST_DESIGN_PACKAGES = {
    'release': {
        'directory': 'design/architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/test-design',
        'entrypoint': 'tests/engineering/release/test-release-transaction.py',
        'groups': ('profile-input', 'preparation', 'preflight', 'candidate-identity',
                   'approval-recovery', 'evidence-closeout', 'maintenance-review'),
    },
    'skill': {
        'directory': 'design/architecture/modules/MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/test-design',
        'entrypoint': 'tests/skill/test-skill-validator.py',
        'groups': ('capability-contract', 'resource-contract', 'recording-composition',
                   'implementation-handoffs', 'capability-composition'),
    },
    'authoring': {
        'directory': 'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/test-design',
        'entrypoint': 'tests/skill/test-skill-validator.py',
        'groups': ('refinement', 'scope-handoff', 'correction-reconciliation'),
    },
}


def test_design_paths(model):
    package = TEST_DESIGN_PACKAGES[model]
    directory = package['directory']
    return (PROJECT_MODEL_PATHS[model], directory+'/test-design.md', directory+'/test-cases.json',
            *(directory+'/cases/'+group+'.json' for group in package['groups']))


def supporting_architecture_json_paths(root):
    """Exact selected catalogs, separate from entity/facet discovery and validation."""
    return {root / path for model in TEST_DESIGN_PACKAGES
            for path in test_design_paths(model) if path.endswith('.json')}
