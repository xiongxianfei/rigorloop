import { readRetainedLogs } from "./log-sink.js";

export function findInvocationEvents(directory, invocationId) {
  if (!/^[0-9a-f]{16}$/.test(invocationId)) return { status: "error", code: "RL_INVALID_INVOCATION_ID", events: [], warnings: [] };
  const events = [];
  const warnings = [];
  try {
    for (const file of readRetainedLogs(directory)) {
      for (const line of file.content.split("\n").filter(Boolean)) {
        try {
          const event = JSON.parse(line);
          if (event.schema_version !== 1) { warnings.push({ code: "RL_LOG_UNAVAILABLE" }); continue; }
          if (event.invocation_id === invocationId) events.push(event);
        } catch { warnings.push({ code: "RL_LOG_CORRUPT_ENTRY" }); }
      }
    }
  } catch (error) { return { status: "error", code: error.code === "RL_LOG_UNSAFE_PATH" ? error.code : "RL_LOG_UNAVAILABLE", events: [], warnings: [] }; }
  if (!events.length) return { status: "error", code: "RL_LOG_NOT_FOUND", events: [], warnings };
  return { status: warnings.length ? "warning" : "success", events, warnings };
}
