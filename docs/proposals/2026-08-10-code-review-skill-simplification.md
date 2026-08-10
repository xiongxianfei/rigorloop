<!-- Template: proposal-skeleton-v1 -->
<!-- Skill: proposal -->

# Simplify the Published Code-Review Skill

## Owning change record

`docs/changes/2026-08-10-code-review-skill-simplification/change.yaml`

## Problem

The published `code-review` skill has grown to 518 lines and 4,514 words in its common-path `SKILL.md`, with another 149 lines and 1,055 words in packaged resources.
The common-path body repeats its inputs, evidence-selection rules, claim boundaries, status handling, milestone routing, and output shape across several sections.
It also loads detailed workflow-managed automation rules for every invocation even though direct and isolated reviews do not use those rules.

This growth makes the skill harder to scan and increases the chance that duplicated instructions drift or conflict.
The problem is not that the review contract is too rigorous; it is that the same rigor is expressed repeatedly and specialized policy is loaded outside the situations that need it.

## Goals

- Make the common review path shorter and easier for an agent or maintainer to follow.
- Preserve all behaviorally significant review, evidence, recording, isolation, stop, claim-boundary, and milestone-handoff rules.
- Give each repeated rule one clear owner inside the skill package.
- Load workflow-managed automation and other specialized guidance only when its trigger applies.
- Keep the published package portable, deterministic, self-contained, and semantically reviewable.
- Measure both common-path reduction and total packaged-content movement so that relocation is not misreported as deletion.

## Non-goals

- Reduce rigor, weaken independent review, or remove direct-proof obligations.
- Change review status vocabulary, severity meaning, review settlement, lifecycle stage order, or workflow automation behavior.
- Simplify every RigorLoop skill in the same change.
- Remove required core sections, frontmatter, the Resource map, or governed recording policy merely to meet a line target.
- Hand-edit generated adapter packages or installed skill copies.
- Treat line count or token count as proof that the revised skill is better.
- Execute Codex, Claude Code, opencode, or another model runtime to prove the simplification.
- Introduce prompt journeys, model-selection fixtures, transcript grading, runtime-version evidence, a permanent token or line-count gate, or a prose-quality score.
- Implement the simplification before an approved spec, test spec, architecture decision when triggered, and execution plan exist.

## Vision fit

fits the current vision

The change makes a core workflow artifact easier to inspect, trust, and continue using without weakening the traceability chain that differentiates RigorLoop.
It also supports the vision's refusal of process cost that does not improve review quality.

## Context

`skills/code-review/SKILL.md` is currently the repository's largest published skill.
The main file exceeds the general skill-authoring recommendation of fewer than 500 lines and contains several repeated instruction clusters:

- the 27-line quick guide restates mandatory core sections;
- evidence access is split across Inputs, Evidence access, Change-record bounded reads, Evidence collection efficiency, and full-file guidance;
- claim boundaries appear in at least six locations;
- handoff behavior is repeated across Handoff, workflow handoff, milestone handoff, review evidence, and the output contract;
- the output assets are mapped but large inline templates are still repeated;
- the boundary-first method is both packaged as a reference and substantially restated inline; and
- automated independent-review and requirement-fidelity policy is always loaded despite its conditional workflow-managed trigger.

The approved skill contract requires the normalized core sections, review vocabulary, checklist and finding semantics, recording behavior, claim boundaries, summary-first output, and mapped packaged resources.
It also prefers references for future `code-review` packaged-resource proposals unless repeated output structures justify assets.
The published-skill-first simplification contract keeps semantic skill quality in review rather than turning prose quality into a deterministic scoring gate.

## Options Considered

### O1: Keep the skill unchanged

Avoids migration risk and preserves the exact current text.
It leaves the largest skill above the recommended common-path size, keeps duplicated policy vulnerable to drift, and does not improve ordinary review usability.

### O2: Deduplicate prose only within `SKILL.md`

