import {executeRecordStore} from '../dist/lib/record-store.js';
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,readFileSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {digest} from '../dist/lib/record-store-files.js';
const cli=new URL('../dist/bin/rigorloop.js',import.meta.url).pathname;
const fixture=JSON.parse(readFileSync(new URL('../../../tests/fixtures/rigorloop-records-v2/records.json',import.meta.url)));
const prefix='docs/changes/example/';
const encode=x=>JSON.stringify(x)+'\n';
const actor=(id,role)=>({id,role});
const implementer=actor('implementer','implement'),verifier=actor('verifier','verify'),reviewer=actor('independent','review');
for(const contract of ['rigorloop-records-v2'])test(`TG-FINAL-01 public correction, recovery and explanation: ${contract}`,t=>{
 const root=mkdtempSync(join(tmpdir(),'recording-adoption-'));t.after(()=>rmSync(root,{recursive:true,force:true}));mkdirSync(join(root,'docs/changes'),{recursive:true});
 const mp=prefix+'change.json',ep=prefix+'evidence.json',rp=prefix+'reviews/final-review.json';
 writeFileSync(join(root,'basis'),'A\n');let subject={path:'basis',identity:digest('A\n')},revision=null;
 function call(words,payload,extra=[],expected=0){const args=[...words,'--root',root,...(words[0]==='subject'?[]:['--change','example']),'--format','json',...(payload?['--input','-']:[]),...extra];const r=spawnSync(process.execPath,[cli,...args],{input:payload?encode(payload):undefined,encoding:'utf8',maxBuffer:16*1024*1024});assert.equal(r.status,expected,r.stdout+r.stderr);const result=JSON.parse(r.stdout);assert.equal(result.claim,'storage-only');return result;}
 const app=who=>({value:'current',actor:who,reason:'Explicit actor assessment for this test.'});
 function request(operations,expected=revision){return{schema_version:1,interface:'targeted-recording-v1',contract,change_id:'example',expected_revision:expected,reads:[subject],...(Array.isArray(operations)?{operations}:{operation:operations})};}
 function words(op){return Array.isArray(op)?['batch']:[...op.op.split('.'),...(op.target.id?[op.target.id]:[])];}
 function mutate(op){const r=call(words(op),request(op));assert.equal(r.status,'saved');assert.ok(Buffer.byteLength(encode(r))<65536);if(r.observation_summary)assert.equal(r.observation_summary.details_included,false);revision=r.revision;return r;}
 const initial={proposal:subject,models:[],activity:{stage:'verify',status:'completed',owner:verifier,reason:'An earlier explicit completion.'},plan:null,work:[{id:'work-1',status:'completed',owner:implementer,requirement_refs:['CLI-SR-07']}],blockers:[]};
 const historical={schema_version:2,contract,change_id:'example',...initial,records:[],applicability:[]};assert.equal(executeRecordStore({root,changeId:'example',operation:'record',request:{schema_version:2,contract,change_id:'example',expected_revision:null,reads:[],writes:[{path:mp,expected_identity:null,content:encode(historical)}]}}).status,'saved');
 const context=call(['context'],{schema_version:1,select:[{kind:'activity',where:{}},{kind:'work',where:{ids:['work-1']}}]});assert.equal(context.record_contract,contract);revision=context.revision;
 const inspected=call(['subject','inspect'],undefined,['--path','basis','--content','full']);assert.deepEqual(inspected.data.subjects,[subject]);
 const failed={op:'evidence.record',target:{id:'failed-check'},values:{actor:verifier,subjects:[subject],result:'failed',procedure:'Observe the interrupted correction fixture.',summary:'Required result failed.'},applicability:app(verifier)};
 const blocker={op:'blocker.add',target:{id:'defect'},values:{reporter:verifier,owner:implementer,subjects:[subject],evidence:'The check failed after recorded completion.',required_outcome:'Demonstrate correction with a current passing check.',state:'open',resolution:null,basis:{rationale:'Failure requires correction.',supporting_judgment:null}}};
 const beforeFailure=revision;assert.ok(mutate([failed,blocker]).observation_summary.total>0);assert.equal(call(['status']).data.activity.status,'completed');
 call(['batch'],request([failed,blocker],beforeFailure),[],3);
 mutate({op:'activity.set',target:{},values:{stage:'implement',status:'in-progress',owner:implementer,reason:'Route explicitly selects correction.'}});
 const corrected={op:'evidence.record',target:{id:'corrected-check'},values:{actor:implementer,subjects:[subject],result:'passed',procedure:'Re-run the exact failed check after correction.',summary:'Required outcome observed.'}};
 // Interrupt a real public batch dispatcher, then recover through the public
 // maintenance command. No production fault flag is exposed.
 const batch=[{op:'work.set',target:{id:'work-1'},values:{status:'in-progress'}},corrected],payload=request(batch),launcher=join(root,'interrupt.mjs');
 writeFileSync(launcher,`import {main} from ${JSON.stringify(new URL('../dist/bin/rigorloop.js',import.meta.url).href)}; await main(process.argv.slice(2),{recordStoreOptions:{fault:p=>{if(p==='after-replace:0')process.exit(99);}}});\n`);
 const interrupted=spawnSync(process.execPath,[launcher,'batch','--root',root,'--change','example','--input','-','--format','json'],{input:encode(payload),encoding:'utf8'});assert.equal(interrupted.status,99,interrupted.stdout+interrupted.stderr);assert.equal(interrupted.stdout,'');
 const blocked=call(['context'],{schema_version:1,select:[{kind:'work',where:{}}]},[],5);assert.equal(blocked.data,undefined);assert.equal(blocked.status,'recovery-required');
 const tx=blocked.transaction;assert.equal(call(['record-store','recover'],undefined,['--transaction',tx.id,'--expected-recovery',tx.recovery_identity,'--action','complete']).status,'recovered');
 revision=call(['status']).revision;call(['batch'],payload,[],3);
 mutate({op:'review.record',target:{id:'final-review'},values:{target:'code',reviewer,contributors:[implementer],independence_basis:'Separate reviewer assesses this complete fixture implementation.',subjects:[subject],judgment:'approved',body:'The corrected subject meets the stated requirement.\n'},applicability:app(reviewer)});
 let concern=call(['blocker','show','defect']).data.items[0].fields;assert.equal(concern.state,'open');assert.deepEqual(concern.origin.subjects,[subject]);assert.equal(concern.origin.supporting_judgment,null);
 mutate({op:'blocker.set',target:{id:'defect'},values:{state:'resolved',resolution:{actor:verifier,rationale:'Verify reassessed its required outcome.',evidence_refs:[{path:ep,id:'corrected-check'}]}}});
 const explanation='Correction retained the original failure, its ownership and the explicit final assessment.\n';
 mutate({op:'decision.record',target:{id:'correction-basis'},values:{actor:verifier,subjects:[subject],rationale:'Keep the original failure as truthful evidence.',source_refs:[{path:mp,id:'defect'}],body:explanation},applicability:app(verifier)});
 mutate([{op:'verify.record',target:{},values:{verifier,subjects:[subject],evidence_refs:[{path:ep,id:'corrected-check'}],review_refs:[{path:rp,id:'final-review'}],outcome:'success',body:explanation},applicability:app(verifier)},{op:'activity.set',target:{},values:{stage:'verify',status:'completed',owner:verifier,reason:'Explicit final assessment.'}},{op:'work.set',target:{id:'work-1'},values:{status:'completed'}}]);
 assert.equal(call(['verify','show']).data.items[0].fields.body,explanation);assert.equal(call(['decisions','show']).data.items[0].fields.body,explanation);
 assert.equal(call(['evidence','show','failed-check']).data.items[0].fields.result,'failed');
 // Basis B -> C changes diagnostic identity without changing record revision.
 writeFileSync(join(root,'basis'),'B\n');const page=call(['observations','show'],undefined,['--limit','1']);assert.ok(page.scope.next);writeFileSync(join(root,'basis'),'C\n');const next=page.scope.next;const fresh=call(['observations','show'],undefined,['--limit','1']);assert.equal(fresh.revision,page.revision);assert.notEqual(fresh.scope.observation_identity,page.scope.observation_identity);call(['observations','show'],undefined,['--after',next.token,'--expected-revision',next.expected_revision,'--expected-observations',next.expected_observations],3);
 const stale=request({op:'activity.set',target:{},values:{stage:'implement',status:'in-progress',owner:implementer,reason:'Must reassess changed basis.'}});call(['activity','set'],stale,[],3);assert.equal(call(['status']).revision,revision);
});

