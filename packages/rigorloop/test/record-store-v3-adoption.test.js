import assert from 'node:assert/strict';
import {test} from 'node:test';
import {spawnSync} from 'node:child_process';
import {mkdtempSync,mkdirSync,readFileSync,rmSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {executeRecordingMutationCli} from '../dist/lib/recording-mutation-cli.js';
import {executeRecordStore} from '../dist/lib/record-store.js';
import {fixture,changeId,prefix,manifest,encode} from './helpers/v3-fixture.mjs';
const cli=new URL('../dist/bin/rigorloop.js',import.meta.url).pathname;
function rootFor(t){const root=mkdtempSync(join(tmpdir(),'v3-adoption-'));t.after(()=>rmSync(root,{recursive:true,force:true}));mkdirSync(join(root,'docs/changes'),{recursive:true});return root;}
function call(root,words,input,expected=0){const r=spawnSync(process.execPath,[cli,...words,'--root',root,'--change',changeId,'--format','json',...(input?['--input','-']:[])],{input:input?encode(input):undefined,encoding:'utf8',maxBuffer:16*1024*1024});assert.equal(r.status,expected,r.stdout+r.stderr);return JSON.parse(r.stdout);}
const createValues=()=>Object.fromEntries(Object.entries(JSON.parse(fixture()[manifest])).filter(([k])=>!['schema_version','contract','change_id','records','applicability'].includes(k)));
const envelope=(operation,revision=null,contract='rigorloop-records-v3')=>({schema_version:1,interface:'targeted-recording-v1',contract,change_id:changeId,expected_revision:revision,reads:[],operation});
test('TG-07 public creation selects v3 and new v2 creation rejects without changing an absent store',t=>{
 for(const contract of ['rigorloop-records-v2','rigorloop-records-v3']){const root=rootFor(t),request=envelope({op:'change.create',target:{},values:createValues()},null,contract);const r=call(root,['change','create'],request,contract.endsWith('v2')?2:0);if(contract.endsWith('v2')){assert.equal(r.errors[0].code,'unsupported-contract');assert.equal(existsSync(join(root,manifest)),false);}else{assert.equal(r.schema_version,3);assert.equal(r.status,'saved');assert.equal(call(root,['status']).record_contract,contract);}}
});
test('TG-FINAL-01 public advanced v3 creation and named updates share the adopted candidate boundary',t=>{
 const root=rootFor(t),files=fixture(),advanced={schema_version:2,contract:'rigorloop-records-v3',change_id:changeId,expected_revision:null,reads:[],writes:Object.entries(files).map(([path,content])=>({path,content,expected_identity:null}))};
 const saved=call(root,['record-store','record'],advanced);assert.equal(saved.schema_version,1);assert.equal(saved.status,'saved');
 const before=call(root,['verify','show']);const op={op:'verify.set',target:{},values:{limitations:['Only the explicitly supplied evidence is assessed.']}};const changed=call(root,['verify','set'],envelope(op,before.revision));assert.equal(changed.schema_version,3);assert.equal(changed.status,'saved');
 const selected=call(root,['verify','show','--fields','limitations']);assert.deepEqual(selected.data.items[0].fields,op.values);assert.equal(selected.scope.complete,true);assert.ok(selected.scope.omitted_fields.length);assert.deepEqual(selected.data.items[0].applicability,before.data.items[0].applicability);
 const stale=call(root,['verify','set'],envelope(op,before.revision),3);assert.equal(stale.status,'conflict');assert.equal(call(root,['verify','set'],envelope(op,changed.revision)).status,'unchanged');
 const validation=spawnSync(process.execPath,[new URL('../../../scripts/validate-record-store.mjs',import.meta.url).pathname,join(root,manifest)],{encoding:'utf8'});assert.equal(validation.status,0,validation.stderr);
});
test('TG-07 public advanced v2 creation is rejected while its contract stays available for existing stores',t=>{
 const root=rootFor(t),change=JSON.parse(fixture()[manifest]);change.schema_version=2;change.contract='rigorloop-records-v2';change.records=[];change.applicability=[];
 const r=call(root,['record-store','record'],{schema_version:2,contract:'rigorloop-records-v2',change_id:changeId,expected_revision:null,reads:[],writes:[{path:manifest,expected_identity:null,content:encode(change)}]},2);assert.equal(r.errors[0].code,'unsupported-contract');assert.equal(existsSync(join(root,manifest)),false);
});

for(const phase of ['after-preparation','after-replace:0','before-commit','after-commit'])for(const action of ['restore','complete'])test(`TG-06 v3 targeted batch ${phase} recovery ${action} retains explicit assessment values`,t=>{
 const root=rootFor(t),files=fixture();const saved=executeRecordStore({root,changeId,operation:'record',request:{schema_version:2,contract:'rigorloop-records-v3',change_id:changeId,expected_revision:null,reads:[],writes:Object.entries(files).map(([path,content])=>({path,content,expected_identity:null}))}});assert.equal(saved.status,'saved');
 const request=envelope(undefined,saved.revision);delete request.operation;request.operations=[{op:'review.set',target:{id:'final-code-review'},values:{limitations:['Updated review limitation']}},{op:'verify.set',target:{},values:{limitations:['Updated Verify limitation']}}];
 const result=executeRecordingMutationCli(['batch','--root',root,'--change',changeId,'--input','-','--format','json'],{input:encode(request),fault:p=>p===phase?'crash':undefined}).result;assert.equal(result.status,'recovery-required');assert.equal(result.schema_version,3);
 const transaction=result.transaction;const recovered=call(root,['record-store','recover','--transaction',transaction.id,'--expected-recovery',transaction.recovery_identity,'--action',action],undefined,phase==='after-commit'&&action==='restore'?5:0);
 if(phase==='after-commit'&&action==='restore'){assert.equal(recovered.status,'recovery-required');return;}
 assert.equal(recovered.status,'recovered');
 if(action==='restore')for(const [path,content]of Object.entries(files))assert.equal(readFileSync(join(root,path),'utf8'),content);
 else{assert.deepEqual(call(root,['review','show','final-code-review','--fields','limitations']).data.items[0].fields.limitations,['Updated review limitation']);assert.deepEqual(call(root,['verify','show','--fields','limitations']).data.items[0].fields.limitations,['Updated Verify limitation']);call(root,['batch'],request,3);}
});
