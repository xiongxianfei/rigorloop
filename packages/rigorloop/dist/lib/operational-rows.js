import { CONTRACT, fail, validateType, validateChange, createChange } from './operational-contract.js';
import { layouts, fieldSpec, referenceFields, subjectFields, getField, setField } from './operational-layout.js';

const parse = value => value === null ? null : JSON.parse(value);
const stringify = value => value === null ? null : JSON.stringify(value);
const common = (changeId, id) => ({ schema_version: 4, contract: CONTRACT, change_id: changeId, id });
const issueKeys = ['id', 'reporter', 'owner', 'scope', 'description', 'required_outcome', 'state', 'disposition'];
const issueFromRow = row => Object.fromEntries(issueKeys.map(key => [key, ['reporter','owner','disposition'].includes(key) ? parse(row[key]) : row[key]]));
function insert(db, table, values) {
  // Table and column names come exclusively from this product-owned mapping.
  const keys = Object.keys(values);
  db.prepare(`INSERT INTO ${table}(${keys.join(',')}) VALUES(${keys.map(() => '?').join(',')})`).run(...Object.values(values));
}
export function loadSnapshot(db, id) {
  const row = db.prepare('SELECT * FROM changes WHERE change_id=?').get(id);
  if (!row) return null;
  const change = createChange(id, {
    intent: { goal: row.goal, scope: row.scope, exclusions: parse(row.exclusions) },
    request: parse(row.request), authority: parse(row.authority),
    activity: { stage: row.activity_stage, status: row.activity_status, owner: parse(row.activity_owner), reason: row.activity_reason },
    next_action: parse(row.next_action),
  });
  const accounts = Object.fromEntries(Object.keys(layouts).filter(k => k !== 'work').map(k => [k, []]));
  const indexed = new Map();
  for (const { kind, id: accountId } of db.prepare('SELECT kind,id FROM accounts WHERE change_id=? ORDER BY kind,id').all(id)) {
    const layout = layouts[kind];
    if (!layout) fail('store-unavailable', 'Unsupported stored account kind.');
    const stored = db.prepare(`SELECT * FROM ${layout.table} WHERE change_id=? AND id=?`).get(id, accountId);
    if (!stored) fail('store-unavailable', 'A registered account body is missing.');
    const value = kind === 'work' ? { id: accountId } : common(id, accountId);
    for (const field of layout.fields.map(fieldSpec)) setField(value, field.path, field.json ? parse(stored[field.column]) : stored[field.column]);
    for (const field of referenceFields[kind] ?? []) setField(value, field, field === 'review' ? null : []);
    for (const field of subjectFields[kind] ?? []) setField(value, field, field.endsWith('plan') ? null : []);
    if (kind === 'review') { value.findings = []; value.assessment.support = []; if (stored.assessment_reviewer === null) value.assessment = null; }
    if (kind === 'verification') value.support = [];
    if (kind === 'work') value.blocker_ids = [];
    if (kind === 'evidence') value.attachments = [];
    indexed.set(kind + ':' + accountId, value);
    if (kind === 'work') change.work.push(value); else accounts[kind].push(value);
  }
  const owner = (kind, accountId) => {
    const value = kind === 'change' ? change : indexed.get(kind + ':' + accountId);
    if (!value) fail('store-unavailable', 'A stored relationship has no owner.');
    return value;
  };
  for (const r of db.prepare('SELECT * FROM account_refs WHERE change_id=? ORDER BY owner_kind,owner_id,relation,ordinal').all(id)) {
    const value = owner(r.owner_kind, r.owner_id), ref = { kind: r.target_kind, id: r.target_id };
    if (r.relation === 'review') value.review = ref; else getField(value, r.relation).push(ref);
  }
  for (const r of db.prepare('SELECT * FROM subjects WHERE change_id=? ORDER BY owner_kind,owner_id,role,ordinal').all(id)) {
    const value = owner(r.owner_kind, r.owner_id), subject = { path: r.path, state: r.state, identity: r.identity };
    if (r.role.endsWith('plan')) setField(value, r.role, subject); else getField(value, r.role).push(subject);
  }
  for (const r of db.prepare('SELECT * FROM selections WHERE change_id=? ORDER BY slot').all(id)) {
    const ref = { kind: r.kind, id: r.id };
    if (r.slot.startsWith('review-')) change.reviews.push({ purpose: r.slot.slice(7), review: ref });
    else change[{ 'requirement-basis': 'requirement_basis', 'design-basis': 'design_basis', 'active-adoption': 'active_adoption' }[r.slot]] = ref;
  }
  change.blockers = db.prepare('SELECT * FROM blockers WHERE change_id=? ORDER BY id').all(id).map(issueFromRow);
  for (const r of db.prepare('SELECT * FROM findings WHERE change_id=? ORDER BY review_id,id').all(id)) owner('review', r.review_id).findings.push(issueFromRow(r));
  for (const r of db.prepare('SELECT * FROM work_blockers WHERE change_id=? ORDER BY work_id,ordinal').all(id)) owner('work', r.work_id).blocker_ids.push(r.blocker_id);
  for (const r of db.prepare('SELECT * FROM support_summaries WHERE change_id=? ORDER BY owner_kind,owner_id,ordinal').all(id)) {
    const target = owner(r.owner_kind,r.owner_id), support = r.owner_kind === 'review' ? target.assessment.support : target.support;
    support.push({ source: { kind: r.source_kind, id: r.source_id }, scope: r.scope, result: r.result, explanation: r.explanation, limitations: parse(r.limitations), basis: [], attachments: [] });
  }
  for (const r of db.prepare('SELECT * FROM support_subjects WHERE change_id=? ORDER BY owner_kind,owner_id,support_ordinal,ordinal').all(id)) {
    const target = owner(r.owner_kind,r.owner_id), support = r.owner_kind === 'review' ? target.assessment.support : target.support;
    support[Number(r.support_ordinal)].basis.push({ path: r.path, state: r.state, identity: r.identity });
  }
  change.attachments = db.prepare('SELECT * FROM attachments WHERE change_id=? ORDER BY name').all(id).map(r => ({ name: r.name, media_type: r.media_type, byte_count: Number(r.byte_count) }));
  const completion = db.prepare('SELECT * FROM completions WHERE change_id=?').get(id);
  if (completion) {
    change.completion = Object.fromEntries(Object.entries(completion).filter(([k]) => k !== 'change_id').map(([k,v]) => [k, ['actor','governing_references','acceptance','limitations'].includes(k) ? parse(v) : v]));
    change.completion.retained_attachments = [];
  }
  change.completion_notes = db.prepare('SELECT actor,reason,explanation FROM completion_notes WHERE change_id=? ORDER BY ordinal').all(id).map(r => ({ ...r, actor: parse(r.actor) }));
  for (const r of db.prepare('SELECT * FROM attachment_refs WHERE change_id=? ORDER BY owner_kind,owner_id,ordinal').all(id)) {
    if (r.owner_kind === 'completion') change.completion.retained_attachments.push(r.name);
    else {
      const target = owner(r.owner_kind,r.owner_id);
      const holder = r.owner_kind === 'evidence' ? target : (r.owner_kind === 'review' ? target.assessment.support : target.support)[Number(r.support_ordinal)];
      holder.attachments.push(r.name);
    }
  }
  try { validateChange(change); for (const [kind, records] of Object.entries(accounts)) for (const value of records) validateType(kind,value); }
  catch { fail('store-unavailable', 'Stored records do not satisfy the supported contract.'); }
  return { change, accounts, revision: row.revision };
}

