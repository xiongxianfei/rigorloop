import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

import {
  LIFECYCLE_OPERATIONS,
  PROVENANCE_EXCLUDED_FIELDS,
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
    "record-artifact-revision",
    "record-review",
    "record-validation",
    "record-finding-resolution",
    "settle-artifact",
    "start-milestone",
    "complete-milestone",
    "route-correction",
    "return-correction",
    "withdraw-artifact-registration",
    "migrate",
    "repair",
  ]);
  const result = validateLifecycleRequest({
    schema_version: 1,
    operation: "set-status",
    change_id: "example",
    expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
  });
  assert.equal(result.ok, false);
  assert.equal(result.errors[0].code, "RL_INVALID_REQUEST");
});

test("request schema rejects unknown fields before operation consistency", () => {
  const result = validateLifecycleRequest({
    schema_version: 1,
    operation: "settle-artifact",
    change_id: "example",
    expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
    artifact_id: "spec",
    target_state: "approved",
  });
  assert.equal(result.ok, false);
  assert.match(result.errors[0].summary, /unknown field target_state/);
});

const operationRequests = {
  "record-artifact-revision": { artifact_id: "spec", artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", evidence_path: "evidence/spec-authoring.md", stage_authority: "spec" },
  "record-review": { artifact_id: "spec", evidence_path: "reviews/spec-review-r1.md", stage_authority: "spec-review" },
  "record-validation": { artifact_id: "spec", evidence_path: "evidence/validation.md", subject_path: "specs/example.md", stage_authority: "verify" },
  "record-finding-resolution": { artifact_id: "spec", evidence_path: "review-resolution.md", finding_id: "F-1", stage_authority: "review-resolution" },
  "settle-artifact": { artifact_id: "spec", stage_authority: "spec-review" },
  "start-milestone": { milestone_id: "M1", stage_authority: "workflow" },
  "complete-milestone": { milestone_id: "M1", evidence_path: "evidence/m1.md", stage_authority: "workflow" },
  "route-correction": { source_stage: "verify", destination_stage: "test-spec", destination_artifact_id: "test-spec", reason: "upstream-proof-gap", evidence_path: "evidence/correction-route.md", finding_ids: ["F-1"], return_stage: "verify", stage_authority: "workflow" },
  "return-correction": { route_id: "route-1", evidence_path: "evidence/correction-return.md", stage_authority: "workflow" },
  "withdraw-artifact-registration": { artifact_id: "architecture", artifact_path: "docs/architecture/example.md", canonical_owner_change_id: "canonical-change", reason: "duplicate-registration", evidence_path: "evidence/withdrawal.md", stage_authority: "workflow" },
  migrate: { source_schema_version: 1, stage_authority: "workflow" },
  repair: { condition: "reconcile-interrupted-replace", stage_authority: "workflow", dry_run_acknowledgement: true },
};

for (const operation of LIFECYCLE_OPERATIONS) {
  test(`${operation} enforces its required request fields`, () => {
    const request = {
      schema_version: 1,
      operation,
      change_id: "example",
      expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
      ...operationRequests[operation],
    };
    assert.equal(validateLifecycleRequest(request).ok, true);
    const requiredField = Object.keys(operationRequests[operation])[0];
    delete request[requiredField];
    const result = validateLifecycleRequest(request);
    assert.equal(result.ok, false);
    assert.match(result.errors[0].summary, new RegExp(requiredField));
  });
}

test("operation authority and repair condition vocabularies fail closed", () => {
  const base = {
    schema_version: 1,
    operation: "repair",
    change_id: "example",
    expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
    condition: "rewrite-anything",
    stage_authority: "administrator",
    dry_run_acknowledgement: true,
  };
  const condition = validateLifecycleRequest(base);
  assert.equal(condition.ok, false);
  assert.match(condition.errors[0].summary, /condition/);
  const authority = validateLifecycleRequest({ ...base, condition: "clear-orphaned-lock" });
  assert.equal(authority.ok, false);
  assert.match(authority.errors[0].summary, /stage_authority/);
});

test("correction and withdrawal vocabularies fail closed before consistency", () => {
  const route = {
    schema_version: 1,
    operation: "route-correction",
    change_id: "example",
    expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
    ...operationRequests["route-correction"],
  };
  assert.match(validateLifecycleRequest({ ...route, reason: "fix-it" }).errors[0].summary, /reason/);
  assert.match(validateLifecycleRequest({ ...route, destination_stage: "implementation" }).errors[0].summary, /destination_stage/);
  assert.match(validateLifecycleRequest({ ...route, finding_ids: ["F-1", "F-1"] }).errors[0].summary, /finding_ids/);
  const withdrawal = {
    schema_version: 1,
    operation: "withdraw-artifact-registration",
    change_id: "example",
    expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
    ...operationRequests["withdraw-artifact-registration"],
  };
  const unknownWithdrawalReason = validateLifecycleRequest({ ...withdrawal, reason: "cleanup" });
  assert.equal(unknownWithdrawalReason.errors[0].code, "RL_WITHDRAWAL_UNSAFE");
  assert.match(unknownWithdrawalReason.errors[0].summary, /reason/);
});

test("request provenance uses the closed version-one vocabulary", () => {
  const request = {
    schema_version: 1,
    operation: "settle-artifact",
    change_id: "example",
    expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
    artifact_id: "spec",
    stage_authority: "spec-review",
    actor: "review-agent",
    recorded_at: "2026-08-24T21:15:00+01:00",
  };
  assert.equal(validateLifecycleRequest(request).ok, true);
  assert.match(validateLifecycleRequest({ ...request, actor: " " }).errors[0].summary, /actor/);
  assert.match(validateLifecycleRequest({ ...request, recorded_at: "24 August" }).errors[0].summary, /recorded_at/);
  assert.match(validateLifecycleRequest({ ...request, recorded_at: "2026-02-31T21:15:00Z" }).errors[0].summary, /recorded_at/);
  assert.match(validateLifecycleRequest({ ...request, recorded_at: "2026-08-24T21:15:00+25:00" }).errors[0].summary, /recorded_at/);
  assert.match(validateLifecycleRequest({ ...request, provenance: "hidden" }).errors[0].summary, /unknown field provenance/);
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

test("lifecycle revision excludes only the versioned provenance fields", () => {
  assert.deepEqual([...PROVENANCE_EXCLUDED_FIELDS], fixture.provenance_excluded_fields);
  const change = parseLifecycleYaml(validChange);
  const baseline = lifecycleRevision(change);
  assert.equal(lifecycleRevision({ ...change, actor: "agent", recorded_at: "2026-08-24T20:00:00Z" }), baseline);
  assert.notEqual(
    lifecycleRevision({ ...change, workflow_state: { ...change.workflow_state, current_stage: "architecture" } }),
    baseline,
  );
});
