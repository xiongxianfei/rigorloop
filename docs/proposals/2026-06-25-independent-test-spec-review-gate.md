# Independent Test-Spec-Review Gate for Proof-Map Adequacy

## Status

accepted

## Problem

RigorLoop has a defined authoring stage for test specifications, but it does not currently have a named independent owner for reviewing whether a test specification is sufficient before implementation begins.

The current lifecycle establishes:

```text
plan-review
-> test-spec
-> implement
-> code-review
```

This creates an ownership gap. `plan-review` can determine that an approved plan is ready for test-spec authoring, but it cannot review the resulting test spec because that artifact does not exist yet. `code-review` and `verify` can discover weak coverage later, but by then implementation has already relied on the proof map.

The workflow intentionally treats a test spec differently from a feature spec:

```text
feature spec:
  durable behavior contract
  review approval settles the contract

test spec:
  active proof map
  operationalizes the approved contract and plan
```

That distinction should remain. A test spec does not need a new artifact status such as `approved`; it needs a separate review result establishing whether the active proof map is adequate for implementation.

The adjacent gates cannot fully absorb this responsibility:

| Existing stage | Why it is insufficient |
| --- | --- |
| `spec-review` | Reviews requirements before the plan and test spec exist. |
| `architecture-review` | Reviews design boundaries, not proof coverage. |
| `plan-review` | Runs before the test spec is authored. |
| `implement` | Should consume an adequate test spec, not approve its own proof contract. |
| `code-review` | Runs after implementation has already relied on the test spec. |
| `verify` | Confirms final evidence; it should not be the first test-spec adequacy gate. |

A dedicated `test-spec-review` skill is justified because it owns a distinct, recurring, pre-implementation review responsibility: independent proof-map adequacy.

## Goals

- Add a dedicated `test-spec-review` skill.
- Insert the gate between `test-spec` and `implement`.
- Independently assess whether an active test spec is adequate for implementation.
- Preserve the test-spec artifact settlement state as `active`.
- Record review outcomes separately as `approved`, `changes-requested`, `blocked`, or `inconclusive`.
- Require traceability from approved requirements, examples, edge cases, architecture decisions, and plan milestones to test cases and evidence.
- Review negative, boundary, error, permission, compatibility, migration, rollback, and observability coverage when relevant.
- Verify that planned validation commands are real, correctly sourced, and capable of failing when required behavior is absent.
- Review automation versus manual-proof boundaries.
- Require deterministic fixtures, test isolation, cleanup, and safe data handling where relevant.
- Prevent test specs from silently overriding approved product or architecture contracts.
- Require re-review after substantive test-spec changes.
- Keep formal review records inside the change pack.
- Preserve isolated/manual review use without claiming full workflow approval.
- Add validator, workflow, skill-inventory, generated-adapter, and lifecycle proof for the new stage.

## Non-goals

- Do not make `test-spec-review` author or rewrite the test spec.
- Do not reapprove product requirements.
- Do not redesign architecture.
- Do not reapprove implementation milestone sequencing.
- Do not implement tests or production code.
- Do not execute final validation or claim that planned commands pass.
- Do not replace `code-review` or `verify`.
- Do not change the test-spec settlement state from `active`.
- Do not create a new `conditionally-approved` review result.
- Do not auto-start implementation from an isolated review invocation.
- Do not require historical test specs to be retroactively reviewed in the first slice.
- Do not introduce a numeric quality score as a substitute for reviewer judgment.
- Do not require a different AI vendor or model for every review unless the governing review-independence contract separately requires it.
- Do not hand-edit generated adapter output.

## Vision fit

fits the current vision

RigorLoop depends on traceable and reviewable evidence before implementation and final verification. A test spec bridges approved behavior, approved architecture and plan, implemented tests and production changes, and final verification evidence.

