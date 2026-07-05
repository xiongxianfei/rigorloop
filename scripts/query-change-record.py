#!/usr/bin/env python3
"""Bounded read helper for change-record metadata."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_HELPER = ROOT / "scripts" / "validate-change-metadata.py"
SUPPORTED_QUERIES = {"summary", "artifacts", "validation"}
COMPACT_ARTIFACT_PATH_VAR_KEYS = {
    "proposal",
    "spec",
    "test_spec",
    "architecture",
    "adr",
    "plan",
    "review_log",
    "review_resolution",
    "explain_change",
    "verify",
    "pr",
}
AUTOPROGRESSION_NAMED_RECORDS = (
    "authoring_through_plan_review",
    "implementation_through_verify",
    "review_fix",
)


class QueryShapeError(Exception):
    """Raised when metadata is valid enough to parse but unsafe to query."""


def load_metadata_parser() -> Any:
    spec = importlib.util.spec_from_file_location("change_metadata_validator_for_query", VALIDATION_HELPER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load change metadata parser")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def emit(payload: dict[str, Any], *, exit_code: int = 0) -> int:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return exit_code


def error_payload(code: str, message: str, **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": "error",
        "code": code,
        "message": message,
    }
    payload.update(extra)
    return payload


def usage_error(message: str) -> int:
    return emit(
        error_payload(
            "usage",
            message,
            supported_queries=sorted(SUPPORTED_QUERIES),
        ),
        exit_code=2,
    )


def is_safe_repo_path(value: str) -> bool:
    if not value or value.startswith(("/", "~")) or "\\" in value or "://" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def change_yaml_path(repo_root: Path, change_id: str) -> Path:
    return repo_root / "docs" / "changes" / change_id / "change.yaml"


def metadata_shape(data: dict[str, Any]) -> str:
    if data.get("schema_version") == 2 and "validation_events" in data:
        return "compact"
    return "legacy"


def load_change_metadata(repo_root: Path, change_id: str) -> tuple[Path, dict[str, Any] | None, dict[str, Any] | None]:
    path = change_yaml_path(repo_root, change_id)
    if not path.exists():
        return path, None, error_payload(
            "change-not-found",
            f"change metadata not found for {change_id}",
            change_id=change_id,
            detail_pointers={"expected_change_metadata": repo_relative(path, repo_root)},
        )
    try:
        parser = load_metadata_parser()
        data = parser.load_yaml(path)
    except Exception as exc:  # noqa: BLE001 - diagnostics must not leak parser stack.
        return path, None, error_payload(
            "unsupported-shape",
            "change metadata could not be parsed safely",
            change_id=change_id,
            detail=str(exc),
            detail_pointers={"change_metadata": repo_relative(path, repo_root)},
        )
    if not isinstance(data, dict):
        return path, None, error_payload(
            "unsupported-shape",
            "change metadata root must be an object",
            change_id=change_id,
            detail_pointers={"change_metadata": repo_relative(path, repo_root)},
        )
    shape_error = validate_supported_shape(data, change_id=change_id, metadata_path=path, repo_root=repo_root)
    if shape_error is not None:
        return path, None, shape_error
    return path, data, None


def validate_supported_shape(
    data: dict[str, Any],
    *,
    change_id: str,
    metadata_path: Path,
    repo_root: Path,
) -> dict[str, Any] | None:
    try:
        paths = artifact_paths(data)
    except QueryShapeError as exc:
        return error_payload(
            "unsupported-shape",
            "change metadata contains unsupported artifact path metadata",
            change_id=change_id,
            detail=str(exc),
            detail_pointers={"change_metadata": repo_relative(metadata_path, repo_root)},
        )
    for path in paths:
        if not is_safe_repo_path(path):
            return error_payload(
                "unsupported-shape",
                "change metadata contains an unsafe artifact path",
                change_id=change_id,
                path=path,
                detail_pointers={"change_metadata": repo_relative(metadata_path, repo_root)},
            )
    for event in validation_events(data):
        transcript = event_transcript(event)
        if transcript is not None and not is_safe_repo_path(transcript.split("#", 1)[0]):
            return error_payload(
                "unsupported-shape",
                "change metadata contains an unsafe transcript pointer",
                change_id=change_id,
                path=transcript,
                detail_pointers={"change_metadata": repo_relative(metadata_path, repo_root)},
            )
    return None


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.as_posix()


def artifact_paths_from_top_level(data: dict[str, Any]) -> list[str]:
    artifacts = data.get("artifacts")
    paths: list[str] = []
    if isinstance(artifacts, dict):
        for value in artifacts.values():
            if isinstance(value, str):
                paths.append(value)
            elif isinstance(value, dict):
                path = value.get("path")
                if isinstance(path, str):
                    paths.append(path)
    return paths


def artifact_paths_from_compact_path_vars(data: dict[str, Any]) -> list[str]:
    path_vars = data.get("path_vars")
    if not isinstance(path_vars, dict):
        return []
    parser = load_metadata_parser()
    resolved, errors = parser.resolve_compact_path_vars(path_vars)
    artifact_errors = [
        error
        for error in errors
        if any(error.startswith(f"path_vars.{key}:") for key in COMPACT_ARTIFACT_PATH_VAR_KEYS)
    ]
    if artifact_errors:
        raise QueryShapeError("; ".join(f"query artifact path {error}" for error in artifact_errors))

    paths: list[str] = []
    for key in sorted(COMPACT_ARTIFACT_PATH_VAR_KEYS):
        value = resolved.get(key)
        if value is None:
            continue
        if not is_safe_repo_path(value):
            raise QueryShapeError(f"query artifact path path_vars.{key} is unsafe: {value}")
        paths.append(value)
    return paths


def artifact_paths(data: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    paths.extend(artifact_paths_from_top_level(data))
    paths.extend(artifact_paths_from_compact_path_vars(data))
    return sorted(dict.fromkeys(paths))


def review_state(data: dict[str, Any], change_id: str) -> dict[str, Any]:
    review = data.get("review")
    state: dict[str, Any] = {
        "status": "unknown",
        "unresolved_items": None,
        "detail_pointers": {
            "review_log": f"docs/changes/{change_id}/review-log.md",
            "review_resolution": f"docs/changes/{change_id}/review-resolution.md",
        },
    }
    if isinstance(review, dict):
        if isinstance(review.get("status"), str):
            state["status"] = review["status"]
        unresolved = review.get("unresolved_items")
        if isinstance(unresolved, int):
            state["unresolved_items"] = unresolved
        reviewed_artifact = review.get("reviewed_artifact")
        if isinstance(reviewed_artifact, str):
            state["reviewed_artifact"] = reviewed_artifact
    return state


def validation_events(data: dict[str, Any]) -> list[dict[str, Any]]:
    events = data.get("validation_events")
    if isinstance(events, list):
        return [event for event in events if isinstance(event, dict)]
    legacy = data.get("validation")
    if isinstance(legacy, list):
        converted: list[dict[str, Any]] = []
        for index, item in enumerate(legacy, start=1):
            if isinstance(item, dict):
                converted.append(
                    {
                        "stage": f"legacy-validation-{index}",
                        "lifecycle_stage": "legacy",
                        "bundles": [],
                        "result": item.get("result"),
                        "command": item.get("command"),
                    }
                )
        return converted
    return []


def validation_summary(data: dict[str, Any]) -> dict[str, Any]:
    summary = data.get("validation_summary")
    return summary if isinstance(summary, dict) else {}


def event_transcript(event: dict[str, Any]) -> str | None:
    evidence = event.get("evidence")
    if isinstance(evidence, dict) and isinstance(evidence.get("transcript"), str):
        return evidence["transcript"]
    return None


def event_blockers(event: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for key in ("failures", "blockers"):
        entries = event.get(key)
        if not isinstance(entries, list):
            continue
        for item in entries:
            if isinstance(item, str):
                blockers.append(item)
            elif isinstance(item, dict):
                code = item.get("code") or item.get("stage") or item.get("message")
                if isinstance(code, str):
                    blockers.append(code)
    result = event.get("result")
    stage = event.get("stage")
    if not blockers and result in {"fail", "blocked", "not-run"} and isinstance(stage, str):
        blockers.append(stage)
    return blockers


def latest_validation_slice(data: dict[str, Any]) -> dict[str, Any] | None:
    events = validation_events(data)
    if not events:
        return None
    return validation_slice(events[-1])


def validation_slice(event: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "stage": event.get("stage"),
        "lifecycle_stage": event.get("lifecycle_stage"),
        "bundles": event.get("bundles") if isinstance(event.get("bundles"), list) else [],
        "result": event.get("result"),
        "counts": event.get("counts") if isinstance(event.get("counts"), dict) else {},
        "blockers": event_blockers(event),
        "transcript": event_transcript(event),
    }
    if isinstance(event.get("command"), str):
        result["command"] = event["command"]
    return result


def open_blockers(data: dict[str, Any]) -> list[str]:
    summary = validation_summary(data)
    blockers = summary.get("open_validation_blockers")
    if isinstance(blockers, list):
        return [item for item in blockers if isinstance(item, str)]
    latest = latest_validation_slice(data)
    return latest.get("blockers", []) if latest else []


def profile_policy(
    data: dict[str, Any],
    metadata_path: Path,
    repo_root: Path,
) -> dict[str, Any] | None:
    workflow = data.get("workflow")
    if not isinstance(workflow, dict):
        return None
    autoprogression = workflow.get("autoprogression")
    if not isinstance(autoprogression, dict):
        return None

    policy: dict[str, Any] = {
        "policy_owner": "change-metadata",
        "detail_pointer": f"{repo_relative(metadata_path, repo_root)}#workflow.autoprogression",
    }
    if isinstance(autoprogression.get("profile"), str):
        for field in ("profile", "authorized_by", "authorized_at", "change_id"):
            value = autoprogression.get(field)
            if isinstance(value, str):
                policy[field] = value
        return policy

    records: dict[str, dict[str, Any]] = {}
    for record_key in AUTOPROGRESSION_NAMED_RECORDS:
        record = autoprogression.get(record_key)
        if not isinstance(record, dict):
            continue
        record_policy: dict[str, Any] = {
            "detail_pointer": (
                f"{repo_relative(metadata_path, repo_root)}"
                f"#workflow.autoprogression.{record_key}"
            )
        }
        for field in (
            "profile",
            "phase",
            "state",
            "status",
            "target_stage",
            "authorized_by",
            "authorized_at",
            "armed_by",
            "armed_at",
            "change_id",
        ):
            value = record.get(field)
            if isinstance(value, str):
                record_policy[field] = value
        records[record_key] = record_policy
    if records:
        policy["records"] = records
    return policy


def detail_pointers(change_id: str, metadata_path: Path, repo_root: Path) -> dict[str, str]:
    return {
        "change_metadata": repo_relative(metadata_path, repo_root),
        "review_log": f"docs/changes/{change_id}/review-log.md",
        "review_resolution": f"docs/changes/{change_id}/review-resolution.md",
        "validation_history": f"{repo_relative(metadata_path, repo_root)}#validation_events",
        "forensic_read": repo_relative(metadata_path, repo_root),
    }


def query_summary(change_id: str, metadata_path: Path, data: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    return {
        "status": "ok",
        "query": "summary",
        "change_id": change_id,
        "metadata_shape": metadata_shape(data),
        "artifact_paths": artifact_paths(data),
        "review_state": review_state(data, change_id),
        "profile_policy": profile_policy(data, metadata_path, repo_root),
        "latest_validation": latest_validation_slice(data),
        "open_blockers": open_blockers(data),
        "detail_pointers": detail_pointers(change_id, metadata_path, repo_root),
    }


def query_artifacts(change_id: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "ok",
        "query": "artifacts",
        "change_id": change_id,
        "artifact_paths": artifact_paths(data),
    }


def query_validation_latest(change_id: str, metadata_path: Path, data: dict[str, Any], repo_root: Path) -> tuple[dict[str, Any], int]:
    latest = latest_validation_slice(data)
    if latest is None:
        return (
            error_payload(
                "no-validation-evidence",
                "change metadata has no validation evidence",
                change_id=change_id,
                detail_pointers=detail_pointers(change_id, metadata_path, repo_root),
            ),
            2,
        )
    return (
        {
            "status": "ok",
            "query": "validation",
            "mode": "latest",
            "change_id": change_id,
            "validation": latest,
            "detail_pointers": detail_pointers(change_id, metadata_path, repo_root),
        },
        0,
    )


def query_validation_stage(
    change_id: str,
    metadata_path: Path,
    data: dict[str, Any],
    repo_root: Path,
    stage: str,
) -> tuple[dict[str, Any], int]:
    for event in validation_events(data):
        if event.get("stage") == stage:
            return (
                {
                    "status": "ok",
                    "query": "validation",
                    "mode": "stage",
                    "change_id": change_id,
                    "validation": validation_slice(event),
                    "detail_pointers": detail_pointers(change_id, metadata_path, repo_root),
                },
                0,
            )
    return (
        error_payload(
            "stage-not-found",
            "requested validation stage was not found",
            change_id=change_id,
            stage=stage,
            detail_pointers=detail_pointers(change_id, metadata_path, repo_root),
        ),
        2,
    )


def parse_args(argv: list[str]) -> tuple[str, str, list[str], Path] | int:
    repo_root = ROOT
    args = list(argv)
    if "--repo-root" in args:
        index = args.index("--repo-root")
        if index + 1 >= len(args):
            return usage_error("--repo-root requires a path")
        repo_root = Path(args[index + 1]).resolve()
        del args[index : index + 2]
    if len(args) < 2:
        return usage_error("usage: query-change-record.py <change-id> <query> [options]")
    change_id = args[0]
    query = args[1]
    rest = args[2:]
    return change_id, query, rest, repo_root


def main(argv: list[str]) -> int:
    parsed = parse_args(argv)
    if isinstance(parsed, int):
        return parsed
    change_id, query, rest, repo_root = parsed
    if query not in SUPPORTED_QUERIES:
        return emit(
            error_payload(
                "unsupported-query",
                f"unsupported query: {query}",
                change_id=change_id,
                query=query,
                supported_queries=sorted(SUPPORTED_QUERIES),
            ),
            exit_code=2,
        )

    metadata_path, data, error = load_change_metadata(repo_root, change_id)
    if error is not None:
        return emit(error, exit_code=2)
    assert data is not None

    if query == "summary":
        if rest:
            return usage_error("summary does not accept extra options")
        return emit(query_summary(change_id, metadata_path, data, repo_root))
    if query == "artifacts":
        if rest:
            return usage_error("artifacts does not accept extra options")
        return emit(query_artifacts(change_id, data))

    if rest == ["--latest"]:
        payload, exit_code = query_validation_latest(change_id, metadata_path, data, repo_root)
        return emit(payload, exit_code=exit_code)
    if len(rest) == 2 and rest[0] == "--stage":
        payload, exit_code = query_validation_stage(change_id, metadata_path, data, repo_root, rest[1])
        return emit(payload, exit_code=exit_code)
    return usage_error("validation requires --latest or --stage <stage>")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
