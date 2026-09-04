import { randomBytes } from "node:crypto";

export const COMMAND_FAMILIES = Object.freeze(["lifecycle", "compact", "repository-setup", "introspection", "log-inspection", "invalid-input"]);
export const EVENT_SEVERITIES = Object.freeze(["debug", "info", "warning", "error"]);
export const LIFECYCLE_OPERATIONS = Object.freeze(["status", "context", "validate", "record-artifact-revision", "record-review", "record-validation", "record-finding-resolution", "settle-artifact", "record-package-review", "settle-review-package", "advance-stage", "initialize-approved-plan", "start-milestone", "complete-milestone", "record-final-review", "route-correction", "return-correction", "withdraw-artifact-registration", "migrate", "repair", "unknown"]);
const EVENT_KINDS = Object.freeze(["invocation-start", "invocation-complete"]);
const EVENT_SEQUENCES = Object.freeze({ "invocation-start": 1, "invocation-complete": 2 });
const COMPLETION_STATUSES = Object.freeze(["success", "blocked", "error"]);
const COMMON = ["schema_version", "event", "timestamp", "invocation_id", "severity", "command_family", "command", "cli_version", "sequence"];
const COMPLETE = ["status", "exit_code", "duration_ms"];
const LIFECYCLE = ["operation", "change_id", "stage", "prior_lifecycle_revision", "resulting_lifecycle_revision", "state_changed", "codes", "finding_ids", "milestone_ids"];
const STRING_FIELDS = new Set(["command", "cli_version", "operation", "change_id", "stage"]);
const STRING_LIST_FIELDS = new Set(["codes", "finding_ids", "milestone_ids"]);
const INTEGER_FIELDS = new Set(["sequence", "exit_code", "duration_ms", "prior_lifecycle_revision", "resulting_lifecycle_revision"]);
const MAX_EVENT_BYTES = 16 * 1024;

export function createInvocationId(entropy = randomBytes) {
  const value = entropy(8);
  if (!Buffer.isBuffer(value) || value.length !== 8) throw new Error("Invalid invocation ID entropy");
  return value.toString("hex");
}

export function isInvocationId(value) {
  return typeof value === "string" && /^[0-9a-f]{16}$/.test(value);
}

function safeString(value) {
  return value.replace(/[\u0000-\u001f\u007f]/g, " ");
}

function invalid(key) {
  throw new Error(`Invalid diagnostic field ${key}`);
}

function clockUnavailable() {
  return Object.assign(new Error("Diagnostic clock unavailable"), { code: "RL_LOG_UNAVAILABLE" });
}

function safeValue(key, value) {
  if (STRING_FIELDS.has(key)) {
    if (typeof value !== "string") invalid(key);
    return safeString(value);
  }
  if (STRING_LIST_FIELDS.has(key)) {
    if (!Array.isArray(value) || value.some((item) => typeof item !== "string")) invalid(key);
    return value.map(safeString);
  }
  if (INTEGER_FIELDS.has(key)) {
    if (!Number.isSafeInteger(value) || value < 0 || (key === "sequence" && value === 0)) invalid(key);
    return value;
  }
  if (key === "state_changed") {
    if (typeof value !== "boolean") invalid(key);
    return value;
  }
  if (key === "status") {
    if (!COMPLETION_STATUSES.includes(value)) invalid(key);
    return value;
  }
  return value;
}

function timestamp(now) {
  let value;
  try { value = now?.() ?? new Date(); }
  catch { throw clockUnavailable(); }
  if (!(value instanceof Date) || !Number.isFinite(value.getTime())) throw clockUnavailable();
  try { return Date.prototype.toISOString.call(value); }
  catch { throw clockUnavailable(); }
}

function requireInput(input, keys) {
  for (const key of keys) {
    if (input[key] === undefined || input[key] === null) throw new Error(`Missing diagnostic field ${key}`);
  }
}

