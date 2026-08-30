import { createHash } from "node:crypto";

import { isAlias, isMap, isScalar, isSeq, parseAllDocuments, stringify } from "yaml";

export const LIFECYCLE_OPERATIONS = Object.freeze([
  "record-artifact-revision",
  "record-review",
  "record-validation",
  "record-finding-resolution",
  "settle-artifact",
  "record-package-review",
  "settle-review-package",
  "advance-stage",
  "initialize-approved-plan",
  "start-milestone",
  "complete-milestone",
  "route-correction",
  "return-correction",
  "withdraw-artifact-registration",
  "migrate",
  "repair",
]);

export const LIFECYCLE_ERROR_CODES = Object.freeze([
  "RL_CHANGE_NOT_FOUND",
  "RL_AMBIGUOUS_CHANGE",
  "RL_UNSUPPORTED_SCHEMA",
  "RL_INCOMPATIBLE_VERSION",
  "RL_INVALID_REQUEST",
  "RL_OPERATION_NOT_PERMITTED",
  "RL_STALE_OPERATION",
  "RL_STALE_EVIDENCE",
  "RL_UNRESOLVED_MATERIAL_FINDING",
  "RL_MILESTONE_ORDER",
  "RL_AUTHORITY_BOUNDARY",
  "RL_POST_VALIDATION_FAILED",
  "RL_REPAIR_UNSAFE",
  "RL_OPERATION_BUSY",
  "RL_RECOVERY_REQUIRED",
  "RL_WORKFLOW_ROUTE_REQUIRED",
  "RL_CORRECTION_ROUTE_INVALID",
  "RL_ARTIFACT_PATH_OWNED",
  "RL_WITHDRAWAL_UNSAFE",
]);

export const PROVENANCE_EXCLUDED_FIELDS = Object.freeze(["actor", "recorded_at"]);

const STANDARD_TAGS = new Set([
  "tag:yaml.org,2002:map",
  "tag:yaml.org,2002:seq",
  "tag:yaml.org,2002:str",
  "tag:yaml.org,2002:null",
  "tag:yaml.org,2002:bool",
  "tag:yaml.org,2002:int",
  "tag:yaml.org,2002:float",
]);

const TOP_LEVEL_ORDER = [
  "change_id",
  "title",
  "classification",
  "risk",
  "lifecycle_contract",
  "artifact_states",
  "review_packages",
  "workflow_state",
  "workflow",
  "artifacts",
  "requirements",
  "tests",
  "validation",
  "changed_files",
  "review",
  "architecture",
];

const OPERATION_FIELDS = Object.freeze({
  "record-artifact-revision": ["artifact_id", "artifact_kind", "artifact_role", "artifact_path", "evidence_path", "prior_artifact_sha256", "stage_authority"],
  "record-review": ["artifact_id", "evidence_path", "stage_authority"],
  "record-validation": ["artifact_id", "evidence_path", "subject_path", "stage_authority"],
  "record-finding-resolution": ["artifact_id", "evidence_path", "finding_id", "stage_authority"],
  "settle-artifact": ["artifact_id", "stage_authority"],
  "record-package-review": ["package_kind", "members", "upstream_review_id", "review_id", "evidence_path", "stage_authority"],
  "settle-review-package": ["package_kind", "review_id", "stage_authority"],
  "advance-stage": ["source_stage", "destination_stage", "stage_authority"],
  "initialize-approved-plan": ["artifact_id", "stage_authority"],
  "start-milestone": ["milestone_id", "stage_authority"],
  "complete-milestone": ["milestone_id", "evidence_path", "review_evidence_path", "stage_authority"],
  "route-correction": ["source_stage", "destination_stage", "destination_artifact_id", "reason", "evidence_path", "finding_ids", "return_stage", "milestone_id", "stage_authority"],
  "return-correction": ["route_id", "evidence_path", "stage_authority"],
  "withdraw-artifact-registration": ["artifact_id", "artifact_path", "canonical_owner_change_id", "reason", "evidence_path", "stage_authority"],
  migrate: ["source_schema_version", "stage_authority"],
  repair: ["condition", "stage_authority", "dry_run_acknowledgement"],
});

const REVIEW_AUTHORITIES = Object.freeze([
  "proposal-review",
]);

