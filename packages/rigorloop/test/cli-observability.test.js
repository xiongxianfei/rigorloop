import assert from "node:assert/strict";
import { chmodSync, closeSync, existsSync, fstatSync, lstatSync, mkdtempSync, openSync, readFileSync, renameSync, statSync, symlinkSync, unlinkSync, writeFileSync, writeSync } from "node:fs";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { buildDiagnosticEvent, createInvocationId, encodedEvent, validateDiagnosticEvent } from "../dist/lib/diagnostic-event.js";
import { defaultLogDirectory, resolveLogConfig } from "../dist/lib/log-config.js";
import { appendDiagnosticEvent, LOG_NAMES, MAX_LOG_BYTES } from "../dist/lib/log-sink.js";

function root() { return mkdtempSync(join(tmpdir(), "rigorloop-observability-")); }

function jsonLineOfSize(bytes) {
  const empty = `${JSON.stringify({ pad: "" })}\n`;
  const line = `${JSON.stringify({ pad: "x".repeat(bytes - Buffer.byteLength(empty)) })}\n`;
  assert.equal(Buffer.byteLength(line), bytes);
  return line;
}

test("logging configuration is strict and CLI flags override environment", () => {
  const directory = root();
  assert.deepEqual(resolveLogConfig(["version", "--file-log-level", "debug", "--console-log-level", "off", "--no-file-log"], {
    env: { RIGORLOOP_LOG_DIR: directory, RIGORLOOP_FILE_LOG_LEVEL: "error" }, home: directory,
  }), { fileLevel: "debug", consoleLevel: "off", fileEnabled: false, directory, args: ["version"], issue: null });
  assert.throws(() => resolveLogConfig([], { env: { RIGORLOOP_FILE_LOG_LEVEL: "trace" } }), (error) => error.code === "RL_INVALID_LOG_LEVEL");
  assert.equal(resolveLogConfig([], { env: { RIGORLOOP_LOG_DIR: "relative" } }).issue.code, "RL_LOG_UNSAFE_PATH");
});

test("platform defaults, symlink refusal, permissions, and lock exhaustion are bounded", () => {
  assert.equal(defaultLogDirectory({ platform: "linux", env: { XDG_STATE_HOME: "/state" }, home: "/home/example" }), "/state/rigorloop/logs");
  assert.equal(defaultLogDirectory({ platform: "linux", env: { XDG_STATE_HOME: "relative" }, home: "/home/example" }), "/home/example/.local/state/rigorloop/logs");
  assert.equal(defaultLogDirectory({ platform: "darwin", env: {}, home: "/home/example" }), "/home/example/Library/Logs/RigorLoop");
  assert.equal(defaultLogDirectory({ platform: "win32", env: { LOCALAPPDATA: "C:\\State" }, home: "C:\\Users\\example" }), "C:\\State\\RigorLoop\\Logs");
  assert.equal(defaultLogDirectory({ platform: "win32", env: { LOCALAPPDATA: "relative" }, home: "C:\\Users\\example" }), "C:\\Users\\example\\AppData\\Local\\RigorLoop\\Logs");

  const broad = root();
  chmodSync(broad, 0o755);
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  assert.throws(() => appendDiagnosticEvent(broad, event), (error) => error.code === "RL_LOG_UNSAFE_PATH");
  assert.equal(statSync(broad).mode & 0o777, 0o755);

  const parent = root();
  const target = root();
  const linked = join(parent, "linked");
  symlinkSync(target, linked, "dir");
  assert.throws(() => appendDiagnosticEvent(linked, event), (error) => error.code === "RL_LOG_UNSAFE_PATH");

  const locked = root();
  chmodSync(locked, 0o700);
  writeFileSync(join(locked, ".rigorloop-log.lock"), "owned elsewhere", { mode: 0o600 });
  assert.throws(() => appendDiagnosticEvent(locked, event, { wait: false }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.equal(readFileSync(join(locked, ".rigorloop-log.lock"), "utf8"), "owned elsewhere");
});

test("events are bounded, normalized, and lifecycle-only extensions do not escape", () => {
  const id = createInvocationId();
  assert.match(id, /^[0-9a-f]{16}$/);
  const event = buildDiagnosticEvent({ schema_version: 99, event: "invocation-complete", invocation_id: id, severity: "warning", command_family: "lifecycle", command: "lifecycle", cli_version: "0.4.1", sequence: 2, status: "blocked", exit_code: 2, duration_ms: 1, operation: "status", change_id: "change\nunsafe", secret: "do-not-write" });
  assert.equal(event.schema_version, 1);
  assert.equal(event.operation, "status");
  assert.equal(event.change_id, "change unsafe");
  assert.equal("secret" in event, false);
  const other = buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1, change_id: "secret" });
  assert.equal("change_id" in other, false);
  assert.equal(JSON.stringify(event).includes("do-not-write"), false);
  const withLists = buildDiagnosticEvent({
    event: "invocation-complete", invocation_id: createInvocationId(), severity: "warning",
    command_family: "lifecycle", command: "lifecycle", cli_version: "0.4.1", sequence: 2,
    status: "blocked", exit_code: 2, duration_ms: 1,
    codes: ["RL_ONE\nINJECTED"], finding_ids: ["F-1\u0000hidden"], milestone_ids: ["M1\u007fhidden"],
  });
  assert.deepEqual(withLists.codes, ["RL_ONE INJECTED"]);
  assert.deepEqual(withLists.finding_ids, ["F-1 hidden"]);
  assert.deepEqual(withLists.milestone_ids, ["M1 hidden"]);
  assert.throws(() => buildDiagnosticEvent({
    event: "invocation-complete", invocation_id: createInvocationId(), severity: "warning",
    command_family: "lifecycle", command: "lifecycle", cli_version: "0.4.1", sequence: 2,
    status: "blocked", exit_code: 2, duration_ms: 1, codes: [{ private: "value" }],
  }), /Invalid diagnostic field codes/);
});

