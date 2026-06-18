# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Target: specs/workflow-skill-artifact-location-map.md
Reviewed artifact: specs/workflow-skill-artifact-location-map.md
Review date: 2026-06-17
Reviewer: Codex spec-review
Recording status: recorded
Status: changes-requested

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: WFO-SR1, WFO-SR2, WFO-SR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-06-17-workflow-skill-artifact-location-map/reviews/spec-review-r1.md
- Review log: docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md
- Review resolution: docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md
- Open blockers: WFO-SR1, WFO-SR2, WFO-SR3
- Immediate next stage: spec revision
- Eventual test-spec readiness: not-ready
- Stop condition: Resolve WFO-SR1, WFO-SR2, and WFO-SR3 before architecture, plan, test-spec, or implementation reliance.

## Findings

## Finding WFO-SR1

Finding ID: WFO-SR1
Severity: major
Location: `specs/workflow-skill-artifact-location-map.md` R17-R24, Compatibility and migration; `specs/installed-skill-artifact-placement-contract.md` Glossary, E4, R18, AC8
Evidence: The draft spec adopts `docs/changes/<change-id>/plan.md` as the forward canonical workflow-managed change plan path, while the approved installed-skill artifact placement spec still defines the `plan body` as `docs/plans/YYYY-MM-DD-slug.md`, says plan wording should name active plan bodies under `docs/plans/YYYY-MM-DD-slug.md`, and has AC8 requiring plan-related skill wording to distinguish `docs/plans/YYYY-MM-DD-slug.md`. The draft lists that spec as related but does not say whether it amends, supersedes, or must be revised with this contract.
Required outcome: The spec must define how it resolves or amends the existing approved installed-skill artifact placement contract for plan-body location.
Safe resolution path: Add a compatibility section and requirements stating that this spec amends the installed-skill artifact placement contract's plan-body definition and affected requirements/acceptance criteria for new workflow-managed changes, while retaining existing `docs/plans/*.md` as historical or pre-contract artifacts. Add acceptance criteria requiring the implementation slice to update `specs/installed-skill-artifact-placement-contract.md` or explicitly mark its conflicting clauses superseded by this spec.
needs-decision rationale: none

## Finding WFO-SR2

Finding ID: WFO-SR2
Severity: major
Location: R8, R15, Inputs and outputs, Acceptance criteria
Evidence: R8 requires every artifact registry entry to contain exactly one canonical `path`, and R15 requires the registry to include `PR handoff`. The spec never defines the canonical path for PR handoff. The accepted proposal left this as `docs/changes/<change-id>/pr.md` or PR body artifact / project policy, but the spec turns the registry into a single-path contract without choosing the path or defining an exception.
Required outcome: The spec must decide the PR handoff registry representation or explicitly exclude PR handoff from the exactly-one-path registry rule.
Safe resolution path: Either define the canonical PR handoff path, such as `docs/changes/<change-id>/pr.md`, or add a structured exception for PR handoff with a required `external_surface` or `policy` field instead of `path`. Update R8, R15, examples, acceptance criteria, and validator expectations so tests can check the intended behavior without guessing.
needs-decision rationale: none

## Finding WFO-SR3

Finding ID: WFO-SR3
Severity: major
Location: R35-R37, EC3, EC14, Non-goals
Evidence: R35 says formal review records must route under `docs/changes/<change-id>/reviews/`, but R36 and R37 allow proposal-review and spec-review records to be overridden by a safe project-local customization. EC3 from the related approved spec also allows a custom review-record path when safe. The draft does not say whether a custom review path may leave the change pack or whether R35 constrains all safe customizations.
Required outcome: The spec must define the allowed boundary for review-record customization.
Safe resolution path: Clarify that safe project-local customization for formal review records must either remain under the change pack, or explicitly define the conditions under which a custom path outside `docs/changes/<change-id>/reviews/` is allowed despite R35. Update R35-R37, EC3/EC14-style edge cases, and acceptance criteria so validators know whether outside-change-pack paths are valid or forbidden.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
|---|---|---|
| requirement clarity | concern | Most requirements are clear, but PR handoff and review-record customization boundaries are underspecified. |
| normative language | concern | MUST language is mostly testable, but R8/R15 and R35-R37 create conflicting or incomplete obligations. |
| completeness | concern | The spec covers the proposal direction, but does not settle its relationship to the approved installed-skill placement contract. |
| testability | concern | Registry/table and drift checks are testable after revision; PR handoff and customization rules need deterministic expected results. |
| examples | concern | Examples cover the main path, but do not exercise PR handoff or review-record customization boundaries. |
| compatibility | block | The draft conflicts with the already-approved installed-skill placement contract without declaring an amendment or supersession. |
| observability | pass | Validator diagnostics and cold-read proof are named clearly. |
| security/privacy | pass | Explicit paths remain subordinate to governance, security, schema, and privacy constraints. |
| non-goals | pass | Non-goals preserve lifecycle order, schemas, historical plans, CLI scaffolding, portable defaults, and generated-output boundaries. |
| acceptance criteria | concern | Acceptance criteria need coverage for the installed-skill spec amendment, PR handoff representation, and review customization boundary. |

## Eventual test-spec readiness

not-ready

The draft is close, but a test spec would have to guess how to reconcile the approved installed-skill placement spec, what PR handoff path to validate, and whether custom formal-review paths may leave the change pack.

## Stop condition

Material findings WFO-SR1, WFO-SR2, and WFO-SR3 require spec revision before architecture, plan, test-spec, or implementation reliance.

## Recommended spec edits

- Add an explicit amendment/supersession relationship to `specs/installed-skill-artifact-placement-contract.md` for new workflow-managed plan-body placement.
- Decide and specify the PR handoff registry representation.
- Clarify whether safe formal review-record customizations must remain under `docs/changes/<change-id>/reviews/`.

## No-finding statement

Not applicable. This review recorded material findings.
