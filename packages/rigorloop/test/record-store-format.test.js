import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync, mkdtempSync, mkdirSync, writeFileSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { spawnSync } from 'node:child_process';
import {
  RECORDS_V3_SCHEMA,
  validateV3Record,
  parseV3Record,
  validateV3Set,
  validateV3Preservation,
  validateV3Creation,
  v3PathKind,
} from '../dist/lib/record-format-v3.js';

const root = 'docs/changes/example/';
const encode = (x) => JSON.stringify(x) + '\n';
const fixture = () =>
  JSON.parse(
    readFileSync(
      new URL('../../../tests/fixtures/rigorloop-records-v3/records.json', import.meta.url),
    ),
  );
const files = () => {
  const f = fixture();
  return Object.fromEntries(
    ['change', ...f.change.records.map((r) => r.kind)].map((kind) => [
      kind === 'change' ? root + 'change.json' : f.change.records.find((r) => r.kind === kind).path,
      encode(f[kind]),
    ]),
  );
};
const reject = (fn, code = 'invalid-input') => assert.throws(fn, (e) => e.recordStoreCode === code);

test('TG-01 v3 complete fixtures and packaged templates validate without mutation', () => {
  const f = fixture();
  for (const [kind, value] of Object.entries(f)) {
    const before = encode(value);
    assert.deepEqual(parseV3Record(kind, before), value);
    assert.equal(encode(value), before);
  }
  assert.equal(validateV3Set('example', files()).size, 5);
  const templates = JSON.parse(
    readFileSync(new URL('../../../templates/rigorloop-records-v3/records.json', import.meta.url)),
  );
  for (const [kind, value] of Object.entries(templates)) validateV3Record(kind, value);
  for (const path of [
    'schemas/rigorloop-records-v3.schema.json',
    'templates/rigorloop-records-v3/records.json',
  ]) {
    assert.deepEqual(
      readFileSync(new URL('../../../' + path, import.meta.url)),
      readFileSync(new URL('../dist/' + path, import.meta.url)),
    );
  }
});

test('TG-01 unknown_value closed vocabularies fail before consistency', () => {
  const f = fixture();
  const cases = [
    ['change', (x) => (x.contract = 'unknown_value'), 'unsupported-contract'],
    ['change', (x) => (x.schema_version = 99), 'unsupported-contract'],
    ['change', (x) => (x.activity.stage = 'unknown_value')],
    ['change', (x) => (x.activity.status = 'unknown_value')],
    ['change', (x) => (x.activity.owner.role = 'unknown_value')],
    ['change', (x) => (x.records[0].kind = 'unknown_value')],
    ['change', (x) => (x.applicability[0].value = 'unknown_value')],
    ['review', (x) => (x.target = 'unknown_value')],
    ['review', (x) => (x.judgment = 'unknown_value')],
    ['review', (x) => (x.findings[0].state = 'unknown_value')],
    ['evidence', (x) => (x.checks[0].result = 'unknown_value')],
    ['verify', (x) => (x.outcome = 'unknown_value')],
    ['request', (x) => (x.schema_version = 1), 'unsupported-contract'],
    ['review', (x) => (x.reviewer.role = 'unknown_value')],
  ];
  assert.doesNotThrow(() => validateV3Set('example', files()));
  for (const [kind, mutate, expectedCode = 'invalid-input'] of cases) {
    const value = structuredClone(f[kind]);
    assert.doesNotThrow(() => validateV3Record(kind, value));
    mutate(value);
    reject(() => validateV3Record(kind, value), expectedCode);
    if (kind === 'request') {
      value.reads = [{ path: value.writes[0].path, expected_identity: null }];
      reject(() => validateV3Record(kind, value), expectedCode);
      value.schema_version = 2;
      assert.throws(() => validateV3Record(kind, value), /read\/write path overlap/);
      continue;
    }
    // A real dangling reference is a competing consistency fault. Restoring
    // only the unknown value must expose it, proving the earlier rejection.
    const map = files();
    const path = kind === 'change' ? root + 'change.json'
      : f.change.records.find((record) => record.kind === kind).path;
    map[path] = encode(value);
    const verifyPath = root + 'verify-report.json';
    const verification = JSON.parse(map[verifyPath]);
    verification.evidence_refs = [{ path: root + 'evidence.json', id: 'missing-check' }];
    map[verifyPath] = encode(verification);
    const before = structuredClone(map);
    reject(() => validateV3Set('example', map), expectedCode);
    assert.deepEqual(map, before);
    map[path] = encode(f[kind]);
    if (kind === 'verify') {
      const restored = JSON.parse(map[path]);
      restored.evidence_refs = verification.evidence_refs;
      map[path] = encode(restored);
    }
    reject(() => validateV3Set('example', map), 'broken-reference');
  }
  reject(() => validateV3Record('unknown_value', {}));
  assert.ok(RECORDS_V3_SCHEMA.$defs.origin);
});

