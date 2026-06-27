#!/usr/bin/env python3
"""Validation selector domain model and path classification."""

from __future__ import annotations

import json
import fnmatch
import re
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any


DEFAULT_ADAPTER_VERSION = "0.1.1"
STATUSES = frozenset({"ok", "blocked", "fallback", "error"})
EXIT_CODES = {"ok": 0, "blocked": 2, "fallback": 3, "error": 4}
ROOT_VISION_PATH = "VISION.md"
REQUIRED_EVIDENCE_DEFERRAL_FIELDS = frozenset(
    {"owner", "path", "reason", "validation_impact", "follow_up"}
)


@dataclass(frozen=True)
class CheckCatalogEntry:
    id: str
    command_template: str
    category: str
    parallel_safe: bool = False


CHECK_CATALOG: dict[str, CheckCatalogEntry] = {
    "skills.validate": CheckCatalogEntry(
        "skills.validate",
        "python scripts/validate-skills.py",
        "skills",
    ),
    "skills.regression": CheckCatalogEntry(
        "skills.regression",
        "python scripts/test-skill-validator.py",
        "skills",
        parallel_safe=True,
    ),
    "skills.generation_regression": CheckCatalogEntry(
        "skills.generation_regression",
        "python scripts/test-build-skills.py",
        "skills",
        parallel_safe=True,
    ),
    "skills.drift": CheckCatalogEntry(
        "skills.drift",
        "python scripts/build-skills.py --check",
        "skills",
    ),
    "adapters.regression": CheckCatalogEntry(
        "adapters.regression",
        "python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_generation_creates_independent_packages_and_thin_entrypoints AdapterDistributionTests.test_adapter_generation_drift_check_detects_stale_and_unexpected_files AdapterDistributionTests.test_validate_adapters_cli_rejects_retired_repository_output AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata",
        "adapters",
        parallel_safe=True,
    ),
    "adapters.drift": CheckCatalogEntry(
        "adapters.drift",
        "python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives",
        "adapters",
    ),
    "adapters.validate": CheckCatalogEntry(
        "adapters.validate",
        "python scripts/test-adapter-distribution.py AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root",
        "adapters",
    ),
    "review_artifacts.regression": CheckCatalogEntry(
        "review_artifacts.regression",
        "python scripts/test-review-artifact-validator.py",
        "review-artifacts",
        parallel_safe=True,
    ),
    "review_artifacts.validate": CheckCatalogEntry(
        "review_artifacts.validate",
        "python scripts/validate-review-artifacts.py <change-root>...",
        "review-artifacts",
    ),
    "artifact_lifecycle.regression": CheckCatalogEntry(
        "artifact_lifecycle.regression",
        "python scripts/test-artifact-lifecycle-validator.py",
        "lifecycle",
        parallel_safe=True,
    ),
    "artifact_lifecycle.validate": CheckCatalogEntry(
        "artifact_lifecycle.validate",
        "python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <path>...",
        "lifecycle",
    ),
    "validation_cache.regression": CheckCatalogEntry(
        "validation_cache.regression",
        "python scripts/test-validation-cache.py",
        "validation-cache",
        parallel_safe=True,
    ),
    "change_metadata.regression": CheckCatalogEntry(
        "change_metadata.regression",
        "python scripts/test-change-metadata-validator.py",
        "change-metadata",
        parallel_safe=True,
    ),
    "change_metadata.validate": CheckCatalogEntry(
        "change_metadata.validate",
        "python scripts/validate-change-metadata.py <change-yaml>...",
        "change-metadata",
    ),
    "change_record_query.regression": CheckCatalogEntry(
        "change_record_query.regression",
        "python scripts/test-query-change-record.py",
        "change-record-query",
        parallel_safe=True,
    ),
    "release.validate": CheckCatalogEntry(
        "release.validate",
        "python scripts/validate-release-ci.py --version <version>",
        "release",
    ),
    "readme.validate": CheckCatalogEntry(
        "readme.validate",
        "python scripts/validate-readme.py README.md",
        "readme",
    ),
    "readme.vision_markers": CheckCatalogEntry(
        "readme.vision_markers",
        "python scripts/validate-readme.py README.md --vision-markers",
        "readme",
    ),
    "guide_system.regression": CheckCatalogEntry(
        "guide_system.regression",
        "python scripts/test-guide-system-validator.py",
        "guide-system",
        parallel_safe=True,
    ),
    "guide_system.validate": CheckCatalogEntry(
        "guide_system.validate",
        "python scripts/validate-guide-system.py",
        "guide-system",
    ),
    "selector.regression": CheckCatalogEntry(
        "selector.regression",
        "python scripts/test-select-validation.py",
        "selector",
        parallel_safe=True,
    ),
    "requirement_fidelity.spec_reads": CheckCatalogEntry(
        "requirement_fidelity.spec_reads",
        "python scripts/test-fidelity-gate-spec-reads.py --review-set tests/fixtures/requirement-fidelity-gate/representative-reviews --max-bytes-per-clause 4096 --assert-no-broad-reads",
        "requirement-fidelity",
        parallel_safe=True,
    ),
    "token_cost.regression": CheckCatalogEntry(
        "token_cost.regression",
        "python scripts/test-token-cost-measurement.py",
        "token-cost",
        parallel_safe=True,
    ),
    "token_cost.report_regression": CheckCatalogEntry(
        "token_cost.report_regression",
        "python scripts/test-token-cost-report-validation.py",
        "token-cost",
        parallel_safe=True,
    ),
    "token_cost.report_validate": CheckCatalogEntry(
        "token_cost.report_validate",
        "python scripts/validate-token-cost-report.py <report-yaml>...",
        "token-cost",
    ),
    "broad_smoke.repo": CheckCatalogEntry(
        "broad_smoke.repo",
        "bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped",
        "broad-smoke",
    ),
    "rigorloop_cli.test": CheckCatalogEntry(
        "rigorloop_cli.test",
        "npm test --prefix packages/rigorloop",
        "rigorloop-cli",
    ),
    "npm_package_publication.test": CheckCatalogEntry(
        "npm_package_publication.test",
        "python scripts/test-npm-package-publication.py",
        "rigorloop-cli",
    ),
}

BOUNDARY_CHECK_IDS = frozenset(
    {
        "broad_smoke.repo",
        "release.validate",
        "adapters.drift",
        "adapters.validate",
    }
)
AUTHORITATIVE_ARTIFACT_PREFIXES = (
    "docs/proposals/",
    "docs/plans/",
    "docs/architecture/",
    "docs/adr/",
    "specs/",
    "skills/",
    "schemas/",
    "scripts/",
    "templates/",
)
AUTHORITATIVE_ARTIFACT_FILES = frozenset({"AGENTS.md", "CONSTITUTION.md", "VISION.md", "docs/plan.md", "docs/workflows.md"})


@dataclass(frozen=True)
class EvidenceClassRegistration:
    evidence_class_id: str
    patterns: tuple[str, ...]
    selector_routes: tuple[str, ...]
    required_validator: str
    lifecycle_stage: str
    allowed_root: str = "docs/changes/{change_id}/"
    allowed_when: tuple[str, ...] = ()
    required_when: tuple[str, ...] = ()
    forbidden_when: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvidenceDeferralStatus:
    status: str
    missing_fields: tuple[str, ...] = ()
    invalid_fields: tuple[str, ...] = ()
    deferral: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RepositoryPreflightContext:
    tracked_paths: frozenset[str]
    unmerged_paths: tuple[str, ...]


EVIDENCE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
BROAD_EVIDENCE_PATTERNS = frozenset({"*.md", "*.txt", "*.yaml", "*.yml"})

