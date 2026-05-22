#!/usr/bin/env python3
"""Regression tests for bounded change-record query helper."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "query-change-record.py"


def run_query(*args: str, repo_root: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = ["python", str(SCRIPT), *args]
    if repo_root is not None:
        command.extend(["--repo-root", str(repo_root)])
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def parse_json(result: subprocess.CompletedProcess[str]) -> dict:
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"stdout was not JSON: {result.stdout!r}; stderr={result.stderr!r}") from exc


class QueryChangeRecordTests(unittest.TestCase):
    def make_change(self, change_id: str, body: str) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        repo = Path(temp.name)
        change_root = repo / "docs" / "changes" / change_id
        change_root.mkdir(parents=True)
        (change_root / "change.yaml").write_text(body, encoding="utf-8")
        return repo

    def compact_change_yaml(self, *, validation_events: str | None = None, summary: str | None = None) -> str:
        events = validation_events if validation_events is not None else """
  - stage: proposal-review-r1
    lifecycle_stage: proposal-review
    bundles:
      - metadata
    result: pass
    counts:
      reviews: 1
      findings: 0
      log_entries: 1
      resolution_entries: 0
  - stage: code-review-r1
    lifecycle_stage: code-review
    bundles:
      - metadata
      - lifecycle
    result: blocked
    counts:
      reviews: 2
      findings: 1
      log_entries: 2
      resolution_entries: 1
    failures:
      - code: CR1
        message: unresolved review finding
    evidence:
      transcript: docs/changes/2026-05-22-query-fixture/validation-log.md#code-review-r1
"""
        summary_block = summary if summary is not None else """
  all_passed: false
  stages_validated:
    - proposal-review-r1
  final_counts:
    reviews: 2
    findings: 1
    log_entries: 2
    resolution_entries: 1
  open_validation_blockers:
    - code-review-r1
"""
        return f"""schema_version: 2
path_vars:
  change_id: 2026-05-22-query-fixture
  change_root: docs/changes/2026-05-22-query-fixture
artifacts:
  spec: specs/query-fixture.md
  test_spec: specs/query-fixture.test.md
  plan: docs/plans/query-fixture.md
review:
  status: changes-requested
  unresolved_items: 1
validation_bundles:
  metadata:
    command: python should-not-run.py
  lifecycle:
    command: python should-not-run-either.py
validation_events:{events}
validation_summary:{summary_block}
"""

    def legacy_change_yaml(self) -> str:
        return """change_id: 2026-05-22-legacy-query
title: Legacy query fixture
classification: default
risk: low
artifacts:
  proposal: docs/changes/2026-05-22-legacy-query/proposal.md
  plan: docs/changes/2026-05-22-legacy-query/plan.md
review:
  status: resolved
  unresolved_items: 0
validation:
  - command: python scripts/validate-change-metadata.py docs/changes/2026-05-22-legacy-query/change.yaml
    result: pass
  - command: python scripts/test-query-change-record.py
    result: fail
changed_files:
  - scripts/query-change-record.py
"""

    def compact_path_vars_change_yaml(
        self,
        *,
        path_vars: str | None = None,
    ) -> str:
        path_vars_block = path_vars if path_vars is not None else """
  change_id: 2026-05-21-compact-fixture
  slug: compact-fixture
  change_root: docs/changes/{change_id}
  spec: specs/{slug}.md
  test_spec: specs/{slug}.test.md
  plan: docs/plans/{change_id}.md
"""
        return f"""schema_version: 2
path_vars:{path_vars_block}
validation_bundles:
  metadata:
    command: python scripts/validate-change-metadata.py {{change_root}}/change.yaml
validation_events:
  - stage: spec-review-r1
    lifecycle_stage: spec-review
    bundles:
      - metadata
    result: pass
validation_summary:
  all_passed: true
  stages_validated:
    - spec-review-r1
  open_validation_blockers: []
