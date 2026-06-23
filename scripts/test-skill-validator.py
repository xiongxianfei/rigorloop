#!/usr/bin/env python3
"""Fixture-driven tests for the first-release skill validator."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import unittest
import math
import tempfile
import textwrap
from collections.abc import Callable
from pathlib import Path

import skill_validation


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-skills.py"
FIXTURES = ROOT / "tests" / "fixtures" / "skills"
SCAN_SENSITIVE_SKILLS = [
    "architecture",
    "architecture-review",
    "bugfix",
    "ci-maintenance",
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
DOWNSTREAM_STATUS_SETTLEMENT_FIRST_SLICE_SKILLS = [
    "spec",
    "architecture",
    "plan",
]
DOWNSTREAM_STATUS_SETTLEMENT_LATER_SLICE_SKILLS = [
    "test-spec",
    "implement",
    "explain-change",
    "verify",
    "pr",
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
FORMAL_REVIEW_RECORDING_SPEC = ROOT / "specs" / "formal-review-recording.md"
MILESTONE_AWARE_REVIEW_HANDOFF_SPEC = ROOT / "specs" / "milestone-aware-review-handoff.md"
MILESTONE_AWARE_REVIEW_HANDOFF_TEST_SPEC = (
    ROOT / "specs" / "milestone-aware-review-handoff.test.md"
)
SKILL_CONTRACT_SPEC = ROOT / "specs" / "skill-contract.md"
SKILL_CONTRACT_TEST_SPEC = ROOT / "specs" / "skill-contract.test.md"
SKILL_CONTRACT_PLAN = ROOT / "docs" / "plans" / "2026-05-08-skill-contract-optimization.md"
SINGLE_SOURCE_WORKFLOW_STATE_SPEC = ROOT / "specs" / "single-source-of-workflow-state.md"
SINGLE_SOURCE_WORKFLOW_STATE_TEST_SPEC = ROOT / "specs" / "single-source-of-workflow-state.test.md"
SINGLE_SOURCE_WORKFLOW_STATE_PLAN = (
    ROOT / "docs" / "plans" / "2026-05-09-single-source-of-workflow-state.md"
)
SKILL_CONTRACT_WORKFLOW_SPEC = ROOT / "specs" / "rigorloop-workflow.md"
SKILL_CONTRACT_WORKFLOWS_DOC = ROOT / "docs" / "workflows.md"
SKILL_CONTRACT_AGENTS = ROOT / "AGENTS.md"
SKILL_VALIDATOR_FIXTURE_README = ROOT / "docs" / "changes" / "0001-skill-validator" / "README.md"
SKILL_CONTRACT_EVIDENCE_BLOCK = ROOT / "templates" / "shared" / "evidence-collection-efficiency.md"
SKILL_CONTRACT_FIRST_SLICE_SKILLS = [
    "workflow",
    "plan",
    "implement",
    "code-review",
    "verify",
    "pr",
    "learn",
]
TOKEN_COST_SELECTED_SKILLS = [
    "proposal",
    "proposal-review",
    "spec",
    "spec-review",
    "plan",
    "plan-review",
    "implement",
    "code-review",
    "verify",
    "pr",
    "learn",
]
PROGRESSIVE_LOADING_OPTIMIZED_SKILLS = [
    "workflow",
    "implement",
    "code-review",
]
PROGRESSIVE_LOADING_QUICK_GUIDE_LABELS = [
    "Use this skill to:",
    "Read first:",
    "Produce:",
    "Stop when:",
    "Do not claim:",
    "Next stage:",
]
PROGRESSIVE_LOADING_CODE_REVIEW_PROTECTED_TERMS = [
    "independent-review",
    "mixed-evidence",
    "material finding",
    "first-pass status",
    "severity",
    "isolation",
    "detailed review record",
    "milestone-aware",
    "stop conditions",
    "result format",
]
CUSTOMER_PORTABLE_FIRST_SLICE_SKILLS = [
    "proposal",
    "proposal-review",
    "spec",
    "plan",
    "implement",
    "workflow",
    "verify",
    "pr",
    "project-map",
]
CUSTOMER_PORTABLE_M2_SKILLS = [
    "proposal",
    "proposal-review",
    "spec",
    "plan",
    "implement",
    "verify",
    "pr",
]
CUSTOMER_PORTABLE_REQUIRED_INTERNAL_DEPENDENCY_PATTERNS = {
    "required RigorLoop specs": re.compile(
        r"\b(?:must|must first|required|require|required:|read)\b.{0,80}\bRigorLoop\b.{0,80}\bspecs/",
        re.IGNORECASE,
    ),
    "required RigorLoop constitution": re.compile(
        r"\b(?:must|must first|required|require|required:|read)\b.{0,80}\bRigorLoop\b.{0,80}\bCONSTITUTION\.md\b",
        re.IGNORECASE,
    ),
    "required RigorLoop agents": re.compile(
        r"\b(?:must|must first|required|require|required:|read)\b.{0,80}\bRigorLoop\b.{0,80}\bAGENTS\.md\b",
        re.IGNORECASE,
    ),
    "required RigorLoop workflow spec": re.compile(
        r"\bread the RigorLoop workflow spec before proceeding\b",
        re.IGNORECASE,
    ),
    "required RigorLoop reports": re.compile(
        r"\brequired:\s*docs/reports/token-cost/",
        re.IGNORECASE,
    ),
}
CUSTOMER_PORTABLE_ALLOWED_GUARD_TERMS = [
    "project-local",
    "if present",
    "when present",
    "when operating inside the RigorLoop repository",
    "when this file is the review target",
    "when the user provided this path",
    "when governing project docs exist",
    "direct target",
]
SKILL_CONTRACT_FORBIDDEN_NEW_SKILLS = [
    "ci",
    "review-resolution",
    "ui-design",
    "ui-design-review",
    "workflow-contract",
    "adopt-rigorloop",
]
SKILL_CONTRACT_DEFERRED_SHARED_BLOCKS = [
    "vision-fit",
    "plan-readiness-vs-completion",
    "milestone-aware-review-handoff",
    "first-pass-completeness",
    "material-finding-requirements",
]
SKILL_CONTRACT_REQUIRED_CORE_SECTIONS = [
    "Purpose",
    "When to use",
    "When not to use",
    "Inputs to read",
    "Outputs",
    "Handoff",
    "Stop conditions",
    "Claims this skill must not make",
]
SKILL_CONTRACT_RESULT_FIELDS = [
    "Skill",
    "Status",
    "Artifacts changed",
    "Open blockers",
    "Next stage",
]
SKILL_CONTRACT_PROGRESS_SKILLS = [
    "workflow",
    "plan",
    "implement",
    "code-review",
    "verify",
    "pr",
]
PROJECT_ARTIFACT_LOOKUP_SKILLS = [
    "proposal",
    "spec",
    "architecture",
    "plan",
    "test-spec",
    "proposal-review",
    "spec-review",
    "architecture-review",
    "plan-review",
    "code-review",
    "explain-change",
    "verify",
    "pr",
]
CHANGE_RECORD_BOUNDED_READ_SKILLS = [
    "proposal-review",
    "code-review",
    "verify",
    "pr",
    "plan",
]
CHANGE_RECORD_FULL_READ_ESCALATION_TERMS = [
    "full `change.yaml`",
    "forensic reconstruction",
    "unsupported-shape",
    "whole-record review",
]
PUBLIC_WORKFLOW_AND_SKILL_SURFACES = [
    "README.md",
    "AGENTS.md",
    "CONSTITUTION.md",
    "docs/workflows.md",
    "skills",
    ".codex/skills",
    "dist/adapters",
]
TEXT_SURFACE_SUFFIXES = {".md", ".txt", ".yaml", ".yml"}
RETIRED_PUBLIC_ROUTE_PATTERNS = {
    "fast lane": re.compile(r"\bfast[- ]lane\b", re.IGNORECASE),
    "full lane": re.compile(r"\bfull[- ]lane\b", re.IGNORECASE),
    "full-feature lane": re.compile(r"\bfull[- ]feature(?:[- ]lane)?\b", re.IGNORECASE),
    "low-risk route": re.compile(r"\blow[- ]risk\b", re.IGNORECASE),
    "high-risk route": re.compile(r"\bhigh[- ]risk\b", re.IGNORECASE),
    "tiny low-risk route": re.compile(r"\btiny\s+low[- ]risk\b", re.IGNORECASE),
    "small-change route": re.compile(r"\bsmall[- ]change(?:[- ]lane)?\b", re.IGNORECASE),
    "mini-spec": re.compile(r"\bmini[- ]spec\b", re.IGNORECASE),
    "proportional evidence": re.compile(r"\bproportional[- ]evidence\b", re.IGNORECASE),
}
WORKFLOW_SPEC_ALLOWED_RETIRED_ROUTE_CONTEXTS = [
    "MUST NOT classify work as",
    "Static validation MUST fail",
    "not separate",
]
PUBLISHED_SKILL_FORBIDDEN_INTERNAL_PATTERNS = {
    "workflow spec path": re.compile(r"\bspecs/rigorloop-workflow\.md\b"),
    "skill contract spec path": re.compile(r"\bspecs/skill-contract\.md\b"),
    "codex generated mirror path": re.compile(r"\.codex/skills"),
    "adapter package path": re.compile(r"\bdist/adapters\b"),
    "selector command": re.compile(r"\bscripts/select-validation\.py\b"),
    "adapter build command": re.compile(r"\bscripts/build-adapters\.py\b"),
    "shared template path": re.compile(r"\btemplates/shared\b"),
    "canonical skill source placeholder": re.compile(r"\bskills/<skill>/SKILL\.md\b"),
    "selector path constraints": re.compile(r"\bselector[- ]path constraints\b", re.IGNORECASE),
    "selector-driven validation": re.compile(r"\bselector[- ]driven validation\b", re.IGNORECASE),
    "dist path selector warning": re.compile(r"do not pass `--path dist/adapters`", re.IGNORECASE),
    "drift-check mechanics": re.compile(r"\bdrift[- ]check mechanics\b", re.IGNORECASE),
    "generated-output handling": re.compile(r"\bGenerated-output handling\b"),
    "regenerate generated outputs": re.compile(r"\bRegenerate generated outputs\b"),
    "repository-owned drift checks": re.compile(r"\bValidate drift with repository-owned checks\b"),
    "shared blocks copied into skills": re.compile(r"\bShared blocks are copied into skills\b"),
    "shared-block implementation mechanics": re.compile(
        r"\bshared[- ]block implementation (?:details|mechanics)\b",
        re.IGNORECASE,
    ),
    "RigorLoop-local examples": re.compile(r"\bRigorLoop-local examples\b", re.IGNORECASE),
}
CODE_REVIEW_FORBIDDEN_FINAL_CLOSEOUT_PATTERNS = {
    "verify only after final milestone": re.compile(
        r"`?verify`?\s+only\s+after\s+the\s+final\s+in[- ]scope\s+implementation\s+milestone",
        re.IGNORECASE,
    ),
    "final milestone cleanly reviewed to verify": re.compile(
        r"final\s+in[- ]scope\s+implementation\s+milestone\s+is\s+cleanly\s+reviewed.{0,80}\bverify\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "clean final implementation milestone to verify": re.compile(
        r"clean\s+final\s+implementation\s+milestone.{0,80}\bverify\b",
        re.IGNORECASE | re.DOTALL,
    ),
}
VERIFY_FORBIDDEN_EXPLAIN_ORDER_PATTERNS = {
    "before explanation or PR": re.compile(r"\bbefore explanation or PR\b", re.IGNORECASE),
    "toward explanation and PR": re.compile(r"\btoward explanation and PR\b", re.IGNORECASE),
    "verify ascii arrow explain-change": re.compile(
        r"\bverify\b\s*(?:->|→)\s*`?explain-change`?",
        re.IGNORECASE,
    ),
}
SKILL_CONTRACT_CLAIM_BOUNDARY_TERMS = {
    "implement": [
        "review passed",
        "clean review",
        "branch-ready",
        "PR-ready",
        "ready-for-final-closeout",
    ],
    "code-review": [
        "branch-ready",
        "PR-ready",
        "CI passed",
        "verification passed",
    ],
    "verify": [
        "PR-ready",
        "PR body ready",
        "review passed",
    ],
    "pr": [
        "implementation passed",
        "review passed",
        "verification passed",
        "tests passed",
        "owning evidence",
    ],
    "plan": [
        "Readiness is not Done",
        "Remaining completion gates",
        "ready for PR",
        "ready for final closeout",
    ],
    "learn": [
        "new workflow policy",
        "authoritative artifact",
        "PR readiness",
    ],
}


def extract_markdown_block(text: str, heading: str) -> str:
    start_marker = f"## {heading}"
    start = text.find(start_marker)
    if start == -1:
        raise AssertionError(f"missing heading: {start_marker}")
    next_heading = text.find("\n## ", start + len(start_marker))
    if next_heading == -1:
        return text[start:].rstrip() + "\n"
    return text[start:next_heading].rstrip() + "\n"


def estimate_local_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, max(len(text.split()), math.ceil(len(text) / 4)))


def assert_progressive_loading_quick_guide_contract(
    test_case: unittest.TestCase,
    skill_body: str,
    *,
    max_position_tokens: int = 800,
    max_words: int = 250,
) -> None:
    quick_guide = extract_markdown_block(skill_body, "Quick operating guide")
    heading_index = skill_body.find("## Quick operating guide")
    leading_text = skill_body[:heading_index]
    test_case.assertLessEqual(
        estimate_local_tokens(leading_text),
        max_position_tokens,
        "Quick operating guide must appear within the first 800 estimated tokens",
    )

    for label in PROGRESSIVE_LOADING_QUICK_GUIDE_LABELS:
        test_case.assertIn(label, quick_guide)

    guide_word_count = len(quick_guide.split())
    has_safety_rationale = "safety rationale" in skill_body.lower()
    test_case.assertTrue(
        guide_word_count <= max_words or has_safety_rationale,
        "Quick operating guide over 250 words requires a safety rationale",
    )
    test_case.assertIn("full-file", skill_body)
    test_case.assertIn("broader-section", skill_body)


def assert_progressive_loading_implement_handoff_contract(
    test_case: unittest.TestCase,
    skill_body: str,
) -> None:
    required_terms = [
        "Current Handoff Summary",
        "current milestone section",
        "validation notes",
        "do not run broad repository searches to infer milestone state",
        "stop and report the missing state",
    ]
    for term in required_terms:
        test_case.assertIn(term, skill_body)

    forbidden_first_steps = [
        "start by searching all docs",
        "start by searching generated adapter output",
        "infer current state from broad `rg` output",
    ]
    for term in forbidden_first_steps:
        test_case.assertNotIn(term, skill_body)


def assert_progressive_loading_code_review_protected_contracts(
    test_case: unittest.TestCase,
    skill_body: str,
) -> None:
    lowered = skill_body.lower()
    for term in PROGRESSIVE_LOADING_CODE_REVIEW_PROTECTED_TERMS:
        test_case.assertIn(term, lowered)
    test_case.assertNotIn("references/clean-review-template.md", skill_body)
    test_case.assertNotIn("references/finding-format.md", skill_body)


def iter_public_workflow_and_skill_surfaces() -> list[Path]:
    files: list[Path] = []
    for relative_path in PUBLIC_WORKFLOW_AND_SKILL_SURFACES:
        path = ROOT / relative_path
        if path.is_file():
            files.append(path)
            continue
        if path.is_dir():
            for candidate in sorted(path.rglob("*")):
                if candidate.is_file() and candidate.suffix.lower() in TEXT_SURFACE_SUFFIXES:
                    files.append(candidate)
    return files


def iter_published_skill_text_surfaces() -> list[Path]:
    files: list[Path] = []
    for root in [ROOT / "skills", ROOT / ".codex" / "skills"]:
        if root.exists():
            files.extend(sorted(root.glob("*/SKILL.md")))

    adapter_root = ROOT / "dist" / "adapters"
    if adapter_root.exists():
        for candidate in sorted(adapter_root.rglob("SKILL.md")):
            if "skills" in candidate.parts:
                files.append(candidate)

    return files


def iter_published_skill_surfaces_for(skill_name: str) -> list[Path]:
    return [
        path
        for path in iter_published_skill_text_surfaces()
        if path.parent.name == skill_name
    ]


def has_customer_portable_guard(text: str) -> bool:
    normalized = text.lower()
    return any(term.lower() in normalized for term in CUSTOMER_PORTABLE_ALLOWED_GUARD_TERMS)


def run_validator(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(target)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def assert_requirement_id_covered(test_case: unittest.TestCase, body: str, requirement_number: int) -> None:
    if f"`R{requirement_number}`" in body:
        return
    range_pattern = re.compile(r"`R(?P<start>\d+)`-`R(?P<end>\d+)`")
    for match in range_pattern.finditer(body):
        start = int(match.group("start"))
        end = int(match.group("end"))
        if start <= requirement_number <= end:
            return
    test_case.fail(f"R{requirement_number} is not covered explicitly or by range")


def assert_boundary_id_covered(test_case: unittest.TestCase, body: str, boundary_number: int) -> None:
    if f"`EB{boundary_number}`" in body:
        return
    range_pattern = re.compile(r"`EB(?P<start>\d+)`-`EB(?P<end>\d+)`")
    for match in range_pattern.finditer(body):
        start = int(match.group("start"))
        end = int(match.group("end"))
        if start <= boundary_number <= end:
            return
    test_case.fail(f"EB{boundary_number} is not covered explicitly or by range")


class SkillValidatorFixtureTests(unittest.TestCase):
    maxDiff = None

    def write_spec_family_asset_fixture(
        self,
        root: Path,
        skill_name: str,
        assets: dict[str, str],
        resource_entries: str | None = None,
    ) -> Path:
        skill_dir = root / skill_name
        skill_dir.mkdir(parents=True)
        if resource_entries is None:
            resource_entries = "\n".join(
                [
                    f"- COPY `{relative_path}` when producing the related artifact structure.\n"
                    f"  Fill: structural fields for {relative_path}.\n"
                    "  Do not emit unfilled placeholders."
                    for relative_path in sorted(assets)
                ]
            )
        (skill_dir / "SKILL.md").write_text(
            "\n".join(
                [
                    "---",
                    f"name: {skill_name}",
                    "description: Validate spec-family asset packaging.",
                    "---",
                    "",
                    f"# {skill_name}",
                    "",
                    "## Resource map",
                    "",
                    resource_entries.rstrip(),
                    "",
                    "## Expected output",
                    "",
                    "Compact output summary.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        for relative_path, content in assets.items():
            asset_path = skill_dir / relative_path
            asset_path.parent.mkdir(parents=True, exist_ok=True)
            asset_path.write_text(textwrap.dedent(content), encoding="utf-8")
        return skill_dir

    def spec_family_asset_text(
        self,
        *,
        template: str,
        skill: str,
        status: str = "normative",
        body: str = "| <field> | <value> |\n",
        include_metadata: bool = True,
    ) -> str:
        metadata = ""
        if include_metadata:
            metadata = textwrap.dedent(
                f"""\
                <!-- Template: {template} -->
                <!-- Skill: {skill} -->
                <!-- Template status: {status} -->
                <!-- Maintained alongside: skills/{skill}/SKILL.md -->

                """
            )
        return metadata + textwrap.dedent(body)

    def proposal_family_asset_text(
        self,
        *,
        template: str,
        skill: str,
        status: str = "normative",
        body: str = "| <field> | <value> |\n",
        include_metadata: bool = True,
    ) -> str:
        return self.spec_family_asset_text(
            template=template,
            skill=skill,
            status=status,
            body=body,
            include_metadata=include_metadata,
        )

    def review_family_asset_text(
        self,
        *,
        template: str,
        skill: str,
        status: str = "normative",
        body: str = "| <field> | <value> |\n",
        include_metadata: bool = True,
    ) -> str:
        return self.spec_family_asset_text(
            template=template,
            skill=skill,
            status=status,
            body=body,
            include_metadata=include_metadata,
        )

    def write_resource_integrity_skill(
        self,
        root: Path,
        *,
        resource_entries: str,
        resources: dict[str, str] | None = None,
        body_extra: str = "",
        skill_name: str = "resource-integrity-fixture",
    ) -> Path:
        skill_dir = root / skill_name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "\n".join(
                [
                    "---",
                    f"name: {skill_name}",
                    "description: Validate mapped skill-local resource integrity.",
                    "---",
                    "",
                    f"# {skill_name}",
                    "",
                    "## Resource map",
                    "",
                    textwrap.dedent(resource_entries).strip(),
                    "",
                    "## Expected output",
                    "",
                    "Compact output summary.",
                    "",
                    body_extra.strip(),
                    "",
                ]
            ),
            encoding="utf-8",
        )
        for relative_path, content in (resources or {}).items():
            resource_path = skill_dir / relative_path
            resource_path.parent.mkdir(parents=True, exist_ok=True)
            resource_path.write_text(textwrap.dedent(content), encoding="utf-8")
        return skill_dir

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

    def copy_ci_maintenance_fixture(self, root: Path) -> Path:
        source = ROOT / "skills" / "ci-maintenance"
        target = root / "ci-maintenance"
        shutil.copytree(source, target)
        return target

    def assertCiMaintenanceFixtureFails(
        self,
        mutate: Callable[[Path], None],
        expected_text: str,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = self.copy_ci_maintenance_fixture(Path(temporary))
            mutate(skill_dir)
            result = run_validator(skill_dir)
            combined_output = f"{result.stdout}\n{result.stderr}"
            self.assertNotEqual(
                result.returncode,
                0,
                msg=f"expected ci-maintenance fixture to fail\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
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

    def test_skill_readability_valid_fixture_passes(self) -> None:
        self.assertFixturePasses("skill-readability/valid-pilot")

    def test_skill_readability_missing_version_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/missing-version",
            "version: missing required readability contract field",
        )

    def test_skill_readability_invalid_schema_version_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/invalid-schema-version",
            "schema-version must be 'skill-readability-v1'",
        )

    def test_skill_readability_missing_workflow_role_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/missing-workflow-role",
            "missing required '## Workflow role' section",
        )

    def test_skill_readability_missing_workflow_role_field_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/missing-workflow-role-field",
            "Workflow role missing required field 'downstream'",
        )

    def test_skill_readability_invalid_stage_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/invalid-stage",
            "workflow role stage must be one of",
        )

    def test_skill_readability_missing_output_skeleton_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/missing-output-skeleton",
            "missing required '## Output skeleton' section",
        )

    def test_skill_readability_output_skeleton_without_placeholder_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/output-skeleton-without-placeholder",
            "Output skeleton must include fillable placeholders",
        )

    def test_skill_readability_required_internal_reference_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/required-internal-reference",
            "required unavailable internal reference",
        )

    def test_skill_readability_duplicate_closed_enum_fails(self) -> None:
        self.assertFixtureFails(
            "skill-readability/duplicate-closed-enum",
            "duplicate closed enum block",
        )

    def test_published_design_description_too_long_fails(self) -> None:
        self.assertFixtureFails(
            "published-design/description-too-long",
            "description must be 1024 characters or fewer",
        )

    def test_published_design_when_to_use_cannot_replace_description(self) -> None:
        self.assertFixtureFails(
            "published-design/when-to-use-replaces-description",
            "when_to_use must not replace description",
        )

    def test_published_design_missing_resource_map_fails(self) -> None:
        self.assertFixtureFails(
            "published-design/missing-resource-map",
            "packaged resources require a '## Resource map' section",
        )

    def test_published_design_resource_map_must_name_every_resource(self) -> None:
        self.assertFixtureFails(
            "published-design/resource-map-missing-resource",
            "Resource map must name packaged resource 'references/detail.md'",
        )

    def test_published_design_packaged_script_with_map_passes(self) -> None:
        self.assertFixturePasses("published-design/packaged-script-valid")

    def test_published_design_packaged_script_requires_failure_behavior(self) -> None:
        self.assertFixtureFails(
            "published-design/packaged-script-missing-failure",
            "packaged script 'scripts/check.py' map entry must describe failure behavior",
        )

    def test_published_design_repository_root_script_dependency_fails(self) -> None:
        self.assertFixtureFails(
            "published-design/required-root-script",
            "required repository-root dependency",
        )

    def test_published_design_repository_root_script_command_dependency_fails(self) -> None:
        self.assertFixtureFails(
            "published-design/required-root-script-command",
            "required repository-root dependency by command wording: scripts/validate-internal.py",
        )

    def test_published_design_packaged_script_resource_map_passes(self) -> None:
        self.assertFixturePasses("published-design/packaged-script-resource-map")

    def test_published_skill_resource_map_copy_read_run_classes_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = self.write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - COPY `assets/skeleton.md` when creating the output structure.
                  Fill all fields and do not emit unfilled placeholders.
                - READ `references/guidance.md` when reviewing domain guidance.
                - RUN `scripts/check.py` when deterministic checking is needed.
                  Input: repository root path.
                  Output: zero exit code or diagnostic output.
                  Failure: nonzero exit code blocks the check.
                """,
                resources={
                    "assets/skeleton.md": "# Skeleton\n",
                    "references/guidance.md": "# Guidance\n",
                    "scripts/check.py": "print('ok')\n",
                },
            )
            result = run_validator(skill_dir)
            self.assertEqual(
                result.returncode,
                0,
                msg=f"expected mapped resources to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )

    def assertResourceIntegritySkillFails(
        self,
        *,
        resource_entries: str,
        expected_text: str,
        resources: dict[str, str] | None = None,
        body_extra: str = "",
        skill_name: str = "resource-integrity-fixture",
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = self.write_resource_integrity_skill(
                Path(temporary),
                resource_entries=resource_entries,
                resources=resources,
                body_extra=body_extra,
                skill_name=skill_name,
            )
            result = run_validator(skill_dir)
            combined_output = f"{result.stdout}\n{result.stderr}"
            self.assertNotEqual(
                result.returncode,
                0,
                msg=f"expected resource-integrity fixture to fail\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )
            self.assertIn(expected_text, combined_output)

    def test_published_skill_resource_map_copy_must_point_to_assets(self) -> None:
        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - COPY `references/guidance.md` when creating output.
            """,
            resources={"references/guidance.md": "# Guidance\n"},
            expected_text="Resource map entry 'COPY references/guidance.md' must point to assets/",
        )

    def test_published_skill_resource_map_read_must_point_to_references(self) -> None:
        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - READ `assets/skeleton.md` when reviewing guidance.
            """,
            resources={"assets/skeleton.md": "# Skeleton\n"},
            expected_text="Resource map entry 'READ assets/skeleton.md' must point to references/",
        )

    def test_published_skill_resource_map_run_must_point_to_scripts(self) -> None:
        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - RUN `assets/check.md` when checking output.
            """,
            resources={"assets/check.md": "# Check\n"},
            expected_text="Resource map entry 'RUN assets/check.md' must point to scripts/",
        )

    def test_published_skill_resource_map_rejects_templates_class(self) -> None:
        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - COPY `templates/architecture.md` when creating output.
            """,
            resources={"templates/architecture.md": "# Architecture\n"},
            expected_text="Resource map entry 'COPY templates/architecture.md' must point to assets/",
        )

    def test_published_skill_resource_map_rejects_missing_mapped_resource(self) -> None:
        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - COPY `assets/missing.md` when creating output.
            """,
            expected_text="mapped resource 'assets/missing.md' does not exist in canonical skill source",
        )

    def test_published_skill_resource_map_rejects_path_traversal(self) -> None:
        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - READ `../references/escape.md` when reviewing guidance.
            """,
            expected_text="mapped resource path '../references/escape.md' must be relative to the skill root and stay inside it",
        )

    def test_published_skill_resource_map_rejects_absolute_path(self) -> None:
        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - RUN `/tmp/check.py` when checking output.
            """,
            expected_text="mapped resource path '/tmp/check.py' must be relative to the skill root and stay inside it",
        )

    def test_published_skill_legacy_template_loading_instruction_fails(self) -> None:
        cases = [
            ("Use templates/architecture.md when relevant.", "templates/architecture.md"),
            ("Use templates/architecture.md when available.", "templates/architecture.md"),
            ("Read references/diagram-conventions.md when needed.", "references/diagram-conventions.md"),
            ("Copy assets/architecture-skeleton.md if present.", "assets/architecture-skeleton.md"),
            ("Run scripts/render-diagram.py when relevant.", "scripts/render-diagram.py"),
        ]
        for instruction, resource_path in cases:
            with self.subTest(instruction=instruction):
                self.assertResourceIntegritySkillFails(
                    resource_entries="""\
                    - READ `references/guidance.md` when reviewing guidance.
                    """,
                    resources={"references/guidance.md": "# Guidance\n"},
                    body_extra=instruction,
                    expected_text=(
                        f"unmapped skill-local resource reference `{resource_path}`; "
                        "declare it in `## Resource map`, migrate it to an approved "
                        "resource class, or remove the instruction"
                    ),
                )

    def test_published_skill_legacy_lint_avoids_examples_and_docs_paths(self) -> None:
        cases = [
            "Use the project-provided templates/architecture.md when relevant.",
            "Use templates/custom.md provided by the project.",
            "Read the repository-root templates/architecture.md when available.",
            "Read references/policy.md supplied by the repository.",
            "Use the user-provided references/diagram-conventions.md.",
            "Example path: templates/architecture.md",
            "Illustrative resource: references/diagram.md",
            "The generated artifact may contain the string templates/architecture.md.",
            "Inspect docs/templates/architecture.md when that artifact is the review target.",
            """\
            ```text
            Use templates/architecture.md in a customer artifact example.
            ```
            """,
            "Customer projects may contain `assets/example.png` as normal data.",
        ]
        for instruction in cases:
            with self.subTest(instruction=instruction):
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = self.write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=f"""\
                        Artifact examples may mention `docs/changes/example/review-log.md`.

                        {instruction}
                        """,
                    )
                    result = run_validator(skill_dir)
                    self.assertEqual(
                        result.returncode,
                        0,
                        msg=f"expected non-resource example to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                    )

    def test_published_skill_legacy_lint_checks_each_reference_on_mixed_line(self) -> None:
        cases = [
            (
                "Use the user-provided references/external.md and templates/architecture.md.",
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                """\
                Use the user-provided references/external.md and
                templates/architecture.md when relevant.
                """,
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                """\
                Use templates/architecture.md when relevant and the user-provided
                references/external.md.
                """,
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                """\
                - Use the user-provided references/external.md and
                  templates/architecture.md when relevant.
                """,
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                """\
                - Use templates/architecture.md when relevant and
                  the user-provided references/external.md.
                """,
                "templates/architecture.md",
                "references/external.md",
            ),
            (
                "Use the user-provided references/a.md and references/b.md.",
                "references/b.md",
                "references/a.md",
            ),
            (
                "Example path: references/example.md; use templates/architecture.md.",
                "templates/architecture.md",
                "references/example.md",
            ),
        ]
        for instruction, reported_path, suppressed_path in cases:
            with self.subTest(instruction=instruction):
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = self.write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=instruction,
                    )
                    result = run_validator(skill_dir)
                    combined_output = f"{result.stdout}\n{result.stderr}"
                    self.assertNotEqual(
                        result.returncode,
                        0,
                        msg=f"expected mixed reference fixture to fail\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                    )
                    self.assertIn(
                        f"unmapped skill-local resource reference `{reported_path}`",
                        combined_output,
                    )
                    self.assertNotIn(
                        f"unmapped skill-local resource reference `{suppressed_path}`",
                        combined_output,
                    )

    def test_published_skill_legacy_lint_keeps_instruction_boundaries(self) -> None:
        cases = [
            """\
            - Use the user-provided references/external.md.
            - The generated artifact may contain the string templates/architecture.md.
            """,
            """\
            1. Use the user-provided references/external.md.
            2. The generated artifact may contain templates/architecture.md.
            """,
            """\
            Use the user-provided references/external.md.

            The generated artifact may contain templates/architecture.md.
            """,
            """\
            Use the user-provided references/external.md.

            ## Output example

            The generated artifact may contain templates/architecture.md.
            """,
            """\
            Use the user-provided references/external.md.

            ```md
            Use templates/architecture.md.
            ```
            """,
        ]
        for instruction in cases:
            with self.subTest(instruction=instruction):
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = self.write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=instruction,
                    )
                    result = run_validator(skill_dir)
                    self.assertEqual(
                        result.returncode,
                        0,
                        msg=f"expected independent instruction boundaries to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                    )

    def test_published_skill_legacy_lint_ignores_resource_map_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill_dir = self.write_resource_integrity_skill(
                Path(temporary),
                resource_entries="""\
                - COPY `assets/architecture-skeleton.md` when authoring architecture.
                """,
                resources={"assets/architecture-skeleton.md": "# Architecture\n"},
            )
            result = run_validator(skill_dir)
            self.assertEqual(
                result.returncode,
                0,
                msg=f"expected Resource map entries to stay owned by mapped validation\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
            )

    def test_published_skill_legacy_lint_allows_individually_qualified_references(self) -> None:
        cases = [
            "Use the user-provided references/external.md and the project-provided templates/custom.md.",
            "Use the user-provided references/external.md and templates/custom.md provided by the project.",
        ]
        for instruction in cases:
            with self.subTest(instruction=instruction):
                with tempfile.TemporaryDirectory() as temporary:
                    skill_dir = self.write_resource_integrity_skill(
                        Path(temporary),
                        resource_entries="""\
                        - READ `references/guidance.md` when reviewing guidance.
                        """,
                        resources={"references/guidance.md": "# Guidance\n"},
                        body_extra=instruction,
                    )
                    result = run_validator(skill_dir)
                    self.assertEqual(
                        result.returncode,
                        0,
                        msg=f"expected individually qualified references to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                    )

    def test_published_skill_architecture_legacy_references_fail_after_m3(self) -> None:
        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - READ `references/guidance.md` when reviewing guidance.
            """,
            resources={"references/guidance.md": "# Guidance\n"},
            body_extra=(
                "Use `templates/architecture.md` for the full 12-section arc42 structure. "
                "Use `templates/diagram-styles.mmd` for Mermaid flowchart or graph C4 role styles. "
                "Use `templates/adr.md` for ADR structure."
            ),
            skill_name="architecture",
            expected_text="architecture: unmapped skill-local resource reference `templates/architecture.md`",
        )

        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - READ `references/guidance.md` when reviewing guidance.
            """,
            resources={"references/guidance.md": "# Guidance\n"},
            body_extra="Use templates/architecture.md when relevant.",
            expected_text="resource-integrity-fixture: unmapped skill-local resource reference `templates/architecture.md`",
        )

        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - READ `references/guidance.md` when reviewing guidance.
            """,
            resources={"references/guidance.md": "# Guidance\n"},
            body_extra="Use templates/unapproved.md when relevant.",
            skill_name="architecture",
            expected_text="architecture: unmapped skill-local resource reference `templates/unapproved.md`",
        )

        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - READ `references/guidance.md` when reviewing guidance.
            """,
            resources={"references/guidance.md": "# Guidance\n"},
            body_extra="Use the user-provided references/external.md and templates/architecture.md when relevant.",
            skill_name="architecture",
            expected_text="architecture: unmapped skill-local resource reference `templates/architecture.md`",
        )

        self.assertResourceIntegritySkillFails(
            resource_entries="""\
            - READ `references/guidance.md` when reviewing guidance.
            """,
            resources={"references/guidance.md": "# Guidance\n"},
            body_extra="""\
            Use `templates/architecture.md` for the full 12-section arc42 structure. Use `templates/diagram-styles.mmd` for Mermaid flowchart or graph C4 role styles. Use `templates/adr.md` for ADR structure.
            - Use templates/unapproved.md when relevant.
            """,
            skill_name="architecture",
            expected_text="architecture: unmapped skill-local resource reference `templates/unapproved.md`",
        )

    def test_current_architecture_resource_map_uses_packaged_assets(self) -> None:
        architecture_dir = ROOT / "skills" / "architecture"
        skill_text = (architecture_dir / "SKILL.md").read_text(encoding="utf-8")
        expected_resources = {
            "assets/architecture-skeleton.md",
            "assets/adr-skeleton.md",
            "assets/diagram-styles.mmd",
        }

        for resource_path in expected_resources:
            with self.subTest(resource_path=resource_path):
                self.assertIn(resource_path, skill_text)
                self.assertTrue((architecture_dir / resource_path).is_file())

        self.assertNotIn("templates/architecture.md", skill_text)
        self.assertNotIn("templates/diagram-styles.mmd", skill_text)
        self.assertNotIn("templates/adr.md", skill_text)

        result = run_validator(architecture_dir)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected normalized architecture resource map to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_published_design_plan_asset_pilot_valid_fixture_passes(self) -> None:
        self.assertFixturePasses("published-design/plan-assets-valid")

    def test_published_design_plan_asset_count_is_exact(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-missing-approved-asset",
            "plan asset pilot must ship exactly approved assets",
        )

    def test_published_design_plan_asset_metadata_required(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-missing-metadata",
            "asset metadata missing required field 'Template'",
        )

    def test_published_design_plan_asset_status_must_be_normative(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-optional-status",
            "plan asset pilot asset 'assets/milestone.md' must use normative status",
        )

    def test_published_design_plan_asset_resource_map_requires_copy(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-non-copy-verb",
            "Resource map entry for 'assets/milestone.md' must use literal COPY",
        )

    def test_published_design_plan_asset_resource_map_requires_trigger_and_fields(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-missing-fields",
            "Resource map entry for 'assets/milestone.md' must name fields or structures to fill",
        )

    def test_published_design_plan_asset_resource_map_requires_every_asset(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-missing-resource-map-entry",
            "Resource map must name packaged resource 'assets/decision-log-row.md'",
        )

    def test_published_design_plan_asset_placeholders_required(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-missing-placeholder",
            "asset 'assets/milestone.md' must include a visible placeholder",
        )

    def test_published_design_plan_asset_root_dependency_fails(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-root-dependency",
            "asset 'assets/milestone.md' must not require repository-root dependency",
        )

    def test_published_design_plan_asset_fingerprint_mismatch_fails(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-fingerprint-mismatch",
            "asset 'assets/milestone.md' structural fingerprint mismatch",
        )

    def test_published_design_plan_skeleton_section_set_mismatch_fails(self) -> None:
        self.assertFixtureFails(
            "published-design/plan-assets-section-mismatch",
            "plan-skeleton section set does not match SKILL.md expected sections",
        )

    def test_ci_maintenance_contract_validates_canonical_skill(self) -> None:
        result = run_validator(ROOT / "skills" / "ci-maintenance" / "SKILL.md")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"expected canonical ci-maintenance skill to pass\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_ci_maintenance_contract_rejects_stale_identifier_surfaces(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace("role_name: ci-maintenance", "role_name: ci"),
                encoding="utf-8",
            )

        self.assertCiMaintenanceFixtureFails(
            mutate,
            "stale ci-maintenance identifier",
        )

    def test_ci_maintenance_contract_rejects_missing_schema_version(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace("schema-version: skill-readability-v1\n", ""),
                encoding="utf-8",
            )

        self.assertCiMaintenanceFixtureFails(
            mutate,
            "ci-maintenance frontmatter must include schema-version",
        )

    def test_ci_maintenance_contract_requires_resource_map_verbs(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace(
                    "- READ `references/risk-to-check-map.md`",
                    "- COPY `references/risk-to-check-map.md`",
                ),
                encoding="utf-8",
            )

        self.assertCiMaintenanceFixtureFails(
            mutate,
            "Resource map entry for 'references/risk-to-check-map.md' must use literal READ",
        )

    def test_ci_maintenance_contract_requires_skeleton_defaults(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skeleton_path = skill_dir / "assets" / "github-workflow-skeleton.yml"
            text = skeleton_path.read_text(encoding="utf-8")
            skeleton_path.write_text(
                text.replace("permissions:\n  contents: read\n\n", ""),
                encoding="utf-8",
            )

        self.assertCiMaintenanceFixtureFails(
            mutate,
            "workflow skeleton must include least-privilege permissions",
        )

    def test_ci_maintenance_contract_requires_risk_map_split_and_fail_safe(self) -> None:
        def mutate(skill_dir: Path) -> None:
            risk_map_path = skill_dir / "references" / "risk-to-check-map.md"
            text = risk_map_path.read_text(encoding="utf-8")
            risk_map_path.write_text(
                text.replace(
                    "Unmapped changed surfaces are not no-risk surfaces. If a changed path does not match this map, flag it for reviewer judgment, route it to a conservative boundary check, or both.\n\n",
                    "",
                ),
                encoding="utf-8",
            )

        self.assertCiMaintenanceFixtureFails(
            mutate,
            "risk map must include unmapped-surface fail-safe",
        )

    def test_ci_maintenance_contract_requires_review_guardrails_and_command_blocker(self) -> None:
        def mutate(skill_dir: Path) -> None:
            skill_path = skill_dir / "SKILL.md"
            text = skill_path.read_text(encoding="utf-8")
            skill_path.write_text(
                text.replace("overbroad permissions", "permission concerns").replace(
                    "report a blocker instead of guessing",
                    "continue with a likely command",
                ),
                encoding="utf-8",
            )

        self.assertCiMaintenanceFixtureFails(
            mutate,
            "ci-maintenance must flag overbroad permissions during workflow review",
        )

    def test_spec_family_asset_valid_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "spec",
                {
                    "assets/spec-skeleton.md": self.spec_family_asset_text(
                        template="spec-skeleton-v1", skill="spec", body="## Status\n\n<status>\n"
                    ),
                },
            )
            self.write_spec_family_asset_fixture(
                root,
                "spec-review",
                {
                    "assets/review-result-skeleton.md": self.spec_family_asset_text(
                        template="spec-review-result-skeleton-v1",
                        skill="spec-review",
                        body=(
                            "## Result\n\n"
                            "- Review status: <review status>\n"
                            "- Recording status: <recording status>\n"
                        ),
                    ),
                    "assets/material-finding.md": self.spec_family_asset_text(
                        template="spec-review-material-finding-v1",
                        skill="spec-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding ID: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                            "- needs-decision rationale: <needs-decision rationale>\n"
                        ),
                    ),
                },
                resource_entries=textwrap.dedent(
                    """\
                    - COPY `assets/material-finding.md` when recording each material finding.
                      Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path.
                      Confirm the literal `Finding ID:` line exists before linking the finding from `review-log.md` or `review-resolution.md`.
                      Do not emit unfilled placeholders.
                    - COPY `assets/review-result-skeleton.md` when recording the review result.
                      Fill: review result fields.
                      Do not emit unfilled placeholders.
                    """
                ),
            )
            self.write_spec_family_asset_fixture(
                root,
                "test-spec",
                {
                    "assets/test-spec-skeleton.md": self.spec_family_asset_text(
                        template="test-spec-skeleton-v1",
                        skill="test-spec",
                        body="## Status\n\n<status>\n",
                    ),
                    "assets/test-case.md": self.spec_family_asset_text(
                        template="test-spec-test-case-v1", skill="test-spec"
                    ),
                    "assets/coverage-map-row.md": self.spec_family_asset_text(
                        template="test-spec-coverage-map-row-v1", skill="test-spec"
                    ),
                },
            )

            result = run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_spec_family_generated_asset_presence_passes_for_complete_output(self) -> None:
        fixture = FIXTURES / "published-design/generated-output-presence/valid"
        errors = skill_validation.validate_generated_asset_presence(
            skill_name="spec",
            canonical_skill_dir=fixture / "canonical/spec",
            generated_skill_dir=fixture / "generated/spec",
            surface_label="generated skill mirror",
        )

        self.assertEqual(errors, [])

    def test_spec_family_generated_asset_presence_fails_for_missing_generated_asset(self) -> None:
        fixture = FIXTURES / "published-design/generated-output-presence/missing-asset"
        errors = skill_validation.validate_generated_asset_presence(
            skill_name="spec",
            canonical_skill_dir=fixture / "canonical/spec",
            generated_skill_dir=fixture / "generated/spec",
            surface_label="generated skill mirror",
        )

        self.assertEqual(
            errors,
            [
                "Generated output for skill 'spec' is missing mapped asset "
                "'assets/spec-skeleton.md' in generated skill mirror"
            ],
        )

    def test_spec_family_generated_asset_presence_names_adapter_surface(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical_skill_dir = self.write_spec_family_asset_fixture(
                root / "canonical",
                "spec-review",
                {
                    "assets/review-result-skeleton.md": self.spec_family_asset_text(
                        template="spec-review-result-skeleton-v1",
                        skill="spec-review",
                        body="## Result\n\n- Review status: <review status>\n",
                    ),
                    "assets/material-finding.md": self.spec_family_asset_text(
                        template="spec-review-material-finding-v1",
                        skill="spec-review",
                        body="## Finding <finding id>\n\n- Finding ID: <finding id>\n- Severity: <severity>\n",
                    ),
                },
            )
            generated_skill_dir = root / "generated-adapter" / "spec-review"
            generated_asset = generated_skill_dir / "assets/review-result-skeleton.md"
            generated_asset.parent.mkdir(parents=True, exist_ok=True)
            generated_asset.write_text("generated result skeleton", encoding="utf-8")

            errors = skill_validation.validate_generated_asset_presence(
                skill_name="spec-review",
                canonical_skill_dir=canonical_skill_dir,
                generated_skill_dir=generated_skill_dir,
                surface_label="generated adapter output",
            )

            self.assertEqual(
                errors,
                [
                    "Generated output for skill 'spec-review' is missing mapped asset "
                    "'assets/material-finding.md' in generated adapter output"
                ],
            )

    def test_spec_family_asset_rejects_unapproved_asset_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "spec-review",
                {
                    "assets/review-result-skeleton.md": self.spec_family_asset_text(
                        template="spec-review-result-skeleton-v1", skill="spec-review"
                    ),
                    "assets/material-finding.md": self.spec_family_asset_text(
                        template="spec-review-material-finding-v1", skill="spec-review"
                    ),
                    "assets/review-dimension-row.md": self.spec_family_asset_text(
                        template="spec-review-dimension-row-v1", skill="spec-review"
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("spec-family asset rollout must ship exactly approved assets", result.stdout + result.stderr)

    def test_spec_family_asset_resource_map_requires_copy_and_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "spec",
                {
                    "assets/spec-skeleton.md": self.spec_family_asset_text(
                        template="spec-skeleton-v1", skill="spec"
                    ),
                },
                resource_entries=textwrap.dedent(
                    """\
                    - READ `assets/spec-skeleton.md` when creating a spec.
                      Do not emit unfilled placeholders.
                    """
                ),
            )

            result = run_validator(root)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Resource map entry for 'assets/spec-skeleton.md' must use literal COPY", output)
            self.assertIn("Resource map entry for 'assets/spec-skeleton.md' must name fields or structures to fill", output)

    def test_spec_family_asset_metadata_status_and_placeholder_required(self) -> None:
        cases = [
            (
                "missing metadata",
                self.spec_family_asset_text(
                    template="spec-skeleton-v1",
                    skill="spec",
                    include_metadata=False,
                ),
                "asset metadata missing required field 'Template'",
            ),
            (
                "invalid status",
                self.spec_family_asset_text(
                    template="spec-skeleton-v1",
                    skill="spec",
                    status="example",
                ),
                "spec-family asset 'assets/spec-skeleton.md' Template status must be one of normative, optional",
            ),
            (
                "missing placeholder",
                self.spec_family_asset_text(
                    template="spec-skeleton-v1",
                    skill="spec",
                    body="## Status\n\nStatus field.\n",
                ),
                "asset 'assets/spec-skeleton.md' must include a visible placeholder",
            ),
            (
                "filler prose",
                self.spec_family_asset_text(
                    template="spec-skeleton-v1",
                    skill="spec",
                    body="your text here\n",
                ),
                "asset 'assets/spec-skeleton.md' must not use filler placeholder text",
            ),
            (
                "root dependency",
                self.spec_family_asset_text(
                    template="spec-skeleton-v1",
                    skill="spec",
                    body="Run scripts/internal-check.py before filling <field>.\n",
                ),
                "asset 'assets/spec-skeleton.md' must not require repository-root dependency",
            ),
        ]

        for name, asset_text, expected in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.write_spec_family_asset_fixture(
                    root,
                    "spec",
                    {
                        "assets/spec-skeleton.md": asset_text,
                    },
                )

                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_spec_review_asset_review_policy_prose_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "spec-review",
                {
                    "assets/review-result-skeleton.md": self.spec_family_asset_text(
                        template="spec-review-result-skeleton-v1",
                        skill="spec-review",
                        body="This asset MUST define severity policy for reviewers.\n<field>\n",
                    ),
                    "assets/material-finding.md": self.spec_family_asset_text(
                        template="spec-review-material-finding-v1", skill="spec-review"
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "spec-review asset 'assets/review-result-skeleton.md' must not contain review-policy labels or guidance",
                result.stdout + result.stderr,
            )

    def test_spec_review_asset_review_policy_field_label_fails(self) -> None:
        for forbidden_label in (
            "Severity policy",
            "Recording-status rules",
            "Review dimension",
            "Security",
            "Privacy",
            "Observability",
            "Sufficiency",
            "Safe-resolution decision",
        ):
            with self.subTest(forbidden_label=forbidden_label):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self.write_spec_family_asset_fixture(
                        root,
                        "spec-review",
                        {
                            "assets/review-result-skeleton.md": self.spec_family_asset_text(
                                template="spec-review-result-skeleton-v1",
                                skill="spec-review",
                                body=f"- {forbidden_label}: <policy>\n",
                            ),
                            "assets/material-finding.md": self.spec_family_asset_text(
                                template="spec-review-material-finding-v1", skill="spec-review"
                            ),
                        },
                    )

                    result = run_validator(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "spec-review asset 'assets/review-result-skeleton.md' must not contain review-policy labels or guidance",
                        result.stdout + result.stderr,
                    )

    def test_spec_family_baseline_summary_records_required_surfaces(self) -> None:
        baseline = (
            ROOT
            / "docs"
            / "changes"
            / "2026-05-20-spec-family-assets-progressive-disclosure"
            / "baseline.md"
        )
        self.assertTrue(baseline.exists())
        text = baseline.read_text(encoding="utf-8")
        for required in [
            "PR #79 remains the authoritative behavior baseline",
            "skills/spec/SKILL.md",
            "skills/spec-review/SKILL.md",
            "skills/test-spec/SKILL.md",
            "Closed enums that remain in `SKILL.md`",
            "Stop conditions that remain in `SKILL.md`",
            "Review dimensions or coverage obligations that remain in `SKILL.md`",
            "Source location for each extracted asset",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_proposal_family_asset_valid_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "proposal",
                {
                    "assets/proposal-skeleton.md": self.proposal_family_asset_text(
                        template="proposal-skeleton-v1",
                        skill="proposal",
                        body=(
                            "## Status\n\n<status>\n\n"
                            "## Conditional sections\n\n"
                            "- Initial intent preservation: include when triggered by SKILL.md.\n"
                            "- Scope budget: include when triggered by SKILL.md.\n"
                        ),
                    ),
                },
            )
            self.write_spec_family_asset_fixture(
                root,
                "proposal-review",
                {
                    "assets/review-result-skeleton.md": self.proposal_family_asset_text(
                        template="proposal-review-result-skeleton-v1",
                        skill="proposal-review",
                        body=(
                            "## Result\n\n"
                            "- Skill: proposal-review\n"
                            "- Review status: <review status>\n"
                            "- Material findings: <material findings>\n"
                            "- Recording status: <recording status>\n"
                            "- Recording blocker: <recording blocker>\n"
                            "- Review record: <review record>\n"
                            "- Review log: <review log>\n"
                            "- Review resolution: <review resolution>\n"
                            "- Open blockers: <open blockers>\n"
                            "- Immediate next stage: <immediate next stage>\n"
                            "- Review dimensions: <review dimensions>\n"
                            "- Scope-preservation result: <scope-preservation result>\n"
                            "- Recommended edits: <recommended edits>\n"
                            "- Recommendation: <recommendation>\n"
                        ),
                    ),
                    "assets/material-finding.md": self.proposal_family_asset_text(
                        template="proposal-review-material-finding-v1",
                        skill="proposal-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding ID: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                            "- needs-decision rationale: <needs-decision rationale>\n"
                        ),
                    ),
                },
            )

            result = run_validator(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_proposal_review_result_skeleton_preserves_baseline_result_block(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "proposal-review",
                {
                    "assets/review-result-skeleton.md": self.proposal_family_asset_text(
                        template="proposal-review-result-skeleton-v1",
                        skill="proposal-review",
                        body=(
                            "# Result\n\n"
                            "- Review status: <review status>\n"
                            "- Material findings: <material findings>\n"
                            "- Recording status: <recording status>\n"
                        ),
                    ),
                    "assets/material-finding.md": self.proposal_family_asset_text(
                        template="proposal-review-material-finding-v1",
                        skill="proposal-review",
                        body="- Severity: <severity>\n",
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            output = result.stdout + result.stderr
            self.assertIn(
                "proposal-review review-result-skeleton must include baseline heading: ## Result",
                output,
            )
            self.assertIn(
                "proposal-review review-result-skeleton must include baseline field: Skill",
                output,
            )

    def test_proposal_family_asset_rejects_unapproved_asset_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "proposal",
                {
                    "assets/proposal-skeleton.md": self.proposal_family_asset_text(
                        template="proposal-skeleton-v1", skill="proposal"
                    ),
                    "assets/scope-budget-row.md": self.proposal_family_asset_text(
                        template="proposal-scope-budget-row-v1", skill="proposal"
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "proposal-family asset rollout must ship exactly approved assets",
                result.stdout + result.stderr,
            )

    def test_proposal_family_asset_resource_map_requires_copy_and_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "proposal",
                {
                    "assets/proposal-skeleton.md": self.proposal_family_asset_text(
                        template="proposal-skeleton-v1", skill="proposal"
                    ),
                },
                resource_entries=textwrap.dedent(
                    """\
                    - READ `assets/proposal-skeleton.md` when creating a proposal.
                      Do not emit unfilled placeholders.
                    """
                ),
            )

            result = run_validator(root)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Resource map entry for 'assets/proposal-skeleton.md' must use literal COPY",
                output,
            )
            self.assertIn(
                "Resource map entry for 'assets/proposal-skeleton.md' must name fields or structures to fill",
                output,
            )

    def test_proposal_family_asset_metadata_status_and_placeholder_required(self) -> None:
        cases = [
            (
                "missing metadata",
                self.proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    include_metadata=False,
                ),
                "asset metadata missing required field 'Template'",
            ),
            (
                "invalid status",
                self.proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    status="example",
                ),
                "proposal-family asset 'assets/proposal-skeleton.md' Template status must be one of normative, optional",
            ),
            (
                "missing placeholder",
                self.proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    body="## Status\n\nStatus field.\n",
                ),
                "asset 'assets/proposal-skeleton.md' must include a visible placeholder",
            ),
            (
                "filler prose",
                self.proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    body="your text here\n",
                ),
                "asset 'assets/proposal-skeleton.md' must not use filler placeholder text",
            ),
            (
                "root dependency",
                self.proposal_family_asset_text(
                    template="proposal-skeleton-v1",
                    skill="proposal",
                    body="Run scripts/internal-check.py before filling <field>.\n",
                ),
                "asset 'assets/proposal-skeleton.md' must not require repository-root dependency",
            ),
        ]

        for name, asset_text, expected in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.write_spec_family_asset_fixture(
                    root,
                    "proposal",
                    {
                        "assets/proposal-skeleton.md": asset_text,
                    },
                )

                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stdout + result.stderr)

    def test_proposal_review_asset_policy_field_labels_fail(self) -> None:
        for forbidden_label in (
            "Severity policy",
            "Material-finding sufficiency",
            "Safe-resolution decision rule",
            "Recording-status rules",
            "Scope-preservation rules",
            "Scope-budget review",
            "Vision fit review",
            "Standing artifact gate review",
            "Review dimension guidance",
        ):
            with self.subTest(forbidden_label=forbidden_label):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self.write_spec_family_asset_fixture(
                        root,
                        "proposal-review",
                        {
                            "assets/review-result-skeleton.md": self.proposal_family_asset_text(
                                template="proposal-review-result-skeleton-v1",
                                skill="proposal-review",
                                body=f"- {forbidden_label}: <policy>\n",
                            ),
                            "assets/material-finding.md": self.proposal_family_asset_text(
                                template="proposal-review-material-finding-v1",
                                skill="proposal-review",
                                body="- Severity: <severity>\n",
                            ),
                        },
                    )

                    result = run_validator(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "proposal-review asset 'assets/review-result-skeleton.md' must not contain review-policy labels or guidance",
                        result.stdout + result.stderr,
                    )

    def test_proposal_review_asset_non_allowlisted_field_labels_fail(self) -> None:
        for label in (
            "Architecture impact",
            "Testability notes",
            "Rollout realism",
            "Strategic value",
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.write_spec_family_asset_fixture(
                    root,
                    "proposal-review",
                    {
                        "assets/review-result-skeleton.md": self.proposal_family_asset_text(
                            template="proposal-review-result-skeleton-v1",
                            skill="proposal-review",
                            body=f"- {label}: <notes>\n",
                        ),
                        "assets/material-finding.md": self.proposal_family_asset_text(
                            template="proposal-review-material-finding-v1",
                            skill="proposal-review",
                            body="- Severity: <severity>\n",
                        ),
                    },
                )

                result = run_validator(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "proposal-review asset 'assets/review-result-skeleton.md' field label is not in the approved structural-label allowlist: "
                    + label,
                    result.stdout + result.stderr,
                )

    def test_proposal_review_asset_policy_prose_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "proposal-review",
                {
                    "assets/review-result-skeleton.md": self.proposal_family_asset_text(
                        template="proposal-review-result-skeleton-v1",
                        skill="proposal-review",
                        body="This asset MUST define severity policy for reviewers.\n<field>\n",
                    ),
                    "assets/material-finding.md": self.proposal_family_asset_text(
                        template="proposal-review-material-finding-v1",
                        skill="proposal-review",
                        body="- Severity: <severity>\n",
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "proposal-review asset 'assets/review-result-skeleton.md' must not contain review-policy labels or guidance",
                result.stdout + result.stderr,
            )

    def test_proposal_family_generated_asset_presence_names_adapter_surface(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical_skill_dir = self.write_spec_family_asset_fixture(
                root / "canonical",
                "proposal-review",
                {
                    "assets/review-result-skeleton.md": self.proposal_family_asset_text(
                        template="proposal-review-result-skeleton-v1",
                        skill="proposal-review",
                        body="- Review status: <review status>\n",
                    ),
                    "assets/material-finding.md": self.proposal_family_asset_text(
                        template="proposal-review-material-finding-v1",
                        skill="proposal-review",
                        body="- Severity: <severity>\n",
                    ),
                },
            )
            generated_skill_dir = root / "generated-adapter" / "proposal-review"
            generated_asset = generated_skill_dir / "assets/review-result-skeleton.md"
            generated_asset.parent.mkdir(parents=True, exist_ok=True)
            generated_asset.write_text("generated result skeleton", encoding="utf-8")

            errors = skill_validation.validate_generated_asset_presence(
                skill_name="proposal-review",
                canonical_skill_dir=canonical_skill_dir,
                generated_skill_dir=generated_skill_dir,
                surface_label="generated adapter output",
            )

            self.assertEqual(
                errors,
                [
                    "Generated output for skill 'proposal-review' is missing mapped asset "
                    "'assets/material-finding.md' in generated adapter output"
                ],
            )

    def test_review_family_asset_resource_map_requires_finding_id_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "code-review",
                {
                    "assets/material-finding.md": self.review_family_asset_text(
                        template="code-review-material-finding-v1",
                        skill="code-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding ID: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                            "- needs-decision rationale: <needs-decision rationale>\n"
                        ),
                    ),
                    "assets/review-result-skeleton.md": self.review_family_asset_text(
                        template="code-review-result-skeleton-v1",
                        skill="code-review",
                        body="- Review status: <review status>\n",
                    ),
                },
                resource_entries=textwrap.dedent(
                    """\
                    - COPY `assets/material-finding.md` when recording each material finding.
                      Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path.
                      Do not emit unfilled placeholders.
                    - COPY `assets/review-result-skeleton.md` when recording the review result.
                      Fill: review result fields.
                      Do not emit unfilled placeholders.
                    """
                ),
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Resource map entry for 'assets/material-finding.md' must instruct agents to confirm the literal Finding ID line before linking",
                result.stdout + result.stderr,
            )

    def test_code_review_family_assets_are_installed_and_preserve_status_vocabulary(self) -> None:
        skills_dir = ROOT / "skills"
        skill_path = skills_dir / "code-review" / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8")

        self.assertIn("- COPY `assets/material-finding.md`", skill_text)
        self.assertIn("- COPY `assets/review-result-skeleton.md`", skill_text)
        self.assertIn("Finding ID:", skill_text)

        material_finding = (skills_dir / "code-review" / "assets" / "material-finding.md").read_text(
            encoding="utf-8"
        )
        for label in [
            "Finding ID:",
            "Severity:",
            "Location:",
            "Evidence:",
            "Required outcome:",
            "Safe resolution path:",
            "needs-decision rationale:",
        ]:
            self.assertIn(label, material_finding)

        result_skeleton = (
            skills_dir / "code-review" / "assets" / "review-result-skeleton.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "clean-with-notes | changes-requested | blocked | inconclusive",
            result_skeleton,
        )
        self.assertIn("- Reviewed milestone:", result_skeleton)
        self.assertIn("- Milestone closeout:", result_skeleton)
        self.assertNotIn("approved | changes-requested", result_skeleton)

    def test_proposal_review_family_assets_preserve_gate_status_vocabulary(self) -> None:
        skills_dir = ROOT / "skills"
        skill_text = (skills_dir / "proposal-review" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("- COPY `assets/material-finding.md`", skill_text)
        self.assertIn("- COPY `assets/review-result-skeleton.md`", skill_text)
        self.assertIn("Finding ID:", skill_text)

        material_finding = (
            skills_dir / "proposal-review" / "assets" / "material-finding.md"
        ).read_text(encoding="utf-8")
        code_review_finding = (
            skills_dir / "code-review" / "assets" / "material-finding.md"
        ).read_text(encoding="utf-8")
        for label in [
            "Finding ID:",
            "Severity:",
            "Location:",
            "Evidence:",
            "Required outcome:",
            "Safe resolution path:",
            "needs-decision rationale:",
        ]:
            self.assertIn(label, material_finding)
        self.assertEqual(
            skill_validation._review_family_material_finding_field_block(material_finding),
            skill_validation._review_family_material_finding_field_block(code_review_finding),
        )

        result_skeleton = (
            skills_dir / "proposal-review" / "assets" / "review-result-skeleton.md"
        ).read_text(encoding="utf-8")
        self.assertIn("approved | changes-requested | blocked | inconclusive", result_skeleton)
        self.assertNotIn("clean-with-notes", result_skeleton)

    def test_spec_review_family_assets_use_material_finding_and_preserve_readiness(self) -> None:
        skills_dir = ROOT / "skills"
        skill_text = (skills_dir / "spec-review" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("- COPY `assets/material-finding.md`", skill_text)
        self.assertIn("- COPY `assets/review-result-skeleton.md`", skill_text)
        self.assertIn("Finding ID:", skill_text)
        self.assertNotIn("assets/review-finding.md", skill_text)
        self.assertFalse((skills_dir / "spec-review" / "assets" / "review-finding.md").exists())

        material_finding = (
            skills_dir / "spec-review" / "assets" / "material-finding.md"
        ).read_text(encoding="utf-8")
        code_review_finding = (
            skills_dir / "code-review" / "assets" / "material-finding.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(
            skill_validation._review_family_material_finding_field_block(material_finding),
            skill_validation._review_family_material_finding_field_block(code_review_finding),
        )

        result_skeleton = (
            skills_dir / "spec-review" / "assets" / "review-result-skeleton.md"
        ).read_text(encoding="utf-8")
        self.assertIn("approved | changes-requested | blocked | inconclusive", result_skeleton)
        self.assertIn("Eventual test-spec readiness", result_skeleton)
        self.assertNotIn("clean-with-notes", result_skeleton)

    def test_spec_review_canonical_contract_enforces_routing_readiness_split(self) -> None:
        skill_path = ROOT / "skills" / "spec-review" / "SKILL.md"

        self.assertEqual(
            skill_validation.validate_spec_review_canonical_contract(skill_path),
            [],
        )

    def test_spec_review_canonical_contract_rejects_test_spec_immediate_stage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill_dir = self.write_spec_family_asset_fixture(
                root,
                "spec-review",
                {
                    "assets/review-result-skeleton.md": self.spec_family_asset_text(
                        template="spec-review-result-skeleton-v1",
                        skill="spec-review",
                        body=(
                            "## Result\n\n"
                            "- Review status: <approved | changes-requested | blocked | inconclusive>\n"
                            "- Immediate next stage: <architecture | plan | test-spec>\n"
                            "- Eventual test-spec readiness: <ready | conditionally-ready | not-ready>\n"
                            "- Stop condition: <none or stop condition>\n"
                        ),
                    ),
                    "assets/material-finding.md": self.review_family_asset_text(
                        template="spec-review-material-finding-v1",
                        skill="spec-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding ID: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                            "- needs-decision rationale: <needs-decision rationale>\n"
                        ),
                    ),
                },
            )

            errors = skill_validation.validate_spec_review_canonical_contract(
                skill_dir / "SKILL.md"
            )

        self.assertIn(
            "spec-review result skeleton Immediate next stage enum must exclude test-spec",
            "\n".join(errors),
        )

    def test_spec_review_canonical_contract_rejects_duplicate_material_field_list(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill_dir = self.write_spec_family_asset_fixture(
                root,
                "spec-review",
                {
                    "assets/review-result-skeleton.md": self.spec_family_asset_text(
                        template="spec-review-result-skeleton-v1",
                        skill="spec-review",
                        body=(
                            "## Result\n\n"
                            "- Review status: <approved | changes-requested | blocked | inconclusive>\n"
                            "- Immediate next stage: <spec revision | review-resolution | architecture | plan | none>\n"
                            "- Eventual test-spec readiness: <ready | conditionally-ready | not-ready>\n"
                            "- Stop condition: <none or stop condition>\n"
                        ),
                    ),
                    "assets/material-finding.md": self.review_family_asset_text(
                        template="spec-review-material-finding-v1",
                        skill="spec-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding ID: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                            "- needs-decision rationale: <needs-decision rationale>\n"
                        ),
                    ),
                },
            )
            skill_path = skill_dir / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8")
                + textwrap.dedent(
                    """

                    ## Isolation and Recording

                    Material findings must include:

                    - Finding ID
                    - Severity
                    - Location
                    - Evidence
                    - Required outcome
                    - Safe resolution path
                    """
                ),
                encoding="utf-8",
            )

            errors = skill_validation.validate_spec_review_canonical_contract(skill_path)

        self.assertIn(
            "spec-review SKILL.md must not re-enumerate the complete material-finding field list outside the Resource map",
            "\n".join(errors),
        )

    def test_spec_review_routing_adjacent_skills_preserve_direct_contracts(self) -> None:
        plan_review = (ROOT / "skills" / "plan-review" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        test_spec = (ROOT / "skills" / "test-spec" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        workflow_spec = (ROOT / "specs" / "rigorloop-workflow.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("- Immediate next stage: <test-spec | plan revision | blocked>", plan_review)
        self.assertIn("implementation-readiness notes only when clearly downstream", plan_review)
        self.assertNotIn("not-assessed", test_spec)
        self.assertIn("eventual `test-spec` readiness as `not-ready`", test_spec)
        self.assertNotIn("not-assessed", workflow_spec)
        self.assertIn("spec revision", workflow_spec)
        self.assertIn("review-resolution", workflow_spec)
        self.assertIn("Immediate next stage", workflow_spec)
        self.assertIn("Immediate next stage: none", workflow_spec)
        self.assertNotIn(
            "without naming any immediate next repository stage", workflow_spec
        )
        self.assertNotIn("no immediate-next-stage value", workflow_spec)
        self.assertNotIn("no immediate next-stage value", workflow_spec)
        self.assertIn(
            "Only `architecture` and `plan` are forward repository-stage handoff values",
            workflow_spec,
        )
        self.assertIn(
            "`spec revision`, `review-resolution`, and `none` are routing or no-handoff values",
            workflow_spec,
        )

    def assertSpecReviewResultPasses(self, result_text: str) -> None:
        errors = skill_validation.validate_spec_review_result_fields(
            textwrap.dedent(result_text)
        )
        self.assertEqual(errors, [])

    def assertSpecReviewResultFails(self, result_text: str, expected_text: str) -> None:
        errors = skill_validation.validate_spec_review_result_fields(
            textwrap.dedent(result_text)
        )
        self.assertTrue(errors, "expected controlled spec-review result fixture to fail")
        self.assertIn(expected_text, "\n".join(errors))

    def test_spec_review_result_fixture_accepts_allowed_immediate_next_stage_values(self) -> None:
        fixtures = {
            "spec revision": (
                "Review status: changes-requested\n"
                "Immediate next stage: spec revision\n"
                "Eventual test-spec readiness: not-ready\n"
                "Stop condition: none\n"
            ),
            "review-resolution": (
                "Review status: blocked\n"
                "Immediate next stage: review-resolution\n"
                "Eventual test-spec readiness: not-ready\n"
                "Stop condition: material findings require disposition\n"
            ),
            "architecture": (
                "Review status: approved\n"
                "Immediate next stage: architecture\n"
                "Eventual test-spec readiness: conditionally-ready\n"
                "Readiness condition: architecture must be completed before test-spec authoring\n"
                "Stop condition: none\n"
            ),
            "plan": (
                "Review status: approved\n"
                "Immediate next stage: plan\n"
                "Eventual test-spec readiness: ready\n"
                "Stop condition: none\n"
            ),
            "none": (
                "Review status: inconclusive\n"
                "Immediate next stage: none\n"
                "Eventual test-spec readiness: not-ready\n"
                "Stop condition: missing reviewer input\n"
            ),
        }

        for stage, fixture in fixtures.items():
            with self.subTest(stage=stage):
                self.assertSpecReviewResultPasses(fixture)

    def test_spec_review_result_fixture_rejects_test_spec_as_immediate_next_stage(self) -> None:
        self.assertSpecReviewResultFails(
            """
            Review status: approved
            Immediate next stage: test-spec
            Eventual test-spec readiness: ready
            Stop condition: none
            """,
            "Immediate next stage must not be test-spec",
        )

    def test_spec_review_result_fixture_rejects_pseudo_routing_values(self) -> None:
        for stage in ("blocker handling", "missing-context resolution", "ready for test-spec"):
            with self.subTest(stage=stage):
                self.assertSpecReviewResultFails(
                    f"""
                    Review status: blocked
                    Immediate next stage: {stage}
                    Eventual test-spec readiness: not-ready
                    Stop condition: blocker
                    """,
                    "Immediate next stage is not an allowed value",
                )

    def test_spec_review_result_fixture_rejects_approved_not_ready(self) -> None:
        self.assertSpecReviewResultFails(
            """
            Review status: approved
            Immediate next stage: plan
            Eventual test-spec readiness: not-ready
            Stop condition: none
            """,
            "approved requires Eventual test-spec readiness ready or conditionally-ready",
        )

    def test_spec_review_result_fixture_rejects_not_assessed_readiness(self) -> None:
        self.assertSpecReviewResultFails(
            """
            Review status: inconclusive
            Immediate next stage: none
            Eventual test-spec readiness: not-assessed
            Stop condition: missing reviewer input
            """,
            "Eventual test-spec readiness must not be not-assessed",
        )

    def test_spec_review_result_fixture_rejects_status_to_routing_contradictions(self) -> None:
        invalid = {
            "approved spec revision": (
                "Review status: approved\n"
                "Immediate next stage: spec revision\n"
                "Eventual test-spec readiness: ready\n"
                "Stop condition: none\n",
                "approved requires Immediate next stage architecture or plan",
            ),
            "approved review-resolution": (
                "Review status: approved\n"
                "Immediate next stage: review-resolution\n"
                "Eventual test-spec readiness: ready\n"
                "Stop condition: none\n",
                "approved requires Immediate next stage architecture or plan",
            ),
            "approved none": (
                "Review status: approved\n"
                "Immediate next stage: none\n"
                "Eventual test-spec readiness: ready\n"
                "Stop condition: none\n",
                "approved requires Immediate next stage architecture or plan",
            ),
            "changes-requested plan": (
                "Review status: changes-requested\n"
                "Immediate next stage: plan\n"
                "Eventual test-spec readiness: not-ready\n"
                "Stop condition: none\n",
                "changes-requested requires Immediate next stage spec revision or review-resolution",
            ),
            "blocked architecture": (
                "Review status: blocked\n"
                "Immediate next stage: architecture\n"
                "Eventual test-spec readiness: not-ready\n"
                "Stop condition: blocker\n",
                "blocked requires Immediate next stage review-resolution or none",
            ),
            "inconclusive plan": (
                "Review status: inconclusive\n"
                "Immediate next stage: plan\n"
                "Eventual test-spec readiness: not-ready\n"
                "Stop condition: missing input\n",
                "inconclusive requires Immediate next stage none",
            ),
        }

        for name, (fixture, expected) in invalid.items():
            with self.subTest(name=name):
                self.assertSpecReviewResultFails(fixture, expected)

    def test_spec_review_result_fixture_requires_stop_condition_for_inconclusive(self) -> None:
        self.assertSpecReviewResultFails(
            """
            Review status: inconclusive
            Immediate next stage: none
            Eventual test-spec readiness: not-ready
            Stop condition: none
            """,
            "inconclusive requires a concrete Stop condition",
        )

    def test_spec_review_result_fixture_requires_condition_for_conditionally_ready(self) -> None:
        self.assertSpecReviewResultFails(
            """
            Review status: approved
            Immediate next stage: architecture
            Eventual test-spec readiness: conditionally-ready
            Stop condition: none
            """,
            "conditionally-ready requires a named condition",
        )

    def test_review_family_material_finding_requires_parser_owned_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "code-review",
                {
                    "assets/material-finding.md": self.review_family_asset_text(
                        template="code-review-material-finding-v1",
                        skill="code-review",
                        body=(
                            "## Finding <finding id>\n\n"
                            "- Finding: <finding id>\n"
                            "- Severity: <severity>\n"
                            "- Location: <location>\n"
                            "- Evidence: <evidence>\n"
                            "- Required outcome: <required outcome>\n"
                            "- Safe resolution path: <safe resolution path>\n"
                        ),
                    ),
                    "assets/review-result-skeleton.md": self.review_family_asset_text(
                        template="code-review-result-skeleton-v1",
                        skill="code-review",
                        body="- Review status: <review status>\n",
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "review-family material-finding must include parser-owned label 'Finding ID:'",
                result.stdout + result.stderr,
            )

    def test_review_family_material_finding_field_block_must_match_across_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common_finding = (
                "## Finding <finding id>\n\n"
                "- Finding ID: <finding id>\n"
                "- Severity: <severity>\n"
                "- Location: <location>\n"
                "- Evidence: <evidence>\n"
                "- Required outcome: <required outcome>\n"
                "- Safe resolution path: <safe resolution path>\n"
                "- needs-decision rationale: <needs-decision rationale>\n"
            )
            changed_finding = common_finding.replace(
                "- Evidence: <evidence>\n- Required outcome: <required outcome>\n",
                "- Required outcome: <required outcome>\n- Evidence: <evidence>\n",
            )
            for skill_name, finding_body in (
                ("code-review", common_finding),
                ("proposal-review", common_finding),
                ("spec-review", changed_finding),
            ):
                result_body = "- Review status: <review status>\n"
                if skill_name == "proposal-review":
                    result_body = "## Result\n\n- Skill: proposal-review\n- Review status: <review status>\n"
                self.write_spec_family_asset_fixture(
                    root,
                    skill_name,
                    {
                        "assets/material-finding.md": self.review_family_asset_text(
                            template=f"{skill_name}-material-finding-v1",
                            skill=skill_name,
                            body=finding_body,
                        ),
                        "assets/review-result-skeleton.md": self.review_family_asset_text(
                            template=f"{skill_name}-result-skeleton-v1",
                            skill=skill_name,
                            body=result_body,
                        ),
                    },
                )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "review-family material-finding parser-owned field block must be byte-identical across first-slice review skills",
                result.stdout + result.stderr,
            )

    def test_review_family_asset_policy_field_labels_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_spec_family_asset_fixture(
                root,
                "code-review",
                {
                    "assets/material-finding.md": self.review_family_asset_text(
                        template="code-review-material-finding-v1",
                        skill="code-review",
                        body="- Severity: <severity>\n",
                    ),
                    "assets/review-result-skeleton.md": self.review_family_asset_text(
                        template="code-review-result-skeleton-v1",
                        skill="code-review",
                        body="- Severity policy: <policy>\n",
                    ),
                },
            )

            result = run_validator(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "review-family asset 'assets/review-result-skeleton.md' must not contain review-policy labels or guidance",
                result.stdout + result.stderr,
            )

    def test_proposal_family_baseline_summary_records_required_surfaces(self) -> None:
        baseline = (
            ROOT
            / "docs"
            / "changes"
            / "2026-05-20-proposal-family-assets-progressive-disclosure"
            / "baseline.md"
        )
        self.assertTrue(baseline.exists())
        text = baseline.read_text(encoding="utf-8")
        for required in [
            "Source commit or branch point",
            "skills/proposal/SKILL.md",
            "skills/proposal-review/SKILL.md",
            "Source file hashes",
            "Existing full skeleton section set",
            "Repeated substructure fields to extract",
            "Conditional sections governed by `SKILL.md`",
            "Closed enums that remain in `SKILL.md`",
            "Scope-preservation and scope-budget rules that remain in `SKILL.md`",
            "Vision fit and standing artifact gate rules that remain in `SKILL.md`",
            "Review dimensions and recording obligations that remain in `SKILL.md`",
            "Source location for each extracted asset",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_published_design_routing_coverage_fixture_is_bounded(self) -> None:
        routing = (
            ROOT
            / "docs"
            / "changes"
            / "2026-05-19-rigorloop-published-skill-design-contract"
            / "routing-coverage.md"
        ).read_text(encoding="utf-8")

        self.assertIn("This evidence is a fixture and transcript-review input.", routing)
        self.assertIn("It does not claim deterministic runtime skill auto-selection.", routing)
        self.assertIn("| Skill | Positive triggers | Near misses | Competing skills | Should-not-trigger prompt classes |", routing)
        for skill in ("`proposal`", "`proposal-review`"):
            with self.subTest(skill=skill):
                self.assertIn(f"| {skill} |", routing)
        for fixture_type in (
            "Obvious positive",
            "Casual positive",
            "Edge positive",
            "Near negative",
            "Competing skill",
            "Should not trigger",
        ):
            with self.subTest(fixture_type=fixture_type):
                self.assertIn(fixture_type, routing)
        forbidden_claims = [
            "proves automatic runtime selection",
            "CI proves runtime skill selection",
            "use broad semantic scoring",
        ]
        for claim in forbidden_claims:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, routing)

    def test_published_design_spec_family_routing_coverage_fixture_is_bounded(self) -> None:
        routing = (
            ROOT
            / "docs"
            / "changes"
            / "2026-05-19-published-skill-design-spec-family"
            / "routing-coverage.md"
        ).read_text(encoding="utf-8")

        self.assertIn("This evidence is a fixture and transcript-review input.", routing)
        self.assertIn("It does not claim deterministic runtime skill auto-selection.", routing)
        self.assertIn("| Skill | Positive triggers | Near misses | Competing skills | Should-not-trigger prompt classes |", routing)
        for skill in ("`spec`", "`spec-review`"):
            with self.subTest(skill=skill):
                self.assertIn(f"| {skill} |", routing)
        for fixture_type in (
            "Obvious positive",
            "Casual positive",
            "Edge positive",
            "Near negative",
            "Competing skill",
            "Should not trigger",
        ):
            with self.subTest(fixture_type=fixture_type):
                self.assertIn(fixture_type, routing)
        forbidden_claims = [
            "proves automatic runtime selection",
            "CI proves runtime skill selection",
            "use broad semantic scoring",
        ]
        for claim in forbidden_claims:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, routing)

    def test_published_design_plan_family_routing_coverage_fixture_is_bounded(self) -> None:
        routing = (
            ROOT
            / "docs"
            / "changes"
            / "2026-05-19-published-skill-design-plan-family"
            / "routing-coverage.md"
        ).read_text(encoding="utf-8")

        self.assertIn("prompt\nfixtures evaluate description coverage and transcript behavior", routing)
        self.assertIn("do not\nclaim deterministic runtime model auto-selection", routing)
        for required_field in (
            "positive triggers",
            "near misses",
            "competing skills",
            "should-not-trigger classes",
        ):
            with self.subTest(required_field=required_field):
                self.assertIn(required_field, routing)
        for skill in ("`plan`", "`plan-review`"):
            with self.subTest(skill=skill):
                self.assertIn(f"## {skill}", routing)
        for fixture_type in (
            "obvious positive",
            "casual positive",
            "edge positive",
            "near negative",
            "competing skill",
            "should not trigger",
        ):
            with self.subTest(fixture_type=fixture_type):
                self.assertIn(fixture_type, routing)
        forbidden_claims = [
            "proves automatic runtime selection",
            "CI proves runtime skill selection",
            "use broad semantic scoring",
        ]
        for claim in forbidden_claims:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, routing)

    def test_published_design_spec_family_audit_records_deterministic_gaps(self) -> None:
        audit = (
            ROOT
            / "docs"
            / "changes"
            / "2026-05-19-published-skill-design-spec-family"
            / "skill-audit.md"
        ).read_text(encoding="utf-8")

        for skill in ("`spec`", "`spec-review`"):
            with self.subTest(skill=skill):
                self.assertIn(f"| {skill} |", audit)
                self.assertIn("description routing gap", audit)
                self.assertIn("missing near-miss boundary", audit)
                self.assertIn("missing workflow role", audit)
                self.assertIn("missing compact output skeleton", audit)
        self.assertIn("No packaged `references/`, `scripts/`, or `assets/` directories exist", audit)
        self.assertIn("Both target skills earn their existence", audit)
        self.assertIn("None recorded in this audit.", audit)

    def test_published_design_plan_family_audit_records_deterministic_gaps(self) -> None:
        audit = (
            ROOT
            / "docs"
            / "changes"
            / "2026-05-19-published-skill-design-plan-family"
            / "skill-audit.md"
        ).read_text(encoding="utf-8")

        for skill in ("`plan`", "`plan-review`"):
            with self.subTest(skill=skill):
                self.assertIn(f"| {skill} |", audit)
                self.assertIn("description routing gap", audit)
                self.assertIn("missing near-miss boundary", audit)
                self.assertIn("missing workflow role", audit)
                self.assertIn("missing output template", audit)
        self.assertIn("Neither ships packaged `references/`, `scripts/`, or `assets/` resources", audit)
        self.assertIn("Both skills earn their existence", audit)
        self.assertIn("M1 did not identify a production validator gap", audit)
        self.assertIn("None.", audit)

    def test_published_design_spec_family_preservation_and_parity_are_scaffolded(self) -> None:
        change_root = ROOT / "docs" / "changes" / "2026-05-19-published-skill-design-spec-family"
        preservation = (change_root / "behavior-preservation.md").read_text(encoding="utf-8")
        parity = (change_root / "behavior-parity.md").read_text(encoding="utf-8")

        for skill in ("`spec`", "`spec-review`"):
            with self.subTest(skill=skill):
                self.assertIn(f"| {skill} |", preservation)
                self.assertNotIn(f"| {skill} | pending M3 | pending M3 | pending M3 |", preservation)
                self.assertIn(skill, parity)
        for artifact_id in ("`SF-PARITY-1`", "`SF-PARITY-2`", "`SF-PARITY-3`"):
            with self.subTest(artifact_id=artifact_id):
                self.assertIn(artifact_id, parity)
        self.assertIn("M3 must not close on structural validation alone", preservation)
        self.assertIn("M3 must not claim behavior parity from structural validation alone", parity)
        self.assertIn("## M3 Preservation Result", preservation)
        self.assertIn("## M3 Final Parity Statement", parity)
        self.assertIn("| `spec` | 9164 | 192 | 2288 |", parity)
        self.assertIn("| `spec-review` | 7968 | 183 | 1992 |", parity)

    def test_published_design_execution_review_evidence_is_scaffolded(self) -> None:
        change_root = (
            ROOT
            / "docs"
            / "changes"
            / "2026-05-19-published-skill-design-implement-code-review"
        )
        audit = (change_root / "skill-audit.md").read_text(encoding="utf-8")
        routing = (change_root / "routing-coverage.md").read_text(encoding="utf-8")
        preservation = (change_root / "behavior-preservation.md").read_text(encoding="utf-8")
        parity = (change_root / "behavior-parity.md").read_text(encoding="utf-8")

        for skill in ("`implement`", "`code-review`"):
            with self.subTest(skill=skill):
                self.assertIn(f"| {skill} | yes |", audit)
                self.assertIn(f"## {skill}", routing)
                self.assertIn(f"| {skill} |", preservation)
                self.assertIn(skill, parity)
        for fixture_type in (
            "Obvious positive",
            "Casual positive",
            "Edge positive",
            "Near negative",
            "Competing skill",
            "Should not trigger",
        ):
            with self.subTest(fixture_type=fixture_type):
                self.assertIn(fixture_type, routing)
        self.assertIn("They do not claim runtime model auto-selection in CI.", routing)
        self.assertIn("No merge or retire candidate is approved in this slice.", audit)
        self.assertIn("| `implement` | 4421 |", audit)
        self.assertIn("| `code-review` | 5054 |", audit)
        self.assertIn("M3 must fill final evidence", preservation)
        self.assertIn("M3 must confirm the rewrite preserves these outcomes", parity)

    def test_published_design_plan_family_preservation_and_parity_are_scaffolded(self) -> None:
        change_root = ROOT / "docs" / "changes" / "2026-05-19-published-skill-design-plan-family"
        preservation = (change_root / "behavior-preservation.md").read_text(encoding="utf-8")
        parity = (change_root / "behavior-parity.md").read_text(encoding="utf-8")

        for skill in ("`plan`", "`plan-review`"):
            with self.subTest(skill=skill):
                self.assertIn(f"| {skill} |", preservation)
                self.assertIn(skill, parity)
                self.assertNotIn(f"| {skill} | pending", parity)
        for required_rule in (
            "Current Handoff Summary",
            "Upstream status settlement",
            "formal lifecycle review",
            "review-log.md",
            "test-spec",
        ):
            with self.subTest(required_rule=required_rule):
                self.assertIn(required_rule, preservation)
        for case_id in (
            "PLAN-P1",
            "PLAN-P2",
            "PLAN-P3",
            "PLAN-P4",
            "PLAN-P5",
            "PRV-P1",
            "PRV-P2",
            "PRV-P3",
            "PRV-P4",
            "PRV-P5",
        ):
            with self.subTest(case_id=case_id):
                self.assertIn(case_id, parity)
        self.assertIn("| `plan` | 14070 | 303 | 3518 | 15447 | 317 | 3862 | +344 | +9.78% | within +10% hard cap |", parity)
        self.assertIn("| `plan-review` | 6529 | 165 | 1631 | 7183 | 157 | 1794 | +163 | +9.99% | within +10% hard cap |", parity)
        self.assertIn("## M3 Preservation Result", preservation)
        self.assertIn("## M3 Final Parity Statement", parity)
        self.assertIn("No lifecycle behavior weakening was found", parity)

    def test_skill_readability_pilot_pair_opts_into_contract(self) -> None:
        for skill_name in ("proposal", "proposal-review"):
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            result = run_validator(skill_path)
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=(
                        f"expected {skill_name} to satisfy the readability contract\n"
                        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                    ),
                )
                body = skill_path.read_text(encoding="utf-8")
                self.assertIn("schema-version: skill-readability-v1", body)
                self.assertIn("## Workflow role", body)
                self.assertIn("## Output skeleton", body)

    def test_skill_readability_spec_family_opts_into_contract(self) -> None:
        for skill_name in ("spec", "spec-review"):
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            result = run_validator(skill_path)
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=(
                        f"expected {skill_name} to satisfy the readability contract\n"
                        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                    ),
                )
                body = skill_path.read_text(encoding="utf-8")
                self.assertIn("schema-version: skill-readability-v1", body)
                self.assertIn("## Workflow role", body)
                self.assertIn("## Output skeleton", body)

    def test_skill_readability_execution_review_opts_into_contract(self) -> None:
        for skill_name in ("implement", "code-review"):
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            result = run_validator(skill_path)
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=(
                        f"expected {skill_name} to satisfy the readability contract\n"
                        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                    ),
                )
                body = skill_path.read_text(encoding="utf-8")
                self.assertIn("schema-version: skill-readability-v1", body)
                self.assertIn("## Workflow role", body)
                self.assertIn("## Output skeleton", body)

    def test_skill_readability_plan_family_opts_into_contract(self) -> None:
        for skill_name in ("plan", "plan-review"):
            skill_path = ROOT / "skills" / skill_name / "SKILL.md"
            result = run_validator(skill_path)
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    result.returncode,
                    0,
                    msg=(
                        f"expected {skill_name} to satisfy the readability contract\n"
                        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                    ),
                )
                body = skill_path.read_text(encoding="utf-8")
                self.assertIn("schema-version: skill-readability-v1", body)
                self.assertIn("## Workflow role", body)
                self.assertIn("## Output skeleton", body)

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
            "## Architecture Surface Decision",
            "Choose the smallest valid architecture action.",
            "No architecture impact",
            "Direction unclear",
            "Spec unclear",
            "Clear architecture update",
            "Durable decision",
            "Do not create temporary architecture documents to resolve direction uncertainty.",
            "Use the project's canonical architecture package.",
            "Common default paths are:",
            "`docs/architecture/system/architecture.md`",
            "`docs/architecture/system/diagrams/`",
            "`docs/adr/`",
            "If the project uses different architecture paths, follow the project's configured paths.",
            "C4 system context diagram",
            "C4 container diagram",
            "## Resource map",
            "COPY `assets/architecture-skeleton.md`",
            "COPY `assets/adr-skeleton.md`",
            "COPY `assets/diagram-styles.mmd`",
            "Use the architecture skeleton for section structure.",
            "```mermaid\nC4Context",
            "```mermaid\nC4Container",
            "## ADR Triggers",
            "skills/architecture/references/architecture-example.md",
            "- Architecture surface: no-impact-rationale | canonical-update | ADR | blocked",
            "- Direction/spec blockers:",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

        forbidden_terms = [
            "`docs/changes/<change-id>/architecture.md`",
            "Change-local working architecture lives",
            "Use a change-local architecture delta",
            "Merge accepted durable content from change-local deltas",
            "merge-back",
            "`specs/architecture-package-method.md`",
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
            "## Review Surface",
            "Classify the review surface before reviewing:",
            "`canonical-architecture-update`",
            "`ADR`",
            "`no-architecture-impact-rationale`",
            "`proposal-or-spec-gap`",
            "Review the changed canonical architecture sections, diagrams, and ADR links directly.",
            "Do not require a change-local architecture delta for a canonical architecture update.",
            "Review the ADR for context, decision, alternatives, consequences, and compatibility with the canonical architecture.",
            "Check whether the no-architecture-impact rationale is credible.",
            "If the design direction is unresolved, return a finding that routes back to `proposal` or proposal revision.",
            "If behavior is unsettled, route to `spec` or spec revision.",
            "Do not use architecture-review to settle product direction.",
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

        forbidden_terms = [
            "Change-local delta:",
            "Merge-back:",
            "docs/changes/<change-id>/architecture.md",
            "`specs/architecture-package-method.md`",
            "must not compete with the canonical package",
            "when merge-back from a change-local delta may affect multiple sections",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, body)

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
        ci = (ROOT / "skills" / "ci-maintenance" / "SKILL.md").read_text(encoding="utf-8")
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
            "hands off to `pr`",
            "ci-maintenance",
            "hosted workflow automation, validation automation, or related platform configuration",
        ]
        for term in verify_terms:
            with self.subTest(skill="verify", term=term):
                self.assertIn(term, verify)
        self.assertNotIn("next required or default downstream stage", verify)
        self.assertNotIn("downstream stage is `ci`", verify)

    def test_customer_project_portability_workflow_guide(self) -> None:
        workflow_guide = (ROOT / "docs" / "workflows.md").read_text(encoding="utf-8")
        block = extract_markdown_block(workflow_guide, "Customer-project portability")

        required_terms = [
            "Public skills operate in customer-project mode by default.",
            "Use project-local artifacts when present",
            "`docs/workflows.md`",
            "`rigorloop.yaml`",
            "`rigorloop.lock`",
            "`docs/changes/<change-id>/change.yaml`",
            "Do not require RigorLoop repository-internal `specs/`, `docs/`, `CONSTITUTION.md`, `AGENTS.md`, reports, or follow-up files in a customer project.",
            "portable defaults where safe",
            "block on ambiguity",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, block)

        self.assertNotIn("must read RigorLoop", block)
        self.assertNotIn("required precondition for every task", block)

    def test_workflow_skill_customer_project_guide_caveat(self) -> None:
        workflow = (ROOT / "skills" / "workflow" / "SKILL.md").read_text(encoding="utf-8")
        block = extract_markdown_block(workflow, "Customer-project workflow guide")

        required_terms = [
            "create or refresh the project-local `docs/workflows.md`",
            "RigorLoop is being adopted",
            "artifact locations are missing",
            "routing depends on local workflow guidance",
            "Do not require RigorLoop repository-internal specs or docs to be present.",
            "Use project-local guidance when available",
            "portable defaults",
            "block on ambiguity",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, block)

    def test_customer_portable_public_skills_define_project_local_evidence_contract(self) -> None:
        for skill_name in CUSTOMER_PORTABLE_M2_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            block = extract_markdown_block(body, "Project-local evidence")

            required_terms = [
                "customer-project mode by default",
                "project-local",
                "RigorLoop repository-internal",
                "portable defaults",
                "block on ambiguity",
                "`docs/workflows.md`",
            ]
            for term in required_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, block)

    def test_project_map_treats_local_orientation_inputs_as_optional(self) -> None:
        project_map = (ROOT / "skills" / "project-map" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        block = extract_markdown_block(project_map, "Customer-project orientation")

        required_terms = [
            "customer-project mode by default",
            "optional project-local orientation inputs",
            "absence is normal",
            "Do not search for RigorLoop originals",
            "`AGENTS.md`",
            "`CONSTITUTION.md`",
            "`docs/`",
            "`specs/`",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, block)

    def test_customer_portable_required_internal_dependency_detector_examples(self) -> None:
        forbidden_examples = [
            "must read RigorLoop specs/ before drafting",
            "required: read RigorLoop CONSTITUTION.md",
            "must first read RigorLoop AGENTS.md",
            "read the RigorLoop workflow spec before proceeding",
            "required: docs/reports/token-cost/releases/latest.md",
        ]
        for example in forbidden_examples:
            with self.subTest(example=example):
                self.assertTrue(
                    any(
                        pattern.search(example)
                        for pattern in CUSTOMER_PORTABLE_REQUIRED_INTERNAL_DEPENDENCY_PATTERNS.values()
                    )
                )
                self.assertFalse(has_customer_portable_guard(example))

        allowed_examples = [
            "Read local specs/ if present and relevant.",
            "Use project-local `CONSTITUTION.md` when governing project docs exist.",
            "Use RigorLoop repository docs when operating inside the RigorLoop repository.",
            "Read `AGENTS.md` when this file is the review target.",
            "Use `docs/workflows.md` when the user provided this path.",
            "Use RigorLoop specs/ only when the file is the direct target.",
        ]
        for example in allowed_examples:
            with self.subTest(example=example):
                matched = any(
                    pattern.search(example)
                    for pattern in CUSTOMER_PORTABLE_REQUIRED_INTERNAL_DEPENDENCY_PATTERNS.values()
                )
                self.assertFalse(matched and not has_customer_portable_guard(example))

    def test_published_skill_surfaces_block_required_rigorloop_internal_dependencies(self) -> None:
        for path in iter_published_skill_text_surfaces():
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in CUSTOMER_PORTABLE_REQUIRED_INTERNAL_DEPENDENCY_PATTERNS.items():
                for match in pattern.finditer(body):
                    start = max(match.start() - 160, 0)
                    end = min(match.end() + 160, len(body))
                    surrounding = body[start:end]
                    with self.subTest(path=str(relative_path), forbidden=label):
                        self.assertTrue(has_customer_portable_guard(surrounding))

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
        asset_owned_material_terms = {
            "Severity",
            "Location",
            "Evidence",
            "Required outcome",
            "Safe resolution path",
        }
        skill_required_terms = [
            "Every formal lifecycle review result must be recorded or explicitly blocked.",
            "lightweight review receipt",
            "review-log.md",
            "Do not create an\nempty `review-resolution.md` solely for a clean review.",
            "For material findings or blocking outcomes, create the required detailed review\nrecord",
            "Finding ID",
            "Severity",
            "Location",
            "Evidence",
            "Required outcome",
            "Safe resolution path",
            "`needs-decision` rationale",
        ]
        skill_forbidden_terms = [
            "detailed review record triggers",
            "stage-owned non-approval outcomes that block downstream progress or require revision",
            "reconstructed review evidence",
            "closeout evidence citation",
            "clean receipt root",
            "review.status must be",
            "unresolved_items",
            "reviewed_artifact",
            "review_log",
            "Generated review-recording change ID",
        ]
        for skill_name in FORMAL_REVIEW_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            material_asset = ""
            if skill_name == "spec-review":
                material_asset = (
                    ROOT / "skills" / skill_name / "assets" / "material-finding.md"
                ).read_text(encoding="utf-8")
            for term in skill_required_terms:
                with self.subTest(skill=skill_name, term=term):
                    if skill_name == "spec-review" and term in asset_owned_material_terms:
                        self.assertIn(f"- {term}:", material_asset)
                    else:
                        self.assertIn(term, body)
            for term in skill_forbidden_terms:
                with self.subTest(skill=skill_name, forbidden_term=term):
                    self.assertNotIn(term, body)

        spec = FORMAL_REVIEW_RECORDING_SPEC.read_text(encoding="utf-8")
        spec_required_terms = [
            "stage-owned non-approval outcome",
            "reconstructed evidence",
            "closeout evidence",
            "reviewer or maintainer explicitly requests",
            "`pr-review`",
        ]
        for term in spec_required_terms:
            with self.subTest(file="spec", term=term):
                self.assertIn(term, spec)

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
                if skill_name == "spec-review":
                    self.assertIn(
                        "Use `assets/material-finding.md` for each material finding block.",
                        copied,
                    )
                else:
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

    def test_formal_review_skills_define_recording_status_output(self) -> None:
        asset_owned_material_terms = {
            "Severity",
            "Location",
            "Evidence",
            "Required outcome",
            "Safe resolution path",
        }
        required_terms = [
            "Every formal lifecycle review result must be recorded or explicitly blocked.",
            "`Recording status: recorded`",
            "`Recording status: blocked`",
            "`not-required` is reserved for non-formal review-like requests",
            "Review record",
            "Review log",
            "Review resolution",
            "Finding ID",
            "Severity",
            "Location",
            "Evidence",
            "Required outcome",
            "Safe resolution path",
            "`needs-decision` rationale",
            "Do not merely tell the user that review artifacts should be created.",
            "smallest next action",
        ]
        forbidden_exact_fields = [
            "- Status settlement recommendation:",
            "- Status sync:",
            "- Status artifact:",
            "- Status sync blocker:",
        ]
        forbidden_long_change_id_terms = [
            "YYYY-MM-DD-<reviewed-artifact-or-topic>-review-recording",
            "Generated review-recording change ID",
            "Existing active change root",
        ]

        for skill_name in FORMAL_REVIEW_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            material_asset = ""
            if skill_name == "spec-review":
                material_asset = (
                    ROOT / "skills" / skill_name / "assets" / "material-finding.md"
                ).read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(skill=skill_name, term=term):
                    if skill_name == "spec-review" and term in asset_owned_material_terms:
                        self.assertIn(f"- {term}:", material_asset)
                    else:
                        self.assertIn(term, body)
            for term in forbidden_exact_fields:
                with self.subTest(skill=skill_name, forbidden_field=term):
                    self.assertNotIn(term, body)
            for term in forbidden_long_change_id_terms:
                with self.subTest(skill=skill_name, long_rule=term):
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
            "For a clean review, create the lightweight review receipt required by the formal review recording spec",
            "Do not create an empty `review-resolution.md` solely for a clean review.",
            "For material findings or blocking outcomes, create the required detailed review record",
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
        required_terms = [
            "Material review findings",
            "always",
            "All material findings require",
            "change-local review",
            "Isolation",
            "handoff",
            "not recording",
            "Every supported formal lifecycle review",
            "clean review receipt",
        ]
        for relative_path in ["CONSTITUTION.md", "AGENTS.md", "docs/workflows.md"]:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in required_terms:
                with self.subTest(path=relative_path, term=term):
                    self.assertIn(term, body)
            with self.subTest(path=relative_path, term="old clean review settlement"):
                self.assertNotIn(
                    "Clean reviews may settle artifact-locally when no detailed-record trigger applies",
                    body,
                )

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

    def test_downstream_status_settlement_first_slice_skill_guidance(self) -> None:
        def extract_fenced_block_after_heading(
            body: str,
            heading: str,
            *,
            start_after: str | None = None,
        ) -> list[str]:
            search_start = 0
            if start_after is not None:
                search_start = body.find(start_after)
                self.assertNotEqual(search_start, -1, f"missing start marker {start_after!r}")
            heading_index = body.find(heading, search_start)
            self.assertNotEqual(heading_index, -1, f"missing heading {heading!r}")
            fence_start = body.find("```text", heading_index)
            self.assertNotEqual(fence_start, -1, f"missing fenced block after {heading!r}")
            value_start = body.find("\n", fence_start)
            self.assertNotEqual(value_start, -1, f"malformed fenced block after {heading!r}")
            fence_end = body.find("```", value_start + 1)
            self.assertNotEqual(fence_end, -1, f"unterminated fenced block after {heading!r}")
            return [
                line.strip()
                for line in body[value_start + 1 : fence_end].splitlines()
                if line.strip()
            ]

        common_required_terms = [
            "Upstream status settlement",
            "workflow-managed downstream execution",
            "review-only",
            "no-edit",
            "do not ask whether edits are allowed",
            "lifecycle/status/readiness/follow-on/closeout metadata",
            "Do not rewrite substantive artifact content",
            "clear review evidence",
            "approving or clean",
            "no later contradictory review record",
            "review-log.md",
            "review-resolution.md",
            "artifact type, lifecycle field, next status, or target status is unknown or unmapped",
            "block instead of inferring a settlement",
            "Settlement result:",
            "New status",
            "not-applicable",
            "Settlement blocker",
            "blocked settlement with a deterministic target",
            "blocked settlement with no deterministic target",
            "known target blocked by evidence/state",
            "unknown target blocked by missing mapping or lifecycle vocabulary",
            "updated, blocked, or stale status was detected",
        ]
        skill_specific_terms = {
            "spec": [
                "proposal-review approved",
                "proposal `Status: accepted`",
                "<settlement result>",
                "## Closed enums",
                "Settlement result:",
            ],
            "architecture": [
                "spec-review approved",
                "spec `Status: approved`",
                "Settlement result: updated | blocked | not-needed",
            ],
            "plan": [
                "spec-review approved",
                "spec `Status: approved`",
                "architecture-review approved",
                "architecture `Status: approved`",
                "ADR",
                "`accepted` or `active`",
                "unknown lifecycle vocabulary",
                "Settlement result: updated | blocked | not-needed",
            ],
        }

        for skill_name in DOWNSTREAM_STATUS_SETTLEMENT_FIRST_SLICE_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in common_required_terms + skill_specific_terms[skill_name]:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)
            if skill_name == "spec":
                with self.subTest(skill=skill_name, enum="settlement result"):
                    self.assertEqual(
                        extract_fenced_block_after_heading(
                            body,
                            "Settlement result:",
                            start_after="## Closed enums",
                        ),
                        ["updated", "blocked", "not-needed"],
                    )
                    self.assertNotIn(
                        "Settlement result: updated | blocked | not-needed",
                        body,
                    )

    def test_downstream_status_settlement_first_slice_boundaries(self) -> None:
        forbidden_operational_terms = [
            "## Upstream status settlement",
            "Settlement result: updated | blocked | not-needed",
        ]
        for skill_name in DOWNSTREAM_STATUS_SETTLEMENT_LATER_SLICE_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in forbidden_operational_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertNotIn(term, body)

        forbidden_review_fields = [
            "- Status settlement recommendation:",
            "- Status sync:",
            "- Status artifact:",
            "- Status sync blocker:",
        ]
        for skill_name in FORMAL_REVIEW_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in forbidden_review_fields:
                with self.subTest(skill=skill_name, term=term):
                    self.assertNotIn(term, body)

    def test_downstream_status_settlement_validator_enforcement_is_deferred(self) -> None:
        validator_body = (ROOT / "scripts" / "validate-artifact-lifecycle.py").read_text(
            encoding="utf-8"
        )
        deferred_enforcement_terms = [
            "Upstream status settlement",
            "Settlement result",
            "stale upstream artifact status",
        ]
        for term in deferred_enforcement_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, validator_body)

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
            "T4. Inconclusive or ambiguous review never starts final closeout",
            "T5. Milestone state vocabulary is single-field and exact",
            "T6. Implement handoff uses `review-requested` and does not claim final closeout readiness",
            "T7. Handoff summaries and plan update obligations are explicit",
            "T8. Milestones are not postponed to reach final closeout",
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
        """Skills describe milestone-aware state, handoff, and final-closeout readiness boundaries."""

        required_by_skill = {
            "implement": [
                "`planned` to `implementing`",
                "`review-requested`",
                "targeted validation evidence",
                "not set plan readiness to `Ready for final closeout`",
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
                "final-closeout readiness",
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
            "routing a clean review to `verify`",
            "route to `verify`",
            "routes to `verify`",
            "hand off to `verify`",
            "make `verify` available",
            "`verify` may proceed",
            "ready for `verify`",
            "whole plan ready for `verify`",
        ]
        for relative_path in [
            "specs/workflow-stage-autoprogression.md",
            "specs/rigorloop-workflow.md",
            "specs/milestone-aware-review-handoff.md",
            "specs/workflow-stage-autoprogression.test.md",
            "specs/rigorloop-workflow.test.md",
            "specs/milestone-aware-review-handoff.test.md",
        ]:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in stale_terms:
                with self.subTest(path=relative_path, stale=term):
                    self.assertNotIn(term, body)

    def test_single_source_workflow_state_test_spec_maps_static_proof(self) -> None:
        body = SINGLE_SOURCE_WORKFLOW_STATE_TEST_SPEC.read_text(encoding="utf-8")
        required_test_cases = [
            "T1. Active plan exposes one live current handoff owner",
            "T2. Non-owner plan sections do not duplicate live next-stage claims",
            "T3. Change-local evidence surfaces keep scoped ownership",
            "T4. Milestone state vocabulary and transitions are enforced",
            "T5. State-sync checklist updates affected owners",
            "T6. Plan lifecycle closeout and merge boundary remain explicit",
            "T7. Verify, explain-change, and PR claim boundaries stay separated",
            "T8. Milestone review loop blocks premature final closeout",
            "T9. Public skill portability and generated output stay aligned",
            "T10. First implementation slice avoids broad semantic validation",
            "T11. Full milestone and final validation closeout",
        ]
        for term in required_test_cases:
            with self.subTest(term=term):
                self.assertIn(term, body)

        for requirement_number in range(1, 37):
            with self.subTest(requirement=requirement_number):
                assert_requirement_id_covered(self, body, requirement_number)

        for example_number in range(1, 5):
            with self.subTest(example=example_number):
                self.assertIn(f"`E{example_number}`", body)

        for boundary_number in range(1, 8):
            with self.subTest(boundary=boundary_number):
                assert_boundary_id_covered(self, body, boundary_number)

        required_validation_terms = [
            "Active proof surface for M1 implementation. The active plan `Current Handoff Summary` owns the next workflow action.",
            "Do not add broad semantic natural-language scoring for plan state.",
            "python scripts/build-adapters.py --version 0.1.1 --check",
            "python scripts/validate-adapters.py --version 0.1.1",
        ]
        for term in required_validation_terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

    def test_single_source_workflow_state_plan_keeps_m1_scaffolding_reviewable(self) -> None:
        spec = SINGLE_SOURCE_WORKFLOW_STATE_SPEC.read_text(encoding="utf-8")
        plan = SINGLE_SOURCE_WORKFLOW_STATE_PLAN.read_text(encoding="utf-8")

        required_spec_terms = [
            "Write current state once; link to it everywhere else.",
            "the active plan's `Current Handoff Summary` MUST be the authoritative live state block",
            "The active plan `Readiness` section MUST point to `Current Handoff Summary`",
            "A state-sync check MUST update the active plan `Current Handoff Summary`",
            "Published skill wording MUST NOT expose RigorLoop repository-internal source paths",
            "python scripts/build-adapters.py --version 0.1.1 --check",
            "python scripts/validate-adapters.py --version 0.1.1",
        ]
        for term in required_spec_terms:
            with self.subTest(surface="spec", term=term):
                self.assertIn(term, spec)

        required_plan_terms = [
            "M1. Test Spec and Validator Coverage",
            "Keep semantic plan-state validation out of scope",
            "python scripts/test-skill-validator.py",
            "python scripts/test-artifact-lifecycle-validator.py",
            "M1-M4 must each pass their implementation handoff and code-review loop before M5 final lifecycle closeout.",
            "python scripts/build-adapters.py --version 0.1.1 --check",
            "python scripts/validate-adapters.py --version 0.1.1",
        ]
        for term in required_plan_terms:
            with self.subTest(surface="plan", term=term):
                self.assertIn(term, plan)

    def test_single_source_workflow_state_m2_governance_guidance(self) -> None:
        """Contributor-facing guidance names one live state owner and scoped evidence surfaces."""

        workflows = (ROOT / "docs" / "workflows.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        constitution = (ROOT / "CONSTITUTION.md").read_text(encoding="utf-8")
        example_plan = (ROOT / "docs" / "examples" / "plans" / "example-plan.md").read_text(
            encoding="utf-8"
        )

        workflow_terms = [
            "For planned initiatives, the active plan `Current Handoff Summary` is the live state owner.",
            "`Readiness` points to `Current Handoff Summary` for current live state instead of duplicating the current next stage.",
            "State-sync checks update affected state owners before downstream readiness is claimed.",
            "Change metadata, review-resolution, review-log, explain-change, verify output, and PR handoff own scoped evidence; they do not own the active plan's current next stage.",
        ]
        for term in workflow_terms:
            with self.subTest(surface="docs/workflows.md", term=term):
                self.assertIn(term, workflows)

        governance_terms = [
            "Current Handoff Summary",
            "state-sync check",
            "scoped evidence",
            "must not own the active plan's current next stage",
        ]
        for body, surface in ((agents, "AGENTS.md"), (constitution, "CONSTITUTION.md")):
            for term in governance_terms:
                with self.subTest(surface=surface, term=term):
                    self.assertIn(term, body)

        example_terms = [
            "## Current Handoff Summary",
            "- Current milestone:",
            "- Current milestone state:",
            "- Last reviewed milestone:",
            "- Review status:",
            "- Remaining in-scope implementation milestones:",
            "- Next stage:",
            "- Final closeout readiness:",
            "- Reason final closeout is or is not ready:",
            "See `Current Handoff Summary`.",
        ]
        for term in example_terms:
            with self.subTest(surface="example plan", term=term):
                self.assertIn(term, example_plan)

        stale_workflow_terms = [
            "in the active plan or review handoff",
            "If the plan is still active, name the next expected milestone or workflow stage.",
        ]
        for term in stale_workflow_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, workflows)
                self.assertNotIn(term, example_plan)

    def test_single_source_workflow_state_m3_skill_guidance(self) -> None:
        """Canonical skills write live state once and keep final artifacts scoped."""

        skill_bodies = {
            skill_name: (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for skill_name in [
                "workflow",
                "plan",
                "implement",
                "code-review",
                "verify",
                "explain-change",
                "pr",
            ]
        }

        required_by_skill = {
            "workflow": [
                "For planned initiatives, the active plan `Current Handoff Summary` owns live state.",
                "State-sync checks update affected owners before downstream readiness is claimed.",
            ],
            "plan": [
                "The active plan `Readiness` section points to `Current Handoff Summary` for current live state.",
                "Do not duplicate the current next stage outside `Current Handoff Summary` unless the statement is explicitly historical.",
            ],
            "implement": [
                "Perform a state-sync check before claiming readiness for `code-review`.",
                "Update the active plan `Current Handoff Summary` when the milestone moves to `review-requested`.",
            ],
            "code-review": [
                "Update or require update of the active plan `Current Handoff Summary` before downstream handoff.",
                "When findings require review-resolution, update or require update of the reviewed milestone to `resolution-needed`.",
            ],
            "verify": [
                "Final verification is scoped evidence and must not own the active plan's current next stage.",
                "Use the active plan `Current Handoff Summary` to assess current planned-initiative state.",
            ],
            "explain-change": [
                "Explain-change is scoped evidence and must not own the active plan's current next stage.",
                "Use the active plan `Current Handoff Summary` when summarizing current planned-initiative state.",
            ],
            "pr": [
                "PR handoff is scoped evidence and must not own the active plan's current next stage.",
                "Summarize planned-initiative state from the active plan `Current Handoff Summary`.",
            ],
        }
        for skill_name, terms in required_by_skill.items():
            body = skill_bodies[skill_name]
            for term in terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

        for skill_name in ["workflow", "plan", "implement", "code-review"]:
            body = skill_bodies[skill_name]
            with self.subTest(skill=skill_name, stale="in the active plan or review handoff"):
                self.assertNotIn("in the active plan or review handoff", body)

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
            "docs/workflows.md",
            "skills/code-review/SKILL.md",
            "skills/workflow/SKILL.md",
        ]
        for relative_path in paths:
            body = (ROOT / relative_path).read_text(encoding="utf-8")
            for term in stale_terms:
                with self.subTest(path=relative_path, term=term):
                    self.assertNotIn(term, body)

    def test_public_workflow_and_skill_surfaces_block_retired_route_vocabulary(self) -> None:
        """Public workflow and shipped skill surfaces must not restore retired lane wording."""

        for path in iter_public_workflow_and_skill_surfaces():
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in RETIRED_PUBLIC_ROUTE_PATTERNS.items():
                with self.subTest(path=str(relative_path), pattern=label):
                    self.assertIsNone(pattern.search(body))

    def test_workflow_spec_retired_route_terms_are_only_forbidden_context(self) -> None:
        spec = SKILL_CONTRACT_WORKFLOW_SPEC.read_text(encoding="utf-8")
        for line_number, line in enumerate(spec.splitlines(), start=1):
            for label, pattern in RETIRED_PUBLIC_ROUTE_PATTERNS.items():
                if pattern.search(line) and not any(
                    context in line for context in WORKFLOW_SPEC_ALLOWED_RETIRED_ROUTE_CONTEXTS
                ):
                    self.fail(
                        f"retired route term '{label}' appears outside forbidden/static-validation "
                        f"context at {SKILL_CONTRACT_WORKFLOW_SPEC.relative_to(ROOT)}:{line_number}"
                    )

    def test_published_skill_surfaces_block_internal_repository_details(self) -> None:
        """Published skill text must stay portable across projects."""

        for path in iter_published_skill_text_surfaces():
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in PUBLISHED_SKILL_FORBIDDEN_INTERNAL_PATTERNS.items():
                with self.subTest(path=str(relative_path), pattern=label):
                    self.assertIsNone(pattern.search(body))

    def test_code_review_and_verify_public_skills_use_final_closeout_order(self) -> None:
        """Shipped review and verify skills must not restore direct-verify closeout."""

        code_review_paths = iter_published_skill_surfaces_for("code-review")
        self.assertTrue(code_review_paths, "expected published code-review skill surfaces")
        for path in code_review_paths:
            body = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(ROOT)
            for label, pattern in CODE_REVIEW_FORBIDDEN_FINAL_CLOSEOUT_PATTERNS.items():
                with self.subTest(path=str(relative_path), forbidden=label):
                    self.assertIsNone(pattern.search(body))
            for term in ["final closeout", "explain-change", "verify", "pr"]:
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
                "after durable change rationale",
                "after `explain-change`",
                "before PR",
                "validates the final change pack",
                "hands off to `pr`",
            ]:
                with self.subTest(path=str(relative_path), required=term):
                    self.assertIn(term, body)

    def test_skill_contract_test_spec_maps_static_proof(self) -> None:
        body = SKILL_CONTRACT_TEST_SPEC.read_text(encoding="utf-8")
        required_terms = [
            "T1. Normative skill-contract source and workflow-routing split",
            "T2. Required and conditional sections are present without hollow normalization",
            "T3. First-slice and later-phase scope stay exact",
            "T4. Claim boundaries and do-not-overclaim guidance",
            "T5. Result blocks and handoff sections are summary-first and local",
            "T6. Progress, readiness, closeout, and Done stay distinct",
            "T7. Public shared blocks are canonical copied text with drift checks",
            "T8. Evidence-reading and example guidance stay bounded",
            "T9. Generated output is refreshed from concrete canonical changes",
            "T10. Forbidden-overclaim validation is narrow and positive-first",
            "T11. Minimum viable skill rule and guidance placement",
            "T12. Compatibility, security, and non-goal boundaries",
            "T13. Full milestone and final validation closeout",
            "T14. Published skills exclude repository-maintainer details",
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
            "Skills are also a published user-facing interface.",
            "Generated skill mirrors under `.codex/skills/` MUST be treated as derived output.",
            "Adapter output under `dist/adapters/` MUST be treated as derived output.",
            "Contributors MUST NOT hand-edit `.codex/skills/` or `dist/adapters/` to satisfy this spec.",
            "Public shared blocks are copied and checked in v1, not generated into skills.",
            "Published skill text does not expose repository-local source paths, generated mirror paths, adapter package paths, selector path constraints, drift-check mechanics, shared-block implementation details, or RigorLoop-local examples.",
            "The baseline normalization first slice and published-skill design pilot MUST NOT add broad natural-language quality scoring.",
            "The `ci-maintenance` skill is the entrypoint for the `ci-maintenance` stage label.",
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

        self.assertIn("The `ci-maintenance` skill MUST be treated as the skill entrypoint", spec)
        self.assertIn("The baseline normalization first slice MUST NOT normalize every skill.", spec)
        self.assertIn("Do not implement Phase 2, Phase 3, or Phase 4 skill normalization", plan)
        self.assertTrue((ROOT / "skills" / "ci-maintenance" / "SKILL.md").exists())

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

    def test_skill_contract_m2_summary_surfaces_keep_source_split(self) -> None:
        workflow_spec = SKILL_CONTRACT_WORKFLOW_SPEC.read_text(encoding="utf-8")
        workflows_doc = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        agents = SKILL_CONTRACT_AGENTS.read_text(encoding="utf-8")

        required_workflow_terms = [
            "`specs/skill-contract.md` owns skill-contract behavior.",
            "standard skill shape, claim boundaries, result output expectations, shared-block rules, generated-output boundaries, evidence-reading guidance, and minimum viable skill rules",
            "`specs/rigorloop-workflow.md` continues to own stage order, stage obligation, handoff, and downstream-blocking semantics.",
        ]
        for term in required_workflow_terms:
            with self.subTest(surface="workflow_spec", term=term):
                self.assertIn(term, workflow_spec)

        required_workflows_terms = [
            "## Skill Contract",
            "The normative skill-contract source is `specs/skill-contract.md`.",
            "The workflow-routing source is `specs/rigorloop-workflow.md`.",
            "Skills are operational guides, not substitute specs.",
            "Shipped skill text is the user-facing interface.",
            "Shared skill policy blocks live under `templates/shared/<block-name>.md`.",
            "Public shared blocks are copied into consuming skills and checked for drift; maintainer-only blocks such as generated-output handling are not copied into published skills.",
            "Add a skill only when it owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.",
            "Edit canonical skill source under `skills/<skill>/SKILL.md`; for public adapter installation, use `dist/adapters/README.md`. For `v0.1.3` and later, generated public adapter skill bodies are release archives, not tracked source under `dist/adapters/`.",
        ]
        for term in required_workflows_terms:
            with self.subTest(surface="workflows_doc", term=term):
                self.assertIn(term, workflows_doc)

        required_agents_terms = [
            "Follow `specs/skill-contract.md` for normalized skill structure and claim boundaries.",
            "Treat shipped skill text as user-facing.",
            "Do not create a new skill for one-off behavior; update an existing skill unless the new skill owns a distinct artifact, gate, review responsibility, recurring action, or approved operational process.",
        ]
        for term in required_agents_terms:
            with self.subTest(surface="agents", term=term):
                self.assertIn(term, agents)

        self.assertNotIn("## Required core sections", agents)
        self.assertNotIn("## Shared-block source of truth", agents)

    def test_single_authored_first_slice_docs_and_ignore_policy(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        workflows_doc = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        agents = SKILL_CONTRACT_AGENTS.read_text(encoding="utf-8")
        constitution = (ROOT / "CONSTITUTION.md").read_text(encoding="utf-8")
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

        shared_terms = [
            "`skills/` is the only authored skill source.",
            "dist/adapters/README.md",
            "generated public adapter skill bodies are release archives",
            ".codex/skills/",
            "Historical note: `v0.1.2` kept repository-tree adapter packages during the compatibility window",
        ]
        for term in shared_terms:
            for surface_name, surface in {
                "README": readme,
                "workflows": workflows_doc,
                "AGENTS": agents,
                "CONSTITUTION": constitution,
            }.items():
                with self.subTest(surface=surface_name, term=term):
                    self.assertIn(term, surface)

        self.assertIn(".codex/skills/", gitignore)
        self.assertNotIn("commit `.codex/skills/`", readme)
        self.assertNotIn("tracked `.codex/skills/`", workflows_doc)
        for surface_name, surface in {
            "README": readme,
            "workflows": workflows_doc,
            "AGENTS": agents,
            "CONSTITUTION": constitution,
        }.items():
            with self.subTest(surface=surface_name, stale_term="Regenerate build-skills"):
                self.assertNotIn("Regenerate it with `python scripts/build-skills.py`", surface)
            with self.subTest(surface=surface_name, stale_term="generated local Codex runtime"):
                self.assertNotIn("`.codex/skills/` is generated local Codex runtime output", surface)

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

    def test_skill_contract_token_cost_amendment_is_defined(self) -> None:
        spec = SKILL_CONTRACT_SPEC.read_text(encoding="utf-8")
        test_spec = SKILL_CONTRACT_TEST_SPEC.read_text(encoding="utf-8")

        required_spec_terms = [
            "Token-cost discipline is part of normalized skill behavior.",
            "Token-cost discipline MUST NOT reduce required validation coverage, review obligations, artifact obligations, or workflow stage gates.",
            "Normalized skills that collect evidence from high-volume surfaces MUST prefer bounded evidence before broad reads.",
            "Output caps MUST be treated as safety rails, not evidence-selection strategy.",
            "Summary-first and failure-focused output MUST preserve validation semantics.",
            "Static validation for token-cost discipline MUST be narrow and reviewable.",
            "Reviewers MAY report broad, noisy evidence collection as a process defect",
            "Do not add a standalone `token-budget` skill.",
        ]
        for term in required_spec_terms:
            with self.subTest(file="spec", term=term):
                self.assertIn(term, spec)

        required_test_terms = [
            "T15. Token-cost amendment and static proof stay narrow",
            "bounded evidence before broad reads",
            "output caps are safety rails, not evidence-selection strategy",
            "no `skills/token-budget/SKILL.md` path exists",
        ]
        for term in required_test_terms:
            with self.subTest(file="test_spec", term=term):
                self.assertIn(term, test_spec)

        self.assertFalse((ROOT / "skills" / "token-budget" / "SKILL.md").exists())

    def test_token_cost_selected_skills_copy_tightened_evidence_block(self) -> None:
        evidence = extract_markdown_block(
            SKILL_CONTRACT_EVIDENCE_BLOCK.read_text(encoding="utf-8"),
            "Evidence collection efficiency",
        )
        for skill_name in TOKEN_COST_SELECTED_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name, block="evidence"):
                self.assertEqual(extract_markdown_block(body, "Evidence collection efficiency"), evidence)

            with self.subTest(skill=skill_name, term="output_caps"):
                self.assertIn("Output caps are safety rails, not evidence-selection strategy.", body)

            with self.subTest(skill=skill_name, term="validation_semantics"):
                self.assertIn("Validation summaries must not change selected check coverage", body)

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

        late_guide = "# Skill\n\n" + ("padding " * 900) + "\n" + valid_skill
        with self.assertRaises(AssertionError):
            assert_progressive_loading_quick_guide_contract(self, late_guide)

        overlong_guide = valid_skill.replace(
            "Use this skill to: route work from the shortest safe operating path.",
            "Use this skill to: " + ("preserve safety " * 260),
        )
        with self.assertRaises(AssertionError):
            assert_progressive_loading_quick_guide_contract(self, overlong_guide)

    def test_progressive_loading_implement_handoff_contract_helper_detects_bounded_state_inspection(self) -> None:
        valid_skill = """# Implement

