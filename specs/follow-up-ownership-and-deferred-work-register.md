# Follow-up Ownership and Deferred Work Register

## Status

approved

## Related proposal

- [Follow-Up Ownership and Deferred Work Register](../docs/proposals/2026-05-13-follow-up-ownership-and-deferred-work-register.md)

## Goal and context

This spec defines where RigorLoop follow-ups and deferred work are recorded so future work remains discoverable without turning `project-map` into a backlog.

The contract is intentionally split:

- `docs/workflows.md` owns the user-facing follow-up ownership table.
- `workflow` routes follow-ups to the artifact that can act on them.
- `project-map` records repository orientation risks and open questions, but does not own deferred execution.
- action-owning artifacts, such as plans, change artifacts, review-resolution, release reports, proposals, and learn sessions, own work that belongs to their scope.
- `docs/follow-ups.md` is optional and exists only for accepted cross-change follow-ups that are not already owned by another durable artifact.

The first implementation slice keeps skill text concise. It does not introduce a `templates/shared/` block.

## Glossary

- `follow-up`: future work discovered during a RigorLoop activity that is not completed immediately.
- `deferred execution`: follow-up work that requires future action rather than an orientation note.
- `action-owning artifact`: a durable artifact that can drive, resolve, or close the follow-up, such as an active plan, change artifact, review-resolution, release report, proposal, or learn session.
- `unowned cross-change follow-up`: a real follow-up expected to matter beyond the current change and not already owned by an action-owning artifact.
- `follow-up register`: the optional `docs/follow-ups.md` file for unowned cross-change follow-ups.
- `owner stage`: the lifecycle stage expected to act on or route the follow-up, such as `proposal`, `plan`, `learn`, or release workflow.
- `owner surface`: the artifact type or specific artifact path expected to own or close the follow-up.
- `project-map orientation note`: a risk or open question recorded in `project-map` to help repository understanding, not to track execution.

## Examples first

### Example E1: current-change follow-up stays in the active plan

Given an implementation plan defers one milestone to a later slice
When the follow-up belongs to the same active change
Then the plan records the deferred milestone or follow-up
And `docs/follow-ups.md` is not created for that item.

### Example E2: review finding follow-up stays in review-resolution

Given `code-review` records a material finding that requires later validation
When the finding is accepted, deferred, or partially accepted
Then `review-resolution.md` records the disposition, rationale, follow-up, and validation evidence required by the review-resolution contract
And `project-map` is not used as the follow-up tracker.

### Example E3: project-map risk remains an orientation note

Given `project-map` identifies weak test coverage in a repository area
And no concrete action, owner stage, or source rationale has been selected
When the map is updated
Then the item remains a risk or open question in `project-map`
And no follow-up register entry is created.

### Example E4: project-map risk routes to an action-owning artifact

Given `project-map` identifies unclear release ownership
And maintainers decide the work requires a workflow policy change
When the risk becomes actionable
Then the follow-up is routed to a proposal
And `project-map` continues to record only the orientation risk or link to the owner.

### Example E5: optional register is not created empty

Given no accepted unowned cross-change follow-up exists
When the first implementation slice adds follow-up ownership guidance
Then `docs/workflows.md`, `workflow`, and `project-map` are updated
And `docs/follow-ups.md` is not created.

### Example E6: register entry is admitted

Given a release report identifies future adapter packaging work
And the item is accepted, cross-change, has a source artifact, has an owner stage, has an owner surface, and has a concrete next action
When no active plan, proposal, release report, review-resolution, change artifact, or learn session owns it
Then the item may be added to `docs/follow-ups.md`.

### Example E7: vague idea is rejected from the register

Given a chat note says "clean up docs sometime"
When it has no durable source artifact, owner stage, owner surface, or concrete next action
Then it is not added to `docs/follow-ups.md`.

### Example E8: learn follow-up routes by ownership

Given a learn session identifies repeated release smoke confusion
When the fix requires workflow policy
Then the follow-up routes to a proposal
And the learn session is the source artifact.

### Example E9: first slice avoids shared templates

Given only `workflow` and `project-map` need follow-up wording
When the first implementation slice updates skill text
Then each skill receives concise operational wording
And no `templates/shared/` block is introduced.

## Requirements

R1. `docs/workflows.md` MUST define follow-up ownership in a clearly labeled `Follow-up ownership` section or an equivalent section whose purpose is unambiguous.

R1a. The follow-up ownership section MUST tell users and agents to record follow-ups where they can be acted on.

