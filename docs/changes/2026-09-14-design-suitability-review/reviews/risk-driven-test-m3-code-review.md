# Risk-driven test redesign M3 Code Review

## Initial result

- Skill: code-review.
- Review status: approved after correction.
- Material finding: RT-M3-CR-01 resolved; no open findings.
- Recording status: recorded, advisory-durable/manual.
- Scope: eight-file M3 diff against `/tmp/risk-driven-m3-before`; unrelated dirty changes excluded.
- Nonauthor reviewer: `/root/validation_design_review`; author: `/root`.
- Full required execution remains pending and is not claimed passed.

## RT-M3-CR-01

- Severity: major.
- Location: `tests/engineering/release/release_coordination_tests.py:112`, `FixtureHostedServices.__init__`.
- Evidence: despite extracting approval_fixture, this real candidate/coordination fixture still constructs `ReleaseCoordinationTests()` and invokes its `setUp()` to obtain baseline facts. Source search finds this remaining TestCase-as-fixture dependency inside the exact M3 scope. The newly extracted helper is only reached indirectly through the TestCase lifecycle.
- Governing requirement: approved M3 explicitly replaces construction of another TestCase plus setUp calls; its expected outcome says policy fixtures no longer depend on TestCase lifecycle.
- Required outcome: construct independently owned hosted-service facts from an ordinary fixture builder, preserving the branch protection augmentation and event-specific updates. No test lifecycle call remains in this fixture.
- Safe resolution: use the existing approval fixture plus explicit setup facts, or a narrowly shared plain coordination fixture if both actual readers need it. Preserve all baseline values and rerun affected coordination/actual candidate evidence after correction. No new production policy or extra runtime abstraction is needed.
- Correction owner: implementation.

This finding was recorded before correction. Reviewer has not edited engineering files. Default-version and remaining proof inspection continue; no final M3 judgment is claimed here.

## Correction and source assessment

RT-M3-CR-01 is corrected on inspected source: FixtureHostedServices now obtains fresh approval facts directly, adds the original protected-main branch facts and retains event/run updates and its empty initial approvals. A source search finds no remaining explicit setUp calls in the Release suites. Fresh affected coordination and candidate integration proof passed 11 tests in 112.903 seconds. This supports resolution of the finding; complete M3 judgment still awaits remaining required execution.

The plain helper preserves the former literal candidate, binding and provider facts, creating new nested values on every call. It is setup, not the assertion oracle; existing policy, denied-write, identity/retry and real persistence tests retain their actual production boundaries. No approval or external-service policy changed.

The lazy version change removes Packaging's import-time metadata read and invokes the same calculation at the two actual default consumers: build-parser construction and missing-manifest support fallback. Existing explicit version parsing, help text and metadata exceptions remain. The parser still resolves its default before parsing options, as before. Current source consumers are reconciled; Validation's separately owned constant is unrelated and remains intact. A focused copied-lib test exercises actual policy import and approval evaluation with missing/malformed package metadata, without fabricating it; it failed for both inputs before correction and passes afterward. Independent Package tests retain missing/malformed default failure and explicit/default/help observations. This is bounded dependency cleanup allowed by M3, not new default or public behavior policy.

The exact new fixture helper path routes to the existing release aggregate check. Its independently named selector regression failed before admission and passed afterward. No catch-all routing or new check ID is introduced. Reviewer independently compared ordinary discovery: Release 179→180, Packaging 93→95 and Selector 182→183, with no removed baseline ID.

## Exact corrected subjects

The eight source/test paths are the M3 implementation slice; Design and plan are approved dependencies. CLI subject inspection records corrected source identities here.

