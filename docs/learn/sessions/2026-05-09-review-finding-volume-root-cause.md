# Learn Session: Review Finding Volume Root Cause

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking why the single-workflow initiative produced many review findings, what the root cause was, what can improve, and what best practices should guide future work.
- Trigger type: explicit maintainer request / contributor observation / repeated review findings.
- Scope:
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-log.md`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md`
  - review records under `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/reviews/`
  - prior learn sessions about spec-review rounds, public skill surface boundaries, architecture workflow overhead, code-review timing evidence, and milestone commit policy mismatch
- Evidence in scope:
  - 17 formal review records
  - 23 resolved material findings
  - proposal-review findings `SWF1` through `SWF8`
  - spec-review findings `SR1` through `SR9`
  - plan-review findings `PLR1` through `PLR3`
  - code-review findings `CR1` through `CR3`
- Explicit exclusions:
  - no workflow, spec, skill, architecture, validator, topic, PR, or plan update from this learn session;
  - no claim about PR readiness, CI status, branch readiness, review-resolution closeout, or verification status;
  - no curated topic update without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-08-spec-review-rounds-and-readiness.md`
  - `docs/learn/sessions/2026-05-08-public-skill-surface-boundary.md`
  - `docs/learn/sessions/2026-05-08-architecture-update-workflow-overhead.md`
  - `docs/learn/sessions/2026-05-08-code-review-timing-evidence.md`
  - `docs/learn/sessions/2026-05-08-milestone-commit-policy-mismatch.md`
  - `docs/learn/sessions/2026-05-07-milestone-closeout-vs-progress.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`
- Session record path: `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`

## Observe

### O1 - The finding count was high because the change was workflow-governance work, not ordinary implementation work

Evidence:

- The review log records 17 formal review entries and 23 resolved findings.
- Proposal-review R1 alone produced 8 findings covering the new workflow model, explain-change/verify claim boundaries, public skill portability, guide generation, static validation, active-plan transition notes, `ci-maintenance`, and public-skill check scope.
- Spec-review R1 through R4 produced 9 findings before spec-review R5 approved the amended contract.
- The affected surfaces included governing specs, matching test specs, public docs, canonical skills, generated Codex mirrors, public adapter skill copies, validators, architecture docs, plan state, change metadata, and review records.

Observation:

The volume was partly structural. This change altered the workflow contract while also changing the public skill contract and generated outputs. A small wording error could appear in several authoritative, public, generated, and validation surfaces. That makes the review surface much larger than an ordinary feature slice.

Practical answer:

Many findings were expected for a cross-cutting governance change. The problem is not that review found issues. The useful signal is that the first passes did not turn each issue class into a complete surface sweep soon enough.

### O2 - The deepest root cause was unstable route vocabulary

Evidence:

- `SWF1` challenged "proportional evidence" because it lacked a minimum observable contract.
- `SR1` found the proportional-evidence model conflicted with mandatory-stage wording.
- `SR4` found remaining public route categories such as trivial work, high-risk route wording, and retired size/risk vocabulary.
- `SR9` found remaining proportional-evidence and fast-lane wording after earlier fixes.

Observation:

The workflow was trying to remove lanes while still explaining focused use through smallness or risk categories. That left overlapping concepts: one standard workflow, proportional evidence, tiny/low-risk work, manual skill use, and triggered stages. Review kept finding contradictions until focused use was reframed as isolated manual skill invocation, not as a second workflow path.

Best-practice answer:

For workflow policy changes, stabilize the routing vocabulary before editing downstream surfaces. If a concept is retired, write a short replacement rule and a retired-term list first, then use that list to sweep specs, docs, skills, tests, generated output, and validators.

### O3 - Safe resolutions were applied locally before same-class sweeps were complete

Evidence:

- `SR2`, `SR5`, `SR8`, `CR2`, and `CR3` all involved stale final-closeout or verify-before-explanation wording in different surfaces.
- `SR7` found matching test specs still preserved fast-lane and direct-verify behavior after governing text had moved on.
- `CR2` and `CR3` found stale phrases in canonical skill text plus generated Codex and adapter copies, even though broader static checks were already passing.
- The prior learn session `2026-05-08-spec-review-rounds-and-readiness.md` observed the same pattern: each safe resolution fixed the visible defect class in a bounded surface set, while later reviews found adjacent stale wording variants.

Observation:

The safe path reduced blast radius per edit, but it also encouraged narrow fixes. Each review round closed the latest specific finding, then the next round discovered another instance of the same class in a different surface or spelling.

Best-practice answer:

After every material wording finding, run a same-class sweep before asking for the next review. The sweep should cover canonical specs, matching test specs, public workflow docs, canonical skills, generated skill mirrors, adapter packages, validators, and active plan/change artifacts when touched.

### O4 - Static checks were added after drift had already spread

Evidence:

- `SWF5` requested exact static validation targets.
- `SR9` found stale variants such as `Proportional-evidence` and `Fast-lane exceptions` because earlier checks were too narrow.
- `CR2` and `CR3` found stale direct-verify and verify-before-explanation phrases that generated output faithfully mirrored from canonical skill bugs.

Observation:

The validators were initially weaker than the cross-surface change. They proved some intended properties, but they did not yet reject all retired spellings, hyphen variants, case variants, or direct-route phrase patterns.

Best-practice answer:

For retired vocabulary or retired ordering, add the negative static check at the same time as the first canonical edit. Prefer case-insensitive and hyphen/space-aware checks for public workflow and shipped skill surfaces. Pair negative checks with positive checks for the replacement invariant.

### O5 - Generated output increased the cost of stale canonical wording

Evidence:

- `CR2` found stale `code-review` final-closeout text in the canonical skill and generated Codex and adapter copies.
- `CR3` found stale `verify` final-order text in the canonical skill and generated Codex and adapter copies.
- `SR9` required regenerating generated skill mirrors and adapter packages after canonical public skill wording changed.

Observation:

Generated files were not the root cause. They amplified canonical drift. If canonical text is stale, regeneration correctly copies the stale behavior into every shipped surface.

Best-practice answer:

Fix canonical sources first, then regenerate generated surfaces once the canonical wording and checks are stable. Review canonical and generated surfaces together only for drift and public-output correctness, not as separate sources of truth.

### O6 - Plan and lifecycle bookkeeping used too many mutable state surfaces

Evidence:

- `PLR1` found plan-review was premature because architecture-review was still pending.
- `PLR2` found `test-spec` readiness was worded as depending on the test-spec proof map itself.
- `PLR3` found lifecycle closeout formatted like an implementation milestone.
- `CR1` found M1 state conflicted between the current handoff and the milestone section.
- Prior learn sessions record related plan-state and milestone-commit mismatches.

Observation:

The plan carried duplicated lifecycle facts across current handoff, milestone sections, readiness fields, progress notes, plan index, and change metadata. Manual updates across those surfaces made timing-dependent inconsistencies likely.

Best-practice answer:

Use one concise current-state block as the primary operational state, and make the rest of the plan either stable milestone detail or historical evidence. When state changes, update the state block, matching milestone section, index, and change metadata in one bookkeeping step before requesting review.

### O7 - Reviews were often catching real contradictions, not just creating ceremony

Evidence:

- Proposal-review R2, spec-review R5, architecture-review R1, plan-review R2, and code-review R2, R3, R5, R6, and R7 all passed without material findings after earlier contradictions were resolved.
- Review-resolution records all 23 findings as resolved and none unresolved.

Observation:

The findings were not random churn. They clustered around real contradictions in route semantics, final-closeout order, public-skill boundaries, generated output, and plan state. Once the same-class sweeps and static checks caught up, later reviews were clean.

Best-practice answer:

Keep the review gates, but improve pre-review preparation. The target is fewer repeated same-class findings, not weaker review.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Review log and review-resolution evidence | High finding count is partly explained by the cross-cutting governance scope. |
| O2 | artifact-update | pending confirmation | Possible proposal/spec/workflow guidance for retired vocabulary setup before broad edits. | Not yet confirmed | The pattern is reusable, but behavior belongs in authoritative workflow or skill guidance. |
| O3 | process-follow-up | pending confirmation | Possible review checklist or skill guidance requiring same-class sweeps after material wording findings. | Not yet confirmed | The pattern recurred across spec-review and code-review findings. |
| O4 | process-follow-up | pending confirmation | Possible validator guidance for retired-term checks at first canonical edit. | Not yet confirmed | Static checks caught the problem only after several stale variants surfaced. |
| O5 | observation | observation | None | Generated-output findings in `CR2`, `CR3`, and `SR9` | Generated output amplified canonical wording drift but did not independently create the issue. |
| O6 | process-follow-up | pending confirmation | Possible plan template or active-plan state-sync guidance. | Not yet confirmed | Similar plan-state issues appeared in prior sessions and this initiative. |
| O7 | observation | observation | None | Later clean review rounds | The evidence supports keeping reviews but improving pre-review sweeps. |

## Route

No routing performed.

Contributor confirmation is unavailable for derivative updates to workflow, skills, validators, templates, or topic files. This session records the evidence-bound retrospective and stops before changing action-owning artifacts.

## Best Practices

- Stabilize vocabulary first. For workflow-policy changes, define the replacement model and retired terms before editing broad surfaces.
- Treat each material finding as a class of defect. Fix the instance, then sweep for the same class across authoritative, public, generated, validation, and active-plan surfaces.
- Add static checks early. Retired route terms and retired stage ordering should get negative checks in the same milestone that removes them.
- Use positive invariants too. Require the replacement phrasing, such as one recommended standard workflow, isolated manual skill invocation, and final closeout order.
- Keep generated output downstream. Edit canonical skills/templates first, regenerate, then run drift and public-output validation.
- Reduce mutable plan state. Keep one operational current-state block and update all mirrored state surfaces together before review.
- Separate isolated skill use from workflow completion. This avoids inventing new lane vocabulary for focused use.
- Keep reviews strict. The improvement target is better pre-review preparation and automation, not lower review standards.

## No Durable Lesson Rationale

No topic entry was created. This session found repeated patterns and likely follow-ups, but routing those improvements would change workflow, skill, validator, or plan-template behavior. Those changes require contributor confirmation and action-owning artifact updates rather than a learn topic alone.
