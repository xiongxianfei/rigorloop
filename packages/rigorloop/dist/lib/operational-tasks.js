import { CONTRACT, canonical, fail, validateType } from './operational-contract.js';
import { recordEntries, basisSupported } from './operational-model.js';
const equal=(a,b)=>canonical(a)===canonical(b);
const base=(change,id)=>({schema_version:4,contract:CONTRACT,change_id:change.change_id,id});
function merge(previous,incoming,key='id') {
  if(new Set(incoming.map(v=>v[key])).size!==incoming.length)fail('invalid-request','Duplicate supplied identity.');
  const values=new Map(previous.map(value=>[value[key],value]));
  for(const value of incoming)values.set(value[key],structuredClone(value));
  return [...values.values()].sort((a,b)=>a[key].localeCompare(b[key],'en'));
}
function currentAccounts(snapshot,kind) { return kind==='work'?snapshot.change.work:kind==='blocker'?snapshot.change.blockers:kind==='attachment'?snapshot.change.attachments:snapshot.accounts[kind]; }
export function changedRecords(before,after) {
  const old=new Map(recordEntries(before).map(e=>[e.kind+':'+e.id,e])),next=new Map(recordEntries(after).map(e=>[e.kind+':'+e.id,e]));
  const keys=[...new Set([...old.keys(),...next.keys()])].sort();
  const entries=keys.filter(key=>!equal(old.get(key)??null,next.get(key)??null)).map(key=>{const e=next.get(key)??old.get(key);return {kind:e.kind,id:e.id};});
  for(const id of new Set([...before.accounts.review,...after.accounts.review].map(r=>r.id))) {
    const a=before.accounts.review.find(r=>r.id===id)?.findings??[],b=after.accounts.review.find(r=>r.id===id)?.findings??[];
    for(const finding of new Set([...a,...b].map(f=>f.id)))if(!equal(a.find(f=>f.id===finding)??null,b.find(f=>f.id===finding)??null))entries.push({kind:'finding',review_id:id,id:finding});
  }
  return entries;
}
function retain(snapshot,retention) {
  const c=snapshot.change;
  for(const ref of retention.drop) {
    const list=currentAccounts(snapshot,ref.kind),key=ref.kind==='attachment'?'name':'id',record=list?.find(v=>v[key]===ref.id);
    if(!record&&ref.kind==='attachment') {
      validateType('attachment_name',ref.id);
      (snapshot.orphan_drops??=[]).push(ref.id);continue;
    }
    if(!record)fail('record-missing','Retention selects an absent account.');
    if(ref.kind==='work'&&(!c.completion||!['completed','cancelled'].includes(record.status)))fail('invalid-request','Active work cannot be compacted.');
    if(ref.kind==='blocker'&&(record.state==='open'||record.state==='deferred'&&!c.completion?.acceptance.some(text=>text.includes(record.disposition.follow_up))))fail('invalid-request','Unresolved obligations cannot be compacted.');
    if(ref.kind==='review'&&record.findings.some(f=>f.state==='open'||f.state==='deferred'&&!c.completion?.acceptance.some(text=>text.includes(f.disposition.follow_up))))fail('invalid-request','Unresolved findings protect their Review.');
    const selected=['requirement_basis','design_basis','active_adoption'].filter(field=>equal(c[field],ref));
    const reviews=c.reviews.filter(s=>equal(s.review,ref));
    if(!c.completion&&(selected.length||reviews.length))fail('invalid-request','Selected active accounts cannot be compacted.');
    for(const field of selected)c[field]=null;
    c.reviews=c.reviews.filter(s=>!equal(s.review,ref));
    list.splice(list.indexOf(record),1);
  }
}
function invalidate(before,after) {
  const changes=changedRecords(before,after),changed=new Set(changes.filter(r=>{
    if(r.kind!=='basis')return true;
    const prior=before.accounts.basis.find(b=>b.id===r.id),next=after.accounts.basis.find(b=>b.id===r.id);
    return !prior||!next||!equal({kind:prior.kind,subjects:prior.subjects},{kind:next.kind,subjects:next.subjects});
  }).map(r=>r.kind+':'+r.id));
  const finalInputs=c=>({intent:c.intent,authority:c.authority,requirement_basis:c.requirement_basis,design_basis:c.design_basis,plan:c.plan,reviews:c.reviews,work:c.work,blockers:c.blockers});
  const finalChanged=!equal(finalInputs(before.change),finalInputs(after.change));
  // Reach a fixed point: changing a scoped assessment can invalidate another
  // assessment through several retained support references, in either order.
  let expanded;
  do {
    expanded=false;
    for(const review of after.accounts.review) {
      const refs=[...review.prepared.basis_refs,...review.assessment?.evidence_refs??[],...review.assessment?.support.map(s=>s.source)??[]];
      if(refs.some(r=>changed.has(r.kind+':'+r.id))) {
        review.applicability.value='needs-reassessment';
        const key='review:'+review.id;if(!changed.has(key)){changed.add(key);expanded=true;}
      }
    }
    for(const verification of after.accounts.verification) {
      const refs=[...verification.review_refs,...verification.evidence_refs,...verification.support.map(s=>s.source)];
      if(verification.scope==='final'&&finalChanged||refs.some(r=>changed.has(r.kind+':'+r.id))) {
        verification.support_state='needs-reassessment';
        const key='verification:'+verification.id;if(!changed.has(key)){changed.add(key);expanded=true;}
      }
    }
  } while(expanded);

}
export function updateSnapshot(before,input,observe) {
  if(!Object.keys(input).length)fail('invalid-request','Update requires at least one explicit section.');
  const snapshot=structuredClone(before),c=snapshot.change;
  const count=['work','blockers','evidence','decisions'].reduce((n,k)=>n+(input[k]?.length??0),0)+(input.retention?.drop.length??0)+(input.basis?1:0)+(input.adoption?1:0);
  if(count>64)fail('size-limit','Task exceeds 64 supplied engineering entries.');
  if(c.completion&&Object.keys(input).some(k=>!['completion_note','retention'].includes(k)))fail('invalid-request','Completed Changes admit only explicit notes and safe compaction.');
  for(const field of ['intent','request','authority','activity','next_action'])if(Object.hasOwn(input,field))c[field]=structuredClone(input[field]);
  if(input.work)c.work=merge(c.work,input.work);
  if(input.blockers)c.blockers=merge(c.blockers,input.blockers);
  if(input.evidence) {
    const values=input.evidence.map(value=>{
      const previous=before.accounts.evidence.find(e=>e.id===value.id);
      if(previous&&(previous.procedure!==value.procedure||previous.scope!==value.scope))fail('invalid-request','Changed procedure or scope requires another Evidence ID.');
      const {retain,...stored}=value;return {...base(c,value.id),...stored};
    });
    snapshot.accounts.evidence=merge(snapshot.accounts.evidence,values);
  }
  if(input.decisions)snapshot.accounts.decision=merge(snapshot.accounts.decision,input.decisions.map(value=>({...base(c,value.id),...value})));
  if(Object.hasOwn(input,'plan'))c.plan=input.plan===null?null:observe([{path:input.plan,state:'present'}])[0];
  if(input.basis) {
    const {selection,...fields}=input.basis,value={...base(c,fields.id),...fields,subjects:observe(selection)};
    snapshot.accounts.basis=merge(snapshot.accounts.basis,[value]);c[value.kind==='requirements'?'requirement_basis':'design_basis']={kind:'basis',id:value.id};
  }
  if(input.adoption) {
    const value={...base(c,input.adoption.id),...input.adoption};
    if(value.target_workflow!==c.workflow_contract)fail('invalid-request','Adoption target does not match the Change workflow.');
    snapshot.accounts.adoption=merge(snapshot.accounts.adoption,[value]);
    if(value.phase==='activated')c.active_adoption={kind:'adoption',id:value.id};
    else if(value.phase==='unavailable'&&c.active_adoption?.id===value.id)c.active_adoption=null;
  }
  if(input.completion_note) {
    if(!c.completion)fail('invalid-request','Completion notes require a completed Change.');
    c.completion_notes.push(structuredClone(input.completion_note));
  }
  if(input.retention)retain(snapshot,input.retention);
  if(!c.completion)invalidate(before,snapshot);
  if(input.basis?.decision==='accepted'&&!basisSupported(snapshot,snapshot.accounts.basis.find(b=>b.id===input.basis.id)))fail('invalid-request','New acceptance requires current compatible formal approval of its subjects.');
  return snapshot;
}

