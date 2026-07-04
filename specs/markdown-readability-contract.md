# Markdown Readability Contract for Generated RigorLoop Documents

## Status

approved

Approved after clean `spec-review-r1`.

## Related proposal

- [Markdown Readability Contract for Generated RigorLoop Documents](../docs/proposals/2026-07-04-markdown-readability-contract.md)
- Proposal review R1: [proposal-review-r1](../docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md), changes requested
- Proposal review R2: [proposal-review-r2](../docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r2.md), approved

## Goal and context

This spec defines a readability contract for generated and generator-shaped RigorLoop Markdown.
The contract exists because RigorLoop artifacts are reviewed both as rendered Markdown and as source diffs.
Generated Markdown that renders well can still be difficult to review when source lines split semantic phrases, workflow chains, commands, or proof claims.

The contract favors semantic source lines, stable skeletons, evidence-local structure, bounded deterministic validation, and audit-only treatment for subjective prose quality.
It explicitly rejects fixed-width line wrapping as the default prose rule and excludes manual-proof contract enforcement from this change.

## Glossary

- `generated Markdown`: Markdown emitted by a script, skill, template, projection, or repeatable agent-owned skeleton.
- `generator-shaped Markdown`: Markdown not fully script-generated, but expected to follow a stable skill-owned or template-owned structure.
- `semantic source line`: a physical Markdown source line that preserves one complete sentence, natural clause, list item, table row, command, marker, or other meaningful unit.
- `mechanical hard wrap`: a physical source line break inserted only to satisfy a column width, even when it splits a semantic unit.
- `readability validator`: the repository-owned Markdown readability validator at `scripts/validate-markdown-readability.py`.
- `generated region`: a Markdown region delimited by RigorLoop generated-region markers and owned by a canonical source or generator.
- `source owner`: the canonical source path, structured data owner, or generator that must be updated instead of hand-editing generated projection content.
- `audit-only check`: a check that reports possible readability issues without failing validation.
- `deterministic check`: a check with objective pass/fail behavior and representative fixtures.

## Examples first

Example E1: semantic source lines preserve review-critical prose
Given generated README prose contains the phrase `reviewable in Git`
When the Markdown source is emitted
Then the phrase stays on one semantic source line unless structure requires otherwise.

Example E2: long semantic line passes
Given a generated sentence is long but forms one complete semantic unit
When readability validation runs
Then generic line length alone does not fail the file.

Example E3: hard-wrap regression fails for changed README and `VISION.md` sections
Given a changed README or `VISION.md` section splits `AI agents` or `proposal to spec` across arbitrary physical source lines
When readability validation runs for the changed section
Then the known hard-wrap regression fails.

Example E4: generated regions declare ownership
Given a generated Markdown projection is present
When the region is emitted
Then it uses paired `rigorloop:generated` markers with stable `surface`, `source`, and optional `generator` metadata.

Example E5: manual-proof contracts remain out of scope
Given an artifact includes manual verification prose
When this readability contract is applied
Then the contract does not require a manual-proof contract block.

## Requirements

R1. Generated and generator-shaped Markdown SHOULD use semantic source lines for review-critical prose.

R2. Mechanical hard wrapping MUST NOT be the default formatting rule for generated or generator-shaped Markdown prose.

R3. A generated source line MUST NOT fail readability validation solely because it exceeds a fixed character width.

R4. The readability contract MUST NOT define or enforce a universal Markdown line-length limit.

R5. Human-facing generated prose SHOULD use one complete sentence per source line when practical.

R6. Long human-facing generated sentences SHOULD use one natural clause per source line when splitting improves source review.

R7. Generated list content SHOULD keep one complete list item per Markdown bullet.

R8. Generated Markdown tables MUST keep one complete table row per physical source line.

R9. Generated commands MUST be copyable in fenced code blocks or table-owned command rows.

R10. Dense generated prose that contains workflow chains, decision matrices, command sequences, mappings, or multiple conditions SHOULD use bullets, numbered steps, tables, diagrams, or fenced command blocks instead of mid-sentence wrapping.

R11. Substantial generated artifact classes MUST have a skeleton, template, or required structure before broad generation depends on them.

R12. Skeletons and templates MUST own output shape, not policy.
Policy remains in the governing spec, skill, workflow guide, or schema.

R13. Lifecycle and review artifacts SHOULD start with a concise result or status block when generated or generator-shaped.

R14. Review result blocks SHOULD identify skill, review status, material findings, recording status, review record, review log, review resolution, open blockers, and immediate next stage when applicable.

R15. Non-review status blocks SHOULD identify artifact status, scope, owner skill or source owner, last update, and related artifacts when applicable.