const OPERATION_CONTRACTS = Object.freeze({
  "record-artifact-revision": { required: ["artifact_id", "artifact_kind", "artifact_role", "artifact_path", "evidence_path", "stage_authority"], authorities: ["proposal", "spec", "architecture", "plan", "test-spec"] },
  "record-review": { required: ["artifact_id", "evidence_path", "stage_authority"], authorities: REVIEW_AUTHORITIES },
  "record-validation": { required: ["artifact_id", "evidence_path", "subject_path", "stage_authority"], authorities: ["implement", "verify", "ci-maintenance"] },
  "record-finding-resolution": { required: ["artifact_id", "evidence_path", "finding_id", "stage_authority"], authorities: ["review-resolution"] },
  "settle-artifact": { required: ["artifact_id", "stage_authority"], authorities: REVIEW_AUTHORITIES },
  "record-package-review": { required: ["package_kind", "members", "upstream_review_id", "evidence_path", "stage_authority"], authorities: ["design-review", "delivery-review"] },
  "settle-review-package": { required: ["package_kind", "review_id", "stage_authority"], authorities: ["design-review", "delivery-review"] },
  "advance-stage": { required: ["source_stage", "destination_stage", "stage_authority"], authorities: ["workflow"] },
  "initialize-approved-plan": { required: ["artifact_id", "stage_authority"], authorities: ["plan"] },
  "start-milestone": { required: ["milestone_id", "stage_authority"], authorities: ["workflow"] },
  "complete-milestone": { required: ["milestone_id", "evidence_path", "stage_authority"], authorities: ["workflow"] },
  "route-correction": { required: ["source_stage", "destination_stage", "destination_artifact_id", "reason", "evidence_path", "finding_ids", "return_stage", "stage_authority"], authorities: ["workflow"] },
  "return-correction": { required: ["route_id", "evidence_path", "stage_authority"], authorities: ["workflow"] },
  "withdraw-artifact-registration": { required: ["artifact_id", "artifact_path", "canonical_owner_change_id", "reason", "evidence_path", "stage_authority"], authorities: ["workflow"] },
  migrate: { required: ["source_schema_version", "stage_authority"], authorities: ["workflow"] },
  repair: { required: ["condition", "stage_authority", "dry_run_acknowledgement"], authorities: ["workflow"] },
});

const REPAIR_CONDITIONS = new Set(["reconcile-interrupted-replace", "clear-orphaned-lock"]);
const CORRECTION_REASONS = new Set(["upstream-contract-gap", "upstream-proof-gap", "upstream-ownership-gap", "upstream-planning-gap", "upstream-stale-input"]);
const CORRECTION_DESTINATIONS = new Set(["proposal", "spec", "architecture", "design-review", "plan", "test-spec"]);

const STAGE_TRANSITIONS = Object.freeze({
  proposal: ["proposal-review"],
  "proposal-review": ["architecture"],
  architecture: ["spec"],
  spec: ["design-review"],
  "design-review": ["plan"],
  plan: ["test-spec"],
  "test-spec": ["delivery-review"],
  "delivery-review": ["implement"],
});

export function allowedNextStages(_change, sourceStage) {
  return STAGE_TRANSITIONS[sourceStage] ?? [];
}

function invalid(message) {
  const error = new Error(`RL_INVALID_REQUEST: ${message}`);
  error.code = "RL_INVALID_REQUEST";
  return error;
}

function inspectNode(node) {
  if (!node) return;
  if (isAlias(node)) throw invalid("YAML aliases are not supported");
  if (node.anchor) throw invalid("YAML anchors are not supported");
  if (node.tag && !STANDARD_TAGS.has(node.tag)) throw invalid("custom YAML tags are not supported");
  if (isMap(node)) {
    for (const pair of node.items) {
      if (!isScalar(pair.key) || typeof pair.key.value !== "string") {
        throw invalid("YAML mapping keys must be strings");
      }
      if (pair.key.value === "<<") throw invalid("YAML merge keys are not supported");
      inspectNode(pair.value);
    }
  } else if (isSeq(node)) {
    for (const item of node.items) inspectNode(item);
  } else if (isScalar(node)) {
    if (typeof node.value === "number" && !Number.isFinite(node.value)) {
      throw invalid("non-finite YAML numbers are not supported");
    }
  } else {
    throw invalid("unsupported YAML node kind");
  }
}

export function parseLifecycleYaml(text) {
  if (typeof text !== "string") throw invalid("YAML input must be UTF-8 text");
  let documents;
  try {
    documents = parseAllDocuments(text, { uniqueKeys: true, merge: false, maxAliasCount: 0 });
  } catch (error) {
    throw invalid(error.message);
  }
  if (documents.length !== 1) throw invalid("exactly one YAML document is required");
  const [document] = documents;
  if (document.errors.length > 0) throw invalid(document.errors[0].message);
  inspectNode(document.contents);
  const value = document.toJS({ maxAliasCount: 0, mapAsMap: false });
  if (!value || Array.isArray(value) || typeof value !== "object") {
    throw invalid("lifecycle YAML root must be a mapping");
  }
  return value;
}

