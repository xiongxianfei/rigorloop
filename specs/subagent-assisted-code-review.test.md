# Subagent-Assisted Code Review Test Spec

## Status

active

## Related spec and plan

- Spec: `specs/subagent-assisted-code-review.md`
- Plan: `docs/plans/2026-07-06-subagent-assisted-code-review.md`
- Architecture/ADRs: not required; architecture assessment recorded in `docs/changes/2026-07-06-subagent-assisted-code-review/architecture-assessment.md`

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Proposal | `docs/proposals/2026-07-06-subagent-assisted-code-review.md` | accepted | `proposal-review-r1` |
| Proposal review | `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/proposal-review-r1.md` | approved | `proposal-review-r1` |
| Feature spec | `specs/subagent-assisted-code-review.md` | approved | `spec-review-r1` |
| Spec review | `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/spec-review-r1.md` | approved | `spec-review-r1` |
| Architecture assessment | `docs/changes/2026-07-06-subagent-assisted-code-review/architecture-assessment.md` | architecture-not-required | `architecture-not-required` |
| Plan | `docs/plans/2026-07-06-subagent-assisted-code-review.md` | active; plan-review approved | `plan-review-r1` |
| Plan review | `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/plan-review-r1.md` | approved | `plan-review-r1` |

## Testing strategy

Use skill validation, review-artifact validation, focused validator unit tests, fixtures, generated-output checks, and adapter packaging proof.

M1 proves the public `code-review` contract and assets preserve direct review, reviewer-of-record authority, role selection, packet boundaries, aggregation, coverage recording, advisory import behavior, and first-slice non-goals.
M2 proves parser-owned validation for closed role/status vocabulary, malformed or missing packets, missing coverage, deduplication, conflicts, and low-evidence non-promotion.
M3 proves generated skills and adapter packaging stay aligned with authored source through repository-owned scripts.

Manual proof is limited to behavior-preservation notes for no auto-fix behavior, no required target-native configs, no persistent packet files, no parallel execution, and unchanged verify/PR boundaries.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R2 | T1, T2, T13 | contract, unit | Reviewer-of-record and direct-review preservation. |
| R3-R5 | T3, T4, T5 | unit, integration | Closed role vocabulary and changed-surface selection. |
| R6-R8 | T6, T7, T8 | unit, integration | Input packet, read-only boundary, and packet schema. |
| R9-R12 | T9, T10, T11, T12 | unit, integration | Evidence promotion, dedupe, conflicts, missing coverage, and malformed packets. |
| R13-R14 | T13, T14 | contract, integration | Lifecycle gates and external advisory import. |
| R15-R17 | T15 | contract, manual | First-slice boundaries for Claude configs, packet files, and parallel execution. |
| R18 | T16 | integration, smoke | No unjustified new dependency and generated-output proof. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1 | Direct review without subagents remains valid. |
| E2 | T4, T5 | Generated-output surfaces select the right specialists or record cap rationale. |
| E3 | T9, T11 | One evidenced security finding can be promoted without consensus. |
| E4 | T12 | Low-evidence suggestion is not promoted. |
| E5 | T7, T10 | Malformed or missing required packets block or mark review incomplete. |
| E6 | T14 | Codex/GitHub review remains advisory unless imported. |
| E7 | T5, T11 | Review record exposes subagent coverage and aggregation results. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T1 | No specialist triggers still allows direct review. |
| EC2 | T5 | Specialist cap records omission or substitute coverage. |
| EC3 | T10 | Missing required packet blocks or marks incomplete. |
| EC4 | T7 | Malformed packet fails closed. |
| EC5 | T3 | Unknown role fails closed. |
| EC6 | T7 | Unknown advisory status fails closed. |
| EC7 | T10 | Duplicate findings are collapsed before canonical recording. |
| EC8 | T9 | One evidenced security finding blocks without consensus. |
| EC9 | T12 | Low-evidence suggestion is downgraded or ignored. |
| EC10 | T14 | External advisory output does not replace canonical review. |
| EC11 | T15 | Claude custom configs are optional in the first slice. |
| EC12 | T15 | Persistent packet files are optional in the first slice. |
| EC13 | T4 | Docs-only command/contract changes select docs/ops coverage. |
| EC14 | T4 | Generated-output and release-package surfaces trigger both coverage classes. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/validate-skills.py skills/code-review/SKILL.md` | existing/configured | implement | M1 | M1 closeout | fail milestone validation | not applicable; structural validator | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | local only; no network |
| CMD2 | `python scripts/test-skill-validator.py -k subagent_code_review` | planned-for-implementation | implement | M2 | M2 closeout | fail packet/coverage validation proof | zero selected tests fail | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | local only; no network |
| CMD3 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review` | existing/configured | implement | M2 | M2 closeout | fail review-artifact structure validation | not applicable; review validator | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | local only; no network |
| CMD4 | `python scripts/build-skills.py --check` | existing/configured | implement | M3 | M3 closeout | fail generated-skill sync validation | not applicable; build check | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | local generated-output check only; no hand edits |
| CMD5 | `python scripts/test-build-skills.py` | existing/configured | implement | M3 | M3 closeout | fail generated-skill proof | zero selected tests fail | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | local only; no network |
| CMD6 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M3 | M3 closeout | fail adapter packaging proof | zero selected tests fail | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | local package/fixture proof; no publication |
| CMD7 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/subagent-assisted-code-review.md --path specs/subagent-assisted-code-review.test.md --path docs/plans/2026-07-06-subagent-assisted-code-review.md --path docs/plan.md --path docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | existing/configured | test-spec / verify | lifecycle closeout | test-spec-review closeout | block downstream handoff on lifecycle inconsistency | not applicable; lifecycle validator | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | local only; no network |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T1, T2, T4, T5, T6, T13, T14, T15 | MQA1 | CMD1, CMD7 | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`; behavior-preservation evidence when created | code-review M1 | Proves skill guidance, assets, lifecycle boundaries, and first-slice non-goals. |
| M2 | T3, T7, T8, T9, T10, T11, T12 | none | CMD1, CMD2, CMD3, CMD7 | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml` | code-review M2 | Proves closed vocabulary, packet validation, missing coverage, dedupe, conflict handling, and suggestion downgrade. |
| M3 | T13, T14, T15, T16 | MQA1 | CMD4, CMD5, CMD6, CMD7 | `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`; behavior-preservation evidence when created | code-review M3 | Proves generated skill and adapter packaging alignment without hand edits. |

