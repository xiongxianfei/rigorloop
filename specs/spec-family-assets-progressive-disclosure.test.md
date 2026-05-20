# Spec-Family Assets Progressive Disclosure Test Spec

## Status

active

Owner approved on 2026-05-20.

This test spec is the active proof surface for implementing the approved [Spec-Family Assets Progressive Disclosure](spec-family-assets-progressive-disclosure.md) spec.

## Related spec and plan

- Spec: [Spec-Family Assets Progressive Disclosure](spec-family-assets-progressive-disclosure.md)
- Plan: [Spec-Family Assets Progressive Disclosure Plan](../docs/plans/2026-05-20-spec-family-assets-progressive-disclosure.md)
- Architecture/ADRs: not applicable; the approved plan records no separate architecture package because the change stays inside skill text, assets, validators, generated-output proof, and lifecycle evidence.

## Testing strategy

This is an assets-only skill packaging and preservation change. The proof combines deterministic static validation, manual source-to-asset preservation evidence, generated-output proof, and lifecycle artifact validation.

| Level | Use in this change |
| --- | --- |
| unit | Add or update validator fixture tests for asset mapping, metadata, placeholders, review-class boundaries, generated-output expectations, and baseline-summary presence. |
| integration | Run full skill validation and generated skill mirror checks against canonical skill changes. |
| smoke | Run selected lifecycle, change metadata, review-artifact, and whitespace checks for changed artifacts. |
| manual | Inspect preservation matrices, behavior parity, token measurements, cold-read evidence, generated temporary adapter contents, and any tracked-tree adapter debt deferral. |
| contract | Confirm every `SFA-R*`, example, edge case, and acceptance criterion is mapped to proof before implementation closeout. |
| migration | Not applicable; no data, CLI, adapter-root, lockfile, or release archive migration is in scope. |

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `SFA-R1` | `T3`, `T4`, `T5`, `T7` | integration | Asset directories are limited to the three spec-family skills and checked in generated output. |
| `SFA-R2` | `T2`, `T3`, `T4`, `T5`, `T9` | unit | Validator and review checks block references, scripts, partials, install-root, lockfile, CLI, and unrelated skill assets. |
| `SFA-R3` | `T2`, `T3`, `T4`, `T5`, `T6` | unit | Asset content and preservation evidence prove assets are structural templates only. |
| `SFA-R4` | `T3`, `T6` | manual | `spec` rules and lifecycle boundaries remain in `SKILL.md`. |
| `SFA-R5` | `T5`, `T6` | manual | `test-spec` rules and coverage obligations remain in `SKILL.md`. |
| `SFA-R6` | `T4`, `T6` | manual | `spec-review` review judgment and recording rules remain in `SKILL.md`. |
| `SFA-R7` | `T3`, `T6` | manual | `spec` full skeleton asset or fallback is proven. |
| `SFA-R8` | `T2`, `T3` | unit | `spec` asset count and approved paths are checked. |
| `SFA-R9` | `T2`, `T4` | unit | `spec-review` asset list is exactly scoped. |
| `SFA-R10` | `T2`, `T4` | unit | Review-dimension assets and review-judgment assets are blocked. |
| `SFA-R11` | `T5`, `T6` | manual | `test-spec` full skeleton asset or fallback is proven. |
| `SFA-R12` | `T2`, `T5` | unit | `test-spec` asset count and approved paths are checked. |
| `SFA-R13` | `T1`, `T9` | manual | Higher-count justification is either absent because caps are followed or recorded in the plan. |
| `SFA-R14` | `T2`, `T3`, `T4`, `T5` | unit | Each touched `SKILL.md` has a resource map naming every asset. |
| `SFA-R15` | `T2`, `T3`, `T4`, `T5` | unit | Resource-map entries use `COPY`, conditions, fill fields, and no-unfilled-placeholder instruction. |
| `SFA-R16` | `T3`, `T5`, `T6` | manual | Full skeleton assets have compact summaries in `SKILL.md`. |
| `SFA-R17` | `T3`, `T5`, `T6` | manual | Full skeleton is not duplicated in both locations. |
| `SFA-R18` | `T3`, `T5`, `T6` | manual | Inline fallback is recorded if review finds hidden contract risk. |
| `SFA-R19` | `T2`, `T3`, `T4`, `T5` | unit | Asset metadata comments are validated. |
| `SFA-R20` | `T2`, `T3`, `T4`, `T5` | unit | Only `normative` or `optional` statuses are accepted. |
| `SFA-R21` | `T2`, `T3`, `T4`, `T5` | unit | Visible placeholder policy is checked. |
| `SFA-R22` | `T2`, `T3`, `T4`, `T5` | unit | Empty fields and filler prose are blocked. |
| `SFA-R23` | `T2`, `T4` | unit | `spec-review` assets are limited to structure, labels, placeholders, and short fill hints. |
| `SFA-R24` | `T2`, `T4` | unit | Review policy, severity policy, sufficiency rules, and examples are blocked from `spec-review` assets. |
| `SFA-R25` | `T1` | smoke | Baseline summary exists before skill edits. |
| `SFA-R26` | `T1` | manual | Baseline summary contains required per-skill content. |
| `SFA-R27` | `T1`, `T6` | manual | Baseline summary does not redefine PR #79 behavior. |
| `SFA-R28` | `T6` | manual | Preservation matrices exist for all extracted structures. |
| `SFA-R29` | `T6` | manual | Preservation proof covers fields, obligations, enums, stops, coverage, dimensions, and lifecycle boundaries. |
| `SFA-R30` | `T6` | manual | Representative behavior parity is recorded for all three skills. |
| `SFA-R31` | `T6` | manual | Parity evidence shows no regression across applicable skill behaviors. |
| `SFA-R32` | `T7` | integration | Generated skill mirrors include all mapped assets. |
| `SFA-R33` | `T7` | integration | Temporary adapter output includes all mapped assets. |
| `SFA-R34` | `T7` | integration | Adapter validation runs against temporary output or records a blocker. |
| `SFA-R35` | `T7` | manual | Tracked-tree adapter proof runs when supported. |
| `SFA-R36` | `T7` | manual | Any tracked-tree debt deferral is explicit and follows temporary proof. |
| `SFA-R37` | `T7`, `T9` | manual | Generated bodies and assets are not hand-edited. |
| `SFA-R38` | `T8` | manual | Token measurement separates common-path body size from total packaged footprint. |
| `SFA-R39` | `T8` | manual | Common-path decrease or justified exception is recorded. |
| `SFA-R40` | `T6`, `T8` | manual | Representative outputs do not contain unfilled placeholders. |
| `SFA-R41` | `T8` | manual | Cold-read evidence confirms installed skill output explains asset use. |
| `SFA-R42` | `T2` | unit | Validator or fixture coverage is updated for required checks. |
| `SFA-R43` | `T2` | unit | Hidden-rule checks use deterministic checks or declared bounded heuristics. |
| `SFA-R44` | `T1`, `T9` | manual | Contract gap blocks skill edits and routes to a spec amendment packet. |
| `SFA-R45` | `T1`, `T9` | manual | Sufficiency assessment is recorded before proceeding under this spec. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T3`, `T6` | Verifies `spec` full skeleton asset and compact `SKILL.md` summary. |
| `E2` | `T4`, `T6` | Verifies `spec-review` keeps dimensions and policy in `SKILL.md`. |
| `E3` | `T7` | Verifies generated mirrors and temporary adapter archives include mapped assets. |
| `E4` | `T1`, `T6` | Verifies baseline summary and source-to-asset preservation proof. |

## Edge case coverage

- `EC1`: `T3`, `T5`, `T6`
- `EC2`: `T4`
- `EC3`: `T7`
- `EC4`: `T7`
- `EC5`: `T8`
- `EC6`: `T6`, `T8`

## Test cases

### T1. Baseline summary and proof-route gate

- Covers: `SFA-R13`, `SFA-R25`, `SFA-R26`, `SFA-R27`, `SFA-R44`, `SFA-R45`, `E4`
- Level: manual
- Fixture/setup: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md`, `specs/skill-contract.md`, `specs/spec-family-assets-progressive-disclosure.md`, active plan.
- Steps:
  1. Confirm the baseline summary exists before any skill edit in M2 through M4.
  2. Confirm it records each skill's full skeleton section set, extracted substructure fields, closed enums kept in `SKILL.md`, stop conditions kept in `SKILL.md`, dimensions or coverage obligations kept in `SKILL.md`, and source locations.
  3. Confirm the plan records whether `specs/skill-contract.md` plus this spec is sufficient for multi-skill rollout, full-skeleton boundaries, and review-class restrictions.
  4. If a gap is found, confirm skill edits stop and a spec amendment packet is created before implementation proceeds.
  5. Confirm no asset count exceeds the plan cap unless the required higher-count justification is added.
