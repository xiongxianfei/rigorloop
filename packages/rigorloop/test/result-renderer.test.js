import assert from "node:assert/strict";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

import { projectConciseResult, projectDetailedResult, renderResult, RESULT_FORMATS } from "../dist/lib/result-renderer.js";
import { executeLifecycleCli, repairStateChanged } from "../dist/lib/lifecycle-cli.js";
import { runLifecycleTransaction } from "../dist/lib/lifecycle-transaction.js";

const compatibilityFixturePath = join(import.meta.dirname, "fixtures", "observability", "v0.4.x-output-compatibility-v1.json");

function compatibilityProject(kind) {
  const project = mkdtempSync(join(tmpdir(), "rigorloop-compatibility-"));
  if (kind === "empty-lifecycle") mkdirSync(join(project, "docs", "changes"), { recursive: true });
  if (kind === "governed") {
    mkdirSync(join(project, "docs", "changes", "example"), { recursive: true });
    mkdirSync(join(project, "specs"), { recursive: true });
    writeFileSync(join(project, "specs", "example.md"), "# Example\n");
    writeFileSync(join(project, "docs", "changes", "example", "change.yaml"), `change_id: example
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
`);
  } else if (kind === "malformed") {
    mkdirSync(join(project, "docs", "changes", "broken"), { recursive: true });
    writeFileSync(join(project, "docs", "changes", "broken", "change.yaml"), "change_id: [\n");
  }
  return project;
}

function normalizeCompatibilityOutput(child, project) {
  const replaceProject = (value) => typeof value === "string" ? value.split(project).join("<PROJECT>") : value;
  const normalizeJson = (value) => {
    if (Array.isArray(value)) return value.map(normalizeJson);
    if (value && typeof value === "object") return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, normalizeJson(item)]));
    return replaceProject(value);
  };
  const stdout = child.stdout.trim();
  let semanticStdout;
  try {
    semanticStdout = normalizeJson(JSON.parse(stdout));
  } catch {
    semanticStdout = replaceProject(stdout.replace(/\r\n/g, "\n"));
  }
  return {
    exit_code: child.status,
    stdout: semanticStdout,
    stderr: replaceProject(child.stderr.trim().replace(/\r\n/g, "\n")),
  };
}

function detailedArgs(args) {
  const copy = [...args];
  const json = copy.indexOf("--json");
  if (json >= 0) copy.splice(json, 1, "--format", "detailed-json");
  const format = copy.indexOf("--format");
  if (format >= 0 && copy[format + 1] === "json") copy[format + 1] = "detailed-json";
  return copy;
}

function prepareMigrationRequest(cli, project) {
  const status = spawnSync(process.execPath, [cli, "lifecycle", "status", "--change", "example", "--format", "json"], {
    cwd: project, encoding: "utf8", env: { ...process.env, RIGORLOOP_FILE_LOG: "off", RIGORLOOP_CONSOLE_LOG_LEVEL: "off" },
  });
  writeFileSync(join(project, "migrate.json"), `${JSON.stringify({
    schema_version: 1,
    operation: "migrate",
    change_id: "example",
    expected_lifecycle_revision: JSON.parse(status.stdout).lifecycle_revision,
    source_schema_version: 1,
    stage_authority: "workflow",
  })}\n`);
}

const detailed = {
  schema_version: 1,
  command: "lifecycle",
  operation: "settle-artifact",
  status: "blocked",
  change_id: "example",
  lifecycle_revision: "sha256:abc",
  blockers: [{ code: "RL_UNRESOLVED_MATERIAL_FINDING", relevant_identities: ["F-12"], corrective_operation: "revise specification" }],
  permitted_operations: ["record-artifact-revision"],
  effective_state: { active_milestone: "M2" },
};

test("result formats are a closed vocabulary", () => {
  assert.deepEqual(RESULT_FORMATS, ["human", "json", "concise-human", "concise-json", "detailed-json"]);
  assert.throws(() => renderResult(detailed, { format: "verbose" }), /Unknown result format/);
});

