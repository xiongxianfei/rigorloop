"""Current model inventory and read-only boundary expectations."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# Independent inventory selected by System's current model composition.
EXPECTED_MODEL_PATHS = (
    'docs/design/system.md',
    'docs/design/skill/authoring/authoring.md',
    'docs/design/skill/authoring/proposal.md',
    'docs/design/skill/authoring/design.md',
    'docs/design/skill/authoring/plan.md',
    'docs/design/skill/workflow.md',
    'docs/design/skill/assessment.md',
    'docs/design/cli/records.md',
    'docs/design/cli/installation.md',
    'docs/design/engineering/validation.md',
    'docs/design/engineering/packaging.md',
    'docs/design/engineering/release/release.md',
    'docs/design/skill/skill.md',
    'docs/design/cli/cli.md',
    'docs/design/engineering/engineering.md',
    'docs/design/skill/project-foundations/project-foundations.md',
    'docs/design/skill/project-foundations/vision.md',
    'docs/design/skill/project-foundations/constitution.md',
    'docs/design/skill/project-foundations/project-map.md',
    'docs/design/skill/discovery/discovery.md',
    'docs/design/skill/discovery/explore.md',
    'docs/design/skill/discovery/research.md',
    'docs/design/skill/learning.md',
    'docs/design/skill/delivery-handoff.md',
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