Independent review of that bridge reduces the risk that implementation begins with missing requirement coverage, happy-path-only tests, non-existent validation commands, ambiguous manual proof, untestable acceptance criteria, milestone sequencing that cannot produce reviewable evidence, or unsafe and nondeterministic fixtures.

The proposal is falsified if `test-spec-review` reapproves product requirements instead of reviewing proof, implementation can proceed with a stale or changes-requested review, review approval is stored only by changing the test spec's `active` status, the reviewer must wait for implemented tests before reaching a result, code-review or verify becomes weaker because the new gate exists, review findings are not durably recorded, or the skill creates ceremony without detecting meaningful proof gaps.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Identify who approves an active test spec | in scope | Problem, Recommended Direction |
| Consider a dedicated skill | in scope | Options Considered |
| Preserve the test-spec `active` state | in scope | Recommended Direction, Expected Behavior Changes |
| Add independent proof review before implementation | in scope | Goals, Recommended Direction |
| Avoid duplicating spec-review | in scope | Non-goals, Review Boundary |
| Avoid making code-review the first adequacy gate | in scope | Problem, Options Considered |
| Keep later review and verify backstops | in scope | Non-goals, Expected Behavior Changes |
| Change workflow only through an owning proposal/spec | in scope | Next Artifacts, Readiness |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| New `test-spec-review` skill | core to this proposal | It owns the new independent gate. |
| New workflow stage | core to this proposal | The gate belongs between `test-spec` and `implement`. |
| Review result and finding assets | core to this proposal | Review output needs a consistent structure. |
| Workflow and stage-skill updates | same-slice dependency | Routing needs to be coherent. |
| Implement precondition update | same-slice dependency | Implementation should consume approved proof. |
| Formal review-record placement | same-slice dependency | Review evidence should be durable. |
| Skill and lifecycle validator coverage | same-slice dependency | Stage and output rules need enforcement. |
| Generated adapter inclusion | same-slice dependency | Public skill installations should include the new skill. |
| Historical test-spec review | separate implementation slice | Retrospective review has different cost and value. |
| Automated semantic scoring of test specs | out of scope | Reviewer judgment remains necessary. |
| Execution of planned tests during review | out of scope | Tests may not exist yet. |
| Review-model/vendor independence enforcement | separate proposal | Broader review-independence policy should own it. |

## Context

The existing test-spec authoring contract treats the test spec as the proof-design artifact produced after an approved plan and before implementation. Its role is to map requirements, examples, edge cases, and plan surfaces into test cases and validation evidence while avoiding claims of implementation, code-review approval, verification, or branch readiness.

The proposed review gate should follow the established review-family pattern:

```text
independent stage invocation
closed review-status enum
material findings with evidence and required outcomes
formal review record
review-log entry
review-resolution when findings require disposition
no automatic downstream claim from isolated review use
```

The existing `spec-review` skill demonstrates the applicable structure: normalized frontmatter, workflow-role boundaries, explicit review dimensions, resource-mapped review skeletons, material-finding records, and must-not-claim constraints.

## Options Considered

### Option 1: Keep the repository-defined review surface

Pros:

- No workflow change.
- Repositories can choose their own process.
- No additional skill or validation work.

Cons:

- Ownership remains ambiguous.
- Different changes receive inconsistent review.
- Implementation may begin without independent proof-map review.
- Review records and handoff rules remain nonstandard.

Rejected.

### Option 2: Make `plan-review` own test-spec approval

Pros:

- Reuses an existing pre-implementation gate.
- Avoids adding a lifecycle stage.

Cons:

- The test spec does not exist when plan-review runs.
- Moving plan-review later would weaken plan authoring and disrupt current stage semantics.
- Combining plan and test-spec approval creates an oversized gate.

Rejected.

### Option 3: Make `implement` validate the test spec before coding

Pros:

- Implementation already consumes the test spec.
- No additional review stage.

Cons:

- Author and gate owner are no longer independent.
- Implementation may interpret or repair proof gaps silently.
- Weak test specifications can become implementation assumptions.

Rejected.