test("CLIOBS-M3-R1-F1 read-side event validation rejects every non-canonical partition", () => {
  const valid = buildDiagnosticEvent({
    event: "invocation-complete",
    invocation_id: createInvocationId(),
    severity: "warning",
    command_family: "lifecycle",
    command: "lifecycle",
    cli_version: "0.4.1",
    sequence: 2,
    status: "blocked",
    exit_code: 2,
    duration_ms: 1,
    operation: "status",
  }, { now: () => new Date("2026-08-25T00:00:00.000Z") });
  assert.equal(validateDiagnosticEvent(valid), valid);
  for (const candidate of [
    { ...valid, schema_version: 2 },
    { ...valid, private: "M3_PRIVATE_SENTINEL" },
    Object.fromEntries(Object.entries(valid).filter(([key]) => key !== "command")),
    { ...valid, duration_ms: "1" },
    { ...valid, operation: "unknown-private-operation" },
    { ...valid, timestamp: "not-a-timestamp" },
    { ...valid, command_family: "introspection" },
  ]) assert.throws(() => validateDiagnosticEvent(candidate));
});

test("T02 event schemas reject unsafe scalar types and incomplete completion facts", () => {
  const base = {
    event: "invocation-complete", invocation_id: createInvocationId(), severity: "warning",
    command_family: "lifecycle", command: "lifecycle", cli_version: "0.4.1", sequence: 2,
    status: "blocked", exit_code: 2, duration_ms: 1,
  };
  for (const [field, value] of [
    ["operation", { private: "M2_PRIVATE_SENTINEL" }], ["state_changed", "true"],
    ["exit_code", "2"], ["duration_ms", -1], ["prior_lifecycle_revision", 1.5],
  ]) {
    assert.throws(() => buildDiagnosticEvent({ ...base, [field]: value }), /Invalid diagnostic/);
  }
  for (const field of ["status", "exit_code", "duration_ms"]) {
    const input = { ...base };
    delete input[field];
    assert.throws(() => buildDiagnosticEvent(input), /Missing diagnostic/);
  }
});

test("T02 event kind and sequence are one closed pair", () => {
  const base = {
    invocation_id: createInvocationId(), severity: "info", command_family: "introspection",
    command: "version", cli_version: "0.4.1",
  };
  assert.doesNotThrow(() => buildDiagnosticEvent({ ...base, event: "invocation-start", sequence: 1 }));
  assert.doesNotThrow(() => buildDiagnosticEvent({ ...base, event: "invocation-complete", sequence: 2, status: "success", exit_code: 0, duration_ms: 1 }));
  assert.throws(() => buildDiagnosticEvent({ ...base, event: "invocation-start", sequence: 2 }), /Invalid diagnostic field sequence/);
  assert.throws(() => buildDiagnosticEvent({ ...base, event: "invocation-complete", sequence: 1, status: "success", exit_code: 0, duration_ms: 1 }), /Invalid diagnostic field sequence/);
});

