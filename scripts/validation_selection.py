#!/usr/bin/env python3
"""Validation selector domain model and path classification."""

from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any


DEFAULT_ADAPTER_VERSION = "0.1.1"
STATUSES = frozenset({"ok", "blocked", "fallback", "error"})
EXIT_CODES = {"ok": 0, "blocked": 2, "fallback": 3, "error": 4}


@dataclass(frozen=True)
class CheckCatalogEntry:
    id: str
    command_template: str
    category: str


CHECK_CATALOG: dict[str, CheckCatalogEntry] = {
    "skills.validate": CheckCatalogEntry(
        "skills.validate",
        "python scripts/validate-skills.py",
        "skills",
    ),
    "skills.regression": CheckCatalogEntry(
        "skills.regression",
        "python scripts/test-skill-validator.py",
        "skills",
    ),
    "skills.drift": CheckCatalogEntry(
        "skills.drift",
        "python scripts/build-skills.py --check",
        "skills",
    ),
    "adapters.regression": CheckCatalogEntry(
        "adapters.regression",
        "python scripts/test-adapter-distribution.py",
        "adapters",
    ),
    "adapters.drift": CheckCatalogEntry(
        "adapters.drift",
        "python scripts/build-adapters.py --version <adapter-version> --check",
        "adapters",
    ),
    "adapters.validate": CheckCatalogEntry(
        "adapters.validate",
        "python scripts/validate-adapters.py --version <adapter-version>",
        "adapters",
    ),
    "review_artifacts.regression": CheckCatalogEntry(
        "review_artifacts.regression",
        "python scripts/test-review-artifact-validator.py",
        "review-artifacts",
    ),
    "review_artifacts.validate": CheckCatalogEntry(
        "review_artifacts.validate",
        "python scripts/validate-review-artifacts.py <change-root>...",
        "review-artifacts",
    ),
    "artifact_lifecycle.regression": CheckCatalogEntry(
        "artifact_lifecycle.regression",
        "python scripts/test-artifact-lifecycle-validator.py",
        "lifecycle",
    ),
    "artifact_lifecycle.validate": CheckCatalogEntry(
        "artifact_lifecycle.validate",
        "python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <path>...",
        "lifecycle",
    ),
    "change_metadata.regression": CheckCatalogEntry(
        "change_metadata.regression",
        "python scripts/test-change-metadata-validator.py",
        "change-metadata",
    ),
    "change_metadata.validate": CheckCatalogEntry(
        "change_metadata.validate",
        "python scripts/validate-change-metadata.py <change-yaml>...",
        "change-metadata",
    ),
    "release.validate": CheckCatalogEntry(
        "release.validate",
        "python scripts/validate-release.py --version <version>",
        "release",
    ),
    "selector.regression": CheckCatalogEntry(
        "selector.regression",
        "python scripts/test-select-validation.py",
        "selector",
    ),
    "broad_smoke.repo": CheckCatalogEntry(
        "broad_smoke.repo",
        "bash scripts/ci.sh --mode broad-smoke",
        "broad-smoke",
    ),
}


@dataclass(frozen=True)
class SelectionRequest:
    mode: str
    paths: tuple[str, ...] = ()
    base: str | None = None
    head: str | None = None
    release_version: str | None = None
    broad_smoke: bool = False
    trigger_context_paths: tuple[str, ...] = ()
    repo_root: Path | str = Path.cwd()
    adapter_version: str = DEFAULT_ADAPTER_VERSION


@dataclass(frozen=True)
class NormalizedPath:
    ok: bool
    path: str | None = None
    blocking_code: str | None = None
    message: str | None = None


@dataclass(frozen=True)
class PathClassification:
    path: str
    category: str | None


@dataclass
class SelectedCheckDraft:
    id: str
    reasons: list[str] = field(default_factory=list)
    paths: set[str] = field(default_factory=set)
    affected_roots: set[str] = field(default_factory=set)
    versions: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class SelectionResult:
    mode: str
    status: str
    changed_paths: tuple[str, ...]
    classified_paths: tuple[dict[str, str], ...]
    unclassified_paths: tuple[str, ...]
    selected_checks: tuple[dict[str, Any], ...]
    affected_roots: tuple[str, ...]
    broad_smoke_required: bool
    blocking_results: tuple[dict[str, str], ...]
    rationale: tuple[str, ...]
    broad_smoke: dict[str, Any]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "status": self.status,
            "changed_paths": list(self.changed_paths),
            "classified_paths": list(self.classified_paths),
            "unclassified_paths": list(self.unclassified_paths),
            "selected_checks": list(self.selected_checks),
            "affected_roots": list(self.affected_roots),
            "broad_smoke_required": self.broad_smoke_required,
            "broad_smoke": self.broad_smoke,
            "blocking_results": list(self.blocking_results),
            "rationale": list(self.rationale),
        }


