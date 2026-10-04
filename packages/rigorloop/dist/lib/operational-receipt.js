// MOD-010's pure codec: storage can establish receipt readiness without
// acquiring a renderer, filesystem capability or callback from the caller.
import { LIMIT, fail, result } from './operational-contract.js';

export function publicResult(operation, changeId, outcome) {
  const identity = outcome.identity;
  const output = result(operation, outcome.status, {
    ...(changeId ? { change_id: changeId } : {}),
    ...(identity.record_contract ? { record_contract: identity.record_contract } : {}),
    ...(outcome.kind==='maintenance'?{interface:'store-maintenance-v1',maintenance:outcome.maintenance}:{}),
    ...(identity.store_revision?{store_revision:identity.store_revision}:{}),
    ...(identity.change_revision ? { revision: identity.change_revision } : {}),
    committed: outcome.committed,
    errors: outcome.status === 'ok' || ['saved', 'preview', 'unchanged'].includes(outcome.status) ? [] : outcome.diagnostics,
    observations: ['ok','saved','preview','unchanged'].includes(outcome.status) ? outcome.diagnostics : [],
    changed: outcome.kind === 'read' ? { count: 0, entries: [], omitted: 0 } : outcome.changed,
    items: [...(outcome.records ?? [])],
  });
  for (const projection of outcome.projections ?? []) {
    if (projection.query_kind === 'selector-index') output.available_selectors = projection.value;
    else output.items.push({ kind: projection.query_kind, id: changeId, value: projection.value });
  }
  return output;
}

export function encodeReceipt(operation, changeId, outcome, profile) {
  if (!['record-json-v1', 'record-text-v1', 'maintenance-json-v1', 'maintenance-text-v1'].includes(profile)) fail('invalid-request', 'Unknown receipt profile.');
  const output = publicResult(operation, changeId, outcome);
  // Both profiles preserve complete content and explicit gaps. Text may evolve
  // independently without allowing storage to choose another result contract.
  const bytes = JSON.stringify(output) + '\n';
  if (Buffer.byteLength(bytes) > LIMIT) fail('size-limit', 'Selected result exceeds 1 MiB.');
  return bytes;
}
