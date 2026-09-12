import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtempSync,mkdirSync,readFileSync,rmSync,readdirSync,writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {executeRecordStore} from '../dist/lib/record-store.js';
import {executeRecordingQueryCli} from '../dist/lib/recording-query-cli.js';
import {validateMutationRequest} from '../dist/lib/recording-construction.js';
import {validatePrimaryResult} from '../dist/lib/recording-contract.js';
import {executeWorkflowContext} from '../dist/lib/workflow-context.js';
import {fixture,changeId,prefix,encode} from './helpers/v3-fixture.mjs';
const reviewPath=prefix+'reviews/final-code-review.json',verifyPath=prefix+'verify-report.json';
function setup(t,edit=()=>{}){const root=mkdtempSync(join(tmpdir(),'v3-reads-'));t.after(()=>rmSync(root,{recursive:true,force:true}));mkdirSync(join(root,'docs/changes'),{recursive:true});const files=fixture(),records=Object.fromEntries(Object.entries(files).map(([p,s])=>[p,JSON.parse(s)]));edit(records);const result=executeRecordStore({root,changeId,operation:'record',request:{schema_version:2,contract:'rigorloop-records-v3',change_id:changeId,expected_revision:null,reads:[],writes:Object.entries(records).map(([path,r])=>({path,content:encode(r),expected_identity:null}))}});assert.equal(result.status,'saved');return{root,records};}
function read(root,kind='review',flags=[],input){const argv=kind==='context'?['context','--input','-']:kind==='status'?['status']:[kind,'show',...(kind==='review'?['final-code-review']:kind==='finding'?['example-finding','--review','final-code-review']:[])];return executeRecordingQueryCli([...argv,'--root',root,'--change',changeId,'--format','json',...flags],input?{input:encode(input)}:{});}
const item=r=>r.result.data.items[0];
test('TG-05 complete and projected assessments retain identity applicability and exact content',t=>{
 const {root,records}=setup(t),before=readFileSync(join(root,reviewPath));const full=read(root);assert.equal(full.result.schema_version,3);assert.deepEqual(item(full).fields,records[reviewPath]);assert.equal(item(full).applicability.value,'current');assert.deepEqual(full.result.scope.absent_fields,[]);
 const selected=read(root,'review',['--fields','rationale,limitations']);assert.deepEqual(item(selected).fields,{limitations:records[reviewPath].limitations,rationale:records[reviewPath].rationale});assert.deepEqual(selected.result.scope.fields,['limitations','rationale']);assert.deepEqual(selected.result.scope.omitted_fields,[{kind:'review',fields:Object.keys(records[reviewPath]).filter(k=>!['rationale','limitations'].includes(k)).sort()}]);assert.equal(selected.result.scope.complete,true);assert.deepEqual(readFileSync(join(root,reviewPath)),before);
 const v=read(root,'verify',['--fields','verification_basis,changes']);assert.deepEqual(v.result.scope.absent_fields,['verification_basis']);assert.deepEqual(item(v).fields,{changes:records[verifyPath].changes});assert.equal('verification_basis' in item(v).fields,false);
 assert.deepEqual(read(root,'verify').result.scope.absent_fields,['verification_basis']);
});
test('TG-05 unknown_value projection selectors fail closed before repository access',()=>{
 for(const flags of [['--fields','unknown_value'],['--fields','summary,summary'],['--fields',''],['--fields','summary, limitations'],['--fields','rationale[0]'],['--fields','changes'],['--fields','summary','--fields','rationale']]){const r=read('/missing','review',flags);assert.equal(r.result.schema_version,2);assert.equal(r.result.errors[0].code,'invalid-input');}
 assert.equal(read('/missing','context',['--fields','summary']).result.errors[0].code,'invalid-input');
});
test('TG-05 v3 findings have exact full and summary shapes; context explanation omissions are honest',t=>{
 const finding={id:'example-finding',reporter:{id:'reviewer',role:'review'},owner:{id:'implementer',role:'implement'},subjects:[],evidence:'Current observation',required_outcome:'Correct it',state:'open',resolution:null};
 const {root,records}=setup(t,r=>{r[reviewPath].findings=[finding];});const full=read(root,'finding');assert.deepEqual(item(full).fields,finding);assert.equal('origin_available' in item(full),false);assert.equal('absent_fields' in full.result.scope,false);
 const query={schema_version:1,detail:'summary',select:[{kind:'finding',where:{}},{kind:'review',where:{}},{kind:'verify',where:{}}]};const summary=read(root,'context',[],query);assert.equal(summary.result.schema_version,3);assert.deepEqual(summary.result.scope.omitted_fields.find(x=>x.kind==='finding').fields,['evidence','resolution']);assert.equal('origin_available' in summary.result.data.items.find(x=>x.kind==='finding'),false);assert.ok(summary.result.scope.omitted_fields.find(x=>x.kind==='verify').fields.includes('verification_basis'));
 const context=read(root,'context',[],{...query,detail:'full'});const review=context.result.data.items.find(x=>x.kind==='review');assert.deepEqual(review.fields.rationale,records[reviewPath].rationale);assert.equal('findings' in review.fields,false);assert.equal('absent_fields' in context.result.scope,false);assert.equal(read(root,'status').result.schema_version,3);
});
test('TG-05 v3 response validation rejects dishonest projection and unknown_value fields',t=>{
 const {root}=setup(t),r=read(root,'review',['--fields','summary']).result;
 for(const edit of [x=>{x.data.items[0].fields.unknown_value='bad';},x=>{x.scope.fields=['rationale'];},x=>{x.scope.omitted_fields=[];},x=>{x.scope.absent_fields=['summary'];},x=>{delete x.data.items[0].applicability;}]){const changed=structuredClone(r);edit(changed);assert.throws(()=>validatePrimaryResult(changed));}
});
test('TG-05 readable selected output preserves paragraphs literal escapes and array order within exact byte limits',t=>{
 const reason='First paragraph\n\n```text\n  A → B\\n\n```\nLast paragraph';const {root}=setup(t,r=>{r[reviewPath].rationale=[reason,'Second reason'];r[reviewPath].limitations=[];});
 const flags=['--fields','rationale,limitations'];const output=read(root,'review',flags);assert.match(output.human,/Selected fields/);assert.match(output.human,/Rationale:/);assert.match(output.human,/No listed limitations/);assert.ok(output.human.includes('A → B\\n'));assert.ok(output.human.indexOf('First paragraph')<output.human.indexOf('Second reason'));assert.deepEqual(item(output).fields.rationale,[reason,'Second reason']);
 const {root:large}=setup(t,r=>{r[reviewPath].summary='é'.repeat(5000);});for(const format of ['json','text']){const r=read(large,'review',['--fields','summary']);const bytes=Buffer.byteLength(format==='json'?r.json:r.human);const args=['review','show','final-code-review','--root',large,'--change',changeId,'--format',format,'--fields','summary','--max-bytes',String(bytes)];assert.equal(executeRecordingQueryCli(args).result.status,'inspected');args[args.length-1]=String(bytes-1);assert.equal(executeRecordingQueryCli(args).result.errors[0].code,'limit-exceeded');}
});
test('TG-05 factual discovery admits validated v3 stores without changing discovery response version',t=>{
 const {root}=setup(t);const r=executeWorkflowContext(['--change',changeId,'--format','json'],{cwd:root});assert.equal(r.result.status,'success');assert.equal(r.result.schema_version,2);assert.equal(r.result.candidates[0].record_contract,'rigorloop-records-v3');
});

