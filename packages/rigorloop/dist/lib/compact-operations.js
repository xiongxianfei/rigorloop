import { createHash } from "node:crypto";

import { compactLifecycleRevision, parseCompactMarkdown, parseCompactYaml, validateCompactRecord, validateCompactSet } from "./compact-contract.js";
import { compactOperationEligibility } from "./compact-eligibility.js";
import { serializeLifecycleYaml } from "./lifecycle-contract.js";

const SENTINEL = `sha256:${"0".repeat(64)}`;
const REVIEWER_BY_KIND = Object.freeze({ proposal: "proposal-review", "design-package": "design-review", "delivery-package": "delivery-review", milestone: "code-review", "final-code": "code-review" });
const NEXT_STAGE = Object.freeze({ proposal: "proposal-review", "proposal-review": "architecture", architecture: "spec", spec: "design-review", "design-review": "plan", plan: "delivery-review", "delivery-review": "implement", implement: "code-review", "ci-maintenance": "verify", verify: "pr" });

function sha256(value) {
  return `sha256:${createHash("sha256").update(value).digest("hex")}`;
}

function fail(code, message) {
  const error = new Error(message);
  error.code = code;
  return error;
}

function sortedObject(value) {
  return Object.fromEntries(Object.entries(value ?? {}).sort(([left], [right]) => Buffer.compare(Buffer.from(left), Buffer.from(right))));
}

function markdown(record, priorBody = "") {
  return `---\n${serializeLifecycleYaml(record)}---\n${priorBody}`;
}

function inputBytes(input, resolvedInputs) {
  if (input.source === "inline") return Buffer.from(input.content, "utf8");
  const value = resolvedInputs[input.source_path];
  if (value === undefined || value === null) throw fail("RL_INVALID_REQUEST", "content source_path was not resolved");
  const bytes = Buffer.isBuffer(value) ? Buffer.from(value) : Buffer.from(value, "utf8");
  if (sha256(bytes) !== input.identity) throw fail("RL_INVALID_REQUEST", "resolved content identity does not match");
  return bytes;
}

function expectedState(request, currentFiles) {
  const expected = Object.keys(request.expected_files).sort();
  const actual = Object.keys(currentFiles).sort();
  if (JSON.stringify(expected) !== JSON.stringify(actual)) throw fail("RL_STALE_OPERATION", "expected_files must bind the complete evaluator input");
  for (const path of actual) {
    const bytes = currentFiles[path];
    const row = request.expected_files[path];
    const identity = bytes === null ? null : sha256(bytes);
    if (row.path !== path || row.state !== (bytes === null ? "absent" : "present") || row.identity !== identity) throw fail("RL_STALE_OPERATION", `expected identity is stale for ${path}`);
  }
}

function exactPathSet(actual, expected, message) {
  const left = [...actual].sort();
  const right = [...expected].sort();
  if (JSON.stringify(left) !== JSON.stringify(right)) throw fail("RL_STALE_OPERATION", message);
}

function authoritative(change, files) {
  const path = `docs/changes/${change.change_id}/change.yaml`;
  const selected = new Set([
    ...Object.values(change.artifacts ?? {}).map((entry) => entry.path),
    ...Object.values(change.reviews ?? {}).map((entry) => entry.path),
    ...Object.values(change.material_decisions ?? {}).map((entry) => entry.path),
    ...Object.values(change.evidence ?? {}).map((entry) => entry.manifest_path),
    ...(change.readiness === "verified" ? [`docs/changes/${change.change_id}/verify-report.md`] : []),
  ]);
  const rest = Object.fromEntries([...selected].sort().map((entry) => [entry, files[entry]]));
  return { path, rest };
}

function parseCurrent(currentFiles, changeId) {
  const path = `docs/changes/${changeId}/change.yaml`;
  const bytes = currentFiles[path];
  if (!bytes) throw fail("RL_CHANGE_NOT_FOUND", "compact change coordinator is missing");
  const changeBytes = Buffer.isBuffer(bytes) ? bytes.toString("utf8") : bytes;
  let change;
  try { change = parseCompactYaml(changeBytes, "compact-change-v1"); }
  catch (error) { throw fail("RL_INVALID_CURRENT_STATE", error.message); }
  let validated;
  try { validated = validateCompactSet({ changeBytes, files: authoritative(change, currentFiles).rest }); }
  catch (error) { throw fail("RL_INVALID_CURRENT_STATE", error.message); }
  return { path, change: structuredClone(validated.change), parsed: validated };
}

