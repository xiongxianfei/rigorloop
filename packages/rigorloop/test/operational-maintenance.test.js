import assert from 'node:assert/strict';
import { test } from 'node:test';
import { spawnSync } from 'node:child_process';
import { join } from 'node:path';
import { readFileSync,writeFileSync,existsSync,unlinkSync,renameSync,mkdirSync } from 'node:fs';
import { DatabaseSync } from 'node:sqlite';
import { project, actor, createInput, invoke, cli, databasePath } from './helpers/operational-fixture.mjs';

function command(root, words, input, extra=[]) {
  const p=spawnSync(process.execPath,[cli,...words,'--root',root,'--format','json',...extra,...(input?['--input','-']:[])],{encoding:'utf8',input:input?JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input}):undefined,timeout:15000});
  assert.ifError(p.error);assert.ok(p.stdout,p.stderr);return {exit:p.status,result:JSON.parse(p.stdout),stderr:p.stderr};
}
function setup(t) {
  const root=project(t);const created=invoke(root,['change','create'],createInput());assert.equal(created.exit,0,JSON.stringify(created));
  writeFileSync(join(root,'report.txt'),'retained report bytes');
  const evidence={id:'checks',actor,reported_at:'2026-10-04',procedure:'test navigation',scope:'Navigation',subjects:[],observation:{method:'reported',actor,scope:'Navigation',summary:'Observed test execution'},result:'passed',summary:'Checks passed',limitations:[],attachments:['report.txt'],retain:[{name:'report.txt',source:'report.txt',media_type:'text/plain'}]};
  const saved=invoke(root,['change','update'],{...createInput(),expected_revision:created.result.revision,input:{evidence:[evidence]}});assert.equal(saved.exit,0,JSON.stringify(saved));
  return {root,revision:saved.result.revision};
}
const backupInput=output=>({scope:{changes:'all'},output,actor});

test('maintenance backup captures selected complete records and payloads, restores into matching empty project',t=>{
  const {root,revision}=setup(t),output=join(root,'selected-backup');
  const second=createInput({change_id:'unselected'});
  const created=spawnSync(process.execPath,[cli,'change','create','--root',root,'--change','unselected','--input','-','--format','json'],{encoding:'utf8',input:JSON.stringify(second)});
  assert.equal(created.status,0,created.stdout);
  const selected={...backupInput(output),scope:{changes:['navigation']}};
  const preview=command(root,['store','backup'],selected,['--dry-run']);assert.equal(preview.exit,0,JSON.stringify(preview));assert.equal(existsSync(output),false);
  const saved=command(root,['store','backup'],selected);assert.equal(saved.exit,0,JSON.stringify(saved));assert.equal(saved.result.committed,true);
  const manifest=JSON.parse(readFileSync(join(output,'manifest.json'),'utf8'));
  assert.deepEqual(manifest.included_changes,['navigation']);assert.deepEqual(manifest.excluded_changes,['unselected']);
  assert.equal(readFileSync(join(output,'attachments/navigation/report.txt'),'utf8'),'retained report bytes');
  assert.equal(existsSync(join(output,'database.sqlite-wal')),false);
  const db=new DatabaseSync(join(output,'database.sqlite'),{readOnly:true});assert.equal(db.prepare('PRAGMA journal_mode').get().journal_mode,'delete');assert.deepEqual(db.prepare('SELECT change_id FROM changes').all().map(r=>r.change_id),['navigation']);db.close();
  const restored=project(t);writeFileSync(join(restored,'.rigorloop.json'),readFileSync(join(root,'.rigorloop.json')));
  const request={backup:output,expected_backup:saved.result.maintenance.integrity,expected_store:{kind:'absent'},replace:false,actor,reason:'Transfer selected context to another checkout'};
  const result=command(restored,['store','restore'],request);assert.equal(result.exit,0,JSON.stringify(result));assert.equal(result.result.committed,true);
  const context=invoke(restored,['change','context']);assert.equal(context.exit,0,JSON.stringify(context));assert.notEqual(context.result.revision,revision);
  assert.equal(readFileSync(join(restored,'.rigorloop/artifacts/changes/navigation/report.txt'),'utf8'),'retained report bytes');
  assert.equal(invoke(restored,['change','update'],{...createInput(),expected_revision:revision,input:{activity:{...createInput().input.activity,reason:'Stale pre-restore expectation'}}}).exit,3);
});

