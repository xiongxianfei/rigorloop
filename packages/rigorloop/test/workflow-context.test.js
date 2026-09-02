import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, readFileSync, symlinkSync, writeFileSync } from "node:fs";
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
