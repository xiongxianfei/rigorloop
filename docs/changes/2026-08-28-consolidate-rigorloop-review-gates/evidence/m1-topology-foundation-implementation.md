# M1 Single-Cutover Foundation Correction Evidence

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Milestone: M1
Stage authority: implement
Subject path: docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md
Subject identity: sha256:353734d3bc315fcd24134bb452dd2d00d2fc344aed34058a84c9a6e3a2b759ee
Validation result: pass

## Scope

M1 removes the abandoned dual-topology activation design. The existing workflow remains authoritative while this change is implemented. The consolidated workflow will replace it only at one complete reviewed release cutover after runtime, canonical skills, validators, generated packages, and nonterminal legacy-work checks agree.

## Implemented result

- Removed `specs/review-topology-activation.yaml`, its schema, the runtime parser, the 146-change baseline inventory, and all activation-state interpretation.
- Removed `review_topology` from new-change metadata, lifecycle serialization, lifecycle status/context, change schema, and semantic validation.
- Restored `new-change` to deterministic metadata generation without repository activation configuration.
- Revised the approved proposal, specification, ADR, plan, and test specification to require one atomic cutover and retirement of old progression rather than runtime coexistence.
- Revised the CLI observability contract so a later approved feature may intentionally change public lifecycle facts with matching spec, fixture, and release-note updates instead of adding legacy rendering or output-version complexity.

No activation document, per-change topology value, compatibility baseline, contributor-maintained document hash, or runtime old/new workflow selector remains in scope.

## Validation

- `node --test packages/rigorloop/test/cli.test.js packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js` — 155 passed.
- `node --test packages/rigorloop/test/result-renderer.test.js` — 14 passed, including the previously failing frozen-output regression.
- `python scripts/test-change-metadata-validator.py` — 64 passed.
- `python scripts/test-artifact-lifecycle-validator.py` — 170 passed.
- `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-08-28-consolidate-rigorloop-review-gates` — passed with 16 reviews, 8 findings, 16 log entries, and 8 resolution entries.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-28-consolidate-rigorloop-review-gates/change.yaml` — passed after approved-artifact identity synchronization.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` over the proposal, spec, ADR, plan, and test spec — passed.
- `python scripts/validate-documentation-prose.py --mode audit ...` over the six revised authored documents — zero errors and warnings.
- Runtime/schema scan for `review-topology`, `review_topology`, `pre-manifest-compatibility`, `activation-baseline`, `package-gates-v2`, and `artifact-gates-v1` — no matches in the owned M1 implementation surfaces; all three activation files are absent.
- `git diff --check` — passed.

## Compatibility evidence

The public result-renderer regression now passes unchanged because M1 no longer exposes topology fields. The observability spec explicitly permits later approved lifecycle features to supersede affected output fields in one release-visible contract update; it does not require a legacy renderer or CLI version selector.

## Approval carry-forward

The owner explicitly approved direct correction of the corresponding authored documents while retaining their recorded approval status. This correction therefore updates the registered identities of the proposal, specification, ADR, plan, and test specification without reopening their lifecycle states. The review findings remain historical evidence, and M1 still requires a fresh code review over the corrected packet.

## Handoff

After final validation and identity synchronization, M1 returns to independent code review. M2 package-review authority, consolidated routing, skills, generated adapters, and release cutover remain out of scope.
