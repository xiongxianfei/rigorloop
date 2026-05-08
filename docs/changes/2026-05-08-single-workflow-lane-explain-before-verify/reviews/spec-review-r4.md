# Spec Review R4

Review ID: spec-review-r4
Stage: spec-review
Round: 4
Reviewer: Codex spec-review
Target: `specs/rigorloop-workflow.md`, matching workflow test specs, public skill text, and generated skill copies
Status: changes-requested

## Review inputs

- Workflow spec amendment: `specs/rigorloop-workflow.md`
- Matching test specs: `specs/rigorloop-workflow.test.md`, `specs/workflow-stage-autoprogression.test.md`, `specs/milestone-aware-review-handoff.test.md`
- Public skill text: `skills/constitution/SKILL.md`
- Generated skill mirror: `.codex/skills/constitution/SKILL.md`
- Public workflow summary: `docs/workflows.md`
- Prior review-resolution: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/review-resolution.md`

## Findings

### SR9 - Retired proportional-evidence and fast-lane wording remains

Finding ID: SR9
Severity: major

Evidence: The accepted direction removes proportional-evidence and lane vocabulary from public workflow guidance and says manual isolated skill invocation explains focused use. `specs/rigorloop-workflow.md:927` still says "Proportional-evidence instructions SHOULD fit comfortably inside common PR or issue workflows". The public `constitution` skill still asks for `Fast-lane exceptions` at `skills/constitution/SKILL.md:68`, and the generated Codex skill mirror carries the same wording at `.codex/skills/constitution/SKILL.md:68`. Existing stale-term validation did not catch these forms because the checked phrases were narrower than the retired vocabulary variants.

Required outcome: Remove the retired proportional-evidence and fast-lane wording from the canonical workflow spec and public skill text. Regenerate generated skill and adapter copies as needed. Extend static checks so case and hyphen variants such as `Proportional-evidence` and `Fast-lane exceptions` cannot return on public workflow or shipped skill surfaces.

Safe resolution: Replace `specs/rigorloop-workflow.md:927` with UX wording about concise contributor-facing workflow instructions or manual-skill isolation, without using the retired proportional-evidence term. Replace the constitution skill section with standard workflow and manual skill invocation/isolation guidance. Rebuild generated skill mirrors and adapter packages from canonical sources. Update static wording checks to use case-insensitive and hyphen/space-aware retired-term patterns for public workflow and shipped skill surfaces.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Requirement clarity | concern | The main requirements now define one standard workflow and isolated manual skill invocation, but a later UX bullet still uses the retired proportional-evidence term. |
| Normative language | concern | The stale workflow-spec bullet uses `SHOULD`, so it remains contract wording rather than harmless history. |
| Completeness | concern | The public `constitution` skill and generated mirror still carry fast-lane exception guidance. |
| Testability | concern | Existing static checks missed case and hyphen variants of retired terms. |
| Examples | pass | The amended examples use the current final closeout order and isolated manual skill model. |
| Compatibility | pass | Direct isolated skill behavior, direct `verify`, direct `pr`, and final closeout routing remain intact. |
| Observability | pass | The defect is statically observable and can be covered by phrase-based checks. |
| Security/privacy | pass | No security-sensitive behavior is introduced. |
| Non-goals | pass | The finding does not require runtime workflow orchestration or adapter format changes. |
| Acceptance criteria | concern | Public surfaces still expose retired lane/evidence vocabulary that the amendment says contributors should not see as route guidance. |

## Review outcome

Changes requested.

No automatic downstream handoff is performed because this was a direct `spec-review` request.

Immediate next repository stage: none

Eventual `test-spec` readiness: not-ready

Stop condition: upstream workflow spec, public skill guidance, generated copies, and static wording checks must remove or block the retired proportional-evidence and fast-lane variants before downstream planning or implementation relies on the amended public workflow-surface contract.
