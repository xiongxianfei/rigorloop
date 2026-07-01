# Behavior Preservation: Bounded Review-Fix Autoprogression in Chat

## Scope

This proof covers the integrated proposal-side `bounded-review-fix` profile
through `test-spec-review`. It records the preservation evidence required by M5
after M1 through M4 established review-fix metadata, routing, review-resolution
validation, and workflow guidance.

The implemented feature is artifact-, validator-, and skill-guidance-driven. It
does not add a daemon, background worker, release runner, public network
operation, or PR automation. The repository-owned proof is the combination of
change metadata validation, artifact lifecycle route fixtures, review artifact
validation, canonical skill checks, generated-skill checks, adapter distribution
checks, formal review records, and this preservation matrix.

## Preservation Matrix

| Surface | Baseline | Review-fix proof | Result |
| --- | --- | --- | --- |
| Direct review invocations | isolated by default | direct `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, `test-spec-review`, and `code-review` do not activate, resume, or advance `bounded-review-fix` | preserved |
| Formal review recording | required for lifecycle reviews | review log and review records remain required before review-fix continuation or auto-resolution evidence | preserved |
| Material finding disposition | durable `review-resolution.md` required | review-fix auto-resolution fields are validated only inside recorded dispositions and require final closeout consistency | preserved and tightened |
| Same-review rerun after fixes | manual or reviewer-owned | auto-applied review-fix dispositions require same-review rerun linkage before closeout | strengthened |
| `authoring-through-plan-review` | separate profile, stops after clean plan-review | validator and skill guidance preserve its stop-before-`test-spec` boundary | preserved |
| `implementation-through-verify` | separate phase-gated profile, stops before PR | validator and skill guidance preserve its separate authorization, phase gates, review correction loop, and stop-before-PR boundary | preserved |
| Review-fix stage scope | did not exist | bounded to proposal-side targets through `test-spec-review` | intentionally extended |
| Implementation, verify, PR, release, publication, network, destructive, and external-state operations | owned by other workflow stages or out of scope | review-fix validators and guidance prohibit routing to these operations | preserved |
| Architecture conditional stages | manually routed from spec evidence | recorded assessment is exactly `architecture-required`, `architecture-not-required`, or `architecture-ambiguous` | preserved with explicit routing |
| Skipped conditional target | no review-fix behavior | `architecture-not-required` plus requested architecture target stops with `target-not-applicable` | added safe stop |
| Unknown state values | must fail closed | profile, status, target stage, stop reason, review status, auto-fix class, and disposition validators reject unknown values | preserved and broadened |
| Partial user-visible mode | not available | M5 validates the full proposal-side contract before handoff; no partial review-fix mode is separately enabled | preserved |

## Boundary Evidence

| Boundary | Evidence | Result |
| --- | --- | --- |
| Durable authorization lives only under `workflow.autoprogression.review_fix` | `scripts/test-change-metadata-validator.py -k review_fix`; `schemas/change.schema.json`; `scripts/validate-change-metadata.py` | preserved single owner |
| Direct review invocations stay isolated even when state exists | `scripts/test-artifact-lifecycle-validator.py -k review_fix`; `scripts/test-skill-validator.py -k review_fix` | preserved |
| Current gate must be recorded, current, and approved before routing | `scripts/test-artifact-lifecycle-validator.py -k review_fix`; CR-RFA-M2-1 resolution evidence | preserved and tightened |
| Auto-safe resolution evidence is driver-owned and fail-closed | `scripts/test-review-artifact-validator.py -k review_fix`; CR-RFA-M3-1 and CR-RFA-M3-2 resolution evidence | preserved and tightened |
| The proposal-side path reaches no later than `test-spec-review` | artifact-lifecycle review-fix routing tests and workflow skill guidance | preserved |
| Existing autoprogression profiles remain independent | `scripts/test-artifact-lifecycle-validator.py -k autoprogression`; `scripts/test-change-metadata-validator.py -k autoprogression`; `scripts/test-skill-validator.py -k review_fix` | preserved |
| Generated skill output remains reproducible from canonical skills | `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py`; `python scripts/validate-skills.py` | preserved |
| Adapter support surface remains metadata/install guidance only | `python scripts/test-adapter-distribution.py`; unchanged `dist/adapters/README.md` and `dist/adapters/manifest.yaml` | preserved |
| Release-note fixture support for non-portable skills | release metadata fixtures previously assumed no exclusions | fixture helper can now name `workflow` when current canonical skills are used | preserved and updated |

## Acceptance Criteria Trace

| Criteria | Proof surface |
| --- | --- |
| `AC1`-`AC6`, `AC15`-`AC19` | change metadata validators and review-fix state fixtures |
| `AC7`-`AC13`, `AC26` | review artifact validators and review-resolution fixtures |
| `AC14`, `AC20`-`AC23` | artifact lifecycle routing fixtures |
| `AC24`-`AC25` | autoprogression compatibility fixtures, skill guidance checks, and generated/adapter validation |

## Unaffected Surfaces

| Surface | Rationale |
| --- | --- |
| `scripts/build-skills.py` | Existing generated-skill check already validates canonical skill output; no logic change is required for review-fix wording. |
| `scripts/test-build-skills.py` | Existing generated output and resource parity tests cover the canonical skill changes. |
| `dist/adapters/README.md` | Review-fix changes affect canonical skills and workflow guidance, not the public adapter install contract. |
| `dist/adapters/manifest.yaml` | The supported skill list and adapter command aliases are unchanged by review-fix behavior. |

## Result

The review-fix profile is additive and bounded. It preserves direct-review
isolation, formal review recording, same-review rereview after auto-fixes, the
existing `authoring-through-plan-review` and `implementation-through-verify`
profiles, and the adapter/public distribution boundary.

The only intentional extension is the explicitly armed `bounded-review-fix`
proposal-side loop through `test-spec-review`, with validators enforcing target
bounds, clean-gate requirements, recorded evidence, owner-decision stops, and
fail-closed vocabulary handling.
