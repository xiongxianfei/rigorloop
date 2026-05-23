#!/usr/bin/env python3
"""Validate lifecycle state for top-level workflow artifacts."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

from artifact_lifecycle_validation import ValidationFinding, ValidationInputError, validate_repository
import validation_cache


ROOT = Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate lifecycle state for top-level workflow artifacts."
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=("explicit-paths", "local", "pr-ci", "push-main-ci"),
        help="How to determine validation scope.",
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Repo-relative path to validate in explicit-paths mode. May be repeated.",
    )
    parser.add_argument("--base", help="Base SHA for pr-ci mode.")
    parser.add_argument("--head", help="Head SHA for pr-ci mode.")
    parser.add_argument("--before", help="Before SHA for push-main-ci mode.")
    parser.add_argument("--after", help="After SHA for push-main-ci mode.")
    parser.add_argument(
        "--pr-body-file",
        help="Optional repo-relative draft PR body file whose artifact references join scope.",
    )
    parser.add_argument(
        "--use-validation-cache",
        action="store_true",
        help="Use first-slice local cache for explicit-path lifecycle validation.",
    )
    parser.add_argument(
        "--validation-cache-dir",
        default=".rigorloop-validation-cache",
        help="Local untracked validation cache directory.",
    )
    parser.add_argument(
        "--validation-cache-change-id",
        help="Change ID for change-local cache eligibility.",
    )
    parser.add_argument(
        "--validation-cache-context",
        choices=("inner-loop", "closeout"),
        default="inner-loop",
        help="Cache context; closeout always forces actual validation.",
    )
    parser.add_argument(
        "--validation-cache-current-stage",
        default="local-validation",
        help="Stage name to store with a passing local cache record.",
    )
    parser.add_argument(
        "--validation-cache-current-evidence",
        default="docs/plan.md#validation",
        help="Repository-relative evidence reference to store with a passing local cache record.",
    )
    parser.add_argument(
        "--validation-cache-evidence-file",
        help="Optional change-local validation-cache-evidence.yaml to write on a cache hit.",
    )
    parser.add_argument(
        "--validation-cache-hit-id",
        default="cache-hit-001",
        help="Stable cache-hit ID to write when formal cache-hit evidence is requested.",
    )
    parser.add_argument(
        "--validation-cache-ttl-seconds",
        type=float,
        help="Optional TTL for otherwise valid local cache entries.",
    )
    return parser


def format_finding(finding: ValidationFinding) -> str:
    path = finding.path.relative_to(ROOT).as_posix()
    prefix = "BLOCK" if finding.severity == "block" else "WARN"
    detail = f"{prefix} {path}"
    if finding.artifact_class:
        detail += f" [{finding.artifact_class}"
        if finding.status:
            detail += f", status={finding.status}"
        detail += "]"
    detail += f": {finding.message}"
    return detail


def semantic_argv(args: argparse.Namespace) -> list[str]:
    argv = ["python", "scripts/validate-artifact-lifecycle.py", "--mode", args.mode]
    for path in args.path:
        argv.extend(["--path", path])
    if args.base:
        argv.extend(["--base", args.base])
    if args.head:
        argv.extend(["--head", args.head])
    if args.before:
        argv.extend(["--before", args.before])
    if args.after:
        argv.extend(["--after", args.after])
    if args.pr_body_file:
        argv.extend(["--pr-body-file", args.pr_body_file])
    return argv


def cache_context_for(
    args: argparse.Namespace,
    identity: validation_cache.LifecycleCacheIdentity,
) -> validation_cache.LocalCacheContext:
    return validation_cache.LocalCacheContext(
        cache_key=identity.cache_key,
        validator_id=identity.validator_id,
        command_family=identity.command_family,
        repository_id=local_repository_id(ROOT),
        branch=current_branch(ROOT),
        worktree_id=ROOT.resolve().as_posix(),
        change_id=args.validation_cache_change_id or infer_change_id(args.path),
        command_hash=identity.normalized_command.command_hash,
        input_surface_hash=identity.input_surface.manifest_hash,
        implementation_hash=identity.implementation.manifest_hash,
        policy_hash=identity.policy.manifest_hash,
        now=time.time(),
        ttl_seconds=args.validation_cache_ttl_seconds,
    )


def local_repository_id(root: Path) -> str:
    encoded = root.resolve().as_posix().encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def current_branch(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return "unknown"
    return result.stdout.strip() or "detached"


def infer_change_id(paths: list[str]) -> str:
    prefix = "docs/changes/"
    found: set[str] = set()
    for path in paths:
        normalized = path.replace("\\", "/")
        if normalized.startswith(prefix):
            remainder = normalized[len(prefix) :]
            change_id = remainder.split("/", 1)[0]
            if change_id:
                found.add(change_id)
    if len(found) == 1:
        return next(iter(found))
    return "no-change-id"


def maybe_cache_hit(args: argparse.Namespace) -> tuple[validation_cache.LifecycleCacheIdentity, validation_cache.LocalCacheContext] | None:
    if (
        not args.use_validation_cache
        or args.mode != "explicit-paths"
        or args.validation_cache_context != "inner-loop"
        or os.environ.get("CI")
    ):
        return None
    try:
        identity = validation_cache.build_lifecycle_cache_identity(ROOT, semantic_argv(args))
        context = cache_context_for(args, identity)
    except validation_cache.CacheIdentityError as exc:
        print(f"validation cache disabled: {exc}", file=sys.stderr)
        return None

    lookup = validation_cache.find_local_cache_hit(args.validation_cache_dir, context)
    if lookup.record is None:
        return identity, context

    short_key = lookup.record.cache_key[:19] if lookup.record.cache_key else identity.cache_key[:19]
    if args.validation_cache_evidence_file:
        try:
            validation_cache.write_cache_hit_evidence(
                repo_root=ROOT,
                evidence_file=args.validation_cache_evidence_file,
                change_id=context.change_id,
                cache_hit_id=args.validation_cache_hit_id,
                identity=identity,
                record=lookup.record,
            )
        except validation_cache.CacheIdentityError as exc:
            print(f"validation cache evidence rejected: {exc}", file=sys.stderr)
            return None
    print(
        "[CACHE HIT] artifact-lifecycle: input surface unchanged since "
        f"{lookup.record.prior_event_stage or 'prior local pass'}; "
        f"prior result pass; key {short_key}"
    )
    raise SystemExit(0)


def record_passing_cache_entry(
    args: argparse.Namespace,
    cache_state: tuple[validation_cache.LifecycleCacheIdentity, validation_cache.LocalCacheContext] | None,
) -> None:
    if cache_state is None:
        return
    identity, context = cache_state
    record = validation_cache.make_local_cache_record(
        identity=identity,
        context=context,
        prior_event_stage=args.validation_cache_current_stage,
        prior_event_evidence=args.validation_cache_current_evidence,
    )
    validation_cache.store_local_cache_record(args.validation_cache_dir, record)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cache_state = maybe_cache_hit(args)

    try:
        result = validate_repository(
            ROOT,
            mode=args.mode,
            paths=args.path,
            base=args.base,
            head=args.head,
            before=args.before,
            after=args.after,
            pr_body_file=args.pr_body_file,
        )
    except ValidationInputError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or str(exc), file=sys.stderr)
        return 2

    for finding in result.warning_findings:
        print(format_finding(finding))
    for finding in result.blocking_findings:
        print(format_finding(finding), file=sys.stderr)

    if result.blocking_findings:
        return 1

    print(f"validated {len(result.checked_artifacts)} artifact files in {args.mode} mode")
    record_passing_cache_entry(args, cache_state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
