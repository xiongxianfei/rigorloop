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
    r"(ready for (proposal-review|spec-review|implement|implementation|pr|code-review)|"
    r"next stage should be `?(proposal-review|spec-review|implement|implementation|pr|code-review)`?)",
    re.IGNORECASE,
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
    changed_paths: tuple[Path, ...]
    related_artifact_paths: tuple[Path, ...]
    baseline_paths: tuple[Path, ...]
    generated_paths: tuple[Path, ...]


class ValidationInputError(Exception):
    """Raised when validator input is incomplete or ambiguous."""


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
    refs: set[Path] = set()
    text = path.read_text(encoding="utf-8")
    for match in REPO_PATH_PATTERN.finditer(text):
        resolved = _normalize_repo_path(root, path, match.group("path"))
        if resolved is not None:
            refs.add(resolved)
    return refs


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


def _extract_change_yaml_refs(root: Path, path: Path) -> set[Path]:
    refs: set[Path] = set()
    lines = path.read_text(encoding="utf-8").splitlines()
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

    if "Follow-on artifacts" in sections:
        follow_on_body = sections["Follow-on artifacts"].strip()
        if not follow_on_body:
            errors.append("Follow-on artifacts section must not be empty")
        elif follow_on_body.lower() == "none yet":
            pass

    readiness = sections.get("Readiness", "")
    if readiness and STALE_READINESS_PATTERN.search(readiness):
        errors.append("status and readiness disagree about whether earlier pending stages remain")

    return errors, status


def _validate_artifact(path: Path, root: Path) -> tuple[str | None, str | None, list[str]]:
    relative_path = path.relative_to(root)
    contract = classify_artifact(relative_path)
    if contract is None:
        return None, None, []

    text = path.read_text(encoding="utf-8")
    sections = _parse_sections(text)
    errors, status = _validate_status_and_sections(relative_path, contract, sections, text)
    return contract.class_name, status, errors


def _discover_all_in_scope_artifacts(root: Path) -> set[Path]:
    results: set[Path] = set()
    for candidate in root.rglob("*.md"):
        if not candidate.is_file():
            continue
        if not _is_relative_to(candidate.resolve(), root):
            continue
        relative = candidate.resolve().relative_to(root)
        if classify_artifact(relative) is not None:
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


def _collect_diff_paths(root: Path, start: str, end: str) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", f"{start}..{end}"],
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
        changed_paths = _collect_diff_paths(root, base, head)
        input_source = "explicit PR diff range"
    elif mode == "push-main-ci":
        if not before or not after:
            raise ValidationInputError("push-main-ci mode requires --before and --after")
        changed_paths = _collect_diff_paths(root, before, after)
        input_source = "explicit push diff range"
    else:
        raise ValidationInputError(f"unsupported mode: {mode}")

    queue: list[Path] = []
    for path in changed_paths:
        if not path.exists():
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

        if not current.exists():
            continue

        if not _is_relative_to(current, root):
            continue

        relative = current.relative_to(root)
        if relative.as_posix().startswith(".codex/"):
            generated_paths.add(current)
            continue

        contract = classify_artifact(relative)
        if contract is not None:
            related_artifacts.add(current)

        if current.name == "change.yaml":
            queue.extend(sorted(_extract_change_yaml_refs(root, current)))
            continue

        relative_text = relative.as_posix()
        is_reference_surface = (
            current == pr_path
            or relative_text.startswith("docs/explain/")
            or relative_text.startswith("docs/plans/")
            or relative_text.startswith("docs/changes/")
        )
        if current.suffix == ".md" and is_reference_surface:
            queue.extend(sorted(_extract_markdown_refs(root, current)))

    baseline_paths: set[Path] = set()
    if mode != "explicit-paths":
        baseline_paths = _discover_all_in_scope_artifacts(root) - related_artifacts

    return ValidationScope(
        mode=mode,
        input_source=input_source,
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

    seen_identifiers: dict[tuple[str, str], Path] = {}

    def record_findings(paths_to_validate: tuple[Path, ...], severity: str) -> None:
        target_findings = blocking_findings if severity == "block" else warning_findings
        for path in paths_to_validate:
            artifact_class, status, errors = _validate_artifact(path, root.resolve())
            if artifact_class is None:
                continue

            contract = classify_artifact(path.relative_to(root.resolve()))
            identifier = _extract_identifier(contract, path.relative_to(root.resolve())) if contract else None
            if artifact_class and identifier:
                key = (artifact_class, identifier)
                owner = seen_identifiers.get(key)
                if owner and owner != path:
                    errors.append(f"duplicate {artifact_class} identifier: {identifier}")
                else:
                    seen_identifiers[key] = path

            for error in errors:
                target_findings.append(
                    ValidationFinding(
                        severity=severity,
                        path=path,
                        artifact_class=artifact_class,
                        status=status,
                        message=error,
                    )
                )

    record_findings(scope.related_artifact_paths, "block")
    record_findings(scope.baseline_paths, "warn")

    return ValidationResult(
        checked_artifacts=[path.relative_to(root.resolve()) for path in scope.related_artifact_paths],
        blocking_findings=blocking_findings,
        warning_findings=warning_findings,
    )