R1b. The follow-up ownership section MUST include a table or equivalent list that maps these follow-up types to owners:

- active implementation follow-up;
- review finding follow-up;
- change closeout follow-up;
- release follow-up;
- repeated lesson;
- architecture risk or open question;
- unowned cross-change future work;
- new direction or policy change.

R1c. The follow-up ownership section MUST state that `project-map` may identify risks and open questions, but does not own deferred execution.

R1d. `docs/workflows.md` MUST remain the policy owner for follow-up placement. Skill text MUST NOT replace it with a second full policy table.

R2. Follow-ups MUST be recorded in the artifact that can act on them whenever such an artifact exists.

R2a. Current implementation follow-ups MUST be recorded in the active plan or active change artifacts.

R2b. Review finding follow-ups MUST be recorded in `review-resolution.md` when the review-resolution contract is triggered.

R2c. Change closeout follow-ups MUST be recorded in `explain-change.md`, `change.yaml`, or another current change-local artifact when they belong to the active change.

R2d. Release follow-ups MUST be recorded in the release report, release plan, or another release-owned artifact when they belong to release work.

R2e. Follow-ups requiring new product direction, workflow policy, source-of-truth ownership, public skill behavior, release packaging policy, or architecture direction MUST route to `proposal`.

R2f. Future implementation sequences MUST route to `plan` once the direction is accepted and sequencing is needed.

R3. `project-map` MUST NOT own deferred execution.

R3a. `project-map` MAY record risks, unclear ownership, missing tests, architecture uncertainty, and open questions as repository orientation notes.

R3b. A `project-map` risk MUST become an execution follow-up only when it has a concrete action, owner stage, and source rationale.

R3c. If a `project-map` risk does not satisfy `R3b`, it MUST remain an orientation note rather than being converted into `docs/follow-ups.md`, a proposal, or a plan.

R3d. When a `project-map` risk satisfies `R3b`, workflow routing MUST send it to an action-owning artifact such as proposal, plan, learn, review-resolution, release evidence, or the follow-up register when register rules are satisfied.

R4. `workflow` MUST route follow-ups to the artifact that can act on them.

R4a. `workflow` MUST use `docs/workflows.md` as the follow-up placement guide.

R4b. `workflow` MUST NOT maintain a backlog inside `project-map`.

R4c. `workflow` MUST NOT create detailed plans for every follow-up solely because it routes follow-ups.

R4d. `workflow` MUST NOT turn every minor note into tracked future work.

R5. `learn` MUST NOT be used as a general backlog.

R5a. Learn follow-ups tied to the current change MUST route to the active plan or current change artifacts.

R5b. Learn follow-ups requiring policy, workflow, skill, architecture, or other direction-setting changes MUST route to proposal.

R5c. Learn follow-ups that are accepted, real, cross-change, and unowned MAY route to `docs/follow-ups.md`, with the learn session recorded as the source.

R6. `docs/follow-ups.md` MUST be optional.

R6a. The system MUST NOT create `docs/follow-ups.md` unless at least one accepted follow-up is real, cross-change, and not already owned by an active plan, change artifact, review-resolution, release report, proposal, or learn session.

R6b. The first implementation slice MUST NOT create an empty `docs/follow-ups.md`.

R6c. If no follow-up satisfies the creation rule, the implementation MUST update `docs/workflows.md` and concise skill guidance without creating the register.

R7. A `docs/follow-ups.md` entry MUST satisfy all admission criteria:

- the item is not already owned by an active plan, change artifact, review-resolution, release report, proposal, or learn session;
- the item has a durable source artifact or review-visible source;
- the item has an owner stage or owning artifact type;
- the item has an owner surface;
- the item has a concrete next action;
- the item is expected to matter beyond the current change.

R7a. Chat-only, vague, or speculative notes MUST NOT be added to `docs/follow-ups.md`.

R7b. If `Owner surface` is `undecided`, the next action MUST be to choose the owner rather than to implement the work.

R8. If `docs/follow-ups.md` exists, it MUST contain:

- a title;
- a short purpose statement;
- an `Open follow-ups` section;
- a `Closed follow-ups` section.

R8a. The open follow-ups table MUST include columns equivalent to `ID`, `Title`, `Source`, `Owner stage`, `Owner surface`, `Status`, and `Next action`.

R8b. The closed follow-ups table MUST include columns equivalent to `ID`, `Title`, `Closed by`, and `Notes`.

