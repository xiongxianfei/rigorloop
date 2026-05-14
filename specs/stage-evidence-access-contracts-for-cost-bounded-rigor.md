# Stage Evidence Access Contracts for Cost-Bounded Rigor

## Status

approved

## Related proposal

- [Stage Evidence Access Contracts for Cost-Bounded Rigor](../docs/proposals/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md)

## Goal and context

This spec defines the contract for stage evidence access guidance in RigorLoop skills.

The change addresses workflow amplification caused by broad evidence collection before a stage knows what it must prove. It introduces a default/conditional/expansion evidence model, a bounded-discovery boundary, and input-contract preservation rules.

The first implementation slice is intentionally narrow. M1 covers the shared operational model in `docs/workflows.md`, concise evidence-access guidance in `proposal` and `proposal-review`, and `spec` only if immediate proposal-to-spec handoff needs the same rule. M2 separately covers `implement` and `code-review`; `plan` remains future-slice design context unless later promoted.

## Glossary

- stage evidence access contract: the per-stage rule that defines default evidence, conditional evidence, expansion evidence, and bounded-read behavior.
- default evidence: evidence a stage reads first without extra explanation because it is normally required to make that stage's claim.
- conditional evidence: evidence a stage reads only when a named trigger applies.
- expansion evidence: substantive evidence outside the default set and triggered conditional set.
- bounded discovery: low-content lookup activity used to locate paths, headings, counts, metadata, line numbers, or targeted diffs.
- substantive out-of-set read: reading meaningful content outside the default and triggered conditional set.
- standing operating instructions: governance or workflow instructions a skill must preserve as operating context even when task evidence is narrowed.
- task evidence: artifacts or source content needed to decide or prove the current stage-owned claim.
- first implementation slice: M1 proposal-side evidence access work defined by this spec.

## Examples first

### Example E1: proposal starts from proposal-side evidence

Given a user asks for a workflow-guidance proposal
When `proposal` authors the artifact
Then it starts from the user request, vision or constitution when standing gates matter, and any directly related proposal being extended or superseded
And it does not broad-search specs, docs, generated output, or historical proposals merely because they might be relevant.

### Example E2: bounded discovery does not create an expansion log

Given `proposal-review` needs to find the current review record path
When it runs a path inventory, heading scan, line-number search, count query, targeted diff summary, or metadata lookup
Then that lookup is bounded discovery
And the review output does not need an `Evidence expansion` section solely for that lookup.

### Example E3: substantive out-of-set read records a reason

Given `proposal-review` reads an ADR that is not part of its default evidence and was not linked by the proposal
When the ADR content is needed because the proposal appears to conflict with an architecture decision
Then the review records a compact evidence-expansion reason
And the reason names the artifact, trigger, bounded method, and result.

### Example E4: existing inputs are classified before skill edits

Given M2 updates `implement`
When current `implement` inputs include the active plan, approved spec, test spec, architecture constraints, code/tests, validation commands, `CONSTITUTION.md`, and neighboring patterns
Then implementation classifies each as standing operating instructions, default task evidence, conditional task evidence, expansion evidence, or obsolete/duplicated guidance
And any removed or downgraded input has a recorded rationale.

### Example E5: M1 validation does not pull in M2 paths

Given M1 changes `docs/workflows.md`, `proposal`, and `proposal-review`
When validation is selected
Then M1 validation covers those paths and includes `spec` only if M1 updates the `spec` skill
And it does not select `implement` or `code-review` paths until M2 runs.

## Requirements

R1. M1 MUST define the shared stage evidence access model in `docs/workflows.md`.

R2. M1 MUST add or update concise evidence-access guidance in `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`.

R3. M1 MUST update `skills/spec/SKILL.md` only when immediate proposal-to-spec handoff needs the same evidence-access rule.

R4. M1 MUST NOT update `skills/implement/SKILL.md`, `skills/code-review/SKILL.md`, or `skills/plan/SKILL.md`.

R5. The stage evidence access model MUST define default evidence, conditional evidence, expansion evidence, and broad/full-file evidence behavior.

R6. Participating skills MUST direct agents to read default evidence first.

R7. Participating skills MUST direct agents to read conditional evidence only when the named trigger applies.

R8. Participating skills MUST require a compact reason when a stage reads substantive evidence outside its default evidence and triggered conditional evidence.

R9. Participating skills MUST NOT require an evidence-expansion record for default evidence, triggered conditional evidence, or bounded discovery.

R10. The shared model MUST define bounded discovery as distinct from evidence expansion.

R10a. Bounded discovery MUST include path inventory, heading scan, line-number search, count query, targeted diff summary, and metadata lookup.

R11. Evidence expansion MUST begin only when the stage reads substantive content outside its default evidence and triggered conditional evidence.

R12. Evidence-expansion output MUST appear only when evidence expansion occurred.

R13. The shared model MUST discourage broad searches of authoritative documents solely for path or state discovery when bounded evidence can answer the question.

R14. The shared model MUST preserve full-file reads when the whole file is the target, the relevant section cannot be isolated safely, bounded evidence is contradictory or incomplete, surrounding context can change the conclusion, or the decision depends on whole-file context.

