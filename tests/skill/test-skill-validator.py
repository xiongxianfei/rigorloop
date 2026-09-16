"""Supported aggregate for all Skill validation and guidance tests.

Behavior groups remain individually addressable through this script."""
from __future__ import annotations

import re
import shutil
import subprocess
import unittest
from unittest import mock
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation
from skill_cli_tests import run_validator
from skill_metadata_tests import SkillMetadataTests
from skill_resource_tests import SkillResourceMapTests
from skill_asset_tests import SkillAssetContractTests
from skill_ci_contract_tests import CiMaintenanceInputTests
from skill_canonical_tests import CanonicalSkillGuidanceTests
from skill_portability_tests import SkillPortabilityTests
from skill_project_map_tests import ProjectMapInputTests
from skill_placement_tests import InstalledSkillPlacementTests
from skill_cli_tests import SkillCliTests
from skill_guidance_tests import SkillGuidanceTests, ExplicitRecordingGuidanceTests
from skill_contract_tests import RecordingReferenceContractTests, RelocatedPlanSurfaceTests, CiAssemblyDeclarationTests


class MarkdownReadabilityGuidanceTests(unittest.TestCase):
    def test_generated_markdown_skeletons_declare_readability_shape(self) -> None:
        skeletons = [
            ROOT / "skills" / "proposal" / "assets" / "proposal-skeleton.md",
            ROOT / "skills" / "design" / "assets" / "design-skeleton.md",
            ROOT / "skills" / "plan" / "assets" / "plan-skeleton.md",
        ]
        required_terms = [
            "Readability contract:",
            "normal prose paragraphs",
            "complete sentences",
            "stable IDs",
            "tables",
        ]

        for skeleton in skeletons:
            text = skeleton.read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skeleton=skeleton, term=term):
                    self.assertIn(term, text)

    def test_generated_markdown_skills_include_readability_guidance(self) -> None:
        skill_paths = [
            ROOT / "skills" / "proposal" / "SKILL.md",
            ROOT / "skills" / "design" / "SKILL.md",
            ROOT / "skills" / "plan" / "SKILL.md",
            ROOT / "skills" / "code-review" / "SKILL.md",
            ROOT / "skills" / "verify" / "SKILL.md",
        ]
        required_terms = [
            "## Generated Markdown readability",
            "normal Markdown paragraphs",
            "Do not split a sentence across physical source lines",
            "stable IDs",
            "Do not require manual-proof contracts",
        ]

        for skill_path in skill_paths:
            text = skill_path.read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skill=skill_path, term=term):
                    self.assertIn(term, text)

            if skill_path.parent.name == "design":
                self.assertIn("Living models require the overview and every supporting view judged necessary", text)
                self.assertIn("other diagrams are optional", text)
            else:
                self.assertIn("Diagrams are optional", text)

            with self.subTest(skill=skill_path, term="legacy clause-per-line guidance"):
                self.assertNotIn("one sentence or natural clause per source line", text)

    def test_implementation_markdown_guidance_keeps_sentences_intact(self) -> None:
        skill_path = ROOT / "skills" / "implement" / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")

        self.assertIn("normal Markdown paragraphs", text)
        self.assertIn("Do not split a sentence across physical source lines", text)
        self.assertNotIn("use semantic source lines", text)

    def test_canonical_skill_prose_has_no_suspected_sentence_splits(self) -> None:
        skill_paths = sorted((ROOT / "skills").glob("*/SKILL.md"))
        command = [
            sys.executable,
            str(ROOT / "scripts" / "validate-documentation-prose.py"),
            "--mode",
            "audit",
        ]
        for skill_path in skill_paths:
            command.extend(("--path", str(skill_path.relative_to(ROOT))))

        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            f"documentation prose validation: errors=0 warnings=0 paths={len(skill_paths)}\n",
            result.stdout,
        )


class RetainedSkillAuthorityTests(unittest.TestCase):
    # These checks protect current actor/asset boundaries or separately retained
    # optional automation methods; they are not legacy record acceptance.
    DOWNSTREAM_READ_ONLY_PHRASES = {
        "implement": "Do not update the plan, upstream artifacts, artifact settlement, or workflow",
        "code-review": "It must not edit implementation, the plan, artifact settlement, milestone",
        "verify": "plan and upstream artifacts as read-only",
        "pr": "upstream artifacts as read-only",
    }


    def test_downstream_skills_keep_upstream_surfaces_read_only(self) -> None:
        for skill_name, phrase in self.DOWNSTREAM_READ_ONLY_PHRASES.items():
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            with self.subTest(skill=skill_name):
                self.assertIn(phrase, body)


    def test_authoring_skills_do_not_claim_review_settlement(self) -> None:
        for skill_name in ("proposal", "design", "plan"):
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            with self.subTest(skill=skill_name):
                self.assertNotIn("self-approve", body.lower())
                self.assertNotRegex(
                    body,
                    r"(?i)(authoring skill|this skill).{0,60}(approve|accept).{0,40}(its|the) (proposal|spec|architecture|plan|test spec)",
                )


    def test_governed_artifact_assets_do_not_emit_mutable_status(self) -> None:
        asset_paths = [
            ROOT / "skills" / "proposal" / "assets" / "proposal-skeleton.md",
            ROOT / "skills" / "design" / "assets" / "design-skeleton.md",
            ROOT / "skills" / "plan" / "assets" / "plan-skeleton.md",
        ]
        forbidden = (
            "## Status",
            "Current milestone:",
            "Review status:",
            "Next stage:",
            "Final closeout readiness:",
        )
        for asset_path in asset_paths:
            text = asset_path.read_text(encoding="utf-8")
            for phrase in forbidden:
                with self.subTest(asset=asset_path, phrase=phrase):
                    self.assertNotIn(phrase, text)


    def test_route_uses_one_target_and_evidence_first_recovery(self) -> None:
        body = (
            ROOT
            / "skills"
            / "route"
            / "references"
            / "bounded-workflow-automation.md"
        ).read_text(encoding="utf-8")
        required = (
            "one target-driven",
            "The requested target is the complete automation boundary.",
            "`$route auto: status` is read-only.",
            "`$route auto: off` durably cancels",
            "Resume uses tracked artifact and review evidence.",
            "Direct review invocations do not activate, resume, or advance automation",
            "verify failure",
            "never opens a PR",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, body)
        for retired in ("active profile", "writable profile", "selector ledger"):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, body.lower())


class RouteSkillCutoverContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "route"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")

    def test_route_maps_only_routing_conditional_resources(self) -> None:
        expected = {
            "references/governed-lifecycle-routing.md": "READ",
            "references/bounded-workflow-automation.md": "READ",
            "references/boundary-first-method-v1.md": "READ",
        }
        for relative_path, verb in expected.items():
            with self.subTest(resource=relative_path):
                self.assertTrue((self.root / relative_path).is_file())
                self.assertIn(f"- {verb} `{relative_path}`", self.skill)

        self.assertFalse((self.root / "references/workflow-guide-authoring.md").exists())
        self.assertFalse((self.root / "assets/workflows-skeleton.md").exists())

    def test_route_declares_exact_predicates_and_assemblies(self) -> None:
        for predicate in (
            "governed_change_context",
            "automation_command_context",
            "armed_automation_context",
        ):
            self.assertIn(predicate, self.skill)
        self.assertNotIn("workflow_guide_authoring_context", self.skill)
        for assembly in (
            "WP0-generic-routing",
            "WP1-governed",
            "WP2-governed-automated",
            "WPB-automation-bootstrap",
            "WPS-stateless-automation-command",
        ):
            self.assertIn(assembly, self.skill)
        self.assertNotIn("WP3-guide-authoring", self.skill)
        self.assertNotIn("WP4-governed-guide-authoring", self.skill)

    def test_route_keeps_universal_stops_inline(self) -> None:
        for phrase in (
            "Conversational wording alone does not establish",
            "Unknown artifact types and unknown lifecycle stages are blockers",
            "Every predicate combination must match exactly one assembly row",
            "After classification and before resource-dependent interpretation or action",
            "contradiction among packaged resources",
            "stop rather than invent, recall, or partially reconstruct",
        ):
            self.assertIn(phrase, self.skill)

    def test_route_references_have_non_overlapping_owners(self) -> None:
        governed = (self.root / "references" / "governed-lifecycle-routing.md").read_text(encoding="utf-8")
        automation = (self.root / "references" / "bounded-workflow-automation.md").read_text(encoding="utf-8")
        self.assertIn("reviewed stable plan", governed)
        self.assertNotIn("architecture-required", governed)
        self.assertNotIn("architecture-not-required", governed)
        self.assertNotIn("architecture-ambiguous", governed)
        self.assertIn("Actor-owned updates", governed)
        self.assertIn("asks governed lifecycle procedure", automation)
        self.assertIn("must not redefine stage order", automation)

    def test_route_bootstrap_and_stateless_paths_are_explicit(self) -> None:
        automation = (self.root / "references" / "bounded-workflow-automation.md").read_text(encoding="utf-8")
        bootstrap_steps = (
            "Recognize the explicit target command",
            "Load bounded workflow automation procedure",
            "Resolve or create governed change identity",
            "Validate the governed record",
            "Reclassify as governed",
            "Load governed lifecycle procedure",
            "Only then persist authorization",
        )
        positions = [automation.index(step) for step in bootstrap_steps]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("no-active-run", automation)
        self.assertIn("creates no governed or automation state", automation)

    def test_route_consumes_cli_context_and_preserves_protocol_authority(self) -> None:
        self.assertIn("rigorloop workflow-context", self.skill)
        self.assertIn("Route owns explicit activity", self.skill)
        self.assertIn("targeted", self.skill)
        self.assertNotIn("docs/workflows.md", self.skill)

    def test_current_skill_validator_has_no_retired_guide_parser(self) -> None:
        validator = (ROOT / "scripts/lib/validation" / "skill_validation.py").read_text(encoding="utf-8")
        for retired in (
            "def validate_workflow_artifact_map_lookup",
            "def validate_workflow_artifact_map_contract",
            "def validate_workflow_guide_skeleton_contract",
            "WORKFLOW_GUIDE_SKELETON_REQUIRED_METADATA",
            "WORKFLOW_ARTIFACT_REQUIRED_REGISTRY_ENTRIES",
        ):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, validator)


class VerifySkillSimplificationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "verify"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")

    def test_verify_simplification_maps_exact_resources(self) -> None:
        for relative_path in (
            "references/boundary-first-method-v1.md",
            "references/branch-readiness-verification.md",
        ):
            self.assertTrue((self.root / relative_path).is_file())
            self.assertIn(f"- READ `{relative_path}`", self.skill)

    def test_verify_simplification_declares_closed_outcomes_profiles_and_modes(self) -> None:
        for value in ("scoped-verification", "branch-readiness", "workflow-final-verification"):
            self.assertIn(value, self.skill)
        for value in ("VP0-scoped", "VP0B-scoped-boundary", "VP1-final-readiness", "VP1B-final-readiness-boundary"):
            self.assertIn(value, self.skill)
        for value in ("isolated", "governed-final"):
            self.assertIn(value, self.skill)

    def test_verify_simplification_keeps_item_evidence_and_claim_safety_inline(self) -> None:
        for phrase in (
            "passed`, `failed`, `skipped`, `pending`, `not-run`, and `unknown",
            "configured command is not an actual run",
            "local validation is not observed hosted CI",
            "current from stale evidence",
            "generated-output currency",
            "manual proof",
            "branch-ready",
            "pr-body-ready",
            "pr-open-ready",
        ):
            self.assertIn(phrase, self.skill)

    def test_verify_simplification_reference_owns_aggregation_not_item_meaning(self) -> None:
        reference = (self.root / "references" / "branch-readiness-verification.md").read_text(encoding="utf-8")
        for phrase in ("Final-readiness prerequisites", "Final evidence composition", "blocker aggregation", "Verdict and completion"):
            self.assertIn(phrase, reference)
        for forbidden in ("defines the meaning of `passed`", "owns workflow stage order", "authorizes `pr`"):
            self.assertNotIn(forbidden, reference)

    def test_verify_simplification_fails_safe_on_missing_triggered_resource(self) -> None:
        for phrase in (
            "missing or unreadable triggered reference",
            "stop before dependent interpretation, verdict, recording, or handoff",
            "must not reconstruct",
            "untriggered reference does not load",
        ):
            self.assertIn(phrase, self.skill)


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


class PlanSkillSimplificationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "plan"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.reference = (
            self.root / "references" / "governed-plan-authoring.md"
        ).read_text(encoding="utf-8")
        self.change_root = (
            ROOT / "docs" / "changes" / "2026-08-12-plan-skill-simplification"
        )


    def test_plan_simplification_package_and_profiles_are_closed(self) -> None:
        self.assertEqual(
            sorted(path.name for path in (self.root / "assets").iterdir()),
            ["decision-log-row.md", "milestone.md", "plan-skeleton.md"],
        )
        self.assertIn("references/governed-plan-authoring.md", self.skill)
        self.assertIn("references/boundary-first-method-v1.md", self.skill)
        for operation in (
            "create-primary-plan",
            "revise-primary-plan",
            "initialize-approved-plan",
        ):
            self.assertIn(operation, self.skill)
        self.assertIn("change link", self.reference)
        self.assertIn("Conversational wording", self.skill)
        self.assertIn("does not establish governed authority", self.skill)

    def test_plan_simplification_governed_reference_owns_only_governed_procedure(self) -> None:
        for phrase in ("approved Delivery Review package", "change link", "Never initialize an unreviewed draft", "route owns subsequent work decisions", "exactly once"):
            self.assertIn(phrase, self.reference)
        self.assertNotIn("record-artifact-revision", self.reference)

    def test_plan_simplification_assets_are_stable_intent_only(self) -> None:
        milestone = (self.root / "assets" / "milestone.md").read_text(
            encoding="utf-8"
        )
        for required in (
            "Milestone kind",
            "Completion criteria",
            "Required evidence",
            "Review handoff",
            "Rollback/recovery",
        ):
            self.assertIn(required, milestone)
        for forbidden in (
            "Milestone state:",
            "validation passed",
            "progress updated",
            "milestone committed",
        ):
            self.assertNotIn(forbidden, milestone)


class ProposalSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "proposal"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        governed_path = self.root / "references" / "governed-proposal-authoring.md"
        strategic_path = self.root / "references" / "strategic-and-scope-gates.md"
        self.governed = governed_path.read_text(encoding="utf-8") if governed_path.is_file() else ""
        self.strategic = strategic_path.read_text(encoding="utf-8") if strategic_path.is_file() else ""
        self.skeleton = (self.root / "assets" / "proposal-skeleton.md").read_text(encoding="utf-8")

    def test_package_assemblies_and_resource_ownership_are_closed(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["governed-proposal-authoring.md", "requirement-to-delivery-model.md", "strategic-and-scope-gates.md"])
        for assembly in ("PA0-portable", "PA0G-portable-gated", "PA1-governed", "PA1G-governed-gated"):
            self.assertIn(assembly, self.skill)
        self.assertIn("READ `references/governed-proposal-authoring.md`", self.skill)
        self.assertIn("READ `references/strategic-and-scope-gates.md`", self.skill)
        self.assertIn("COPY `assets/proposal-skeleton.md`", self.skill)
        self.assertIn("must not reconstruct", self.skill.lower())

    def test_portable_and_governed_operation_authority_is_separate(self) -> None:
        for operation in ("create-primary-proposal", "revise-primary-proposal"):
            self.assertIn(operation, self.skill)
        self.assertIn("change link", self.governed)
        for phrase in (
            "governed_proposal_candidate_context",
            "Conversational wording alone does not establish",
            "does not grant mutation authority",
            "must not fall back to portable",
            "Portable authoring writes only the proposal artifact",
        ):
            self.assertIn(phrase.lower(), self.skill.lower())
        for phrase in ("review readiness", "Conflict requires rereading", "downstream reliance", "prior subject identities"):
            self.assertIn(phrase.lower(), self.governed.lower())

    def test_governed_retry_and_authorized_reset_fail_closed(self) -> None:
        for phrase in ("Conflict requires rereading and reassessment", "stop on ambiguous outcome", "Preserve partial evidence", "Do not settle review"):
            self.assertIn(phrase, self.governed)

    def test_specialized_predicates_and_scope_budget_vocabulary_are_closed(self) -> None:
        for predicate in ("vision_exception_context", "standing_artifact_context", "initial_intent_table_context", "scope_budget_context"):
            self.assertIn(predicate, self.skill)
            self.assertIn(predicate, self.strategic)
        self.assertIn("semantic proposal judgment", self.skill.lower())
        self.assertIn("loads exactly once", self.skill.lower())
        for value in ("in scope", "out of scope", "deferred follow-up", "rejected option", "open question", "core to this proposal", "first-slice candidate", "same-slice dependency", "separate implementation slice", "deferable follow-up", "separate proposal"):
            self.assertIn(value, self.strategic)

    def test_skeleton_owns_exact_direction_sections_and_one_conditional_section(self) -> None:
        headings = [
            line.removeprefix("## ")
            for line in self.skeleton.splitlines()
            if line.startswith("## ")
        ]
        self.assertEqual(
            headings,
            [
                "Challenge",
                "Goals",
                "Scope and non-goals",
                "Governing principle",
                "Proposed direction",
                "Feasibility",
                "Impact and major trade-offs",
                "Decision requested",
            ],
        )
        self.assertIn("otherwise omit this section", self.skeleton)
        self.assertIn("Omit the material-impact section when it is not needed", self.skill)
        self.assertIn("inside an allowed section", self.skill)

    def test_references_have_non_overlapping_policy_owners(self) -> None:
        self.assertIn("governed proposal authoring", self.governed.lower())
        self.assertIn("strategic and scope gates", self.strategic.lower())
        self.assertNotIn("scope budget treatment", self.governed.lower())
        self.assertNotIn("change.yaml", self.strategic)
        self.assertNotIn("review-required", self.strategic)