### Option 4: Use `code-review` or `verify` as the approval owner

Pros:

- Existing reviewers already inspect tests and evidence.
- No new stage.

Cons:

- Both occur after implementation has relied on the test spec.
- Defects are found late and create avoidable code/test churn.
- They review implemented evidence, not only the pre-implementation proof map.

Rejected as the primary owner.

### Option 5: Add a dedicated `test-spec-review` gate

Pros:

- Gives proof adequacy a clear independent owner.
- Runs at the correct lifecycle point.
- Keeps test-spec state and review status separate.
- Preserves later code-review and verify responsibilities.
- Standardizes review dimensions, records, and stop conditions.
- Prevents implementation from beginning with a weak proof map.

Cons:

- Adds a workflow stage and public skill.
- Requires workflow, validation, adapter, and documentation updates.
- Adds review cost for non-trivial changes.

Recommended.

## Recommended Direction

Choose Option 5. Adopt this standard workflow for formal workflow-managed work:

```text
proposal
-> proposal-review
-> spec
-> spec-review
-> architecture, when required
-> architecture-review, when required
-> plan
-> plan-review
-> test-spec
-> test-spec-review
-> implement
-> code-review
-> review-resolution, when triggered
-> ci-maintenance, when triggered
-> explain-change
-> verify
-> pr
```

The new gate is mandatory whenever the workflow requires a formal test spec. Isolated/manual test-spec authoring and review remain possible, but they do not establish formal implementation eligibility unless the review is recorded under the workflow contract.

### Artifact-state contract

Keep the durable test-spec artifact state as:

```text
active
```

Do not add `approved` or `changes-requested` to the test-spec artifact-state enum. The artifact state means "this is the current proof map for the change." The review record means "an independent reviewer has or has not accepted its adequacy."

Implementation may begin only when the required feature spec is approved, required architecture review is clean, the plan and plan-review are clean, the test spec is active, the latest applicable `test-spec-review` is approved, no later substantive test-spec change has made that review stale, and no material `test-spec-review` finding remains open.

### Published-skill contract

Add the canonical skill at:

```text
skills/test-spec-review/
  SKILL.md
  assets/
    review-result-skeleton.md
    material-finding.md
```

The skill frontmatter should identify it as an independent review of an active test specification before implementation, focused on proof-map alignment, requirement and edge-case coverage, milestone mapping, validation commands, fixtures, automation/manual evidence, and implementation handoff readiness.

The workflow role should set:

```text
role_name: test-spec-review
stage: review
upstream: active test spec, approved feature spec, approved architecture when required, approved plan, clean plan-review, and project-local workflow evidence
downstream: implement, test-spec revision, upstream artifact revision, review-resolution when triggered, or isolated stop
summary: Independently review whether the active test spec is a complete, executable, and traceable proof map for implementation.
must_not_claim: test implementation, production implementation, code-review approval, validation success, branch readiness, PR readiness, or final lifecycle closeout.
```

### Review boundary

The review should be a distinct review-stage invocation. It should not author and approve the same test-spec content in one undifferentiated action, rewrite the test spec during review unless explicitly requested, weaken the finding threshold because implementation is waiting, or review product direction instead of proof adequacy.

If the same agent performs authoring and review, it should use a separate review context and apply the repository's existing review-independence rules.

### Review dimensions

Evaluate each dimension using `pass`, `concern`, or `block`:

