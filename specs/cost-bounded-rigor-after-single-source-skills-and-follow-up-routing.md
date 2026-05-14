# Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing

## Status

approved

## Related proposal

- [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md)

## Goal and context

This spec defines the first implementation slice for cost-bounded rigor.

The first slice targets the earliest workflow cost multipliers:

- broad or multi-workstream proposals that carry too much work downstream;
- proposal reviews that approve broad scope without explicit classification;
- broad path and state searches before narrower evidence is tried.

The first slice is intentionally narrow. It defines contributor-visible proposal, proposal-review, and workflow-guide behavior for scope budgets and bounded evidence. It does not change validation-selector behavior, release validation, generated adapter packaging, lifecycle token-cost summary artifacts, dynamic benchmark requirements, or the full progressive-loading work for high-cost skills.

## Glossary

- cost-bounded rigor: workflow behavior that preserves reviewability and proof while asking each stage to make the smallest sufficient decision from the smallest sufficient evidence.
- broad proposal: a proposal whose request, scope, or effect contains multiple independently valuable work items or more than one lifecycle family.
- multi-workstream proposal: a proposal that groups work that could reasonably require separate specs, plans, implementation slices, owners, or validation surfaces.
- scope budget: a proposal section that classifies work items by treatment and explains why each item belongs in the current slice, a later slice, a separate proposal, a follow-up, or no scope.
- scope-budget trigger: a condition that tells proposal authors or reviewers that a scope budget is expected.
- scope-budget treatment: one of the approved classification values used to separate current scope from later or excluded work.
- bounded evidence: evidence gathered through exact paths, current state, metadata, headings, stable IDs, counts, line ranges, diffs, or targeted excerpts before broad reads.
- broad read: a broad search, whole-file read, recursive listing, generated-output dump, or long validation-log read used before narrower evidence has been tried.
- under-reading: stopping at narrow evidence when that evidence is incomplete, contradictory, or insufficient for the claim being made.
- first implementation slice: the M1 scope defined by this spec.

## Examples first

### Example E1: broad workflow proposal includes a scope budget

Given a user asks to update proposal behavior, evidence-search behavior, validation policy, and token-cost reporting
When the proposal is drafted
Then the proposal includes a scope budget
And each work item is classified as current, later, separate, follow-up, or out of scope
And downstream spec and plan work can rely on the classification instead of carrying every workstream into one slice.

### Example E2: small single-decision proposal may omit the scope budget

Given a user asks for one narrow wording change in one proposal
When the proposal has no independent workstreams, policy change, generated-output effect, or hidden follow-up risk
Then the proposal may omit the scope budget
And proposal-review does not request one solely as routine ceremony.

### Example E3: proposal-review catches missing classification

Given a proposal touches skill wording, workflow docs, and validation-selection behavior
When it does not classify those work items
Then proposal-review returns `changes-requested`
And the finding names the missing or misleading scope-budget classification.

### Example E4: validators do not infer broadness in the first slice

Given a validator inspects a proposal with no scope-budget table
When no table is present
Then the validator does not fail the proposal solely because it infers that the proposal is broad
And proposal-review remains the first-slice owner for semantic broadness judgment.

### Example E5: workflow guidance starts from bounded evidence

Given an agent needs to find the active path for a spec or review record
When exact user paths, active metadata, change metadata, review logs, or `docs/workflows.md` provide the answer
Then the agent uses those sources before broad-searching authoritative documents or reading full files.

### Example E6: bounded evidence expands when it is insufficient

Given targeted headings and line ranges conflict about whether a workflow rule applies
When the narrower evidence cannot support a safe conclusion
Then the agent expands to a broader section or full file
And the result does not treat bounded evidence as permission to under-read.

### Example E7: first slice does not absorb deferred work

Given lifecycle token-cost summaries, validation-budget selector behavior, dynamic benchmark comparison, and progressive-loading implementation are useful later
When this first slice is implemented
Then those items remain out of first-slice scope unless a later accepted spec or plan explicitly brings them in.

## Requirements

R1. The first implementation slice MUST cover only scope-budget guidance for broad or multi-workstream proposals, proposal-review checks for missing or misleading scope-budget classification, and concise bounded-evidence or path-search guidance in `docs/workflows.md`.

R2. The first implementation slice MUST NOT change validation-selector behavior, broad-smoke triggers, release validation, generated adapter packaging, lifecycle token-cost summary artifacts, dynamic benchmark requirements, or full progressive-loading implementation for `workflow`, `implement`, or `code-review`.

