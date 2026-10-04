import assert from 'node:assert/strict';
import {test} from 'node:test';
import {writeFileSync,unlinkSync} from 'node:fs';
import {join} from 'node:path';
import {actor,invoke} from './helpers/operational-fixture.mjs';
import {envelope,observation,prepare,assessment,applicability,fixture,deliveryFixture} from './helpers/operational-review-fixture.mjs';
const revision=root=>invoke(root,['change','context']).result.revision;

test('missing retained support is visible and cannot establish new success or closeout',t=>{
  const {root,send,verification,closeout}=deliveryFixture(t);
  writeFileSync(join(root,'report.txt'),'retained report');
  const evidence={id:'check',actor,reported_at:'2026-10-04',procedure:'navigation tests',scope:'Navigation',subjects:[],observation:{...observation,actor},result:'passed',summary:'Checks pass',limitations:[],attachments:['report.txt'],retain:[{name:'report.txt',source:'report.txt',media_type:'text/plain'}]};
  send(['change','update'],{evidence:[evidence]});
  const support={source:{kind:'evidence',id:'check'},scope:'Navigation',basis:[],result:'passed',explanation:'Selected report supports acceptance',limitations:[],attachments:['report.txt']};
  send(['verification','record','final'],{assessment:{...verification,evidence_refs:[support.source],support:[support]}});
  unlinkSync(join(root,'.rigorloop/artifacts/changes/navigation/report.txt'));
  const context=invoke(root,['change','context']);assert.equal(context.exit,0);assert.ok(context.result.observations.some(o=>o.code==='payload-unavailable'));
  const updated=invoke(root,['verification','record','final'],envelope(revision(root),{assessment:{...verification,summary:'Renewed success',evidence_refs:[support.source],support:[support]}}));assert.equal(updated.exit,2,JSON.stringify(updated));
  const completed=invoke(root,['change','complete'],envelope(revision(root),{...closeout,retained_attachments:['report.txt']}));assert.equal(completed.exit,2,JSON.stringify(completed));
  // Loss remains reportable without deleting the retained reference or fabricating bytes.
  const loss={...evidence,result:'inconclusive',summary:'Selected report is missing',limitations:['Retained report unavailable'],retain:[]};
  send(['change','update'],{evidence:[loss]});
});

test('compared applicability uses assessed subjects even after a new preparation',t=>{
  const {root,revision:initial}=fixture(t);
  const first=invoke(root,['review','prepare','code'],envelope(initial,prepare()));assert.equal(first.exit,0);
  const review=invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value;
  assert.equal(invoke(root,['review','record','code'],envelope(first.result.revision,{assessment:assessment(review.prepared.subjects),applicability})).exit,0);
  writeFileSync(join(root,'implementation.txt'),'materially changed implementation');
  assert.equal(invoke(root,['review','prepare','code'],envelope(revision(root),prepare())).exit,0);
  const result=invoke(root,['review','record','code'],envelope(revision(root),{applicability:{...applicability,observation:{...observation,method:'compared'}}}));
  assert.equal(result.exit,3,JSON.stringify(result));
  assert.equal(invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value.applicability.value,'needs-reassessment');
});

test('replacing a scoped Verification invalidates dependent assessments transitively',t=>{
  const {root,send,verification,closeout}=deliveryFixture(t);
  const scoped={...verification,scope:'scoped',review_refs:[],summary:'Scoped interaction check'};
  send(['verification','record','slice'],{assessment:scoped});
  const support=id=>({source:{kind:'verification',id},scope:'Navigation',basis:[],result:'success',explanation:'Scoped result supports this assessment',limitations:[],attachments:[]});
  send(['verification','record','dependent'],{assessment:{...scoped,support:[support('slice')]}});
  const code=invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value;
  send(['review','record','code'],{assessment:{...code.assessment,support:[support('dependent')]},applicability});
  send(['verification','record','final'],{assessment:verification});
  send(['verification','record','slice'],{assessment:{...scoped,outcome:'failed',summary:'Interaction failure discovered'}});
  assert.equal(invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value.applicability.value,'needs-reassessment');
  const final=invoke(root,['verification','show','final']).result.items.find(i=>i.kind==='verification').value;
  assert.equal(final.outcome,'success');assert.equal(final.support_state,'needs-reassessment');
  assert.equal(invoke(root,['change','complete'],envelope(revision(root),closeout)).exit,2);
});