def exit_code_for_status(status: str) -> int:
    return EXIT_CODES.get(status, 4)


def selection_result_to_json(result: SelectionResult) -> str:
    return json.dumps(result.to_json_dict(), indent=2, sort_keys=False) + "\n"


def error_result(mode: str, message: str, *, code: str = "invalid-invocation") -> SelectionResult:
    return _build_result(
        mode=mode or "unknown",
        changed_paths=[],
        classified_paths=[],
        unclassified_paths=[],
        selected={},
        affected_roots=set(),
        broad_smoke_sources=[],
        blocking_results=[{"code": code, "message": message}],
        status="error",
    )


def normalize_path(raw_path: str, *, repo_root: Path | str) -> NormalizedPath:
    root = Path(repo_root).resolve()
    raw = raw_path.strip()
    if not raw:
        return NormalizedPath(False, blocking_code="empty-path", message="path must not be empty")

    candidate = Path(raw)
    if ".." in candidate.parts:
        return NormalizedPath(
            False,
            blocking_code="path-traversal",
            message="path traversal is not allowed",
        )

    resolved = candidate.resolve(strict=False) if candidate.is_absolute() else (root / candidate).resolve(strict=False)
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return NormalizedPath(
            False,
            blocking_code="outside-repository-path",
            message="path is outside the repository",
        )

    return NormalizedPath(True, path=PurePosixPath(relative.as_posix()).as_posix())


def classify_path(path: str) -> PathClassification:
    category = _path_category(path)
    return PathClassification(path=path, category=category)


def catalog_command(
    check_id: str,
    *,
    paths: tuple[str, ...] = (),
    affected_roots: tuple[str, ...] = (),
    versions: tuple[str, ...] = (),
    adapter_version: str = DEFAULT_ADAPTER_VERSION,
) -> str:
    if check_id not in CHECK_CATALOG:
        raise ValueError(f"unknown check ID: {check_id}")

    if check_id == "adapters.drift":
        return _join("python", "scripts/build-adapters.py", "--version", adapter_version, "--check")
    if check_id == "adapters.validate":
        return _join("python", "scripts/validate-adapters.py", "--version", adapter_version)
    if check_id == "review_artifacts.validate":
        if not affected_roots:
            raise ValueError("review_artifacts.validate requires at least one change root")
        return _join("python", "scripts/validate-review-artifacts.py", *affected_roots)
    if check_id == "artifact_lifecycle.validate":
        if not paths:
            raise ValueError("artifact_lifecycle.validate requires at least one path")
        args = ["python", "scripts/validate-artifact-lifecycle.py", "--mode", "explicit-paths"]
        for path in paths:
            args.extend(["--path", path])
        return _join(*args)
    if check_id == "change_metadata.validate":
        if not paths:
            raise ValueError("change_metadata.validate requires at least one change.yaml path")
        return _join("python", "scripts/validate-change-metadata.py", *paths)
    if check_id == "release.validate":
        if len(versions) != 1:
            raise ValueError("release.validate requires exactly one release version")
        return _join("python", "scripts/validate-release.py", "--version", versions[0])

    return CHECK_CATALOG[check_id].command_template


