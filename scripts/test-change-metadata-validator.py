#!/usr/bin/env python3
"""Fixture-driven tests for change metadata validation."""

from __future__ import annotations

import importlib.util
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
FIXTURES = ROOT / "tests" / "fixtures" / "change-metadata"
SKILL_VALIDATOR_EXAMPLE = ROOT / "docs" / "changes" / "0001-skill-validator" / "change.yaml"
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
    maxDiff = None

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

    def test_valid_basic_fixture_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "valid-basic" / "change.yaml")

    def test_compact_valid_fixture_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "compact-valid" / "change.yaml")

    def test_compact_path_variable_helpers(self) -> None:
        validator = load_validator_module()
        self.assertEqual(
            validator.derive_compact_slug("2026-05-21-compact-change-validation-metadata"),
            "compact-change-validation-metadata",
        )
        self.assertEqual(
            validator.resolve_compact_path_template(
                "docs/changes/{change_id}/notes/{{draft}}.md",
                {
                    "change_id": "2026-05-21-compact-change-validation-metadata",
                    "slug": "compact-change-validation-metadata",
                },
            ),
            "docs/changes/2026-05-21-compact-change-validation-metadata/notes/{draft}.md",
        )
        with self.assertRaisesRegex(validator.MetadataValidationError, r"unmatched"):
            validator.resolve_compact_path_template("docs/{change_id", {"change_id": "x"})
        with self.assertRaisesRegex(validator.MetadataValidationError, r"unsupported interpolation"):
            validator.resolve_compact_path_template("docs/${change_id}", {"change_id": "x"})
        with self.assertRaisesRegex(validator.MetadataValidationError, r"unknown variable"):
            validator.resolve_compact_path_template("docs/{missing}", {"change_id": "x"})

    def test_compact_path_safety_helper_rejects_unsafe_values(self) -> None:
        validator = load_validator_module()
        unsafe_values = [
            "/tmp/change.yaml",
            r"C:\Users\alice\change.yaml",
            "~/change.yaml",
            "../change.yaml",
            "example.com/change.yaml",
            "https://example.com/change.yaml",
            "https://user:pass@example.com/change.yaml",
            "docs/changes/token=value/change.yaml",
            "home/alice/change.yaml",
        ]
        for value in unsafe_values:
            with self.subTest(value=value):
                self.assertTrue(
                    validator.validate_repo_relative_path(value, "path_vars.example"),
                    msg=f"expected {value!r} to be unsafe",
                )

    def test_compact_bundle_command_helper_rejects_unsafe_values(self) -> None:
        validator = load_validator_module()
        cases = [
            (
                "python $HOME/private/validate.py",
                "unsafe machine-local path",
            ),
            (
                r"python C:\Users\alice\validate.py",
                "unsafe machine-local path",
            ),
            (
                "curl https://user:password@example.com/validate",
                "credential-bearing URL",
            ),
            (
                "python scripts/check.py --token ghp_example_secret",
                "secret-like value",
            ),
        ]
        for command, expected in cases:
            with self.subTest(command=command):
                errors = validator.validate_compact_bundle_command_safety(
                    "validation_bundles.example",
                    command,
                    {},
                )
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_compact_invalid_fixtures_fail(self) -> None:
        cases = [
            (
                "compact-invalid-missing-section",
                "validation_events: missing required compact field",
            ),
            (
                "compact-invalid-mixed-shape",
                "mixed legacy and compact validation metadata",
            ),
            (
                "compact-invalid-undefined-bundle",
                "validation_events[0].bundles[0]: unknown validation bundle 'metadata'",
            ),
            (
                "compact-invalid-result-enum",
                "validation_events[0].result: expected one of",
            ),
            (
                "compact-invalid-noninteger-count",
                "validation_events[0].counts.reviews: expected integer",
            ),
            (
                "compact-invalid-fail-without-details",
                "validation_events[0].failures: required when result is fail",
            ),
            (
                "compact-invalid-blocked-without-details",
                "validation_events[0].failures: required when result is blocked",
            ),
            (
                "compact-invalid-conflicting-slug",
                "path_vars.slug: must match derived slug",
            ),
            (
                "compact-invalid-recursive-var",
                "path_vars.change_root: recursive variable reference",
            ),
            (
                "compact-invalid-unresolved-var",
                "path_vars.change_root: unknown variable 'missing'",
            ),
            (
                "compact-invalid-brace-syntax",
                "path_vars.change_root: unsupported interpolation syntax '${'",
            ),
            (
                "compact-invalid-unsafe-path",
                "path_vars.change_root: unsafe absolute path",
            ),
            (
                "compact-invalid-dated-spec-path",
                "path_vars.spec: expected canonical spec path 'specs/compact-change-validation-metadata.md'",
            ),
            (
                "compact-invalid-dated-test-spec-path",
                "path_vars.test_spec: expected canonical test spec path 'specs/compact-change-validation-metadata.test.md'",
            ),
            (
                "compact-invalid-lifecycle-stage",
                "validation_events[0].lifecycle_stage: expected one of",
            ),
            (
                "compact-invalid-missing-first-exists",
                "path_vars.spec: required artifact does not exist",
            ),
            (
                "compact-invalid-path-opt-out",
                "validation_events[0].not_yet_created: per-path existence opt-out flags are not allowed",
            ),
            (
                "compact-invalid-transcript-missing",
                "validation_events[0].evidence.transcript: referenced transcript file does not exist",
            ),
            (
                "compact-invalid-unknown-path-var",
                "path_vars.mystery: unknown compact path variable",
            ),
            (
                "compact-invalid-unsafe-bundle-command-local-path",
                "validation_bundles.unsafe_local_path.command contains unsafe machine-local path",
            ),
            (
                "compact-invalid-unsafe-bundle-command-credential-url",
                "validation_bundles.unsafe_credentials.command contains credential-bearing URL",
            ),
            (
                "compact-invalid-unsafe-bundle-command-secret",
                "validation_bundles.unsafe_secret.command contains secret-like value",
            ),
            (
                "compact-invalid-summary-conflict",
                "validation_summary.all_passed: expected false when any event is not pass",
            ),
            (
                "compact-invalid-stages-validated-drift",
                "validation_summary.stages_validated: expected pass-event stages",
            ),
            (
                "compact-invalid-duplicate-stage",
                "validation_events[1].stage: duplicate stage 'proposal-review-r1'",
            ),
            (
                "compact-invalid-skipped-without-decision",
                "validation_events[1].owner_decision: required when result is skipped",
            ),
            (
                "compact-invalid-not-run-without-blocker",
                "validation_summary.open_validation_blockers: missing blocker for stage 'spec-review-r1'",
            ),
            (
                "compact-invalid-missing-path-delta",
                "validation_events[0].paths_added.lifecycle: required for first path-expanding bundle event",
            ),
            (
                "compact-invalid-final-count-drift",
                "validation_summary.final_counts.reviews: expected 1",
            ),
            (
                "compact-invalid-review-counts",
                "validation_events[0].counts.reviews: expected review artifact count 1",
            ),
            (
                "compact-invalid-review-count-precondition",
                "review artifact count cross-check blocked",
            ),
            (
                "compact-invalid-extra-summary-blocker",
                "validation_summary.open_validation_blockers: extra blocker not derived from validation_events: fake-blocker",
            ),
            (
                "compact-invalid-evidence-kind-result",
                "validation_events[0].evidence_kind: actual-run-fail requires result fail",
            ),
            (
                "compact-invalid-evidence-kind-unknown",
                "validation_events[0].evidence_kind: expected one of",
            ),
            (
                "compact-invalid-evidence-ref-unsafe",
                "validation_events[0].evidence_ref: unsafe URL or hostname path",
            ),
            (
                "compact-invalid-evidence-ref-missing-anchor",
                "validation_events[0].evidence_ref: unresolved anchor 'missing-anchor'",
            ),
            (
                "compact-invalid-cache-only-closeout",
                "validation_events[0].evidence_kind: cache-hit-inner-loop cannot satisfy closeout",
            ),
            (
                "legacy-invalid-cache-evidence-fields",
                "validation[0].evidence_kind: legacy validation metadata cannot claim cache-hit or closeout evidence",
            ),
        ]
        for fixture, expected in cases:
            with self.subTest(fixture=fixture):
                self.assertPathFails(FIXTURES / fixture / "change.yaml", expected)

    def test_compact_pre_stage_missing_artifact_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "compact-valid-pre-stage-missing-artifact" / "change.yaml")

    def test_compact_m3_valid_fixtures_pass(self) -> None:
        for fixture in (
            "compact-valid-cache-hit-plus-closeout",
            "compact-valid-skipped-with-decision",
            "compact-valid-review-counts",
        ):
            with self.subTest(fixture=fixture):
                self.assertPathPasses(FIXTURES / fixture / "change.yaml")

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
                "summary.eligible_commands: expected cache_hits + cache_misses + cache_disabled",
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

    def test_compact_path_accumulation_helper(self) -> None:
        validator = load_validator_module()
        data = validator.load_yaml(FIXTURES / "compact-valid" / "change.yaml")
        variables, errors = validator.resolve_compact_path_vars(data["path_vars"])
        self.assertEqual(errors, [])
        reconstructed, errors = validator.reconstruct_compact_path_sets(
            data["validation_bundles"],
            data["validation_events"],
            variables,
        )
        self.assertEqual(errors, [])
        self.assertEqual(
            reconstructed[("proposal-review-r1", "lifecycle")],
            [
                "docs/proposals/2026-05-21-compact-change-validation-metadata.md",
                "tests/fixtures/change-metadata/compact-valid/change.yaml",
            ],
        )
        self.assertEqual(
            reconstructed[("test-spec-r1", "lifecycle")],
            [
                "docs/proposals/2026-05-21-compact-change-validation-metadata.md",
                "tests/fixtures/change-metadata/compact-valid/change.yaml",
                "specs/compact-change-validation-metadata.md",
                "specs/compact-change-validation-metadata.test.md",
                "tests/fixtures/change-metadata/compact-valid/change.validation-log.yaml",
            ],
        )

    def test_compact_common_read_reduction_helper(self) -> None:
        validator = load_validator_module()
        legacy_path = FIXTURES / "compactness-representative-legacy" / "change.yaml"
        compact_path = FIXTURES / "compactness-representative-compact" / "change.yaml"
        self.assertPathPasses(legacy_path)
        self.assertPathPasses(compact_path)

        compact_data = validator.load_yaml(compact_path)
        variables, errors = validator.resolve_compact_path_vars(compact_data["path_vars"])
        self.assertEqual(errors, [])
        reconstructed, errors = validator.reconstruct_compact_path_sets(
            compact_data["validation_bundles"],
            compact_data["validation_events"],
            variables,
        )
        self.assertEqual(errors, [])
        self.assertEqual(
            reconstructed[("code-review-m3-r1", "lifecycle")],
            [
                "docs/proposals/2026-05-21-compact-change-validation-metadata.md",
                "specs/compact-change-validation-metadata.md",
                "specs/compact-change-validation-metadata.test.md",
                "docs/plans/2026-05-21-compact-change-validation-metadata.md",
                "docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m1-r1.md",
                "docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r1.md",
                "docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m2-r2.md",
                "docs/changes/2026-05-21-compact-change-validation-metadata/reviews/code-review-m3-r1.md",
            ],
        )
        reduction = validator.measure_compact_common_read_reduction(
            validator.extract_change_validation_common_read_surface(
                validator.load_yaml(legacy_path)
            ),
            validator.extract_change_validation_common_read_surface(compact_data),
        )
        self.assertGreaterEqual(reduction, 0.30)

    def test_compact_validator_does_not_execute_bundle_commands(self) -> None:
        sentinel = ROOT / "tests" / "fixtures" / "change-metadata" / "compact-command-sentinel"
        if sentinel.exists():
            sentinel.unlink()
        with tempfile.TemporaryDirectory(prefix="change-metadata-no-exec-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                """schema_version: 2
path_vars:
  change_id: 2026-05-21-compact-change-validation-metadata
  change_root: tests/fixtures/change-metadata/compact-valid
validation_bundles:
  sentinel:
    command: python -c "from pathlib import Path; Path('tests/fixtures/change-metadata/compact-command-sentinel').write_text('executed')"
validation_events:
  - stage: proposal-review-r1
    lifecycle_stage: proposal-review
    bundles:
      - sentinel
    result: pass
validation_summary:
  all_passed: true
  stages_validated:
    - proposal-review-r1
  final_counts: {}
  open_validation_blockers: []
""",
                encoding="utf-8",
            )
            self.assertPathPasses(target)
        self.assertFalse(sentinel.exists(), "bundle command was executed")
        if sentinel.exists():
            sentinel.unlink()

    def test_clean_receipt_root_metadata_passes(self) -> None:
        self.assertPathPasses(CLEAN_RECEIPT_ROOT)

    def test_shipped_0001_example_passes(self) -> None:
        self.assertPathPasses(SKILL_VALIDATOR_EXAMPLE)

    def test_inline_empty_collections_pass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-inline-empty-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                """change_id: "inline-empty"
title: "Inline empty collections"
classification: "test"
risk: "low"
artifacts: {}
requirements: []
tests: []
validation: []
changed_files: []
review:
  status: "pending"
  unresolved_items: 0
""",
                encoding="utf-8",
            )
            self.assertPathPasses(target)

    def test_noncanonical_artifact_key_fails(self) -> None:
        self.assertPathFails(
            FIXTURES / "bad-artifact-key" / "change.yaml",
            "artifacts.explain-change: invalid artifact key",
        )

    def test_nested_artifact_value_shape_fails(self) -> None:
        self.assertPathFails(
            FIXTURES / "bad-artifact-value-shape" / "change.yaml",
            "artifacts.explain_change: expected string",
        )

    def test_clean_receipt_review_metadata_shape_fails(self) -> None:
        fixture_text = CLEAN_RECEIPT_ROOT.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix="change-metadata-clean-receipt-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                fixture_text.replace("reviewed_artifact: specs/example.md", "reviewed_artifact: 1"),
                encoding="utf-8",
            )
            self.assertPathFails(target, "review.reviewed_artifact: expected string")

        with tempfile.TemporaryDirectory(prefix="change-metadata-clean-receipt-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                fixture_text.replace("review_log: tests/fixtures/review-artifacts/valid-clean-receipt-root/review-log.md", "review_log: 1"),
                encoding="utf-8",
            )
            self.assertPathFails(target, "review.review_log: expected string")

    def test_clean_receipt_review_metadata_required_fields_fail(self) -> None:
        fixture_text = CLEAN_RECEIPT_ROOT.read_text(encoding="utf-8")
        cases = [
            (
                "  reviewed_artifact: specs/example.md\n",
                "",
                "review.reviewed_artifact is required for clean receipt roots",
            ),
            (
                "  review_log: tests/fixtures/review-artifacts/valid-clean-receipt-root/review-log.md\n",
                "",
                "review.review_log is required for clean receipt roots",
            ),
            (
                "  status: clean\n",
                "",
                "review.status: missing required field",
            ),
            (
                "  status: clean\n",
                "  status: approved\n",
                "review.status must be 'clean' for clean receipt roots",
            ),
            (
                "  status: clean\n",
                "  status: changes-requested\n",
                "review.status must be 'clean' for clean receipt roots",
            ),
            (
                "  unresolved_items: 0\n",
                "",
                "review.unresolved_items: missing required field",
            ),
            (
                "  unresolved_items: 0\n",
                "  unresolved_items: 1\n",
                "review.unresolved_items must be 0 for clean receipt roots",
            ),
            (
                "  unresolved_items: 0\n",
                "  unresolved_items: \"0\"\n",
                "review.unresolved_items: expected integer",
            ),
        ]
        for old, new, expected in cases:
            with self.subTest(expected=expected):
                with tempfile.TemporaryDirectory(prefix="change-metadata-clean-receipt-") as temp_dir:
                    target = Path(temp_dir) / "change.yaml"
                    target.write_text(fixture_text.replace(old, new), encoding="utf-8")
                    self.assertPathFails(target, expected)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
