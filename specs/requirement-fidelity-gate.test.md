# Requirement-Fidelity Gate Test Spec

## Status

- active

## Related spec and plan

- Spec: [Requirement-Fidelity Gate for Spec-Canonical Reviews](requirement-fidelity-gate.md), approved.
- Plan: [Requirement-Fidelity Gate for Spec-Canonical Reviews Execution Plan](../docs/plans/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md), approved by `plan-review-r1`.
- Proposal: [Requirement-Fidelity Gate for Spec-Canonical Reviews](../docs/proposals/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews.md), accepted.
- Architecture: [System Architecture](../docs/architecture/system/architecture.md), approved.
- ADR: [ADR-20260626 Requirement-Fidelity Gate](../docs/adr/ADR-20260626-requirement-fidelity-gate.md), accepted.
- Spec-review: [spec-review-r2](../docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/spec-review-r2.md), approved.
- Architecture-review: [architecture-review-r1](../docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/architecture-review-r1.md), approved.
- Plan-review: [plan-review-r1](../docs/changes/2026-06-26-requirement-fidelity-gate-for-spec-canonical-reviews/reviews/plan-review-r1.md), approved.

## Testing strategy

- Use unit and fixture-backed integration tests in `scripts/test-review-artifact-validator.py` and `scripts/review_artifact_validation.py` for applicability manifests, packet ordering evidence, decomposition tables, property matrices, fidelity receipts, material finding classification, calibration records, corpus iterations, rotation logs, and closed-vocabulary fail-closed behavior.
- Use lifecycle/state-sync integration tests in `scripts/test-artifact-lifecycle-validator.py`, `scripts/artifact_lifecycle_validation.py`, and `scripts/lifecycle_state_sync.py` for automated handoff blocking, AND semantics with independent-review gates, historical-review compatibility, manual/profile-off behavior, plan state synchronization, and final closeout boundaries.
- Use change-metadata integration tests in `scripts/test-change-metadata-validator.py`, `scripts/change_metadata_semantics.py`, and `scripts/validate-change-metadata.py` only where the implementation records fidelity gate evidence or validation ledger entries in compact change metadata.
- Use skill-validator and generated-output tests in `scripts/test-skill-validator.py`, `scripts/validate-skills.py`, `scripts/test-build-skills.py`, and `scripts/build-skills.py --check` for canonical review guidance, code-review pilot wording, manual opt-in wording, no finding quota, exact-wording guidance, and the R26 property-list by surface-list pilot.
- Use public adapter archive proof when canonical `skills/` files change: `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`.
- Use selected validation routing tests in `scripts/test-select-validation.py`, `scripts/select-validation.py`, and `scripts/ci.sh` for new review-artifact fixture paths, calibration fixture paths, lifecycle fixture paths, and skill changes.
- Use smoke validation for the authored artifact set: review artifact validation, change metadata validation, artifact lifecycle validation over explicit paths, and `git diff --check`.
- Use structured manual proof cases only for policies that cannot be fully asserted structurally, such as private rotating corpus custody, whether sample receipt prose is substantively strong rather than boilerplate, and scan-first public skill usability.
- Migration strategy: prove historical clean reviews are not retroactively invalidated, prove profile-off and direct manual reviews remain compatible, and do not migrate historical review records in this slice.
- End-to-end strategy: use fixture-backed lifecycle scenarios that simulate applicable automated code-review handoff from changed paths through clean-review receipt evaluation and autoprogression blocking or advance.

## Manual proof case schema

Every manual proof case MUST contain:

| Field | Required |
| --- | --- |
| Stable ID | yes; pattern `MP-RFG-NNN` |
| Automation rationale | yes; explain why automation cannot or should not perform this check |
| Owning stage | yes; one of: `code-review`, `verify`, `calibration`, `scheduled-audit` |
| Required environment | yes; tools, fixtures, reviewer profile, access rights |
| Exact steps | yes; ordered, numbered, named commands or actions |
| Evidence artifact | yes; path or path pattern for the recorded result |
| Pass condition | yes; bounded, specific |
| Failure condition | yes; bounded, specific |
| Owner role | yes; named role from the spec roles table or explicitly named skill owner for public skill usability checks |
| Cadence | yes; trigger or recurring schedule |

