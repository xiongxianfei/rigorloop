import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync, readdirSync } from "node:fs";
import { basename, dirname, join, relative, resolve, sep } from "node:path";

import { LIFECYCLE_ERROR_CODES, parseLifecycleYaml, serializeLifecycleYaml, validateLifecycleRequest } from "./lifecycle-contract.js";
import { evaluateLifecycleOperation, operationDiagnostic } from "./lifecycle-operations.js";
import { contextForStage, findRepositoryRoot, interpretGovernedChange, lifecycleDiagnostic, selectGovernedChange } from "./lifecycle-read.js";
import { clearOrphanedLifecycleLock, inspectLifecycleLock, inspectLifecycleRecovery, reconcileInterruptedTransaction, runLifecycleTransaction } from "./lifecycle-transaction.js";
import { renderResult, RESULT_FORMATS } from "./result-renderer.js";

const RESULT_FIELDS = ["schema_version", "command", "operation", "status", "change_id", "lifecycle_revision", "effective_state", "blockers", "permitted_operations", "artifacts", "warnings", "errors"];
const MUTATING_OPERATIONS = new Set(["record-artifact-revision", "record-review", "record-validation", "record-finding-resolution", "settle-artifact", "record-package-review", "settle-review-package", "advance-stage", "initialize-approved-plan", "start-milestone", "complete-milestone", "record-final-review", "route-correction", "return-correction", "withdraw-artifact-registration", "migrate", "repair"]);
const REPAIR_CHANGED_STATUSES = new Set(["cleared-orphaned-lock", "restored-prior", "committed-candidate", "abandoned-prepared"]);
const REPAIR_UNCHANGED_STATUSES = new Set(["already-clear", "nothing-to-reconcile"]);
const UNSAFE_RECOVERY_CODES = new Set(["RL_RECOVERY_REQUIRED", "RL_REPAIR_UNSAFE"]);
const INTERNAL_ERROR_CODES = new Set(["RL_POST_VALIDATION_FAILED"]);
const EXPECTED_REJECTION_CODES = new Set(LIFECYCLE_ERROR_CODES.filter((code) => !UNSAFE_RECOVERY_CODES.has(code) && !INTERNAL_ERROR_CODES.has(code)));

export function lifecycleTerminalClass(result) {
  const codes = Array.isArray(result?.errors) ? result.errors.map((error) => error?.code) : [];
  if ((result?.status === "success" || result?.status === "already-recorded") && codes.length === 0) return "success";
  if (codes.some((code) => !LIFECYCLE_ERROR_CODES.includes(code) || INTERNAL_ERROR_CODES.has(code))) return "internal-error";
  if (codes.some((code) => UNSAFE_RECOVERY_CODES.has(code))) return "unsafe-recovery";
  if ((codes.length > 0 && codes.every((code) => EXPECTED_REJECTION_CODES.has(code))) || (result?.status === "blocked" && codes.length === 0)) return "expected-rejection";
  return "internal-error";
}

export function repairStateChanged(status) {
  if (REPAIR_CHANGED_STATUSES.has(status)) return true;
  if (REPAIR_UNCHANGED_STATUSES.has(status)) return false;
  throw Object.assign(new Error(`Unknown repair result status: ${String(status)}`), { code: "RL_POST_VALIDATION_FAILED" });
}

function lifecycleOwnedSnapshot(changePath) {
  const directory = dirname(changePath);
  const changeName = basename(changePath);
  let names;
  try {
    names = readdirSync(directory).filter((name) => name === changeName || name.startsWith(".rigorloop-lifecycle-")).sort();
  } catch (error) {
    return `directory-error:${error.code ?? error.name}`;
  }
  return names.map((name) => {
    const path = join(directory, name);
    try {
      const stat = lstatSync(path);
      if (!stat.isFile()) return `${name}:non-file:${stat.mode & 0o170000}`;
      const digest = createHash("sha256").update(readFileSync(path)).digest("hex");
      return `${name}:file:${digest}`;
    } catch (error) {
      return `${name}:read-error:${error.code ?? error.name}`;
    }
  }).join("\n");
}

