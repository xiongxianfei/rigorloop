# M1 Code Review R1

Review ID: code-review-m1-r1
Stage: code-review
Round: 1
Reviewer: two independent L2 Codex reviewers
Target: 9d16bbe2..58d60870
Reviewed artifact: commit 58d60870
Reviewed milestone: M1
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-implementation
Reviewer context ID: m1-primary-and-second-fresh-agents
Context separation mechanism: fresh-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; generated-output machinery; compatibility identity; multi-component change
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md@58d60870#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@58d60870#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@58d60870#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@58d60870#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/progressive-boundary-first-skill-guidance.md@58d60870#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@58d60870#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@58d60870#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@58d60870#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9; commit:58d60870.diff@58d60870#sha256:9b3e64293d517fed7dfeddbd8cda68cfd5fe3bc510fc828597bb366a95f57698
Prompt template version: code-review-v1
Initial packet hash: sha256:a79e8b799b63cadc827a20b2cd15fc6ffd6b909043d363c50df71bacd61a2a9b
Manifest owner: workflow-orchestrator
Affected behavior: closed manifest parsing, three-resource ownership, 14-target projection, skill resource validation, and pending activation identity
Highest-impact failure modes: wrong exact matrix accepted; circular authority; partial write; semantic omission; unsafe escape; incomplete activation identity
Changed boundaries: manifest authority; canonical-to-skill composition; compatibility-stable core; multi-target mutation; validation authority; recovery
Evidence expected: T1, T2, and T5 negative matrices; independent hashes; exact maps; interruption proof; pending activation proof
Areas requiring direct inspection: parser; exact matrix; path containment; transaction; digest; activation; skill validation; resource split; negative tests
Areas intentionally out of scope: M2, M3, M4, PR, CI, and final verification
Risk classes considered: contract fidelity; closed vocabulary; filesystem containment; mutation atomicity; retry; authority separation; compatibility; diagnostics
Falsifiable review questions: Can known-value matrix drift pass; can a later write leave partial state; can mixed versions pass; can activation hide manifest errors
Material findings: CR-M1-R1-001, CR-M1-R1-002, CR-M1-R1-003, CR-M1-R1-004
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, and review resolution
- Open blockers: four M1 findings
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-M1-R1-001, CR-M1-R1-002, CR-M1-R1-003, CR-M1-R1-004
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/code-review-m1-r1.md
- Review log: review-log.md
- Review resolution: review-resolution.md
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CR-M1-R1-001, CR-M1-R1-002, CR-M1-R1-003, CR-M1-R1-004
- Verify readiness: not-claimed

## Review inputs

- Diff: `9d16bbe2..58d60870`
- Invocation manifest: `review-invocation-code-review-m1-r1.yaml`
- Governing artifacts: feature spec, test spec, M1 plan slice, and ADR-20260729
- Validation evidence challenged: 16 projection tests, 57 activation tests, 272 skill-validator tests, 24 canonical skill validations, and boundary validation

## Diff summary

M1 adds the three-resource manifest, splits the canonical resource, projects 14 stage-owned copies, revises ten resource maps, makes projection and skill validation manifest-aware, and extends pending activation identity.

## Findings

### CR-M1-R1-001 — Exact resource authority is not closed

Finding ID: CR-M1-R1-001
Severity: blocker
Location: `scripts/boundary_first_reference.py`, `scripts/skill_validation.py`
Evidence: Known but unowned consumer additions and valid-looking alternate source or target paths pass because parser checks derive only generic membership and containment. Projection and skill validation then trust the same changed manifest. A mixed canonical resource version can also be rehashed and accepted.
Required outcome: Bind every stable resource ID to the ADR-exact source, target, consumers, and `boundary-first-v1` resource identity before projection or activation.
Safe resolution path: Add one immutable contract definition used only to validate the manifest, keep projection derived from the validated manifest, validate declared resource versions, and add coherent known-value mutation tests.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M1-R1-002 — Compact core omits the compact scan