def select_validation(request: SelectionRequest) -> SelectionResult:
    repo_root = Path(request.repo_root).resolve()
    invalid = _validate_request(request)
    if invalid:
        return error_result(request.mode, invalid)

    changed_paths, normalization_blocks = _resolve_changed_paths(request, repo_root=repo_root)
    selected: dict[str, SelectedCheckDraft] = {}
    classified_paths: list[dict[str, str]] = []
    unclassified_paths: list[str] = []
    affected_roots: set[str] = set()
    blocking_results: list[dict[str, str]] = []
    blocking_results.extend(normalization_blocks)

    release_versions: set[str] = set()
    for path in changed_paths:
        classification = classify_path(path)
        if classification.category is None:
            unclassified_paths.append(path)
            blocking_results.append(
                {
                    "code": "unclassified-path",
                    "path": path,
                    "message": "changed path is not classified by the v1 selector",
                }
            )
            continue

        classified_paths.append({"path": path, "category": classification.category})
        _apply_path_selection(
            path,
            classification.category,
            changed_paths=changed_paths,
            selected=selected,
            affected_roots=affected_roots,
            blocking_results=blocking_results,
            release_versions=release_versions,
        )

    broad_smoke_sources = _broad_smoke_sources(request, changed_paths=changed_paths, repo_root=repo_root)
    broad_smoke_required = bool(broad_smoke_sources)
    if broad_smoke_required:
        _add_check(selected, "broad_smoke.repo", "Broad smoke is required by an authoritative source.")

    if not changed_paths and not broad_smoke_required:
        blocking_results.append(
            {
                "code": "empty-changed-paths",
                "message": "no changed paths were provided or discovered",
            }
        )

    status = "blocked" if blocking_results else "ok"
    return _build_result(
        mode=request.mode,
        changed_paths=changed_paths,
        classified_paths=classified_paths,
        unclassified_paths=unclassified_paths,
        selected=selected,
        affected_roots=affected_roots,
        broad_smoke_sources=broad_smoke_sources,
        blocking_results=blocking_results,
        status=status,
        adapter_version=request.adapter_version,
    )


def _validate_request(request: SelectionRequest) -> str | None:
    if request.mode not in {"local", "explicit", "pr", "main", "release"}:
        return "unsupported or missing --mode"
    if request.mode == "explicit" and not request.paths:
        return "--mode explicit requires at least one --path"
    if request.mode in {"pr", "main"} and (not request.base or not request.head):
        return f"--mode {request.mode} requires --base and --head"
    if request.mode == "release" and not request.release_version:
        return "--mode release requires --release-version"
    return None


def _resolve_changed_paths(
    request: SelectionRequest,
    *,
    repo_root: Path,
) -> tuple[list[str], list[dict[str, str]]]:
    raw_paths: list[str]
    blocks: list[dict[str, str]] = []

    if request.mode in {"explicit", "local"} and request.paths:
        raw_paths = list(request.paths)
    elif request.mode == "local":
        raw_paths = _git_local_changed_paths(repo_root)
    elif request.mode in {"pr", "main"}:
        raw_paths = _git_range_changed_paths(repo_root, request.base or "", request.head or "")
    elif request.mode == "release":
        raw_paths = [f"docs/releases/{request.release_version}/release.yaml"]
    else:
        raw_paths = []

    normalized_paths: list[str] = []
    seen: set[str] = set()
    for raw_path in raw_paths:
        normalized = normalize_path(raw_path, repo_root=repo_root)
        if not normalized.ok:
            blocks.append(
                {
                    "code": normalized.blocking_code or "invalid-path",
                    "path": _safe_path_label(raw_path),
                    "message": normalized.message or "invalid path",
                }
            )
            continue
        assert normalized.path is not None
        if normalized.path not in seen:
            normalized_paths.append(normalized.path)
            seen.add(normalized.path)
    return normalized_paths, blocks