## Handoff inspection budget

Start with the active plan's Current Handoff Summary.
Then read the current milestone section and validation notes.
For milestone readiness, do not run broad repository searches to infer milestone state.
If the active plan does not identify the current milestone or next stage, stop and report the missing state.
"""
        assert_progressive_loading_implement_handoff_contract(self, valid_skill)

        missing_summary = valid_skill.replace("Current Handoff Summary", "handoff notes")
        with self.assertRaises(AssertionError):
            assert_progressive_loading_implement_handoff_contract(self, missing_summary)

        broad_first_step = valid_skill + "\nAgents may start by searching all docs for milestones.\n"
        with self.assertRaises(AssertionError):
            assert_progressive_loading_implement_handoff_contract(self, broad_first_step)

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

    def test_progressive_loading_test_spec_maps_static_proof_surfaces(self) -> None:
        test_spec = (
            ROOT / "specs" / "progressive-loading-high-cost-public-skills.test.md"
        ).read_text(encoding="utf-8")
        plan = (
            ROOT
            / "docs"
            / "plans"
            / "2026-05-11-progressive-loading-high-cost-public-skills.md"
        ).read_text(encoding="utf-8")

        required_test_terms = [
            "T2. Optimized skills contain valid quick operating guides",
            "T3. `implement` starts handoff-state inspection from active plan state",
            "T4. Workflow detail migration has owner-surface accounting",
            "T5. `code-review` preserves protected review contracts",
            "T6. Section-first reading guidance preserves escape conditions",
            "scripts/test-skill-validator.py",
        ]
        for term in required_test_terms:
            with self.subTest(file="test_spec", term=term):
                self.assertIn(term, test_spec)

        plan_terms = [
            "Quick guide heading, required labels, and top-of-skill placement checks",
            "Static checks that `implement` names `Current Handoff Summary`",
            "Static or manual-check scaffolding for protected `code-review` contracts",
            "Static or report-check scaffolding for workflow migration accounting",
        ]
        for term in plan_terms:
            with self.subTest(file="plan", term=term):
                self.assertIn(term, plan)

    def test_progressive_loading_canonical_skills_satisfy_quick_guide_contract(self) -> None:
        for skill_name in PROGRESSIVE_LOADING_OPTIMIZED_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                assert_progressive_loading_quick_guide_contract(self, body)

    def test_progressive_loading_canonical_implement_handoff_contract(self) -> None:
        body = (ROOT / "skills" / "implement" / "SKILL.md").read_text(encoding="utf-8")
        assert_progressive_loading_implement_handoff_contract(self, body)

    def test_progressive_loading_canonical_code_review_preserves_protected_contracts(self) -> None:
        body = (ROOT / "skills" / "code-review" / "SKILL.md").read_text(encoding="utf-8")
        assert_progressive_loading_code_review_protected_contracts(self, body)

    def test_progressive_loading_workflow_migration_and_report_surfaces_exist(self) -> None:
        workflows = (ROOT / "docs" / "workflows.md").read_text(encoding="utf-8")
        report = (
            ROOT
            / "docs"
            / "reports"
            / "token-cost"
            / "optimizations"
            / "2026-05-11-progressive-loading-high-cost-skills.md"
        ).read_text(encoding="utf-8")

        for term in [
            "## Workflow Detail Ownership",
            "review-resolution detail",
            "lifecycle-managed artifact tables",
            "validation-layering detail",
            "default artifact path lists",
        ]:
            with self.subTest(file="workflows", term=term):
                self.assertIn(term, workflows)

        report_terms = [
            "## Workflow Detail Migration Table",
            "| Removed or summarized topic | New owner surface | Rationale |",
            "Review-resolution details",
            "Lifecycle-managed artifact table",
            "Detailed validation layering",
            "## Static Skill Size",
        ]
        for term in report_terms:
            with self.subTest(file="optimization_report", term=term):
                self.assertIn(term, report)

    def test_proposal_scope_preservation_guidance_is_static_validated(self) -> None:
        proposal = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal_review = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
        ).read_text(encoding="utf-8")

        proposal_terms = [
            "## Scope preservation",
            "Before drafting or materially revising a proposal, extract the user's initial goals, concerns, constraints, and requested outcomes.",
            "Every initial user goal must be visible in the proposal as one `initial goal treatment` enum value.",
            "Closed enum: initial goal treatment",
            "## Initial intent preservation",
            "| Initial user goal | Proposal treatment | Where recorded |",
            "Do not silently drop a user goal when narrowing a proposal.",
            "If a proposal intentionally narrows the user's request, record the narrowing",
        ]
        for term in proposal_terms:
            with self.subTest(skill="proposal", term=term):
                self.assertIn(term, proposal)

        proposal_review_terms = [
            "## Scope preservation review",
            "Compare the user's initial request with the proposal.",
            "Every initial goal must be visibly classified with one `initial goal treatment` enum value.",
            "Return `changes-requested` if any initial user goal disappears.",
            "Return `changes-requested` if a deferred goal has no follow-up.",
            "Return `changes-requested` if a rejected goal has no rationale.",
            "Return `changes-requested` if the proposal narrows scope but does not say why.",
            "Scope-preservation failures must return `changes-requested`.",
            "review status: `approved`, `changes-requested`, `blocked`, or `inconclusive`",
            "scope-preservation result",
            "Do not rewrite the proposal as part of proposal-review unless the user explicitly asks.",
        ]
        for term in proposal_review_terms:
            with self.subTest(skill="proposal-review", term=term):
                self.assertIn(term, proposal_review)

    def test_cost_bounded_rigor_m1_proposal_scope_budget_guidance(self) -> None:
        proposal = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")

        required_terms = [
            "## Scope budget for broad proposals",
            "Scope-budget applicability is proposal/proposal-review judgment in this first slice, not mechanical validator inference.",
            "the user request contains two or more independent work items",
            "the change touches more than one lifecycle family",
            "the change could reasonably require more than one spec or implementation plan",
            "release policy, workflow policy, generated output, public skill behavior, or validation policy",
            "`proposal-review` identifies silent narrowing, hidden follow-up risk, or multi-workstream scope",
            "Small single-decision proposals may omit the scope budget.",
            "| Work item | Treatment | Reason |",
            "Closed enum: scope budget treatment",
            "Use the `scope budget treatment` enum above for allowed treatment values.",
            "Route deferred work through the follow-up ownership model rather than chat-only notes or `project-map` ownership.",
            "workflow routes, `project-map` orients when present, action-owning artifacts track current work, and unowned cross-change follow-ups use the follow-up ownership surface.",
            "Do not search generated adapter output for authored skill truth.",
            "Do not add generated public adapter skill bodies back to tracked source.",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, proposal)

    def test_cost_bounded_rigor_m1_proposal_review_scope_budget_guidance(self) -> None:
        proposal_review = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
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

    def test_cost_bounded_rigor_m1_workflows_bounded_evidence_guidance(self) -> None:
        workflows = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        evidence = extract_markdown_block(workflows, "Efficient Evidence Collection")

        required_terms = [
            "Do not broad-search authoritative documents solely for path or state discovery when narrower evidence is available.",
            "Default evidence sequence for path or state discovery:",
            "exact user-provided path or change ID",
            "current handoff summary or active plan state",
            "`change.yaml`, review log, review resolution, or release metadata",
            "`docs/workflows.md` artifact-location map",
            "targeted headings, stable IDs, line ranges, counts, or diffs",
            "full-file read only when the whole file is the target or bounded evidence is insufficient",
            "Use bounded evidence before broad reads, but do not under-read.",
            "Expand to a broader section or full file when bounded evidence is incomplete, contradictory, or insufficient to support the claim being made.",
            "A full-file read is required when the file itself is the review target",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, evidence)

        proposal = (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8")
        proposal_review = (
            ROOT / "skills" / "proposal-review" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for body, skill_name in ((proposal, "proposal"), (proposal_review, "proposal-review")):
            with self.subTest(skill=skill_name, forbidden="full workflow sequence"):
                self.assertNotIn("Default evidence sequence for path or state discovery:", body)

    def test_stage_evidence_access_contract_guidance(self) -> None:
        workflows = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        evidence = extract_markdown_block(workflows, "Stage Evidence Access")

        required_terms = [
            "Default evidence",
            "Conditional evidence",
            "Expansion evidence",
            "bounded discovery",
            "path inventory, heading scan, line-number search, count query, targeted diff summary, and metadata lookup",
            "substantive content outside its default evidence and triggered conditional evidence",
            "Only include `Evidence expansion` when expansion occurred.",
            "Do not broad-search authoritative documents solely for path or state discovery",
            "A stage must expand when bounded evidence is missing, stale, contradictory, or insufficient",
            "Full-file reads remain allowed",
            "M1 validation covers `docs/workflows.md`, `skills/proposal/SKILL.md`, and `skills/proposal-review/SKILL.md`",
            "include `skills/spec/SKILL.md` only when M1 updates `spec`",
            "M2 validation separately covers `skills/implement/SKILL.md` and `skills/code-review/SKILL.md` when M2 runs",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, evidence)

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
                "`docs/workflows.md` when artifact placement or workflow routing matters",
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
                "`docs/workflows.md` when workflow behavior or artifact placement is proposed",
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

    def test_stage_evidence_access_m2_execution_review_skills(self) -> None:
        skill_terms = {
            "implement": [
                "## Evidence access",
                "Default evidence:",
                "active plan `Current Handoff Summary`",
                "current milestone section",
                "approved spec",
                "test spec",
                "code and tests named by the milestone",
                "validation commands for the milestone",
                "Conditional evidence:",
                "architecture or ADR when the milestone touches architecture boundaries",
                "review-resolution when implementing accepted review findings",
                "`docs/workflows.md` when stage routing or artifact placement is ambiguous",
                "`CONSTITUTION.md` when governance, source-of-truth, or safety constraints matter",
                "neighboring files when needed to follow existing patterns",
                "Record a compact reason only when reading substantive evidence outside the default and triggered conditional set.",
            ],
            "code-review": [
                "## Evidence access",
                "Default evidence:",
                "actual diff or changed files",
                "approved spec",
                "test spec",
                "current plan milestone",
                "validation evidence",
                "relevant tests",
                "Conditional evidence:",
                "architecture or ADR when architecture is touched",
                "review-resolution when reviewing fixes for findings",
                "change metadata when lifecycle state or review closeout matters",
                "`CONSTITUTION.md` when source-of-truth, governance, or safety boundaries matter",
                "related code paths when the diff depends on them",
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

    def test_cost_bounded_rigor_m2_selected_skill_reminders(self) -> None:
        selected_skills = {
            "proposal": (ROOT / "skills" / "proposal" / "SKILL.md").read_text(encoding="utf-8"),
            "proposal-review": (
                ROOT / "skills" / "proposal-review" / "SKILL.md"
            ).read_text(encoding="utf-8"),
            "workflow": (ROOT / "skills" / "workflow" / "SKILL.md").read_text(encoding="utf-8"),
        }

        common_terms = [
            "Use bounded evidence before broad reads",
            "Read exact ranges",
            "narrower evidence",
            "insufficient",
            "## When full-file read is required",
            "bounded searches disagree",
        ]
        for skill_name, body in selected_skills.items():
            for term in common_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)
            with self.subTest(skill=skill_name, forbidden="full workflow sequence"):
                self.assertNotIn("Default evidence sequence for path or state discovery:", body)

        for skill_name in ["proposal", "proposal-review"]:
            body = selected_skills[skill_name]
            for term in [
                "Do not broad-search authoritative documents just to find paths.",
                "Use `docs/workflows.md` as the path index",
                "active plan, change metadata, reviewed artifact path, or current artifact metadata",
            ]:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)

        workflow = selected_skills["workflow"]
        for term in [
            "path or state lookup",
            "active plan",
            "current artifact metadata",
            "`docs/workflows.md`",
            "targeted headings",
            "broader searches",
            "incomplete, contradictory, or insufficient",
        ]:
            with self.subTest(skill="workflow", term=term):
                self.assertIn(term, workflow)

    def test_skill_contract_m3_first_slice_core_sections_and_result_blocks(self) -> None:
        for skill_name in SKILL_CONTRACT_FIRST_SLICE_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name, surface="core_sections"):
                for section in SKILL_CONTRACT_REQUIRED_CORE_SECTIONS:
                    self.assertIn(f"## {section}", body)

            expected_output_start = body.find("## Expected output")
            self.assertNotEqual(
                expected_output_start,
                -1,
                msg=f"{skill_name} must preserve the validator-required Expected output section",
            )
            expected_output = body[expected_output_start:]
            with self.subTest(skill=skill_name, surface="result_block"):
                self.assertIn("## Result", expected_output)
                for field in SKILL_CONTRACT_RESULT_FIELDS:
                    self.assertIn(f"- {field}:", expected_output)

            handoff = extract_markdown_block(body, "Handoff")
            with self.subTest(skill=skill_name, surface="handoff"):
                self.assertIn("workflow", handoff)
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

    def test_project_artifact_location_m1_workflows_doc_contains_artifact_map(self) -> None:
        workflows = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        artifact_locations = extract_markdown_block(workflows, "Artifact locations")

        required_terms = [
            "The table defines default locations and owning skills.",
            "It does not define full artifact schemas",
            "For exact shapes, use the governing spec, schema, or reference",
            "Project vision",
            "Workflow guide",
            "Examples",
            "Proposals",
            "Specs",
            "Test specs",
            "Architecture",
            "ADRs",
            "Plans",
            "Plan index",
            "Change root",
            "Change metadata",
            "Formal review records",
            "Review log",
            "Review resolution",
            "Explain change",
            "Verify report",
            "Reports",
            "default location only",
            "formal review recording",
            "when findings or blocking outcomes require disposition",
            "when required",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, artifact_locations)

    def test_workflow_map_m1_workflows_doc_contains_canonical_artifact_registry(self) -> None:
        workflows = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        registry = extract_markdown_block(workflows, "Artifact registry")

        required_terms = [
            "canonical fenced YAML artifact registry",
            "```yaml",
            "artifact_locations:",
            "proposal:",
            "path: docs/proposals/YYYY-MM-DD-slug.md",
            "spec:",
            "path: specs/slug.md",
            "test_spec:",
            "path: specs/slug.test.md",
            "plan_index:",
            "path: docs/plan.md",
            "change_plan:",
            "path: docs/plans/YYYY-MM-DD-slug.md",
            "change_metadata:",
            "path: docs/changes/<change-id>/change.yaml",
            "formal_review_record:",
            "path: docs/changes/<change-id>/reviews/<stage>-r<n>.md",
            "review_log:",
            "path: docs/changes/<change-id>/review-log.md",
            "review_resolution:",
            "path: docs/changes/<change-id>/review-resolution.md",
            "explain_change:",
            "path: docs/changes/<change-id>/explain-change.md",
            "verify_report:",
            "path: docs/changes/<change-id>/verify-report.md",
            "pr_handoff:",
            "external_surface: pull_request_body",
            "learn_session:",
            "path: docs/learn/sessions/YYYY-MM-DD-slug.md",
            "required_when:",
            "owner:",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, registry)

        self.assertNotIn(
            "docs/changes/<change-id>/plan.md",
            registry,
            "workflow registry must not make change-pack plan.md a canonical plan-body path",
        )

    def test_workflow_map_m1_workflow_skill_default_paths_match_change_pack_contract(
        self,
    ) -> None:
        workflow = (ROOT / "skills" / "workflow" / "SKILL.md").read_text(encoding="utf-8")
        defaults = extract_markdown_block(workflow, "Default artifact paths")

        required_terms = [
            "docs/workflows.md",
            "docs/plan.md",
            "docs/proposals/YYYY-MM-DD-slug.md",
            "specs/slug.md",
            "specs/slug.test.md",
            "docs/plans/YYYY-MM-DD-slug.md",
            "docs/changes/<change-id>/change.yaml",
            "docs/changes/<change-id>/reviews/<stage>-r<n>.md",
            "docs/changes/<change-id>/review-log.md",
            "docs/changes/<change-id>/review-resolution.md",
            "docs/changes/<change-id>/explain-change.md",
            "docs/changes/<change-id>/verify-report.md",
            "docs/learn/sessions/YYYY-MM-DD-slug.md",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, defaults)

        forbidden_terms = [
            "docs/changes/<change-id>/plan.md",
            "docs/explain/YYYY-MM-DD-slug.md",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, defaults)

    def test_workflow_map_m2_validator_accepts_current_registry_and_tables(self) -> None:
        workflows = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        workflow_skill = (ROOT / "skills" / "workflow" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        stage_skills = {
            name: (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            for name in ("plan", "proposal-review", "spec-review")
        }

        errors = skill_validation.validate_workflow_artifact_map_contract(
            SKILL_CONTRACT_WORKFLOWS_DOC,
            workflows,
            workflow_skill_text=workflow_skill,
            stage_skill_texts=stage_skills,
        )

        self.assertEqual(errors, [])

    def test_workflow_map_m2_validator_requires_architecture_registry_entries(
        self,
    ) -> None:
        workflows = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        without_architecture_record = workflows.replace(
            "  architecture_record:\n"
            "    owner: architecture\n"
            "    path: docs/architecture/YYYY-MM-DD-slug.md\n"
            "    required_when: architecture stage is triggered\n",
            "",
        )
        without_adr = workflows.replace(
            "  adr:\n"
            "    owner: architecture\n"
            "    path: docs/adr/ADR-YYYYMMDD-slug.md\n"
            "    required_when: durable architecture decision is recorded\n",
            "",
        )

        architecture_record_errors = (
            skill_validation.validate_workflow_artifact_map_contract(
                SKILL_CONTRACT_WORKFLOWS_DOC,
                without_architecture_record,
            )
        )
        adr_errors = skill_validation.validate_workflow_artifact_map_contract(
            SKILL_CONTRACT_WORKFLOWS_DOC,
            without_adr,
        )

        self.assertTrue(
            any(
                error.endswith(
                    ": artifact registry missing required entry architecture_record"
                )
                for error in architecture_record_errors
            ),
            architecture_record_errors,
        )
        self.assertTrue(
            any(
                error.endswith(": artifact registry missing required entry adr")
                for error in adr_errors
            ),
            adr_errors,
        )

    def test_workflow_map_m2_validator_rejects_registry_shape_errors(self) -> None:
        workflows = """
        # Workflows

        ## Artifact registry

        ```yaml
        artifact_locations:
          proposal:
            path: docs/proposals/YYYY-MM-DD-slug.md
            required_when: proposal stage
          change_plan:
            owner: plan
            path: docs/plans/YYYY-MM-DD-slug.md
        ```

        ## Artifact locations

        | Artifact type | Default location | Owning skill | Required when |
        | --- | --- | --- | --- |
        | Proposals | `docs/proposals/YYYY-MM-DD-slug.md` | `proposal` | Proposal stage. |
        | Plans | `docs/plans/YYYY-MM-DD-slug.md` | `plan` | Planned initiative. |
        """

        errors = skill_validation.validate_workflow_artifact_map_contract(
            Path("docs/workflows.md"),
            textwrap.dedent(workflows),
        )

        self.assertIn(
            "docs/workflows.md: artifact registry entry proposal missing owner",
            errors,
        )
        self.assertIn(
            "docs/workflows.md: artifact registry entry change_plan missing required_when",
            errors,
        )

    def test_workflow_map_m2_validator_rejects_duplicate_registry_keys(self) -> None:
        workflows = """
        # Workflows

        ## Artifact registry

        ```yaml
        artifact_locations:
          verify_report:
            owner: verify
            path: docs/changes/<change-id>/verify-report.md
            required_when: verify stage
          verify_report:
            owner: verify
            path: docs/changes/<change-id>/verify-report.md
            required_when: duplicate verify stage
          proposal:
            owner: proposal
            path: docs/proposals/YYYY-MM-DD-slug.md
            path: docs/proposals/duplicate.md
            required_when: proposal stage
        ```

        ## Artifact locations

        | Artifact type | Default location | Owning skill | Required when |
        | --- | --- | --- | --- |
        | Verify report | `docs/changes/<change-id>/verify-report.md` | `verify` | Verify stage. |
        | Proposals | `docs/proposals/YYYY-MM-DD-slug.md` | `proposal` | Proposal stage. |
        """

        errors = skill_validation.validate_workflow_artifact_map_contract(
            Path("docs/workflows.md"),
            textwrap.dedent(workflows),
        )

        self.assertIn(
            "docs/workflows.md: artifact registry has duplicate entry verify_report",
            errors,
        )
        self.assertIn(
            "docs/workflows.md: artifact registry entry proposal has duplicate field path",
            errors,
        )

    def test_workflow_map_m2_validator_rejects_ambiguous_placement(self) -> None:
        workflows = """
        # Workflows

        ## Artifact registry

        ```yaml
        artifact_locations:
          proposal:
            owner: proposal
            required_when: proposal stage
          pr_handoff:
            owner: pr
            path: docs/changes/<change-id>/pr.md
            external_surface: pull_request_body
            required_when: pr stage
        ```

        ## Artifact locations

        | Artifact type | Default location | Owning skill | Required when |
        | --- | --- | --- | --- |
        | Proposals | `docs/proposals/YYYY-MM-DD-slug.md` | `proposal` | Proposal stage. |
        | PR handoff | Pull request body | `pr` | PR stage. |
        """

        errors = skill_validation.validate_workflow_artifact_map_contract(
            Path("docs/workflows.md"),
            textwrap.dedent(workflows),
        )

        self.assertIn(
            "docs/workflows.md: repository-local artifact proposal must define exactly one path",
            errors,
        )
        self.assertIn(
            "docs/workflows.md: artifact registry entry pr_handoff must define exactly one placement representation",
            errors,
        )

    def test_workflow_map_m2_validator_rejects_table_and_path_drift(self) -> None:
        workflows = """
        # Workflows

        ## Artifact registry

        ```yaml
        artifact_locations:
          change_plan:
            owner: plan
            path: docs/changes/<change-id>/plan.md
            required_when: planned initiative
          formal_review_record:
            owner: review skills
            path: docs/reviews/<stage>-r<n>.md
            required_when: formal lifecycle review
        ```

        ## Artifact locations

        | Artifact type | Default location | Owning skill | Required when |
        | --- | --- | --- | --- |
        | Plans | `docs/plans/YYYY-MM-DD-slug.md` | `plan` | Planned initiative. |
        | Formal review records | `docs/reviews/<stage>-r<n>.md` | review skills | Formal lifecycle review. |
        """

        errors = skill_validation.validate_workflow_artifact_map_contract(
            Path("docs/workflows.md"),
            textwrap.dedent(workflows),
            workflow_skill_text="docs/plans/YYYY-MM-DD-slug.md",
            stage_skill_texts={
                "plan": "Canonical plan path: docs/changes/<change-id>/plan.md",
                "proposal-review": "Record at docs/reviews/proposal-review-r<n>.md",
            },
        )

        self.assertIn(
            "docs/workflows.md: change_plan must use docs/plans/YYYY-MM-DD-slug.md, not docs/changes/<change-id>/plan.md",
            errors,
        )
        self.assertIn(
            "docs/workflows.md: formal_review_record must route under docs/changes/<change-id>/reviews/",
            errors,
        )
        self.assertIn(
            "docs/workflows.md: artifact table row Plans placement docs/plans/YYYY-MM-DD-slug.md does not match registry entry change_plan placement docs/changes/<change-id>/plan.md",
            errors,
        )
        self.assertIn(
            "skills/plan/SKILL.md: stage skill contradicts plan-body registry with docs/changes/<change-id>/plan.md",
            errors,
        )
        self.assertIn(
            "skills/proposal-review/SKILL.md: stage skill routes formal reviews outside docs/changes/<change-id>/reviews/",
            errors,
        )

    def test_workflow_map_m2_validator_rejects_unknown_artifact_input(self) -> None:
        errors = skill_validation.validate_workflow_artifact_map_lookup(
            {"proposal": {"path": "docs/proposals/YYYY-MM-DD-slug.md"}},
            ["proposal", "release_attestation"],
        )

        self.assertEqual(
            errors,
            [
                "unknown artifact type release_attestation has unresolved placement; request an explicit path or workflow-map update"
            ],
        )

    def test_project_artifact_location_m1_workflows_doc_names_source_rank(self) -> None:
        workflows = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        source_rank = extract_markdown_block(workflows, "Artifact-location source rank")

        required_terms = [
            "source rank is precedence when sources conflict, not mandatory read order",
            "explicit user-provided path or change ID",
            "active artifact metadata, active plan metadata, or active change metadata",
            "approved project specs or schemas",
            "`docs/workflows.md` artifact-location map",
            "portable default path",
            "block on ambiguity",
            "If a conflict is discovered",
            "higher-priority source wins",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, source_rank)

    def test_project_artifact_location_m1_workflow_skill_refreshes_guide_on_defined_triggers(
        self,
    ) -> None:
        workflow = (ROOT / "skills" / "workflow" / "SKILL.md").read_text(encoding="utf-8")

        required_terms = [
            "creates or refreshes the project workflow guide",
            "artifact-location map",
            "RigorLoop is adopted in a project and no workflow guide exists",
            "artifact locations are added, removed, renamed, or customized",
            "review-recording, examples, reports, or change-root placement changes",
            "stage skill guidance starts relying on the artifact-location map",
            "generated-output or adapter source-of-truth guidance changes",
            "existing guide contradicts current repository paths or governing specs",
            "reference the guide rather than rewrite it",
            "must not author proposals, specs, plans, reviews, ADRs, or exact schemas",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, workflow)

    def test_project_artifact_location_m1_retained_fixture_has_durable_rationale(self) -> None:
        rationale = SKILL_VALIDATOR_FIXTURE_README.read_text(encoding="utf-8")

        required_terms = [
            "retained validator fixture",
            "historical proof pack",
            "not an active change root",
            "not the universal template",
            "does not block the v0.1.2 archive-introduction release",
            "M4 retention decision",
            "tests, validators, compatibility references, or historical proof references",
            "docs/examples/changes/skill-validator/",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, rationale)

    def test_project_artifact_location_m2_stage_skills_share_lookup_wording(self) -> None:
        required_terms = [
            "Use the project workflow guide for artifact locations when placement matters.",
            "Lookup order:",
            "explicit user path or change ID",
            "active plan, change metadata, reviewed artifact path, or current artifact metadata",
            "known governing spec or schema constraint when directly relevant",
            "`docs/workflows.md` artifact-location table",
            "this skill's portable default path",
            "block on ambiguity",
            "discovery order is subordinate to the source-rank rule",
            "Do not broad-search authoritative documents just to find paths.",
            "Use `docs/workflows.md` as the path index",
            "consult specs or schemas only when they govern exact shape, placement, or a detected conflict",
        ]

        for skill_name in PROJECT_ARTIFACT_LOOKUP_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=skill_name):
                for term in required_terms:
                    self.assertIn(term, body)

    def test_project_artifact_location_m2_stage_skills_avoid_path_table_duplication(self) -> None:
        forbidden_terms = [
            "| Artifact type | Default location | Owning skill |",
            "docs/changes/0001-skill-validator",
            "docs/examples/formal-review-recording/",
            "docs/examples/plans/example-plan.md",
        ]

        for skill_name in PROJECT_ARTIFACT_LOOKUP_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in forbidden_terms:
                with self.subTest(skill=skill_name, term=term):
                    self.assertNotIn(term, body)

    def test_installed_skill_artifact_placement_contract_helper_accepts_compliant_review_skills(
        self,
    ) -> None:
        def review_skill_placement_fixture(skill_name: str) -> str:
            return textwrap.dedent(
                f"""\
                # {skill_name}

                ## Artifact placement

                Formal {skill_name} records go under:
                `docs/changes/<change-id>/reviews/{skill_name}-r<n>.md`

                Record the review-log entry in:
                `docs/changes/<change-id>/review-log.md`

                Use `docs/changes/<change-id>/review-resolution.md` only when material
                findings, blocking outcomes, or accepted dispositions require it.

                If this is a formal lifecycle review and no change pack exists, create
                or request `docs/changes/<change-id>/` before claiming `Recording status:
                recorded`.

                If the user requested an isolated advisory review and no formal recording
                is required, do not create lifecycle artifacts unless explicitly asked.
                """
            )

        for skill_name in ("proposal-review", "spec-review"):
            with self.subTest(skill=skill_name):
                self.assertEqual(
                    skill_validation.validate_installed_skill_artifact_placement_contract(
                        Path(f"skills/{skill_name}/SKILL.md"),
                        skill_name,
                        review_skill_placement_fixture(skill_name),
                    ),
                    [],
                )

    def test_installed_skill_artifact_placement_contract_helper_rejects_wrong_record_type(
        self,
    ) -> None:
        def review_skill_placement_fixture(
            *,
            skill_name: str,
            record_type_name: str,
        ) -> str:
            return textwrap.dedent(
                f"""\
                # {skill_name}

                ## Artifact placement

                Formal {record_type_name} records go under:
                `docs/changes/<change-id>/reviews/{skill_name}-r<n>.md`

                Record the review-log entry in:
                `docs/changes/<change-id>/review-log.md`

                Use `docs/changes/<change-id>/review-resolution.md` only when material
                findings, blocking outcomes, or accepted dispositions require it.

                If this is a formal lifecycle review and no change pack exists, create
                or request `docs/changes/<change-id>/` before claiming `Recording status:
                recorded`.

                If the user requested an isolated advisory review and no formal recording
                is required, do not create lifecycle artifacts unless explicitly asked.
                """
            )

        cases = (
            (
                "proposal-review",
                "spec-review",
                "skills/proposal-review/SKILL.md: installed-skill placement contract names the wrong stage-owned record type spec-review records",
            ),
            (
                "spec-review",
                "proposal-review",
                "skills/spec-review/SKILL.md: installed-skill placement contract names the wrong stage-owned record type proposal-review records",
            ),
        )

        for skill_name, record_type_name, expected_error in cases:
            with self.subTest(skill=skill_name):
                errors = skill_validation.validate_installed_skill_artifact_placement_contract(
                    Path(f"skills/{skill_name}/SKILL.md"),
                    skill_name,
                    review_skill_placement_fixture(
                        skill_name=skill_name,
                        record_type_name=record_type_name,
                    ),
                )

                self.assertIn(expected_error, errors)

    def test_installed_skill_artifact_placement_contract_helper_rejects_missing_record_type(
        self,
    ) -> None:
        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/spec-review/SKILL.md"),
            "spec-review",
            textwrap.dedent(
                """\
                # Spec review

                ## Artifact placement

                Formal review records go under:
                `docs/changes/<change-id>/reviews/spec-review-r<n>.md`

                Record the review-log entry in:
                `docs/changes/<change-id>/review-log.md`

                Use `docs/changes/<change-id>/review-resolution.md` only when material
                findings, blocking outcomes, or accepted dispositions require it.

                If this is a formal lifecycle review and no change pack exists, create
                or request `docs/changes/<change-id>/` before claiming `Recording status:
                recorded`.

                If the user requested an isolated advisory review and no formal recording
                is required, do not create lifecycle artifacts unless explicitly asked.
                """
            ),
        )

        self.assertIn(
            "skills/spec-review/SKILL.md: installed-skill placement contract must state the stage-owned record type spec-review record(s)",
            errors,
        )

    def test_installed_skill_artifact_placement_contract_helper_rejects_wrong_record_type_in_artifact_placement_only(
        self,
    ) -> None:
        body = textwrap.dedent(
            """\
            # Spec review

            Mentioning spec-review records outside the placement block does not
            satisfy the placement contract.

            ## Artifact placement

            Formal proposal-review records go under:
            `docs/changes/<change-id>/reviews/spec-review-r<n>.md`

            Record the review-log entry in:
            `docs/changes/<change-id>/review-log.md`

            Use `docs/changes/<change-id>/review-resolution.md` only when material
            findings, blocking outcomes, or accepted dispositions require it.

            If this is a formal lifecycle review and no change pack exists, create
            or request `docs/changes/<change-id>/` before claiming `Recording status:
            recorded`.

            If the user requested an isolated advisory review and no formal recording
            is required, do not create lifecycle artifacts unless explicitly asked.
            """
        )

        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/spec-review/SKILL.md"),
            "spec-review",
            body,
        )

        self.assertIn(
            "skills/spec-review/SKILL.md: installed-skill placement contract names the wrong stage-owned record type proposal-review records",
            errors,
        )

    def test_installed_skill_artifact_placement_contract_helper_rejects_missing_review_path(
        self,
    ) -> None:
        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/proposal-review/SKILL.md"),
            "proposal-review",
            textwrap.dedent(
                """\
                # Proposal review

                ## Artifact placement

                Formal review records go under `docs/changes/<change-id>/reviews/<stage>-r<n>.md`.
                Record the review-log entry in `docs/changes/<change-id>/review-log.md`.
                Use `docs/changes/<change-id>/review-resolution.md` only when material findings require it.
                If no change pack exists, create or request `docs/changes/<change-id>/` before claiming `Recording status: recorded`.
                If this is an isolated advisory review, do not create lifecycle artifacts unless explicitly asked.
                """
            ),
        )

        self.assertIn(
            "skills/proposal-review/SKILL.md: installed-skill placement contract missing default formal review record path docs/changes/<change-id>/reviews/proposal-review-r<n>.md",
            errors,
        )

    def test_installed_skill_artifact_placement_contract_helper_rejects_missing_change_pack_behavior(
        self,
    ) -> None:
        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/spec-review/SKILL.md"),
            "spec-review",
            textwrap.dedent(
                """\
                # Spec review

                ## Artifact placement

                Formal spec-review records go under `docs/changes/<change-id>/reviews/spec-review-r<n>.md`.
                Record the review-log entry in `docs/changes/<change-id>/review-log.md`.
                Use `docs/changes/<change-id>/review-resolution.md` only when material findings require it.
                Isolated advisory reviews do not create lifecycle artifacts unless explicitly asked.
                """
            ),
        )

        self.assertIn(
            "skills/spec-review/SKILL.md: installed-skill placement contract must state create-or-request change-pack behavior before claiming Recording status: recorded",
            errors,
        )

    def test_installed_skill_artifact_placement_contract_helper_checks_workflow_map_sync(
        self,
    ) -> None:
        body = textwrap.dedent(
            """\
            # Spec review

            ## Artifact placement

            Formal spec-review records go under:
            `docs/changes/<change-id>/reviews/spec-review-r<n>.md`

            Record the review-log entry in:
            `docs/changes/<change-id>/review-log.md`

            Use `docs/changes/<change-id>/review-resolution.md` only when material
            findings, blocking outcomes, or accepted dispositions require it.

            If this is a formal lifecycle review and no change pack exists, create
            or request `docs/changes/<change-id>/` before claiming `Recording status:
            recorded`.

            If the user requested an isolated advisory review and no formal recording
            is required, do not create lifecycle artifacts unless explicitly asked.
            """
        )
        workflow = "Formal review records | `docs/changes/<change-id>/reviews/<stage>-r<n>.md`"

        errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/spec-review/SKILL.md"),
            "spec-review",
            body,
            workflow_text=workflow,
        )

        self.assertEqual(errors, [])

        stale_workflow = "Formal review records | `docs/reviews/<stage>-r<n>.md`"
        stale_errors = skill_validation.validate_installed_skill_artifact_placement_contract(
            Path("skills/spec-review/SKILL.md"),
            "spec-review",
            body,
            workflow_text=stale_workflow,
        )

        self.assertIn(
            "skills/spec-review/SKILL.md: docs/workflows.md formal review record default does not match docs/changes/<change-id>/reviews/<stage>-r<n>.md",
            stale_errors,
        )

    def test_installed_skill_artifact_placement_contract_canonical_review_skills(
        self,
    ) -> None:
        workflow_text = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")

        for skill_name in ("proposal-review", "spec-review"):
            with self.subTest(skill=skill_name):
                path = ROOT / "skills" / skill_name / "SKILL.md"
                body = path.read_text(encoding="utf-8")

                self.assertEqual(
                    skill_validation.validate_installed_skill_artifact_placement_contract(
                        path.relative_to(ROOT),
                        skill_name,
                        body,
                        workflow_text=workflow_text,
                    ),
                    [],
                )

    def test_installed_skill_plan_surface_contract_helper_rejects_ambiguous_plan_wording(
        self,
    ) -> None:
        errors = skill_validation.validate_installed_skill_plan_surface_contract(
            Path("skills/plan/SKILL.md"),
            "plan",
            textwrap.dedent(
                """\
                # Plan

                Update the plan before continuing.
                """
            ),
        )

        self.assertIn(
            "skills/plan/SKILL.md: installed-skill plan surface contract must distinguish docs/workflows.md, docs/plan.md, docs/plans/YYYY-MM-DD-slug.md, docs/changes/<change-id>/change.yaml, and docs/changes/<change-id>/",
            errors,
        )
        self.assertIn(
            "skills/plan/SKILL.md: installed-skill plan surface contract must tell plan authors to use clickable relative Markdown links like [Title](plans/YYYY-MM-DD-slug.md) in docs/plan.md",
            errors,
        )

    def test_installed_skill_plan_surface_contract_helper_accepts_explicit_surfaces(
        self,
    ) -> None:
        body = textwrap.dedent(
            """\
            # Plan

            Consult the workflow map at `docs/workflows.md`.
            Update the plan index at `docs/plan.md`.
            Update the plan body at `docs/plans/YYYY-MM-DD-slug.md`.
            Use change metadata at `docs/changes/<change-id>/change.yaml`.
            Record review evidence under `docs/changes/<change-id>/`.
            Write index links as `[Title](plans/YYYY-MM-DD-slug.md)`.
            """
        )

        self.assertEqual(
            skill_validation.validate_installed_skill_plan_surface_contract(
                Path("skills/plan/SKILL.md"),
                "plan",
                body,
            ),
            [],
        )

    def test_installed_skill_plan_surface_contract_canonical_plan_skill(self) -> None:
        path = ROOT / "skills" / "plan" / "SKILL.md"
        body = path.read_text(encoding="utf-8")

        self.assertEqual(
            skill_validation.validate_installed_skill_plan_surface_contract(
                path.relative_to(ROOT),
                "plan",
                body,
            ),
            [],
        )

    def test_change_record_catalog_m4_stage_skills_name_bounded_reads(self) -> None:
        required_terms_by_skill = {
            "proposal-review": [
                "## Change-record bounded reads",
                "proposal under review",
                "user intent",
                "`review-log.md`",
                "`review-resolution.md`",
            ],
            "code-review": [
                "## Change-record bounded reads",
                "`scripts/query-change-record.py <change-id> artifacts`",
                "`scripts/query-change-record.py <change-id> validation --stage <stage>`",
                "`review-resolution.md`",
            ],
            "verify": [
                "## Change-record bounded reads",
                "`scripts/query-change-record.py <change-id> summary`",
                "`scripts/query-change-record.py <change-id> artifacts`",
                "`scripts/query-change-record.py <change-id> validation --latest`",
            ],
            "pr": [
                "## Change-record bounded reads",
                "`scripts/query-change-record.py <change-id> summary`",
                "`scripts/query-change-record.py <change-id> artifacts`",
                "`scripts/query-change-record.py <change-id> validation --latest`",
            ],
            "plan": [
                "## Change-record bounded reads",
                "Current Handoff Summary",
                "`scripts/query-change-record.py <change-id> artifacts`",
                "do not replace active plan state",
            ],
        }

        for skill_name in CHANGE_RECORD_BOUNDED_READ_SKILLS:
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            for term in required_terms_by_skill[skill_name]:
                with self.subTest(skill=skill_name, term=term):
                    self.assertIn(term, body)
            for term in CHANGE_RECORD_FULL_READ_ESCALATION_TERMS:
                with self.subTest(skill=skill_name, escalation=term):
                    self.assertIn(term, body)

    def test_change_record_catalog_m4_query_commands_exist(self) -> None:
        helper = (ROOT / "scripts" / "query-change-record.py").read_text(encoding="utf-8")
        for term in ["summary", "artifacts", "validation", "--latest", "--stage"]:
            with self.subTest(term=term):
                self.assertIn(term, helper)

    def test_follow_up_ownership_m1_workflows_doc_contains_policy_table(self) -> None:
        workflows = SKILL_CONTRACT_WORKFLOWS_DOC.read_text(encoding="utf-8")
        follow_up = extract_markdown_block(workflows, "Follow-up ownership")

        required_terms = [
            "Record follow-ups where they can be acted on.",
            "| Follow-up type | Owner |",
            "Active implementation follow-up",
            "active plan",
            "Review finding follow-up",
            "`review-resolution.md`",
            "Change closeout follow-up",
            "`explain-change.md` or `change.yaml`",
            "Release follow-up",
            "release report or release plan",
            "Repeated lesson",
            "`learn`",
            "Architecture risk or open question",
            "`project-map` risk/open-question note",
            "Unowned cross-change future work",
            "`docs/follow-ups.md`, only when needed",
            "New direction or policy change",
            "`proposal`",
            "`project-map` may identify risks and open questions, but it does not own deferred execution.",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, follow_up)

    def test_follow_up_ownership_m1_workflow_skill_routes_concisely(self) -> None:
        workflow = (ROOT / "skills" / "workflow" / "SKILL.md").read_text(encoding="utf-8")

        required_terms = [
            "## Follow-up routing",
            "Route future work to the artifact that can act on it.",
            "according to `docs/workflows.md`",
            "Do not put deferred execution work in `project-map`.",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, workflow)

        forbidden_terms = [
            "| Follow-up type | Owner |",
            "Active implementation follow-up",
            "Architecture risk or open question",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, workflow)

    def test_follow_up_ownership_m1_project_map_skill_boundary(self) -> None:
        project_map = (ROOT / "skills" / "project-map" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        required_terms = [
            "## Follow-up boundary",
            "`project-map` may record risks and open questions for orientation.",
            "It does not own deferred execution or act as a backlog.",
            "route it to `proposal`, `plan`, `learn`, review-resolution, release evidence, or `docs/follow-ups.md` through the workflow guide.",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, project_map)

        forbidden_terms = [
            "| Follow-up type | Owner |",
            "Active implementation follow-up",
            "Review finding follow-up",
        ]
        for term in forbidden_terms:
            with self.subTest(term=term):
                self.assertNotIn(term, project_map)

    def test_follow_up_ownership_register_absent_or_valid_and_no_shared_block(self) -> None:
        follow_up_shared_blocks = [
            path
            for path in (ROOT / "templates" / "shared").glob("*")
            if "follow" in path.name.lower()
        ]
        self.assertEqual([], follow_up_shared_blocks)

        register_path = ROOT / "docs" / "follow-ups.md"
        if not register_path.exists():
            return

        register = register_path.read_text(encoding="utf-8")
        required_terms = [
            "# Follow-ups",
            "This file tracks deferred work that is not owned by an active plan",
            "## Open follow-ups",
            "| ID | Title | Source | Owner stage | Owner surface | Status | Next action |",
            "## Closed follow-ups",
            "| ID | Title | Closed by | Notes |",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, register)

        allowed_statuses = {"open", "planned", "blocked", "done", "superseded", "deferred"}
        open_section = extract_markdown_block(register, "Open follow-ups")
        rows = [
            line
            for line in open_section.splitlines()
            if line.startswith("|")
            and not re.match(r"^\|\s*-+\s*\|", line)
            and "ID | Title | Source" not in line
        ]
        self.assertGreater(len(rows), 0, "docs/follow-ups.md must not be empty")

        for row in rows:
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            self.assertEqual(7, len(cells), row)
            self.assertTrue(all(cells), row)
            self.assertIn(cells[5], allowed_statuses, row)


if __name__ == "__main__":
    unittest.main(verbosity=2)