class UnifiedDesignResourceTests(unittest.TestCase):
    def test_retired_standalone_resources_are_absent_and_cannot_be_reintroduced(self):
        retired = ("assets/legacy-architecture-skeleton.md", "assets/legacy-adr-skeleton.md",
                   "references/legacy-technical-authoring.md")
        for resource in retired:
            with self.subTest(resource=resource), tempfile.TemporaryDirectory() as tmp:
                source = ROOT / "skills/design"
                self.assertFalse((source / resource).exists())
                root = Path(tmp) / "design"
                shutil.copytree(source, root)
                (root / resource).write_text("# Retired standalone output resource\n")
                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unknown design resource: " + resource, result.stdout + result.stderr)
        for name in ("architecture.md", "adr.md"):
            self.assertFalse((ROOT / "templates" / name).exists())

    def test_unknown_design_resource_precedes_missing_resource_consistency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "design"
            shutil.copytree(ROOT / "skills/design", root)
            (root / "references/unrecognized.md").write_text("# Unexpected resource\n")
            (root / "references/technical-design.md").unlink()
            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            output = result.stdout + result.stderr
            self.assertLess(output.index("unknown design resource: references/unrecognized.md"),
                            output.index("required design resource missing: references/technical-design.md"))

    def test_complete_package_and_retired_names(self):
        root = ROOT / "skills/design"
        self.assertFalse((ROOT / "skills/spec").exists())
        self.assertFalse((ROOT / "skills/architecture").exists())
        self.assertEqual(run_validator(root).returncode, 0)
        from lib.validation.skill_validation import DESIGN_RESOURCES
        self.assertEqual({p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}, {"SKILL.md", *DESIGN_RESOURCES})

    def test_missing_each_conditional_design_resource_rejects(self):
        from lib.validation.skill_validation import DESIGN_RESOURCES
        for resource in DESIGN_RESOURCES:
            with self.subTest(resource=resource), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "design"
                shutil.copytree(ROOT / "skills/design", root)
                (root / resource).unlink()
                self.assertNotEqual(run_validator(root).returncode, 0)

    def test_unknown_value_design_resource_rejects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "design"
            shutil.copytree(ROOT / "skills/design", root)
            (root / "references/unknown_value.md").write_text("unexpected resource")
            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown", (result.stdout + result.stderr).lower())

    def test_legacy_boundary_projection_keeps_complete_format(self):
        root = ROOT / "skills/design/references"
        for name in ("boundary-first-method-v1.md", "boundary-first-feature-authoring-v1.md"):
            self.assertEqual((root / name).read_bytes(), (ROOT / "templates/shared" / name).read_bytes())
        body = (root / "boundary-first-feature-authoring-v1.md").read_text()
        headings = ("## Boundary model", "## Boundary definitions", "## Selected interactions", "## Example ownership")
        positions = [body.index(h) for h in headings]
        self.assertEqual(positions, sorted(positions))

    def test_governed_recording_stays_conditional_and_readable(self):
        root = ROOT / "skills/design"
        body = (root / "SKILL.md").read_text()
        self.assertIn("do not fall back to portable mode", body)
        self.assertIn("when one valid governed change", body)
        ref = (root / "references/governed-design-authoring.md").read_text()
        self.assertIn("expected_revision", ref)
        self.assertIn("Do not migrate", ref)
        self.assertIn("does not approve", ref)
        self.assertNotIn("record-store check|record", ref)


class VisionSkillProgressiveDisclosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "vision"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.strategic = (self.root / "references" / "strategic-vision-authoring.md").read_text(encoding="utf-8")
        self.readme = (self.root / "references" / "readme-vision-sync.md").read_text(encoding="utf-8")
        self.vision_asset = (self.root / "assets" / "vision-skeleton.md").read_text(encoding="utf-8")
        self.positioning_asset = (self.root / "assets" / "strategic-positioning-skeleton.md").read_text(encoding="utf-8")
        self.package = "\n".join((self.skill, self.strategic, self.readme))

    def test_package_inventory_resource_verbs_and_six_assemblies_are_exact(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["readme-vision-sync.md", "strategic-vision-authoring.md"])
        self.assertEqual(sorted(path.name for path in (self.root / "assets").iterdir()), ["strategic-positioning-skeleton.md", "vision-skeleton.md"])
        self.assertFalse(any(path.suffix == ".py" for path in self.root.rglob("*")))
        for mapping in ("READ `references/strategic-vision-authoring.md`", "READ `references/readme-vision-sync.md`", "COPY `assets/vision-skeleton.md`", "COPY `assets/strategic-positioning-skeleton.md`"):
            self.assertIn(mapping, self.skill)
        rows = [line for line in self.skill.splitlines() if line.startswith("| `VA")]
        for assembly in ("VA0-readme-sync", "VA0S-readme-skip", "VA1-editorial-sync", "VA1S-editorial-skip", "VA2-strategic-sync", "VA2S-strategic-skip"):
            self.assertEqual(sum(assembly in row for row in rows), 1)

    def test_universal_operations_actions_authority_and_claims_remain_inline(self) -> None:
        for value in ("establish-vision", "revise-vision", "sync-readme", "editorial", "substantive-nonmaterial", "material-repositioning", "synchronize-existing", "insert-and-synchronize", "full-rewrite", "partial-retry-required", "blocked-before-write"):
            self.assertIn(value, self.skill)
        for phrase in ("`CONSTITUTION.md` outranks `VISION.md`", "`VISION.md` is canonical", "only supported project-vision artifact", "loading a reference or copying an asset never grants", "privacy", "stop before", "do not claim", "does not hand off automatically"):
            self.assertIn(phrase.lower(), self.skill.lower())
        self.assertNotIn("## Modes", self.skill)

    def test_references_have_distinct_procedure_and_no_authority_grant(self) -> None:
        for phrase in ("project category", "primary user", "primary pain", "primary promise", "core mechanism", "alternatives", "tradeoff", "compatibility surfaces", "refusals", "falsifiability", "MUST NOT exceed 900 words", "methodology-as-product"):
            self.assertIn(phrase.lower(), self.strategic.lower())
        for phrase in ("<!-- vision:start -->", "<!-- vision:end -->", "first H1 block", "preserve every byte outside", "derived", "idempot"):
            self.assertIn(phrase.lower(), self.readme.lower())
        for reference in (self.strategic, self.readme):
            self.assertIn("parent skill owns", reference.lower())
            self.assertNotIn("grants authority", reference.lower())

    def test_assets_are_structural_complete_and_policy_free(self) -> None:
        for heading in ("## Pitch", "## What makes this different", "## Who it is for", "## Who it is not for", "## What it commits to", "## What it refuses to be", "## What would prove this wrong"):
            self.assertIn(heading, self.vision_asset)
        for heading in ("## Project category", "## Primary user", "## Primary pain", "## Primary promise", "## Core mechanism", "## Alternatives", "## Tradeoff", "## Compatibility surfaces", "## Refusals", "## Falsifiability"):
            self.assertIn(heading, self.positioning_asset)
        self.assertIn("does not independently override it", self.positioning_asset)
        for asset in (self.vision_asset, self.positioning_asset):
            for forbidden in ("authority is", "lifecycle", "review status", "marker parsing", "word limit"):
                self.assertNotIn(forbidden, asset.lower())

    def test_skip_manifest_write_order_retry_and_resource_failures_are_closed(self) -> None:
        for phrase in ("not-evaluated-under-exact-skip", "equal prior and intended identities", "authorized change-local authoring evidence before its first target write", "otherwise stop and require Design before planning", "zero-write skip has no changed files", "claims neither synchronization nor marker validity", "write source-first", "immediately before README", "read-back of every required", "committed and pending targets", "portable cross-session recovery", "missing, unreadable, escaped, stale, contradictory, or mixed-version", "do not reconstruct"):
            self.assertIn(phrase.lower(), self.skill.lower())
        for claim in ("review approval", "implementation", "validation", "verification", "branch readiness", "PR readiness", "release", "deployment"):
            self.assertIn(claim.lower(), self.skill.lower())