`RFG-022` requires the test-spec validator to fail closed when any section labeled `Manual proof` omits a required field.

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`-`R1b` | `T1`, `T9`, `T11` | integration, contract | Formal automated applicability is enforced; manual review remains voluntary and out of mandatory first-slice scope. |
| `R2`-`R3` | `T5`, `T9`, `T14` | integration | Independent-review gates remain additive and both receipts are required when both contracts apply. |
| `R4`-`R8` | `T1`, `T10` | integration | Applicability manifest is computed before comparison, uses closed enums, and records justified overrides. |
| `R9`-`R11` | `T1`, `T10` | unit, integration | Path triggers, category triggers, and not-applicable reasons are closed lists and fail closed on unknown values. |
| `R12`-`R13` | `T2` | integration | Applicable review packet evidence starts from the relevant spec clause. |
| `R14`-`R16` | `T3` | integration | Accepted decomposition is preferred; reviewer-authored decomposition is recorded with source and authoring marker. |
| `R17`-`R17d` | `T8`, `T10`, `MP-RFG-002` | integration, manual | Calibration sample floors, reviewer-authored sampling, sampling fields, sampling reasons, and receipt-quality audit are enforced. |
| `R18`-`R19` | `T3` | integration | Vague clauses route to spec-quality findings, and applicable reviews include decomposition evidence. |
| `R20`-`R23` | `T4`, `T11` | integration, contract | Multi-surface contracts require property-by-surface matrices and accepted surface vocabularies are honored. |
| `R24`-`R26` | `T7`, `T10` | unit, integration | Selected changed contracts use shared property-list by surface-list assertions, source annotations, and missing-property negative proof. |
| `R27`-`R29` | `T7`, `T11` | unit, contract | Semantic property IDs are preferred and exact wording is required only for public contract wording. |
| `R30`-`R34` | `T5` | integration | Applicable clean automated reviews require structurally valid fidelity receipts and block on missing or invalid evidence. |
| `R35`-`R40` | `T6`, `T11` | integration, contract | Requirement compression is material in specified areas, severity and mechanical classification are bounded. |
| `R41`-`R43` | `T8`, `T7` | integration | Requirement-compression seeded family exists and includes the canonical R26 missing-`recorded` regression. |
| `R44`-`R44g` | `T8`, `T10`, `MP-RFG-001` | integration, manual | Corpus iterations, rotation triggers, logs, `iteration_id` evidence, and private custody are enforced with closed trigger values. |
| `R45`-`R45c` | `T8`, `T10`, `MP-RFG-002` | integration, manual | Not-applicable sampling rate, proportionality, sampled receipt fields, audit outcomes, and prose-quality review are enforced. |
| `R46` | `T9`, `T14` | integration | Existing independent-review fixtures and behavior still pass. |
| `R47` | `T9`, `T14` | migration | Historical reviews, all validators, and all existing specs are not rewritten in this slice. |
| `R48` | `T10` | unit, integration | Applicability trigger and seeded-defect lists are protected by closed-list tests or equivalent coverage. |
| `R49` | `T12` | smoke, integration | Generated public adapter outputs are refreshed through normal generation when canonical skill behavior changes. |
| `R50` | `T9` | migration, integration | Historical clean reviews are not retroactively invalidated only for missing fidelity receipts. |
| Inputs and outputs | `T1`-`T8`, `T13` | integration | Required manifests, matrices, receipts, findings, calibration outputs, and review-log updates are covered. |
| State and invariants | `T2`-`T5`, `T9`, `T14`, `T-RFG-GATE-001` | integration | Spec is canonical, implementation/validator agreement is insufficient, receipts do not replace lifecycle state, and implementation activity is gated by approved test-spec-review. |
| Error and boundary behavior | `T1`-`T8`, `T10` | integration | Missing manifests, missing decomposition, unknown values, vague specs, matrix failures, override failures, and unknown calibration fields fail closed. |
| Compatibility and migration | `T9`, `T12`, `T14` | migration, smoke | Independent gates, direct/manual reviews, generated outputs, and historical records remain compatible. |
| Observability | `T1`-`T8`, `T13` | integration | Applicability, decomposition, matrix, validator comparison, compressed-risk, finding IDs, and calibration evidence are visible. |
| Security and privacy | `T6`, `T13`, `MP-RFG-001` | integration, manual | Security/privacy compression is material, records avoid secrets and private chain-of-thought, and private corpus custody is audited. |
| Accessibility and UX | `T11`, `MP-RFG-003` | manual, contract | Contributor-facing output remains scan-first and inspectable without hidden reasoning. |
| Performance expectations | `T1`, `T13`, `T-RFG-PERF-001` | smoke, integration | Applicability starts from affected paths and bounded excerpts; no broad full-spec read is required for unrelated changes. |
| `RFG-T017`-`RFG-T021` | `T8` | integration | Sampling and rotation planned checks are represented directly. |
| `RFG-T022` | `T10` | unit | Undefined soft-normative wording in `MUST` requirements is rejected unless defined, quantified, or non-normative. |
| `RFG-022` | `T10` | unit | Manual proof sections that omit required schema fields fail the test-spec validator. |
| `RFG-023` | `T10` | unit | Every requirement in the coverage map references at least one automated or structured manual proof. |
| `RFG-024` | `T-RFG-PERF-001` | integration | Bounded spec-read instrumentation is exercised at least once per implementation milestone touching the gate's reviewer surface. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T3`, `T7`, `T8` | R26 `approved + current + recorded` compression is caught and seeded as the canonical regression. |
| `E2` | `T1` | `skills/` plus validator paths trigger deterministic applicability. |
| `E3` | `T4` | Property-by-surface matrix catches one weakened surface. |
| `E4` | `T3`, `T6` | Vague spec routes to a spec-quality finding rather than implementation approval. |
| `E5` | `T1`, `T5` | `not-applicable` uses a closed reason and free-form opt-out fails. |
| `E6` | `T5`, `T9` | Independent review and fidelity both apply, and both passing receipts are required. |
| `E7` | `T9`, `T11` | Manual review can voluntarily record a receipt without mandatory first-slice manual applicability classification. |

