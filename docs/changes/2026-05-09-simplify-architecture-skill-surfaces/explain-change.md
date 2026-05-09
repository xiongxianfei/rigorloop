# Explain Change: Simplify Architecture Skill Surfaces

## Summary

This change simplifies the `architecture` and `architecture-review` skill surfaces around one invariant:

```text
Proposal resolves uncertainty.
Architecture records accepted design.
ADR records durable decisions.
```

The implementation removes change-local architecture deltas from the normal architecture authoring and review path, teaches architecture-review to classify the review surface before applying checks, preserves the existing C4 plus arc42 plus ADR method, and refreshes generated Codex skill mirrors plus public adapter packages from canonical skill sources.

## Problem

The previous architecture workflow made change-local architecture deltas a normal authoring and review surface. That let architecture artifacts drift into temporary design exploration and encouraged architecture-review to look for delta and merge-back evidence even when the right surface was a direct canonical architecture update, an ADR, or a no-impact rationale.

That created recurring workflow ambiguity:

- proposal and proposal-review should settle uncertain direction, but architecture could still appear to own unresolved option selection;
- architecture should record accepted current design, but temporary deltas could look like durable design truth;
- architecture-review could keep requiring change-local delta evidence for canonical updates;
- generated skill and adapter outputs could carry stale public guidance if they were not refreshed after canonical skill edits.

## Decision Trail

| Artifact | Decision carried into the change |
| --- | --- |
| `docs/proposals/2026-05-09-simplify-architecture-skill-surfaces.md` | Simplify architecture surfaces to no-impact rationale, proposal/spec blocker, canonical update, or ADR; preserve public skill portability and adapter validation. |
| `specs/architecture-package-method.md` | Added `R32`-`R39`, `R56`-`R58`, `R61`, `R85`-`R86`, `R108`-`R110`, `R119`-`R124`, `AC20`-`AC22` for the simplification. |
| `docs/architecture/system/architecture.md` | Records canonical architecture package and generated-output boundaries. |
| `docs/adr/ADR-20260509-architecture-skill-surface-simplification.md` | Narrows the earlier architecture-package method by removing normal change-local deltas from the architecture skill surface. |
| `docs/plans/2026-05-09-simplify-architecture-skill-surfaces.md` | Sequenced M1-M4 through per-milestone implementation, code-review, generated-output refresh, and lifecycle closeout. |
| `docs/changes/2026-05-09-simplify-architecture-skill-surfaces/review-resolution.md` | Records proposal, plan, and code-review finding dispositions; all material findings are resolved or explicitly dispositioned. |

## Milestone Map

| Milestone | Outcome |
| --- | --- |
| M1 | Revised the test spec for the 2026-05-09 simplification, normalized reviewed architecture/ADR lifecycle state, and removed stale normal-delta proof wording. |
| M2 | Updated `skills/architecture/SKILL.md` to choose the smallest valid architecture surface and removed normal change-local delta and merge-back authoring guidance. |
| M3 | Updated `skills/architecture-review/SKILL.md` to classify review surfaces first and removed normal delta/merge-back review checklist wording. |
| M4 | Refreshed generated `.codex/skills/` and `dist/adapters/` outputs through repository generators and proved generated-output and adapter drift are closed. |
| M5 | Adds this durable rationale so final `verify` can assess artifact-code-test coherence before PR handoff. |

## Diff Rationale By Area

