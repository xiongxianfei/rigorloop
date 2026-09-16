import { test } from 'node:test';
import assert from 'node:assert/strict';
import { runInteraction, SCENARIOS } from './helpers/record-store-interactions.mjs';

const prefix = 'docs/changes/example/';
const manifest = prefix + 'change.json';
const review = prefix + 'reviews/design-review.json';
const evidence = prefix + 'evidence.json';
const verify = prefix + 'verify-report.json';

// Assertions consume returned observations; all CLI operations live in the
// explicitly named runInteraction operation, which owns one private project.
function assertRequiredOutcome(result) {
  const { initial, semantic, basis } = result;
  assert.equal(initial[review].findings.length, 24);
  assert.equal(initial[evidence].checks.length, 12);
  const touched = new Set();

  if (result.scenario === 'finding-with-neighbors') {
    touched.add(review);
    const added = {
      id: 'new-finding',
      reporter: { id: 'reviewer', role: 'review' },
      owner: { id: 'implementer', role: 'implement' },
      subjects: basis,
      evidence: 'Observed preservation defect in the selected engineering basis.',
      required_outcome: 'Demonstrate unchanged neighboring entries.',
      state: 'open',
      resolution: null,
    };
    assert.deepEqual(semantic[review], {
      ...initial[review],
      findings: [...initial[review].findings, added],
    });
  } else if (result.scenario === 'failed-verify-correction') {
    touched.add(manifest);
    touched.add(evidence);
    assert.deepEqual(semantic[evidence].checks, [
      ...initial[evidence].checks,
      {
        id: 'final-failure',
        actor: { id: 'verifier', role: 'verify' },
        subjects: basis,
        result: 'failed',
        procedure: 'Compare neighboring records against the preservation requirement.',
        summary: 'A neighbor changed during the simulated failed check.',
      },
    ]);
    const blocker = {
      id: 'verify-defect',
      reporter: { id: 'verifier', role: 'verify' },
      owner: { id: 'implementer', role: 'implement' },
      subjects: basis,
      evidence: 'Observed preservation defect in the selected engineering basis.',
      required_outcome: 'Demonstrate unchanged neighboring entries.',
      state: 'open',
      resolution: null,
      origin: {
        reporter: { id: 'verifier', role: 'verify' },
        subjects: basis,
        evidence: 'Observed preservation defect in the selected engineering basis.',
        required_outcome: 'Demonstrate unchanged neighboring entries.',
        rationale:
          'Verify observed the defect; correction remains required despite recorded completion.',
        supporting_judgment: null,
      },
    };
    assert.deepEqual(semantic[manifest], {
      ...initial[manifest],
      blockers: [...initial[manifest].blockers, blocker],
    });
  } else if (result.scenario === 'applicability-reassessment') {
    touched.add(manifest);
    touched.add(review);
    assert.equal(result.checkpoints.length, 2);
    assert.equal(
      result.checkpoints[0][manifest].applicability.find((a) => a.path === review).value,
      'stale',
    );
    assert.equal(
      result.checkpoints[1][manifest].applicability.find((a) => a.path === review).value,
      'current',
    );
    assert.equal(semantic[review].judgment, 'approved');
    assert.deepEqual(semantic[review].findings, initial[review].findings);
    assert.deepEqual(semantic[review].subjects, initial[review].subjects);
  } else {
    assert.equal(result.scenario, 'final-explanation-read');
    assert.deepEqual(semantic, initial[verify]);
  }

  // These are actual stored bytes, compared to an observation before mutation.
  for (const [path, before] of Object.entries(result.initialBytes)) {
    if (!touched.has(path)) assert.equal(result.bytes[path], before, path);
  }
}

for (const scenario of SCENARIOS) {
  test(`TG-08 ${scenario} has equivalent complete interaction semantics`, () => {
    const advanced = runInteraction(scenario, 'advanced');
    const targeted = runInteraction(scenario, 'targeted');
    assertRequiredOutcome(advanced);
    assertRequiredOutcome(targeted);
    assert.deepEqual(targeted.semantic, advanced.semantic);
    assert.deepEqual(targeted.basis, advanced.basis);
    assert.deepEqual(targeted.checkpoints, advanced.checkpoints);
    assert.ok(targeted.calls.includes('context'));
    assert.ok(advanced.calls.includes('record-store.inspect'));
    if (scenario !== 'final-explanation-read') {
      assert.ok(targeted.calls.includes('subject.inspect'));
    }
  });
}