test("T02 invocation identity and every lifecycle extension have closed shapes", () => {
  assert.equal(createInvocationId(() => Buffer.from("0011223344556677", "hex")), "0011223344556677");
  assert.throws(() => createInvocationId(() => Buffer.from("short")), /Invalid invocation ID entropy/);
  const base = {
    event: "invocation-complete", invocation_id: createInvocationId(), severity: "warning",
    command_family: "lifecycle", command: "lifecycle", cli_version: "0.4.1", sequence: 2,
    status: "blocked", exit_code: 2, duration_ms: 1,
  };
  for (const field of ["command", "cli_version", "operation", "change_id", "stage"]) {
    assert.throws(() => buildDiagnosticEvent({ ...base, [field]: { private: "M2_PRIVATE_SENTINEL" } }), /Invalid diagnostic/);
  }
  assert.throws(() => buildDiagnosticEvent({ ...base, operation: "private-raw-operation" }), /Invalid diagnostic field operation/);
  for (const field of ["codes", "finding_ids", "milestone_ids"]) {
    assert.throws(() => buildDiagnosticEvent({ ...base, [field]: ["safe", { private: "M2_PRIVATE_SENTINEL" }] }), /Invalid diagnostic/);
  }
});

test("T02 wall-clock failure fails closed and oversized private input yields a bounded safe event", () => {
  const privateMarker = `M2_PRIVATE_SENTINEL_${"x".repeat(20 * 1024)}`;
  const input = {
    event: "invocation-complete", invocation_id: createInvocationId(), severity: "warning",
    command_family: "lifecycle", command: "lifecycle", cli_version: "0.4.1", sequence: 2,
    status: "blocked", exit_code: 2, duration_ms: 1, operation: "status", codes: [privateMarker],
  };
  assert.throws(() => buildDiagnosticEvent(input, { now: () => { throw new Error(privateMarker); } }), (error) => error.code === "RL_LOG_UNAVAILABLE" && !error.message.includes(privateMarker));
  const event = buildDiagnosticEvent(input, { now: () => new Date("2026-08-25T00:00:00.000Z") });
  const encoded = encodedEvent(event);
  assert.ok(Buffer.byteLength(encoded) <= 16 * 1024);
  assert.equal(encoded.includes("M2_PRIVATE_SENTINEL"), false);
  assert.match(event.timestamp, /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/);
});

test("T02 encoded event uses the exact 16 KiB boundary", () => {
  const now = () => new Date("2026-08-25T00:00:00.000Z");
  const base = {
    event: "invocation-start", invocation_id: createInvocationId(), severity: "info",
    command_family: "lifecycle", command: "lifecycle", cli_version: "0.4.1", sequence: 1,
  };
  const emptyBytes = Buffer.byteLength(encodedEvent(buildDiagnosticEvent({ ...base, codes: [""] }, { now })));
  const exact = buildDiagnosticEvent({ ...base, codes: ["x".repeat(16 * 1024 - emptyBytes)] }, { now });
  assert.equal(Buffer.byteLength(encodedEvent(exact)), 16 * 1024);
  const oversized = buildDiagnosticEvent({ ...base, codes: ["M2_PRIVATE_SENTINEL".repeat(1024)] }, { now });
  assert.ok(Buffer.byteLength(encodedEvent(oversized)) <= 16 * 1024);
  assert.equal(JSON.stringify(oversized).includes("M2_PRIVATE_SENTINEL"), false);
});

