import { COMPACT_VOCABULARIES, validateCompactVocabulary } from "./compact-contract.js";

const REVIEW_STAGES = new Set(["proposal-review", "design-review", "delivery-review", "code-review"]);
const REVIEW_RESPONSIBILITY = Object.freeze({
  proposal: "proposal-review",
  "design-package": "design-review",
  "delivery-package": "delivery-review",
  milestone: "code-review",
  "final-code": "code-review",
});
const ARTIFACT_STAGE = Object.freeze({ proposal: "proposal", architecture: "architecture", adr: "architecture", spec: "spec", plan: "plan" });
const AUTHORING_STAGES = new Set(Object.values(ARTIFACT_STAGE));

function diagnostic(operation, code, summary, invariant, identities = []) {
  return { code, summary, invariant, scope: "operation", operation, identities, next_operation: null };
}

function blockingFindings(snapshot) {
  return Object.values(snapshot.open_findings ?? {}).filter((finding) => finding.blocking_effect === "blocks-progression");
}

function finalReview(snapshot) {
  return Object.values(snapshot.reviews ?? {}).find((review) => review.path.endsWith("/reviews/code-review-final.md"));
}

function approvedReview(snapshot, reviewerAuthority) {
  return Object.values(snapshot.reviews ?? {}).some((review) => review.reviewer_authority === reviewerAuthority && review.status === "current" && review.outcome === "approved");
}

function remainingOwnedBy(snapshot, owner) {
  return Object.values(snapshot.remaining_work ?? {}).some((work) => work.owner === owner);
}

function findingsOwnedBy(snapshot, owner) {
  const findings = Object.values(snapshot.open_findings ?? {});
  return findings.length > 0 && findings.every((finding) => finding.owner === owner);
}

function hasReviewableArtifact(snapshot, kind) {
  return Object.values(snapshot.artifacts ?? {}).some((artifact) => artifact.kind === kind && artifact.status === "review-required");
}

function structuralBlockers(snapshot, operation) {
  const active = snapshot.active_work;
  const currentReview = Object.values(snapshot.reviews ?? {}).find((review) => review.status === "review-required");
  switch (operation) {
    case "record-artifact":
      if (AUTHORING_STAGES.has(snapshot.current_stage)) return [];
      if (Object.values(snapshot.artifacts ?? {}).some((artifact) => ARTIFACT_STAGE[artifact.kind] === snapshot.current_stage)) return [];
      if (active?.kind === "correction" && active.status === "authoring" && active.destination_stage === snapshot.current_stage) return [];
      break;
    case "advance-stage":
      if (!active && blockingFindings(snapshot).length === 0 && (snapshot.blockers ?? []).length === 0) return [];
      if (active?.kind === "milestone" && active.status === "review-required" && snapshot.current_stage === "implement" && blockingFindings(snapshot).length === 0 && (snapshot.blockers ?? []).length === 0) return [];
      if (!snapshot.blockers?.length && REVIEW_STAGES.has(snapshot.current_stage) && Object.keys(snapshot.open_findings ?? {}).length > 0 && active?.kind !== "correction") return [];
      if (!snapshot.blockers?.length && snapshot.current_stage === "review-resolution" && Object.keys(snapshot.open_findings ?? {}).length > 0 && active?.kind !== "correction") return [];
      break;
    case "replace-review":
      if (REVIEW_STAGES.has(snapshot.current_stage) || currentReview) return [];
      break;
    case "settle-review":
      if (Object.keys(snapshot.reviews ?? {}).length > 0 && (REVIEW_STAGES.has(snapshot.current_stage) || active?.kind === "correction" && active.status === "review-required")) return [];
      break;
    case "resolve-finding":
      if (Object.keys(snapshot.open_findings ?? {}).length > 0 && (snapshot.current_stage === "review-resolution" || active?.kind === "correction" && active.status === "review-required")) return [];
      break;
    case "upsert-decision":
      if (snapshot.current_stage === "review-resolution" || Object.keys(snapshot.material_decisions ?? {}).length > 0) return [];
      break;
    case "remove-decision":
      if (snapshot.current_stage === "review-resolution" && Object.keys(snapshot.material_decisions ?? {}).length > 0) return [];
      break;
    case "route-correction":
      if (!active && (REVIEW_STAGES.has(snapshot.current_stage) || snapshot.current_stage === "verify") && Object.keys(snapshot.open_findings ?? {}).length > 0) return [];
      break;
    case "return-correction":
      if (active?.kind === "correction" && active.status === "authoring") return [];
      break;
    case "advance-milestone":
      if (active?.kind === "milestone") return [];
      if (!active && snapshot.current_stage === "implement" && Object.values(snapshot.remaining_work ?? {}).some((work) => work.kind === "milestone" && work.owner === "implement" && work.status === "pending")) return [];
      break;
    case "update-evidence":
      if (active?.kind === "correction" ? active.owner === snapshot.current_stage : ["implement", "ci-maintenance", "verify"].includes(snapshot.current_stage)) return [];
      break;
    case "invalidate-evidence":
      if (Object.keys(snapshot.evidence ?? {}).length > 0) return [];
      break;
    case "record-verify":
      if (snapshot.current_stage === "verify" && !active && blockingFindings(snapshot).length === 0 && (snapshot.blockers ?? []).length === 0 && Object.keys(snapshot.remaining_work ?? {}).length === 0) {
        const review = finalReview(snapshot);
        if (review?.status === "current" && review.outcome === "approved" && review.reviewer_authority === "code-review") return [];
      }
      break;
    case "recover":
      break;
  }
  return [diagnostic(operation, "RL_OPERATION_NOT_PERMITTED", `${operation} is not structurally eligible in the current state`, "operation-eligibility")];
}

