import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { test } from "node:test";

import { compactLifecycleRevision, validateCompactSet } from "../dist/lib/compact-contract.js";
import { compactOperationEligibility } from "../dist/lib/compact-eligibility.js";
import { evaluateCompactOperation } from "../dist/lib/compact-operations.js";
import { serializeLifecycleYaml } from "../dist/lib/lifecycle-contract.js";

const sentinel = `sha256:${"0".repeat(64)}`;
const hash = (value) => `sha256:${createHash("sha256").update(value).digest("hex")}`;
const changePath = "docs/changes/example/change.yaml";
const reviewPath = "docs/changes/example/reviews/code-review-M1.md";

function review({ id = "review-1", round = 1, outcome = "changes-requested", findings = {} } = {}) {
  const record = {
    schema: "compact-review-v1",
    review_id: id,
    target: { target_id: "M1", target_kind: "milestone" },
    round,
    subjects: {},
    reviewer_authority: "code-review",
    outcome,
    recording_status: "recorded",
    open_findings: findings,
    material_decisions: [],
    limitations: [],
    recorded_at: "2026-09-04T00:00:00Z",
  };
  return `---\n${serializeLifecycleYaml(record)}---\n\n# Current review\n`;
}

const finding = {
  finding_id: "F1",
  affected_surfaces: ["implementation"],
  severity: "major",
  blocking_effect: "blocks-progression",
  owner: "implement",
  required_next_action: "Correct the implementation",
  disposition: "open",
  evidence: "The focused check fails",
};

function compactSet({ currentStage = "code-review", activeWork = null, reviewBytes = null, findingValues = { F1: finding } } = {}) {
  reviewBytes ??= review({ findings: findingValues });
  const files = { [reviewPath]: Buffer.from(reviewBytes) };
  const change = {
    schema: "compact-change-v1",
    change_id: "example",
    title: "Example",
    lifecycle_contract: "compact-current-state-v1",
    lifecycle_revision: sentinel,
    current_stage: currentStage,
    artifacts: {},
    reviews: { M1: { target_id: "M1", path: reviewPath, identity: hash(reviewBytes), review_id: reviewBytes.includes("review-2") ? "review-2" : "review-1", outcome: reviewBytes.includes("outcome: approved") ? "approved" : "changes-requested", reviewer_authority: "code-review", status: "current" } },
    active_work: activeWork,
    open_findings: Object.fromEntries(Object.values(findingValues).map((entry) => [entry.finding_id, { finding_id: entry.finding_id, review_target_id: "M1", review_path: reviewPath, review_identity: hash(reviewBytes), owner: entry.owner, severity: entry.severity, blocking_effect: entry.blocking_effect }])),
    material_decisions: {},
    evidence: {},
    blockers: [],
    remaining_work: {},
    readiness: "blocked",
  };
  const initial = serializeLifecycleYaml(change);
  change.lifecycle_revision = compactLifecycleRevision({ changeBytes: initial, files }).revision;
  const changeBytes = Buffer.from(serializeLifecycleYaml(change));
  validateCompactSet({ changeBytes: changeBytes.toString("utf8"), files });
  return { change, files: { [changePath]: changeBytes, ...files } };
}

function expectedFiles(files, additions = {}) {
  return Object.fromEntries(Object.entries({ ...files, ...additions }).sort(([a], [b]) => a.localeCompare(b)).map(([path, bytes]) => [path, { path, state: bytes === null ? "absent" : "present", identity: bytes === null ? null : hash(bytes) }]));
}

function request(state, operation, payload, additions = {}) {
  return { schema: "compact-operation-v1", operation, change_id: "example", expected_lifecycle_revision: state.change.lifecycle_revision, expected_files: expectedFiles(state.files, additions), payload };
}

function nextState(candidate) {
  return { change: candidate.change, files: candidate.candidateSet };
}

function refreshCompactSet(state) {
  state.change.lifecycle_revision = sentinel;
  const authoritative = Object.fromEntries(Object.entries(state.files).filter(([path]) => path !== changePath));
  state.change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(state.change), files: authoritative }).revision;
  state.files[changePath] = Buffer.from(serializeLifecycleYaml(state.change));
  validateCompactSet({ changeBytes: state.files[changePath].toString("utf8"), files: authoritative });
  return state;
}