Merge repeated sections and remove duplicate templates while keeping all policy in the main file.
This is low risk and produces a meaningful reduction, but specialized automation policy would still burden every direct review invocation.

### O3: Consolidate the core and progressively disclose conditional policy

Keep the mandatory review contract and code-review-specific decision rules in `SKILL.md`, use existing assets as the single structural output source, retain only a compact code-review-specific boundary-first bridge, and move workflow-managed automation detail into one explicitly mapped conditional reference at `skills/code-review/references/workflow-managed-automated-review.md`.
Measure common-path and total packaged content separately and require semantic preservation review.

This option best addresses both duplication and unnecessary common-path loading without disguising moved content as removal.

### O4: Rewrite the skill as a short generic code-review checklist

Would achieve the largest size reduction, but it would discard lifecycle recording, milestone settlement, evidence authority, direct proof, independence, and workflow-managed review gates.
It is rejected because those rules are the specialized behavior the skill exists to provide.

## Recommended Direction

Choose O3.

Restructure the skill around one compact operating sequence:

1. establish the review surface and governing authority;
2. inspect the diff, contract, tests, and targeted proof;
3. apply the required checklist and any triggered specialized review guidance;
4. record findings or a clean receipt before downstream action;
5. emit one status and one milestone-aware handoff.

Retain every required core heading, but remove the separate Quick operating guide because it duplicates them.
Consolidate evidence-reading guidance into one section, claim limits into the required claim-boundary section, and routing into one status-to-handoff table plus the required Handoff and Stop conditions summaries.
Use the mapped assets as the only copy-and-fill output structures rather than reproducing their fields in inline templates.

Keep the shared Isolation and Recording policy byte-consistent while its governing contract requires that shared form.
Keep the published-skill semantic-review checklist because it protects the repository's current product boundary.
Keep code-review-specific boundary-first triggers and finding behavior in the main skill, while relying on the mapped boundary reference for the shared vocabulary and method.

Create exactly one automation-policy reference:

```text
skills/code-review/references/workflow-managed-automated-review.md
```

Map it from `SKILL.md` with an exact `READ` trigger for a formally armed workflow-managed automated review or correction loop.
The complete governing published skill is the `code-review` package: canonical `SKILL.md` plus explicitly mapped packaged references and structural assets.
The reference does not become a separate lifecycle, policy, review, or readiness owner; ownership remains at `code-review`.

Keep the following universal contract inline:

| Inline contract | Reason |
| --- | --- |
| Purpose, trigger, workflow role, and stage ownership | Required before any reference is loaded. |
| Review-surface and governing-authority resolution | Required for every review. |
| Core checklist, review statuses, severity, and material-finding fields | Defines universal review behavior. |
| Isolation and recording policy | Applies to every formal or isolated review. |
| Direct-proof obligation and universal stop conditions | Must act before optional procedure. |
| Claim boundaries and status-to-handoff behavior | Must never depend on conditional loading. |
| Milestone-local versus final-review distinction | Core `code-review` behavior. |
| Resource-map entry and exact load trigger | Makes progressive disclosure reliable. |
| Compact boundary-first bridge | Tells the reviewer when shared method guidance applies. |

Move only workflow-managed automation procedure:

- automated independent-review phases and packet handling;
- requirement-fidelity gate procedure;
- automation-only risk-tier and review checks;
- reviewer-owned auto-fix classification;
- bounded correction and rereview loops;
- automation-specific phase receipts, promotion, pause, and failure handling.

Do not move material-finding meaning, `changes-requested` semantics, downstream blocking, claim limits, formal recording, or the requirement to rereview changed code.

Require a change-local rule-disposition ledger at:

```text
docs/changes/2026-08-10-code-review-skill-simplification/code-review-rule-disposition.yaml
```

Every behaviorally significant current rule or repeated rule cluster receives a stable ID, source locations, behavior summary, governing requirement references, one destination, and exactly one closed disposition:

```text
retained-inline
retained-conditional-reference
asset-owned
removed-duplicate
removed-obsolete-with-approved-contract-change
```

No rule may disappear without a recorded disposition.

Treat a 35–45 percent decrease in common-path words or tokens as a planning target, not a normative minimum or semantic gate.
Acceptance depends on complete rule disposition, one owner per repeated rule, removal of the identified duplication clusters, material direct-review common-path reduction, honest total-package accounting, and no behavioral loss.
Less than 35 percent remains acceptable when the ledger and semantic review show that further reduction would hide universal policy or weaken clarity; no material reduction means the proposal objective was not met.

## Expected Behavior Changes

- Direct and isolated code reviews encounter a shorter, linear operating contract with less repeated routing and output prose.
- Workflow-managed automated review loads its additional gate procedure only when the exact mapped trigger applies.
- Agents continue to use the same review statuses, checklist dimensions, material-finding fields, recording duties, stop conditions, and milestone outcomes.
- Review outputs continue to use the packaged result and finding assets.
- Users and maintainers can distinguish content that was removed as duplication from content moved behind progressive disclosure.
- Direct and isolated review remains performable from `SKILL.md` without loading the automation reference.

No review outcome, lifecycle transition, or downstream authority is intended to change.

## Architecture Impact

The primary boundary is the governing `code-review` skill package: canonical `SKILL.md`, its explicitly mapped assets and references, and generated adapter archives.
No runtime service, persistent data model, or external API changes.

The conditional automation guidance becomes a new packaged reference, so adapter generation and validation must preserve its path and bytes for every supported target.
The canonical source remains `skills/code-review/`; generated packages remain derived output.

The specification must identify the ownership boundary between:

- common-path stage policy that remains visible in `SKILL.md`;
- shared method detail owned by mapped references;
- copied structural output owned by assets; and
- repository-maintainer validation or packaging guidance that must not appear in published skill text.

An architecture assessment is required after proposal approval because this change formalizes a policy-bearing packaged reference and its generated-package boundary.
A new ADR is required only if existing published-skill resource-integrity architecture does not already establish that mapped policy references remain part of the owning skill package.

## Testing and Verification Strategy

Use exactly three acceptance-proof classes.

### Deterministic structural proof

Validate frontmatter, required headings, closed vocabulary values, the Resource map, reference and asset existence and containment, placeholder absence, narrowly forbidden deterministic claims, generated package inventory, and canonical-to-generated resource parity with existing repository-owned checks.

### Fixture-based contract proof

Use static representative invocation records for direct review, formal recorded review, missing authority, material findings, clean non-final milestone, clean final milestone, and workflow-managed automated review.
Each fixture names required and forbidden contract outcomes without starting or grading a model runtime.

For example, a direct review with a material finding requires an identified review surface, complete finding evidence and outcome fields, `changes-requested`, blocked downstream handoff, and no verify-readiness claim; it forbids automatic editing, automatic next-stage invocation, and branch-readiness claims.

### Independent semantic review

Review the final skill package and rule-disposition ledger for trigger clarity, ownership, prerequisites, operating sequence, evidence use, stop conditions, claim boundaries, output usefulness, handoff clarity, and the exact conditional-reference load trigger.

Scenario proof is fixture-based and deterministic.
Semantic preservation is established through independent review of the complete package and its source-to-destination rule ledger.
No Codex, Claude Code, opencode, or other target-agent runtime is part of implementation, verification, release, or acceptance for this change.

Report these before-and-after measurements as change-local evidence, not permanent validation:

| Metric | Purpose |
| --- | --- |
| `SKILL.md` lines and words | Main-file scale and common-path prose size. |
| `SKILL.md` tokenizer count | Approximate loaded-context cost. |
| Conditional-reference words and tokens | Relocated conditional content. |
| Total package words and tokens | True maintenance footprint. |
| Duplicated rule-cluster count | Ownership improvement. |
| Inline-template count | Structural duplication. |
| Mapped-resource count | Package complexity. |

