#!/usr/bin/env python3
"""Regression tests for the boundary-first shared-reference projection."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from boundary_first_reference import (  # noqa: E402
    CANONICAL_REFERENCE,
    GOVERNED_SKILLS,
    METHOD_VERSION,
    PROJECTED_REFERENCE,
    RESOURCE_MANIFEST,
    ProjectionContractError,
    inventory_digest,
    load_resource_manifest,
    project_reference,
    projected_paths,
)

MANIFEST_BYTES = b"""schema_version: 1
contract_version: boundary-first-v1
resources:
  - id: compact-core
    source: specs/references/boundary-first-method-v1.md
    target: references/boundary-first-method-v1.md
    consumers:
      - workflow
      - spec
      - design-review
      - plan
      - test-spec
      - delivery-review
      - implement
      - code-review
      - verify
  - id: feature-authoring
    source: specs/references/boundary-first-feature-authoring-v1.md
    target: references/boundary-first-feature-authoring-v1.md
    consumers:
      - spec
      - design-review
  - id: proof
    source: specs/references/boundary-first-proof-v1.md
    target: references/boundary-first-proof-v1.md
    consumers:
      - test-spec
      - delivery-review
"""


class BoundaryFirstReferenceTests(unittest.TestCase):
    def make_repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = root / CANONICAL_REFERENCE
        source.parent.mkdir(parents=True)
        source.write_bytes(
            b"# portable boundary method\n\n"
            b"Boundary model version: boundary-first-v1\n"
        )
        (root / "specs" / "boundary-first-resources.yaml").write_bytes(
            MANIFEST_BYTES
        )
        (source.parent / "boundary-first-feature-authoring-v1.md").write_bytes(
            b"# feature authoring\n\n"
            b"Boundary model version: boundary-first-v1\n"
        )
        (source.parent / "boundary-first-proof-v1.md").write_bytes(
            b"# proof guidance\n\n"
            b"Boundary model version: boundary-first-v1\n"
        )
        for skill in GOVERNED_SKILLS:
            (root / "skills" / skill).mkdir(parents=True)
        return temporary, root

    def make_outside_directory(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def test_closed_version_source_and_consumers(self) -> None:
        self.assertEqual(METHOD_VERSION, "boundary-first-v1")
        self.assertEqual(
            CANONICAL_REFERENCE,
            Path("specs/references/boundary-first-method-v1.md"),
        )
        self.assertEqual(
            GOVERNED_SKILLS,
            (
                "workflow",
                "spec",
                "design-review",
                "plan",
                "test-spec",
                "delivery-review",
                "implement",
                "code-review",
                "verify",
            ),
        )
        self.assertEqual(
            PROJECTED_REFERENCE,
            Path("references/boundary-first-method-v1.md"),
        )
        self.assertEqual(
            RESOURCE_MANIFEST,
            Path("specs/boundary-first-resources.yaml"),
        )

    def test_manifest_is_the_exact_closed_resource_authority(self) -> None:
        _, root = self.make_repository()

        manifest = load_resource_manifest(root)

        self.assertEqual(manifest.schema_version, 1)
        self.assertEqual(manifest.contract_version, METHOD_VERSION)
        self.assertEqual(
            tuple(resource.resource_id for resource in manifest.resources),
            ("compact-core", "feature-authoring", "proof"),
        )
        self.assertEqual(
            projected_paths(root),
            (
                *(
                    Path("skills")
                    / skill
                    / "references/boundary-first-method-v1.md"
                    for skill in GOVERNED_SKILLS
                ),
                Path(
                    "skills/spec/references/"
                    "boundary-first-feature-authoring-v1.md"
                ),
                Path(
                    "skills/design-review/references/"
                    "boundary-first-feature-authoring-v1.md"
                ),
                Path(
                    "skills/test-spec/references/"
                    "boundary-first-proof-v1.md"
                ),
                Path(
                    "skills/delivery-review/references/"
                    "boundary-first-proof-v1.md"
                ),
            ),
        )

    def test_unknown_value_fails_before_consistency_checks(self) -> None:
        _, root = self.make_repository()
        manifest = root / RESOURCE_MANIFEST
        manifest.write_bytes(
            MANIFEST_BYTES.replace(
                b"contract_version: boundary-first-v1",
                b"contract_version: boundary-first-v2",
            ).replace(
                b"      - workflow\n",
                b"      - future-stage\n",
                1,
            )
        )

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-MANIFEST-CONTRACT-VERSION-UNKNOWN",
        ):
            project_reference(root, mode="write")

    def test_manifest_rejects_unknown_missing_and_duplicate_fields(self) -> None:
        variants = {
            "unknown": MANIFEST_BYTES.replace(
                b"schema_version: 1\n",
                b"schema_version: 1\nfuture: true\n",
            ),
            "missing": MANIFEST_BYTES.replace(
                b"contract_version: boundary-first-v1\n",
                b"",
            ),
            "duplicate": MANIFEST_BYTES.replace(
                b"schema_version: 1\n",
                b"schema_version: 1\nschema_version: 1\n",
            ),
        }
        for name, raw in variants.items():
            with self.subTest(name=name):
                _, root = self.make_repository()
                (root / RESOURCE_MANIFEST).write_bytes(raw)
                with self.assertRaisesRegex(
                    ProjectionContractError,
                    "BFR-MANIFEST-(FIELDS|DUPLICATE-KEY)",
                ):
                    project_reference(root, mode="write")

    def test_manifest_rejects_unknown_ids_consumers_and_duplicates(self) -> None:
        variants = {
            "unknown-id": MANIFEST_BYTES.replace(
                b"id: proof", b"id: future"
            ),
            "unknown-consumer": MANIFEST_BYTES.replace(
                b"      - verify\n", b"      - future-stage\n"
            ),
            "duplicate-consumer": MANIFEST_BYTES.replace(
                b"      - verify\n", b"      - verify\n      - verify\n"
            ),
            "duplicate-source": MANIFEST_BYTES.replace(
                b"specs/references/boundary-first-proof-v1.md",
                b"specs/references/boundary-first-feature-authoring-v1.md",
                1,
            ),
            "duplicate-target": MANIFEST_BYTES.replace(
                b"references/boundary-first-proof-v1.md",
                b"references/boundary-first-feature-authoring-v1.md",
                1,
            ),
        }
        for name, raw in variants.items():
            with self.subTest(name=name):
                _, root = self.make_repository()
                (root / RESOURCE_MANIFEST).write_bytes(raw)
                with self.assertRaisesRegex(
                    ProjectionContractError,
                    "BFR-MANIFEST-",
                ):
                    project_reference(root, mode="write")

    def test_manifest_rejects_known_but_wrong_exact_resource_tuples(
        self,
    ) -> None:
        variants = {
            "missing-compact-consumer": (
                MANIFEST_BYTES.replace(b"      - verify\n", b"", 1),
                "compact-core",
            ),
            "unowned-feature-consumer": (
                MANIFEST_BYTES.replace(
                    b"      - design-review\n  - id: proof",
                    b"      - design-review\n      - plan\n  - id: proof",
                ),
                "feature-authoring",
            ),
            "wrong-source": (
                MANIFEST_BYTES.replace(
                    b"specs/references/boundary-first-proof-v1.md",
                    b"specs/references/alternate-proof-v1.md",
                ),
                "proof",
            ),
            "wrong-target": (
                MANIFEST_BYTES.replace(
                    b"    target: references/boundary-first-proof-v1.md",
                    b"    target: references/alternate-proof-v1.md",
                ),
                "proof",
            ),
        }
        for name, (raw, expected_layer) in variants.items():
            with self.subTest(name=name):
                _, root = self.make_repository()
                if name == "wrong-source":
                    (
                        root / "specs/references/alternate-proof-v1.md"
                    ).write_bytes(b"# alternate\n")
                (root / RESOURCE_MANIFEST).write_bytes(raw)
                with self.assertRaisesRegex(
                    ProjectionContractError,
                    "BFR-MANIFEST-IDENTITY",
                ) as raised:
                    project_reference(root, mode="write")
                self.assertIn(expected_layer, raised.exception.message)

    def test_projection_module_does_not_restate_the_resource_matrix(self) -> None:
        module = (
            ROOT / "scripts" / "boundary_first_reference.py"
        ).read_text(encoding="utf-8")

        self.assertNotIn("RESOURCE_CONTRACTS", module)

    def test_mixed_canonical_resource_version_fails_before_write(self) -> None:
        _, root = self.make_repository()
        proof = root / "specs/references/boundary-first-proof-v1.md"
        proof.write_text(
            "# Proof\n\nBoundary model version: boundary-first-v2\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-RESOURCE-VERSION-UNKNOWN",
        ):
            project_reference(root, mode="write")

    def test_manifest_rejects_unsafe_paths_before_mutation(self) -> None:
        variants = {
            "absolute": b"/tmp/boundary.md",
            "dot": b"specs/./references/boundary.md",
            "escape": b"../boundary.md",
            "outside-target": b"assets/boundary-first-method-v1.md",
        }
        for name, replacement in variants.items():
            with self.subTest(name=name):
                _, root = self.make_repository()
                raw = MANIFEST_BYTES
                needle = b"specs/references/boundary-first-method-v1.md"
                if name == "outside-target":
                    needle = b"references/boundary-first-method-v1.md"
                (root / RESOURCE_MANIFEST).write_bytes(
                    raw.replace(needle, replacement, 1)
                )
                sentinel = root / "skills/spec/references/sentinel"
                sentinel.parent.mkdir(parents=True)
                sentinel.write_bytes(b"unchanged")
                with self.assertRaisesRegex(
                    ProjectionContractError,
                    "BFR-MANIFEST-PATH",
                ):
                    project_reference(root, mode="write")
                self.assertEqual(sentinel.read_bytes(), b"unchanged")

    def test_write_is_raw_byte_exact_and_idempotent(self) -> None:
        _, root = self.make_repository()
        source = root / CANONICAL_REFERENCE
        raw = b"# method\r\n\xce\xbb portable bytes\n"
        raw += b"Boundary model version: boundary-first-v1\n"
        source.write_bytes(raw)

        first = project_reference(root, mode="write")
        second = project_reference(root, mode="write")

        self.assertTrue(first.ok)
        self.assertTrue(second.ok)
        self.assertEqual(first.projection_sha256, second.projection_sha256)
        for relative in projected_paths(root):
            target = root / relative
            expected_name = target.name
            if expected_name == PROJECTED_REFERENCE.name:
                expected = raw
            elif expected_name == "boundary-first-feature-authoring-v1.md":
                expected = (
                    b"# feature authoring\n\n"
                    b"Boundary model version: boundary-first-v1\n"
                )
            else:
                expected = (
                    b"# proof guidance\n\n"
                    b"Boundary model version: boundary-first-v1\n"
                )
            self.assertEqual(target.read_bytes(), expected)

    def test_check_reports_missing_stale_and_unexpected_projections(self) -> None:
        _, root = self.make_repository()
        project_reference(root, mode="write")
        missing = root / "skills" / "workflow" / PROJECTED_REFERENCE
        missing.unlink()
        stale = root / "skills" / "spec" / PROJECTED_REFERENCE
        stale.write_bytes(b"stale")
        unexpected = (
            root
            / "skills"
            / "proposal"
            / "references"
            / "boundary-first-method-v1.md"
        )
        unexpected.parent.mkdir(parents=True)
        unexpected.write_bytes((root / CANONICAL_REFERENCE).read_bytes())

        result = project_reference(root, mode="check")

        self.assertFalse(result.ok)
        self.assertEqual(
            result.errors,
            (
                "BFR-PROJECTION-MISSING: skills/workflow/references/"
                "boundary-first-method-v1.md",
                "BFR-PROJECTION-STALE: skills/spec/references/"
                "boundary-first-method-v1.md",
                "BFR-PROJECTION-UNEXPECTED: skills/proposal/references/"
                "boundary-first-method-v1.md",
            ),
        )

    def test_check_rejects_alternate_version_and_nested_resources(
        self,
    ) -> None:
        _, root = self.make_repository()
        project_reference(root, mode="write")
        extras = (
            root
            / "skills/workflow/references/boundary-first-method-v2.md",
            root
            / "skills/spec/references/nested/boundary-first-extra.md",
            root
            / "specs/references/boundary-first-proof-v2.md",
        )
        for extra in extras:
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text("# unexpected\n", encoding="utf-8")

        result = project_reference(root, mode="check")

        self.assertFalse(result.ok)
        for extra in extras:
            self.assertIn(
                "BFR-PROJECTION-UNEXPECTED: "
                + extra.relative_to(root).as_posix(),
                result.errors,
            )

    def test_check_rejects_symlink_projection(self) -> None:
        _, root = self.make_repository()
        project_reference(root, mode="write")
        target = root / "skills" / "workflow" / PROJECTED_REFERENCE
        target.unlink()
        target.symlink_to(root / CANONICAL_REFERENCE)

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-PATH-SYMLINK: skills/workflow/references/"
            "boundary-first-method-v1.md",
        ):
            project_reference(root, mode="check")

    def test_parent_symlink_escape_fails_without_outside_mutation(self) -> None:
        _, root = self.make_repository()
        outside = self.make_outside_directory()
        sentinel = outside / PROJECTED_REFERENCE.name
        sentinel.write_bytes(b"outside sentinel")
        references = root / "skills" / "workflow" / "references"
        references.symlink_to(outside, target_is_directory=True)

        for mode in ("check", "write"):
            with self.subTest(mode=mode):
                with self.assertRaisesRegex(
                    ProjectionContractError,
                    "BFR-PATH-SYMLINK: skills/workflow/references",
                ):
                    project_reference(root, mode=mode)
                self.assertEqual(sentinel.read_bytes(), b"outside sentinel")

    def test_invalid_late_source_preflight_performs_no_partial_write(self) -> None:
        _, root = self.make_repository()
        existing = root / "skills/workflow" / PROJECTED_REFERENCE
        existing.parent.mkdir(parents=True)
        existing.write_bytes(b"original")
        (
            root
            / "specs/references/boundary-first-proof-v1.md"
        ).unlink()

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-SOURCE-MISSING.*boundary-first-proof-v1.md",
        ):
            project_reference(root, mode="write")

        self.assertEqual(existing.read_bytes(), b"original")

    def test_write_failure_restores_every_prior_target_and_retry_succeeds(
        self,
    ) -> None:
        _, root = self.make_repository()
        project_reference(root, mode="write")
        before = {
            relative: (root / relative).read_bytes()
            for relative in projected_paths(root)
        }
        (root / CANONICAL_REFERENCE).write_bytes(
            b"# revised compact\n\n"
            b"Boundary model version: boundary-first-v1\n"
        )

        from boundary_first_reference import _write_target_bytes

        for failure_index in (1, 7, 13):
            calls = 0
            failed = False

            def fail_once(
                write_root: Path, path: Path, data: bytes
            ) -> None:
                nonlocal calls, failed
                calls += 1
                if calls == failure_index and not failed:
                    failed = True
                    raise OSError("injected write interruption")
                _write_target_bytes(write_root, path, data)

            with self.subTest(failure_index=failure_index):
                with patch(
                    "boundary_first_reference._write_target_bytes",
                    side_effect=fail_once,
                ):
                    with self.assertRaisesRegex(
                        ProjectionContractError,
                        "BFR-PROJECTION-WRITE",
                    ):
                        project_reference(root, mode="write")
                self.assertEqual(
                    {
                        relative: (root / relative).read_bytes()
                        for relative in projected_paths(root)
                    },
                    before,
                )

        retry = project_reference(root, mode="write")
        self.assertTrue(retry.ok)

    def test_keyboard_interrupt_restores_prior_targets_before_reraise(
        self,
    ) -> None:
        from boundary_first_reference import _write_target_bytes

        for preexisting in (False, True):
            with self.subTest(preexisting=preexisting):
                _, root = self.make_repository()
                paths = projected_paths(root)
                if preexisting:
                    project_reference(root, mode="write")
                    before = {
                        relative: (root / relative).read_bytes()
                        for relative in paths
                    }
                    (root / CANONICAL_REFERENCE).write_bytes(
                        b"# revised compact\n\n"
                        b"Boundary model version: boundary-first-v1\n"
                    )
                else:
                    before = {relative: None for relative in paths}

                calls = 0

                def interrupt(
                    write_root: Path, path: Path, data: bytes
                ) -> None:
                    nonlocal calls
                    calls += 1
                    if calls == 7:
                        raise KeyboardInterrupt
                    _write_target_bytes(write_root, path, data)

                with patch(
                    "boundary_first_reference._write_target_bytes",
                    side_effect=interrupt,
                ):
                    with self.assertRaises(KeyboardInterrupt):
                        project_reference(root, mode="write")

                after = {
                    relative: (
                        (root / relative).read_bytes()
                        if (root / relative).is_file()
                        else None
                    )
                    for relative in paths
                }
                self.assertEqual(after, before)
                self.assertTrue(project_reference(root, mode="write").ok)

    def test_input_drift_restores_targets_and_retry_succeeds(self) -> None:
        from boundary_first_reference import _write_target_bytes

        inputs = (
            RESOURCE_MANIFEST,
            CANONICAL_REFERENCE,
            Path(
                "specs/references/"
                "boundary-first-feature-authoring-v1.md"
            ),
            Path("specs/references/boundary-first-proof-v1.md"),
        )
        for relative_input in inputs:
            for mutation_index in (1, 7, 13):
                with self.subTest(
                    input=relative_input,
                    mutation_index=mutation_index,
                ):
                    _, root = self.make_repository()
                    project_reference(root, mode="write")
                    paths = projected_paths(root)
                    before_targets = {
                        path: (root / path).read_bytes()
                        for path in paths
                    }
                    input_path = root / relative_input
                    before_input = input_path.read_bytes()
                    calls = 0

                    def mutate_input(
                        write_root: Path, path: Path, data: bytes
                    ) -> None:
                        nonlocal calls
                        calls += 1
                        _write_target_bytes(write_root, path, data)
                        if calls == mutation_index:
                            input_path.write_bytes(
                                before_input + b"\n# concurrent mutation\n"
                            )

                    with patch(
                        "boundary_first_reference._write_target_bytes",
                        side_effect=mutate_input,
                    ):
                        with self.assertRaisesRegex(
                            ProjectionContractError,
                            "BFR-INPUT-CHANGED",
                        ):
                            project_reference(root, mode="write")

                    self.assertEqual(
                        {
                            path: (root / path).read_bytes()
                            for path in paths
                        },
                        before_targets,
                    )
                    input_path.write_bytes(before_input)
                    self.assertTrue(project_reference(root, mode="write").ok)

    def test_target_parent_swap_never_writes_outside_and_recovery_continues(
        self,
    ) -> None:
        from boundary_first_reference import _write_target_bytes

        _, root = self.make_repository()
        project_reference(root, mode="write")
        paths = projected_paths(root)
        before = {
            path: (root / path).read_bytes()
            for path in paths
        }
        (root / CANONICAL_REFERENCE).write_bytes(
            b"# revised compact\n\n"
            b"Boundary model version: boundary-first-v1\n"
        )
        outside = self.make_outside_directory()
        references = root / "skills/workflow/references"
        displaced = root / "skills/workflow/references-displaced"
        calls = 0

        def swap_then_fail(
            write_root: Path, relative: Path, data: bytes
        ) -> None:
            nonlocal calls
            calls += 1
            if calls == 7:
                references.rename(displaced)
                references.symlink_to(outside, target_is_directory=True)
                raise OSError("injected topology drift")
            _write_target_bytes(write_root, relative, data)

        with patch(
            "boundary_first_reference._write_target_bytes",
            side_effect=swap_then_fail,
        ):
            with self.assertRaisesRegex(
                ProjectionContractError,
                "BFR-PROJECTION-RESTORE",
            ):
                project_reference(root, mode="write")

        self.assertFalse(
            (outside / "boundary-first-method-v1.md").exists()
        )
        for relative in paths:
            if relative.parts[:3] == (
                "skills",
                "workflow",
                "references",
            ):
                continue
            self.assertEqual((root / relative).read_bytes(), before[relative])

    def test_missing_manifest_cli_diagnostic_preserves_identity(self) -> None:
        _, root = self.make_repository()
        (root / RESOURCE_MANIFEST).unlink()

        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/project-boundary-first-reference.py"),
                "--check",
                "--root",
                str(root),
            ],
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("BFR-MANIFEST-MISSING", completed.stdout)
        self.assertIn(
            "path=specs/boundary-first-resources.yaml",
            completed.stdout,
        )
        self.assertIn("expected=existing resource manifest", completed.stdout)
        self.assertNotIn(str(root), completed.stdout)

    def test_untrusted_manifest_scalar_is_not_disclosed_by_cli(self) -> None:
        _, root = self.make_repository()
        secret = "token-super-secret-marker"
        manifest = root / RESOURCE_MANIFEST
        manifest.write_text(
            manifest.read_text(encoding="utf-8").replace(
                "      - verify\n",
                f"      - {secret}\n",
                1,
            ),
            encoding="utf-8",
        )

        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/project-boundary-first-reference.py"),
                "--check",
                "--root",
                str(root),
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 2)
        self.assertIn("BFR-MANIFEST-CONSUMER-UNKNOWN", completed.stdout)
        self.assertIn("offending_value=sha256:", completed.stdout)
        self.assertNotIn(secret, completed.stdout)

    def test_source_parent_symlink_escape_fails_before_read(self) -> None:
        _, root = self.make_repository()
        source = root / CANONICAL_REFERENCE
        for resource in source.parent.iterdir():
            resource.unlink()
        source.parent.rmdir()
        outside = self.make_outside_directory()
        (outside / CANONICAL_REFERENCE.name).write_bytes(b"outside method")
        source.parent.symlink_to(outside, target_is_directory=True)

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-PATH-SYMLINK: specs/references",
        ):
            project_reference(root, mode="check")

    def test_unexpected_consumer_symlink_topologies_fail_closed(self) -> None:
        for topology in ("skill-root", "references"):
            for mode in ("check", "write"):
                with self.subTest(topology=topology, mode=mode):
                    _, root = self.make_repository()
                    project_reference(root, mode="write")
                    outside = self.make_outside_directory()
                    outside_bytes = b"outside sentinel"
                    if topology == "skill-root":
                        outside_reference = outside / PROJECTED_REFERENCE
                        outside_reference.parent.mkdir()
                        outside_reference.write_bytes(outside_bytes)
                        (root / "skills" / "proposal").symlink_to(
                            outside,
                            target_is_directory=True,
                        )
                        expected_path = "skills/proposal"
                    else:
                        outside_reference = outside / PROJECTED_REFERENCE.name
                        outside_reference.write_bytes(outside_bytes)
                        proposal = root / "skills" / "proposal"
                        proposal.mkdir()
                        (proposal / "references").symlink_to(
                            outside,
                            target_is_directory=True,
                        )
                        expected_path = "skills/proposal/references"

                    expected_errors = [
                        "BFR-UNEXPECTED-CONSUMER-SYMLINK: "
                        + expected_path
                    ]
                    if mode == "check":
                        (
                            root
                            / "skills"
                            / "workflow"
                            / PROJECTED_REFERENCE
                        ).unlink()
                        expected_errors.append(
                            "BFR-PROJECTION-MISSING: "
                            "skills/workflow/references/"
                            "boundary-first-method-v1.md"
                        )

                    result = project_reference(root, mode=mode)

                    self.assertFalse(result.ok)
                    self.assertEqual(
                        result.errors,
                        tuple(sorted(expected_errors)),
                    )
                    self.assertEqual(
                        outside_reference.read_bytes(),
                        outside_bytes,
                    )

    def test_unrelated_reference_symlinks_are_outside_projection_scope(
        self,
    ) -> None:
        _, root = self.make_repository()
        project_reference(root, mode="write")
        outside = self.make_outside_directory()
        target = outside / "other-guidance.md"
        target.write_text("# unrelated\n", encoding="utf-8")
        skill_link = (
            root / "skills/workflow/references/other-guidance.md"
        )
        skill_link.symlink_to(target)
        canonical_link = root / "specs/references/other-guidance.md"
        canonical_link.symlink_to(target)

        result = project_reference(root, mode="check")

        self.assertTrue(result.ok)

    def test_inventory_digest_uses_sorted_posix_path_and_raw_hash_records(
        self,
    ) -> None:
        records = {
            "skills/z/reference.md": hashlib.sha256(b"z").hexdigest(),
            "skills/a/reference.md": hashlib.sha256(b"a").hexdigest(),
        }
        serialized = b"".join(
            (
                f"{path}\0{records[path]}\n".encode("utf-8")
                for path in sorted(records)
            )
        )

        self.assertEqual(
            inventory_digest(records),
            hashlib.sha256(serialized).hexdigest(),
        )

    def test_unknown_mode_fails_before_projection_consistency(self) -> None:
        _, root = self.make_repository()

        with self.assertRaisesRegex(
            ProjectionContractError,
            "BFR-MODE-UNKNOWN: unknown projection mode 'future'",
        ):
            project_reference(root, mode="future")

    def test_projection_cli_preserves_structured_resource_diagnostic(
        self,
    ) -> None:
        _, root = self.make_repository()
        feature = (
            root
            / "specs/references/boundary-first-feature-authoring-v1.md"
        )
        secret = "token-super-secret-resource-version"
        feature.write_text(
            f"# Feature\n\nBoundary model version: {secret}\n",
            encoding="utf-8",
        )

        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/project-boundary-first-reference.py"),
                "--check",
                "--root",
                str(root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 2)
        self.assertIn("BFR-RESOURCE-VERSION-UNKNOWN", completed.stdout)
        self.assertIn(
            "path=specs/references/"
            "boundary-first-feature-authoring-v1.md",
            completed.stdout,
        )
        self.assertIn("offending_value=sha256:", completed.stdout)
        self.assertIn("expected=boundary-first-v1", completed.stdout)
        self.assertNotIn(secret, completed.stdout)
        self.assertNotIn(str(root), completed.stdout)

    def test_canonical_method_contains_portable_contract_without_stage_policy(
        self,
    ) -> None:
        text = (ROOT / CANONICAL_REFERENCE).read_text(encoding="utf-8")
        required = (
            "Boundary model version: boundary-first-v1",
            "## Core dimensions",
            "applicable",
            "not-applicable",
            "illustration",
            "regression",
            "discovery",
            "No interaction selected:",
            "Structural validation",
            "Semantic review",
            "Which inputs or actors can change the outcome?",
            "Which state or timing conditions can change the outcome?",
            "Which public, sibling, helper, or alternate path can change the outcome?",
            "Which failure, retry, recovery, compatibility, or external condition can change the outcome?",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, text)
        forbidden = (
            "Immediate next stage:",
            "Implementation handoff:",
            "Recording status:",
            "branch-ready",
            "PR readiness",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, text)

        feature = (
            ROOT
            / "specs/references/boundary-first-feature-authoring-v1.md"
        ).read_text(encoding="utf-8")
        proof = (
            ROOT / "specs/references/boundary-first-proof-v1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("## Feature-spec boundary record", feature)
        self.assertNotIn("## Test-spec proof record", feature)
        self.assertIn("## Test-spec proof record", proof)
        self.assertNotIn("## Feature-spec boundary record", proof)


if __name__ == "__main__":
    unittest.main()
