const IMPACT_SURFACES = new Set(["runtime-behavior", "public-api", "state-or-persistence", "migration", "dependencies", "build", "packaging", "generated-output", "security-or-authority", "documentation", "repository-metadata", "lifecycle-governance", "external-environment"]);
const IMPACT_STATES = new Set(["affected", "unaffected", "unknown"]);
const FRESHNESS_CLASSES = new Set(["always-current", "fresh-required", "impact-sensitive"]);
const EVIDENCE_DECISIONS = new Set(["reuse", "rerun", "newly-required"]);
const VERIFY_OUTCOMES = new Set(["pending", "successful", "failed", "inconclusive", "interrupted", "stale"]);
const EVIDENCE_RESULTS = new Set(["pass", "fail", "blocked", "missing", "conflicting", "unknown"]);
const EXECUTION_KINDS = new Set(["actual-run", "hosted-observation", "reused-pass", "cache-hit", "not-run"]);
const CI_STATUSES = new Set(["passed", "failed", "pending", "unavailable", "not-required"]);
const AUTHORITY_STATUSES = new Set(["current", "stale", "missing", "conflicting", "ambiguous"]);
const PROOF_KINDS = new Set(["command", "hosted", "prior-evidence", "cache"]);
const ACTUAL_EXECUTIONS = new Set(["actual-run", "hosted-observation"]);
const BASIS_FIELDS = new Set(["repository_identity", "remote_identity", "base_branch", "base_revision", "merge_base_revision", "head_branch", "verified_subject_revision", "governed_change_id", "final_review_id", "design_package_id", "delivery_plan_id", "final_diff_sha256"]);
const BASIS_STATUS_FIELDS = new Set(["repository", "governed_change", "verified_subject", "final_review", "design_package", "delivery_plan", "final_diff"]);
const RESULT_FIELDS = new Set(["protocol_version", "outcome", "basis", "basis_status", "impact", "evidence", "always_current", "ci_status", "blockers", "residual_risks", "branch_ready", "explanation"]);
const EXPLANATION_FIELDS = new Set(["what_changed", "why", "requirements_and_design", "important_choices", "supporting_evidence", "limitations", "residual_risks"]);
const ALWAYS_CURRENT_CHECKS = new Set(["current-change-and-repository-identity", "reviewed-subject-and-review-identity", "lifecycle-and-package-consistency", "review-closeout", "unresolved-blocker-state", "final-diff-classification", "required-artifact-and-evidence-existence", "complete-verify-result-consistency"]);
const REPORT_MARKER = "```json final-verification-v3\n";
const REPORT_PREFIX = `# Verify report\n\n${REPORT_MARKER}`;
const REPORT_SUFFIX = "\n```\n";
const SAFE_ID = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;
const REVISION = /^(?:[0-9a-f]{40}|[0-9a-f]{64})$/;
const DIGEST = /^sha256:[0-9a-f]{64}$/;
const REPOSITORY_ID = /^repo:sha256:[0-9a-f]{64}$/;
const REMOTE_ID = /^remote:sha256:[0-9a-f]{64}$/;
const BRANCH = /^(?:[A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._/-]*[A-Za-z0-9])$/;
const EVIDENCE_FIELDS = new Set(["evidence_id", "proved_surfaces", "freshness", "existing_result", "authority_current", "identity_current", "environment_current", "conflicting", "new_obligation", "decision", "decision_rationale", "execution", "observed_result", "cache_hit", "proof"]);
const ALWAYS_CURRENT_FIELDS = new Set(["check_id", "execution", "observed_result", "proof"]);
const APPLICABILITY_BOOLEAN_FIELDS = ["authority_current", "identity_current", "environment_current", "conflicting", "new_obligation"];
const EVIDENCE_BOOLEAN_FIELDS = [...APPLICABILITY_BOOLEAN_FIELDS, "cache_hit"];

function sameFields(value, fields) {
  return value && !Array.isArray(value) && typeof value === "object"
    && Object.keys(value).length === fields.size
    && Object.keys(value).every((key) => fields.has(key));
}

function nonEmptyStrings(value) {
  return Array.isArray(value) && value.length > 0 && value.every((item) => typeof item === "string" && item.trim());
}

