import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";

const packageRoot = resolve(import.meta.dirname, "..");
const packageJsonPath = join(packageRoot, "package.json");
const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf8"));
const cliPath = join(packageRoot, packageJson.bin.rigorloop);

function runCli(args, options = {}) {
  return spawnSync(process.execPath, [cliPath, ...args], {
    cwd: options.cwd ?? packageRoot,
    env: { ...process.env, ...(options.env ?? {}) },
    encoding: "utf8",
  });
}

function tempProject() {
  return mkdtempSync(join(tmpdir(), "rigorloop-cli-test-"));
}

function listProject(root) {
  return readdirSync(root, { recursive: true }).sort();
}

test("T1 package metadata exposes one public binary and no archive files", () => {
  assert.equal(packageJson.name, "@xiongxianfei/rigorloop");
  assert.deepEqual(Object.keys(packageJson.bin), ["rigorloop"]);
  assert.equal(packageJson.bin.rigorloop, "dist/bin/rigorloop.js");

  const files = packageJson.files ?? [];
  assert.ok(!files.some((entry) => entry.endsWith(".zip")));
});

test("T2 help output shows only the implemented command surface", () => {
  const result = runCli(["--help"]);

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /rigorloop\b/);
  assert.match(result.stdout, /rigorloop version/);
  assert.match(result.stdout, /rigorloop init --adapter codex/);
  assert.doesNotMatch(result.stdout, /\bnew-change\b/);
  assert.doesNotMatch(result.stdout, /\bstatus\b/);
  assert.doesNotMatch(result.stdout, /\bvalidate\b/);
});

test("T3 version output reports package identity", () => {
  const result = runCli(["version"]);

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /@xiongxianfei\/rigorloop/);
  assert.match(result.stdout, /0\.1\.3/);
});

test("T4 unknown commands return usage errors", () => {
  const result = runCli(["unknown-command"]);

  assert.equal(result.status, 4);
  assert.match(`${result.stdout}${result.stderr}`, /Unknown command/);
  assert.match(`${result.stdout}${result.stderr}`, /rigorloop --help/);
});

test("T5 unsupported adapters are blocked and do not write files", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "claude", "--json"], { cwd });

  assert.equal(result.status, 2);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "adapter-unsupported");
  assert.deepEqual(listProject(cwd), []);
});

test("T6 JSON envelope is stable and stdout contains JSON only", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.deepEqual(Object.keys(output), [
    "schema_version",
    "command",
    "package",
    "cwd",
    "status",
    "summary",
    "actions",
    "artifacts",
    "blockers",
    "warnings",
    "errors",
    "diagnostics",
  ]);
  assert.equal(output.schema_version, 1);
  assert.equal(output.command, "init");
  assert.equal(output.package.name, "@xiongxianfei/rigorloop");
  assert.equal(output.package.version, "0.1.3");
  assert.equal(output.cwd, cwd);
  assert.ok(["success", "warning", "blocked", "error"].includes(output.status));
  assert.ok(Array.isArray(output.actions));
  assert.ok(Array.isArray(output.artifacts));
  assert.ok(Array.isArray(output.blockers));
  assert.ok(Array.isArray(output.warnings));
  assert.ok(Array.isArray(output.errors));
  assert.equal(typeof output.diagnostics, "object");
});

test("T7 human output is not JSON-fragment output", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--dry-run"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /RigorLoop init dry run/);
  assert.doesNotThrow(() => {
    assert.throws(() => JSON.parse(result.stdout));
  });
});

test("T8 quiet mode does not change JSON shape or behavior", () => {
  const cwd = tempProject();
  const base = JSON.parse(
    execFileSync(process.execPath, [cliPath, "init", "--adapter", "codex", "--dry-run", "--json"], {
      cwd,
      encoding: "utf8",
    }),
  );
  const quietResult = runCli(["init", "--adapter", "codex", "--dry-run", "--json", "--quiet"], { cwd });

  assert.equal(quietResult.status, 0, quietResult.stderr);
  const quiet = JSON.parse(quietResult.stdout);
  assert.deepEqual(Object.keys(quiet), Object.keys(base));
  assert.equal(quiet.status, base.status);
});

test("T9 debug mode preserves stable top-level JSON fields", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--dry-run", "--json", "--debug"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.deepEqual(Object.keys(output), [
    "schema_version",
    "command",
    "package",
    "cwd",
    "status",
    "summary",
    "actions",
    "artifacts",
    "blockers",
    "warnings",
    "errors",
    "diagnostics",
  ]);
  assert.equal(output.diagnostics.debug, true);
});

test("T10 color is disabled by flag and environment", () => {
  const withFlag = runCli(["--help", "--no-color"]);
  const withEnv = runCli(["--help"], { env: { NO_COLOR: "1" } });
  const ansiPattern = /\u001b\[[0-9;]*m/;

  assert.equal(withFlag.status, 0);
  assert.equal(withEnv.status, 0);
  assert.doesNotMatch(withFlag.stdout, ansiPattern);
  assert.doesNotMatch(withEnv.stdout, ansiPattern);
});

test("T11 exit-code mapping is enforced for M1 command paths", () => {
  const cwd = tempProject();
  const success = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd });
  const blocked = runCli(["init", "--adapter", "claude", "--json"], { cwd });
  const usage = runCli(["unknown-command"], { cwd });

  assert.equal(success.status, 0);
  assert.equal(blocked.status, 2);
  assert.equal(usage.status, 4);
});
