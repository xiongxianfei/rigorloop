import { createHash } from "node:crypto";
import { existsSync, lstatSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join, relative, resolve, sep } from "node:path";

import { lifecycleRevision, parseLifecycleYaml } from "./lifecycle-contract.js";

const SUPPORTED_CONTRACT = "stage-owned-change-local-v1";
const REVIEW_STAGES = new Set(["proposal-review", "spec-review", "architecture-review", "plan-review", "test-spec-review", "code-review"]);

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
    const expected = state?.identity ?? state?.sha256 ?? state?.review?.artifact_sha256;
    const evidenceState = expected && String(expected).replace(/^sha256:/, "") !== digest ? "stale" : "current";
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

function permittedOperations(change, blockers) {
  if (blockers.length > 0) return [];
  const stage = change.workflow_state?.current_stage;
  const operations = [];
  if (REVIEW_STAGES.has(stage)) operations.push("record-review");
  if (stage === "review-resolution") operations.push("record-finding-resolution");
  if (["implement", "verify", "ci-maintenance"].includes(stage)) operations.push("record-validation");
  const milestone = activeMilestone(change);
  const milestoneState = milestone && change.workflow_state?.planned_work?.milestones?.[milestone]?.state;
  if (stage === "implement" && milestoneState === "planned") operations.push("start-milestone");
  if (stage === "implement" && milestoneState === "implementing") operations.push("complete-milestone");
  return operations;
}

export function interpretGovernedChange(root, selected) {
  const change = selected.change;
  const errors = [];
  if (change.change_id !== selected.id) errors.push(diagnostic("RL_INVALID_REQUEST", "Change directory and change_id do not match.", "change-identity", null, [selected.id, String(change.change_id)]));
  if (change.lifecycle_contract !== SUPPORTED_CONTRACT) errors.push(diagnostic("RL_UNSUPPORTED_SCHEMA", `Unsupported lifecycle contract ${String(change.lifecycle_contract)}.`, "lifecycle-contract", "migrate", [String(change.lifecycle_contract)]));
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
      unresolved_findings: unresolvedFindings,
      stale_evidence: staleEvidence,
      supporting_paths: [relative(root, selected.path), ...collected.artifacts.map((artifact) => artifact.path)].sort(),
    },
    blockers,
    permitted_operations: permittedOperations(change, blockers),
    artifacts: collected.artifacts,
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
  const review = targetId ? interpreted.change.artifact_states?.[targetId]?.review : null;
  const settledInputs = interpreted.artifacts
    .filter((artifact) => ["accepted", "approved", "active"].includes(artifact.recorded_state) && artifact.evidence_state === "current" && artifact.artifact_id !== targetId)
    .map(({ artifact_id, path, sha256 }) => ({ artifact_id, path, sha256 }));
  return {
    exact_change: interpreted.change_id,
    operation: stage,
    target_artifact: target ? { artifact_id: target.artifact_id, path: target.path, sha256: target.sha256 } : null,
    settled_upstream_inputs: settledInputs,
    review_round: REVIEW_STAGES.has(stage) ? review?.round ?? "r1" : null,
    authorized_output_path: target?.path ?? null,
    blockers: interpreted.blockers,
    lifecycle_revision: interpreted.lifecycle_revision,
    permitted_registration_operation: REVIEW_STAGES.has(stage) ? "record-review" : stage === "review-resolution" ? "record-finding-resolution" : ["implement", "verify", "ci-maintenance"].includes(stage) ? "record-validation" : null,
  };
}

export function lifecycleDiagnostic(code, summary, invariant, correctiveOperation = null, identities = []) {
  return diagnostic(code, summary, invariant, correctiveOperation, identities);
}