function unknown(prefix, value, vocabulary) {
  return vocabulary.has(value) ? [] : [`${prefix}: unknown_value ${String(value)}`];
}

function containsSelfCommitIdentity(value) {
  if (Array.isArray(value)) return value.some(containsSelfCommitIdentity);
  if (!value || typeof value !== "object") return false;
  return Object.entries(value).some(([key, item]) => new Set(["report_commit", "report_commit_identity", "verify_report_revision"]).has(key) || containsSelfCommitIdentity(item));
}

function stableValue(value) {
  if (Array.isArray(value)) return value.map(stableValue);
  if (!value || typeof value !== "object") return value;
  return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stableValue(value[key])]));
}

function nonEmptyExplanationValue(value) {
  if (typeof value === "string") return value.trim() !== "";
  return nonEmptyStrings(value);
}

function repositoryPath(value, suffix = null) {
  if (typeof value !== "string" || !value || value.startsWith("/") || value.includes("\\")) return false;
  const parts = value.split("/");
  if (parts.some((part) => !part || part === "." || part === "..")) return false;
  return suffix === null || value.endsWith(suffix);
}

function branch(value) {
  return typeof value === "string" && BRANCH.test(value) && !value.includes("..") && !value.includes("//") && !value.includes("@{") && !value.endsWith(".lock");
}

function validBasisIdentity(field, value) {
  if (field === "repository_identity") return typeof value === "string" && REPOSITORY_ID.test(value);
  if (field === "remote_identity") return typeof value === "string" && REMOTE_ID.test(value);
  if (["base_revision", "merge_base_revision", "verified_subject_revision"].includes(field)) return typeof value === "string" && REVISION.test(value);
  if (["base_branch", "head_branch"].includes(field)) return branch(value);
  if (["governed_change_id", "final_review_id", "design_package_id"].includes(field)) return typeof value === "string" && SAFE_ID.test(value);
  if (field === "delivery_plan_id") return repositoryPath(value, ".md") && value.startsWith("docs/plans/");
  if (field === "final_diff_sha256") return typeof value === "string" && DIGEST.test(value);
  return false;
}

function validateProof(proof, execution, prefix) {
  if (execution === "not-run" && proof === null) return [];
  if (!proof || Array.isArray(proof) || typeof proof !== "object") return [`${prefix}.proof: required mapping for ${String(execution)}`];
  let errors = unknown(`${prefix}.proof.kind`, proof.kind, PROOF_KINDS);
  if (errors.length) return errors;
  const expectedKind = { "actual-run": "command", "hosted-observation": "hosted", "reused-pass": "prior-evidence", "cache-hit": "cache" }[execution];
  if (!expectedKind) return [`${prefix}.proof: execution ${String(execution)} must not carry readiness proof`];
  if (proof.kind !== expectedKind) return [`${prefix}.proof.kind: expected ${expectedKind} for ${execution}`];
  const shapes = {
    command: new Set(["kind", "command", "evidence_path", "evidence_sha256"]),
    hosted: new Set(["kind", "provider", "run_id", "check_name", "subject_revision", "evidence_path", "evidence_sha256"]),
    "prior-evidence": new Set(["kind", "evidence_path", "evidence_sha256", "subject_revision"]),
    cache: new Set(["kind", "cache_key"]),
  };
  if (!sameFields(proof, shapes[proof.kind])) return [`${prefix}.proof: invalid ${proof.kind} proof fields`];
  if (proof.kind === "command" && !nonEmptyStrings(proof.command)) errors.push(`${prefix}.proof.command: expected exact non-empty argv`);
  if (proof.kind === "hosted") for (const field of ["provider", "run_id", "check_name"]) {
    if (typeof proof[field] !== "string" || !proof[field].trim()) errors.push(`${prefix}.proof.${field}: required`);
  }
  if (["hosted", "prior-evidence"].includes(proof.kind) && (typeof proof.subject_revision !== "string" || !REVISION.test(proof.subject_revision))) errors.push(`${prefix}.proof.subject_revision: expected immutable Git revision`);
  if (["command", "hosted", "prior-evidence"].includes(proof.kind)) {
    if (!repositoryPath(proof.evidence_path)) errors.push(`${prefix}.proof.evidence_path: expected normalized repository-relative path`);
    if (typeof proof.evidence_sha256 !== "string" || !DIGEST.test(proof.evidence_sha256)) errors.push(`${prefix}.proof.evidence_sha256: expected sha256 identity`);
  }
  if (proof.kind === "cache" && (typeof proof.cache_key !== "string" || !DIGEST.test(proof.cache_key))) errors.push(`${prefix}.proof.cache_key: expected sha256 identity`);
  return errors;
}

