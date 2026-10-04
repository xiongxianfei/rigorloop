import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, rmSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { installCandidate } from '../dist/lib/installer-replacement.js';
import { workflowContract, validateWorkflowDescriptor } from '../dist/lib/workflow-package.js';
import { projectConciseResult } from '../dist/lib/result-renderer.js';

const root='.agents/skills';
const retireUnits=['design','proposal','proposal-review'].map(name=>`${root}/${name}`);
const files=workflowContract.required_skills.map(name=>({path:`${root}/${name}/SKILL.md`, content:Buffer.from(`candidate ${name}`)}));
function fixture(t) {
  const projectRoot=mkdtempSync(join(tmpdir(),'workflow-replacement-'));
  t.after(()=>rmSync(projectRoot,{recursive:true,force:true}));
  for(const path of [...retireUnits, '.claude/skills/design', '.codex/skills/proposal', `${root}/custom`]) {
    mkdirSync(join(projectRoot,path),{recursive:true});
    writeFileSync(join(projectRoot,path,'custom.md'),`original ${path}`);
  }
  return projectRoot;
}
test('explicit profile retires only selected units with exact originals outside discovery',t=>{
  const projectRoot=fixture(t);
  assert.throws(()=>installCandidate({projectRoot,files,roots:[root],retireUnits}),/force/);
  const result=installCandidate({projectRoot,files,roots:[root],retireUnits,force:true});
  for(const path of retireUnits) {
    assert.equal(existsSync(join(projectRoot,path)),false);
    const row=result.unit_results.find(r=>r.path===path);
    assert.equal(row.action,'retire');assert.equal(row.outcome,'completed');
    assert.equal(readFileSync(join(row.retained_path,'custom.md'),'utf8'),`original ${path}`);
    assert.ok(!row.retained_path.includes('/skills/'));
  }
  for(const path of ['.claude/skills/design','.codex/skills/proposal',`${root}/custom`]) assert.equal(readFileSync(join(projectRoot,path,'custom.md'),'utf8'),`original ${path}`);
  for(const file of files) assert.deepEqual(readFileSync(join(projectRoot,file.path)),file.content);
  const retry=installCandidate({projectRoot,files,roots:[root],retireUnits,force:true});
  assert.ok(retry.unit_results.filter(r=>r.action==='retire').every(r=>r.outcome==='absent'));
});
test('recreated obsolete path stops without second detach or publishing candidates',t=>{
  const projectRoot=fixture(t), first=retireUnits[0];
  let caught;
  try { installCandidate({projectRoot,files,roots:[root],retireUnits,force:true,checkpoint(event){
    if(event===`retired:${first}`) {mkdirSync(join(projectRoot,first));writeFileSync(join(projectRoot,first,'competing'),'keep');}
  }}); } catch(error){caught=error;}
  assert.ok(caught);assert.equal(caught.retained.length,1);
  assert.equal(readFileSync(join(projectRoot,first,'competing'),'utf8'),'keep');
  assert.equal(existsSync(join(projectRoot,files[0].path)),false);
  assert.equal(caught.unit_results.find(r=>r.path===retireUnits[1]).outcome,'untouched');
  const projected=projectConciseResult({command:'init',status:'blocked',unit_results:caught.unit_results},{invocationId:'test',exitCode:2});
  assert.deepEqual(projected.unit_results,caught.unit_results);
});
test('candidate interruption preserves retired originals and reports partial candidate effects',t=>{
  const projectRoot=fixture(t);
  let caught;
  try {installCandidate({projectRoot,files,roots:[root],retireUnits,force:true,checkpoint(event){if(event.startsWith('file-published:'))throw new Error('interrupted');}});}catch(error){caught=error;}
  assert.equal(caught.retained.length,3);
  assert.ok(caught.unit_results.filter(r=>r.action==='retire').every(r=>r.outcome==='completed'));
  assert.equal(caught.unit_results.filter(r=>r.outcome==='partial').length,1);
  for(const path of retireUnits)assert.equal(existsSync(join(projectRoot,path)),false);
  assert.throws(()=>installCandidate({projectRoot,files,roots:[root]}),e=>e.code==='destination-conflict');
});
test('descriptor rejects unknown vocabulary, extra fields, duplicate keys and unsafe retirement names',()=>{
  assert.deepEqual(validateWorkflowDescriptor(Buffer.from(JSON.stringify(workflowContract))),workflowContract);
  for(const value of [{...workflowContract,schema_version:99},{...workflowContract,workflow_contract:'invented'}, {...workflowContract,extra:true}, {...workflowContract,retired_skills:['../custom']}]) assert.throws(()=>validateWorkflowDescriptor(Buffer.from(JSON.stringify(value))));
  assert.throws(()=>validateWorkflowDescriptor(Buffer.from(JSON.stringify(workflowContract).replace('"schema_version":1','"schema_version":1,"schema_version":1'))));
});
test('replacement grammar rejects before acquisition; preliminary dry run leaves target unchanged',t=>{
  const projectRoot=fixture(t), cli=fileURLToPath(new URL('../dist/bin/rigorloop.js',import.meta.url));
  const before=readdirSync(projectRoot).sort();
  for(const args of [ ['--replace-workflow','unknown','--force'], ['--replace-workflow','requirement-first-v1'], ['--replace-workflow','requirement-first-v1','--replace-workflow','requirement-first-v1','--force'] ]) {
    const result=spawnSync(process.execPath,[cli,'init','codex',...args,'--json','--no-file-log'],{cwd:projectRoot,encoding:'utf8'});
    assert.notEqual(result.status,0);assert.doesNotMatch(result.stdout,/download-failed|metadata-missing/);
  }
  const result=spawnSync(process.execPath,[cli,'init','codex','--replace-workflow','requirement-first-v1','--force','--dry-run','--json','--no-file-log'],{cwd:projectRoot,encoding:'utf8'});
  assert.equal(result.status,0,result.stdout+result.stderr);
  const output=JSON.parse(result.stdout);assert.equal(output.schema_version,2);
  assert.deepEqual(output.possible_retirements,[...workflowContract.retired_skills].map(name=>`${root}/${name}`));
  assert.deepEqual(readdirSync(projectRoot).sort(),before);
});
