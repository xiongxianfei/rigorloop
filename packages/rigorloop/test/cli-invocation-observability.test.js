import assert from "node:assert/strict";
import { chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

import { classifyCommand } from "../dist/lib/cli-observability.js";
import { findInvocationEvents } from "../dist/lib/log-inspection.js";
import { runObservedCli } from "../dist/lib/cli-observability.js";

function root() { return mkdtempSync(join(tmpdir(), "rigorloop-invocation-")); }

function writeGovernedFixture(project) {
  const changeRoot = join(project, "docs", "changes", "example");
  const specRoot = join(project, "specs");
  mkdirSync(changeRoot, { recursive: true });
  mkdirSync(specRoot, { recursive: true });
  writeFileSync(join(specRoot, "example.md"), "# Example\n");
  const change = `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states:
  spec:
    kind: spec
    path: specs/example.md
    role: primary
    lifecycle_state: approved
workflow_state:
  lifecycle_state: active
  current_stage: implement
  next_stage: implement
  blocker: null
  evidence: []
  planned_work:
    current_milestone: M1
    milestones:
      M1:
        kind: implementation
        state: implementing
    remaining_implementation_milestones:
      - M1
review:
  status: approved
  unresolved_items: 0
`;
  const path = join(changeRoot, "change.yaml");
  writeFileSync(path, change);
  return path;
}

function normalizedSemantic(payload) {
  const copy = structuredClone(payload);
  delete copy.invocation_id;
  delete copy.observability;
  return copy;
}

test("public commands have one closed family", () => {
  assert.equal(classifyCommand(["lifecycle", "status"]).family, "lifecycle");
  assert.equal(classifyCommand(["init"]).family, "repository-setup");
  assert.equal(classifyCommand(["version"]).family, "introspection");
  assert.equal(classifyCommand(["logs", "path"]).family, "log-inspection");
  assert.equal(classifyCommand(["future-command"]).family, "invalid-input");
  assert.equal(classifyCommand(["lifecycle", "private-raw-operation"]).operation, "unknown");
});

test("T06 public command families record deterministic terminal severity and status", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const project = root();
  writeGovernedFixture(project);
  const cases = [
    { args: ["version"], family: "introspection", exit: 0, severity: "info", status: "success" },
    { args: ["init", "unsupported", "--json"], family: "repository-setup", exit: 2, severity: "warning", status: "blocked" },
    { args: ["future-command", "--json"], family: "invalid-input", exit: 4, severity: "warning", status: "error" },
    { args: ["logs", "path"], family: "log-inspection", exit: 0, severity: "info", status: "success" },
    { args: ["lifecycle", "status", "--change", "example", "--format", "json"], family: "lifecycle", exit: 0, severity: "info", status: "success" },
  ];
  for (const [index, item] of cases.entries()) {
    const directory = join(root(), `logs-${index}`);
    const child = spawnSync(process.execPath, [cli.pathname, ...item.args], {
      cwd: project, encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: directory },
    });
    assert.equal(child.status, item.exit, item.family);
    const events = readFileSync(join(directory, "rigorloop.jsonl"), "utf8").trim().split("\n").map(JSON.parse);
    assert.deepEqual(events.map((event) => event.sequence), [1, 2], item.family);
    assert.equal(events[1].command_family, item.family);
    assert.equal(events[1].severity, item.severity);
    assert.equal(events[1].status, item.status);
    assert.equal(events[1].exit_code, item.exit);
  }
});