export function evaluateEvidenceDecision(obligation, impacts) {
  if (!nonEmptyStrings(obligation.proved_surfaces)) throw new Error("proved_surfaces: expected non-empty closed surface list");
  if (new Set(obligation.proved_surfaces).size !== obligation.proved_surfaces.length) throw new Error("proved_surfaces: duplicate surface");
  const bySurface = new Map(impacts.map((item) => [item.surface, item]));
  for (const surface of obligation.proved_surfaces) {
    if (!IMPACT_SURFACES.has(surface)) throw new Error(`proved_surfaces: unknown_value ${String(surface)}`);
    if (!bySurface.has(surface)) throw new Error(`proved_surfaces: unclassified ${String(surface)}`);
  }
  if (!FRESHNESS_CLASSES.has(obligation.freshness)) throw new Error(`freshness: unknown_value ${String(obligation.freshness)}`);
  for (const field of APPLICABILITY_BOOLEAN_FIELDS) {
    if (typeof obligation[field] !== "boolean") throw new Error(`${field}: expected boolean`);
  }
  if (obligation.new_obligation === true) return "newly-required";
  if (obligation.freshness === "always-current" || obligation.freshness === "fresh-required") return "rerun";
  const relevant = obligation.proved_surfaces.map((surface) => bySurface.get(surface));
  if (relevant.some((item) => !item || item.state !== "unaffected" || !nonEmptyStrings(item.affirmative_evidence))) return "rerun";
  if (obligation.existing_result !== "pass" || obligation.authority_current !== true || obligation.identity_current !== true) return "rerun";
  if (obligation.environment_current !== true || obligation.conflicting !== false) return "rerun";
  return "reuse";
}

