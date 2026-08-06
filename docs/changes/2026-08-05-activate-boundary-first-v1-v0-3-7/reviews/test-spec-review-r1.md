# Test-Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: independent Codex test-spec-review peer
Target: `specs/boundary-first-v1-v0-3-7-activation-release.test.md`
Target revision: `eb488f99233c191f8b77b33cf75f90bd91eaa79a`
Status: changes-requested
Review status: changes-requested
Material findings: BFA-TSR1-001, BFA-TSR1-002, BFA-TSR1-003, BFA-TSR1-004
Immediate next stage: test-spec revision
Implementation handoff: not-allowed

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: BFA-TSR1-001, BFA-TSR1-002, BFA-TSR1-003, BFA-TSR1-004
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/reviews/test-spec-review-r1.md
- Review log: docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-log.md
- Review resolution: docs/changes/2026-08-05-activate-boundary-first-v1-v0-3-7/review-resolution.md#test-spec-review-r1
- Open blockers: BFA-TSR1-001, BFA-TSR1-002, BFA-TSR1-003, BFA-TSR1-004
- Immediate next stage: test-spec revision
- Implementation handoff: not-allowed
- Stop condition: revised test spec requires independent rereview
- Structural inventory: all 35 requirements, 15 acceptance criteria, eight examples, 12 edge cases, eight boundaries, and seven interactions are present.

## Finding BFA-TSR1-001

Finding ID: BFA-TSR1-001
Severity: major
Location: PRF-007, PRF-014, and T15
Evidence: Both proof rows use `migration`, which is not in the closed proof-level enum.
Required outcome: Every proof obligation uses a valid closed-enum proof level.
Safe resolution path: Use `integration` or `end-to-end` according to the actual rollback execution boundary and keep migration only as descriptive semantics.
needs-decision rationale: none

## Finding BFA-TSR1-002

Finding ID: BFA-TSR1-002
Severity: major
Location: PRF-002, T12, CMD21-CMD23, and milestone proof map
Evidence: Test-spec review evidence is circular for publication-time BFA-R017; current-tree authoring validators do not exercise missing lifecycle evidence fixtures or align with M4/release-checkpoint timing.
Required outcome: Give BFA-R017 and BND-STATE-001 direct phase-correct automated proof and non-circular runtime evidence.
Safe resolution path: Add a planned regression command for missing evidence classes, schedule current-state readiness at M4/release checkpoint, and use M4 candidate plus release-checkpoint evidence.
needs-decision rationale: none

## Finding BFA-TSR1-003

Finding ID: BFA-TSR1-003
Severity: major
Location: PRF-003, PRF-004, PRF-012, PRF-013, T13, and milestone proof map
Evidence: Atomic publication, actual tag-workflow gating, and public closeout are not directly connected to their commands, milestone timing, and distinct evidence artifacts; T13 has no M3 automated workflow-regression command.
Required outcome: Directly connect atomic publication, tag workflow, and public closeout to distinct automated/actual commands and evidence.
Safe resolution path: Add an M3 workflow-composition regression command, keep actual CMD20 plus MP2, and add CMD17/atomic evidence and CMD20/public evidence to the owning proof rows.
needs-decision rationale: none

## Finding BFA-TSR1-004

Finding ID: BFA-TSR1-004
Severity: major
Location: MP1 and MP2
Evidence: Procedures omit explicit automation rationale, environment, owner/stage, evidence artifacts, pass/failure conditions, and exact MP2 public queries/smoke commands.
Required outcome: Make both procedures executable, bounded, and independently auditable.
Safe resolution path: Add owner/stage, rationale, prerequisites, exact commands, evidence, pass/failure, cleanup/recovery, and forbidden-action fields; bind MP2 to exact workflow, GitHub/npm/integrity queries, three public npx commands, CMD18, and CMD19.
needs-decision rationale: none

## Review Dimensions

| Dimension | Verdict |
| --- | --- |
| Governing-contract alignment | concern |
| Requirement coverage | block |
| Example coverage | concern |
| Negative and boundary coverage | pass |
| Proof-level adequacy | block |
| Milestone mapping | block |
| Command validity | block |
| Fixture and data design | pass |
| Manual-proof boundary | block |
| Observability | concern |
| Determinism and isolation | pass |
| Scope and non-goals | pass |
| Execution economics | pass |
| Traceability | block |
| Implementation handoff | block |

## Exact Checks

- Packet hashes matched at review HEAD `466e83e26c8c737929cb881dc0918106681c5a5c`.
- Scoped diff check passed.
- Boundary-first structural validation passed.
- Artifact lifecycle validated nine artifacts.
- Change metadata and review artifacts passed.
- Markdown readability passed with nonblocking warnings.
- Explicit validation selection had no unclassified paths, blockers, or registration debt.
- No-side-effect help checks resolved existing release commands.
- Static ID audit found the complete governed ID inventory.
- No test suites, fixtures, network, secret, publication, or mutating release commands ran.