test("T06 controller severity and console thresholds cover success, blocked, and internal outcomes", async () => {
  const cases = [
    { exitCode: 0, level: "info", severity: "info", console: true },
    { exitCode: 2, level: "warning", severity: "warning", console: true },
    { exitCode: 2, level: "error", severity: "warning", console: false },
    { exitCode: 1, level: "error", severity: "error", console: true },
  ];
  for (const item of cases) {
    const events = [];
    const stderr = [];
    const exit = await runObservedCli(["version", "--console-log-level", item.level], async () => ({ exitCode: item.exitCode, render: () => ({ stdout: "", stderr: "" }) }), {
      cliVersion: "0.4.1", env: { RIGORLOOP_LOG_DIR: root() },
      appendEvent: (_directory, encoded) => events.push(JSON.parse(encoded)),
      writeStdout() {}, writeStderr: (value) => stderr.push(value),
    });
    assert.equal(exit, item.exitCode);
    assert.equal(events.at(-1).severity, item.severity);
    assert.equal(stderr.join("").includes("invocation="), item.console);
  }

  const events = [];
  const stderr = [];
  const exit = await runObservedCli(["version"], async () => { throw new Error("private internal detail"); }, {
    cliVersion: "0.4.1", env: { RIGORLOOP_LOG_DIR: root() },
    appendEvent: (_directory, encoded) => events.push(JSON.parse(encoded)),
    writeStdout() {}, writeStderr: (value) => stderr.push(value),
  });
  assert.equal(exit, 1);
  assert.equal(events.at(-1).severity, "error");
  assert.equal(events.at(-1).status, "error");
  assert.equal(stderr.join("").includes("private internal detail"), false);
});

test("CLIOBS-M3-R1-F3 semantic terminal class controls severity independently of exit code", async () => {
  for (const item of [
    { terminalClass: "expected-rejection", severity: "warning", console: false },
    { terminalClass: "internal-error", severity: "error", console: true },
    { terminalClass: "unknown-terminal-class", severity: "error", console: true },
  ]) {
    const events = [];
    const stderr = [];
    const exit = await runObservedCli(["lifecycle", "validate"], async () => ({
      exitCode: 3,
      terminalClass: item.terminalClass,
      render: () => ({ stdout: "", stderr: "" }),
    }), {
      cliVersion: "0.4.1",
      env: { RIGORLOOP_LOG_DIR: root() },
      appendEvent: (_directory, encoded) => events.push(JSON.parse(encoded)),
      writeStdout() {},
      writeStderr: (value) => stderr.push(value),
    });
    assert.equal(exit, 3);
    assert.equal(events.at(-1).severity, item.severity);
    assert.equal(stderr.join("").includes("RL_CLI_INTERNAL"), item.console);
  }
});

test("CLI records correlated events, stays quiet on success, and supports exact lookup", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const child = spawnSync(process.execPath, [cli.pathname, "version"], { encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: directory } });
  assert.equal(child.status, 0);
  assert.equal(child.stderr, "");
  const lines = readFileSync(join(directory, "rigorloop.jsonl"), "utf8").trim().split("\n").map(JSON.parse);
  assert.deepEqual(lines.map((event) => event.sequence), [1, 2]);
  assert.equal(lines[0].invocation_id, lines[1].invocation_id);
  assert.deepEqual(findInvocationEvents(directory, lines[0].invocation_id).events, lines);
  assert.equal(findInvocationEvents(directory, "0000000000000000").code, "RL_LOG_NOT_FOUND");
  const lookup = spawnSync(process.execPath, [cli.pathname, "logs", "show", lines[0].invocation_id, "--format", "json"], { encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: directory } });
  assert.equal(lookup.status, 0);
  assert.equal(JSON.parse(lookup.stdout).events[0].invocation_id, lines[0].invocation_id);
});

test("explicit concise output is compact and disabling file logs is semantic-only", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const project = root();
  const child = spawnSync(process.execPath, [cli.pathname, "init", "codex", "--dry-run", "--format", "concise-json", "--no-file-log"], { cwd: project, encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: directory } });
  assert.equal(child.status, 0);
  assert.equal(child.stderr, "");
  const payload = JSON.parse(child.stdout);
  assert.equal(payload.schema_version, 2);
  assert.equal(payload.projection, "concise");
  assert.equal(payload.observability, "disabled");
  assert.equal(existsSync(join(directory, "rigorloop.jsonl")), false);
});

