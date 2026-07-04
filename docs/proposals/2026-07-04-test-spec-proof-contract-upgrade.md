# Proposal: Test-Spec Proof-Contract Upgrade

## Status

accepted

Accepted after clean `proposal-review-r1`.

## Problem

The `test-spec` skill designs proof before implementation, but its current authored contract does not make all proof ownership explicit enough for `test-spec-review`, `implement`, `code-review`, and `verify` to consume without inference.

The current skill already requires requirement coverage, example coverage, edge cases, test cases, fixtures and data, mocking/stubbing policy, manual QA, uncovered gaps, and readiness wording. It also keeps the test-spec artifact state separate from implementation readiness and routes formal workflow-managed test specs to `test-spec-review`.

That is not sufficient for the next quality bar. Recent review and learning evidence showed that a generated test spec can still name validation commands without making them executable, owned, staged, or auditable. In particular, reviewers had to discover after authoring that named validation commands lacked ownership, milestone timing, and evidence behavior.

The root issue is:

```text
The authoring skill does not yet encode the full proof contract that the review skill enforces.
```

## Goals

- Make the `test-spec` authoring contract explicit enough that future generated test specs are review-ready on first pass more often.
- Align `test-spec` authoring structures with `test-spec-review` expectations.
- Add a conditional validation-command ledger whenever a test spec names, references, or depends on validation commands.
- Require stable command IDs and references from test cases, milestone maps, and evidence rows when commands are involved.
- Classify commands as `existing/configured`, `planned-for-implementation`, `release-owned`, `ci-owned`, `external-owned`, or `not-applicable`.
- Capture command owner, owning milestone, first required milestone, failure behavior, zero-test behavior, safe-mode expectations, and evidence artifact.
- Add milestone proof maps for staged implementation plans.
- Update `SKILL.md`, the skeleton, command and milestone repeated-row assets, validation checks, representative fixtures, and generated-skill proof together.
- Preserve the current test-spec status model and `test-spec-review` gate.
- Avoid partial rollout where skill text references missing assets or skeleton structures that validation does not cover.

## Non-goals

- Do not make `test-spec` execute validation commands.
- Do not make `test-spec` implement tests or production code.
- Do not replace `test-spec-review`.
- Do not change the test-spec artifact status model from `active` as the relied-on proof-planning state.
- Do not let the test spec override approved feature specs, architecture records, ADRs, or plans.
- Do not require every test spec to use every possible proof level.
- Do not add manual proof contracts or manual-proof asset work in this proposal.
- Do not require staged milestone maps for one-shot trivial changes.
- Do not invent command names without classifying them as planned and assigning ownership.
- Do not migrate all historical test specs as part of this proposal.
- Do not hand-edit generated adapter output.

## Vision fit

fits the current vision

RigorLoop exists to make AI-assisted work traceable, resumable, and reviewable in Git. A test spec is the proof map that connects approved behavior to implementation evidence, code review, and verification. This proposal strengthens that traceability by requiring the test spec to record what must be proven, how it will be proven, when each proof becomes required, and where evidence is recorded.