function evidenceSet({ second = false, currentStage = "spec" } = {}) {
  const artifactPath = "specs/example.md";
  const evidencePath = "docs/changes/example/evidence.yaml";
  const verifyPath = "docs/changes/example/verify-report.md";
  const artifact = Buffer.from("initial specification\n");
  const evidenceRecord = { schema: "compact-evidence-v1", evidence: { EV1: { evidence_id: "EV1", verifies: ["SR-01"], subjects: { spec: { subject_id: "spec", path: artifactPath, identity: hash(artifact) } }, method: "node --test", outcome: "passed", surfaces: ["contract"], freshness: "current", invalidating_dependencies: [{ kind: "artifact", id: "spec", identity: hash(artifact) }], producer_authority: "implement", detail_location: null, required_rerun: null } } };
  if (second) evidenceRecord.evidence.EV2 = { ...structuredClone(evidenceRecord.evidence.EV1), evidence_id: "EV2", verifies: ["SR-02"] };
  const evidence = Buffer.from(serializeLifecycleYaml(evidenceRecord));
  const verifyRecord = { schema: "compact-verify-v1", verification_id: "verify-1", subjects: { spec: { subject_id: "spec", path: artifactPath, identity: hash(artifact) } }, verdict: "passed", impact: "standard", evidence_reused: ["EV1"], evidence_rerun: [], limitations: [], residual_risks: [], explanation: "The current subject passed.", handoff: "ready", recorded_at: "2026-09-04T00:00:00Z" };
  const verify = Buffer.from(`---\n${serializeLifecycleYaml(verifyRecord)}---\n\n# Verify\n`);
  const files = { [artifactPath]: artifact, [evidencePath]: evidence, [verifyPath]: verify };
  const evidenceRefs = Object.fromEntries(Object.keys(evidenceRecord.evidence).map((id) => [id, { evidence_id: id, manifest_path: evidencePath, manifest_identity: hash(evidence), freshness: "current" }]));
  const change = { schema: "compact-change-v1", change_id: "example", title: "Example", lifecycle_contract: "compact-current-state-v1", lifecycle_revision: sentinel, current_stage: currentStage, artifacts: { spec: { artifact_id: "spec", kind: "spec", role: "primary", path: artifactPath, identity: hash(artifact), owner: "spec", status: "approved" } }, reviews: {}, active_work: null, open_findings: {}, material_decisions: {}, evidence: evidenceRefs, blockers: [], remaining_work: {}, readiness: "verified" };
  change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(change), files }).revision;
  const changeBytes = Buffer.from(serializeLifecycleYaml(change));
  return { change, files: { [changePath]: changeBytes, ...files }, artifactPath, evidencePath, verifyPath };
}

test("route, explicit return, rereview, and approving settlement preserve one correction until review settles", () => {
  let state = compactSet();
  const correction = { finding_ids: ["F1"], source_stage: "code-review", destination_stage: "implement", return_stage: "code-review", owner: "implement", reason: "implementation-defect", return_condition: "Focused proof passes", expected_review_target: "M1" };
  let candidate = evaluateCompactOperation({ request: request(state, "route-correction", { correction }), currentFiles: state.files });
  assert.deepEqual(candidate.change.active_work, { kind: "correction", ...correction, status: "authoring" });
  assert.equal(candidate.change.current_stage, "implement");

  state = nextState(candidate);
  candidate = evaluateCompactOperation({ request: request(state, "return-correction", { finding_ids: ["F1"], return_stage: "code-review", satisfied_condition: "Focused proof passes" }), currentFiles: state.files });
  assert.equal(candidate.change.active_work.status, "review-required");
  assert.equal(candidate.change.current_stage, "code-review");

  state = nextState(candidate);
  const cleanReview = review({ id: "review-2", round: 2, outcome: "approved", findings: {} });
  const reviewInput = { path: reviewPath, identity: hash(cleanReview), source: "inline", content: cleanReview, source_path: null };
  candidate = evaluateCompactOperation({ request: request(state, "replace-review", { target_id: "M1", prior_review_identity: state.change.reviews.M1.identity, review: reviewInput, resolutions: { F1: { finding_id: "F1", disposition: "accepted", materiality: "non-material", decision_id: null } } }), currentFiles: state.files });
  assert.equal(candidate.change.active_work.status, "review-required");
  assert.deepEqual(candidate.change.open_findings, {});

  state = nextState(candidate);
  candidate = evaluateCompactOperation({ request: request(state, "settle-review", { target_id: "M1", review_id: "review-2", outcome: "approved" }), currentFiles: state.files });
  assert.equal(candidate.change.active_work, null);
});