test('TG-05 approved v3 request and response examples conform to executable profiles',()=>{
 const base=new URL('../../../docs/design/cli/examples/',import.meta.url);
 for(const dir of readdirSync(base).filter(n=>n.startsWith('v3-')))for(const name of readdirSync(new URL(dir+'/',base)).filter(n=>n.endsWith('.json')&&!n.includes('v2-store'))){
  const value=JSON.parse(readFileSync(new URL(dir+'/'+name,base)));
  if(value.interface==='targeted-recording-v1')assert.doesNotThrow(()=>validateMutationRequest(value,!!value.operations),dir+'/'+name);
  else if(value.operation&&value.status)assert.doesNotThrow(()=>validatePrimaryResult(value),dir+'/'+name);
 }
});

test('TG-05 retained blocker origins remain readable and contribute to observation freshness',t=>{
 const blocker=JSON.parse(readFileSync(new URL('../../../tests/fixtures/rigorloop-records-v3/records.json',import.meta.url))).change.blockers[0];blocker.resolution.evidence_refs=[];blocker.origin.subjects=[{path:'origin-only.txt',identity:'sha256:'+'a'.repeat(64)}];
 const {origin,...finding}=structuredClone(blocker);finding.subjects=[{path:'current-only.txt',identity:'sha256:'+'b'.repeat(64)}];
 const {root}=setup(t,r=>{r[prefix+'change.json'].blockers=[blocker];r[reviewPath].findings=[finding];});
 const full=executeRecordingQueryCli(['blocker','show',blocker.id,'--root',root,'--change',changeId,'--format','json']);assert.equal(item(full).origin_available,true);assert.deepEqual(item(full).fields.origin,blocker.origin);
 const summary=read(root,'context',[],{schema_version:1,detail:'summary',select:[{kind:'blocker',where:{}}]});assert.equal(item(summary).origin_available,true);assert.ok(summary.result.scope.omitted_fields[0].fields.includes('origin'));
 const before=read(root,'status').result;writeFileSync(join(root,'origin-only.txt'),'changed externally');const after=read(root,'status').result;assert.equal(before.revision,after.revision);assert.notEqual(before.observation_summary.observation_identity,after.observation_summary.observation_identity);writeFileSync(join(root,'current-only.txt'),'current finding subject changed');const current=read(root,'status').result;assert.equal(current.revision,after.revision);assert.notEqual(current.observation_summary.observation_identity,after.observation_summary.observation_identity);
});

test('TG-05 v3 context retains nullable upstream links without treating them as explanation objects',t=>{
 const {root}=setup(t,r=>{r[prefix+'change.json'].plan=null;});
 const response=read(root,'context',[],{schema_version:1,select:[{kind:'proposal',where:{}},{kind:'plan',where:{}},{kind:'activity',where:{}}]});assert.equal(response.result.status,'inspected');assert.equal(response.result.data.items.find(x=>x.kind==='plan').fields,null);
});
