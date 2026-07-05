# Documentation Source Formatting Test Spec

## Status

active

## Related spec and plan

- Spec: [Documentation Source Formatting](documentation-source-formatting.md)
- Plan: [Semantic Source-Line Contract Plan](../docs/plans/2026-06-24-semantic-source-line-contract.md)
- Architecture/ADRs: not applicable; architecture assessment recorded as `architecture-not-required` in [change.yaml](../docs/changes/2026-06-24-semantic-source-line-contract/change.yaml)

## Testing strategy

Unit tests cover Markdown block segmentation, semantic-unit classification, deterministic violation detection, audit-warning classification, diagnostics, and non-mutating behavior.
Integration tests cover the CLI modes, path selection, generated-marker ownership handling, selected-validation routing, existing validator composition, and Tier A/Tier B/Tier C behavior.
Smoke tests run the validator against current Tier A files after baseline cleanup.
Manual checks cover rendered README and VISION meaning, generated-marker ownership, and changed-section source-form review where automation cannot safely prove intent.
Contract tests cover requirement-to-diagnostic shape, first-slice coverage boundaries, formatter guardrails, and no fixed-width line-length behavior.
Migration checks prove historical Markdown is not mass-reformatted and excluded paths do not become first-slice enforcement targets.
End-to-end browser or UI tests are not applicable because this is a repository validation and source-authoring contract.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1 | T1, T2, T3, T4 | unit, contract | Proves semantic units are preserved and mechanical wraps are rejected. |
| R2 | T5, T18 | integration | Proves Tier A enforcement is limited to README and VISION human-authored prose. |
| R3 | T6, T18 | integration | Proves Tier B audit scope for skills and explain-change artifacts. |
| R4 | T7, T18 | integration, migration | Proves Tier C exclusions stay outside first-slice enforcement. |
| R5 | T2, T8 | unit, contract | Proves long complete source lines pass and line length alone is not an error. |
| R6 | T3, T16 | unit, manual | Proves sentence-per-line source paragraphs are accepted and reviewable. |
| R7 | T9, T16 | unit, manual | Proves deliberate clause boundaries are allowed or warned without fixed-width failure. |
| R8 | T1, T2, T10 | unit, contract | Proves Tier A deterministic failures and no fixed line-length rule. |
| R9 | T9, T11 | unit | Proves ambiguous cases warn instead of failing. |
| R10 | T12 | unit | Proves Markdown blocks are segmented before prose evaluation. |
| R11 | T12, T13 | unit, integration | Proves exclusions for code, tables, HTML, links, headings, hard breaks, frontmatter, URLs, and inline code. |
| R12 | T1, T4, T10, T14 | unit, contract | Proves deterministic prohibited patterns and named regressions fail. |
| R13 | T15 | unit, contract | Proves diagnostics include file, line range, suspected unit, reason, severity, and suggested actions. |
| R14 | T17 | integration | Proves validator never mutates input files. |
| R15 | T19, T20 | integration, manual | Proves generated or marker-owned content keeps canonical ownership. |
| R16 | T21 | contract, manual | Proves guidance points to the spec and concise contributor summary without duplicate contract ownership. |
| R17 | T22 | contract | Proves formatter guardrails disable fixed line-length enforcement and preserve prose wrapping. |
| R18 | T16, T23 | manual, contract | Proves source-form review evidence covers rendered output, physical lines, section scope, vocabulary, command copyability, and marker ownership. |
| R19 | T7, T24 | contract | Proves expansion beyond Tier A requires a separate evidence-based decision. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 complete sentence source line | T2, T8 | Long semantic lines pass. |
| E2 mechanical mid-sentence wrap | T1, T15 | Deterministic error and diagnostic shape. |
| E3 structured dense prose | T3, T4 | Bullet/list alternatives pass when semantic units are intact. |
| E4 generated README marker region | T19, T20 | Canonical-source ownership is preserved. |
| E5 Tier B audit | T6, T11 | Suspicious Tier B breaks warn without repository failure. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 long complete source line | T2, T8 | No fixed-width failure. |
| EC2 multi-line paragraph with semantic lines | T3 | Sentence-per-line paragraph passes. |
| EC3 `AI agents` split | T10 | Named regression fails. |
| EC4 lifecycle chain split | T14 | Connected lifecycle elements fail when split mechanically. |
| EC5 command split versus fenced command | T4 | Prose split fails; fenced command passes. |
| EC6 tables as rows | T12 | Table rows are not prose paragraphs. |
| EC7 README marker ownership | T19, T20 | No direct edit suggestion for marker-owned content. |
| EC8 deliberate clause break | T9, T11 | Positive-list cases pass or warn; not fixed-width failure. |
| EC9 editor/tool rewrap | T10 | Previously valid Tier A semantic line fails after mechanical rewrap. |
| EC10 excluded historical paths | T7, T18 | Tier C paths remain outside first-slice enforcement. |

