"""Public observation contracts, preservation and historical reader isolation."""

from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest
import subprocess

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import GitHubReleaseAsset, NpmPackageMetadata, ReleaseProfileError, load_release_profile, close_release_publication, validate_published_release_artifacts, validate_release_timing_evidence
from release_fixture_helpers import (make_prepared_release, make_recorded_release, relative_tree, write_public_evidence)
from release_provider_fixtures import RecordingPublicEvidenceProvider


class PublishedEvidenceCloseoutTests(unittest.TestCase):
    maxDiff = None

    def test_close_release_publication_fails_when_public_evidence_unavailable_without_modifying_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            before = relative_tree(root)
            provider = RecordingPublicEvidenceProvider(fail_github=True)

            result = close_release_publication(
                "v0.3.5",
                root=root,
                provider=provider,
            )

            after = relative_tree(root)

        self.assertTrue(any("GitHub" in error and "v0.3.5" in error for error in result.errors), result.errors)
        self.assertEqual(before, after)

    def test_close_release_publication_generates_published_evidence_and_validation_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            (root / "unrelated.bin").write_bytes(b"\x00\xffpreserved\n")
            before = relative_tree(root)
            provider = RecordingPublicEvidenceProvider(
                github_assets=(
                    GitHubReleaseAsset("rigorloop-adapter-codex-v0.3.5.zip", "https://observed.example/codex.zip", 731, "sha256:" + "c" * 64),
                    GitHubReleaseAsset("rigorloop-adapter-claude-v0.3.5.zip", "https://observed.example/claude.zip", 947, "sha256:" + "d" * 64),
                ),
                npm_metadata=NpmPackageMetadata(
                    package="@xiongxianfei/rigorloop", version="0.3.5",
                    tarball_url="https://observed.example/package.tgz", integrity="sha512-independent-observation",
                    shasum="e" * 40, published_at="2026-09-18T03:00:00Z",
                ),
            )
            checked = close_release_publication("v0.3.5", root=root, provider=provider, check=True)
            self.assertEqual(checked.errors, ())
            self.assertEqual(checked.changed_paths, ("docs/releases/v0.3.5/npm-publication.md",))
            self.assertEqual(relative_tree(root), before)

            result = close_release_publication("v0.3.5", root=root, provider=provider)
            errors = validate_published_release_artifacts("v0.3.5", root=root)
            npm_publication = root / "docs" / "releases" / "v0.3.5" / "npm-publication.md"
            text = npm_publication.read_text(encoding="utf-8")
            after = relative_tree(root)
            self.assertEqual(set(after), set(before))
            self.assertEqual({path for path in after if after[path] != before[path]}, {"docs/releases/v0.3.5/npm-publication.md"})
            repeated = close_release_publication("v0.3.5", root=root, provider=provider)
            self.assertEqual(repeated.errors, ())
            self.assertEqual(repeated.changed_paths, ())
            self.assertEqual(relative_tree(root), after)

        self.assertEqual(result.errors, ())
        self.assertEqual(errors, [])
        self.assertIn("Status: published", text)
        self.assertIn("version_smoke:", text)
        self.assertIn("npx @xiongxianfei/rigorloop@0.3.5 init codex", text)
        self.assertNotIn("npx -y", text)
        self.assertIn("sha256:provider-codex-tree", text)
        self.assertIn("post_publish_closeout_blocked: false", text)
        for observed in ("https://observed.example/codex.zip", "https://observed.example/claude.zip", "sha256:" + "c" * 64, "sha256:" + "d" * 64, "https://observed.example/package.tgz", "sha512-independent-observation", "2026-09-18T03:00:00Z", "sha256:provider-claude-tree"):
            self.assertIn(observed, text)

    def test_close_release_publication_fetches_github_release_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            provider = RecordingPublicEvidenceProvider()

            result = close_release_publication("v0.3.5", root=root, provider=provider)
            text = (root / "docs" / "releases" / "v0.3.5" / "npm-publication.md").read_text(encoding="utf-8")

        self.assertEqual(result.errors, ())
        self.assertEqual(provider.github_calls, ["v0.3.5"])
        self.assertIn("https://provider.example/releases/codex-provider.zip", text)
        self.assertIn("sha256:provider-codex-archive", text)

    def test_close_release_publication_fetches_npm_registry_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            provider = RecordingPublicEvidenceProvider()

            result = close_release_publication("v0.3.5", root=root, provider=provider)
            text = (root / "docs" / "releases" / "v0.3.5" / "npm-publication.md").read_text(encoding="utf-8")

        self.assertEqual(result.errors, ())
        self.assertEqual(provider.npm_calls, [("@xiongxianfei/rigorloop", "0.3.5")])
        self.assertIn("sha512-provider-integrity", text)
        self.assertIn("https://registry.provider.example/rigorloop-0.3.5.tgz", text)

    def test_close_release_publication_runs_public_version_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            provider = RecordingPublicEvidenceProvider()

            result = close_release_publication("v0.3.5", root=root, provider=provider)

        self.assertEqual(result.errors, ())
        self.assertIn("npx @xiongxianfei/rigorloop@0.3.5 version", provider.smoke_calls)

    def test_close_release_publication_runs_public_target_init_smoke_for_all_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            provider = RecordingPublicEvidenceProvider()

            result = close_release_publication("v0.3.5", root=root, provider=provider)

        self.assertEqual(result.errors, ())
        target_commands = [
            command for command in provider.smoke_calls
            if " init " in command
        ]
        self.assertEqual(
            target_commands,
            [
                "npx @xiongxianfei/rigorloop@0.3.5 init codex",
                "npx @xiongxianfei/rigorloop@0.3.5 init claude",
            ],
        )

    def test_close_release_publication_rejects_manual_public_evidence_in_default_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            public_evidence = write_public_evidence(root)
            before = relative_tree(root)

            result = close_release_publication("v0.3.5", root=root, public_evidence=public_evidence)

            after = relative_tree(root)

        self.assertTrue(any("manual public evidence" in error for error in result.errors), result.errors)
        self.assertEqual(before, after)

    def test_close_release_publication_fails_when_npm_metadata_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            before = relative_tree(root)

            result = close_release_publication(
                "v0.3.5",
                root=root,
                provider=RecordingPublicEvidenceProvider(fail_npm=True),
            )

            after = relative_tree(root)

        self.assertTrue(any("npm metadata" in error and "0.3.5" in error for error in result.errors), result.errors)
        self.assertEqual(before, after)

    def test_close_release_publication_fails_when_public_npx_smoke_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            before = relative_tree(root)
            failed_command = "npx @xiongxianfei/rigorloop@0.3.5 init codex"

            result = close_release_publication(
                "v0.3.5",
                root=root,
                provider=RecordingPublicEvidenceProvider(fail_smoke_command=failed_command),
            )

            after = relative_tree(root)

        self.assertTrue(any("codex" in error and failed_command in error for error in result.errors), result.errors)
        self.assertEqual(before, after)

    def test_close_release_publication_uses_provider_values_not_fixture_literals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            write_public_evidence(root)

            result = close_release_publication("v0.3.5", root=root, provider=RecordingPublicEvidenceProvider())
            text = (root / "docs" / "releases" / "v0.3.5" / "npm-publication.md").read_text(encoding="utf-8")

        self.assertEqual(result.errors, ())
        self.assertIn("provider-codex", text)
        self.assertNotIn("codexarchive", text)
        self.assertNotIn("sha256:codextree", text)

    def test_public_evidence_fixture_mode_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            public_evidence = write_public_evidence(root)

            result = close_release_publication(
                "v0.3.5",
                root=root,
                public_evidence=public_evidence,
                fixture_mode=True,
            )
            errors = validate_published_release_artifacts("v0.3.5", root=root)

        self.assertEqual(result.errors, ())
        self.assertEqual(errors, [])

    def test_close_release_publication_cli_check_reports_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            public_evidence = write_public_evidence(root)
            npm_publication = root / "docs" / "releases" / "v0.3.5" / "npm-publication.md"
            before = relative_tree(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "close-release-publication.py"),
                    "v0.3.5",
                    "--root",
                    str(root),
                    "--fixture-mode",
                    "--fixture-public-evidence",
                    str(public_evidence),
                    "--check",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            text = npm_publication.read_text(encoding="utf-8")
            self.assertEqual(relative_tree(root), before)

        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("docs/releases/v0.3.5/npm-publication.md", stdout := result.stdout)
        self.assertIn("Status: pending-publication", text)
        self.assertNotIn("Status: published", text)

    def test_close_release_publication_cli_rejects_fixture_evidence_without_fixture_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            public_evidence = write_public_evidence(root)
            before = relative_tree(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "close-release-publication.py"),
                    "v0.3.5",
                    "--root",
                    str(root),
                    "--fixture-public-evidence",
                    str(public_evidence),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(relative_tree(root), before)

        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn("fixture public evidence mode", output)

    def test_close_release_publication_rejects_npx_y_command_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            public_evidence = write_public_evidence(root)
            valid_before = relative_tree(root)
            control = close_release_publication("v0.3.5", root=root, public_evidence=public_evidence, fixture_mode=True, check=True)
            self.assertEqual(control.errors, ())
            self.assertEqual(relative_tree(root), valid_before)
            original = public_evidence.read_text()
            changed = original.replace("npx @xiongxianfei/rigorloop@0.3.5 init codex", "npx -y @xiongxianfei/rigorloop@0.3.5 init codex", 1)
            self.assertNotEqual(changed, original)
            public_evidence.write_text(changed)
            before = relative_tree(root)

            result = close_release_publication(
                "v0.3.5",
                root=root,
                public_evidence=public_evidence,
                fixture_mode=True,
            )
            self.assertEqual(relative_tree(root), before)

        self.assertTrue(any("codex" in error and "invalid command" in error for error in result.errors), result.errors)

    def test_validate_published_release_artifacts_rejects_raw_tree_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            control = close_release_publication("v0.3.5", root=root, provider=RecordingPublicEvidenceProvider())
            self.assertEqual(control.errors, ())
            self.assertEqual(validate_published_release_artifacts("v0.3.5", root=root), [])
            npm_publication = root / "docs" / "releases" / "v0.3.5" / "npm-publication.md"
            original = npm_publication.read_text(encoding="utf-8")
            changed = original.replace("sha256:provider-codex-tree", "provider-codex-tree", 1)
            self.assertNotEqual(changed, original)
            npm_publication.write_text(changed, encoding="utf-8")
            before = relative_tree(root)

            errors = validate_published_release_artifacts("v0.3.5", root=root)
            self.assertEqual(relative_tree(root), before)

        self.assertTrue(any("codex" in error and "sha256:" in error for error in errors), errors)

    def test_validate_published_release_artifacts_rejects_missing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            control = close_release_publication("v0.3.5", root=root, provider=RecordingPublicEvidenceProvider())
            self.assertEqual(control.errors, ())
            self.assertEqual(validate_published_release_artifacts("v0.3.5", root=root), [])
            npm_publication = root / "docs" / "releases" / "v0.3.5" / "npm-publication.md"
            text = npm_publication.read_text(encoding="utf-8")
            start = text.index("  claude:\n")
            end = text.index("\n```", start)
            npm_publication.write_text(text[:start] + text[end:], encoding="utf-8")
            before = relative_tree(root)

            errors = validate_published_release_artifacts("v0.3.5", root=root)
            self.assertEqual(relative_tree(root), before)

        self.assertTrue(any("missing target: claude" in error for error in errors), errors)

    def test_close_release_publication_does_not_rewrite_historical_release_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            historical = root / "docs" / "releases" / "v0.3.4" / "release.yaml"
            before = historical.read_text(encoding="utf-8")

            result = close_release_publication("v0.3.5", root=root, provider=RecordingPublicEvidenceProvider())
            after = historical.read_text(encoding="utf-8")

        self.assertEqual(result.errors, ())
        self.assertEqual(before, after)


class HistoricalReleaseReaderTests(unittest.TestCase):
    maxDiff = None

    def test_owned_three_target_evidence_is_readable_but_not_current_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_recorded_release(root)
            before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            with self.assertRaises(ReleaseProfileError) as caught:
                load_release_profile("v0.3.5", root=root)
            self.assertIn("unknown target: opencode", caught.exception.errors)
            self.assertFalse(validate_release_timing_evidence("v0.3.5", root=root).errors)
            self.assertEqual(validate_published_release_artifacts("v0.3.5", root=root), [])
            self.assertEqual(before, {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()})

    def test_unknown_value_rejects_in_historical_reader(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = make_recorded_release(root)
            profile.write_text(profile.read_text().replace("- opencode", "- unknown_value"))
            self.assertIn("unknown target: unknown_value", validate_release_timing_evidence("v0.3.5", root=root).errors)
