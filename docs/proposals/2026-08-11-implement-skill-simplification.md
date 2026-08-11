# Implement Skill Simplification

## Owning change record

`docs/changes/2026-08-11-implement-skill-simplification/change.yaml`

## Problem

The published `implement` skill carries universal implementation policy, repeated orientation and handoff guidance, planned-milestone lifecycle procedure, automation-only review-packet rules, and two overlapping output structures in one common path.

An isolated implementation request therefore loads and navigates procedure that applies only to workflow-managed milestones or armed review-fix loops.
The result is a 395-line, 3,338-word skill with an estimated static cost of 5,977 tokens, even though many invocations need only authority checks, test-first execution, scoped validation, stop rules, and a handoff to `code-review`.

Simple deletion would be unsafe.
Repeated passages currently carry compatibility-sensitive distinctions about test-spec approval, workflow ownership, milestone state, validation failure, review-fix authority, claim boundaries, and final holistic review.

## Goals

- Make isolated, planned-milestone, and armed correction journeys easier to understand by reducing the context each journey actually loads.
- Give each behaviorally significant implementation rule one explicit owner and destination.
- Keep the universal implementation contract self-sufficient in `SKILL.md`.
- Load planned-milestone and automation-only procedure separately, only when each exact invocation condition applies.
- Define a closed profile lattice in which armed implementation automation is valid only inside the same current planned milestone.
- Make one packaged asset the sole owner of repeated implementation-result structure.
- Let that asset serve all profiles through one core group and two omitted-when-inapplicable conditional groups without owning policy.
- Separate semantic rule preservation from literal dependency classification so incidental tests do not freeze prose.
- Preserve deterministic canonical, generated, archived, and installed package behavior across supported adapters.
- Measure loaded context for each invocation profile separately from `SKILL.md` and total package size, and subordinate every size measurement to semantic preservation.

## Non-goals

- Changing the standard workflow stage order or the ownership boundary between `implement`, `workflow`, `code-review`, `verify`, and `pr`.
- Weakening test-first practice, first-pass completeness, validation layering, stop conditions, scope control, milestone review, or claim boundaries.
- Changing the meaning of `smallest scope-complete change`, `first-pass acceptable result`, `review-requested`, or milestone closeout.
- Optimizing `workflow`, review skills, or other published skills in the same change.
- Creating a generic execution framework or a new skill.
- Adding target-agent prompt journeys, transcript grading, model-selection fixtures, or runtime-version evidence.
- Adding a permanent line-count, token-count, prose-quality, or simplicity gate.
- Hand-editing generated public adapter packages or tracking generated skill bodies as authored source.

## Vision fit

fits the current vision

The change makes a central execution skill easier for contributors and agents to inspect and use while preserving the durable evidence, test discipline, review handoff, and resumability that distinguish RigorLoop.
It reduces ceremony that does not improve a given invocation without weakening the traceability chain.

## Context

`skills/` remains the only authored skill source.
A published skill is already treated as a canonical `SKILL.md` plus its explicitly mapped packaged references and assets, with lifecycle and policy ownership remaining at the skill level.

The completed `code-review` simplification demonstrated that progressive disclosure can reduce ordinary-path content while preserving canonical, generated, packed, and installed package parity.
That change also demonstrated the need for a closed rule-disposition ledger, separate common-path and package measurements, independent semantic review, and early inventory of literal vocabulary dependencies.

