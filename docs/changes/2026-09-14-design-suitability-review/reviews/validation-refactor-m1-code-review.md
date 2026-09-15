# Validation organization M1 independent Code Review

## Result

- Skill: code-review.
- Status: completed.
- Artifacts changed: this review only.
- Open blockers: none within M1.
- Next stage: implement M2 under existing user authorization.
- Review status: approved.
- Material findings and Finding IDs: none.
- Recording status: recorded, advisory-durable/manual; recording blocker: none.
- Review record: `reviews/validation-refactor-m1-code-review.md` in this change directory.
- Assessment scope: advisory milestone assessment, not formal lifecycle settlement.
- Reviewed milestone: M1 of `docs/plans/2026-09-14-validation-test-organization.md`.
- Milestone closeout: closed for this scoped review; no lifecycle work record changed.
- Remaining implementation milestones: M2.
- Required review-resolution: no.
- Verify readiness: not-claimed. Independent final whole-change Code Review and distinct Verify remain after M2 and corrections.

## Basis and independence

Author `/root` implemented the slice. Separately delegated reviewer `/root/validation_design_review` did not author or edit the implementation and wrote only review evidence. Prior Design and Delivery advisory judgments are `validation-refactor-design-review` and `validation-refactor-delivery-review`, round 1, at their recorded exact package identities. This is a fresh assessment of actual implementation, not inference from those judgments.

The review compared each moved file against the pre-migration working-tree source in `/tmp/validation-migration-baseline/sources.tar`, using `/tmp/validation-m1-move-map.json`. This preserves preceding uncommitted contributions as baseline rather than attributing the whole Git HEAD diff to M1. The baseline is an ephemeral recovery/reference artifact; the scope, changes, findings and durable evidence here remain understandable without it. The ten suites preserve their existing logic and assertions except path/root/import references and one added selection regression. Existing operational validators and executor are unchanged by this slice.

## Exact reviewed subjects

The following identities came from CLI subject inspection and were rechecked unchanged after final evidence arrived. Old suite paths are the corresponding basenames under `scripts/`; old fixture paths are the corresponding relative files under `scripts/fixtures/boundary-first/`. Their absence is part of the migration scope, not deletion of protected cases.

| Current subject | Identity |
| --- | --- |
| `tests/engineering/validation/test-boundary-first-reference.py` | `sha256:913b0485fb2981129a29fb4cef6e61ecf9a92688b39f90353cb6582b70f4aeb8` |
| `tests/engineering/validation/test-boundary-first-validation.py` | `sha256:a82454ae9c101be1e80ad7e896ac5c5381532ea8dd72a6fa19ce33c987773183` |
| `tests/engineering/validation/test-change-metadata-validator.py` | `sha256:da72bcb80d9cf94a16b119957e6162f8bedacd27bbea70be10429b424f9a4193` |
| `tests/engineering/validation/test-documentation-prose-validator.py` | `sha256:dc10776c0eb29063aa26af888cfeed1b58fe397a573045a7a19e45fc717a3a3a` |
| `tests/engineering/validation/test-governed-lifecycle-cli-validator.py` | `sha256:fe065d545c066d2ebdc8c6facbe773d547adaea93dc79f14292eb81814d0790b` |
| `tests/engineering/validation/test-guide-system-validator.py` | `sha256:504cbe9317427874b32c61edff61ec901be155e619ae4362e95ebe07ff341997` |
| `tests/engineering/validation/test-markdown-readability-validator.py` | `sha256:6235d8e9143bae6ffd5d17d83c817618e960ecdd2472efe80a115614668a9a6d` |
| `tests/engineering/validation/test-query-change-record.py` | `sha256:bf1b60484d5191a9524c5033179127310d7e77544a7d877ceb4fbf4c32df1616` |
| `tests/engineering/validation/test-select-validation.py` | `sha256:9529b684c345f85d147602c7e313c0f684ca76650c92c72aacc4f411ea61e594` |
| `tests/engineering/validation/test-validation-execution.py` | `sha256:c1eb565327164a70e57d8bfee8a5ce10b83e9397f9fb1256a92d09ce67199a29` |
| `tests/engineering/validation/fixtures/boundary-first/feature-records/complex.md` | `sha256:952548a58c0f8cc23c959539e698d309a98fe630c10b37a40c44973f56b251cd` |
| `tests/engineering/validation/fixtures/boundary-first/feature-records/minimal.md` | `sha256:4cb7a204e0280bf57c83e4e13f5bc38c7cd5b7bab1409a9f6403115947934cb1` |
| `tests/engineering/validation/fixtures/boundary-first/feature-records/semantic-omission.md` | `sha256:299b88acc292cd9f47174654b8e31f641ac87eb8ec660690cc8134ca825720e5` |
| `tests/engineering/validation/fixtures/boundary-first/proof-maps/complete.md` | `sha256:6192fc7f1e4b7e70754c91c457d89ba14d4d957c4f8b270898fb1eee752353a6` |
| `tests/engineering/validation/fixtures/boundary-first/proof-maps/complex-complete.md` | `sha256:5a5c80fbc972c5cbd14e44483fbef5ff2a8099e0fbcdaa79c45dd4995dae36eb` |
| `tests/engineering/validation/fixtures/boundary-first/proof-maps/gap.md` | `sha256:6907f8fb1ece7847fd2d39bca3f22b9ff32037bb8f8bd708e6c2f83031d9fc6a` |
| `scripts/validation_selection.py` | `sha256:56da326ebcc69c858b6bcb011791da073d127ec4d71fcf6af63d37ba35219ea8` |
| `.github/workflows/ci.yml` | `sha256:12a38c1809fa0deca17805ca783020c7783934e6c1f91bbb1e7c9fb6c2e4fb2a` |
| `docs/design/cli/cli.md` | `sha256:6c955345e06f9f95ef63f3e3829fa858d2f5408ef4b073d2e4eab5ea4b55425f` |

