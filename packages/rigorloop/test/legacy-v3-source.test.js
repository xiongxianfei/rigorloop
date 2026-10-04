import { fixture } from './helpers/v3-fixture.mjs';
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import {
  parseV3Record,
  validateV3Record,
  validateV3Set,
} from '../dist/lib/record-format-v3.js';
const read = (p) =>
  JSON.parse(
    readFileSync(
      new URL(`../../../docs/design/cli/examples/records/${p}`, import.meta.url),
      'utf8',
    ),
  );
const encode = (x) => JSON.stringify(x) + '\n';
const prefix = 'docs/changes/example-change/';
const edit = (files, path, fn) => {
  const value = JSON.parse(files[prefix + path]);
  fn(value);
  files[prefix + path] = encode(value);
};
const fail = (fn, expectedCode = 'invalid-input') =>
  assert.throws(fn, (e) => {
    assert.equal(e.recordStoreCode, expectedCode, e.message);
    return true;
  });
test('TG-01 complete v3 store and standalone design examples conform without narrative conversion', () => {
  assert.equal(validateV3Set('example-change', fixture()).size, 5);
  for (const path of [
    'v3-review-limitations-update/before.json',
    'v3-review-limitations-update/after.json',
    'v3-finding-correction/stored-review.json',
    'v3-finding-correction/updated-review.json',
  ])
    validateV3Record('review', read(path));
  for (const path of [
    'v3-verify-without-evidence/verify-report.json',
    'v3-verify-limitations-update/before.json',
  ])
    validateV3Record('verify', read(path));
});
test('TG-01 explanation collections allow repeated reasons and preserve multiline bytes', () => {
  const r = read('v3-review-limitations-update/before.json');
  r.rationale.push(r.rationale[0]);
  r.limitations = [];
  assert.deepEqual(parseV3Record('review', encode(r)), r);
  for (const field of ['summary', 'assessment_scope']) {
    const b = structuredClone(r);
    b[field] = ' \n\t';
    fail(() => validateV3Record('review', b));
  }
  for (const bad of [[], [''], [' \n'], null]) {
    const b = structuredClone(r);
    b.rationale = bad;
    fail(() => validateV3Record('review', b));
  }
});
test('TG-01 unknown_value closed fields kinds enums and dual explanation reject', () => {
  const r = read('v3-review-limitations-update/before.json');
  for (const field of ['body', 'sections', 'unknown_value'])
    fail(() => validateV3Record('review', { ...r, [field]: 'unexpected' }));
  fail(() => validateV3Record('unknown_value', r));
  fail(() => validateV3Record('review', { ...r, judgment: 'unknown_value' }));
  for (const field of ['reporter', 'owner']) {
    const b = structuredClone(r);
    b.findings[0][field].role = 'unknown_value';
    fail(() => validateV3Record('review', b));
  }
  const b = structuredClone(r);
  b.findings[0].state = 'unknown_value';
  fail(() => validateV3Record('review', b));
});
test('TG-01 optional conditional basis is closed and complete when present', () => {
  const v = read('v3-verify-limitations-update/before.json');
  validateV3Record('verify', v);
  const absent = structuredClone(v);
  delete absent.verification_basis;
  validateV3Record('verify', absent);
  for (const bad of [
    null,
    {},
    { ...v.verification_basis, unknown_value: 'x' },
    { ...v.verification_basis, head_branch: ' ' },
  ])
    fail(() => validateV3Record('verify', { ...v, verification_basis: bad }));
  fail(() => validateV3Record('verify', { ...v, changes: [] }));
  fail(() => validateV3Record('verify', { ...v, outcome: 'failed' }));
});
test('TG-02 mixed versions and broken typed references reject', () => {
  const files = fixture();
  edit(files, 'evidence.json', (r) => (r.schema_version = 2));
  fail(() => validateV3Set('example-change', files), 'unsupported-contract');
  const bad = fixture();
  edit(
    bad,
    'verify-report.json',
    (r) =>
      (r.evidence_refs = [
        { path: prefix + 'reviews/final-code-review.json', id: 'final-code-review' },
      ]),
  );
  fail(() => validateV3Set('example-change', bad), 'broken-reference');
});