| Review dimension | Review question |
| --- | --- |
| Governing-contract alignment | Does the test spec operationalize, rather than override, the approved spec, architecture, and plan? |
| Requirement coverage | Does every in-scope normative requirement and acceptance criterion map to test cases or explicit manual evidence? |
| Example coverage | Are approved examples represented by stable test IDs? |
| Negative and boundary coverage | Are empty, invalid, failure, permission, security, compatibility, migration, rollback, old-client, and old-data cases covered when relevant? |
| Proof-level adequacy | Are unit, integration, end-to-end, smoke, static, and manual levels chosen according to the behavior and risk? |
| Milestone mapping | Does the test spec align tests and validation to implementation milestones and review boundaries? |
| Command validity | Do named commands exist or have an explicit implementation owner, correct arguments, failure behavior, and zero-test safety? |
| Fixture and data design | Are fixtures deterministic, isolated, safe, representative, and cleaned up? |
| Manual-proof boundary | Are manual checks used only where automation is impractical, with exact procedure, evidence location, and pass/fail criteria? |
| Observability | Will failures expose which requirement, case, command, or environment failed? |
| Determinism and isolation | Are tests protected from hidden order, shared mutable state, network dependence, time, randomness, and external environment drift? |
| Scope and non-goals | Does the proof map avoid adding requirements or implementation scope not approved upstream? |
| Execution economics | Does the test plan distinguish fast focused checks from expensive boundary/release checks without weakening coverage? |
| Traceability | Are requirement, example, milestone, test, and validation IDs linked consistently? |
| Implementation handoff | Can implementation proceed without guessing how required behavior will be proved? |

### Review result contract

Use the closed review-status enum:

```text
approved
changes-requested
blocked
inconclusive
```

Meanings:

| Status | Meaning |
| --- | --- |
| `approved` | No material proof-map defect remains; implementation handoff is allowed if all other workflow gates are clean. |
| `changes-requested` | The target is reviewable, but proof-map defects require revision. |
| `blocked` | A missing or contradictory upstream contract prevents a valid review. |
| `inconclusive` | The available evidence is insufficient to determine adequacy. |

Do not add `conditionally-approved`.

An `inconclusive` result should identify the specific evidence gap, explain why the gap prevents a proof-map adequacy judgment, and name the smallest evidence the author or upstream owner can provide to make a later review conclusive. It should not become an unlabeled soft rejection.

Use this immediate-next-stage enum:

```text
test-spec revision
spec revision
architecture revision
plan revision
review-resolution
implement
none
```

Use this implementation-handoff enum:

```text
allowed
not-allowed
```

Required mapping:

```text
approved:
  allowed

changes-requested:
  not-allowed

blocked:
  not-allowed

inconclusive:
  not-allowed
```

### Result skeleton

The review result should include:

```md
## Result

- Skill: test-spec-review
- Review status: <approved | changes-requested | blocked | inconclusive>
- Material findings: <finding IDs or none>
- Recording status: <recorded | blocked | not-required>
- Recording blocker: <blocker or none>
- Review record: <path | blocked | not-required>
- Review log: <path | blocked | not-required>
- Review resolution: <path | blocked | not-required>
- Open blockers: <blockers or none>
- Immediate next stage: <test-spec revision | spec revision | architecture revision | plan revision | review-resolution | implement | none>
- Implementation handoff: <allowed | not-allowed>
- Stop condition: <exact stop condition or none>
```

Validators should reject inconsistent combinations such as `Review status: changes-requested` with `Implementation handoff: allowed`, or `Review status: approved` with `Immediate next stage: test-spec revision`.

### Material findings

Reuse the existing review-family material-finding contract. Each material finding should include a finding ID, severity, location, evidence, required outcome, safe resolution path, and `needs-decision` rationale when applicable.

A finding should identify the uncovered or contradictory proof obligation, the governing requirement, example, milestone, or command, why the omission matters before implementation, and the smallest safe correction. Vague findings such as "add more tests" or "coverage seems incomplete" are not sufficient.

### Artifact placement

For formal workflow-managed review:

```text
docs/changes/<change-id>/reviews/test-spec-review-r<n>.md
```

Also update:

```text
docs/changes/<change-id>/review-log.md
```

Create or update:

```text
docs/changes/<change-id>/review-resolution.md
```

only when material findings or blocking outcomes require disposition.

If no change pack exists for a formal workflow-managed test spec, create or request the change pack before claiming `Recording status: recorded`.

