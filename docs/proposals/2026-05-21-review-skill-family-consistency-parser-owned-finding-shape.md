# Review-Skill Family Consistency and Parser-Owned Finding Shape

## Status

accepted

## First principle

```text
A review artifact is at once a human judgment and a machine-parseable record.
The review skills must make the machine-readable field shape the primary,
single-sourced contract that all review skills share, rather than prose each
skill restates and each reviewer re-derives.
```

Everything in this proposal follows from that principle. The 2026-05-20 review-artifact-field-shape learn session showed the cost of violating it: a reviewer wrote human-readable finding bullets that were valid to a person but invalid to the parser, because the material-finding field block was prose to be re-derived rather than a shared, primary contract.

## Problem

The review-skill family (`code-review`, `proposal-review`, `spec-review`, and the other `*-review` skills) shares large, near-identical blocks of text that are independently restated in each skill:

- Material findings shape (Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path).
- Isolation and Recording rules (recorded/blocked status, lightweight receipt vs detailed record, isolation does not suppress recording).
- Finding severity enums.
- Evidence collection efficiency guidance.
- When-full-file-read-is-required guidance.
- Artifact placement lookup order.
- The Result output skeleton.

This duplication has three costs:

1. Drift surface. The same rule restated in N skills can desync. The recent learn session's failure rode in on exactly this: the material-finding field shape is described in prose in each review skill, and a reviewer satisfied the human description while missing the parser-required `Finding ID:` field.
2. Formalism risk in output. Because the finding shape is prose, a reviewer can produce a human-valid, parser-invalid finding. The validator catches it after the fact, but the skill should make the validator-shaped record the first-pass default.
3. Inconsistency. Each review skill has slightly different surrounding wording for the same machinery, so a reviewer moving between them re-orients each time, and a maintainer fixing a recording rule must fix it in many places.

The most recent learn session classified the root cause as source-shape substitution: replacing the parser-owned field shape with a prose habit. The fix it identified ("start material findings from the field block; use validator fixture shape as the example source; validate structure first") is a per-reviewer discipline. This proposal asks whether the skills can make that discipline the structural default rather than a thing each reviewer must remember.

## Goals

- Establish the parser-owned finding field block as the primary, shared contract across all review skills.
- Provide the material-finding field block as a packaged `assets/material-finding.md` template that review skills `COPY`, so the first-pass record starts in the validator-shaped structure by default.
- Provide the result block as a packaged `assets/review-result-skeleton.md` per review skill.
- Reduce duplicated review machinery across review skills without changing any review rule, severity enum, recording rule, or lifecycle boundary.
- Preserve every review skill's distinct review dimensions, stop conditions, and handoff behavior in its own `SKILL.md`.
- Keep shared rules single-sourced where the mechanism allows, and explicitly defer cross-skill deduplication that would require build-time partials.

## Non-goals

- Do not change any review dimension, severity value, recording rule, review-status value, stop condition, or lifecycle boundary in any review skill.
- Do not change review judgment, what counts as a finding, or what blocks a stage.
- Do not introduce packaged `references/` for review skills.
- Do not introduce packaged `scripts/` for review skills.
- Do not introduce build-time partials or include syntax to deduplicate shared prose. That is a separate mechanism with separate risk; cross-skill rule deduplication beyond assets is deferred.
- Do not change the review-artifact validator's parsing contract. Assets conform to the validator that already exists, not the other way around.
- Do not move review-policy prose (dimension definitions, severity policy, recording rules, scope-preservation rules, Vision fit review rules) into assets. Assets carry field shape only.
- Do not apply this to non-review skills in this proposal.
- Do not hand-edit generated adapter output or retroactively rewrite legacy adapter archives.

## Vision fit

fits the current vision

`VISION.md` commits RigorLoop to making artifacts easier to inspect, reason about, validate, and maintain. Review artifacts are the records by which the project proves its own rigor. Making the parser-owned finding shape the primary, shared, single-sourced contract directly serves inspectability and validation, while preventing the source-shape-substitution failure the learn session recorded.

The proposal is falsified if the change causes any of:

```text
- a review dimension, severity value, recording rule, review-status value,
  stop condition, or lifecycle boundary changes meaning;
- a review skill produces a different verdict or finding set on a representative input;
- an asset contains review judgment or review-policy prose beyond field labels,
  placeholders, and short fill hints;
- a finding asset's field set diverges from the review-artifact validator's
  parser contract;
- a representative valid fill from the finding asset fails structure validation,
  or representative invalid fills are not rejected by validation;
- a finding asset is referenced but missing from generated adapter output;
- common-path SKILL.md grows without recorded rationale;
- generated adapter output is hand-edited instead of built from canonical skills.
```

Token reduction does not offset any of these.

## Context

- The review skills inspected (`code-review`, `proposal-review`, `spec-review`) share the Material findings block, the Isolation and Recording block, severity enums, evidence-collection guidance, full-file-read guidance, and artifact-placement guidance nearly verbatim.
- The 2026-05-20 learn session `review-artifact-field-shape` recorded a source-shape-substitution failure and routed a durable lesson to `docs/learn/topics/review-artifact-recording.md`.
- The published-skill design contract and the assets-first pilots established: assets are copy-and-fill structural templates; the smell test ("if the metadata header is larger than the template body, the asset probably does not earn a file") excludes one-line rows; review-class skills are deliberative, so assets carry field shape only, never review judgment.
- The proposal-family assets proposal already specified `material-finding.md` and `review-result-skeleton.md` for `proposal-review`. This proposal generalizes that to the whole review family and ties it to the first principle.
- The review-artifact validator (`scripts/review_artifact_validation.py`) already owns the parser contract for finding fields. This proposal makes assets conform to it.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Optimize the review-skill family | in scope | Goals, Recommended direction |
| Apply the first principle (parser-owned shape) | in scope | First principle, Goals |
| Use assets where they earn a file | in scope | Recommended direction, Asset contract |
| Preserve review behavior | in scope | Vision fit, Non-goals, Testing and verification strategy |
| Reduce cross-skill duplication | in scope | Recommended direction; build-time partials deferred |
| Full cross-skill rule deduplication | deferred follow-up | Non-goals, Follow-on artifacts |
| Apply to non-review skills | out of scope | Non-goals |

## Scope budget

| Work item | Treatment | Reason |
|---|---|---|
| Add `assets/material-finding.md` to each review skill | core to this proposal | Six-field, error-prone, multi-instance structure that earns a file by the established smell test; directly fixes the learn-session failure. |
| Add `assets/review-result-skeleton.md` to each review skill | core to this proposal | The result block is a substantial structural template the skill produces. |
| Add `COPY` resource-map entries and validate asset presence in adapters | same-slice dependency | Asset packaging is part of the observable adapter contract. |
| Add validator coverage proving finding-asset field set matches the parser contract | same-slice dependency | The first principle requires the asset to match the parser, provably. |
| Record behavior-preservation and parity evidence | same-slice dependency | Proves the pass is structural, not behavioral. |
| Single-source shared recording rules via build-time partials | separate proposal | Requires a new build mechanism; out of the assets-only slice. |
| Packaged `references/` for review dimensions or severity policy | separate proposal | References can hide judgment; review-class risk. |
| Row assets for single-line structures | out of scope | Fails the smell test; the spec-family review established that one-line rows stay inline. |

## Priority order

```text
1. Preserved review behavior (no rule, severity, recording, or handoff change).
2. Parser-shaped findings by default, with validation as the backstop (the first-principle fix).
3. Reduced duplication and drift across the review family.
4. Common-path SKILL.md readability.
5. Token cost.
```

Token cost is not a driver. Behavior preservation outranks every other goal.

## Options considered

| Option | Verdict | Rationale |
|---|---|---|
| Keep finding and result shapes inline as prose in each review skill | rejected option | Preserves the current source-shape-substitution failure mode and leaves parser conformance as reviewer discipline. |
| Add field-shape assets for material findings and result skeletons, with parser-conformance checks | recommended | Makes the copied finding block the parser contract while keeping review judgment and policy in `SKILL.md`. |
| Introduce build-time partials now to single-source shared rules and the identical finding block | deferred follow-up | Solves more duplication but requires a separate build mechanism and broader risk than this assets-only slice. |
| Move review rubrics, severity policy, or recording rules into packaged references | rejected option | Review-class assets must not hide judgment or policy away from the main skill body in this proposal. |
| Apply the pattern to every `*-review` skill immediately | deferred follow-up | The first slice should cover the highest-volume duplicated skills and prove the contract before broadening. |
| Use a shared result skeleton or shared base result skeleton in this slice | rejected option | Shared status fields would homogenize distinct review-status semantics, especially `code-review` `clean-with-notes` versus gate-review `approved`. |

