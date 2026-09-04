import { createHash } from "node:crypto";

import { parseLifecycleYaml } from "./lifecycle-contract.js";

const MAX_DOCUMENT_BYTES = 8 * 1024 * 1024;
const MAX_TEXT_LENGTH = 16 * 1024;
const DIGEST = /^sha256:[a-f0-9]{64}$/;
const ID = /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/;

export const COMPACT_SCHEMA_IDS = Object.freeze([
  "compact-change-v1",
  "compact-review-v1",
  "compact-decisions-v1",
  "compact-evidence-v1",
  "compact-verify-v1",
  "compact-operation-v1",
  "compact-result-v1",
  "compact-recovery-v1",
]);

export const COMPACT_VOCABULARIES = Object.freeze({
  Schema: COMPACT_SCHEMA_IDS,
  Stage: ["proposal", "proposal-review", "architecture", "spec", "design-review", "plan", "delivery-review", "implement", "code-review", "review-resolution", "ci-maintenance", "verify", "pr"],
  Authority: ["proposal", "proposal-review", "architecture", "spec", "design-review", "plan", "delivery-review", "implement", "code-review", "review-resolution", "ci-maintenance", "verify", "pr", "workflow"],
  Operation: ["record-artifact", "advance-stage", "replace-review", "settle-review", "resolve-finding", "upsert-decision", "remove-decision", "route-correction", "return-correction", "advance-milestone", "update-evidence", "invalidate-evidence", "record-verify", "recover"],
  ArtifactKind: ["proposal", "architecture", "adr", "spec", "plan"],
  ArtifactRole: ["primary", "supporting"],
  ArtifactStatus: ["authoring", "review-required", "accepted", "approved", "active", "revision-required", "blocked", "superseded"],
  ReviewOutcome: ["approved", "changes-requested", "blocked", "inconclusive"],
  Severity: ["critical", "major", "minor", "note"],
  BlockingEffect: ["blocks-progression", "advisory"],
  Disposition: ["open", "accepted", "rejected", "deferred", "partially-accepted"],
  Freshness: ["current", "stale"],
  Readiness: ["not-ready", "blocked", "ready-for-review", "verified"],
  ReviewTargetKind: ["proposal", "design-package", "delivery-package", "milestone", "final-code"],
  ReviewRecordingStatus: ["recorded", "blocked"],
  ReviewRefStatus: ["current", "review-required", "blocked"],
  Applicability: ["applicable", "retained-pending-decision"],
  EvidenceOutcome: ["passed", "failed", "inconclusive", "not-run"],
  DetailLocationKind: ["repository", "external", "machine-local"],
  RemainingWorkKind: ["milestone", "task"],
  RemainingWorkStatus: ["pending", "blocked"],
  ActiveWorkKind: ["milestone", "correction"],
  MilestoneStatus: ["planned", "implementing", "review-required"],
  ExpectedFileState: ["absent", "present"],
  ContentInputSource: ["inline", "path"],
  Materiality: ["material", "non-material"],
  VerifyImpact: ["low", "standard", "high", "critical"],
  VerifyHandoff: ["ready", "ready-with-limitations"],
  ResultStatus: ["success", "already-applied", "rejected", "busy", "recovery-required"],
  DiagnosticScope: ["progression", "operation"],
  ProgressionStatus: ["blocked", "ready"],
  EligibilityStatus: ["permitted", "prohibited"],
  CorrectionStatus: ["authoring", "review-required", "blocked"],
  ProjectionView: ["summary", "reviews", "open-findings", "material-decisions", "evidence", "remaining-work", "verification", "skill-context"],
  RecoveryPhase: ["prepared", "replacing", "persisted"],
  ReplacementStatus: ["pending", "replaced"],
  RecoveryAction: ["restore-prior", "accept-candidate"],
});

const VOCABULARY_SETS = Object.fromEntries(Object.entries(COMPACT_VOCABULARIES).map(([name, values]) => [name, new Set(values)]));

export function validateCompactVocabulary(name, value) {
  const values = VOCABULARY_SETS[name];
  if (!values) throw new Error(`vocabulary: unknown_value ${name}`);
  if (!values.has(value)) throw new Error(`${name}: unknown_value ${String(value)}`);
  return value;
}

function record(value, label) {
  if (!value || Array.isArray(value) || typeof value !== "object") throw new Error(`${label} must be a mapping`);
  return value;
}

function exact(value, fields, label) {
  record(value, label);
  const expected = new Set(fields);
  for (const field of Object.keys(value)) if (!expected.has(field)) throw new Error(`${label}: unknown field ${field}`);
  for (const field of fields) if (!Object.hasOwn(value, field)) throw new Error(`${label}: missing field ${field}`);
}

function id(value, label) {
  if (typeof value !== "string" || !ID.test(value)) throw new Error(`${label} must be an Id`);
}

function text(value, label) {
  if (typeof value !== "string" || value.length === 0 || Buffer.byteLength(value, "utf8") > MAX_TEXT_LENGTH) throw new Error(`${label} must be non-empty Text of at most 16 KiB`);
}

function digest(value, label, nullable = false) {
  if (nullable && value === null) return;
  if (typeof value !== "string" || !DIGEST.test(value)) throw new Error(`${label} must be a Digest`);
}

export function validateCompactPath(value, label = "path") {
  if (typeof value !== "string" || value.length === 0 || Buffer.byteLength(value, "utf8") > 1024) throw new Error(`${label} must be a repository-relative Path`);
  if (value.startsWith("/") || value.includes("\\") || value.endsWith("/") || value.split("/").some((part) => part === "" || part === "." || part === "..")) {
    throw new Error(`${label} must be a normalized repository-relative Path`);
  }
}

function timestamp(value, label) {
  const match = typeof value === "string" ? value.match(/^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(?:\.\d+)?Z$/) : null;
  if (!match) throw new Error(`${label} must be an RFC 3339 UTC Timestamp`);
  const [year, month, day, hour, minute, second] = match.slice(1, 7).map(Number);
  if (month < 1 || month > 12 || day < 1 || hour > 23 || minute > 59 || second > 59) throw new Error(`${label} must be an RFC 3339 UTC Timestamp`);
  const instant = new Date(0);
  instant.setUTCFullYear(year, month - 1, day);
  instant.setUTCHours(hour, minute, second, 0);
  if (instant.getUTCFullYear() !== year || instant.getUTCMonth() !== month - 1 || instant.getUTCDate() !== day) throw new Error(`${label} must be an RFC 3339 UTC Timestamp`);
}