test('maintenance rejects unknown values, corrupt bundles, occupied outputs and stale replacement expectations',t=>{
  const {root}=setup(t),output=join(root,'backup');
  const unknown=command(root,['store','backup'],{...backupInput(output),extra:true});assert.equal(unknown.exit,2);assert.equal(existsSync(join(root,'.rigorloop/maintenance/active.json')),false);
  for (const input of [{...backupInput(output),actor:{...actor,role:'unknown'}},{...backupInput(output),scope:{changes:'latest'}},{resume:{operation_id:'missing',expected_observation:'sha256:'+'0'.repeat(64),action:'retry'},actor,reason:'Invalid mode'}]) {
    const rejected=command(root,['store','backup'],input);assert.equal(rejected.exit,2);assert.equal(rejected.result.errors[0].code,'invalid-request');
  }
  const nullStore=command(root,['store','restore'],{backup:output,expected_backup:'sha256:'+'0'.repeat(64),expected_store:null,replace:true,actor,reason:'Invalid absent expectation'});
  assert.equal(nullStore.exit,2);assert.equal(nullStore.result.errors[0].code,'invalid-request');assert.equal(existsSync(output),false);
  const saved=command(root,['store','backup'],backupInput(output));assert.equal(saved.exit,0,JSON.stringify(saved));
  const observation=command(root,['capabilities']);assert.equal(observation.result.store.state,'ready');
  const restore={backup:output,expected_backup:saved.result.maintenance.integrity,expected_store:{kind:'current',revision:'stale'},replace:true,actor,reason:'Explicit replacement'};
  const preview=command(root,['store','restore'],restore,['--dry-run']);assert.equal(preview.exit,3,JSON.stringify(preview));assert.equal(existsSync(join(root,'.rigorloop/maintenance/active.json')),false);
  writeFileSync(join(output,'attachments/navigation/report.txt'),'altered report bytes');
  const corrupt=command(root,['store','restore'],{...restore,expected_store:{kind:'current',revision:observation.result.store.revision}},['--dry-run']);assert.equal(corrupt.exit,3,JSON.stringify(corrupt));
});

test('maintenance replacement preserves prior bytes and unrelated runtime files',t=>{
  const {root}=setup(t),output=join(root,'backup');
  const saved=command(root,['store','backup'],backupInput(output));assert.equal(saved.exit,0,JSON.stringify(saved));
  writeFileSync(join(root,'.rigorloop/keep.txt'),'unrelated');
  const current=command(root,['capabilities']).result.store;
  const restored=command(root,['store','restore'],{backup:output,expected_backup:saved.result.maintenance.integrity,expected_store:{kind:'current',revision:current.revision},replace:true,actor,reason:'Exercise explicit whole-store replacement'});
  assert.equal(restored.exit,0,JSON.stringify(restored));assert.equal(existsSync(join(restored.result.maintenance.retained_prior,'rigorloop.db')),true);
  assert.equal(readFileSync(join(root,'.rigorloop/keep.txt'),'utf8'),'unrelated');assert.equal(existsSync(join(root,'.rigorloop/maintenance/active.json')),false);
});