function exactBlockers(snapshot, operation, request) {
  if (!request) return [];
  const payload = request.payload ?? {};
  const active = snapshot.active_work;
  const fail = (summary, invariant = "operation-target", identities = []) => diagnostic(operation, "RL_OPERATION_NOT_PERMITTED", summary, invariant, identities);
  switch (operation) {
    case "record-artifact": {
      const expectedStage = ARTIFACT_STAGE[payload.artifact?.kind];
      if (expectedStage !== snapshot.current_stage && !(active?.kind === "correction" && active.status === "authoring" && active.destination_stage === expectedStage)) return [fail("artifact responsibility does not match the current authoring stage", "responsibility-metadata")];
      if (payload.artifact?.owner !== expectedStage) return [fail("artifact owner is inconsistent responsibility metadata", "responsibility-metadata")];
      if (payload.artifact?.status !== "review-required") return [fail("an authored artifact must enter review-required", "artifact-state")];
      return [];
    }
    case "advance-stage": {
      if (payload.from_stage !== snapshot.current_stage) return [fail("from_stage does not match current_stage")];
      const additional = new Set(["code-review>implement", "code-review>ci-maintenance", "code-review>verify", "review-resolution>implement", "review-resolution>verify"]);
      const main = { proposal: "proposal-review", "proposal-review": "architecture", architecture: "spec", spec: "design-review", "design-review": "plan", plan: "delivery-review", "delivery-review": "implement", implement: "code-review", "code-review": "review-resolution", "review-resolution": "ci-maintenance", "ci-maintenance": "verify", verify: "pr" };
      if (main[payload.from_stage] !== payload.to_stage && !additional.has(`${payload.from_stage}>${payload.to_stage}`)) return [fail("stage transition is not an approved edge", "stage-edge")];
      if (payload.to_stage === "review-resolution") return Object.keys(snapshot.open_findings ?? {}).length > 0 ? [] : [fail("review-resolution requires a current finding", "finding-closeout")];
      const edge = `${payload.from_stage}>${payload.to_stage}`;
      if (edge === "proposal>proposal-review" && !hasReviewableArtifact(snapshot, "proposal")) return [fail("Proposal is not ready for Proposal Review", "artifact-state")];
      if (edge === "architecture>spec" && !hasReviewableArtifact(snapshot, "architecture")) return [fail("Architecture is not current for specification authoring", "artifact-state")];
      if (edge === "spec>design-review" && !hasReviewableArtifact(snapshot, "spec")) return [fail("Specification is not ready for Design Review", "artifact-state")];
      if (edge === "plan>delivery-review" && !hasReviewableArtifact(snapshot, "plan")) return [fail("Plan is not ready for Delivery Review", "artifact-state")];
      if (edge === "proposal-review>architecture" && !approvedReview(snapshot, "proposal-review")) return [fail("Proposal Review is not currently approved", "review-readiness")];
      if (edge === "design-review>plan" && !approvedReview(snapshot, "design-review")) return [fail("Design Review is not currently approved", "review-readiness")];
      if (edge === "delivery-review>implement" && !approvedReview(snapshot, "delivery-review")) return [fail("Delivery Review is not currently approved", "review-readiness")];
      if (edge === "implement>code-review" && !(active?.kind === "milestone" && active.status === "review-required")) return [fail("Implementation handoff requires its active milestone to be review-required", "milestone-state")];
      if (edge === "code-review>implement" || edge === "review-resolution>implement") {
        if (!(active?.kind === "milestone" && active.status === "review-required" && findingsOwnedBy(snapshot, "implement"))) return [fail("Implementation correction requires one active review milestone and implementation-owned findings", "correction-route")];
        return [];
      }
      if ((edge === "code-review>ci-maintenance" || edge === "review-resolution>ci-maintenance") && (active || !remainingOwnedBy(snapshot, "ci-maintenance"))) return [fail("CI maintenance is not selected by current remaining work", "remaining-work")];
      if ((edge === "code-review>verify" || edge === "review-resolution>verify") && (active || Object.keys(snapshot.remaining_work ?? {}).length || Object.keys(snapshot.open_findings ?? {}).length)) return [fail("Verify is not selected while active or remaining work exists", "remaining-work")];
      if (edge === "ci-maintenance>verify" && (active || remainingOwnedBy(snapshot, "ci-maintenance"))) return [fail("CI maintenance work is not complete", "remaining-work")];
      if (edge === "verify>pr" && snapshot.readiness !== "verified") return [fail("PR handoff requires current successful Verify readiness", "verify-readiness")];
      if (blockingFindings(snapshot).length || (snapshot.blockers ?? []).length) return [fail("downstream stage progression is blocked", "progression-readiness")];
      return [];
    }
    case "replace-review": {
      const prior = snapshot.reviews?.[payload.target_id];
      if ((prior?.identity ?? null) !== payload.prior_review_identity) return [fail("prior review identity is stale", "review-identity")];
      if (prior && prior.status !== "review-required" && prior.reviewer_authority !== snapshot.current_stage) return [fail("review target is not due at the current review stage", "review-target")];
      return [];
    }
    case "settle-review": {
      const review = snapshot.reviews?.[payload.target_id];
      if (!review || review.review_id !== payload.review_id || review.outcome !== payload.outcome) return [fail("review settlement does not match the current judgment", "review-identity")];
      if (review.reviewer_authority !== snapshot.current_stage && !(active?.kind === "correction" && active.status === "review-required" && active.return_stage === snapshot.current_stage)) return [fail("review settlement is not owned by the current review stage", "review-target")];
      if (payload.outcome === "approved" && blockingFindings(snapshot).some((finding) => finding.review_target_id === payload.target_id)) return [fail("an approving settlement cannot hide an open blocking finding", "finding-non-loss")];
      if (active?.kind === "correction" && active.status === "review-required" && active.expected_review_target !== payload.target_id) return [fail("settlement is not for the active correction review target", "correction-target")];
      return [];
    }
    case "resolve-finding":
      return snapshot.open_findings?.[payload.resolution?.finding_id] ? [] : [fail("finding is not currently open", "finding-identity")];
    case "route-correction": {
      const correction = payload.correction;
      if (correction?.source_stage !== snapshot.current_stage) return [fail("correction source_stage does not match current_stage", "correction-route")];
      if (correction?.owner !== correction?.destination_stage) return [fail("correction owner and destination responsibility differ", "responsibility-metadata")];
      if (correction?.return_stage === correction?.destination_stage) return [fail("an explicit correction must return to a distinct review stage", "correction-route")];
      if (correction?.return_stage !== correction?.source_stage) return [fail("correction return_stage must match its source review stage", "correction-route")];
      if (correction?.finding_ids?.some((id) => !snapshot.open_findings?.[id])) return [fail("correction contains a finding that is not currently open", "finding-identity")];
      if (correction?.finding_ids?.some((id) => snapshot.open_findings[id].owner !== correction.owner)) return [fail("correction findings do not have one coherent owner", "correction-route")];
      if (correction?.finding_ids?.some((id) => snapshot.open_findings[id].review_target_id !== correction.expected_review_target)) return [fail("correction findings do not belong to the expected review target", "correction-target")];
      return [];
    }
    case "return-correction":
      if (snapshot.current_stage !== active?.destination_stage || active?.owner !== active?.destination_stage || payload.return_stage !== active?.return_stage || payload.satisfied_condition !== active?.return_condition || JSON.stringify(payload.finding_ids) !== JSON.stringify(active?.finding_ids)) return [fail("return does not match the exact active correction", "correction-return")];
      return [];
    case "advance-milestone":
      if (!active) {
        const pending = snapshot.remaining_work?.[payload.milestone_id];
        if (snapshot.current_stage !== "implement" || payload.from_status !== null || payload.to_status !== "planned") return [fail("milestone selection requires implement with null to planned", "milestone-edge")];
        if (!pending || pending.work_id !== payload.milestone_id || pending.kind !== "milestone" || pending.owner !== "implement" || pending.status !== "pending") return [fail("milestone selection requires one exact pending implementation milestone", "milestone-selection", [payload.milestone_id])];
        return [];
      }
      if (payload.milestone_id !== active.milestone_id || payload.from_status !== active.status) return [fail("milestone transition does not match active work", "milestone-identity")];
      if (!new Set(["planned>implementing", "implementing>review-required", "review-required>closed"]).has(`${payload.from_status}>${payload.to_status}`)) return [fail("milestone transition is not an approved adjacent edge", "milestone-edge")];
      if (payload.to_status === "closed") {
        const review = snapshot.reviews?.[payload.milestone_id];
        if (!review || review.status !== "current" || review.outcome !== "approved" || review.reviewer_authority !== "code-review") return [fail("milestone closure requires its exact current approving Code Review", "milestone-review")];
        if (Object.values(snapshot.evidence ?? {}).some((entry) => entry.freshness !== "current")) return [fail("milestone closure requires current evidence", "evidence-freshness")];
      }
      return [];
    case "update-evidence":
      return payload.evidence_ids?.length ? [] : [fail("evidence operation requires an exact evidence selection", "evidence-identity")];
    case "invalidate-evidence":
      if (!payload.evidence_ids?.length || payload.evidence_ids.some((id) => snapshot.evidence?.[id]?.freshness !== "current")) return [fail("evidence invalidation requires an exact current or directly drifted evidence selection", "evidence-identity")];
      return [];
    case "record-verify":
      if (!payload.evidence_ids?.every((id) => snapshot.evidence?.[id]?.freshness === "current")) return [fail("Verify requires exact current evidence", "evidence-freshness")];
      if (Object.keys(snapshot.remaining_work ?? {}).length) return [fail("Verify requires no remaining work", "remaining-work")];
      return [];
    default:
      return [];
  }
}

