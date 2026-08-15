# Code Review M2 R1: Spec Package Simplification

Review ID: code-review-M2-r1

Stage: code-review

Round: r1

Reviewer: Codex independent code-review context

Target: implementation milestone M2 diff `40f6539b..89efb1f3`

Reviewed milestone: M2

Reviewed artifact: commit `89efb1f3`

Reviewed revision: `89efb1f3`

Review date: 2026-08-15

Recording status: recorded

Status: changes-requested

Review status: changes-requested

Material findings: SPSIM-M2-CR1, SPSIM-M2-CR2

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: review record, invocation manifest, review log, review resolution, and workflow review state
- Open blockers: two accepted M2 corrections
- Next stage: implement M2 correction
- Review status: changes-requested
- Material findings: `SPSIM-M2-CR1`, `SPSIM-M2-CR2`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-15-spec-skill-simplification/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-15-spec-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-15-spec-skill-simplification/review-resolution.md#code-review-M2-r1`
- Reviewed milestone: M2
- Milestone closeout: open
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: `SPSIM-M2-CR1`, `SPSIM-M2-CR2`
- Verify readiness: not-claimed

## Actual diff summary

M2 shortens the universal skill, adds one governed reference, adds the skeleton insertion marker, extends the existing packaged-resource allowlist, and adds focused contract assertions. The static validation suite passes and both loaded profiles decrease, but semantic inspection found two preservation gaps hidden by phrase-level assertions.

## Material findings

## Finding SPSIM-M2-CR1

Finding ID: SPSIM-M2-CR1

Severity: major

Location: `skills/spec/references/governed-spec-authoring.md`

Evidence: The governed reference compresses R21-R42 into phrases such as “bound identities,” “both bases,” and “preserves identity, history, and state.” Those phrases do not explicitly require the change ID, artifact kind and role, governing-input and retry identities, complete spec validation and content identity, complete restart evidence fields, or preservation of completed authoring and review evidence. A future executor could satisfy the prose while omitting contract-mandated transaction inputs or writes.

Required outcome: State every mandatory identity, prerequisite, commit result, restart evidence field, preservation rule, and stop condition from R21-R42 compactly and directly. Extend focused assertions around semantic groups rather than freezing whole sentences.

Safe resolution path: Revise only the governed reference, its focused tests, and M2 evidence; preserve the selected package boundary and keep both loaded profiles below baseline.

needs-decision rationale: none

auto_fix_class: bounded-semantic

deterministic_authority: R21-R42 define the exact governed transaction contract.

affected_paths: `skills/spec/references/governed-spec-authoring.md`, `scripts/test-skill-validator.py`, `docs/changes/2026-08-15-spec-skill-simplification/evidence/m2-package-implementation.md`

required_validation: focused and broad skill tests, canonical validation, build checks, profile measurement, and diff checking

## Finding SPSIM-M2-CR2

Finding ID: SPSIM-M2-CR2

Severity: major

Location: `skills/spec/SKILL.md`

Evidence: The M1 ledger assigns universal proposal settlement, unrelated-target protection, normative scope-aware requirements, and superseded replacement identification to the compact common path. The current text does not explicitly cover later contradictory proposal reviews and required resolution, never overwriting an unrelated spec, not inventing excluded scope, normative requirement language, or identifying the replacement of a superseded spec.

Required outcome: Restore these universal semantics in compact form and add focused preservation assertions. Do not restore obsolete duplicated sections or move these rules behind governed loading.

Safe resolution path: Update only `SKILL.md`, focused tests, and M2 evidence while preserving shared exact blocks and profile reduction.

needs-decision rationale: none

auto_fix_class: bounded-semantic

deterministic_authority: R2 and M1 rows SRULE-003, SRULE-004, SRULE-022, and SRULE-024 define the missing semantics.

affected_paths: `skills/spec/SKILL.md`, `scripts/test-skill-validator.py`, `docs/changes/2026-08-15-spec-skill-simplification/evidence/m2-package-implementation.md`

required_validation: focused and broad skill tests, readability validation, profile measurement, and rule-ledger inspection


## Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | fail | R21-R42 and M1 retained-inline rows are not fully explicit. |
| Test coverage | concern | All tests pass, but focused checks cover phrases rather than several complete semantic groups. |
| Edge cases | fail | Restart evidence and unrelated-target protection are under-specified. |
| Error handling | pass | Invalid signals and missing resources fail closed. |
| Architecture boundaries | pass | The package uses existing owners and introduces no new state model. |
| Compatibility | fail | Superseded replacement identification and complete upstream review settlement are missing. |
| Security/privacy | pass | No new external or sensitive-data surface exists. |
| Derived artifact currency | pass for M2 | Existing build and generated checks pass; M3 owns adapter parity. |
| Unrelated changes | pass | The committed diff is limited to planned M2 surfaces and evidence. |
| Validation evidence | pass | Canonical, focused, broad, build, boundary, prose, metadata, and diff checks passed. |

## Handoff

M2 returns to implementation for the two accepted corrections, then requires same-stage code rereview. This review does not authorize M3, verification, branch readiness, or PR readiness.