test("T03 prohibited caller values are absent from every admitted event surface", () => {
  const markers = [
    "credential-M2_PRIVATE", "argv-M2_PRIVATE", "request-M2_PRIVATE", "fingerprint-M2_PRIVATE",
    "https://private.example/repo.git", "username-M2_PRIVATE", "hostname-M2_PRIVATE",
    "/private/repository/M2_PRIVATE", "stack-M2_PRIVATE",
  ];
  const event = buildDiagnosticEvent({
    event: "invocation-complete", invocation_id: createInvocationId(), severity: "warning",
    command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 2,
    status: "blocked", exit_code: 2, duration_ms: 1,
    raw_argv: markers[0], request: markers[1], fingerprint: markers[2], remote_url: markers[3],
    username: markers[4], hostname: markers[5], repository_path: markers[6], stack: markers[7], secret: markers[8],
    operation: markers.join("|"), change_id: markers.join("|"), codes: markers,
  });
  const serialized = JSON.stringify(event);
  for (const marker of markers) assert.equal(serialized.includes(marker), false, marker);
  assert.deepEqual(Object.keys(event), ["event", "invocation_id", "severity", "command_family", "command", "cli_version", "sequence", "status", "exit_code", "duration_ms", "schema_version", "timestamp"]);

  const directory = root();
  chmodSync(directory, 0o700);
  const encoded = encodedEvent(event);
  appendDiagnosticEvent(directory, encoded);
  writeFileSync(join(directory, "rigorloop.jsonl"), `${encoded}${jsonLineOfSize(MAX_LOG_BYTES - Buffer.byteLength(encoded) + 1)}`, { mode: 0o600 });
  appendDiagnosticEvent(directory, encoded);
  const retainedFiles = LOG_NAMES.filter((name) => existsSync(join(directory, name))).map((name) => readFileSync(join(directory, name), "utf8"));
  const retained = retainedFiles.join("");
  for (const marker of markers) assert.equal(retained.includes(marker), false, marker);
  assert.doesNotThrow(() => retainedFiles.flatMap((content) => content.trim().split("\n")).forEach(JSON.parse));
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

test("T04 creates restrictive roots and files and refuses owned symlinks or broad files", () => {
  const parent = root();
  const absent = join(parent, "absent", "logs");
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  appendDiagnosticEvent(absent, event);
  assert.equal(statSync(absent).mode & 0o777, 0o700);
  assert.equal(statSync(join(absent, "rigorloop.jsonl")).mode & 0o777, 0o600);

  for (const ownedName of ["rigorloop.jsonl", ".rigorloop-log.lock"]) {
    const directory = root();
    chmodSync(directory, 0o700);
    const external = join(root(), "external");
    writeFileSync(external, "sentinel", { mode: 0o600 });
    symlinkSync(external, join(directory, ownedName));
    assert.throws(() => appendDiagnosticEvent(directory, event), (error) => error.code === "RL_LOG_UNSAFE_PATH");
    assert.equal(readFileSync(external, "utf8"), "sentinel");
  }

  const broadFileRoot = root();
  chmodSync(broadFileRoot, 0o700);
  writeFileSync(join(broadFileRoot, "rigorloop.jsonl"), "", { mode: 0o644 });
  assert.throws(() => appendDiagnosticEvent(broadFileRoot, event), (error) => error.code === "RL_LOG_UNSAFE_PATH");
  assert.equal(statSync(join(broadFileRoot, "rigorloop.jsonl")).mode & 0o777, 0o644);

  const componentParent = root();
  chmodSync(componentParent, 0o700);
  const nonDirectoryComponent = join(componentParent, "not-a-directory");
  writeFileSync(nonDirectoryComponent, "sentinel", { mode: 0o600 });
  const nestedRoot = join(nonDirectoryComponent, "logs");
  assert.throws(() => appendDiagnosticEvent(nestedRoot, event), (error) => error.code === "RL_LOG_UNSAFE_PATH");
  assert.equal(readFileSync(nonDirectoryComponent, "utf8"), "sentinel");
  assert.equal(existsSync(nestedRoot), false);
});

test("T05 rotates only above the exact byte boundary and retains four archives", () => {
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  const exact = root();
  chmodSync(exact, 0o700);
  writeFileSync(join(exact, "rigorloop.jsonl"), jsonLineOfSize(MAX_LOG_BYTES - Buffer.byteLength(event)), { mode: 0o600 });
  appendDiagnosticEvent(exact, event);
  assert.equal(statSync(join(exact, "rigorloop.jsonl")).size, MAX_LOG_BYTES);
  assert.equal(existsSync(join(exact, "rigorloop.1.jsonl")), false);
  assert.doesNotThrow(() => readFileSync(join(exact, "rigorloop.jsonl"), "utf8").trim().split("\n").forEach(JSON.parse));

  const above = root();
  chmodSync(above, 0o700);
  writeFileSync(join(above, "rigorloop.jsonl"), jsonLineOfSize(MAX_LOG_BYTES - Buffer.byteLength(event) + 1), { mode: 0o600 });
  for (let index = 1; index <= 4; index += 1) writeFileSync(join(above, `rigorloop.${index}.jsonl`), `${index}\n`, { mode: 0o600 });
  appendDiagnosticEvent(above, event);
  assert.deepEqual([0, 1, 2, 3, 4].map((index) => existsSync(join(above, index ? `rigorloop.${index}.jsonl` : "rigorloop.jsonl"))), [true, true, true, true, true]);
  assert.equal(readFileSync(join(above, "rigorloop.4.jsonl"), "utf8"), "3\n");
  assert.doesNotThrow(() => JSON.parse(readFileSync(join(above, "rigorloop.jsonl"), "utf8")));
});

test("T05 validates root, source, and destination immediately before every pathname mutation", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  writeFileSync(join(directory, "rigorloop.jsonl"), jsonLineOfSize(MAX_LOG_BYTES - Buffer.byteLength(event) + 1), { mode: 0o600 });
  for (let index = 1; index <= 4; index += 1) writeFileSync(join(directory, `rigorloop.${index}.jsonl`), `${index}\n`, { mode: 0o600 });

  const operations = [];
  appendDiagnosticEvent(directory, event, { fs: {
    lstatSync(path) {
      operations.push({ kind: "lstat", path });
      return lstatSync(path);
    },
    renameSync(source, destination) {
      operations.push({ kind: "rename", source, destination });
      return renameSync(source, destination);
    },
    unlinkSync(path) {
      operations.push({ kind: "unlink", path });
      return unlinkSync(path);
    },
  } });

  const mutations = operations.map((operation, index) => ({ operation, index })).filter(({ operation }) => operation.kind === "rename" || operation.kind === "unlink");
  assert.equal(mutations.length, 6);
  let previousMutation = -1;
  for (const { operation, index } of mutations) {
    const validation = operations.slice(previousMutation + 1, index);
    const source = operation.kind === "unlink" ? operation.path : operation.source;
    assert.ok(validation.some((entry) => entry.kind === "lstat" && entry.path === directory));
    assert.ok(validation.some((entry) => entry.kind === "lstat" && entry.path === source));
    if (operation.kind === "rename") assert.ok(validation.some((entry) => entry.kind === "lstat" && entry.path === operation.destination));
    assert.deepEqual(operations[index - 1], { kind: "lstat", path: source });
    previousMutation = index;
  }
});

test("T05 mutation validation failure prevents unlink and rename", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  writeFileSync(join(directory, "rigorloop.jsonl"), jsonLineOfSize(MAX_LOG_BYTES - Buffer.byteLength(event) + 1), { mode: 0o600 });
  const oldest = join(directory, "rigorloop.4.jsonl");
  writeFileSync(oldest, "sentinel\n", { mode: 0o600 });
  let mutations = 0;

  assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
    lstatSync(path) {
      if (path === directory) throw Object.assign(new Error("validation unavailable"), { code: "EIO" });
      return lstatSync(path);
    },
    renameSync(source, destination) { mutations += 1; return renameSync(source, destination); },
    unlinkSync(path) { mutations += 1; return unlinkSync(path); },
  } }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.equal(mutations, 0);
  assert.equal(readFileSync(oldest, "utf8"), "sentinel\n");
});

