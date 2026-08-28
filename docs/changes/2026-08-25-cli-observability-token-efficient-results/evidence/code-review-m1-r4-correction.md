# M1 R4 Correction Evidence

Change record: `docs/changes/2026-08-25-cli-observability-token-efficient-results/change.yaml`

Milestone: M1

Validation result: passed

## Corrections

- `CLIOBS-M1-L1-F1`: lifecycle mutations now carry an authoritative `state_changed` fact. Dry runs and already-recorded operations report `false`; persisted revision changes report `true`.
- `CLIOBS-M1-L1-F2`: concise projection emits `next_operation` only for an explicit continuation or exactly one unique corrective/permitted operation.
- `CLIOBS-M1-L1-F3`: `new-change` accepts the shared closed `--format` vocabulary while preserving legacy `--json` and default human output.
- `CLIOBS-M1-L1-F4`: table-driven result-class, mutation-state, exact-one continuation, and mandatory-field coverage was added, together with public `new-change` compatibility characterization.

## Bound identities

- `packages/rigorloop/dist/lib/result-renderer.js`: `sha256:7e131ea61620ab75ead4dc840f0947a931866b46e7bfe9b76ae3eb3b3176ef57`
- `packages/rigorloop/dist/lib/lifecycle-cli.js`: `sha256:52e2868441bac44751877471b00b794bd3c4db6ac97d5c41e0356eaab5308d09`
- `packages/rigorloop/dist/lib/new-change.js`: `sha256:91084729d6af46c65f9b8dce64b3bd0a06fed30cd61830814a98f2014a6e5e4f`
- `packages/rigorloop/test/result-renderer.test.js`: `sha256:3e58938def07f22254b2627663184cce6b88f956ccd160f712672617decb762d`
- `packages/rigorloop/test/cli-invocation-observability.test.js`: `sha256:f1fcb02bfe0cd82563f92e4e8623c3df2b8c2576642439d6c81d2c635e8c6678`

## Commands run

- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` — 14 passed, 0 failed.
- `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-invocation-observability.test.js packages/rigorloop/test/cli-observability.test.js` — 32 passed, 0 failed.
- `npm test --prefix packages/rigorloop` — 211 passed, 0 failed.

No publication, network mutation, or lifecycle transition was performed by these validation commands.