class ExplainChangeSkillRetirementTests(unittest.TestCase):
    def test_standalone_skill_is_absent_and_verify_owns_explanation(self) -> None:
        self.assertFalse((ROOT / "skills" / "explain-change").exists())
        verify = (ROOT / "skills" / "verify" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("final durable explanation", verify)
        manifest = (ROOT / "dist" / "adapters" / "manifest.yaml").read_text(encoding="utf-8")
        self.assertNotIn("name: explain-change", manifest)
class LearnSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "learn"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.method = (self.root / "references" / "session-method.md").read_text(encoding="utf-8")
        self.package = self.skill + "\n" + self.method

    def test_package_profiles_and_resource_trigger_are_exact(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["session-method.md"])
        self.assertFalse((self.root / "assets").exists())
        self.assertIn("LR0-route-result", self.skill)
        self.assertIn("LR1-session", self.skill)
        self.assertIn("READ `references/session-method.md`", self.skill)
        self.assertIn("exactly for `run-learn-session`", self.skill)
        self.assertIn("at most once", self.skill)

    def test_operations_authority_and_resource_failures_are_closed(self) -> None:
        for value in ("run-learn-session", "record-learn-route-result"):
            self.assertIn(value, self.skill)
        self.assertNotIn("assess-learn-trigger` operation", self.skill)
        for phrase in ("unknown, missing, combined, or ambiguous", "contributor confirmation", "destination mutation", "workflow continuation", "missing, unreadable, escaped, stale, contradictory, or mixed-version", "must not reconstruct"):
            self.assertIn(phrase.lower(), self.skill.lower())
        for phrase in ("unless the request explicitly identifies", "before session creation"):
            self.assertIn(phrase.lower(), self.skill.lower())
        self.assertNotIn("$learn", self.skill)

    def test_session_paths_interruption_and_confirmation_fail_closed(self) -> None:
        for phrase in ("lowest available suffix", "recheck absence", "complete `Frame`", "must not resume, repair, adopt, or overwrite", "same complete session", "new unique path", "pending", "confirmed", "rejected"):
            self.assertIn(phrase.lower(), self.package.lower())
        for phrase in ("session identity", "evidence-basis identity", "recorded evidence", "bounded inference", "unknowns", "sensitive or excluded evidence", "conflicting or ambiguous topic content"):
            self.assertIn(phrase.lower(), self.method.lower())

    def test_routes_and_result_recording_have_narrow_ownership(self) -> None:
        for value in ("ROUTE-NNN", "pending-owner-action", "complete", "blocked", "authoritative-artifact", "durable-scheduled-follow-up"):
            self.assertIn(value, self.package)
        for phrase in ("only the matching route", "exact owner-result identity", "idempotent success", "must not poll", "must not mutate the destination", "historical sessions"):
            self.assertIn(phrase.lower(), self.package.lower())
        for field in ("source observation", "confirmed classification", "requested action", "destination kind", "owning skill or process", "evidence-basis identity", "required completion kind", "settlement", "optional owner-result identity", "optional blocker"):
            self.assertIn(field.lower(), self.method.lower())
        for phrase in ("fixed when the route is created", "must match the route's immutable required completion kind"):
            self.assertIn(phrase.lower(), self.package.lower())

    def test_compact_result_and_claim_limits_are_complete(self) -> None:
        for phrase in ("operation", "session identity and path", "trigger and scope", "confirmation result", "session recording result", "topic effects", "route IDs and settlements", "owner-result identities", "blockers", "next owner or handoff", "claim limitations"):
            self.assertIn(phrase.lower(), self.skill.lower())
        for claim in ("destination approval", "implementation", "release", "workflow completion", "verification", "branch readiness", "PR readiness"):
            self.assertIn(claim.lower(), self.skill.lower())


class ProjectMapSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "project-map"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.reference_path = self.root / "references" / "map-maintenance-and-area-coordination.md"
        self.reference = self.reference_path.read_text(encoding="utf-8") if self.reference_path.is_file() else ""

    def test_package_and_loaded_assemblies_are_closed(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "assets").iterdir()), ["project-map-skeleton.md"])
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["map-maintenance-and-area-coordination.md"])
        for value in ("PMA0-simple-root-create", "PMA1-maintenance-or-coordinated"):
            self.assertIn(value, self.skill)
        self.assertIn("READ `references/map-maintenance-and-area-coordination.md`", self.skill)
        self.assertIn("COPY `assets/project-map-skeleton.md`", self.skill)
        self.assertIn("Late coordination discovery", self.skill)

    def test_operation_scope_and_target_state_contract_is_closed(self) -> None:
        for value in ("`create`", "`refresh`", "`audit`", "`repository`", "`area:<slug>`"):
            self.assertIn(value, self.skill)
        for phrase in (
            "applies only when the resolved target is absent",
            "applies only when the resolved target exists",
            "complete rewrite of an existing map is a refresh",
            "is always read-only",
            "missing-map",
            "new refresh operation",
        ):
            self.assertIn(phrase, self.skill.lower())
        self.assertIn("Operation: <create | refresh | audit>", self.skill)
        self.assertIn("Map scope: <repository | area:<slug>>", self.skill)
        self.assertNotIn("Mode: <", self.skill)

    def test_coordination_preflight_is_bounded_and_fail_closed(self) -> None:
        for phrase in (
            "project-local workflow guidance",
            "root-map path",
            "area-map directory",
            "root registration",
            "area-map files",
            "request-supplied coordination evidence",
            "active change context",
            "must not broadly scan the repository merely to prove absence",
            "unavailable, conflicting, or ambiguous",
        ):
            self.assertIn(phrase, self.skill.lower())

    def test_universal_evidence_and_reliance_rules_remain_inline(self) -> None:
        for phrase in (
            "observed",
            "inferred",
            "unknown",
            "current",
            "partial",
            "stale",
            "configured command",
            "executed command",
            "<sha>+dirty",
            "source and runtime configuration",
            "must inspect source directly",
        ):
            self.assertIn(phrase, self.skill.lower())

    def test_conditional_reference_owns_maintenance_and_area_transaction(self) -> None:
        for phrase in (
            "refresh trigger comparison",
            "affected-section selection",
            "correction note",
            "audit procedure",
            "root registration",
            "overlap ownership",
            "previous and current baseline",
            "write the area map first",
            "registration last",
            "transaction commit point",
            "idempotent success",
            "must not adopt",
        ):
            self.assertIn(phrase, self.reference.lower())

    def test_required_resource_failure_stops_without_reconstruction(self) -> None:
        for phrase in (
            "missing",
            "unreadable",
            "escaped",
            "contradictory",
            "mixed-version",
            "stop",
            "must not reconstruct",
        ):
            self.assertIn(phrase, self.skill.lower())


class CiMaintenanceSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "docs" / "changes" / "2026-08-19-ci-maintenance-skill-simplification"
        self.skill_dir = ROOT / "skills" / "ci-maintenance"


    def test_package_split_and_closed_axes_are_present(self) -> None:
        skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        reference = (self.skill_dir / "references" / "github-workflow-authoring.md").read_text(encoding="utf-8")
        for value in (
            "create",
            "revise",
            "review",
            "invalid-or-ambiguous-target",
            "CIM8",
            "bounded-pr-ci-repair",
            "not-observed",
            "pending",
            "passed",
            "failed",
        ):
            self.assertIn(value, skill)
        self.assertIn("serializes", reference)
        self.assertIn("MUST NOT independently choose", reference)

    def test_minimal_skeleton_omits_privileged_and_boundary_examples(self) -> None:
        skeleton = (self.skill_dir / "assets" / "github-workflow-skeleton.yml").read_text(encoding="utf-8")
        for forbidden in ("pull_request:", "push:", "schedule:", "workflow_dispatch:", "pull_request_target", "secrets:", "id-token:"):
            self.assertNotIn(forbidden, skeleton)
        self.assertIn("permissions:\n  contents: read", skeleton)

    def test_risk_map_owns_semantic_placement(self) -> None:
        risk_map = (self.skill_dir / "references" / "risk-to-check-map.md").read_text(encoding="utf-8")
        self.assertIn("sole semantic owner", risk_map)
        self.assertIn("required execution boundary", risk_map)


    def test_write_and_batch_safety_guidance_is_present(self) -> None:
        skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for phrase in ("Create uses commit-time atomic no-clobber", "Revise replaces only while identity matches", "Providers precede wrappers", "Unsafe states or cycles return `blocked-before-write`"):
            self.assertIn(phrase, skill)

    def test_partial_batch_and_retry_are_exact(self) -> None:
        skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for phrase in ("partial-blocked", "completed and pending targets", "Retry rebuilds the entire graph", "adopts no stale manifest"):
            self.assertIn(phrase, skill)


class BugfixSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "docs" / "changes" / "2026-08-20-bugfix-skill-simplification"
        self.skill_dir = ROOT / "skills" / "bugfix"
        self.skill = (self.skill_dir / "SKILL.md").read_text(encoding="utf-8")


    def test_bugfix_package_keeps_supported_resources_and_complete_behavior(self):
        files = sorted(path.relative_to(self.skill_dir).as_posix() for path in self.skill_dir.rglob("*") if path.is_file())
        self.assertEqual(files, ["SKILL.md", "references/test-maintenance.md", "references/test-quality.md"])
        self.assertIn("Keep required behavior complete", self.skill)
        self.assertNotIn("Report before/after LF-normalized words", self.skill)

    def test_meaningful_legacy_rules_remain_executable(self) -> None:
        for phrase in (
            "unexpected behavior, failing evidence, incident, regression, or bug report",
            "governing behavior, current code and tests, available bug evidence",
            "smallest reliable reproduction",
            "Assess blast radius and inspect nearby code for the same pattern",
            "Fix the supported root cause with the smallest scoped change",
            "Do not refactor unrelated code",
        ):
            self.assertIn(phrase, self.skill)

    def test_evidence_vocabularies_and_proof_table_are_complete(self) -> None:
        for value in (
            "reproduced",
            "not-established",
            "settled",
            "resolvable-restoration",
            "behavior-change-request",
            "feasible",
            "infeasible-with-rationale",
            "unresolved",
            "failing-automated-test",
            "deterministic-alternative",
            "missing",
            "conflicting",
            "supported",
            "uncertain",
        ):
            self.assertIn(value, self.skill)
        for required_row in (
            "Any recognized | failing-automated-test | apply-production-correction",
            "Any recognized | conflicting | stop-blocked",
            "feasible | missing or deterministic-alternative | author-automated-proof",
            "unresolved | missing or deterministic-alternative | resolve-test-feasibility",
            "infeasible-with-rationale | complete deterministic-alternative | apply-production-correction",
            "infeasible-with-rationale | missing | stop-blocked",
        ):
            self.assertIn(required_row, self.skill)

        table = self.skill.split("Use this exhaustive proof-action table:", 1)[1].split("Before production mutation", 1)[0]
        rows = []
        for line in table.splitlines():
            if not line.startswith("|") or "---" in line or "Test feasibility" in line:
                continue
            rows.append(tuple(cell.strip() for cell in line.strip("|").split("|")))
        self.assertEqual(len(rows), 6)

        feasibilities = ("feasible", "unresolved", "infeasible-with-rationale")
        proofs = ("failing-automated-test", "conflicting", "missing", "deterministic-alternative")
        for feasibility in feasibilities:
            for proof in proofs:
                matches = []
                for row_feasibility, row_proof, action in rows:
                    feasibility_matches = row_feasibility == "Any recognized" or row_feasibility == feasibility
                    proof_matches = proof in tuple(part.strip() for part in row_proof.replace("complete ", "").split(" or "))
                    if feasibility_matches and proof_matches:
                        matches.append(action)
                self.assertEqual(
                    len(matches),
                    1,
                    f"expected one proof action for {feasibility}/{proof}, got {matches}",
                )

    def test_edge_classification_prevents_action_overlap(self) -> None:
        self.assertIn("without one concrete defect returns `blocked`", self.skill)
        self.assertIn("incomplete claimed deterministic alternative as `missing`", self.skill)
        self.assertIn("cross-axis inconsistency", self.skill)
        self.assertIn("contract basis value `conflicting` routes under the next rule", self.skill)

    def test_operation_command_and_write_authority_are_independent(self) -> None:
        for value in (
            "diagnose-only",
            "current-bounded",
            "portable-request-bound",
            "governed-scope-bound",
            "invalid-or-ambiguous",
            "one concrete defect",
            "rerun preflight",
        ):
            self.assertIn(value, self.skill)

    def test_proof_authoring_precedes_production_correction(self) -> None:
        for value in (
            "proof-authoring",
            "production-correction",
            "failing-automated-test",
            "infeasible-with-rationale",
            "deterministic-alternative",
            "proof identity",
        ):
            self.assertIn(value, self.skill)
        self.assertLess(self.skill.index("proof-authoring"), self.skill.index("production-correction"))
        self.assertIn("post-fix-validation", self.skill)

    def test_action_precedence_protects_completed_and_failed_corrections(self) -> None:
        for value in (
            "stop-blocked",
            "route-owner",
            "continue-diagnosis",
            "complete-diagnosis",
            "resolve-test-feasibility",
            "author-automated-proof",
            "apply-production-correction",
            "run-post-fix-validation",
            "complete-fix",
        ):
            self.assertIn(value, self.skill)
        completed = self.skill.index("correction exists and all required checks pass")
        eligible = self.skill.index("eligible fix without correction")
        self.assertLess(completed, eligible)

    def test_causes_and_terminal_results_are_closed(self) -> None:
        for value in (
            "implementation-defect",
            "contract-gap",
            "integration-mismatch",
            "data-or-migration",
            "race-or-timing",
            "configuration-or-environment",
            "external-dependency",
            "test-defect",
            "unknown",
            "diagnosis-complete",
            "diagnosis-incomplete",
            "fix-applied",
            "routed-to-owner",
            "blocked",
        ):
            self.assertIn(value, self.skill)

    def test_governed_signals_and_write_owners_fail_closed(self) -> None:
        for value in (
            "no-governed-signal",
            "single-governed-candidate",
            "invalid-or-ambiguous-governed-signal",
            "never fall back",
            "change.json",
            "read-only",
            "do not invent",
        ):
            self.assertIn(value, self.skill)
        for required_row in (
            "Portable diagnose-only | None",
            "Portable proof-authoring | Request-bound tests, fixtures, test-only helpers, and controlled reproduction artifacts",
            "Portable production-correction | Request-bound implementation and explicitly scoped non-authoritative documentation or examples",
            "Governed diagnose-only | None",
            "Governed proof-authoring | Exact governed proof surfaces and one existing authorized evidence destination",
            "Governed production-correction | Exact governed implementation, existing authorized evidence, and only scope-named non-authoritative documentation",
        ):
            self.assertIn(required_row, self.skill)

    def test_result_and_handoff_claims_are_bounded(self) -> None:
        for value in (
            "commands actually run",
            "unexecuted checks",
            "changed surfaces",
            "code-review",
            "no stage continues automatically",
            "PR readiness",
            "lifecycle completion",
            "Unexpected mutation",
            "repository and defect",
            "proof identity",
            "next owner",
        ):
            self.assertIn(value, self.skill)


