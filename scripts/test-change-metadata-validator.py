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

from change_metadata_semantics import (
    validate_artifact_transition,
    validate_stage_owned_lifecycle_metadata,
)
from artifact_lifecycle_contracts import (
    classify_lifecycle_contract,
    validate_final_verification_activation_manifest,
    validate_lifecycle_activation_manifest,
    validate_lifecycle_activation_prerequisites,
)
from final_verification_protocol import (
    evaluate_pr_handoff,
    evaluate_evidence_decision,
    parse_verify_report,
    render_verify_report,
    replay_disposition,
    tail_disposition,
    validate_final_verification_result,
)


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
    maxDiff = None

    def write_policy_fixture(
        self,
        root: Path,
        *,
        change_id: str = "2026-06-24-policy-fixture",
        workflow_block: str = """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
""",
    ) -> Path:
        target = root / "change.yaml"
        target.write_text(
            f"""change_id: {change_id}
title: Policy fixture
classification: spec
risk: low
artifacts: {{}}
requirements:
  - fixture
tests:
  - fixture
validation:
  - command: fixture
    result: pass
changed_files:
  - docs/example.md
review:
  status: pending
  unresolved_items: 0
{workflow_block}""",
            encoding="utf-8",
        )
        return target

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

    def valid_implementation_named_record_workflow(self, *, extra_container: str = "") -> str:
        extra = f"{extra_container}\n" if extra_container else ""
        return f"""workflow:
  autoprogression:
{extra}    implementation_through_verify:
      profile: implementation-through-verify
      state: armed
      phase: B
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
"""

    def valid_review_fix_named_record_workflow(self, *, extra_review_fix: str = "") -> str:
        extra = f"{extra_review_fix}\n" if extra_review_fix else ""
        return f"""workflow:
  autoprogression:
    review_fix:
      profile: bounded-review-fix
      status: armed
      target_stage: spec-review
      armed_by: user
      armed_at: 2026-06-24T12:05:00Z
      current_stage: spec
      current_review: spec-review-r1
      stop_reason: none
      last_updated_evidence: docs/changes/2026-06-24-policy-fixture/change.yaml
      change_id: 2026-06-24-policy-fixture
{extra}"""

    def valid_workflow_automation(self, *, extra_automation: str = "") -> str:
        extra = f"{extra_automation}\n" if extra_automation else ""
        return f"""workflow:
  automation:
    mechanism: bounded-review-fix
    schema_version: 1
    run:
      run_id: run-001
      change_id: 2026-06-24-policy-fixture
      status: active
      policy_version: 1
      target:
        stage: proposal-review
        occurrence:
          kind: singleton
        bound_at: 2026-06-24T12:00:00Z
        completion:
          rule: formal review occurrence is recorded
    parent_authorizations: {{}}
    effective_capabilities: {{}}
    transition_receipts: {{}}
    external_actions: prohibited
{extra}"""

    def test_workflow_automation_valid_minimum_passes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-workflow-automation-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_workflow_automation(),
            )
            self.assertPathPasses(target)

    def test_workflow_automation_unknown_mechanism_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-workflow-automation-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_workflow_automation().replace(
                    "mechanism: bounded-review-fix", "mechanism: legacy-profile"
                ),
            )
            self.assertPathFails(
                target,
                "workflow.automation.mechanism: unknown value 'legacy-profile'; expected one of: bounded-review-fix",
            )

    def test_workflow_automation_rejects_live_state_ownership(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-workflow-automation-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_workflow_automation(extra_automation="    next_stage: spec"),
            )
            self.assertPathFails(
                target,
                "workflow.automation.next_stage: automation state must not own live workflow state",
            )

    def test_workflow_automation_rejects_mixed_legacy_state(self) -> None:
        block = self.valid_workflow_automation() + """  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
"""
        with tempfile.TemporaryDirectory(prefix="change-metadata-workflow-automation-") as temp_dir:
            target = self.write_policy_fixture(Path(temp_dir), workflow_block=block)
            self.assertPathFails(
                target,
                "workflow: mixed writable workflow.automation and legacy workflow.autoprogression state",
            )

    def test_workflow_automation_accepts_read_only_legacy_after_migration(self) -> None:
        legacy_record = {
            "profile": "authoring-through-plan-review",
            "authorized_by": "user",
            "authorized_at": "2026-06-24T12:00:00Z",
            "change_id": "2026-06-24-policy-fixture",
        }
        source_identity = "sha256:" + hashlib.sha256(
            json.dumps(
                legacy_record, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ).encode("utf-8")
        ).hexdigest()
        migration = f"""    migration_receipts:
      migration-001:
        migration_id: migration-001
        source_mechanism: authoring-through-plan-review
        source_record_identity: {source_identity}
        migrated_at: 2026-07-22T00:00:00Z
        unified_run_id: run-001
        projection_result: equivalent
        legacy_read_only: true"""
        block = self.valid_workflow_automation(extra_automation=migration) + """  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
"""
        with tempfile.TemporaryDirectory(prefix="change-metadata-workflow-automation-") as temp_dir:
            target = self.write_policy_fixture(Path(temp_dir), workflow_block=block)
            self.assertPathPasses(target)

        with tempfile.TemporaryDirectory(prefix="change-metadata-workflow-automation-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=block.replace(source_identity, "sha256:" + "0" * 64),
            )
            self.assertPathFails(
                target,
                "legacy source mechanism and identity must match exactly",
            )

    def test_valid_basic_fixture_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "valid-basic" / "change.yaml")

    def test_compact_valid_fixture_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "compact-valid" / "change.yaml")

    def test_autoprogression_policy_record_passes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-valid-") as temp_dir:
            target = self.write_policy_fixture(Path(temp_dir))
            self.assertPathPasses(target)

        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-off-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block="""workflow:
  autoprogression:
    profile: off
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
""",
            )
            self.assertPathPasses(target)

    def test_review_fix_autoprogression_policy_record_passes(self) -> None:
        self.assertPathPasses(FIXTURES / "review-fix-valid" / "change.yaml")

        with tempfile.TemporaryDirectory(prefix="change-metadata-review-fix-targets-") as temp_dir:
            for target_stage in (
                "proposal-review",
                "spec",
                "spec-review",
                "architecture",
                "architecture-review",
                "plan",
                "plan-review",
                "test-spec",
                "test-spec-review",
            ):
                with self.subTest(target_stage=target_stage):
                    target = self.write_policy_fixture(
                        Path(temp_dir),
                        workflow_block=self.valid_review_fix_named_record_workflow().replace(
                            "target_stage: spec-review",
                            f"target_stage: {target_stage}",
                        ),
                    )
                    self.assertPathPasses(target)

        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-implementation-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block="""workflow:
  autoprogression:
    authoring_through_plan_review:
      profile: authoring-through-plan-review
      authorized_by: user
      authorized_at: 2026-06-24T12:00:00Z
      change_id: 2026-06-24-policy-fixture
    implementation_through_verify:
      profile: implementation-through-verify
      state: armed
      phase: B
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
      activation_baseline: abc123
      cancellation:
        cancelled_by: user
        cancelled_at: 2026-06-24T12:10:00Z
        reason: user-request
""",
            )
            self.assertPathPasses(target)

    def test_review_gate_metadata_passes_with_packet_hash_and_phase_receipts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-review-gate-valid-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block="""  review_gate:
    manifest: docs/changes/example/reviews/code-review-r1.md
    independence_level: L1
    initial_packet_sha256: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    phase_receipts:
      - risk-map-recorded
      - evidence-menu-released
      - evidence-results-released
      - prior-findings-released
      - verdict-recorded
""",
            )
            self.assertPathPasses(target)

    def test_review_gate_metadata_rejects_l0_missing_hash_and_bad_phase_order(self) -> None:
        cases = [
            (
                "l0",
                """  review_gate:
    manifest: docs/changes/example/reviews/code-review-r1.md
    independence_level: L0
    initial_packet_sha256: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    phase_receipts:
      - risk-map-recorded
      - evidence-menu-released
      - evidence-results-released
      - prior-findings-released
      - verdict-recorded
""",
                "review.review_gate.independence_level: L0 is not valid for automated handoff",
            ),
            (
                "missing-hash",
                """  review_gate:
    manifest: docs/changes/example/reviews/code-review-r1.md
    independence_level: L1
    phase_receipts:
      - risk-map-recorded
      - evidence-menu-released
      - evidence-results-released
      - prior-findings-released
      - verdict-recorded
""",
                "review.review_gate.initial_packet_sha256: missing required field",
            ),
            (
                "bad-order",
                """  review_gate:
    manifest: docs/changes/example/reviews/code-review-r1.md
    independence_level: L1
    initial_packet_sha256: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    phase_receipts:
      - evidence-menu-released
      - risk-map-recorded
      - evidence-results-released
      - prior-findings-released
      - verdict-recorded
""",
                "review.review_gate.phase_receipts: evidence-menu-released appears before risk-map-recorded",
            ),
        ]
        for name, review_gate_block, expected in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-review-gate-{name}-") as temp_dir:
                    target = self.write_policy_fixture(Path(temp_dir), workflow_block=review_gate_block)
                    self.assertPathFails(target, expected)

    def test_requirement_fidelity_metadata_passes_with_closed_values(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-rfg-valid-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block="""  requirement_fidelity:
    applicability: applicable
    matched_path_triggers:
      - skills/
      - scripts/*validator*
    matched_category_triggers:
      - skill instructions derived from specs
    review_stage: code-review
    receipt_valid: true
""",
            )
            self.assertPathPasses(target)

    def test_requirement_fidelity_metadata_rejects_unknown_values(self) -> None:
        cases = [
            (
                "unknown-applicability",
                """  requirement_fidelity:
    applicability: maybe
    matched_path_triggers:
      - skills/
    matched_category_triggers:
      - skill instructions derived from specs
    review_stage: code-review
    receipt_valid: true
""",
                "review.requirement_fidelity.applicability: expected one of applicable, not-applicable",
            ),
            (
                "unknown-path-trigger",
                """  requirement_fidelity:
    applicability: applicable
    matched_path_triggers:
      - random/
    matched_category_triggers:
      - skill instructions derived from specs
    review_stage: code-review
    receipt_valid: true
""",
                "review.requirement_fidelity.matched_path_triggers[0]: unknown path trigger random/",
            ),
            (
                "unknown-not-applicable-reason",
                """  requirement_fidelity:
    applicability: not-applicable
    matched_path_triggers:
      - none
    matched_category_triggers:
      - none
    review_stage: code-review
    not_applicable_reason: just docs
""",
                "review.requirement_fidelity.not_applicable_reason: expected closed reason",
            ),
        ]
        for name, block, expected in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-rfg-{name}-") as temp_dir:
                    target = self.write_policy_fixture(Path(temp_dir), workflow_block=block)
                    self.assertPathFails(target, expected)

    def test_autoprogression_policy_record_required_fields_fail(self) -> None:
        cases = [
            (
                "unknown-profile",
                """workflow:
  autoprogression:
    profile: auto
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.profile: expected one of",
            ),
            (
                "missing-profile",
                """workflow:
  autoprogression:
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.profile: missing required field",
            ),
            (
                "missing-authorized-by",
                """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.authorized_by: missing required field",
            ),
            (
                "missing-authorized-at",
                """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.authorized_at: missing required field",
            ),
            (
                "missing-change-id",
                """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
""",
                "workflow.autoprogression.change_id: missing required field",
            ),
            (
                "mismatched-change-id",
                """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-other-change
""",
                "workflow.autoprogression.change_id: must match top-level change_id",
            ),
            (
                "invalid-timestamp",
                """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: June 24 2026
    change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.authorized_at: expected RFC3339 UTC timestamp",
            ),
            (
                "malformed-workflow",
                "workflow: true\n",
                "workflow: expected object",
            ),
            (
                "malformed-autoprogression",
                """workflow:
  autoprogression: true
""",
                "workflow.autoprogression: expected object",
            ),
        ]
        for name, workflow_block, expected in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-policy-{name}-") as temp_dir:
                    target = self.write_policy_fixture(Path(temp_dir), workflow_block=workflow_block)
                    self.assertPathFails(target, expected)

    def test_autoprogression_policy_non_durable_records_fail(self) -> None:
        cases = [
            (
                "pre-pack-session-intent",
                """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
    session_intent: true
""",
                "workflow.autoprogression.session_intent: session-only arming is not durable authorization",
            ),
            (
                "failed-persistence",
                """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
    persistence_status: failed
""",
                "workflow.autoprogression.persistence_status: authorization-not-persisted",
            ),
            (
                "fallback-without-contract-rejection",
                """workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
    fallback_policy_path: docs/changes/2026-06-24-policy-fixture/workflow-policy.yaml
""",
                "workflow.autoprogression.fallback_policy_path: fallback is only valid when change metadata rejects policy data",
            ),
        ]
        for name, workflow_block, expected in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-policy-{name}-") as temp_dir:
                    target = self.write_policy_fixture(Path(temp_dir), workflow_block=workflow_block)
                    self.assertPathFails(target, expected)

    def test_implementation_autoprogression_policy_record_required_fields_fail(self) -> None:
        cases = [
            (
                "missing-phase",
                """workflow:
  autoprogression:
    implementation_through_verify:
      profile: implementation-through-verify
      state: armed
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.implementation_through_verify.phase: missing required field",
            ),
            (
                "unsupported-phase",
                """workflow:
  autoprogression:
    implementation_through_verify:
      profile: implementation-through-verify
      state: armed
      phase: D
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.implementation_through_verify.phase: expected one of: A, B, C",
            ),
            (
                "unsupported-state",
                """workflow:
  autoprogression:
    implementation_through_verify:
      profile: implementation-through-verify
      state: running
      phase: B
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.implementation_through_verify.state: expected one of",
            ),
            (
                "wrong-record-profile",
                """workflow:
  autoprogression:
    implementation_through_verify:
      profile: authoring-through-plan-review
      state: armed
      phase: B
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
""",
                "workflow.autoprogression.implementation_through_verify.profile: expected implementation-through-verify",
            ),
            (
                "live-state-field",
                """workflow:
  autoprogression:
    implementation_through_verify:
      profile: implementation-through-verify
      state: armed
      phase: B
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
      next_stage: implement M1
""",
                "workflow.autoprogression.implementation_through_verify.next_stage: profile policy must not own live workflow state",
            ),
        ]
        for name, workflow_block, expected in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-implementation-policy-{name}-") as temp_dir:
                    target = self.write_policy_fixture(Path(temp_dir), workflow_block=workflow_block)
                    self.assertPathFails(target, expected)

    def test_review_fix_autoprogression_unknown_values_fail_closed(self) -> None:
        cases = [
            (
                "wrong-profile",
                self.valid_review_fix_named_record_workflow().replace(
                    "profile: bounded-review-fix",
                    "profile: implementation-through-verify",
                ),
                "workflow.autoprogression.review_fix.profile: expected bounded-review-fix",
            ),
            (
                "unsupported-status",
                self.valid_review_fix_named_record_workflow().replace(
                    "status: armed",
                    "status: running",
                ),
                "workflow.autoprogression.review_fix.status: expected one of",
            ),
            (
                "unsupported-target",
                self.valid_review_fix_named_record_workflow().replace(
                    "target_stage: spec-review",
                    "target_stage: verify",
                ),
                "workflow.autoprogression.review_fix.target_stage: expected one of",
            ),
            (
                "unsupported-stop-reason",
                self.valid_review_fix_named_record_workflow().replace(
                    "stop_reason: none",
                    "stop_reason: unexpected",
                ),
                "workflow.autoprogression.review_fix.stop_reason: expected one of",
            ),
        ]
        for name, workflow_block, expected in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-review-fix-{name}-") as temp_dir:
                    target = self.write_policy_fixture(Path(temp_dir), workflow_block=workflow_block)
                    self.assertPathFails(target, expected)

    def test_review_fix_autoprogression_required_fields_fail(self) -> None:
        cases = [
            ("profile", "workflow.autoprogression.review_fix.profile: missing required field"),
            ("status", "workflow.autoprogression.review_fix.status: missing required field"),
            ("target_stage", "workflow.autoprogression.review_fix.target_stage: missing required field"),
            ("armed_by", "workflow.autoprogression.review_fix.armed_by: missing required field"),
            ("armed_at", "workflow.autoprogression.review_fix.armed_at: missing required field"),
            ("current_stage", "workflow.autoprogression.review_fix.current_stage: missing required field"),
            ("current_review", "workflow.autoprogression.review_fix.current_review: missing required field"),
            ("stop_reason", "workflow.autoprogression.review_fix.stop_reason: missing required field"),
            (
                "last_updated_evidence",
                "workflow.autoprogression.review_fix.last_updated_evidence: missing required field",
            ),
            ("change_id", "workflow.autoprogression.review_fix.change_id: missing required field"),
        ]
        for missing_field, expected in cases:
            with self.subTest(missing_field=missing_field):
                workflow_block = "\n".join(
                    line
                    for line in self.valid_review_fix_named_record_workflow().splitlines()
                    if not line.strip().startswith(f"{missing_field}:")
                ) + "\n"
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-review-fix-missing-{missing_field}-") as temp_dir:
                    target = self.write_policy_fixture(Path(temp_dir), workflow_block=workflow_block)
                    self.assertPathFails(target, expected)

    def test_review_fix_autoprogression_terminal_transitions_pass(self) -> None:
        cases = [
            ("off", "user-off"),
            ("completed", "target-reached"),
            ("cancelled", "cancelled"),
            ("paused", "needs-decision"),
        ]
        for status, stop_reason in cases:
            with self.subTest(status=status, stop_reason=stop_reason):
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-review-fix-{status}-") as temp_dir:
                    target = self.write_policy_fixture(
                        Path(temp_dir),
                        workflow_block=self.valid_review_fix_named_record_workflow()
                        .replace("status: armed", f"status: {status}")
                        .replace("stop_reason: none", f"stop_reason: {stop_reason}"),
                    )
                    self.assertPathPasses(target)

    def test_direct_review_only_metadata_does_not_create_review_fix_authorization(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-review-fix-direct-review-") as temp_dir:
            repo_root = Path(temp_dir)
            change_id = "2026-06-24-policy-fixture"
            change_root = repo_root / "docs" / "changes" / change_id
            change_root.mkdir(parents=True)
            target = self.write_policy_fixture(
                change_root,
                workflow_block="""review:
  status: clean
  reviewed_artifact: docs/example.md
  review_log: docs/changes/2026-06-24-policy-fixture/review-log.md
  unresolved_items: 0
""",
            )
            self.assertPathPasses(target)
            result = run_query_change_record(repo_root, change_id, "summary")
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(result.stdout)
            self.assertIsNone(payload["profile_policy"])

    def test_named_records_reject_container_next_stage(self) -> None:
        self.assertPathFails(
            FIXTURES / "2026-06-24-separately-armed-implementation-autoprogression-through-verify" / "change.yaml",
            "workflow.autoprogression.next_stage: profile policy must not own live workflow state",
        )

    def test_forbidden_live_state_container_fixture_fails(self) -> None:
        self.assertPathFails(
            FIXTURES / "2026-06-24-separately-armed-implementation-autoprogression-through-verify" / "change.yaml",
            "workflow.autoprogression.next_stage: profile policy must not own live workflow state",
        )

    def test_named_records_reject_container_current_stage(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-current-stage-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_implementation_named_record_workflow(
                    extra_container="    current_stage: implement"
                ),
            )
            self.assertPathFails(
                target,
                "workflow.autoprogression.current_stage: profile policy must not own live workflow state",
            )

    def test_named_records_reject_container_review_status(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-review-status-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_implementation_named_record_workflow(
                    extra_container="    review_status: approved"
                ),
            )
            self.assertPathFails(
                target,
                "workflow.autoprogression.review_status: profile policy must not own live workflow state",
            )

    def test_named_records_reject_container_branch_readiness(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-branch-readiness-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_implementation_named_record_workflow(
                    extra_container="    branch_readiness: ready"
                ),
            )
            self.assertPathFails(
                target,
                "workflow.autoprogression.branch_readiness: profile policy must not own live workflow state",
            )

    def test_named_records_reject_container_pr_readiness(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-pr-readiness-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_implementation_named_record_workflow(
                    extra_container="    pr_readiness: ready"
                ),
            )
            self.assertPathFails(
                target,
                "workflow.autoprogression.pr_readiness: profile policy must not own live workflow state",
            )

    def test_named_records_reject_all_forbidden_fields_at_once(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-all-live-fields-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_implementation_named_record_workflow(
                    extra_container="""    current_stage: implement
    next_stage: code-review
    review_status: approved
    branch_readiness: ready
    pr_readiness: ready"""
                ),
            )
            result = run_validator(target)
            combined_output = f"{result.stdout}\n{result.stderr}"
            self.assertNotEqual(result.returncode, 0)
            for field in (
                "current_stage",
                "next_stage",
                "review_status",
                "branch_readiness",
                "pr_readiness",
            ):
                self.assertIn(
                    f"workflow.autoprogression.{field}: profile policy must not own live workflow state",
                    combined_output,
                )

    def test_legacy_record_still_rejects_container_forbidden_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-legacy-live-field-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block="""workflow:
  autoprogression:
    profile: authoring-through-plan-review
    authorized_by: user
    authorized_at: 2026-06-24T12:00:00Z
    change_id: 2026-06-24-policy-fixture
    next_stage: implement M1
""",
            )
            self.assertPathFails(
                target,
                "workflow.autoprogression.next_stage: profile policy must not own live workflow state",
            )

    def test_forbidden_field_inside_authoring_record_still_rejects(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-authoring-live-field-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block="""workflow:
  autoprogression:
    authoring_through_plan_review:
      profile: authoring-through-plan-review
      authorized_by: user
      authorized_at: 2026-06-24T12:00:00Z
      change_id: 2026-06-24-policy-fixture
      next_stage: implement M1
""",
            )
            self.assertPathFails(
                target,
                "workflow.autoprogression.authoring_through_plan_review.next_stage: profile policy must not own live workflow state",
            )

    def test_forbidden_field_inside_implementation_record_still_rejects(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-implementation-live-field-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block=self.valid_implementation_named_record_workflow(
                    extra_container=""
                ).replace(
                    "      change_id: 2026-06-24-policy-fixture\n",
                    "      change_id: 2026-06-24-policy-fixture\n      next_stage: implement M1\n",
                ),
            )
            self.assertPathFails(
                target,
                "workflow.autoprogression.implementation_through_verify.next_stage: profile policy must not own live workflow state",
            )

    def test_unrelated_workflow_top_level_field_is_not_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-unrelated-workflow-") as temp_dir:
            target = self.write_policy_fixture(
                Path(temp_dir),
                workflow_block="""workflow:
  some_unrelated_field: allowed
  autoprogression:
    implementation_through_verify:
      profile: implementation-through-verify
      state: armed
      phase: B
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
""",
            )
            self.assertPathPasses(target)

    def test_query_summary_exposes_autoprogression_policy_as_evidence_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-query-") as temp_dir:
            repo_root = Path(temp_dir)
            change_id = "2026-06-24-policy-fixture"
            change_root = repo_root / "docs" / "changes" / change_id
            change_root.mkdir(parents=True)
            self.write_policy_fixture(change_root)

            result = run_query_change_record(repo_root, change_id, "summary")
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["profile_policy"]["profile"], "authoring-through-plan-review")
            self.assertEqual(payload["profile_policy"]["policy_owner"], "change-metadata")
            self.assertEqual(
                payload["profile_policy"]["detail_pointer"],
                f"docs/changes/{change_id}/change.yaml#workflow.autoprogression",
            )
            self.assertNotIn("next_stage", payload["profile_policy"])
            self.assertNotIn("current_stage", payload["profile_policy"])

    def test_query_summary_exposes_named_autoprogression_policy_records(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-policy-query-named-") as temp_dir:
            repo_root = Path(temp_dir)
            change_id = "2026-06-24-policy-fixture"
            change_root = repo_root / "docs" / "changes" / change_id
            change_root.mkdir(parents=True)
            self.write_policy_fixture(
                change_root,
                workflow_block="""workflow:
  autoprogression:
    authoring_through_plan_review:
      profile: authoring-through-plan-review
      authorized_by: user
      authorized_at: 2026-06-24T12:00:00Z
      change_id: 2026-06-24-policy-fixture
    implementation_through_verify:
      profile: implementation-through-verify
      state: armed
      phase: B
      authorized_by: user
      authorized_at: 2026-06-24T12:05:00Z
      change_id: 2026-06-24-policy-fixture
    review_fix:
      profile: bounded-review-fix
      status: armed
      target_stage: spec-review
      armed_by: user
      armed_at: 2026-06-24T12:06:00Z
      current_stage: spec
      current_review: spec-review-r1
      stop_reason: none
      last_updated_evidence: docs/changes/2026-06-24-policy-fixture/change.yaml
      change_id: 2026-06-24-policy-fixture
""",
            )

            result = run_query_change_record(repo_root, change_id, "summary")
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            payload = json.loads(result.stdout)
            records = payload["profile_policy"]["records"]
            self.assertEqual(
                records["authoring_through_plan_review"]["profile"],
                "authoring-through-plan-review",
            )
            self.assertEqual(
                records["implementation_through_verify"]["profile"],
                "implementation-through-verify",
            )
            self.assertEqual(records["implementation_through_verify"]["phase"], "B")
            self.assertEqual(records["implementation_through_verify"]["state"], "armed")
            self.assertNotIn("next_stage", records["implementation_through_verify"])
            self.assertNotIn("current_stage", records["implementation_through_verify"])
            self.assertEqual(records["review_fix"]["profile"], "bounded-review-fix")
            self.assertEqual(records["review_fix"]["status"], "armed")
            self.assertEqual(records["review_fix"]["target_stage"], "spec-review")
            self.assertNotIn("next_stage", records["review_fix"])

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
                "compact-invalid-helper-closeout-command",
                "validation_events[0].bundles[0]: explicit-paths-inner-loop cannot satisfy closeout",
            ),
            (
                "compact-invalid-helper-closeout-command-equals-mode",
                "validation_events[0].bundles[0]: explicit-paths-inner-loop cannot satisfy closeout",
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

    def test_valid_basic_fixture_passes(self) -> None:
        self.assertPathPasses(VALID_BASIC_FIXTURE)

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

    def test_inline_mapping_item_accepts_nested_sequence_for_first_key(self) -> None:
        validator = load_validator_module()
        with tempfile.TemporaryDirectory(prefix="change-metadata-inline-nested-sequence-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                """review_packages:
  delivery:
    findings:
      - affected_artifact_ids:
          - plan
        finding_id: SPC-DR1
""",
                encoding="utf-8",
            )
            self.assertEqual(
                validator.load_yaml(target),
                {
                    "review_packages": {
                        "delivery": {
                            "findings": [
                                {
                                    "affected_artifact_ids": ["plan"],
                                    "finding_id": "SPC-DR1",
                                }
                            ]
                        }
                    }
                },
            )

    def test_changes_requested_review_pointers_do_not_declare_clean_receipt_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-changes-requested-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            target.write_text(
                """change_id: "changes-requested-review"
title: "Changes requested review"
classification: "test"
risk: "low"
artifacts: {}
requirements: []
tests: []
validation: []
changed_files: []
review:
  latest_review: docs/changes/changes-requested-review/reviews/spec-review-r1.md
  review_log: docs/changes/changes-requested-review/review-log.md
  reviewed_artifact: specs/example.md
  status: "changes-requested"
  unresolved_items: 1
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

    def write_review_summary_change_fixture(
        self,
        root: Path,
        *,
        unresolved_items: int = 1,
        material_findings: int = 1,
        closed_findings: int = 0,
        open_findings: int = 1,
        extra_review_field: str = "",
        close_resolution: bool = False,
        log_open_findings: str = "WSS-F1",
        include_validation_evidence: bool = True,
        disposition: str | None = "accepted",
        include_closeout_status: bool = True,
    ) -> Path:
        change_yaml = root / "change.yaml"
        change_yaml.write_text(
            f"""change_id: 2026-06-23-review-summary-fixture
title: Review summary fixture
classification: implementation
risk: low
artifacts: {{}}
requirements:
  - fixture
tests:
  - fixture
validation:
  - command: fixture
    result: pass
changed_files:
  - docs/example.md
review:
  status: changes-requested
  unresolved_items: {unresolved_items}
  material_findings: {material_findings}
  closed_findings: {closed_findings}
  open_findings: {open_findings}
{extra_review_field}""",
            encoding="utf-8",
        )
        (root / "review-log.md").write_text(
            f"""# Review Log

### Review entry
Review ID: code-review-r1
Stage: code-review
Round: 1
Status: changes-requested
Detailed record: reviews/code-review-r1.md
Resolution: review-resolution.md#code-review-r1
Material findings: WSS-F1
Open findings: {log_open_findings}
""",
            encoding="utf-8",
        )
        if close_resolution:
            validation_evidence = "Validation evidence: Fixture validation passed.\n" if include_validation_evidence else ""
            closeout_status = "Closeout status: closed\n\n" if include_closeout_status else ""
            disposition_line = "" if disposition is None else f"Disposition: {disposition}\n"
            (root / "review-resolution.md").write_text(
                f"""# Review Resolution

{closeout_status}### code-review-r1

Finding ID: WSS-F1
{disposition_line}Owner: implementation author
Owning stage: review-resolution
Chosen action: Resolve the finding.
Rationale: Fixture models a historical open log entry closed by resolution evidence.
Validation target: Metadata summary counts derive zero open findings.
{validation_evidence}""",
                encoding="utf-8",
            )
        return change_yaml

    def test_review_summary_counts_match_review_log(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-review-summary-") as temp_dir:
            target = self.write_review_summary_change_fixture(Path(temp_dir))
            self.assertPathPasses(target)

        cases = [
            {"unresolved_items": 0, "expected": "review.unresolved_items must match review-log open finding count"},
            {"material_findings": 2, "expected": "review.material_findings must match review evidence"},
            {"closed_findings": 1, "expected": "review.closed_findings must match review evidence"},
            {"open_findings": 0, "expected": "review.open_findings must match review evidence"},
        ]
        for kwargs in cases:
            expected = kwargs.pop("expected")
            with self.subTest(expected=expected):
                with tempfile.TemporaryDirectory(prefix="change-metadata-review-summary-") as temp_dir:
                    target = self.write_review_summary_change_fixture(Path(temp_dir), **kwargs)
                    self.assertPathFails(target, expected)

        with tempfile.TemporaryDirectory(prefix="change-metadata-review-summary-closed-") as temp_dir:
            target = self.write_review_summary_change_fixture(
                Path(temp_dir),
                unresolved_items=0,
                material_findings=1,
                closed_findings=1,
                open_findings=0,
                close_resolution=True,
                log_open_findings="None",
            )
            self.assertPathPasses(target)

        with tempfile.TemporaryDirectory(prefix="change-metadata-review-summary-missing-evidence-") as temp_dir:
            target = self.write_review_summary_change_fixture(
                Path(temp_dir),
                unresolved_items=0,
                material_findings=1,
                closed_findings=1,
                open_findings=0,
                close_resolution=True,
                include_validation_evidence=False,
            )
            self.assertPathFails(target, "review.unresolved_items must match review-log open finding count")

        invalid_resolution_cases = [
            {"name": "missing-disposition", "disposition": None},
            {"name": "unsupported-disposition", "disposition": "deferred-to-next-quarter"},
            {"name": "missing-closeout-status", "include_closeout_status": False},
        ]
        for case in invalid_resolution_cases:
            name = case.pop("name")
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory(prefix=f"change-metadata-review-summary-{name}-") as temp_dir:
                    target = self.write_review_summary_change_fixture(
                        Path(temp_dir),
                        unresolved_items=0,
                        material_findings=1,
                        closed_findings=1,
                        open_findings=0,
                        close_resolution=True,
                        log_open_findings="None",
                        **case,
                    )
                    self.assertPathFails(target, "review.unresolved_items must match review-log open finding count")

    def test_review_summary_rejects_next_stage_like_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="change-metadata-review-next-stage-") as temp_dir:
            target = self.write_review_summary_change_fixture(
                Path(temp_dir),
                extra_review_field="  next_stage: code-review M2\n",
            )
            self.assertPathFails(target, "review.next_stage must not author live planned-initiative next stage")


class StageOwnedLifecycleMetadataTests(unittest.TestCase):
    def valid_record(self) -> dict:
        return {
            "lifecycle_contract": "stage-owned-change-local-v1",
            "artifact_states": {
                "proposal": {
                    "kind": "proposal",
                    "path": "docs/proposals/example.md",
                    "role": "primary",
                    "lifecycle_state": "accepted",
                    "review": {
                        "id": "proposal-review-r1",
                        "artifact_id": "proposal",
                        "outcome": "approved",
                        "record": "docs/changes/example/reviews/proposal-review-r1.md",
                        "round": "r1",
                    },
                }
            },
            "workflow_state": {
                "lifecycle_state": "active",
                "current_stage": "spec",
                "next_stage": "spec-review",
                "blocker": None,
                "evidence": ["docs/changes/example/reviews/proposal-review-r1.md"],
            },
            "workflow": {
                "automation": {
                    "mechanism": "bounded-review-fix",
                    "target": {
                        "stage": "verify",
                        "occurrence": {"kind": "final"},
                        "bound_at": "2026-07-29T00:00:00Z",
                        "completion": {"rule": "fresh verification passes"},
                    },
                    "status": "active",
                    "current_stage": "spec",
                    "stop_reason": None,
                    "evidence": [],
                }
            },
        }

    def test_stage_owned_valid_record_passes(self) -> None:
        self.assertEqual(validate_stage_owned_lifecycle_metadata(self.valid_record()), [])

    def test_v2_plan_centered_delivery_package_passes_without_test_spec(self) -> None:
        record = self.valid_record()
        record["lifecycle_contract"] = "stage-owned-change-local-v2"
        record["artifact_states"]["plan"] = {
            "kind": "plan",
            "path": "docs/plans/example.md",
            "role": "primary",
            "lifecycle_state": "review-required",
            "authoring_evidence": "docs/changes/example/evidence/plan-authoring.md",
        }
        record["review_packages"] = {
            "delivery": {
                "authority": "granted",
                "correction_targets": [],
                "findings": [],
                "members": {"plan": "docs/plans/example.md"},
                "outcome": "approved",
                "package_kind": "delivery",
                "review_id": "delivery-review-r1",
                "review_round": "r1",
                "status": "approved",
                "upstream_review_id": "design-review-r1",
            }
        }
        self.assertEqual(validate_stage_owned_lifecycle_metadata(record), [])

    def test_v2_retired_test_spec_values_fail_closed(self) -> None:
        record = self.valid_record()
        record["lifecycle_contract"] = "stage-owned-change-local-v2"
        record["artifact_states"]["test-spec"] = {
            "kind": "test-spec",
            "path": "specs/example.test.md",
            "role": "primary",
            "lifecycle_state": "review-required",
            "authoring_evidence": "docs/changes/example/evidence/test-spec-authoring.md",
        }
        record["workflow_state"]["current_stage"] = "test-spec-review"
        record["lifecycle_cli"] = {
            "reviews": {"test-spec": {"stage_authority": "test-spec-review"}}
        }
        errors = validate_stage_owned_lifecycle_metadata(record)
        self.assertTrue(any("artifact_states.test-spec.kind: unknown_value" in error for error in errors), errors)
        self.assertTrue(any("workflow_state.current_stage: unknown_value" in error for error in errors), errors)
        self.assertTrue(any("stage_authority: unknown_value test-spec-review" in error for error in errors), errors)

    def test_new_primary_plan_allows_review_required_without_planned_work(self) -> None:
        record = self.valid_record()
        record["artifact_states"]["plan"] = {
            "kind": "plan",
            "path": "docs/plans/example.md",
            "role": "primary",
            "lifecycle_state": "review-required",
            "authoring_evidence": "docs/changes/example/evidence/plan-authoring.md",
        }
        self.assertEqual(validate_stage_owned_lifecycle_metadata(record), [])

    def test_reviewed_plan_initialization_requires_matching_review_basis(self) -> None:
        record = self.valid_record()
        record["artifact_states"]["plan"] = {
            "kind": "plan",
            "path": "docs/plans/example.md",
            "role": "primary",
            "lifecycle_state": "review-required",
            "authoring_evidence": "docs/changes/example/evidence/plan-authoring.md",
            "review": {
                "id": "plan-review-r1",
                "artifact_id": "plan",
                "outcome": "approved",
                "record": "docs/changes/example/reviews/plan-review-r1.md",
                "round": "r1",
            },
        }
        initial_planned_work = {
            "plan_artifact_id": "plan",
            "initialization_basis": {
                "review_id": "plan-review-r1",
                "review_round": "r1",
                "review_record": "docs/changes/example/reviews/plan-review-r1.md",
                "reviewed_artifact_path": "docs/plans/example.md",
                "reviewed_revision": "abc1234",
            },
            "current_milestone": "M1",
            "milestones": {
                "M1": {"kind": "implementation", "state": "planned"},
                "M2": {"kind": "implementation", "state": "planned"},
            },
            "remaining_implementation_milestones": ["M1", "M2"],
            "latest_review": {
                "status": "not-started",
                "stage": "none",
                "round": "none",
                "artifact_id": "none",
                "occurrence": "none",
                "milestone_id": "none",
                "evidence": [],
            },
            "final_closeout": {
                "readiness": "not-ready",
                "reasons": ["lifecycle-gates-open"],
                "evidence": [],
            },
        }

        record["workflow_state"]["planned_work"] = initial_planned_work
        self.assertEqual(validate_stage_owned_lifecycle_metadata(record), [])

        record["workflow_state"]["planned_work"]["initialization_basis"]["review_id"] = "plan-review-r2"
        errors = validate_stage_owned_lifecycle_metadata(record)
        self.assertIn(
            "workflow_state.planned_work.initialization_basis: must match current clean plan review",
            errors,
        )

    def test_delivery_review_initialization_accepts_current_package_basis(self) -> None:
        record = self.valid_record()
        record["artifact_states"]["plan"] = {
            "kind": "plan",
            "path": "docs/plans/example.md",
            "role": "primary",
            "lifecycle_state": "review-required",
            "authoring_evidence": "docs/changes/example/evidence/plan-authoring.md",
        }
        record["artifact_states"]["test-spec"] = {
            "kind": "test-spec",
            "path": "specs/example.test.md",
            "role": "primary",
            "lifecycle_state": "review-required",
            "authoring_evidence": "docs/changes/example/evidence/test-spec-authoring.md",
        }
        record["review_packages"] = {
            "delivery": {
                "authority": "granted",
                "correction_targets": [],
                "findings": [],
                "members": {
                    "plan": "docs/plans/example.md",
                    "test-spec": "specs/example.test.md",
                },
                "outcome": "approved",
                "package_kind": "delivery",
                "review_id": "delivery-review-r1",
                "review_round": "r1",
                "status": "approved",
                "upstream_review_id": "design-review-r1",
            }
        }
        record["lifecycle_cli"] = {
            "package_reviews": {
                "delivery": {
                    "evidence_path": "docs/changes/example/reviews/delivery-review-r1.md",
                    "members": {
                        "plan": "docs/plans/example.md",
                        "test-spec": "specs/example.test.md",
                    },
                    "outcome": "approved",
                    "review_id": "delivery-review-r1",
                    "round": "r1",
                    "stage_authority": "delivery-review",
                }
            }
        }
        record["workflow_state"]["planned_work"] = {
            "plan_artifact_id": "plan",
            "initialization_basis": {
                "review_id": "delivery-review-r1",
                "review_round": "r1",
                "review_record": "docs/changes/example/reviews/delivery-review-r1.md",
                "reviewed_artifact_path": "docs/plans/example.md",
            },
            "current_milestone": "M1",
            "milestones": {"M1": {"kind": "implementation", "state": "planned"}},
            "remaining_implementation_milestones": ["M1"],
            "latest_review": {
                "status": "not-started", "stage": "none", "round": "none",
                "artifact_id": "none", "occurrence": "none", "milestone_id": "none", "evidence": [],
            },
            "final_closeout": {
                "readiness": "not-ready", "reasons": ["implementation-milestones-open"], "evidence": [],
            },
        }

        self.assertEqual(validate_stage_owned_lifecycle_metadata(record), [])

        mismatches = (
            (("workflow_state", "planned_work", "initialization_basis", "review_id"), "delivery-review-r2"),
            (("workflow_state", "planned_work", "initialization_basis", "review_round"), "r2"),
            (("workflow_state", "planned_work", "initialization_basis", "review_record"), "docs/changes/example/reviews/wrong-review.md"),
            (("workflow_state", "planned_work", "initialization_basis", "reviewed_artifact_path"), "docs/plans/wrong.md"),
            (("review_packages", "delivery", "authority"), "withheld"),
            (("review_packages", "delivery", "status"), "review-required"),
            (("review_packages", "delivery", "outcome"), "changes-requested"),
            (("review_packages", "delivery", "members", "plan"), "docs/plans/wrong.md"),
        )
        for keys, value in mismatches:
            with self.subTest(keys=keys):
                candidate = copy.deepcopy(record)
                target = candidate
                for key in keys[:-1]:
                    target = target[key]
                target[keys[-1]] = value
                errors = validate_stage_owned_lifecycle_metadata(candidate)
                self.assertTrue(
                    any("initialization_basis" in error for error in errors),
                    errors,
                )

    def test_review_required_plan_rejects_planned_work_without_clean_review(self) -> None:
        record = self.valid_record()
        record["artifact_states"]["plan"] = {
            "kind": "plan",
            "path": "docs/plans/example.md",
            "role": "primary",
            "lifecycle_state": "review-required",
            "authoring_evidence": "docs/changes/example/evidence/plan-authoring.md",
        }
        record["workflow_state"]["planned_work"] = {
            "plan_artifact_id": "plan",
            "current_milestone": "M1",
            "milestones": {"M1": {"kind": "implementation", "state": "planned"}},
            "remaining_implementation_milestones": ["M1"],
            "latest_review": {
                "status": "not-started", "stage": "none", "round": "none",
                "artifact_id": "none", "occurrence": "none", "milestone_id": "none", "evidence": [],
            },
            "final_closeout": {"readiness": "not-ready", "reasons": ["lifecycle-gates-open"], "evidence": []},
        }
        errors = validate_stage_owned_lifecycle_metadata(record)
        self.assertIn(
            "workflow_state.planned_work: review-required plan needs current clean review and initialization basis",
            errors,
        )

    def test_unmarked_historical_record_remains_readable(self) -> None:
        self.assertEqual(validate_stage_owned_lifecycle_metadata({"workflow": {"autoprogression": {}}}), [])

    def test_unknown_value_fails_before_consistency(self) -> None:
        record = self.valid_record()
        record["artifact_states"]["proposal"]["kind"] = "mystery"
        errors = validate_stage_owned_lifecycle_metadata(record)
        self.assertTrue(any("unknown_value" in error for error in errors))

    def test_unknown_automation_status_fails_closed(self) -> None:
        record = self.valid_record()
        record["workflow"]["automation"]["status"] = "waiting"
        errors = validate_stage_owned_lifecycle_metadata(record)
        self.assertTrue(any("automation.status: unknown_value" in error for error in errors))

    def test_review_package_projection_validates_compact_authority(self) -> None:
        record = self.valid_record()
        for artifact_id, kind, path in (
            ("architecture", "architecture", "docs/architecture/example.md"),
            ("spec", "spec", "specs/example.md"),
        ):
            record["artifact_states"][artifact_id] = {
                "kind": kind,
                "path": path,
                "role": "primary",
                "lifecycle_state": "approved",
                "review": {
                    "id": f"{kind}-review-r1",
                    "artifact_id": artifact_id,
                    "outcome": "approved",
                    "record": f"docs/changes/example/reviews/{kind}-review-r1.md",
                    "round": "r1",
                },
            }
        record["review_packages"] = {
            "design": {
                "authority": "granted",
                "correction_targets": [],
                "findings": [],
                "members": {"architecture": "docs/architecture/example.md", "spec": "specs/example.md"},
                "outcome": "approved",
                "package_kind": "design",
                "review_id": "design-review-r1",
                "review_round": "r1",
                "status": "approved",
                "upstream_review_id": "proposal-review-r1",
            }
        }
        self.assertEqual(validate_stage_owned_lifecycle_metadata(record), [])

    def test_review_package_closed_vocabularies_reject_unknown_values(self) -> None:
        record = self.valid_record()
        record["review_packages"] = {
            "combined": {
                "authority": "partial",
                "correction_targets": [],
                "findings": [{
                    "affected_artifact_ids": ["proposal"],
                    "evidence": "evidence",
                    "finding_id": "F-1",
                    "owning_stages": ["proposal"],
                    "required_outcome": "outcome",
                    "safe_resolution_path": "resolution",
                    "scope": "mixed",
                }],
                "members": {"proposal": "docs/proposals/example.md"},
                "outcome": "accepted",
                "package_kind": "combined",
                "review_id": "design-review-r1",
                "review_round": "r1",
                "status": "settled",
                "upstream_review_id": "proposal-review-r1",
            }
        }
        errors = validate_stage_owned_lifecycle_metadata(record)
        self.assertTrue(any("review_packages.combined: unknown_value" in error for error in errors))
        self.assertTrue(any("review_packages.combined.status: unknown_value" in error for error in errors))
        self.assertTrue(any("review_packages.combined.authority: unknown_value" in error for error in errors))
        self.assertTrue(any("review_packages.combined.findings[0].scope: unknown_value" in error for error in errors))

    def test_review_outcome_must_match_settled_state(self) -> None:
        record = self.valid_record()
        record["artifact_states"]["proposal"]["review"]["outcome"] = "changes-requested"
        errors = validate_stage_owned_lifecycle_metadata(record)
        self.assertTrue(any("requires revision-required" in error for error in errors))

    def test_duplicate_paths_and_mixed_legacy_writer_fail(self) -> None:
        record = self.valid_record()
        record["artifact_states"]["spec"] = copy.deepcopy(record["artifact_states"]["proposal"])
        record["artifact_states"]["spec"].update({"kind": "spec", "role": "supporting"})
        record["workflow"]["autoprogression"] = {}
        errors = validate_stage_owned_lifecycle_metadata(record)
        self.assertTrue(any("duplicate artifact path" in error for error in errors))
        self.assertTrue(any("mixed legacy writer" in error for error in errors))

    def test_artifact_transition_rejects_unknown_value(self) -> None:
        errors = validate_artifact_transition("proposal", "accepted", "mystery")
        self.assertTrue(any("unknown_value" in error for error in errors))

    def test_artifact_transition_rejects_illegal_and_non_adr_deprecation(self) -> None:
        self.assertTrue(validate_artifact_transition("spec", "approved", "review-required"))
        self.assertTrue(validate_artifact_transition("proposal", "accepted", "deprecated"))
        self.assertEqual(validate_artifact_transition("adr", "active", "deprecated"), [])


class LifecycleContractClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture_path = ROOT / "packages/rigorloop/test/fixtures/lifecycle/contract-classification-v1.json"
        cls.fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        final_fixture_path = ROOT / "packages/rigorloop/test/fixtures/lifecycle/final-verification-contract-classification-v1.json"
        cls.final_fixture = json.loads(final_fixture_path.read_text(encoding="utf-8"))

    def test_final_verification_preactivation_keeps_v3_inactive_and_v2_active(self) -> None:
        current_manifest = self.fixture["active_manifest"]
        final_manifest = self.final_fixture["preactivation_manifest"]
        self.assertEqual(validate_final_verification_activation_manifest(final_manifest), [])
        self.assertEqual(
            classify_lifecycle_contract("new-v3", {"lifecycle_contract": "stage-owned-change-local-v3"}, current_manifest, final_manifest),
            {"contract_class": "stage-owned-change-local-v3", "activation_state": "preactivation", "authority": "inactive"},
        )
        self.assertEqual(
            classify_lifecycle_contract("new-v2", {"lifecycle_contract": "stage-owned-change-local-v2"}, current_manifest, final_manifest),
            {"contract_class": "stage-owned-change-local-v2", "activation_state": "active", "authority": "active"},
        )

    def test_active_final_verification_manifest_binds_exact_v2_records(self) -> None:
        current_manifest = self.fixture["active_manifest"]
        final_manifest = self.final_fixture["active_manifest"]
        self.assertEqual(validate_final_verification_activation_manifest(final_manifest), [])
        self.assertEqual(
            classify_lifecycle_contract("v2", {"lifecycle_contract": "stage-owned-change-local-v2"}, current_manifest, final_manifest)["authority"],
            "prior-compatible",
        )
        with self.assertRaisesRegex(ValueError, "not present in the final verification activation manifest"):
            classify_lifecycle_contract("unlisted-v2", {"lifecycle_contract": "stage-owned-change-local-v2"}, current_manifest, final_manifest)

    def test_final_verification_unknown_class_and_v3_explain_change_fail_first(self) -> None:
        final_manifest = copy.deepcopy(self.final_fixture["active_manifest"])
        final_manifest["changes"][0]["contract_class"] = "stage-owned-change-local-v1"
        final_manifest["changes"].append(copy.deepcopy(final_manifest["changes"][0]))
        self.assertRegex(
            validate_final_verification_activation_manifest(final_manifest)[0],
            "unknown_value.*stage-owned-change-local-v1",
        )
        for change in (
            {"lifecycle_contract": "stage-owned-change-local-v3", "workflow_state": {"current_stage": "explain-change"}},
            {"lifecycle_contract": "stage-owned-change-local-v3", "artifacts": {"explain_change": "docs/changes/example/explain-change.md"}},
        ):
            with self.assertRaisesRegex(ValueError, "v3 lifecycle contract carries active explain-change state"):
                classify_lifecycle_contract(
                    "new-v3",
                    change,
                    self.fixture["active_manifest"],
                    self.final_fixture["preactivation_manifest"],
                )

    def test_final_verification_manifest_rejects_duplicate_and_unsorted_entries(self) -> None:
        active = self.final_fixture["active_manifest"]
        duplicate = copy.deepcopy(active)
        duplicate["changes"].append(copy.deepcopy(duplicate["changes"][0]))
        self.assertRegex(validate_final_verification_activation_manifest(duplicate)[0], "duplicate")

        unsorted = copy.deepcopy(active)
        unsorted["changes"] = [
            {"change_id": "z-v2", "contract_class": "stage-owned-change-local-v2"},
            {"change_id": "a-v2", "contract_class": "stage-owned-change-local-v2"},
        ]
        self.assertRegex(
            validate_final_verification_activation_manifest(unsorted)[0],
            "raw UTF-8 byte order",
        )

        unknown_before_consistency = copy.deepcopy(duplicate)
        unknown_before_consistency["changes"][0]["contract_class"] = "stage-owned-change-local-v1"
        self.assertRegex(
            validate_final_verification_activation_manifest(unknown_before_consistency)[0],
            "unknown_value.*stage-owned-change-local-v1",
        )

    def test_v3_metadata_semantics_reject_explain_change_authority(self) -> None:
        change = {
            "lifecycle_contract": "stage-owned-change-local-v3",
            "artifact_states": {},
            "review_packages": {},
            "workflow_state": {
                "lifecycle_state": "active",
                "current_stage": "explain-change",
                "next_stage": "verify",
                "blocker": None,
                "evidence": [],
            },
            "lifecycle_cli": {
                "validations": {
                    "old-explanation": {"stage_authority": "explain-change"},
                },
            },
        }
        errors = validate_stage_owned_lifecycle_metadata(change)
        self.assertTrue(any(error.startswith("workflow_state.current_stage: unknown_value") for error in errors))
        self.assertTrue(any("stage_authority: unknown_value explain-change" in error for error in errors))

    def test_manifest_classifies_exact_prior_records(self) -> None:
        manifest = self.fixture["active_manifest"]
        self.assertEqual(validate_lifecycle_activation_manifest(manifest), [])
        self.assertEqual(classify_lifecycle_contract("new-v2", {"lifecycle_contract": "stage-owned-change-local-v2"}, manifest)["contract_class"], "stage-owned-change-local-v2")
        self.assertEqual(classify_lifecycle_contract("v1", {"lifecycle_contract": "stage-owned-change-local-v1"}, manifest)["contract_class"], "stage-owned-change-local-v1")
        self.assertEqual(classify_lifecycle_contract("legacy", {}, manifest)["contract_class"], "legacy-unversioned")

    def test_manifest_rejects_missing_mismatch_and_v2_test_spec_state(self) -> None:
        manifest = self.fixture["active_manifest"]
        with self.assertRaisesRegex(ValueError, "not present in the activation manifest"):
            classify_lifecycle_contract("missing", {"lifecycle_contract": "stage-owned-change-local-v1"}, manifest)
        with self.assertRaisesRegex(ValueError, "does not match"):
            classify_lifecycle_contract("legacy", {"lifecycle_contract": "stage-owned-change-local-v1"}, manifest)
        with self.assertRaisesRegex(ValueError, "active test-spec state"):
            classify_lifecycle_contract("new-v2", {
                "lifecycle_contract": "stage-owned-change-local-v2",
                "workflow_state": {"current_stage": "test-spec"},
            }, manifest)
        with self.assertRaisesRegex(ValueError, "active test-spec state"):
            classify_lifecycle_contract("new-v2", {
                "lifecycle_contract": "stage-owned-change-local-v2",
                "lifecycle_cli": {"reviews": {"test-spec": {"stage_authority": "test-spec-review"}}},
            }, manifest)

    def test_unknown_value_contract_fails_before_manifest_consistency(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown_value.*future-v9"):
            classify_lifecycle_contract("missing", {"lifecycle_contract": "future-v9"}, self.fixture["active_manifest"])

    def test_explicit_null_contract_is_unknown_value_not_legacy(self) -> None:
        case = self.fixture["contract_cases"]["explicit_null"]
        with self.assertRaisesRegex(ValueError, case["error"]):
            classify_lifecycle_contract(case["change_id"], case["change"], self.fixture["active_manifest"])

    def test_public_validator_rejects_v2_active_test_spec_state(self) -> None:
        validator = load_validator_module()
        with tempfile.TemporaryDirectory(prefix="change-metadata-v2-contract-") as temp_dir:
            target = Path(temp_dir) / "change.yaml"
            text = VALID_BASIC_FIXTURE.read_text(encoding="utf-8").replace(
                "change_id: valid-basic",
                "change_id: new-v2\nlifecycle_contract: stage-owned-change-local-v2\nworkflow_state:\n  current_stage: test-spec",
                1,
            )
            target.write_text(text, encoding="utf-8")
            errors = validator.validate_file(
                target,
                activation_manifest=self.fixture["active_manifest"],
            )
        self.assertIn("v2 lifecycle contract carries active test-spec state", errors)

    def test_unknown_value_activation_state_fails_before_consistency(self) -> None:
        manifest = copy.deepcopy(self.fixture["active_manifest"])
        manifest["state"] = "published"
        manifest["changes"].append(copy.deepcopy(manifest["changes"][0]))
        self.assertRegex(validate_lifecycle_activation_manifest(manifest)[0], "state: unknown_value published")

    def test_classification_ignores_heuristic_facts(self) -> None:
        manifest = self.fixture["active_manifest"]
        baseline = classify_lifecycle_contract("v1", {"lifecycle_contract": "stage-owned-change-local-v1"}, manifest)
        changed = classify_lifecycle_contract("v1", {
            "lifecycle_contract": "stage-owned-change-local-v1",
            "created_at": "2999-01-01",
            "workflow_state": {"current_stage": "implement"},
            "artifacts": {"plan": "docs/plans/example.md"},
            "git_reachable": False,
            "network_available": False,
        }, manifest)
        self.assertEqual(changed, baseline)

    def test_activation_prerequisites_report_exact_blocking_change_ids(self) -> None:
        manifest = copy.deepcopy(self.fixture["active_manifest"])
        records = {
            "Z-change": {"lifecycle_contract": "stage-owned-change-local-v1", "workflow_state": {"lifecycle_state": "completed"}},
            "a-change": {"workflow_state": {"lifecycle_state": "completed"}},
            "legacy": {
                "workflow_state": {"lifecycle_state": "completed"},
            },
            "v1": {
                "lifecycle_contract": "stage-owned-change-local-v1",
                "workflow_state": {"lifecycle_state": "active", "current_stage": "plan"},
                "review_packages": {},
            },
        }
        errors = validate_lifecycle_activation_prerequisites(manifest, records)
        self.assertEqual(
            errors,
            ["activation prerequisite blocked by prior-contract changes: v1"],
        )

    def test_activation_prerequisites_accept_post_delivery_and_terminal_records(self) -> None:
        manifest = copy.deepcopy(self.fixture["active_manifest"])
        records = {
            "Z-change": {"lifecycle_contract": "stage-owned-change-local-v1", "workflow_state": {"lifecycle_state": "completed"}},
            "a-change": {"workflow_state": {"lifecycle_state": "completed"}},
            "legacy": {"workflow_state": {"lifecycle_state": "completed"}},
            "v1": {
                "lifecycle_contract": "stage-owned-change-local-v1",
                "workflow_state": {"lifecycle_state": "active", "current_stage": "implement"},
                "review_packages": {
                    "delivery": {
                        "status": "approved",
                        "authority": "granted",
                        "members": {
                            "plan": "docs/plans/v1.md",
                            "test-spec": "specs/v1.test.md",
                        },
                    }
                },
            },
        }
        self.assertEqual(validate_lifecycle_activation_prerequisites(manifest, records), [])

    def test_activation_prerequisites_accept_legacy_plan_and_test_spec_reviews(self) -> None:
        manifest = copy.deepcopy(self.fixture["active_manifest"])
        records = {
            "Z-change": {"lifecycle_contract": "stage-owned-change-local-v1", "workflow_state": {"lifecycle_state": "completed"}},
            "a-change": {"workflow_state": {"lifecycle_state": "completed"}},
            "legacy": {"workflow_state": {"lifecycle_state": "completed"}},
            "v1": {
                "lifecycle_contract": "stage-owned-change-local-v1",
                "workflow_state": {"lifecycle_state": "active", "current_stage": "verify"},
                "artifact_states": {
                    "plan": {"kind": "plan", "role": "primary", "path": "docs/plans/v1.md", "review": {"outcome": "approved"}},
                    "test-spec": {"kind": "test-spec", "role": "primary", "path": "specs/v1.test.md", "review": {"outcome": "approved"}},
                },
            },
        }
        self.assertEqual(validate_lifecycle_activation_prerequisites(manifest, records), [])

    def test_activation_prerequisites_reject_unknown_state_before_readiness(self) -> None:
        manifest = copy.deepcopy(self.fixture["active_manifest"])
        records = {
            "Z-change": {"lifecycle_contract": "stage-owned-change-local-v1", "workflow_state": {"lifecycle_state": "completed"}},
            "a-change": {"workflow_state": {"lifecycle_state": "completed"}},
            "legacy": {"workflow_state": {"lifecycle_state": "completed"}},
            "v1": {
                "lifecycle_contract": "stage-owned-change-local-v1",
                "workflow_state": {"lifecycle_state": "future-state", "current_stage": "implement"},
            },
        }
        self.assertEqual(
            validate_lifecycle_activation_prerequisites(manifest, records),
            ["prior-contract change v1 lifecycle_state: unknown_value future-state"],
        )

    def test_activation_prerequisites_reject_unknown_stage_before_readiness(self) -> None:
        manifest = copy.deepcopy(self.fixture["active_manifest"])
        records = {
            "Z-change": {"lifecycle_contract": "stage-owned-change-local-v1", "workflow_state": {"lifecycle_state": "completed"}},
            "a-change": {"workflow_state": {"lifecycle_state": "completed"}},
            "legacy": {"workflow_state": {"lifecycle_state": "completed"}},
            "v1": {
                "lifecycle_contract": "stage-owned-change-local-v1",
                "workflow_state": {"lifecycle_state": "active", "current_stage": "future-stage"},
            },
        }
        self.assertEqual(
            validate_lifecycle_activation_prerequisites(manifest, records),
            ["prior-contract change v1 current_stage: unknown_value future-stage"],
        )


class FinalVerificationProtocolTests(unittest.TestCase):
    def basis(self) -> dict[str, str]:
        return {
            "repository_identity": "repo:sha256:" + "1" * 64,
            "remote_identity": "remote:sha256:" + "2" * 64,
            "base_branch": "main",
            "base_revision": "d" * 40,
            "merge_base_revision": "e" * 40,
            "head_branch": "proposal/example",
            "governed_change_id": "2026-08-31-example",
            "verified_subject_revision": "a" * 40,
            "final_review_id": "code-review-r1",
            "design_package_id": "design-review-r1",
            "delivery_plan_id": "docs/plans/2026-08-31-example.md",
            "final_diff_sha256": "sha256:" + "b" * 64,
        }

    def impact(self, state: str = "unaffected") -> list[dict[str, object]]:
        return [{
            "surface": "runtime-behavior",
            "state": state,
            "rationale": "The reviewed metadata-only tail cannot alter runtime inputs.",
            "affirmative_evidence": ["TG-06:runtime-input-boundary"],
        }]

    def obligation(self, **updates: object) -> dict[str, object]:
        value: dict[str, object] = {
            "evidence_id": "TG-06-runtime",
            "proved_surfaces": ["runtime-behavior"],
            "freshness": "impact-sensitive",
            "existing_result": "pass",
            "authority_current": True,
            "identity_current": True,
            "environment_current": True,
            "conflicting": False,
            "new_obligation": False,
        }
        value.update(updates)
        return value

    def successful_result(self) -> dict[str, object]:
        return {
            "protocol_version": 3,
            "outcome": "successful",
            "basis": self.basis(),
            "basis_status": {
                "repository": "current",
                "governed_change": "current",
                "verified_subject": "current",
                "final_review": "current",
                "design_package": "current",
                "delivery_plan": "current",
                "final_diff": "current",
            },
            "impact": self.impact(),
            "evidence": [{
                **self.obligation(),
                "decision": "reuse",
                "decision_rationale": "Affirmative non-impact proof preserves this passing result.",
                "execution": "reused-pass",
                "observed_result": "pass",
                "cache_hit": False,
                "proof": {
                    "kind": "prior-evidence",
                    "evidence_path": "docs/changes/example/evidence/tg-06.md",
                    "evidence_sha256": "sha256:" + "3" * 64,
                    "subject_revision": "a" * 40,
                },
            }],
            "always_current": [
                {
                    "check_id": check_id,
                    "execution": "actual-run",
                    "observed_result": "pass",
                    "proof": {
                        "kind": "command",
                        "command": ["python", "scripts/validate-change-metadata.py", "docs/changes/example/change.yaml"],
                        "evidence_path": "docs/changes/example/evidence/always-current.md",
                        "evidence_sha256": "sha256:" + "4" * 64,
                    },
                }
                for check_id in (
                    "current-change-and-repository-identity",
                    "reviewed-subject-and-review-identity",
                    "lifecycle-and-package-consistency",
                    "review-closeout",
                    "unresolved-blocker-state",
                    "final-diff-classification",
                    "required-artifact-and-evidence-existence",
                    "complete-verify-result-consistency",
                )
            ],
            "ci_status": "not-required",
            "blockers": [],
            "residual_risks": ["Semantic non-impact judgment remains reviewable."],
            "branch_ready": True,
            "explanation": {
                "what_changed": "Added the inactive final-verification protocol.",
                "why": "Enable impact-aware evidence selection.",
                "requirements_and_design": "Implements FV-R8 through FV-R22.",
                "important_choices": "Uses conservative structural checks.",
                "supporting_evidence": ["TG-06-runtime"],
                "limitations": ["The v3 public route remains inactive."],
                "residual_risks": ["Semantic decisions require review."],
            },
        }

    def test_closed_vocabulary_unknown_values_fail_before_consistency(self) -> None:
        cases = (
            ("impact-surface", {**self.successful_result(), "impact": [{**self.impact()[0], "surface": "magic-surface"}]}, "impact[0].surface: unknown_value magic-surface"),
            ("impact", {**self.successful_result(), "impact": self.impact("future-impact")}, "impact[0].state: unknown_value future-impact"),
            ("freshness", {**self.successful_result(), "evidence": [{**self.successful_result()["evidence"][0], "freshness": "eventually-fresh"}]}, "evidence[0].freshness: unknown_value eventually-fresh"),
            ("decision", {**self.successful_result(), "evidence": [{**self.successful_result()["evidence"][0], "decision": "skip"}]}, "evidence[0].decision: unknown_value skip"),
            ("evidence-result", {**self.successful_result(), "evidence": [{**self.successful_result()["evidence"][0], "observed_result": "mostly-pass"}]}, "evidence[0].observed_result: unknown_value mostly-pass"),
            ("execution", {**self.successful_result(), "evidence": [{**self.successful_result()["evidence"][0], "execution": "assumed-run"}]}, "evidence[0].execution: unknown_value assumed-run"),
            ("outcome", {**self.successful_result(), "outcome": "mostly-successful"}, "outcome: unknown_value mostly-successful"),
            ("basis-status", {**self.successful_result(), "basis_status": {**self.successful_result()["basis_status"], "final_diff": "probably-current"}}, "basis_status.final_diff: unknown_value probably-current"),
            ("ci-status", {**self.successful_result(), "ci_status": "probably-passed"}, "ci_status: unknown_value probably-passed"),
            ("always-current-check", {**self.successful_result(), "always_current": [{**self.successful_result()["always_current"][0], "check_id": "probably-current"}, *self.successful_result()["always_current"][1:]]}, "always_current[0].check_id: unknown_value probably-current"),
            ("proof-kind", {**self.successful_result(), "evidence": [{**self.successful_result()["evidence"][0], "proof": {"kind": "asserted"}}]}, "evidence[0].proof.kind: unknown_value asserted"),
        )
        for name, result, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(validate_final_verification_result(result)[0], expected)

    def test_target_basis_requires_exact_singleton_identities(self) -> None:
        result = self.successful_result()
        result["basis"] = {**self.basis(), "final_review_id": ["r1", "r2"]}
        self.assertIn("basis.final_review_id: invalid canonical identity", validate_final_verification_result(result))

        stale = self.successful_result()
        stale["basis_status"]["final_review"] = "stale"
        self.assertIn("successful result requires every basis authority current", validate_final_verification_result(stale))

    def test_unaffected_requires_affirmative_evidence_not_filename(self) -> None:
        result = self.successful_result()
        result["impact"] = [{
            "surface": "repository-metadata",
            "state": "unaffected",
            "rationale": ".gitignore file extension",
            "affirmative_evidence": [],
        }]
        self.assertIn("impact[0].unaffected: affirmative_evidence required", validate_final_verification_result(result))

    def test_unknown_impact_broadens_and_freshness_overrides_reuse(self) -> None:
        self.assertEqual(evaluate_evidence_decision(self.obligation(), self.impact("unknown")), "rerun")
        self.assertEqual(evaluate_evidence_decision(self.obligation(freshness="fresh-required"), self.impact()), "rerun")
        self.assertEqual(evaluate_evidence_decision(self.obligation(freshness="always-current"), self.impact()), "rerun")

    def test_new_obligation_and_multi_surface_impact_select_execution(self) -> None:
        impacts = self.impact() + [{
            "surface": "generated-output",
            "state": "affected",
            "rationale": "Generator input changed.",
            "affirmative_evidence": [],
        }]
        self.assertEqual(evaluate_evidence_decision(self.obligation(new_obligation=True), impacts), "newly-required")
        self.assertEqual(evaluate_evidence_decision(self.obligation(proved_surfaces=["runtime-behavior", "generated-output"]), impacts), "rerun")

    def test_proved_surfaces_are_closed_unique_and_mapped_before_freshness(self) -> None:
        for proved_surfaces, expected in (
            (["magic-surface"], "evidence[0].proved_surfaces[0]: unknown_value magic-surface"),
            (["runtime-behavior", "runtime-behavior"], "evidence[0].proved_surfaces: duplicate runtime-behavior"),
            (["generated-output"], "evidence[0].proved_surfaces[0]: unclassified generated-output"),
        ):
            result = self.successful_result()
            result["evidence"][0].update({"freshness": "fresh-required", "decision": "rerun", "execution": "actual-run", "proved_surfaces": proved_surfaces, "proof": {
                "kind": "command", "command": ["npm", "test"], "evidence_path": "docs/changes/example/evidence/test.md", "evidence_sha256": "sha256:" + "5" * 64,
            }})
            with self.subTest(proved_surfaces=proved_surfaces):
                self.assertIn(expected, validate_final_verification_result(result))
        with self.assertRaisesRegex(ValueError, "unknown_value magic-surface"):
            evaluate_evidence_decision(self.obligation(freshness="fresh-required", proved_surfaces=["magic-surface"]), self.impact())

    def test_cache_hit_cannot_satisfy_required_execution(self) -> None:
        result = self.successful_result()
        result["evidence"] = [{
            **self.obligation(freshness="fresh-required"),
            "decision": "rerun",
            "decision_rationale": "Policy requires fresh evidence.",
            "execution": "cache-hit",
            "observed_result": "pass",
            "cache_hit": True,
            "proof": {"kind": "cache", "cache_key": "sha256:" + "6" * 64},
        }]
        self.assertIn("evidence[0].execution: rerun requires actual-run or hosted-observation", validate_final_verification_result(result))

    def test_non_success_omits_explanation_and_readiness(self) -> None:
        for outcome in ("failed", "inconclusive", "interrupted"):
            result = self.successful_result()
            result.update({"outcome": outcome, "branch_ready": False, "blockers": ["owner: plan"], "explanation": None})
            self.assertEqual(validate_final_verification_result(result), [], outcome)
            result["explanation"] = self.successful_result()["explanation"]
            self.assertIn(f"{outcome} result must omit explanation", validate_final_verification_result(result))

    def test_early_inconclusive_result_may_record_unresolved_inputs(self) -> None:
        result = self.successful_result()
        result.update({
            "outcome": "inconclusive",
            "basis": {field: None for field in self.basis()},
            "basis_status": {field: "missing" for field in result["basis_status"]},
            "impact": [],
            "evidence": [],
            "always_current": [],
            "blockers": ["owner: workflow; exact target unresolved"],
            "branch_ready": False,
            "explanation": None,
        })
        self.assertEqual(validate_final_verification_result(result), [])

    def test_success_serializes_and_reads_back_without_self_commit_identity(self) -> None:
        result = self.successful_result()
        rendered = render_verify_report(result)
        self.assertEqual(parse_verify_report(rendered), result)
        self.assertNotIn("report_commit", rendered)
        self.assertEqual(validate_final_verification_result(result), [])

        result["report_commit_identity"] = "f" * 40
        self.assertIn("result: Verify report must not embed its own Git commit identity", validate_final_verification_result(result))

        with self.assertRaisesRegex(ValueError, "trailing or malformed content"):
            parse_verify_report(rendered + "trailing\n")

    def test_execution_kinds_require_exact_proof_identity(self) -> None:
        for target, index in (("evidence", 0), ("always_current", 0)):
            result = self.successful_result()
            result[target][index]["proof"] = None
            with self.subTest(target=target):
                self.assertTrue(any("proof" in error for error in validate_final_verification_result(result)))

        hosted = self.successful_result()
        hosted["always_current"][0].update({"execution": "hosted-observation", "proof": {
            "kind": "hosted", "provider": "github-actions", "run_id": "12345", "check_name": "test", "subject_revision": "a" * 40,
            "evidence_path": "docs/changes/example/evidence/hosted.md", "evidence_sha256": "sha256:" + "7" * 64,
        }})
        self.assertEqual(validate_final_verification_result(hosted), [])

    def test_report_write_and_registration_failure_grant_no_authority(self) -> None:
        for failure in ("report-write-failure", "registration-failure"):
            result = self.successful_result()
            result.update({"outcome": "inconclusive", "branch_ready": False, "blockers": [failure], "explanation": None})
            self.assertEqual(validate_final_verification_result(result), [], failure)

    def test_identical_replay_is_idempotent_and_changed_basis_is_new(self) -> None:
        result = self.successful_result()
        self.assertEqual(replay_disposition(result, parse_verify_report(render_verify_report(result))), "identical-replay")
        changed = copy.deepcopy(result)
        changed["basis"]["final_diff_sha256"] = "sha256:" + "c" * 64
        self.assertEqual(replay_disposition(result, changed), "changed-basis")

    def test_tail_drift_allows_only_verify_owned_paths_and_fields(self) -> None:
        report = render_verify_report(self.successful_result())
        report_sha = "sha256:" + hashlib.sha256(report.encode()).hexdigest()
        tail = {
            "changed_paths": ["docs/changes/example/verify-report.md", "docs/changes/example/change.yaml#lifecycle_cli.validations.verify-result"],
            "report_path": "docs/changes/example/verify-report.md",
            "report_content": report,
            "report_sha256": report_sha,
            "registration": {
                "selector": "lifecycle_cli.validations.verify-result",
                "evidence_path": "docs/changes/example/verify-report.md",
                "evidence_sha256": report_sha,
                "verified_subject_revision": "a" * 40,
                "stage_authority": "verify",
            },
        }
        self.assertEqual(tail_disposition(tail, "example", "a" * 40), "current")
        for path in ("src/product.py", "specs/feature.md", "docs/plans/feature.md", "package-lock.json", "docs/unrelated.md"):
            with self.subTest(path=path):
                changed = copy.deepcopy(tail)
                changed["changed_paths"].append(path)
                self.assertEqual(tail_disposition(changed, "example", "a" * 40), "stale")
        for mutate in (
            lambda value: value.update({"changed_paths": []}),
            lambda value: value.update({"changed_paths": [value["report_path"]]}),
            lambda value: value.update({"changed_paths": ["docs/changes/example/change.yaml#lifecycle_cli.validations.verify-result"]}),
            lambda value: value.update({"changed_paths": [value["report_path"], value["report_path"]]}),
            lambda value: value["registration"].update({"evidence_sha256": "sha256:" + "0" * 64}),
            lambda value: value["registration"].update({"verified_subject_revision": "f" * 40}),
            lambda value: value["registration"].update({"selector": "validation_events.verify"}),
        ):
            changed = copy.deepcopy(tail)
            mutate(changed)
            self.assertEqual(tail_disposition(changed, "example", "a" * 40), "incomplete")

    def test_pr_handoff_consumes_exact_successful_verify_authority(self) -> None:
        result = self.successful_result()
        report = render_verify_report(result)
        report_sha = "sha256:" + hashlib.sha256(report.encode()).hexdigest()
        tail = {
            "changed_paths": ["docs/changes/example/verify-report.md", "docs/changes/example/change.yaml#lifecycle_cli.validations.verify-result"],
            "report_path": "docs/changes/example/verify-report.md",
            "report_content": report,
            "report_sha256": report_sha,
            "registration": {
                "selector": "lifecycle_cli.validations.verify-result",
                "evidence_path": "docs/changes/example/verify-report.md",
                "evidence_sha256": report_sha,
                "verified_subject_revision": "a" * 40,
                "stage_authority": "verify",
            },
        }
        references = sorted({
            tail["report_path"],
            result["basis"]["delivery_plan_id"],
            *(item["proof"]["evidence_path"] for item in [*result["evidence"], *result["always_current"]]),
        })
        inputs = {
            "tail": tail,
            "change_id": "example",
            "verified_subject_revision": "a" * 40,
            "current_basis": result["basis"],
            "explanation": result["explanation"],
            "authoritative_references": references,
        }
        self.assertTrue(evaluate_pr_handoff(**inputs)["ready"])
        competing = copy.deepcopy(inputs)
        competing["explanation"]["why"] = "competing"
        self.assertEqual(evaluate_pr_handoff(**competing)["reason"], "competing-rationale")
        new_reference = copy.deepcopy(inputs)
        new_reference["authoritative_references"].append("docs/new-authority.md")
        self.assertEqual(evaluate_pr_handoff(**new_reference)["reason"], "authoritative-reference-mismatch")

    def test_success_rejects_duplicate_checks_empty_explanation_and_malformed_basis(self) -> None:
        duplicate = self.successful_result()
        duplicate["always_current"].append(copy.deepcopy(duplicate["always_current"][0]))
        self.assertIn("always_current[8].check_id: duplicate current-change-and-repository-identity", validate_final_verification_result(duplicate))
        for value in ("   ", ["valid", "   "]):
            result = self.successful_result()
            result["explanation"]["what_changed"] = value
            self.assertIn("successful result explanation fields must be non-empty", validate_final_verification_result(result))
        for field, value in (
            ("repository_identity", "github.com/example/project"),
            ("remote_identity", "origin"),
            ("base_branch", "refs/../main"),
            ("head_branch", "feature.lock"),
            ("base_revision", "not-a-revision"),
            ("merge_base_revision", "abc"),
            ("verified_subject_revision", "x"),
            ("governed_change_id", 12),
            ("final_review_id", "review/r1"),
            ("design_package_id", "design r1"),
            ("delivery_plan_id", "../plan.md"),
            ("final_diff_sha256", "not-a-digest"),
        ):
            result = self.successful_result()
            result["basis"][field] = value
            with self.subTest(field=field):
                self.assertTrue(any(error.startswith(f"basis.{field}:") for error in validate_final_verification_result(result)))

    def test_collection_shapes_are_required_for_every_outcome(self) -> None:
        for field in ("impact", "evidence", "always_current"):
            for value in (None, "items", {"item": True}, 1):
                result = self.successful_result()
                result.update({
                    "outcome": "inconclusive",
                    "branch_ready": False,
                    "blockers": ["owner: workflow"],
                    "explanation": None,
                    field: value,
                })
                with self.subTest(field=field, value=value):
                    self.assertIn(f"{field}: expected array", validate_final_verification_result(result))

        result = self.successful_result()
        for field in ("impact", "evidence", "always_current"):
            empty = copy.deepcopy(result)
            empty[field] = []
            with self.subTest(success_empty=field):
                self.assertNotEqual(validate_final_verification_result(empty), [])

        inconclusive = self.successful_result()
        inconclusive.update({
            "outcome": "inconclusive",
            "branch_ready": False,
            "blockers": ["owner: workflow"],
            "explanation": None,
            "impact": [],
            "evidence": [],
            "always_current": [],
        })
        self.assertEqual(validate_final_verification_result(inconclusive), [])

    def test_evidence_facts_require_json_booleans(self) -> None:
        fields = (
            "authority_current",
            "identity_current",
            "environment_current",
            "conflicting",
            "new_obligation",
            "cache_hit",
        )
        for field in fields:
            for value in ("yes", 1, None, {}, []):
                result = self.successful_result()
                result["evidence"][0][field] = value
                with self.subTest(field=field, value=value):
                    self.assertIn(
                        f"evidence[0].{field}: expected boolean",
                        validate_final_verification_result(result),
                    )

        for field in fields:
            for value in (True, False):
                result = self.successful_result()
                result["evidence"][0][field] = value
                with self.subTest(valid_field=field, value=value):
                    self.assertFalse(any(
                        error == f"evidence[0].{field}: expected boolean"
                        for error in validate_final_verification_result(result)
                    ))
        with self.assertRaisesRegex(ValueError, "authority_current: expected boolean"):
            evaluate_evidence_decision(self.obligation(authority_current="yes"), self.impact())

    def test_javascript_and_python_result_conformance_matches(self) -> None:
        cases = [self.successful_result()]
        duplicate = self.successful_result()
        duplicate["always_current"].append(copy.deepcopy(duplicate["always_current"][0]))
        cases.append(duplicate)
        whitespace = self.successful_result()
        whitespace["explanation"]["what_changed"] = ["valid", "   "]
        cases.append(whitespace)
        unknown_surface = self.successful_result()
        unknown_surface["evidence"][0]["proved_surfaces"] = ["magic-surface"]
        cases.append(unknown_surface)
        malformed_basis = self.successful_result()
        malformed_basis["basis"]["verified_subject_revision"] = "not-a-revision"
        cases.append(malformed_basis)
        missing_proof = self.successful_result()
        missing_proof["always_current"][0]["proof"] = None
        cases.append(missing_proof)
        for field in ("impact", "evidence", "always_current"):
            for value in (None, "items", {"item": True}, 1):
                malformed_collection = self.successful_result()
                malformed_collection.update({
                    "outcome": "inconclusive",
                    "branch_ready": False,
                    "blockers": ["owner: workflow"],
                    "explanation": None,
                    field: value,
                })
                cases.append(malformed_collection)
        for field in (
            "authority_current",
            "identity_current",
            "environment_current",
            "conflicting",
            "new_obligation",
            "cache_hit",
        ):
            for value in ("yes", 1, None, {}, []):
                malformed_boolean = self.successful_result()
                malformed_boolean["evidence"][0][field] = value
                cases.append(malformed_boolean)

        node_source = """
import { validateFinalVerificationResult } from './packages/rigorloop/dist/lib/final-verification-protocol.js';
let input = '';
for await (const chunk of process.stdin) input += chunk;
process.stdout.write(JSON.stringify(JSON.parse(input).map(validateFinalVerificationResult)));
"""
        completed = subprocess.run(
            ["node", "--input-type=module", "--eval", node_source],
            input=json.dumps(cases),
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=True,
        )
        self.assertEqual(
            json.loads(completed.stdout),
            [validate_final_verification_result(case) for case in cases],
        )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
