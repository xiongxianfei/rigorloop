# Review Resolution: Retire the Standalone Test-Spec Stage

## Summary

Closeout status: closed

Review closeout: code-review-m5-r2

Review closeout: code-review-m5-r1

Review closeout: code-review-m4-r1

Review closeout: code-review-m3-r1

Review closeout: code-review-m2-r2

Review closeout: code-review-m2-r1

Review closeout: code-review-m1-r2

Review closeout: delivery-review-r3

Review closeout: design-review-r2

Review closeout: proposal-review-r3

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `proposal-review-r3`, `design-review-r1`, `design-review-r2`, `delivery-review-r1`, `delivery-review-r2`, `delivery-review-r3`, `code-review-m1-r1`, `code-review-m1-r2`, `code-review-m2-r1`, `code-review-m2-r2`, `code-review-m3-r1`, `code-review-m4-r1`, `code-review-m5-r1`, `code-review-m5-r2`
- Findings resolved: 10
- Unresolved findings: 0
- Current result: Code Review M5 R2 found the bounded corrections clean and resolved both M5 findings.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RTS-PR1 | accepted | resolved | The proposal now reflects the completed upstream vision revision and no longer requests that completed action. |
| RTS-DR1 | accepted | resolved | The architecture and ADR now select v2 plus a frozen activation manifest as the durable discriminator. |
| RTS-DLR1 | accepted | resolved | The test specification now assigns stable identities and complete mappings to all plan-dependent validation commands. |
| RTS-DLR2 | accepted | resolved | Every acceptance criterion now maps explicitly to its existing direct test owner. |
| RTS-M1-CR1 | accepted | resolved | Python now rejects explicit null as unknown and shared fixtures prove Node/Python parity. |
| RTS-M1-CR2 | accepted | resolved | Production repository validators now consume the shared classifier and tracked manifest with direct public-boundary proof. |
| RTS-M2-CR1 | accepted | resolved | The classified lifecycle contract now reaches central automation evaluation, validation, persistence, binding, coordination, and routing. |
| RTS-M2-CR2 | accepted | resolved | Delivery Review now validates the exact registered primary plan rather than a literal artifact ID. |
| RTS-M5-CR1 | accepted | resolved | Active conditional workflow resources omit standalone test-spec and direct package regressions protect the route. |
| RTS-M5-CR2 | accepted | resolved | Governed plan authoring is v2-only and manifest-bound v1 authoring fails closed for Workflow handling. |

## Finding Details

### proposal-review-r1

#### RTS-PR1

Finding ID: RTS-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Decision owner: proposal author
Decision needed: none
Chosen action: revised the vision-impact disclosure and requested decision without changing the retirement direction.
Rationale: current standing authority already expresses artifact-independent verification traceability.
Required outcome: the proposal describes current vision alignment and does not request an already-completed vision revision.
Follow-up: none; proposal-review-r2 completed the required same-stage rereview.
Validation target: `Impact and major trade-offs`, `Decision requested`, and the closing authority paragraph agree with current `VISION.md`.
Validation evidence: corrected proposal `sha256:b8dd19d8ad073dbae31ffe232e59f23ac3f8445cf9cf791c2be95f8c5781d774`; proposal-review-r3 approved the exact revision with no material findings against the final closeout records.

### proposal-review-r2

No material findings. The clean rereview confirms that `RTS-PR1` is resolved and that the proposal remains direction-ready.

### proposal-review-r3

No material findings. This clean evidence-reconciliation review binds the unchanged proposal judgment to the final review-log and resolution identities.

### design-review-r1

#### RTS-DR1

