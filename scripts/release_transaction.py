#!/usr/bin/env python3
"""Release transaction profile loading and validation helpers."""

from __future__ import annotations

import json
import hashlib
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


SCHEMA_VERSION = "release-profile-v1"
EXPECTED_NPM_PACKAGE = "@xiongxianfei/rigorloop"
RELEASE_KINDS = frozenset(("routine", "special"))
ROUTINE_RELEASE_KIND = "routine"
SPECIAL_RELEASE_KIND = "special"
ROUTINE_TARGETS = ("codex", "claude", "opencode")
SUPPORTED_TARGETS = frozenset(ROUTINE_TARGETS)
REQUIRED_VALUE = "required"

REQUIRED_TOP_LEVEL_FIELDS = (
    "schema_version",
    "release_kind",
    "release_tag",
    "package_version",
    "npm_package",
    "targets",
    "adapter_artifacts",
    "publication",
    "evidence",
    "validation",
)
REQUIRED_ADAPTER_ARTIFACT_FIELDS = (
    "required",
    "metadata_file",
    "archive_version",
)
REQUIRED_PUBLICATION_FIELDS = (
    "github_release_required",
    "npm_publication_required",
    "trusted_publishing_required",
    "public_smoke_required",
)
REQUIRED_EVIDENCE_FIELDS = (
    "release_yaml",
    "release_notes",
    "npm_publication",
    "public_target_init_smoke",
    "archive_hashes",
    "tree_hashes",
    "file_counts",
    "timing",
)
REQUIRED_VALIDATION_FIELDS = (
    "local_release_verify_required",
    "ci_release_verify_required",
    "security_scanning_required",
)
TIMING_PHASE_IDS = frozenset(
    (
        "prepare_release",
        "preflight",
        "local_release_verify",
        "ci_release_verify",
        "publication_wait",
        "public_closeout",
    )
)
REQUIRED_TIMING_PHASES = (
    "prepare_release",
    "preflight",
    "local_release_verify",
    "ci_release_verify",
    "publication_wait",
    "public_closeout",
)
TIMING_RESULTS = frozenset(("pass", "fail", "skipped", "pending", "not-applicable"))
TIMING_DURATION_TARGET_SECONDS = {
    "preflight": 30,
    "local_release_verify": 1800,
    "public_closeout": 600,
}


class ReleaseProfileError(ValueError):
    """Raised when a release profile cannot be parsed or validated."""

    def __init__(self, path: Path, errors: list[str]) -> None:
        self.path = path
        self.errors = errors
        super().__init__(f"{path}: " + "; ".join(errors))


class ReleasePreflightChangedFilesError(ValueError):
    """Raised when release preflight cannot determine changed files."""


class PublicEvidenceUnavailable(RuntimeError):
    """Raised when public release closeout evidence is not available."""


@dataclass(frozen=True)
class ReleaseProfile:
    path: Path
    schema_version: str
    release_kind: str
    release_tag: str
    package_version: str
    npm_package: str
    targets: tuple[str, ...]
    adapter_artifacts: dict[str, Any]
    publication: dict[str, Any]
    evidence: dict[str, Any]
    validation: dict[str, Any]
    owner_decision: str | None = None


@dataclass(frozen=True)
class ReleaseSurfaceInventory:
    path: Path
    schema_version: str
    change_id: str
    surfaces: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class LiteralAuditBaseline:
    path: Path
    schema_version: str
    change_id: str
    audited_release_tag: str
    release_profile: str
    entries: tuple[dict[str, Any], ...]
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class PrepareReleaseResult:
    release_tag: str
    changed_paths: tuple[str, ...]
    external_actions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReleasePreflightResult:
    release_tag: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()
    external_actions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReleaseTimingValidationResult:
    release_tag: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class CloseReleasePublicationResult:
    release_tag: str
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()
    changed_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class GitHubReleaseAsset:
    name: str
    url: str
    size: int
    sha256: str | None = None


@dataclass(frozen=True)
class NpmPackageMetadata:
    package: str
    version: str
    tarball_url: str
    integrity: str
    shasum: str | None = None
    published_at: str | None = None


@dataclass(frozen=True)
class PublicSmokeResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    summary: str


class PublicEvidenceProvider(Protocol):
    def fetch_github_release_assets(self, *, tag: str) -> tuple[GitHubReleaseAsset, ...]:
        ...

    def fetch_npm_package_metadata(self, *, package: str, version: str) -> NpmPackageMetadata:
        ...

    def run_public_npx_smoke(self, *, command: str, cwd: Path) -> PublicSmokeResult:
        ...


@dataclass(frozen=True)
class PendingTargetSmoke:
    target: str
    fields: dict[str, Any]


SURFACE_CLASSIFICATIONS = frozenset(
    (
        "profile-owned-generated",
        "human-authored-profile-checked",
        "historical-immutable",
    )
)
LITERAL_CLASSIFICATIONS = frozenset(
    (
        "generated-current",
        "profile-owned",
        "historical-fixture",
        "version-independent",
        "baseline-drift",
        "unauthorized",
    )
)
LITERAL_DISPOSITIONS = frozenset(("allowed", "report-only", "must-fix"))


def profile_path_for_tag(tag: str, *, root: Path | str = Path(".")) -> Path:
    return Path(root) / "docs" / "releases" / "profiles" / f"{tag}.yaml"


def load_release_profile(tag: str, *, root: Path | str = Path(".")) -> ReleaseProfile:
    path = profile_path_for_tag(tag, root=root)
    profile = load_release_profile_file(path)
    if profile.release_tag != tag:
        raise ReleaseProfileError(
            path,
            [f"release_tag {profile.release_tag} does not match requested tag {tag}"],
        )
    return profile


def load_release_profile_file(path: Path | str) -> ReleaseProfile:
    profile_path = Path(path)
    try:
        text = profile_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ReleaseProfileError(
            profile_path,
            [f"release profile not found: {profile_path}"],
        ) from exc
    except OSError as exc:
        raise ReleaseProfileError(profile_path, [f"could not read release profile: {exc}"]) from exc

    try:
        data = _parse_profile_yaml(text)
    except ValueError as exc:
        raise ReleaseProfileError(profile_path, [f"could not parse release profile: {exc}"]) from exc

    return _validate_profile_data(profile_path, data)


def is_routine_release_profile(profile: ReleaseProfile) -> bool:
    return profile.release_kind == ROUTINE_RELEASE_KIND


def load_surface_inventory_file(path: Path | str) -> ReleaseSurfaceInventory:
    inventory_path = Path(path)
    data = _load_yaml_subset(inventory_path, "surface inventory")
    return _validate_surface_inventory(inventory_path, data)


def load_literal_audit_baseline_file(
    path: Path | str,
    *,
    changed_files: tuple[str, ...] = (),
) -> LiteralAuditBaseline:
    baseline_path = Path(path)
    data = _load_yaml_subset(baseline_path, "literal audit baseline")
    return _validate_literal_audit_baseline(
        baseline_path,
        data,
        changed_files=frozenset(changed_files),
    )


def prepare_release(
    tag: str,
    *,
    root: Path | str = Path("."),
    check: bool = False,
) -> PrepareReleaseResult:
    repo_root = Path(root)
    profile = load_release_profile(tag, root=repo_root)
    if not is_routine_release_profile(profile):
        raise ReleaseProfileError(profile.path, ["prepare-release requires a routine release profile"])

    planned: dict[Path, str] = {}
    package_version = _current_package_version(repo_root)
    _plan_package_json_update(planned, repo_root, profile)
    _plan_package_readme_update(planned, repo_root, profile, current_version=package_version)
    _plan_release_index_update(planned, repo_root, profile)
    _plan_release_yaml(planned, repo_root, profile)
    _plan_release_notes(planned, repo_root, profile)
    _plan_npm_publication(planned, repo_root, profile)
    _plan_timing_evidence(planned, repo_root, profile)
    _plan_adapter_artifact_report(planned, repo_root, profile)
    _plan_current_version_fixture(planned, repo_root, profile)

    changed_paths = tuple(
        _repo_relative(path, repo_root)
        for path, content in planned.items()
        if not path.exists() or path.read_text(encoding="utf-8") != content
    )
    if check and changed_paths:
        raise ReleaseProfileError(
            profile.path,
            ["prepare-release would update: " + ", ".join(changed_paths)],
        )
    if not check:
        for path, content in planned.items():
            if path.exists() and path.read_text(encoding="utf-8") == content:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    return PrepareReleaseResult(
        release_tag=tag,
        changed_paths=changed_paths,
    )


def validate_pending_release_artifacts(
    tag: str,
    *,
    root: Path | str = Path("."),
) -> list[str]:
    repo_root = Path(root)
    errors: list[str] = []
    profile = load_release_profile(tag, root=repo_root)
    release_dir = repo_root / "docs" / "releases" / tag
    release_yaml = release_dir / "release.yaml"
    npm_publication = release_dir / "npm-publication.md"
    release_notes = release_dir / "release-notes.md"

    for path in (release_yaml, npm_publication, release_notes):
        if not path.exists():
            errors.append(f"{_repo_relative(path, repo_root)}: missing pending release artifact")

    if release_yaml.exists():
        text = release_yaml.read_text(encoding="utf-8")
        _require_text(errors, release_yaml, repo_root, text, f"version: {profile.release_tag}")
        _require_text(errors, release_yaml, repo_root, text, "publication_status: pending-publication")
        _require_text(errors, release_yaml, repo_root, text, f'  version: "{profile.package_version}"')
        _require_text(errors, release_yaml, repo_root, text, f"  release_tag: {profile.release_tag}")
        _require_text(errors, release_yaml, repo_root, text, f"  bundled_metadata: {profile.adapter_artifacts['metadata_file']}")
    if npm_publication.exists():
        text = npm_publication.read_text(encoding="utf-8")
        _require_text(errors, npm_publication, repo_root, text, "Status: pending-publication")
        _require_text(errors, npm_publication, repo_root, text, "published: false")
        _validate_pending_npm_publication(
            errors,
            npm_publication,
            repo_root,
            text,
            profile,
        )
    if release_notes.exists():
        text = release_notes.read_text(encoding="utf-8")
        marker = _generated_region_start("release-metadata", profile)
        _require_text(errors, release_notes, repo_root, text, marker)
        _require_text(errors, release_notes, repo_root, text, _generated_region_end("release-metadata"))
    return errors


