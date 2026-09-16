"""Read-only canonical guidance inventories and structural assertions.

These helpers expose required sections and source consistency, not semantic quality."""
from __future__ import annotations

import re
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


DOWNSTREAM_REVIEW_CLOSEOUT_SKILLS = [
    "route",
    "verify",
    "pr",
]

SHARED_REVIEW_BLOCK_PATH = ROOT / "templates" / "shared" / "review-isolation-and-recording.md"

SKILL_CONTRACT_EVIDENCE_BLOCK = ROOT / "templates" / "shared" / "evidence-collection-efficiency.md"

SKILL_CONTRACT_FIRST_SLICE_SKILLS = [
    "route",
    "plan",
    "implement",
    "code-review",
    "verify",
    "pr",
    "learn",
]

PROGRESSIVE_LOADING_OPTIMIZED_SKILLS = [
    "route",
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

CUSTOMER_PORTABLE_M2_SKILLS = [
    "proposal",
    "proposal-review",
    "design",
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
    "route",
    "plan",
    "implement",
    "code-review",
    "verify",
    "pr",
]

PUBLIC_WORKFLOW_AND_SKILL_SURFACES = [
    "README.md",
    "AGENTS.md",
    "CONSTITUTION.md",
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

def assert_progressive_loading_quick_guide_contract(test_case, skill_body):
    quick_guide = extract_markdown_block(skill_body, "Quick operating guide")
    for label in PROGRESSIVE_LOADING_QUICK_GUIDE_LABELS:
        test_case.assertIn(label, quick_guide)
    test_case.assertIn("full-file", skill_body)
    test_case.assertIn("broader-section", skill_body)

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
