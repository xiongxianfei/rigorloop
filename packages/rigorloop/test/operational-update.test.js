import assert from 'node:assert/strict';
import { test } from 'node:test';
import { DatabaseSync } from 'node:sqlite';
import { project,actor,createInput,invoke,databasePath } from './helpers/operational-fixture.mjs';
const body = (revision,input) => ({...createInput(),expected_revision:revision,input});
const work = (id,status='in-progress') => ({id,status,owner:actor,scope:'Navigation',locations:[],remaining:'Run relevant checks',check_refs:[],blocker_ids:[],completion_reason:null});
const blocker = id => ({id,reporter:actor,owner:actor,scope:'Navigation',description:'Missing behavior',required_outcome:'Correct it',state:'open',disposition:null});
function start(t) {
  const root=project(t),saved=invoke(root,['change','create'],createInput());
  assert.equal(saved.exit,0,JSON.stringify(saved));return {root,revision:saved.result.revision};
}
const select = (root,kind,id) => invoke(root,['change','context'],{schema_version:2,interface:'targeted-recording-v2',contract:'rigorloop-records-v4',selectors:[{kind,id}],include_observations:false}).result.items[0].value;

test('operational update persists named work and issues, preserves omissions and rejects stale intent',t=>{
  const {root,revision}=start(t);
  const saved=invoke(root,['change','update'],body(revision,{work:[work('first'),work('second')],blockers:[blocker('missing')]}));
  assert.equal(saved.exit,0,JSON.stringify(saved));assert.equal(saved.result.committed,true);
  const resolved=blocker('missing');resolved.state='resolved';resolved.disposition={actor,reason:'Implementation corrected',follow_up:null};
  const next=invoke(root,['change','update'],body(saved.result.revision,{blockers:[resolved],work:[{...work('first','completed'),completion_reason:'Relevant checks passed',remaining:null}]}));
  assert.equal(next.exit,0,JSON.stringify(next));
  const change=select(root,'change','navigation');
  assert.deepEqual(change.work.map(w=>[w.id,w.status]),[['first','completed'],['second','in-progress']]);
  assert.equal(change.blockers[0].state,'resolved');
  const stale=invoke(root,['change','update'],body(saved.result.revision,{next_action:null}));
  assert.equal(stale.result.status,'conflict');assert.equal(stale.result.committed,false);
  assert.equal(invoke(root,['change','context']).result.revision,next.result.revision);
});

test('operational update is atomic on bad references, unsupported fields and missing dispositions',t=>{
  const {root,revision}=start(t);
  for(const input of [{work:[{...work('first'),check_refs:[{kind:'evidence',id:'absent'}]}]}, {blockers:[{...blocker('missing'),state:'resolved'}]}, {work:[{...work('first'),status:'unknown'}]}, {completion:{summary:'Pretend complete'}}, {}]) {
    const rejected=invoke(root,['change','update'],body(revision,input));
    assert.equal(rejected.exit,2,JSON.stringify(rejected));assert.equal(rejected.result.committed,false);
    assert.equal(invoke(root,['change','context']).result.revision,revision);
  }
  const db=new DatabaseSync(databasePath(root),{readOnly:true});
  assert.equal(db.prepare('SELECT count(*) AS n FROM accounts').get().n,0);db.close();
});

test('operational unchanged update has no revision effects but still requires current preconditions',t=>{
  const {root,revision}=start(t),input={next_action:createInput().input.next_action};
  const same=invoke(root,['change','update'],body(revision,input));
  assert.equal(same.result.status,'unchanged');assert.equal(same.result.revision,revision);assert.equal(same.result.committed,false);
  const preview=invoke(root,['change','update'],body(revision,{next_action:null}),['--dry-run']);
  assert.equal(preview.result.status,'preview');assert.equal(preview.result.committed,false);
  assert.equal(invoke(root,['change','context']).result.revision,revision);
});

