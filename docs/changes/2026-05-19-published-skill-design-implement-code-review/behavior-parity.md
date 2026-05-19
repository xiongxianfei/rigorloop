# Published Skill Design Implement And Code-Review Behavior Parity

Change: `2026-05-19-published-skill-design-implement-code-review`

## Representative Artifacts

| Artifact class | Representative surface | Why it matters |
|---|---|---|
| Active plan | `docs/plans/2026-05-19-published-skill-design-implement-code-review.md` | Exercises planned milestone handoff, plan progress updates, validation notes, and state-sync expectations. |
| Implementation handoff | M1/M2/M3 milestone sections in the active plan | Exercises `implement` milestone state, validation evidence, and `code-review` handoff boundaries. |
| Clean code-review receipt | `docs/changes/2026-05-19-published-skill-design-spec-family/reviews/code-review-m3-r1.md` | Representative clean review shape with checklist, no-finding rationale, and next-stage routing. |
| Material finding review | `docs/changes/2026-05-19-published-skill-design-spec-family/reviews/code-review-m2-r1.md` | Representative material finding with evidence, required outcome, safe resolution, and review-resolution routing. |
| Review resolution | `docs/changes/2026-05-19-published-skill-design-spec-family/review-resolution.md` | Representative accepted finding disposition and closeout behavior. |
| Review log | `docs/changes/2026-05-19-published-skill-design-spec-family/review-log.md` | Representative clean receipt and material finding ledger behavior. |

## Parity Checks

M3 must confirm the rewrite preserves these outcomes:

| Area | Required parity result | M3 result |
|---|---|---|
| Implementation handoff state | `implement` still moves implemented milestones to `review-requested`, not `closed`. | Pass. `Milestone-aware handoff`, `Stop conditions`, and `Output skeleton` keep `review-requested | blocked` as the implementation result state. |
| Validation obligations | `implement` still names and records targeted validation before handoff. | Pass. `Validation layering`, `Implementation loop`, `Plan update requirements`, and `Output skeleton` preserve validation command/result reporting. |
| Plan update ownership | `implement` still owns active-plan progress, decisions, discoveries, and validation notes during execution. | Pass. Opening guidance and `Plan update requirements` keep active-plan ownership; the skeleton includes `Plan updates`. |
| First-pass completeness | `implement` still requires same-slice completeness before code-review handoff. | Pass. The full `First-pass completeness` section is preserved. |
| Review status taxonomy | `code-review` still uses exactly one first-pass status from the approved set. | Pass. `First-pass statuses` and result skeleton preserve `clean-with-notes`, `changes-requested`, `blocked`, and `inconclusive`. |
| Finding format | `code-review` still requires evidence, required outcome, and safe resolution or `needs-decision` for material findings. | Pass. `Material findings`, `Isolation and Recording`, and the skeleton findings placeholder preserve this shape. |
| Recording obligations | `code-review` still records clean formal reviews and material findings, and does not create empty review-resolution for clean reviews. | Pass. `Isolation and Recording` is preserved and the result skeleton names review record, review log, and review resolution. |
| Stop conditions | Both skills still stop on missing or contradictory governing artifacts, failing validation, or unresolved owner decisions. | Pass. Both skills preserve `Stop conditions`; `implement` also preserves validation-failure stop language. |
| Claim boundaries | Neither skill claims verification, CI, branch-ready, PR-ready, or downstream completion without owning evidence. | Pass. Frontmatter-adjacent `Workflow role`, claim-boundary sections, and expected-output wording preserve the no-claim boundaries. |
| Milestone routing | `code-review` still routes clean non-final reviews to the next implementation milestone and final clean reviews to final closeout only when all implementation milestones are closed. | Pass. `Handoff`, `Workflow handoff behavior`, and `Milestone-aware review handoff` preserve milestone routing. |

## M1 No-Change Evidence

M1 creates parity scope only. No behavior-significant skill wording changes are
made in M1.

## M3 Final Parity Statement

The M3 rewrite preserves the representative implementation handoff and
code-review outcomes. Static regression tests protect the new readability
contract, existing lifecycle-contract tests still pass, and generated skill plus
temporary adapter archive validation passed from canonical `skills/`.

## Token Cost Result

Command: `python scripts/measure-skill-tokens.py --skills-root skills`

| Skill | Baseline estimated tokens | M3 estimated tokens | Delta | Result |
|---|---:|---:|---:|---|
| `implement` | 4421 | 4860 | +9.9% | Pass. The increase is from explicit workflow-role and output-skeleton fields for a high-risk execution gate and remains under the `+10%` hard cap. |
| `code-review` | 5054 | 5554 | +9.9% | Pass. The increase is from explicit workflow-role and first-pass review output fields for the highest-risk review gate and remains under the `+10%` hard cap. |

Both skills exceed the `+5%` rationale threshold because M3 adds required
published-skill contract fields, but both remain below the `+10%` hard cap.
