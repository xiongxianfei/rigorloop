import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { test } from "node:test";

import {
  COMPACT_SCHEMA_IDS,
  COMPACT_VOCABULARIES,
  compactLifecycleRevision,
  parseCompactMarkdown,
  parseCompactYaml,
  validateCompactRecord,
  validateCompactSet,
  validateCompactVocabulary,
} from "../dist/lib/compact-contract.js";
import { serializeLifecycleYaml } from "../dist/lib/lifecycle-contract.js";

const digest = (value) => `sha256:${createHash("sha256").update(value).digest("hex")}`;
const d = `sha256:${"a".repeat(64)}`;

function compactChange() {
  return {
    schema: "compact-change-v1",
    change_id: "example",
    title: "Example",
    lifecycle_contract: "compact-current-state-v1",
    lifecycle_revision: d,
    current_stage: "proposal",
    artifacts: {},
    reviews: {},
    active_work: null,
    open_findings: {},
    material_decisions: {},
    evidence: {},
    blockers: [],
    remaining_work: {},
    readiness: "not-ready",
  };
}

const subject = { subject_id: "spec", path: "specs/example.md", identity: d };
const diagnostic = { code: "RL_BLOCKED", summary: "Blocked", invariant: "current-state", scope: "progression", operation: null, identities: [], next_operation: null };
const projection = {
  view: "summary",
  change_id: "example",
  lifecycle_contract: "compact-current-state-v1",
  lifecycle_revision: d,
  current_stage: "proposal",
  artifacts: {},
  reviews: {},
  open_findings: {},
  material_decisions: {},
  evidence: {},
  active_work: null,
  progression_status: "ready",
  blockers: [],
  remaining_work: {},
  permitted_operations: [],
  requested_operation: null,
  operation_eligibility: null,
  required_paths: [],
};

function operationPayloads() {
  const artifact = { artifact_id: "spec", kind: "spec", role: "primary", path: "specs/example.md", identity: d, owner: "spec", status: "approved" };
  const input = (path) => ({ path, identity: digest("content\n"), source: "inline", content: "content\n", source_path: null });
  const resolution = { finding_id: "F1", disposition: "accepted", materiality: "non-material", decision_id: null };
  return {
    "record-artifact": { artifact, content: input("specs/example.md") },
    "advance-stage": { from_stage: "proposal", to_stage: "proposal-review" },
    "replace-review": { target_id: "proposal", prior_review_identity: null, review: input("docs/changes/example/reviews/proposal-review.md"), resolutions: {} },
    "settle-review": { target_id: "proposal", review_id: "review-1", outcome: "approved" },
    "resolve-finding": { resolution, review: input("docs/changes/example/reviews/code-review-M1.md"), decisions: null },
    "upsert-decision": { decision_id: "D1", decisions: input("docs/changes/example/material-decisions.md") },
    "remove-decision": { decision_id: "D1" },
    "route-correction": { correction: { finding_ids: ["F1"], source_stage: "code-review", destination_stage: "implement", return_stage: "code-review", owner: "implement", reason: "implementation-defect", return_condition: "Correct F1", expected_review_target: "M1" } },
    "return-correction": { finding_ids: ["F1"], return_stage: "code-review", satisfied_condition: "F1 corrected" },
    "advance-milestone": { milestone_id: "M1", from_status: "implementing", to_status: "review-required" },
    "update-evidence": { evidence_ids: ["EV1"], evidence: input("docs/changes/example/evidence.yaml") },
    "invalidate-evidence": { evidence_ids: ["EV1"], reason: "subject-changed", evidence: null },
    "record-verify": { verification_id: "verify-1", report: input("docs/changes/example/verify-report.md"), evidence_ids: ["EV1"] },
    recover: { transaction_id: "tx-1", expected_recovery_identity: d, action: "restore-prior" },
  };
}