test("T10 new-change supports shared explicit formats without changing legacy JSON", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const args = ["new-change", "example-change", "--title", "Example change", "--dry-run", "--no-file-log"];
  const project = root();
  const run = (extra) => spawnSync(process.execPath, [cli.pathname, ...args, ...extra], { cwd: project, encoding: "utf8" });
  const legacy = run(["--json"]);
  const detailed = run(["--format", "detailed-json"]);
  const concise = run(["--format", "concise-json"]);
  const conciseHuman = run(["--format", "concise-human"]);
  assert.equal(legacy.status, 0, legacy.stderr);
  assert.equal(detailed.status, 0, detailed.stderr);
  const detailedPayload = JSON.parse(detailed.stdout);
  const { observability, ...legacyCompatibleDetailed } = detailedPayload;
  assert.equal(observability, "disabled");
  assert.deepEqual(legacyCompatibleDetailed, JSON.parse(legacy.stdout));
  assert.equal(JSON.parse(concise.stdout).projection, "concise");
  assert.equal(JSON.parse(concise.stdout).command, "new-change");
  assert.equal(conciseHuman.status, 0, conciseHuman.stderr);
  assert.ok(conciseHuman.stdout.includes("new-change success"));
  assert.ok(conciseHuman.stdout.includes("observability=disabled"));
  assert.ok(conciseHuman.stdout.trim().split("\n").length <= 2);
});

test("file and console thresholds suppress lower-severity success events", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const child = spawnSync(process.execPath, [cli.pathname, "version", "--file-log-level", "error", "--console-log-level", "warning"], { encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: directory } });
  assert.equal(child.status, 0);
  assert.equal(child.stderr, "");
  assert.equal(existsSync(join(directory, "rigorloop.jsonl")), false);
});

test("an unsafe log override degrades diagnostics without suppressing semantic dispatch", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const project = root();
  const child = spawnSync(process.execPath, [cli.pathname, "init", "codex", "--dry-run", "--format", "concise-json"], {
    encoding: "utf8",
    cwd: project,
    env: { ...process.env, RIGORLOOP_LOG_DIR: "relative-private-value" },
  });
  assert.equal(child.status, 0);
  assert.equal(JSON.parse(child.stdout).observability, "degraded");
  assert.equal((child.stderr.match(/RL_LOG_UNAVAILABLE/g) ?? []).length, 1);
  assert.equal(child.stderr.includes("relative-private-value"), false);
});

test("explicitly disabled file logging does not validate an unused unsafe override", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const project = root();
  const child = spawnSync(process.execPath, [cli.pathname, "init", "codex", "--dry-run", "--format", "concise-json", "--no-file-log"], {
    encoding: "utf8",
    cwd: project,
    env: { ...process.env, RIGORLOOP_LOG_DIR: "unused-relative-value" },
  });
  assert.equal(child.status, 0);
  assert.equal(child.stderr, "");
  assert.equal(JSON.parse(child.stdout).observability, "disabled");
});

test("T07 environment-off and console-off degraded logging preserve semantic output", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const disabledRoot = root();
  const disabled = spawnSync(process.execPath, [cli.pathname, "version"], {
    encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: disabledRoot, RIGORLOOP_FILE_LOG: "off" },
  });
  assert.equal(disabled.status, 0);
  assert.equal(disabled.stderr, "");
  assert.equal(existsSync(join(disabledRoot, "rigorloop.jsonl")), false);

  const degraded = spawnSync(process.execPath, [cli.pathname, "version", "--console-log-level", "off"], {
    encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: "relative-private-path" },
  });
  assert.equal(degraded.status, 0);
  assert.equal(degraded.stdout, disabled.stdout);
  assert.equal(degraded.stderr, "");
});

