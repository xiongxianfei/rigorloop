# Code Review: M1 R4

Review ID: code-review-m1-r4
Stage: code-review
Round: 4
Reviewer: two independent L2 Codex reviewers
Target: e418519c..3a19bb73
Reviewed artifact: corrected M1 implementation range
Reviewed milestone: M1
Review date: 2026-08-05
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-review-resolution-r3
Reviewer context ID: m1-r4-primary-and-second-reviewers
Context separation mechanism: existing-separate-agents-blind-first
Automated review: yes
Risk tier: elevated
Risk-tier triggers: validator behavior; remote authority read; release boundary; lifecycle gate
Risk-tier classifier: affected-path-and-contract-surface-v1
Governing artifacts: spec; test spec; M1 plan; activation-publication ADR
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/boundary-first-v1-v0-3-7-activation-release.md@3a19bb73#sha256:fa622a617f8af6f36a9b877338b97d4a4df25a493f385764c66feaad751b7918; specs/boundary-first-v1-v0-3-7-activation-release.test.md@3a19bb73#sha256:9d0d7c839c9c44d4c138fe22961b861a06c6520dc4d3dd9a1a648f0de8114186; docs/plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md@3a19bb73#sha256:eaea12dafb3ee49d6ab284603566c8a9f190a92fbdcd4fe665ef70388ef07bde; docs/adr/ADR-20260805-boundary-first-activation-candidate-and-atomic-publication.md@3a19bb73#sha256:614c19fb59aae74205845024fa23993fed38e0b5dce2c65991a24909858b542a; range:e418519c..3a19bb73.diff@3a19bb73#sha256:cc3bb03e0b2a649bcce96808ad2bc182ae76ee396d8e0ba2d88f31f4536f6c29
Initial packet hash: sha256:bed633f209f14b320caf5bbba7cf72b2e515472b35fe4ad025fcdc3582ea616c
Prompt template version: code-review-v1
Manifest owner: workflow-orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Affected behavior: candidate evidence identity; invocation authority; privacy serialization; sibling composition
Highest-impact failure modes: wrong-phase readiness; valid receipt rejection; short secret disclosure
Changed boundaries: BND-AUTH-001; BND-STATE-001; BND-COMPOSE-001; BND-TEMPORAL-001; BND-RECOVERY-001; BND-ENV-001
Evidence expected: exact tagged R-to-C readiness; canonical receipt matrix; short privacy probes; every selected sibling failure
Areas requiring direct inspection: candidate evidence helper; invocation validation; privacy bounds; selected execution
Areas intentionally out of scope: publication mutation; release payload; real transition; public release; final verify
Risk classes considered: identity authority; lifecycle; temporal recovery; composition; privacy; compatibility
Falsifiable review questions: can tagged readiness pass; can accepted receipts pass; can short secrets or failed siblings escape
Material findings: BFA-M1-R4-001, BFA-M1-R4-002, BFA-M1-R4-003
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

Both blind-first reviewers reproduced BFA-M1-R4-001 independently. The second
reviewer additionally challenged accepted repository manifests and short
environment secrets, reproducing BFA-M1-R4-002 and BFA-M1-R4-003. M1 remains
open for correction and R5 review.

## Findings

### BFA-M1-R4-001 — Readiness reruns the forbidden pre-tag candidate gate

Finding ID: BFA-M1-R4-001
Severity: blocker
Location: `scripts/boundary_first_validation.py` candidate-evidence readiness
Evidence: `_candidate_evidence_issues()` calls `validate_activation_candidate()`.
After valid `R -> C` evidence is followed by the required local `v0.4.0 -> T`
tag, readiness returns `BFR-CANDIDATE-EVIDENCE-UNSETTLED` because candidate
mode requires that tag to be absent.
Required outcome: validate stored `R -> C` provenance and fresh live-H
authority through a phase-correct readiness path that accepts the required
local tag and never reruns candidate mode.
Safe resolution path: separate phase-neutral identity derivation from
candidate-only tag checks and add a positive tagged-readiness regression.

### BFA-M1-R4-002 — Closed invocation validation rejects accepted manifests

Finding ID: BFA-M1-R4-002
Severity: major
Location: `scripts/boundary_first_validation.py` review-invocation validation
Evidence: the new 40-character minimum for base/head revisions rejects five
accepted activation review manifests that use canonical abbreviated revisions.
The positive test covers only a synthetic full-SHA spec-review receipt.
Required outcome: align the closed schema with accepted repository receipt
shapes while continuing to reject unknown identities, fields, and payloads.
Safe resolution path: admit canonical abbreviated revisions and test every
admitted review family using representative repository manifests.

### BFA-M1-R4-003 — Short PIN/auth values can escape path redaction

Finding ID: BFA-M1-R4-003
Severity: major
Location: `scripts/boundary_first_validation.py` private runtime value discovery
Evidence: `PIN=1234` is not collected by the sensitive-name regex, so a path
containing `1234` is emitted without redaction. The existing short-value test
uses a variable name that already contains `PRIVATE`.
Required outcome: recognize the governed short OTP/auth/API-key name families
and prove their values never reach diagnostics.
Safe resolution path: expand the sensitive-name vocabulary and add short PIN,
API-key, and auth-code CLI regressions.

## Prior-finding reconciliation

| Finding | R4 status | Basis |
| --- | --- | --- |
| BFA-M1-R3-001 | resolved | Approved spec, architecture, plan, test spec, and implementation now distinguish R, C, and H. |
| BFA-M1-CR1-003 | failed-remediation | Exact R/C checks exist, but readiness uses the wrong phase and cannot pass after tag creation. |
| BFA-M1-CR1-005 | resolved | All eight sibling owners, including `rigorloop_cli.test`, propagate injected failure. |
| BFA-M1-CR1-007 | failed-remediation | Unknown fields are rejected, but accepted abbreviated receipt identities are also rejected. |
| BFA-M1-CR1-008 | failed-remediation | Named private variables are bounded, but short PIN/auth-name variants remain exposed. |

## Validation evidence

- `python scripts/test-boundary-first-validation.py` — 85 passed.
- `python scripts/validate-boundary-first.py --check` — passed.
- `python -m py_compile scripts/validate-boundary-first.py scripts/boundary_first_validation.py` — passed.
- Exact CMD4 selection — passed with three owned checks and no debt.
- `python scripts/test-select-validation.py` — 146 passed.
- `git diff --check` — passed.

The named suites did not cover the three adversarial reproductions above.