## Edge case coverage

- `EC1`: Reviewer-authored decomposition before artifact comparison when no accepted decomposition exists: `T3`.
- `EC2`: Triggered path with reviewer override to `force-not-applicable` only with justification and closed reason: `T1`, `T5`.
- `EC3`: Category trigger applies even when path trigger does not match: `T1`.
- `EC4`: Global phrase match fails when one required section omits a property: `T4`.
- `EC5`: Closed enum with missing validator value is compression: `T6`, `T7`.
- `EC6`: Vague "behave appropriately" spec clause routes to spec-quality finding: `T3`, `T6`.
- `EC7`: Clean review without required fidelity receipt stops autoprogression: `T5`.
- `EC8`: Fixed public corpus reaching memorized recall is insufficient without rotation: `T8`.
- `EC9`: Historical clean review lacking fidelity receipt remains historical evidence: `T9`.

## Milestone coverage map

| Milestone | Covered by | Notes |
| --- | --- | --- |
| `M1` Requirement-fidelity review contract and guidance | `T1`-`T6`, `T9`, `T11`, `T14`, `MP-RFG-003` | Skill and workflow guidance, AND semantics, receipt shape, compression findings, no finding quota, manual opt-in, scan-first public skill proof. |
| `M2` Applicability, receipt, and autoprogression validators | `T1`-`T6`, `T9`, `T10`, `T13`, `T14`, `T-RFG-GATE-001` | Review artifact, lifecycle, change metadata, closed vocabulary, gating, and historical compatibility fixtures. |
| `M3` Spec-derived validator matrix pilot | `T7`, `T10`, `T12`, `T14`, `T-RFG-PERF-001` | R26 property/surface constants, missing-property negative proof, skill guidance, generated-output proof, bounded spec-read instrumentation. |
| `M4` Compression calibration corpus and sampling records | `T8`, `T10`, `T13`, `T14`, `MP-RFG-001`, `MP-RFG-002` | Seed types, rotating iterations, sampling floors, audit outcomes, selector routing, soft-normative meta-test, custody and receipt-quality audit. |
| `M5` Generated guidance, behavior preservation, and lifecycle closeout | `T9`, `T12`, `T13`, `T14` | Generated skills/adapters, behavior-preservation matrix, selected CI, lifecycle state synchronization. |

## Test cases

### T1. Deterministic applicability manifest uses affected paths, categories, and closed override fields

- Covers: `R1`, `R1a`, `R1b`, `R4`-`R11`, `E2`, `E5`, `EC2`, `EC3`
- Level: integration
- Fixture/setup: Review artifact or lifecycle fixtures with changed-path sets, matched category triggers, applicability results, override directions, override justifications, and not-applicable reasons.
- Steps:
  - Create valid fixtures where affected paths under `skills/`, `scripts/*validator*`, `scripts/validate-*`, `schemas/`, `specs/`, `templates/`, `docs/workflows.md`, `docs/changes/**/reviews/`, and `docs/changes/**/review-*.md` trigger `applicable`.
  - Create valid fixtures where a category trigger such as `closed enums` or `material-finding schemas` triggers `applicable` even without a path-trigger match.
  - Create a valid `force-not-applicable` override only when override direction, non-empty justification, and a closed not-applicable reason are present.
  - Add negative fixtures for unknown applicability result, unknown override direction, empty override justification, free-form not-applicable reason, missing affected paths, missing matched triggers, and reviewer replacement of computed applicability without evidence.