R3. Proposal guidance MUST ask broad or multi-workstream proposals to include a scope budget or equivalent work-item classification before downstream stages rely on the proposal.

R4. Proposal guidance MUST define the scope-budget trigger conditions as proposal/proposal-review judgment rather than mechanical validator inference.

R4a. The scope-budget trigger guidance MUST include these trigger conditions:

- the user request contains two or more independent work items;
- the change touches more than one lifecycle family, such as release packaging plus skill wording plus examples migration;
- the change could reasonably require more than one spec or implementation plan;
- the proposal includes release policy, workflow policy, generated output, public skill behavior, or validation policy;
- proposal-review identifies silent narrowing, hidden follow-up risk, or multi-workstream scope.

R4b. The scope-budget trigger guidance MUST state that small single-decision proposals may omit the scope budget.

R5. A scope budget MUST identify each classified work item, its treatment, and the reason for that treatment.

R5a. Repository proposal guidance SHOULD prefer this table shape when a scope budget is present:

```md
## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| <work item> | <treatment> | <why> |
```

R5b. The allowed scope-budget treatments MUST include:

- `core to this proposal`;
- `first-slice candidate`;
- `same-slice dependency`;
- `separate implementation slice`;
- `deferable follow-up`;
- `separate proposal`;
- `out of scope`.

R5c. Proposal guidance MUST define each allowed treatment value in terms of current scope, first-slice scope, same-slice dependency, later implementation slice, follow-up, separate proposal, or exclusion.

R6. Proposal guidance MUST route deferred work through the accepted follow-up ownership model rather than chat-only notes or `project-map` ownership.

R6a. Proposal guidance MUST preserve the boundary that workflow routes, `project-map` orients when present, action-owning artifacts track current work, and unowned cross-change follow-ups use the follow-up ownership surface.

R7. Proposal guidance MUST preserve the completed single-authored-skill-source boundary.

R7a. Proposal guidance MUST NOT direct contributors to search generated adapter output for authored skill truth.

R7b. Proposal guidance MUST NOT reintroduce tracked generated public adapter skill bodies as a first-slice source surface.

R8. Proposal-review guidance MUST check whether broad or multi-workstream proposals classify current scope, dependencies, later slices, follow-ups, separate proposals, and out-of-scope work clearly enough for downstream reliance.

R9. Proposal-review guidance MUST return `changes-requested` when a broad or multi-workstream proposal lacks required scope-budget classification, hides follow-up work, silently narrows a user request, or uses a misleading treatment value.

R10. Proposal-review guidance MUST allow small single-decision proposals to omit a scope budget when the omission does not create silent narrowing, hidden follow-up risk, or multi-workstream ambiguity.

R11. First-slice validators MUST NOT fail a proposal solely because they infer that the proposal is broad.

R11a. Static validation MAY check the shape of a scope-budget table when one is present.

R11b. Static validation that checks a present table MUST use narrow section, heading, column, or phrase checks rather than broad natural-language scoring.

R12. `docs/workflows.md` MUST remain the full project-local guide for artifact locations, follow-up routing, and bounded evidence or path-search behavior.

R13. `docs/workflows.md` MUST discourage broad searches of authoritative documents solely for path or state discovery when narrower evidence is available.

R14. `docs/workflows.md` MUST direct agents and contributors to start evidence collection from bounded sources before broad reads.

R14a. The bounded evidence guidance MUST include this default evidence sequence or an equivalent ordered strategy:

1. exact user-provided path or change ID;
2. current handoff summary or active plan state;
3. `change.yaml`, review log, review resolution, or release metadata;
4. `docs/workflows.md` artifact-location map;
5. targeted headings, stable IDs, line ranges, counts, or diffs;
6. full-file read only when the whole file is the target or bounded evidence is insufficient.

R15. Bounded-evidence guidance MUST include a do-not-under-read guardrail.

R15a. The guardrail MUST require expansion to a broader section or full file when bounded evidence is incomplete, contradictory, or insufficient to support the claim being made.

R15b. The guardrail MUST preserve full-file reads when the whole file is the review target, surrounding context can change the conclusion, or behavior-changing edits depend on understanding the whole source-of-truth artifact.

R16. The first implementation slice MUST keep public skill wording concise and must not create a long repeated shared template for bounded evidence.

R16a. `docs/workflows.md` owns the full bounded-evidence rule.

R16b. Skills touched by this first slice may include only short local reminders needed for their stage behavior.

R17. The first implementation slice MUST keep safety-critical formal review, verify, PR, material-finding, and release guidance intact.

R18. The first implementation slice MUST keep token-cost measurement diagnostic and warning-only.