function integer(value, label, minimum = Number.MIN_SAFE_INTEGER) {
  if (!Number.isSafeInteger(value) || value < minimum) throw new Error(`${label} must be an integer >= ${minimum}`);
}

function boolean(value, label) {
  if (typeof value !== "boolean") throw new Error(`${label} must be boolean`);
}

function array(value, label, validate, { minimum = 0, unique = false } = {}) {
  if (!Array.isArray(value) || value.length < minimum) throw new Error(`${label} must be an array with at least ${minimum} entries`);
  if (unique && new Set(value).size !== value.length) throw new Error(`${label} contains duplicate values`);
  value.forEach((entry, index) => validate(entry, `${label}[${index}]`));
}

function stringArray(value, label, validator, minimum = 0) {
  array(value, label, validator, { minimum, unique: true });
}

function rawUtf8Compare(left, right) {
  return Buffer.compare(Buffer.from(left, "utf8"), Buffer.from(right, "utf8"));
}

function mapping(value, label, validate, identityField, { minimum = 0, pathKeys = false } = {}) {
  record(value, label);
  const keys = Object.keys(value);
  if (keys.length < minimum) throw new Error(`${label} must be absent instead of empty`);
  for (let index = 1; index < keys.length; index += 1) {
    if (rawUtf8Compare(keys[index - 1], keys[index]) >= 0) throw new Error(`${label} keys must use strict UTF-8 byte order`);
  }
  for (const key of keys) {
    if (pathKeys) validateCompactPath(key, `${label} key`); else id(key, `${label} key`);
    validate(value[key], `${label}.${key}`);
    if (identityField && value[key][identityField] !== key) throw new Error(`${label}.${key}.${identityField} must equal its mapping key`);
  }
}

function subject(value, label) {
  exact(value, ["subject_id", "path", "identity"], label);
  id(value.subject_id, `${label}.subject_id`);
  validateCompactPath(value.path, `${label}.path`);
  digest(value.identity, `${label}.identity`);
}

function artifactRef(value, label) {
  exact(value, ["artifact_id", "kind", "role", "path", "identity", "owner", "status"], label);
  id(value.artifact_id, `${label}.artifact_id`);
  validateCompactVocabulary("ArtifactKind", value.kind);
  validateCompactVocabulary("ArtifactRole", value.role);
  validateCompactPath(value.path, `${label}.path`);
  digest(value.identity, `${label}.identity`);
  validateCompactVocabulary("Authority", value.owner);
  validateCompactVocabulary("ArtifactStatus", value.status);
}

function reviewRef(value, label) {
  exact(value, ["target_id", "path", "identity", "review_id", "outcome", "reviewer_authority", "status"], label);
  id(value.target_id, `${label}.target_id`);
  validateCompactPath(value.path, `${label}.path`);
  digest(value.identity, `${label}.identity`);
  id(value.review_id, `${label}.review_id`);
  validateCompactVocabulary("ReviewOutcome", value.outcome);
  validateCompactVocabulary("Authority", value.reviewer_authority);
  validateCompactVocabulary("ReviewRefStatus", value.status);
}

function finding(value, label) {
  exact(value, ["finding_id", "affected_surfaces", "severity", "blocking_effect", "owner", "required_next_action", "disposition", "evidence"], label);
  id(value.finding_id, `${label}.finding_id`);
  stringArray(value.affected_surfaces, `${label}.affected_surfaces`, text, 1);
  validateCompactVocabulary("Severity", value.severity);
  validateCompactVocabulary("BlockingEffect", value.blocking_effect);
  validateCompactVocabulary("Authority", value.owner);
  text(value.required_next_action, `${label}.required_next_action`);
  if (value.disposition !== "open") validateCompactVocabulary("Disposition", value.disposition);
  if (value.disposition !== "open") throw new Error(`${label}.disposition must be open`);
  text(value.evidence, `${label}.evidence`);
}

function findingRef(value, label) {
  exact(value, ["finding_id", "review_target_id", "review_path", "review_identity", "owner", "severity", "blocking_effect"], label);
  id(value.finding_id, `${label}.finding_id`);
  id(value.review_target_id, `${label}.review_target_id`);
  validateCompactPath(value.review_path, `${label}.review_path`);
  digest(value.review_identity, `${label}.review_identity`);
  validateCompactVocabulary("Authority", value.owner);
  validateCompactVocabulary("Severity", value.severity);
  validateCompactVocabulary("BlockingEffect", value.blocking_effect);
}

function decisionRef(value, label) {
  exact(value, ["decision_id", "path", "identity", "applicability"], label);
  id(value.decision_id, `${label}.decision_id`);
  validateCompactPath(value.path, `${label}.path`);
  digest(value.identity, `${label}.identity`);
  validateCompactVocabulary("Applicability", value.applicability);
}

function evidenceRef(value, label) {
  exact(value, ["evidence_id", "manifest_path", "manifest_identity", "freshness"], label);
  id(value.evidence_id, `${label}.evidence_id`);
  validateCompactPath(value.manifest_path, `${label}.manifest_path`);
  digest(value.manifest_identity, `${label}.manifest_identity`);
  validateCompactVocabulary("Freshness", value.freshness);
}

function diagnostic(value, label) {
  exact(value, ["code", "summary", "invariant", "scope", "operation", "identities", "next_operation"], label);
  id(value.code, `${label}.code`);
  text(value.summary, `${label}.summary`);
  id(value.invariant, `${label}.invariant`);
  validateCompactVocabulary("DiagnosticScope", value.scope);
  if (value.operation !== null) validateCompactVocabulary("Operation", value.operation);
  if ((value.scope === "operation") !== (value.operation !== null)) throw new Error(`${label}.operation must be non-null exactly for operation scope`);
  stringArray(value.identities, `${label}.identities`, text);
  if (value.next_operation !== null) validateCompactVocabulary("Operation", value.next_operation);
}

