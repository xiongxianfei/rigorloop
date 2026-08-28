import { readRetainedLogs } from "./log-sink.js";
import { isInvocationId, validateDiagnosticEvent } from "./diagnostic-event.js";

export function findInvocationEvents(directory, invocationId) {
  if (!isInvocationId(invocationId)) return { status: "error", code: "RL_INVALID_INVOCATION_ID", events: [], warnings: [] };
  const events = [];
  const warnings = [];
  let relatedCorrupt = false;
  try {
    for (const file of readRetainedLogs(directory)) {
      for (const line of file.content.split("\n").filter(Boolean)) {
        try {
          const candidate = JSON.parse(line);
          if (candidate.schema_version !== 1) { warnings.push({ code: "RL_LOG_UNAVAILABLE" }); continue; }
          let event;
          try { event = validateDiagnosticEvent(candidate); }
          catch {
            if (candidate.invocation_id === invocationId) relatedCorrupt = true;
            else warnings.push({ code: "RL_LOG_CORRUPT_ENTRY" });
            continue;
          }
          if (event.invocation_id === invocationId) events.push(event);
        } catch { warnings.push({ code: "RL_LOG_CORRUPT_ENTRY" }); }
      }
    }
  } catch (error) { return { status: "error", code: error.code === "RL_LOG_UNSAFE_PATH" ? error.code : "RL_LOG_UNAVAILABLE", events: [], warnings: [] }; }
  if (relatedCorrupt) return { status: "error", code: "RL_LOG_CORRUPT_ENTRY", events: [], warnings };
  if (!events.length) return { status: "error", code: "RL_LOG_NOT_FOUND", events: [], warnings };
  return { status: warnings.length ? "warning" : "success", events, warnings };
}