R8c. Each open entry MUST include non-empty values for `ID`, `Title`, `Source`, `Owner stage`, `Owner surface`, `Status`, and `Next action`.

R9. Follow-up register status MUST use only these values:

- `open`;
- `planned`;
- `blocked`;
- `done`;
- `superseded`;
- `deferred`.

R9a. `open` means an accepted follow-up exists but is not yet owned by an active plan, proposal, release plan, or other action-owning artifact.

R9b. `planned` means the follow-up is now owned by a proposal, plan, release plan, or other action-owning artifact.

R9c. `blocked` means the follow-up cannot proceed until a named decision, dependency, or artifact exists.

R9d. `done` means the follow-up was completed and links to the closing artifact.

R9e. `superseded` means the follow-up was replaced by another artifact or decision.

R9f. `deferred` means the follow-up remains valid but is intentionally postponed and includes a reason plus revisit condition.

R9g. Closed follow-ups MUST link to the artifact or decision that closed them.

R10. The first implementation slice MUST NOT introduce a `templates/shared/` block for follow-up ownership wording.

R10a. The first implementation slice MUST put the durable ownership rule in `docs/workflows.md`.

R10b. The first implementation slice MUST add only concise operational wording to `workflow` and `project-map`.

R10c. A shared template MAY be proposed later only if three or more skills require the same concise operational text and duplication becomes a measured maintenance problem.

R11. Skill wording MUST stay concise.

R11a. `workflow` skill wording MUST route future work to the artifact that can act on it and refer to `docs/workflows.md` for the ownership rule.

R11b. `workflow` skill wording MUST state that deferred execution work does not belong in `project-map`.

R11c. `project-map` skill wording MUST state that `project-map` may record risks and open questions for orientation.

R11d. `project-map` skill wording MUST state that `project-map` does not own deferred execution or act as a backlog.

R11e. `project-map` skill wording MUST tell agents to route actionable risks through the workflow guide.

R11f. Public skill wording MUST NOT duplicate the full `docs/workflows.md` follow-up ownership table.

R12. If `docs/follow-ups.md` is created, repository-owned validation MUST include lightweight structural checks for the register.

R12a. Initial validation MUST check that required headings exist.

R12b. Initial validation MUST check that the open table has required columns.

R12c. Initial validation MUST check that each open entry has `ID`, `Title`, `Source`, `Owner stage`, `Owner surface`, `Status`, and `Next action`.

R12d. Initial validation MUST check that status is one of the allowed values in `R9`.

R12e. The first slice MUST NOT add semantic validation for every possible ownership claim.

R13. Workflow-governance surfaces affected by this contract MUST be updated, explicitly marked unaffected with rationale, or recorded as deferred with owner and follow-up in a contributor-visible tracked or review-visible surface.

R13a. At minimum, the affected-surface check MUST consider `docs/workflows.md`, `skills/workflow/SKILL.md`, `skills/project-map/SKILL.md`, generated public skill or adapter output when canonical skills change and generated output remains tracked, and root guidance if it names follow-up ownership.

## Inputs and outputs

Inputs:

- maintainer or agent discoveries that create potential follow-ups;
- review findings and review-resolution dispositions;
- active plans and change-local artifacts;
- release reports or release plans;
- learn sessions;
- `project-map` risks and open questions;
- proposal or policy decisions.

Outputs:

- follow-up ownership guidance in `docs/workflows.md`;
- concise routing guidance in `workflow`;
- concise orientation boundary guidance in `project-map`;
- action-owning artifact updates when a follow-up belongs to an existing owner;
- optional `docs/follow-ups.md` entries only when creation and admission rules are met.

## State and invariants

- `project-map` orients; it does not own deferred execution.
- `workflow` routes; it does not replace action-owning artifacts.
- Action-owning artifacts track work when they can act on it.
- `docs/follow-ups.md` holds only accepted unowned cross-change follow-ups.
- Empty `docs/follow-ups.md` is not created.
- No shared follow-up wording template exists in the first slice.

## Error and boundary behavior

- If a follow-up has no durable source or review-visible source, it is not admitted to `docs/follow-ups.md`.
- If a follow-up has no concrete next action, it is not admitted to `docs/follow-ups.md`.
- If a follow-up already belongs to an active plan, change artifact, review-resolution, release report, proposal, or learn session, it stays there.
- If a `project-map` note lacks concrete action, owner stage, or source rationale, it remains an orientation note.
- If `docs/follow-ups.md` exists and contains an unknown status, validation fails.
- If `docs/follow-ups.md` exists and an open entry lacks a required field, validation fails.
- If the correct owner cannot be determined, the item may use `Owner surface: undecided` only when the next action is to choose the owner.