test("T05 rename and fsync faults preserve only complete retained records", () => {
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  for (const fault of ["fsync", "rename"]) {
    const directory = root();
    chmodSync(directory, 0o700);
    appendDiagnosticEvent(directory, event);
    const before = readFileSync(join(directory, "rigorloop.jsonl"));
    assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
      ...(fault === "fsync" ? { fsyncSync() { throw new Error("disk unavailable"); } } : {}),
      ...(fault === "rename" ? { renameSync() { throw new Error("rename unavailable"); } } : {}),
    } }), (error) => error.code === "RL_LOG_UNAVAILABLE");
    assert.deepEqual(readFileSync(join(directory, "rigorloop.jsonl")), before);
    assert.doesNotThrow(() => readFileSync(join(directory, "rigorloop.jsonl"), "utf8").trim().split("\n").forEach(JSON.parse));
  }
});

test("T05 disk-full write failure preserves the prior active record", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  appendDiagnosticEvent(directory, event);
  const before = readFileSync(join(directory, "rigorloop.jsonl"));
  assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
    writeSync() { throw Object.assign(new Error("disk full"), { code: "ENOSPC" }); },
  } }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.deepEqual(readFileSync(join(directory, "rigorloop.jsonl")), before);
});

test("T05 close failure degrades after publishing only a complete record", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  let injected = false;
  assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
    closeSync(fd) {
      closeSync(fd);
      if (!injected) {
        injected = true;
        throw new Error("close unavailable");
      }
    },
  } }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.doesNotThrow(() => readFileSync(join(directory, "rigorloop.jsonl"), "utf8").trim().split("\n").forEach(JSON.parse));
});

