#!/usr/bin/env python3
"""Deterministic current model and owned-example validation."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from lib.validation.model_layout import PROJECT_MODEL_PATHS


STABLE_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9-]*$")


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str
    offending_value: str
    expected: str

    def as_dict(self) -> dict[str, str]:
        return {
            "check_id": self.code,
            "path": self.path,
            "message": self.message,
            "offending_value": _redacted_value(self.offending_value),
            "expected": self.expected,
        }


def _issue(
    code: str,
    path: str,
    message: str,
    value: object = "-",
    expected: object = "-",
) -> ValidationIssue:
    return ValidationIssue(code, path, message, str(value), str(expected))


def _redacted_value(value: str) -> str:
    encoded = value.encode("utf-8")
    return (
        "redacted:sha256:"
        + hashlib.sha256(encoded).hexdigest()
        + f":bytes={len(encoded)}"
    )


def _live_markdown(text: str) -> str:
    """Preserve line positions while removing fenced-code content."""

    output: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(?:[^`]*)$", line)
        if fence_character is None:
            if match:
                token = match.group(1)
                fence_character = token[0]
                fence_length = len(token)
                output.append("")
            else:
                output.append(line)
            continue
        close = re.match(
            rf"^ {{0,3}}{re.escape(fence_character)}{{{fence_length},}}\s*$",
            line,
        )
        output.append("")
        if close:
            fence_character = None
            fence_length = 0
    return "\n".join(output)


MODEL_DIMENSIONS = (
    "Input domain", "State/lifecycle", "Identity/authority", "Composition/path",
    "Temporal/retry", "Failure/recovery", "Compatibility/migration", "External/environment",
)


def validate_model_record(text: str, path: str) -> tuple[ValidationIssue, ...]:
    """Explicit model format: structural proof only, never workflow settlement."""
    text = _live_markdown(re.sub(r"<!--[\s\S]*?(?:-->|$)", "", text))
    markers = re.findall(r"^Model validation contract:\s*(.*?)\s*$", text, re.MULTILINE)
    if markers != ["model-document-v1"]:
        return (_issue("BFR-MODEL-CONTRACT", path, "exactly one model-document-v1 model contract marker is required", markers),)

    def table(heading: str, columns: tuple[str, ...]) -> list[list[str]]:
        # Four columns (including tabs) are code, not authoritative structure.
        # Normalize only ordinary indentation.
        lines = ["" if line.expandtabs(4).startswith("    ") else line.strip()
                 for line in text.splitlines()]
        positions = [i for i, line in enumerate(lines) if line == heading]
        if len(positions) != 1:
            raise ValueError("one required heading is required")
        body = []
        for line in lines[positions[0] + 1:]:
            if line.startswith("#"):
                break
            body.append(line)
        starts = [i for i, line in enumerate(body) if line.startswith("|") and (i == 0 or not body[i-1].startswith("|"))]
        if len(starts) != 1:
            raise ValueError("one table is required")
        rows = []
        for line in body[starts[0]:]:
            if not line.startswith("|"):
                break
            if not line.endswith("|"):
                raise ValueError("table row is not closed")
            row = [cell.strip() for cell in line[1:-1].split("|")]
            if len(row) != len(columns):
                raise ValueError("table row has wrong width")
            rows.append(row)
        if len(rows) < 3 or tuple(rows[0]) != columns or any(not re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
            raise ValueError("table header, separator or body is invalid")
        return rows[2:]

    try:
        requirements = table("## Requirements", ("ID", "Required behavior"))
        scenarios = table("### Boundary scan and acceptance scenarios", ("Dimension", "Requirement basis", "Distinct outcome to demonstrate"))
    except ValueError as error:
        return (_issue("BFR-MODEL-TABLE", path, str(error)),)
    ids = [row[0] for row in requirements]
    if len(ids) != len(set(ids)) or any(not STABLE_ID_RE.fullmatch(row[0]) or not row[1] for row in requirements):
        return (_issue("BFR-MODEL-REQUIREMENTS", path, "requirement IDs must be unique and valid with nonempty text"),)
    dimensions = [row[0] for row in scenarios]
    # Closed vocabulary is checked before dependent reference/consistency rules.
    if len(dimensions) != len(MODEL_DIMENSIONS) or set(dimensions) != set(MODEL_DIMENSIONS):
        return (_issue("BFR-MODEL-DIMENSIONS", path, "exactly one row for each known model dimension is required", dimensions),)
    for _, basis, outcome in scenarios:
        if basis == "-":
            if not outcome.startswith("Not applicable:") or not outcome.removeprefix("Not applicable:").strip():
                return (_issue("BFR-MODEL-APPLICABILITY", path, "non-applicability requires a reason"),)
        else:
            refs = basis.split(", ")
            if len(refs) != len(set(refs)) or not set(refs).issubset(ids) or not outcome or outcome.startswith("Not applicable:"):
                return (_issue("BFR-MODEL-REFERENCES", path, "applicable rows require unique local requirement references and an outcome"),)
    return ()


def validate_model_path(root: Path, relative_path: str) -> tuple[ValidationIssue, ...]:
    if relative_path not in PROJECT_MODEL_PATHS.values() and not re.fullmatch(r"docs/design/(?P<model>[a-z0-9][a-z0-9-]{0,79})(?:/(?P=model))?\.md", relative_path):
        return (_issue("BFR-MODEL-PATH", "<model-path>", "invalid model path", relative_path),)
    root = root.resolve()
    path = root
    try:
        for part in PurePosixPath(relative_path).parts:
            path = path / part
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                return (_issue("BFR-MODEL-PATH", "<model-path>", "model path must not traverse symlinks", relative_path),)
        if not path.is_file():
            return (_issue("BFR-MODEL-PATH", relative_path, "model must be an existing regular file"),)
        return validate_model_record(path.read_text(encoding="utf-8"), relative_path)
    except (OSError, UnicodeError, RuntimeError):
        return (_issue("BFR-MODEL-READ", relative_path, "model file cannot be safely read"),)


def validate_repository_examples(root: Path) -> tuple[tuple[str, ...], tuple[ValidationIssue, ...]]:
    """Check model-document examples and JSON syntax in declared owned namespaces.

    Complete stored records and request/result semantics retain their schema and
    interaction checks in the model example suites; syntax never grants approval.
    """
    checked = []
    issues = []
    for namespace in ("docs/design/cli/examples", "docs/design/skill/examples/workflow"):
        base = root / namespace
        if any(parent.is_symlink() for parent in (base, *base.parents) if parent != root):
            issues.append(_issue("BFR-EXAMPLE-PATH", namespace, "example namespace must not traverse symlinks"))
            continue
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                issues.append(_issue("BFR-EXAMPLE-PATH", relative, "example must not be a symlink"))
            elif path.is_file() and path.suffix == ".json":
                checked.append(relative)
                try:
                    json.loads(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, ValueError):
                    issues.append(_issue("BFR-EXAMPLE-JSON", relative, "example must be readable valid JSON"))
    # The authoring model owns the portable model-document worked example.
    relative = PROJECT_MODEL_PATHS["design"]
    if not validate_model_path(root, relative):
        text = (root / relative).read_text(encoding="utf-8")
        for index, (_, example) in enumerate(re.findall(r"^(`{3,})markdown\n([\s\S]*?)^\1[ \t]*$", text, re.MULTILINE)):
            if "Model validation contract:" in example:
                label = f"{relative}#model-example-{index + 1}"
                checked.append(label)
                issues.extend(validate_model_record(example, label))
    return tuple(checked), tuple(issues)