test("concise JSON uses schema 2, closed applicable fields, and compact encoding", () => {
  const projected = projectConciseResult(detailed, { invocationId: "a1b2c3d4e5f60718", exitCode: 2, observability: "recorded" });
  assert.deepEqual(projected, {
    schema_version: 2,
    projection: "concise",
    invocation_id: "a1b2c3d4e5f60718",
    command: "lifecycle",
    operation: "settle-artifact",
    status: "blocked",
    exit_code: 2,
    change_id: "example",
    lifecycle_revision: "sha256:abc",
    next_operation: "revise specification",
    codes: ["RL_UNRESOLVED_MATERIAL_FINDING"],
    finding_ids: ["F-12"],
    milestone_ids: ["M2"],
    observability: "recorded",
  });
  const rendered = renderResult(detailed, { format: "concise-json", invocationId: "a1b2c3d4e5f60718", exitCode: 2 });
  assert.equal(rendered, `${JSON.stringify({ ...projected, observability: "disabled" })}\n`);
});

test("concise human output is actionable and at most two lines", () => {
  const output = renderResult(detailed, { format: "concise-human", invocationId: "a1b2c3d4e5f60718", exitCode: 2, observability: "recorded" });
  assert.ok(output.includes("settle-artifact blocked"));
  assert.ok(output.includes("RL_UNRESOLVED_MATERIAL_FINDING"));
  assert.ok(output.includes("next=revise specification"));
  assert.ok(output.includes("invocation=a1b2c3d4e5f60718"));
  assert.ok(output.trim().split("\n").length <= 2);
});

test("legacy JSON and detailed JSON retain the detailed object", () => {
  assert.equal(renderResult(detailed, { format: "json" }), `${JSON.stringify(detailed, null, 2)}\n`);
  assert.deepEqual(JSON.parse(renderResult(detailed, { format: "detailed-json", observability: "recorded" })), { ...detailed, observability: "recorded" });
});