The rule-disposition ledger, size measurements, duplicate-cluster count, and semantic judgment remain change-local evidence.
Do not add a new validator family, token-budget gate, line-count gate, prose-quality score, selector, scheduler, or runtime journey test.

## Proposed Acceptance Criteria

| ID | Criterion |
| --- | --- |
| AC-CRSIM-001 | Every behaviorally significant current rule has one disposition and destination. |
| AC-CRSIM-002 | Universal status, stop, recording, claim, and handoff rules remain inline. |
| AC-CRSIM-003 | Workflow-managed automation procedure lives in one mapped conditional reference. |
| AC-CRSIM-004 | The conditional reference remains owned by the `code-review` skill package. |
| AC-CRSIM-005 | Direct and isolated review can be performed from `SKILL.md` without loading the automation reference. |
| AC-CRSIM-006 | Workflow-managed automated review has an exact reference-load trigger. |
| AC-CRSIM-007 | Output structures are owned only by mapped assets. |
| AC-CRSIM-008 | No target-agent runtime is executed for acceptance. |
| AC-CRSIM-009 | Scenario proof uses deterministic fixtures and independent semantic review. |
| AC-CRSIM-010 | Common-path and total-package metrics are reported separately. |
| AC-CRSIM-011 | The 35–45 percent reduction is a target, not a normative semantic gate. |
| AC-CRSIM-012 | No permanent line-count, token-count, or prose-quality validator is introduced. |
| AC-CRSIM-013 | Generated packages include every mapped reference and asset with required parity. |
| AC-CRSIM-014 | Review status, severity, recording, milestone settlement, and downstream authority remain unchanged. |

## Rollout and Rollback

Deliver the change as one reviewed skill-package revision after spec, architecture assessment, plan, and test-spec approval.
Do not stage a period where `SKILL.md` points to a missing resource or generated packages contain mixed versions.

Roll back by reverting the canonical skill-package revision and regenerating adapter archives from the restored canonical source.
Do not preserve a partially moved policy reference if the main skill is rolled back.

Existing change records and historical review artifacts remain valid because the proposal does not change their schema or status vocabulary.
No runtime acceptance harness or model-version rollback is involved.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Contract compression removes a meaningful condition | Review behavior becomes less safe or less traceable | Require a source-to-destination preservation map and semantic review against governing requirements. |
| Progressive disclosure hides a required stop or claim boundary | An agent may proceed or overclaim before loading the reference | Keep universal stops, claim limits, and load triggers in `SKILL.md`; move only conditionally applicable procedure. |
| Content is moved but reported as eliminated | The project mistakes context relocation for actual simplification | Measure common-path and total packaged content separately. |
| Shared policy drift | Review skills disagree about recording | Preserve the governed Isolation and Recording block unless its owning contract changes first. |
| Package or adapter drift | Installed skills reference absent or stale resources | Use mapped-resource and generated-package parity validation. |
| A numeric target drives unsafe editing | Important rules are removed to meet a budget | Treat reduction as an outcome target subordinate to semantic preservation. |
| Scope expands into repository-wide skill rewriting | Review and rollback become difficult | Limit this proposal to `code-review` and directly governing or generated surfaces. |
| Fixture proof is mistaken for model-behavior certification | Validation expands into nondeterministic runtime testing | State that fixtures prove contract requirements only and exclude every target-agent runtime. |
| The rule ledger becomes a permanent product validator | One-off simplification evidence becomes maintenance burden | Keep the ledger and size measurements change-local and review-owned. |

## Open Questions

None at proposal level.

