# M1 Code Review R3

Review ID: code-review-m1-r3
Stage: code-review
Round: 3
Reviewer: two independent L2 Codex reviewers
Target: 9d16bbe2..240b805b
Reviewed artifact: commit 240b805b
Reviewed milestone: M1
Review date: 2026-07-29
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: root-m1-r2-resolution
Reviewer context ID: m1-r3-primary-and-second-fresh-agents
Context separation mechanism: fresh-separate-agents-blind-first
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: validator behavior; generated-output machinery; compatibility identity; multi-component change
Risk-tier classifier: deterministic-changed-surface-check
Governing artifacts: specs/progressive-boundary-first-skill-guidance.md@240b805b#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@240b805b#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@240b805b#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@240b805b#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9
Formal criteria: code-review-first-pass-v1; independent-review-gate-v1; requirement-fidelity-gate-v1
Initial packet inventory: specs/progressive-boundary-first-skill-guidance.md@240b805b#sha256:983a6cab29dd12ff18866f06a2a818ab9c198dd3a3ccddccc06c8e95516d2dd2; specs/progressive-boundary-first-skill-guidance.test.md@240b805b#sha256:30595f49cb782e772588334dc9b6c31c728f5b6567892784d6fa27488e3f5257; docs/plans/2026-07-29-progressive-boundary-first-skill-guidance.md@240b805b#sha256:7aa4b69d2636eb0ff6bf6fb77bcf6835ad2dd5c889feaa8b786e1badce65d5c1; docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md@240b805b#sha256:ad78a2f644679a6b0dbaaa6000c1c9b0a8751f9abeb238fcb74cee04e16181c9; commit:240b805b.diff@240b805b#sha256:4fbd40a30a30a896380f30f5f70d47dc2d09f2ce43a82eafd80cffcde71945a0
Prompt template version: code-review-v1
Initial packet hash: sha256:8149200079e803bfbc27d79a7e4df920542fc9af01c2203cf5614c0dae16c2c5
Manifest owner: workflow-orchestrator
Affected behavior: manifest authority; resource split; 14-target projection; stage maps; activation identity; recovery and diagnostics
Highest-impact failure modes: catchable interruption leaves mixed projections; parallel resource authority drifts; missing-manifest diagnostics lose identity
Changed boundaries: identity authority; composition; temporal retry; recovery; compatibility; filesystem environment
Evidence expected: T1, T2, T5 negative matrices; semantic accounting; exact maps; independent digests; activation, CLI, and interruption probes
Areas requiring direct inspection: parser; resource authority; inventory; write restoration; digest; activation; CLI; skill validation; tests
Areas intentionally out of scope: M2, M3, M4, PR, CI, and final verification
Risk classes considered: identity authority; composition; temporal retry; recovery; compatibility; filesystem containment; fidelity; diagnostics
Falsifiable review questions: Can catchable interruption leave partial state; is the manifest the only projection matrix; does every missing resource retain exact diagnostic identity
Material findings: CR-M1-R3-001, CR-M1-R3-002, CR-M1-R3-003
Immediate next stage: review-resolution
Milestone closeout: resolution-needed
Required review-resolution: yes
Verify readiness: not-claimed

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, and review resolution
- Open blockers: three R3 findings
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: CR-M1-R3-001, CR-M1-R3-002, CR-M1-R3-003
- Recording status: recorded
- Recording blocker: none
- Review record: reviews/code-review-m1-r3.md
- Review log: review-log.md
- Review resolution: review-resolution.md
- Reviewed milestone: M1
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: CR-M1-R3-001, CR-M1-R3-002, CR-M1-R3-003
- Verify readiness: not-claimed

## Findings

### CR-M1-R3-001 — Catchable interruption leaves a mixed projection tree