function replaceContent(files, input, resolvedInputs) {
  const bytes = inputBytes(input, resolvedInputs);
  if (sha256(bytes) !== input.identity) throw fail("RL_INVALID_REQUEST", "content input identity does not match bytes");
  files[input.path] = bytes;
  return bytes;
}

function replaceReview(change, files, input, resolvedInputs) {
  const bytes = replaceContent(files, input, resolvedInputs);
  const review = parseCompactMarkdown(bytes.toString("utf8"), "compact-review-v1").record;
  const targetId = review.target.target_id;
  change.reviews[targetId] = {
    target_id: targetId,
    path: input.path,
    identity: sha256(bytes),
    review_id: review.review_id,
    outcome: review.outcome,
    reviewer_authority: review.reviewer_authority,
    status: review.recording_status === "blocked" ? "blocked" : "current",
  };
  for (const [findingId, reference] of Object.entries(change.open_findings)) if (reference.review_target_id === targetId) delete change.open_findings[findingId];
  for (const finding of Object.values(review.open_findings)) change.open_findings[finding.finding_id] = { finding_id: finding.finding_id, review_target_id: targetId, review_path: input.path, review_identity: sha256(bytes), owner: finding.owner, severity: finding.severity, blocking_effect: finding.blocking_effect };
  return review;
}

function requireReviewResponsibility(change, review) {
  const expected = REVIEWER_BY_KIND[review.target.target_kind];
  if (review.reviewer_authority !== expected || change.current_stage !== expected) throw fail("RL_AUTHORITY_BOUNDARY", "review target is not due at its responsible review stage");
}

function canonicalReviewPath(changeId, review) {
  const names = { proposal: "proposal-review.md", "design-package": "design-review.md", "delivery-package": "delivery-review.md", "final-code": "code-review-final.md" };
  return `docs/changes/${changeId}/reviews/${names[review.target.target_kind] ?? `code-review-${review.target.target_id}.md`}`;
}

function replaceDecisions(change, files, input, resolvedInputs) {
  const bytes = replaceContent(files, input, resolvedInputs);
  const decisions = parseCompactMarkdown(bytes.toString("utf8"), "compact-decisions-v1").record.decisions;
  for (const [id, ref] of Object.entries(change.material_decisions)) if (ref.path === input.path) delete change.material_decisions[id];
  for (const decision of Object.values(decisions)) change.material_decisions[decision.decision_id] = { decision_id: decision.decision_id, path: input.path, identity: sha256(bytes), applicability: decision.applicability };
  return decisions;
}

function replaceEvidence(change, files, input, resolvedInputs) {
  const bytes = replaceContent(files, input, resolvedInputs);
  const evidence = parseCompactYaml(bytes.toString("utf8"), "compact-evidence-v1").evidence;
  for (const [id, ref] of Object.entries(change.evidence)) if (ref.manifest_path === input.path) delete change.evidence[id];
  for (const entry of Object.values(evidence)) change.evidence[entry.evidence_id] = { evidence_id: entry.evidence_id, manifest_path: input.path, manifest_identity: sha256(bytes), freshness: entry.freshness };
  return evidence;
}

function requiredSubjectPaths(change, files) {
  const paths = new Set();
  for (const path of new Set(Object.values(change.evidence).map((entry) => entry.manifest_path))) {
    if (files[path] == null) continue;
    const manifest = parseCompactYaml(files[path].toString("utf8"), "compact-evidence-v1");
    for (const entry of Object.values(manifest.evidence)) {
      for (const dependency of entry.invalidating_dependencies) {
        if (dependency.kind === "subject") paths.add(entry.subjects[dependency.id].path);
      }
    }
  }
  return [...paths];
}

function semanticContentInputs(payload) {
  return Object.values(payload).filter((value) => value && typeof value === "object" && !Array.isArray(value) && Object.hasOwn(value, "source") && Object.hasOwn(value, "path"));
}

