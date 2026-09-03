# Code Review M1 R2: PR safeguard preservation correction

Review ID: code-review-m1-r2
Stage: code-review
Round: r2
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Target: M1 correction commit e1493f69
Reviewed artifact: M1 implementation 6d2be4e2..e1493f69
Reviewed milestone: M1
Review date: 2026-09-03
Status: clean-with-notes
Review status: clean-with-notes
Material findings: none
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-09-03-relax-pr-evidence-tail/reviews/code-review-m1-r2.md`, `docs/changes/2026-09-03-relax-pr-evidence-tail/review-log.md`, and `docs/changes/2026-09-03-relax-pr-evidence-tail/review-resolution.md`
- Open blockers: none
- Next stage: implement next milestone
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-09-03-relax-pr-evidence-tail/reviews/code-review-m1-r2.md`
- Review log: `docs/changes/2026-09-03-relax-pr-evidence-tail/review-log.md`
- Review resolution: `docs/changes/2026-09-03-relax-pr-evidence-tail/review-resolution.md`
- Reviewed milestone: M1
- Milestone closeout: closed
- Remaining implementation milestones: M2
- Required review-resolution: no
- Finding IDs: none
- Verify readiness: not-claimed

## Scope and authority

R2 independently reread the complete canonical M1 package and the bounded PRTAIL-M1-CR1 correction against the focused specification, unaffected prior PR requirements, approved architecture, and Delivery Review `delivery-review-r2`. No implementation file was changed during rereview.

## Prior-finding closeout

PRTAIL-M1-CR1 is resolved. The governed-signal negative partition, retry reconciliation, procedure-owned body applicability and adequacy, exact result fields, and current owning-evidence condition are restored and directly asserted. The correction does not restore the retired direct-child proxy.

## Findings

No material findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The cumulative `none`/`evidence-only`/`invalidating` rule implements the focused delta while exact preservation assertions retain unaffected PR requirements. |
| Test coverage | pass | Focused tests cover closed outcomes, multi-commit topology independence, authority negatives, protected and mixed changes, Verify distinction, and the five corrected preservation clauses. |
| Edge cases | pass | Same revision, non-ancestor, stale, cross-change, mixed, unknown, and retry/concurrent-state behavior have direct contract proof. |
| Error handling | pass | Invalid suffixes and invalid governed signals block before external mutation and route to the applicable owner. |
| Architecture boundaries | pass | PR remains a read-only consumer; Verify still owns branch readiness and its registered result remains exact. |
| Compatibility | pass | Existing remote, PR, CI, refresh, draft, retry, body, result, and read-back protections remain explicit. |
| Security/privacy | pass | Exact identity, secret inspection, no-force behavior, and protected-surface rejection remain current. |
| Derived artifact currency | pass | Canonical and temporary generated-skill validation pass; tracked adapter candidate parity remains M2 scope. |
| Unrelated changes | pass | The correction is limited to retained-contract restoration, direct tests, and lifecycle evidence. |
| Validation evidence | pass | 365 skill-validator tests, canonical validation, temporary generated-skill validation, focused boundary validation, size measurement, and whitespace validation pass. |

## No-finding rationale and residual risk

The complete M1 text now satisfies both the focused topology relaxation and the unaffected prior contract within the existing 11,750-byte ceiling. Runtime classification remains instruction-driven and therefore depends on disciplined authority inspection; M2 still must prove exact adapter and current-candidate metadata parity.

## Handoff

M1 is clean for workflow closeout. Workflow may complete M1 with this exact review evidence and start M2; final verification remains unclaimed.
