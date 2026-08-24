import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";

async function repository(changeIds = ["example"], overrides = {}) {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-lifecycle-read-"));
  for (const changeId of changeIds) {
    const changeRoot = join(root, "docs", "changes", changeId);
    mkdirSync(changeRoot, { recursive: true });
    mkdirSync(join(root, "specs"), { recursive: true });
    const specPath = join(root, "specs", `${changeId}.md`);
    writeFileSync(specPath, `# ${changeId}\n`, "utf8");
    const change = {
      change_id: changeId,
      title: "Example",
      classification: "feature",
      risk: "standard",
      lifecycle_contract: "stage-owned-change-local-v1",
      artifact_states: {
        spec: { kind: "spec", path: `specs/${changeId}.md`, role: "primary", lifecycle_state: "approved" },
      },
      workflow_state: {
        lifecycle_state: "active",
        current_stage: "implement",
        next_stage: "implement",
        blocker: null,
        planned_work: {
          current_milestone: "M1",
          milestones: { M1: { kind: "implementation", state: "implementing" } },
          remaining_implementation_milestones: ["M1"],
        },
      },
      ...overrides,
    };
    writeFileSync(join(changeRoot, "change.yaml"), `${toYaml(change)}\n`, "utf8");
  }
  return root;
}

function toYaml(value, indent = 0) {
  const prefix = " ".repeat(indent);
  if (Array.isArray(value)) return value.map((item) => `${prefix}- ${typeof item === "object" ? `\n${toYaml(item, indent + 2)}` : item}`).join("\n");
  return Object.entries(value).map(([key, child]) => {
    if (child === null) return `${prefix}${key}: null`;
    if (Array.isArray(child)) return child.length ? `${prefix}${key}:\n${toYaml(child, indent + 2)}` : `${prefix}${key}: []`;
    if (typeof child === "object") return `${prefix}${key}:\n${toYaml(child, indent + 2)}`;
    return `${prefix}${key}: ${child}`;
  }).join("\n");
}

test("read commands require an unambiguous governed change", async () => {
  const empty = await repository([]);
  assert.equal(executeLifecycleCli(["status", "--format", "json"], { cwd: empty }).result.errors[0].code, "RL_CHANGE_NOT_FOUND");
  const multiple = await repository(["one", "two"]);
  assert.equal(executeLifecycleCli(["status"], { cwd: multiple }).result.errors[0].code, "RL_AMBIGUOUS_CHANGE");
  assert.equal(executeLifecycleCli(["status", "--change", "two"], { cwd: multiple }).result.change_id, "two");
});

test("status exposes one deterministic result model without writes", async () => {
  const root = await repository();
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const before = readFileSync(path, "utf8");
  const execution = executeLifecycleCli(["status", "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 0);
  assert.deepEqual(Object.keys(execution.result).slice(0, 12), [
    "schema_version", "command", "operation", "status", "change_id", "lifecycle_revision", "effective_state", "blockers", "permitted_operations", "artifacts", "warnings", "errors",
  ]);
  assert.equal(execution.result.effective_state.recorded_state.spec, "approved");
  assert.equal(execution.result.effective_state.evidence_state.spec, "current");
  assert.deepEqual(execution.result.permitted_operations, ["record-validation", "complete-milestone"]);
  assert.equal(readFileSync(path, "utf8"), before);
});

test("context returns bounded stage facts from the shared interpretation", async () => {
  const root = await repository();
  const result = executeLifecycleCli(["context", "code-review", "--format", "json"], { cwd: root }).result;
  assert.equal(result.context.exact_change, "example");
  assert.equal(result.context.target_artifact, null);
  assert.equal(result.context.permitted_registration_operation, "record-review");
  assert.match(result.context.lifecycle_revision, /^sha256:[a-f0-9]{64}$/);
  assert.equal(JSON.stringify(result).includes(root), false);
});

test("validate rejects unsupported contracts and malformed YAML deterministically", async () => {
  const unsupported = await repository(["example"], { lifecycle_contract: "future-v9" });
  const incompatible = executeLifecycleCli(["validate"], { cwd: unsupported });
  assert.equal(incompatible.exitCode, 4);
  assert.equal(incompatible.result.errors[0].code, "RL_UNSUPPORTED_SCHEMA");
  const malformed = await repository();
  writeFileSync(join(malformed, "docs", "changes", "example", "change.yaml"), "change_id: example\nchange_id: duplicate\n", "utf8");
  assert.equal(executeLifecycleCli(["validate", "--change", "example"], { cwd: malformed }).result.errors[0].code, "RL_INVALID_REQUEST");
});
