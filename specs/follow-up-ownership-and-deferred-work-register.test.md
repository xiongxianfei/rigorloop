# Follow-up Ownership and Deferred Work Register Test Spec

## Status

active

## Related spec and plan

- Spec: [Follow-up Ownership and Deferred Work Register](follow-up-ownership-and-deferred-work-register.md), approved.
- Plan: [Follow-up Ownership and Deferred Work Register Plan](../docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md), active.
- Proposal: [Follow-Up Ownership and Deferred Work Register](../docs/proposals/2026-05-13-follow-up-ownership-and-deferred-work-register.md), accepted.
- Spec review: [spec-review-r1](../docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/reviews/spec-review-r1.md), approved.
- Plan review: [plan-review-r1](../docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/reviews/plan-review-r1.md), approved.
- Architecture: not required. `spec-review-r1` and `plan-review-r1` record no boundary or runtime architecture change.

## Testing strategy

This change is verified through contract, static, and validator checks rather than runtime end-to-end tests.

- Contract checks prove `docs/workflows.md` owns the follow-up ownership table and maps follow-up types to action-owning artifacts.
- Skill static checks prove `workflow` and `project-map` contain concise operational wording and do not duplicate the full ownership table.
- Absence checks prove the first implementation slice does not create an empty `docs/follow-ups.md` and does not introduce a `templates/shared/` follow-up ownership block.
- Optional register checks are specified for future use only if `docs/follow-ups.md` is created by a qualifying accepted unowned cross-change follow-up.
- Lifecycle, review-artifact, change-metadata, selector, skill, and adapter checks prove affected workflow-governance surfaces remain coherent.

Use milestone-specific validation first. Broad repository smoke is not required unless implementation changes validation routing, generated output, or another broad-smoke trigger.

## Requirement coverage map

| Requirement | Coverage |
|---|---|
| `R1`-`R1d` | `T1`, `T2`, `T12` |
| `R2`-`R2f` | `T1`, `T3`, `T12` |
| `R3`-`R3d` | `T4`, `T12` |
| `R4`-`R4d` | `T3`, `T12` |
| `R5`-`R5c` | `T5`, `T12` |
| `R6`-`R6c` | `T6`, `T11`, `T12` |
| `R7`-`R7b` | `T7`, `T8`, `T11` |
| `R8`-`R8c` | `T8`, `T11` |
| `R9`-`R9g` | `T8`, `T9`, `T11` |
| `R10`-`R10c` | `T6`, `T10`, `T12` |
| `R11`-`R11f` | `T2`, `T3`, `T4`, `T10`, `T12` |
| `R12`-`R12e` | `T8`, `T9`, `T11` |
| `R13`-`R13a` | `T12`, `T13` |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` | `T3`, `T6` |
| `E2` | `T3`, `T12` |
| `E3` | `T4`, `T6` |
| `E4` | `T4`, `T5` |
| `E5` | `T1`, `T6`, `T10` |
| `E6` | `T7`, `T8`, `T11` |
| `E7` | `T7`, `T11` |
| `E8` | `T5` |
| `E9` | `T2`, `T4`, `T10` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` | `T3`, `T6` |
| `EC2` | `T3`, `T12` |
| `EC3` | `T7`, `T8`, `T11` |
| `EC4` | `T5` |
| `EC5` | `T4`, `T6` |
| `EC6` | `T4`, `T5` |
| `EC7` | `T7`, `T8` |
| `EC8` | `T6`, `T10` |
| `EC9` | `T10` |
| `EC10` | `T9`, `T11` |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| `M1. Follow-up ownership guidance and concise skill boundaries` | `T1`, `T2`, `T3`, `T4`, `T5`, `T6`, `T10`, `T12` |
| `M2. Validation alignment and lifecycle handoff` | `T7`, `T8`, `T9`, `T11`, `T12`, `T13` |

## Test cases

### T1. Workflow guide owns follow-up ownership policy

- Covers: `R1`-`R1d`, `R2`-`R2f`, `E5`
- Level: contract, manual
- Fixture/setup: `docs/workflows.md`, approved spec
- Steps:
  - Assert `docs/workflows.md` contains a clearly labeled `Follow-up ownership` section.
  - Assert the section says follow-ups are recorded where they can be acted on.
  - Assert it maps active implementation, review finding, change closeout, release, repeated lesson, architecture risk/open question, unowned cross-change future work, and new direction/policy follow-ups to owners.
  - Assert it states `project-map` may identify risks and open questions but does not own deferred execution.
  - Assert skill text does not replace the workflow guide with a second full ownership table.
