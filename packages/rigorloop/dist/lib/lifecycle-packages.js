import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync } from "node:fs";
import { relative, resolve, sep } from "node:path";

import { canonicalJson } from "./lifecycle-contract.js";

export const REVIEW_PACKAGE_KINDS = Object.freeze(["design", "delivery"]);
export const REVIEW_PACKAGE_OUTCOMES = Object.freeze(["approved", "changes-requested", "blocked", "inconclusive"]);
export const REVIEW_PACKAGE_FINDING_SCOPES = Object.freeze(["artifact-local", "cross-artifact", "upstream-direction"]);
export const REVIEW_PACKAGE_STATES = Object.freeze(["approved", "changes-requested", "blocked", "inconclusive"]);

const ID = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;

function diagnostic(code, summary, invariant, identities = []) {
  return { code, summary, blocking_invariant: invariant, relevant_identities: identities, corrective_operation: null };
}

function packageError(code, message, invariant, identities = []) {
  const error = new Error(`${code}: ${message}`);
  error.code = code;
  error.diagnostic = diagnostic(code, message, invariant, identities);
  return error;
}

function repositoryFile(root, candidate) {
  if (typeof candidate !== "string" || !candidate || candidate.includes("\\") || candidate.split("/").some((part) => !part || part === "." || part === "..")) return null;
  const absolute = resolve(root, candidate);
  const rel = relative(root, absolute);
  if (rel === ".." || rel.startsWith(`..${sep}`) || rel.startsWith(sep)) return null;
  let cursor = root;
  for (const part of candidate.split("/")) {
    cursor = resolve(cursor, part);
    if (existsSync(cursor) && lstatSync(cursor).isSymbolicLink()) return null;
  }
  return existsSync(absolute) && lstatSync(absolute).isFile() ? absolute : null;
}

function hash(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function list(value) {
  if (value === null || value === undefined || /^none$/i.test(String(value).trim())) return [];
  return String(value).split(",").map((item) => item.trim().replace(/^`|`$/g, "")).filter(Boolean);
}

function metadata(text, label) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = new RegExp(`^${escaped}:\\s*(.+?)\\s*$`, "m").exec(text);
  return match?.[1]?.trim() ?? null;
}

function currentMembers(change, kind) {
  const entries = Object.entries(change.artifact_states ?? {});
  const primary = (artifactKind) => entries.filter(([, entry]) => entry?.kind === artifactKind && entry?.role === "primary");
  if (kind === "design") {
    const architectures = primary("architecture");
    const specs = primary("spec");
    if (architectures.length !== 1) return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Design package requires exactly one primary architecture artifact.", "review-package-membership", architectures.map(([id]) => id)) };
    if (specs.length !== 1) return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Design package requires exactly one primary specification artifact.", "review-package-membership", specs.map(([id]) => id)) };
    const adrs = entries.filter(([, entry]) => entry?.kind === "adr").sort(([left], [right]) => left.localeCompare(right));
    if (adrs.some(([, entry]) => entry?.role !== "supporting")) return { error: diagnostic("RL_INVALID_REQUEST", "Design package ADR members must use the supporting role.", "review-package-member-role", adrs.map(([id]) => id)) };
    return { entries: [architectures[0], specs[0], ...adrs] };
  }
  if (kind === "delivery") {
    const plans = primary("plan");
    const tests = primary("test-spec");
    if (plans.length !== 1) return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Delivery package requires exactly one primary plan artifact.", "review-package-membership", plans.map(([id]) => id)) };
    if (tests.length !== 1) return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Delivery package requires exactly one primary test specification artifact.", "review-package-membership", tests.map(([id]) => id)) };
    return { entries: [plans[0], tests[0]] };
  }
  return { error: diagnostic("RL_INVALID_REQUEST", `Unknown review package kind ${String(kind)}.`, "review-package-kind", [String(kind)]) };
}

function upstreamBinding(root, change, kind) {
  if (kind === "design") {
    const proposal = Object.entries(change.artifact_states ?? {}).filter(([, entry]) => entry?.kind === "proposal" && entry?.role === "primary");
    if (proposal.length !== 1 || proposal[0][1]?.lifecycle_state !== "accepted" || proposal[0][1]?.review?.outcome !== "approved" || !ID.test(proposal[0][1]?.review?.id ?? "")) {
      return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Design package requires one exact accepted Proposal Review binding.", "review-package-upstream", proposal.map(([id]) => id)) };
    }
    return { value: proposal[0][1].review.id };
  }
  const design = reviewPackageContext(root, change, "design");
  const projection = change.review_packages?.design;
  if (design.errors.length || design.stale || projection?.state !== "approved" || projection?.authority !== "granted" || projection?.aggregate_revision !== design.aggregate_revision) {
    return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Delivery package requires one current approved design package revision.", "review-package-upstream", [String(projection?.aggregate_revision ?? "none")]) };
  }
  return { value: projection.aggregate_revision };
}

