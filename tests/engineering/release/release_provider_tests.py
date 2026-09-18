"""Public filesystem observations with controlled npx transport and independent hashes."""

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_execution import ExecutionError
from lib.release.release_provider import NetworkPublisher


V1 = "rigorloop-tree-hash-v1"
V2 = "rigorloop-tree-hash-v2"
# Literal normalized bytes and orders are independent of the production helpers.
NORMALIZED = {
    "Z.md": b"Z\nkeep  \n", "_.md": b"punctuation\n", "a.md": b"A\n",
    "binary.bin": b"\xef\xbb\xbf\x00\r\n\xff", "é.md": b"accent\n",
}
ORDER = {V1: ("_.md", "a.md", "binary.bin", "Z.md", "é.md"),
         V2: ("Z.md", "_.md", "a.md", "binary.bin", "é.md")}


def expected_tree(algorithm):
    manifest = (algorithm + "\n").encode() + b"".join(
        name.encode() + b"\t" + hashlib.sha256(NORMALIZED[name]).hexdigest().encode() + b"\n"
        for name in ORDER[algorithm]
    )
    return hashlib.sha256(manifest).hexdigest()


def public_metadata(target, algorithm=V1):
    artifact = {
        "adapter": target, "archive": f"rigorloop-adapter-{target}-v0.5.1.zip",
        "url": f"https://github.com/xiongxianfei/rigorloop/releases/download/v0.5.1/rigorloop-adapter-{target}-v0.5.1.zip",
        "sha256": "a" * 64, "size_bytes": 900,
        "install_root": ".agents/skills" if target == "codex" else ".claude/skills",
        "tree_sha256": expected_tree(algorithm), "file_count": len(NORMALIZED),
        "tree_hash_algorithm": algorithm,
    }
    return {"schema_version": 1,
            "release": {"version": "v0.5.1", "release_tag": "v0.5.1", "source_repository": "xiongxianfei/rigorloop",
                        "source_commit": "b" * 40, "published_at": "2026-09-18T03:00:00Z"},
            "metadata": {"url": "https://github.com/xiongxianfei/rigorloop/releases/download/v0.5.1/archive-proof-v0.5.1.json", "sha256": "c" * 64},
            "validation": {"command": "controlled archive fixture", "result": "pass"},
            "artifacts": [artifact]}


class ReleasePublicTreeIdentityTests(unittest.TestCase):
    def observe_private_tree(self, workspace, target="codex", unsafe=None):
        """Substitute only npx transport; the real provider inspects actual files."""
        command = f"npx @xiongxianfei/rigorloop@0.5.1 init {target}"
        relative = ".agents/skills" if target == "codex" else ".claude/skills"
        provider = NetworkPublisher()
        outside = workspace / "outside"
        outside.mkdir()
        outside_file = outside / "private.md"
        outside_file.write_bytes(b"outside bytes must remain unchanged\r\n")
        cwd = workspace / "installed"
        cwd.mkdir()

        def npx_transport(args, **kwargs):
            self.assertEqual(args, command.split())
            self.assertEqual(kwargs["cwd"], cwd)
            self.assertEqual(kwargs["env"]["npm_config_registry"], "https://registry.npmjs.org/")
            self.assertTrue(Path(kwargs["env"]["npm_config_cache"]).is_dir())
            install_root = cwd / relative
            install_root.parent.mkdir(parents=True)
            if unsafe == "root-link":
                install_root.symlink_to(outside, target_is_directory=True)
            else:
                install_root.mkdir()
                for name in reversed(tuple(NORMALIZED)):
                    content = b"\xef\xbb\xbfZ\r\nkeep  \r" if name == "Z.md" else NORMALIZED[name]
                    (install_root / name).write_bytes(content)
                (install_root / "empty").mkdir()
                if unsafe == "member-link":
                    (install_root / "linked.md").symlink_to(outside_file)
            return subprocess.CompletedProcess(args, 0, "controlled public init completed\n", "")

        with patch("lib.release.release_provider.subprocess.run", side_effect=npx_transport) as transport:
            result = provider.run_public_npx_smoke(command=command, cwd=cwd)
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(outside_file.read_bytes(), b"outside bytes must remain unchanged\r\n")
        return provider, result

    def test_public_tree_observation_selects_exact_declared_hash_algorithm(self):
        for algorithm, target in ((V1, "codex"), (None, "codex"), (V2, "codex"), (V2, "claude")):
            with self.subTest(algorithm=algorithm, target=target), tempfile.TemporaryDirectory() as tmp:
                workspace = Path(tmp)
                provider, result = self.observe_private_tree(workspace, target)
                self.assertEqual(result.exit_code, 0)
                metadata = public_metadata(target, algorithm or V1)
                if algorithm is None:
                    del metadata["artifacts"][0]["tree_hash_algorithm"]
                path = workspace / "adapter-artifacts-v0.5.1.json"
                path.write_text(json.dumps(metadata))
                before = path.read_bytes()
                provider.verify_smoke_identity({"tag": "v0.5.1"}, workspace)
                self.assertEqual(path.read_bytes(), before)

    def test_public_tree_verification_never_falls_back_to_another_algorithm(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            provider, result = self.observe_private_tree(workspace)
            self.assertEqual(result.exit_code, 0)
            path = workspace / "adapter-artifacts-v0.5.1.json"
            metadata = public_metadata("codex", V1)
            path.write_text(json.dumps(metadata))
            provider.verify_smoke_identity({"tag": "v0.5.1"}, workspace)
            self.assertNotEqual(expected_tree(V1), expected_tree(V2))
            metadata["artifacts"][0]["tree_hash_algorithm"] = V2
            path.write_text(json.dumps(metadata))
            before = path.read_bytes()
            with self.assertRaisesRegex(ExecutionError, "public installed tree differs"):
                provider.verify_smoke_identity({"tag": "v0.5.1"}, workspace)
            self.assertEqual(path.read_bytes(), before)

    def test_public_tree_unknown_algorithm_rejects_before_root_consistency(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            provider, result = self.observe_private_tree(workspace)
            self.assertEqual(result.exit_code, 0)
            path = workspace / "adapter-artifacts-v0.5.1.json"
            valid = public_metadata("codex")
            path.write_text(json.dumps(valid))
            provider.verify_smoke_identity({"tag": "v0.5.1"}, workspace)
            for unknown in ("", "unknown_value", None):
                with self.subTest(algorithm=unknown):
                    metadata = copy.deepcopy(valid)
                    metadata["artifacts"][0]["install_root"] = "missing/root"
                    metadata["artifacts"].append(dict(valid["artifacts"][0], tree_hash_algorithm=unknown))
                    path.write_text(json.dumps(metadata))
                    before = path.read_bytes()
                    with self.assertRaisesRegex(ExecutionError, "unknown tree hash algorithm"):
                        provider.verify_smoke_identity({"tag": "v0.5.1"}, workspace)
                    self.assertEqual(path.read_bytes(), before)

    def test_public_smoke_rejects_symlinked_roots_and_members(self):
        for unsafe in ("root-link", "member-link"):
            with self.subTest(unsafe=unsafe), tempfile.TemporaryDirectory() as tmp:
                _, result = self.observe_private_tree(Path(tmp), unsafe=unsafe)
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(result.summary, "public init codex failed")