function schemaFixtures() {
  return [
    compactChange(),
    {
      schema: "compact-review-v1", review_id: "review-1", target: { target_id: "proposal", target_kind: "proposal" }, round: 1,
      subjects: { spec: subject }, reviewer_authority: "proposal-review", outcome: "approved", recording_status: "recorded",
      open_findings: {}, material_decisions: [], limitations: [], recorded_at: "2026-09-04T00:00:00Z",
    },
    {
      schema: "compact-decisions-v1",
      decisions: { D1: { decision_id: "D1", source: { kind: "finding", id: "F1" }, decision: "Keep the boundary", rationale: "It preserves authority", affected_surfaces: ["CLI"], owner: "architecture", applicability: "applicable", applicable_since: d } },
    },
    {
      schema: "compact-evidence-v1",
      evidence: { EV1: { evidence_id: "EV1", verifies: ["SR-01"], subjects: { spec: subject }, method: "node --test", outcome: "passed", surfaces: ["contract"], freshness: "current", invalidating_dependencies: [{ kind: "subject", id: "spec", identity: d }], producer_authority: "implement", detail_location: null, required_rerun: null } },
    },
    {
      schema: "compact-verify-v1", verification_id: "verify-1", subjects: { spec: subject }, verdict: "passed", impact: "standard",
      evidence_reused: ["EV1"], evidence_rerun: [], limitations: [], residual_risks: [], explanation: "The exact subject passed.", handoff: "ready", recorded_at: "2026-09-04T00:00:00Z",
    },
    {
      schema: "compact-operation-v1", operation: "advance-stage", change_id: "example", expected_lifecycle_revision: d,
      expected_files: {}, payload: { from_stage: "proposal", to_stage: "proposal-review" },
    },
    {
      schema: "compact-result-v1", status: "success", change_id: "example", prior_lifecycle_revision: null, resulting_lifecycle_revision: null,
      affected_paths: [], bytes_changed: false, blockers: [], errors: [], next_operation: null, projection,
    },
    {
      schema: "compact-recovery-v1", transaction_id: "tx-1", change_id: "example", phase: "prepared", prior_lifecycle_revision: d,
      candidate_lifecycle_revision: `sha256:${"b".repeat(64)}`, affected_files: [{ path: "docs/changes/example/change.yaml", prior_state: "present", prior_identity: d, prior_content: ".rigorloop/transactions/example/prior/change", candidate_state: "present", candidate_identity: `sha256:${"b".repeat(64)}`, candidate_content: ".rigorloop/transactions/example/candidate/change", replacement_status: "pending" }],
    },
  ];
}

test("compact schema identities and every closed vocabulary reject unknown_value", () => {
  assert.deepEqual(COMPACT_SCHEMA_IDS, [
    "compact-change-v1",
    "compact-review-v1",
    "compact-decisions-v1",
    "compact-evidence-v1",
    "compact-verify-v1",
    "compact-operation-v1",
    "compact-result-v1",
    "compact-recovery-v1",
  ]);
  for (const name of Object.keys(COMPACT_VOCABULARIES)) {
    assert.throws(() => validateCompactVocabulary(name, "unknown_value"), new RegExp(`${name}: unknown_value`));
  }
  assert.throws(() => validateCompactVocabulary("unknown_vocabulary", "x"), /vocabulary: unknown_value/);
});

test("compact change validates exact fields and rejects unknown fields before consistency", () => {
  assert.deepEqual(validateCompactRecord(compactChange()), compactChange());
  assert.throws(() => validateCompactRecord({ ...compactChange(), extension: true }), /unknown field extension/);
  assert.throws(() => validateCompactRecord({ ...compactChange(), current_stage: "future" }), /Stage: unknown_value future/);
});

test("all eight compact schemas accept exact records and reject extra top-level fields", () => {
  for (const fixture of schemaFixtures()) {
    assert.equal(validateCompactRecord(fixture), fixture, fixture.schema);
    assert.throws(() => validateCompactRecord({ ...fixture, extension: true }), /unknown field extension/, fixture.schema);
  }
});