function parseArgs(args) {
  const [operation, maybeStage, ...rest] = args;
  const positional = operation === "context" ? [maybeStage] : [];
  const flags = operation === "context" ? rest : args.slice(1);
  let format = "human";
  let change;
  let request;
  let dryRun = false;
  for (let index = 0; index < flags.length; index += 1) {
    if (flags[index] === "--format" && flags[index + 1]) format = flags[++index];
    else if (flags[index] === "--change" && flags[index + 1]) change = flags[++index];
    else if (flags[index] === "--request" && flags[index + 1]) request = flags[++index];
    else if (flags[index] === "--dry-run") dryRun = true;
    else return { error: `Unknown or incomplete lifecycle argument ${flags[index]}` };
  }
  if (!operation || !["status", "context", "validate", ...MUTATING_OPERATIONS].includes(operation)) return { error: `Unknown lifecycle operation ${String(operation)}` };
  if (operation === "context" && (!positional[0] || positional[0].startsWith("--"))) return { error: "context requires a stage" };
  if (MUTATING_OPERATIONS.has(operation) && !request) return { error: `${operation} requires --request` };
  if (!MUTATING_OPERATIONS.has(operation) && (request || dryRun)) return { error: `${operation} does not accept mutation flags` };
  if (!RESULT_FORMATS.includes(format)) return { error: `Unknown format ${format}` };
  return { operation, stage: positional[0], format, change, request, dryRun };
}

function baseResult(operation, overrides = {}) {
  return {
    schema_version: 1,
    command: "lifecycle",
    operation,
    status: "success",
    change_id: null,
    lifecycle_revision: null,
    effective_state: null,
    blockers: [],
    permitted_operations: [],
    artifacts: [],
    warnings: [],
    errors: [],
    ...overrides,
  };
}

function withStateChanged(result, stateChanged) {
  Object.defineProperty(result, "state_changed", { value: stateChanged, enumerable: false });
  return result;
}

function errorResult(operation, error, status = "error") {
  return baseResult(operation ?? null, { status, blockers: [error], errors: [error] });
}

function resultExitCode(result) {
  const code = result.errors[0]?.code;
  if (result.status === "success") return 0;
  if (result.status === "already-recorded") return 0;
  if (result.status === "blocked" && result.errors.length === 0) return 2;
  if (["RL_INVALID_REQUEST", "RL_UNSUPPORTED_SCHEMA", "RL_INCOMPATIBLE_VERSION"].includes(code)) return 4;
  if (code === "RL_STALE_OPERATION") return 5;
  if (["RL_CHANGE_NOT_FOUND", "RL_AMBIGUOUS_CHANGE", "RL_OPERATION_NOT_PERMITTED", "RL_UNRESOLVED_MATERIAL_FINDING", "RL_AUTHORITY_BOUNDARY", "RL_OPERATION_BUSY", "RL_RECOVERY_REQUIRED", "RL_WORKFLOW_ROUTE_REQUIRED", "RL_CORRECTION_ROUTE_INVALID", "RL_ARTIFACT_PATH_OWNED", "RL_WITHDRAWAL_UNSAFE"].includes(code)) return 2;
  return 3;
}