CHANGE_EVIDENCE_CLASSES: tuple[EvidenceClassRegistration, ...] = (
    EvidenceClassRegistration(
        evidence_class_id="audit",
        patterns=("*-audit.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("audit evidence is recorded for a milestone or review",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="identity",
        patterns=("*-identity.txt",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("identity proof is recorded for command or output evidence",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="preservation",
        patterns=("*-preservation.md", "behavior-preservation.md"),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("behavior preservation evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="adoption-surface-review",
        patterns=("adoption-surface-review.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("adoption-surface cold-read, link, command, stale-version, unsupported-claim, and visual evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="readme-ownership-proof",
        patterns=("readme-ownership-proof.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("README generated-region and source-of-truth ownership proof is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="vision-readme-sync-proof",
        patterns=("vision-readme-sync-proof.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("VISION.md and README consistency proof is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="cold-read-review",
        patterns=("cold-read-review.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("cold-read reviewer evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="guide-cold-read-proof",
        patterns=("guide-cold-read.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("guide-system cold-read proof is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="repository-metadata-proof",
        patterns=("repository-metadata-proof.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("external repository metadata before and after proof is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="version-sync-proof",
        patterns=("version-sync-proof.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("Quick Start release-version source and stale-version proof is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="baseline",
        patterns=("baseline.md", "selected-tests-baseline.txt", "script-performance-baseline.yaml"),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("baseline evidence is recorded for a comparison",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="selector-regression-profile",
        patterns=("selector-regression-profile.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("selector-regression profiling evidence is recorded before optimization",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="token-cost",
        patterns=("token-cost.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("token-cost evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="behavior-parity",
        patterns=("behavior-parity.md", "behavior-parity-report.md"),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("behavior parity evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="generated-output",
        patterns=("generated-output-proof.md", "*-generated-token-cold-read-evidence.md"),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("generated-output evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="routing-coverage",
        patterns=("routing-coverage.md", "selector-routing-proof.md"),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("routing coverage evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="skill-audit",
        patterns=("skill-contract-sufficiency.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("skill audit evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="script-output",
        patterns=("output-contract-red-test.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("script-output behavior evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="command-output",
        patterns=(
            "broad-smoke-child-classification.md",
            "broad-smoke-child-commands-*.txt",
            "change-metadata-validator-tests-*.txt",
            "selected-tests-m3.txt",
        ),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("command-output evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="historical-coverage",
        patterns=("historical-coverage.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("historical coverage evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="clean-install-proof",
        patterns=("clean-install-proof.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("clean-install proof evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="validator-fixtures",
        patterns=("validator-fixtures.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("validator fixture evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="project-map-output-proof",
        patterns=("cold-read-proof.md", "representative-project-map-outputs.md"),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("project-map representative output or cold-read proof is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="release-process-dry-run",
        patterns=("release-process-dry-run.md",),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("non-publishing release-process rehearsal evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="implementation-note",
        patterns=("implementation-notes.md", "cold-read-report.md", "adapter-packaging.md"),
        selector_routes=("artifact_lifecycle.validate",),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("implementation support evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="validation-cache-evidence",
        patterns=("validation-cache-evidence.yaml",),
        selector_routes=("artifact_lifecycle.validate", "validation_cache.regression"),
        required_validator="validate-artifact-lifecycle",
        lifecycle_stage="implementation",
        allowed_when=("formal validation cache-hit evidence is recorded",),
    ),
    EvidenceClassRegistration(
        evidence_class_id="validation-cache-measurement",
        patterns=("validation-cache-measurement.yaml",),
        selector_routes=("artifact_lifecycle.validate", "change_metadata.validate"),
        required_validator="validate-change-metadata",
        lifecycle_stage="implementation",
        allowed_when=("Workstream A validation cache measurement evidence is recorded",),
    ),
)


@dataclass(frozen=True)
class SelectionRequest:
    mode: str
    paths: tuple[str, ...] = ()
    base: str | None = None
    head: str | None = None
    release_version: str | None = None
    broad_smoke: bool = False
    trigger_context_paths: tuple[str, ...] = ()
    repo_root: Path | str = Path.cwd()
    adapter_version: str = DEFAULT_ADAPTER_VERSION


@dataclass(frozen=True)
class NormalizedPath:
    ok: bool
    path: str | None = None
    blocking_code: str | None = None
    message: str | None = None


@dataclass(frozen=True)
class PathClassification:
    path: str
    category: str | None


@dataclass
class SelectedCheckDraft:
    id: str
    reasons: list[str] = field(default_factory=list)
    paths: set[str] = field(default_factory=set)
    affected_roots: set[str] = field(default_factory=set)
    versions: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class SelectionResult:
    mode: str
    status: str
    changed_paths: tuple[str, ...]
    classified_paths: tuple[dict[str, str], ...]
    unclassified_paths: tuple[str, ...]
    selected_checks: tuple[dict[str, Any], ...]
    affected_roots: tuple[str, ...]
    broad_smoke_required: bool
    blocking_results: tuple[dict[str, str], ...]
    preflight_results: tuple[dict[str, Any], ...]
    registration_debt: tuple[dict[str, Any], ...]
    rationale: tuple[str, ...]
    broad_smoke: dict[str, Any]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "status": self.status,
            "changed_paths": list(self.changed_paths),
            "classified_paths": list(self.classified_paths),
            "unclassified_paths": list(self.unclassified_paths),
            "selected_checks": list(self.selected_checks),
            "affected_roots": list(self.affected_roots),
            "broad_smoke_required": self.broad_smoke_required,
            "broad_smoke": self.broad_smoke,
            "blocking_results": list(self.blocking_results),
            "preflight_results": list(self.preflight_results),
            "registration_debt": list(self.registration_debt),
            "rationale": list(self.rationale),
        }


def exit_code_for_status(status: str) -> int:
    return EXIT_CODES.get(status, 4)


def selection_result_to_json(result: SelectionResult) -> str:
    return json.dumps(result.to_json_dict(), indent=2, sort_keys=False) + "\n"


def is_parallel_safe_check(check_id: str) -> bool:
    if check_id not in CHECK_CATALOG:
        raise ValueError(f"unknown check ID: {check_id}")
    return CHECK_CATALOG[check_id].parallel_safe


def error_result(mode: str, message: str, *, code: str = "invalid-invocation") -> SelectionResult:
    return _build_result(
        mode=mode or "unknown",
        changed_paths=[],
        classified_paths=[],
        unclassified_paths=[],
        selected={},
        affected_roots=set(),
        broad_smoke_sources=[],
        blocking_results=[{"code": code, "message": message}],
        preflight_results=[],
        status="error",
    )


def normalize_path(raw_path: str, *, repo_root: Path | str) -> NormalizedPath:
    root = Path(repo_root).resolve()
    raw = raw_path.strip()
    if not raw:
        return NormalizedPath(False, blocking_code="empty-path", message="path must not be empty")

    candidate = Path(raw)
    if ".." in candidate.parts:
        return NormalizedPath(
            False,
            blocking_code="path-traversal",
            message="path traversal is not allowed",
        )

    resolved = candidate.resolve(strict=False) if candidate.is_absolute() else (root / candidate).resolve(strict=False)
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return NormalizedPath(
            False,
            blocking_code="outside-repository-path",
            message="path is outside the repository",
        )

    return NormalizedPath(True, path=PurePosixPath(relative.as_posix()).as_posix())


def classify_path(path: str) -> PathClassification:
    category = _path_category(path)
    return PathClassification(path=path, category=category)


def validate_evidence_class_registry(
    registry: tuple[EvidenceClassRegistration, ...] | list[EvidenceClassRegistration] = CHANGE_EVIDENCE_CLASSES,
    *,
    sample_paths: tuple[str, ...] = (),
) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    for entry in registry:
        if not EVIDENCE_ID_PATTERN.fullmatch(entry.evidence_class_id):
            errors.append(f"evidence class ID is not stable ASCII: {entry.evidence_class_id}")
        if entry.evidence_class_id in seen_ids:
            errors.append(f"duplicate evidence class ID: {entry.evidence_class_id}")
        seen_ids.add(entry.evidence_class_id)
        if entry.allowed_root != "docs/changes/{change_id}/":
            errors.append(f"{entry.evidence_class_id}: unsupported allowed root {entry.allowed_root}")
        if not entry.patterns:
            errors.append(f"{entry.evidence_class_id}: missing filename pattern or exact filename")
        for pattern in entry.patterns:
            if _is_broad_evidence_pattern(pattern):
                errors.append(f"{entry.evidence_class_id}: evidence pattern {pattern} is too broad")
        if not entry.selector_routes:
            errors.append(f"{entry.evidence_class_id}: missing selector route")
        for route in entry.selector_routes:
            if route not in CHECK_CATALOG:
                errors.append(f"{entry.evidence_class_id}: unknown selector route {route}")
        if not entry.required_validator:
            errors.append(f"{entry.evidence_class_id}: missing required validator")
        if not entry.lifecycle_stage:
            errors.append(f"{entry.evidence_class_id}: missing lifecycle stage")
        if not (entry.allowed_when or entry.required_when or entry.forbidden_when):
            errors.append(f"{entry.evidence_class_id}: missing allowed/required/forbidden conditions")

    for sample_path in sample_paths:
        matches = _matching_evidence_classes(sample_path, registry=tuple(registry))
        if len(matches) > 1:
            class_ids = ", ".join(entry.evidence_class_id for entry in matches)
            errors.append(f"{sample_path}: ambiguous evidence class match: {class_ids}")
    return errors


def catalog_command(
    check_id: str,
    *,
    paths: tuple[str, ...] = (),
    affected_roots: tuple[str, ...] = (),
    versions: tuple[str, ...] = (),
    adapter_version: str = DEFAULT_ADAPTER_VERSION,
) -> str:
    if check_id not in CHECK_CATALOG:
        raise ValueError(f"unknown check ID: {check_id}")

    if check_id == "adapters.drift":
        return _join(
            "python",
            "scripts/test-adapter-distribution.py",
            "AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives",
        )
    if check_id == "adapters.validate":
        return _join(
            "python",
            "scripts/test-adapter-distribution.py",
            "AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root",
        )
    if check_id == "review_artifacts.validate":
        if not affected_roots:
            raise ValueError("review_artifacts.validate requires at least one change root")
        return _join("python", "scripts/validate-review-artifacts.py", *affected_roots)
    if check_id == "artifact_lifecycle.validate":
        if not paths:
            raise ValueError("artifact_lifecycle.validate requires at least one path")
        args = ["python", "scripts/validate-artifact-lifecycle.py", "--mode", "explicit-paths"]
        for path in paths:
            args.extend(["--path", path])
        return _join(*args)
    if check_id == "change_metadata.validate":
        if not paths:
            raise ValueError("change_metadata.validate requires at least one change.yaml path")
        return _join("python", "scripts/validate-change-metadata.py", *paths)
    if check_id == "release.validate":
        if not versions:
            raise ValueError("release.validate requires at least one release version")
        args = ["python", "scripts/validate-release-ci.py", "--version"]
        args.extend(versions)
        return _join(*args)
    if check_id == "token_cost.report_validate":
        if not paths:
            raise ValueError("token_cost.report_validate requires at least one report YAML path")
        return _join("python", "scripts/validate-token-cost-report.py", *paths)

    return CHECK_CATALOG[check_id].command_template


def select_validation(request: SelectionRequest) -> SelectionResult:
    repo_root = Path(request.repo_root).resolve()
    invalid = _validate_request(request)
    if invalid:
        return error_result(request.mode, invalid)

    changed_paths, normalization_blocks = _resolve_changed_paths(request, repo_root=repo_root)
    selected: dict[str, SelectedCheckDraft] = {}
    classified_paths: list[dict[str, str]] = []
    unclassified_paths: list[str] = []
    affected_roots: set[str] = set()
    blocking_results: list[dict[str, str]] = []
    blocking_results.extend(normalization_blocks)
    preflight_results = _preflight_results(changed_paths, repo_root=repo_root)
    blocking_results.extend(
        result for result in preflight_results if result.get("result") == "blocked"
    )
    registration_debt: list[dict[str, Any]] = []

    release_versions: set[str] = set()
    for path in changed_paths:
        classification = classify_path(path)
        if classification.category is None:
            unclassified_paths.append(path)
            blocking_results.append(
                {
                    "code": "unclassified-path",
                    "path": path,
                    "message": "changed path is not classified by the v1 selector",
                }
            )
            continue

        classified_paths.append({"path": path, "category": classification.category})
        _apply_path_selection(
            path,
            classification.category,
            changed_paths=changed_paths,
            selected=selected,
            affected_roots=affected_roots,
            blocking_results=blocking_results,
            registration_debt=registration_debt,
            release_versions=release_versions,
            repo_root=repo_root,
        )

    if _readme_marker_validation_required(tuple(changed_paths), repo_root=repo_root):
        _add_check(
            selected,
            "readme.vision_markers",
            "README vision markers require marker-boundary validation.",
        )

    broad_smoke_sources = _broad_smoke_sources(request, changed_paths=changed_paths, repo_root=repo_root)
    broad_smoke_required = bool(broad_smoke_sources)
    if broad_smoke_required:
        _add_check(selected, "broad_smoke.repo", "Broad smoke is required by an authoritative source.")

    if not changed_paths and not broad_smoke_required:
        blocking_results.append(
            {
                "code": "empty-changed-paths",
                "message": "no changed paths were provided or discovered",
            }
        )

    status = "blocked" if blocking_results else "ok"
    return _build_result(
        mode=request.mode,
        changed_paths=changed_paths,
        classified_paths=classified_paths,
        unclassified_paths=unclassified_paths,
        selected=selected,
        affected_roots=affected_roots,
        broad_smoke_sources=broad_smoke_sources,
        blocking_results=blocking_results,
        preflight_results=preflight_results,
        registration_debt=registration_debt,
        status=status,
        adapter_version=request.adapter_version,
    )


def _validate_request(request: SelectionRequest) -> str | None:
    if request.mode not in {"local", "explicit", "pr", "main", "release"}:
        return "unsupported or missing --mode"
    if request.mode == "explicit" and not request.paths:
        return "--mode explicit requires at least one --path"
    if request.mode in {"pr", "main"} and (not request.base or not request.head):
        return f"--mode {request.mode} requires --base and --head"
    if request.mode == "release" and not request.release_version:
        return "--mode release requires --release-version"
    return None


def _resolve_changed_paths(
    request: SelectionRequest,
    *,
    repo_root: Path,
) -> tuple[list[str], list[dict[str, str]]]:
    raw_paths: list[str]
    blocks: list[dict[str, str]] = []

    if request.mode in {"explicit", "local"} and request.paths:
        raw_paths = list(request.paths)
    elif request.mode == "local":
        raw_paths = _git_local_changed_paths(repo_root)
    elif request.mode in {"pr", "main"}:
        raw_paths = _git_range_changed_paths(repo_root, request.base or "", request.head or "")
    elif request.mode == "release":
        raw_paths = [f"docs/releases/{request.release_version}/release.yaml"]
    else:
        raw_paths = []

    normalized_paths: list[str] = []
    seen: set[str] = set()
    for raw_path in raw_paths:
        normalized = normalize_path(raw_path, repo_root=repo_root)
        if not normalized.ok:
            blocks.append(
                {
                    "code": normalized.blocking_code or "invalid-path",
                    "path": _safe_path_label(raw_path),
                    "message": normalized.message or "invalid path",
                }
            )
            continue
        assert normalized.path is not None
        if normalized.path not in seen:
            normalized_paths.append(normalized.path)
            seen.add(normalized.path)
    return normalized_paths, blocks


def _is_authoritative_artifact(path: str) -> bool:
    return path in AUTHORITATIVE_ARTIFACT_FILES or path.startswith(AUTHORITATIVE_ARTIFACT_PREFIXES)


def _run_git(
    repo_root: Path,
    args: list[str],
) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return None


def _inside_git_worktree(repo_root: Path) -> bool:
    result = _run_git(repo_root, ["rev-parse", "--is-inside-work-tree"])
    return bool(result and result.returncode == 0 and result.stdout.strip() == "true")


def _git_unmerged_paths(repo_root: Path) -> list[str]:
    result = _run_git(repo_root, ["status", "--porcelain=v1", "--untracked-files=no"])
    if not result or result.returncode != 0:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        index_status = line[0]
        worktree_status = line[1]
        if "U" in {index_status, worktree_status} or (index_status, worktree_status) in {
            ("A", "A"),
            ("D", "D"),
        }:
            paths.append(line[3:])
    return paths


def _git_tracked_paths(repo_root: Path) -> frozenset[str]:
    result = _run_git(repo_root, ["ls-files", "-z"])
    if not result or result.returncode != 0:
        return frozenset()
    return frozenset(path for path in result.stdout.split("\0") if path)


def _build_preflight_context(repo_root: Path) -> RepositoryPreflightContext:
    return RepositoryPreflightContext(
        tracked_paths=_git_tracked_paths(repo_root),
        unmerged_paths=tuple(_git_unmerged_paths(repo_root)),
    )


def _preflight_results(changed_paths: list[str], *, repo_root: Path) -> list[dict[str, str]]:
    if not _inside_git_worktree(repo_root):
        return []

    results: list[dict[str, str]] = []
    context = _build_preflight_context(repo_root)
    unmerged = list(context.unmerged_paths)
    if unmerged:
        results.append(
            {
                "check": "unmerged_paths",
                "result": "blocked",
                "code": "unmerged-paths",
                "path": ", ".join(unmerged),
                "message": "unmerged paths make validation readiness ambiguous",
                "corrective_action": "resolve merge conflicts, then rerun validation",
            }
        )
    else:
        results.append({"check": "unmerged_paths", "result": "pass"})

    untracked_authoritative = [
        path
        for path in changed_paths
        if _is_authoritative_artifact(path)
        and (repo_root / path).exists()
        and path not in context.tracked_paths
    ]
    if untracked_authoritative:
        path_list = ", ".join(untracked_authoritative)
        results.append(
            {
                "check": "tracked_authoritative_artifacts",
                "result": "blocked",
                "code": "untracked-authoritative-artifacts",
                "path": path_list,
                "message": "authoritative artifacts must be tracked before broad validation can prove branch readiness",
                "corrective_action": f"git add -- {path_list}",
            }
        )
    else:
        results.append({"check": "tracked_authoritative_artifacts", "result": "pass"})

    return results


def _git_local_changed_paths(repo_root: Path) -> list[str]:
    tracked = _git_lines(repo_root, "diff", "--name-only", "--diff-filter=ACMRT", "HEAD", "--", ".")
    staged = _git_lines(repo_root, "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "--", ".")
    untracked = _git_lines(repo_root, "ls-files", "--others", "--exclude-standard")
    return _dedupe([*tracked, *staged, *untracked])


def _git_range_changed_paths(repo_root: Path, base: str, head: str) -> list[str]:
    return _git_lines(repo_root, "diff", "--name-only", "--diff-filter=ACMRT", base, head, "--", ".")


def _git_lines(repo_root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _apply_path_selection(
    path: str,
    category: str,
    *,
    changed_paths: tuple[str, ...],
    selected: dict[str, SelectedCheckDraft],
    affected_roots: set[str],
    blocking_results: list[dict[str, str]],
    registration_debt: list[dict[str, Any]],
    release_versions: set[str],
    repo_root: Path,
) -> None:
    if category == "skills":
        root = _skill_root(path)
        if root:
            affected_roots.add(root)
        _add_check(selected, "skills.validate", "Changed canonical skill source requires skill validation.")
        _add_check(selected, "skills.regression", "Changed canonical skill source requires skill regression fixtures.")
        _add_check(
            selected,
            "skills.generation_regression",
            "Changed canonical skill source requires local mirror generation regression fixtures.",
        )
        _add_check(selected, "skills.drift", "Changed canonical skill source requires generated skill mirror validation.")
        _add_check(selected, "adapters.drift", "Public adapter output can be affected by canonical skill changes.")
        _add_lifecycle_warning_check(
            selected,
            path,
            "Changed canonical skill source can carry lifecycle guidance and requires lifecycle-language warning validation.",
        )
        return

    if category == "generated-skills":
        _add_check(
            selected,
            "skills.generation_regression",
            "Generated Codex skill output requires local mirror generation regression fixtures.",
        )
        _add_check(selected, "skills.drift", "Generated Codex skill output must be reproducible from canonical skills.")
        return

    if category in {"generated-adapters", "adapters"}:
        _add_check(selected, "adapters.regression", "Adapter output or generator change requires adapter regression fixtures.")
        _add_check(selected, "adapters.drift", "Adapter output or generator change requires adapter drift check.")
        _add_check(selected, "adapters.validate", "Adapter output or generator change requires adapter validation.")
        return

    if category == "review-artifacts":
        root = _change_root(path)
        if root:
            affected_roots.add(root)
            _add_check(
                selected,
                "review_artifacts.validate",
                "Changed review artifact requires review artifact structure validation.",
                affected_root=root,
            )
        _add_lifecycle_warning_check(
            selected,
            path,
            "Changed review artifact can carry lifecycle state and requires lifecycle-language warning validation.",
        )
        return

    if category == "change-metadata":
        root = _change_root(path)
        if root:
            affected_roots.add(root)
        _add_check(
            selected,
            "change_metadata.validate",
            "Changed change metadata requires change metadata validation.",
            path=path,
        )
        _add_check(selected, "change_metadata.regression", "Changed change metadata requires validator regression fixtures.")
        _add_lifecycle_warning_check(
            selected,
            path,
            "Changed change metadata can carry lifecycle state and requires lifecycle-language warning validation.",
        )
        return

    if category == "lifecycle":
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed lifecycle artifact requires artifact lifecycle validation.",
            path=path,
        )
        return

    if category == "change-local-lifecycle":
        governing_change_yaml = _change_root_change_yaml(path)
        if governing_change_yaml:
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed change-local lifecycle artifact requires its governing change metadata for lifecycle validation.",
                path=governing_change_yaml,
            )
        if _is_plan_index_migration_proof(path):
            for index_path in _plan_index_surface_paths():
                _add_check(
                    selected,
                    "artifact_lifecycle.validate",
                    "Changed plan-index migration proof requires plan index surface validation.",
                    path=index_path,
                )
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed change-local lifecycle artifact requires artifact lifecycle validation.",
            path=path,
        )
        return

    if category == "registered-change-evidence":
        evidence_name = path.split("/")[3]
        matches = _matching_evidence_classes(evidence_name)
        if len(matches) != 1:
            blocking_results.append(
                {
                    "code": "manual-routing-required",
                    "path": path,
                    "message": "registered change evidence could not be resolved to exactly one evidence class",
                }
            )
            return
        evidence_class = matches[0]
        governing_change_root = _change_root(path)
        governing_change_yaml = _change_root_change_yaml(path)
        if governing_change_root:
            affected_roots.add(governing_change_root)
        for route in evidence_class.selector_routes:
            if route == "artifact_lifecycle.validate":
                if governing_change_yaml:
                    _add_check(
                        selected,
                        route,
                        f"Registered change evidence class {evidence_class.evidence_class_id} requires governing change metadata for lifecycle validation.",
                        path=governing_change_yaml,
                    )
                _add_check(
                    selected,
                    route,
                    f"Registered change evidence class {evidence_class.evidence_class_id} requires lifecycle validation.",
                    path=path,
                )
            elif route == "change_metadata.validate":
                if evidence_class.evidence_class_id == "validation-cache-measurement":
                    _add_check(
                        selected,
                        route,
                        "Validation cache measurement evidence requires measurement metadata validation.",
                        path=path,
                    )
                    _add_check(
                        selected,
                        "change_metadata.regression",
                        "Validation cache measurement evidence requires validator regression fixtures.",
                    )
                elif governing_change_yaml:
                    _add_check(
                        selected,
                        route,
                        f"Registered change evidence class {evidence_class.evidence_class_id} requires change metadata validation.",
                        path=governing_change_yaml,
                    )
                    _add_check(
                        selected,
                        "change_metadata.regression",
                        "Registered change evidence with metadata route requires validator regression fixtures.",
                    )
            else:
                _add_check(
                    selected,
                    route,
                    f"Registered change evidence class {evidence_class.evidence_class_id} requires {route}.",
                    path=path,
                )
        return

    if category == "ambiguous-change-evidence":
        blocking_results.append(
            {
                "code": "ambiguous-evidence-class",
                "path": path,
                "message": "changed evidence path matches more than one registered evidence class",
            }
        )
        return

    if category == "unregistered-change-evidence":
        root = _change_root(path)
        if root:
            affected_roots.add(root)
        governing_change_yaml = _change_root_change_yaml(path)
        deferral = evaluate_evidence_registration_deferral(
            evidence_path=path,
            change_yaml_path=repo_root / governing_change_yaml if governing_change_yaml else None,
            change_root=root,
        )
        debt_result = _evidence_registration_debt_result(path, deferral)
        if deferral.status == "complete":
            registration_debt.append(debt_result)
        else:
            blocking_results.append(debt_result)
        return

    if category == "architecture-diagram":
        architecture_doc = _architecture_doc_for_diagram(path)
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed architecture diagram requires validation of its architecture package context.",
            path=architecture_doc or path,
        )
        return

    if category == "plan-index":
        _add_check(
            selected,
            "guide_system.validate",
            "Changed plan index surface requires cross-guide boundary validation.",
        )
        context_paths = _plan_index_context_paths(changed_paths)
        for index_path in _plan_index_surface_paths():
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed plan index surface requires paired plan index surface lifecycle validation.",
                path=index_path,
            )
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed plan index requires artifact lifecycle validation with the related plan context.",
            path=path,
        )
        for context_path in context_paths:
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed plan index requires artifact lifecycle validation with the related plan context.",
                path=context_path,
            )
        return

    if category == "release":
        if _is_flat_release_evidence_path(path):
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed flat release evidence requires release evidence checklist validation.",
                path=path,
            )
            return
        version = _release_version_from_path(path)
        if not version:
            blocking_results.append(
                {
                    "code": "release-version-required",
                    "path": path,
                    "message": "release version could not be inferred from release path",
                }
            )
            return
        release_versions.add(version)
        _add_check(selected, "release.validate", "Changed release artifact requires release validation.", version=version)
        return

    if category == "readme":
        _add_check(selected, "readme.validate", "Changed README requires lightweight README validation.")
        _add_check(
            selected,
            "guide_system.validate",
            "Changed README requires cross-guide index validation.",
        )
        return

    if category == "learn-artifact":
        _add_check(
            selected,
            "guide_system.validate",
            "Changed learn session requires non-authority guide validation.",
        )
        return

    if category == "requirement-fidelity-spec-read":
        _add_check(
            selected,
            "requirement_fidelity.spec_reads",
            "Changed requirement-fidelity spec-read proof requires bounded-read validation.",
        )
        return

    if category == "examples":
        return

    if category == "living-reference/project-map":
        _add_check(
            selected,
            "guide_system.validate",
            "Changed project map requires cross-guide scope validation.",
        )
        return

    if category == "follow-up-register":
        _add_check(
            selected,
            "skills.regression",
            "Changed follow-up register requires follow-up register static validation.",
        )
        return

    if category == "vision":
        _add_check(
            selected,
            "readme.vision_markers",
            "Changed root vision requires README vision marker validation.",
        )
        _add_check(
            selected,
            "guide_system.validate",
            "Changed root vision requires cross-guide registry duplication validation.",
        )
        return

    if category == "guide-system-validator":
        _add_check(
            selected,
            "guide_system.regression",
            "Changed guide-system validator requires guide-system regression fixtures.",
        )
        _add_check(
            selected,
            "guide_system.validate",
            "Changed guide-system validator requires live guide-system validation.",
        )
        return

    if category in {"selector", "ci-wrapper"}:
        reason = (
            "Changed CI wrapper requires selector and wrapper regression fixtures."
            if category == "ci-wrapper"
            else "Changed selector code requires selector regression fixtures."
        )
        _add_check(selected, "selector.regression", reason)
        return

    if category == "token-cost":
        _add_check(
            selected,
            "token_cost.regression",
            "Changed token-cost measurement surface requires token-cost measurement regression fixtures.",
        )
        if _is_token_cost_report_validation_surface(path):
            _add_check(
                selected,
                "token_cost.report_regression",
                "Changed token-cost report validation surface requires report validator regression fixtures.",
            )
        if _is_token_cost_release_report_yaml(path):
            _add_check(
                selected,
                "token_cost.report_validate",
                "Changed token-cost release report metadata requires report validation.",
                path=path,
            )
        return

    if category == "adapter-artifact-metadata":
        _add_check(
            selected,
            "adapters.regression",
            "Changed adapter artifact metadata requires adapter distribution regression fixtures.",
        )
        return

    if category == "validator-review-artifacts":
        _add_check(
            selected,
            "review_artifacts.regression",
            "Changed review artifact validator requires review artifact regression fixtures.",
        )
        return

    if category == "review-artifact-fixtures":
        _add_check(
            selected,
            "review_artifacts.regression",
            "Changed review artifact fixture requires review artifact regression fixtures.",
        )
        if path.endswith("/change.yaml"):
            _add_check(
                selected,
                "change_metadata.regression",
                "Changed review artifact metadata fixture requires change metadata regression fixtures.",
            )
        return

    if category == "change-metadata-fixtures":
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed change metadata fixture requires change metadata regression fixtures.",
        )
        return

    if category == "change-record-query":
        _add_check(
            selected,
            "change_record_query.regression",
            "Changed change-record query helper requires query regression fixtures.",
        )
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed change-record query helper depends on supported change metadata shapes.",
        )
        return

    if category == "validator-artifact-lifecycle":
        _add_check(
            selected,
            "artifact_lifecycle.regression",
            "Changed artifact lifecycle validator requires lifecycle regression fixtures.",
        )
        return

    if category == "artifact-lifecycle-fixtures":
        _add_check(
            selected,
            "artifact_lifecycle.regression",
            "Changed artifact lifecycle fixture requires lifecycle regression fixtures.",
        )
        return

    if category == "validation-cache":
        _add_check(
            selected,
            "validation_cache.regression",
            "Changed validation cache identity helper requires cache regression fixtures.",
        )
        return

    if category == "retained-change-fixture":
        _add_check(
            selected,
            "artifact_lifecycle.regression",
            "Changed retained change fixture rationale requires lifecycle regression fixtures.",
        )
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed retained change fixture rationale requires lifecycle validation.",
            path=path,
        )
        return

    if category == "validator-change-metadata":
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed change metadata validator requires change metadata regression fixtures.",
        )
        return

    if category == "validator-skills":
        _add_check(selected, "skills.regression", "Changed skill generation or validation requires skill regression fixtures.")
        _add_check(
            selected,
            "skills.generation_regression",
            "Changed skill generation or validation requires local mirror generation regression fixtures.",
        )
        return

    if category in {"ci-workflow", "templates"}:
        _add_check(
            selected,
            "selector.regression",
            f"Changed {category} path requires selector and workflow routing regression fixtures.",
        )
        return

    if category in {"workflow-guidance", "governance"}:
        _add_check(
            selected,
            "selector.regression",
            f"Changed {category} path requires selector and workflow routing regression fixtures.",
        )
        _add_check(
            selected,
            "guide_system.validate",
            f"Changed {category} path requires cross-guide validation.",
        )
        _add_lifecycle_warning_check(
            selected,
            path,
            f"Changed {category} path can carry lifecycle policy and requires lifecycle-language warning validation.",
        )
        return

    if category == "ignore-policy":
        _add_check(
            selected,
            "skills.generation_regression",
            "Changed ignore policy requires local mirror generation regression fixtures.",
        )
        return

    if category == "schemas":
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed schema path requires change metadata regression fixtures.",
        )
        return

    if category == "release-script":
        _add_check(
            selected,
            "adapters.regression",
            "Changed release script requires release and adapter distribution regression fixtures.",
        )
        return

    if category == "rigorloop-cli":
        _add_check(
            selected,
            "rigorloop_cli.test",
            "Changed RigorLoop CLI package requires package test validation.",
        )
        _add_check(
            selected,
            "npm_package_publication.test",
            "Changed RigorLoop npm package surface requires package publication validation.",
        )
        return

    blocking_results.append(
        {
            "code": "manual-routing-required",
            "path": path,
            "message": f"changed {category} path has no deterministic v1 selector check",
        }
    )


def _add_check(
    selected: dict[str, SelectedCheckDraft],
    check_id: str,
    reason: str,
    *,
    path: str | None = None,
    affected_root: str | None = None,
    version: str | None = None,
) -> None:
    draft = selected.setdefault(check_id, SelectedCheckDraft(id=check_id))
    if reason not in draft.reasons:
        draft.reasons.append(reason)
    if path:
        draft.paths.add(path)
    if affected_root:
        draft.affected_roots.add(affected_root)
    if version:
        draft.versions.add(version)


def _add_lifecycle_warning_check(
    selected: dict[str, SelectedCheckDraft],
    path: str,
    reason: str,
) -> None:
    _add_check(selected, "artifact_lifecycle.validate", reason, path=path)


def _evidence_registration_debt_result(
    evidence_path: str,
    deferral: EvidenceDeferralStatus,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "code": "manual-routing-required",
        "path": evidence_path,
        "path_class": "unregistered-change-evidence",
        "affected_class": "change-local evidence",
        "manual_routing_required": True,
        "debt": "evidence-registration",
        "verify_readiness": "owner-deferred" if deferral.status == "complete" else "blocked",
        "deferral_status": deferral.status,
        "next_action": (
            "Register an evidence class and selector routing for this deterministic change-local evidence path "
            "or record a complete owner-approved deferral before verify with owner, path, "
            "reason, validation impact, and follow-up."
        ),
        "message": "unregistered deterministic change-local evidence creates registration debt",
    }
    if deferral.missing_fields:
        result["missing_deferral_fields"] = list(deferral.missing_fields)
    if deferral.invalid_fields:
        result["invalid_deferral_fields"] = list(deferral.invalid_fields)
    if deferral.status == "complete":
        result["owner"] = deferral.deferral.get("owner", "")
        result["follow_up"] = deferral.deferral.get("follow_up", "")
        result["deferral"] = dict(deferral.deferral)
    return result


def evaluate_evidence_registration_deferral(
    *,
    evidence_path: str,
    change_yaml_path: Path | None,
    change_root: str | None,
) -> EvidenceDeferralStatus:
    if change_yaml_path is None or change_root is None or not change_yaml_path.exists():
        return EvidenceDeferralStatus(status="none")

    deferrals = load_evidence_registration_deferrals(change_yaml_path)
    matching = [entry for entry in deferrals if entry.get("path") == evidence_path]
    if not matching:
        return EvidenceDeferralStatus(status="none")
    if len(matching) > 1:
        return EvidenceDeferralStatus(status="invalid", invalid_fields=("duplicate:path",))

    entry = matching[0]
    missing = tuple(sorted(field for field in REQUIRED_EVIDENCE_DEFERRAL_FIELDS if not entry.get(field, "").strip()))
    invalid = tuple(
        sorted(
            field
            for field in ("path", "follow_up")
            if entry.get(field) and not _is_safe_repo_relative_path(entry[field])
        )
    )
    path = entry.get("path", "")
    if path and not path.startswith(change_root):
        invalid = tuple(sorted((*invalid, "path")))

    if missing:
        return EvidenceDeferralStatus(status="incomplete", missing_fields=missing, invalid_fields=invalid)
    if invalid:
        return EvidenceDeferralStatus(status="invalid", invalid_fields=invalid)

    return EvidenceDeferralStatus(
        status="complete",
        deferral={field: entry[field].strip() for field in sorted(REQUIRED_EVIDENCE_DEFERRAL_FIELDS)},
    )


def load_evidence_registration_deferrals(change_yaml_path: Path) -> list[dict[str, str]]:
    lines = change_yaml_path.read_text(encoding="utf-8").splitlines()
    start_index: int | None = None
    for index, raw_line in enumerate(lines):
        if raw_line.strip() == "evidence_registration_deferrals:" and not raw_line.startswith(" "):
            start_index = index + 1
            break
    if start_index is None:
        return []

    deferrals: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    index = start_index
    while index < len(lines):
        line = lines[index]
        if line and not line.startswith(" "):
            break
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            index += 1
            continue
        if line.startswith("  - "):
            if current is not None:
                deferrals.append(current)
            current = {}
            remainder = line[4:].strip()
            if remainder:
                key, value = _split_selector_yaml_pair(remainder)
                current[key] = value
            index += 1
            continue
        if line.startswith("    ") and current is not None:
            key, value = _split_selector_yaml_pair(stripped)
            current[key] = value
        index += 1
    if current is not None:
        deferrals.append(current)
    return deferrals


def _split_selector_yaml_pair(text: str) -> tuple[str, str]:
    if ":" not in text:
        return text.strip(), ""
    key, value = text.split(":", 1)
    return key.strip(), value.strip().strip("\"'")


def _is_safe_repo_relative_path(value: str) -> bool:
    if not value or value.startswith(("/", "~")) or "\\" in value or "://" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _build_result(
    *,
    mode: str,
    changed_paths: list[str],
    classified_paths: list[dict[str, str]],
    unclassified_paths: list[str],
    selected: dict[str, SelectedCheckDraft],
    affected_roots: set[str],
    broad_smoke_sources: list[dict[str, str]],
    blocking_results: list[dict[str, str]],
    preflight_results: list[dict[str, Any]] | None = None,
    registration_debt: list[dict[str, Any]] | None = None,
    status: str,
    adapter_version: str = DEFAULT_ADAPTER_VERSION,
) -> SelectionResult:
    selected_checks: list[dict[str, Any]] = []
    build_errors: list[dict[str, str]] = []
    for check_id in CHECK_CATALOG:
        draft = selected.get(check_id)
        if draft is None:
            continue
        paths = tuple(sorted(draft.paths))
        roots = tuple(sorted(draft.affected_roots))
        versions = tuple(sorted(draft.versions))
        try:
            command = catalog_command(
                check_id,
                paths=paths,
                affected_roots=roots,
                versions=versions,
                adapter_version=adapter_version,
            )
        except ValueError as exc:
            build_errors.append(
                {
                    "code": "command-substitution-error",
                    "message": str(exc),
                }
            )
            continue
        entry: dict[str, Any] = {
            "id": check_id,
            "command": command,
            "reason": " ".join(draft.reasons),
            "phase": "boundary" if check_id in BOUNDARY_CHECK_IDS else "focused",
            "cache_status": "not-applicable",
        }
        if paths:
            entry["paths"] = list(paths)
        if roots:
            entry["affected_roots"] = list(roots)
        if versions:
            entry["versions"] = list(versions)
        selected_checks.append(entry)

    combined_blocking = [*blocking_results, *build_errors]
    final_status = "error" if build_errors else status
    return SelectionResult(
        mode=mode,
        status=final_status,
        changed_paths=tuple(changed_paths),
        classified_paths=tuple(classified_paths),
        unclassified_paths=tuple(unclassified_paths),
        selected_checks=tuple(selected_checks),
        affected_roots=tuple(sorted(affected_roots)),
        broad_smoke_required=bool(broad_smoke_sources),
        broad_smoke={
            "required": bool(broad_smoke_sources),
            "sources": list(broad_smoke_sources),
        },
        blocking_results=tuple(combined_blocking),
        preflight_results=tuple(preflight_results or []),
        registration_debt=tuple(registration_debt or []),
        rationale=tuple(entry["reason"] for entry in selected_checks),
    )


def _path_category(path: str) -> str | None:
    parts = path.split("/")
    if path == "README.md":
        return "readme"
    if path == ROOT_VISION_PATH:
        return "vision"
    if path.startswith("tests/fixtures/artifact-lifecycle/"):
        return "artifact-lifecycle-fixtures"
    if path.startswith("tests/fixtures/review-artifacts/"):
        return "review-artifact-fixtures"
    if path == "tests/fixtures/change-metadata" or path.startswith("tests/fixtures/change-metadata/"):
        return "change-metadata-fixtures"
    if path.startswith("tests/fixtures/requirement-fidelity-gate/representative-reviews/"):
        return "requirement-fidelity-spec-read"
    if path.startswith("tests/fixtures/adapters/"):
        return "adapters"
    if path == "tests/fixtures/skills" or path.startswith("tests/fixtures/skills/"):
        return "validator-skills"
    if path.startswith("skills/"):
        return "skills"
    if path.startswith(".codex/skills/"):
        return "generated-skills"
    if path.startswith("dist/adapters/"):
        return "generated-adapters"
    if path.startswith("scripts/adapter_templates/") or path in {
        "scripts/adapter_distribution.py",
        "scripts/build-adapters.py",
        "scripts/test-adapter-distribution.py",
        "scripts/validate-adapters.py",
    }:
        return "adapters"
    if path in {
        "scripts/select-validation.py",
        "scripts/validation_selection.py",
        "scripts/test-select-validation.py",
        "scripts/validate-readme.py",
    }:
        return "selector"
    if path == "scripts/test-fidelity-gate-spec-reads.py":
        return "requirement-fidelity-spec-read"
    if path in {"scripts/validate-guide-system.py", "scripts/test-guide-system-validator.py"}:
        return "guide-system-validator"
    if path == "scripts/ci.sh":
        return "ci-wrapper"
    if path == ".gitignore":
        return "ignore-policy"
    if path == ".github/workflows/ci.yml":
        return "ci-workflow"
    if path == ".github/workflows/release.yml":
        return "release-script"
    if path in {"scripts/validate-review-artifacts.py", "scripts/review_artifact_validation.py", "scripts/test-review-artifact-validator.py"}:
        return "validator-review-artifacts"
    if path in {
        "scripts/validate-artifact-lifecycle.py",
        "scripts/artifact_lifecycle_validation.py",
        "scripts/artifact_lifecycle_contracts.py",
        "scripts/lifecycle_state_sync.py",
        "scripts/test-artifact-lifecycle-validator.py",
    }:
        return "validator-artifact-lifecycle"
    if path in {"scripts/validation_cache.py", "scripts/test-validation-cache.py"}:
        return "validation-cache"
    if path in {
        "scripts/change_metadata_semantics.py",
        "scripts/validate-change-metadata.py",
        "scripts/test-change-metadata-validator.py",
    }:
        return "validator-change-metadata"
    if path in {
        "scripts/query-change-record.py",
        "scripts/test-query-change-record.py",
    }:
        return "change-record-query"
    if path in {
        "scripts/build-skills.py",
        "scripts/validate-skills.py",
        "scripts/skill_validation.py",
        "scripts/review_independence_skill_phrases.py",
        "scripts/test-build-skills.py",
        "scripts/test-skill-validator.py",
    }:
        return "validator-skills"
    if path in {
        "scripts/analyze-codex-jsonl.py",
        "scripts/measure-skill-tokens.py",
        "scripts/run-token-cost-benchmarks.py",
        "scripts/test-token-cost-measurement.py",
        "scripts/test-token-cost-report-validation.py",
        "scripts/validate-token-cost-report.py",
    }:
        return "token-cost"
    if path.startswith("benchmarks/token-cost/"):
        return "token-cost"
    if path.startswith("docs/reports/token-cost/"):
        return "token-cost"
    if path == "packages/rigorloop" or path.startswith("packages/rigorloop/"):
        return "rigorloop-cli"
    if path in {
        "scripts/npm_package_validation.py",
        "scripts/validate-npm-package.py",
        "scripts/test-npm-package-publication.py",
    }:
        return "rigorloop-cli"
    if path.startswith("docs/reports/adapter-artifacts/releases/") and path.endswith(".yaml"):
        return "adapter-artifact-metadata"
    if path.startswith("tests/fixtures/token-cost/"):
        return "token-cost"
    if path.startswith("docs/examples/"):
        return "examples"
    if path == "docs/project-map.md" or (
        path.startswith("docs/project-map/") and path.endswith(".md")
    ):
        return "living-reference/project-map"
    if path == "docs/follow-ups.md":
        return "follow-up-register"
    if path == "docs/changes/0001-skill-validator/README.md":
        return "retained-change-fixture"
    if path.startswith("docs/changes/") and len(parts) >= 4:
        if parts[3] == "change.yaml":
            return "change-metadata"
        if parts[3] in {"review-log.md", "review-resolution.md"} or parts[3] == "reviews":
            return "review-artifacts"
        if len(parts) == 4:
            matches = _matching_evidence_classes(parts[3])
            if len(matches) == 1:
                return "registered-change-evidence"
            if len(matches) > 1:
                return "ambiguous-change-evidence"
        change_local_name = parts[3]
        if change_local_name in {
            "explain-change.md",
            "architecture.md",
            "verify-report.md",
            "implementation-notes.md",
            "cold-read-report.md",
            "adapter-packaging.md",
            "baseline.md",
            "behavior-parity-report.md",
            "behavior-parity.md",
            "behavior-preservation.md",
            "output-contract-red-test.md",
            "script-output-audit.md",
            "script-output-layer-audit.md",
            "generated-output-proof.md",
            "historical-coverage.md",
            "plan-index-migration.md",
            "routing-coverage.md",
            "selected-tests-baseline.txt",
            "selected-tests-m3.txt",
            "skill-audit.md",
            "token-cost.md",
        } or (
            parts[3] == "diagrams"
        ):
            return "change-local-lifecycle"
        if len(parts) == 4:
            return "unregistered-change-evidence"
        return "change-local-unsupported"
    if path in _plan_index_surface_paths():
        return "plan-index"
    if path.startswith("docs/architecture/") and path.endswith(".mmd"):
        return "architecture-diagram"
    if _is_learn_artifact_path(path):
        return "learn-artifact"
    if _is_lifecycle_path(path):
        return "lifecycle"
    if path.startswith("docs/releases/"):
        if path in {"docs/releases/README.md", "docs/releases/index.md"}:
            return "workflow-guidance"
        return "release"
    if path == "docs/workflows.md":
        return "workflow-guidance"
    if path in {"AGENTS.md", "CONSTITUTION.md"}:
        return "governance"
    if path.startswith("templates/"):
        return "templates"
    if path.startswith("schemas/"):
        return "schemas"
    if path in {"scripts/validate-release.py", "scripts/validate-release-ci.py", "scripts/release-verify.sh"}:
        return "release-script"
    if path.startswith("scripts/"):
        return "script-unsupported"
    return None


def _matching_evidence_classes(
    filename: str,
    *,
    registry: tuple[EvidenceClassRegistration, ...] = CHANGE_EVIDENCE_CLASSES,
) -> list[EvidenceClassRegistration]:
    return [
        entry
        for entry in registry
        if any(fnmatch.fnmatchcase(filename, pattern) for pattern in entry.patterns)
    ]


def _is_broad_evidence_pattern(pattern: str) -> bool:
    if pattern in BROAD_EVIDENCE_PATTERNS:
        return True
    if pattern.startswith("*.") and pattern.count("*") == 1:
        return True
    return False


def _is_lifecycle_path(path: str) -> bool:
    if path == "docs/plan.md":
        return False
    if path.startswith("docs/proposals/") and path.endswith(".md"):
        return True
    if path.startswith("specs/") and path.endswith(".md"):
        return True
    if path.startswith("docs/architecture/") and path.endswith(".md"):
        return True
    if path.startswith("docs/adr/") and path.endswith(".md"):
        return True
    if path.startswith("docs/plans/") and path.endswith(".md"):
        return True
    if path.startswith("docs/vision/") and path.endswith(".md"):
        return True
    if path.startswith("docs/explain/") and path.endswith(".md"):
        return True
    return False


def _is_token_cost_release_report_yaml(path: str) -> bool:
    return (
        path.startswith("docs/reports/token-cost/releases/")
        and path.endswith(".yaml")
    )


def _is_token_cost_report_validation_surface(path: str) -> bool:
    return path in {
        "scripts/validate-token-cost-report.py",
        "scripts/test-token-cost-report-validation.py",
    } or path.startswith("tests/fixtures/token-cost/reports/")


def _is_learn_artifact_path(path: str) -> bool:
    if path == "docs/learn/README.md":
        return True
    if path.startswith("docs/learn/sessions/") and path.endswith(".md"):
        return True
    if path.startswith("docs/learn/topics/") and path.endswith(".md"):
        return True
    return False


def _change_root_change_yaml(path: str) -> str | None:
    root = _change_root(path)
    if root:
        return f"{root}change.yaml"
    return None


def _is_plan_index_migration_proof(path: str) -> bool:
    return path.startswith("docs/changes/") and path.endswith("/plan-index-migration.md")


def _plan_index_surface_paths() -> tuple[str, str]:
    return ("docs/plan-archive.md", "docs/plan.md")


def _architecture_doc_for_diagram(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) < 4 or parts[0] != "docs" or parts[1] != "architecture":
        return None
    try:
        diagrams_index = parts.index("diagrams")
    except ValueError:
        return None
    if diagrams_index <= 2:
        return None
    return "/".join([*parts[:diagrams_index], "architecture.md"])


def _plan_index_context_paths(changed_paths: tuple[str, ...]) -> list[str]:
    context: list[str] = []
    for path in changed_paths:
        if path == "docs/plan.md":
            continue
        if _is_lifecycle_path(path):
            context.append(path)
            continue
        if path.startswith("docs/changes/"):
            parts = path.split("/")
            if len(parts) >= 4 and parts[3] == "change.yaml":
                context.append(path)
                continue
            change_yaml = _change_root_change_yaml(path)
            if change_yaml:
                context.append(change_yaml)
    return _dedupe(context)


def _skill_root(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 2:
        return f"skills/{parts[1]}"
    return None


def _change_root(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 3 and parts[0] == "docs" and parts[1] == "changes":
        return f"docs/changes/{parts[2]}/"
    return None


def _release_version_from_path(path: str) -> str | None:
    parts = path.split("/")
    if _is_flat_release_evidence_path(path):
        return parts[2][:-3]
    if len(parts) >= 4 and parts[0] == "docs" and parts[1] == "releases" and parts[2] and parts[3]:
        return parts[2]
    return None


def _is_flat_release_evidence_path(path: str) -> bool:
    parts = path.split("/")
    if len(parts) != 3 or parts[0] != "docs" or parts[1] != "releases":
        return False
    filename = parts[2]
    return filename.startswith("v") and filename.endswith(".md") and len(filename) > len("v.md")


def _broad_smoke_sources(
    request: SelectionRequest,
    *,
    changed_paths: list[str],
    repo_root: Path,
) -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    if request.mode in {"main", "release"}:
        sources.append({"type": "mode", "value": request.mode})
    if request.broad_smoke:
        sources.append({"type": "explicit_flag", "value": "--broad-smoke"})
    if request.mode == "release" and request.release_version:
        sources.append(
            {
                "type": "release_metadata",
                "path": f"docs/releases/{request.release_version}/release.yaml",
            }
        )

    context_paths = _dedupe([*changed_paths, *request.trigger_context_paths])
    for raw_path in context_paths:
        normalized = normalize_path(raw_path, repo_root=repo_root)
        if not normalized.ok or normalized.path is None:
            continue
        source_type = _trigger_source_type(normalized.path)
        if source_type is None:
            continue
        path = repo_root / normalized.path
        if source_type != "release_metadata" and not _file_requires_broad_smoke(path):
            continue
        source = {"type": source_type, "path": normalized.path}
        if source not in sources:
            sources.append(source)
    return sources


def _readme_marker_validation_required(changed_paths: tuple[str, ...], *, repo_root: Path) -> bool:
    readme_changed = "README.md" in changed_paths
    return _vision_skill_in_scope(changed_paths) or (readme_changed and _readme_has_standalone_marker_block(repo_root))


def _vision_skill_in_scope(changed_paths: tuple[str, ...]) -> bool:
    for path in changed_paths:
        if path == "skills/vision/SKILL.md":
            return True
        if path == ".codex/skills/vision/SKILL.md":
            return True
        if path.endswith("/skills/vision/SKILL.md") and path.startswith("dist/adapters/"):
            return True
        if path.startswith("specs/vision-skill") and path.endswith(".md"):
            return True
        if (
            "vision-skill" in path
            and path.endswith(".md")
            and (path.startswith("docs/proposals/") or path.startswith("docs/plans/"))
        ):
            return True
        if path.startswith("docs/changes/") and "vision-skill" in path:
            return True
    return False


def _readme_has_standalone_marker_block(repo_root: Path) -> bool:
    readme = repo_root / "README.md"
    if not readme.is_file():
        return False
    try:
        lines = readme.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return False
    return "<!-- vision:start -->" in lines or "<!-- vision:end -->" in lines


def _trigger_source_type(path: str) -> str | None:
    if path.startswith("docs/plans/") and path.endswith(".md"):
        return "active_plan"
    if path.startswith("specs/") and path.endswith(".test.md"):
        return "test_spec"
    if path.startswith("docs/changes/") and path.endswith("/review-resolution.md"):
        return "review_resolution"
    if path.startswith("docs/releases/") and path.endswith("/release.yaml"):
        return "release_metadata"
    return None


def _file_requires_broad_smoke(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    return "broad_smoke_required: true" in lowered or "broad smoke required" in lowered


def _join(*args: str) -> str:
    return shlex.join(args)


def _dedupe(items: list[str] | tuple[str, ...]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def _safe_path_label(path: str) -> str:
    if Path(path).is_absolute():
        return "<outside-repository>"
    return path