The current `implement` package maps only the shared boundary-first reference.
Its three largest sections are the boundary-first method at about 607 estimated tokens, first-pass completeness at about 517, and implementation autoprogression at about 477.
Additional repetition exists across the preamble, workflow role, quick guide, purpose, evidence sections, four handoff-oriented sections, stop and claim guidance, and two result structures.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Optimize the `implement` skill next | in scope | Goals and Recommended Direction |
| Make the skill more concise and easier to use | in scope | Problem, Goals, and Expected Behavior Changes |
| Select the best solution rather than applying blind deletion | in scope | Options Considered and Recommended Direction |
| Preserve implementation rigor and workflow behavior | in scope | Non-goals, Recommended Direction, and Risks and Mitigations |
| Close the relationship between planned and armed invocation profiles | in scope | Recommended Direction and Expected Behavior Changes |
| Define profile-specific groups within one result asset | in scope | Recommended Direction and Testing and Verification Strategy |
| Separate semantic preservation from literal compatibility | in scope | Recommended Direction and Testing and Verification Strategy |
| Optimize other large skills | out of scope | Non-goals and Scope Budget |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Inventory and disposition current `implement` rules | core to this proposal | Semantic preservation requires explicit source-to-destination accounting. |
| Consolidate universal common-path prose | core to this proposal | This improves every invocation profile before conditional resources are loaded. |
| Add one planned-milestone implementation reference | core to this proposal | Planned lifecycle procedure is conditional on workflow-managed milestone execution. |
| Add one armed automated review/correction reference | core to this proposal | Review-packet and correction-loop procedure is conditional on explicitly armed automation. |
| Add one implementation-result asset | core to this proposal | Repeated output structure needs one structural owner. |
| Define core, planned, and armed result groups | core to this proposal | One asset needs closed profile applicability without policy leakage. |
| Create separate semantic-rule and literal-compatibility ledgers | core to this proposal | Behavioral preservation and dependency migration require different evidence. |
| Extend existing skill and adapter proof | same-slice dependency | New mapped resources require deterministic package parity. |
| Assess canonical architecture impact | same-slice dependency | The change adds packaged resources but should reuse the existing published-skill package model. |
| Optimize `workflow` | separate proposal | Its routing authority and larger blast radius require an independent decision. |
| Consolidate contracts across all execution and review skills | separate proposal | Cross-skill ownership would exceed this bounded package refactor. |
| Add a permanent simplicity validator | out of scope | Change-local measurements are evidence, not durable product invariants. |

## Options Considered

### O0: Keep the current skill

This avoids compatibility risk and maintenance work.
It leaves the 5,977-token common path, overlapping result structures, repeated handoffs, and automation-only content unchanged.

### O1: Editorial deduplication only

This would consolidate repeated wording while keeping every procedure inline.
It is the smallest structural change and may reduce common-path content by roughly 15–25 percent.
It does not prevent isolated requests from loading planned-work and automation-only procedure.

### O2: Deduplicate and extract only the result asset

This adds one structural owner for output and consolidates common prose.
It should improve maintainability and may reduce common-path content by roughly 20–30 percent.
Workflow-managed procedure would still occupy the ordinary path.

### O3: Consolidate the universal contract, add two conditionally loaded procedure references, and add one output asset

This keeps direct implementation self-sufficient, separates ordinary planned-milestone procedure from automation-only review and correction procedure, and gives each invocation profile an exact resource set.
It applies progressive disclosure at the two real authority boundaries without fragmenting universal policy.
The expected planning range is a 30–45 percent reduction for the isolated profile; every profile is evaluated by its actual loaded context, subject to semantic preservation.

### O4: Split execution, milestone, evidence, automation, and output guidance into three or more procedure references

This could minimize the main file further and enable narrow loading.
It would increase package navigation, resource-map complexity, partial-load risk, and maintenance across several policy fragments.

## Recommended Direction

Choose O3.

Keep a shorter linear `SKILL.md` that owns purpose and trigger, stage authority, prerequisites, test-first execution, the definition of a scope-complete first pass, core validation layering, scope and stop rules, claim boundaries, direct review handoff, exact resource triggers, and required output fields.

Add `references/planned-milestone-implementation.md`.
Load it only when authoritative evidence establishes a current planned workflow-managed milestone owned by `implement`.
It should own change-record milestone inspection, baseline change-pack procedure, state synchronization, planned-milestone handoff procedure, milestone commit convention, and accepted review-fix return to the same milestone.

