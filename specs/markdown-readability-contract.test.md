# Markdown Readability Contract Test Spec

## Status

active

## Related spec and plan

- Spec: `specs/markdown-readability-contract.md`
- Plan: `docs/plans/2026-07-04-markdown-readability-contract.md`
- Architecture/ADRs: not required; architecture assessment recorded in `docs/changes/2026-07-04-markdown-readability-contract/reviews/spec-review-r1.md`

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Proposal | `docs/proposals/2026-07-04-markdown-readability-contract.md` | accepted | `proposal-review-r2` |
| Proposal review | `docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r2.md` | approved | `proposal-review-r2` |
| Feature spec | `specs/markdown-readability-contract.md` | approved | `spec-review-r1` |
| Spec review | `docs/changes/2026-07-04-markdown-readability-contract/reviews/spec-review-r1.md` | approved; architecture-not-required | `spec-review-r1` |
| Plan | `docs/plans/2026-07-04-markdown-readability-contract.md` | active; plan-review approved | `plan-review-r1` |
| Plan review | `docs/changes/2026-07-04-markdown-readability-contract/reviews/plan-review-r1.md` | approved | `plan-review-r1` |
| Architecture | not applicable | architecture-not-required | `spec-review-r1` |

## Testing strategy

Use fixture-backed unit tests for the owner readability validator, integration checks for selected validator composition, lifecycle metadata validation, generated-output checks for affected skill and adapter surfaces, and review-visible cold-read evidence.

Unit coverage proves semantic-line regressions, no fixed-width failure, Markdown block exclusions, generated-region marker parsing, placeholder diagnostics, audit-only warning behavior, and closed check IDs.
Integration coverage proves README and `VISION.md` changed-section selection, composition from existing validators without moving policy ownership, and generated-output rebuild or check behavior from canonical authored sources.
End-to-end coverage is not required because the change is repository-local validation and generated artifact guidance, not a runtime user workflow.
Smoke coverage runs the new validator help and representative selected paths after implementation.
Manual QA is limited to source-form cold read and behavior-preservation review; this test spec intentionally does not require manual-proof contracts.
Contract coverage checks lifecycle artifact state, review recording, and active plan synchronization.
Migration coverage proves historical Markdown remains audit-only and no mass reflow occurs.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| R1-R7 | T1, T2, T3, T11 | unit, contract | Semantic source-line guidance, no mechanical hard-wrap default, no fixed line limit, and prose guidance. |
| R8-R10 | T4, T8, T11 | unit, integration | Table row, command, dense-content, and structure behavior. |
| R11-R17 | T8, T9, T11, T12 | integration, contract | Skeletons, status/result blocks, IDs, tables, and selected generated artifact guidance. |
| R18-R19 | T8, T10 | unit, integration | Proof-bearing command references and command-row ownership fields. |
| R20 | T10, T12 | contract | Manual-proof contracts remain excluded. |
| R21-R27 | T5, T6 | unit, integration | Canonical generated-region marker syntax, metadata, pairing, and source-owner rule. |
| R28-R31 | T7, T13 | unit, integration | Dedicated owner validator and composed-validator boundary. |
| R32-R35 | T3, T13, T14 | unit, migration | README and `VISION.md` changed-section enforcement, generated README vision-block source ownership, and no historical mass reflow. |
| R36-R39 | T2, T4, T11 | unit | Audit-only warnings, generic long-line behavior, graduation boundary, and block-type exclusions. |
| R40-R44 | T1, T2, T3, T4, T5, T9, T11 | unit, contract | Required fixtures, placeholder diagnostics, marker coverage, and cold-read proof. |
| R45-R48 | T12 | contract | Diagrams are encouraged when useful, never required, and must map to real nodes. |
| R49-R50 | T9, T14 | integration, smoke | Generated adapter output is regenerated or checked from canonical sources and not hand-edited. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| E1 | T1, T3 | Semantic source-line regression fixtures keep review-critical phrases intact. |
| E2 | T2 | Long semantic lines pass when line length is the only issue. |
| E3 | T3, T13 | Changed README and `VISION.md` hard-wrap fixtures fail only in changed-section scope. |
| E4 | T5, T6 | Generated-region marker fixtures prove canonical syntax and pairing. |
| E5 | T10, T12 | Manual verification prose does not trigger manual-proof contract requirements. |

## Edge case coverage

