#!/usr/bin/env python3
"""Private npm candidate setup and explicit subprocess operations."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

PACKAGE_ROOT = ROOT / "packages" / "rigorloop"
# Smoke tests pack the current package, not the release-transaction's old-version fixture.
PACKAGE_VERSION = json.loads((PACKAGE_ROOT / "package.json").read_text(encoding="utf-8"))["version"]
RELEASE_TAG = f"v{PACKAGE_VERSION}"
METADATA_FILE = f"adapter-artifacts-{RELEASE_TAG}.json"
TARGET_SKILL_ROOTS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
}


def run_command(
    args: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False, env=env)


def pack_package(destination: Path) -> Path:
    package_root = PACKAGE_ROOT
    if not (package_root / "dist/metadata" / METADATA_FILE).is_file():
        # Source checkouts do not author candidate metadata. Exercise the real
        # producer in a private fixture; prepared-candidate runs use their bytes.
        from lib.packaging.adapter_distribution import build_adapter_archives
        from lib.release.release_candidate import write_archive_metadata
        package_root = destination / "candidate-package"
        shutil.copytree(PACKAGE_ROOT, package_root, ignore=shutil.ignore_patterns("node_modules"))
        archives = destination / "archives"
        build_adapter_archives(RELEASE_TAG, archives, skills_root=ROOT / "skills")
        write_archive_metadata(ROOT, archives, RELEASE_TAG, "0" * 40, package_root)
    result = run_command(
        ["npm", "pack", "--json", "--prefix", str(package_root), "--pack-destination", str(destination), str(package_root)]
    )
    if result.returncode != 0:
        raise AssertionError(f"npm pack failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    payload = json.loads(result.stdout)
    filename = payload[0]["filename"]
    return destination / filename


def configure_npm_case(add_cleanup) -> None:
    temporary = tempfile.TemporaryDirectory(prefix="package-case-")
    add_cleanup(temporary.cleanup)
    root = Path(temporary.name)
    environment = patch.dict(os.environ, {
        "npm_config_cache": str(root / "npm"),
        "npm_config_audit": "false", "npm_config_fund": "false",
        "npm_config_update_notifier": "false",
        "RIGORLOOP_LOG_DIR": str(root / "logs"),
    })
    environment.start()
    add_cleanup(environment.stop)
