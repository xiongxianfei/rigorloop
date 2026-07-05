#!/usr/bin/env python3
"""Validate Markdown readability with RigorLoop-specific deterministic checks."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


KNOWN_HARD_WRAP_PHRASES = (
    "AI agents",
    "proposal to spec",
    "reviewable in Git",
)
LONG_LINE_THRESHOLD = 120
GENERATED_START_RE = re.compile(
    r"^<!-- rigorloop:generated:start surface=(?P<surface>\S+) source=(?P<source>\S+)(?: generator=(?P<generator>\S+))? -->$"
)
GENERATED_END_RE = re.compile(r"^<!-- rigorloop:generated:end surface=(?P<surface>\S+) -->$")
PLACEHOLDER_RE = re.compile(r"<[A-Za-z][A-Za-z0-9 _/-]*>")
SURFACE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


@dataclass(frozen=True)
class ChangedSection:
    path: Path
    start_line: int
    end_line: int


@dataclass(frozen=True)
class Diagnostic:
    check_id: str
    severity: str
    path: Path
    line: int
    message: str

    def render(self) -> str:
        return f"{self.severity.upper()} {self.check_id} {self.path}:{self.line}: {self.message}"


@dataclass(frozen=True)
class ValidationResult:
    diagnostics: tuple[Diagnostic, ...]

    @property
    def has_errors(self) -> bool:
        return any(diagnostic.severity == "error" for diagnostic in self.diagnostics)


@dataclass(frozen=True)
class LineInfo:
    line_number: int
    text: str
    excluded_from_prose: bool


@dataclass(frozen=True)
class GeneratedRegionStart:
    surface: str
    source: str | None
    generator: str | None
    line_number: int


def parse_changed_section(raw: str) -> ChangedSection:
    try:
        path_text, start_text, end_text = raw.rsplit(":", 2)
        start_line = int(start_text)
        end_line = int(end_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "changed sections must use PATH:START:END with 1-based line numbers"
        ) from exc
    if start_line < 1 or end_line < start_line:
        raise argparse.ArgumentTypeError("changed section line range must be positive and ordered")
    return ChangedSection(Path(path_text), start_line, end_line)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Markdown readability.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Markdown paths to validate; defaults to README.md and VISION.md when present",
    )
    parser.add_argument(
        "--changed-section",
        action="append",
        default=[],
        type=parse_changed_section,
        help="enforce changed-section prose checks for PATH:START:END",
    )
    parser.add_argument(
        "--generated-document",
        action="append",
        default=[],
        type=Path,
        help="validate generated-document placeholder removal for this path",
    )
    parser.add_argument("--verbose", action="store_true", help="print audit-only warning diagnostics")
    return parser.parse_args(argv)


def default_paths() -> list[Path]:
    return [path for path in (Path("README.md"), Path("VISION.md")) if path.exists()]


def validate_paths(
    paths: list[Path],
    *,
    changed_sections: list[ChangedSection] | None = None,
    generated_documents: set[Path] | None = None,
) -> ValidationResult:
    changed_sections = changed_sections or []
    generated_documents = generated_documents or set()
    normalized_generated_documents = {_normalize_path(path) for path in generated_documents}
    diagnostics: list[Diagnostic] = []

    for path in paths:
        normalized_path = _normalize_path(path)
        text = _read_text(path)
        lines = text.splitlines()
        line_infos = _classify_lines(lines)
        path_changed_sections = [
            section
            for section in changed_sections
            if _normalize_path(section.path) == normalized_path
        ]

        diagnostics.extend(_validate_generated_regions(path, lines))
        diagnostics.extend(_validate_hard_wraps(path, line_infos, path_changed_sections))
        diagnostics.extend(_audit_long_lines(path, line_infos, path_changed_sections))
        diagnostics.extend(_audit_dense_paragraphs(path, line_infos, path_changed_sections))
        if normalized_path in normalized_generated_documents:
            diagnostics.extend(_validate_placeholders(path, lines))

    return ValidationResult(tuple(diagnostics))


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"{path}: file does not exist") from exc
    except UnicodeDecodeError as exc:
        raise SystemExit(f"{path}: not valid UTF-8: {exc}") from exc


def _normalize_path(path: Path) -> Path:
    try:
        return path.resolve()
    except FileNotFoundError:
        return path.absolute()


def _classify_lines(lines: list[str]) -> list[LineInfo]:
    infos: list[LineInfo] = []
    in_fence = False
    in_html_block = False
    in_generated_region = False

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        excluded = False

        if stripped.startswith("```") or stripped.startswith("~~~"):
            excluded = True
            in_fence = not in_fence
        elif in_fence:
            excluded = True
        elif GENERATED_START_RE.match(stripped):
            excluded = True
            in_generated_region = True
        elif GENERATED_END_RE.match(stripped):
            excluded = True
            in_generated_region = False
        elif in_generated_region:
            excluded = True
        elif _is_table_line(stripped):
            excluded = True
        elif _is_link_reference(stripped):
            excluded = True
        elif _is_html_block_start(stripped):
            excluded = True
            if not _is_html_block_single_line(stripped):
                in_html_block = True
        elif in_html_block:
            excluded = True
            if _is_html_block_end(stripped):
                in_html_block = False

        infos.append(LineInfo(index, line, excluded))

    return infos


def _is_table_line(stripped: str) -> bool:
    return stripped.startswith("|") or stripped.endswith("|")


def _is_link_reference(stripped: str) -> bool:
    return bool(re.match(r"^\[[^\]]+\]:\s+\S+", stripped))


def _is_html_block_start(stripped: str) -> bool:
    return bool(re.match(r"^<[A-Za-z][^>]*>$", stripped))


def _is_html_block_end(stripped: str) -> bool:
    return bool(re.match(r"^</[A-Za-z][^>]*>$", stripped))


def _is_html_block_single_line(stripped: str) -> bool:
    return _is_html_block_end(stripped) or bool(re.match(r"^<[A-Za-z][^>]*/>$", stripped))


def _validate_generated_regions(path: Path, lines: list[str]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    stack: list[GeneratedRegionStart] = []
    seen_surfaces: dict[str, int] = {}

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if "rigorloop:generated:start" in stripped:
            match = GENERATED_START_RE.match(stripped)
            if not match:
                diagnostics.append(
                    Diagnostic(
                        "MDREAD-004",
                        "error",
                        path,
                        index,
                        "generated-region start marker must use canonical surface/source/generator syntax",
                    )
                )
                continue
            surface = match.group("surface")
            source = match.group("source")
            generator = match.group("generator")
            if not SURFACE_RE.fullmatch(surface):
                diagnostics.append(
                    Diagnostic("MDREAD-004", "error", path, index, "generated-region surface is not stable")
                )
            if surface in seen_surfaces:
                diagnostics.append(
                    Diagnostic(
                        "MDREAD-004",
                        "error",
                        path,
                        index,
                        f"generated-region surface duplicates line {seen_surfaces[surface]}",
                    )
                )
            else:
                seen_surfaces[surface] = index
            if not source:
                diagnostics.append(
                    Diagnostic("MDREAD-004", "error", path, index, "generated-region source metadata is required")
                )
            if generator is not None and not generator.strip():
                diagnostics.append(
                    Diagnostic("MDREAD-004", "error", path, index, "generated-region generator metadata is empty")
                )
            stack.append(GeneratedRegionStart(surface, source, generator, index))
        elif "rigorloop:generated:end" in stripped:
            match = GENERATED_END_RE.match(stripped)
            if not match:
                diagnostics.append(
                    Diagnostic(
                        "MDREAD-004",
                        "error",
                        path,
                        index,
                        "generated-region end marker must use canonical surface syntax",
                    )
                )
                continue
            if not stack:
                diagnostics.append(
                    Diagnostic("MDREAD-004", "error", path, index, "generated-region end marker has no start")
                )
                continue
            start = stack.pop()
            end_surface = match.group("surface")
            if start.surface != end_surface:
                diagnostics.append(
                    Diagnostic(
                        "MDREAD-004",
                        "error",
                        path,
                        index,
                        f"generated-region end surface '{end_surface}' does not match start surface '{start.surface}'",
                    )
                )

    for start in stack:
        diagnostics.append(
            Diagnostic(
                "MDREAD-004",
                "error",
                path,
                start.line_number,
                f"generated-region surface '{start.surface}' is missing an end marker",
            )
        )

    return diagnostics


def _validate_hard_wraps(
    path: Path, line_infos: list[LineInfo], changed_sections: list[ChangedSection]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for current, following in zip(line_infos, line_infos[1:]):
        if not _is_prose_pair(current, following):
            continue
        joined = f"{current.text.strip()} {following.text.strip()}"
        normalized = _collapse_spaces(joined)
        for phrase in KNOWN_HARD_WRAP_PHRASES:
            if phrase not in normalized:
                continue
            if phrase in current.text or phrase in following.text:
                continue
            severity = "error" if _line_pair_in_changed_sections(current, following, changed_sections) else "warning"
            diagnostics.append(
                Diagnostic(
                    "MDREAD-001",
                    severity,
                    path,
                    current.line_number,
                    f"known semantic phrase '{phrase}' is split across source lines",
                )
            )
    return diagnostics


def _audit_long_lines(
    path: Path, line_infos: list[LineInfo], changed_sections: list[ChangedSection]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for line_info in line_infos:
        if line_info.excluded_from_prose or len(line_info.text) <= LONG_LINE_THRESHOLD:
            continue
        if changed_sections and not _line_in_changed_sections(line_info.line_number, changed_sections):
            continue
        diagnostics.append(
            Diagnostic(
                "MDREAD-002",
                "warning",
                path,
                line_info.line_number,
                "long semantic source line is audit-only and does not fail validation",
            )
        )
    return diagnostics


def _audit_dense_paragraphs(
    path: Path, line_infos: list[LineInfo], changed_sections: list[ChangedSection]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    paragraph: list[LineInfo] = []

    def flush() -> None:
        if len(paragraph) < 4:
            return
        first = paragraph[0]
        if changed_sections and not any(
            _line_in_changed_sections(line_info.line_number, changed_sections) for line_info in paragraph
        ):
            return
        diagnostics.append(
            Diagnostic(
                "MDREAD-003",
                "warning",
                path,
                first.line_number,
                "dense generated prose is audit-only unless narrowed by deterministic fixtures",
            )
        )

    for line_info in line_infos:
        stripped = line_info.text.strip()
        if line_info.excluded_from_prose or not stripped or stripped.startswith("#") or stripped.startswith("- "):
            flush()
            paragraph = []
        else:
            paragraph.append(line_info)
    flush()
    return diagnostics


def _validate_placeholders(path: Path, lines: list[str]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for index, line in enumerate(lines, start=1):
        for match in PLACEHOLDER_RE.finditer(line):
            diagnostics.append(
                Diagnostic(
                    "MDREAD-005",
                    "error",
                    path,
                    index,
                    f"generated document contains unfilled placeholder {match.group(0)}",
                )
            )
    return diagnostics


def _is_prose_pair(current: LineInfo, following: LineInfo) -> bool:
    return _is_prose_line(current) and _is_prose_line(following)


def _is_prose_line(line_info: LineInfo) -> bool:
    stripped = line_info.text.strip()
    if line_info.excluded_from_prose or not stripped:
        return False
    if stripped.startswith(("#", "-", "*", ">", "<!--")):
        return False
    return True


def _collapse_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value)


def _line_pair_in_changed_sections(
    current: LineInfo, following: LineInfo, changed_sections: list[ChangedSection]
) -> bool:
    return _line_in_changed_sections(current.line_number, changed_sections) or _line_in_changed_sections(
        following.line_number, changed_sections
    )


def _line_in_changed_sections(line_number: int, changed_sections: list[ChangedSection]) -> bool:
    return any(section.start_line <= line_number <= section.end_line for section in changed_sections)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    paths = [Path(path) for path in args.paths] if args.paths else default_paths()
    result = validate_paths(
        paths,
        changed_sections=args.changed_section,
        generated_documents=set(args.generated_document),
    )

    for diagnostic in result.diagnostics:
        if diagnostic.severity == "error" or args.verbose:
            print(diagnostic.render())
    warnings = [diagnostic for diagnostic in result.diagnostics if diagnostic.severity == "warning"]
    if warnings and not args.verbose:
        counts = Counter(diagnostic.check_id for diagnostic in warnings)
        summary = ", ".join(f"{check_id}={count}" for check_id, count in sorted(counts.items()))
        print(f"Markdown readability warnings: {summary}")
    if result.has_errors:
        print(f"Markdown readability validation failed: {len(result.diagnostics)} diagnostic(s)")
        return 1
    print(f"Markdown readability validation passed: {len(paths)} file(s), {len(result.diagnostics)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
