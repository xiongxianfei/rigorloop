# Review-Skill Family Consistency and Parser-Owned Finding Shape Test Spec

## Status

active

Owner approved on 2026-05-21 after clean `plan-review` round 1.

This test spec is the active proof surface for implementing the approved [Review-Skill Family Consistency and Parser-Owned Finding Shape](review-skill-family-consistency-parser-owned-finding-shape.md) spec.

## Related spec and plan

- Spec: [Review-Skill Family Consistency and Parser-Owned Finding Shape](review-skill-family-consistency-parser-owned-finding-shape.md)
- Plan: [Review-Skill Family Consistency and Parser-Owned Finding Shape Plan](../docs/plans/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md)
- Architecture/ADRs: not applicable; the approved plan records no separate architecture package because the change stays inside skill text, assets, deterministic validators/fixtures, generated-output proof, and lifecycle evidence.

## Testing strategy

This is a review-skill asset packaging, parser-conformance, and behavior-preservation change. The proof combines deterministic static validation, review-artifact parser fixtures, manual preservation/parity evidence, generated-output proof, token-cost evidence, cold-read proof, and lifecycle artifact validation.

| Level | Use in this change |
| --- | --- |
| unit | Add or update validator fixture tests for first-slice asset inventory, resource maps, `COPY`, metadata, placeholders, review-class asset boundaries, parser-owned field labels, byte-identical material-finding blocks, invalid `Finding ID:` identity fills, and no severity-enum validation requirement. |
| integration | Run full skill validation, review-artifact structure validation, generated skill mirror checks, temporary adapter generation, and adapter validation. |
| smoke | Run lifecycle, change metadata, review-artifact closeout, and whitespace checks for changed artifacts and handoff state. |
| manual | Inspect skill-contract sufficiency, source-to-asset preservation matrices, representative behavior parity, token-cost evidence, cold-read evidence, generated-output no-hand-edit proof, and follow-on trigger notes. |
| contract | Confirm every `RSF-R*`, example, edge case, and acceptance criterion is mapped to proof before implementation closeout. |
| migration | Not applicable; no data, CLI, adapter-root, lockfile, or release archive migration is in scope. Existing historical adapter archives are not rewritten. |