def _git_local_changed_paths(repo_root: Path) -> list[str]:
    tracked = _git_lines(repo_root, "diff", "--name-only", "--diff-filter=ACMRT", "HEAD", "--", ".")
    staged = _git_lines(repo_root, "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "--", ".")
    untracked = _git_lines(repo_root, "ls-files", "--others", "--exclude-standard")
    return _dedupe([*tracked, *staged, *untracked])


def _git_range_changed_paths(repo_root: Path, base: str, head: str) -> list[str]:
    return _git_lines(repo_root, "diff", "--name-only", "--diff-filter=ACMRT", base, head, "--", ".")


def _git_lines(repo_root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _apply_path_selection(
    path: str,
    category: str,
    *,
    changed_paths: tuple[str, ...],
    selected: dict[str, SelectedCheckDraft],
    affected_roots: set[str],
    blocking_results: list[dict[str, str]],
    release_versions: set[str],
) -> None:
    if category == "skills":
        root = _skill_root(path)
        if root:
            affected_roots.add(root)
        _add_check(selected, "skills.validate", "Changed canonical skill source requires skill validation.")
        _add_check(selected, "skills.regression", "Changed canonical skill source requires skill regression fixtures.")
        _add_check(selected, "skills.drift", "Changed canonical skill source requires generated skill drift check.")
        _add_check(selected, "adapters.drift", "Public adapter output can be affected by canonical skill changes.")
        return

    if category == "generated-skills":
        _add_check(selected, "skills.drift", "Generated Codex skill output must match canonical skills.")
        return

    if category in {"generated-adapters", "adapters"}:
        _add_check(selected, "adapters.regression", "Adapter output or generator change requires adapter regression fixtures.")
        _add_check(selected, "adapters.drift", "Adapter output or generator change requires adapter drift check.")
        _add_check(selected, "adapters.validate", "Adapter output or generator change requires adapter validation.")
        return

    if category == "review-artifacts":
        root = _change_root(path)
        if root:
            affected_roots.add(root)
            _add_check(
                selected,
                "review_artifacts.validate",
                "Changed review artifact requires review artifact structure validation.",
                affected_root=root,
            )
        return

    if category == "change-metadata":
        root = _change_root(path)
        if root:
            affected_roots.add(root)
        _add_check(
            selected,
            "change_metadata.validate",
            "Changed change metadata requires change metadata validation.",
            path=path,
        )
        _add_check(selected, "change_metadata.regression", "Changed change metadata requires validator regression fixtures.")
        return

    if category == "lifecycle":
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed lifecycle artifact requires artifact lifecycle validation.",
            path=path,
        )
        return

    if category == "change-local-lifecycle":
        governing_change_yaml = _change_root_change_yaml(path)
        if governing_change_yaml:
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed change-local lifecycle artifact requires its governing change metadata for lifecycle validation.",
                path=governing_change_yaml,
            )
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed change-local lifecycle artifact requires artifact lifecycle validation.",
            path=path,
        )
        return

    if category == "plan-index":
        context_paths = _plan_index_context_paths(changed_paths)
        if not context_paths:
            blocking_results.append(
                {
                    "code": "manual-routing-required",
                    "path": path,
                    "message": "changed plan index requires an active plan or change metadata context",
                }
            )
            return
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed plan index requires artifact lifecycle validation with the related plan context.",
            path=path,
        )
        for context_path in context_paths:
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed plan index requires artifact lifecycle validation with the related plan context.",
                path=context_path,
            )
        return

    if category == "release":
        version = _release_version_from_path(path)
        if not version:
            blocking_results.append(
                {
                    "code": "release-version-required",
                    "path": path,
                    "message": "release version could not be inferred from release path",
                }
            )
            return
        release_versions.add(version)
        _add_check(selected, "release.validate", "Changed release artifact requires release validation.", version=version)
        return

    if category in {"selector", "ci-wrapper"}:
        reason = (
            "Changed CI wrapper requires selector and wrapper regression fixtures."
            if category == "ci-wrapper"
            else "Changed selector code requires selector regression fixtures."
        )
        _add_check(selected, "selector.regression", reason)
        return

    if category == "validator-review-artifacts":
        _add_check(
            selected,
            "review_artifacts.regression",
            "Changed review artifact validator requires review artifact regression fixtures.",
        )
        return

    if category == "validator-artifact-lifecycle":
        _add_check(
            selected,
            "artifact_lifecycle.regression",
            "Changed artifact lifecycle validator requires lifecycle regression fixtures.",
        )
        return

    if category == "validator-change-metadata":
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed change metadata validator requires change metadata regression fixtures.",
        )
        return

    if category == "validator-skills":
        _add_check(selected, "skills.regression", "Changed skill validator requires skill regression fixtures.")
        return

    if category in {"ci-workflow", "workflow-guidance", "governance", "templates"}:
        _add_check(
            selected,
            "selector.regression",
            f"Changed {category} path requires selector and workflow routing regression fixtures.",
        )
        return

    if category == "schemas":
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed schema path requires change metadata regression fixtures.",
        )
        return

    if category == "release-script":
        _add_check(
            selected,
            "adapters.regression",
            "Changed release script requires release and adapter distribution regression fixtures.",
        )
        return

    blocking_results.append(
        {
            "code": "manual-routing-required",
            "path": path,
            "message": f"changed {category} path has no deterministic v1 selector check",
        }
    )


