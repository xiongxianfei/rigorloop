"""Actual archive membership, byte parity and archive integrity."""

from __future__ import annotations

import sys
from pathlib import Path
import hashlib
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging import adapter_distribution as adapter_distribution_module
from lib.packaging.adapter_distribution import ADAPTERS, POST_CUTOVER_ADAPTER_SKILLS, RETIRED_PROGRESSION_SKILLS, SUPPORTED_ADAPTERS, adapter_archive_name, build_adapter_archives, validate_adapter_archives, validate_adapter_output, validate_clean_install_smoke
from adapter_fixture_helpers import (configure_adapter_case, copy_fixture_skills, generate_fixture_adapters)


class AdapterArchiveTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        configure_adapter_case(self.addCleanup)

    def test_tree_hash_representation_has_independent_order_normalization_and_count(self):
        # These are the contract's literal manifest order and normalized bytes,
        # deliberately unlike ZIP insertion order or locale/casefold ordering.
        normalized = (("Z.md", b"Z\nkeep  \n"), ("a-b.md", b"dash\n"),
                      ("a.md", b"A\n"), ("a_b.md", b"underscore\n"),
                      ("binary.bin", b"\xef\xbb\xbf\x00\r\n\xff"),
                      ("e\u0301.md", b"decomposed\n"), ("t.md", b"t\n"),
                      ("ß.md", b"sharp\n"), ("é.md", b"composed\n"), ("İ.md", b"dot\n"))
        manifest = b"rigorloop-tree-hash-v2\n" + b"".join(
            name.encode() + b"\t" + hashlib.sha256(content).hexdigest().encode() + b"\n"
            for name, content in normalized)
        expected = (hashlib.sha256(manifest).hexdigest(), 10)
        for order in (tuple(range(10)), tuple(reversed(range(10)))):
            with self.subTest(order=order), tempfile.TemporaryDirectory() as tmp:
                archive_path = Path(tmp) / "tree.zip"
                with zipfile.ZipFile(archive_path, "w") as archive:
                    archive.writestr("outside.md", b"not in the install root")
                    archive.writestr(".agents/skills/empty/", b"")
                    link = zipfile.ZipInfo(".agents/skills/linked.md")
                    link.create_system = 3
                    link.external_attr = 0o120777 << 16
                    archive.writestr(link, b"outside.md")
                    for index in order:
                        name, content = normalized[index]
                        if name == "Z.md":
                            content = b"\xef\xbb\xbfZ\r\nkeep  \r"
                        archive.writestr(".agents/skills/" + name, content)
                self.assertEqual(adapter_distribution_module._archive_root_hash(
                    archive_path, ".agents/skills", algorithm="rigorloop-tree-hash-v2"), expected)
                # A changed regular file must change the digest, not its count.
                with zipfile.ZipFile(archive_path, "w") as archive:
                    for name, content in normalized:
                        archive.writestr(".agents/skills/" + name,
                                         content + b"changed" if name == "a.md" else content)
                changed = adapter_distribution_module._archive_root_hash(archive_path, ".agents/skills", algorithm="rigorloop-tree-hash-v2")
                self.assertNotEqual(changed[0], expected[0])
                self.assertEqual(changed[1], expected[1])

    def test_public_tree_hash_uses_same_representation_and_excludes_symlinks(self):
        from lib.release.release_transaction import _tree_hash_and_file_count
        normalized = (("a.md", b"A\n"), ("binary.bin", b"\xef\xbb\xbf\x00\r\n\xff"),
                      ("Z.md", b"Z\nkeep  \n"))
        manifest = b"rigorloop-tree-hash-v1\n" + b"".join(
            name.encode() + b"\t" + hashlib.sha256(content).hexdigest().encode() + b"\n"
            for name, content in normalized)
        expected = (hashlib.sha256(manifest).hexdigest(), 3)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "installed"
            root.mkdir()
            for name, content in reversed(normalized):
                (root / name).write_bytes(b"\xef\xbb\xbfZ\r\nkeep  \r" if name == "Z.md" else content)
            (root / "empty").mkdir()
            outside = Path(tmp) / "outside"
            outside.write_bytes(b"unrelated")
            (root / "linked.md").symlink_to(outside)
            self.assertEqual(_tree_hash_and_file_count(root), expected)
            outside.write_bytes(b"outside changed")
            self.assertEqual(_tree_hash_and_file_count(root), expected)
            (root / "a.md").write_bytes(b"changed\n")
            changed = _tree_hash_and_file_count(root)
            self.assertNotEqual(changed[0], expected[0])
            self.assertEqual(changed[1], expected[1])

    def test_current_candidate_metadata_matches_generated_route_only_archives(self) -> None:
        version = "v0.5.1"
        with tempfile.TemporaryDirectory(prefix="route-candidate-") as temp_dir:
            output = Path(temp_dir)
            archives = build_adapter_archives(version, output)
            generated = adapter_distribution_module._local_release_candidate_metadata(version, output)

            # Current canonical archives have fresh identities. Historical bundled
            # release metadata remains immutable; packed current metadata is proved
            # by the actual candidate integration test.
            self.assertEqual({row['adapter'] for row in generated['artifacts']}, {'codex', 'claude'})
            self.assertEqual(validate_adapter_archives(version, output), [])
            for artifact in generated['artifacts']:
                archive_path = output / artifact['archive']
                self.assertEqual(artifact['sha256'], hashlib.sha256(archive_path.read_bytes()).hexdigest())
                self.assertEqual(artifact['size_bytes'], archive_path.stat().st_size)
                root = artifact['install_root'] + '/'
                with zipfile.ZipFile(archive_path) as archive:
                    names = [name for name in archive.namelist() if name.startswith(root) and not name.endswith('/')]
                self.assertEqual(artifact['file_count'], len(names))
                self.assertEqual(artifact['skill_names'], sorted({name[len(root):].split('/')[0] for name in names}))
            for archive_path in archives:
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    pr_entry = next(name for name in names if name.endswith("/pr/SKILL.md"))
                    verify_entry = next(
                        name for name in names
                        if name.endswith("/verify/references/successful-explanation.md")
                    )
                    pr_body = archive.read(pr_entry).decode("utf-8")
                    verify_explanation = archive.read(verify_entry).decode("utf-8")
                self.assertTrue(any("/route/SKILL.md" in name for name in names))
                self.assertFalse(any("/workflow/" in name for name in names))
                self.assertIn("evidence suffix: `none`, `evidence-only`, `invalidating`", pr_body)
                self.assertIn("any commit count or direct-parent topology", pr_body)
                self.assertNotIn("exactly one direct-child verify-owned evidence commit", pr_body)
                self.assertIn(
                    "Keep substantive success, durable save and current reliance distinct",
                    verify_explanation,
                )

    def test_current_archives_omit_explain_change_and_package_complete_verify_resources(self) -> None:
        with tempfile.TemporaryDirectory(prefix="current-adapters-") as temp_dir:
            output = Path(temp_dir)
            archives = build_adapter_archives("v0.1.6", output)
            self.assertEqual(validate_adapter_archives("v0.1.6", output), [])
            required = {
                "final-impact-analysis.md",
                "evidence-applicability.md",
                "successful-explanation.md",
                "verify-report-skeleton.md",
            }
            for archive_path in archives:
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    verify_entry = next(name for name in names if name.endswith("/verify/SKILL.md"))
                    verify_body = archive.read(verify_entry).decode("utf-8")
                self.assertFalse(any("/explain-change/" in name for name in names))
                self.assertTrue(
                    all(any(name.endswith(f"/verify/{'assets' if item.endswith('skeleton.md') else 'references'}/{item}") for name in names) for item in required)
                )
                for forbidden in (
                    "after `explain-change`",
                    "explain-change artifact",
                    "current explanation",
                    "rationale to `explain-change`",
                ):
                    self.assertNotIn(forbidden, verify_body)
                self.assertIn(
                    "final explanation only after successful final readiness",
                    verify_body,
                )

    def test_current_archive_validation_rejects_mixed_explain_change_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory(prefix="current-mixed-") as temp_dir:
            output = Path(temp_dir)
            archives = build_adapter_archives("v0.1.6", output)
            target = archives[0]
            with zipfile.ZipFile(target, "a") as archive:
                archive.writestr(".agents/skills/explain-change/SKILL.md", "retired")
            errors = validate_adapter_archives("v0.1.6", output)
            self.assertTrue(any("unexpected entries" in error and "explain-change" in error for error in errors))

    def test_build_adapter_archives_creates_required_release_archives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-basic", "transformable-frontmatter"))
            output_dir = root / "release-output"

            archives = build_adapter_archives(
                "v0.1.2",
                output_dir,
                skills_root=root / "skills",
            )

            self.assertEqual(
                [archive.name for archive in archives],
                [
                    "rigorloop-adapter-codex-v0.1.2.zip",
                    "rigorloop-adapter-claude-v0.1.2.zip",
                ],
            )
            for archive in archives:
                self.assertEqual(archive.parent, output_dir)
                self.assertTrue(archive.is_file())

            self.assertFalse((output_dir / "dist").exists())
            self.assertEqual([], validate_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills"))

    def test_adapter_archives_install_under_target_project_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")

            expected = {
                "codex": ("AGENTS.md", ".agents/skills/portable-basic/SKILL.md"),
                "claude": ("CLAUDE.md", ".claude/skills/portable-basic/SKILL.md"),
            }
            for adapter, required_entries in expected.items():
                archive_path = output_dir / adapter_archive_name(adapter, "v0.1.2")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                for entry in required_entries:
                    self.assertIn(entry, names)
                self.assertFalse(
                    any(name.startswith(f"{adapter}/") or name.startswith("dist/") for name in names)
                )

    def test_distribution_archives_have_independent_complete_resource_inventory(self) -> None:
        # Independent filesystem oracle: do not use the producer's inventory helper.
        canonical = {path.relative_to(ROOT / "skills").as_posix(): path.read_bytes()
                     for path in (ROOT / "skills").rglob("*") if path.is_file()}
        with tempfile.TemporaryDirectory() as tmp:
            archives = build_adapter_archives("v1.0.0", Path(tmp))
            self.assertEqual(validate_adapter_archives("v1.0.0", Path(tmp)), [])
            # One actual candidate/install operation covers the formerly separate
            # discovery and proposal happy paths; assertions inspect installed resources.
            self.assertEqual(validate_clean_install_smoke(
                "v1.0.0", Path(tmp), skill_names=("explore", "research", "proposal", "proposal-review")), [])
            self.assertEqual(len(archives), 2)
            for target, archive_path in zip(("codex", "claude"), archives):
                prefix = {"codex": ".agents/skills/", "claude": ".claude/skills/"}[target]
                with zipfile.ZipFile(archive_path) as archive:
                    actual = {name[len(prefix):]: archive.read(name) for name in archive.namelist() if name.startswith(prefix)}
                self.assertEqual(set(actual), set(canonical), target)
                # Full emitted entrypoints include transformed Claude frontmatter;
                # canonical guidance checks and body parity alone cannot guard it.
                for skill_name in ("explore", "research"):
                    for forbidden in (b"skills/explore/SKILL.md", b"skills/research/SKILL.md",
                                      b"templates/shared", b"dist/adapters"):
                        self.assertNotIn(forbidden, actual[f"{skill_name}/SKILL.md"])
                for name, expected in canonical.items():
                    if target == "codex" or not name.endswith("/SKILL.md"):
                        self.assertEqual(actual[name], expected, f"{target}/{name}")
                    else:
                        # Only declared frontmatter transformations are permitted;
                        # existing metadata tests check that projection separately.
                        self.assertEqual(actual[name].split(b"---", 2)[2], expected.split(b"---", 2)[2], name)

    def test_distribution_generated_skill_structure_is_validated_independently(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills, output = generate_fixture_adapters(root, ("portable-basic",))
            for target in ("codex", "claude"):
                skill = output / target / ADAPTERS[target].skill_root / "portable-basic/SKILL.md"
                original = skill.read_bytes()
                skill.write_text("# Missing frontmatter\n")
                errors = validate_adapter_output("0.1.0-rc.1", skills_root=skills, output_root=output)
                self.assertTrue(any("file must begin with YAML frontmatter" in error and str(skill) in error for error in errors), errors)
                skill.write_bytes(original)

    def test_adapter_archives_include_packaged_skill_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.5", output_dir, skills_root=root / "skills")

            expected = {
                "codex": ".agents/skills/portable-with-assets/assets/template.md",
                "claude": ".claude/skills/portable-with-assets/assets/template.md",
            }
            for adapter, asset_entry in expected.items():
                archive_path = output_dir / adapter_archive_name(adapter, "v0.1.5")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    self.assertIn(asset_entry, names)
                    self.assertEqual(
                        archive.read(asset_entry).decode("utf-8"),
                        (root / "skills" / "portable-with-assets" / "assets" / "template.md").read_text(
                            encoding="utf-8"
                        ),
                    )

            self.assertEqual([], validate_adapter_archives("v0.1.5", output_dir, skills_root=root / "skills"))

    def test_adapter_archives_include_route_resources_without_retired_guide_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            build_adapter_archives("v0.1.3", output_dir, skills_root=ROOT / "skills")

            packaged_adapters: list[str] = []
            expected_text = (ROOT / "skills" / "route" / "references" / "governed-lifecycle-routing.md").read_text(encoding="utf-8")
            for adapter in SUPPORTED_ADAPTERS:
                config = ADAPTERS[adapter]
                skill_entry = config.skill_path("route").as_posix()
                resource_entry = (config.skill_root / "route" / "references" / "governed-lifecycle-routing.md").as_posix()
                archive_path = output_dir / adapter_archive_name(adapter, "v0.1.3")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                    if skill_entry not in names:
                        continue
                    packaged_adapters.append(adapter)
                    self.assertIn(resource_entry, names)
                    self.assertEqual(archive.read(resource_entry).decode("utf-8"), expected_text)
                    self.assertNotIn((config.skill_root / "route" / "assets" / "workflows-skeleton.md").as_posix(), names)
                    self.assertNotIn((config.skill_root / "route" / "references" / "workflow-guide-authoring.md").as_posix(), names)

            self.assertTrue(packaged_adapters)
            self.assertEqual([], validate_adapter_archives("v0.1.3", output_dir, skills_root=ROOT / "skills"))

    def test_validate_adapter_archives_rejects_stale_mapped_resource_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.5", output_dir, skills_root=root / "skills")
            archive_path = output_dir / adapter_archive_name("codex", "v0.1.5")
            entry_name = ".agents/skills/portable-with-assets/assets/template.md"

            with zipfile.ZipFile(archive_path) as archive:
                entries = {
                    name: archive.read(name)
                    for name in archive.namelist()
                    if not name.endswith("/")
                }
            entries[entry_name] = b"stale\n"
            with zipfile.ZipFile(archive_path, "w") as archive:
                for name, content in sorted(entries.items()):
                    archive.writestr(name, content)

            errors = validate_adapter_archives("v0.1.5", output_dir, skills_root=root / "skills")

            self.assertTrue(
                any(
                    "mapped resource parity mismatch: codex/portable-with-assets: "
                    "assets/template.md" in error
                    and "canonical sha256=" in error
                    and "archive sha256=" in error
                    for error in errors
                ),
                errors,
            )

    def test_boundary_first_archive_drift_reports_exact_layer_and_hashes(self) -> None:
        cases = (
            ("portable-with-assets", "references/boundary-first-method-v1.md"),
            ("portable-with-assets", "references/boundary-first-feature-authoring-v1.md"),
        )
        for skill_name, relative_resource in cases:
            with self.subTest(layer=relative_resource), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                skills_root = copy_fixture_skills(root, (skill_name,))
                resource = skills_root / skill_name / relative_resource
                resource.parent.mkdir()
                resource.write_bytes(b"# Boundary reference\nIndependent fixture content.\n")
                skill_path = skills_root / skill_name / "SKILL.md"
                body = skill_path.read_text(encoding="utf-8")
                self.assertIn("## Resource map\n", body)
                skill_path.write_text(body.replace("## Resource map\n",
                    f"## Resource map\n\n- READ `{relative_resource}` when checking this fixture.\n", 1), encoding="utf-8")
                output_dir = root / "release-output"
                version = "v0.3.6"
                build_adapter_archives(version, output_dir, skills_root=skills_root)
                self.assertEqual(validate_adapter_archives(version, output_dir, skills_root=skills_root), [])
                archive_path = output_dir / adapter_archive_name("codex", version)
                entry_name = (
                    ADAPTERS["codex"].skill_root
                    / skill_name
                    / relative_resource
                ).as_posix()
                with zipfile.ZipFile(archive_path) as archive:
                    entries = {
                        name: archive.read(name)
                        for name in archive.namelist()
                        if not name.endswith("/")
                    }
                entries[entry_name] = b"stale boundary reference\n"
                with zipfile.ZipFile(archive_path, "w") as archive:
                    for name, content in sorted(entries.items()):
                        archive.writestr(name, content)

                errors = validate_adapter_archives(
                    version,
                    output_dir,
                    skills_root=skills_root,
                )

                self.assertTrue(
                    any(
                        f"mapped resource parity mismatch: codex/{skill_name}: "
                        f"{relative_resource}" in error
                        and "canonical sha256=" in error
                        and "archive sha256=" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_validate_adapter_archives_rejects_missing_required_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_fixture_skills(root, ("portable-basic",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")
            (output_dir / adapter_archive_name("claude", "v0.1.2")).unlink()

            errors = validate_adapter_archives("v0.1.2", output_dir, skills_root=root / "skills")

            self.assertTrue(
                any("missing adapter archive: claude" in error for error in errors),
                errors,
            )

    def test_gate_b_does_not_accept_one_targets_archive_as_another(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = copy_fixture_skills(root, ("portable-with-assets",))
            output_dir = root / "release-output"
            build_adapter_archives("v0.3.4", output_dir, skills_root=skills_root)
            codex = output_dir / adapter_archive_name("codex", "v0.3.4")
            claude = output_dir / adapter_archive_name("claude", "v0.3.4")
            claude.write_bytes(codex.read_bytes())

            errors = validate_adapter_archives(
                "v0.3.4", output_dir, skills_root=skills_root
            )

        self.assertTrue(
            any("claude" in error and ("root" in error or "missing" in error) for error in errors),
            errors,
        )

    def test_post_cutover_archives_have_exact_gate_inventory_for_every_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "release-output"
            version = "v0.4.1"
            archives = build_adapter_archives(version, output_dir)

            self.assertEqual(len(archives), len(SUPPORTED_ADAPTERS))
            for adapter_name in SUPPORTED_ADAPTERS:
                archive_path = output_dir / adapter_archive_name(adapter_name, version)
                skill_root = ADAPTERS[adapter_name].skill_root.as_posix().rstrip("/")
                with zipfile.ZipFile(archive_path) as archive:
                    names = set(archive.namelist())
                packaged = {
                    path.removeprefix(f"{skill_root}/").split("/", 1)[0]
                    for path in names
                    if path.startswith(f"{skill_root}/") and path.endswith("/SKILL.md")
                }
                with self.subTest(adapter=adapter_name):
                    self.assertEqual(packaged, set(POST_CUTOVER_ADAPTER_SKILLS))
                    self.assertTrue(RETIRED_PROGRESSION_SKILLS.isdisjoint(packaged))
