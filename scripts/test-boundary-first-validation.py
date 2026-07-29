#!/usr/bin/env python3
"""Regression tests for boundary-first structural and activation validation."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from boundary_first_reference import (
    inventory_digest,
    projected_paths,
    raw_sha256,
)
from boundary_first_validation import (
    rollback_package_selection,
    validate_activation,
    validate_changed_spec,
    validate_feature_record,
    validate_proof_map,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "scripts" / "fixtures" / "boundary-first"


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


def copy_activation_surfaces(root: Path) -> None:
    (root / "specs" / "references").mkdir(parents=True)
    for relative in (
        Path("specs/boundary-first-activation.yaml"),
        Path("specs/boundary-first-resources.yaml"),
        Path("specs/boundary-first-proof-model.md"),
        Path("specs/references/boundary-first-method-v1.md"),
        Path("specs/references/boundary-first-feature-authoring-v1.md"),
        Path("specs/references/boundary-first-proof-v1.md"),
    ):
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / relative).read_bytes())
    for relative in projected_paths():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / relative).read_bytes())


def copy_rollback_surfaces(root: Path, version: str) -> None:
    manifest = root / "dist" / "adapters" / "manifest.yaml"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_bytes((ROOT / "dist" / "adapters" / "manifest.yaml").read_bytes())
    metadata = (
        root
        / "docs"
        / "reports"
        / "adapter-artifacts"
        / "releases"
        / f"{version}.yaml"
    )
    metadata.parent.mkdir(parents=True, exist_ok=True)
    source = (
        ROOT
        / "docs"
        / "reports"
        / "adapter-artifacts"
        / "releases"
        / "v0.3.5.yaml"
    ).read_text(encoding="utf-8")
    metadata.write_text(source.replace("v0.3.5", version), encoding="utf-8")


def initialize_active_fixture(
    root: Path,
    *,
    symlink_parent: bool = False,
    invalid_transition_snapshot: bool = False,
    bootstrap_release: str = "v0.9.0",
    rollback_release: str = "v1.0.0",
    activating_release: str = "v1.1.0",
) -> tuple[Path, str]:
    copy_activation_surfaces(root)
    copy_rollback_surfaces(root, rollback_release)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "fixture@example.test"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "bootstrap"], cwd=root, check=True)
    bootstrap = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    subprocess.run(["git", "tag", bootstrap_release, bootstrap], cwd=root, check=True)
    lifecycle_specs = {
        "accepted.md": "accepted",
        "approved.md": "approved",
        "active.md": "active",
        "draft.md": "draft",
        "é.md": "approved",
    }
    for name, status in lifecycle_specs.items():
        (root / "specs" / name).write_text(
            f"# {name}\n\n## Status\n\n{status}\n",
            encoding="utf-8",
        )
    (root / "specs" / "marked.md").write_text(valid_feature(), encoding="utf-8")
    (root / "specs" / "README.md").write_text("# index\n", encoding="utf-8")
    (root / "specs" / "ignored.test.md").write_text("# proof\n", encoding="utf-8")
    if symlink_parent:
        (root / "specs" / "symlinked.md").symlink_to("approved.md")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "parent"], cwd=root, check=True)
    baseline = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    subprocess.run(["git", "tag", rollback_release, baseline], cwd=root, check=True)
    (root / "specs" / "child.md").write_text(
        "# child\n\n## Status\n\napproved\n",
        encoding="utf-8",
    )
    proof_model = root / "specs" / "boundary-first-proof-model.md"
    proof_model.write_text(
        proof_model.read_text(encoding="utf-8").replace(
            "Boundary-first contract activation: pending",
            "Boundary-first contract activation: active",
        ),
        encoding="utf-8",
    )
    activation_path = root / "specs" / "boundary-first-activation.yaml"
    data = json.loads(activation_path.read_text(encoding="utf-8"))
    data.update(
        {
            "state": "active",
            "activating_release": activating_release,
            "rollback_release": rollback_release,
            "grandfathering_baseline_revision": (
                bootstrap if invalid_transition_snapshot else baseline
            ),
            "grandfathered_specs": (
                []
                if invalid_transition_snapshot
                else [
                    "specs/accepted.md",
                    "specs/active.md",
                    "specs/approved.md",
                    "specs/é.md",
                ]
            ),
        }
    )
    activation_path.write_text(json.dumps(data), encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "activate"], cwd=root, check=True)
    subprocess.run(["git", "tag", activating_release], cwd=root, check=True)
    return activation_path, baseline


def initialize_merge_activation_fixture(root: Path) -> Path:
    copy_activation_surfaces(root)
    copy_rollback_surfaces(root, "v1.0.0")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "fixture@example.test"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "pending"], cwd=root, check=True)
    main_branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    subprocess.run(["git", "tag", "v0.9.0"], cwd=root, check=True)
    subprocess.run(["git", "checkout", "-qb", "activation"], cwd=root, check=True)
    (root / "specs" / "branch.md").write_text(
        "# branch\n\n## Status\n\napproved\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "activation parent"], cwd=root, check=True)
    branch_parent = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    subprocess.run(["git", "tag", "v1.0.0"], cwd=root, check=True)
    proof_model = root / "specs" / "boundary-first-proof-model.md"
    proof_model.write_text(
        proof_model.read_text(encoding="utf-8").replace(
            "Boundary-first contract activation: pending",
            "Boundary-first contract activation: active",
        ),
        encoding="utf-8",
    )
    activation_path = root / "specs" / "boundary-first-activation.yaml"
    data = json.loads(activation_path.read_text(encoding="utf-8"))
    data.update(
        {
            "state": "active",
            "activating_release": "v1.1.0",
            "rollback_release": "v1.0.0",
            "grandfathering_baseline_revision": branch_parent,
            "grandfathered_specs": ["specs/branch.md"],
        }
    )
    activation_path.write_text(json.dumps(data), encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "activate branch"], cwd=root, check=True)
    subprocess.run(["git", "tag", "v1.1.0"], cwd=root, check=True)
    subprocess.run(["git", "checkout", "-q", main_branch], cwd=root, check=True)
    (root / "specs" / "main.md").write_text(
        "# main\n\n## Status\n\napproved\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "target parent"], cwd=root, check=True)
    subprocess.run(
        ["git", "merge", "--no-ff", "-qm", "integrate activation", "activation"],
        cwd=root,
        check=True,
    )
    return activation_path


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


class BoundaryFirstStructuralTests(unittest.TestCase):
    def test_durable_minimal_semantic_omission_and_gap_fixtures(self) -> None:
        minimal = (FIXTURES / "feature-records" / "minimal.md").read_text(
            encoding="utf-8"
        )
        semantic_omission = (
            FIXTURES / "feature-records" / "semantic-omission.md"
        ).read_text(encoding="utf-8")
        complex_feature = (
            FIXTURES / "feature-records" / "complex.md"
        ).read_text(encoding="utf-8")
        complete = (FIXTURES / "proof-maps" / "complete.md").read_text(
            encoding="utf-8"
        )
        complex_complete = (
            FIXTURES / "proof-maps" / "complex-complete.md"
        ).read_text(encoding="utf-8")
        gap = (FIXTURES / "proof-maps" / "gap.md").read_text(encoding="utf-8")
        self.assertEqual(validate_feature_record(minimal), ())
        self.assertEqual(validate_feature_record(semantic_omission), ())
        self.assertEqual(validate_feature_record(complex_feature), ())
        self.assertEqual(validate_proof_map(complete, minimal), ())
        self.assertEqual(
            validate_proof_map(complex_complete, complex_feature),
            (),
        )
        self.assertIn(
            "BFR-MISSING-DIRECT-PROOF",
            {issue.code for issue in validate_proof_map(gap, minimal)},
        )

    def test_valid_concise_feature_and_complete_proof_pass(self) -> None:
        feature = valid_feature()
        self.assertEqual(validate_feature_record(feature), ())
        self.assertEqual(validate_proof_map(valid_proof(), feature), ())

    def test_unknown_dimension_fails_before_consistency(self) -> None:
        text = valid_feature().replace("input-domain | applicable", "future-domain | applicable")
        issues = validate_feature_record(text)
        self.assertGreaterEqual(len(issues), 1)
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-DIMENSION")

    def test_unknown_applicability_fails_before_consistency(self) -> None:
        text = valid_feature().replace("input-domain | applicable", "input-domain | undecidable")
        issues = validate_feature_record(text)
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-APPLICABILITY")

    def test_unknown_contract_version_fails_before_consistency(self) -> None:
        issues = validate_feature_record(
            valid_feature().replace(
                "boundary_contract: boundary-first-v1",
                "boundary_contract: boundary-first-v2",
            )
        )
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-CONTRACT-VERSION")

    def test_marker_must_follow_lifecycle_value_inside_status(self) -> None:
        misplaced = valid_feature().replace(
            "approved\nboundary_contract: boundary-first-v1",
            "approved",
        ).replace(
            "## Boundary model",
            "## Boundary model\n\nboundary_contract: boundary-first-v1",
        )
        self.assertEqual(
            validate_feature_record(misplaced)[0].code,
            "BFR-MARKER-PLACEMENT",
        )
        duplicated = valid_feature().replace(
            "boundary_contract: boundary-first-v1",
            "boundary_contract: boundary-first-v1\nboundary_contract: boundary-first-v1",
            1,
        )
        self.assertEqual(
            validate_feature_record(duplicated)[0].code,
            "BFR-MARKER-COUNT",
        )

    def test_fenced_record_and_malformed_separator_fail_closed(self) -> None:
        fenced = "```md\n" + valid_feature() + "\n```\n"
        self.assertIn(
            validate_feature_record(fenced)[0].code,
            {"BFR-MARKER-COUNT", "BFR-MISSING-HEADING"},
        )
        malformed = valid_feature().replace(
            "| --- | --- | --- | --- | --- |",
            "| -- | --- | --- | --- | --- |",
            1,
        )
        self.assertEqual(
            validate_feature_record(malformed)[0].code,
            "BFR-INVALID-TABLE-SEPARATOR",
        )

    def test_valid_markdown_alignment_separators_pass(self) -> None:
        aligned_feature = valid_feature().replace(
            "| --- | --- | --- | --- | --- |",
            "| :--- | ---: | :---: | --- | --- |",
            1,
        )
        aligned_proof = valid_proof().replace(
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            "| :--- | ---: | :---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            1,
        )
        self.assertEqual(validate_feature_record(aligned_feature), ())
        self.assertEqual(
            validate_proof_map(aligned_proof, aligned_feature),
            (),
        )

    def test_unknown_model_version_fails_before_consistency(self) -> None:
        issues = validate_feature_record(
            valid_feature().replace(
                "Boundary model version: boundary-first-v1",
                "Boundary model version: boundary-first-v2",
            )
        )
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-MODEL-VERSION")

    def test_unknown_heading_fails_closed(self) -> None:
        issues = validate_feature_record(
            valid_feature().replace(
                "## Boundary definitions",
                "## Future boundary definitions",
            )
        )
        self.assertEqual(issues[0].code, "BFR-MISSING-HEADING")

    def test_unknown_column_fails_before_consistency(self) -> None:
        issues = validate_feature_record(
            valid_feature().replace(
                "| Dimension ID | Applicability |",
                "| Future dimension | Applicability |",
                1,
            )
        )
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-COLUMNS")

    def test_boundary_prefix_must_match_dimension(self) -> None:
        text = valid_feature().replace(
            "| BND-INPUT-001 | input-domain |",
            "| BND-STATE-001 | input-domain |",
        )
        issues = validate_feature_record(text)
        self.assertEqual(issues[0].code, "BFR-BOUNDARY-PREFIX-MISMATCH")

    def test_blank_and_unicode_sentinels_fail_closed(self) -> None:
        for sentinel in ("", "—"):
            with self.subTest(sentinel=sentinel or "blank"):
                text = valid_feature().replace(
                    "| state-lifecycle | not-applicable | - | - | No state exists. |",
                    f"| state-lifecycle | not-applicable | {sentinel} | - | No state exists. |",
                )
                self.assertEqual(
                    validate_feature_record(text)[0].code,
                    "BFR-INVALID-SENTINEL",
                )

    def test_extensions_and_imports_are_forbidden(self) -> None:
        for declaration in ("Extensions: future-domain", "Imports: other.md"):
            with self.subTest(declaration=declaration):
                text = valid_feature().replace(
                    "## Boundary definitions",
                    f"{declaration}\n\n## Boundary definitions",
                )
                self.assertEqual(
                    validate_feature_record(text)[0].code,
                    "BFR-FORBIDDEN-EXTENSION-IMPORT",
                )

    def test_boundary_record_headings_are_contiguous(self) -> None:
        text = valid_feature().replace(
            "## Boundary definitions",
            "## Interleaved notes\n\nNotes.\n\n## Boundary definitions",
        )
        self.assertEqual(
            validate_feature_record(text)[0].code,
            "BFR-NONCONTIGUOUS-RECORD",
        )

    def test_unknown_example_classification_fails_before_consistency(self) -> None:
        text = valid_feature().replace(
            "| FIX-E001 | illustration |",
            "| FIX-E001 | anecdote |",
        )
        self.assertEqual(
            validate_feature_record(text)[0].code,
            "BFR-UNKNOWN-EXAMPLE-CLASS",
        )

    def test_applicable_dimension_requires_requirement_and_boundary(self) -> None:
        text = valid_feature().replace(
            "| input-domain | applicable | FIX-R001 | BND-INPUT-001 | - |",
            "| input-domain | applicable | - | - | - |",
        )
        self.assertIn(
            "BFR-APPLICABLE-MISSING-OWNER",
            {issue.code for issue in validate_feature_record(text)},
        )

    def test_interaction_requires_two_defined_boundaries(self) -> None:
        text = valid_feature().replace(
            "No interaction selected: Only one boundary is applicable.",
            "\n".join(
                [
                    "| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |",
                    "| --- | --- | --- | --- | --- |",
                    "| INT-001 | FIX-R001 | BND-INPUT-001 | bypass | reject |",
                ]
            ),
        )
        self.assertIn(
            "BFR-INTERACTION-BOUNDARY-COUNT",
            {issue.code for issue in validate_feature_record(text)},
        )

    def test_duplicate_boundary_example_interaction_and_proof_ids_fail(self) -> None:
        duplicate_boundary = valid_feature().replace(
            "| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |",
            "\n".join(
                [
                    "| BND-INPUT-001 | input-domain | FIX-R001 | present | known values only | accept | FIX-R001 |",
                    "| BND-INPUT-001 | input-domain | FIX-R001 | missing | known values only | reject | FIX-R001 |",
                ]
            ),
        )
        self.assertIn(
            "BFR-DUPLICATE-BOUNDARY",
            {issue.code for issue in validate_feature_record(duplicate_boundary)},
        )
        duplicate_example = valid_feature().replace(
            "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
            "\n".join(
                [
                    "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
                    "| FIX-E001 | illustration | FIX-R001 | BND-INPUT-001 | - | - |",
                ]
            ),
        )
        self.assertIn(
            "BFR-DUPLICATE-EXAMPLE",
            {issue.code for issue in validate_feature_record(duplicate_example)},
        )
        duplicate_interaction = valid_feature().replace(
            "No interaction selected: Only one boundary is applicable.",
            "\n".join(
                [
                    "| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |",
                    "| --- | --- | --- | --- | --- |",
                    "| INT-001 | FIX-R001 | BND-INPUT-001 | bypass | reject |",
                    "| INT-001 | FIX-R001 | BND-INPUT-001 | retry | reject |",
                ]
            ),
        )
        self.assertIn(
            "BFR-DUPLICATE-INTERACTION",
            {issue.code for issue in validate_feature_record(duplicate_interaction)},
        )
        duplicate_proof = valid_proof().replace(
            "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
            "\n".join(
                [
                    "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
                    "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T2 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
                ]
            ),
        )
        self.assertIn(
            "BFR-DUPLICATE-PROOF",
            {issue.code for issue in validate_proof_map(duplicate_proof, valid_feature())},
        )

    def test_semantic_omission_is_not_a_structural_error(self) -> None:
        text = valid_feature().replace(
            "No interaction selected: Only one boundary is applicable.",
            "No interaction selected: Reviewer must judge whether a hidden hazard exists.",
        )
        self.assertEqual(validate_feature_record(text), ())

    def test_unknown_proof_vocabulary_fails_first(self) -> None:
        text = valid_proof().replace("| PRF-001 | covered |", "| PRF-001 | future |")
        issues = validate_proof_map(text, valid_feature())
        self.assertEqual(issues[0].code, "BFR-UNKNOWN-COVERAGE")

    def test_unknown_proof_level_and_automation_fail_closed(self) -> None:
        mutations = (
            ("| unit | automated |", "| future | automated |", "BFR-UNKNOWN-PROOF-LEVEL"),
            ("| unit | automated |", "| unit | delegated |", "BFR-UNKNOWN-AUTOMATION-MODE"),
        )
        for old, new, expected in mutations:
            with self.subTest(expected=expected):
                issues = validate_proof_map(
                    valid_proof().replace(old, new),
                    valid_feature(),
                )
                self.assertEqual(issues[0].code, expected)

    def test_malformed_feature_does_not_crash_proof_validation(self) -> None:
        malformed_feature = valid_feature().replace(
            "| BND-INPUT-001 | input-domain | FIX-R001 | present, missing, unknown | known values only | accept, reject | FIX-R001 |",
            "| BND-INPUT-001 | input-domain |",
        )
        issues = validate_proof_map(valid_proof(), malformed_feature)
        self.assertTrue(issues)
        self.assertEqual(issues[0].code, "BFR-ROW-SHAPE")

    def test_proof_reference_serialization_and_gap_id_are_vocabulary_checked(
        self,
    ) -> None:
        feature = (FIXTURES / "feature-records" / "complex.md").read_text(
            encoding="utf-8"
        )
        proof = (FIXTURES / "proof-maps" / "complex-complete.md").read_text(
            encoding="utf-8"
        )
        malformed_refs = proof.replace(
            "BND-INPUT-001, BND-STATE-001",
            "BND-INPUT-001,BND-STATE-001",
        )
        # Use a valid multi-reference proof row so the mutation reaches the
        # proof-reference vocabulary rather than feature consistency.
        malformed_refs = malformed_refs.replace(
            "INT-001 | T3",
            "BND-INPUT-001,BND-STATE-001 | T3",
        )
        self.assertEqual(
            validate_proof_map(malformed_refs, feature)[0].code,
            "BFR-INVALID-PROOF-REFERENCE",
        )
        gap = (FIXTURES / "proof-maps" / "gap.md").read_text(encoding="utf-8")
        invalid_gap = gap.replace("FIX-GAP-001", "not a stable id")
        self.assertEqual(
            validate_proof_map(
                invalid_gap,
                (FIXTURES / "feature-records" / "minimal.md").read_text(
                    encoding="utf-8"
                ),
            )[0].code,
            "BFR-INVALID-GAP-ID",
        )

    def test_gap_row_cannot_carry_proof_metadata(self) -> None:
        text = valid_proof().replace(
            "| PRF-001 | covered | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | - |",
            "| PRF-001 | gap | FIX-R001 | BND-INPUT-001 | T1 | unit | automated | CMD1 | fixture-evidence | M3 | - | FIX-GAP-001 |",
        )
        self.assertIn(
            "BFR-GAP-HAS-PROOF",
            {issue.code for issue in validate_proof_map(text, valid_feature())},
        )

    def test_cross_feature_boundary_reference_fails(self) -> None:
        text = valid_proof().replace("BND-INPUT-001 | T1", "BND-STATE-999 | T1")
        self.assertIn(
            "BFR-UNKNOWN-BOUNDARY-REFERENCE",
            {issue.code for issue in validate_proof_map(text, valid_feature())},
        )

    def test_automated_proof_rejects_manual_procedure(self) -> None:
        text = valid_proof().replace("| M3 | - | - |", "| M3 | FIX-MANUAL-001 | - |")
        self.assertIn(
            "BFR-AUTOMATED-MANUAL-PROCEDURE",
            {issue.code for issue in validate_proof_map(text, valid_feature())},
        )


class BoundaryFirstActivationTests(unittest.TestCase):
    def test_repository_pending_activation_record_passes(self) -> None:
        self.assertEqual(validate_activation(ROOT), ())

    def test_unknown_activation_state_fails_before_consistency(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            source = ROOT / "specs" / "boundary-first-activation.yaml"
            data = json.loads(source.read_text(encoding="utf-8"))
            fixture = json.loads(
                (FIXTURES / "activation" / "unknown-state.yaml").read_text(
                    encoding="utf-8"
                )
            )
            data["state"] = fixture["state"]
            (root / "specs" / "boundary-first-activation.yaml").write_text(
                json.dumps(data), encoding="utf-8"
            )
            issues = validate_activation(root)
            self.assertEqual(issues[0].code, "BFR-UNKNOWN-ACTIVATION-STATE")

    def test_unknown_activation_contract_and_consumer_fail_closed(self) -> None:
        source = ROOT / "specs" / "boundary-first-activation.yaml"
        for field, value, expected in (
            ("contract_version", "boundary-first-v2", "BFR-UNKNOWN-CONTRACT-VERSION"),
            ("governed_skills", ["workflow", "future"], "BFR-UNKNOWN-GOVERNED-SKILL"),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                (root / "specs").mkdir()
                data = json.loads(source.read_text(encoding="utf-8"))
                data[field] = value
                (root / "specs" / "boundary-first-activation.yaml").write_text(
                    json.dumps(data), encoding="utf-8"
                )
                self.assertEqual(validate_activation(root)[0].code, expected)

    def test_unknown_activation_field_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            data = json.loads(
                (ROOT / "specs" / "boundary-first-activation.yaml").read_text(
                    encoding="utf-8"
                )
            )
            data["future_inventory"] = []
            (root / "specs" / "boundary-first-activation.yaml").write_text(
                json.dumps(data),
                encoding="utf-8",
            )
            self.assertEqual(
                validate_activation(root)[0].code,
                "BFR-ACTIVATION-FIELDS",
            )

    def test_manifest_path_and_hash_must_match_projection_authority(self) -> None:
        source = ROOT / "specs" / "boundary-first-activation.yaml"
        for field, value, expected in (
            (
                "resource_manifest",
                "specs/future-resources.yaml",
                "BFR-RESOURCE-MANIFEST-PATH",
            ),
            (
                "resource_manifest_sha256",
                "0" * 64,
                "BFR-RESOURCE-MANIFEST-HASH",
            ),
        ):
            with (
                self.subTest(field=field),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = Path(temporary)
                copy_activation_surfaces(root)
                data = json.loads(source.read_text(encoding="utf-8"))
                data[field] = value
                (
                    root / "specs" / "boundary-first-activation.yaml"
                ).write_text(json.dumps(data), encoding="utf-8")
                self.assertIn(
                    expected,
                    {issue.code for issue in validate_activation(root)},
                )

    def test_activation_preserves_manifest_error_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_activation_surfaces(root)
            manifest = root / "specs/boundary-first-resources.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "contract_version: boundary-first-v1",
                    "contract_version: boundary-first-v2",
                ),
                encoding="utf-8",
            )

            issue = validate_activation(root)[0]

            self.assertEqual(
                issue.code,
                "BFR-MANIFEST-CONTRACT-VERSION-UNKNOWN",
            )
            self.assertEqual(
                issue.path,
                "specs/boundary-first-resources.yaml",
            )
            self.assertIn("boundary-first-v1", issue.expected)

    def test_active_manifest_uses_parent_inventory_and_immediate_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_active_fixture(root)
            self.assertEqual(validate_activation(root), ())

    def test_child_cannot_self_grandfather_and_all_parent_statuses_are_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            activation_path, _ = initialize_active_fixture(root)
            data = json.loads(activation_path.read_text(encoding="utf-8"))
            for inventory in (
                [
                    "specs/accepted.md",
                    "specs/active.md",
                    "specs/approved.md",
                ],
                [
                    "specs/accepted.md",
                    "specs/active.md",
                    "specs/approved.md",
                    "specs/child.md",
                    "specs/é.md",
                ],
                [
                    "specs/accepted.md",
                    "specs/active.md",
                    "specs/approved.md",
                    "specs/draft.md",
                    "specs/é.md",
                ],
            ):
                with self.subTest(inventory=inventory):
                    data["grandfathered_specs"] = inventory
                    activation_path.write_text(json.dumps(data), encoding="utf-8")
                    self.assertIn(
                        "BFR-GRANDFATHERED-MEMBERSHIP",
                        {issue.code for issue in validate_activation(root)},
                    )

    def test_older_rollback_release_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            activation_path, _ = initialize_active_fixture(root)
            data = json.loads(activation_path.read_text(encoding="utf-8"))
            data["rollback_release"] = "v0.9.0"
            activation_path.write_text(json.dumps(data), encoding="utf-8")
            self.assertIn(
                "BFR-ROLLBACK-RELEASE",
                {issue.code for issue in validate_activation(root)},
            )

    def test_release_tags_must_exist_and_be_adjacent(self) -> None:
        for activating, rollback in (
            ("v2.0.0", "v1.1.0"),
            ("v1.1.0", "v1.1.0"),
        ):
            with (
                self.subTest(activating=activating, rollback=rollback),
                tempfile.TemporaryDirectory() as temporary,
            ):
                root = Path(temporary)
                activation_path, _ = initialize_active_fixture(root)
                data = json.loads(activation_path.read_text(encoding="utf-8"))
                data["activating_release"] = activating
                data["rollback_release"] = rollback
                activation_path.write_text(json.dumps(data), encoding="utf-8")
                self.assertTrue(
                    {"BFR-ACTIVATING-RELEASE", "BFR-ROLLBACK-RELEASE"}
                    & {issue.code for issue in validate_activation(root)}
                )

    def test_baseline_must_be_exact_transition_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            activation_path, baseline = initialize_active_fixture(root)
            child = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            grandparent = subprocess.run(
                ["git", "rev-parse", f"{baseline}^"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            original = json.loads(activation_path.read_text(encoding="utf-8"))
            for invalid in (7, child, grandparent):
                with self.subTest(invalid=invalid):
                    data = dict(original)
                    data["grandfathering_baseline_revision"] = invalid
                    activation_path.write_text(json.dumps(data), encoding="utf-8")
                    self.assertTrue(
                        {"BFR-BASELINE-REVISION", "BFR-BASELINE-PARENT"}
                        & {issue.code for issue in validate_activation(root)}
                    )

    def test_merge_activation_uses_integration_first_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_merge_activation_fixture(root)
            codes = {issue.code for issue in validate_activation(root)}
            self.assertIn("BFR-BASELINE-PARENT", codes)
            self.assertIn("BFR-ACTIVATING-TAG-COMMIT", codes)
            self.assertIn("BFR-GRANDFATHERED-MEMBERSHIP", codes)

    def test_activating_tag_and_release_fields_are_transition_immutable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_active_fixture(root)
            pending = subprocess.run(
                ["git", "rev-parse", "v0.9.0"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            subprocess.run(
                ["git", "tag", "-f", "v1.1.0", pending],
                cwd=root,
                check=True,
                capture_output=True,
            )
            self.assertIn(
                "BFR-ACTIVATING-TAG-COMMIT",
                {issue.code for issue in validate_activation(root)},
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            activation_path, _ = initialize_active_fixture(root)
            data = json.loads(activation_path.read_text(encoding="utf-8"))
            data["activating_release"] = "v1.2.0"
            data["rollback_release"] = "v1.1.0"
            activation_path.write_text(json.dumps(data), encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "rewrite releases"], cwd=root, check=True)
            subprocess.run(["git", "tag", "v1.2.0"], cwd=root, check=True)
            self.assertIn(
                "BFR-ACTIVATION-IMMUTABLE",
                {issue.code for issue in validate_activation(root)},
            )

    def test_invalid_transition_snapshot_cannot_be_repaired_later(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            activation_path, baseline = initialize_active_fixture(
                root,
                invalid_transition_snapshot=True,
            )
            data = json.loads(activation_path.read_text(encoding="utf-8"))
            data["grandfathering_baseline_revision"] = baseline
            data["grandfathered_specs"] = [
                "specs/accepted.md",
                "specs/active.md",
                "specs/approved.md",
                "specs/é.md",
            ]
            activation_path.write_text(json.dumps(data), encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "repair active snapshot"], cwd=root, check=True)

            codes = {issue.code for issue in validate_activation(root)}
            self.assertIn("BFR-BASELINE-PARENT", codes)
            self.assertIn("BFR-GRANDFATHERED-MEMBERSHIP", codes)
            self.assertIn("BFR-ACTIVATION-IMMUTABLE", codes)

    def test_active_rollback_release_matches_current_adapter_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_active_fixture(
                root,
                bootstrap_release="v0.3.4",
                rollback_release="v0.3.5",
                activating_release="v0.3.6",
            )
            before = relevant_tree_snapshot(root)

            selection, issues = rollback_package_selection(root)

            self.assertEqual(issues, ())
            self.assertIsNotNone(selection)
            assert selection is not None
            self.assertEqual(selection.release, "v0.3.5")
            self.assertEqual(
                tuple(row.adapter for row in selection.artifacts),
                ("claude", "codex", "opencode"),
            )
            self.assertEqual(
                tuple(row.archive for row in selection.artifacts),
                tuple(
                    f"rigorloop-adapter-{adapter}-v0.3.5.zip"
                    for adapter in ("claude", "codex", "opencode")
                ),
            )
            self.assertTrue(
                all(
                    re.fullmatch(r"[0-9a-f]{64}", row.sha256)
                    for row in selection.artifacts
                )
            )
            self.assertEqual(before, relevant_tree_snapshot(root))

    def test_rollback_metadata_rejects_incomplete_or_mixed_matrices_without_mutation(self) -> None:
        source_metadata = (
            ROOT
            / "docs"
            / "reports"
            / "adapter-artifacts"
            / "releases"
            / "v0.3.5.yaml"
        )
        original = source_metadata.read_text(encoding="utf-8")
        codex_block = re.search(
            r"  - adapter: codex\n(?:    .+\n){4}",
            original,
        )
        self.assertIsNotNone(codex_block)
        assert codex_block is not None
        cases = {
            "missing": re.sub(
                r"  - adapter: claude\n(?:    .+\n){4}",
                "",
                original,
                count=1,
            ),
            "additional": original.replace(
                "\ncombined_artifact:",
                "\n"
                "  - adapter: extra\n"
                "    archive: rigorloop-adapter-extra-v0.3.5.zip\n"
                f"    sha256: {'a' * 64}\n"
                "    install_root: .extra/skills/\n"
                "    result: pass\n"
                "\ncombined_artifact:",
                1,
            ),
            "duplicated": original.replace(
                codex_block.group(0),
                codex_block.group(0) + codex_block.group(0),
                1,
            ),
            "failing": original.replace("    result: pass", "    result: fail", 1),
            "mixed-version": original.replace(
                "  version: v0.3.5",
                "  version: v0.3.4",
                1,
            ),
        }
        for name, metadata_text in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                initialize_active_fixture(
                    root,
                    bootstrap_release="v0.3.4",
                    rollback_release="v0.3.5",
                    activating_release="v0.3.6",
                )
                metadata = (
                    root
                    / "docs"
                    / "reports"
                    / "adapter-artifacts"
                    / "releases"
                    / "v0.3.5.yaml"
                )
                metadata.write_text(metadata_text, encoding="utf-8")
                before = relevant_tree_snapshot(root)

                selection, issues = rollback_package_selection(root)

                self.assertIsNone(selection)
                self.assertTrue(issues, name)
                self.assertEqual(before, relevant_tree_snapshot(root))

    def test_rollback_authoritative_paths_fail_closed_without_mutation(self) -> None:
        relative_paths = (
            Path("dist/adapters/manifest.yaml"),
            Path("docs/reports/adapter-artifacts/releases/v0.3.5.yaml"),
        )
        for relative_path in relative_paths:
            for mutation in ("missing", "directory", "symlink"):
                with (
                    self.subTest(path=relative_path, mutation=mutation),
                    tempfile.TemporaryDirectory() as temporary,
                ):
                    outer = Path(temporary)
                    root = outer / "repository"
                    root.mkdir()
                    initialize_active_fixture(
                        root,
                        bootstrap_release="v0.3.4",
                        rollback_release="v0.3.5",
                        activating_release="v0.3.6",
                    )
                    target = root / relative_path
                    target.unlink()
                    outside = outer / "outside-sentinel"
                    outside.write_bytes(b"outside remains unchanged\n")
                    if mutation == "directory":
                        target.mkdir()
                    elif mutation == "symlink":
                        target.symlink_to(outside)
                    before = relevant_tree_snapshot(root)
                    outside_before = outside.read_bytes()

                    selection, issues = rollback_package_selection(root)

                    self.assertIsNone(selection)
                    self.assertIn(
                        "BFR-ROLLBACK-PATH-UNSAFE",
                        {issue.code for issue in issues},
                    )
                    self.assertEqual(before, relevant_tree_snapshot(root))
                    self.assertEqual(outside_before, outside.read_bytes())

    def test_active_validation_cli_emits_authoritative_rollback_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_active_fixture(
                root,
                bootstrap_release="v0.3.4",
                rollback_release="v0.3.5",
                activating_release="v0.3.6",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate-boundary-first.py"),
                    "--check",
                    "--root",
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output["rollback_release"], "v0.3.5")
            self.assertEqual(
                tuple(row["adapter"] for row in output["rollback_artifacts"]),
                ("claude", "codex", "opencode"),
            )

            (
                root
                / "docs"
                / "reports"
                / "adapter-artifacts"
                / "releases"
                / "v0.3.5.yaml"
            ).unlink()
            failed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate-boundary-first.py"),
                    "--check",
                    "--root",
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("BFR-ROLLBACK-PATH-UNSAFE", failed.stdout)

    def test_unicode_parent_path_is_inventoried_and_symlink_mode_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_active_fixture(root)
            self.assertEqual(validate_activation(root), ())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_active_fixture(root, symlink_parent=True)
            self.assertIn(
                "BFR-BASELINE-MODE",
                {issue.code for issue in validate_activation(root)},
            )

    def test_grandfathered_inventory_requires_raw_utf8_order_and_uniqueness(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            activation_path, _ = initialize_active_fixture(root)
            data = json.loads(activation_path.read_text(encoding="utf-8"))
            for inventory in (
                ["specs/active.md", "specs/accepted.md", "specs/approved.md"],
                [
                    "specs/accepted.md",
                    "specs/accepted.md",
                    "specs/approved.md",
                    "specs/é.md",
                ],
            ):
                with self.subTest(inventory=inventory):
                    data["grandfathered_specs"] = inventory
                    activation_path.write_text(json.dumps(data), encoding="utf-8")
                    self.assertIn(
                        "BFR-GRANDFATHERED-ORDER",
                        {issue.code for issue in validate_activation(root)},
                    )

    def test_mixed_projection_bytes_fail_even_with_recomputed_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_activation_surfaces(root)
            changed = root / projected_paths()[0]
            changed.write_text("# divergent\n", encoding="utf-8")
            data = json.loads(
                (root / "specs" / "boundary-first-activation.yaml").read_text(
                    encoding="utf-8"
                )
            )
            records = {
                relative.as_posix(): raw_sha256((root / relative).read_bytes())
                for relative in projected_paths()
            }
            data["projection_sha256"] = inventory_digest(records)
            (root / "specs" / "boundary-first-activation.yaml").write_text(
                json.dumps(data), encoding="utf-8"
            )
            self.assertIn(
                "BFR-PROJECTION-DIVERGENT",
                {issue.code for issue in validate_activation(root)},
            )

    def test_issue_evidence_is_privacy_bounded(self) -> None:
        issue = validate_feature_record(
            valid_feature().replace("input-domain | applicable", "secret | applicable"),
            path="specs/fixture.md",
        )[0]
        self.assertEqual(
            set(issue.as_dict()),
            {"check_id", "path", "message", "offending_value", "expected"},
        )

    def test_changed_grandfathered_spec_routes_to_semantic_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            spec_path = root / "specs" / "historical.md"
            spec_path.write_text("# Historical\n", encoding="utf-8")
            data = json.loads(
                (ROOT / "specs" / "boundary-first-activation.yaml").read_text(
                    encoding="utf-8"
                )
            )
            data["state"] = "active"
            data["grandfathered_specs"] = ["specs/historical.md"]
            (root / "specs" / "boundary-first-activation.yaml").write_text(
                json.dumps(data), encoding="utf-8"
            )
            issues = validate_changed_spec(root, "specs/historical.md")
            self.assertEqual(issues[0].code, "BFR-GRANDFATHERED-REVIEW")

    def test_changed_adopting_test_spec_validates_against_feature(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            feature = (FIXTURES / "feature-records" / "minimal.md").read_text(
                encoding="utf-8"
            )
            proof = (FIXTURES / "proof-maps" / "complete.md").read_text(
                encoding="utf-8"
            )
            (root / "specs" / "feature.md").write_text(feature, encoding="utf-8")
            (root / "specs" / "feature.test.md").write_text(
                proof, encoding="utf-8"
            )
            data = json.loads(
                (ROOT / "specs" / "boundary-first-activation.yaml").read_text(
                    encoding="utf-8"
                )
            )
            data["state"] = "active"
            (root / "specs" / "boundary-first-activation.yaml").write_text(
                json.dumps(data), encoding="utf-8"
            )
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md"),
                (),
            )

    def test_pending_marker_gate_applies_to_changed_test_spec(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            (root / "specs" / "feature.md").write_text(
                valid_feature(), encoding="utf-8"
            )
            (root / "specs" / "feature.test.md").write_text(
                valid_proof(), encoding="utf-8"
            )
            (root / "specs" / "boundary-first-activation.yaml").write_bytes(
                (ROOT / "specs" / "boundary-first-activation.yaml").read_bytes()
            )
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md")[0].code,
                "BFR-MARKER-INACTIVE",
            )

    def test_changed_spec_paths_are_repository_contained(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            (root / "specs" / "boundary-first-activation.yaml").write_bytes(
                (ROOT / "specs" / "boundary-first-activation.yaml").read_bytes()
            )
            outside = root.parent / "outside-boundary-first.md"
            outside.write_text("# outside\n", encoding="utf-8")
            self.addCleanup(outside.unlink, missing_ok=True)
            for path in (
                "/etc/passwd",
                "../outside-boundary-first.md",
                "README.md",
            ):
                with self.subTest(path=path):
                    self.assertEqual(
                        validate_changed_spec(root, path)[0].code,
                        "BFR-INVALID-CHANGED-PATH",
                    )
            (root / "specs" / "escape.md").symlink_to(outside)
            self.assertEqual(
                validate_changed_spec(root, "specs/escape.md")[0].code,
                "BFR-CHANGED-PATH-ESCAPE",
            )

    def test_derived_feature_and_proof_paths_are_contained(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            (root / "specs" / "boundary-first-activation.yaml").write_bytes(
                (ROOT / "specs" / "boundary-first-activation.yaml").read_bytes()
            )
            outside = root.parent / "outside-boundary-companion.md"
            outside.write_text(valid_feature(), encoding="utf-8")
            self.addCleanup(outside.unlink, missing_ok=True)
            (root / "specs" / "feature.md").symlink_to(outside)
            (root / "specs" / "feature.test.md").write_text(
                valid_proof(), encoding="utf-8"
            )
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md")[0].code,
                "BFR-CHANGED-PATH-ESCAPE",
            )
            (root / "specs" / "feature.md").unlink()
            (root / "specs" / "feature.md").write_text(
                valid_feature(), encoding="utf-8"
            )
            (root / "specs" / "feature.test.md").unlink()
            (root / "specs" / "feature.test.md").symlink_to(outside)
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.md")[0].code,
                "BFR-CHANGED-PATH-ESCAPE",
            )

    def test_deleted_adopting_proof_and_orphaned_test_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            data = json.loads(
                (ROOT / "specs" / "boundary-first-activation.yaml").read_text(
                    encoding="utf-8"
                )
            )
            data["state"] = "active"
            (root / "specs" / "boundary-first-activation.yaml").write_text(
                json.dumps(data), encoding="utf-8"
            )
            feature_path = root / "specs" / "feature.md"
            proof_path = root / "specs" / "feature.test.md"
            feature_path.write_text(valid_feature(), encoding="utf-8")
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md")[0].code,
                "BFR-PROOF-MAP-MISSING",
            )
            feature_path.unlink()
            proof_path.write_text(valid_proof(), encoding="utf-8")
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md")[0].code,
                "BFR-FEATURE-CONTRACT-MISSING",
            )
            proof_path.unlink()
            self.assertEqual(
                validate_changed_spec(root, "specs/feature.test.md"),
                (),
            )

    def test_fixed_authoritative_inputs_reject_external_symlinks(self) -> None:
        for relative in (
            Path("specs/boundary-first-activation.yaml"),
            Path("specs/boundary-first-proof-model.md"),
        ):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                copy_activation_surfaces(root)
                outside = root.parent / f"{root.name}-{relative.name}"
                outside.write_bytes((root / relative).read_bytes())
                self.addCleanup(outside.unlink, missing_ok=True)
                (root / relative).unlink()
                (root / relative).symlink_to(outside)
                self.assertEqual(
                    validate_activation(root)[0].code,
                    "BFR-AUTHORITATIVE-PATH-UNSAFE",
                )
                if relative == Path("specs/boundary-first-activation.yaml"):
                    (root / "specs" / "feature.md").write_text(
                        valid_feature(),
                        encoding="utf-8",
                    )
                    self.assertEqual(
                        validate_changed_spec(root, "specs/feature.md")[0].code,
                        "BFR-AUTHORITATIVE-PATH-UNSAFE",
                    )

    def test_specs_root_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            outside_specs = root.parent / f"{root.name}-outside-specs"
            shutil.copytree(ROOT / "specs", outside_specs)
            self.addCleanup(shutil.rmtree, outside_specs, ignore_errors=True)
            (root / "specs").symlink_to(outside_specs, target_is_directory=True)
            self.assertEqual(
                validate_activation(root)[0].code,
                "BFR-SPECS-ROOT-UNSAFE",
            )

    def test_serialized_issue_redacts_private_payload(self) -> None:
        secret = "credential=super-secret-private-value"
        issue = validate_feature_record(
            valid_feature().replace("input-domain | applicable", f"{secret} | applicable"),
            path="specs/fixture.md",
        )[0]
        serialized = json.dumps(issue.as_dict(), sort_keys=True)
        self.assertNotIn(secret, serialized)
        self.assertIn("redacted:sha256:", serialized)


if __name__ == "__main__":
    unittest.main(verbosity=2)