def _add_check(
    selected: dict[str, SelectedCheckDraft],
    check_id: str,
    reason: str,
    *,
    path: str | None = None,
    affected_root: str | None = None,
    version: str | None = None,
) -> None:
    draft = selected.setdefault(check_id, SelectedCheckDraft(id=check_id))
    if reason not in draft.reasons:
        draft.reasons.append(reason)
    if path:
        draft.paths.add(path)
    if affected_root:
        draft.affected_roots.add(affected_root)
    if version:
        draft.versions.add(version)


def _build_result(
    *,
    mode: str,
    changed_paths: list[str],
    classified_paths: list[dict[str, str]],
    unclassified_paths: list[str],
    selected: dict[str, SelectedCheckDraft],
    affected_roots: set[str],
    broad_smoke_sources: list[dict[str, str]],
    blocking_results: list[dict[str, str]],
    status: str,
    adapter_version: str = DEFAULT_ADAPTER_VERSION,
) -> SelectionResult:
    selected_checks: list[dict[str, Any]] = []
    build_errors: list[dict[str, str]] = []
    for check_id in CHECK_CATALOG:
        draft = selected.get(check_id)
        if draft is None:
            continue
        paths = tuple(sorted(draft.paths))
        roots = tuple(sorted(draft.affected_roots))
        versions = tuple(sorted(draft.versions))
        try:
            command = catalog_command(
                check_id,
                paths=paths,
                affected_roots=roots,
                versions=versions,
                adapter_version=adapter_version,
            )
        except ValueError as exc:
            build_errors.append(
                {
                    "code": "command-substitution-error",
                    "message": str(exc),
                }
            )
            continue
        entry: dict[str, Any] = {
            "id": check_id,
            "command": command,
            "reason": " ".join(draft.reasons),
        }
        if paths:
            entry["paths"] = list(paths)
        if roots:
            entry["affected_roots"] = list(roots)
        if versions:
            entry["versions"] = list(versions)
        selected_checks.append(entry)

    combined_blocking = [*blocking_results, *build_errors]
    final_status = "error" if build_errors else status
    return SelectionResult(
        mode=mode,
        status=final_status,
        changed_paths=tuple(changed_paths),
        classified_paths=tuple(classified_paths),
        unclassified_paths=tuple(unclassified_paths),
        selected_checks=tuple(selected_checks),
        affected_roots=tuple(sorted(affected_roots)),
        broad_smoke_required=bool(broad_smoke_sources),
        broad_smoke={
            "required": bool(broad_smoke_sources),
            "sources": list(broad_smoke_sources),
        },
        blocking_results=tuple(combined_blocking),
        rationale=tuple(entry["reason"] for entry in selected_checks),
    )


def _path_category(path: str) -> str | None:
    parts = path.split("/")
    if path.startswith("skills/"):
        return "skills"
    if path.startswith(".codex/skills/"):
        return "generated-skills"
    if path.startswith("dist/adapters/"):
        return "generated-adapters"
    if path.startswith("scripts/adapter_templates/") or path in {
        "scripts/adapter_distribution.py",
        "scripts/build-adapters.py",
        "scripts/validate-adapters.py",
    }:
        return "adapters"
    if path in {"scripts/select-validation.py", "scripts/validation_selection.py", "scripts/test-select-validation.py"}:
        return "selector"
    if path == "scripts/ci.sh":
        return "ci-wrapper"
    if path == ".github/workflows/ci.yml":
        return "ci-workflow"
    if path in {"scripts/validate-review-artifacts.py", "scripts/review_artifact_validation.py", "scripts/test-review-artifact-validator.py"}:
        return "validator-review-artifacts"
    if path in {
        "scripts/validate-artifact-lifecycle.py",
        "scripts/artifact_lifecycle_validation.py",
        "scripts/artifact_lifecycle_contracts.py",
        "scripts/test-artifact-lifecycle-validator.py",
    }:
        return "validator-artifact-lifecycle"
    if path in {"scripts/validate-change-metadata.py", "scripts/test-change-metadata-validator.py"}:
        return "validator-change-metadata"
    if path in {"scripts/validate-skills.py", "scripts/skill_validation.py", "scripts/test-skill-validator.py"}:
        return "validator-skills"
    if path.startswith("docs/changes/") and len(parts) >= 4:
        if parts[3] == "change.yaml":
            return "change-metadata"
        if parts[3] in {"review-log.md", "review-resolution.md"} or parts[3] == "reviews":
            return "review-artifacts"
        if parts[3] == "explain-change.md":
            return "change-local-lifecycle"
        return "change-local-unsupported"
    if path == "docs/plan.md":
        return "plan-index"
    if _is_lifecycle_path(path):
        return "lifecycle"
    if path.startswith("docs/releases/"):
        return "release"
    if path == "docs/workflows.md":
        return "workflow-guidance"
    if path in {"AGENTS.md", "CONSTITUTION.md"}:
        return "governance"
    if path.startswith("templates/"):
        return "templates"
    if path.startswith("schemas/"):
        return "schemas"
    if path in {"scripts/validate-release.py", "scripts/release-verify.sh"}:
        return "release-script"
    if path.startswith("scripts/"):
        return "script-unsupported"
    return None