- Expected result: Applicable changes produce structured applicability manifests before reviewer comparison, and malformed or hand-waved applicability evidence fails closed.
- Failure proves: The gate can be silently bypassed at the applicability layer.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-change-metadata-validator.py` when metadata records gate state.

### T2. Applicable review packet evidence is spec-canonical and records spec-first ordering

- Covers: `R12`, `R13`, state invariants
- Level: integration
- Fixture/setup: Review artifact fixtures with ordered evidence enumeration entries for spec clause, decomposition, expected surfaces, implementation diff, validator assertions, validation evidence, and prior findings.
- Steps:
  - Validate a packet-order fixture whose first evidence entry is the relevant spec clause.
  - Add negative fixtures where implementation diff, validator assertions, validation evidence, or prior findings appear before the spec clause for an applicable requirement-fidelity review.
  - Add a fixture where packet ordering is absent for a non-applicable review and prove it does not block solely because the gate is not applicable.
- Expected result: Applicable review evidence starts from the normative spec clause and rejects implementation-first or validator-first ordering when ordering is recorded.
- Failure proves: Review can still compare implementation to validator assertions without first establishing the canonical spec reference.
- Automation location: `python scripts/test-review-artifact-validator.py`.

### T3. Decomposition evidence prefers accepted decompositions and routes vague specs upstream

- Covers: `R14`-`R19`, `R32`, `E1`, `E4`, `EC1`, `EC6`
- Level: integration
- Fixture/setup: Review record fixtures with accepted decomposition references, reviewer-authored decompositions, missing decomposition evidence, and spec-quality finding records.
- Steps:
  - Validate an applicable review that links to an accepted decomposition and uses it as the comparison baseline.
  - Validate an applicable review with reviewer-authored decomposition evidence that names the source spec clause and marks the decomposition as reviewer-authored.
  - Add a negative fixture where the review compares implementation and validator text before any decomposition evidence exists.
  - Add a vague-spec fixture where the cited clause cannot be decomposed and the review records a spec-quality finding against the spec.
  - Add a negative fixture where a vague-spec clause passes cleanly without decomposition or spec-quality finding.
- Expected result: Reviews cannot pass applicable surfaces without accepted or reviewer-authored decomposition evidence, and vague requirements route upstream.
- Failure proves: The gate can pass vacuously because the decomposition itself was omitted or compressed.
- Automation location: `python scripts/test-review-artifact-validator.py`.

### T4. Multi-surface contracts require property-by-surface matrix verification

- Covers: `R20`-`R23`, `E3`, `EC4`
- Level: integration
- Fixture/setup: Review record fixtures with requirement properties, required surfaces, evidence paths, verification results, accepted surface vocabulary, and validator coverage fields.
- Steps:
  - Validate a complete property-by-surface matrix for a multi-surface contract.
  - Add a negative fixture where one property is missing from one required surface.
  - Add a negative fixture where a global substring match appears elsewhere but one required surface omits the property.
  - Add a fixture using accepted surface vocabulary and assert conflicting surface identifiers for the same surface are rejected.
  - Add a fixture where no accepted surface vocabulary exists and the reviewer records bounded surface identifiers without conflict.
- Expected result: Every property on every required surface is checked independently, and global substring checks are insufficient.
- Failure proves: A complete-looking review can still miss a weakened public or machine-enforced surface.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/test-skill-validator.py` for public skill surface examples.

### T5. Applicable clean automated review requires a valid fidelity receipt before autoprogression

- Covers: `R3`, `R30`-`R34`, `E5`, `E6`, `EC7`
- Level: integration
- Fixture/setup: Lifecycle fixtures with independent-review gate evidence, requirement-fidelity applicability manifests, clean review records, fidelity receipts, and autoprogression handoff decisions.
- Steps:
  - Validate that a clean automated review with `applicable` manifest, decomposition evidence, complete matrix, validator/spec comparison, compressed-risk result, and no-finding rationale can satisfy the fidelity gate.
  - Add negative fixtures for missing receipt, missing decomposition table or accepted decomposition link, incomplete receipt fields, free-form `not-applicable`, validator assertions accepted without spec comparison, and `yes` decomposition value without decomposition evidence.
  - Add a fixture where the independent-review receipt passes but the fidelity receipt is missing, and assert workflow-managed continuation is blocked.
  - Add a fixture where fidelity passes but independent-review gates fail, and assert continuation is blocked.
- Expected result: Clean automated review advances only when all applicable fidelity receipt evidence and independent-review evidence are valid.
- Failure proves: Workflow-managed automation can treat tests-passed or validator agreement as sufficient spec fidelity.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`.

### T6. Requirement-compression findings have bounded materiality, severity, and mechanical classification

- Covers: `R18`, `R35`-`R40`, `EC5`, `EC6`, security/privacy requirements
- Level: integration
- Fixture/setup: Detailed review records with requirement-compression findings, spec-quality findings, severity, evidence, required outcome, and safe resolution or mechanical classification fields.
- Steps:
  - Validate material compression findings for required evidence, lifecycle gating, workflow routing, validation correctness, published skill behavior, test coverage, package/install integrity, and security/privacy/release gates.
  - Assert severity defaults to `major` when no blocking gate is affected.
  - Assert severity is `blocking` when the omitted property protects implementation start, verification, review recording, security, compatibility, or release gates.
  - Validate `mechanical` only when the spec uniquely determines the missing phrase and the fix is inserting that exact phrase into identified surfaces with no coordinated validator or test changes.
  - Add negative fixtures where rephrasing, choice between alternatives, or coordinated validator/test changes are mislabeled mechanical.
- Expected result: Compression findings are classified consistently and cannot be under-scoped as minor wording issues.
- Failure proves: Review-resolution can auto-fix or downgrade compression defects that require owner review.
- Automation location: `python scripts/test-review-artifact-validator.py`; manual contract review for severity rationale quality.

### T7. R26 validator matrix pilot uses one property list multiplied by one surface list

- Covers: `R24`-`R29`, `R41`-`R43`, `AC-RFG-009`-`AC-RFG-012`, `E1`, `EC5`
- Level: unit, integration
- Fixture/setup: `scripts/test-skill-validator.py` constants and fixtures for `specs/test-spec-review-gate.md` R26 and `skills/implement/SKILL.md` surfaces.
- Steps:
  - Add source-annotated constants for R26 evidence properties `approved`, `current`, and `recorded`.
  - Add source-annotated constants for required `implement` skill surfaces selected by the implementation.
  - Assert each property is present on each required surface or represented by an equivalent surface-specific semantic assertion.
  - Add a missing-property negative fixture or equivalent proof where removing `recorded` from one required surface fails validation.
  - Add a regression fixture where implementation and validator both check only `approved + current`, and assert validation fails because `recorded` is omitted.
  - Assert exact wording is required only when the value is public contract wording under `R28`; otherwise semantic property IDs may satisfy the check.
- Expected result: The canonical R26 compression case is protected by a property-list by surface-list assertion matrix.
- Failure proves: The first validator pilot still hand-copies a compressed subset of the spec.
- Automation location: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### T8. Compression calibration enforces seed types, sampling floors, and rotating corpus iterations

- Covers: `R17`-`R17d`, `R41`-`R45c`, `AC-RFG-014`, `AC-RFG-015`, `AC-RFG-020`, `RFG-T017`-`RFG-T021`, `E1`, `EC8`
- Level: integration
- Fixture/setup: Calibration fixtures under `tests/fixtures/review-artifacts/`, `tests/fixtures/artifact-lifecycle/`, or the smallest implementation-owned calibration fixture location chosen during M4.
- Steps:
  - Validate a named corpus iteration with at least six defects spanning at least four of the six seed types in `R42`.
  - Assert the corpus includes the canonical R26 missing-`recorded` regression seed.
  - Add negative corpus fixtures with fewer than six defects, fewer than four seed types, unknown seed type, missing `iteration_id`, or missing expected finding.
  - Validate Phase B sampling records at or above 10 percent baseline applicable receipts and 30 percent reviewer-authored decomposition receipts.
  - Validate not-applicable sampling at or above 5 percent per calibration cycle, with proportionality unless fewer than five not-applicable receipts exist.
  - Add rotation trigger fixtures for complete defect-set exposure, recall above 95 percent across two consecutive cycles, and scheduled two-cycle rotation.
  - Add negative fixtures for unknown `sampling_reason`, `rotation_trigger`, or `audit_outcome`, and for steady-state rates below 5 percent baseline or 15 percent reviewer-authored without follow-on amendment.
- Expected result: Calibration evidence detects requirement-compression recall using measured, rotating corpus iterations and quantified sampling floors.
- Failure proves: Calibration can devolve into fixed-fixture memorization or unmeasured sampling assertions.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-change-metadata-validator.py` if sampling records are stored in change metadata.

