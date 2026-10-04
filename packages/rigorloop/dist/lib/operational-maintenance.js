import { readFileSync, readdirSync, mkdirSync, renameSync, unlinkSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { randomUUID } from 'node:crypto';
import { inspectLegacy, buildImportedCandidate, recheckLegacy, legacyLockDescriptors, acquireLegacyLocks } from './operational-legacy-import.js';
import { CONTRACT, fail, exact, canonical, parseInput, failure, LIMIT } from './operational-contract.js';
import { project, stat, regular, directory, acquireLease, durableWrite, syncDirectory } from './operational-files.js';
import { fence, ownerAbsent, owner } from './operational-coordination.js';
import { qualifyRuntime, openOperationalDatabase, metadata } from './operational-store.js';
import { MAINTENANCE_INTERFACE, validateMaintenance } from './operational-maintenance-contract.js';
import { digest, inventory, sameInventory, fileIdentity, absolutePath, atomicJSON, copyDurable, validateBundle, validateDatabase } from './operational-bundle.js';

const units = ['rigorloop.db','rigorloop.db-wal','rigorloop.db-shm','rigorloop.db-journal','artifacts/changes'];
const storeToken = meta => meta.store_incarnation + ':' + meta.store_revision;
function unitSet(runtime) { return Object.fromEntries(units.map(name => [name, inventory(join(runtime,name))])); }
function active(info) {
  const base = join(info.root,'.rigorloop/maintenance'), path = join(base,'active.json');
  if (!stat(path)) return null;
  regular(path); const entry = parseInput(readFileSync(path));
  if (entry.project_id !== info.id || !/^[a-f0-9-]{36}$/.test(entry.operation_id)) fail('project-mismatch','Unrecognized maintenance fence.');
  const operation = join(base,entry.operation_id), manifestPath = join(operation,'manifest.json');
  const manifest = stat(manifestPath) ? parseInput(readFileSync(manifestPath)) : null;
  const observed = { fence: entry, manifest, live: unitSet(join(info.root,'.rigorloop')), operation: (inventory(operation)??[]).filter(entry=>entry.path!==''&&!['resume-exclusion.sqlite','resume-exclusion.sqlite-journal','resume-exclusion.sqlite-wal','resume-exclusion.sqlite-shm'].includes(entry.path)) };
  return { entry, operation, manifestPath, manifest, observation: digest(canonical(observed)) };
}
export async function observeStore(info, fenced = false) {
  const maintenance = active(info);
  if (maintenance && !fenced) return {state:'maintenance',revision:null,observation:maintenance.observation,database_schema:null,maintenance:{operation_id:maintenance.entry.operation_id,task:maintenance.entry.task,phase:maintenance.manifest?.phase??'unavailable',observation:maintenance.observation}};
  const runtime = join(info.root,'.rigorloop');
  const observed = unitSet(runtime), observation = digest(canonical({ project_id:info.id, files:observed }));
  if (Object.values(observed).every(value=>value===null)) return {state:'absent',revision:null,observation,database_schema:null,maintenance:null};
  let db;
  try {
    ({db}=await openOperationalDatabase(info,false)); db.exec('BEGIN');
    const meta=metadata(db,info); db.exec('COMMIT');
    return {state:'ready',revision:storeToken(meta),observation:null,database_schema:1,maintenance:null};
  } catch (error) {if(error.operationalCode==='project-mismatch')throw error;return {state:'unavailable',revision:null,observation,database_schema:null,maintenance:null};}
  finally {db?.close();}
}
export async function inspectStore(root) {
  const info=project(root);qualifyRuntime();
  if (active(info)) return observeStore(info);
  const lease=acquireLease(info);try{return await observeStore(info);}finally{lease.release();}
}
function checkExpectation(observation, expectation, replace) {
  if (expectation.kind==='absent') {
    if (replace || observation.state!=='absent') fail('destination-conflict','An absent store was required; replacement was not authorized.');
  } else {
    if (!replace) fail('invalid-request','Occupied destination requires explicit replacement.');
    if (expectation.kind==='current' && (observation.state!=='ready'||expectation.revision!==observation.revision) || expectation.kind==='unavailable' && (observation.state!=='unavailable'||expectation.observation!==observation.observation)) fail('destination-conflict','Destination no longer matches the selected store observation.');
  }
}
function details(manifest, phase=manifest.phase) {
  return {operation_id:manifest.id,phase,output:manifest.output??null,retained_prior:manifest.retained_prior??null,scope:manifest.scope??null,integrity:manifest.integrity??null,limitations:manifest.limitations??[]};
}
function outcome(task,status,committed,manifest,revision=null,diagnostics=[]) {
  return {kind:'maintenance',status,committed,changed:task==='store.backup'?{count:0,entries:[],omitted:0}:null,diagnostics,identity:{record_contract:CONTRACT,change_revision:null,store_revision:revision},maintenance:details(manifest)};
}
function writeManifest(operation,manifest) {
  if(Buffer.byteLength(JSON.stringify(manifest))>LIMIT)fail('size-limit','Maintenance manifest exceeds 1 MiB.');
  atomicJSON(join(operation,'manifest.json'),manifest);
}
function createOperation(lock,task,input) {
  const id=lock.value.operation_id,operation=directory(join(lock.maintenance,id),true);
  const manifest={version:1,id,task,project_id:lock.value.project_id,phase:'prepared',input,scope:null,integrity:null,limitations:[],output:null,retained_prior:null};
  writeManifest(operation,manifest);return {operation,manifest};
}
function makeParents(path,root) {
  if(path===root)return;
  if(!stat(dirname(path)))makeParents(dirname(path),root);
  directory(path,true);
}
async function captureBackup(info,lock,operation,manifest,input) {
  const output=absolutePath(input.output,info,true);
  const stage=join(dirname(output),'.rigorloop-backup-'+manifest.id);
  manifest.output=output;manifest.stage=stage;writeManifest(operation,manifest);
  directory(stage,true);directory(join(stage,'attachments'),true);syncDirectory(dirname(stage));
  let db;
  try {
    ({db}=await openOperationalDatabase(info,false));
    const meta=metadata(db,info),all=db.prepare('SELECT change_id FROM changes ORDER BY change_id').all().map(r=>r.change_id);
    const included=input.scope.changes==='all'?all:[...input.scope.changes].sort();
    if(included.some(id=>!all.includes(id)))fail('record-missing','Backup selected a missing Change.');
    const {backup,DatabaseSync}=await import('node:sqlite');
    await backup(db,join(stage,'database.sqlite'));
    const snapshot=new DatabaseSync(join(stage,'database.sqlite'),{readBigInts:true,allowExtension:false});
    try {
      snapshot.exec('PRAGMA foreign_keys=ON; BEGIN IMMEDIATE; PRAGMA defer_foreign_keys=ON');
      const tables=snapshot.prepare("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT IN ('project','changes')").all().map(r=>r.name);
      for(const id of all.filter(id=>!included.includes(id))) {
        for(const table of tables) {
          if(!/^[a-z_]+$/.test(table))fail('store-unavailable','Unexpected table in backup source.');
          snapshot.prepare('DELETE FROM '+table+' WHERE change_id=?').run(id);
        }
        snapshot.prepare('DELETE FROM changes WHERE change_id=?').run(id);
      }
      snapshot.exec('COMMIT; PRAGMA journal_mode=DELETE');
      for(const row of snapshot.prepare('SELECT change_id,name FROM attachments ORDER BY change_id,name').all()) {
        const target=join(stage,'attachments',row.change_id);directory(target,true);
        copyDurable(join(lock.runtime,'artifacts/changes',row.change_id,row.name),join(target,row.name));
      }
    } finally {snapshot.close();}
    const checked=await validateDatabase(join(stage,'database.sqlite'),info.id,join(stage,'attachments'));
    const record={format:1,backup_id:manifest.id,project_id:info.id,source_incarnation:meta.store_incarnation,source_revision:meta.store_revision.toString(),database_schema:1,record_contract:CONTRACT,included_changes:included,excluded_changes:all.filter(id=>!included.includes(id)),external_references:checked.external,files:[{path:'database.sqlite',...fileIdentity(join(stage,'database.sqlite'))},...checked.attachments.map(a=>({...a,path:'attachments/'+a.path}))]};
    const bytes=JSON.stringify(record)+'\n';if(Buffer.byteLength(bytes)>LIMIT)fail('size-limit','Backup member manifest exceeds 1 MiB.');
    durableWrite(join(stage,'manifest.json'),bytes);durableWrite(join(stage,'complete.json'),JSON.stringify({manifest_digest:digest(bytes)})+'\n');syncDirectory(stage);
    await validateBundle(stage,info,digest(bytes));
    manifest.integrity=digest(bytes);manifest.scope={included_changes:included,excluded_changes:record.excluded_changes};manifest.stage_identity=inventory(stage);writeManifest(operation,manifest);
    return meta;
  } finally {db?.close();}
}
async function publishBackup(info,operation,manifest) {
  if(!manifest.integrity||!manifest.stage_identity)fail('maintenance-required','Backup capture was incomplete; rollback its identified staging and start a new request.');
  if(stat(manifest.stage)) {
    if(!sameInventory(manifest.stage,manifest.stage_identity)||stat(manifest.output))fail('destination-conflict','Backup staging or destination changed.');
    await validateBundle(manifest.stage,info,manifest.integrity);
    manifest.publication_started=true;
    renameSync(manifest.stage,manifest.output);syncDirectory(dirname(manifest.output));manifest.publication_durable=true;
  } else {
    if(!sameInventory(manifest.output,manifest.stage_identity))fail('destination-conflict','Published backup differs from captured bytes.');
    await validateBundle(manifest.output,info,manifest.integrity);
  }
  manifest.phase='complete';writeManifest(operation,manifest);
}
async function stageRestore(info,operation,manifest,input) {
  const source=absolutePath(input.backup,info),bundle=await validateBundle(source,info,input.expected_backup);
  const candidate=directory(join(operation,'candidate'),true);directory(join(candidate,'artifacts'),true);directory(join(candidate,'artifacts/changes'),true);
  copyDurable(join(source,'database.sqlite'),join(candidate,'rigorloop.db'));
  const databaseMember=bundle.manifest.files.find(f=>f.path==='database.sqlite');
  if(canonical(fileIdentity(join(candidate,'rigorloop.db')))!==canonical({bytes:databaseMember.bytes,digest:databaseMember.digest}))fail('source-conflict','Copied database differs from selected backup bytes.');
  for(const attachment of bundle.checked.attachments) {
    const selectedMember=bundle.manifest.files.find(f=>f.path==='attachments/'+attachment.path);
    const [id,name]=attachment.path.split('/');const target=directory(join(candidate,'artifacts/changes',id),true);copyDurable(join(source,'attachments',id,name),join(target,name));
    if(canonical(fileIdentity(join(target,name)))!==canonical({bytes:selectedMember.bytes,digest:selectedMember.digest}))fail('source-conflict','Copied attachment differs from selected backup bytes.');
  }
  const {DatabaseSync}=await import('node:sqlite');const db=new DatabaseSync(join(candidate,'rigorloop.db'),{readBigInts:true,allowExtension:false});
  try{db.exec('PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; BEGIN IMMEDIATE');db.prepare('UPDATE project SET store_incarnation=? WHERE singleton=1').run(randomUUID());db.exec('COMMIT; PRAGMA wal_checkpoint(TRUNCATE)');}finally{db.close();}
  await validateDatabase(join(candidate,'rigorloop.db'),info.id,join(candidate,'artifacts/changes'));
  manifest.scope={included_changes:bundle.manifest.included_changes,source:input.expected_backup};manifest.integrity=input.expected_backup;manifest.candidate=unitSet(candidate);manifest.output=join(info.root,'.rigorloop/rigorloop.db');
  manifest.retained_prior=join(operation,'displaced');writeManifest(operation,manifest);
}
function moveUnit(source,target,root) {
  makeParents(dirname(target),root);renameSync(source,target);syncDirectory(dirname(source));syncDirectory(dirname(target));
}
async function activate(info,operation,manifest,rollback=false) {
  const runtime=join(info.root,'.rigorloop'),candidate=join(operation,'candidate'),displaced=directory(join(operation,'displaced'),true);
  if(!manifest.before||!manifest.candidate)fail('maintenance-required','Replacement was not prepared; only rollback of untouched staging is available.');
  if(rollback&&manifest.phase==='activated')fail('invalid-request','Activated replacement cannot be rolled back.');
  // Verify every location before any further move. Unknown bytes never acquire
  // ownership from a path name or from an interrupted previous invocation.
  for(const unit of units) {
    const live=inventory(join(runtime,unit)),prior=inventory(join(displaced,unit)),next=inventory(join(candidate,unit));
    const before=manifest.before[unit],after=manifest.candidate[unit];
    if(live!==null&&canonical(live)!==canonical(before)&&canonical(live)!==canonical(after)||prior!==null&&canonical(prior)!==canonical(before)||next!==null&&canonical(next)!==canonical(after))fail('destination-conflict','Foreign or ambiguous bytes in replacement recovery.');
    if(before!==null&&prior===null&&canonical(live)!==canonical(before))fail('destination-conflict','Retained prior bytes are unavailable.');
    if(after!==null&&next===null&&canonical(live)!==canonical(after))fail('destination-conflict','Validated candidate bytes are unavailable.');
  }
  if(rollback) {
    for(const unit of [...units].reverse()) {
      const live=join(runtime,unit),old=join(displaced,unit),next=join(candidate,unit);
      if(stat(live)&&sameInventory(live,manifest.candidate[unit])&&!stat(next))moveUnit(live,next,operation);
      if(stat(old)) {
        if(stat(live))fail('destination-conflict','Rollback destination is occupied.');
        moveUnit(old,live,runtime);
      }
    }
    if(canonical(unitSet(runtime))!==canonical(manifest.before))fail('destination-conflict','Rollback did not restore the observed original file set.');
    manifest.phase='complete';manifest.rolled_back=true;writeManifest(operation,manifest);return null;
  }
  for(const unit of units) {
    const live=join(runtime,unit),old=join(displaced,unit),next=join(candidate,unit);
    if(manifest.before[unit]!==null&&!stat(old))moveUnit(live,old,operation);
    if(stat(next)) {if(stat(live))fail('destination-conflict','Candidate destination is occupied.');moveUnit(next,live,runtime);}
  }
  await validateDatabase(join(runtime,'rigorloop.db'),info.id,join(runtime,'artifacts/changes'));
  let db,revision;
  try{({db}=await openOperationalDatabase(info,false));revision=storeToken(metadata(db,info));db.exec('PRAGMA wal_checkpoint(TRUNCATE)');}finally{db?.close();}
  manifest.phase='activated';manifest.store_revision=revision;manifest.activation_started=true;writeManifest(operation,manifest);manifest.activation_durable=true;return revision;
}
async function resumeMaintenance(info,task,input) {
  const current=active(info);
  if(!current||current.entry.task!==task||current.entry.operation_id!==input.resume.operation_id||current.observation!==input.resume.expected_observation)fail('destination-conflict','Maintenance observation no longer matches.');
  if(!ownerAbsent(current.entry.owner))fail('store-busy','Maintenance owner may still be active.');
  // A private SQLite transaction supplies crash-released process exclusion.
  // Stale PID-file deletion cannot safely arbitrate competing resumptions.
  directory(current.operation,true);
  const guardPath=join(current.operation,'resume-exclusion.sqlite');
  for(const suffix of ['','-journal','-wal','-shm'])regular(guardPath+suffix,true);
  const {DatabaseSync}=await import('node:sqlite');
  const guard=new DatabaseSync(guardPath,{timeout:0,defensive:true,allowExtension:false});
  try {
    guard.exec('PRAGMA synchronous=FULL; BEGIN IMMEDIATE');
    const tables=guard.prepare("SELECT name FROM sqlite_schema WHERE type='table'").all();
    if(!tables.length){guard.exec('CREATE TABLE exclusion(project TEXT NOT NULL, operation TEXT NOT NULL) STRICT');guard.prepare('INSERT INTO exclusion VALUES (?,?)').run(info.id,current.entry.operation_id);}
    else if(tables.length!==1||tables[0].name!=='exclusion')fail('store-unavailable','Unrecognized resume exclusion database.');
    const rows=guard.prepare('SELECT project,operation FROM exclusion').all();
    if(rows.length!==1||rows[0].project!==info.id||rows[0].operation!==current.entry.operation_id)fail('project-mismatch','Resume exclusion belongs to another operation.');
    const fresh=active(info);
    if(!fresh||fresh.observation!==input.resume.expected_observation)fail('destination-conflict','Maintenance changed while acquiring resume exclusion.');
  } catch(error) {
    try{guard.exec('ROLLBACK');}catch{}guard.close();
    if([5,6].includes(error.errcode))fail('store-busy','Another resume owns recovery.');throw error;
  }
  const {operation}=current;let manifest=current.manifest;
  let releaseLegacy;
  let committed=manifest?.phase==='activated'||manifest?.task==='store.backup'&&manifest.phase==='complete';
  try {
    const rollback=input.resume.action==='rollback';
    if(!manifest) {
      if(!rollback)fail('maintenance-required','Capture did not establish a manifest; only fence rollback is available.');
      manifest={id:current.entry.operation_id,task,project_id:info.id,phase:'complete',rolled_back:true,limitations:['No capture manifest was established; all existing operation bytes were retained.']};
      writeManifest(operation,manifest);
    }
    if(task==='store.migrate'&&manifest.legacy_locks) {
      const previous=[...manifest.legacy_locks,...manifest.legacy_prior_locks??[]];
      manifest.legacy_prior_locks=previous;
      manifest.legacy_locks=legacyLockDescriptors(previous[0].root,manifest.input.changes);writeManifest(operation,manifest);
      releaseLegacy=acquireLegacyLocks(manifest.legacy_locks,previous);
    }
    if(task==='store.migrate'&&!rollback&&!manifest.rolled_back&&manifest.phase!=='activated') {
      const source=inspectLegacy(info,manifest.input,manifest.legacy_locks);
      if(source.identity!==manifest.input.expected_source)fail('source-conflict','Legacy source changed before resumed activation.');
      if(!manifest.originals_identity||!sameInventory(manifest.originals_output,manifest.originals_identity))fail('source-conflict','Required retained originals are unavailable or changed.');
    }
    if(committed&&rollback)fail('invalid-request','Published maintenance cannot be rolled back.');
    if(manifest.rolled_back) {
      if(manifest.before&&canonical(unitSet(join(info.root,'.rigorloop')))!==canonical(manifest.before))fail('destination-conflict','Restored original state changed before terminal rollback cleanup.');
      // Terminal rollback is a completed recovery decision. Releasing a fence
      // after result loss must never reinterpret finish as candidate activation.
      committed=false;
    } else if(task==='store.backup') {
      if(rollback) {
        if(stat(manifest.output))fail('destination-conflict','Output exists; inspect publication before rollback.');
        if(manifest.stage&&stat(manifest.stage)) {
          if(manifest.stage_identity) {
            if(!sameInventory(manifest.stage,manifest.stage_identity))fail('destination-conflict','Staging bytes changed.');
            rmSync(manifest.stage,{recursive:true});syncDirectory(dirname(manifest.stage));
          } else manifest.limitations.push('Incomplete staging retained for inspection; exact cleanup ownership is unavailable: '+manifest.stage);
        }
        manifest.phase='complete';manifest.rolled_back=true;writeManifest(operation,manifest);
      } else {await publishBackup(info,operation,manifest);committed=true;}
    } else if(manifest.phase==='activated') {
      // Once activated, validate identity; never reapply the captured candidate.
      const observed=await observeStore(info,true);
      if(observed.revision!==manifest.store_revision)fail('destination-conflict','Activated store changed before fence release.');
    } else if(!manifest.before&&rollback) {
      manifest.phase='complete';manifest.rolled_back=true;writeManifest(operation,manifest);
    } else {await activate(info,operation,manifest,rollback);committed=!rollback;}
    // Source cleanup is part of recovery. Keep the fence if it cannot finish,
    // even when the candidate is already durably activated.
    if(releaseLegacy){const release=releaseLegacy;releaseLegacy=null;release();}
    const fencePath=join(info.root,'.rigorloop/maintenance/active.json');
    const saved=parseInput(readFileSync(fencePath));if(canonical(saved)!==canonical(current.entry))fail('destination-conflict','Fence ownership changed during recovery.');
    unlinkSync(fencePath);syncDirectory(dirname(fencePath));
    return outcome(task,'saved',committed,manifest,manifest.store_revision??null);
  } catch(error){error.committed=committed;error.maintenance=manifest?details(manifest):null;throw error;}
  finally{
    try{try{releaseLegacy?.();}finally{try{guard.exec('ROLLBACK');}finally{guard.close();}}}
    catch(error){error.committed=committed;error.maintenance=manifest?details(manifest):null;throw error;}
  }
}
function maintenanceFailure(task,error,manifest,committed) {
  error.committed=Object.hasOwn(error,'committed')?error.committed:committed;
  const result=failure(task,error);
  return {kind:'maintenance',status:result.status,committed:result.committed,changed:result.committed!==false?null:{count:0,entries:[],omitted:0},diagnostics:result.errors,identity:{record_contract:CONTRACT,change_revision:null,store_revision:null},maintenance:error.maintenance??(manifest?details(manifest):{operation_id:null,phase:'unavailable',output:null,retained_prior:null,scope:null,integrity:null,limitations:[]})};
}
export async function executeMaintenance(request) {
  let manifest,lock,operation,releaseLegacy,committed=false;
  try {
    exact(request,['project_root','task','preview','input','receipt_profile']);
    if(!['store.backup','store.restore','store.migrate'].includes(request.task)||typeof request.preview!=='boolean'||!['maintenance-json-v1','maintenance-text-v1'].includes(request.receipt_profile))fail('invalid-request','Invalid typed maintenance request.');
    const input=validateMaintenance(request.task,{schema_version:1,interface:MAINTENANCE_INTERFACE,input:request.input},request.preview);
    qualifyRuntime();const info=project(request.project_root);
    if(input.resume)return await resumeMaintenance(info,request.task,input);
    if(request.task==='store.migrate'&&input.mode==='schema-upgrade') {
      if(input.target_schema!==1)fail('schema-unsupported','No packaged ordered migration supports this target schema.');
      const observation=await inspectStore(info.root);checkExpectation(observation,input.expected_store,true);
      return outcome(request.task,'unchanged',false,{id:null,phase:'complete',scope:{database_schema:1},limitations:['Database is already at schema 1; no upgrade or backup was needed.']},observation.revision);
    }
    let source;
    if(request.task==='store.migrate') {
      if(input.expected_store.kind!=='absent')fail('invalid-request','Legacy import requires an absent SQLite destination.');
      absolutePath(input.originals_output,info,true);
      source=inspectLegacy(info,input);
      if(!request.preview&&input.expected_source!==source.identity)fail('source-conflict','Legacy source observation changed.');
      if(!request.preview&&source.classifications.some(d=>d.action==='block'))fail('invalid-request','Selected source dispositions remain blocked; inspect import dry-run.');
    }
    if(request.preview) {
      const lease=acquireLease(info);
      try {
        manifest={id:null,phase:'prepared',scope:null,limitations:['Preview reserves no source, destination or store revision.']};
        if(request.task==='store.backup') {
          absolutePath(input.output,info,true);let db;
          try{
            ({db}=await openOperationalDatabase(info,false));
            const checked=await validateDatabase(join(info.root,'.rigorloop/rigorloop.db'),info.id,join(info.root,'.rigorloop/artifacts/changes'));
            const selected=input.scope.changes==='all'?checked.changes:input.scope.changes;
            if(selected.some(id=>!checked.changes.includes(id)))fail('record-missing','Backup selected a missing Change.');
            manifest.scope={included_changes:selected,excluded_changes:checked.changes.filter(id=>!selected.includes(id))};
          }finally{db?.close();}
        } else if(request.task==='store.migrate') {
          checkExpectation(await observeStore(info),input.expected_store,false);
          manifest.scope={included_changes:input.changes,source_observation:source.identity,dispositions:source.classifications};
          manifest.integrity=source.identity;
        } else {
          const source=absolutePath(input.backup,info),bundle=await validateBundle(source,info,input.expected_backup);
          checkExpectation(await observeStore(info),input.expected_store,input.replace);manifest.scope={included_changes:bundle.manifest.included_changes};
        }
        return outcome(request.task,'preview',false,manifest);
      } finally{lease.release();}
    }
    lock=await fence(info,request.task);({operation,manifest}=createOperation(lock,request.task,input));
    if(source) {
      manifest.legacy_locks=legacyLockDescriptors(source.root,input.changes);writeManifest(operation,manifest);
      releaseLegacy=acquireLegacyLocks(manifest.legacy_locks);
      source=inspectLegacy(info,input,manifest.legacy_locks);
      if(source.identity!==input.expected_source)fail('source-conflict','Legacy source changed before exclusion.');
    }
    if(request.task==='store.backup') {
      const meta=await captureBackup(info,lock,operation,manifest,input);await publishBackup(info,operation,manifest);committed=true;
      lock.release();return outcome(request.task,'saved',true,manifest,storeToken(meta));
    }
    if(request.task==='store.migrate') {
      const originals=absolutePath(input.originals_output,info,true),stage=join(dirname(originals),'.rigorloop-originals-'+manifest.id);
      manifest.originals_output=originals;manifest.originals_stage=stage;manifest.scope={included_changes:input.changes,source_observation:source.identity,dispositions:source.classifications};manifest.integrity=source.identity;writeManifest(operation,manifest);
      await buildImportedCandidate(info,input,source,join(operation,'candidate'),stage);
      recheckLegacy(source,manifest.legacy_locks);
      manifest.originals_identity=inventory(stage);manifest.candidate=unitSet(join(operation,'candidate'));manifest.output=join(lock.runtime,'rigorloop.db');manifest.retained_prior=join(operation,'displaced');writeManifest(operation,manifest);
      renameSync(stage,originals);syncDirectory(dirname(originals));manifest.originals_published=true;writeManifest(operation,manifest);
    } else await stageRestore(info,operation,manifest,input);
    checkExpectation(await observeStore(info,true),input.expected_store,input.replace??false);
    // Checkpoint coherent source before recording exact displaced bytes. An
    // unreadable source is preserved with every existing sidecar instead.
    if(input.expected_store.kind==='current') {let db;try{({db}=await openOperationalDatabase(info,false));db.exec('PRAGMA wal_checkpoint(TRUNCATE)');}finally{db?.close();}}
    manifest.before=unitSet(lock.runtime);writeManifest(operation,manifest);
    if(source)recheckLegacy(source,manifest.legacy_locks);
    const revision=await activate(info,operation,manifest);committed=true;
    if(releaseLegacy){const release=releaseLegacy;releaseLegacy=null;release();}
    lock.release();
    return outcome(request.task,'saved',true,manifest,revision);
  } catch(error) {
    if(manifest?.activation_durable||manifest?.publication_durable)committed=true;
    else if(manifest?.activation_started||manifest?.publication_started)committed=null;
    return maintenanceFailure(request.task,error,manifest,committed);
  } finally {try{releaseLegacy?.();}catch(error){return maintenanceFailure(request.task,error,manifest,committed);}}
}
