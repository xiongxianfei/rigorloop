import { validateCompactPath, validateCompactProjection, validateCompactVocabulary } from "./compact-contract.js";
import { compactOperationEligibility, compactPermittedOperations, compactProgression } from "./compact-eligibility.js";

function rawUtf8Compare(left, right) {
  return Buffer.compare(Buffer.from(left, "utf8"), Buffer.from(right, "utf8"));
}

function sortedMapping(source, selected = null) {
  const allowed = selected === null ? null : new Set(selected);
  return Object.fromEntries(Object.entries(source ?? {})
    .filter(([key]) => allowed === null || allowed.has(key))
    .sort(([left], [right]) => rawUtf8Compare(left, right)));
}

function selectedPaths(paths = []) {
  const unique = [...new Set(paths)];
  unique.forEach((path) => validateCompactPath(path, "required_paths"));
  return unique.sort(rawUtf8Compare);
}

export function projectCompactSnapshot(snapshot, view, selection = {}) {
  validateCompactVocabulary("ProjectionView", view);
  validateCompactVocabulary("Stage", snapshot.current_stage);

  const includeAll = view === "summary";
  const requestedOperation = selection.requestedOperation ?? null;
  if (requestedOperation !== null) validateCompactVocabulary("Operation", requestedOperation);
  const progression = compactProgression(snapshot);
  const projection = {
    view,
    change_id: snapshot.change_id,
    lifecycle_contract: snapshot.lifecycle_contract,
    lifecycle_revision: snapshot.lifecycle_revision,
    current_stage: snapshot.current_stage,
    artifacts: {},
    reviews: {},
    open_findings: {},
    material_decisions: {},
    evidence: {},
    active_work: includeAll || view === "remaining-work" || view === "verification" || view === "skill-context" ? snapshot.active_work ?? null : null,
    progression_status: progression.status,
    blockers: includeAll || view === "evidence" || view === "remaining-work" || view === "verification" || view === "skill-context" ? progression.blockers : [],
    remaining_work: {},
    permitted_operations: includeAll || view === "remaining-work" || view === "verification" || view === "skill-context" ? compactPermittedOperations(snapshot) : [],
    requested_operation: requestedOperation,
    operation_eligibility: requestedOperation === null ? null : compactOperationEligibility(snapshot, requestedOperation, selection.request ?? null),
    required_paths: selectedPaths(selection.requiredPaths ?? []),
  };

  if (includeAll) {
    projection.artifacts = sortedMapping(snapshot.artifacts);
    projection.reviews = sortedMapping(snapshot.reviews);
    projection.open_findings = sortedMapping(snapshot.open_findings);
    projection.material_decisions = sortedMapping(snapshot.material_decisions);
    projection.evidence = sortedMapping(snapshot.evidence);
    projection.remaining_work = sortedMapping(snapshot.remaining_work);
  } else if (view === "reviews") {
    projection.reviews = sortedMapping(snapshot.reviews);
  } else if (view === "open-findings") {
    projection.open_findings = sortedMapping(snapshot.open_findings);
  } else if (view === "material-decisions") {
    projection.material_decisions = sortedMapping(snapshot.material_decisions);
  } else if (view === "evidence") {
    projection.evidence = sortedMapping(snapshot.evidence);
  } else if (view === "remaining-work") {
    projection.remaining_work = sortedMapping(snapshot.remaining_work);
  } else if (view === "verification") {
    projection.artifacts = sortedMapping(snapshot.artifacts);
    projection.reviews = sortedMapping(snapshot.reviews);
    projection.open_findings = sortedMapping(snapshot.open_findings);
    projection.material_decisions = sortedMapping(snapshot.material_decisions);
    projection.evidence = sortedMapping(snapshot.evidence);
    projection.remaining_work = sortedMapping(snapshot.remaining_work);
  } else {
    projection.artifacts = sortedMapping(snapshot.artifacts, selection.artifactIds ?? []);
    projection.reviews = sortedMapping(snapshot.reviews, selection.reviewTargetIds ?? []);
    projection.open_findings = sortedMapping(snapshot.open_findings, selection.findingIds ?? []);
    projection.material_decisions = sortedMapping(snapshot.material_decisions, selection.decisionIds ?? []);
    projection.evidence = sortedMapping(snapshot.evidence, selection.evidenceIds ?? []);
    projection.remaining_work = sortedMapping(snapshot.remaining_work, selection.remainingWorkIds ?? []);
  }

  return validateCompactProjection(projection);
}