| Area | Change | Reason | Source artifact | Test or evidence |
| --- | --- | --- | --- | --- |
| Test specification | Updated `specs/architecture-package-method.test.md` for normal architecture surfaces, historical/exceptional delta evidence, architecture-review classification, and adapter drift plus validation proof. | The approved spec changed the contract; the test spec needed to operationalize it before skill implementation. | `R32`-`R39`, `R56`-`R58`, `R61`, `R85`-`R86`, `R110`, `R119`-`R124`, `AC20`-`AC22` | M1 targeted validation and code-review R6. |
| Canonical architecture package and ADR | Normalized the architecture package/ADR lifecycle state and amended the method with `ADR-20260509`. | Accepted architecture truth and durable decisions belong in canonical architecture and ADRs, not temporary deltas. | Architecture-review R1; ADR decision | Artifact lifecycle validation and architecture-review R1. |
| `architecture` skill | Replaced normal delta output with no-impact rationale, blocked proposal/spec routing, direct canonical architecture update, or ADR. | Architecture records accepted design and stops when direction or behavior is unsettled. | `R32`-`R39`, `R108`-`R110`, `AC21` | `test-skill-validator.py`, stale wording scans, code-review R7. |
| `architecture-review` skill | Added review-surface classification and surface-specific checks for canonical updates, ADRs, no-impact rationales, and proposal/spec gaps. | Review should evaluate the actual architecture surface and must not require change-local deltas for canonical updates. | `R57`, `R119`-`R124`, `AC22` | `test-skill-validator.py`, `test-review-artifact-validator.py`, code-review R8. |
| Generated Codex skills | Refreshed `.codex/skills/architecture*/SKILL.md` through `scripts/build-skills.py`. | Generated runtime mirrors must match canonical skill sources. | `R58`, `AC20`; generated-output boundary in architecture | `python scripts/build-skills.py --check`, SHA-256 hash comparison during code-review R9. |
| Public adapters | Refreshed Claude, Codex, and opencode adapter skill copies through `scripts/build-adapters.py --version 0.1.1`. | Public adapter packages must ship the same accepted skill guidance. | Proposal adapter validation requirement; `R58`, `AC20` | `python scripts/build-adapters.py --version 0.1.1 --check`, `python scripts/validate-adapters.py --version 0.1.1`, `python scripts/test-adapter-distribution.py`. |
| Review and lifecycle evidence | Recorded proposal-review, spec-review, architecture-review, plan-review, per-milestone code-review, and review-resolution evidence. | The workflow requires material findings and milestone review closeout to be durable, not chat-only. | `CONSTITUTION.md`, active plan, review artifacts | `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`. |

## Tests And Proof Surfaces

No runtime service code was changed. The implementation surface is workflow-governance artifacts, skill text, generated skill mirrors, and adapter packages.

The main proof surfaces are:

- `specs/architecture-package-method.test.md` for traceability from requirements to proof;
- `scripts/test-skill-validator.py` for canonical skill wording and stale-term regression coverage;
- `scripts/test-review-artifact-validator.py` for review artifact contract coverage;
- `scripts/test-adapter-distribution.py` for adapter generation, drift, manifest, and validation behavior;
- generated-output drift checks for `.codex/skills/` and `dist/adapters/`;
- artifact lifecycle, change metadata, review artifact, selector, diff, and whitespace validation.

## Validation Evidence

Validation already recorded in the active plan and `change.yaml` includes:

- `python scripts/validate-skills.py`
- `python scripts/test-skill-validator.py`
- `python scripts/test-review-artifact-validator.py`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version 0.1.1 --check`
- `python scripts/validate-adapters.py --version 0.1.1`
- `python scripts/test-adapter-distribution.py`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces/change.yaml`
- `python scripts/validate-review-artifacts.py docs/changes/2026-05-09-simplify-architecture-skill-surfaces`
- `python scripts/select-validation.py --mode explicit ...`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `bash scripts/ci.sh --mode explicit ...`
- `git diff --check ...`
- whitespace scans with `rg -n '[[:blank:]]$|\t' ...`

The known lifecycle warning in `docs/plan.md` line 17 is pre-existing unrelated baseline debt and is not introduced by this change.

Hosted CI has not been observed from this environment.

## Review Resolution Summary

Material findings were recorded and dispositioned in `review-resolution.md`:

- `PASS-F1`: accepted and resolved by requiring a new ADR that amends or narrows the existing architecture-package-method ADR.
- `PR-F1`: accepted and resolved by adding per-milestone code-review handoff and review closeout requirements.
- `CR1-F1`, `CR2-F1`, and `CR4-F1`: accepted and resolved through tracked plan/change/review state alignment.
- `CR5-F1`: rejected by owner decision and recorded as resolved.

Code-review R6, R7, R8, and R9 then closed M1, M2, M3, and M4 with no material findings.

## Scope Control

This change intentionally did not:

- remove the C4 plus arc42 plus ADR architecture method;
- delete historical change-local architecture evidence;
- require ADRs for every small architecture edit;
- use architecture-review to settle product direction;
- create a new skill;
- hand-edit generated `.codex/skills/` or `dist/adapters/` output;
- mark the initiative done before explain-change, verify, and PR handoff complete.

## Risks And Follow-Ups

- Final verification still needs to run after this rationale exists.
- PR handoff remains downstream of successful verify.
- The unrelated `docs/plan.md` lifecycle warning should remain visible to reviewers but is not caused by this change.
