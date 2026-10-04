import { CONTRACT, LIMIT, fail, canonical, validateType, validateChange, encodedSize, issueReserve } from './operational-contract.js';
import { publicResult } from './operational-receipt.js';
import { referenceFields, subjectFields, getField } from './operational-layout.js';

export const emptyAccounts = () => ({ basis: [], review: [], evidence: [], decision: [], verification: [], adoption: [] });
export function recordEntries(snapshot) {
  const c = snapshot.change;
  return [{ kind: 'change', id: c.change_id, value: c },
    ...['work', 'blocker', 'attachment'].flatMap(kind => c[{work:'work',blocker:'blockers',attachment:'attachments'}[kind]].map(value=>({kind,id:value.id??value.name,value}))),
    ...Object.entries(snapshot.accounts).flatMap(([kind,values])=>values.map(value=>({kind,id:value.id,value}))),
  ].sort((a,b)=>a.kind.localeCompare(b.kind,'en')||a.id.localeCompare(b.id,'en'));
}
export function selectorIndex(snapshot) { return recordEntries(snapshot).map(({kind,id})=>({kind,id})); }
export const observedIdentity = (token = null, store = null) => ({ record_contract: CONTRACT, change_revision: token, store_revision: store });
export function selectedOutcome(snapshot, selected, token) {
  const entries = recordEntries(snapshot);
  const records = selected.map(s=>{
    const entry=entries.find(e=>e.kind===s.kind&&e.id===s.id);
    if(!entry)fail('record-missing','The selected account is absent.');
    return entry.kind==='attachment'?{...entry,value:{...entry.value,read_location:`.rigorloop/artifacts/changes/${snapshot.change.change_id}/${entry.id}`}}:entry;
  });
  const discovery=selected.length===1&&selected[0].kind==='change';
  return {kind:'read',status:'ok',committed:false,records,projections:discovery?[{query_kind:'selector-index',value:selectorIndex(snapshot)}]:[],diagnostics:[],identity:observedIdentity(token)};
}
function unique(values,key,description) {
  if(new Set(values.map(key)).size!==values.length)fail('invalid-request','Duplicate '+description+'.');
}
function validateSubjects(subjects) {
  unique(subjects,s=>s.path,'subject path');
  for(const s of subjects)if(s.state==='absent'&&s.identity!==null)fail('invalid-request','Absent subjects cannot have compared identities.');
}
function validateIssue(issue) {
  if((issue.state==='open')!==(issue.disposition===null))fail('invalid-request','Issue state requires an explicit matching disposition.');
  if(issue.state==='deferred'&&issue.disposition.follow_up===null)fail('invalid-request','Deferred issues require accountable follow-up.');
  issueReserve([issue]);
}
export function validateSnapshot(snapshot) {
  const {change:c,accounts}=snapshot;
  validateChange(c);
  for(const [kind,values] of Object.entries(accounts))for(const value of values) {
    validateType(kind,value);
    if(value.change_id!==c.change_id)fail('invalid-request','Accounts cannot cross Change scope.');
  }
  const entries=recordEntries(snapshot);
  unique(entries,e=>e.kind+':'+e.id,'account identity');
  const byKey=new Map(entries.map(e=>[e.kind+':'+e.id,e.value]));
  const ref=(r,kinds)=>{
    if(!r)return null;
    if(kinds&&!kinds.includes(r.kind))fail('invalid-request','Reference kind does not match its role.');
    const value=byKey.get(r.kind+':'+r.id);
    if(!value)fail('invalid-request','Reference selects an absent account.');
    return value;
  };
  const attachment=name=>{if(!byKey.has('attachment:'+name))fail('invalid-request','Attachment reference selects absent metadata.');};
  const validateSupport=support=>support.forEach(s=>{ref(s.source);validateSubjects(s.basis);s.attachments.forEach(attachment);});
  c.blockers.forEach(validateIssue);
  if(c.plan)validateSubjects([c.plan]);
  for(const work of c.work) {
    if(['completed','cancelled'].includes(work.status)&&!work.completion_reason)fail('invalid-request','Terminal work requires a completion reason.');
    work.check_refs.forEach(r=>ref(r,['evidence']));
    unique(work.blocker_ids,x=>x,'work blocker');
    work.blocker_ids.forEach(id=>{if(!byKey.has('blocker:'+id))fail('invalid-request','Work selects an absent blocker.');});
  }
  for(const [kind,values] of Object.entries(accounts))for(const value of values) {
    for(const field of referenceFields[kind]??[]) {
      const selected=getField(value,field), refs=selected==null?[]:Array.isArray(selected)?selected:[selected];
      unique(refs,canonical,'reference');
      refs.forEach(r=>ref(r,field==='review'||field==='review_refs'?['review']:field.includes('evidence')?['evidence']:field.includes('basis')?['basis']:null));
    }
    for(const field of subjectFields[kind]??[]) {
      const selected=getField(value,field);validateSubjects(selected==null?[]:Array.isArray(selected)?selected:[selected]);
    }
    if(kind==='review') {
      unique(value.findings,f=>f.id,'finding');value.findings.forEach(validateIssue);
      if(value.scope==='advisory'&&value.purpose!=='code')fail('invalid-request','Advisory review is code-only.');
      if(value.assessment) {
        if((value.scope==='advisory')!==(value.assessment.judgment===null))fail('invalid-request','Review judgment does not match its scope.');
        validateSupport(value.assessment.support);
      }
      if(value.applicability.value==='current'&&(!value.assessment||value.scope!=='formal'||value.assessment.judgment!=='approved'))fail('invalid-request','Current applicability requires an approved formal assessment.');
      if(value.prepared.plan&&!value.prepared.subjects.some(s=>canonical(s)===canonical(value.prepared.plan)))fail('invalid-request','Review plan must be included among prepared subjects.');
    }
    if(kind==='evidence')value.attachments.forEach(attachment);
    if(kind==='verification')validateSupport(value.support);
    if(kind==='basis'&&value.decision==='accepted') {
      const r=ref(value.review,['review']);
      if(!r||r.scope!=='formal'||r.purpose!==(value.kind==='requirements'?'requirements':'design'))fail('invalid-request','Accepted Basis must retain its compatible formal Review reference.');
    }
  }
  const rb=ref(c.requirement_basis,['basis']),db=ref(c.design_basis,['basis']);
  if(rb&&rb.kind!=='requirements'||db&&db.kind!=='design')fail('invalid-request','Selected Basis kind is inconsistent.');
  const adoption=ref(c.active_adoption,['adoption']);
  if(adoption&&adoption.phase!=='activated')fail('invalid-request','Selected Adoption is not activated.');
  unique(c.reviews,r=>r.purpose,'selected review purpose');
  for(const selection of c.reviews){const review=ref(selection.review,['review']);if(review.scope!=='formal'||review.purpose!==selection.purpose)fail('invalid-request','Review selection purpose or scope is inconsistent.');}
  c.completion?.retained_attachments.forEach(attachment);
  const largest='ffffffff-ffff-ffff-ffff-ffffffffffff:9223372036854775807';
  for(const entry of entries) {
    const reserve=entry.kind==='change'?issueReserve(c.blockers):entry.kind==='review'?issueReserve(entry.value.findings):entry.kind==='blocker'?issueReserve([entry.value]):0;
    const output=publicResult('change.context',c.change_id,selectedOutcome(snapshot,[{kind:entry.kind,id:entry.id}],largest));
    if(encodedSize(output)+reserve>LIMIT)fail('size-limit','Account and required disposition capacity exceed the retrievable response bound.');
  }
}

