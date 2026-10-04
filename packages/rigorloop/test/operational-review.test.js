import assert from 'node:assert/strict';
import {test} from 'node:test';
import {writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {actor,project,createInput,invoke} from './helpers/operational-fixture.mjs';
import {reviewer,envelope,observation,prepare,assessment,applicability,fixture,deliveryFixture} from './helpers/operational-review-fixture.mjs';

test('operational review separates preparation, explicit assessment and selected standing',t=>{
  const {root,revision}=fixture(t);
  const prepared=invoke(root,['review','prepare','code'],envelope(revision,prepare()));assert.equal(prepared.exit,0,JSON.stringify(prepared));
  const shown=invoke(root,['review','show','code']);assert.equal(shown.exit,0,JSON.stringify(shown));
  const review=shown.result.items.find(i=>i.kind==='review').value;
  assert.equal(review.assessment,null);assert.equal(review.applicability.value,'needs-reassessment');
  assert.match(review.prepared.subjects[0].identity,/^sha256:/);
  const judged=invoke(root,['review','record','code'],envelope(prepared.result.revision,{assessment:assessment(review.prepared.subjects)}));assert.equal(judged.exit,0,JSON.stringify(judged));
  const after=invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value;
  assert.equal(after.assessment.judgment,'approved');assert.equal(after.applicability.value,'needs-reassessment');
  const current=invoke(root,['review','record','code'],envelope(judged.result.revision,{applicability}));assert.equal(current.exit,0,JSON.stringify(current));
  assert.equal(invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value.applicability.value,'current');
});

test('operational advisory assessment cannot select or establish a formal gate',t=>{
  const {root,revision}=fixture(t);
  const prepared=invoke(root,['review','prepare','advice'],envelope(revision,prepare('advisory')));assert.equal(prepared.exit,0,JSON.stringify(prepared));
  const review=invoke(root,['review','show','advice']).result.items.find(i=>i.kind==='review').value;
  const fake=invoke(root,['review','record','advice'],envelope(prepared.result.revision,{assessment:assessment(review.prepared.subjects)}));assert.equal(fake.exit,2);
  const actual=invoke(root,['review','record','advice'],envelope(prepared.result.revision,{assessment:assessment(review.prepared.subjects,null)}));assert.equal(actual.exit,0,JSON.stringify(actual));
  const context=invoke(root,['change','context']);assert.deepEqual(context.result.items[0].value.review_standing.selected,[]);
});

test('operational review findings survive a replacement assessment until explicitly dispositioned',t=>{
  const {root,revision}=fixture(t),prepared=invoke(root,['review','prepare','code'],envelope(revision,prepare()));assert.equal(prepared.exit,0,JSON.stringify(prepared));
  const review=invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value;
  const finding={id:'gap',reporter:reviewer,owner:actor,scope:'Navigation',description:'Missing interaction',required_outcome:'Correct interaction',state:'open',disposition:null};
  const adverse=invoke(root,['review','record','code'],envelope(prepared.result.revision,{assessment:assessment(review.prepared.subjects,'changes-requested'),findings:[finding]}));assert.equal(adverse.exit,0,JSON.stringify(adverse));
  const fresh=invoke(root,['review','record','code'],envelope(adverse.result.revision,{assessment:assessment(review.prepared.subjects)}));assert.equal(fresh.exit,0,JSON.stringify(fresh));
  const retained=invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value;assert.equal(retained.findings[0].state,'open');
  const compact=invoke(root,['review','record','code'],envelope(fresh.result.revision,{compact_findings:{ids:['gap'],actor:reviewer,reason:'Omit an inconvenient concern'}}));assert.equal(compact.exit,2);
  const resolved=invoke(root,['review','record','code'],envelope(fresh.result.revision,{findings:[{...finding,state:'resolved',disposition:{actor:reviewer,reason:'Correction assessed',follow_up:null}}],applicability}));assert.equal(resolved.exit,0,JSON.stringify(resolved));
});

test('operational completion requires distinct final Verify and retains a historical account after compaction',t=>{
  const {root,send,verification,closeout}=deliveryFixture(t);
  const context=()=>invoke(root,['change','context']);
  const premature=invoke(root,['change','complete'],envelope(context().result.revision,closeout));assert.equal(premature.exit,2);
  send(['verification','record','final'],{assessment:verification});
  const completed=send(['change','complete'],closeout);assert.equal(completed.result.committed,true);
  const historical=context().result.items[0].value;assert.equal(historical.historical,true);assert.equal(historical.completion.acceptance.length,5);
  writeFileSync(join(root,'implementation.txt'),'later unrelated regression');
  const repeated=send(['change','complete'],closeout);assert.equal(repeated.result.status,'unchanged');
  const drop=[...['requirements','design'].map(id=>({kind:'basis',id})),...['requirements','design','delivery','code'].map(id=>({kind:'review',id})),{kind:'verification',id:'final'},{kind:'work',id:'milestone'}];
  send(['change','update'],{retention:{drop,actor,reason:'Compact obsolete working support; completion is self-contained'}});
  const retry=send(['change','complete'],closeout);assert.equal(retry.result.status,'unchanged');
  assert.deepEqual(context().result.items[0].value.completion,historical.completion);
  const reopen=invoke(root,['change','update'],envelope(context().result.revision,{activity:createInput().input.activity}));assert.equal(reopen.exit,2);
});

test('operational support changes preserve earlier outcomes but require explicit renewed Verification',t=>{
  const {root,send,verification,closeout}=deliveryFixture(t);
  send(['verification','record','final'],{assessment:verification});
  send(['change','update'],{next_action:null});
  const show=()=>invoke(root,['verification','show','final']).result.items.find(i=>i.kind==='verification').value;
  assert.equal(show().support_state,'current');
  send(['review','record','code'],{applicability:{...applicability,rationale:'Reviewer explicitly confirms a harmless change'}});
  assert.equal(show().outcome,'success');assert.equal(show().support_state,'needs-reassessment');
  const revision=invoke(root,['change','context']).result.revision;
  const stale=invoke(root,['change','complete'],envelope(revision,closeout));assert.equal(stale.exit,2);
  send(['verification','record','final'],{assessment:verification});assert.equal(show().support_state,'current');
});

test('operational adverse requirement review preserves recorded acceptance and exposes unsupported reliance',t=>{
  const {root,send,verification}=deliveryFixture(t);
  const review=invoke(root,['review','show','requirements']).result.items.find(i=>i.kind==='review').value;
  send(['review','record','requirements'],{assessment:{...review.assessment,judgment:'changes-requested',summary:'New evidence contradicts the requirement basis'}});
  const context=invoke(root,['change','context']).result;
  assert.match(JSON.stringify(context),/Recorded acceptance of Basis requirements lacks current compatible review support/);
  assert.equal(context.items[0].value.governing_basis.bases.find(b=>b.id==='requirements').decision,'accepted');
  const verify=invoke(root,['verification','record','final'],envelope(context.revision,{assessment:verification}));assert.equal(verify.exit,2);
});