test('TG-FINAL-01 public correction receipt with a densely filled evidence record',t=>{
 const root=mkdtempSync(join(tmpdir(),'recording-dense-adoption-'));t.after(()=>rmSync(root,{recursive:true,force:true}));mkdirSync(join(root,'docs/changes'),{recursive:true});
 const ep=prefix+'evidence.json',mp=prefix+'change.json',change=structuredClone(fixture.change);change.blockers=[];change.records=[{kind:'evidence',path:ep}];change.applicability=change.applicability.filter(a=>a.path===ep);
 const evidence={schema_version:2,change_id:'example',checks:[]};let size=Buffer.byteLength(encode(evidence));
 // Fill the one-MiB record to within one minimal failed-check entry. Maximum
 // counters/target lengths have their separate representation-boundary proof.
 for(let i=0;;i++){const check={id:`c${i}`,actor:implementer,subjects:[],result:'failed',procedure:'p',summary:'s'},delta=Buffer.byteLength(JSON.stringify(check))+(i?1:0);if(size+delta>1024*1024)break;evidence.checks.push(check);size+=delta;}
 assert.ok(size>1024*1024-200);
 function call(words,payload,extra=[]){const r=spawnSync(process.execPath,[cli,...words,'--root',root,'--change','example','--format','json',...(payload?['--input','-']:[]),...extra],{input:payload?encode(payload):undefined,encoding:'utf8',maxBuffer:16*1024*1024});assert.equal(r.status,0,r.stdout+r.stderr);return{result:JSON.parse(r.stdout),bytes:Buffer.byteLength(r.stdout)};}
 assert.equal(executeRecordStore({root,changeId:'example',operation:'record',request:{schema_version:2,contract:'rigorloop-records-v2',change_id:'example',expected_revision:null,reads:[],writes:[{path:mp,expected_identity:null,content:encode(change)},{path:ep,expected_identity:null,content:encode(evidence)}]}}).status,'saved');
 const context=call(['context'],{schema_version:1,select:[{kind:'activity',where:{}}]}).result;
 const correction=call(['blocker','add','dense-defect'],{schema_version:1,interface:'targeted-recording-v1',contract:context.record_contract,change_id:'example',expected_revision:context.revision,reads:[],operation:{op:'blocker.add',target:{id:'dense-defect'},values:{reporter:verifier,owner:implementer,subjects:[],evidence:'Failed dense evidence needs correction.',required_outcome:'Reassess all failed checks.',state:'open',resolution:null,basis:{rationale:'Explicit correction decision.',supporting_judgment:null}}}});
 assert.equal(correction.result.status,'saved');assert.ok(correction.bytes<65536);assert.ok(correction.result.observation_summary.total>=evidence.checks.length);
 const page=call(['observations','show'],undefined,['--limit','5']).result;assert.equal(page.scope.returned,5);assert.equal(page.scope.complete,false);assert.equal(page.scope.observation_identity,correction.result.observation_summary.observation_identity);
 assert.equal(call(['blocker','show','dense-defect']).result.data.items[0].fields.state,'open');
});
