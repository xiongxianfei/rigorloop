"""Workflow parity and honest standalone timing diagnostics."""

from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_transaction import validate_release_timing_evidence, validate_release_workflow_parity
from release_fixture_helpers import (make_prepared_release, make_release_repo, valid_timing_text, write_timing)


class ReleaseGateParityAndTimingTests(unittest.TestCase):
    maxDiff = None

    def test_release_workflow_matches_current_coordination_contract(self) -> None:
        self.assertEqual(validate_release_workflow_parity(ROOT), [])

    def test_release_workflow_parity_rejects_direct_validate_release_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workflow = root / ".github" / "workflows" / "release.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text(
                "name: release\n"
                "jobs:\n"
                "  release:\n"
                "    steps:\n"
                "      - run: python scripts/validate-release.py --version \"$GITHUB_REF_NAME\"\n",
                encoding="utf-8",
            )

            errors = validate_release_workflow_parity(root)

        self.assertTrue(any("release-verify.sh" in error for error in errors), errors)
        self.assertTrue(any("validate-release.py" in error for error in errors), errors)

    def test_prepare_release_generates_timing_evidence_skeleton(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertEqual(result.errors, ())
        self.assertEqual(result.warnings, ())

    def test_release_timing_evidence_validates_required_phases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            write_timing(root, valid_timing_text())

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertEqual(result.errors, ())
        self.assertEqual(result.warnings, ())

    def test_release_timing_missing_when_profile_requires_it_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_release_repo(root)

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertTrue(any("timing.yaml" in error and "missing" in error for error in result.errors), result.errors)

    def test_release_timing_missing_duration_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            write_timing(root, valid_timing_text().replace("    duration_seconds: 12\n", ""))

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertTrue(any("preflight" in error and "duration_seconds" in error for error in result.errors), result.errors)

    def test_release_timing_unknown_phase_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            write_timing(root, valid_timing_text().replace("id: preflight", "id: fast_lane", 1))

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertTrue(any("unknown timing phase id: fast_lane" in error for error in result.errors), result.errors)

    def test_release_timing_unknown_result_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            write_timing(root, valid_timing_text().replace("result: pass", "result: done", 1))

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertTrue(any("unknown timing result: done" in error for error in result.errors), result.errors)

    def test_release_timing_duration_over_target_is_warning_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_prepared_release(root)
            write_timing(root, valid_timing_text(preflight_duration=999))

            result = validate_release_timing_evidence("v0.3.5", root=root)

        self.assertEqual(result.errors, ())
        self.assertTrue(any("preflight" in warning and "target" in warning for warning in result.warnings), result.warnings)
