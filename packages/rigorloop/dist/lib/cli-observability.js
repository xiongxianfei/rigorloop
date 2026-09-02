import { performance } from "node:perf_hooks";

import { buildDiagnosticEvent, createInvocationId, encodedEvent, LIFECYCLE_OPERATIONS } from "./diagnostic-event.js";
import { resolveLogConfig } from "./log-config.js";
import { appendDiagnosticEvent } from "./log-sink.js";

const LEVEL = { debug: 10, info: 20, warning: 30, error: 40, off: Infinity };
const TERMINAL_SEVERITY = Object.freeze({
  success: "info",
  "diagnostic-warning": "warning",
  "expected-rejection": "warning",
  "internal-error": "error",
  "unsafe-recovery": "error",
  "logging-failure": "error",
});

export function classifyCommand(args) {
  const command = args[0];
  if (command === "lifecycle") return { family: "lifecycle", command: "lifecycle", operation: LIFECYCLE_OPERATIONS.includes(args[1]) ? args[1] : "unknown" };
  if (["init", "new-change"].includes(command)) return { family: "repository-setup", command };
  if (["version", "workflow-context", "--help", "-h"].includes(command) || !command) return { family: "introspection", command: command || "help" };
  if (command === "logs") return { family: "log-inspection", command: "logs", operation: args[1] };
  return { family: "invalid-input", command: "unknown" };
}

function defaultTerminalClass(exitCode) {
  if (exitCode === 0) return "success";
  if ([2, 3, 4, 5].includes(exitCode)) return "expected-rejection";
  return "internal-error";
}

function completionSeverity(exitCode, requestedClass) {
  const terminalClass = requestedClass ?? defaultTerminalClass(exitCode);
  return TERMINAL_SEVERITY[terminalClass] ?? "error";
}

export async function runObservedCli(args, dispatch, options = {}) {
  const writeStdout = options.writeStdout ?? ((value) => process.stdout.write(value));
  const writeStderr = options.writeStderr ?? ((value) => process.stderr.write(value));
  const writeDiagnostic = (value) => {
    try { writeStderr(value); }
    catch { /* diagnostic output cannot change semantic execution */ }
  };
  const appendEvent = options.appendEvent ?? appendDiagnosticEvent;
  let config;
  try { config = resolveLogConfig(args, options); }
  catch (error) {
    writeDiagnostic(`${error.code ?? "RL_INVALID_LOG_LEVEL"}: logging configuration rejected\n`);
    return 4;
  }
  const identity = classifyCommand(config.args);
  let invocationId;
  try { invocationId = createInvocationId(options.entropy); }
  catch {
    try { invocationId = createInvocationId(); }
    catch { invocationId = null; }
  }
  const monotonic = options.monotonic ?? (() => performance.now());
  let started;
  try { started = monotonic(); }
  catch { started = null; }
  let observability = config.issue ? "degraded" : config.fileEnabled ? "recorded" : "disabled";
  let fallbackWritten = false;
  const fallback = () => {
    observability = "degraded";
    if (!fallbackWritten && config.consoleLevel !== "off") {
      fallbackWritten = true;
      writeDiagnostic(`RL_LOG_UNAVAILABLE: local CLI logging is unavailable; invocation=${invocationId ?? "unavailable"}\n`);
    }
  };
  if (config.issue || !invocationId || started === null) fallback();
  const write = (build) => {
    if (!config.fileEnabled) return;
    try {
      const event = build();
      if (LEVEL[event.severity] < LEVEL[config.fileLevel]) return;
      appendEvent(config.directory, encodedEvent(event), options);
    }
    catch { fallback(); }
  };
  write(() => buildDiagnosticEvent({
    event: "invocation-start", invocation_id: invocationId, severity: "info", command_family: identity.family,
    command: identity.command, cli_version: options.cliVersion, sequence: 1,
    ...(identity.family === "lifecycle" ? { operation: identity.operation } : {}),
  }, options));
  let exitCode = 1;
  let execution;
  try {
    execution = await dispatch(config.args, {
      invocationId,
      getObservability: () => observability,
      logDirectory: config.directory,
      loggingIssue: config.issue,
    });
    exitCode = typeof execution === "number" ? execution : execution.exitCode;
  }
  catch { exitCode = 1; }
  const severity = completionSeverity(exitCode, execution && typeof execution === "object" ? execution.terminalClass : undefined);
  let complete;
  write(() => {
    let duration;
    try { duration = started === null ? 0 : Math.max(0, Math.round(monotonic() - started)); }
    catch { throw Object.assign(new Error("Monotonic clock unavailable."), { code: "RL_LOG_UNAVAILABLE" }); }
    complete = buildDiagnosticEvent({
      event: "invocation-complete", invocation_id: invocationId, severity, command_family: identity.family,
      command: identity.command, cli_version: options.cliVersion, sequence: 2,
      status: exitCode === 0 ? "success" : exitCode === 2 ? "blocked" : "error", exit_code: exitCode,
      duration_ms: duration,
      ...(identity.family === "lifecycle" ? { operation: identity.operation } : {}),
    }, options);
    return complete;
  });
  if (execution && typeof execution === "object" && typeof execution.render === "function") {
    const rendered = execution.render({ invocationId, observability, exitCode });
    if (rendered.stdout) writeStdout(rendered.stdout);
    if (rendered.stderr) writeStderr(rendered.stderr);
  }
  if (LEVEL[severity] >= LEVEL[config.consoleLevel] && !fallbackWritten) {
    const code = severity === "error" ? "RL_CLI_INTERNAL" : "RL_CLI_EVENT";
    writeDiagnostic(`${code}: ${identity.command} ${complete?.status ?? "error"}; invocation=${invocationId ?? "unavailable"}\n`);
  }
  return exitCode;
}