Add `references/automated-review-correction.md`.
Load it only when durable workflow evidence formally arms automated independent review or a bounded correction loop for that same current change and milestone.
It should own automated adversarial-review packet construction, requirement-fidelity routing metadata, forbidden initial-review context, phase receipts and release conditions, reviewer-declared auto-fix constraints, bounded correction procedure, and the final holistic-review prerequisite for later Phase C work.

Use these invocation profiles as the optimization boundary:

| Profile | Planned milestone | Armed automation | Loaded package content after the change | Success interpretation |
| --- | ---: | ---: | --- | --- |
| `IP0-isolated` | no | no | `SKILL.md` and the result asset; the existing boundary-first reference only when its independent trigger applies | Materially less loaded prose than the current skill, with no universal behavior loss. |
| `IP1-planned` | yes | no | `SKILL.md`, the planned-milestone reference, and the result asset; boundary-first only when triggered | Materially less loaded prose than the equivalent current planned journey; automation-only procedure is absent. |
| `IP2-planned-armed` | yes | yes | `SKILL.md`, both conditional references, and the result asset; boundary-first only when triggered | No unjustified loaded-context growth, and automation authority remains complete and isolated from other profiles. |
| Invalid | no | yes | no conditional procedure | Stop because armed implementation automation requires a current planned milestone. |

`planned_milestone_context` is established by a workflow-managed invocation, a valid active plan, one exact current milestone owned by `implement`, and a milestone state that permits implementation.
`armed_automation_context` additionally requires current durable workflow authorization, the current review or correction mode, matching change and milestone identity, and non-stale authorization evidence.
Conversational wording alone establishes neither predicate.

Missing or ambiguous plan evidence, an armed-but-unplanned combination, or stale or mismatched automation identity stops before conditional procedure is loaded or implementation state is mutated.
A valid planned context without automation loads only the planned reference.
A direct or isolated request loads neither conditional reference.

The result asset is counted when comparing packaged content even though copying its structure into output is distinct from reading policy.
The specification should carry this deterministic measurement convention forward unchanged for before-and-after profile totals.

Keep the compact boundary decision bridge inline and let the existing mapped boundary-first reference own the detailed shared method.

Use this resource ownership model:

| Content | Owner |
| --- | --- |
| Universal authority, prerequisites, tests, validation, stops, claims, and direct handoff | `SKILL.md` |
| Planned milestone inspection, synchronization, commit, and milestone handoff procedure | `planned-milestone-implementation.md` |
| Automated packet, correction, receipt, pause, and promotion procedure | `automated-review-correction.md` |
| Shared boundary method | Existing boundary-first reference |
| Result labels and layout | `implementation-result-skeleton.md` |
| Status meaning, group applicability, and claim authority | `SKILL.md` and the applicable procedure reference, never the asset |

The planned and automation references may point to each other by stable concept or section name, but they should not duplicate governing procedure.
Milestone state and milestone handoff remain owned by the planned reference; automation classification and correction remain owned by the automation reference.

Add `assets/implementation-result-skeleton.md` as the only copy-and-fill implementation-result structure.
It contains three structural groups:

| Group | Profiles | Fields |
| --- | --- | --- |
| Core | every valid profile | status, completed scope, changed artifacts, tests, validation and result, blockers, next stage or handoff, and claim limitations |
| Planned milestone | `IP1-planned`, `IP2-planned-armed` | change and milestone identity, plan identity, milestone state, baseline/change-pack status, milestone validation, commit status, and code-review handoff |
| Armed automation | `IP2-planned-armed` | automation mode, review packet or phase identity, requirement-fidelity routing, correction eligibility and cycle count, rereview requirement, pause or promotion condition, and final holistic-review prerequisite when relevant |

