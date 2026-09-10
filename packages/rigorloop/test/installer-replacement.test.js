import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, rmSync, symlinkSync, openSync, closeSync, writeSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { installCandidate } from '../dist/lib/installer-replacement.js';
const unit='.agents/skills/design';
function fixture(t) { const root=mkdtempSync(join(tmpdir(),'distribution-')); t.after(()=>rmSync(root,{recursive:true,force:true})); return root; }
function old(root) { mkdirSync(join(root,unit),{recursive:true}); writeFileSync(join(root,unit,'old.md'),'old'); }
const files=[{path:`${unit}/SKILL.md`,content:Buffer.from('new')}];
test('fresh install and default identical or empty directory conflicts are whole-candidate',t=>{ const root=fixture(t); installCandidate({projectRoot:root,files}); assert.equal(readFileSync(join(root,files[0].path),'utf8'),'new'); assert.throws(()=>installCandidate({projectRoot:root,files:[...files,{path:'.agents/skills/new/SKILL.md',content:Buffer.from('x')}]}),e=>e.code==='destination-conflict'&&e.conflicts.includes(unit)); assert.equal(existsSync(join(root,'.agents/skills/new')),false); });
test('force detaches directly outside discovery and preserves late old-inode writes',t=>{ const root=fixture(t); old(root); const fd=openSync(join(root,unit,'old.md'),'r+'); t.after(()=>closeSync(fd)); const result=installCandidate({projectRoot:root,files,force:true,checkpoint(event){ if(event===`detached:${unit}`) assert.equal(existsSync(join(root,unit)),false); }}); assert.equal(existsSync(join(root,unit,'old.md')),false); writeSync(fd,Buffer.from('late'),0,4,0); assert.equal(readFileSync(join(result.retained[0].backup,'old.md'),'utf8'),'late'); assert.ok(!result.retained[0].backup.includes('/skills/')); });
test('force cannot clobber a newly appearing destination after detach',t=>{ const root=fixture(t); old(root); assert.throws(()=>installCandidate({projectRoot:root,files,force:true,checkpoint(event){ if(event===`detached:${unit}`) writeFileSync(join(root,unit),'independent'); }}),e=>e.retained.length===1&&e.completed.length===0); assert.equal(readFileSync(join(root,unit),'utf8'),'independent'); });
test('source changes after preflight stop before detachment',t=>{ const root=fixture(t); old(root); assert.throws(()=>installCandidate({projectRoot:root,files,force:true,checkpoint(event){if(event==='preflight')writeFileSync(join(root,unit,'old.md'),'changed');}})); assert.equal(readFileSync(join(root,unit,'old.md'),'utf8'),'changed'); });
test('symlinks, unsafe paths and unsafe retention placement block force',t=>{const root=fixture(t);old(root);symlinkSync('/tmp',join(root,unit,'link'));assert.throws(()=>installCandidate({projectRoot:root,files,force:true})); assert.throws(()=>installCandidate({projectRoot:root,files:[{path:'../escape',content:Buffer.from('x')}],force:true}));rmSync(join(root,unit,'link'));assert.throws(()=>installCandidate({projectRoot:root,files,force:true,discoveryRoots:['.']}));assert.ok(existsSync(join(root,unit,'old.md')));});
test('unsupported anchoring rejects before detachment',t=>{const root=fixture(t);old(root);assert.throws(()=>installCandidate({projectRoot:root,files,force:true,descriptorRoot:'/unavailable-fd-filesystem'}));assert.ok(existsSync(join(root,unit,'old.md')));});
test('interruption reports partial progress and default retry conflicts',t=>{const root=fixture(t);old(root);assert.throws(()=>installCandidate({projectRoot:root,files,force:true,checkpoint(event){if(event===`published:${unit}`)throw Error('interrupted');}}),e=>e.completed.includes(unit)&&e.retained.length===1);assert.throws(()=>installCandidate({projectRoot:root,files}),e=>e.code==='destination-conflict');});

test('a new directory after detach is not adopted even under force',t=>{const root=fixture(t);old(root);assert.throws(()=>installCandidate({projectRoot:root,files,force:true,checkpoint(event){if(event===`detached:${unit}`)mkdirSync(join(root,unit));}}));assert.equal(existsSync(join(root,unit,'SKILL.md')),false);});
test('force replaces regular file with skill directory and standalone file',t=>{const root=fixture(t);mkdirSync(join(root,'.agents/skills'),{recursive:true});writeFileSync(join(root,unit),'old');installCandidate({projectRoot:root,files,force:true});const standalone=[{path:'.agents/skills/helper.md',content:Buffer.from('one')}];installCandidate({projectRoot:root,files:standalone});installCandidate({projectRoot:root,files:[{...standalone[0],content:Buffer.from('two')}],force:true});assert.equal(readFileSync(join(root,standalone[0].path),'utf8'),'two');});
test('empty destinations conflict and all conflicts are listed',t=>{const root=fixture(t);mkdirSync(join(root,unit),{recursive:true});mkdirSync(join(root,'.agents/skills/other'));assert.throws(()=>installCandidate({projectRoot:root,files:[...files,{path:'.agents/skills/other/SKILL.md',content:Buffer.from('x')}]}),e=>e.conflicts.length===2);});
test('ancestor replaced after preflight is preserved without escaping writes',t=>{const root=fixture(t);old(root);assert.throws(()=>installCandidate({projectRoot:root,files,force:true,checkpoint(event){if(event==='preflight'){rmSync(join(root,'.agents'),{recursive:true});symlinkSync('/tmp',join(root,'.agents'));}}}));assert.ok(existsSync(join(root,'.agents')));});

test('configured discovery alias and missing child below an alias reject before detach',t=>{
  const root=fixture(t);old(root);symlinkSync(root,join(root,'alias'));
  for(const discovery of ['alias','alias/missing']) {
    assert.throws(()=>installCandidate({projectRoot:root,files,force:true,discoveryRoots:[discovery]}),/discovery root traverses a symlink/);
    assert.equal(readFileSync(join(root,unit,'old.md'),'utf8'),'old');
  }
});
test('mid-publication failure reports completed failed and untouched units and preserves retry conflicts',t=>{
  const root=fixture(t);old(root);
  const candidate=[{path:'.agents/skills/a/SKILL.md',content:Buffer.from('first')},...files,{path:`${unit}/resource.md`,content:Buffer.from('resource')},{path:'.agents/skills/z/SKILL.md',content:Buffer.from('last')}];
  let stopped;
  assert.throws(()=>installCandidate({projectRoot:root,files:candidate,force:true,checkpoint(event){if(event===`file-published:${files[0].path}`)throw Error('interrupted');}}),e=>{stopped=e;return e.message==='interrupted';});
  assert.deepEqual(stopped.completed,['.agents/skills/a']);assert.equal(stopped.failed,unit);assert.deepEqual(stopped.untouched,['.agents/skills/z']);
  assert.equal(readFileSync(join(root,files[0].path),'utf8'),'new');assert.equal(existsSync(join(root,unit,'resource.md')),false);assert.equal(existsSync(join(root,'.agents/skills/z')),false);
  assert.equal(readFileSync(join(stopped.retained[0].backup,'old.md'),'utf8'),'old');
  writeFileSync(join(root,files[0].path),'independent');
  assert.throws(()=>installCandidate({projectRoot:root,files:candidate}),e=>e.conflicts.includes(unit));assert.equal(readFileSync(join(root,files[0].path),'utf8'),'independent');
});
