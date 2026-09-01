const IMPACT_SURFACES = new Set(["runtime-behavior", "public-api", "state-or-persistence", "migration", "dependencies", "build", "packaging", "generated-output", "security-or-authority", "documentation", "repository-metadata", "lifecycle-governance", "external-environment"]);
const IMPACT_STATES = new Set(["affected", "unaffected", "unknown"]);
const FRESHNESS_CLASSES = new Set(["always-current", "fresh-required", "impact-sensitive"]);
const EVIDENCE_DECISIONS = new Set(["reuse", "rerun", "newly-required"]);
const VERIFY_OUTCOMES = new Set(["pending", "successful", "failed", "inconclusive", "interrupted", "stale"]);
const EVIDENCE_RESULTS = new Set(["pass", "fail", "blocked", "missing", "conflicting", "unknown"]);
const EXECUTION_KINDS = new Set(["actual-run", "hosted-observation", "reused-pass", "cache-hit", "not-run"]);
const CI_STATUSES = new Set(["passed", "failed", "pending", "unavailable", "not-required"]);
const AUTHORITY_STATUSES = new Set(["current", "stale", "missing", "conflicting", "ambiguous"]);
const ACTUAL_EXECUTIONS = new Set(["actual-run", "hosted-observation"]);
const BASIS_FIELDS = new Set(["repository_identity", "remote_identity", "base_branch", "base_revision", "merge_base_revision", "head_branch", "verified_subject_revision", "governed_change_id", "final_review_id", "design_package_id", "delivery_plan_id", "final_diff_sha256"]);
const BASIS_STATUS_FIELDS = new Set(["repository", "governed_change", "verified_subject", "final_review", "design_package", "delivery_plan", "final_diff"]);
const RESULT_FIELDS = new Set(["protocol_version", "outcome", "basis", "basis_status", "impact", "evidence", "always_current", "ci_status", "blockers", "residual_risks", "branch_ready", "explanation"]);
const EXPLANATION_FIELDS = new Set(["what_changed", "why", "requirements_and_design", "important_choices", "supporting_evidence", "limitations", "residual_risks"]);
const ALWAYS_CURRENT_CHECKS = new Set(["current-change-and-repository-identity", "reviewed-subject-and-review-identity", "lifecycle-and-package-consistency", "review-closeout", "unresolved-blocker-state", "final-diff-classification", "required-artifact-and-evidence-existence", "complete-verify-result-consistency"]);
const REPORT_MARKER = "```json final-verification-v3\n";

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