test("route-correction rejects caller-supplied durable correction fields", () => {
  const state = compactSet();
  const correction = { kind: "correction", finding_ids: ["F1"], source_stage: "code-review", destination_stage: "implement", return_stage: "code-review", owner: "implement", reason: "implementation-defect", return_condition: "Pass", expected_review_target: "M1" };
  assert.throws(() => evaluateCompactOperation({ request: request(state, "route-correction", { correction }), currentFiles: state.files }), /unknown field kind/);
});

test("review replacement fails closed instead of losing an open finding", () => {
  const state = compactSet();
  const cleanReview = review({ id: "review-2", round: 2, outcome: "approved", findings: {} });
  const input = { path: reviewPath, identity: hash(cleanReview), source: "inline", content: cleanReview, source_path: null };
  assert.throws(() => evaluateCompactOperation({ request: request(state, "replace-review", { target_id: "M1", prior_review_identity: state.change.reviews.M1.identity, review: input, resolutions: {} }), currentFiles: state.files }), /omitted an open finding/);
});

test("legacy and unknown migration requests never acquire compact writer authority", () => {
  const state = compactSet();
  assert.throws(() => evaluateCompactOperation({ request: { ...request(state, "advance-stage", { from_stage: "code-review", to_stage: "verify" }), operation: "migrate-change" }, currentFiles: state.files }), /Operation: unknown_value migrate-change/);
});

test("an artifact revision atomically stales dependent evidence and removes final readiness", () => {
  const state = evidenceSet();
  const content = "revised specification\n";
  const artifact = { ...state.change.artifacts.spec, identity: hash(content), status: "review-required" };
  const input = { path: state.artifactPath, identity: hash(content), source: "inline", content, source_path: null };
  const candidate = evaluateCompactOperation({ request: request(state, "record-artifact", { artifact, content: input }), currentFiles: state.files });
  assert.equal(candidate.change.evidence.EV1.freshness, "stale");
  assert.equal(candidate.change.readiness, "not-ready");
  assert.equal(candidate.candidateSet[state.verifyPath], null);
  assert.match(candidate.candidateSet[state.evidencePath].toString("utf8"), /freshness: stale/);
});

test("the first artifact is structurally eligible at its owning authoring stage", () => {
  const state = compactSet({ currentStage: "proposal" });
  state.change.artifacts = {};
  assert.equal(compactOperationEligibility(state.change, "record-artifact").status, "permitted");
});

test("a correction cannot mix findings from another review target", () => {
  const state = compactSet();
  const correction = { finding_ids: ["F1"], source_stage: "code-review", destination_stage: "implement", return_stage: "code-review", owner: "implement", reason: "implementation-defect", return_condition: "Focused proof passes", expected_review_target: "final-code" };
  const eligibility = compactOperationEligibility(state.change, "route-correction", request(state, "route-correction", { correction }));
  assert.equal(eligibility.status, "prohibited");
  assert.equal(eligibility.blockers[0].invariant, "correction-target");
});

test("resolve-finding cannot erase another finding from the stable review", () => {
  const second = { ...finding, finding_id: "F2", evidence: "A second focused failure" };
  const state = compactSet({ currentStage: "review-resolution", findingValues: { F1: finding, F2: second } });
  const candidateReview = review({ id: "review-2", round: 2, findings: {} });
  const input = { path: reviewPath, identity: hash(candidateReview), source: "inline", content: candidateReview, source_path: null };
  const operation = request(state, "resolve-finding", { resolution: { finding_id: "F1", disposition: "accepted", materiality: "non-material", decision_id: null }, review: input, decisions: null });
  assert.throws(() => evaluateCompactOperation({ request: operation, currentFiles: state.files }), /omitted another open finding/);
});