## Test cases

### T1. Direct code review remains supported

- Covers: R1, R2, E1, EC1, AC1, AC2
- Level: contract
- Command IDs: CMD1
- Fixture/setup: `skills/code-review/SKILL.md` and any code-review skeleton assets.
- Steps: Inspect or validate that direct review remains a supported path when no subagent triggers apply.
- Expected result: The skill does not require subagent execution for every review and keeps canonical review recording behavior.
- Failure proves: subagent-assisted mode accidentally replaces ordinary code review.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/validate-skills.py skills/code-review/SKILL.md`
- Required by milestone: M1

### T2. Subagents cannot own lifecycle review authority

- Covers: R1a-R1c, R13, AC2, AC13, AC16
- Level: contract
- Command IDs: CMD1
- Fixture/setup: `skills/code-review/SKILL.md` and review-result guidance.
- Steps: Confirm subagents cannot approve, block, close milestones, write review records, or claim verify/PR readiness.
- Expected result: Only the canonical `code-review` artifact owns lifecycle review status and findings.
- Failure proves: review authority is fragmented.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/validate-skills.py skills/code-review/SKILL.md`
- Required by milestone: M1

### T3. Specialist role vocabulary fails closed

- Covers: R3, R3b, EC5, AC3
- Level: unit
- Command IDs: CMD2
- Fixture/setup: valid and invalid role fixtures for subagent packet or selection validation.
- Steps: Validate a known role and an unknown role.
- Expected result: Known roles pass; unknown roles fail with a closed-vocabulary diagnostic.
- Failure proves: unsupported specialist roles can pass silently.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`
- Required by milestone: M2

### T4. Changed surfaces select expected specialists

- Covers: R4, R5, E2, EC13, EC14, AC4
- Level: unit
- Command IDs: CMD2
- Fixture/setup: changed-surface fixtures for validator, test, security, generated-output, compatibility, performance, and docs surfaces.
- Steps: Run selection validation against representative changed surfaces.
- Expected result: Triggered specialists match the spec and omissions have rationale where required.
- Failure proves: broad changes can silently under-review specialist risks.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`
- Required by milestone: M2

### T5. Specialist cap records omission or substitute coverage

