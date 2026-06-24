#!/usr/bin/env python3
"""Validate semantic source lines in review-critical Markdown."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


SENTENCE_END_RE = re.compile(r"""[.!?][)"'`\]]*$""")
CLAUSE_END_RE = re.compile(r"""[:;][)"'`\]]*$""")
LIST_ITEM_RE = re.compile(r"^\s{0,3}(?:[-*+]|\d+[.)])\s+")
FENCE_RE = re.compile(r"^\s{0,3}(```+|~~~+)")
TABLE_RE = re.compile(r"^\s{0,3}\|")
LINK_DEFINITION_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s+")
THEMATIC_BREAK_RE = re.compile(r"^\s{0,3}(?:[-*_]\s*){3,}$")
HTML_COMMENT_RE = re.compile(r"^\s*<!--\s*([^:]+):(start|end)\s*-->\s*$")
URL_RE = re.compile(r"https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`]+`")

DETERMINISTIC_SPLITS = {
    ("AI", "agents"): "known regression: AI agents split",
    ("proposal", "to spec"): "known regression: proposal to spec split",
    ("reviewable", "in Git"): "known regression: reviewable in Git split",
}

CONTINUATION_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "for",
    "from",
    "in",
    "into",
    "of",
    "or",
    "the",
    "to",
    "with",
    "without",
}

COMMAND_START_RE = re.compile(
    r"^(?:python|python3|pip|npx|npm|yarn|pnpm|git|make|tox|pytest|ruff|mypy|./)\b"
)


@dataclass(frozen=True)
class ProseLine:
    path: Path
    number: int
    text: str
    hard_break: bool = False
    kind: str = "paragraph"


@dataclass(frozen=True)
class Finding:
    path: str
    line_start: int
    line_end: int
    severity: str
    suspected_unit: str
    reason: str
    suggested_actions: tuple[str, ...]

    def format(self) -> str:
        actions = "; ".join(self.suggested_actions)
        return (
            f"{self.path}:{self.line_start}-{self.line_end}: "
            f"{self.severity}: {self.reason}: {self.suspected_unit} "
            f"(suggested actions: {actions})"
        )


@dataclass
class ValidationResult:
    errors: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)

    @property
    def findings(self) -> list[Finding]:
        return self.errors + self.warnings

    def add(self, finding: Finding) -> None:
        if finding.severity == "error":
            self.errors.append(finding)
        else:
            self.warnings.append(finding)

    def extend(self, other: "ValidationResult") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)


def validate_paths(paths: Iterable[Path | str], mode: str = "audit") -> ValidationResult:
    result = ValidationResult()
    for raw_path in paths:
        result.extend(validate_path(Path(raw_path), mode=mode))
    return result


def validate_path(path: Path, mode: str = "audit") -> ValidationResult:
    del mode
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks = segment_prose_blocks(path, lines)
    result = ValidationResult()
    for block in blocks:
        analyze_block(block, result)
    return result


