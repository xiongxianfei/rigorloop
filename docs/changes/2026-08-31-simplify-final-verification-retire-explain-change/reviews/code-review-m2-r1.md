# Code Review M2 R1: Impact-Aware Evidence Protocol

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review agent
Target: M2 implementation commit `b1e6ba7a`
Reviewed artifact: commit `b1e6ba7a` against M2 baseline `839c84bb`
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m2-r1.md`, `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`, and `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Open blockers: `FV-M2-CR1`, `FV-M2-CR2`, `FV-M2-CR3`, `FV-M2-CR4`, `FV-M2-CR5`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M2-CR1`, `FV-M2-CR2`, `FV-M2-CR3`, `FV-M2-CR4`, `FV-M2-CR5`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: `FV-M2-CR1`, `FV-M2-CR2`, `FV-M2-CR3`, `FV-M2-CR4`, `FV-M2-CR5`
- Verify readiness: not-claimed

## Scope and authority

Reviewed the exact `839c84bb..b1e6ba7a` M2 implementation against approved Design Review `design-review-r1`, approved Delivery Review `delivery-review-r1`, FV-R8 through FV-R22, FV-R25 through FV-R28, FV-R31 through FV-R34, FV-R38, M2 TG-05 through TG-09, and the mapped input, state, authority, composition, temporal, recovery, environment, and interaction boundaries. The review read the complete change record and M2 implementation evidence, inspected both protocol implementations and all new tests and Verify resources, reran every M2 command, and used adversarial Node/Python probes for readiness-sensitive counterexamples.

This formal review is isolated. It records evidence and findings only; it does not repair implementation, edit approved artifacts, mutate `change.yaml`, or perform workflow routing.

## Actual-diff summary

- Added an inactive JavaScript and Python v3 result protocol with impact, freshness, evidence-decision, result, execution, CI, authority, and always-current vocabularies.
- Added conservative applicability evaluation, report rendering/read-back, replay classification, and a Verify-tail path classifier.
- Added staged Verify resources and a report skeleton guarded by final-verification preactivation.
- Added focused runtime, validator, cache-separation, and published-skill tests plus M2 implementation evidence.
- Kept the tracked final-verification manifest preactivation and left public v2 lifecycle routing and the current explain-change prerequisite unchanged.

## Material findings

## Finding FV-M2-CR1

Finding ID: FV-M2-CR1
Severity: major
Location: `packages/rigorloop/dist/lib/final-verification-protocol.js:49-59,74-82,115-130`; `scripts/final_verification_protocol.py:127-150,170-179,228-265`
Evidence: `proved_surfaces` is checked only as a non-empty string list. Its values are never checked against the closed impact-surface vocabulary and need not reference a classified impact entry. Freshness precedence returns `rerun` before inspecting surfaces, so a successful fresh-required obligation with `proved_surfaces: ["magic-surface"]`, an actual-run label, and a passing result validates with no errors in both JavaScript and Python. This lets an evidence obligation escape the closed surface map instead of being traceable to the final impact partition. It violates FV-R10, FV-R11, FV-R14, FV-R18, FV-R22, FV-R38, M2 TG-06/TG-07, BND-INPUT-001, and the M2 completion criterion that every obligation has a traceable surface.
Required outcome: Every proved surface must use the closed impact vocabulary, be unique within its obligation, and resolve to an applicable classified impact entry before freshness or decision consistency is interpreted; unknown values must fail first.
Safe resolution path: Validate `proved_surfaces` in the unknown-first pass in JavaScript and Python, reject duplicates and missing impact-map membership, preserve freshness precedence only after structural closure, and add matching unknown, duplicate, missing-map, fresh-required, and multi-surface regressions.
needs-decision rationale: none; this is a bounded conformance correction under the approved M2 contract.

## Finding FV-M2-CR2

Finding ID: FV-M2-CR2
Severity: major
Location: `packages/rigorloop/dist/lib/final-verification-protocol.js:115-148`; `scripts/final_verification_protocol.py:228-309`; `skills/verify/assets/verify-report-v3-skeleton.md:6-21`
Evidence: A successful evidence item or always-current check can claim `execution: actual-run` and `observed_result: pass` without recording any command, hosted-observation identity, or other execution evidence. The committed successful fixtures do exactly that, and both validators accept them. The result model therefore cannot distinguish a configured or asserted execution label from an exact command that actually ran, even though FV-R22, FV-R26, the architecture, ADR, and the v3 applicability resource require exact commands and observed results. This weakens cache separation because the model rejects a `cache-hit` label but does not positively bind the asserted actual run to proof.
Required outcome: Every actual-run, hosted observation, reused pass, and always-current result must carry the exact proof identity appropriate to its execution kind, including exact commands and observed results for command-backed checks, so a successful report cannot be constructed from bare execution labels.
Safe resolution path: Define closed evidence and always-current entry shapes with execution-kind-specific required fields; require exact command identity/output evidence for actual runs, hosted evidence identity for hosted observations, and durable prior-evidence identity for reuse; update the report skeleton/resources and add missing-proof, configured-only, cache-only, hosted, reused, and successful round-trip tests in both implementations.
needs-decision rationale: none; the approved Design and M2 plan already require command/result truthfulness.

## Finding FV-M2-CR3

Finding ID: FV-M2-CR3
Severity: major
Location: `packages/rigorloop/dist/lib/final-verification-protocol.js:163-179`; `scripts/final_verification_protocol.py:320-350`; `packages/rigorloop/test/final-verification-protocol.test.js:84-95`; `scripts/test-change-metadata-validator.py:2784-2802`
Evidence: `tailDisposition`/`tail_disposition` checks only that every supplied path belongs to an allowed set. Empty input, report-only input, and lifecycle-registration-only input all return `current` in both implementations, so missing one half of the required report-plus-registration tail is indistinguishable from a complete tail. The named report-write and registration-failure tests merely construct an inconclusive object by assertion; they do not prove that a missing write or registration is detected. The allowed pseudo-field `change.yaml#validation_events.verify` also names no field in the current change schema or lifecycle record, while the current registration owner is `lifecycle_cli.validations`. Report parsing additionally stops at the first closing fence and ignores trailing bytes, so read-back does not establish an exact whole-file result. This violates FV-R31-FV-R34, TG-09, BND-AUTH-001, BND-COMPOSE-001, BND-TEMPORAL-001, EC8, and the architecture rule that lifecycle registration binds report content identity and the exact permitted write set.
Required outcome: Tail validation must require one complete report and one matching schema-valid lifecycle registration bound to the exact report content and permitted writes; empty, singleton, duplicate, unknown-field, mismatched-content, trailing-content, report-write-failed, and registration-failed states must grant no current authority.
Safe resolution path: Model the exact report and lifecycle-registration identities rather than only an allow-list predicate; align the field selector with the actual lifecycle schema; make report read-back consume the exact complete artifact; and add direct JavaScript/Python tests for every partial, mismatch, duplicate, trailing, replay, and drift partition before M3 integrates routing.
needs-decision rationale: none; the exact tail closure and failure outcome are already approved and allocated to M2.

