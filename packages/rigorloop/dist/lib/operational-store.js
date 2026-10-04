import { readFileSync, openSync, closeSync } from 'node:fs';
import { join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { CONTRACT, LIMIT, fail, exact, validateType, validateTask, createChange, validateChange, encodedSize, issueReserve, failure, canonical } from './operational-contract.js';
import { encodeReceipt, publicResult } from './operational-receipt.js';
import { emptyAccounts, validateSnapshot, selectedOutcome, handoff } from './operational-model.js';
import { captureAttachments, removeUnusedAttachments, attachmentPath } from './operational-attachments.js';
import { updateSnapshot, changedRecords, prepareReview, recordReview, recordVerification, completeChange } from './operational-tasks.js';
import { loadSnapshot, saveSnapshot } from './operational-rows.js';
import { project, acquireLease, regular, checkSubjects, observeSubjects, stat } from './operational-files.js';

const MAX_REVISION = 9223372036854775807n;
const schemaSQL = readFileSync(new URL('./migrations/operational-schema-1.sql', import.meta.url), 'utf8');
export function qualifyRuntime() {
  const [major, minor] = process.versions.node.split('.').map(Number);
  const sqlite = (process.versions.sqlite ?? '0.0.0').split('.').map(Number);
  if (major !== 24 || minor < 15 || sqlite[0] < 3 || (sqlite[0] === 3 && (sqlite[1] < 51 || (sqlite[1] === 51 && sqlite[2] < 3)))) fail('unsupported-runtime', 'Operational SQLite requires a qualified Node 24.15+ runtime with SQLite 3.51.3 or newer.');
}
export function metadata(db, info) {
  const version = db.prepare('PRAGMA user_version').get().user_version;
  if (version === 0n) fail('store-unavailable', 'Database initialization is incomplete or unavailable; inspect before retrying.');
  if (version !== 1n) fail('schema-unsupported', 'The operational database schema is unsupported.');
  const row = db.prepare('SELECT * FROM project WHERE singleton=1').get();
  if (!row) fail('store-unavailable', 'Project metadata is incomplete.');
  if (row.project_id !== info.id) fail('project-mismatch', 'Database and project identities differ.');
  return row;
}
const readChange = loadSnapshot;
const revision = (meta, number) => meta.store_incarnation + ':' + number.toString();
const identity = (token = null, store = null) => ({ record_contract: CONTRACT, change_revision: token, store_revision: store });
function mutation(status, id, token = null) {
  return { kind: 'mutation', status, committed: status === 'saved', changed: { count: 1, entries: [{ kind: 'change', id }], omitted: 0 }, diagnostics: [], identity: identity(token) };
}
function capacity(change) { validateSnapshot({change,accounts:emptyAccounts()}); }
function insertChange(db, change) {
  saveSnapshot(db, { change, accounts: { basis: [], review: [], evidence: [], decision: [], verification: [], adoption: [] } }, 1n);
}
export async function openOperationalDatabase(info, create) {
  const path = join(info.root, '.rigorloop/rigorloop.db');
  const existing = regular(path, true);
  for (const suffix of ['-wal', '-shm', '-journal']) regular(path + suffix, true);
  if (!existing && !create) fail('store-unavailable', 'No operational database exists; reads do not initialize storage.');
  const { DatabaseSync } = await import('node:sqlite');
  let db;
  try {
    db = new DatabaseSync(path, { timeout: 5000, defensive: true, enableForeignKeyConstraints: true, allowExtension: false, enableDoubleQuotedStringLiterals: false, readBigInts: true });
    if (!existing) {
      db.exec('PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; BEGIN IMMEDIATE');
      try {
        // Another admitted first writer may have initialized while we waited.
        if (db.prepare('PRAGMA user_version').get().user_version === 0n) {
          db.exec(schemaSQL);
          db.prepare('INSERT INTO project VALUES (1,?,?,0)').run(info.id, randomUUID());
        }
        db.exec('COMMIT');
      } catch (error) { try { db.exec('ROLLBACK'); } catch {} throw error; }
    }
    const meta = metadata(db, info);
    db.exec('PRAGMA foreign_keys=ON; PRAGMA synchronous=FULL');
    if (db.prepare('PRAGMA journal_mode').get().journal_mode !== 'wal' || db.prepare('PRAGMA foreign_keys').get().foreign_keys !== 1n || db.prepare('PRAGMA synchronous').get().synchronous !== 2n) fail('store-unavailable', 'Required SQLite settings are unavailable.');
    return { db, meta };
  } catch (error) { try { db?.close(); } catch {} if (error.operationalCode) throw error; if ([5,6].includes(error.errcode)) throw databaseFailure(error); fail('store-unavailable', 'The operational database cannot be opened coherently.'); }
}
function databaseFailure(error) {
  if (error.operationalCode) return error;
  if ([5, 6].includes(error.errcode) || ['SQLITE_BUSY', 'SQLITE_LOCKED'].includes(error.code)) return Object.assign(new Error('Operational storage is busy.'), { operationalCode: 'store-busy' });
  return Object.assign(new Error('Operational storage could not complete the request.'), { operationalCode: 'write-failed' });
}
async function runRecordTask(request, preview = false) {
  exact(request, ['project_root','task','change_id','item_id','expected_revision','reads','input','receipt_profile']);
  validateType('text',request.project_root);validateType('id',request.change_id);
  const creating=request.task==='change.create';
  const schema={'change.create':'create_input','change.update':'update_input','change.complete':'complete_input','review.prepare':'prepare_input','review.record':'review_input','verification.record':'verification_input'}[request.task];
  if(!schema||!['record-json-v1','record-text-v1'].includes(request.receipt_profile))fail('invalid-request','Unsupported typed task variant.');
  if(request.task.startsWith('change.')){if(request.item_id!==null)fail('invalid-request','Change task does not admit an item ID.');}
  else validateType('id',request.item_id);
  if(creating?request.expected_revision!==null:typeof request.expected_revision!=='string'||!request.expected_revision.trim())fail('invalid-request','Invalid expected revision for task.');
  validateTask(schema,request.input);
  if(!Array.isArray(request.reads)||request.reads.length>64)fail('invalid-request','Invalid subject collection.');
  request.reads.forEach(subject=>validateType('subject',subject));
  qualifyRuntime();
  const info=project(request.project_root);
  const initial=creating?{change:createChange(request.change_id,request.input),accounts:emptyAccounts()}:null;
  if(initial)validateSnapshot(initial);
  checkSubjects(info.root,request.reads);
  const lease=acquireLease(info);
  let db,inTransaction=false,committed=false,captured;
  try {
    if(preview&&creating&&!stat(join(lease.runtime,'rigorloop.db')))return mutation('preview',request.change_id);
    ({db}=await openOperationalDatabase(info,creating&&!preview));
    db.exec(preview?'BEGIN':'BEGIN IMMEDIATE');inTransaction=true;
    const meta=metadata(db,info),before=readChange(db,request.change_id);
    if(creating&&before)fail('invalid-request','The Change already exists.');
    if(!creating&&!before)fail('record-missing','The selected Change is absent.');
    if(before&&revision(meta,before.revision)!==request.expected_revision)fail('revision-conflict','The Change has changed; inspect and reconcile current intent.');
    if(before)validateSnapshot(before);
    const observed=[];
    const observe=selection=>{const subjects=observeSubjects(info.root,selection);observed.push(...subjects);return subjects;};
    const check=subjects=>{
      if(!subjects.length||subjects.some(s=>s.state==='present'&&s.identity===null))fail('invalid-request','Compared support needs explicit comparable subjects.');
      checkSubjects(info.root,subjects);observed.push(...subjects);
    };
    const next=creating?initial:request.task==='change.update'?updateSnapshot(before,request.input,observe)
      :request.task==='review.prepare'?prepareReview(before,request.item_id,request.input,observe)
      :request.task==='review.record'?recordReview(before,request.item_id,request.input,check)
      :request.task==='verification.record'?recordVerification(before,request.item_id,request.input,observe,check)
      :completeChange(before,request.input);
    if(request.input.evidence) {
      captured=captureAttachments(info.root,before.change,request.input.evidence,preview);
      next.change.attachments.push(...captured.metadata);
      next.change.attachments.sort((a,b)=>a.name.localeCompare(b.name,'en'));
      for(const evidence of request.input.evidence) if(evidence.observation.method==='compared') {
        if(!evidence.subjects.length||evidence.subjects.some(s=>s.state==='present'&&s.identity===null))fail('invalid-request','Compared evidence needs explicit comparable subjects.');
        checkSubjects(info.root,evidence.subjects);observed.push(...evidence.subjects);
      }
    }
    validateSnapshot(next);
    for(const value of request.input.evidence??[]) {
      const old=before.accounts.evidence.find(e=>e.id===value.id);
      for(const name of value.attachments)if(!old?.attachments.includes(name)&&!captured?.metadata.some(a=>a.name===name))regular(attachmentPath(info.root,request.change_id,name));
    }
    // Retaining a past unavailable reference is allowed. Renewed reliance and
    // new completion claims require the selected payload bytes to be readable.
    const relied = new Set();
    for (const review of next.accounts.review) {
      const old = before?.accounts.review.find(r => r.id === review.id);
      if (review.applicability.value === 'current' && canonical(review) !== canonical(old))
        review.assessment.support.forEach(s => s.attachments.forEach(name => relied.add(name)));
    }
    for (const verification of next.accounts.verification) {
      const old = before?.accounts.verification.find(v => v.id === verification.id);
      if (verification.outcome === 'success' && verification.support_state === 'current' && canonical(verification) !== canonical(old))
        verification.support.forEach(s => s.attachments.forEach(name => relied.add(name)));
    }
    if (next.change.completion && !before?.change.completion)
      next.change.completion.retained_attachments.forEach(name => relied.add(name));
    for (const name of relied) {
      const descriptor = next.change.attachments.find(a => a.name === name);
      const path = attachmentPath(info.root, request.change_id, name);
      try { if (regular(path).size !== descriptor.byte_count) throw new Error(); closeSync(openSync(path, 'r')); }
      catch { fail('payload-unavailable', 'Selected support attachment is unavailable: ' + name + '. Report the loss before renewed reliance.'); }
    }
    const entries=creating?[{kind:'change',id:request.change_id}]:changedRecords(before,next);
    for(const name of next.orphan_drops??[]) {
      const path=attachmentPath(info.root,request.change_id,name);
      if(!regular(path,true))fail('record-missing','Selected unused attachment is absent.');
      entries.push({kind:'attachment',id:name});
    }
    entries.sort((a,b)=>a.kind.localeCompare(b.kind,'en')||(a.review_id??'').localeCompare(b.review_id??'','en')||a.id.localeCompare(b.id,'en'));
    if(entries.length&&(meta.store_revision===MAX_REVISION||before?.revision===MAX_REVISION))fail('size-limit','Revision capacity is exhausted.');
    const number=creating?1n:before.revision+(entries.length?1n:0n);
    const token=preview?(before?revision(meta,before.revision):null):revision(meta,number);
    const status=entries.length?(preview?'preview':'saved'):'unchanged';
    const output={kind:'mutation',status,committed:status==='saved',changed:{count:entries.length,entries,omitted:0},diagnostics:[],identity:identity(token)};
    encodeReceipt(request.task,request.change_id,output,request.receipt_profile);
    checkSubjects(info.root,request.reads);checkSubjects(info.root,observed);
    if(preview||!entries.length)db.exec('ROLLBACK');
    else {
      captured?.publish();
      saveSnapshot(db,next,number);
      db.prepare('UPDATE project SET store_revision=? WHERE singleton=1').run(meta.store_revision+1n);
      committed=null;db.exec('COMMIT');committed=true;
    }
    inTransaction=false;
    if(committed===true&&before) {
      const dropped=[...before.change.attachments.filter(a=>!next.change.attachments.some(b=>a.name===b.name)).map(a=>a.name),...next.orphan_drops??[]];
      if(dropped.length)try {
        db.exec('BEGIN IMMEDIATE');
        const unused=dropped.filter(name=>!db.prepare('SELECT 1 FROM attachments WHERE change_id=? AND name=?').get(request.change_id,name));
        removeUnusedAttachments(info.root,request.change_id,unused);db.exec('ROLLBACK');
      }catch{try{db.exec('ROLLBACK');}catch{}output.diagnostics.push({code:'write-failed',message:'Records committed; unused attachment cleanup needs another explicit retention request.'});}
    }
    return output;
  } catch(error) {
    let rollbackKnown=!inTransaction;
    if(inTransaction){try{db.exec('ROLLBACK');rollbackKnown=true;}catch{}}
    committed=committed===true?true:rollbackKnown?false:null;
    const mapped=databaseFailure(error);mapped.committed=committed;
    if(captured?.published.length&&committed!==true)mapped.message+=' Selected attachment files may remain unused; inspect before explicit reuse or retention cleanup.';
    throw mapped;
  } finally {
    try{captured?.dispose();}catch{}
    try{db?.close();}catch(error){const mapped=databaseFailure(error);mapped.committed=committed;throw mapped;}finally{lease.release();}
  }
}
async function readRecords(request) {
  exact(request, ['project_root','query']);
  const kind=request.query?.kind;
  if(!['change-context','review','verification','verification-context'].includes(kind))fail('invalid-request','Unsupported query variant.');
  exact(request.query,kind==='change-context'?['kind','change_id','selectors','include_observations']:['review','verification'].includes(kind)?['kind','change_id','id']:['kind','change_id']);
  validateType('text', request.project_root);validateType('id',request.query.change_id);
  if(request.query.id!==undefined)validateType('id',request.query.id);
  if(kind==='change-context') {
    if(typeof request.query.include_observations!=='boolean')fail('invalid-request','Invalid observation selection.');
    if(request.query.selectors!==null) {
      if(!Array.isArray(request.query.selectors)||!request.query.selectors.length||request.query.selectors.length>64)fail('invalid-request','Invalid selectors.');
      request.query.selectors.forEach(s=>validateTask('selector',s));
    }
  }
  qualifyRuntime();
  const info = project(request.project_root), lease = acquireLease(info);
  let db;
  try {
    ({ db } = await openOperationalDatabase(info, false)); db.exec('BEGIN');
    const meta = metadata(db, info), found = readChange(db, request.query.change_id);
    if (!found) fail('record-missing', 'The selected Change is absent.');
    const token = revision(meta, found.revision), change = found.change;
    try { validateSnapshot(found); } catch { fail('store-unavailable', 'Stored records or relationships are incoherent.'); }
    const selected=kind==='change-context'?request.query.selectors:['review','verification'].includes(kind)?[{kind,id:request.query.id}]:null;
    const output=selected?selectedOutcome(found,selected,token):handoff(found,token);
    if(kind==='verification-context')output.projections=[{query_kind:'verification-context',value:{complete:true,governing_basis:output.projections[0].value.governing_basis??null,review_standing:output.projections[0].value.review_standing??null,verifications:found.accounts.verification,limitations:change.completion?['Historical completed Change; no current applicability comparison.']:['Records provide support; the verifier supplies the assessment.']}}];
    if(kind==='review')output.projections.push({query_kind:'review-standing',value:{selected:change.reviews.some(r=>r.review.id===request.query.id),complete:false,limitations:['Selected Review scope only; use Change context for other obligations.']}});
    if (kind !== 'change-context' || request.query.include_observations) {
      for (const descriptor of change.attachments) {
        try {
          const path = attachmentPath(info.root, change.change_id, descriptor.name);
          if (regular(path).size !== descriptor.byte_count) throw new Error();
          closeSync(openSync(path, 'r'));
        } catch {
          output.diagnostics.push({code:'payload-unavailable', message:'Retained attachment is missing, unreadable or has a different size: ' + descriptor.name});
        }
      }
    }
    try { encodeReceipt('change.context', change.change_id, output, 'record-json-v1'); }
    catch(error) {
      if(error.operationalCode!=='size-limit')throw error;
      const selector={schema_version:2,interface:'targeted-recording-v2',contract:CONTRACT,selectors:[{kind:'change',id:change.change_id}],include_observations:false};
      fail('size-limit','Retrieve the complete account index using --input - with '+JSON.stringify(selector));
    }
    db.exec('COMMIT'); return output;
  } catch (error) { if (db) { try { db.exec('ROLLBACK'); } catch {} } if (error.operationalCode) throw error; fail('store-unavailable', 'No coherent operational snapshot is available.'); }
  finally { try { db?.close(); } finally { lease.release(); } }
}

function rejectedOutcome(kind,error) {
  const output=failure(null,error);
  return {kind,status:output.status,committed:output.committed,diagnostics:output.errors,identity:{record_contract:null,change_revision:null,store_revision:null},...(kind==='read'?{records:[],projections:[]}:{changed:output.committed===null?null:{count:0,entries:[],omitted:0}})};
}
export async function executeRecordTask(request) {
  try{return await runRecordTask(request,false);}catch(error){return rejectedOutcome('mutation',error);}
}
export async function previewRecordTask(request) {
  try{return await runRecordTask(request,true);}catch(error){return rejectedOutcome('mutation',error);}
}
export async function inspectRecords(request) {
  try{return await readRecords(request);}catch(error){return rejectedOutcome('read',error);}
}
