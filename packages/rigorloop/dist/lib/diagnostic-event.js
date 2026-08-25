import { randomBytes } from "node:crypto";

export const COMMAND_FAMILIES = Object.freeze(["lifecycle", "repository-setup", "introspection", "log-inspection", "invalid-input"]);
export const EVENT_SEVERITIES = Object.freeze(["debug", "info", "warning", "error"]);
const COMMON = ["schema_version", "event", "timestamp", "invocation_id", "severity", "command_family", "command", "cli_version", "sequence"];
const COMPLETE = ["status", "exit_code", "duration_ms"];
const LIFECYCLE = ["operation", "change_id", "stage", "prior_lifecycle_revision", "resulting_lifecycle_revision", "state_changed", "codes", "finding_ids", "milestone_ids"];
const MAX_EVENT_BYTES = 16 * 1024;

export function createInvocationId(entropy = randomBytes) {
  return entropy(8).toString("hex");
}

function safeString(value) {
  return String(value).replace(/[\u0000-\u001f\u007f]/g, " ");
}

export function buildDiagnosticEvent(input, options = {}) {
  if (!COMMAND_FAMILIES.includes(input.command_family)) throw new Error("Unknown command family");
  if (!EVENT_SEVERITIES.includes(input.severity)) throw new Error("Unknown event severity");
  if (!/^[0-9a-f]{16}$/.test(input.invocation_id)) throw new Error("Invalid invocation ID");
  if (!new Set(["invocation-start", "invocation-complete"]).has(input.event)) throw new Error("Unknown diagnostic event");
  const allowed = new Set([...COMMON, ...(input.event === "invocation-complete" ? COMPLETE : []), ...(input.command_family === "lifecycle" ? LIFECYCLE : [])]);
  const event = {};
  for (const key of allowed) {
    if (input[key] === undefined || input[key] === null || (Array.isArray(input[key]) && input[key].length === 0)) continue;
    event[key] = typeof input[key] === "string" ? safeString(input[key]) : input[key];
  }
  event.schema_version = 1;
  event.timestamp = (options.now?.() ?? new Date()).toISOString();
  const encoded = JSON.stringify(event);
  if (Buffer.byteLength(encoded) <= MAX_EVENT_BYTES) return event;
  return {
    schema_version: 1, event: input.event, timestamp: event.timestamp, invocation_id: input.invocation_id,
    severity: "error", command_family: input.command_family, command: input.command, cli_version: input.cli_version,
    sequence: input.sequence, ...(input.event === "invocation-complete" ? { status: input.status ?? "error", exit_code: input.exit_code ?? 1, duration_ms: input.duration_ms ?? 0 } : {}),
    codes: input.command_family === "lifecycle" ? ["RL_LOG_EVENT_TOO_LARGE"] : undefined,
  };
}

export function encodedEvent(event) {
  return `${JSON.stringify(event)}\n`;
}
