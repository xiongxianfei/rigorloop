"""Fresh portable records and read-only expectations for boundary scenarios."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "tests/engineering/validation/fixtures/boundary-first"

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


def valid_feature() -> str:
    dimensions = [
        "| input-domain | applicable | FIX-R001 | BND-INPUT-001 | - |",
        "| state-lifecycle | not-applicable | - | - | No state exists. |",
        "| identity-authority | not-applicable | - | - | No authority exists. |",
        "| composition-path | not-applicable | - | - | One path exists. |",
        "| temporal-retry | not-applicable | - | - | No retry exists. |",
        "| failure-recovery | not-applicable | - | - | No mutation exists. |",
        "| compatibility-migration | not-applicable | - | - | No history exists. |",
        "| external-environment | not-applicable | - | - | No dependency exists. |",
    ]
    return "\n".join(
        [
            "# Fixture",
            "",
            "## Status",
            "",
            "approved",
            "boundary_contract: boundary-first-v1",
            "",
            "## Boundary model",
            "",
            "Boundary model version: boundary-first-v1",
            "Boundary model scope: FIX-R001",
            "",
            "| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |",
            "| --- | --- | --- | --- | --- |",
            *dimensions,
            "",
            "## Boundary definitions",
            "",
            "| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            "| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |",
            "",
            "## Selected interactions",
            "",
            "No interaction selected: Only one boundary is applicable.",
            "",
            "## Example ownership",
            "",
            "| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |",
            "| --- | --- | --- | --- | --- | --- |",
            "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
            "",
        ]
    )


def valid_proof() -> str:
    return "\n".join(
        [
            "# Fixture proof",
            "",
            "Boundary model version: boundary-first-v1",
            "Boundary model scope: FIX-R001",
            "",
            "## Proof map",
            "",
            "| Proof obligation ID | Coverage state | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Proof level | Automation mode | Command IDs | Evidence artifact | Required milestone | Manual procedure IDs | Uncovered gap ID |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
            "",
        ]
    )
