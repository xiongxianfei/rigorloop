import { createHash } from "node:crypto";
import { existsSync, lstatSync, readFileSync } from "node:fs";
import { relative, resolve, sep } from "node:path";

import { canonicalJson } from "./lifecycle-contract.js";

export const REVIEW_PACKAGE_KINDS = Object.freeze(["design", "delivery"]);
export const REVIEW_PACKAGE_OUTCOMES = Object.freeze(["approved", "changes-requested", "blocked", "inconclusive"]);
export const REVIEW_PACKAGE_FINDING_SCOPES = Object.freeze(["artifact-local", "cross-artifact", "upstream-direction"]);
export const REVIEW_PACKAGE_STATES = Object.freeze(["review-required", ...REVIEW_PACKAGE_OUTCOMES]);

const ID = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;

function diagnostic(code, summary, invariant, identities = [], correctiveOperation = null) {
  return { code, summary, blocking_invariant: invariant, relevant_identities: identities, corrective_operation: correctiveOperation };
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

function hash(bytes) { return createHash("sha256").update(bytes).digest("hex"); }
function list(value) { return value === null || value === undefined || /^none$/i.test(String(value).trim()) ? [] : String(value).split(",").map((item) => item.trim().replace(/^`|`$/g, "")).filter(Boolean); }
function metadata(text, label) { const match = new RegExp(`^${label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}:\\s*(.+?)\\s*$`, "m").exec(text); return match?.[1]?.trim() ?? null; }

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
    if (plans.length !== 1) return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Delivery package requires exactly one primary plan artifact.", "review-package-membership", plans.map(([id]) => id)) };
    return { entries: [plans[0]] };
  }
  return { error: diagnostic("RL_INVALID_REQUEST", `Unknown review package kind ${String(kind)}.`, "review-package-kind", [String(kind)]) };
}

function upstreamReviewId(change, kind) {
  if (kind === "design") {
    const proposal = Object.entries(change.artifact_states ?? {}).filter(([, entry]) => entry?.kind === "proposal" && entry?.role === "primary");
    if (proposal.length !== 1 || proposal[0][1]?.lifecycle_state !== "accepted" || proposal[0][1]?.review?.outcome !== "approved" || !ID.test(proposal[0][1]?.review?.id ?? "")) return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Design package requires one accepted Proposal Review ID.", "review-package-upstream", proposal.map(([id]) => id)) };
    return { value: proposal[0][1].review.id };
  }
  const design = change.review_packages?.design;
  if (design?.status !== "approved" || !ID.test(design?.review_id ?? "")) return { error: diagnostic("RL_OPERATION_NOT_PERMITTED", "Delivery package requires one approved Design Review ID.", "review-package-upstream", [String(design?.review_id ?? "none")]) };
  return { value: design.review_id };
}