- Expected result: users and agents can find one concise follow-up ownership policy in `docs/workflows.md`.
- Failure proves: follow-up policy is missing, scattered, or duplicated into skills.
- Automation location: `scripts/test-skill-validator.py` if static checks are added; otherwise manual contract review plus `python scripts/validate-skills.py`.

### T2. Skills do not duplicate the full follow-up table

- Covers: `R1d`, `R10`-`R10c`, `R11`-`R11f`, `E9`, `EC9`
- Level: contract, static
- Fixture/setup: `skills/workflow/SKILL.md`, `skills/project-map/SKILL.md`, `templates/shared/`
- Steps:
  - Assert `skills/workflow/SKILL.md` and `skills/project-map/SKILL.md` do not copy the full `docs/workflows.md` ownership table.
  - Assert no new follow-up ownership block exists under `templates/shared/`.
  - Assert skill wording is concise and points to `docs/workflows.md` for the ownership rule.
- Expected result: policy detail stays in `docs/workflows.md`; skills remain operational and concise.
- Failure proves: the first slice created a second policy surface or premature shared abstraction.
- Automation location: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, manual diff review.

### T3. Workflow skill routes follow-ups to action-owning artifacts

- Covers: `R2`-`R2f`, `R4`-`R4d`, `R11a`, `R11b`, `E1`, `E2`, `EC1`, `EC2`
- Level: contract, static
- Fixture/setup: `skills/workflow/SKILL.md`, `docs/workflows.md`
- Steps:
  - Assert `workflow` wording says future work routes to the artifact that can act on it.
  - Assert `workflow` refers to `docs/workflows.md` for the follow-up ownership rule.
  - Assert `workflow` says deferred execution work does not belong in `project-map`.
  - Assert `workflow` does not claim to maintain a project-map backlog, create detailed plans for every follow-up, or track every minor note.
- Expected result: `workflow` routes follow-ups without replacing action-owning artifacts.
- Failure proves: workflow guidance can turn into a backlog or duplicate owner.
- Automation location: `python scripts/test-skill-validator.py`, manual review.

### T4. Project-map remains orientation, not backlog ownership

- Covers: `R3`-`R3d`, `R11c`-`R11f`, `E3`, `E4`, `E9`, `EC5`, `EC6`
- Level: contract, static
- Fixture/setup: `skills/project-map/SKILL.md`
- Steps:
  - Assert `project-map` wording says it may record risks and open questions for orientation.
  - Assert it says `project-map` does not own deferred execution or act as a backlog.
  - Assert it says actionable risks route through the workflow guide to proposal, plan, learn, review-resolution, release evidence, or `docs/follow-ups.md` when allowed.
  - Assert it does not require converting every risk/open question into a follow-up.
- Expected result: project-map keeps useful risk notes without owning execution.
- Failure proves: project-map can become a backlog or lose orientation value.
- Automation location: `python scripts/test-skill-validator.py`, manual review.

### T5. Learn follow-ups route by ownership

- Covers: `R5`-`R5c`, `E4`, `E8`, `EC4`, `EC6`
- Level: contract, manual
- Fixture/setup: `docs/workflows.md`, `skills/workflow/SKILL.md`, approved learn guidance
- Steps:
  - Assert follow-up ownership guidance preserves `learn` as repeated lesson capture, not a general backlog.
  - Assert current-change learn follow-ups route to active plans or change artifacts.
  - Assert policy, workflow, skill, architecture, or direction-setting learn follow-ups route to proposal.
  - Assert real unowned cross-change learn follow-ups may route to `docs/follow-ups.md` only with the learn session as source and register rules satisfied.
- Expected result: learn can surface follow-ups without becoming a general execution tracker.
- Failure proves: learn sessions can accumulate backlog items outside action-owning artifacts.
- Automation location: manual contract review; static checks may be added if wording changes in touched files.

### T6. First slice does not create an empty register

- Covers: `R6`-`R6c`, `R10`-`R10b`, `E1`, `E3`, `E5`, `EC1`, `EC5`, `EC8`
- Level: integration, manual
- Fixture/setup: repository tree after M1 implementation
- Steps:
  - Assert `docs/follow-ups.md` is absent unless a maintainer identified at least one qualifying accepted unowned cross-change follow-up.
  - Assert M1 validation notes or change metadata record that no qualifying item exists when the register remains absent.
  - Assert no project-map risk or current-change follow-up was used to justify an empty register.
- Expected result: the first slice adds guidance without creating an empty process artifact.
- Failure proves: `docs/follow-ups.md` can become a blank backlog shell.
- Automation location: manual check with `test ! -e docs/follow-ups.md`; optional static validation in `scripts/test-skill-validator.py`.

### T7. Register admission rejects vague or owned items

