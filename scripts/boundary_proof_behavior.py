#!/usr/bin/env python3
"""Standalone hermetic behavior harness for boundary-first proof evidence.

M2 intentionally starts with only the read-only environment preflight. Later
commands are added only after this gate proves the required runtime boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Final


ENVIRONMENT_CHECK_IDS: Final[tuple[str, ...]] = (
    "runtime-identity",
    "fresh-configuration",
    "workspace-only-filesystem",
    "child-network-denial",
    "connector-subagent-denial",
    "opaque-authentication",
    "runtime-metadata",
)
_CHECK_VALUES: Final[frozenset[str]] = frozenset({"pass", "fail", "not-run"})
_VERSION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9 ._+:/()-]{0,127}$"
)


@dataclass(frozen=True)
class _ExecutableIdentity:
    device: int
    inode: int
    size: int
    modified_ns: int
    changed_ns: int
    digest: str


def _run_runtime(argv: Sequence[str]) -> tuple[int, str, str]:
    completed = subprocess.run(
        list(argv),
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
        env={
            "HOME": os.environ.get("HOME", ""),
            "PATH": os.environ.get("PATH", ""),
        },
    )
    return completed.returncode, completed.stdout, completed.stderr


def _empty_result(diagnostic_id: str) -> dict[str, object]:
    return {
        "schema_version": "boundary-environment-preflight-v1",
        "result": "environment-unavailable",
        "diagnostic_id": diagnostic_id,
        "runtime": None,
        "checks": {check_id: "not-run" for check_id in ENVIRONMENT_CHECK_IDS},
    }


def _resolved_regular_executable(command: str) -> Path | None:
    discovered = shutil.which(command)
    if discovered is None:
        return None
    try:
        resolved = Path(discovered).resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not resolved.is_file() or resolved.is_symlink():
        return None
    return resolved


def _safe_version(stdout: str) -> str | None:
    version = stdout.strip()
    if "\n" in version or "\r" in version or _VERSION_PATTERN.fullmatch(version) is None:
        return None
    return version


def _read_executable_identity(executable: Path) -> _ExecutableIdentity:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(executable, flags)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise OSError("resolved runtime executable is not a regular file")
        digest = hashlib.sha256()
        while chunk := os.read(descriptor, 1024 * 1024):
            digest.update(chunk)
        return _ExecutableIdentity(
            device=metadata.st_dev,
            inode=metadata.st_ino,
            size=metadata.st_size,
            modified_ns=metadata.st_mtime_ns,
            changed_ns=metadata.st_ctime_ns,
            digest="sha256:" + digest.hexdigest(),
        )
    finally:
        os.close(descriptor)


def _identity_or_none(executable: Path) -> _ExecutableIdentity | None:
    try:
        return _read_executable_identity(executable)
    except OSError:
        return None


def assess_environment(command: str = "codex") -> dict[str, object]:
    """Return a bounded, secret-free parent assessment of runtime feasibility."""

    result = _empty_result("runtime-executable-unavailable")
    checks = result["checks"]
    assert isinstance(checks, dict)

    executable = _resolved_regular_executable(command)
    if executable is None:
        return result

    initial_identity = _identity_or_none(executable)
    if initial_identity is None:
        result["diagnostic_id"] = "runtime-identity-unavailable"
        return result

    try:
        version_status, version_stdout, _ = _run_runtime(
            (str(executable), "--version")
        )
    except (OSError, subprocess.SubprocessError):
        return result
    if version_status != 0:
        result["diagnostic_id"] = "runtime-version-unavailable"
        return result
    version = _safe_version(version_stdout)
    if version is None:
        result["diagnostic_id"] = "runtime-version-unsafe"
        return result
    after_version_identity = _identity_or_none(executable)
    if after_version_identity is None:
        result["diagnostic_id"] = "runtime-identity-unavailable"
        return result
    if after_version_identity != initial_identity:
        result["diagnostic_id"] = "runtime-identity-changed"
        return result

    checks["runtime-identity"] = "pass"
    result["runtime"] = {
        "agent_runtime": "codex",
        "runtime_version": version,
        "runtime_executable_identity": initial_identity.digest,
        "python_implementation": platform.python_implementation().lower(),
        "python_version": (
            f"{sys.version_info.major}.{sys.version_info.minor}."
            f"{sys.version_info.micro}"
        ),
    }

    try:
        help_status, help_stdout, _ = _run_runtime(
            (str(executable), "exec", "--help")
        )
    except (OSError, subprocess.SubprocessError):
        result["diagnostic_id"] = "runtime-profile-unavailable"
        return result
    if help_status != 0:
        result["diagnostic_id"] = "runtime-profile-unavailable"
        return result
    del help_stdout
    final_identity = _identity_or_none(executable)
    if final_identity is None:
        result["diagnostic_id"] = "runtime-identity-unavailable"
        return result
    if final_identity != initial_identity:
        result["diagnostic_id"] = "runtime-identity-changed"
        return result

    # CLI option discovery is not effective-state attestation. This runtime
    # exposes no authoritative parent-readable record that binds the child
    # process to exact readable/writable roots, tool closure, network denial,
    # opaque authentication placement, and runtime/model metadata. Fail closed
    # until an approved architecture revision defines such an interface.
    for check_id in ENVIRONMENT_CHECK_IDS[1:]:
        checks[check_id] = "fail"
    if not all(value in _CHECK_VALUES for value in checks.values()):
        raise AssertionError("internal environment preflight vocabulary error")
    result["diagnostic_id"] = "effective-profile-attestation-unavailable"
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    environment = subparsers.add_parser(
        "check-environment",
        help="check the hermetic child-runtime boundary without mutating the repository",
    )
    environment.add_argument(
        "--json",
        action="store_true",
        help="emit the bounded environment receipt as canonical JSON",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "check-environment":
        raise AssertionError(f"unknown command: {args.command}")
    result = assess_environment()
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(f"{result['result']}: {result['diagnostic_id']}")
    return 0 if result["result"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
