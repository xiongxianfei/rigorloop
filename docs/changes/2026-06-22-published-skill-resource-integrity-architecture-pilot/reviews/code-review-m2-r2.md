# Code Review M2 R2

Review ID: code-review-m2-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review
Target: commit `d0fcb0b`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r2.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SRI-M2-CR2
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r2.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
- Reviewed milestone: M2. Canonical Resource-Integrity Validator and Fixtures
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution, M3, M4, M5, M6, M7
- Required review-resolution: yes
- Finding IDs: SRI-M2-CR2
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `d0fcb0b` (`M2: resolve legacy resource lint finding`).
- Tracked governing branch state: accepted proposal, approved skill-contract amendment, owner-approved test spec, approved architecture/ADR, active plan, M1 audit and review, M2 R1 review, accepted SRI-M2-CR1 review-resolution, and M2 R2 implementation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R49-R49d; `specs/skill-contract.test.md` T43; `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md` M2; `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md#code-review-m2-r1`.
- Validation evidence: M2 R2 validation entries in `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml` and the active plan validation notes.
- Implementation files reviewed: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/validator-fixtures.md`, active plan state, review-resolution, review log, and change metadata.

## Diff summary

The SRI-M2-CR1 resolution adds resource-lint-specific constants for skill-local prefixes, resource-loading verbs, and external resource context. It stops using `PUBLISHED_ALLOWED_PROJECT_LOCAL_TERMS` as a blanket skip for legacy resource linting, keeps fenced examples and the `Resource map` section out of the unmapped-reference scan, improves the unmapped-resource diagnostic, adds table-driven failure cases for ordinary conditional loading wording, adds false-positive cases for explicit external ownership and examples, and tests the temporary architecture exception as exact by skill and path. Lifecycle artifacts now return M2 to code-review after the accepted fix.

## Findings

## Finding SRI-M2-CR2

Finding ID: SRI-M2-CR2
Severity: major
Location: `scripts/skill_validation.py:1428`
Evidence: The review-resolution request required the resource lint to suppress a finding only when the surrounding text explicitly identifies the resource as project-provided, repository-root, user-provided, or illustrative, and the conceptual flow evaluated context per reference. The current implementation checks `PUBLISHED_RESOURCE_EXTERNAL_CONTEXT_PATTERN.search(line)` before iterating references, so one external-context phrase suppresses every skill-local-looking reference on the line. A direct fixture command with `Use the user-provided references/external.md and templates/architecture.md when relevant.` validated successfully, even though `templates/architecture.md` is still an unqualified legacy skill-local resource instruction and should be reported. This leaves a false-negative path for the same defect class SRI-M2-CR1 was meant to close.
Required outcome: External ownership or illustrative wording must suppress only the resource reference it actually qualifies, not unrelated unqualified skill-local references on the same instruction line.
Safe resolution path: Move external-context evaluation to the individual reference context. For example, derive a bounded context window around each matched path, suppress only when that context explicitly qualifies that path as project-provided, repository-root, user-provided, or illustrative, and continue checking other references on the same line. Add a regression where a mixed line with `user-provided references/...` plus unqualified `templates/architecture.md` fails for the template path, while the existing explicit external ownership and false-positive fixtures remain green. Rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, selector-selected validation, lifecycle validation, review artifact validation, change metadata validation, and `git diff --check --`.
needs-decision rationale: none

## Checklist coverage

- Spec alignment: concern. The broad allowed-term reuse was removed, but the whole-line external-context skip still violates R49b/R49d for mixed-reference resource-loading instructions.
- Test coverage: concern. The new tests cover single-reference load-condition failures and single-reference external false positives, but they do not cover a line containing both an external resource path and an unqualified legacy skill-local resource.
- Edge cases: concern. Mixed-reference instructions create a false negative where one explicitly external resource hides another unqualified skill-local resource.
- Error handling: pass. The changed diagnostic is actionable and existing mapped-resource class, existence, and containment failure behavior remains intact.
- Architecture boundaries: pass. The diff does not normalize architecture resources, package outputs, or installed trees before M3.
- Compatibility: pass. Canonical skill validation remains compatible with existing project-provided helper wording, and `templates/` is not made an approved resource class.
- Security/privacy: pass. No secrets, credentials, private hostnames, or unsafe logging were introduced.
- Derived artifact currency: pass. No generated artifacts were hand-edited; selector-selected `python scripts/test-build-skills.py` was rerun.
- Unrelated changes: pass. The diff is limited to validator logic, validator tests, fixture evidence, and lifecycle/review state.
- Validation evidence: concern. The recorded validation commands are relevant and passed, but they do not include direct proof for the mixed-reference suppression edge.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M2. Canonical Resource-Integrity Validator and Fixtures
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `SRI-M2-CR2`
Remaining implementation milestones: M2 resolution, M3, M4, M5, M6, M7
Verify readiness: not-claimed

This direct `code-review` invocation stops after recording the review result and lifecycle state. It does not apply the fix.
