import { readFileSync } from 'node:fs';
import { strictJSON } from './record-json.js';

// One source is bundled by build-record-store-schema.mjs and included in the
// adapter archive by the packager. It cannot supply arbitrary removal paths.
export const workflowContract = JSON.parse(readFileSync(new URL('../templates/shared/rigorloop-workflow.json', import.meta.url), 'utf8'));
export const workflowMember = 'rigorloop-workflow.json';
export function validateWorkflowDescriptor(bytes) {
  let value;
  try { value = strictJSON(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
  catch { throw new Error('Invalid workflow descriptor JSON.'); }
  if (!value || Object.keys(value).sort().join() !== Object.keys(workflowContract).sort().join() ||
      Object.entries(workflowContract).some(([key, expected]) => JSON.stringify(value[key]) !== JSON.stringify(expected))) {
    throw new Error('Unsupported workflow descriptor fields, versions or profile.');
  }
  return value;
}