| Edge case | Covered by | Notes |
| --- | --- | --- |
| EC1 | T2 | Long semantic unit passes generic line-length handling. |
| EC2 | T4 | Code fences are excluded from prose-line checks. |
| EC3 | T4 | Tables are excluded from prose-line checks. |
| EC4 | T5 | Mismatched generated-region surfaces fail marker validation. |
| EC5 | T3 | Changed README hard-wrap fixtures fail for known phrase splits. |
| EC6 | T14 | Historical hard wrapping remains audit-only when untouched. |
| EC7 | T6, T13 | Generated README vision block is fixed through `VISION.md` or generator ownership. |
| EC8 | T12 | Decorative or unnecessary diagrams are not required. |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CMD1 | `python scripts/test-markdown-readability-validator.py` | planned-for-implementation | implement | M1 | M1 closeout | fail milestone validation | zero selected tests fail | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | local repository tests only |
| CMD2 | `python scripts/validate-markdown-readability.py --help` | planned-for-implementation | implement | M1 | M1 closeout | fail smoke validation | not applicable; help command | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | local read-only CLI smoke check |
| CMD3 | `python scripts/validate-markdown-readability.py` | planned-for-implementation | implement | M1, M2 | M1 closeout | fail readability validation | not applicable; validator command | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | local repository validation only |
| CMD4 | `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | existing/configured | test-spec / implement / verify | lifecycle | test-spec authoring | block downstream handoff on invalid metadata | not applicable; metadata validator | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | local metadata validation only |
| CMD5 | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/markdown-readability-contract.md --path specs/markdown-readability-contract.test.md --path docs/plans/2026-07-04-markdown-readability-contract.md --path docs/plan.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | existing/configured | test-spec / implement / verify | lifecycle | test-spec authoring | block downstream handoff on lifecycle inconsistency | not applicable; lifecycle validator | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | local lifecycle validation only |
| CMD6 | `python scripts/validate-skills.py` | existing/configured | implement | M2 | M2 closeout | fail skill guidance validation | not applicable; structural validator | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | local skill validation only |
| CMD7 | `python scripts/build-skills.py --check` | existing/configured | implement | M2 | M2 closeout | fail generated-output freshness validation | not applicable; build check | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | generated-output check only; no hand edits |
| CMD8 | `python scripts/test-build-skills.py` | existing/configured | implement | M2 | M2 closeout | fail generated-skill behavior validation | zero selected tests fail | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | local generated-skill test only |
| CMD9 | `python scripts/test-adapter-distribution.py` | existing/configured | implement | M2 | M2 closeout | fail adapter output validation | zero selected tests fail | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml` | local package/fixture proof; no publication |
| CMD10 | `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-markdown-readability-contract` | existing/configured | test-spec / verify | lifecycle | test-spec-review closeout | fail review evidence validation | not applicable; review-artifact validator | `docs/changes/2026-07-04-markdown-readability-contract/review-log.md` | local review-artifact validation only |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T1, T2, T3, T4, T5, T6, T7, T10, T11, T13, T14 | none | CMD1, CMD2, CMD3, CMD4, CMD5 | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml`; validator fixtures; changed-section fixtures | code-review M1 | Proves owner validator, deterministic fixtures, marker syntax, changed-section scope, audit-only boundaries, and no historical mass reflow. |
| M2 | T8, T9, T10, T11, T12, T14 | none | CMD3, CMD4, CMD5, CMD6, CMD7, CMD8, CMD9, CMD10 | `docs/changes/2026-07-04-markdown-readability-contract/change.yaml`; behavior-preservation proof when created | code-review M2 | Proves selected generated artifact guidance, generated-output freshness, cold-read evidence, diagram guidance, and no generated adapter hand edits. |

## Test cases

### T1. Known hard-wrap phrase fixtures fail

- Covers: R1-R7, R40, E1
- Level: unit
- Fixture/setup: positive and negative README or `VISION.md` fixture snippets containing `AI agents`, `proposal to spec`, and `reviewable in Git`.
- Steps: Run the readability validator fixture test against changed-section negative fixtures and semantic-line positive fixtures.
- Expected result: Known bad split phrases fail with stable `MDREAD-*` diagnostics, while fixtures with intact sentences pass.
- Failure proves: prior hard-wrap regressions can recur undetected.
- Automation location: `CMD1`

### T2. Long complete semantic lines do not fail generic line length

- Covers: R2-R4, R36-R38, R41, EC1, E2
- Level: unit
- Fixture/setup: positive fixture with a long complete sentence, command, table row, or link that preserves one semantic unit.
- Steps: Run readability fixture tests with generic long-line diagnostics enabled.
- Expected result: The fixture does not fail solely because a line is long; any long-line output is audit-only.
- Failure proves: the validator reintroduced a fixed-width line-length rule.
- Automation location: `CMD1`

### T3. README and VISION changed-section enforcement is bounded

- Covers: R32-R35, R40, EC5, EC6, E3
- Level: integration
- Fixture/setup: changed-section fixtures for README and `VISION.md`, plus untouched historical fixture sections with similar old wrapping.
- Steps: Run changed-section selection tests for README and `VISION.md`.
- Expected result: Changed sections with known hard-wrap regressions fail, while untouched historical sections remain audit-only or out of enforcement scope.
- Failure proves: first-slice enforcement either misses known recurrence surfaces or overreaches into historical Markdown.
- Automation location: `CMD1`, `CMD3`

### T4. Markdown block exclusions protect code, tables, HTML, links, and generated regions

- Covers: R8-R10, R36-R39, EC2, EC3
- Level: unit
- Fixture/setup: fixture containing code fences, tables, HTML blocks, link reference definitions, and generated regions with long or wrapped content.
- Steps: Run prose-line checks against the fixture.
- Expected result: Prose-line checks skip excluded block types unless a check explicitly targets that structure.
- Failure proves: readability validation will create false positives on non-prose Markdown.
- Automation location: `CMD1`

### T5. Canonical generated-region marker pairing passes and mismatches fail

- Covers: R21-R23, R42, EC4, E4
- Level: unit
- Fixture/setup: positive fixture using canonical paired markers and negative fixtures with mismatched or missing `surface` values.
- Steps: Run generated-region marker validation fixtures.
- Expected result: Matching canonical pairs pass; mismatched, missing, or duplicate invalid surfaces fail with stable check IDs.
- Failure proves: generated-region ownership cannot be audited reliably.
- Automation location: `CMD1`

### T6. Generated-region source-owner metadata is enforced where in scope

- Covers: R24-R27, EC7, E4
- Level: integration
- Fixture/setup: generated-region fixtures with repository-relative `source`, optional `generator`, and projection content.
- Steps: Validate marker metadata and any projection consistency checks implemented for selected generated regions.
- Expected result: Missing required `source` metadata fails in generated-region scope, `generator` is accepted when present, and projection fixes route through source owner or generator.
- Failure proves: generated content can become an unauditable manual-maintenance surface.
- Automation location: `CMD1`, `CMD3`

### T7. Dedicated owner validator exposes stable check IDs and composition boundary

- Covers: R28-R31
- Level: unit
- Fixture/setup: `scripts/validate-markdown-readability.py` and representative diagnostics.
- Steps: Run unit tests and help output for the owner validator.
- Expected result: The owner validator exposes stable `MDREAD-*` check IDs, artifact-class selectable checks, and reusable CLI behavior without making guide or skill validators policy owners.
- Failure proves: readability policy can drift across validators.
- Automation location: `CMD1`, `CMD2`

### T8. Proof-bearing commands are fenced or command-table owned

- Covers: R9, R17-R19
- Level: unit
- Fixture/setup: generated document fixtures with fenced commands, command tables, raw command prose, and required command-row fields.
- Steps: Run validator tests for proof-bearing command references.
- Expected result: Fenced commands and complete command rows pass; unsupported raw proof-bearing command prose fails or warns according to deterministic scope.
- Failure proves: generated docs can make validation claims without copyable or owned commands.
- Automation location: `CMD1`, `CMD3`

### T9. Stable skeleton and placeholder checks cover selected generated artifacts

- Covers: R11-R17, R43, R44, R49-R50
- Level: integration
- Fixture/setup: selected high-value skeleton or skill assets, generated output checks, and representative generated-doc fixture.
- Steps: Validate required status/result blocks, stable IDs, mapping tables, placeholder removal, generated-output freshness, and cold-read evidence for selected artifact classes.
- Expected result: Stable skeleton fields are present where required, placeholders fail, generated adapter output is checked from canonical sources, and reviewers can find status, blockers, commands, evidence, and next stage.
- Failure proves: generated artifacts remain unpredictable or generated output was hand-edited.
- Automation location: `CMD3`, `CMD6`, `CMD7`, `CMD8`, `CMD9`

### T10. Manual-proof contracts remain out of scope

- Covers: R20, E5
- Level: contract
- Fixture/setup: fixture or representative artifact containing manual verification prose without a manual-proof contract block.
- Steps: Run applicable readability validation and inspect generated artifact guidance updates.
- Expected result: Manual verification prose is not rejected merely because it lacks a manual-proof contract, and no skill or skeleton update introduces manual-proof contract enforcement for this change.
- Failure proves: implementation exceeded the approved scope.
- Automation location: `CMD1`, `CMD3`, `CMD6`

### T11. Audit-only warning graduation stays deterministic and fixture-backed

- Covers: R10, R36-R39, R44
- Level: unit
- Fixture/setup: audit-only fixtures for long lines, dense paragraphs, lifecycle chains, and ambiguous sentence splits.
- Steps: Run validator tests for warning and failure modes.
- Expected result: Generic long lines, subjective prose quality, and generic dense-paragraph concerns remain audit-only; only narrow fixture-backed deterministic cases can fail.
- Failure proves: the validator became a subjective prose judge.
- Automation location: `CMD1`

### T12. Diagram guidance is encouraged but never required

- Covers: R45-R48, EC8
- Level: contract
- Fixture/setup: selected generated artifact guidance or representative documents with workflow, state-machine, table, and list alternatives.
- Steps: Inspect or validate that diagrams are described as useful when they reduce cognitive load and map to real nodes, but are not mandatory when a table, list, or prose structure is clearer.
- Expected result: No artifact class fails solely for omitting a diagram, and decorative diagrams are not encouraged.
- Failure proves: implementation added an unsupported diagram requirement.
- Automation location: `CMD6`

### T13. Existing validators compose readability validation without owning policy

- Covers: R28-R34, E3, EC7
- Level: integration
- Fixture/setup: selected existing validator integration points and path selectors chosen during M1.
- Steps: Run integration tests for validators that call the owner readability validator for relevant README, `VISION.md`, or generated-region paths.
- Expected result: Existing validators delegate to `scripts/validate-markdown-readability.py` and preserve path selection, changed-section scope, and source-owner boundaries.
- Failure proves: readability rules are duplicated or owned by downstream validators.
- Automation location: `CMD1`, `CMD3`

### T14. Historical and generated adapter surfaces avoid migration churn

- Covers: R35, R49-R50, EC6
- Level: smoke
- Fixture/setup: repository diff, generated adapter validation commands, and historical Markdown paths touched or referenced by the implementation.
- Steps: Inspect the diff and run generated-output checks after M2.
- Expected result: Historical Markdown is not mass-reflowed, generated public adapter bodies are not hand-edited, and adapter support output is current or intentionally unaffected.
- Failure proves: the change created noisy migration churn or modified generated release surfaces by hand.
- Automation location: `CMD7`, `CMD8`, `CMD9`, `git diff --check --`

## Fixtures and data

- README changed-section hard-wrap fixtures.
- `VISION.md` changed-section hard-wrap fixtures.
- Long semantic-line passing fixture.
- Markdown block exclusion fixtures for code fences, tables, HTML blocks, link reference definitions, and generated regions.
- Generated-region marker positive and negative fixtures.
- Placeholder-positive and placeholder-negative generated document fixtures for selected artifact classes.
- Representative generated-doc cold-read fixture or evidence file selected during M2.

## Mocking/stubbing policy

Use local fixture files and temporary in-repository test data.
Do not use network calls, hosted CI state, or generated public adapter package hand edits as test inputs.
Composition tests may stub changed-section selectors only when a separate integration test exercises the real repository path selection.

## Migration or compatibility tests

- T3 proves changed-section enforcement does not fail untouched historical README or `VISION.md` content.
- T14 proves historical Markdown is not mass-reflowed.
- T9 and T14 prove generated adapter output is regenerated or checked from canonical authored sources rather than hand-edited.

## Observability verification

- Validator diagnostics use stable `MDREAD-*` check IDs.
- Change metadata records validation commands and lifecycle state.
- Review records and review log record formal review outcomes.
- Cold-read evidence records whether reviewers can find status, blockers, commands, evidence, and next stage in representative generated docs.

## Security/privacy verification

- Generated-region `source` and `generator` marker metadata use repository-relative paths or approved canonical identifiers.
- Fixtures and diagnostics do not require secrets, credentials, private machine paths, or network state.

## Performance checks

- Validator tests should include enough fixture coverage to exercise block parsing and changed-section selection without scanning unrelated historical files.
- Full repository readability validation should be bounded to selected paths or audit-only modes until broader enforcement is approved.

## Manual QA checklist

- Cold-read representative generated documents for status, blockers, commands, evidence, and next stage.
- Inspect the implementation diff for historical Markdown mass reflow.
- Inspect affected generated artifact guidance to confirm manual-proof contracts and required diagrams were not introduced.
- Inspect generated adapter proof to confirm output was rebuilt or checked from canonical sources.

## What not to test and why

- Do not test runtime end-user UI behavior; this change has no user interface.
- Do not test external hosted CI status; repository-owned local validators are the proof surface.
- Do not test manual-proof contract enforcement; R20 excludes it from this change.
- Do not test universal line-length failure; R3 and R4 prohibit that behavior.
- Do not test mandatory diagram presence; R46 prohibits required diagrams when other structures are clearer.

## Uncovered gaps

None.

## Next artifacts

```text
implementation M1
code-review M1
implementation M2
code-review M2
explain-change
verify
pr
```

## Follow-on artifacts

- Test-spec review R1: `../docs/changes/2026-07-04-markdown-readability-contract/reviews/test-spec-review-r1.md`

## Readiness

Approved after clean `test-spec-review-r1`.
Active proof surface for implementation.
The active plan `Current Handoff Summary` owns the next workflow action.