R15. The shared model MUST preserve the do-not-under-read invariant: a stage must expand when bounded evidence is missing, stale, contradictory, or insufficient for the stage-owned claim.

R16. Skill updates governed by this spec MUST preserve existing mandatory operating inputs unless a removal or downgrade has a rationale.

R17. Before updating a participating skill's inputs, implementation MUST classify current inputs as standing operating instructions, default task evidence, conditional task evidence, expansion evidence, or obsolete/duplicated guidance.

R18. Implementation MUST record a migration table or equivalent review-visible note for each touched skill whose input guidance is removed, downgraded, or reclassified.

R19. `proposal` evidence guidance MUST include these default evidence categories: user request, `VISION.md` when proposal fit matters, `CONSTITUTION.md` for governance/source-of-truth/workflow/release-policy changes, and a related proposal only when superseding or extending it.

R20. `proposal` evidence guidance MUST include these conditional evidence categories: `docs/project-map.md` when architecture or repository orientation matters, existing specs or ADRs when the proposal changes their direction, `docs/workflows.md` when artifact placement or workflow routing matters, and code only when current behavior is part of the decision.

R21. `proposal-review` evidence guidance MUST include these default evidence categories: proposal under review, user's original request or initial intent, and `VISION.md` or `CONSTITUTION.md` when standing gates or vision fit matter.

R22. `proposal-review` evidence guidance MUST include these conditional evidence categories: linked specs, ADRs, plans, or learn sessions when the proposal relies on them; `docs/workflows.md` when workflow behavior or artifact placement is proposed; and code only when the proposal depends on current implementation reality.

R23. `spec` evidence guidance, if updated in M1, MUST start from accepted proposal, latest proposal-review result, review-resolution when proposal-review findings exist, and existing related spec when amending, superseding, or overlapping behavior.

R24. `spec` evidence guidance, if updated in M1, MUST allow conditional reads of architecture/ADR, `docs/workflows.md`, code, and `CONSTITUTION.md` when the corresponding trigger applies.

R25. `plan` evidence guidance in this spec is future-slice design context only and MUST NOT require M1 `plan` skill edits.

R26. `implement` and `code-review` evidence guidance MUST remain M2 scope and MUST NOT be selected by M1 validation solely because they are described as future work.

R27. M1 validation guidance MUST be separated from M2 validation guidance.

R28. M1 validation guidance MUST select `docs/workflows.md`, `skills/proposal/SKILL.md`, and `skills/proposal-review/SKILL.md`, plus `skills/spec/SKILL.md` only when M1 updates `spec`.

R29. M2 validation guidance MUST separately select `skills/implement/SKILL.md` and `skills/code-review/SKILL.md` when M2 runs.

R30. Static checks, when added, MUST be concept-based and MUST NOT require exact long paragraphs across skills.

R31. Concept checks MAY look for evidence-access section presence, default evidence, conditional evidence, reason recording, bounded evidence before broad reads, and full-file-read escape behavior.

R32. This spec MUST NOT introduce runtime enforcement, semantic read auditing, hard token gates, lifecycle token-cost summary implementation, release validation changes, adapter packaging changes, or generated-output source model changes.

R33. Static skill token measurement MUST remain diagnostic and warning-only.

R34. Safety-critical formal review, validation, material-finding, source-of-truth, verify, PR, and release rules MUST remain intact.

## Inputs and outputs

Inputs:

- accepted stage evidence access contracts proposal;
- proposal-review records and review-resolution closeout;
- existing `docs/workflows.md` bounded-evidence and artifact-location guidance;
- current `proposal`, `proposal-review`, and optionally `spec` skill text;
- related cost-bounded-rigor and skill-contract specs.

Outputs:

- accepted proposal status settlement;
- this draft spec;
- M1 updates to `docs/workflows.md`, `proposal`, `proposal-review`, and optionally `spec` when later implemented;
- review-visible input-classification or migration rationale for touched skills when input guidance changes;
- scoped M1 and M2 validation guidance;
- later test spec and plan artifacts after spec-review.

## State and invariants

- Rigor remains mandatory; evidence access guidance reduces waste without weakening required review, validation, verification, release, or material-finding behavior.
- Bounded evidence is a starting strategy, not permission to under-read.
- Full-file reads remain allowed when the full file or broader context is necessary for the stage-owned claim.
- `docs/workflows.md` owns the shared operational model.
- Individual skills own concise stage-local default and conditional evidence sets.
- `skills/` remains the canonical authored skill source.
- Generated public adapter skill bodies remain release artifacts, not tracked authored source.
- M1 remains separate from M2 execution/review evidence access and from later validation-budget, lifecycle token-cost, and progressive-loading work.

## Error and boundary behavior

