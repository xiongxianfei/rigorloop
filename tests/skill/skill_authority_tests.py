"""Authority.

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