test("expected_files rejects an unrelated caller-selected input path", () => {
  const state = compactSet();
  const extraPath = "unrelated/private.txt";
  const extra = Buffer.from("not an evaluator input\n");
  const correction = { finding_ids: ["F1"], source_stage: "code-review", destination_stage: "implement", return_stage: "code-review", owner: "implement", reason: "implementation-defect", return_condition: "Focused proof passes", expected_review_target: "M1" };
  const operation = request(state, "route-correction", { correction }, { [extraPath]: extra });
  assert.throws(() => evaluateCompactOperation({ request: operation, currentFiles: { ...state.files, [extraPath]: extra } }), /bind exactly/);
});

test("record-artifact cannot change stable registration metadata", () => {
  const state = evidenceSet();
  const changedPath = "specs/renamed.md";
  const content = "same contract at a different path\n";
  const artifact = { ...state.change.artifacts.spec, path: changedPath, identity: hash(content), status: "review-required" };
  const input = { path: changedPath, identity: hash(content), source: "inline", content, source_path: null };
  const operation = request(state, "record-artifact", { artifact, content: input }, { [changedPath]: null });
  assert.throws(() => evaluateCompactOperation({ request: operation, currentFiles: { ...state.files, [changedPath]: null } }), /stable registration fields/);
});

test("Verify is prohibited without a current approved final Code Review", () => {
  const state = evidenceSet();
  state.change.current_stage = "verify";
  assert.equal(compactOperationEligibility(state.change, "record-verify").status, "prohibited");
});

test("update-evidence cannot erase another current manifest entry", () => {
  const state = evidenceSet({ second: true, currentStage: "implement" });
  const candidateRecord = { schema: "compact-evidence-v1", evidence: { EV1: { evidence_id: "EV1", verifies: ["SR-01"], subjects: { spec: { subject_id: "spec", path: state.artifactPath, identity: hash(state.files[state.artifactPath]) } }, method: "node --test focused", outcome: "passed", surfaces: ["contract"], freshness: "current", invalidating_dependencies: [{ kind: "artifact", id: "spec", identity: hash(state.files[state.artifactPath]) }], producer_authority: "implement", detail_location: null, required_rerun: null } } };
  const content = serializeLifecycleYaml(candidateRecord);
  const input = { path: state.evidencePath, identity: hash(content), source: "inline", content, source_path: null };
  const operation = request(state, "update-evidence", { evidence_ids: ["EV1"], evidence: input });
  assert.throws(() => evaluateCompactOperation({ request: operation, currentFiles: state.files }), /omitted unselected current entries/);
});

test("upsert-decision cannot erase another current material decision", () => {
  const state = compactSet({ currentStage: "review-resolution" });
  const decisionsPath = "docs/changes/example/material-decisions.md";
  const makeDecision = (id) => ({ decision_id: id, source: { kind: "finding", id: "F1" }, decision: `Keep ${id}`, rationale: "It remains constraining", affected_surfaces: ["contract"], owner: "spec", applicability: "applicable", applicable_since: state.change.lifecycle_revision });
  const currentRecord = { schema: "compact-decisions-v1", decisions: { D1: makeDecision("D1"), D2: makeDecision("D2") } };
  const currentBytes = Buffer.from(`---\n${serializeLifecycleYaml(currentRecord)}---\n`);
  state.files[decisionsPath] = currentBytes;
  state.change.material_decisions = Object.fromEntries(["D1", "D2"].map((id) => [id, { decision_id: id, path: decisionsPath, identity: hash(currentBytes), applicability: "applicable" }]));
  state.change.lifecycle_revision = sentinel;
  state.change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(state.change), files: { [reviewPath]: state.files[reviewPath], [decisionsPath]: currentBytes } }).revision;
  state.files[changePath] = Buffer.from(serializeLifecycleYaml(state.change));

  const candidateRecord = { schema: "compact-decisions-v1", decisions: { D1: makeDecision("D1") } };
  const content = `---\n${serializeLifecycleYaml(candidateRecord)}---\n`;
  const input = { path: decisionsPath, identity: hash(content), source: "inline", content, source_path: null };
  const operation = request(state, "upsert-decision", { decision_id: "D1", decisions: input });
  assert.throws(() => evaluateCompactOperation({ request: operation, currentFiles: state.files }), /omitted unselected current entries/);
});