## Test cases

### T1. Tier A mechanical mid-sentence wrap fails

- Covers: R1, R8, R12, E2, EC2
- Level: unit
- Fixture/setup: Tier A fixture with one sentence split across physical lines only at a visual column boundary.
- Steps: Run the validator in enforce mode against the fixture.
- Expected result: Exit is failing and diagnostic identifies a deterministic mechanical-wrap error.
- Failure proves: The validator cannot enforce the core semantic-line contract.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T2. Long complete source line passes

- Covers: R5, R8, E1, EC1
- Level: unit
- Fixture/setup: Tier A fixture with a long but complete sentence on one physical line.
- Steps: Run the validator in enforce mode against the fixture.
- Expected result: Exit is passing and no line-length diagnostic appears.
- Failure proves: The implementation reintroduced fixed-width prose validation.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T3. Semantic sentence-per-line paragraph passes

- Covers: R1, R6, E3, EC2
- Level: unit
- Fixture/setup: Markdown paragraph containing multiple physical lines, each a complete sentence.
- Steps: Run the validator in enforce mode against the fixture.
- Expected result: Exit is passing.
- Failure proves: The validator incorrectly requires one paragraph per source line.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T4. Structured alternatives and command boundaries

- Covers: R1, R12, E3, EC5
- Level: unit
- Fixture/setup: Paired fixtures for dense prose rewritten as bullets, a command split as prose, and the same command in a fenced code block.
- Steps: Run the validator against each paired fixture.
- Expected result: Bullet structure and fenced command pass; command split in prose fails.
- Failure proves: The validator cannot distinguish semantic structure from mechanical continuation.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T5. Tier A enforcement scope

- Covers: R2, AC3
- Level: integration
- Fixture/setup: Path-selection fixtures for `README.md`, `VISION.md`, and unrelated Markdown.
- Steps: Run enforce-mode path selection.
- Expected result: README and VISION human-authored prose are enforceable; unrelated Markdown is not Tier A enforcement.
- Failure proves: First-slice enforcement scope is too broad or too narrow.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T6. Tier B audit scope

- Covers: R3, E5
- Level: integration
- Fixture/setup: Suspicious-break fixtures under `skills/example/SKILL.md` and `docs/changes/example/explain-change.md`.
- Steps: Run audit or selected validation for Tier B paths.
- Expected result: Warnings are emitted without repository-failing enforcement.
- Failure proves: Tier B audit-only behavior is not preserved.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T7. Tier C exclusion and expansion guard

- Covers: R4, R19, EC10
- Level: integration
- Fixture/setup: Fixtures under `specs/`, `docs/plans/`, `docs/changes/example/reviews/`, `docs/learn/`, historical release evidence, and third-party documentation.
- Steps: Run path selection and selected validation.
- Expected result: Tier C paths do not receive first-slice enforcement.
- Failure proves: The implementation silently expanded beyond the approved first slice.
- Automation location: `python scripts/test-documentation-prose-validator.py` and `python scripts/test-select-validation.py`

### T8. No fixed line-length rule

- Covers: R5, R8, AC2
- Level: contract
- Fixture/setup: Fixture with long URLs, long inline code, and long semantic prose lines.
- Steps: Run enforce mode and inspect diagnostics.
- Expected result: No diagnostic is emitted solely because of character count.
- Failure proves: A fixed line-length rule is substituting for semantic validation.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T9. Deliberate clause boundaries

- Covers: R7, R9, EC8
- Level: unit
- Fixture/setup: Fixtures with breaks after semicolons, colons, dashes, and before top-level coordinating conjunctions.
- Steps: Run audit and enforce mode.
- Expected result: Positive-list clause breaks pass or produce warnings, not deterministic fixed-width failures.
- Failure proves: Human-review-owned clause breaks are being over-enforced.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T10. Named regression and editor rewrap fixtures

- Covers: R12, AC10, AC15, EC3, EC9
- Level: unit
- Fixture/setup: Fixtures for `AI` / `agents`, `proposal` / `to spec`, `reviewable` / `in Git`, and a previously passing Tier A line mechanically rewrapped by an editor.
- Steps: Run enforce mode against failing fixtures and corrected paired fixtures.
- Expected result: Mechanical and named-regression fixtures fail; corrected semantic forms pass.
- Failure proves: The known recurrence patterns are not protected.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T11. Ambiguous cases warn

- Covers: R9, E5, EC8
- Level: unit
- Fixture/setup: Fixtures with abbreviations, inline Markdown, unusual punctuation, and possible clause-level breaks.
- Steps: Run audit and enforce mode.
- Expected result: Ambiguous cases produce warnings rather than deterministic failures unless another deterministic rule applies.
- Failure proves: The validator is too aggressive for review-owned prose judgment.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T12. Markdown block segmentation

