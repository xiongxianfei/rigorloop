import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {executeRecordStore} from '../dist/lib/record-store.js';
import {executeWorkflowContext} from '../dist/lib/workflow-context.js';
const old={request:{schema_version:1,contract:'explicit-recording-v1'}};
function setup(t){const root=mkdtempSync(join(tmpdir(),'retirement-'));t.after(()=>rmSync(root,{recursive:true,force:true}));mkdirSync(join(root,'.git'));mkdirSync(join(root,'docs/changes/example'),{recursive:true});return root;}
test('retired stored v1 rejects inspection and creation without mutation',t=>{const root=setup(t),path=join(root,'docs/changes/example/change.yaml'),bytes='Uninterpreted archival bytes\n';writeFileSync(path,bytes);assert.equal(executeRecordStore({root,changeId:'example',operation:'inspect'}).errors[0]?.code,'unsupported-contract');assert.equal(executeRecordStore({root,changeId:'example',operation:'check',request:old.request}).errors[0]?.code,'unsupported-contract');assert.equal(readFileSync(path,'utf8'),bytes);});
test('discovery excludes sole archival YAML without parsing and explicit selection rejects it',t=>{const root=setup(t);writeFileSync(join(root,'docs/changes/example/change.yaml'),'archival bytes: [ intentionally malformed');const discovered=executeWorkflowContext(['--json'],{cwd:root});assert.equal(discovered.exitCode,0);assert.equal(discovered.result.schema_version,2);assert.deepEqual(discovered.result.candidates,[]);assert.equal(discovered.result.scope.excluded_noncurrent,1);assert.equal(executeWorkflowContext(['--change','example','--json'],{cwd:root}).result.errors[0]?.code,'unsupported-contract');});
test('reserved v2 residue outranks archival exclusion',t=>{const root=setup(t);writeFileSync(join(root,'docs/changes/example/change.yaml'),'archive');writeFileSync(join(root,'docs/changes/example/evidence.json'),'{}');const r=executeWorkflowContext(['--json'],{cwd:root});assert.equal(r.exitCode,2);assert.equal(r.result.errors[0]?.code,'invalid-input');assert.equal(r.result.scope.complete,false);});
for(const contract of ['explicit-recording-v1','compact-current-state-v1','stage-owned-change-local-v1','stage-owned-change-local-v2','stage-owned-change-local-v3','legacy-unversioned'])test(`retired ${contract} has no advanced acceptance or archival reinterpretation`,t=>{
 const root=setup(t),path=join(root,'docs/changes/example/change.yaml'),bytes=`contract: ${contract}\narchival: [ uninterpreted`;
 writeFileSync(path,bytes);
 for(const operation of ['inspect','check','record']){
  const result=executeRecordStore({root,changeId:'example',operation,...(operation==='inspect'?{}:{request:{schema_version:1,contract}})});
  assert.equal(result.errors[0]?.code,'unsupported-contract');assert.equal(readFileSync(path,'utf8'),bytes);
 }
});
