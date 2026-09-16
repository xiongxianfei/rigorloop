"""Independent generated trees, drift validation and safe output roots."""

from __future__ import annotations

import sys
from pathlib import Path
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging import adapter_distribution as adapter_distribution_module
from lib.packaging.adapter_distribution import ADAPTERS, adapter_archive_name, build_adapter_archives, collect_adapter_drift, collect_adapter_drift_entries, expected_adapter_files, format_adapter_drift_normal, format_adapter_drift_verbose, sync_adapter_output, validate_adapter_output
from adapter_fixture_helpers import (copy_fixture_skills, generate_fixture_adapters)


class AdapterGenerationTests(unittest.TestCase):
    maxDiff = None

    def test_distribution_generation_rejects_source_and_active_output_roots(self) -> None:
        for operation in ("archives", "tree"):
            for destination in ("skills", "skills/nested", ".codex/skills", ".agents/skills", ".claude/skills", ".opencode/skills", "alias"):
                with self.subTest(operation=operation, destination=destination), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    skills = copy_fixture_skills(root, ("portable-with-assets",))
                    if destination == "alias":
                        (root / "alias").symlink_to(skills, target_is_directory=True)
                    before = {path.relative_to(skills): path.read_bytes() for path in skills.rglob("*") if path.is_file()}
                    with self.assertRaisesRegex(ValueError, "unsafe output"):
                        if operation == "archives":
                            build_adapter_archives("v1.0.0", root / destination, skills_root=skills)
                        else:
                            sync_adapter_output("v1.0.0", skills_root=skills, output_root=root / destination)
                    self.assertEqual(before, {path.relative_to(skills): path.read_bytes() for path in skills.rglob("*") if path.is_file()})
                    if destination.startswith("."):
                        self.assertFalse((root / destination).exists())

    def test_distribution_generation_preserves_runtime_under_output_parent_and_symlinks(self) -> None:
        for operation in ("tree", "archives"):
            for hazard in ("parent", "ancestor", "nested-link", "archive-link", "hard-link", "special-file"):
                with self.subTest(operation=operation, hazard=hazard), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    skills = copy_fixture_skills(root, ("portable-basic",))
                    runtime = root / "project/.codex/skills/portable-basic/SKILL.md"
                    runtime.parent.mkdir(parents=True)
                    runtime.write_bytes(b"user runtime bytes\n")
                    output = root / "output"
                    if hazard == "parent":
                        output = root / "project/.codex"
                    elif hazard == "ancestor":
                        output = root / "project"
                    elif hazard == "nested-link":
                        (output / "codex").mkdir(parents=True)
                        (output / "codex/.agents").symlink_to(root / "project/.codex", target_is_directory=True)
                    elif hazard == "archive-link":
                        output.mkdir()
                        (output / adapter_archive_name("codex", "v1.0.0")).symlink_to(runtime)
                    elif hazard == "special-file":
                        output.mkdir()
                        os.mkfifo(output / adapter_archive_name("codex", "v1.0.0"))
                    else:
                        target = (output / "codex/.agents/skills/portable-basic/SKILL.md" if operation == "tree"
                                  else output / adapter_archive_name("codex", "v1.0.0"))
                        target.parent.mkdir(parents=True)
                        os.link(runtime, target)
                    before = runtime.read_bytes()
                    with self.assertRaisesRegex(ValueError, "unsafe output"):
                        if operation == "tree":
                            sync_adapter_output("v1.0.0", skills_root=skills, output_root=output)
                        else:
                            build_adapter_archives("v1.0.0", output, skills_root=skills)
                    self.assertEqual(runtime.read_bytes(), before)
                    self.assertFalse((output / "claude").exists())

    def test_retired_gate_in_generated_output_is_unexpected_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"
            sync_adapter_output("v0.4.1", output_root=output_root)
            retired_path = (
                output_root
                / "codex"
                / ".agents"
                / "skills"
                / "spec-review"
                / "SKILL.md"
            )
            retired_path.parent.mkdir(parents=True)
            retired_path.write_text("retired\n", encoding="utf-8")

            drift = collect_adapter_drift_entries("v0.4.1", output_root=output_root)
            self.assertTrue(
                any(entry.category == "unexpected" and entry.path == retired_path for entry in drift),
                drift,
            )

    def test_adapter_generation_creates_independent_packages_and_thin_entrypoints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(
                root,
                (
                    "portable-basic",
                    "transformable-frontmatter",
                    "partial-portability",
                    "unsupported-frontmatter",
                ),
            )
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)

            for adapter, config in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    package_root = output_root / adapter
                    entrypoint = package_root / Path(config.entrypoint.as_posix())
                    skill_root = package_root / Path(config.skill_root.as_posix())
                    copied_project = root / f"copied-{adapter}"

                    shutil.copytree(package_root, copied_project)

                    self.assertTrue(entrypoint.is_file())
                    self.assertTrue(skill_root.is_dir())
                    self.assertTrue((copied_project / Path(config.entrypoint.as_posix())).is_file())
                    self.assertTrue((copied_project / Path(config.skill_root.as_posix())).is_dir())

                    entrypoint_text = entrypoint.read_text(encoding="utf-8")
                    self.assertIn("generated adapter output", entrypoint_text)
                    self.assertIn("canonical", entrypoint_text)
                    self.assertNotIn("# Portable Basic", entrypoint_text)

            self.assertFalse(
                (
                    output_root
                    / "opencode"
                    / ".opencode"
                    / "skills"
                    / "partial-portability"
                    / "SKILL.md"
                ).exists()
            )

    def test_adapter_generation_drops_transformed_frontmatter_for_non_codex(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("transformable-frontmatter",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)

            codex_skill = (
                output_root
                / "codex"
                / ".agents"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            ).read_text(encoding="utf-8")
            claude_skill = (
                output_root
                / "claude"
                / ".claude"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            ).read_text(encoding="utf-8")

            self.assertIn("argument-hint:", codex_skill)
            self.assertIn("schema-version:", codex_skill)
            self.assertIn("version:", codex_skill)
            self.assertNotIn("argument-hint:", claude_skill)
            self.assertNotIn("schema-version:", claude_skill)
            self.assertNotIn("version:", claude_skill)

    def test_adapter_generation_drift_check_detects_stale_and_unexpected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            self.assertEqual(
                collect_adapter_drift(
                    "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
                ),
                [],
            )

            stale_file = output_root / "codex" / "AGENTS.md"
            stale_file.write_text(
                stale_file.read_text(encoding="utf-8") + "\nstale\n",
                encoding="utf-8",
            )
            stale_drift = collect_adapter_drift(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )
            self.assertTrue(any("stale generated adapter file" in entry for entry in stale_drift))

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            unexpected_file = output_root / "codex" / "unexpected.txt"
            unexpected_file.write_text("unexpected\n", encoding="utf-8")
            unexpected_drift = collect_adapter_drift(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )
            self.assertTrue(
                any("unexpected generated adapter file" in entry for entry in unexpected_drift)
            )

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            self.assertFalse(unexpected_file.exists())
            self.assertEqual(
                collect_adapter_drift(
                    "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
                ),
                [],
            )

    def test_adapter_drift_entries_classify_generated_output_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            sorted(output_root.rglob("SKILL.md"))[0].unlink()
            stale_file = output_root / "codex" / "AGENTS.md"
            stale_file.write_text(stale_file.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
            unexpected_file = output_root / "codex" / "unexpected.txt"
            unexpected_file.write_text("unexpected\n", encoding="utf-8")

            entries = collect_adapter_drift_entries(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )

            categories = {entry.category for entry in entries}
            self.assertIn("missing", categories)
            self.assertIn("stale", categories)
            self.assertIn("unexpected", categories)
            self.assertTrue(
                all(entry.category in {"missing", "stale", "unexpected"} for entry in entries)
            )
            self.assertTrue(all(entry.path for entry in entries))
            self.assertTrue(all(entry.detail for entry in entries))

    def test_manifest_first_inspection_precedes_filesystem_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("portable-basic",))
            output_root = root / "dist" / "adapters"
            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            missing_skill = sorted(output_root.rglob("SKILL.md"))[0]
            missing_skill.unlink()
            stale_file = output_root / "codex" / "AGENTS.md"
            stale_file.write_text(stale_file.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
            unexpected_file = output_root / "codex" / "unexpected.txt"
            unexpected_file.write_text("unexpected\n", encoding="utf-8")

            call_order: list[str] = []
            real_manifest_read = adapter_distribution_module._inspect_generated_adapter_manifest
            real_file_collect = adapter_distribution_module._collect_generated_files

            def manifest_read(output_root: Path):
                call_order.append("manifest")
                return real_manifest_read(output_root)

            def file_collect(output_root: Path):
                call_order.append("filesystem")
                return real_file_collect(output_root)

            with patch.object(
                adapter_distribution_module,
                "_inspect_generated_adapter_manifest",
                side_effect=manifest_read,
            ), patch.object(
                adapter_distribution_module,
                "_collect_generated_files",
                side_effect=file_collect,
            ):
                entries = collect_adapter_drift_entries(
                    "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
                )

            self.assertEqual(call_order[:2], ["manifest", "filesystem"])
            categories = {entry.category for entry in entries}
            self.assertIn("missing", categories)
            self.assertIn("stale", categories)
            self.assertIn("unexpected", categories)
            self.assertNotIn("manifest-error", categories)

    def test_manifest_errors_are_structured_and_displayed_completely(self) -> None:
        cases = (
            (
                "missing",
                lambda manifest_path: manifest_path.unlink(),
                "generated adapter manifest is missing",
            ),
            (
                "malformed",
                lambda manifest_path: manifest_path.write_text("version: [\n", encoding="utf-8"),
                "malformed",
            ),
            (
                "version",
                lambda manifest_path: manifest_path.write_text(
                    manifest_path.read_text(encoding="utf-8").replace(
                        "version: 0.1.0-rc.1",
                        "version: 0.0.0",
                        1,
                    ),
                    encoding="utf-8",
                ),
                "version mismatch",
            ),
            (
                "contract",
                lambda manifest_path: manifest_path.write_text(
                    manifest_path.read_text(encoding="utf-8").replace(
                        "adapters: [codex, claude]",
                        "adapters: [codex]",
                        1,
                    ),
                    encoding="utf-8",
                ),
                "adapter list mismatch",
            ),
        )

        for _name, mutate_manifest, expected_detail in cases:
            with self.subTest(_name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                skills_root = copy_fixture_skills(root, ("portable-basic",))
                output_root = root / "dist" / "adapters"
                sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
                missing_skill = sorted(output_root.rglob("SKILL.md"))[0]
                missing_skill.unlink()
                manifest_path = output_root / "manifest.yaml"
                mutate_manifest(manifest_path)

                entries = collect_adapter_drift_entries(
                    "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
                )
                manifest_entries = [
                    entry for entry in entries if entry.category == "manifest-error"
                ]
                normal_output = format_adapter_drift_normal(
                    entries,
                    version="0.1.0-rc.1",
                    output_root=output_root,
                )
                verbose_output = format_adapter_drift_verbose(
                    entries,
                    version="0.1.0-rc.1",
                    output_root=output_root,
                )

                self.assertTrue(manifest_entries)
                self.assertTrue(all(entry.path == manifest_path for entry in manifest_entries))
                self.assertTrue(any(expected_detail in entry.detail for entry in manifest_entries))
                self.assertIn("missing", {entry.category for entry in entries})
                self.assertIn("manifest-error", normal_output)
                self.assertIn(str(manifest_path), normal_output)
                self.assertIn("fix or regenerate the generated adapter manifest", normal_output)
                self.assertIn(expected_detail, verbose_output)
                self.assertIn(str(manifest_path), verbose_output)

    def test_canonical_source_failures_are_structured_adapter_drift_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "skills"
            broken_skill = skills_root / "broken-skill"
            broken_skill.mkdir(parents=True)
            (broken_skill / "SKILL.md").write_text("---\nname: broken-skill\n", encoding="utf-8")
            output_root = root / "dist" / "adapters"

            entries = collect_adapter_drift_entries(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )

            self.assertTrue(entries)
            self.assertTrue(all(entry.category == "canonical-source-error" for entry in entries))
            self.assertTrue(any("canonical skill validation failed" in entry.detail for entry in entries))

    def test_adapter_drift_collection_does_not_write_persistent_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(root)
            before_files = {path.relative_to(root) for path in root.rglob("*") if path.is_file()}

            entries = collect_adapter_drift_entries(
                "0.1.0-rc.1", skills_root=skills_root, output_root=output_root
            )

            after_files = {path.relative_to(root) for path in root.rglob("*") if path.is_file()}
            self.assertEqual(entries, ())
            self.assertEqual(after_files, before_files)
            self.assertFalse(any(".cache" in path.parts for path in after_files))

    def test_generated_manifest_matches_version_and_generated_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(
                root,
                (
                    "portable-basic",
                    "partial-portability",
                    "unsupported-frontmatter",
                ),
            )
            output_root = root / "dist" / "adapters"

            sync_adapter_output("0.1.0-rc.1", skills_root=skills_root, output_root=output_root)
            rc_manifest = (output_root / "manifest.yaml").read_text(encoding="utf-8")

            self.assertIn("version: 0.1.0-rc.1", rc_manifest)
            self.assertIn("  portable-basic:", rc_manifest)
            self.assertIn("    adapters: [codex, claude]", rc_manifest)
            self.assertIn("  partial-portability:", rc_manifest)
            self.assertIn("    adapters: [codex, claude]", rc_manifest)
            self.assertIn("  unsupported-frontmatter:", rc_manifest)
            self.assertIn("    adapters: [codex]", rc_manifest)
            self.assertTrue(
                (
                    output_root
                    / "claude"
                    / ".claude"
                    / "skills"
                    / "portable-basic"
                    / "SKILL.md"
                ).is_file()
            )
            self.assertFalse(
                (
                    output_root
                    / "claude"
                    / ".claude"
                    / "skills"
                    / "unsupported-frontmatter"
                    / "SKILL.md"
                ).exists()
            )

            stable_files = expected_adapter_files(
                "0.1.0",
                skills_root=skills_root,
            )
            self.assertIn("version: 0.1.0", stable_files[Path("manifest.yaml")])

    def test_validate_adapter_output_accepts_generated_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(root)

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertEqual(errors, [])

    def test_validate_adapter_output_rejects_missing_adapter_directory_and_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(root)
            shutil.rmtree(output_root / "claude")

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("missing adapter directory: claude" in error for error in errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(root)
            (output_root / "claude" / "CLAUDE.md").unlink()

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("missing instruction entrypoint: claude" in error for error in errors))

    def test_adapter_generation_rejects_malformed_canonical_skill_before_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "skills"
            broken_skill = skills_root / "broken-skill"
            broken_skill.mkdir(parents=True)
            (broken_skill / "SKILL.md").write_text(
                "---\nname: broken-skill\n",
                encoding="utf-8",
            )
            output_root = root / "dist" / "adapters"

            with self.assertRaisesRegex(ValueError, "canonical skill validation failed"):
                sync_adapter_output(
                    "0.1.0-rc.1",
                    skills_root=skills_root,
                    output_root=output_root,
                )

            self.assertFalse(output_root.exists())

    def test_validate_adapter_output_rejects_missing_or_malformed_canonical_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            missing_skills_root = root / "missing-skills"
            output_root = root / "dist" / "adapters"

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=missing_skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("canonical skills root does not exist" in error for error in errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(root, ("portable-basic",))
            broken_skill = skills_root / "broken-skill"
            broken_skill.mkdir()
            (broken_skill / "SKILL.md").write_text(
                "---\nname: broken-skill\n",
                encoding="utf-8",
            )

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("canonical skill validation failed" in error for error in errors))

    def test_validate_adapter_output_rejects_manifest_file_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(root, ("portable-basic",))
            manifest_path = output_root / "manifest.yaml"
            manifest_path.write_text(
                manifest_path.read_text(encoding="utf-8").replace(
                    "adapters: [codex, claude]",
                    "adapters: [codex]",
                    1,
                ),
                encoding="utf-8",
            )

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("adapter list mismatch: portable-basic" in error for error in errors))
            self.assertTrue(
                any(
                    "generated skill is not listed in manifest: claude/portable-basic" in error
                    for error in errors
                )
            )

    def test_validate_adapter_output_rejects_unsupported_non_codex_metadata_leak(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(root, ("transformable-frontmatter",))
            codex_skill = (
                output_root
                / "codex"
                / ".agents"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            )
            claude_skill = (
                output_root
                / "claude"
                / ".claude"
                / "skills"
                / "transformable-frontmatter"
                / "SKILL.md"
            )
            claude_skill.write_text(codex_skill.read_text(encoding="utf-8"), encoding="utf-8")

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(
                any(
                    "unsupported metadata in claude/transformable-frontmatter: argument-hint" in error
                    for error in errors
                )
            )

    def test_validate_adapter_output_rejects_security_violations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(root, ("portable-basic",))
            entrypoint = output_root / "codex" / "AGENTS.md"
            entrypoint.write_text(
                entrypoint.read_text(encoding="utf-8")
                + "\n-----BEGIN PRIVATE KEY-----\n/home/alice/.ssh/id_rsa\n--dangerously-skip-permissions\n",
                encoding="utf-8",
            )

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(any("private key delimiter" in error for error in errors))
            self.assertTrue(any("machine-local absolute path" in error for error in errors))
            self.assertTrue(any("permission bypass" in error for error in errors))