// Reconcile only this Change's complete admitted candidate inside the caller's
// transaction. Deferred constraints validate surviving references at COMMIT.
export function saveSnapshot(db, snapshot, revision) {
  const { change: c, accounts } = snapshot, id = c.change_id;
  const a = c.activity;
  const values = { revision, workflow_contract: c.workflow_contract, goal: c.intent.goal, scope: c.intent.scope, exclusions: stringify(c.intent.exclusions), request: stringify(c.request), authority: stringify(c.authority), activity_stage: a.stage, activity_status: a.status, activity_owner: stringify(a.owner), activity_reason: a.reason, next_action: stringify(c.next_action) };
  if (db.prepare('SELECT 1 FROM changes WHERE change_id=?').get(id)) db.prepare(`UPDATE changes SET ${Object.keys(values).map(k=>k+'=?').join(',')} WHERE change_id=?`).run(...Object.values(values),id);
  else insert(db,'changes',{change_id:id,...values});
  const childTables = ['attachment_refs','support_subjects','support_summaries','account_refs','subjects','selections','work_blockers','findings','blockers','attachments','completions','completion_notes', ...Object.values(layouts).map(x=>x.table),'accounts'];
  for (const table of childTables) db.prepare(`DELETE FROM ${table} WHERE change_id=?`).run(id);
  const issue = (table, value, extra={}) => insert(db,table,{change_id:id,...extra,...Object.fromEntries(issueKeys.map(k=>[k,['reporter','owner','disposition'].includes(k)?stringify(value[k]):value[k]]))});
  const addSubjects = (kind, accountId, role, subjects) => subjects.forEach((subject,ordinal)=>insert(db,'subjects',{change_id:id,owner_kind:kind,owner_id:accountId,role,ordinal,...subject}));
  const addAttachments = (kind,accountId,names,supportOrdinal=null,start=0) => names.forEach((name,n)=>insert(db,'attachment_refs',{change_id:id,owner_kind:kind,owner_id:accountId,support_ordinal:supportOrdinal,ordinal:start+n,name}));
  for (const [kind, records] of Object.entries({...accounts,work:c.work})) for (const record of records) {
    const key={change_id:id,kind,id:record.id}; insert(db,'accounts',key);
    const layout=layouts[kind], fields={};
    for (const f of layout.fields.map(fieldSpec)) { const value=getField(record,f.path)??null; fields[f.column]=f.json?stringify(value):value; }
    insert(db,layout.table,{...key,...fields});
    for (const relation of referenceFields[kind]??[]) {
      const source=getField(record,relation), refs=source===null||source===undefined?[]:Array.isArray(source)?source:[source];
      refs.forEach((ref,ordinal)=>insert(db,'account_refs',{change_id:id,owner_kind:kind,owner_id:record.id,relation,ordinal,target_kind:ref.kind,target_id:ref.id}));
    }
    for (const role of subjectFields[kind]??[]) { const subjects=getField(record,role); addSubjects(kind,record.id,role,subjects==null?[]:Array.isArray(subjects)?subjects:[subjects]); }
    if(kind==='review') record.findings.forEach(value=>issue('findings',value,{review_id:record.id}));
    if(kind==='work') record.blocker_ids.forEach((blocker_id,ordinal)=>insert(db,'work_blockers',{change_id:id,work_id:record.id,ordinal,blocker_id}));
    const support = kind==='review'?record.assessment?.support??[]:kind==='verification'?record.support:[];
    let attachmentOrdinal=0;
    support.forEach((summary,ordinal)=>{
      insert(db,'support_summaries',{change_id:id,owner_kind:kind,owner_id:record.id,ordinal,source_kind:summary.source.kind,source_id:summary.source.id,scope:summary.scope,result:summary.result,explanation:summary.explanation,limitations:stringify(summary.limitations)});
      summary.basis.forEach((subject,n)=>insert(db,'support_subjects',{change_id:id,owner_kind:kind,owner_id:record.id,support_ordinal:ordinal,ordinal:n,...subject}));
      addAttachments(kind,record.id,summary.attachments,ordinal,attachmentOrdinal); attachmentOrdinal+=summary.attachments.length;
    });
    if(kind==='evidence')addAttachments(kind,record.id,record.attachments);
  }
  c.blockers.forEach(value=>issue('blockers',value));
  c.attachments.forEach(value=>insert(db,'attachments',{change_id:id,...value}));
  for(const [slot,ref] of [['requirement-basis',c.requirement_basis],['design-basis',c.design_basis],['active-adoption',c.active_adoption],...c.reviews.map(r=>['review-'+r.purpose,r.review])]) if(ref)insert(db,'selections',{change_id:id,slot,...ref});
  if(c.plan)addSubjects('change',id,'plan',[c.plan]);
  if(c.completion) {
    const {retained_attachments,...body}=c.completion;
    insert(db,'completions',{change_id:id,...Object.fromEntries(Object.entries(body).map(([k,v])=>[k,['actor','governing_references','acceptance','limitations'].includes(k)?stringify(v):v]))});
    addAttachments('completion',id,retained_attachments);
  }
  c.completion_notes.forEach((note,ordinal)=>insert(db,'completion_notes',{change_id:id,ordinal,...note,actor:stringify(note.actor)}));
}
