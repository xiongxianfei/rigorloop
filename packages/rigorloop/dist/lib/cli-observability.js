import { performance } from "node:perf_hooks";

import { buildDiagnosticEvent, createInvocationId, encodedEvent } from "./diagnostic-event.js";
import { resolveLogConfig } from "./log-config.js";
import { appendDiagnosticEvent } from "./log-sink.js";

const LEVEL = { debug: 10, info: 20, warning: 30, error: 40, off: Infinity };

export function classifyCommand(args) {
  const command = args[0];
  if (command === "lifecycle") return { family: "lifecycle", command: "lifecycle", operation: args[1] };
  if (["init", "new-change"].includes(command)) return { family: "repository-setup", command };
  if (["version", "--help", "-h"].includes(command) || !command) return { family: "introspection", command: command || "help" };
  if (command === "logs") return { family: "log-inspection", command: "logs", operation: args[1] };
  return { family: "invalid-input", command: "unknown" };
}

function completionSeverity(exitCode) {
  if (exitCode === 0) return "info";
  if ([2, 3, 4, 5].includes(exitCode)) return "warning";
  return "error";
}

export async function runObservedCli(args, dispatch, options = {}) {
  let config;
  try { config = resolveLogConfig(args, options); }
  catch (error) {
    process.stderr.write(`${error.code ?? "RL_INVALID_LOG_LEVEL"}: logging configuration rejected\n`);
    return 4;
  }
  const identity = classifyCommand(config.args);
  const invocationId = createInvocationId(options.entropy);
  const started = performance.now();
  let observability = config.fileEnabled ? "recorded" : "disabled";
  let fallbackWritten = false;
  const fallback = () => {
    observability = "degraded";
    if (!fallbackWritten && config.consoleLevel !== "off") {
      fallbackWritten = true;
      process.stderr.write(`RL_LOG_UNAVAILABLE: local CLI logging is unavailable; invocation=${invocationId}\n`);
    }
  };
  const write = (event) => {
    if (!config.fileEnabled) return;
    if (LEVEL[event.severity] < LEVEL[config.fileLevel]) return;
    try { appendDiagnosticEvent(config.directory, encodedEvent(event), options); }
    catch { fallback(); }
  };
  write(buildDiagnosticEvent({
    event: "invocation-start", invocation_id: invocationId, severity: "info", command_family: identity.family,
    command: identity.command, cli_version: options.cliVersion, sequence: 1,
    ...(identity.family === "lifecycle" ? { operation: identity.operation } : {}),
  }, options));
  let exitCode = 1;
  try { exitCode = await dispatch(config.args, { invocationId, getObservability: () => observability, logDirectory: config.directory }); }
  catch { exitCode = 1; }
  const severity = completionSeverity(exitCode);
  const complete = buildDiagnosticEvent({
    event: "invocation-complete", invocation_id: invocationId, severity, command_family: identity.family,
    command: identity.command, cli_version: options.cliVersion, sequence: 2,
    status: exitCode === 0 ? "success" : exitCode === 2 ? "blocked" : "error", exit_code: exitCode,
    duration_ms: Math.max(0, Math.round(performance.now() - started)),
    ...(identity.family === "lifecycle" ? { operation: identity.operation } : {}),
  }, options);
  write(complete);
  if (LEVEL[severity] >= LEVEL[config.consoleLevel] && !fallbackWritten) {
    const code = severity === "error" ? "RL_CLI_INTERNAL" : "RL_CLI_EVENT";
    process.stderr.write(`${code}: ${identity.command} ${complete.status}; invocation=${invocationId}\n`);
  }
  return exitCode;
}