test('TG-01 plain JSON rejects front matter trailing narrative duplicate keys and invalid encoding', () => {
  const text = encode(fixture().review);
  for (const bad of [
    '---\n' + text + '---\nbody\n',
    text + 'body\n',
    text.slice(0, -1),
    '\ufeff' + text,
    text.replace('\n', '\r\n'),
    text.replace('"id":', '"id":"duplicate","id":'),
  ])
    reject(() => parseV3Record('review', bad));
  reject(() => parseV3Record('review', Buffer.from([0xff, 10])));
  for (const body of [null, '', 4]) {
    const r = fixture().review;
    r.summary = body;
    reject(() => validateV3Record('review', r));
  }
  const r = fixture().review;
  r.summary = 'Quoted "text"\nUnicode 确认 and \\ escapes';
  assert.equal(parseV3Record('review', encode(r)).summary, r.summary);
  r.extra = true;
  reject(() => validateV3Record('review', r));
});

test('TG-01 byte/depth/path limits and JSON domain reject', () => {
  const r = fixture().review;
  r.summary = 'a'.repeat(1024 * 1024);
  reject(() => parseV3Record('review', encode(r)), 'limit-exceeded');
  reject(() => parseV3Record('review', '['.repeat(33) + ']'.repeat(33) + '\n'), 'limit-exceeded');
  for (const p of [
    '../escape',
    '/absolute',
    'C:/escape',
    'a\\b',
    'a//b',
    'a/./b',
    'x'.repeat(1025),
  ])
    reject(() => v3PathKind('example', p), 'unsafe-path');
  const r2 = fixture().review;
  r2.summary = '\ud800';
  reject(() => validateV3Record('review', r2));
});

test('TG-01 namespaces reject wrong extensions dual manifests mixed versions and wrong review id', () => {
  reject(() => v3PathKind('example', root + 'evidence.yaml'), 'unsafe-path');
  const dual = files();
  dual[root + 'change.yaml'] = dual[root + 'change.json'];
  reject(() => validateV3Set('example', dual));
  const f = files();
  const r = fixture().review;
  r.schema_version = 1;
  f[root + 'reviews/design-review.json'] = encode(r);
  reject(() => validateV3Set('example', f), 'unsupported-contract');
  r.schema_version = 3;
  r.id = 'other';
  f[root + 'reviews/design-review.json'] = encode(r);
  reject(() => validateV3Set('example', f));
});

test('TG-01 disjoint referenceable ids reject even without a reference', () => {
  const c = fixture().change;
  c.work.push({
    id: c.models[0].id,
    status: 'pending',
    owner: c.activity.owner,
    requirement_refs: [],
  });
  reject(() => validateV3Record('change', c));
  const r = fixture().review;
  r.findings[0].id = r.id;
  reject(() => validateV3Record('review', r));
});

