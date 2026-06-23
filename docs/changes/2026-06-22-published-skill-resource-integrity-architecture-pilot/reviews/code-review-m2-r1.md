# Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit `3260407`
Status: changes-requested

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r1.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`, `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md`, `docs/plan.md`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml`
- Open blockers: none
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: SRI-M2-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-log.md`
- Review resolution: `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/review-resolution.md`
- Reviewed milestone: M2. Canonical Resource-Integrity Validator and Fixtures
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2 resolution, M3, M4, M5, M6, M7
- Required review-resolution: yes
- Finding IDs: SRI-M2-CR1
- Verify readiness: not-claimed

## Review inputs

- Review surface: commit `3260407` (`M2: validate mapped skill-local resources`).
- Tracked governing branch state: proposal, approved spec amendment, owner-approved test spec, architecture, ADR, active plan, M1 audit, M1 code-review, and M2 implementation evidence are tracked on the branch.
- Governing artifacts: `specs/skill-contract.md` R46-R49d, R53-R53b, R54-R54a; `specs/skill-contract.test.md` T42-T43; `docs/plans/2026-06-23-published-skill-resource-integrity-architecture-pilot.md` M2.
- Validation evidence: M2 validation entries in `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/change.yaml` and the active plan validation notes.
- Implementation files reviewed: `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/validator-fixtures.md`, active plan state, and change metadata.

## Diff summary

M2 adds generic resource-map entry parsing and validation for mapped skill-local resources. It checks `COPY`, `READ`, and `RUN` entries for approved resource classes, skill-root containment, and canonical file existence. It also adds bounded unmapped skill-local reference lint, a temporary architecture migration exception for the known `templates/...` references recorded by M1, validator tests for the new behavior, fixture-coverage evidence, and lifecycle handoff state for M2 review.

## Findings

## Finding SRI-M2-CR1

Finding ID: SRI-M2-CR1
Severity: major
Location: `scripts/skill_validation.py:1384`
Evidence: R49b requires bounded migration lint to examine recognized resource-loading instructions with approved skill-local prefixes, including legacy `templates/`. T43 specifically requires a legacy `templates/...` resource-loading instruction outside the Resource map to be detected while avoiding broad false positives. The implementation skips any matching line that contains any term from `PUBLISHED_ALLOWED_PROJECT_LOCAL_TERMS`, including broad terms such as `when relevant`, `when available`, and `when those paths are the target`. As a result, a line such as `Use templates/architecture.md when relevant.` contains the recognized loading verb `Use`, the legacy skill-local prefix `templates/`, and a broad allowed term, so it is skipped rather than reported. The current positive legacy test only covers `Use templates/architecture.md for the output skeleton` and does not prove this common resource-loading wording.
Required outcome: Bounded legacy-resource lint must still report recognized skill-local resource-loading instructions when they include ordinary load-condition wording such as `when relevant` or `when available`. False-positive avoidance must be narrower than reusing the full repository-root dependency guard-term list.
Safe resolution path: Replace the broad `PUBLISHED_ALLOWED_PROJECT_LOCAL_TERMS` skip in `_iter_unmapped_skill_local_resource_references` with resource-lint-specific false-positive boundaries, such as project-provided helper wording, artifact/example wording, customer-project data wording, or other explicitly tested non-resource contexts. Add a regression fixture where `Use templates/architecture.md when relevant.` fails with the unmapped legacy resource diagnostic. Rerun `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, selector-selected validation, artifact lifecycle validation, change metadata validation, review artifact validation, and whitespace checks.
needs-decision rationale: none

## Checklist coverage

- Spec alignment: concern. Explicit mapped-resource validation aligns with R47-R48b, but the broad guard-term skip can miss recognized legacy resource-loading instructions required by R49b/R49d.
- Test coverage: concern. The new tests cover verb/class mismatches, missing resources, containment, `templates/` class rejection, one legacy positive case, false-positive examples, and the architecture exception, but they do not cover a common `Use templates/... when relevant` loading sentence that the implementation currently skips.
- Edge cases: concern. False-positive examples are covered, but broad allowed-term suppression creates a false negative edge case for load-condition wording.
- Error handling: pass. Invalid mapped path, absolute path, missing file, and wrong verb/class paths fail closed with deterministic diagnostics.
- Architecture boundaries: pass. M2 does not normalize architecture resources; it preserves the reviewed M1 temporary architecture debt until M3.
- Compatibility: pass. Existing packaged-script and plan-asset validation behavior is retained, and canonical `validate-skills.py` remains green through the temporary architecture exception.
- Security/privacy: pass. No secrets, credentials, tokens, or private data are introduced; diagnostics use repository paths and fixture paths.
- Derived artifact currency: pass. Selector-selected `skills.generation_regression` ran via `python scripts/test-build-skills.py`; no generated output is checked in.
- Unrelated changes: pass. The diff is scoped to validator logic, validator tests, M2 fixture evidence, and lifecycle state.
- Validation evidence: concern. Recorded commands are relevant and passed, but the tests do not prove the skipped `when relevant` legacy-loading case.

## No-finding rationale

Not applicable; one material finding was found.

## Handoff

Reviewed milestone: M2. Canonical Resource-Integrity Validator and Fixtures
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `SRI-M2-CR1`
Remaining implementation milestones: M2 resolution, M3, M4, M5, M6, M7
Verify readiness: not-claimed

This direct `code-review` invocation stops after recording the review result and lifecycle state. It does not apply the fix.