- Expected result: baseline and proof-route gate are complete before implementation edits.
- Failure proves: implementation is proceeding without a stable behavior baseline or contract authority.
- Automation location: manual review plus `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` for the baseline and lifecycle artifacts when lifecycle validation covers the baseline path.

### T2. Asset validator and fixture coverage

- Covers: `SFA-R2`, `SFA-R3`, `SFA-R8`, `SFA-R9`, `SFA-R10`, `SFA-R12`, `SFA-R14`, `SFA-R15`, `SFA-R19`, `SFA-R20`, `SFA-R21`, `SFA-R22`, `SFA-R23`, `SFA-R24`, `SFA-R42`, `SFA-R43`, `AC-SFA-001` through `AC-SFA-006`, `AC-SFA-015`
- Level: unit
- Fixture/setup: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, validator fixtures for valid and invalid spec-family asset layouts.
- Steps:
  1. Add positive fixtures for the approved asset layouts.
  2. Add negative fixtures for unmapped assets, non-`COPY` resource-map verbs, missing fill fields, missing no-placeholder instruction, missing metadata, invalid statuses, missing visible placeholders, filler placeholder content, repository-root dependency requirements, extra assets, `review-dimension-row.md`, and review-policy prose in `spec-review` assets.
  3. Run the validator unit suite.
  4. Run full skill validation after canonical skill edits.
