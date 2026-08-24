import { contextForStage, findRepositoryRoot, interpretGovernedChange, lifecycleDiagnostic, selectGovernedChange } from "./lifecycle-read.js";

const RESULT_FIELDS = ["schema_version", "command", "operation", "status", "change_id", "lifecycle_revision", "effective_state", "blockers", "permitted_operations", "artifacts", "warnings", "errors"];

function parseArgs(args) {
  const [operation, maybeStage, ...rest] = args;
  const positional = operation === "context" ? [maybeStage] : [];
  const flags = operation === "context" ? rest : args.slice(1);
  let format = "human";
  let change;
  for (let index = 0; index < flags.length; index += 1) {
    if (flags[index] === "--format" && flags[index + 1]) format = flags[++index];
    else if (flags[index] === "--change" && flags[index + 1]) change = flags[++index];
    else return { error: `Unknown or incomplete lifecycle argument ${flags[index]}` };
  }
  if (!operation || !["status", "context", "validate"].includes(operation)) return { error: `Unknown lifecycle operation ${String(operation)}` };
  if (operation === "context" && (!positional[0] || positional[0].startsWith("--"))) return { error: "context requires a stage" };
  if (!new Set(["human", "json"]).has(format)) return { error: `Unknown format ${format}` };
  return { operation, stage: positional[0], format, change };
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

function errorResult(operation, error, status = "error") {
  return baseResult(operation ?? null, { status, blockers: [error], errors: [error] });
}

function resultExitCode(result) {
  const code = result.errors[0]?.code;
  if (result.status === "success") return 0;
  if (["RL_INVALID_REQUEST", "RL_UNSUPPORTED_SCHEMA", "RL_INCOMPATIBLE_VERSION"].includes(code)) return 4;
  if (code === "RL_STALE_OPERATION") return 5;
  if (code === "RL_CHANGE_NOT_FOUND" || code === "RL_AMBIGUOUS_CHANGE" || code === "RL_OPERATION_NOT_PERMITTED") return 2;
  return 3;
}

function human(result) {
  const lines = [`RigorLoop lifecycle ${result.operation ?? "request"}: ${result.status}`];
  if (result.change_id) lines.push(`Change: ${result.change_id}`);
  if (result.lifecycle_revision) lines.push(`Lifecycle revision: ${result.lifecycle_revision}`);
  if (result.effective_state?.effective_state) lines.push(`Effective state: ${result.effective_state.effective_state}`);
  for (const blocker of result.blockers) lines.push(`${blocker.code}: ${blocker.summary}`);
  if (result.permitted_operations.length) lines.push(`Permitted operations: ${result.permitted_operations.join(", ")}`);
  return `${lines.join("\n")}\n`;
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
  const result = baseResult(parsed.operation, {
    status: interpreted.errors.length ? "error" : interpreted.blockers.length ? "blocked" : "success",
    change_id: interpreted.change_id,
    lifecycle_revision: interpreted.lifecycle_revision,
    effective_state: interpreted.effective_state,
    blockers: interpreted.blockers,
    permitted_operations: interpreted.permitted_operations,
    artifacts: interpreted.artifacts,
    warnings: interpreted.warnings,
    errors: interpreted.errors,
    ...(parsed.operation === "context" ? { context: contextForStage(interpreted, parsed.stage) } : {}),
    ...(parsed.operation === "validate" ? { validation: { valid: interpreted.errors.length === 0, checks: ["schema", "artifacts", "evidence", "findings", "milestones"] } } : {}),
  });
  for (const field of RESULT_FIELDS) if (!(field in result)) throw new Error(`missing lifecycle result field ${field}`);
  return { result, exitCode: resultExitCode(result), format: parsed.format, human: human(result) };
}

export function runLifecycleCli(args, options = {}) {
  const execution = executeLifecycleCli(args, options);
  if (execution.format === "json") process.stdout.write(`${JSON.stringify(execution.result, null, 2)}\n`);
  else (execution.exitCode === 0 ? process.stdout : process.stderr).write(execution.human);
  return execution.exitCode;
}
