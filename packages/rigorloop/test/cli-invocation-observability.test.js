import assert from "node:assert/strict";
import { chmodSync, existsSync, mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

import { classifyCommand } from "../dist/lib/cli-observability.js";
import { findInvocationEvents } from "../dist/lib/log-inspection.js";

function root() { return mkdtempSync(join(tmpdir(), "rigorloop-invocation-")); }

test("public commands have one closed family", () => {
  assert.equal(classifyCommand(["lifecycle", "status"]).family, "lifecycle");
  assert.equal(classifyCommand(["init"]).family, "repository-setup");
  assert.equal(classifyCommand(["version"]).family, "introspection");
  assert.equal(classifyCommand(["logs", "path"]).family, "log-inspection");
  assert.equal(classifyCommand(["future-command"]).family, "invalid-input");
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
