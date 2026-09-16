#!/usr/bin/env python3
"""Fixture-driven tests for validation selection."""

from __future__ import annotations

import json
import os
import re
import shutil
import signal
import shlex
import subprocess
import sys
import tempfile
import time
import unittest
from dataclasses import dataclass
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

SELECTOR = ROOT / "scripts" / "select-validation.py"
CI = ROOT / "scripts" / "ci.sh"
CHANGE_METADATA_TEST = ROOT / "tests" / "engineering" / "validation" / "test-change-metadata-validator.py"
README_VALIDATOR = ROOT / "scripts" / "validate-readme.py"

from lib.validation.validation_selection import (  # noqa: E402
    CHECK_CATALOG, MODE_CHECK_IDS,
    catalog_command,
    build_repository_preflight_context,
    SelectionRequest,
    normalize_path,
    select_validation,
)

from selection_test_helpers import (
    SelectionFixtures,
    run_selector,
    run_ci,
    run_ci_bytes,
    run_change_metadata_test,
    parse_stdout,
    selected_ids,
    allocated_workers,
    EXPECTED_CATALOG,
    ADAPTER_REGRESSION_COMMAND,
    CHANGE_METADATA_PASSING_TEST,
    CHANGE_METADATA_FAILING_TEST,
)
from selection_contract_tests import SelectionContractChecks
from selection_git_tests import SelectionGitChecks
from selection_cli_tests import SelectionCliChecks


SUITE_NAME = "test-select-validation"


@dataclass(frozen=True)
class RunnerConfig:
    verbose: bool
    quiet: bool
    names: list[str]
    pattern: str | None


def short_test_id(test: unittest.case.TestCase) -> str:
    test_id = test.id()
    module_prefix = f"{Path(__file__).stem}."
    main_prefix = "__main__."
    if test_id.startswith(module_prefix):
        return test_id[len(module_prefix) :]
    if test_id.startswith(main_prefix):
        return test_id[len(main_prefix) :]
    return test_id


def parse_runner_args(argv: list[str]) -> tuple[RunnerConfig | None, int]:
    if ("--verbose" in argv or "-v" in argv) and ("--quiet" in argv or "-q" in argv):
        print(
            "error: --verbose and --quiet are mutually exclusive",
            file=sys.stderr,
        )
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
        lines.append(f"  Re-run: python tests/engineering/validation/test-select-validation.py {quoted}")
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


def run_script_tests(argv: list[str]) -> int:
    config, parse_status = parse_runner_args(argv)
    if config is None:
        return parse_status

    suite = build_test_suite(config)
    stream = sys.stdout if config.verbose else StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2 if config.verbose else 1)
    started = time.perf_counter()
    result = runner.run(suite)
    elapsed = time.perf_counter() - started

    if result.testsRun == 0:
        if not config.quiet:
            print(format_result(result, elapsed))
        else:
            print(format_result(result, elapsed), file=sys.stderr)
        return 1

    if config.verbose:
        return 0 if result.wasSuccessful() else 1

    if result.wasSuccessful():
        if not config.quiet:
            print(format_result(result, elapsed))
        return 0

    print(format_result(result, elapsed))
    return 1


class ScriptOutputFixtureTests(unittest.TestCase):
    def fixture_contract_failure(self) -> None:
        self.fail("script output contract fixture failure")


