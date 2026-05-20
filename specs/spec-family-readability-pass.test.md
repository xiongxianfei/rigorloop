# Spec-Family Readability Pass Test Spec

## Status

active

Owner approved on 2026-05-20.

This test spec is the active proof surface for implementing the approved
[Spec-Family Readability Pass](spec-family-readability-pass.md).

## Related spec and plan

- Spec: [Spec-Family Readability Pass](spec-family-readability-pass.md)
- Plan: [Spec-Family Readability Pass Plan](../docs/plans/2026-05-20-spec-family-readability-pass.md)
- Change root: [docs/changes/2026-05-20-spec-family-readability-pass](../docs/changes/2026-05-20-spec-family-readability-pass/change.yaml)

## Testing strategy

This is a presentation-only Markdown change. The primary proof is deterministic
source-to-destination preservation evidence, not model-output comparison alone.

| Level | Use in this change |
| --- | --- |
| Static contract checks | Validate lifecycle artifacts, change metadata, skill structure, and selected CI paths. |
| Manual source review | Compare every tabulated, fenced, moved, or reordered content block against its source. |
| Manual behavior parity | Run representative skill prompts or dry comparisons and classify differences for each changed skill. |
| Generated-output validation | Validate or explicitly defer current adapter output generated from canonical `skills/`. |
| Cold-read verification | Confirm a reader can locate required sections, enums, boundaries, validation, and handoff surfaces. |

## Requirement coverage map

| Requirement | Tests |
| --- | --- |
| `SFRP-R1` | `T2`, `T6`, `T9`, `T12`, `T14` |
| `SFRP-R2` | `T2`, `T5`, `T6`, `T8`, `T9`, `T11`, `T14` |
| `SFRP-R3` | `T2`, `T6`, `T9`, `T14` |
| `SFRP-R4` | `T12`, `T14` |
| `SFRP-R5` | `T1` |
| `SFRP-R6` | `T1` |
| `SFRP-R7` | `T2`, `T9` |
| `SFRP-R8` | `T6` |
| `SFRP-R9` | `T9` |
| `SFRP-R10` | `T3`, `T7`, `T10` |
| `SFRP-R11` | `T3`, `T7`, `T10` |
| `SFRP-R12` | `T3`, `T7`, `T10` |
| `SFRP-R13` | `T3`, `T7`, `T10` |
| `SFRP-R14` | `T3`, `T7`, `T10` |
| `SFRP-R15` | `T4`, `T10` |
| `SFRP-R16` | `T4`, `T10` |
| `SFRP-R17` | `T4`, `T10` |
| `SFRP-R18` | `T4`, `T10` |
| `SFRP-R19` | `T2`, `T6`, `T9` |
| `SFRP-R20` | `T2`, `T6`, `T9` |
| `SFRP-R21` | `T5`, `T8`, `T11` |
| `SFRP-R22` | `T5`, `T8`, `T11` |
| `SFRP-R23` | `T5`, `T8`, `T11` |
| `SFRP-R24` | `T12` |
| `SFRP-R25` | `T13` |

## Example coverage map

| Example | Tests |
| --- | --- |
| `E1` | `T2` |
| `E2` | `T7` |
| `E3` | `T10` |
| `E4` | `T12` |

## Edge case coverage

| Edge case | Tests |
| --- | --- |
| `EC1` | `T3`, `T7`, `T10` |
| `EC2` | `T4`, `T10` |
| `EC3` | `T9`, `T10` |
| `EC4` | `T2`, `T6`, `T9` |
| `EC5` | `T12` |

## Test cases

T1. Normalized test-spec baseline gate
- Covers: `SFRP-R5`, `SFRP-R6`, `EC3`
- Level: manual
- Fixture/setup: `skills/test-spec/SKILL.md`; normalization evidence under `docs/changes/2026-05-20-test-spec-contract-normalization/`.
- Steps:
  1. Before any readability edit, inspect `skills/test-spec/SKILL.md`.
  2. Confirm front matter includes `version` and `schema-version`.
  3. Confirm `Workflow role`, `Stop conditions`, and fenced `Output skeleton` sections are present.
  4. Confirm normalization behavior-preservation evidence is present or explicitly accepted.
- Expected result: all normalized baseline checks are present; otherwise implementation stops and routes back to normalization.
- Failure proves: readability began from an unstable or non-compliant `test-spec` baseline.
- Automation location: manual evidence in `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md`.