test("record-verify requires and binds the exact approved final review, evidence basis, and observed subject", () => {
  const state = evidenceSet();
  const finalPath = "docs/changes/example/reviews/code-review-final.md";
  const finalRecord = { schema: "compact-review-v1", review_id: "final-review-1", target: { target_id: "final", target_kind: "final-code" }, round: 1, subjects: { spec: { subject_id: "spec", path: state.artifactPath, identity: hash(state.files[state.artifactPath]) } }, reviewer_authority: "code-review", outcome: "approved", recording_status: "recorded", open_findings: {}, material_decisions: [], limitations: [], recorded_at: "2026-09-04T00:00:00Z" };
  const finalBytes = Buffer.from(`---\n${serializeLifecycleYaml(finalRecord)}---\n`);
  state.change.current_stage = "verify";
  state.change.readiness = "not-ready";
  state.change.reviews = { final: { target_id: "final", path: finalPath, identity: hash(finalBytes), review_id: "final-review-1", outcome: "approved", reviewer_authority: "code-review", status: "current" } };
  delete state.files[state.verifyPath];
  state.files[finalPath] = finalBytes;
  state.change.lifecycle_revision = sentinel;
  state.change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(state.change), files: { [state.artifactPath]: state.files[state.artifactPath], [state.evidencePath]: state.files[state.evidencePath], [finalPath]: finalBytes } }).revision;
  state.files[changePath] = Buffer.from(serializeLifecycleYaml(state.change));

  const reportRecord = { schema: "compact-verify-v1", verification_id: "verify-2", subjects: { spec: { subject_id: "spec", path: state.artifactPath, identity: hash(state.files[state.artifactPath]) } }, verdict: "passed", impact: "standard", evidence_reused: ["EV1"], evidence_rerun: [], limitations: [], residual_risks: [], explanation: "The exact current set passed.", handoff: "ready", recorded_at: "2026-09-04T00:00:00Z" };
  const report = `---\n${serializeLifecycleYaml(reportRecord)}---\n`;
  const input = { path: state.verifyPath, identity: hash(report), source: "inline", content: report, source_path: null };
  const operation = request(state, "record-verify", { verification_id: "verify-2", report: input, evidence_ids: ["EV1"] }, { [state.verifyPath]: null });
  const candidate = evaluateCompactOperation({ request: operation, currentFiles: { ...state.files, [state.verifyPath]: null } });
  assert.equal(candidate.change.readiness, "verified");
  assert.match(candidate.candidateSet[state.verifyPath].toString("utf8"), /verification_id: verify-2/);

  const mismatched = structuredClone(operation);
  mismatched.payload.evidence_ids = ["EV2"];
  assert.throws(() => evaluateCompactOperation({ request: mismatched, currentFiles: { ...state.files, [state.verifyPath]: null } }), /current evidence|basis differs/);
});

test("the exact operation matrix admits active-milestone review handoff and rejects wrong-gate review work", () => {
  const milestone = { kind: "milestone", milestone_id: "M1", status: "review-required", owner: "implement" };
  const handoff = compactSet({ currentStage: "implement", activeWork: milestone, findingValues: {} });
  const advance = request(handoff, "advance-stage", { from_stage: "implement", to_stage: "code-review" });
  assert.equal(compactOperationEligibility(handoff.change, "advance-stage", advance).status, "permitted");
  assert.equal(evaluateCompactOperation({ request: advance, currentFiles: handoff.files }).change.current_stage, "code-review");

  const wrongGate = compactSet({ currentStage: "proposal-review" });
  const replacement = review({ id: "review-2", round: 2, findings: { F1: finding } });
  const input = { path: reviewPath, identity: hash(replacement), source: "inline", content: replacement, source_path: null };
  const replace = request(wrongGate, "replace-review", { target_id: "M1", prior_review_identity: wrongGate.change.reviews.M1.identity, review: input, resolutions: {} });
  assert.equal(compactOperationEligibility(wrongGate.change, "replace-review", replace).status, "prohibited");
  const settle = request(wrongGate, "settle-review", { target_id: "M1", review_id: "review-1", outcome: "changes-requested" });
  assert.equal(compactOperationEligibility(wrongGate.change, "settle-review", settle).status, "prohibited");
});

