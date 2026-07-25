# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Target: specs/single-bounded-review-fix-workflow-automation.md
Reviewed artifact: specs/single-bounded-review-fix-workflow-automation.md
Review date: 2026-07-21
Reviewer: Codex spec-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: `BRF-SR1`, `BRF-SR2`, `BRF-SR3`, `BRF-SR4`, `BRF-SR5`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/spec-review-r1.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: repeated targets are not deterministically bound; durable state and capability vocabularies are incomplete; verification authorization timing is underspecified; compatibility aliases and supersession boundaries remain ambiguous
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: revise the spec, close `BRF-SR1` through `BRF-SR5`, and record an approving same-stage rereview before architecture or test-spec work relies on the contract

## Review Inputs

- Spec: `specs/single-bounded-review-fix-workflow-automation.md`
- Accepted proposal: `docs/proposals/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism.md`
- Proposal approval: `docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/proposal-review-r4.md`
- Governing contracts: `CONSTITUTION.md`, `specs/rigorloop-workflow.md`, `specs/workflow-stage-autoprogression.md`, `specs/review-fix-autoprogression.md`, `specs/review-finding-resolution-contract.md`
- Operating and boundary context: `docs/workflows.md`, `docs/project-map.md`, `AGENTS.md`

## Findings

## Finding BRF-SR1

Finding ID: BRF-SR1
Severity: major
Location: `BRF-R004`, `BRF-R009` through `BRF-R013`, `BRF-R081` through `BRF-R084`, and `BRF-AC002`/`BRF-AC017`
Evidence: The only public command shape accepts a bare stage, while the persisted target must contain an occurrence. The spec permits all three occurrence kinds for every stage and requires a milestone ID for `implement` or `code-review` only if an implementation chooses `milestone`. It never requires those repeated stages to use `milestone`, never defines how `$workflow auto: implement` or `$workflow auto: code-review` selects the milestone before persistence, and never rejects `singleton` or `final` occurrences for those stages. An implementation could therefore bind the same command to the current milestone, the next milestone, or an invalid singleton while still satisfying the written requirements.
Required outcome: Define a closed stage-to-occurrence compatibility matrix and a deterministic command-to-occurrence binding rule so every public command resolves to one valid structured target before authorization or run state is persisted.
Safe resolution path: Require `implement` and `code-review` to use `occurrence.kind: milestone`; bind a bare repeated-stage command to the active plan's current in-scope implementation milestone at command evaluation time; persist that milestone ID and completion predicate; reject or pause before persistence when no unique current milestone exists; require singleton occurrence for singleton public stages and final occurrence for `verify`; and add normal, missing-plan, ambiguous-milestone, invalid-occurrence, and resume-no-rebind acceptance proof.
needs-decision rationale: none; the accepted proposal already requires repeated targets to bind deterministically to a milestone occurrence before persistence.

## Finding BRF-SR2

Finding ID: BRF-SR2
Severity: major
Location: `BRF-R003`, `BRF-R007` through `BRF-R008`, `BRF-R024`, `BRF-R032` through `BRF-R036`, `BRF-R079`, and observability
Evidence: The spec requires unknown `status` and `capability kind` values to fail closed, but it never defines the closed automation-run status set, parent-authorization status set, effective-capability status set, or capability-kind set. It also allows `$workflow auto: off` to "cancel or disable" without selecting one durable state transition. Terms such as `active`, `paused`, `completed`, `cancelled`, `revoked`, and `invalidated` appear behaviorally, but their legal combinations and terminality are not specified. Validators, status output, cancellation, resume, and the typed stage registry cannot be implemented exhaustively from this contract.
Required outcome: Define distinct closed vocabularies and transition invariants for automation runs, parent authorizations, effective capabilities, and capability kinds, including one deterministic `$workflow auto: off` result.
Safe resolution path: Add normative closed sets and a transition table for each durable record type; define which states are active, resumable, and terminal; define whether pause belongs to the run, capability, or both; bind every automatable stage policy to one enumerated capability kind; require `off` to persist one named cancellation state and propagate invalidation to executable children; and add unknown-value plus illegal-transition acceptance proof for every set.
needs-decision rationale: none; the proposal and repository closed-vocabulary rule already require exhaustive durable types rather than implicit prose states.

## Finding BRF-SR3

Finding ID: BRF-SR3
Severity: major
Location: `BRF-R024` through `BRF-R030`, `BRF-R043`, examples, and `BRF-AC004` through `BRF-AC009`
Evidence: The spec correctly prevents a verification capability from materializing without implementation-closeout evidence, but it does not constrain when a verification parent authorization may be persisted. Because a parent authorization is explicitly allowed to be durable maximum consent rather than executable authority, the written contract permits a future-contingent verification authorization at implementation start. The accepted proposal settles the stricter rule: implementation and verification use separate durable parent authorizations, and one interaction may authorize both only when the complete prerequisites and basis identities for both effective capabilities already exist and validate independently.
Required outcome: Carry the accepted proposal's verification-authorization timing rule into the normative contract and distinguish an eventual `verify` target from current verification consent.
Safe resolution path: Add requirements that a run may target `verify` before verification authority exists, but a verification parent authorization cannot be created from future-contingent consent; it may be persisted only when closed milestones, final-review evidence, promotion evidence, current explanation inputs, and branch-state verification inputs are concrete and independently valid. Require a pause at the verification boundary otherwise, and add tests contrasting early target persistence, early verification-authorization rejection, and valid same-interaction implementation-plus-verification authorization after both bases exist.
needs-decision rationale: none; this timing decision is explicit in the accepted proposal's open-question resolution.