Finding ID: CR-M1-R1-002
Severity: blocker
Location: `specs/references/boundary-first-method-v1.md`, `scripts/test-boundary-first-reference.py`
Evidence: PBS-R012 assigns the PBS-R007 four-question scan to the compact core, but the split resource contains only the eight-dimension table and shared interpretation rules.
Required outcome: Put the exact four compact-scan questions in the canonical compact core without activating stage-local automatic behavior.
Safe resolution path: Add the questions, assert their exact presence, reproject all ten compact copies, and refresh activation identities.
needs-decision rationale: none
Auto-fix class: mechanical

### CR-M1-R1-003 — Interrupted writes leave a mixed tree

Finding ID: CR-M1-R1-003
Severity: major
Location: `scripts/boundary_first_reference.py`, `scripts/test-boundary-first-reference.py`
Evidence: Fourteen direct sequential `write_bytes` operations have no rollback. Injecting an `OSError` after an early target write leaves earlier targets changed, while the existing preflight test only covers a missing source before mutation.
Required outcome: A handled failure during the projection transaction leaves the prior target set unchanged and retry remains deterministic.
Safe resolution path: Snapshot all affected target states after preflight, restore them on write failure, return a structured failure, and inject failures at early, middle, and final writes.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M1-R1-004 — Activation diagnostics erase manifest failure identity

Finding ID: CR-M1-R1-004
Severity: blocker
Location: `scripts/boundary_first_validation.py`
Evidence: Every `ProjectionContractError` becomes `BFR-PROJECTION-PATH` against the compact-core path with an unsafe-path message. An unknown manifest version is therefore attributed to the wrong artifact, check, and reason.
Required outcome: Preserve or accurately translate the source check ID, repository-relative affected path, expected value, and reason.
Safe resolution path: Make projection contract errors structured and translate them without collapsing manifest failures; add activation-level mutations for version, fields, consumers, and unsafe paths.
needs-decision rationale: none
Auto-fix class: declared-safe

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | CR-M1-R1-001 through CR-M1-R1-004 violate M1 MUST properties. |
| Test coverage | block | Exact known-value drift, compact scan, interrupted write, and diagnostic translation lack direct proof. |
| Edge cases | block | T1 and T2 negative/interruption matrices are incomplete. |
| Error handling | block | Partial writes and misclassified diagnostics. |
| Architecture boundaries | block | ADR-exact resource ownership is not enforced. |
| Compatibility | concern | Stable path and pending state remain, but mixed resource versions can be accepted. |
| Security/privacy | pass | Existing containment and redaction checks pass. |
| Derived artifact currency | concern | The live 14-target tree matches, but the accepted matrix can be redefined. |
| Unrelated changes | pass | The diff is scoped to M1. |
| Validation evidence | concern | Named commands pass but adversarial reproductions expose proof gaps. |

## Requirement-fidelity receipt

Applicability: applicable
Relevant spec clauses decomposed: yes
Property matrix complete: no
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present in exact ownership, compact-core scan, interruption, and diagnostics
No-finding rationale: not-applicable because material findings exist

| Clause | Required property | Required surfaces | Result |
| --- | --- | --- | --- |
| PBS-R002 | One version and resource identity | three canonical resources, parser, activation | fail |
| PBS-R012 | Exact layers, ownership, and compact scan | manifest, compact core, family resources | fail |
| PBS-R013-PBS-R015 | ADR-exact paths, consumers, maps, and fail-closed behavior | parser, projections, resource maps, validator | fail |
| PBS-R016 | Deeper resources can remain unloaded | resource maps | pass for M1 |
| PBS-R032-PBS-R034 | deterministic complete projection and coherent mutation | projection engine, activation | fail |
| PBS-R037 | actionable stable diagnostics | projection and activation errors | fail |
| PBS-R038 | portable repository-owned proof | scripts and resources | pass |

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > verdict-recorded
Independence level: L2
Second review: satisfied; both reviewers requested changes
Prior-finding reconciliation: not applicable; all findings are new
Confidence: high

No clean-review sufficiency receipt is issued because the review is not clean.
