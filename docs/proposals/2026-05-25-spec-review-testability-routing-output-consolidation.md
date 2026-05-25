# Spec-Review Testability Routing and Output Consolidation

## Status

accepted

## Problem

The `spec-review` skill currently mixes two different `test-spec` concepts in a way that is easy to misread:

| Concept | Current role | Problem |
|---|---|---|
| `test-spec` as an immediate routing target | A guard says not to name `test-spec` as the immediate next stage while `architecture` or `plan` remains. | The guard is prose-only, so reviewers can still violate it. |
| Eventual `test-spec` readiness as a quality assessment | The review must state whether an approved spec is eventually ready for test-spec authoring. | The assessment is load-bearing, but it is interwoven with routing language. |

The right optimization is not to remove `test-spec` from `spec-review`. The routing guard protects against a real misrouting failure, while eventual `test-spec` readiness is the spec-review gate's substantive output: it certifies whether the reviewed spec is precise enough for tests to follow without guessing.

The current skill includes both rules. It says not to report `approved` without explicit eventual `test-spec` readiness of `ready` or `conditionally-ready`, and it separately says not to name `test-spec` as the immediate next stage while `architecture` or `plan` remains. The problem is that these rules are scattered prose reminders instead of a structural output contract:

```text
Immediate next stage: closed routing enum that excludes test-spec.
Eventual test-spec readiness: separate assessment enum.
```

There is also a smaller drift surface: the skill states material-finding field obligations in more than one place, even though its resource map already points to `assets/material-finding.md` as the copied structure for material findings.

## Goals

- Make `spec-review` less confusing about `test-spec`.
- Preserve eventual `test-spec` readiness as a required quality assessment.
- Make the immediate-next-stage field structurally unable to hold `test-spec`.
- Consolidate scattered `test-spec` wording into one routing contract and one readiness contract.
- Keep the `spec-review` gate's purpose intact: make the spec precise enough for tests, architecture, and implementation to follow without guessing.
- De-duplicate material-finding field wording so the asset owns the detailed field shape.
- Preserve review recording behavior, review status values, finding severity values, material-finding sufficiency, and formal lifecycle review recording.
- Add validation or fixture coverage so the previous routing failure cannot recur.

## Non-goals

- Do not remove eventual `test-spec` readiness.
- Do not allow `test-spec` as an immediate next stage from `spec-review`.
- Do not change spec-review's review dimensions.
- Do not change review status values.
- Do not change finding severity values.
- Do not change formal lifecycle recording requirements.
- Do not change `assets/material-finding.md` field shape unless a separate asset-change review requires it.
- Do not change the `spec`, `test-spec`, `plan`, or `workflow` skills in this first slice unless validation proves a direct drift dependency.
- Do not introduce new downstream auto-handoff behavior.
- Do not claim architecture completion, plan completion, test-spec completion, implementation readiness, verification, branch readiness, or PR readiness.

## Vision fit

fits the current vision

RigorLoop depends on review gates that are understandable, testable, and hard to misuse. This proposal strengthens the `spec-review` gate by separating routing from testability assessment:

```text
routing says what should happen next;
readiness says whether the spec is eventually testable.
```

The proposal is falsified if:

- `spec-review` can still output `Immediate next stage: test-spec`.
- `approved` no longer requires a `ready` or `conditionally-ready` testability assessment.
- Reviewers cannot tell the difference between routing and readiness.
- Material-finding fields drift because the same field list remains duplicated in multiple places.
- Generated public skill output diverges from canonical `skills/spec-review/`.

## Context

The current `spec-review` skill describes itself as an independent contract reviewer whose job is to make the spec precise enough that tests, architecture, and implementation can follow without guessing. That makes eventual testability central to the skill's purpose, not optional decoration.

The current skill also has a resource map that tells the model to copy `assets/review-result-skeleton.md` for the review result and `assets/material-finding.md` for each material finding, including a requirement to confirm the literal `Finding ID:` line before linking the finding from review logs or resolutions.