## Recommended direction

Add two assets to each in-scope review skill, carrying field shape only, conforming to the existing parser contract:

```text
each in-scope review skill:
  assets/material-finding.md
  assets/review-result-skeleton.md
```

The principle:

```text
The finding block the reviewer copies IS the parser contract.
A reviewer who starts from the asset starts from the correct parser-shaped
record by default; validation remains the backstop for bad fills or edits.
```

This makes the learn session's discipline ("start from the field block") the structural default: the reviewer copies `material-finding.md`, which already contains the literal `Finding ID:`, `Severity:`, `Location:`, `Evidence:`, `Required outcome:`, and `Safe resolution path:` labels the validator parses. The prose-bullet substitution becomes structurally hard to commit, while the validator still catches blank required fields, non-enum values, renamed labels, and other invalid fills.

### Why these two assets and not more

| Candidate | Verdict | Reason |
|---|---|---|
| `material-finding.md` | earns a file | Six fields, error-prone, used once per finding (multi-instance), and directly maps to the parser contract. The exact structure the learn session failure was about. |
| `review-result-skeleton.md` | earns a file | Substantial result block; one per review; moves real structure out of the body. |
| `severity-row.md`, `checklist-row.md`, `dimension-row.md` | stay inline | One-line or fixed-list structures; fail the smell test; the spec-family review already established these stay inline. |

### What stays in SKILL.md

Every review skill keeps in its own body:

```text
- its review dimensions / checklist (deliberative judgment);
- severity enum and its meaning;
- review-status enum;
- recording rules and isolation rules (until build-time partials exist);
- stop conditions;
- workflow handoff behavior;
- the compact result-output summary plus a COPY pointer to the result skeleton.
```

Assets carry field shape; `SKILL.md` carries judgment, rules, and routing.

## Asset contract

An asset here is a packaged, skill-local, copy-and-fill structural template substantial enough to justify a file, conforming to the review-artifact parser contract.

An asset is not:

```text
- a review rubric or dimension definition;
- severity policy;
- recording or isolation rules;
- a one-line row whose shape is already inline;
- a hidden source of enum values;
- a substitute for SKILL.md review judgment.
```

Smell test carried from prior asset work:

```text
If the metadata header is larger than the template body, the asset does not earn a file.
```

`material-finding.md` clears the smell test: six labeled fields, not one line.

Resource verbs: `COPY` for `assets/` only. `READ` (`references/`) and `RUN` (`scripts/`) are reserved and not used here.

Asset metadata header:

```md
<!-- Template: <template-id> -->
<!-- Skill: <skill-name> -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/<skill-name>/SKILL.md -->
```

Placeholders use `<field-name>`; unfilled placeholders must not appear in final output.

## Parser-conformance boundary

This is the proposal's defining constraint and the operational form of the first principle.

```text
The finding asset's field set must equal the review-artifact validator's parsed field set.
```

Specifically:

- `assets/material-finding.md` contains exactly the labels the validator parses: `Finding ID:`, `Severity:`, `Location:`, `Evidence:`, `Required outcome:`, `Safe resolution path:` (and the `needs-decision` rationale variant where the validator accepts it).
- A validator check proves the asset's labels match the parser contract, so the asset cannot drift from what the validator requires.
- If the parser contract changes in a future proposal, the asset changes with it, proven by the same check. The asset is downstream of the parser, never a competing source.

This is what makes the asset a fix rather than a new drift surface: the asset and the parser are bound by a check, not by hope.

## Review-class asset boundary

Review skills are deliberative. Their assets carry only headings, field labels, placeholders, and short fill hints. They must not carry dimension definitions, severity policy, recording rules, scope-preservation rules, Vision fit review rules, or review guidance of any kind. Those remain in `SKILL.md`.

