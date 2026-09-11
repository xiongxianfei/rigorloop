import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFileSync} from 'node:fs';
import {validateMutationRequest} from '../dist/lib/recording-construction.js';
import {validatePrimaryResult} from '../dist/lib/recording-contract.js';
import {canonicalJSON} from '../dist/lib/recording-observations.js';
import {digest} from '../dist/lib/record-store-files.js';

const example = path => JSON.parse(readFileSync(
  new URL('../../../docs/design/cli/examples/' + path, import.meta.url), 'utf8'));

// Read the published examples themselves: a valid duplicate fixture would not
// detect drift in the documents selected by model/example validation.
test('model CLI work-set examples conform to the published transport', () => {
  const request = example('v2-work-status-update/request.json');
  const response = example('v2-work-status-update/response.json');
  assert.doesNotThrow(() => validateMutationRequest(request));
  assert.doesNotThrow(() => validatePrimaryResult(response));
  assert.equal(response.operation, request.operation.op);
  assert.equal(response.change_id, request.change_id);
  assert.deepEqual(response.changed, [{kind: 'work', target: request.operation.target}]);
  assert.equal(response.claim, 'storage-only');
});

test('model CLI request/receipt examples reject malformed and unknown_value variants', () => {
  for (const corrupt of [
    x => { delete x.operation.target; },
    x => { x.operation.values.status = 'unknown_value'; },
    x => { x.contract = 'unknown_value'; },
  ]) {
    const request = example('v2-work-status-update/request.json');
    corrupt(request);
    assert.throws(() => validateMutationRequest(request));
  }
  for (const corrupt of [
    x => { delete x.revision; },
    x => { x.status = 'unknown_value'; },
    x => { x.claim = 'engineering-approved'; },
  ]) {
    const response = example('v2-work-status-update/response.json');
    corrupt(response);
    assert.throws(() => validatePrimaryResult(response));
  }
});

test('model CLI observation examples bind continuation to current observed identities', () => {
  const first = example('observation-freshness/scan-b.json');
  const current = example('observation-freshness/scan-c.json');
  const expected = example('observation-freshness/expected.json');
  assert.equal(first.schema_version, 2);
  assert.equal(current.schema_version, 2);
  assert.equal(first.revision === current.revision, expected.same_record_revision);
  assert.deepEqual(first.observations, current.observations);
  assert.equal(expected.same_diagnostics, true);
  assert.equal(digest(canonicalJSON(first)), expected.first_observation_identity);
  assert.equal(digest(canonicalJSON(current)), expected.current_observation_identity);
  assert.notEqual(expected.first_observation_identity, expected.current_observation_identity);
  assert.notEqual(first.observed_subjects[0].identity, expected.historical_subject_identity);
  assert.notEqual(current.observed_subjects[0].identity, expected.historical_subject_identity);
  assert.equal(expected.continuation_status, 'conflict');
  // A copied digest or edited preimage must not retain the claimed expectation.
  const changed = structuredClone(first);
  changed.observed_subjects[0].identity = current.observed_subjects[0].identity;
  assert.notEqual(digest(canonicalJSON(changed)), expected.first_observation_identity);
});
