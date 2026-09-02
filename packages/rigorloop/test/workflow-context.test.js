import assert from "node:assert/strict";
import { spawn, spawnSync } from "node:child_process";
import { lstatSync, mkdirSync, readFileSync, readdirSync, symlinkSync, unlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { parseLifecycleYaml, serializeLifecycleYaml } from "../dist/lib/lifecycle-contract.js";
import { executeWorkflowContext } from "../dist/lib/workflow-context.js";
import { packageRepository } from "./helpers/lifecycle-package-fixture.js";

const cli = new URL("../dist/bin/rigorloop.js", import.meta.url).pathname;

function runPublic(root, args) {
  return spawnSync(process.execPath, [cli, "workflow-context", ...args], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, RIGORLOOP_FILE_LOG: "off", RIGORLOOP_CONSOLE_LOG_LEVEL: "off" },
  });
}

function snapshot(root) {
  return readFileSync(join(root, "docs", "changes", "example", "change.yaml"), "utf8");
}

function governedSnapshot(root, includeConfig = true) {
  const files = [];
  function visit(directory, prefix = "") {
    for (const entry of readdirSync(directory, { withFileTypes: true }).sort((left, right) => left.name.localeCompare(right.name))) {
      const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) visit(join(directory, entry.name), relative);
      else if (entry.isFile()) files.push([relative, readFileSync(join(directory, entry.name)).toString("base64")]);
    }
  }
  visit(join(root, "docs", "changes"));
  if (includeConfig) try { files.push(["rigorloop.workflow.yaml", readFileSync(join(root, "rigorloop.workflow.yaml")).toString("base64")]); } catch {}
  return files;
}

test("project phase reports bounded candidates and never selects one", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const secondRoot = join(root, "docs", "changes", "second");
  mkdirSync(secondRoot, { recursive: true });
  const second = parseLifecycleYaml(snapshot(root));
  second.change_id = "second";
  second.workflow_state.current_stage = "spec";
  second.workflow_state.next_stage = "spec";
  writeFileSync(join(secondRoot, "change.yaml"), serializeLifecycleYaml(second));
  writeFileSync(join(secondRoot, "review-log.md"), "# Review log\n");

  const before = snapshot(root);
  const execution = executeWorkflowContext(["--format", "json"], { cwd: root });

  assert.equal(execution.exitCode, 2);
  assert.equal(execution.result.phase, "project");
  assert.equal(execution.result.selection.state, "ambiguous");
  assert.equal(execution.result.selection.selected_change, null);
  assert.deepEqual(execution.result.candidates.map((item) => item.change_id), ["example", "second"]);
  assert.equal(execution.result.blockers[0].code, "RL_CONTEXT_SELECTION_AMBIGUOUS");
  assert.equal(snapshot(root), before);
});

test("project phase reports the effective lifecycle contract with no active candidates", async () => {
  const { root } = await packageRepository({ stage: "pr" });
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const change = parseLifecycleYaml(readFileSync(path, "utf8"));
  change.workflow_state.lifecycle_state = "complete";
  writeFileSync(path, serializeLifecycleYaml(change));

  const execution = executeWorkflowContext(["--format", "json"], { cwd: root });

  assert.equal(execution.exitCode, 0);
  assert.equal(execution.result.selection.state, "none");
  assert.deepEqual(execution.result.candidates, []);
  assert.equal(execution.result.lifecycle_contract.contract_class, "stage-owned-change-local-v3");
  assert.equal(execution.result.lifecycle_contract.activation_state, "active");
});