T2. M1 spec required-section table preservation
- Covers: `SFRP-R1`, `SFRP-R2`, `SFRP-R3`, `SFRP-R7`, `SFRP-R19`, `SFRP-R20`, `E1`, `EC4`
- Level: manual
- Fixture/setup: baseline and edited `skills/spec/SKILL.md`.
- Steps:
  1. Identify the baseline required-section prose in `skills/spec/SKILL.md`.
  2. Compare every required section and obligation to the edited table.
  3. Record source location, destination location, change type, and preservation proof.
  4. Confirm no produced spec artifact section or output expectation was added, removed, or redefined.
- Expected result: the table preserves the same section names, applicability, and obligations.
- Failure proves: tabulation changed the spec artifact contract or lost required content.
- Automation location: `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md`.

T3. M1 spec enum authority and duplicate check
- Covers: `SFRP-R10`, `SFRP-R11`, `SFRP-R12`, `SFRP-R13`, `SFRP-R14`, `EC1`
- Level: manual
- Fixture/setup: baseline and edited `skills/spec/SKILL.md`.
- Steps:
  1. Identify closed enum values changed by M1, including settlement-result related values.
  2. Record each enum's existing source, authoritative destination, exact values, and duplicate-handling rule.
  3. Confirm later instructions reference the enum by name or placeholder instead of restating a full duplicate value set.
- Expected result: each changed closed enum has one authoritative value surface with identical values.
- Failure proves: enum fencing added, removed, renamed, or duplicated enum values.
- Automation location: enum authority map in `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md`.

T4. M1 spec section-order behavior clarity
- Covers: `SFRP-R15`, `SFRP-R16`, `SFRP-R17`, `SFRP-R18`, `EC2`
- Level: manual
- Fixture/setup: edited `skills/spec/SKILL.md`; approved family section order in the spec.
- Steps:
  1. Compare edited top-level section order to the family order.
  2. Confirm behavior-significant sections remain visible before normal generation procedure when needed.
  3. Record any exception with skill, section, expected placement, chosen placement, and reason.
- Expected result: section order improves scanability without hiding stop conditions, claim boundaries, validation, or handoff obligations.
- Failure proves: ordering weakened behavior clarity.
- Automation location: content-preservation matrix section-order entries.

T5. M1 spec representative behavior parity
- Covers: `SFRP-R2`, `SFRP-R21`, `SFRP-R22`, `SFRP-R23`
- Level: manual
- Fixture/setup: representative proposal input selected during M1.
- Steps:
  1. Compare expected `spec` output behavior before and after M1.
  2. Check verdict/status settlement, output structure, required-section coverage, and examples or edge-case coverage.
  3. Classify every difference as `equivalent`, `improvement`, or `regression`.
- Expected result: no unresolved `regression` is present.
- Failure proves: the presentation edit caused a material behavior change.
- Automation location: `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`.

T6. M2 spec-review dimension table preservation
- Covers: `SFRP-R1`, `SFRP-R2`, `SFRP-R3`, `SFRP-R8`, `SFRP-R19`, `SFRP-R20`, `EC4`
- Level: manual
- Fixture/setup: baseline and edited `skills/spec-review/SKILL.md`.
- Steps:
  1. Identify baseline review-dimension prose and verdict guidance.
  2. Compare every dimension and guidance point to the edited table.
  3. Record source location, destination location, change type, and preservation proof.
  4. Confirm review output structure and recording obligations are unchanged.
- Expected result: the table preserves the same dimensions and verdict guidance.
- Failure proves: tabulation changed review criteria or review output obligations.
- Automation location: content-preservation matrix.

T7. M2 spec-review verdict enum authority and recording boundary preservation
- Covers: `SFRP-R10`, `SFRP-R11`, `SFRP-R12`, `SFRP-R13`, `SFRP-R14`, `E2`, `EC1`
- Level: manual
- Fixture/setup: baseline and edited `skills/spec-review/SKILL.md`.
- Steps:
  1. Identify review-dimension verdict values and any changed review-status or recording-status closed enums.
  2. Record each enum's existing source, authoritative destination, exact values, and duplicate-handling rule.
  3. Confirm recording boundaries, material-finding shape, and review-result semantics remain unchanged.
- Expected result: verdict and related enum values are preserved once without weakening recording behavior.
- Failure proves: enum authority work changed review semantics or duplicated value lists.
- Automation location: enum authority map.

T8. M2 spec-review representative behavior parity
- Covers: `SFRP-R2`, `SFRP-R21`, `SFRP-R22`, `SFRP-R23`
- Level: manual
- Fixture/setup: representative spec input selected during M2.
- Steps:
  1. Compare expected `spec-review` output behavior before and after M2.
  2. Check review status, material findings, review dimensions, recording status, and eventual test-spec readiness.
  3. Classify every difference as `equivalent`, `improvement`, or `regression`.