The proposal is falsified if future test specs still name commands without ownership and milestone timing, implementation must infer which command to run or when it becomes required, `test-spec-review` keeps finding the same command and milestone proof-contract omissions, or `test-spec` starts claiming implementation, validation, branch, or PR readiness.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize `test-spec` around the principle that a test spec is a pre-implementation proof contract | in scope | Problem, Recommended Direction |
| Add validation command ledger with command IDs, ownership, milestone timing, evidence behavior, zero-test behavior, and side-effect boundaries | in scope | Goals, Recommended Direction, Acceptance Criteria |
| Require test cases, milestone maps, and evidence rows to reference command IDs | in scope | Recommended Direction, Acceptance Criteria |
| Add complete manual proof contracts with automation rationale, environment, evidence artifact, pass/fail criteria, owning stage, and re-run trigger | deferred follow-up | Non-goals, Scope Budget, Decision Log |
| Add milestone proof maps for staged work | in scope | Goals, Recommended Direction, Acceptance Criteria |
| Update skill text and skeleton/assets together | in scope | Goals, Scope Budget, Recommended Direction |
| Add validator and representative fixture coverage | in scope | Testing and Verification Strategy |
| Prove generated adapters include the revised skill and assets without hand editing generated output | in scope | Architecture Impact, Testing and Verification Strategy |
| Preserve the `active` test-spec model and `test-spec-review` route | in scope | Non-goals, Expected Behavior Changes |
| Avoid historical migration in this proposal | in scope | Non-goals, Rollout and Rollback |
| Use internal milestones for reviewability but ship one integrated external deliverable | in scope | Scope Budget, Rollout and Rollback |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Command ledger contract in `skills/test-spec/SKILL.md` | core to this proposal | Command ownership and evidence behavior are the primary review gap. |
| Milestone proof map contract in `skills/test-spec/SKILL.md` | core to this proposal | Staged implementation needs proof timing and milestone ownership. |
| `test-spec` skeleton update | same-slice dependency | Authors should start from the structure reviewers enforce. |
| Repeated-row assets for validation commands and milestone proof rows | same-slice dependency | The resource map should provide reusable filled structures for repeated proof rows. |
| Test-case asset update for command IDs, evidence artifact, and required milestone | same-slice dependency | Test cases should link to command and evidence ownership. |
| Skill validation and representative fixtures | same-slice dependency | The new authoring structure needs regression coverage against the recent omission classes. |
| Generated skill and adapter inclusion proof | same-slice dependency | Public skill output should reflect canonical authored skill changes. |
| Behavior-preservation evidence | same-slice dependency | The role, status model, and review route should remain unchanged while proof detail strengthens. |
| Manual proof contracts and `assets/manual-proof.md` | separate proposal | The owner direction is to avoid considering manual-proof cases in this proposal. |
| Full semantic validator for every future test-spec artifact | first-slice candidate | Representative validation may be enough initially; a full artifact validator can follow if drift persists. |
| Historical migration of older test specs | separate implementation slice | Backfilling old artifacts has different cost and should not block the new authoring contract. |
| Changes to `test-spec-review` role or outcome model | out of scope | This proposal strengthens authoring inputs for the existing review gate. |

## Context

The current `skills/test-spec/SKILL.md` defines `test-spec` as proof design before implementation and names `test-spec-review` as the downstream stage. Its required sections cover strategy, coverage maps, test cases, fixtures, manual QA, uncovered gaps, follow-on artifacts, and readiness. Its assets currently include:

```text
skills/test-spec/assets/test-spec-skeleton.md
skills/test-spec/assets/test-case.md
skills/test-spec/assets/coverage-map-row.md
```

The current skeleton does not include input artifact identities, a validation-command ledger, or a milestone proof map. The current test-case asset does not include command IDs, evidence artifacts, or required milestone fields.

This gap matters because `test-spec-review` is the independent pre-implementation proof adequacy gate. Review should challenge the proof map, but it should not have to rediscover missing command ownership or milestone proof timing after the authoring skill has already produced the artifact.

## Options Considered

### Option 1: Keep the current `test-spec` structure

Pros:

- No added authoring weight.
- No validator or asset changes.
- No risk of overfitting the skill to one recent review.

Cons:

- Reviewers keep finding avoidable omissions.
- Implementation must infer command ownership and timing.
- Code-review and verify cannot reliably inspect expected evidence without tracing unstated assumptions.

Rejected.

### Option 2: Update `test-spec-review` only

Pros:

- Keeps the authoring skill smaller.
- Gives the review gate more explicit checks.

Cons:

- Review remains the first place missing proof-contract structure is discovered.
- Authors still start from a skeleton that omits the enforced structures.
- The same omissions become predictable review churn rather than prevented defects.