export function reviewPackageContext(root, change, kind) {
  if (!REVIEW_PACKAGE_KINDS.includes(kind)) return { package_kind: kind, members: {}, upstream_review_id: null, status: "invalid", authority: "withheld", latest_review: null, correction_targets: [], blockers: [], errors: [diagnostic("RL_INVALID_REQUEST", `Unknown review package kind ${String(kind)}.`, "review-package-kind", [String(kind)])], next_permitted_operation: null };
  const membership = currentMembers(change, kind);
  const upstream = upstreamReviewId(change, kind);
  const errors = [membership.error, upstream.error].filter(Boolean);
  const members = {};
  if (!membership.error) for (const [artifactId, entry] of membership.entries) {
    const registration = change.lifecycle_cli?.artifacts?.[artifactId];
    if (!repositoryFile(root, entry?.path) || registration?.artifact_path !== entry?.path || registration?.artifact_kind !== entry?.kind || registration?.artifact_role !== entry?.role) errors.push(diagnostic("RL_INVALID_REQUEST", `Package member ${artifactId} is missing a safe exact artifact registration.`, "review-package-member-registration", [artifactId, String(entry?.path)]));
    else members[artifactId] = entry.path;
  }
  const projection = change.review_packages?.[kind] ?? null;
  const latest = change.lifecycle_cli?.package_reviews?.[kind] ?? null;
  if (latest) {
    const reviewPath = repositoryFile(root, latest.evidence_path);
    if (!reviewPath || hash(readFileSync(reviewPath)) !== latest.evidence_sha256) {
      errors.push(diagnostic("RL_STALE_EVIDENCE", `${kind} package review evidence is missing or stale.`, "review-package-review-freshness", [String(latest.review_id), String(latest.evidence_path)], "record-package-review"));
    }
    try {
      const log = logEntry(root, change.change_id, latest.review_id);
      if (log.path !== latest.review_log_path || !log.compatible_sha256.includes(latest.review_log_sha256)) errors.push(diagnostic("RL_STALE_EVIDENCE", `${kind} package review log is stale.`, "review-package-review-freshness", [String(latest.review_id), String(latest.review_log_path)], "record-package-review"));
    } catch (error) {
      errors.push(error.diagnostic ?? diagnostic("RL_STALE_EVIDENCE", `${kind} package review log is missing or stale.`, "review-package-review-freshness", [String(latest.review_id)], "record-package-review"));
    }
  }
  const projectionCurrent = projection && canonicalJson(projection.members) === canonicalJson(members) && projection.upstream_review_id === upstream.value;
  const status = errors.length ? "incomplete" : projection && !projectionCurrent ? "review-required" : projection?.status ?? "review-required";
  const authority = status === "approved" ? "granted" : "withheld";
  const registeredCurrent = latest && canonicalJson(latest.members) === canonicalJson(members) && latest.upstream_review_id === upstream.value;
  const registeredPendingSettlement = registeredCurrent && (!projection || projection.review_id !== latest.review_id);
  let nextOperation = null;
  if (!errors.length && registeredPendingSettlement) nextOperation = "settle-review-package";
  else if (!errors.length && !projection) nextOperation = "record-package-review";
  else if (!errors.length && status === "review-required") nextOperation = "record-package-review";
  else if (!errors.length && status === "changes-requested" && (projection?.correction_targets ?? []).length) nextOperation = "route-correction";
  else if (!errors.length && status === "blocked" && (projection?.correction_targets ?? []).length) nextOperation = "route-correction";
  else if (!errors.length && status === "blocked" && !(projection?.correction_targets ?? []).length) nextOperation = "record-package-review";
  else if (!errors.length && status === "inconclusive") nextOperation = "record-package-review";
  const blockers = status === "approved" || errors.length ? [] : [diagnostic("RL_OPERATION_NOT_PERMITTED", `${kind} package is ${status} and grants no progression authority.`, "review-package-authority", [`review-package:${kind}`, status], nextOperation)];
  return { package_kind: kind, members, upstream_review_id: upstream.value ?? null, status, authority, latest_review: latest ? { review_id: latest.review_id, round: latest.round, outcome: latest.outcome, evidence_path: latest.evidence_path } : null, correction_targets: projection?.correction_targets ?? latest?.correction_targets ?? [], blockers, errors, next_permitted_operation: nextOperation };
}

function logEntry(root, changeId, reviewId) {
  const path = `docs/changes/${changeId}/review-log.md`;
  const absolute = repositoryFile(root, path);
  if (!absolute) throw packageError("RL_INVALID_REQUEST", "Package review requires a canonical review log.", "review-log-consistency", [reviewId]);
  const text = readFileSync(absolute, "utf8");
  const indexes = [...text.matchAll(new RegExp(`^Review ID: ${reviewId.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`, "gm"))];
  if (indexes.length !== 1) throw packageError("RL_INVALID_REQUEST", "Review log must contain exactly one package review occurrence.", "review-log-consistency", [reviewId]);
  const start = indexes[0].index;
  const remainder = text.slice(start);
  const nextHeading = /\n#{2,6}\s+/.exec(remainder);
  const entry = remainder.slice(0, nextHeading?.index).trimEnd();
  const compatibleSha256 = new Set([hash(entry)]);
  if (nextHeading) {
    const afterEntry = remainder.slice(nextHeading.index + 1);
    const nextSection = /\n##\s+/.exec(afterEntry);
    if (nextSection) {
      const sectionStart = nextHeading.index + 1 + nextSection.index;
      compatibleSha256.add(hash(`${entry}\n${remainder.slice(sectionStart)}`.trimEnd()));
    }
  }
  return { path, sha256: hash(entry), compatible_sha256: [...compatibleSha256], entry };
}