R16. Generated mapping content SHOULD use stable IDs instead of vague prose references.

R17. Requirement coverage, command ledgers, milestone proof maps, review finding summaries, release surface inventories, risk matrices, and decision logs SHOULD be represented as tables when generated.

R18. Proof-bearing generated command references MUST be fenced or table-owned.

R19. Proof-bearing command rows SHOULD include command ID, command string, owner, when required, failure behavior, evidence artifact, and safe-mode or side-effect boundary.

R20. Manual-proof contracts MUST NOT be introduced or enforced by this change.

R21. Generated regions MUST use the canonical marker shape:

```md
<!-- rigorloop:generated:start surface=<surface-id> source=<canonical-source> generator=<generator-id> -->
...
<!-- rigorloop:generated:end surface=<surface-id> -->
```

R22. The `surface` marker value MUST be stable and unique within the containing file.

R23. Generated-region start and end markers MUST use matching `surface` values.

R24. The `source` marker value MUST identify the canonical source path or structured data owner.

R25. The `generator` marker value SHOULD identify the generator when a generator script or repeatable generator exists.

R26. The `generator` marker value MAY be omitted only when no generator script or repeatable generator exists yet.

R27. Generated-region content MUST be changed by updating the source owner or generator rather than hand-editing the projection.

R28. `scripts/validate-markdown-readability.py` MUST be the owner script for deterministic Markdown readability validation.

R29. Existing guide, skill, artifact, or release validators MAY compose `scripts/validate-markdown-readability.py` for relevant paths.

R30. Composed validators MUST NOT become the policy owner for Markdown readability.

R31. The downstream implementation spec and plan details MAY define field validation details, path selection, parser behavior, and integration mechanics without moving policy ownership out of the readability validator.

R32. The first enforcement slice MUST apply README and `VISION.md` semantic source-line checks only to changed sections.

R33. Untouched historical README and `VISION.md` sections MUST remain audit-only unless a separate migration decision approves reflow.

R34. Generated README vision-block content MUST be fixed through `VISION.md` or the generator, not by hand-editing the generated projection.

R35. Historical Markdown documents MUST NOT be mass-reflowed by this change.

R36. Long-line and dense-paragraph checks MUST start as audit-only unless a narrow deterministic check has representative pass and fail fixtures.

R37. Generic long-line checks MUST remain audit-only.

R38. A warning MAY graduate to a failing check only when it is deterministic, fixture-backed, low-noise across Markdown block types, and scoped to selected artifact classes or changed sections.

R39. Readability validation MUST exclude code fences, tables, HTML blocks, link reference definitions, and generated regions from prose-line checks unless the check is explicitly validating those structures.

R40. Known README and `VISION.md` hard-wrap regressions SHOULD have failing fixtures.

R41. Long complete semantic-line examples SHOULD have passing fixtures.

R42. Generated-region marker pairing MUST have positive and negative validation coverage.

R43. Unfilled placeholders in generated or generator-shaped documents SHOULD fail deterministic validation where the artifact class has a stable skeleton.

R44. Representative generated documents SHOULD pass a source-form cold read where a reviewer can quickly find status, blockers, commands, evidence, and next stage.

R45. Diagrams SHOULD be encouraged for workflow order, state transitions, artifact ownership, data flow, runtime flow, and boundary-heavy architecture when they reduce cognitive load.

R46. Diagrams MUST NOT be required when a table, list, or prose structure is clearer.

R47. Diagram nodes SHOULD map to real artifacts, stages, components, actors, or states.

R48. Decorative diagrams MUST NOT be required or encouraged by this contract.

R49. Generated adapter output MUST be regenerated or validated from canonical authored sources when affected by readability changes.

R50. Generated public adapter bodies MUST NOT be hand-edited to satisfy this contract.

## Inputs and outputs

Inputs:

- accepted proposal `docs/proposals/2026-07-04-markdown-readability-contract.md`;
- approved `proposal-review-r2`;
- learn records for Markdown source-line recurrence;
- README and `VISION.md` source content;
- canonical skills, skeleton assets, templates, scripts, and generated adapter support surfaces;
- existing validator and lifecycle contracts.

Outputs:

- this feature spec;
- a matching test spec;
- architecture or ADR evidence if the downstream design introduces shared generated-region ownership or validator architecture decisions;
- an execution plan;
- validator, fixture, skeleton, skill, and generated-output changes during implementation;
- review, rationale, and verification evidence.

## State and invariants

- Semantic source lines are the preferred source-review convention for generated prose.
- Fixed-width wrapping is not a correctness criterion.
- The readability validator owns deterministic readability checks.
- Existing validators compose readability checks for their relevant paths.
- Generated-region markers identify source ownership.
- Manual-proof contracts remain out of scope.
- Historical Markdown remains stable unless migration is separately approved.