Rejected.

### Option 3: Update `SKILL.md` only

Pros:

- Smaller diff than changing assets and validation.
- Makes the policy visible in the main skill text.

Cons:

- Skeleton and repeated-row assets would drift from the policy.
- Authors copying assets would not get the required proof-contract shape.
- Validators and representative fixtures would not protect the new contract.

Rejected.

### Option 4: Integrated proof-contract upgrade

Pros:

- Skill policy, skeleton, repeated structures, fixtures, validation, and generated output move together.
- Authors start from the same structure reviewers enforce.
- Implementation, code-review, and verify get stable command IDs, milestone proof mapping, and evidence locations.
- The current `active` test-spec model and `test-spec-review` gate remain intact.

Cons:

- Larger single change.
- Requires careful behavior-preservation proof so stronger proof metadata does not blur lifecycle ownership.

Recommended.

## Recommended Direction

Choose Option 4: implement one integrated proof-contract upgrade for `test-spec`.

The upgraded authoring contract should add these structures:

| Structure | Applicability | Purpose |
| --- | --- | --- |
| Input artifact identities | Required when implementation or code-review will rely on the test spec | Records upstream spec, review, plan, and architecture identities used to author the proof map. |
| Validation commands | Required whenever commands are named, referenced, or depended on | Makes command ownership, milestone timing, failure behavior, zero-test behavior, evidence artifacts, and side-effect boundaries explicit. |
| Milestone proof map | Required when the approved plan is milestone-based or has staged validation | Shows which tests, command IDs, and evidence artifacts are required before each milestone gate. |
| Strengthened test case format | Required for test cases | Adds command IDs, evidence artifact, and required milestone fields where commands or staged proof are involved. |

The validation-command ledger should use stable command IDs and a closed classification set:

```text
existing/configured
planned-for-implementation
release-owned
ci-owned
external-owned
not-applicable
```

Each command entry should identify the command, classification, owner, owning milestone, first required milestone, failure behavior, zero-test behavior, evidence artifact, and safe-mode or side-effect boundary. Planned commands should not become required before their owning milestone, but the test spec should record when they become required.

Milestone proof maps should link every implementation milestone to required test IDs, command IDs, evidence artifacts, the gate they are required before, and notes or explicit not-applicable rationale.

Update the resource map so the `test-spec` skill points authors to these assets:

```text
assets/test-spec-skeleton.md
assets/test-case.md
assets/coverage-map-row.md
assets/validation-command-row.md
assets/milestone-proof-row.md
```

The proposal does not require every small test spec to use every structure. Conditional sections can use explicit not-applicable rationale, for example no commands or no milestone-based plan.

## Expected Behavior Changes

- Future test specs include command ownership before review when commands are named.
- Future test cases reference command IDs when commands are involved.
- Milestone-based changes include milestone proof maps.
- `test-spec-review` can inspect proof adequacy from authored structures instead of inferring missing ownership.
- Implementation has clearer milestone proof obligations.
- Code-review can distinguish missing proof for a milestone from proof intentionally deferred to a later milestone or stage.
- Verify can inspect final evidence closure against command and evidence artifacts.
- The `test-spec` artifact remains an active proof-planning surface and does not claim implementation, validation, branch, or PR readiness.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| `skills/test-spec/SKILL.md` | Add command ledger, milestone proof map, input artifact identity, and self-check guidance. |
| `skills/test-spec/assets/test-spec-skeleton.md` | Add sections for input identities, validation commands, and milestone proof map. |
| `skills/test-spec/assets/test-case.md` | Add command IDs, evidence artifact, and required milestone fields. |
| `skills/test-spec/assets/validation-command-row.md` | New repeated structure for command ledger rows. |
| `skills/test-spec/assets/milestone-proof-row.md` | New repeated structure for milestone proof-map rows. |
| Skill validation | Add resource-map and asset-shape checks for the new structures. |
| Representative fixtures | Add pass/fail examples for command ledger and milestone proof map coverage. |
| Generated skills and adapters | Rebuild or validate generated output from canonical `skills/`; do not hand-edit generated adapter bodies. |
| Historical test specs | No automatic migration. |

