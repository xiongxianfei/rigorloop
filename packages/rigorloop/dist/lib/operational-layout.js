// Typed row mapping. Only explanatory values use JSON; account references,
// subjects, selections and attachment relationships have their own tables.
export const layouts = {
  basis: { table: 'bases', fields: ['kind', 'decision', 'actor:j', 'rationale'] },
  review: { table: 'reviews', fields: ['purpose', 'scope', 'prepared.scope', 'prepared.coverage_rationale', 'prepared.prepared_by:j', 'assessment.reviewer:j?', 'assessment.contributors:j?', 'assessment.independence_basis?', 'assessment.judgment?', 'assessment.summary?', 'assessment.rationale:j?', 'assessment.limitations:j?', 'applicability.value', 'applicability.actor:j', 'applicability.rationale', 'applicability.observation:j'] },
  evidence: { table: 'evidence', fields: ['actor:j', 'reported_at', 'procedure', 'scope', 'observation:j', 'result', 'summary', 'limitations:j'] },
  decision: { table: 'decisions', fields: ['actor:j', 'scope', 'decision', 'rationale'] },
  verification: { table: 'verifications', fields: ['scope', 'verifier:j', 'observation:j', 'outcome', 'summary', 'rationale:j', 'limitations:j', 'support_state'] },
  adoption: { table: 'adoptions', fields: ['actor:j', 'source_contract', 'target_workflow', 'source_basis', 'compatibility', 'disposition', 'phase', 'rationale'] },
  work: { table: 'work', fields: ['status', 'owner:j', 'scope', 'locations:j', 'remaining?', 'completion_reason?'] },
};
export const fieldSpec = field => {
  const path = field.replace(/\?$/, '').split(':')[0];
  return { path, column: path.replaceAll('.', '_') === 'kind' ? 'basis_kind' : path.replaceAll('.', '_'), json: field.includes(':j'), nullable: field.endsWith('?') };
};
export const referenceFields = {
  basis: ['review'], review: ['prepared.basis_refs', 'assessment.evidence_refs'],
  decision: ['source_refs'], verification: ['review_refs', 'evidence_refs'], work: ['check_refs'],
};
export const subjectFields = {
  basis: ['subjects'], review: ['prepared.subjects', 'prepared.plan', 'assessment.assessed_subjects', 'assessment.governing_basis'],
  evidence: ['subjects'], verification: ['subjects', 'governing_basis'],
};
export function getField(object, path) { return path.split('.').reduce((v, k) => v?.[k], object); }
export function setField(object, path, value) {
  const parts = path.split('.'), key = parts.pop();
  let target = object;
  for (const part of parts) target = target[part] ??= {};
  target[key] = value;
}