## Requirement coverage map

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `RSF-R1` | `T2`, `T5`, `T6`, `T7`, `T9` | integration | Limits review-family assets to `code-review`, `proposal-review`, and `spec-review`. |
| `RSF-R2` | `T2`, `T11` | unit | Deferred review skills must remain unchanged unless the spec is amended. |
| `RSF-R3` | `T2`, `T11` | unit | Blocks references, scripts, partials, adapter-root, lockfile, CLI, and unrelated asset changes. |
| `RSF-R4` | `T2`, `T5`, `T6`, `T7` | unit | Each first-slice skill has exactly `material-finding.md` and `review-result-skeleton.md` as review-family assets. |
| `RSF-R5` | `T2`, `T5`, `T6`, `T7`, `T8` | unit | Assets remain copy-and-fill structural templates only. |
| `RSF-R6` | `T2`, `T5`, `T6`, `T7` | unit | Assets contain only headings, field labels, placeholders, and short fill hints. |
| `RSF-R7` | `T2`, `T5`, `T6`, `T7` | unit | Review-policy leakage into assets is rejected. |
| `RSF-R8` | `T5`, `T6`, `T7`, `T8` | manual | Review judgment, rules, enums, and handoff behavior stay in `SKILL.md`. |
| `RSF-R9` | `T2`, `T5`, `T6`, `T7` | unit | Each first-slice `SKILL.md` has a resource map for every asset. |
| `RSF-R10` | `T2`, `T5`, `T6`, `T7` | unit | Resource-map entries use `COPY`, copy conditions, fill fields, and no-placeholder guidance. |
| `RSF-R11` | `T2`, `T5`, `T6`, `T7` | unit | Material-finding resource maps include literal `Finding ID:` confirmation before linking. |
| `RSF-R12` | `T2`, `T5`, `T6`, `T7` | unit | Required metadata comments are validated. |
| `RSF-R13` | `T2`, `T5`, `T6`, `T7` | unit | Review-family assets use `normative` status. |
| `RSF-R14` | `T2`, `T5`, `T6`, `T7` | unit | Placeholders use visible forms. |
| `RSF-R15` | `T2`, `T5`, `T6`, `T7` | unit | Empty required fields and filler placeholder content are rejected. |
| `RSF-R16` | `T3`, `T5`, `T6`, `T7` | unit | `material-finding.md` labels match accepted parser-owned labels and accepted `needs-decision rationale:` variant where applicable. |
| `RSF-R17` | `T3` | unit | Material-finding labels match the existing parser contract without parser-contract changes. |
| `RSF-R18` | `T3`, `T5`, `T6`, `T7` | unit | Parser-owned material-finding field blocks are byte-identical across first-slice skills unless harmless non-parser variation is recorded. |
| `RSF-R19` | `T4` | integration | A representative valid finding copied from the asset passes structure validation. |
| `RSF-R20` | `T4` | unit | Parser-owned structure validation is limited to parser-owned fields and shapes. |
| `RSF-R21` | `T4` | unit | Invalid fills cover blank, renamed, or missing `Finding ID:` identity, not non-enum severity. |
| `RSF-R22` | `T5`, `T6`, `T7` | manual | Each result skeleton is skill-specific. |
| `RSF-R23` | `T5`, `T6`, `T7`, `T8` | manual | Each result skeleton preserves source review-status enum verbatim. |
| `RSF-R24` | `T2`, `T5`, `T6`, `T7` | unit | Shared result skeletons and shared result-skeleton bases are rejected. |
| `RSF-R25` | `T5`, `T8` | manual | `code-review` `clean-with-notes` semantics stay distinct from gate-review `approved`. |
| `RSF-R26` | `T5`, `T6`, `T7`, `T8` | manual | Skill-specific result fields are preserved. |
| `RSF-R27` | `T8` | manual | Preservation evidence maps extracted material-finding and result-skeleton fields. |
| `RSF-R28` | `T8` | manual | Preservation evidence covers fields, obligations, enums, rules, stops, lifecycle boundaries, and handoff semantics. |
| `RSF-R29` | `T8` | manual | Representative behavior parity is unchanged for all first-slice review skills. |
| `RSF-R30` | `T8`, `T10` | manual | Representative final review outputs contain no unfilled placeholders. |
| `RSF-R31` | `T9` | integration | Generated skill mirrors include every mapped review-family asset. |
| `RSF-R32` | `T9` | integration | Temporary generated adapter packages include every mapped review-family asset. |
| `RSF-R33` | `T9` | integration | Adapter validation runs against temporary output or records a blocker. |
| `RSF-R34` | `T9` | manual | Generated adapter skill bodies and assets are not hand-edited. |
| `RSF-R35` | `T10` | manual | Token evidence reports common-path `SKILL.md` body size separately from total packaged footprint. |
| `RSF-R36` | `T10` | manual | Token evidence records per-skill asset usage expectations or rationale. |
| `RSF-R37` | `T10` | manual | Cold-read proof confirms installed skills plus assets are sufficient to produce a valid material finding. |
| `RSF-R38` | `T2`, `T3`, `T4`, `T9` | unit | Validator/fixture coverage deterministically checks asset, parser, generated-output, and no-hand-edit constraints. |
| `RSF-R39` | `T2` | unit | Review-policy leakage checks use deterministic labels, allowlists, forbidden labels, or declared bounded heuristics. |
| `RSF-R40` | `T1`, `T11` | smoke | Active test spec exists before implementation begins. |
| `RSF-R41` | `T1` | manual | Skill-contract insufficiency stops implementation before skill edits and routes to amendment. |
| `RSF-R42` | `T1` | manual | Skill-contract sufficiency assessment is recorded before proceeding. |
| `RSF-R43` | `T5`, `T6`, `T7` | unit | Resource-map cross-file confirmation instruction is required; referential-integrity validation is deferred. |
| `RSF-R44` | `T11` | manual | Follow-on trigger for referential-integrity validation is recorded. |
| `RSF-R45` | `T11` | manual | Follow-on trigger for build-time partials is recorded. |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T3`, `T4`, `T6` | Verifies copied material-finding labels and valid filled finding structure. |
| `E2` | `T4` | Verifies invalid parser-owned finding identity fills fail while validation remains the backstop. |
| `E3` | `T5`, `T6`, `T7`, `T8` | Verifies per-skill result-status vocabularies remain distinct. |
| `E4` | `T2`, `T11` | Verifies deferred review skills are visible and unchanged. |
| `E5` | `T9` | Verifies generated mirrors and temporary adapters include mapped assets with no hand edits. |

## Edge case coverage

- `EC1`: `T4`
- `EC2`: `T4`
- `EC3`: `T4`
- `EC4`: `T3`, `T8`
- `EC5`: `T2`, `T5`, `T8`
- `EC6`: `T2`, `T11`
- `EC7`: `T9`
- `EC8`: `T8`, `T10`

## Test cases

### T1. Pre-implementation authority and skill-contract sufficiency gate

- Covers: `RSF-R40`, `RSF-R41`, `RSF-R42`, `AC-RSF-019`, `AC-RSF-020`
- Level: manual
- Fixture/setup: `specs/review-skill-family-consistency-parser-owned-finding-shape.md`, this test spec, active plan, `specs/skill-contract.md`, plan-review receipt.
- Steps:
  1. Confirm this test spec is active before implementation starts.
  2. Confirm the active plan records the no-architecture rationale and the M1 stop-or-proceed check for `specs/skill-contract.md` sufficiency.
  3. During M1, confirm the sufficiency assessment is recorded before any skill asset edits.
  4. If the skill contract is insufficient for review-family assets, parser-conformance checks, or generated-output asset presence, confirm implementation stops and a spec amendment packet is created.
- Expected result: implementation begins only with an approved proof surface and recorded contract authority.
- Failure proves: implementation is proceeding without the required lifecycle proof or contract basis.
- Automation location: manual review plus `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.

