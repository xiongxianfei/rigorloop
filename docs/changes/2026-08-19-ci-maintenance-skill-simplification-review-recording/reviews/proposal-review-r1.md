# Proposal Review: CI-Maintenance Skill Simplification

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex independent proposal-review context
Target: `docs/proposals/2026-08-19-ci-maintenance-skill-simplification.md`

Reviewed artifact: `docs/proposals/2026-08-19-ci-maintenance-skill-simplification.md` at `sha256:6515d39164d65f82aa5b4dffe9beb48c79dabd346b62f9691e4aafa1a0eedc4a`
Review date: 2026-08-19
Recording status: recorded
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: CIMSIM-PR1, CIMSIM-PR2, CIMSIM-PR3
- Open blockers: target-kind compatibility, privileged approved-design authority, and hosted-CI claim ownership require proposal decisions
- Proposal readiness: not ready for specification
- Immediate next stage: proposal revision followed by same-stage proposal rereview
- Automatic downstream handoff: none
- Claim limitations: this isolated review records judgment only; it does not settle the portable proposal, activate a governed change, authorize specification, or continue workflow

## Overall assessment

The selected package shape is proportionate:

```text
compact universal SKILL.md
+ one GitHub workflow-authoring reference
+ the existing risk-to-check map
+ a safer existing workflow skeleton
+ no scripts
```

Separating operation, concern, provider, privilege context, and structure mode addresses the current overloaded classifier. The resource boundaries are also credible: narrow review can remain root-only, coverage reasoning earns the risk map, create and revise earn authoring procedure, and copied YAML structure is needed only for creation or explicit structural replacement.

The proposal is especially strong in keeping command ownership, least privilege, secret and fork safety, dangerous-event detection, write authority, stops, and claims inline. It makes review read-only, binds mutation to exact target identity, rejects managed-region parsing, preserves historical workflows, and requires every actual loaded assembly and package-parity surface to remain visible.

Three contracts still need proposal-level closure. The first-version target model silently drops existing validation-automation and related-platform-configuration authoring. The privileged classifier does not represent read-only review or implementation under an already approved hardened design. The result model permits hosted-CI pass and failure claims that the proposal and current skill expressly prohibit.

## What is strong

### The progressive-disclosure boundary is real

Detailed GitHub authoring, coverage mapping, and copied YAML structure have different triggers. The proposal represents those triggers independently and requires late resource loading before dependent judgment or mutation.

### Universal safety remains self-sufficient

The root retains exact target resolution, authoritative commands, coverage-gap detection, least privilege, secret and fork safety, third-party action provenance, resource selection, stops, and claim limits. A missing optional resource therefore cannot weaken narrow review safety.

### Operation and concern are correctly separated

`create`, `revise`, and `review` are target-state-bound operations. Performance, caching, permissions, triggers, coverage, and ordinary hardening are independent concerns. Review correction begins a fresh revision rather than acquiring mutation authority.

### Structural ownership is bounded

The reduced skeleton owns YAML shape and placeholders without owning trigger, command, cache, permission, action-version, or coverage policy. Historical workflows are not migrated merely to adopt it.

## Material findings

### CIMSIM-PR1 - The target model silently narrows existing CI-maintenance scope

Finding ID: CIMSIM-PR1
Severity: major
Location: `Non-goals`, `Use a closed provider classification`, `Use one atomic single-file write protocol`, and `Preserve truthful results and ownership`
Evidence: The current public skill authors or reviews “GitHub Actions workflows, validation automation, and related platform configuration.” The proposal limits first-version authoring to GitHub Actions, describes every mutation as exactly one workflow-file write, and states that `ci-maintenance` writes only the exact CI infrastructure file. It does not classify project-owned validation automation or related platform configuration as target kinds, define who authors them, or declare a compatibility migration. An optimization proposal therefore silently removes supported behavior while claiming to preserve the current stage contract.
Required outcome: Close the target-kind model and preserve, replace, or explicitly migrate every current public target class.
Safe resolution path: Add an independent target-kind classifier such as `github-workflow`, `project-validation-automation`, and `related-platform-configuration`. Keep the proposed GitHub resource assemblies for `github-workflow`. For the other kinds, define evidence-bound read-only review and either a bounded current authoring contract or an explicit replacement owner and compatibility route. If each mutation remains single-file, say that multi-target requests decompose into separately authorized operations and cannot claim atomic group completion.
needs-decision rationale: none; this can be closed without changing the selected package boundary.

### CIMSIM-PR2 - Privileged context lacks an approved-design authority path

Finding ID: CIMSIM-PR2
Severity: major
Location: `Non-goals`, `Separate ordinary from privileged workflow context`, `Expected Behavior Changes`, and `Decision Log`
Evidence: The current skill declines privileged workflow design and stops when deployment, publishing, privileged permissions, secrets, self-hosted runners, or `pull_request_target` lack a separate design. It can still review such files and implies that bounded implementation may proceed under an approved hardened design. The proposal instead makes every privileged signal select `privileged-design-required`, says privileged workflow contexts stop before authoring, and does not state whether read-only review remains available. That conflates three states: review, design invention without authority, and implementation under current approved design.
Required outcome: Define a closed operation-by-privileged-authority matrix that preserves read-only review and distinguishes missing design from valid implementation authority.
Safe resolution path: Allow `review` to remain read-only for privileged targets and record findings. For `create` or `revise`, require one exact current approved design, target identity, and bounded implementation authority; without them, stop and route to the design owner. Keep `ci-maintenance` prohibited from creating the hardened design or broadening permissions beyond it.
needs-decision rationale: none; the authority matrix can be added without a new resource or owner.

