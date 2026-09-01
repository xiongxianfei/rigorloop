import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import {
  evaluateEvidenceDecision,
  parseVerifyReport,
  renderVerifyReport,
  replayDisposition,
  tailDisposition,
  validateFinalVerificationResult,
} from "../dist/lib/final-verification-protocol.js";

const alwaysCurrent = ["current-change-and-repository-identity", "reviewed-subject-and-review-identity", "lifecycle-and-package-consistency", "review-closeout", "unresolved-blocker-state", "final-diff-classification", "required-artifact-and-evidence-existence", "complete-verify-result-consistency"];

function success() {
  const impact = [{ surface: "runtime-behavior", state: "unaffected", rationale: "Tail cannot alter runtime inputs.", affirmative_evidence: ["TG-06"] }];
  const evidence = [{ evidence_id: "TG-06", proved_surfaces: ["runtime-behavior"], freshness: "impact-sensitive", existing_result: "pass", authority_current: true, identity_current: true, environment_current: true, conflicting: false, new_obligation: false, decision: "reuse", decision_rationale: "Affirmative non-impact proof.", execution: "reused-pass", observed_result: "pass", cache_hit: false, proof: { kind: "prior-evidence", evidence_path: "docs/changes/example/evidence/tg-06.md", evidence_sha256: `sha256:${"3".repeat(64)}`, subject_revision: "a".repeat(40) } }];
  return {
    protocol_version: 3,
    outcome: "successful",
    basis: { repository_identity: `repo:sha256:${"1".repeat(64)}`, remote_identity: `remote:sha256:${"2".repeat(64)}`, base_branch: "main", base_revision: "d".repeat(40), merge_base_revision: "e".repeat(40), head_branch: "proposal/example", verified_subject_revision: "a".repeat(40), governed_change_id: "example", final_review_id: "code-review-r1", design_package_id: "design-review-r1", delivery_plan_id: "docs/plans/example.md", final_diff_sha256: `sha256:${"b".repeat(64)}` },
    basis_status: { repository: "current", governed_change: "current", verified_subject: "current", final_review: "current", design_package: "current", delivery_plan: "current", final_diff: "current" },
    impact,
    evidence,
    always_current: alwaysCurrent.map((check_id) => ({ check_id, execution: "actual-run", observed_result: "pass", proof: { kind: "command", command: ["npm", "test"], evidence_path: "docs/changes/example/evidence/always-current.md", evidence_sha256: `sha256:${"4".repeat(64)}` } })),
    ci_status: "not-required",
    blockers: [],
    residual_risks: ["Semantic judgment remains reviewable."],
    branch_ready: true,
    explanation: { what_changed: "Protocol", why: "Safety", requirements_and_design: "FV-R8", important_choices: "Conservative", supporting_evidence: ["TG-06"], limitations: ["Inactive"], residual_risks: ["Review"] },
  };
}

test("v3 protocol rejects every unknown closed vocabulary", () => {
  const mutations = [
    ["impact surface", (r) => { r.impact[0].surface = "magic"; }, "impact[0].surface: unknown_value magic"],
    ["impact state", (r) => { r.impact[0].state = "maybe"; }, "impact[0].state: unknown_value maybe"],
    ["freshness", (r) => { r.evidence[0].freshness = "eventual"; }, "evidence[0].freshness: unknown_value eventual"],
    ["decision", (r) => { r.evidence[0].decision = "skip"; }, "evidence[0].decision: unknown_value skip"],
    ["result", (r) => { r.evidence[0].observed_result = "mostly"; }, "evidence[0].observed_result: unknown_value mostly"],
    ["execution", (r) => { r.evidence[0].execution = "assumed"; }, "evidence[0].execution: unknown_value assumed"],
    ["outcome", (r) => { r.outcome = "mostly"; }, "outcome: unknown_value mostly"],
    ["authority", (r) => { r.basis_status.final_diff = "maybe"; }, "basis_status.final_diff: unknown_value maybe"],
    ["ci", (r) => { r.ci_status = "maybe"; }, "ci_status: unknown_value maybe"],
    ["always-current", (r) => { r.always_current[0].check_id = "maybe"; }, "always_current[0].check_id: unknown_value maybe"],
    ["proof", (r) => { r.evidence[0].proof = { kind: "asserted" }; }, "evidence[0].proof.kind: unknown_value asserted"],
  ];
  for (const [name, mutate, expected] of mutations) {
    const result = success(); mutate(result);
    assert.equal(validateFinalVerificationResult(result)[0], expected, name);
  }
});