### T9. Compatibility preserves independent gates, direct/manual review behavior, and historical reviews

- Covers: `R1a`, `R1b`, `R2`, `R3`, `R46`, `R47`, `R50`, `AC-RFG-016`-`AC-RFG-019`, `E6`, `E7`, `EC9`
- Level: integration, migration
- Fixture/setup: Existing independent-review gate fixtures, historical clean review fixtures without fidelity receipts, direct isolated review fixtures, and manual voluntary fidelity receipt fixtures.
- Steps:
  - Rerun existing independent-review fixture tests and assert their original pass/fail behavior is preserved.
  - Validate a historical clean review without fidelity receipt as historical evidence when it is not the current applicable review surface.
  - Validate direct isolated review behavior remains isolated by default and does not require mandatory manual applicability classification.
  - Validate a manual review can voluntarily record a fidelity receipt without turning first-slice manual applicability into an orchestrator gate.
  - Add negative lifecycle fixture proving both gates are required only when both contracts apply under workflow-managed automated continuation.
- Expected result: The new gate is additive and forward-looking, with no historical migration or manual-review expansion.
- Failure proves: Requirement fidelity either replaces independence gates or widens first-slice scope beyond the approved contract.
- Automation location: `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-review-artifact-validator.py`; `python scripts/test-skill-validator.py`.

### T10. Closed vocabularies and soft-normative spec language fail closed

- Covers: `R6`-`R11`, `R17d`, `R44g`, `R45c`, `R48`, `RFG-T022`
- Level: unit, integration
- Fixture/setup: Unit tests and fixtures for every new closed set introduced by the implementation, plus a spec-text meta-test for undefined soft-normative terms in `MUST` requirements.
- Steps:
  - Add constants for applicability results, override directions, not-applicable reasons, path triggers, category triggers, sampling reasons, rotation triggers, audit outcomes, and seeded defect types.
  - Add unknown-value regression tests, preferably with `unknown_value` or `not_in_vocabulary` in the test name.
  - Assert unknown values produce explicit validation errors before consistency checks.
  - Add a meta-test scanning `specs/requirement-fidelity-gate.md` for soft-normative terms such as `high-risk`, `periodically`, `higher`, `appropriate`, `sufficient`, or `reasonable` in `MUST` requirements unless quantified, defined, or explicitly non-normative.
  - Add test-spec validation for the manual proof case schema: every `Manual proof` section must include all required fields, and every requirement coverage-map row must cite at least one proof.