test("shared cross-runtime compact schema records match the Node validator", () => {
  const records = JSON.parse(readFileSync(new URL("../../../tests/fixtures/compact-current-state-v1/schema-records.json", import.meta.url), "utf8"));
  assert.deepEqual(records.map((record) => record.schema), COMPACT_SCHEMA_IDS);
  for (const record of records) {
    assert.equal(validateCompactRecord(record), record, record.schema);
    assert.throws(() => validateCompactRecord({ ...record, extension: true }), /unknown field extension/, record.schema);
  }
});

test("Text limits count UTF-8 bytes and semantic content inputs are exact", () => {
  const review = schemaFixtures()[1];
  assert.throws(() => validateCompactRecord({ ...review, limitations: ["é".repeat(9000)] }), /at most 16 KiB/);
  const operation = schemaFixtures()[5];
  assert.throws(() => validateCompactRecord({ ...operation, operation: "record-artifact" }), /unknown field|missing field/);
  assert.throws(() => validateCompactRecord({ ...operation, payload: { ...operation.payload, extension: true } }), /unknown field extension/);
  const recordArtifact = { ...operation, operation: "record-artifact", payload: operationPayloads()["record-artifact"] };
  assert.equal(validateCompactRecord(recordArtifact), recordArtifact);
  assert.throws(() => validateCompactRecord({ ...recordArtifact, payload: { ...recordArtifact.payload, content: { ...recordArtifact.payload.content, content: "tampered\n" } } }), /inline identity mismatch/);
});

test("all fourteen semantic operation payload variants validate and mismatches fail closed", () => {
  for (const [operation, payload] of Object.entries(operationPayloads())) {
    const envelope = { schema: "compact-operation-v1", operation, change_id: "example", expected_lifecycle_revision: d, expected_files: {}, payload };
    assert.equal(validateCompactRecord(envelope), envelope, operation);
  }
  const advance = operationPayloads()["advance-stage"];
  assert.throws(() => validateCompactRecord({ schema: "compact-operation-v1", operation: "recover", change_id: "example", expected_lifecycle_revision: d, expected_files: {}, payload: advance }), /unknown field|missing field/);
  for (const [field, value] of [["from_status", "closed"], ["to_status", "blocked"]]) {
    const milestone = operationPayloads()["advance-milestone"];
    assert.throws(() => validateCompactRecord({ schema: "compact-operation-v1", operation: "advance-milestone", change_id: "example", expected_lifecycle_revision: d, expected_files: {}, payload: { ...milestone, [field]: value } }), /unknown_value/, field);
  }
  const activation = { ...operationPayloads()["advance-milestone"], from_status: null, to_status: "planned" };
  assert.equal(validateCompactRecord({ schema: "compact-operation-v1", operation: "advance-milestone", change_id: "example", expected_lifecycle_revision: d, expected_files: {}, payload: activation }).payload, activation);
});

test("operation envelopes reject caller identity and claimed authority fields", () => {
  const operation = schemaFixtures()[5];
  assert.throws(() => validateCompactRecord({ ...operation, authority: "workflow" }), /unknown field authority/);
  assert.throws(() => validateCompactRecord({ ...operation, caller: "proposal" }), /unknown field caller/);
  const route = operationPayloads()["route-correction"];
  assert.throws(() => validateCompactRecord({ ...operation, operation: "route-correction", payload: { correction: { ...route.correction, kind: "correction" } } }), /unknown field kind/);
  assert.throws(() => validateCompactRecord({ ...operation, operation: "route-correction", payload: { correction: { ...route.correction, status: "authoring" } } }), /unknown field status/);
});