A validator allowlist of structural labels plus a forbidden-review-policy-label check enforces this, following the pattern established for the proposal-family review assets.

## Proposed asset layout

```text
skills/code-review/assets/
  material-finding.md
  review-result-skeleton.md
skills/proposal-review/assets/
  material-finding.md
  review-result-skeleton.md
skills/spec-review/assets/
  material-finding.md
  review-result-skeleton.md
```

The `material-finding.md` field block is identical across review skills because it is the shared parser contract. The `review-result-skeleton.md` differs per skill because each review skill's Result block has skill-specific fields, such as `Reviewed milestone` for `code-review` and eventual test-spec readiness for `spec-review`.

The identical `material-finding.md` across skills is itself a duplication. Single-sourcing it is the deferred build-time-partials follow-up; this proposal accepts three identical copies bound to one parser contract by check, which is safer than three prose restatements.

The same check also records whether the parser-owned field block is byte-identical across all in-scope review skills. Until build-time partials exist, parser-relevant fields must stay identical; non-parser comments or fill hints may vary only when the preservation evidence records why that variation is intentional and harmless.

## First-slice review family

The first slice is selected by explicit criteria, not by intuition:

| Selection criterion | Why it picks the first-slice skills |
|---|---|
| Highest review volume | `code-review`, `proposal-review`, and `spec-review` run on most substantive changes; `plan-review` and `architecture-review` run conditionally. |
| Most shared machinery | The first-slice skills carry the identical finding block, recording rules, and severity enum duplication this proposal targets. |
| Already contract-compliant | The first-slice skills have been through readability normalization and share a cleaner extraction baseline. |
| Has a parity baseline | The first-slice skills have prior review records that can support representative behavior-parity checks. |

Full current `*-review` family:

| Review skill | First slice? | Reason |
|---|---|---|
| `code-review` | Yes | High volume, high duplication, already normalized, and has parity baseline. |
| `proposal-review` | Yes | High volume, high duplication, already normalized, has parity baseline, and already had material-finding/result assets proposed in the proposal-family assets work. |
| `spec-review` | Yes | High volume, high duplication, already normalized, and has parity baseline. |
| `plan-review` | Defer | Lower-volume conditional stage; add in slice 2 after the first-slice contract is proven. |
| `architecture-review` | Defer | Conditional stage that does not run on every change; add in a later slice after first-slice validation evidence exists. |

The first-slice set is spec-resolvable because the spec amendment defines which skills the parser-conformance and asset-packaging contract governs. The plan sequences the selected skills into milestones; it does not decide the contract surface.

## Resource map pattern

```md
## Resource map

- COPY `assets/material-finding.md` once per material finding.
  Fill: Finding ID, Severity, Location, Evidence, Required outcome, Safe resolution path.
  Confirm the literal `Finding ID:` line exists before linking the finding from
  review-log.md or review-resolution.md.
  Do not emit unfilled placeholders.
- COPY `assets/review-result-skeleton.md` as the review result block.
  Fill: the result fields for this skill.
  Do not emit unfilled placeholders.
```

The "confirm the literal `Finding ID:` line" instruction encodes the learn session's cross-file-reference rule directly into the resource map.

A future validator check for this concern is a referential-integrity check, not a parser-conformance check: it would verify that a Finding ID referenced in `review-log.md` or `review-resolution.md` resolves to a detailed record containing the literal `Finding ID:` field. That check is deferred unless the failure recurs once after this slice ships, or the next review-artifact learn session cites the same cross-file-reference failure.

## Behavior preservation boundary

This is an asset-extraction and shape-standardization pass, not a behavior change. For each extraction, record a preservation matrix mapping the source field set to the asset field set, proving identical labels and identical meaning. Each `review-result-skeleton.md` preserves its source skill's review-status enum and skill-specific fields verbatim; no status vocabulary is homogenized across skills. A structural pass is insufficient if it changes field names, field obligations, severity values, review-status values, recording rules, or stop conditions.

## Expected behavior changes

