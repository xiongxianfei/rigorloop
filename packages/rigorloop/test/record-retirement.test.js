import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdirSync,writeFileSync,readFileSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {cli,project,invoke,createInput} from './helpers/operational-fixture.mjs';

test('retired commands cannot read, mutate or recover archived filesystem records',t=>{
  const root=project(t),path=join(root,'docs/changes/navigation/change.json');
  mkdirSync(join(root,'docs/changes/navigation'),{recursive:true});
  const original='Historical unsupported content must remain byte-exact.\n';writeFileSync(path,original);
  for(const args of [['workflow-context'],['record-store','record'],['status'],['work','add','item'],['verify','record'],['subject','inspect'],['batch'],['compact'],['lifecycle'],['new-change']]){
    const result=spawnSync(process.execPath,[cli,...args,'--root',root,'--change','navigation','--input','-','--format','json'],{cwd:root,input:'unparseable input',encoding:'utf8'});
    assert.notEqual(result.status,0);assert.match(result.stdout,/invalid-usage/);
    assert.equal(readFileSync(path,'utf8'),original);
    assert.equal(existsSync(join(root,'.rigorloop')),false);
  }
  const created=invoke(root,['change','create'],createInput());assert.equal(created.exit,0,JSON.stringify(created));
  assert.equal(readFileSync(path,'utf8'),original);
  assert.equal(invoke(root,['change','context']).exit,0);
});