- Expected result: no unresolved `regression` is present.
- Failure proves: the presentation edit caused a material review behavior change.
- Automation location: `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`.

T9. M3 test-spec required-section and coverage table preservation
- Covers: `SFRP-R1`, `SFRP-R2`, `SFRP-R3`, `SFRP-R7`, `SFRP-R9`, `SFRP-R19`, `SFRP-R20`, `EC3`, `EC4`
- Level: manual
- Fixture/setup: baseline and edited `skills/test-spec/SKILL.md`.
- Steps:
  1. Confirm the normalized baseline remains present immediately before M3 edits.
  2. Identify required-section prose and coverage expectations.
  3. Compare every section, coverage rule, and output-skeleton obligation to the edited table or authority surface.
  4. Confirm the output skeleton still reflects the same test-spec artifact contract.
- Expected result: table form preserves all required sections, coverage rules, and output skeleton obligations.
- Failure proves: readability work changed the test-spec artifact contract.
- Automation location: content-preservation matrix.

T10. M3 test-spec enum authority, stop-condition visibility, and section exceptions
- Covers: `SFRP-R10`, `SFRP-R11`, `SFRP-R12`, `SFRP-R13`, `SFRP-R14`, `SFRP-R15`, `SFRP-R16`, `SFRP-R17`, `SFRP-R18`, `E3`, `EC1`, `EC2`, `EC3`
- Level: manual
- Fixture/setup: baseline and edited `skills/test-spec/SKILL.md`.
- Steps:
  1. Record each changed closed enum's source, destination, exact values, and duplicate-handling rule.
  2. Confirm stop conditions remain before the normal artifact-generation procedure.
  3. Record any family-order exception that preserves stop-condition or claim-boundary visibility.
  4. Confirm the output skeleton is not treated as a second full enum authority unless explicitly selected as the authority.
- Expected result: enum values remain identical, stop conditions stay visible, and section-order exceptions are documented.
- Failure proves: readability work weakened invocation boundaries or enum authority.
- Automation location: enum authority map and content-preservation matrix.

T11. M3 test-spec representative behavior parity
- Covers: `SFRP-R2`, `SFRP-R21`, `SFRP-R22`, `SFRP-R23`
- Level: manual
- Fixture/setup: representative approved spec and plan selected during M3.
- Steps:
  1. Compare expected `test-spec` output behavior before and after M3.
  2. Check output structure, required-section coverage, requirement coverage, example coverage, edge-case coverage, and stop-condition behavior.
  3. Classify every difference as `equivalent`, `improvement`, or `regression`.
- Expected result: no unresolved `regression` is present.
- Failure proves: the presentation edit caused a material test-planning behavior change.
- Automation location: `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md`.

T12. Generated adapter output validation and no hand edits
- Covers: `SFRP-R1`, `SFRP-R4`, `SFRP-R24`, `E4`, `EC5`
- Level: static
- Fixture/setup: edited canonical skills; repository adapter manifest and current version value.
- Steps:
  1. Run skill generation and adapter validation commands named in the plan.
  2. Confirm generated public adapter skill bodies were not hand-edited.
  3. If validation cannot run or exposes unrelated baseline debt, record an explicit deferral with rationale.
- Expected result: current adapter output is validated from canonical skills, or a reviewed deferral explains why it is intentionally deferred.
- Failure proves: canonical and generated output currency is unproven.
- Automation location: M3 validation notes and `change.yaml`.

T13. Cold-read scanability verification
- Covers: `SFRP-R25`, `AC1`
- Level: manual
- Fixture/setup: edited `skills/spec/SKILL.md`, `skills/spec-review/SKILL.md`, and `skills/test-spec/SKILL.md`.
- Steps:
  1. Inspect each changed skill without using repository-internal context.
  2. Locate required sections or review dimensions, closed enums, stop conditions, output expectations, validation obligations, and handoff boundaries.
  3. Record success or explain why cold-read was deferred.
- Expected result: a reader can find the required surfaces quickly in each changed skill, or a deferral is recorded.
- Failure proves: the readability pass did not achieve its scanability goal.
- Automation location: M3 cold-read notes in `behavior-preservation.md` or separate reviewed evidence.