test("unknown impact and freshness override reuse while filenames grant no shortcut", () => {
  const result = success();
  result.impact[0] = { surface: "repository-metadata", state: "unaffected", rationale: ".gitignore", affirmative_evidence: [] };
  assert.ok(validateFinalVerificationResult(result).includes("impact[0].unaffected: affirmative_evidence required"));
  const obligation = success().evidence[0];
  assert.equal(evaluateEvidenceDecision(obligation, [{ ...success().impact[0], state: "unknown" }]), "rerun");
  assert.equal(evaluateEvidenceDecision({ ...obligation, freshness: "fresh-required" }, success().impact), "rerun");
});

test("cache-only required execution cannot support success", () => {
  const result = success();
  Object.assign(result.evidence[0], { freshness: "fresh-required", decision: "rerun", execution: "cache-hit", cache_hit: true, proof: { kind: "cache", cache_key: `sha256:${"6".repeat(64)}` } });
  assert.ok(validateFinalVerificationResult(result).includes("evidence[0].execution: rerun requires actual-run or hosted-observation"));
});

test("non-success omits explanation and readiness", () => {
  for (const outcome of ["failed", "inconclusive", "interrupted"]) {
    const result = success();
    Object.assign(result, { outcome, branch_ready: false, blockers: ["owner: plan"], explanation: null });
    assert.deepEqual(validateFinalVerificationResult(result), []);
  }
});

test("early inconclusive result records unresolved inputs without invented identities", () => {
  const result = success();
  Object.assign(result, { outcome: "inconclusive", impact: [], evidence: [], always_current: [], blockers: ["owner: workflow"], branch_ready: false, explanation: null });
  for (const key of Object.keys(result.basis)) result.basis[key] = null;
  for (const key of Object.keys(result.basis_status)) result.basis_status[key] = "missing";
  assert.deepEqual(validateFinalVerificationResult(result), []);
});

test("success round trips, replay is idempotent, and drift stales", () => {
  const result = success();
  assert.deepEqual(validateFinalVerificationResult(result), []);
  const parsed = parseVerifyReport(renderVerifyReport(result));
  assert.deepEqual(parsed, result);
  assert.equal(replayDisposition(result, parsed), "identical-replay");
  const changed = structuredClone(result); changed.basis.final_diff_sha256 = `sha256:${"c".repeat(64)}`;
  assert.equal(replayDisposition(result, changed), "changed-basis");
  const report = renderVerifyReport(result);
  const reportSha = `sha256:${createHash("sha256").update(report).digest("hex")}`;
  const tail = { changed_paths: ["docs/changes/example/verify-report.md", "docs/changes/example/change.yaml#lifecycle_cli.validations.verify-result"], report_path: "docs/changes/example/verify-report.md", report_content: report, report_sha256: reportSha, registration: { selector: "lifecycle_cli.validations.verify-result", evidence_path: "docs/changes/example/verify-report.md", evidence_sha256: reportSha, verified_subject_revision: "a".repeat(40), stage_authority: "verify" } };
  assert.equal(tailDisposition(tail, "example", "a".repeat(40)), "current");
  assert.equal(tailDisposition({ ...tail, changed_paths: ["src/product.js"] }, "example", "a".repeat(40)), "stale");
  assert.equal(tailDisposition({ ...tail, changed_paths: [tail.report_path] }, "example", "a".repeat(40)), "incomplete");
  assert.equal(tailDisposition({ ...tail, changed_paths: [tail.changed_paths[1]] }, "example", "a".repeat(40)), "incomplete");
  assert.equal(tailDisposition({ ...tail, changed_paths: [tail.report_path, tail.report_path] }, "example", "a".repeat(40)), "incomplete");
  assert.equal(tailDisposition({ ...tail, registration: { ...tail.registration, evidence_sha256: `sha256:${"0".repeat(64)}` } }, "example", "a".repeat(40)), "incomplete");
  result.report_commit_identity = "f".repeat(40);
  assert.ok(validateFinalVerificationResult(result).includes("result: Verify report must not embed its own Git commit identity"));
});

