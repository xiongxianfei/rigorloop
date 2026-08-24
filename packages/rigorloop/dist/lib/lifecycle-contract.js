import { createHash } from "node:crypto";

import { isAlias, isMap, isScalar, isSeq, parseAllDocuments, stringify } from "yaml";

export const LIFECYCLE_OPERATIONS = Object.freeze([
  "record-review",
  "record-validation",
  "record-finding-resolution",
  "settle-artifact",
  "start-milestone",
  "complete-milestone",
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
  "record-review": ["artifact_id", "evidence_path", "stage_authority"],
  "record-validation": ["artifact_id", "evidence_path", "subject_path", "stage_authority"],
  "record-finding-resolution": ["artifact_id", "evidence_path", "finding_id", "stage_authority"],
  "settle-artifact": ["artifact_id", "stage_authority"],
  "start-milestone": ["milestone_id", "stage_authority"],
  "complete-milestone": ["milestone_id", "evidence_path", "stage_authority"],
  migrate: ["source_schema_version", "stage_authority"],
  repair: ["condition", "stage_authority", "dry_run_acknowledgement"],
});

const REVIEW_AUTHORITIES = Object.freeze([
  "proposal-review",
  "spec-review",
  "architecture-review",
  "plan-review",
  "test-spec-review",
  "code-review",
]);

const OPERATION_CONTRACTS = Object.freeze({
  "record-review": { required: ["artifact_id", "evidence_path", "stage_authority"], authorities: REVIEW_AUTHORITIES },
  "record-validation": { required: ["artifact_id", "evidence_path", "subject_path", "stage_authority"], authorities: ["implement", "verify", "ci-maintenance"] },
  "record-finding-resolution": { required: ["artifact_id", "evidence_path", "finding_id", "stage_authority"], authorities: ["review-resolution"] },
  "settle-artifact": { required: ["artifact_id", "stage_authority"], authorities: REVIEW_AUTHORITIES },
  "start-milestone": { required: ["milestone_id", "stage_authority"], authorities: ["workflow"] },
  "complete-milestone": { required: ["milestone_id", "evidence_path", "stage_authority"], authorities: ["workflow"] },
  migrate: { required: ["source_schema_version", "stage_authority"], authorities: ["workflow"] },
  repair: { required: ["condition", "stage_authority", "dry_run_acknowledgement"], authorities: ["workflow"] },
});

const REPAIR_CONDITIONS = new Set(["reconcile-interrupted-replace", "clear-orphaned-lock"]);

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
    : keys.sort();
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

function requestError(summary) {
  return { code: "RL_INVALID_REQUEST", summary, blocking_invariant: "request-schema-v1" };
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
  for (const field of ["artifact_id", "finding_id", "milestone_id"]) {
    if (request[field] !== undefined && (typeof request[field] !== "string" || !/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(request[field]))) {
      return { ok: false, errors: [requestError(`${field} must be one safe identifier`)] };
    }
  }
  for (const field of ["evidence_path", "subject_path"]) {
    if (request[field] !== undefined && !isRepositoryRelativePath(request[field])) {
      return { ok: false, errors: [requestError(`${field} must be a normalized repository-relative path`)] };
    }
  }
  if (request.source_schema_version !== undefined && (!Number.isInteger(request.source_schema_version) || request.source_schema_version < 1)) {
    return { ok: false, errors: [requestError("source_schema_version must be a positive integer")] };
  }
  if (request.dry_run_acknowledgement !== undefined && request.dry_run_acknowledgement !== true) {
    return { ok: false, errors: [requestError("dry_run_acknowledgement must be true")] };
  }
  return { ok: true, value: structuredClone(request), errors: [] };
}

function isRepositoryRelativePath(value) {
  if (typeof value !== "string" || value.length === 0 || value.startsWith("/") || value.includes("\\") || value.includes("\0")) {
    return false;
  }
  const segments = value.split("/");
  return segments.every((segment) => segment.length > 0 && segment !== "." && segment !== "..");
}
