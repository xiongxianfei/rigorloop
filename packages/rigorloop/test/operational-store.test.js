import assert from 'node:assert/strict';
import { test } from 'node:test';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, rmSync, symlinkSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { validateSnapshot } from '../dist/lib/operational-model.js';
import { loadSnapshot, saveSnapshot } from '../dist/lib/operational-rows.js';

import { cli,actor,project,createInput,invoke,databasePath } from './helpers/operational-fixture.mjs';

test('operational creation persists relational current work and a second process resumes it', t => {
  const root = project(t);
  const saved = invoke(root, ['change', 'create'], createInput());
  assert.equal(saved.exit, 0, JSON.stringify(saved));
  assert.equal(saved.result.status, 'saved');
  assert.equal(saved.result.committed, true);
  assert.match(saved.result.revision, /\S/);
  const read = invoke(root, ['change', 'context']);
  assert.equal(read.exit, 0, JSON.stringify(read));
  assert.equal(read.result.status, 'ok');
  assert.equal(read.result.committed, false);
  assert.equal(read.result.revision, saved.result.revision);
  assert.match(JSON.stringify(read.result), /Repair navigation/);
  assert.match(JSON.stringify(read.result), /No publication/);
  const db = new DatabaseSync(databasePath(root), { readOnly: true });
  t.after(() => db.close());
  assert.equal(db.prepare('SELECT change_id FROM changes').get().change_id, 'navigation');
  assert.equal(db.prepare('PRAGMA user_version').get().user_version, 1);
  assert.equal(db.prepare('PRAGMA integrity_check').get().integrity_check, 'ok');
});

test('operational closed vocabularies and duplicate fields reject before store initialization', t => {
  for (const alteration of [r => { r.input.activity.stage = 'unknown-stage'; }, r => { r.input.extra = true; }, r => { r.schema_version = 1; }, r => { r.input.activity.owner.role = 'unknown-role'; }]) {
    const root = project(t), input = createInput(); alteration(input);
    const r = invoke(root, ['change', 'create'], input);
    assert.equal(r.exit, 2, JSON.stringify(r));
    assert.equal(r.result.committed, false);
    assert.equal(existsSync(databasePath(root)), false);
  }
  const root = project(t);
  const r = invoke(root, ['change', 'create'], JSON.stringify(createInput()).replace('"schema_version":2', '"schema_version":2,"schema_version":2'));
  assert.equal(r.result.errors[0].code, 'invalid-request');
  assert.equal(existsSync(databasePath(root)), false);
});

test('operational corrupt storage is unavailable and never replaced with an empty store', t => {
  const root = project(t); mkdirSync(join(root, '.rigorloop'));
  const bytes = Buffer.from('An existing file that is not a SQLite database.'); writeFileSync(databasePath(root), bytes);
  const r = invoke(root, ['change', 'create'], createInput());
  assert.notEqual(r.exit, 0);
  assert.equal(r.result.committed, false);
  assert.deepEqual(readFileSync(databasePath(root)), bytes);
});

test('operational path admission rejects symlinked storage and SQLite sidecars', t => {
  for (const name of ['.rigorloop', '.rigorloop/rigorloop.db-wal']) {
    const root = project(t), foreign = project(t);
    const sentinel = join(foreign, 'sentinel'); writeFileSync(sentinel, 'preserve me');
    if (name.includes('/')) mkdirSync(join(root, '.rigorloop'));
    symlinkSync(name.includes('/') ? sentinel : foreign, join(root, name));
    const r = invoke(root, ['change', 'create'], createInput());
    assert.equal(r.result.errors[0].code, 'invalid-request');
    assert.equal(r.result.committed, false);
    assert.equal(readFileSync(sentinel, 'utf8'), 'preserve me');
    assert.equal(existsSync(join(foreign, 'rigorloop.db')), false);
  }
});
