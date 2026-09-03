import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync } from "node:fs";
import { join } from "node:path";

import { allowedNextStages } from "./lifecycle-contract.js";
import { reviewPackageContext } from "./lifecycle-packages.js";

function expectedAuthorAuthority(kind) {
  return kind === "adr" ? "architecture" : kind;
}

function expectedReviewAuthority(kind) {
  return kind === "proposal" ? "proposal-review" : null;
}

export function stageIsComplete(root, change, stage) {
  if (["design-review", "delivery-review"].includes(stage)) {
    const packageKind = stage.replace(/-review$/, "");
    const context = reviewPackageContext(root, change, packageKind);
    const projection = change.review_packages?.[packageKind];
    const registered = change.lifecycle_cli?.package_reviews?.[packageKind];
    return context.errors.length === 0
      && context.status === "approved"
      && context.authority === "granted"
      && projection?.review_id === registered?.review_id
      && (stage !== "delivery-review" || Boolean(change.workflow_state?.planned_work));
  }

  if (stage === "code-review" && change.workflow_state?.planned_work?.current_milestone === "none") {
    const planned = change.workflow_state.planned_work;
    const review = change.lifecycle_cli?.reviews?.["final-code-review"];
    const projection = planned.latest_review;
    const evidencePath = review?.evidence_path;
    const safeEvidencePath = typeof evidencePath === "string" && !evidencePath.startsWith("/") && !evidencePath.includes("\\") && !evidencePath.split("/").some((part) => !part || part === "." || part === "..");
    const evidenceExists = safeEvidencePath && existsSync(join(root, evidencePath)) && lstatSync(join(root, evidencePath)).isFile();
    const evidenceCurrent = evidenceExists && createHash("sha256").update(readFileSync(join(root, evidencePath))).digest("hex") === review.evidence_sha256;
    const logPath = review?.review_log_path;
    const safeLogPath = typeof logPath === "string" && !logPath.startsWith("/") && !logPath.includes("\\") && !logPath.split("/").some((part) => !part || part === "." || part === "..");
    const logExists = safeLogPath && existsSync(join(root, logPath)) && lstatSync(join(root, logPath)).isFile();
    const logCurrent = logExists && createHash("sha256").update(readFileSync(join(root, logPath))).digest("hex") === review.review_log_sha256;
    const implementationMilestones = Object.values(planned.milestones ?? {}).filter((milestone) => milestone?.kind === "implementation");
    return implementationMilestones.length > 0 && implementationMilestones.every((milestone) => milestone.state === "closed")
      && Array.isArray(planned.remaining_implementation_milestones) && planned.remaining_implementation_milestones.length === 0
      && review?.stage_authority === "code-review" && review?.outcome === "approved" && /^(?:[a-f0-9]{40}|[a-f0-9]{64})$/.test(review?.reviewed_revision ?? "") && evidenceCurrent && logCurrent
      && projection?.artifact_id === "plan" && projection?.occurrence === "final" && projection?.milestone_id === "none"
      && projection?.stage === "code-review" && projection?.status === "approved" && projection?.round === review.round
      && Array.isArray(projection?.evidence) && projection.evidence.length === 1 && projection.evidence[0] === review.evidence_path;
  }

  const coordination = change.lifecycle_cli;
  const entries = Object.entries(change.artifact_states ?? {}).filter(([, entry]) => entry && (
    stage.endsWith("-review")
      ? expectedReviewAuthority(entry.kind) === stage
      : expectedAuthorAuthority(entry.kind) === stage
  ));
  if (!entries.length) return false;
  if (stage.endsWith("-review")) {
    return entries.every(([artifactId, entry]) => {
      const registeredReview = coordination?.reviews?.[artifactId];
      return ["accepted", "approved", "active"].includes(entry.lifecycle_state)
        && entry.review?.outcome === "approved"
        && (!registeredReview || registeredReview.review_id === entry.review.id);
    });
  }
  return entries.every(([artifactId, entry]) => {
    if (entry.lifecycle_state !== "review-required") return false;
    const registration = coordination?.artifacts?.[artifactId];
    return registration
      ? registration.artifact_path === entry.path && registration.stage_authority === stage
      : Boolean(entry.authoring_evidence);
  });
}

export function stageTransitionDecision(root, change, sourceStage, destinationStage) {
  if (!allowedNextStages(change, sourceStage).includes(destinationStage)) return { allowed: false, invariant: "workflow-stage-edge" };
  if (!stageIsComplete(root, change, sourceStage)) return { allowed: false, invariant: "workflow-stage-completion" };
  return { allowed: true, invariant: null };
}