function candidateObservedPaths(request, resolvedInputs) {
  const paths = new Set();
  for (const input of semanticContentInputs(request.payload)) {
    paths.add(input.path);
    let parsed = null;
    if (request.operation === "update-evidence" || request.operation === "invalidate-evidence") parsed = parseCompactYaml(inputBytes(input, resolvedInputs).toString("utf8"), "compact-evidence-v1");
    if (request.operation === "record-verify") parsed = parseCompactMarkdown(inputBytes(input, resolvedInputs).toString("utf8"), "compact-verify-v1").record;
    const entries = parsed?.evidence ? Object.values(parsed.evidence) : parsed ? [parsed] : [];
    for (const entry of entries) for (const subject of Object.values(entry.subjects ?? {})) paths.add(subject.path);
  }
  return paths;
}

function requiredInputPaths(change, files, request, resolvedInputs) {
  const changeRecordPath = `docs/changes/${change.change_id}/change.yaml`;
  return new Set([changeRecordPath, ...Object.keys(authoritative(change, files).rest), ...requiredSubjectPaths(change, files), ...candidateObservedPaths(request, resolvedInputs)]);
}

function preserveKeys(prior, candidate, selected, code, label) {
  const allowed = new Set(selected);
  const omitted = prior.filter((id) => !allowed.has(id) && !Object.hasOwn(candidate, id));
  if (omitted.length) throw fail(code, `${label} omitted unselected current entries: ${omitted.join(", ")}`);
}

function validateObservedSubjects(entries, files) {
  for (const entry of entries) {
    for (const subject of Object.values(entry.subjects ?? {})) {
      if (!Object.hasOwn(files, subject.path) || files[subject.path] === null || sha256(files[subject.path]) !== subject.identity) throw fail("RL_STALE_OPERATION", `observed subject identity is stale for ${subject.path}`);
    }
  }
}

function settleCorrection(change, outcome, targetId) {
  const correction = change.active_work;
  if (correction?.kind !== "correction" || correction.status !== "review-required" || correction.expected_review_target !== targetId) return;
  if (outcome === "approved") {
    if (correction.finding_ids.some((id) => change.open_findings[id])) throw fail("RL_UNRESOLVED_MATERIAL_FINDING", "the active correction still has an open finding");
    change.active_work = null;
    return;
  }
  if (outcome === "changes-requested") {
    const findings = correction.finding_ids.map((id) => change.open_findings[id]).filter(Boolean);
    const owners = [...new Set(findings.map((finding) => finding.owner))];
    if (owners.length !== 1) throw fail("RL_CORRECTION_ROUTE_INVALID", "changes-requested does not select one coherent correction owner");
    change.active_work = { ...correction, destination_stage: owners[0], owner: owners[0], status: "authoring" };
    change.current_stage = owners[0];
    return;
  }
  change.active_work = { ...correction, status: "blocked" };
}

function settleReviewedArtifacts(change, review, outcome) {
  const kinds = { proposal: new Set(["proposal"]), "design-package": new Set(["architecture", "adr", "spec"]), "delivery-package": new Set(["plan"]) }[review.target.target_kind];
  if (!kinds) return;
  const desired = outcome === "approved"
    ? { proposal: "accepted", "design-package": "approved", "delivery-package": "active" }[review.target.target_kind]
    : outcome === "changes-requested" ? "revision-required" : "blocked";
  for (const artifact of Object.values(change.artifacts)) if (kinds.has(artifact.kind)) artifact.status = desired;
}

