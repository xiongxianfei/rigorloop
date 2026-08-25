import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml } from "../dist/lib/lifecycle-contract.js";
import { lifecycleTransactionPaths } from "../dist/lib/lifecycle-transaction.js";

async function fixture() {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-lifecycle-migrate-"));
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(changeRoot, { recursive: true });
  mkdirSync(join(root, "specs"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  writeFileSync(join(root, "specs", "example.md"), "# Example specification\n", "utf8");
  const changePath = join(changeRoot, "change.yaml");
  writeFileSync(changePath, `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v1
artifact_states:
  spec:
    kind: spec
    role: primary
    path: specs/example.md
    lifecycle_state: approved
workflow_state:
  lifecycle_state: active
  current_stage: implement
  next_stage: implement
  blocker: null
  evidence: []
`, "utf8");
  return { root, changeRoot, changePath };
}

function revision(root) { return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.lifecycle_revision; }
function request(root, name, body) { const path = `requests/${name}.json`; writeFileSync(join(root, path), JSON.stringify(body), "utf8"); return path; }

test("migration supports only the enumerated legacy coordination schema", async () => {
  const { root, changePath } = await fixture();
  const path = request(root, "migrate", { schema_version: 1, operation: "migrate", change_id: "example", expected_lifecycle_revision: revision(root), source_schema_version: 1, stage_authority: "workflow" });
  assert.equal(executeLifecycleCli(["migrate", "--request", path, "--dry-run"], { cwd: root }).exitCode, 0);
  assert.doesNotMatch(readFileSync(changePath, "utf8"), /lifecycle_cli/);
  assert.equal(executeLifecycleCli(["migrate", "--request", path], { cwd: root }).exitCode, 0);
  assert.match(readFileSync(changePath, "utf8"), /lifecycle_cli:\n\s+schema_version: 1/);
  const registration = parseLifecycleYaml(readFileSync(changePath, "utf8")).lifecycle_cli.artifacts.spec;
  assert.equal(registration.artifact_path, "specs/example.md");
  assert.match(registration.artifact_sha256, /^[a-f0-9]{64}$/);
  assert.equal(registration.stage_authority, "spec");
});

test("migration rejects an ambiguous legacy artifact without changing bytes", async () => {
  const { root, changePath } = await fixture();
  writeFileSync(changePath, readFileSync(changePath, "utf8").replace("kind: spec", "kind: unknown"), "utf8");
  const before = readFileSync(changePath);
  const path = request(root, "ambiguous-migrate", { schema_version: 1, operation: "migrate", change_id: "example", expected_lifecycle_revision: revision(root), source_schema_version: 1, stage_authority: "workflow" });
  const result = executeLifecycleCli(["migrate", "--request", path, "--format", "json"], { cwd: root });
  assert.notEqual(result.exitCode, 0);
  assert.equal(result.result.errors[0].code, "RL_UNSUPPORTED_SCHEMA");
  assert.deepEqual(readFileSync(changePath), before);
});

test("clear-orphaned-lock repair requires explicit condition and preserves change bytes", async () => {
  const { root, changePath } = await fixture();
  const before = readFileSync(changePath);
  const paths = lifecycleTransactionPaths(changePath);
  writeFileSync(paths.lock, JSON.stringify({ schema_version: 1, change_id: "example", pid: 99999999, nonce: "dead" }), { mode: 0o600 });
  const path = request(root, "repair", { schema_version: 1, operation: "repair", change_id: "example", expected_lifecycle_revision: revision(root), condition: "clear-orphaned-lock", stage_authority: "workflow", dry_run_acknowledgement: true });
  const dry = executeLifecycleCli(["repair", "--request", path, "--dry-run", "--format", "json"], { cwd: root });
  assert.equal(dry.result.mutation.observed_state, "orphaned");
  assert.equal(executeLifecycleCli(["repair", "--request", path], { cwd: root }).exitCode, 0);
  assert.deepEqual(readFileSync(changePath), before);
});
