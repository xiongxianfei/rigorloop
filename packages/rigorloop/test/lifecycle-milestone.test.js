import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml, serializeLifecycleYaml } from "../dist/lib/lifecycle-contract.js";
import { writeActiveV3Manifests } from "./helpers/lifecycle-package-fixture.js";

async function fixture(m2State = "planned", reviewStatus = "not-started", currentStage = "implement") {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-lifecycle-milestone-"));
  writeActiveV3Manifests(root);
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(join(changeRoot, "evidence"), { recursive: true });
  mkdirSync(join(changeRoot, "reviews"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });
  writeFileSync(join(changeRoot, "evidence", "m2.md"), "Milestone: M2\nValidation result: passed\n", "utf8");
  writeFileSync(join(changeRoot, "change.yaml"), `change_id: example
title: Example
classification: feature
risk: standard
lifecycle_contract: stage-owned-change-local-v3
artifact_states: {}
workflow_state:
  lifecycle_state: active
  current_stage: ${currentStage}
  next_stage: code-review
  blocker: null
  evidence: []
  planned_work:
    current_milestone: M2
    milestones:
      M1:
        kind: implementation
        state: closed
      M2:
        kind: implementation
        state: ${m2State}
      M3:
        kind: implementation
        state: planned
    remaining_implementation_milestones:
      - M2
      - M3
    latest_review:
      status: ${reviewStatus}
      stage: code-review
      round: r1
      artifact_id: plan
      occurrence: milestone
      milestone_id: M2
      evidence: []
    final_closeout:
      readiness: not-ready
      reasons:
        - lifecycle-gates-open
      evidence: []
`, "utf8");
  return { root, changeRoot };
}

function revision(root) { return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.lifecycle_revision; }
function request(root, name, body) { const path = `requests/${name}.json`; writeFileSync(join(root, path), JSON.stringify(body), "utf8"); return path; }
function writeReview(root, changeRoot, overrides = {}) {
  const source = "docs/changes/example/evidence/m2.md";
  const contextPath = "docs/changes/example/evidence/context.md";
  writeFileSync(join(root, contextPath), "Context: stable\n", "utf8");
  const sourceHash = createHash("sha256").update(readFileSync(join(root, source))).digest("hex");
  const contextHash = createHash("sha256").update(readFileSync(join(root, contextPath))).digest("hex");
  const inventory = `${source}@working-tree#sha256:${sourceHash}; ${contextPath}@working-tree#sha256:${contextHash}`;
  const inventoryHash = createHash("sha256").update(inventory).digest("hex");
  const reviewPath = "docs/changes/example/reviews/code-review-m2-r2.md";
  writeFileSync(join(root, reviewPath), `Review ID: code-review-m2-r2
Stage: code-review
Round: r2
Reviewed milestone: ${overrides.milestone ?? "M2"}
Review status: ${overrides.outcome ?? "clean-with-notes"}
Recording status: recorded
Material findings: ${overrides.findings ?? "none"}
${overrides.direct ? "" : `Review gate outcome: ${overrides.gate ?? "advance"}\nInitial packet inventory: ${inventory}\nInitial packet hash: sha256:${inventoryHash}\n`}
`, "utf8");
  const tableLog = `| Review ID | Stage | Round | Reviewed artifact | Record | Status | Material findings | Recording |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| \`code-review-m2-r2\` | \`${overrides.logStage ?? "code-review"}\` | \`${overrides.logRound ?? "r2"}\` | M2 bundle | \`${overrides.logRecord ?? "reviews/code-review-m2-r2.md"}\` | \`${overrides.logOutcome ?? overrides.outcome ?? "clean-with-notes"}\` | ${overrides.logFindings ?? (overrides.openFindings ? 1 : overrides.findings && overrides.findings !== "none" ? 1 : 0)} | \`${overrides.logRecording ?? "recorded"}\` |
`;
  const proseLog = `### Review entry

Review ID: code-review-m2-r2
Stage: ${overrides.logStage ?? "code-review"}
Round: ${overrides.logRound ?? "r2"}
Status: ${overrides.logOutcome ?? overrides.outcome ?? "clean-with-notes"}
Detailed record: ${overrides.logRecord ?? "reviews/code-review-m2-r2.md"}
${overrides.omitMaterial ? "" : `Material findings: ${overrides.findings ?? "none"}\n`}${overrides.omitOpen ? "" : `Open findings: ${overrides.openFindings ?? "none"}\n`}Recording status: ${overrides.logRecording ?? "recorded"}
`;
  writeFileSync(join(changeRoot, "review-log.md"), overrides.logFormat === "prose" ? proseLog : tableLog, "utf8");
  return { reviewPath, source, contextPath, logPath: "docs/changes/example/review-log.md" };
}