"""

    def test_summary_returns_common_read_slice_for_compact_metadata(self) -> None:
        repo = self.make_change("2026-05-22-query-fixture", self.compact_change_yaml())

        result = run_query("2026-05-22-query-fixture", "summary", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["query"], "summary")
        self.assertEqual(payload["change_id"], "2026-05-22-query-fixture")
        self.assertEqual(
            payload["artifact_paths"],
            [
                "docs/plans/query-fixture.md",
                "specs/query-fixture.md",
                "specs/query-fixture.test.md",
            ],
        )
        self.assertEqual(payload["review_state"]["status"], "changes-requested")
        self.assertEqual(payload["latest_validation"]["stage"], "code-review-r1")
        self.assertEqual(payload["latest_validation"]["result"], "blocked")
        self.assertEqual(payload["open_blockers"], ["code-review-r1"])
        self.assertIn("validation_history", payload["detail_pointers"])
        self.assertNotIn("validation_events", payload)

    def test_summary_supports_legacy_metadata(self) -> None:
        repo = self.make_change("2026-05-22-legacy-query", self.legacy_change_yaml())

        result = run_query("2026-05-22-legacy-query", "summary", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["metadata_shape"], "legacy")
        self.assertEqual(payload["latest_validation"]["result"], "fail")
        self.assertEqual(payload["review_state"]["status"], "resolved")

    def test_artifacts_returns_canonical_paths_only(self) -> None:
        repo = self.make_change("2026-05-22-query-fixture", self.compact_change_yaml())

        result = run_query("2026-05-22-query-fixture", "artifacts", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["query"], "artifacts")
        self.assertEqual(set(payload), {"status", "query", "change_id", "artifact_paths"})
        self.assertEqual(
            payload["artifact_paths"],
            [
                "docs/plans/query-fixture.md",
                "specs/query-fixture.md",
                "specs/query-fixture.test.md",
            ],
        )

    def test_compact_path_vars_artifacts_are_expanded_without_top_level_artifacts(self) -> None:
        repo = self.make_change(
            "2026-05-21-compact-fixture",
            self.compact_path_vars_change_yaml(),
        )

        result = run_query("2026-05-21-compact-fixture", "artifacts", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(
            payload["artifact_paths"],
            [
                "docs/plans/2026-05-21-compact-fixture.md",
                "specs/compact-fixture.md",
                "specs/compact-fixture.test.md",
            ],
        )

    def test_compact_path_vars_summary_includes_expanded_artifacts(self) -> None:
        repo = self.make_change(
            "2026-05-21-compact-fixture",
            self.compact_path_vars_change_yaml(),
        )

        result = run_query("2026-05-21-compact-fixture", "summary", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("specs/compact-fixture.md", payload["artifact_paths"])
        self.assertIn("specs/compact-fixture.test.md", payload["artifact_paths"])
        self.assertIn("docs/plans/2026-05-21-compact-fixture.md", payload["artifact_paths"])

    def test_compact_artifact_paths_exclude_expansion_only_path_vars(self) -> None:
        repo = self.make_change(
            "2026-05-21-compact-fixture",
            self.compact_path_vars_change_yaml(),
        )

        result = run_query("2026-05-21-compact-fixture", "artifacts", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertNotIn("2026-05-21-compact-fixture", payload["artifact_paths"])
        self.assertNotIn("compact-fixture", payload["artifact_paths"])
        self.assertNotIn("docs/changes/2026-05-21-compact-fixture", payload["artifact_paths"])

    def test_compact_path_var_artifact_with_unsafe_path_fails_closed(self) -> None:
        repo = self.make_change(
            "2026-05-21-compact-fixture",
            self.compact_path_vars_change_yaml(
                path_vars="""
  change_id: 2026-05-21-compact-fixture
  slug: compact-fixture
  spec: /Users/alice/spec.md
"""
            ),
        )

        result = run_query("2026-05-21-compact-fixture", "artifacts", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["code"], "unsupported-shape")
        self.assertIn("path_vars.spec", payload["detail"])

    def test_compact_path_var_artifact_with_unresolved_variable_fails_closed(self) -> None:
        repo = self.make_change(
            "2026-05-21-compact-fixture",
            self.compact_path_vars_change_yaml(
                path_vars="""
  change_id: 2026-05-21-compact-fixture
  slug: compact-fixture
  spec: specs/{missing}.md