test('interrupted replacement remains fenced and explicit finish resumes only the validated candidate',t=>{
  const {root}=setup(t),output=join(root,'backup');
  const saved=command(root,['store','backup'],backupInput(output));assert.equal(saved.exit,0,JSON.stringify(saved));
  const current=command(root,['capabilities']).result.store;
  const input={backup:output,expected_backup:saved.result.maintenance.integrity,expected_store:{kind:'current',revision:current.revision},replace:true,actor,reason:'Qualified interrupted replacement'};
  const injection=new URL('./helpers/operational-maintenance-crash.mjs',import.meta.url).href;
  const killed=spawnSync(process.execPath,['--import',injection,cli,'store','restore','--root',root,'--input','-','--format','json'],{input:JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input}),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_MAINTENANCE_CRASH:'candidate'}});
  assert.equal(killed.signal,'SIGKILL');assert.equal(invoke(root,['change','context']).exit,4);
  const state=command(root,['capabilities']).result.store;assert.equal(state.state,'maintenance');
  const resumed=command(root,['store','restore'],{resume:{operation_id:state.maintenance.operation_id,expected_observation:state.maintenance.observation,action:'finish'},actor,reason:'Finish the inspected candidate after interrupted owner exited'});
  assert.equal(resumed.exit,0,JSON.stringify(resumed));assert.equal(resumed.result.committed,true);
  assert.equal(invoke(root,['change','context']).exit,0);assert.equal(existsSync(join(resumed.result.maintenance.retained_prior,'rigorloop.db')),true);
});

test('interrupted replacement rollback restores prior bytes and rejects a stale recovery observation',t=>{
  const {root}=setup(t),output=join(root,'backup');
  const saved=command(root,['store','backup'],backupInput(output));const current=command(root,['capabilities']).result.store;
  const input={backup:output,expected_backup:saved.result.maintenance.integrity,expected_store:{kind:'current',revision:current.revision},replace:true,actor,reason:'Qualified rollback'};
  const injection=new URL('./helpers/operational-maintenance-crash.mjs',import.meta.url).href;
  const killed=spawnSync(process.execPath,['--import',injection,cli,'store','restore','--root',root,'--input','-','--format','json'],{input:JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input}),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_MAINTENANCE_CRASH:'candidate'}});assert.equal(killed.signal,'SIGKILL');
  const state=command(root,['capabilities']).result.store;
  const request={resume:{operation_id:state.maintenance.operation_id,expected_observation:state.observation,action:'rollback'},actor,reason:'Restore the exact observed prior state'};
  assert.equal(command(root,['store','restore'],{...request,resume:{...request.resume,expected_observation:'sha256:'+'0'.repeat(64)}}).exit,3);
  const result=command(root,['store','restore'],request);assert.equal(result.exit,0,JSON.stringify(result));assert.equal(result.result.committed,false);
  assert.equal(command(root,['capabilities']).result.store.revision,current.revision);
});