Inapplicable groups are omitted rather than emitted with empty or `not applicable` placeholders, and unfilled placeholders are forbidden.
The asset owns labels and layout only; `SKILL.md` and the references own applicability, status meaning, claim authority, and handoff policy.

Before moving prose, create `docs/changes/2026-08-11-implement-skill-simplification/implement-rule-disposition.yaml` for every behaviorally significant rule and known duplication cluster.
Each entry records a stable rule ID, source locations, behavior, governing requirements, applicable profiles, one disposition, destination, and preservation proof.
The closed dispositions are `retained-inline`, `retained-planned-reference`, `retained-automation-reference`, `asset-owned`, `removed-duplicate`, and `removed-obsolete-with-approved-contract-change`.
Every significant rule receives exactly one disposition; no rule disappears without an explicit destination or approved semantic change.

Separately create `docs/changes/2026-08-11-implement-skill-simplification/implement-literal-compatibility.yaml`.
Each entry records a literal ID, literal, source location, consumers, classification, required semantics, disposition, and replacement when applicable.
The closed classifications are `normative-contract`, `parser-or-package-contract`, `test-only-incidental`, and `obsolete`.
Normative contract literals remain exact unless their governing contract changes; parser or package contracts are preserved or migrated with all consumers atomically; incidental tests are updated instead of owning prose; obsolete literals are removed with evidence.

## Expected Behavior Changes

- Isolated implementation requests encounter a shorter, linear common path with less repeated orientation and handoff prose.
- Planned workflow-managed milestones load the planned-milestone reference but not automation-only procedure.
- Armed automated review or correction is valid only for the same current planned milestone, loads both references, and retains all packet, independence, fix-authority, and final-review constraints.
- Invalid, missing, stale, mismatched, or ambiguous profile evidence stops before conditional procedure or state mutation.
- Implementation outputs use one mapped result skeleton with a universal core and omitted-when-inapplicable planned and automation groups.
- Canonical, generated, archived, and temporary installed packages include identical mapped resources at stable relative paths.
- Status, milestone, validation, stop, claim, and downstream handoff behavior remains unchanged.

## Architecture Impact

The change affects the published `implement` skill package boundary by adding two conditional references and one asset.
It reuses the existing canonical-skill, mapped-resource, adapter-generation, and installed-resource integrity architecture.

No new runtime, dependency, persistent state, selector family, or lifecycle owner is expected.
The complete `implement` package remains the policy owner; references and assets do not become independent stages or governance owners.

After specification review, a bounded architecture assessment should confirm whether the canonical package model already covers this addition.
The expected outcome is `architecture-not-required` because the change adds no runtime, state, service, dependency, lifecycle owner, or package-ownership model.
A bounded architecture documentation update may correct an outdated `implement` resource example or general conditional-reference description.
A new ADR is warranted only if later specification changes the normative definition of a published skill package or gives a reference independent policy ownership.

## Testing and Verification Strategy

Use four proof classes:

1. Deterministic semantic-rule, literal-compatibility, and static-scenario proof that rejects unknown dispositions or classifications before consistency checks.
2. Focused existing skill-validator coverage for inline ownership, exact conditional loading, output-asset ownership, closed vocabulary, claim boundaries, and absence of target-runtime machinery.
3. Existing skill generation and adapter-distribution proof for canonical, generated, archived, and temporary installed resource parity across Codex, Claude, and opencode.
4. Independent semantic review of trigger clarity, authority, prerequisites, test-first sequence, completeness, validation, stops, claims, milestone behavior, output, handoff, and conditional loading.

Representative static scenarios should include `IP0-isolated`, `IP1-planned`, `IP2-planned-armed`, and the invalid unplanned-armed combination, plus missing or stale authority, mismatched change or milestone identity, failing tests, a discovered specification gap, accepted review-fix return, workflow-managed automated review handoff, and an attempted next-milestone transition before review closeout.
Fixtures should prove both required and forbidden resource loads for each profile without executing an agent runtime.
Result fixtures should prove exact core and conditional group applicability, omission of inapplicable groups, placeholder absence, and the asset's lack of policy text.