- Covers: R4c-R4e, R11, E2, E7, EC2, AC4, AC12
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: review-record fixture with more triggered specialists than the default cap.
- Steps: Validate selected, omitted, or folded specialists plus coverage rationale.
- Expected result: The review record exposes what ran, what did not run, and whether coverage remains acceptable or incomplete.
- Failure proves: cap behavior can hide missing review coverage.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review`
- Required by milestone: M2

### T6. Input packets preserve bounded read-only review

- Covers: R6, R7, AC5
- Level: contract
- Command IDs: CMD1
- Fixture/setup: `skills/code-review/SKILL.md` and input packet asset when added.
- Steps: Confirm input packet fields include review ID, role, scope, governing artifacts, must-check, must-not, and output format, and exclude secrets or write authority.
- Expected result: Subagent input packets are bounded and read-only by default.
- Failure proves: subagents can receive unbounded context or mutation authority.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/validate-skills.py skills/code-review/SKILL.md`
- Required by milestone: M1

### T7. Packet schema rejects malformed fields and unknown statuses

- Covers: R8, R8d, EC4, EC6, AC6, AC7
- Level: unit
- Command IDs: CMD2
- Fixture/setup: positive `subagent-review-packet-v1` fixture and negative malformed fixtures.
- Steps: Validate packet schema version, role, status, reviewed scope, coverage, findings, rationale, and limitations.
- Expected result: Valid packet passes; unknown status, unknown schema, and missing required fields fail closed.
- Failure proves: malformed advisory output can influence canonical review.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`
- Required by milestone: M2

### T8. Missing required specialist coverage blocks or marks incomplete

- Covers: R12, E5, EC3, AC7
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: review-record fixture with triggered specialist coverage missing.
- Steps: Validate canonical status and coverage section behavior.
- Expected result: Missing required coverage records blocked or inconclusive status unless safe substitute coverage is recorded.
- Failure proves: missing specialist evidence can be treated as a clean review.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review`
- Required by milestone: M2

### T9. Evidenced specialist finding can block without consensus

- Covers: R9, R9d, E3, EC8, AC8, AC10
- Level: integration
- Command IDs: CMD2
- Fixture/setup: one security finding packet plus no-finding packets from other specialists.
- Steps: Run aggregation fixture validation.
- Expected result: Verified material evidence can promote to a canonical material finding without consensus.
- Failure proves: subagent consensus incorrectly suppresses specialist-only material defects.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`
- Required by milestone: M2

### T10. Duplicate findings are deduplicated before canonical recording

- Covers: R10a-R10d, EC7, AC9
- Level: unit
- Command IDs: CMD2
- Fixture/setup: overlapping subagent finding packets.
- Steps: Run aggregation fixture validation.
- Expected result: One canonical material finding remains with preserved evidence.
- Failure proves: canonical review can flood duplicate findings.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`
- Required by milestone: M2

### T11. Material conflicts record final aggregation decision

- Covers: R10c-R10e, R11, E7, AC12
- Level: integration
- Command IDs: CMD2, CMD3
- Fixture/setup: conflicting packets where one specialist finds a generated-output risk and another reports no findings.
- Steps: Validate conflict, inspected evidence, final decision, and reason fields.
- Expected result: Material conflicts are resolved by evidence and recorded.
- Failure proves: conflicts can disappear or be decided by vote count.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`; `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review`
- Required by milestone: M2

### T12. Low-evidence suggestions are not promoted

- Covers: R9c, E4, EC9, AC11
- Level: unit
- Command IDs: CMD2
- Fixture/setup: low-confidence style suggestion without material evidence.
- Steps: Run aggregation fixture validation.
- Expected result: Suggestion is rejected or downgraded and is not a canonical material finding.
- Failure proves: noisy comments can block lifecycle closeout.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`
- Required by milestone: M2

### T13. Existing lifecycle gates stay unchanged

- Covers: R13, AC13, AC16
- Level: contract
- Command IDs: CMD1, CMD7
- Fixture/setup: `skills/code-review/SKILL.md`, workflow guidance when touched, and lifecycle artifacts.
- Steps: Confirm material findings still require evidence, required outcome, safe resolution or needs-decision rationale, and review-resolution routing.
- Expected result: Subagent output does not claim verify or PR readiness and does not bypass review-resolution.
- Failure proves: subagent-assisted mode weakens existing lifecycle gates.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/validate-skills.py skills/code-review/SKILL.md`; artifact lifecycle validation
- Required by milestone: M1, M3

### T14. External advisory output does not replace canonical review

- Covers: R14, E6, EC10, AC14
- Level: integration
- Command IDs: CMD2
- Fixture/setup: advisory Codex or GitHub review summary fixture.
- Steps: Validate imported source, scope, limitations, promoted findings, and rejected comments.
- Expected result: Advisory output can inform aggregation but never replaces canonical review status.
- Failure proves: external comments can become lifecycle authority.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/test-skill-validator.py -k subagent_code_review`
- Required by milestone: M2

