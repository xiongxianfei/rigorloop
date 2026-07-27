# Boundary-First Proof Modeling Test-Spec Review R25

Review ID: test-spec-review-r25

Stage: test-spec-review

Round: 25

Reviewer: Codex test-spec-review skill

Target: specs/rigorloop-workflow.test.md

Reviewed artifact: corrected lease-first publisher-recovery proof map at
`a9748c41`

Status: approved

Review status: approved

Material findings: None

Recording status: recorded

Review date: 2026-07-27

Context separation mechanism: tracked-artifact and governing-contract reset

Reviewed commit: `a9748c41`

Reviewed test-spec identity:
`sha256:8c660c1728b189c87646f089bff3ee12c16f793c8691d26143cf2086378e23b1`

Immediate next stage: implement

Implementation handoff: allowed

Stop condition: none

## Result

Approved with no material findings.

T51 now projects the complete approved publisher transaction into eight
separately named executable property obligations. Its executable steps start
with lock acquisition and ordered global discovery, then require durable exact
lease and working-root evidence before the first lifecycle invocation.

## Review dimensions

| Dimension | Verdict |
| --- | --- |
| R28y traceability | pass |
| Exact schema and identity proof | pass |
| Negative mutation coverage | pass |
| Crash-boundary coverage | pass |
| Closed publication-state coverage | pass |
| Global discovery and conflict coverage | pass |
| Manual-recovery coverage | pass |
| No-reinvocation coverage | pass |
| Milestone and command ownership | pass |
| Input identity currency | pass |
| Implementation handoff | pass |

## Finding reconciliation

`BFP-TSR24-1` is resolved. The corrected steps now require:

1. the exclusive publisher lock;
2. fixed-order global discovery with no stage invocation;
3. fresh run and publisher identities only for a clean state;
4. exclusive lease creation and fsync;
5. deterministic working-root creation and fsync;
6. observation of those durable prerequisites at first lifecycle invocation.

Failures at either durability boundary prove that no lifecycle work or
publication mutation occurred.

## Validation

- `python scripts/test-boundary-proof.py` — 77 tests passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-workflow.test.md --path docs/plans/2026-07-25-boundary-first-proof-modeling.md --path docs/plan.md` — passed with existing merge-dependent-language warnings.
- `git diff --check` — passed.

## Handoff

M2 may implement `T51-PUBLISHER-IDENTITY` through
`T51-MANUAL-RECOVERY`. Code-review finding `BFP-CR-M2-10` remains open until
the implementation, regenerated canonical evidence, and M2 rereview pass.