test('legacy import requires explicit dispositions, retains original approvals without promotion and exposes current work',t=>{
  const root=project(t),id='legacy-navigation',source=join(root,'docs/changes',id);mkdirSync(source,{recursive:true});mkdirSync(join(source,'reviews'));
  const original={schema_version:3,contract:'rigorloop-records-v3',change_id:id,proposal:{path:'requirements.md',identity:'sha256:'+'a'.repeat(64)},models:[],activity:{stage:'implement',status:'in-progress',owner:actor,reason:'Implement navigation'},plan:null,work:[{id:'navigation',status:'in-progress',owner:actor,requirement_refs:['SR-001']}],records:[{kind:'review',path:`docs/changes/${id}/reviews/old-review.json`}],applicability:[{path:`docs/changes/${id}/reviews/old-review.json`,value:'current',actor,reason:'Legacy judgment'}],blockers:[]};
  const oldReview={schema_version:3,change_id:id,id:'old-review',target:'proposal',reviewer:{id:'reviewer-old',role:'review'},contributors:[actor],independence_basis:'Independent legacy reviewer',subjects:[],judgment:'approved',findings:[],summary:'Legacy proposal accepted',assessment_scope:'Proposal direction',rationale:['The direction is coherent'],limitations:[]};
  const originalBytes=JSON.stringify(original,null,2)+'\n',reviewBytes=JSON.stringify(oldReview)+'\n';writeFileSync(join(source,'change.json'),originalBytes);writeFileSync(join(source,'reviews/old-review.json'),reviewBytes);
  const input={mode:'legacy-import',expected_store:{kind:'absent'},actor,reason:'Resume navigation implementation against the requirement-first basis',source_contract:'rigorloop-records-v3',source_root:root,changes:[id],expected_source:null,originals_output:join(root,'legacy-originals'),dispositions:[]};
  const preview=command(root,['store','migrate'],input,['--dry-run']);assert.equal(preview.exit,0,JSON.stringify(preview));assert.equal(existsSync(databasePath(root)),false);
  const scope=preview.result.maintenance.scope;
  const dispositions=scope.dispositions.map(d=>({source_record:d.source_record,action:d.allowed_target?'import':'retain',reason:d.allowed_target?'Preserve current work and its source attribution':'Retain original legacy judgment; no target approval inferred',target:d.allowed_target}));
  const result=command(root,['store','migrate'],{...input,expected_source:scope.source_observation,dispositions});assert.equal(result.exit,0,JSON.stringify(result));assert.equal(result.result.committed,true);
  assert.equal(readFileSync(join(source,'change.json'),'utf8'),originalBytes);assert.equal(readFileSync(join(input.originals_output,`docs/changes/${id}/reviews/old-review.json`),'utf8'),reviewBytes);
  const p=spawnSync(process.execPath,[cli,'change','context','--root',root,'--change',id,'--format','json'],{encoding:'utf8'});assert.equal(p.status,0,p.stdout+p.stderr);const handoff=JSON.parse(p.stdout).items[0].value;
  assert.equal(handoff.progress.work[0].id,'navigation');assert.deepEqual(handoff.review_standing.selected,[]);assert.ok(handoff.governing_basis.gaps.length);assert.deepEqual(handoff.intent_and_authority.authority.allowed,[]);
});

test('finish after interrupted terminal rollback releases the fence without reactivating candidate',t=>{
  const {root}=setup(t),output=join(root,'backup');const saved=command(root,['store','backup'],backupInput(output));const current=command(root,['capabilities']).result.store;
  const input={backup:output,expected_backup:saved.result.maintenance.integrity,expected_store:{kind:'current',revision:current.revision},replace:true,actor,reason:'Interrupted rollback qualification'};
  const injection=new URL('./helpers/operational-maintenance-crash.mjs',import.meta.url).href;
  const run=(input,point)=>spawnSync(process.execPath,['--import',injection,cli,'store','restore','--root',root,'--input','-','--format','json'],{input:JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input}),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_MAINTENANCE_CRASH:point}});
  assert.equal(run(input,'candidate').signal,'SIGKILL');
  let state=command(root,['capabilities']).result.store;
  const resume=(state,action)=>({resume:{operation_id:state.maintenance.operation_id,expected_observation:state.observation,action},actor,reason:'Resume the selected recovery decision'});
  assert.equal(run(resume(state,'rollback'),'rolled-back').signal,'SIGKILL');
  const retained=join(root,'.rigorloop/artifacts/changes/navigation/report.txt'),original=readFileSync(retained);
  writeFileSync(retained,Buffer.alloc(original.length,88));
  state=command(root,['capabilities']).result.store;
  const conflict=command(root,['store','restore'],resume(state,'finish'));
  assert.notEqual(conflict.exit,0);assert.equal(conflict.result.committed,false);
  assert.equal(command(root,['capabilities']).result.store.state,'maintenance');
  writeFileSync(retained,original);
  state=command(root,['capabilities']).result.store;
  const finished=command(root,['store','restore'],resume(state,'finish'));assert.equal(finished.exit,0,JSON.stringify(finished));assert.equal(finished.result.committed,false);
  assert.equal(command(root,['capabilities']).result.store.revision,current.revision);
});

