# Explain Change: Spec-Family Readability Pass

## Summary

This change makes the three spec-family published skills easier to scan without
changing their behavior:

- `spec` now presents required sections as a table and centralizes changed
  status/settlement enum values.
- `spec-review` now presents review dimensions as a table and centralizes the
  review-dimension verdict enum.
- `test-spec` now presents required sections and coverage rules as tables and
  centralizes test-spec status and level enums.

The implementation also records preservation, behavior-parity, cold-read,
review, validation, and lifecycle evidence under
`docs/changes/2026-05-20-spec-family-readability-pass/`.

## Problem

After Test-Spec Contract Normalization, `spec`, `spec-review`, and `test-spec`
shared the same published-skill contract baseline, but still had presentation
gaps: prose enumerations, narrated closed enums, and uneven scan patterns. The
approved scope was a readability-only pass: improve installed skill text
scanability while preserving all rules, stop conditions, enum values, output
obligations, lifecycle boundaries, routing behavior, and produced-artifact
contracts.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Choose one coordinated readability pass across `spec`, `spec-review`, and normalized `test-spec`; defer packaging, build-time partials, and produced-artifact readability. |
| Proposal review | Add durable controls for normalized `test-spec` baseline, section-order safety, enum authority, content preservation, behavior parity, and produced-artifact scope. |
| Spec | Requirements `SFRP-R1` through `SFRP-R25` define scoped canonical skill edits, no behavior change, table/enum authority requirements, preservation matrices, behavior parity, adapter validation or deferral, and cold-read evidence. |
| Test spec | Tests `T1` through `T14` map baseline gating, per-skill table preservation, enum authority, section-order clarity, behavior parity, generated-output proof, cold-read proof, and non-goal guardrails. |
| Plan | Implement in three milestones: M1 `spec`, M2 `spec-review`, M3 `test-spec` plus generated-output proof. |
| Code review | M1 and M2 first-pass findings were resolved; M1 R2, M2 R2, and M3 R1 closed clean-with-notes. |

No architecture or ADR artifact was required because this is published skill
text and workflow evidence, not a runtime architecture change.

## Diff Rationale By Area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/spec/SKILL.md` | Tabulated required sections and added closed enum authority for spec status and settlement result. | Satisfies `SFRP-R7`, `SFRP-R10` through `SFRP-R14`; preserves output skeleton and status settlement behavior. | M1 plan; spec requirements | `T2`, `T3`, `T4`, `T5`; M1 preservation/parity evidence; code-review M1 R2 |
| `scripts/test-skill-validator.py` | Made downstream status-settlement expectations skill-specific. | Resolves `SFRP-M1-CR1`: `spec` may use enum authority, while unchanged `architecture` and `plan` still require the legacy inline value list. | code-review M1 R1; review-resolution | `python scripts/test-skill-validator.py`; M1 selected CI |
| `skills/spec-review/SKILL.md` | Tabulated the ten baseline review dimensions and added a closed enum authority for review-dimension verdict. | Satisfies `SFRP-R8`, `SFRP-R10` through `SFRP-R14`; the M2 fix removed non-baseline review-focus examples. | M2 plan; code-review M2 R1 | `T6`, `T7`, `T8`; M2 preservation/parity evidence; code-review M2 R2 |
| `skills/test-spec/SKILL.md` | Tabulated required sections and coverage rules; added closed enum authorities for test spec status, test case level, and coverage map level. | Satisfies `SFRP-R5` through `SFRP-R14`, `SFRP-R18`, and preserves the normalized output skeleton. | M3 plan; normalized baseline gate | `T1`, `T9`, `T10`, `T11`; M3 preservation/parity evidence; code-review M3 R1 |
| `docs/proposals/2026-05-20-spec-family-readability-pass.md` | Recorded the accepted scope, guardrails, dependency, and follow-on boundaries. | Captures the decision to make skill readability changes only after normalization. | proposal/proposal-review | proposal-review R2 |
| `specs/spec-family-readability-pass.md` | Defines the behavior-preserving readability contract. | Converts proposal decisions into requirements and acceptance criteria. | spec/spec-review | spec-review R1 |
| `specs/spec-family-readability-pass.test.md` | Defines deterministic tests and proof surfaces for each milestone. | Makes preservation, enum authority, parity, adapter deferral, and cold-read checks reviewable. | test-spec approval | owner-approved test spec |
| `docs/plans/2026-05-20-spec-family-readability-pass.md` and `docs/plan.md` | Track milestone sequencing, validation, review state, and current handoff. | Keeps workflow state current as M1, M2, and M3 move through implementation and code review. | active plan contract | artifact lifecycle validation |
| `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md` | Records source-to-destination preservation matrices, enum authority maps, section-order notes, adapter boundary, and cold-read notes. | Required by `SFRP-R13`, `SFRP-R14`, `SFRP-R17`, `SFRP-R19`, `SFRP-R20`, `SFRP-R24`, and `SFRP-R25`. | proposal-review findings; spec | code-review evidence |
| `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md` | Records representative behavior-parity classifications for each skill. | Required by `SFRP-R21` through `SFRP-R23`; supplements, not replaces, preservation matrices. | spec and test spec | code-review evidence |
| `docs/changes/2026-05-20-spec-family-readability-pass/reviews/*.md`, `review-log.md`, `review-resolution.md` | Records proposal/spec/plan/code review outcomes and finding dispositions. | Required formal lifecycle review evidence. | review skills; workflow contract | review artifact validation |
| `docs/changes/2026-05-20-spec-family-readability-pass/change.yaml` | Tracks artifacts, requirements, tests, validation, changed files, and latest review state. | Provides the change-local metadata and validation ledger. | docs-changes contract | change metadata validation |