## Finding FV-M2-CR4

Finding ID: FV-M2-CR4
Severity: major
Location: `packages/rigorloop/dist/lib/final-verification-protocol.js:133-147`; `scripts/final_verification_protocol.py:267-309`; corresponding protocol tests
Evidence: The JavaScript and Python validators disagree on readiness-critical inputs. JavaScript accepts a successful result containing all eight always-current checks plus a duplicate; Python rejects the duplicate. Python accepts a successful explanation field containing only whitespace or a non-empty list containing empty strings; JavaScript rejects it. Reviewer probes produced these opposite results from otherwise identical payloads. The evidence claims JavaScript/Python agreement, but the suites contain no shared conformance fixture for these partitions. One implementation can therefore grant `branch_ready` where the other refuses it, violating FV-R19, FV-R27, FV-R38, TG-09, BND-STATE-001, and the architecture's single normalized result contract.
Required outcome: JavaScript and Python must accept and reject the same payloads; the always-current set must contain each required check exactly once, and every successful explanation field must be substantively non-empty under one identical scalar/list rule.
Safe resolution path: Share or mirror an explicit result conformance fixture across both implementations, add duplicate always-current and whitespace/empty-list-element cases, align non-empty and collection validation, and compare full ordered error outcomes for all closed and consistency partitions.
needs-decision rationale: none; parity and truthful successful explanation are explicit M2 review criteria.

