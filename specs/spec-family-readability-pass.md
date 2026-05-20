# Spec-Family Readability Pass

## Status

approved

Approved after clean `spec-review` round 1.

## Related proposal

- [Spec-Family Readability Pass](../docs/proposals/2026-05-20-spec-family-readability-pass.md)

## Goal and context

This spec defines the contract for a presentation-only readability pass across the spec-family skills: `spec`, `spec-review`, and `test-spec`.

The change exists because, after `test-spec` contract normalization, all three skills share the published-skill design baseline but still expose some long prose enumerations, narrated closed enums, and uneven section ordering. The pass makes the installed skill text easier to scan without changing skill behavior, routing, rules, stop conditions, output obligations, lifecycle boundaries, or produced-artifact semantics.

This spec extends the existing skill readability and published skill contracts. It does not replace `specs/skill-contract.md` or `specs/skill-readability-contract.md`.

## Glossary

- `spec-family skills`: the canonical skills `spec`, `spec-review`, and `test-spec`.
- `presentation-only rewrite`: a change to ordering, tabulation, fencing, or wording shape that preserves the same normative meaning and output obligations.
- `section-order exception`: a recorded case where a skill keeps a section outside the shared order because strict alignment would weaken behavior clarity.
- `enum authority map`: a proof table identifying each changed closed enum's source, authoritative destination, exact values, and duplicate-handling rule.
- `content-preservation matrix`: a proof table mapping moved, tabulated, fenced, or reordered content from source location to destination location with preservation evidence.

## Examples first

Example E1: required sections become scannable without changing obligations
Given `skills/spec/SKILL.md` lists required spec sections in prose
When the readability pass tabulates those sections
Then the table contains the same section set and obligations
And `spec` still requires the same artifact shape.

Example E2: review verdict values are fenced without duplication
Given `skills/spec-review/SKILL.md` describes review-dimension verdicts as `pass`, `concern`, and `block`
When the readability pass creates an authoritative enum surface
Then those exact values remain available once in an authoritative block or table
And later instructions reference the enum rather than restating the full value set.

Example E3: family order yields to stop-condition visibility
Given strict family ordering would move a `test-spec` stop condition below normal output procedure
When implementation aligns sections
Then the stop condition remains visible before the normal output procedure
And the exception is recorded in the content-preservation matrix.

Example E4: generated adapter output is validated from canonical skills
Given a canonical spec-family skill changes
When the readability pass verifies generated output currency
Then current adapter output is rebuilt or validated from canonical `skills/`
And generated public adapter skill bodies are not hand-edited.

## Requirements