test('restore cannot replace selected manifest identity with a later same-size source observation',t=>{
  const {root}=setup(t),output=join(root,'backup');
  const saved=command(root,['store','backup'],backupInput(output));assert.equal(saved.exit,0,JSON.stringify(saved));
  const destination=project(t);writeFileSync(join(destination,'.rigorloop.json'),readFileSync(join(root,'.rigorloop.json')));
  const input={backup:output,expected_backup:saved.result.maintenance.integrity,expected_store:{kind:'absent'},replace:false,actor,reason:'Selected original bytes only'};
  const injection=new URL('./helpers/operational-maintenance-fault.mjs',import.meta.url).href;
  const result=spawnSync(process.execPath,['--import',injection,cli,'store','restore','--root',destination,'--input','-','--format','json'],{input:JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input}),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_MAINTENANCE_FAULT:'recapture',RIGORLOOP_TEST_BACKUP_MEMBER:join(output,'attachments/navigation/report.txt')}});
  const receipt=JSON.parse(result.stdout);assert.notEqual(result.status,0);assert.equal(receipt.committed,false);
  assert.equal(existsSync(databasePath(destination)),false);
});

test('legacy source cleanup failure after activation preserves truthful commit and resumable fence',t=>{
  const root=project(t),id='legacy-cleanup',source=join(root,'docs/changes',id);mkdirSync(source,{recursive:true});
  writeFileSync(join(source,'change.json'),JSON.stringify({schema_version:3,contract:'rigorloop-records-v3',change_id:id,proposal:{path:'requirements.md',identity:'sha256:'+'a'.repeat(64)},models:[],activity:{stage:'implement',status:'in-progress',owner:actor,reason:'Authorized source'},plan:null,work:[],records:[],applicability:[],blockers:[]})+'\n');
  const input={mode:'legacy-import',expected_store:{kind:'absent'},actor,reason:'Import qualified original',source_contract:'rigorloop-records-v3',source_root:root,changes:[id],expected_source:null,originals_output:join(root,'originals'),dispositions:[]};
  const preview=command(root,['store','migrate'],input,['--dry-run']);assert.equal(preview.exit,0,JSON.stringify(preview));
  input.expected_source=preview.result.maintenance.scope.source_observation;
  input.dispositions=preview.result.maintenance.scope.dispositions.map(d=>({source_record:d.source_record,action:'import',reason:'Import current Change',target:d.allowed_target}));
  const injection=new URL('./helpers/operational-maintenance-fault.mjs',import.meta.url).href;
  const child=spawnSync(process.execPath,['--import',injection,cli,'store','migrate','--root',root,'--input','-','--format','json'],{input:JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input}),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_MAINTENANCE_FAULT:'legacy-cleanup'}});
  const receipt=JSON.parse(child.stdout);assert.notEqual(child.status,0);assert.equal(receipt.committed,true);
  assert.equal(receipt.maintenance.phase,'activated');
  const state=command(root,['capabilities']).result.store;assert.equal(state.state,'maintenance');
  assert.equal(state.maintenance.operation_id,receipt.maintenance.operation_id);
  const finished=command(root,['store','migrate'],{resume:{operation_id:state.maintenance.operation_id,expected_observation:state.observation,action:'finish'},actor,reason:'Complete source lock cleanup after failure'});
  assert.equal(finished.exit,0,JSON.stringify(finished));assert.equal(finished.result.committed,true);
  assert.equal(command(root,['capabilities']).result.store.state,'ready');
  assert.equal(existsSync(join(root,'.rigorloop/record-store',id,'lock')),false);
});


test('selected backup preview ignores excluded payloads but rejects missing selected payloads',t=>{
  const {root}=setup(t),output=join(root,'subset');
  const created=spawnSync(process.execPath,[cli,'change','create','--root',root,'--change','unselected','--input','-','--format','json'],{encoding:'utf8',input:JSON.stringify(createInput({change_id:'unselected'}))});
  assert.equal(created.status,0,created.stdout);
  unlinkSync(join(root,'.rigorloop/artifacts/changes/navigation/report.txt'));
  assert.notEqual(command(root,['store','backup'],backupInput(output),['--dry-run']).exit,0);
  const selected={...backupInput(output),scope:{changes:['unselected']}};
  assert.equal(command(root,['store','backup'],selected,['--dry-run']).exit,0);
  assert.equal(existsSync(output),false);
  assert.equal(command(root,['store','backup'],selected).exit,0);
});

