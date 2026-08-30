import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync, readdirSync } from "node:fs";
import { join, relative, resolve, sep } from "node:path";

import { canonicalJson, parseLifecycleYaml } from "./lifecycle-contract.js";
import { packageProjection, readPackageReview, reviewPackageContext } from "./lifecycle-packages.js";
import { stageTransitionDecision } from "./lifecycle-stage-routing.js";

const REVIEW_OUTCOMES = new Set(["approved", "changes-requested", "blocked", "inconclusive", "clean-with-notes"]);
const RESOLUTION_DISPOSITIONS = new Set(["accepted", "rejected", "deferred", "partially-accepted", "needs-decision"]);
const ARTIFACT_KINDS = new Set(["proposal", "spec", "architecture", "adr", "plan", "test-spec"]);
const ARTIFACT_ROLES = new Set(["primary", "supporting"]);
const CORRECTION_STAGE_ORDER = ["proposal", "proposal-review", "architecture", "spec", "design-review", "plan", "test-spec", "delivery-review", "implement", "code-review", "review-resolution", "explain-change", "verify", "pr"];
const GOVERNED_LIFECYCLE_CONTRACT = /^lifecycle_contract:\s*(?:stage-owned-change-local-v1|"stage-owned-change-local-v1"|'stage-owned-change-local-v1')\s*(?:#.*)?$/m;

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
  if (current === undefined) return { schema_version: 1, artifacts: {}, reviews: {}, package_reviews: {}, validations: {}, resolutions: {}, milestones: {} };
  if (!current || typeof current !== "object" || ![1, 2].includes(current.schema_version)) throw operationError("RL_UNSUPPORTED_SCHEMA", "unsupported lifecycle_cli coordination schema", "coordination-schema", [String(current?.schema_version)], "migrate");
  return { artifacts: {}, reviews: {}, package_reviews: {}, validations: {}, resolutions: {}, milestones: {}, correction_history: {}, withdrawals: {}, ...structuredClone(current) };
}

function requireSchema2(state) {
  if (state.schema_version !== 2) throw operationError("RL_UNSUPPORTED_SCHEMA", "operation requires lifecycle_cli schema version 2", "coordination-schema", [String(state.schema_version)], "migrate");
}

function changeFiles(root) {
  const changesRoot = join(root, "docs", "changes");
  if (!existsSync(changesRoot) || !lstatSync(changesRoot).isDirectory()) return [];
  return readdirSync(changesRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !entry.isSymbolicLink())
    .map((entry) => ({ changeId: entry.name, path: join(changesRoot, entry.name, "change.yaml") }))
    .filter((entry) => existsSync(entry.path) && lstatSync(entry.path).isFile())
    .sort((a, b) => a.changeId.localeCompare(b.changeId));
}

function artifactOwners(root, artifactPath) {
  const owners = [];
  for (const entry of changeFiles(root)) {
    const source = readFileSync(entry.path, "utf8");
    if (!GOVERNED_LIFECYCLE_CONTRACT.test(source)) continue;
    let candidate;
    try { candidate = parseLifecycleYaml(source); }
    catch { throw operationError("RL_ARTIFACT_PATH_OWNED", "artifact ownership cannot be determined from an unreadable change record", "cross-change-artifact-ownership", [entry.changeId]); }
    if (candidate.lifecycle_contract !== "stage-owned-change-local-v1") continue;
    const registrations = candidate.lifecycle_cli?.artifacts ?? {};
    for (const [artifactId, registration] of Object.entries(registrations)) {
      const projected = candidate.artifact_states?.[artifactId];
      const registrationPath = registration?.artifact_path;
      if (typeof registrationPath !== "string" || registrationPath.startsWith("/") || registrationPath.includes("\\") || registrationPath.split("/").some((part) => !part || part === "." || part === "..")) throw operationError("RL_ARTIFACT_PATH_OWNED", "artifact ownership contains an unsafe path", "cross-change-artifact-ownership", [entry.changeId, artifactId, String(registrationPath)]);
      if (!projected || projected.path !== registrationPath || projected.kind !== registration.artifact_kind || projected.role !== registration.artifact_role) throw operationError("RL_ARTIFACT_PATH_OWNED", "artifact ownership projections are contradictory", "cross-change-artifact-ownership", [entry.changeId, artifactId]);
      if (registrationPath === artifactPath) owners.push({ changeId: entry.changeId, artifactId, kind: registration.artifact_kind, registration, change: candidate });
    }
  }
  return owners;
}

function routeIdentity(request) {
  return `route-${digest(Buffer.from(canonicalJson({ schema: "rigorloop-correction-route-v1", prior: request.expected_lifecycle_revision, source_stage: request.source_stage, destination_stage: request.destination_stage, destination_artifact_id: request.destination_artifact_id, reason: request.reason, finding_ids: [...request.finding_ids].sort(), return_stage: request.return_stage, milestone_id: request.milestone_id ?? null })) )}`;
}

function evidenceMetadata(file, required) {
  const values = Object.fromEntries(required.map((name) => [name, metadata(file.text, name)]));
  const missing = required.filter((name) => !values[name]);
  if (missing.length) throw operationError("RL_CORRECTION_ROUTE_INVALID", "operation evidence is incomplete", "operation-evidence", missing);
  return values;
}

