import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";

import { exitCodeForResult } from "../dist/lib/command-result.js";

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

function readProjectFile(root, path) {
  return readFileSync(join(root, path), "utf8");
}

function actionFor(output, path) {
  return output.actions.find((action) => action.path === path);
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
  for (const key of [
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
  ]) {
    assert.ok(Object.hasOwn(output, key), key);
  }
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
  for (const key of [
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
  ]) {
    assert.ok(Object.hasOwn(output, key), key);
  }
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

test("T11 exit-code mapping covers every public exit class", () => {
  const cases = [
    ["success", { status: "success", exit_class: "success" }, 0],
    ["warning", { status: "warning", exit_class: "success" }, 0],
    ["blocked", { status: "blocked", exit_class: "blocked" }, 2],
    ["validation failed", { status: "error", exit_class: "validation_failed" }, 3],
    ["invalid usage", { status: "error", exit_class: "invalid_usage" }, 4],
    ["mutation conflict", { status: "blocked", exit_class: "mutation_conflict" }, 5],
    ["internal", { status: "error", exit_class: "internal" }, 1],
  ];

  for (const [name, result, expected] of cases) {
    assert.equal(exitCodeForResult(result), expected, name);
  }
});

test("T11 command-path exit-code mapping is enforced for M1 command paths", () => {
  const cwd = tempProject();
  const success = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd });
  const blocked = runCli(["init", "--adapter", "claude", "--json"], { cwd });
  const usage = runCli(["unknown-command"], { cwd });

  assert.equal(success.status, 0);
  assert.equal(blocked.status, 2);
  assert.equal(usage.status, 4);
});

test("T12 dry-run init plans scaffold writes without mutating the project", () => {
  const cwd = tempProject();
  const before = listProject(cwd);
  const result = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "success");
  assert.equal(output.planned_manifest.path, "rigorloop.yaml");
  assert.match(output.planned_manifest.content, /schema_version: 1/);
  assert.match(output.planned_manifest.content, /name: codex/);
  assert.match(output.planned_manifest.content, /install_root: ".agents\/skills"/);
  assert.equal(output.planned_lockfile.tree_hash_algorithm, "rigorloop-tree-hash-v1");
  assert.deepEqual(output.actions.map((action) => action.path).slice(0, 3), [".agents", ".agents/skills", "rigorloop.yaml"]);
  assert.equal(actionFor(output, ".agents")?.type, "create-dir");
  assert.equal(actionFor(output, ".agents")?.status, "planned");
  assert.equal(actionFor(output, ".agents/skills")?.type, "create-dir");
  assert.equal(actionFor(output, ".agents/skills")?.status, "planned");
  assert.equal(actionFor(output, "rigorloop.yaml")?.type, "write");
  assert.deepEqual(listProject(cwd), before);
});

test("T13 init requires --adapter codex", () => {
  const cwd = tempProject();
  const result = runCli(["init"], { cwd });

  assert.equal(result.status, 4);
  assert.match(`${result.stdout}${result.stderr}`, /--adapter codex/);
  assert.deepEqual(listProject(cwd), []);
});

test("T14 missing local archive path is invalid input", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--from-archive", "./missing.zip", "--json"], { cwd });

  assert.equal(result.status, 4);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "invalid-archive-path");
  assert.deepEqual(listProject(cwd), []);

  const missingValue = runCli(["init", "--adapter", "codex", "--from-archive", "--json"], { cwd });
  assert.equal(missingValue.status, 4);
  assert.equal(JSON.parse(missingValue.stdout).errors[0].code, "invalid-archive-path");
  assert.deepEqual(listProject(cwd), []);
});