## Compatibility and migration

Existing proposals, plans, change artifacts, review-resolution records, release reports, learn sessions, and `project-map` notes remain valid. This contract does not require migrating every historical follow-up into `docs/follow-ups.md`.

Existing `project-map` risk and open-question sections remain valid as orientation surfaces. They must not be reinterpreted as execution backlogs.

Existing follow-ups already owned by active or historical artifacts should stay with those artifacts unless a later accepted plan chooses to migrate them.

Rollback is compatible with retaining `docs/workflows.md` ownership guidance while removing `docs/follow-ups.md` if the register creates noise.

## Observability

Follow-up routing must be observable through tracked artifacts:

- `docs/workflows.md` shows the ownership rule;
- action-owning artifacts show current-change and stage-owned follow-ups;
- `docs/follow-ups.md`, when present, shows unowned cross-change follow-ups;
- review-visible or tracked surfaces record any affected-surface deferral or unaffected rationale required by workflow governance.

No runtime logs, metrics, or traces are required because this is workflow documentation and validation behavior.

## Security and privacy

Follow-up entries and source links must not expose secrets, credentials, private keys, or machine-local sensitive information.

`docs/follow-ups.md` must not become a place to preserve private chat content. Entries require durable or review-visible sources and concise next actions.

## Accessibility and UX

No UI behavior is involved.

## Performance expectations

Skill wording should remain token-conscious:

- the full ownership table lives in `docs/workflows.md`;
- `workflow` and `project-map` receive short operational wording;
- the first slice does not introduce a shared template;
- agents should not broad-search many documents solely to find follow-up ownership rules.

## Edge cases

EC1. A current change discovers a cleanup that belongs to the active plan: record it in the plan, not `docs/follow-ups.md`.

EC2. A review finding is deferred with a final disposition: record it in `review-resolution.md`, not `project-map`.

EC3. A release report discovers future work that is not owned by a plan: add it to `docs/follow-ups.md` only if it satisfies the creation and admission rules.

EC4. A learn session discovers a repeated problem requiring new policy: route it to proposal, not a learn backlog.

EC5. A `project-map` risk has no action yet: keep it as an orientation note.

EC6. A `project-map` risk becomes actionable and needs implementation sequencing: route it to proposal or plan before implementation.

EC7. A proposed follow-up has `Owner surface: undecided`: its next action is to choose the owner.

EC8. No qualifying unowned follow-up exists during M1: do not create `docs/follow-ups.md`.

EC9. Three or more skills later need identical concise follow-up wording: propose a shared template separately before introducing it.

EC10. `docs/follow-ups.md` has a status outside `open`, `planned`, `blocked`, `done`, `superseded`, or `deferred`: validation fails.

## Non-goals

- Do not create a new workflow stage.
- Do not create a new skill for follow-up ownership.
- Do not make `project-map` a backlog.
- Do not require every minor note to become tracked future work.
- Do not migrate all historical follow-ups.
- Do not replace proposals, plans, learn sessions, release reports, review-resolution, or change artifacts.
- Do not change workflow stage order.
- Do not introduce heavy semantic validation in the first slice.
- Do not introduce a `templates/shared/` block in the first slice.

## Acceptance criteria

- `docs/workflows.md` defines follow-up ownership.
- `workflow` routes future work according to the workflow guide.
- `project-map` explicitly says it does not own deferred execution or act as a backlog.
- `docs/follow-ups.md` is absent when no qualifying unowned cross-change follow-up exists.
- If `docs/follow-ups.md` exists, it uses the required headings, table columns, fields, and status values.
- Current-change follow-ups stay in active plans, change artifacts, review-resolution, release reports, or explain-change artifacts when those are the action-owning surfaces.
- Proposal-worthy follow-ups route to `proposal`.
- Learn-worthy follow-ups route according to `R5`.
- No `templates/shared/` block is introduced in the first slice.
- Skill wording does not duplicate the full follow-up ownership table.
- Minimal validation exists if the follow-up register exists.

## Open questions

None.

## Next artifacts

```text
spec-review
architecture only if review identifies broader architecture impact
plan
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- [Follow-up Ownership and Deferred Work Register plan](../docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md)
- [Follow-up Ownership and Deferred Work Register test spec](follow-up-ownership-and-deferred-work-register.test.md)

## Readiness

Approved after spec-review. Downstream plan and test spec are active.
