# Behavior Preservation: Spec-Review Testability Routing and Output Consolidation

## Scope

This evidence covers M2 canonical skill and asset changes plus M3 generated-output proof for the spec-review routing/readiness contract.

## Preservation Matrix

| Surface | Baseline | New proof | Preservation result |
| --- | --- | --- | --- |
| Approved spec-review | Approval required eventual readiness, but the rule was scattered in prose. | `skills/spec-review/SKILL.md` now says `Review status: approved` requires `Eventual test-spec readiness` of `ready` or `conditionally-ready`; validator fixtures reject approved/not-ready. | preserved |
| Routing | Prose warned not to name `test-spec` while architecture or plan remained. | `Immediate next stage` is a closed enum in the skill and result skeleton: `spec revision`, `review-resolution`, `architecture`, `plan`, `none`; validator rejects `test-spec`. | strengthened |
| Readiness | Readiness wording existed separately from the immediate-stage warning but was interwoven. | `Eventual test-spec readiness` is a separate closed enum: `ready`, `conditionally-ready`, `not-ready`. | clarified |
| Status-to-routing binding | Prior wording did not structurally prevent approved/backward-route contradictions. | Validator fixtures reject approved with `spec revision`, `review-resolution`, or `none`, and reject non-approved outcomes with forward routing where structurally inspectable. | strengthened |
| Missing input behavior | Prior wording could imply an empty immediate-stage field. | Skill, workflow spec, and fixtures use `Review status: inconclusive`, `Immediate next stage: none`, `Eventual test-spec readiness: not-ready`, and a stop condition. | clarified |
| Material findings | Field shape was repeated in skill prose and asset. | `assets/material-finding.md` remains unchanged as the structural field owner; `SKILL.md` keeps the sufficiency rule and references the asset for field blocks. | de-duplicated |
| Recording | Formal review recording was required for lifecycle reviews. | Recording status values, review record/log/resolution behavior, and material-finding recording obligations remain in `SKILL.md`. | preserved |
| Review status values | `approved`, `changes-requested`, `blocked`, `inconclusive`. | Result skeleton and validator preserve the same values. | preserved |
| Finding severity values | `blocking`, `major`, `minor`. | Skill severity enum unchanged. | preserved |
| Workflow order | `plan-review` remains the normal immediate handoff into `test-spec`. | `plan-review` still exposes `Immediate next stage: <test-spec | plan revision | blocked>`; workflow spec preserves plan-review-to-test-spec handoff while clarifying spec-review routing. | preserved |
| Autoprogression | Direct and review-only spec-review requests remained isolated. | Skill still says no auto-continue into `architecture`, `plan`, or `test-spec`. | preserved |
| Adjacent test-spec gating | Test-spec authoring stopped on upstream spec-review readiness failure. | `test-spec` now stops on `not-ready` only; `not-assessed` is removed because it is no longer a valid readiness value. | aligned |
| Generated adapters | Previous generated output came from canonical skill source. | M3 built temporary `v0.1.5` Codex, Claude, and opencode adapter archives from canonical `skills/`, validated the archives, and inspected each archive's generated `spec-review` skill body and result skeleton for the updated routing/readiness contract. | current |

## Manual Contract Checks

- Review dimensions are unchanged.
- Review status values are unchanged.
- Finding severity values are unchanged.
- Recording status values are unchanged.
- `skills/spec-review/assets/material-finding.md` is unchanged.
- `plan-review` did not require a behavior edit; its immediate handoff remains `test-spec`.
- `test-spec` required only the direct removal of stale `not-assessed` readiness wording.
- `specs/rigorloop-workflow.md` required a direct invariant update because it still contained the old `not-assessed` and empty immediate-stage wording.

## Validation Evidence

- `python scripts/test-skill-validator.py -k spec_review` passed.
- `python scripts/test-skill-validator.py` passed.
- `python scripts/validate-skills.py skills/spec-review/SKILL.md` passed.
- `python scripts/validate-skills.py skills/test-spec/SKILL.md` passed.
- `python scripts/validate-skills.py` passed.
- `python scripts/build-skills.py --check` passed.
- `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-srto-m3-adapters-byvYm0` passed.
- `python scripts/validate-adapters.py --root /tmp/rigorloop-srto-m3-adapters-byvYm0 --version v0.1.5` passed.
- Python `zipfile` archive content inspection passed for:
  - `rigorloop-adapter-codex-v0.1.5.zip`
  - `rigorloop-adapter-claude-v0.1.5.zip`
  - `rigorloop-adapter-opencode-v0.1.5.zip`

## M3 Generated Archive Content Proof

The archive content check inspected each generated `spec-review/SKILL.md` and `spec-review/assets/review-result-skeleton.md` for these contract markers:

- `## Routing and testability assessment`
- "Do not put `test-spec` in `Immediate next stage`."
- "Do not report `Review status: approved` unless `Eventual test-spec readiness` is `ready` or `conditionally-ready`."
- `Immediate next stage: <spec revision | review-resolution | architecture | plan | none>`
- `Eventual test-spec readiness: <ready | conditionally-ready | not-ready>`
- "`Immediate next stage` is the routing field; allowed values exclude `test-spec`."

It also checked that generated `spec-review` content did not contain an immediate-stage placeholder beginning with `test-spec` and did not contain `not-assessed`.