function human(result) {
  const lines = [`RigorLoop lifecycle ${result.operation ?? "request"}: ${result.status}`];
  if (result.change_id) lines.push(`Change: ${result.change_id}`);
  if (result.lifecycle_revision) lines.push(`Lifecycle revision: ${result.lifecycle_revision}`);
  if (result.effective_state?.effective_state) lines.push(`Effective state: ${result.effective_state.effective_state}`);
  if (result.effective_state?.current_stage) lines.push(`Current stage: ${result.effective_state.current_stage}`);
  if (result.effective_state?.active_artifact) lines.push(`Active artifact: ${result.effective_state.active_artifact}`);
  if (result.effective_state?.active_milestone) lines.push(`Active milestone: ${result.effective_state.active_milestone}`);
  if (result.effective_state?.active_correction) lines.push(`Active correction: ${result.effective_state.active_correction.route_id}; ${result.effective_state.active_correction.source_stage} -> ${result.effective_state.active_correction.destination_stage}; milestone ${result.effective_state.active_correction.milestone_id ?? "none"}`);
  if (result.effective_state?.unresolved_findings?.length) lines.push(`Unresolved findings: ${result.effective_state.unresolved_findings.join(", ")}`);
  if (result.effective_state?.stale_evidence?.length) lines.push(`Stale evidence: ${result.effective_state.stale_evidence.join(", ")}`);
  if (result.operation !== "context") for (const artifact of result.artifacts) lines.push(`Artifact ${artifact.artifact_id}: ${artifact.recorded_state}; evidence ${artifact.evidence_state}; ${artifact.path}`);
  for (const blocker of result.blockers) lines.push(`${blocker.code}: ${blocker.summary}`);
  if (result.permitted_operations.length) lines.push(`Permitted operations: ${result.permitted_operations.join(", ")}`);
  if (result.context) {
    lines.push(`Context operation: ${result.context.operation}`);
    lines.push(`Target artifact: ${result.context.target_artifact ? `${result.context.target_artifact.artifact_id} (${result.context.target_artifact.path})` : "none"}`);
    lines.push(`Settled upstream inputs: ${result.context.settled_upstream_inputs.map((item) => item.artifact_id).join(", ") || "none"}`);
    lines.push(`Review round: ${result.context.review_round ?? "not-applicable"}`);
    lines.push(`Authorized output path: ${result.context.authorized_output_path ?? "none"}`);
    lines.push(`Permitted registration operation: ${result.context.permitted_registration_operation ?? "none"}`);
    if (result.context.route_required) {
      lines.push(`${result.context.route_required.code}: workflow must route ${result.context.route_required.current_stage} -> ${result.context.route_required.requested_stage}`);
      lines.push(`Available after workflow route: ${result.context.available_after_workflow_route}`);
    }
    if (result.context.review_package) {
      const reviewPackage = result.context.review_package;
      lines.push(`Review package: ${reviewPackage.package_kind}; status ${reviewPackage.status}; authority ${reviewPackage.authority}`);
      lines.push(`Package members: ${Object.entries(reviewPackage.members).map(([id, path]) => `${id}=${path}`).join(", ") || "none"}`);
      lines.push(`Upstream review ID: ${reviewPackage.upstream_review_id ?? "none"}`);
    }
  }
  if (result.validation) lines.push(`Repository validation: ${result.validation.valid ? "valid" : "invalid"}`);
  if (result.mutation) lines.push(`Mutation: ${result.mutation.status}; ${result.mutation.changed_path}`);
  if (result.operation_result?.route_id) lines.push(`Route: ${result.operation_result.route_id}`);
  if (result.operation_result?.withdrawal_id) lines.push(`Withdrawal: ${result.operation_result.artifact_id}; ${result.operation_result.artifact_path}; ${result.operation_result.receipt_status}; canonical owner ${result.operation_result.canonical_owner_change_id}`);
  return `${lines.join("\n")}\n`;
}

function readRequestFile(root, path) {
  if (typeof path !== "string" || !path || path.startsWith("/") || path.includes("\\") || path.split("/").some((part) => !part || part === "." || part === "..")) throw Object.assign(new Error("invalid request path"), { code: "RL_INVALID_REQUEST" });
  const absolute = resolve(root, path);
  const rel = relative(root, absolute);
  if (rel === ".." || rel.startsWith(`..${sep}`)) throw Object.assign(new Error("request path escapes repository"), { code: "RL_INVALID_REQUEST" });
  let cursor = root;
  for (const part of path.split("/")) {
    cursor = resolve(cursor, part);
    if (existsSync(cursor) && lstatSync(cursor).isSymbolicLink()) throw Object.assign(new Error("request path traverses symlink"), { code: "RL_INVALID_REQUEST" });
  }
  if (!existsSync(absolute) || !lstatSync(absolute).isFile()) throw Object.assign(new Error("request path must be an existing regular file"), { code: "RL_INVALID_REQUEST" });
  try { return JSON.parse(readFileSync(absolute, "utf8")); } catch { throw Object.assign(new Error("request file must contain one JSON object"), { code: "RL_INVALID_REQUEST" }); }
}

