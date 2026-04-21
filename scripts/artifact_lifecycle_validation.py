#!/usr/bin/env python3
"""Shared validation helpers for artifact lifecycle ownership."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from artifact_lifecycle_contracts import ArtifactContract, classify_artifact


PLACEHOLDER_PATTERN = re.compile(r"\b(TODO|TBD|lorem ipsum)\b", re.IGNORECASE)
REPO_PATH_PATTERN = re.compile(
    r"(?P<path>(?:\.\./|\.\/)?(?:docs|specs|\.codex)/[A-Za-z0-9._/\-]+(?:\.md|\.yaml))"
)
STALE_READINESS_PATTERN = re.compile(
    r"(ready for `?(proposal-review|spec-review|implement|implementation|pr|code-review)`?|"
    r"next stage should be `?(proposal-review|spec-review|implement|implementation|pr|code-review)`?)",
    re.IGNORECASE,
)
PLAN_NON_SCOPE_SECTIONS = frozenset(
    {
        "Milestones",
        "Progress",
        "Decision log",
        "Surprises and discoveries",
        "Validation notes",
        "Outcome and retrospective",
        "Readiness",
    }
)
PLAN_SCOPE_SECTIONS = frozenset(
    {
        "Source artifacts",
        "Pre-implementation prerequisites",
        "Related artifacts",
    }
)


@dataclass(frozen=True)
class ValidationFinding:
    severity: str
    path: Path
    artifact_class: str | None
    status: str | None
    message: str


@dataclass(frozen=True)
class ValidationResult:
    checked_artifacts: list[Path]
    blocking_findings: list[ValidationFinding]
    warning_findings: list[ValidationFinding]


@dataclass(frozen=True)
class ValidationScope:
    mode: str
    input_source: str
    tracked_revision: str | None
    changed_paths: tuple[Path, ...]
    related_artifact_paths: tuple[Path, ...]
    baseline_paths: tuple[Path, ...]
    generated_paths: tuple[Path, ...]


class ValidationInputError(Exception):
    """Raised when validator input is incomplete or ambiguous."""


@dataclass(frozen=True)
class ArtifactInspection:
    path: Path
    contract: ArtifactContract
    status: str | None
    identifier: str | None
    errors: tuple[str, ...]


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def _normalize_repo_path(root: Path, source_path: Path, raw_path: str) -> Path | None:
    candidate = raw_path.strip().strip("`").rstrip(").,")
    if not candidate:
        return None

    if candidate.startswith("./") or candidate.startswith("../"):
        resolved = (source_path.parent / candidate).resolve()
    else:
        resolved = (root / candidate).resolve()

    if not _is_relative_to(resolved, root):
        return None
    return resolved


def _extract_markdown_refs(root: Path, path: Path) -> set[Path]:
    return _extract_repo_path_refs_from_text(root, path, _read_repo_text(root, path))


def _extract_repo_path_refs_from_text(root: Path, path: Path, text: str) -> set[Path]:
    refs: set[Path] = set()
    for match in REPO_PATH_PATTERN.finditer(text):
        resolved = _normalize_repo_path(root, path, match.group("path"))
        if resolved is not None:
            refs.add(resolved)
    return refs


def _extract_plan_refs(root: Path, path: Path, tracked_revision: str | None = None) -> set[Path]:
    refs: set[Path] = set()
    sections = _parse_sections(_read_repo_text(root, path, tracked_revision))
    for section_name, body in sections.items():
        if section_name in PLAN_NON_SCOPE_SECTIONS:
            continue
        if section_name not in PLAN_SCOPE_SECTIONS and not section_name.startswith("Related "):
            continue
        refs.update(_extract_repo_path_refs_from_text(root, path, body))
    return {ref for ref in refs if _is_lifecycle_reference_path(root, ref)}


def _contains_placeholder_text(text: str) -> bool:
    sanitized_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        sanitized_lines.append(re.sub(r"`[^`]+`", "", line))
    sanitized = "\n".join(sanitized_lines)
    return PLACEHOLDER_PATTERN.search(sanitized) is not None


def _extract_change_yaml_refs(root: Path, path: Path, tracked_revision: str | None = None) -> set[Path]:
    refs: set[Path] = set()
    lines = _read_repo_text(root, path, tracked_revision).splitlines()
    in_artifacts = False
    artifact_indent = 0

    for raw_line in lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if stripped == "artifacts:":
            in_artifacts = True
            artifact_indent = indent
            continue
        if in_artifacts and indent <= artifact_indent:
            break
        if not in_artifacts or ":" not in stripped:
            continue
        _, value = stripped.split(":", 1)
        resolved = _normalize_repo_path(root, path, value.strip().strip("'\""))
        if resolved is not None:
            refs.add(resolved)

    return refs


def _parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    body: list[str] = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(body).strip("\n")
            current = line[3:].strip()
            body = []
            continue
        if current is not None:
            body.append(line)

    if current is not None:
        sections[current] = "\n".join(body).strip("\n")

    return sections


def _extract_status(sections: dict[str, str]) -> str | None:
    raw = sections.get("Status")
    if raw is None:
        return None
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            return stripped[2:].strip()
        return stripped
    return None


def _extract_identifier(contract: ArtifactContract, relative_path: Path) -> str | None:
    if contract.class_name == "proposal":
        return relative_path.stem
    if contract.class_name == "spec":
        return relative_path.stem
    if contract.class_name == "adr":
        return relative_path.stem
    return None


def _has_replacement_pointer(text: str) -> bool:
    lowered = text.lower()
    return "superseded_by:" in lowered or "superseded by:" in lowered


def _has_terminal_closeout(sections: dict[str, str]) -> bool:
    return "Follow-on artifacts" in sections or "Closeout" in sections


def _is_lifecycle_reference_path(root: Path, path: Path) -> bool:
    relative = path.relative_to(root).as_posix()
    if relative.startswith("docs/proposals/"):
        return True
    if relative.startswith("docs/architecture/"):
        return True
    if relative.startswith("docs/adr/"):
        return True
    if relative.startswith("docs/plans/"):
        return True
    if relative.startswith("docs/explain/"):
        return True
    if relative.startswith("docs/changes/") and relative.endswith("/change.yaml"):
        return True
    if relative.startswith("specs/") and relative.endswith(".md"):
        return True
    return False


def _read_git_text(root: Path, tracked_revision: str, relative_path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{tracked_revision}:{relative_path.as_posix()}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _read_repo_text(root: Path, path: Path, tracked_revision: str | None = None) -> str:
    if tracked_revision is None:
        return path.read_text(encoding="utf-8")
    return _read_git_text(root, tracked_revision, path.relative_to(root))


def _tracked_path_exists(root: Path, tracked_revision: str, relative_path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-e", f"{tracked_revision}:{relative_path.as_posix()}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _path_exists(root: Path, path: Path, tracked_revision: str | None = None) -> bool:
    if tracked_revision is None:
        return path.exists()
    return _tracked_path_exists(root, tracked_revision, path.relative_to(root))


def _requires_readiness_consistency_check(contract: ArtifactContract, status: str | None) -> bool:
    if status is None:
        return False
    return status in contract.settlement_statuses or status in contract.terminal_statuses


def _validate_status_and_sections(
    path: Path,
    contract: ArtifactContract,
    sections: dict[str, str],
    text: str,
) -> tuple[list[str], str | None]:
    errors: list[str] = []
    status = _extract_status(sections)

    if status is None:
        return ["missing required Status section"], None
    if status not in contract.allowed_statuses:
        errors.append(f"invalid status '{status}' for {contract.class_name}")

    if _contains_placeholder_text(text):
        errors.append("placeholder text is not allowed")

    for section_name in contract.required_sections:
        if section_name not in sections:
            errors.append(f"missing required '{section_name}' section")
            continue
        if not sections[section_name].strip():
            errors.append(f"required '{section_name}' section must not be empty")

    identifier = _extract_identifier(contract, path)
    if identifier and contract.identifier_pattern and not contract.identifier_pattern.fullmatch(identifier):
        errors.append(f"invalid {contract.identifier_label}: {identifier}")

    if status in contract.terminal_statuses:
        if not _has_terminal_closeout(sections):
            errors.append("terminal artifacts must include a Closeout or Follow-on artifacts section")
        follow_on = sections.get("Follow-on artifacts")
        if follow_on is not None and not follow_on.strip():
            errors.append("Follow-on artifacts section must not be empty")
        if status.lower() == "superseded" and not _has_replacement_pointer(text):
            errors.append("superseded artifacts must identify a replacement")

    if "Next artifacts" in sections and not sections["Next artifacts"].strip():
        errors.append("Next artifacts section must not be empty")

    if "Follow-on artifacts" in sections:
        follow_on_body = sections["Follow-on artifacts"].strip()
        if not follow_on_body:
            errors.append("Follow-on artifacts section must not be empty")
        elif follow_on_body.lower() == "none yet":
            pass

    readiness = sections.get("Readiness", "")
    if readiness and _requires_readiness_consistency_check(contract, status) and STALE_READINESS_PATTERN.search(
        readiness
    ):
        errors.append("status and readiness disagree about whether earlier pending stages remain")

    return errors, status


def _inspect_artifact(path: Path, root: Path, tracked_revision: str | None = None) -> ArtifactInspection | None:
    relative_path = path.relative_to(root)
    text = _read_repo_text(root, path, tracked_revision)
    contract = classify_artifact(relative_path, text)
    if contract is None:
        return None
    sections = _parse_sections(text)
    errors, status = _validate_status_and_sections(relative_path, contract, sections, text)
    identifier = _extract_identifier(contract, relative_path)
    return ArtifactInspection(
        path=path,
        contract=contract,
        status=status,
        identifier=identifier,
        errors=tuple(errors),
    )


def _tracked_markdown_paths(root: Path, tracked_revision: str) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only", "-z", tracked_revision],
        check=True,
        capture_output=True,
    )
    return [
        (root / entry.decode("utf-8")).resolve()
        for entry in result.stdout.split(b"\0")
        if entry and entry.decode("utf-8").endswith(".md")
    ]


def _discover_all_in_scope_artifacts(root: Path, tracked_revision: str | None = None) -> set[Path]:
    results: set[Path] = set()
    candidates = root.rglob("*.md") if tracked_revision is None else _tracked_markdown_paths(root, tracked_revision)
    for candidate in candidates:
        if not candidate.is_file():
            if tracked_revision is None:
                continue
        if not _is_relative_to(candidate.resolve(), root):
            continue
        text = _read_repo_text(root, candidate.resolve(), tracked_revision)
        relative = candidate.resolve().relative_to(root)
        if classify_artifact(relative, text) is not None:
            results.add(candidate.resolve())
    return results


def _collect_local_changed_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
        check=True,
        capture_output=True,
        text=True,
    )
    changed: list[Path] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        raw_path = line[3:]
        if " -> " in raw_path:
            raw_path = raw_path.split(" -> ", 1)[1]
        changed.append((root / raw_path).resolve())
    return changed


def _collect_diff_paths(root: Path, diff_spec: str) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", diff_spec],
        check=True,
        capture_output=True,
        text=True,
    )
    return [(root / line.strip()).resolve() for line in result.stdout.splitlines() if line.strip()]


def _resolve_scope(
    root: Path,
    *,
    mode: str,
    paths: list[str],
    base: str | None = None,
    head: str | None = None,
    before: str | None = None,
    after: str | None = None,
    pr_body_file: str | None = None,
) -> ValidationScope:
    tracked_revision: str | None = None
    if mode == "explicit-paths":
        if not paths:
            raise ValidationInputError("explicit-paths mode requires at least one --path")
        changed_paths = [((root / raw).resolve()) for raw in paths]
        input_source = "explicit paths"
    elif mode == "local":
        changed_paths = _collect_local_changed_paths(root)
        input_source = "local working tree"
    elif mode == "pr-ci":
        if not base or not head:
            raise ValidationInputError("pr-ci mode requires --base and --head")
        changed_paths = _collect_diff_paths(root, f"{base}...{head}")
        input_source = "explicit PR diff range"
        tracked_revision = head
    elif mode == "push-main-ci":
        if not before or not after:
            raise ValidationInputError("push-main-ci mode requires --before and --after")
        changed_paths = _collect_diff_paths(root, f"{before}..{after}")
        input_source = "explicit push diff range"
        tracked_revision = after
    else:
        raise ValidationInputError(f"unsupported mode: {mode}")

    queue: list[Path] = []
    for path in changed_paths:
        if not _path_exists(root, path, tracked_revision):
            if tracked_revision is not None:
                continue
            raise ValidationInputError(f"input path does not exist: {path.relative_to(root)}")
        queue.append(path)

    if pr_body_file:
        pr_path = (root / pr_body_file).resolve()
        if not pr_path.exists():
            raise ValidationInputError(f"PR body file does not exist: {pr_body_file}")
        queue.append(pr_path)
    else:
        pr_path = None

    visited: set[Path] = set()
    related_artifacts: set[Path] = set()
    generated_paths: set[Path] = set()

    while queue:
        current = queue.pop()
        if current in visited:
            continue
        visited.add(current)

        current_revision = None if current == pr_path else tracked_revision

        if not _path_exists(root, current, current_revision):
            continue

        if not _is_relative_to(current, root):
            continue

        relative = current.relative_to(root)
        if relative.as_posix().startswith(".codex/"):
            if mode == "explicit-paths":
                generated_paths.add(current)
            continue

        current_text = _read_repo_text(root, current, current_revision) if current.suffix in {".md", ".yaml"} else None
        contract = classify_artifact(relative, current_text if current.suffix == ".md" else None)
        if contract is not None:
            related_artifacts.add(current)

        if current.name == "change.yaml":
            queue.extend(sorted(_extract_change_yaml_refs(root, current, current_revision)))
            continue

        relative_text = relative.as_posix()
        is_reference_surface = (
            current == pr_path
            or relative_text.startswith("docs/explain/")
            or relative_text.startswith("docs/plans/")
            or relative_text.startswith("docs/changes/")
        )
        if current.suffix == ".md" and is_reference_surface:
            if relative_text.startswith("docs/plans/"):
                queue.extend(sorted(_extract_plan_refs(root, current, current_revision)))
            else:
                queue.extend(sorted(_extract_repo_path_refs_from_text(root, current, current_text or "")))

    baseline_paths: set[Path] = set()
    if mode != "explicit-paths":
        baseline_paths = _discover_all_in_scope_artifacts(root, tracked_revision) - related_artifacts

    return ValidationScope(
        mode=mode,
        input_source=input_source,
        tracked_revision=tracked_revision,
        changed_paths=tuple(sorted(changed_paths)),
        related_artifact_paths=tuple(sorted(related_artifacts)),
        baseline_paths=tuple(sorted(baseline_paths)),
        generated_paths=tuple(sorted(generated_paths)),
    )


def validate_repository(
    root: Path,
    *,
    mode: str,
    paths: list[str] | None = None,
    base: str | None = None,
    head: str | None = None,
    before: str | None = None,
    after: str | None = None,
    pr_body_file: str | None = None,
) -> ValidationResult:
    scope = _resolve_scope(
        root.resolve(),
        mode=mode,
        paths=paths or [],
        base=base,
        head=head,
        before=before,
        after=after,
        pr_body_file=pr_body_file,
    )

    blocking_findings: list[ValidationFinding] = []
    warning_findings: list[ValidationFinding] = []
    root_resolved = root.resolve()
    related_paths = set(scope.related_artifact_paths)

    for path in scope.generated_paths:
        blocking_findings.append(
            ValidationFinding(
                severity="block",
                path=path,
                artifact_class=None,
                status=None,
                message="generated output path must not be treated as authored source of truth",
            )
        )

    inspections: dict[Path, ArtifactInspection] = {}
    for path in tuple(sorted(related_paths | set(scope.baseline_paths))):
        inspection = _inspect_artifact(path, root_resolved, scope.tracked_revision)
        if inspection is not None:
            inspections[path] = inspection

    for inspection in inspections.values():
        target_findings = blocking_findings if inspection.path in related_paths else warning_findings
        for error in inspection.errors:
            target_findings.append(
                ValidationFinding(
                    severity="block" if inspection.path in related_paths else "warn",
                    path=inspection.path,
                    artifact_class=inspection.contract.class_name,
                    status=inspection.status,
                    message=error,
                )
            )

    duplicate_groups: dict[tuple[str, str], list[ArtifactInspection]] = {}
    for inspection in inspections.values():
        if inspection.identifier is None:
            continue
        key = (inspection.contract.class_name, inspection.identifier)
        duplicate_groups.setdefault(key, []).append(inspection)

    for (artifact_class, identifier), group in duplicate_groups.items():
        if len(group) < 2:
            continue
        any_related = any(inspection.path in related_paths for inspection in group)
        target_findings = blocking_findings if any_related else warning_findings
        severity = "block" if any_related else "warn"
        for inspection in sorted(group, key=lambda item: item.path.as_posix()):
            target_findings.append(
                ValidationFinding(
                    severity=severity,
                    path=inspection.path,
                    artifact_class=artifact_class,
                    status=inspection.status,
                    message=f"duplicate {artifact_class} identifier: {identifier}",
                )
            )

    return ValidationResult(
        checked_artifacts=[path.relative_to(root_resolved) for path in scope.related_artifact_paths],
        blocking_findings=blocking_findings,
        warning_findings=warning_findings,
    )
