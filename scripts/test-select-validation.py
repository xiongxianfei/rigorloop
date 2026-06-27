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

import yaml


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / "scripts" / "select-validation.py"
CI = ROOT / "scripts" / "ci.sh"
BROAD_SMOKE_CLASSIFICATION_VALIDATOR = ROOT / "scripts" / "validate-broad-smoke-classification.py"
CHANGE_METADATA_TEST = ROOT / "scripts" / "test-change-metadata-validator.py"
README_VALIDATOR = ROOT / "scripts" / "validate-readme.py"
BROAD_SMOKE_CLASSIFICATION = (
    ROOT
    / "docs"
    / "changes"
    / "2026-06-26-preflight-first-validation-runtime-optimization"
    / "broad-smoke-child-classification.md"
)
sys.path.insert(0, str(ROOT / "scripts"))

from validation_selection import (  # noqa: E402
    CHECK_CATALOG,
    EvidenceClassRegistration,
    build_repository_preflight_context,
    SelectionRequest,
    normalize_path,
    select_validation,
    validate_evidence_class_registry,
)

ADAPTER_REGRESSION_COMMAND = (
    "python scripts/test-adapter-distribution.py "
    "AdapterDistributionTests.test_adapter_generation_creates_independent_packages_and_thin_entrypoints "
    "AdapterDistributionTests.test_adapter_generation_drift_check_detects_stale_and_unexpected_files "
    "AdapterDistributionTests.test_validate_adapters_cli_rejects_retired_repository_output "
    "AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives "
    "AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root "
    "AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata"
)

EXPECTED_CATALOG = {
    "skills.validate": "python scripts/validate-skills.py",
    "skills.regression": "python scripts/test-skill-validator.py",
    "skills.generation_regression": "python scripts/test-build-skills.py",
    "skills.drift": "python scripts/build-skills.py --check",
    "adapters.regression": ADAPTER_REGRESSION_COMMAND,
    "adapters.drift": "python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives",
    "adapters.validate": "python scripts/test-adapter-distribution.py AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root",
    "review_artifacts.regression": "python scripts/test-review-artifact-validator.py",
    "review_artifacts.validate": "python scripts/validate-review-artifacts.py <change-root>...",
    "artifact_lifecycle.regression": "python scripts/test-artifact-lifecycle-validator.py",
    "artifact_lifecycle.validate": "python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <path>...",
    "validation_cache.regression": "python scripts/test-validation-cache.py",
    "change_metadata.regression": "python scripts/test-change-metadata-validator.py",
    "change_metadata.validate": "python scripts/validate-change-metadata.py <change-yaml>...",
    "change_record_query.regression": "python scripts/test-query-change-record.py",
    "release.validate": "python scripts/validate-release-ci.py --version <version>",
    "readme.validate": "python scripts/validate-readme.py README.md",
    "readme.vision_markers": "python scripts/validate-readme.py README.md --vision-markers",
    "guide_system.regression": "python scripts/test-guide-system-validator.py",
    "guide_system.validate": "python scripts/validate-guide-system.py",
    "selector.regression": "python scripts/test-select-validation.py",
    "requirement_fidelity.spec_reads": (
        "python scripts/test-fidelity-gate-spec-reads.py "
        "--review-set tests/fixtures/requirement-fidelity-gate/representative-reviews "
        "--max-bytes-per-clause 4096 --assert-no-broad-reads"
    ),
    "token_cost.regression": "python scripts/test-token-cost-measurement.py",
    "token_cost.report_regression": "python scripts/test-token-cost-report-validation.py",
    "token_cost.report_validate": "python scripts/validate-token-cost-report.py <report-yaml>...",
    "broad_smoke.repo": "bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped",
    "rigorloop_cli.test": "npm test --prefix packages/rigorloop",
    "npm_package_publication.test": "python scripts/test-npm-package-publication.py",
}

CI_SELECTED_POLICY_EXCEPTION = {
    "reason": "selected-CI already captures child stdout/stderr and prints successful output only under --verbose",
    "spec": "specs/script-output-optimization.md R29-R31, R51-R52",
    "test": "specs/script-output-optimization.test.md TSRO-020, TSRO-026",
}

BROAD_SMOKE_CHECK_IDS_BY_RUN_CHECK_LABEL = {
    "Validate canonical skills": "broad_smoke.skills.validate",
    "Run skill validator fixtures": "broad_smoke.skills.regression",
    "Run local skill mirror generation fixtures": "broad_smoke.skills.generation_regression",
    "Validate generated skill mirror output": "broad_smoke.skills.drift",
    "Run adapter distribution fixtures": "broad_smoke.adapters.regression",
    "Build generated adapter archives": "broad_smoke.adapters.build_archives",
    "Validate generated adapter archives": "broad_smoke.adapters.validate_archives",
    "Run change metadata validator fixtures": "broad_smoke.change_metadata.regression",
    "Run artifact lifecycle validator fixtures": "broad_smoke.artifact_lifecycle.regression",
    "Run review artifact validator fixtures": "broad_smoke.review_artifacts.regression",
    "$review_artifact_label": "broad_smoke.review_artifacts.changed_roots",
    "$artifact_lifecycle_label": "broad_smoke.artifact_lifecycle.scoped",
}
BROAD_SMOKE_REQUIRED_CLASSIFICATION_FIELDS = (
    "Check ID",
    "Command",
    "Reads",
    "Writes",
    "Temp roots",
    "Shared outputs",
    "Network use",
    "CPU/I/O expectations",
    "Nested parallelism risk",
    "Output-order risk",
    "Failure-output dependency",
    "Parallel-safe candidate",
    "Classification confidence",
)
NON_CANDIDATE_VALUES = {"no", "not-approved", "blocked"}
BROAD_SMOKE_PARALLEL_CLASSIFICATION = (
    ROOT
    / "docs"
    / "changes"
    / "2026-06-27-broad-smoke-safe-parallelism"
    / "broad-smoke-child-classification.yaml"
)
BROAD_SMOKE_PARALLEL_BASELINE = (
    ROOT
    / "docs"
    / "changes"
    / "2026-06-27-broad-smoke-safe-parallelism"
    / "broad-smoke-parallelism-baseline.yaml"
)

VALIDATION_PRODUCER_PATTERN = re.compile(
    r"\bpython\s+scripts/(?:test|validate|build)-[\w-]+\.py\b"
)
CHANGE_METADATA_PASSING_TEST = "ChangeMetadataValidatorFixtureTests.test_valid_basic_fixture_passes"
CHANGE_METADATA_FAILING_TEST = "ChangeMetadataValidatorFixtureTests.test_output_contract_fixture_failure"


