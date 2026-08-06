# Test-Spec Review R2

Review ID: test-spec-review-r2
Stage: test-spec-review
Round: 2
Reviewer: independent Codex test-spec-review peer
Target: `specs/boundary-first-v1-v0-3-7-activation-release.test.md`
Target revision: `74b19fe727ea92fb7434fe68f12c635c84ce690f`
Status: changes-requested
Review status: changes-requested
Material findings: BFA-TSR2-001
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: BFA-TSR2-001
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/test-spec-review-r2.md
- Review log: docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-log.md
- Review resolution: docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-resolution.md#test-spec-review-r2
- Open blockers: BFA-TSR2-001
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: revised proof-map rows require independent rereview

## Prior Finding Closeout

- BFA-TSR1-001: resolved; all proof rows use admitted levels.
- BFA-TSR1-002: resolved; lifecycle readiness uses M1 fixture, M4 actual, and release-checkpoint proof.
- BFA-TSR1-003: remains open only through BFA-TSR2-001.
- BFA-TSR1-004: resolved; MP1 and MP2 are executable and auditable.

## Finding BFA-TSR2-001

Finding ID: BFA-TSR2-001
Severity: major
Location: PRF-006 and PRF-008
Evidence: PRF-006 omits T11, MP1, checkpoint commands, and release-checkpoint evidence for pre-publication recovery. PRF-008 claims actual atomic evidence but omits CMD17 and MP1, which produce it.
Required outcome: Every hybrid boundary row directly cites the procedure and command that produce its claimed external evidence.
Safe resolution path: Add T11, MP1, checkpoint commands, and release-checkpoint evidence to PRF-006; add CMD17 and MP1 to PRF-008 while retaining public-environment proof.
needs-decision rationale: none

## Review Dimensions

| Dimension | Verdict |
| --- | --- |
| governing-contract alignment | pass |
| requirement coverage | concern |
| example coverage | pass |
| negative and boundary coverage | pass |
| proof-level adequacy | block |
| milestone mapping | pass |
| command validity | pass |
| fixture and data design | pass |
| manual-proof boundary | pass |
| observability | pass |
| determinism and isolation | pass |
| scope and non-goals | pass |
| execution economics | pass |
| traceability | block |
| implementation handoff | block |

## No-Side-Effect Checks

- All seven packet hashes matched at HEAD `62f675c5b47bd022a067cf887c72ca588eb26bd9`.
- Scoped diff, boundary-first, lifecycle, metadata, review-artifact, readability, and selector checks passed.
- Proof levels use only integration and end-to-end.
- Existing help surfaces and CMD25's workflow parity seam resolved.
- No test suites, fixtures, network queries, credentials, publication, or mutating commands ran.