The proposed change keeps those responsibilities but makes the output contract easier to validate. The immediate next-stage field becomes routing-only, and the eventual test-spec readiness field becomes assessment-only.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Reduce confusing `test-spec` mentions | in scope | Goals, Recommended Direction |
| Preserve useful testability assessment | in scope | Goals, Expected Behavior Changes |
| Prevent misrouting to `test-spec` | in scope | Goals, Recommended Direction, Testing and Verification Strategy |
| Preserve spec-review gate substance | in scope | Goals, Non-goals, Vision fit |
| Remove redundant material-finding field duplication | in scope | Goals, Recommended Direction |
| Avoid behavior drift | in scope | Non-goals, Expected Behavior Changes, Testing and Verification Strategy |
| Avoid broad skill-family rewrite | out of scope | Non-goals, Scope Budget |
| Avoid downstream auto-handoff | in scope | Non-goals, Expected Behavior Changes |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| `skills/spec-review/SKILL.md` routing and readiness wording | core to this proposal | This is the source of the confusing contract. |
| `skills/spec-review/assets/review-result-skeleton.md` fields | core to this proposal | The result skeleton should expose the structural contract reviewers must output. |
| Material-finding wording de-duplication in `SKILL.md` | core to this proposal | The proposal reduces drift by letting the asset own the detailed field shape. |
| Validator or fixture coverage for invalid immediate next stage | first-slice candidate | Validation makes the previous routing failure hard to reintroduce. |
| Generated adapter validation or rebuild checks | same-slice dependency | Generated public output must stay consistent with authored skill source. |
| Recorded review-artifact validation for result fields | deferable follow-up | It may require broader parser support and is not needed to fix the skill contract first. |
| Similar routing/readiness separation in other review-family skills | separate proposal | This proposal is intentionally scoped to `spec-review`. |
| Workflow stage-order or auto-handoff changes | out of scope | The change clarifies a review result, not downstream automation. |

## Options Considered

### Option 1: Remove all `test-spec` mentions from `spec-review`

This simplifies wording and eliminates one source of confusion, but it removes the gate's testability assessment, reopens the documented misrouting failure, and makes `approved` weaker because approval would no longer certify downstream testability.

Rejected.

### Option 2: Keep current wording unchanged

This avoids implementation risk and preserves both existing concepts, but routing and readiness remain interwoven. The routing prohibition remains prose-only, reviewers can still put `test-spec` into the wrong field, and material-finding field obligations remain duplicated.

Rejected.

### Option 3: Add another warning not to route to `test-spec`

This is small and keeps the current shape, but it adds another prose reminder without structurally preventing the error. It would make the skill longer and more repetitive.

Rejected.

### Option 4: Split routing and readiness into closed output fields

This preserves eventual test-spec readiness, makes `test-spec` structurally invalid as an immediate next stage, reduces confusing overlap, converts a reminder into an output contract, and supports validator or fixture coverage.

Recommended.

## Recommended Direction

Choose Option 4.

Revise `spec-review` so it has two separate concepts:

```text
Immediate next stage:
  routing field
  closed enum
  excludes test-spec

Eventual test-spec readiness:
  quality assessment field
  closed enum
  required for approved outcomes
```

The central rule is:

```text
`test-spec` is never an immediate next stage from `spec-review`.

`spec-review` may say the spec is eventually ready for test-spec authoring, but
it does not route directly into test-spec.
```

The first-slice immediate next-stage enum should be:

```text
spec revision
review-resolution
architecture
plan
none
```

Document the enum by value kind so a single routing field can carry backward, conditional, forward, and halt outcomes without implying they are the same kind of stage:

| Kind | Values | Meaning |
|---|---|---|
| Backward rework | `spec revision` | The spec needs authoring changes before downstream reliance. |
| Conditional review closeout | `review-resolution` | Material findings or blocking outcomes need disposition before downstream reliance. |
| Forward repository stage | `architecture`, `plan` | The reviewed spec can move to the next repository stage, subject to normal stage-order rules. |
| Halt or isolated outcome | `none` | The review is inconclusive, isolated, blocked by missing inputs, or makes no repository-stage handoff claim. |

Bind the routing field to review status so the new field cannot contradict the existing result:

| Review status | Allowed immediate next stage |
|---|---|
| `approved` | `architecture` or `plan` |
| `changes-requested` | `spec revision` or `review-resolution` |
| `blocked` | `review-resolution` or `none` |
| `inconclusive` | `none` |

If a status-to-routing pair does not fit these bindings, the review result is internally inconsistent and should be corrected before downstream handoff.

The first-slice eventual test-spec readiness enum should be:

```text
ready
conditionally-ready
not-ready
```

