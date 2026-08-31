#!/usr/bin/env python3
"""Regression tests for boundary-first structural and activation validation."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from adapter_distribution import parse_adapter_artifact_metadata_yaml
from boundary_first_reference import (
    GOVERNED_SKILLS,
    inventory_digest,
    load_resource_manifest,
    projected_paths,
    raw_sha256,
)
from boundary_first_validation import (
    derive_grandfathered_specs,
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
    source_path = (
        ROOT
        / "docs"
        / "reports"
        / "adapter-artifacts"
        / "releases"
        / f"{version}.yaml"
    )
    metadata.write_bytes(source_path.read_bytes())


def initialize_checked_revision_active_fixture(root: Path) -> Path:
    """Build a coherent active current tree without history, tags, or remotes."""

    copy_activation_surfaces(root)
    copy_rollback_surfaces(root, "v0.3.6")
    activation_path = root / "specs" / "boundary-first-activation.yaml"
    data = json.loads(activation_path.read_text(encoding="utf-8"))
    data.update(
        {
            "state": "active",
            "activating_release": "v0.4.0",
            "rollback_release": "v0.3.6",
            "grandfathering_baseline_revision": "a" * 40,
            "grandfathered_specs": [],
        }
    )
    activation_path.write_text(json.dumps(data), encoding="utf-8")
    proof_model = root / "specs" / "boundary-first-proof-model.md"
    proof_model.write_text(
        proof_model.read_text(encoding="utf-8").replace(
            "Boundary-first contract activation: pending",
            "Boundary-first contract activation: active",
        ),
        encoding="utf-8",
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

    def test_stage_owned_marker_requires_matching_lifecycle_contract(self) -> None:
        stage_owned = valid_feature().replace(
            "## Status\n\napproved\nboundary_contract: boundary-first-v1",
            "## Owning change record\n\n"
            "`docs/changes/2026-08-06-example/change.yaml`\n\n"
            "boundary_contract: boundary-first-v1",
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            change_path = root / "docs/changes/2026-08-06-example/change.yaml"
            change_path.parent.mkdir(parents=True)
            change_path.write_text(
                "change_id: 2026-08-06-example\n"
                "lifecycle_contract: stage-owned-change-local-v1\n",
                encoding="utf-8",
            )

            self.assertEqual(
                validate_feature_record(
                    stage_owned,
                    "specs/example.md",
                    root=root,
                ),
                (),
            )

            stage_owned_status = valid_feature().replace(
                "## Status",
                "## Owning change record\n\n"
                "`docs/changes/2026-08-06-example/change.yaml`\n\n"
                "## Status",
                1,
            )
            self.assertEqual(
                validate_feature_record(
                    stage_owned_status,
                    "specs/example.md",
                    root=root,
                )[0].code,
                "BFR-MARKER-PLACEMENT",
            )

            change_path.write_text(
                "change_id: 2026-08-06-example\n"
                "lifecycle_contract : stage-owned-change-local-v1\n",
                encoding="utf-8",
            )
            self.assertEqual(
                validate_feature_record(
                    stage_owned,
                    "specs/example.md",
                    root=root,
                ),
                (),
            )
            self.assertEqual(
                validate_feature_record(
                    stage_owned_status,
                    "specs/example.md",
                    root=root,
                )[0].code,
                "BFR-MARKER-PLACEMENT",
            )

            before_pointer = stage_owned.replace(
                "`docs/changes/2026-08-06-example/change.yaml`\n\n"
                "boundary_contract: boundary-first-v1",
                "boundary_contract: boundary-first-v1\n\n"
                "`docs/changes/2026-08-06-example/change.yaml`",
            )
            self.assertEqual(
                validate_feature_record(
                    before_pointer,
                    "specs/example.md",
                    root=root,
                )[0].code,
                "BFR-MARKER-PLACEMENT",
            )

            change_path.unlink()
            self.assertEqual(
                validate_feature_record(
                    stage_owned,
                    "specs/example.md",
                    root=root,
                )[0].code,
                "BFR-MARKER-AUTHORITY",
            )
            change_path.write_text(
                "change_id: 2026-08-06-example\n",
                encoding="utf-8",
            )
            self.assertEqual(
                validate_feature_record(
                    stage_owned,
                    "specs/example.md",
                    root=root,
                )[0].code,
                "BFR-MARKER-AUTHORITY",
            )
            self.assertEqual(
                validate_feature_record(
                    stage_owned_status,
                    "specs/example.md",
                    root=root,
                ),
                (),
            )

            change_path.write_text(
                "change_id: 2026-08-06-example\n"
                'lifecycle_contract: "stage-owned-change-local-v1"\n',
                encoding="utf-8",
            )
            self.assertEqual(
                validate_feature_record(
                    stage_owned,
                    "specs/example.md",
                    root=root,
                ),
                (),
            )
            self.assertEqual(
                validate_feature_record(
                    stage_owned_status,
                    "specs/example.md",
                    root=root,
                )[0].code,
                "BFR-MARKER-PLACEMENT",
            )

    def test_unknown_value_lifecycle_contract_fails_before_marker_consistency(self) -> None:
        stage_owned_status = valid_feature().replace(
            "## Status",
            "## Owning change record\n\n"
            "`docs/changes/2026-08-06-example/change.yaml`\n\n"
            "## Status",
            1,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            change_path = root / "docs/changes/2026-08-06-example/change.yaml"
            change_path.parent.mkdir(parents=True)
            for case, contract in (
                ("canonical unknown", "lifecycle_contract: future-contract-v2\n"),
                ("spaced unknown", "lifecycle_contract : future-contract-v2\n"),
                ("spaced malformed", 'lifecycle_contract : "unterminated\n'),
                (
                    "mixed duplicate",
                    "lifecycle_contract: stage-owned-change-local-v1\n"
                    "lifecycle_contract : stage-owned-change-local-v1\n",
                ),
            ):
                with self.subTest(case=case):
                    change_path.write_text(
                        "change_id: 2026-08-06-example\n" + contract,
                        encoding="utf-8",
                    )

                    issues = validate_feature_record(
                        stage_owned_status,
                        "specs/example.md",
                        root=root,
                    )

                    self.assertEqual(
                        issues[0].code,
                        "BFR-UNKNOWN-LIFECYCLE-CONTRACT"
                        if case != "mixed duplicate"
                        else "BFR-MARKER-AUTHORITY",
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
    def test_active_inventory_retires_test_spec_consumers_without_rewriting_history(self) -> None:
        activation = json.loads(
            (ROOT / "specs" / "boundary-first-activation.yaml").read_text(
                encoding="utf-8"
            )
        )
        manifest = load_resource_manifest(ROOT)

        self.assertNotIn("test-spec", GOVERNED_SKILLS)
        self.assertNotIn("test-spec", activation["governed_skills"])
        self.assertTrue(
            all(
                "test-spec" not in resource.consumers
                for resource in manifest.resources
            )
        )
        self.assertIn(
            "specs/test-spec-review-gate.md",
            activation["grandfathered_specs"],
        )

    def test_repository_and_no_history_active_snapshots_are_independent(self) -> None:
        self.assertEqual(validate_activation(ROOT), ())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_checked_revision_active_fixture(root)
            with mock.patch(
                "boundary_first_validation.subprocess.run",
                side_effect=AssertionError("current-file validation must not invoke Git"),
            ), mock.patch(
                "boundary_first_validation.derive_grandfathered_specs",
                side_effect=AssertionError("normal validation must not derive inventory"),
            ):
                self.assertEqual(validate_activation(root), ())

    def test_checked_revision_snapshot_tuples_fail_closed(self) -> None:
        pending_source = json.loads(
            (ROOT / "specs" / "boundary-first-activation.yaml").read_text(
                encoding="utf-8"
            )
        )
        pending_source.update(
            {
                "state": "pending",
                "activating_release": "-",
                "rollback_release": "-",
                "grandfathering_baseline_revision": "-",
                "grandfathered_specs": [],
            }
        )
        pending_cases = {
            "release": ("activating_release", "v0.4.0"),
            "rollback": ("rollback_release", "v0.3.6"),
            "baseline": ("grandfathering_baseline_revision", "a" * 40),
            "inventory": ("grandfathered_specs", ["specs/historical.md"]),
        }
        for name, (field, value) in pending_cases.items():
            with self.subTest(state="pending", case=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                copy_activation_surfaces(root)
                data = dict(pending_source)
                data[field] = value
                (root / "specs/boundary-first-activation.yaml").write_text(
                    json.dumps(data), encoding="utf-8"
                )
                self.assertTrue(validate_activation(root))

        active_cases = {
            "release": ("activating_release", "v0.4.1"),
            "rollback": ("rollback_release", "v0.3.5"),
            "baseline": ("grandfathering_baseline_revision", "short"),
        }
        for name, (field, value) in active_cases.items():
            with self.subTest(state="active", case=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                activation_path = initialize_checked_revision_active_fixture(root)
                data = json.loads(activation_path.read_text(encoding="utf-8"))
                data[field] = value
                activation_path.write_text(json.dumps(data), encoding="utf-8")
                self.assertTrue(validate_activation(root))

    def test_grandfathered_derivation_is_explicit_sorted_and_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "fixture@example.test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
            for name in ("zeta", "é", "alpha"):
                (root / "specs" / f"{name}.md").write_text(
                    f"# {name}\n\n## Status\n\naccepted\n", encoding="utf-8"
                )
            (root / "specs" / "draft.md").write_text(
                "# Draft\n\n## Status\n\ndraft\n", encoding="utf-8"
            )
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=root, check=True)
            baseline = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True,
                capture_output=True, text=True,
            ).stdout.strip()
            before = relevant_tree_snapshot(root)

            inventory, issues = derive_grandfathered_specs(root, baseline)

            self.assertEqual(issues, ())
            self.assertEqual(
                inventory,
                tuple(sorted(("specs/alpha.md", "specs/zeta.md", "specs/é.md"), key=lambda value: value.encode("utf-8"))),
            )
            self.assertEqual(before, relevant_tree_snapshot(root))
            self.assertTrue(derive_grandfathered_specs(root, "short")[1])
            self.assertTrue(derive_grandfathered_specs(root, "f" * 40)[1])
            tree_revision = subprocess.run(
                ["git", "rev-parse", "HEAD^{tree}"], cwd=root, check=True,
                capture_output=True, text=True,
            ).stdout.strip()
            tree_inventory, tree_issues = derive_grandfathered_specs(root, tree_revision)
            self.assertEqual(tree_inventory, ())
            self.assertEqual(tree_issues[0].code, "BFR-BASELINE-TYPE")
            self.assertEqual(before, relevant_tree_snapshot(root))

    def test_grandfathered_derivation_ignores_replacement_refs_and_disables_lazy_fetch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "fixture@example.test"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
            (root / "specs/alpha.md").write_text(
                "# Alpha\n\n## Status\n\naccepted\n", encoding="utf-8"
            )
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "alpha"], cwd=root, check=True)
            baseline = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True,
                capture_output=True, text=True,
            ).stdout.strip()
            (root / "specs/alpha.md").unlink()
            (root / "specs/beta.md").write_text(
                "# Beta\n\n## Status\n\naccepted\n", encoding="utf-8"
            )
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "beta"], cwd=root, check=True)
            replacement = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True,
                capture_output=True, text=True,
            ).stdout.strip()
            subprocess.run(["git", "replace", baseline, replacement], cwd=root, check=True)

            real_run = subprocess.run
            calls: list[dict[str, object]] = []

            def recording_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[object]:
                calls.append(kwargs)
                return real_run(*args, **kwargs)

            with mock.patch("boundary_first_validation.subprocess.run", side_effect=recording_run):
                inventory, issues = derive_grandfathered_specs(root, baseline)

            self.assertEqual(issues, ())
            self.assertEqual(inventory, ("specs/alpha.md",))
            self.assertTrue(calls)
            for kwargs in calls:
                environment = kwargs.get("env")
                self.assertIsInstance(environment, dict)
                assert isinstance(environment, dict)
                self.assertEqual(environment.get("GIT_NO_REPLACE_OBJECTS"), "1")
                self.assertEqual(environment.get("GIT_NO_LAZY_FETCH"), "1")

    def test_grandfathered_derivation_rejects_ambient_git_authority_and_trace_output(self) -> None:
        baseline = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            empty_root = outer / "empty-root"
            empty_root.mkdir()
            trace_path = outer / "private-git-trace.log"
            trace2_path = outer / "private-git-trace2.log"
            poisoned = {
                "GIT_DIR": str(ROOT / ".git"),
                "GIT_WORK_TREE": str(ROOT),
                "GIT_OBJECT_DIRECTORY": str(ROOT / ".git/objects"),
                "GIT_ALTERNATE_OBJECT_DIRECTORIES": str(ROOT / ".git/objects"),
                "GIT_NAMESPACE": "private-namespace",
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.repositoryformatversion",
                "GIT_CONFIG_VALUE_0": "0",
                "GIT_TRACE": str(trace_path),
                "GIT_TRACE2": str(trace2_path),
            }
            with mock.patch.dict(os.environ, poisoned, clear=False):
                inventory, issues = derive_grandfathered_specs(empty_root, baseline)

            self.assertEqual(inventory, ())
            self.assertEqual(issues[0].code, "BFR-BASELINE-UNAVAILABLE")
            self.assertFalse(trace_path.exists())
            self.assertFalse(trace2_path.exists())

    def test_custom_activation_experiment_is_absent_and_cli_rejects_candidate_mode(self) -> None:
        for relative in (
            "scripts/boundary_activation_release.py",
            "scripts/publish-boundary-activation.py",
            "scripts/test-boundary-activation-release.py",
        ):
            self.assertFalse((ROOT / relative).exists(), relative)

        validator_source = (ROOT / "scripts/boundary_first_validation.py").read_text(encoding="utf-8")
        cli_source = (ROOT / "scripts/validate-boundary-first.py").read_text(encoding="utf-8")
        for retired_name in (
            "ActivationCandidateResult",
            "validate_activation_candidate",
            "publication_readiness",
        ):
            self.assertNotIn(retired_name, validator_source)
        self.assertNotIn("--activation-candidate", cli_source)
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate-boundary-first.py"),
                "--activation-candidate",
                "v0.4.0",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("unrecognized arguments", completed.stderr)

    def test_active_cli_reports_snapshot_and_release_intent_without_public_claim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_checked_revision_active_fixture(root)
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate-boundary-first.py"), "--check", "--root", str(root)],
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            output = json.loads(completed.stdout)
            self.assertEqual(output["snapshot"], "active")
            self.assertEqual(output["release_intent"], "v0.4.0")
            self.assertNotIn("published", completed.stdout.lower())
            self.assertNotIn("tagged", completed.stdout.lower())

    def test_repository_active_activation_record_passes(self) -> None:
        self.assertEqual(validate_activation(ROOT), ())

    def test_unknown_activation_state_fails_before_consistency(self) -> None:
        fixture = json.loads(
            (FIXTURES / "activation" / "unknown-state.yaml").read_text(
                encoding="utf-8"
            )
        )
        for state in (fixture["state"], [], {}):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                (root / "specs").mkdir()
                source = ROOT / "specs" / "boundary-first-activation.yaml"
                data = json.loads(source.read_text(encoding="utf-8"))
                data["state"] = state
                (root / "specs" / "boundary-first-activation.yaml").write_text(
                    json.dumps(data), encoding="utf-8"
                )
                issues = validate_activation(root)
                self.assertEqual(issues[0].code, "BFR-UNKNOWN-ACTIVATION-STATE")
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts/validate-boundary-first.py"),
                        "--check",
                        "--root",
                        str(root),
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(completed.returncode, 1)
                self.assertEqual(
                    json.loads(completed.stdout)["issues"][0]["check_id"],
                    "BFR-UNKNOWN-ACTIVATION-STATE",
                )

    def test_activation_cli_suppresses_private_root_for_missing_and_malformed_records(self) -> None:
        sentinel = "credential-token-otp-user-host-private"
        with tempfile.TemporaryDirectory(prefix=f"{sentinel}-") as temporary:
            root = Path(temporary)
            (root / "specs").mkdir()
            activation_path = root / "specs/boundary-first-activation.yaml"
            for case, contents in (
                ("missing", None),
                ("malformed", "{"),
                ("wrong-shape", "[]"),
            ):
                with self.subTest(case=case):
                    if contents is None:
                        activation_path.unlink(missing_ok=True)
                    else:
                        activation_path.write_text(contents, encoding="utf-8")
                    completed = subprocess.run(
                        [
                            sys.executable,
                            str(ROOT / "scripts/validate-boundary-first.py"),
                            "--check",
                            "--root",
                            str(root),
                        ],
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(completed.returncode, 1)
                    payload = json.loads(completed.stdout)
                    self.assertEqual(
                        payload["issues"][0]["path"],
                        "specs/boundary-first-activation.yaml",
                    )
                    self.assertNotIn(sentinel, completed.stdout)
                    self.assertNotIn(str(root), completed.stdout)

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

    def test_activation_preserves_missing_manifest_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_activation_surfaces(root)
            (root / "specs/boundary-first-resources.yaml").unlink()

            issue = validate_activation(root)[0]

            self.assertEqual(issue.code, "BFR-MANIFEST-MISSING")
            self.assertEqual(
                issue.path,
                "specs/boundary-first-resources.yaml",
            )
            self.assertEqual(issue.expected, "existing resource manifest")

    def test_activation_does_not_disclose_untrusted_manifest_scalar(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_activation_surfaces(root)
            secret = "token-super-secret-marker"
            manifest = root / "specs/boundary-first-resources.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "      - verify\n",
                    f"      - {secret}\n",
                    1,
                ),
                encoding="utf-8",
            )

            issue = validate_activation(root)[0]
            serialized = json.dumps(issue.as_dict())

            self.assertEqual(
                issue.code,
                "BFR-MANIFEST-CONSUMER-UNKNOWN",
            )
            self.assertTrue(issue.offending_value.startswith("sha256:"))
            self.assertNotIn(secret, serialized)

    def test_activation_does_not_disclose_resource_version_scalar(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_activation_surfaces(root)
            secret = "token-super-secret-resource-version"
            resource = (
                root
                / "specs/references/"
                "boundary-first-feature-authoring-v1.md"
            )
            resource.write_text(
                f"# Feature\n\nBoundary model version: {secret}\n",
                encoding="utf-8",
            )

            issue = validate_activation(root)[0]
            serialized = json.dumps(issue.as_dict())

            self.assertEqual(issue.code, "BFR-RESOURCE-VERSION-UNKNOWN")
            self.assertTrue(issue.offending_value.startswith("sha256:"))
            self.assertNotIn(secret, serialized)

    def test_activation_preserves_missing_family_source_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_activation_surfaces(root)
            missing = (
                root / "specs/references/boundary-first-proof-v1.md"
            )
            missing.unlink()

            issue = validate_activation(root)[0]

            self.assertEqual(issue.code, "BFR-SOURCE-MISSING")
            self.assertEqual(
                issue.path,
                "specs/references/boundary-first-proof-v1.md",
            )
            self.assertIn("existing canonical resource", issue.expected)

    def test_activation_preserves_family_source_symlink_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copy_activation_surfaces(root)
            source = (
                root
                / "specs/references/"
                "boundary-first-feature-authoring-v1.md"
            )
            source.unlink()
            source.symlink_to(
                root / "specs/references/boundary-first-method-v1.md"
            )

            issue = validate_activation(root)[0]

            self.assertEqual(issue.code, "BFR-PATH-SYMLINK")
            self.assertEqual(
                issue.path,
                "specs/references/"
                "boundary-first-feature-authoring-v1.md",
            )
            self.assertIn("non-symlink", issue.expected)

    def test_active_rollback_release_matches_current_adapter_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            initialize_checked_revision_active_fixture(root)
            before = relevant_tree_snapshot(root)

            selection, issues = rollback_package_selection(root)

            self.assertEqual(issues, ())
            self.assertIsNotNone(selection)
            assert selection is not None
            self.assertEqual(selection.release, "v0.3.6")
            self.assertEqual(
                tuple(row.adapter for row in selection.artifacts),
                ("claude", "codex", "opencode"),
            )
            self.assertEqual(
                tuple(row.archive for row in selection.artifacts),
                tuple(
                    f"rigorloop-adapter-{adapter}-v0.3.6.zip"
                    for adapter in ("claude", "codex", "opencode")
                ),
            )
            tracked_path = (
                ROOT
                / "docs/reports/adapter-artifacts/releases/v0.3.6.yaml"
            )
            tracked = parse_adapter_artifact_metadata_yaml(
                tracked_path.read_text(encoding="utf-8"), tracked_path
            )
            expected_hashes = {
                artifact.adapter: artifact.sha256 for artifact in tracked.artifacts
            }
            self.assertEqual(
                {row.adapter: row.sha256 for row in selection.artifacts},
                expected_hashes,
            )
            self.assertEqual(before, relevant_tree_snapshot(root))

    def test_rollback_metadata_rejects_incomplete_or_mixed_matrices_without_mutation(self) -> None:
        source_metadata = (
            ROOT
            / "docs"
            / "reports"
            / "adapter-artifacts"
            / "releases"
            / "v0.3.6.yaml"
        )
        original = source_metadata.read_text(encoding="utf-8")
        substituted = (
            ROOT
            / "docs"
            / "reports"
            / "adapter-artifacts"
            / "releases"
            / "v0.3.5.yaml"
        ).read_text(encoding="utf-8").replace("v0.3.5", "v0.3.6")
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
                "    archive: rigorloop-adapter-extra-v0.3.6.zip\n"
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
                "  version: v0.3.6",
                "  version: v0.3.4",
                1,
            ),
            "substituted-artifacts": substituted,
        }
        for name, metadata_text in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                initialize_checked_revision_active_fixture(root)
                metadata = (
                    root
                    / "docs"
                    / "reports"
                    / "adapter-artifacts"
                    / "releases"
                    / "v0.3.6.yaml"
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
            Path("docs/reports/adapter-artifacts/releases/v0.3.6.yaml"),
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
                    initialize_checked_revision_active_fixture(root)
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
            initialize_checked_revision_active_fixture(root)
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
            self.assertEqual(output["rollback_release"], "v0.3.6")
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
                / "v0.3.6.yaml"
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

    def test_grandfathered_inventory_requires_raw_utf8_order_and_uniqueness(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            activation_path = initialize_checked_revision_active_fixture(root)
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

    def test_changed_bootstrap_proof_model_is_exempt_from_adoption_marker(self) -> None:
        self.assertEqual(
            validate_changed_spec(ROOT, "specs/boundary-first-proof-model.md"),
            (),
        )

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
            data = json.loads(
                (ROOT / "specs" / "boundary-first-activation.yaml").read_text(
                    encoding="utf-8"
                )
            )
            data.update(
                {
                    "state": "pending",
                    "activating_release": "-",
                    "rollback_release": "-",
                    "grandfathering_baseline_revision": "-",
                    "grandfathered_specs": [],
                }
            )
            (root / "specs" / "boundary-first-activation.yaml").write_text(
                json.dumps(data), encoding="utf-8"
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