## Finding BRF-SR4

Finding ID: BRF-SR4
Severity: major
Location: `BRF-R005`, `BRF-R091` through `BRF-R098`, `BRF-AC026`, and compatibility lines 416-417
Evidence: The accepted proposal lists support for existing public command forms through adapters as a goal and defers their removal to a separate compatibility policy. The spec weakens that to aliases that `MAY` remain and provides no mapping for `auto-through: plan-review` or `auto-through: verify`. This conflicts with `BRF-AC026`, which assumes compatibility adapters preserve historical command meaning, and leaves old-client behavior undefined during the dual-read migration. In particular, `auto-through: verify` previously authorized a separately persisted implementation profile, while the new contract forbids early verification authority; an adapter needs an explicit target and authorization-boundary result rather than an unspecified "same structured target."
Required outcome: Define the compatibility window and an exhaustive old-command mapping that preserves supported user intent without recreating legacy writers or violating the new authorization boundaries.
Safe resolution path: Change compatibility support during the migration window from `MAY` to `MUST`; map `auto-through: plan-review` to structured `plan-review` plus bounded authoring authorization; map `auto-through: verify` to structured final `verify` plus only the risk-class authorization whose concrete basis currently exists, with later boundary pauses and separate verification authorization; map legacy status/off forms to the unified run; define unknown/deprecated alias behavior; and require a separately approved compatibility change before alias removal.
needs-decision rationale: none; the accepted proposal already chooses adapter compatibility and separate risk-class authorization.

## Finding BRF-SR5

Finding ID: BRF-SR5
Severity: major
Location: `Compatibility and migration`, especially the supersession table at lines 399-406
Evidence: The table names some exact ranges but also uses open-ended phrases such as "profile-local state/target compatibility statements" and "compatibility statements that keep" legacy mechanisms writable. It omits directly conflicting requirements outside those ranges. For example, `specs/workflow-stage-autoprogression.md` `R2g` permits review-to-next-authoring continuation only inside `authoring-through-plan-review`, while `R2w` through `R2al` preserve required authoring behavior using the retired profile as their subject. The new table supersedes `R2h` through `R2v` but neither supersedes nor normatively rebinds `R2g` and `R2w` through `R2al`. Same-rank approved specs would therefore give incompatible answers after this draft becomes approved.
Required outcome: Make cross-spec precedence exhaustive enough that every retained legacy requirement has one deterministic status: superseded, preserved unchanged, or preserved with its subject rebound to the unified mechanism.
Safe resolution path: Replace open-ended supersession phrases with an exact requirement/acceptance mapping, including `R2b`, `R2g`, `R2w` through `R2al`, relevant inputs/outputs and acceptance criteria, and corresponding `rigorloop-workflow` and review-fix references; alternatively amend the affected approved specs in the same spec revision. State explicitly that preserved safety predicates apply to the matching unified stage policy or authorization class, not to a still-writable retired profile. Add a static cross-spec contradiction check to acceptance coverage.
needs-decision rationale: none; exact supersession is required by repository source precedence and the proposal already chooses single-write unified state.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | block | Repeated-target binding and durable state transitions are not uniquely defined. |
| normative language | concern | `MAY` compatibility and "cancel or disable" weaken otherwise mandatory behavior. |
| completeness | block | Verification authorization timing and several closed vocabularies are missing. |
| testability | block | Invalid stage-occurrence pairs, illegal state transitions, early verification consent, and alias behavior cannot be tested exhaustively. |
| examples | concern | Strong recovery and proposal-review examples exist, but cancellation, legacy aliases, and repeated-command binding are absent. |
| compatibility | block | Alias support is optional and same-rank supersession leaves contradictory legacy requirements. |
| observability | concern | Required status reporting exists, but the statuses and their transition meanings are not closed. |
| security/privacy | concern | External actions and path scope are safe, but future-contingent verification authorization remains permitted by omission. |
| non-goals | pass | External actions, background execution, blanket authority, and immediate command removal are clearly excluded. |
| acceptance criteria | block | The criteria do not prove stage-occurrence compatibility, closed durable states, verification authorization timing, or exact cross-spec precedence. |

## Exact Wording Suggestions

- Add: `implement` and `code-review` targets MUST use `occurrence.kind: milestone` and MUST bind the unique current in-scope milestone from the active plan before target persistence.
- Add closed tables for run status, parent-authorization status, capability status, capability kind, legal transitions, and terminality.
- Add: a final `verify` target MAY exist before verification authority, but verification parent authorization and capability MUST NOT be persisted until their concrete basis exists.
- Replace optional alias compatibility with a mandatory migration-window mapping for `auto-through: plan-review`, `auto-through: verify`, status, and off.
- Replace descriptive supersession phrases with exact requirement IDs or amend the affected approved specs so no legacy profile remains the exclusive subject of preserved behavior.

## Recommendation

Review status is `changes-requested`.
The immediate next stage is spec revision, followed by same-stage `spec-review-r2`.
Eventual test-spec readiness is `not-ready` until all five findings are closed.
This direct review is isolated and performs no automatic downstream handoff.