test("event construction and completion sink failures preserve dispatch and finalize projection", async () => {
  const stdout = [];
  const stderr = [];
  let dispatched = 0;
  let appendCount = 0;
  const exitCode = await runObservedCli(["version"], async () => {
    dispatched += 1;
    return {
      exitCode: 0,
      render: ({ invocationId, observability }) => ({
        stdout: `${JSON.stringify({ schema_version: 2, projection: "concise", invocation_id: invocationId, command: "version", status: "success", exit_code: 0, observability })}\n`,
        stderr: "",
      }),
    };
  }, {
    cliVersion: "0.4.1",
    env: { RIGORLOOP_LOG_DIR: root() },
    now: () => new Date("2026-08-25T00:00:00.000Z"),
    appendEvent() {
      appendCount += 1;
      if (appendCount > 1) throw new Error("completion unavailable");
    },
    writeStdout: (value) => stdout.push(value),
    writeStderr: (value) => stderr.push(value),
  });
  assert.equal(exitCode, 0);
  assert.equal(dispatched, 1);
  assert.equal(JSON.parse(stdout.join("")).observability, "degraded");
  assert.equal((stderr.join("").match(/RL_LOG_UNAVAILABLE/g) ?? []).length, 1);
});

test("event construction failure is diagnostic-only", async () => {
  let dispatched = false;
  const events = [];
  const stderr = [];
  let renderedObservability;
  const exitCode = await runObservedCli(["version"], async () => {
    dispatched = true;
    return { exitCode: 0, render: ({ observability }) => { renderedObservability = observability; return { stdout: `${observability}\n`, stderr: "" }; } };
  }, {
    cliVersion: "0.4.1",
    env: { RIGORLOOP_LOG_DIR: root() },
    now: () => { throw new Error("clock unavailable"); },
    appendEvent: (_directory, encoded) => events.push(JSON.parse(encoded)),
    writeStdout() {},
    writeStderr: (value) => stderr.push(value),
  });
  assert.equal(exitCode, 0);
  assert.equal(dispatched, true);
  assert.equal(renderedObservability, "degraded");
  assert.equal(events.length, 0);
  assert.equal((stderr.join("").match(/RL_LOG_UNAVAILABLE/g) ?? []).length, 1);
});

test("diagnostic stderr failure never prevents semantic dispatch", async () => {
  let dispatched = false;
  const exitCode = await runObservedCli(["version"], async () => {
    dispatched = true;
    return { exitCode: 0, render: () => ({ stdout: "semantic output\n", stderr: "" }) };
  }, {
    env: { RIGORLOOP_LOG_DIR: root() },
    appendEvent() { throw new Error("sink unavailable"); },
    writeStdout() {},
    writeStderr() { throw new Error("stderr unavailable"); },
  });
  assert.equal(dispatched, true);
  assert.equal(exitCode, 0);
});

test("diagnostic writes are non-throwing before and after dispatch and suppressed by off", async () => {
  for (const args of [["version"], ["version", "--console-log-level", "off"]]) {
    let dispatched = false;
    let diagnosticWrites = 0;
    const exitCode = await runObservedCli(args, async () => {
      dispatched = true;
      return { exitCode: 1, render: () => ({ stdout: "", stderr: "" }) };
    }, {
      env: { RIGORLOOP_LOG_DIR: root() },
      appendEvent(_directory, _encoded) {},
      writeStdout() {},
      writeStderr() { diagnosticWrites += 1; throw new Error("stderr unavailable"); },
    });
    assert.equal(dispatched, true);
    assert.equal(exitCode, 1);
    assert.equal(diagnosticWrites, args.includes("off") ? 0 : 1);
  }

  let dispatched = false;
  const invalid = await runObservedCli(["version", "--file-log-level", "private-invalid-level"], async () => {
    dispatched = true;
    return 0;
  }, { writeStderr() { throw new Error("stderr unavailable"); } });
  assert.equal(invalid, 4);
  assert.equal(dispatched, false);
});

test("T03 private failure details are absent from stdout, stderr, retained logs, and lookup", async () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const marker = "M2_PRIVATE_FAILURE_SENTINEL";
  const stdout = [];
  const stderr = [];
  const exitCode = await runObservedCli(["version"], async () => {
    throw new Error(`${marker}: private stack and credential`);
  }, {
    cliVersion: "0.4.1",
    env: { RIGORLOOP_LOG_DIR: directory },
    writeStdout: (value) => stdout.push(value),
    writeStderr: (value) => stderr.push(value),
  });
  assert.equal(exitCode, 1);
  const retained = readFileSync(join(directory, "rigorloop.jsonl"), "utf8");
  const invocationId = JSON.parse(retained.split("\n")[0]).invocation_id;
  const lookup = JSON.stringify(findInvocationEvents(directory, invocationId));
  for (const surface of [stdout.join(""), stderr.join(""), retained, lookup]) assert.equal(surface.includes(marker), false);
});