test("review counterexamples fail closed", () => {
  for (const proved_surfaces of [["magic-surface"], ["runtime-behavior", "runtime-behavior"], ["generated-output"]]) {
    const result = success();
    Object.assign(result.evidence[0], { proved_surfaces, freshness: "fresh-required", decision: "rerun", execution: "actual-run", proof: { kind: "command", command: ["npm", "test"], evidence_path: "docs/changes/example/evidence/test.md", evidence_sha256: `sha256:${"5".repeat(64)}` } });
    assert.notDeepEqual(validateFinalVerificationResult(result), []);
  }
  assert.throws(() => evaluateEvidenceDecision({ ...success().evidence[0], freshness: "fresh-required", proved_surfaces: ["magic-surface"] }, success().impact), /unknown_value magic-surface/);
  const missingProof = success(); missingProof.evidence[0].proof = null;
  assert.ok(validateFinalVerificationResult(missingProof).some((error) => error.includes("proof")));
  const duplicate = success(); duplicate.always_current.push(structuredClone(duplicate.always_current[0]));
  assert.ok(validateFinalVerificationResult(duplicate).includes("always_current[8].check_id: duplicate current-change-and-repository-identity"));
  for (const value of ["   ", ["valid", "   "]]) {
    const result = success(); result.explanation.what_changed = value;
    assert.ok(validateFinalVerificationResult(result).includes("successful result explanation fields must be non-empty"));
  }
  for (const [field, value] of [["repository_identity", "github.com/example/project"], ["remote_identity", "origin"], ["base_branch", "refs/../main"], ["head_branch", "feature.lock"], ["base_revision", "not-a-revision"], ["merge_base_revision", "abc"], ["verified_subject_revision", "x"], ["final_review_id", "review/r1"], ["design_package_id", "design r1"], ["final_diff_sha256", "not-a-digest"], ["delivery_plan_id", "../plan.md"], ["governed_change_id", 12]]) {
    const result = success(); result.basis[field] = value;
    assert.ok(validateFinalVerificationResult(result).some((error) => error.startsWith(`basis.${field}:`)), field);
  }
  assert.throws(() => parseVerifyReport(`${renderVerifyReport(success())}trailing\n`), /trailing or malformed content/);
});

test("collection shapes are required for every outcome", () => {
  for (const field of ["impact", "evidence", "always_current"]) {
    for (const value of [null, "items", { item: true }, 1]) {
      const result = success();
      Object.assign(result, { outcome: "inconclusive", branch_ready: false, blockers: ["owner: workflow"], explanation: null, [field]: value });
      assert.ok(validateFinalVerificationResult(result).includes(`${field}: expected array`), `${field}: ${JSON.stringify(value)}`);
    }
    const empty = success(); empty[field] = [];
    assert.notDeepEqual(validateFinalVerificationResult(empty), [], `successful ${field}`);
  }
  const inconclusive = success();
  Object.assign(inconclusive, { outcome: "inconclusive", branch_ready: false, blockers: ["owner: workflow"], explanation: null, impact: [], evidence: [], always_current: [] });
  assert.deepEqual(validateFinalVerificationResult(inconclusive), []);
});

test("evidence facts require JSON booleans", () => {
  const fields = ["authority_current", "identity_current", "environment_current", "conflicting", "new_obligation", "cache_hit"];
  for (const field of fields) {
    for (const value of ["yes", 1, null, {}, []]) {
      const result = success(); result.evidence[0][field] = value;
      assert.ok(validateFinalVerificationResult(result).includes(`evidence[0].${field}: expected boolean`), `${field}: ${JSON.stringify(value)}`);
    }
    for (const value of [true, false]) {
      const result = success(); result.evidence[0][field] = value;
      assert.ok(!validateFinalVerificationResult(result).includes(`evidence[0].${field}: expected boolean`), `${field}: ${value}`);
    }
  }
  assert.throws(() => evaluateEvidenceDecision({ ...success().evidence[0], authority_current: "yes" }, success().impact), /authority_current: expected boolean/);
});
