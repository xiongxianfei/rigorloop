#!/usr/bin/env python3
"""Run release token-cost benchmarks against a temporary public-skill fixture."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CODEX_SKILL_SOURCE = "dist/adapters/codex/.agents/skills/"


@dataclass(frozen=True)
class Benchmark:
    id: str
    prompt: Path
    fixture: Path


def load_yaml(path: Path) -> Any:
    validator_path = ROOT / "scripts" / "validate-token-cost-report.py"
    spec = importlib.util.spec_from_file_location("token_cost_validator", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load token-cost YAML parser")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.load_yaml(path)


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return ROOT / path


def display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_skill_source(path_text: str) -> str:
    return path_text.rstrip("/") + "/"


def default_temp_root() -> Path:
    if os.environ.get("CI") and os.environ.get("RUNNER_TEMP"):
        return Path(os.environ["RUNNER_TEMP"])
    return Path(tempfile.gettempdir())


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def load_benchmarks(suite_path: Path, fixture_override: Path | None) -> list[Benchmark]:
    suite = load_yaml(suite_path)
    if not isinstance(suite, dict):
        raise ValueError("suite manifest must be a mapping")
    prompts = suite.get("prompts")
    if not isinstance(prompts, list) or not prompts:
        raise ValueError("suite manifest must contain prompt entries")
    suite_root = suite_path.parent
    default_fixture = fixture_override or repo_path(suite_root / str(suite.get("fixture", "")))
    benchmarks: list[Benchmark] = []
    for entry in prompts:
        if not isinstance(entry, dict):
            raise ValueError("suite prompt entry must be a mapping")
        benchmark_id = entry.get("id")
        prompt = entry.get("path")
        if not isinstance(benchmark_id, str) or not benchmark_id:
            raise ValueError("suite prompt entry is missing id")
        if not isinstance(prompt, str) or not prompt:
            raise ValueError(f"{benchmark_id}: missing prompt path")
        fixture = fixture_override or repo_path(suite_root / str(entry.get("fixture", "")))
        if not fixture.exists():
            fixture = default_fixture
        benchmarks.append(
            Benchmark(
                id=benchmark_id,
                prompt=repo_path(suite_root / prompt),
                fixture=fixture,
            )
        )
    return benchmarks


def prepare_fixture(source_fixture: Path, skill_source: Path, temp_root: Path, release: str) -> Path:
    if not source_fixture.is_dir():
        raise ValueError(f"fixture does not exist: {display_path(source_fixture)}")
    if not skill_source.is_dir():
        raise ValueError(f"public Codex skill source does not exist: {display_path(skill_source)}")
    temp_root.mkdir(parents=True, exist_ok=True)
    run_dir = temp_root / f"rigorloop-token-bench-{release}-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    shutil.copytree(source_fixture, run_dir)
    target = run_dir / ".agents" / "skills"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill_source, target, dirs_exist_ok=True)
    return run_dir


def write_dry_run_jsonl(path: Path, benchmark_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    records = [
        {
            "usage": {
                "input_tokens": 0,
                "cached_input_tokens": 0,
                "output_tokens": 0,
                "reasoning_output_tokens": 0,
            }
        },
        {
            "tool": "dry-run",
            "args": {"cmd": f"token-cost dry-run {benchmark_id}"},
            "output": "",
        },
    ]
    path.write_text(
        "".join(json.dumps(record, separators=(",", ":")) + "\n" for record in records),
        encoding="utf-8",
    )


def run_analyzer(jsonl: Path, analysis: Path, benchmark_id: str) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "analyze-codex-jsonl.py"),
        str(jsonl),
        "--summary-output",
        str(analysis),
        "--run-id",
        benchmark_id,
    ]
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def run_benchmark(
    benchmark: Benchmark,
    *,
    temp_fixture: Path,
    output_dir: Path,
    dry_run: bool,
) -> tuple[Path, Path]:
    prompt_text = benchmark.prompt.read_text(encoding="utf-8")
    jsonl = output_dir / f"{benchmark.id}-run1.jsonl"
    analysis = output_dir / f"{benchmark.id}-run1.analysis.yaml"
    output_dir.mkdir(parents=True, exist_ok=True)
    codex_command = ["codex", "exec", "--json", "--ephemeral", "--skip-git-repo-check"]
    command_display = " ".join(codex_command)
    if dry_run:
        write_dry_run_jsonl(jsonl, benchmark.id)
    else:
        print(f"codex_command: {command_display} <{display_path(benchmark.prompt)}>")
        with jsonl.open("w", encoding="utf-8") as handle:
            result = subprocess.run(
                [*codex_command, prompt_text],
                cwd=temp_fixture,
                text=True,
                stdout=handle,
                stderr=subprocess.PIPE,
                check=False,
            )
        if result.returncode != 0:
            raise RuntimeError(f"{benchmark.id}: codex exec failed: {result.stderr.strip()}")
    if dry_run:
        print(f"codex_command: {command_display} <{display_path(benchmark.prompt)}>")

    analyzer_result = run_analyzer(jsonl, analysis, benchmark.id)
    if analyzer_result.returncode != 0:
        raise RuntimeError(f"{benchmark.id}: analyzer failed: {analyzer_result.stderr.strip()}")
    print(
        "analyzer_command: "
        f"python scripts/analyze-codex-jsonl.py {display_path(jsonl)} "
        f"--summary-output {display_path(analysis)} --run-id {benchmark.id}"
    )
    return jsonl, analysis


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", required=True, help="Release version for output paths.")
    parser.add_argument("--suite", default="benchmarks/token-cost/manifest.yaml")
    parser.add_argument("--tool", default="codex", choices=["codex"])
    parser.add_argument("--fixture", help="Override fixture source path.")
    parser.add_argument("--temp-root", help="Temporary root directory.")
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--keep-failed-temp", action="store_true")
    parser.add_argument("--output-dir", help="Run output directory.")
    parser.add_argument("--skill-source", default=PUBLIC_CODEX_SKILL_SOURCE)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Prepare fixture and write synthetic JSONL instead of invoking Codex.",
    )
    args = parser.parse_args(argv)

    skill_source_text = normalize_skill_source(args.skill_source)
    if skill_source_text != PUBLIC_CODEX_SKILL_SOURCE:
        sys.stderr.write(f"error: skill source must be {PUBLIC_CODEX_SKILL_SOURCE}\n")
        return 1

    suite = repo_path(args.suite)
    output_dir = repo_path(args.output_dir or f"docs/reports/token-cost/runs/{args.release}")
    temp_root = Path(args.temp_root) if args.temp_root else default_temp_root()
    if is_relative_to(temp_root, ROOT):
        sys.stderr.write("error: temporary root must be outside the repository\n")
        return 1
    fixture_override = repo_path(args.fixture) if args.fixture else None
    temp_fixture: Path | None = None
    try:
        benchmarks = load_benchmarks(suite, fixture_override)
        if not benchmarks:
            raise ValueError("no benchmarks found")
        fixture = benchmarks[0].fixture
        skill_source = repo_path(skill_source_text)
        temp_fixture = prepare_fixture(fixture, skill_source, temp_root, args.release)
        print(f"release: {args.release}")
        print(f"tool: {args.tool}")
        print(f"dry_run: {'true' if args.dry_run else 'false'}")
        print(f"suite: {display_path(suite)}")
        print(f"fixture: {display_path(fixture)}")
        print(f"skill_source: {skill_source_text}")
        print(f"temp_policy: {'runner-temp' if os.environ.get('CI') else 'system-temp'}")
        print(f"output_dir: {display_path(output_dir)}")
        print(f"temp_fixture: {temp_fixture}")
        for benchmark in benchmarks:
            jsonl, analysis = run_benchmark(
                benchmark,
                temp_fixture=temp_fixture,
                output_dir=output_dir,
                dry_run=args.dry_run,
            )
            print(f"run: {benchmark.id} jsonl={display_path(jsonl)} analysis={display_path(analysis)}")
    except Exception as exc:
        sys.stderr.write(f"error: {exc}\n")
        if temp_fixture and temp_fixture.exists() and not args.keep_failed_temp:
            shutil.rmtree(temp_fixture)
        elif temp_fixture and temp_fixture.exists():
            sys.stderr.write(f"kept failed temp fixture: {temp_fixture}\n")
        return 1
    if temp_fixture and temp_fixture.exists() and not args.keep_temp:
        shutil.rmtree(temp_fixture)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