test("T20 actual init writes minimum manifest and Codex install root without lockfile", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex", "--json"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stderr, "");
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "warning");
  assert.equal(output.warnings[0].code, "lockfile-spec-not-approved");
  assert.deepEqual(output.actions.map((action) => action.path).slice(0, 3), [".agents", ".agents/skills", "rigorloop.yaml"]);
  assert.equal(actionFor(output, ".agents")?.status, "done");
  assert.equal(actionFor(output, ".agents/skills")?.status, "done");
  assert.equal(actionFor(output, "rigorloop.yaml")?.status, "done");
  assert.equal(existsSync(join(cwd, ".agents")), true);
  assert.equal(existsSync(join(cwd, ".agents", "skills")), true);
  assert.equal(existsSync(join(cwd, "rigorloop.lock")), false);

  const manifest = readProjectFile(cwd, "rigorloop.yaml");
  assert.match(manifest, /schema_version: 1/);
  assert.match(manifest, /package: "@xiongxianfei\/rigorloop"/);
  assert.match(manifest, /package_version: "0\.1\.3"/);
  assert.match(manifest, /name: codex/);
  assert.match(manifest, /install_root: ".agents\/skills"/);
  assert.match(manifest, /type: release-archive/);
  assert.match(manifest, /release: "v0\.1\.3"/);
});

test("T24 write plan represents parent and leaf directory states before mutation", () => {
  const parentOnlyProject = tempProject();
  mkdirSync(join(parentOnlyProject, ".agents"));
  const parentOnly = runCli(["init", "--adapter", "codex", "--json"], { cwd: parentOnlyProject });

  assert.equal(parentOnly.status, 0, parentOnly.stderr);
  const parentOnlyOutput = JSON.parse(parentOnly.stdout);
  assert.equal(actionFor(parentOnlyOutput, ".agents")?.status, "skipped");
  assert.equal(actionFor(parentOnlyOutput, ".agents/skills")?.status, "done");

  const existingDirsProject = tempProject();
  mkdirSync(join(existingDirsProject, ".agents", "skills"), { recursive: true });
  const existingDirs = runCli(["init", "--adapter", "codex", "--json"], { cwd: existingDirsProject });

  assert.equal(existingDirs.status, 0, existingDirs.stderr);
  const existingDirsOutput = JSON.parse(existingDirs.stdout);
  assert.equal(actionFor(existingDirsOutput, ".agents")?.status, "skipped");
  assert.equal(actionFor(existingDirsOutput, ".agents/skills")?.status, "skipped");
});

test("T21 existing manifest handling is non-destructive", () => {
  const validProject = tempProject();
  const existingManifest = `schema_version: 1
rigorloop:
  package: "@xiongxianfei/rigorloop"
  package_version: "0.1.3"
adapters:
  - name: codex
    install_root: ".agents/skills"
    source:
      type: release-archive
      release: "v0.1.3"
`;
  writeFileSync(join(validProject, "rigorloop.yaml"), existingManifest);
  const validResult = runCli(["init", "--adapter", "codex", "--json"], { cwd: validProject });

  assert.equal(validResult.status, 0, validResult.stderr);
  assert.equal(readProjectFile(validProject, "rigorloop.yaml"), existingManifest);
  assert.ok(JSON.parse(validResult.stdout).actions.some((action) => action.path === "rigorloop.yaml" && action.status === "skipped"));

  const invalidProject = tempProject();
  writeFileSync(join(invalidProject, "rigorloop.yaml"), "schema_version: 99\n");
  const invalidResult = runCli(["init", "--adapter", "codex", "--json"], { cwd: invalidProject });

  assert.equal(invalidResult.status, 4);
  assert.equal(readProjectFile(invalidProject, "rigorloop.yaml"), "schema_version: 99\n");
  const output = JSON.parse(invalidResult.stdout);
  assert.equal(output.status, "error");
  assert.equal(output.errors[0].code, "invalid-config");
});