test("published JSON Schema closes projections, result consistency, candidate files, and every operation payload", () => {
  const schema = JSON.parse(readFileSync(new URL("../../../schemas/compact-current-state-v1.schema.json", import.meta.url), "utf8"));
  assert.deepEqual(schema.$defs.projection.required.slice(0, 4), ["view", "change_id", "lifecycle_contract", "lifecycle_revision"]);
  assert.equal(schema.$defs.operationEnvelope.allOf.length, Object.keys(operationPayloads()).length);
  assert.ok(schema.$defs.operationEnvelope.allOf.every((branch) => branch.then.properties.payload.$ref.startsWith("#/$defs/")));
  assert.equal(schema.$defs.result.allOf[0].then.properties.bytes_changed.const, false);
  assert.equal(schema.$defs.result.allOf[0].then.properties.affected_paths.maxItems, 0);
});

test("read-only result consistency is enforced", () => {
  const result = schemaFixtures()[6];
  assert.throws(() => validateCompactRecord({ ...result, prior_lifecycle_revision: d }), /read-only projection/);
  assert.throws(() => validateCompactRecord({ ...result, bytes_changed: true }), /read-only projection/);
  assert.throws(() => validateCompactRecord({ ...result, affected_paths: ["change.yaml"] }), /read-only projection/);
  assert.throws(() => validateCompactRecord({ ...result, change_id: "other" }), /projection change_id/);
  assert.throws(() => validateCompactRecord({ ...result, status: "rejected" }), /read-only projection/);
  assert.deepEqual(validateCompactRecord({ ...result, projection: null, prior_lifecycle_revision: d, resulting_lifecycle_revision: d }), { ...result, projection: null, prior_lifecycle_revision: d, resulting_lifecycle_revision: d });
  assert.equal(diagnostic.code, "RL_BLOCKED");
});

test("timestamps and recovery content paths enforce real UTC and the exact private transaction root", () => {
  const review = schemaFixtures()[1];
  assert.throws(() => validateCompactRecord({ ...review, recorded_at: "2026-02-31T00:00:00Z" }), /Timestamp/);
  const recovery = schemaFixtures()[7];
  const valid = structuredClone(recovery);
  valid.affected_files[0].prior_content = ".rigorloop/transactions/example/prior/change";
  valid.affected_files[0].candidate_content = ".rigorloop/transactions/example/candidate/change";
  assert.equal(validateCompactRecord(valid), valid);
  const escaped = structuredClone(valid);
  escaped.affected_files[0].prior_content = "docs/prior-change";
  assert.throws(() => validateCompactRecord(escaped), /prior\/ directory/);
  const wrongChange = structuredClone(valid);
  wrongChange.affected_files[0].candidate_content = ".rigorloop/transactions/other/candidate/change";
  assert.throws(() => validateCompactRecord(wrongChange), /candidate\/ directory/);
});

test("compact YAML rejects aliases, duplicate keys, multiple documents, and schema mismatch", () => {
  const valid = [
    "schema: compact-change-v1",
    "change_id: example",
    "title: Example",
    "lifecycle_contract: compact-current-state-v1",
    `lifecycle_revision: ${d}`,
    "current_stage: proposal",
    "artifacts: {}",
    "reviews: {}",
    "active_work: null",
    "open_findings: {}",
    "material_decisions: {}",
    "evidence: {}",
    "blockers: []",
    "remaining_work: {}",
    "readiness: not-ready",
    "",
  ].join("\n");
  assert.equal(parseCompactYaml(valid, "compact-change-v1").change_id, "example");
  assert.throws(() => parseCompactYaml(`${valid}title: Again\n`, "compact-change-v1"), /duplicate|Map keys must be unique/i);
  assert.throws(() => parseCompactYaml("schema: &s compact-change-v1\ntitle: *s\n", "compact-change-v1"), /alias|anchor/i);
  assert.throws(() => parseCompactYaml(`${valid}---\nschema: compact-change-v1\n`, "compact-change-v1"), /exactly one YAML document/);
  assert.throws(() => parseCompactYaml(valid, "compact-evidence-v1"), /schema mismatch/);
});