test("change phase composes exact lifecycle, package, milestone, artifact, and automation facts", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const change = parseLifecycleYaml(readFileSync(path, "utf8"));
  change.workflow_state.planned_work = {
    current_milestone: "M1",
    milestones: { M1: { kind: "implementation", state: "implementing" } },
    remaining_implementation_milestones: ["M1"],
  };
  change.workflow.automation = {
    status: "active",
    target: "verify",
    occurrence: "automation-7",
    current_stage: "implement",
    budgets: { correction_cycles: 2 },
    receipts: ["receipt-1"],
    secret: "must-not-leak",
  };
  writeFileSync(path, serializeLifecycleYaml(change));
  const before = snapshot(root);

  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });

  assert.equal(execution.exitCode, 0);
  assert.equal(execution.result.phase, "change");
  assert.equal(execution.result.change_id, "example");
  assert.match(execution.result.lifecycle_revision, /^sha256:[0-9a-f]{64}$/);
  assert.equal(execution.result.current_stage, "implement");
  assert.equal(execution.result.milestones.current_milestone, "M1");
  assert.equal(execution.result.packages.design.status, "review-required");
  assert.ok(execution.result.artifacts.some((item) => item.artifact_id === "spec" && item.path === "specs/example.md"));
  assert.equal(execution.result.automation.occurrence, "automation-7");
  assert.equal("secret" in execution.result.automation, false);
  assert.ok(execution.result.permitted_operations.includes("complete-milestone"));
  assert.equal(snapshot(root), before);
});

test("formal review locations preserve their distinct stage owners", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });
  const locations = Object.fromEntries(execution.result.locations.map((item) => [item.artifact_kind, item]));

  for (const stage of ["proposal-review", "design-review", "delivery-review", "code-review"]) {
    assert.equal(locations[`${stage}-record`].owner, stage);
    assert.match(locations[`${stage}-record`].path_template, new RegExp(`/reviews/${stage}-<review-round>\\.md$`));
  }
  assert.equal(locations["review-records"], undefined);
});

for (const [kind, wrongOwner] of [
  ["proposal-review-record", "code-review"],
  ["design-review-record", "proposal-review"],
  ["delivery-review-record", "design-review"],
  ["code-review-record", "delivery-review"],
]) test(`${kind} rejects a conflicting review owner`, async () => {
  const { root } = await packageRepository({ stage: "implement" });
  writeFileSync(join(root, "rigorloop.workflow.yaml"), `schema_version: 1
artifact_locations:
  ${kind}:
    path_template: docs/changes/<change-id>/reviews/custom-<review-round>.md
    owner: ${wrongOwner}
`);

  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });

  assert.equal(execution.exitCode, 2);
  assert.equal(execution.result.errors[0].code, "RL_CONTEXT_CONFIG_INVALID");
  assert.equal(execution.result.errors[0].artifact_kind, kind);
});

test("project candidates are capped and report truncation without semantic selection", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const original = parseLifecycleYaml(snapshot(root));
  for (let index = 0; index < 40; index += 1) {
    const id = `candidate-${String(index).padStart(2, "0")}`;
    const directory = join(root, "docs", "changes", id);
    mkdirSync(directory, { recursive: true });
    writeFileSync(join(directory, "change.yaml"), serializeLifecycleYaml({ ...original, change_id: id }));
  }

  const execution = executeWorkflowContext(["--format", "json"], { cwd: root });

  assert.equal(execution.result.candidates.length, 32);
  assert.equal(execution.result.candidate_total_count, 41);
  assert.equal(execution.result.candidates_truncated, true);
  assert.equal(execution.result.selection.state, "ambiguous");
  assert.equal(execution.result.selection.selected_change, null);
  assert.ok(JSON.stringify(execution.result).length < 16_384);

  const human = runPublic(root, ["--format", "human"]);
  const humanOutput = `${human.stdout}${human.stderr}`;
  assert.equal(human.status, 2);
  assert.match(humanOutput, /Candidate count: 41/);
  assert.match(humanOutput, /showing 32; use --change <id>/);
});