function oversizedFallback(event) {
  const fallback = {
    schema_version: 1,
    event: event.event,
    timestamp: event.timestamp,
    invocation_id: event.invocation_id,
    severity: "error",
    command_family: event.command_family,
    command: "diagnostic",
    cli_version: "unknown",
    sequence: event.sequence,
  };
  if (event.event === "invocation-complete") {
    Object.assign(fallback, { status: "error", exit_code: 1, duration_ms: 0 });
  }
  if (event.command_family === "lifecycle") fallback.codes = ["RL_LOG_EVENT_TOO_LARGE"];
  return fallback;
}

export function buildDiagnosticEvent(input, options = {}) {
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new Error("Invalid diagnostic input");
  if (!COMMAND_FAMILIES.includes(input.command_family)) throw new Error("Unknown command family");
  if (!EVENT_SEVERITIES.includes(input.severity)) throw new Error("Unknown event severity");
  if (!isInvocationId(input.invocation_id)) throw new Error("Invalid invocation ID");
  if (!EVENT_KINDS.includes(input.event)) throw new Error("Unknown diagnostic event");
  if (input.sequence !== EVENT_SEQUENCES[input.event]) invalid("sequence");
  if (input.command_family === "lifecycle" && input.operation !== undefined && !LIFECYCLE_OPERATIONS.includes(input.operation)) invalid("operation");
  const required = ["command", "cli_version", "sequence", ...(input.event === "invocation-complete" ? COMPLETE : [])];
  requireInput(input, required);
  const allowed = new Set([...COMMON, ...(input.event === "invocation-complete" ? COMPLETE : []), ...(input.command_family === "lifecycle" ? LIFECYCLE : [])]);
  const event = {};
  for (const key of allowed) {
    if (input[key] === undefined || input[key] === null || (Array.isArray(input[key]) && input[key].length === 0)) continue;
    event[key] = safeValue(key, input[key]);
  }
  event.schema_version = 1;
  event.timestamp = timestamp(options.now);
  return Buffer.byteLength(JSON.stringify(event)) + 1 <= MAX_EVENT_BYTES ? event : oversizedFallback(event);
}

export function validateDiagnosticEvent(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new Error("Invalid diagnostic event");
  if (input.schema_version !== 1) throw new Error("Unsupported diagnostic schema");
  if (!EVENT_KINDS.includes(input.event)) throw new Error("Unknown diagnostic event");
  if (!EVENT_SEVERITIES.includes(input.severity)) throw new Error("Unknown event severity");
  if (!COMMAND_FAMILIES.includes(input.command_family)) throw new Error("Unknown command family");
  if (!isInvocationId(input.invocation_id)) throw new Error("Invalid invocation ID");
  if (input.sequence !== EVENT_SEQUENCES[input.event]) invalid("sequence");
  if (
    typeof input.timestamp !== "string"
    || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(input.timestamp)
    || new Date(input.timestamp).toISOString() !== input.timestamp
  ) invalid("timestamp");
  if (input.command_family === "lifecycle" && input.operation !== undefined && !LIFECYCLE_OPERATIONS.includes(input.operation)) invalid("operation");
  const required = [...COMMON, ...(input.event === "invocation-complete" ? COMPLETE : [])];
  requireInput(input, required);
  const allowed = new Set([...COMMON, ...(input.event === "invocation-complete" ? COMPLETE : []), ...(input.command_family === "lifecycle" ? LIFECYCLE : [])]);
  for (const key of Object.keys(input)) if (!allowed.has(key)) invalid(key);
  for (const [key, value] of Object.entries(input)) {
    if (value === null || value === undefined || (Array.isArray(value) && value.length === 0)) invalid(key);
    const normalized = safeValue(key, value);
    if (JSON.stringify(normalized) !== JSON.stringify(value)) invalid(key);
  }
  if (Buffer.byteLength(JSON.stringify(input)) + 1 > MAX_EVENT_BYTES) throw new Error("Diagnostic event too large");
  return input;
}

export function encodedEvent(event) {
  return `${JSON.stringify(event)}\n`;
}
