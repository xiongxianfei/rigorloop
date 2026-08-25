export const RESULT_FORMATS = Object.freeze(["human", "json", "concise-human", "concise-json", "detailed-json"]);

const OBSERVABILITY_STATES = new Set(["recorded", "degraded", "disabled"]);
const CONCISE_FIELDS = new Set([
  "schema_version", "projection", "invocation_id", "command", "operation", "status", "exit_code",
  "change_id", "lifecycle_revision", "state_changed", "next_operation", "codes", "finding_ids",
  "milestone_ids", "observability",
]);

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function diagnosticValues(result) {
  return [...(result.blockers ?? []), ...(result.warnings ?? []), ...(result.errors ?? [])];
}

function relevantIdentities(result) {
  return diagnosticValues(result).flatMap((item) => item.relevant_identities ?? []);
}

function omitEmpty(value) {
  return Object.fromEntries(Object.entries(value).filter(([, item]) => item !== null && item !== undefined && item !== "" && (!Array.isArray(item) || item.length > 0)));
}

export function projectConciseResult(result, options = {}) {
  const observability = options.observability ?? "disabled";
  if (!OBSERVABILITY_STATES.has(observability)) throw new Error(`Unknown observability state ${observability}`);
  const diagnostics = diagnosticValues(result);
  const identities = relevantIdentities(result);
  const nextOperation = result.next_operation ?? diagnostics.find((item) => item.corrective_operation)?.corrective_operation ?? result.permitted_operations?.[0] ?? null;
  const projected = omitEmpty({
    schema_version: 2,
    projection: "concise",
    invocation_id: options.invocationId ?? result.invocation_id ?? null,
    command: result.command ?? null,
    operation: result.operation ?? null,
    status: result.status ?? "error",
    exit_code: options.exitCode ?? result.exit_code ?? null,
    change_id: result.change_id ?? null,
    lifecycle_revision: result.lifecycle_revision ?? null,
    state_changed: result.state_changed ?? (result.mutation ? !["unchanged", "dry-run"].includes(result.mutation.status) : null),
    next_operation: nextOperation,
    codes: unique(diagnostics.map((item) => item.code)),
    finding_ids: unique([...(result.finding_ids ?? []), ...identities.filter((item) => /^F(?:-|\d)/i.test(String(item)))]),
    milestone_ids: unique([...(result.milestone_ids ?? []), result.effective_state?.active_milestone, ...identities.filter((item) => /^M\d+$/i.test(String(item)))]),
    observability,
  });
  for (const field of Object.keys(projected)) {
    if (!CONCISE_FIELDS.has(field)) throw new Error(`Unsupported concise result field ${field}`);
  }
  return projected;
}

function conciseHuman(result, options) {
  const projected = projectConciseResult(result, options);
  const identity = projected.change_id ?? projected.milestone_ids?.[0] ?? "-";
  const name = projected.operation ?? projected.command ?? "command";
  const details = [projected.codes?.[0], projected.next_operation ? `next=${projected.next_operation}` : null, `invocation=${projected.invocation_id ?? "unavailable"}`].filter(Boolean);
  return `${name} ${projected.status} (${identity})${details.length ? `: ${details.join("; ")}` : ""}\n`;
}

export function renderResult(result, options = {}) {
  const format = options.format ?? "human";
  if (!RESULT_FORMATS.includes(format)) throw new Error(`Unknown result format ${format}`);
  if (format === "concise-json") return `${JSON.stringify(projectConciseResult(result, options))}\n`;
  if (format === "concise-human") return conciseHuman(result, options);
  if (format === "json" || format === "detailed-json") return `${JSON.stringify(result, null, 2)}\n`;
  if (typeof options.human === "function") return options.human(result);
  return `${result.summary ?? `${result.command ?? "command"}: ${result.status ?? "error"}`}\n`;
}