export function validateFinalVerificationResult(result) {
  if (!result || Array.isArray(result) || typeof result !== "object") return ["result: expected mapping"];
  let errors = unknown("outcome", result.outcome, VERIFY_OUTCOMES);
  if (result.basis_status && typeof result.basis_status === "object") {
    for (const [field, status] of Object.entries(result.basis_status)) errors.push(...unknown(`basis_status.${field}`, status, AUTHORITY_STATUSES));
  }
  if (Array.isArray(result.impact)) result.impact.forEach((item, index) => {
    if (item && typeof item === "object") {
      errors.push(...unknown(`impact[${index}].surface`, item.surface, IMPACT_SURFACES));
      errors.push(...unknown(`impact[${index}].state`, item.state, IMPACT_STATES));
    }
  });
  if (Array.isArray(result.evidence)) result.evidence.forEach((item, index) => {
    if (item && typeof item === "object") {
      errors.push(...unknown(`evidence[${index}].freshness`, item.freshness, FRESHNESS_CLASSES));
      errors.push(...unknown(`evidence[${index}].decision`, item.decision, EVIDENCE_DECISIONS));
      errors.push(...unknown(`evidence[${index}].existing_result`, item.existing_result, EVIDENCE_RESULTS));
      errors.push(...unknown(`evidence[${index}].observed_result`, item.observed_result, EVIDENCE_RESULTS));
      errors.push(...unknown(`evidence[${index}].execution`, item.execution, EXECUTION_KINDS));
      if (Array.isArray(item.proved_surfaces)) item.proved_surfaces.forEach((surface, surfaceIndex) => errors.push(...unknown(`evidence[${index}].proved_surfaces[${surfaceIndex}]`, surface, IMPACT_SURFACES)));
      if (item.proof && typeof item.proof === "object") errors.push(...unknown(`evidence[${index}].proof.kind`, item.proof.kind, PROOF_KINDS));
    }
  });
  if (Array.isArray(result.always_current)) result.always_current.forEach((item, index) => {
    if (item && typeof item === "object") {
      errors.push(...unknown(`always_current[${index}].check_id`, item.check_id, ALWAYS_CURRENT_CHECKS));
      errors.push(...unknown(`always_current[${index}].execution`, item.execution, EXECUTION_KINDS));
      errors.push(...unknown(`always_current[${index}].observed_result`, item.observed_result, EVIDENCE_RESULTS));
      if (item.proof && typeof item.proof === "object") errors.push(...unknown(`always_current[${index}].proof.kind`, item.proof.kind, PROOF_KINDS));
    }
  });
  errors.push(...unknown("ci_status", result.ci_status, CI_STATUSES));
  if (errors.length) return errors;

  if (!sameFields(result, RESULT_FIELDS)) errors.push(`result fields: expected exactly ${JSON.stringify([...RESULT_FIELDS].sort())}`);
  if (containsSelfCommitIdentity(result)) errors.push("result: Verify report must not embed its own Git commit identity");
  if (result.protocol_version !== 3) errors.push(`protocol_version: expected 3, got ${String(result.protocol_version)}`);
  if (!sameFields(result.basis, BASIS_FIELDS)) errors.push(`basis fields: expected exactly ${JSON.stringify([...BASIS_FIELDS].sort())}`);
  else for (const field of [...BASIS_FIELDS].sort()) {
    if (result.outcome === "successful" && !validBasisIdentity(field, result.basis[field])) errors.push(`basis.${field}: invalid canonical identity`);
    else if (result.outcome !== "successful" && result.basis[field] !== null && !validBasisIdentity(field, result.basis[field])) errors.push(`basis.${field}: expected canonical identity or null`);
  }
  if (!sameFields(result.basis_status, BASIS_STATUS_FIELDS)) errors.push(`basis_status fields: expected exactly ${JSON.stringify([...BASIS_STATUS_FIELDS].sort())}`);

  if (!Array.isArray(result.impact)) errors.push("impact: expected array");
  const impacts = Array.isArray(result.impact) ? result.impact : [];
  if (result.outcome === "successful" && !impacts.length) errors.push("impact: expected at least one classified surface");
  const surfaces = new Set();
  impacts.forEach((item, index) => {
    if (!item || typeof item !== "object") return errors.push(`impact[${index}]: expected mapping`);
    if (surfaces.has(item.surface)) errors.push(`impact[${index}].surface: duplicate ${String(item.surface)}`);
    surfaces.add(item.surface);
    if (typeof item.rationale !== "string" || !item.rationale.trim()) errors.push(`impact[${index}].rationale: required`);
    if (item.state === "unaffected" && !nonEmptyStrings(item.affirmative_evidence)) errors.push(`impact[${index}].unaffected: affirmative_evidence required`);
  });

  if (!Array.isArray(result.evidence)) errors.push("evidence: expected array");
  const evidence = Array.isArray(result.evidence) ? result.evidence : [];
  if (result.outcome === "successful" && !evidence.length) errors.push("evidence: expected at least one obligation");
  const evidenceIds = new Set();
  evidence.forEach((item, index) => {
    if (!item || typeof item !== "object") return errors.push(`evidence[${index}]: expected mapping`);
    if (!sameFields(item, EVIDENCE_FIELDS)) errors.push(`evidence[${index}] fields: expected closed evidence entry`);
    if (typeof item.evidence_id !== "string" || !SAFE_ID.test(item.evidence_id)) errors.push(`evidence[${index}].evidence_id: expected safe identifier`);
    else if (evidenceIds.has(item.evidence_id)) errors.push(`evidence[${index}].evidence_id: duplicate ${item.evidence_id}`);
    evidenceIds.add(item.evidence_id);
    if (!nonEmptyStrings(item.proved_surfaces)) errors.push(`evidence[${index}].proved_surfaces: expected non-empty list`);
    const proved = new Set();
    for (const [surfaceIndex, surface] of (Array.isArray(item.proved_surfaces) ? item.proved_surfaces : []).entries()) {
      if (proved.has(surface)) errors.push(`evidence[${index}].proved_surfaces: duplicate ${String(surface)}`);
      proved.add(surface);
      if (!surfaces.has(surface)) errors.push(`evidence[${index}].proved_surfaces[${surfaceIndex}]: unclassified ${String(surface)}`);
    }
    if (typeof item.decision_rationale !== "string" || !item.decision_rationale.trim()) errors.push(`evidence[${index}].decision_rationale: required`);
    let invalidBoolean = false;
    for (const field of EVIDENCE_BOOLEAN_FIELDS) {
      if (typeof item[field] !== "boolean") {
        errors.push(`evidence[${index}].${field}: expected boolean`);
        invalidBoolean = true;
      }
    }
    if (invalidBoolean) return;
    try {
      const expected = evaluateEvidenceDecision(item, impacts);
      if (item.decision !== expected) errors.push(`evidence[${index}].decision: expected ${expected} from applicability inputs`);
    } catch (error) {
      errors.push(`evidence[${index}].${error.message}`);
    }
    if ((item.decision === "rerun" || item.decision === "newly-required") && !ACTUAL_EXECUTIONS.has(item.execution)) errors.push(`evidence[${index}].execution: ${item.decision} requires actual-run or hosted-observation`);
    if ((item.freshness === "fresh-required" || item.freshness === "always-current") && !ACTUAL_EXECUTIONS.has(item.execution)) errors.push(`evidence[${index}].execution: ${item.freshness} requires actual-run or hosted-observation`);
    if (item.decision === "reuse" && item.execution !== "reused-pass") errors.push(`evidence[${index}].execution: reuse requires reused-pass`);
    if (item.cache_hit === true && ACTUAL_EXECUTIONS.has(item.execution)) errors.push(`evidence[${index}].cache_hit: cannot represent actual execution`);
    errors.push(...validateProof(item.proof, item.execution, `evidence[${index}]`));
  });

  if (!Array.isArray(result.always_current)) errors.push("always_current: expected array");
  const current = Array.isArray(result.always_current) ? result.always_current : [];
  const currentIds = new Set();
  current.forEach((item, index) => {
    if (!sameFields(item, ALWAYS_CURRENT_FIELDS)) errors.push(`always_current[${index}] fields: expected closed always-current entry`);
    if (currentIds.has(item?.check_id)) errors.push(`always_current[${index}].check_id: duplicate ${String(item?.check_id)}`);
    currentIds.add(item?.check_id);
    if (result.outcome === "successful" && !ACTUAL_EXECUTIONS.has(item?.execution)) errors.push(`always_current[${index}].execution: requires actual-run or hosted-observation`);
    if (result.outcome === "successful" && item?.observed_result !== "pass") errors.push(`always_current[${index}].observed_result: success requires pass`);
    errors.push(...validateProof(item?.proof, item?.execution, `always_current[${index}]`));
  });
  if (result.outcome === "successful" && (currentIds.size !== ALWAYS_CURRENT_CHECKS.size || [...currentIds].some((id) => !ALWAYS_CURRENT_CHECKS.has(id)))) errors.push(`always_current check_ids: expected exactly ${JSON.stringify([...ALWAYS_CURRENT_CHECKS].sort())}`);

  if (result.outcome === "successful") {
    if (Object.values(result.basis_status ?? {}).some((status) => status !== "current")) errors.push("successful result requires every basis authority current");
    if (result.branch_ready !== true) errors.push("successful result requires branch_ready true");
    if (!Array.isArray(result.blockers) || result.blockers.length) errors.push("successful result requires no blockers");
    if (result.ci_status !== "passed" && result.ci_status !== "not-required") errors.push("successful result requires CI passed or not-required");
    if (!sameFields(result.explanation, EXPLANATION_FIELDS)) errors.push(`successful result explanation fields: expected exactly ${JSON.stringify([...EXPLANATION_FIELDS].sort())}`);
    else if (Object.values(result.explanation).some((value) => !nonEmptyExplanationValue(value))) errors.push("successful result explanation fields must be non-empty");
    evidence.forEach((item, index) => { if (item?.observed_result !== "pass") errors.push(`evidence[${index}].observed_result: success requires pass`); });
  } else {
    if (result.branch_ready !== false) errors.push(`${result.outcome} result must set branch_ready false`);
    if (result.explanation !== null) errors.push(`${result.outcome} result must omit explanation`);
    if (!nonEmptyStrings(result.blockers)) errors.push(`${result.outcome} result must record blockers`);
  }
  return errors;
}