export function reviewPackageContext(root, change, kind) {
  if (!REVIEW_PACKAGE_KINDS.includes(kind)) {
    return { package_kind: kind, member_artifact_ids: [], upstream_binding: null, aggregate_revision: null, state: "invalid", authority: "withheld", stale: false, latest_review: null, correction_targets: [], blockers: [], errors: [diagnostic("RL_INVALID_REQUEST", `Unknown review package kind ${String(kind)}.`, "review-package-kind", [String(kind)])], next_permitted_operation: null };
  }
  const membership = currentMembers(change, kind);
  const upstream = upstreamBinding(root, change, kind);
  const errors = [membership.error, upstream.error].filter(Boolean);
  const members = [];
  if (!membership.error) {
    for (const [artifactId, entry] of membership.entries) {
      const registration = change.lifecycle_cli?.artifacts?.[artifactId];
      const absolute = repositoryFile(root, entry?.path);
      if (!absolute || registration?.artifact_path !== entry?.path || registration?.artifact_kind !== entry?.kind || registration?.artifact_role !== entry?.role) {
        errors.push(diagnostic("RL_INVALID_REQUEST", `Package member ${artifactId} is missing a safe exact artifact registration.`, "review-package-member-registration", [artifactId, String(entry?.path)]));
        continue;
      }
      members.push({ artifact_id: artifactId, path: entry.path, sha256: hash(readFileSync(absolute)) });
    }
  }
  const aggregateRevision = errors.length ? null : `sha256:${hash(Buffer.from(canonicalJson({ algorithm: "review-package-sha256-v1", package_kind: kind, members, upstream_binding: upstream.value }), "utf8"))}`;
  const memberIds = members.map((member) => member.artifact_id);
  const projection = change.review_packages?.[kind] ?? null;
  const latest = change.lifecycle_cli?.package_reviews?.[kind] ?? null;
  const stale = Boolean(projection && aggregateRevision && (
    projection.aggregate_revision !== aggregateRevision
    || canonicalJson(projection.member_artifact_ids ?? []) !== canonicalJson(memberIds)
    || projection.upstream_binding !== upstream.value
  ));
  const state = errors.length ? "incomplete" : stale ? "stale" : projection?.state ?? (latest?.aggregate_revision === aggregateRevision ? "review-recorded" : "review-required");
  const authority = !stale && projection?.state === "approved" && projection?.authority === "granted" ? "granted" : "withheld";
  const nextOperation = errors.length ? null : stale || latest?.aggregate_revision !== aggregateRevision ? "record-package-review" : projection?.aggregate_revision !== aggregateRevision ? "settle-review-package" : projection ? null : "settle-review-package";
  return {
    package_kind: kind,
    member_artifact_ids: memberIds,
    upstream_binding: upstream.value ?? null,
    aggregate_revision: aggregateRevision,
    state,
    authority,
    stale,
    latest_review: latest ? { review_id: latest.review_id, round: latest.round, outcome: latest.outcome, evidence_path: latest.evidence_path } : null,
    correction_targets: projection?.correction_targets ?? latest?.correction_targets ?? [],
    blockers: stale ? [diagnostic("RL_STALE_EVIDENCE", `${kind} package authority is stale.`, "review-package-freshness", [`review-package:${kind}`])] : [],
    errors,
    next_permitted_operation: nextOperation,
  };
}

function logEntry(root, changeId, reviewId) {
  const path = `docs/changes/${changeId}/review-log.md`;
  const absolute = repositoryFile(root, path);
  if (!absolute) throw packageError("RL_INVALID_REQUEST", "Package review requires a canonical review log.", "review-log-consistency", [reviewId]);
  const text = readFileSync(absolute, "utf8");
  const marker = `Review ID: ${reviewId}`;
  const indexes = [...text.matchAll(new RegExp(`^Review ID: ${reviewId.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`, "gm"))];
  if (indexes.length !== 1) throw packageError("RL_INVALID_REQUEST", "Review log must contain exactly one package review occurrence.", "review-log-consistency", [reviewId]);
  const start = indexes[0].index;
  const end = text.indexOf("\n### Review entry", start + marker.length);
  return { path, text, sha256: hash(readFileSync(absolute)), entry: text.slice(start, end < 0 ? undefined : end) };
}

