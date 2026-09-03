#!/usr/bin/env python3
"""Shared validation helpers for first-release RigorLoop skill checks."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from boundary_first_reference import (
    GOVERNED_SKILLS as BOUNDARY_FIRST_GOVERNED_SKILLS,
)
from boundary_first_reference import (
    ProjectionContractError,
    format_contract_error,
    load_resource_manifest,
)


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILLS_DIR = ROOT / "skills"
GENERATED_SKILLS_DIR = ROOT / ".codex" / "skills"
SKILL_SCHEMA_PATH = ROOT / "schemas" / "skill.schema.json"
REQUIREMENT_DELIVERY_MODEL_SOURCE = ROOT / "templates" / "shared" / "requirement-to-delivery-model.md"
REQUIREMENT_DELIVERY_MODEL_CONSUMERS = frozenset(
    {
        "proposal",
        "proposal-review",
        "architecture",
        "spec",
        "design-review",
        "plan",
        "delivery-review",
        "code-review",
        "verify",
    }
)
REQUIREMENT_DELIVERY_MODEL_TARGET = Path("references/requirement-to-delivery-model.md")
DISCOVERY_SUPPORT_SOURCE = ROOT / "templates" / "shared" / "discovery-support.md"
DISCOVERY_SUPPORT_CONSUMERS = frozenset({"explore", "research"})
DISCOVERY_SUPPORT_TARGET = Path("references/discovery-support.md")


@dataclass(frozen=True)
class SkillLocalResourceReference:
    path: str
    start: int
    end: int
    line_number: int


@dataclass(frozen=True)
class ResourceInstructionSegment:
    text: str
    start_line: int
    end_line: int
    kind: str

    def line_number_for_offset(self, offset: int) -> int:
        return self.start_line + self.text[:offset].count("\n")


@dataclass(frozen=True)
class MappedResourceIdentity:
    skill_name: str
    relative_path: str
    path: Path
    sha256: str


@dataclass(frozen=True)
class BoundaryLoadingMeasurement:
    skill_name: str
    mapped_resource_ids: tuple[str, ...]
    initial_resource_ids: tuple[str, ...]
    permitted_expansion_ids: tuple[str, ...]
    mapped_resource_count: int
    initial_resource_count: int
    expanded_resource_count: int
    mapped_resource_bytes: int
    initial_resource_bytes: int
    expanded_resource_bytes: int


def validate_requirement_delivery_model_copy(
    skill_path: Path,
    skill_name: str | None,
    *,
    canonical_path: Path | None = None,
) -> list[str]:
    """Require every selected canonical consumer to carry the shared bytes."""

    if skill_name not in REQUIREMENT_DELIVERY_MODEL_CONSUMERS:
        return []
    if canonical_path is None:
        canonical_path = REQUIREMENT_DELIVERY_MODEL_SOURCE
    local_path = skill_path.parent / REQUIREMENT_DELIVERY_MODEL_TARGET
    if not canonical_path.is_file():
        return [f"{canonical_path}: requirement-to-delivery canonical reference is missing"]
    if not local_path.is_file():
        return [f"{local_path}: mapped requirement-to-delivery reference is missing"]
    if local_path.read_bytes() != canonical_path.read_bytes():
        return [f"{local_path}: mapped requirement-to-delivery reference differs from canonical source"]
    return []


def validate_discovery_support_copy(
    local_path: Path,
    skill_name: str,
    *,
    canonical_path: Path | None = None,
) -> list[str]:
    """Require each closed discovery consumer to carry the shared bytes."""

    if skill_name not in DISCOVERY_SUPPORT_CONSUMERS:
        allowed = ", ".join(sorted(DISCOVERY_SUPPORT_CONSUMERS))
        return [
            f"{local_path}: unknown discovery support consumer '{skill_name}'; "
            f"expected one of {allowed}"
        ]
    if canonical_path is None:
        canonical_path = DISCOVERY_SUPPORT_SOURCE
    if not canonical_path.is_file():
        return [f"{canonical_path}: discovery-support canonical reference is missing"]
    if not local_path.is_file():
        return [f"{local_path}: mapped discovery-support reference is missing"]
    if local_path.read_bytes() != canonical_path.read_bytes():
        return [f"{local_path}: mapped discovery-support reference differs from canonical source"]
    return []


def measure_boundary_loading_profiles(
    repo_root: Path,
    fixture_path: Path,
) -> dict[str, BoundaryLoadingMeasurement]:
    """Validate and measure the closed representative boundary loading profiles."""

    try:
        document = json.loads(fixture_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("loading profile fixture must be readable JSON-compatible YAML") from error
    if not isinstance(document, dict) or set(document) != {
        "schema_version",
        "profiles",
    }:
        raise ValueError("loading profile fixture must use the closed top-level shape")
    if (
        type(document["schema_version"]) is not int
        or document["schema_version"] != 1
    ):
        raise ValueError("loading profile schema version is not supported")
    if not isinstance(document["profiles"], list):
        raise ValueError("loading profile profiles must be a list")

    try:
        manifest = load_resource_manifest(repo_root)
    except ProjectionContractError as error:
        raise ValueError(f"loading profile resource manifest is invalid: {error.code}") from error
    resources = {resource.resource_id: resource for resource in manifest.resources}
    expected_by_skill = {
        skill_name: tuple(
            resource.resource_id
            for resource in manifest.resources
            if skill_name in resource.consumers
        )
        for skill_name in sorted(BOUNDARY_FIRST_GOVERNED_SKILLS)
    }
    measurements: dict[str, BoundaryLoadingMeasurement] = {}
    profile_fields = {
        "skill",
        "mapped_resource_ids",
        "initial_resource_ids",
        "permitted_expansion_ids",
    }
    for profile in document["profiles"]:
        if not isinstance(profile, dict) or set(profile) != profile_fields:
            raise ValueError("loading profile row must use the closed field set")
        skill_name = profile["skill"]
        if (
            not isinstance(skill_name, str)
            or skill_name not in BOUNDARY_FIRST_GOVERNED_SKILLS
        ):
            raise ValueError("loading profile skill is not in the closed vocabulary")
        if skill_name in measurements:
            raise ValueError("loading profile skill must appear exactly once")

        lists: dict[str, tuple[str, ...]] = {}
        for field in (
            "mapped_resource_ids",
            "initial_resource_ids",
            "permitted_expansion_ids",
        ):
            value = profile[field]
            if (
                not isinstance(value, list)
                or any(not isinstance(item, str) for item in value)
                or len(value) != len(set(value))
            ):
                raise ValueError(f"loading profile {field} must be a unique string list")
            unknown = set(value) - set(resources)
            if unknown:
                raise ValueError(
                    f"loading profile {field} contains an unknown resource"
                )
            lists[field] = tuple(value)

        mapped = lists["mapped_resource_ids"]
        initial = lists["initial_resource_ids"]
        expansion = lists["permitted_expansion_ids"]
        if mapped != expected_by_skill[skill_name]:
            raise ValueError("loading profile mapped resources do not match the manifest")
        if set(initial) & set(expansion) or set(initial) | set(expansion) != set(mapped):
            raise ValueError(
                "loading profile initial and expansion resources must partition mapped resources"
            )

        byte_counts = {
            resource_id: (repo_root / resources[resource_id].source).stat().st_size
            for resource_id in mapped
        }
        expanded = tuple(resource_id for resource_id in mapped)
        measurements[skill_name] = BoundaryLoadingMeasurement(
            skill_name=skill_name,
            mapped_resource_ids=mapped,
            initial_resource_ids=initial,
            permitted_expansion_ids=expansion,
            mapped_resource_count=len(mapped),
            initial_resource_count=len(initial),
            expanded_resource_count=len(expanded),
            mapped_resource_bytes=sum(byte_counts.values()),
            initial_resource_bytes=sum(byte_counts[item] for item in initial),
            expanded_resource_bytes=sum(byte_counts[item] for item in expanded),
        )

    if set(measurements) != set(BOUNDARY_FIRST_GOVERNED_SKILLS):
        raise ValueError("loading profile fixture must cover every governed skill")
    return measurements


PLACEHOLDER_PATTERN = re.compile(r"\b(TODO|TBD)\b")
READABILITY_SCHEMA_VERSION = "skill-readability-v1"
READABILITY_STAGE_VALUES = {
    "authoring",
    "review",
    "execution",
    "verification",
    "handoff",
    "support",
    "periodic",
}
READABILITY_REQUIRED_ROLE_FIELDS = {
    "role_name",
    "stage",
    "upstream",
    "downstream",
    "summary",
}
READABILITY_INTERNAL_PATH_PATTERN = re.compile(
    r"\b(?:specs/|schemas/|docs/workflows\.md|docs/reports/|docs/changes/|CONSTITUTION\.md|AGENTS\.md)\b"
)
READABILITY_REQUIRED_CONTEXT_PATTERN = re.compile(
    r"\b(?:must|must first|required|require|requires|read|open|consult|before proceeding)\b",
    re.IGNORECASE,
)
READABILITY_ALLOWED_PROJECT_LOCAL_TERMS = [
    "project-local",
    "if present",
    "when present",
    "when available",
    "when operating inside the RigorLoop repository",
    "when this file is the review target",
    "when the user provided this path",
    "when governing project docs exist",
    "direct target",
    "maintainer-only",
    "unavailable to adopters",
]
DESCRIPTION_MAX_CHARS = 1024
ROUTING_HINT_PATTERN = re.compile(
    r"\b(use|when|ask|asks|create|write|review|implement|verify|prepare|generate|capture|produce|update|fix|route)\b",
    re.IGNORECASE,
)
PACKAGED_RESOURCE_DIRS = ("references", "scripts", "assets")
RESOURCE_MAP_VERB_CLASSES = {
    "COPY": "assets/",
    "READ": "references/",
    "RUN": "scripts/",
}
RESOURCE_MAP_ENTRY_PATTERN = re.compile(
    r"^\s*-\s*(?P<verb>COPY|READ|RUN)\s+`(?P<path>[^`]+)`",
    re.IGNORECASE,
)
PACKAGED_NON_ASSET_RESOURCE_ALLOWLIST = {
    ("code-review", "references/workflow-managed-automated-review.md"),
    ("code-review", "references/requirement-to-delivery-model.md"),
    ("proposal", "references/governed-proposal-authoring.md"),
    ("proposal", "references/requirement-to-delivery-model.md"),
    ("proposal", "references/strategic-and-scope-gates.md"),
    ("proposal-review", "references/proposal-review-recording-and-settlement.md"),
    ("proposal-review", "references/conditional-proposal-gates.md"),
    ("proposal-review", "references/requirement-to-delivery-model.md"),
    ("spec", "references/governed-spec-authoring.md"),
    ("spec", "references/requirement-to-delivery-model.md"),
    ("spec-review", "references/governed-spec-review-settlement.md"),
    ("test-spec", "references/governed-test-spec-authoring.md"),
    ("test-spec-review", "references/test-spec-review-recording-and-settlement.md"),
}


def _is_approved_packaged_non_asset_resource(
    skill_name: str | None,
    relative_resource: str,
) -> bool:
    if (skill_name, relative_resource) in PACKAGED_NON_ASSET_RESOURCE_ALLOWLIST:
        return True
    if skill_name not in BOUNDARY_FIRST_GOVERNED_SKILLS:
        return False
    manifest = load_resource_manifest(ROOT)
    return any(
        skill_name in resource.consumers
        and relative_resource == resource.target.as_posix()
        for resource in manifest.resources
    )


MARKDOWN_LIST_ITEM_PATTERN = re.compile(
    r"^(?P<indent>[ \t]*)(?P<marker>[-+*]|\d+[.)])(?P<spacing>[ \t]+)(?P<body>.*)$"
)
PUBLISHED_SKILL_LOCAL_RESOURCE_PREFIXES = (
    "assets/",
    "references/",
    "scripts/",
    "templates/",
)
PUBLISHED_RESOURCE_LOADING_VERBS = (
    "copy",
    "read",
    "run",
    "use",
    "load",
    "open",
    "consult",
    "execute",
)
SKILL_LOCAL_RESOURCE_REFERENCE_PATTERN = re.compile(
    r"`?(?P<path>(?<![A-Za-z0-9._/-])(?:"
    + "|".join(re.escape(prefix[:-1]) for prefix in PUBLISHED_SKILL_LOCAL_RESOURCE_PREFIXES)
    + r")/[A-Za-z0-9_/-](?:[A-Za-z0-9._/-]*[A-Za-z0-9_/-])?)`?"
)
LEGACY_RESOURCE_LOADING_CONTEXT_PATTERN = re.compile(
    r"\b(?:"
    + "|".join(re.escape(verb) for verb in PUBLISHED_RESOURCE_LOADING_VERBS)
    + r")\b",
    re.IGNORECASE,
)
PUBLISHED_RESOURCE_EXTERNAL_PREFIX_PATTERN = re.compile(
    r"(?:(?:^|[\s(\[])(?:the\s+)?(?:project|repository|user)[- ]"
    r"(?:provided|supplied|owned)(?:\s+(?:resource|file|path))?"
    r"(?:\s+(?:at|from))?\s*[`'\"]?$|"
    r"(?:^|[\s(\[])(?:the\s+)?repository-root\s*[`'\"]?$|"
    r"\bwhen the project provides\b)",
    re.IGNORECASE,
)
PUBLISHED_RESOURCE_EXTERNAL_SUFFIX_PATTERN = re.compile(
    r"^(?:[`'\"]?\s*(?:provided|supplied|owned)\s+by\s+"
    r"(?:the\s+)?(?:project|repository|user)\b|"
    r"[^.;:]*\bwhen the project provides\b)",
    re.IGNORECASE,
)
PUBLISHED_RESOURCE_ILLUSTRATIVE_PREFIX_PATTERN = re.compile(
    r"(?:^|[\s(\[])(?:example|illustrative)\s+"
    r"(?:resource|file|path)\s*:\s*[`'\"]?$",
    re.IGNORECASE,
)
PUBLISHED_PROJECT_PROVIDED_HELPER_PATHS = {
    "scripts/query-change-record.py",
}
TEMPORARY_RESOURCE_INTEGRITY_EXCEPTIONS: set[tuple[str, str, str]] = set()
RESOURCE_LOAD_CONDITION_PATTERN = re.compile(
    r"\b(when|if|only|use|read|run|load)\b",
    re.IGNORECASE,
)
SCRIPT_INPUT_PATTERN = re.compile(r"\b(input|expects?)\b", re.IGNORECASE)
SCRIPT_OUTPUT_PATTERN = re.compile(r"\b(output|exit code|exit-code|returns?)\b", re.IGNORECASE)
SCRIPT_FAILURE_PATTERN = re.compile(r"\b(fail|failure|nonzero|non-zero|error)\b", re.IGNORECASE)
PUBLISHED_INTERNAL_PATH_PATTERN = re.compile(
    r"`?(?:specs/|schemas/|docs/reports/|docs/changes/|benchmarks/|scripts/|dist/)`?"
)
PUBLISHED_INTERNAL_PATH_REFERENCE_PATTERN = re.compile(
    r"`?(?P<path>(?:specs|schemas|docs/reports|docs/changes|benchmarks|scripts|dist)/[A-Za-z0-9._/-]+)`?"
)
PUBLISHED_REQUIRED_COMMAND_CONTEXT_PATTERN = re.compile(
    r"""
    ^\s*(?:[-*]\s*)?
    (?:
      run
      | execute
      | invoke
      | call
      | launch
      | rerun
      | use
      | validate\s+with
      | generate\s+with
      | check\s+with
    )\b
    """,
    re.IGNORECASE | re.VERBOSE,
)
PUBLISHED_NON_REQUIRED_CONTEXT_PATTERN = re.compile(
    r"""
    \b(
      do\s+not\s+run
      | don't\s+run
      | not\s+required
      | optional
      | example
      | for\s+example
      | if\s+present
      | when\s+packaged
      | skill-local
    )\b
    """,
    re.IGNORECASE | re.VERBOSE,
)
PUBLISHED_ALLOWED_PROJECT_LOCAL_TERMS = [
    "project-local",
    "when present",
    "if present",
    "when available",
    "when relevant",
    "when the project provides",
    "when operating inside the RigorLoop repository",
    "when those paths are the target",
    "when this repository is the target",
    "when supplied by the user",
    "user-provided",
    "direct target",
    "packaged",
]
PLAN_ASSET_PILOT_APPROVED_ASSETS = {
    "assets/plan-skeleton.md",
    "assets/milestone.md",
    "assets/decision-log-row.md",
}
PLAN_ASSET_REQUIRED_METADATA_FIELDS = {
    "Template",
    "Skill",
    "Template status",
    "Structural-fingerprint",
    "Maintained alongside",
}
PLAN_ASSET_TEMPLATE_STATUS_VALUES = {"normative", "optional", "example", "deprecated"}
PLAN_ASSET_PLACEHOLDER_PATTERN = re.compile(r"<[^>\n]+>|\[FILL IN\]")
PLAN_ASSET_FIELDS_TO_FILL_PATTERN = re.compile(r"\b(?:Fill|Fields|Structures):", re.IGNORECASE)
PLAN_ASSET_METADATA_PATTERN = re.compile(r"^<!--\s*(?P<key>[^:]+):\s*(?P<value>.*?)\s*-->$")
PLAN_ASSET_SECTIONS_PATTERN = re.compile(
    r"\bSections:\s*(?P<sections>.*?)(?:\s+Do not emit|\s+Fill:|\s*$)",
    re.IGNORECASE,
)
PROJECT_MAP_SKELETON = "assets/project-map-skeleton.md"
PROJECT_MAP_REQUIRED_OPERATIONS = ("create", "refresh", "audit")
PROJECT_MAP_REQUIRED_METADATA_FIELDS = (
    "Map status",
    "Scope",
    "Baseline",
    "Last reviewed",
    "Coverage",
    "Exclusions",
    "Parent map",
    "Known gaps",
)
PROJECT_MAP_REQUIRED_EVIDENCE_CLASSES = ("observed", "inferred", "unknown")
PROJECT_MAP_REQUIRED_OUTPUT_SECTIONS = (
    "Map metadata",
    "Purpose and scope",
    "System overview",
    "Repository layout",
    "Runtime flow",
    "Data flow",
    "External boundaries",
    "Test map",
    "CI and release map",
    "Architecture rules observed",
    "Risk areas",
    "Open questions",
)
PROJECT_MAP_AREA_REGISTRATION_COLUMNS = (
    "Area",
    "Map",
    "Scope",
    "Baseline",
    "Freshness",
    "Known gaps",
)
PROJECT_MAP_SKELETON_FORBIDDEN_POLICY_PATTERNS = {
    "evidence-ranking or source-rank policy": re.compile(
        r"\b(?:source-rank|source rank|evidence-ranking|evidence ranking)\b",
        re.IGNORECASE,
    ),
    "inference policy": re.compile(r"\binference policy\b", re.IGNORECASE),
    "refresh triggers": re.compile(r"\brefresh triggers?\b", re.IGNORECASE),
    "future-design prohibitions": re.compile(
        r"\bfuture-design prohibitions?\b|\bfuture design prohibitions?\b",
        re.IGNORECASE,
    ),
    "handoff rules": re.compile(r"\bhandoff rules?\b", re.IGNORECASE),
    "claim boundaries": re.compile(r"\bclaim boundaries?\b", re.IGNORECASE),
}
SPEC_FAMILY_ASSET_APPROVED_ASSETS = {
    "spec": {
        "assets/spec-skeleton.md",
    },
    "spec-review": {
        "assets/review-result-skeleton.md",
        "assets/material-finding.md",
    },
    "test-spec": {
        "assets/test-spec-skeleton.md",
        "assets/test-case.md",
        "assets/coverage-map-row.md",
        "assets/validation-command-row.md",
        "assets/milestone-proof-row.md",
    },
}
TEST_SPEC_COMMAND_CLASSIFICATIONS = {
    "existing/configured",
    "planned-for-implementation",
    "release-owned",
    "ci-owned",
    "external-owned",
    "not-applicable",
}
TEST_SPEC_VALIDATION_COMMAND_COLUMNS = (
    "Command ID",
    "Command",
    "Classification",
    "Owner",
    "Owning milestone",
    "First required milestone",
    "Failure behavior",
    "Zero-test behavior",
    "Evidence artifact",
    "Safe mode / side-effect boundary",
)
TEST_SPEC_MILESTONE_PROOF_COLUMNS = (
    "Milestone",
    "Required test IDs",
    "Manual proof IDs",
    "Command IDs",
    "Evidence artifacts",
    "Required before",
    "Notes",
)
TEST_SPEC_COMMAND_PATTERN = re.compile(
    r"`(?P<command>(?:python|pytest|npm|pnpm|yarn|uv|ruff|mypy|make|bash|sh)\s+[^`]+)`"
)
SPEC_FAMILY_ASSET_REQUIRED_METADATA_FIELDS = {
    "Template",
    "Skill",
    "Template status",
    "Maintained alongside",
}
SPEC_FAMILY_ASSET_TEMPLATE_STATUS_VALUES = {"normative", "optional"}
SPEC_FAMILY_ASSET_PLACEHOLDER_PATTERN = re.compile(r"<[^>\n]+>|\[FILL IN\]|TODO:")
SPEC_FAMILY_ASSET_FILLER_PATTERN = re.compile(
    r"\b(?:your text here|lorem ipsum)\b",
    re.IGNORECASE,
)
SPEC_REVIEW_ASSET_FORBIDDEN_POLICY_PATTERN = re.compile(
    r"\b(?:must|should|review[- ]dimension|severity policy|sufficiency|"
    r"safe[- ]resolution decision|recording[- ]status|security|privacy|"
    r"observability|example)\b",
    re.IGNORECASE,
)
SPEC_REVIEW_ASSET_ALLOWED_FIELD_LABEL_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?(?P<label>[A-Za-z][A-Za-z /_-]*):\s*<[^>\n]+>\s*$"
)
SPEC_REVIEW_ASSET_APPROVED_LABELS = {
    "skill",
    "review-status",
    "material-findings",
    "recording-status",
    "recording-blocker",
    "review-record",
    "review-log",
    "review-resolution",
    "open-blockers",
    "immediate-next-stage",
    "eventual-test-spec-readiness",
    "stop-condition",
    "settlement-mode",
    "settlement-status",
    "governed-change-identity",
    "boundary-applicability",
    "boundary-resources",
    "boundary-blocker",
    "automation-mode",
    "automation-evidence",
    "automation-result",
    "finding-id",
    "severity",
    "location",
    "evidence",
    "required-outcome",
    "safe-resolution-path",
    "needs-decision-rationale",
}
SPEC_REVIEW_ASSET_FORBIDDEN_LABEL_PATTERN = re.compile(
    r"\b(?:severity[- ]policy|sufficiency|safe[- ]resolution[- ]decision|"
    r"recording[- ]status[- ]rules?|security|privacy|observability|"
    r"review[- ]dimension)\b",
    re.IGNORECASE,
)
PROPOSAL_FAMILY_ASSET_APPROVED_ASSETS = {
    "proposal": {
        "assets/proposal-skeleton.md",
    },
    "proposal-review": {
        "assets/review-result-skeleton.md",
        "assets/material-finding.md",
    },
}
PROPOSAL_REVIEW_ASSET_ALLOWED_FIELD_LABELS = {
    "skill",
    "review-status",
    "vision-alignment",
    "material-findings",
    "recording-status",
    "recording-blocker",
    "review-record",
    "review-log",
    "review-resolution",
    "open-blockers",
    "immediate-next-stage",
    "proposal-readiness",
    "automatic-downstream-handoff",
    "claim-limitations",
    "review-dimensions",
    "scope-preservation-result",
    "recommended-edits",
    "recommendation",
    "active-gate-predicates",
    "gate-outcomes",
    "trigger-ambiguity",
    "record-path",
    "finding-record-paths",
    "review-id",
    "proposal-settlement",
    "governed-change-identity",
    "formal-next-stage-eligibility",
    "packet-identity",
    "phase-receipt-identity",
    "independence-result",
    "correction-eligibility",
    "correction-cycle-state",
    "promotion-or-pause-result",
    "rereview-requirement",
    "finding-id",
    "severity",
    "location",
    "evidence",
    "required-outcome",
    "safe-resolution-path",
    "needs-decision-rationale",
}
PROPOSAL_REVIEW_ASSET_FORBIDDEN_POLICY_PATTERN = re.compile(
    r"\b(?:must|should|severity[- ]policy|material[- ]finding sufficiency|"
    r"safe[- ]resolution decision rule|recording[- ]status rules?|"
    r"scope[- ]preservation rules?|scope[- ]budget review|vision fit review|"
    r"standing artifact gate review|review dimension guidance|"
    r"review[- ]dimension definitions?|security|privacy|rollout examples?)\b",
    re.IGNORECASE,
)
PROPOSAL_REVIEW_ASSET_FORBIDDEN_LABEL_PATTERN = re.compile(
    r"\b(?:severity[- ]policy|material[- ]finding[- ]sufficiency|"
    r"safe[- ]resolution[- ]decision[- ]rule|recording[- ]status[- ]rules?|"
    r"scope[- ]preservation[- ]rules?|scope[- ]budget[- ]review|"
    r"vision[- ]fit[- ]review|standing[- ]artifact[- ]gate[- ]review|"
    r"review[- ]dimension[- ]guidance)\b",
    re.IGNORECASE,
)
CI_MAINTENANCE_SKILL_NAME = "ci-maintenance"
CI_MAINTENANCE_SKELETON = "assets/github-workflow-skeleton.yml"
CI_MAINTENANCE_RISK_MAP = "references/risk-to-check-map.md"
CI_MAINTENANCE_AUTHORING_REFERENCE = "references/github-workflow-authoring.md"
REVIEW_FAMILY_FIRST_SLICE_SKILLS = {
    "code-review",
    "proposal-review",
    "spec-review",
    "test-spec-review",
}
REVIEW_FAMILY_ASSET_APPROVED_ASSETS = {
    skill_name: {
        "assets/material-finding.md",
        "assets/review-result-skeleton.md",
    }
    for skill_name in REVIEW_FAMILY_FIRST_SLICE_SKILLS
}
REVIEW_FAMILY_PARSER_FIELD_LABELS = (
    "Finding ID",
    "Severity",
    "Location",
    "Evidence",
    "Required outcome",
    "Safe resolution path",
)
REVIEW_FAMILY_MATERIAL_FINDING_ALLOWED_LABELS = {
    *REVIEW_FAMILY_PARSER_FIELD_LABELS,
    "needs-decision rationale",
}
SPEC_REVIEW_RESULT_FIELD_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?(?P<label>[A-Za-z][A-Za-z /_-]*):\s*(?P<value>.*?)\s*$"
)
SPEC_REVIEW_RESULT_ALLOWED_REVIEW_STATUSES = {
    "approved",
    "changes-requested",
    "blocked",
    "inconclusive",
}
SPEC_REVIEW_RESULT_ALLOWED_IMMEDIATE_STAGES = {
    "spec revision",
    "review-resolution",
    "architecture",
    "plan",
    "none",
}
SPEC_REVIEW_RESULT_ALLOWED_READINESS = {
    "ready",
    "conditionally-ready",
    "not-ready",
}
SPEC_REVIEW_RESULT_PSEUDO_ROUTING_VALUES = {
    "blocker handling",
    "missing-context resolution",
    "test-spec",
    "ready for test-spec",
}
REVIEW_FAMILY_ASSET_FORBIDDEN_POLICY_PATTERN = re.compile(
    r"\b(?:must|should|review[- ]dimension definitions?|review[- ]dimension guidance|"
    r"severity[- ]policy|review[- ]status[- ]policy|material[- ]finding[- ]sufficiency|"
    r"safe[- ]resolution[- ]decision(?:[- ]rule)?|recording[- ]status[- ]rules?|"
    r"isolation[- ]rules?|scope[- ]preservation[- ]rules?|vision[- ]fit[- ]review|"
    r"standing[- ]artifact[- ]gate[- ]review|workflow[- ]handoff|"
    r"lifecycle[- ]boundary)\b",
    re.IGNORECASE,
)
ASSET_ROLLOUT_APPROVED_ASSETS = {
    **SPEC_FAMILY_ASSET_APPROVED_ASSETS,
    **PROPOSAL_FAMILY_ASSET_APPROVED_ASSETS,
    **REVIEW_FAMILY_ASSET_APPROVED_ASSETS,
}
INSTALLED_SKILL_PLACEMENT_REVIEW_PATHS = {
    "proposal-review": "docs/changes/<change-id>/reviews/proposal-review-r<n>.md",
    "spec-review": "docs/changes/<change-id>/reviews/spec-review-r<n>.md",
    "test-spec-review": "docs/changes/<change-id>/reviews/test-spec-review-r<n>.md",
}
INSTALLED_SKILL_PLACEMENT_REVIEW_RECORD_TYPES = {
    "proposal-review": {
        "record_type_terms": (
            "proposal-review record",
            "proposal-review records",
        ),
        "forbidden_record_type_terms": (
            "spec-review record",
            "spec-review records",
        ),
    },
    "spec-review": {
        "record_type_terms": (
            "spec-review record",
            "spec-review records",
        ),
        "forbidden_record_type_terms": (
            "proposal-review record",
            "proposal-review records",
        ),
    },
    "test-spec-review": {
        "record_type_terms": (
            "test-spec-review record",
            "test-spec-review records",
        ),
        "forbidden_record_type_terms": (
            "proposal-review record",
            "proposal-review records",
        ),
    },
}
INSTALLED_SKILL_PLACEMENT_REVIEW_LOG_PATH = "docs/changes/<change-id>/review-log.md"
INSTALLED_SKILL_PLACEMENT_REVIEW_RESOLUTION_PATH = (
    "docs/changes/<change-id>/review-resolution.md"
)


def _normalize_result_label(label: str) -> str:
    return re.sub(r"[\s/_]+", "-", label.strip().lower())


def _parse_spec_review_result_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = SPEC_REVIEW_RESULT_FIELD_PATTERN.match(line)
        if not match:
            continue
        label = _normalize_result_label(match.group("label"))
        fields[label] = match.group("value").strip()
    return fields


def validate_spec_review_result_fields(text: str) -> list[str]:
    """Validate structurally inspectable spec-review result fields."""

    fields = _parse_spec_review_result_fields(text)
    errors: list[str] = []

    review_status = fields.get("review-status")
    immediate_stage = fields.get("immediate-next-stage")
    readiness = fields.get("eventual-test-spec-readiness")
    stop_condition = fields.get("stop-condition")
    readiness_condition = (
        fields.get("readiness-condition")
        or fields.get("eventual-test-spec-readiness-condition")
        or fields.get("condition")
    )

    for label, value in (
        ("Review status", review_status),
        ("Immediate next stage", immediate_stage),
        ("Eventual test-spec readiness", readiness),
        ("Stop condition", stop_condition),
    ):
        if value is None:
            errors.append(f"spec-review result missing required field: {label}")

    if review_status is not None and review_status not in SPEC_REVIEW_RESULT_ALLOWED_REVIEW_STATUSES:
        errors.append(f"Review status is not an allowed value: {review_status}")

    if immediate_stage is not None:
        if immediate_stage == "test-spec":
            errors.append("Immediate next stage must not be test-spec")
        if (
            immediate_stage not in SPEC_REVIEW_RESULT_ALLOWED_IMMEDIATE_STAGES
            or immediate_stage in SPEC_REVIEW_RESULT_PSEUDO_ROUTING_VALUES
        ):
            errors.append(f"Immediate next stage is not an allowed value: {immediate_stage}")

    if readiness is not None:
        if readiness == "not-assessed":
            errors.append("Eventual test-spec readiness must not be not-assessed")
        if readiness not in SPEC_REVIEW_RESULT_ALLOWED_READINESS:
            errors.append(f"Eventual test-spec readiness is not an allowed value: {readiness}")

    if review_status == "approved":
        if immediate_stage not in {"architecture", "plan"}:
            errors.append("approved requires Immediate next stage architecture or plan")
        if readiness not in {"ready", "conditionally-ready"}:
            errors.append(
                "approved requires Eventual test-spec readiness ready or conditionally-ready"
            )

    if review_status == "changes-requested":
        if immediate_stage not in {"spec revision", "review-resolution"}:
            errors.append(
                "changes-requested requires Immediate next stage spec revision or review-resolution"
            )
        if readiness != "not-ready":
            errors.append("changes-requested requires Eventual test-spec readiness not-ready")

    if review_status == "blocked":
        if immediate_stage not in {"review-resolution", "none"}:
            errors.append("blocked requires Immediate next stage review-resolution or none")
        if readiness != "not-ready":
            errors.append("blocked requires Eventual test-spec readiness not-ready")

    if review_status == "inconclusive":
        if immediate_stage != "none":
            errors.append("inconclusive requires Immediate next stage none")
        if readiness != "not-ready":
            errors.append("inconclusive requires Eventual test-spec readiness not-ready")
        if stop_condition in {None, "", "none"}:
            errors.append("inconclusive requires a concrete Stop condition")

    if readiness == "conditionally-ready" and not readiness_condition:
        errors.append("conditionally-ready requires a named condition")

    return errors


def _placeholder_values(value: str | None) -> set[str]:
    if value is None:
        return set()
    stripped = value.strip()
    if stripped.startswith("<") and stripped.endswith(">"):
        stripped = stripped[1:-1]
    return {part.strip() for part in stripped.split("|") if part.strip()}


def _sectionless_text(body: str, heading: str) -> str:
    lines = body.splitlines()
    result: list[str] = []
    skipping = False
    marker = f"## {heading}"
    for line in lines:
        if line.strip() == marker:
            skipping = True
            continue
        if skipping and line.startswith("## "):
            skipping = False
        if not skipping:
            result.append(line)
    return "\n".join(result)


def _normalized_material_field_mentions(text: str) -> set[str]:
    mentions: set[str] = set()
    for line in _iter_lines_outside_fences(text):
        stripped = line.strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        stripped = stripped.strip("` ")
        if not stripped:
            continue
        label = stripped.split(":", 1)[0].split(",", 1)[0].strip("` ")
        normalized = label.lower()
        if normalized in {field.lower() for field in REVIEW_FAMILY_PARSER_FIELD_LABELS}:
            mentions.add(normalized)
    return mentions


def validate_spec_review_canonical_contract(skill_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        _, body = load_skill_file(skill_path)
    except ValueError as exc:
        return [str(exc)]

    result_skeleton_path = skill_path.parent / "assets" / "review-result-skeleton.md"
    material_finding_path = skill_path.parent / "assets" / "material-finding.md"

    if not result_skeleton_path.is_file():
        errors.append(f"{skill_path}: spec-review result skeleton is missing")
        result_skeleton_text = ""
    else:
        result_skeleton_text = result_skeleton_path.read_text(encoding="utf-8")

    result_fields = _parse_spec_review_result_fields(result_skeleton_text)
    required_result_fields = {
        "review-status": "Review status",
        "immediate-next-stage": "Immediate next stage",
        "eventual-test-spec-readiness": "Eventual test-spec readiness",
        "stop-condition": "Stop condition",
    }
    for normalized_label, display_label in required_result_fields.items():
        if normalized_label not in result_fields:
            errors.append(
                f"{result_skeleton_path}: spec-review result skeleton missing field: {display_label}"
            )

    immediate_values = _placeholder_values(result_fields.get("immediate-next-stage"))
    if "test-spec" in immediate_values:
        errors.append(
            "spec-review result skeleton Immediate next stage enum must exclude test-spec"
        )
    if immediate_values and immediate_values != SPEC_REVIEW_RESULT_ALLOWED_IMMEDIATE_STAGES:
        expected = ", ".join(sorted(SPEC_REVIEW_RESULT_ALLOWED_IMMEDIATE_STAGES))
        actual = ", ".join(sorted(immediate_values))
        errors.append(
            "spec-review result skeleton Immediate next stage enum mismatch: "
            f"expected {expected}; found {actual}"
        )

    readiness_values = _placeholder_values(result_fields.get("eventual-test-spec-readiness"))
    if "not-assessed" in readiness_values:
        errors.append(
            "spec-review result skeleton Eventual test-spec readiness enum must exclude not-assessed"
        )
    if readiness_values and readiness_values != SPEC_REVIEW_RESULT_ALLOWED_READINESS:
        expected = ", ".join(sorted(SPEC_REVIEW_RESULT_ALLOWED_READINESS))
        actual = ", ".join(sorted(readiness_values))
        errors.append(
            "spec-review result skeleton Eventual test-spec readiness enum mismatch: "
            f"expected {expected}; found {actual}"
        )

    routing_section = _extract_markdown_section(body, "Routing and testability assessment")
    if routing_section is None:
        errors.append(
            f"{skill_path}: spec-review must include a Routing and testability assessment section"
        )
        routing_section = ""

    for value in sorted(SPEC_REVIEW_RESULT_ALLOWED_IMMEDIATE_STAGES):
        if value not in routing_section:
            errors.append(
                f"{skill_path}: Routing and testability assessment missing immediate-stage value: {value}"
            )
    for value in sorted(SPEC_REVIEW_RESULT_ALLOWED_READINESS):
        if value not in routing_section:
            errors.append(
                f"{skill_path}: Routing and testability assessment missing readiness value: {value}"
            )
    if "approved" in routing_section and "not-ready" in routing_section:
        approved_rule_pattern = re.compile(
            r"approved[^\n.]*Eventual test-spec readiness[^\n.]*"
            r"(?:ready[^\n.]*conditionally-ready|conditionally-ready[^\n.]*ready)",
            re.IGNORECASE,
        )
        if not approved_rule_pattern.search(routing_section):
            errors.append(
                f"{skill_path}: Routing and testability assessment must bind approved to ready or conditionally-ready"
            )

    no_test_spec_routing = re.search(
        r"(?:do not|never)[^\n.]*test-spec[^\n.]*Immediate next stage",
        routing_section,
        re.IGNORECASE,
    ) or re.search(
        r"Immediate next stage[^\n.]*(?:do not|never|must not)[^\n.]*test-spec",
        routing_section,
        re.IGNORECASE,
    )
    if not no_test_spec_routing:
        errors.append(
            f"{skill_path}: Routing and testability assessment must state that test-spec is not an Immediate next stage value"
        )

    if material_finding_path.is_file():
        material_finding_text = material_finding_path.read_text(encoding="utf-8")
        material_finding_body = _asset_body_without_metadata(material_finding_text)
        material_labels = {
            label.lower()
            for label in _asset_field_labels(material_finding_body)
            if label in REVIEW_FAMILY_PARSER_FIELD_LABELS
        }
        missing_material_labels = {
            label.lower() for label in REVIEW_FAMILY_PARSER_FIELD_LABELS
        } - material_labels
        for label in sorted(missing_material_labels):
            errors.append(
                f"{material_finding_path}: spec-review material-finding asset missing field label: {label}"
            )

    skill_without_resource_map = _sectionless_text(body, "Resource map")
    skill_material_mentions = _normalized_material_field_mentions(skill_without_resource_map)
    complete_required_mentions = {
        label.lower() for label in REVIEW_FAMILY_PARSER_FIELD_LABELS
    }
    if complete_required_mentions <= skill_material_mentions:
        errors.append(
            "spec-review SKILL.md must not re-enumerate the complete material-finding field list outside the Resource map"
        )

    return errors
INSTALLED_SKILL_PLAN_SURFACE_PATHS = (
    "docs/plan.md",
    "docs/plans/YYYY-MM-DD-slug.md",
    "docs/changes/<change-id>/change.yaml",
    "docs/changes/<change-id>/",
)
INSTALLED_SKILL_PLAN_INDEX_LINK_EXAMPLE = "[Title](plans/YYYY-MM-DD-slug.md)"


@dataclass(frozen=True)
class ValidationResult:
    checked_files: list[Path]
    errors: list[str]


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _normalized_asset_label(label: str) -> str:
    return re.sub(r"[-_\s]+", "-", label.strip().lower())


def _consume_block(lines: list[str], index: int) -> tuple[list[str], int]:
    block: list[str] = []
    while index < len(lines):
        raw_line = lines[index]
        if raw_line.startswith("  "):
            block.append(raw_line[2:])
            index += 1
            continue
        if raw_line.strip():
            break
        block.append("")
        index += 1
    return block, index


def _parse_frontmatter(frontmatter_lines: list[str], path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    index = 0
    while index < len(frontmatter_lines):
        raw_line = frontmatter_lines[index]
        index += 1

        if not raw_line.strip():
            continue
        if raw_line.startswith(" ") or raw_line.startswith("\t"):
            raise ValueError(f"{path}: frontmatter keys must be top-level mappings")
        if ":" not in raw_line:
            raise ValueError(f"{path}: invalid frontmatter line: {raw_line}")

        key, remainder = raw_line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"{path}: frontmatter key must not be empty")
        remainder = remainder.lstrip()

        if remainder in {">", "|"}:
            block, index = _consume_block(frontmatter_lines, index)
            value = "\n".join(block).strip()
        elif remainder:
            value = _strip_quotes(remainder)
        else:
            block, index = _consume_block(frontmatter_lines, index)
            value = "\n".join(block).strip()

        metadata[key] = value

    return metadata


def load_skill_file(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: file must begin with YAML frontmatter")

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        raise ValueError(f"{path}: YAML frontmatter must end with '---'")

    metadata = _parse_frontmatter(lines[1:closing_index], path)
    body = "\n".join(lines[closing_index + 1 :])
    return metadata, body


def load_skill_schema() -> dict:
    return json.loads(SKILL_SCHEMA_PATH.read_text(encoding="utf-8"))


def _iter_lines_outside_fences(text: str) -> list[str]:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return lines


def _iter_resource_instruction_segments(body: str) -> list[ResourceInstructionSegment]:
    segments: list[ResourceInstructionSegment] = []
    current_parts: list[str] = []
    current_start_line: int | None = None
    current_end_line: int | None = None
    current_kind: str | None = None

    def flush() -> None:
        nonlocal current_parts, current_start_line, current_end_line, current_kind
        if current_parts and current_start_line is not None and current_end_line is not None:
            segments.append(
                ResourceInstructionSegment(
                    text="\n".join(current_parts),
                    start_line=current_start_line,
                    end_line=current_end_line,
                    kind=current_kind or "paragraph",
                )
            )
        current_parts = []
        current_start_line = None
        current_end_line = None
        current_kind = None

    in_fence = False
    in_resource_map = False
    for line_number, line in enumerate(body.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped == "## Resource map":
            flush()
            in_resource_map = True
            continue
        if in_resource_map:
            if line.startswith("## "):
                in_resource_map = False
            else:
                continue
        if not stripped:
            flush()
            continue
        if stripped.startswith("## "):
            flush()
            continue
        list_match = MARKDOWN_LIST_ITEM_PATTERN.match(line)
        if list_match:
            flush()
            current_parts.append(stripped)
            current_start_line = line_number
            current_end_line = line_number
            current_kind = "list-item"
            continue
        if current_kind is None:
            current_parts.append(stripped)
            current_start_line = line_number
            current_end_line = line_number
            current_kind = "paragraph"
            continue
        current_parts.append(stripped)
        current_end_line = line_number
    flush()
    return segments


def _extract_markdown_section(body: str, heading: str) -> str | None:
    marker = f"## {heading}"
    lines = body.splitlines()
    start_index = None
    for index, line in enumerate(lines):
        if line.strip() == marker:
            start_index = index
            break
    if start_index is None:
        return None

    section_lines: list[str] = []
    for line in lines[start_index + 1 :]:
        if line.startswith("## "):
            break
        section_lines.append(line)
    return "\n".join(section_lines).strip()


def _clean_table_cell(cell: str) -> str:
    value = cell.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1]
    return value.strip()


def _is_blank_or_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return not normalized or normalized in {"none", "not applicable", "n/a", "-"}


def _parse_markdown_table(section: str, expected_columns: tuple[str, ...]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    for index, line in enumerate(lines):
        cells = [_clean_table_cell(cell) for cell in line.strip().strip("|").split("|")]
        if tuple(cells) != expected_columns:
            continue
        if index + 2 > len(lines):
            return rows
        for row_line in lines[index + 2 :]:
            row_cells = [
                _clean_table_cell(cell)
                for cell in row_line.strip().strip("|").split("|")
            ]
            if len(row_cells) != len(expected_columns):
                continue
            rows.append(dict(zip(expected_columns, row_cells)))
        return rows
    return rows


def _split_ids(value: str, prefix: str) -> list[str]:
    if _is_blank_or_placeholder(value):
        return []
    return re.findall(rf"\b{re.escape(prefix)}\d+\b", value)


def _extract_test_case_blocks(section: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    current_id: str | None = None
    current_lines: list[str] = []
    for line in section.splitlines():
        match = re.match(r"^###\s+(?P<id>T\d+)\b", line.strip())
        if match:
            if current_id is not None:
                blocks.append((current_id, "\n".join(current_lines)))
            current_id = match.group("id")
            current_lines = [line]
            continue
        if current_id is not None:
            current_lines.append(line)
    if current_id is not None:
        blocks.append((current_id, "\n".join(current_lines)))
    return blocks


def _test_case_command_ids(block: str) -> list[str]:
    for line in block.splitlines():
        if line.strip().startswith("- Command IDs:"):
            return _split_ids(line.split(":", 1)[1], "CMD")
    return []


def validate_test_spec_proof_contract_fixture(
    body: str,
    *,
    milestone_based_plan: bool,
) -> list[str]:
    """Representative fixture validation for the test-spec proof contract.

    This intentionally validates static representative outputs rather than every
    historical test-spec artifact.
    """

    errors: list[str] = []
    validation_section = _extract_markdown_section(body, "Validation commands")
    if validation_section is None:
        errors.append("missing Validation commands section")
        command_rows: list[dict[str, str]] = []
    else:
        command_rows = _parse_markdown_table(
            validation_section,
            TEST_SPEC_VALIDATION_COMMAND_COLUMNS,
        )

    command_by_id: dict[str, dict[str, str]] = {}
    command_values: set[str] = set()
    if command_rows:
        for row in command_rows:
            command_id = row["Command ID"]
            command = row["Command"]
            classification = row["Classification"]
            if _is_blank_or_placeholder(command_id):
                errors.append("validation command row missing command ID")
                continue
            command_by_id[command_id] = row
            if not _is_blank_or_placeholder(command):
                command_values.add(command)
            if _is_blank_or_placeholder(classification):
                errors.append(f"command {command_id} missing classification")
            elif classification not in TEST_SPEC_COMMAND_CLASSIFICATIONS:
                errors.append(
                    f"command {command_id} has unknown classification: {classification}"
                )
            for column in (
                "Command",
                "Owner",
                "Owning milestone",
                "First required milestone",
                "Failure behavior",
                "Zero-test behavior",
                "Evidence artifact",
                "Safe mode / side-effect boundary",
            ):
                if _is_blank_or_placeholder(row[column]):
                    errors.append(f"command {command_id} missing {column.lower()}")
            if classification == "planned-for-implementation":
                if _is_blank_or_placeholder(row["Owner"]):
                    errors.append(f"planned command {command_id} missing owner")
                if _is_blank_or_placeholder(row["Owning milestone"]):
                    errors.append(f"planned command {command_id} missing owning milestone")
                if _is_blank_or_placeholder(row["First required milestone"]):
                    errors.append(
                        f"planned command {command_id} missing first required milestone"
                    )
    elif validation_section is not None and "No validation commands are part of this proof map" not in validation_section:
        errors.append("Validation commands section missing command ledger or no-command rationale")

    test_cases_section = _extract_markdown_section(body, "Test cases") or ""
    for test_id, block in _extract_test_case_blocks(test_cases_section):
        command_ids = _test_case_command_ids(block)
        raw_commands = [match.group("command").strip() for match in TEST_SPEC_COMMAND_PATTERN.finditer(block)]
        if raw_commands and not command_ids:
            errors.append(f"test case {test_id} uses raw command without Command ID")
        for command_id in command_ids:
            if command_id not in command_by_id:
                errors.append(f"test case {test_id} references unknown Command ID {command_id}")
        for command in raw_commands:
            if command not in command_values:
                errors.append(f"named validation command missing from ledger: {command}")

    milestone_section = _extract_markdown_section(body, "Milestone proof map")
    if milestone_based_plan:
        if milestone_section is None:
            errors.append("milestone-based plan missing Milestone proof map")
        else:
            milestone_rows = _parse_markdown_table(
                milestone_section,
                TEST_SPEC_MILESTONE_PROOF_COLUMNS,
            )
            if not milestone_rows:
                errors.append("milestone-based plan missing Milestone proof map")
            for row in milestone_rows:
                for command_id in _split_ids(row["Command IDs"], "CMD"):
                    if command_id not in command_by_id:
                        errors.append(
                            f"milestone {row['Milestone']} references unknown Command ID {command_id}"
                        )
    elif milestone_section is not None and "Not applicable" not in milestone_section:
        # Non-milestone fixtures may still include an explicit map; no error.
        pass

    return errors


def _normalized_prose(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _has_create_or_request_change_pack_behavior(text: str) -> bool:
    normalized = _normalized_prose(text)
    has_create_or_request = (
        "create or request" in normalized
        or "create or require" in normalized
        or "create or block" in normalized
    )
    return (
        "change pack" in normalized
        and has_create_or_request
        and "recording status:" in normalized
        and "recorded" in normalized
    )


def _has_conditional_review_resolution_behavior(text: str) -> bool:
    normalized = _normalized_prose(text)
    if INSTALLED_SKILL_PLACEMENT_REVIEW_RESOLUTION_PATH not in text:
        return False
    conditional_terms = (
        "only when",
        "when material",
        "when findings",
        "when blocking",
        "conditional",
        "if material",
    )
    return any(term in normalized for term in conditional_terms)


def _has_isolated_advisory_carveout(text: str) -> bool:
    normalized = _normalized_prose(text)
    return (
        ("isolated advisory" in normalized or "outside `spec-review`" in normalized)
        and (
            "do not create lifecycle artifacts" in normalized
            or "without lifecycle artifacts" in normalized
            or "no formal recording" in normalized
            or "no lifecycle artifacts" in normalized
        )
    )


def _validate_stage_owned_review_record_type(
    *,
    path: Path,
    skill_name: str,
    text: str,
    errors: list[str],
) -> None:
    config = INSTALLED_SKILL_PLACEMENT_REVIEW_RECORD_TYPES.get(skill_name)
    if config is None:
        return

    normalized = _normalized_prose(text)
    expected_terms = config["record_type_terms"]
    forbidden_terms = config["forbidden_record_type_terms"]

    if not any(term in normalized for term in expected_terms):
        errors.append(
            f"{path}: installed-skill placement contract must state the stage-owned record type {skill_name} record(s)"
        )
    for forbidden in forbidden_terms:
        if forbidden in normalized:
            errors.append(
                f"{path}: installed-skill placement contract names the wrong stage-owned record type {forbidden}"
            )


def validate_installed_skill_artifact_placement_contract(
    path: Path,
    skill_name: str,
    body: str,
) -> list[str]:
    """Validate first-slice installed-skill placement contract wording.

    M1 exposed this as a fixture-backed helper. M2 connects it to canonical
    first-slice skill validation after updating the public skill text.
    """
    errors: list[str] = []
    review_path = INSTALLED_SKILL_PLACEMENT_REVIEW_PATHS.get(skill_name)
    if review_path is None:
        return errors

    placement_source = body
    if skill_name == "test-spec-review":
        recording_reference = (
            path.parent
            / "references"
            / "test-spec-review-recording-and-settlement.md"
        )
        if recording_reference.is_file():
            placement_source = "\n".join(
                [body, recording_reference.read_text(encoding="utf-8")]
            )

    placement = _extract_markdown_section(placement_source, "Artifact placement")
    if placement is None:
        errors.append(
            f"{path}: installed-skill placement contract must include an Artifact placement section"
        )
        placement = body

    _validate_stage_owned_review_record_type(
        path=path,
        skill_name=skill_name,
        text=placement,
        errors=errors,
    )
    if review_path not in placement:
        errors.append(
            f"{path}: installed-skill placement contract missing default formal review record path {review_path}"
        )
    if INSTALLED_SKILL_PLACEMENT_REVIEW_LOG_PATH not in placement:
        errors.append(
            f"{path}: installed-skill placement contract missing review-log path {INSTALLED_SKILL_PLACEMENT_REVIEW_LOG_PATH}"
        )
    if not _has_conditional_review_resolution_behavior(placement):
        errors.append(
            f"{path}: installed-skill placement contract must describe {INSTALLED_SKILL_PLACEMENT_REVIEW_RESOLUTION_PATH} as conditional"
        )
    if not _has_create_or_request_change_pack_behavior(placement):
        errors.append(
            f"{path}: installed-skill placement contract must state create-or-request change-pack behavior before claiming Recording status: recorded"
        )
    if not _has_isolated_advisory_carveout(placement):
        errors.append(
            f"{path}: installed-skill placement contract must preserve isolated advisory review without lifecycle artifacts"
        )
    return errors


def validate_installed_skill_plan_surface_contract(
    path: Path,
    skill_name: str,
    body: str,
) -> list[str]:
    """Validate first-slice plan-surface disambiguation fixture wording."""
    if skill_name not in {"plan", "plan-review", "implement", "verify"}:
        return []
    errors: list[str] = []
    missing = [
        surface for surface in INSTALLED_SKILL_PLAN_SURFACE_PATHS if surface not in body
    ]
    if missing:
        errors.append(
            f"{path}: installed-skill plan surface contract must distinguish docs/plan.md, docs/plans/YYYY-MM-DD-slug.md, docs/changes/<change-id>/change.yaml, and docs/changes/<change-id>/"
        )
    if skill_name == "plan" and INSTALLED_SKILL_PLAN_INDEX_LINK_EXAMPLE not in body:
        errors.append(
            f"{path}: installed-skill plan surface contract must tell plan authors to use clickable relative Markdown links like {INSTALLED_SKILL_PLAN_INDEX_LINK_EXAMPLE} in docs/plan.md"
        )
    return errors


def _parse_colon_fields(section: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("- "):
            line = line[2:].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().strip("`")
        if key:
            fields[key] = value.strip()
    return fields


def _contains_fenced_block(section: str) -> bool:
    return any(line.strip().startswith("```") for line in section.splitlines())


def _resource_files(skill_dir: Path) -> list[Path]:
    resources: list[Path] = []
    for directory_name in PACKAGED_RESOURCE_DIRS:
        resource_dir = skill_dir / directory_name
        if not resource_dir.is_dir():
            continue
        for path in sorted(resource_dir.rglob("*")):
            if path.is_file() and path.name != ".gitkeep":
                resources.append(path)
    return resources


def _resource_entry_text(section: str, relative_resource: str) -> str | None:
    lines = section.splitlines()
    for index, line in enumerate(lines):
        if relative_resource in line:
            entry_lines = [line.strip()]
            for continuation in lines[index + 1 :]:
                if continuation.startswith("- "):
                    break
                if continuation.strip():
                    entry_lines.append(continuation.strip())
            return " ".join(entry_lines)
    return None


def _resource_map_entries(section: str) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    lines = section.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        match = RESOURCE_MAP_ENTRY_PATTERN.match(line)
        if not match:
            index += 1
            continue
        entry_lines = [line.strip()]
        index += 1
        while index < len(lines):
            continuation = lines[index]
            if RESOURCE_MAP_ENTRY_PATTERN.match(continuation):
                break
            if continuation.startswith("- ") and continuation.strip():
                break
            if continuation.strip():
                entry_lines.append(continuation.strip())
            index += 1
        entries.append(
            (
                match.group("verb").upper(),
                match.group("path").strip(),
                " ".join(entry_lines),
            )
        )
    return entries


def _sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mapped_resource_identities_for_skill(skill_dir: Path) -> tuple[MappedResourceIdentity, ...]:
    """Return mapped skill-local resource identities from canonical skill source."""

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return ()

    try:
        metadata, body = load_skill_file(skill_file)
    except (OSError, ValueError):
        return ()

    skill_name = metadata.get("name")
    if not isinstance(skill_name, str) or not skill_name:
        skill_name = skill_dir.name

    section = _extract_markdown_section(body, "Resource map")
    if section is None:
        return ()

    identities: list[MappedResourceIdentity] = []
    for _verb, relative_path, _entry in _resource_map_entries(section):
        if _mapped_resource_containment_error(relative_path, skill_dir) is not None:
            continue
        path = skill_dir / relative_path
        if not path.is_file():
            continue
        identities.append(
            MappedResourceIdentity(
                skill_name=skill_name,
                relative_path=relative_path,
                path=path,
                sha256=_sha256_bytes(path),
            )
        )
    return tuple(identities)


def mapped_resource_parity_errors(
    canonical_skill_dir: Path,
    generated_skill_dir: Path,
    *,
    skill_label: str | None = None,
    surface_label: str,
    actual_hash_label: str = "generated",
) -> list[str]:
    """Compare mapped resources by skill-root relative path and raw-byte SHA-256."""

    errors: list[str] = []
    for identity in mapped_resource_identities_for_skill(canonical_skill_dir):
        label = skill_label or identity.skill_name
        generated_path = generated_skill_dir / identity.relative_path
        if not generated_path.is_file():
            errors.append(
                f"mapped resource missing: {label}: {identity.relative_path} "
                f"in {surface_label}"
            )
            continue

        actual_sha256 = _sha256_bytes(generated_path)
        if actual_sha256 != identity.sha256:
            errors.append(
                f"mapped resource parity mismatch: {label}: {identity.relative_path}: "
                f"canonical sha256={identity.sha256}; "
                f"{actual_hash_label} sha256={actual_sha256}"
            )
    return errors


def _mapped_resource_containment_error(resource_path: str, skill_dir: Path) -> str | None:
    raw_path = Path(resource_path)
    if raw_path.is_absolute():
        return (
            f"mapped resource path '{resource_path}' must be relative to the skill root "
            "and stay inside it"
        )
    resolved = (skill_dir / resource_path).resolve()
    if not _is_relative_to(resolved, skill_dir.resolve()):
        return (
            f"mapped resource path '{resource_path}' must be relative to the skill root "
            "and stay inside it"
        )
    return None


def _skill_name_for_path(path: Path) -> str:
    return path.parent.name


def _has_resource_integrity_exception(path: Path, resource_path: str, line: str) -> bool:
    return (
        _skill_name_for_path(path),
        resource_path,
        line,
    ) in TEMPORARY_RESOURCE_INTEGRITY_EXCEPTIONS


def _find_skill_local_resource_references(
    segment: ResourceInstructionSegment,
) -> tuple[SkillLocalResourceReference, ...]:
    references: list[SkillLocalResourceReference] = []
    for match in SKILL_LOCAL_RESOURCE_REFERENCE_PATTERN.finditer(segment.text):
        references.append(
            SkillLocalResourceReference(
                path=match.group("path"),
                start=match.start("path"),
                end=match.end("path"),
                line_number=segment.line_number_for_offset(match.start("path")),
            )
        )
    return tuple(references)


def _resource_reference_has_external_context(
    line: str,
    reference: SkillLocalResourceReference,
    *,
    previous_reference_end: int,
    next_reference_start: int,
) -> bool:
    prefix = line[previous_reference_end : reference.start]
    suffix = line[reference.end : next_reference_start]
    full_prefix = line[: reference.start]
    return bool(
        PUBLISHED_RESOURCE_EXTERNAL_PREFIX_PATTERN.search(prefix)
        or PUBLISHED_RESOURCE_EXTERNAL_SUFFIX_PATTERN.match(suffix)
        or PUBLISHED_RESOURCE_ILLUSTRATIVE_PREFIX_PATTERN.search(prefix)
        or (
            reference.path in PUBLISHED_PROJECT_PROVIDED_HELPER_PATHS
            and re.search(r"\bwhen the project provides the helper\b", full_prefix, re.IGNORECASE)
        )
    )


def _iter_unmapped_skill_local_resource_references(
    path: Path,
    body: str,
    mapped_resources: set[str],
) -> list[tuple[int, str, str]]:
    references: list[tuple[int, str, str]] = []
    for segment in _iter_resource_instruction_segments(body):
        if not LEGACY_RESOURCE_LOADING_CONTEXT_PATTERN.search(segment.text):
            continue
        line_references = _find_skill_local_resource_references(segment)
        for index, reference in enumerate(line_references):
            if reference.path in mapped_resources:
                continue
            previous_reference_end = line_references[index - 1].end if index else 0
            next_reference_start = (
                line_references[index + 1].start
                if index + 1 < len(line_references)
                else len(segment.text)
            )
            if _resource_reference_has_external_context(
                segment.text,
                reference,
                previous_reference_end=previous_reference_end,
                next_reference_start=next_reference_start,
            ):
                continue
            if _has_resource_integrity_exception(path, reference.path, segment.text):
                continue
            references.append((reference.line_number, reference.path, segment.text.strip()))
    return references


def _asset_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = PLAN_ASSET_METADATA_PATTERN.match(stripped)
        if not match:
            continue
        metadata[match.group("key").strip()] = match.group("value").strip()
    return metadata


def _asset_structural_fingerprint(text: str) -> str:
    normalized_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        line = PLAN_ASSET_PLACEHOLDER_PATTERN.sub("<>", line)
        normalized_lines.append(line)
    normalized = "\n".join(normalized_lines)
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _markdown_h2_sections(text: str) -> list[str]:
    sections: list[str] = []
    for line in text.splitlines():
        if not line.startswith("## "):
            continue
        heading = line[3:].strip()
        if heading:
            sections.append(heading)
    return sections


def _expected_sections_from_resource_entry(entry: str) -> list[str]:
    match = PLAN_ASSET_SECTIONS_PATTERN.search(entry)
    if not match:
        return []
    raw_sections = match.group("sections")
    return [
        section.strip().rstrip(".")
        for section in raw_sections.split(";")
        if section.strip()
    ]


def _asset_body_without_metadata(text: str) -> str:
    lines = [
        line
        for line in text.splitlines()
        if not (line.strip().startswith("<!--") and line.strip().endswith("-->"))
    ]
    return "\n".join(lines)


def _validate_plan_asset_file(path: Path, relative_resource: str, text: str) -> list[str]:
    errors: list[str] = []
    metadata = _asset_metadata(text)

    missing = sorted(PLAN_ASSET_REQUIRED_METADATA_FIELDS - metadata.keys())
    for field in missing:
        errors.append(f"{path}: asset metadata missing required field '{field}'")

    if missing:
        return errors

    if metadata["Skill"] != "plan":
        errors.append(
            f"{path}: plan asset pilot asset '{relative_resource}' must declare Skill: plan"
        )

    status = metadata["Template status"]
    if status not in PLAN_ASSET_TEMPLATE_STATUS_VALUES:
        allowed = ", ".join(sorted(PLAN_ASSET_TEMPLATE_STATUS_VALUES))
        errors.append(f"{path}: asset metadata Template status must be one of {allowed}")
    if status != "normative":
        errors.append(
            f"{path}: plan asset pilot asset '{relative_resource}' must use normative status"
        )

    maintained_alongside = metadata["Maintained alongside"]
    if maintained_alongside != "skills/plan/SKILL.md":
        errors.append(
            f"{path}: plan asset pilot asset '{relative_resource}' must be maintained alongside skills/plan/SKILL.md"
        )

    fingerprint = metadata["Structural-fingerprint"]
    expected_fingerprint = _asset_structural_fingerprint(text)
    if fingerprint != expected_fingerprint:
        errors.append(
            f"{path}: asset '{relative_resource}' structural fingerprint mismatch: expected {expected_fingerprint}"
        )

    if not PLAN_ASSET_PLACEHOLDER_PATTERN.search(_asset_body_without_metadata(text)):
        errors.append(
            f"{path}: asset '{relative_resource}' must include a visible placeholder"
        )

    for line_number, line in enumerate(_iter_lines_outside_fences(text), start=1):
        if not PUBLISHED_INTERNAL_PATH_PATTERN.search(line):
            continue
        context = _required_repository_dependency_context(line)
        if context is None:
            continue
        match = PUBLISHED_INTERNAL_PATH_REFERENCE_PATTERN.search(line)
        dependency = match.group("path") if match else line.strip()
        errors.append(
            f"{path}:{line_number}: asset '{relative_resource}' must not require repository-root dependency: {dependency}"
        )

    return errors


def _validate_plan_asset_pilot(path: Path, body: str, skill_name: str | None) -> list[str]:
    skill_dir = path.parent
    asset_dir = skill_dir / "assets"
    if not asset_dir.is_dir():
        return []
    if skill_name != "plan":
        return []

    errors: list[str] = []
    assets = [
        asset
        for asset in sorted(asset_dir.rglob("*"))
        if asset.is_file() and asset.name != ".gitkeep"
    ]
    relative_assets = {asset.relative_to(skill_dir).as_posix() for asset in assets}
    if relative_assets != PLAN_ASSET_PILOT_APPROVED_ASSETS:
        expected = ", ".join(sorted(PLAN_ASSET_PILOT_APPROVED_ASSETS))
        actual = ", ".join(sorted(relative_assets)) or "none"
        errors.append(
            f"{path}: plan asset pilot must ship exactly approved assets: expected {expected}; found {actual}"
        )

    section = _extract_markdown_section(body, "Resource map")
    if section is None:
        return errors

    for relative_resource in sorted(relative_assets & PLAN_ASSET_PILOT_APPROVED_ASSETS):
        entry = _resource_entry_text(section, relative_resource)
        if entry is None:
            continue
        expected_prefix = f"- COPY `{relative_resource}`"
        if not entry.startswith(expected_prefix):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must use literal COPY"
            )
        if not RESOURCE_LOAD_CONDITION_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must include a trigger condition"
            )
        if not PLAN_ASSET_FIELDS_TO_FILL_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must name fields or structures to fill"
            )
    if "Do not emit unfilled placeholders" not in section:
        errors.append(
            f"{path}: Resource map must instruct agents not to emit unfilled placeholders"
        )

    for asset in assets:
        relative_resource = asset.relative_to(skill_dir).as_posix()
        if relative_resource not in PLAN_ASSET_PILOT_APPROVED_ASSETS:
            continue
        text = asset.read_text(encoding="utf-8")
        errors.extend(_validate_plan_asset_file(asset, relative_resource, text))

    skeleton = asset_dir / "plan-skeleton.md"
    if skeleton.is_file():
        skeleton_entry = _resource_entry_text(section, "assets/plan-skeleton.md")
        if skeleton_entry is not None:
            expected_sections = _expected_sections_from_resource_entry(skeleton_entry)
            actual_sections = _markdown_h2_sections(
                skeleton.read_text(encoding="utf-8")
            )
            if expected_sections and set(expected_sections) != set(actual_sections):
                errors.append(
                    f"{path}: plan-skeleton section set does not match SKILL.md expected sections"
                )

    return errors


def validate_project_map_contract_fixture(
    path: Path,
    metadata: dict[str, str],
    body: str,
    *,
    diagnostic_subject: str = "contract fixture",
) -> list[str]:
    """Validate controlled and canonical project-map contract surfaces."""

    errors: list[str] = []

    for field in ("version", "schema-version", "description", "argument-hint"):
        if field not in metadata:
            errors.append(
                f"{path}: project-map {diagnostic_subject} missing frontmatter field '{field}'"
            )

    workflow_role = _extract_markdown_section(body, "Workflow role")
    if workflow_role is None:
        errors.append(f"{path}: project-map {diagnostic_subject} missing Workflow role")
    else:
        fields = _parse_colon_fields(workflow_role)
        missing_role_fields = sorted(READABILITY_REQUIRED_ROLE_FIELDS - fields.keys())
        for field in missing_role_fields:
            errors.append(
                f"{path}: project-map workflow role missing required field '{field}'"
            )

    for operation in PROJECT_MAP_REQUIRED_OPERATIONS:
        if f"`{operation}`" not in body and f"- {operation}" not in body:
            errors.append(f"{path}: project-map contract missing operation '{operation}'")
    for scope in ("repository", "area:<slug>"):
        if f"`{scope}`" not in body:
            errors.append(f"{path}: project-map contract missing map scope '{scope}'")

    metadata_section = _extract_markdown_section(body, "Map metadata and freshness")
    if metadata_section is None:
        errors.append(
            f"{path}: project-map contract missing Map metadata and freshness section"
        )
        metadata_section = ""
    for field in PROJECT_MAP_REQUIRED_METADATA_FIELDS:
        if field not in metadata_section:
            errors.append(
                f"{path}: project-map contract missing map metadata field '{field}'"
            )

    evidence_section = _extract_markdown_section(body, "Evidence and confidence")
    if evidence_section is None:
        errors.append(f"{path}: project-map contract missing Evidence and confidence section")
        evidence_section = ""
    for evidence_class in PROJECT_MAP_REQUIRED_EVIDENCE_CLASSES:
        if evidence_class not in evidence_section.lower():
            errors.append(
                f"{path}: project-map contract missing evidence class '{evidence_class}'"
            )
    if "Material claim example" not in evidence_section:
        errors.append(f"{path}: project-map contract missing material claim example")
    if "Incidental statement example" not in evidence_section:
        errors.append(f"{path}: project-map contract missing incidental statement example")

    root_area_section = _extract_markdown_section(body, "Root and area maps")
    if root_area_section is None:
        errors.append(f"{path}: project-map contract missing Root and area maps section")
        root_area_section = ""
    structure_section = _extract_markdown_section(body, "Required output structure")
    if structure_section is None:
        errors.append(f"{path}: project-map contract missing Required output structure section")
        structure_section = ""
    if "sole owner" not in structure_section.lower():
        errors.append(f"{path}: project-map contract must identify the skeleton as structural owner")

    output_skeleton = _extract_markdown_section(body, "Output skeleton") or ""
    if "- Operation:" not in output_skeleton:
        errors.append(f"{path}: project-map result must emit Operation")
    if "- Map scope:" not in output_skeleton:
        errors.append(f"{path}: project-map result must emit Map scope")
    if "- Mode:" in output_skeleton:
        errors.append(f"{path}: project-map result must not emit legacy Mode")

    resource_map = _extract_markdown_section(body, "Resource map")
    if resource_map is None:
        errors.append(f"{path}: project-map contract missing Resource map")
        resource_map = ""
    skeleton_entry = _resource_entry_text(resource_map, PROJECT_MAP_SKELETON)
    if skeleton_entry is None:
        errors.append(
            f"{path}: Resource map must name packaged resource '{PROJECT_MAP_SKELETON}'"
        )
    else:
        expected_prefix = f"- COPY `{PROJECT_MAP_SKELETON}`"
        if not skeleton_entry.startswith(expected_prefix):
            errors.append(
                f"{path}: Resource map entry for '{PROJECT_MAP_SKELETON}' must use literal COPY"
            )
        if not RESOURCE_LOAD_CONDITION_PATTERN.search(skeleton_entry):
            errors.append(
                f"{path}: Resource map entry for '{PROJECT_MAP_SKELETON}' must include a load condition"
            )
        if not PLAN_ASSET_FIELDS_TO_FILL_PATTERN.search(skeleton_entry):
            errors.append(
                f"{path}: Resource map entry for '{PROJECT_MAP_SKELETON}' must name fields or structures to fill"
            )
        if "Do not emit unfilled placeholders" not in skeleton_entry:
            errors.append(
                f"{path}: Resource map entry for '{PROJECT_MAP_SKELETON}' must instruct agents not to emit unfilled placeholders"
            )

    skeleton_path = path.parent / PROJECT_MAP_SKELETON
    if not skeleton_path.is_file():
        errors.append(
            f"{path}: mapped project-map skeleton asset '{PROJECT_MAP_SKELETON}' must exist"
        )
        return errors

    skeleton = skeleton_path.read_text(encoding="utf-8")
    for heading in PROJECT_MAP_REQUIRED_OUTPUT_SECTIONS:
        if f"## {heading}" not in skeleton:
            errors.append(
                f"{skeleton_path}: project-map skeleton missing section '{heading}'"
            )
    for column in PROJECT_MAP_AREA_REGISTRATION_COLUMNS:
        if column not in skeleton:
            errors.append(
                f"{skeleton_path}: project-map skeleton area table missing column '{column}'"
            )
    for label, pattern in PROJECT_MAP_SKELETON_FORBIDDEN_POLICY_PATTERNS.items():
        if pattern.search(skeleton):
            errors.append(f"{skeleton_path}: project-map skeleton must not own {label}")

    return errors


def validate_project_map_canonical_contract(
    path: Path,
    metadata: dict[str, str],
    body: str,
) -> list[str]:
    """Validate canonical project-map source after M2 opt-in."""

    if metadata.get("name") != "project-map":
        return []
    if not _is_relative_to(path.resolve(), CANONICAL_SKILLS_DIR.resolve()):
        return []
    return validate_project_map_contract_fixture(
        path,
        metadata,
        body,
        diagnostic_subject="contract",
    )


def _validate_spec_family_asset_file(
    path: Path,
    relative_resource: str,
    skill_name: str,
    text: str,
) -> list[str]:
    errors: list[str] = []
    metadata = _asset_metadata(text)

    missing = sorted(SPEC_FAMILY_ASSET_REQUIRED_METADATA_FIELDS - metadata.keys())
    for field in missing:
        errors.append(f"{path}: asset metadata missing required field '{field}'")

    if missing:
        return errors

    if metadata["Skill"] != skill_name:
        errors.append(
            f"{path}: spec-family asset '{relative_resource}' must declare Skill: {skill_name}"
        )

    status = metadata["Template status"]
    if status not in SPEC_FAMILY_ASSET_TEMPLATE_STATUS_VALUES:
        allowed = ", ".join(sorted(SPEC_FAMILY_ASSET_TEMPLATE_STATUS_VALUES))
        errors.append(
            f"{path}: spec-family asset '{relative_resource}' Template status must be one of {allowed}"
        )

    maintained_alongside = metadata["Maintained alongside"]
    expected_maintained_alongside = f"skills/{skill_name}/SKILL.md"
    if maintained_alongside != expected_maintained_alongside:
        errors.append(
            f"{path}: spec-family asset '{relative_resource}' must be maintained alongside {expected_maintained_alongside}"
        )

    asset_body = _asset_body_without_metadata(text)
    if not SPEC_FAMILY_ASSET_PLACEHOLDER_PATTERN.search(asset_body):
        errors.append(
            f"{path}: asset '{relative_resource}' must include a visible placeholder"
        )

    if SPEC_FAMILY_ASSET_FILLER_PATTERN.search(asset_body):
        errors.append(
            f"{path}: asset '{relative_resource}' must not use filler placeholder text"
        )

    for line_number, line in enumerate(_iter_lines_outside_fences(text), start=1):
        if not PUBLISHED_INTERNAL_PATH_PATTERN.search(line):
            continue
        context = _required_repository_dependency_context(line)
        if context is None:
            continue
        match = PUBLISHED_INTERNAL_PATH_REFERENCE_PATTERN.search(line)
        dependency = match.group("path") if match else line.strip()
        errors.append(
            f"{path}:{line_number}: asset '{relative_resource}' must not require repository-root dependency: {dependency}"
        )

    review_policy_lines: list[str] = []
    for line in asset_body.splitlines():
        if line.lstrip().startswith("#"):
            continue
        field_label_match = SPEC_REVIEW_ASSET_ALLOWED_FIELD_LABEL_PATTERN.match(line)
        if field_label_match is not None:
            label = field_label_match.group("label")
            normalized_label = _normalized_asset_label(label)
            if SPEC_REVIEW_ASSET_FORBIDDEN_LABEL_PATTERN.search(
                line
            ) or SPEC_REVIEW_ASSET_FORBIDDEN_LABEL_PATTERN.search(normalized_label):
                review_policy_lines.append(line)
                continue
            if normalized_label in SPEC_REVIEW_ASSET_APPROVED_LABELS:
                continue
        review_policy_lines.append(line)
    review_policy_text = "\n".join(review_policy_lines)
    if skill_name == "spec-review" and SPEC_REVIEW_ASSET_FORBIDDEN_POLICY_PATTERN.search(review_policy_text):
        errors.append(
            f"{path}: spec-review asset '{relative_resource}' must not contain review-policy labels or guidance"
        )

    return errors


def _proposal_review_asset_policy_errors(
    path: Path,
    relative_resource: str,
    asset_body: str,
) -> list[str]:
    errors: list[str] = []
    review_policy_lines: list[str] = []
    for line in asset_body.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        field_label_match = SPEC_REVIEW_ASSET_ALLOWED_FIELD_LABEL_PATTERN.match(line)
        if PROPOSAL_REVIEW_ASSET_FORBIDDEN_POLICY_PATTERN.search(line):
            review_policy_lines.append(line)
            continue
        if field_label_match is not None:
            label = field_label_match.group("label")
            normalized_label = _normalized_asset_label(label)
            if PROPOSAL_REVIEW_ASSET_FORBIDDEN_LABEL_PATTERN.search(
                line
            ) or PROPOSAL_REVIEW_ASSET_FORBIDDEN_LABEL_PATTERN.search(normalized_label):
                review_policy_lines.append(line)
                continue
            if normalized_label not in PROPOSAL_REVIEW_ASSET_ALLOWED_FIELD_LABELS:
                errors.append(
                    f"{path}: proposal-review asset '{relative_resource}' field label is not in the approved "
                    f"structural-label allowlist: {label}"
                )
                continue
            continue
        review_policy_lines.append(line)

    if PROPOSAL_REVIEW_ASSET_FORBIDDEN_POLICY_PATTERN.search("\n".join(review_policy_lines)):
        errors.append(
            f"{path}: proposal-review asset '{relative_resource}' must not contain review-policy labels or guidance"
        )

    return errors


def _proposal_review_asset_baseline_errors(
    path: Path,
    relative_resource: str,
    asset_body: str,
) -> list[str]:
    errors: list[str] = []
    if relative_resource != "assets/review-result-skeleton.md":
        return errors

    if not re.search(r"(?m)^## Result$", asset_body):
        errors.append(
            f"{path}: proposal-review review-result-skeleton must include baseline heading: ## Result"
        )

    if not re.search(r"(?m)^- Skill:\s*proposal-review$", asset_body):
        errors.append(
            f"{path}: proposal-review review-result-skeleton must include baseline field: Skill"
        )

    return errors


def _review_family_should_validate(
    skill_name: str | None,
    relative_assets: set[str],
    resource_map: str | None,
) -> bool:
    if skill_name not in REVIEW_FAMILY_FIRST_SLICE_SKILLS:
        return False
    if "assets/material-finding.md" not in relative_assets:
        return False
    if skill_name in {"code-review", "spec-review"}:
        return True
    return bool(resource_map and "Finding ID:" in resource_map)


def _asset_field_labels(asset_body: str) -> list[str]:
    labels: list[str] = []
    for line in asset_body.splitlines():
        field_label_match = SPEC_REVIEW_ASSET_ALLOWED_FIELD_LABEL_PATTERN.match(line)
        if field_label_match is not None:
            labels.append(field_label_match.group("label"))
    return labels


def _review_family_material_finding_field_block(asset_body: str) -> str:
    block_lines: list[str] = []
    for line in asset_body.splitlines():
        field_label_match = SPEC_REVIEW_ASSET_ALLOWED_FIELD_LABEL_PATTERN.match(line)
        if field_label_match is None:
            continue
        label = field_label_match.group("label")
        if label in REVIEW_FAMILY_MATERIAL_FINDING_ALLOWED_LABELS:
            block_lines.append(line.strip())
    return "\n".join(block_lines)


def _validate_review_family_asset_file(
    path: Path,
    relative_resource: str,
    skill_name: str,
    text: str,
) -> list[str]:
    errors: list[str] = []
    metadata = _asset_metadata(text)

    missing = sorted(SPEC_FAMILY_ASSET_REQUIRED_METADATA_FIELDS - metadata.keys())
    for field in missing:
        errors.append(f"{path}: asset metadata missing required field '{field}'")

    if missing:
        return errors

    if metadata["Skill"] != skill_name:
        errors.append(
            f"{path}: review-family asset '{relative_resource}' must declare Skill: {skill_name}"
        )

    if metadata["Template status"] != "normative":
        errors.append(
            f"{path}: review-family asset '{relative_resource}' Template status must be normative"
        )

    maintained_alongside = metadata["Maintained alongside"]
    expected_maintained_alongside = f"skills/{skill_name}/SKILL.md"
    if maintained_alongside != expected_maintained_alongside:
        errors.append(
            f"{path}: review-family asset '{relative_resource}' must be maintained alongside {expected_maintained_alongside}"
        )

    asset_body = _asset_body_without_metadata(text)
    if not SPEC_FAMILY_ASSET_PLACEHOLDER_PATTERN.search(asset_body):
        errors.append(
            f"{path}: asset '{relative_resource}' must include a visible placeholder"
        )

    if SPEC_FAMILY_ASSET_FILLER_PATTERN.search(asset_body):
        errors.append(
            f"{path}: asset '{relative_resource}' must not use filler placeholder text"
        )

    if REVIEW_FAMILY_ASSET_FORBIDDEN_POLICY_PATTERN.search(asset_body):
        errors.append(
            f"{path}: review-family asset '{relative_resource}' must not contain review-policy labels or guidance"
        )

    if relative_resource != "assets/material-finding.md":
        return errors

    labels = _asset_field_labels(asset_body)
    for label in REVIEW_FAMILY_PARSER_FIELD_LABELS:
        if label not in labels:
            errors.append(
                f"{path}: review-family material-finding must include parser-owned label '{label}:'"
            )

    extra_labels = [
        label
        for label in labels
        if label not in REVIEW_FAMILY_MATERIAL_FINDING_ALLOWED_LABELS
    ]
    for label in extra_labels:
        errors.append(
            f"{path}: review-family material-finding label is not parser-owned: {label}"
        )

    return errors


def _validate_review_family_asset_rollout(
    path: Path,
    body: str,
    skill_name: str | None,
) -> list[str]:
    if skill_name not in REVIEW_FAMILY_FIRST_SLICE_SKILLS:
        return []

    skill_dir = path.parent
    assets = [
        asset
        for asset in sorted((skill_dir / "assets").rglob("*"))
        if asset.is_file() and asset.name != ".gitkeep"
    ] if (skill_dir / "assets").is_dir() else []
    relative_assets = {asset.relative_to(skill_dir).as_posix() for asset in assets}
    section = _extract_markdown_section(body, "Resource map")
    if not _review_family_should_validate(skill_name, relative_assets, section):
        return []

    errors: list[str] = []
    resources = _resource_files(skill_dir)
    unexpected_resource_classes = [
        resource.relative_to(skill_dir).as_posix()
        for resource in resources
        if not resource.relative_to(skill_dir).as_posix().startswith("assets/")
        and not _is_approved_packaged_non_asset_resource(
            skill_name,
            resource.relative_to(skill_dir).as_posix(),
        )
    ]
    for relative_resource in unexpected_resource_classes:
        errors.append(
            f"{path}: review-family asset rollout must not ship packaged non-asset resource '{relative_resource}'"
        )

    approved_assets = REVIEW_FAMILY_ASSET_APPROVED_ASSETS[skill_name]
    if relative_assets != approved_assets:
        expected = ", ".join(sorted(approved_assets))
        actual = ", ".join(sorted(relative_assets)) or "none"
        errors.append(
            f"{path}: review-family asset rollout must ship exactly approved assets: expected {expected}; found {actual}"
        )

    if section is None:
        return errors

    for relative_resource in sorted(relative_assets & approved_assets):
        entry = _resource_entry_text(section, relative_resource)
        if entry is None:
            continue
        expected_prefix = f"- COPY `{relative_resource}`"
        if not entry.startswith(expected_prefix):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must use literal COPY"
            )
        if not RESOURCE_LOAD_CONDITION_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must include a trigger condition"
            )
        if not PLAN_ASSET_FIELDS_TO_FILL_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must name fields or structures to fill"
            )
        if "Do not emit unfilled placeholders" not in entry:
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must instruct agents not to emit unfilled placeholders"
            )
        if (
            relative_resource == "assets/material-finding.md"
            and "Finding ID:" not in entry
        ):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must instruct agents to confirm the literal Finding ID line before linking"
            )

    for asset in assets:
        relative_resource = asset.relative_to(skill_dir).as_posix()
        if relative_resource not in approved_assets:
            continue
        text = asset.read_text(encoding="utf-8")
        errors.extend(
            _validate_review_family_asset_file(asset, relative_resource, skill_name, text)
        )

    return errors


def _validate_proposal_family_asset_file(
    path: Path,
    relative_resource: str,
    skill_name: str,
    text: str,
) -> list[str]:
    errors: list[str] = []
    metadata = _asset_metadata(text)

    missing = sorted(SPEC_FAMILY_ASSET_REQUIRED_METADATA_FIELDS - metadata.keys())
    for field in missing:
        errors.append(f"{path}: asset metadata missing required field '{field}'")

    if missing:
        return errors

    if metadata["Skill"] != skill_name:
        errors.append(
            f"{path}: proposal-family asset '{relative_resource}' must declare Skill: {skill_name}"
        )

    status = metadata["Template status"]
    if status not in SPEC_FAMILY_ASSET_TEMPLATE_STATUS_VALUES:
        allowed = ", ".join(sorted(SPEC_FAMILY_ASSET_TEMPLATE_STATUS_VALUES))
        errors.append(
            f"{path}: proposal-family asset '{relative_resource}' Template status must be one of {allowed}"
        )

    maintained_alongside = metadata["Maintained alongside"]
    expected_maintained_alongside = f"skills/{skill_name}/SKILL.md"
    if maintained_alongside != expected_maintained_alongside:
        errors.append(
            f"{path}: proposal-family asset '{relative_resource}' must be maintained alongside {expected_maintained_alongside}"
        )

    asset_body = _asset_body_without_metadata(text)
    if not SPEC_FAMILY_ASSET_PLACEHOLDER_PATTERN.search(asset_body):
        errors.append(
            f"{path}: asset '{relative_resource}' must include a visible placeholder"
        )

    if SPEC_FAMILY_ASSET_FILLER_PATTERN.search(asset_body):
        errors.append(
            f"{path}: asset '{relative_resource}' must not use filler placeholder text"
        )

    for line_number, line in enumerate(_iter_lines_outside_fences(text), start=1):
        if not PUBLISHED_INTERNAL_PATH_PATTERN.search(line):
            continue
        context = _required_repository_dependency_context(line)
        if context is None:
            continue
        match = PUBLISHED_INTERNAL_PATH_REFERENCE_PATTERN.search(line)
        dependency = match.group("path") if match else line.strip()
        errors.append(
            f"{path}:{line_number}: asset '{relative_resource}' must not require repository-root dependency: {dependency}"
        )

    if skill_name == "proposal-review":
        errors.extend(
            _proposal_review_asset_baseline_errors(
                path, relative_resource, asset_body
            )
        )
        errors.extend(
            _proposal_review_asset_policy_errors(path, relative_resource, asset_body)
        )

    return errors


def mapped_asset_paths_for_skill(skill_dir: Path) -> list[str]:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return []

    try:
        metadata, body = load_skill_file(skill_file)
    except ValueError:
        return []

    skill_name = metadata.get("name")
    if not isinstance(skill_name, str) or skill_name not in ASSET_ROLLOUT_APPROVED_ASSETS:
        return []

    section = _extract_markdown_section(body, "Resource map")
    if section is None:
        return []

    mapped_assets: list[str] = []
    for relative_resource in sorted(ASSET_ROLLOUT_APPROVED_ASSETS[skill_name]):
        entry = _resource_entry_text(section, relative_resource)
        if entry is not None and entry.startswith(f"- COPY `{relative_resource}`"):
            mapped_assets.append(relative_resource)
    return mapped_assets


def validate_generated_asset_presence(
    *,
    skill_name: str,
    canonical_skill_dir: Path,
    generated_skill_dir: Path,
    surface_label: str,
) -> list[str]:
    """Return stable validation errors for mapped assets missing from generated output."""
    errors: list[str] = []

    for relative_resource in mapped_asset_paths_for_skill(canonical_skill_dir):
        canonical_path = canonical_skill_dir / relative_resource
        generated_path = generated_skill_dir / relative_resource

        if not canonical_path.is_file():
            errors.append(
                f"Canonical skill '{skill_name}' maps missing asset '{relative_resource}'"
            )
            continue

        if not generated_path.is_file():
            errors.append(
                f"Generated output for skill '{skill_name}' is missing mapped asset "
                f"'{relative_resource}' in {surface_label}"
            )

    return errors


def _validate_spec_family_asset_rollout(
    path: Path,
    body: str,
    skill_name: str | None,
) -> list[str]:
    if skill_name not in SPEC_FAMILY_ASSET_APPROVED_ASSETS:
        return []

    skill_dir = path.parent
    resources = _resource_files(skill_dir)
    if not resources:
        return []

    errors: list[str] = []
    unexpected_resource_classes = [
        resource.relative_to(skill_dir).as_posix()
        for resource in resources
        if not resource.relative_to(skill_dir).as_posix().startswith("assets/")
        and not _is_approved_packaged_non_asset_resource(
            skill_name,
            resource.relative_to(skill_dir).as_posix(),
        )
    ]
    for relative_resource in unexpected_resource_classes:
        errors.append(
            f"{path}: spec-family asset rollout must not ship packaged non-asset resource '{relative_resource}'"
        )

    assets = [
        asset
        for asset in sorted((skill_dir / "assets").rglob("*"))
        if asset.is_file() and asset.name != ".gitkeep"
    ] if (skill_dir / "assets").is_dir() else []
    relative_assets = {asset.relative_to(skill_dir).as_posix() for asset in assets}
    approved_assets = SPEC_FAMILY_ASSET_APPROVED_ASSETS[skill_name]
    if relative_assets != approved_assets:
        expected = ", ".join(sorted(approved_assets))
        actual = ", ".join(sorted(relative_assets)) or "none"
        errors.append(
            f"{path}: spec-family asset rollout must ship exactly approved assets: expected {expected}; found {actual}"
        )

    section = _extract_markdown_section(body, "Resource map")
    if section is None:
        return errors

    for relative_resource in sorted(relative_assets & approved_assets):
        entry = _resource_entry_text(section, relative_resource)
        if entry is None:
            continue
        expected_prefix = f"- COPY `{relative_resource}`"
        if not entry.startswith(expected_prefix):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must use literal COPY"
            )
        if not RESOURCE_LOAD_CONDITION_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must include a trigger condition"
            )
        if not PLAN_ASSET_FIELDS_TO_FILL_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must name fields or structures to fill"
            )
        if "Do not emit unfilled placeholders" not in entry:
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must instruct agents not to emit unfilled placeholders"
            )

    for asset in assets:
        relative_resource = asset.relative_to(skill_dir).as_posix()
        if relative_resource not in approved_assets:
            continue
        text = asset.read_text(encoding="utf-8")
        errors.extend(
            _validate_spec_family_asset_file(asset, relative_resource, skill_name, text)
        )

    return errors


def _validate_proposal_family_asset_rollout(
    path: Path,
    body: str,
    skill_name: str | None,
) -> list[str]:
    if skill_name not in PROPOSAL_FAMILY_ASSET_APPROVED_ASSETS:
        return []

    skill_dir = path.parent
    resources = _resource_files(skill_dir)
    if not resources:
        return []

    errors: list[str] = []
    unexpected_resource_classes = [
        resource.relative_to(skill_dir).as_posix()
        for resource in resources
        if not resource.relative_to(skill_dir).as_posix().startswith("assets/")
        and not _is_approved_packaged_non_asset_resource(
            skill_name, resource.relative_to(skill_dir).as_posix()
        )
    ]
    for relative_resource in unexpected_resource_classes:
        errors.append(
            f"{path}: proposal-family asset rollout must not ship packaged non-asset resource '{relative_resource}'"
        )

    assets = [
        asset
        for asset in sorted((skill_dir / "assets").rglob("*"))
        if asset.is_file() and asset.name != ".gitkeep"
    ] if (skill_dir / "assets").is_dir() else []
    relative_assets = {asset.relative_to(skill_dir).as_posix() for asset in assets}
    approved_assets = PROPOSAL_FAMILY_ASSET_APPROVED_ASSETS[skill_name]
    if relative_assets != approved_assets:
        expected = ", ".join(sorted(approved_assets))
        actual = ", ".join(sorted(relative_assets)) or "none"
        errors.append(
            f"{path}: proposal-family asset rollout must ship exactly approved assets: expected {expected}; found {actual}"
        )

    section = _extract_markdown_section(body, "Resource map")
    if section is None:
        return errors

    for relative_resource in sorted(relative_assets & approved_assets):
        entry = _resource_entry_text(section, relative_resource)
        if entry is None:
            continue
        expected_prefix = f"- COPY `{relative_resource}`"
        if not entry.startswith(expected_prefix):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must use literal COPY"
            )
        if not RESOURCE_LOAD_CONDITION_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must include a trigger condition"
            )
        if not PLAN_ASSET_FIELDS_TO_FILL_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must name fields or structures to fill"
            )
        if "Do not emit unfilled placeholders" not in entry:
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must instruct agents not to emit unfilled placeholders"
            )

    for asset in assets:
        relative_resource = asset.relative_to(skill_dir).as_posix()
        if relative_resource not in approved_assets:
            continue
        text = asset.read_text(encoding="utf-8")
        errors.extend(
            _validate_proposal_family_asset_file(asset, relative_resource, skill_name, text)
        )

    return errors


def _references_packaged_resource(line: str, skill_dir: Path) -> bool:
    for resource in _resource_files(skill_dir):
        relative_resource = resource.relative_to(skill_dir).as_posix()
        if relative_resource in line:
            return True
    return False


def _required_repository_dependency_context(line: str) -> str | None:
    if PUBLISHED_NON_REQUIRED_CONTEXT_PATTERN.search(line):
        return None
    if READABILITY_REQUIRED_CONTEXT_PATTERN.search(line):
        return "required context"
    if PUBLISHED_REQUIRED_COMMAND_CONTEXT_PATTERN.search(line):
        return "command wording"
    return None


def _validate_readability_workflow_role(
    path: Path,
    metadata: dict[str, str],
    body: str,
) -> list[str]:
    section = _extract_markdown_section(body, "Workflow role")
    if section is None:
        return [f"{path}: missing required '## Workflow role' section"]

    errors: list[str] = []
    fields = _parse_colon_fields(section)
    missing_fields = sorted(READABILITY_REQUIRED_ROLE_FIELDS - fields.keys())
    for field in missing_fields:
        errors.append(f"{path}: Workflow role missing required field '{field}'")

    role_name = fields.get("role_name")
    expected_name = metadata.get("name")
    if role_name and expected_name and role_name != expected_name:
        errors.append(
            f"{path}: workflow role role_name must match skill name '{expected_name}'"
        )

    stage = fields.get("stage")
    if stage and stage not in READABILITY_STAGE_VALUES:
        allowed = ", ".join(sorted(READABILITY_STAGE_VALUES))
        errors.append(f"{path}: workflow role stage must be one of {allowed}")

    summary = fields.get("summary")
    if summary is not None and summary.count("\n") >= 2:
        errors.append(f"{path}: workflow role summary must be no more than two lines")

    return errors


def _validate_readability_output_skeleton(path: Path, body: str) -> list[str]:
    section = _extract_markdown_section(body, "Output skeleton")
    if section is None:
        return [f"{path}: missing required '## Output skeleton' section"]
    errors: list[str] = []
    if not _contains_fenced_block(section):
        errors.append(f"{path}: Output skeleton must include a fenced block")
    if "<" not in section or ">" not in section:
        errors.append(f"{path}: Output skeleton must include fillable placeholders")
    return errors


def _validate_readability_internal_references(path: Path, body: str) -> list[str]:
    errors: list[str] = []
    for line_number, line in enumerate(_iter_lines_outside_fences(body), start=1):
        if not READABILITY_INTERNAL_PATH_PATTERN.search(line):
            continue
        if not READABILITY_REQUIRED_CONTEXT_PATTERN.search(line):
            continue
        normalized = line.lower()
        if any(term.lower() in normalized for term in READABILITY_ALLOWED_PROJECT_LOCAL_TERMS):
            continue
        errors.append(
            f"{path}:{line_number}: required unavailable internal reference: {line.strip()}"
        )
    return errors


def _validate_published_description(path: Path, metadata: dict[str, str]) -> list[str]:
    errors: list[str] = []
    description = metadata.get("description")
    if isinstance(description, str) and len(description) > DESCRIPTION_MAX_CHARS:
        errors.append(
            f"{path}: description must be {DESCRIPTION_MAX_CHARS} characters or fewer"
        )

    when_to_use = metadata.get("when_to_use")
    if isinstance(when_to_use, str) and when_to_use.strip():
        description_text = description or ""
        if len(description_text.strip()) < 20 or not ROUTING_HINT_PATTERN.search(description_text):
            errors.append(
                f"{path}: when_to_use must not replace description as the routing source"
            )
    return errors


def _validate_resource_map(path: Path, body: str) -> list[str]:
    resources = _resource_files(path.parent)
    section = _extract_markdown_section(body, "Resource map")
    if section is None and resources:
        return [f"{path}: packaged resources require a '## Resource map' section"]
    if section is None:
        section = ""

    errors: list[str] = []
    entries = _resource_map_entries(section)
    mapped_resources = {resource_path for _, resource_path, _ in entries}

    for verb, resource_path, _entry in entries:
        containment_error = _mapped_resource_containment_error(resource_path, path.parent)
        if containment_error:
            errors.append(f"{path}: {containment_error}")
            continue

        required_prefix = RESOURCE_MAP_VERB_CLASSES[verb]
        if not resource_path.startswith(required_prefix):
            errors.append(
                f"{path}: Resource map entry '{verb} {resource_path}' must point to {required_prefix}"
            )
            continue

        resource_file = path.parent / resource_path
        if not resource_file.is_file():
            errors.append(
                f"{path}: mapped resource '{resource_path}' does not exist in canonical skill source"
            )

    for resource in resources:
        relative_resource = resource.relative_to(path.parent).as_posix()
        entry = _resource_entry_text(section, relative_resource)
        if entry is None:
            errors.append(
                f"{path}: Resource map must name packaged resource '{relative_resource}'"
            )
            continue
        if not RESOURCE_LOAD_CONDITION_PATTERN.search(entry):
            errors.append(
                f"{path}: Resource map entry for '{relative_resource}' must include a load condition"
            )
        if relative_resource.startswith("scripts/"):
            if not SCRIPT_INPUT_PATTERN.search(entry):
                errors.append(
                    f"{path}: packaged script '{relative_resource}' map entry must describe input"
                )
            if not SCRIPT_OUTPUT_PATTERN.search(entry):
                errors.append(
                    f"{path}: packaged script '{relative_resource}' map entry must describe output or exit code"
                )
            if not SCRIPT_FAILURE_PATTERN.search(entry):
                errors.append(
                    f"{path}: packaged script '{relative_resource}' map entry must describe failure behavior"
                )
    for line_number, resource_path, line in _iter_unmapped_skill_local_resource_references(
        path,
        body,
        mapped_resources,
    ):
        skill_name = _skill_name_for_path(path)
        errors.append(
            f"{path}:{line_number}: {skill_name}: unmapped skill-local resource "
            f"reference `{resource_path}`; declare it in `## Resource map`, migrate "
            f"it to an approved resource class, or remove the instruction: {line}"
        )
    return errors


def _validate_ci_maintenance_skeleton(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    required_terms = {
        "authorized trigger placeholder": ("<explicitly authorized trigger>",),
        "least-privilege permissions": ("permissions:\n  contents: read",),
        "concurrency": ("concurrency:", "cancel-in-progress: true"),
        "ordinary job": ("<ordinary job id>", "<ordinary job name>"),
        "job timeout placeholder": ("timeout-minutes: <bounded timeout>",),
        "action-reference placeholder": ("<project-approved reference>",),
        "validation command placeholder": ("<authoritative project command>",),
    }
    for label, terms in required_terms.items():
        if not all(term in text for term in terms):
            errors.append(f"{path}: workflow skeleton must include {label}")

    if re.search(r"@[0-9a-fA-F]{40}\b", text):
        errors.append(f"{path}: workflow skeleton must not include invented real action SHAs")
    for forbidden in ("pull_request:", "push:", "schedule:", "workflow_dispatch:", "pull_request_target", "secrets:", "id-token:"):
        if forbidden in text:
            errors.append(f"{path}: workflow skeleton must not include privileged or boundary example '{forbidden}'")
    return errors


def _validate_ci_maintenance_risk_map(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    required_terms = {
        "portable core": ("## Portable core", "workflow files", "source code"),
        "project-specific extensions": ("## Project-specific extensions", "Example only"),
        "changed-surface table": ("Changed surface", "PR check", "Boundary check"),
        "unmapped-surface fail-safe": (
            "Unmapped changed surfaces",
            "reviewer judgment",
            "conservative boundary check",
        ),
        "bounded risk claim": ("not no-risk surfaces",),
    }
    for label, terms in required_terms.items():
        if not all(term in text for term in terms):
            errors.append(f"{path}: risk map must include {label}")
    if "non-RigorLoop projects do not need this" not in text:
        errors.append(f"{path}: risk map must label RigorLoop rows as project-specific examples")
    return errors


def validate_ci_maintenance_contract(
    path: Path,
    metadata: dict[str, str],
    body: str,
) -> list[str]:
    is_ci_maintenance_path = path.parent.name == CI_MAINTENANCE_SKILL_NAME
    is_ci_maintenance_name = metadata.get("name") == CI_MAINTENANCE_SKILL_NAME
    if not is_ci_maintenance_path and not is_ci_maintenance_name:
        return []

    errors: list[str] = []
    if metadata.get("name") != CI_MAINTENANCE_SKILL_NAME:
        errors.append(f"{path}: ci-maintenance frontmatter must use name: ci-maintenance")
    non_codex_adapter_path = any(part in {".claude", ".opencode"} for part in path.parts)
    if not non_codex_adapter_path:
        if not metadata.get("version"):
            errors.append(f"{path}: ci-maintenance frontmatter must include version")
        if metadata.get("schema-version") != READABILITY_SCHEMA_VERSION:
            errors.append(f"{path}: ci-maintenance frontmatter must include schema-version")

    stale_identifier_patterns = (
        r"(?m)^\s*-\s*role_name:\s*ci\s*$",
        r"\bwhen ci is run\b",
        r"\bwhen `ci` is run\b",
        r"\bci-mantance\b",
    )
    for pattern in stale_identifier_patterns:
        if re.search(pattern, body):
            errors.append(f"{path}: stale ci-maintenance identifier reference")
            break

    if re.search(r"\bnarrower(?:\s+job-specific)?\s+elevation\b", body, re.IGNORECASE):
        errors.append(f"{path}: permissions wording must not say narrower elevation")

    resource_map = _extract_markdown_section(body, "Resource map")
    if resource_map is None:
        errors.append(f"{path}: ci-maintenance requires a Resource map")
    else:
        skeleton_entry = _resource_entry_text(resource_map, CI_MAINTENANCE_SKELETON)
        if skeleton_entry is None:
            errors.append(
                f"{path}: Resource map must name packaged resource '{CI_MAINTENANCE_SKELETON}'"
            )
        elif not skeleton_entry.startswith(f"- COPY `{CI_MAINTENANCE_SKELETON}`"):
            errors.append(
                f"{path}: Resource map entry for '{CI_MAINTENANCE_SKELETON}' must use literal COPY"
            )

        risk_entry = _resource_entry_text(resource_map, CI_MAINTENANCE_RISK_MAP)
        if risk_entry is None:
            errors.append(
                f"{path}: Resource map must name packaged resource '{CI_MAINTENANCE_RISK_MAP}'"
            )
        elif not risk_entry.startswith(f"- READ `{CI_MAINTENANCE_RISK_MAP}`"):
            errors.append(
                f"{path}: Resource map entry for '{CI_MAINTENANCE_RISK_MAP}' must use literal READ"
            )
        authoring_entry = _resource_entry_text(resource_map, CI_MAINTENANCE_AUTHORING_REFERENCE)
        if authoring_entry is None:
            errors.append(f"{path}: Resource map must name packaged resource '{CI_MAINTENANCE_AUTHORING_REFERENCE}'")
        elif not authoring_entry.startswith(f"- READ `{CI_MAINTENANCE_AUTHORING_REFERENCE}`"):
            errors.append(f"{path}: Resource map entry for '{CI_MAINTENANCE_AUTHORING_REFERENCE}' must use literal READ")

    skeleton_path = path.parent / CI_MAINTENANCE_SKELETON
    if skeleton_path.is_file():
        errors.extend(
            _validate_ci_maintenance_skeleton(
                skeleton_path,
                skeleton_path.read_text(encoding="utf-8"),
            )
        )
    else:
        errors.append(f"{path}: missing ci-maintenance workflow skeleton asset")

    risk_map_path = path.parent / CI_MAINTENANCE_RISK_MAP
    if risk_map_path.is_file():
        errors.extend(
            _validate_ci_maintenance_risk_map(
                risk_map_path,
                risk_map_path.read_text(encoding="utf-8"),
            )
        )
    else:
        errors.append(f"{path}: missing ci-maintenance risk-to-check reference")

    required_body_terms = {
        "known command blocker": ("report a blocker instead of guessing",),
        "allowed command sources": ("Allowed command sources", "explicit user-provided commands"),
        "overbroad permissions during workflow review": ("overbroad permissions",),
        "unsafe path filters during workflow review": (
            "path filters that skip required checks",
        ),
        "slow PR checks during workflow review": ("slow comprehensive checks on every PR",),
        "pull_request_target warning": ("pull_request_target", "untrusted code"),
        "risk coverage review": ("missing risk coverage", "unmapped changed surfaces"),
        "bounded PR repair eligibility": (
            "Use `bounded-pr-ci-repair` only for an already-open PR with an exact failing run and head",
            "current review and verification evidence",
            "no open material finding",
        ),
        "bounded PR repair decision boundary": (
            "runtime implementation",
            "dependencies",
            "lifecycle schema",
            "stage routing",
            "earliest affected owning stage",
        ),
        "bounded PR repair lifecycle restraint": (
            "Do not create a new review round",
            "lifecycle-only commit solely because CI failed",
        ),
        "bounded PR repair hosted observation": (
            "`not-observed`, `pending`, `passed`, or `failed`",
            "exact run and head",
        ),
    }
    for label, terms in required_body_terms.items():
        if not all(term in body for term in terms):
            errors.append(f"{path}: ci-maintenance must flag {label}")

    if "Do not invent validation commands" not in body:
        errors.append(f"{path}: ci-maintenance must forbid invented validation commands")
    if "Add broader job-specific permissions only when a known workflow need requires them" not in body:
        errors.append(f"{path}: ci-maintenance must require rationale for broader permissions")
    if "Use dependency caches only when a stable invalidation key exists" not in body:
        errors.append(f"{path}: ci-maintenance must require stable cache invalidation keys")
    return errors


def _validate_published_self_containment(path: Path, metadata: dict[str, str], body: str) -> list[str]:
    if metadata.get("schema-version") != READABILITY_SCHEMA_VERSION:
        return []

    errors: list[str] = []
    for line_number, line in enumerate(_iter_lines_outside_fences(body), start=1):
        if not PUBLISHED_INTERNAL_PATH_PATTERN.search(line):
            continue
        context = _required_repository_dependency_context(line)
        if context is None:
            continue
        if _references_packaged_resource(line, path.parent):
            continue
        normalized = line.lower()
        if any(term.lower() in normalized for term in PUBLISHED_ALLOWED_PROJECT_LOCAL_TERMS):
            continue
        match = PUBLISHED_INTERNAL_PATH_REFERENCE_PATTERN.search(line)
        dependency = match.group("path") if match else line.strip()
        errors.append(
            f"{path}:{line_number}: required repository-root dependency by {context}: {dependency}"
        )
    return errors


def _validate_readability_closed_enums(path: Path, body: str) -> list[str]:
    errors: list[str] = []
    enum_names: dict[str, int] = {}
    lines = body.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^\s*Closed enum:\s*(?P<name>.+?)\s*$", line, re.IGNORECASE)
        if not match:
            continue
        name = match.group("name").strip().lower()
        if name in enum_names:
            errors.append(
                f"{path}:{index + 1}: duplicate closed enum block '{name}'"
            )
            continue
        enum_names[name] = index + 1

        following_lines: list[str] = []
        for following in lines[index + 1 :]:
            if re.match(r"^\s*Closed enum:\s*", following, re.IGNORECASE):
                break
            if following.startswith("## "):
                break
            following_lines.append(following)
        block = "\n".join(following_lines)
        has_fence = _contains_fenced_block(block)
        has_table = any(line.strip().startswith("|") for line in following_lines)
        if not has_fence and not has_table:
            errors.append(
                f"{path}:{index + 1}: closed enum '{name}' must use a fenced block or table"
            )
    return errors


def validate_readability_contract(
    path: Path,
    metadata: dict[str, str],
    body: str,
) -> list[str]:
    schema_version = metadata.get("schema-version")
    if schema_version is None:
        return []

    errors: list[str] = []
    if schema_version != READABILITY_SCHEMA_VERSION:
        errors.append(
            f"{path}: schema-version must be '{READABILITY_SCHEMA_VERSION}'"
        )
        return errors
    if not metadata.get("version"):
        errors.append(f"{path}: version: missing required readability contract field")

    errors.extend(_validate_readability_workflow_role(path, metadata, body))
    errors.extend(_validate_readability_output_skeleton(path, body))
    errors.extend(_validate_readability_internal_references(path, body))
    errors.extend(_validate_readability_closed_enums(path, body))
    return errors


def _has_ancestor_skill_dir(directory: Path, target: Path) -> bool:
    current = directory.parent
    while True:
        if (current / "SKILL.md").is_file():
            return True
        if current == target:
            return False
        if current == current.parent:
            return False
        current = current.parent


def discover_source_skill_dirs(target: Path) -> list[Path]:
    if target.is_file():
        if target.name != "SKILL.md":
            return []
        return [target.parent]

    directories = [target]
    directories.extend(path for path in sorted(target.rglob("*")) if path.is_dir())

    candidates: list[Path] = []
    for directory in directories:
        if directory != target and _has_ancestor_skill_dir(directory, target):
            continue
        has_skill_file = (directory / "SKILL.md").is_file()
        has_child_directories = any(child.is_dir() for child in directory.iterdir())
        if has_skill_file or not has_child_directories:
            candidates.append(directory)

    return candidates


def validate_metadata_against_schema(metadata: dict[str, str], schema: dict, path: Path) -> list[str]:
    errors: list[str] = []

    if schema.get("type") != "object":
        return [f"{path}: skill schema must define an object root"]

    for key in schema.get("required", []):
        if key not in metadata:
            errors.append(f"{path}: {key}: missing required field")

    properties = schema.get("properties", {})
    for key, property_schema in properties.items():
        if key not in metadata:
            continue
        value = metadata[key]
        if property_schema.get("type") == "string" and not isinstance(value, str):
            errors.append(f"{path}: {key}: expected string")
            continue
        min_length = property_schema.get("minLength")
        if isinstance(min_length, int) and len(value.strip()) < min_length:
            errors.append(f"{path}: {key}: must be at least {min_length} characters")

    return errors


def validate_skill_file(path: Path, schema: dict) -> tuple[list[str], str | None]:
    errors: list[str] = []
    full_text = path.read_text(encoding="utf-8")

    try:
        metadata, body = load_skill_file(path)
    except ValueError as exc:
        return [str(exc)], None

    errors.extend(validate_metadata_against_schema(metadata, schema, path))

    title_count = sum(1 for line in _iter_lines_outside_fences(body) if line.startswith("# "))
    if title_count != 1:
        errors.append(f"{path}: expected exactly one top-level # title, found {title_count}")

    if "## Expected output" not in body.splitlines():
        errors.append(f"{path}: missing required '## Expected output' section")

    if PLACEHOLDER_PATTERN.search(full_text):
        errors.append(f"{path}: placeholder text is not allowed")

    name = metadata.get("name")
    skill_name = name.strip() if isinstance(name, str) and name.strip() else None
    if isinstance(name, str) and not name.strip():
        errors.append(f"{path}: name: must be at least 1 characters")

    description = metadata.get("description")
    if isinstance(description, str) and not description.strip():
        errors.append(f"{path}: description: must be at least 1 characters")

    errors.extend(_validate_published_description(path, metadata))
    errors.extend(_validate_resource_map(path, body))
    errors.extend(validate_ci_maintenance_contract(path, metadata, body))
    errors.extend(_validate_published_self_containment(path, metadata, body))
    errors.extend(validate_readability_contract(path, metadata, body))
    errors.extend(
        _validate_plan_asset_pilot(
            path,
            body,
            name.strip() if isinstance(name, str) else None,
        )
    )
    errors.extend(
        _validate_spec_family_asset_rollout(
            path,
            body,
            name.strip() if isinstance(name, str) else None,
        )
    )
    errors.extend(
        _validate_proposal_family_asset_rollout(
            path,
            body,
            name.strip() if isinstance(name, str) else None,
        )
    )
    errors.extend(
        _validate_review_family_asset_rollout(
            path,
            body,
            name.strip() if isinstance(name, str) else None,
        )
    )
    errors.extend(validate_project_map_canonical_contract(path, metadata, body))
    if skill_name and _is_relative_to(path.resolve(), CANONICAL_SKILLS_DIR.resolve()):
        errors.extend(validate_requirement_delivery_model_copy(path, skill_name))
        if skill_name in DISCOVERY_SUPPORT_CONSUMERS:
            errors.extend(
                validate_discovery_support_copy(
                    path.parent / DISCOVERY_SUPPORT_TARGET,
                    skill_name,
                )
            )
        errors.extend(
            validate_installed_skill_artifact_placement_contract(
                path,
                skill_name,
                body,
            )
        )
        if skill_name == "plan":
            errors.extend(
                validate_installed_skill_plan_surface_contract(
                    path,
                    skill_name,
                    body,
                )
            )
        if skill_name == "spec-review":
            errors.extend(validate_spec_review_canonical_contract(path))
    return errors, skill_name


def validate_skill_tree(target: Path, *, allow_generated: bool = False) -> ValidationResult:
    resolved_target = target.resolve()
    resolved_generated = GENERATED_SKILLS_DIR.resolve()
    if not allow_generated and _is_relative_to(resolved_target, resolved_generated):
        return ValidationResult(
            checked_files=[],
            errors=[
                f"{target}: generated output path must not be used as authored source of truth"
            ],
        )
    if not target.exists():
        return ValidationResult(
            checked_files=[], errors=[f"{target}: target does not exist"]
        )

    skill_dirs = discover_source_skill_dirs(target)
    if not skill_dirs:
        return ValidationResult(checked_files=[], errors=[f"{target}: no SKILL.md files found"])

    schema = load_skill_schema()
    errors: list[str] = []
    owners: dict[str, Path] = {}
    checked_files: list[Path] = []
    review_family_material_blocks: dict[str, str] = {}

    for directory in skill_dirs:
        path = directory if directory.is_file() else directory / "SKILL.md"
        if not path.is_file():
            errors.append(f"{path}: missing required skill file")
            continue
        checked_files.append(path)
        try:
            file_errors, name = validate_skill_file(path, schema)
        except ProjectionContractError as exc:
            try:
                diagnostic_path = path.resolve().relative_to(
                    ROOT.resolve()
                ).as_posix()
            except ValueError:
                diagnostic_path = "<external-skill>"
            file_errors = [
                f"{diagnostic_path}: boundary resource contract invalid: "
                f"{format_contract_error(exc)}"
            ]
            name = None
        errors.extend(file_errors)
        if (
            name in REVIEW_FAMILY_FIRST_SLICE_SKILLS
            and (path.parent / "assets" / "material-finding.md").is_file()
        ):
            material_finding_text = (path.parent / "assets" / "material-finding.md").read_text(
                encoding="utf-8"
            )
            material_finding_body = _asset_body_without_metadata(material_finding_text)
            review_family_material_blocks[name] = (
                _review_family_material_finding_field_block(material_finding_body)
            )
        if not name:
            continue
        if name in owners:
            errors.append(f"duplicate skill name: {name} in {owners[name]} and {path}")
            continue
        owners[name] = path

    if len(review_family_material_blocks) > 1:
        unique_blocks = set(review_family_material_blocks.values())
        if len(unique_blocks) > 1:
            skills = ", ".join(sorted(review_family_material_blocks))
            errors.append(
                "review-family material-finding parser-owned field block must be byte-identical "
                f"across first-slice review skills: {skills}"
            )

    canonical_root = CANONICAL_SKILLS_DIR.resolve()
    if (
        resolved_target == canonical_root
        or _is_relative_to(resolved_target, canonical_root)
    ) and "ci" in owners:
        errors.append("stale active ci skill body is not allowed after ci-maintenance hard rename")

    return ValidationResult(checked_files=checked_files, errors=errors)