test("T05 pre-close faults release active and rotation descriptors before returning", () => {
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  const scenarios = [
    { name: "active read", rotation: false, faultAt: 1 },
    { name: "ordinary pre-publication validation", rotation: false, faultAt: 2 },
    { name: "oldest archive", rotation: true, faultAt: 2 },
    { name: "archive three", rotation: true, faultAt: 3 },
    { name: "archive two", rotation: true, faultAt: 4 },
    { name: "archive one", rotation: true, faultAt: 5 },
    { name: "active rotation", rotation: true, faultAt: 6 },
  ];

  for (const scenario of scenarios) {
    const directory = root();
    chmodSync(directory, 0o700);
    if (scenario.rotation) {
      writeFileSync(join(directory, "rigorloop.jsonl"), jsonLineOfSize(MAX_LOG_BYTES - Buffer.byteLength(event) + 1), { mode: 0o600 });
      for (let index = 1; index <= 4; index += 1) writeFileSync(join(directory, `rigorloop.${index}.jsonl`), `${index}\n`, { mode: 0o600 });
    } else {
      appendDiagnosticEvent(directory, event);
    }

    let closeCalls = 0;
    let faultedFd = null;
    assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
      closeSync(fd) {
        closeCalls += 1;
        if (closeCalls === scenario.faultAt) {
          faultedFd = fd;
          throw new Error(`pre-close fault: ${scenario.name}`);
        }
        closeSync(fd);
      },
    } }), (error) => error.code === "RL_LOG_UNAVAILABLE", scenario.name);
    assert.notEqual(faultedFd, null, scenario.name);
    try {
      assert.throws(() => fstatSync(faultedFd), (error) => error.code === "EBADF", scenario.name);
    } finally {
      try { closeSync(faultedFd); } catch { /* already closed by the corrected sink */ }
    }
  }
});

test("T05 a partial candidate write plus rollback failure preserves complete active JSONL", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  appendDiagnosticEvent(directory, event);
  const active = join(directory, "rigorloop.jsonl");
  const before = readFileSync(active);
  assert.throws(() => appendDiagnosticEvent(directory, event, {
    fs: {
      writeSync(fd, buffer) {
        writeSync(fd, buffer.subarray(0, 7));
        return 7;
      },
      ftruncateSync() { throw new Error("rollback unavailable"); },
    },
  }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.deepEqual(readFileSync(active), before);
  assert.doesNotThrow(() => readFileSync(active, "utf8").trim().split("\n").forEach(JSON.parse));
  assert.equal(existsSync(join(directory, ".rigorloop-log.lock")), true);
});

test("T05 acquisition failure closes its descriptor, returns a stable code, and retains the stale lock", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const lock = join(directory, ".rigorloop-log.lock");
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  let closes = 0;
  assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
    fstatSync() { throw new Error("fstat unavailable"); },
    closeSync(fd) { closes += 1; closeSync(fd); },
  } }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.equal(closes, 1);
  assert.equal(existsSync(lock), true);
  assert.throws(() => appendDiagnosticEvent(directory, event, { wait: false }), (error) => error.code === "RL_LOG_UNAVAILABLE");
});