### T2. Review-family asset inventory, resource-map, metadata, placeholder, and boundary validation

- Covers: `RSF-R1` through `RSF-R15`, `RSF-R24`, `RSF-R38`, `RSF-R39`, `RSF-R43`, `AC-RSF-001` through `AC-RSF-006`, `E4`, `EC5`, `EC6`
- Level: unit
- Fixture/setup: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, valid and invalid review-family skill fixtures.
- Steps:
  1. Add positive fixtures for `code-review`, `proposal-review`, and `spec-review` with exactly `assets/material-finding.md` and `assets/review-result-skeleton.md` as review-family assets.
  2. Add negative fixtures for `plan-review`, `architecture-review`, future `*-review` edits, packaged `references/`, packaged `scripts/`, build-time partials, row-only assets, extra unrelated assets, and shared result skeletons.
  3. Add negative fixtures for missing resource-map entries, non-`COPY` verbs, missing copy conditions, missing fill fields, missing no-placeholder guidance, and missing literal `Finding ID:` confirmation before linking.
  4. Add negative fixtures for missing metadata, non-`normative` status, missing visible placeholders, empty required fields, realistic filler prose, generic filler text, `lorem ipsum`, and `your text here`.
  5. Add positive and negative review-class boundary fixtures using deterministic allowed labels, forbidden labels, and declared bounded heuristics only.
  6. Run the validator unit suite and full skill validation.
- Expected result: valid review-family fixtures pass, invalid fixtures fail for stable and specific reasons, and full skill validation passes after implementation.
- Failure proves: review-family asset contract enforcement is missing, too weak, or too broad.
- Automation location: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### T3. Parser-conformance and byte-identical material-finding field blocks

- Covers: `RSF-R16`, `RSF-R17`, `RSF-R18`, `RSF-R38`, `AC-RSF-007`, `AC-RSF-008`, `E1`, `EC4`
- Level: unit
- Fixture/setup: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, `scripts/review_artifact_validation.py`, implemented `assets/material-finding.md` files.
- Steps:
  1. Extract the material-finding labels parsed by the current review-artifact parser without changing parser accepted-label behavior.
  2. Confirm each first-slice `assets/material-finding.md` contains exactly the parser-owned labels: `Finding ID:`, `Severity:`, `Location:`, `Evidence:`, `Required outcome:`, `Safe resolution path:`, plus accepted `needs-decision rationale:` where applicable.
  3. Confirm the parser-owned field block is byte-identical across `code-review`, `proposal-review`, and `spec-review`.
  4. If harmless non-parser variation exists outside the field block, confirm the plan or preservation evidence records it.
  5. Add a negative fixture where one label is renamed, reordered, removed, or added beyond the parser contract.
