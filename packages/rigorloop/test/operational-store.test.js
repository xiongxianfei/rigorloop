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

test('operational reads and previews do not initialize an absent database', t => {
  const root = project(t);
  const read = invoke(root, ['change', 'context']);
  assert.notEqual(read.exit, 0);
  assert.equal(read.result.committed, false);
  assert.equal(existsSync(databasePath(root)), false);
  const preview = invoke(root, ['change', 'create'], createInput(), ['--dry-run']);
  assert.equal(preview.exit, 0, JSON.stringify(preview));
  assert.equal(preview.result.status, 'preview');
  assert.equal(preview.result.committed, false);
  assert.equal(existsSync(databasePath(root)), false);
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

test('operational project association and future schema refuse without replacing existing data', t => {
  const root = project(t);
  const created = invoke(root, ['change', 'create'], createInput());
  assert.equal(created.exit, 0, JSON.stringify(created));
  writeFileSync(join(root, '.rigorloop.json'), JSON.stringify({ schema_version: 1, project_id: randomUUID() }));
  const mismatch = invoke(root, ['change', 'context']);
  assert.equal(mismatch.result.errors[0].code, 'project-mismatch');
  const db = new DatabaseSync(databasePath(root));
  const original = db.prepare('SELECT project_id FROM project').get().project_id;
  writeFileSync(join(root, '.rigorloop.json'), JSON.stringify({ schema_version: 1, project_id: original }));
  db.exec('PRAGMA user_version=999'); db.close();
  const future = invoke(root, ['change', 'context']);
  assert.equal(future.result.errors[0].code, 'schema-unsupported');
  const check = new DatabaseSync(databasePath(root), { readOnly: true });
  assert.equal(check.prepare('PRAGMA user_version').get().user_version, 999);
  assert.equal(check.prepare('SELECT COUNT(*) AS count FROM changes').get().count, 1); check.close();
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

test('operational exact selector yields complete discovery and preserves 64-bit revision precision', t => {
  const root = project(t);
  assert.equal(invoke(root, ['change', 'create'], createInput()).exit, 0);
  const db = new DatabaseSync(databasePath(root));
  db.prepare('UPDATE changes SET revision=?').run(9007199254740993n); db.close();
  const input = { schema_version: 2, interface: 'targeted-recording-v2', contract: 'rigorloop-records-v4', selectors: [{ kind: 'change', id: 'navigation' }], include_observations: false };
  const selected = invoke(root, ['change', 'context'], input);
  assert.equal(selected.exit, 0, JSON.stringify(selected));
  assert.match(selected.result.revision, /:9007199254740993$/);
  assert.deepEqual(selected.result.available_selectors, [{ kind: 'change', id: 'navigation' }]);
  assert.equal(selected.result.items[0].value.requirement_basis, null);
  assert.equal(selected.result.items[0].value.completion, null);
});

test('operational response capacity rejects an otherwise bounded request before creation', t => {
  const root = project(t), input = createInput();
  // Request overhead is smaller than the retained record + response envelope.
  const current = Buffer.byteLength(JSON.stringify(input));
  input.input.intent.goal += 'x'.repeat(1024 * 1024 - current - 100);
  assert.ok(Buffer.byteLength(JSON.stringify(input)) < 1024 * 1024);
  const r = invoke(root, ['change', 'create'], input);
  assert.equal(r.result.errors[0].code, 'size-limit');
  assert.equal(r.result.committed, false);
  assert.equal(existsSync(databasePath(root)), false);
});

test('operational grammar and help finish without consuming an open stdin or accessing a project', async t => {
  const { spawn } = await import('node:child_process');
  for (const words of [['change', '--help'], ['change', 'create', '--help'], ['change', 'create', '--bogus'], ['change', 'context', '--dry-run']]) {
    const p = spawn(process.execPath, [cli, ...words], { stdio: ['pipe', 'pipe', 'pipe'] });
    let output = ''; p.stdout.on('data', data => { output += data; });
    const timer = setTimeout(() => p.kill('SIGKILL'), 5000);
    const code = await new Promise((resolve, reject) => { p.on('error', reject); p.on('close', resolve); });
    clearTimeout(timer);
    assert.equal(code, words.includes('--help') ? 0 : 2, output);
    if (words.includes('--help')) assert.match(output, /rigorloop-records-v4/);
  }
});

test('operational relational constraints reject foreign references and unknown persisted vocabularies', t => {
  const root = project(t);
  assert.equal(invoke(root, ['change', 'create'], createInput()).exit, 0);
  const db = new DatabaseSync(databasePath(root), { enableForeignKeyConstraints: true });
  try {
    assert.equal(db.prepare('PRAGMA foreign_keys').get().foreign_keys, 1);
    assert.equal(db.prepare('PRAGMA journal_mode').get().journal_mode, 'wal');
    assert.throws(() => db.exec("INSERT INTO accounts VALUES('foreign-change','evidence','check')"), /FOREIGN KEY/);
    assert.throws(() => db.exec("INSERT INTO accounts VALUES('navigation','unknown','check')"), /CHECK/);
    assert.throws(() => db.exec("UPDATE changes SET activity_stage='unknown'"), /CHECK/);
    db.exec('BEGIN');
    db.exec("INSERT INTO accounts VALUES('navigation','evidence','check')");
    db.exec("INSERT INTO account_refs VALUES('navigation','evidence','check','review_refs',0,'review','missing')");
    assert.throws(() => db.exec('COMMIT'), /FOREIGN KEY/);
    db.exec('ROLLBACK');
    assert.equal(db.prepare('SELECT count(*) AS n FROM accounts').get().n, 0);
  } finally { db.close(); }
});

test('operational missing typed body is unavailable, never an empty usable account', t => {
  const root = project(t);
  assert.equal(invoke(root, ['change', 'create'], createInput()).exit, 0);
  const db = new DatabaseSync(databasePath(root));
  db.exec("INSERT INTO accounts VALUES('navigation','evidence','broken')"); db.close();
  const read = invoke(root, ['change', 'context']);
  assert.equal(read.result.errors[0].code, 'store-unavailable');
  assert.equal(read.result.committed, false);
  assert.deepEqual(read.result.items, []);
});

test('operational simultaneous creators preserve both independent Changes in one project', async t => {
  const { spawn } = await import('node:child_process');
  const root = project(t);
  const run = id => new Promise((resolve, reject) => {
    const p = spawn(process.execPath, [cli, 'change', 'create', '--root', root, '--change', id, '--format', 'json', '--input', '-']);
    let output = ''; p.stdout.on('data', data => { output += data; });
    p.on('error', reject); p.on('close', code => resolve({ code, output }));
    p.stdin.end(JSON.stringify(createInput({ change_id: id })));
  });
  const results = await Promise.all([run('first'), run('second')]);
  for (const [index,result] of results.entries()) {
    const outcome = JSON.parse(result.output);
    assert.ok([0,4,5].includes(result.code), result.output);
    if (result.code !== 0) {
      assert.equal(outcome.committed,false);
      const check = new DatabaseSync(databasePath(root), { readOnly:true });
      const id = ['first','second'][index];
      assert.equal(check.prepare('SELECT count(*) AS n FROM changes WHERE change_id=?').get(id).n,0); check.close();
      // Caller explicitly reconciles known absence before another creation.
      const retry = await run(id); assert.equal(retry.code,0,retry.output);
    }
  }
  const db = new DatabaseSync(databasePath(root), { readOnly: true });
  try {
    assert.deepEqual(db.prepare('SELECT change_id FROM changes ORDER BY change_id').all().map(r=>r.change_id), ['first', 'second']);
    assert.equal(db.prepare('SELECT store_revision FROM project').get().store_revision, 2);
  } finally { db.close(); }
});

test('operational bounded writer contention reports busy and preserves the previous Change', t => {
  const root = project(t);
  const before = invoke(root, ['change', 'create'], createInput());
  assert.equal(before.exit, 0);
  const db = new DatabaseSync(databasePath(root));
  db.exec('BEGIN IMMEDIATE');
  let busy;
  try { busy = invoke(root, ['change', 'create'], createInput()); }
  finally { db.exec('ROLLBACK'); db.close(); }
  assert.equal(busy.result.status, 'busy', JSON.stringify(busy));
  assert.equal(busy.result.committed, false);
  assert.equal(invoke(root, ['change', 'context']).result.revision, before.result.revision);
});

function preparedReview(id, scope = 'Whole implementation') {
  return {
    schema_version:4, contract:'rigorloop-records-v4',change_id:'navigation',id,
    purpose:'code',scope:'advisory',
    prepared:{subjects:[],basis_refs:[],plan:null,scope,coverage_rationale:'Early advice',prepared_by:actor},
    assessment:null,findings:[],
    applicability:{value:'needs-reassessment',actor,rationale:'No assessment supplied',observation:{method:'unknown',actor,scope:'Review input',summary:'Not assessed'}},
  };
}
test('operational oversized aggregate exposes a complete index including unselected advisory reviews', t => {
  const root=project(t);assert.equal(invoke(root,['change','create'],createInput()).exit,0);
  const db=new DatabaseSync(databasePath(root));
  try {
    const snapshot=loadSnapshot(db,'navigation');
    snapshot.accounts.review=[preparedReview('early-one','x'.repeat(550000)),preparedReview('early-two','y'.repeat(550000))];
    validateSnapshot(snapshot);
    db.exec('BEGIN IMMEDIATE');saveSnapshot(db,snapshot,2n);db.exec('COMMIT');
  } finally { db.close(); }
  const aggregate=invoke(root,['change','context']);
  assert.equal(aggregate.result.errors[0].code,'size-limit');
  const body={schema_version:2,interface:'targeted-recording-v2',contract:'rigorloop-records-v4',selectors:[{kind:'change',id:'navigation'}],include_observations:false};
  assert.ok(aggregate.result.errors[0].message.includes(JSON.stringify(body)));
  const discovery=invoke(root,['change','context'],body);
  assert.deepEqual(discovery.result.available_selectors,[{kind:'change',id:'navigation'},{kind:'review',id:'early-one'},{kind:'review',id:'early-two'}]);
  const selected=invoke(root,['change','context'],{...body,selectors:[{kind:'review',id:'early-two'}]});
  assert.equal(selected.exit,0,JSON.stringify(selected));
  assert.equal(selected.result.items[0].value.prepared.scope.length,550000);
});

test('operational capacity reserves future disposition for retained findings, including disposed findings', t => {
  const root=project(t);assert.equal(invoke(root,['change','create'],createInput()).exit,0);
  const db=new DatabaseSync(databasePath(root));
  const snapshot=loadSnapshot(db,'navigation');db.close();
  const review=preparedReview('advice');snapshot.accounts.review=[review];
  const issue=i=>({id:'issue-'+i,reporter:actor,owner:actor,scope:'Navigation',description:'Concern',required_outcome:'Resolve concern',state:'open',disposition:null});
  review.findings=Array.from({length:60},(_,i)=>issue(i));
  assert.doesNotThrow(()=>validateSnapshot(snapshot));
  for(const finding of review.findings) {
    finding.state='resolved';finding.disposition={actor,reason:'Resolved',follow_up:null};
  }
  assert.doesNotThrow(()=>validateSnapshot(snapshot));
  review.findings.push(...[60,61,62,63].map(issue));
  assert.throws(()=>validateSnapshot(snapshot),e=>e.operationalCode==='size-limit');
  review.findings=review.findings.slice(0,60);
  review.findings[0].disposition.reason='x'.repeat(16384);
  assert.throws(()=>validateSnapshot(snapshot),e=>e.operationalCode==='size-limit');
});


test('context rejects every explicitly supplied non-object query', t => {
  const root=project(t);assert.equal(invoke(root,['change','create'],createInput()).exit,0);
  for (const value of [null,false,0,'',[],{}]) {
    const child=spawnSync(process.execPath,[cli,'change','context','--root',root,'--change','navigation','--input','-','--format','json'],{encoding:'utf8',input:JSON.stringify(value)});
    assert.equal(child.status,2,child.stdout);assert.equal(JSON.parse(child.stdout).errors[0].code,'invalid-request');
  }
  assert.equal(invoke(root,['change','context']).exit,0);
});