- Expected result: all positive fixtures pass, negative fixtures fail for the expected reason, and full skill validation passes.
- Failure proves: asset contract enforcement is missing or too broad/narrow.
- Automation location: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### T3. `spec` asset extraction

- Covers: `SFA-R1`, `SFA-R3`, `SFA-R4`, `SFA-R7`, `SFA-R8`, `SFA-R14` through `SFA-R22`, `SFA-R28` through `SFA-R31`, `SFA-R40`, `E1`, `EC1`
- Level: manual
- Fixture/setup: baseline summary, edited `skills/spec/SKILL.md`, `skills/spec/assets/*.md`, preservation matrix, behavior-parity evidence.
- Steps:
  1. Confirm only the four approved `spec` assets exist.
  2. Confirm `SKILL.md` retains rules, stops, routing, claim boundaries, closed enums, validation obligations, and lifecycle boundaries.
  3. Confirm `spec-skeleton.md` owns the full skeleton and `SKILL.md` keeps a compact output expectation summary, or record inline fallback.
  4. Confirm the full skeleton is not duplicated in both places.
  5. Confirm every extracted field maps to baseline source content.
  6. Confirm representative `spec` behavior parity has no unresolved regression.
- Expected result: `spec` asset extraction preserves behavior and satisfies the asset contract.
- Failure proves: `spec` assets changed or hid the skill contract.
- Automation location: `python scripts/validate-skills.py skills/spec/SKILL.md`; preservation and parity evidence under the change root.

### T4. `spec-review` review-class asset extraction

- Covers: `SFA-R1`, `SFA-R3`, `SFA-R6`, `SFA-R9`, `SFA-R10`, `SFA-R14`, `SFA-R15`, `SFA-R19` through `SFA-R24`, `SFA-R28` through `SFA-R31`, `E2`, `EC2`
- Level: manual
- Fixture/setup: baseline summary, edited `skills/spec-review/SKILL.md`, `skills/spec-review/assets/*.md`, preservation matrix, behavior-parity evidence.
- Steps:
  1. Confirm only `review-result-skeleton.md` and `review-finding.md` exist under `skills/spec-review/assets/`.
  2. Confirm no review-dimension asset exists.
  3. Confirm review dimensions, dimension table structure, review guidance, verdict enum, severity policy, material-finding sufficiency rules, recording obligations, validation obligations, and lifecycle boundaries remain in `SKILL.md`.
  4. Confirm assets contain only headings, field labels, placeholders, and short fill hints.
  5. Confirm representative `spec-review` behavior parity has no unresolved regression.
- Expected result: `spec-review` assets remain structural and do not carry review judgment.
- Failure proves: the review-class asset boundary was violated.
- Automation location: `python scripts/validate-skills.py skills/spec-review/SKILL.md`; validator negative fixtures from `T2`; preservation and parity evidence under the change root.