function remainingWork(value, label) {
  exact(value, ["work_id", "kind", "owner", "required_action", "status"], label);
  id(value.work_id, `${label}.work_id`);
  validateCompactVocabulary("RemainingWorkKind", value.kind);
  validateCompactVocabulary("Authority", value.owner);
  text(value.required_action, `${label}.required_action`);
  validateCompactVocabulary("RemainingWorkStatus", value.status);
}

function activeWork(value, label) {
  record(value, label);
  validateCompactVocabulary("ActiveWorkKind", value.kind);
  if (value.kind === "milestone") {
    exact(value, ["kind", "milestone_id", "status", "owner"], label);
    id(value.milestone_id, `${label}.milestone_id`);
    validateCompactVocabulary("MilestoneStatus", value.status);
    validateCompactVocabulary("Authority", value.owner);
  } else {
    exact(value, ["kind", "finding_ids", "source_stage", "destination_stage", "return_stage", "owner", "reason", "return_condition", "expected_review_target", "status"], label);
    stringArray(value.finding_ids, `${label}.finding_ids`, id, 1);
    validateCompactVocabulary("Stage", value.source_stage);
    validateCompactVocabulary("Stage", value.destination_stage);
    validateCompactVocabulary("Stage", value.return_stage);
    validateCompactVocabulary("Authority", value.owner);
    id(value.reason, `${label}.reason`);
    text(value.return_condition, `${label}.return_condition`);
    id(value.expected_review_target, `${label}.expected_review_target`);
    validateCompactVocabulary("CorrectionStatus", value.status);
  }
}

function correctionInput(value, label) {
  exact(value, ["finding_ids", "source_stage", "destination_stage", "return_stage", "owner", "reason", "return_condition", "expected_review_target"], label);
  stringArray(value.finding_ids, `${label}.finding_ids`, id, 1);
  validateCompactVocabulary("Stage", value.source_stage);
  validateCompactVocabulary("Stage", value.destination_stage);
  validateCompactVocabulary("Stage", value.return_stage);
  validateCompactVocabulary("Authority", value.owner);
  id(value.reason, `${label}.reason`);
  text(value.return_condition, `${label}.return_condition`);
  id(value.expected_review_target, `${label}.expected_review_target`);
}

function contentInput(value, label) {
  exact(value, ["path", "identity", "source", "content", "source_path"], label);
  validateCompactPath(value.path, `${label}.path`);
  digest(value.identity, `${label}.identity`);
  validateCompactVocabulary("ContentInputSource", value.source);
  if (value.source === "inline") {
    if (typeof value.content !== "string" || Buffer.byteLength(value.content, "utf8") > MAX_DOCUMENT_BYTES || value.source_path !== null) throw new Error(`${label} inline source is inconsistent`);
    if (sha256(value.content) !== value.identity) throw new Error(`${label} inline identity mismatch`);
  } else if (value.content !== null || value.source_path === null) throw new Error(`${label} path source is inconsistent`);
  else validateCompactPath(value.source_path, `${label}.source_path`);
}

function expectedFile(value, label) {
  exact(value, ["path", "state", "identity"], label);
  validateCompactPath(value.path, `${label}.path`);
  validateCompactVocabulary("ExpectedFileState", value.state);
  digest(value.identity, `${label}.identity`, true);
  if ((value.state === "present") !== (value.identity !== null)) throw new Error(`${label}.identity must match state`);
}

function detailLocation(value, label) {
  exact(value, ["kind", "value"], label);
  validateCompactVocabulary("DetailLocationKind", value.kind);
  text(value.value, `${label}.value`);
}

function projection(value, label) {
  exact(value, ["view", "change_id", "lifecycle_contract", "lifecycle_revision", "current_stage", "artifacts", "reviews", "open_findings", "material_decisions", "evidence", "active_work", "progression_status", "blockers", "remaining_work", "permitted_operations", "requested_operation", "operation_eligibility", "required_paths"], label);
  validateCompactVocabulary("ProjectionView", value.view);
  id(value.change_id, `${label}.change_id`);
  if (value.lifecycle_contract !== "compact-current-state-v1") throw new Error(`${label}.lifecycle_contract: unknown_value ${String(value.lifecycle_contract)}`);
  digest(value.lifecycle_revision, `${label}.lifecycle_revision`);
  validateCompactVocabulary("Stage", value.current_stage);
  mapping(value.artifacts, `${label}.artifacts`, artifactRef, "artifact_id");
  mapping(value.reviews, `${label}.reviews`, reviewRef, "target_id");
  mapping(value.open_findings, `${label}.open_findings`, findingRef, "finding_id");
  mapping(value.material_decisions, `${label}.material_decisions`, decisionRef, "decision_id");
  mapping(value.evidence, `${label}.evidence`, evidenceRef, "evidence_id");
  if (value.active_work !== null) activeWork(value.active_work, `${label}.active_work`);
  validateCompactVocabulary("ProgressionStatus", value.progression_status);
  array(value.blockers, `${label}.blockers`, diagnostic);
  mapping(value.remaining_work, `${label}.remaining_work`, remainingWork, "work_id");
  stringArray(value.permitted_operations, `${label}.permitted_operations`, (entry) => validateCompactVocabulary("Operation", entry));
  if (value.requested_operation !== null) validateCompactVocabulary("Operation", value.requested_operation);
  if (value.operation_eligibility !== null) {
    exact(value.operation_eligibility, ["operation", "status", "blockers"], `${label}.operation_eligibility`);
    validateCompactVocabulary("Operation", value.operation_eligibility.operation);
    validateCompactVocabulary("EligibilityStatus", value.operation_eligibility.status);
    array(value.operation_eligibility.blockers, `${label}.operation_eligibility.blockers`, diagnostic);
    if (value.operation_eligibility.operation !== value.requested_operation) throw new Error(`${label}.operation_eligibility operation must match requested_operation`);
    if ((value.operation_eligibility.status === "permitted") !== (value.operation_eligibility.blockers.length === 0)) throw new Error(`${label}.operation_eligibility status must match blockers`);
  }
  if ((value.requested_operation === null) !== (value.operation_eligibility === null)) throw new Error(`${label} requested operation and eligibility must both be null or non-null`);
  stringArray(value.required_paths, `${label}.required_paths`, validateCompactPath);
}