export function prepareReview(before,id,input,observe) {
  if(before.change.completion)fail('invalid-request','Completed Change reviews are historical.');
  if(input.selection.length+input.basis_refs.length>64)fail('size-limit','Review preparation exceeds 64 entries.');
  if(input.scope==='advisory'&&input.purpose!=='code')fail('invalid-request','Only code reviews admit advisory scope.');
  const snapshot=structuredClone(before),previous=snapshot.accounts.review.find(r=>r.id===id);
  if(previous&&(previous.purpose!==input.purpose||previous.scope!==input.scope))fail('invalid-request','An existing Review cannot change purpose or formal scope.');
  const subjects=observe(input.selection);
  const plan=input.plan_path===null?null:subjects.find(s=>s.path===input.plan_path&&s.state==='present');
  if(input.plan_path!==null&&!plan)fail('invalid-request','The selected plan must be a present prepared subject.');
  const prepared={subjects,basis_refs:input.basis_refs,plan,scope:input.description,coverage_rationale:input.coverage_rationale,prepared_by:input.actor};
  const value=previous??{...base(snapshot.change,id),purpose:input.purpose,scope:input.scope,assessment:null,findings:[],applicability:{value:'needs-reassessment',actor:input.actor,rationale:'Prepared input has no current assessment.',observation:{method:'unknown',actor:input.actor,scope:input.description,summary:'No assessment of this prepared scope is established.'}}};
  if(!previous||!equal(previous.prepared,prepared))value.applicability.value='needs-reassessment';
  value.prepared=prepared;snapshot.accounts.review=merge(snapshot.accounts.review,[value]);
  invalidate(before,snapshot);return snapshot;
}
export function recordReview(before,id,input,check) {
  if(before.change.completion)fail('invalid-request','Completed Change reviews are historical.');
  if(!Object.keys(input).length)fail('invalid-request','Review recording requires an explicit section.');
  if((input.findings?.length??0)+(input.compact_findings?.ids.length??0)>64)fail('size-limit','Review recording exceeds 64 entries.');
  const snapshot=structuredClone(before),review=snapshot.accounts.review.find(r=>r.id===id);
  if(!review)fail('record-missing','Prepare the Review before recording an assessment.');
  if(input.assessment) {
    if(!equal(review.assessment,input.assessment)){review.assessment=structuredClone(input.assessment);review.applicability.value='needs-reassessment';}
    if(review.scope==='formal')snapshot.change.reviews=merge(snapshot.change.reviews,[{purpose:review.purpose,review:{kind:'review',id}}],'purpose');
  }
  if(input.findings)review.findings=merge(review.findings,input.findings);
  if(input.compact_findings) {
    for(const id of input.compact_findings.ids) {
      const finding=review.findings.find(f=>f.id===id);
      if(!finding)fail('record-missing','The selected finding is absent.');
      if(['open','deferred'].includes(finding.state))fail('invalid-request','Unresolved findings cannot be compacted.');
      review.findings.splice(review.findings.indexOf(finding),1);
    }
  }
  if(input.applicability) {
    if(input.applicability.value==='current') {
      if(!review.assessment||review.scope!=='formal'||review.assessment.judgment!=='approved')fail('invalid-request','Current standing needs an approved formal assessment.');
      if(review.assessment.contributors.some(a=>a.id===review.assessment.reviewer.id))fail('invalid-request','Known implementation contributors cannot establish independent current review of their own work.');
      if(!review.prepared.subjects.every(s=>review.assessment.assessed_subjects.some(a=>a.path===s.path&&a.state===s.state)))fail('invalid-request','Prepared scope exceeds the assessed scope.');
      if(input.applicability.observation.method==='compared')check([...review.assessment.assessed_subjects,...review.assessment.governing_basis]);
    }
    review.applicability=structuredClone(input.applicability);
  }
  invalidate(before,snapshot);return snapshot;
}
function selectedReview(snapshot,purpose) {
  const selected=snapshot.change.reviews.find(r=>r.purpose===purpose);
  return snapshot.accounts.review.find(r=>r.id===selected?.review.id);
}
export function requireCompletionBasis(snapshot) {
  const c=snapshot.change;
  for(const selection of [c.requirement_basis,c.design_basis]) {
    const basis=snapshot.accounts.basis.find(b=>b.id===selection?.id);
    if(!basis||!basisSupported(snapshot,basis))fail('invalid-request','Completion requires currently supported accepted requirement and design bases.');
  }
  for(const purpose of ['requirements','design','delivery','code']) {
    const review=selectedReview(snapshot,purpose);
    if(!review||review.scope!=='formal'||review.assessment?.judgment!=='approved'||review.applicability.value!=='current')fail('invalid-request','Completion requires current formal review support for every mandatory gate.');
  }
  const delivery=selectedReview(snapshot,'delivery');
  if(!c.plan||!delivery.prepared.subjects.some(s=>equal(s,c.plan)))fail('invalid-request','Completion requires the reviewed delivery plan.');
  if(c.work.some(w=>!['completed','cancelled'].includes(w.status)))fail('invalid-request','Completion has unfinished work.');
  const issues=[...c.blockers,...snapshot.accounts.review.flatMap(r=>r.findings)];
  if(issues.some(i=>i.state==='open'||i.state==='deferred'&&!i.disposition?.follow_up))fail('invalid-request','Completion has unresolved obligations; record their explicit disposition before relying on success.');
}
export function recordVerification(before,id,input,observe,check) {
  if(before.change.completion)fail('invalid-request','Completed Change verification is historical.');
  const snapshot=input.evidence?updateSnapshot(before,{evidence:input.evidence},observe):structuredClone(before);
  const value={...base(snapshot.change,id),...structuredClone(input.assessment),support_state:'current'};
  if(value.observation.method==='compared')check([...value.subjects,...value.governing_basis]);
  if(value.scope==='final'&&value.outcome==='success') {
    requireCompletionBasis(snapshot);
    for(const selection of snapshot.change.reviews)if(!value.review_refs.some(r=>equal(r,selection.review)))fail('invalid-request','Final success must identify every selected supporting Review.');
  }
  snapshot.accounts.verification=merge(snapshot.accounts.verification,[value]);
  invalidate(before,snapshot);
  // This explicit assessment owns its new support account; existing dependent
  // judgments still need reassessment. A newly invalidated gate blocks success.
  value.support_state='current';
  snapshot.accounts.verification=merge(snapshot.accounts.verification,[value]);
  if(value.scope==='final'&&value.outcome==='success')requireCompletionBasis(snapshot);
  return snapshot;
}
export function completeChange(before,input) {
  const snapshot=structuredClone(before),c=snapshot.change;
  if(c.completion) {
    const {acceptance,verification_id,...saved}=c.completion;
    if(!equal({...saved,verification:verification_id},input))fail('invalid-request','A completed historical account cannot be replaced; use a completion note.');
    return snapshot;
  }
  requireCompletionBasis(snapshot);
  const verification=snapshot.accounts.verification.find(v=>v.id===input.verification);
  if(!verification||verification.scope!=='final'||verification.outcome!=='success'||verification.support_state!=='current')fail('invalid-request','Completion requires current successful final Verification.');
  const {verification:id,...fields}=input;
  const acceptance=c.reviews.map(s=>{
    const review=snapshot.accounts.review.find(r=>r.id===s.review.id);
    return `${review.purpose} Review ${review.id}: ${review.assessment.judgment}; assessor ${review.assessment.reviewer.id}; scope ${review.prepared.scope}; ${review.assessment.summary}`;
  });
  for(const issue of [...c.blockers,...snapshot.accounts.review.flatMap(r=>r.findings)].filter(i=>i.state==='deferred'))acceptance.push(`Deferred ${issue.id}; owner ${issue.owner.id}; disposition by ${issue.disposition.actor.id}: ${issue.disposition.reason}; follow-up: ${issue.disposition.follow_up}`);
  acceptance.push(`Final Verification ${id}: ${verification.outcome}; verifier ${verification.verifier.id}; ${verification.summary}`);
  c.completion={...structuredClone(fields),verification_id:id,acceptance};
  c.activity={stage:'verify',status:'completed',owner:input.actor,reason:input.reason};c.next_action=null;
  return snapshot;
}