R18a. It MUST NOT introduce hard token thresholds.

R18b. It MUST NOT require before/after dynamic benchmark comparison for proposal/evidence wording changes unless a later accepted plan or test spec explicitly requires it.

R19. The first implementation slice MUST record affected-surface decisions for workflow-governance scope.

R19a. Affected surfaces updated in the first slice MUST include the proposal guidance surface, the proposal-review guidance surface, and `docs/workflows.md`.

R19b. Affected workflow-governance surfaces intentionally left unchanged MUST be recorded as unaffected with rationale or deferred with owner and follow-up in a contributor-visible tracked or review-visible surface.

## Inputs and outputs

Inputs:

- user requests that start or materially revise proposals;
- proposal artifacts under `docs/proposals/`;
- proposal-review records and findings;
- change-local metadata and review artifacts under `docs/changes/<change-id>/`;
- `docs/workflows.md` as the artifact-location, follow-up-routing, and bounded-evidence guide;
- canonical proposal and proposal-review guidance surfaces;
- existing workflow, skill-contract, single-source skill, and follow-up ownership specs.

Outputs:

- updated proposal guidance for scope-budget triggers, table shape, treatment values, and follow-up routing;
- updated proposal-review guidance for checking broad proposal classification;
- updated `docs/workflows.md` wording for bounded evidence and path-search behavior;
- contributor-visible rationale for any affected workflow-governance surface left unchanged or deferred;
- validation evidence for changed lifecycle, workflow, and skill guidance surfaces selected by the active plan or test spec.

## State and invariants

- Rigor remains mandatory; cost reduction does not weaken required artifacts, formal review, validation, or release safety.
- `skills/` remains the only authored skill source.
- Generated public adapter skill bodies remain release-generated output, not tracked authored source.
- `docs/workflows.md` remains the artifact-location and follow-up-routing guide.
- `project-map` remains an orienting living reference when present and does not own deferred execution.
- Action-owning artifacts track current-change work.
- Unowned cross-change follow-ups use the follow-up ownership surface.
- Scope-budget guidance separates current scope from deferred work before downstream stages rely on broad proposals.

## Error and boundary behavior

- If a broad proposal lacks a scope budget or equivalent classification, proposal-review MUST request changes before spec or plan reliance.
- If a proposal is small and single-decision, proposal-review MUST NOT request a scope budget solely as routine ceremony.
- If a scope budget classifies a work item as a follow-up without an owning route, proposal-review MUST request clarification or routing.
- If a scope budget uses a non-standard treatment value that is still clear and reviewable, proposal-review MAY accept it only when no downstream ambiguity is created.
- If a scope budget hides current-change work as an unowned follow-up, proposal-review MUST request changes.
- If bounded evidence is incomplete, contradictory, or insufficient, agents MUST broaden the evidence before making the claim.
- If `docs/workflows.md` conflicts with `CONSTITUTION.md` or an approved spec, the higher-priority source wins and the stale guide must be updated or reported before downstream reliance.
- If a future plan attempts to change selector behavior, release validation, lifecycle token-cost summary artifacts, dynamic benchmarks, or progressive-loading implementation under this spec, the plan MUST stop or cite a later accepted spec that authorizes that scope.

## Compatibility and migration

- Existing accepted proposals are not retroactively invalid solely because they lack a scope-budget table.
- Broad proposals created or substantively revised after this spec is approved must follow the new scope-budget guidance.
- Existing validation-selector behavior and broad-smoke triggers remain unchanged in this first slice.
- Existing release validation and adapter packaging behavior remain unchanged.
- Existing generated adapter archives and adapter support files are unaffected.
- Existing token-cost measurement reports remain valid and advisory.
- Existing bounded-evidence guidance in `docs/workflows.md` may be revised or consolidated, but its correctness-preserving full-file-read escape conditions must remain.

## Observability

- Proposal-review findings about missing or misleading scope budgets must identify the reviewed proposal and the missing classification, hidden follow-up, or silent narrowing risk.
- Scope-budget classifications are observable in proposal artifacts.
- Bounded-evidence behavior is observable through `docs/workflows.md`, review findings, validation command summaries, and stage outputs that cite targeted evidence before broad reads.
- No new telemetry, metrics service, hosted logging, or runtime tracing is required.
- No lifecycle token-cost summary artifact is required by this first slice.

## Security and privacy

- This change does not alter authentication, authorization, secrets handling, or data access.
- Bounded-evidence guidance must not encourage pasting secrets, private logs, credentials, or unnecessary large excerpts into artifacts or chat.
- Guidance should prefer paths, IDs, counts, and targeted excerpts over broad log dumps when evidence may contain sensitive data.