const PAYLOAD_FIELDS = Object.freeze({
  "record-artifact": ["artifact", "content"],
  "advance-stage": ["from_stage", "to_stage"],
  "replace-review": ["target_id", "prior_review_identity", "review", "resolutions"],
  "settle-review": ["target_id", "review_id", "outcome"],
  "resolve-finding": ["resolution", "review", "decisions"],
  "upsert-decision": ["decision_id", "decisions"],
  "remove-decision": ["decision_id"],
  "route-correction": ["correction"],
  "return-correction": ["finding_ids", "return_stage", "satisfied_condition"],
  "advance-milestone": ["milestone_id", "from_status", "to_status"],
  "update-evidence": ["evidence_ids", "evidence"],
  "invalidate-evidence": ["evidence_ids", "reason", "evidence"],
  "record-verify": ["verification_id", "report", "evidence_ids"],
  recover: ["transaction_id", "expected_recovery_identity", "action"],
});

function operationPayload(value, operation, label) {
  const fields = PAYLOAD_FIELDS[operation];
  exact(value, fields, label);
  const idList = (field, minimum = 0) => stringArray(value[field], `${label}.${field}`, id, minimum);
  const findingResolution = (resolution, resolutionLabel) => {
    exact(resolution, ["finding_id", "disposition", "materiality", "decision_id"], resolutionLabel);
    id(resolution.finding_id, `${resolutionLabel}.finding_id`);
    if (resolution.disposition === "open") throw new Error(`${resolutionLabel}.disposition cannot be open`);
    validateCompactVocabulary("Disposition", resolution.disposition);
    validateCompactVocabulary("Materiality", resolution.materiality);
    if ((resolution.materiality === "material") !== (resolution.decision_id !== null)) throw new Error(`${resolutionLabel}.decision_id must match materiality`);
    if (resolution.decision_id !== null) id(resolution.decision_id, `${resolutionLabel}.decision_id`);
  };
  switch (operation) {
    case "record-artifact": artifactRef(value.artifact, `${label}.artifact`); contentInput(value.content, `${label}.content`); break;
    case "advance-stage": validateCompactVocabulary("Stage", value.from_stage); validateCompactVocabulary("Stage", value.to_stage); break;
    case "replace-review": id(value.target_id, `${label}.target_id`); digest(value.prior_review_identity, `${label}.prior_review_identity`, true); contentInput(value.review, `${label}.review`); mapping(value.resolutions, `${label}.resolutions`, findingResolution, "finding_id"); break;
    case "settle-review": id(value.target_id, `${label}.target_id`); id(value.review_id, `${label}.review_id`); validateCompactVocabulary("ReviewOutcome", value.outcome); break;
    case "resolve-finding": findingResolution(value.resolution, `${label}.resolution`); contentInput(value.review, `${label}.review`); if (value.decisions !== null) contentInput(value.decisions, `${label}.decisions`); break;
    case "upsert-decision": id(value.decision_id, `${label}.decision_id`); contentInput(value.decisions, `${label}.decisions`); break;
    case "remove-decision": id(value.decision_id, `${label}.decision_id`); break;
    case "route-correction": correctionInput(value.correction, `${label}.correction`); break;
    case "return-correction": idList("finding_ids", 1); validateCompactVocabulary("Stage", value.return_stage); text(value.satisfied_condition, `${label}.satisfied_condition`); break;
    case "advance-milestone": {
      id(value.milestone_id, `${label}.milestone_id`);
      if (value.from_status !== null && !["planned", "implementing", "review-required"].includes(value.from_status)) throw new Error(`${label}.from_status: unknown_value ${String(value.from_status)}`);
      if (!["planned", "implementing", "review-required", "closed"].includes(value.to_status)) throw new Error(`${label}.to_status: unknown_value ${String(value.to_status)}`);
      break;
    }
    case "update-evidence": idList("evidence_ids", 1); contentInput(value.evidence, `${label}.evidence`); break;
    case "invalidate-evidence": idList("evidence_ids", 1); text(value.reason, `${label}.reason`); if (value.evidence !== null) contentInput(value.evidence, `${label}.evidence`); break;
    case "record-verify": id(value.verification_id, `${label}.verification_id`); contentInput(value.report, `${label}.report`); idList("evidence_ids", 1); break;
    case "recover": id(value.transaction_id, `${label}.transaction_id`); digest(value.expected_recovery_identity, `${label}.expected_recovery_identity`); validateCompactVocabulary("RecoveryAction", value.action); break;
  }
}

function validateChange(value) {
  exact(value, ["schema", "change_id", "title", "lifecycle_contract", "lifecycle_revision", "current_stage", "artifacts", "reviews", "active_work", "open_findings", "material_decisions", "evidence", "blockers", "remaining_work", "readiness"], "compact-change-v1");
  id(value.change_id, "compact-change-v1.change_id"); text(value.title, "compact-change-v1.title");
  if (value.lifecycle_contract !== "compact-current-state-v1") throw new Error(`lifecycle_contract: unknown_value ${String(value.lifecycle_contract)}`);
  digest(value.lifecycle_revision, "compact-change-v1.lifecycle_revision"); validateCompactVocabulary("Stage", value.current_stage);
  mapping(value.artifacts, "compact-change-v1.artifacts", artifactRef, "artifact_id"); mapping(value.reviews, "compact-change-v1.reviews", reviewRef, "target_id");
  if (value.active_work !== null) activeWork(value.active_work, "compact-change-v1.active_work");
  mapping(value.open_findings, "compact-change-v1.open_findings", findingRef, "finding_id"); mapping(value.material_decisions, "compact-change-v1.material_decisions", decisionRef, "decision_id"); mapping(value.evidence, "compact-change-v1.evidence", evidenceRef, "evidence_id");
  array(value.blockers, "compact-change-v1.blockers", diagnostic); mapping(value.remaining_work, "compact-change-v1.remaining_work", remainingWork, "work_id");
  validateCompactVocabulary("Readiness", value.readiness);
}