| Subject | SHA-256 identity |
| --- | --- |
| `tests/engineering/release/release_execution_tests.py` | `sha256:dfb7b6829f9cec8676aedcc37e61871afc2bfccb0cd2b8ce89be916efcc6fb4b` |
| `tests/engineering/release/release_coordination_tests.py` | `sha256:7ab982ac924eded08a9d414bcacf95b4c0c287a13048ae634b6d58776a354cd3` |
| `tests/engineering/release/release_fixture_helpers.py` | `sha256:59c7b4eb22a6a2cc92c357f8e4bcc37cbd7c08309aab491e12e279e7d3e9ad18` |
| `scripts/lib/packaging/adapter_distribution.py` | `sha256:6f9d86e382d22d46453d0b7afa7128b043b1622f9be88cc8e82a4b1b43b19b0d` |
| `scripts/build-adapters.py` | `sha256:016bba889f4aecad94db38cf89db1bfcc2e22690d9b5ba6ba2b0257a5d8e1d20` |
| `tests/engineering/packaging/test-adapter-distribution.py` | `sha256:0d7c97ffe7d8e0728b935e3e18fdfb49dff391660886290442a76681d99b79fb` |
| `scripts/lib/validation/validation_selection.py` | `sha256:8d89ea493dd64a7c740b06216e419df98f8cc70bd83bd6d013f8db42a883fa20` |
| `tests/engineering/validation/test-select-validation.py` | `sha256:0dd913aa2b149671813f27a0d20c19e640e1327841de7bc5cc5eb3d4677bf7ca` |
| `docs/plans/2026-09-15-risk-driven-test-redesign.md` | `sha256:687849e708b45cdf80e42ca3f12d7dbf168a64fd47a695bdffdb8dddc7a938e5` |
| `docs/design/engineering/validation.md` | `sha256:200d5859395b87e7999e152f44c7d77a1da7d21d85ba028349f4fdd5eb70ed14` |

## Final M3 judgment

Approved. RT-M3-CR-01 is resolved by the direct plain-fixture construction, unchanged hosted fact values and fresh real coordination/candidate proof. All ten recorded source/authority identities still match the final current files. No additional material concern remains.

Completed execution: full Release 180 passed in 157.302 seconds; full Packaging 95 passed in 315.031 seconds; npm package 8 passed in 26.796 seconds; selected execution exited 0 with all 429 result rows passed and boundary scope passed; fresh corrected coordination/candidate groups passed all 11 cases in 112.903 seconds. Reviewer inspected the completed logs and found no failed or unstarted selected row. The selected scope covers existing Adapter, Release, Selector and Executor check families; focused approval/default/helper tests also passed.

Earlier full executions began before the hosted-fixture correction. Their results remain applicable only to unchanged surfaces; fresh eleven-case coordination/candidate execution establishes corrected hosted composition. Full Packaging/npm proof covers the altered production default consumers. This combined basis is sufficient under Assessment RC-SR-15; it neither rewrites earlier subjects nor claims the original entire invocation used final fixture bytes.

| Checklist criterion | Judgment and evidence |
| --- | --- |
| Spec alignment | Pass: plain independent fixtures and bounded import/default compatibility implement approved M3. |
| Test coverage | Pass: all baseline IDs retained, actual missing/malformed import regression plus default/parser and helper-route proof. |
| Edge cases | Pass: absent/malformed metadata, explicit/default versions, real candidate composition, retained retry/conflict/Git cases. |
| Error handling | Pass: owning default operation still reports actual metadata failure; policy-only import no longer fails on unrelated metadata. |
| Architecture boundaries | Pass: test data helper remains test-owned; production helper reads metadata only at actual operation consumers. |
| Compatibility | Pass: current callers reconciled, parser/help/default behavior retained, no release policy or immutable-identity change. |
| Security/privacy | Pass for scope: provider effects remain faked outside real policy, temporary copied source isolated, no publication or permissions expanded. |
| Derived artifact currency | Pass: full Packaging/npm and real candidate observations apply to changed production dependencies. |
| Unrelated changes | Pass: eight-file baseline-relative slice only; earlier dirty work excluded. |
| Validation evidence | Pass: complete relevant execution plus fresh corrected composition and exact subject recheck. |

The author records actual commands, red/green observations, correction scope and counts in `../contract-refinement.md`. Temporary logs include `/tmp/risk-driven-m3-release.log`, `/tmp/risk-driven-m3-packaging.log`, `/tmp/risk-driven-m3-npm.log`, `/tmp/risk-driven-m3-ci.log` and `/tmp/risk-driven-m3-coordination-corrected.log`. Evidence prose and diff checks were reported passed. Timings are observations, not a speed claim.

This independent advisory-durable M3 approval supports M4 under the existing implementation authorization. It grants no approval of later work, the entire dirty branch, final Verify, hosted CI or external publication. Fresh final whole-change Code Review and distinct Verify remain required after implementation and corrections.
