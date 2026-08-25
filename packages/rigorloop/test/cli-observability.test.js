import assert from "node:assert/strict";
import { chmodSync, mkdtempSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { buildDiagnosticEvent, createInvocationId, encodedEvent } from "../dist/lib/diagnostic-event.js";
import { resolveLogConfig } from "../dist/lib/log-config.js";
import { appendDiagnosticEvent, MAX_LOG_BYTES } from "../dist/lib/log-sink.js";

function root() { return mkdtempSync(join(tmpdir(), "rigorloop-observability-")); }

test("logging configuration is strict and CLI flags override environment", () => {
  const directory = root();
  assert.deepEqual(resolveLogConfig(["version", "--file-log-level", "debug", "--console-log-level", "off", "--no-file-log"], {
    env: { RIGORLOOP_LOG_DIR: directory, RIGORLOOP_FILE_LOG_LEVEL: "error" }, home: directory,
  }), { fileLevel: "debug", consoleLevel: "off", fileEnabled: false, directory, args: ["version"] });
  assert.throws(() => resolveLogConfig([], { env: { RIGORLOOP_FILE_LOG_LEVEL: "trace" } }), (error) => error.code === "RL_INVALID_LOG_LEVEL");
  assert.throws(() => resolveLogConfig([], { env: { RIGORLOOP_LOG_DIR: "relative" } }), (error) => error.code === "RL_LOG_UNSAFE_PATH");
});

test("events are bounded, normalized, and lifecycle-only extensions do not escape", () => {
  const id = createInvocationId();
  assert.match(id, /^[0-9a-f]{16}$/);
  const event = buildDiagnosticEvent({ schema_version: 99, event: "invocation-complete", invocation_id: id, severity: "warning", command_family: "lifecycle", command: "lifecycle", cli_version: "0.4.1", sequence: 2, status: "blocked", exit_code: 2, duration_ms: 1, operation: "status\nunsafe", secret: "do-not-write" });
  assert.equal(event.schema_version, 1);
  assert.equal(event.operation, "status unsafe");
  assert.equal("secret" in event, false);
  const other = buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1, change_id: "secret" });
  assert.equal("change_id" in other, false);
});

test("sink writes complete JSONL and rotates inside its root", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const id = createInvocationId();
  const event = buildDiagnosticEvent({ event: "invocation-start", invocation_id: id, severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 });
  appendDiagnosticEvent(directory, encodedEvent(event));
  writeFileSync(join(directory, "rigorloop.jsonl"), "x".repeat(MAX_LOG_BYTES), { mode: 0o600 });
  appendDiagnosticEvent(directory, encodedEvent(event));
  assert.equal(statSync(join(directory, "rigorloop.1.jsonl")).size, MAX_LOG_BYTES);
  assert.equal(JSON.parse(readFileSync(join(directory, "rigorloop.jsonl"), "utf8")).invocation_id, id);
});
