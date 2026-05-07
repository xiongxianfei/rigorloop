# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review skill
Target: specs/vision-skill.md
Status: changes-requested

## Scope

Reviewed the draft vision skill strategic-positioning contract against the accepted proposal, the proposal-review closeout for `PR-1`, `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, and the existing vision skill test-spec context. The review focused on requirement clarity, proposal alignment, testability, migration behavior, observability, and acceptance criteria.

## Dimension Results

| Dimension | Result | Notes |
| --- | --- | --- |
| Requirement clarity | concern | Most requirements are precise, but the word-cap exception in `R32b` permits a different cap outside the accepted proposal. |
| Normative language | concern | `R32b` uses a strong `MUST NOT` but then adds an owner override that weakens the intended hard cap. |
| Completeness | pass | Initial, material repositioning, editorial, no-vision, README, retired lowercase path, and rationale-artifact cases are covered. |
| Testability | pass | The new requirements can map to static assertions, selector regressions, review of generated guidance, and artifact checks. |
| Examples | pass | Examples cover methodology, ordinary substrate, true substrate, material repositioning, and editorial no-update behavior. |
| Compatibility | concern | The rollback and migration model is mostly clear, but the word-cap override conflicts with the accepted compatibility decision. |
| Observability | pass | Final output requirements include changed files, README action, positioning summary, rationale path, section changes, and stop reasons. |
| Security/privacy | pass | Existing sensitive-information and research boundaries remain in force. |
| Non-goals | pass | Scope exclusions are explicit, including no prompt-output harness and no validator enforcement for prose quality. |
| Acceptance criteria | concern | `AC15` says owner-authorized 900-word cap, but `R32b` allows a different owner-requested cap. |

## Findings

### SR1-F1: `R32b` allows a word-cap override beyond the accepted proposal

Finding ID: SR1-F1

Severity: major

Evidence: `specs/vision-skill.md:212` says methodology, protocol, workflow, or operating-model projects may exceed 750 words only when the owner explicitly allows the extra length and the extra content is needed. `specs/vision-skill.md:214` then says `VISION.md` must not exceed 900 words "unless the owner explicitly requests a different cap." The accepted proposal instead says `VISION.md` should normally stay at or under 750 words, and that methodology, protocol, workflow, or operating-model visions may go up to 900 words only with owner permission when needed (`docs/proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md:77`, `docs/proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md:104`-`105`). `AC15` also frames the accepted behavior as a 750-word normal cap and owner-authorized 900-word methodology cap (`specs/vision-skill.md:469`).

Required outcome: The spec must make 900 words the maximum under this proposal's contract, rather than adding a general owner-requested alternate cap.

Safe resolution: Replace `R32b` with wording such as: "`VISION.md` generated or revised by the skill MUST NOT exceed 900 words." If a future owner wants a different hard cap, that should be handled by a later accepted proposal/spec update rather than by this contract.

## Recommendation

Request changes before approving the spec. The remaining contract is reviewable, and after `SR1-F1` is corrected the immediate next repository stage can be spec-review rerun.
