import test from 'node:test';
import assert from 'node:assert/strict';
import {
  mkdtempSync,
  mkdirSync,
  writeFileSync,
  readFileSync,
  existsSync,
  rmSync,
  symlinkSync,
  openSync,
  closeSync,
  writeSync,
  readdirSync,
  readlinkSync,
  lstatSync,
} from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { installCandidate } from '../dist/lib/installer-replacement.js';
const unit = '.agents/skills/design';
function fixture(t) {
  const root = mkdtempSync(join(tmpdir(), 'distribution-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  return root;
}
function old(root) {
  mkdirSync(join(root, unit), { recursive: true });
  writeFileSync(join(root, unit, 'old.md'), 'old');
}
const files = [{ path: `${unit}/SKILL.md`, content: Buffer.from('new') }];
test('fresh install and default identical or empty directory conflicts are whole-candidate', (t) => {
  const root = fixture(t);
  installCandidate({ projectRoot: root, files });
  assert.equal(readFileSync(join(root, files[0].path), 'utf8'), 'new');
  assert.throws(
    () =>
      installCandidate({
        projectRoot: root,
        files: [...files, { path: '.agents/skills/new/SKILL.md', content: Buffer.from('x') }],
      }),
    (e) => e.code === 'destination-conflict' && e.conflicts.includes(unit),
  );
  assert.equal(existsSync(join(root, '.agents/skills/new')), false);
});
test('symlinks, unsafe paths and unsafe retention placement block force', (t) => {
  const parent = fixture(t),
    root = join(parent, 'project'),
    outside = fixture(t);
  mkdirSync(root);
  old(root);
  writeFileSync(join(parent, 'escape'), 'parent sentinel');
  writeFileSync(join(outside, 'sentinel'), 'unchanged');
  symlinkSync(outside, join(root, unit, 'link'));
  assert.throws(
    () => installCandidate({ projectRoot: root, files, force: true }),
    (e) => e.code === 'unsafe-destination',
  );
  assert.throws(
    () =>
      installCandidate({
        projectRoot: root,
        files: [{ path: '../escape', content: Buffer.from('x') }],
        force: true,
      }),
    (e) => e.code === 'unsafe-destination',
  );
  rmSync(join(root, unit, 'link'));
  assert.throws(
    () => installCandidate({ projectRoot: root, files, force: true, discoveryRoots: ['.'] }),
    (e) => e.code === 'unsafe-destination',
  );
  assert.equal(readFileSync(join(root, unit, 'old.md'), 'utf8'), 'old');
  assert.equal(readFileSync(join(parent, 'escape'), 'utf8'), 'parent sentinel');
  assert.deepEqual(readdirSync(outside), ['sentinel']);
  assert.equal(readFileSync(join(outside, 'sentinel'), 'utf8'), 'unchanged');
});
test('mid-publication failure reports completed failed and untouched units and preserves retry conflicts', (t) => {
  const root = fixture(t);
  old(root);
  writeFileSync(join(root, 'unrelated.txt'), 'preserve');
  function snapshot(path) {
    const info = lstatSync(path);
    return info.isDirectory()
      ? ['directory', info.mode, readdirSync(path).sort().map(name => [name, snapshot(join(path, name))])]
      : ['file', info.mode, readFileSync(path).toString('base64')];
  }
  const candidate = [
    { path: '.agents/skills/a/SKILL.md', content: Buffer.from('first') },
    ...files,
    { path: `${unit}/resource.md`, content: Buffer.from('resource') },
    { path: '.agents/skills/z/SKILL.md', content: Buffer.from('last') },
  ];
  let stopped;
  assert.throws(
    () =>
      installCandidate({
        projectRoot: root,
        files: candidate,
        force: true,
        checkpoint(event) {
          if (event === `file-published:${files[0].path}`) throw Error('interrupted');
        },
      }),
    (e) => {
      stopped = e;
      return e.message === 'interrupted';
    },
  );
  assert.deepEqual(stopped.completed, ['.agents/skills/a']);
  assert.equal(stopped.failed, unit);
  assert.deepEqual(stopped.untouched, ['.agents/skills/z']);
  assert.equal(readFileSync(join(root, '.agents/skills/a/SKILL.md'), 'utf8'), 'first');
  assert.equal(readFileSync(join(root, files[0].path), 'utf8'), 'new');
  assert.equal(existsSync(join(root, unit, 'resource.md')), false);
  assert.equal(existsSync(join(root, '.agents/skills/z')), false);
  assert.equal(stopped.retained.length, 1);
  assert.equal(stopped.retained[0].path, unit);
  const backup = stopped.retained[0].backup;
  assert.ok(backup.startsWith(`${root}/.rigorloop-install-retained-`));
  assert.ok(!backup.slice(root.length).includes('/skills/'));
  assert.deepEqual(readdirSync(backup), ['old.md']);
  assert.equal(readFileSync(join(backup, 'old.md'), 'utf8'), 'old');
  const retainedBeforeRetry = snapshot(backup);
  writeFileSync(join(root, files[0].path), 'independent');
  const beforeRetry = snapshot(root);
  assert.throws(
    () => installCandidate({ projectRoot: root, files: candidate }),
    (e) => {
      assert.equal(e.code, 'destination-conflict');
      assert.deepEqual(e.conflicts, ['.agents/skills/a', unit]);
      return true;
    },
  );
  assert.deepEqual(snapshot(root), beforeRetry);
  assert.equal(readFileSync(join(root, files[0].path), 'utf8'), 'independent');
  const retried = installCandidate({ projectRoot: root, files: candidate, force: true });
  assert.deepEqual(retried.completed, ['.agents/skills/a', unit, '.agents/skills/z']);
  assert.deepEqual(retried.conflicts, ['.agents/skills/a', unit]);
  assert.deepEqual(retried.retained.map(({ path }) => path), ['.agents/skills/a', unit]);
  for (const file of candidate) assert.deepEqual(readFileSync(join(root, file.path)), file.content);
  assert.deepEqual(readdirSync(join(root, unit)).sort(), ['SKILL.md', 'resource.md']);
  assert.equal(readFileSync(join(retried.retained[1].backup, 'SKILL.md'), 'utf8'), 'independent');
  assert.equal(readFileSync(join(root, 'unrelated.txt'), 'utf8'), 'preserve');
  assert.deepEqual(snapshot(backup), retainedBeforeRetry);
});
