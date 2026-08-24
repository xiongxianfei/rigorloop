import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync } from "node:fs";
import { relative, resolve, sep } from "node:path";

const REVIEW_OUTCOMES = new Set(["approved", "changes-requested", "blocked", "inconclusive", "clean-with-notes"]);
const RESOLUTION_DISPOSITIONS = new Set(["accepted", "rejected", "deferred", "partially-accepted", "needs-decision"]);
const ARTIFACT_KINDS = new Set(["proposal", "spec", "architecture", "adr", "plan", "test-spec"]);
const ARTIFACT_ROLES = new Set(["primary", "supporting"]);

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
  const match = text.match(new RegExp(`^(?:[-*]\\s*)?${name}:\\s*(.+)$`, "mi"));
  return match?.[1]?.trim().replace(/^`|`$/g, "") ?? null;
}

function reviewedTarget(text, target) {
  const pathLine = text.split("\n").find((line) => line.includes(target.path));
  const path = metadata(text, "Reviewed artifact path") ?? (pathLine ? target.path : null);
  const targetLineIdentity = pathLine?.match(/sha256:([a-f0-9]{64})/)?.[1] ?? null;
  const declaredIdentity = identityValue(metadata(text, "Reviewed artifact identity") ?? metadata(text, "Reviewed artifact"));
  const sha256 = targetLineIdentity ?? (/^[a-f0-9]{64}$/.test(declaredIdentity) ? declaredIdentity : null);
  return { path, sha256 };
}

function authoredTarget(text, path) {
  const pathLine = text.split("\n").find((line) => line.includes(path));
  const declaredPath = metadata(text, "Artifact path") ?? (pathLine ? path : null);
  const lineIdentity = pathLine?.match(/sha256:([a-f0-9]{64})/)?.[1] ?? null;
  const declaredIdentity = identityValue(metadata(text, "Artifact identity"));
  return { path: declaredPath, sha256: lineIdentity ?? (/^[a-f0-9]{64}$/.test(declaredIdentity) ? declaredIdentity : null) };
}

function coordination(change) {
  const current = change.lifecycle_cli;
  if (current === undefined) return { schema_version: 1, artifacts: {}, reviews: {}, validations: {}, resolutions: {}, milestones: {} };
  if (!current || typeof current !== "object" || current.schema_version !== 1) throw operationError("RL_UNSUPPORTED_SCHEMA", "unsupported lifecycle_cli coordination schema", "coordination-schema", [String(current?.schema_version)], "migrate");
  return { artifacts: {}, reviews: {}, validations: {}, resolutions: {}, milestones: {}, ...structuredClone(current) };
}

function expectedAuthorAuthority(kind) {
  return kind === "adr" ? "architecture" : kind;
}

