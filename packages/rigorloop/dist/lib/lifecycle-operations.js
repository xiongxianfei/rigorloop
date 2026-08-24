import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync } from "node:fs";
import { relative, resolve, sep } from "node:path";

const REVIEW_OUTCOMES = new Set(["approved", "changes-requested", "blocked", "inconclusive", "clean-with-notes"]);
const RESOLUTION_DISPOSITIONS = new Set(["accepted", "rejected", "deferred", "partially-accepted", "needs-decision"]);

function operationError(code, summary, invariant, identities = [], correctiveOperation = null) {
  const error = new Error(`${code}: ${summary}`);
  error.code = code;
  error.diagnostic = { code, summary, blocking_invariant: invariant, relevant_identities: identities, corrective_operation: correctiveOperation };
  return error;
}

function digest(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function safeFile(root, path) {
  if (typeof path !== "string" || !path || path.startsWith("/") || path.includes("\\") || path.split("/").some((part) => !part || part === "." || part === "..")) {
    throw operationError("RL_INVALID_REQUEST", "evidence path is not normalized and repository-relative", "repository-path", [String(path)]);
  }
  const absolute = resolve(root, path);
  const rel = relative(root, absolute);
  if (rel === ".." || rel.startsWith(`..${sep}`)) throw operationError("RL_INVALID_REQUEST", "evidence path escapes the repository", "repository-path", [path]);
  let cursor = root;
  for (const part of path.split("/")) {
    cursor = resolve(cursor, part);
    if (existsSync(cursor) && lstatSync(cursor).isSymbolicLink()) throw operationError("RL_INVALID_REQUEST", "evidence path traverses a symlink", "repository-path", [path]);
  }
  if (!existsSync(absolute) || !lstatSync(absolute).isFile()) throw operationError("RL_INVALID_REQUEST", "evidence path must identify an existing regular file", "evidence-exists", [path]);
  const bytes = readFileSync(absolute);
  return { path, bytes, sha256: digest(bytes), text: bytes.toString("utf8") };
}

function metadata(text, name) {
  const match = text.match(new RegExp(`^${name}:\\s*(.+)$`, "mi"));
  return match?.[1]?.trim().replace(/^`|`$/g, "") ?? null;
}

function coordination(change) {
  const current = change.lifecycle_cli;
  if (current === undefined) return { schema_version: 1, reviews: {}, validations: {}, resolutions: {} };
  if (!current || typeof current !== "object" || current.schema_version !== 1) throw operationError("RL_UNSUPPORTED_SCHEMA", "unsupported lifecycle_cli coordination schema", "coordination-schema", [String(current?.schema_version)], "migrate");
  return structuredClone(current);
}

function artifact(change, artifactId) {
  const value = change.artifact_states?.[artifactId];
  if (!value) throw operationError("RL_INVALID_REQUEST", `unknown artifact ${artifactId}`, "artifact-identity", [artifactId]);
  return value;
}

function artifactIdentity(root, entry) {
  return safeFile(root, entry.path);
}

function alreadyRecorded(existing, requested) {
  if (!existing) return false;
  if (JSON.stringify(existing) === JSON.stringify(requested)) return true;
  throw operationError("RL_OPERATION_NOT_PERMITTED", "conflicting durable facts are already registered", "idempotent-registration");
}

function reviewOutcome(text) {
  const outcome = metadata(text, "(?:Review status|Status)");
  if (!REVIEW_OUTCOMES.has(outcome)) throw operationError("RL_INVALID_REQUEST", "review evidence has an unknown or missing outcome", "review-outcome", [String(outcome)]);
  return outcome;
}

function identityValue(value) {
  return String(value ?? "").replace(/^sha256:/, "");
}

function findingSet(value) {
  if (!value || value.trim().toLowerCase() === "none") return [];
  return value.split(",").map((item) => item.trim().replace(/`/g, "")).filter(Boolean).sort();
}

function expectedReviewAuthority(kind) {
  return kind === "adr" ? "architecture-review" : `${kind}-review`;
}

function requireLogEntry(root, changeId, reviewId) {
  const log = safeFile(root, `docs/changes/${changeId}/review-log.md`);
  const marker = `Review ID: ${reviewId}`;
  const markerIndex = log.text.indexOf(marker);
  if (markerIndex >= 0) {
    const nextEntry = log.text.indexOf("\n### Review entry", markerIndex + marker.length);
    return { ...log, entry_text: log.text.slice(markerIndex, nextEntry < 0 ? undefined : nextEntry) };
  }
  const findingMarker = `Finding ID: ${reviewId}`;
  const findingIndex = log.text.indexOf(findingMarker);
  if (findingIndex >= 0) return { ...log, entry_text: log.text.slice(findingIndex, log.text.indexOf("\n### Review entry", findingIndex + findingMarker.length) < 0 ? undefined : log.text.indexOf("\n### Review entry", findingIndex + findingMarker.length)) };
  const tableLine = log.text.split("\n").find((line) => line.includes(`\`${reviewId}\``));
  if (tableLine) return { ...log, entry_text: tableLine };
  throw operationError("RL_INVALID_REQUEST", "review log does not contain the review or finding occurrence", "review-log-consistency", [reviewId]);
}

export function evaluateLifecycleOperation({ root, change, request }) {
  const next = structuredClone(change);
  const state = coordination(next);
  next.lifecycle_cli = state;
  const target = request.artifact_id ? artifact(next, request.artifact_id) : null;
  const targetIdentity = target ? artifactIdentity(root, target) : null;

  if (request.operation === "record-review") {
    const evidence = safeFile(root, request.evidence_path);
    const reviewId = metadata(evidence.text, "Review ID");
    const round = metadata(evidence.text, "Round");
    const outcome = reviewOutcome(evidence.text);
    const reviewedPath = metadata(evidence.text, "Reviewed artifact path");
    const reviewedIdentity = metadata(evidence.text, "Reviewed artifact identity");
    const findings = findingSet(metadata(evidence.text, "Material findings"));
    if (!reviewId || !/^r\d+$/.test(round ?? "")) throw operationError("RL_INVALID_REQUEST", "review evidence requires Review ID and r<n> Round", "review-shape", [request.evidence_path]);
    if (reviewedPath !== target.path || identityValue(reviewedIdentity) !== targetIdentity.sha256) throw operationError("RL_STALE_EVIDENCE", "review evidence does not name the exact current artifact", "reviewed-artifact-identity", [String(reviewedPath), String(reviewedIdentity), target.path, targetIdentity.sha256]);
    if (request.stage_authority !== expectedReviewAuthority(target.kind)) throw operationError("RL_AUTHORITY_BOUNDARY", "review authority does not own the target artifact", "stage-authority", [request.stage_authority, expectedReviewAuthority(target.kind)]);
    const log = requireLogEntry(root, change.change_id, reviewId);
    const loggedFindings = log.entry_text.startsWith("|") && /\|\s*0\s*\|\s*`?recorded`?\s*\|\s*$/.test(log.entry_text)
      ? []
      : findingSet(metadata(log.entry_text, "Material findings"));
    if (JSON.stringify(findings) !== JSON.stringify(loggedFindings)) throw operationError("RL_INVALID_REQUEST", "review evidence and review log finding sets differ", "review-log-consistency", [...findings, ...loggedFindings]);
    const registration = { review_id: reviewId, round, outcome, findings, artifact_path: target.path, artifact_sha256: targetIdentity.sha256, evidence_path: evidence.path, evidence_sha256: evidence.sha256, review_log_sha256: log.sha256, stage_authority: request.stage_authority };
    if (alreadyRecorded(state.reviews[request.artifact_id], registration)) return { status: "already-recorded", candidate: change };
    state.reviews[request.artifact_id] = registration;
    return { status: "recorded", candidate: next };
  }

  if (request.operation === "record-validation") {
    const evidence = safeFile(root, request.evidence_path);
    const subject = safeFile(root, request.subject_path);
    if (subject.path !== target.path) throw operationError("RL_AUTHORITY_BOUNDARY", "validation subject must be the registered target artifact", "validation-subject", [subject.path, target.path]);
    if (metadata(evidence.text, "Subject path") !== subject.path || identityValue(metadata(evidence.text, "Subject identity")) !== subject.sha256) throw operationError("RL_STALE_EVIDENCE", "validation evidence does not name the exact current subject", "validation-subject-identity", [subject.path, subject.sha256]);
    if (!metadata(evidence.text, "Validation result")) throw operationError("RL_INVALID_REQUEST", "validation evidence must record a result without implying approval", "validation-evidence-shape", [evidence.path]);
    const registration = { artifact_path: target.path, artifact_sha256: targetIdentity.sha256, subject_path: subject.path, subject_sha256: subject.sha256, evidence_path: evidence.path, evidence_sha256: evidence.sha256, stage_authority: request.stage_authority };
    if (alreadyRecorded(state.validations[request.artifact_id], registration)) return { status: "already-recorded", candidate: change };
    state.validations[request.artifact_id] = registration;
    return { status: "recorded", candidate: next };
  }

  if (request.operation === "record-finding-resolution") {
    const evidence = safeFile(root, request.evidence_path);
    if (!evidence.text.includes(`Finding ID: ${request.finding_id}`)) throw operationError("RL_INVALID_REQUEST", "resolution evidence does not contain the finding identity", "resolution-consistency", [request.finding_id]);
    const disposition = metadata(evidence.text, "Disposition");
    const owner = metadata(evidence.text, "Owner");
    const status = metadata(evidence.text, "Status");
    const validationEvidence = metadata(evidence.text, "Validation evidence");
    if (!RESOLUTION_DISPOSITIONS.has(disposition) || !owner || status !== "resolved" || !validationEvidence || /^pending$/i.test(validationEvidence)) throw operationError("RL_INVALID_REQUEST", "resolution requires a closed disposition, owner, resolved status, and validation evidence", "resolution-shape", [request.finding_id]);
    requireLogEntry(root, change.change_id, request.finding_id);
    const registration = { finding_id: request.finding_id, disposition, owner, evidence_path: evidence.path, evidence_sha256: evidence.sha256, stage_authority: request.stage_authority };
    if (alreadyRecorded(state.resolutions[request.finding_id], registration)) return { status: "already-recorded", candidate: change };
    state.resolutions[request.finding_id] = registration;
    return { status: "recorded", candidate: next };
  }

  if (request.operation === "settle-artifact") {
    const review = state.reviews[request.artifact_id];
    if (!review) throw operationError("RL_OPERATION_NOT_PERMITTED", "artifact has no registered review", "review-registration", [request.artifact_id], "record-review");
    if (review.stage_authority !== request.stage_authority) throw operationError("RL_AUTHORITY_BOUNDARY", "settlement authority differs from the registered review", "stage-authority", [request.stage_authority, review.stage_authority]);
    if (request.stage_authority !== expectedReviewAuthority(target.kind)) throw operationError("RL_AUTHORITY_BOUNDARY", "settlement authority does not own the target artifact", "stage-authority", [request.stage_authority, expectedReviewAuthority(target.kind)]);
    const evidence = safeFile(root, review.evidence_path);
    if (review.artifact_sha256 !== targetIdentity.sha256 || review.evidence_sha256 !== evidence.sha256) throw operationError("RL_STALE_EVIDENCE", "review or artifact identity is stale", "evidence-freshness", [request.artifact_id], "record-review");
    const log = requireLogEntry(root, change.change_id, review.review_id);
    if (review.review_log_sha256 !== log.sha256) throw operationError("RL_STALE_EVIDENCE", "review log changed after registration", "review-log-freshness", [review.review_id], "record-review");
    const openFindings = [...log.text.matchAll(/^Open findings:[ \t]*(.*)$/gmi)]
      .map((match) => match[1].trim())
      .filter((value) => value && value.toLowerCase() !== "none");
    if (openFindings.length) throw operationError("RL_UNRESOLVED_MATERIAL_FINDING", "material review findings remain open", "finding-closeout", openFindings, "record-finding-resolution");
    const desired = review.outcome === "approved" || review.outcome === "clean-with-notes"
      ? ({ proposal: "accepted", spec: "approved", architecture: "approved", plan: "active", "test-spec": "active", adr: "accepted" }[target.kind] ?? "approved")
      : review.outcome === "changes-requested" ? "revision-required" : "blocked";
    if (target.lifecycle_state === desired) return { status: "already-recorded", candidate: change };
    target.lifecycle_state = desired;
    target.review = { id: review.review_id, artifact_id: request.artifact_id, outcome: review.outcome === "clean-with-notes" ? "approved" : review.outcome, record: review.evidence_path, round: review.round, ...(target.kind === "adr" && desired === "accepted" ? { adr_settlement: "accepted" } : {}) };
    return { status: "settled", candidate: next };
  }

  throw operationError("RL_INVALID_REQUEST", `operation ${request.operation} is not implemented by the evidence evaluator`, "operation-vocabulary", [request.operation]);
}

export function operationDiagnostic(error) {
  return error.diagnostic ?? { code: error.code ?? "RL_POST_VALIDATION_FAILED", summary: error.message, blocking_invariant: "lifecycle-operation", relevant_identities: [], corrective_operation: null };
}