- Each in-scope review skill ships `material-finding.md` and `review-result-skeleton.md`.
- A reviewer starts from the finding asset and gets the parser-shaped field block by default.
- The finding asset's labels provably match the validator parser contract.
- The validator rejects representative invalid fills of the asset, including a blank `Finding ID:`, a non-enum `Severity:`, and a renamed parser-owned label.
- Generated adapter output contains each asset.
- Review judgment, dimensions, severity, recording rules, and handoff behavior remain unchanged in each `SKILL.md`.
- Representative review behavior is unchanged: same verdicts, same findings, same recording outcomes.

## Architecture impact

| Surface | Impact |
|---|---|
| `skills/<review-skill>/SKILL.md` | Adds resource map; replaces inline finding/result shape with compact summary plus COPY pointer; keeps all rules and judgment. |
| `skills/<review-skill>/assets/*.md` | New structural templates conforming to the parser contract. |
| `scripts/review_artifact_validation.py` | No parsing-contract change; remains the source of truth the assets conform to. |
| `scripts/skill_validation.py` / `scripts/test-skill-validator.py` | Add asset coverage and the parser-conformance check. |
| `scripts/build-skills.py`, `build-adapters.py`, `validate-adapters.py` | Must package and verify review-skill assets. |
| Adapter roots, lockfiles, CLI | No change. |

## Testing and verification strategy

| Check ID | What is verified |
|---|---|
| `RFA-001` | Each review skill has a resource map for every packaged asset. |
| `RFA-002` | Each resource-map entry uses literal `COPY`. |
| `RFA-003` | Each asset has required metadata comments and an allowed status. |
| `RFA-004` | `material-finding.md` field labels exactly match the review-artifact validator parser contract. |
| `RFA-004b` | The `material-finding.md` parser-owned field block is byte-identical across all in-scope review skills, or any non-parser variation is explicitly recorded as intentional and harmless. |
| `RFA-005` | Assets contain no review judgment, dimension definitions, severity policy, or recording rules. |
| `RFA-006` | Assets contain visible placeholders and no disallowed filler prose. |
| `RFA-007` | Generated skill mirror and adapter archives include all review-family assets. |
| `RFA-008` | No generated adapter body or asset is hand-edited. |
| `RFA-009` | Preservation matrices prove source-to-asset field parity for each review skill, including verbatim preservation of each skill's review-status enum and skill-specific result fields. |
| `RFA-010` | Representative review behavior parity is unchanged (same verdicts, findings, recording). |
| `RFA-011` | A representative finding produced by copying the asset passes `scripts/validate-review-artifacts.py --mode structure`. |
| `RFA-011b` | Representative invalid fills based on the asset fail structure validation, including blank `Finding ID:`, non-enum `Severity:`, and renamed parser-owned label. |
| `RFA-012` | Common-path `SKILL.md` token count is measured separately from packaged asset footprint. |
| `RFA-013` | Cold-read confirms a reviewer can produce a valid finding from the installed skill and its assets alone. |

`RFA-004`, `RFA-011`, and `RFA-011b` are the first-principle checks: the asset matches the parser, a valid finding built from the asset validates, and malformed fills remain validator failures.