- Expected result: Closed-list drift and soft-normative backsliding are caught structurally.
- Failure proves: The implementation can silently accept unknown terms, reintroduce untestable safety claims, or let manual proof obligations degrade into unauditable prose.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/test-artifact-lifecycle-validator.py`; `python scripts/test-change-metadata-validator.py`; `python scripts/validate-test-spec.py specs/requirement-fidelity-gate.test.md` planned for M1; spec meta-test location selected during M4.

### T11. Canonical skill and workflow guidance teaches the gate without finding quotas or maintainer-only leakage

- Covers: `R1a`, `R1b`, `R20`-`R23`, `R27`-`R40`, accessibility/UX requirements
- Level: unit, manual
- Fixture/setup: Canonical skill text under `skills/`, workflow guidance in `docs/workflows.md`, and skill-validator phrase/resource checks.
- Steps:
  - Assert `skills/code-review/SKILL.md` teaches deterministic applicability evidence, spec-first packet ordering, decomposition before artifact comparison, property-by-surface review, fidelity receipt, compression findings, and AND semantics.
  - Assert adjacent workflow/review skills preserve direct isolated review behavior and voluntary manual receipt recording.
  - Assert skill text does not introduce a finding quota or forced-finding rule.
  - Assert exact public wording guidance distinguishes stage names, review outcomes, matched error strings, config keys, and command-line flags from prose, comments, and rationale.
  - Execute `MP-RFG-003` for public skill scan-first usability when the change modifies a public skill teaching the gate.
- Expected result: Reviewers receive actionable fidelity instructions without changing manual-review scope or incentivizing noisy findings.
- Failure proves: The process layer exists in validators but not in the public guidance reviewers actually follow.
- Automation location: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `MP-RFG-003` evidence recorded in milestone evidence.

### T12. Generated local skills and public adapter outputs are refreshed only through normal generation

- Covers: `R49`, M5 generated-output obligations
- Level: smoke, integration
- Fixture/setup: Canonical skill changes from M1 or M3, generated local skill check, and temporary public adapter archive output.
- Steps:
  - Run `python scripts/test-build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
  - Run `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5` when canonical skill behavior changes.
  - Assert no generated public adapter skill body is hand-edited as tracked source.
- Expected result: Generated outputs are current and produced by repository-owned generation commands.
- Failure proves: Canonical guidance and generated/install surfaces can drift.
- Automation location: `python scripts/test-build-skills.py`; `python scripts/build-skills.py --check`; `python scripts/build-adapters.py`; `python scripts/validate-adapters.py`.

### T13. Observability, selected validation routing, and bounded evidence are available for new surfaces

- Covers: inputs/outputs, observability, performance expectations, M4 selector routing, M5 selected CI
- Level: integration, smoke
- Fixture/setup: Changed review-artifact fixtures, calibration fixtures, lifecycle fixtures, change metadata, active plan, and the new test spec path.
- Steps:
  - Add selector tests so changed requirement-fidelity review fixtures route to `review_artifacts.regression` and `review_artifacts.validate`.
  - Add selector tests so changed lifecycle fixtures route to `artifact_lifecycle.regression` and `artifact_lifecycle.validate`.
  - Add selector tests so changed skill sources route to skill validation, generation regression, drift checks, and adapter proof where applicable.
  - Run selected CI with the final changed-path set before code-review handoff.
  - Assert review/calibration records expose applicability result, trigger evidence, spec clause IDs, decomposition source, properties, surfaces, validator comparison, compressed-risk result, not-applicable reason, finding IDs, corpus iteration, seed type, expected finding, observed finding, and recall result.
- Expected result: New proof surfaces are routed to the right validators and provide inspectable evidence without broad full-spec reads for unrelated changes.
- Failure proves: The new gate has artifacts that can drift without selected validation or observable evidence.
- Automation location: `python scripts/test-select-validation.py`; `bash scripts/ci.sh --mode explicit --path <changed paths>`; relevant validator tests.

### T14. Behavior-preservation and lifecycle state synchronization remain valid through closeout

- Covers: `R2`, `R3`, `R46`-`R50`, M5 behavior-preservation obligations
- Level: integration, migration
- Fixture/setup: Change-local `behavior-preservation.md`, active plan, `docs/plan.md`, change metadata, review log, review resolution, and all touched lifecycle artifacts.
- Steps:
  - Record behavior-preservation evidence showing independent-review behavior is unchanged, clean-review receipt behavior is strengthened only when applicable, validator tests use selected matrices, workflow stage order is unchanged, autoprogression uses both receipts when applicable, and historical reviews are preserved.
  - Validate active plan and plan index state before downstream handoff.
  - Validate change metadata, review artifacts, and artifact lifecycle state after every review or milestone state change.
  - Add fixtures or assertions proving final holistic code-review remains required before explain-change and verify after all implementation milestones close.
- Expected result: Lifecycle state remains synchronized and the fidelity gate strengthens review quality without stale plan/index/change-record state.
- Failure proves: The implementation can pass local tests while workflow evidence, plan state, or review gates drift.
- Automation location: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `python scripts/validate-change-metadata.py ...`; `python scripts/validate-review-artifacts.py --mode structure ...`; `git diff --check -- <changed paths>`.

### T-RFG-PERF-001. Bounded spec-read behavior

- Covers: performance expectations, `RFG-024`, M3 implementation-internal performance contract
- Level: integration
- Surface: implementation spec-read instrumentation
- Fixture/setup: Representative review fixtures under `tests/fixtures/requirement-fidelity-gate/representative-reviews/`.
- Command: `python scripts/test-fidelity-gate-spec-reads.py --review-set tests/fixtures/requirement-fidelity-gate/representative-reviews --max-bytes-per-clause 4096 --assert-no-broad-reads`
- Steps:
  - Instrument the gate's spec-reader path to record cited spec clause IDs and byte counts during representative review fixture runs.
  - Run the command above against the representative review set.
  - Assert total bytes read for each cited spec clause are no more than the clause bounds: default 4096 bytes per clause unless the clause itself is larger.
  - Assert no full spec-file read is observed in any review fixture.