export function renderVerifyReport(result) {
  const errors = validateFinalVerificationResult(result);
  if (errors.length) throw new Error(`invalid final verification result: ${errors.join("; ")}`);
  return `# Verify report\n\n${REPORT_MARKER}${JSON.stringify(stableValue(result), null, 2)}\n\`\`\`\n`;
}

export function parseVerifyReport(text) {
  if (!text.startsWith(REPORT_PREFIX) || !text.endsWith(REPORT_SUFFIX) || text.split(REPORT_MARKER).length !== 2) throw new Error("verify report has trailing or malformed content");
  const result = JSON.parse(text.slice(REPORT_PREFIX.length, -REPORT_SUFFIX.length));
  const errors = validateFinalVerificationResult(result);
  if (errors.length) throw new Error(`invalid final verification result: ${errors.join("; ")}`);
  return result;
}

export function replayDisposition(previous, candidate) {
  if (JSON.stringify(stableValue(previous)) === JSON.stringify(stableValue(candidate))) return "identical-replay";
  if (JSON.stringify(stableValue(previous.basis)) !== JSON.stringify(stableValue(candidate.basis))) return "changed-basis";
  return "new-attempt";
}

export function tailDisposition(tail, changeId, verifiedSubjectRevision) {
  if (!tail || Array.isArray(tail) || typeof tail !== "object") return "incomplete";
  const reportPath = `docs/changes/${changeId}/verify-report.md`;
  const selector = "lifecycle_cli.validations.verify-result";
  const changeField = `docs/changes/${changeId}/change.yaml#${selector}`;
  const allowed = new Set([reportPath, changeField]);
  if (!Array.isArray(tail.changed_paths) || tail.changed_paths.length !== 2 || new Set(tail.changed_paths).size !== 2 || tail.changed_paths.some((path) => !allowed.has(path))) {
    return Array.isArray(tail.changed_paths) && tail.changed_paths.some((path) => !allowed.has(path)) ? "stale" : "incomplete";
  }
  if (tail.report_path !== reportPath || typeof tail.report_content !== "string") return "incomplete";
  const reportIdentity = `sha256:${createHash("sha256").update(tail.report_content).digest("hex")}`;
  if (tail.report_sha256 !== reportIdentity) return "incomplete";
  let report;
  try { report = parseVerifyReport(tail.report_content); } catch { return "incomplete"; }
  const expectedRegistration = { selector, evidence_path: reportPath, evidence_sha256: reportIdentity, verified_subject_revision: verifiedSubjectRevision, stage_authority: "verify" };
  if (JSON.stringify(stableValue(tail.registration)) !== JSON.stringify(stableValue(expectedRegistration))) return "incomplete";
  if (report.basis?.verified_subject_revision !== verifiedSubjectRevision || report.outcome !== "successful" || report.branch_ready !== true) return "incomplete";
  return "current";
}