function migrateArtifactRegistrations(root, change) {
  const registrations = {};
  for (const [artifactId, entry] of Object.entries(change.artifact_states ?? {})) {
    if (!entry || !ARTIFACT_KINDS.has(entry.kind) || !ARTIFACT_ROLES.has(entry.role) || !entry.path) {
      throw operationError("RL_UNSUPPORTED_SCHEMA", "legacy artifact cannot be migrated without a supported kind, role, and path", "migration-artifact-shape", [artifactId, String(entry?.kind), String(entry?.role), String(entry?.path)]);
    }
    const identity = artifactIdentity(root, entry);
    const registration = {
      artifact_kind: entry.kind,
      artifact_role: entry.role,
      artifact_path: entry.path,
      artifact_sha256: identity.sha256,
      stage_authority: expectedAuthorAuthority(entry.kind),
    };
    if (entry.authoring_evidence) {
      const evidence = safeFile(root, entry.authoring_evidence);
      registration.authoring_evidence_path = evidence.path;
      registration.authoring_evidence_sha256 = evidence.sha256;
    }
    registrations[artifactId] = registration;
  }
  return registrations;
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
  const target = request.artifact_id && request.operation !== "record-artifact-revision" ? artifact(next, request.artifact_id) : request.artifact_id ? next.artifact_states?.[request.artifact_id] ?? null : null;
  const targetIdentity = target ? artifactIdentity(root, target) : null;

  if (request.operation === "record-artifact-revision") {
    const authored = safeFile(root, request.artifact_path);
    const evidence = safeFile(root, request.evidence_path);
    const evidenced = authoredTarget(evidence.text, authored.path);
    const authoringResult = metadata(evidence.text, "Authoring result") ?? metadata(evidence.text, "Evidence state");
    if (evidenced.path !== authored.path || evidenced.sha256 !== authored.sha256 || authoringResult !== "complete") throw operationError("RL_STALE_EVIDENCE", "authoring evidence does not bind the exact completed artifact", "authoring-evidence-identity", [authored.path, authored.sha256, String(evidenced.path), String(evidenced.sha256)]);
    if (request.stage_authority !== expectedAuthorAuthority(request.artifact_kind)) throw operationError("RL_AUTHORITY_BOUNDARY", "authoring authority does not own the artifact kind", "stage-authority", [request.stage_authority, expectedAuthorAuthority(request.artifact_kind)]);
    const registration = { artifact_kind: request.artifact_kind, artifact_role: request.artifact_role, artifact_path: authored.path, artifact_sha256: authored.sha256, authoring_evidence_path: evidence.path, authoring_evidence_sha256: evidence.sha256, stage_authority: request.stage_authority };
    const existingRegistration = state.artifacts[request.artifact_id];
    if (!target) {
      if (request.prior_artifact_sha256 !== undefined) throw operationError("RL_INVALID_REQUEST", "creation must not supply a prior artifact identity", "artifact-revision-mode", [request.artifact_id]);
      const pathCollision = Object.entries(next.artifact_states ?? {}).find(([, entry]) => entry?.path === request.artifact_path);
      if (pathCollision) throw operationError("RL_OPERATION_NOT_PERMITTED", "artifact path is already registered", "artifact-path-identity", [request.artifact_path, pathCollision[0]]);
      next.artifact_states ??= {};
      next.artifact_states[request.artifact_id] = { kind: request.artifact_kind, path: request.artifact_path, role: request.artifact_role, lifecycle_state: "review-required", authoring_evidence: request.evidence_path };
    } else {
      if (target.kind !== request.artifact_kind || target.role !== request.artifact_role || target.path !== request.artifact_path) throw operationError("RL_AUTHORITY_BOUNDARY", "revision cannot change artifact kind, role, or path", "artifact-entry-identity", [request.artifact_id]);
      if (!request.prior_artifact_sha256) {
        if (alreadyRecorded(existingRegistration, registration) && target.lifecycle_state === "review-required") return { status: "already-recorded", candidate: change };
        throw operationError("RL_INVALID_REQUEST", "revision requires the prior artifact identity", "artifact-prior-identity", [request.artifact_id]);
      }
      if (!existingRegistration || existingRegistration.artifact_sha256 !== request.prior_artifact_sha256) throw operationError("RL_STALE_EVIDENCE", "prior artifact identity is not the registered current identity", "artifact-prior-identity", [request.artifact_id, request.prior_artifact_sha256], "record-artifact-revision");
      target.lifecycle_state = "review-required";
      target.authoring_evidence = request.evidence_path;
      delete target.review;
      delete state.reviews[request.artifact_id];
      delete state.validations[request.artifact_id];
      for (const [findingId, resolution] of Object.entries(state.resolutions)) if (resolution.artifact_id === request.artifact_id) delete state.resolutions[findingId];
      if (request.artifact_kind === "plan") state.milestones = {};
    }
    state.artifacts[request.artifact_id] = registration;
    return { status: "recorded", candidate: next };
  }

  if (request.operation === "record-review") {
    const evidence = safeFile(root, request.evidence_path);
    const reviewId = metadata(evidence.text, "Review ID");
    const rawRound = metadata(evidence.text, "Round");
    const round = /^\d+$/.test(rawRound ?? "") ? `r${rawRound}` : rawRound;
    const outcome = reviewOutcome(evidence.text);
    const reviewed = reviewedTarget(evidence.text, target);
    const findings = findingSet(metadata(evidence.text, "Material findings"));
    if (!reviewId || !/^r\d+$/.test(round ?? "")) throw operationError("RL_INVALID_REQUEST", "review evidence requires Review ID and r<n> Round", "review-shape", [request.evidence_path]);
    if (reviewed.path !== target.path || reviewed.sha256 !== targetIdentity.sha256) throw operationError("RL_STALE_EVIDENCE", "review evidence does not name the exact current artifact", "reviewed-artifact-identity", [String(reviewed.path), String(reviewed.sha256), target.path, targetIdentity.sha256]);
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
    const registration = { artifact_id: request.artifact_id, finding_id: request.finding_id, disposition, owner, evidence_path: evidence.path, evidence_sha256: evidence.sha256, stage_authority: request.stage_authority };
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

  if (request.operation === "start-milestone") {
    const planned = next.workflow_state?.planned_work;
    const milestones = planned?.milestones;
    const targetMilestone = milestones?.[request.milestone_id];
    if (!planned || !targetMilestone || planned.current_milestone !== request.milestone_id || targetMilestone.kind !== "implementation") throw operationError("RL_MILESTONE_ORDER", "requested milestone is not the unique current implementation milestone", "milestone-selection", [request.milestone_id]);
    if (targetMilestone.state === "implementing") return { status: "already-recorded", candidate: change };
    if (targetMilestone.state !== "planned") throw operationError("RL_OPERATION_NOT_PERMITTED", "milestone cannot start from its current state", "milestone-state", [request.milestone_id, String(targetMilestone.state)]);
    const ordered = Object.keys(milestones);
    const predecessors = ordered.slice(0, ordered.indexOf(request.milestone_id));
    const incomplete = predecessors.filter((id) => milestones[id].kind === "implementation" && milestones[id].state !== "closed");
    if (incomplete.length) throw operationError("RL_MILESTONE_ORDER", "required predecessor milestones are incomplete", "milestone-predecessors", incomplete);
    targetMilestone.state = "implementing";
    return { status: "started", candidate: next };
  }

  if (request.operation === "complete-milestone") {
    const planned = next.workflow_state?.planned_work;
    const targetMilestone = planned?.milestones?.[request.milestone_id];
    if (!planned || planned.current_milestone !== request.milestone_id || !targetMilestone || targetMilestone.kind !== "implementation") throw operationError("RL_MILESTONE_ORDER", "requested milestone is not the unique current implementation milestone", "milestone-selection", [request.milestone_id]);
    if (targetMilestone.state === "closed") return { status: "already-recorded", candidate: change };
    if (targetMilestone.state !== "review-requested" && targetMilestone.state !== "implementing") throw operationError("RL_OPERATION_NOT_PERMITTED", "milestone cannot complete from its current state", "milestone-state", [request.milestone_id, String(targetMilestone.state)]);
    const review = planned.latest_review;
    if (!review || review.milestone_id !== request.milestone_id || review.status !== "approved") throw operationError("RL_OPERATION_NOT_PERMITTED", "milestone completion requires its approved code review", "milestone-review", [request.milestone_id], "record-review");
    const evidence = safeFile(root, request.evidence_path);
    if (metadata(evidence.text, "Milestone") !== request.milestone_id || !/^pass(?:ed)?$/i.test(metadata(evidence.text, "Validation result") ?? "")) throw operationError("RL_INVALID_REQUEST", "milestone evidence must name the milestone and passing validation", "milestone-proof", [request.milestone_id, evidence.path]);
    state.milestones[request.milestone_id] = { evidence_path: evidence.path, evidence_sha256: evidence.sha256, review_round: review.round, stage_authority: request.stage_authority };
    targetMilestone.state = "closed";
    planned.remaining_implementation_milestones = (planned.remaining_implementation_milestones ?? []).filter((id) => id !== request.milestone_id);
    return { status: "completed", candidate: next };
  }

  if (request.operation === "migrate") {
    if (request.source_schema_version !== 1) throw operationError("RL_UNSUPPORTED_SCHEMA", "only legacy coordination schema 1 is supported for migration", "migration-source", [String(request.source_schema_version)]);
    if (change.lifecycle_cli?.schema_version === 1) return { status: "already-recorded", candidate: change };
    next.lifecycle_cli = { schema_version: 1, artifacts: migrateArtifactRegistrations(root, change), reviews: {}, validations: {}, resolutions: {}, milestones: {} };
    return { status: "migrated", candidate: next };
  }

  throw operationError("RL_INVALID_REQUEST", `operation ${request.operation} is not implemented by the evidence evaluator`, "operation-vocabulary", [request.operation]);
}

export function operationDiagnostic(error) {
  return error.diagnostic ?? { code: error.code ?? "RL_POST_VALIDATION_FAILED", summary: error.message, blocking_invariant: "lifecycle-operation", relevant_identities: [], corrective_operation: null };
}