### T5. `test-spec` asset extraction

- Covers: `SFA-R1`, `SFA-R3`, `SFA-R5`, `SFA-R11`, `SFA-R12`, `SFA-R14` through `SFA-R22`, `SFA-R28` through `SFA-R31`, `SFA-R40`, `EC1`
- Level: manual
- Fixture/setup: baseline summary, edited `skills/test-spec/SKILL.md`, `skills/test-spec/assets/*.md`, preservation matrix, behavior-parity evidence.
- Steps:
  1. Confirm only the four approved `test-spec` assets exist.
  2. Confirm `SKILL.md` retains rules, stops, routing, claim boundaries, status and level enums, coverage obligations, validation obligations, and lifecycle boundaries.
  3. Confirm `test-spec-skeleton.md` owns the full skeleton and `SKILL.md` keeps a compact output expectation summary, or record inline fallback.
  4. Confirm the full skeleton is not duplicated in both places.
  5. Confirm every extracted field maps to baseline source content.
  6. Confirm representative `test-spec` behavior parity has no unresolved regression.
- Expected result: `test-spec` asset extraction preserves behavior and coverage obligations.
- Failure proves: `test-spec` assets changed or hid the proof-planning contract.
- Automation location: `python scripts/validate-skills.py skills/test-spec/SKILL.md`; preservation and parity evidence under the change root.

### T6. Preservation matrices and behavior parity

- Covers: `SFA-R3` through `SFA-R7`, `SFA-R11`, `SFA-R16` through `SFA-R18`, `SFA-R25` through `SFA-R31`, `SFA-R40`, `AC-SFA-007`, `AC-SFA-008`, `E4`, `EC1`, `EC6`
- Level: manual
- Fixture/setup: `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/behavior-preservation.md`, behavior-parity evidence, baseline summary.
- Steps:
  1. Confirm every extracted full skeleton or repeated substructure has a source-to-asset preservation row.
  2. Confirm preservation proof covers field names, obligations, enum values, stop conditions, coverage obligations, review dimensions, and lifecycle boundaries.
  3. Confirm representative behavior parity exists for all three skills.
  4. Confirm no parity item is classified as unresolved regression.
  5. Confirm representative outputs contain no unfilled placeholders.
- Expected result: preservation and parity evidence prove behavior did not regress.
- Failure proves: the structural extraction is not reviewable or changed behavior.
- Automation location: manual evidence under `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/`.

### T7. Generated skill mirror and temporary adapter proof

- Covers: `SFA-R1`, `SFA-R32` through `SFA-R37`, `AC-SFA-009` through `AC-SFA-011`, `E3`, `EC3`, `EC4`
- Level: integration
- Fixture/setup: canonical `skills/`, generated skill mirrors, temporary adapter output directory, current repository version.
- Steps:
  1. Run generated skill mirror check.
  2. Build adapter packages into a temporary directory using the current version.
  3. Validate adapters against the temporary generated output.
  4. Inspect generated output evidence to confirm every mapped asset is present.
  5. Confirm no generated skill body or asset is hand-edited.
  6. If tracked-tree adapter proof is unsupported or stale, confirm the deferral is explicit and separate from temporary archive proof.
- Expected result: generated mirrors and temporary adapter packages include every mapped asset, adapter validation passes, and any tracked-tree debt is separately justified.
- Failure proves: assets may not ship to installed users.
- Automation location: `python scripts/build-skills.py --check`; `python scripts/build-adapters.py --version <version> --output-dir <tmpdir>`; `python scripts/validate-adapters.py --root <tmpdir> --version <version>`.

### T8. Token-cost, cold-read, and placeholder closeout

- Covers: `SFA-R38` through `SFA-R41`, `AC-SFA-012`, `AC-SFA-013`, `EC5`, `EC6`
- Level: manual
- Fixture/setup: token measurement output, installed-skill or generated-output cold-read evidence, representative outputs.
- Steps:
  1. Measure common-path `SKILL.md` body size separately from total packaged footprint.
  2. Record decrease or justified exception for each touched skill.
  3. Cold-read installed skill output and confirm resource-map entries explain when to use each asset.
  4. Confirm no representative final output contains unfilled placeholders.
- Expected result: token-cost benefit is measured honestly and installed skill output remains understandable.
- Failure proves: the change overstates value or creates unusable asset guidance.
- Automation location: `python scripts/measure-skill-tokens.py`; manual cold-read evidence under the change root.