function ordered(value, topLevel = false) {
  if (Array.isArray(value)) return value.map((item) => ordered(item));
  if (!value || typeof value !== "object") return value;
  const keys = Object.keys(value);
  const orderedKeys = topLevel
    ? [...TOP_LEVEL_ORDER.filter((key) => keys.includes(key)), ...keys.filter((key) => !TOP_LEVEL_ORDER.includes(key)).sort()]
    : keys.includes("schema_version") ? ["schema_version", ...keys.filter((key) => key !== "schema_version").sort()] : keys.sort();
  return Object.fromEntries(orderedKeys.map((key) => [key, ordered(value[key])]));
}

export function serializeLifecycleYaml(value) {
  return stringify(ordered(value, true), { lineWidth: 0, indent: 2 }).replace(/\r\n?/g, "\n");
}

export function canonicalJson(value) {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value)
      .sort()
      .map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

export function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function lifecycleRevision(change, referenced = []) {
  const identities = [...referenced]
    .map(({ path, sha256: digest }) => ({ path, sha256: digest }))
    .sort((left, right) => left.path.localeCompare(right.path));
  const payload = canonicalJson({
    schema: "rigorloop-lifecycle-revision-v1",
    change: ordered(withoutProvenance(change), true),
    referenced: identities,
  });
  return `sha256:${sha256(payload)}`;
}

function withoutProvenance(value) {
  if (Array.isArray(value)) return value.map(withoutProvenance);
  if (!value || typeof value !== "object") return value;
  return Object.fromEntries(
    Object.entries(value)
      .filter(([key]) => !PROVENANCE_EXCLUDED_FIELDS.includes(key))
      .map(([key, child]) => [key, withoutProvenance(child)]),
  );
}

function requestError(summary, code = "RL_INVALID_REQUEST") {
  return { code, summary, blocking_invariant: "request-schema-v1" };
}