The specification and plan must inventory the exact existing structural, resource, and package-parity command owners before adding checks, but that inventory does not reopen the selected package model, runtime exclusion, or rule-disposition success criteria.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Quantify how much content the current skill contains | in scope | Problem, Context, Testing and Verification Strategy |
| Identify unnecessary content that can be simplified or removed | in scope | Context, Options Considered, Recommended Direction |
| Preserve important behavior while simplifying | in scope | Goals, Non-goals, Risks and Mitigations |
| Start the work on a new branch | in scope | Owning change record and branch-level execution context |
| Create a proposal | in scope | This artifact |
| Run proposal-review after authoring | in scope | Readiness and Next Artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Consolidate duplicated `code-review` common-path prose | core to this proposal | This is the principal user-value change. |
| Preserve mandatory review and lifecycle semantics | same-slice dependency | Simplification is unacceptable without behavior preservation. |
| Package automation-only guidance in one mapped reference | core to this proposal | This is the selected progressive-disclosure mechanism and remains owned by `code-review`. |
| Update governing skill-contract clauses when required | same-slice dependency | Published behavior cannot diverge from higher-priority approved requirements. |
| Update generated adapter packages or archives | same-slice dependency | Published targets must remain self-contained and byte-consistent. |
| Complete architecture assessment of the policy-reference package boundary | same-slice dependency | The change formalizes policy-bearing mapped content and must confirm whether an ADR is needed. |
| Create a change-local rule-disposition ledger | same-slice dependency | This is the primary semantic-preservation and ownership proof. |
| Simplify other skills | out of scope | A repository-wide rewrite would obscure whether this focused approach works. |
| Retire unrelated token-cost or validation systems | separate proposal | Those systems have broader release and governance ownership. |

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-08-10 | Focus on `code-review` as the first simplification target. | It is the largest current skill and has concrete duplicated clusters. | Repository-wide skill rewrite. |
| 2026-08-10 | Preserve rigor while consolidating ownership. | Review and lifecycle semantics are product behavior, not disposable verbosity. | Generic checklist rewrite. |
| 2026-08-10 | Prefer progressive disclosure for automation-only detail, subject to spec confirmation. | Direct reviews should not load policy that only workflow-managed automation uses. | Inline-only deduplication as the final design. |
| 2026-08-10 | Measure common-path and total packaged content separately. | Moving text is useful for context efficiency but is not the same as removing it. | Reporting only the main-file reduction. |
| 2026-08-10 | Select one mapped `workflow-managed-automated-review.md` reference and keep ownership at `code-review`. | This closes CRSIM-PR1 and makes the primary simplification mechanism explicit. | Keeping a fallback between inline and referenced automation policy. |
| 2026-08-10 | Exclude every target-agent runtime and model-output proof path from acceptance. | Deterministic fixtures and independent semantic review preserve the contract without rebuilding runtime certification. | Prompt journeys, transcript grading, and runtime-version evidence. |
| 2026-08-10 | Make the rule-disposition ledger the semantic preservation gate and keep 35–45 percent non-normative. | This closes CRSIM-PR3 without incentivizing unsafe compression or accepting immaterial edits. | A hard percentage gate or unmeasured prose-only judgment. |

## Next Artifacts

- Formal proposal rereview of the CRSIM-PR1 through CRSIM-PR3 revisions.
- If approved, a feature-spec amendment defining preserved semantics, package ownership, fixture proof, the rule ledger, and acceptance criteria.
- Required architecture assessment for the skill-package and adapter-resource boundary, with an ADR only if existing architecture is insufficient.
- Execution plan and matching test spec after the contract is approved.

## Follow-on Artifacts

- Initial proposal review: `docs/changes/2026-08-10-code-review-skill-simplification/reviews/proposal-review-r1.md`.
- Superseding changes-requested review: `docs/changes/2026-08-10-code-review-skill-simplification/reviews/proposal-review-r2.md`.
- Finding dispositions: `docs/changes/2026-08-10-code-review-skill-simplification/review-resolution.md`.

## Readiness

Ready for proposal rereview.
The proposal now selects one conditional-reference model, excludes target-agent runtime acceptance, and defines rule-disposition-based success with a non-normative reduction target.
It does not claim specification readiness until the rereview approves these revisions.
