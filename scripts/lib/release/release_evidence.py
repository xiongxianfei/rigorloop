"""Release-owned evidence shape, publication gate and safety validation."""

from __future__ import annotations

import os
import subprocess
import re

from pathlib import Path

RELEASE_EVIDENCE_REQUIRED_SECTIONS = (
    "Result",
    "Related Lifecycle Evidence",
    "Version Decision",
    "Routine Publish Boundary",
    "Preflight Gate",
    "Package Contents",
    "Publish Event",
    "Registry Verification",
    "Emergency Deferrals",
    "Recovery / Rollback Notes",
    "Follow-up",
    "Evidence Safety Checklist",
)

RELEASE_EVIDENCE_RESULT_FIELDS = (
    "Package",
    "Version",
    "Release type",
    "Routine publish",
    "No new decision introduced",
    "Source commit",
    "Source branch",
    "npm dist-tag",
    "Publish path",
    "Provenance",
    "Status",
)

RELEASE_EVIDENCE_PUBLISH_FIELDS = (
    "Command family",
    "Registry",
    "Package reference",
    "Published at",
    "Dist-tag",
    "Provenance status",
    "Manual fallback reason",
)

ROUTINE_RELEASE_GATE_ITEMS = (
    "clean worktree except intentional release artifacts",
    "release notes or not-required rationale",
    "generated output current",
    "tests / selected CI / broad smoke",
    "package build or pack proof",
    "package preview",
    "local packed-install smoke",
    "no unresolved release blockers",
    "publish path selected",
    "evidence path prepared",
)

ROUTINE_RELEASE_GATE_FINAL_RESULTS = {
    **{item: frozenset(("pass",)) for item in ROUTINE_RELEASE_GATE_ITEMS},
    "release notes or not-required rationale": frozenset(("pass", "not-required")),
}

RELEASE_REGISTRY_ITEMS = (
    "registry version query",
    "dist-tag points correctly",
    "integrity metadata available",
    "fresh registry install smoke",
    "CLI or npx smoke",
)

EMERGENCY_DEFERRABLE_RELEASE_ITEMS = frozenset(("fresh registry install smoke",))

RELEASE_EVIDENCE_STATUSES = frozenset(
    (
        "published",
        "pending-publication",
        "failed-before-publish",
        "failed-during-publish",
        "failed-after-publish",
        "emergency-with-deferred-gate",
        "rolled-back",
        "deprecated",
        "not-published",
    )
)

NON_DEFERRABLE_RELEASE_ITEMS = (
    "release evidence",
    "secret",
    "token",
    "otp",
    "credential",
    "private environment",
    "machine-local",
    "source commit",
    "package version",
    "package name",
    "dist-tag",
    "publish path",
    "registry verification",
    "recovery",
    "follow-up",
)

FORBIDDEN_RELEASE_EVIDENCE_PATTERNS = (
    re.compile(r"(?i)\b(?:NPM_TOKEN|NODE_AUTH_TOKEN|GITHUB_TOKEN|AWS_SECRET_ACCESS_KEY)\s*="),
    re.compile(r"(?i)//registry\.npmjs\.org/:_authToken\s*="),
    re.compile(r"(?i)\bnpm_[A-Za-z0-9]{10,}\b"),
    re.compile(r"(?i)\bOTP\s*[:=]\s*\d{4,}\b"),
    re.compile(r"(?i)\b(?:password|credential|secret)\s*[:=]\s*\S+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:HOME|USER|USERNAME|HOSTNAME)\s*=\s*\S+"),
    re.compile(r"(?:^|[\s`])(?:/home/|/Users/|/tmp/)\S+"),
)

