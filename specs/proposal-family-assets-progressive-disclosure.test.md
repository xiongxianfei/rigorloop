# Proposal-Family Assets Progressive Disclosure Test Spec

## Status

active

Owner approved on 2026-05-20 after clean `plan-review` round 1.

This test spec is the active proof surface for implementing the approved [Proposal-Family Assets Progressive Disclosure](proposal-family-assets-progressive-disclosure.md) spec.

## Related spec and plan

- Spec: [Proposal-Family Assets Progressive Disclosure](proposal-family-assets-progressive-disclosure.md)
- Plan: [Proposal-Family Assets Progressive Disclosure Plan](../docs/plans/2026-05-20-proposal-family-assets-progressive-disclosure.md)
- Architecture/ADRs: not applicable; the approved plan records no separate architecture package because the change stays inside skill text, assets, validators, generated-output proof, and lifecycle evidence.

## Testing strategy

This is an assets-only skill packaging and preservation change for `proposal` and `proposal-review`. The proof combines deterministic static validation, manual baseline and preservation review, generated-output proof, token-cost evidence with P, cold-read proof, and lifecycle artifact validation.

| Level | Use in this change |
| --- | --- |
| unit | Add or update validator fixture tests for proposal-family asset inventory, resource maps, `COPY`, metadata, placeholders, proposal-review structural labels, forbidden policy labels, and baseline-summary presence. |
| integration | Run full skill validation, focused skill validation, generated skill mirror checks, temporary adapter generation, and adapter validation. |
| smoke | Run lifecycle, review-artifact, and whitespace checks for changed artifacts and handoff state. |
| manual | Inspect the pinned baseline, preservation matrices, behavior parity, token-cost P evidence, cold-read evidence, representative no-placeholder output, and no-hand-edit proof. |
| contract | Confirm every `PFA-R*`, example, edge case, and acceptance criterion is mapped to proof before implementation closeout. |
| migration | Not applicable; no data, CLI, adapter-root, lockfile, or release archive migration is in scope. |

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `PFA-R1` | `T2`, `T4`, `T5`, `T6` | integration | Asset directories are limited to `proposal` and `proposal-review` and checked in generated output. |
| `PFA-R2` | `T2`, `T8` | unit | Validator and lifecycle checks block references, scripts, partials, install-root, lockfile, CLI, and unrelated skill asset changes. |
| `PFA-R3` | `T2`, `T4`, `T5`, `T3` | unit | Assets and preservation evidence prove copy-and-fill structure only. |
| `PFA-R4` | `T2`, `T4`, `T5` | manual | Trivial one-line row assets are blocked or rejected in review. |
| `PFA-R5` | `T4`, `T3` | manual | `proposal` rules, enums, gates, and handoff stay in `SKILL.md`. |
| `PFA-R6` | `T5`, `T3` | manual | `proposal-review` rules, dimensions, statuses, recording, and handoff stay in `SKILL.md`. |
| `PFA-R7` | `T4`, `T3` | manual | `proposal` full skeleton asset or fallback is proven. |
| `PFA-R8` | `T2`, `T4` | unit | `proposal` asset inventory is exactly scoped unless a plan exception exists. |
| `PFA-R9` | `T2`, `T4` | unit | Row-only `proposal` assets are rejected. |
| `PFA-R10` | `T2`, `T5` | unit | `proposal-review` asset inventory is exactly two approved assets. |
| `PFA-R11` | `T2`, `T5` | unit | Review-dimension and review-judgment assets are rejected. |
| `PFA-R12` | `T2`, `T4`, `T5` | unit | Each touched `SKILL.md` has a resource map naming every asset. |
| `PFA-R13` | `T2`, `T4`, `T5` | unit | Resource-map entries use `COPY`, trigger conditions, fill fields, and no-placeholder guidance. |
| `PFA-R14` | `T4`, `T5` | manual | Full skeleton assets have compact output expectation summaries in `SKILL.md`. |
| `PFA-R15` | `T4`, `T5` | manual | Full skeletons are not duplicated in both `SKILL.md` and assets. |
| `PFA-R16` | `T4`, `T3` | manual | Inline fallback is recorded if code review rejects the full proposal skeleton asset. |
| `PFA-R17` | `T4`, `T3` | manual | Conditional proposal sections stay trigger-based after extraction. |
| `PFA-R18` | `T4`, `T2` | unit | Conditional blocks are clearly labeled, or `SKILL.md` instructs trigger-based insertion. |
| `PFA-R19` | `T4`, `T3` | manual | `Initial intent preservation` trigger behavior is preserved. |
| `PFA-R20` | `T4`, `T3` | manual | `Scope budget` trigger behavior is preserved. |
| `PFA-R21` | `T4`, `T2` | unit | Conditional sections are not made universal required sections. |
| `PFA-R22` | `T4`, `T3` | manual | Triggered conditional sections remain available when applicable. |
| `PFA-R23` | `T2`, `T5` | unit | `proposal-review` assets are limited to headings, labels, placeholders, and short fill hints. |
| `PFA-R24` | `T2`, `T5` | unit | Review policy, rules, examples, dimensions, and guidance are blocked from review assets. |
| `PFA-R25` | `T2`, `T5` | unit | Review-class validation uses structural-label allowlist and forbidden-label checks. |
| `PFA-R26` | `T2`, `T5` | unit | Allowed labels are limited to fields needed by approved review assets. |
| `PFA-R27` | `T2`, `T5` | unit | Required allowed structural labels pass when present. |
| `PFA-R28` | `T2`, `T5` | unit | Required forbidden review-policy labels fail when present. |
| `PFA-R29` | `T2`, `T4`, `T5` | unit | Asset metadata comments are validated. |
| `PFA-R30` | `T2`, `T4`, `T5` | unit | Only `normative` or `optional` asset statuses are accepted. |
| `PFA-R31` | `T2`, `T4`, `T5` | unit | Visible placeholder forms are required. |
| `PFA-R32` | `T2`, `T4`, `T5` | unit | Empty required fields and filler placeholder text are blocked. |
| `PFA-R33` | `T1`, `T3`, `T8` | manual | Baseline summary exists before skill text changes. |
| `PFA-R34` | `T1`, `T3` | manual | Baseline summary contains required pinned source and extraction details. |
| `PFA-R35` | `T1`, `T3` | manual | Baseline summary defines the behavior baseline for review. |
| `PFA-R36` | `T3`, `T4`, `T5` | manual | Preservation matrices exist for every extracted structure. |
| `PFA-R37` | `T3`, `T4`, `T5` | manual | Preservation proof covers fields, obligations, enums, dimensions, statuses, scope, recording, and handoff. |
| `PFA-R38` | `T3`, `T4`, `T5` | manual | Representative behavior parity is recorded for both skills. |
| `PFA-R39` | `T3`, `T7` | manual | Representative final outputs contain no unfilled placeholders. |
| `PFA-R40` | `T6` | integration | Generated skill mirrors include every mapped proposal-family asset. |
| `PFA-R41` | `T6` | integration | Temporary generated adapter packages include every mapped asset. |
| `PFA-R42` | `T6` | integration | Adapter validation runs against temporary output or records a blocker. |
| `PFA-R43` | `T6` | manual | Tracked-tree adapter proof runs when supported. |
| `PFA-R44` | `T6` | manual | Tracked-tree debt deferral is explicit and does not replace temporary proof. |
| `PFA-R45` | `T6`, `T8` | manual | Generated adapter bodies and assets are not hand-edited. |
| `PFA-R46` | `T7` | manual | Token evidence separates common-path body size from total packaged footprint. |
| `PFA-R47` | `T7` | manual | Token evidence records P for each proposal-family asset. |
| `PFA-R48` | `T7` | manual | Token evidence acknowledges possible total footprint growth for `proposal-skeleton.md`. |
| `PFA-R49` | `T7` | manual | Common-path decrease or justified exception is recorded for each touched skill. |
| `PFA-R50` | `T7` | manual | Cold-read proof confirms installed output explains asset use. |
| `PFA-R51` | `T2`, `T4`, `T5`, `T6` | unit | Validator or fixture coverage checks all required asset and generated-output constraints. |
| `PFA-R52` | `T2` | unit | Hidden-rule checks use deterministic checks or declared bounded heuristics. |
| `PFA-R53` | `T8` | smoke | This active test spec is present before implementation begins. |
| `PFA-R54` | `T1`, `T8` | manual | Skill-contract gaps stop implementation before skill edits and route to amendment. |
| `PFA-R55` | `T1`, `T8` | manual | Skill-contract sufficiency assessment is recorded before proceeding under this spec and test spec. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T4`, `T3` | Verifies `proposal` full skeleton asset preserves conditional sections. |
| `E2` | `T5`, `T2` | Verifies `proposal-review` assets remain structural and review judgment stays in `SKILL.md`. |
| `E3` | `T2`, `T5` | Verifies allowed labels pass and forbidden policy labels fail. |
| `E4` | `T6` | Verifies generated skill mirrors and temporary adapters include mapped assets. |
| `E5` | `T7` | Verifies common-path, total footprint, and P are recorded with the expected skeleton-asset tradeoff. |

## Edge case coverage

- `EC1`: `T2`, `T4`
- `EC2`: `T3`, `T4`
- `EC3`: `T2`, `T5`
- `EC4`: `T2`, `T5`
- `EC5`: `T2`, `T5`
- `EC6`: `T2`, `T5`
- `EC7`: `T6`
- `EC8`: `T7`
- `EC9`: `T3`, `T4`

## Test cases

### T1. Baseline and proof-route gate

- Covers: `PFA-R33`, `PFA-R34`, `PFA-R35`, `PFA-R54`, `PFA-R55`
- Level: manual
- Fixture/setup: `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`, `specs/skill-contract.md`, `specs/proposal-family-assets-progressive-disclosure.md`, active plan.
- Steps:
  1. Confirm `baseline.md` exists before any edits to `skills/proposal/` or `skills/proposal-review/`.
  2. Confirm it records source commit or branch point, canonical source paths, file or section hashes, existing skeleton section sets, extracted source ranges or headings, repeated substructure fields, conditional sections, closed enums, review dimensions, recording obligations, and asset destinations.
  3. Confirm the plan records whether `specs/skill-contract.md` plus this spec is sufficient for proposal-family full-skeleton assets, review-class restrictions, generated-output presence, and behavior-preservation evidence.
  4. If a gap is found, confirm implementation stops before skill edits and a skill-contract spec amendment packet is created.
- Expected result: baseline identity and proof authority are complete before implementation edits.
- Failure proves: extraction is proceeding without stable behavior identity or contract authority.
- Automation location: manual review plus lifecycle validation where the baseline path is included.

### T2. Proposal-family validator and fixture coverage

- Covers: `PFA-R1` through `PFA-R4`, `PFA-R8` through `PFA-R13`, `PFA-R18`, `PFA-R21`, `PFA-R23` through `PFA-R32`, `PFA-R51`, `PFA-R52`, `AC-PFA-001` through `AC-PFA-006`, `AC-PFA-016`, `AC-PFA-017`, `E2`, `E3`, `EC1`, `EC3`, `EC4`, `EC5`, `EC6`
- Level: unit
- Fixture/setup: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, valid and invalid proposal-family asset fixtures.
- Steps:
  1. Add positive fixtures for `proposal` with only `assets/proposal-skeleton.md`.
  2. Add positive fixtures for `proposal-review` with only `assets/review-result-skeleton.md` and `assets/material-finding.md`.
  3. Add negative fixtures for unmapped assets, non-`COPY` resource verbs, missing fill fields, missing no-placeholder guidance, missing metadata, invalid statuses, missing visible placeholders, filler placeholder content, repository-root dependency requirements, `references/`, `scripts/`, extra assets, row-only `proposal` assets, review-dimension assets, and review-judgment assets.
  4. Add positive `proposal-review` label fixtures for `Recording status`, `Severity`, and the complete allowed structural-label list from `PFA-R27`.
  5. Add negative `proposal-review` label fixtures for `Severity policy`, `Material-finding sufficiency`, `Safe-resolution decision rule`, `Recording-status rules`, `Scope-preservation rules`, `Scope-budget review`, `Vision fit review`, `Standing artifact gate review`, and `Review dimension guidance`.
  6. Run the validator unit suite.
- Expected result: valid proposal-family fixtures pass, invalid fixtures fail for stable and specific reasons, and hidden-rule checks are deterministic or declared bounded heuristics.
- Failure proves: proposal-family asset enforcement is missing, too weak, or too broad.
- Automation location: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### T3. Preservation matrices and behavior-parity evidence

- Covers: `PFA-R3`, `PFA-R5` through `PFA-R7`, `PFA-R16` through `PFA-R20`, `PFA-R22`, `PFA-R33` through `PFA-R39`, `AC-PFA-008`, `AC-PFA-009`, `AC-PFA-015`, `E1`, `EC2`, `EC9`
- Level: manual
- Fixture/setup: baseline summary, preservation matrices, representative behavior-parity evidence, representative outputs.
- Steps:
  1. Confirm every extracted full skeleton or repeated substructure has a source-to-asset preservation row.
  2. Confirm `proposal` preservation covers the full skeleton section set plus `Initial intent preservation` and `Scope budget` as trigger-based conditional sections.
  3. Confirm `proposal-review` preservation covers review result fields and material-finding fields.
  4. Confirm proof names the rules, enums, review dimensions, status values, recording obligations, scope behavior, and handoff behavior that remain in `SKILL.md`.
  5. Confirm representative behavior parity exists for `proposal` and `proposal-review` against the pinned baseline.
  6. Confirm representative final outputs contain no unfilled asset placeholders.
- Expected result: preservation and parity evidence prove extraction did not change behavior.
- Failure proves: structural extraction is not reviewable or has changed user-visible skill behavior.
- Automation location: manual evidence under `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/`.

### T4. `proposal` skeleton asset extraction

- Covers: `PFA-R1`, `PFA-R3` through `PFA-R5`, `PFA-R7` through `PFA-R22`, `PFA-R29` through `PFA-R39`, `AC-PFA-001`, `AC-PFA-003` through `AC-PFA-005`, `AC-PFA-007`, `AC-PFA-017`, `E1`, `EC1`, `EC2`, `EC9`
- Level: manual
- Fixture/setup: baseline summary, edited `skills/proposal/SKILL.md`, `skills/proposal/assets/proposal-skeleton.md`, preservation matrix, behavior-parity evidence.
- Steps:
  1. Confirm only `assets/proposal-skeleton.md` exists under `skills/proposal/assets/`.
  2. Confirm `SKILL.md` retains routing, evidence access, artifact placement, required section guidance, proposal status values, Vision fit values and rules, standing artifact gates, scope preservation, scope-budget rules, decision-quality checks, workflow handoff, and output obligations.
  3. Confirm the `Resource map` uses `COPY`, names the asset, states when to copy it, names fill structures, and forbids unfilled placeholders.
  4. Confirm `SKILL.md` has a compact output expectation summary and does not duplicate the full skeleton.
  5. Confirm the asset preserves `Initial intent preservation` and `Scope budget` as trigger-based sections, either through clearly labeled conditional blocks or `SKILL.md` trigger instructions.
  6. Confirm initial intent, scope budget, decision log, risk rows, and similar row-only structures remain inline.
  7. If code review rejects the full skeleton asset, confirm the full skeleton is re-inlined and the fallback is recorded in behavior-preservation evidence.
- Expected result: `proposal` ships one mapped skeleton asset while preserving behavior and conditional section triggers.
- Failure proves: the constructive skill asset extraction hid contract surface or changed proposal output obligations.
- Automation location: `python scripts/validate-skills.py skills/proposal/SKILL.md`; validator fixtures from `T2`; preservation evidence under the change root.

### T5. `proposal-review` structural asset extraction

- Covers: `PFA-R1`, `PFA-R3`, `PFA-R4`, `PFA-R6`, `PFA-R10` through `PFA-R13`, `PFA-R23` through `PFA-R39`, `PFA-R51`, `PFA-R52`, `AC-PFA-002` through `AC-PFA-006`, `AC-PFA-008`, `AC-PFA-009`, `AC-PFA-016`, `E2`, `E3`, `EC3`, `EC4`, `EC5`, `EC6`
- Level: manual
- Fixture/setup: baseline summary, edited `skills/proposal-review/SKILL.md`, `skills/proposal-review/assets/review-result-skeleton.md`, `skills/proposal-review/assets/material-finding.md`, preservation matrix, behavior-parity evidence.
- Steps:
  1. Confirm only `review-result-skeleton.md` and `material-finding.md` exist under `skills/proposal-review/assets/`.
  2. Confirm no review-dimension row asset, full review-dimensions asset, review-policy asset, or review-judgment asset exists.
  3. Confirm `SKILL.md` retains routing, evidence access, artifact placement, review dimensions, result values, Vision fit review rules, vision-conflict outcomes, standing artifact gate review rules, scope preservation, scope-budget review, material-finding sufficiency, recording statuses, review statuses, isolation and recording rules, and workflow handoff.
  4. Confirm assets contain only headings, allowed field labels, placeholders, and short fill hints.
  5. Confirm forbidden review-policy labels and prose are absent from assets and covered by failing fixtures.
  6. Confirm preservation proof maps review result fields and material-finding fields to the pinned baseline.
- Expected result: `proposal-review` ships only the approved structural assets and keeps review judgment in `SKILL.md`.
- Failure proves: review-class asset boundaries were violated or behavior-preserving field parity was not proven.
- Automation location: `python scripts/validate-skills.py skills/proposal-review/SKILL.md`; validator fixtures from `T2`; preservation evidence under the change root.

### T6. Generated skill mirror and adapter proof

- Covers: `PFA-R1`, `PFA-R40` through `PFA-R45`, `PFA-R51`, `AC-PFA-010` through `AC-PFA-012`, `E4`, `EC7`
- Level: integration
- Fixture/setup: canonical `skills/`, generated skill mirrors, temporary adapter output directory, repository version `v0.1.5`.
- Steps:
  1. Run generated skill mirror checks.
  2. Build adapter packages into a temporary directory using the repository version.
  3. Validate adapters against the temporary generated output.
  4. Confirm every mapped proposal-family asset exists in generated skill mirrors and temporary adapter packages.
  5. Confirm no generated skill body or asset is hand-edited.
  6. If tracked-tree adapter proof is unsupported or blocked by stale debt, confirm the deferral is explicit and does not replace temporary generated-output proof.
- Expected result: generated mirrors and temporary adapter packages include every mapped asset, adapter validation passes or records a precise blocker, and no generated output is hand-edited.
- Failure proves: assets may not ship to installed users.
- Automation location: `python scripts/build-skills.py --check`; `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir"`; `python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5`.

