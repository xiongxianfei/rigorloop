"""Canonical cross-skill guidance, shared blocks and workflow contract consistency.

Preserves the group's existing conditions and required observations.
Structural wording checks do not establish instruction quality.
"""
from __future__ import annotations

import unittest
from review_independence_skill_phrases import R5_FORBIDDEN_INITIAL_PACKET_ITEMS, R8D_FAILED_REMEDIATION_REQUIRED_PHRASES, R8D_RECONCILIATION_CATEGORIES
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.validation import skill_validation
from skill_guidance_helpers import (
    CODE_REVIEW_FORBIDDEN_FINAL_CLOSEOUT_PATTERNS,
    DOWNSTREAM_REVIEW_CLOSEOUT_SKILLS,
    PROGRESSIVE_LOADING_OPTIMIZED_SKILLS,
    SHARED_REVIEW_BLOCK_PATH,
    SKILL_CONTRACT_CLAIM_BOUNDARY_TERMS,
    SKILL_CONTRACT_DEFERRED_SHARED_BLOCKS,
    SKILL_CONTRACT_EVIDENCE_BLOCK,
    SKILL_CONTRACT_FIRST_SLICE_SKILLS,
    SKILL_CONTRACT_FORBIDDEN_NEW_SKILLS,
    SKILL_CONTRACT_PROGRESS_SKILLS,
    SKILL_CONTRACT_REQUIRED_CORE_SECTIONS,
    SKILL_CONTRACT_RESULT_FIELDS,
    VERIFY_FORBIDDEN_EXPLAIN_ORDER_PATTERNS,
    assert_progressive_loading_code_review_protected_contracts,
    assert_progressive_loading_quick_guide_contract,
    extract_markdown_block,
    iter_published_skill_surfaces_for,
)


