# Code Review M3 R2

Review ID: code-review-m3-r2
Stage: code-review
Round: 2
Reviewer: Codex code-review skill
Target: M3 verified branch state after `4ace23a`
Status: changes-requested
Review date: 2026-05-04

## Scope

Reviewed the verified M3 branch state after a direct follow-up code-review request, including the M3 implementation, review, and verification commits.

## Review inputs

- Diff range: `HEAD~3..HEAD`
- Review surface: `skills/learn/SKILL.md`, `docs/learn/README.md`, `scripts/test-skill-validator.py`, generated learn skill output, generated public adapter learn skill output, active plan, change metadata, explain-change, review log, review-resolution, and M3 review record.
- Tracked governing branch state: approved proposal, approved spec, active test spec, active plan, M1/M2/M3 commits, change metadata, explain-change, and review artifacts are tracked on the current branch.
- Spec: `specs/learn-artifact-model.md` `R29`.
- Test spec: `specs/learn-artifact-model.test.md` `T7`.
- Plan milestone: `docs/plans/2026-05-04-learn-artifact-model.md` M3.
- Architecture / ADR: not required; M3 is skill guidance, namespace index, generated output, and validation evidence work without runtime architecture impact.
- Validation evidence: selector-selected explicit CI for the M3 surface passed during this review, including skill, adapter, review artifact, lifecycle, and change metadata checks.

## Diff summary

The reviewed M3 branch rewrote the canonical learn skill, added the learn namespace index, added stable skill-validator coverage, refreshed generated outputs, and recorded M3 review and verification state.

## Findings

### CR-M3-R2-F1: learn skill omits the R29 maintainer-driven rule-adoption edge case

Finding ID: CR-M3-R2-F1

Severity: major

Evidence: `specs/learn-artifact-model.md` `R29` requires maintainer-driven rule adoption without accumulated evidence to route to proposal work that may later produce an ADR, not to durable learn capture. `specs/learn-artifact-model.test.md` `T7` requires checking that behavior. The M3 skill names maintainer requests and single-event evidence standards, and it has a generic `direction` route, but it does not state the R29 rule. The M3 skill-validator regression also lacks stable wording for this edge case.

Problem: A maintainer-requested new rule without accumulated evidence could still be treated as durable learn guidance or written into a topic file without proposal review, contrary to the approved evidence standard.

Required outcome: The learn skill must explicitly say that maintainer-driven rule adoption without accumulated evidence is not durable learn capture, must classify as `direction`, and must route to proposal work that may later produce an ADR or other authoritative artifact if accepted. Skill-validator coverage must protect that wording.

Safe resolution: Add the R29 guidance to `skills/learn/SKILL.md`, add stable skill-validator assertions for the edge case, regenerate `.codex/skills/` and public adapter output through repository generators, then rerun skill validation, skill regression, generated-output drift checks, adapter validation, review artifact validation, change metadata validation, lifecycle validation, selector-selected explicit CI, and whitespace validation.

## Checklist coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | concern | `R29` is not explicitly represented in the M3 skill guidance. |
| Test coverage | concern | The stable skill-validator regression does not assert the R29 maintainer-driven rule-adoption wording. |
| Edge cases | concern | `T7` names maintainer-driven rule adoption without accumulated evidence, but the implemented skill does not cover it. |
| Error handling | pass | No invalid-state or command fallback behavior changed in M3. |
| Architecture boundaries | pass | The reviewed diff stays within workflow documentation, skill guidance, selector/test infrastructure, generated output, and lifecycle evidence. |
| Compatibility | pass | The reviewed M3 branch preserves `learn` as periodic or explicitly invoked and does not migrate historical notes or add templates. |
| Security/privacy | pass | Incident guidance avoids committing secrets, credentials, tokens, private keys, private incident data, or unnecessary machine-local details. |
| Generated output drift | pass | Selector-selected CI showed generated skill and adapter outputs were in sync for the reviewed branch. |
| Unrelated changes | pass | The reviewed M3 diff is scoped to learn skill/index/generated output and required evidence updates. |
| Validation evidence | concern | Validation passed, but it did not catch the R29 wording gap because the regression did not cover it. |

## No-finding rationale

Not applicable; one required-change finding was found.

## Residual risks

- M4 final validation and lifecycle closeout remain incomplete. This review applies to the M3 slice only.

## Recommended next stage

Enter `review-resolution` for `CR-M3-R2-F1`, then rerun `code-review` for M3 after the targeted fix.