export function basisSupported(snapshot,basis) {
  const review=snapshot.accounts.review.find(r=>r.id===basis.review?.id);
  return basis.decision==='accepted'&&review?.scope==='formal'&&review.purpose===basis.kind&&review.assessment?.judgment==='approved'&&review.applicability.value==='current'&&basis.subjects.every(s=>review.prepared.subjects.some(a=>canonical(a)===canonical(s))&&review.assessment.assessed_subjects.some(a=>a.path===s.path&&a.state===s.state));
}

export function handoff(snapshot,token) {
  const {change:c,accounts:a}=snapshot;
  const value=c.completion?{complete:true,historical:true,completion:c.completion,notes:c.completion_notes,limitations:['Historical acceptance; no present-system applicability assessment.']}:{
    complete:true,limitations:['Recorded handoff; actor attribution does not authenticate authority or independence.'],
    intent_and_authority:{intent:c.intent,request:c.request,authority:c.authority},
    governing_basis:{requirements:c.requirement_basis,design:c.design_basis,plan:c.plan,bases:a.basis,gaps:[...a.basis.filter(b=>b.decision==='accepted'&&!basisSupported(snapshot,b)).map(b=>'Recorded acceptance of Basis '+b.id+' lacks current compatible review support.'),...(!c.requirement_basis?['Requirement basis not recorded.']:[]),...(!c.design_basis?['Design basis not recorded.']:[]),...(!c.plan?['Delivery plan not recorded.']:[])]},
    progress:{activity:c.activity,work:c.work},
    issues_and_rationale:{blockers:c.blockers,findings:a.review.flatMap(r=>r.findings.map(f=>({review_id:r.id,...f}))),decisions:a.decision},
    evidence:{items:a.evidence,limitations:a.evidence.length?[]:['No evidence recorded.']},
    review_standing:{items:a.review,selected:c.reviews,verification:a.verification,limitations:a.review.length?[]:['No review judgments recorded.']},
    next_action:c.next_action,
  };
  return {kind:'read',status:'ok',committed:false,records:[],projections:[{query_kind:'context',value}],diagnostics:[],identity:observedIdentity(token)};
}