test("T05 acquisition cleanup never closes a different file that reuses its descriptor", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const replacement = join(directory, "replacement.txt");
  writeFileSync(replacement, "replacement\n", { mode: 0o600 });
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  let replacementFd = null;

  try {
    assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
      fstatSync() { throw new Error("acquisition identity unavailable"); },
      closeSync(fd) {
        closeSync(fd);
        replacementFd = openSync(replacement, "r");
        assert.equal(replacementFd, fd);
        throw new Error("close result unavailable");
      },
    } }), (error) => error.code === "RL_LOG_UNAVAILABLE");
    assert.notEqual(replacementFd, null);
    assert.doesNotThrow(() => fstatSync(replacementFd));
  } finally {
    if (replacementFd !== null) {
      try { closeSync(replacementFd); } catch { /* the failing implementation already closed it */ }
    }
  }
});

test("T05 active-file validation failure closes every opened descriptor", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  appendDiagnosticEvent(directory, event);
  let fstats = 0;
  let closes = 0;
  assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
    fstatSync(fd) {
      fstats += 1;
      if (fstats === 2) throw new Error("active fstat unavailable");
      return fstatSync(fd);
    },
    closeSync(fd) { closes += 1; closeSync(fd); },
  } }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.equal(fstats, 2);
  assert.equal(closes, 2);
});

test("T05 failed publication never performs pathname unlink cleanup", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const lock = join(directory, ".rigorloop-log.lock");
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  let unlinkCalls = 0;
  assert.throws(() => appendDiagnosticEvent(directory, event, { fs: {
    writeSync() { throw new Error("write unavailable"); },
    unlinkSync() { unlinkCalls += 1; throw new Error("must not unlink"); },
  } }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.equal(unlinkCalls, 0);
  assert.equal(existsSync(lock), true);
});

test("T05 cleanup never removes a replacement unowned lock", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const lock = join(directory, ".rigorloop-log.lock");
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  assert.throws(() => appendDiagnosticEvent(directory, event, {
    fs: {
      writeSync() {
        renameSync(lock, `${lock}.original`);
        writeFileSync(lock, "owned elsewhere", { mode: 0o600 });
        throw new Error("injected write failure");
      },
    },
  }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.equal(readFileSync(lock, "utf8"), "owned elsewhere");
});

test("T05 lock acquisition has deterministic attempt and deadline bounds", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  writeFileSync(join(directory, ".rigorloop-log.lock"), "owned elsewhere", { mode: 0o600 });
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  let elapsed = 0;
  let waits = 0;
  assert.throws(() => appendDiagnosticEvent(directory, event, {
    lockClock: () => elapsed,
    lockWait(milliseconds) { waits += 1; elapsed += milliseconds; },
  }), (error) => error.code === "RL_LOG_UNAVAILABLE");
  assert.ok(waits <= 9);
  assert.ok(elapsed <= 1000);
  assert.equal(readFileSync(join(directory, ".rigorloop-log.lock"), "utf8"), "owned elsewhere");
});

test("real concurrent writers retain only complete JSONL records", async () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const moduleUrl = new URL("../dist/lib/log-sink.js", import.meta.url).href;
  const eventUrl = new URL("../dist/lib/diagnostic-event.js", import.meta.url).href;
  const children = Array.from({ length: 6 }, (_, index) => new Promise((resolveChild, rejectChild) => {
    const source = `import { appendDiagnosticEvent } from ${JSON.stringify(moduleUrl)}; import { buildDiagnosticEvent, encodedEvent } from ${JSON.stringify(eventUrl)}; const id=${JSON.stringify(index.toString(16).padStart(16, "0"))}; const event=buildDiagnosticEvent({event:"invocation-start",invocation_id:id,severity:"info",command_family:"introspection",command:"version",cli_version:"0.4.1",sequence:1}); appendDiagnosticEvent(${JSON.stringify(directory)}, encodedEvent(event));`;
    const child = spawn(process.execPath, ["--input-type=module", "--eval", source], { stdio: "ignore" });
    child.once("error", rejectChild);
    child.once("exit", (code) => code === 0 ? resolveChild() : rejectChild(new Error(`writer exited ${code}`)));
  }));
  await Promise.all(children);
  const lines = readFileSync(join(directory, "rigorloop.jsonl"), "utf8").trim().split("\n");
  assert.equal(lines.length, 6);
  assert.doesNotThrow(() => lines.forEach(JSON.parse));
});