def _is_lifecycle_path(path: str) -> bool:
    if path == "docs/plan.md":
        return False
    if path.startswith("docs/proposals/") and path.endswith(".md"):
        return True
    if path.startswith("specs/") and path.endswith(".md"):
        return True
    if path.startswith("docs/architecture/") and path.endswith(".md"):
        return True
    if path.startswith("docs/adr/") and path.endswith(".md"):
        return True
    if path.startswith("docs/plans/") and path.endswith(".md"):
        return True
    if path.startswith("docs/explain/") and path.endswith(".md"):
        return True
    return False


def _change_root_change_yaml(path: str) -> str | None:
    root = _change_root(path)
    if root:
        return f"{root}change.yaml"
    return None


def _plan_index_context_paths(changed_paths: tuple[str, ...]) -> list[str]:
    context: list[str] = []
    for path in changed_paths:
        if path == "docs/plan.md":
            continue
        if _is_lifecycle_path(path):
            context.append(path)
            continue
        if path.startswith("docs/changes/"):
            parts = path.split("/")
            if len(parts) >= 4 and parts[3] == "change.yaml":
                context.append(path)
                continue
            change_yaml = _change_root_change_yaml(path)
            if change_yaml:
                context.append(change_yaml)
    return _dedupe(context)


def _skill_root(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 2:
        return f"skills/{parts[1]}"
    return None


def _change_root(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 3 and parts[0] == "docs" and parts[1] == "changes":
        return f"docs/changes/{parts[2]}/"
    return None


def _release_version_from_path(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 4 and parts[0] == "docs" and parts[1] == "releases" and parts[2] and parts[3]:
        return parts[2]
    return None


def _broad_smoke_sources(
    request: SelectionRequest,
    *,
    changed_paths: list[str],
    repo_root: Path,
) -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    if request.mode in {"main", "release"}:
        sources.append({"type": "mode", "value": request.mode})
    if request.broad_smoke:
        sources.append({"type": "explicit_flag", "value": "--broad-smoke"})
    if request.mode == "release" and request.release_version:
        sources.append(
            {
                "type": "release_metadata",
                "path": f"docs/releases/{request.release_version}/release.yaml",
            }
        )

    context_paths = _dedupe([*changed_paths, *request.trigger_context_paths])
    for raw_path in context_paths:
        normalized = normalize_path(raw_path, repo_root=repo_root)
        if not normalized.ok or normalized.path is None:
            continue
        source_type = _trigger_source_type(normalized.path)
        if source_type is None:
            continue
        path = repo_root / normalized.path
        if source_type != "release_metadata" and not _file_requires_broad_smoke(path):
            continue
        source = {"type": source_type, "path": normalized.path}
        if source not in sources:
            sources.append(source)
    return sources


def _trigger_source_type(path: str) -> str | None:
    if path.startswith("docs/plans/") and path.endswith(".md"):
        return "active_plan"
    if path.startswith("specs/") and path.endswith(".test.md"):
        return "test_spec"
    if path.startswith("docs/changes/") and path.endswith("/review-resolution.md"):
        return "review_resolution"
    if path.startswith("docs/releases/") and path.endswith("/release.yaml"):
        return "release_metadata"
    return None


def _file_requires_broad_smoke(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    return "broad_smoke_required: true" in lowered or "broad smoke required" in lowered


def _join(*args: str) -> str:
    return shlex.join(args)


def _dedupe(items: list[str] | tuple[str, ...]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def _safe_path_label(path: str) -> str:
    if Path(path).is_absolute():
        return "<outside-repository>"
    return path