Suggested validation commands:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/validate-review-artifacts.py --mode structure docs/changes/<change-id>
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --output-dir <tmpdir>
python scripts/validate-adapters.py --root <tmpdir> --version <version>
python scripts/measure-skill-tokens.py
git diff --check --
```

## Token-cost expectation

As with prior skeleton assets, total packaged footprint may grow while common-path `SKILL.md` shrinks. This is acceptable: the justification is parser-shaped findings by default, validator backstops for malformed fills, and common-path readability, not total-token reduction. Record the common-path delta and the per-skill asset usage fraction so the plan does not misread a total-footprint increase as a regression.

## Rollout and rollback

Rollout:

1. Approve proposal.
2. Amend `specs/skill-contract.md` only if the existing asset contract does not cover review-family assets or the parser-conformance check.
3. Amend or add the test spec for review-family asset packaging and parser conformance.
4. Plan per-skill milestones: M1 `code-review`, M2 `proposal-review`, M3 `spec-review`, M4 family closeout and adapter proof.
5. Implement one review skill at a time.
6. Code-review per milestone.
7. Generated skill and adapter validation; review-artifact structure validation.
8. explain-change, verify, PR.

Rollback:

- Reinline the asset content into the owning `SKILL.md`.
- Remove the skill's `assets/` directory.
- Preserve generic validator improvements (parser-conformance check) if still valid.
- Rebuild generated mirrors and adapters from canonical skills.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Asset field set drifts from the parser contract. | `RFA-004` binds them by check; the asset is downstream of the parser. |
| Review judgment leaks into assets. | Review-class boundary plus forbidden-label validator check (`RFA-005`). |
| Identical `material-finding.md` copies drift across skills. | Bound to one parser contract by `RFA-004`; parser-owned field blocks checked across skills by `RFA-004b`; full single-sourcing deferred to build-time partials. |
| Total footprint grows. | Token-cost expectation states this is acceptable for shape assets; measure common-path separately. |
| A reviewer copies the asset and then makes an invalid fill or edits a parser-owned label. | `RFA-011` proves a valid finding built from the asset validates; `RFA-011b` proves representative bad fills fail validation; the resource map encodes the cross-file-reference confirmation. |
| Result skeleton extraction homogenizes distinct review-status vocabularies. | `RFA-009` requires each per-skill result skeleton to preserve its source skill's review-status enum and skill-specific result fields verbatim. |
| Behavior parity regresses. | Preservation matrices and representative parity per skill. |
| Scope creeps into references/scripts/partials. | Non-goals exclude them; deferred as follow-ups. |

## First-slice boundary

```text
in:
  skills/code-review/SKILL.md and assets/
  skills/proposal-review/SKILL.md and assets/
  skills/spec-review/SKILL.md and assets/
  parser-conformance validator check and fixtures
  generated skill and adapter validation proof
  behavior-preservation and parity evidence
  lifecycle artifacts for this change

out:
  other *-review skills not listed (separate follow-on if needed)
  references/, scripts/, build-time partials
  parser-contract changes
  review judgment, dimension, severity, or recording changes
  produced-artifact readability changes