function applySemantic(change, files, request, resolvedInputs) {
  const payload = request.payload;
  switch (request.operation) {
    case "record-artifact": {
      const bytes = replaceContent(files, payload.content, resolvedInputs);
      if (payload.artifact.path !== payload.content.path || payload.artifact.identity !== sha256(bytes)) throw fail("RL_INVALID_REQUEST", "artifact and content identities differ");
      const prior = change.artifacts[payload.artifact.artifact_id];
      if (prior && ["kind", "role", "path", "owner"].some((field) => prior[field] !== payload.artifact[field])) throw fail("RL_AUTHORITY_BOUNDARY", "artifact revision cannot change stable registration fields");
      if (Object.values(change.artifacts).some((entry) => entry.artifact_id !== payload.artifact.artifact_id && entry.path === payload.artifact.path)) throw fail("RL_AUTHORITY_BOUNDARY", "artifact path is already registered to another artifact");
      change.artifacts[payload.artifact.artifact_id] = payload.artifact;
      break;
    }
    case "advance-stage":
      if (NEXT_STAGE[payload.from_stage] !== payload.to_stage && !new Set(["code-review>implement", "code-review>ci-maintenance", "code-review>verify", "review-resolution>implement", "review-resolution>verify"]).has(`${payload.from_stage}>${payload.to_stage}`)) throw fail("RL_OPERATION_NOT_PERMITTED", "stage transition is not an approved lifecycle edge");
      change.current_stage = payload.to_stage;
      break;
    case "replace-review": {
      const prior = change.reviews[payload.target_id];
      const priorFindings = Object.values(change.open_findings).filter((finding) => finding.review_target_id === payload.target_id).map((finding) => finding.finding_id);
      const review = replaceReview(change, files, payload.review, resolvedInputs);
      requireReviewResponsibility(change, review);
      if (review.target.target_id !== payload.target_id || review.reviewer_authority !== REVIEWER_BY_KIND[review.target.target_kind]) throw fail("RL_AUTHORITY_BOUNDARY", "review target and responsibility metadata are inconsistent");
      if (payload.review.path !== canonicalReviewPath(change.change_id, review) || prior && prior.path !== payload.review.path) throw fail("RL_AUTHORITY_BOUNDARY", "review replacement must use its stable canonical path");
      const omitted = priorFindings.filter((id) => !review.open_findings[id]);
      if (omitted.some((id) => !payload.resolutions[id])) throw fail("RL_FINDING_LOSS", "replacement review omitted an open finding without a final disposition");
      for (const id of omitted) if (payload.resolutions[id].materiality === "material" && !change.material_decisions[payload.resolutions[id].decision_id]) throw fail("RL_DECISION_REQUIRED", "material resolution must already have current decision memory");
      if ((prior?.identity ?? null) !== payload.prior_review_identity) throw fail("RL_STALE_OPERATION", "prior review identity does not match");
      break;
    }
    case "settle-review": {
      const reference = change.reviews[payload.target_id];
      const review = parseCompactMarkdown(files[reference.path].toString("utf8"), "compact-review-v1").record;
      requireReviewResponsibility(change, review);
      reference.status = payload.outcome === "approved" ? "current" : payload.outcome === "changes-requested" ? "review-required" : "blocked";
      settleReviewedArtifacts(change, review, payload.outcome);
      settleCorrection(change, payload.outcome, payload.target_id);
      break;
    }
    case "resolve-finding": {
      const id = payload.resolution.finding_id;
      const prior = change.open_findings[id];
      if (!prior) throw fail("RL_OPERATION_NOT_PERMITTED", "finding is not current");
      const otherFindings = Object.values(change.open_findings).filter((finding) => finding.review_target_id === prior.review_target_id && finding.finding_id !== id).map((finding) => finding.finding_id);
      const review = replaceReview(change, files, payload.review, resolvedInputs);
      if (review.target.target_id !== prior.review_target_id) throw fail("RL_FINDING_LOSS", "finding resolution must replace its exact current review");
      if (payload.review.path !== canonicalReviewPath(change.change_id, review)) throw fail("RL_AUTHORITY_BOUNDARY", "finding resolution must preserve the stable review path");
      if (review.open_findings[id]) throw fail("RL_FINDING_LOSS", "resolved finding remains open in candidate review");
      if (otherFindings.some((findingId) => !review.open_findings[findingId])) throw fail("RL_FINDING_LOSS", "finding resolution omitted another open finding");
      if (payload.resolution.materiality === "material") {
        if (payload.decisions) replaceDecisions(change, files, payload.decisions, resolvedInputs);
        if (!change.material_decisions[payload.resolution.decision_id]) throw fail("RL_DECISION_REQUIRED", "material finding resolution requires current decision memory");
      } else if (payload.decisions) throw fail("RL_INVALID_REQUEST", "non-material resolution cannot supply decisions content");
      break;
    }
    case "upsert-decision": {
      if (payload.decisions.path !== `docs/changes/${change.change_id}/material-decisions.md`) throw fail("RL_AUTHORITY_BOUNDARY", "material decisions must use the stable canonical path");
      const prior = Object.values(change.material_decisions).filter((entry) => entry.path === payload.decisions.path).map((entry) => entry.decision_id);
      const priorRecord = change.material_decisions[payload.decision_id]
        ? parseCompactMarkdown(files[change.material_decisions[payload.decision_id].path].toString("utf8"), "compact-decisions-v1").record.decisions[payload.decision_id]
        : null;
      const decisions = replaceDecisions(change, files, payload.decisions, resolvedInputs);
      if (!decisions[payload.decision_id]) throw fail("RL_INVALID_REQUEST", "candidate decisions omit the selected decision");
      const decision = decisions[payload.decision_id];
      if (priorRecord && (decision.decision_id !== priorRecord.decision_id || decision.source.kind !== priorRecord.source.kind || decision.source.id !== priorRecord.source.id || decision.owner !== priorRecord.owner)) throw fail("RL_AUTHORITY_BOUNDARY", "decision update cannot change stable identity, source, or owner");
      if (change.current_stage !== "review-resolution" && (!priorRecord || priorRecord.owner !== change.current_stage)) throw fail("RL_OPERATION_NOT_PERMITTED", "decision update is not owned by the current stage");
      if (!priorRecord && decision.source.kind === "finding" && !change.open_findings[decision.source.id]) throw fail("RL_OPERATION_NOT_PERMITTED", "new decision does not name a current finding");
      preserveKeys(prior, decisions, [payload.decision_id], "RL_DECISION_LOSS", "decision update");
      break;
    }
    case "remove-decision": {
      const ref = change.material_decisions[payload.decision_id];
      if (!ref) throw fail("RL_OPERATION_NOT_PERMITTED", "decision is not current");
      const parsed = parseCompactMarkdown(files[ref.path].toString("utf8"), "compact-decisions-v1");
      const references = JSON.stringify({ artifacts: change.artifacts, reviews: change.reviews, evidence: change.evidence, blockers: change.blockers, remaining_work: change.remaining_work });
      if (references.includes(payload.decision_id)) throw fail("RL_DECISION_REFERENCED", "decision remains referenced by current state");
      delete parsed.record.decisions[payload.decision_id];
      delete change.material_decisions[payload.decision_id];
      if (Object.keys(parsed.record.decisions).length === 0) files[ref.path] = null;
      else {
        const bytes = Buffer.from(markdown(parsed.record, parsed.markdown));
        files[ref.path] = bytes;
        for (const item of Object.values(change.material_decisions)) if (item.path === ref.path) item.identity = sha256(bytes);
      }
      break;
    }
    case "route-correction":
      change.active_work = { kind: "correction", ...payload.correction, status: "authoring" };
      change.current_stage = payload.correction.destination_stage;
      break;
    case "return-correction":
      change.active_work = { ...change.active_work, status: "review-required" };
      change.current_stage = payload.return_stage;
      if (change.reviews[change.active_work.expected_review_target]) change.reviews[change.active_work.expected_review_target].status = "review-required";
      break;
    case "advance-milestone":
      if (change.active_work === null) {
        if (payload.from_status !== null || payload.to_status !== "planned") throw fail("RL_OPERATION_NOT_PERMITTED", "milestone selection must transition from null to planned");
        const pending = change.remaining_work[payload.milestone_id];
        if (!pending || pending.work_id !== payload.milestone_id || pending.kind !== "milestone" || pending.owner !== "implement" || pending.status !== "pending") throw fail("RL_OPERATION_NOT_PERMITTED", "milestone selection requires one exact pending implementation milestone");
        delete change.remaining_work[payload.milestone_id];
        change.active_work = { kind: "milestone", milestone_id: payload.milestone_id, status: "planned", owner: "implement" };
      } else {
        if (![["planned", "implementing"], ["implementing", "review-required"], ["review-required", "closed"]].some(([from, to]) => from === payload.from_status && to === payload.to_status)) throw fail("RL_OPERATION_NOT_PERMITTED", "milestone transition is not adjacent");
        change.active_work = payload.to_status === "closed" ? null : { ...change.active_work, status: payload.to_status };
      }
      break;
    case "update-evidence": {
      if (payload.evidence.path !== `docs/changes/${change.change_id}/evidence.yaml`) throw fail("RL_AUTHORITY_BOUNDARY", "evidence must use the stable canonical path");
      const prior = Object.values(change.evidence).filter((entry) => entry.manifest_path === payload.evidence.path).map((entry) => entry.evidence_id);
      const evidence = replaceEvidence(change, files, payload.evidence, resolvedInputs);
      if (payload.evidence_ids.some((id) => !evidence[id])) throw fail("RL_INVALID_REQUEST", "candidate evidence omits a selected evidence identity");
      preserveKeys(prior, evidence, payload.evidence_ids, "RL_EVIDENCE_LOSS", "evidence update");
      const selected = payload.evidence_ids.map((id) => evidence[id]);
      const expectedProducer = change.active_work?.kind === "correction" ? change.active_work.owner : change.current_stage;
      if (selected.some((entry) => entry.producer_authority !== expectedProducer)) throw fail("RL_AUTHORITY_BOUNDARY", "evidence producer responsibility does not match current work");
      validateObservedSubjects(selected, files);
      break;
    }
    case "invalidate-evidence": {
      if (payload.evidence === null) {
        if (payload.evidence_ids.length !== Object.keys(change.evidence).length || payload.evidence_ids.some((id) => !change.evidence[id])) throw fail("RL_EVIDENCE_LOSS", "null evidence replacement must remove the complete current manifest");
        for (const id of payload.evidence_ids) delete change.evidence[id];
        const paths = [...new Set(Object.values(change.evidence).map((entry) => entry.manifest_path))];
        for (const path of Object.keys(files)) if (path.endsWith("/evidence.yaml") && !paths.includes(path)) files[path] = null;
      } else {
        if (payload.evidence.path !== `docs/changes/${change.change_id}/evidence.yaml`) throw fail("RL_AUTHORITY_BOUNDARY", "evidence must use the stable canonical path");
        const prior = Object.values(change.evidence).filter((entry) => entry.manifest_path === payload.evidence.path).map((entry) => entry.evidence_id);
        const evidence = replaceEvidence(change, files, payload.evidence, resolvedInputs);
        preserveKeys(prior, evidence, payload.evidence_ids, "RL_EVIDENCE_LOSS", "evidence invalidation");
        for (const id of payload.evidence_ids) if (evidence[id] && evidence[id].freshness !== "stale") throw fail("RL_INVALID_REQUEST", "retained invalidated evidence must be stale");
      }
      break;
    }
    case "record-verify": {
      const bytes = replaceContent(files, payload.report, resolvedInputs);
      const report = parseCompactMarkdown(bytes.toString("utf8"), "compact-verify-v1").record;
      if (report.verification_id !== payload.verification_id) throw fail("RL_INVALID_REQUEST", "Verify report identity differs from the request");
      if (payload.report.path !== `docs/changes/${change.change_id}/verify-report.md`) throw fail("RL_AUTHORITY_BOUNDARY", "Verify must use the stable canonical report path");
      const reportEvidence = [...new Set([...report.evidence_reused, ...report.evidence_rerun])].sort();
      if (JSON.stringify(reportEvidence) !== JSON.stringify([...payload.evidence_ids].sort())) throw fail("RL_INVALID_REQUEST", "Verify report evidence basis differs from the request");
      const finalReviews = Object.values(change.reviews).filter((reference) => {
        const current = parseCompactMarkdown(files[reference.path].toString("utf8"), "compact-review-v1").record;
        return current.target.target_kind === "final-code" && reference.status === "current" && reference.outcome === "approved" && reference.reviewer_authority === "code-review";
      });
      if (finalReviews.length !== 1 || Object.keys(change.remaining_work).length > 0) throw fail("RL_OPERATION_NOT_PERMITTED", "Verify requires one current approved final Code Review and no remaining work");
      validateObservedSubjects([report], files);
      change.readiness = "verified";
      break;
    }
    case "recover":
      throw fail("RL_INVALID_REQUEST", "recover is evaluated by the recovery adapter, not the semantic evaluator");
  }
}

