"""Mapped resource closure across generated, archived and installed boundaries."""

from __future__ import annotations

import sys
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging.adapter_distribution import ADAPTERS, POST_CUTOVER_ADAPTER_SKILLS, SUPPORTED_ADAPTERS, adapter_archive_name, build_adapter_archives, collect_skill_reports, sync_adapter_output, validate_adapter_archives, validate_adapter_output, validate_clean_install_smoke
from lib.validation.boundary_first_reference import GOVERNED_SKILLS, inventory_digest, load_resource_manifest, raw_sha256
from adapter_fixture_helpers import (configure_adapter_case, generate_fixture_adapters)


class AdapterResourcesTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        configure_adapter_case(self.addCleanup)

    def test_validate_adapter_output_rejects_stale_mapped_resource_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(
                root,
                ("portable-with-assets",),
            )
            generated_resource = (
                output_root
                / "codex"
                / ".agents"
                / "skills"
                / "portable-with-assets"
                / "assets"
                / "template.md"
            )
            generated_resource.write_text(
                generated_resource.read_text(encoding="utf-8") + "\nstale\n",
                encoding="utf-8",
            )

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(
                any(
                    "mapped resource parity mismatch: codex/portable-with-assets: "
                    "assets/template.md" in error
                    and "canonical sha256=" in error
                    and "generated sha256=" in error
                    for error in errors
                ),
                errors,
            )

    def test_boundary_first_archives_and_clean_installs_preserve_all_resources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temporary_root = Path(tmp)
            output_dir = temporary_root / "release-output"
            generated_root = temporary_root / "generated"
            version = "v0.3.6"
            sync_adapter_output(
                version,
                skills_root=ROOT / "skills",
                output_root=generated_root,
            )
            build_adapter_archives(version, output_dir, skills_root=ROOT / "skills")

            self.assertEqual(
                [],
                validate_adapter_archives(
                    version,
                    output_dir,
                    skills_root=ROOT / "skills",
                ),
            )
            manifest = load_resource_manifest(ROOT)
            reports = {
                report.name: report
                for report in collect_skill_reports(ROOT / "skills")
            }
            public_governed_skills = tuple(
                sorted(set(GOVERNED_SKILLS) & set(POST_CUTOVER_ADAPTER_SKILLS))
            )
            for skill_name in public_governed_skills:
                self.assertEqual(
                    reports[skill_name].included_adapters,
                    SUPPORTED_ADAPTERS,
                    skill_name,
                )
            expected_records = {
                (Path("skills") / skill_name / resource.target).as_posix(): raw_sha256(
                    (ROOT / resource.source).read_bytes()
                )
                for skill_name in public_governed_skills
                for resource in manifest.resources
                if skill_name in resource.consumers
            }
            expected_digest = inventory_digest(expected_records)
            seen: set[tuple[str, str, str]] = set()
            for adapter_name in SUPPORTED_ADAPTERS:
                config = ADAPTERS[adapter_name]
                archive_path = output_dir / adapter_archive_name(adapter_name, version)
                generated_records: dict[str, str] = {}
                archive_records: dict[str, str] = {}
                with zipfile.ZipFile(archive_path) as archive:
                    for skill_name in public_governed_skills:
                        skill_entry = config.skill_path(skill_name).as_posix()
                        self.assertTrue(archive.read(skill_entry))
                        for resource in manifest.resources:
                            if skill_name not in resource.consumers:
                                continue
                            reference_entry = (
                                config.skill_root
                                / skill_name
                                / resource.target
                            ).as_posix()
                            self.assertEqual(
                                archive.read(reference_entry),
                                (ROOT / resource.source).read_bytes(),
                            )
                            logical_path = (
                                Path("skills") / skill_name / resource.target
                            ).as_posix()
                            generated_path = (
                                generated_root
                                / adapter_name
                                / config.skill_root
                                / skill_name
                                / resource.target
                            )
                            generated_records[logical_path] = raw_sha256(
                                generated_path.read_bytes()
                            )
                            archive_records[logical_path] = raw_sha256(
                                archive.read(reference_entry)
                            )
                            seen.add(
                                (adapter_name, skill_name, resource.resource_id)
                            )
                self.assertEqual(len(generated_records), len(expected_records))
                self.assertEqual(inventory_digest(generated_records), expected_digest)
                self.assertEqual(len(archive_records), len(expected_records))
                self.assertEqual(inventory_digest(archive_records), expected_digest)
            expected = {
                (adapter_name, skill_name, resource.resource_id)
                for skill_name in public_governed_skills
                for adapter_name in SUPPORTED_ADAPTERS
                for resource in manifest.resources
                if skill_name in resource.consumers
            }
            self.assertEqual(seen, expected)

            installed_identities: dict[str, tuple[int, str]] = {}

            def capture_runner(command, **kwargs):
                result = subprocess.run(command, **kwargs)
                if result.returncode != 0:
                    return result
                adapter_name = command[command.index("init") + 1]
                config = ADAPTERS[adapter_name]
                project_root = Path(kwargs["cwd"])
                records: dict[str, str] = {}
                for resource in manifest.resources:
                    for skill_name in sorted(
                        set(resource.consumers) & set(public_governed_skills)
                    ):
                        installed_path = (
                            project_root
                            / config.skill_root
                            / skill_name
                            / resource.target
                        )
                        logical_path = (
                            Path("skills") / skill_name / resource.target
                        ).as_posix()
                        records[logical_path] = raw_sha256(installed_path.read_bytes())
                installed_identities[adapter_name] = (
                    len(records),
                    inventory_digest(records),
                )
                return result

            self.assertEqual(
                [],
                validate_clean_install_smoke(
                    version,
                    output_dir,
                    skills_root=ROOT / "skills",
                    skill_names=public_governed_skills,
                    command_runner=capture_runner,
                ),
            )
            self.assertEqual(
                installed_identities,
                {
                    adapter_name: (len(expected_records), expected_digest)
                    for adapter_name in SUPPORTED_ADAPTERS
                },
            )

    def test_validate_adapter_output_rejects_missing_mapped_resource(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root, output_root = generate_fixture_adapters(
                root,
                ("portable-with-assets",),
            )
            (
                output_root
                / "claude"
                / ".claude"
                / "skills"
                / "portable-with-assets"
                / "assets"
                / "template.md"
            ).unlink()

            errors = validate_adapter_output(
                "0.1.0-rc.1",
                skills_root=skills_root,
                output_root=output_root,
            )

            self.assertTrue(
                any(
                    "mapped resource missing: claude/portable-with-assets: "
                    "assets/template.md in generated adapter output claude" in error
                    for error in errors
                ),
                errors,
            )