"""
            ),
        )

        result = run_query("2026-05-21-compact-fixture", "summary", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["code"], "unsupported-shape")
        self.assertIn("path_vars.spec", payload["detail"])

    def test_validation_latest_returns_only_latest_compact_event(self) -> None:
        repo = self.make_change("2026-05-22-query-fixture", self.compact_change_yaml())

        result = run_query("2026-05-22-query-fixture", "validation", "--latest", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["query"], "validation")
        self.assertEqual(payload["mode"], "latest")
        self.assertEqual(payload["validation"]["stage"], "code-review-r1")
        self.assertEqual(payload["validation"]["result"], "blocked")
        self.assertEqual(payload["validation"]["bundles"], ["metadata", "lifecycle"])
        self.assertEqual(payload["validation"]["counts"]["findings"], 1)
        self.assertEqual(payload["validation"]["blockers"], ["CR1"])
        self.assertEqual(
            payload["validation"]["transcript"],
            "docs/changes/2026-05-22-query-fixture/validation-log.md#code-review-r1",
        )
        self.assertNotIn("proposal-review-r1", json.dumps(payload))

    def test_validation_stage_returns_requested_event_only(self) -> None:
        repo = self.make_change("2026-05-22-query-fixture", self.compact_change_yaml())

        result = run_query(
            "2026-05-22-query-fixture",
            "validation",
            "--stage",
            "proposal-review-r1",
            repo_root=repo,
        )
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["mode"], "stage")
        self.assertEqual(payload["validation"]["stage"], "proposal-review-r1")
        self.assertEqual(payload["validation"]["result"], "pass")
        self.assertNotIn("code-review-r1", json.dumps(payload))

    def test_validation_latest_without_evidence_reports_stable_diagnostic(self) -> None:
        repo = self.make_change(
            "2026-05-22-query-fixture",
            self.compact_change_yaml(validation_events="\n", summary="\n  all_passed: false\n"),
        )

        result = run_query("2026-05-22-query-fixture", "validation", "--latest", repo_root=repo)
        payload = parse_json(result)

        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["code"], "no-validation-evidence")

    def test_validation_unknown_stage_reports_stable_diagnostic(self) -> None:
        repo = self.make_change("2026-05-22-query-fixture", self.compact_change_yaml())

        result = run_query(
            "2026-05-22-query-fixture",
            "validation",
            "--stage",
            "verify-r1",
            repo_root=repo,
        )
        payload = parse_json(result)

        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["code"], "stage-not-found")
        self.assertEqual(payload["stage"], "verify-r1")

    def test_unknown_change_and_unknown_subcommand_fail_with_json_diagnostics(self) -> None:
        repo = self.make_change("2026-05-22-query-fixture", self.compact_change_yaml())

        missing = run_query("2026-05-22-missing", "summary", repo_root=repo)
        missing_payload = parse_json(missing)
        bad_command = run_query("2026-05-22-query-fixture", "review", repo_root=repo)
        bad_payload = parse_json(bad_command)

        self.assertEqual(missing.returncode, 2)
        self.assertEqual(missing_payload["code"], "change-not-found")
        self.assertEqual(bad_command.returncode, 2)
        self.assertEqual(bad_payload["code"], "unsupported-query")

    def test_malformed_or_unsafe_metadata_fails_closed_without_modifying_files(self) -> None:
        repo = self.make_change(
            "2026-05-22-query-fixture",
            """change_id: 2026-05-22-query-fixture
artifacts:
  spec: /home/user/private.md
""",
        )
        before = sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*"))

        result = run_query("2026-05-22-query-fixture", "summary", repo_root=repo)
        payload = parse_json(result)
        after = sorted(path.relative_to(repo).as_posix() for path in repo.rglob("*"))

        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["code"], "unsupported-shape")
        self.assertEqual(before, after)

    def test_query_helper_does_not_execute_validation_bundle_commands(self) -> None:
        repo = self.make_change("2026-05-22-query-fixture", self.compact_change_yaml())
        marker = repo / "should-not-run.py"

        first = run_query("2026-05-22-query-fixture", "validation", "--latest", repo_root=repo)
        second = run_query("2026-05-22-query-fixture", "validation", "--latest", repo_root=repo)

        self.assertEqual(first.returncode, 0, msg=first.stderr)
        self.assertEqual(second.returncode, 0, msg=second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertFalse(marker.exists())

    def test_active_change_summary_command_runs(self) -> None:
        result = run_query(
            "2026-05-22-change-record-catalog-registration-and-bounded-read-model",
            "summary",
        )
        payload = parse_json(result)

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(
            payload["detail_pointers"]["change_metadata"],
            "docs/changes/2026-05-22-change-record-catalog-registration-and-bounded-read-model/change.yaml",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