def _markdown_field_value(section: str, label: str) -> str | None:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}:\s*(?P<value>.+?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(section)
    if match is None:
        return None
    return match.group("value").strip()

def _markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        if cells[0].casefold() in {"check", "deferred gate item"}:
            continue
        rows.append(cells)
    return rows

def _table_row_results(section: str, row_label: str) -> list[str]:
    return [
        row[1].strip()
        for row in _markdown_table_rows(section)
        if len(row) >= 2 and row[0].casefold() == row_label.casefold()
    ]

def _is_blank_table_value(value: str) -> bool:
    return not value.strip() or value.strip().casefold() in {"-", "missing", "not-recorded"}

def _is_missing_emergency_deferral_value(value: str) -> bool:
    return _is_blank_table_value(value) or value.strip().casefold() == "not-applicable"

def _validate_emergency_deferrals(section: str) -> list[str]:
    errors: list[str] = []
    deferred_items: list[str] = []
    for row in _markdown_table_rows(section):
        if not row:
            continue
        deferred_item = row[0].strip()
        if not deferred_item or deferred_item.casefold() == "none":
            continue
        normalized = deferred_item.casefold()
        deferred_items.append(normalized)
        if (
            normalized not in EMERGENCY_DEFERRABLE_RELEASE_ITEMS
            or any(term in normalized for term in NON_DEFERRABLE_RELEASE_ITEMS)
        ):
            errors.append(f"emergency deferral '{deferred_item}' is non-deferrable")
        if len(row) < 9:
            errors.append(f"emergency deferral '{deferred_item}' must include all required fields")
            continue
        required_fields = (
            ("approving owner", row[1]),
            ("emergency rationale", row[2]),
            ("reason for deferral", row[3]),
            ("validation impact", row[4]),
            ("risk accepted", row[5]),
            ("follow-up location", row[6]),
            ("deadline or next lifecycle stage", row[7]),
            ("status", row[8]),
        )
        for field_name, value in required_fields:
            if _is_missing_emergency_deferral_value(value):
                errors.append(f"emergency deferral '{deferred_item}' is missing {field_name}")
        if row[8].strip().casefold() != "open":
            errors.append(
                f"emergency deferral '{deferred_item}' status must be open while its result is deferred"
            )
    for deferred_item in set(deferred_items):
        if deferred_items.count(deferred_item) != 1:
            errors.append(
                f"emergency deferral '{deferred_item}' is duplicated; must appear exactly once"
            )
    return errors

def _emergency_deferral_items(section: str) -> list[str]:
    return [
        row[0].strip().casefold()
        for row in _markdown_table_rows(section)
        if row and row[0].strip() and row[0].strip().casefold() != "none"
    ]

def validate_release_evidence_checklist(
    relative_path: Path,
    text: str,
    *,
    require_preflight_pass: bool = True,
) -> list[str]:
    """Validate the shared release-evidence shape and, when requested, its publish gate."""

    errors: list[str] = []
    sections = _parse_sections(text)

    for section_name in RELEASE_EVIDENCE_REQUIRED_SECTIONS:
        body = _get_section(sections, section_name)
        if body is None:
            errors.append(f"release evidence missing required '{section_name}' section")
        elif not body.strip():
            errors.append(f"release evidence required '{section_name}' section must not be empty")

    if re.search(r"<[^>\n]+>", text):
        errors.append("release evidence contains unresolved template placeholder")

    if any(pattern.search(text) for pattern in FORBIDDEN_RELEASE_EVIDENCE_PATTERNS):
        errors.append("release evidence contains forbidden secret or private machine-state marker")

    result_section = _get_section(sections, "Result") or ""
    result_values = {field: _markdown_field_value(result_section, field) for field in RELEASE_EVIDENCE_RESULT_FIELDS}
    for field, value in result_values.items():
        if value is None:
            errors.append(f"release evidence missing Result field '{field}'")
        elif _is_blank_table_value(value):
            errors.append(f"release evidence Result field '{field}' must not be empty")

    publish_section = _get_section(sections, "Publish Event") or ""
    for field in RELEASE_EVIDENCE_PUBLISH_FIELDS:
        value = _markdown_field_value(publish_section, field)
        if value is None:
            errors.append(f"release evidence missing Publish Event field '{field}'")
        elif _is_blank_table_value(value):
            errors.append(f"release evidence Publish Event field '{field}' must not be empty")

    preflight_section = _get_section(sections, "Preflight Gate") or ""
    status = (result_values.get("Status") or "").casefold()
    release_type = (result_values.get("Release type") or "").casefold()
    if status and status not in RELEASE_EVIDENCE_STATUSES:
        errors.append(f"release evidence status '{status}' is not in the supported vocabulary")
    is_emergency = release_type == "emergency" or status == "emergency-with-deferred-gate"
    for gate_item in ROUTINE_RELEASE_GATE_ITEMS:
        gate_results = _table_row_results(preflight_section, gate_item)
        if len(gate_results) != 1:
            errors.append(
                f"routine release gate item '{gate_item}' is missing or duplicated; must appear exactly once"
            )
            continue
        allowed_results = set(ROUTINE_RELEASE_GATE_FINAL_RESULTS[gate_item])
        if not require_preflight_pass and not is_emergency:
            allowed_results.add("pending")
        gate_result = gate_results[0].casefold()
        if gate_result not in allowed_results:
            if allowed_results == {"pass"}:
                errors.append(f"routine release gate item '{gate_item}' must pass before publish")
            else:
                expected = " or ".join(sorted(allowed_results))
                errors.append(
                    f"routine release gate item '{gate_item}' must be {expected} before publish"
                )

    registry_section = _get_section(sections, "Registry Verification") or ""
    registry_results_by_item: dict[str, str] = {}
    for registry_item in RELEASE_REGISTRY_ITEMS:
        registry_results = _table_row_results(registry_section, registry_item)
        if len(registry_results) != 1:
            errors.append(
                f"release registry item '{registry_item}' is missing or duplicated; must appear exactly once"
            )
            continue
        registry_result = registry_results[0].casefold()
        registry_results_by_item[registry_item] = registry_result
        if status in {"published", "emergency-with-deferred-gate"}:
            allowed_registry_results = {"pass"}
        else:
            allowed_registry_results = {"pass", "pending", "not-applicable", "not-run"}
        if (
            status == "emergency-with-deferred-gate"
            and registry_item in EMERGENCY_DEFERRABLE_RELEASE_ITEMS
        ):
            allowed_registry_results.add("deferred")
        if registry_result not in allowed_registry_results:
            expected = " or ".join(sorted(allowed_registry_results))
            errors.append(
                f"post-publish registry verification '{registry_item}' must be {expected}"
            )

    emergency_section = _get_section(sections, "Emergency Deferrals") or ""
    errors.extend(_validate_emergency_deferrals(emergency_section))
    deferral_items = _emergency_deferral_items(emergency_section)
    none_deferral_count = sum(
        1
        for row in _markdown_table_rows(emergency_section)
        if row and row[0].strip().casefold() == "none"
    )
    if deferral_items and none_deferral_count:
        errors.append(
            f"emergency deferral '{deferral_items[0]}' must not coexist with a none sentinel"
        )
    elif not deferral_items and none_deferral_count != 1:
        errors.append("release evidence without deferrals requires exactly one none sentinel")
    deferred_results = {
        item.casefold()
        for item, result in registry_results_by_item.items()
        if result == "deferred"
    }
    for deferred_item in deferred_results:
        if deferral_items.count(deferred_item) != 1:
            errors.append(
                f"deferred result '{deferred_item}' requires exactly one matching emergency deferral"
            )
    for deferred_item in set(deferral_items):
        if deferred_item not in deferred_results:
            errors.append(
                f"emergency deferral '{deferred_item}' has no matching deferred result"
            )
    if status == "emergency-with-deferred-gate" and not deferred_results:
        errors.append("emergency-with-deferred-gate status requires a matching deferred result")
    if not is_emergency and deferral_items:
        errors.append("non-emergency release evidence must not contain emergency deferrals")

    path_version = relative_path.stem
    result_version = (result_values.get("Version") or "").strip()
    accepted_versions = {path_version}
    if path_version.startswith("v"):
        accepted_versions.add(path_version[1:])
    if result_version not in accepted_versions:
        errors.append("release evidence path version must match Result version")

    return errors

def _parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    body: list[str] = []

    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(body).strip("\n")
            current = line[3:].strip()
            body = []
            continue
        if current is not None:
            body.append(line)

    if current is not None:
        sections[current] = "\n".join(body).strip("\n")

    return sections

def _get_section(sections: dict[str, str], name: str) -> str | None:
    if name in sections:
        return sections[name]

    normalized_name = name.casefold()
    for section_name, body in sections.items():
        if section_name.casefold() == normalized_name:
            return body
    return None


def _prepared_ci_release_tag(root: Path, revision: str | None) -> str | None:
    if os.environ.get('RIGORLOOP_CI_WORKSPACE') != str(root.resolve()):
        return None
    output = os.environ.get('RIGORLOOP_CI_CANDIDATE')
    if not output:
        return None
    import tarfile
    from lib.release.release_candidate import CandidateError, ci_subject
    try:
        candidate = ci_subject(Path(output), root)
        if revision is not None and revision != candidate['prepared_commit']:
            raise CandidateError('selected revision differs from prepared candidate')
        return candidate['tag']
    except (CandidateError, OSError, KeyError, TypeError, AttributeError, ValueError,
            subprocess.SubprocessError, tarfile.TarError) as exc:
        raise ValueError('invalid or mismatched prepared CI release context') from exc


def validate_paths(root: Path, paths: list[str], *, revision: str | None = None) -> list[str]:
    from lib.release.release_candidate import local_file
    if not paths:
        return ['release evidence requires explicit paths']
    prepared_tag = _prepared_ci_release_tag(root, revision)
    errors = []
    for raw in paths:
        if not re.fullmatch(r'docs/releases/v[^/]+\.md', raw):
            errors.append('unsupported release evidence path')
            continue
        try:
            path = local_file(root, raw)
            content = path.read_text(encoding='utf-8')
        except (OSError, ValueError, UnicodeError):
            errors.append('missing, unsafe or unreadable release evidence')
            continue
        errors.extend(validate_release_evidence_checklist(Path(raw), content,
            require_preflight_pass=raw != f'docs/releases/{prepared_tag}.md'))
    return errors


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description='Validate explicit current release evidence.')
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args(argv)
    try:
        errors = validate_paths(Path.cwd(), args.paths)
    except ValueError as exc:
        errors = [str(exc)]
    for error in errors:
        print('Release evidence: ' + error)
    if not errors:
        print('Release evidence structure and gate checks passed.')
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
