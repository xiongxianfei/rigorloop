import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { parseLifecycleYaml, serializeLifecycleYaml } from "../../dist/lib/lifecycle-contract.js";
import { executeLifecycleCli } from "../../dist/lib/lifecycle-cli.js";

function digest(value) {
  return createHash("sha256").update(value).digest("hex");
}

export function writeActiveV3Manifests(root) {
  mkdirSync(join(root, "specs"), { recursive: true });
  writeFileSync(join(root, "specs", "lifecycle-contract-activation.yaml"), `schema_version: 1\nstate: active\nactivating_source_revision: ${"a".repeat(40)}\nchanges: []\n`, "utf8");
  writeFileSync(join(root, "specs", "final-verification-contract-activation.yaml"), `schema_version: 1\nstate: active\nactivating_source_revision: ${"b".repeat(40)}\nchanges: []\n`, "utf8");
}

export async function packageRepository({ stage = "design-review", includeArchitecture = true, includeAdr = true, lifecycleContract = "stage-owned-change-local-v3" } = {}) {
  const root = await mkdtemp(join(tmpdir(), "rigorloop-package-"));
  const changeId = "example";
  const changeRoot = join(root, "docs", "changes", changeId);
  mkdirSync(join(changeRoot, "reviews"), { recursive: true });
  mkdirSync(join(changeRoot, "evidence"), { recursive: true });
  mkdirSync(join(root, "docs", "architecture"), { recursive: true });
  mkdirSync(join(root, "docs", "adr"), { recursive: true });
  mkdirSync(join(root, "docs", "plans"), { recursive: true });
  mkdirSync(join(root, "docs", "proposals"), { recursive: true });
  mkdirSync(join(root, "specs"), { recursive: true });
  mkdirSync(join(root, "requests"), { recursive: true });

  const sources = {
    proposal: ["docs/proposals/example.md", "# Proposal\n\n## Feasibility\n\nFeasible.\n"],
    architecture: ["docs/architecture/example.md", "# Architecture\n"],
    "adr-cache": ["docs/adr/ADR-cache.md", "# ADR cache\n"],
    spec: ["specs/example.md", "# Specification\n"],
    plan: ["docs/plans/example.md", "# Plan\n\n## Milestones\n\n### M1. Implement\n\n- Milestone kind: implementation\n\n### M2. Close lifecycle\n\n- Milestone kind: lifecycle-closeout\n"],
    "test-spec": ["specs/example.test.md", "# Test specification\n"],
  };
  for (const [path, bytes] of Object.values(sources)) writeFileSync(join(root, path), bytes, "utf8");
  if (lifecycleContract === "stage-owned-change-local-v3") {
    writeActiveV3Manifests(root);
  } else if (lifecycleContract === "stage-owned-change-local-v2") {
    writeFileSync(join(root, "specs", "lifecycle-contract-activation.yaml"), `schema_version: 1\nstate: active\nactivating_source_revision: ${"a".repeat(40)}\nchanges: []\n`, "utf8");
  }

  const artifactStates = {
    proposal: { kind: "proposal", path: sources.proposal[0], role: "primary", lifecycle_state: "accepted", review: { id: "proposal-review-r1", artifact_id: "proposal", outcome: "approved", record: "docs/changes/example/reviews/proposal-review-r1.md", round: "r1" } },
    spec: { kind: "spec", path: sources.spec[0], role: "primary", lifecycle_state: "review-required" },
    plan: { kind: "plan", path: sources.plan[0], role: "primary", lifecycle_state: "review-required" },
  };
  if (lifecycleContract === "stage-owned-change-local-v1") artifactStates["test-spec"] = { kind: "test-spec", path: sources["test-spec"][0], role: "primary", lifecycle_state: "review-required" };
  if (includeArchitecture) artifactStates.architecture = { kind: "architecture", path: sources.architecture[0], role: "primary", lifecycle_state: "review-required" };
  if (includeAdr) artifactStates["adr-cache"] = { kind: "adr", path: sources["adr-cache"][0], role: "supporting", lifecycle_state: "review-required" };

  const registrations = Object.fromEntries(Object.entries(artifactStates).map(([artifactId, entry]) => [artifactId, {
    artifact_kind: entry.kind,
    artifact_role: entry.role,
    artifact_path: entry.path,
    artifact_sha256: digest(sources[artifactId][1]),
    stage_authority: entry.kind === "adr" ? "architecture" : entry.kind,
  }]));
  const change = {
    change_id: changeId,
    title: "Package fixture",
    classification: "workflow",
    risk: "high",
    lifecycle_contract: lifecycleContract,
    artifact_states: artifactStates,
    workflow_state: { lifecycle_state: "active", current_stage: stage, next_stage: stage, blocker: null, evidence: [] },
    workflow: {},
    artifacts: {},
    requirements: [],
    tests: [],
    validation: [],
    changed_files: [],
    review: { status: "not-reviewed", unresolved_items: 0 },
    lifecycle_cli: { schema_version: 2, artifacts: registrations, reviews: {}, package_reviews: {}, validations: {}, resolutions: {}, milestones: {}, correction_history: {}, withdrawals: {} },
  };
  writeFileSync(join(changeRoot, "change.yaml"), serializeLifecycleYaml(change), "utf8");
  writeFileSync(join(changeRoot, "review-log.md"), "# Review log\n", "utf8");
  return { root, changeRoot, changeId, sources };
}