class ScriptOutputContractTests(unittest.TestCase):
    """Acceptance coverage for the approved script-output contract."""

    PASSING_TEST = "ValidationSelectionTests.test_catalog_matches_v1_contract"
    FAILING_TEST = "ScriptOutputFixtureTests.fixture_contract_failure"
    SUITE = "test-select-validation"
    PASS_SUMMARY = re.compile(r"^\[PASS\] test-select-validation: [1-9][0-9]* passed in \d+(?:\.\d+)?s$")
    FAIL_SUMMARY = re.compile(
        r"^\[FAIL\] test-select-validation: [1-9][0-9]* failed, [0-9]+ passed in \d+(?:\.\d+)?s"
    )

    def run_runner(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def combined_output(self, result: subprocess.CompletedProcess[str]) -> str:
        return result.stdout + result.stderr

    def test_output_contract_default_success_is_single_summary_line(self) -> None:
        result = self.run_runner(self.PASSING_TEST)

        self.assertEqual(result.returncode, 0, msg=self.combined_output(result))
        stdout_lines = result.stdout.splitlines()
        self.assertEqual(len(stdout_lines), 1, msg=self.combined_output(result))
        self.assertRegex(stdout_lines[0], self.PASS_SUMMARY)
        self.assertNotIn(self.PASSING_TEST, self.combined_output(result))
        self.assertEqual(result.stderr, "")

    def test_output_contract_default_failure_expands_failures_only(self) -> None:
        result = self.run_runner(self.PASSING_TEST, self.FAILING_TEST)
        output = self.combined_output(result)

        self.assertEqual(result.returncode, 1, msg=output)
        first_line = next(line for line in output.splitlines() if line.strip())
        self.assertRegex(first_line, self.FAIL_SUMMARY)
        self.assertIn(self.FAILING_TEST, output)
        self.assertIn("script output contract fixture failure", output)
        self.assertIn("tests/engineering/validation/test-select-validation.py", output)
        self.assertNotIn(f"{self.PASSING_TEST}) ... ok", output)

    def test_output_contract_verbose_success_preserves_full_pass_detail(self) -> None:
        for flag in ("--verbose", "-v"):
            with self.subTest(flag=flag):
                result = self.run_runner(flag, self.PASSING_TEST)
                output = self.combined_output(result)

                self.assertEqual(result.returncode, 0, msg=output)
                self.assertIn(self.PASSING_TEST, output)
                self.assertIn("ok", output)

    def test_output_contract_quiet_success_is_silent(self) -> None:
        for flag in ("--quiet", "-q"):
            with self.subTest(flag=flag):
                result = self.run_runner(flag, self.PASSING_TEST)

                self.assertEqual(result.returncode, 0, msg=self.combined_output(result))
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")

    def test_output_contract_quiet_failure_remains_actionable(self) -> None:
        result = self.run_runner("--quiet", self.PASSING_TEST, self.FAILING_TEST)
        output = self.combined_output(result)

        self.assertEqual(result.returncode, 1, msg=output)
        self.assertIn("[FAIL] test-select-validation:", output)
        self.assertIn(self.FAILING_TEST, output)
        self.assertIn("script output contract fixture failure", output)
        self.assertIn("tests/engineering/validation/test-select-validation.py", output)
        self.assertNotIn("[PASS]", output)

    def test_output_contract_conflicting_output_flags_fail_before_tests_run(self) -> None:
        for args in (("--verbose", "--quiet"), ("--quiet", "--verbose")):
            with self.subTest(args=args):
                result = self.run_runner(*args, self.PASSING_TEST)

                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("--verbose", result.stderr)
                self.assertIn("--quiet", result.stderr)
                self.assertNotIn("[PASS]", result.stderr)
                self.assertNotIn("[FAIL]", result.stderr)
                self.assertNotIn("[SKIP]", result.stderr)
                self.assertNotIn("Ran 1 test", result.stderr)
                self.assertNotIn(self.PASSING_TEST, result.stderr)

    def test_output_contract_zero_executed_tests_fail_with_summary(self) -> None:
        result = self.run_runner("-k", "definitely_no_script_output_tests")
        output = self.combined_output(result)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[FAIL] test-select-validation:", output)
        self.assertIn("0 tests", output)
        self.assertIn("expected at least 1", output)

    def test_output_contract_reliable_failure_includes_scoped_rerun(self) -> None:
        result = self.run_runner(self.FAILING_TEST)
        output = self.combined_output(result)

        self.assertEqual(result.returncode, 1, msg=output)
        commands = [line.strip().removeprefix("Re-run: ")
                    for line in output.splitlines()
                    if line.strip().startswith("Re-run: ")]
        self.assertEqual(len(commands), 1, output)

        rerun = subprocess.run(shlex.split(commands[0]), cwd=ROOT,
                               capture_output=True, text=True)

        rerun_output = self.combined_output(rerun)
        self.assertEqual(rerun.returncode, 1, rerun_output)
        self.assertIn("[FAIL] test-select-validation: 1 failed, 0 passed", rerun_output)
        self.assertIn(f"FAILED {self.FAILING_TEST}", rerun_output)
        self.assertIn("script output contract fixture failure", rerun_output)
        self.assertNotIn("0 tests run", rerun_output)

    def test_output_contract_unreliable_failure_omits_misleading_scoped_rerun(self) -> None:
        result = self.run_runner("NoSuchTest")
        output = self.combined_output(result)

        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('-k "NoSuchTest"', output)

    def test_output_contract_json_support_is_not_added_in_first_slice(self) -> None:
        result = self.run_runner("--json")

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(result.stdout.lstrip().startswith("{"))
        self.assertIn("--json", self.combined_output(result))


class ValidationSelectionTests(SelectionContractChecks, SelectionGitChecks,
                               SelectionCliChecks, SelectionFixtures, unittest.TestCase):
    """Stable public selectors over responsibility-owned test groups."""
    maxDiff = None
    root_preflight_context = build_repository_preflight_context(ROOT)


if __name__ == "__main__":
    raise SystemExit(run_script_tests(sys.argv[1:]))
