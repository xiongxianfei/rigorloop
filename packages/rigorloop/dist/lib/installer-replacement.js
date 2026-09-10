// Candidate-unit filesystem installation. No project-state or recovery readers.
import { constants, openSync, closeSync, fstatSync, lstatSync, readdirSync, readFileSync, mkdirSync, writeFileSync, renameSync, linkSync, unlinkSync, realpathSync } from 'node:fs';
import { createHash, randomBytes } from 'node:crypto';
import { resolve, join, dirname, basename } from 'node:path';
const failure = (message, code='unsafe-destination') => Object.assign(new Error(message), {code});
const equal = (a,b) => JSON.stringify(a)===JSON.stringify(b);
const identity = s => [s.dev,s.ino];
function stat(path) { try { return lstatSync(path); } catch(e) { if(e.code==='ENOENT') return null; throw e; } }
function relative(path) {
  if(typeof path!=='string'||!path||path.startsWith('/')||path.includes('\\')||path.includes('\0')||path.split('/').some(p=>!p||p==='.'||p==='..')) throw failure('Unsafe candidate path.');
  return path;
}
export function candidateUnits(files, roots=['.agents/skills','.claude/skills']) {
  const units=new Set(); const seen=new Set();
  for(const file of files) {
    relative(file.path);
    if(!Buffer.isBuffer(file.content)||seen.has(file.path)) throw failure('Invalid or duplicate candidate file.');
    seen.add(file.path);
    const root=roots.find(r=>file.path.startsWith(`${r}/`));
    if(!root) throw failure('Candidate lies outside declared install roots.');
    const child=file.path.slice(root.length+1).split('/')[0];
    units.add(`${root}/${child}`);
  }
  if(!units.size) throw failure('Candidate contains no files.');
  return [...units].sort();
}