### T15. First-slice deferred boundaries are preserved

- Covers: R15-R17, EC11, EC12, AC15
- Level: manual
- Command IDs: CMD1, CMD4, CMD5, CMD6
- Fixture/setup: implementation diff, generated output proof, adapter proof.
- Steps: Confirm no required Claude config packaging, no persistent packet files, no parallel execution requirement, and no generated-output hand edits.
- Expected result: Deferred work remains outside first implementation.
- Failure proves: the first slice silently expands scope.
- Evidence artifact: behavior-preservation evidence when created; `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: manual review plus generated-output checks
- Required by milestone: M1, M3

### T16. Generated skill and adapter proof stays source-derived

- Covers: R18, AC12-AC16
- Level: smoke
- Command IDs: CMD4, CMD5, CMD6
- Fixture/setup: canonical `skills/code-review` source and generated build outputs.
- Steps: Run generated-skill and adapter packaging tests named by the milestone.
- Expected result: Updated code-review skill and assets are generated or packaged through repository-owned scripts with no hand edits.
- Failure proves: public adapter output can drift from canonical source.
- Evidence artifact: `docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml`
- Automation location: `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`
- Required by milestone: M3

## Fixtures and data

- Positive and negative subagent role fixtures.
- Positive and negative `subagent-review-packet-v1` fixtures.
- Changed-surface selection fixtures.
- Review-record coverage fixtures.
- Aggregation fixtures for duplicate findings, conflicts, no-consensus material finding promotion, and low-evidence suggestion downgrade.
- Advisory import fixture for Codex or GitHub review summaries.

## Mocking/stubbing policy

Use fixture packets and review-record snippets rather than live subagent execution.
Do not require external network, live GitHub review, Claude runtime, Codex runtime, publication, or secret access for test proof.

## Migration or compatibility tests

Existing direct code-review records and direct review without subagents remain valid.
No historical review records are migrated solely to add subagent coverage.

## Observability verification

Review-record fixtures must expose selected specialists, changed-surface triggers, omitted specialists and rationale when relevant, packet status, accepted findings, rejected or downgraded comments when relevant, limitations, and material conflict decisions.

Validator diagnostics should name unknown roles, unknown statuses, malformed packets, missing required coverage, duplicate finding collapse, and malformed coverage rows.

## Security/privacy verification

Verify read-only defaults, secret exclusion, no network/publication by default, no generated-output mutation by subagents, and no external advisory output replacing canonical lifecycle review.

## Performance checks

Verify the default selection model can cap specialist count and record omitted or folded coverage rationale.
No runtime performance benchmark is required in the first slice because parallel execution and live subagent orchestration are out of scope.

## Manual QA checklist

MQA1. Confirm first-slice boundaries remain intact: no required persistent packet files, no mandatory Claude configs, no mandatory Codex review, no parallel execution, no auto-fix behavior, and no generated-output hand edits.

## What not to test and why

- Do not test live Claude custom subagent configs; they are optional and not required in the first slice.
- Do not test live Codex GitHub review execution; Codex output is advisory and optional.
- Do not test background asynchronous review; it is out of scope.
- Do not test parallel subagent execution; it is deferred.
- Do not test auto-fixes; code-review remains a judging stage.
- Do not test persistent packet file retention; separate packet files are deferred.

## Uncovered gaps

None.

Any implementation expansion into persistent packet files, reusable orchestration, target-native config generation, new dependencies, or external review-service integration must return to proposal, spec, or architecture before implementation.

## Next artifacts

- `test-spec-review`
- Implementation milestones M1-M3 after clean test-spec-review
- `code-review` for each implementation milestone
- `explain-change`
- `verify`
- `pr`

## Follow-on artifacts

- Test-spec review R1: `docs/changes/2026-07-06-subagent-assisted-code-review/reviews/test-spec-review-r1.md`
- Review log: `docs/changes/2026-07-06-subagent-assisted-code-review/review-log.md`

## Readiness

Active proof surface.
Implementation handoff is allowed by `test-spec-review-r1`, but workflow auto stopped at the requested `test-spec-review` target.