const evidence = (id='navigation-check') => ({id,actor,reported_at:'2026-10-04T10:00:00Z',procedure:'Run navigation checks',scope:'Navigation behavior',subjects:[],observation:{method:'reported',actor,scope:'Navigation behavior',summary:'Engineer reports this candidate was checked'},result:'passed',summary:'Navigation checks passed',limitations:[],attachments:[]});
test('operational evidence replacement preserves its procedure and scope and stores queryable results',t=>{
  const {root,revision}=start(t);
  const first=invoke(root,['change','update'],body(revision,{evidence:[{...evidence(),result:'failed',summary:'Navigation check failed'}]}));
  assert.equal(first.exit,0,JSON.stringify(first));
  const unrelated=invoke(root,['change','update'],body(first.result.revision,{evidence:[{...evidence(),procedure:'Run smoke checks'}]}));
  assert.equal(unrelated.exit,2);
  assert.equal(select(root,'evidence','navigation-check').result,'failed');
  const replacement=invoke(root,['change','update'],body(first.result.revision,{evidence:[evidence()],work:[{...work('navigation'),check_refs:[{kind:'evidence',id:'navigation-check'}]}]}));
  assert.equal(replacement.exit,0,JSON.stringify(replacement));
  const db=new DatabaseSync(databasePath(root),{readOnly:true});
  assert.equal(db.prepare('SELECT result FROM evidence WHERE id=?').get('navigation-check').result,'passed');
  assert.equal(db.prepare('SELECT target_id FROM account_refs WHERE owner_kind=?').get('work').target_id,'navigation-check');db.close();
});

test('operational retained attachments stay stable while caller output changes and support safe compaction',async t=>{
  const {writeFileSync,readFileSync,existsSync}=await import('node:fs');
  const {join}=await import('node:path');
  const {root,revision}=start(t);const source=join(root,'test-output.txt');writeFileSync(source,'original selected result');
  const value={...evidence(),attachments:['selected.txt'],retain:[{name:'selected.txt',source:'test-output.txt',media_type:'text/plain'}]};
  const preview=invoke(root,['change','update'],body(revision,{evidence:[value]}),['--dry-run']);
  assert.equal(preview.exit,0,JSON.stringify(preview));
  const retained=join(root,'.rigorloop/artifacts/changes/navigation/selected.txt');assert.equal(existsSync(retained),false);
  const saved=invoke(root,['change','update'],body(revision,{evidence:[value]}));assert.equal(saved.exit,0,JSON.stringify(saved));
  writeFileSync(source,'new routine run');assert.equal(readFileSync(retained,'utf8'),'original selected result');
  const metadata=select(root,'attachment','selected.txt');assert.equal(metadata.byte_count,24);
  const replace=invoke(root,['change','update'],body(saved.result.revision,{evidence:[value]}));assert.equal(replace.exit,2);assert.equal(readFileSync(retained,'utf8'),'original selected result');
  const drop=invoke(root,['change','update'],body(saved.result.revision,{retention:{drop:[{kind:'attachment',id:'selected.txt'}],reason:'Attempt to discard still-used detail',actor}}));assert.equal(drop.exit,2);
  const compact=invoke(root,['change','update'],body(saved.result.revision,{evidence:[evidence()],retention:{drop:[{kind:'attachment',id:'selected.txt'}],reason:'Summary is sufficient; log has no remaining reliance',actor}}));assert.equal(compact.exit,0,JSON.stringify(compact));assert.equal(existsSync(retained),false);
});