test("T10 exact output fixture includes approved lifecycle fact evolution", () => {
  const fixture = JSON.parse(readFileSync(compatibilityFixturePath, "utf8"));
  assert.equal(fixture.baseline_revision, "fcbbfda44a89945ee06cfa0c1b16dcbd39984036");
  const cli = process.env.RIGORLOOP_COMPATIBILITY_CLI ?? new URL("../dist/bin/rigorloop.js", import.meta.url).pathname;
  const cases = [
    ["version-human-success", ["version"], "empty", false],
    ["unknown-human-failure", ["future-command"], "empty", false],
    ["unknown-json-failure", ["future-command", "--json"], "empty", true],
    ["init-human-success", ["init", "codex", "--dry-run"], "empty", false],
    ["init-human-blocked", ["init", "unsupported"], "empty", false],
    ["init-json-success", ["init", "codex", "--dry-run", "--json"], "empty", true],
    ["init-json-blocked", ["init", "unsupported", "--json"], "empty", true],
    ["new-change-human-success", ["new-change", "example-change", "--title", "Example change", "--dry-run"], "empty", false],
    ["new-change-human-failure", ["new-change", "example-change"], "empty", false],
    ["new-change-json-success", ["new-change", "example-change", "--title", "Example change", "--dry-run", "--json"], "empty", true],
    ["new-change-json-failure", ["new-change", "example-change", "--json"], "empty", true],
    ["lifecycle-status-human-success", ["lifecycle", "status", "--change", "example"], "governed", false],
    ["lifecycle-status-json-success", ["lifecycle", "status", "--change", "example", "--format", "json"], "governed", true],
    ["lifecycle-status-human-failure", ["lifecycle", "status"], "empty-lifecycle", false],
    ["lifecycle-status-json-failure", ["lifecycle", "status", "--format", "json"], "empty-lifecycle", true],
    ["lifecycle-context-human-success", ["lifecycle", "context", "code-review", "--change", "example"], "governed", false],
    ["lifecycle-context-json-success", ["lifecycle", "context", "code-review", "--change", "example", "--format", "json"], "governed", true],
    ["lifecycle-context-human-failure", ["lifecycle", "context", "unknown-stage", "--change", "example"], "governed", false],
    ["lifecycle-context-json-failure", ["lifecycle", "context", "unknown-stage", "--change", "example", "--format", "json"], "governed", true],
    ["lifecycle-validate-human-success", ["lifecycle", "validate", "--change", "example"], "governed", false],
    ["lifecycle-validate-json-success", ["lifecycle", "validate", "--change", "example", "--format", "json"], "governed", true],
    ["lifecycle-validate-human-failure", ["lifecycle", "validate", "--change", "broken"], "malformed", false],
    ["lifecycle-validate-json-failure", ["lifecycle", "validate", "--change", "broken", "--format", "json"], "malformed", true],
    ["lifecycle-mutation-human-success", ["lifecycle", "migrate", "--request", "migrate.json", "--dry-run"], "governed", false],
    ["lifecycle-mutation-json-success", ["lifecycle", "migrate", "--request", "migrate.json", "--dry-run", "--format", "json"], "governed", true],
    ["lifecycle-mutation-human-failure", ["lifecycle", "record-review", "--request", "missing.json"], "governed", false],
    ["lifecycle-mutation-json-failure", ["lifecycle", "record-review", "--request", "missing.json", "--format", "json"], "governed", true],
  ];
  const observed = {};
  for (const [id, args, projectKind, json] of cases) {
    const project = compatibilityProject(projectKind);
    if (id.includes("mutation") && id.includes("success")) {
      prepareMigrationRequest(cli, project);
    }
    const child = spawnSync(process.execPath, [cli, ...args], {
      cwd: project,
      encoding: "utf8",
      env: { ...process.env, RIGORLOOP_FILE_LOG: "off", RIGORLOOP_CONSOLE_LOG_LEVEL: "off" },
    });
    observed[id] = normalizeCompatibilityOutput(child, project);
    if (process.env.RIGORLOOP_UPDATE_COMPATIBILITY_FIXTURE !== "1") {
      assert.deepEqual(observed[id], fixture.cases[id], id);
      if (json) {
        const detailedProject = compatibilityProject(projectKind);
        if (id.includes("mutation") && id.includes("success")) prepareMigrationRequest(cli, detailedProject);
        const detailed = spawnSync(process.execPath, [cli, ...detailedArgs(args)], {
          cwd: detailedProject,
          encoding: "utf8",
          env: { ...process.env, RIGORLOOP_FILE_LOG: "off", RIGORLOOP_CONSOLE_LOG_LEVEL: "off" },
        });
        const normalizedDetailed = normalizeCompatibilityOutput(detailed, detailedProject);
        const compatibilityComparable = structuredClone(normalizedDetailed);
        if (compatibilityComparable.stdout && typeof compatibilityComparable.stdout === "object") {
          delete compatibilityComparable.stdout.state_changed;
          delete compatibilityComparable.stdout.observability;
        }
        assert.deepEqual(compatibilityComparable, fixture.cases[id], `${id} detailed-json compatibility facts`);
        assert.equal(normalizedDetailed.stdout.observability, "disabled");
        if (id === "lifecycle-mutation-json-success") assert.equal(normalizedDetailed.stdout.state_changed, false);
      }
    }
  }
  assert.equal(Object.keys(observed).length, 27);
  if (process.env.RIGORLOOP_UPDATE_COMPATIBILITY_FIXTURE !== "1") {
    assert.deepEqual(Object.keys(observed).sort(), Object.keys(fixture.cases).sort());
  }
  if (process.env.RIGORLOOP_UPDATE_COMPATIBILITY_FIXTURE === "1") {
    writeFileSync(compatibilityFixturePath, `${JSON.stringify({ ...fixture, cases: observed }, null, 2)}\n`);
  }
});

test("T11 state_changed reflects authoritative mutation facts only", () => {
  const cases = [
    ["planned", false],
    ["already-recorded", false],
    ["unchanged", false],
    ["recorded", true],
  ];
  for (const [status, stateChanged] of cases) {
    const projected = projectConciseResult({
      schema_version: 1, command: "lifecycle", operation: "record-review", status: "success",
      mutation: { status, state_changed: stateChanged },
    }, { invocationId: "a1b2c3d4e5f60718", exitCode: 0, observability: "disabled" });
    assert.equal(projected.state_changed, stateChanged, status);
  }
  const read = projectConciseResult({ command: "lifecycle", operation: "status", status: "success" }, {
    invocationId: "a1b2c3d4e5f60718", exitCode: 0, observability: "recorded",
  });
  assert.equal("state_changed" in read, false);
});

