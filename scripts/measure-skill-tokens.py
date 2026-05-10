#!/usr/bin/env python3
"""Measure static size and estimated token cost for canonical skills."""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SectionMeasurement:
    heading: str
    bytes: int
    lines: int
    estimated_tokens: int


@dataclass(frozen=True)
class SkillMeasurement:
    path: Path
    bytes: int
    lines: int
    estimated_tokens: int
    status: str
    largest_sections: tuple[SectionMeasurement, ...]


def estimate_tokens(text: str) -> int:
    """Return a deterministic local token estimate without external dependencies."""
    if not text:
        return 0
    wordish = len(text.split())
    charish = math.ceil(len(text) / 4)
    return max(1, max(wordish, charish))


def find_skill_files(skills_root: Path) -> list[Path]:
    return sorted(path for path in skills_root.glob("*/SKILL.md") if path.is_file())


def measure_sections(text: str) -> tuple[SectionMeasurement, ...]:
    sections: list[tuple[str, list[str]]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                if current_heading is not None:
                    sections.append((current_heading, current_lines))
                current_heading = heading
                current_lines = [line]
                continue
        if current_heading is not None:
            current_lines.append(line)

    if current_heading is not None:
        sections.append((current_heading, current_lines))

    measured = []
    for heading, lines in sections:
        section_text = "\n".join(lines)
        measured.append(
            SectionMeasurement(
                heading=heading,
                bytes=len(section_text.encode("utf-8")),
                lines=len(lines),
                estimated_tokens=estimate_tokens(section_text),
            )
        )
    return tuple(sorted(measured, key=lambda section: section.estimated_tokens, reverse=True)[:3])


def measure_skill(path: Path) -> SkillMeasurement:
    text = path.read_text(encoding="utf-8")
    return SkillMeasurement(
        path=path,
        bytes=len(text.encode("utf-8")),
        lines=len(text.splitlines()),
        estimated_tokens=estimate_tokens(text),
        status="measured",
        largest_sections=measure_sections(text),
    )


def format_measurement(measurement: SkillMeasurement, root: Path, warn_tokens: int | None) -> str:
    try:
        display_path = measurement.path.relative_to(root)
    except ValueError:
        display_path = measurement.path

    lines = [
        f"- path: {display_path}",
        f"  status: {measurement.status}",
        f"  bytes: {measurement.bytes}",
        f"  lines: {measurement.lines}",
        f"  estimated_tokens: {measurement.estimated_tokens}",
    ]
    if warn_tokens is not None and measurement.estimated_tokens > warn_tokens:
        lines.append(
            f"  WARNING: estimated_tokens {measurement.estimated_tokens} exceeds warning threshold {warn_tokens}"
        )
    if measurement.largest_sections:
        lines.append("  largest_sections:")
        for section in measurement.largest_sections:
            lines.extend(
                [
                    f"    - heading: {section.heading}",
                    f"      lines: {section.lines}",
                    f"      bytes: {section.bytes}",
                    f"      estimated_tokens: {section.estimated_tokens}",
                ]
            )
    else:
        lines.append("  largest_sections: unavailable")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        default=str(ROOT / "skills"),
        help="Directory containing canonical skill subdirectories.",
    )
    parser.add_argument(
        "--warn-tokens",
        type=int,
        default=None,
        help="Warn when a measured skill exceeds this estimated token count.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    skills_root = Path(args.skills_root)
    skill_files = find_skill_files(skills_root)
    if not skill_files:
        sys.stderr.write(f"error: no canonical skills found under {skills_root}\n")
        return 1

    measurements = [measure_skill(path) for path in skill_files]
    total_tokens = sum(measurement.estimated_tokens for measurement in measurements)
    total_bytes = sum(measurement.bytes for measurement in measurements)

    print("# Static Skill Cost")
    print()
    print(f"skills_root: {skills_root}")
    print(f"skills_measured: {len(measurements)}")
    print(f"total_bytes: {total_bytes}")
    print(f"total_estimated_tokens: {total_tokens}")
    print("token_estimate: approximate local estimate")
    print()
    print("skills:")
    for measurement in measurements:
        print(format_measurement(measurement, skills_root, args.warn_tokens))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