### T7. Token-cost, P, cold-read, and placeholder closeout

- Covers: `PFA-R39`, `PFA-R46` through `PFA-R50`, `AC-PFA-013`, `AC-PFA-014`, `E5`, `EC8`
- Level: manual
- Fixture/setup: token measurement output, P estimates, generated or installed skill output, representative outputs.
- Steps:
  1. Measure common-path `SKILL.md` body size separately from total packaged footprint.
  2. Record P for `proposal-skeleton.md`, `review-result-skeleton.md`, and `material-finding.md`.
  3. Explicitly record that `proposal-skeleton.md` may increase total packaged footprint while still being justified by common-path readability and maintainability.
  4. Record common-path decrease or justified exception for each touched skill.
  5. Cold-read generated or installed skill output and confirm each resource-map entry explains when to use the asset.
  6. Confirm representative final outputs contain no unfilled placeholders.
- Expected result: token-cost evidence is honest about common-path, total footprint, and P, and installed skill output remains understandable.
- Failure proves: the change overstates value or makes asset usage unclear to installed-skill users.
- Automation location: `python scripts/measure-skill-tokens.py`; manual token, P, cold-read, and no-placeholder evidence under the change root.

### T8. Lifecycle state and implementation gate

- Covers: `PFA-R2`, `PFA-R45`, `PFA-R53`, `PFA-R54`, `PFA-R55`
- Level: smoke
- Fixture/setup: proposal, spec, test spec, plan, plan index, change-local review records, review log, review resolution.
- Steps:
  1. Confirm proposal status is `accepted`, spec status is `approved`, this test spec status is `active`, and plan-review R1 is approved.
  2. Confirm the active plan Current Handoff Summary points to `implement M1` only after this test spec is active.
  3. Confirm no implementation milestone starts if the proof-route assessment finds a skill-contract gap.
  4. Confirm lifecycle and review-artifact validation pass after handoff state changes.
  5. Confirm generated adapter body or asset edits do not appear in the tracked diff.
