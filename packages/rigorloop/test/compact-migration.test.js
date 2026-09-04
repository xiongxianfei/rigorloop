import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { test } from "node:test";

const cli = new URL("../dist/bin/rigorloop.js", import.meta.url).pathname;

test("legacy changes remain readable by legacy tooling but compact projection and writes reject without migration", async () => {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-legacy-"));
  mkdirSync(join(root, "docs/changes/legacy"), { recursive: true });
  writeFileSync(join(root, "docs/changes/legacy/change.yaml"), "schema_version: 3\nchange_id: legacy\ntitle: Legacy\nlifecycle_contract: stage-owned-change-local-v3\n");
  const projected = spawnSync(process.execPath, [cli, "compact", "project", "--change", "legacy", "--view", "summary", "--format", "json"], { cwd: root, encoding: "utf8" });
  assert.equal(projected.status, 4);
  assert.match(projected.stdout, /RL_UNSUPPORTED_CONTRACT/);
  const migration = { schema: "compact-operation-v1", operation: "migrate-change", change_id: "legacy", expected_lifecycle_revision: `sha256:${"a".repeat(64)}`, expected_files: {}, payload: {} };
  const applied = spawnSync(process.execPath, [cli, "compact", "apply", "--request-json", JSON.stringify(migration), "--format", "json"], { cwd: root, encoding: "utf8" });
  assert.equal(applied.status, 2);
  assert.match(applied.stdout, /unknown_value migrate-change/);
});