test("T11 repair state_changed includes lifecycle-owned lock bytes", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url).pathname;
  const env = { ...process.env, RIGORLOOP_FILE_LOG: "off", RIGORLOOP_CONSOLE_LOG_LEVEL: "off" };
  const invokeRepair = (withLock, lockPid = 99999999, expectedStatus = 0) => {
    const project = compatibilityProject("governed");
    const lock = join(project, "docs", "changes", "example", ".rigorloop-lifecycle.lock");
    if (withLock) writeFileSync(lock, JSON.stringify({ schema_version: 1, change_id: "example", pid: lockPid, nonce: "lock" }), { mode: 0o600 });
    const status = spawnSync(process.execPath, [cli, "lifecycle", "status", "--change", "example", "--format", "json"], { cwd: project, encoding: "utf8", env });
    writeFileSync(join(project, "repair.json"), `${JSON.stringify({
      schema_version: 1,
      operation: "repair",
      change_id: "example",
      expected_lifecycle_revision: JSON.parse(status.stdout).lifecycle_revision,
      condition: "clear-orphaned-lock",
      stage_authority: "workflow",
      dry_run_acknowledgement: true,
    })}\n`);
    const repair = spawnSync(process.execPath, [cli, "lifecycle", "repair", "--request", "repair.json", "--format", "concise-json"], { cwd: project, encoding: "utf8", env });
    assert.equal(repair.status, expectedStatus, repair.stderr);
    return { payload: JSON.parse(repair.stdout), lock };
  };
  const changed = invokeRepair(true);
  assert.equal(changed.payload.state_changed, true);
  assert.equal(existsSync(changed.lock), false);
  assert.equal(invokeRepair(false).payload.state_changed, false);
  const liveLock = invokeRepair(true, process.pid, 2);
  assert.equal(liveLock.payload.state_changed, false);
  assert.deepEqual(liveLock.payload.codes, ["RL_OPERATION_BUSY"]);
  assert.equal(existsSync(liveLock.lock), true);
});

test("T11 repair status vocabulary maps every persistence partition and fails closed", () => {
  for (const status of ["cleared-orphaned-lock", "restored-prior", "committed-candidate", "abandoned-prepared"]) {
    assert.equal(repairStateChanged(status), true, status);
  }
  for (const status of ["already-clear", "nothing-to-reconcile"]) {
    assert.equal(repairStateChanged(status), false, status);
  }
  assert.throws(() => repairStateChanged("unknown-repair-status"), { code: "RL_POST_VALIDATION_FAILED" });
});