- Expected result: lifecycle artifacts are synchronized and implementation can start with M1 only after required upstream gates are complete.
- Failure proves: downstream work may rely on stale lifecycle state or bypass the approved proof route.
- Automation location: `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure`; `git diff --check --`.

## Fixtures and data

- Valid proposal-family validator fixtures for the approved asset layouts.
- Invalid validator fixtures for unmapped assets, non-`COPY` resource entries, missing metadata, invalid statuses, placeholder violations, repository-root dependencies, extra assets, row-only proposal assets, review-dimension assets, and review-policy labels.
- Change-local baseline summary under `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/baseline.md`.
- Preservation and behavior-parity evidence under `docs/changes/2026-05-20-proposal-family-assets-progressive-disclosure/`.
- Temporary adapter output directory for generated archive proof.
- Token measurement output and P estimates for each proposal-family asset.

## Mocking/stubbing policy

- Do not mock canonical skill files for final validation; use real `skills/` paths.
- Unit tests may use validator fixtures to exercise valid and invalid shapes.
- Generated-output proof must use generated skill mirrors and temporary adapter output, not hand-created adapter trees.
- Token, P, cold-read, preservation, and behavior-parity evidence may be recorded manually, but must cite exact inspected files, command output, source hashes, or generated output.

## Migration or compatibility tests

