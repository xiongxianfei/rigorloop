# Documentation Source Formatting

## Status

approved

## Related proposal

- Proposal: [Semantic Source-Line Contract for Review-Critical Markdown](../docs/proposals/2026-06-24-semantic-source-line-contract.md)
- Change record: [2026-06-24-semantic-source-line-contract](../docs/changes/2026-06-24-semantic-source-line-contract/change.yaml)

## Goal and context

RigorLoop review-critical Markdown must be reviewable from source, not only after rendering.
This spec defines how covered Markdown files preserve semantic source units, how validation distinguishes deterministic violations from audit warnings, and how generated-content ownership is preserved.

The contract exists because repeated corrections showed that arbitrary hard wrapping can split meaning-bearing phrases, lifecycle chains, commands, and public positioning even when rendered Markdown appears acceptable.

## Glossary

- Semantic source unit: a complete meaning-bearing Markdown source unit, such as one sentence, list item, table row, command, heading, blockquote unit, or lifecycle chain.
- Mechanical wrap: a physical line break introduced only because a line reached an arbitrary column threshold.
- Tier A: first-slice enforcement files, currently `README.md` and `VISION.md`.
- Tier B: first-slice audit files, currently `skills/**/SKILL.md` and `docs/changes/**/explain-change.md`.
- Tier C: files excluded from first-slice enforcement.
- Generated or marker-owned region: Markdown whose source of truth is another canonical file or generator.
- Deterministic violation: a source-line defect precise enough for validation failure.
- Audit warning: a suspicious or ambiguous break requiring human review rather than failure.

## Examples first

Example E1: complete sentence source line
Given a Tier A Markdown paragraph
When a sentence is long but complete on one physical source line
Then the validator accepts the line because length alone is not a defect.

Example E2: mechanical mid-sentence wrap
Given a Tier A Markdown paragraph
When a complete sentence is split across physical lines only because it reached a column threshold
Then the validator reports a deterministic error with file, line range, suspected unit, reason, and suggested actions.

Example E3: structured dense prose
Given dense lifecycle prose in a covered file
When the author rewrites it as a list or diagram instead of mechanically wrapping it
Then the validator accepts the structure when each item preserves a semantic unit.

Example E4: generated README marker region
Given README content generated from `VISION.md`
When source-line shape needs correction
Then the correction is made in `VISION.md` or the synchronization mechanism, not by hand-editing the generated README block.

Example E5: Tier B audit
Given a canonical skill `SKILL.md`
When the validator finds a suspicious line break that is not a deterministic prohibited pattern
Then the validator emits an audit warning without failing the repository in the first slice.

## Requirements

R1. Covered human-authored Markdown prose MUST preserve semantic source units rather than split lines solely at an arbitrary column threshold.

R2. The first-slice enforcement scope MUST be limited to human-authored prose in `README.md` and `VISION.md`.

R3. The first-slice audit scope MUST include `skills/**/SKILL.md` and `docs/changes/**/explain-change.md`.

R4. First-slice enforcement MUST NOT include `specs/**`, `docs/plans/**`, `docs/changes/**/reviews/**`, `docs/learn/**`, generated output, historical release evidence, or third-party documentation.

R5. Long source lines MUST be allowed when they contain a complete semantic source unit.

R6. Covered ordinary prose SHOULD use one complete sentence per physical source line when practical.

R7. Long sentences MAY be split at deliberate clause boundaries when the break improves source review, avoids splitting a compound term or lifecycle transition, and remains understandable without rendered reflow.

R8. The validator MUST fail Tier A deterministic violations and MUST NOT fail solely because a line exceeds a fixed length.

R9. The validator MUST report ambiguous clause-level, punctuation, abbreviation, or inline-Markdown cases as audit warnings rather than deterministic errors.

R10. The validator MUST identify Markdown blocks before evaluating prose.

R11. The validator MUST exclude or separately handle fenced code blocks, indented code, tables, HTML blocks, link definitions, headings, thematic breaks, generated or marker-owned regions, URLs, long inline code, explicit Markdown hard breaks, and YAML frontmatter.

R12. Deterministic violations MUST include ordinary prose split mid-phrase, commands split outside valid fenced or continuation structures, lifecycle chains split between connected elements, mechanically continued list items, and named regression phrases such as `AI agents` and `proposal to spec`.

R13. The validator MUST emit diagnostics containing the file, line range, suspected split unit, reason, and suggested actions to join lines, rewrite the sentence, or convert prose to structured Markdown.

R14. The validator MUST be non-mutating and MUST NOT rewrite prose.

R15. Generated or marker-owned content MUST preserve current source ownership; fixes belong in the canonical source or generator and then in synchronized output when applicable.

R16. Contributor-facing guidance MUST keep the full contract in this spec, put only the concise authoring summary and validation command in `CONTRIBUTING.md`, and allow `docs/workflows.md` to link to that summary without duplicating the full contract.

R17. Formatter configuration MUST prevent mechanical rewrap from reintroducing violations by disabling Markdown line-length enforcement such as `MD013` for covered files and configuring Prettier `proseWrap: "preserve"` repository-wide or for Tier A and Tier B paths.

R18. Source-form review for changed covered Markdown MUST inspect rendered output, physical source lines, the complete changed section, phrase integrity, lifecycle readability, command copyability, vocabulary, marker ownership, and prose validation output before PR handoff.

R19. Expansion beyond Tier A enforcement MUST require a separate evidence-based decision.

## Inputs and outputs

Inputs:

- Markdown files in Tier A and Tier B.
- Markdown block structure in each evaluated file.
- Generated or marker-region ownership metadata or markers where present.
- Validator mode, expected to include audit and enforcement modes.
- Optional path selection for targeted validation.