export function packageContext(root, stage = "design-review") {
  return executeLifecycleCli(["context", stage, "--change", "example", "--format", "json"], { cwd: root });
}

export function lifecycleRevision(root) {
  return executeLifecycleCli(["status", "--change", "example", "--format", "json"], { cwd: root }).result.lifecycle_revision;
}

export function writeRequest(root, name, body) {
  const path = `requests/${name}.json`;
  writeFileSync(join(root, path), `${JSON.stringify(body, null, 2)}\n`, "utf8");
  return path;
}

export function writePackageReview(root, context, { kind = "design", outcome = "approved", findings = [], correctionTargets = [], round = "r1" } = {}) {
  const stage = `${kind}-review`;
  const reviewId = `${stage}-${round}`;
  const reviewPath = `docs/changes/example/reviews/${reviewId}.md`;
  const packageFacts = context.result.context.review_package;
  const findingText = findings.map((finding) => `\n### Finding ${finding.id}\n\nFinding ID: ${finding.id}\nFinding scope: ${finding.scope}\nAffected artifact IDs: ${finding.affected.join(", ")}\nOwning stages: ${finding.owners.join(", ")}\nEvidence: direct fixture evidence\nRequired outcome: correct the package\nSafe resolution path: route to the named owner\n`).join("");
  writeFileSync(join(root, reviewPath), `# ${stage}\n\nReview ID: ${reviewId}\nStage: ${stage}\nRound: ${round}\nReviewer authority: ${stage}\nPackage kind: ${kind}\nPackage members: ${Object.entries(packageFacts.members).map(([id, path]) => `${id}=${path}`).join(", ")}\nUpstream review ID: ${packageFacts.upstream_review_id}\nStatus: ${outcome}\nMaterial findings: ${findings.length ? findings.map((item) => item.id).join(", ") : "none"}\nCorrection targets: ${correctionTargets.length ? correctionTargets.join(", ") : "none"}\nRecording status: recorded\n${findingText}`, "utf8");
  const logPath = join(root, "docs", "changes", "example", "review-log.md");
  const priorLog = readFileSync(logPath, "utf8").trimEnd();
  writeFileSync(logPath, `${priorLog}\n\n### Review entry\n\nReview ID: ${reviewId}\nStage: ${stage}\nRound: ${round}\nStatus: ${outcome}\nDetailed record: reviews/${reviewId}.md\nResolution: ${findings.length ? "review-resolution.md" : "not-required"}\nMaterial findings: ${findings.length ? findings.map((item) => item.id).join(", ") : "none"}\n${findings.map((item) => `Finding ID: ${item.id}\n`).join("")}Open findings: ${findings.length ? findings.map((item) => item.id).join(", ") : "none"}\nRecording status: recorded\n`, "utf8");
  return { reviewId, reviewPath, packageFacts };
}

export function changeBytes(root) {
  return readFileSync(join(root, "docs", "changes", "example", "change.yaml"), "utf8");
}

export function setWorkflowStage(root, stage) {
  const path = join(root, "docs", "changes", "example", "change.yaml");
  const change = parseLifecycleYaml(readFileSync(path, "utf8"));
  change.workflow_state.current_stage = stage;
  change.workflow_state.next_stage = stage;
  writeFileSync(path, serializeLifecycleYaml(change), "utf8");
}