export function evaluateEvidenceDecision(obligation, impacts) {
  if (!FRESHNESS_CLASSES.has(obligation.freshness)) throw new Error(`freshness: unknown_value ${String(obligation.freshness)}`);
  if (obligation.new_obligation === true) return "newly-required";
  if (obligation.freshness === "always-current" || obligation.freshness === "fresh-required") return "rerun";
  const bySurface = new Map(impacts.map((item) => [item.surface, item]));
  if (!nonEmptyStrings(obligation.proved_surfaces)) return "rerun";
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
    }
  });
  if (Array.isArray(result.always_current)) result.always_current.forEach((item, index) => {
    if (item && typeof item === "object") {
      errors.push(...unknown(`always_current[${index}].check_id`, item.check_id, ALWAYS_CURRENT_CHECKS));
      errors.push(...unknown(`always_current[${index}].execution`, item.execution, EXECUTION_KINDS));
      errors.push(...unknown(`always_current[${index}].observed_result`, item.observed_result, EVIDENCE_RESULTS));
    }
  });
  errors.push(...unknown("ci_status", result.ci_status, CI_STATUSES));
  if (errors.length) return errors;

  if (!sameFields(result, RESULT_FIELDS)) errors.push(`result fields: expected exactly ${JSON.stringify([...RESULT_FIELDS].sort())}`);
  if (containsSelfCommitIdentity(result)) errors.push("result: Verify report must not embed its own Git commit identity");
  if (result.protocol_version !== 3) errors.push(`protocol_version: expected 3, got ${String(result.protocol_version)}`);
  if (!sameFields(result.basis, BASIS_FIELDS)) errors.push(`basis fields: expected exactly ${JSON.stringify([...BASIS_FIELDS].sort())}`);
  else for (const field of [...BASIS_FIELDS].sort()) {
    const scalar = (typeof result.basis[field] === "string" || typeof result.basis[field] === "number") && String(result.basis[field]).trim() !== "";
    if (result.outcome === "successful" && !scalar) errors.push(`basis.${field}: expected exactly one non-empty scalar identity`);
    else if (result.outcome !== "successful" && result.basis[field] !== null && !scalar) errors.push(`basis.${field}: expected one non-empty scalar identity or null`);
  }
  if (!sameFields(result.basis_status, BASIS_STATUS_FIELDS)) errors.push(`basis_status fields: expected exactly ${JSON.stringify([...BASIS_STATUS_FIELDS].sort())}`);

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

  const evidence = Array.isArray(result.evidence) ? result.evidence : [];
  if (result.outcome === "successful" && !evidence.length) errors.push("evidence: expected at least one obligation");
  const evidenceIds = new Set();
  evidence.forEach((item, index) => {
    if (!item || typeof item !== "object") return errors.push(`evidence[${index}]: expected mapping`);
    if (typeof item.evidence_id !== "string" || !item.evidence_id.trim()) errors.push(`evidence[${index}].evidence_id: required`);
    else if (evidenceIds.has(item.evidence_id)) errors.push(`evidence[${index}].evidence_id: duplicate ${item.evidence_id}`);
    evidenceIds.add(item.evidence_id);
    if (!nonEmptyStrings(item.proved_surfaces)) errors.push(`evidence[${index}].proved_surfaces: expected non-empty list`);
    if (typeof item.decision_rationale !== "string" || !item.decision_rationale.trim()) errors.push(`evidence[${index}].decision_rationale: required`);
    const expected = evaluateEvidenceDecision(item, impacts);
    if (item.decision !== expected) errors.push(`evidence[${index}].decision: expected ${expected} from applicability inputs`);
    if ((item.decision === "rerun" || item.decision === "newly-required") && !ACTUAL_EXECUTIONS.has(item.execution)) errors.push(`evidence[${index}].execution: ${item.decision} requires actual-run or hosted-observation`);
    if ((item.freshness === "fresh-required" || item.freshness === "always-current") && !ACTUAL_EXECUTIONS.has(item.execution)) errors.push(`evidence[${index}].execution: ${item.freshness} requires actual-run or hosted-observation`);
    if (item.decision === "reuse" && item.execution !== "reused-pass") errors.push(`evidence[${index}].execution: reuse requires reused-pass`);
    if (item.cache_hit === true && ACTUAL_EXECUTIONS.has(item.execution)) errors.push(`evidence[${index}].cache_hit: cannot represent actual execution`);
  });

  const current = Array.isArray(result.always_current) ? result.always_current : [];
  const currentIds = new Set(current.map((item) => item?.check_id));
  current.forEach((item, index) => {
    if (result.outcome === "successful" && !ACTUAL_EXECUTIONS.has(item?.execution)) errors.push(`always_current[${index}].execution: requires actual-run or hosted-observation`);
    if (result.outcome === "successful" && item?.observed_result !== "pass") errors.push(`always_current[${index}].observed_result: success requires pass`);
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
  if (text.split(REPORT_MARKER).length !== 2) throw new Error("verify report must contain exactly one final-verification-v3 payload");
  const result = JSON.parse(text.split(REPORT_MARKER, 2)[1].split("\n```", 1)[0]);
  const errors = validateFinalVerificationResult(result);
  if (errors.length) throw new Error(`invalid final verification result: ${errors.join("; ")}`);
  return result;
}

export function replayDisposition(previous, candidate) {
  if (JSON.stringify(stableValue(previous)) === JSON.stringify(stableValue(candidate))) return "identical-replay";
  if (JSON.stringify(stableValue(previous.basis)) !== JSON.stringify(stableValue(candidate.basis))) return "changed-basis";
  return "new-attempt";
}

export function tailDisposition(changedPaths, changeId) {
  const allowed = new Set([`docs/changes/${changeId}/verify-report.md`, `docs/changes/${changeId}/change.yaml#validation_events.verify`]);
  return changedPaths.every((path) => allowed.has(path)) ? "current" : "stale";
}
