import { exact, fail, validateType, validate, schemas } from './operational-contract.js';
export const MAINTENANCE_INTERFACE = 'store-maintenance-v1';
const text = value => validateType('text', value);
export function checkedDigest(value) {
  if (typeof value !== 'string' || !/^sha256:[a-f0-9]{64}$(?![\s\S])/.test(value)) fail('invalid-request', 'Expected a tagged SHA-256 observation.');
}
export function validateMaintenance(task, envelope, preview) {
  const schema=schemas['store-maintenance-v1.schema.json'];
  if (!['store.backup','store.restore','store.migrate'].includes(task)) fail('invalid-request','Unsupported maintenance task.');
  validate(schema.$defs[task.split('.')[1]],envelope,schema);
  exact(envelope, ['schema_version','interface','input']);
  if (envelope.schema_version !== 1 || envelope.interface !== MAINTENANCE_INTERFACE) fail('invalid-request', 'Unsupported maintenance request contract.');
  const input = envelope.input;
  if (!input || typeof input !== 'object') fail('invalid-request', 'Missing maintenance input.');
  if (Object.hasOwn(input, 'resume')) {
    exact(input, ['resume','actor','reason']); exact(input.resume, ['operation_id','expected_observation','action']);
    validateType('id', input.resume.operation_id); checkedDigest(input.resume.expected_observation);
    if (!['finish','rollback'].includes(input.resume.action) || preview) fail('invalid-request', 'Resume requires finish or rollback and does not allow dry-run.');
  } else if (task === 'store.backup') {
    exact(input, ['scope','output','actor']); exact(input.scope, ['changes']); text(input.output);
    if (input.scope.changes !== 'all') ids(input.scope.changes);
  } else if (task === 'store.restore') {
    exact(input, ['backup','expected_backup','expected_store','replace','actor','reason']); text(input.backup); checkedDigest(input.expected_backup);
    if (typeof input.replace !== 'boolean') fail('invalid-request', 'Explicit replacement intent is required.');
  } else if (task === 'store.migrate') {
    if (input.mode === 'schema-upgrade') {
      exact(input, ['mode','expected_store','actor','reason','target_schema','backup_output']);
      if (!Number.isSafeInteger(input.target_schema) || input.target_schema < 1) fail('invalid-request', 'Invalid target schema.'); text(input.backup_output);
    } else if (input.mode === 'legacy-import') {
      exact(input, ['mode','expected_store','actor','reason','source_contract','source_root','changes','expected_source','originals_output','dispositions']);
      text(input.source_contract); text(input.source_root); ids(input.changes); text(input.originals_output);
      if (!(preview && input.expected_source === null)) checkedDigest(input.expected_source);
      if (!Array.isArray(input.dispositions) || input.dispositions.length > 64) fail('invalid-request', 'Invalid import dispositions.');
      for (const item of input.dispositions) {
        exact(item, ['source_record','action','reason','target']);text(item.source_record);text(item.reason);
        if (!['import','retain','block'].includes(item.action)) fail('invalid-request', 'Unknown import disposition.');
        if (item.target !== null) {
          exact(item.target, ['change_id','kind','id','parent_id']); validateType('id',item.target.change_id);validateType('id',item.target.id);
          if (!['change','basis','review','evidence','decision','verification','adoption','work','blocker','finding'].includes(item.target.kind)) fail('invalid-request','Unknown import target kind.');
          if (item.target.parent_id !== null) validateType('id',item.target.parent_id);
          if ((item.target.kind === 'finding') !== (item.target.parent_id !== null)) fail('invalid-request','Finding import requires its parent Review.');
        }
      }
    } else fail('invalid-request', 'Unknown migration mode.');
  } else fail('invalid-request', 'Unsupported maintenance task.');
  validateType('actor', input.actor); if (input.reason !== undefined) text(input.reason);
  if (input.expected_store) {
    const e = input.expected_store;
    if (e.kind === 'absent') exact(e,['kind']);
    else if (e.kind === 'current') { exact(e,['kind','revision']);text(e.revision); }
    else if (e.kind === 'unavailable' && task === 'store.restore') { exact(e,['kind','observation']);checkedDigest(e.observation); }
    else fail('invalid-request','Unknown or inapplicable store expectation.');
  }
  return input;
}
function ids(values) {
  if (!Array.isArray(values) || !values.length || values.length > 64 || new Set(values).size !== values.length) fail('invalid-request','Expected 1–64 distinct Change IDs.');
  values.forEach(id=>validateType('id',id));
}