Inventory existing validator assertions that depend on literal headings, phrases, or capitalization before editing the skill.
This avoids discovering compatibility vocabulary only during final verification.

Use normalized LF canonical authored files, count each unique resource once, and assemble each profile in documented load order.
Report before and after UTF-8 bytes, Unicode whitespace-separated words, and exact resource lists for every invocation profile.
Also report `SKILL.md` lines, words, and bytes; each conditional resource; total package words and bytes; duplicate-cluster owners; inline-template count; and mapped-resource count.
A token estimate is optional secondary evidence only when the existing repository tool is stable and its tool version, vocabulary, and normalization are recorded; the change adds no tokenizer dependency.
The 30–45 percent isolated-profile range is planning evidence, not an acceptance threshold.
Acceptance depends on complete rule disposition, one owner per duplication cluster, material improvement for `IP0-isolated` and `IP1-planned`, justified non-regression for `IP2-planned-armed`, honest total-package accounting, and preserved semantic and lifecycle behavior.

No acceptance command should execute or grade Codex, Claude Code, opencode, or another target-agent runtime.

Use these proposal-level preservation criteria as the basis for the downstream specification:

| ID | Criterion |
| --- | --- |
| `AC-IMPSIM-001` | Exactly three valid invocation profiles exist. |
| `AC-IMPSIM-002` | Armed implementation automation requires a valid current planned milestone. |
| `AC-IMPSIM-003` | Trigger evidence is durable, identity-bound, and not inferred from conversational wording. |
| `AC-IMPSIM-004` | Each conditional reference has exact required and forbidden load cases. |
| `AC-IMPSIM-005` | The result asset has one core and two conditional structural groups. |
| `AC-IMPSIM-006` | Inapplicable result groups and unfilled placeholders are omitted. |
| `AC-IMPSIM-007` | Every semantic rule has exactly one disposition and destination. |
| `AC-IMPSIM-008` | Literal dependencies are classified separately from semantic rules. |
| `AC-IMPSIM-009` | Incidental tests do not become prose-policy owners. |
| `AC-IMPSIM-010` | Profile measurements use one deterministic resource-assembly convention. |
| `AC-IMPSIM-011` | UTF-8 bytes and words are the primary portable metrics. |
| `AC-IMPSIM-012` | No permanent simplicity or tokenizer validator is introduced. |
| `AC-IMPSIM-013` | No target-agent runtime executes during acceptance. |
| `AC-IMPSIM-014` | Canonical, generated, archived, and installed resources retain required parity. |

## Rollout and Rollback

Ship the canonical `implement` package, mapped reference, output asset, validator coverage, and package proof in one atomic change.
Generate adapter output only through existing repository scripts and temporary directories.

Rollback restores the prior complete canonical package and regenerates every derived target from that source.
Do not roll back only `SKILL.md` while leaving new mapped resources or validation expectations in place.