Finding ID: RTS-DR1
Disposition: accepted
Status: resolved
Owner: architecture author
Owning stage: architecture
Decision owner: architecture author
Decision needed: none
Chosen action: use `stage-owned-change-local-v2` for new changes and a frozen activation manifest binding every pre-activation ID to its exact v1 or legacy-unversioned class; keep migration optional and workflow-owned.
Rationale: the explicit contract plus immutable eligibility inventory distinguishes prior, new, historical, migrated, unknown, and contradictory states without relying on dates, artifact presence, Git history, or network state.
Required outcome: prior-contract, new active, historical, migrated, unknown, and contradictory states are classified without date inference, artifact-presence inference, or history rewriting.
Safe resolution path: revise the ADR and architecture, register both exact revisions, validate their coherence with the unchanged specification, and return to Design Review.
Follow-up: Design Review R2 of the complete revised package.
Validation target: RTS-R20 through RTS-R23; BND-STATE-001; BND-RECOVERY-001; BND-COMPAT-001; INT-001; INT-005.
Validation evidence: primary architecture `sha256:98023a64b3248bd4095a25242dd830b7f71bff280f050127a1390f623175129c`; ADR `sha256:fb9409e89524101cc54cb0af1ab9d7a22b6472a7a2cabe556ac9aaf3a91e795e`; registered authoring evidence `evidence/architecture-correction-r1.md` and `evidence/adr-correction-r1.md`; workflow return receipts `evidence/design-review-r1-architecture-return.md` and `evidence/design-review-r1-adr-return.md`; `git diff --check` passed.

### delivery-review-r1

#### RTS-DLR1

Finding ID: RTS-DLR1
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Decision owner: test-spec author
Decision needed: none
Chosen action: add stable command entries for focused skill validation and the two final closeout validators, then update every affected proof and milestone mapping.
Rationale: the plan already depends on these repository-owned commands, so the test-spec command ledger must make their ownership, timing, failure, evidence, and side-effect behavior auditable.
Required outcome: every plan-dependent validation command has a stable ID and complete ledger and milestone mapping.
Safe resolution path: revise and register only the test specification, validate boundary and lifecycle structure, return to Delivery Review, and settle the exact revised package only after a clean rereview.
Follow-up: Delivery Review R2 of the revised exact package.
Validation target: test-spec Validation commands, Proof map, Milestone proof map, and affected test-case Command IDs.
Validation evidence: corrected test specification `sha256:5f7c890e74e843980d1dd5570d32f83465155e7ef6bbf6e685a09a9a2a084f67`; `evidence/test-spec-correction-r1.md`; boundary-first validation, documentation prose audit, and `git diff --check` passed; workflow correction return is `evidence/delivery-review-r1-test-spec-return.md`.

### delivery-review-r2

#### RTS-DLR2

Finding ID: RTS-DLR2
Disposition: accepted
Status: resolved
Owner: test-spec author
Owning stage: test-spec
Decision owner: test-spec author
Decision needed: none
Chosen action: add one explicit acceptance-criterion coverage map and discrete criterion IDs to existing test cases.
Rationale: stable-ID traceability cannot rely on prose ranges, and the approved Design Review coherence criterion also needs an explicit proof owner.
Required outcome: every one of `RTS-AC1` through `RTS-AC13` has an explicit direct test mapping.
Safe resolution path: revise and register only the test specification, validate the exact proof map and documentation, return to Delivery Review, and perform a clean exact-package rereview.
Follow-up: Delivery Review R3 of the revised exact package.
Validation target: acceptance-criterion coverage map and affected test-case `Covers` fields.
Validation evidence: corrected test specification `sha256:4924c73977b907a8348ea7d1d78914d8dfb14c7365262bcc4bdfaeca52c53fd7`; `evidence/test-spec-correction-r2.md`; boundary-first validation, documentation prose audit, thirteen-ID coverage check, and `git diff --check` passed; workflow correction return is `evidence/delivery-review-r2-test-spec-return.md`; Delivery Review R3 found no material issue.

### delivery-review-r3

No material findings. The clean rereview confirms `RTS-DLR1` and `RTS-DLR2` are resolved and approves the exact corrected delivery package.

### code-review-m1-r1

#### RTS-M1-CR1