test("change projections cap milestone, package-member, budget, and receipt collections", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const change = parseLifecycleYaml(readFileSync(path, "utf8"));
  change.workflow_state.planned_work = {
    current_milestone: "M00",
    milestones: Object.fromEntries(Array.from({ length: 40 }, (_, index) => [`M${String(index).padStart(2, "0")}`, { kind: "implementation", state: "planned" }])),
    remaining_implementation_milestones: Array.from({ length: 40 }, (_, index) => `M${String(index).padStart(2, "0")}`),
  };
  mkdirSync(join(root, "docs", "adr"), { recursive: true });
  for (let index = 0; index < 40; index += 1) {
    const id = `adr-${String(index).padStart(2, "0")}`;
    const artifactPath = `docs/adr/${id}.md`;
    writeFileSync(join(root, artifactPath), `# ${id}\n`);
    change.artifact_states[id] = { kind: "adr", role: "supporting", path: artifactPath, lifecycle_state: "review-required" };
    change.lifecycle_cli.artifacts[id] = { artifact_kind: "adr", artifact_role: "supporting", artifact_path: artifactPath };
  }
  change.workflow.automation = {
    status: "active",
    target: "verify",
    budgets: Object.fromEntries(Array.from({ length: 40 }, (_, index) => [`budget-${String(index).padStart(2, "0")}`, index])),
    receipts: Array.from({ length: 40 }, (_, index) => `receipt-${String(index).padStart(2, "0")}`),
  };
  writeFileSync(path, serializeLifecycleYaml(change));

  const result = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root }).result;

  assert.equal(Object.keys(result.milestones.milestones).length, 32);
  assert.equal(result.milestones.total_count, 40);
  assert.equal(result.milestones.truncated, true);
  assert.equal(result.milestones.remaining_implementation_milestones.length, 32);
  assert.equal(Object.keys(result.packages.design.members).length, 32);
  assert.equal(result.packages.design.member_total_count, 43);
  assert.equal(result.packages.design.members_truncated, true);
  assert.equal(Object.keys(result.automation.budgets).length, 32);
  assert.equal(result.automation.budgets_truncated, true);
  assert.equal(result.automation.receipts.length, 32);
  assert.equal(result.automation.receipts_truncated, true);
});

test("invalid lifecycle identifiers fail closed without leaking private values", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const change = parseLifecycleYaml(readFileSync(path, "utf8"));
  change.workflow_state.current_stage = "/private/host/path";
  writeFileSync(path, serializeLifecycleYaml(change));

  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });

  assert.notEqual(execution.exitCode, 0);
  assert.equal(execution.result.current_stage, null);
  assert.equal(execution.result.errors.some((item) => item.code === "RL_CONTEXT_PROJECTION_INVALID"), true);
  assert.doesNotMatch(JSON.stringify(execution.result), /private\/host\/path/);
});

test("exact selection ignores a malformed unrelated governed change", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const unrelated = join(root, "docs", "changes", "unrelated");
  mkdirSync(unrelated, { recursive: true });
  writeFileSync(join(unrelated, "change.yaml"), "not: [valid\n");

  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });

  assert.equal(execution.exitCode, 0);
  assert.equal(execution.result.change_id, "example");
});

test("identical retry, ambiguity, configuration failure, and mutation preserve freshness semantics", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const before = governedSnapshot(root);
  const first = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });
  const second = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });
  assert.deepEqual(second.result, first.result);
  assert.deepEqual(governedSnapshot(root), before);

  const secondDirectory = join(root, "docs", "changes", "second");
  mkdirSync(secondDirectory, { recursive: true });
  const change = parseLifecycleYaml(snapshot(root));
  writeFileSync(join(secondDirectory, "change.yaml"), serializeLifecycleYaml({ ...change, change_id: "second" }));
  const ambiguousBefore = governedSnapshot(root);
  assert.equal(executeWorkflowContext(["--format", "json"], { cwd: root }).result.selection.state, "ambiguous");
  assert.deepEqual(governedSnapshot(root), ambiguousBefore);

  writeFileSync(join(root, "rigorloop.workflow.yaml"), "schema_version: 1\nartifact_locations:\n  unknown: {}\n");
  const failureBefore = governedSnapshot(root);
  assert.equal(executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root }).exitCode, 2);
  assert.deepEqual(governedSnapshot(root), failureBefore);

  writeFileSync(join(root, "rigorloop.workflow.yaml"), "schema_version: 1\nartifact_locations: {}\n");
  change.workflow_state.next_stage = "code-review";
  writeFileSync(join(root, "docs", "changes", "example", "change.yaml"), serializeLifecycleYaml(change));
  const afterMutation = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });
  assert.notEqual(afterMutation.result.lifecycle_revision, first.result.lifecycle_revision);
});