No user data migration, feature flag, external service rollout, or dependency change is expected.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Universal policy moves behind a conditional trigger | Isolated implementations could weaken authority, testing, stops, or handoff behavior. | Define inline and conditional ownership before editing; verify direct scenarios and conduct semantic review. |
| Similar paragraphs encode different behavior | Deduplication could erase planned-versus-isolated or implementation-versus-workflow distinctions. | Use a closed rule ledger with source locations, behavior summaries, and destinations. |
| A conditional trigger is too broad or too narrow | Required procedure may load unnecessarily or fail to load. | Use identity-bound durable evidence, a closed profile lattice, and required and forbidden load fixtures. |
| The output asset becomes a policy owner | Structure and behavioral rules could drift between files. | Keep only fields and layout in the asset; retain policy and claim rules inline. |
| One asset produces meaningless profile fields | Results could contain empty placeholders or automation fields in direct use. | Use one core and two conditional groups; omit every inapplicable group. |
| Literal compatibility dependencies are missed or over-preserved | Regressions could appear late, or incidental tests could freeze prose. | Maintain a literal inventory separate from semantic rules and classify every consumer before editing. |
| Main-file reduction hides a planned-journey regression | A smaller `SKILL.md` could still increase the context loaded by the central milestone journey. | Measure actual loaded resources, words, and bytes for all three invocation profiles before and after. |
| Package growth is hidden by profile improvements | Progressive disclosure could reduce invocation cost while increasing maintenance footprint. | Report every profile and the total package separately, and explain any package growth. |
| Several small resources fragment execution guidance | Agents and maintainers could miss required procedure. | Use exactly two procedure references aligned to distinct authority boundaries and one structural asset. |
| Permanent simplicity checks overfit one change | Future semantic improvements could be blocked by arbitrary prose budgets. | Keep measurements and the rule ledger change-local; reuse only durable structural and package validators. |

## Open Questions

No proposal-level product or ownership questions remain.
The specification will name the exact existing metadata fields that satisfy the selected planned and armed evidence predicates, and implementation discovery will populate the literal consumers.
The bounded architecture assessment will confirm the expected `architecture-not-required` result or identify a documentation-only correction.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-11 | Revise O3 to use separate planned-milestone and armed-automation references, one output asset, and one consolidated universal contract. | The two references align resource loading with distinct invocation and authority profiles while avoiding broad policy fragmentation. | A single reference couples ordinary milestone execution to automation-only procedure; three or more procedure references add unnecessary navigation. |
| 2026-08-11 | Optimize and measure `IP0-isolated`, `IP1-planned`, and `IP2-planned-armed` by their actual loaded resources. | `SKILL.md` size alone cannot establish improvement for planned or armed journeys. | File-only and total-package-only measurements hide invocation-specific regressions. |
| 2026-08-11 | Rename the armed profile to `IP2-planned-armed` and reject unplanned armed automation. | Automation procedure depends on the same current planned milestone authority as implementation and correction. | Allowing an isolated armed mode leaves plan, milestone, and handoff authority ambiguous. |
| 2026-08-11 | Structure the single result asset as one core group plus planned and armed conditional groups. | Closed groups preserve one structural owner without empty fields or policy leakage. | Separate assets duplicate the core; one flat asset cannot express profile applicability cleanly. |
| 2026-08-11 | Separate semantic-rule disposition from literal-compatibility classification. | Behavioral policy and incidental text consumers require different preservation decisions. | A combined ledger risks treating tests as prose-policy owners. |
| 2026-08-11 | Use words and UTF-8 bytes as primary profile metrics and tokens only as optional pinned evidence. | Words and bytes are portable and deterministic across target agents. | A new tokenizer dependency would create a permanent mechanism for change-local evidence. |
| 2026-08-11 | Treat 30–45 percent as a planning range rather than an acceptance threshold. | Semantic and lifecycle preservation take precedence over numeric optimization. | A hard threshold could encourage unsafe deletion or concealment. |
| 2026-08-11 | Exclude target-agent runtime acceptance. | Deterministic package proof and independent semantic review establish the relevant contract without creating a model-behavior test system. | Prompt journeys and transcript grading are nondeterministic and outside repository ownership. |

## Next Artifacts

- Formal proposal review.
- Contract-level feature specification after proposal approval.
- Architecture assessment after approved specification review, followed by architecture work only when required.
- Execution plan and traceable test specification after the governing contract and architecture decision are stable.

## Follow-on Artifacts

None yet

## Readiness

Ready for `proposal-review` R4.
The proposal settles the profile lattice and trigger evidence, result-group applicability, semantic-versus-literal preservation boundary, portable measurement convention, and expected architecture outcome.
Only downstream specification field mapping, literal inventory population, and bounded architecture confirmation remain.