function dependencyIdentity(change, entry, dependency, files) {
  if (dependency.kind === "subject") {
    const subject = entry.subjects[dependency.id];
    if (!subject) return null;
    return files[subject.path] == null ? subject.identity : sha256(files[subject.path]);
  }
  if (dependency.kind === "artifact") return change.artifacts[dependency.id]?.identity ?? null;
  if (dependency.kind === "review") return change.reviews[dependency.id]?.identity ?? null;
  return change.material_decisions[dependency.id]?.identity ?? null;
}

function invalidateDependentEvidence(change, files) {
  for (const path of new Set(Object.values(change.evidence).map((entry) => entry.manifest_path))) {
    if (files[path] == null) continue;
    const manifest = parseCompactYaml(files[path].toString("utf8"), "compact-evidence-v1");
    let changed = false;
    for (const entry of Object.values(manifest.evidence)) {
      if (entry.freshness !== "current") continue;
      const invalid = entry.invalidating_dependencies.find((dependency) => dependencyIdentity(change, entry, dependency, files) !== dependency.identity);
      if (!invalid) continue;
      entry.freshness = "stale";
      entry.required_rerun = `Dependency ${invalid.kind}:${invalid.id} changed`;
      changed = true;
    }
    if (!changed) continue;
    const bytes = Buffer.from(serializeLifecycleYaml(manifest));
    files[path] = bytes;
    for (const entry of Object.values(manifest.evidence)) change.evidence[entry.evidence_id] = { evidence_id: entry.evidence_id, manifest_path: path, manifest_identity: sha256(bytes), freshness: entry.freshness };
  }
}