export function executeLifecycleCli(args, options = {}) {
  const parsed = parseArgs(args);
  if (parsed.error) {
    const error = lifecycleDiagnostic("RL_INVALID_REQUEST", parsed.error, "command-input");
    const result = errorResult(args[0], error);
    return { result, exitCode: resultExitCode(result), format: args.includes("json") ? "json" : "human", human: human(result) };
  }
  const root = findRepositoryRoot(options.cwd ?? process.cwd());
  const selected = selectGovernedChange(root, parsed.change);
  if (selected.error instanceof Error) {
    const error = lifecycleDiagnostic("RL_INVALID_REQUEST", "The selected change record is malformed.", "yaml-domain");
    const result = errorResult(parsed.operation, error);
    return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
  }
  if (selected.error) {
    const result = errorResult(parsed.operation, selected.error, "blocked");
    return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
  }
  const interpreted = interpretGovernedChange(root, selected);
  if (MUTATING_OPERATIONS.has(parsed.operation)) {
    let transitionEvaluated = false;
    let lifecycleBytesBefore;
    try {
      const request = readRequestFile(root, parsed.request);
      const requestValidation = validateLifecycleRequest(request);
      if (!requestValidation.ok) {
        const issue = requestValidation.errors[0];
        const result = errorResult(parsed.operation, { ...issue, relevant_identities: [], corrective_operation: null }, issue.code === "RL_WITHDRAWAL_UNSAFE" ? "blocked" : "error");
        return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
      }
      if (request.operation !== parsed.operation || request.change_id !== interpreted.change_id || (parsed.change && parsed.change !== request.change_id)) {
        const issue = lifecycleDiagnostic("RL_INVALID_REQUEST", "command, selected change, and request envelope do not agree", "request-binding", null, [parsed.operation, request.operation, interpreted.change_id, request.change_id]);
        const result = errorResult(parsed.operation, issue);
        return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
      }
      if (request.expected_lifecycle_revision !== interpreted.lifecycle_revision) {
        if (["record-package-review", "settle-review-package"].includes(request.operation)) {
          try {
            const replay = evaluateLifecycleOperation({ root, change: interpreted.change, request });
            if (replay.status === "already-recorded") {
              const result = withStateChanged(baseResult(parsed.operation, { status: "already-recorded", change_id: interpreted.change_id, lifecycle_revision: interpreted.lifecycle_revision, effective_state: interpreted.effective_state, blockers: interpreted.blockers, permitted_operations: interpreted.permitted_operations, artifacts: interpreted.artifacts, warnings: [], errors: [], mutation: { status: "already-recorded", changed_path: `docs/changes/${interpreted.change_id}/change.yaml` } }), false);
              return { result, exitCode: 0, format: parsed.format, human: human(result) };
            }
          } catch (error) {
            if (error?.code === "RL_STALE_EVIDENCE") {
              const issue = error.diagnostic ?? lifecycleDiagnostic("RL_STALE_EVIDENCE", error.message, "review-package-review-freshness");
              const result = errorResult(parsed.operation, issue);
              return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
            }
            // A stale request that is not an exact semantic replay follows the normal stale rejection.
          }
        }
        const issue = lifecycleDiagnostic("RL_STALE_OPERATION", "expected lifecycle revision is not current", "optimistic-concurrency", null, [request.expected_lifecycle_revision, interpreted.lifecycle_revision]);
        const result = errorResult(parsed.operation, issue, "blocked");
        return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
      }
      if (request.operation === "repair") {
        transitionEvaluated = true;
        lifecycleBytesBefore = lifecycleOwnedSnapshot(selected.path);
        const condition = request.condition;
        const inspection = condition === "clear-orphaned-lock" ? inspectLifecycleLock(selected.path) : inspectLifecycleRecovery(selected.path);
        if (parsed.dryRun) {
          const result = withStateChanged(baseResult(parsed.operation, { status: "success", change_id: interpreted.change_id, lifecycle_revision: interpreted.lifecycle_revision, effective_state: interpreted.effective_state, blockers: interpreted.blockers, permitted_operations: interpreted.permitted_operations, artifacts: interpreted.artifacts, warnings: [], errors: [], mutation: { status: "planned", changed_path: `docs/changes/${interpreted.change_id}/${condition === "clear-orphaned-lock" ? ".rigorloop-lifecycle.lock" : ".rigorloop-lifecycle-recovery.json"}`, condition, observed_state: inspection.state } }), false);
          return { result, exitCode: 0, format: parsed.format, human: human(result) };
        }
        const repair = condition === "clear-orphaned-lock"
          ? clearOrphanedLifecycleLock(selected.path)
          : reconcileInterruptedTransaction({ changePath: selected.path, changeId: interpreted.change_id, validateCandidate: (bytes) => {
              try { return interpretGovernedChange(root, { ...selected, bytes: bytes.toString("utf8"), change: parseLifecycleYaml(bytes.toString("utf8")) }).errors.length === 0; } catch { return false; }
            } });
        const persisted = readFileSync(selected.path, "utf8");
        const after = interpretGovernedChange(root, { ...selected, bytes: persisted, change: parseLifecycleYaml(persisted) });
        const repairChanged = repairStateChanged(repair.status);
        const result = withStateChanged(baseResult(parsed.operation, { status: "success", change_id: after.change_id, lifecycle_revision: after.lifecycle_revision, effective_state: after.effective_state, blockers: after.blockers, permitted_operations: after.permitted_operations, artifacts: after.artifacts, warnings: [], errors: [], mutation: { status: repair.status, changed_path: `docs/changes/${after.change_id}/${condition === "clear-orphaned-lock" ? ".rigorloop-lifecycle.lock" : ".rigorloop-lifecycle-recovery.json"}`, condition } }), repairChanged);
        return { result, exitCode: 0, format: parsed.format, human: human(result) };
      }
      transitionEvaluated = true;
      lifecycleBytesBefore = lifecycleOwnedSnapshot(selected.path);
      const transition = evaluateLifecycleOperation({ root, change: interpreted.change, request });
      if (transition.status === "already-recorded") {
        const result = withStateChanged(baseResult(parsed.operation, { status: "already-recorded", change_id: interpreted.change_id, lifecycle_revision: interpreted.lifecycle_revision, effective_state: interpreted.effective_state, blockers: interpreted.blockers, permitted_operations: interpreted.permitted_operations, artifacts: interpreted.artifacts, warnings: [], errors: [], mutation: { status: "already-recorded", changed_path: `docs/changes/${interpreted.change_id}/change.yaml` } }), false);
        return { result, exitCode: 0, format: parsed.format, human: human(result) };
      }
      const candidateBytes = Buffer.from(serializeLifecycleYaml(transition.candidate), "utf8");
      const candidateSelected = { ...selected, bytes: candidateBytes.toString("utf8"), change: transition.candidate };
      const candidateInterpretation = interpretGovernedChange(root, candidateSelected);
      if (candidateInterpretation.errors.length) throw Object.assign(new Error("candidate lifecycle state is invalid"), { code: "RL_POST_VALIDATION_FAILED" });
      const stateChanged = !parsed.dryRun && candidateInterpretation.lifecycle_revision !== interpreted.lifecycle_revision;
      const mutation = { status: parsed.dryRun ? "planned" : transition.status, changed_path: `docs/changes/${interpreted.change_id}/change.yaml`, prior_lifecycle_revision: interpreted.lifecycle_revision, resulting_lifecycle_revision: candidateInterpretation.lifecycle_revision };
      if (!parsed.dryRun) {
        (options.runLifecycleTransaction ?? runLifecycleTransaction)({
          changePath: selected.path,
          changeId: interpreted.change_id,
          expectedRevision: request.expected_lifecycle_revision,
          currentRevision: interpreted.lifecycle_revision,
          candidateBytes,
          candidateRevision: candidateInterpretation.lifecycle_revision,
          validateCandidate: (bytes) => {
            try {
              const persisted = parseLifecycleYaml(bytes.toString("utf8"));
              return interpretGovernedChange(root, { ...selected, bytes: bytes.toString("utf8"), change: persisted }).errors.length === 0;
            } catch { return false; }
          },
        });
      }
      const result = withStateChanged(baseResult(parsed.operation, { status: "success", change_id: interpreted.change_id, lifecycle_revision: candidateInterpretation.lifecycle_revision, effective_state: candidateInterpretation.effective_state, blockers: candidateInterpretation.blockers, permitted_operations: candidateInterpretation.permitted_operations, artifacts: candidateInterpretation.artifacts, warnings: [], errors: [], mutation, ...(transition.operationResult ? { operation_result: transition.operationResult } : {}) }), stateChanged);
      return { result, exitCode: 0, format: parsed.format, human: human(result) };
    } catch (error) {
      const issue = operationDiagnostic(error);
      const result = errorResult(parsed.operation, issue, ["RL_STALE_OPERATION", "RL_OPERATION_NOT_PERMITTED", "RL_UNRESOLVED_MATERIAL_FINDING", "RL_AUTHORITY_BOUNDARY", "RL_OPERATION_BUSY", "RL_RECOVERY_REQUIRED", "RL_WORKFLOW_ROUTE_REQUIRED", "RL_CORRECTION_ROUTE_INVALID", "RL_ARTIFACT_PATH_OWNED", "RL_WITHDRAWAL_UNSAFE"].includes(issue.code) ? "blocked" : "error");
      if (transitionEvaluated) withStateChanged(result, lifecycleOwnedSnapshot(selected.path) !== lifecycleBytesBefore);
      return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
    }
  }
  const context = parsed.operation === "context" ? contextForStage(interpreted, parsed.stage) : null;
  const routeIssue = context?.route_required ? lifecycleDiagnostic("RL_WORKFLOW_ROUTE_REQUIRED", `Workflow must route from ${context.route_required.current_stage} to ${context.route_required.requested_stage} before authoring can begin.`, "correction-route-ownership", "route-correction", context.route_required.finding_ids) : null;
  const packageIssue = context?.review_package?.errors?.[0] ?? null;
  const contextIssue = context?.errors?.[0] ?? null;
  const result = baseResult(parsed.operation, {
    status: interpreted.errors.length || contextIssue ? "error" : interpreted.blockers.length || routeIssue || packageIssue ? "blocked" : "success",
    change_id: interpreted.change_id,
    lifecycle_revision: interpreted.lifecycle_revision,
    effective_state: interpreted.effective_state,
    blockers: interpreted.blockers,
    permitted_operations: interpreted.permitted_operations,
    artifacts: interpreted.artifacts,
    warnings: interpreted.warnings,
    errors: [...interpreted.errors, ...(routeIssue ? [routeIssue] : []), ...(packageIssue ? [packageIssue] : []), ...(contextIssue ? [contextIssue] : [])],
    ...((routeIssue || packageIssue || contextIssue) ? { blockers: [...interpreted.blockers, ...(routeIssue ? [routeIssue] : []), ...(packageIssue ? [packageIssue] : []), ...(contextIssue ? [contextIssue] : [])] } : {}),
    ...(context ? { context } : {}),
    ...(parsed.operation === "validate" ? { validation: { valid: interpreted.errors.length === 0, checks: ["schema", "artifacts", "evidence", "findings", "milestones"] } } : {}),
  });
  for (const field of RESULT_FIELDS) if (!(field in result)) throw new Error(`missing lifecycle result field ${field}`);
  return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
}

export function runLifecycleCli(args, options = {}) {
  const execution = executeLifecycleCli(args, options);
  const rendered = renderResult(execution.result, {
    format: execution.format,
    exitCode: execution.exitCode,
    invocationId: options.invocationId,
    observability: options.observability,
    human: () => execution.human,
  });
  if (execution.format === "human" && execution.exitCode !== 0) process.stderr.write(rendered);
  else process.stdout.write(rendered);
  return execution.exitCode;
}