## Finding FV-M2-CR5

Finding ID: FV-M2-CR5
Severity: major
Location: `packages/rigorloop/dist/lib/final-verification-protocol.js:93-102`; `scripts/final_verification_protocol.py:192-209`; successful-result fixtures
Evidence: Successful basis validation requires only a non-empty string or number. Both implementations accept `base_revision: "not-a-revision"`, `merge_base_revision: "also-not-a-revision"`, `verified_subject_revision: "x"`, and `final_diff_sha256: "not-a-digest"` while granting `branch_ready`. The test named `target_basis_requires_exact_singleton_identities` checks only that a list is rejected, not that immutable revisions, digests, governed IDs, review identities, and plan paths have canonical identity forms. This does not close the exact S/R/Design/Delivery/diff boundary required by FV-R8, FV-R26, FV-R31, FV-R33, TG-05, BND-AUTH-001, and INT-003.
Required outcome: Each basis field must use its approved canonical identity form and reject prose, numbers, unresolved names, malformed revisions/digests, unsafe governed IDs, and invalid plan/review identities before a successful result can grant readiness.
Safe resolution path: Reuse repository identity, safe-ID, Git revision, digest, and repository-relative path validators where applicable; document fields whose canonical form is intentionally opaque; add matching JavaScript/Python invalid-format, ambiguous, stale, and exact-success fixtures.
needs-decision rationale: none; this enforces the approved exact-identity contract without choosing a new identity model.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Applicability, exact command proof, complete registered tail, exact identity, and truthful successful explanation remain under-enforced. |
| Test coverage | block | Planned suites pass, but direct counterexamples for unknown proved surfaces, partial tails, invalid identities, and cross-language parity are absent. |
| Edge cases | block | Empty/singleton tails, duplicate always-current checks, whitespace explanations, and unclassified proved surfaces can change readiness outcomes. |
| Error handling | concern | Unknown declared impact values fail first, but unknown evidence-surface references bypass that phase and partial registration failure is not derived by the protocol. |
| Architecture boundaries | block | The S -> R -> V content-registration boundary is not closed, and asserted executions are not linked to durable proof. |
| Compatibility | pass | The v3 protocol remains inactive; the full Node suite retains v1/v2 lifecycle tests and current v2 routing/explain-change behavior. |
| Security/privacy | concern | Evidence and command fields are not yet modeled, so the architecture's bounded repository-relative and sensitive-data recording rules cannot be validated; the Verify skill retains general credential-boundary guidance. |
| Derived artifact currency | pass | Canonical Verify source, staged resources, report skeleton, JavaScript runtime module, Python module, and focused tests are present; public v3 activation remains later scope. |
| Unrelated changes | pass | The implementation diff is bounded to M2 protocol, resources, tests, evidence, and lifecycle handoff receipts. |
| Validation evidence | concern | All five planned commands pass, but reviewer counterexamples demonstrate that their current fixtures do not establish the named safety claims. |

## Validation performed

- `npm test --prefix packages/rigorloop` — 321 passed, 2 skipped, 0 failed.
- `python scripts/test-change-metadata-validator.py` — 99 passed.
- `python scripts/test-artifact-lifecycle-validator.py` — 167 passed.
- `python scripts/test-validation-cache.py` — 25 passed.
- `python scripts/test-skill-validator.py` — 382 passed.
- `git diff --check 839c84bb..b1e6ba7a` — passed.
- Reviewer Node/Python probes — both accepted unknown proved surfaces, bare actual-run claims, malformed successful basis identities, and empty/singleton tails; JavaScript accepted a duplicate always-current entry that Python rejected, while Python accepted whitespace explanation content that JavaScript rejected.

## No automatic handoff

This isolated review makes no lifecycle mutation and performs no automatic correction or downstream handoff. The detailed record exists before fixing. No product, architecture, or scope decision is required: all five findings have bounded safe correction paths under the approved M2 contract.

## Handoff

- Reviewed milestone: M2
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4, M5
- Required review-resolution: yes
- Recommended next stage: Workflow records the five open findings, routes M2 to bounded implementation correction, and returns the complete corrected M2 diff for Code Review M2 R2.
- Final closeout readiness: not ready; M2 has five open material findings and M3-M5 remain planned.