function setAutomation(changeRoot, currentStage, status = "active") {
  const changePath = join(changeRoot, "change.yaml");
  const change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  change.workflow = { automation: { current_stage: currentStage, mechanism: "bounded-review-fix", status } };
  writeFileSync(changePath, serializeLifecycleYaml(change), "utf8");
}

function projectReview(changeRoot, reviewPath, status = "approved") {
  const changePath = join(changeRoot, "change.yaml");
  const change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  change.workflow_state.planned_work.latest_review = {
    artifact_id: "plan",
    evidence: [reviewPath],
    milestone_id: "M2",
    occurrence: "milestone",
    round: "r2",
    stage: "code-review",
    status,
  };
  writeFileSync(changePath, serializeLifecycleYaml(change), "utf8");
}

test("start milestone enforces current selection and predecessor order", async () => {
  const { root, changeRoot } = await fixture();
  const path = request(root, "start", { schema_version: 1, operation: "start-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", stage_authority: "workflow" });
  assert.equal(executeLifecycleCli(["start-milestone", "--request", path], { cwd: root }).exitCode, 0);
  assert.match(readFileSync(join(changeRoot, "change.yaml"), "utf8"), /M2:\n\s+kind: implementation\n\s+state: implementing/);
  const wrong = request(root, "wrong", { schema_version: 1, operation: "start-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M3", stage_authority: "workflow" });
  assert.equal(executeLifecycleCli(["start-milestone", "--request", wrong], { cwd: root }).result.errors[0].code, "RL_MILESTONE_ORDER");
});