function validateReview(value) {
  exact(value, ["schema", "review_id", "target", "round", "subjects", "reviewer_authority", "outcome", "recording_status", "open_findings", "material_decisions", "limitations", "recorded_at"], "compact-review-v1");
  id(value.review_id, "compact-review-v1.review_id"); exact(value.target, ["target_id", "target_kind"], "compact-review-v1.target"); id(value.target.target_id, "compact-review-v1.target.target_id"); validateCompactVocabulary("ReviewTargetKind", value.target.target_kind); integer(value.round, "compact-review-v1.round", 1);
  mapping(value.subjects, "compact-review-v1.subjects", subject, "subject_id");
  if (!["proposal-review", "design-review", "delivery-review", "code-review"].includes(value.reviewer_authority)) throw new Error(`reviewer_authority: unknown_value ${String(value.reviewer_authority)}`);
  validateCompactVocabulary("ReviewOutcome", value.outcome); validateCompactVocabulary("ReviewRecordingStatus", value.recording_status); mapping(value.open_findings, "compact-review-v1.open_findings", finding, "finding_id"); stringArray(value.material_decisions, "compact-review-v1.material_decisions", id); stringArray(value.limitations, "compact-review-v1.limitations", text); timestamp(value.recorded_at, "compact-review-v1.recorded_at");
}

function validateDecisions(value) {
  exact(value, ["schema", "decisions"], "compact-decisions-v1");
  mapping(value.decisions, "compact-decisions-v1.decisions", (entry, label) => {
    exact(entry, ["decision_id", "source", "decision", "rationale", "affected_surfaces", "owner", "applicability", "applicable_since"], label); id(entry.decision_id, `${label}.decision_id`); exact(entry.source, ["kind", "id"], `${label}.source`); if (!["finding", "issue"].includes(entry.source.kind)) throw new Error(`${label}.source.kind: unknown_value ${String(entry.source.kind)}`); id(entry.source.id, `${label}.source.id`); text(entry.decision, `${label}.decision`); text(entry.rationale, `${label}.rationale`); stringArray(entry.affected_surfaces, `${label}.affected_surfaces`, text, 1); validateCompactVocabulary("Authority", entry.owner); validateCompactVocabulary("Applicability", entry.applicability); digest(entry.applicable_since, `${label}.applicable_since`);
  }, "decision_id", { minimum: 1 });
}

function validateEvidence(value) {
  exact(value, ["schema", "evidence"], "compact-evidence-v1");
  mapping(value.evidence, "compact-evidence-v1.evidence", (entry, label) => {
    exact(entry, ["evidence_id", "verifies", "subjects", "method", "outcome", "surfaces", "freshness", "invalidating_dependencies", "producer_authority", "detail_location", "required_rerun"], label); id(entry.evidence_id, `${label}.evidence_id`); stringArray(entry.verifies, `${label}.verifies`, id, 1); mapping(entry.subjects, `${label}.subjects`, subject, "subject_id"); text(entry.method, `${label}.method`); validateCompactVocabulary("EvidenceOutcome", entry.outcome); stringArray(entry.surfaces, `${label}.surfaces`, id, 1); validateCompactVocabulary("Freshness", entry.freshness); array(entry.invalidating_dependencies, `${label}.invalidating_dependencies`, (dependency, dependencyLabel) => { exact(dependency, ["kind", "id", "identity"], dependencyLabel); if (!["subject", "artifact", "review", "decision"].includes(dependency.kind)) throw new Error(`${dependencyLabel}.kind: unknown_value ${String(dependency.kind)}`); id(dependency.id, `${dependencyLabel}.id`); digest(dependency.identity, `${dependencyLabel}.identity`); }, { minimum: 1 }); for (let index = 1; index < entry.invalidating_dependencies.length; index += 1) { const prior = entry.invalidating_dependencies[index - 1]; const current = entry.invalidating_dependencies[index]; if (rawUtf8Compare(`${prior.kind}\0${prior.id}`, `${current.kind}\0${current.id}`) >= 0) throw new Error(`${label}.invalidating_dependencies must be unique and sorted`); } validateCompactVocabulary("Authority", entry.producer_authority); if (entry.detail_location !== null) detailLocation(entry.detail_location, `${label}.detail_location`); if ((entry.freshness === "stale") !== (entry.required_rerun !== null)) throw new Error(`${label}.required_rerun must be non-null exactly when stale`); if (entry.required_rerun !== null) text(entry.required_rerun, `${label}.required_rerun`);
  }, "evidence_id", { minimum: 1 });
}

function validateVerify(value) {
  exact(value, ["schema", "verification_id", "subjects", "verdict", "impact", "evidence_reused", "evidence_rerun", "limitations", "residual_risks", "explanation", "handoff", "recorded_at"], "compact-verify-v1"); id(value.verification_id, "compact-verify-v1.verification_id"); mapping(value.subjects, "compact-verify-v1.subjects", subject, "subject_id"); if (value.verdict !== "passed") throw new Error(`verdict: unknown_value ${String(value.verdict)}`); validateCompactVocabulary("VerifyImpact", value.impact); stringArray(value.evidence_reused, "compact-verify-v1.evidence_reused", id); stringArray(value.evidence_rerun, "compact-verify-v1.evidence_rerun", id); stringArray(value.limitations, "compact-verify-v1.limitations", text); stringArray(value.residual_risks, "compact-verify-v1.residual_risks", text); text(value.explanation, "compact-verify-v1.explanation"); validateCompactVocabulary("VerifyHandoff", value.handoff); timestamp(value.recorded_at, "compact-verify-v1.recorded_at");
}

function validateOperation(value) {
  exact(value, ["schema", "operation", "change_id", "expected_lifecycle_revision", "expected_files", "payload"], "compact-operation-v1"); validateCompactVocabulary("Operation", value.operation); id(value.change_id, "compact-operation-v1.change_id"); digest(value.expected_lifecycle_revision, "compact-operation-v1.expected_lifecycle_revision"); mapping(value.expected_files, "compact-operation-v1.expected_files", expectedFile, "path", { pathKeys: true }); operationPayload(value.payload, value.operation, "compact-operation-v1.payload");
}