test("concise projections use the controller's semantic exit code", () => {
  const directory = root();
  const archive = join(directory, "invalid.zip");
  writeFileSync(archive, "not-a-zip");
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const child = spawnSync(process.execPath, [cli.pathname, "init", "codex", "--from-archive", archive, "--dry-run", "--format", "concise-json", "--no-file-log"], { cwd: directory, encoding: "utf8" });
  assert.equal(child.status, 3);
  assert.equal(JSON.parse(child.stdout).exit_code, child.status);
});

test("unsafe log inspection fails without exposing or resolving the override", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const child = spawnSync(process.execPath, [cli.pathname, "logs", "path", "--format", "json"], { encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: "private-relative-value" } });
  assert.equal(child.status, 3);
  assert.equal(JSON.parse(child.stdout).errors[0].code, "RL_LOG_UNSAFE_PATH");
  assert.equal(`${child.stdout}${child.stderr}`.includes("private-relative-value"), false);
});

test("log inspection rejects undocumented common-result projections", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  for (const args of [["logs", "path"], ["logs", "show", "a1b2c3d4e5f60718"]]) {
    const child = spawnSync(process.execPath, [cli.pathname, ...args, "--format", "detailed-json", "--no-file-log"], { encoding: "utf8" });
    assert.equal(child.status, 4);
    assert.match(child.stderr, /RL_INVALID_REQUEST: unknown log output format/);
    assert.equal(child.stdout, "");
  }
});

test("lookup of an absent log store is read-only", () => {
  const parent = root();
  const absent = join(parent, "missing-store");
  assert.equal(findInvocationEvents(absent, "0000000000000000").code, "RL_LOG_NOT_FOUND");
  assert.equal(existsSync(absent), false);
});

test("lookup returns exact events and only bounded warnings for unrelated corruption", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const identity = "a1b2c3d4e5f60718";
  const valid = {
    schema_version: 1,
    event: "invocation-start",
    timestamp: "2026-08-25T00:00:00.000Z",
    invocation_id: identity,
    severity: "info",
    command_family: "introspection",
    command: "version",
    cli_version: "0.4.1",
    sequence: 1,
  };
  writeFileSync(join(directory, "rigorloop.jsonl"), `${JSON.stringify(valid)}\nprivate-corrupt-content\n${JSON.stringify({ schema_version: 2, invocation_id: identity })}\n`, { mode: 0o600 });
  const result = findInvocationEvents(directory, identity);
  assert.equal(result.status, "warning");
  assert.equal(result.events.length, 1);
  assert.equal(JSON.stringify(result).includes("private-corrupt-content"), false);
  assert.deepEqual(result.warnings.map((warning) => warning.code), ["RL_LOG_CORRUPT_ENTRY", "RL_LOG_UNAVAILABLE"]);
});

test("CLIOBS-M3-R1-F1 lookup rejects matching schema-one objects outside the closed event schema", () => {
  const directory = root();
  chmodSync(directory, 0o700);
  const identity = "a1b2c3d4e5f60718";
  const marker = "M3_LOOKUP_PRIVATE_SENTINEL";
  writeFileSync(join(directory, "rigorloop.jsonl"), `${JSON.stringify({ schema_version: 1, invocation_id: identity, event: "invocation-start", private: marker })}\n`, { mode: 0o600 });
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const child = spawnSync(process.execPath, [cli.pathname, "logs", "show", identity, "--format", "json", "--no-file-log"], {
    encoding: "utf8",
    env: { ...process.env, RIGORLOOP_LOG_DIR: directory },
  });
  assert.equal(child.status, 3);
  assert.equal(JSON.parse(child.stdout).code, "RL_LOG_CORRUPT_ENTRY");
  assert.equal(`${child.stdout}${child.stderr}`.includes(marker), false);
});