## Tests Added Or Changed

No production runtime tests were needed because the change edits published skill
text and lifecycle artifacts. The validation fixture
`scripts/test-skill-validator.py` changed in M1 to keep settlement-result
coverage precise after `spec` moved to enum authority.

The active test spec supplied the proof plan:

- `T1`: confirms normalized `test-spec` baseline before readability edits.
- `T2` through `T5`: prove M1 required-section, enum, section-order, and parity behavior for `spec`.
- `T6` through `T8`: prove M2 review-dimension, verdict enum, recording-boundary, and parity behavior for `spec-review`.
- `T9` through `T11`: prove M3 required-section, coverage-rule, enum, stop-condition, section-order, and parity behavior for `test-spec`.
- `T12`: proves generated adapter output validation or explicit deferral, and no hand edits.
- `T13`: proves cold-read scanability across the three skills.
- `T14`: proves final scope and non-goal guardrails.

This test level is appropriate because the observable behavior is the published
skill contract and workflow evidence. Deterministic static checks and
source-to-destination matrices are stronger proof here than model-output
sampling alone.

## Validation Evidence Available Before Final Verify

Available validation evidence is recorded in `change.yaml` and the active plan.
Key commands include:

- `python scripts/validate-skills.py skills/spec/SKILL.md`
- `python scripts/validate-skills.py skills/spec-review/SKILL.md`
- `python scripts/validate-skills.py skills/test-spec/SKILL.md`
- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/build-skills.py --check`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-readability-pass/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-readability-pass`
- `git diff --check -- ...`
- `bash scripts/ci.sh --mode explicit ...`

Adapter validation caveat:

- `python scripts/build-adapters.py --version v0.1.5 --check` failed on
  existing repository-tree adapter layout debt.
- `python scripts/validate-adapters.py --version v0.1.5` failed on the same
  existing adapter layout debt.
- This is recorded as the approved `SFRP-R24` deferral path. Generated adapter
  skill bodies were not hand-edited, and selected CI passed the current
  archive-based adapter drift proof.

Final `verify` has not yet run.

## Review Resolution Summary

Review closeout is closed in
`docs/changes/2026-05-20-spec-family-readability-pass/review-resolution.md`.

- Reviews covered: 9.
- Material findings resolved: 7.
- Unresolved findings: 0.
- Implementation findings resolved:
  - `SFRP-M1-CR1`: fixed the validator fixture so `spec` can use enum authority without weakening legacy inline settlement-result coverage for `architecture` and `plan`.
  - `SFRP-M2-CR1`: narrowed the `spec-review` table to source-preserving dimension names and verdict placeholders, removing non-baseline focus examples.

M3 code review completed clean-with-notes with no material findings.

## Alternatives Rejected

| Alternative | Why rejected |
| --- | --- |
| Do nothing | Leaves prose enumerations and narrated enums in installed skill text. |
| Apply readability before `test-spec` normalization | Would mix presentation work with contract-compliance work. |
| Three independent proposals, one per skill | Higher lifecycle overhead and weaker family consistency. |
| Add packaging, assets, references, scripts, or build-time partials | Out of scope; packaging and duplicated-block resolution have different mechanisms and risks. |
| Improve produced spec/test-spec artifact readability here | Out of scope because it would change output expectations rather than only published skill readability. |
| Hand-edit generated adapter skill bodies | Violates the generated-output boundary; canonical `skills/` remains the authored source. |

## Scope Control

The final diff stays within the approved surfaces: canonical spec-family skill
sources, the validator fixture required by M1 review, proposal/spec/test-spec
and plan artifacts, change-local proof and review records, and metadata.

Preserved non-goals:

- no routing-description changes;
- no packaging resources;
- no build-time partials;
- no generated public adapter skill-body hand edits;
- no produced-artifact readability contract changes;
- no retroactive rewrite of legacy adapter archives.

## Risks And Follow-Ups

Remaining risks before PR:

- Final `verify` has not yet run.
- Repository-tree adapter validation for `v0.1.5` remains explicitly deferred
  because current tracked adapter support uses archive-based proof rather than
  generated repository-tree adapter packages.
- The predecessor Test-Spec Contract Normalization plan still appears as an
  active plan on this branch; this change records that as existing lifecycle
  state rather than closing unrelated work.

Deferred follow-ups remain:

- spec-family packaging using assets/references;
- build-time partials for duplicated blocks;
- produced spec and test-spec artifact readability;
- broader lifecycle skill section-ordering conventions.

## Readiness

All implementation milestones are closed. This explanation completes the
durable change-rationale step and hands off to `verify`. It does not claim final
verification, branch readiness, PR readiness, hosted CI status, or release
readiness.