function parseFindings(text, declared, context, change) {
  const findings = text.split(/(?=^### Finding\s+)/m).slice(1).map((block) => ({ finding_id: metadata(block, "Finding ID"), scope: metadata(block, "Finding scope"), affected_artifact_ids: list(metadata(block, "Affected artifact IDs")), owning_stages: list(metadata(block, "Owning stages")), evidence: metadata(block, "Evidence"), required_outcome: metadata(block, "Required outcome"), safe_resolution_path: metadata(block, "Safe resolution path") }));
  if (canonicalJson(findings.map((finding) => finding.finding_id).sort()) !== canonicalJson([...declared].sort())) throw packageError("RL_INVALID_REQUEST", "Package review finding blocks do not match Material findings.", "review-package-findings", declared);
  const memberIds = Object.keys(context.members);
  for (const finding of findings) {
    if (!ID.test(finding.finding_id ?? "") || !REVIEW_PACKAGE_FINDING_SCOPES.includes(finding.scope)) throw packageError("RL_INVALID_REQUEST", `Package review finding scope ${String(finding.scope)} is unknown.`, "review-package-finding-scope", [String(finding.finding_id)]);
    if (!finding.evidence || !finding.required_outcome || !finding.safe_resolution_path || !finding.owning_stages.length) throw packageError("RL_INVALID_REQUEST", "Package review finding is missing required evidence, outcome, resolution, or ownership.", "review-package-findings", [finding.finding_id]);
    const affected = finding.affected_artifact_ids;
    if (finding.scope === "artifact-local" && (affected.length !== 1 || !memberIds.includes(affected[0]))) throw packageError("RL_INVALID_REQUEST", "Artifact-local finding must identify exactly one package member.", "review-package-finding-attribution", [finding.finding_id, ...affected]);
    if (finding.scope === "cross-artifact" && (affected.length < 2 || affected.some((id) => !memberIds.includes(id)))) throw packageError("RL_INVALID_REQUEST", "Cross-artifact finding must identify at least two package members.", "review-package-finding-attribution", [finding.finding_id, ...affected]);
    if (finding.scope === "upstream-direction" && (affected.length !== 1 || ![context.package_kind === "design" ? "proposal" : "design"].includes(affected[0]))) throw packageError("RL_INVALID_REQUEST", "Upstream-direction finding must identify the owning upstream artifact or package.", "review-package-finding-attribution", [finding.finding_id, ...affected]);
    const expectedOwners = finding.scope === "upstream-direction"
      ? [context.package_kind === "design" ? "proposal" : "design-review"]
      : [...new Set(affected.map((id) => change.artifact_states?.[id]?.kind === "adr" ? "architecture" : change.artifact_states?.[id]?.kind))].filter(Boolean);
    if (canonicalJson([...finding.owning_stages].sort()) !== canonicalJson([...expectedOwners].sort())) throw packageError("RL_AUTHORITY_BOUNDARY", "Package finding owning stages do not match affected artifact owners.", "review-package-finding-ownership", [finding.finding_id, ...finding.owning_stages, ...expectedOwners]);
  }
  return findings;
}

export function readPackageReview(root, change, request, context) {
  const absolute = repositoryFile(root, request.evidence_path);
  if (!absolute) throw packageError("RL_INVALID_REQUEST", "Package review evidence must be one safe regular file.", "review-package-evidence", [String(request.evidence_path)]);
  const text = readFileSync(absolute, "utf8");
  const reviewId = metadata(text, "Review ID"); const round = metadata(text, "Round"); const stage = metadata(text, "Stage"); const outcome = metadata(text, "Status"); const reviewerAuthority = metadata(text, "Reviewer authority"); const packageKind = metadata(text, "Package kind"); const upstreamReviewId = metadata(text, "Upstream review ID"); const findingIds = list(metadata(text, "Material findings")); const correctionTargets = list(metadata(text, "Correction targets"));
  const members = Object.fromEntries(list(metadata(text, "Package members")).map((entry) => { const split = entry.indexOf("="); return split > 0 ? [entry.slice(0, split).trim(), entry.slice(split + 1).trim()] : [entry, ""]; }));
  if (!ID.test(reviewId ?? "") || !/^r\d+$/.test(round ?? "") || stage !== `${request.package_kind}-review` || reviewerAuthority !== stage || packageKind !== request.package_kind || !REVIEW_PACKAGE_OUTCOMES.includes(outcome) || metadata(text, "Recording status") !== "recorded") throw packageError("RL_INVALID_REQUEST", "Package review evidence has invalid identity, authority, outcome, or recording fields.", "review-package-review-shape", [String(reviewId), String(stage), String(outcome)]);
  if (canonicalJson(members) !== canonicalJson(context.members) || upstreamReviewId !== context.upstream_review_id) throw packageError("RL_STALE_EVIDENCE", "Package review evidence does not bind the current member map and upstream review ID.", "review-package-review-identity", [reviewId]);
  const findings = parseFindings(text, findingIds, context, change);
  if (outcome === "approved" && findings.length) throw packageError("RL_UNRESOLVED_MATERIAL_FINDING", "Approved package review cannot retain material findings.", "review-package-findings", findingIds);
  if (outcome === "changes-requested" && !findings.length) throw packageError("RL_INVALID_REQUEST", "Changes-requested package review requires at least one attributable finding.", "review-package-findings", [reviewId]);
  if (correctionTargets.some((target) => !ID.test(target)) || new Set(correctionTargets).size !== correctionTargets.length) throw packageError("RL_INVALID_REQUEST", "Package review correction targets must be unique safe identifiers.", "review-package-correction-targets", correctionTargets);
  const expectedTargets = [...new Set(findings.flatMap((finding) => finding.affected_artifact_ids))].sort();
  if (canonicalJson([...correctionTargets].sort()) !== canonicalJson(expectedTargets)) throw packageError("RL_AUTHORITY_BOUNDARY", "Package correction targets must exactly match the affected artifacts.", "review-package-correction-targets", [...correctionTargets, ...expectedTargets]);
  const log = logEntry(root, change.change_id, reviewId);
  if (metadata(log.entry, "Stage") !== stage || metadata(log.entry, "Round") !== round || metadata(log.entry, "Status") !== outcome || canonicalJson(list(metadata(log.entry, "Material findings")).sort()) !== canonicalJson([...findingIds].sort())) throw packageError("RL_INVALID_REQUEST", "Package review evidence contradicts its canonical review-log occurrence.", "review-log-consistency", [reviewId]);
  return { package_kind: request.package_kind, members, upstream_review_id: upstreamReviewId, review_id: reviewId, round, reviewer_authority: reviewerAuthority, outcome, findings, correction_targets: correctionTargets, evidence_path: request.evidence_path, evidence_sha256: hash(readFileSync(absolute)), review_log_path: log.path, review_log_sha256: log.sha256, stage_authority: request.stage_authority };
}

export function packageProjection(review) { return { authority: review.outcome === "approved" ? "granted" : "withheld", correction_targets: review.correction_targets, findings: review.findings, members: review.members, outcome: review.outcome, package_kind: review.package_kind, review_id: review.review_id, review_round: review.round, status: review.outcome, upstream_review_id: review.upstream_review_id }; }

function validMembers(value) { return value && typeof value === "object" && !Array.isArray(value) && Object.keys(value).length > 0 && Object.entries(value).every(([id, path]) => ID.test(id) && typeof path === "string" && path.length > 0); }
export function validateStoredReviewPackages(change) {
  const errors = [];
  for (const [kind, review] of Object.entries(change.lifecycle_cli?.package_reviews ?? {})) {
    if (!REVIEW_PACKAGE_KINDS.includes(kind) || review?.package_kind !== kind) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored package review kind ${String(kind)} is unknown or contradictory.`, "review-package-kind", [kind]));
    if (!REVIEW_PACKAGE_OUTCOMES.includes(review?.outcome)) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored package review outcome ${String(review?.outcome)} is unknown.`, "review-package-outcome", [kind]));
    if (!validMembers(review?.members)) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored package review members are invalid.", "review-package-membership", [kind]));
  }
  for (const [kind, projection] of Object.entries(change.review_packages ?? {})) {
    if (!REVIEW_PACKAGE_KINDS.includes(kind) || projection?.package_kind !== kind) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored review package kind ${String(kind)} is unknown or contradictory.`, "review-package-kind", [kind]));
    if (!REVIEW_PACKAGE_STATES.includes(projection?.status)) errors.push(diagnostic("RL_INVALID_REQUEST", `Stored review package status ${String(projection?.status)} is unknown.`, "review-package-status", [kind]));
    if (!validMembers(projection?.members)) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored review package members are invalid.", "review-package-membership", [kind]));
    if ((projection?.status === "approved") !== (projection?.authority === "granted")) errors.push(diagnostic("RL_INVALID_REQUEST", "Stored review package authority contradicts its status.", "review-package-authority", [kind]));
  }
  return errors;
}