Outputs:

- Non-mutating validation diagnostics.
- Tier A enforcement errors for deterministic violations.
- Audit warnings for Tier B and ambiguous cases.
- Review evidence or validation notes for changed covered sections.

## State and invariants

- The authoritative documentation source-formatting contract lives in this spec.
- Learn records remain historical rationale and examples, not normative owners.
- Rendered Markdown semantics are unchanged by this contract.
- The validator never rewrites source.
- Fixed-width line limits are not a proxy for semantic correctness.
- Generated or marker-owned regions keep their current ownership.
- Tier A whole-file enforcement starts only after the Tier A baseline is cleaned.

## Error and boundary behavior

- A Tier A deterministic violation fails enforcement mode.
- A Tier B suspicious break produces an audit warning in the first slice unless it matches a deterministic prohibited pattern selected for failure.
- Ambiguous punctuation, abbreviations, inline Markdown, and clause boundaries produce warnings.
- Tables, code fences, long URLs, inline code, link definitions, frontmatter, and generated-marker blocks are not misclassified as prose violations.
- Missing ownership metadata for a marker-owned region must not cause direct edit suggestions for generated content.
- Validator parse uncertainty should degrade to warnings unless a deterministic rule still applies.

## Compatibility and migration

- No historical Markdown migration is required in the first slice.
- The implementation cleans only current Tier A baseline violations needed for enforcement.
- Existing README marker validation, vocabulary validation, guide-system validation, and skill validation remain active.
- Existing Markdown rendering behavior is preserved.
- Rollback disables enforcement before removing the validator and does not restore mechanical wrapping solely to match old line width.

## Observability

- Validator diagnostics identify the file, line range, suspected split unit, reason, severity, and suggested actions.
- Validation results should be recordable in change metadata, plan validation notes, review records, or PR handoff evidence.
- Audit warnings for changed covered files require manual disposition when the workflow stage requires source-form review evidence.

## Security and privacy

The contract introduces no new secrets, authentication, authorization, or private-data handling.
Validator diagnostics must not execute Markdown content, follow embedded links, run scripts, or process active document objects.

## Accessibility and UX

Rendered Markdown accessibility is unchanged.
Contributor UX changes are limited to source authoring guidance, validator diagnostics, and review procedure.
Diagnostics should be specific enough to support manual repair without requiring automatic rewrite.

## Performance expectations

The validator should support targeted validation for selected paths and should avoid repository-wide prose scanning unless explicitly requested.
Normal output should summarize results and expand details only for errors, warnings, or requested verbose output.

## Edge cases

EC1. A long complete source line passes even if it exceeds a common editor width.

EC2. A Markdown paragraph containing multiple source lines passes when each physical line is a complete sentence or deliberate semantic unit.

EC3. A sentence split between a noun phrase such as `AI agents` fails when the split matches a deterministic regression pattern.

EC4. A lifecycle chain split between connected stages fails when the split obscures order.

EC5. A command split in prose fails, while the same command in a fenced code block passes.

EC6. Tables are evaluated as rows, not prose paragraphs.

EC7. README marker content generated from `VISION.md` is validated without suggesting direct hand edits to the marker-owned region.

EC8. A deliberate clause break after a semicolon, colon, or top-level conjunction may pass or warn depending on rule confidence, but it is not treated as a fixed-width violation.

EC9. A formatter or editor that mechanically rewraps a previously valid Tier A semantic line produces a failing Tier A regression fixture.

EC10. Specs, plans, review records, learn sessions, historical evidence, and third-party documentation remain outside first-slice enforcement.

## Non-goals

- No fixed 80-, 88-, 100-, or other column limit for prose.
- No repository-wide Markdown reflow.
- No automatic prose rewriting.
- No general grammar, tone, or writing-quality checker.
- No change to Markdown rendering semantics.
- No first-slice enforcement for specs, plans, review records, logs, or historical evidence.
- No direct hand edits to generated README marker content.
- No workflow stage-order changes.

## Acceptance criteria

AC1. The contract distinguishes semantic source-line breaks from mechanical hard wrapping.

AC2. No fixed prose line-length limit is introduced.

AC3. README and VISION are the only first-slice enforcement surfaces.

AC4. Canonical skills and explain-change artifacts remain audit-only in the first slice.

AC5. Generated and marker-owned regions retain their current source ownership.

AC6. Deterministic mechanical wraps fail with line-specific diagnostics.

AC7. Ambiguous semantic breaks produce warnings rather than false failures.

AC8. Tables, code fences, links, and structural Markdown are not misclassified as prose violations.

AC9. The validator performs no automatic reflow.

AC10. README recurrence and `AI agents` / lifecycle-chain failures have direct regression fixtures.

AC11. Existing README marker, vocabulary, guide-system, and skill validation remain active.

AC12. Historical Markdown is not migrated in this slice.

AC13. Changed covered sections receive source-form review before PR handoff.

AC14. Expansion beyond Tier A requires a separate evidence-based decision.

AC15. A Tier A file fails when a previously passing semantic line is later mechanically wrapped by an editor or tool.

## Open questions

None.

## Next artifacts

```text
spec-review
architecture assessment
plan
plan-review
test-spec
implementation
code-review
explain-change
verify
pr
```

Architecture is expected to be assessed after spec review.
Architecture artifacts are not expected unless implementation introduces a shared Markdown parsing subsystem or changes generated-content ownership.

## Follow-on artifacts

- Spec review: [spec-review-r1](../docs/changes/2026-06-24-semantic-source-line-contract/reviews/spec-review-r1.md)

## Readiness

Approved.
Architecture assessment is recorded as not required for the first implementation slice.
