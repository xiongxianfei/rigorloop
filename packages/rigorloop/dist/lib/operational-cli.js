import { createHash } from 'node:crypto';
import { executeMaintenance, inspectStore } from './operational-maintenance.js';
import { validateMaintenance } from './operational-maintenance-contract.js';
import { readSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { LIMIT, CONTRACT, INTERFACE, fail, failure, parseInput, validateTask, validateType, exitCode } from './operational-contract.js';
import { executeRecordTask, previewRecordTask, inspectRecords } from './operational-store.js';
import { publicResult, encodeReceipt } from './operational-receipt.js';

const mutationSchemas = {'change.create':'create','change.update':'update','change.complete':'complete','review.prepare':'prepare','review.record':'review','verification.record':'verification'};
const operations = new Set([...Object.keys(mutationSchemas),'change.context','review.show','verification.show','store.backup','store.restore','store.migrate']);
export const operationalFamilies = new Set(['change', 'review', 'verification', 'store', 'capabilities']);

function stdin() {
  const chunks = []; let total = 0;
  for (;;) {
    const chunk = Buffer.alloc(Math.min(65536, LIMIT + 1 - total));
    const count = readSync(0, chunk, 0, chunk.length, null);
    if (!count) break;
    total += count;
    if (total > LIMIT) fail('size-limit', 'Request exceeds 1 MiB.');
    chunks.push(chunk.subarray(0, count));
  }
  return Buffer.concat(chunks);
}

export async function executeOperationalCli(args) {
  let operation = null, changeId;
  try {
    const candidate = args[0] === 'capabilities' ? 'capabilities' : args.slice(0, 2).join('.');
    if (operations.has(candidate) || candidate === 'capabilities') operation = candidate;
    if (args.includes('--help') || args.includes('-h')) {
      if (args.length > 3 || !operationalFamilies.has(args[0]) || (args.length === 3 && !operation)) fail('invalid-request', 'Unknown help target.');
      const schemaName=operation?.startsWith('store.')?'store-maintenance-v1.schema.json':'targeted-recording-v2.schema.json';
      const definition=operation?.startsWith('store.')?operation.split('.')[1]:mutationSchemas[operation]??(operation==='change.context'?'query':null);
      const schemaPath=fileURLToPath(new URL('../schemas/'+schemaName,import.meta.url));
      const envelope=operation?.startsWith('store.')?'{"schema_version":1,"interface":"store-maintenance-v1","input":{...}}':'{"schema_version":2,"interface":"targeted-recording-v2","contract":"rigorloop-records-v4","change_id":"ID","expected_revision":null,"reads":[],"input":{...}}';
      return { exitCode: 0, output: `RigorLoop ${INTERFACE} / ${CONTRACT}\n${[...operations].sort().map(name=>name.replace('.', ' ')).join('\n')}\ncapabilities --root PATH [--format text|json]\n\nAll tasks require --root PATH. Record tasks require --change ID.\nMutations use --input -; ordinary mutations accept --dry-run, explicit maintenance resume does not. Reads do not mutate records.\nReview tasks require a Review ID; verification record requires a Verification ID.\nStore tasks never accept --change. IDs are Change-local.\n${definition?`Request schema: ${schemaPath}#/$defs/${definition}\n${operation==='change.context'?'Optional selector input; use the query definition.':`Envelope: ${envelope}\nCreation expects null revision; record updates copy the revision from the selected current context. Store replacement supplies an explicit expected_store observation.`}\n`:''}Task input fields and closed variants are in the packaged schemas. See the package README for maintenance capture, preview and explicit recovery examples.\n` };

    }
    if (!operation) fail('invalid-request', 'Unsupported operational task in this executable.');
    const maintenance=operation.startsWith('store.'),capability=operation==='capabilities';
    let itemId=null,start=capability?1:2;
    if(!capability&&args[2]&&!args[2].startsWith('--')){itemId=args[2];start=3;validateType('id',itemId);}
    if((operation.startsWith('change.')||maintenance)&&itemId!==null||operation.startsWith('review.')&&itemId===null||operation==='verification.record'&&itemId===null)fail('invalid-request','Item scope does not match the selected task.');
    const reading=!maintenance&&!Object.hasOwn(mutationSchemas,operation);
    const flags = {};
    for (let i = start; i < args.length; i++) {
      const key = args[i];
      if (!['--root', '--change', '--input', '--format', '--dry-run'].includes(key) || Object.hasOwn(flags, key)) fail('invalid-request', 'Unknown or duplicate option.');
      if (key === '--dry-run') flags[key] = true;
      else {
        const value = args[++i];
        if (value === undefined || value.startsWith('--')) fail('invalid-request', 'Missing option value.');
        flags[key] = value;
      }
    }
    if (!flags['--root'] || (!maintenance&&!capability&&!flags['--change'])) fail('invalid-request', 'Explicit project root and Change are required.');
    if(maintenance||capability){if(flags['--change'])fail('invalid-request','This project-level task does not admit --change.');}
    else{validateType('id', flags['--change']); changeId = flags['--change'];}
    const format = flags['--format'] ?? 'text';
    if (!['text', 'json'].includes(format)) fail('invalid-request', 'Unknown result format.');
    if (Object.hasOwn(flags, '--input') && flags['--input'] !== '-') fail('invalid-request', 'Input must use stdin: --input -.');
    if (reading && flags['--dry-run']) fail('invalid-request', 'Reads do not admit dry-run.');
    if (!reading && !flags['--input']) fail('invalid-request', 'Creation requires --input -.');
    if(reading&&operation!=='change.context'&&flags['--input'])fail('invalid-request','This read does not accept stdin.');
    const root = resolve(flags['--root']);
    if(capability) {
      let store,limitation=null;
      try{store=await inspectStore(root);}catch(error){store={state:'unavailable',revision:null,observation:null,database_schema:null,maintenance:null};limitation=error.operationalCode?error.message:'Store inspection unavailable.';}
      const description={interface:INTERFACE,record_contract:CONTRACT,workflow_contract:'requirement-first-v1',operations:[...operations].map(name=>name.replace('.',' ')).concat(['capabilities','init','logs','version','--help']).sort()};
      const output={...description,backend_available:store.state==='ready'||store.state==='absent',limitation:limitation??(store.state==='maintenance'?'Explicit maintenance recovery is pending.':null),identity:'sha256:'+createHash('sha256').update(JSON.stringify(description)).digest('hex'),store};
      return {exitCode:0,output:JSON.stringify(output)+'\n'};
    }
    let outcome;
    if(maintenance) {
      const input=validateMaintenance(operation,parseInput(stdin()),!!flags['--dry-run']);
      outcome=await executeMaintenance({project_root:root,task:operation,preview:!!flags['--dry-run'],input,receipt_profile:`maintenance-${format}-v1`});
    } else if (operation === 'change.context') {
      const body = flags['--input'] ? parseInput(stdin()) : null;
      if (body) validateTask('query', body);
      outcome = await inspectRecords({ project_root: root, query: { kind: 'change-context', change_id: changeId, selectors: body?.selectors ?? null, include_observations: body?.include_observations ?? true } });
    } else if(reading) {
      const query=operation==='review.show'?{kind:'review',change_id:changeId,id:itemId}:itemId?{kind:'verification',change_id:changeId,id:itemId}:{kind:'verification-context',change_id:changeId};
      outcome=await inspectRecords({project_root:root,query});
    } else {
      const body = parseInput(stdin()); validateTask(mutationSchemas[operation], body);
      if (body.change_id !== changeId) fail('invalid-request', 'Body and command Change scopes disagree.');
      outcome = await (flags['--dry-run'] ? previewRecordTask : executeRecordTask)({ project_root: root, task: operation, change_id: changeId, item_id: itemId, expected_revision: body.expected_revision, reads: body.reads, input: body.input, receipt_profile: `record-${format}-v1` });
    }
    try { return { exitCode: exitCode(publicResult(operation, changeId, outcome)), output: encodeReceipt(operation, changeId, outcome, `${maintenance?'maintenance':'record'}-${format}-v1`) }; }
    catch (error) { error.committed = outcome.committed; throw error; }
  } catch (error) {
    const output = failure(operation, error, changeId ? { change_id: changeId } : {});
    if(operation?.startsWith('store.'))output.interface='store-maintenance-v1';
    return { exitCode: exitCode(output), output: JSON.stringify(output) + '\n' };
  }
}