function validateResult(value) {
  exact(value, ["schema", "status", "change_id", "prior_lifecycle_revision", "resulting_lifecycle_revision", "affected_paths", "bytes_changed", "blockers", "errors", "next_operation", "projection"], "compact-result-v1"); validateCompactVocabulary("ResultStatus", value.status); if (value.change_id !== null) id(value.change_id, "compact-result-v1.change_id"); digest(value.prior_lifecycle_revision, "compact-result-v1.prior_lifecycle_revision", true); digest(value.resulting_lifecycle_revision, "compact-result-v1.resulting_lifecycle_revision", true); stringArray(value.affected_paths, "compact-result-v1.affected_paths", validateCompactPath); boolean(value.bytes_changed, "compact-result-v1.bytes_changed"); array(value.blockers, "compact-result-v1.blockers", diagnostic); array(value.errors, "compact-result-v1.errors", diagnostic); if (value.next_operation !== null) validateCompactVocabulary("Operation", value.next_operation);
  if (value.projection !== null) {
    projection(value.projection, "compact-result-v1.projection");
    if (value.status !== "success" || value.prior_lifecycle_revision !== null || value.resulting_lifecycle_revision !== null || value.affected_paths.length !== 0 || value.bytes_changed) throw new Error("compact-result-v1 read-only projection success must not report mutation");
    if (value.change_id !== value.projection.change_id) throw new Error("compact-result-v1 projection change_id must equal result change_id");
  }
}

function recoveryFile(value, label, changeId) {
  exact(value, ["path", "prior_state", "prior_identity", "prior_content", "candidate_state", "candidate_identity", "candidate_content", "replacement_status"], label); validateCompactPath(value.path, `${label}.path`); validateCompactVocabulary("ExpectedFileState", value.prior_state); validateCompactVocabulary("ExpectedFileState", value.candidate_state); digest(value.prior_identity, `${label}.prior_identity`, true); digest(value.candidate_identity, `${label}.candidate_identity`, true); if (value.prior_content !== null) validateCompactPath(value.prior_content, `${label}.prior_content`); if (value.candidate_content !== null) validateCompactPath(value.candidate_content, `${label}.candidate_content`); if ((value.prior_state === "present") !== (value.prior_identity !== null && value.prior_content !== null)) throw new Error(`${label} prior fields must match state`); if ((value.candidate_state === "present") !== (value.candidate_identity !== null && value.candidate_content !== null)) throw new Error(`${label} candidate fields must match state`);
  const root = `.rigorloop/transactions/${changeId}`;
  if (value.prior_content !== null && !value.prior_content.startsWith(`${root}/prior/`)) throw new Error(`${label}.prior_content must be a descendant of the current transaction prior/ directory`);
  if (value.candidate_content !== null && !value.candidate_content.startsWith(`${root}/candidate/`)) throw new Error(`${label}.candidate_content must be a descendant of the current transaction candidate/ directory`);
  validateCompactVocabulary("ReplacementStatus", value.replacement_status);
}

function validateRecovery(value) {
  exact(value, ["schema", "transaction_id", "change_id", "phase", "prior_lifecycle_revision", "candidate_lifecycle_revision", "affected_files"], "compact-recovery-v1"); id(value.transaction_id, "compact-recovery-v1.transaction_id"); id(value.change_id, "compact-recovery-v1.change_id"); validateCompactVocabulary("RecoveryPhase", value.phase); digest(value.prior_lifecycle_revision, "compact-recovery-v1.prior_lifecycle_revision"); digest(value.candidate_lifecycle_revision, "compact-recovery-v1.candidate_lifecycle_revision"); array(value.affected_files, "compact-recovery-v1.affected_files", (entry, label) => recoveryFile(entry, label, value.change_id), { minimum: 1 }); for (let index = 1; index < value.affected_files.length; index += 1) if (rawUtf8Compare(value.affected_files[index - 1].path, value.affected_files[index].path) >= 0) throw new Error("compact-recovery-v1.affected_files must be sorted by path");
}

const VALIDATORS = Object.freeze({
  "compact-change-v1": validateChange,
  "compact-review-v1": validateReview,
  "compact-decisions-v1": validateDecisions,
  "compact-evidence-v1": validateEvidence,
  "compact-verify-v1": validateVerify,
  "compact-operation-v1": validateOperation,
  "compact-result-v1": validateResult,
  "compact-recovery-v1": validateRecovery,
});

export function validateCompactRecord(value, expectedSchema = null) {
  record(value, "compact record");
  validateCompactVocabulary("Schema", value.schema);
  if (expectedSchema !== null && value.schema !== expectedSchema) throw new Error(`schema mismatch: expected ${expectedSchema}, found ${String(value.schema)}`);
  VALIDATORS[value.schema](value);
  return value;
}

export function validateCompactProjection(value) {
  projection(value, "Projection");
  return value;
}

export function parseCompactYaml(source, expectedSchema = null) {
  if (typeof source !== "string" || Buffer.byteLength(source, "utf8") > MAX_DOCUMENT_BYTES) throw new Error("compact YAML exceeds the 8 MiB input limit or is not UTF-8 text");
  return validateCompactRecord(parseLifecycleYaml(source), expectedSchema);
}

export function parseCompactMarkdown(source, expectedSchema) {
  if (typeof source !== "string" || Buffer.byteLength(source, "utf8") > MAX_DOCUMENT_BYTES) throw new Error("compact Markdown exceeds the 8 MiB input limit or is not UTF-8 text");
  if (!source.startsWith("---\n")) throw new Error("compact Markdown requires YAML front matter");
  const end = source.indexOf("\n---\n", 4);
  if (end < 0) throw new Error("compact Markdown requires a closing front matter delimiter");
  const frontMatter = source.slice(4, end + 1);
  return { record: parseCompactYaml(frontMatter, expectedSchema), markdown: source.slice(end + 5) };
}

function sha256(value) {
  return `sha256:${createHash("sha256").update(value).digest("hex")}`;
}