export function installCandidate({projectRoot, files, roots, force=false, dryRun=false, discoveryRoots=[], descriptorRoot='/proc/self/fd', checkpoint=()=>{}}) {
  projectRoot=resolve(projectRoot);
  const units=candidateUnits(files,roots);
  const handles=new Set(); const parents=new Map();
  const retained=[]; const completed=[]; let active=null; let retention=null;
  function pin(path) {
    const fd=openSync(path,constants.O_RDONLY|constants.O_DIRECTORY|constants.O_NOFOLLOW);
    handles.add(fd);
    const info=fstatSync(fd);
    if(!info.isDirectory()) throw failure('Unsafe destination parent.');
    const anchored=`${descriptorRoot}/${fd}`;
    // This capability is essential: both rename endpoints must resolve to
    // opened directory objects, never to mutable ancestor pathnames.
    if(!equal(identity(lstatSync(`${anchored}/.`)),identity(info))) throw failure('Descriptor-relative filesystem operations are unavailable.');
    return {fd,path:anchored,id:identity(info),dev:info.dev};
  }
  function inspect(path) {
    const info=stat(path); if(!info)return null;
    if(info.isSymbolicLink())throw failure(`Symlink is unsafe: ${path}`);
    if(info.isDirectory()) {
      const dir=pin(path);
      try { return {kind:'directory',id:dir.id,mode:info.mode,entries:readdirSync(dir.path).sort().map(n=>[n,inspect(`${dir.path}/${n}`)])}; } finally { closeSync(dir.fd);handles.delete(dir.fd); }
    }
    if(!info.isFile())throw failure(`Unsupported destination type: ${path}`);
    const fd=openSync(path,constants.O_RDONLY|constants.O_NOFOLLOW);handles.add(fd);
    const before=fstatSync(fd); if(!before.isFile()||!equal(identity(info),identity(before)))throw failure('Destination changed during inspection.');
    const hash=createHash('sha256').update(readFileSync(fd)).digest('hex');
    const after=fstatSync(fd);
    if(before.size!==after.size||before.mtimeMs!==after.mtimeMs||before.ctimeMs!==after.ctimeMs)throw failure('Destination changed during inspection.');
    closeSync(fd);handles.delete(fd);return {kind:'file',id:identity(info),mode:info.mode,hash};
  }
  function checkParents() {
    if(realpathSync(projectRoot)!==projectRoot)throw failure('Project root changed.');
    for(const [path,pinned] of parents) {
      const actual=stat(path==='.'?projectRoot:join(projectRoot,path));
      if(!actual?.isDirectory()||actual.isSymbolicLink()||!equal(identity(actual),pinned.id))throw failure('Destination ancestor changed.');
    }
  }
  function parentFor(path,create=false) {
    const pieces=dirname(path)==='.'?[]:dirname(path).split('/'); let key='.'; let parent=parents.get('.');
    for(const piece of pieces) {
      key=key==='.'?piece:`${key}/${piece}`;
      if(parents.has(key)){parent=parents.get(key);continue;}
      const child=`${parent.path}/${piece}`;
      if(create) { checkParents(); mkdirSync(child); } else if(!stat(child))return null;
      const next=pin(child); parents.set(key,next); parent=next;
    }
    return parent;
  }
  function actual(path) {const p=parentFor(path);return p?inspect(`${p.path}/${basename(path)}`):null;}
  try {
    if(realpathSync(projectRoot)!==projectRoot)throw failure('Project root must not traverse symlinks.');
    parents.set('.',pin(projectRoot));
    const basis=Object.fromEntries(units.map(unit=>[unit,actual(unit)]));
    const conflicts=units.filter(unit=>basis[unit]);
    checkParents();
    if(dryRun)return {units,conflicts,completed,retained};
    if(conflicts.length&&!force)throw Object.assign(failure('Destination skills already exist. Use --force to replace them.','destination-conflict'),{conflicts});
    checkpoint('preflight');
    // Validate all required placement/capability before detaching any original.
    const stageName=`.rigorloop-install-retained-${randomBytes(24).toString('hex')}`;
    for(const root of ['.agents/skills','.claude/skills','.codex/skills','.opencode',...discoveryRoots]) {
      const discovery=resolve(projectRoot,root); const stage=join(projectRoot,stageName);
      if(stage===discovery||stage.startsWith(`${discovery}/`)||discovery.startsWith(`${stage}/`))throw failure('Safe retention outside discovery cannot be established.');
    }
    checkParents();
    mkdirSync(`${parents.get('.').path}/${stageName}`,{mode:0o700});
    retention=pin(`${parents.get('.').path}/${stageName}`);parents.set(stageName,retention);
    for(const unit of units) {
      const p=parentFor(unit,true);
      if(p.dev!==retention.dev)throw failure('Cross-filesystem installation is unsupported.');
    }
    const expected={...basis};
    function assertCurrent() {checkParents();for(const unit of units)if(!equal(actual(unit),expected[unit]))throw failure(`Destination changed: ${unit}`);}
    assertCurrent();
    for(const unit of units) {
      active=unit; assertCurrent();
      const parent=parentFor(unit); const target=`${parent.path}/${basename(unit)}`;
      if(basis[unit]) {
        const name=`original-${randomBytes(24).toString('hex')}`;
        if(stat(`${retention.path}/${name}`))throw failure('Retention name collision.');
        renameSync(target,`${retention.path}/${name}`);
        retained.push({path:unit,backup:join(projectRoot,stageName,name)});
        expected[unit]=null;
        if(!equal(inspect(`${retention.path}/${name}`),basis[unit]))throw failure('Detached original changed; inspect retained content.');
        checkpoint(`detached:${unit}`);assertCurrent();
      }
      const selected=files.filter(f=>f.path===unit||f.path.startsWith(`${unit}/`));
      for(const file of selected) {
        const p=parentFor(file.path,true);checkParents();
        const temporary=`candidate-${randomBytes(24).toString('hex')}`;
        writeFileSync(`${retention.path}/${temporary}`,file.content,{flag:'wx',mode:0o644});
        linkSync(`${retention.path}/${temporary}`,`${p.path}/${basename(file.path)}`);
        unlinkSync(`${retention.path}/${temporary}`);
      }
      expected[unit]=actual(unit);
      // Independent bytes and exact membership, not a tree hash calculated by
      // the same archive oracle. Obsolete files cannot survive replacement.
      const expectedPaths=selected.map(f=>f.path).sort();const installed=[];
      function verify(path,node){if(node.kind==='file')installed.push(path);else for(const [name,child]of node.entries)verify(`${path}/${name}`,child);}
      verify(unit,expected[unit]);
      if(!equal(installed.sort(),expectedPaths))throw failure('Installed candidate inventory mismatch.');
      for(const file of selected){const p=parentFor(file.path);const value=inspect(`${p.path}/${basename(file.path)}`);if(value.hash!==createHash('sha256').update(file.content).digest('hex'))throw failure('Installed candidate bytes mismatch.');}
      completed.push(unit);checkpoint(`published:${unit}`);assertCurrent();
    }
    return {units,conflicts,completed,retained};
  } catch(error) {
    error.completed=completed;error.retained=retained;error.failed=active;error.untouched=units.filter(u=>!completed.includes(u)&&u!==active);throw error;
  } finally {for(const fd of [...handles].reverse())closeSync(fd);}
}