## Accessibility and UX

This change has no application UI.

The contributor-facing experience must remain scan-friendly:

- scope-budget tables should be short enough to review quickly;
- proposal-review findings should name the missing classification directly;
- workflow guidance should route contributors to concise path and evidence strategies before broad reads.

## Performance expectations

- The first slice has no hard token-reduction target.
- The first slice must reduce avoidable workflow amplification by making broad scope and broad evidence collection visible earlier.
- Normal validation behavior and command exit semantics must not change for token-cost reasons.
- Any measurement recorded for this slice is diagnostic and warning-only.

## Edge cases

1. A proposal includes two work items that share a file but have different lifecycle owners. It still requires scope-budget classification.
2. A proposal touches workflow docs and public skill behavior but claims to be a docs-only edit. Proposal-review must treat this as a scope-budget trigger.
3. A proposal classifies validation-selector changes as first-slice work. Proposal-review must request narrowing or a later accepted spec.
4. A proposal classifies lifecycle token-cost summary artifacts as routine first-slice output. Proposal-review must request narrowing or conditional/deferred routing.
5. A proposal uses a scope-budget table but leaves the treatment or reason blank. Proposal-review must request completion.
6. A proposal has a `deferable follow-up` row with no owner route. Proposal-review must request routing through the accepted follow-up model.
7. A validator sees no `Scope budget` heading. It must not fail solely by inferring broadness in the first slice.
8. Bounded evidence finds two conflicting line ranges. The agent must read a broader section or full file before relying on either range.
9. The whole file is the review target. The full-file-read escape applies immediately.
10. `docs/project-map.md` is absent, stale, contradicted, or missing the relied-on area. The workflow relies on `docs/workflows.md` and active artifacts for path and follow-up routing until the map is refreshed or bypassed with a no-map rationale.
11. A later plan tries to edit `implement` or `code-review` for progressive loading. That work is out of scope unless the later plan cites accepted authority for that separate slice.
12. A release or adapter path appears only as completed context from PR #52. The first slice must not reopen adapter packaging or generated skill body tracking.

## Non-goals

- Do not rewrite every public skill.
- Do not change validation-selector behavior.
- Do not change broad-smoke triggers.
- Do not add lifecycle token-cost summary artifacts.
- Do not require before/after dynamic benchmark comparison for proposal/evidence wording changes.
- Do not implement the full progressive-loading proposal for high-cost skills.
- Do not edit generated public adapter skill bodies.
- Do not change release validation or adapter packaging.
- Do not move deferred-work ownership into `project-map`.
- Do not weaken formal review, verify, PR, material-finding, or release rules.
- Do not introduce hard token thresholds.
- Do not replace durable proposal, spec, plan, review, or verification artifacts with chat summaries.

## Acceptance criteria

- Broad or multi-workstream proposals are guided to include a scope budget or equivalent work-item classification when trigger conditions apply.
- Small single-decision proposals may omit the scope budget.
- Scope-budget guidance defines trigger conditions, table shape, treatment values, and treatment meanings.
- Proposal-review guidance checks for missing or misleading classification in broad proposals.
- Proposal-review guidance requests changes for silent narrowing, hidden follow-up risk, missing follow-up routing, or misleading treatment values.
- Validators do not infer broadness as a hard failure in the first slice.
- `docs/workflows.md` remains the path, follow-up-routing, and bounded-evidence guide.
- `docs/workflows.md` discourages broad path or state searches when narrower evidence is available.
- Bounded-evidence guidance includes the do-not-under-read escape.
- The first slice does not change validation selectors, lifecycle token reports, dynamic benchmark requirements, release validation, adapter packaging, or high-cost skill progressive-loading implementation.
- Affected-surface decisions are recorded for workflow-governance surfaces left unchanged or deferred.
- Safety-critical review, verification, material-finding, and release guidance remains intact.

## Open questions

None.

## Next artifacts

```text
spec-review
plan
test-spec
implement
code-review
explain-change
verify
pr
```

Architecture is not expected for this first slice because the change does not alter runtime architecture, data flow, persistence, APIs, deployment, security boundaries, or hard-to-reverse design. `spec-review` may still require architecture if it finds a cross-component design risk.

## Follow-on artifacts

- Spec-review approval: `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/spec-review-r2.md`
- Execution plan: `docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md`
- Test spec: `specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.test.md`

## Readiness

Approved after clean spec-review. The active plan and active test spec now own the implementation handoff.
