import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { test } from "node:test";

import { executeLifecycleCli } from "../dist/lib/lifecycle-cli.js";
import { parseLifecycleYaml, serializeLifecycleYaml } from "../dist/lib/lifecycle-contract.js";
import { lifecycleRevision, packageContext, packageRepository, writePackageReview, writeRequest } from "./helpers/lifecycle-package-fixture.js";

async function repository(changeIds = ["example"], overrides = {}) {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-lifecycle-read-"));
  for (const changeId of changeIds) {
    const changeRoot = join(root, "docs", "changes", changeId);
    mkdirSync(changeRoot, { recursive: true });
    mkdirSync(join(root, "specs"), { recursive: true });
    const specPath = join(root, "specs", `${changeId}.md`);
    writeFileSync(specPath, `# ${changeId}\n`, "utf8");
    const change = {
      change_id: changeId,
      title: "Example",
      classification: "feature",
      risk: "standard",
      lifecycle_contract: "stage-owned-change-local-v1",
      artifact_states: {
        spec: { kind: "spec", path: `specs/${changeId}.md`, role: "primary", lifecycle_state: "approved" },
      },
      workflow_state: {
        lifecycle_state: "active",
        current_stage: "implement",
        next_stage: "implement",
        blocker: null,
        planned_work: {
          current_milestone: "M1",
          milestones: { M1: { kind: "implementation", state: "implementing" } },
          remaining_implementation_milestones: ["M1"],
        },
      },
      ...overrides,
    };
    writeFileSync(join(changeRoot, "change.yaml"), `${toYaml(change)}\n`, "utf8");
  }
  return root;
}

function toYaml(value, indent = 0) {
  const prefix = " ".repeat(indent);
  if (Array.isArray(value)) return value.map((item) => `${prefix}- ${typeof item === "object" ? `\n${toYaml(item, indent + 2)}` : item}`).join("\n");
  return Object.entries(value).map(([key, child]) => {
    if (child === null) return `${prefix}${key}: null`;
    if (Array.isArray(child)) return child.length ? `${prefix}${key}:\n${toYaml(child, indent + 2)}` : `${prefix}${key}: []`;
    if (typeof child === "object") return Object.keys(child).length ? `${prefix}${key}:\n${toYaml(child, indent + 2)}` : `${prefix}${key}: {}`;
    return `${prefix}${key}: ${child}`;
  }).join("\n");
}

test("read commands require an unambiguous governed change", async () => {
  const empty = await repository([]);
  assert.equal(executeLifecycleCli(["status", "--format", "json"], { cwd: empty }).result.errors[0].code, "RL_CHANGE_NOT_FOUND");
  const multiple = await repository(["one", "two"]);
  assert.equal(executeLifecycleCli(["status"], { cwd: multiple }).result.errors[0].code, "RL_AMBIGUOUS_CHANGE");
  assert.equal(executeLifecycleCli(["status", "--change", "two"], { cwd: multiple }).result.change_id, "two");
});

