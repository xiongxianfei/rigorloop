# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: SRI-PLAN1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/plan-review-r1.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
- Open blockers: SRI-PLAN1
- Immediate next stage: plan revision

## Findings

### SRI-PLAN1: Clean-install comparison is sequenced after architecture resource changes

Finding ID: SRI-PLAN1
Severity: major
Location: `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md` M1, M3, M5, Dependencies, and Decision log.
Evidence: R55 requires the architecture resource-integrity pilot to audit the architecture resource chain before adding, renaming, packaging, or removing architecture resources. R55a requires that audit to compare canonical skill source, built skill output, adapter package or archive output, release candidate, and clean installed target trees for Codex, Claude, and opencode. The plan's M1 says it will compare clean installed target trees only "where tooling already exists" and its rollback says to "defer unimplemented smoke proof to M5." M3 then changes architecture resources, while M5 adds the clean-install smoke later. The Dependencies section also says "M4 generated/archive parity should complete before M5 clean-install smoke," and the Decision log says to "Keep clean-install smoke after generated/archive parity."
Required outcome: The plan must require complete R55/R55a resource-chain audit evidence, including clean installed Codex, Claude, and opencode target trees or an explicitly approved scope-changing spec/proposal revision, before M3 changes architecture resources.
Safe resolution path: Revise the plan so M1 either includes enough temporary or repository-owned clean-install inspection to compare the installed target trees before architecture resource normalization, or split an early prerequisite milestone before M3 that implements only the minimum clean-install audit/proof needed for R55a. Keep the later M5 release-quality clean-install smoke only for reusable enforcement hardening if still useful. Re-run plan-review after the sequencing is corrected.
needs-decision rationale: none

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| self-contained context | pass | The plan names the defect, current legacy references, source/generated/install boundaries, and implementation anchors. |
| source alignment | block | SRI-PLAN1 conflicts with R55/R55a sequencing because full clean-install comparison is deferred until after architecture resource changes. |
| milestone size | pass | Milestones are reviewable and mostly split by audit, validator, resource normalization, generated/archive parity, clean install, audit/enforcement, and closeout. |
| sequencing | block | SRI-PLAN1: M5 clean-install proof comes after M3 resource normalization even though R55 requires the full architecture resource-chain audit first. |
| scope discipline | pass | Non-goals reject `templates/` as implicit package class, generated-output hand edits, broad path scanning, and live registry proof as implementation closeout. |
| validation quality | concern | Validation commands are concrete, but the sequencing gap means the clean-install proof cannot protect M3 as written. |
| TDD readiness | pass | The plan identifies test fixtures for resource maps, legacy lint, false positives, stale generated copies, archive parity, and clean-install failures. |
| risk coverage | pass | Risks cover stale local install state, false positives, hidden policy extraction, clean-install cost, and unrelated audit drift. |
| architecture alignment | concern | The architecture surfaces are represented, but the R55 architecture-pilot audit ordering is not preserved. |
| operational readiness | concern | The plan acknowledges clean-install tooling may not exist, but it defers that tooling past the point where the spec needs its evidence. |
| plan maintainability | pass | The plan has clear milestones, requirements mapping, validation, recovery, and handoff state. |

## Readiness

Changes requested.

No automatic downstream handoff is performed because this was a direct `plan-review` request.

Immediate next repository stage: plan revision.

Stop condition: Do not proceed to `test-spec` or implementation until SRI-PLAN1 is resolved and the revised plan is re-reviewed.
