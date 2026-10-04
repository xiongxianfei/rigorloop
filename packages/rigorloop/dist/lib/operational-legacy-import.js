// Qualified v3 source adapter. No legacy writer or public v3 dispatch is used.
import { readFileSync, mkdirSync, unlinkSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { randomUUID } from 'node:crypto';
import { parseV3Record, validateV3Set } from './record-format-v3.js';
import { RecordFiles } from './record-store-files.js';
import { owner, ownerAbsent } from './operational-coordination.js';
import { CONTRACT, canonical, createChange, fail, validateType } from './operational-contract.js';
import { emptyAccounts, validateSnapshot } from './operational-model.js';
import { saveSnapshot } from './operational-rows.js';
import { directory, stat, durableWrite, syncDirectory } from './operational-files.js';
import { digest, absolutePath, fileIdentity } from './operational-bundle.js';

function gate(reader,id,owned=[]) {
  const root=`.rigorloop/record-store/${id}`;
  const lock=reader.read(root+'/lock'),expected=owned.find(entry=>entry.path===root+'/lock');
  if(lock!==null&&(!expected||lock.toString()!==expected.value)||reader.read(root+'/journal.json')!==null)fail('store-busy','Quiesce and recover the selected legacy source before import.');
  return reader.hash(root+'/epoch');
}
function capture(root,ids,owned=[]) {
  const reader=new RecordFiles(root),files={},changes=[];
  for(const id of [...ids].sort()) {
    const initial=gate(reader,id,owned),path=`docs/changes/${id}/change.json`;
    if(reader.inspect(`docs/changes/${id}/change.yaml`).info)fail('schema-unsupported','Ambiguous or retired source layout.');
    const bytes=reader.read(path);if(bytes===null)fail('record-missing','Legacy Change is absent.');
    const change=parseV3Record('change',bytes),set={[path]:bytes};
    if(change.change_id!==id)fail('invalid-request','Source Change identity differs.');
    for(const record of change.records) {
      const content=reader.read(record.path);if(content===null)fail('store-unavailable','Registered legacy source content is unavailable.');set[record.path]=content;
    }
    const parsed=validateV3Set(id,set);
    if(gate(reader,id,owned)!==initial)fail('source-conflict','Legacy source changed during capture.');
    for(const [name,content] of Object.entries(set))if(digest(reader.read(name))!==digest(content))fail('source-conflict','Legacy source changed during capture.');
    if(gate(reader,id,owned)!==initial)fail('source-conflict','Legacy writer entered during capture.');
    Object.assign(files,set);changes.push({id,path,change,parsed});
  }
  const observations=Object.entries(files).sort(([a],[b])=>a.localeCompare(b)).map(([path,bytes])=>({path,bytes:bytes.length,digest:digest(bytes)}));
  return {files,changes,observations,identity:digest(canonical(observations))};
}
const sourceKey=(path,kind,id)=>kind==='change'?path:`${path}#${kind}/${id}`;
export function inspectLegacy(info,input,owned=[]) {
  if(input.source_contract!=='rigorloop-records-v3')fail('schema-unsupported','Only the qualified rigorloop-records-v3 source adapter is supported.');
  const root=absolutePath(input.source_root,info,false,true);directory(root);
  const captured=capture(root,input.changes,owned),items=[];
  for(const entry of captured.changes) {
    items.push({source_record:entry.path,kind:'change',id:entry.id,change_id:entry.id,value:entry.change,path:entry.path});
    for(const work of entry.change.work)items.push({source_record:sourceKey(entry.path,'work',work.id),kind:'work',id:work.id,change_id:entry.id,value:work,path:entry.path});
    for(const issue of entry.change.blockers)items.push({source_record:sourceKey(entry.path,'blocker',issue.id),kind:'blocker',id:issue.id,change_id:entry.id,value:issue,path:entry.path});
    for(const record of entry.change.records) {
      const data=entry.parsed.get(record.path);
      if(record.kind==='evidence') for(const value of data.checks)items.push({source_record:sourceKey(record.path,'evidence',value.id),kind:'evidence',id:value.id,change_id:entry.id,value,path:record.path});
      // The original container itself also receives a disposition. Assessment
      // and decision meanings remain attributable in the retained source bytes.
      items.push({source_record:record.path,kind:record.kind,id:data.id??record.kind,change_id:entry.id,value:data,path:record.path,container:true});
      for(const finding of data.findings??[])items.push({source_record:sourceKey(record.path,'finding',finding.id),kind:'finding',id:finding.id,change_id:entry.id,value:finding,path:record.path});
    }
  }
  if(new Set(input.dispositions.map(d=>d.source_record)).size!==input.dispositions.length||input.dispositions.some(d=>!items.some(i=>i.source_record===d.source_record)))fail('invalid-request','Duplicate or unknown source disposition.');
  const classifications=items.map(item=>{
    const supplied=input.dispositions.find(d=>d.source_record===item.source_record);
    const required=item.kind==='change'||item.kind==='work'&&!['completed','cancelled'].includes(item.value.status)||['blocker','finding'].includes(item.kind)&&['open','deferred'].includes(item.value.state);
    const importable=!item.container&&['change','work','blocker','finding','evidence'].includes(item.kind);
    const targetKind=item.kind==='finding'?'blocker':item.kind;
    let action=supplied?.action??'block',reason=supplied?.reason??'An explicit attributable disposition is required.';
    if(action==='retain'&&required){action='block';reason='Unresolved active dependencies must be imported, not hidden in retained originals.';}
    if(action==='import'&&(!importable||supplied.target?.kind!==targetKind||supplied.target?.id!==item.id||supplied.target?.change_id!==item.change_id||supplied.target?.parent_id!==null)){action='block';reason='This mapping is not qualified; preserve IDs and use the declared target kind. Original judgments must be retained without promotion.';}
    if(action!=='import'&&supplied?.target!==null&&supplied?.target!==undefined){action='block';reason='Retained or blocked material cannot declare an imported target.';}
    return {source_record:item.source_record,action,reason,target:action==='import'?supplied.target:null,allowed_target:importable?{change_id:item.change_id,kind:targetKind,id:item.id,parent_id:null}:null};
  });
  return {...captured,root,items,classifications};
}
function convertIssue(item) {
  const v=item.value;
  // Roles and resolution vocabularies are validated against v4 without guessing
  // equivalence; unsupported historical roles/dispositions block this mapping.
  return {id:v.id,reporter:v.reporter,owner:v.owner,scope:`Legacy ${item.kind} from ${item.source_record}; subjects: ${v.subjects.map(s=>s.path).join(', ')||'unspecified'}`,description:v.evidence,required_outcome:v.required_outcome,state:v.state,disposition:v.resolution?{actor:v.resolution.actor,reason:v.resolution.rationale,follow_up:null}:null};
}
export async function buildImportedCandidate(info,input,source,candidate,originalsStage) {
  if(source.classifications.some(d=>d.action==='block'))fail('invalid-request','Every selected source account needs an unblocked disposition.');
  if(input.expected_source!==source.identity)fail('source-conflict','Legacy source differs from the selected observation.');
  directory(candidate,true);directory(join(candidate,'artifacts'),true);directory(join(candidate,'artifacts/changes'),true);
  const {DatabaseSync}=await import('node:sqlite');
  const db=new DatabaseSync(join(candidate,'rigorloop.db'),{readBigInts:true,allowExtension:false});
  try {
    db.exec('PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; PRAGMA foreign_keys=ON; BEGIN IMMEDIATE');
    db.exec(readFileSync(new URL('./migrations/operational-schema-1.sql',import.meta.url),'utf8'));
    db.prepare('INSERT INTO project VALUES (1,?,?,0)').run(info.id,randomUUID());
    for(const original of source.changes) {
      const selected=source.classifications.filter(d=>d.action==='import'&&d.target.change_id===original.id);
      const c=createChange(original.id,{intent:{goal:input.reason,scope:`Resume selected legacy Change ${original.id}; requirement intent remains at ${original.change.proposal.path}`,exclusions:['No legacy approval is promoted to a requirement-first approval.']},request:{locator:original.path,content:input.reason,captured_by:input.actor},authority:{source:`Explicit import by ${input.actor.id}; source ${source.identity}`,allowed:[],limits:['Import does not grant new engineering execution authority; establish current authority before progression.'],reported_by:input.actor},activity:{stage:'support',status:'blocked',owner:input.actor,reason:'Imported work requires requirement-first basis and current authority reconciliation.'},next_action:{action:'Reconcile the preserved requirement/design basis, current authority and missing assessments before progression.',owner:input.actor,rationale:input.reason}});
      const snapshot={change:c,accounts:emptyAccounts()};
      if(original.change.plan)c.plan={...original.change.plan,state:'present'};
      for(const disposition of selected) {
        const item=source.items.find(i=>i.source_record===disposition.source_record),v=item.value;
        if(item.kind==='work')c.work.push({id:v.id,status:v.status,owner:v.owner,scope:`Legacy work ${v.id}; requirement references ${v.requirement_refs.join(', ')||'not supplied'}`,locations:[],remaining:['completed','cancelled'].includes(v.status)?null:'Resume from retained legacy source; reconcile current evidence.',completion_reason:['completed','cancelled'].includes(v.status)?'Legacy terminal work statement retained; no new review approval inferred.':null,check_refs:[],blocker_ids:[]});
        if(['blocker','finding'].includes(item.kind))c.blockers.push(convertIssue(item));
        if(item.kind==='evidence')snapshot.accounts.evidence.push({schema_version:4,contract:CONTRACT,change_id:c.change_id,id:v.id,actor:v.actor,reported_at:'Historical source; original did not record time',procedure:v.procedure,scope:`Legacy check ${v.id} from ${item.path}`,subjects:v.subjects.map(s=>({...s,state:'present'})),observation:{method:'unknown',actor:input.actor,scope:'Imported historical result',summary:'No new comparison or execution was performed.'},result:v.result,summary:v.summary,limitations:['Original reported result; current applicability requires assessment.'],attachments:[]});
      }
      validateSnapshot(snapshot);saveSnapshot(db,snapshot,1n);
    }
    db.exec('COMMIT; PRAGMA wal_checkpoint(TRUNCATE)');
  } finally {db.close();}
  directory(originalsStage,true);
  for(const [path,bytes] of Object.entries(source.files)) {
    let target=originalsStage;for(const part of path.split('/').slice(0,-1))target=directory(join(target,part),true);
    durableWrite(join(originalsStage,path),bytes);syncDirectory(target);
  }
  const manifest={format:1,source_contract:input.source_contract,source_root:source.root,source_identity:source.identity,project_id:info.id,actor:input.actor,reason:input.reason,dispositions:source.classifications,files:source.observations};
  const bytes=JSON.stringify(manifest)+'\n';durableWrite(join(originalsStage,'manifest.json'),bytes);durableWrite(join(originalsStage,'complete.json'),JSON.stringify({manifest_digest:digest(bytes)})+'\n');syncDirectory(originalsStage);
}
export function recheckLegacy(source,owned=[]) {
  const current=capture(source.root,source.changes.map(c=>c.id),owned);
  if(current.identity!==source.identity)fail('source-conflict','Legacy source changed; reclassify before activation.');
}

// The retained v3 executable honors these exact source lock paths. Holding
// them prevents a legacy writer from entering between capture and activation.
export function legacyLockDescriptors(root, ids) {
  return ids.map(id=>({root,path:`.rigorloop/record-store/${id}/lock`,owner:owner(),value:JSON.stringify({pid:process.pid,nonce:randomUUID()})+'\n'}));
}
export function acquireLegacyLocks(descriptors, prior=[]) {
  const acquired=[];
  const release=()=>{
    for(const entry of acquired.reverse()) {
      const reader=new RecordFiles(entry.root),bytes=reader.read(entry.path);
      if(bytes!==null&&bytes.toString()===entry.value)reader.removeLock(entry.path,digest(bytes));
      else if(bytes!==null)fail('source-conflict','Legacy capture lock ownership changed.');
    }
  };
  try {
    for(const entry of descriptors) {
      const reader=new RecordFiles(entry.root),old=reader.read(entry.path),previous=prior.find(p=>p.root===entry.root&&p.path===entry.path&&old?.toString()===p.value);
      if(old!==null) {
        if(!previous||old.toString()!==previous.value||!ownerAbsent(previous.owner))fail('store-busy','Legacy source is not quiescent.');
        reader.removeLock(entry.path,digest(old));
      }
      let directory='';for(const part of entry.path.split('/').slice(0,-1)){directory=directory?directory+'/'+part:part;reader.mkdir(directory);}
      try{reader.createLock(entry.path,Buffer.from(entry.value));}
      catch(error){if(error.code==='EEXIST')fail('store-busy','Another legacy actor acquired the source.');throw error;}
      acquired.push(entry);
    }
    return release;
  } catch(error){release();throw error;}
}