function owningChangePointer(text) {
  const sections = [...text.matchAll(/^## Owning change record\s*\n+\s*`docs\/changes\/([^/`]+)\/change\.yaml`/gm)];
  return sections.length === 1 ? sections[0][1] : null;
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

function tableCells(line) {
  return line.split("|").slice(1, -1).map((cell) => cell.trim().replace(/^`|`$/g, ""));
}

function reviewLogFacts(log, reviewId) {
  if (!log.entry_text.trimStart().startsWith("|")) {
    return {
      format: "prose",
      reviewId: metadata(log.entry_text, "Review ID"),
      stage: metadata(log.entry_text, "Stage"),
      round: metadata(log.entry_text, "Round"),
      record: metadata(log.entry_text, "(?:Detailed record|Record)"),
      outcome: metadata(log.entry_text, "(?:Review status|Status)"),
      findings: metadata(log.entry_text, "Material findings"),
      openFindings: metadata(log.entry_text, "Open findings"),
      recording: metadata(log.entry_text, "(?:Recording status|Recording)"),
    };
  }
  const lines = log.text.split("\n");
  const rowIndex = lines.findIndex((line) => line === log.entry_text);
  let headerIndex = rowIndex - 1;
  while (headerIndex >= 0 && !/^\s*\|\s*Review ID\s*\|/i.test(lines[headerIndex])) headerIndex -= 1;
  if (headerIndex < 0) throw operationError("RL_INVALID_REQUEST", "review log table has no canonical header", "review-log-consistency", [reviewId]);
  const headers = tableCells(lines[headerIndex]).map((value) => value.toLowerCase());
  const values = tableCells(log.entry_text);
  const facts = Object.fromEntries(headers.map((header, index) => [header, values[index] ?? null]));
  return {
    format: "table",
    reviewId: facts["review id"],
    stage: facts.stage,
    round: facts.round,
    record: facts.record ?? facts["detailed record"],
    outcome: facts.status ?? facts["review status"],
    findings: facts["material findings"],
    openFindings: facts["open findings"],
    recording: facts.recording ?? facts["recording status"],
  };
}

function noFindings(value) {
  return value === null || value === undefined || /^(?:0|none)$/i.test(String(value).trim().replace(/`/g, ""));
}

function resetLatestReview() {
  return { artifact_id: "none", evidence: [], milestone_id: "none", occurrence: "none", round: "none", stage: "none", status: "not-started" };
}

function reviewedPlanMilestones(plan) {
  const headings = [...plan.text.matchAll(/^###\s+(M[1-9][0-9]*)\.\s+.+$/gm)];
  if (!headings.length) throw operationError("RL_INVALID_REQUEST", "approved plan has no milestone definitions", "plan-milestone-shape", [plan.path]);
  const milestones = {};
  for (let index = 0; index < headings.length; index += 1) {
    const milestoneId = headings[index][1];
    if (milestones[milestoneId]) throw operationError("RL_INVALID_REQUEST", "approved plan contains a duplicate milestone ID", "plan-milestone-shape", [plan.path, milestoneId]);
    const section = plan.text.slice(headings[index].index, headings[index + 1]?.index ?? plan.text.length);
    const kinds = [...section.matchAll(/^\s*-\s*Milestone kind:\s*`?(implementation|lifecycle-closeout)`?\s*$/gm)].map((match) => match[1]);
    if (kinds.length !== 1) throw operationError("RL_INVALID_REQUEST", "each approved plan milestone requires exactly one supported kind", "plan-milestone-shape", [plan.path, milestoneId]);
    milestones[milestoneId] = { kind: kinds[0], state: "planned" };
  }
  return milestones;
}

function milestoneProof(root, request) {
  const evidence = safeFile(root, request.evidence_path);
  if (metadata(evidence.text, "Milestone") !== request.milestone_id || !/^pass(?:ed)?$/i.test(metadata(evidence.text, "Validation result") ?? "")) {
    throw operationError("RL_INVALID_REQUEST", "milestone evidence must name the milestone and passing validation", "milestone-proof", [request.milestone_id, evidence.path]);
  }
  return evidence;
}

function fingerprintedCompletion(record) {
  return { ...record, completion_fingerprint: digest(Buffer.from(canonicalJson(record))) };
}

function projectedCompletion(evidence, review, request) {
  return fingerprintedCompletion({
    completion_schema_version: 1,
    evidence_path: evidence.path,
    evidence_sha256: evidence.sha256,
    milestone_id: request.milestone_id,
    review_mode: "projected",
    review_round: review.round,
    review_stage: review.stage,
    review_status: review.status,
    stage_authority: request.stage_authority,
  });
}

function recordedCompletion(evidence, review, request, reviewMode = "supplied") {
  return fingerprintedCompletion({
    completion_schema_version: 1,
    evidence_path: evidence.path,
    evidence_sha256: evidence.sha256,
    milestone_id: request.milestone_id,
    review_evidence_path: review.evidence.path,
    review_evidence_sha256: review.evidence.sha256,
    review_id: review.reviewId,
    review_log_entry_sha256: digest(Buffer.from(review.log.entry_text)),
    review_log_path: review.log.path,
    review_material_findings: [],
    review_open_findings: [],
    review_outcome: review.outcome,
    review_record_path: review.evidence.path,
    review_recording_status: review.recording,
    review_mode: reviewMode,
    review_round: review.round,
    review_stage: review.stage,
    stage_authority: request.stage_authority,
    ...(review.gate ? { review_gate_outcome: review.gate, packet_inventory: review.packetInventory, packet_sha256: review.packetSha256 } : {}),
  });
}

function sameCompletion(left, right) {
  return canonicalJson(left) === canonicalJson(right);
}

function requireMilestoneProjection(planned) {
  const expected = Object.entries(planned?.milestones ?? {})
    .filter(([, milestone]) => milestone.kind === "implementation" && milestone.state !== "closed")
    .map(([id]) => id);
  if (!Array.isArray(planned?.remaining_implementation_milestones) || canonicalJson(planned.remaining_implementation_milestones) !== canonicalJson(expected)) {
    throw operationError("RL_MILESTONE_ORDER", "remaining implementation milestone projection is inconsistent", "milestone-projection", expected);
  }
}

function milestoneReview(root, change, request) {
  const evidence = safeFile(root, request.review_evidence_path);
  const reviewId = metadata(evidence.text, "Review ID");
  const rawRound = metadata(evidence.text, "Round");
  const round = /^\d+$/.test(rawRound ?? "") ? `r${rawRound}` : rawRound;
  const stage = metadata(evidence.text, "Stage");
  const milestoneId = metadata(evidence.text, "Reviewed milestone");
  const outcome = reviewOutcome(evidence.text);
  const gate = metadata(evidence.text, "Review gate outcome");
  const recording = metadata(evidence.text, "Recording status");
  const findings = findingSet(metadata(evidence.text, "Material findings"));
  if (!reviewId || !/^r\d+$/.test(round ?? "") || stage !== "code-review" || milestoneId !== request.milestone_id || !["approved", "clean-with-notes"].includes(outcome) || recording !== "recorded") {
    throw operationError("RL_OPERATION_NOT_PERMITTED", "milestone completion requires an exact recorded clean code review", "milestone-review", [request.milestone_id, String(reviewId), String(milestoneId), String(outcome)], "complete-milestone");
  }
  if (findings.length) throw operationError("RL_UNRESOLVED_MATERIAL_FINDING", "milestone review contains material findings", "milestone-review-findings", findings);
  const log = requireLogEntry(root, change.change_id, reviewId);
  const logFacts = reviewLogFacts(log, reviewId);
  const expectedRecord = `docs/changes/${change.change_id}/${logFacts.record}`;
  if (logFacts.reviewId !== reviewId || logFacts.stage !== stage || logFacts.round !== round || logFacts.outcome !== outcome || (logFacts.record !== evidence.path && expectedRecord !== evidence.path) || logFacts.recording !== recording) {
    throw operationError("RL_OPERATION_NOT_PERMITTED", "milestone review receipt contradicts its canonical review-log occurrence", "review-log-consistency", [reviewId], "record-review");
  }
  const missingFindingState = logFacts.format === "prose"
    ? logFacts.findings === null || logFacts.openFindings === null
    : logFacts.findings === null;
  if (missingFindingState || !noFindings(logFacts.findings) || !noFindings(logFacts.openFindings)) {
    throw operationError("RL_UNRESOLVED_MATERIAL_FINDING", "milestone review log contains open findings", "milestone-review-findings", [reviewId]);
  }
  const inventory = metadata(evidence.text, "Initial packet inventory");
  const rawInventoryHash = metadata(evidence.text, "Initial packet hash");
  const declaredInventoryHash = rawInventoryHash === null ? undefined : identityValue(rawInventoryHash);
  const automated = gate !== null || inventory !== null || rawInventoryHash !== null;
  if (automated) {
    if (gate !== "advance" || !inventory || !/^[a-f0-9]{64}$/.test(declaredInventoryHash) || digest(Buffer.from(inventory)) !== declaredInventoryHash) {
      throw operationError("RL_STALE_EVIDENCE", "automated milestone review gate or packet identity is missing or invalid", "milestone-review-identity", [reviewId]);
    }
    const entries = inventory.split("; ");
    if (!entries.length) throw operationError("RL_STALE_EVIDENCE", "milestone review packet is empty", "milestone-review-identity", [reviewId]);
    for (const entry of entries) {
      const match = /^(.+)@working-tree#sha256:([a-f0-9]{64})$/.exec(entry);
      if (!match) throw operationError("RL_STALE_EVIDENCE", "milestone review packet entry is invalid", "milestone-review-identity", [reviewId]);
      const current = safeFile(root, match[1]);
      if (current.sha256 !== match[2]) throw operationError("RL_STALE_EVIDENCE", "milestone review packet is stale", "milestone-review-identity", [reviewId, match[1]]);
    }
  }
  return {
    evidence,
    gate,
    log,
    outcome,
    packetInventory: automated ? inventory : undefined,
    packetSha256: automated ? declaredInventoryHash : undefined,
    projection: { artifact_id: "plan", evidence: [evidence.path], milestone_id: request.milestone_id, occurrence: "milestone", round, stage: "code-review", status: "approved" },
    recording,
    reviewId,
    round,
    stage,
  };
}

function expectedReviewAuthority(kind) {
  return kind === "adr" ? "architecture-review" : `${kind}-review`;
}

function requireLogEntry(root, changeId, reviewId) {
  const log = safeFile(root, `docs/changes/${changeId}/review-log.md`);
  const marker = `Review ID: ${reviewId}`;
  const findingMarker = `Finding ID: ${reviewId}`;
  const lines = log.text.split("\n");
  const reviewLines = lines.filter((line) => line.trim() === marker).length;
  const findingLines = lines.filter((line) => line.trim() === findingMarker).length;
  const tableLines = lines.filter((line) => line.trimStart().startsWith("|") && tableCells(line)[0] === reviewId);
  if (reviewLines + findingLines + tableLines.length !== 1) {
    throw operationError("RL_INVALID_REQUEST", "review log must contain exactly one canonical review or finding occurrence", "review-log-consistency", [reviewId]);
  }
  if (reviewLines === 1) {
    const markerIndex = log.text.indexOf(marker);
    const nextEntry = log.text.indexOf("\n### Review entry", markerIndex + marker.length);
    return { ...log, entry_text: log.text.slice(markerIndex, nextEntry < 0 ? undefined : nextEntry) };
  }
  if (findingLines === 1) {
    const findingIndex = log.text.indexOf(findingMarker);
    const nextEntry = log.text.indexOf("\n### Review entry", findingIndex + findingMarker.length);
    return { ...log, entry_text: log.text.slice(findingIndex, nextEntry < 0 ? undefined : nextEntry) };
  }
  return { ...log, entry_text: tableLines[0] };
}

export function evaluateLifecycleOperation({ root, change, request }) {
  const next = structuredClone(change);
  const state = coordination(next);
  next.lifecycle_cli = state;
  const target = request.artifact_id && !["record-artifact-revision", "withdraw-artifact-registration"].includes(request.operation) ? artifact(next, request.artifact_id) : request.artifact_id ? next.artifact_states?.[request.artifact_id] ?? null : null;
  const targetIdentity = target ? artifactIdentity(root, target) : null;

  if (request.operation === "advance-stage") {
    const workflow = next.workflow_state ?? {};
    const transition = stageTransitionDecision(root, next, request.source_stage, request.destination_stage);
    if (!transition.allowed && transition.invariant === "workflow-stage-edge") throw operationError("RL_OPERATION_NOT_PERMITTED", "requested stage transition is not allowed", transition.invariant, [request.source_stage, request.destination_stage]);
    if (workflow.current_stage === request.destination_stage && workflow.next_stage === request.destination_stage) return { status: "already-recorded", candidate: change };
    if (workflow.current_stage !== request.source_stage) throw operationError("RL_OPERATION_NOT_PERMITTED", "source stage is not current", "workflow-stage-source", [String(workflow.current_stage), request.source_stage]);
    if (workflow.lifecycle_state !== "active" || workflow.blocker !== null || state.active_correction) throw operationError("RL_OPERATION_NOT_PERMITTED", "workflow is not eligible for normal advancement", "workflow-stage-readiness", [String(workflow.lifecycle_state), String(workflow.blocker)]);
    if (!transition.allowed) throw operationError("RL_OPERATION_NOT_PERMITTED", "source stage lacks exact completion authority", transition.invariant, [request.source_stage]);
    const automation = next.workflow?.automation;
    if (automation?.status === "active" && automation.current_stage !== request.source_stage) throw operationError("RL_OPERATION_NOT_PERMITTED", "active automation stage contradicts workflow state", "workflow-projection", [String(automation.current_stage), request.source_stage]);
    workflow.current_stage = request.destination_stage;
    workflow.next_stage = request.destination_stage;
    if (automation?.status === "active") automation.current_stage = request.destination_stage;
    return { status: "advanced", candidate: next, operationResult: { source_stage: request.source_stage, destination_stage: request.destination_stage } };
  }

  if (request.operation === "initialize-approved-plan") {
    const review = state.reviews[request.artifact_id];
    if (target?.kind !== "plan" || target.role !== "primary" || target.lifecycle_state !== "review-required") throw operationError("RL_OPERATION_NOT_PERMITTED", "initialization requires the review-required primary plan", "approved-plan-initialization", [request.artifact_id, String(target?.kind), String(target?.role), String(target?.lifecycle_state)]);
    if (next.workflow_state?.current_stage !== "plan-review") throw operationError("RL_OPERATION_NOT_PERMITTED", "approved plan initialization is not current", "approved-plan-initialization", [String(next.workflow_state?.current_stage)]);
    if (!review || !["approved", "clean-with-notes"].includes(review.outcome) || review.stage_authority !== "plan-review") throw operationError("RL_OPERATION_NOT_PERMITTED", "initialization requires one registered clean plan review", "approved-plan-review", [request.artifact_id], "record-review");
    const registration = state.artifacts[request.artifact_id];
    const plan = targetIdentity;
    const evidence = safeFile(root, review.evidence_path);
    const log = requireLogEntry(root, change.change_id, review.review_id);
    if (!registration || registration.artifact_kind !== "plan" || registration.artifact_role !== "primary" || registration.stage_authority !== "plan" || registration.artifact_path !== target.path || registration.artifact_sha256 !== plan.sha256) throw operationError("RL_STALE_EVIDENCE", "primary plan registration is missing or stale", "approved-plan-identity", [request.artifact_id, target.path], "record-artifact-revision");
    if (review.artifact_path !== target.path || review.artifact_sha256 !== plan.sha256 || review.evidence_sha256 !== evidence.sha256 || review.review_log_sha256 !== log.sha256) throw operationError("RL_STALE_EVIDENCE", "clean plan review is stale", "approved-plan-review", [review.review_id, target.path], "record-review");
    const openFindings = review.findings.filter((findingId) => state.resolutions[findingId]?.artifact_id !== request.artifact_id);
    if (openFindings.length) throw operationError("RL_UNRESOLVED_MATERIAL_FINDING", "plan review findings remain open", "approved-plan-review", openFindings, "record-finding-resolution");
    const milestones = reviewedPlanMilestones(plan);
    const ordered = Object.keys(milestones);
    const expected = {
      plan_artifact_id: request.artifact_id,
      current_milestone: ordered[0],
      milestones,
      remaining_implementation_milestones: ordered.filter((milestoneId) => milestones[milestoneId].kind === "implementation"),
      latest_review: resetLatestReview(),
      final_closeout: { readiness: "not-ready", reasons: [ordered.some((milestoneId) => milestones[milestoneId].kind === "implementation") ? "implementation-milestones-open" : "lifecycle-gates-open"], evidence: [] },
      initialization_basis: { review_id: review.review_id, review_round: review.round, review_record: review.evidence_path, reviewed_artifact_path: target.path, reviewed_revision: plan.sha256 },
    };
    const existing = next.workflow_state?.planned_work;
    if (existing) {
      if (canonicalJson(existing) === canonicalJson(expected)) return { status: "already-recorded", candidate: change };
      throw operationError("RL_OPERATION_NOT_PERMITTED", "existing planned work cannot be replaced", "approved-plan-initialization", [request.artifact_id]);
    }
    next.workflow_state.planned_work = expected;
    return { status: "initialized", candidate: next, operationResult: { artifact_id: request.artifact_id, current_milestone: expected.current_milestone, next_operation: "settle-artifact" } };
  }

  if (request.operation === "route-correction") {
    requireSchema2(state);
    const workflow = next.workflow_state ?? {};
    if (state.active_correction) {
      const active = state.active_correction;
      const sameRoute = active.source_snapshot?.current_stage === request.source_stage
        && active.destination_stage === request.destination_stage
        && active.destination_artifact_id === request.destination_artifact_id
        && active.reason === request.reason
        && active.return_stage === request.return_stage
        && active.evidence_path === request.evidence_path
        && (active.source_snapshot?.milestone_id ?? null) === (request.milestone_id ?? null)
        && JSON.stringify(active.source_snapshot?.finding_ids ?? []) === JSON.stringify([...request.finding_ids].sort());
      if (sameRoute) return { status: "already-recorded", candidate: change };
      throw operationError("RL_CORRECTION_ROUTE_INVALID", "a conflicting correction route is already active", "active-correction-route", [state.active_correction.route_id]);
    }
    if (workflow.current_stage !== request.source_stage || request.return_stage !== request.source_stage) throw operationError("RL_CORRECTION_ROUTE_INVALID", "route source and return stage must match current workflow stage", "correction-source", [String(workflow.current_stage), request.source_stage, request.return_stage]);
    const sourceIndex = CORRECTION_STAGE_ORDER.indexOf(request.source_stage);
    const destinationIndex = CORRECTION_STAGE_ORDER.indexOf(request.destination_stage);
    if (sourceIndex < 0 || destinationIndex < 0 || destinationIndex >= sourceIndex) throw operationError("RL_CORRECTION_ROUTE_INVALID", "correction destination must precede the source stage", "correction-order", [request.source_stage, request.destination_stage]);
    const destination = artifact(next, request.destination_artifact_id);
    const packageKind = ["design-review", "delivery-review"].includes(request.source_stage) ? request.source_stage.replace(/-review$/, "") : null;
    const packageReview = packageKind ? state.package_reviews?.[packageKind] : null;
    if (packageKind && (packageReview?.outcome !== "changes-requested" || !packageReview.correction_targets?.includes(request.destination_artifact_id))) throw operationError("RL_CORRECTION_ROUTE_INVALID", "package correction must target an artifact named by the current changes-requested review", "correction-destination", [request.source_stage, request.destination_artifact_id]);
    if (packageKind && Object.values(state.correction_history ?? {}).some((receipt) => receipt?.source_review_id === packageReview.review_id && receipt?.destination_artifact_id === request.destination_artifact_id)) throw operationError("RL_CORRECTION_ROUTE_INVALID", "package correction target already returned for the current review", "correction-destination", [packageReview.review_id, request.destination_artifact_id]);
    if (destination.kind !== request.destination_stage && !(request.destination_stage === "architecture" && destination.kind === "adr")) throw operationError("RL_CORRECTION_ROUTE_INVALID", "destination artifact kind does not match destination stage", "correction-destination", [request.destination_stage, request.destination_artifact_id, destination.kind]);
    if (!["accepted", "approved", "active", ...(packageKind ? ["review-required"] : [])].includes(destination.lifecycle_state)) throw operationError("RL_CORRECTION_ROUTE_INVALID", "destination artifact is not currently settled or package-reviewable", "correction-destination", [request.destination_artifact_id, String(destination.lifecycle_state)]);
    const registration = state.artifacts[request.destination_artifact_id];
    const destinationIdentity = artifactIdentity(root, destination);
    if (!registration || registration.artifact_path !== destination.path) throw operationError("RL_CORRECTION_ROUTE_INVALID", "destination artifact registration is missing or mismatched", "correction-destination", [request.destination_artifact_id]);
    if (registration.artifact_sha256 !== destinationIdentity.sha256 && request.finding_ids.length === 0) throw operationError("RL_CORRECTION_ROUTE_INVALID", "a stale destination correction requires an open finding", "correction-findings", [request.destination_artifact_id]);
    const evidence = safeFile(root, request.evidence_path);
    const facts = evidenceMetadata(evidence, ["Change ID", "Source stage", "Destination artifact", "Reason", "Finding IDs", "Return stage", "Lifecycle revision"]);
    const evidenceFindings = findingSet(facts["Finding IDs"]);
    if (facts["Change ID"] !== change.change_id || facts["Source stage"] !== request.source_stage || facts["Destination artifact"] !== request.destination_artifact_id || facts.Reason !== request.reason || facts["Return stage"] !== request.return_stage || facts["Lifecycle revision"] !== request.expected_lifecycle_revision || JSON.stringify(evidenceFindings) !== JSON.stringify([...request.finding_ids].sort())) throw operationError("RL_CORRECTION_ROUTE_INVALID", "route evidence does not bind the exact request", "correction-evidence", [request.evidence_path]);
    const reviewLogPath = `docs/changes/${change.change_id}/review-log.md`;
    const reviewLog = safeFile(root, reviewLogPath).text;
    const openFindingIds = new Set([...reviewLog.matchAll(/^Open findings:\s*(.+)$/gm)].flatMap((match) => match[1].trim().toLowerCase() === "none" ? [] : match[1].split(",").map((value) => value.trim().replace(/`/g, "")).filter(Boolean)));
    for (const findingId of request.finding_ids) if (!openFindingIds.has(findingId)) throw operationError("RL_CORRECTION_ROUTE_INVALID", "route cites a finding that is not currently open", "correction-findings", [findingId]);
    const planned = workflow.planned_work;
    if ((planned?.current_milestone ?? null) !== (request.milestone_id ?? null) && !(planned?.current_milestone === "none" && request.milestone_id === undefined)) throw operationError("RL_CORRECTION_ROUTE_INVALID", "route milestone does not match current workflow milestone", "correction-source", [String(planned?.current_milestone), String(request.milestone_id)]);
    const routeId = routeIdentity(request);
    state.active_correction = {
      route_id: routeId,
      status: "active",
      prior_lifecycle_revision: request.expected_lifecycle_revision,
      source_snapshot: {
        current_stage: workflow.current_stage,
        next_stage: workflow.next_stage ?? null,
        lifecycle_state: workflow.lifecycle_state ?? null,
        blocker: workflow.blocker ?? null,
        milestone_id: planned?.current_milestone ?? null,
        milestone_state: request.milestone_id ? planned?.milestones?.[request.milestone_id]?.state ?? null : null,
        finding_ids: [...request.finding_ids].sort(),
      },
      destination_stage: request.destination_stage,
      destination_artifact_id: request.destination_artifact_id,
      prior_artifact_sha256: registration.artifact_sha256,
      reason: request.reason,
      evidence_path: evidence.path,
      evidence_sha256: evidence.sha256,
      return_stage: request.return_stage,
      ...(packageReview ? { source_review_id: packageReview.review_id } : {}),
    };
    workflow.current_stage = request.destination_stage;
    workflow.next_stage = expectedReviewAuthority(destination.kind);
    workflow.blocker = null;
    return { status: "routed", candidate: next, operationResult: { route_id: routeId, source_stage: request.source_stage, destination_stage: request.destination_stage, destination_artifact_id: request.destination_artifact_id, reason: request.reason, finding_ids: [...request.finding_ids].sort(), return_stage: request.return_stage, evidence_path: evidence.path, source_snapshot: { current_stage: state.active_correction.source_snapshot.current_stage, next_stage: state.active_correction.source_snapshot.next_stage, lifecycle_state: state.active_correction.source_snapshot.lifecycle_state, blocker: state.active_correction.source_snapshot.blocker, milestone_id: state.active_correction.source_snapshot.milestone_id, milestone_state: state.active_correction.source_snapshot.milestone_state } } };
  }

  if (request.operation === "return-correction") {
    requireSchema2(state);
    const route = state.active_correction;
    const returned = state.correction_history[request.route_id];
    if (!route && returned?.status === "returned" && returned.return_evidence_path === request.evidence_path) return { status: "already-recorded", candidate: change };
    if (!route || route.route_id !== request.route_id) throw operationError("RL_CORRECTION_ROUTE_INVALID", "return does not identify the active correction route", "correction-return", [request.route_id]);
    const destination = artifact(next, route.destination_artifact_id);
    const currentIdentity = artifactIdentity(root, destination);
    if (currentIdentity.sha256 === route.prior_artifact_sha256) throw operationError("RL_CORRECTION_ROUTE_INVALID", "destination artifact has not changed", "correction-return", [route.destination_artifact_id]);
    const packageCorrection = ["design-review", "delivery-review"].includes(route.return_stage);
    const review = state.reviews[route.destination_artifact_id];
    const registration = state.artifacts[route.destination_artifact_id];
    if (packageCorrection) {
      if (!registration || registration.artifact_sha256 !== currentIdentity.sha256 || registration.stage_authority !== route.destination_stage || destination.lifecycle_state !== "review-required") throw operationError("RL_CORRECTION_ROUTE_INVALID", "package correction destination lacks an exact current authoring revision", "correction-return", [route.destination_artifact_id]);
    } else if (!review || !["approved", "clean-with-notes"].includes(review.outcome) || review.artifact_sha256 !== currentIdentity.sha256 || review.stage_authority !== expectedReviewAuthority(destination.kind)) throw operationError("RL_CORRECTION_ROUTE_INVALID", "destination lacks an exact current approving review", "correction-return", [route.destination_artifact_id]);
    const evidence = safeFile(root, request.evidence_path);
    const baseFields = ["Change ID", "Route ID", "Lifecycle revision", "Destination artifact", "Artifact path", "Artifact identity"];
    const facts = evidenceMetadata(evidence, packageCorrection ? [...baseFields, "Authoring evidence path", "Authoring evidence identity"] : [...baseFields, "Review ID", "Review round", "Review authority", "Review outcome", "Review evidence path", "Review evidence identity"]);
    const baseMatches = facts["Change ID"] === change.change_id && facts["Route ID"] === route.route_id && facts["Lifecycle revision"] === request.expected_lifecycle_revision && facts["Destination artifact"] === route.destination_artifact_id && facts["Artifact path"] === destination.path && identityValue(facts["Artifact identity"]) === currentIdentity.sha256;
    const authorityMatches = packageCorrection
      ? facts["Authoring evidence path"] === registration.authoring_evidence_path && identityValue(facts["Authoring evidence identity"]) === registration.authoring_evidence_sha256
      : facts["Review ID"] === review.review_id && facts["Review round"] === review.round && facts["Review authority"] === review.stage_authority && facts["Review outcome"] === review.outcome && facts["Review evidence path"] === review.evidence_path && identityValue(facts["Review evidence identity"]) === review.evidence_sha256;
    if (!baseMatches || !authorityMatches) throw operationError("RL_CORRECTION_ROUTE_INVALID", "return evidence does not bind the exact route and owning-stage result", "correction-return-evidence", [request.evidence_path]);
    const snapshot = route.source_snapshot;
    next.workflow_state.current_stage = snapshot.current_stage;
    next.workflow_state.next_stage = snapshot.next_stage;
    next.workflow_state.lifecycle_state = snapshot.lifecycle_state;
    next.workflow_state.blocker = snapshot.blocker;
    if (next.workflow_state.planned_work) {
      next.workflow_state.planned_work.current_milestone = snapshot.milestone_id;
      if (snapshot.milestone_id && next.workflow_state.planned_work.milestones?.[snapshot.milestone_id]) next.workflow_state.planned_work.milestones[snapshot.milestone_id].state = snapshot.milestone_state;
    }
    state.correction_history[route.route_id] = { ...route, status: "returned", return_evidence_path: evidence.path, return_evidence_sha256: evidence.sha256 };
    delete state.active_correction;
    return { status: "returned", candidate: next, operationResult: { route_id: route.route_id, restored_stage: snapshot.current_stage, restored_next_stage: snapshot.next_stage, restored_milestone_id: snapshot.milestone_id, return_evidence_path: evidence.path } };
  }

  if (request.operation === "withdraw-artifact-registration") {
    requireSchema2(state);
    const existingReceipt = Object.values(state.withdrawals).find((receipt) => receipt?.status === "withdrawn" && receipt.artifact_id === request.artifact_id && receipt.artifact_path === request.artifact_path && receipt.canonical_owner_change_id === request.canonical_owner_change_id && receipt.reason === request.reason && receipt.evidence_path === request.evidence_path);
    if (existingReceipt && !target) return { status: "already-recorded", candidate: change };
    if (!target || !["architecture", "adr"].includes(target.kind) || target.path !== request.artifact_path) throw operationError("RL_WITHDRAWAL_UNSAFE", "withdrawal supports only the exact architecture or ADR registration", "withdrawal-target", [request.artifact_id]);
    const targetStage = target.kind === "adr" ? "architecture" : target.kind;
    if (state.active_correction?.destination_artifact_id === request.artifact_id || [targetStage, `${targetStage}-review`].includes(next.workflow_state?.current_stage)) throw operationError("RL_WITHDRAWAL_UNSAFE", "active workflow state depends on the selected artifact", "withdrawal-active-dependency", [request.artifact_id]);
    const semantic = safeFile(root, target.path);
    const pointer = owningChangePointer(semantic.text);
    const owners = artifactOwners(root, target.path);
    const canonical = owners.filter((owner) => owner.changeId === request.canonical_owner_change_id);
    const selectedOwners = owners.filter((owner) => owner.changeId === change.change_id && owner.artifactId === request.artifact_id);
    if (pointer !== request.canonical_owner_change_id || request.canonical_owner_change_id === change.change_id || canonical.length !== 1 || selectedOwners.length !== 1) throw operationError("RL_WITHDRAWAL_UNSAFE", "canonical ownership cannot be proved exactly", "withdrawal-ownership", [String(pointer), request.canonical_owner_change_id, ...owners.map((owner) => owner.changeId)]);
    const evidence = safeFile(root, request.evidence_path);
    const facts = evidenceMetadata(evidence, ["Change ID", "Artifact ID", "Artifact path", "Canonical owner", "Reason", "Lifecycle revision"]);
    if (facts["Change ID"] !== change.change_id || facts["Artifact ID"] !== request.artifact_id || facts["Artifact path"] !== request.artifact_path || facts["Canonical owner"] !== request.canonical_owner_change_id || facts.Reason !== request.reason || facts["Lifecycle revision"] !== request.expected_lifecycle_revision) throw operationError("RL_WITHDRAWAL_UNSAFE", "withdrawal evidence does not bind the exact request", "withdrawal-evidence", [request.evidence_path]);
    const withdrawalId = `withdrawal-${digest(Buffer.from(canonicalJson({ schema: "rigorloop-withdrawal-v1", artifact_id: request.artifact_id, artifact_path: request.artifact_path, canonical_owner: request.canonical_owner_change_id, prior: request.expected_lifecycle_revision })))}`;
    if (state.withdrawals[withdrawalId]) return { status: "already-recorded", candidate: change };
    const registration = state.artifacts[request.artifact_id];
    delete next.artifact_states[request.artifact_id];
    delete next.artifacts?.[request.artifact_id];
    delete state.artifacts[request.artifact_id];
    delete state.reviews[request.artifact_id];
    delete state.validations[request.artifact_id];
    for (const [findingId, resolution] of Object.entries(state.resolutions)) if (resolution.artifact_id === request.artifact_id) delete state.resolutions[findingId];
    state.withdrawals[withdrawalId] = { withdrawal_id: withdrawalId, status: "withdrawn", artifact_id: request.artifact_id, artifact_kind: target.kind, artifact_path: target.path, artifact_sha256: registration?.artifact_sha256 ?? semantic.sha256, canonical_owner_change_id: request.canonical_owner_change_id, reason: request.reason, evidence_path: evidence.path, evidence_sha256: evidence.sha256, prior_lifecycle_revision: request.expected_lifecycle_revision };
    return { status: "withdrawn", candidate: next, operationResult: { withdrawal_id: withdrawalId, artifact_id: request.artifact_id, artifact_path: request.artifact_path, canonical_owner_change_id: request.canonical_owner_change_id, receipt_status: "withdrawn", evidence_path: evidence.path } };
  }

  if (request.operation === "record-artifact-revision") {
    if (state.active_correction && state.active_correction.destination_artifact_id !== request.artifact_id) throw operationError("RL_CORRECTION_ROUTE_INVALID", "only the routed destination artifact may be revised", "correction-destination", [request.artifact_id, state.active_correction.destination_artifact_id]);
    if (state.active_correction) {
      const atDestination = next.workflow_state?.current_stage === state.active_correction.destination_stage;
      const handedBackByReview = next.workflow_state?.current_stage === expectedReviewAuthority(request.artifact_kind)
        && target?.lifecycle_state === "revision-required"
        && target?.review?.outcome === "changes-requested";
      if (!atDestination && !handedBackByReview) throw operationError("RL_CORRECTION_ROUTE_INVALID", "routed destination revision is not current", "correction-destination", [String(next.workflow_state?.current_stage), state.active_correction.destination_stage]);
    }
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
      const crossChangeOwners = artifactOwners(root, request.artifact_path).filter((owner) => owner.changeId !== change.change_id);
      if (crossChangeOwners.length) throw operationError("RL_ARTIFACT_PATH_OWNED", "artifact path is already owned by another governed change", "cross-change-artifact-ownership", [request.artifact_path, ...crossChangeOwners.map((owner) => owner.changeId)]);
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
    for (const reviewPackage of Object.values(next.review_packages ?? {})) {
      if (reviewPackage?.status !== "review-required" && Object.hasOwn(reviewPackage?.members ?? {}, request.artifact_id)) {
        reviewPackage.status = "review-required";
        reviewPackage.authority = "withheld";
      }
    }
    if (state.active_correction?.destination_artifact_id === request.artifact_id) {
      const packageCorrection = ["design-review", "delivery-review"].includes(state.active_correction.return_stage);
      next.workflow_state.current_stage = packageCorrection ? state.active_correction.destination_stage : expectedReviewAuthority(request.artifact_kind);
      next.workflow_state.next_stage = packageCorrection ? state.active_correction.return_stage : expectedReviewAuthority(request.artifact_kind);
    }
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
    const desired = review.outcome === "approved" || review.outcome === "clean-with-notes"
      ? ({ proposal: "accepted", spec: "approved", architecture: "approved", plan: "active", "test-spec": "active", adr: "accepted" }[target.kind] ?? "approved")
      : review.outcome === "changes-requested" ? "revision-required" : "blocked";
    const openFindings = review.findings.filter((findingId) => state.resolutions[findingId]?.artifact_id !== request.artifact_id).sort();
    if ((review.outcome === "approved" || review.outcome === "clean-with-notes") && openFindings.length) {
      throw operationError("RL_UNRESOLVED_MATERIAL_FINDING", "material review findings remain open", "finding-closeout", openFindings, "record-finding-resolution");
    }
    const settledReviewOutcome = review.outcome === "clean-with-notes" ? "approved" : review.outcome;
    const alreadySettled = target.lifecycle_state === desired && target.review?.id === review.review_id && target.review?.outcome === settledReviewOutcome;
    if (next.workflow_state?.current_stage !== expectedReviewAuthority(target.kind) && !alreadySettled) throw operationError("RL_OPERATION_NOT_PERMITTED", "artifact settlement is not current for its reviewing stage", "review-stage", [String(next.workflow_state?.current_stage), expectedReviewAuthority(target.kind)]);
    target.lifecycle_state = desired;
    delete target.authoring_evidence;
    target.review = { id: review.review_id, artifact_id: request.artifact_id, outcome: settledReviewOutcome, record: review.evidence_path, round: review.round, ...(target.kind === "adr" && desired === "accepted" ? { adr_settlement: "accepted" } : {}) };
    if (target.kind === "proposal" && next.review_packages?.design?.status === "approved" && next.review_packages.design.upstream_review_id !== review.review_id) {
      next.review_packages.design.status = "review-required";
      next.review_packages.design.authority = "withheld";
    }
    if (target.kind === "plan" && ["approved", "clean-with-notes"].includes(review.outcome) && next.workflow_state?.planned_work?.initialization_basis) {
      next.workflow_state.planned_work.initialization_basis = { review_id: review.review_id, review_record: review.evidence_path, review_round: review.round, reviewed_artifact_path: target.path, reviewed_revision: targetIdentity.sha256 };
    }
    if (!next.review || typeof next.review !== "object" || Array.isArray(next.review)) next.review = {};
    next.review.latest_review = review.evidence_path;
    next.review.review_log = log.path;
    next.review.reviewed_artifact = target.path;
    next.review.status = ["approved", "clean-with-notes"].includes(review.outcome) ? "clean" : review.outcome;
    next.review.unresolved_items = openFindings.length;
    if (JSON.stringify(next) === JSON.stringify(change)) return { status: "already-recorded", candidate: change };
    return { status: "settled", candidate: next };
  }

  if (request.operation === "record-package-review") {
    requireSchema2(state);
    const expectedAuthority = `${request.package_kind}-review`;
    if (request.stage_authority !== expectedAuthority) throw operationError("RL_AUTHORITY_BOUNDARY", "Package review authority does not own the package kind.", "review-package-authority", [request.stage_authority, expectedAuthority]);
    const context = reviewPackageContext(root, next, request.package_kind);
    if (context.errors.length) throw Object.assign(new Error(context.errors[0].summary), { code: context.errors[0].code, diagnostic: context.errors[0] });
    if (request.upstream_review_id !== context.upstream_review_id || canonicalJson(request.members) !== canonicalJson(context.members)) throw operationError("RL_STALE_EVIDENCE", "Package review request does not bind the current member map and upstream review ID.", "review-package-request-identity", [request.package_kind, request.upstream_review_id, String(context.upstream_review_id)]);
    if (next.workflow_state?.current_stage !== expectedAuthority) throw operationError("RL_OPERATION_NOT_PERMITTED", "Package review recording is not current for its reviewing stage.", "review-package-stage", [String(next.workflow_state?.current_stage), expectedAuthority]);
    const registration = readPackageReview(root, next, request, context);
    if (alreadyRecorded(state.package_reviews[request.package_kind], registration)) return { status: "already-recorded", candidate: change };
    state.package_reviews[request.package_kind] = registration;
    return { status: "recorded", candidate: next, operationResult: { package_kind: request.package_kind, members: context.members, upstream_review_id: context.upstream_review_id, review_id: registration.review_id, outcome: registration.outcome } };
  }

  if (request.operation === "settle-review-package") {
    requireSchema2(state);
    const expectedAuthority = `${request.package_kind}-review`;
    if (request.stage_authority !== expectedAuthority) throw operationError("RL_AUTHORITY_BOUNDARY", "Package settlement authority does not own the package kind.", "review-package-authority", [request.stage_authority, expectedAuthority]);
    const registered = state.package_reviews[request.package_kind];
    if (!registered) throw operationError("RL_OPERATION_NOT_PERMITTED", "Review package has no registered review.", "review-package-registration", [request.package_kind], "record-package-review");
    const desiredProjection = packageProjection(registered);
    const existingProjection = next.review_packages?.[request.package_kind];
    const context = reviewPackageContext(root, next, request.package_kind);
    if (context.errors.length) throw Object.assign(new Error(context.errors[0].summary), { code: context.errors[0].code, diagnostic: context.errors[0] });
    if (request.review_id !== registered.review_id || registered.upstream_review_id !== context.upstream_review_id || canonicalJson(registered.members) !== canonicalJson(context.members)) throw operationError("RL_STALE_EVIDENCE", "Registered package review or settlement request does not bind current package facts.", "review-package-freshness", [request.package_kind, request.review_id, registered.review_id], "record-package-review");
    if (registered.stage_authority !== request.stage_authority || next.workflow_state?.current_stage !== expectedAuthority) throw operationError("RL_OPERATION_NOT_PERMITTED", "Package settlement is not current for its registered review authority.", "review-package-stage", [String(next.workflow_state?.current_stage), request.stage_authority]);
    const currentReview = readPackageReview(root, next, { ...request, evidence_path: registered.evidence_path }, context);
    if (canonicalJson(currentReview) !== canonicalJson(registered)) throw operationError("RL_STALE_EVIDENCE", "Registered package review evidence changed before settlement.", "review-package-review-freshness", [registered.review_id], "record-package-review");
    if (request.review_id === registered.review_id && existingProjection && canonicalJson(existingProjection) === canonicalJson(desiredProjection)) return { status: "already-recorded", candidate: change };
    next.review_packages ??= {};
    next.review_packages[request.package_kind] = desiredProjection;
    if (request.package_kind === "design" && next.review_packages.delivery && next.review_packages.delivery.upstream_review_id !== registered.review_id) {
      next.review_packages.delivery.status = "review-required";
      next.review_packages.delivery.authority = "withheld";
    }
    if (!next.review || typeof next.review !== "object" || Array.isArray(next.review)) next.review = {};
    next.review.latest_review = registered.evidence_path;
    next.review.review_log = registered.review_log_path;
    next.review.reviewed_artifact = `review-package:${request.package_kind}`;
    next.review.status = registered.outcome === "approved" ? "clean" : registered.outcome;
    next.review.unresolved_items = registered.findings.length;
    return { status: "settled", candidate: next, operationResult: { package_kind: request.package_kind, members: context.members, upstream_review_id: context.upstream_review_id, review_id: registered.review_id, outcome: registered.outcome, authority: desiredProjection.authority } };
  }

  if (request.operation === "start-milestone") {
    const planned = next.workflow_state?.planned_work;
    const milestones = planned?.milestones;
    const targetMilestone = milestones?.[request.milestone_id];
    if (!planned || !targetMilestone || planned.current_milestone !== request.milestone_id || targetMilestone.kind !== "implementation") throw operationError("RL_MILESTONE_ORDER", "requested milestone is not the unique current implementation milestone", "milestone-selection", [request.milestone_id]);
    requireMilestoneProjection(planned);
    const automation = next.workflow?.automation;
    const activeAutomation = automation?.status === "active";
    if (activeAutomation && automation.current_stage !== next.workflow_state.current_stage) {
      throw operationError("RL_OPERATION_NOT_PERMITTED", "active workflow automation contradicts the governed workflow stage", "workflow-projection", [String(next.workflow_state.current_stage), String(automation.current_stage)]);
    }
    if (targetMilestone.state === "implementing") {
      const routingMatches = next.workflow_state.current_stage === "implement" && next.workflow_state.next_stage === "code-review" && (!activeAutomation || automation.current_stage === "implement");
      if (routingMatches) return { status: "already-recorded", candidate: change };
      throw operationError("RL_OPERATION_NOT_PERMITTED", "implementing milestone has contradictory workflow routing", "workflow-projection", [request.milestone_id]);
    }
    if (targetMilestone.state !== "planned") throw operationError("RL_OPERATION_NOT_PERMITTED", "milestone cannot start from its current state", "milestone-state", [request.milestone_id, String(targetMilestone.state)]);
    const ordered = Object.keys(milestones);
    const predecessors = ordered.slice(0, ordered.indexOf(request.milestone_id));
    const incomplete = predecessors.filter((id) => milestones[id].kind === "implementation" && milestones[id].state !== "closed");
    if (incomplete.length) throw operationError("RL_MILESTONE_ORDER", "required predecessor milestones are incomplete", "milestone-predecessors", incomplete);
    targetMilestone.state = "implementing";
    next.workflow_state.current_stage = "implement";
    next.workflow_state.next_stage = "code-review";
    if (activeAutomation) automation.current_stage = "implement";
    return { status: "started", candidate: next };
  }

  if (request.operation === "complete-milestone") {
    const planned = next.workflow_state?.planned_work;
    const targetMilestone = planned?.milestones?.[request.milestone_id];
    if (!planned || !targetMilestone || targetMilestone.kind !== "implementation") throw operationError("RL_MILESTONE_ORDER", "requested milestone is not an implementation milestone", "milestone-selection", [request.milestone_id]);
    requireMilestoneProjection(planned);
    if (targetMilestone.state === "closed") {
      const existing = state.milestones[request.milestone_id];
      if (!existing) throw operationError("RL_STALE_EVIDENCE", "closed milestone has no completion registration", "milestone-completion-evidence", [request.milestone_id]);
      let replay;
      try {
        const evidence = milestoneProof(root, request);
        if (existing.review_evidence_path) {
          const reviewMode = existing.review_mode ?? "supplied";
          if (reviewMode === "supplied" && request.review_evidence_path !== existing.review_evidence_path) throw new Error("review evidence omitted or changed");
          if (reviewMode === "projected" && request.review_evidence_path !== undefined) throw new Error("projected review replay changed its request facts");
          const replayRequest = { ...request, review_evidence_path: existing.review_evidence_path };
          replay = recordedCompletion(evidence, milestoneReview(root, next, replayRequest), request, reviewMode);
        } else {
          if (request.review_evidence_path) throw new Error("review evidence conflicts with projected completion");
          replay = projectedCompletion(evidence, {
            round: existing.review_round,
            stage: existing.review_stage ?? "code-review",
            status: existing.review_status ?? "approved",
          }, request);
        }
      } catch {
        throw operationError("RL_STALE_EVIDENCE", "milestone completion evidence is missing, stale, or contradictory", "milestone-completion-evidence", [request.milestone_id]);
      }
      if (existing.completion_fingerprint) {
        if (!sameCompletion(existing, replay)) throw operationError("RL_STALE_EVIDENCE", "milestone completion evidence differs from its recorded fingerprint", "milestone-completion-evidence", [request.milestone_id]);
        return { status: "already-recorded", candidate: change };
      }
      const legacyMatches = existing.evidence_path === replay.evidence_path
        && existing.evidence_sha256 === replay.evidence_sha256
        && existing.stage_authority === replay.stage_authority
        && existing.review_round === replay.review_round
        && (!existing.review_evidence_path || (existing.review_evidence_path === replay.review_evidence_path && existing.review_evidence_sha256 === replay.review_evidence_sha256));
      if (!legacyMatches) throw operationError("RL_STALE_EVIDENCE", "legacy milestone completion evidence is contradictory", "milestone-completion-evidence", [request.milestone_id]);
      state.milestones[request.milestone_id] = replay;
      return { status: "completed", candidate: next, operationResult: { legacy_completion_upgraded: true, milestone_id: request.milestone_id } };
    }
    if (planned.current_milestone !== request.milestone_id) throw operationError("RL_MILESTONE_ORDER", "requested milestone is not the unique current implementation milestone", "milestone-selection", [request.milestone_id]);
    if (targetMilestone.state === "implementing") {
      if (request.review_evidence_path !== undefined) throw operationError("RL_OPERATION_NOT_PERMITTED", "implementation must be handed to code review before review evidence can settle the milestone", "milestone-state", [request.milestone_id, targetMilestone.state]);
      milestoneProof(root, request);
      const workflow = next.workflow_state;
      if (workflow.current_stage !== "implement" || workflow.next_stage !== "code-review") throw operationError("RL_OPERATION_NOT_PERMITTED", "implementing milestone has contradictory workflow routing", "workflow-projection", [request.milestone_id, String(workflow.current_stage), String(workflow.next_stage)]);
      const automation = next.workflow?.automation;
      if (automation?.status === "active" && automation.current_stage !== "implement") throw operationError("RL_OPERATION_NOT_PERMITTED", "active workflow automation contradicts the governed workflow stage", "workflow-projection", [String(workflow.current_stage), String(automation.current_stage)]);
      targetMilestone.state = "review-requested";
      workflow.current_stage = "code-review";
      workflow.next_stage = "code-review";
      if (automation?.status === "active") automation.current_stage = "code-review";
      return { status: "review-requested", candidate: next, operationResult: { milestone_id: request.milestone_id, next_stage: "code-review" } };
    }
    if (targetMilestone.state !== "review-requested") throw operationError("RL_OPERATION_NOT_PERMITTED", "milestone can complete only after review is requested", "milestone-state", [request.milestone_id, String(targetMilestone.state)]);
    const suppliedReview = request.review_evidence_path ? milestoneReview(root, next, request) : null;
    if (suppliedReview) planned.latest_review = suppliedReview.projection;
    const review = planned.latest_review;
    if (!review || review.milestone_id !== request.milestone_id || review.status !== "approved") throw operationError("RL_OPERATION_NOT_PERMITTED", "milestone completion requires its approved code review", "milestone-review", [request.milestone_id], "record-review");
    const evidence = milestoneProof(root, request);
    let reviewDetails = suppliedReview;
    if (!reviewDetails) {
      if (!Array.isArray(review.evidence) || review.evidence.length !== 1 || typeof review.evidence[0] !== "string") {
        throw operationError("RL_STALE_EVIDENCE", "projected milestone review must identify one exact review record", "milestone-review-identity", [request.milestone_id]);
      }
      reviewDetails = milestoneReview(root, next, { ...request, review_evidence_path: review.evidence[0] });
      if (canonicalJson(reviewDetails.projection) !== canonicalJson(review)) {
        throw operationError("RL_STALE_EVIDENCE", "projected milestone review contradicts its current evidence", "milestone-review-identity", [request.milestone_id]);
      }
    }
    state.milestones[request.milestone_id] = recordedCompletion(evidence, reviewDetails, request, suppliedReview ? "supplied" : "projected");
    targetMilestone.state = "closed";
    planned.remaining_implementation_milestones = (planned.remaining_implementation_milestones ?? []).filter((id) => id !== request.milestone_id);
    planned.current_milestone = Object.entries(planned.milestones).find(([, milestone]) => milestone.state !== "closed")?.[0] ?? "none";
    if (planned.current_milestone !== "none") planned.latest_review = resetLatestReview();
    const nextMilestone = planned.milestones?.[planned.current_milestone];
    const continuationEligible = nextMilestone?.kind === "implementation" && nextMilestone.state === "planned";
    return { status: "completed", candidate: next, operationResult: { completed_milestone: request.milestone_id, continuation_eligible: continuationEligible, next_milestone: planned.current_milestone } };
  }

  if (request.operation === "migrate") {
    if (request.source_schema_version !== 1) throw operationError("RL_UNSUPPORTED_SCHEMA", "only legacy coordination schema 1 is supported for migration", "migration-source", [String(request.source_schema_version)]);
    if (change.lifecycle_cli?.schema_version === 2) return { status: "already-recorded", candidate: change };
    const prior = change.lifecycle_cli?.schema_version === 1 ? coordination(change) : { artifacts: migrateArtifactRegistrations(root, change), reviews: {}, package_reviews: {}, validations: {}, resolutions: {}, milestones: {} };
    next.lifecycle_cli = { ...prior, schema_version: 2, package_reviews: prior.package_reviews ?? {}, correction_history: prior.correction_history ?? {}, withdrawals: prior.withdrawals ?? {} };
    return { status: "migrated", candidate: next };
  }

  throw operationError("RL_INVALID_REQUEST", `operation ${request.operation} is not implemented by the evidence evaluator`, "operation-vocabulary", [request.operation]);
}

export function operationDiagnostic(error) {
  return error.diagnostic ?? { code: error.code ?? "RL_POST_VALIDATION_FAILED", summary: error.message, blocking_invariant: "lifecycle-operation", relevant_identities: [], corrective_operation: null };
}