class ConsolidatedReviewGateSkillContractTests(unittest.TestCase):
    """CRG-T03 and CRG-T13 public-skill contract proof for M4."""

    def test_proposal_owns_one_complete_embedded_feasibility_section(self) -> None:
        skeleton = (ROOT / "skills/proposal/assets/proposal-skeleton.md").read_text(
            encoding="utf-8"
        )
        proposal = (ROOT / "skills/proposal/SKILL.md").read_text(encoding="utf-8")
        review = (ROOT / "skills/proposal-review/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertEqual(skeleton.count("## Feasibility"), 1)
        for term in ("assessment", "basis", "constraints", "blockers"):
            self.assertIn(term, skeleton.lower())
        self.assertIn("exactly one non-empty `Feasibility` section", proposal)
        self.assertIn("no standalone feasibility artifact", proposal)
        for term in (
            "missing",
            "unsupported",
            "contradicted",
            "materially stale",
            "blocking",
            "proposal revision",
        ):
            self.assertIn(term, review)

    def test_consolidated_review_skills_own_distinct_exact_packages(self) -> None:
        expected = {
            "design-review": (
                "architecture",
                "specification",
                "applicable ADR",
                "accepted Proposal Review ID",
                "plan authoring",
            ),
            "delivery-review": (
                "execution plan",
                "exact primary plan",
                "approved Design Review ID",
                "requirement -> architectural boundary -> implementation milestone -> required proof -> validation command or manual evidence",
                "implementation",
            ),
        }
        for skill_name, terms in expected.items():
            skill_dir = ROOT / "skills" / skill_name
            body = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            for path in (
                skill_dir / "assets/review-result-skeleton.md",
                skill_dir / "assets/material-finding.md",
                skill_dir / f"references/{skill_name}-recording-and-settlement.md",
            ):
                self.assertTrue(path.is_file(), path)
            for term in terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)
            for term in (
                "artifact-local",
                "cross-artifact",
                "upstream-direction",
                "does not edit",
                "Direct review remains isolated",
                "review record",
                "no separate legacy settlement operation",
            ):
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

    def test_post_cutover_inventory_retires_old_reviews_without_aliases(self) -> None:
        route = (ROOT / "skills/route/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "proposal -> proposal-review -> design -> design-review -> plan -> delivery-review -> implement",
            " ".join(route.split()),
        )
        self.assertIn("Supported targets are", route)
        for retired_target in (
            "spec-review",
            "architecture-review",
            "plan-review",
            "test-spec-review",
        ):
            self.assertNotIn(f"`{retired_target}`", route)

    def test_downstream_skills_consume_package_authority_without_merging_gates(self) -> None:
        for skill_name in ("code-review", "verify", "pr"):
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            with self.subTest(skill=skill_name):
                self.assertIn("approved Design Review ID", body)
                self.assertIn("approved Delivery Review ID", body)


class RequirementDeliveryModelM1Tests(unittest.TestCase):
    def test_m1_shared_model_defines_lightweight_refinement_and_work_decomposition(self) -> None:
        shared_path = ROOT / "templates" / "shared" / "requirement-to-delivery-model.md"
        self.assertTrue(shared_path.is_file(), shared_path)
        shared = shared_path.read_text(encoding="utf-8")
        for term in (
            "RR → IR → SR → AR",
            "Epic → Feature → Story → Task",
            "The two views are not equivalent hierarchies.",
            "SR identities are the durable downstream requirement references.",
            "RR, IR, and AR do not require separate artifacts or identifiers.",
            "Add a work level only when it materially improves ownership, sequencing, reviewability, traceability, or coordination.",
            "SR-01 → M1 and M2",
            "SR-01 + SR-02 → M2",
        ):
            with self.subTest(term=term):
                self.assertIn(term, shared)

    def test_m1_authoring_skills_map_local_responsibility_and_conditionally_load_model(self) -> None:
        expected = {
            "proposal": (
                "Treat the incoming need as RR and the approved proposal as the durable IR-level direction.",
                "when clarifying an incoming need into proposal direction or explaining how proposal approval feeds Design",
            ),
            "plan": (
                "Treat the plan as the primary allocation surface from SRs and architecture boundaries into proportional delivery work.",
                "when allocating system requirements and architecture boundaries into milestones or optional work hierarchy",
            ),
        }
        for skill_name, (responsibility, load_condition) in expected.items():
            skill_root = ROOT / "skills" / skill_name
            body = (skill_root / "SKILL.md").read_text(encoding="utf-8")
            local_reference = skill_root / "references" / "requirement-to-delivery-model.md"
            with self.subTest(skill=skill_name, check="responsibility"):
                self.assertIn(responsibility, body)
            with self.subTest(skill=skill_name, check="resource-map"):
                self.assertIn(
                    f"READ `references/requirement-to-delivery-model.md` {load_condition}.",
                    body,
                )
            with self.subTest(skill=skill_name, check="packaged-reference"):
                self.assertTrue(local_reference.is_file(), local_reference)

    def test_m1_existing_artifact_structures_already_expose_traceability_without_new_entities(self) -> None:
        spec_asset = (ROOT / "skills" / "design" / "assets" / "design-skeleton.md").read_text(encoding="utf-8")
        milestone_asset = (ROOT / "skills" / "plan" / "assets" / "milestone.md").read_text(encoding="utf-8")
        self.assertIn("## Requirements", spec_asset)
        self.assertIn("## Architecture Decisions", spec_asset)
        self.assertIn("- Requirements:", milestone_asset)
        self.assertIn("- Architecture responsibility:", milestone_asset)
        combined = "\n".join((spec_asset, milestone_asset))
        for forbidden in ("RR ID", "IR ID", "AR ID", "## Epic", "## Feature", "## Story"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, combined)


class RequirementDeliveryModelM2Tests(unittest.TestCase):
    def test_m2_review_and_verification_skills_apply_stage_local_traceability(self) -> None:
        expected = {
            "proposal-review": "Judge whether the proposal responsibly refines the incoming RR into an IR-level direction sufficient for Design.",
            "design-review": "Trace the approved IR-level direction into coherent requirements and their Design realization.",
            "delivery-review": "Trace SRs and architecture boundaries into proportional allocated work and proof.",
            "code-review": "Trace the implementation to its allocated work, governing SRs, and approved design boundaries.",
            "verify": "Trace current evidence backward through implementation and allocated work to governing SRs and the approved proposal direction.",
        }
        shared = (ROOT / "templates" / "shared" / "requirement-to-delivery-model.md").read_bytes()
        for skill_name, criterion in expected.items():
            skill_root = ROOT / "skills" / skill_name
            body = (skill_root / "SKILL.md").read_text(encoding="utf-8")
            local_reference = skill_root / "references" / "requirement-to-delivery-model.md"
            with self.subTest(skill=skill_name, check="criterion"):
                self.assertIn(criterion, body)
            with self.subTest(skill=skill_name, check="resource-map"):
                self.assertIn("READ `references/requirement-to-delivery-model.md` when tracing", body)
            with self.subTest(skill=skill_name, check="packaged-reference"):
                self.assertEqual(local_reference.read_bytes(), shared)

    def test_m2_shared_guidance_does_not_grant_review_or_lifecycle_authority(self) -> None:
        shared = (ROOT / "templates" / "shared" / "requirement-to-delivery-model.md").read_text(encoding="utf-8")
        self.assertIn("It creates no lifecycle stage, artifact, identifier, settlement authority, readiness claim, or required hierarchy.", shared)
        for forbidden in ("approval authority", "may settle", "may advance", "automatically approves"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, shared.lower())


class ReviewCloseoutResourceTests(unittest.TestCase):
    def test_unknown_value_consumer_fails_closed(self):
        errors = skill_validation.validate_review_closeout_copies(Path("unused/SKILL.md"), "unknown_value")
        self.assertTrue(any("unknown" in e for e in errors))

    def test_missing_drifted_and_valid_resources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            skill = root / "skills" / "code-review" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            for name in ("review-assessment", "review-reliance"):
                (source / (name + ".md")).write_text(name)
            self.assertTrue(skill_validation.validate_review_closeout_copies(skill, "code-review", source=source))
            (skill.parent / "references").mkdir()
            for name in ("review-assessment", "review-reliance"):
                shutil.copyfile(source / (name + ".md"), skill.parent / "references" / (name + ".md"))
            self.assertEqual([], skill_validation.validate_review_closeout_copies(skill, "code-review", source=source))
            (skill.parent / "references" / "review-assessment.md").write_text("drift")
            self.assertTrue(any("differs" in e for e in skill_validation.validate_review_closeout_copies(skill, "code-review", source=source)))

    def test_all_selected_consumers_carry_exact_resources(self):
        for name in skill_validation.REVIEW_CLOSEOUT_CONSUMERS:
            with self.subTest(skill=name):
                self.assertEqual([], skill_validation.validate_review_closeout_copies(ROOT / "skills" / name / "SKILL.md", name))