No data migration is in scope.

Compatibility is verified by `T3`, `T4`, `T5`, `T6`, `T7`, and `T8`: behavior parity preserves the pinned baseline, generated output proves packaged assets ship, token and cold-read proof preserves installed-skill usability, and lifecycle checks keep public workflow state synchronized.

## Observability verification

Observability is verified through durable proof surfaces named in the plan:

- baseline summary;
- preservation matrices;
- behavior-parity evidence;
- generated mirror proof;
- temporary adapter proof;
- token-cost evidence with P;
- cold-read evidence;
- review records;
- final verify report.

No runtime logging, metrics, tracing, or audit event behavior is introduced.

## Security/privacy verification

No secrets or private data are introduced. Verification checks:

- assets do not require repository-root internal paths as customer-project dependencies;
- generated output is derived from canonical sources and not hand-edited;
- no adapter install-root, lockfile, CLI, or release archive trust-boundary behavior changes are included.

Covered by `T2`, `T6`, and `T8`.

## Performance checks

No runtime performance checks are applicable.

Token-cost checks are required as product and usability evidence for installed skills and are covered by `T7`.

## Manual QA checklist

- Confirm `proposal` resource-map guidance can be understood without reading repository-maintainer docs.
- Confirm `proposal-review` assets contain no review policy, rule definitions, or examples.
- Confirm `Initial intent preservation` and `Scope budget` remain trigger-based, not universal required sections.
- Confirm behavior-parity evidence names no unresolved regression.
- Confirm temporary adapter output includes every mapped proposal-family asset.
- Confirm token evidence records common-path size, total packaged footprint, and P separately.

## What not to test and why

- Do not test packaged `references/` or packaged `scripts/`; they are out of scope and should be blocked if introduced.
- Do not test build-time partials or include syntax; out of scope.
- Do not test assets for `spec`, `spec-review`, `test-spec`, `plan`, `code-review`, `verify`, or `pr`; out of scope for this initiative except as prior-art references.
- Do not test proposal or proposal-review routing changes; routing behavior must remain unchanged.
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
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Active proof surface for the first execution milestone. The active plan owns downstream milestone handoff state.
