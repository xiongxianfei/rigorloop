# Spec Review R2

Review ID: spec-review-r2
Stage: spec-review
Round: 2
Reviewer: Codex spec-review skill
Target: specs/vision-skill.md
Status: changes-requested

## Scope

Reviewed the revised vision skill strategic-positioning contract after the `SR1-F1` fix. This rerun focused on whether the 750/900-word cap is now internally consistent with the accepted proposal, prior review closeout, acceptance criteria, and boundary behavior.

## Dimension Results

| Dimension | Result | Notes |
| --- | --- | --- |
| Requirement clarity | concern | `R32b` now has the correct hard cap, but the boundary behavior still permits an owner-requested cap above 900 words. |
| Normative language | concern | The requirement-level `MUST NOT exceed 900 words` conflicts with a later invalidity rule that includes an override. |
| Completeness | pass | Initial, material repositioning, editorial, no-vision, README, retired lowercase path, and rationale-artifact cases remain covered. |
| Testability | concern | Static assertions can test `R32b`, but they would still need to resolve the contradictory boundary sentence. |
| Examples | pass | Examples remain concrete and aligned with the strategic-positioning proposal. |
| Compatibility | concern | The cap model still does not fully match the accepted proposal because one boundary rule preserves a beyond-900 override. |
| Observability | pass | Final output and validation reporting requirements remain clear. |
| Security/privacy | pass | Sensitive-information and external-research boundaries remain intact. |
| Non-goals | pass | Scope exclusions are explicit, including no prompt-output harness and no validator enforcement for prose quality. |
| Acceptance criteria | concern | `AC15` says owner-authorized 900-word methodology cap, while the boundary behavior still allows a different owner-requested cap. |

## Findings

### SR2-F1: Boundary behavior still allows an override beyond the 900-word cap

Finding ID: SR2-F1

Severity: major

Evidence: `specs/vision-skill.md:214` now correctly says `VISION.md` generated or revised by the skill must not exceed 900 words. But `specs/vision-skill.md:383` still says a generated or revised `VISION.md` over 900 words is invalid "unless the owner explicitly requested a different cap." The accepted proposal permits owner-authorized expansion only up to 900 words for methodology, protocol, workflow, or operating-model projects (`docs/proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md:77`, `docs/proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md:104`-`105`), and `AC15` frames the same owner-authorized 900-word methodology cap (`specs/vision-skill.md:469`).

Required outcome: The spec must remove the remaining owner-requested alternate-cap exception so boundary behavior enforces the same hard 900-word maximum as `R32b`.

Safe resolution: Replace the boundary sentence at `specs/vision-skill.md:383` with wording such as: "A generated or revised `VISION.md` over 900 words is invalid and must be shortened before completion."

## Recommendation

Request changes before approving the spec. `SR1-F1` is closed at the requirement line, but `SR2-F1` must be fixed before downstream planning or test-spec derivation relies on the word-cap contract.