## Error and boundary behavior

- Unknown generated-region marker shapes fail only where generated-region validation is in scope.
- Mismatched generated-region `surface` values fail marker-pair validation.
- Missing required marker metadata fails when the region claims RigorLoop-generated ownership.
- Changed README or `VISION.md` sections with known hard-wrap regressions fail when changed-section enforcement applies.
- Generic line length does not fail validation.
- Subjective clause quality, dense prose, and diagram usefulness stay audit-only unless narrowed into deterministic fixture-backed checks.
- Generated-region hand edits fail only when projection consistency or source-owner validation can prove the edit bypassed the canonical source.

## Compatibility and migration

This change applies to new generated documents and changed current documents first.
Historical Markdown remains audit-only.
No mass reflow is part of this change.

Rollback is to remove or disable the readability validator integration, restore prior skeleton or skill shapes, and remove generated-region marker enforcement introduced by the implementation.
Generated adapter output must be rebuilt from canonical authored sources rather than hand-edited.

## Observability

The change is observable through:

- readability validator diagnostics with stable check IDs;
- README and `VISION.md` hard-wrap fixtures;
- generated-region marker fixtures;
- placeholder and skeleton-shape diagnostics;
- representative generated-doc cold-read evidence;
- review records, change metadata, and verification artifacts.

## Security and privacy

This contract operates on repository-local Markdown, templates, scripts, and fixtures.
It must not expose secrets, credentials, private machine paths, or network-only state.
Generated-region `source` and `generator` metadata should use repository-relative or approved canonical identifiers rather than machine-local paths.

## Accessibility and UX

No end-user UI is introduced.
Contributor-facing Markdown should remain readable in plain source and rendered form.
Diagrams, when used, should reduce cognitive load and not replace required text or table evidence.

## Performance expectations

Readability validation should use bounded parsing and path-scoped checks.
Changed-section README and `VISION.md` enforcement should avoid scanning or reflowing unrelated historical content.
Audit-only diagnostics should avoid excessive output and should summarize findings with stable check IDs and paths.

## Edge cases

EC1. A long sentence that is one semantic unit passes generic line-length review.

EC2. A code fence contains long commands; prose-line checks ignore the fence.

EC3. A Markdown table has long rows; prose-line checks ignore the table row.

EC4. A generated region lacks matching `surface` values; generated-region marker validation fails.

EC5. A README changed section splits `proposal to spec` across lines; changed-section hard-wrap validation fails.

EC6. A historical document has old hard wrapping but is untouched; first-slice validation reports audit-only or ignores it according to selector scope.

EC7. A generated README vision block needs correction; the fix updates `VISION.md` or the generator rather than hand-editing the projection.

EC8. A diagram would decorate rather than clarify; the artifact uses a table or list instead.

## Non-goals

- Do not impose a universal line-length limit.
- Do not auto-format all Markdown.
- Do not mass-reflow historical Markdown.
- Do not add or enforce manual-proof contracts.
- Do not make subjective prose clarity a failing validator by default.
- Do not hand-edit generated public adapter bodies.
- Do not require diagrams.
- Do not make learn sessions the authoritative formatting policy.

## Acceptance criteria

AC1. The spec defines semantic source-line guidance without a fixed line-length limit.

AC2. The spec assigns readability validation ownership to `scripts/validate-markdown-readability.py`.

AC3. The spec permits existing validators to compose readability validation without owning policy.

AC4. The spec defines canonical generated-region marker syntax.

AC5. The spec limits first-slice README and `VISION.md` enforcement to changed sections.

AC6. The spec excludes manual-proof contracts.

AC7. The spec keeps historical Markdown audit-only unless migration is separately approved.

AC8. The spec defines deterministic checks and audit-only warning boundaries.

AC9. The spec requires or recommends fixtures for known hard-wrap failures, long semantic lines, marker pairing, and block-type exclusions.

AC10. The spec encourages diagrams only when they reduce cognitive load and never requires them.

AC11. The spec identifies generated adapter output as regenerated or validated from canonical authored sources.

AC12. The spec is ready for `spec-review` with no open proposal-level decisions.

## Open questions

None.

## Next artifacts

```text
spec-review
architecture assessment
architecture or ADR if required
plan
plan-review
test-spec
test-spec-review
```

## Follow-on artifacts

- Spec review R1: `../docs/changes/2026-07-04-markdown-readability-contract/reviews/spec-review-r1.md`

## Readiness

Approved after clean `spec-review-r1`; architecture assessment is `architecture-not-required`; ready for `plan`.