### CIMSIM-PR3 - Hosted-CI result values exceed the skill claim boundary

Finding ID: CIMSIM-PR3
Severity: major
Location: `Non-goals` and `Preserve truthful results and ownership`
Evidence: The proposal says running validation, waiting for CI, and claiming hosted CI passed are non-goals. It later makes `hosted CI status` a result field with `pending`, `passed`, `failed`, and `unavailable`. The current skill explicitly must not claim hosted CI pass status. Even when observed elsewhere, projecting those states into the CI-maintenance result expands this stage into external-check observation and blurs verification and PR ownership.
Required outcome: Keep the result limited to CI-maintenance-owned authoring or review evidence and prohibit hosted execution-status claims.
Safe resolution path: Replace the hosted-status vocabulary with a fixed statement such as `hosted CI observation: not performed by ci-maintenance`, or omit the field. Report only static configuration validation actually performed, commands referenced but not executed, authored/reviewed target identity, coverage judgment, blockers, and tradeoffs. Leave hosted check observation and readiness to their existing owners.
needs-decision rationale: none; the result contract can be corrected directly.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The overloaded classifier, flat authoring procedure, and over-capable skeleton are concrete. |
| User value | pass | Narrow reviews and revisions should load materially less unrelated procedure. |
| Option diversity | pass | Flat, compressed, catch-all, two-resource, fragmented, and executable alternatives are meaningfully different. |
| Decision rationale | pass | One authoring reference, the existing map, and the existing asset match real activation boundaries. |
| Vision fit | pass | The direction reduces ceremony while preserving reviewable Git-tracked automation and human judgment. |
| Scope control | concern | Validation automation and related platform configuration disappear from the supported authoring model without a migration decision. |
| Universal safety | pass | Commands, coverage, permissions, secrets, provider signals, stops, and claims remain inline. |
| Operation model | pass | Create, revise, and review are target-state-bound; concerns are independent. |
| Resource model | pass | Review, coverage, authoring, and structural resources have explicit independent triggers. |
| Privileged authority | block | Review and approved-design implementation are conflated with unapproved privileged design. |
| Claim ownership | block | Hosted-CI execution states exceed the stage's claim boundary. |
| Mutation and recovery | pass with revision | Atomic single-file replacement is sound for a single target after target kinds and multi-target decomposition are closed. |
| Measurement | pass | Every declared assembly and complete package remain visible, including both structural-revision variants. |
| Testing boundary | pass | Static fixtures and package parity are proportionate; live CI and agent runtime are excluded. |
| Architecture awareness | pass with revision | No architecture work is expected if target preservation and authority fit existing contracts. |
| Readiness for spec | changes-requested | Resolve CIMSIM-PR1 through CIMSIM-PR3 and pass same-stage rereview. |

## Scope Preservation Review

- Scope-preservation result: changes requested; the scope budget is explicit, but two existing public target classes are neither retained nor assigned a compatibility route.

## Recommended Proposal Edits

- Add a closed target-kind classifier and one-target-per-operation or explicit multi-target decomposition rule.
- Add a privileged operation/authority matrix covering read-only review, missing design, current approved design, and ambiguous authority.
- Remove hosted execution states from the CI-maintenance result and state which owner observes hosted checks.
- Add deterministic acceptance criteria for the new matrices and claim boundary.
- Rerun independent proposal review against the revised artifact identity.

## Recommendation

- Recommendation: changes-requested. Retain the package direction, revise the proposal to close CIMSIM-PR1 through CIMSIM-PR3, and perform a new isolated proposal review. No automatic downstream handoff follows.

## Specialized-gate group

- Active gate predicates: `scope_budget_context`
- Gate outcomes: changes requested; directly coupled package work is classified, but current public target coverage is incomplete
- Trigger ambiguity: none

## Durable-recording group

- Recording status: recorded
- Recording blocker: none
- Record path: `docs/changes/2026-08-19-ci-maintenance-skill-simplification-review-recording/reviews/proposal-review-r1.md`
- Finding-record paths: this detailed review record and `review-resolution.md#proposal-review-r1`

## Formal-settlement group

- Review ID: `proposal-review-r1`
- Review record: `docs/changes/2026-08-19-ci-maintenance-skill-simplification-review-recording/reviews/proposal-review-r1.md`
- Review log: `docs/changes/2026-08-19-ci-maintenance-skill-simplification-review-recording/review-log.md`
- Review resolution: `docs/changes/2026-08-19-ci-maintenance-skill-simplification-review-recording/review-resolution.md#proposal-review-r1`
- Proposal settlement: not-settled; the recording-only root has no proposal lifecycle authority
- Governed change identity: none; recording-only root `2026-08-19-ci-maintenance-skill-simplification-review-recording`
- Formal next-stage eligibility: blocked pending proposal revision and approving rereview