test("T11 post-evaluation failures report authoritative lifecycle-owned persistence", () => {
  const cli = new URL("../dist/bin/rigorloop.js", import.meta.url).pathname;
  const env = { ...process.env, RIGORLOOP_FILE_LOG: "off", RIGORLOOP_CONSOLE_LOG_LEVEL: "off" };
  const busyProject = compatibilityProject("governed");
  prepareMigrationRequest(cli, busyProject);
  const liveLock = join(busyProject, "docs", "changes", "example", ".rigorloop-lifecycle.lock");
  writeFileSync(liveLock, JSON.stringify({ schema_version: 1, change_id: "example", pid: process.pid, nonce: "live" }), { mode: 0o600 });
  const busy = spawnSync(process.execPath, [cli, "lifecycle", "migrate", "--request", "migrate.json", "--format", "concise-json"], {
    cwd: busyProject, encoding: "utf8", env,
  });
  assert.equal(busy.status, 2, busy.stderr);
  assert.equal(JSON.parse(busy.stdout).state_changed, false);
  assert.equal(existsSync(liveLock), true);

  const rollbackProject = compatibilityProject("governed");
  prepareMigrationRequest(cli, rollbackProject);
  const before = readFileSync(join(rollbackProject, "docs", "changes", "example", "change.yaml"));
  const rollback = executeLifecycleCli(["migrate", "--request", "migrate.json", "--format", "concise-json"], {
    cwd: rollbackProject,
    runLifecycleTransaction() {
      throw Object.assign(new Error("injected transaction rollback"), { code: "RL_POST_VALIDATION_FAILED" });
    },
  });
  const projected = projectConciseResult(rollback.result, {
    invocationId: "a1b2c3d4e5f60718", exitCode: rollback.exitCode, observability: "disabled",
  });
  assert.equal(projected.state_changed, false);
  assert.equal(projectDetailedResult(rollback.result, { observability: "disabled" }).state_changed, false);
  assert.deepEqual(readFileSync(join(rollbackProject, "docs", "changes", "example", "change.yaml")), before);

  const retainedRecoveryProject = compatibilityProject("governed");
  prepareMigrationRequest(cli, retainedRecoveryProject);
  const retainedRecovery = executeLifecycleCli(["migrate", "--request", "migrate.json", "--format", "concise-json"], {
    cwd: retainedRecoveryProject,
    runLifecycleTransaction(args) {
      return runLifecycleTransaction({ ...args, fault: (point) => point === "after-recovery-prepared" ? "failure" : null });
    },
  });
  const retainedRecoveryProjection = projectConciseResult(retainedRecovery.result, {
    invocationId: "a1b2c3d4e5f60718", exitCode: retainedRecovery.exitCode, observability: "disabled",
  });
  assert.equal(retainedRecoveryProjection.state_changed, true);
  assert.equal(projectDetailedResult(retainedRecovery.result, { observability: "disabled" }).state_changed, true);
  assert.equal(existsSync(join(retainedRecoveryProject, "docs", "changes", "example", ".rigorloop-lifecycle-recovery.json")), true);

  const verifiedRollbackProject = compatibilityProject("governed");
  prepareMigrationRequest(cli, verifiedRollbackProject);
  const verifiedRollbackBefore = readFileSync(join(verifiedRollbackProject, "docs", "changes", "example", "change.yaml"));
  const verifiedRollback = executeLifecycleCli(["migrate", "--request", "migrate.json", "--format", "concise-json"], {
    cwd: verifiedRollbackProject,
    runLifecycleTransaction(args) {
      return runLifecycleTransaction({ ...args, fault: (point) => point === "after-replace-before-phase" ? "failure" : null });
    },
  });
  const verifiedRollbackProjection = projectConciseResult(verifiedRollback.result, {
    invocationId: "a1b2c3d4e5f60718", exitCode: verifiedRollback.exitCode, observability: "disabled",
  });
  assert.equal(verifiedRollbackProjection.state_changed, false);
  assert.equal(projectDetailedResult(verifiedRollback.result, { observability: "disabled" }).state_changed, false);
  assert.deepEqual(readFileSync(join(verifiedRollbackProject, "docs", "changes", "example", "change.yaml")), verifiedRollbackBefore);
  assert.equal(existsSync(join(verifiedRollbackProject, "docs", "changes", "example", ".rigorloop-lifecycle-recovery.json")), false);

  const preEvaluation = executeLifecycleCli(["migrate", "--request", "missing.json", "--format", "concise-json"], { cwd: rollbackProject });
  assert.equal("state_changed" in projectConciseResult(preEvaluation.result, {
    invocationId: "a1b2c3d4e5f60718", exitCode: preEvaluation.exitCode, observability: "disabled",
  }), false);
  assert.equal("state_changed" in projectDetailedResult(preEvaluation.result, { observability: "disabled" }), false);
});

test("T11 next_operation requires one deterministic continuation", () => {
  const base = { command: "lifecycle", operation: "status", status: "blocked" };
  const options = { invocationId: "a1b2c3d4e5f60718", exitCode: 2, observability: "recorded" };
  assert.equal(projectConciseResult({ ...base, permitted_operations: [] }, options).next_operation, undefined);
  assert.equal(projectConciseResult({ ...base, permitted_operations: ["validate"] }, options).next_operation, "validate");
  assert.equal(projectConciseResult({ ...base, permitted_operations: ["status", "validate"] }, options).next_operation, undefined);
  assert.equal(projectConciseResult({ ...base, next_operation: "record-review", permitted_operations: ["status", "validate"] }, options).next_operation, "record-review");
  assert.equal(projectConciseResult({ ...base, blockers: [
    { code: "RL_ONE", corrective_operation: "revise" },
    { code: "RL_TWO", corrective_operation: "decide" },
  ] }, options).next_operation, undefined);
});