An isolated advisory review may remain chat-only or use an explicit user path, but it does not establish formal implementation eligibility.

### Staleness and re-review

An approved review becomes stale after a substantive test-spec change. Substantive changes include requirement or acceptance-criterion mappings, test-case additions, removals, or meaning changes, example or edge-case coverage, validation commands, fixtures or test data, manual proof procedures, milestone mapping, automation levels, pass/fail criteria, and non-goal treatment.

Formatting, typo, link-only edits, heading fixes, and list reordering do not automatically require re-review when a reviewer or workflow check confirms that proof obligations are unchanged.

When a `test-spec-review` routes to `spec revision`, `architecture revision`, or `plan revision`, the spec should define whether the reviewed test spec remains the active proof map, is marked stale pending upstream revision, or is replaced after the upstream artifact changes. The test-spec-review gate should not silently treat a proof map as implementation-eligible after the upstream contract it maps to changes.

The first slice may use tracked review evidence and change comparison rather than introducing a new content-hash schema.

## Expected Behavior Changes

- Formal workflow-managed test specs receive independent review before implementation.
- Implementation is blocked when the latest review is missing, stale, or not approved.
- Test-spec state and review status remain separate.
- Weak requirement coverage and vague proof commands are found before code is written.
- Plan-review, code-review, and verify retain their existing ownership.
- Isolated manual skill use remains possible without false lifecycle claims.
- Formal findings are recorded under the change pack.
- Generated skill packages include `test-spec-review`.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| Workflow stage graph | Adds a review stage between `test-spec` and `implement`. |
| Published skill inventory | Adds `test-spec-review`. |
| Test-spec skill | Changes downstream routing. |
| Implement skill | Adds an upstream gate. |
| Review assets | Adds result and finding skeletons. |
| Lifecycle and review validators | Add stage/result support. |
| Workflow guide and spec | Add review ownership and placement. |
| Generated adapters | Include the skill and assets. |
| Runtime application code | No expected change. |

Architecture assessment is recommended because the change affects the lifecycle graph, public skill inventory, routing, validators, and generated packages.

A new ADR is required only if implementation introduces a novel review engine or routing mechanism rather than using the established review-family pattern.

## Testing and Verification Strategy

Likely checks:

| Check ID | What is verified |
| --- | --- |
| `TSR-001` | Published skill frontmatter is normalized. |
| `TSR-002` | Workflow role has the correct upstream and downstream boundaries. |
| `TSR-003` | Standard workflow order includes `test-spec-review` before `implement`. |
| `TSR-004` | `test-spec` routes to `test-spec-review`. |
| `TSR-005` | `implement` blocks without an approved current review. |
| `TSR-006` | Test-spec state remains `active`. |
| `TSR-007` | Complete requirement, example, edge-case, and milestone coverage can receive approval. |
| `TSR-008` | Missing requirement coverage returns `changes-requested`. |
| `TSR-009` | Happy-path-only proof for a failure-bearing requirement returns `changes-requested`. |
| `TSR-010` | A vague manual test returns `changes-requested`. |
| `TSR-011` | A nonexistent or ownerless validation command returns `changes-requested` or `blocked` as specified. |
| `TSR-012` | An upstream spec contradiction routes to spec revision rather than being repaired in the test spec. |
| `TSR-013` | An upstream plan contradiction routes to plan revision. |
| `TSR-014` | Review status and implementation-handoff combinations are validated. |
| `TSR-015` | Formal review records use the change-pack path. |
| `TSR-016` | Material findings update review-log and review-resolution correctly. |
| `TSR-017` | Clean reviews do not require an empty review-resolution artifact. |
| `TSR-018` | A substantive post-review test-spec edit makes the approval stale. |
| `TSR-019` | An isolated review does not auto-start implementation. |
| `TSR-020` | Generated adapters contain the new skill and assets. |
| `TSR-021` | Code-review and verify responsibilities remain unchanged. |

Also create:

```text
docs/changes/<change-id>/behavior-preservation.md
```

with this preservation matrix:

| Surface | Baseline | New proof | Result |
| --- | --- | --- | --- |
| Test-spec authoring | Produces active proof map | Same artifact/status | preserved |
| Plan-review | Approves plan before test-spec | Same responsibility | preserved |
| Implement | Consumes active test spec | Adds approved-review precondition | strengthened |
| Code-review | Reviews implemented code and tests | Same responsibility | preserved |
| Verify | Confirms final evidence and branch readiness | Same responsibility | preserved |
| Test-spec state | `active` | remains `active` | preserved |
| Review evidence | repository-defined | named independent gate | strengthened |
| Generated adapters | no dedicated review skill | new skill packaged | extended |

## Rollout and Rollback

First implementation slice:

- Amend the workflow and review contracts.
- Define result-field and status mappings.
- Add `skills/test-spec-review/SKILL.md`.
- Add result and material-finding assets.
- Update `test-spec` downstream and `implement` upstream wording.
- Update workflow guide/spec.
- Add lifecycle and review-artifact recognition.
- Add formal review-record placement checks.
- Add stale-review behavior where feasible.
- Build canonical skills and validate generated packages for supported targets.
- Prove installed skill self-containment.
- Run representative review proofs against complete, missing-coverage, vague-manual-proof, upstream-contradiction, and stale-review fixtures.
- Update explanation and validation evidence.
- Run final review/verify and prepare PR handoff.

Out of scope for the first slice:

- Historical test-spec migration.
- Automatic test execution.
- Numeric scoring.
- New review service.
- Different-model enforcement.
- Broad test framework redesign.
- Code-review or verify redesign.

Rollback:

- Remove the stage from workflow routing and restore `test-spec -> implement`.
- Restore `test-spec` and `implement` skill wording together.
- Remove the new skill from generated packages through normal generation.
- Preserve review records already created; mark them historical rather than deleting evidence.
- Remove validator requirements only after restoring the old workflow contract.
- Do not rewrite historical test-spec artifacts.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Adds workflow latency | Keep review focused on proof adequacy and use bounded evidence. |
| Duplicates spec-review | Explicitly prohibit product-contract reapproval. |
| Duplicates plan-review | Review milestone-to-proof mapping, not sequencing approval. |
| Duplicates code-review | Review planned proof before implementation; code-review checks implemented proof. |
| Creates false approval confidence | Approval gates implementation only; it does not claim tests pass. |
| Review becomes a test execution stage | Distinguish configured/planned commands from executed results. |
| Test spec changes after approval | Make substantive edits invalidate the review. |
| Review skill becomes too large | Put structural output in assets; keep detailed rules concise and tabulated. |
| Historical changes lack reviews | Apply forward; migrate only through a separate decision. |
| Generated adapters drift | Add build/package parity validation. |

## Open Questions

