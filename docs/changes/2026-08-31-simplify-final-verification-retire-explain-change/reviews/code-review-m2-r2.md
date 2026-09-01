# Code Review M2 R2: Impact-Aware Evidence Protocol

Review ID: code-review-m2-r2
Stage: code-review
Round: r2
Reviewer: Independent Codex code-review agent
Target: corrected M2 implementation commit `8b8ac337ce846007981d01b0d668fee92ef0167f`
Reviewed artifact: complete M2 diff `839c84bb..8b8ac337` and correction diff `b1e6ba7a..8b8ac337`
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-log.md`, and `review-resolution.md`
- Open blockers: `FV-M2-CR6`, `FV-M2-CR7`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M2-CR6`, `FV-M2-CR7`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: `FV-M2-CR6`, `FV-M2-CR7`
- Verify readiness: not-claimed

## Scope and authority

Reviewed the complete M2 implementation and correction through `8b8ac337ce846007981d01b0d668fee92ef0167f` against approved Design Review `design-review-r1`, Delivery Review `delivery-review-r1`, M2 TG-05 through TG-09, and FV-R8 through FV-R22, FV-R25 through FV-R28, FV-R31 through FV-R34, and FV-R38. The review inspected both runtime implementations, focused tests, staged Verify resources, report asset, implementation evidence, and the inactive activation boundary. It reran the planned command set and direct counterexamples in both runtimes.

This isolated review records evidence only. It does not repair implementation, change approved artifacts, mutate `change.yaml`, or route lifecycle state.

## R1 finding reconciliation

| Finding | R2 result | Evidence |
| --- | --- | --- |
| `FV-M2-CR1` | resolved | Proved surfaces are closed, unique, and mapped before decision precedence; unknown, duplicate, and unmapped cases fail in both runtimes. |
| `FV-M2-CR2` | resolved | Exact entry shapes and execution-kind-specific command, hosted, prior-evidence, and cache proof are required. |
| `FV-M2-CR3` | resolved | A current tail requires exactly the report and matching `lifecycle_cli.validations.verify-result` registration, with full-file parsing, report digest, subject, selector, and authority binding. |
| `FV-M2-CR4` | resolved for the reported cases | Both runtimes reject duplicate always-current IDs, whitespace explanation content, unknown proved surfaces, malformed basis values, and missing proof. A separate collection-shape parity defect remains as `FV-M2-CR6`. |
| `FV-M2-CR5` | resolved | Successful basis members require canonical repository/remote fingerprints, safe branches and IDs, immutable revisions, plan path, and SHA-256 diff identity. |

## Material findings

## Finding FV-M2-CR6

Finding ID: FV-M2-CR6
Severity: major
Location: `packages/rigorloop/dist/lib/final-verification-protocol.js:172-184,213-223`; `scripts/final_verification_protocol.py:328-347,392-412`; `scripts/test-change-metadata-validator.py:2901-2937`
Evidence: The JavaScript validator silently normalizes non-array `impact`, `evidence`, and `always_current` values to empty arrays for a non-success result, while Python rejects the same payload. A reviewer probe changed an otherwise valid result to `outcome: inconclusive`, set all three collection fields to `null`, retained a blocker, set `branch_ready: false`, and omitted the explanation. JavaScript returned `[]`; Python returned three collection-shape errors. Even for success, the ordered error lists differ because Python emits an additional always-current shape error. The committed cross-runtime matrix covers selected payloads but not the promised malformed-collection partition, so identical report bytes can be accepted by one runtime and rejected by the other. This violates FV-R26, FV-R28, FV-R34, TG-09, BND-STATE-001, and the single normalized result contract.
Required outcome: JavaScript and Python must require the same collection types for every outcome and return equivalent readiness decisions and deterministic diagnostics for malformed `impact`, `evidence`, and `always_current` values.
Safe resolution path: Reject non-array collection fields explicitly in JavaScript, align the exact Python/JavaScript error order, and extend the shared conformance matrix with null, scalar, mapping, empty-success, and valid empty-non-success partitions.
needs-decision rationale: none; this is a bounded parity correction under the approved M2 result contract.

