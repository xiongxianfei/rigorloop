import assert from "node:assert/strict";
import { mkdirSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import { test } from "node:test";

import { compactLifecycleRevision } from "../dist/lib/compact-contract.js";
import { loadPackagedCompactActivation } from "../dist/lib/compact-activation.js";
import { executeCompactCli } from "../dist/lib/compact-cli.js";
import { evaluateCompactOperation } from "../dist/lib/compact-operations.js";
import { runCompactTransaction } from "../dist/lib/compact-transaction.js";
import { serializeLifecycleYaml } from "../dist/lib/lifecycle-contract.js";
import { compactHash, correctionRequest, writeCompactFixture } from "./helpers/compact-fixture.js";

const cli = new URL("../dist/bin/rigorloop.js", import.meta.url).pathname;

function run(root, args, input = null) {
  return spawnSync(process.execPath, [cli, ...args], { cwd: root, encoding: "utf8", input, env: { ...process.env, RIGORLOOP_LOG_DIR: join(root, ".local-logs") } });
}

test("bounded project reports blocked progression and permitted correction independently", async () => {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-cli-"));
  writeCompactFixture(root);
  const execution = run(root, ["compact", "project", "--change", "example", "--view", "skill-context", "--requested-operation", "route-correction", "--format", "json"]);
  assert.equal(execution.status, 0, execution.stderr);
  const result = JSON.parse(execution.stdout);
  assert.equal(result.projection.progression_status, "blocked");
  assert.equal(result.projection.operation_eligibility.status, "permitted");
  assert.ok(result.projection.permitted_operations.includes("route-correction"));
  assert.equal(result.projection.requested_operation, "route-correction");
});

test("workflow-context delegates exact compact candidates to the bounded current-state projection", async () => {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-context-"));
  writeCompactFixture(root);
  const execution = run(root, ["workflow-context", "--change", "example", "--format", "json"]);
  assert.equal(execution.status, 0, execution.stderr);
  const result = JSON.parse(execution.stdout);
  assert.equal(result.lifecycle_contract.contract_class, "compact-current-state-v1");
  assert.equal(result.compact_projection.progression_status, "blocked");
  assert.ok(result.permitted_operations.includes("route-correction"));

  const discovered = run(root, ["workflow-context", "--format", "json"]);
  assert.equal(discovered.status, 0, discovered.stderr);
  const project = JSON.parse(discovered.stdout);
  assert.equal(project.selection.state, "single-candidate");
  assert.deepEqual(project.candidates.map((candidate) => candidate.change_id), ["example"]);
});

test("bounded projections are identical for equal current state with unequal disposable history", async () => {
  const leanRoot = await mkdtemp(join(tmpdir(), "rigorloop-compact-lean-"));
  const noisyRoot = await mkdtemp(join(tmpdir(), "rigorloop-compact-noisy-"));
  writeCompactFixture(leanRoot);
  writeCompactFixture(noisyRoot);
  for (let round = 1; round <= 250; round += 1) {
    const requestPath = join(noisyRoot, `docs/changes/example/requests/operation-${round}.json`);
    const reviewPath = join(noisyRoot, `docs/changes/example/disposable-history/code-review-M1-r${round}.md`);
    mkdirSync(join(requestPath, ".."), { recursive: true });
    mkdirSync(join(reviewPath, ".."), { recursive: true });
    writeFileSync(requestPath, JSON.stringify({ round, diagnostic: "not authoritative" }));
    writeFileSync(reviewPath, `# Superseded round ${round}\n`);
  }

  const args = ["compact", "project", "--change", "example", "--view", "skill-context", "--format", "json"];
  const lean = run(leanRoot, args);
  const noisy = run(noisyRoot, args);
  assert.equal(lean.status, 0, lean.stderr);
  assert.equal(noisy.status, 0, noisy.stderr);
  assert.deepEqual(JSON.parse(noisy.stdout).projection, JSON.parse(lean.stdout).projection);
  assert.ok(Buffer.byteLength(noisy.stdout) < 16 * 1024);
});

test("argument, stdin, and temporary-file transports apply identical correction semantics without retaining requests", async () => {
  for (const transport of ["argument", "stdin", "file"]) {
    const root = await mkdtemp(join(tmpdir(), `rigorloop-compact-${transport}-`));
    const fixture = writeCompactFixture(root);
    const request = JSON.stringify(correctionRequest(fixture));
    let execution;
    if (transport === "argument") execution = run(root, ["compact", "apply", "--request-json", request, "--format", "json"]);
    else if (transport === "stdin") execution = run(root, ["compact", "apply", "--request", "-", "--format", "json"], request);
    else {
      writeFileSync(join(root, "request.json"), request);
      execution = run(root, ["compact", "apply", "--request", "request.json", "--format", "json"]);
    }
    assert.equal(execution.status, 0, `${transport}: ${execution.stdout}${execution.stderr}`);
    const result = JSON.parse(execution.stdout);
    assert.equal(result.status, "success");
    const changed = readFileSync(join(root, fixture.changePath), "utf8");
    assert.match(changed, /kind: correction/);
    assert.match(changed, /status: authoring/);
    assert.match(changed, /current_stage: implement/);
    assert.equal(changed.includes("request.json"), false);
  }
});

test("writer rollback rejects apply while preserving compact projection", async () => {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-rollback-"));
  const fixture = writeCompactFixture(root);
  const activation = { ...loadPackagedCompactActivation(), state: "withheld" };
  const projected = executeCompactCli(["project", "--change", "example", "--view", "summary", "--format", "json"], { cwd: root, activation });
  assert.equal(projected.exitCode, 0);
  const applied = executeCompactCli(["apply", "--request-json", JSON.stringify(correctionRequest(fixture)), "--format", "json"], { cwd: root, activation });
  assert.equal(applied.exitCode, 2);
  assert.equal(applied.result.errors[0].code, "RL_INCOMPATIBLE_VERSION");
});

test("public recovery status exposes the bounded recovery identity and the action restores a valid compact set", async () => {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-public-recovery-"));
  const fixture = writeCompactFixture(root);
  const request = correctionRequest(fixture);
  const candidate = evaluateCompactOperation({ request, currentFiles: fixture.files });
  const crashed = runCompactTransaction({ root, candidate, validateCandidateSet: () => true, fault: (point) => point === "after-recovery-prepared" ? "crash" : null });
  assert.equal(crashed.status, "recovery-required");
  unlinkSync(join(root, ".rigorloop/transactions/example/lock"));

  const status = run(root, ["compact", "recover", "--change", "example", "--format", "json"]);
  assert.equal(status.status, 2);
  const statusResult = JSON.parse(status.stdout);
  assert.equal(statusResult.status, "recovery-required");
  assert.equal(statusResult.next_operation, "recover");
  assert.match(statusResult.errors[0].identities[0], /^sha256:[a-f0-9]{64}$/);

  const recovery = run(root, ["compact", "recover", "--change", "example", "--action", "restore-prior", "--expected-recovery-identity", statusResult.errors[0].identities[0], "--format", "json"]);
  assert.equal(recovery.status, 0, `${recovery.stdout}${recovery.stderr}`);
  assert.equal(JSON.parse(recovery.stdout).status, "success");
  assert.equal(readFileSync(join(root, fixture.changePath), "utf8"), fixture.files[fixture.changePath].toString("utf8"));
});

test("an evidence projection hashes only its declared subject and reports bounded drift without mutation", async () => {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-compact-drift-"));
  const changePath = "docs/changes/drift/change.yaml";
  const evidencePath = "docs/changes/drift/evidence.yaml";
  const subjectPath = "observed/current.txt";
  const recordedSubject = Buffer.from("recorded\n");
  const evidenceRecord = { schema: "compact-evidence-v1", evidence: { EV1: { evidence_id: "EV1", verifies: ["SR-15"], subjects: { output: { subject_id: "output", path: subjectPath, identity: compactHash(recordedSubject) } }, method: "focused check", outcome: "passed", surfaces: ["evidence-freshness"], freshness: "current", invalidating_dependencies: [{ kind: "subject", id: "output", identity: compactHash(recordedSubject) }], producer_authority: "implement", detail_location: null, required_rerun: null } } };
  const evidence = Buffer.from(serializeLifecycleYaml(evidenceRecord));
  const change = { schema: "compact-change-v1", change_id: "drift", title: "Drift", lifecycle_contract: "compact-current-state-v1", lifecycle_revision: `sha256:${"0".repeat(64)}`, current_stage: "verify", artifacts: {}, reviews: {}, active_work: null, open_findings: {}, material_decisions: {}, evidence: { EV1: { evidence_id: "EV1", manifest_path: evidencePath, manifest_identity: compactHash(evidence), freshness: "current" } }, blockers: [], remaining_work: {}, readiness: "not-ready" };
  change.lifecycle_revision = compactLifecycleRevision({ changeBytes: serializeLifecycleYaml(change), files: { [evidencePath]: evidence } }).revision;
  for (const path of [changePath, evidencePath, subjectPath]) mkdirSync(join(root, path, ".."), { recursive: true });
  writeFileSync(join(root, changePath), serializeLifecycleYaml(change));
  writeFileSync(join(root, evidencePath), evidence);
  writeFileSync(join(root, subjectPath), "changed\n");

  const execution = run(root, ["compact", "project", "--change", "drift", "--view", "evidence", "--format", "json"]);
  assert.equal(execution.status, 0, execution.stderr);
  const projected = JSON.parse(execution.stdout).projection;
  assert.equal(projected.evidence.EV1.freshness, "stale");
  assert.equal(projected.progression_status, "blocked");
  assert.equal(projected.blockers[0].code, "RL_EVIDENCE_DRIFT");
  assert.deepEqual(projected.required_paths, [changePath, evidencePath, subjectPath]);
  assert.match(readFileSync(join(root, evidencePath), "utf8"), /freshness: current/);

  const context = run(root, ["workflow-context", "--change", "drift", "--format", "json"]);
  assert.equal(context.status, 0, context.stderr);
  const contextProjection = JSON.parse(context.stdout).compact_projection;
  assert.equal(contextProjection.evidence.EV1.freshness, "stale");
  assert.equal(contextProjection.progression_status, "blocked");
  assert.equal(contextProjection.blockers[0].code, "RL_EVIDENCE_DRIFT");
});
