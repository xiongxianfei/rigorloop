import assert from 'node:assert/strict';
import {test} from 'node:test';
import {writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {actor,project,createInput,invoke} from './helpers/operational-fixture.mjs';
import {reviewer,envelope,observation,prepare,assessment,applicability,fixture,deliveryFixture} from './helpers/operational-review-fixture.mjs';

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

test('owner-selected bases complete with final review and Verify without intermediate approvals',t=>{
  const {root,send,verification,closeout}=deliveryFixture(t,{intermediateReviews:false});
  const context=()=>invoke(root,['change','context']);
  const value=context().result.items[0].value;
  assert.deepEqual(value.governing_basis.gaps,[]);
  assert.ok(value.governing_basis.bases.every(b=>b.decision==='accepted'&&b.review===null));
  assert.deepEqual(value.review_standing.selected.map(r=>r.purpose),['code']);
  assert.equal(invoke(root,['change','complete'],envelope(context().result.revision,closeout)).exit,2);
  send(['verification','record','final'],{assessment:verification});
  send(['change','complete'],closeout);
  const historical=context().result.items[0].value;
  assert.equal(historical.historical,true);
  assert.equal(historical.completion.acceptance.length,2);
  assert.match(historical.completion.acceptance[0],/code Review code/);
  assert.match(historical.completion.acceptance[1],/Final Verification final/);
});

test('removing intermediate gates does not admit final success without whole-change approval',t=>{
  const {root,verification,closeout}=deliveryFixture(t,{intermediateReviews:false,finalReview:false});
  const revision=invoke(root,['change','context']).result.revision;
  const result=invoke(root,['verification','record','final'],envelope(revision,{assessment:verification}));
  assert.equal(result.exit,2);
  assert.match(JSON.stringify(result.result.errors),/whole-change/);
  assert.equal(invoke(root,['change','complete'],envelope(revision,closeout)).exit,2);
});

test('owner selection cannot substitute self-approval for independent final review',t=>{
  const {root,send,verification}=deliveryFixture(t,{intermediateReviews:false,finalReview:false});
  send(['review','prepare','code'],prepare());
  const review=invoke(root,['review','show','code']).result.items.find(i=>i.kind==='review').value;
  const revision=invoke(root,['change','context']).result.revision;
  const result=invoke(root,['review','record','code'],envelope(revision,{assessment:{...assessment(review.prepared.subjects),reviewer:actor},applicability}));
  assert.equal(result.exit,2);
  assert.match(JSON.stringify(result.result.errors),/contributors.*independent/);
  assert.equal(invoke(root,['verification','record','final'],envelope(revision,{assessment:verification})).exit,2);
});

test('optional requirement advice records findings without becoming an approval prerequisite',t=>{
  const {root,send,verification,closeout}=deliveryFixture(t,{intermediateReviews:false});
  send(['review','prepare','requirements-advice'],{...prepare('advisory'),purpose:'requirements',selection:[{path:'requirements.md',state:'present'}]});
  const review=invoke(root,['review','show','requirements-advice']).result.items.find(i=>i.kind==='review').value;
  const finding={id:'ambiguous',reporter:reviewer,owner:actor,scope:'Requirements',description:'An unresolved obligation',required_outcome:'Resolve the obligation',state:'open',disposition:null};
  send(['review','record','requirements-advice'],{assessment:assessment(review.prepared.subjects,null),findings:[finding]});
  let context=invoke(root,['change','context']);
  assert.deepEqual(context.result.items[0].value.review_standing.selected.map(r=>r.purpose),['code']);
  assert.equal(invoke(root,['verification','record','final'],envelope(context.result.revision,{assessment:verification})).exit,2);
  send(['review','record','requirements-advice'],{findings:[{...finding,state:'resolved',disposition:{actor:reviewer,reason:'Inspected the existing obligation and resolved the ambiguity without changing subjects',follow_up:null}}]});
  send(['verification','record','final'],{assessment:verification});
  send(['change','complete'],closeout);
});
