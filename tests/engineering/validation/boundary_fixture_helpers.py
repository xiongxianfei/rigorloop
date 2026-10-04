"""Current model inventory and read-only boundary expectations."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# Independent inventory selected by System's current model composition.
EXPECTED_MODEL_PATHS = (
    'design/architecture/composition.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/authoring.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/requirement-analysis.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/design-authoring.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/planning.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md',
    'design/architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md',
    'design/architecture/modules/MOD-019-product-delivery/modules/MOD-014-verified-skill-installation/installation.md',
    'design/support/validation.md',
    'design/architecture/modules/MOD-019-product-delivery/modules/MOD-013-product-package-production/packaging.md',
    'design/architecture/modules/MOD-019-product-delivery/modules/MOD-015-product-release-coordination/release.md',
    'design/architecture/modules/MOD-018-engineering-operations/modules/MOD-012-published-engineering-capability-guidance/capability-contract.md',
    'design/architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md',
    'design/support/development.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/project-foundations.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/vision.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/constitution.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/project-map.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/discovery.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/explore.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-008-engineering-authoring-guidance/research.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-009-engineering-learning/learning.md',
    'design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/delivery-handoff.md',
)


def relevant_tree_snapshot(root: Path) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    for top_level in ("specs", "dist", "docs"):
        base = root / top_level
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                snapshot[relative] = b"symlink:" + str(path.readlink()).encode("utf-8")
            elif path.is_file():
                snapshot[relative] = path.read_bytes()
            elif path.is_dir():
                snapshot[relative] = b"directory"
    return snapshot