function finalize(change, files, changePath, operation) {
  invalidateDependentEvidence(change, files);
  if (operation !== "record-verify" && change.readiness === "verified") {
    files[`docs/changes/${change.change_id}/verify-report.md`] = null;
    change.readiness = "not-ready";
  }
  if (operation !== "record-verify") change.readiness = Object.values(change.open_findings).some((finding) => finding.blocking_effect === "blocks-progression") || change.blockers.length > 0 || change.active_work?.kind === "correction" ? "blocked" : "not-ready";
  change.artifacts = sortedObject(change.artifacts);
  change.reviews = sortedObject(change.reviews);
  change.open_findings = sortedObject(change.open_findings);
  change.material_decisions = sortedObject(change.material_decisions);
  change.evidence = sortedObject(change.evidence);
  change.remaining_work = sortedObject(change.remaining_work);
  change.lifecycle_revision = SENTINEL;
  const currentAuthoritative = authoritative(change, files).rest;
  const initial = serializeLifecycleYaml(change);
  change.lifecycle_revision = compactLifecycleRevision({ changeBytes: initial, files: currentAuthoritative }).revision;
  const changeBytes = Buffer.from(serializeLifecycleYaml(change));
  files[changePath] = changeBytes;
  validateCompactSet({ changeBytes: changeBytes.toString("utf8"), files: currentAuthoritative });
}