test("non-file configuration is a normalized read failure and does not mutate governed files", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  mkdirSync(join(root, "rigorloop.workflow.yaml"));
  const before = governedSnapshot(root);

  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });

  assert.equal(execution.exitCode, 2);
  assert.equal(execution.result.errors[0].code, "RL_CONTEXT_PATH_UNSAFE");
  assert.deepEqual(governedSnapshot(root), before);
});

test("unexpected repository read failure is normalized without exposing or mutating state", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const before = governedSnapshot(root);

  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], {
    cwd: root,
    beforeRepositoryRead() { throw new Error("/private/host/read-failure"); },
  });

  assert.equal(execution.exitCode, 2);
  assert.equal(execution.result.errors[0].code, "RL_CONTEXT_READ_FAILED");
  assert.doesNotMatch(JSON.stringify(execution.result), /private\/host/);
  assert.deepEqual(governedSnapshot(root), before);
});

test("interrupted public workflow context leaves governed state and its blocking input unchanged", { skip: process.platform === "win32" }, async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const configPath = join(root, "rigorloop.workflow.yaml");
  const before = governedSnapshot(root, false);
  const fifo = spawnSync("mkfifo", [configPath]);
  assert.equal(fifo.status, 0);

  const child = spawn(process.execPath, [cli, "workflow-context", "--change", "example", "--format", "json"], {
    cwd: root,
    env: { ...process.env, RIGORLOOP_FILE_LOG: "off", RIGORLOOP_CONSOLE_LOG_LEVEL: "off" },
    stdio: "ignore",
  });
  await new Promise((resolve) => setTimeout(resolve, 50));
  child.kill("SIGTERM");
  const [code, signal] = await new Promise((resolve) => child.once("exit", (...values) => resolve(values)));

  assert.equal(code, null);
  assert.equal(signal, "SIGTERM");
  assert.equal(lstatSync(configPath).isFIFO(), true);
  assert.deepEqual(governedSnapshot(root, false), before);
  unlinkSync(configPath);
});

test("valid repository overrides replace defaults with explicit provenance", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  writeFileSync(join(root, "rigorloop.workflow.yaml"), `schema_version: 1
artifact_locations:
  change-record:
    path_template: governed/<change-id>/state.yaml
    owner: workflow
`);

  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });
  const location = execution.result.locations.find((item) => item.artifact_kind === "change-record");

  assert.equal(execution.exitCode, 0);
  assert.equal(execution.result.configuration.source, "rigorloop.workflow.yaml");
  assert.equal(location.path, "governed/example/state.yaml");
  assert.equal(location.provenance, "repository-override");
});