Finding ID: CR-M1-R3-001
Severity: major
Location: `scripts/boundary_first_reference.py`
Evidence: The transaction restores snapshots only for `OSError`. A public-path probe raising `KeyboardInterrupt` after six writes left six of fourteen targets changed.
Required outcome: Restore the exact prior target set before propagating a catchable in-process interruption, then allow deterministic retry.
Safe resolution path: Restore on `BaseException`, preserve the original interruption after successful restoration, retain explicit restoration-failure reporting, and add a `KeyboardInterrupt` regression.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M1-R3-002 — Projection code retains a parallel resource inventory

Finding ID: CR-M1-R3-002
Severity: blocker
Location: `scripts/boundary_first_reference.py`
Evidence: `RESOURCE_IDS` and `RESOURCE_CONTRACTS` restate the complete resource, source, target, and consumer matrix even though the ADR names the manifest as the sole declarative projection matrix.
Required outcome: Derive projection solely from the manifest without a second complete resource/consumer inventory.
Safe resolution path: Replace the duplicated matrix with independent structural and invariant validation, retain closed vocabularies only where the contract expressly requires them, and add a source-level regression against parallel tuple inventories.
needs-decision rationale: none
Auto-fix class: declared-safe

### CR-M1-R3-003 — Missing-manifest diagnostics lose path and expectation

Finding ID: CR-M1-R3-003
Severity: blocker
Location: `scripts/boundary_first_reference.py`, `scripts/boundary_first_validation.py`
Evidence: Missing manifest still raises a text-only error, so the CLI reports `path=-` and activation substitutes the compact-core path.
Required outcome: Both public consumers identify `specs/boundary-first-resources.yaml`, a stable check, and the explicit expected condition.
Safe resolution path: Raise a structured missing-manifest error and add CLI and activation regressions.
needs-decision rationale: none
Auto-fix class: declared-safe

## Prior-finding reconciliation

| Finding | Result | Basis |
| --- | --- | --- |
| CR-M1-R1-001 | resolved | Exact tuple and version mutations fail, though R3 separately rejects the duplicate implementation authority. |
| CR-M1-R1-002 | resolved | The exact compact scan exists in the compact core and all projections. |
| CR-M1-R1-003 | failed-remediation | `OSError` recovery works, but `KeyboardInterrupt` leaves a mixed tree. |
| CR-M1-R1-004 | failed-remediation | Family-resource identity is fixed, but missing-manifest identity is not. |
| CR-M1-R2-001 | resolved | Recursive canonical and skill-local inventory rejects alternate and nested additions. |
| CR-M1-R2-002 | failed-remediation | Family paths are structured, but the missing-manifest public path remains incomplete. |

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Atomicity, sole authority, and diagnostics remain incomplete. |
| Test coverage | block | Catchable interruption and missing-manifest public paths lack proof. |
| Edge cases | block | `KeyboardInterrupt` and absent manifest fail the contract. |
| Error handling | block | Interruption leaves mixed state and missing-manifest identity is flattened. |
| Architecture boundaries | block | A parallel full matrix conflicts with the ADR. |
| Compatibility | pass | Stable core path/version and pending state remain intact. |
| Security/privacy | pass | Inspected diagnostics remain repository-relative. |
| Derived artifact currency | pass | Current 14 M1 projections are byte-current. |
| Unrelated changes | pass | The target remains M1-scoped. |
| Validation evidence | concern | Named suites pass but focused probes falsify their sufficiency. |

## Requirement-fidelity receipt

Applicability: applicable
Relevant spec clauses decomposed: yes
Property matrix complete: yes
Multi-surface contracts identified: yes
Validator assertions checked against spec: yes
Compressed requirement risk: present for authority, interruption, and missing-manifest diagnostics
No-finding rationale: not-applicable because material findings exist

## Independent-review receipts

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Independence level: L2
Second review: satisfied; both reviewers requested changes
Confidence: high
Unreviewed surfaces: M2 automatic guidance; M3 selector routing; M4 packages and activation readiness; final verification

No clean-review sufficiency receipt is issued because the review is not clean.
