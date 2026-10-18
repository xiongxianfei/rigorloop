"""Actual tag identity and public release-gate diagnostics."""

from __future__ import annotations

import sys

from pathlib import Path

import tempfile

import unittest

import os

import subprocess

ROOT = Path(__file__).resolve().parents[3]

sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import validate_trusted_release_tag_identity

from release_fixture_helpers import (make_tag_identity_repo)

class TrustedReleaseTagIdentityTests(unittest.TestCase):
    maxDiff = None

    def test_accepts_matching_lightweight_and_annotated_tags(self) -> None:
        for annotated in (False, True):
            with self.subTest(annotated=annotated), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                commit = make_tag_identity_repo(root)
                command = ["git", "-C", str(root), "tag"]
                if annotated:
                    command.extend(["-a", "v0.4.0", "-m", "v0.4.0"])
                else:
                    command.append("v0.4.0")
                subprocess.run(command, check=True)

                errors = validate_trusted_release_tag_identity(
                    "v0.4.0", "v0.4.0", commit, root=root
                )

            self.assertEqual(errors, [])

    def test_rejects_tag_that_does_not_point_at_trusted_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trusted_commit = make_tag_identity_repo(root)
            (root / "README.md").write_text("rewritten\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "commit", "-qam", "later"], check=True)
            subprocess.run(["git", "-C", str(root), "tag", "v0.4.0"], check=True)
            subprocess.run(["git", "-C", str(root), "checkout", "-q", trusted_commit], check=True)

            errors = validate_trusted_release_tag_identity(
                "v0.4.0", "v0.4.0", trusted_commit, root=root
            )

        self.assertTrue(any("hosted tag" in error for error in errors), errors)
