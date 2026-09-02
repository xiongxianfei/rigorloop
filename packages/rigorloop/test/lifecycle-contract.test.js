import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

import {
  LIFECYCLE_CONTRACT_V1,
  LIFECYCLE_CONTRACT_V2,
  LIFECYCLE_CONTRACT_V3,
  LIFECYCLE_OPERATIONS,
  PROVENANCE_EXCLUDED_FIELDS,
  canonicalJson,
  allowedArtifactKinds,
  allowedNextStages,
  classifyLifecycleContract,
  lifecycleRevision,
  parseLifecycleYaml,
  serializeLifecycleYaml,
  validateLifecycleActivationManifest,
  validateFinalVerificationActivationManifest,
  validateLifecycleRequest,
  verificationCorrectionOwner,
} from "../dist/lib/lifecycle-contract.js";
import { LIFECYCLE_OPERATIONS as OBSERVABLE_LIFECYCLE_OPERATIONS } from "../dist/lib/diagnostic-event.js";

const fixture = JSON.parse(
  readFileSync(join(import.meta.dirname, "fixtures", "lifecycle", "conformance-v1.json"), "utf8"),
);
const validChange = fixture.valid_yaml;
const classificationFixture = JSON.parse(
  readFileSync(join(import.meta.dirname, "fixtures", "lifecycle", "contract-classification-v1.json"), "utf8"),
);
const finalVerificationClassificationFixture = JSON.parse(
  readFileSync(join(import.meta.dirname, "fixtures", "lifecycle", "final-verification-contract-classification-v1.json"), "utf8"),
);

test("final verification preactivation keeps v3 inactive and non-v3 historical", () => {
  const currentManifest = classificationFixture.active_manifest;
  const finalManifest = finalVerificationClassificationFixture.preactivation_manifest;
  assert.deepEqual(validateFinalVerificationActivationManifest(finalManifest), []);
  assert.deepEqual(
    classifyLifecycleContract("new-v3", { lifecycle_contract: LIFECYCLE_CONTRACT_V3 }, currentManifest, finalManifest),
    { contract_class: LIFECYCLE_CONTRACT_V3, activation_state: "preactivation", authority: "inactive" },
  );
  assert.deepEqual(
    classifyLifecycleContract("new-v2", { lifecycle_contract: LIFECYCLE_CONTRACT_V2 }, currentManifest, finalManifest),
    { contract_class: LIFECYCLE_CONTRACT_V2, activation_state: "historical", authority: "historical" },
  );
  assert.deepEqual(allowedNextStages({ lifecycle_contract: LIFECYCLE_CONTRACT_V3 }, "proposal"), ["proposal-review"]);
  assert.deepEqual(allowedArtifactKinds({ lifecycle_contract: LIFECYCLE_CONTRACT_V3 }), ["proposal", "spec", "architecture", "adr", "plan"]);
  assert.deepEqual(allowedNextStages({ lifecycle_contract: LIFECYCLE_CONTRACT_V2 }, "proposal"), []);
  assert.deepEqual(allowedArtifactKinds({ lifecycle_contract: LIFECYCLE_CONTRACT_V2 }), []);
});

test("active final verification manifest activates v3 without a historical allowlist", () => {
  const currentManifest = classificationFixture.active_manifest;
  const finalManifest = finalVerificationClassificationFixture.active_manifest;
  assert.deepEqual(validateFinalVerificationActivationManifest(finalManifest), []);
  assert.equal(
    classifyLifecycleContract("new-v3", { lifecycle_contract: LIFECYCLE_CONTRACT_V3 }, currentManifest, finalManifest).authority,
    "active",
  );
  assert.deepEqual(
    classifyLifecycleContract("v2", { lifecycle_contract: LIFECYCLE_CONTRACT_V2 }, currentManifest, finalManifest),
    { contract_class: LIFECYCLE_CONTRACT_V2, activation_state: "historical", authority: "historical" },
  );
  assert.deepEqual(
    classifyLifecycleContract("unlisted-v2", { lifecycle_contract: LIFECYCLE_CONTRACT_V2 }, currentManifest, finalManifest),
    { contract_class: LIFECYCLE_CONTRACT_V2, activation_state: "historical", authority: "historical" },
  );
});

test("final verification manifest and v3 explain-change values fail closed", () => {
  const currentManifest = classificationFixture.active_manifest;
  const finalManifest = structuredClone(finalVerificationClassificationFixture.active_manifest);
  finalManifest.changes.push({ change_id: "old", contract_class: "stage-owned-change-local-v1" });
  assert.match(validateFinalVerificationActivationManifest(finalManifest)[0], /changes must be empty/);
  for (const change of [
    { lifecycle_contract: LIFECYCLE_CONTRACT_V3, workflow_state: { current_stage: "explain-change" } },
    { lifecycle_contract: LIFECYCLE_CONTRACT_V3, artifacts: { explain_change: "docs/changes/example/explain-change.md" } },
  ]) {
    assert.throws(
      () => classifyLifecycleContract("new-v3", change, currentManifest, finalVerificationClassificationFixture.preactivation_manifest),
      /v3 lifecycle contract carries active explain-change state/,
    );
  }
});