## Testing and Verification Strategy

Validation should prove both structure and behavior preservation.

Structural checks should cover:

| Check ID | What is verified |
| --- | --- |
| `TSP-001` | `test-spec` resource map includes all required assets. |
| `TSP-002` | `test-spec-skeleton.md` contains `Validation commands`. |
| `TSP-003` | `test-spec-skeleton.md` contains `Milestone proof map`. |
| `TSP-004` | `validation-command-row.md` contains all required command fields. |
| `TSP-005` | `milestone-proof-row.md` contains all required milestone proof fields. |
| `TSP-006` | `test-case.md` includes command IDs, evidence artifact, and required milestone fields. |
| `TSP-007` | Formal workflow-managed test specs still route to `test-spec-review`. |
| `TSP-008` | No `test-spec` output claims implementation, verification, branch, or PR readiness. |
| `TSP-009` | Generated adapters include the revised skill and new assets. |

Representative fixture coverage should include:

| Fixture | Expected |
| --- | --- |
| Valid command ledger | pass |
| Named command missing from ledger | fail |
| Command missing classification | fail |
| Planned command missing owner or milestone | fail |
| Milestone plan without milestone proof map | fail |
| Test case uses raw command string without command ID | fail |
| Trivial non-milestone test spec with no commands | pass with explicit not-applicable rationale |

Behavior-preservation evidence should record that the test-spec role, status model, review route, requirement coverage, example coverage, and existing Manual QA behavior are preserved while command ownership and milestone proof are strengthened.

Candidate repository-owned validation includes the existing skill and adapter validation scripts, refined by the downstream spec and plan:

```bash
python scripts/validate-skills.py skills/test-spec/SKILL.md
python scripts/test-skill-validator.py
python scripts/build-skills.py
python scripts/validate-adapters.py
```

The exact commands should be settled in the downstream spec, test spec, and execution plan based on the final validator changes.

## Rollout and Rollback

Roll out as one coherent external upgrade. Internal implementation slices may be used for reviewability, but the public skill should not land in a state where `SKILL.md` references assets that do not exist, the skeleton requires structures validators do not cover, or generated output is known to lag canonical authored sources without a recorded deferral.

Enforcement should start with the canonical `test-spec` skill and assets, representative output fixtures, and new or changed workflow-managed test specs after this change. Historical test specs should not be automatically migrated in this proposal.

Rollback is straightforward: revert the canonical skill, assets, validators, fixtures, and generated-output proof together. Because historical test specs are not migrated and no runtime behavior executes commands, rollback risk is limited to authoring and validation surfaces.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Test specs become too heavy | Keep structures conditional with explicit not-applicable rationale for simple cases. |
| Authors invent command IDs without command reality | Require classification plus owner and milestone fields, and inspect known manifests and scripts when feasible. |
| Planned commands look executable too early | Separate owning milestone from first required milestone. |
| Manual proof remains vague | Keep manual-proof contracts out of this proposal and route that concern to a separate follow-up if the owner later wants it. |
| Skeleton becomes policy owner | Keep policy in `SKILL.md`; skeleton owns structure. |
| Historical test specs fail new checks | Apply enforcement to new and changed specs first; audit history separately. |
| Assets drift from skill text | Validate resource map and asset field shape. |
| Generated adapter output drifts | Validate generated output from canonical authored skills and avoid hand edits. |
| Review still finds the same omissions | Add representative fixtures that encode the recent finding classes. |

## Acceptance Criteria