test("decision maintenance enforces current source, stable ownership, and responsible stage", () => {
  const state = compactSet({ currentStage: "proposal" });
  const decisionsPath = "docs/changes/example/material-decisions.md";
  const current = { decision_id: "D1", source: { kind: "finding", id: "F1" }, decision: "Keep the boundary", rationale: "It remains constraining", affected_surfaces: ["contract"], owner: "spec", applicability: "applicable", applicable_since: state.change.lifecycle_revision };
  const currentRecord = { schema: "compact-decisions-v1", decisions: { D1: current } };
  const currentBytes = Buffer.from(`---\n${serializeLifecycleYaml(currentRecord)}---\n`);
  state.files[decisionsPath] = currentBytes;
  state.change.material_decisions = { D1: { decision_id: "D1", path: decisionsPath, identity: hash(currentBytes), applicability: "applicable" } };
  state.change.lifecycle_revision = sentinel;
  state.change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(state.change), files: { [reviewPath]: state.files[reviewPath], [decisionsPath]: currentBytes } }).revision;
  state.files[changePath] = Buffer.from(serializeLifecycleYaml(state.change));
  const revised = { ...current, decision: "Keep the exact boundary" };
  const content = `---\n${serializeLifecycleYaml({ schema: "compact-decisions-v1", decisions: { D1: revised } })}---\n`;
  const input = { path: decisionsPath, identity: hash(content), source: "inline", content, source_path: null };
  assert.throws(() => evaluateCompactOperation({ request: request(state, "upsert-decision", { decision_id: "D1", decisions: input }), currentFiles: state.files }), /not owned by the current stage/);

  const newState = compactSet({ currentStage: "review-resolution" });
  const invalid = { ...current, decision_id: "D2", source: { kind: "finding", id: "F99" } };
  const invalidContent = `---\n${serializeLifecycleYaml({ schema: "compact-decisions-v1", decisions: { D2: invalid } })}---\n`;
  const invalidInput = { path: decisionsPath, identity: hash(invalidContent), source: "inline", content: invalidContent, source_path: null };
  const operation = request(newState, "upsert-decision", { decision_id: "D2", decisions: invalidInput }, { [decisionsPath]: null });
  assert.throws(() => evaluateCompactOperation({ request: operation, currentFiles: { ...newState.files, [decisionsPath]: null } }), /does not name a current finding/);
});

test("evidence invalidation rejects unknown and already stale selections", () => {
  const state = evidenceSet();
  const unknown = request(state, "invalidate-evidence", { evidence_ids: ["EV99"], reason: "Observed drift", evidence: null });
  assert.equal(compactOperationEligibility(state.change, "invalidate-evidence", unknown).status, "prohibited");
  state.change.evidence.EV1.freshness = "stale";
  const stale = request(state, "invalidate-evidence", { evidence_ids: ["EV1"], reason: "Already stale", evidence: null });
  assert.equal(compactOperationEligibility(state.change, "invalidate-evidence", stale).status, "prohibited");
});

test("stage edges require current gate judgments and final Verify readiness", () => {
  const state = compactSet({ currentStage: "proposal-review", findingValues: {} });
  state.change.reviews.M1.reviewer_authority = "proposal-review";
  state.change.reviews.M1.outcome = "changes-requested";
  const next = request(state, "advance-stage", { from_stage: "proposal-review", to_stage: "architecture" });
  assert.equal(compactOperationEligibility(state.change, "advance-stage", next).status, "prohibited");
  state.change.reviews.M1.outcome = "approved";
  assert.equal(compactOperationEligibility(state.change, "advance-stage", next).status, "permitted");

  state.change.current_stage = "verify";
  state.change.readiness = "not-ready";
  const handoff = request(state, "advance-stage", { from_stage: "verify", to_stage: "pr" });
  assert.equal(compactOperationEligibility(state.change, "advance-stage", handoff).status, "prohibited");
  state.change.readiness = "verified";
  assert.equal(compactOperationEligibility(state.change, "advance-stage", handoff).status, "permitted");
});

test("blocking findings select correction edges without granting downstream progression", () => {
  const milestone = { kind: "milestone", milestone_id: "M1", status: "review-required", owner: "implement" };
  const state = compactSet({ currentStage: "code-review", activeWork: milestone });
  const correction = request(state, "advance-stage", { from_stage: "code-review", to_stage: "implement" });
  assert.equal(compactOperationEligibility(state.change, "advance-stage", correction).status, "permitted");
  const verify = request(state, "advance-stage", { from_stage: "code-review", to_stage: "verify" });
  assert.equal(compactOperationEligibility(state.change, "advance-stage", verify).status, "prohibited");

  state.change.current_stage = "review-resolution";
  const resolvedRoute = request(state, "advance-stage", { from_stage: "review-resolution", to_stage: "implement" });
  assert.equal(compactOperationEligibility(state.change, "advance-stage", resolvedRoute).status, "permitted");
});