test("verification findings map to exact owners and unknown kinds fail closed", () => {
  assert.deepEqual(Object.fromEntries([
    "system-requirement-gap",
    "technical-realization-gap",
    "verification-allocation-gap",
    "implementation-defect",
    "stale-or-incomplete-review",
    "ci-or-environment-gap",
    "external-evidence-gap",
  ].map((kind) => [kind, verificationCorrectionOwner(kind)])), {
    "system-requirement-gap": "spec",
    "technical-realization-gap": "architecture",
    "verification-allocation-gap": "plan",
    "implementation-defect": "implement",
    "stale-or-incomplete-review": "code-review",
    "ci-or-environment-gap": "ci-maintenance",
    "external-evidence-gap": "external-evidence-acquisition",
  });
  assert.throws(() => verificationCorrectionOwner("maybe"), /unknown_value maybe/);
});

test("final verification manifest rejects every historical progression allowlist entry", () => {
  const active = finalVerificationClassificationFixture.active_manifest;
  for (const contractClass of [LIFECYCLE_CONTRACT_V1, LIFECYCLE_CONTRACT_V2, "future-v9"]) {
    const candidate = structuredClone(active);
    candidate.changes.push({ change_id: "old", contract_class: contractClass });
    assert.match(validateFinalVerificationActivationManifest(candidate)[0], /changes must be empty/);
  }
});

test("contract activation manifest classifies v2 and exact prior records", () => {
  const manifest = classificationFixture.active_manifest;
  assert.deepEqual(validateLifecycleActivationManifest(manifest), []);
  assert.equal(classifyLifecycleContract("new-v2", { lifecycle_contract: LIFECYCLE_CONTRACT_V2 }, manifest).contract_class, LIFECYCLE_CONTRACT_V2);
  assert.equal(classifyLifecycleContract("v1", { lifecycle_contract: LIFECYCLE_CONTRACT_V1 }, manifest).contract_class, LIFECYCLE_CONTRACT_V1);
  assert.equal(classifyLifecycleContract("legacy", {}, manifest).contract_class, "legacy-unversioned");
});

test("legacy activation manifest remains structurally validated but grants no current progression", () => {
  const manifest = classificationFixture.active_manifest;
  assert.equal(classifyLifecycleContract("missing", { lifecycle_contract: LIFECYCLE_CONTRACT_V1 }, manifest).authority, "historical");
  assert.equal(classifyLifecycleContract("legacy", { lifecycle_contract: LIFECYCLE_CONTRACT_V1 }, manifest).authority, "historical");
  const duplicate = structuredClone(manifest);
  duplicate.changes.splice(1, 0, structuredClone(duplicate.changes[0]));
  assert.match(validateLifecycleActivationManifest(duplicate)[0], /duplicate/);
  const unsorted = structuredClone(manifest);
  [unsorted.changes[0], unsorted.changes[1]] = [unsorted.changes[1], unsorted.changes[0]];
  assert.match(validateLifecycleActivationManifest(unsorted)[0], /raw UTF-8 byte order/);
});

test("unknown_value contract and manifest class fail before consistency checks", () => {
  const manifest = structuredClone(classificationFixture.active_manifest);
  manifest.changes[0].contract_class = "future-v9";
  manifest.changes.push(structuredClone(manifest.changes[0]));
  assert.match(validateLifecycleActivationManifest(manifest)[0], /unknown_value.*future-v9/);
  assert.throws(
    () => classifyLifecycleContract("missing", { lifecycle_contract: "future-v9" }, classificationFixture.active_manifest),
    /unknown_value.*future-v9/,
  );
  const explicitNull = classificationFixture.contract_cases.explicit_null;
  assert.throws(
    () => classifyLifecycleContract(explicitNull.change_id, explicitNull.change, classificationFixture.active_manifest),
    new RegExp(explicitNull.error),
  );
});

test("unknown_value activation state fails before manifest consistency checks", () => {
  const manifest = structuredClone(classificationFixture.active_manifest);
  manifest.state = "published";
  manifest.changes.push(structuredClone(manifest.changes[0]));
  assert.match(validateLifecycleActivationManifest(manifest)[0], /state: unknown_value published/);
});

