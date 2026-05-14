# Cost-Bounded Rigor M2 Selected Skill Reminders

## Status

approved

## Related proposal

- [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md)

## Goal and context

This spec defines the second cost-bounded-rigor implementation slice after PR #54 completed M1.

M1 made `docs/workflows.md` the full bounded-evidence and path-search guide, added scope-budget guidance to `proposal`, and added scope-budget review checks to `proposal-review`.

M2 keeps the scope narrow: selected public skill surfaces should carry only concise local reminders for bounded evidence and path/state lookup when that reminder materially reduces broad reads. The full rule remains in `docs/workflows.md`.

This slice is intentionally not validation-budget work, lifecycle token-cost reporting, release work, adapter packaging work, dynamic benchmark work, or progressive-loading restructuring.

## Glossary

- selected skill surfaces: `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, and `skills/workflow/SKILL.md`.
- concise local reminder: a short skill-local instruction that points the stage toward bounded evidence without copying the full workflow-guide rule.
- full bounded-evidence rule: the project-local rule in `docs/workflows.md` covering path/state lookup, broad-read avoidance, do-not-under-read behavior, and full-file-read escape conditions.
- no-change rationale: tracked contributor-visible evidence that a selected skill already satisfies the M2 contract and therefore was intentionally left unchanged.
- wording churn: edits that increase or move text without improving stage behavior or proof.

## Examples first

### Example E1: selected skill needs a short reminder

Given a selected skill tells agents to inspect lifecycle state
When it does not remind them to start from active state, metadata, `docs/workflows.md`, headings, or targeted excerpts before broad reads
Then M2 may add a concise local reminder
And the reminder does not copy the full `docs/workflows.md` evidence sequence.

### Example E2: selected skill already has sufficient wording

Given a selected skill already directs agents to use exact paths, active state, `docs/workflows.md`, targeted excerpts, and broader reads only when needed
When M2 audits that skill
Then implementation may leave the skill unchanged
And records a no-change rationale in the active plan, change metadata, explain-change, or another tracked contributor-visible surface.

### Example E3: full workflow rule stays in one place

Given `docs/workflows.md` contains the full bounded-evidence rule
When M2 updates selected skills
Then skills get only local reminders
And `docs/workflows.md` remains the authoritative full guide.

### Example E4: validation-budget work is out of scope

Given a reviewer notices that validation selection could be more targeted
When M2 is being implemented
Then selector behavior and validation-budget policy remain unchanged
And the work routes to the later M3 slice instead.

### Example E5: progressive-loading restructuring is out of scope

Given `workflow` is a high-cost skill
When M2 touches `workflow`
Then the edit is limited to the selected reminder contract
And full progressive-loading restructuring remains out of scope.

## Requirements

R1. M2 MUST cover only selected skill reminders for bounded evidence and path/state lookup, static proof for those reminders when needed, and lifecycle bookkeeping for the M2 slice.

R2. M2 MUST limit selected skill surfaces to `proposal`, `proposal-review`, and `workflow`.

R3. M2 MUST NOT edit `implement` or `code-review`.

R4. M2 MUST NOT change validation-selector behavior, broad-smoke triggers, release validation, adapter packaging, lifecycle token-cost summary artifacts, dynamic benchmark requirements, or hard token gates.

R5. `docs/workflows.md` MUST remain the full project-local bounded-evidence and path-search guide.

R6. Selected skills MUST NOT duplicate the full bounded-evidence rule from `docs/workflows.md`.

R7. A selected skill reminder, when added or revised, MUST be concise and local to that skill's stage behavior.

R8. A selected skill reminder MUST preserve the bounded-first behavior: start from active state, metadata, `docs/workflows.md`, headings, targeted excerpts, paths, IDs, counts, or diffs before broad reads when those narrower sources are sufficient.

R9. A selected skill reminder MUST preserve the do-not-under-read behavior: expand to a broader section or full file when narrower evidence is incomplete, contradictory, or insufficient to support the claim being made.

R10. A selected skill reminder MUST preserve full-file-read escape conditions for cases where the whole file is the target, surrounding context can change the conclusion, relevant sections cannot be isolated safely, bounded searches disagree or are incomplete, or behavior-changing edits depend on the whole source-of-truth artifact.

R11. Before editing selected skills, implementation MUST audit each selected skill for existing equivalent bounded-evidence, path/state lookup, and full-file-read escape wording.

R12. If a selected skill already satisfies the M2 contract, implementation MUST leave that skill unchanged or make only a justified clarification, and MUST record a no-change rationale.

R13. Static proof MAY be added for stable M2 wording, but it MUST use narrow checks for stable phrases, section presence, selected-surface boundaries, and forbidden-surface absence rather than broad natural-language scoring.

R14. Static proof MUST NOT require a selected skill to use one exact sentence when equivalent concise wording satisfies the contract.

R15. M2 MUST keep token-cost measurement diagnostic and warning-only.

R16. M2 MUST NOT require before/after dynamic benchmark comparison unless a later approved plan or test spec explicitly requires it.

R17. M2 MUST preserve safety-critical formal review, verify, PR, material-finding, release, and full-file-read guidance.

R18. M2 MUST preserve the single-authored-skill-source boundary: `skills/` remains the authored source, and generated public adapter skill bodies are not edited or reintroduced as tracked source.

R19. M2 MUST record affected-surface decisions for every selected skill, including edited, unchanged with rationale, and deferred surfaces.

## Inputs and outputs

Inputs:

- accepted cost-bounded-rigor proposal;
- completed M1 plan and PR #54 outcome;
- current selected skill text under `skills/proposal/`, `skills/proposal-review/`, and `skills/workflow/`;
- `docs/workflows.md` as the full bounded-evidence and path-search guide;
- M2 plan and change-local artifacts.

Outputs:

- focused selected-skill reminder edits, only when needed;
- no-change rationale for selected skills that already satisfy the contract;
- focused static proof, only where useful and stable;
- lifecycle and review evidence for the M2 slice.

## State and invariants

- Rigor remains mandatory; M2 does not reduce required review, validation, verification, release, or material-finding behavior.
- `docs/workflows.md` remains the full bounded-evidence guide.
- Selected skills remain user-facing, concise operating guides.
- `skills/` remains the only authored skill source.
- Generated adapter skill bodies remain release-generated output, not tracked authored source.
- M2 remains separate from M3 validation-budget guidance, M4 lifecycle token-cost summaries, and M5 progressive-loading follow-through.

## Error and boundary behavior

1. If a selected skill's current wording conflicts with `docs/workflows.md`, M2 must either update the selected skill or record a blocker before implementation handoff.
2. If a selected skill already satisfies this spec, implementation must avoid wording churn and record no-change rationale.
3. If satisfying M2 would require selector behavior, validation-budget policy, release validation, adapter packaging, dynamic benchmark behavior, or progressive-loading restructuring, implementation must stop and route that work to the appropriate later slice.
4. If static proof would require brittle semantic scoring, implementation must prefer manual review evidence or narrower static checks.
5. If a broader full-file read is needed to safely edit or review a selected skill, bounded-evidence guidance must not prevent that read.

## Compatibility and migration

- Existing accepted proposals, reviews, plans, and lifecycle artifacts remain valid.
- Existing selected skill behavior remains valid unless it contradicts this M2 contract or `docs/workflows.md`.
- No migration of historical skill outputs, release archives, adapter packages, reports, or proposals is required.
- Rollback is to remove unnecessary selected skill wording while keeping `docs/workflows.md` as the full rule and preserving no-change rationale where applicable.

## Observability

M2 behavior is observable through:

- selected skill text;
- static proof in `scripts/test-skill-validator.py`, when added;
- selected validation output;
- active plan validation notes;
- change metadata and later explain-change evidence;
- review findings if a selected skill duplicates the full rule, under-reads, or drifts from `docs/workflows.md`.

No runtime telemetry, logs, metrics, traces, or hosted observability changes are required.

## Security and privacy

- M2 must preserve guidance that favors targeted excerpts, paths, IDs, counts, diffs, and line citations over unnecessary broad dumps.
- M2 must not encourage agents to paste secrets, credentials, private logs, or irrelevant large excerpts into artifacts or chat.
- M2 does not change authentication, authorization, secrets handling, dependency trust, release signing, or data-access behavior.

## Accessibility and UX

No UI is involved.

## Performance expectations

- Selected skill wording should not materially increase static skill size without a stage-local reason.
- Static skill token measurement should be run after canonical skill changes and treated as diagnostic evidence only.
- No hard token threshold is introduced.
- No dynamic benchmark comparison is required for M2 unless a later approved plan or test spec requires it.

## Edge Cases

1. `proposal` already has artifact-placement lookup and evidence-efficiency wording. Implementation must audit before adding text.
2. `proposal-review` already has artifact-placement lookup and evidence-efficiency wording. Implementation must audit before adding text.
3. `workflow` already has a quick operating guide and evidence-efficiency wording. Implementation must audit before adding text.
4. A selected skill has bounded-first wording but lacks an explicit do-not-under-read escape. Implementation may add only the missing concise reminder.
5. A selected skill has a full-file-read escape but lacks path/state lookup wording. Implementation may add only the missing concise reminder.
6. A proposed edit copies the full six-step workflow sequence into every selected skill. Review must reject it as duplication.
7. A proposed static test enforces exact prose instead of stable behavior cues. Review must reject or narrow it.
8. A proposed M2 edit touches `implement` or `code-review`. Review must reject it unless a later approved artifact broadens scope.
9. A proposed M2 edit changes selector behavior. Review must route it to M3 validation-budget work.
10. A proposed M2 edit changes adapter or release surfaces. Review must reject it as out of scope.
11. A selected skill is left unchanged without rationale. Review must request tracked no-change rationale.
12. Token measurement shows a larger static skill total. The result is diagnostic and must not become a hard gate in M2.

## Non-goals

- Do not implement M3 validation-budget guidance.
- Do not change validation selector behavior.
- Do not change broad-smoke triggers.
- Do not add lifecycle token-cost summary artifacts.
- Do not run or require dynamic benchmark comparison by default.
- Do not implement progressive-loading restructuring.
- Do not edit `implement` or `code-review`.
- Do not edit generated public adapter skill bodies.
- Do not change release validation or adapter packaging.
- Do not create a new shared bounded-evidence template.
- Do not rewrite every public skill.

## Acceptance criteria

- M2 selected surfaces are limited to `proposal`, `proposal-review`, and `workflow`.
- Each selected skill is either updated with a concise bounded-evidence reminder or recorded as unchanged with rationale.
- `docs/workflows.md` remains the full bounded-evidence and path-search guide.
- Selected skills do not duplicate the full workflow-guide rule.
- Do-not-under-read and full-file-read escape behavior is preserved.
- No validation-selector, release, adapter, lifecycle-token-summary, dynamic benchmark, hard token gate, `implement`, or `code-review` behavior changes are included.
- Static proof, if added, checks stable boundaries without broad natural-language scoring.
- Static skill token measurement remains diagnostic.
- Safety-critical review, verify, PR, material-finding, release, and full-file-read guidance remains intact.

## Open questions

None.

## Next artifacts

```text
spec-review
plan revision or confirmation
plan-review
test-spec
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- [Spec Review R1](../docs/changes/2026-05-14-cost-bounded-rigor-m2-selected-skill-reminders/reviews/spec-review-r1.md)

## Readiness

Approved after clean spec-review. Ready for M2 plan revision or confirmation and plan-review; not ready for test-spec or implementation until the revised plan is reviewed.
