import { readSync, lstatSync, realpathSync, readFileSync, mkdirSync, openSync, writeFileSync, fsyncSync, closeSync, unlinkSync, existsSync } from 'node:fs';
import { resolve, join, relative, isAbsolute } from 'node:path';
import { randomUUID, createHash } from 'node:crypto';
import { owner } from './operational-coordination.js';
import { fail, exact, parseInput } from './operational-contract.js';

export function stat(path) { try { return lstatSync(path); } catch (error) { if (error.code === 'ENOENT') return null; throw error; } }
export function regular(path, optional = false) {
  const value = stat(path);
  if (!value && optional) return null;
  if (!value?.isFile() || value.isSymbolicLink()) fail('invalid-request', 'Expected a contained regular file.');
  return value;
}
export function directory(path, create = false) {
  let value = stat(path);
  if (!value && create) { try { mkdirSync(path, { mode: 0o700 }); } catch (error) { if (error.code !== 'EEXIST') throw error; } value = stat(path); }
  if (!value?.isDirectory() || value.isSymbolicLink()) fail('invalid-request', 'Expected an owned regular directory.');
  return path;
}
export function contained(root, path, { absent = false } = {}) {
  if (typeof path !== 'string' || !path || path.includes('\\') || isAbsolute(path) || /^[A-Za-z]:/.test(path) || path.split('/').some(p => !p || p === '.' || p === '..') || /[\x00-\x1f]/.test(path)) fail('invalid-request', 'Invalid project-relative path.');
  const full = resolve(root, path);
  if (relative(root, full).startsWith('..')) fail('invalid-request', 'Path leaves the selected project.');
  const parts = path.split('/');
  for (let i = 1; i < parts.length; i++) {
    const entry = stat(join(root, ...parts.slice(0, i)));
    if (!entry && absent) return full;
    if (!entry?.isDirectory() || entry.isSymbolicLink()) fail('invalid-request', 'Unsafe project path component.');
  }
  if (stat(full)?.isSymbolicLink()) fail('invalid-request', 'Symbolic-link subjects are not admitted.');
  return full;
}
export function project(root) {
  root = resolve(root);
  directory(root);
  if (realpathSync(root) !== root) fail('invalid-request', 'Project root must be canonical.');
  const file = join(root, '.rigorloop.json');
  regular(file);
  if (stat(file).size > 4096) fail('size-limit', 'Project identity configuration is too large.');
  let configuration;
  try { configuration = parseInput(readFileSync(file)); } catch { fail('invalid-request', 'Invalid project identity configuration.'); }
  exact(configuration, ['schema_version', 'project_id']);
  if (configuration.schema_version !== 1 || !/^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i.test(configuration.project_id)) fail('project-mismatch', 'A supported explicit project UUID is required.');
  return { root, id: configuration.project_id };
}
export function durableWrite(path, value) {
  const fd = openSync(path, 'wx', 0o600);
  try { writeFileSync(fd, value); fsyncSync(fd); } finally { closeSync(fd); }
}
export function syncDirectory(path) {
  const fd = openSync(path, 'r');
  try { fsyncSync(fd); } finally { closeSync(fd); }
}
export function acquireLease(info) {
  const runtime = directory(join(info.root, '.rigorloop'), true);
  const access = directory(join(runtime, 'access'), true);
  const fence = join(runtime, 'maintenance/active.json');
  if (existsSync(fence)) fail('store-busy', 'Project storage is fenced for maintenance.');
  const id = randomUUID(), path = join(access, id + '.json');
  const value = JSON.stringify({ id, project_id: info.id, owner: owner() });
  durableWrite(path, value); syncDirectory(access);
  const release = () => {
    try { if (regular(path, true) && readFileSync(path, 'utf8') === value) { unlinkSync(path); syncDirectory(access); } }
    catch { /* A coordination cleanup error cannot change an established commit. */ }
  };
  if (existsSync(fence)) { release(); fail('store-busy', 'Maintenance began during connection admission.'); }
  return { runtime, release };
}
export function checkSubjects(root, subjects) {
  for (const subject of subjects) {
    const path = contained(root, subject.path, { absent: subject.state === 'absent' });
    const observed = stat(path);
    if (subject.state === 'absent') {
      if (subject.identity !== null || observed) fail('source-conflict', 'A declared absent subject is present or invalid.');
    } else {
      regular(path);
      if (subject.identity !== null) {
        const identity = 'sha256:' + createHash('sha256').update(readFileSync(path)).digest('hex');
        if (identity !== subject.identity) fail('source-conflict', 'A compared subject changed.');
      }
    }
  }
}

export function observeSubjects(root, selection) {
  if(new Set(selection.map(s=>s.path)).size!==selection.length)fail('invalid-request','Duplicate selected subject path.');
  return selection.map(s=>{
    const path=contained(root,s.path,{absent:s.state==='absent'}),before=stat(path);
    if(s.state==='absent') {
      if(before)fail('source-conflict','A selected absent subject exists.');
      return {...s,identity:null};
    }
    regular(path);
    const hash=createHash('sha256'),fd=openSync(path,'r');
    try {
      const chunk=Buffer.alloc(65536);let count;
      while((count=readSync(fd,chunk,0,chunk.length,null))>0)hash.update(chunk.subarray(0,count));
    } finally {closeSync(fd);}
    const after=stat(path);
    if(!after||['dev','ino','size','mtimeMs','ctimeMs'].some(k=>before[k]!==after[k]))fail('source-conflict','Selected subject changed during observation.');
    return {...s,identity:'sha256:'+hash.digest('hex')};
  });
}