def run_selector(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SELECTOR), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def run_ci(
    *args: str,
    env: dict[str, str] | None = None,
    script: Path = CI,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[str]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    return subprocess.run(
        ["bash", str(script), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=run_env,
    )


def run_ci_bytes(
    *args: str,
    env: dict[str, str] | None = None,
    script: Path = CI,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[bytes]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    return subprocess.run(
        ["bash", str(script), *args],
        cwd=cwd,
        capture_output=True,
        env=run_env,
    )


def run_change_metadata_test(
    *args: str,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    return subprocess.run(
        [sys.executable, str(CHANGE_METADATA_TEST), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=run_env,
    )


def parse_stdout(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:  # pragma: no cover - failure helper
        raise AssertionError(f"selector stdout was not JSON:\n{result.stdout}") from exc


def selected_ids(result: dict[str, object]) -> set[str]:
    return {check["id"] for check in result["selected_checks"]}  # type: ignore[index]


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
        lines.append(f"  Re-run: python scripts/test-select-validation.py -k {quoted}")
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
        self.assertIn("scripts/test-select-validation.py", output)
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
        self.assertIn("scripts/test-select-validation.py", output)
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
        self.assertIn(
            'Re-run: python scripts/test-select-validation.py -k "ScriptOutputFixtureTests.fixture_contract_failure"',
            output,
        )

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


class ValidationSelectionTests(unittest.TestCase):
    maxDiff = None
    root_preflight_context = build_repository_preflight_context(ROOT)

    def addCleanupTree(self, path: Path) -> None:
        self.addCleanup(lambda: shutil.rmtree(path, ignore_errors=True))

    def make_git_repo(self) -> Path:
        repo = Path(tempfile.mkdtemp(prefix="validation-selection-git-"))
        self.addCleanupTree(repo)
        subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "config", "user.email", "tester@example.com"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture Tester"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        (repo / "skills" / "workflow").mkdir(parents=True)
        (repo / "skills" / "workflow" / "SKILL.md").write_text("# Workflow\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "baseline"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        return repo

    def git_output(self, repo: Path, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def write_selector_fixture(self, payload: object | str) -> Path:
        fixture = Path(tempfile.mkdtemp(prefix="validation-selection-fixture-")) / "selector.json"
        self.addCleanupTree(fixture.parent)
        if isinstance(payload, str):
            fixture.write_text(payload, encoding="utf-8")
        else:
            fixture.write_text(json.dumps(payload), encoding="utf-8")
        return fixture

    def minimal_selector_payload(
        self,
        *,
        mode: str = "explicit",
        status: str = "ok",
        selected_checks: list[dict[str, object]] | None = None,
        blocking_results: list[dict[str, str]] | None = None,
    ) -> dict[str, object]:
        return {
            "mode": mode,
            "status": status,
            "changed_paths": [],
            "classified_paths": [],
            "unclassified_paths": [],
            "selected_checks": selected_checks or [],
            "affected_roots": [],
            "broad_smoke_required": False,
            "broad_smoke": {"required": False, "sources": []},
            "blocking_results": blocking_results or [],
            "preflight_results": [],
            "rationale": [],
        }

    def make_ci_workspace(self) -> Path:
        workspace = Path(tempfile.mkdtemp(prefix="validation-selection-ci-workspace-"))
        self.addCleanupTree(workspace)
        (workspace / "scripts").mkdir()
        shutil.copy2(CI, workspace / "scripts" / "ci.sh")
        shutil.copy2(ROOT / "scripts" / "validation_selection.py", workspace / "scripts" / "validation_selection.py")
        return workspace

    def make_broad_smoke_workspace(self, *, failing_child: str | None = None) -> Path:
        workspace = self.make_ci_workspace()
        child_scripts = [
            "scripts/validate-skills.py",
            "scripts/test-skill-validator.py",
            "scripts/test-build-skills.py",
            "scripts/build-skills.py",
            "scripts/test-adapter-distribution.py",
            "scripts/build-adapters.py",
            "scripts/validate-adapters.py",
            "scripts/test-change-metadata-validator.py",
            "scripts/test-artifact-lifecycle-validator.py",
            "scripts/test-review-artifact-validator.py",
            "scripts/validate-review-artifacts.py",
            "scripts/validate-artifact-lifecycle.py",
        ]
        for relative_path in child_scripts:
            name = Path(relative_path).name
            exit_code = 7 if relative_path == failing_child else 0
            self.write_fake_script(
                workspace,
                relative_path,
                f"""
import sys

print("{name} STDOUT marker", flush=True)
print("{name} STDERR marker", file=sys.stderr)
raise SystemExit({exit_code})
""".lstrip(),
            )

        change_yaml = workspace / "docs" / "changes" / "example" / "change.yaml"
        change_yaml.parent.mkdir(parents=True)
        change_yaml.write_text("change_id: example\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=workspace, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "config", "user.email", "tester@example.com"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture Tester"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(["git", "add", "."], cwd=workspace, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "baseline"],
            cwd=workspace,
            check=True,
            capture_output=True,
            text=True,
        )
        change_yaml.write_text("change_id: example\nstatus: draft\n", encoding="utf-8")
        return workspace

    def write_fake_script(self, workspace: Path, relative_path: str, body: str) -> Path:
        script = workspace / relative_path
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text(body, encoding="utf-8")
        return script

    def write_active_counter_script(
        self,
        workspace: Path,
        relative_path: str,
        check_name: str,
        *,
        sleep_seconds: float = 0.2,
        exit_code: int = 0,
    ) -> Path:
        return self.write_fake_script(
            workspace,
            relative_path,
            f"""
import fcntl
import os
import time
from pathlib import Path

active_dir = Path(os.environ["ACTIVE_DIR"])
active_dir.mkdir(parents=True, exist_ok=True)
name = "{check_name}"
lock_path = active_dir / "lock"
active_path = active_dir / f"active-{{name}}"
max_path = active_dir / "max-active.txt"
events_path = active_dir / "events.txt"

with lock_path.open("a+", encoding="utf-8") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    active_path.write_text("active", encoding="utf-8")
    active_count = len(list(active_dir.glob("active-*")))
    previous_max = int(max_path.read_text(encoding="utf-8")) if max_path.exists() else 0
    if active_count > previous_max:
        max_path.write_text(str(active_count), encoding="utf-8")
    with events_path.open("a", encoding="utf-8") as events:
        events.write(f"{{name}} start {{active_count}}\\n")
    fcntl.flock(lock, fcntl.LOCK_UN)

time.sleep({sleep_seconds!r})

with lock_path.open("a+", encoding="utf-8") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    active_path.unlink(missing_ok=True)
    with events_path.open("a", encoding="utf-8") as events:
        events.write(f"{{name}} end\\n")
    fcntl.flock(lock, fcntl.LOCK_UN)

print(f"{{name}} done")
raise SystemExit({exit_code})
""".lstrip(),
        )

    def read_max_active(self, active_dir: Path) -> int:
        max_path = active_dir / "max-active.txt"
        if not max_path.exists():
            return 0
        return int(max_path.read_text(encoding="utf-8"))

    def selected_check(self, check_id: str, command: str, **extra: object) -> dict[str, object]:
        check: dict[str, object] = {
            "id": check_id,
            "command": command,
            "reason": f"{check_id} fixture",
        }
        check.update(extra)
        return check

    def run_workspace_ci(
        self,
        workspace: Path,
        fixture: Path,
        *args: str,
        text: bool = True,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
        run_env = {"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)}
        if env:
            run_env.update(env)
        if text:
            return run_ci(
                *args,
                env=run_env,
                script=workspace / "scripts" / "ci.sh",
                cwd=workspace,
            )
        return run_ci_bytes(
            *args,
            env=run_env,
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )

    def extract_ci_functions(self, ci_text: str) -> dict[str, str]:
        functions: dict[str, str] = {}
        for match in re.finditer(
            r"(?ms)^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\(\) \{\n(?P<body>.*?)\n\}",
            ci_text,
        ):
            functions[match.group("name")] = match.group("body")
        return functions

    def assert_run_check_captures_output(self, ci_text: str) -> None:
        match = re.search(r"run_check\(\) \{\n(?P<body>.*?)\n\}", ci_text, re.DOTALL)
        self.assertIsNotNone(match)
        assert match is not None
        body = match.group("body")
        self.assertIn('"$@" 2>&1', body)
        self.assertIn("Captured output:", body)
        self.assertIn("verbose", body)
        self.assertNotRegex(body, r'(?m)^\s*"\$@"\s*$')

    def assert_selected_ci_policy_exception_is_documented(self) -> None:
        for field in ("reason", "spec", "test"):
            self.assertIn(field, CI_SELECTED_POLICY_EXCEPTION)
            self.assertTrue(CI_SELECTED_POLICY_EXCEPTION[field])
        self.assertIn("selected-CI", CI_SELECTED_POLICY_EXCEPTION["reason"])
        self.assertIn("specs/script-output-optimization.md", CI_SELECTED_POLICY_EXCEPTION["spec"])
        self.assertIn("specs/script-output-optimization.test.md", CI_SELECTED_POLICY_EXCEPTION["test"])

    def assert_ci_mode_dispatch_has_documented_policies(self, ci_text: str) -> None:
        self.assertRegex(
            ci_text,
            r"(?ms)^case \"\$mode\" in.*local\|explicit\|pr\|main\|release\)\n\s*run_selected_mode",
        )
        self.assertRegex(
            ci_text,
            r"(?ms)^case \"\$mode\" in.*broad-smoke\)\n\s*run_broad_smoke",
        )
        self.assert_selected_ci_policy_exception_is_documented()

    def producer_line_uses_capture_helper(self, lines: list[str], index: int) -> bool:
        if re.search(r"\brun_check\b", lines[index]):
            return True

        current = index - 1
        while current >= 0 and lines[current].rstrip().endswith("\\"):
            if re.search(r"\brun_check\b", lines[current]):
                return True
            current -= 1
        return False

    def producer_line_is_command_array_assignment(self, lines: list[str], index: int) -> bool:
        inside_array_assignment = False
        for current, line in enumerate(lines[: index + 1]):
            stripped = line.strip()
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=\($", stripped):
                inside_array_assignment = True
            if current == index:
                return inside_array_assignment
            if inside_array_assignment and stripped == ")":
                inside_array_assignment = False
        return False

    def assert_ci_orchestration_modes_have_capture_policy(self, ci_text: str) -> None:
        functions = self.extract_ci_functions(ci_text)
        self.assertIn("run_broad_smoke", functions)

        for name, body in functions.items():
            if not name.startswith("run_") or name == "run_check":
                continue

            direct_stream = re.search(r'(?m)^\s*"\$@"\s*$', body)
            if direct_stream:
                raise AssertionError(
                    f"scripts/ci.sh mode '{name.removeprefix('run_')}' streams child command directly"
                )

            lines = body.splitlines()
            for index, line in enumerate(lines):
                if not VALIDATION_PRODUCER_PATTERN.search(line):
                    continue
                if self.producer_line_is_command_array_assignment(lines, index):
                    continue
                if self.producer_line_uses_capture_helper(lines, index):
                    continue
                raise AssertionError(
                    f"scripts/ci.sh mode '{name.removeprefix('run_')}' runs validation producer "
                    f"without capture policy: {line.strip()}"
                )

    def assert_ci_wrapper_consistency_guard_passes(self, ci_text: str) -> None:
        self.assert_run_check_captures_output(ci_text)
        self.assert_ci_mode_dispatch_has_documented_policies(ci_text)
        self.assert_ci_orchestration_modes_have_capture_policy(ci_text)

    def assert_ci_wrapper_consistency_guard_fails(
        self,
        ci_text: str,
        expected_message: str | None = None,
    ) -> None:
        context = (
            self.assertRaisesRegex(AssertionError, expected_message)
            if expected_message is not None
            else self.assertRaises(AssertionError)
        )
        with context:
            self.assert_ci_wrapper_consistency_guard_passes(ci_text)

    def extract_broad_smoke_run_check_ids(self, ci_text: str) -> list[str]:
        functions = self.extract_ci_functions(ci_text)
        self.assertIn("run_broad_smoke", functions)
        labels: list[str] = []
        for match in re.finditer(
            r"(?m)^\s*run_check\s+(?P<label>\"[^\"]+\"|\$[A-Za-z_][A-Za-z0-9_]*)",
            functions["run_broad_smoke"],
        ):
            label = match.group("label")
            if label.startswith('"') and label.endswith('"'):
                label = label[1:-1]
            labels.append(label)

        check_ids: list[str] = []
        for label in labels:
            self.assertIn(label, BROAD_SMOKE_CHECK_IDS_BY_RUN_CHECK_LABEL)
            check_ids.append(BROAD_SMOKE_CHECK_IDS_BY_RUN_CHECK_LABEL[label])
        return check_ids

    def parse_broad_smoke_classification_rows(self) -> list[dict[str, str]]:
        self.assertTrue(BROAD_SMOKE_CLASSIFICATION.exists(), msg=str(BROAD_SMOKE_CLASSIFICATION))
        lines = BROAD_SMOKE_CLASSIFICATION.read_text(encoding="utf-8").splitlines()
        header_index = next(
            index
            for index, line in enumerate(lines)
            if line.startswith("| Check ID | Command | Reads |")
        )
        headers = [cell.strip() for cell in lines[header_index].strip("|").split("|")]
        self.assertEqual(tuple(headers), BROAD_SMOKE_REQUIRED_CLASSIFICATION_FIELDS)

        rows: list[dict[str, str]] = []
        for line in lines[header_index + 2 :]:
            if not line.startswith("| broad_smoke."):
                if rows:
                    break
                continue
            cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
            self.assertEqual(len(cells), len(headers), msg=line)
            rows.append(dict(zip(headers, cells, strict=True)))
        return rows

    def load_broad_smoke_parallel_classification(self) -> dict[str, object]:
        self.assertTrue(BROAD_SMOKE_PARALLEL_CLASSIFICATION.exists(), msg=str(BROAD_SMOKE_PARALLEL_CLASSIFICATION))
        with BROAD_SMOKE_PARALLEL_CLASSIFICATION.open(encoding="utf-8") as handle:
            loaded = yaml.safe_load(handle)
        self.assertIsInstance(loaded, dict)
        return loaded

    def run_broad_smoke_classification_validator(
        self,
        classification: Path = BROAD_SMOKE_PARALLEL_CLASSIFICATION,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(BROAD_SMOKE_CLASSIFICATION_VALIDATOR),
                "--classification",
                str(classification),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def select(self, paths: list[str], *, mode: str = "explicit", **kwargs):
        kwargs.setdefault("preflight_context", self.root_preflight_context)
        return select_validation(SelectionRequest(mode=mode, paths=tuple(paths), repo_root=ROOT, **kwargs))

    def test_shared_preflight_context_requires_matching_repository_identity(self) -> None:
        other_root = Path(tempfile.mkdtemp(prefix="validation-selection-preflight-mismatch-"))
        self.addCleanupTree(other_root)

        with self.assertRaisesRegex(ValueError, "preflight context does not match repository root"):
            select_validation(
                SelectionRequest(
                    mode="explicit",
                    paths=("docs/workflows.md",),
                    repo_root=other_root,
                    preflight_context=self.root_preflight_context,
                )
            )

    def test_change_evidence_registry_entries_are_complete_and_stable(self) -> None:
        valid = [
            EvidenceClassRegistration(
                evidence_class_id="preservation",
                patterns=("behavior-preservation.md",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="implementation",
                allowed_when=("behavior preservation evidence is recorded",),
            )
        ]
        self.assertEqual(validate_evidence_class_registry(valid), [])

        invalid_cases = [
            EvidenceClassRegistration(
                evidence_class_id="bad id",
                patterns=("bad-id.md",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="implementation",
                allowed_when=("invalid ID fixture",),
            ),
            EvidenceClassRegistration(
                evidence_class_id="missing-route",
                patterns=("missing-route.md",),
                selector_routes=(),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="implementation",
                allowed_when=("invalid route fixture",),
            ),
            EvidenceClassRegistration(
                evidence_class_id="missing-validator",
                patterns=("missing-validator.md",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="",
                lifecycle_stage="implementation",
                allowed_when=("invalid validator fixture",),
            ),
            EvidenceClassRegistration(
                evidence_class_id="missing-stage",
                patterns=("missing-stage.md",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="",
                allowed_when=("invalid stage fixture",),
            ),
            EvidenceClassRegistration(
                evidence_class_id="missing-conditions",
                patterns=("missing-conditions.md",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="implementation",
            ),
        ]

        for entry in invalid_cases:
            with self.subTest(entry=entry.evidence_class_id):
                self.assertTrue(validate_evidence_class_registry([entry]))

    def test_registered_change_evidence_patterns_and_exact_names_match_once(self) -> None:
        paths = [
            "docs/changes/2026-04-25-example/script-output-audit.md",
            "docs/changes/2026-04-25-example/session-identity.txt",
            "docs/changes/2026-04-25-example/command-output-identity.txt",
            "docs/changes/2026-04-25-example/behavior-preservation.md",
            "docs/changes/2026-04-25-example/adoption-surface-review.md",
            "docs/changes/2026-04-25-example/readme-ownership-proof.md",
            "docs/changes/2026-04-25-example/vision-readme-sync-proof.md",
            "docs/changes/2026-04-25-example/cold-read-review.md",
            "docs/changes/2026-04-25-example/guide-cold-read.md",
            "docs/changes/2026-04-25-example/repository-metadata-proof.md",
            "docs/changes/2026-04-25-example/version-sync-proof.md",
            "docs/changes/2026-04-25-example/baseline.md",
            "docs/changes/2026-04-25-example/script-performance-baseline.yaml",
            "docs/changes/2026-04-25-example/token-cost.md",
            "docs/changes/2026-04-25-example/cold-read-proof.md",
            "docs/changes/2026-04-25-example/representative-project-map-outputs.md",
            "docs/changes/2026-04-25-example/broad-smoke-child-classification.md",
        ]
        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["blocking_results"])
        self.assertTrue(
            all(
                classified["category"] == "registered-change-evidence"
                for classified in payload["classified_paths"]
            )
        )
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))

    def test_change_evidence_registry_rejects_broad_and_ambiguous_patterns(self) -> None:
        broad_entries = [
            EvidenceClassRegistration(
                evidence_class_id="broad-md",
                patterns=("*.md",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="implementation",
                allowed_when=("invalid broad fixture",),
            ),
            EvidenceClassRegistration(
                evidence_class_id="broad-txt",
                patterns=("*.txt",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="implementation",
                allowed_when=("invalid broad fixture",),
            ),
        ]
        errors = validate_evidence_class_registry(broad_entries)
        self.assertGreaterEqual(len(errors), 2)
        self.assertTrue(all("too broad" in error for error in errors))

        ambiguous_entries = [
            EvidenceClassRegistration(
                evidence_class_id="preservation-a",
                patterns=("*-preservation.md",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="implementation",
                allowed_when=("ambiguous fixture",),
            ),
            EvidenceClassRegistration(
                evidence_class_id="preservation-b",
                patterns=("behavior-preservation.md",),
                selector_routes=("artifact_lifecycle.validate",),
                required_validator="validate-artifact-lifecycle",
                lifecycle_stage="implementation",
                allowed_when=("ambiguous fixture",),
            ),
        ]
        ambiguous_result = validate_evidence_class_registry(
            ambiguous_entries,
            sample_paths=("behavior-preservation.md",),
        )
        self.assertTrue(any("ambiguous" in error for error in ambiguous_result))

    def test_registered_change_evidence_selects_declared_checks_and_governing_metadata(self) -> None:
        result = self.select(["docs/changes/2026-04-25-example/behavior-preservation.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["blocking_results"])
        self.assertIn(
            {
                "path": "docs/changes/2026-04-25-example/behavior-preservation.md",
                "category": "registered-change-evidence",
            },
            payload["classified_paths"],
        )
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertIn("docs/changes/2026-04-25-example/behavior-preservation.md", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/change.yaml", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/", payload["affected_roots"])

    def test_selector_preservation_surface_keeps_selected_check_identity(self) -> None:
        paths = [
            "scripts/validation_selection.py",
            "scripts/test-select-validation.py",
            "docs/changes/2026-04-25-example/selector-preservation.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertEqual(
            {"artifact_lifecycle.validate", "selector.regression"},
            selected_ids(payload),
        )
        selector_check = next(check for check in payload["selected_checks"] if check["id"] == "selector.regression")
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertEqual(selector_check["phase"], "focused")
        self.assertEqual(selector_check["cache_status"], "not-applicable")
        self.assertIn("Changed selector code requires selector regression fixtures.", selector_check["reason"])
        self.assertIn("docs/changes/2026-04-25-example/change.yaml", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/selector-preservation.md", lifecycle_check["paths"])

    def test_validation_cache_evidence_files_route_without_manual_debt(self) -> None:
        paths = [
            "docs/changes/2026-04-25-example/validation-cache-evidence.yaml",
            "docs/changes/2026-04-25-example/validation-cache-measurement.yaml",
        ]
        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["blocking_results"])
        self.assertFalse(payload["registration_debt"])
        self.assertTrue(
            all(
                classified["category"] == "registered-change-evidence"
                for classified in payload["classified_paths"]
            )
        )
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertIn("change_metadata.validate", selected_ids(payload))
        self.assertIn("validation_cache.regression", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertIn("docs/changes/2026-04-25-example/change.yaml", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/validation-cache-evidence.yaml", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/validation-cache-measurement.yaml", lifecycle_check["paths"])
        metadata_check = next(check for check in payload["selected_checks"] if check["id"] == "change_metadata.validate")
        self.assertIn("docs/changes/2026-04-25-example/validation-cache-measurement.yaml", metadata_check["paths"])

    def test_selector_runtime_evidence_files_route_without_manual_debt(self) -> None:
        paths = [
            "docs/changes/2026-04-25-example/selector-regression-runtime-baseline.yaml",
            "docs/changes/2026-04-25-example/selector-regression-runtime-result.yaml",
        ]
        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["blocking_results"])
        self.assertFalse(payload["registration_debt"])
        self.assertTrue(
            all(
                classified["category"] == "registered-change-evidence"
                for classified in payload["classified_paths"]
            )
        )
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertIn("docs/changes/2026-04-25-example/change.yaml", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/selector-regression-runtime-baseline.yaml", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/selector-regression-runtime-result.yaml", lifecycle_check["paths"])

    def test_unregistered_change_evidence_produces_registration_debt(self) -> None:
        result = self.select(["docs/changes/2026-04-25-example/notes.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            {
                "path": "docs/changes/2026-04-25-example/notes.md",
                "category": "unregistered-change-evidence",
            },
            payload["classified_paths"],
        )
        self.assertIn("docs/changes/2026-04-25-example/", payload["affected_roots"])
        self.assertNotIn("artifact_lifecycle.validate", selected_ids(payload))
        debt = next(item for item in payload["blocking_results"] if item["code"] == "manual-routing-required")
        self.assertEqual(debt["path"], "docs/changes/2026-04-25-example/notes.md")
        self.assertTrue(debt["manual_routing_required"])
        self.assertEqual(debt["path_class"], "unregistered-change-evidence")
        self.assertEqual(debt["affected_class"], "change-local evidence")
        self.assertEqual(debt["debt"], "evidence-registration")
        self.assertEqual(debt["verify_readiness"], "blocked")
        self.assertEqual(debt["deferral_status"], "none")
        self.assertIn("selector routing", debt["next_action"])
        self.assertIn("owner-approved deferral", debt["next_action"])
        for required_term in ("owner", "path", "reason", "validation impact", "follow-up"):
            self.assertIn(required_term, debt["next_action"])

    def test_diagnostic_broad_smoke_does_not_erase_missing_route_blocker(self) -> None:
        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("docs/changes/2026-04-25-example/notes.md",),
                broad_smoke=True,
                repo_root=ROOT,
            )
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "blocked")
        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        self.assertIn(
            "manual-routing-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        debt = next(item for item in payload["blocking_results"] if item["code"] == "manual-routing-required")
        self.assertEqual(debt["path"], "docs/changes/2026-04-25-example/notes.md")
        self.assertEqual(debt["verify_readiness"], "blocked")
        self.assertIn({"type": "explicit_flag", "value": "--broad-smoke"}, payload["broad_smoke"]["sources"])

    def write_change_with_evidence_deferral(
        self,
        *,
        deferral_fields: dict[str, str],
        change_id: str = "2026-04-25-deferral",
    ) -> tuple[Path, str]:
        repo = self.make_git_repo()
        evidence_path = f"docs/changes/{change_id}/unregistered-evidence.md"
        change_root = repo / "docs" / "changes" / change_id
        change_root.mkdir(parents=True, exist_ok=True)
        (change_root / "unregistered-evidence.md").write_text("manual evidence\n", encoding="utf-8")
        field_lines = "\n".join(
            f"    {field}: {value}"
            for field, value in deferral_fields.items()
        )
        (change_root / "change.yaml").write_text(
            "change_id: 2026-04-25-deferral\n"
            "evidence_registration_deferrals:\n"
            f"  - {field_lines.lstrip()}\n",
            encoding="utf-8",
        )
        return repo, evidence_path

    def test_unregistered_change_evidence_with_complete_deferral_unblocks_readiness(self) -> None:
        repo, evidence_path = self.write_change_with_evidence_deferral(
            deferral_fields={
                "path": "docs/changes/2026-04-25-deferral/unregistered-evidence.md",
                "owner": "plan-review",
                "reason": "intentionally unsupported fixture",
                "validation_impact": "explicit lifecycle coverage required",
                "follow_up": "docs/plans/2026-04-25-deferral.md#M3",
            }
        )

        result = select_validation(SelectionRequest(mode="explicit", paths=(evidence_path,), repo_root=repo))
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn(
            {"path": evidence_path, "category": "unregistered-change-evidence"},
            payload["classified_paths"],
        )
        self.assertNotIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertEqual(payload["blocking_results"], [])
        debt = next(item for item in payload["registration_debt"] if item["path"] == evidence_path)
        self.assertTrue(debt["manual_routing_required"])
        self.assertEqual(debt["debt"], "evidence-registration")
        self.assertEqual(debt["verify_readiness"], "owner-deferred")
        self.assertEqual(debt["deferral_status"], "complete")
        self.assertEqual(debt["deferral"]["owner"], "plan-review")
        self.assertEqual(debt["deferral"]["path"], evidence_path)
        self.assertEqual(debt["deferral"]["reason"], "intentionally unsupported fixture")
        self.assertEqual(debt["deferral"]["validation_impact"], "explicit lifecycle coverage required")
        self.assertEqual(debt["deferral"]["follow_up"], "docs/plans/2026-04-25-deferral.md#M3")

    def test_unregistered_change_evidence_with_incomplete_deferral_remains_blocking(self) -> None:
        repo, evidence_path = self.write_change_with_evidence_deferral(
            deferral_fields={
                "path": "docs/changes/2026-04-25-deferral/unregistered-evidence.md",
                "owner": "plan-review",
                "reason": "missing fields fixture",
            }
        )

        result = select_validation(SelectionRequest(mode="explicit", paths=(evidence_path,), repo_root=repo))
        payload = result.to_json_dict()

        self.assertEqual(result.status, "blocked")
        debt = next(item for item in payload["blocking_results"] if item["path"] == evidence_path)
        self.assertEqual(debt["deferral_status"], "incomplete")
        self.assertEqual(debt["verify_readiness"], "blocked")
        self.assertIn("validation_impact", debt["missing_deferral_fields"])
        self.assertIn("follow_up", debt["missing_deferral_fields"])

    def test_owner_deferral_for_different_path_does_not_unblock_evidence(self) -> None:
        repo, evidence_path = self.write_change_with_evidence_deferral(
            deferral_fields={
                "path": "docs/changes/2026-04-25-deferral/other-evidence.md",
                "owner": "plan-review",
                "reason": "wrong path fixture",
                "validation_impact": "explicit lifecycle coverage required",
                "follow_up": "docs/plans/2026-04-25-deferral.md#M3",
            }
        )

        result = select_validation(SelectionRequest(mode="explicit", paths=(evidence_path,), repo_root=repo))
        payload = result.to_json_dict()

        self.assertEqual(result.status, "blocked")
        debt = next(item for item in payload["blocking_results"] if item["path"] == evidence_path)
        self.assertEqual(debt["deferral_status"], "none")
        self.assertEqual(debt["verify_readiness"], "blocked")

    def test_local_mode_discovers_registered_evidence_not_named_by_explicit_paths(self) -> None:
        repo = self.make_git_repo()
        change_root = repo / "docs" / "changes" / "2026-04-25-local"
        change_root.mkdir(parents=True)
        (change_root / "change.yaml").write_text("change_id: 2026-04-25-local\n", encoding="utf-8")
        (change_root / "selector-routing-proof.md").write_text("# Selector routing proof\n", encoding="utf-8")

        explicit_result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("docs/changes/2026-04-25-local/change.yaml",),
                repo_root=repo,
            )
        )
        local_result = select_validation(SelectionRequest(mode="local", repo_root=repo))
        explicit_payload = explicit_result.to_json_dict()
        local_payload = local_result.to_json_dict()

        self.assertEqual(explicit_result.status, "ok")
        self.assertNotIn(
            "docs/changes/2026-04-25-local/selector-routing-proof.md",
            explicit_payload["changed_paths"],
        )
        self.assertEqual(local_result.status, "ok")
        self.assertIn(
            "docs/changes/2026-04-25-local/selector-routing-proof.md",
            local_payload["changed_paths"],
        )
        self.assertIn(
            {
                "path": "docs/changes/2026-04-25-local/selector-routing-proof.md",
                "category": "registered-change-evidence",
            },
            local_payload["classified_paths"],
        )
        self.assertIn("artifact_lifecycle.validate", selected_ids(local_payload))
        self.assertIn("docs/changes/2026-04-25-local/", local_payload["affected_roots"])

    def test_selector_registry_changes_select_selector_regression(self) -> None:
        result = self.select(
            [
                "scripts/validation_selection.py",
                "scripts/test-select-validation.py",
                "scripts/validate-broad-smoke-classification.py",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["blocking_results"])
        self.assertIn("selector.regression", selected_ids(payload))

    def test_catalog_matches_v1_contract(self) -> None:
        self.assertEqual(set(CHECK_CATALOG), set(EXPECTED_CATALOG))
        for check_id, command in EXPECTED_CATALOG.items():
            with self.subTest(check_id=check_id):
                self.assertEqual(CHECK_CATALOG[check_id].command_template, command)
                self.assertTrue(CHECK_CATALOG[check_id].category)

    def test_catalog_records_initial_parallel_safe_allowlist(self) -> None:
        from validation_selection import is_parallel_safe_check

        expected_parallel_safe = {
            "adapters.regression",
            "artifact_lifecycle.regression",
            "change_record_query.regression",
            "change_metadata.regression",
            "guide_system.regression",
            "requirement_fidelity.spec_reads",
            "review_artifacts.regression",
            "selector.regression",
            "skills.generation_regression",
            "skills.regression",
            "token_cost.regression",
            "token_cost.report_regression",
            "validation_cache.regression",
        }

        self.assertEqual(
            {check_id for check_id in CHECK_CATALOG if is_parallel_safe_check(check_id)},
            expected_parallel_safe,
        )
        for check_id, entry in CHECK_CATALOG.items():
            with self.subTest(check_id=check_id):
                self.assertIsInstance(entry.parallel_safe, bool)
                self.assertEqual(entry.parallel_safe, check_id in expected_parallel_safe)

    def test_cli_outputs_json_for_classified_skill_path(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "skills/code-review/SKILL.md")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["mode"], "explicit")
        self.assertEqual(payload["status"], "ok")
        for field in (
            "changed_paths",
            "classified_paths",
            "unclassified_paths",
            "selected_checks",
            "affected_roots",
            "broad_smoke_required",
            "blocking_results",
            "preflight_results",
            "rationale",
        ):
            self.assertIn(field, payload)
        self.assertIn(
            {"path": "skills/code-review/SKILL.md", "category": "skills"},
            payload["classified_paths"],
        )
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue(
            {
                "skills.validate",
                "skills.regression",
                "skills.generation_regression",
                "skills.drift",
            }.issubset(selected_ids(payload))
        )
        self.assertIn("adapters.drift", selected_ids(payload))
        for check in payload["selected_checks"]:
            self.assertIn(check["phase"], {"focused", "boundary"})
            self.assertEqual(check["cache_status"], "not-applicable")

    def test_selector_marks_broad_smoke_as_boundary_phase(self) -> None:
        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("skills/code-review/SKILL.md",),
                broad_smoke=True,
                repo_root=ROOT,
            )
        )
        payload = result.to_json_dict()
        phases = {check["id"]: check["phase"] for check in payload["selected_checks"]}
        self.assertEqual(phases["broad_smoke.repo"], "boundary")
        self.assertEqual(phases["skills.validate"], "focused")

    def test_preflight_blocks_untracked_authoritative_artifact_with_action(self) -> None:
        repo = self.make_git_repo()
        proposal = repo / "docs" / "proposals" / "new-proposal.md"
        proposal.parent.mkdir(parents=True)
        proposal.write_text("# New proposal\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("docs/proposals/new-proposal.md",),
                repo_root=repo,
            )
        )
        payload = result.to_json_dict()

        self.assertEqual(payload["status"], "blocked")
        blockers = payload["blocking_results"]
        self.assertTrue(
            any(
                blocker.get("code") == "untracked-authoritative-artifacts"
                and blocker.get("corrective_action") == "git add -- docs/proposals/new-proposal.md"
                for blocker in blockers
            ),
            blockers,
        )
        self.assertTrue(
            any(
                result.get("check") == "tracked_authoritative_artifacts"
                and result.get("result") == "blocked"
                for result in payload["preflight_results"]
            ),
            payload["preflight_results"],
        )

    def test_preflight_passes_tracked_authoritative_artifact(self) -> None:
        repo = self.make_git_repo()
        proposal = repo / "docs" / "proposals" / "tracked-proposal.md"
        proposal.parent.mkdir(parents=True)
        proposal.write_text("# Tracked proposal\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("docs/proposals/tracked-proposal.md",),
                repo_root=repo,
            )
        )
        payload = result.to_json_dict()

        self.assertNotIn(
            "untracked-authoritative-artifacts",
            {blocker.get("code") for blocker in payload["blocking_results"]},
        )
        self.assertTrue(
            any(
                item.get("check") == "tracked_authoritative_artifacts"
                and item.get("result") == "pass"
                for item in payload["preflight_results"]
            ),
            payload["preflight_results"],
        )

    def test_missing_mode_specific_inputs_return_json_error(self) -> None:
        result = run_selector("--mode", "pr", "--base", "HEAD~1")
        self.assertEqual(result.returncode, 4)
        payload = parse_stdout(result)
        self.assertEqual(payload["status"], "error")
        self.assertIn("invalid-invocation", {item["code"] for item in payload["blocking_results"]})

    def test_unclassified_path_blocks_without_fail_open(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "experimental/runtime/example.txt")
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["unclassified_paths"], ["experimental/runtime/example.txt"])
        self.assertIn("unclassified-path", {item["code"] for item in payload["blocking_results"]})
        self.assertNotEqual(payload["status"], "ok")

    def test_mixed_classified_and_unclassified_paths_block_partial_execution(self) -> None:
        result = run_selector(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            "--path",
            "experimental/runtime/example.txt",
        )
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertIn("skills.validate", selected_ids(payload))
        self.assertEqual(payload["unclassified_paths"], ["experimental/runtime/example.txt"])

    def test_change_metadata_paths_select_multi_file_validator(self) -> None:
        result = self.select(
            [
                "docs/changes/2026-04-25-a/change.yaml",
                "docs/changes/2026-04-25-b/change.yaml",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("change_metadata.validate", selected_ids(payload))
        self.assertIn("change_metadata.regression", selected_ids(payload))
        self.assertEqual(
            payload["affected_roots"],
            ["docs/changes/2026-04-25-a/", "docs/changes/2026-04-25-b/"],
        )
        validate_check = next(check for check in payload["selected_checks"] if check["id"] == "change_metadata.validate")
        self.assertEqual(
            validate_check["command"],
            "python scripts/validate-change-metadata.py docs/changes/2026-04-25-a/change.yaml docs/changes/2026-04-25-b/change.yaml",
        )

    def test_review_lifecycle_and_release_paths_select_scoped_validators(self) -> None:
        result = self.select(
            [
                "docs/changes/2026-04-25-example/review-resolution.md",
                "specs/test-layering-and-change-scoped-validation.test.md",
                "docs/releases/v0.1.1/release.yaml",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("review_artifacts.validate", selected_ids(payload))
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertIn("release.validate", selected_ids(payload))
        self.assertIn("docs/changes/2026-04-25-example/", payload["affected_roots"])
        release_check = next(check for check in payload["selected_checks"] if check["id"] == "release.validate")
        self.assertEqual(release_check["command"], "python scripts/validate-release-ci.py --version v0.1.1")

    def test_multiple_release_paths_share_one_release_validation_check(self) -> None:
        result = self.select(
            [
                "docs/releases/v0.1.1/release.yaml",
                "docs/releases/v0.1.2/release.yaml",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("release.validate", selected_ids(payload))
        release_check = next(check for check in payload["selected_checks"] if check["id"] == "release.validate")
        self.assertEqual(
            release_check["command"],
            "python scripts/validate-release-ci.py --version v0.1.1 v0.1.2",
        )

    def test_release_evidence_markdown_path_selects_lifecycle_checklist_validation(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "docs/releases/v1.2.3.md")
        payload = parse_stdout(result)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "ok")
        self.assertIn({"path": "docs/releases/v1.2.3.md", "category": "release"}, payload["classified_paths"])
        self.assertNotIn(
            "manual-routing-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertNotIn(
            "release-version-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        lifecycle_check = next(
            check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate"
        )
        self.assertEqual(
            lifecycle_check["command"],
            "python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/releases/v1.2.3.md",
        )

    def test_release_guidance_paths_do_not_require_release_version(self) -> None:
        result = run_selector(
            "--mode",
            "explicit",
            "--path",
            "docs/releases/README.md",
            "--path",
            "docs/releases/index.md",
        )
        payload = parse_stdout(result)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(payload["status"], "ok")
        self.assertIn(
            {"path": "docs/releases/README.md", "category": "workflow-guidance"},
            payload["classified_paths"],
        )
        self.assertIn(
            {"path": "docs/releases/index.md", "category": "workflow-guidance"},
            payload["classified_paths"],
        )
        self.assertNotIn(
            "release-version-required",
            {item["code"] for item in payload["blocking_results"]},
        )

    def test_release_path_without_version_directory_blocks(self) -> None:
        result = run_selector("--mode", "explicit", "--path", "docs/releases/release-notes.md")
        self.assertEqual(result.returncode, 2)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertIn({"path": "docs/releases/release-notes.md", "category": "release"}, payload["classified_paths"])
        self.assertIn(
            "release-version-required",
            {item["code"] for item in payload["blocking_results"]},
        )
        self.assertNotIn("release.validate", selected_ids(payload))

    def test_first_slice_representative_categories_route_or_block_safely(self) -> None:
        cases = [
            {
                "path": "dist/adapters/opencode/AGENTS.md",
                "category": "generated-adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": ".codex/skills/code-review/SKILL.md",
                "category": "generated-skills",
                "status": "ok",
                "checks": {"skills.generation_regression", "skills.drift"},
            },
            {
                "path": "docs/workflows.md",
                "category": "workflow-guidance",
                "status": "ok",
                "checks": {"selector.regression", "guide_system.validate"},
            },
            {
                "path": ".gitignore",
                "category": "ignore-policy",
                "status": "ok",
                "checks": {"skills.generation_regression"},
            },
            {
                "path": "CONSTITUTION.md",
                "category": "governance",
                "status": "ok",
                "checks": {"selector.regression", "guide_system.validate"},
            },
            {
                "path": "schemas/change.schema.json",
                "category": "schemas",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "templates/example.md",
                "category": "templates",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": "scripts/build-adapters.py",
                "category": "adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": "scripts/test-adapter-distribution.py",
                "category": "adapters",
                "status": "ok",
                "checks": {"adapters.regression", "adapters.drift", "adapters.validate"},
            },
            {
                "path": "scripts/validation_cache.py",
                "category": "validation-cache",
                "status": "ok",
                "checks": {"validation_cache.regression"},
            },
            {
                "path": "scripts/test-validation-cache.py",
                "category": "validation-cache",
                "status": "ok",
                "checks": {"validation_cache.regression"},
            },
            {
                "path": "scripts/validate-skills.py",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "skills.generation_regression"},
            },
            {
                "path": "scripts/review_independence_skill_phrases.py",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "skills.generation_regression"},
            },
            {
                "path": "scripts/validate-guide-system.py",
                "category": "guide-system-validator",
                "status": "ok",
                "checks": {"guide_system.regression", "guide_system.validate"},
            },
            {
                "path": "scripts/test-guide-system-validator.py",
                "category": "guide-system-validator",
                "status": "ok",
                "checks": {"guide_system.regression", "guide_system.validate"},
            },
            {
                "path": "scripts/lifecycle_state_sync.py",
                "category": "validator-artifact-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.regression"},
            },
            {
                "path": "scripts/change_metadata_semantics.py",
                "category": "validator-change-metadata",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "scripts/query-change-record.py",
                "category": "change-record-query",
                "status": "ok",
                "checks": {"change_record_query.regression", "change_metadata.regression"},
            },
            {
                "path": "scripts/build-skills.py",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "skills.generation_regression"},
            },
            {
                "path": "tests/fixtures/skills/skill-readability/valid-pilot/SKILL.md",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "skills.generation_regression"},
            },
            {
                "path": "tests/fixtures/skills",
                "category": "validator-skills",
                "status": "ok",
                "checks": {"skills.regression", "skills.generation_regression"},
            },
            {
                "path": "scripts/validate-release.py",
                "category": "release-script",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "scripts/validate-release-ci.py",
                "category": "release-script",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": ".github/workflows/release.yml",
                "category": "release-script",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "scripts/ci.sh",
                "category": "ci-wrapper",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": ".github/workflows/ci.yml",
                "category": "ci-workflow",
                "status": "ok",
                "checks": {"selector.regression"},
            },
            {
                "path": "docs/plan.md",
                "category": "plan-index",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate", "guide_system.validate"},
            },
            {
                "path": "docs/plan-archive.md",
                "category": "plan-index",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate", "guide_system.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/plan-index-migration.md",
                "category": "change-local-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/explain-change.md",
                "category": "change-local-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/architecture.md",
                "category": "change-local-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/verify-report.md",
                "category": "change-local-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/implementation-notes.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/cold-read-report.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/adapter-packaging.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/behavior-parity-report.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/behavior-parity.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/behavior-preservation.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/vision-readme-sync-proof.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/cold-read-review.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/guide-cold-read.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/output-contract-red-test.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/script-output-audit.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/script-output-layer-audit.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/broad-smoke-child-commands-baseline.txt",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/broad-smoke-child-classification.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/broad-smoke-child-commands-post-m4.txt",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/change-metadata-validator-tests-baseline.txt",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/change-metadata-validator-tests-post-m4.txt",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/selected-tests-baseline.txt",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/selected-tests-m3.txt",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/baseline.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/script-performance-baseline.yaml",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/selector-regression-profile.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/broad-smoke-child-classification.yaml",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/broad-smoke-parallelism-baseline.yaml",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/broad-smoke-parallelism-result.yaml",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/generated-output-proof.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/historical-coverage.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/clean-install-proof.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/validator-fixtures.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/release-process-dry-run.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/routing-coverage.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/selector-routing-proof.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/skill-audit.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/token-cost.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/m2-code-review-preservation.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/m5-generated-token-cold-read-evidence.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/skill-contract-sufficiency.md",
                "category": "registered-change-evidence",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/changes/2026-04-25-example/diagrams/context.mmd",
                "category": "change-local-lifecycle",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "docs/architecture/system/diagrams/context.mmd",
                "category": "architecture-diagram",
                "status": "ok",
                "checks": {"artifact_lifecycle.validate"},
            },
            {
                "path": "tests/fixtures/artifact-lifecycle/valid-canonical-arc42-architecture/docs/architecture/system/architecture.md",
                "category": "artifact-lifecycle-fixtures",
                "status": "ok",
                "checks": {"artifact_lifecycle.regression"},
            },
            {
                "path": "tests/fixtures/review-artifacts/valid-clean-receipt-root/review-log.md",
                "category": "review-artifact-fixtures",
                "status": "ok",
                "checks": {"review_artifacts.regression"},
            },
            {
                "path": "tests/fixtures/review-artifacts/valid-requirement-compression-calibration/reviews/code-review-r1.md",
                "category": "review-artifact-fixtures",
                "status": "ok",
                "checks": {"review_artifacts.regression"},
            },
            {
                "path": "tests/fixtures/review-artifacts/valid-clean-receipt-root/change.yaml",
                "category": "review-artifact-fixtures",
                "status": "ok",
                "checks": {"review_artifacts.regression", "change_metadata.regression"},
            },
            {
                "path": "tests/fixtures/change-metadata/compact-valid/change.yaml",
                "category": "change-metadata-fixtures",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "tests/fixtures/change-metadata",
                "category": "change-metadata-fixtures",
                "status": "ok",
                "checks": {"change_metadata.regression"},
            },
            {
                "path": "tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json",
                "category": "requirement-fidelity-spec-read",
                "status": "ok",
                "checks": {"requirement_fidelity.spec_reads"},
            },
            {
                "path": "scripts/test-fidelity-gate-spec-reads.py",
                "category": "requirement-fidelity-spec-read",
                "status": "ok",
                "checks": {"requirement_fidelity.spec_reads"},
            },
            {
                "path": "scripts/measure-skill-tokens.py",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "scripts/analyze-codex-jsonl.py",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "scripts/test-token-cost-measurement.py",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "scripts/run-token-cost-benchmarks.py",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "scripts/validate-token-cost-report.py",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression", "token_cost.report_regression"},
            },
            {
                "path": "scripts/test-token-cost-report-validation.py",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression", "token_cost.report_regression"},
            },
            {
                "path": "benchmarks/token-cost/manifest.yaml",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "benchmarks/token-cost/prompts/proposal-short.md",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "benchmarks/token-cost/fixtures/minimal-public-project/AGENTS.md",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "docs/reports/token-cost/2026-05-10-baseline.md",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "docs/reports/token-cost/releases/v0.1.1.yaml",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression", "token_cost.report_validate"},
            },
            {
                "path": "docs/reports/adapter-artifacts/releases/v0.1.2.yaml",
                "category": "adapter-artifact-metadata",
                "status": "ok",
                "checks": {"adapters.regression"},
            },
            {
                "path": "docs/reports/token-cost/runs/v0.1.1/proposal-short-run1.analysis.yaml",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "packages/rigorloop/package.json",
                "category": "rigorloop-cli",
                "status": "ok",
                "checks": {"rigorloop_cli.test", "npm_package_publication.test"},
            },
            {
                "path": "scripts/test-npm-package-publication.py",
                "category": "rigorloop-cli",
                "status": "ok",
                "checks": {"rigorloop_cli.test", "npm_package_publication.test"},
            },
            {
                "path": "tests/fixtures/token-cost/sample-codex-session.jsonl",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression"},
            },
            {
                "path": "tests/fixtures/token-cost/reports/valid-final-pass/v0.1.1.yaml",
                "category": "token-cost",
                "status": "ok",
                "checks": {"token_cost.regression", "token_cost.report_regression"},
            },
        ]

        for case in cases:
            with self.subTest(path=case["path"]):
                result = self.select([case["path"]])
                payload = result.to_json_dict()

                self.assertEqual(result.status, case["status"])
                self.assertIn({"path": case["path"], "category": case["category"]}, payload["classified_paths"])
                if case.get("checks"):
                    self.assertTrue(case["checks"].issubset(selected_ids(payload)))
                if case.get("blocking_code"):
                    self.assertIn(
                        case["blocking_code"],
                        {item["code"] for item in payload["blocking_results"]},
                    )

    def test_learn_artifact_paths_are_known_lightweight_paths(self) -> None:
        paths = [
            "docs/learn/README.md",
            "docs/learn/sessions/2026-05-04-example.md",
            "docs/learn/topics/verification.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        for path in paths:
            with self.subTest(path=path):
                self.assertIn({"path": path, "category": "learn-artifact"}, payload["classified_paths"])

        self.assertNotIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertEqual({"guide_system.validate"}, selected_ids(payload))

    def test_docs_examples_paths_are_known_non_lifecycle_paths(self) -> None:
        paths = [
            "docs/examples/README.md",
            "docs/examples/plans/example-plan.md",
            "docs/examples/formal-review-recording/README.md",
            "docs/examples/formal-review-recording/change-id-selection-examples.md",
            "docs/examples/formal-review-recording/clean-review-receipt-root.md",
            "docs/examples/formal-review-recording/material-finding-location-examples.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        for path in paths:
            with self.subTest(path=path):
                self.assertIn({"path": path, "category": "examples"}, payload["classified_paths"])

        self.assertNotIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertNotIn("review_artifacts.validate", selected_ids(payload))
        self.assertEqual(payload["selected_checks"], [])

    def test_project_map_paths_are_living_reference_not_lifecycle(self) -> None:
        cli_result = run_selector("--mode", "explicit", "--path", "docs/project-map.md")
        self.assertEqual(cli_result.returncode, 0, cli_result.stdout + cli_result.stderr)
        cli_payload = parse_stdout(cli_result)
        self.assertIn(
            {"path": "docs/project-map.md", "category": "living-reference/project-map"},
            cli_payload["classified_paths"],
        )
        self.assertEqual(cli_payload["unclassified_paths"], [])
        self.assertEqual(cli_payload["blocking_results"], [])

        paths = ["docs/project-map.md", "docs/project-map/release.md"]
        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        for path in paths:
            with self.subTest(path=path):
                self.assertIn(
                    {"path": path, "category": "living-reference/project-map"},
                    payload["classified_paths"],
                )

        self.assertNotIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertEqual({"guide_system.validate"}, selected_ids(payload))

    def test_follow_up_register_path_selects_static_validation(self) -> None:
        path = "docs/follow-ups.md"

        result = self.select([path])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertIn({"path": path, "category": "follow-up-register"}, payload["classified_paths"])
        self.assertEqual({"skills.regression"}, selected_ids(payload))

    def test_plan_index_surfaces_select_lifecycle_validation_with_both_surfaces(self) -> None:
        result = self.select(["docs/plan-archive.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertIn({"path": "docs/plan-archive.md", "category": "plan-index"}, payload["classified_paths"])
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertEqual(lifecycle_check["paths"], ["docs/plan-archive.md", "docs/plan.md"])

    def test_plan_index_migration_proof_routes_with_metadata_and_index_surfaces(self) -> None:
        result = self.select(["docs/changes/2026-04-25-example/plan-index-migration.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertIn(
            {
                "path": "docs/changes/2026-04-25-example/plan-index-migration.md",
                "category": "change-local-lifecycle",
            },
            payload["classified_paths"],
        )
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertEqual(
            lifecycle_check["paths"],
            [
                "docs/changes/2026-04-25-example/change.yaml",
                "docs/changes/2026-04-25-example/plan-index-migration.md",
                "docs/plan-archive.md",
                "docs/plan.md",
            ],
        )

    def test_retained_skill_validator_fixture_rationale_has_deterministic_routing(self) -> None:
        path = "docs/changes/0001-skill-validator/README.md"

        result = self.select([path])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        self.assertIn({"path": path, "category": "retained-change-fixture"}, payload["classified_paths"])
        self.assertIn("artifact_lifecycle.regression", selected_ids(payload))
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))

        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertEqual(lifecycle_check["paths"], [path])

    def test_selector_and_validation_script_paths_select_regressions(self) -> None:
        result = self.select(["scripts/select-validation.py", "scripts/validate-review-artifacts.py"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertIn("review_artifacts.regression", selected_ids(payload))

    def test_governance_paths_select_deterministic_proof_instead_of_empty_ok(self) -> None:
        result = self.select(["AGENTS.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "AGENTS.md", "category": "governance"}, payload["classified_paths"])
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertFalse(payload["blocking_results"])

    def test_pr_contained_lifecycle_warning_surfaces_select_lifecycle_validation(self) -> None:
        paths = [
            "AGENTS.md",
            "CONSTITUTION.md",
            "docs/workflows.md",
            "skills/workflow/SKILL.md",
            "docs/changes/2026-05-05-example/change.yaml",
            "docs/changes/2026-05-05-example/review-resolution.md",
        ]
        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["blocking_results"])
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        for path in paths:
            with self.subTest(path=path):
                self.assertIn(path, lifecycle_check["paths"])

    def test_readme_path_selects_lightweight_readme_validation(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-no-markers-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text("# Example\n\nNo generated vision marker block.\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertIn("readme.validate", selected_ids(payload))
        self.assertIn("guide_system.validate", selected_ids(payload))
        self.assertNotIn("readme.vision_markers", selected_ids(payload))
        self.assertFalse(payload["blocking_results"])

    def test_workflow_guidance_selects_composed_guide_system_validator(self) -> None:
        result = self.select(["docs/workflows.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "docs/workflows.md", "category": "workflow-guidance"}, payload["classified_paths"])
        self.assertIn("guide_system.validate", selected_ids(payload))
        guide_check = next(check for check in payload["selected_checks"] if check["id"] == "guide_system.validate")
        self.assertEqual(guide_check["command"], "python scripts/validate-guide-system.py")
        self.assertIn("cross-guide validation", guide_check["reason"])

    def test_readme_marker_validation_is_selected_for_marker_block_or_vision_scope(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-markers-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )

        marker_result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        marker_payload = marker_result.to_json_dict()

        self.assertEqual(marker_result.status, "ok")
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(marker_payload)))

        scoped_result = self.select(["README.md", "skills/vision/SKILL.md"])
        scoped_payload = scoped_result.to_json_dict()

        self.assertEqual(scoped_result.status, "ok")
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(scoped_payload)))
        self.assertFalse(scoped_payload["unclassified_paths"])
        self.assertFalse(scoped_payload["blocking_results"])

    def test_root_vision_path_selects_marker_validation_without_unclassified_block(self) -> None:
        result = self.select(["VISION.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "VISION.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertIn("readme.vision_markers", selected_ids(payload))
        self.assertFalse(payload["blocking_results"])

    def test_vision_rationale_path_selects_lifecycle_validation_without_unclassified_block(self) -> None:
        result = self.select(["docs/vision/strategic-positioning.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn(
            {"path": "docs/vision/strategic-positioning.md", "category": "lifecycle"},
            payload["classified_paths"],
        )
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertFalse(payload["blocking_results"])

    def test_retired_lowercase_root_vision_path_blocks_as_unclassified(self) -> None:
        result = self.select(["vision.md"])
        payload = result.to_json_dict()

        self.assertEqual(result.status, "blocked")
        self.assertNotIn({"path": "vision.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], ["vision.md"])
        self.assertNotIn("readme.vision_markers", selected_ids(payload))
        self.assertIn("unclassified-path", {item["code"] for item in payload["blocking_results"]})
        self.assertNotIn("vision-path-conflict", {item["code"] for item in payload["blocking_results"]})

    def test_retired_lowercase_root_vision_presence_does_not_create_global_conflict(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-retired-vision-presence-"))
        self.addCleanupTree(temp_root)
        (temp_root / "README.md").write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )
        (temp_root / "vision.md").write_text("# Legacy Vision\n", encoding="utf-8")
        (temp_root / "VISION.md").write_text("# Canonical Vision\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(mode="explicit", paths=("README.md",), repo_root=temp_root)
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
        self.assertFalse(payload["blocking_results"])

    def test_pr_handoff_surfaces_select_deterministic_checks(self) -> None:
        result = self.select(
            [
                ".github/workflows/ci.yml",
                "docs/workflows.md",
                "docs/plan.md",
                "docs/changes/2026-04-25-example/explain-change.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["unclassified_paths"])
        self.assertFalse(payload["blocking_results"])
        self.assertIn("selector.regression", selected_ids(payload))
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))

    def test_architecture_support_paths_route_without_manual_blocks(self) -> None:
        result = self.select(
            [
                "docs/architecture/system/diagrams/context.mmd",
                "docs/architecture/system/diagrams/container.mmd",
                "docs/changes/2026-04-25-example/architecture.md",
                "docs/changes/2026-04-25-example/diagrams/context.mmd",
                "tests/fixtures/artifact-lifecycle/valid-canonical-arc42-architecture/docs/architecture/system/architecture.md",
            ]
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertFalse(payload["unclassified_paths"])
        self.assertFalse(payload["blocking_results"])
        self.assertIn("artifact_lifecycle.validate", selected_ids(payload))
        self.assertIn("artifact_lifecycle.regression", selected_ids(payload))
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertIn("docs/architecture/system/architecture.md", lifecycle_check["paths"])
        self.assertIn("docs/changes/2026-04-25-example/change.yaml", lifecycle_check["paths"])

    def test_workflow_refactor_surface_set_selects_expected_checks(self) -> None:
        paths = [
            "CONSTITUTION.md",
            "AGENTS.md",
            "README.md",
            "docs/workflows.md",
            "docs/plan.md",
            "docs/plan-archive.md",
            "docs/plans/2026-05-03-workflow-refactor.md",
            "docs/vision/strategic-positioning.md",
            "docs/proposals/2026-05-01-workflow-refactor.md",
            "specs/rigorloop-workflow.md",
            "specs/rigorloop-workflow.test.md",
            "skills/workflow/SKILL.md",
            ".codex/skills/workflow/SKILL.md",
            "dist/adapters/codex/.agents/skills/workflow/SKILL.md",
            "scripts/test-select-validation.py",
            "scripts/test-artifact-lifecycle-validator.py",
            "scripts/build-skills.py",
            "scripts/test-build-skills.py",
            "scripts/test-skill-validator.py",
            "docs/changes/2026-05-03-workflow-refactor/change.yaml",
            "docs/changes/2026-05-03-workflow-refactor/explain-change.md",
            "docs/changes/2026-05-03-workflow-refactor/verify-report.md",
            "docs/changes/2026-05-03-workflow-refactor/review-log.md",
            "docs/changes/2026-05-03-workflow-refactor/review-resolution.md",
        ]

        result = self.select(paths)
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertEqual(payload["blocking_results"], [])
        expected_categories = {
            "CONSTITUTION.md": "governance",
            "AGENTS.md": "governance",
            "README.md": "readme",
            "docs/workflows.md": "workflow-guidance",
            "docs/plan.md": "plan-index",
            "docs/plan-archive.md": "plan-index",
            "docs/plans/2026-05-03-workflow-refactor.md": "lifecycle",
            "docs/vision/strategic-positioning.md": "lifecycle",
            "docs/proposals/2026-05-01-workflow-refactor.md": "lifecycle",
            "specs/rigorloop-workflow.md": "lifecycle",
            "specs/rigorloop-workflow.test.md": "lifecycle",
            "skills/workflow/SKILL.md": "skills",
            ".codex/skills/workflow/SKILL.md": "generated-skills",
            "dist/adapters/codex/.agents/skills/workflow/SKILL.md": "generated-adapters",
            "scripts/test-select-validation.py": "selector",
            "scripts/test-artifact-lifecycle-validator.py": "validator-artifact-lifecycle",
            "scripts/build-skills.py": "validator-skills",
            "scripts/test-build-skills.py": "validator-skills",
            "scripts/test-skill-validator.py": "validator-skills",
            "docs/changes/2026-05-03-workflow-refactor/change.yaml": "change-metadata",
            "docs/changes/2026-05-03-workflow-refactor/explain-change.md": "change-local-lifecycle",
            "docs/changes/2026-05-03-workflow-refactor/verify-report.md": "change-local-lifecycle",
            "docs/changes/2026-05-03-workflow-refactor/review-log.md": "review-artifacts",
            "docs/changes/2026-05-03-workflow-refactor/review-resolution.md": "review-artifacts",
        }
        for path, category in expected_categories.items():
            with self.subTest(path=path):
                self.assertIn({"path": path, "category": category}, payload["classified_paths"])

        self.assertTrue(
            {
                "skills.validate",
                "skills.regression",
                "skills.generation_regression",
                "skills.drift",
                "adapters.regression",
                "adapters.drift",
                "adapters.validate",
                "review_artifacts.validate",
                "artifact_lifecycle.regression",
                "artifact_lifecycle.validate",
                "change_metadata.regression",
                "change_metadata.validate",
                "guide_system.validate",
                "readme.validate",
                "readme.vision_markers",
                "selector.regression",
            }.issubset(selected_ids(payload))
        )
        self.assertFalse(payload["broad_smoke_required"])
        lifecycle_check = next(check for check in payload["selected_checks"] if check["id"] == "artifact_lifecycle.validate")
        self.assertIn("docs/plan.md", lifecycle_check["paths"])
        self.assertIn("docs/plan-archive.md", lifecycle_check["paths"])
        self.assertIn("docs/plans/2026-05-03-workflow-refactor.md", lifecycle_check["paths"])
        self.assertIn("docs/proposals/2026-05-01-workflow-refactor.md", lifecycle_check["paths"])
        self.assertIn("specs/rigorloop-workflow.md", lifecycle_check["paths"])
        self.assertIn("specs/rigorloop-workflow.test.md", lifecycle_check["paths"])

    def test_broad_smoke_sources_are_attributed(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-broad-smoke-"))
        self.addCleanupTree(temp_root)
        plan_path = temp_root / "docs" / "plans" / "active.md"
        plan_path.parent.mkdir(parents=True)
        plan_path.write_text("broad_smoke_required: true\n", encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("skills/code-review/SKILL.md",),
                broad_smoke=True,
                trigger_context_paths=(str(plan_path),),
                repo_root=temp_root,
            )
        )
        payload = result.to_json_dict()

        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        sources = payload["broad_smoke"]["sources"]
        self.assertIn({"type": "explicit_flag", "value": "--broad-smoke"}, sources)
        self.assertIn({"type": "active_plan", "path": "docs/plans/active.md"}, sources)

    def test_broad_smoke_sources_include_test_spec_and_review_resolution_context(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-broad-smoke-"))
        self.addCleanupTree(temp_root)
        context_files = {
            "docs/plans/active.md": "broad_smoke_required: true\n",
            "specs/example.test.md": "- broad smoke required before final verify\n",
            "docs/changes/example/review-resolution.md": "- broad smoke required by review closeout\n",
        }
        for relative_path, content in context_files.items():
            target = temp_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        result = select_validation(
            SelectionRequest(
                mode="explicit",
                paths=("skills/code-review/SKILL.md",),
                trigger_context_paths=tuple(context_files),
                repo_root=temp_root,
            )
        )
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        sources = payload["broad_smoke"]["sources"]
        self.assertIn({"type": "active_plan", "path": "docs/plans/active.md"}, sources)
        self.assertIn({"type": "test_spec", "path": "specs/example.test.md"}, sources)
        self.assertIn(
            {"type": "review_resolution", "path": "docs/changes/example/review-resolution.md"},
            sources,
        )

    def test_release_mode_selects_release_validation_and_broad_smoke(self) -> None:
        result = run_selector("--mode", "release", "--release-version", "v0.1.1")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertIn("release.validate", selected_ids(payload))
        self.assertIn("broad_smoke.repo", selected_ids(payload))
        self.assertTrue(payload["broad_smoke_required"])
        self.assertIn({"type": "mode", "value": "release"}, payload["broad_smoke"]["sources"])
        self.assertIn(
            {"type": "release_metadata", "path": "docs/releases/v0.1.1/release.yaml"},
            payload["broad_smoke"]["sources"],
        )

    def test_valid_pr_and_main_modes_use_git_range(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "skills" / "workflow" / "SKILL.md").write_text("# Workflow\n\nChanged\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "change skill"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        pr_result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(pr_result.returncode, 0, msg=pr_result.stderr)
        pr_payload = parse_stdout(pr_result)
        self.assertEqual(pr_payload["mode"], "pr")
        self.assertEqual(pr_payload["changed_paths"], ["skills/workflow/SKILL.md"])
        self.assertIn("skills.validate", selected_ids(pr_payload))
        self.assertFalse(pr_payload["broad_smoke_required"])

        main_result = run_selector("--mode", "main", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(main_result.returncode, 0, msg=main_result.stderr)
        main_payload = parse_stdout(main_result)
        self.assertEqual(main_payload["mode"], "main")
        self.assertEqual(main_payload["changed_paths"], ["skills/workflow/SKILL.md"])
        self.assertIn("skills.validate", selected_ids(main_payload))
        self.assertIn("broad_smoke.repo", selected_ids(main_payload))
        self.assertTrue(main_payload["broad_smoke_required"])
        self.assertIn({"type": "mode", "value": "main"}, main_payload["broad_smoke"]["sources"])

    def test_pr_mode_routes_adapter_distribution_test_script_to_adapter_checks(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "scripts").mkdir()
        adapter_test = repo / "scripts" / "test-adapter-distribution.py"
        adapter_test.write_text("print('adapter tests')\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add adapter test"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["changed_paths"], ["scripts/test-adapter-distribution.py"])
        self.assertIn(
            {"path": "scripts/test-adapter-distribution.py", "category": "adapters"},
            payload["classified_paths"],
        )
        self.assertTrue(
            {"adapters.regression", "adapters.drift", "adapters.validate"}.issubset(selected_ids(payload))
        )
        self.assertFalse(payload["blocking_results"])

    def test_pr_mode_routes_adapter_fixture_to_adapter_checks(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        fixture = repo / "tests" / "fixtures" / "adapters" / "example" / "SKILL.md"
        fixture.parent.mkdir(parents=True)
        fixture.write_text("# Adapter fixture\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add adapter fixture"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["changed_paths"], ["tests/fixtures/adapters/example/SKILL.md"])
        self.assertIn(
            {"path": "tests/fixtures/adapters/example/SKILL.md", "category": "adapters"},
            payload["classified_paths"],
        )
        self.assertTrue(
            {"adapters.regression", "adapters.drift", "adapters.validate"}.issubset(selected_ids(payload))
        )
        self.assertFalse(payload["blocking_results"])

    def test_pr_mode_routes_requirement_fidelity_spec_read_proof_paths(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        script = repo / "scripts" / "test-fidelity-gate-spec-reads.py"
        script.parent.mkdir(parents=True)
        script.write_text("print('spec read proof')\n", encoding="utf-8")
        fixture = (
            repo
            / "tests"
            / "fixtures"
            / "requirement-fidelity-gate"
            / "representative-reviews"
            / "r26-matrix-pilot"
            / "spec-read-log.json"
        )
        fixture.parent.mkdir(parents=True)
        fixture.write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add requirement fidelity spec-read proof"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertEqual(
            payload["changed_paths"],
            [
                "scripts/test-fidelity-gate-spec-reads.py",
                "tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json",
            ],
        )
        self.assertIn(
            {"path": "scripts/test-fidelity-gate-spec-reads.py", "category": "requirement-fidelity-spec-read"},
            payload["classified_paths"],
        )
        self.assertIn(
            {
                "path": "tests/fixtures/requirement-fidelity-gate/representative-reviews/r26-matrix-pilot/spec-read-log.json",
                "category": "requirement-fidelity-spec-read",
            },
            payload["classified_paths"],
        )
        self.assertIn("requirement_fidelity.spec_reads", selected_ids(payload))
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertFalse(payload["blocking_results"])

    def test_pr_mode_routes_readme_without_unclassified_block(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "README.md").write_text("# Example\n\nVision ownership wording.\n", encoding="utf-8")
        (repo / "skills" / "vision").mkdir(parents=True)
        (repo / "skills" / "vision" / "SKILL.md").write_text("# Vision\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add readme and vision skill"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertIn({"path": "README.md", "category": "readme"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
        self.assertFalse(payload["blocking_results"])

    def test_pr_mode_routes_root_vision_without_unclassified_block(self) -> None:
        repo = self.make_git_repo()
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "README.md").write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )
        (repo / "VISION.md").write_text("# Project Vision\n\n## Pitch\n\nExample vision.\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add root vision"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "ok")
        self.assertIn({"path": "VISION.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], [])
        self.assertTrue({"readme.validate", "readme.vision_markers"}.issubset(selected_ids(payload)))
        self.assertFalse(payload["blocking_results"])

    def test_pr_mode_blocks_reintroduced_retired_vision_as_unclassified(self) -> None:
        repo = self.make_git_repo()
        (repo / "VISION.md").write_text("# Project Vision\n\n## Pitch\n\nExample vision.\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "add canonical vision"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        base = self.git_output(repo, "rev-parse", "HEAD")
        (repo / "vision.md").write_text("# Legacy Vision\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "reintroduce legacy vision"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
        head = self.git_output(repo, "rev-parse", "HEAD")

        result = run_selector("--mode", "pr", "--base", base, "--head", head, cwd=repo)
        self.assertEqual(result.returncode, 2, msg=result.stderr)
        payload = parse_stdout(result)

        self.assertEqual(payload["status"], "blocked")
        self.assertNotIn({"path": "vision.md", "category": "vision"}, payload["classified_paths"])
        self.assertEqual(payload["unclassified_paths"], ["vision.md"])
        self.assertNotIn("readme.vision_markers", selected_ids(payload))
        self.assertIn("unclassified-path", {item["code"] for item in payload["blocking_results"]})
        self.assertNotIn("vision-path-conflict", {item["code"] for item in payload["blocking_results"]})

    def test_readme_validator_accepts_absent_or_valid_standalone_marker_block(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-readme-validator-"))
        self.addCleanupTree(temp_root)
        readme = temp_root / "README.md"
        readme.write_text(
            "# Example\n\nInline `<!-- vision:start -->` text is not a generated marker block.\n",
            encoding="utf-8",
        )

        absent = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(absent.returncode, 0, msg=absent.stdout + absent.stderr)

        readme.write_text(
            "# Example\n\n<!-- vision:start -->\nGenerated summary.\n<!-- vision:end -->\n",
            encoding="utf-8",
        )
        valid = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(valid.returncode, 0, msg=valid.stdout + valid.stderr)

        readme.write_text("# Example\n\n<!-- vision:start -->\nMissing end.\n", encoding="utf-8")
        malformed = subprocess.run(
            [sys.executable, str(README_VALIDATOR), str(readme), "--vision-markers"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(malformed.returncode, 0)

    def test_ci_wrapper_executes_selector_selected_path_and_root_checks(self) -> None:
        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md",
            "--path",
            "specs/test-layering-and-change-scoped-validation.md",
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertIn("Selector mode: explicit", output)
        self.assertIn("Preflight results:", output)
        self.assertIn("Run selected check: review_artifacts.validate", output)
        self.assertIn("Run selected check: artifact_lifecycle.validate", output)
        self.assertIn("Phase: focused", output)
        self.assertIn("Selected CI phase timing summary:", output)
        self.assertIn(
            "python scripts/validate-review-artifacts.py docs/changes/2026-04-25-test-layering-and-change-scoped-validation/",
            output,
        )
        self.assertIn(
            "python scripts/validate-artifact-lifecycle.py --mode explicit-paths",
            output,
        )
        self.assertIn(
            "--path docs/changes/2026-04-25-test-layering-and-change-scoped-validation/review-resolution.md",
            output,
        )
        self.assertIn(
            "--path specs/test-layering-and-change-scoped-validation.md",
            output,
        )

    def test_ci_wrapper_fails_on_blocked_selector_without_partial_execution(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                status="blocked",
                selected_checks=[
                    {
                        "id": "review_artifacts.validate",
                        "command": "python scripts/validate-review-artifacts.py docs/changes/example/",
                        "reason": "must not run when selector is blocked",
                        "affected_roots": ["docs/changes/example/"],
                    }
                ],
                blocking_results=[
                    {
                        "code": "unclassified-path",
                        "path": "experimental/runtime/example.txt",
                        "message": "changed path is not classified by the v1 selector",
                    }
                ],
            )
        )

        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "experimental/runtime/example.txt",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture), "RIGORLOOP_SELECTOR_FIXTURE_EXIT": "2"},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Selector status: blocked", output)
        self.assertIn("unclassified-path", output)
        self.assertNotIn("Run selected check: review_artifacts.validate", output)

    def test_ci_wrapper_rejects_fallback_and_malformed_selector_output(self) -> None:
        fallback_fixture = self.write_selector_fixture(self.minimal_selector_payload(status="fallback"))
        fallback = run_ci(
            "--mode",
            "explicit",
            "--path",
            "experimental/runtime/example.txt",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fallback_fixture), "RIGORLOOP_SELECTOR_FIXTURE_EXIT": "3"},
        )
        fallback_output = fallback.stdout + fallback.stderr

        self.assertNotEqual(fallback.returncode, 0)
        self.assertIn("Selector status: fallback", fallback_output)
        self.assertIn("fallback execution is not supported in v1", fallback_output)

        malformed_fixture = self.write_selector_fixture("not json")
        malformed = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(malformed_fixture)},
        )
        malformed_output = malformed.stdout + malformed.stderr

        self.assertNotEqual(malformed.returncode, 0)
        self.assertIn("Malformed selector JSON", malformed_output)

    def test_ci_wrapper_rejects_selector_command_mismatch(self) -> None:
        marker_root = Path(tempfile.mkdtemp(prefix="validation-selection-command-mismatch-"))
        self.addCleanupTree(marker_root)
        marker = marker_root / "executed"
        tampered_command = (
            f"{sys.executable} -c "
            f"\"from pathlib import Path; Path({str(marker)!r}).write_text('ran')\""
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "skills.validate",
                        "command": tampered_command,
                        "reason": "tampered selector command must not be trusted",
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("command does not match catalog", output)
        self.assertNotIn("Run selected check: skills.validate", output)
        self.assertFalse(marker.exists())

    def test_ci_wrapper_preserves_selected_command_failure(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "release.validate",
                        "command": "python scripts/validate-release-ci.py --version missing-version",
                        "reason": "fixture release version should fail validation",
                        "versions": ["missing-version"],
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "release",
            "--release-version",
            "missing-version",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Run selected check: release.validate", output)
        self.assertIn("Selected check release.validate failed", output)

    def test_ci_wrapper_jobs_one_uses_stable_summary_and_hides_success_output(self) -> None:
        workspace = self.make_ci_workspace()
        order_file = workspace / "order.txt"
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import os
import sys
from pathlib import Path

with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("skills-start\\n")
print("SKILLS_STDOUT")
print("SKILLS_STDERR", file=sys.stderr)
with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("skills-end\\n")
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            """
import os
import sys
from pathlib import Path

with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("adapters-start\\n")
print("ADAPTERS_STDOUT")
print("ADAPTERS_STDERR", file=sys.stderr)
with Path(os.environ["ORDER_FILE"]).open("a", encoding="utf-8") as handle:
    handle.write("adapters-end\\n")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            env={"ORDER_FILE": str(order_file)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(
            order_file.read_text(encoding="utf-8").splitlines(),
            ["skills-start", "skills-end", "adapters-start", "adapters-end"],
        )
        self.assertIn("Selected CI check summary:", output)
        self.assertIn("skills.regression | passed | ok |", output)
        self.assertIn("adapters.regression | passed | ok |", output)
        self.assertLess(
            output.index("skills.regression | passed | ok |"),
            output.index("adapters.regression | passed | ok |"),
        )
        self.assertNotIn("SKILLS_STDOUT", output)
        self.assertNotIn("ADAPTERS_STDERR", output)
        self.assertIn("Selected CI checks passed.", output)

    def test_ci_wrapper_parallel_safe_checks_run_concurrently_with_cap(self) -> None:
        workspace = self.make_ci_workspace()
        active_dir = workspace / "active"
        self.write_active_counter_script(workspace, "scripts/test-skill-validator.py", "skills")
        self.write_active_counter_script(workspace, "scripts/test-adapter-distribution.py", "adapters")
        self.write_active_counter_script(
            workspace,
            "scripts/test-artifact-lifecycle-validator.py",
            "artifact-lifecycle",
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                    self.selected_check(
                        "artifact_lifecycle.regression",
                        "python scripts/test-artifact-lifecycle-validator.py",
                    ),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "2",
            env={"ACTIVE_DIR": str(active_dir)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(self.read_max_active(active_dir), 2, msg=(active_dir / "events.txt").read_text(encoding="utf-8"))
        self.assertLess(
            output.index("skills.regression | passed | ok |"),
            output.index("adapters.regression | passed | ok |"),
        )
        self.assertLess(
            output.index("adapters.regression | passed | ok |"),
            output.index("artifact_lifecycle.regression | passed | ok |"),
        )

    def test_ci_wrapper_default_jobs_uses_cpu_minus_one_fixture(self) -> None:
        workspace = self.make_ci_workspace()
        active_dir = workspace / "active"
        self.write_active_counter_script(workspace, "scripts/test-skill-validator.py", "skills")
        self.write_active_counter_script(workspace, "scripts/test-adapter-distribution.py", "adapters")
        self.write_active_counter_script(
            workspace,
            "scripts/test-artifact-lifecycle-validator.py",
            "artifact-lifecycle",
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                    self.selected_check(
                        "artifact_lifecycle.regression",
                        "python scripts/test-artifact-lifecycle-validator.py",
                    ),
                ]
            )
        )

        one_cpu = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            env={
                "ACTIVE_DIR": str(active_dir),
                "RIGORLOOP_CI_CPU_COUNT_FIXTURE": "1",
            },
        )
        assert isinstance(one_cpu.stdout, str)
        self.assertEqual(one_cpu.returncode, 0, msg=one_cpu.stdout + one_cpu.stderr)
        self.assertEqual(self.read_max_active(active_dir), 1)

        shutil.rmtree(active_dir, ignore_errors=True)
        three_cpu = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            env={
                "ACTIVE_DIR": str(active_dir),
                "RIGORLOOP_CI_CPU_COUNT_FIXTURE": "3",
            },
        )
        assert isinstance(three_cpu.stdout, str)
        self.assertEqual(three_cpu.returncode, 0, msg=three_cpu.stdout + three_cpu.stderr)
        self.assertEqual(self.read_max_active(active_dir), 2)

    def test_ci_wrapper_non_allowlisted_checks_run_alone(self) -> None:
        workspace = self.make_ci_workspace()
        active_dir = workspace / "active"
        self.write_active_counter_script(workspace, "scripts/test-skill-validator.py", "skills-regression")
        self.write_active_counter_script(workspace, "scripts/validate-skills.py", "skills-validate")
        self.write_active_counter_script(workspace, "scripts/test-adapter-distribution.py", "adapters-regression")
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("skills.validate", "python scripts/validate-skills.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "4",
            env={"ACTIVE_DIR": str(active_dir)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(self.read_max_active(active_dir), 1)
        self.assertIn("skills.validate | passed | ok |", output)

    def test_ci_wrapper_parallel_default_waits_for_started_check_after_failure(self) -> None:
        workspace = self.make_ci_workspace()
        marker_dir = workspace / "markers"
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import os
import time
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "skills-started").write_text("started", encoding="utf-8")
deadline = time.monotonic() + 2
while not (marker_dir / "adapters-started").exists():
    if time.monotonic() > deadline:
        raise SystemExit(9)
    time.sleep(0.02)
raise SystemExit(7)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            """
import os
import time
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "adapters-started").write_text("started", encoding="utf-8")
time.sleep(0.3)
(marker_dir / "adapters-finished").write_text("finished", encoding="utf-8")
print("adapters finished")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "2",
            env={"MARKER_DIR": str(marker_dir)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((marker_dir / "adapters-finished").exists(), msg=output)
        self.assertIn("skills.regression | exited | exit code 7 |", output)
        self.assertIn("adapters.regression | passed | ok |", output)

    def test_ci_wrapper_fail_fast_reports_queued_checks_not_started(self) -> None:
        workspace = self.make_ci_workspace()
        marker_dir = workspace / "markers"
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import os
import time
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "skills-started").write_text("started", encoding="utf-8")
deadline = time.monotonic() + 2
while not (marker_dir / "adapters-started").exists():
    if time.monotonic() > deadline:
        raise SystemExit(9)
    time.sleep(0.02)
raise SystemExit(7)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            """
import os
import time
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "adapters-started").write_text("started", encoding="utf-8")
time.sleep(0.3)
(marker_dir / "adapters-finished").write_text("finished", encoding="utf-8")
print("adapters finished")
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "scripts/test-artifact-lifecycle-validator.py",
            """
import os
from pathlib import Path

marker_dir = Path(os.environ["MARKER_DIR"])
marker_dir.mkdir(parents=True, exist_ok=True)
(marker_dir / "artifact-started").write_text("started", encoding="utf-8")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                    self.selected_check(
                        "artifact_lifecycle.regression",
                        "python scripts/test-artifact-lifecycle-validator.py",
                    ),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "2",
            "--fail-fast",
            env={"MARKER_DIR": str(marker_dir)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((marker_dir / "adapters-finished").exists(), msg=output)
        self.assertFalse((marker_dir / "artifact-started").exists(), msg=output)
        self.assertIn("skills.regression | exited | exit code 7 |", output)
        self.assertIn("adapters.regression | passed | ok |", output)
        self.assertIn(
            "artifact_lifecycle.regression | not started | fail-fast cancelled remaining queue | 0.00s",
            output,
        )

    def test_ci_wrapper_run_to_completion_reports_failed_output_after_summary(self) -> None:
        workspace = self.make_ci_workspace()
        marker = workspace / "second-ran.txt"
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import sys

print("FIRST_STDOUT")
print("FIRST_STDERR", file=sys.stderr)
raise SystemExit(7)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            """
import os
from pathlib import Path

Path(os.environ["SECOND_MARKER"]).write_text("ran", encoding="utf-8")
print("SECOND_STDOUT")
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            env={"SECOND_MARKER": str(marker)},
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(marker.exists(), msg=output)
        self.assertIn("skills.regression | exited | exit code 7 |", output)
        self.assertIn("adapters.regression | passed | ok |", output)
        self.assertLess(output.index("Selected CI check summary:"), output.index("Failed selected check output:"))
        self.assertIn("==> skills.regression (exited)", output)
        self.assertIn("--- stdout ---", output)
        self.assertIn("FIRST_STDOUT", output)
        self.assertIn("--- stderr ---", output)
        self.assertIn("FIRST_STDERR", output)
        self.assertNotIn("SECOND_STDOUT", output)

    def test_ci_wrapper_verbose_prints_successful_output_in_stable_order(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            "import sys\nprint('SKILL_VERBOSE_STDOUT')\nprint('SKILL_VERBOSE_STDERR', file=sys.stderr)\n",
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            "print('ADAPTER_VERBOSE_STDOUT')\n",
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            "--verbose",
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertIn("Selected check output:", output)
        self.assertLess(output.index("==> skills.regression (passed)"), output.index("==> adapters.regression (passed)"))
        self.assertIn("SKILL_VERBOSE_STDOUT", output)
        self.assertIn("SKILL_VERBOSE_STDERR", output)
        self.assertIn("ADAPTER_VERBOSE_STDOUT", output)

    def test_broad_smoke_default_success_captures_child_output_and_prints_aggregate(self) -> None:
        workspace = self.make_broad_smoke_workspace()

        result = run_ci(
            "--mode",
            "broad-smoke",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        nonempty_lines = [line for line in output.splitlines() if line.strip()]
        self.assertEqual(len(nonempty_lines), 1, msg=output)
        self.assertRegex(nonempty_lines[0], r"^\[PASS\] broad-smoke: 12 checks passed in \d+(?:\.\d+)?s$")
        self.assertNotIn("STDOUT marker", output)
        self.assertNotIn("STDERR marker", output)
        self.assertNotIn("==>", output)
        self.assertNotIn("--quiet", output)

    def test_ci_wrapper_duration_reporting_does_not_use_bash_seconds(self) -> None:
        ci_text = CI.read_text(encoding="utf-8")

        self.assertNotIn("$SECONDS", ci_text)
        self.assertIn("elapsed_seconds_since", ci_text)

    def test_broad_smoke_failure_prints_command_exit_duration_and_captured_output(self) -> None:
        workspace = self.make_broad_smoke_workspace(failing_child="scripts/test-skill-validator.py")

        result = run_ci(
            "--mode",
            "broad-smoke",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 7, msg=output)
        self.assertRegex(output, r"\[FAIL\] Run skill validator fixtures: exit 7 in \d+(?:\.\d+)?s")
        self.assertIn("Command:\npython scripts/test-skill-validator.py", output)
        self.assertIn("Captured output:", output)
        stdout_index = output.index("test-skill-validator.py STDOUT marker")
        stderr_index = output.index("test-skill-validator.py STDERR marker")
        self.assertLess(stdout_index, stderr_index)

    def test_broad_smoke_verbose_prints_successful_child_output_in_order(self) -> None:
        workspace = self.make_broad_smoke_workspace()

        result = run_ci(
            "--mode",
            "broad-smoke",
            "--verbose",
            script=workspace / "scripts" / "ci.sh",
            cwd=workspace,
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertRegex(output, r"\[PASS\] broad-smoke: 12 checks passed in \d+(?:\.\d+)?s")
        self.assertLess(output.index("validate-skills.py STDOUT marker"), output.index("test-skill-validator.py STDOUT marker"))
        self.assertIn("validate-skills.py STDERR marker", output)
        self.assertIn("test-skill-validator.py STDERR marker", output)

    def test_broad_smoke_child_classification_covers_ci_children(self) -> None:
        ci_check_ids = self.extract_broad_smoke_run_check_ids(CI.read_text(encoding="utf-8"))
        rows = self.parse_broad_smoke_classification_rows()
        row_ids = [row["Check ID"] for row in rows]

        self.assertEqual(row_ids, ci_check_ids)
        for row in rows:
            with self.subTest(check_id=row["Check ID"]):
                for field in BROAD_SMOKE_REQUIRED_CLASSIFICATION_FIELDS:
                    self.assertTrue(row[field], msg=field)
                self.assertIn(
                    row["Parallel-safe candidate"],
                    {"no", "needs-follow-up", "candidate-after-separate-approval"},
                )
                self.assertIn(row["Classification confidence"], {"high", "medium", "low"})

    def test_broad_smoke_classification_blocks_unsafe_candidate_claims(self) -> None:
        rows = self.parse_broad_smoke_classification_rows()

        for row in rows:
            with self.subTest(check_id=row["Check ID"]):
                has_writes = row["Writes"].lower() != "none"
                has_shared_outputs = row["Shared outputs"].lower() != "none"
                low_confidence = row["Classification confidence"] == "low"
                if has_writes or has_shared_outputs or low_confidence:
                    self.assertIn(row["Parallel-safe candidate"], NON_CANDIDATE_VALUES | {"needs-follow-up"})

    def test_broad_smoke_classification_keeps_runtime_sequential(self) -> None:
        ci_text = CI.read_text(encoding="utf-8")
        broad_smoke_body = self.extract_ci_functions(ci_text)["run_broad_smoke"]

        self.assertNotIn("ThreadPoolExecutor", broad_smoke_body)
        self.assertNotIn("run_parallel_safe_chunk", broad_smoke_body)
        self.assertNotIn("parallel_safe", broad_smoke_body)
        self.assertNotRegex(broad_smoke_body, r"(?m)^\s*run_check\b.*&\s*$")
        self.assertEqual(
            self.extract_broad_smoke_run_check_ids(ci_text),
            [row["Check ID"] for row in self.parse_broad_smoke_classification_rows()],
        )

    def test_broad_smoke_parallel_classification_reconciles_with_ci_inventory(self) -> None:
        result = self.run_broad_smoke_classification_validator()

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("broad-smoke classification validation passed", result.stdout)

    def test_broad_smoke_parallel_classification_fails_on_stale_command(self) -> None:
        classification = self.load_broad_smoke_parallel_classification()
        children = classification["children"]
        assert isinstance(children, list)
        stale = dict(children[0])
        stale["command"] = "python scripts/validate-skills.py --unexpected"
        mutated_children = [stale, *children[1:]]
        mutated = dict(classification)
        mutated["children"] = mutated_children
        temp_path = Path(tempfile.mkdtemp(prefix="broad-smoke-stale-classification-")) / "classification.yaml"
        self.addCleanupTree(temp_path.parent)
        temp_path.write_text(yaml.safe_dump(mutated, sort_keys=False), encoding="utf-8")

        result = self.run_broad_smoke_classification_validator(temp_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale command", result.stderr)

    def test_broad_smoke_parallel_classification_fails_on_contradictory_parallel_candidate(self) -> None:
        classification = self.load_broad_smoke_parallel_classification()
        children = classification["children"]
        assert isinstance(children, list)
        contradictory = dict(children[0])
        contradictory["side_effects"] = dict(contradictory["side_effects"])
        contradictory["side_effects"]["writes_shared_temp"] = True
        mutated = dict(classification)
        mutated["children"] = [contradictory, *children[1:]]
        temp_path = Path(tempfile.mkdtemp(prefix="broad-smoke-contradictory-classification-")) / "classification.yaml"
        self.addCleanupTree(temp_path.parent)
        temp_path.write_text(yaml.safe_dump(mutated, sort_keys=False), encoding="utf-8")

        result = self.run_broad_smoke_classification_validator(temp_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("blocking side-effect fields", result.stderr)

    def test_broad_smoke_parallel_baseline_artifact_has_child_timing_shape(self) -> None:
        self.assertTrue(BROAD_SMOKE_PARALLEL_BASELINE.exists(), msg=str(BROAD_SMOKE_PARALLEL_BASELINE))
        with BROAD_SMOKE_PARALLEL_BASELINE.open(encoding="utf-8") as handle:
            baseline = yaml.safe_load(handle)
        self.assertEqual(baseline["scenario"], "broad-smoke-sequential-baseline")
        children = baseline["children"]
        self.assertEqual(
            [child["check_id"] for child in children],
            [child["check_id"] for child in self.load_broad_smoke_parallel_classification()["children"]],
        )
        for child in children:
            with self.subTest(check_id=child["check_id"]):
                for field in ("command", "order", "duration_ms", "result", "output_bytes"):
                    self.assertIn(field, child)

    def test_broad_smoke_wrapper_mode_consistency_guard_is_enforced(self) -> None:
        self.assert_ci_wrapper_consistency_guard_passes(CI.read_text(encoding="utf-8"))
        self.assert_ci_wrapper_consistency_guard_fails(
            """
run_check() {
  local label="$1"
  shift

  echo "==> $label"
  "$@"
}
""".lstrip()
        )
        self.assert_ci_wrapper_consistency_guard_fails(
            """
run_check() {
  local label="$1"
  shift
  output="$("$@" 2>&1)"
  status=$?
  if [ "$status" -ne 0 ]; then
    printf '%s\n' "Captured output:"
    printf '%s\n' "$output"
  fi
  if [ "$verbose" -eq 1 ]; then
    printf '%s\n' "$output"
  fi
  return "$status"
}

run_broad_smoke() {
  run_check "metadata" python scripts/test-change-metadata-validator.py
}

run_new_validation_mode() {
  python scripts/test-change-metadata-validator.py
}

case "$mode" in
  local|explicit|pr|main|release)
    run_selected_mode
    ;;
  broad-smoke)
    run_broad_smoke
    ;;
esac
""".lstrip(),
            r"mode 'new_validation_mode' runs validation producer without capture policy",
        )
        self.assert_ci_wrapper_consistency_guard_fails(
            """
run_check() {
  local label="$1"
  shift
  output="$("$@" 2>&1)"
  status=$?
  if [ "$status" -ne 0 ]; then
    printf '%s\n' "Captured output:"
    printf '%s\n' "$output"
  fi
  if [ "$verbose" -eq 1 ]; then
    printf '%s\n' "$output"
  fi
  return "$status"
}

run_broad_smoke() {
  run_check "metadata" python scripts/test-change-metadata-validator.py
}

run_direct_streaming_mode() {
  "$@"
}

case "$mode" in
  local|explicit|pr|main|release)
    run_selected_mode
    ;;
  broad-smoke)
    run_broad_smoke
    ;;
esac
""".lstrip(),
            r"mode 'direct_streaming_mode' streams child command directly",
        )

    def test_change_metadata_validator_default_success_is_compact(self) -> None:
        result = run_change_metadata_test(CHANGE_METADATA_PASSING_TEST)
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 0, msg=output)
        self.assertEqual(result.stderr, "")
        nonempty_lines = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual(len(nonempty_lines), 1, msg=output)
        self.assertRegex(
            nonempty_lines[0],
            r"^\[PASS\] test-change-metadata-validator: 1 passed in \d+(?:\.\d+)?s$",
        )
        self.assertNotIn("test_valid_basic_fixture_passes", output)
        self.assertNotIn(" ... ok", output)

    def test_change_metadata_validator_default_failure_is_actionable(self) -> None:
        result = run_change_metadata_test(
            CHANGE_METADATA_FAILING_TEST,
            env={"RIGORLOOP_CHANGE_METADATA_FAILURE_FIXTURE": "1"},
        )
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 1, msg=output)
        self.assertIn("[FAIL] test-change-metadata-validator: 1 failed, 0 passed", output)
        self.assertIn("FAILED ChangeMetadataValidatorFixtureTests.test_output_contract_fixture_failure", output)
        self.assertIn("AssertionError: intentional output-contract failure", output)
        self.assertIn("scripts/test-change-metadata-validator.py:", output)
        self.assertNotIn("test_valid_basic_fixture_passes", output)

    def test_change_metadata_validator_verbose_preserves_full_detail(self) -> None:
        for flag in ("--verbose", "-v"):
            with self.subTest(flag=flag):
                result = run_change_metadata_test(flag, CHANGE_METADATA_PASSING_TEST)
                output = result.stdout + result.stderr

                self.assertEqual(result.returncode, 0, msg=output)
                self.assertIn("test_valid_basic_fixture_passes", output)
                self.assertIn(" ... ok", output)
                self.assertIn("Ran 1 test", output)
                self.assertIn("OK", output)

    def test_change_metadata_validator_quiet_compatibility_is_preserved(self) -> None:
        for flag in ("--quiet", "-q"):
            with self.subTest(flag=flag):
                result = run_change_metadata_test(flag, CHANGE_METADATA_PASSING_TEST)

                self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertIn("Ran 1 test", result.stderr)
                self.assertIn("OK", result.stderr)
                self.assertNotIn("[PASS] test-change-metadata-validator", result.stderr)

    def test_change_metadata_validator_zero_selected_tests_fail(self) -> None:
        result = run_change_metadata_test("-k", "no_such_test_name")
        output = result.stdout + result.stderr

        self.assertEqual(result.returncode, 1, msg=output)
        self.assertIn(
            "[FAIL] test-change-metadata-validator: 0 tests run; expected at least 1 selected test",
            output,
        )

    def test_ci_wrapper_reports_decode_failures_without_emitting_invalid_bytes(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import sys

sys.stdout.buffer.write(b"valid-before-stdout\\n")
sys.stdout.buffer.write(b"bad-stdout-\\xff\\n")
sys.stderr.buffer.write(b"bad-stderr-\\xfe\\n")
raise SystemExit(1)
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            text=False,
        )
        assert isinstance(result.stdout, bytes)
        combined = result.stdout + result.stderr
        output = combined.decode("utf-8")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skills.regression | exited | exit code 1; stdout decode error; stderr decode error |", output)
        self.assertIn("--- stdout (decode error; replacement text) ---", output)
        self.assertIn("bad-stdout-", output)
        self.assertIn("--- stderr (decode error; replacement text) ---", output)
        self.assertIn("bad-stderr-", output)

    def test_ci_wrapper_keeps_large_output_isolated_per_check(self) -> None:
        workspace = self.make_ci_workspace()
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            """
import sys

sys.stdout.write("SKILLS_STDOUT_BEGIN\\n")
sys.stdout.write("skills-stdout-line\\n" * 5000)
sys.stderr.write("skills-stderr-line\\n" * 5000)
sys.stdout.write("SKILLS_STDOUT_END\\n")
raise SystemExit(2)
""".lstrip(),
        )
        self.write_fake_script(
            workspace,
            "scripts/test-adapter-distribution.py",
            """
import sys

sys.stdout.write("ADAPTERS_STDOUT_BEGIN\\n")
sys.stdout.write("adapters-stdout-line\\n" * 5000)
sys.stderr.write("adapters-stderr-line\\n" * 5000)
sys.stdout.write("ADAPTERS_STDOUT_END\\n")
raise SystemExit(3)
""".lstrip(),
        )
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                    self.selected_check("adapters.regression", ADAPTER_REGRESSION_COMMAND),
                ]
            )
        )

        result = self.run_workspace_ci(
            workspace,
            fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
        )
        assert isinstance(result.stdout, str)
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        skills_start = output.index("==> skills.regression (exited)")
        adapters_start = output.index("==> adapters.regression (exited)")
        skills_section = output[skills_start:adapters_start]
        adapters_section = output[adapters_start:]

        self.assertIn("skills.regression | exited | exit code 2 |", output)
        self.assertIn("adapters.regression | exited | exit code 3 |", output)
        self.assertIn("SKILLS_STDOUT_BEGIN", skills_section)
        self.assertIn("skills-stderr-line", skills_section)
        self.assertNotIn("ADAPTERS_STDOUT_BEGIN", skills_section)
        self.assertIn("ADAPTERS_STDOUT_BEGIN", adapters_section)
        self.assertIn("adapters-stderr-line", adapters_section)
        self.assertNotIn("SKILLS_STDOUT_BEGIN", adapters_section)

    def test_ci_wrapper_timeout_and_signal_failures_have_distinct_statuses(self) -> None:
        workspace = self.make_ci_workspace()
        self.assertRegex(
            (workspace / "scripts" / "ci.sh").read_text(encoding="utf-8"),
            r"(?m)^DEFAULT_TIMEOUT_SECONDS=300$",
        )
        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            "import time\nprint('before-timeout', flush=True)\ntime.sleep(5)\n",
        )
        timeout_fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                ]
            )
        )

        timed_out = self.run_workspace_ci(
            workspace,
            timeout_fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
            "--timeout",
            "1",
        )
        assert isinstance(timed_out.stdout, str)
        timeout_output = timed_out.stdout + timed_out.stderr

        self.assertNotEqual(timed_out.returncode, 0)
        self.assertIn("skills.regression | timed out | timeout after 1s |", timeout_output)
        self.assertIn("before-timeout", timeout_output)

        self.write_fake_script(
            workspace,
            "scripts/test-skill-validator.py",
            f"import os, signal\nos.kill(os.getpid(), {signal.SIGTERM})\n",
        )
        signal_fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    self.selected_check("skills.regression", "python scripts/test-skill-validator.py"),
                ]
            )
        )

        killed = self.run_workspace_ci(
            workspace,
            signal_fixture,
            "--mode",
            "explicit",
            "--path",
            "scripts/test-skill-validator.py",
            "--jobs",
            "1",
        )
        assert isinstance(killed.stdout, str)
        signal_output = killed.stdout + killed.stderr

        self.assertNotEqual(killed.returncode, 0)
        self.assertIn("skills.regression | killed | signal SIGTERM (15) |", signal_output)

    def test_ci_wrapper_reports_unavailable_selected_command(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-ci-missing-"))
        self.addCleanupTree(temp_root)
        (temp_root / "scripts").mkdir()
        shutil.copy2(CI, temp_root / "scripts" / "ci.sh")
        shutil.copy2(ROOT / "scripts" / "validation_selection.py", temp_root / "scripts" / "validation_selection.py")
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "release.validate",
                        "command": "python scripts/validate-release-ci.py --version v0.1.1",
                        "reason": "fixture command should be unavailable in the temporary workspace",
                        "versions": ["v0.1.1"],
                    }
                ]
            )
        )

        result = run_ci(
            "--mode",
            "release",
            "--release-version",
            "v0.1.1",
            env={"RIGORLOOP_SELECTOR_FIXTURE": str(fixture)},
            script=temp_root / "scripts" / "ci.sh",
            cwd=temp_root,
        )
        output = result.stdout + result.stderr

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Run selected check: release.validate", output)
        self.assertIn("release.validate | unavailable | command unavailable: scripts/validate-release-ci.py |", output)

    def test_ci_wrapper_forwards_mode_arguments_to_selector(self) -> None:
        fixture = self.write_selector_fixture(self.minimal_selector_payload())
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-trace-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            (
                ["--mode", "pr", "--base", "base-sha", "--head", "head-sha"],
                ["--mode", "pr", "--base", "base-sha", "--head", "head-sha"],
            ),
            (
                ["--mode", "main", "--base", "before-sha", "--head", "after-sha"],
                ["--mode", "main", "--base", "before-sha", "--head", "after-sha"],
            ),
            (
                ["--mode", "release", "--release-version", "v0.1.1"],
                ["--mode", "release", "--release-version", "v0.1.1"],
            ),
            (
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md", "--broad-smoke"],
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md", "--broad-smoke"],
            ),
        ]

        for args, expected in cases:
            with self.subTest(args=args):
                trace.write_text("", encoding="utf-8")
                result = run_ci(
                    *args,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                    },
                )
                output = result.stdout + result.stderr

                self.assertEqual(result.returncode, 0, msg=output)
                traced = trace.read_text(encoding="utf-8").splitlines()
                self.assertEqual(traced[-len(expected) :], expected)

    def test_ci_wrapper_accepts_execution_flags_without_forwarding_to_selector(self) -> None:
        fixture = self.write_selector_fixture(self.minimal_selector_payload())
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-flags-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            (
                [
                    "--mode",
                    "explicit",
                    "--path",
                    "skills/code-review/SKILL.md",
                    "--jobs",
                    "2",
                    "--timeout",
                    "60",
                    "--fail-fast",
                    "--verbose",
                ],
                ["--mode", "explicit", "--path", "skills/code-review/SKILL.md"],
            ),
            (
                [
                    "--mode",
                    "pr",
                    "--base",
                    "base-sha",
                    "--head",
                    "head-sha",
                    "--jobs",
                    "1",
                    "--timeout",
                    "120",
                ],
                ["--mode", "pr", "--base", "base-sha", "--head", "head-sha"],
            ),
            (
                [
                    "--mode",
                    "main",
                    "--base",
                    "before-sha",
                    "--head",
                    "after-sha",
                    "--verbose",
                ],
                ["--mode", "main", "--base", "before-sha", "--head", "after-sha"],
            ),
            (
                [
                    "--mode",
                    "release",
                    "--release-version",
                    "v0.1.1",
                    "--fail-fast",
                    "--jobs",
                    "3",
                ],
                ["--mode", "release", "--release-version", "v0.1.1"],
            ),
        ]

        for args, expected in cases:
            with self.subTest(args=args):
                trace.write_text("", encoding="utf-8")
                result = run_ci(
                    *args,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                    },
                )
                output = result.stdout + result.stderr

                self.assertEqual(result.returncode, 0, msg=output)
                traced = trace.read_text(encoding="utf-8").splitlines()
                self.assertEqual(traced[-len(expected) :], expected)

        broad_smoke = run_ci(
            "--mode",
            "broad-smoke",
            "--jobs",
            "1",
            "--timeout",
            "60",
            "--fail-fast",
            "--verbose",
            env={"RIGORLOOP_CI_BROAD_SMOKE_STUB": "1"},
        )
        self.assertEqual(broad_smoke.returncode, 0, msg=broad_smoke.stdout + broad_smoke.stderr)
        self.assertIn("Broad smoke stub", broad_smoke.stdout + broad_smoke.stderr)

    def test_ci_wrapper_rejects_invalid_execution_flags_before_selector(self) -> None:
        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "broad_smoke.repo",
                        "command": "bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped",
                        "reason": "must not run when wrapper arguments are invalid",
                    }
                ]
            )
        )
        trace = Path(tempfile.mkdtemp(prefix="validation-selection-invalid-flags-")) / "argv.txt"
        self.addCleanupTree(trace.parent)

        cases = [
            ("--jobs", "0"),
            ("--jobs", "-1"),
            ("--jobs", "abc"),
            ("--jobs", ""),
            ("--jobs", "unlimited"),
            ("--timeout", "0"),
            ("--timeout", "-1"),
            ("--timeout", "abc"),
            ("--timeout", ""),
        ]

        for flag, value in cases:
            with self.subTest(flag=flag, value=value):
                if trace.exists():
                    trace.unlink()
                result = run_ci(
                    "--mode",
                    "explicit",
                    "--path",
                    "skills/code-review/SKILL.md",
                    flag,
                    value,
                    env={
                        "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                        "RIGORLOOP_CI_SELECTOR_ARGV_FILE": str(trace),
                        "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
                    },
                )
                output = result.stdout + result.stderr

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"Invalid {flag}", output)
                self.assertFalse(trace.exists(), msg=output)
                self.assertNotIn("Selector mode:", output)
                self.assertNotIn("Run selected check:", output)

    def test_ci_wrapper_delegates_broad_smoke_non_recursively(self) -> None:
        malformed_fixture = self.write_selector_fixture("not json")
        direct = run_ci(
            "--mode",
            "broad-smoke",
            env={
                "RIGORLOOP_SELECTOR_FIXTURE": str(malformed_fixture),
                "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
            },
        )
        direct_output = direct.stdout + direct.stderr

        self.assertEqual(direct.returncode, 0, msg=direct_output)
        self.assertIn("Broad smoke stub", direct_output)
        self.assertNotIn("Malformed selector JSON", direct_output)

        fixture = self.write_selector_fixture(
            self.minimal_selector_payload(
                selected_checks=[
                    {
                        "id": "broad_smoke.repo",
                        "command": "bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped",
                        "reason": "Broad smoke is required by an authoritative source.",
                    }
                ]
            )
        )
        selected = run_ci(
            "--mode",
            "explicit",
            "--path",
            "skills/code-review/SKILL.md",
            "--verbose",
            env={
                "RIGORLOOP_SELECTOR_FIXTURE": str(fixture),
                "RIGORLOOP_CI_BROAD_SMOKE_STUB": "1",
            },
        )
        selected_output = selected.stdout + selected.stderr

        self.assertEqual(selected.returncode, 0, msg=selected_output)
        self.assertIn("Run selected check: broad_smoke.repo", selected_output)
        self.assertIn("Broad smoke stub", selected_output)

    def test_workflow_guidance_aligns_with_validation_layering_contract(self) -> None:
        expectations = {
            "specs/rigorloop-workflow.md": [
                "targeted proof",
                "broad smoke",
                "manual proof",
                "scripts/select-validation.py",
                "broad_smoke_required",
                "skills.validate",
                "broad_smoke.repo",
            ],
            "docs/workflows.md": [
                "targeted proof",
                "broad smoke",
                "Validation owner surfaces",
                "contributor-facing validation guidance",
                "executable check selection",
                "concise local validation reminders",
                "change-specific validation requirements",
                "finding-specific validation requirements",
                "release-specific validation requirements",
                "scripts/select-validation.py",
                "scripts/ci.sh --mode explicit",
                "scripts/ci.sh --mode broad-smoke",
                "--jobs",
                "--jobs 1",
                "--timeout",
                "--fail-fast",
                "--verbose",
                "skills.validate",
                "review_artifacts.validate",
                "broad_smoke.repo",
                "does not imply broad smoke for every PR",
            ],
            "skills/implement/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "project's validation selector",
                "selected checks",
                "skills.validate",
            ],
            "skills/code-review/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "selected checks",
                "direct proof",
            ],
            "skills/verify/SKILL.md": [
                "verify-report.md",
                "manual by design",
                "manual proof",
                "release metadata",
                "not-run",
                "project's broad validation command",
                "broad_smoke_required",
            ],
            "skills/workflow/SKILL.md": [
                "targeted proof",
                "broad smoke",
                "manual proof",
                "broad_smoke.sources",
                "verify-report.md",
            ],
        }

        for path, required_terms in expectations.items():
            with self.subTest(path=path):
                content = (ROOT / path).read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, content)

    def test_hosted_ci_remains_thin_and_matrix_free(self) -> None:
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

        self.assertIn("bash scripts/ci.sh --mode pr", workflow)
        self.assertIn("bash scripts/ci.sh --mode main", workflow)
        forbidden_terms = [
            "matrix:",
            "check-id:",
            "fromJson",
            "scripts/select-validation.py",
            "actions/cache",
            "distributed",
            "sandbox",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, workflow)

    def test_local_mode_discovers_tracked_and_untracked_git_paths(self) -> None:
        repo = self.make_git_repo()
        (repo / "skills" / "workflow" / "SKILL.md").write_text("# Workflow\n\nChanged\n", encoding="utf-8")
        (repo / "docs" / "changes" / "2026-04-25-local").mkdir(parents=True)
        (repo / "docs" / "changes" / "2026-04-25-local" / "change.yaml").write_text(
            "change_id: 2026-04-25-local\n",
            encoding="utf-8",
        )

        result = select_validation(SelectionRequest(mode="local", repo_root=repo))
        payload = result.to_json_dict()

        self.assertEqual(result.status, "ok")
        self.assertIn("skills/workflow/SKILL.md", payload["changed_paths"])
        self.assertIn("docs/changes/2026-04-25-local/change.yaml", payload["changed_paths"])
        self.assertIn("skills.validate", selected_ids(payload))
        self.assertIn("change_metadata.validate", selected_ids(payload))

    def test_normalize_path_rejects_outside_repository_paths(self) -> None:
        temp_root = Path(tempfile.mkdtemp(prefix="validation-selection-paths-"))
        self.addCleanupTree(temp_root)
        outside = temp_root.parent / "outside.txt"

        normalized = normalize_path(str(outside), repo_root=temp_root)
        self.assertFalse(normalized.ok)
        self.assertEqual(normalized.blocking_code, "outside-repository-path")

    def test_output_contract_red_tests_are_unmasked_and_separate(self) -> None:
        source = Path(__file__).read_text(encoding="utf-8")
        contract_section = source.split("class ScriptOutputContractTests", 1)[1].split(
            "class ValidationSelectionTests",
            1,
        )[0]

        self.assertNotIn("@unittest.expectedFailure", contract_section)
        self.assertIn("class ScriptOutputContractTests", source)


if __name__ == "__main__":
    raise SystemExit(run_script_tests(sys.argv[1:]))