class RequirementDeliveryModelM3Tests(unittest.TestCase):
    def test_m3_all_nine_consumers_match_canonical_bytes(self) -> None:
        canonical = ROOT / "templates" / "shared" / "requirement-to-delivery-model.md"
        for skill_name in sorted(skill_validation.REQUIREMENT_DELIVERY_MODEL_CONSUMERS):
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    skill_validation.validate_requirement_delivery_model_copy(skill_path, skill_name),
                    [],
                )
                self.assertEqual(
                    (skill_path.parent / "references" / "requirement-to-delivery-model.md").read_bytes(),
                    canonical.read_bytes(),
                )

    def test_m3_missing_and_drifted_copy_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = root / "canonical.md"
            canonical.write_text("canonical\n", encoding="utf-8")
            skill_path = root / "skills" / "proposal" / "SKILL.md"
            skill_path.parent.mkdir(parents=True)
            skill_path.write_text("# Proposal\n", encoding="utf-8")
            missing = skill_validation.validate_requirement_delivery_model_copy(
                skill_path, "proposal", canonical_path=canonical
            )
            self.assertIn("is missing", missing[0])
            local = skill_path.parent / "references" / "requirement-to-delivery-model.md"
            local.parent.mkdir()
            local.write_text("drifted\n", encoding="utf-8")
            drifted = skill_validation.validate_requirement_delivery_model_copy(
                skill_path, "proposal", canonical_path=canonical
            )
            self.assertIn("differs from canonical", drifted[0])

    def test_m3_public_validator_rejects_missing_mapped_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skills_root = root / "skills"
            shutil.copytree(ROOT / "skills" / "proposal", skills_root / "proposal")
            missing = skills_root / "proposal" / "references" / "requirement-to-delivery-model.md"
            missing.unlink()
            with mock.patch.object(skill_validation, "CANONICAL_SKILLS_DIR", skills_root), mock.patch.object(
                skill_validation,
                "REQUIREMENT_DELIVERY_MODEL_SOURCE",
                ROOT / "templates" / "shared" / "requirement-to-delivery-model.md",
            ):
                result = skill_validation.validate_skill_tree(skills_root / "proposal")
            self.assertTrue(
                any("mapped requirement-to-delivery reference is missing" in error for error in result.errors),
                result.errors,
            )


class RetireStandaloneTestSpecM3Tests(unittest.TestCase):
    """RTS TS-007 through TS-011 and TS-016 skill-package proof."""

    def test_spec_owns_testable_behavior_without_test_mechanics(self) -> None:
        root = ROOT / "skills/design"
        body = (root / "SKILL.md").read_text() + (root / "references/model-authoring.md").read_text()
        for concept in ("observable", "invariants", "authority", "compatibility", "migration", "retries", "concurrency", "recovery", "representative", "prohibited side effects"):
            self.assertIn(concept, body)
        self.assertIn("Delivery allocates concrete checks, commands, milestones and evidence", body)
        skeleton = (root / "assets/design-skeleton.md").read_text()
        self.assertIn("## Requirements", skeleton)
        self.assertIn("### Boundary scan and acceptance scenarios", skeleton)

    def test_plan_allocates_verification_without_replacement_artifact(self) -> None:
        skill = (ROOT / "skills/plan/SKILL.md").read_text(encoding="utf-8")
        skeleton = (ROOT / "skills/plan/assets/plan-skeleton.md").read_text(
            encoding="utf-8"
        )
        milestone = (ROOT / "skills/plan/assets/milestone.md").read_text(
            encoding="utf-8"
        )
        for field in (
            "Engineering purpose",
            "Requirements",
            "Architecture responsibility",
            "Dependencies",
            "Implementation scope",
            "Completion criteria",
            "Required verification",
            "Evidence expectations",
        ):
            with self.subTest(field=field):
                self.assertIn(field, milestone)
        self.assertIn("## Change-level verification", skeleton)
        self.assertIn("SR → allocated milestone or work → verification group → concrete proof → evidence", skill)
        self.assertIn("does not imply complete-change correctness", skill)
        self.assertIn("not a governed artifact", skill)
        self.assertIn("safe engineering and dependency sequence", skill)

    def test_plan_specialist_methods_are_complete_and_conditional(self) -> None:
        skill_root = ROOT / "skills/plan"
        body = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        references = (
            "boundary-and-negative-verification.md",
            "state-machine-verification.md",
            "concurrency-and-retry-verification.md",
            "migration-and-compatibility-verification.md",
            "failure-and-recovery-verification.md",
            "security-and-authority-verification.md",
            "cross-milestone-integration-verification.md",
            "manual-and-operational-evidence.md",
        )
        for name in references:
            with self.subTest(reference=name):
                self.assertTrue((skill_root / "references" / name).is_file())
                self.assertIn(f"READ `references/{name}` only when", body)
        self.assertIn("do not load every specialist reference by default", body.lower())

    def test_delivery_review_owns_one_joint_plan_centered_decision(self) -> None:
        body = (ROOT / "skills/delivery-review/SKILL.md").read_text(
            encoding="utf-8"
        )
        for concept in (
            "implementation readiness",
            "verification adequacy",
            "exact primary plan",
            "change-level verification",
            "realistic evidence",
            "route the correction to `plan`",
            "standalone test-spec substitute",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, body.lower())
        self.assertIn("one independent decision", body)
        self.assertNotIn("one execution plan, one test specification", body)


    def test_verification_allocation_gaps_route_to_plan_without_legacy_progression(self) -> None:
        for skill_name in ("design", "plan", "route"):
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            with self.subTest(skill=skill_name):
                self.assertIn(
                    "A pre-implementation verification-allocation gap routes to `plan`",
                    body,
                )
                self.assertIn(
                    "Historical contracts grant no current progression authority",
                    body,
                )
                self.assertNotIn("a proof-only gap routes to `test-spec`", body)


class RetireStandaloneTestSpecM4Tests(unittest.TestCase):
    """RTS TS-012 and TS-016 activation governance coherence."""

    def test_current_boundary_adoption_is_owned_by_the_selected_project_contract(self):
        source = (ROOT / "templates/shared/boundary-first-compact-scan.md").read_text()
        self.assertNotIn("new behavior-changing specs adopt automatically", source)
        self.assertIn("project's selected contract", source)
        self.assertIn("Design Review", source)
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            text = path.read_text()
            self.assertNotIn("new behavior-changing specs adopt automatically", text, str(path))

    def test_shared_boundary_routing_is_v3_only(self) -> None:
        required = (
            "A pre-implementation verification-allocation gap routes to `plan`",
            "Historical contracts grant no current progression authority",
        )
        template = (ROOT / "templates/shared/boundary-first-compact-scan.md").read_text(encoding="utf-8")
        for phrase in required:
            self.assertIn(phrase, template)
        for skill_name in ("route", "design", "plan", "implement", "code-review"):
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                for phrase in required:
                    self.assertIn(phrase, body)
        verify = (ROOT / "skills/verify/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("A pre-implementation verification-allocation gap routes to `plan`", verify)
        self.assertIn("Historical contracts grant no current progression authority", verify)

    def test_active_guidance_preserves_downstream_gates_and_history(self) -> None:
        combined = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in ("CONSTITUTION.md", "AGENTS.md", "skills/route/SKILL.md")
        )
        lowered = combined.lower()
        self.assertIn("code-review", lowered)
        self.assertIn("verify", lowered)
        self.assertIn("historical", lowered)
        self.assertNotIn("New changes remain v1 until M5", combined)


class FinalVerificationPackageParityM4Tests(unittest.TestCase):

    def test_verify_has_no_preverification_explanation_dependency(self) -> None:
        body = (ROOT / "skills/verify/SKILL.md").read_text(encoding="utf-8")
        for forbidden in (
            "after `explain-change`",
            "explain-change artifact",
            "current explanation",
            "rationale to `explain-change`",
        ):
            self.assertNotIn(forbidden, body)
        self.assertIn("final explanation only after successful final readiness", body)


    def test_scoped_verify_does_not_load_final_impact_or_explanation_resources(self) -> None:
        body = (ROOT / "skills/verify/SKILL.md").read_text(encoding="utf-8")
        scoped = body.split("### Final-readiness profile", 1)[1].split("## Execution authority", 1)[0]
        self.assertIn("Scoped verification loads none of those final-closeout resources", scoped)
        self.assertNotIn("VP0-scoped` | yes", body)
        self.assertIn("only after a selected final-readiness attempt has succeeded", body)


