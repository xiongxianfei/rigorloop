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