class CanonicalSkillGuidanceTests(unittest.TestCase):
    maxDiff = None

    def test_vision_skill_defines_state_based_boundaries_and_readme_marker_contract(self) -> None:
        root = ROOT / "skills" / "vision"
        body = (root / "SKILL.md").read_text(encoding="utf-8")
        body += "\n" + (root / "references" / "strategic-vision-authoring.md").read_text(encoding="utf-8")
        body += "\n" + (root / "references" / "readme-vision-sync.md").read_text(encoding="utf-8")
        required_terms = [
            "name: vision",
            "project vision and matching README front-matter",
            "## State-Based Behavior",
            "ordinary user intent",
            "Do not ask users to choose `create`, `revise`, or `mirror` modes.",
            "Do not create the initial `VISION.md` just because this skill is installed",
            "`VISION.md` is canonical",
            "`CONSTITUTION.md` outranks `VISION.md`",
            "`VISION.md` outranks README front-matter",
            "retired root `vision.md`",
            "only supported project-vision artifact",
            "If the user explicitly asks to establish project vision, create root `VISION.md`",
            "<!-- vision:start -->",
            "<!-- vision:end -->",
            "first H1 block",
            "Automatic marker insertion is allowed only when creating the initial `VISION.md`.",
            "When updating an existing `VISION.md` or syncing README",
            "missing or malformed markers stop the skill before file modification",
            "explicitly authorizes marker insertion or skipping README mirroring",
            "malformed, nested, or multiple vision marker pairs",
            "Files changed:",
            "README front-matter:",
            "Assumptions:",
            "Sections changed:",
            "`VISION.md` unchanged:",
            "secrets",
            "credentials",
            "private local filesystem paths",
            "private machine names",
            "personal data not explicitly intended for publication",
            "must not fetch external information unless",
            "distinguish researched facts from project assumptions",
            "plain Markdown",
            "rendered tables, diagrams, HTML layout, or generated assets",
            "compact project inputs",
            "full-file reads",
            "summary and stable-ID first",
            "When full-file read is required",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

        forbidden_terms = [
            "## Modes",
            "Use exactly one mode.",
            "Mode used:",
            "The only authorized edit paths are `create`, `revise`, and `mirror`.",
            "Automatic marker insertion is allowed only in `create` mode.",
            "In `mirror` or `revise`, missing or malformed markers stop the skill before file modification",
            "treat `vision.md` as migration input",
            "both root `vision.md` and root `VISION.md`",
            "neither root vision file exists",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, body)

    def test_vision_skill_quality_refinement_contract(self) -> None:
        root = ROOT / "skills" / "vision"
        body = (root / "SKILL.md").read_text(encoding="utf-8")
        body += "\n" + (root / "references" / "strategic-vision-authoring.md").read_text(encoding="utf-8")
        required_terms = [
            "## Drafting Heuristics",
            "alternative class or specific tool",
            "tradeoff",
            "pain points",
            "checkable",
            "observable",
            "at least one plausible non-fit",
            "concrete enough to block misaligned proposals",
            "not additional `VISION.md` sections",
            "does not require naming a specific competitor",
            "## Edit Authorization",
            "`CONSTITUTION.md` outranks `VISION.md`",
            "`VISION.md` outranks README front-matter",
            "state-based behavior",
            "existing visions are not overwritten without clear update intent",
            "existing or required change-local pack",
            "before finalizing",
            "ask or confirm whether the change is `substantive` or `editorial` before finalizing",
            "required causal link was recorded or not required",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

        forbidden_terms = [
            "remind the contributor",
            "## Source Of Truth",
            "## Existing Vision Protection",
            "only authorized edit paths",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, body)

    def test_vision_skill_quality_refinement_structure(self) -> None:
        root = ROOT / "skills" / "vision"
        body = (root / "SKILL.md").read_text(encoding="utf-8")
        strategic = (root / "references" / "strategic-vision-authoring.md").read_text(encoding="utf-8")
        readme = (root / "references" / "readme-vision-sync.md").read_text(encoding="utf-8")

        workflow_index = body.index("## Workflow Fit")
        inputs_index = body.index("## Inputs To Read")
        state_index = body.index("## State-Based Behavior")
        resource_index = body.index("## Resource classification")

        self.assertLess(workflow_index, inputs_index)
        self.assertLess(inputs_index, state_index)
        self.assertLess(state_index, resource_index)
        self.assertLess(strategic.index("## Strategic Positioning"), strategic.index("## Vision Content"))
        self.assertLess(strategic.index("## Vision Content"), strategic.index("## Drafting Heuristics"))
        self.assertIn("## README Front-Matter", readme)

        self.assertNotIn("| Mode |", body)
        self.assertNotIn("| `create` |", body)
        self.assertNotIn("| `revise` |", body)
        self.assertNotIn("| `mirror` |", body)

    def test_vision_skill_strategic_positioning_contract(self) -> None:
        root = ROOT / "skills" / "vision"
        body = (root / "SKILL.md").read_text(encoding="utf-8")
        body += "\n" + (root / "references" / "strategic-vision-authoring.md").read_text(encoding="utf-8")
        required_terms = [
            "## Strategic Positioning",
            "project category",
            "primary user",
            "primary pain",
            "primary promise",
            "core mechanism",
            "alternatives",
            "tradeoff",
            "compatibility surfaces",
            "refusals",
            "falsifiability",
            "docs/vision/strategic-positioning.md",
            "`VISION.md` remains canonical",
            "supporting rationale",
            "methodology, workflow, protocol, or operating model",
            "methodology-as-product",
            "repository layout, Git, CI, pull requests, runtime, package format, hosting platform, language, and template mechanics",
            "RigorLoop-style",
            "Windows-native file manager",
            "Git extension",
            "Git-first starter kit",
            "normally stay at or under 750 words",
            "MUST NOT exceed 900 words",
            "one optional methodology-oriented section",
            "strategic-positioning summary",
            "rationale path",
            "first sentence names the highest-level category",
            "differentiator includes a tradeoff",
            "vision can guide proposal-fit review without chat history",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

    def test_proposal_skills_define_simplified_direction_contract(self) -> None:
        proposal_body = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal_asset = (
            ROOT / "skills" / "proposal" / "assets" / "proposal-skeleton.md"
        ).read_text(encoding="utf-8")
        proposal_review_body = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        review_asset = (
            ROOT / "skills" / "proposal-review" / "assets" / "review-result-skeleton.md"
        ).read_text(encoding="utf-8")

        required_sections = [
            "Challenge",
            "Goals",
            "Scope and non-goals",
            "Governing principle",
            "Proposed direction",
            "Feasibility",
            "Decision requested",
        ]
        level_two_headings = [
            line.removeprefix("## ")
            for line in proposal_asset.splitlines()
            if line.startswith("## ")
        ]
        self.assertEqual(
            level_two_headings,
            required_sections[:-1] + ["Impact and major trade-offs", required_sections[-1]],
        )

        proposal_terms = [
            "direction-approval artifact",
            "exactly seven required level-two sections",
            "Impact and major trade-offs",
            "only when it could materially affect approval",
            "depth is proportional to uncertainty",
            "No fixed word count, length, or token budget",
            "detailed behavior, architecture, APIs, commands, schemas, component design, implementation sequencing, verification design, test cases, and rollout mechanics",
            "Portable authoring requires no `change.json`",
            "`change.json` is the sole owner of governed proposal lifecycle state and ownership",
        ]
        for term in proposal_terms:
            with self.subTest(skill="proposal", term=term):
                self.assertIn(term, proposal_body)

        proposal_review_terms = [
            "Does this proposal provide enough evidence for a responsible decision about whether to pursue the direction?",
            "too vague",
            "prematurely settles",
            "must not create a finding solely because downstream detail or a routine impact section is absent",
            "Design authoring only",
            "Direct and review-only requests remain isolated",
            "aligned",
            "material-conflict",
            "vision-revision-requested",
            "no-vision-bootstrap",
        ]
        for term in proposal_review_terms:
            with self.subTest(skill="proposal-review", term=term):
                self.assertIn(term, proposal_review_body)
        self.assertIn("Vision alignment: <aligned | material-conflict | vision-revision-requested | no-vision-bootstrap>", review_asset)

        forbidden_terms = [
            "## Status",
            "## Owning change record",
            "## Vision fit",
            "## Expected Behavior Changes",
            "## Architecture Impact",
            "## Testing and Verification Strategy",
            "## Rollout and Rollback",
        ]
        for term in forbidden_terms:
            with self.subTest(asset="proposal", forbidden=term):
                self.assertNotIn(term, proposal_asset)

    def test_governance_workflow_and_readme_define_vision_source_of_truth(self) -> None:
        constitution = (ROOT / "CONSTITUTION.md").read_text()
        agents = (ROOT / "AGENTS.md").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertIn("[VISION.md](VISION.md) owns project identity and direction", constitution)
        self.assertIn("governs vision and proposal fit below this Constitution", constitution)
        self.assertIn("README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`", readme)
        self.assertIn("README front-matter is not the source of truth when it conflicts with `VISION.md`", readme)
        self.assertIn("Read [CONSTITUTION.md](CONSTITUTION.md)", agents)
        self.assertIn("README content between the vision markers is generated from it", agents)
        assessment = (ROOT / "docs/design/skill/assessment.md").read_text()
        self.assertIn("routine vision alignment", assessment)
        self.assertIn("a Proposal Review judgment", assessment)

    def test_workflow_refactor_stage_skill_guidance_alignment(self) -> None:
        workflow = (ROOT / "skills" / "route" / "SKILL.md").read_text(encoding="utf-8")
        proposal = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal += "\n" + (ROOT / "skills" / "proposal" / "references" / "strategic-and-scope-gates.md").read_text(encoding="utf-8")
        proposal_review = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        proposal_review += "\n" + (
            ROOT / "skills" / "proposal-review" / "references" / "conditional-proposal-gates.md"
        ).read_text(encoding="utf-8")
        ci = (ROOT / "skills" / "ci-maintenance" / "SKILL.md").read_text(encoding="utf-8")
        learn = (ROOT / "skills" / "learn" / "SKILL.md").read_text(encoding="utf-8")
        verify = (ROOT / "skills" / "verify" / "SKILL.md").read_text(encoding="utf-8")

        workflow_terms = [
            "## Lifecycle overview",
            "Standing artifacts",
            "Living references",
            "Workflow infrastructure",
            "On-demand support",
            "Per-change chain",
            "Periodic artifacts",
            "`mandatory`",
            "`conditional`",
            "`on-demand`",
            "`periodic`",
            "next mandatory or triggered downstream stage",
            "ci-maintenance when triggered",
        ]
        for term in workflow_terms:
            with self.subTest(skill="workflow", term=term):
                self.assertIn(term, workflow)

        workflow_forbidden = [
            "constitution / project context",
            "project-map when architecture is unclear",
            "Treat `learn` as an advice-only follow-up",
            "Advice-only stages such as `learn`",
            "next required or default downstream stage",
            "verify -> ci ->",
            "`ci` when GitHub workflow automation",
        ]
        for term in workflow_forbidden:
            with self.subTest(skill="workflow", term=term):
                self.assertNotIn(term, workflow)

        proposal_terms = [
            "A substantive proposal is any proposal that chooses product direction",
            "`VISION.md` absence blocks the first substantive proposal",
            "`CONSTITUTION.md` absence blocks governance adoption",
            "Bootstrap proposals",
            "`Impact and major trade-offs` and `Decision requested`",
            "next mandatory or triggered downstream stage",
        ]
        for term in proposal_terms:
            with self.subTest(skill="proposal", term=term):
                self.assertIn(term, proposal)

        proposal_review_terms = [
            "bootstrap exception",
            "`Impact and major trade-offs` and `Decision requested`",
            "Request revision if the disclosure is missing",
            "standing artifact gate",
        ]
        for term in proposal_review_terms:
            with self.subTest(skill="proposal-review", term=term):
                self.assertIn(term, proposal_review)

        ci_terms = [
            "ci-maintenance",
            "CI infrastructure",
            "bounded PR CI repair",
            "already-authoritative validation commands",
            "observe the replacement hosted check",
            "does not design tests",
            "does not specify validation commands",
            "does not claim branch readiness",
        ]
        for term in ci_terms:
            with self.subTest(skill="ci", term=term):
                self.assertIn(term, ci)

        learn_terms = [
            "`learn` is periodic or explicitly invoked",
            "repeated review findings",
            "blocker or major workflow-process findings",
            "failed release or adapter smoke",
            "accepted postmortem action",
            "explicit maintainer request",
            "capture the lesson immediately",
            "scheduled follow-up",
            "explicit no-learn rationale",
            "blocks downstream only when a higher-priority artifact explicitly makes it blocking",
            "contributor-visible tracked or review-visible surface",
        ]
        for term in learn_terms:
            with self.subTest(skill="learn", term=term):
                self.assertIn(term, learn)
        self.assertNotIn("advice-only", learn)

        verify_terms = [
            "hands off to `pr`",
            "ci-maintenance",
            "hosted workflow automation, validation automation, or related platform configuration",
        ]
        for term in verify_terms:
            with self.subTest(skill="verify", term=term):
                self.assertIn(term, verify)
        self.assertNotIn("next required or default downstream stage", verify)
        self.assertNotIn("downstream stage is `ci`", verify)

    def test_learn_skill_final_artifact_model_and_bounded_process(self) -> None:
        skill_body = (ROOT / "skills" / "learn" / "SKILL.md").read_text(encoding="utf-8")
        method_path = ROOT / "skills" / "learn" / "references" / "session-method.md"
        method_body = method_path.read_text(encoding="utf-8") if method_path.exists() else ""
        combined_body = skill_body + "\n" + method_body
        readme_path = ROOT / "docs" / "learn" / "README.md"
        self.assertTrue(readme_path.exists(), "docs/learn/README.md must exist as the learn namespace index")
        readme_body = readme_path.read_text(encoding="utf-8")

        required_skill_terms = [
            "`docs/learn/sessions/YYYY-MM-DD-<slug>.md`",
            "`docs/learn/topics/<topic>.md`",
            "Frame",
            "Observe",
            "Classify",
            "Route",
            "primary classification",
            "secondary routes",
            "`observation`",
            "`durable-lesson`",
            "`artifact-update`",
            "`decision`",
            "`direction`",
            "`process-follow-up`",
            "`no-durable-lesson`",
            "contributor confirmation",
            "confirmed-by",
            "candidate classifications",
            "no-learn rationale",
            "single event",
            "systemic gap",
            "maintainer request",
            "Maintainer-driven rule adoption without accumulated evidence",
            "repeated review findings",
            "repeated incidents",
            "failed smoke patterns",
            "recurring validation gaps",
            "prior session evidence",
            "not `durable-lesson`",
            "proposal work",
            "may later produce an ADR",
            "accepted authoritative artifact",
            "incident response",
            "contributor observation",
            "periodic learn sessions",
            "time window start",
            "time window end",
            "window basis",
            "bounded evidence",
            "trigger statement and named artifacts",
            "exact sections first",
            "full-file reads only when narrower evidence is insufficient",
            "topic files are curated guidance",
            "must not override",
            "action-owning artifact",
            "`docs/roadmap.md`",
            "pre-session trigger closeout",
            "Frame phase",
        ]
        for term in required_skill_terms:
            with self.subTest(file="learn skill", term=term):
                self.assertIn(term, combined_body)

        required_readme_terms = [
            "docs/learn/",
            "sessions/",
            "topics/",
            "`docs/learn/sessions/YYYY-MM-DD-<slug>.md`",
            "`docs/learn/topics/<topic>.md`",
            "raw historical session records",
            "curated durable topic guidance",
            "session record is the primary output",
            "Topic files are curated guidance",
            "not authoritative",
            "No templates",
            "No empty topic taxonomy",
            "remove, revise, or absorb",
            "traceability",
        ]
        for term in required_readme_terms:
            with self.subTest(file="learn readme", term=term):
                self.assertIn(term, readme_body)

        forbidden_terms = [
            "docs/retrospectives",
            "docs/learnings",
            "future learn refactor",
            "temporary learn refactor",
            "General retrospective",
            "Until the future learn refactor",
        ]
        for body, label in ((skill_body, "learn skill"), (readme_body, "learn readme")):
            for term in forbidden_terms:
                with self.subTest(file=label, term=term):
                    self.assertNotIn(term, body)

    def test_shared_isolation_and_recording_block_defines_broad_material_rule(self) -> None:
        canonical = extract_markdown_block(
            SHARED_REVIEW_BLOCK_PATH.read_text(encoding="utf-8"),
            "Isolation and Recording",
        )
        normalized = " ".join(canonical.split())
        required_terms = [
            "Isolation governs handoff. Recording follows formal review triggers.",
            "A direct or review-only request remains isolated by default",
            "Isolation does not suppress recording.",
            "Every formal lifecycle review result must be recorded or explicitly blocked.",
            "`Recording status: recorded`",
            "`Recording status: blocked`",
            "Use the selected v3 registry and targeted review/finding commands.",
            "Preserve finding IDs and unresolved concerns",
            "Historical records remain unchanged archives",
            "Saving does not settle workflow",
            "Material findings must include:",
            "For an isolated review with material findings",
            "the final review output must state:",
            "no automatic downstream handoff",
            "material Finding IDs",
            "required review record path",
            "whether the record must be created before fixing or reconstructed",
            "whether owner decision is needed",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, normalized)
        removed_terms = [
            "specs/rigorloop-workflow.md",
            "A tracked artifact is any version-controlled repository file whose",
            "Operational shortcut",
            "resolution-step gate",
            "review-driven edits",
            "`create-change-local-record-before-fixing`",
            "`reconstruct-record-because-fixes-already-began`",
            "`stop-for-owner-decision`",
            "The durable record should be created",
            "clean reviews can settle artifact-locally",
            "`not-required`: no material findings and no detailed-record trigger",
            "Use the formal review recording change-ID selection rule.",
            "clean receipt root",
            "review.status",
            "unresolved_items",
            "reviewed_artifact",
        ]
        for term in removed_terms:
            with self.subTest(removed_term=term):
                self.assertNotIn(term, normalized)

    def test_governance_guidance_uses_broad_material_finding_rule(self) -> None:
        constitution = (ROOT / "CONSTITUTION.md").read_text().lower()
        for term in ("whole-change code review", "material findings", "safe resolution path", "verify"):
            self.assertIn(term, constitution)
        agents = (ROOT / "AGENTS.md").read_text()
        self.assertIn("[Assessment](docs/design/skill/assessment.md)", agents)
        self.assertIn("[Records](docs/design/cli/records.md)", agents)
        self.assertIn("targeted recording", agents)
        self.assertIn("rigorloop-records-v3", (ROOT / "docs/design/cli/records.md").read_text())

    def test_downstream_skills_preserve_review_closeout_boundaries(self) -> None:
        for skill in DOWNSTREAM_REVIEW_CLOSEOUT_SKILLS:
            body = (ROOT / "skills" / skill / "SKILL.md").read_text()
            self.assertIn("review-reliance.md", body)
            relative = skill_validation.RECORDING_REFERENCES.get(skill)
            if relative is not None:
                body += (ROOT / "skills" / skill / relative).read_text()
            self.assertIn("does not approve", body)
            self.assertNotIn("review-log.md", body)

    def test_review_independence_m3_code_review_pilot_guidance(self) -> None:
        """Automated code-review guidance includes the blind-first independent gate pilot."""

        body = (
            ROOT
            / "skills"
            / "code-review"
            / "references"
            / "workflow-managed-automated-review.md"
        ).read_text(encoding="utf-8")
        required_terms = [
            "## Automated Independent Review Gate",
            "orchestrator-owned review invocation manifest",
            "neutral initial packet",
            "record an independent risk map before validation-result summaries, evidence menus, implementation notes, or prior finding content are released",
            "risk-map-recorded",
            "Evidence challenge happens only after the risk map",
            "Prior finding reconciliation happens only after the blind-first pass",
            "Clean automated reviews require a clean-review sufficiency receipt",
            "A clean automated review may advance only when the manifest, phase receipts, clean receipt, risk-tier escalation, unresolved-finding, and second-review gates are satisfied",
            "A final holistic code review is required before `verify`",
            "Do not introduce a minimum-finding quota",
            "The reviewer must not edit the reviewed target during review.",
            "Direct or profile-off review behavior remains isolated and does not require automated-review manifests unless the result is used as a workflow-managed automated handoff gate.",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)
        for item in R5_FORBIDDEN_INITIAL_PACKET_ITEMS:
            with self.subTest(forbidden_initial_packet_item=item):
                self.assertIn(item, body)
        for category in R8D_RECONCILIATION_CATEGORIES:
            with self.subTest(reconciliation_category=category):
                self.assertIn(category, body)
        for phrase in R8D_FAILED_REMEDIATION_REQUIRED_PHRASES:
            with self.subTest(failed_remediation_phrase=phrase):
                self.assertIn(phrase, body)

    def test_review_independence_m3_workflow_and_implement_route_automated_gate(self) -> None:
        """Workflow and implement skills route automated code review through the independent gate."""

        required_by_skill = {
            "route": [
                "Route-managed automated `code-review` uses the independent adversarial review gate",
                "The orchestrator creates the neutral review invocation manifest and initial packet",
                "It must withhold validation-result summaries, evidence menus, implementation notes, and prior finding content until the required phase receipts allow release.",
                "A clean automated review may advance only after the normalized `review_gate_outcome`, independence manifest, phase receipts, clean receipt, risk-tier gates, unresolved-finding check, and second-review policy all pass.",
                "Before `verify`, require final holistic code-review evidence covering the complete final diff and cross-milestone interactions.",
            ],
            "implement": [
                "When handing workflow-managed implementation work to automated `code-review`, hand off to the independent adversarial review gate.",
                "Provide tracked artifacts, the actual diff, governing contracts, and neutral routing metadata.",
                "Do not expose auto-fix classification to review discovery; findings and verdict are recorded before fixability is classified.",
                "Before Phase C can enter `verify`, require final holistic code-review evidence for the complete cross-milestone diff.",
            ],
        }
        for skill_name, terms in required_by_skill.items():
            path = ROOT / "skills" / skill_name / "SKILL.md"
            if skill_name == "route":
                path = (
                    ROOT
                    / "skills"
                    / "route"
                    / "references"
                    / "bounded-workflow-automation.md"
                )
            elif skill_name == "implement":
                path = (
                    ROOT
                    / "skills"
                    / "implement"
                    / "references"
                    / "automated-review-correction.md"
                )
            body = path.read_text(encoding="utf-8")
            for term in terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)
        implement_body = (
            ROOT
            / "skills"
            / "implement"
            / "references"
            / "automated-review-correction.md"
        ).read_text(encoding="utf-8")
        for item in R5_FORBIDDEN_INITIAL_PACKET_ITEMS:
            with self.subTest(skill="implement", forbidden_initial_packet_item=item):
                self.assertIn(item, implement_body)

    def test_requirement_fidelity_m1_guidance_surfaces(self) -> None:
        """M1 public guidance teaches requirement-fidelity as an additive code-review pilot."""

        required_by_skill = {
            "code-review-reference": [
                "## Requirement-Fidelity Gate",
                "Requirement fidelity is a sibling gate to independent review: independence reduces anchoring, while fidelity checks the complete normative spec projection.",
                "For workflow-managed automated `code-review`, use the requirement-fidelity gate when the applicability manifest says `applicable`.",
                "Start from the relevant spec clause before comparing implementation text, validator assertions, validation evidence, or prior findings.",
                "Decompose each relevant spec clause into requirement properties before artifact comparison unless accepted decomposition evidence already exists.",
                "For multi-surface contracts, check every requirement property on every required surface; a global substring match is insufficient.",
                "Applicable clean automated reviews require a requirement-fidelity receipt.",
                "A clean automated review may advance only when both the independent-review gate and the requirement-fidelity gate pass when both apply.",
                "Requirement compression is a material finding when an implementation, validator, skill, workflow, schema, fixture, generated output, or review-recording surface omits a required property.",
                "Do not introduce a minimum-finding quota.",
                "Direct or profile-off review behavior remains isolated and does not require requirement-fidelity manifests unless the result is used as a workflow-managed automated handoff gate.",
            ],
            "route": [
                "Route-managed automated `code-review` uses the requirement-fidelity gate when deterministic applicability is `applicable`.",
                "The requirement-fidelity gate is additive with the independent adversarial review gate; both receipts must pass when both contracts apply.",
                "Requirement-fidelity review starts from the relevant spec clause, then decomposition, expected surfaces, implementation diff, validator assertions, validation evidence, and prior findings.",
            ],
            "implement": [
                "When handing workflow-managed implementation work to automated `code-review`, include neutral routing metadata for requirement-fidelity applicability.",
                "Do not present implementation and validator agreement as sufficient proof of spec fidelity.",
                "When both contracts apply, downstream continuation requires both the independent-review receipt and the requirement-fidelity receipt.",
            ],
        }
        for skill_name, terms in required_by_skill.items():
            if skill_name == "code-review-reference":
                path = (
                    ROOT
                    / "skills"
                    / "code-review"
                    / "references"
                    / "workflow-managed-automated-review.md"
                )
            elif skill_name == "route":
                path = (
                    ROOT
                    / "skills"
                    / "route"
                    / "references"
                    / "bounded-workflow-automation.md"
                )
            elif skill_name == "implement":
                path = (
                    ROOT
                    / "skills"
                    / "implement"
                    / "references"
                    / "automated-review-correction.md"
                )
            else:
                path = ROOT / "skills" / skill_name / "SKILL.md"
            body = path.read_text(encoding="utf-8")
            for term in terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

    def test_implement_simplification_m2_package_contract(self) -> None:
        """M2 keeps universal implementation policy inline and splits conditional procedure."""

        root = ROOT / "skills" / "implement"
        body = (root / "SKILL.md").read_text(encoding="utf-8")
        planned = (
            root / "references" / "planned-milestone-implementation.md"
        ).read_text(encoding="utf-8")
        automation = (
            root / "references" / "automated-review-correction.md"
        ).read_text(encoding="utf-8")
        result = (
            root / "assets" / "implementation-result-skeleton.md"
        ).read_text(encoding="utf-8")

        planned_mapping = (
            "- READ `references/planned-milestone-implementation.md` when "
            "authoritative workflow evidence establishes a current planned milestone "
            "owned by `implement`."
        )
        automation_mapping = (
            "- READ `references/automated-review-correction.md` only when durable "
            "workflow evidence formally arms automated review or correction for that "
            "same current change and milestone."
        )
        result_mapping = (
            "- COPY `assets/implementation-result-skeleton.md` when producing the "
            "implementation result."
        )
        self.assertEqual(body.count(planned_mapping), 1)
        self.assertEqual(body.count(automation_mapping), 1)
        self.assertEqual(body.count(result_mapping), 1)

        for heading in (
            "## Workflow role",
            "## Scope and inputs",
            "## Invocation classification",
            "## Recording boundary",
            "## First-pass completeness",
            "## Implementation contract",
            "## Operating sequence",
            "## Stop conditions",
            "## Claims this skill must not make",
            "## Resource map",
            "## Boundary-first method",
            "## Expected output",
        ):
            with self.subTest(inline_heading=heading):
                self.assertIn(heading, body)

        for term in (
            "`IP0-isolated`",
            "`IP1-planned`",
            "`IP2-planned-armed`",
            "Armed automation without a valid planned milestone is invalid",
            "Conversational wording alone establishes neither predicate",
            "Missing, stale, mismatched, contradictory, or ambiguous evidence stops before conditional procedure is loaded or implementation state is mutated.",
        ):
            with self.subTest(profile_contract=term):
                self.assertIn(term, body)

        for heading in (
            "## Load conditions",
            "## Milestone authority and inspection",
            "## Baseline change pack",
            "## Milestone execution and validation",
            "## Commit and review handoff",
            "## Accepted correction return",
        ):
            with self.subTest(planned_heading=heading):
                self.assertIn(heading, planned)

        for heading in (
            "## Load conditions",
            "## Armed authority",
            "## Independent review packet",
            "## Requirement-fidelity routing",
            "## Correction and rereview",
            "## Promotion and pause",
        ):
            with self.subTest(automation_heading=heading):
                self.assertIn(heading, automation)

        for forbidden_policy in (
            "## First-pass completeness",
            "## Stop conditions",
            "## Claims this skill must not make",
        ):
            with self.subTest(reference="planned", forbidden=forbidden_policy):
                self.assertNotIn(forbidden_policy, planned)
            with self.subTest(reference="automation", forbidden=forbidden_policy):
                self.assertNotIn(forbidden_policy, automation)

        for heading in (
            "## Core result",
            "## Planned milestone",
            "## Armed automation",
        ):
            with self.subTest(result_group=heading):
                self.assertIn(heading, result)
        for policy_term in (
            "what status means",
            "when correction is allowed",
            "when review-requested is legal",
            "what readiness may be claimed",
        ):
            with self.subTest(asset_policy=policy_term):
                self.assertNotIn(policy_term, result.lower())

        self.assertNotIn("## Result\n\n- Skill: implement", body)
        self.assertNotIn("## Implementation summary", body)
        self.assertIn(
            "Armed implementation automation is valid only inside a current planned workflow-managed milestone.",
            automation,
        )

    def test_milestone_aware_guidance_removes_unconditional_verify_handoff(self) -> None:
        """Docs and skills must not retain stale unconditional clean-review-to-verify shortcuts."""

        stale_terms = [
            "first-pass `clean-with-notes` continues to `verify`",
            "`clean-with-notes` hands off to `verify` when no stop condition applies",
            "`code-review -> verify` only for first-pass `clean-with-notes`",
            "hands off to `verify` only when no in-scope implementation milestone remains open or unresolved",
            "Milestones are not postponed to make `verify` available",
            "Do not hand off to `verify` until all in-scope implementation milestones are `closed`",
        ]
        paths = [
            "skills/code-review/SKILL.md",
            "skills/route/SKILL.md",
        ]
        for relative_path in paths:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in stale_terms:
                with self.subTest(path=relative_path, term=term):
                    self.assertNotIn(term, body)

    def test_code_review_and_verify_public_skills_use_current_final_closeout_order(self) -> None:
        """Current review and Verify route directly through success-owned rationale."""

        code_review_paths = iter_published_skill_surfaces_for("code-review")
        self.assertTrue(code_review_paths, "expected published code-review skill surfaces")
        for path in code_review_paths:
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in CODE_REVIEW_FORBIDDEN_FINAL_CLOSEOUT_PATTERNS.items():
                with self.subTest(path=str(relative_path), forbidden=label):
                    self.assertIsNone(pattern.search(body))
            for term in ["final closeout", "final explanation", "verify", "PR"]:
                with self.subTest(path=str(relative_path), required=term):
                    self.assertIn(term, body)

        verify_paths = iter_published_skill_surfaces_for("verify")
        self.assertTrue(verify_paths, "expected published verify skill surfaces")
        for path in verify_paths:
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in VERIFY_FORBIDDEN_EXPLAIN_ORDER_PATTERNS.items():
                with self.subTest(path=str(relative_path), forbidden=label):
                    self.assertIsNone(pattern.search(body))
            for term in [
                "final explanation only after successful final readiness",
                "before PR",
                "validates the reviewed final change pack",
                "hands off to `pr`",
            ]:
                with self.subTest(path=str(relative_path), required=term):
                    self.assertIn(term, body)

    def test_skill_contract_current_skill_inventory(self) -> None:
        self.assertTrue((ROOT / "skills/ci-maintenance/SKILL.md").is_file())
        for name in [*SKILL_CONTRACT_FORBIDDEN_NEW_SKILLS, "token-budget"]:
            with self.subTest(skill=name):
                self.assertFalse((ROOT / "skills" / name / "SKILL.md").exists())

    def test_skill_contract_m2_shared_block_sources_exist_and_stay_bounded(self) -> None:
        shared_blocks = {
            "review-isolation-and-recording": SHARED_REVIEW_BLOCK_PATH,
            "evidence-collection-efficiency": SKILL_CONTRACT_EVIDENCE_BLOCK,
        }
        for block_name, path in shared_blocks.items():
            with self.subTest(block=block_name):
                self.assertTrue(path.exists(), f"missing shared block source: {path}")

        evidence_block = SKILL_CONTRACT_EVIDENCE_BLOCK.read_text(encoding="utf-8")
        review_block = SHARED_REVIEW_BLOCK_PATH.read_text(encoding="utf-8")

        evidence_terms = [
            "## Evidence collection efficiency",
            "Use bounded evidence before broad reads or raw excerpts.",
            "Use summary and stable-ID first reasoning before broad reads or raw excerpts.",
            "Prefer check IDs, requirement IDs, test IDs, file paths, counts, line citations",
            "generated output, validation logs, or repeated scans",
            "Output caps are safety rails, not evidence-selection strategy.",
            "Validation summaries must not change selected check coverage, command exit behavior, failure detection, or required validation evidence.",
            "## When full-file read is required",
            "Read the full file when the whole file is the review target",
            "bounded searches disagree or produce incomplete evidence",
        ]
        for term in evidence_terms:
            with self.subTest(block="evidence", term=term):
                self.assertIn(term, evidence_block)

        self.assertFalse(
            (ROOT / "templates" / "shared" / "generated-output-handling.md").exists(),
            "generated-output handling is contributor-maintenance guidance, not an adopted shared block",
        )

        self.assertIn(
            "Every formal lifecycle review result must be recorded or explicitly blocked.",
            review_block,
        )
        for block_name in SKILL_CONTRACT_DEFERRED_SHARED_BLOCKS:
            with self.subTest(deferred_block=block_name):
                self.assertFalse((ROOT / "templates" / "shared" / f"{block_name}.md").exists())

    def test_progressive_loading_quick_guide_contract_helper_detects_required_shape(self) -> None:
        valid_skill = """# Skill

## Quick operating guide

Use this skill to: route work from the shortest safe operating path.

Read first:
- active plan

Produce:
- reviewed route

Stop when:
- state is missing

Do not claim:
- downstream readiness

Next stage:
- test-spec

## When full-file read is required

Use a full-file or broader-section read when correctness requires surrounding context.
"""
        assert_progressive_loading_quick_guide_contract(self, valid_skill)

        missing_label = valid_skill.replace("Next stage:\n- test-spec\n", "")
        with self.assertRaises(AssertionError):
            assert_progressive_loading_quick_guide_contract(self, missing_label)

    def test_progressive_loading_code_review_protected_contract_helper_detects_safety_regression(self) -> None:
        valid_skill = """# Code Review

Keep independent-review mode, mixed-evidence handling, material finding requirements,
first-pass status vocabulary, severity vocabulary, isolation and recording rules,
detailed review record triggers, milestone-aware review handoff, stop conditions,
and result format.
"""
        assert_progressive_loading_code_review_protected_contracts(self, valid_skill)

        missing_material_findings = valid_skill.replace("material finding requirements,\n", "")
        with self.assertRaises(AssertionError):
            assert_progressive_loading_code_review_protected_contracts(self, missing_material_findings)

        split_template = valid_skill + "\nUse references/clean-review-template.md for the clean review template.\n"
        with self.assertRaises(AssertionError):
            assert_progressive_loading_code_review_protected_contracts(self, split_template)

    def test_progressive_loading_canonical_skills_satisfy_quick_guide_contract(self) -> None:
        for skill_name in PROGRESSIVE_LOADING_OPTIMIZED_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                if skill_name in {"implement", "code-review"}:
                    # SKL-SR-31: the approved equivalent exposes core work before
                    # conditional recording; other skills keep the quick guide.
                    scope = "Scope and inputs" if skill_name == "implement" else "Scope"
                    for heading in ("Workflow role", scope, "Invocation classification", "Operating sequence", "Stop conditions", "Resource map", "Expected output"):
                        self.assertTrue(extract_markdown_block(body, heading).strip())
                    self.assertLess(body.index("## " + scope), body.index("## Recording boundary"))
                    self.assertNotIn("## Explicit recording", body)
                else:
                    assert_progressive_loading_quick_guide_contract(self, body)

    def test_progressive_loading_canonical_code_review_preserves_protected_contracts(self) -> None:
        body = (ROOT / "skills" / "code-review" / "SKILL.md").read_text(encoding="utf-8")
        body += (ROOT / "skills/code-review/references/governed-code-review-recording.md").read_text()
        assert_progressive_loading_code_review_protected_contracts(self, body)

    def test_proposal_scope_preservation_guidance_is_static_validated(self) -> None:
        proposal = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal += "\n" + (ROOT / "skills" / "proposal" / "references" / "strategic-and-scope-gates.md").read_text(encoding="utf-8")
        proposal += "\n" + (ROOT / "skills" / "proposal" / "assets" / "proposal-skeleton.md").read_text(encoding="utf-8")
        proposal_review = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
        ).read_text(encoding="utf-8")

        proposal_terms = [
            "## Scope preservation",
            "Before drafting or materially revising a proposal, extract the user's initial goals, concerns, constraints, and requested outcomes.",
            "Keep each material goal visible in `Goals`, `Scope and non-goals`, or the requested decision.",
            "Closed enum: initial goal treatment",
            "summarize its destination inside `Scope and non-goals`",
            "Do not silently drop a user goal when narrowing a proposal; state intentional narrowing and its reason.",
        ]
        for term in proposal_terms:
            with self.subTest(skill="proposal", term=term):
                self.assertIn(term, proposal)

        proposal_review_terms = [
            "## Scope preservation review",
            "Compare the user's initial request with the proposal.",
            "Each material goal must remain visible in goals, scope, or the requested decision.",
            "an initial goal disappears, a deferred goal has no follow-up, a rejected goal has no rationale, or scope narrows without explanation",
            "Under adopted Review and Closeout policy, use the packaged combined-condition rule",
            "In a project that has not adopted that policy, these scope-preservation failures require `changes-requested`",
            "review status: `approved`, `changes-requested`, `blocked`, or `inconclusive`",
            "scope-preservation result",
            "Do not rewrite the proposal as part of proposal-review unless the user explicitly asks.",
        ]
        for term in proposal_review_terms:
            with self.subTest(skill="proposal-review", term=term):
                self.assertIn(term, proposal_review)

    def test_cost_bounded_rigor_m1_proposal_scope_budget_guidance(self) -> None:
        proposal = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal += "\n" + (ROOT / "skills" / "proposal" / "references" / "strategic-and-scope-gates.md").read_text(encoding="utf-8")
        proposal += "\n" + (ROOT / "skills" / "proposal" / "assets" / "proposal-skeleton.md").read_text(encoding="utf-8")

        required_terms = [
            "## Scope budget for broad proposals",
            "Scope-budget applicability is proposal/proposal-review judgment in this first slice, not mechanical validator inference.",
            "the user request contains two or more independent work items",
            "the change touches more than one lifecycle family",
            "the change could reasonably require more than one spec or implementation plan",
            "release policy, workflow policy, generated output, public skill behavior, or validation policy",
            "`proposal-review` identifies silent narrowing, hidden follow-up risk, or multi-workstream scope",
            "Small single-decision proposals may omit the scope budget.",
            "Closed enum: scope budget treatment",
            "keep the result inside `Scope and non-goals` rather than adding a level-two section.",
            "Route deferred work through the follow-up ownership model rather than chat-only notes or `project-map` ownership.",
            "route selects semantic ownership, `project-map` orients when present, action-owning artifacts track current work, and unowned cross-change follow-ups use the follow-up ownership surface.",
            "Do not search generated adapter output for authored skill truth.",
            "Do not add generated public adapter skill bodies back to tracked source.",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, proposal)

    def test_cost_bounded_rigor_m1_proposal_review_scope_budget_guidance(self) -> None:
        proposal_review = (
            ROOT / "skills" / "proposal-review" / "references" / "conditional-proposal-gates.md"
        ).read_text(encoding="utf-8")

        required_terms = [
            "## Scope-budget review",
            "Scope-budget applicability is proposal/proposal-review judgment, not validator inference.",
            "current scope, same-slice dependencies, separate implementation slices, deferable follow-ups, separate proposals, and out-of-scope work",
            "Return `changes-requested` when a broad or multi-workstream proposal lacks required scope-budget classification.",
            "Return `changes-requested` when the proposal hides follow-up work, silently narrows a user request, leaves a treatment or reason blank, omits follow-up routing, or uses a misleading treatment value.",
            "Small single-decision proposals may omit a scope budget when omission does not create silent narrowing, hidden follow-up risk, or multi-workstream ambiguity.",
            "Do not request a scope budget solely as routine ceremony.",
            "Accept non-standard treatment values only when they are clear and create no downstream ambiguity.",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, proposal_review)

    def test_stage_evidence_access_proposal_side_skills(self) -> None:
        skill_terms = {
            "proposal": [
                "## Evidence access",
                "Default evidence:",
                "user request",
                "`VISION.md` when proposal fit matters",
                "`CONSTITUTION.md` for governance, source-of-truth, workflow, or release-policy changes",
                "related proposal only when superseding or extending it",
                "Conditional evidence:",
                "`docs/project-map.md` when architecture or repository orientation matters",
                "existing specs or ADRs when the proposal changes their direction",
                "authoritative CLI workflow context when governed artifact placement or workflow routing matters",
                "code only when current behavior is part of the decision",
                "Record a compact reason only when reading substantive evidence outside the default and triggered conditional set.",
            ],
            "proposal-review": [
                "## Evidence access",
                "Default evidence:",
                "proposal under review",
                "user's original request or initial intent",
                "`VISION.md` or `CONSTITUTION.md` when standing gates or vision fit matter",
                "Conditional evidence:",
                "linked specs, ADRs, plans, or learn sessions when the proposal relies on them",
                "authoritative CLI workflow context when governed workflow behavior or artifact placement is proposed",
                "code only when the proposal depends on current implementation reality",
                "Record a compact reason only when reading substantive evidence outside the default and triggered conditional set.",
            ],
        }

        for skill_name, required_terms in skill_terms.items():
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

            with self.subTest(skill=skill_name, term="bounded discovery"):
                self.assertIn("Bounded discovery is not evidence expansion.", body)
            with self.subTest(skill=skill_name, term="full-file read"):
                self.assertIn("full-file", body)

    def test_skill_contract_m3_first_slice_core_sections_and_result_blocks(self) -> None:
        for skill_name in SKILL_CONTRACT_FIRST_SLICE_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name, surface="core_sections"):
                sections = SKILL_CONTRACT_REQUIRED_CORE_SECTIONS
                if skill_name in {"implement", "code-review"}:
                    # The pair consolidates generic headings only; result fields,
                    # stops, handoff and package semantics remain checked below.
                    sections = ("Workflow role", "Scope and inputs" if skill_name == "implement" else "Scope", "Invocation classification", "Operating sequence", "Handoff", "Stop conditions", "Expected output")
                for section in sections:
                    self.assertIn(f"## {section}", body)

            expected_output_start = body.find("## Expected output")
            self.assertNotEqual(
                expected_output_start,
                -1,
                msg=f"{skill_name} must preserve the validator-required Expected output section",
            )
            expected_output = body[expected_output_start:]
            with self.subTest(skill=skill_name, surface="result_block"):
                result_surface = expected_output
                if skill_name == "code-review":
                    result_surface = (
                        ROOT
                        / "skills"
                        / "code-review"
                        / "assets"
                        / "review-result-skeleton.md"
                    ).read_text(encoding="utf-8")
                elif skill_name == "implement":
                    result_surface = (
                        ROOT
                        / "skills"
                        / "implement"
                        / "assets"
                        / "implementation-result-skeleton.md"
                    ).read_text(encoding="utf-8")
                self.assertIn("## Result", result_surface)
                for field in SKILL_CONTRACT_RESULT_FIELDS:
                    self.assertIn(f"- {field}:", result_surface)

            handoff = extract_markdown_block(body, "Handoff")
            with self.subTest(skill=skill_name, surface="handoff"):
                self.assertTrue("workflow" in handoff or "`route`" in handoff)
                self.assertNotIn("specs/rigorloop-workflow.md", handoff)
                self.assertIn("Normal next stage", handoff)
                self.assertIn("Conditional next stages", handoff)

    def test_skill_contract_m3_claim_boundaries_and_readiness_terms(self) -> None:
        for skill_name, required_terms in SKILL_CONTRACT_CLAIM_BOUNDARY_TERMS.items():
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            claims = extract_markdown_block(body, "Claims this skill must not make")
            for term in required_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, claims)

        progress_terms = [
            "Progress means work that has happened so far.",
            "Readiness means the next stage that can happen.",
            "Closeout means the current artifact or stage satisfied its checklist.",
            "Done means final lifecycle state after required gates are complete.",
            "Readiness is not Done.",
        ]
        for skill_name in SKILL_CONTRACT_PROGRESS_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in progress_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

    def test_skill_contract_m3_first_slice_copies_shared_blocks(self) -> None:
        evidence = extract_markdown_block(
            SKILL_CONTRACT_EVIDENCE_BLOCK.read_text(encoding="utf-8"),
            "Evidence collection efficiency",
        )
        for skill_name in SKILL_CONTRACT_FIRST_SLICE_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name, block="evidence"):
                self.assertEqual(extract_markdown_block(body, "Evidence collection efficiency"), evidence)

            with self.subTest(skill=skill_name, block="generated"):
                self.assertNotIn("## Generated-output handling", body)

    def test_skill_contract_m3_public_skills_exclude_maintainer_details(self) -> None:
        forbidden_terms = [
            "specs/rigorloop-workflow.md",
            "skills/<skill>/SKILL.md",
            ".codex/skills",
            "dist/adapters",
            "selector-driven validation",
            "do not pass `--path dist/adapters`",
            "Generated-output handling",
            "Regenerate generated outputs",
            "Validate drift with repository-owned checks",
            "Shared blocks are copied into skills",
            "shared-block implementation details",
        ]
        for skill_name in SKILL_CONTRACT_FIRST_SLICE_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in forbidden_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertNotIn(term, body)

    def test_workflow_change_root_creation_uses_dated_change_id_convention(self) -> None:
        route_skill = (ROOT / "skills" / "route" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        implement_skill = (ROOT / "skills" / "implement" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        for term in [
            "For governed routing, use factual `rigorloop workflow-context` discovery",
            "For a missing formal change root in portable mode, use `YYYY-MM-DD-slug`.",
        ]:
            with self.subTest(surface="skills/route/SKILL.md", term=term):
                self.assertIn(term, route_skill)

        for term in [
            "When creating a root in governed mode, use the CLI-resolved location.",
            "In portable mode, use `YYYY-MM-DD-slug` without claiming governed placement.",
        ]:
            with self.subTest(surface="skills/implement/SKILL.md", term=term):
                self.assertIn(term, implement_skill)