1. If a skill's existing mandatory operating input would be removed or downgraded without rationale, implementation must stop or add the required migration rationale before review.
2. If bounded discovery reveals contradictory or incomplete evidence, the stage must expand rather than claim the narrower evidence is sufficient.
3. If an M1 change needs `implement` or `code-review` evidence guidance, implementation must stop and route that work to M2 or a later approved artifact.
4. If static checks would require broad semantic scoring or exact long prose, implementation must narrow them to concept checks or defer them.
5. If selected validation for M1 includes M2 paths without an explicit reason, review must request correction.
6. If a skill edit duplicates the full shared model instead of using concise local wording, review must request reduction or relocation to `docs/workflows.md`.
7. If evidence-expansion logging becomes routine for bounded discovery, review must request correction.

## Compatibility and migration

- Existing accepted specs, plans, review records, and change-local artifacts remain valid.
- Existing skill input obligations remain valid unless a touched skill records a reviewed migration rationale.
- Historical evidence reads and old review records do not need backfill.
- No migration of generated adapter archives, release artifacts, token reports, or historical proposals is required.
- Rollback is to remove or narrow the evidence-access wording while preserving the do-not-under-read rule and full-file-read escape conditions.

## Observability

The behavior is observable through:

- `docs/workflows.md` shared evidence-access wording;
- selected skill text for `proposal`, `proposal-review`, and optionally `spec`;
- input-classification or migration rationale in plan, change metadata, explain-change, or another review-visible artifact;
- `scripts/test-skill-validator.py` output when static checks are added;
- `scripts/validate-skills.py` output;
- `scripts/select-validation.py` output showing M1 and M2 path separation;
- static skill token measurement output;
- formal review findings when a skill under-reads, over-logs, or duplicates shared guidance.

No runtime logs, metrics, traces, audit events, or user-visible application status changes are required.

## Security and privacy

- Evidence access guidance must prefer targeted excerpts, paths, IDs, counts, and diffs before broad dumps.
- Evidence access guidance must not encourage pasting secrets, credentials, private logs, or irrelevant large excerpts into artifacts or chat.
- The change does not alter authentication, authorization, dependency trust, release signing, or data-access behavior.

## Accessibility and UX

No UI is involved.

## Performance expectations

- Skill wording should stay concise and stage-local.
- Static skill token measurement should run after canonical skill changes and remain diagnostic.
- No hard token threshold is introduced.
- Dynamic benchmark comparison is not required for M1 unless a later approved plan or test spec requires it.

## Edge cases

1. A stage reads a line-number search result outside its default evidence. This is bounded discovery and does not require `Evidence expansion`.
2. A stage reads a full out-of-set ADR section because the proposal appears to conflict with architecture. This is evidence expansion and requires a compact reason.
3. A current skill input is `AGENTS.md` or `CONSTITUTION.md`. It may be classified as standing operating instructions or conditional governance evidence, but removal or downgrade needs rationale.
4. A proposal-side M1 implementation wants to edit `implement` because the proposal includes future guidance for it. M1 must reject or defer that edit to M2.
5. M1 updates `spec`. M1 selected validation must include `skills/spec/SKILL.md`; otherwise it must omit that path.
6. M2 runs later. M2 selected validation includes `skills/implement/SKILL.md` and `skills/code-review/SKILL.md`.
7. Static checks are added. They check stable concepts, not exact long paragraphs.
8. Token measurement shows a size increase. The result is diagnostic and review may ask for rationale, but no hard gate is introduced.
9. Bounded evidence is contradictory. The stage expands and does not record a false clean conclusion.
10. A full file is the review target. Full-file read remains valid without treating bounded evidence as a blocker.

## Non-goals

- Do not implement M2 `implement` or `code-review` evidence guidance in M1.
- Do not update `plan` in M1.
- Do not rewrite every skill.
- Do not add runtime enforcement or semantic read auditing.
- Do not add hard token gates.
- Do not implement lifecycle token-cost summaries.
- Do not implement full progressive-loading work.
- Do not change validation-selector behavior beyond scoped selected validation guidance.
- Do not change release validation, adapter packaging, generated-output source policy, or public adapter artifacts.
- Do not replace stage artifacts with chat-only summaries.

## Acceptance criteria

- The proposal status is settled to `accepted` using clean proposal-review evidence.
- `docs/workflows.md` defines the stage evidence access model.
- `proposal` and `proposal-review` include concise evidence-access sections.
- `spec` is updated only if immediate proposal-to-spec handoff requires it.
- M1 does not update `implement`, `code-review`, or `plan`.
- Participating skills distinguish default evidence, conditional evidence, and expansion evidence.
- Evidence expansion reasons are required only for substantive out-of-set reads.
- Bounded discovery is not treated as evidence expansion.
- Full-file reads remain allowed under the defined escape conditions.
- Touched skills preserve existing mandatory operating inputs or record rationale for removal or downgrade.
- M1 and M2 validation guidance remain separate.
- Static checks, if added, are concept-based.
- Static skill token measurement is run after canonical skill changes.
- No hard token gates, runtime enforcement, adapter packaging changes, release validation changes, or generated-output source model changes are introduced.

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

## Follow-on artifacts

- Spec-review approval: `docs/changes/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor-review-recording/reviews/spec-review-r1.md`
- Execution plan: `docs/plans/2026-05-14-stage-evidence-access-contracts-for-cost-bounded-rigor.md`

## Readiness

Approved after clean spec-review evidence. The execution plan owns the next planning handoff.
