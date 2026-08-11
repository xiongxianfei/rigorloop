# Planned milestone implementation

Load this procedure only after `SKILL.md` establishes valid `planned_milestone_context`.
The `implement` skill package remains the policy and lifecycle owner.

## Load conditions

Required evidence:

- workflow-managed invocation;
- valid active plan and owning `change.yaml`;
- one exact current milestone owned by `implement`;
- a current milestone state that permits implementation.

Do not load this reference for `IP0-isolated`.
Planned evidence without armed automation loads this reference alone.

## Milestone authority and inspection

Start with the owning `change.yaml`, then the active plan's `Current Handoff Summary`, the current milestone section, implementation validation notes, and review-resolution only when findings exist.

Confirm:

- `lifecycle_contract: stage-owned-change-local-v1`;
- plan artifact identity and current milestone match;
- the milestone is the first nonterminal implementation milestone;
- test-spec and test-spec-review identities are current;
- no blocker or unresolved prior review prevents execution.

For milestone readiness, do not run broad repository searches to infer milestone state.
If change-local state does not identify the current milestone or next stage, stop and report the missing state.

## Baseline change pack

Before implementation, identify the milestone's required authored surfaces, aligned surfaces, tests, commands, evidence path, rollback unit, and commit subject.
Treat the stable plan as execution intent and `change.yaml` as the sole live state owner.
Implementation writes scoped evidence only; workflow performs state transitions.

Record unchanged required surfaces as `unaffected with rationale`.
Do not postpone milestone work to make a later gate available.

## Milestone execution and validation

Implement only the current milestone.
Run its proof first, perform the smallest scope-complete change, and execute every command required before milestone code review.

After implementation:

- record decisions, surprises, changed and unaffected surfaces, commands, and results in milestone evidence;
- run the artifact-lifecycle state-sync check;
- confirm the handoff still binds the same plan and milestone;
- report implementation-complete only as evidence, never as a milestone state.

## Commit and review handoff

Create the implementation handoff commit with subject `M<n>: <implemented milestone outcome>` and include validation in its body or referenced evidence.

When required proof passes, report the milestone as ready for workflow to transition to `review-requested` and route to `code-review`.
The milestone becomes `closed` only after clean review and required resolution.
A clean non-final review returns workflow to the next in-scope implementation milestone; a clean final milestone enters final closeout rather than direct verification.

## Accepted correction return

Accepted findings stay attached to the same milestone.
Apply only the recorded resolution scope, rerun named validation, update implementation evidence, and return the same milestone to `review-requested` for rereview.

Do not silently rebind a correction to another milestone, alter upstream artifacts as bookkeeping, or start later work while the current milestone remains open.