| ID | Criterion |
| --- | --- |
| `AC-TSP-001` | `test-spec` requires a validation-command ledger whenever commands are named, referenced, or depended on. |
| `AC-TSP-002` | Every named command has a stable command ID. |
| `AC-TSP-003` | Command classifications use a closed enum. |
| `AC-TSP-004` | Planned commands identify owner, owning milestone, and first required milestone. |
| `AC-TSP-005` | Command entries include failure behavior, zero-test behavior, evidence artifact, and safe-mode boundary. |
| `AC-TSP-006` | Test cases reference command IDs when commands are involved. |
| `AC-TSP-007` | Milestone-based plans include a milestone proof map or explicit not-applicable rationale when the downstream spec permits it. |
| `AC-TSP-008` | The skeleton includes `Validation commands` and `Milestone proof map`. |
| `AC-TSP-009` | Manual proof contracts and `assets/manual-proof.md` are not part of this proposal. |
| `AC-TSP-010` | Repeated structures have packaged assets and are mapped in `SKILL.md`. |
| `AC-TSP-011` | The upgraded skill still routes formal workflow-managed test specs to `test-spec-review`. |
| `AC-TSP-012` | The test-spec artifact state model remains unchanged. |
| `AC-TSP-013` | The skill does not claim implementation, validation, branch, or PR readiness. |
| `AC-TSP-014` | Validators or representative fixtures catch missing command ownership and missing milestone proof mapping. |
| `AC-TSP-015` | Generated adapters include the revised skill and new assets. |
| `AC-TSP-016` | Historical test specs are not automatically migrated. |

## Open Questions

None.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-07-04 | Propose upgrading the skill and skeleton/assets together. | Reviewers enforce structure that authors should start from. | Update `SKILL.md` only. |
| 2026-07-04 | Propose a command ledger. | Review found named commands without ownership and milestone timing. | Leave commands as raw strings. |
| 2026-07-04 | Make the command ledger conditional, not universal. | Commands need ownership when named or depended on; command-free proof maps can state no validation commands are part of the proof map with rationale. | Require a command ledger with command rows for every test spec. |
| 2026-07-04 | Defer manual-proof contracts out of this proposal. | Owner direction is not to consider manual-proof cases now. | Include manual-proof contract assets in the integrated slice. |
| 2026-07-04 | Propose milestone proof maps. | Staged implementation needs proof timing and ownership. | Let implement and code-review infer timing. |
| 2026-07-04 | Make milestone proof maps mandatory for milestone-based plans only. | One-shot or very small changes can use not-applicable rationale without carrying staged proof structure. | Require milestone proof maps for every test spec. |
| 2026-07-04 | Preserve existing Manual QA behavior. | Manual-proof contracts are out of scope for this proposal. | Replace Manual QA checklist with manual proof contracts now. |
| 2026-07-04 | Inspect command existence during authoring when feasible, but do not execute commands. | Authoring should classify command reality without turning `test-spec` into a validation runner. | Execute commands during authoring; allow nonexistent commands without planned ownership. |
| 2026-07-04 | Start with representative fixture validation instead of a full test-spec artifact validator. | Representative validation targets the known drift classes while leaving room to add a full validator if future test specs still drift. | Build full semantic validation for every future test-spec artifact in this slice. |
| 2026-07-04 | Preserve test-spec status as `active`. | Review approval belongs in `test-spec-review`, not the test-spec status value. | Add `approved` status to test specs. |
| 2026-07-04 | Avoid automatic historical migration. | The new contract should improve future authoring without creating broad unrelated churn. | Rewrite all historical test specs now. |

## Next Artifacts

```text
proposal-review
spec: test-spec proof-contract authoring upgrade
spec-review
architecture or ADR only if spec review identifies a cross-component design decision
plan
plan-review
test-spec
test-spec-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on Artifacts

- Proposal review: `docs/changes/2026-07-04-test-spec-proof-contract-upgrade/reviews/proposal-review-r1.md`

## Readiness

Accepted after clean `proposal-review-r1`; ready for `spec`.
