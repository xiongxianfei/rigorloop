# Cost-Bounded Rigor M3 Validation-Budget Guidance

## Status

approved

## Related proposal

- [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md)

## Goal and context

This spec defines the third cost-bounded-rigor implementation slice after PR #54 completed M1 and PR #55 completed M2.

M1 added scope-budget guidance, proposal-review checks, and the full bounded-evidence rule in `docs/workflows.md`. M2 added selected skill reminders without changing validation behavior.

M3 defines validation-budget behavior: stages should validate the smallest sufficient surface that proves the current change, while preserving mandatory broad-smoke, release, review-resolution, test-spec, plan, and selector triggers.

This slice is intentionally not lifecycle token-cost reporting, release packaging work, adapter packaging work, dynamic benchmark work, or progressive-loading restructuring.

## Glossary

- validation budget: guidance that selects the smallest sufficient validation set for a change without weakening correctness, lifecycle, review, release, or safety gates.
- targeted validation: selector-selected or explicitly scoped validation over known changed paths, affected artifacts, stable check IDs, and governing lifecycle surfaces.
- broad smoke: repository-wide validation selected by an authoritative trigger, such as `main` mode, `release` mode, explicit `--broad-smoke`, active plan field, test-spec requirement, review-resolution requirement, or release metadata.
- validation owner surface: the artifact or code surface that owns validation guidance or executable behavior.
- selector behavior: executable check-selection behavior in validation selection scripts and wrapper tests.
- skill-local reminder: short stage guidance in a public skill that points the stage toward targeted validation without duplicating the full workflow guide.

## Examples first

### Example E1: proposal-only or spec-only change uses targeted validation

Given a change only adds or revises a draft proposal or draft spec
When the changed paths are known
Then validation starts with selector-selected or explicit-path lifecycle and metadata checks
And broad release validation is not required unless an authoritative broad-smoke or release trigger exists.

### Example E2: skill wording change validates canonical skills

Given a change edits canonical skill wording under `skills/`
When validation is selected
Then the required proof includes canonical skill validation, skill regression proof, generated local mirror drift checks, and affected lifecycle checks
And release packaging validation is not required solely because a skill file changed.

### Example E3: review-resolution trigger can require broader proof

Given a material review finding requires broad smoke as part of its accepted disposition
When verify evaluates branch readiness
Then broad smoke is required even if the changed paths otherwise have a targeted validation set.

### Example E4: release metadata triggers release validation

Given a change touches release metadata or uses release validation mode
When validation is selected
Then release-specific validation and broad-smoke requirements apply according to release metadata and selector behavior
And ordinary targeted validation guidance does not override release gates.

### Example E5: selector behavior change needs executable proof

Given M3 implementation changes validation-selection script behavior
When the change is implemented
Then the matching test spec must require selector regression coverage for the changed behavior
And review must reject skill-only proof as insufficient.

### Example E6: guidance-only change does not require selector behavior changes

Given M3 implementation only clarifies `docs/workflows.md` guidance and skill-local reminders
When validation runs
Then skill or artifact static proof may be sufficient
And selector behavior remains unchanged with recorded rationale.

## Requirements

R1. M3 MUST define validation-budget guidance for selecting targeted validation before broad smoke when changed paths are known and no authoritative broad-smoke trigger applies.

R2. M3 MUST preserve all existing mandatory validation semantics, including lifecycle validation, review-artifact validation, change-metadata validation, generated-output drift checks, release validation, adapter validation, token-cost report validation, and broad-smoke triggers.

R3. M3 MUST keep broad smoke trigger-driven rather than routine for every non-trivial PR.

R4. M3 MUST define the authoritative broad-smoke trigger set as including selector mode `main`, selector mode `release`, explicit `--broad-smoke`, active plan field `broad_smoke_required: true`, test-spec requirement, review-resolution requirement, and release metadata.

R5. M3 MUST distinguish validation owner surfaces:

- `docs/workflows.md` owns contributor-facing operational guidance;
- validation-selection scripts and selector tests own executable check-selection behavior;
- stage skills own only concise local reminders when a stage directly needs them;
- active plans and test specs own change-specific validation requirements;
- review-resolution owns finding-specific validation requirements;
- release metadata owns release-specific validation requirements.

R6. M3 MUST NOT move executable selector behavior into skill prose or make skill prose the source of truth for selected checks.

R7. M3 MUST NOT let guidance-only wording change selected check coverage, command exit behavior, failure detection, or required validation evidence.

R8. If implementation changes selector behavior, the test spec MUST require selector regression tests that prove the new or changed check-selection behavior.

R9. If implementation only changes wording in `docs/workflows.md` or selected skills, the test spec MAY use static proof and manual review evidence instead of selector behavior tests.

R10. M3 MUST require implementations to record whether selector behavior is changed, unchanged with rationale, or deferred to a later selector slice.

R11. M3 MUST require any selected skill wording to be concise, local to that stage, and subordinate to `docs/workflows.md` for the full validation-budget rule.

R12. M3 MUST NOT require edits to every stage skill.

R13. M3 MUST NOT edit `implement`, `code-review`, or `verify` unless a later approved plan identifies a specific stage-local validation-budget gap in those skills.

R14. M3 MUST preserve full review-resolution and material-finding closeout requirements.

R15. M3 MUST preserve release validation and adapter packaging boundaries, including the single-authored skill source model.

R16. M3 MUST NOT add lifecycle token-cost summary artifacts, dynamic benchmark requirements, hard token gates, release packaging changes, or full progressive-loading restructuring.

R17. M3 MUST keep validation guidance compatible with dirty worktrees by preferring explicit paths, diff-derived modes, or wrapper-selected checks over local whole-repository lifecycle validation when unrelated local changes exist.

R18. M3 MUST require final verify to check that actual validation evidence matches the accepted plan, test spec, review-resolution, and release metadata triggers.

R19. M3 MUST define no-change rationale as acceptable when existing `docs/workflows.md`, selector behavior, or stage skills already satisfy the M3 contract.

## Inputs and outputs

Inputs:

- accepted cost-bounded-rigor proposal;
- M1 and M2 specs and plans;
- current `docs/workflows.md` validation guidance;
- current validation selector and CI wrapper behavior;
- current stage skills that mention validation selection;
- active plan, test-spec, review-resolution, and release metadata conventions.

Outputs:

- focused M3 spec;
- later M3 plan and test spec;
- implementation evidence for affected owner surfaces;
- selected validation and lifecycle validation results;
- no-change rationale for owner surfaces that already satisfy the contract.

## State and invariants

1. Targeted validation remains the default first layer when changed paths are known.
2. Broad smoke remains mandatory when an authoritative trigger requires it.
3. `docs/workflows.md` remains the contributor-facing validation-budget guide.
4. Validation-selection scripts remain the executable source for selected check behavior.
5. Stage skills do not duplicate the full validation-budget rule.
6. Review-resolution, release metadata, active plans, and test specs may require stronger validation than path-based targeting alone.

## Error and boundary behavior

1. If selector output conflicts with the accepted plan, test spec, review-resolution, or release metadata, implementation or verify must stop and report the conflict instead of silently choosing the smaller validation set.
2. If a changed path is unclassified by selector behavior, the change must either add narrow selector coverage or route the path-specific gap to a later accepted selector slice before relying on selected validation.
3. If broad smoke is required but cannot run, verify must block unless the governing artifact explicitly allows a temporary state with rationale, owner, and follow-up.
4. If a stage skill claims validation behavior that differs from `docs/workflows.md` or selector behavior, review must request correction or owner-surface clarification.
5. If implementation discovers that M3 requires release behavior, adapter packaging, dynamic benchmarks, lifecycle token-cost summaries, or progressive-loading restructuring, it must stop and route that work to the appropriate later slice or proposal.

