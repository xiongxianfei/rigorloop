import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync } from "node:fs";
import { relative, resolve, sep } from "node:path";

import { compactWriterStatus, loadPackagedCompactActivation } from "./compact-activation.js";
import { parseCompactYaml, validateCompactPath, validateCompactRecord, validateCompactSet, validateCompactVocabulary } from "./compact-contract.js";
import { evaluateCompactOperation } from "./compact-operations.js";
import { projectCompactSnapshot } from "./compact-projection.js";
import { inspectCompactTransaction, recoverCompactTransaction, runCompactTransaction } from "./compact-transaction.js";
import { parseLifecycleYaml } from "./lifecycle-contract.js";
import { findRepositoryRoot } from "./lifecycle-read.js";

function diagnostic(code, summary, invariant, operation = null, identities = [], nextOperation = null) {
  return { code, summary, invariant, scope: operation === null ? "progression" : "operation", operation, identities, next_operation: nextOperation };
}

function sha256(bytes) {
  return `sha256:${createHash("sha256").update(bytes).digest("hex")}`;
}

function result(status, changeId = null, error = null, projection = null) {
  const value = {
    schema: "compact-result-v1",
    status,
    change_id: changeId,
    prior_lifecycle_revision: null,
    resulting_lifecycle_revision: null,
    affected_paths: [],
    bytes_changed: false,
    blockers: [],
    errors: error ? [diagnostic(error.code ?? "RL_COMPACT_FAILED", error.message ?? "Compact operation failed", "compact-cli", error.operation ?? null, error.identities ?? [], error.nextOperation ?? null)] : [],
    next_operation: error?.nextOperation ?? null,
    projection,
  };
  return validateCompactRecord(value, "compact-result-v1");
}

function safeRead(root, path, nullable = false) {
  validateCompactPath(path);
  const absolute = resolve(root, path);
  const rel = relative(root, absolute);
  if (rel === ".." || rel.startsWith(`..${sep}`)) throw Object.assign(new Error("path escapes repository"), { code: "RL_UNSAFE_PATH" });
  let cursor = root;
  for (const part of path.split("/")) {
    cursor = resolve(cursor, part);
    if (existsSync(cursor) && lstatSync(cursor).isSymbolicLink()) throw Object.assign(new Error("path crosses a symbolic link"), { code: "RL_UNSAFE_PATH" });
  }
  if (!existsSync(absolute)) {
    if (nullable) return null;
    throw Object.assign(new Error(`required path is missing: ${path}`), { code: "RL_CHANGE_NOT_FOUND" });
  }
  if (!lstatSync(absolute).isFile()) throw Object.assign(new Error("path is not a regular file"), { code: "RL_UNSAFE_PATH" });
  return readFileSync(absolute);
}

function changePath(changeId) {
  validateCompactPath(changeId, "change id");
  if (changeId.includes("/")) throw Object.assign(new Error("change id must be one path segment"), { code: "RL_INVALID_REQUEST" });
  return `docs/changes/${changeId}/change.yaml`;
}

function loadCompactSet(root, changeId, expected = null) {
  const coordinatorPath = changePath(changeId);
  const coordinator = safeRead(root, coordinatorPath);
  let header;
  try { header = parseLifecycleYaml(coordinator.toString("utf8")); }
  catch (error) { throw Object.assign(new Error("change coordinator is malformed"), { code: "RL_INVALID_CURRENT_STATE", cause: error }); }
  if (header.lifecycle_contract !== "compact-current-state-v1") throw Object.assign(new Error("legacy changes remain on their registered contract and reject compact writes or migration"), { code: "RL_UNSUPPORTED_CONTRACT" });
  const change = parseCompactYaml(coordinator.toString("utf8"), "compact-change-v1");
  const authoritative = new Set([
    coordinatorPath,
    ...Object.values(change.artifacts).map((entry) => entry.path),
    ...Object.values(change.reviews).map((entry) => entry.path),
    ...Object.values(change.material_decisions).map((entry) => entry.path),
    ...Object.values(change.evidence).map((entry) => entry.manifest_path),
    ...(change.readiness === "verified" ? [`docs/changes/${changeId}/verify-report.md`] : []),
  ]);
  if (expected) for (const path of Object.keys(expected)) authoritative.add(path);
  const files = Object.fromEntries([...authoritative].sort().map((path) => [path, safeRead(root, path, expected?.[path]?.state === "absent")]));
  return { change, files };
}

