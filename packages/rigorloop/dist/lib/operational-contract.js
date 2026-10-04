import { readFileSync } from 'node:fs';
import { strictJSON } from './record-json.js';

export const LIMIT = 1024 * 1024;
export const ISSUE_DISPOSITION_LIMIT = 16 * 1024;
export const CONTRACT = 'rigorloop-records-v4';
export const INTERFACE = 'targeted-recording-v2';
export const encodedSize = value => Buffer.byteLength(JSON.stringify(value) + '\n');
export const schemas = Object.fromEntries(['rigorloop-records-v4.schema.json', 'targeted-recording-v2.schema.json', 'store-maintenance-v1.schema.json'].map(name => [name, JSON.parse(readFileSync(new URL('../schemas/' + name, import.meta.url), 'utf8'))]));

export function fail(code, message) {
  throw Object.assign(new Error(message), { operationalCode: code });
}
export function exact(value, required, optional = []) {
  if (!value || typeof value !== 'object' || Array.isArray(value) || required.some(k => !Object.hasOwn(value, k)) || Object.keys(value).some(k => !required.includes(k) && !optional.includes(k))) {
    fail('invalid-request', 'Object fields do not match the selected contract.');
  }
}
export function canonical(value) {
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  if (value && typeof value === 'object') return '{' + Object.keys(value).sort().map(k => JSON.stringify(k) + ':' + canonical(value[k])).join(',') + '}';
  return JSON.stringify(value);
}

// This interpreter supports the finite schema vocabulary used by the packaged
// operational schemas. Schemas are product inputs, never caller-provided code.
export function validate(schema, value, root = schemas['rigorloop-records-v4.schema.json']) {
  if (schema.$ref) {
    const [file, pointer] = schema.$ref.split('#');
    const owner = file ? schemas[file] : root;
    if (!owner || !pointer?.startsWith('/$defs/')) fail('internal-error', 'Packaged schema reference is unavailable.');
    const target = pointer.slice(1).split('/').reduce((v, key) => v?.[key], owner);
    if (!target) fail('internal-error', 'Packaged schema definition is unavailable.');
    return validate(target, value, owner);
  }
  if (schema.anyOf) {
    for (const option of schema.anyOf) {
      try { validate(option, value, root); return; }
      catch (error) { if (error.operationalCode !== 'invalid-request') throw error; }
    }
    fail('invalid-request', 'Value does not match an admitted variant.');
  }
  if (Object.hasOwn(schema, 'const') && value !== schema.const) fail('invalid-request', 'Unknown contract discriminator.');
  if (schema.enum && !schema.enum.includes(value)) fail('invalid-request', 'Unknown contract value.');
  if (schema.type === 'null' && value !== null) fail('invalid-request', 'Expected null.');
  if (schema.type === 'boolean' && typeof value !== 'boolean') fail('invalid-request', 'Expected boolean.');
  if (schema.type === 'string' && (typeof value !== 'string' || (schema.minLength !== undefined && value.length < schema.minLength) || (schema.maxLength !== undefined && value.length > schema.maxLength) || (schema.pattern && !new RegExp(schema.pattern).test(value)))) fail('invalid-request', 'Invalid string value.');
  if (schema.type === 'integer' && (!Number.isSafeInteger(value) || (schema.minimum !== undefined && value < schema.minimum) || (schema.maximum !== undefined && value > schema.maximum))) fail('invalid-request', 'Invalid integer value.');
  if (schema.type === 'array') {
    if (!Array.isArray(value) || (schema.minItems !== undefined && value.length < schema.minItems) || (schema.maxItems !== undefined && value.length > schema.maxItems)) fail('invalid-request', 'Invalid collection size or type.');
    for (const child of value) validate(schema.items, child, root);
    if (schema.uniqueItems && new Set(value.map(canonical)).size !== value.length) fail('invalid-request', 'Duplicate collection entry.');
  }
  if (schema.type === 'object') {
    exact(value, schema.required, Object.keys(schema.properties).filter(k => !schema.required.includes(k)));
    for (const [key, child] of Object.entries(value)) validate(schema.properties[key], child, root);
  }
}
export function validateType(type, value) { validate(schemas['rigorloop-records-v4.schema.json'].$defs[type], value); }
export function validateTask(type, value) {
  const root = schemas['targeted-recording-v2.schema.json'];
  validate(root.$defs[type], value, root);
}
export function parseInput(bytes) {
  if (bytes.length > LIMIT) fail('size-limit', 'Request exceeds 1 MiB.');
  try { return strictJSON(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
  catch { fail('invalid-request', 'Expected bounded UTF-8 JSON with unique keys.'); }
}
export function createChange(id, input) {
  return {
    schema_version: 4, contract: CONTRACT, change_id: id, ...structuredClone(input),
    workflow_contract: 'requirement-first-v1', requirement_basis: null, design_basis: null, plan: null,
    work: [], blockers: [], reviews: [], attachments: [], active_adoption: null, completion: null, completion_notes: [],
  };
}
export function validateChange(change) {
  validateType('change', change);
  for (const subject of change.plan ? [change.plan] : []) {
    if (subject.state === 'absent' && subject.identity !== null) fail('invalid-request', 'Absent subjects cannot have compared identities.');
  }
}
export function issueReserve(issues) {
  return issues.reduce((bytes, issue) => {
    const current = Buffer.byteLength(JSON.stringify(issue.disposition));
    if (current > ISSUE_DISPOSITION_LIMIT) fail('size-limit', 'Issue disposition exceeds 16 KiB.');
    return bytes + ISSUE_DISPOSITION_LIMIT - current + Math.max(0, 'withdrawn'.length - issue.state.length);
  }, 0);
}
export function result(operation, status, fields = {}) {
  return { schema_version: 4, interface: INTERFACE, operation, status, claim: 'storage-only', errors: [], observations: [], items: [], changed: { count: 0, entries: [], omitted: 0 }, committed: false, ...fields };
}
export function exitCode(output) {
  return { ok: 0, saved: 0, unchanged: 0, preview: 0, rejected: 2, conflict: 3, busy: 4, 'recovery-needed': 5, failed: 1 }[output.status] ?? 1;
}
export function failure(operation, error, scope = {}) {
  const code = error.operationalCode ?? 'internal-error';
  const status = ['revision-conflict', 'source-conflict', 'destination-conflict'].includes(code) ? 'conflict'
    : code === 'store-busy' ? 'busy' : ['store-unavailable', 'maintenance-required'].includes(code) ? 'recovery-needed'
      : ['write-failed', 'output-failed', 'internal-error'].includes(code) ? 'failed' : 'rejected';
  return result(operation, status, { ...scope, errors: [{ code, message: error.operationalCode ? error.message : 'Operational request could not be completed.' }], committed: Object.hasOwn(error, 'committed') ? error.committed : false });
}