### T9. Lifecycle state and implementation gate

- Covers: `SFA-R2`, `SFA-R13`, `SFA-R37`, `SFA-R44`, `SFA-R45`
- Level: smoke
- Fixture/setup: proposal, spec, test spec, plan, plan index, change metadata, review log, review resolution.
- Steps:
  1. Confirm proposal status is `accepted`, spec status is `approved`, and this test spec status is `active`.
  2. Confirm the active plan Current Handoff Summary points to implementation only after plan-review and test-spec completion.
  3. Confirm change metadata includes the active test spec and current validation evidence.
  4. Confirm no implementation milestone starts if the proof-route assessment finds a skill-contract gap.
  5. Run lifecycle, review-artifact, change metadata, and whitespace validation.
- Expected result: lifecycle artifacts are synchronized and implementation can start only when required upstream gates are complete.
- Failure proves: downstream work may rely on stale or unsynchronized lifecycle state.
- Automation location: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `python scripts/validate-change-metadata.py docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/change.yaml`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-spec-family-assets-progressive-disclosure`; `git diff --check -- ...`.

## Fixtures and data

- Validator fixtures for valid and invalid spec-family asset layouts.
- Existing plan-asset fixtures may be used as structural references, but spec-family fixtures must have their own expected paths and review-class constraints.
- PR #79 baseline evidence under `docs/changes/2026-05-20-spec-family-readability-pass/`.
- Change-local baseline summary under `docs/changes/2026-05-20-spec-family-assets-progressive-disclosure/baseline.md`.
- Temporary adapter output directory for generated archive proof.

## Mocking/stubbing policy

- Do not mock canonical skill files for final validation; use real `skills/` paths.
- Unit tests may use validator fixtures to exercise invalid shapes.
- Adapter packaging proof must use temporary generated output rather than hand-created asset trees.
- Token and cold-read evidence may be recorded manually, but must cite the exact command output or inspected generated output.

## Migration or compatibility tests

No data migration is in scope.

Compatibility is verified by `T6`, `T7`, `T8`, and `T9`: behavior parity preserves PR #79 behavior, generated output proves packaged assets ship, token/cold-read proof preserves installed-skill usability, and lifecycle checks keep public workflow state synchronized.

## Observability verification

Observability is verified through the durable proof surfaces named in the plan:

- baseline summary;
- preservation matrices;
- behavior-parity evidence;
- generated mirror proof;
- temporary adapter proof;
- token-cost evidence;
- cold-read evidence;
- review records;
- change metadata;
- final verify report.

## Security/privacy verification

No secrets or private data are introduced. Verification checks:

- assets do not require repository-root internal paths as customer-project dependencies;
- generated output is derived from canonical sources and not hand-edited;
- no adapter install-root, lockfile, CLI, or release archive trust-boundary behavior changes are included.

Covered by `T2`, `T7`, and `T9`.

## Performance checks

No runtime performance checks are applicable.

Token-cost checks are required as product/performance-adjacent evidence for installed skill usability and are covered by `T8`.

## Manual QA checklist

- Confirm each skill's `Resource map` can be understood without reading repository-maintainer docs.
- Confirm `spec-review` assets contain no review policy or examples.
- Confirm full skeleton assets for `spec` and `test-spec` do not cause required sections to disappear from common-path expectations.
- Confirm behavior-parity evidence names no unresolved regression.
- Confirm temporary adapter output includes every mapped asset.

## What not to test and why

- Do not test packaged `references/` or packaged `scripts/`; they are out of scope.
- Do not test build-time partials or include syntax; out of scope.
- Do not test produced spec/test-spec artifact readability improvements; output behavior must be preserved.
- Do not test adapter install-root, lockfile, CLI, or release archive migration behavior; unchanged.
- Do not rely on broad natural-language scoring to decide whether an asset hides rules; use deterministic checks, declared bounded heuristics, and code-review judgment.

## Uncovered gaps

None.

## Next artifacts

```text
implement M1
code-review M1
review-resolution M1 if triggered
implement M2
code-review M2
review-resolution M2 if triggered
implement M3
code-review M3
review-resolution M3 if triggered
implement M4
code-review M4
review-resolution M4 if triggered
implement M5
code-review M5
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for the first execution milestone. The active plan owns downstream milestone handoff state.
