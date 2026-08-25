import assert from "node:assert/strict";
import test from "node:test";

import { projectConciseResult, renderResult, RESULT_FORMATS } from "../dist/lib/result-renderer.js";

const detailed = {
  schema_version: 1,
  command: "lifecycle",
  operation: "settle-artifact",
  status: "blocked",
  change_id: "example",
  lifecycle_revision: "sha256:abc",
  blockers: [{ code: "RL_UNRESOLVED_MATERIAL_FINDING", relevant_identities: ["F-12"], corrective_operation: "revise specification" }],
  permitted_operations: ["record-artifact-revision"],
  effective_state: { active_milestone: "M2" },
};

test("result formats are a closed vocabulary", () => {
  assert.deepEqual(RESULT_FORMATS, ["human", "json", "concise-human", "concise-json", "detailed-json"]);
  assert.throws(() => renderResult(detailed, { format: "verbose" }), /Unknown result format/);
});

test("concise JSON uses schema 2, closed applicable fields, and compact encoding", () => {
  const projected = projectConciseResult(detailed, { invocationId: "a1b2c3d4e5f60718", exitCode: 2, observability: "recorded" });
  assert.deepEqual(projected, {
    schema_version: 2,
    projection: "concise",
    invocation_id: "a1b2c3d4e5f60718",
    command: "lifecycle",
    operation: "settle-artifact",
    status: "blocked",
    exit_code: 2,
    change_id: "example",
    lifecycle_revision: "sha256:abc",
    next_operation: "revise specification",
    codes: ["RL_UNRESOLVED_MATERIAL_FINDING"],
    finding_ids: ["F-12"],
    milestone_ids: ["M2"],
    observability: "recorded",
  });
  const rendered = renderResult(detailed, { format: "concise-json", invocationId: "a1b2c3d4e5f60718", exitCode: 2 });
  assert.equal(rendered, `${JSON.stringify({ ...projected, observability: "disabled" })}\n`);
});

test("concise human output is actionable and at most two lines", () => {
  const output = renderResult(detailed, { format: "concise-human", invocationId: "a1b2c3d4e5f60718", exitCode: 2, observability: "recorded" });
  assert.ok(output.includes("settle-artifact blocked"));
  assert.ok(output.includes("RL_UNRESOLVED_MATERIAL_FINDING"));
  assert.ok(output.includes("next=revise specification"));
  assert.ok(output.includes("invocation=a1b2c3d4e5f60718"));
  assert.ok(output.trim().split("\n").length <= 2);
});

test("legacy JSON and detailed JSON retain the detailed object", () => {
  assert.equal(renderResult(detailed, { format: "json" }), `${JSON.stringify(detailed, null, 2)}\n`);
  assert.equal(renderResult(detailed, { format: "detailed-json" }), `${JSON.stringify(detailed, null, 2)}\n`);
});
