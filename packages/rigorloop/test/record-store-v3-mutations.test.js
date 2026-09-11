import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,rmSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {executeRecordStore} from '../dist/lib/record-store.js';
import {executeRecordingMutationCli} from '../dist/lib/recording-mutation-cli.js';
import {validatePrimaryResult,validate,RECORDING_SCHEMA} from '../dist/lib/recording-contract.js';
import {validateMutationRequest} from '../dist/lib/recording-construction.js';
import {fixture,changeId,prefix,manifest,encode} from './helpers/v3-fixture.mjs';
const reviewPath=prefix+'reviews/final-code-review.json',verifyPath=prefix+'verify-report.json';
function setup(t,create=true){const root=mkdtempSync(join(tmpdir(),'v3-mutation-'));t.after(()=>rmSync(root,{recursive:true,force:true}));mkdirSync(join(root,'docs/changes'),{recursive:true});if(create){const r=executeRecordStore({root,changeId,operation:'record',request:{schema_version:2,contract:'rigorloop-records-v3',change_id:changeId,expected_revision:null,reads:[],writes:Object.entries(fixture()).map(([path,content])=>({path,content,expected_identity:null}))}});assert.equal(r.status,'saved');}return root;}
const snapshot=root=>executeRecordStore({root,changeId,operation:'inspect'});
const stored=(root,path)=>JSON.parse(readFileSync(join(root,path),'utf8'));
function request(root,operation,override={}){return{schema_version:1,interface:'targeted-recording-v1',contract:'rigorloop-records-v3',change_id:changeId,expected_revision:snapshot(root).revision,reads:[],operation,...override};}
function run(root,operation,override={},flags=[]){const batch=Array.isArray(operation),req=request(root,operation,override);if(batch){delete req.operation;req.operations=operation;}
 const argv=batch?['batch']:operation.op.split('.');if(!batch&&operation.target.id)argv.push(operation.target.id);if(!batch&&operation.target.review)argv.push('--review',operation.target.review);
 const result=executeRecordingMutationCli([...argv,'--root',root,'--change',changeId,'--input','-','--format','json',...flags],{input:encode(req)});validatePrimaryResult(result.result);return result;
}
const set=(kind,values)=>({op:kind+'.set',target:kind==='review'?{id:'final-code-review'}:{},values});
const values=(record)=>Object.fromEntries(Object.entries(record).filter(([k])=>!['schema_version','change_id','id','findings'].includes(k)));
for(const kind of ['review','verify'])test(`TG-04 ${kind}.set selector errors use schema3 before any input or filesystem access`,()=>{
 for(const extra of [['--unknown','private'],['--change',changeId],['--format','bad']]){let read=false;const argv=[kind,'set',...(kind==='review'?['final-code-review']:[]),'--root','/does-not-exist','--change',changeId,'--input','-','--format','json',...extra];const r=executeRecordingMutationCli(argv,{readInput:()=>{read=true;throw Error('read');}});assert.equal(read,false);assert.equal(r.result.schema_version,3);assert.equal(r.result.operation,kind+'.set');assert.equal(r.result.errors[0].code,'invalid-input');assert.equal('change_id' in r.result,extra[0]!=='--change');assert.doesNotMatch(r.json,/private/);}
});
for(const kind of ['review','verify'])test(`TG-04 ${kind}.set missing v2 unknown and mixed stores reject through new interface`,t=>{
 const root=setup(t,false);const op=set(kind,{limitations:[]});const requestRevision='sha256:'+'b'.repeat(64);
 const absent=run(root,op,{expected_revision:requestRevision});assert.equal(absent.result.schema_version,3);assert.equal(absent.result.errors[0].code,'target-not-found');assert.equal(existsSync(join(root,manifest)),false);
 mkdirSync(join(root,prefix),{recursive:true});
 for(const object of [{schema_version:2,contract:'rigorloop-records-v2'},{schema_version:3,contract:'unknown_value'}]){const change=JSON.parse(fixture()[manifest]);Object.assign(change,object);writeFileSync(join(root,manifest),encode(change));const r=run(root,op,{expected_revision:requestRevision});assert.equal(r.result.schema_version,3);assert.equal(r.result.errors[0].code,'unsupported-contract');assert.equal('record_contract' in r.result,false);}
 const v2=run(root,op,{contract:'rigorloop-records-v2',expected_revision:requestRevision});assert.equal(v2.result.errors[0].code,'unsupported-contract');
});
test('TG-03 narrow edits preserve neighbor bytes and semantic no-ops preserve all files',t=>{
 const root=setup(t),before=readFileSync(join(root,reviewPath),'utf8'),original=stored(root,reviewPath),manifestBefore=readFileSync(join(root,manifest));
 const text='Named reason\n\n```text\nA → B\\n\n```';const r=run(root,set('review',{summary:text}));assert.equal(r.result.status,'saved');assert.equal(r.result.schema_version,3);assert.equal(readFileSync(join(root,reviewPath),'utf8'),before.replace(JSON.stringify(original.summary),JSON.stringify(text)));assert.deepEqual(readFileSync(join(root,manifest)),manifestBefore);
 const unchanged=readFileSync(join(root,reviewPath));assert.equal(run(root,set('review',{summary:text})).result.status,'unchanged');assert.deepEqual(readFileSync(join(root,reviewPath)),unchanged);
 const retry=run(root,set('review',{summary:'stale'}),{expected_revision:r.result.revision.replace(/.$/,'0')});assert.equal(retry.result.status,'conflict');assert.equal(retry.result.schema_version,3);
});
test('TG-03 unknown_value explanation members empty and null inputs reject without storing',t=>{
 const root=setup(t),before=readFileSync(join(root,reviewPath));assert.equal(run(root,set('review',{})).result.errors[0].code,'invalid-input');for(const v of [{},{summary:''},{assessment_scope:' \n'},{rationale:[]},{limitations:null},{body:'bad'},{judgment:'approved'},{unknown_value:[]},{changes:['wrong kind']}]){const r=run(root,set('review',v));assert.equal(r.result.status,'rejected');assert.deepEqual(readFileSync(join(root,reviewPath)),before);}
 assert.equal(run(root,set('review',{limitations:[]})).result.status,'saved');
 const op=set('review',{summary:'x'});op.target.id='missing';assert.equal(run(root,op).result.errors[0].code,'target-not-found');
});
test('TG-03 complete Verify adds and removes conditional basis without rewriting unrelated bytes',t=>{
 const root=setup(t),initial=stored(root,verifyPath),basis=JSON.parse(readFileSync(new URL('../../../docs/design/record-format/examples/v3-verify-limitations-update/before.json',import.meta.url))).verification_basis;
 const r=run(root,{op:'verify.record',target:{},values:{...values(initial),verification_basis:basis}});assert.equal(r.result.status,'saved');assert.deepEqual(stored(root,verifyPath).verification_basis,basis);
 assert.equal(run(root,set('verify',{verification_basis:basis})).result.status,'rejected');
 const current=stored(root,verifyPath);delete current.verification_basis;assert.equal(run(root,{op:'verify.record',target:{},values:values(current)}).result.status,'saved');assert.deepEqual(stored(root,verifyPath),initial);
});
test('TG-03 explicit finding edits and complete review replacement preserve their separate targets',t=>{
 const root=setup(t),f=JSON.parse(readFileSync(new URL('../../../docs/design/record-format/examples/v3-finding-correction/stored-review.json',import.meta.url))).findings[0],target={review:'final-code-review',id:f.id},fv={...f};delete fv.id;
 assert.equal(run(root,{op:'finding.add',target,values:fv}).result.status,'saved');const before=stored(root,reviewPath);
 assert.equal(run(root,{op:'review.record',target:{id:'final-code-review'},values:{...values(before),summary:'Updated explanation'}}).result.status,'saved');assert.deepEqual(stored(root,reviewPath).findings,before.findings);
 assert.equal(run(root,{op:'finding.set',target,values:{evidence:'More precise',reporter:{id:'corrected-reporter',role:'review'}}}).result.status,'saved');assert.equal(stored(root,reviewPath).summary,'Updated explanation');
 for(const v of [{id:'renamed'},{origin:{}},{basis:{}},{state:'resolved'}])assert.equal(run(root,{op:'finding.set',target,values:v}).result.status,'rejected');
 assert.equal(run(root,{op:'finding.set',target,values:{state:'resolved',resolution:{actor:f.reporter,rationale:'Withdraw mistaken report',evidence_refs:[]}}}).result.status,'saved');
});
test('TG-03 batch separates explanation fields findings and explicit applicability',t=>{
 const root=setup(t),app={op:'applicability.set',target:{path:reviewPath},values:{value:'stale',actor:{id:'reviewer-a',role:'review'},reason:'Scope clarified'}};
 assert.equal(run(root,[set('review',{summary:'Changed'}),set('review',{limitations:[]}),app]).result.status,'saved');assert.equal(stored(root,manifest).applicability.find(a=>a.path===reviewPath).value,'stale');
 for(const ops of [[set('review',{summary:'a'}),set('review',{summary:'a'})],[{op:'review.record',target:{id:'final-code-review'},values:values(stored(root,reviewPath))},set('review',{limitations:[]})]])assert.equal(run(root,ops).result.errors[0].code,'overlapping-operation');
});
test('TG-04 schema2 retains closed operations and early batch errors keep the batch tag',()=>{
 for(const operation of ['review.set','verify.set'])assert.throws(()=>validatePrimaryResult({schema_version:2,operation,status:'rejected',claim:'storage-only',errors:[{code:'invalid-input',message:'safe'}]}));
 const r=executeRecordingMutationCli(['batch','--root','/does-not-exist','--change',changeId,'--input','-','--format','json'],{input:'bad\n'});assert.equal(r.result.schema_version,2);assert.equal(r.result.operation,'batch');
});
test('TG-03 preview and stale decision-basis reads never write; retained operations dispatch after validation',t=>{
 const root=setup(t),before=readFileSync(join(root,reviewPath)),op=set('review',{summary:'Preview reason'});
 const preview=run(root,op,{},['--dry-run','--details']);assert.equal(preview.result.status,'valid');assert.equal(preview.result.schema_version,3);assert.notEqual(preview.result.revision,preview.result.candidate_revision);assert.deepEqual(readFileSync(join(root,reviewPath)),before);
 const stale=run(root,op,{reads:[{path:'README.md',identity:'sha256:'+'a'.repeat(64)}]});assert.equal(stale.result.status,'conflict');assert.deepEqual(readFileSync(join(root,reviewPath)),before);
 const record={op:'review.record',target:{id:'final-code-review'},values:values(stored(root,reviewPath))};
 assert.equal(run(root,record,{expected_revision:'sha256:'+'a'.repeat(64)}).result.schema_version,3);
 const invalid={...record,values:{...record.values,summary:''}};assert.equal(run(root,invalid).result.schema_version,2);
});
test('TG-03 new complete supporting records require all explanation and applicability inputs',t=>{
 const root=setup(t),record=stored(root,reviewPath),op={op:'review.record',target:{id:'another-review'},values:values(record)};
 assert.equal(run(root,op).result.errors[0].code,'missing-input');
 op.applicability={value:'current',actor:record.reviewer,reason:'Explicit assessment scope'};
 assert.equal(run(root,op).result.status,'saved');assert.deepEqual(stored(root,prefix+'reviews/another-review.json').findings,[]);
 const complete=readFileSync(join(root,prefix+'reviews/another-review.json'));assert.equal(run(root,op).result.status,'unchanged');assert.deepEqual(readFileSync(join(root,prefix+'reviews/another-review.json')),complete);
});