test('operational commit errors report rollback or uncertainty and inspection reconciles actual state',async t=>{
  const {spawnSync}=await import('node:child_process');
  const {fileURLToPath}=await import('node:url');
  const cli=fileURLToPath(new URL('../dist/bin/rigorloop.js',import.meta.url));
  const fault=fileURLToPath(new URL('./helpers/operational-sqlite-fault.mjs',import.meta.url));
  for(const mode of ['before','after']) {
    const {root,revision}=start(t);
    const p=spawnSync(process.execPath,['--import',fault,cli,'change','update','--root',root,'--change','navigation','--input','-','--format','json'],{input:JSON.stringify(body(revision,{work:[work('actual')]})),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_COMMIT_FAULT:mode}});
    const result=JSON.parse(p.stdout);assert.equal(p.status,1,p.stdout+p.stderr);
    assert.equal(result.committed,mode==='before'?false:null);
    assert.equal(result.status,'failed');assert.ok(!p.stdout.includes('test-only private'));
    const current=select(root,'change','navigation');assert.equal(current.work.length,mode==='before'?0:1);
  }
});

test('operational failed record commit leaves an explicit recoverable attachment orphan',async t=>{
  const {spawnSync}=await import('node:child_process');
  const {fileURLToPath}=await import('node:url');
  const {writeFileSync,existsSync,readFileSync}=await import('node:fs');
  const {join}=await import('node:path');
  const cli=fileURLToPath(new URL('../dist/bin/rigorloop.js',import.meta.url));
  const fault=fileURLToPath(new URL('./helpers/operational-sqlite-fault.mjs',import.meta.url));
  for(const disposition of ['reuse','remove']) {
    const {root,revision}=start(t);writeFileSync(join(root,'result.txt'),'selected result');
    const input={evidence:[{...evidence(),attachments:['result.txt'],retain:[{name:'result.txt',source:'result.txt',media_type:'text/plain'}]}]};
    const p=spawnSync(process.execPath,['--import',fault,cli,'change','update','--root',root,'--change','navigation','--input','-','--format','json'],{input:JSON.stringify(body(revision,input)),encoding:'utf8',env:{...process.env,RIGORLOOP_TEST_COMMIT_FAULT:'before'}});
    const rejected=JSON.parse(p.stdout);assert.equal(rejected.committed,false);assert.match(rejected.errors[0].message,/may remain unused/);
    const retained=join(root,'.rigorloop/artifacts/changes/navigation/result.txt');assert.equal(readFileSync(retained,'utf8'),'selected result');
    assert.equal(select(root,'change','navigation').attachments.length,0);
    assert.equal(invoke(root,['change','context']).result.revision,revision);
    const nextInput=disposition==='reuse'?input:{retention:{drop:[{kind:'attachment',id:'result.txt'}],actor,reason:'Unused failed-publication detail is no longer needed'}};
    const saved=invoke(root,['change','update'],body(revision,nextInput));assert.equal(saved.exit,0,JSON.stringify(saved));assert.equal(saved.result.committed,true);
    assert.equal(existsSync(retained),disposition==='reuse');
  }
});

test('operational attachment admission rejects unsafe sources and byte/count overflow without revision effects',async t=>{
  const {writeFileSync,symlinkSync,truncateSync}=await import('node:fs');const {join}=await import('node:path');
  const {root,revision}=start(t);writeFileSync(join(root,'safe.txt'),'safe');symlinkSync(join(root,'safe.txt'),join(root,'alias.txt'));
  writeFileSync(join(root,'large.txt'),'');truncateSync(join(root,'large.txt'),64*1024*1024+1);
  const retain=source=>[{name:'selected.txt',source,media_type:'text/plain'}];
  for(const [selection,code] of [[retain('alias.txt'),'invalid-request'],[retain('large.txt'),'size-limit'],[retain('../foreign'),'invalid-request'],[Array.from({length:65},(_,i)=>({name:'report-'+i,source:'safe.txt',media_type:'text/plain'})),'size-limit']]) {
    const r=invoke(root,['change','update'],body(revision,{evidence:[{...evidence(),retain:selection}]}));
    assert.equal(r.result.errors[0].code,code,JSON.stringify(r));assert.equal(r.result.committed,false);
    assert.equal(invoke(root,['change','context']).result.revision,revision);
  }
});