test("v2 contract remains readable history regardless of retired stage state", () => {
  for (const change of [
    {
      lifecycle_contract: LIFECYCLE_CONTRACT_V2,
      workflow_state: { current_stage: "test-spec" },
    },
    {
      lifecycle_contract: LIFECYCLE_CONTRACT_V2,
      lifecycle_cli: { reviews: { "test-spec": { stage_authority: "test-spec-review" } } },
    },
  ]) {
    assert.deepEqual(
      classifyLifecycleContract("new-v2", change, classificationFixture.active_manifest),
      { contract_class: LIFECYCLE_CONTRACT_V2, activation_state: "historical", authority: "historical" },
    );
  }
});

test("contract classification ignores heuristic dates stages artifacts git and network facts", () => {
  const baseline = classifyLifecycleContract("v1", { lifecycle_contract: LIFECYCLE_CONTRACT_V1 }, classificationFixture.active_manifest);
  const changed = classifyLifecycleContract("v1", {
    lifecycle_contract: LIFECYCLE_CONTRACT_V1,
    created_at: "2999-01-01",
    workflow_state: { current_stage: "implement" },
    artifacts: { plan: "docs/plans/example.md" },
    git_reachable: false,
    network_available: false,
  }, classificationFixture.active_manifest);
  assert.deepEqual(changed, baseline);
});

test("closed lifecycle operation vocabulary rejects an unknown operation", () => {
  assert.deepEqual([...LIFECYCLE_OPERATIONS], [
    "record-artifact-revision",
    "record-review",
    "record-validation",
    "record-finding-resolution",
    "settle-artifact",
    "record-package-review",
    "settle-review-package",
    "advance-stage",
    "initialize-approved-plan",
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
  assert.equal(OBSERVABLE_LIFECYCLE_OPERATIONS.includes("initialize-approved-plan"), true);
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
  "record-review": { artifact_id: "proposal", evidence_path: "reviews/proposal-review-r1.md", stage_authority: "proposal-review" },
  "record-validation": { artifact_id: "spec", evidence_path: "evidence/validation.md", subject_path: "specs/example.md", stage_authority: "verify" },
  "record-finding-resolution": { artifact_id: "spec", evidence_path: "review-resolution.md", finding_id: "F-1", stage_authority: "review-resolution" },
  "settle-artifact": { artifact_id: "proposal", stage_authority: "proposal-review" },
  "record-package-review": { package_kind: "design", members: { architecture: "docs/architecture/example.md", spec: "specs/example.md" }, upstream_review_id: "proposal-review-r1", evidence_path: "reviews/design-review-r1.md", stage_authority: "design-review" },
  "settle-review-package": { package_kind: "design", review_id: "design-review-r1", stage_authority: "design-review" },
  "advance-stage": { source_stage: "spec-review", destination_stage: "architecture", stage_authority: "workflow" },
  "initialize-approved-plan": { artifact_id: "plan", stage_authority: "plan" },
  "start-milestone": { milestone_id: "M1", stage_authority: "workflow" },
  "complete-milestone": { milestone_id: "M1", evidence_path: "evidence/m1.md", stage_authority: "workflow" },
  "route-correction": { source_stage: "verify", destination_stage: "spec", destination_artifact_id: "spec", reason: "system-requirement-gap", evidence_path: "evidence/correction-route.md", finding_ids: ["F-1"], return_stage: "verify", stage_authority: "workflow" },
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

test("package request vocabularies fail closed before consistency", () => {
  const base = {
    schema_version: 1,
    operation: "record-package-review",
    change_id: "example",
    expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
    ...operationRequests["record-package-review"],
  };
  assert.match(validateLifecycleRequest({ ...base, package_kind: "combined" }).errors[0].summary, /package_kind/);
  assert.match(validateLifecycleRequest({ ...base, stage_authority: "spec-review" }).errors[0].summary, /stage_authority/);
  assert.match(validateLifecycleRequest({ ...base, members: { spec: "../escape.md" } }).errors[0].summary, /members/);
  assert.match(validateLifecycleRequest({ ...base, upstream_review_id: "bad review" }).errors[0].summary, /upstream_review_id/);
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
    artifact_id: "proposal",
    stage_authority: "proposal-review",
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

test("retired artifact review authorities fail closed", () => {
  for (const stage_authority of ["spec-review", "architecture-review", "plan-review", "test-spec-review", "code-review"]) {
    for (const operation of ["record-review", "settle-artifact"]) {
      const result = validateLifecycleRequest({
        schema_version: 1,
        operation,
        change_id: "example",
        expected_lifecycle_revision: `sha256:${"a".repeat(64)}`,
        artifact_id: "proposal",
        ...(operation === "record-review" ? { evidence_path: "reviews/proposal-review-r1.md" } : {}),
        stage_authority,
      });
      assert.equal(result.ok, false);
      assert.match(result.errors[0].summary, /stage_authority/);
    }
  }
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