- Covers: R10, R11, EC6
- Level: unit
- Fixture/setup: Mixed Markdown file containing headings, paragraphs, tables, fenced code, indented code, HTML blocks, thematic breaks, link definitions, frontmatter, and blockquotes.
- Steps: Run block segmentation tests and validator checks.
- Expected result: Prose rules apply only to eligible prose blocks; table rows and code blocks are handled separately or excluded.
- Failure proves: The validator is running broad prose regexes over whole files.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T13. Structural exclusions

- Covers: R11, AC8
- Level: integration
- Fixture/setup: Files with URLs, long inline code, explicit Markdown hard breaks, link definitions, YAML frontmatter, and HTML blocks.
- Steps: Run enforce mode.
- Expected result: Structural Markdown is not misclassified as prose violation.
- Failure proves: Exclusion handling is incomplete.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T14. Lifecycle chain split fails

- Covers: R12, AC10, EC4
- Level: unit
- Fixture/setup: Paired lifecycle-chain fixtures where connected workflow stages are mechanically split versus structured as an intact list or diagram.
- Steps: Run enforce mode.
- Expected result: Mechanical lifecycle-chain split fails; structured alternative passes.
- Failure proves: Lifecycle order remains vulnerable to source-line wrapping.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T15. Diagnostic shape

- Covers: R13, E2, AC6
- Level: contract
- Fixture/setup: Fixture with one deterministic Tier A violation and one audit warning.
- Steps: Capture CLI output.
- Expected result: Diagnostics include file, line range, suspected split unit, reason, severity, and suggested actions.
- Failure proves: Validator output is not actionable enough for review or PR handoff.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T16. Source-form review checklist

- Covers: R6, R7, R18, AC13
- Level: manual
- Fixture/setup: Changed covered Markdown section in README or VISION.
- Steps: Inspect rendered output, `nl -ba` source lines, complete changed section, phrase integrity, lifecycle readability, command copyability, vocabulary, marker ownership, and validator output.
- Expected result: Review evidence records that the complete changed section was inspected and any audit warnings were dispositioned.
- Failure proves: The process can still fix only a cited line while leaving surrounding source mechanically wrapped.
- Automation location: manual checklist in review or PR evidence

### T17. Validator is non-mutating

- Covers: R14, AC9
- Level: integration
- Fixture/setup: Temporary copy of passing and failing fixture files.
- Steps: Record file hashes, run audit and enforce mode, record hashes again.
- Expected result: File contents are unchanged.
- Failure proves: The validator is acting as an autoformatter.
- Automation location: `python scripts/test-documentation-prose-validator.py`

### T18. Selected validation routing

- Covers: R2, R3, R4, AC3, AC4, AC11
- Level: integration
- Fixture/setup: `scripts/select-validation.py` changed-file scenarios for Tier A, Tier B, Tier C, README marker content, and guide surfaces.
- Steps: Run selected-validation tests.
- Expected result: Tier A selects enforcing prose validation; Tier B selects audit validation; Tier C does not select first-slice enforcement; existing README, marker, guide-system, and skill checks still route where applicable.
- Failure proves: Validation integration is not scoped to the accepted first slice or displaced existing checks.
- Automation location: `python scripts/test-select-validation.py`

### T19. Generated marker ownership

- Covers: R15, E4, EC7, AC5
- Level: integration
- Fixture/setup: README marker-region fixture with canonical `VISION.md` source reference.
- Steps: Run prose validation and marker validation.
- Expected result: Generated projection is validated or skipped according to ownership rules and diagnostics do not suggest direct generated-block edits.
- Failure proves: Marker-owned content can drift or be hand-edited contrary to source ownership.
- Automation location: `python scripts/test-documentation-prose-validator.py` and existing README marker validation

### T20. README and VISION behavior preservation

- Covers: R15, AC11, AC12
- Level: manual
- Fixture/setup: Current README and VISION after Tier A cleanup.
- Steps: Compare rendered README content, marker synchronization, VISION meaning, retired vocabulary checks, and no-migration diff scope.
- Expected result: Rendered meaning, marker ownership, vocabulary checks, and historical non-migration are preserved.
- Failure proves: Formatting enforcement changed content meaning or ownership.
- Automation location: `docs/changes/2026-06-24-semantic-source-line-contract/behavior-preservation.md`

### T21. Contributor guidance ownership

- Covers: R16
- Level: contract
- Fixture/setup: `CONTRIBUTING.md`, `docs/workflows.md`, and this spec.
- Steps: Inspect guidance text and run guide validation.
- Expected result: The spec owns the full contract, `CONTRIBUTING.md` has concise authoring summary and command, and `docs/workflows.md` links without duplicating the contract.
- Failure proves: Policy ownership can drift across multiple docs.
- Automation location: `python scripts/validate-guide-system.py` plus manual contract review