test('TG-01 every EntryRef field resolves only its permitted collection', () => {
  const reviewPath = root + 'reviews/design-review.json',
    ev = root + 'evidence.json';
  const cases = [
    ['review', (r) => r.findings[0].resolution.evidence_refs, reviewPath,
      { path: ev, id: 'check-1' }, { path: reviewPath, id: 'design-review' }],
    ['change', (r) => r.blockers[0].resolution.evidence_refs, root + 'change.json',
      { path: ev, id: 'check-1' }, { path: reviewPath, id: 'design-review' }],
    ['verify', (r) => r.evidence_refs, root + 'verify-report.json',
      { path: ev, id: 'check-1' }, { path: reviewPath, id: 'design-review' }],
    ['verify', (r) => r.review_refs, root + 'verify-report.json',
      { path: reviewPath, id: 'design-review' }, { path: reviewPath, id: 'finding-1' }],
    ['decisions', (r) => r.decisions[0].source_refs, root + 'material-decisions.json',
      { path: ev, id: 'check-1' }, { path: root + 'verify-report.json', id: 'example' }],
  ];
  for (const [kind, refs, path, valid, wrongClass] of cases) {
    const map = files();
    const accepted = fixture()[kind];
    refs(accepted).splice(0, refs(accepted).length, valid);
    map[path] = encode(accepted);
    assert.doesNotThrow(() => validateV3Set('example', map));
    for (const bad of [
      { path: valid.path, id: 'missing' },
      { path: root + 'reviews/unregistered.json', id: 'unregistered' },
      wrongClass,
    ]) {
      const candidate = structuredClone(map);
      const record = structuredClone(accepted);
      refs(record).splice(0, refs(record).length, bad);
      candidate[path] = encode(record);
      const before = structuredClone(candidate);
      reject(() => validateV3Set('example', candidate), 'broken-reference');
      assert.deepEqual(candidate, before);
    }
  }
  const f = files(),
    v = fixture().verify;
  v.review_refs = [{ path: reviewPath, id: 'finding-1' }];
  f[root + 'verify-report.json'] = encode(v);
  reject(() => validateV3Set('example', f), 'broken-reference');
  v.review_refs = [{ path: reviewPath, id: 'design-review' }];
  v.evidence_refs = [{ path: reviewPath, id: 'design-review' }];
  f[root + 'verify-report.json'] = encode(v);
  reject(() => validateV3Set('example', f), 'broken-reference');
});

test('TG-01 source references cover manifest collections review root findings checks and decisions', () => {
  const f = fixture(),
    map = files(),
    d = f.decisions;
  d.decisions[0].source_refs = [
    ...['model-1', 'work-1', 'blocker-1'].map((id) => ({ path: root + 'change.json', id })),
    ...['design-review', 'finding-1'].map((id) => ({
      path: root + 'reviews/design-review.json',
      id,
    })),
    { path: root + 'evidence.json', id: 'check-1' },
    { path: root + 'material-decisions.json', id: 'decision-1' },
  ];
  map[root + 'material-decisions.json'] = encode(d);
  assert.doesNotThrow(() => validateV3Set('example', map)); // Self-link is not recursive evaluation.
  for (const ref of [
    { path: root + 'verify-report.json', id: 'example' },
    { path: root + 'change.json', id: 'example' },
    { path: 'docs/changes/other/evidence.json', id: 'check-1' },
  ]) {
    d.decisions[0].source_refs = [ref];
    map[root + 'material-decisions.json'] = encode(d);
    reject(() => validateV3Set('example', map), 'broken-reference');
  }
  const sameId = files();
  const evidence = fixture().evidence;
  evidence.checks.push({ ...structuredClone(evidence.checks[0]), id: 'design-review' });
  sameId[root + 'evidence.json'] = encode(evidence);
  const decision = fixture().decisions;
  decision.decisions[0].source_refs = [
    { path: root + 'evidence.json', id: 'design-review' },
    { path: root + 'reviews/design-review.json', id: 'design-review' },
  ];
  sameId[root + 'material-decisions.json'] = encode(decision);
  const before = structuredClone(sameId);
  assert.doesNotThrow(() => validateV3Set('example', sameId));
  assert.deepEqual(sameId, before);
});

