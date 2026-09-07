# Explicit Recording M1 — Isolated Implementation Evidence

## Authority and scope

The user explicitly approved an M1-only implementation exception using the independently reviewed model designs and delivery plan, before formal registration. This permits schema/fixture/validation foundations and independent Code Review, not public writers, lifecycle activation, historical migration or M2. This is IP0 isolated work; no governed milestone or formal review identity is fabricated.

Basis: [delivery plan M1](../plans/2026-09-05-explicit-recording-and-model-centered-design.md), [Workflow model](../design/workflow.md), [CLI model](../design/cli.md), and [advisory Delivery rereview](../reviews/explicit-recording-and-model-centered-design-delivery.md). All preexisting changes on `feature/explicit-recording-model-design` are preserved.

## Completeness and proof allocation

TG-01 covers all five Workflow record types, transient request and result, closed vocabularies, required/unknown fields, duplicate identities/keys/paths, representation limits, exact encoding and candidate references. TG-02 covers rejection of historical/unknown discriminators, absent-root creation and no public writer. Current subject freshness, commands and persistence remain M2; M1 does not claim those behaviors.

The new validator must not import semantic eligibility from existing engines. Metadata dispatch and old schemas stay unchanged because ordinary adoption is withheld; cross-contract rejection is exercised at the new validation boundary and through existing public-command rejection. Tests and evidence must distinguish representation validation from workflow approval.

## Execution evidence

Tests were written before implementation. The first focused run failed with `ERR_MODULE_NOT_FOUND` for the not-yet-created validation module, establishing the initial red result.

The isolated implementation adds the canonical `schemas/explicit-recording-v1.schema.json`, its packaged counterpart under `packages/rigorloop/dist/schemas/`, the representation-only `record-store-contract.js` module, `record-store-contract.test.js`, the seven-kind fixture under `tests/fixtures/explicit-recording-v1/`, and `scripts/build-record-store-schema.mjs` for reproducible bundling and read-only parity checks. No existing dispatcher, historical schema or governed lifecycle state was changed by M1.

Commands actually run on this slice:

| Command | Result |
| --- | --- |
| `node --test packages/rigorloop/test/record-store-contract.test.js` | After corrections: 17 passed, zero failed |
| `npm --prefix packages/rigorloop test` | After corrections: 491 tests: 489 passed, 2 skipped, zero failed |
| `python scripts/test-change-metadata-validator.py` | 112 passed |
| `node scripts/build-record-store-schema.mjs --check` | Exit 0; canonical/package bytes match |
| `git diff --check` | Exit 0 |

The broader regressions include the preserved working-tree changes; their success is not a review or ownership claim for those unrelated changes. The two skipped package tests remain skipped; no claim is made that they ran. M2, adoption, formal lifecycle closeout, branch readiness and PR readiness are not claimed.

## Independent review corrections

The [independent advisory M1 Code Review](../reviews/explicit-recording-m1-code-review.md) recorded three findings before correction: overlapping decision-basis/write paths (ER-M1-001), distinct diagnostics incorrectly sharing path identity (ER-M1-002), and incomplete inspected-snapshot representation validation (ER-M1-003).

Focused regressions were added first and reproduced all three defects: 14 passed and 3 failed. The bounded corrections enforce disjoint read/write paths, use complete diagnostic identity instead of path-only identity, and validate inspected manifest/content encoding, per-file limits, exact registry membership, change/review identities, byte revision, explicit missing-sidecar observations and absent-root shape. They neither access live decision-basis files nor enforce lifecycle eligibility. After correction all 17 focused tests passed, followed by the broader commands above. An additional otherwise-valid fixture test directly demonstrates duplicate, escaped-duplicate and nested-duplicate key rejection.

The review record owns the independent rereview judgment and finding disposition. No next milestone is authorized by this implementation evidence.