## Checklist and rationale

| Criterion | Result and evidence |
| --- | --- |
| Spec alignment | Pass: TEST-SR-17 and M1 source destinations are realized; no case deletion, production validator move or new executor is introduced. |
| Test coverage | Pass: ordinary loader mapping preserves all367 baseline M1 cases and adds one routing regression, for368. Real negative boundary/proof fixtures and selector unknown-path rejection remain. |
| Edge cases | Pass: old deleted paths and new paths use the same owned classifications; actual local selection includes additions/deletions without unclassified or blocking paths. Existing concurrency/retry/recovery tests remain. |
| Error handling | Pass: stale command bases initially rejected; explicit assessed hashes now bind the new command paths without bypassing validation. Unknown paths remain unclassified rather than becoming empty successes. |
| Architecture boundaries | Pass: ten suites and exclusive boundary fixtures move to Validation; production imports explicitly resolve scripts. Shared documentation-prose and record fixtures retain their consumers. |
| Compatibility | Pass: catalog IDs, arguments, scoped check composition, workflow invocation, metadata-suite caller and rerun strings are preserved with current paths. The current CLI documentation link resolves to the moved suite. |
| Security/privacy | Pass for this slice: no new permissions, external action, secret handling or mutable shared fixture behavior. Recovery preserves the existing dirty baseline; no branch reset or external publication is part of the diff. |
| Derived artifact currency | Pass for applicability: this slice changes no canonical published skill, generated adapter or package implementation. Full integrated/package observations remain M2/final obligations. |
| Unrelated changes | Pass: baseline-relative diff separates prior work. Reviewed live-reader search found no unintended operational old paths outside intentional selector deletion routes. |
| Validation evidence | Pass: post-correction selected results, direct observations, normal discovery and focused correction results support the affected boundaries as detailed below. No hosted result is inferred. |

The routing regression compares both locations and asserts unknown new test paths remain unclassified. It complements existing exact check-set assertions; it is not the sole oracle for required selection. Root changes use the actual nested source depth, while production-script lookup is explicit. Six relocated boundary fixture files independently byte-match their baseline copies. No snapshot or expected failure outcome was changed to obtain success.

## Actual evidence and limitations

Reviewer inspected the implementation-relative diff, actual-reader search, nineteen subject identities, fixture byte parity, discovery mapping and the author's logs. Execution below is attributed to the implementation actor; the reviewer did not rerun the expensive suites.

- New routing regression: failed before the move; passed after command/path reconciliation.
- Normal discovery:367 baseline cases preserved plus one new case across ten suites; discovery is not reported as execution.
- Eight direct suite runs passed. The initial selector run exposed stale joined metadata paths; the five affected methods passed after correction. The corrected selected execution also completed the selector population.
- Initial executor direct run passed51/52 with one existing five-second nested child timeout under concurrent direct/selected load. The case passed unchanged in a focused rerun and in the complete corrected selected executor execution. No timeout or assertion weakening occurred; timing sensitivity remains visible as an observation rather than a concealed failure.
- `bash scripts/ci.sh --mode explicit --path scripts/validation_selection.py --path tests/engineering/validation/test-guide-system-validator.py --path tests/engineering/validation/test-boundary-first-validation.py --path .github/workflows/ci.yml`: author records exit0 and306 passed check/case rows across six families. Reviewer inspected the final selected result log and its successful completion.
- Emitted-style selector `-k` rerun: one passed case. Relocated boundary suite:61 passed tests, including invalid fixtures. Actual local selection: status `ok`, no unclassified or blocking paths.

Detailed logs and commands are indexed in the durable M1 section of `contract-refinement.md`; `/tmp/validation-m1-ci.log`, `/tmp/validation-m1-metadata-callers-green.log`, `/tmp/validation-m1-report-ownership-rerun.log`, `/tmp/validation-m1-negative-fixtures.log` and `/tmp/validation-m1-rerun.log` were inspected as supporting observations. No claim depends on interpreting the earlier failed runs as passes.

## Handoff

No required correction remains in the assessed M1 slice. M2 may proceed under the existing scoped authorization and reviewed plan. This does not approve unrelated accumulated work or complete the refactor. M2 and final integration must reconcile the remaining suites/callers and execute their allocated full proof; final whole-change independent Code Review and separate Verify remain required. Changed reviewed subjects or contradictory evidence require applicability assessment and appropriate reassessment.