test("compact Markdown uses YAML front matter as sole machine authority", () => {
  const text = [
    "---",
    "schema: compact-review-v1",
    "review_id: review-1",
    "target:",
    "  target_id: proposal",
    "  target_kind: proposal",
    "round: 1",
    "subjects: {}",
    "reviewer_authority: proposal-review",
    "outcome: approved",
    "recording_status: recorded",
    "open_findings: {}",
    "material_decisions: []",
    "limitations: []",
    "recorded_at: 2026-09-04T00:00:00Z",
    "---",
    "",
    "# Human explanation",
    "",
  ].join("\n");
  const parsed = parseCompactMarkdown(text, "compact-review-v1");
  assert.equal(parsed.record.review_id, "review-1");
  assert.match(parsed.markdown, /Human explanation/);
  assert.throws(() => parseCompactMarkdown("schema: compact-review-v1\n", "compact-review-v1"), /front matter/);
});

test("whole-set lifecycle revision uses exact coordinator bytes and sorted authoritative files", () => {
  const sentinel = `sha256:${"0".repeat(64)}`;
  const changeBytes = `schema: compact-change-v1\nchange_id: example\nlifecycle_contract: compact-current-state-v1\nlifecycle_revision: ${d}\n`;
  const files = new Map([
    ["specs/example.md", Buffer.from("spec\n")],
    ["docs/proposals/example.md", Buffer.from("proposal\n")],
  ]);
  const coordinator = changeBytes.replace(d, sentinel);
  const manifest = `${JSON.stringify({
    change_id: "example",
    contract: "compact-current-state-v1",
    coordinator_sha256: digest(coordinator),
    files: [
      { path: "docs/proposals/example.md", sha256: digest("proposal\n") },
      { path: "specs/example.md", sha256: digest("spec\n") },
    ],
  })}\n`;
  assert.deepEqual(compactLifecycleRevision({ changeBytes, files }), {
    revision: digest(manifest),
    manifest,
    coordinator_sha256: digest(coordinator),
  });
  assert.notEqual(compactLifecycleRevision({ changeBytes, files: new Map(files).set("specs/example.md", Buffer.from("changed\n")) }).revision, digest(manifest));
  assert.throws(() => compactLifecycleRevision({ changeBytes: changeBytes.replace(d, `"${d}"`), files }), /plain-style lifecycle_revision/);
  assert.throws(() => compactLifecycleRevision({ changeBytes: changeBytes.replace("lifecycle_contract: compact-current-state-v1\n", ""), files }), /lifecycle_contract/);
});

test("optional decision and evidence surfaces reject empty placeholder records", () => {
  assert.throws(() => validateCompactRecord({ schema: "compact-decisions-v1", decisions: {} }), /must be absent instead of empty/);
  assert.throws(() => validateCompactRecord({ schema: "compact-evidence-v1", evidence: {} }), /must be absent instead of empty/);
});

test("complete-set validation binds the coordinator to every authoritative byte", () => {
  const sentinel = `sha256:${"0".repeat(64)}`;
  const initial = [
    "schema: compact-change-v1",
    "change_id: example",
    "title: Example",
    "lifecycle_contract: compact-current-state-v1",
    `lifecycle_revision: ${sentinel}`,
    "current_stage: proposal",
    "artifacts: {}",
    "reviews: {}",
    "active_work: null",
    "open_findings: {}",
    "material_decisions: {}",
    "evidence: {}",
    "blockers: []",
    "remaining_work: {}",
    "readiness: not-ready",
    "",
  ].join("\n");
  const revision = compactLifecycleRevision({ changeBytes: initial, files: new Map() }).revision;
  const current = initial.replace(sentinel, revision);
  assert.equal(validateCompactSet({ changeBytes: current, files: new Map() }).change.lifecycle_revision, revision);
  assert.throws(() => validateCompactSet({ changeBytes: current.replace("title: Example", "title: Changed"), files: new Map() }), /lifecycle revision mismatch/);
  const procedural = new Map([["docs/changes/example/request.json", "{}\n"]]);
  const proceduralRevision = compactLifecycleRevision({ changeBytes: initial, files: procedural }).revision;
  assert.throws(() => validateCompactSet({ changeBytes: initial.replace(sentinel, proceduralRevision), files: procedural }), /not a current authoritative path/);
});

