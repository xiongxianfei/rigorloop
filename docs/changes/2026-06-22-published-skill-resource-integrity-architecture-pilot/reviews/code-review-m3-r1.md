# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `a4695bc`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m3-r1.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SRI-M3-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
- Reviewed milestone: M3. Architecture Resource Normalization and Behavior Preservation
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3 resolution, M4, M5, M6, M7
- Required review-resolution: yes
- Finding IDs: SRI-M3-CR1
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `a4695bc` (`M3: normalize architecture skill resources`).
- Tracked governing branch state: approved skill-contract amendment, owner-approved test spec, approved architecture/ADR, closed M1 and M2 reviews, active plan M3 review-requested state, and M3 validation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R47-R49d and R55-R55e; `specs/skill-contract.test.md` T44; active plan M3.
- Validation evidence: M3 validation entries in `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml` and active plan validation notes.
- Implementation files reviewed: `skills/architecture/SKILL.md`, `skills/architecture/assets/`, `scripts/test-skill-validator.py`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/behavior-preservation.md`, active plan state, and change metadata.

## Diff summary

M3 adds `skills/architecture/assets/architecture-skeleton.md`, `skills/architecture/assets/adr-skeleton.md`, and `skills/architecture/assets/diagram-styles.mmd`; replaces operative architecture skill `templates/...` references with a `Resource map`; updates architecture skill tests to expect mapped assets; and records behavior-preservation evidence. The architecture and ADR skeletons are copy-and-fill assets, and the diagram style file is literal Mermaid copied material.

## Findings

## Finding SRI-M3-CR1

Finding ID: SRI-M3-CR1
Severity: major
Location: `scripts/skill_validation.py:144`; `scripts/test-skill-validator.py:1195`
Evidence: M3 normalized the canonical architecture skill and removed the operative `templates/...` references from `skills/architecture/SKILL.md`, but the validator still contains `TEMPORARY_RESOURCE_INTEGRITY_EXCEPTIONS` entries for the exact architecture legacy instructions. The comment immediately above those entries says M3 removes them by normalizing the architecture Resource map. The current test `test_published_skill_architecture_migration_exception_is_exact` still asserts that an architecture skill containing the exact legacy instruction passes validation. After M3, that exception lets the original defect class re-enter the architecture skill without failing canonical validation.

R49 requires steady-state published skills to express required skill-local dependencies in the `Resource map`, and R49d allows unmapped legacy references only as explicitly approved temporary migration debt. M3 is the migration milestone for the architecture skill, so the architecture-specific temporary exception should no longer remain active for the normalized architecture resource paths.

Required outcome: Remove or expire the architecture-specific temporary resource-integrity exceptions that were only approved until M3 normalization, and update regression coverage so the exact legacy architecture `templates/...` instructions now fail validation after M3. Keep the general bounded legacy-resource lint and false-positive protections intact.

Safe resolution path: Delete the architecture `templates/architecture.md`, `templates/diagram-styles.mmd`, and `templates/adr.md` entries from `TEMPORARY_RESOURCE_INTEGRITY_EXCEPTIONS`, or mark them inactive through an explicit expiration mechanism if the validator already supports one. Replace `test_published_skill_architecture_migration_exception_is_exact` with post-M3 coverage proving the exact former architecture instruction fails for an unmapped legacy resource, while `test_current_architecture_resource_map_uses_packaged_assets` continues to pass. Rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, selector-selected validation for `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, and `skills/architecture`, generated-skill checks selected for canonical skill changes, lifecycle validation, change metadata validation, review artifact validation, and `git diff --check --`.

needs-decision rationale: none

## Checklist coverage

- Spec alignment: concern. The architecture skill itself now matches R47-R48b and R55c-R55e, but the stale architecture exception conflicts with R49/R49d after M3 migration.
- Test coverage: concern. The new canonical architecture resource-map test is useful, but an existing test still proves the exact former architecture legacy instruction passes.
- Edge cases: concern. The exact original architecture defect instruction can be reintroduced and still pass validation.
- Error handling: pass. Mapped-resource diagnostics, path containment, and class checks remain unchanged.
- Architecture boundaries: pass. The new assets keep normative trigger, arc42, C4, ADR, review, and handoff behavior in `SKILL.md`, with behavior-preservation evidence recorded.
- Compatibility: concern. Leaving the temporary exception active weakens enforcement for newly changed architecture skill content after migration.
- Security/privacy: pass. No secrets, credentials, unsafe logging, or new trust boundary were introduced.
- Derived artifact currency: pass. M3 ran `build-skills.py --check`, `test-build-skills.py`, and an adapter archive regression selected for canonical skill changes.
- Unrelated changes: pass. The implementation diff is scoped to architecture resources, validator tests, behavior-preservation evidence, and lifecycle bookkeeping.
- Validation evidence: concern. The named validation commands are relevant and passed, but they include the stale exception test that should change for post-M3 behavior.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M3. Architecture Resource Normalization and Behavior Preservation
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Remaining implementation milestones: M3 resolution, M4, M5, M6, M7
Next stage: review-resolution for SRI-M3-CR1
Final closeout readiness: not ready; M3 remains open and later implementation milestones remain.