SFRP-R1. The implementation MUST change only the canonical spec-family skill sources `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, and `skills/test-spec/SKILL.md`, plus proof, validation, plan, review, or metadata artifacts required by the workflow.

SFRP-R2. The implementation MUST preserve every existing normative rule, stop condition, lifecycle boundary, routing behavior, closed enum value, output obligation, and required produced-artifact section in each changed skill.

SFRP-R3. The implementation MUST NOT change the readability, structure, required sections, or output expectations of artifacts produced by `spec`, `spec-review`, or `test-spec`.

SFRP-R4. The implementation MUST NOT introduce `assets/`, `references/`, `scripts/`, build-time partials, new packaging mechanisms, routing-description changes, or generated public adapter skill-body hand edits.

SFRP-R5. Before readability edits begin, the plan MUST confirm the normalized `test-spec` baseline is present: `version`, `schema-version`, Workflow role, surfaced stop conditions, fenced output skeleton, and accepted or closed behavior-preservation evidence for the normalization work.

SFRP-R6. If the normalized `test-spec` baseline is absent, implementation MUST stop and route back to normalization resolution instead of applying readability changes.

SFRP-R7. `spec` and `test-spec` required-section prose MUST be converted to scannable tables or equivalent table-authority surfaces that preserve the same section names, applicability, and obligations.

SFRP-R8. `spec-review` review-dimension guidance MUST be converted to a scannable table or equivalent table-authority surface that preserves the same dimensions and verdict guidance.

SFRP-R9. `test-spec` coverage expectations that are long enumerations MUST be converted to a scannable table or equivalent table-authority surface when doing so improves scanning without changing coverage obligations.

SFRP-R10. Each changed closed enum MUST have exactly one authoritative value surface in its skill, either a fenced block or a table authority.

SFRP-R11. The authoritative value surface for a closed enum MUST preserve the baseline spelling, capitalization, and membership of the enum values.

SFRP-R12. Later instructions in the same skill MUST reference the enum by name or placeholder instead of restating the full value set, unless the implementation records a safety reminder that does not introduce conflicting wording.

SFRP-R13. The implementation MUST record an enum authority map for `spec`, `spec-review`, and `test-spec` before code review.

SFRP-R14. The enum authority map MUST include skill, enum name, existing source, authoritative destination, exact values, and duplicate-handling rule.

SFRP-R15. Section ordering SHOULD align to the spec-family order where behavior clarity allows:

```text
1. Front matter
2. Purpose / short skill summary
3. Workflow role
4. Stop conditions / blocking conditions
5. Inputs and source-of-truth handling
6. Operating procedure / rules
7. Required artifact sections or review dimensions
8. Closed enums
9. Output expectations / fenced output skeleton
10. Validation and preservation checks
11. Handoff / next-stage boundaries
```

SFRP-R16. Section-order alignment MUST remain best effort and MUST yield to behavior parity, stop-condition visibility, lifecycle claim-boundary clarity, and validation-obligation visibility.

SFRP-R17. Any section-order exception MUST be recorded with skill, section, family-order expectation, chosen placement, and reason the exception preserves behavior clarity.

SFRP-R18. Stop conditions, must-not-claim boundaries, and validation obligations MUST remain visible before a reader follows the normal output procedure when that ordering affects behavior clarity.

SFRP-R19. The implementation MUST record a content-preservation matrix for every moved, tabulated, fenced, or reordered content block before code review.

SFRP-R20. The content-preservation matrix MUST include source content, existing location, new location, change type, and preservation proof.

SFRP-R21. Representative-input behavior parity MUST be performed for each changed skill and MUST supplement, not replace, the content-preservation matrix.

SFRP-R22. Behavior parity MUST compare verdict, output structure, required-section coverage, and requirement/example/edge-case coverage where the skill owns those outputs.

SFRP-R23. Any representative-output difference MUST be classified as `equivalent`, `improvement`, or `regression`; any `regression` MUST block readiness unless a later approved spec changes the behavior.

SFRP-R24. Current generated adapter output MUST be rebuilt or validated from canonical `skills/` after canonical spec-family skill changes, unless the plan records an explicit deferral with rationale.

SFRP-R25. Cold-read verification SHOULD confirm that a reader can locate required sections or review dimensions, closed enums, stop conditions, output expectations, validation obligations, and handoff boundaries in each changed skill without repository-internal context.

## Inputs and outputs

Inputs:

- accepted proposal `docs/proposals/2026-05-20-spec-family-readability-pass.md`;
- canonical skill sources for `spec`, `spec-review`, and `test-spec`;
- existing skill contracts in `specs/skill-contract.md` and `specs/skill-readability-contract.md`;
- review findings and resolution under `docs/changes/2026-05-20-spec-family-readability-pass/`.

Outputs:

- updated canonical spec-family skill text;
- enum authority map evidence;
- content-preservation matrix evidence;
- representative behavior-parity evidence;
- adapter currency validation or explicit deferral evidence.

## State and invariants

- The change is presentation-only.
- Canonical skill source remains under `skills/`.
- Generated adapter skill bodies remain derived output.
- The installed skills remain self-contained for user-facing normative behavior.
- Produced spec, review, and test-spec artifacts remain governed by their existing output skeletons and obligations.

## Error and boundary behavior

- If `test-spec` normalization baseline evidence is missing, stop before readability edits.
- If a proposed table cannot preserve source meaning clearly, keep the original structure and record the exception.
- If a closed enum's baseline value set is ambiguous, stop and route to spec or owner clarification before fencing it.
- If adapter validation cannot be run in the expected way, record the blocker or explicit deferral rationale before readiness is claimed.

## Compatibility and migration

Existing users should observe only easier-to-scan skill text. The skills' routing descriptions, generated artifact shapes, lifecycle statuses, stop conditions, and output obligations remain compatible.

Rollback is a Git revert of the presentation edits and any same-slice proof artifacts. No data migration, release archive rewrite, or adapter packaging migration is part of this change.

## Observability

The change is observable through:

- diffs to the three canonical skill files;
- enum authority map;
- content-preservation matrix;
- behavior-parity evidence;
- cold-read notes when performed;
- adapter validation or deferral evidence;
- review records and final verification report.

## Security and privacy

No new secrets, credentials, private data flows, authorization behavior, or external services are introduced. The implementation must not add repository-internal paths as required customer runtime dependencies in published skill text.

## Accessibility and UX

The user experience improvement is text scanability for installed skills. Tables and fenced enum blocks should make values, required sections, and boundaries easier to find in plain Markdown. No UI accessibility surface is otherwise affected.

## Performance expectations

No runtime performance behavior is affected. Token cost is not the driver for this change. A token increase is acceptable only when it preserves output quality and improves scanability under the existing skill-readability contract.

## Edge cases

EC1. A closed enum already appears in a fenced skeleton and narrated prose. The implementation must choose one authoritative surface and avoid duplicate full value lists.

EC2. A section-order move would make a stop condition less visible. The implementation must keep the safer order and record the exception.

EC3. `test-spec` contains normalized output-skeleton content that overlaps with required-section guidance. The implementation must preserve the skeleton's artifact contract and avoid implying new output obligations.

EC4. A table would require awkward rewording that could change meaning. The implementation must preserve source wording or defer that table row with a recorded exception.

EC5. Generated adapter validation exposes a baseline layout issue unrelated to this proposal. The plan or verification evidence must distinguish current-output currency from retroactive archive rewriting.

## Non-goals

- No changes to produced spec, spec-review, or test-spec artifact readability.
- No changes to routing descriptions.
- No changes to workflow stage order or lifecycle state semantics.
- No packaging through `assets/`, `references/`, or `scripts/`.
- No build-time partial or duplicated-block authoring mechanism.
- No generated public adapter skill-body hand edits.
- No retroactive rewrite of legacy adapter archives.

## Acceptance criteria

AC1. `spec`, `spec-review`, and `test-spec` each expose the targeted required-section, review-dimension, coverage, and enum information in tables or fenced blocks where this spec requires it.

AC2. Code review can trace every moved, tabulated, fenced, or reordered content block through a content-preservation matrix.

AC3. Code review can trace every changed closed enum through an enum authority map and confirm no duplicate full enum value set remains in the same skill.

AC4. Behavior parity for each changed skill is recorded and contains no unresolved `regression` classification.

AC5. Any section-order exception is recorded with the required fields and preserves behavior clarity.

AC6. Adapter output currency is validated from canonical skills or explicitly deferred with rationale.

AC7. The final diff does not include routing-description changes, packaging additions, produced-artifact readability changes, or generated public adapter skill-body hand edits.

## Open questions

None.

## Next artifacts

```text
spec-review
plan
plan-review
test-spec
implementation milestones or per-skill proof packets
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

Deferred follow-up candidates remain: spec-family packaging, build-time partials for duplicated blocks, produced spec and test-spec artifact readability, and broader lifecycle skill section-ordering conventions.

## Readiness

Approved for planning.