Do not add a `not-assessed` readiness value. A review that cannot assess testability should use `Review status: inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and an explicit stop condition.

Use `Stop condition` and `Eventual test-spec readiness` instead of pseudo-routing values such as `blocker handling`, `missing-context resolution`, `test-spec`, or `ready for test-spec`.

Keep the material-finding sufficiency rule in `SKILL.md`: a material finding is incomplete if it lacks evidence, required outcome, and either a safe resolution path or a `needs-decision` rationale. Keep `assets/material-finding.md` as the detailed field-shape owner, and replace the duplicate full field list in `Isolation and Recording` with a short reference to the asset.

## Expected Behavior Changes

- `spec-review` output cannot validly name `test-spec` as immediate next stage.
- `spec-review` still reports whether the spec is eventually test-spec-ready.
- `approved` still requires `ready` or `conditionally-ready`.
- `conditionally-ready` names the condition that must be satisfied.
- Missing required inputs map to `inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and a stop condition.
- The skill becomes shorter and less repetitive around `test-spec`.
- The material-finding field shape has one structural owner: `assets/material-finding.md`.
- Formal lifecycle recording behavior remains unchanged.
- No downstream stage is auto-started by this skill.

## Architecture Impact

| Surface | Impact |
|---|---|
| `skills/spec-review/SKILL.md` | Add a consolidated routing/readiness section and remove scattered duplicate wording. |
| `skills/spec-review/assets/review-result-skeleton.md` | Make the immediate-stage enum and eventual readiness enum explicit. |
| `skills/spec-review/assets/material-finding.md` | No intended change unless parity review finds missing field labels. |
| `scripts/skill_validation.py` | Add or update checks for enum separation and no duplicate material-finding field list if feasible. |
| `scripts/test-skill-validator.py` | Add positive and negative fixtures for routing/readiness separation when existing validation supports it. |
| Generated adapters | Rebuild or validate generated output from canonical skills if adapter output is tracked or checked. |
| Review-artifact validator | Possible follow-up enforcement for actual review records if current parser can inspect result fields. |
| Other skills | No direct change in the first slice. |

## Testing and Verification Strategy

| Check ID | What is verified |
|---|---|
| `SRTO-001` | `spec-review` defines `Immediate next stage` as a closed enum excluding `test-spec`. |
| `SRTO-002` | `spec-review` defines `Eventual test-spec readiness` as a separate closed enum. |
| `SRTO-003` | `review-result-skeleton.md` contains both fields and does not allow `test-spec` in immediate next stage. |
| `SRTO-004` | A fixture with `Immediate next stage: test-spec` fails validation. |
| `SRTO-005` | A fixture with `Eventual test-spec readiness: ready` and `Immediate next stage: plan` passes. |
| `SRTO-006` | `Review status: approved` with `Eventual test-spec readiness: not-ready` fails validation. |
| `SRTO-007` | Missing inputs produce `inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and a stop condition. |
| `SRTO-008` | Material-finding field obligations have structural single ownership: the complete field-label set appears in `assets/material-finding.md`, while `SKILL.md` may reference the fields but does not re-enumerate the full labeled set. |
| `SRTO-009` | `assets/material-finding.md` still contains the required material-finding structure. |
| `SRTO-010` | Generated adapter output includes the updated `spec-review` skill and assets. |
| `SRTO-011` | Review dimensions, severity values, recording statuses, and review statuses remain unchanged. |
| `SRTO-012` | Review status and `Immediate next stage` combinations follow the accepted status-to-routing binding. |

Suggested validation commands for the implementation plan:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py skills/spec-review/SKILL.md
python scripts/validate-skills.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --check
python scripts/validate-adapters.py --version <version>
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path skills/spec-review/SKILL.md \
  --path skills/spec-review/assets/review-result-skeleton.md \
  --path skills/spec-review/assets/material-finding.md \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/plans/<plan>.md \
  --path docs/plan.md
git diff --check --
```

Use repository-owned exact adapter commands in the plan if they differ.

## Rollout and Rollback

Rollout:

1. Approve this proposal.
2. Write or amend relevant skill-contract or test-spec coverage for `spec-review` routing/readiness output if needed.
3. Update `skills/spec-review/SKILL.md`.
4. Update `skills/spec-review/assets/review-result-skeleton.md`.
5. Keep `assets/material-finding.md` unchanged unless parity review finds a structural defect.
6. Add validator or test fixtures for the immediate-stage enum and readiness enum.
7. Rebuild or validate generated skills/adapters from canonical source.
8. Record behavior-preservation evidence.
9. Run code review and verify.

Rollback:

- Restore prior `spec-review` wording if the new enum separation causes ambiguity.
- Keep any validator tests that catch `Immediate next stage: test-spec` if the output contract remains valid.
- Do not change material-finding asset shape during rollback unless the rollback also restores the duplicated field list.
- Do not alter historical review records.
- Do not change downstream workflow stage order.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Removing `test-spec` from immediate routing is misread as removing testability assessment. | Keep a distinct `Eventual test-spec readiness` field and explain its purpose. |
| Closed enum is too narrow for real spec-review outcomes. | Include `spec revision`, `review-resolution`, `architecture`, `plan`, and `none`; use stop condition for blocker detail. |
| `conditionally-ready` becomes vague. | Require a named condition. |
| Material-finding de-duplication removes useful guidance. | Keep the sufficiency rule in `SKILL.md`; let the asset own field structure. |
| Validator overfits prose wording. | Prefer checking skeleton fields, enum values, status-to-routing bindings, and structural single ownership over exact paragraph text. |
| Generated adapters drift. | Validate generated output from canonical `skills/`. |

## Open Questions

- Should `Immediate next stage` include both `spec revision` and `review-resolution`, or should `review-resolution` be represented only as a stop condition?
  Answer: include both, because review-resolution is a concrete lifecycle stage when material findings require disposition. Bind allowed routing values to review status so `review-resolution` remains a proper routing target without letting the routing field contradict the review result.
- Should `Eventual test-spec readiness` add a fourth value, `not-assessed`?
  Answer: no. Use `not-ready` when the review cannot certify testability. A review that did not assess testability should be `inconclusive`, not approved with a separate escape-hatch readiness value.
- Should validator enforcement apply only to the `spec-review` skill skeleton, or also to recorded review artifacts?
  Answer: enforce the skill skeleton first. Recorded-artifact validation is a follow-up when the review-artifact parser gains result-field inspection.
- Should the material-finding de-duplication be mechanically enforced?
  Answer: yes, when feasible, with a targeted structural check. The check should verify that the complete material-finding field-label set has one authored owner, not that prose paragraphs are textually identical.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-25 | Keep eventual test-spec readiness. | It is the quality assessment that makes spec-review approval meaningful. | Remove all test-spec mentions. |
| 2026-05-25 | Exclude `test-spec` from immediate next stage. | Spec-review should not route directly into test-spec; it should assess eventual readiness separately. | Prose warning only. |
| 2026-05-25 | Consolidate scattered test-spec wording. | Current wording mixes routing and assessment. | Add more reminders. |
| 2026-05-25 | De-duplicate material-finding field lists. | The asset owns the shape; duplication creates drift risk. | Keep two prose field lists. |
| 2026-05-25 | Keep changes scoped to `spec-review`. | The issue is localized to this skill and its assets. | Broader review-family rewrite. |
| 2026-05-25 | Bind immediate routing to review status. | Proposal review identified that routing and status can otherwise contradict each other. | Leave routing and status independent. |
| 2026-05-25 | Reject `not-assessed` as a readiness value. | It would weaken the spec-review gate by letting a review decline testability assessment. | Add a fourth readiness value. |

## Next Artifacts

```text
proposal-review
spec or test-spec amendment only if current skill-contract coverage is insufficient
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Recommended route:

```text
proposal-review -> plan -> plan-review -> implementation -> code-review -> verify -> pr
```

Use a spec or test-spec amendment only if the current skill-contract tests do not already cover review-result skeleton field enums and material-finding asset ownership.

## Follow-on Artifacts

Proposal review outcome: approved with observations on 2026-05-25. No material findings were raised. Observations were incorporated into this accepted proposal by documenting routing value kinds, binding routing to review status, rejecting `not-assessed`, naming the parser trigger for recorded-artifact validation, and defining material-finding de-duplication as structural single ownership.

None yet for downstream artifacts.

Candidate follow-ons after this proposal is settled:

- Proposal for the same routing/readiness separation in other review-family skills if a similar pattern exists.
- Proposal for recorded review-artifact validation of immediate next-stage enums.
- Proposal for review-family shared result-skeleton conventions if duplication persists.
- Proposal for build-time partials if common review wording continues to drift.

## Readiness

Proposal review is complete. This proposal is accepted and ready for `plan`; spec or test-spec amendment remains conditional on the plan's coverage check.

Core invariant:

```text
Do not remove testability from spec-review.

Separate it.

`Immediate next stage` is routing and must never be `test-spec`.
`Eventual test-spec readiness` is the review's testability assessment and must
remain present, especially for approved reviews.

Make the wrong routing value structurally impossible instead of relying on a
prose reminder.
```