def segment_prose_blocks(path: Path, lines: list[str]) -> list[list[ProseLine]]:
    blocks: list[list[ProseLine]] = []
    current: list[ProseLine] = []
    current_list_item: list[ProseLine] = []
    current_list_content_column = 0
    in_frontmatter = bool(lines and lines[0].strip() == "---")
    in_fence = False
    in_list_fence = False
    in_html_block = False
    in_marker_block = False

    def flush() -> None:
        nonlocal current
        if current:
            blocks.append(current)
            current = []

    def flush_list_item() -> None:
        nonlocal current_list_item, current_list_content_column, in_list_fence
        if current_list_item:
            blocks.append(current_list_item)
            current_list_item = []
        current_list_content_column = 0
        in_list_fence = False

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        hard_break = has_explicit_hard_break(line)

        if current_list_item:
            if not stripped:
                flush_list_item()
                continue

            list_fence_match = FENCE_RE.match(line[current_list_content_column:])
            if in_list_fence:
                if list_fence_match:
                    in_list_fence = False
                continue
            if indentation_width(line) >= current_list_content_column and list_fence_match:
                in_list_fence = True
                continue

            nested = nested_list_item(line, current_list_content_column)
            if nested:
                flush_list_item()
                item_text = nested.group(1).strip()
                if item_text:
                    blocks.append([ProseLine(path, index, item_text, hard_break=hard_break, kind="list-item")])
                continue

            next_list_match = LIST_ITEM_RE.match(line)
            if next_list_match:
                flush_list_item()
                item_text = line[next_list_match.end() :].strip()
                if item_text:
                    current_list_item = [
                        ProseLine(path, index, item_text, hard_break=hard_break, kind="list-item")
                    ]
                    current_list_content_column = next_list_match.end()
                continue

            if indentation_width(line) >= current_list_content_column:
                item_text = line[current_list_content_column:].strip()
                if item_text:
                    current_list_item.append(
                        ProseLine(path, index, item_text, hard_break=hard_break, kind="list-item")
                    )
                continue

            flush_list_item()

        if in_frontmatter:
            if index > 1 and stripped == "---":
                in_frontmatter = False
            flush()
            continue

        fence_match = FENCE_RE.match(line)
        if fence_match:
            in_fence = not in_fence
            flush()
            continue
        if in_fence:
            flush()
            continue

        marker_match = HTML_COMMENT_RE.match(line)
        if marker_match:
            flush()
            in_marker_block = marker_match.group(2) == "start"
            continue
        if in_marker_block:
            flush()
            continue

        if in_html_block:
            if re.search(r"</[A-Za-z][^>]*>\s*$", line):
                in_html_block = False
            flush()
            continue
        if re.match(r"^\s{0,3}<[A-Za-z][^>]*>\s*$", line):
            in_html_block = not bool(re.search(r"</[A-Za-z][^>]*>\s*$", line))
            flush()
            continue

        if not stripped or is_structural_markdown(line):
            flush()
            continue

        if line.startswith("    ") or line.startswith("\t"):
            flush()
            continue

        list_match = LIST_ITEM_RE.match(line)
        if list_match:
            flush()
            item_text = line[list_match.end() :].strip()
            if item_text:
                current_list_item = [
                    ProseLine(path, index, item_text, hard_break=hard_break, kind="list-item")
                ]
                current_list_content_column = list_match.end()
            continue

        current.append(ProseLine(path, index, stripped, hard_break=hard_break))

    flush_list_item()
    flush()
    return blocks


def has_explicit_hard_break(line: str) -> bool:
    return line.endswith("\\") or len(line) - len(line.rstrip(" ")) >= 2