export function validateLifecycleRequest(request) {
  if (!request || Array.isArray(request) || typeof request !== "object") {
    return { ok: false, errors: [requestError("request must be a JSON object")] };
  }
  if (request.schema_version !== 1) {
    return { ok: false, errors: [requestError("unsupported request schema_version")] };
  }
  if (!LIFECYCLE_OPERATIONS.includes(request.operation)) {
    return { ok: false, errors: [requestError(`unknown operation ${String(request.operation)}`)] };
  }
  const allowed = new Set([
    "schema_version",
    "operation",
    "change_id",
    "expected_lifecycle_revision",
    ...PROVENANCE_EXCLUDED_FIELDS,
    ...OPERATION_FIELDS[request.operation],
  ]);
  const unknown = Object.keys(request).find((field) => !allowed.has(field));
  if (unknown) return { ok: false, errors: [requestError(`unknown field ${unknown}`)] };
  if (typeof request.change_id !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(request.change_id)) {
    return { ok: false, errors: [requestError("change_id must be one safe non-empty identifier")] };
  }
  if (typeof request.expected_lifecycle_revision !== "string" || !/^sha256:[a-f0-9]{64}$/.test(request.expected_lifecycle_revision)) {
    return { ok: false, errors: [requestError("expected_lifecycle_revision must be a sha256 lifecycle revision")] };
  }
  const contract = OPERATION_CONTRACTS[request.operation];
  for (const field of contract.required) {
    if (request[field] === undefined || request[field] === null || request[field] === "") {
      return { ok: false, errors: [requestError(`${field} is required for ${request.operation}`)] };
    }
  }
  if (request.condition !== undefined && !REPAIR_CONDITIONS.has(request.condition)) {
    return { ok: false, errors: [requestError(`unknown condition ${String(request.condition)}`)] };
  }
  if (!contract.authorities.includes(request.stage_authority)) {
    return { ok: false, errors: [requestError(`unknown stage_authority ${String(request.stage_authority)}`)] };
  }
  for (const field of ["artifact_id", "finding_id", "milestone_id", "destination_artifact_id", "route_id", "canonical_owner_change_id", "review_id"]) {
    if (request[field] !== undefined && (typeof request[field] !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(request[field]))) {
      return { ok: false, errors: [requestError(`${field} must be one safe identifier`)] };
    }
  }
  if (request.finding_ids !== undefined && (!Array.isArray(request.finding_ids) || request.finding_ids.some((value) => typeof value !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(value)) || new Set(request.finding_ids).size !== request.finding_ids.length)) {
    return { ok: false, errors: [requestError("finding_ids must be a unique array of safe identifiers")] };
  }
  if (request.members !== undefined && (typeof request.members !== "object" || request.members === null || Array.isArray(request.members) || Object.keys(request.members).length === 0 || Object.entries(request.members).some(([id, path]) => !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(id) || !isRepositoryRelativePath(path)))) {
    return { ok: false, errors: [requestError("members must map safe artifact IDs to normalized repository-relative paths")] };
  }
  if (request.package_kind !== undefined && !["design", "delivery"].includes(request.package_kind)) {
    return { ok: false, errors: [requestError(`unknown package_kind ${String(request.package_kind)}`)] };
  }
  if (request.upstream_review_id !== undefined && (typeof request.upstream_review_id !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(request.upstream_review_id))) {
    return { ok: false, errors: [requestError("upstream_review_id must be one safe review identity")] };
  }
  if (request.reason !== undefined) {
    const allowedReasons = request.operation === "withdraw-artifact-registration" ? new Set(["duplicate-registration"]) : CORRECTION_REASONS;
    if (!allowedReasons.has(request.reason)) return { ok: false, errors: [requestError(`unknown reason ${String(request.reason)}`, request.operation === "withdraw-artifact-registration" ? "RL_WITHDRAWAL_UNSAFE" : "RL_INVALID_REQUEST")] };
  }
  if (request.operation === "route-correction" && request.destination_stage !== undefined && !CORRECTION_DESTINATIONS.has(request.destination_stage)) {
    return { ok: false, errors: [requestError(`unknown destination_stage ${String(request.destination_stage)}`)] };
  }
  for (const field of ["source_stage", "destination_stage", "return_stage"]) {
    if (request[field] !== undefined && (typeof request[field] !== "string" || !/^[a-z][a-z0-9-]*$/.test(request[field]))) return { ok: false, errors: [requestError(`${field} must be one normalized stage`)] };
  }
  for (const field of ["artifact_path", "evidence_path", "review_evidence_path", "subject_path"]) {
    if (request[field] !== undefined && !isRepositoryRelativePath(request[field])) {
      return { ok: false, errors: [requestError(`${field} must be a normalized repository-relative path`)] };
    }
  }
  if (request.artifact_kind !== undefined && !["proposal", "spec", "architecture", "adr", "plan", "test-spec"].includes(request.artifact_kind)) {
    return { ok: false, errors: [requestError(`unknown artifact_kind ${String(request.artifact_kind)}`)] };
  }
  if (request.artifact_role !== undefined && !["primary", "supporting"].includes(request.artifact_role)) {
    return { ok: false, errors: [requestError(`unknown artifact_role ${String(request.artifact_role)}`)] };
  }
  if (request.prior_artifact_sha256 !== undefined && !/^[a-f0-9]{64}$/.test(request.prior_artifact_sha256)) {
    return { ok: false, errors: [requestError("prior_artifact_sha256 must be a 64-character sha256 digest") ] };
  }
  if (request.source_schema_version !== undefined && (!Number.isInteger(request.source_schema_version) || request.source_schema_version < 1)) {
    return { ok: false, errors: [requestError("source_schema_version must be a positive integer")] };
  }
  if (request.dry_run_acknowledgement !== undefined && request.dry_run_acknowledgement !== true) {
    return { ok: false, errors: [requestError("dry_run_acknowledgement must be true")] };
  }
  if (request.actor !== undefined && (typeof request.actor !== "string" || request.actor.trim().length === 0)) {
    return { ok: false, errors: [requestError("actor must be a non-empty string")] };
  }
  if (request.recorded_at !== undefined && !isRfc3339Timestamp(request.recorded_at)) {
    return { ok: false, errors: [requestError("recorded_at must be an RFC 3339 timestamp")] };
  }
  return { ok: true, value: structuredClone(request), errors: [] };
}

function isRfc3339Timestamp(value) {
  if (typeof value !== "string") return false;
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(?:Z|[+-](\d{2}):(\d{2}))$/.exec(value);
  if (!match) return false;
  const [, yearText, monthText, dayText, hourText, minuteText, secondText, offsetHourText, offsetMinuteText] = match;
  const year = Number(yearText);
  const month = Number(monthText);
  const day = Number(dayText);
  const daysInMonth = month >= 1 && month <= 12 ? new Date(Date.UTC(year, month, 0)).getUTCDate() : 0;
  return day >= 1
    && day <= daysInMonth
    && Number(hourText) <= 23
    && Number(minuteText) <= 59
    && Number(secondText) <= 59
    && (offsetHourText === undefined || Number(offsetHourText) <= 23)
    && (offsetMinuteText === undefined || Number(offsetMinuteText) <= 59);
}

function isRepositoryRelativePath(value) {
  if (typeof value !== "string" || value.length === 0 || value.startsWith("/") || value.includes("\\") || value.includes("\0")) {
    return false;
  }
  const segments = value.split("/");
  return segments.every((segment) => segment.length > 0 && segment !== "." && segment !== "..");
}