test("CI and Verify edges are selected by remaining work instead of generic readiness", () => {
  const state = compactSet({ currentStage: "code-review", findingValues: {} });
  state.change.remaining_work = { CI1: { work_id: "CI1", kind: "task", owner: "ci-maintenance", required_action: "Add the required check", status: "pending" } };
  const ci = request(state, "advance-stage", { from_stage: "code-review", to_stage: "ci-maintenance" });
  assert.equal(compactOperationEligibility(state.change, "advance-stage", ci).status, "permitted");
  const verify = request(state, "advance-stage", { from_stage: "code-review", to_stage: "verify" });
  assert.equal(compactOperationEligibility(state.change, "advance-stage", verify).status, "prohibited");
});

test("advance-milestone selects one exact pending milestone and derives active work", () => {
  const state = compactSet({ currentStage: "implement", findingValues: {} });
  state.change.remaining_work = {
    M1: { work_id: "M1", kind: "milestone", owner: "implement", required_action: "Implement M1", status: "pending" },
    M2: { work_id: "M2", kind: "milestone", owner: "implement", required_action: "Implement M2", status: "pending" },
  };
  refreshCompactSet(state);
  const operation = request(state, "advance-milestone", { milestone_id: "M2", from_status: null, to_status: "planned" });
  assert.equal(compactOperationEligibility(state.change, "advance-milestone", operation).status, "permitted");
  const candidate = evaluateCompactOperation({ request: operation, currentFiles: state.files });
  assert.deepEqual(candidate.change.active_work, { kind: "milestone", milestone_id: "M2", status: "planned", owner: "implement" });
  assert.deepEqual(Object.keys(candidate.change.remaining_work), ["M1"]);
});

test("advance-milestone rejects invalid pending selections unchanged", () => {
  const variants = [
    ["missing", {}],
    ["blocked", { M1: { work_id: "M1", kind: "milestone", owner: "implement", required_action: "Implement M1", status: "blocked" } }],
    ["wrong-kind", { M1: { work_id: "M1", kind: "task", owner: "implement", required_action: "Implement M1", status: "pending" } }],
    ["wrong-owner", { M1: { work_id: "M1", kind: "milestone", owner: "plan", required_action: "Implement M1", status: "pending" } }],
  ];
  for (const [label, remainingWork] of variants) {
    const state = compactSet({ currentStage: "implement", findingValues: {} });
    state.change.remaining_work = remainingWork;
    refreshCompactSet(state);
    const before = Buffer.from(state.files[changePath]);
    const operation = request(state, "advance-milestone", { milestone_id: "M1", from_status: null, to_status: "planned" });
    assert.equal(compactOperationEligibility(state.change, "advance-milestone", operation).status, "prohibited", label);
    assert.throws(() => evaluateCompactOperation({ request: operation, currentFiles: state.files }), /pending milestone|structurally eligible/, label);
    assert.deepEqual(state.files[changePath], before, label);
  }
});

test("advance-milestone selection retries fail stale and reviewed closure clears active work", () => {
  let state = compactSet({ currentStage: "implement", findingValues: {} });
  state.change.remaining_work = { M1: { work_id: "M1", kind: "milestone", owner: "implement", required_action: "Implement M1", status: "pending" } };
  refreshCompactSet(state);
  const selection = request(state, "advance-milestone", { milestone_id: "M1", from_status: null, to_status: "planned" });
  const selected = evaluateCompactOperation({ request: selection, currentFiles: state.files });
  assert.throws(() => evaluateCompactOperation({ request: selection, currentFiles: selected.candidateSet }), /stale/);

  const approved = review({ outcome: "approved", findings: {} });
  state = compactSet({ currentStage: "code-review", activeWork: { kind: "milestone", milestone_id: "M1", status: "review-required", owner: "implement" }, reviewBytes: approved, findingValues: {} });
  const close = request(state, "advance-milestone", { milestone_id: "M1", from_status: "review-required", to_status: "closed" });
  assert.equal(evaluateCompactOperation({ request: close, currentFiles: state.files }).change.active_work, null);
});