test("complete-set validation rejects a current review finding hidden from the coordinator", () => {
  const sentinel = `sha256:${"0".repeat(64)}`;
  const reviewPath = "docs/changes/example/reviews/code-review-M1.md";
  const reviewBytes = [
    "---", "schema: compact-review-v1", "review_id: review-1", "target:", "  target_id: M1", "  target_kind: milestone", "round: 1",
    "subjects: {}", "reviewer_authority: code-review", "outcome: changes-requested", "recording_status: recorded", "open_findings:", "  F1:",
    "    finding_id: F1", "    affected_surfaces:", "      - implementation", "    severity: major", "    blocking_effect: blocks-progression",
    "    owner: implement", "    required_next_action: Fix it", "    disposition: open", "    evidence: Current failure", "material_decisions: []", "limitations: []",
    "recorded_at: 2026-09-04T00:00:00Z", "---", "", "# Review", "",
  ].join("\n");
  const initial = [
    "schema: compact-change-v1", "change_id: example", "title: Example", "lifecycle_contract: compact-current-state-v1", `lifecycle_revision: ${sentinel}`,
    "current_stage: code-review", "artifacts: {}", "reviews:", "  M1:", "    target_id: M1", `    path: ${reviewPath}`, `    identity: ${digest(reviewBytes)}`,
    "    review_id: review-1", "    outcome: changes-requested", "    reviewer_authority: code-review", "    status: current", "active_work: null", "open_findings: {}",
    "material_decisions: {}", "evidence: {}", "blockers: []", "remaining_work: {}", "readiness: blocked", "",
  ].join("\n");
  const files = new Map([[reviewPath, reviewBytes]]);
  const revision = compactLifecycleRevision({ changeBytes: initial, files }).revision;
  assert.throws(() => validateCompactSet({ changeBytes: initial.replace(sentinel, revision), files }), /finding F1 is omitted from change.yaml/);
});

test("complete-set validation binds proposal review subjects to current artifact identities", () => {
  const artifactPath = "docs/proposals/example.md";
  const reviewPath = "docs/changes/example/reviews/proposal-review.md";
  const artifact = Buffer.from("# Proposal\n");
  const stale = `sha256:${"b".repeat(64)}`;
  const reviewRecord = { schema: "compact-review-v1", review_id: "proposal-review-1", target: { target_id: "proposal", target_kind: "proposal" }, round: 1, subjects: { proposal: { subject_id: "proposal", path: artifactPath, identity: stale } }, reviewer_authority: "proposal-review", outcome: "approved", recording_status: "recorded", open_findings: {}, material_decisions: [], limitations: [], recorded_at: "2026-09-04T00:00:00Z" };
  const review = Buffer.from(`---\n${serializeLifecycleYaml(reviewRecord)}---\n`);
  const change = compactChange();
  change.artifacts = { proposal: { artifact_id: "proposal", kind: "proposal", role: "primary", path: artifactPath, identity: digest(artifact), owner: "proposal", status: "accepted" } };
  change.reviews = { proposal: { target_id: "proposal", path: reviewPath, identity: digest(review), review_id: "proposal-review-1", outcome: "approved", reviewer_authority: "proposal-review", status: "current" } };
  const files = { [artifactPath]: artifact, [reviewPath]: review };
  change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(change), files }).revision;
  assert.throws(() => validateCompactSet({ changeBytes: serializeLifecycleYaml(change), files }), /subject proposal is not current/);
});
