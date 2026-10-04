import { readFileSync, readSync, openSync, closeSync, readdirSync, mkdirSync, renameSync, copyFileSync, fsyncSync, lstatSync, fstatSync, constants } from 'node:fs';
import { resolve, dirname, join, relative, isAbsolute } from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { CONTRACT, fail, exact, canonical, parseInput, LIMIT, validateType } from './operational-contract.js';
import { stat, regular, directory, durableWrite, syncDirectory, contained } from './operational-files.js';
import { loadSnapshot } from './operational-rows.js';
import { validateSnapshot } from './operational-model.js';

export const digest = value => 'sha256:' + createHash('sha256').update(value).digest('hex');
export function fileIdentity(path) {
  const before = regular(path), fd = openSync(path, constants.O_RDONLY | constants.O_NOFOLLOW), hash = createHash('sha256');
  try { if (['dev','ino','size','mtimeMs','ctimeMs'].some(k=>before[k]!==fstatSync(fd)[k])) fail('source-conflict','File changed before integrity capture.'); const chunk = Buffer.alloc(65536); let count; while ((count = readSync(fd, chunk, 0, chunk.length, null))) hash.update(chunk.subarray(0, count)); }
  finally { closeSync(fd); }
  const after = regular(path);
  if (['dev','ino','size','mtimeMs','ctimeMs'].some(k => before[k] !== after[k])) fail('source-conflict', 'File changed during integrity capture.');
  return { bytes: after.size, digest: 'sha256:' + hash.digest('hex') };
}
export function inventory(root) {
  if (!stat(root)) return null;
  const walk = (path, prefix) => {
    const value = stat(path);
    if (value?.isFile()) return [{ path: prefix, ...fileIdentity(path) }];
    directory(path);
    const entries = [{ path: prefix, directory: true }];
    for (const name of readdirSync(path).sort()) entries.push(...walk(join(path, name), prefix ? prefix + '/' + name : name));
    if (Buffer.byteLength(canonical(entries)) > LIMIT / 2) fail('size-limit', 'Maintenance file observation exceeds the bounded manifest.');
    return entries;
  };
  return walk(root, '');
}
export function sameInventory(path, expected) { return canonical(inventory(path)) === canonical(expected); }
export function absolutePath(value, info, absent = false, allowProjectRoot = false) {
  if (typeof value !== 'string' || !value || /[\x00-\x1f\\]/.test(value)) fail('invalid-request', 'Invalid maintenance path.');
  const path = resolve(info.root, value), runtime = join(info.root, '.rigorloop');
  if (path === runtime || path.startsWith(runtime + '/') || runtime.startsWith(path + '/') && !(allowProjectRoot && path===info.root)) fail('invalid-request', 'Maintenance output/source must be outside the live runtime tree and its ancestors.');
  let cursor = dirname(path);
  for (;;) { directory(cursor); if (cursor === dirname(cursor)) break; cursor = dirname(cursor); }
  if (stat(path)?.isSymbolicLink()) fail('invalid-request', 'Maintenance paths cannot be symbolic links.');
  if (absent && stat(path)) fail('destination-conflict', 'Maintenance destination already exists.');
  return path;
}
export function copyDurable(source, target) {
  const before=regular(source), sourceFd=openSync(source,constants.O_RDONLY|constants.O_NOFOLLOW);
  try {
    if (['dev','ino','size','mtimeMs','ctimeMs'].some(k=>before[k]!==fstatSync(sourceFd)[k])) fail('source-conflict','Source changed before copy.');
    copyFileSync('/proc/self/fd/'+sourceFd,target,constants.COPYFILE_EXCL);
    const after=regular(source);
    if (['dev','ino','size','mtimeMs','ctimeMs'].some(k=>before[k]!==after[k]||before[k]!==fstatSync(sourceFd)[k])) fail('source-conflict','Source changed during copy.');
    const fd=openSync(target,constants.O_RDONLY|constants.O_NOFOLLOW);try{fsyncSync(fd);}finally{closeSync(fd);}
  } finally { closeSync(sourceFd); }
  syncDirectory(dirname(target));
}
export function atomicJSON(path, value) {
  const temporary = path + '.' + randomUUID(); durableWrite(temporary, JSON.stringify(value) + '\n'); renameSync(temporary, path); syncDirectory(dirname(path));
}
export async function validateDatabase(path, projectId, payloadRoot) {
  const { DatabaseSync } = await import('node:sqlite');
  regular(path);
  const db = new DatabaseSync(path, { readOnly: true, readBigInts: true, allowExtension: false, defensive: true });
  try {
    if (db.prepare('PRAGMA user_version').get().user_version !== 1n) fail('schema-unsupported', 'Backup database schema is unsupported.');
    const project = db.prepare('SELECT * FROM project WHERE singleton=1').get();
    if (project?.project_id !== projectId) fail('project-mismatch', 'Backup and project identities differ.');
    if (db.prepare('PRAGMA integrity_check').all().some(row => Object.values(row)[0] !== 'ok') || db.prepare('PRAGMA foreign_key_check').all().length) fail('store-unavailable', 'Database integrity or relationship check failed.');
    const changes = db.prepare('SELECT change_id FROM changes ORDER BY change_id').all().map(row => row.change_id);
    const attachments = [], external = [];
    for (const id of changes) {
      const snapshot = loadSnapshot(db, id); validateSnapshot(snapshot);
      for (const attachment of snapshot.change.attachments) {
        const path = contained(payloadRoot, id + '/' + attachment.name); regular(path);
        if (stat(path).size !== attachment.byte_count) fail('store-unavailable', 'Retained attachment size differs from its recorded metadata.');
        attachments.push({ path: id + '/' + attachment.name, ...fileIdentity(path) });
      }
      for (const row of db.prepare('SELECT DISTINCT path FROM subjects WHERE change_id=? ORDER BY path').all(id)) external.push({ change_id: id, path: row.path });
    }
    return { project, changes, attachments, external };
  } finally { db.close(); }
}
export async function validateBundle(path, info, expected = null) {
  directory(path); regular(join(path, 'manifest.json')); regular(join(path, 'complete.json'));
  const bytes = readFileSync(join(path, 'manifest.json')), identity = digest(bytes);
  if (expected !== null && expected !== identity) fail('source-conflict', 'Backup manifest differs from the selected observation.');
  const manifest = parseInput(bytes), complete = parseInput(readFileSync(join(path, 'complete.json')));
  exact(complete, ['manifest_digest']); if (complete.manifest_digest !== identity) fail('source-conflict', 'Backup completion marker does not match its manifest.');
  exact(manifest, ['format','backup_id','project_id','source_incarnation','source_revision','database_schema','record_contract','included_changes','excluded_changes','external_references','files']);
  if (manifest.format !== 1 || manifest.database_schema !== 1 || manifest.record_contract !== CONTRACT) fail('schema-unsupported', 'Unsupported backup format or schema.');
  if (manifest.project_id !== info.id) fail('project-mismatch', 'Backup belongs to another project.');
  validateType('id', manifest.backup_id);
  if (typeof manifest.source_incarnation !== 'string' || !/^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/.test(manifest.source_incarnation) ||
      typeof manifest.source_revision !== 'string' || !/^(0|[1-9][0-9]{0,18})$/.test(manifest.source_revision) || BigInt(manifest.source_revision)>9223372036854775807n) fail('invalid-request','Invalid backup store identity.');
  if (!Array.isArray(manifest.files) || !Array.isArray(manifest.included_changes) || !Array.isArray(manifest.excluded_changes)) fail('invalid-request', 'Invalid backup collections.');
  for(const ids of [manifest.included_changes,manifest.excluded_changes]) {
    ids.forEach(id=>validateType('id',id));
    if(new Set(ids).size!==ids.length || canonical([...ids].sort())!==canonical(ids)) fail('invalid-request','Backup Change lists must be unique and sorted.');
  }
  if(manifest.included_changes.some(id=>manifest.excluded_changes.includes(id)))fail('invalid-request','Included and excluded Changes overlap.');
  if(!Array.isArray(manifest.external_references))fail('invalid-request','Invalid external reference list.');
  for(const reference of manifest.external_references){exact(reference,['change_id','path']);validateType('id',reference.change_id);validateType('path',reference.path);}
  const seen = new Set();
  for (const member of manifest.files) {
    exact(member, ['path','bytes','digest']);
    if (seen.has(member.path) || !Number.isSafeInteger(member.bytes) || member.bytes < 0) fail('invalid-request', 'Duplicate or invalid backup member.');
    seen.add(member.path); if (typeof member.digest !== 'string' || !/^sha256:[a-f0-9]{64}$(?![\s\S])/.test(member.digest)) fail('invalid-request', 'Invalid integrity digest.');
    if (member.path !== 'database.sqlite' && !/^attachments\/[A-Za-z0-9][A-Za-z0-9._-]*\/[A-Za-z0-9][A-Za-z0-9._-]*$/.test(member.path)) fail('invalid-request', 'Unexpected backup member path.');
    if (canonical(fileIdentity(contained(path, member.path))) !== canonical({ bytes: member.bytes, digest: member.digest })) fail('source-conflict', 'Backup member integrity differs.');
  }
  if (!seen.has('database.sqlite')) fail('invalid-request', 'Backup database member is missing.');
  const contents = inventory(path);
  if (contents.some(entry => !entry.directory && !['manifest.json','complete.json'].includes(entry.path) && !seen.has(entry.path))) fail('invalid-request', 'Backup contains an undeclared file.');
  const checked = await validateDatabase(join(path, 'database.sqlite'), info.id, join(path, 'attachments'));
  if(checked.project.store_incarnation!==manifest.source_incarnation || checked.project.store_revision.toString()!==manifest.source_revision || canonical(checked.external)!==canonical(manifest.external_references))fail('source-conflict','Backup metadata disagrees with its captured database.');
  if (canonical(checked.changes) !== canonical(manifest.included_changes) || checked.attachments.some(a => !seen.has('attachments/' + a.path)) || seen.size !== checked.attachments.length + 1) fail('invalid-request', 'Backup manifest does not match retained database scope.');
  for (const attachment of checked.attachments) {
    const member = manifest.files.find(row => row.path === 'attachments/' + attachment.path);
    if (attachment.bytes !== member.bytes || attachment.digest !== member.digest) fail('source-conflict', 'Backup attachment changed during semantic validation.');
  }
  return { manifest, identity, checked };
}