test("CLIOBS-M3-R1-F2 invalid lookup identities are never reflected", () => {
  const directory = root();
  const marker = "M3_INVALID_PRIVATE_SENTINEL";
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  for (const extra of [[], ["--format", "json"]]) {
    const child = spawnSync(process.execPath, [cli.pathname, "logs", "show", marker, ...extra, "--no-file-log"], {
      encoding: "utf8",
      env: { ...process.env, RIGORLOOP_LOG_DIR: directory },
    });
    assert.equal(child.status, 4);
    assert.equal(`${child.stdout}${child.stderr}`.includes(marker), false);
    assert.match(`${child.stdout}${child.stderr}`, /RL_INVALID_INVOCATION_ID/);
    if (extra.length) assert.equal("invocation_id" in JSON.parse(child.stdout), false);
  }
});

test("T12 logging states preserve lifecycle semantics and repository bytes", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const project = root();
  const changePath = writeGovernedFixture(project);
  const before = readFileSync(changePath);
  const run = (extraArgs, env) => spawnSync(process.execPath, [cli.pathname, "lifecycle", "status", "--change", "example", "--format", "concise-json", ...extraArgs], {
    cwd: project, encoding: "utf8", env: { ...process.env, ...env },
  });
  const recordedRoot = root();
  const recorded = run([], { RIGORLOOP_LOG_DIR: recordedRoot });
  const disabled = run(["--no-file-log"], { RIGORLOOP_LOG_DIR: root() });
  const unsafe = run([], { RIGORLOOP_LOG_DIR: "relative-private-path" });
  const lockedRoot = root();
  writeFileSync(join(lockedRoot, ".rigorloop-log.lock"), "owned elsewhere", { mode: 0o600 });
  const locked = run([], { RIGORLOOP_LOG_DIR: lockedRoot });
  const results = [recorded, disabled, unsafe, locked];
  for (const result of results) assert.equal(result.status, 0, result.stderr);
  const semantic = results.map((result) => normalizedSemantic(JSON.parse(result.stdout)));
  for (const result of semantic.slice(1)) assert.deepEqual(result, semantic[0]);
  assert.deepEqual(readFileSync(changePath), before);
  assert.equal(JSON.parse(recorded.stdout).observability, "recorded");
  assert.equal(JSON.parse(disabled.stdout).observability, "disabled");
  assert.equal(JSON.parse(unsafe.stdout).observability, "degraded");
  assert.equal(JSON.parse(locked.stdout).observability, "degraded");
});

test("T14 copied diagnostic claims cannot alter lifecycle status", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url);
  const project = root();
  writeGovernedFixture(project);
  const cleanRoot = root();
  const adversarialRoot = root();
  const fake = {
    schema_version: 1, event: "invocation-complete", timestamp: "2026-08-25T00:00:00.000Z",
    invocation_id: "0000000000000000", severity: "info", command_family: "lifecycle",
    command: "lifecycle", cli_version: "0.4.1", sequence: 2, status: "approved",
    exit_code: 0, duration_ms: 0, operation: "settle-artifact", change_id: "example",
    resulting_lifecycle_revision: "sha256:forged", state_changed: true,
  };
  writeFileSync(join(adversarialRoot, "rigorloop.jsonl"), `${JSON.stringify(fake)}\n`, { mode: 0o600 });
  const invoke = (directory) => spawnSync(process.execPath, [cli.pathname, "lifecycle", "status", "--change", "example", "--format", "concise-json", "--no-file-log"], {
    cwd: project, encoding: "utf8", env: { ...process.env, RIGORLOOP_LOG_DIR: directory },
  });
  const clean = invoke(cleanRoot);
  const adversarial = invoke(adversarialRoot);
  assert.equal(clean.status, 0);
  assert.equal(adversarial.status, 0);
  assert.deepEqual(normalizedSemantic(JSON.parse(adversarial.stdout)), normalizedSemantic(JSON.parse(clean.stdout)));
  assert.notEqual(JSON.parse(adversarial.stdout).lifecycle_revision, "sha256:forged");
});