test("complete milestone hands validated implementation to code review before settlement", async () => {
  const { root, changeRoot } = await fixture("implementing", "not-started", "implement");
  const path = request(root, "request-review", { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", evidence_path: "docs/changes/example/evidence/m2.md", stage_authority: "workflow" });

  const execution = executeLifecycleCli(["complete-milestone", "--request", path], { cwd: root });

  assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  assert.equal(execution.result.mutation.status, "review-requested");
  const changed = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.match(changed, /M2:\n\s+kind: implementation\n\s+state: review-requested/);
  assert.match(changed, /current_stage: code-review/);
  assert.match(changed, /next_stage: code-review/);
  assert.match(changed, /current_milestone: M2/);
  assert.match(changed, /remaining_implementation_milestones:\n\s+- M2\n\s+- M3/);
});

test("complete milestone requires matching review and proof", async () => {
  const { root, changeRoot } = await fixture("review-requested", "approved", "code-review");
  const { reviewPath } = writeReview(root, changeRoot);
  projectReview(changeRoot, reviewPath);
  const path = request(root, "complete", { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", evidence_path: "docs/changes/example/evidence/m2.md", stage_authority: "workflow" });
  assert.equal(executeLifecycleCli(["complete-milestone", "--request", path], { cwd: root }).exitCode, 0);
  const changed = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.match(changed, /M2:\n\s+kind: implementation\n\s+state: closed/);
  assert.doesNotMatch(changed, /remaining_implementation_milestones:\n\s+- M2/);
  assert.match(changed, /current_milestone: M3/);
  assert.match(changed, /current_stage: code-review/);
});

test("complete milestone accepts a canonical direct clean review without automation gate fields", async () => {
  const { root, changeRoot } = await fixture("review-requested", "not-started", "code-review");
  const { reviewPath, source } = writeReview(root, changeRoot, { direct: true });
  const operation = { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" };

  const execution = executeLifecycleCli(["complete-milestone", "--request", request(root, "direct-clean", operation)], { cwd: root });

  assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  assert.match(readFileSync(join(changeRoot, "change.yaml"), "utf8"), /M2:\n\s+kind: implementation\n\s+state: closed/);
});

test("pre-projected completion revalidates its review evidence on replay", async () => {
  const { root, changeRoot } = await fixture("review-requested", "approved", "code-review");
  const { reviewPath, source } = writeReview(root, changeRoot);
  projectReview(changeRoot, reviewPath);
  const operation = { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", evidence_path: source, stage_authority: "workflow" };
  assert.equal(executeLifecycleCli(["complete-milestone", "--request", request(root, "projected-first", operation)], { cwd: root }).exitCode, 0);
  const settled = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  writeFileSync(join(root, reviewPath), `${readFileSync(join(root, reviewPath), "utf8")}Changed: yes\n`, "utf8");
  const replay = executeLifecycleCli(["complete-milestone", "--request", request(root, "projected-replay", { ...operation, expected_lifecycle_revision: revision(root) })], { cwd: root });
  assert.equal(replay.result.errors[0].code, "RL_STALE_EVIDENCE");
  assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), settled);
});

test("completion reports eligibility without routing and a later start synchronizes routing", async () => {
  const { root, changeRoot } = await fixture("review-requested", "not-started", "code-review");
  setAutomation(changeRoot, "code-review");
  const { reviewPath, source } = writeReview(root, changeRoot);
  const path = request(root, "complete-from-review", { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" });

  const completed = executeLifecycleCli(["complete-milestone", "--request", path], { cwd: root });
  assert.equal(completed.exitCode, 0);
  assert.equal(completed.result.operation_result.continuation_eligible, true);
  assert.equal(completed.result.operation_result.next_milestone, "M3");
  const changed = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.match(changed, /latest_review:\n\s+artifact_id: none\n\s+evidence: \[\]\n\s+milestone_id: none\n\s+occurrence: none\n\s+round: none\n\s+stage: none\n\s+status: not-started/);
  assert.match(changed, /M2:\n\s+completion_fingerprint: [a-f0-9]{64}/);
  assert.match(changed, /review_log_entry_sha256: [a-f0-9]{64}/);
  assert.match(changed, /packet_inventory:/);
  assert.match(changed, /M2:\n\s+kind: implementation\n\s+state: closed/);
  assert.match(changed, /current_milestone: M3/);
  assert.match(changed, /current_stage: code-review/);
  assert.match(changed, /next_stage: code-review/);
  assert.match(changed, /automation:\n\s+current_stage: code-review/);

  const start = request(root, "start-m3", { schema_version: 1, operation: "start-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M3", stage_authority: "workflow" });
  assert.equal(executeLifecycleCli(["start-milestone", "--request", start], { cwd: root }).exitCode, 0);
  const started = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  assert.match(started, /M3:\n\s+kind: implementation\n\s+state: implementing/);
  assert.match(started, /current_stage: implement/);
  assert.match(started, /next_stage: code-review/);
  assert.match(started, /automation:\n\s+current_stage: implement/);
});

test("start milestone rejects a contradictory active automation projection without mutation", async () => {
  const { root, changeRoot } = await fixture("planned", "not-started", "code-review");
  setAutomation(changeRoot, "spec-review");
  const before = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  const path = request(root, "contradictory-automation", { schema_version: 1, operation: "start-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", stage_authority: "workflow" });
  const result = executeLifecycleCli(["start-milestone", "--request", path], { cwd: root });
  assert.notEqual(result.exitCode, 0);
  assert.equal(result.result.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
  assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), before);
});

test("complete milestone rejects wrong, non-clean, open, and stale review evidence without mutation", async () => {
  for (const [name, overrides, stale] of [
    ["wrong", { milestone: "M3" }, false],
    ["non-clean", { outcome: "changes-requested", gate: "stop", findings: "F-1" }, false],
    ["open", { openFindings: "F-1" }, false],
    ["stale", {}, true],
  ]) {
    const { root, changeRoot } = await fixture("review-requested", "not-started");
    const { reviewPath, source } = writeReview(root, changeRoot, overrides);
    if (stale) writeFileSync(join(root, source), "Milestone: M2\nValidation result: passed\nchanged\n", "utf8");
    const before = readFileSync(join(changeRoot, "change.yaml"), "utf8");
    const path = request(root, name, { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" });
    assert.notEqual(executeLifecycleCli(["complete-milestone", "--request", path], { cwd: root }).exitCode, 0, name);
    assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), before, name);
  }
});

test("complete milestone binds a review receipt to every canonical review-log field", async () => {
  for (const [name, overrides] of [
    ["stage", { logStage: "spec-review" }],
    ["round", { logRound: "r9" }],
    ["outcome", { logOutcome: "changes-requested" }],
    ["record", { logRecord: "reviews/different.md" }],
    ["findings", { logFindings: 1 }],
    ["recording", { logRecording: "blocked" }],
  ]) {
    const { root, changeRoot } = await fixture("review-requested", "not-started");
    const { reviewPath, source } = writeReview(root, changeRoot, overrides);
    const before = readFileSync(join(changeRoot, "change.yaml"), "utf8");
    const path = request(root, `log-${name}`, { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" });
    assert.notEqual(executeLifecycleCli(["complete-milestone", "--request", path], { cwd: root }).exitCode, 0, name);
    assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), before, name);
  }
});

test("complete milestone rejects duplicate canonical review-log occurrences", async () => {
  const { root, changeRoot } = await fixture("review-requested", "not-started");
  const { reviewPath, source, logPath } = writeReview(root, changeRoot);
  const log = readFileSync(join(root, logPath), "utf8");
  const row = log.trimEnd().split("\n").at(-1);
  writeFileSync(join(root, logPath), `${log}${row}\n`, "utf8");
  const before = readFileSync(join(changeRoot, "change.yaml"), "utf8");
  const operation = { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" };
  const result = executeLifecycleCli(["complete-milestone", "--request", request(root, "duplicate-log", operation)], { cwd: root });
  assert.notEqual(result.exitCode, 0);
  assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), before);
});

test("milestone operations reject inconsistent remaining work and illegal completion source", async () => {
  const inconsistent = await fixture("planned", "not-started", "code-review");
  const inconsistentPath = join(inconsistent.changeRoot, "change.yaml");
  const inconsistentChange = parseLifecycleYaml(readFileSync(inconsistentPath, "utf8"));
  inconsistentChange.workflow_state.planned_work.remaining_implementation_milestones = ["M3"];
  writeFileSync(inconsistentPath, serializeLifecycleYaml(inconsistentChange), "utf8");
  const beforeStart = readFileSync(inconsistentPath, "utf8");
  const start = { schema_version: 1, operation: "start-milestone", change_id: "example", expected_lifecycle_revision: revision(inconsistent.root), milestone_id: "M2", stage_authority: "workflow" };
  assert.notEqual(executeLifecycleCli(["start-milestone", "--request", request(inconsistent.root, "bad-remaining", start)], { cwd: inconsistent.root }).exitCode, 0);
  assert.equal(readFileSync(inconsistentPath, "utf8"), beforeStart);

  const illegal = await fixture("implementing", "not-started", "code-review");
  const paths = writeReview(illegal.root, illegal.changeRoot);
  const beforeComplete = readFileSync(join(illegal.changeRoot, "change.yaml"), "utf8");
  const complete = { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(illegal.root), milestone_id: "M2", review_evidence_path: paths.reviewPath, evidence_path: paths.source, stage_authority: "workflow" };
  assert.notEqual(executeLifecycleCli(["complete-milestone", "--request", request(illegal.root, "illegal-source", complete)], { cwd: illegal.root }).exitCode, 0);
  assert.equal(readFileSync(join(illegal.changeRoot, "change.yaml"), "utf8"), beforeComplete);
});

test("complete milestone fails closed when canonical prose finding fields are missing", async () => {
  for (const [name, overrides] of [
    ["material", { logFormat: "prose", omitMaterial: true }],
    ["open", { logFormat: "prose", omitOpen: true }],
  ]) {
    const { root, changeRoot } = await fixture("review-requested", "not-started");
    const { reviewPath, source } = writeReview(root, changeRoot, overrides);
    const before = readFileSync(join(changeRoot, "change.yaml"), "utf8");
    const path = request(root, `missing-${name}`, { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" });
    assert.notEqual(executeLifecycleCli(["complete-milestone", "--request", path], { cwd: root }).exitCode, 0, name);
    assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), before, name);
  }
});

test("complete milestone revalidates its full evidence packet on every replay", async () => {
  const { root, changeRoot } = await fixture("review-requested", "not-started");
  const { reviewPath, source, logPath } = writeReview(root, changeRoot);
  const first = { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" };
  assert.equal(executeLifecycleCli(["complete-milestone", "--request", request(root, "first", first)], { cwd: root }).exitCode, 0);
  const settled = readFileSync(join(changeRoot, "change.yaml"), "utf8");

  const retry = { ...first, expected_lifecycle_revision: revision(root) };
  const retried = executeLifecycleCli(["complete-milestone", "--request", request(root, "retry", retry)], { cwd: root });
  assert.equal(retried.exitCode, 0);
  assert.equal(retried.result.status, "already-recorded");
  assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), settled);

  const omitted = { ...retry, expected_lifecycle_revision: revision(root) };
  delete omitted.review_evidence_path;
  const omission = executeLifecycleCli(["complete-milestone", "--request", request(root, "omission", omitted)], { cwd: root });
  assert.equal(omission.result.errors[0].code, "RL_STALE_EVIDENCE");
  assert.equal(readFileSync(join(changeRoot, "change.yaml"), "utf8"), settled);

  writeFileSync(join(root, logPath), `${readFileSync(join(root, logPath), "utf8")}\nUnrelated note.\n`, "utf8");
  const appendReplay = executeLifecycleCli(["complete-milestone", "--request", request(root, "append-replay", { ...retry, expected_lifecycle_revision: revision(root) })], { cwd: root });
  assert.equal(appendReplay.exitCode, 0);
  assert.equal(appendReplay.result.status, "already-recorded");

  for (const name of ["receipt", "log-entry", "proof", "packet"]) {
    const fresh = await fixture("review-requested", "not-started");
    const paths = writeReview(fresh.root, fresh.changeRoot);
    const operation = { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(fresh.root), milestone_id: "M2", review_evidence_path: paths.reviewPath, evidence_path: paths.source, stage_authority: "workflow" };
    assert.equal(executeLifecycleCli(["complete-milestone", "--request", request(fresh.root, `${name}-first`, operation)], { cwd: fresh.root }).exitCode, 0);
    const stable = readFileSync(join(fresh.changeRoot, "change.yaml"), "utf8");
    const target = { receipt: paths.reviewPath, "log-entry": paths.logPath, proof: paths.source, packet: paths.contextPath }[name];
    if (name === "receipt") writeFileSync(join(fresh.root, target), `${readFileSync(join(fresh.root, target), "utf8")}Changed: yes\n`, "utf8");
    if (name === "log-entry") writeFileSync(join(fresh.root, target), readFileSync(join(fresh.root, target), "utf8").replace("clean-with-notes", "approved"), "utf8");
    if (name === "proof") writeFileSync(join(fresh.root, target), "Milestone: M2\nValidation result: passed\nchanged\n", "utf8");
    if (name === "packet") writeFileSync(join(fresh.root, target), "Context: changed\n", "utf8");
    const result = executeLifecycleCli(["complete-milestone", "--request", request(fresh.root, `${name}-replay`, { ...operation, expected_lifecycle_revision: revision(fresh.root) })], { cwd: fresh.root });
    assert.equal(result.result.errors[0].code, "RL_STALE_EVIDENCE", name);
    assert.equal(readFileSync(join(fresh.changeRoot, "change.yaml"), "utf8"), stable, name);
  }
});

test("complete milestone upgrades a matching legacy registration without implicit routing", async () => {
  const { root, changeRoot } = await fixture("review-requested", "not-started", "code-review");
  const { reviewPath, source } = writeReview(root, changeRoot);
  const first = { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" };
  assert.equal(executeLifecycleCli(["complete-milestone", "--request", request(root, "reconcile-first", first)], { cwd: root }).exitCode, 0);
  const changePath = join(changeRoot, "change.yaml");
  const legacy = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  delete legacy.lifecycle_cli.milestones.M2.completion_fingerprint;
  delete legacy.lifecycle_cli.milestones.M2.review_log_entry_sha256;
  delete legacy.lifecycle_cli.milestones.M2.packet_inventory;
  delete legacy.lifecycle_cli.milestones.M2.packet_sha256;
  writeFileSync(changePath, serializeLifecycleYaml(legacy), "utf8");

  const older = executeLifecycleCli(["complete-milestone", "--request", request(root, "older-replay", { ...first, expected_lifecycle_revision: revision(root), milestone_id: "M1" })], { cwd: root });
  assert.notEqual(older.exitCode, 0);
  assert.match(readFileSync(changePath, "utf8"), /current_stage: code-review/);

  const reconciled = executeLifecycleCli(["complete-milestone", "--request", request(root, "reconcile", { ...first, expected_lifecycle_revision: revision(root) })], { cwd: root });
  assert.equal(reconciled.exitCode, 0);
  assert.equal(reconciled.result.mutation.status, "completed");
  assert.match(readFileSync(changePath, "utf8"), /current_stage: code-review/);
  assert.match(readFileSync(changePath, "utf8"), /completion_fingerprint: [a-f0-9]{64}/);
  assert.match(readFileSync(changePath, "utf8"), /status: not-started/);

  const replayed = executeLifecycleCli(["complete-milestone", "--request", request(root, "reconcile-replay", { ...first, expected_lifecycle_revision: revision(root) })], { cwd: root });
  assert.equal(replayed.exitCode, 0);
  assert.equal(replayed.result.status, "already-recorded");
});

test("complete final implementation milestone does not route lifecycle closeout to implement", async () => {
  const { root, changeRoot } = await fixture("review-requested", "not-started", "code-review");
  const changePath = join(changeRoot, "change.yaml");
  const change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  change.workflow_state.planned_work.milestones.M3.kind = "lifecycle-closeout";
  change.workflow_state.planned_work.remaining_implementation_milestones = ["M2"];
  writeFileSync(changePath, serializeLifecycleYaml(change), "utf8");
  const { reviewPath, source } = writeReview(root, changeRoot);
  const operation = { schema_version: 1, operation: "complete-milestone", change_id: "example", expected_lifecycle_revision: revision(root), milestone_id: "M2", review_evidence_path: reviewPath, evidence_path: source, stage_authority: "workflow" };

  assert.equal(executeLifecycleCli(["complete-milestone", "--request", request(root, "final-implementation", operation)], { cwd: root }).exitCode, 0);
  const changed = readFileSync(changePath, "utf8");
  assert.match(changed, /current_milestone: M3/);
  assert.match(changed, /current_stage: code-review/);
  assert.doesNotMatch(changed, /current_stage: implement/);
  assert.match(changed, /status: not-started/);
});
