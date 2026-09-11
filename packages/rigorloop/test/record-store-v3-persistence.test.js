import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,rmSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {executeRecordStore} from '../dist/lib/record-store.js';
import {executeRecordStoreCli} from '../dist/lib/record-store-cli.js';
import {digest} from '../dist/lib/record-store-files.js';
import {validateAdvancedResult} from '../dist/lib/record-store-format.js';
import {fixture,changeId,prefix,manifest,encode} from './helpers/v3-fixture.mjs';
function setup(t){const root=mkdtempSync(join(tmpdir(),'v3-store-'));t.after(()=>rmSync(root,{recursive:true,force:true}));mkdirSync(join(root,'docs/changes'),{recursive:true});return root;}
function run(root,operation,extra={},options={}){const r=executeRecordStore({root,changeId,operation,...extra},options);validateAdvancedResult(r);return r;}
function creation(){return {schema_version:2,contract:'rigorloop-records-v3',change_id:changeId,expected_revision:null,writes:Object.entries(fixture()).map(([path,content])=>({path,content,expected_identity:null})),reads:[]};}
function create(root){const req=creation();assert.equal(run(root,'record',{request:req}).status,'saved');return req;}
function update(root){const snapshot=run(root,'inspect');assert.equal(snapshot.status,'inspected');return {...creation(),expected_revision:snapshot.revision,writes:snapshot.snapshot.records.map(r=>({path:r.path,content:r.content,expected_identity:digest(r.content)}))};}
function edit(req,path,fn){const w=req.writes.find(w=>w.path===prefix+path),v=JSON.parse(w.content);fn(v);w.content=encode(v);}
function bytes(root,req){for(const w of req.writes)assert.equal(readFileSync(join(root,w.path),'utf8'),w.content);}
test('TG-02 v3 internal create and advanced inspect retain independent result version and exact bytes',t=>{
 const root=setup(t),req=create(root);bytes(root,req);const r=run(root,'inspect');assert.equal(r.schema_version,1);assert.equal(r.snapshot.records.length,5);
 const bad=structuredClone(r);bad.snapshot.records[0].content+=' ';assert.throws(()=>validateAdvancedResult(bad));
 const fresh=update(root);assert.equal(run(root,'record',{request:fresh}).status,'unchanged');assert.equal(run(root,'record',{request:req}).status,'conflict');
});
test('TG-02 public v3 creation stays unavailable before coordinated consumer adoption',t=>{
 const root=setup(t),r=executeRecordStoreCli(['record','--root',root,'--change',changeId,'--input','-','--format','json'],{input:encode(creation())});
 assert.equal(r.result.errors[0].code,'unsupported-contract');assert.equal(existsSync(join(root,manifest)),false);
});
for(const phase of ['after-preparation','after-replace:0','before-commit','after-commit'])for(const action of ['restore','complete'])test(`TG-02 v3 ${phase} interruption ${action} preserves prepared bytes`,t=>{
 const root=setup(t),before=create(root),req=update(root);edit(req,'reviews/final-code-review.json',r=>r.limitations=['Changed limitation']);edit(req,'verify-report.json',r=>r.summary='Changed final explanation');
 const stopped=run(root,'record',{request:req},{fault:p=>p===phase?'crash':undefined});assert.equal(stopped.status,'recovery-required');
 const journal=JSON.parse(readFileSync(join(root,'.rigorloop/record-store',changeId,'journal.json'),'utf8'));assert.equal(journal.version,3);
 const recovered=run(root,'recover',{transaction:stopped.transaction.id,expectedRecovery:stopped.transaction.recovery_identity,action});
 if(phase==='after-commit'&&action==='restore'){assert.equal(recovered.status,'recovery-required');bytes(root,req);}else{assert.equal(recovered.status,'recovered');bytes(root,action==='complete'?req:before);}
});
test('TG-02 unknown_value journal versions and mixed selector cannot recover',t=>{
 const root=setup(t);create(root);const req=update(root);edit(req,'verify-report.json',r=>r.limitations=['x']);const stopped=run(root,'record',{request:req},{fault:p=>p==='after-preparation'?'crash':undefined});
 const path=join(root,'.rigorloop/record-store',changeId,'journal.json'),original=JSON.parse(readFileSync(path,'utf8'));
 for(const version of [999,2]){const raw=encode({...original,version});writeFileSync(path,raw);const r=run(root,'recover',{transaction:stopped.transaction.id,expectedRecovery:digest(raw),action:'complete'});assert.equal(r.status,'recovery-required');}
});
test('TG-02 v3 declared basis conflict and third-state recovery never overwrite external edits',t=>{
 const root=setup(t),before=create(root),req=update(root);edit(req,'verify-report.json',r=>r.summary='new');writeFileSync(join(root,'basis'),'now');req.reads=[{path:'basis',expected_identity:digest('before')}];assert.equal(run(root,'record',{request:req}).status,'conflict');bytes(root,before);
 req.reads=[];const s=run(root,'record',{request:req},{fault:p=>p==='after-preparation'?'crash':undefined});writeFileSync(join(root,manifest),'external content\n');const r=run(root,'recover',{transaction:s.transaction.id,expectedRecovery:s.transaction.recovery_identity,action:'restore'});assert.equal(r.status,'recovery-required');assert.equal(readFileSync(join(root,manifest),'utf8'),'external content\n');
});