test('TG-01 registry applicability duplicates and final candidate references', () => {
  for (const mutate of [
    (c) => c.applicability.pop(),
    (c) => (c.records[0].kind = 'evidence'),
    (c) => c.records.push(c.records[0]),
    (c) => c.applicability.push(structuredClone(c.applicability[0])),
  ]) {
    const c = fixture().change;
    assert.doesNotThrow(() => validateV3Record('change', c));
    mutate(c);
    reject(() => validateV3Record('change', c));
  }
  const map = files();
  delete map[root + 'evidence.json'];
  reject(() => validateV3Set('example', map), 'broken-reference');
  map[root + 'evidence.json'] = encode(fixture().evidence);
  assert.doesNotThrow(() => validateV3Set('example', map));
});

test('TG-01 v3 advanced request validates candidate bytes and explicit absent creation', () => {
  const request = fixture().request;
  assert.doesNotThrow(() => validateV3Creation(request, false));
  reject(() => validateV3Creation(request, true));
  request.reads = [{ path: request.writes[0].path, expected_identity: null }];
  reject(() => validateV3Record('request', request));
});

test('TG-01 standalone v3 validation is read-only and rejects symlink/mixed manifests', () => {
  const dir = mkdtempSync(join(tmpdir(), 'records-v3-'));
  try {
    const map = files();
    for (const [path, content] of Object.entries(map)) {
      mkdirSync(dirname(join(dir, path)), { recursive: true });
      writeFileSync(join(dir, path), content);
    }
    const script = new URL('../../../scripts/validate-record-store.mjs', import.meta.url);
    const run = () =>
      spawnSync(process.execPath, [script.pathname, join(dir, root + 'change.json')], {
        encoding: 'utf8',
      });
    assert.equal(run().status, 0);
    for (const [path, content] of Object.entries(map))
      assert.equal(readFileSync(join(dir, path), 'utf8'), content);
    writeFileSync(join(dir, root + 'change.yaml'), '{}\n');
    assert.notEqual(run().status, 0);
    rmSync(join(dir, root + 'change.yaml'));
    const ev = join(dir, root + 'evidence.json');
    rmSync(ev);
    symlinkSync(join(dir, root + 'change.json'), ev);
    assert.notEqual(run().status, 0);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('TG-01 unknown_value regression reaches every stored and request vocabulary occurrence', () => {
  const cases = fixture(),
    covered = new Set();
  function walk(schema, value, path, kind) {
    if (schema.$ref)
      return walk(RECORDS_V3_SCHEMA.$defs[schema.$ref.split('/').at(-1)], value, path, kind);
    if (schema.anyOf) {
      const branch = schema.anyOf.find((x) =>
        value === null ? x.type === 'null' : x.type !== 'null',
      );
      return walk(branch, value, path, kind);
    }
    if (schema.enum || Object.hasOwn(schema, 'const')) {
      const candidate = structuredClone(cases[kind]);
      let target = candidate;
      for (const key of path.slice(0, -1)) target = target[key];
      target[path.at(-1)] = 'unknown_value';
      const expectedCode = path.length === 1 &&
        (path[0] === 'schema_version' || path[0] === 'contract')
        ? 'unsupported-contract' : 'invalid-input';
      assert.throws(() => validateV3Record(kind, candidate), (error) => {
        assert.equal(error.recordStoreCode, expectedCode, `${kind}.${path.join('.')}: ${error.message}`);
        return true;
      });
      covered.add(kind + '.' + path.join('.'));
    }
    if (schema.type === 'object')
      for (const [key, child] of Object.entries(schema.properties))
        if (Object.hasOwn(value, key)) walk(child, value[key], [...path, key], kind);
    if (schema.type === 'array')
      value.forEach((entry, index) => walk(schema.items, entry, [...path, index], kind));
  }
  for (const [kind, value] of Object.entries(cases)) {
    assert.doesNotThrow(() => validateV3Record(kind, value));
    walk(RECORDS_V3_SCHEMA.$defs[kind], value, [], kind);
  }
  assert.ok(covered.size > 35);
});

test('TG-01 nested optional references retain unsafe-path diagnostics', () => {
  const review = fixture().review;
  review.findings[0].resolution.evidence_refs[0].path = '../escape';
  reject(() => validateV3Record('review', review), 'unsafe-path');
  review.findings[0].resolution.evidence_refs[0].path = root + 'evidence.json';
  const change = fixture().change;
  change.blockers[0].origin.supporting_judgment.subjects[0].path = '../escape';
  reject(() => validateV3Record('change', change), 'unsafe-path');
});

test('TG-01 either manifest entry rejects dual manifests live and at an exact Git snapshot', () => {
  const dir = mkdtempSync(join(tmpdir(), 'records-dispatch-'));
  try {
    mkdirSync(join(dir, root), { recursive: true });
    writeFileSync(join(dir, root + 'change.yaml'), 'Uninterpreted archival bytes\n');
    writeFileSync(
      join(dir, root + 'change.json'),
      encode(
        JSON.parse(
          readFileSync(
            new URL('../../../templates/rigorloop-records-v3/records.json', import.meta.url),
          ),
        ).change,
      ),
    );
    const git = (args) => {
      const r = spawnSync('git', ['-C', dir, ...args], { encoding: 'utf8' });
      assert.equal(r.status, 0, r.stderr);
      return r.stdout.trim();
    };
    git(['init', '-q']);
    git(['add', 'docs']);
    git([
      '-c',
      'user.name=Fixture',
      '-c',
      'user.email=fixture@example.invalid',
      '-c',
      'commit.gpgsign=false',
      'commit',
      '-qm',
      'Fixture',
    ]);
    const revision = git(['rev-parse', 'HEAD']);
    for (const name of ['change.yaml', 'change.json'])
      for (const suffix of [[], ['--revision', revision]]) {
        const r = spawnSync(
          process.execPath,
          [
            new URL('../../../scripts/validate-record-store.mjs', import.meta.url).pathname,
            join(dir, root + name),
            ...suffix,
          ],
          { encoding: 'utf8' },
        );
        assert.notEqual(r.status, 0, `${name} ${suffix.join(' ')}`);
      }
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('TG-01 preservation permits repair of missing members and broken prior refs', () => {
  const after = files(),
    before = files();
  delete before[root + 'evidence.json'];
  assert.doesNotThrow(() => validateV3Preservation('example', before, after));
  before[root + 'evidence.json'] = null;
  assert.doesNotThrow(() => validateV3Preservation('example', before, after));
  const broken = files(),
    review = fixture().review;
  review.findings[0].resolution.evidence_refs[0].id = 'missing';
  broken[root + 'reviews/design-review.json'] = encode(review);
  assert.doesNotThrow(() => validateV3Preservation('example', broken, after));
  const removed = files(),
    manifest = fixture().change;
  manifest.records = manifest.records.filter((x) => x.kind !== 'verify');
  manifest.applicability = manifest.applicability.filter(
    (x) => x.path !== root + 'verify-report.json',
  );
  removed[root + 'change.json'] = encode(manifest);
  delete removed[root + 'verify-report.json'];
  before[root + 'verify-report.json'] = null;
  reject(() => validateV3Preservation('example', before, removed));
});

test('TG-01 unknown_value version and contract pairs reject unsupported-contract', () => {
  for (const [kind, value] of Object.entries(fixture())) {
    value.schema_version = 99;
    reject(() => validateV3Record(kind, value), 'unsupported-contract');
    value.schema_version = 1;
    reject(() => validateV3Record(kind, value), 'unsupported-contract');
  }
  for (const kind of ['change', 'request']) {
    const value = fixture()[kind];
    value.contract = 'explicit-recording-v1';
    reject(() => validateV3Record(kind, value), 'unsupported-contract');
  }
});