def release_preflight(
    tag: str,
    *,
    root: Path | str = Path("."),
    changed_files: tuple[str, ...] = (),
    check_remote: bool = True,
) -> ReleasePreflightResult:
    repo_root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []

    try:
        profile = load_release_profile(tag, root=repo_root)
    except ReleaseProfileError as exc:
        return ReleasePreflightResult(
            release_tag=tag,
            errors=tuple(exc.errors),
        )

    if not is_routine_release_profile(profile):
        errors.append("release-preflight requires a routine release profile")
    _preflight_package_profile_agreement(errors, repo_root, profile)
    _preflight_release_metadata_pointer(errors, repo_root, profile)
    errors.extend(validate_pending_release_artifacts(tag, root=repo_root))
    _preflight_literal_audit(errors, warnings, repo_root, changed_files=changed_files)
    _preflight_release_output(errors, repo_root)
    _preflight_local_tag(errors, repo_root, tag)
    if check_remote:
        _preflight_remote_tag(errors, warnings, repo_root, tag)

    return ReleasePreflightResult(
        release_tag=tag,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def validate_release_timing_evidence(
    tag: str,
    *,
    root: Path | str = Path("."),
) -> ReleaseTimingValidationResult:
    repo_root = Path(root)
    try:
        profile = load_release_profile(tag, root=repo_root)
    except ReleaseProfileError as exc:
        return ReleaseTimingValidationResult(tag, tuple(exc.errors))

    if profile.evidence.get("timing") != REQUIRED_VALUE:
        return ReleaseTimingValidationResult(tag, ())

    timing_path = repo_root / "docs" / "releases" / tag / "timing.yaml"
    if not timing_path.exists():
        return ReleaseTimingValidationResult(
            tag,
            (f"{_repo_relative(timing_path, repo_root)}: missing required timing evidence",),
        )

    try:
        data = _load_yaml_subset(timing_path, "release timing evidence")
    except ReleaseProfileError as exc:
        return ReleaseTimingValidationResult(tag, tuple(exc.errors))

    errors: list[str] = []
    warnings: list[str] = []
    schema_version = data.get("schema_version")
    release_tag = data.get("release_tag")
    release_profile = data.get("release_profile")
    phases = data.get("phases")
    checks = data.get("checks", [])

    if schema_version != "release-timing-v1":
        errors.append("timing schema_version must be release-timing-v1")
    if release_tag != tag:
        errors.append(f"timing release_tag `{release_tag}` does not match `{tag}`")
    expected_profile_path = f"docs/releases/profiles/{tag}.yaml"
    if release_profile != expected_profile_path:
        errors.append(
            f"timing release_profile `{release_profile}` does not match `{expected_profile_path}`"
        )
    if "created_at" not in data:
        errors.append("timing missing required field: created_at")

    if not isinstance(phases, list):
        errors.append("timing phases must be a list")
        phases = []
    if checks is None:
        checks = []
    if not isinstance(checks, list):
        errors.append("timing checks must be a list")
        checks = []

    seen_phases: set[str] = set()
    for phase in phases:
        if not isinstance(phase, dict):
            errors.append("timing phase must be a mapping")
            continue
        phase_id = phase.get("id")
        if not isinstance(phase_id, str) or not phase_id:
            errors.append("timing phase missing required field: id")
            continue
        if phase_id in seen_phases:
            errors.append(f"duplicate timing phase id: {phase_id}")
        seen_phases.add(phase_id)
        if phase_id not in TIMING_PHASE_IDS:
            errors.append(f"unknown timing phase id: {phase_id}")
        _validate_timing_record(errors, warnings, phase, f"timing phase {phase_id}", phase_id=phase_id)

    for phase_id in REQUIRED_TIMING_PHASES:
        if phase_id not in seen_phases:
            errors.append(f"missing timing phase: {phase_id}")

    for check in checks:
        if not isinstance(check, dict):
            errors.append("timing check must be a mapping")
            continue
        check_id = check.get("id")
        context = f"timing check {check_id}" if isinstance(check_id, str) and check_id else "timing check"
        phase_id = check.get("phase")
        if phase_id not in TIMING_PHASE_IDS:
            errors.append(f"{context} references unknown phase: {phase_id}")
        _validate_timing_record(errors, warnings, check, context, phase_id=phase_id if isinstance(phase_id, str) else None)

    return ReleaseTimingValidationResult(tag, tuple(errors), tuple(warnings))


def validate_release_workflow_parity(root: Path | str = Path(".")) -> list[str]:
    repo_root = Path(root)
    workflow_path = repo_root / ".github" / "workflows" / "release.yml"
    if not workflow_path.exists():
        return [f"{_repo_relative(workflow_path, repo_root)}: release workflow not found"]
    text = workflow_path.read_text(encoding="utf-8")
    errors: list[str] = []
    release_verify_count = text.count("bash scripts/release-verify.sh")
    if release_verify_count == 0:
        errors.append(
            ".github/workflows/release.yml: release workflow must invoke bash scripts/release-verify.sh"
        )
    if 'bash scripts/release-verify.sh "$GITHUB_REF_NAME"' not in text:
        errors.append(
            ".github/workflows/release.yml: release job must delegate readiness to bash scripts/release-verify.sh \"$GITHUB_REF_NAME\""
        )
    if 'bash scripts/release-verify.sh "$tag"' not in text:
        errors.append(
            ".github/workflows/release.yml: npm publication validation must delegate to bash scripts/release-verify.sh \"$tag\""
        )
    forbidden_direct_checks = (
        "python scripts/validate-release.py",
        "python scripts/test-adapter-distribution.py",
        "python scripts/test-npm-package-publication.py",
        "python scripts/build-adapters.py",
        "python scripts/validate-adapters.py",
    )
    for check in forbidden_direct_checks:
        if check in text:
            errors.append(
                f".github/workflows/release.yml: release workflow must not duplicate release gate command directly: {check}"
            )
    return errors


class NetworkPublicEvidenceProvider:
    """Collect public closeout evidence from GitHub, npm, and npx."""

    def __init__(self, *, github_repository: str = "xiongxianfei/rigorloop") -> None:
        self.github_repository = github_repository

    def fetch_github_release_assets(self, *, tag: str) -> tuple[GitHubReleaseAsset, ...]:
        release_url = (
            f"https://api.github.com/repos/{self.github_repository}/releases/tags/"
            f"{urllib.parse.quote(tag, safe='')}"
        )
        data = _read_json_url(release_url, f"GitHub release asset metadata not found for {tag}")
        assets = data.get("assets")
        if not isinstance(assets, list) or not assets:
            raise PublicEvidenceUnavailable(f"GitHub release asset metadata not found for {tag}")

        collected: list[GitHubReleaseAsset] = []
        for item in assets:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            url = item.get("browser_download_url")
            size = item.get("size", 0)
            if not isinstance(name, str) or not isinstance(url, str):
                continue
            collected.append(
                GitHubReleaseAsset(
                    name=name,
                    url=url,
                    size=int(size) if isinstance(size, int) else 0,
                    sha256=_download_sha256(url),
                )
            )
        if not collected:
            raise PublicEvidenceUnavailable(f"GitHub release asset metadata not found for {tag}")
        return tuple(collected)

    def fetch_npm_package_metadata(self, *, package: str, version: str) -> NpmPackageMetadata:
        package_url = f"https://registry.npmjs.org/{urllib.parse.quote(package, safe='')}"
        data = _read_json_url(package_url, f"npm metadata for {package}@{version} not available")
        versions = data.get("versions")
        if not isinstance(versions, dict) or version not in versions:
            raise PublicEvidenceUnavailable(f"npm metadata for {package}@{version} not available")
        record = versions[version]
        if not isinstance(record, dict):
            raise PublicEvidenceUnavailable(f"npm metadata for {package}@{version} not available")
        dist = record.get("dist")
        if not isinstance(dist, dict):
            raise PublicEvidenceUnavailable(f"npm tarball metadata for {package}@{version} not available")
        tarball = dist.get("tarball")
        integrity = dist.get("integrity")
        if not isinstance(tarball, str) or not isinstance(integrity, str):
            raise PublicEvidenceUnavailable(f"npm tarball metadata for {package}@{version} not available")
        shasum = dist.get("shasum")
        times = data.get("time")
        published_at = times.get(version) if isinstance(times, dict) and isinstance(times.get(version), str) else None
        return NpmPackageMetadata(
            package=package,
            version=version,
            tarball_url=tarball,
            integrity=integrity,
            shasum=shasum if isinstance(shasum, str) else None,
            published_at=published_at,
        )

    def run_public_npx_smoke(self, *, command: str, cwd: Path) -> PublicSmokeResult:
        result = subprocess.run(
            command.split(),
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        summary = _first_output_line(result.stdout) or _first_output_line(result.stderr) or "no output"
        return PublicSmokeResult(
            command=command,
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            summary=summary,
        )


def close_release_publication(
    tag: str,
    *,
    root: Path | str = Path("."),
    public_evidence: Path | str | None = None,
    fixture_mode: bool = False,
    provider: PublicEvidenceProvider | None = None,
    check: bool = False,
) -> CloseReleasePublicationResult:
    repo_root = Path(root)
    profile = load_release_profile(tag, root=repo_root)
    evidence_path: Path | None = None
    if fixture_mode:
        if public_evidence is None:
            return CloseReleasePublicationResult(
                tag,
                ("fixture public evidence mode requires --fixture-public-evidence",),
            )
        evidence_path = Path(public_evidence)
        if not evidence_path.exists():
            return CloseReleasePublicationResult(
                tag,
                (f"fixture public evidence not available: {_repo_relative(evidence_path, repo_root)}",),
            )
        try:
            evidence = _load_yaml_subset(evidence_path, "fixture public release evidence")
        except ReleaseProfileError as exc:
            return CloseReleasePublicationResult(tag, tuple(exc.errors))
    else:
        if public_evidence is not None:
            return CloseReleasePublicationResult(
                tag,
                (
                    "manual public evidence cannot satisfy routine closeout; "
                    "collect public evidence through closeout providers or use explicit fixture mode"
                ,),
            )
        try:
            evidence = _collect_public_release_evidence(
                profile,
                provider=provider or NetworkPublicEvidenceProvider(),
                repo_root=repo_root,
            )
        except PublicEvidenceUnavailable as exc:
            return CloseReleasePublicationResult(
                tag,
                (f"public closeout unavailable: {exc}",),
            )

    validation_path = evidence_path or repo_root / "public-closeout-provider"
    errors = _validate_public_release_evidence(evidence, profile, validation_path, repo_root)
    if errors:
        return CloseReleasePublicationResult(tag, tuple(errors))

    npm_publication = repo_root / "docs" / "releases" / tag / "npm-publication.md"
    published_text = _published_npm_publication_text(profile, evidence)
    planned = {npm_publication: published_text}
    changed_paths = tuple(
        _repo_relative(path, repo_root)
        for path, content in planned.items()
        if not path.exists() or path.read_text(encoding="utf-8") != content
    )
    if not check:
        for path, content in planned.items():
            if path.exists() and path.read_text(encoding="utf-8") == content:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    return CloseReleasePublicationResult(tag, (), changed_paths=changed_paths)


def validate_published_release_artifacts(
    tag: str,
    *,
    root: Path | str = Path("."),
) -> list[str]:
    repo_root = Path(root)
    errors: list[str] = []
    profile = load_release_profile(tag, root=repo_root)
    path = repo_root / "docs" / "releases" / tag / "npm-publication.md"
    if not path.exists():
        return [f"{_repo_relative(path, repo_root)}: missing published npm-publication evidence"]
    text = path.read_text(encoding="utf-8")
    _require_text(errors, path, repo_root, text, "Status: published")
    _require_text(errors, path, repo_root, text, "published: true")
    yaml_block = _extract_yaml_fence(errors, path, repo_root, text)
    version_smoke = _parse_section_fields(yaml_block, "version_smoke")
    _validate_published_version_smoke(errors, path, repo_root, version_smoke, profile)
    rows = _parse_published_target_init_smoke(errors, path, repo_root, yaml_block)
    _validate_published_target_rows(errors, path, repo_root, rows, profile)
    _validate_published_table_projection(errors, path, repo_root, text, rows, profile)
    return errors


def _collect_public_release_evidence(
    profile: ReleaseProfile,
    *,
    provider: PublicEvidenceProvider,
    repo_root: Path,
) -> dict[str, Any]:
    github_assets = provider.fetch_github_release_assets(tag=profile.release_tag)
    npm_metadata = provider.fetch_npm_package_metadata(
        package=profile.npm_package,
        version=profile.package_version,
    )
    asset_rows = _public_asset_rows(profile, github_assets)

    smoke_rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="rigorloop-public-closeout-") as tmp:
        smoke_root = Path(tmp)
        version_command = f"npx {profile.npm_package}@{profile.package_version} version"
        version_smoke = provider.run_public_npx_smoke(command=version_command, cwd=smoke_root)
        if version_smoke.exit_code != 0:
            raise PublicEvidenceUnavailable(
                f"public npx version smoke failed for {profile.release_tag}: "
                f"`{version_command}` exited {version_smoke.exit_code}"
            )
        for target in profile.targets:
            command = f"npx {profile.npm_package}@{profile.package_version} init {target}"
            smoke = provider.run_public_npx_smoke(command=command, cwd=smoke_root)
            if smoke.exit_code != 0:
                raise PublicEvidenceUnavailable(
                    f"public npx smoke failed for {target}: `{command}` exited {smoke.exit_code}"
                )
            smoke_rows.append(_public_smoke_row(target, smoke, cwd=smoke_root))

    return {
        "schema_version": "release-public-evidence-v1",
        "release_tag": profile.release_tag,
        "package": npm_metadata.package,
        "version": npm_metadata.version,
        "github_release_url": f"https://github.com/xiongxianfei/rigorloop/releases/tag/{profile.release_tag}",
        "npm_package_url": f"https://www.npmjs.com/package/{profile.npm_package}/v/{profile.package_version}",
        "npm_integrity": npm_metadata.integrity,
        "npm_tarball": npm_metadata.tarball_url,
        "published_at": npm_metadata.published_at or "public registry timestamp unavailable",
        "dist_tag_latest": npm_metadata.version,
        "version_command": version_smoke.command,
        "version_result": "pass",
        "version_output_summary": version_smoke.summary,
        "github_assets": asset_rows,
        "target_init_smoke": smoke_rows,
    }


def _public_asset_rows(
    profile: ReleaseProfile,
    github_assets: tuple[GitHubReleaseAsset, ...],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in profile.targets:
        matches = [
            asset for asset in github_assets
            if target in asset.name and profile.release_tag in asset.name
        ]
        if not matches:
            raise PublicEvidenceUnavailable(
                f"GitHub release asset metadata not found for {profile.release_tag} target {target}"
            )
        if len(matches) > 1:
            raise PublicEvidenceUnavailable(
                f"GitHub release asset metadata is ambiguous for {profile.release_tag} target {target}"
            )
        asset = matches[0]
        if not asset.sha256:
            raise PublicEvidenceUnavailable(
                f"GitHub release asset checksum not available for {profile.release_tag} target {target}"
            )
        rows.append(
            {
                "target": target,
                "url": asset.url,
                "sha256": _normalize_sha256(asset.sha256),
            }
        )
    return rows


def _public_smoke_row(target: str, smoke: PublicSmokeResult, *, cwd: Path) -> dict[str, Any]:
    tree_hashes, file_counts = _public_install_root_evidence(target, cwd)
    if tree_hashes is None:
        tree_hashes = _public_smoke_output_value(smoke, "tree_hashes")
    if file_counts is None:
        file_counts = _public_smoke_output_value(smoke, "file_counts")
    if tree_hashes is None:
        raise PublicEvidenceUnavailable(f"public npx smoke for {target} did not report tree_hashes")
    if file_counts is None:
        raise PublicEvidenceUnavailable(f"public npx smoke for {target} did not report file_counts")
    return {
        "target": target,
        "command": smoke.command,
        "result": "pass",
        "output_summary": smoke.summary,
        "tree_hashes": tree_hashes,
        "file_counts": file_counts,
    }


def _public_install_root_evidence(target: str, cwd: Path) -> tuple[str | None, str | None]:
    tree_values: list[str] = []
    count_values: list[str] = []
    roots = _target_install_roots(target)
    for root_name in roots:
        root_path = cwd / root_name
        if not root_path.exists():
            return None, None
        tree_hash, file_count = _tree_hash_and_file_count(root_path)
        value = f"sha256:{tree_hash}"
        count = str(file_count)
        if len(roots) > 1:
            value = f"{root_name}={value}"
            count = f"{root_name}={count}"
        tree_values.append(value)
        count_values.append(count)
    return ";".join(tree_values), ";".join(count_values)


def _tree_hash_and_file_count(root: Path) -> tuple[str, int]:
    rows: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append((relative, digest))
    manifest = "".join(f"{relative}\t{digest}\n" for relative, digest in rows)
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest(), len(rows)


def _public_smoke_output_value(smoke: PublicSmokeResult, key: str) -> str | None:
    prefix = f"{key}="
    for line in smoke.stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped[len(prefix):].strip()
            if value:
                return value
    return None


def _normalize_sha256(value: str) -> str:
    return value if value.startswith("sha256:") else f"sha256:{value}"


def _validate_public_release_evidence(
    evidence: dict[str, Any],
    profile: ReleaseProfile,
    path: Path,
    repo_root: Path,
) -> list[str]:
    errors: list[str] = []
    prefix = _repo_relative(path, repo_root)
    if evidence.get("schema_version") != "release-public-evidence-v1":
        errors.append(f"{prefix}: schema_version must be release-public-evidence-v1")
    if evidence.get("release_tag") != profile.release_tag:
        errors.append(f"{prefix}: release_tag `{evidence.get('release_tag')}` does not match `{profile.release_tag}`")
    if evidence.get("package") != profile.npm_package:
        errors.append(f"{prefix}: package `{evidence.get('package')}` does not match `{profile.npm_package}`")
    if evidence.get("version") != profile.package_version:
        errors.append(f"{prefix}: version `{evidence.get('version')}` does not match `{profile.package_version}`")
    for field in (
        "github_release_url",
        "npm_package_url",
        "npm_integrity",
        "npm_tarball",
        "published_at",
        "dist_tag_latest",
        "version_command",
        "version_result",
        "version_output_summary",
    ):
        if not isinstance(evidence.get(field), str) or not evidence.get(field):
            errors.append(f"{prefix}: missing required public evidence field: {field}")
    expected_version_command = f"npx {profile.npm_package}@{profile.package_version} version"
    if evidence.get("version_command") != expected_version_command:
        errors.append(f"{prefix}: version smoke has invalid command; expected `{expected_version_command}`")
    if evidence.get("version_result") != "pass":
        errors.append(f"{prefix}: version smoke result must be pass")

    asset_rows = _require_mapping_list(errors, evidence, "github_assets")
    smoke_rows = _require_mapping_list(errors, evidence, "target_init_smoke")
    asset_by_target = _rows_by_target(asset_rows)
    smoke_by_target = _rows_by_target(smoke_rows)
    for target in profile.targets:
        assets = asset_by_target.get(target, [])
        smokes = smoke_by_target.get(target, [])
        if not assets:
            errors.append(f"{prefix}: missing GitHub release asset for target: {target}")
        elif len(assets) > 1:
            errors.append(f"{prefix}: duplicate GitHub release asset for target: {target}")
        else:
            asset = assets[0]
            if not isinstance(asset.get("url"), str) or not asset.get("url", "").startswith("https://"):
                errors.append(f"{prefix}: GitHub release asset {target} missing public URL")
            _validate_sha_values(errors, prefix, target, "archive sha256", str(asset.get("sha256", "")), allow_root_qualified=False)
        if not smokes:
            errors.append(f"{prefix}: missing public npx smoke for target: {target}")
        elif len(smokes) > 1:
            errors.append(f"{prefix}: duplicate public npx smoke for target: {target}")
        else:
            _validate_public_smoke_row(errors, prefix, target, smokes[0], profile)

    for target in sorted(set(asset_by_target) - set(profile.targets)):
        errors.append(f"{prefix}: unknown GitHub release asset target: {target}")
    for target in sorted(set(smoke_by_target) - set(profile.targets)):
        errors.append(f"{prefix}: unknown public npx smoke target: {target}")
    return errors


def _rows_by_target(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_target: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        target = row.get("target")
        if isinstance(target, str):
            by_target.setdefault(target, []).append(row)
    return by_target


def _validate_public_smoke_row(
    errors: list[str],
    prefix: str,
    target: str,
    row: dict[str, Any],
    profile: ReleaseProfile,
) -> None:
    expected_command = f"npx {profile.npm_package}@{profile.package_version} init {target}"
    command = row.get("command")
    if command != expected_command:
        errors.append(f"{prefix}: public npx smoke target {target} has invalid command; expected `{expected_command}`")
    if row.get("result") != "pass":
        errors.append(f"{prefix}: public npx smoke target {target} result must be pass")
    if not isinstance(row.get("output_summary"), str) or not row.get("output_summary"):
        errors.append(f"{prefix}: public npx smoke target {target} missing output_summary")
    _validate_sha_values(errors, prefix, target, "tree hash", str(row.get("tree_hashes", "")), allow_root_qualified=True)
    _validate_file_count_values(errors, prefix, target, str(row.get("file_counts", "")))


def _published_npm_publication_text(profile: ReleaseProfile, evidence: dict[str, Any]) -> str:
    asset_by_target = {row["target"]: row for row in _require_mapping_list([], evidence, "github_assets")}
    smoke_by_target = {row["target"]: row for row in _require_mapping_list([], evidence, "target_init_smoke")}
    yaml_block = _published_npm_publication_yaml(profile, evidence, asset_by_target, smoke_by_target)
    table_rows = "\n".join(
        _published_table_row(profile, target, asset_by_target[target], smoke_by_target[target])
        for target in profile.targets
    )
    return (
        f"# npm publication evidence for {profile.release_tag}\n\n"
        "Status: published\n\n"
        "This file is generated by `close-release-publication` from public GitHub, npm, and npx evidence.\n\n"
        "```yaml\n"
        f"{yaml_block}"
        "```\n\n"
        "| Target | Command | npm version | Package source | Public archive URL | Installed root(s) | Tree hash value(s) | File count(s) | Command output summary | Archive verified | Tree verified | Result | Closeout blocker |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        f"{table_rows}\n"
    )


def _published_npm_publication_yaml(
    profile: ReleaseProfile,
    evidence: dict[str, Any],
    asset_by_target: dict[str, dict[str, Any]],
    smoke_by_target: dict[str, dict[str, Any]],
) -> str:
    target_rows = "\n".join(
        _published_target_init_smoke_yaml(profile, target, asset_by_target[target], smoke_by_target[target])
        for target in profile.targets
    )
    return (
        "publication:\n"
        f"  package: \"{profile.npm_package}\"\n"
        f"  version: \"{profile.package_version}\"\n"
        f"  release_tag: \"{profile.release_tag}\"\n"
        "  mode: \"trusted-publishing\"\n"
        "  status: \"published\"\n"
        "\n"
        "github:\n"
        f"  release_url: \"{evidence['github_release_url']}\"\n"
        "\n"
        "npm:\n"
        "  published: true\n"
        f"  package_url: \"{evidence['npm_package_url']}\"\n"
        f"  published_at: \"{evidence['published_at']}\"\n"
        f"  dist_tag_latest: \"{evidence['dist_tag_latest']}\"\n"
        f"  integrity: \"{evidence['npm_integrity']}\"\n"
        f"  tarball: \"{evidence['npm_tarball']}\"\n"
        "\n"
        "version_smoke:\n"
        f"  command: \"{evidence['version_command']}\"\n"
        f"  result: \"{evidence['version_result']}\"\n"
        f"  output_summary: \"{evidence['version_output_summary']}\"\n"
        "\n"
        "target_init_smoke:\n"
        f"{target_rows}"
    )


def _published_target_init_smoke_yaml(
    profile: ReleaseProfile,
    target: str,
    asset: dict[str, Any],
    smoke: dict[str, Any],
) -> str:
    return (
        f"  {target}:\n"
        f"    command: \"{smoke['command']}\"\n"
        f"    npm_version: \"{profile.package_version}\"\n"
        "    package_source: \"npm public registry\"\n"
        f"    target: \"{target}\"\n"
        f"    official_archive_url: \"{asset['url']}\"\n"
        f"    archive_sha256: \"{asset['sha256']}\"\n"
        f"    installed_roots: \"{';'.join(_target_install_roots(target))}\"\n"
        f"    tree_hashes: \"{smoke['tree_hashes']}\"\n"
        f"    file_counts: \"{smoke['file_counts']}\"\n"
        f"    command_output_summary: \"{smoke['output_summary']}\"\n"
        "    archive_sha256_verified: true\n"
        "    tree_hash_verified: true\n"
        "    result: \"pass\"\n"
        "    closeout_blocker: \"none\"\n"
        "    post_publish_closeout_blocked: false\n"
    )


def _published_table_row(
    profile: ReleaseProfile,
    target: str,
    asset: dict[str, Any],
    smoke: dict[str, Any],
) -> str:
    return (
        f"| {target} | `{smoke['command']}` | `{profile.package_version}` | npm public registry "
        f"| {asset['url']} | {';'.join(_target_install_roots(target))} | {smoke['tree_hashes']} "
        f"| {smoke['file_counts']} | {smoke['output_summary']} | true | true | pass | none |"
    )


def _parse_section_fields(yaml_block: str, section_name: str) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    in_section = False
    for raw_line in yaml_block.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if indent == 0:
            if in_section:
                break
            in_section = line == f"{section_name}:"
            continue
        if in_section and indent == 2 and ":" in line:
            key, raw_value = line.split(":", 1)
            value = raw_value.strip()
            if value:
                fields[key.strip()] = _parse_scalar(value)
    return fields


def _parse_published_target_init_smoke(
    errors: list[str],
    path: Path,
    repo_root: Path,
    yaml_block: str,
) -> tuple[PendingTargetSmoke, ...]:
    return _parse_pending_target_init_smoke(errors, path, repo_root, yaml_block)


def _validate_published_version_smoke(
    errors: list[str],
    path: Path,
    repo_root: Path,
    fields: dict[str, Any],
    profile: ReleaseProfile,
) -> None:
    expected_command = f"npx {profile.npm_package}@{profile.package_version} version"
    command = fields.get("command")
    if command != expected_command:
        errors.append(f"{_repo_relative(path, repo_root)}: version smoke has invalid command; expected `{expected_command}`")
    if fields.get("result") != "pass":
        errors.append(f"{_repo_relative(path, repo_root)}: version smoke result must be pass")
    if not isinstance(fields.get("output_summary"), str) or not fields.get("output_summary"):
        errors.append(f"{_repo_relative(path, repo_root)}: version smoke missing output_summary")


def _validate_published_target_rows(
    errors: list[str],
    path: Path,
    repo_root: Path,
    rows: tuple[PendingTargetSmoke, ...],
    profile: ReleaseProfile,
) -> None:
    rows_by_target: dict[str, list[PendingTargetSmoke]] = {}
    expected_targets = set(profile.targets)
    for row in rows:
        rows_by_target.setdefault(row.target, []).append(row)
        if row.target not in expected_targets:
            errors.append(f"{_repo_relative(path, repo_root)}: published npm-publication target_init_smoke unknown target: {row.target}")
    for target in profile.targets:
        target_rows = rows_by_target.get(target, [])
        if not target_rows:
            errors.append(f"{_repo_relative(path, repo_root)}: published npm-publication target_init_smoke missing target: {target}")
            continue
        if len(target_rows) > 1:
            errors.append(f"{_repo_relative(path, repo_root)}: published npm-publication target_init_smoke duplicate target: {target}")
            continue
        _validate_published_target_row(errors, path, repo_root, target_rows[0], target, profile)


def _validate_published_target_row(
    errors: list[str],
    path: Path,
    repo_root: Path,
    row: PendingTargetSmoke,
    expected_target: str,
    profile: ReleaseProfile,
) -> None:
    prefix = _repo_relative(path, repo_root)
    fields = row.fields
    expected_command = f"npx {profile.npm_package}@{profile.package_version} init {expected_target}"
    if fields.get("target") != expected_target:
        errors.append(f"{prefix}: published npm-publication target {expected_target} records mismatched target `{fields.get('target')}`")
    if fields.get("command") != expected_command:
        errors.append(f"{prefix}: published npm-publication target {expected_target} has invalid command; expected `{expected_command}`")
    if fields.get("npm_version") != profile.package_version:
        errors.append(f"{prefix}: published npm-publication target {expected_target} has invalid npm_version")
    if fields.get("result") != "pass":
        errors.append(f"{prefix}: published npm-publication target {expected_target} result must be pass")
    if fields.get("closeout_blocker") != "none":
        errors.append(f"{prefix}: published npm-publication target {expected_target} closeout_blocker must be none")
    if fields.get("post_publish_closeout_blocked") is not False:
        errors.append(f"{prefix}: published npm-publication target {expected_target} must set post_publish_closeout_blocked false")
    if fields.get("archive_sha256_verified") is not True:
        errors.append(f"{prefix}: published npm-publication target {expected_target} archive_sha256_verified must be true")
    if fields.get("tree_hash_verified") is not True:
        errors.append(f"{prefix}: published npm-publication target {expected_target} tree_hash_verified must be true")
    _validate_sha_values(errors, prefix, expected_target, "archive sha256", str(fields.get("archive_sha256", "")), allow_root_qualified=False)
    _validate_sha_values(errors, prefix, expected_target, "tree hash", str(fields.get("tree_hashes", "")), allow_root_qualified=True)
    _validate_file_count_values(errors, prefix, expected_target, str(fields.get("file_counts", "")))


def _validate_sha_values(
    errors: list[str],
    prefix: str,
    target: str,
    field_name: str,
    value: str,
    *,
    allow_root_qualified: bool,
) -> None:
    if not value:
        errors.append(f"{prefix}: target {target} missing {field_name}")
        return
    for item in value.split(";"):
        item = item.strip()
        if allow_root_qualified and "=" in item:
            _, item = item.split("=", 1)
            item = item.strip()
        if not item.startswith("sha256:"):
            errors.append(f"{prefix}: target {target} {field_name} must use sha256:<hex> form")


def _validate_file_count_values(errors: list[str], prefix: str, target: str, value: str) -> None:
    if not value:
        errors.append(f"{prefix}: target {target} missing file count")
        return
    for item in value.split(";"):
        item = item.strip()
        if "=" in item:
            _, item = item.split("=", 1)
            item = item.strip()
        if not item.isdigit():
            errors.append(f"{prefix}: target {target} file count must be numeric")


def _validate_published_table_projection(
    errors: list[str],
    path: Path,
    repo_root: Path,
    text: str,
    rows: tuple[PendingTargetSmoke, ...],
    profile: ReleaseProfile,
) -> None:
    table_rows = _parse_pending_table_rows(text)
    if not table_rows:
        errors.append(f"{_repo_relative(path, repo_root)}: missing published npm-publication target table")
        return
    rows_by_target = {row.target: row for row in rows}
    table_by_target = {row["target"]: row for row in table_rows}
    for target in profile.targets:
        table_row = table_by_target.get(target)
        yaml_row = rows_by_target.get(target)
        if table_row is None or yaml_row is None:
            continue
        comparisons = (
            ("command", table_row["command"], yaml_row.fields.get("command")),
            ("npm_version", table_row["npm_version"], yaml_row.fields.get("npm_version")),
            ("result", table_row["result"], yaml_row.fields.get("result")),
            ("closeout_blocker", table_row["closeout_blocker"], yaml_row.fields.get("closeout_blocker")),
        )
        for field, table_value, yaml_value in comparisons:
            if table_value != yaml_value:
                errors.append(
                    f"{_repo_relative(path, repo_root)}: published npm-publication target {target} table projection mismatch for {field}: "
                    f"table `{table_value}` yaml `{yaml_value}`"
                )


def _validate_timing_record(
    errors: list[str],
    warnings: list[str],
    record: dict[str, Any],
    context: str,
    *,
    phase_id: str | None,
) -> None:
    command = record.get("command")
    if not isinstance(command, str) or not command:
        errors.append(f"{context} missing required field: command")

    if "duration_seconds" not in record:
        errors.append(f"{context} missing required field: duration_seconds")
    else:
        duration = _coerce_duration_seconds(record.get("duration_seconds"))
        if duration is None:
            errors.append(f"{context} duration_seconds must be a non-negative number")
        elif phase_id in TIMING_DURATION_TARGET_SECONDS and duration > TIMING_DURATION_TARGET_SECONDS[phase_id]:
            warnings.append(
                f"{context} duration_seconds {duration:g} exceeds first-slice target "
                f"{TIMING_DURATION_TARGET_SECONDS[phase_id]:g}; warning only"
            )

    result = record.get("result")
    if not isinstance(result, str) or not result:
        errors.append(f"{context} missing required field: result")
    elif result not in TIMING_RESULTS:
        errors.append(f"unknown timing result: {result}")


def _coerce_duration_seconds(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        duration = float(value)
    elif isinstance(value, str):
        try:
            duration = float(value)
        except ValueError:
            return None
    else:
        return None
    if duration < 0:
        return None
    return duration


def discover_changed_files(root: Path | str = Path(".")) -> tuple[str, ...]:
    repo_root = Path(root)
    git_root = _run_git(repo_root, "rev-parse", "--show-toplevel")
    if git_root.returncode != 0:
        raise ReleasePreflightChangedFilesError(
            "release preflight could not derive changed files; run in a Git working tree "
            "or pass --changed-file explicitly for fixture mode"
        )

    changed: list[str] = []
    commands = (
        ("diff", "--name-only", "--cached", "--diff-filter=ACMRTUXB"),
        ("diff", "--name-only", "--diff-filter=ACMRTUXB"),
        ("ls-files", "--others", "--exclude-standard"),
    )
    for command in commands:
        result = _run_git(repo_root, *command)
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
            raise ReleasePreflightChangedFilesError(
                f"release preflight could not derive changed files: {detail}"
            )
        changed.extend(line.strip() for line in result.stdout.splitlines() if line.strip())

    deduped: list[str] = []
    seen: set[str] = set()
    for file_path in changed:
        normalized = Path(file_path).as_posix()
        if normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return tuple(deduped)


def _read_json_url(url: str, unavailable_message: str) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise PublicEvidenceUnavailable(f"{unavailable_message}: {exc}") from exc
    if not isinstance(data, dict):
        raise PublicEvidenceUnavailable(unavailable_message)
    return data


def _download_sha256(url: str) -> str:
    digest = hashlib.sha256()
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
    except (OSError, urllib.error.URLError) as exc:
        raise PublicEvidenceUnavailable(f"GitHub release asset checksum not available for {url}: {exc}") from exc
    return f"sha256:{digest.hexdigest()}"


def _first_output_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _current_package_version(repo_root: Path) -> str | None:
    package_json_path = repo_root / "packages" / "rigorloop" / "package.json"
    if not package_json_path.exists():
        return None
    data = json.loads(package_json_path.read_text(encoding="utf-8"))
    version = data.get("version")
    return version if isinstance(version, str) else None


def _plan_package_json_update(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    package_json_path = repo_root / "packages" / "rigorloop" / "package.json"
    data: dict[str, Any] = {}
    if package_json_path.exists():
        data = json.loads(package_json_path.read_text(encoding="utf-8"))
    data["name"] = profile.npm_package
    data["version"] = profile.package_version
    planned[package_json_path] = json.dumps(data, indent=2) + "\n"


def _plan_package_readme_update(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
    *,
    current_version: str | None,
) -> None:
    readme_path = repo_root / "packages" / "rigorloop" / "README.md"
    if readme_path.exists():
        text = readme_path.read_text(encoding="utf-8")
    else:
        text = "# @xiongxianfei/rigorloop\n\n"
    if current_version:
        text = text.replace(f"{profile.npm_package}@{current_version}", f"{profile.npm_package}@{profile.package_version}")
        text = text.replace(f"rigorloop-adapter-codex-v{current_version}.zip", f"rigorloop-adapter-codex-{profile.release_tag}.zip")
        text = text.replace(f"rigorloop-adapter-claude-v{current_version}.zip", f"rigorloop-adapter-claude-{profile.release_tag}.zip")
        text = text.replace(f"rigorloop-adapter-opencode-v{current_version}.zip", f"rigorloop-adapter-opencode-{profile.release_tag}.zip")
    planned[readme_path] = text


def _plan_release_index_update(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    index_path = repo_root / "packages" / "rigorloop" / "dist" / "metadata" / "releases.json"
    data: dict[str, Any] = {"schema_version": 1, "releases": {}}
    if index_path.exists():
        data = json.loads(index_path.read_text(encoding="utf-8"))
    releases = data.setdefault("releases", {})
    if not isinstance(releases, dict):
        releases = {}
        data["releases"] = releases
    releases[profile.release_tag] = {
        "source_repository": "xiongxianfei/rigorloop",
        "release_tag": profile.release_tag,
        "bundled_metadata": profile.adapter_artifacts["metadata_file"],
        "bundled_metadata_sha256": "pending",
    }
    planned[index_path] = json.dumps(data, indent=2, sort_keys=True) + "\n"


def _plan_release_yaml(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    release_path = repo_root / "docs" / "releases" / profile.release_tag / "release.yaml"
    target_lines = "\n".join(f"  - {target}" for target in profile.targets)
    smoke_lines = "\n".join(
        (
            f"  {target}:\n"
            "    result: pending\n"
            "    tool_version: \"packed-package\"\n"
            f"    evidence: \"Pending packed-package smoke for {profile.release_tag} {target}.\"\n"
            "    reason: \"pending release verification\"\n"
            "    owner: maintainer"
        )
        for target in profile.targets
    )
    planned[release_path] = (
        f"version: {profile.release_tag}\n"
        "release_type: final\n"
        "publication_status: pending-publication\n"
        "manifest_version: pending\n"
        "\n"
        "supported_tools:\n"
        f"{target_lines}\n"
        "\n"
        "smoke:\n"
        f"{smoke_lines}\n"
        "\n"
        "validation:\n"
        "  generated_sync: pending\n"
        "  release_notes_consistency: pending\n"
        "  placeholder_release_check: pending\n"
        "  security: pending\n"
        "  adapter_archives: pending\n"
        "  adapter_artifact_metadata: pending\n"
        "  npm_publication_evidence: pending\n"
        "\n"
        "npm_package:\n"
        f"  name: \"{profile.npm_package}\"\n"
        f"  version: \"{profile.package_version}\"\n"
        f"  release_tag: {profile.release_tag}\n"
        "\n"
        "adapter_release:\n"
        f"  tag: {profile.release_tag}\n"
        f"  bundled_metadata: {profile.adapter_artifacts['metadata_file']}\n"
    )


def _plan_release_notes(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    notes_path = repo_root / "docs" / "releases" / profile.release_tag / "release-notes.md"
    generated = _release_notes_generated_block(profile)
    if notes_path.exists():
        text = notes_path.read_text(encoding="utf-8")
        text = _replace_or_append_generated_region(text, "release-metadata", profile, generated)
    else:
        text = (
            f"# RigorLoop {profile.release_tag}\n\n"
            "Release narrative pending maintainer notes.\n\n"
            f"{generated}\n"
        )
    planned[notes_path] = text


def _plan_npm_publication(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    path = repo_root / "docs" / "releases" / profile.release_tag / "npm-publication.md"
    yaml_block = _pending_npm_publication_yaml(profile)
    table_rows = "\n".join(
        (
            f"| {target} | `npx {profile.npm_package}@{profile.package_version} init {target} --json` "
            f"| `{profile.package_version}` | pending publication | pending public archive URL | pending | pending | pending | pending live command output summary | pending | pending | pending-publication | live-smoke-pending |"
        )
        for target in profile.targets
    )
    planned[path] = (
        f"# npm publication evidence for {profile.release_tag}\n\n"
        "Status: pending-publication\n\n"
        "This file is generated by `prepare-release` before public GitHub and npm evidence exists. "
        "Publication closeout must replace pending values with public evidence.\n\n"
        "```yaml\n"
        f"{yaml_block}"
        "```\n\n"
        "| Target | Command | npm version | Package source | Public archive URL | Installed root(s) | Tree hash value(s) | File count(s) | Command output summary | Archive verified | Tree verified | Result | Closeout blocker |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        f"{table_rows}\n"
    )


def _plan_timing_evidence(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    path = repo_root / "docs" / "releases" / profile.release_tag / "timing.yaml"
    planned[path] = (
        "schema_version: release-timing-v1\n"
        f"release_tag: {profile.release_tag}\n"
        f"release_profile: docs/releases/profiles/{profile.release_tag}.yaml\n"
        "created_at: pending\n"
        "\n"
        "phases:\n"
        "  - id: prepare_release\n"
        f"    command: python scripts/prepare-release.py {profile.release_tag}\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "  - id: preflight\n"
        f"    command: python scripts/release-preflight.py {profile.release_tag}\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "  - id: local_release_verify\n"
        f"    command: bash scripts/release-verify.sh {profile.release_tag}\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "  - id: ci_release_verify\n"
        f"    command: bash scripts/release-verify.sh {profile.release_tag}\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "  - id: publication_wait\n"
        "    command: external GitHub and npm publication wait\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "  - id: public_closeout\n"
        f"    command: python scripts/close-release-publication.py {profile.release_tag}\n"
        "    duration_seconds: 0\n"
        "    result: pending\n"
        "\n"
        "checks: []\n"
    )


def _plan_adapter_artifact_report(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    path = repo_root / "docs" / "reports" / "adapter-artifacts" / "releases" / f"{profile.release_tag}.yaml"
    artifacts = "\n".join(
        (
            f"  - adapter: {target}\n"
            f"    archive: rigorloop-adapter-{target}-{profile.release_tag}.zip\n"
            "    sha256: pending\n"
            f"    install_root: {_target_install_root(target)}\n"
            "    result: pending"
        )
        for target in profile.targets
    )
    planned[path] = (
        "schema_version: 1\n"
        "\n"
        "release:\n"
        f"  version: {profile.release_tag}\n"
        "  source_commit: pending\n"
        "  date: pending\n"
        "\n"
        "generator:\n"
        f"  command: \"python scripts/build-adapters.py --version {profile.release_tag} --output-dir <release-output-dir>\"\n"
        "  source_skills: \"skills/\"\n"
        "  manifest: \"dist/adapters/manifest.yaml\"\n"
        "\n"
        "artifacts:\n"
        f"{artifacts}\n"
        "\n"
        "validation:\n"
        f"  command: \"python scripts/validate-adapters.py --root <release-output-dir> --version {profile.release_tag}\"\n"
        "  result: pending\n"
    )


def _plan_current_version_fixture(
    planned: dict[Path, str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    path = repo_root / "tests" / "fixtures" / "release-transaction" / "current-version.json"
    data = {
        "schema_version": "release-current-version-fixture-v1",
        "release_tag": profile.release_tag,
        "package_version": profile.package_version,
        "npm_package": profile.npm_package,
        "targets": list(profile.targets),
        "release_profile": _repo_relative(profile.path, repo_root),
    }
    planned[path] = json.dumps(data, indent=2, sort_keys=True) + "\n"


def _pending_npm_publication_yaml(profile: ReleaseProfile) -> str:
    rows = "\n".join(
        _pending_target_init_smoke_yaml(profile, target)
        for target in profile.targets
    )
    return (
        "publication:\n"
        f"  package: \"{profile.npm_package}\"\n"
        f"  version: \"{profile.package_version}\"\n"
        f"  release_tag: \"{profile.release_tag}\"\n"
        "  source_commit: \"pending\"\n"
        "  mode: \"trusted-publishing\"\n"
        "\n"
        "workflow:\n"
        "  release_workflow: \".github/workflows/release.yml\"\n"
        "  published_by_workflow: true\n"
        "  unsupported_tags_rejected: true\n"
        "\n"
        "tarball:\n"
        f"  filename: \"xiongxianfei-rigorloop-{profile.package_version}.tgz\"\n"
        "  sha256: \"pending\"\n"
        "  pack_command: \"npm pack --prefix packages/rigorloop\"\n"
        "  content_check: \"pending\"\n"
        "  smoke_result: \"pending\"\n"
        "\n"
        "trusted_publishing:\n"
        "  configured: true\n"
        "  workflow: \".github/workflows/release.yml\"\n"
        "  id_token_write: true\n"
        "\n"
        "bootstrap:\n"
        "  used: false\n"
        "  approving_maintainer: null\n"
        "  publish_command: null\n"
        "\n"
        "npm:\n"
        "  published: false\n"
        "  package_url: \"pending\"\n"
        "  published_at: \"pending\"\n"
        "  dist_tag_latest: \"pending\"\n"
        "  integrity: \"pending\"\n"
        "  tarball: \"pending\"\n"
        "\n"
        "target_init_smoke:\n"
        f"{rows}"
    )


def _pending_target_init_smoke_yaml(profile: ReleaseProfile, target: str) -> str:
    roots = _target_install_roots(target)
    root_lines = "\n".join(f"      - \"{root}\"" for root in roots)
    if target == "opencode":
        tree_hashes = (
            "      - \".opencode/skills=<pending skills tree sha256>\"\n"
            "      - \".opencode/commands=<pending commands tree sha256>\""
        )
        file_counts = (
            "      - \".opencode/skills=<pending skills file count>\"\n"
            "      - \".opencode/commands=<pending commands file count>\""
        )
    else:
        tree_hashes = "      - \"<pending live tree sha256>\""
        file_counts = "      - \"<pending live file count>\""
    return (
        f"  {target}:\n"
        f"    command: \"npx {profile.npm_package}@{profile.package_version} init {target} --json\"\n"
        f"    npm_version: \"{profile.package_version}\"\n"
        "    temp_project: \"pending\"\n"
        "    package_source: \"pending publication\"\n"
        f"    target: \"{target}\"\n"
        "    official_archive_url: \"<pending public archive URL>\"\n"
        "    installed_roots:\n"
        f"{root_lines}\n"
        "    tree_hashes:\n"
        f"{tree_hashes}\n"
        "    file_counts:\n"
        f"{file_counts}\n"
        "    command_output_summary: \"<pending live command output summary>\"\n"
        "    archive_sha256_verified: \"pending\"\n"
        "    tree_hash_verified: \"pending\"\n"
        "    result: \"pending-publication\"\n"
        "    closeout_blocker: \"live-smoke-pending\"\n"
        "    post_publish_closeout_blocked: true\n"
    )


def _release_notes_generated_block(profile: ReleaseProfile) -> str:
    targets = ", ".join(profile.targets)
    return (
        f"{_generated_region_start('release-metadata', profile)}\n"
        f"- Release profile: `{_repo_relative(profile.path, profile.path.parents[3])}`\n"
        f"- npm package: `{profile.npm_package}@{profile.package_version}`\n"
        f"- Supported targets: {targets}\n"
        f"- Adapter metadata: `{profile.adapter_artifacts['metadata_file']}`\n"
        f"- Pending publication evidence: `docs/releases/{profile.release_tag}/npm-publication.md`\n"
        f"{_generated_region_end('release-metadata')}\n"
    )


def _replace_or_append_generated_region(
    text: str,
    surface: str,
    profile: ReleaseProfile,
    generated: str,
) -> str:
    start_prefix = f"<!-- rigorloop:generated:start release-transaction surface={surface} "
    end = _generated_region_end(surface)
    start_index = text.find(start_prefix)
    if start_index == -1:
        suffix = "" if text.endswith("\n") else "\n"
        return f"{text}{suffix}\n{generated}"
    end_index = text.find(end, start_index)
    if end_index == -1:
        raise ReleaseProfileError(profile.path, [f"generated region {surface} missing end marker"])
    end_index += len(end)
    if end_index < len(text) and text[end_index:end_index + 1] == "\n":
        end_index += 1
    return text[:start_index] + generated + text[end_index:]


def _generated_region_start(surface: str, profile: ReleaseProfile) -> str:
    return (
        "<!-- rigorloop:generated:start release-transaction "
        f"surface={surface} profile={_repo_relative(profile.path, profile.path.parents[3])} -->"
    )


def _generated_region_end(surface: str) -> str:
    return f"<!-- rigorloop:generated:end release-transaction surface={surface} -->"


def _target_install_root(target: str) -> str:
    return _target_install_roots(target)[0]


def _target_install_roots(target: str) -> tuple[str, ...]:
    if target == "codex":
        return (".agents/skills",)
    if target == "claude":
        return (".claude/skills",)
    if target == "opencode":
        return (".opencode/skills", ".opencode/commands")
    return ("pending",)


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _require_text(
    errors: list[str],
    path: Path,
    repo_root: Path,
    text: str,
    needle: str,
) -> None:
    if needle not in text:
        errors.append(f"{_repo_relative(path, repo_root)}: missing {needle}")


def _preflight_package_profile_agreement(
    errors: list[str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    package_json_path = repo_root / "packages" / "rigorloop" / "package.json"
    if not package_json_path.exists():
        errors.append(f"{_repo_relative(package_json_path, repo_root)}: missing required local input")
        return
    try:
        data = json.loads(package_json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{_repo_relative(package_json_path, repo_root)}: could not parse package metadata: {exc}")
        return
    name = data.get("name")
    version = data.get("version")
    if name != profile.npm_package:
        errors.append(
            f"{_repo_relative(package_json_path, repo_root)}: package name `{name}` does not match profile `{profile.npm_package}`"
        )
    if version != profile.package_version:
        errors.append(
            f"{_repo_relative(package_json_path, repo_root)}: package version `{version}` does not match profile `{profile.package_version}`"
        )


def _preflight_release_metadata_pointer(
    errors: list[str],
    repo_root: Path,
    profile: ReleaseProfile,
) -> None:
    metadata_path = repo_root / "packages" / "rigorloop" / "dist" / "metadata" / "releases.json"
    if not metadata_path.exists():
        errors.append(f"{_repo_relative(metadata_path, repo_root)}: missing required local input")
        return
    try:
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{_repo_relative(metadata_path, repo_root)}: could not parse release metadata: {exc}")
        return
    releases = data.get("releases")
    if not isinstance(releases, dict):
        errors.append(f"{_repo_relative(metadata_path, repo_root)}: releases must be a mapping")
        return
    entry = releases.get(profile.release_tag)
    if not isinstance(entry, dict):
        errors.append(f"{_repo_relative(metadata_path, repo_root)}: missing release metadata pointer for {profile.release_tag}")
        return
    bundled_metadata = entry.get("bundled_metadata")
    expected_metadata = profile.adapter_artifacts["metadata_file"]
    if bundled_metadata != expected_metadata:
        errors.append(
            f"{_repo_relative(metadata_path, repo_root)}: metadata pointer `{bundled_metadata}` does not match profile `{expected_metadata}`"
        )
    release_tag = entry.get("release_tag")
    if release_tag != profile.release_tag:
        errors.append(
            f"{_repo_relative(metadata_path, repo_root)}: release metadata tag `{release_tag}` does not match profile `{profile.release_tag}`"
        )


def _preflight_literal_audit(
    errors: list[str],
    warnings: list[str],
    repo_root: Path,
    *,
    changed_files: tuple[str, ...],
) -> None:
    baseline_path = (
        repo_root
        / "docs"
        / "changes"
        / "2026-06-29-release-transaction-automation"
        / "release-literal-audit-baseline.yaml"
    )
    if not baseline_path.exists():
        return
    try:
        baseline = load_literal_audit_baseline_file(
            baseline_path,
            changed_files=changed_files,
        )
    except ReleaseProfileError as exc:
        errors.extend(exc.errors)
        return
    warnings.extend(baseline.warnings)


def _preflight_release_output(errors: list[str], repo_root: Path) -> None:
    release_output = repo_root / "release-output"
    if not release_output.exists():
        return
    if not release_output.is_dir():
        errors.append(f"{_repo_relative(release_output, repo_root)}: release-output path is not a directory")
        return
    if any(release_output.iterdir()):
        errors.append(f"{_repo_relative(release_output, repo_root)}: release-output is not clean")


def _preflight_local_tag(errors: list[str], repo_root: Path, tag: str) -> None:
    if not (repo_root / ".git").exists():
        return
    result = _run_git(repo_root, "show-ref", "--verify", "--quiet", f"refs/tags/{tag}")
    if result.returncode == 0:
        errors.append(f"local tag conflict: {tag}")


def _preflight_remote_tag(
    errors: list[str],
    warnings: list[str],
    repo_root: Path,
    tag: str,
) -> None:
    if not (repo_root / ".git").exists():
        return
    remote = _run_git(repo_root, "remote", "get-url", "origin")
    if remote.returncode != 0:
        return
    result = _run_git(repo_root, "ls-remote", "--tags", "origin", f"refs/tags/{tag}")
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git ls-remote failed"
        warnings.append(f"remote tag state unreachable for {tag}: {detail}")
        return
    if result.stdout.strip():
        errors.append(f"remote tag conflict: {tag}")


def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ("git", "-C", str(repo_root), *args),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _validate_pending_npm_publication(
    errors: list[str],
    path: Path,
    repo_root: Path,
    text: str,
    profile: ReleaseProfile,
) -> None:
    yaml_block = _extract_yaml_fence(errors, path, repo_root, text)
    rows = _parse_pending_target_init_smoke(errors, path, repo_root, yaml_block)
    _validate_pending_target_rows(errors, path, repo_root, rows, profile)
    _validate_pending_table_projection(errors, path, repo_root, text, rows, profile)


def _extract_yaml_fence(
    errors: list[str],
    path: Path,
    repo_root: Path,
    text: str,
) -> str:
    start = text.find("```yaml\n")
    if start == -1:
        errors.append(f"{_repo_relative(path, repo_root)}: missing pending npm-publication yaml block")
        return ""
    content_start = start + len("```yaml\n")
    end = text.find("\n```", content_start)
    if end == -1:
        errors.append(f"{_repo_relative(path, repo_root)}: pending npm-publication yaml block missing closing fence")
        return ""
    return text[content_start:end]


def _parse_pending_target_init_smoke(
    errors: list[str],
    path: Path,
    repo_root: Path,
    yaml_block: str,
) -> tuple[PendingTargetSmoke, ...]:
    rows: list[PendingTargetSmoke] = []
    in_target_init_smoke = False
    current_target: str | None = None
    current_fields: dict[str, Any] = {}

    def finish_current() -> None:
        nonlocal current_target, current_fields
        if current_target is not None:
            rows.append(PendingTargetSmoke(target=current_target, fields=dict(current_fields)))
        current_target = None
        current_fields = {}

    for line_number, raw_line in enumerate(yaml_block.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if not in_target_init_smoke:
            if line == "target_init_smoke:" and indent == 0:
                in_target_init_smoke = True
            continue

        if indent == 0:
            finish_current()
            break
        if indent == 2 and line.endswith(":"):
            finish_current()
            current_target = line[:-1].strip()
            if not current_target:
                errors.append(f"{_repo_relative(path, repo_root)}: pending target_init_smoke has empty target at yaml line {line_number}")
            continue
        if indent == 4 and current_target is not None:
            if ":" not in line:
                errors.append(f"{_repo_relative(path, repo_root)}: pending target_init_smoke target {current_target} has malformed field at yaml line {line_number}")
                continue
            key, raw_value = line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            if not key:
                errors.append(f"{_repo_relative(path, repo_root)}: pending target_init_smoke target {current_target} has empty field at yaml line {line_number}")
                continue
            if value:
                current_fields[key] = _parse_scalar(value)
            continue
        if indent >= 6:
            continue
        errors.append(f"{_repo_relative(path, repo_root)}: pending target_init_smoke has unsupported yaml line {line_number}: {line}")

    if in_target_init_smoke:
        finish_current()
    else:
        errors.append(f"{_repo_relative(path, repo_root)}: pending npm-publication yaml missing target_init_smoke")
    return tuple(rows)


def _validate_pending_target_rows(
    errors: list[str],
    path: Path,
    repo_root: Path,
    rows: tuple[PendingTargetSmoke, ...],
    profile: ReleaseProfile,
) -> None:
    rows_by_target: dict[str, list[PendingTargetSmoke]] = {}
    expected_targets = set(profile.targets)
    for row in rows:
        rows_by_target.setdefault(row.target, []).append(row)
        if row.target not in expected_targets:
            errors.append(f"{_repo_relative(path, repo_root)}: pending npm-publication target_init_smoke unknown target: {row.target}")

    for target in profile.targets:
        target_rows = rows_by_target.get(target, [])
        if not target_rows:
            errors.append(f"{_repo_relative(path, repo_root)}: pending npm-publication target_init_smoke missing target: {target}")
            continue
        if len(target_rows) > 1:
            errors.append(f"{_repo_relative(path, repo_root)}: pending npm-publication target_init_smoke duplicate target: {target}")
            continue
        _validate_pending_target_row(errors, path, repo_root, target_rows[0], target, profile)


def _validate_pending_target_row(
    errors: list[str],
    path: Path,
    repo_root: Path,
    row: PendingTargetSmoke,
    expected_target: str,
    profile: ReleaseProfile,
) -> None:
    fields = row.fields
    row_target = fields.get("target")
    if row_target != expected_target:
        errors.append(
            f"{_repo_relative(path, repo_root)}: pending npm-publication target_init_smoke target/command mismatch: "
            f"row target {expected_target} records target `{row_target}`"
        )

    expected_command = f"npx {profile.npm_package}@{profile.package_version} init {expected_target} --json"
    command = fields.get("command")
    if _uses_unpermitted_placeholder(command):
        errors.append(
            f"{_repo_relative(path, repo_root)}: pending npm-publication target {expected_target} uses unpermitted placeholder in command"
        )
    if command != expected_command:
        errors.append(
            f"{_repo_relative(path, repo_root)}: pending npm-publication target {expected_target} has invalid command; "
            f"expected `{expected_command}`"
        )

    npm_version = fields.get("npm_version")
    if _uses_unpermitted_placeholder(npm_version) or npm_version != profile.package_version:
        errors.append(
            f"{_repo_relative(path, repo_root)}: pending npm-publication target {expected_target} has invalid npm_version "
            f"`{npm_version}`; expected `{profile.package_version}`"
        )

    result = fields.get("result")
    if _uses_unpermitted_placeholder(result):
        errors.append(
            f"{_repo_relative(path, repo_root)}: pending npm-publication target {expected_target} uses unpermitted placeholder in result"
        )
    if result != "pending-publication":
        errors.append(
            f"{_repo_relative(path, repo_root)}: pending npm-publication target {expected_target} has invalid result "
            f"`{result}`; expected `pending-publication`"
        )

    if fields.get("post_publish_closeout_blocked") is not True:
        errors.append(
            f"{_repo_relative(path, repo_root)}: pending npm-publication target {expected_target} must set post_publish_closeout_blocked true"
        )


def _uses_unpermitted_placeholder(value: Any) -> bool:
    return isinstance(value, str) and ("<pending" in value or value in {"pending", "<pending>"})


def _validate_pending_table_projection(
    errors: list[str],
    path: Path,
    repo_root: Path,
    text: str,
    rows: tuple[PendingTargetSmoke, ...],
    profile: ReleaseProfile,
) -> None:
    table_rows = _parse_pending_table_rows(text)
    if not table_rows:
        errors.append(f"{_repo_relative(path, repo_root)}: missing pending npm-publication target table")
        return

    yaml_by_target: dict[str, PendingTargetSmoke] = {}
    for row in rows:
        if row.target not in yaml_by_target:
            yaml_by_target[row.target] = row

    table_by_target: dict[str, list[dict[str, str]]] = {}
    expected_targets = set(profile.targets)
    for table_row in table_rows:
        target = table_row["target"]
        table_by_target.setdefault(target, []).append(table_row)
        if target not in expected_targets:
            errors.append(f"{_repo_relative(path, repo_root)}: pending npm-publication table unknown target: {target}")

    for target in profile.targets:
        target_rows = table_by_target.get(target, [])
        if not target_rows:
            errors.append(f"{_repo_relative(path, repo_root)}: pending npm-publication table missing target: {target}")
            continue
        if len(target_rows) > 1:
            errors.append(f"{_repo_relative(path, repo_root)}: pending npm-publication table duplicate target: {target}")
            continue
        yaml_row = yaml_by_target.get(target)
        if yaml_row is None:
            continue
        table_row = target_rows[0]
        comparisons = (
            ("command", table_row["command"], yaml_row.fields.get("command")),
            ("npm_version", table_row["npm_version"], yaml_row.fields.get("npm_version")),
            ("result", table_row["result"], yaml_row.fields.get("result")),
            ("closeout_blocker", table_row["closeout_blocker"], yaml_row.fields.get("closeout_blocker")),
        )
        for field, table_value, yaml_value in comparisons:
            if table_value != yaml_value:
                errors.append(
                    f"{_repo_relative(path, repo_root)}: pending npm-publication target {target} table projection mismatch for {field}: "
                    f"table `{table_value}` yaml `{yaml_value}`"
                )


def _parse_pending_table_rows(text: str) -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    in_table = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("| Target | Command |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) != 13:
            continue
        rows.append(
            {
                "target": cells[0],
                "command": cells[1],
                "npm_version": cells[2],
                "result": cells[11],
                "closeout_blocker": cells[12],
            }
        )
    return tuple(rows)


def _validate_profile_data(path: Path, data: dict[str, Any]) -> ReleaseProfile:
    closed_errors = _closed_vocabulary_errors(data)
    if closed_errors:
        raise ReleaseProfileError(path, closed_errors)

    errors: list[str] = []
    for field in REQUIRED_TOP_LEVEL_FIELDS:
        if field not in data:
            errors.append(f"release profile missing required field: {field}")

    if errors:
        raise ReleaseProfileError(path, errors)

    release_tag = _require_string(errors, data, "release_tag")
    package_version = _require_string(errors, data, "package_version")
    schema_version = _require_string(errors, data, "schema_version")
    release_kind = _require_string(errors, data, "release_kind")
    npm_package = _require_string(errors, data, "npm_package")
    targets = _require_string_list(errors, data, "targets")
    adapter_artifacts = _require_mapping(errors, data, "adapter_artifacts")
    publication = _require_mapping(errors, data, "publication")
    evidence = _require_mapping(errors, data, "evidence")
    validation = _require_mapping(errors, data, "validation")
    owner_decision = data.get("owner_decision")
    if owner_decision is not None and not isinstance(owner_decision, str):
        errors.append("owner_decision must be a string")
        owner_decision = None

    if schema_version and schema_version != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if release_tag and package_version:
        expected_package_version = release_tag.removeprefix("v")
        if package_version != expected_package_version:
            errors.append(
                f"package_version {package_version} does not match release_tag {release_tag}"
            )
    if npm_package and npm_package != EXPECTED_NPM_PACKAGE:
        errors.append(f"npm_package must be {EXPECTED_NPM_PACKAGE}")

    _require_mapping_fields(errors, adapter_artifacts, "adapter_artifacts", REQUIRED_ADAPTER_ARTIFACT_FIELDS)
    _require_mapping_fields(errors, publication, "publication", REQUIRED_PUBLICATION_FIELDS)
    _require_mapping_fields(errors, evidence, "evidence", REQUIRED_EVIDENCE_FIELDS)
    _require_mapping_fields(errors, validation, "validation", REQUIRED_VALIDATION_FIELDS)

    if adapter_artifacts and adapter_artifacts.get("required") is not True:
        errors.append("adapter_artifacts.required must be true")
    for field in REQUIRED_PUBLICATION_FIELDS:
        if publication and publication.get(field) is not True:
            errors.append(f"publication.{field} must be true")
    for field in REQUIRED_EVIDENCE_FIELDS:
        if evidence and evidence.get(field) != REQUIRED_VALUE:
            errors.append(f"evidence.{field} must be required")
    for field in REQUIRED_VALIDATION_FIELDS:
        if validation and validation.get(field) is not True:
            errors.append(f"validation.{field} must be true")

    if release_kind == ROUTINE_RELEASE_KIND and tuple(targets) != ROUTINE_TARGETS:
        errors.append(
            "routine release targets must be codex, claude, opencode in that order"
        )
    if release_kind == SPECIAL_RELEASE_KIND and not owner_decision:
        errors.append("special release requires owner_decision")

    if errors:
        raise ReleaseProfileError(path, errors)

    return ReleaseProfile(
        path=path,
        schema_version=schema_version,
        release_kind=release_kind,
        release_tag=release_tag,
        package_version=package_version,
        npm_package=npm_package,
        targets=tuple(targets),
        adapter_artifacts=dict(adapter_artifacts),
        publication=dict(publication),
        evidence=dict(evidence),
        validation=dict(validation),
        owner_decision=owner_decision,
    )


def _validate_surface_inventory(path: Path, data: dict[str, Any]) -> ReleaseSurfaceInventory:
    errors: list[str] = []
    schema_version = _require_string(errors, data, "schema_version")
    change_id = _require_string(errors, data, "change_id")
    surfaces = _require_mapping_list(errors, data, "surfaces")

    if schema_version and schema_version != "release-surface-inventory-v1":
        errors.append("schema_version must be release-surface-inventory-v1")

    seen_ids: set[str] = set()
    for surface in surfaces:
        surface_id = _require_entry_string(errors, surface, "surface", "id")
        surface_context = f"surface inventory entry {surface_id}" if surface_id else "surface"
        _require_entry_string(errors, surface, surface_context, "path")
        classification = _require_entry_string(
            errors,
            surface,
            surface_context,
            "classification",
        )
        _require_entry_string(errors, surface, surface_context, "expected_owner")
        if surface_id:
            if surface_id in seen_ids:
                errors.append(f"duplicate surface id: {surface_id}")
            seen_ids.add(surface_id)
        if classification and classification not in SURFACE_CLASSIFICATIONS:
            errors.append(f"unknown surface classification: {classification}")
        if surface.get("manual_override") is True and not surface.get("rationale"):
            errors.append(f"manual override requires rationale: {surface_id}")

    if errors:
        raise ReleaseProfileError(path, errors)

    return ReleaseSurfaceInventory(
        path=path,
        schema_version=schema_version,
        change_id=change_id,
        surfaces=tuple(dict(surface) for surface in surfaces),
    )


def _validate_literal_audit_baseline(
    path: Path,
    data: dict[str, Any],
    *,
    changed_files: frozenset[str],
) -> LiteralAuditBaseline:
    errors: list[str] = []
    warnings: list[str] = []
    schema_version = _require_string(errors, data, "schema_version")
    change_id = _require_string(errors, data, "change_id")
    audited_release_tag = _require_string(errors, data, "audited_release_tag")
    release_profile = _require_string(errors, data, "release_profile")
    entries = _require_mapping_list(errors, data, "entries")

    if schema_version and schema_version != "release-literal-audit-baseline-v1":
        errors.append("schema_version must be release-literal-audit-baseline-v1")

    for entry in entries:
        entry_id = _require_entry_string(errors, entry, "literal audit entry", "id")
        entry_context = f"literal audit entry {entry_id}" if entry_id else "literal audit entry"
        literal = _require_entry_string(errors, entry, "literal audit entry", "literal")
        file_path = _require_entry_string(errors, entry, literal or "literal audit entry", "file")
        line = entry.get("line")
        if not isinstance(line, int):
            errors.append(f"literal audit entry line must be an integer: {file_path}")
        classification = _require_entry_string(
            errors,
            entry,
            entry_context,
            "classification",
        )
        expected_owner = _require_entry_string(
            errors,
            entry,
            literal or "literal audit entry",
            "expected_owner",
        )
        disposition = _require_entry_string(
            errors,
            entry,
            literal or "literal audit entry",
            "disposition",
        )
        context = _literal_entry_context(entry)

        if classification and classification not in LITERAL_CLASSIFICATIONS:
            errors.append(f"unknown literal classification: {classification}")
            continue
        if disposition and disposition not in LITERAL_DISPOSITIONS:
            errors.append(f"unknown literal disposition: {disposition}")
            continue
        if classification == "historical-fixture" and not entry.get("rationale"):
            errors.append(f"historical fixture requires rationale: literal={literal} file={file_path}")
        if classification == "generated-current" and not (
            entry.get("release_profile") or entry.get("generated_region")
        ):
            errors.append(
                "generated-current literal requires release_profile or generated_region owner"
            )
        if classification == "unauthorized" and file_path in changed_files:
            errors.append(f"unauthorized changed literal: {context}")
        if classification == "baseline-drift" and disposition == "report-only":
            warnings.append(f"literal audit report-only: {context}")

    if errors:
        raise ReleaseProfileError(path, errors)

    return LiteralAuditBaseline(
        path=path,
        schema_version=schema_version,
        change_id=change_id,
        audited_release_tag=audited_release_tag,
        release_profile=release_profile,
        entries=tuple(dict(entry) for entry in entries),
        warnings=tuple(warnings),
    )


def _closed_vocabulary_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    release_kind = data.get("release_kind")
    if isinstance(release_kind, str) and release_kind not in RELEASE_KINDS:
        errors.append(f"unknown release_kind: {release_kind}")

    targets = data.get("targets")
    if isinstance(targets, list):
        for target in targets:
            if isinstance(target, str) and target not in SUPPORTED_TARGETS:
                errors.append(f"unknown target: {target}")
    return errors


def _require_string(errors: list[str], data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if isinstance(value, str) and value:
        return value
    errors.append(f"{field} must be a non-empty string")
    return ""


def _require_string_list(errors: list[str], data: dict[str, Any], field: str) -> list[str]:
    value = data.get(field)
    if isinstance(value, list) and value and all(isinstance(item, str) for item in value):
        return list(value)
    errors.append(f"{field} must be a non-empty list of strings")
    return []


def _require_mapping(errors: list[str], data: dict[str, Any], field: str) -> dict[str, Any]:
    value = data.get(field)
    if isinstance(value, dict):
        return dict(value)
    errors.append(f"{field} must be a mapping")
    return {}


def _require_mapping_list(errors: list[str], data: dict[str, Any], field: str) -> list[dict[str, Any]]:
    value = data.get(field)
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        return [dict(item) for item in value]
    errors.append(f"{field} must be a list of mappings")
    return []


def _require_entry_string(
    errors: list[str],
    entry: dict[str, Any],
    entry_name: str,
    field: str,
) -> str:
    value = entry.get(field)
    if isinstance(value, str) and value:
        return value
    errors.append(f"{entry_name} missing required field: {field}")
    return ""


def _require_mapping_fields(
    errors: list[str],
    mapping: dict[str, Any],
    prefix: str,
    fields: tuple[str, ...],
) -> None:
    for field in fields:
        if field not in mapping:
            errors.append(f"missing required field: {prefix}.{field}")


def _parse_profile_yaml(text: str) -> dict[str, Any]:
    return _parse_yaml_subset(text)


def _load_yaml_subset(path: Path, label: str) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ReleaseProfileError(path, [f"{label} not found: {path}"]) from exc
    except OSError as exc:
        raise ReleaseProfileError(path, [f"could not read {label}: {exc}"]) from exc
    try:
        return _parse_yaml_subset(text)
    except ValueError as exc:
        raise ReleaseProfileError(path, [f"could not parse {label}: {exc}"]) from exc


def _parse_yaml_subset(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    current_list_item: dict[str, Any] | None = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0:
            if ":" not in line:
                raise ValueError(f"line {line_number} is missing ':'")
            key, raw_value = line.split(":", 1)
            key = key.strip()
            if not key:
                raise ValueError(f"line {line_number} has an empty key")
            value = raw_value.strip()
            if value:
                data[key] = _parse_scalar(value)
                current_key = None
                current_list_item = None
            else:
                data[key] = None
                current_key = key
                current_list_item = None
            continue

        if current_key is None:
            raise ValueError(f"line {line_number} has indented content without a parent key")

        if indent == 4:
            if current_list_item is None:
                raise ValueError(f"line {line_number} has nested content without a list item")
            if ":" not in line:
                raise ValueError(f"line {line_number} is missing ':'")
            key, raw_value = line.split(":", 1)
            key = key.strip()
            if not key:
                raise ValueError(f"line {line_number} has an empty key")
            value = raw_value.strip()
            if not value:
                raise ValueError(f"line {line_number} has an empty mapping value")
            current_list_item[key] = _parse_scalar(value)
            continue

        if indent != 2:
            raise ValueError(f"line {line_number} uses unsupported indentation")

        if line.startswith("- "):
            if data[current_key] is None:
                data[current_key] = []
            if not isinstance(data[current_key], list):
                raise ValueError(f"line {line_number} mixes list and mapping values")
            item_value = line[2:].strip()
            if ":" in item_value:
                key, raw_value = item_value.split(":", 1)
                key = key.strip()
                value = raw_value.strip()
                if not key or not value:
                    raise ValueError(f"line {line_number} has an invalid list mapping")
                current_list_item = {key: _parse_scalar(value)}
                data[current_key].append(current_list_item)
            else:
                current_list_item = None
                data[current_key].append(_parse_scalar(item_value))
            continue

        if ":" not in line:
            raise ValueError(f"line {line_number} is missing ':'")
        if data[current_key] is None:
            data[current_key] = {}
        if not isinstance(data[current_key], dict):
            raise ValueError(f"line {line_number} mixes mapping and list values")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"line {line_number} has an empty key")
        value = raw_value.strip()
        if not value:
            raise ValueError(f"line {line_number} has an empty mapping value")
        data[current_key][key] = _parse_scalar(value)
        current_list_item = None

    return data


def _parse_scalar(value: str) -> str | bool:
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "[]":
        return []
    if value.isdigit():
        return int(value)
    try:
        if "." in value:
            return float(value)
    except ValueError:
        pass
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _literal_entry_context(entry: dict[str, Any]) -> str:
    return (
        f"literal={entry.get('literal')} file={entry.get('file')} "
        f"classification={entry.get('classification')} expected_owner={entry.get('expected_owner')}"
    )