export function compactLifecycleRevision({ changeBytes, files }) {
  if (typeof changeBytes !== "string" || Buffer.byteLength(changeBytes, "utf8") > MAX_DOCUMENT_BYTES) throw new Error("change.yaml exceeds the 8 MiB input limit or is not UTF-8 text");
  const matches = [...changeBytes.matchAll(/^lifecycle_revision: (sha256:[a-f0-9]{64})$/gm)];
  if (matches.length !== 1) throw new Error("change.yaml must contain exactly one plain-style lifecycle_revision");
  const changeIdMatch = changeBytes.match(/^change_id: ([A-Za-z0-9][A-Za-z0-9._-]{0,127})$/m);
  if (!changeIdMatch) throw new Error("change.yaml must contain one plain-style change_id");
  const contractMatches = [...changeBytes.matchAll(/^lifecycle_contract: ([^\s]+)$/gm)];
  if (contractMatches.length !== 1) throw new Error("change.yaml must contain exactly one plain-style lifecycle_contract");
  if (contractMatches[0][1] !== "compact-current-state-v1") throw new Error(`lifecycle_contract: unknown_value ${contractMatches[0][1]}`);
  const entries = files instanceof Map ? [...files.entries()] : Object.entries(files ?? {});
  const rows = entries.map(([path, content]) => {
    validateCompactPath(path, "authoritative file path");
    if (path.split("/").at(-1) === "change.yaml") throw new Error("authoritative files must exclude change.yaml");
    const bytes = Buffer.isBuffer(content) ? content : Buffer.from(content);
    if (bytes.length > MAX_DOCUMENT_BYTES) throw new Error(`${path} exceeds the 8 MiB file limit`);
    return { path, sha256: sha256(bytes) };
  }).sort((left, right) => rawUtf8Compare(left.path, right.path));
  for (let index = 1; index < rows.length; index += 1) if (rows[index - 1].path === rows[index].path) throw new Error(`duplicate authoritative file path ${rows[index].path}`);
  const sentinel = `sha256:${"0".repeat(64)}`;
  const coordinator = `${changeBytes.slice(0, matches[0].index)}lifecycle_revision: ${sentinel}${changeBytes.slice(matches[0].index + matches[0][0].length)}`;
  const coordinatorSha256 = sha256(coordinator);
  const manifest = `${JSON.stringify({ change_id: changeIdMatch[1], contract: "compact-current-state-v1", coordinator_sha256: coordinatorSha256, files: rows })}\n`;
  return { revision: sha256(manifest), manifest, coordinator_sha256: coordinatorSha256 };
}

function utf8(content, path) {
  if (typeof content === "string") return content;
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(content);
  } catch {
    throw new Error(`${path} must contain valid UTF-8`);
  }
}