## Compatibility and migration

- Existing selector behavior remains valid unless the M3 plan identifies a focused selector gap.
- Existing broad-smoke triggers remain valid.
- Existing release and adapter validation behavior remains valid.
- Existing stage skills remain valid unless they contradict this M3 contract.
- Rollback for guidance-only implementation is to remove the unnecessary wording while preserving existing selector behavior and mandatory validation rules.

## Observability

M3 implementation evidence should record:

- changed owner surfaces;
- selected check IDs and commands run;
- whether selector behavior changed;
- whether broad smoke was required and why;
- no-change rationale for unaffected owner surfaces;
- any validation conflicts between selector output and governing artifacts.

## Security and privacy

M3 does not introduce new secrets, credentials, external services, or data exposure. It must preserve security-sensitive validation gates, release gates, material-review closeout, and generated-output validation.

## Accessibility and UX

No UI is involved.

## Performance expectations

M3 should reduce unnecessary validation work by preferring targeted checks when sufficient, but it must not set hard runtime thresholds or skip required checks to meet a speed target.

## Edge cases

1. A plan sets `broad_smoke_required: true` for a docs-only change. Broad smoke is required because the plan is authoritative for that change.
2. A test spec requires broad smoke for a selector change. Broad smoke is required even if changed paths are narrowly classified.
3. A review-resolution accepted disposition requires broad smoke after a finding. Verify blocks without broad-smoke evidence.
4. A release metadata file changes. Release validation applies even if other touched paths look docs-only.
5. A selected-check command passes, but selector output omitted a changed unclassified path. The gap blocks readiness until classified or explicitly routed.
6. A guidance-only change attempts to alter `scripts/validation_selection.py`. Review must require the M3 plan and test spec to cover selector behavior.
7. A stage skill adds a long copied validation checklist. Review must request moving the full rule to `docs/workflows.md` or existing owner surfaces.
8. A dirty worktree contains unrelated drafts. Validation should use explicit paths or diff-derived wrapper modes rather than local whole-repository lifecycle validation.
9. A contributor runs no-argument `bash scripts/ci.sh`. It remains legacy broad smoke and must not be represented as the normal first validation layer.
10. A change touches generated adapter release output. M3 guidance does not bypass adapter or release evidence rules.

## Non-goals

- Do not implement lifecycle token-cost summaries.
- Do not add hard token gates.
- Do not change release validation or adapter packaging.
- Do not reintroduce tracked generated public adapter skill bodies.
- Do not require dynamic benchmark comparison.
- Do not implement progressive-loading follow-through.
- Do not rewrite every stage skill.
- Do not weaken formal review, review-resolution, verify, PR, material-finding, release, or generated-output rules.
- Do not make validators infer semantic validation sufficiency from skill prose.

## Acceptance criteria

- `docs/workflows.md` or an approved no-change rationale identifies targeted validation as the first layer and broad smoke as trigger-driven.
- M3 records the ownership split between workflow guidance, selector behavior, skill-local reminders, plans, test specs, review-resolution, and release metadata.
- Any selector behavior changes have selector regression coverage.
- Guidance-only implementation does not change selected check coverage or command semantics.
- Broad-smoke triggers remain intact.
- Review-resolution, release validation, adapter validation, and generated-output rules remain intact.
- Any selected skill changes are concise and do not duplicate the full validation-budget rule.
- The implementation records no-change rationale for owner surfaces that already satisfy the M3 contract.

## Open questions

None.

## Next artifacts

```text
spec-review
plan
plan-review
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- [Spec Review R1](../docs/changes/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance/reviews/spec-review-r1.md)
- [Execution Plan](../docs/plans/2026-05-14-cost-bounded-rigor-m3-validation-budget-guidance.md)

## Readiness

Approved after clean spec-review. Ready for plan-review of the focused M3 execution plan; not ready for test-spec or implementation until plan-review approves the plan state.