Finding ID: RTS-M1-CR1
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: M1 implementer
Decision needed: none; apply the bounded correction required by the approved contract.
Chosen action: distinguish missing lifecycle-contract metadata from explicit null and reject explicit null as an unknown value in Python.
Rationale: the Node implementation already fails closed, and the approved M1 contract requires deterministic cross-runtime classification rather than treating an explicit unknown as legacy.
Required outcome: Python and Node both reject explicit null before manifest consistency checks, while genuinely absent metadata remains legacy-unversioned.
Safe resolution path: use key-presence or a sentinel, add an explicit-null `unknown_value` parity regression, and rerun CMD-01, CMD-03, and CMD-04.
Follow-up: return corrected M1 to code-review.
Validation target: `RTS-R22`, `TS-002`, and the repository closed-vocabulary validator rule.
Validation evidence: shared explicit-null fixture passed in Node and Python; CMD-01 passed 173 tests with isolated `TMPDIR`; CMD-03 passed 75 tests; Code Review M1 R2 found the correction clean.

#### RTS-M1-CR2

Finding ID: RTS-M1-CR2
Disposition: accepted
Status: resolved
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: M1 implementer
Decision needed: none; complete the already-approved M1 integration boundary.
Chosen action: make production change-metadata and artifact-lifecycle validators load the tracked activation manifest and invoke the shared classifier for governed records.
Rationale: helper-only tests do not enforce the lifecycle compatibility contract at the repository validator boundary that M1 explicitly owns.
Required outcome: public repository validators reject invalid or contradictory v2 states and active-manifest membership/class mismatches for prior records while preserving permitted preactivation behavior.
Safe resolution path: integrate the shared Python classifier through existing validator entry points, add public-boundary regressions for v2 active test-spec state, prior membership/class mismatch, and invalid manifest content, then rerun CMD-03, CMD-04, and CMD-01.
Follow-up: return corrected M1 to code-review.
Validation target: `RTS-R18`, `RTS-R22`, `RTS-AC7`, `RTS-AC10`, `TS-001`, `TS-002`, `TS-015`, `BND-STATE-001`, and `BND-COMPAT-001`.
Validation evidence: public change-metadata and artifact-lifecycle regressions cover v2 active test-spec state, active-manifest membership, invalid manifest vocabulary, and missing-manifest recovery; CMD-03 passed 75 tests; CMD-04 passed 166 tests; Code Review M1 R2 found the correction clean.

### code-review-m1-r2

No material findings. The clean rereview confirms `RTS-M1-CR1` and `RTS-M1-CR2` are resolved and supports M1 milestone settlement against correction commits `ac9b7e2b` and `1aaf38e8`.

### code-review-m2-r1

#### RTS-M2-CR1

Finding ID: RTS-M2-CR1
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; complete the already-approved contract-keyed automation boundary.
Chosen action: propagate the classified lifecycle contract through central transition evaluation, automation validation, target binding/resolution, coordination, and post-completion routing.
Rationale: an isolated v2 route helper is insufficient when the central evaluator and public/coordinated paths continue to select v1 by default.
Required outcome: explicit v2 automation traverses `plan -> delivery-review` through the complete executable path, v1 remains unchanged, and unknown contracts fail before transition consistency.
Safe resolution path: make the central evaluator contract-aware, forward the owning change's classified contract through all callers, add complete v2 transaction and validation regressions, and rerun CMD-05 plus relevant classifier checks.
Follow-up: return corrected M2 to code-review.
Validation target: `RTS-R1`, `RTS-R2`, `RTS-R18`, `RTS-R19`, `RTS-R21`, `RTS-R22`, `TG-04`, `TG-05`, `TG-06`, `BND-STATE-001`, `BND-COMPOSE-001`, and `INT-004`.
Validation evidence: correction commit `ec20afe6`; public persisted-run, central transition, validation, state, and unknown-contract regressions passed; CMD-05 passed 77, 18, and 69 tests; Code Review M2 R2 found the correction clean.

#### RTS-M2-CR2