- Covers: `R7`-`R7b`, `E6`, `E7`, `EC3`, `EC7`
- Level: contract, manual
- Fixture/setup: optional future `docs/follow-ups.md`, register admission rules
- Steps:
  - For any proposed register entry, verify it is not already owned by an active plan, change artifact, review-resolution, release report, proposal, or learn session.
  - Verify it has a durable source artifact or review-visible source.
  - Verify it has owner stage, owner surface, concrete next action, and expected cross-change relevance.
  - Verify chat-only, vague, or speculative notes are rejected.
  - If `Owner surface` is `undecided`, verify the next action is to choose the owner.
- Expected result: only actionable unowned cross-change items enter the register.
- Failure proves: the register can become a dumping ground.
- Automation location: manual review in first slice; future validator tests if `docs/follow-ups.md` is introduced.

### T8. Optional register has required shape when present

- Covers: `R8`-`R8c`, `R9`-`R9g`, `R12`-`R12d`, `E6`, `EC3`, `EC7`
- Level: integration
- Fixture/setup: optional future `docs/follow-ups.md`
- Steps:
  - If `docs/follow-ups.md` exists, assert it has a title, purpose statement, `Open follow-ups`, and `Closed follow-ups`.
  - Assert the open table has `ID`, `Title`, `Source`, `Owner stage`, `Owner surface`, `Status`, and `Next action`.
  - Assert the closed table has `ID`, `Title`, `Closed by`, and `Notes`.
  - Assert every open row has non-empty required values.
  - Assert closed rows link to the closing artifact or decision.
- Expected result: the register is structurally useful when present.
- Failure proves: future agents cannot reliably find owner, source, status, or next action.
- Automation location: future lightweight register validator or `scripts/test-skill-validator.py` if the register is introduced.

### T9. Register status values are constrained

- Covers: `R9`-`R9g`, `R12d`, `EC10`
- Level: integration
- Fixture/setup: optional future `docs/follow-ups.md`
- Steps:
  - If `docs/follow-ups.md` exists, assert every open status is one of `open`, `planned`, `blocked`, `done`, `superseded`, or `deferred`.
  - Assert `deferred` entries include reason and revisit condition.
  - Assert `blocked` entries name the decision, dependency, or artifact.
  - Assert `done` and `superseded` entries link to closing artifacts or decisions.
- Expected result: status is machine-checkable enough for lightweight validation and human-closeout.
- Failure proves: register status can drift into ambiguous backlog states.
- Automation location: future lightweight register validator or focused static test if the register is introduced.

### T10. No first-slice shared template is introduced

- Covers: `R10`-`R10c`, `R11f`, `E5`, `E9`, `EC8`, `EC9`
- Level: static, manual
- Fixture/setup: `templates/shared/`, `skills/workflow/SKILL.md`, `skills/project-map/SKILL.md`
- Steps:
  - Assert no new `templates/shared/*follow*` or equivalent shared follow-up ownership block exists in the first slice.
  - Assert `workflow` and `project-map` contain direct concise wording only.
  - Assert any future shared-template work is left to a later proposal after three or more skills need identical concise text.
- Expected result: first slice avoids premature shared generated prose.
- Failure proves: shared wording is introduced before repetition is proven.
- Automation location: manual diff review; optional static check in `scripts/test-skill-validator.py`.

### T11. Future register validation remains lightweight

- Covers: `R7`-`R9g`, `R12`-`R12e`, `E6`, `E7`, `EC3`, `EC10`
- Level: unit, integration
- Fixture/setup: future register validator, synthetic valid/invalid register fixtures
- Steps:
  - Only if `docs/follow-ups.md` is introduced, add tests for missing headings, missing open table columns, missing required open-entry values, and invalid statuses.
  - Add valid fixture coverage for one open entry and one closed entry.
  - Add invalid fixture coverage for an unknown status and a missing `Owner surface`.
  - Do not add semantic validation for every possible ownership claim in the first slice.
- Expected result: register validation catches structural drift without overfitting the policy.
- Failure proves: malformed entries can accumulate or validation becomes too heavy.
- Automation location: future focused validator tests if `docs/follow-ups.md` is introduced.

### T12. Affected workflow-governance surfaces are synchronized

- Covers: `R1`-`R6c`, `R10`-`R13a`, all examples indirectly
- Level: integration, manual
- Fixture/setup: changed files from M1 and M2, `docs/changes/.../change.yaml`
- Steps:
  - Run skill validation after canonical skill edits.
  - Run explicit-path lifecycle validation for touched lifecycle artifacts.
  - Run selector validation for touched workflow and skill paths when changed-path routing matters.
  - Confirm root guidance is updated, explicitly unaffected with rationale, or deferred with owner and follow-up when it names follow-up ownership.
  - Confirm generated public adapter output handling is updated, validated, explicitly unaffected, or deferred according to current adapter packaging rules.