function projectionSelection(root, change, files, view, requestedOperation) {
  const snapshot = structuredClone(change);
  const allEvidence = ["summary", "evidence", "verification", "skill-context"].includes(view) || requestedOperation === "record-verify";
  const evidenceIds = allEvidence ? Object.keys(snapshot.evidence) : [];
  const requiredPaths = new Set([changePath(change.change_id)]);
  const include = (entries, pathField) => Object.values(entries).forEach((entry) => requiredPaths.add(entry[pathField]));
  if (["summary", "verification", "skill-context"].includes(view)) {
    include(snapshot.artifacts, "path");
    include(snapshot.reviews, "path");
    include(snapshot.material_decisions, "path");
  } else if (view === "reviews") include(snapshot.reviews, "path");
  else if (view === "material-decisions") include(snapshot.material_decisions, "path");
  if (allEvidence) include(snapshot.evidence, "manifest_path");

  const manifests = new Map();
  for (const evidenceId of evidenceIds) {
    const reference = snapshot.evidence[evidenceId];
    if (!reference) continue;
    if (!manifests.has(reference.manifest_path)) manifests.set(reference.manifest_path, parseCompactYaml(files[reference.manifest_path].toString("utf8"), "compact-evidence-v1"));
    const entry = manifests.get(reference.manifest_path).evidence[evidenceId];
    if (!entry || entry.freshness !== "current") continue;
    for (const dependency of entry.invalidating_dependencies.filter((item) => item.kind === "subject")) {
      const subject = entry.subjects[dependency.id];
      requiredPaths.add(subject.path);
      const observed = safeRead(root, subject.path, true);
      const observedIdentity = observed === null ? null : sha256(observed);
      if (observedIdentity === dependency.identity) continue;
      reference.freshness = "stale";
      snapshot.readiness = "blocked";
      snapshot.blockers.push({
        ...diagnostic("RL_EVIDENCE_DRIFT", `Evidence ${evidenceId} subject ${dependency.id} no longer matches its current identity`, "evidence-freshness"),
        identities: [evidenceId, dependency.id, dependency.identity, observedIdentity ?? "absent"],
        next_operation: "invalidate-evidence",
      });
    }
  }
  return { snapshot, requiredPaths: [...requiredPaths] };
}

function authoritativeFiles(change, set) {
  const selected = new Set([
    ...Object.values(change.artifacts).map((entry) => entry.path),
    ...Object.values(change.reviews).map((entry) => entry.path),
    ...Object.values(change.material_decisions).map((entry) => entry.path),
    ...Object.values(change.evidence).map((entry) => entry.manifest_path),
    ...(change.readiness === "verified" ? [`docs/changes/${change.change_id}/verify-report.md`] : []),
  ]);
  return Object.fromEntries([...selected].sort().map((path) => [path, set[path]]));
}

function parseFlags(args, allowed) {
  const values = {};
  for (let index = 0; index < args.length; index += 1) {
    const name = args[index];
    if (!allowed.includes(name) || !args[index + 1]) throw Object.assign(new Error(`unknown or incomplete compact argument ${name}`), { code: "RL_INVALID_REQUEST" });
    values[name.slice(2).replaceAll("-", "_")] = args[++index];
  }
  return values;
}

function readRequest(root, flags) {
  if (Boolean(flags.request) === Boolean(flags.request_json)) throw Object.assign(new Error("provide exactly one of --request or --request-json"), { code: "RL_INVALID_REQUEST" });
  const text = flags.request_json ?? (flags.request === "-" ? readFileSync(0, "utf8") : safeRead(root, flags.request).toString("utf8"));
  try { return JSON.parse(text); }
  catch { throw Object.assign(new Error("request transport must contain one JSON object"), { code: "RL_INVALID_REQUEST" }); }
}

function human(value) {
  if (value.projection) return `RigorLoop compact projection: success\nChange: ${value.change_id}\nStage: ${value.projection.current_stage}\nProgression: ${value.projection.progression_status}\nPermitted operations: ${value.projection.permitted_operations.join(", ") || "none"}\n`;
  const issue = value.errors?.[0];
  return `RigorLoop compact: ${value.status}\n${value.change_id ? `Change: ${value.change_id}\n` : ""}${issue ? `${issue.code}: ${issue.summary}\n${issue.identities.length ? `Identities: ${issue.identities.join(", ")}\n` : ""}` : ""}`;
}