test('resume rejects incompatible capture metadata before writes and reports uncertain activation honestly',t=>{
  const {root}=setup(t),output=join(root,'backup');
  const saved=command(root,['store','backup'],backupInput(output));
  const current=command(root,['capabilities']).result.store;
  const input={backup:output,expected_backup:saved.result.maintenance.integrity,expected_store:{kind:'current',revision:current.revision},replace:true,actor,reason:'Interrupted recovery admission'};
  const crash=new URL('./helpers/operational-maintenance-crash.mjs',import.meta.url).href;
  const killed=spawnSync(process.execPath,['--import',crash,cli,'store','restore','--root',root,'--input','-','--format','json'],{input:JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input}),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_MAINTENANCE_CRASH:'candidate'}});
  assert.equal(killed.signal,'SIGKILL');
  let state=command(root,['capabilities']).result.store;
  const operation=join(root,'.rigorloop/maintenance',state.maintenance.operation_id),path=join(operation,'manifest.json'),original=readFileSync(path),manifest=JSON.parse(original);
  const resume=state=>({resume:{operation_id:state.maintenance.operation_id,expected_observation:state.observation,action:'finish'},actor,reason:'Finish inspected recovery'});
  for(const patch of [{version:999},{id:'foreign'},{project_id:'foreign'},{task:'store.backup'},{phase:'unknown'},{phase:'activated'}]) {
    writeFileSync(path,JSON.stringify({...manifest,...patch}));
    state=command(root,['capabilities']).result.store;
    const rejected=command(root,['store','restore'],resume(state));
    assert.notEqual(rejected.exit,0,JSON.stringify(patch));
    assert.equal(existsSync(join(operation,'resume-exclusion.sqlite')),false);
    assert.equal(command(root,['capabilities']).result.store.observation,state.observation);
  }
  writeFileSync(path,original);state=command(root,['capabilities']).result.store;
  const injection=new URL('./helpers/operational-maintenance-fault.mjs',import.meta.url).href;
  const child=spawnSync(process.execPath,['--import',injection,cli,'store','restore','--root',root,'--input','-','--format','json'],{input:JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input:resume(state)}),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_MAINTENANCE_FAULT:'activation-receipt'}});
  const receipt=JSON.parse(child.stdout);
  assert.notEqual(child.status,0);assert.equal(receipt.committed,null);assert.equal(receipt.changed,null);
  assert.equal(receipt.maintenance.phase,'activated');assert.equal(invoke(root,['change','context']).exit,4);
  state=command(root,['capabilities']).result.store;
  const finished=command(root,['store','restore'],resume(state));
  assert.equal(finished.exit,0,JSON.stringify(finished));assert.equal(finished.result.committed,true);
});


test('manifest-absent recovery permits rollback while preserving the untouched store',t=>{
  const {root}=setup(t),revision=command(root,['capabilities']).result.store.revision;
  const injection=new URL('./helpers/operational-maintenance-crash.mjs',import.meta.url).href;
  const child=spawnSync(process.execPath,['--import',injection,cli,'store','backup','--root',root,'--input','-','--format','json'],{input:JSON.stringify({schema_version:1,interface:'store-maintenance-v1',input:backupInput(join(root,'backup'))}),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_MAINTENANCE_CRASH:'before-capture'}});
  assert.equal(child.signal,'SIGKILL');
  const state=command(root,['capabilities']).result.store;
  const input={resume:{operation_id:state.maintenance.operation_id,expected_observation:state.observation,action:'finish'},actor,reason:'Inspect capture interruption'};
  assert.notEqual(command(root,['store','backup'],input).exit,0);
  const fresh=command(root,['capabilities']).result.store;
  const result=command(root,['store','backup'],{...input,resume:{...input.resume,expected_observation:fresh.observation,action:'rollback'}});
  assert.equal(result.exit,0,JSON.stringify(result));assert.equal(result.result.committed,false);
  assert.equal(command(root,['capabilities']).result.store.revision,revision);
});