export function validateCompactSet({ changeBytes, files }) {
  const changeSource = utf8(changeBytes, "change.yaml");
  const change = parseCompactYaml(changeSource, "compact-change-v1");
  const entries = files instanceof Map ? [...files.entries()] : Object.entries(files ?? {});
  const contentByPath = new Map(entries);
  const verifyPath = `docs/changes/${change.change_id}/verify-report.md`;
  const authoritativePaths = new Set([
    ...Object.values(change.artifacts).map((entry) => entry.path),
    ...Object.values(change.reviews).map((entry) => entry.path),
    ...Object.values(change.material_decisions).map((entry) => entry.path),
    ...Object.values(change.evidence).map((entry) => entry.manifest_path),
    ...(change.readiness === "verified" ? [verifyPath] : []),
  ]);
  for (const [path] of entries) if (!authoritativePaths.has(path)) throw new Error(`${path} is not a current authoritative path`);
  const identityByPath = new Map(entries.map(([path, content]) => {
    validateCompactPath(path, "authoritative file path");
    const bytes = Buffer.isBuffer(content) ? content : Buffer.from(content);
    if (bytes.length > MAX_DOCUMENT_BYTES) throw new Error(`${path} exceeds the 8 MiB file limit`);
    return [path, sha256(bytes)];
  }));
  const requireIdentity = (path, expected, label) => {
    if (!contentByPath.has(path)) throw new Error(`${label} references missing path ${path}`);
    if (identityByPath.get(path) !== expected) throw new Error(`${label} identity mismatch for ${path}`);
  };

  const artifactOwners = { proposal: "proposal", architecture: "architecture", adr: "architecture", spec: "spec", plan: "plan" };
  for (const artifact of Object.values(change.artifacts)) {
    requireIdentity(artifact.path, artifact.identity, `artifact ${artifact.artifact_id}`);
    if (artifact.owner !== artifactOwners[artifact.kind]) throw new Error(`artifact ${artifact.artifact_id} owner is inconsistent with its kind`);
  }

  const reviews = Object.create(null);
  for (const reviewRefValue of Object.values(change.reviews)) {
    requireIdentity(reviewRefValue.path, reviewRefValue.identity, `review ${reviewRefValue.target_id}`);
    const review = parseCompactMarkdown(utf8(contentByPath.get(reviewRefValue.path), reviewRefValue.path), "compact-review-v1").record;
    if (review.target.target_id !== reviewRefValue.target_id || review.review_id !== reviewRefValue.review_id || review.outcome !== reviewRefValue.outcome || review.reviewer_authority !== reviewRefValue.reviewer_authority) throw new Error(`review ${reviewRefValue.target_id} reference is inconsistent`);
    const reviewerByKind = { proposal: "proposal-review", "design-package": "design-review", "delivery-package": "delivery-review", milestone: "code-review", "final-code": "code-review" };
    if (review.reviewer_authority !== reviewerByKind[review.target.target_kind]) throw new Error(`review ${reviewRefValue.target_id} responsibility is inconsistent with its target kind`);
    const stableNames = { proposal: "proposal-review.md", "design-package": "design-review.md", "delivery-package": "delivery-review.md", "final-code": "code-review-final.md" };
    const expectedReviewPath = `docs/changes/${change.change_id}/reviews/${stableNames[review.target.target_kind] ?? `code-review-${review.target.target_id}.md`}`;
    if (reviewRefValue.path !== expectedReviewPath) throw new Error(`review ${reviewRefValue.target_id} does not use its stable canonical path`);
    const reviewedKinds = { proposal: new Set(["proposal"]), "design-package": new Set(["architecture", "adr", "spec"]), "delivery-package": new Set(["plan"]) }[review.target.target_kind];
    if (reviewedKinds) {
      const expectedSubjects = Object.values(change.artifacts).filter((entry) => reviewedKinds.has(entry.kind));
      if (expectedSubjects.length !== Object.keys(review.subjects).length) throw new Error(`review ${reviewRefValue.target_id} subject set is incomplete`);
      for (const artifact of expectedSubjects) {
        const reviewed = review.subjects[artifact.artifact_id];
        if (!reviewed || reviewed.path !== artifact.path || reviewed.identity !== artifact.identity) throw new Error(`review ${reviewRefValue.target_id} subject ${artifact.artifact_id} is not current`);
      }
    }
    reviews[reviewRefValue.target_id] = review;
  }

  for (const findingRefValue of Object.values(change.open_findings)) {
    requireIdentity(findingRefValue.review_path, findingRefValue.review_identity, `finding ${findingRefValue.finding_id}`);
    const review = Object.hasOwn(reviews, findingRefValue.review_target_id) ? reviews[findingRefValue.review_target_id] : null;
    const findingValue = review?.open_findings?.[findingRefValue.finding_id];
    if (!findingValue) throw new Error(`finding ${findingRefValue.finding_id} is absent from its current review`);
    for (const field of ["finding_id", "owner", "severity", "blocking_effect"]) if (findingValue[field] !== findingRefValue[field]) throw new Error(`finding ${findingRefValue.finding_id} reference is inconsistent`);
  }
  const reviewFindingOwners = new Map();
  for (const [targetId, review] of Object.entries(reviews)) {
    for (const decisionId of review.material_decisions) if (!Object.hasOwn(change.material_decisions, decisionId)) throw new Error(`review ${targetId} references missing material decision ${decisionId}`);
    for (const findingValue of Object.values(review.open_findings)) {
      const priorTarget = reviewFindingOwners.get(findingValue.finding_id);
      if (priorTarget && priorTarget !== targetId) throw new Error(`finding ${findingValue.finding_id} occurs in multiple current reviews`);
      reviewFindingOwners.set(findingValue.finding_id, targetId);
      const reference = Object.hasOwn(change.open_findings, findingValue.finding_id) ? change.open_findings[findingValue.finding_id] : null;
      if (!reference) throw new Error(`finding ${findingValue.finding_id} is omitted from change.yaml`);
      if (reference.review_target_id !== targetId) throw new Error(`finding ${findingValue.finding_id} review target is inconsistent`);
    }
  }

  const decisions = Object.create(null);
  for (const decisionRefValue of Object.values(change.material_decisions)) {
    requireIdentity(decisionRefValue.path, decisionRefValue.identity, `decision ${decisionRefValue.decision_id}`);
    if (!decisions[decisionRefValue.path]) decisions[decisionRefValue.path] = parseCompactMarkdown(utf8(contentByPath.get(decisionRefValue.path), decisionRefValue.path), "compact-decisions-v1").record;
    const decisionValues = decisions[decisionRefValue.path].decisions;
    const decisionValue = Object.hasOwn(decisionValues, decisionRefValue.decision_id) ? decisionValues[decisionRefValue.decision_id] : null;
    if (!decisionValue || decisionValue.applicability !== decisionRefValue.applicability) throw new Error(`decision ${decisionRefValue.decision_id} reference is inconsistent`);
  }
  for (const [path, recordValue] of Object.entries(decisions)) {
    for (const decisionValue of Object.values(recordValue.decisions)) {
      const reference = Object.hasOwn(change.material_decisions, decisionValue.decision_id) ? change.material_decisions[decisionValue.decision_id] : null;
      if (!reference || reference.path !== path) throw new Error(`decision ${decisionValue.decision_id} is omitted from change.yaml`);
    }
  }

  const evidence = Object.create(null);
  for (const evidenceRefValue of Object.values(change.evidence)) {
    requireIdentity(evidenceRefValue.manifest_path, evidenceRefValue.manifest_identity, `evidence ${evidenceRefValue.evidence_id}`);
    if (!evidence[evidenceRefValue.manifest_path]) evidence[evidenceRefValue.manifest_path] = parseCompactYaml(utf8(contentByPath.get(evidenceRefValue.manifest_path), evidenceRefValue.manifest_path), "compact-evidence-v1");
    const evidenceValues = evidence[evidenceRefValue.manifest_path].evidence;
    const evidenceValue = Object.hasOwn(evidenceValues, evidenceRefValue.evidence_id) ? evidenceValues[evidenceRefValue.evidence_id] : null;
    if (!evidenceValue || evidenceValue.freshness !== evidenceRefValue.freshness) throw new Error(`evidence ${evidenceRefValue.evidence_id} reference is inconsistent`);
    for (const dependency of evidenceValue.invalidating_dependencies) {
      let actual = null;
      if (dependency.kind === "subject") actual = evidenceValue.subjects[dependency.id]?.identity ?? null;
      else if (dependency.kind === "artifact") actual = change.artifacts[dependency.id]?.identity ?? null;
      else if (dependency.kind === "review") actual = change.reviews[dependency.id]?.identity ?? null;
      else actual = change.material_decisions[dependency.id]?.identity ?? null;
      if (actual === null) throw new Error(`evidence ${evidenceValue.evidence_id} dependency ${dependency.kind}:${dependency.id} does not resolve`);
      if (evidenceValue.freshness === "current" && actual !== dependency.identity) throw new Error(`evidence ${evidenceValue.evidence_id} current dependency ${dependency.kind}:${dependency.id} is stale`);
    }
  }
  for (const [path, recordValue] of Object.entries(evidence)) {
    for (const evidenceValue of Object.values(recordValue.evidence)) {
      const reference = Object.hasOwn(change.evidence, evidenceValue.evidence_id) ? change.evidence[evidenceValue.evidence_id] : null;
      if (!reference || reference.manifest_path !== path) throw new Error(`evidence ${evidenceValue.evidence_id} is omitted from change.yaml`);
    }
  }

  let verify = null;
  if (contentByPath.has(verifyPath)) verify = parseCompactMarkdown(utf8(contentByPath.get(verifyPath), verifyPath), "compact-verify-v1").record;
  if ((change.readiness === "verified") !== (verify !== null)) throw new Error("Verify report presence must match verified readiness");
  for (const evidenceId of new Set([...(verify?.evidence_reused ?? []), ...(verify?.evidence_rerun ?? [])])) {
    if (!Object.hasOwn(change.evidence, evidenceId) || change.evidence[evidenceId].freshness !== "current") throw new Error(`Verify evidence ${evidenceId} must resolve to a current evidence entry`);
  }

  const computed = compactLifecycleRevision({ changeBytes: changeSource, files: contentByPath });
  if (computed.revision !== change.lifecycle_revision) throw new Error(`lifecycle revision mismatch: expected ${change.lifecycle_revision}, computed ${computed.revision}`);
  return { change, reviews, decisions, evidence, verify, manifest: computed.manifest };
}