export function evaluateCompactOperation({ request, currentFiles, resolvedInputs = {} }) {
  validateCompactRecord(request, "compact-operation-v1");
  if (request.operation === "recover") throw fail("RL_INVALID_REQUEST", "recover must use explicit recovery handling");
  const current = parseCurrent(currentFiles, request.change_id);
  if (current.change.lifecycle_revision !== request.expected_lifecycle_revision) throw fail("RL_STALE_OPERATION", "expected lifecycle revision is stale");
  exactPathSet(Object.keys(request.expected_files), requiredInputPaths(current.change, currentFiles, request, resolvedInputs), "expected_files must bind exactly the authoritative, affected, and observed subject paths");
  expectedState(request, currentFiles);
  const eligibility = compactOperationEligibility(current.change, request.operation, request);
  if (eligibility.status !== "permitted") throw fail(eligibility.blockers[0].code, eligibility.blockers[0].summary);
  const files = Object.fromEntries(Object.entries(currentFiles).map(([path, value]) => [path, value === null ? null : Buffer.from(value)]));
  applySemantic(current.change, files, request, resolvedInputs);
  finalize(current.change, files, current.path, request.operation);
  const affectedPaths = Object.keys(files).filter((path) => {
    const prior = currentFiles[path];
    const candidate = files[path];
    return (prior === null ? null : sha256(prior)) !== (candidate === null ? null : sha256(candidate));
  }).sort();
  const candidateFiles = Object.fromEntries(affectedPaths.map((path) => [path, { path, priorBytes: currentFiles[path], priorIdentity: currentFiles[path] === null ? null : sha256(currentFiles[path]), candidateBytes: files[path], candidateIdentity: files[path] === null ? null : sha256(files[path]) }]));
  return { request, requestBytes: Buffer.byteLength(JSON.stringify(request)), changeId: request.change_id, priorLifecycleRevision: request.expected_lifecycle_revision, candidateLifecycleRevision: current.change.lifecycle_revision, currentFiles, candidateSet: files, files: candidateFiles, affectedPaths, change: current.change };
}
