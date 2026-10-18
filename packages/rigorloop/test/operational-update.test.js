import assert from 'node:assert/strict';
import { test } from 'node:test';
import { DatabaseSync } from 'node:sqlite';
import { cli,project,actor,createInput,invoke,databasePath } from './helpers/operational-fixture.mjs';
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

test('operational commit errors report rollback or uncertainty and inspection reconciles actual state',async t=>{
  const {spawnSync}=await import('node:child_process');
  const {fileURLToPath}=await import('node:url');
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