```

## Acceptance criteria

| ID | Criterion |
|---|---|
| `AC-RFA-001` | Each in-scope review skill has `material-finding.md` and `review-result-skeleton.md` with required metadata. |
| `AC-RFA-002` | Each asset has a matching `COPY` resource-map entry. |
| `AC-RFA-003` | `material-finding.md` field labels exactly match the review-artifact validator parser contract. |
| `AC-RFA-004` | No asset contains review judgment, dimension definitions, severity policy, or recording rules. |
| `AC-RFA-005` | A finding produced by copying the asset passes review-artifact structure validation. |
| `AC-RFA-006` | Representative invalid fills based on the finding asset fail review-artifact structure validation. |
| `AC-RFA-007` | Preservation matrices prove source-to-asset field parity per skill, including review-status enum and skill-specific result fields. |
| `AC-RFA-007b` | In-scope `material-finding.md` parser-owned field blocks are byte-identical across skills unless intentional harmless non-parser variation is recorded. |
| `AC-RFA-008` | Representative review behavior parity is unchanged per skill. |
| `AC-RFA-009` | Generated adapter archives include all review-family assets; none hand-edited. |
| `AC-RFA-010` | Common-path `SKILL.md` token counts are recorded separately from asset footprints. |
| `AC-RFA-011` | Cold-read confirms a reviewer can produce a valid finding from installed skill and assets alone. |

## Settled open-question guidance

| Question | Decision | Resolvable in | Reasoning to carry forward |
|---|---|---|---|
| Which `*-review` skills are in the first slice? | `code-review`, `proposal-review`, and `spec-review`; defer `plan-review` and `architecture-review`. | spec | The selected set is the contract surface for the asset and parser-conformance checks. The deferred skills are visible follow-ons, not omissions. |
| Should `material-finding.md` be identical across skills now and single-sourced later? | Accept identical copies now, bound by `RFA-004` and `RFA-004b`; defer single-sourcing. | plan | Three checked-identical copies are deliberate bounded duplication. Build-time partials are a heavier mechanism and should wait until another shared concept needs the mechanism or a copy drifts despite checks. |
| Should the result skeleton be one asset per skill, or a shared base plus per-skill extensions? | One result skeleton per skill. Reject shared base in this slice. | spec | Result status enums carry different semantics. `code-review` uses `clean-with-notes`; proposal/spec gate reviews use `approved`. Homogenizing status vocabulary would be a behavior change. |
| Should cross-file-reference confirmation be a validator check or a resource-map instruction? | Both, sequenced: resource-map instruction now; referential-integrity validator check later on a concrete trigger. | plan | The original failure was one occurrence caught by validation, so instruction is the proportionate first response. Add the validator check after one recurrence post-slice, or if the next review-artifact learn session cites the same failure. |

These decisions do not block proposal review. They are settled inputs for the spec and plan so those artifacts do not re-open contract-surface questions without new evidence.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-20 | Make parser-owned field shape the primary shared contract | The learn session's source-shape-substitution failure is structural, not a one-off; the fix belongs in the skill, not only in reviewer discipline | Leave the fix as per-reviewer discipline only |
| 2026-05-20 | Package `material-finding.md` and `review-result-skeleton.md` as assets | Both clear the smell test; the finding block is the exact structure the failure was about | Keep finding shape inline as prose |
| 2026-05-20 | Bind the finding asset to the parser by check (`RFA-004`) | An asset that can drift from the parser is a new drift surface, not a fix | Asset as an independent restatement |
| 2026-05-20 | Accept identical `material-finding.md` copies for now | Three copies bound to one parser contract by check are safer than three prose restatements; true single-sourcing needs partials | Block on single-sourcing; add partials in this slice |
| 2026-05-20 | Defer build-time partials and references | Different mechanisms, different risk; keep this an assets-only slice | Bundle partials or references here |
| 2026-05-20 | No row assets | One-line rows fail the smell test, per the spec-family review | Template every substructure |
| 2026-05-21 | Treat assets and validation as complementary layers | The asset prevents source-shape substitution by making the parser-shaped block the default starting point, while validation still catches bad fills or edited labels | Claim the asset alone makes invalid findings impossible |
| 2026-05-21 | Select `code-review`, `proposal-review`, and `spec-review` as the first-slice contract surface | They are highest-volume, carry the most shared machinery, are already normalized, and have parity baselines | Include all `*-review` skills immediately; leave the first slice implicit |
| 2026-05-21 | Use one result skeleton per skill | Per-skill review-status enums carry different semantics; a shared base would risk homogenizing `clean-with-notes` and `approved` | Shared result skeleton; shared base plus extensions in this slice |
| 2026-05-21 | Defer cross-file referential-integrity validation until a concrete trigger | Resource-map instruction is the proportionate first response; one recurrence after this slice is enough evidence that instruction is insufficient | Add relationship validation immediately; defer on vague "if recurrence continues" wording |

## Next artifacts

```text
proposal-review
spec amendment if the asset contract does not cover review-family assets or the parser-conformance check
spec-review if a spec amendment is created
test-spec amendment for review-family asset and parser-conformance checks
plan
plan-review
implementation milestones
code-review
explain-change
verify
pr
```

## Follow-on artifacts

- Proposal review: [proposal-review-r1](../changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/reviews/proposal-review-r1.md)
- Spec: [Review-Skill Family Consistency and Parser-Owned Finding Shape](../../specs/review-skill-family-consistency-parser-owned-finding-shape.md)

Planned follow-ons after this proposal is reviewed or accepted:

- Build-time partials proposal to single-source the identical `material-finding.md` and the shared recording/isolation rules across review skills when another shared concept needs that mechanism, or when a checked copy drifts despite `RFA-004`/`RFA-004b`.
- Proposal to extend the pattern to deferred `plan-review` and `architecture-review` skills after the first-slice contract is validated.
- Proposal to add review-artifact referential-integrity validation if the cross-file-reference failure recurs once after this slice ships, or if the next review-artifact learn session cites the same failure.

## Readiness

Accepted. Downstream spec drafting has started; the spec owns its own review readiness.

## Core invariant

```text
The finding block a reviewer copies is the parser contract.

Review-family assets carry field shape only, bound to the review-artifact
validator by check. Review judgment, dimensions, severity, recording rules,
and handoff behavior stay in SKILL.md. A reviewer who starts from the asset
starts from the parser-shaped finding block by default; validation remains the
backstop for bad fills or edited labels. Every review skill produces the same
verdicts, findings, and recording outcomes after the pass as before it.
```