export function executeCompactCli(args, options = {}) {
  const root = findRepositoryRoot(options.cwd ?? process.cwd());
  const activation = compactWriterStatus(options.activation ?? loadPackagedCompactActivation());
  const [capability, ...rest] = args;
  let format = "human";
  let knownChangeId = null;
  try {
    if (capability === "project") {
      const flags = parseFlags(rest, ["--change", "--view", "--requested-operation", "--format"]);
      format = flags.format ?? "human";
      if (!flags.change || !flags.view || !["human", "json"].includes(format)) throw Object.assign(new Error("project requires --change, --view, and a valid --format"), { code: "RL_INVALID_REQUEST" });
      knownChangeId = flags.change;
      if (flags.requested_operation) validateCompactVocabulary("Operation", flags.requested_operation);
      const recovery = inspectCompactTransaction({ root, changeId: flags.change });
      if (recovery.status !== "clear") throw Object.assign(new Error("compact recovery must be resolved before projection"), { code: recovery.status === "busy" ? "RL_OPERATION_BUSY" : "RL_RECOVERY_REQUIRED", identities: recovery.recovery_identity ? [recovery.recovery_identity] : [], nextOperation: recovery.status === "busy" ? null : "recover" });
      const { change, files } = loadCompactSet(root, flags.change);
      const selected = projectionSelection(root, change, files, flags.view, flags.requested_operation ?? null);
      const projection = projectCompactSnapshot(selected.snapshot, flags.view, { requestedOperation: flags.requested_operation ?? null, requiredPaths: selected.requiredPaths });
      const value = result("success", flags.change, null, projection);
      return { result: value, format, exitCode: 0, human: human(value) };
    }
    if (capability === "apply") {
      if (!activation.writer) throw Object.assign(new Error("compact-current-state-v1 writer is withheld; readers remain available"), { code: "RL_INCOMPATIBLE_VERSION" });
      const flags = parseFlags(rest, ["--request", "--request-json", "--format"]);
      format = flags.format ?? "human";
      if (!["human", "json"].includes(format)) throw Object.assign(new Error("apply requires a valid --format"), { code: "RL_INVALID_REQUEST" });
      const request = readRequest(root, flags);
      validateCompactRecord(request, "compact-operation-v1");
      knownChangeId = request.change_id;
      if (request.operation === "recover") throw Object.assign(new Error("use compact recover for explicit recovery"), { code: "RL_INVALID_REQUEST", operation: request.operation });
      const { files } = loadCompactSet(root, request.change_id, request.expected_files);
      const resolvedInputs = Object.fromEntries(Object.values(request.payload).filter((value) => value?.source === "path").map((input) => [input.source_path, safeRead(root, input.source_path)]));
      const candidate = evaluateCompactOperation({ request, currentFiles: files, resolvedInputs });
      const transaction = runCompactTransaction({ root, candidate, validateCandidateSet: (set, revision) => {
        try {
          const coordinator = set[changePath(request.change_id)];
          const coordinatorRecord = parseCompactYaml(coordinator.toString("utf8"), "compact-change-v1");
          const restSet = authoritativeFiles(coordinatorRecord, set);
          return validateCompactSet({ changeBytes: coordinator.toString("utf8"), files: restSet }).change.lifecycle_revision === revision;
        } catch (error) {
          error.code = "RL_POST_VALIDATION_FAILED";
          throw error;
        }
      } });
      return { result: transaction, format, exitCode: transaction.status === "success" || transaction.status === "already-applied" ? 0 : 2, human: human(transaction) };
    }
    if (capability === "recover") {
      const flags = parseFlags(rest, ["--change", "--action", "--expected-recovery-identity", "--format"]);
      format = flags.format ?? "human";
      if (!["human", "json"].includes(format)) throw Object.assign(new Error("recover requires a valid --format"), { code: "RL_INVALID_REQUEST", operation: "recover" });
      if (!flags.change) throw Object.assign(new Error("recover requires --change"), { code: "RL_INVALID_REQUEST", operation: "recover" });
      knownChangeId = flags.change;
      if (!flags.action && !flags.expected_recovery_identity) {
        const recovery = inspectCompactTransaction({ root, changeId: flags.change });
        if (recovery.status === "clear") {
          const value = result("success", flags.change);
          return { result: value, format, exitCode: 0, human: human(value) };
        }
        const error = Object.assign(new Error(recovery.status === "busy" ? "a live compact writer owns the change" : "compact recovery is required"), { code: recovery.status === "busy" ? "RL_OPERATION_BUSY" : "RL_RECOVERY_REQUIRED", operation: "recover", identities: recovery.recovery_identity ? [recovery.recovery_identity] : [], nextOperation: recovery.status === "busy" ? null : "recover" });
        const value = result(recovery.status, flags.change, error);
        return { result: value, format, exitCode: 2, human: human(value) };
      }
      if (!flags.action || !flags.expected_recovery_identity) throw Object.assign(new Error("recover action requires --action and --expected-recovery-identity together"), { code: "RL_INVALID_REQUEST", operation: "recover" });
      const outcome = recoverCompactTransaction({ root, changeId: flags.change, action: flags.action, expectedRecoveryIdentity: flags.expected_recovery_identity, readCompleteSet: () => loadCompactSet(root, flags.change).files, validateCandidateSet: (set, revision) => {
        try {
          const coordinator = set[changePath(flags.change)];
          const coordinatorRecord = parseCompactYaml(coordinator.toString("utf8"), "compact-change-v1");
          return validateCompactSet({ changeBytes: coordinator.toString("utf8"), files: authoritativeFiles(coordinatorRecord, set) }).change.lifecycle_revision === revision;
        } catch { return false; }
      } });
      return { result: outcome, format, exitCode: outcome.status === "success" ? 0 : 2, human: human(outcome) };
    }
    throw Object.assign(new Error(`unknown compact capability ${String(capability)}`), { code: "RL_INVALID_REQUEST" });
  } catch (error) {
    const value = result(error.code === "RL_OPERATION_BUSY" ? "busy" : error.code === "RL_RECOVERY_REQUIRED" ? "recovery-required" : "rejected", knownChangeId, error);
    return { result: value, format, exitCode: ["RL_INVALID_REQUEST", "RL_UNSUPPORTED_CONTRACT"].includes(error.code) ? 4 : 2, human: human(value) };
  }
}
