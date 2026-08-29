import { createHash } from "node:crypto";
import { existsSync, lstatSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";

import { allowedNextStages, lifecycleRevision, parseLifecycleYaml } from "./lifecycle-contract.js";

const SUPPORTED_CONTRACT = "stage-owned-change-local-v1";
const REVIEW_STAGES = new Set(["proposal-review", "spec-review", "architecture-review", "plan-review", "test-spec-review", "code-review"]);
const CORRECTION_REASONS = new Set(["upstream-contract-gap", "upstream-proof-gap", "upstream-ownership-gap", "upstream-planning-gap", "upstream-stale-input"]);
const CORRECTION_DESTINATIONS = new Set(["proposal", "spec", "architecture", "plan", "test-spec"]);
const CORRECTION_STAGE_ORDER = ["proposal", "proposal-review", "spec", "spec-review", "architecture", "architecture-review", "plan", "plan-review", "test-spec", "test-spec-review", "implement", "code-review", "review-resolution", "explain-change", "verify", "pr"];

function diagnostic(code, summary, invariant, correctiveOperation = null, identities = []) {
  return { code, summary, blocking_invariant: invariant, relevant_identities: identities, corrective_operation: correctiveOperation };
}

function repositoryPath(root, candidate) {
  if (typeof candidate !== "string" || !candidate || candidate.includes("\\") || candidate.split("/").some((part) => !part || part === "." || part === "..")) return null;
  const absolute = resolve(root, candidate);
  const rel = relative(root, absolute);
  if (rel.startsWith(`..${sep}`) || rel === ".." || rel.startsWith(sep)) return null;
  let cursor = root;
  for (const part of candidate.split("/")) {
    cursor = join(cursor, part);
    if (existsSync(cursor) && lstatSync(cursor).isSymbolicLink()) return null;
  }
  return absolute;
}

export function findRepositoryRoot(start) {
  let cursor = resolve(start);
  while (true) {
    if (existsSync(join(cursor, ".git")) || existsSync(join(cursor, "docs", "changes"))) return cursor;
    const parent = dirname(cursor);
    if (parent === cursor) return resolve(start);
    cursor = parent;
  }
}

function changeCandidates(root) {
  const changesRoot = join(root, "docs", "changes");
  if (!existsSync(changesRoot) || !lstatSync(changesRoot).isDirectory()) return [];
  return readdirSync(changesRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !entry.isSymbolicLink())
    .map((entry) => ({ id: entry.name, path: join(changesRoot, entry.name, "change.yaml") }))
    .filter((entry) => existsSync(entry.path) && lstatSync(entry.path).isFile())
    .sort((left, right) => left.id.localeCompare(right.id));
}

function readCandidate(candidate) {
  try {
    const bytes = readFileSync(candidate.path, "utf8");
    return { ...candidate, bytes, change: parseLifecycleYaml(bytes) };
  } catch (error) {
    return { ...candidate, error };
  }
}

export function selectGovernedChange(root, requestedId) {
  const candidates = changeCandidates(root);
  if (requestedId) {
    const selected = candidates.find((entry) => entry.id === requestedId);
    if (!selected) return { error: diagnostic("RL_CHANGE_NOT_FOUND", `Governed change ${requestedId} was not found.`, "change-selection", null, [requestedId]) };
    return readCandidate(selected);
  }
  const readable = candidates.map(readCandidate);
  const active = readable.filter((entry) => !entry.error && entry.change?.workflow_state?.lifecycle_state === "active");
  if (active.length === 0) return { error: diagnostic("RL_CHANGE_NOT_FOUND", "No active governed change was found.", "change-selection") };
  if (active.length > 1) return { error: diagnostic("RL_AMBIGUOUS_CHANGE", "Multiple active governed changes require --change.", "change-selection", null, active.map((entry) => entry.id)) };
  return active[0];
}

function hashFile(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function collectArtifacts(root, change) {
  const artifacts = [];
  const errors = [];
  for (const [artifactId, state] of Object.entries(change.artifact_states ?? {}).sort(([a], [b]) => a.localeCompare(b))) {
    const path = state?.path;
    const absolute = repositoryPath(root, path);
    if (!absolute || !existsSync(absolute) || !lstatSync(absolute).isFile()) {
      errors.push(diagnostic("RL_INVALID_REQUEST", `Artifact ${artifactId} does not identify a safe regular file.`, "artifact-identity", null, [artifactId, String(path)]));
      artifacts.push({ artifact_id: artifactId, path, recorded_state: state?.lifecycle_state ?? "unknown", evidence_state: "missing" });
      continue;
    }
    const digest = hashFile(absolute);
    const expected = state?.identity ?? state?.sha256 ?? state?.review?.artifact_sha256 ?? change.lifecycle_cli?.artifacts?.[artifactId]?.artifact_sha256;
    const evidenceState = expected !== undefined && expected !== null && String(expected).replace(/^sha256:/, "") !== digest ? "stale" : "current";
    artifacts.push({ artifact_id: artifactId, path, sha256: digest, recorded_state: state?.lifecycle_state ?? "unknown", evidence_state: evidenceState });
  }
  return { artifacts, errors };
}

function openFindings(root, changeId) {
  const path = join(root, "docs", "changes", changeId, "review-log.md");
  if (!existsSync(path) || !lstatSync(path).isFile()) return [];
  const findings = [];
  for (const match of readFileSync(path, "utf8").matchAll(/^Open findings:\s*(.+)$/gm)) {
    if (match[1].trim().toLowerCase() === "none") continue;
    findings.push(...match[1].split(",").map((value) => value.trim().replace(/`/g, "")).filter(Boolean));
  }
  return [...new Set(findings)].sort();
}

function activeMilestone(change) {
  return change.workflow_state?.planned_work?.current_milestone ?? null;
}

function expectedAuthorAuthority(kind) {
  return kind === "adr" ? "architecture" : kind;
}

function expectedReviewAuthority(kind) {
  return kind === "adr" ? "architecture-review" : `${kind}-review`;
}

function stageIsComplete(change, stage) {
  const coordination = change.lifecycle_cli;
  const entries = Object.entries(change.artifact_states ?? {}).filter(([, entry]) => entry && (
    stage.endsWith("-review")
      ? expectedReviewAuthority(entry.kind) === stage
      : expectedAuthorAuthority(entry.kind) === stage
  ));
  if (!entries.length) return false;
  if (stage.endsWith("-review")) {
    return entries.every(([artifactId, entry]) => {
      const registeredReview = coordination?.reviews?.[artifactId];
      return ["accepted", "approved", "active"].includes(entry.lifecycle_state)
        && entry.review?.outcome === "approved"
        && (!registeredReview || registeredReview.review_id === entry.review.id);
    });
  }
  return entries.every(([artifactId, entry]) => {
    if (entry.lifecycle_state !== "review-required") return false;
    const registration = coordination?.artifacts?.[artifactId];
    return registration
      ? registration.artifact_path === entry.path && registration.stage_authority === stage
      : Boolean(entry.authoring_evidence);
  });
}

function coordinationErrors(root, change) {
  const state = change.lifecycle_cli;
  if (state?.schema_version !== 2) return [];
  const errors = [];
  const objectMaps = ["artifacts", "reviews", "validations", "resolutions", "milestones", "correction_history", "withdrawals"];
  for (const field of objectMaps) {
    if (!state[field] || Array.isArray(state[field]) || typeof state[field] !== "object") errors.push(diagnostic("RL_INVALID_REQUEST", `Lifecycle coordination ${field} must be a mapping.`, "coordination-schema", null, [field]));
  }
  for (const [routeId, receipt] of Object.entries(state.correction_history ?? {})) {
    if (receipt?.route_id !== routeId || receipt?.status !== "returned") errors.push(diagnostic("RL_INVALID_REQUEST", "Correction history contains an unknown or contradictory route receipt.", "correction-history", null, [routeId, String(receipt?.status)]));
    for (const [pathField, hashField] of [["evidence_path", "evidence_sha256"], ["return_evidence_path", "return_evidence_sha256"]]) {
      const absolute = repositoryPath(root, receipt?.[pathField]);
      if (!absolute || !existsSync(absolute) || !lstatSync(absolute).isFile() || hashFile(absolute) !== receipt?.[hashField]) errors.push(diagnostic("RL_CORRECTION_ROUTE_INVALID", "Correction history evidence is missing or stale.", "correction-history", null, [routeId, String(receipt?.[pathField])]));
    }
  }
  for (const [withdrawalId, receipt] of Object.entries(state.withdrawals ?? {})) {
    if (receipt?.withdrawal_id !== withdrawalId || receipt?.status !== "withdrawn") errors.push(diagnostic("RL_INVALID_REQUEST", "Withdrawal history contains an unknown or contradictory receipt.", "withdrawal-history", null, [withdrawalId, String(receipt?.status)]));
    if (!["architecture", "adr"].includes(receipt?.artifact_kind) || receipt?.reason !== "duplicate-registration") errors.push(diagnostic("RL_INVALID_REQUEST", "Withdrawal history contains an unknown artifact kind or reason.", "withdrawal-history", null, [withdrawalId, String(receipt?.artifact_kind), String(receipt?.reason)]));
    const receiptEvidence = repositoryPath(root, receipt?.evidence_path);
    if (!receiptEvidence || !existsSync(receiptEvidence) || !lstatSync(receiptEvidence).isFile() || hashFile(receiptEvidence) !== receipt?.evidence_sha256) errors.push(diagnostic("RL_INVALID_REQUEST", "Withdrawal receipt evidence is missing or stale.", "withdrawal-history", null, [withdrawalId, String(receipt?.evidence_path)]));
    if (state.artifacts?.[receipt?.artifact_id]?.artifact_path === receipt?.artifact_path) errors.push(diagnostic("RL_INVALID_REQUEST", "A withdrawn registration is still active.", "withdrawal-history", null, [withdrawalId, String(receipt?.artifact_id)]));
  }
  const route = state.active_correction;
  if (route) {
    const destination = change.artifact_states?.[route.destination_artifact_id];
    const registration = state.artifacts?.[route.destination_artifact_id];
    const absolute = repositoryPath(root, route.evidence_path);
    const evidenceCurrent = absolute && existsSync(absolute) && lstatSync(absolute).isFile() && hashFile(absolute) === route.evidence_sha256;
    const allowedCurrentStages = new Set([route.destination_stage, `${route.destination_stage}-review`]);
    const snapshot = route.source_snapshot;
    if (route.status !== "active") errors.push(diagnostic("RL_CORRECTION_ROUTE_INVALID", "Active correction has an unknown status.", "active-correction-route", null, [String(route.status)]));
    if (!CORRECTION_REASONS.has(route.reason) || !CORRECTION_DESTINATIONS.has(route.destination_stage)) errors.push(diagnostic("RL_CORRECTION_ROUTE_INVALID", "Active correction has an unknown reason or destination stage.", "active-correction-route", null, [String(route.reason), String(route.destination_stage)]));
    if (!destination || registration?.artifact_path !== destination.path) errors.push(diagnostic("RL_CORRECTION_ROUTE_INVALID", "Active correction destination is missing or mismatched.", "active-correction-route", null, [String(route.destination_artifact_id)]));
    const destinationAbsolute = repositoryPath(root, destination?.path);
    if (change.workflow_state?.current_stage !== route.destination_stage && (!destinationAbsolute || !existsSync(destinationAbsolute) || hashFile(destinationAbsolute) !== registration?.artifact_sha256)) errors.push(diagnostic("RL_CORRECTION_ROUTE_INVALID", "Active correction destination registration is stale.", "active-correction-route", null, [String(route.destination_artifact_id)]));
    if (!evidenceCurrent) errors.push(diagnostic("RL_CORRECTION_ROUTE_INVALID", "Active correction evidence is missing or stale.", "active-correction-evidence", null, [String(route.evidence_path)]));
    if (!snapshot || snapshot.current_stage !== route.return_stage || !Object.hasOwn(snapshot, "blocker") || !Array.isArray(snapshot.finding_ids)) errors.push(diagnostic("RL_CORRECTION_ROUTE_INVALID", "Active correction source snapshot is incomplete or contradictory.", "active-correction-snapshot", null, [String(route.route_id)]));
    if (!allowedCurrentStages.has(change.workflow_state?.current_stage) || change.workflow_state?.blocker !== null) errors.push(diagnostic("RL_CORRECTION_ROUTE_INVALID", "Workflow routing contradicts the active correction.", "active-correction-routing", null, [String(change.workflow_state?.current_stage), String(change.workflow_state?.blocker)]));
  }
  return errors;
}

function permittedOperations(change, blockers) {
  const stage = change.workflow_state?.current_stage;
  const operations = [];
  const targetId = artifactForStage(stage);
  const target = targetId ? change.artifact_states?.[targetId] : null;
  const registeredReview = targetId ? change.lifecycle_cli?.reviews?.[targetId] : null;
  const blockerCodes = new Set(blockers.map((blocker) => blocker.code));
  const onlyOpenFindings = blockerCodes.size === 1 && blockerCodes.has("RL_UNRESOLVED_MATERIAL_FINDING");
  const coordination = change.lifecycle_cli;

  if (coordination?.active_correction) {
    const route = coordination.active_correction;
    if (stage === route.destination_stage) return ["record-artifact-revision"];
    if (stage === `${route.destination_stage}-review`) {
      const routeTarget = change.artifact_states?.[route.destination_artifact_id];
      if (!coordination.reviews?.[route.destination_artifact_id]) return ["record-review"];
      if (["accepted", "approved", "active"].includes(routeTarget?.lifecycle_state)) return ["return-correction"];
      return ["settle-artifact"];
    }
  }
  const sourceIndex = CORRECTION_STAGE_ORDER.indexOf(stage);
  const eligibleDestinationIds = Object.entries(change.artifact_states ?? {}).filter(([artifactId, entry]) => {
    const destinationStage = entry?.kind === "adr" ? "architecture" : entry?.kind;
    return ["proposal", "spec", "architecture", "plan", "test-spec"].includes(destinationStage)
      && CORRECTION_STAGE_ORDER.indexOf(destinationStage) < sourceIndex
      && ["accepted", "approved", "active"].includes(entry?.lifecycle_state)
      && coordination?.artifacts?.[artifactId]?.artifact_path === entry?.path;
  }).map(([artifactId]) => artifactId);
  const staleIdentities = blockers.filter((blocker) => blocker.code === "RL_STALE_EVIDENCE").flatMap((blocker) => blocker.relevant_identities ?? []);
  const staleCorrectionIsRoutable = staleIdentities.length === 0
    || (blockerCodes.has("RL_UNRESOLVED_MATERIAL_FINDING") && staleIdentities.every((artifactId) => eligibleDestinationIds.includes(artifactId)));
  const routeCompatibleBlockers = staleCorrectionIsRoutable && blockers.every((blocker) => ["RL_OPERATION_NOT_PERMITTED", "RL_UNRESOLVED_MATERIAL_FINDING", "RL_STALE_EVIDENCE"].includes(blocker.code));
  if (coordination?.schema_version === 2 && !coordination.active_correction && eligibleDestinationIds.length && routeCompatibleBlockers && (["review-resolution", "code-review", "verify"].includes(stage) || blockers.length)) operations.push("route-correction");

  if (blockers.some((blocker) => blocker.code !== "RL_UNRESOLVED_MATERIAL_FINDING")) return operations;
  if (target?.lifecycle_state === "revision-required") return ["record-artifact-revision"];
  if (REVIEW_STAGES.has(stage) && registeredReview?.outcome === "changes-requested" && onlyOpenFindings) return ["settle-artifact"];
  if (blockers.length > 0) return [...operations, ...(onlyOpenFindings ? ["record-finding-resolution"] : [])];
  if (stage === "plan-review" && target?.kind === "plan" && target.role === "primary" && target.lifecycle_state === "review-required" && ["approved", "clean-with-notes"].includes(registeredReview?.outcome) && !change.workflow_state?.planned_work) return ["initialize-approved-plan"];
  if (stageIsComplete(change, stage) && allowedNextStages(change, stage).length > 0) operations.push("advance-stage");
  if (["proposal", "spec", "architecture", "plan", "test-spec"].includes(stage) && ["authoring", "revision-required"].includes(target?.lifecycle_state)) operations.push("record-artifact-revision");
  if (REVIEW_STAGES.has(stage) && !operations.includes("advance-stage")) operations.push(registeredReview ? "settle-artifact" : "record-review");
  if (stage === "review-resolution") operations.push("record-finding-resolution");
  if (["implement", "verify", "ci-maintenance"].includes(stage)) operations.push("record-validation");
  const milestone = activeMilestone(change);
  const milestoneState = milestone && change.workflow_state?.planned_work?.milestones?.[milestone]?.state;
  if (stage === "implement" && milestoneState === "planned") operations.push("start-milestone");
  if (stage === "implement" && milestoneState === "implementing") operations.push("complete-milestone");
  if (stage === "code-review" && milestoneState === "review-requested") operations.push("complete-milestone");
  return operations;
}

function nextDurableReviewRound(root, changeId, stage) {
  const reviewsRoot = join(root, "docs", "changes", changeId, "reviews");
  if (!existsSync(reviewsRoot) || !lstatSync(reviewsRoot).isDirectory()) return "r1";
  const escapedStage = stage.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const pattern = new RegExp(`^${escapedStage}-r(\\d+)\\.md$`);
  const rounds = readdirSync(reviewsRoot, { withFileTypes: true })
    .filter((entry) => entry.isFile() && !entry.isSymbolicLink())
    .map((entry) => Number(entry.name.match(pattern)?.[1] ?? 0));
  return `r${Math.max(0, ...rounds) + 1}`;
}

export function interpretGovernedChange(root, selected) {
  const change = selected.change;
  const errors = [];
  if (change.change_id !== selected.id) errors.push(diagnostic("RL_INVALID_REQUEST", "Change directory and change_id do not match.", "change-identity", null, [selected.id, String(change.change_id)]));
  if (change.lifecycle_contract !== SUPPORTED_CONTRACT) errors.push(diagnostic("RL_UNSUPPORTED_SCHEMA", `Unsupported lifecycle contract ${String(change.lifecycle_contract)}.`, "lifecycle-contract", "migrate", [String(change.lifecycle_contract)]));
  if (change.lifecycle_cli !== undefined && ![1, 2].includes(change.lifecycle_cli?.schema_version)) errors.push(diagnostic("RL_UNSUPPORTED_SCHEMA", `Unsupported lifecycle CLI schema ${String(change.lifecycle_cli?.schema_version)}.`, "coordination-schema", "migrate", [String(change.lifecycle_cli?.schema_version)]));
  if (change.lifecycle_cli?.active_correction && change.lifecycle_cli.schema_version !== 2) errors.push(diagnostic("RL_UNSUPPORTED_SCHEMA", "Correction state requires lifecycle CLI schema version 2.", "coordination-schema", "migrate"));
  errors.push(...coordinationErrors(root, change));
  const collected = collectArtifacts(root, change);
  errors.push(...collected.errors);
  const unresolvedFindings = openFindings(root, selected.id);
  const staleEvidence = collected.artifacts.filter((artifact) => artifact.evidence_state === "stale").map((artifact) => artifact.artifact_id);
  const blockers = [];
  if (change.workflow_state?.blocker) blockers.push({ code: "RL_OPERATION_NOT_PERMITTED", summary: String(change.workflow_state.blocker), blocking_invariant: "workflow-blocker" });
  if (unresolvedFindings.length) blockers.push({ code: "RL_UNRESOLVED_MATERIAL_FINDING", summary: "Material review findings remain open.", blocking_invariant: "finding-closeout", relevant_identities: unresolvedFindings });
  if (staleEvidence.length) blockers.push({ code: "RL_STALE_EVIDENCE", summary: "Registered evidence is stale.", blocking_invariant: "evidence-freshness", relevant_identities: staleEvidence });
  blockers.push(...errors);
  const referenced = collected.artifacts.filter((artifact) => artifact.sha256).map((artifact) => ({ path: artifact.path, sha256: artifact.sha256 }));
  const revision = lifecycleRevision(change, referenced);
  const recordedState = Object.fromEntries(collected.artifacts.map((artifact) => [artifact.artifact_id, artifact.recorded_state]));
  const evidenceState = Object.fromEntries(collected.artifacts.map((artifact) => [artifact.artifact_id, artifact.evidence_state]));
  return {
    change,
    change_id: selected.id,
    lifecycle_revision: revision,
    effective_state: {
      recorded_state: recordedState,
      evidence_state: evidenceState,
      effective_state: errors.length ? "invalid" : blockers.length ? "blocked" : "current",
      current_stage: change.workflow_state?.current_stage ?? null,
      active_artifact: artifactForStage(change.workflow_state?.current_stage),
      active_milestone: activeMilestone(change),
      active_correction: change.lifecycle_cli?.active_correction ? {
        route_id: change.lifecycle_cli.active_correction.route_id,
        source_stage: change.lifecycle_cli.active_correction.source_snapshot?.current_stage ?? null,
        destination_stage: change.lifecycle_cli.active_correction.destination_stage,
        destination_artifact_id: change.lifecycle_cli.active_correction.destination_artifact_id,
        reason: change.lifecycle_cli.active_correction.reason,
        return_stage: change.lifecycle_cli.active_correction.return_stage,
        milestone_id: change.lifecycle_cli.active_correction.source_snapshot?.milestone_id ?? null,
        milestone_state: change.lifecycle_cli.active_correction.source_snapshot?.milestone_state ?? null,
        finding_ids: change.lifecycle_cli.active_correction.source_snapshot?.finding_ids ?? [],
        evidence_path: change.lifecycle_cli.active_correction.evidence_path,
      } : null,
      unresolved_findings: unresolvedFindings,
      stale_evidence: staleEvidence,
      supporting_paths: [relative(root, selected.path), ...collected.artifacts.map((artifact) => artifact.path)].sort(),
    },
    blockers,
    permitted_operations: permittedOperations(change, blockers),
    artifacts: collected.artifacts,
    next_review_rounds: Object.fromEntries([...REVIEW_STAGES].map((stage) => [stage, nextDurableReviewRound(root, selected.id, stage)])),
    warnings: [],
    errors,
  };
}

function artifactForStage(stage) {
  const normalized = String(stage ?? "").replace(/-review$/, "");
  if (["proposal", "spec", "architecture", "plan", "test-spec"].includes(normalized)) return normalized;
  if (["implement", "code-review", "verify", "explain-change"].includes(stage)) return "plan";
  return null;
}

export function contextForStage(interpreted, stage) {
  const targetId = artifactForStage(stage);
  const target = targetId ? interpreted.artifacts.find((artifact) => artifact.artifact_id === targetId) : null;
  const registeredReview = targetId ? interpreted.change.lifecycle_cli?.reviews?.[targetId] : null;
  const directDependencies = {
    proposal: [],
    spec: ["proposal"],
    architecture: ["spec"],
    plan: ["spec", "architecture"],
    "test-spec": ["spec", "architecture", "plan"],
  }[stage] ?? [];
  const settledInputs = interpreted.artifacts
    .filter((artifact) => directDependencies.includes(artifact.artifact_id) && ["accepted", "approved", "active"].includes(artifact.recorded_state) && artifact.evidence_state === "current")
    .map(({ artifact_id, path, sha256 }) => ({ artifact_id, path, sha256 }));
  const currentStage = interpreted.change.workflow_state?.current_stage;
  const routeAvailable = interpreted.change.lifecycle_cli?.schema_version === 2
    && !interpreted.change.lifecycle_cli?.active_correction
    && interpreted.errors.length === 0
    && interpreted.permitted_operations.includes("route-correction")
    && CORRECTION_STAGE_ORDER.indexOf(stage) >= 0
    && CORRECTION_STAGE_ORDER.indexOf(currentStage) > CORRECTION_STAGE_ORDER.indexOf(stage)
    && ["proposal", "spec", "architecture", "plan", "test-spec"].includes(stage)
    && target
    && ["accepted", "approved", "active"].includes(target.recorded_state);
  return {
    exact_change: interpreted.change_id,
    operation: stage,
    target_artifact: target ? { artifact_id: target.artifact_id, path: target.path, sha256: target.sha256 } : null,
    settled_upstream_inputs: settledInputs,
    review_round: REVIEW_STAGES.has(stage) ? registeredReview?.round ?? interpreted.next_review_rounds?.[stage] ?? "r1" : null,
    authorized_output_path: target?.path ?? null,
    blockers: interpreted.blockers,
    lifecycle_revision: interpreted.lifecycle_revision,
    permitted_registration_operation: routeAvailable ? null : interpreted.permitted_operations.includes("initialize-approved-plan") ? "initialize-approved-plan" : interpreted.permitted_operations.includes("advance-stage") ? "advance-stage" : REVIEW_STAGES.has(stage) ? "record-review" : stage === "review-resolution" ? "record-finding-resolution" : ["proposal", "spec", "architecture", "plan", "test-spec"].includes(stage) ? "record-artifact-revision" : ["implement", "verify", "ci-maintenance"].includes(stage) ? "record-validation" : null,
    ...(routeAvailable ? { route_required: { code: "RL_WORKFLOW_ROUTE_REQUIRED", current_stage: currentStage, requested_stage: stage, route_owner: "workflow", finding_ids: interpreted.effective_state.unresolved_findings }, available_after_workflow_route: "record-artifact-revision" } : {}),
  };
}

export function lifecycleDiagnostic(code, summary, invariant, correctiveOperation = null, identities = []) {
  return diagnostic(code, summary, invariant, correctiveOperation, identities);
}