test("T11 every concise terminal result requires common mandatory fields", () => {
  const complete = { command: "lifecycle", operation: "status", status: "success" };
  const options = { invocationId: "a1b2c3d4e5f60718", exitCode: 0, observability: "recorded" };
  assert.doesNotThrow(() => projectConciseResult(complete, options));
  assert.throws(() => projectConciseResult({ ...complete, command: undefined }, options), /mandatory terminal field/);
  assert.throws(() => projectConciseResult({ ...complete, status: undefined }, options), /mandatory terminal field/);
  assert.throws(() => projectConciseResult(complete, { ...options, invocationId: undefined }), /mandatory terminal field/);
  assert.throws(() => projectConciseResult(complete, { ...options, exitCode: undefined }), /mandatory terminal field/);
});

test("T11 shared facts remain equivalent across result classes", () => {
  const cases = [
    { command: "lifecycle", operation: "status", status: "success", exit: 0 },
    { command: "lifecycle", operation: "settle-artifact", status: "blocked", exit: 2, blockers: [{ code: "RL_BLOCKED" }] },
    { command: "lifecycle", operation: "validate", status: "error", exit: 4, errors: [{ code: "RL_INVALID_REQUEST" }] },
    { command: "lifecycle", operation: "record-review", status: "blocked", exit: 5, blockers: [{ code: "RL_STALE_OPERATION" }] },
    { command: "init", status: "error", exit: 1, errors: [{ code: "RL_CLI_INTERNAL" }] },
  ];
  for (const item of cases) {
    const { exit, ...result } = item;
    const concise = projectConciseResult(result, { invocationId: "a1b2c3d4e5f60718", exitCode: exit, observability: "recorded" });
    assert.equal(concise.command, result.command);
    assert.equal(concise.operation, result.operation);
    assert.equal(concise.status, result.status);
    assert.equal(concise.exit_code, exit);
    const expectedCodes = [...(result.blockers ?? []), ...(result.errors ?? [])].map(({ code }) => code);
    if (expectedCodes.length > 0) {
      assert.deepEqual(concise.codes, expectedCodes);
    } else {
      assert.equal("codes" in concise, false);
    }
  }
});

test("T11 explicit detailed projection materializes authoritative mutation truth without changing legacy JSON", () => {
  for (const stateChanged of [false, true]) {
    const result = { schema_version: 1, command: "lifecycle", operation: "migrate", status: stateChanged ? "success" : "error" };
    Object.defineProperty(result, "state_changed", { value: stateChanged, enumerable: false });
    const concise = projectConciseResult(result, { invocationId: "a1b2c3d4e5f60718", exitCode: stateChanged ? 0 : 3, observability: "disabled" });
    const detailed = JSON.parse(renderResult(result, { format: "detailed-json" }));
    const legacy = JSON.parse(renderResult(result, { format: "json" }));
    assert.equal(detailed.state_changed, concise.state_changed);
    assert.equal(detailed.observability, concise.observability);
    assert.equal("state_changed" in legacy, false);
    assert.equal("observability" in legacy, false);
  }
});

test("T11 every new projection carries a closed observability state", () => {
  const result = { schema_version: 1, command: "lifecycle", operation: "status", status: "success" };
  for (const observability of ["recorded", "degraded", "disabled"]) {
    assert.equal(projectConciseResult(result, { invocationId: "a1b2c3d4e5f60718", exitCode: 0, observability }).observability, observability);
    assert.equal(projectDetailedResult(result, { observability }).observability, observability);
    assert.match(renderResult(result, { format: "concise-human", invocationId: "a1b2c3d4e5f60718", exitCode: 0, observability }), new RegExp(`observability=${observability}`));
  }
  assert.throws(() => projectDetailedResult(result, { observability: "unknown" }), /Unknown observability state/);
  assert.throws(() => renderResult(result, { format: "concise-human", invocationId: "a1b2c3d4e5f60718", exitCode: 0, observability: "unknown" }), /Unknown observability state/);
});