test("status exposes one deterministic result model without writes", async () => {
  const root = await repository();
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const before = readFileSync(path, "utf8");
  const execution = executeLifecycleCli(["status", "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 0);
  assert.deepEqual(Object.keys(execution.result).slice(0, 12), [
    "schema_version", "command", "operation", "status", "change_id", "lifecycle_revision", "effective_state", "blockers", "permitted_operations", "artifacts", "warnings", "errors",
  ]);
  assert.equal(execution.result.effective_state.recorded_state.spec, "approved");
  assert.equal(execution.result.effective_state.evidence_state.spec, "current");
  assert.equal(execution.result.effective_state.downstream_package_authority.enforcement, "cutover-pending");
  assert.equal(execution.result.effective_state.downstream_package_authority.packages.design.state, "missing");
  assert.equal(execution.result.effective_state.downstream_package_authority.packages.delivery.state, "missing");
  assert.equal(execution.result.effective_state.downstream_package_authority.packages.design.authority, "withheld");
  assert.deepEqual(execution.result.permitted_operations, ["record-validation", "complete-milestone"]);
  assert.match(execution.human, /Current stage: implement/);
  assert.match(execution.human, /Artifact spec: approved; evidence current/);
  assert.equal(readFileSync(path, "utf8"), before);
});

test("context returns bounded stage facts from the shared interpretation", async () => {
  const root = await repository();
  const result = executeLifecycleCli(["context", "code-review", "--format", "json"], { cwd: root }).result;
  assert.equal(result.context.exact_change, "example");
  assert.equal(result.context.target_artifact, null);
  assert.equal(result.context.permitted_registration_operation, "record-review");
  assert.equal(result.context.downstream_package_authority.enforcement, "cutover-pending");
  assert.equal(result.context.downstream_package_authority.status, "not-current");
  assert.match(result.context.lifecycle_revision, /^sha256:[a-f0-9]{64}$/);
  assert.equal(JSON.stringify(result).includes(root), false);
  const human = executeLifecycleCli(["context", "code-review"], { cwd: root }).human;
  assert.match(human, /Context operation: code-review/);
  assert.match(human, /Permitted registration operation: record-review/);
});

test("downstream authority distinguishes historical-only reviews without activating the cutover blocker", async () => {
  const root = await repository(["example"], {
    artifact_states: {
      architecture: { kind: "architecture", path: "specs/example.md", role: "primary", lifecycle_state: "approved", review: { outcome: "approved" } },
      spec: { kind: "spec", path: "specs/example.md", role: "primary", lifecycle_state: "approved", review: { outcome: "approved" } },
      plan: { kind: "plan", path: "specs/example.md", role: "primary", lifecycle_state: "approved", review: { outcome: "approved" } },
      "test-spec": { kind: "test-spec", path: "specs/example.md", role: "primary", lifecycle_state: "approved", review: { outcome: "approved" } },
    },
  });
  const execution = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  assert.equal(execution.result.effective_state.downstream_package_authority.packages.design.state, "historical-only");
  assert.equal(execution.result.effective_state.downstream_package_authority.packages.delivery.state, "historical-only");
  assert.equal(execution.result.blockers.some((item) => item.blocking_invariant === "downstream-package-authority"), false);
});

test("downstream authority reports a recorded but unsettled package as partial", async () => {
  const { root } = await packageRepository();
  const context = packageContext(root);
  const review = writePackageReview(root, context);
  const request = writeRequest(root, "record-partial-design", {
    schema_version: 1,
    operation: "record-package-review",
    change_id: "example",
    expected_lifecycle_revision: lifecycleRevision(root),
    package_kind: "design",
    review_id: review.reviewId,
    upstream_review_id: review.packageFacts.upstream_review_id,
    members: review.packageFacts.members,
    evidence_path: review.reviewPath,
    stage_authority: "design-review",
  });
  assert.equal(executeLifecycleCli(["record-package-review", "--request", request], { cwd: root }).exitCode, 0);
  const status = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result;
  assert.equal(status.effective_state.downstream_package_authority.packages.design.state, "partial");
  assert.equal(status.effective_state.downstream_package_authority.packages.design.authority, "withheld");
});

test("non-current upstream context requires workflow routing and keeps deferred work out of immediate permissions", async () => {
  const artifactSha = createHash("sha256").update("# example\n").digest("hex");
  const root = await repository(["example"], {
    lifecycle_cli: {
      schema_version: 2,
      artifacts: { spec: { artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", artifact_sha256: artifactSha, stage_authority: "spec" } },
      reviews: {}, validations: {}, resolutions: {}, milestones: {}, correction_history: {}, withdrawals: {},
    },
  });
  writeFileSync(join(root, "docs", "changes", "example", "review-log.md"), "Finding ID: F-1\nOpen findings: F-1\n", "utf8");
  const execution = executeLifecycleCli(["context", "spec", "--change", "example", "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 2, JSON.stringify(execution.result));
  assert.equal(execution.result.errors.at(-1).code, "RL_WORKFLOW_ROUTE_REQUIRED");
  assert.equal(execution.result.context.permitted_registration_operation, null);
  assert.equal(execution.result.context.available_after_workflow_route, "record-artifact-revision");
  assert.deepEqual(execution.result.context.route_required.finding_ids, ["F-1"]);
  assert.equal(execution.result.permitted_operations.includes("record-artifact-revision"), false);
  assert.equal(execution.result.permitted_operations.includes("route-correction"), true);
  const human = executeLifecycleCli(["context", "spec", "--change", "example"], { cwd: root }).human;
  assert.match(human, /RL_WORKFLOW_ROUTE_REQUIRED/);
  assert.match(human, /Available after workflow route: record-artifact-revision/);
  assert.equal(human.includes(root), false);
});

test("structural blockers use the blocked exit class", async () => {
  const root = await repository();
  const logPath = join(root, "docs", "changes", "example", "review-log.md");
  writeFileSync(logPath, "Open findings: F-1\n", "utf8");
  const execution = executeLifecycleCli(["status"], { cwd: root });
  assert.equal(execution.result.status, "blocked");
  assert.equal(execution.exitCode, 2);
  assert.equal(execution.result.blockers[0].code, "RL_UNRESOLVED_MATERIAL_FINDING");
});

test("open findings preserve the owner-stage revision operation and advance the durable review round", async () => {
  const root = await repository(["example"], {
    artifact_states: {
      spec: {
        kind: "spec",
        path: "specs/example.md",
        role: "primary",
        lifecycle_state: "revision-required",
        review: { id: "spec-review-r1", artifact_id: "spec", outcome: "changes-requested", record: "docs/changes/example/reviews/spec-review-r1.md", round: "r1" },
      },
    },
    workflow_state: {
      lifecycle_state: "active",
      current_stage: "spec-review",
      next_stage: "spec",
      blocker: null,
      evidence: [],
    },
    review: { status: "changes-requested", unresolved_items: 1 },
  });
  const changeRoot = join(root, "docs", "changes", "example");
  mkdirSync(join(changeRoot, "reviews"), { recursive: true });
  writeFileSync(join(changeRoot, "review-log.md"), "Open findings: F-1\n", "utf8");
  writeFileSync(join(changeRoot, "reviews", "spec-review-r1.md"), "Review ID: spec-review-r1\nRound: r1\n", "utf8");

  const status = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result;
  assert.deepEqual(status.permitted_operations, ["record-artifact-revision"]);
  const context = executeLifecycleCli(["context", "spec-review", "--change", "example", "--format", "json"], { cwd: root }).result.context;
  assert.equal(context.review_round, "r2");

  const blockedRoot = await repository(["example"], {
    artifact_states: {
      spec: {
        kind: "spec",
        path: "specs/example.md",
        role: "primary",
        lifecycle_state: "revision-required",
        review: { id: "spec-review-r1", artifact_id: "spec", outcome: "changes-requested", record: "docs/changes/example/reviews/spec-review-r1.md", round: "r1" },
      },
    },
    workflow_state: { lifecycle_state: "active", current_stage: "spec-review", next_stage: "spec", blocker: "owner decision required", evidence: [] },
    review: { status: "changes-requested", unresolved_items: 1 },
  });
  writeFileSync(join(blockedRoot, "docs", "changes", "example", "review-log.md"), "Open findings: F-1\n", "utf8");
  const fatallyBlocked = executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: blockedRoot }).result;
  assert.deepEqual(fatallyBlocked.permitted_operations, []);
});

test("validate rejects unsupported contracts and malformed YAML deterministically", async () => {
  const unsupported = await repository(["example"], { lifecycle_contract: "future-v9" });
  const incompatible = executeLifecycleCli(["validate"], { cwd: unsupported });
  assert.equal(incompatible.exitCode, 4);
  assert.equal(incompatible.result.errors[0].code, "RL_UNSUPPORTED_SCHEMA");
  const malformed = await repository();
  writeFileSync(join(malformed, "docs", "changes", "example", "change.yaml"), "change_id: example\nchange_id: duplicate\n", "utf8");
  assert.equal(executeLifecycleCli(["validate", "--change", "example"], { cwd: malformed }).result.errors[0].code, "RL_INVALID_REQUEST");
});

test("stored correction and withdrawal vocabularies fail closed", async () => {
  const artifactSha = createHash("sha256").update("# example\n").digest("hex");
  const root = await repository(["example"], {
    lifecycle_cli: {
      schema_version: 2,
      artifacts: { spec: { artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", artifact_sha256: artifactSha, stage_authority: "spec" } },
      reviews: {}, validations: {}, resolutions: {}, milestones: {}, correction_history: {},
      withdrawals: { bad: { withdrawal_id: "bad", status: "archived", artifact_id: "old", artifact_kind: "plan", artifact_path: "docs/plans/old.md", canonical_owner_change_id: "owner", reason: "cleanup" } },
    },
  });
  const execution = executeLifecycleCli(["validate", "--change", "example", "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 4);
  assert.equal(execution.result.errors.some((error) => /unknown or contradictory receipt/.test(error.summary)), true);
  assert.equal(execution.result.errors.some((error) => /unknown artifact kind or reason/.test(error.summary)), true);
  assert.equal(execution.result.permitted_operations.includes("route-correction"), false);
});

test("upstream context does not advertise a route against stale registered identity", async () => {
  const root = await repository(["example"], {
    lifecycle_cli: {
      schema_version: 2,
      artifacts: { spec: { artifact_kind: "spec", artifact_role: "primary", artifact_path: "specs/example.md", artifact_sha256: "0".repeat(64), stage_authority: "spec" } },
      reviews: {}, validations: {}, resolutions: {}, milestones: {}, correction_history: {}, withdrawals: {},
    },
  });
  const execution = executeLifecycleCli(["context", "spec", "--change", "example", "--format", "json"], { cwd: root });
  assert.equal(execution.result.context.route_required, undefined);
  assert.equal(execution.result.context.available_after_workflow_route, undefined);
  assert.equal(execution.result.permitted_operations.includes("route-correction"), false);
  assert.deepEqual(execution.result.effective_state.stale_evidence, ["spec"]);
});

test("design review context exposes deterministic explicit package identity", async () => {
  const { root } = await packageRepository();
  const execution = packageContext(root);
  assert.equal(execution.exitCode, 0, JSON.stringify(execution.result));
  assert.deepEqual(execution.result.context.review_package.members, { architecture: "docs/architecture/example.md", spec: "specs/example.md", "adr-cache": "docs/adr/ADR-cache.md" });
  assert.equal(execution.result.context.review_package.upstream_review_id, "proposal-review-r1");
  assert.equal(execution.result.context.review_package.status, "review-required");
  assert.equal(execution.result.context.permitted_registration_operation, "record-package-review");
  assert.equal(JSON.stringify(execution.result.context.review_package).includes("artifact_sha256"), false);
});

test("design package exposes changed membership and upstream review directly", async () => {
  const membership = await packageRepository();
  const changePath = join(membership.root, "docs", "changes", "example", "change.yaml");
  const change = parseLifecycleYaml(readFileSync(changePath, "utf8"));
  const extraPath = "docs/adr/ADR-extra.md";
  const extraBytes = "# ADR extra\n";
  writeFileSync(join(membership.root, extraPath), extraBytes, "utf8");
  change.artifact_states["adr-extra"] = { kind: "adr", path: extraPath, role: "supporting", lifecycle_state: "review-required" };
  change.lifecycle_cli.artifacts["adr-extra"] = {
    artifact_kind: "adr", artifact_role: "supporting", artifact_path: extraPath,
    artifact_sha256: createHash("sha256").update(extraBytes).digest("hex"), stage_authority: "architecture",
  };
  writeFileSync(changePath, serializeLifecycleYaml(change), "utf8");
  const membershipContext = packageContext(membership.root).result.context.review_package;
  assert.deepEqual(membershipContext.members, { architecture: "docs/architecture/example.md", spec: "specs/example.md", "adr-cache": "docs/adr/ADR-cache.md", "adr-extra": "docs/adr/ADR-extra.md" });

  const binding = await packageRepository();
  const bindingPath = join(binding.root, "docs", "changes", "example", "change.yaml");
  writeFileSync(bindingPath, readFileSync(bindingPath, "utf8").replaceAll("proposal-review-r1", "proposal-review-r2"), "utf8");
  const bindingContext = packageContext(binding.root).result.context.review_package;
  assert.equal(bindingContext.upstream_review_id, "proposal-review-r2");
});

test("package context fails closed for missing membership and ignores direct member-byte edits", async () => {
  const missing = await packageRepository({ includeArchitecture: false });
  const rejected = packageContext(missing.root);
  assert.equal(rejected.exitCode, 2);
  assert.equal(rejected.result.context.review_package.errors[0].code, "RL_OPERATION_NOT_PERMITTED");
  assert.match(rejected.result.context.review_package.errors[0].summary, /primary architecture/);

  const complete = await packageRepository();
  const before = packageContext(complete.root).result.context.review_package;
  writeFileSync(join(complete.root, complete.sources.spec[0]), "# Specification changed\n", "utf8");
  const after = packageContext(complete.root).result.context.review_package;
  assert.deepEqual(after.members, before.members);
  assert.equal(after.status, before.status);
});

test("stored package review vocabularies reject an unknown outcome before consistency", async () => {
  const { root } = await packageRepository();
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const source = readFileSync(path, "utf8").replace("package_reviews: {}", "package_reviews:\n    design:\n      package_kind: design\n      outcome: accepted\n      stage_authority: design-review\n      reviewer_authority: design-review\n      members: {architecture: docs/architecture/example.md, spec: specs/example.md}\n      upstream_review_id: proposal-review-r1");
  writeFileSync(path, source, "utf8");
  const execution = executeLifecycleCli(["validate", "--change", "example", "--format", "json"], { cwd: root });
  assert.equal(execution.exitCode, 4);
  assert.equal(execution.result.errors.some((error) => /outcome accepted is unknown/.test(error.summary)), true);
});