def indentation_width(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def nested_list_item(line: str, parent_content_column: int) -> re.Match[str] | None:
    if indentation_width(line) < parent_content_column:
        return None
    return re.match(r"^\s{0,3}(?:[-*+]|\d+[.)])\s+(.+)$", line[parent_content_column:])


def is_structural_markdown(line: str) -> bool:
    stripped = line.strip()
    return bool(
        stripped.startswith("#")
        or stripped.startswith(">")
        or TABLE_RE.match(line)
        or LINK_DEFINITION_RE.match(line)
        or THEMATIC_BREAK_RE.match(line)
    )


def analyze_block(block: list[ProseLine], result: ValidationResult) -> None:
    for previous, current in zip(block, block[1:]):
        finding = classify_pair(previous, current)
        if finding:
            result.add(finding)


def classify_pair(previous: ProseLine, current: ProseLine) -> Finding | None:
    previous_text = visible_prose(previous.text)
    current_text = visible_prose(current.text)
    if not previous_text or not current_text:
        return None
    if previous.hard_break:
        return None

    suspected = f"{previous.text} / {current.text}"
    joined = f"{previous_text} {current_text}"

    for (left, right), reason in DETERMINISTIC_SPLITS.items():
        if previous_text.endswith(left) and current_text.startswith(right):
            return make_finding(previous, current, "error", suspected, reason)

    if looks_like_lifecycle_split(previous_text, current_text):
        return make_finding(
            previous,
            current,
            "error",
            suspected,
            "lifecycle chain split across prose lines",
        )

    if looks_like_command_split(previous_text, current_text):
        return make_finding(
            previous,
            current,
            "error",
            suspected,
            "command split outside fenced block",
        )

    if sentence_complete(previous_text):
        return None

    if previous.kind == "list-item" and current.kind == "list-item":
        return make_finding(
            previous,
            current,
            "error",
            suspected,
            "mechanically continued list item",
        )

    if clause_boundary(previous_text):
        return make_finding(
            previous,
            current,
            "warning",
            suspected,
            "ambiguous clause-level break; reviewer must confirm it is deliberate",
        )

    first_word = first_word_lower(current_text)
    if first_word in CONTINUATION_WORDS:
        return make_finding(
            previous,
            current,
            "error",
            suspected,
            "mechanical mid-sentence wrap",
        )

    if first_word == "because" and "may be intentional" in joined:
        return None

    if first_word == "because" or starts_lowercase(current_text):
        reason = "ambiguous source-line break; reviewer must confirm it is deliberate"
        return make_finding(previous, current, "warning", suspected, reason)

    return None


def visible_prose(text: str) -> str:
    without_urls = URL_RE.sub("", text)
    without_code = INLINE_CODE_RE.sub("", without_urls)
    return without_code.strip()


def sentence_complete(text: str) -> bool:
    return bool(SENTENCE_END_RE.search(text))


def clause_boundary(text: str) -> bool:
    return bool(CLAUSE_END_RE.search(text) or text.endswith(" -"))


def starts_lowercase(text: str) -> bool:
    for char in text:
        if char.isalpha():
            return char.islower()
    return False


def first_word_lower(text: str) -> str:
    match = re.search(r"[A-Za-z][A-Za-z'-]*", text)
    return match.group(0).lower() if match else ""


def looks_like_lifecycle_split(previous: str, current: str) -> bool:
    if previous.rstrip().endswith(("->", "=>")):
        return True
    if " -> " in previous and first_word_lower(current) in {"spec", "plan", "implement", "verify", "pr"}:
        return True
    return False


def looks_like_command_split(previous: str, current: str) -> bool:
    candidate = previous.strip()
    if not candidate:
        return False
    if candidate.endswith(("\\", "|")):
        return False
    if sentence_complete(candidate):
        return False
    first = first_word_lower(candidate)
    if first in {"run", "execute"}:
        words = candidate.split()
        return any(COMMAND_START_RE.match(word) for word in words[1:])
    return bool(COMMAND_START_RE.match(candidate))


def make_finding(
    previous: ProseLine,
    current: ProseLine,
    severity: str,
    suspected_unit: str,
    reason: str,
) -> Finding:
    return Finding(
        path=str(previous.path),
        line_start=previous.number,
        line_end=current.number,
        severity=severity,
        suspected_unit=suspected_unit,
        reason=reason,
        suggested_actions=(
            "join lines",
            "rewrite sentence",
            "convert to structured Markdown",
        ),
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate semantic source-line shape in covered Markdown."
    )
    parser.add_argument(
        "--mode",
        choices=("audit", "enforce"),
        default="audit",
        help="audit reports findings without failing; enforce fails on errors",
    )
    parser.add_argument(
        "--path",
        action="append",
        dest="paths",
        default=[],
        help="Markdown path to validate; may be provided more than once",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    paths = [Path(path) for path in args.paths] or [Path("README.md"), Path("VISION.md")]
    result = validate_paths(paths, mode=args.mode)
    for finding in result.findings:
        print(finding.format())
    print(
        "documentation prose validation: "
        f"errors={len(result.errors)} warnings={len(result.warnings)} paths={len(paths)}"
    )
    if args.mode == "enforce" and result.errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