T14. Final scope and non-goal guard
- Covers: `SFRP-R1`, `SFRP-R2`, `SFRP-R3`, `SFRP-R4`, `AC7`
- Level: static
- Fixture/setup: final branch diff before verify.
- Steps:
  1. Inspect the final diff.
  2. Confirm only in-scope canonical skill files and workflow proof, validation, plan, review, or metadata artifacts changed.
  3. Confirm no routing descriptions, packaging resources, build-time partials, generated public adapter skill bodies, or produced-artifact readability contracts changed.
- Expected result: final diff stays inside the approved scope.
- Failure proves: implementation exceeded the accepted proposal and approved spec.
- Automation location: final code-review and verify evidence.

T15. Lifecycle artifact and metadata validation
- Covers: workflow proof surface for implementation and review reliance
- Level: static
- Fixture/setup: proposal, spec, test spec, plan, plan index, change metadata, and review artifacts.
- Steps:
  1. Run lifecycle validation for touched lifecycle artifacts.
  2. Run change metadata validation.
  3. Run selected CI for touched artifact paths.
- Expected result: lifecycle artifacts are valid and the active plan names the correct next stage.
- Failure proves: implementation would rely on stale or invalid workflow state.
- Automation location: validation notes and `change.yaml`.

## Fixtures and data

| Fixture or evidence | Use |
| --- | --- |
| `skills/spec/SKILL.md` | M1 source and destination for `spec` readability proof. |
| `skills/spec-review/SKILL.md` | M2 source and destination for `spec-review` readability proof. |
| `skills/test-spec/SKILL.md` | M3 source and destination for normalized `test-spec` readability proof. |
| `docs/changes/2026-05-20-test-spec-contract-normalization/behavior-preservation.md` | Baseline evidence for normalized `test-spec` when present. |
| `docs/changes/2026-05-20-test-spec-contract-normalization/behavior-parity.md` | Baseline behavior-parity evidence for normalized `test-spec` when present. |
| `docs/changes/2026-05-20-spec-family-readability-pass/behavior-preservation.md` | Required content-preservation matrix, enum authority map, section-order exceptions, and cold-read notes. |
| `docs/changes/2026-05-20-spec-family-readability-pass/behavior-parity.md` | Required representative behavior-parity classifications for all three skills. |
| `docs/changes/2026-05-20-spec-family-readability-pass/change.yaml` | Validation and changed-file metadata. |

## Mocking/stubbing policy

No mocks or stubs are required. The change is Markdown source plus deterministic
validation. Any representative model-output comparison is manual proof and must
not replace the preservation matrix.

## Migration or compatibility tests

- `T12` verifies generated adapter output currency or an explicit deferral.
- `T14` verifies no generated public adapter skill bodies, packaging surfaces, routing descriptions, legacy archives, or produced-artifact contracts were changed.
- No data migration is applicable.

## Observability verification

Observability is through durable review and proof artifacts:

- `behavior-preservation.md` records source-to-destination proof.
- `behavior-parity.md` records representative behavior classifications.
- review records confirm code-review and final verification results.
- `change.yaml` records validation commands and results.

## Security/privacy verification

`T14` verifies that the final diff does not introduce secrets, credentials, new
external services, private data flows, or repository-internal runtime
dependencies in published skill text.

## Performance checks

No runtime performance behavior is affected. Token cost is not a driver for this
change. If implementation records a material token increase, code-review should
confirm the increase is justified by scanability and preserved output quality
under the existing skill-readability contract.

## Manual QA checklist

- Confirm normalized `test-spec` baseline before M3 edits.
- Compare each table row against its source prose.
- Compare each fenced or table-authority enum against its source value set.
- Confirm every changed closed enum value set appears once per skill.
- Confirm stop conditions, claim boundaries, validation obligations, and handoff boundaries remain visible before normal procedure where required.
- Confirm no produced artifact output expectations changed.
- Confirm behavior-parity classifications contain no unresolved `regression`.
- Confirm adapter validation or an explicit deferral is recorded.

## What not to test and why

- Do not test produced spec or test-spec artifact readability changes; they are out of scope.
- Do not test new packaging resources, build-time partials, or duplicated-block mechanisms; this proposal excludes them.
- Do not rewrite or inspect legacy release archives as if they were current generated output; retroactive archive rewriting is out of scope.
- Do not rely on snapshot-only comparisons for behavior parity; preservation matrices are the primary proof.
- Do not test routing changes beyond confirming routing descriptions were not edited.

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

None yet.

## Readiness

Active proof surface for `implement M1`. Implementation must begin with `T1`
baseline confirmation and must keep `T2` through `T15` current as the milestones
close.