function verifiedAuthoritativeReferences(result, reportPath) {
  const references = new Set([reportPath, result.basis.delivery_plan_id]);
  for (const item of [...result.evidence, ...result.always_current]) {
    if (item.proof && typeof item.proof.evidence_path === "string") references.add(item.proof.evidence_path);
  }
  return [...references].sort();
}

export function evaluatePrHandoff({ tail, change_id, verified_subject_revision, current_basis, explanation, authoritative_references }) {
  if (tailDisposition(tail, change_id, verified_subject_revision) !== "current") return { ready: false, reason: "verify-result-not-current" };
  let result;
  try { result = parseVerifyReport(tail.report_content); } catch { return { ready: false, reason: "verify-result-incomplete" }; }
  if (JSON.stringify(stableValue(current_basis)) !== JSON.stringify(stableValue(result.basis))) return { ready: false, reason: "verify-basis-mismatch" };
  if (JSON.stringify(stableValue(explanation)) !== JSON.stringify(stableValue(result.explanation))) return { ready: false, reason: "competing-rationale" };
  const expectedReferences = verifiedAuthoritativeReferences(result, tail.report_path);
  if (!Array.isArray(authoritative_references) || new Set(authoritative_references).size !== authoritative_references.length || JSON.stringify([...authoritative_references].sort()) !== JSON.stringify(expectedReferences)) {
    return { ready: false, reason: "authoritative-reference-mismatch" };
  }
  return { ready: true, reason: "current-successful-verify-result", explanation: result.explanation, basis: result.basis };
}
import { createHash } from "node:crypto";
