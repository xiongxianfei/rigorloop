import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

import {
  LIFECYCLE_OPERATIONS,
  canonicalJson,
  lifecycleRevision,
  parseLifecycleYaml,
  serializeLifecycleYaml,
  validateLifecycleRequest,
} from "../dist/lib/lifecycle-contract.js";

const fixture = JSON.parse(
  readFileSync(join(import.meta.dirname, "fixtures", "lifecycle", "conformance-v1.json"), "utf8"),
);
const validChange = fixture.valid_yaml;

test("closed lifecycle operation vocabulary rejects an unknown operation", () => {
  assert.deepEqual([...LIFECYCLE_OPERATIONS], [
    "record-review",
    "record-validation",
    "record-finding-resolution",
    "settle-artifact",
    "start-milestone",
    "complete-milestone",
    "migrate",
    "repair",
  ]);
  const result = validateLifecycleRequest({
    schema_version: 1,
    operation: "set-status",
    change_id: "example",
    expected_lifecycle_revision: "sha256:abc",
  });
  assert.equal(result.ok, false);
  assert.equal(result.errors[0].code, "RL_INVALID_REQUEST");
});

test("request schema rejects unknown fields before operation consistency", () => {
  const result = validateLifecycleRequest({
    schema_version: 1,
    operation: "settle-artifact",
    change_id: "example",
    expected_lifecycle_revision: "sha256:abc",
    artifact_id: "spec",
    target_state: "approved",
  });
  assert.equal(result.ok, false);
  assert.match(result.errors[0].summary, /unknown field target_state/);
});

for (const entry of fixture.invalid_yaml) {
  test(`YAML parser rejects ${entry.id}`, () => {
    assert.throws(() => parseLifecycleYaml(entry.source), /RL_INVALID_REQUEST/);
  });
}

test("YAML parser accepts the lifecycle subset and serializer is deterministic", () => {
  const parsed = parseLifecycleYaml(validChange);
  assert.equal(parsed.change_id, "example");
  const first = serializeLifecycleYaml(parsed);
  const second = serializeLifecycleYaml(parseLifecycleYaml(first));
  assert.equal(first, second);
  assert.equal(first.endsWith("\n"), true);
  assert.equal(first.includes("\r"), false);
});

test("canonical JSON sorts object keys recursively", () => {
  assert.equal(canonicalJson({ z: 1, a: { y: 2, b: 3 } }), '{"a":{"b":3,"y":2},"z":1}');
});

test("lifecycle revision includes sorted referenced identities", () => {
  const change = parseLifecycleYaml(validChange);
  const left = lifecycleRevision(change, [
    { path: "specs/b.md", sha256: "b" },
    { path: "specs/a.md", sha256: "a" },
  ]);
  const right = lifecycleRevision(change, [
    { path: "specs/a.md", sha256: "a" },
    { path: "specs/b.md", sha256: "b" },
  ]);
  assert.equal(left, right);
  assert.match(left, /^sha256:[a-f0-9]{64}$/);
});