- Expected result: The implementation proves bounded spec-read behavior without relying on broad manual inspection.
- Failure proves: The gate can satisfy review evidence only by broad-reading full specs or excessive unrelated context.
- Owning milestone: M3.

### T-RFG-GATE-001. No implementation activity before test-spec-review

- Covers: state and invariants, lifecycle gating, M2 lifecycle-state gating
- Level: integration
- Surface: `scripts/lifecycle_state_sync.py`
- Command: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/<change-id>/`
- Steps:
  - Validate a change fixture in implementation-active state whose `test-spec-review` recording is approved, recorded, and has no open blockers.
  - Validate a negative fixture with implementation activity but no approved-and-recorded `test-spec-review` precondition.
  - Assert the negative fixture is rejected with stop reason `implementation-without-test-spec-review`.
- Expected result: Implementation-active workflow state is permitted only after approved-and-recorded test-spec-review evidence exists.
- Failure proves: The lifecycle validator permits implementation before the test-spec-review gate has completed.
- Owning milestone: M2.

## Manual proof cases

### Manual proof MP-RFG-001. Private rotating corpus custody

Stable ID: MP-RFG-001
Automation rationale: Existence of the configured private path and presence of rotation-log fields are machine-checkable in `T8`, but confirming that the corpus is not also stored in an unauthorized public, shared, or mirrored location requires inspection of repository history, team storage indices, and operator-known mirrors that no validator can enumerate deterministically.
Owning stage: scheduled-audit
Required environment: repository checkout; access to the configured private corpus location; access to team artifact storage indices listed in `docs/calibration/corpus-config.yaml`.
Exact steps:
1. Run `python scripts/audit-private-corpus-config.py --config docs/calibration/corpus-config.yaml` to print the configured private path.
2. Confirm the path is outside `docs/`, `tests/`, and any other tracked repository directory.
3. Run `git log --all -- <configured_path>` and confirm no commits exist on any branch.
4. For each team storage index in `corpus-config.yaml`, search for the corpus identifier and confirm only the authorized location appears.
5. Sample three or more previous rotation log entries and confirm each names a previous `iteration_id`, next `iteration_id`, `rotation_trigger`, `rotated_by`, and `rotation_date`.
Evidence artifact: `docs/calibration/private-corpus-custody-audit-<YYYYMMDD>.md`
Pass condition: configured path is outside the repository; no git history exists for it; no unauthorized storage location contains the corpus identifier; sampled rotation log entries are complete.
Failure condition: any condition above fails, the rotation log is missing, or rotation log entries lack required fields.
Owner role: Review-calibration-corpus maintainer
Cadence: every `R44` rotation trigger plus a scheduled audit at least quarterly.

### Manual proof MP-RFG-002. Receipt-prose quality

Stable ID: MP-RFG-002
Automation rationale: Sampling at the `R45` floor rate is automated by `scripts/sample-fidelity-receipts.py`; classification of receipt prose as substantive, boilerplate, or misclassified requires human judgment over the match between the cited spec clause and the receipt's decomposition table.
Owning stage: calibration
Required environment: repository checkout; access to review records under `docs/changes/`; the closed-enum reasons list from `R45`; the spec clauses cited by each sampled receipt.
Exact steps:
1. Run `python scripts/sample-fidelity-receipts.py --rate 0.05 --since <last-cycle> --output <tmp>` to produce a stratified sample.
2. For each not-applicable receipt, read the bounded reason and confirm it falls within the closed enum from `R45`.
3. For each applicable receipt, read the decomposition table and verify each row's properties match the cited spec clause text.
4. Classify each receipt as `correct`, `misclassified-should-have-applied`, `out-of-scope`, or `incomplete-decomposition`.
5. Route any misclassification or incomplete decomposition to corrective action per `R45`.
Evidence artifact: `docs/calibration/receipt-quality-audit-<YYYYMMDD>.md`
Pass condition: at least 95 percent of sampled receipts are classified `correct`; all misclassifications have recorded corrective action.
Failure condition: classification rate is below 95 percent, any misclassification lacks corrective action, or sampling rate is below the `R45` floor.
Owner role: Review-calibration-corpus maintainer
Cadence: monthly per `R45`.

### Manual proof MP-RFG-003. Public skill scan-first usability

Stable ID: MP-RFG-003
Automation rationale: Word count and structural completeness are machine-checkable, but whether the gate's mechanics are extractable in bounded reading time by a reviewer unfamiliar with the change is a human-readability test that no validator can simulate.
Owning stage: code-review
Required environment: a reader who has not participated in the change being reviewed; the changed `skills/<skill>/SKILL.md` file; a stopwatch or timer.
Exact steps:
1. Identify the changed skill file.
2. Provide the file to the reader without additional context or summary.
3. Start the timer and ask the reader to identify when the gate applies, what the reviewer must produce, and what the receipt must contain.
4. Stop the timer and record answers and elapsed time.
5. Compare answers against the cited R-clauses for each property.
Evidence artifact: `docs/changes/<change-id>/scan-first-audit.md`
Pass condition: all three properties are correctly extracted within 120 seconds.
Failure condition: any property is missing or wrong, or elapsed time exceeds 120 seconds.
Owner role: code-review skill owner
Cadence: every change that modifies a public skill teaching the gate.

## Fixtures and data

- Review artifact fixtures under `tests/fixtures/review-artifacts/` for valid and invalid applicability manifests, packet ordering, decompositions, matrices, receipts, compression findings, calibration records, corpus iterations, and rotation logs.
- Artifact lifecycle fixtures under `tests/fixtures/artifact-lifecycle/` for AND-semantics autoprogression, historical review compatibility, direct/manual review behavior, final holistic code-review, and plan/index synchronization.
- Change metadata fixtures under `tests/fixtures/change-metadata/` only when fidelity evidence or sampling records are represented in compact change metadata.
- Skill fixtures under `tests/fixtures/skills/` for R26 missing-property negative cases or equivalent fixture support in `scripts/test-skill-validator.py`.
- Requirement-fidelity representative review fixtures under `tests/fixtures/requirement-fidelity-gate/representative-reviews/` for bounded spec-read instrumentation.
- Calibration corpus configuration under `docs/calibration/corpus-config.yaml`, plus private rotation custody evidence artifacts under `docs/calibration/`.
- Public examples may document defect classes, but protected rotating corpus iterations should not be limited to static public examples.

## Mocking/stubbing policy

- Use filesystem fixtures and temporary directories for review artifacts, lifecycle roots, generated skill output, and adapter archive validation.
- Do not call external services or network resources.
- Do not mock the validator functions being tested; construct fixtures that exercise real parsing and validation paths.
- Mocking is acceptable only for temporary filesystem roots, current date/time when a deterministic calibration cycle is required, and generated-output directories.

## Migration or compatibility tests

- `T9` proves historical clean reviews remain historical evidence when they lack fidelity receipts.
- `T9` proves direct isolated and manual reviews are not forced into mandatory first-slice applicability classification.
- `T12` proves generated output is refreshed through normal generation rather than hand-edited.
- `T14` proves lifecycle state remains synchronized across plan body, plan index, change metadata, review log, and review resolution.

## Observability verification

- Review evidence must expose applicability result, affected paths, path triggers, category triggers, overrides, override justification, review stage, spec clause IDs, decomposition source, properties, surfaces, per-property/per-surface results, validator comparison, compressed-risk result, no-finding rationale, and material finding IDs.
- Calibration evidence must expose corpus iteration, seed type, expected finding, observed finding, recall result, sampling reason, audit outcome, corrective action when applicable, and rotation trigger.
- Validation evidence must record exact commands run and pass/fail result in change metadata and plan validation notes.

## Security/privacy verification

- Review packets, receipts, findings, and calibration fixtures must not require secrets, credentials, private network access, or side-effecting external systems.
- Validators should reject or avoid private chain-of-thought fields and machine-local sensitive paths when they appear in review evidence unless the path is intentionally part of a fixture.
- Requirement-compression findings affecting security, privacy, compatibility, or release gates must be material and may be blocking under `T6`.

## Performance checks

- Applicability computation should operate from changed paths, trigger constants, review stage, and bounded evidence.
- Receipt and calibration validation should be cheap enough to run in targeted review-artifact, lifecycle, or skill validation.
- `T-RFG-PERF-001` proves the implementation does not require broad full-spec reads for changes unrelated to normative contracts.

## Manual QA checklist

- Execute `MP-RFG-001` for private rotating calibration corpus custody.
- Execute `MP-RFG-002` for sampled receipt-prose quality.
- Execute `MP-RFG-003` for public skill scan-first usability when public skill guidance changes.
- Confirm behavior-preservation evidence is specific to independent gates, manual review scope, historical reviews, generated output, and no finding quota.
- Confirm `T-RFG-PERF-001` and `T-RFG-GATE-001` are implemented as automated tests, not downgraded to manual proof cases.

## What not to test and why

- Do not test full automatic requirement extraction from arbitrary prose; the first slice explicitly defers it.
- Do not rewrite or validate every historical review record; the spec is forward-looking and preserves historical evidence.
- Do not require every existing validator to use property matrices; the first slice covers changed or selected contracts, with R26 as the pilot.
- Do not test hosted services, databases, queues, external APIs, or network behavior; the architecture introduces none.
- Do not assert exact prose wording for comments, rationale, or narrative descriptions unless another governing artifact makes the wording normative.
- Do not make seeded-defect recall depend only on public fixed fixtures; public examples are illustrative and rotating instances own measurement value.

## Uncovered gaps

None. Requirements that cannot be fully proven structurally have manual contract review steps or calibration evidence requirements.

## Next artifacts

```text
test-spec-review
implementation
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Ready for `test-spec-review`. Implementation remains blocked until the test spec is reviewed and the active plan handoff allows `implement`.