export function compactOperationEligibility(snapshot, operation, request = null) {
  validateCompactVocabulary("Operation", operation);
  const blockers = [...structuralBlockers(snapshot, operation), ...exactBlockers(snapshot, operation, request)];
  return { operation, status: blockers.length ? "prohibited" : "permitted", blockers };
}

export function compactPermittedOperations(snapshot) {
  return COMPACT_VOCABULARIES.Operation.filter((operation) => compactOperationEligibility(snapshot, operation).status === "permitted");
}

export function compactProgression(snapshot) {
  const blockers = [...(snapshot.blockers ?? [])];
  for (const finding of blockingFindings(snapshot)) blockers.push({ code: "RL_UNRESOLVED_MATERIAL_FINDING", summary: `Open finding ${finding.finding_id} blocks progression`, invariant: "finding-closeout", scope: "progression", operation: null, identities: [finding.finding_id], next_operation: "route-correction" });
  if (snapshot.active_work?.kind === "correction") blockers.push({ code: "RL_CORRECTION_ACTIVE", summary: "An explicit correction is still active", invariant: "correction-closeout", scope: "progression", operation: null, identities: [...snapshot.active_work.finding_ids], next_operation: snapshot.active_work.status === "authoring" ? "return-correction" : "settle-review" });
  return { status: blockers.length ? "blocked" : "ready", blockers };
}