Finding ID: RTS-M2-CR2
Disposition: accepted
Status: resolved
Owner: M2 implementer
Owning stage: review-resolution
Decision owner: M2 implementer
Decision needed: none; align the review validator with existing exact artifact identity authority.
Chosen action: derive the one primary-plan artifact ID and path from the owning v2 change and compare the review member map exactly.
Rationale: artifact IDs are identities rather than fixed kind names, and the other package validators already preserve that distinction.
Required outcome: any valid exact primary-plan identity passes, while missing, extra, wrong-kind, wrong-role, and test-spec members fail.
Safe resolution path: replace the literal `["plan"]` comparison with an exact owning-change projection and add nonliteral-ID positive and mixed-member negative regressions; rerun CMD-06 and CMD-03.
Follow-up: return corrected M2 to code-review.
Validation target: `RTS-R13`, `RTS-R18`, `RTS-R19`, `TG-04`, `TG-06`, `BND-INPUT-001`, `BND-AUTH-001`, and `INT-002`.
Validation evidence: correction commit `ec20afe6`; CMD-06 passed 110 tests including exact nonliteral primary-plan acceptance and mismatched-package rejection; Code Review M2 R2 found the correction clean.

### code-review-m2-r2

No material findings. The clean rereview confirms `RTS-M2-CR1` and `RTS-M2-CR2` are resolved and supports M2 settlement against correction commit `ec20afe6`.

### code-review-m3-r1

No material findings. The review confirms that specification, plan, and Delivery Review own their approved verification responsibilities, v1 compatibility remains executable, and v2 remains inactive pending M4-M5.

### code-review-m4-r1

No material findings. The review confirms that governance and boundary routing are contract-keyed, activation readiness fails closed, all supported staged adapters omit standalone test-spec while retaining plan resources, and released v1 behavior remains unchanged pending M5.

### code-review-m5-r1

#### RTS-M5-CR1

Finding ID: RTS-M5-CR1
Disposition: accepted
Status: resolved
Owner: M5 implementer
Owning stage: review-resolution
Decision owner: M5 implementer
Decision needed: none; apply the bounded correction required by the approved active publication contract.
Chosen action: remove standalone test-spec from the automation target list and workflow-guide skeleton, then cover canonical, generated, and adapter-packaged resources directly.
Rationale: active packaged resources contradict the activated common workflow and can recreate the retired route.
Required outcome: remove the route from the conditional workflow resources and cover those resources directly.
Safe resolution path: update the bounded automation reference and workflow skeleton, add content regressions, and rerun CMD-07, CMD-08, CMD-09, and CMD-13.
Validation target: `RTS-R1`, `RTS-R2`, `RTS-R17`, `RTS-R23`, `TG-20`, and `TS-013`.
Follow-up: none; Code Review M5 R2 completed the required same-milestone rereview.
Validation evidence: correction commit `63a8d13f`; 378 skill tests, 8 build tests, 154 adapter-distribution tests, explicit lifecycle validation, and 12 broad-smoke checks passed; Code Review M5 R2 found the correction clean.

#### RTS-M5-CR2

Finding ID: RTS-M5-CR2
Disposition: accepted
Status: resolved
Owner: M5 implementer
Owning stage: review-resolution
Decision owner: M5 implementer
Decision needed: none; apply the bounded correction required by the approved compatibility contract.
Chosen action: make governed plan authoring explicitly v2-only, route v2 to Delivery Review, and stop manifest-bound v1 authoring for Workflow handling.
Rationale: every resumable v1 record is post-delivery and the referenced skill no longer exists.
Required outcome: make governed plan authoring v2-only and fail closed for manifest-bound v1 authoring.
Safe resolution path: update the governed plan reference, add a direct regression, and rerun CMD-07, CMD-08, and CMD-13.
Validation target: `RTS-R1`, `RTS-R2`, `RTS-R20`, `RTS-R22`, `TG-18`, and `TS-005`.
Follow-up: none; Code Review M5 R2 completed the required same-milestone rereview.
Validation evidence: correction commit `63a8d13f`; direct canonical, generated-mirror, and supported-adapter assertions passed; Code Review M5 R2 confirmed the v2-only handoff and v1 fail-closed boundary.

### code-review-m5-r2

No material findings. The clean rereview confirms that `RTS-M5-CR1` and `RTS-M5-CR2` are resolved and supports M5 settlement against correction commit `63a8d13f`.

### code-review-final-r1

No material findings. The final holistic review confirms that the M1-M5 slices compose into the approved v2 plan-centered lifecycle, exact manifest-bound v1 compatibility remains fail-closed, all earlier findings are resolved, and M6 may proceed to Explain Change without implementation correction.