- Expected result: affected surfaces agree and no stale governance guidance blocks handoff.
- Failure proves: implementation changes one surface while leaving another authoritative surface stale.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/project-map/SKILL.md`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-follow-up-ownership-and-deferred-work-register.md --path specs/follow-up-ownership-and-deferred-work-register.md --path specs/follow-up-ownership-and-deferred-work-register.test.md --path docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md --path docs/plan.md --path docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`

### T13. Review and change-local lifecycle evidence remains valid

- Covers: `R13`-`R13a`
- Level: integration
- Fixture/setup: `docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/`
- Steps:
  - Validate review artifacts after each formal review or review-driven update.
  - Validate change metadata after adding the test spec, implementation evidence, review evidence, and final validation evidence.
  - Run `git diff --check --` before each handoff.
- Expected result: change-local evidence remains valid and reconstructable.
- Failure proves: formal review or lifecycle evidence cannot be trusted.
- Automation location:
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`
  - `git diff --check --`

## Fixtures and data

- Existing canonical skill files:
  - `skills/workflow/SKILL.md`
  - `skills/project-map/SKILL.md`
- Existing workflow guide:
  - `docs/workflows.md`
- Lifecycle artifacts:
  - `docs/proposals/2026-05-13-follow-up-ownership-and-deferred-work-register.md`
  - `specs/follow-up-ownership-and-deferred-work-register.md`
  - `specs/follow-up-ownership-and-deferred-work-register.test.md`
  - `docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/`
- Optional future fixtures only if `docs/follow-ups.md` is introduced:
  - valid register with one open entry and one closed entry;
  - invalid register missing `Owner surface`;
  - invalid register with unknown status.

## Mocking/stubbing policy

No external services are needed.

Use real repository files for documentation and skill wording checks. Use synthetic temporary files or fixtures only for optional future register validation so malformed register cases do not pollute real project state.

## Migration or compatibility tests

- Historical plans, proposals, review-resolution records, release reports, learn sessions, and project-map risk notes are not migrated.
- Verify implementation does not create `docs/follow-ups.md` unless a qualifying item exists.
- Verify existing `docs/workflows.md` workflow guidance remains readable and does not become a competing spec.

## Observability verification

No runtime logs, metrics, traces, or audit events are required.

Verify observability through tracked artifacts:

- `docs/workflows.md` contains the follow-up ownership policy.
- Action-owning artifact guidance is visible in `workflow`.
- `project-map` boundary wording is visible in `project-map`.
- Change-local artifacts record affected-surface and validation decisions.

## Security/privacy verification

- Manual review confirms follow-up guidance forbids secrets, credentials, private keys, and private chat preservation in follow-up entries.
- If `docs/follow-ups.md` is introduced later, register validation or manual review must confirm source and next-action text do not include secrets or private local data.

## Performance checks

No runtime performance checks are required.

Token/performance-sensitive proof:

- Skill wording remains concise.
- Skills do not duplicate the full ownership table.
- No shared template is introduced in the first slice.
- Agents can use `docs/workflows.md` instead of broad-searching many documents for follow-up ownership rules.

## Manual QA checklist

- [ ] `docs/workflows.md` ownership table is complete and concise.
- [ ] `workflow` wording routes follow-ups without becoming a backlog policy document.
- [ ] `project-map` wording clearly says it does not own deferred execution.
- [ ] No empty `docs/follow-ups.md` exists.
- [ ] No first-slice follow-up ownership shared template exists.
- [ ] Root guidance and generated-output handling are updated, explicitly unaffected, or deferred with rationale.
- [ ] Validation notes name the commands actually run.

## What not to test

- Do not test full semantic correctness of every future follow-up ownership decision; that is a human workflow-routing judgment in this slice.
- Do not test historical follow-up migration; migration is out of scope.
- Do not add runtime end-to-end tests; this is workflow documentation, skill text, and optional validation behavior.
- Do not rely on snapshots as the only proof for skill wording.
- Do not require a `docs/follow-ups.md` fixture in real project state when no qualifying item exists.

## Uncovered gaps

None. If implementation identifies a qualifying unowned cross-change follow-up before M1 or M2, return to the plan and revise the register scope before creating `docs/follow-ups.md`.

## Next artifacts

```text
implement M1
code-review M1
review-resolution when triggered
implement M2
code-review M2
review-resolution when triggered
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Active proof-planning surface. Current downstream state is owned by the active plan `Current Handoff Summary`.