test("T22 local archive mode plans local-archive manifest source", () => {
  const cwd = tempProject();
  writeFileSync(join(cwd, "rigorloop-adapter-codex-v0.1.3.zip"), "placeholder archive fixture\n");
  const result = runCli(["init", "--adapter", "codex", "--from-archive", "./rigorloop-adapter-codex-v0.1.3.zip", "--dry-run", "--json"], {
    cwd,
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.match(output.planned_manifest.content, /type: local-archive/);
  assert.match(output.planned_manifest.content, /archive: "\.\/rigorloop-adapter-codex-v0\.1\.3\.zip"/);
  assert.equal(output.planned_lockfile.generated.adapters[0].source, "local-archive");
  assert.equal(output.planned_lockfile.generated.adapters[0].archive, "rigorloop-adapter-codex-v0.1.3.zip");
  assert.deepEqual(listProject(cwd), ["rigorloop-adapter-codex-v0.1.3.zip"]);

  const actualProject = tempProject();
  writeFileSync(join(actualProject, "rigorloop-adapter-codex-v0.1.3.zip"), "placeholder archive fixture\n");
  const actual = runCli(["init", "--adapter", "codex", "--from-archive", "./rigorloop-adapter-codex-v0.1.3.zip"], {
    cwd: actualProject,
  });

  assert.equal(actual.status, 0, actual.stderr);
  const manifest = readProjectFile(actualProject, "rigorloop.yaml");
  assert.match(manifest, /type: local-archive/);
  assert.match(manifest, /archive: "\.\/rigorloop-adapter-codex-v0\.1\.3\.zip"/);
});

test("T23 generated manifest avoids forbidden claims and validation commands", () => {
  const cwd = tempProject();
  const result = runCli(["init", "--adapter", "codex"], { cwd });

  assert.equal(result.status, 0, result.stderr);
  const manifest = readProjectFile(cwd, "rigorloop.yaml");
  assert.doesNotMatch(manifest, /branch-ready|pr-ready|pr-body-ready|pr-open-ready|workflow-accepted|validation-success|lockfile-authority/);
  assert.doesNotMatch(manifest, /validation:\s*\n\s*commands:/);
});

test("T26 overwrite conflicts are refused without replacing user files", () => {
  const cwd = tempProject();
  writeFileSync(join(cwd, ".agents"), "user file\n");
  const result = runCli(["init", "--adapter", "codex", "--json", "--force"], { cwd });

  assert.equal(result.status, 5);
  assert.equal(result.stderr, "");
  assert.equal(readProjectFile(cwd, ".agents"), "user file\n");
  assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "overwrite-refused");
  assert.equal(output.blockers[0].path, ".agents");
  assert.equal(actionFor(output, ".agents")?.status, "blocked");
  assert.equal(actionFor(output, ".agents/skills")?.status, "blocked");
});

test("T26 leaf install-root file conflict is refused without replacing user files", () => {
  const cwd = tempProject();
  mkdirSync(join(cwd, ".agents"));
  writeFileSync(join(cwd, ".agents", "skills"), "user file\n");
  const result = runCli(["init", "--adapter", "codex", "--json", "--force"], { cwd });

  assert.equal(result.status, 5);
  assert.equal(result.stderr, "");
  assert.equal(readProjectFile(cwd, ".agents/skills"), "user file\n");
  assert.equal(existsSync(join(cwd, "rigorloop.yaml")), false);
  const output = JSON.parse(result.stdout);
  assert.equal(output.status, "blocked");
  assert.equal(output.blockers[0].code, "overwrite-refused");
  assert.equal(output.blockers[0].path, ".agents/skills");
  assert.equal(actionFor(output, ".agents")?.status, "skipped");
  assert.equal(actionFor(output, ".agents/skills")?.status, "blocked");
});

test("T41 lockfile is planned output only and never durably written", () => {
  const newProject = tempProject();
  const dryRun = runCli(["init", "--adapter", "codex", "--dry-run", "--json"], { cwd: newProject });

  assert.equal(dryRun.status, 0, dryRun.stderr);
  assert.equal(JSON.parse(dryRun.stdout).planned_lockfile.tree_hash_algorithm, "rigorloop-tree-hash-v1");
  assert.equal(existsSync(join(newProject, "rigorloop.lock")), false);

  const existingProject = tempProject();
  writeFileSync(join(existingProject, "rigorloop.lock"), "existing-lock\n");
  const actual = runCli(["init", "--adapter", "codex", "--json"], { cwd: existingProject });

  assert.equal(actual.status, 0, actual.stderr);
  assert.equal(readProjectFile(existingProject, "rigorloop.lock"), "existing-lock\n");
  const output = JSON.parse(actual.stdout);
  assert.equal(output.planned_lockfile.tree_hash_algorithm, "rigorloop-tree-hash-v1");
  assert.ok(output.warnings.some((warning) => warning.code === "lockfile-spec-not-approved"));
});
