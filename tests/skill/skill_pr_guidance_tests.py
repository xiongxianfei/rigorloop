"""Pr guidance.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


class PRSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "pr"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.reference = (self.root / "references" / "governed-pr-readiness.md").read_text(encoding="utf-8")
        self.asset = (self.root / "assets" / "pr-body-skeleton.md").read_text(encoding="utf-8")
        self.verify_skill = (ROOT / "skills" / "verify" / "SKILL.md").read_text(encoding="utf-8")
        self.verify_reference = (ROOT / "skills" / "verify" / "references" / "branch-readiness-verification.md").read_text(encoding="utf-8")
        self.verify_explanation = (ROOT / "skills" / "verify" / "references" / "successful-explanation.md").read_text(encoding="utf-8")

    def test_package_inventory_and_resource_map_are_exact(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["governed-pr-readiness.md", "review-reliance.md"])
        self.assertEqual(sorted(path.name for path in (self.root / "assets").iterdir()), ["pr-body-skeleton.md"])
        self.assertIn("READ `references/governed-pr-readiness.md`", self.skill)
        self.assertIn("COPY `assets/pr-body-skeleton.md`", self.skill)
        for profile in ("PR0-portable", "PR1-governed"):
            self.assertIn(profile, self.skill)

    def test_closed_vocabularies_reject_unknown_values_first(self) -> None:
        vocabularies = {
            "governed signal": ("no-governed-signal", "single-governed-candidate", "invalid-or-ambiguous-governed-signal"),
            "submission intent": ("open", "draft", "prepare-only"),
            "refresh authority": ("none", "explicit-title-refresh", "explicit-full-replacement", "workflow-title-refresh"),
            "state-transition authority": ("none", "publish-existing-draft", "convert-existing-open-to-draft"),
            "branch relation": ("absent", "same", "remote-ancestor-of-local", "local-ancestor-of-remote", "diverged", "ambiguous"),
            "PR state": ("absent", "open", "draft", "closed", "merged", "ambiguous"),
            "operation result": ("opened", "draft-opened", "updated", "reused", "prepared-not-opened", "blocked"),
            "hosted-CI state": ("passed", "failed", "pending", "unavailable", "unobserved", "not-applicable"),
            "evidence suffix": ("none", "evidence-only", "invalidating"),
        }
        for name, allowed in vocabularies.items():
            with self.subTest(vocabulary=name):
                self.assertIn(name, self.skill)
                self.assertTrue(all(value in self.skill for value in allowed))
        self.assertIn("Unknown values fail before consistency checks", self.skill)

    def test_prepare_only_and_independent_authorities_have_closed_side_effects(self) -> None:
        for phrase in (
            "performs no push, PR creation, refresh, publication, draft conversion, or other external mutation",
            "Submission intent does not grant refresh or PR-state transition authority",
            "Default `open` preserves an existing draft",
            "Explicit `draft` preserves an existing open PR",
            "requested intent, actual operation, blocker, and actual mutation",
        ):
            self.assertIn(phrase, self.skill)

    def test_refresh_preserves_body_without_section_parser(self) -> None:
        for phrase in (
            "title replacement or explicitly authorized whole-body replacement",
            "must not parse or mutate Markdown sections",
            "body bytes remain unchanged",
            "hidden managed markers",
        ):
            self.assertIn(phrase.lower(), self.skill.lower())

    def test_directional_git_and_pr_state_are_fail_closed(self) -> None:
        for phrase in (
            "strict ancestor of the local handoff revision",
            "remote contains work absent locally",
            "must not force-push",
            "Closed, merged, multiple, mismatched, or ambiguous",
            "never create a duplicate matching PR",
        ):
            self.assertIn(phrase.lower(), self.skill.lower())

    def test_verify_owns_normalized_basis_and_legacy_is_preparation_only(self) -> None:
        combined = self.verify_skill + self.verify_reference
        for field in (
            "repository_identity", "remote_identity", "base_branch", "base_revision",
            "merge_base_revision", "head_branch", "verified_subject_revision",
        ):
            self.assertIn(field, combined)
            self.assertIn(field, self.skill)
        self.assertIn("verification_basis", combined)
        self.assertIn("Legacy, prose-only, command-only", self.skill)
        self.assertIn("preparation", self.skill)

    def test_evidence_suffix_external_sequence_and_readback_are_exact(self) -> None:
        for phrase in (
            "cumulative final change",
            "any commit count or direct-parent topology",
            "current attributable final-review, workflow, and Verify evidence",
            "path, file name, commit message, or author identity alone",
            "Immediately before push",
            "After push and before PR mutation",
            "Immediately before PR mutation",
            "After creation, reuse, refresh, or transition",
            "successful external write truthfully",
            "pr-open-ready: false",
        ):
            self.assertIn(phrase.lower(), self.skill.lower())
        self.assertNotIn("exactly one direct-child verify-owned evidence commit", self.skill)

    def test_unaffected_signal_retry_body_output_and_claim_contracts_are_preserved(self) -> None:
        for phrase in (
            "malformed, stale, conflicting, duplicated, unsafe, escaped, or ambiguous signals stop without portable fallback",
            "Retry reconciles state",
            "Procedure owns applicability and adequacy",
            "requested intent, operation, actual external mutation, actual PR state, readiness booleans, hosted-CI state, blockers, claim limitations, and post-read-back URL",
            "without current owning evidence",
        ):
            self.assertIn(phrase, self.skill)

    def test_evidence_suffix_rejects_protected_mixed_stale_and_cross_change_content(self) -> None:
        for phrase in (
            "implementation, tests, specifications, architecture, plans, dependencies, configuration",
            "generated product output",
            "public documentation",
            "another governed change",
            "mixed",
            "unknown",
            "stale",
            "non-ancestor",
        ):
            self.assertIn(phrase.lower(), (self.skill + self.reference).lower())


    def test_hosted_ci_result_and_claim_contracts_are_explicit(self) -> None:
        for phrase in (
            "current hosted evidence for the exact handoff revision at the PR head",
            "must never be described as passed",
            "requested intent", "actual external mutation", "actual PR state",
            "hosted-CI state", "claim limitations",
        ):
            self.assertIn(phrase.lower(), self.skill.lower())

    def test_governed_reference_is_bounded_and_read_only(self) -> None:
        for phrase in (
            "change pack", "plan", "review resolution", "historical rationale", "verify",
            "state-sync", "release-sensitive", "migration", "external completion",
            "read-only", "must not mutate",
        ):
            self.assertIn(phrase.lower(), self.reference.lower())
        self.assertNotIn("force-push", self.reference.lower())

    def test_body_asset_owns_structure_not_policy(self) -> None:
        for heading in (
            "## Summary", "## Why", "## What changed", "## Tests and verification",
            "## Risks and rollback", "## Reviewer notes", "## Follow-ups",
        ):
            self.assertEqual(self.asset.count(heading), 1)
        for heading in ("## Design and delivery basis", "## Requirement coverage", "## Review resolution summary", "## Lifecycle and verification evidence", "## Migration", "## Security and privacy", "## Release or operational impact"):
            self.assertEqual(self.asset.count(heading), 1)
        for forbidden in ("only when", "pr-open-ready", "branch-ready", "force-push"):
            self.assertNotIn(forbidden, self.asset.lower())

    def test_required_resources_and_lifecycle_claims_fail_closed(self) -> None:
        for phrase in (
            "missing, unreadable, escaped, stale, transformed, or mixed-version",
            "stop before governed readiness judgment",
            "stop before body generation and external mutation",
            "must not reconstruct",
            "must not mutate `change.json`",
            "no downstream continuation",
        ):
            self.assertIn(phrase.lower(), self.skill.lower())

    def test_review_resolution_summary_contract_is_preserved(self) -> None:
        for phrase in ("registered reviews", "owned dispositions", "blockers", "independent reassessment", "without duplicating every finding"):
            self.assertIn(phrase, self.skill)