- Expected result: material-finding asset field blocks remain bound to the existing parser contract and to each other.
- Failure proves: the copied material-finding asset has become a new drift surface.
- Automation location: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`.

### T4. Review-artifact parser valid and invalid material-finding fills

- Covers: `RSF-R19`, `RSF-R20`, `RSF-R21`, `RSF-R38`, `AC-RSF-009`, `AC-RSF-010`, `E1`, `E2`, `EC1`, `EC2`, `EC3`
- Level: unit
- Fixture/setup: review-artifact validator fixtures under `scripts/test-review-artifact-validator.py` or equivalent review-artifact fixture paths.
- Steps:
  1. Build a representative detailed review record by copying `assets/material-finding.md` and filling accepted values.
  2. Confirm `python scripts/validate-review-artifacts.py --mode structure <fixture-change-root>` passes for the valid filled finding.
  3. Add invalid fixtures for blank `Finding ID:`, renamed `Finding ID:` such as `Finding:`, and a material-finding block missing parser-owned finding identity.
  4. Confirm invalid parser-owned identity fixtures fail structure validation for the expected reason.
  5. Confirm tests do not require non-enum `Severity:` values to fail structure validation.
- Expected result: the asset starts from the valid parser-owned shape, malformed parser-owned identity fills fail, and severity-enum validation is not introduced.
- Failure proves: the parser/asset proof either misses the learn-session failure mode or silently expands parser behavior.
- Automation location: `python scripts/test-review-artifact-validator.py`; `python scripts/validate-review-artifacts.py --mode structure <fixture-change-root>`.

### T5. `code-review` asset extraction and status preservation

- Covers: `RSF-R1`, `RSF-R4` through `RSF-R30`, `RSF-R43`, `AC-RSF-001` through `AC-RSF-013`, `E3`, `EC5`
- Level: manual
- Fixture/setup: edited `skills/code-review/SKILL.md`, `skills/code-review/assets/material-finding.md`, `skills/code-review/assets/review-result-skeleton.md`, preservation matrix, representative parity evidence.
- Steps:
  1. Confirm `code-review` has exactly the two review-family assets.
  2. Confirm `SKILL.md` retains review dimensions, evidence rules, severity enum and meanings, recording rules, isolation rules, stop conditions, milestone handoff behavior, and artifact-placement behavior.
  3. Confirm the resource map uses `COPY` and includes the literal `Finding ID:` confirmation before linking.
  4. Confirm `review-result-skeleton.md` preserves `clean-with-notes | changes-requested | blocked | inconclusive` verbatim and preserves milestone-specific result fields.
  5. Confirm preservation evidence maps each extracted finding/result field and records unchanged behavior.
  6. Confirm representative behavior parity reaches the same verdicts, findings, recording outcomes, and handoff statements as before extraction.
- Expected result: `code-review` gains structural assets without changing review behavior or status vocabulary.
- Failure proves: asset extraction changed or hid the code-review contract.
- Automation location: `python scripts/validate-skills.py`; preservation and parity evidence under the change root.

### T6. `proposal-review` asset conformance

- Covers: `RSF-R1`, `RSF-R4` through `RSF-R30`, `RSF-R43`, `AC-RSF-001` through `AC-RSF-013`, `E1`, `E3`
- Level: manual
- Fixture/setup: edited `skills/proposal-review/SKILL.md`, existing `skills/proposal-review/assets/material-finding.md`, existing `skills/proposal-review/assets/review-result-skeleton.md`, preservation matrix, representative parity evidence.
- Steps:
  1. Confirm existing `proposal-review` assets are conformed rather than duplicated.
  2. Confirm `SKILL.md` retains review dimensions, Vision fit review, standing artifact gate review, scope preservation, severity enum, review-status enum, recording rules, isolation rules, stop conditions, handoff behavior, and artifact placement.
  3. Confirm `review-result-skeleton.md` preserves `approved | changes-requested | blocked | inconclusive` verbatim and proposal-review-specific result fields.
  4. Confirm `material-finding.md` matches the parser-owned field block and is byte-identical to the other first-slice copies for that block.
  5. Confirm preservation and representative behavior-parity evidence are recorded.
- Expected result: `proposal-review` satisfies the review-family contract without regressing the proposal-family assets contract.
- Failure proves: conformance introduced drift or behavior change in an already asset-enabled review skill.
- Automation location: `python scripts/validate-skills.py`; preservation and parity evidence under the change root.

### T7. `spec-review` asset conformance and material-finding rename

- Covers: `RSF-R1`, `RSF-R4` through `RSF-R30`, `RSF-R43`, `AC-RSF-001` through `AC-RSF-013`, `E3`
- Level: manual
- Fixture/setup: edited `skills/spec-review/SKILL.md`, `skills/spec-review/assets/material-finding.md`, `skills/spec-review/assets/review-result-skeleton.md`, removed or intentionally handled `skills/spec-review/assets/review-finding.md`, preservation matrix, representative parity evidence.
- Steps:
  1. Confirm `spec-review` uses `assets/material-finding.md` in the resource map and output guidance.
  2. Confirm `assets/review-finding.md` is removed or is not a review-family asset only if an approved fallback records why it remains.
  3. Confirm `SKILL.md` retains review dimensions, severity enum, review-status enum, eventual test-spec readiness behavior, recording rules, isolation rules, stop conditions, downstream settlement guidance, handoff behavior, and artifact placement.
  4. Confirm `review-result-skeleton.md` preserves `approved | changes-requested | blocked | inconclusive` verbatim and spec-review-specific readiness fields.
  5. Confirm no stale references to `review-finding.md` remain unless the approved fallback explicitly requires them.
  6. Confirm preservation and representative behavior-parity evidence are recorded.
- Expected result: `spec-review` adopts the approved material-finding asset name and preserves spec-review behavior.
- Failure proves: rename/conformance left stale references or changed downstream readiness behavior.
- Automation location: `python scripts/validate-skills.py`; preservation and parity evidence under the change root.

### T8. Preservation matrices, behavior parity, and no-placeholder outputs

- Covers: `RSF-R8`, `RSF-R22` through `RSF-R30`, `AC-RSF-011` through `AC-RSF-013`, `E3`, `EC4`, `EC5`, `EC8`
- Level: manual
- Fixture/setup: behavior-preservation evidence, representative behavior-parity evidence, representative final review outputs for all first-slice review skills.
- Steps:
  1. Confirm preservation matrices map each source finding field and result-skeleton field to its asset field.
  2. Confirm preservation proof explicitly covers field names, field obligations, severity values, review-status values, review dimensions, recording status values, recording rules, isolation rules, stop conditions, lifecycle boundaries, and handoff semantics.
  3. Confirm representative parity evidence for all three review skills shows unchanged verdicts, material findings, recording outcomes, and handoff statements.
  4. Confirm representative final review outputs contain no unfilled placeholders.
  5. Confirm any harmless non-parser material-finding variation is recorded or removed.
- Expected result: structural extraction is demonstrably behavior-preserving.
- Failure proves: the implementation changed review behavior or lacks enough evidence for review.
- Automation location: manual evidence under `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/`.

### T9. Generated skill mirror, temporary adapter, and no-hand-edit proof

- Covers: `RSF-R31`, `RSF-R32`, `RSF-R33`, `RSF-R34`, `RSF-R38`, `AC-RSF-014`, `AC-RSF-015`, `AC-RSF-016`, `E5`, `EC7`
- Level: integration
- Fixture/setup: canonical `skills/`, generated skill mirror checks, temporary adapter output directory, repository version.
- Steps:
  1. Run generated skill mirror checks from canonical skill sources.
  2. Build adapter packages into a temporary output directory using the current repository version.
  3. Validate adapters against the temporary output directory.
  4. Confirm every mapped first-slice review-family asset is present in generated skill mirrors and temporary adapter packages.
  5. Confirm no generated skill body or generated adapter asset is hand-edited.
  6. If generated-output or adapter validation is blocked, record the blocker and smallest next action.
- Expected result: installed skill packaging includes the review-family assets and remains derived from canonical sources.
- Failure proves: assets may not ship to users or generated output may have been edited by hand.
- Automation location: `python scripts/build-skills.py --check`; `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version <version> --output-dir "$tmpdir"`; `python scripts/validate-adapters.py --root "$tmpdir" --version <version>`.

### T10. Token-cost, cold-read, and asset-use proof

- Covers: `RSF-R30`, `RSF-R35`, `RSF-R36`, `RSF-R37`, `AC-RSF-017`, `AC-RSF-018`, `EC8`
- Level: manual
- Fixture/setup: token measurement output, generated or installed skill output, packaged assets, cold-read evidence.
- Steps:
  1. Measure common-path `SKILL.md` body size separately from total packaged footprint.
  2. Record per-skill asset usage expectations or rationale for `material-finding.md` and `review-result-skeleton.md`.
  3. Record common-path size changes and total packaged-footprint changes without treating total-footprint growth as a regression by itself.
  4. Cold-read generated or installed skill output plus packaged assets and confirm a reviewer can produce a valid material finding without repository-maintainer context.
  5. Confirm representative outputs contain no unfilled placeholders.
- Expected result: token and cold-read evidence support the spec's common-path readability and parser-shaped finding goals.
- Failure proves: the implementation lacks user-facing usability evidence or misreports token cost.
- Automation location: `python scripts/measure-skill-tokens.py`; manual cold-read evidence under the change root.

### T11. Scope boundaries, follow-on triggers, and lifecycle closeout

- Covers: `RSF-R2`, `RSF-R3`, `RSF-R40`, `RSF-R44`, `RSF-R45`, `AC-RSF-002`, `AC-RSF-019`
- Level: smoke
- Fixture/setup: final diff, active plan, change metadata, review artifacts, follow-on notes.
- Steps:
  1. Confirm `plan-review`, `architecture-review`, and future `*-review` skills are unchanged by this slice.
  2. Confirm no out-of-scope references, scripts, partials, adapter install-root changes, lockfile changes, CLI behavior changes, or retroactive adapter archive rewrites exist in the diff.
  3. Confirm follow-on trigger notes remain for referential-integrity validation and build-time partials.
  4. Confirm lifecycle metadata names this active test spec before implementation begins.
  5. Run lifecycle, change metadata, review-artifact, and whitespace validation.
- Expected result: the final implementation stays inside the first-slice boundary and leaves downstream lifecycle state coherent.
- Failure proves: scope creep or lifecycle drift occurred.
- Automation location: `python scripts/validate-change-metadata.py docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/change.yaml`; `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`; `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`; `git diff --check --`.

## Fixtures and data

- Valid and invalid skill-validator fixtures for first-slice review-family assets.
- Valid and invalid review-artifact validator fixtures for copied material-finding fills.
- Canonical skill sources under `skills/code-review/`, `skills/proposal-review/`, and `skills/spec-review/`.
- Behavior-preservation matrices and representative parity evidence under `docs/changes/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape/`.
- Temporary generated adapter output under a disposable directory created during validation.
- Token measurement output from `python scripts/measure-skill-tokens.py`.
- Cold-read evidence from generated or installed skill output plus packaged assets.

## Mocking/stubbing policy

Use filesystem fixtures and temporary directories rather than mocks for validators, generated mirrors, adapter archives, and review-artifact validation. Mocking is acceptable only for narrow unit helpers that already use in-memory fixture content in `scripts/test-skill-validator.py`; it must not replace end-to-end generated-output or adapter validation.

## Migration or compatibility tests

No data or release-archive migration is in scope. Compatibility proof is covered by `T5` through `T8` for unchanged review behavior, `T9` for generated output from canonical sources, and `T11` for unchanged adapter roots, lockfiles, CLI behavior, deferred review skills, and historical adapter archives.

## Observability verification

No runtime logging, metrics, traces, or audit events are introduced. Observability proof is artifact-level: validator results, preservation evidence, behavior parity, generated-output proof, token/cold-read evidence, lifecycle metadata, and review records.

## Security/privacy verification

Security/privacy verification is limited to static review that assets do not introduce secrets, credentials, private data, external services, machine-local paths, repository-root internal paths as customer-facing requirements, or generated-output hand edits. Covered by `T2`, `T9`, and `T11`.

## Performance checks

No runtime performance behavior is affected. Performance proof is limited to token-cost evidence in `T10`, separating common-path `SKILL.md` body size from total packaged footprint and recording per-skill asset usage expectations.

## Manual QA checklist

- Confirm `code-review`, `proposal-review`, and `spec-review` each explain when to copy `material-finding.md` and `review-result-skeleton.md`.
- Confirm copied `material-finding.md` starts with the parser-owned labels a reviewer needs.
- Confirm `code-review` still uses `clean-with-notes` rather than `approved`.
- Confirm `proposal-review` and `spec-review` still use `approved` as their clean gate-review status.
- Confirm no review guidance or policy moved into assets.
- Confirm representative final outputs have no unfilled placeholders.

## What not to test and why

- Do not test severity-enum validation; this slice explicitly does not add it.
- Do not test referential-integrity validation for Finding IDs across review-log/review-resolution; it is a deferred follow-on trigger, not part of this implementation.
- Do not test build-time partials; they are out of scope.
- Do not test `plan-review`, `architecture-review`, or future `*-review` skill asset extraction; those skills are deferred.
- Do not test adapter install-root, lockfile, CLI, or release archive migration behavior beyond confirming this diff does not change them.
- Do not rely only on snapshots for behavior preservation; use preservation matrices and representative parity evidence.

## Uncovered gaps

None. If M1 discovers `specs/skill-contract.md` is insufficient for this contract, implementation must stop and route to a spec amendment packet before skill edits.

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
review-resolution M5 if triggered
explain-change
verify
pr
```

## Follow-on artifacts

None yet

## Readiness

Active proof surface for the first execution milestone. The active plan owns downstream milestone handoff state.