function parseFindings(text, declared, context) {
  const blocks = text.split(/(?=^### Finding\s+)/m).slice(1);
  const findings = blocks.map((block) => ({
    finding_id: metadata(block, "Finding ID"),
    scope: metadata(block, "Finding scope"),
    affected_artifact_ids: list(metadata(block, "Affected artifact IDs")),
    owning_stages: list(metadata(block, "Owning stages")),
    evidence: metadata(block, "Evidence"),
    required_outcome: metadata(block, "Required outcome"),
    safe_resolution_path: metadata(block, "Safe resolution path"),
  }));
  if (canonicalJson(findings.map((finding) => finding.finding_id).sort()) !== canonicalJson([...declared].sort())) throw packageError("RL_INVALID_REQUEST", "Package review finding blocks do not match Material findings.", "review-package-findings", declared);
  for (const finding of findings) {
    if (!ID.test(finding.finding_id ?? "")) throw packageError("RL_INVALID_REQUEST", "Package review finding has an invalid Finding ID.", "review-package-findings", [String(finding.finding_id)]);
    if (!REVIEW_PACKAGE_FINDING_SCOPES.includes(finding.scope)) throw packageError("RL_INVALID_REQUEST", `Package review finding scope ${String(finding.scope)} is unknown.`, "review-package-finding-scope", [finding.finding_id, String(finding.scope)]);
    if (!finding.evidence || !finding.required_outcome || !finding.safe_resolution_path || !finding.owning_stages.length) throw packageError("RL_INVALID_REQUEST", "Package review finding is missing required evidence, outcome, resolution, or ownership.", "review-package-findings", [finding.finding_id]);
    const affected = finding.affected_artifact_ids;
    if (finding.scope === "artifact-local" && (affected.length !== 1 || !context.member_artifact_ids.includes(affected[0]))) throw packageError("RL_INVALID_REQUEST", "Artifact-local finding must identify exactly one package member.", "review-package-finding-attribution", [finding.finding_id, ...affected]);
    if (finding.scope === "cross-artifact" && (affected.length < 2 || affected.some((id) => !context.member_artifact_ids.includes(id)))) throw packageError("RL_INVALID_REQUEST", "Cross-artifact finding must identify at least two package members.", "review-package-finding-attribution", [finding.finding_id, ...affected]);
    const upstreamIds = context.package_kind === "design" ? ["proposal"] : ["design"];
    if (finding.scope === "upstream-direction" && (affected.length !== 1 || !upstreamIds.includes(affected[0]))) throw packageError("RL_INVALID_REQUEST", "Upstream-direction finding must identify the owning upstream artifact or package.", "review-package-finding-attribution", [finding.finding_id, ...affected]);
  }
  return findings;
}

export function readPackageReview(root, change, request, context) {
  const absolute = repositoryFile(root, request.evidence_path);
  if (!absolute) throw packageError("RL_INVALID_REQUEST", "Package review evidence must be one safe regular file.", "review-package-evidence", [String(request.evidence_path)]);
  const text = readFileSync(absolute, "utf8");
  const reviewId = metadata(text, "Review ID");
  const round = metadata(text, "Round");
  const stage = metadata(text, "Stage");
  const outcome = metadata(text, "Status");
  const reviewerAuthority = metadata(text, "Reviewer authority");
  const packageKind = metadata(text, "Package kind");
  const members = list(metadata(text, "Package member artifact IDs"));
  const upstream = metadata(text, "Upstream binding");
  const aggregate = metadata(text, "Aggregate package revision");
  const findingIds = list(metadata(text, "Material findings"));
  const correctionTargets = list(metadata(text, "Correction targets"));
  const recording = metadata(text, "Recording status");
  if (!ID.test(reviewId ?? "") || !/^r\d+$/.test(round ?? "") || stage !== `${request.package_kind}-review` || reviewerAuthority !== stage || packageKind !== request.package_kind || !REVIEW_PACKAGE_OUTCOMES.includes(outcome) || recording !== "recorded") {
    throw packageError("RL_INVALID_REQUEST", "Package review evidence has invalid identity, authority, outcome, or recording fields.", "review-package-review-shape", [String(reviewId), String(stage), String(outcome)]);
  }
  if (canonicalJson(members) !== canonicalJson(context.member_artifact_ids) || upstream !== context.upstream_binding || aggregate !== context.aggregate_revision) throw packageError("RL_STALE_EVIDENCE", "Package review evidence does not bind the exact current package.", "review-package-review-identity", [reviewId, String(aggregate), String(context.aggregate_revision)]);
  const findings = parseFindings(text, findingIds, context);
  if (outcome === "approved" && findings.length) throw packageError("RL_UNRESOLVED_MATERIAL_FINDING", "Approved package review cannot retain material findings.", "review-package-findings", findingIds);
  if (outcome === "changes-requested" && !findings.length) throw packageError("RL_INVALID_REQUEST", "Changes-requested package review requires at least one attributable finding.", "review-package-findings", [reviewId]);
  if (correctionTargets.some((target) => !ID.test(target)) || new Set(correctionTargets).size !== correctionTargets.length) throw packageError("RL_INVALID_REQUEST", "Package review correction targets must be unique safe identifiers.", "review-package-correction-targets", correctionTargets);
  const log = logEntry(root, change.change_id, reviewId);
  if (metadata(log.entry, "Stage") !== stage || metadata(log.entry, "Round") !== round || metadata(log.entry, "Status") !== outcome || canonicalJson(list(metadata(log.entry, "Material findings")).sort()) !== canonicalJson([...findingIds].sort())) throw packageError("RL_INVALID_REQUEST", "Package review evidence contradicts its canonical review-log occurrence.", "review-log-consistency", [reviewId]);
  return {
    package_kind: request.package_kind,
    member_artifact_ids: members,
    upstream_binding: upstream,
    aggregate_revision: aggregate,
    review_id: reviewId,
    round,
    reviewer_authority: reviewerAuthority,
    outcome,
    findings,
    correction_targets: correctionTargets,
    evidence_path: request.evidence_path,
    evidence_sha256: hash(readFileSync(absolute)),
    review_log_path: log.path,
    review_log_sha256: log.sha256,
    stage_authority: request.stage_authority,
  };
}

export function packageProjection(review) {
  return {
    aggregate_revision: review.aggregate_revision,
    authority: review.outcome === "approved" ? "granted" : "withheld",
    correction_targets: review.correction_targets,
    findings: review.findings,
    latest_review: { evidence_path: review.evidence_path, outcome: review.outcome, review_id: review.review_id, reviewer_authority: review.reviewer_authority, round: review.round },
    member_artifact_ids: review.member_artifact_ids,
    package_kind: review.package_kind,
    state: review.outcome,
    upstream_binding: review.upstream_binding,
  };
}

export function validateStoredReviewPackages(change) {
  const errors = [];
  for (const [kind, review] of Object.entries(change.lifecycle_cli?.package_reviews ?? {})) {
    if (!REVIEW_PACKAGE_KINDS.includes(kind) || review?.package_kind !== kind) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored package review kind ${String(kind)} is unknown or contradictory.`, "review-package-kind", [kind, String(review?.package_kind)]));
    if (!REVIEW_PACKAGE_OUTCOMES.includes(review?.outcome)) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored package review outcome ${String(review?.outcome)} is unknown.`, "review-package-outcome", [kind, String(review?.outcome)]));
    if (review?.stage_authority !== `${kind}-review` || review?.reviewer_authority !== `${kind}-review`) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored package review authority contradicts its package kind.", "review-package-authority", [kind, String(review?.stage_authority), String(review?.reviewer_authority)]));
    if (!Array.isArray(review?.member_artifact_ids) || review.member_artifact_ids.some((id) => !ID.test(id)) || new Set(review.member_artifact_ids).size !== review.member_artifact_ids.length) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored package review members are invalid.", "review-package-membership", [kind]));
    if (!/^sha256:[a-f0-9]{64}$/.test(review?.aggregate_revision ?? "")) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored package review aggregate revision is invalid.", "review-package-revision", [kind]));
    for (const finding of review?.findings ?? []) if (!REVIEW_PACKAGE_FINDING_SCOPES.includes(finding?.scope)) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored package review finding scope ${String(finding?.scope)} is unknown.`, "review-package-finding-scope", [kind, String(finding?.finding_id)]));
  }
  for (const [kind, projection] of Object.entries(change.review_packages ?? {})) {
    if (!REVIEW_PACKAGE_KINDS.includes(kind) || projection?.package_kind !== kind) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored review package kind ${String(kind)} is unknown or contradictory.`, "review-package-kind", [kind, String(projection?.package_kind)]));
    if (!REVIEW_PACKAGE_STATES.includes(projection?.state)) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored review package state ${String(projection?.state)} is unknown.`, "review-package-state", [kind, String(projection?.state)]));
    if (!Array.isArray(projection?.member_artifact_ids) || projection.member_artifact_ids.some((id) => !ID.test(id)) || new Set(projection.member_artifact_ids).size !== projection.member_artifact_ids.length) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored review package members are invalid.", "review-package-membership", [kind]));
    if (!/^sha256:[a-f0-9]{64}$/.test(projection?.aggregate_revision ?? "")) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored review package aggregate revision is invalid.", "review-package-revision", [kind]));
    if ((projection?.state === "approved") !== (projection?.authority === "granted")) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored review package authority contradicts its state.", "review-package-authority", [kind, String(projection?.state), String(projection?.authority)]));
    for (const finding of projection?.findings ?? []) if (!REVIEW_PACKAGE_FINDING_SCOPES.includes(finding?.scope)) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored package finding scope ${String(finding?.scope)} is unknown.`, "review-package-finding-scope", [kind, String(finding?.finding_id)]));
  }
  return errors;
}
