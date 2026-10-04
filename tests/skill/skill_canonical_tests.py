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
            "RR input to `requirement-analysis`",
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
            "receiving owner decides",
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