test("the complete current set rejects mismatched review responsibility and unstable review paths", () => {
  const state = compactSet({ findingValues: {} });
  const wrongAuthority = structuredClone(state.change);
  const wrongAuthorityBytes = Buffer.from(review({ findings: {} }).replace("reviewer_authority: code-review", "reviewer_authority: proposal-review"));
  wrongAuthority.reviews.M1.reviewer_authority = "proposal-review";
  wrongAuthority.reviews.M1.identity = hash(wrongAuthorityBytes);
  wrongAuthority.lifecycle_revision = sentinel;
  assert.throws(() => validateCompactSet({ changeBytes: serializeLifecycleYaml(wrongAuthority), files: { [reviewPath]: wrongAuthorityBytes } }), /responsibility is inconsistent/);

  const wrongPath = structuredClone(state.change);
  wrongPath.reviews.M1.path = "docs/changes/example/reviews/code-review-M1-r1.md";
  wrongPath.lifecycle_revision = sentinel;
  assert.throws(() => validateCompactSet({ changeBytes: serializeLifecycleYaml(wrongPath), files: { "docs/changes/example/reviews/code-review-M1-r1.md": state.files[reviewPath] } }), /stable canonical path/);
});

test("artifact authoring and review handoff derive review-required instead of accepting a claimed settled status", () => {
  const state = evidenceSet({ currentStage: "spec" });
  const content = "revised specification\n";
  const artifact = { ...state.change.artifacts.spec, identity: hash(content), status: "approved" };
  const input = { path: state.artifactPath, identity: hash(content), source: "inline", content, source_path: null };
  const operation = request(state, "record-artifact", { artifact, content: input });
  assert.equal(compactOperationEligibility(state.change, "record-artifact", operation).status, "prohibited");

  state.change.artifacts.spec.status = "approved";
  const advance = request(state, "advance-stage", { from_stage: "spec", to_stage: "design-review" });
  assert.equal(compactOperationEligibility(state.change, "advance-stage", advance).status, "prohibited");
  state.change.artifacts.spec.status = "review-required";
  assert.equal(compactOperationEligibility(state.change, "advance-stage", advance).status, "permitted");
});

test("review settlement derives the reviewed artifact lifecycle status", () => {
  const artifactPath = "docs/proposals/example.md";
  const stableReviewPath = "docs/changes/example/reviews/proposal-review.md";
  const artifactBytes = Buffer.from("# Proposal\n");
  const reviewRecord = { schema: "compact-review-v1", review_id: "proposal-review-1", target: { target_id: "proposal", target_kind: "proposal" }, round: 1, subjects: { proposal: { subject_id: "proposal", path: artifactPath, identity: hash(artifactBytes) } }, reviewer_authority: "proposal-review", outcome: "approved", recording_status: "recorded", open_findings: {}, material_decisions: [], limitations: [], recorded_at: "2026-09-04T00:00:00Z" };
  const reviewBytes = Buffer.from(`---\n${serializeLifecycleYaml(reviewRecord)}---\n`);
  const change = { schema: "compact-change-v1", change_id: "example", title: "Example", lifecycle_contract: "compact-current-state-v1", lifecycle_revision: sentinel, current_stage: "proposal-review", artifacts: { proposal: { artifact_id: "proposal", kind: "proposal", role: "primary", path: artifactPath, identity: hash(artifactBytes), owner: "proposal", status: "review-required" } }, reviews: { proposal: { target_id: "proposal", path: stableReviewPath, identity: hash(reviewBytes), review_id: "proposal-review-1", outcome: "approved", reviewer_authority: "proposal-review", status: "current" } }, active_work: null, open_findings: {}, material_decisions: {}, evidence: {}, blockers: [], remaining_work: {}, readiness: "not-ready" };
  const authoritative = { [artifactPath]: artifactBytes, [stableReviewPath]: reviewBytes };
  change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(change), files: authoritative }).revision;
  const files = { [changePath]: Buffer.from(serializeLifecycleYaml(change)), ...authoritative };
  const state = { change, files };
  const operation = request(state, "settle-review", { target_id: "proposal", review_id: "proposal-review-1", outcome: "approved" });
  const candidate = evaluateCompactOperation({ request: operation, currentFiles: files });
  assert.equal(candidate.change.artifacts.proposal.status, "accepted");
});
