"""Public packaging guidance, CI and release caller contracts."""

from __future__ import annotations

import sys
from pathlib import Path
import json
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.packaging.adapter_distribution import sync_adapter_output
from adapter_fixture_helpers import (load_validate_release_module)


class AdapterContractTests(unittest.TestCase):
    maxDiff = None

    def test_validate_adapters_cli_rejects_retired_repository_output(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "validate-adapters.py"),
                "--version",
                "v0.1.3",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing adapter directory", result.stdout)

    def test_ci_script_runs_adapter_checks_and_filters_generated_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '--quiet')
            for name in ['README.md', 'dist/adapters/example.txt']:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('before')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-m', 'Fixture')
            for name in ['README.md', 'dist/adapters/example.txt']:
                (root / name).write_text('after')
            driver = ("import json,sys; from pathlib import Path; "
                      "sys.path.insert(0,sys.argv[1]); from lib.validation.validation_execution import compose_mode; "
                      "print(json.dumps([dict(id=p.check_id,args=p.args,deps=p.dependencies) "
                      "for p in compose_mode('broad-smoke',Path(sys.argv[2]))]))")
            env = {k:v for k,v in os.environ.items() if not k.startswith('RIGORLOOP_CI_')
                   and k not in {'REVIEW_ARTIFACT_ROOTS','RIGORLOOP_BROAD_SMOKE_CLASSIFICATION'}}
            result = subprocess.run([sys.executable, '-c', driver, str(ROOT/'scripts'), str(root/'output')],
                                    cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            plans = {p['id']:p for p in json.loads(result.stdout)}
            self.assertEqual(plans['adapters.full_regression']['args'],
                             ['python','tests/engineering/packaging/test-adapter-distribution.py'])
            self.assertEqual(plans['broad_smoke.adapters.build_archives']['args'],
                             ['python','scripts/build-adapters.py','--version','v0.1.3',
                              '--output-dir',str(root/'output/adapters-broad-smoke')])
            self.assertEqual(plans['broad_smoke.adapters.validate_archives']['args'],
                             ['python','scripts/validate-adapters.py','--root',
                              str(root/'output/adapters-broad-smoke'),'--version','v0.1.3'])
            self.assertIn('broad_smoke.adapters.build_archives',
                          plans['broad_smoke.adapters.validate_archives']['deps'])
            self.assertEqual(plans['current_records.validate']['args'],
                             ['python','scripts/validate-governed-lifecycle-cli.py'])

    def test_validate_release_rejects_retired_benchmark_path_options(self) -> None:
        module = load_validate_release_module()
        for option in ("--changed-path", "--changed-paths-file"):
            with self.subTest(option=option), self.assertRaises(SystemExit) as stopped:
                module.build_parser().parse_args(["--version", "v0.1.1", option, "unused"])
            self.assertEqual(stopped.exception.code, 2)

    def test_release_workflow_uses_tracked_release_notes(self) -> None:
        workflow_text = (ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )

        from lib.release.release_coordination import validate_workflow
        self.assertEqual(validate_workflow(ROOT), [])
        provider = (ROOT / 'scripts/lib/release/release_provider.py').read_text()
        self.assertIn("'--notes-file'", provider)
        self.assertIn("local_file(output, 'release-notes.md')", provider)
        self.assertNotIn('--generate-notes', provider)

    def test_release_workflow_gates_npm_publication_modes(self) -> None:
        from lib.release.release_coordination import validate_workflow
        self.assertEqual(validate_workflow(ROOT), [])
        workflow_root = ROOT / '.github/workflows'
        self.assertFalse((workflow_root / 'npm.yml').exists())
        self.assertFalse((workflow_root / 'publish-npm.yml').exists())

    def test_release_verify_rejects_missing_or_mismatched_trusted_commit(self) -> None:
        base_env = {
            "PATH": os.environ.get("PATH", ""),
            "GITHUB_ACTIONS": "true",
            "GITHUB_REF_NAME": "v0.4.0",
            "GITHUB_REF_TYPE": "tag",
            "RELEASE_VERIFY_DRY_RUN": "1",
        }
        missing = subprocess.run(
            ["bash", "scripts/release-verify.sh", "v0.4.0"],
            cwd=ROOT,
            env=base_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        mismatched = subprocess.run(
            ["bash", "scripts/release-verify.sh", "v0.4.0"],
            cwd=ROOT,
            env={**base_env, "RELEASE_TAG_COMMIT": "0" * 40},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("RELEASE_TAG_COMMIT", missing.stderr)
        self.assertNotEqual(mismatched.returncode, 0)
        self.assertIn("does not match checked HEAD", mismatched.stderr)

    def test_claude_entrypoint_documents_native_skill_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_root = Path(tmp) / "dist" / "adapters"
            sync_adapter_output("0.1.1", output_root=output_root)

            claude_root = output_root / "claude"
            text = (claude_root / "CLAUDE.md").read_text(encoding="utf-8")

            self.assertFalse((claude_root / ".claude" / "commands").exists())
            self.assertIn("Using RigorLoop skills", text)
            self.assertIn(".claude/skills/", text)
            self.assertIn("native Claude Code slash commands", text)
            for command in ("/proposal", "/design", "/implement", "/code-review", "/pr"):
                self.assertIn(command, text)
            self.assertNotIn("claude -p", text)
            self.assertNotIn("opencode run --command", text)

    def test_readme_exposes_the_current_compact_delivery_route(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        recommended = text.split("## Recommended Use", 1)[1].split("## Starting a new repository", 1)[0]

        self.assertIn(
            "proposal -> proposal-review -> design -> design-review -> plan -> delivery-review -> implement -> code-review -> verify",
            recommended,
        )
        self.assertIn("optional external integration", text)
        self.assertIn(
            "writes the final explanation only in a successful Verify report",
            text,
        )
        for retired_entrypoint in (
            "explain-change",
            "spec-review",
            "plan-review",
            "test-spec",
        ):
            self.assertNotIn(retired_entrypoint, recommended)

    def test_readme_describes_supported_invocation_and_conflict_forms(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Claude Code uses native skill slash commands", text)
        self.assertIn("--force", text)
        self.assertIn("OpenCode and `--write-state` are no longer supported", text)
        self.assertNotIn("opencode run --command", text)

    def test_public_docs_describe_adapter_support_and_generated_boundaries(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
            "dist/adapters/README.md": (ROOT / "dist" / "adapters" / "README.md").read_text(encoding="utf-8"),
            "AGENTS.md": (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            "release-notes.md": (
                ROOT / "docs" / "releases" / "v0.1.0" / "release-notes.md"
            ).read_text(encoding="utf-8"),
        }
        combined = "\n".join(docs.values()).lower()

        for term in ("codex", "claude", "opencode", "dist/adapters", ".codex/skills"):
            self.assertIn(term, combined)
        self.assertIn("ordinary contributors do not need all supported tools", combined)
        self.assertIn("external tool contracts", combined)
        self.assertIn("before changing release claims", combined)
        self.assertIn("skills/", combined)
        self.assertNotIn("marketplace package", combined)
        self.assertNotIn("package-manager distribution", combined)

    def test_public_adapter_support_surface_only_tracks_readme_and_manifest(self) -> None:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "dist/adapters/**",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        tracked = result.stdout.splitlines()

        self.assertEqual(
            tracked,
            [
                "dist/adapters/README.md",
                "dist/adapters/manifest.yaml",
            ],
        )
        self.assertFalse(any("/skills/" in path for path in tracked), tracked)
        self.assertFalse(any(path.endswith(("AGENTS.md", "CLAUDE.md")) for path in tracked), tracked)
        self.assertFalse(any("/commands/" in path for path in tracked), tracked)

    def test_public_adapter_readme_documents_archive_install_contract(self) -> None:
        text = (ROOT / "dist/adapters/README.md").read_text(encoding="utf-8")
        for required in ("skills/", "support matrix", "release archives", "rigorloop-adapter-codex-<version>.zip", "rigorloop-adapter-claude-<version>.zip", ".agents/skills/", ".claude/skills/", "--force", "--from-archive", "--dry-run", "outside skill discovery", "project `rigorloop.yaml` and `rigorloop.lock`"):
            self.assertIn(required, text)
        self.assertNotIn("rigorloop-adapter-opencode-<version>.zip", text)
        self.assertIn("Historical archives and evidence remain unchanged", text)

    def test_root_guidance_points_to_adapter_install_contract_surface(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        constitution = (ROOT / "CONSTITUTION.md").read_text(encoding="utf-8")
        self.assertIn("dist/adapters/README.md", agents)
        self.assertIn("docs/design/engineering/packaging.md", agents)
        self.assertIn("docs/design/system.md", constitution)
        self.assertTrue((ROOT / "dist/adapters/README.md").is_file())

    def test_adapter_readme_records_adapter_artifact_metadata_location(self) -> None:
        text = (ROOT / "dist" / "adapters" / "README.md").read_text(encoding="utf-8")

        self.assertNotIn("docs/workflows.md", text)
        self.assertIn("Adapter artifact metadata", text)
        self.assertIn("`docs/reports/adapter-artifacts/releases/<version>.yaml`", text)
        self.assertIn("support matrix", text)

    def test_contributor_docs_keep_codex_runtime_local_and_untracked(self) -> None:
        docs = {
            "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        }

        for path, text in docs.items():
            with self.subTest(path=path):
                self.assertIn("dist/adapters/README.md", text)
                self.assertIn("release archives", text.lower())
                self.assertIn("`.codex/skills/`", text)
                self.assertIn("untracked", text)
                self.assertNotIn(
                    "Regenerate it with `python scripts/build-skills.py` when needed.",
                    text,
                )
                self.assertNotIn("install or copy public Codex adapter output from `dist/adapters/codex/.agents/skills/`", text)
                self.assertNotIn("Do not hand-edit local Codex runtime state", text)
                self.assertNotIn("Do not hand-edit generated Codex compatibility output", text)
                self.assertNotIn("MUST NOT be hand-edited or tracked", text)

    def test_adapter_manifest_remains_metadata_only(self) -> None:
        manifest_path = ROOT / "dist" / "adapters" / "manifest.yaml"
        manifest = manifest_path.read_text(encoding="utf-8")

        self.assertIn("version:", manifest)
        self.assertIn("skills:", manifest)
        self.assertNotIn("command_aliases:", manifest)
        self.assertNotIn("# ", manifest)
        self.assertNotIn("## ", manifest)
        self.assertNotIn("description:", manifest)
        self.assertNotIn("argument-hint:", manifest)
        self.assertNotIn("When to use", manifest)
        self.assertNotIn("How to use", manifest)

    def test_generated_adapter_archives_are_not_committed(self) -> None:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        archives = [
            path
            for path in result.stdout.splitlines()
            if path.endswith(".zip") or path.endswith(".tar.gz")
        ]

        self.assertEqual([], [path for path in archives if "rigorloop-adapter-" in path])