class RetireStandaloneTestSpecM5Tests(unittest.TestCase):
    """RTS TS-013 and TS-017 active publication contract."""

    def test_active_public_skill_inventory_has_no_standalone_test_spec(self) -> None:
        self.assertFalse((ROOT / "skills/test-spec").exists())
        self.assertFalse((ROOT / "skills/test-spec-review").exists())

    def test_active_workflow_is_plan_centered(self) -> None:
        body = (ROOT / "skills/route/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("plan -> delivery-review -> implement", body)
        self.assertNotIn("plan -> test-spec -> delivery-review", body)

    def test_conditional_workflow_resources_are_plan_centered(self) -> None:
        automation = (
            ROOT / "skills/route/references/bounded-workflow-automation.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`plan`, `delivery-review`", automation)
        self.assertNotIn("`plan`, `test-spec`, `delivery-review`", automation)
        self.assertFalse((ROOT / "skills/route/assets/workflows-skeleton.md").exists())


class OptionalDiscoverySkillContractTests(unittest.TestCase):
    """ER-R1-ER-R22 and ER-R27-ER-R34 canonical package contract."""

    def test_explore_uses_proportional_standalone_option_discovery(self) -> None:
        body = (ROOT / "skills/explore/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("docs/explorations/YYYY-MM-DD-slug.md", body)
        self.assertIn("enough materially distinct options", body)
        self.assertIn("explicit invocation", body)
        self.assertIn("decision owner", body)
        self.assertNotIn("Generate at least five options", body)
        self.assertNotIn("docs/proposals/YYYY-MM-DD-slug.explore.md", body)
        self.assertNotIn("inline exploration report", body)

    def test_research_uses_bounded_standalone_evidence(self) -> None:
        body = (ROOT / "skills/research/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("docs/research/YYYY-MM-DD-slug.md", body)
        self.assertIn("bounded", body)
        self.assertIn("explicit invocation", body)
        self.assertIn("confidence", body)
        self.assertIn("decision owner", body)
        self.assertNotIn("compact research section", body)
        self.assertNotIn("research artifact path or concise report", body)

    def test_discovery_packages_are_self_contained_and_share_exact_policy(self) -> None:
        canonical = (ROOT / "templates/shared/discovery-support.md").read_bytes()
        expected_resources = {
            "explore": {
                "assets/exploration-skeleton.md",
                "references/discovery-support.md",
                "references/option-discovery-methods.md",
                "references/high-impact-decision-method.md",
            },
            "research": {
                "assets/research-skeleton.md",
                "references/discovery-support.md",
                "references/source-and-repository-method.md",
                "references/experiment-and-confidence-method.md",
            },
        }
        for skill_name, resources in expected_resources.items():
            skill_dir = ROOT / "skills" / skill_name
            body = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    canonical,
                    (skill_dir / "references/discovery-support.md").read_bytes(),
                )
                for resource in resources:
                    self.assertTrue((skill_dir / resource).is_file(), resource)
                    self.assertIn(resource, body)
                self.assertIn("## Resource map", body)
                self.assertIn("## Stop conditions", body)
                self.assertIn("## Claims this skill must not make", body)

    def test_skill_contract_names_discovery_shared_policy(self) -> None:
        # Structural name-presence guard only. Admission meaning is assessed by
        # independent semantic review; this substring cannot establish it.
        contract = (ROOT / "docs/design/skill/skill.md").read_text(encoding="utf-8")
        self.assertIn("discovery-support", contract)

    def test_every_discovery_package_file_omits_maintainer_only_details(self) -> None:
        forbidden = {
            "canonical skill path": re.compile(r"\bskills/(?:explore|research)/SKILL\.md\b"),
            "shared template path": re.compile(r"\btemplates/shared\b"),
            "adapter package path": re.compile(r"\bdist/adapters\b"),
            "selector constraint": re.compile(r"\bselector[- ]path constraints\b", re.IGNORECASE),
            "shared-copy mechanics": re.compile(r"\bshared[- ]block implementation\b", re.IGNORECASE),
        }
        for skill_name in ("explore", "research"):
            for path in sorted((ROOT / "skills" / skill_name).rglob("*")):
                if not path.is_file():
                    continue
                body = path.read_text(encoding="utf-8")
                for label, pattern in forbidden.items():
                    with self.subTest(skill=skill_name, path=path.name, pattern=label):
                        self.assertIsNone(pattern.search(body))

    def test_canonical_validation_rejects_discovery_shared_policy_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = root / "discovery-support.md"
            canonical.write_text("canonical\n", encoding="utf-8")
            local = root / "local.md"
            local.write_text("drifted\n", encoding="utf-8")
            errors = skill_validation.validate_discovery_support_copy(
                local,
                "explore",
                canonical_path=canonical,
            )
        self.assertTrue(any("differs from canonical source" in error for error in errors))

    def test_canonical_validation_rejects_unknown_discovery_skill_name(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = root / "discovery-support.md"
            canonical.write_text("canonical\n", encoding="utf-8")
            local = root / "local.md"
            local.write_text("canonical\n", encoding="utf-8")
            errors = skill_validation.validate_discovery_support_copy(
                local,
                "unknown-discovery-skill",
                canonical_path=canonical,
            )
        self.assertTrue(any("unknown discovery support consumer" in error for error in errors))

    def test_route_distinguishes_explore_research_both_and_neither(self) -> None:
        route = (ROOT / "skills/route/SKILL.md").read_text(encoding="utf-8")
        expected = {
            "Explore": "the option space is materially unclear",
            "Research": "a material decision depends on an uncertain fact",
            "both": "research questions could materially change the option comparison",
            "neither": "direction and decision-relevant facts are sufficiently clear",
        }
        for route_case, phrase in expected.items():
            with self.subTest(route_case=route_case):
                self.assertIn(phrase, route)

    def test_current_guidance_agrees_on_explicit_optional_discovery_handoff(self) -> None:
        surfaces = {
            "workflow": ROOT / "skills/route/SKILL.md",
            "readme": ROOT / "README.md",
            "project-map": ROOT / "docs/project-map.md",
        }
        bodies = {
            name: path.read_text(encoding="utf-8")
            for name, path in surfaces.items()
        }
        for name, body in bodies.items():
            with self.subTest(surface=name, rule="optional"):
                self.assertIn("Explore", body)
                self.assertIn("Research", body)
        self.assertIn("explicit invocation", bodies["workflow"])
        self.assertIn("owning stage", bodies["workflow"])
        self.assertIn("docs/explorations/", bodies["project-map"])
        self.assertIn("docs/research/", bodies["project-map"])

    def test_route_keeps_incidental_discovery_artifact_free_and_owner_bounded(self) -> None:
        route = (ROOT / "skills/route/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("incidental fact check", route)
        self.assertIn("does not create a discovery artifact", route)
        self.assertIn("must explicitly adopt", route)
        self.assertIn("does not approve", route)
        self.assertIn("does not advance lifecycle state", route)


class TestPolicyResourceTests(unittest.TestCase):
    def test_unknown_value_test_policy_consumer_fails_closed(self):
        errors = skill_validation.validate_test_policy_copies(Path("unused/SKILL.md"), "unknown_value")
        self.assertTrue(any("unknown" in error for error in errors))

    def test_test_policy_missing_and_drifted_resources_reject(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "shared"
            source.mkdir()
            skill = root / "implement" / "SKILL.md"
            refs = skill.parent / "references"
            refs.mkdir(parents=True)
            for name in ("test-quality", "test-maintenance"):
                (source / f"{name}.md").write_text("criterion\n")
            self.assertTrue(skill_validation.validate_test_policy_copies(skill, "implement", source=source))
            for name in ("test-quality", "test-maintenance"):
                (refs / f"{name}.md").write_text("criterion\n")
            self.assertEqual([], skill_validation.validate_test_policy_copies(skill, "implement", source=source))
            (refs / "test-maintenance.md").write_text("changed\n")
            self.assertTrue(any("differs" in error for error in skill_validation.validate_test_policy_copies(skill, "implement", source=source)))

    def test_test_policy_canonical_copies_and_conditional_resources(self):
        for name in skill_validation.TEST_QUALITY_CONSUMERS:
            with self.subTest(name=name):
                path = ROOT / "skills" / name / "SKILL.md"
                self.assertEqual([], skill_validation.validate_test_policy_copies(path, name))
                self.assertIn("READ `references/test-quality.md`", path.read_text())
                if name in skill_validation.TEST_MAINTENANCE_CONSUMERS:
                    self.assertIn("READ `references/test-maintenance.md`", path.read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
