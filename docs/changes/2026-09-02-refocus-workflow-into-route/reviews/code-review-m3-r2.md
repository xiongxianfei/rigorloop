# Code Review M3 R2: Adapter Release Corrections

Review ID: code-review-m3-r2
Stage: code-review
Round: r2
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: corrected M3 through 56019130
Reviewed artifact: complete M3 implementation through 56019130 and R1 correction 71efb815..56019130
Reviewed milestone: M3
Review date: 2026-09-02
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m3-r2.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`; `docs/changes/2026-09-02-refocus-workflow-into-route/change.yaml`
- Open blockers: none
- Next stage: final closeout
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-02-refocus-workflow-into-route/reviews/code-review-m3-r2.md`
- Review log: `docs/changes/2026-09-02-refocus-workflow-into-route/review-log.md`
- Review resolution: `docs/changes/2026-09-02-refocus-workflow-into-route/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: ready for route-owned closeout
- Remaining implementation milestones: M3 before closeout; none after closeout
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Scope and authority

R2 independently inspected the complete M3 outcome and correction against Design Review `design-review-r1`, Delivery Review `delivery-review-r1`, the M3 requirement allocation, TG-12 through TG-16, and RFR-M3-CR1/RFR-M3-CR2. The reviewed implementation remained untouched during formal review.

## Prior-finding closeout

- RFR-M3-CR1: resolved. Package version, bundled release index, documentation, and candidate metadata use the unpublished v0.5.1 identity. A direct test regenerates all three archives, compares the complete resulting metadata with the bundled file, asserts route is present and workflow absent, and preserves the immutable v0.5.0 metadata hash.
- RFR-M3-CR2: resolved. Normal `init --write-state` replaces only a selected workflow install whose complete root matches its lockfile. Unmanaged, drifted, mixed, obsolete-archive, and dry-run states stop with bounded guidance. Direct tests prove successful replacement, unrelated-target preservation, pre-mutation state guidance, failed-write rollback, and the equivalent clean retry basis.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | Current distributions expose route only; stable `workflow.automation` remains unchanged; no publication or workflow alias was introduced. |
| Test coverage | pass | Real candidate metadata, supported archives, managed migration, rollback, unrelated targets, obsolete and mixed states, and current package fixtures have direct coverage. |
| Edge cases | pass | Exact versus drifted state, missing `--write-state`, dry run, archive mismatch, partial write, recovery, and multi-target preservation have deterministic outcomes. |
| Error handling | pass | Archive verification precedes deletion; migration snapshots the exact managed roots and state, restores them on write or post-write verification failure, and reports a bounded error. |
| Architecture boundaries | pass | CLI performs deterministic install-state handling only; semantic route ownership and stored lifecycle authority are unchanged. |
| Compatibility | pass | v0.5.0 metadata is byte-stable, historical records are untouched, and v0.5.1 remains explicitly unpublished. |
| Security/privacy | pass | Migration operates only on repository-relative roots selected by validated adapter state and introduces no network, credential, or diagnostic-data expansion. |
| Derived artifact currency | pass | Bundled v0.5.1 metadata equals freshly generated route-only archive identities for Codex, Claude Code, and opencode. |
| Unrelated changes | pass | The correction is limited to release identity, bounded migration, direct proof, documentation, and lifecycle evidence. |
| Validation evidence | pass | The seven M3 commands pass: 156 adapter tests, 8 build tests, 352 validator tests, 25 token tests, skill parity, 365 package passes with 2 historical skips, and 12 broad-smoke checks. |

## No-finding rationale and residual risk

No required M3 correction remains. The migration intentionally does not overwrite unmanaged, drifted, or mixed installs and does not add a broad replacement flag. Abrupt host termination is not claimed to be an atomic filesystem transaction; the direct recovery guarantee covers detected installation and verification failures, while pre-mutation exact-state checks and unchanged lock state make other incomplete states fail closed on retry. Publication, hosted availability, and live release installation remain outside this milestone.

## Handoff

M3 is clean for route-owned milestone closeout. Because M3 is the final implementation milestone, the next required gate is final holistic Code Review before Verify; this milestone review does not establish branch, Verify, PR, or release readiness.