test("T05 concurrent writers crossing rotation retain only complete JSONL", async () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const moduleUrl = new URL("../dist/lib/log-sink.js", import.meta.url).href;
  const eventUrl = new URL("../dist/lib/diagnostic-event.js", import.meta.url).href;
  const sample = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: "0000000000000000", severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  writeFileSync(join(directory, "rigorloop.jsonl"), jsonLineOfSize(MAX_LOG_BYTES - Buffer.byteLength(sample) + 1), { mode: 0o600 });
  const children = Array.from({ length: 6 }, (_, index) => new Promise((resolveChild, rejectChild) => {
    const source = `import { appendDiagnosticEvent } from ${JSON.stringify(moduleUrl)}; import { buildDiagnosticEvent, encodedEvent } from ${JSON.stringify(eventUrl)}; const id=${JSON.stringify((index + 1).toString(16).padStart(16, "0"))}; appendDiagnosticEvent(${JSON.stringify(directory)}, encodedEvent(buildDiagnosticEvent({event:"invocation-start",invocation_id:id,severity:"info",command_family:"introspection",command:"version",cli_version:"0.4.1",sequence:1})));`;
    const child = spawn(process.execPath, ["--input-type=module", "--eval", source], { stdio: "ignore" });
    child.once("error", rejectChild);
    child.once("exit", (code) => code === 0 ? resolveChild() : rejectChild(new Error(`rotation writer exited ${code}`)));
  }));
  await Promise.all(children);
  const retained = LOG_NAMES.filter((name) => existsSync(join(directory, name))).flatMap((name) => readFileSync(join(directory, name), "utf8").trim().split("\n"));
  assert.equal(retained.length, 7);
  assert.doesNotThrow(() => retained.forEach(JSON.parse));
});

test("T05 interruption after a start append leaves exactly one complete event", async () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const moduleUrl = new URL("../dist/lib/log-sink.js", import.meta.url).href;
  const eventUrl = new URL("../dist/lib/diagnostic-event.js", import.meta.url).href;
  const source = `import { appendDiagnosticEvent } from ${JSON.stringify(moduleUrl)}; import { buildDiagnosticEvent, encodedEvent } from ${JSON.stringify(eventUrl)}; appendDiagnosticEvent(${JSON.stringify(directory)}, encodedEvent(buildDiagnosticEvent({event:"invocation-start",invocation_id:"0123456789abcdef",severity:"info",command_family:"introspection",command:"version",cli_version:"0.4.1",sequence:1}))); process.kill(process.pid, "SIGKILL");`;
  const outcome = await new Promise((resolveChild, rejectChild) => {
    const child = spawn(process.execPath, ["--input-type=module", "--eval", source], { stdio: "ignore" });
    child.once("error", rejectChild);
    child.once("exit", (code, signal) => resolveChild({ code, signal }));
  });
  assert.equal(outcome.signal, "SIGKILL");
  const retained = readFileSync(join(directory, "rigorloop.jsonl"), "utf8").trim().split("\n");
  assert.equal(retained.length, 1);
  assert.equal(JSON.parse(retained[0]).event, "invocation-start");
});

test("T05 logging core has no network, process, database, timer, or surviving handle dependency", () => {
  const sources = ["../dist/lib/diagnostic-event.js", "../dist/lib/log-config.js", "../dist/lib/log-sink.js"]
    .map((path) => readFileSync(new URL(path, import.meta.url), "utf8")).join("\n");
  assert.doesNotMatch(sources, /node:(?:net|http|https|tls|dgram|child_process|cluster|worker_threads)|setInterval|setTimeout|sqlite|postgres|mysql/i);
  const before = new Set(process._getActiveHandles());
  const directory = root();
  chmodSync(directory, 0o700);
  const event = encodedEvent(buildDiagnosticEvent({ event: "invocation-start", invocation_id: createInvocationId(), severity: "info", command_family: "introspection", command: "version", cli_version: "0.4.1", sequence: 1 }));
  appendDiagnosticEvent(directory, event);
  assert.deepEqual(process._getActiveHandles().filter((handle) => !before.has(handle)), []);
});