for (const [name, yaml, code] of [
  ["unknown schema", "schema_version: 99\nartifact_locations: {}\n", "RL_CONTEXT_CONFIG_UNSUPPORTED"],
  ["unknown top-level key", "schema_version: 1\nartifact_locations: {}\nfuture: true\n", "RL_CONTEXT_CONFIG_INVALID"],
  ["unknown artifact kind", "schema_version: 1\nartifact_locations:\n  future-kind:\n    path_template: docs/future.md\n", "RL_CONTEXT_CONFIG_INVALID"],
  ["escaped path", "schema_version: 1\nartifact_locations:\n  plan:\n    path_template: ../outside.md\n", "RL_CONTEXT_PATH_UNSAFE"],
  ["unknown variable", "schema_version: 1\nartifact_locations:\n  plan:\n    path_template: docs/<future>.md\n", "RL_CONTEXT_CONFIG_INVALID"],
  ["incomplete variable", "schema_version: 1\nartifact_locations:\n  plan:\n    path_template: docs/<review-round>.md\n", "RL_CONTEXT_LOCATION_UNRESOLVED"],
]) test(`${name} configuration fails closed before fallback`, async () => {
  const { root } = await packageRepository({ stage: "implement" });
  writeFileSync(join(root, "rigorloop.workflow.yaml"), yaml);
  const before = snapshot(root);
  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 2);
  assert.equal(execution.result.errors[0].code, code);
  assert.equal(execution.result.errors[0].source, "rigorloop.workflow.yaml");
  assert.equal(snapshot(root), before);
});

test("duplicate resolved ownership and symlink traversal fail closed", async () => {
  const duplicate = await packageRepository({ stage: "implement" });
  writeFileSync(join(duplicate.root, "rigorloop.workflow.yaml"), `schema_version: 1
artifact_locations:
  plan:
    path_template: docs/shared.md
  spec:
    path_template: docs/shared.md
`);
  assert.equal(executeWorkflowContext(["--change", "example"], { cwd: duplicate.root }).result.errors[0].code, "RL_CONTEXT_LOCATION_CONFLICT");

  const linked = await packageRepository({ stage: "implement" });
  mkdirSync(join(linked.root, "outside"));
  symlinkSync(join(linked.root, "outside"), join(linked.root, "linked"));
  writeFileSync(join(linked.root, "rigorloop.workflow.yaml"), `schema_version: 1
artifact_locations:
  plan:
    path_template: linked/plan.md
`);
  assert.equal(executeWorkflowContext(["--change", "example"], { cwd: linked.root }).result.errors[0].code, "RL_CONTEXT_PATH_UNSAFE");
});

test("public human and JSON output share one model and omit absolute repository paths", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const jsonRun = runPublic(root, ["--change", "example", "--format", "json"]);
  const humanRun = runPublic(root, ["--change", "example", "--format", "human"]);
  const json = JSON.parse(jsonRun.stdout);

  assert.equal(jsonRun.status, 0);
  assert.equal(humanRun.status, 0);
  assert.equal(json.command, "workflow-context");
  assert.match(humanRun.stdout, /Workflow context: success/);
  assert.match(humanRun.stdout, /Current stage: implement/);
  assert.match(humanRun.stdout, /Configuration: bundled-default/);
  assert.doesNotMatch(jsonRun.stdout, new RegExp(root.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
  assert.doesNotMatch(humanRun.stdout, new RegExp(root.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")));
});

test("invalid registered paths are redacted from change output", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const change = parseLifecycleYaml(readFileSync(path, "utf8"));
  change.artifact_states.spec.path = "/private/secret/spec.md";
  writeFileSync(path, serializeLifecycleYaml(change));

  const execution = executeWorkflowContext(["--change", "example", "--format", "json"], { cwd: root });
  const spec = execution.result.artifacts.find((item) => item.artifact_id === "spec");

  assert.equal(execution.exitCode, 3);
  assert.equal(spec.path, null);
  assert.doesNotMatch(JSON.stringify(execution.result), /private\/secret/);
});

test("unknown CLI arguments and mutation flags are rejected without repository mutation", async () => {
  const { root } = await packageRepository({ stage: "implement" });
  const before = snapshot(root);
  for (const args of [["--future"], ["--dry-run"], ["--change", "example", "--change", "second"], ["--json", "--format", "human"], ["--change", "example", "--format", "future"]]) {
    const execution = executeWorkflowContext(args, { cwd: root });
    assert.equal(execution.exitCode, 4);
    assert.equal(execution.result.errors[0].code, "RL_CONTEXT_INVALID_REQUEST");
  }
  assert.equal(snapshot(root), before);
});