| Question | Candidate decision and proposal-review note |
| --- | --- |
| Should the gate be mandatory for every test spec? | Endorsed candidate: mandatory whenever a formal workflow-managed test spec is required; optional for isolated/manual test-spec use that does not claim implementation eligibility. |
| Should test-spec status become `approved`? | Endorsed candidate: no. Keep test-spec `active`; put approval in the separate review record. |
| Should the reviewer execute validation commands? | Endorsed with sharpening: not as a general requirement. Review command ownership, existence, shape, failure semantics, and planned evidence. Execution belongs to implementation, code-review, CI, or verify. If a lightweight command is needed to validate a current-behavior claim, the spec should bound it to low-risk checks such as command resolvability, help text, or dry-run behavior, with no fixture setup, side effects, or network dependence. |
| Should the reviewer be a different model? | Endorsed candidate: require an independent review-stage context and follow the repository's review independence contract. Do not require a different vendor/model in this proposal. Known limitation: until a broader review-family policy changes, independence rests on context separation rather than model/vendor diversity. |
| Should approval allow unresolved conditions? | Strongly endorsed candidate: no conditionally-approved state. A material unresolved condition means `changes-requested`, `blocked`, or `inconclusive`. |
| Should a review automatically start implementation? | Endorsed candidate: no for the review skill itself. The workflow orchestrator may route to implement after an approved, recorded, current review when all other gates are clean. |
| How should stale review be detected? | Endorsed candidate: require re-review after substantive test-spec changes. Use existing tracked review/change evidence in the first slice; add content-hash or structured target-fingerprint validation only if manual staleness checks prove insufficient. The spec should include examples of non-substantive edits such as heading fixes and list reordering. |
| What content is required for `inconclusive`? | New spec-stage question from proposal-review feedback: require the result to name the specific evidence gap and the evidence needed to make review conclusive, so `inconclusive` does not become a soft rejection. |
| What happens to the active test spec after upstream revision routing? | New spec-stage question from proposal-review feedback: define whether routing to `spec revision`, `architecture revision`, or `plan revision` leaves the current test spec active, marks it stale, or requires replacement after the upstream artifact changes. |

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-06-25 | Propose a dedicated review gate. | No existing stage owns independent pre-implementation proof-map adequacy. | Leave ownership repository-defined. |
| 2026-06-25 | Place the gate after test-spec and before implement. | The artifact should exist before review, and review should precede its use. | Fold into plan-review or code-review. |
| 2026-06-25 | Keep test-spec status `active`. | Review approval is separate from artifact settlement. | Add `approved` to test-spec states. |
| 2026-06-25 | Exclude product and architecture reapproval. | The gate should review proof, not reopen approved direction. | Create a combined spec/plan/test review. |
| 2026-06-25 | Preserve code-review and verify as backstops. | Planned proof and implemented/final proof are different responsibilities. | Replace later gates. |
| 2026-06-25 | Require re-review after substantive edits. | Approval should apply to the proof map implementation actually consumes. | Treat review as permanently valid. |
| 2026-06-25 | Bound any review-time command execution carve-out. | The reviewer may need low-risk checks for current-behavior claims, but broad execution would blur the line with code-review and verify. | Let reviewers run arbitrary planned validation during test-spec-review. |
| 2026-06-25 | Track model/vendor diversity as a limitation, not a gate requirement. | Review independence is broader than this proposal and should remain a review-family policy question. | Require a different model or vendor for this stage only. |
| 2026-06-25 | Require actionable `inconclusive` results in the spec. | The outcome should identify missing evidence rather than act as an unlabeled soft rejection. | Leave `inconclusive` content undefined. |
| 2026-06-25 | Route upstream-revision invalidation semantics to the spec. | The proposal identifies the risk, but the exact lifecycle behavior belongs in the follow-on contract. | Let implementation infer whether the active test spec remains usable after upstream change. |

## Next Artifacts

```text
proposal-review
spec: test-spec-review workflow and skill contract
spec-review
architecture assessment
architecture-review, if required
plan
plan-review
test-spec
implementation
code-review
explain-change
verify
pr
```

The proposal changes the standard lifecycle, public skill inventory, review-artifact handling, validators, and generated adapters, so a dedicated spec is required.

Architecture assessment should determine whether the established review-family pattern is sufficient without a new ADR. Potential later proposals include automated stale-review fingerprinting, reusable review-family result-schema validation, risk-tiered test-spec review, and stronger review-model diversity policy if evidence shows they are needed.

## Follow-on Artifacts

None yet

## Readiness

Accepted after clean recorded `proposal-review`. Downstream spec, architecture, and plan artifacts are now present; current workflow state is owned by the active plan.

Core invariant:

```text
Implementation should not begin merely because a test spec exists.

It should begin only when the active test spec has been independently reviewed
as a complete, executable, and traceable proof map for the approved contract and
plan.

The test spec remains active.
The review record carries approval.
Code-review and verify still prove the implementation and final evidence.
```
