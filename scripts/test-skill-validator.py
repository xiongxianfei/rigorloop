#!/usr/bin/env python3
"""Fixture-driven tests for the first-release skill validator."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-skills.py"
FIXTURES = ROOT / "tests" / "fixtures" / "skills"
SCAN_SENSITIVE_SKILLS = [
    "architecture",
    "architecture-review",
    "bugfix",
    "ci",
    "code-review",
    "explain-change",
    "implement",
    "plan",
    "plan-review",
    "pr",
    "project-map",
    "proposal",
    "proposal-review",
    "research",
    "spec",
    "spec-review",
    "test-spec",
    "verify",
    "vision",
    "workflow",
]
FORMAL_REVIEW_SKILLS = [
    "proposal-review",
    "spec-review",
    "architecture-review",
    "plan-review",
    "code-review",
]
DOWNSTREAM_REVIEW_CLOSEOUT_SKILLS = [
    "workflow",
    "verify",
    "explain-change",
    "pr",
]
PR_SELF_CONTAINED_LIFECYCLE_SKILLS = [
    "workflow",
    "plan",
    "implement",
    "verify",
    "explain-change",
    "pr",
]
MILESTONE_AWARE_REVIEW_HANDOFF_SKILLS = [
    "workflow",
    "implement",
    "code-review",
    "plan",
]
SHARED_REVIEW_BLOCK_PATH = ROOT / "templates" / "shared" / "review-isolation-and-recording.md"
MILESTONE_AWARE_REVIEW_HANDOFF_SPEC = ROOT / "specs" / "milestone-aware-review-handoff.md"
MILESTONE_AWARE_REVIEW_HANDOFF_TEST_SPEC = (
    ROOT / "specs" / "milestone-aware-review-handoff.test.md"
)
SKILL_CONTRACT_SPEC = ROOT / "specs" / "skill-contract.md"
SKILL_CONTRACT_TEST_SPEC = ROOT / "specs" / "skill-contract.test.md"
SKILL_CONTRACT_PLAN = ROOT / "docs" / "plans" / "2026-05-08-skill-contract-optimization.md"
SKILL_CONTRACT_FIRST_SLICE_SKILLS = [
    "workflow",
    "plan",
    "implement",
    "code-review",
    "verify",
    "pr",
    "learn",
]
SKILL_CONTRACT_FORBIDDEN_NEW_SKILLS = [
    "ci-maintenance",
    "review-resolution",
    "ui-design",
    "ui-design-review",
    "workflow-contract",
    "adopt-rigorloop",
]


def extract_markdown_block(text: str, heading: str) -> str:
    start_marker = f"## {heading}"
    start = text.find(start_marker)
    if start == -1:
        raise AssertionError(f"missing heading: {start_marker}")
    next_heading = text.find("\n## ", start + len(start_marker))
    if next_heading == -1:
        return text[start:].rstrip() + "\n"
    return text[start:next_heading].rstrip() + "\n"


def run_validator(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(target)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


class SkillValidatorFixtureTests(unittest.TestCase):
    maxDiff = None

    def assertFixturePasses(self, relative_path: str) -> None:
        result = run_validator(FIXTURES / relative_path)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected fixture '{relative_path}' to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def assertFixtureFails(self, relative_path: str, expected_text: str) -> None:
        result = run_validator(FIXTURES / relative_path)
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"expected fixture '{relative_path}' to fail",
        )
        self.assertIn(expected_text, combined_output)

    def test_valid_skill_passes(self) -> None:
        self.assertFixturePasses("valid-basic")

    def test_missing_name_fails(self) -> None:
        self.assertFixtureFails("missing-name", "name: missing required field")

    def test_missing_description_fails(self) -> None:
        self.assertFixtureFails("missing-description", "description: missing required field")

    def test_missing_title_fails(self) -> None:
        self.assertFixtureFails("missing-title", "expected exactly one top-level # title")

    def test_missing_expected_output_fails(self) -> None:
        self.assertFixtureFails(
            "missing-expected-output", "missing required '## Expected output' section"
        )

    def test_missing_skill_file_fails(self) -> None:
        self.assertFixtureFails(
            "missing-skill-file", "empty-skill/SKILL.md: missing required skill file"
        )

    def test_duplicate_name_fails(self) -> None:
        self.assertFixtureFails("duplicate-name", "duplicate skill name: duplicate-name")

    def test_placeholder_text_fails(self) -> None:
        self.assertFixtureFails("placeholder-text", "placeholder text is not allowed")

    def test_generated_output_path_is_rejected(self) -> None:
        result = run_validator(ROOT / ".codex" / "skills")
        combined_output = f"{result.stdout}\n{result.stderr}"
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("generated output path must not be used as authored source of truth", combined_output)

    def test_workflow_guidance_defines_bounded_extraction_and_output_budgets(self) -> None:
        workflow_text = (ROOT / "docs" / "workflows.md").read_text(encoding="utf-8")
        required_terms = [
            "bounded extraction",
            "stable IDs",
            "matching line numbers",
            "exact ranges",
            "full-file read",
            "routine command output target: 40 lines",
            "routine command output warning threshold: 80 lines",
            "single excerpt target: 12 lines",
            "single excerpt warning threshold: 20 lines",
            "one summary line per file",
            "--verbose",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, workflow_text)

    def test_scan_sensitive_skills_include_summary_id_reasoning_and_full_file_rules(self) -> None:
        for skill_name in SCAN_SENSITIVE_SKILLS:
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            body = skill_path.read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                self.assertIn("summary and stable-ID first", body)
                self.assertIn("check IDs", body)
                self.assertIn("requirement IDs", body)
                self.assertIn("file paths", body)
                self.assertIn("line citations", body)
                self.assertIn("When full-file read is required", body)
                self.assertIn("the whole file is the review target", body)
                self.assertIn("bounded searches disagree", body)
                self.assertIn("behavior-changing edit depends on the whole source-of-truth artifact", body)

    def test_architecture_skill_defines_concise_c4_arc42_adr_output_shape(self) -> None:
        body = (ROOT / "skills" / "architecture" / "SKILL.md").read_text(encoding="utf-8")
        required_terms = [
            "## When to Use / When Not to Use",
            "## Output Shape",
            "Produce or update:",
            "`docs/changes/<change-id>/architecture.md`",
            "canonical architecture package",
            "C4 system context diagram",
            "C4 container diagram",
            "ADRs when durable decisions are introduced",
            "Use `templates/architecture.md` for the full 12-section arc42 structure.",
            "```mermaid\nC4Context",
            "```mermaid\nC4Container",
            "## ADR Triggers",
            "skills/architecture/references/architecture-example.md",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

        forbidden_terms = [
            "## Full Worked Example",
            "### Full Worked Example",
            "## Worked Example",
            "### Worked Example",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, body)

    def test_architecture_review_skill_preserves_simple_finding_and_material_contract(self) -> None:
        body = (ROOT / "skills" / "architecture-review" / "SKILL.md").read_text(encoding="utf-8")
        required_terms = [
            "embedded or duplicated diagram source",
            "generic non-C4 flowchart",
            "wrong C4 level",
            "missing C4 role classes",
            "missing technology labels where relevant",
            "unlabeled relationships",
            "flat Building Block View",
            "duplicated ADR rationale",
            "weak quality-scenario content",
            "Deployment View repeats source layout",
            "Finding:",
            "Location:",
            "Severity:",
            "Recommendation:",
            "`blocker`, `material`, or `minor`",
            "Do not require mandatory C4-level classification",
            "does not replace the repository-wide material-finding contract",
            "evidence, required outcome, and a safe resolution path or `needs-decision` rationale",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

    def test_vision_skill_defines_state_based_boundaries_and_readme_marker_contract(self) -> None:
        body = (ROOT / "skills" / "vision" / "SKILL.md").read_text(encoding="utf-8")
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
        body = (ROOT / "skills" / "vision" / "SKILL.md").read_text(encoding="utf-8")
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
        body = (ROOT / "skills" / "vision" / "SKILL.md").read_text(encoding="utf-8")

        workflow_index = body.index("## Workflow Fit")
        inputs_index = body.index("## Inputs To Read")
        state_index = body.index("## State-Based Behavior")
        vision_content_index = body.index("## Vision Content")
        drafting_index = body.index("## Drafting Heuristics")
        readme_index = body.index("## README Front-Matter")

        self.assertLess(workflow_index, inputs_index)
        self.assertLess(inputs_index, state_index)
        self.assertLess(state_index, vision_content_index)
        self.assertLess(vision_content_index, drafting_index)
        self.assertLess(drafting_index, readme_index)

        self.assertNotIn("| Mode |", body)
        self.assertNotIn("| `create` |", body)
        self.assertNotIn("| `revise` |", body)
        self.assertNotIn("| `mirror` |", body)

    def test_vision_skill_strategic_positioning_contract(self) -> None:
        body = (ROOT / "skills" / "vision" / "SKILL.md").read_text(encoding="utf-8")
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

    def test_proposal_skills_define_vision_fit_contract(self) -> None:
        proposal_body = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal_review_body = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
        ).read_text(encoding="utf-8")

        proposal_terms = [
            "`Vision fit`",
            "new or substantively revised proposals",
            "fits the current vision",
            "may conflict with the current vision",
            "proposes a vision revision",
            "no vision exists yet",
            "first non-empty line",
            "When root `VISION.md` does not exist, proposals must use the exact `Vision fit` value `no vision exists yet`.",
            "If root `VISION.md` exists, choose one of the current-vision outcomes",
            "Retired root `vision.md` must not prevent `no vision exists yet`",
            "must not silently redefine project vision",
            "Legacy proposals",
        ]
        for term in proposal_terms:
            with self.subTest(skill="proposal", term=term):
                self.assertIn(term, proposal_body)

        proposal_review_terms = [
            "Check the proposal's `Vision fit` section",
            "created or substantively revised after the vision spec was adopted",
            "request revision",
            "When root `VISION.md` does not exist, proposal-review must request revision if `Vision fit` is missing or replaced with a claim that fits, conflicts with, or revises a nonexistent vision.",
            "If root `VISION.md` exists, `Vision fit` must not say `no vision exists yet`.",
            "Retired root `vision.md` must not prevent `no vision exists yet`",
            "revise proposal",
            "revise vision",
            "record explicit exception",
            "approving owner or owning stage",
            "evidence for the conflict",
            "why proposal revision is not chosen",
            "why vision revision is not chosen",
            "where the exception is recorded",
            "one-time",
            "future vision-revision trigger",
            "`explain-change.md`",
        ]
        for term in proposal_review_terms:
            with self.subTest(skill="proposal-review", term=term):
                self.assertIn(term, proposal_review_body)

        forbidden_terms = [
            "migration-recognized legacy root `vision.md`",
            "During the `vision.md` to `VISION.md` migration",
            "has not yet replaced",
        ]
        for body, label in ((proposal_body, "proposal"), (proposal_review_body, "proposal-review")):
            for term in forbidden_terms:
                with self.subTest(skill=label, forbidden=term):
                    self.assertNotIn(term, body)

    def test_governance_workflow_and_readme_define_vision_source_of_truth(self) -> None:
        constitution = (ROOT / "CONSTITUTION.md").read_text(encoding="utf-8")
        self.assertIn("2. `VISION.md`", constitution)
        self.assertIn("3. `specs/`", constitution)
        self.assertIn("README front-matter", constitution)

        required_terms = [
            "`VISION.md` is the canonical project-vision artifact",
            "created or substantively revised after this spec is adopted include `Vision fit`",
            "README content between `<!-- vision:start -->` and `<!-- vision:end -->` is generated from `VISION.md`",
            "README front-matter is not the source of truth when it conflicts with `VISION.md`",
        ]
        for relative_path in ["AGENTS.md", "docs/workflows.md", "README.md"]:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(path=relative_path, term=term):
                    self.assertIn(term, body)

    def test_active_vision_spec_retires_lowercase_path_and_user_facing_modes(self) -> None:
        spec = (ROOT / "specs" / "vision-skill.md").read_text(encoding="utf-8")
        test_spec = (ROOT / "specs" / "vision-skill.test.md").read_text(encoding="utf-8")

        required_terms = [
            "`VISION.md`: the canonical project vision document at the repository root.",
            "state-based behavior",
            "establish project vision",
            "update vision",
            "sync README",
            "retired root `vision.md`",
            "no longer exposes `create`, `revise`, or `mirror` as user-facing modes",
            "strategic-positioning pass",
            "docs/vision/strategic-positioning.md",
            "methodology-as-product",
            "MUST NOT exceed 900 words",
        ]
        for term in required_terms:
            with self.subTest(file="spec", term=term):
                self.assertIn(term, spec)

        test_spec_terms = [
            "`R73`-`R79`",
            "`R80`-`R86`",
            "`AC11`",
            "`AC16`",
            "negative proof",
            "RigorLoop-style methodology",
            "Windows-native file manager",
            "Git extension",
        ]
        for term in test_spec_terms:
            with self.subTest(file="test_spec", term=term):
                self.assertIn(term, test_spec)

        forbidden_terms = [
            "MUST define exactly these operating modes",
            "Create mode MUST create",
            "Mirror mode MUST",
            "Revise mode MUST",
            "Every `vision` skill run MUST report the mode used",
            "mode used, files changed",
        ]
        for body, label in ((spec, "spec"), (test_spec, "test_spec")):
            for term in forbidden_terms:
                with self.subTest(file=label, term=term):
                    self.assertNotIn(term, body)

    def test_workflow_refactor_stage_skill_guidance_alignment(self) -> None:
        workflow = (ROOT / "skills" / "workflow" / "SKILL.md").read_text(encoding="utf-8")
        proposal = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal_review = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        ci = (ROOT / "skills" / "ci" / "SKILL.md").read_text(encoding="utf-8")
        learn = (ROOT / "skills" / "learn" / "SKILL.md").read_text(encoding="utf-8")
        verify = (ROOT / "skills" / "verify" / "SKILL.md").read_text(encoding="utf-8")

        workflow_terms = [
            "## Workflow Categories",
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
            "identify the bootstrap exception in `Vision fit`",
            "next mandatory or triggered downstream stage",
        ]
        for term in proposal_terms:
            with self.subTest(skill="proposal", term=term):
                self.assertIn(term, proposal)

        proposal_review_terms = [
            "Bootstrap proposals",
            "identify the bootstrap exception in `Vision fit`",
            "request revision if the bootstrap exception is missing",
            "standing artifact gate",
        ]
        for term in proposal_review_terms:
            with self.subTest(skill="proposal-review", term=term):
                self.assertIn(term, proposal_review)

        ci_terms = [
            "ci-maintenance",
            "CI infrastructure",
            "It does not run validation",
            "does not design tests",
            "does not specify validation commands",
            "does not wait for existing CI checks",
            "validation execution stays under `verify`",
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
            "next mandatory or triggered downstream stage",
            "ci-maintenance",
            "hosted workflow automation or related CI infrastructure",
        ]
        for term in verify_terms:
            with self.subTest(skill="verify", term=term):
                self.assertIn(term, verify)
        self.assertNotIn("next required or default downstream stage", verify)
        self.assertNotIn("downstream stage is `ci`", verify)

    def test_learn_skill_final_artifact_model_and_bounded_process(self) -> None:
        skill_body = (ROOT / "skills" / "learn" / "SKILL.md").read_text(encoding="utf-8")
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
            "repository-owned generators",
        ]
        for term in required_skill_terms:
            with self.subTest(file="learn skill", term=term):
                self.assertIn(term, skill_body)

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

    def test_formal_review_skills_define_detailed_record_triggers(self) -> None:
        required_terms = [
            "detailed review record triggers",
            "material findings",
            "stage-owned non-approval outcomes that block downstream progress or require revision",
            "reconstructed review evidence",
            "closeout evidence citation",
            "explicit reviewer or maintainer request",
            "clean reviews can settle artifact-locally",
            "no-material detailed records need `review-log.md` but not an empty `review-resolution.md`",
            "artifact-local settlement must not replace detailed review records when a trigger applies",
            "stable `Finding ID`",
            "disposition in `review-resolution.md`",
            "`pr-review`",
            "unsupported review stage",
        ]
        for skill_name in FORMAL_REVIEW_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

    def test_formal_review_skills_share_isolation_and_recording_block(self) -> None:
        self.assertTrue(
            SHARED_REVIEW_BLOCK_PATH.exists(),
            "templates/shared/review-isolation-and-recording.md must be the canonical shared block source",
        )
        canonical = extract_markdown_block(
            SHARED_REVIEW_BLOCK_PATH.read_text(encoding="utf-8"),
            "Isolation and Recording",
        )

        for skill_name in FORMAL_REVIEW_SKILLS:
            with self.subTest(skill=skill_name):
                body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
                copied = extract_markdown_block(body, "Isolation and Recording")
                self.assertEqual(copied, canonical)

        forbidden_inside_block = [
            "proposal-review",
            "spec-review",
            "architecture-review",
            "plan-review",
            "code-review",
            "code-review-specific",
        ]
        for term in forbidden_inside_block:
            with self.subTest(term=term):
                self.assertNotIn(term, canonical)

    def test_shared_isolation_and_recording_block_defines_broad_material_rule(self) -> None:
        canonical = extract_markdown_block(
            SHARED_REVIEW_BLOCK_PATH.read_text(encoding="utf-8"),
            "Isolation and Recording",
        )
        normalized = " ".join(canonical.split())
        required_terms = [
            "Isolation governs handoff. Recording follows material findings.",
            "A direct or review-only request remains isolated by default",
            "Isolation does not suppress recording.",
            "Every material finding requires a durable change-local review record",
            "`docs/changes/<change-id>/reviews/<stage>-r<n>.md`",
            "The review record must be indexed in `review-log.md` and resolved in `review-resolution.md`.",
            "Create the durable record before fixing.",
            "A material finding must include:",
            "evidence",
            "required outcome",
            "safe resolution path, or `needs-decision` rationale",
            "Clean reviews with no material findings remain lightweight",
            "do not require detailed review files",
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
        ]
        for term in removed_terms:
            with self.subTest(removed_term=term):
                self.assertNotIn(term, normalized)

    def test_governance_guidance_uses_broad_material_finding_rule(self) -> None:
        required_terms = [
            "Material review findings",
            "always",
            "All material findings require",
            "change-local review",
            "Isolation",
            "handoff",
            "not recording",
        ]
        for relative_path in ["CONSTITUTION.md", "AGENTS.md", "docs/workflows.md"]:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(path=relative_path, term=term):
                    self.assertIn(term, body)

    def test_downstream_skills_preserve_review_closeout_boundaries(self) -> None:
        required_terms = [
            "review-log.md",
            "Closeout status: open",
            "Closeout status: closed",
            "needs-decision",
            "stage-owned non-approval outcome",
            "same-stage later review round or explicit reviewer or owner closeout",
            "`review-resolution.md` alone is not a silent substitute",
            "no-material detailed records need `review-log.md` but not an empty `review-resolution.md`",
        ]
        for skill_name in DOWNSTREAM_REVIEW_CLOSEOUT_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

    def test_pr_self_contained_lifecycle_completion_skill_guidance(self) -> None:
        required_terms = [
            "before the PR opens for review",
            "true downstream completion event",
            "merge itself",
        ]
        forbidden_terms = [
            "Only merge-dependent `Done` transitions may wait",
            "immediate post-merge cleanup",
            "record why only a merge-dependent `Done` transition remains pending",
            "unless merged state is the deciding event",
        ]
        for skill_name in PR_SELF_CONTAINED_LIFECYCLE_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skill=skill_name, required=term):
                    self.assertIn(term, body)
            for term in forbidden_terms:
                with self.subTest(skill=skill_name, forbidden=term):
                    self.assertNotIn(term, body)

    def test_milestone_aware_review_handoff_test_spec_maps_static_proof(self) -> None:
        body = MILESTONE_AWARE_REVIEW_HANDOFF_TEST_SPEC.read_text(encoding="utf-8")
        required_terms = [
            "T1. Scope boundary preserves existing lanes and stop conditions",
            "T2. Clean review routing distinguishes non-final and final milestones",
            "T3. Findings stay attached to the reviewed milestone",
            "T4. Inconclusive or ambiguous review never hands off to verify",
            "T5. Milestone state vocabulary is single-field and exact",
            "T6. Implement handoff uses `review-requested` and does not claim verify readiness",
            "T7. Handoff summaries and plan update obligations are explicit",
            "T8. Milestones are not postponed to reach verify",
            "T9. Lifecycle-closeout milestones are distinguishable from implementation milestones",
            "T10. Affected workflow, skill, and generated surfaces remain aligned",
            "T11. First implementation slice stays static-only",
            "T12. Validation selector accepts concrete generated adapter paths",
            "T13. Handoff summaries do not expose sensitive data",
            "T14. Compatibility expectations remain true for existing plans",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

    def test_milestone_aware_review_handoff_single_state_contract(self) -> None:
        spec = MILESTONE_AWARE_REVIEW_HANDOFF_SPEC.read_text(encoding="utf-8")
        test_spec = MILESTONE_AWARE_REVIEW_HANDOFF_TEST_SPEC.read_text(encoding="utf-8")
        allowed_states = [
            "`planned`",
            "`implementing`",
            "`review-requested`",
            "`resolution-needed`",
            "`closed`",
        ]
        for body, label in ((spec, "spec"), (test_spec, "test spec")):
            for state in allowed_states:
                with self.subTest(file=label, state=state):
                    self.assertIn(state, body)

        self.assertIn(
            "`implementation-complete` and `review-clean` are evidence descriptions, not milestone states.",
            spec,
        )
        self.assertIn("`implementation-complete` and `review-clean` are not milestone state values.", test_spec)
        self.assertNotIn("routing state", spec)
        self.assertNotIn("implementation evidence state", spec)

    def test_milestone_aware_skill_guidance_for_state_and_handoff(self) -> None:
        """Skills describe milestone-aware state, handoff, and verify-readiness boundaries."""

        required_by_skill = {
            "implement": [
                "`planned` to `implementing`",
                "`review-requested`",
                "targeted validation evidence",
                "not set plan readiness to `Ready for verify`",
            ],
            "code-review": [
                "clean non-final milestone",
                "next in-scope implementation milestone",
                "clean final milestone",
                "`resolution-needed`",
                "current handoff summary",
            ],
            "plan": [
                "exactly one `Milestone state`",
                "`review-requested`",
                "`resolution-needed`",
                "current handoff summary",
                "`lifecycle-closeout`",
            ],
            "workflow": [
                "milestone-based",
                "remaining in-scope implementation milestones",
                "`lifecycle-closeout`",
                "verify readiness",
            ],
        }
        for skill_name, required_terms in required_by_skill.items():
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

    def test_milestone_aware_workflow_specs_remove_unconditional_verify_handoff(self) -> None:
        required_terms = [
            "milestone-based plan",
            "clean non-final implementation milestone",
            "next in-scope implementation milestone",
            "clean final implementation milestone",
            "all in-scope implementation milestones are closed",
            "lifecycle-closeout milestone",
            "review-requested",
            "resolution-needed",
        ]
        for relative_path in [
            "specs/workflow-stage-autoprogression.md",
            "specs/rigorloop-workflow.md",
        ]:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(path=relative_path, required=term):
                    self.assertIn(term, body)

        stale_terms = [
            "once `code-review` is satisfied and no accepted findings remain unresolved, the workflow MUST continue into `verify` unless a stop condition applies",
        ]
        for relative_path in [
            "specs/workflow-stage-autoprogression.md",
            "specs/rigorloop-workflow.md",
        ]:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in stale_terms:
                with self.subTest(path=relative_path, stale=term):
                    self.assertNotIn(term, body)

    def test_milestone_aware_guidance_removes_unconditional_verify_handoff(self) -> None:
        """Docs and skills must not retain stale unconditional clean-review-to-verify shortcuts."""

        stale_terms = [
            "first-pass `clean-with-notes` continues to `verify`",
            "`clean-with-notes` hands off to `verify` when no stop condition applies",
            "`code-review -> verify` only for first-pass `clean-with-notes`",
        ]
        paths = [
            "docs/workflows.md",
            "skills/code-review/SKILL.md",
            "skills/workflow/SKILL.md",
        ]
        for relative_path in paths:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in stale_terms:
                with self.subTest(path=relative_path, term=term):
                    self.assertNotIn(term, body)

    def test_skill_contract_test_spec_maps_static_proof(self) -> None:
        body = SKILL_CONTRACT_TEST_SPEC.read_text(encoding="utf-8")
        required_terms = [
            "T1. Normative skill-contract source and workflow-routing split",
            "T2. Required and conditional sections are present without hollow normalization",
            "T3. First-slice and later-phase scope stay exact",
            "T4. Claim boundaries and do-not-overclaim guidance",
            "T5. Result blocks and handoff sections are summary-first and local",
            "T6. Progress, readiness, closeout, and Done stay distinct",
            "T7. Shared blocks are canonical copied text with drift checks",
            "T8. Evidence-reading and example guidance stay bounded",
            "T9. Generated output is refreshed from concrete canonical changes",
            "T10. Forbidden-overclaim validation is narrow and positive-first",
            "T11. Minimum viable skill rule and guidance placement",
            "T12. Compatibility, security, and non-goal boundaries",
            "T13. Full milestone and final validation closeout",
            "Do not test runtime workflow routing",
            "Do not test broad semantic quality of skill prose with natural-language scoring",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

        for requirement_number in range(1, 21):
            with self.subTest(requirement=requirement_number):
                self.assertIn(f"`R{requirement_number}", body)

        for example_number in range(1, 8):
            with self.subTest(example=example_number):
                self.assertIn(f"`E{example_number}`", body)

    def test_skill_contract_source_and_generated_boundaries_are_defined(self) -> None:
        spec = SKILL_CONTRACT_SPEC.read_text(encoding="utf-8")
        test_spec = SKILL_CONTRACT_TEST_SPEC.read_text(encoding="utf-8")
        required_spec_terms = [
            "This spec owns skill-contract behavior.",
            "`specs/rigorloop-workflow.md` continues to own stage order, stage obligation, handoff, and downstream-blocking semantics.",
            "Generated skill mirrors under `.codex/skills/` MUST be treated as derived output.",
            "Adapter output under `dist/adapters/` MUST be treated as derived output.",
            "Contributors MUST NOT hand-edit `.codex/skills/` or `dist/adapters/` to satisfy this spec.",
            "Shared blocks are copied and checked in v1, not generated into skills.",
            "The first validation slice MUST NOT add broad natural-language quality scoring.",
            "The `ci` skill remains the entrypoint for the `ci-maintenance` stage label.",
        ]
        for term in required_spec_terms:
            with self.subTest(file="spec", term=term):
                self.assertIn(term, spec)

        required_test_terms = [
            "Do not add runtime workflow simulation",
            "Do not add runtime workflow simulation, natural-language scoring, broad prose linting",
            "generated-output drift checks",
            "selector validation with concrete generated skill and adapter file paths",
            "do not pass `--path dist/adapters`",
        ]
        for term in required_test_terms:
            with self.subTest(file="test_spec", term=term):
                self.assertIn(term, test_spec)

    def test_skill_contract_first_slice_scope_stays_limited(self) -> None:
        spec = SKILL_CONTRACT_SPEC.read_text(encoding="utf-8")
        test_spec = SKILL_CONTRACT_TEST_SPEC.read_text(encoding="utf-8")
        plan = SKILL_CONTRACT_PLAN.read_text(encoding="utf-8")
        first_slice_test_spec_list = ", ".join(
            f"`{skill_name}`" for skill_name in SKILL_CONTRACT_FIRST_SLICE_SKILLS[:-1]
        )
        first_slice_test_spec_list = (
            f"{first_slice_test_spec_list}, and `{SKILL_CONTRACT_FIRST_SLICE_SKILLS[-1]}`"
        )

        self.assertIn(
            f"first implementation slice names only {first_slice_test_spec_list}",
            test_spec,
        )

        for skill_name in SKILL_CONTRACT_FIRST_SLICE_SKILLS:
            with self.subTest(surface="spec", skill=skill_name):
                self.assertIn(f"`skills/{skill_name}/SKILL.md`", spec)
            with self.subTest(surface="plan", skill=skill_name):
                self.assertIn(f"skills/{skill_name}/SKILL.md", plan)

        self.assertIn(
            "The `ci` skill MUST be treated as the skill entrypoint for the visible `ci-maintenance` workflow stage label",
            spec,
        )
        self.assertIn("The first implementation slice MUST NOT normalize every skill.", spec)
        self.assertIn("Do not implement Phase 2, Phase 3, or Phase 4 skill normalization", plan)
        self.assertTrue((ROOT / "skills" / "ci" / "SKILL.md").exists())

        for skill_name in SKILL_CONTRACT_FORBIDDEN_NEW_SKILLS:
            with self.subTest(forbidden_skill=skill_name):
                self.assertFalse((ROOT / "skills" / skill_name / "SKILL.md").exists())

    def test_skill_contract_plan_keeps_m1_scaffolding_passable_before_skill_edits(self) -> None:
        plan = SKILL_CONTRACT_PLAN.read_text(encoding="utf-8")
        required_terms = [
            "Validator assertions may be added in M1 only when they can pass without the later canonical skill edits",
            "Do not leave failing validator assertions committed as M1 closeout evidence.",
            "Generated-output checks are M4 closeout gates.",
            "If selector output reports generated drift after M3 canonical skill edits",
            "Use concrete generated adapter file paths in selector-driven commands; do not pass `--path dist/adapters`.",
            "dist/adapters/codex/.agents/skills/workflow/SKILL.md",
            "dist/adapters/claude/.claude/skills/workflow/SKILL.md",
            "dist/adapters/opencode/.opencode/skills/workflow/SKILL.md",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, plan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