### T22. Formatter guardrails

- Covers: R17
- Level: contract
- Fixture/setup: Formatter or lint configuration files introduced or modified by implementation.
- Steps: Inspect configuration and run any repo-owned formatter/lint configuration tests if present.
- Expected result: Markdown line-length enforcement such as `MD013` is disabled for covered files and Prettier prose wrapping is preserved repository-wide or for Tier A/Tier B paths.
- Failure proves: Tooling can silently reintroduce mechanical wraps.
- Automation location: configuration review plus future validator/selection tests

### T23. Source-review evidence before PR

- Covers: R18, AC13
- Level: manual
- Fixture/setup: PR or pre-PR evidence for changed Tier A or Tier B Markdown.
- Steps: Confirm source-form review command and disposition are recorded in plan notes, explain-change, verify report, or PR handoff.
- Expected result: Changed covered sections have source-form review evidence before PR handoff.
- Failure proves: The validation exists but the review procedure can still be skipped.
- Automation location: manual verify evidence

### T24. Expansion requires separate decision

- Covers: R19, AC14
- Level: contract
- Fixture/setup: Proposed selected-validation or validator configuration that adds enforcement outside Tier A.
- Steps: Inspect routing/config changes and referenced artifacts.
- Expected result: Any enforcement expansion beyond README and VISION cites a separate accepted proposal or is rejected.
- Failure proves: First-slice scope can expand without evidence-based decision.
- Automation location: manual contract review and selected-validation tests

## Fixtures and data

- `tests/fixtures/documentation-prose/pass/`: semantic-line, long-line, structured-list, fenced-command, table, URL, inline-code, frontmatter, generated-marker, and Tier C exclusion fixtures.
- `tests/fixtures/documentation-prose/fail/`: mechanical-wrap, command-split, lifecycle-chain-split, `AI agents`, `proposal to spec`, `reviewable in Git`, and editor-rewrap fixtures.
- `tests/fixtures/documentation-prose/warn/`: ambiguous punctuation, abbreviation, inline-Markdown, and clause-break fixtures.
- Temporary copies for non-mutating hash checks.
- Current `README.md` and `VISION.md` as smoke-test targets after Tier A cleanup.

## Mocking/stubbing policy

Use temporary fixture directories and explicit path arguments instead of mutating repository files.
Do not mock filesystem writes for the non-mutating check; assert real file contents remain unchanged.
Do not mock selected-validation command selection; use the repository selection helper with changed-file scenarios.
Generated-marker ownership may use minimal fixture marker blocks when current README content would make a unit test too broad.

## Migration or compatibility tests

- T7 proves excluded historical and lifecycle-managed Markdown is not first-slice enforcement.
- T18 proves existing README, marker, guide-system, and skill validation remain active.
- T20 proves rendered README and VISION meaning, marker ownership, and historical non-migration are preserved.
- No data migration is required.

## Observability verification

- T15 verifies diagnostic fields.
- T18 verifies selected-validation output includes the prose validator at the right severity for covered changed paths.
- T23 verifies manual review evidence is recorded before PR handoff.

## Security/privacy verification

- T12 and T13 ensure Markdown content is parsed as text and code blocks, links, HTML, and embedded-looking content are not executed.
- No secret handling, authentication, authorization, or private-data flows are introduced.

## Performance checks

- T18 should keep selected validation path-scoped rather than repository-wide by default.
- Normal validator output should summarize pass/warn/fail counts and print details only for warnings, failures, or verbose mode.
- No benchmark is required for the first slice unless validator runtime becomes visibly slow on Tier A and Tier B paths.

## Manual QA checklist

- Render README and confirm content meaning is preserved after Tier A cleanup.
- Render or inspect VISION and confirm project meaning is preserved.
- Run `nl -ba README.md` and `nl -ba VISION.md` for changed covered sections.
- Confirm generated README marker ownership is respected.
- Confirm no historical Markdown files are mass-reflowed.
- Confirm audit warnings on changed covered files are dispositioned.

## What not to test and why

- Do not test grammar, tone, or writing quality; the spec only covers source-line boundaries.
- Do not test every Markdown file in the repository for first-slice enforcement; broad enforcement is out of scope.
- Do not test Markdown rendering semantics beyond behavior preservation checks; rendering behavior is not intended to change.
- Do not test automatic rewrite output; the validator must not rewrite prose.
- Do not require browser or UI automation; this change is repository validation and authoring guidance.

## Uncovered gaps

None.

## Next artifacts

```text
implement M1
code-review M1
implement M2
code-review M2
implement M3
code-review M3
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Active proof-planning surface.
Downstream execution is owned by the active plan handoff.
