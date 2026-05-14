# Cost-Bounded Rigor M5 Progressive-Loading Follow-Through

## Status

approved

## Related proposal

- [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted.
- [Progressive Loading for High-Cost Public Skills](../docs/proposals/2026-05-11-progressive-loading-for-high-cost-public-skills.md), accepted and already implemented through its own completed plan.
- [Progressive Loading for High-Cost Public Skills spec](progressive-loading-high-cost-public-skills.md), approved.

## Goal and context

This spec defines the fifth cost-bounded-rigor implementation slice after PR #54 completed M1, PR #55 completed M2, PR #56 completed M3, and PR #57 completed M4.

M1 added scope-budget guidance and the full bounded-evidence rule in `docs/workflows.md`. M2 added selected skill reminders without changing validation behavior. M3 added validation-budget owner-surface guidance without changing selector behavior. M4 added conditional lifecycle token-cost summary support without adding hard token gates.

M5 is a follow-through slice for high-cost public skills. Its job is not to redo the full progressive-loading initiative. The standalone progressive-loading work already added quick operating guides, active-plan-first handoff cues, bounded evidence cues, static proof, dynamic benchmark evidence, and an optimization report for `workflow`, `implement`, and `code-review`.

M5 defines the cost-bounded-rigor contract for preserving and lightly aligning those high-cost skills when this proposal touches them: audit first, edit only when a concrete gap exists, keep local skill wording concise, preserve safety-critical review and verification behavior, and avoid broad rewrites or new measurement overhead.

## Glossary

- M5: the cost-bounded-rigor progressive-loading follow-through slice.
- high-cost skill: one of `workflow`, `implement`, or `code-review`, the priority skills identified by the accepted proposal and the completed progressive-loading initiative.
- progressive-loading baseline: the existing approved progressive-loading proposal, spec, plan, skill wording, validation proof, and optimization report completed before M5.
- follow-through alignment: a minimal change, or explicit no-change rationale, that keeps high-cost skills aligned with cost-bounded-rigor principles after M1-M4.
- touched high-cost skill: a high-cost skill edited, cited as proof, or relied on for M5 acceptance.
- quick operating guide: a short top-of-skill entry point or equivalent targeted section that lets agents route common work before reading detailed guidance.
- bounded evidence cue: skill wording that tells agents to start from active state, metadata, stable IDs, headings, targeted excerpts, counts, diffs, or exact paths before broad reads, while preserving a broader-read escape when narrower evidence is insufficient.
- full progressive-loading implementation: broad restructuring, dynamic benchmark comparison, generated public adapter output refresh, and optimization-report work owned by the standalone progressive-loading proposal and spec.

## Examples first

### Example E1: current skill already satisfies M5

Given `workflow` already has a quick operating guide
And it tells agents to start from the active plan, current artifact state, and targeted sections before broader reads
When M5 audits `workflow`
Then implementation may leave `workflow` unchanged
And records a no-change rationale with validation evidence.

### Example E2: missing bounded-evidence cue gets a concise fix

Given a high-cost skill is missing a bounded-evidence cue for path or state lookup
When the implementation can fix the gap with a short local reminder
Then M5 may add that reminder
And it must not copy the full evidence sequence from `docs/workflows.md`.

### Example E3: implementation handoff avoids broad state discovery

Given an agent is checking implementation milestone readiness
When an active plan exists
Then `implement` guidance starts from the active plan `Current Handoff Summary`
And missing or contradictory handoff state is a blocker instead of a reason to infer state from broad repository searches.

### Example E4: review safety remains intact

Given `code-review` is compressed or clarified
When the skill is reviewed
Then independent-review mode, material-finding evidence, review recording, review-resolution routing, and result-claim boundaries remain present.

### Example E5: no broad rewrite

Given a reviewer suggests rewriting every public skill to match one template
When M5 scope is applied
Then the change rejects that expansion
And limits work to the three high-cost skills plus only directly required proof and lifecycle artifacts.

### Example E6: dynamic benchmark comparison is conditional

Given M5 only records no-change rationale or makes small wording clarifications
When the plan and test spec do not identify runtime benchmark behavior as changed
Then before/after dynamic benchmark comparison is not required
And the explain-change or plan records why local static proof is sufficient.

### Example E7: material behavior change escalates proof

Given M5 substantially changes quick operating guides or handoff-state discovery behavior
When the plan or test spec judges runtime behavior evidence necessary
Then targeted dynamic benchmark comparison may be required by that plan or test spec
And the change must not claim runtime improvement without that evidence.

### Example E8: generated adapter bodies remain out of source

Given M5 edits canonical skill text
When validation runs
Then the implementation validates canonical authored skills
And it does not reintroduce tracked generated public adapter skill bodies.

## Requirements

R1. M5 MUST cover only progressive-loading follow-through for `workflow`, `implement`, and `code-review`, plus directly required proof and lifecycle bookkeeping.

R2. M5 MUST treat the completed progressive-loading proposal and approved progressive-loading spec as baseline authority rather than reopening the full optimization initiative.

R3. M5 MUST audit each high-cost skill before editing it for this slice.

R4. If a high-cost skill already satisfies the M5 contract, implementation MUST leave it unchanged or make only a justified clarification, and MUST record no-change rationale in a contributor-visible tracked surface.

R5. If a high-cost skill is changed, the change MUST be the smallest sufficient wording or structure change that fixes a concrete M5 gap.

R6. Each touched high-cost skill MUST preserve or provide a quick operating guide or equivalent targeted entry point near the top of the skill.

R7. Each touched high-cost skill MUST preserve targeted reading behavior: read the user request, active plan state when relevant, governing artifact status, and the specific needed section before broad reads.

R8. Each touched high-cost skill MUST preserve the broader-read escape: expand to a broader section or full file when bounded evidence is incomplete, contradictory, or insufficient to support the claim being made.

R9. `workflow` MUST continue to route work without replacing specialized stage skills, and MUST preserve source-of-truth order, stop conditions, and stage-owned claim boundaries.

R10. `implement` MUST continue to start milestone readiness and handoff-state checks from the active plan `Current Handoff Summary` when a plan exists.

R11. `implement` MUST treat missing, stale, or contradictory milestone state as a blocker rather than instructing agents to infer state from broad repository searches.

R12. `code-review` MUST preserve independent-review mode, mixed-evidence caution, material-finding requirements, review-recording obligations, review-resolution routing, milestone-aware handoff, and result-claim boundaries.

R13. M5 MUST keep `docs/workflows.md` as the full bounded-evidence, workflow-routing, artifact-location, and follow-up-routing guide.

R14. High-cost skill wording MUST remain concise and local. It MUST NOT copy long shared templates or duplicate the full `docs/workflows.md` evidence sequence.

R15. M5 MUST NOT rewrite every public skill.

R16. M5 MUST NOT remove safety-critical review, verification, material-finding, validation, release, or milestone-handoff guidance solely to reduce static size.

R17. M5 MUST NOT add hard token thresholds, hard release gates, or hard CI blockers based on token totals.

R18. M5 MUST NOT change validation-selector behavior, broad-smoke triggers, release validation, adapter packaging, generated public adapter output tracking, or token-cost report schemas.

R19. M5 MUST NOT reintroduce tracked generated adapter skill bodies or treat generated adapter output as authored skill truth.

R20. If canonical skill text changes, implementation MUST validate canonical skill surfaces with the repo-owned skill validation commands selected by the plan and test spec.

R21. If canonical skill text changes, implementation MUST run static skill token measurement or record an explicit plan/test-spec rationale for why it was not needed.

R22. Static token measurement in M5 MUST remain diagnostic and warning-only unless a later accepted spec creates a hard gate.

R23. Before/after dynamic benchmark comparison is advisory for small M5 wording or no-change-rationale work unless the active plan or test spec requires it because runtime benchmark behavior is materially affected.

R24. If M5 claims runtime benchmark improvement, it MUST cite targeted dynamic benchmark evidence that supports the claim.

R25. M5 static or validator proof SHOULD use stable behavior cues, section presence, required terms, and forbidden-sequence checks rather than exact full-sentence prose.

R26. M5 MUST preserve the completed PR #52 single-authored-skill-source model and the PR #53 follow-up ownership model.

R27. If M5 discovers work that belongs to release packaging, adapter packaging, generated-output publication, selector behavior, broad benchmark changes, or hard token gates, implementation MUST stop or route that work to a separate accepted artifact.

R28. If M5 triggers a lifecycle token-cost summary under the approved M4 rules, the plan or test spec MUST name that trigger. Otherwise, lifecycle token-cost summaries remain optional.

R29. M5 implementation MUST record affected and intentionally unaffected surfaces, including `workflow`, `implement`, `code-review`, generated adapter output, release behavior, selector behavior, benchmark behavior, and lifecycle token-cost summary behavior.

R30. M5 MUST preserve project-portable public skill wording. Published skills MUST NOT expose repository-maintainer-only implementation details such as generated mirror paths, adapter package internals, selector path constraints, drift-check mechanics, shared-block mechanics, or local-only examples.

## Inputs and outputs

Inputs:

- accepted cost-bounded-rigor proposal;
- accepted and completed progressive-loading proposal;
- approved progressive-loading spec and completed plan;
- current canonical `workflow`, `implement`, and `code-review` skill text;
- `docs/workflows.md`;
- current skill validation and token-cost measurement scripts;
- M1-M4 cost-bounded-rigor specs, plans, and review evidence when needed for context.

Outputs:

- this M5 spec;
- downstream M5 test spec and plan when approved;
- optional minimal edits to `workflow`, `implement`, or `code-review` if the audit finds concrete M5 gaps;
- no-change rationale for any high-cost skill or related surface left unchanged;
- selected validation, skill validation, static measurement, and optional benchmark evidence as required by the plan/test spec;
- change-local metadata and durable rationale.

## State and invariants

- `skills/` remains the only authored skill source.
- `docs/workflows.md` remains the full workflow and bounded-evidence guide.
- `workflow`, `implement`, and `code-review` remain progressively loadable from short targeted entry points.
- Review, verification, material-finding, release, and milestone-handoff rigor remains unchanged.
- Token-cost measurement remains diagnostic and warning-only for M5.
- Follow-ups use the accepted follow-up ownership model instead of chat-only notes or project-map ownership.

## Error and boundary behavior

1. If the audit cannot determine whether a high-cost skill satisfies M5 without broader context, the implementation must read the necessary broader section or full file and record why bounded evidence was insufficient.
2. If a required high-cost skill is missing, moved, or contradicted by generated output, implementation must stop and report the source-of-truth conflict.
3. If static skill validation fails, implementation must fix the failure before handoff.
4. If token measurement warns on a touched high-cost skill, the result is warning-only, but implementation must record whether the warning is accepted, explained, or addressed.
5. If a review finding requires broader validation, the accepted review-resolution disposition controls validation scope.
6. If dynamic benchmark comparison is not run, explain-change or the active plan must state why the plan/test spec did not require it.

## Compatibility and migration

- Existing agents may still read full skills; M5 preserves full-file-read escape behavior.
- Existing workflow stage order, review gates, release gates, selector behavior, and adapter packaging behavior remain compatible.
- Existing progressive-loading proof remains historical evidence; M5 does not invalidate or replace the prior optimization report.
- If M5 changes canonical skill wording, downstream public adapter release archives pick up that authored source through the existing release-generation process rather than through tracked generated skill bodies.
- Rollback for M5 skill wording is to revert the minimal M5 wording changes while preserving the completed progressive-loading baseline and M1-M4 cost-bounded-rigor guidance.

## Observability

M5 is observed through repository artifacts and validation evidence, not runtime logs or metrics.

Required observable evidence includes:

- the approved spec, test spec, and plan when they exist;
- high-cost skill audit result and no-change rationale or minimal diff;
- selected validation output;
- skill validation output when skills change;
- static skill token measurement or explicit rationale when skills change;
- optional dynamic benchmark evidence only when required by the plan/test spec or claimed by the change;
- final explain-change and verify evidence before PR.

## Security and privacy

- Public skill wording must not include secrets, credentials, private paths, usernames, host-specific workarounds, or debug-only data.
- Public skill wording must remain project-portable and must not expose repository-maintainer-only generated-output mechanics.
- M5 must not weaken authorization, review, release, or verification guidance.

## Accessibility and UX

No UI is involved.

For skill-reader experience, high-cost skills should remain easy to scan from the top-level quick guide, with predictable sections and concise stage-owned output expectations.

## Performance expectations

- M5 should reduce or preserve the cost-bounded operating path for high-cost skills.
- M5 must not increase skill size or validation workload without a recorded justification tied to preserved rigor.
- Static token counts are diagnostic. They help reviewers compare direction, but they are not hard gates in this slice.
- Dynamic benchmarks are not routine for small wording or no-change-rationale work. They become required only when the plan/test spec identifies material runtime-behavior risk or when the change claims runtime improvement.

## Edge cases

1. A high-cost skill already satisfies M5. The expected behavior is no skill edit plus recorded no-change rationale.
2. A high-cost skill has a quick guide but lacks a bounded-evidence escape. The expected behavior is a concise fix or a recorded reason why the existing wording is equivalent.
3. `implement` mentions active plan state in one section but another section encourages broad milestone search first. The expected behavior is to remove or clarify the conflicting cue.
4. `code-review` compression would remove material-finding or review-recording behavior. The expected behavior is to reject the compression or move detail to an approved owner surface with explicit safety rationale.
5. A reviewer requests dynamic benchmark proof for a no-change audit. The expected behavior is to require a plan/test-spec rationale only if runtime behavior is materially affected or improvement is claimed.
6. M5 work discovers release or adapter packaging confusion. The expected behavior is to stop or route that work to a separate accepted artifact.
7. A validator test would assert exact full-sentence prose. The expected behavior is to prefer stable section, term, and behavior-cue checks unless exact text is itself the contract.
8. A broad search or large command output incident occurs during M5. The expected behavior is to apply the M4 lifecycle-summary trigger rules if the incident is relevant and not justified as smallest sufficient evidence.

## Non-goals

- Do not redo the full progressive-loading proposal.
- Do not rewrite every skill.
- Do not add or change generated public adapter skill bodies as tracked source.
- Do not change release packaging, adapter packaging, or generated archive behavior.
- Do not change validation-selector behavior or broad-smoke triggers.
- Do not add hard token thresholds or hard token gates.
- Do not require dynamic benchmark comparison for no-change or small wording-only work unless the plan/test spec identifies material runtime risk.
- Do not move the full bounded-evidence guide out of `docs/workflows.md`.
- Do not weaken review, verification, material-finding, release, or milestone-handoff safety rules.

## Acceptance criteria

- The M5 plan/test spec, when created, treats the completed progressive-loading work as baseline rather than reopening it.
- `workflow`, `implement`, and `code-review` are audited before implementation edits.
- Any unchanged high-cost skill has recorded no-change rationale.
- Any touched high-cost skill preserves quick operating guide behavior, targeted reading, bounded-evidence escape behavior, and stage-owned claim boundaries.
- `implement` preserves active-plan `Current Handoff Summary` first behavior for milestone readiness and handoff-state checks.
- `code-review` preserves independent review, material-finding, review recording, and review-resolution safety behavior.
- No generated public adapter skill bodies are reintroduced as tracked authored source.
- No release, adapter, selector, broad-smoke, benchmark-suite, token-report-schema, or hard-token-gate behavior changes are introduced.
- Static skill validation and token measurement requirements are selected according to whether canonical skill text changes.
- Dynamic benchmark comparison is required only when the plan/test spec requires it or the change claims runtime improvement.
- Safety-critical review, verification, material-finding, release, and milestone-handoff guidance is preserved.

## Open questions

None.

## Next artifacts

```text
spec-review
plan
plan-review
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Spec-review approval: `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/spec-review-r1.md`
- Execution plan: `docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md`
- Plan-review approval: `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/plan-review-r1.md`
- Test spec: `specs/cost-bounded-rigor-m5-progressive-loading-follow-through.test.md`

## Readiness

Approved after clean spec-review. The active M5 plan has clean plan-review approval, and the M5 test spec is active and maintainer-approved for implementation.
