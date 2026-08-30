import { allowedNextStages } from "./lifecycle-contract.js";
import { reviewPackageContext } from "./lifecycle-packages.js";

function expectedAuthorAuthority(kind) {
  return kind === "adr" ? "architecture" : kind;
}

function expectedReviewAuthority(kind) {
  return kind === "adr" ? "architecture-review" : `${kind}-review`;
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
      && projection?.review_id === registered?.review_id;
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