## Finding FV-M2-CR7

Finding ID: FV-M2-CR7
Severity: major
Location: `packages/rigorloop/dist/lib/final-verification-protocol.js:183-210`; `scripts/final_verification_protocol.py:345-390`; `skills/verify/assets/verify-report-v3-skeleton.md:36-52`
Evidence: The closed evidence entry requires `authority_current`, `identity_current`, `environment_current`, `conflicting`, `new_obligation`, and `cache_hit`, but neither runtime validates that they are booleans. A reviewer probe used the strings `"yes"`/`"no"` for all six fields, classified the surface as affected, selected `rerun`, supplied a valid command proof and pass, and otherwise retained a complete successful result. Both validators returned no errors and granted `branch_ready`. This permits ambiguous evidence facts in a successful normalized result; non-boolean `cache_hit` bypasses the cache/actual-run conflict and the other facts are interpreted only through incidental strict comparisons. It violates FV-R14-FV-R17, FV-R21, FV-R26, TG-07 through TG-09, BND-INPUT-001, BND-COMPOSE-001, and BND-ENV-001.
Required outcome: Every boolean evidence fact must accept only JSON booleans before applicability or success consistency is interpreted, and malformed values must never support a successful result.
Safe resolution path: Add an explicit boolean-type pass for all six fields in both runtimes, keep shape checks before dependent decision logic, and add shared false/true and string/number/null/object/list regressions including cache-hit plus actual-run and newly-required precedence cases.
needs-decision rationale: none; the staged report shape and approved evidence semantics already define these as boolean facts.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | R1 surface, proof, tail, stated parity, and basis gaps are corrected; malformed collection and boolean evidence facts remain outside the normalized contract. |
| Test coverage | block | All planned suites pass, but direct probes expose two uncovered safety partitions. |
| Edge cases | block | Null non-success collections have opposite runtime outcomes; string-valued evidence facts can support success. |
| Error handling | concern | Closed vocabularies fail first, but scalar shape/type validation is incomplete and cross-runtime diagnostics diverge. |
| Architecture boundaries | pass | The staged S -> R -> V tail binds exact report content and registration and remains inactive. |
| Compatibility | pass | Activation remains `preactivation`; current v2 routing and `explain-change` behavior are unchanged. |
| Security/privacy | pass | Proof paths and identities are repository-relative/canonical; no new secret or machine-path exposure was found. |
| Unrelated changes | pass | The diff remains scoped to M2 protocol, tests, resources, evidence, and review records. |

## Validation performed

- `npm test --prefix packages/rigorloop` — passed.
- `python scripts/test-change-metadata-validator.py` — passed.
- `python scripts/test-artifact-lifecycle-validator.py` — passed, 167 tests.
- `python scripts/test-validation-cache.py` — passed, 25 tests.
- `python scripts/test-skill-validator.py` — passed, 382 tests.
- `node --test packages/rigorloop/test/final-verification-protocol.test.js` — passed, 7 tests.
- `python scripts/test-change-metadata-validator.py FinalVerificationProtocolTests` — passed, 16 tests.
- `git diff --check 839c84bb..8b8ac337` — passed.
- Reviewer JavaScript/Python probes — confirmed the five R1 counterexamples are rejected; exposed the non-success null-collection parity disagreement and successful malformed-boolean acceptance above.

## No automatic handoff

This isolated review makes no workflow mutation or implementation correction. R1 findings `FV-M2-CR1` through `FV-M2-CR5` are independently resolved, but M2 cannot close while `FV-M2-CR6` and `FV-M2-CR7` remain open.

## Handoff

- Reviewed milestone: M2
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: yes
- Recommended next stage: Workflow records and routes the two bounded M2 implementation corrections, then returns the complete corrected M2 diff for Code Review M2 R3.
- Final closeout readiness: not ready; M2 has two open material findings and M3-M5 remain planned.
