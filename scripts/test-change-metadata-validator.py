#!/usr/bin/env python3
"""Fixture-driven tests for change metadata validation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import copy
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
import unittest
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-change-metadata.py"
QUERY_HELPER = ROOT / "scripts" / "query-change-record.py"
FIXTURES = ROOT / "tests" / "fixtures" / "change-metadata"
VALID_BASIC_FIXTURE = FIXTURES / "valid-basic" / "change.yaml"
CLEAN_RECEIPT_ROOT = (
    ROOT
    / "tests"
    / "fixtures"
    / "review-artifacts"
    / "valid-clean-receipt-root"
    / "change.yaml"
)
SUITE_NAME = "test-change-metadata-validator"


@dataclass(frozen=True)
class RunnerConfig:
    verbose: bool
    quiet: bool
    names: list[str]
    pattern: str | None


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_change_metadata", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load validate-change-metadata.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_validator(*targets: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *(str(target) for target in targets)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def run_query_change_record(
    repo_root: Path,
    change_id: str,
    query: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(QUERY_HELPER),
            change_id,
            query,
            "--repo-root",
            str(repo_root),
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def parse_runner_args(argv: list[str]) -> tuple[RunnerConfig | None, int]:
    if ("--verbose" in argv or "-v" in argv) and ("--quiet" in argv or "-q" in argv):
        print("error: --verbose and --quiet are mutually exclusive", file=sys.stderr)
        return None, 2

    verbose = False
    quiet = False
    names: list[str] = []
    pattern: str | None = None
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--verbose", "-v"):
            verbose = True
        elif arg in ("--quiet", "-q"):
            quiet = True
        elif arg == "-k":
            index += 1
            if index >= len(argv):
                print("error: -k requires a pattern", file=sys.stderr)
                return None, 2
            pattern = argv[index]
        elif arg.startswith("-"):
            print(f"error: unrecognized arguments: {arg}", file=sys.stderr)
            return None, 2
        else:
            names.append(arg)
        index += 1

    return RunnerConfig(verbose=verbose, quiet=quiet, names=names, pattern=pattern), 0


def build_test_suite(config: RunnerConfig) -> unittest.TestSuite:
    loader = unittest.defaultTestLoader
    previous_patterns = loader.testNamePatterns
    if config.pattern is not None:
        loader.testNamePatterns = [f"*{config.pattern}*"]
    try:
        if config.names:
            return loader.loadTestsFromNames(config.names, sys.modules[__name__])
        return loader.loadTestsFromModule(sys.modules[__name__])
    finally:
        loader.testNamePatterns = previous_patterns


def format_duration(seconds: float) -> str:
    return f"{seconds:.2f}s"


def short_test_id(test: unittest.case.TestCase) -> str:
    test_id = test.id()
    for prefix in (f"{Path(__file__).stem}.", "__main__."):
        if test_id.startswith(prefix):
            return test_id[len(prefix) :]
    return test_id


def failure_message(trace: str) -> str:
    for line in reversed(trace.strip().splitlines()):
        stripped = line.strip()
        if stripped:
            return stripped
    return "failure details unavailable"


def failure_location(trace: str) -> str | None:
    for line in trace.splitlines():
        match = re.search(r'File "([^"]+)", line ([0-9]+)', line)
        if not match:
            continue
        path = Path(match.group(1))
        try:
            display = path.relative_to(ROOT)
        except ValueError:
            display = path
        return f"{display}:{match.group(2)}"
    return None


def can_emit_scoped_rerun(test_id: str) -> bool:
    if "._FailedTest." in test_id:
        return False
    return bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+", test_id))


def format_failure_detail(test: unittest.case.TestCase, trace: str) -> str:
    test_id = short_test_id(test)
    lines = [
        "",
        f"FAILED {test_id}",
        f"  {failure_message(trace)}",
    ]
    location = failure_location(trace)
    if location:
        lines.append(f"  {location}")
    if can_emit_scoped_rerun(test_id):
        quoted = shlex.quote(test_id)
        if quoted == test_id:
            quoted = f'"{test_id}"'
        lines.append(f"  Re-run: python scripts/test-change-metadata-validator.py -k {quoted}")
    return "\n".join(lines)


def format_result(result: unittest.TestResult, elapsed: float) -> str:
    failed = len(result.failures) + len(result.errors)
    passed = result.testsRun - failed - len(result.skipped)
    duration = format_duration(elapsed)

    if result.testsRun == 0:
        return f"[FAIL] {SUITE_NAME}: 0 tests run; expected at least 1 selected test in {duration}"

    if result.wasSuccessful():
        return f"[PASS] {SUITE_NAME}: {passed} passed in {duration}"

    lines = [f"[FAIL] {SUITE_NAME}: {failed} failed, {max(passed, 0)} passed in {duration}"]
    for test, trace in [*result.failures, *result.errors]:
        lines.append(format_failure_detail(test, trace))
    return "\n".join(lines)


def add_output_contract_failure_fixture() -> None:
    if os.environ.get("RIGORLOOP_CHANGE_METADATA_FAILURE_FIXTURE") != "1":
        return

    def test_output_contract_fixture_failure(self: unittest.TestCase) -> None:
        self.fail("intentional output-contract failure")

    setattr(
        ChangeMetadataValidatorFixtureTests,
        "test_output_contract_fixture_failure",
        test_output_contract_fixture_failure,
    )


def main(argv: list[str]) -> int:
    add_output_contract_failure_fixture()
    config, parse_exit = parse_runner_args(argv)
    if config is None:
        return parse_exit

    suite = build_test_suite(config)
    if suite.countTestCases() == 0:
        print(f"[FAIL] {SUITE_NAME}: 0 tests run; expected at least 1 selected test in 0.00s")
        return 1

    if config.quiet:
        runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=0)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1

    stream = sys.stderr if config.verbose else StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2 if config.verbose else 1)
    started = time.monotonic()
    result = runner.run(suite)
    elapsed = time.monotonic() - started
    if not config.verbose:
        print(format_result(result, elapsed))
    return 0 if result.wasSuccessful() else 1


class ChangeMetadataValidatorFixtureTests(unittest.TestCase):
    def assertPathPasses(self, target: Path) -> None:
        result = run_validator(target)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected '{target}' to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )


    def assertPathFails(self, target: Path, expected_text: str) -> None:
        result = run_validator(target)
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"expected '{target}' to fail",
        )
        self.assertIn(expected_text, combined_output)


    def test_measurement_valid_fixture_passes(self) -> None:
        self.assertPathPasses(
            FIXTURES / "measurement-valid" / "validation-cache-measurement.yaml"
        )


    def test_measurement_invalid_fixtures_fail(self) -> None:
        cases = [
            (
                "measurement-invalid-missing-field",
                "summary: missing required measurement field",
            ),
            (
                "measurement-invalid-negative-count",
                "summary.eligible_commands: expected non-negative integer",
            ),
            (
                "measurement-invalid-count-drift",
                "summary.helper_invocations: expected cache_hits + actual_run_fallbacks",
            ),
            (
                "measurement-invalid-fallback-drift",
                "summary.actual_run_fallbacks: expected cache_misses + cache_disabled",
            ),
            (
                "measurement-invalid-cache-hit-rate",
                "summary.cache_hit_rate: expected cache_hits / helper_invocations",
            ),
            (
                "measurement-invalid-cache-hit-closeout",
                "summary.actual_runs: expected at least actual_run_fallbacks + closeout_actual_runs",
            ),
            (
                "measurement-invalid-missing-helper-invocations",
                "summary.helper_invocations: missing required field",
            ),
            (
                "measurement-invalid-missing-actual-run-fallbacks",
                "summary.actual_run_fallbacks: missing required field",
            ),
            (
                "measurement-invalid-missing-closeout-actual-runs",
                "summary.closeout_actual_runs: missing required field",
            ),
            (
                "measurement-invalid-closeout-cache-skip",
                "closeout.closeout_cache_skips: expected 0",
            ),
            (
                "measurement-invalid-workstream-b-state",
                "workstream_b_recommendation.state: expected one of",
            ),
            (
                "measurement-invalid-missing-rationale",
                "workstream_b_recommendation.rationale: expected string",
            ),
            (
                "measurement-invalid-unsafe-value",
                "measurement_window.description: unsafe machine-local path",
            ),
        ]
        for fixture, expected in cases:
            with self.subTest(fixture=fixture):
                self.assertPathFails(
                    FIXTURES / fixture / "validation-cache-measurement.yaml",
                    expected,
                )



class ExplicitRecordingMetadataTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="record-metadata-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / "docs/changes/example/change.json"
        self.path.parent.mkdir(parents=True)
        self.fixture = json.loads((ROOT / "tests/fixtures/rigorloop-records-v3/storage-safety.json").read_text())
        self.change = json.loads(self.fixture["request"]["writes"][0]["content"])

    def check(self, change=None):
        self.path.write_text(json.dumps(self.change if change is None else change) + "\n")
        return run_validator(self.path)

    def test_recording_v3_full_set_and_unknown_value_version_fail_closed(self):
        source = ROOT / "docs/design/record-format/examples/v3-complete-store"
        target = self.root / "docs/changes/example-change"
        for file in source.rglob("*.json"):
            destination = target / file.relative_to(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(file.read_bytes())
        manifest = target / "change.json"
        self.assertEqual(run_validator(manifest).returncode, 0)
        review = target / "reviews/final-code-review.json"
        value = json.loads(review.read_text())
        value["schema_version"] = 2
        review.write_text(json.dumps(value) + "\n")
        self.assertNotEqual(run_validator(manifest).returncode, 0)

    def test_recording_v3_manifest_dispatch_preserves_contract_and_unknown_value_rejects(self):
        self.path = self.path.with_name("change.json")
        f = json.loads((ROOT / "tests/fixtures/rigorloop-records-v3/records.json").read_text())
        self.change = f["change"]
        self.change.update(records=[], applicability=[], blockers=[])
        self.assertEqual(self.check().returncode, 0)
        self.change["contract"] = "unknown_value"
        self.assertNotEqual(self.check().returncode, 0)

    def test_explicit_recording_metadata_accepts_structure_without_stage_eligibility(self):
        self.change["activity"]["status"] = "completed"
        self.assertEqual(self.check().returncode, 0)

    def test_explicit_recording_unknown_value_and_mixed_contract_fail_closed(self):
        for field, value in (("contract", "unknown_value"), ("schema_version", 999),
                             ("lifecycle_contract", "compact-current-state-v1")):
            candidate = copy.deepcopy(self.change)
            candidate[field] = value
            self.assertNotEqual(self.check(candidate).returncode, 0)

    def test_explicit_recording_metadata_rejects_duplicate_keys_encoding_and_symlink(self):
        raw = json.dumps(self.change) + "\n"
        for content in (raw.rstrip("\n"), raw.replace('"schema_version": 3', '"schema_version": 3, "schema_version": 3', 1)):
            self.path.write_text(content)
            self.assertNotEqual(run_validator(self.path).returncode, 0)
            self.assertEqual(self.path.read_text(), content)
        outside = self.root / "outside.yaml"
        outside.write_text(raw)
        self.path.unlink()
        self.path.symlink_to(outside)
        self.assertNotEqual(run_validator(self.path).returncode, 0)
        self.assertEqual(outside.read_text(), raw)

    def test_explicit_recording_metadata_validates_registered_set_not_subject_freshness(self):
        path = "docs/changes/example/evidence.json"
        self.change["records"] = [{"path": path, "kind": "evidence"}]
        self.change["applicability"] = [{"path": path, "value": "stale", "actor": {"id": "author", "role": "implement"}, "reason": "Prior proof"}]
        self.assertNotEqual(self.check().returncode, 0)
        (self.root / path).write_text(json.dumps(self.fixture["evidence"]) + "\n")
        self.assertEqual(self.check().returncode, 0)
        (self.root / path).write_text("not a record\n")
        self.assertNotEqual(self.check().returncode, 0)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
