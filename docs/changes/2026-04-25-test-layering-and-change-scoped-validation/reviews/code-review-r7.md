# Code Review R7

Review ID: code-review-r7
Stage: code-review
Round: 7
Reviewer: Codex code-review skill
Target: Post-PR CI fix range `b8d2530..569b5c9`
Status: clean-with-notes

## Scope

Reviewed the hosted-PR-CI fix that maps previously blocking governance and handoff paths to deterministic selector checks. The review covered selector routing, regression coverage, lifecycle validation context, plan/change metadata updates, and explain-change updates.

## Review inputs

- Diff range: `b8d2530..569b5c9`
- Review surface: `scripts/validation_selection.py`, `scripts/test-select-validation.py`, `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/change.yaml`, `docs/changes/2026-04-25-test-layering-and-change-scoped-validation/explain-change.md`, and `docs/plans/2026-04-25-test-layering-and-change-scoped-validation.md`
- Tracked governing branch state: proposal, spec, architecture, test spec, active plan, review records, verify evidence, and explain-change artifact are present in tracked branch commits
- Spec: `specs/test-layering-and-change-scoped-validation.md`
- Test spec: `specs/test-layering-and-change-scoped-validation.test.md`
- Architecture: `docs/architecture/2026-04-25-test-layering-and-change-scoped-validation.md`
- Plan milestone: post-PR CI handoff correction under the completed validation selector plan
- Validation evidence inspected: `python scripts/test-select-validation.py`, targeted `bash scripts/ci.sh --mode explicit ...`, `bash scripts/ci.sh --mode pr --base origin/main --head HEAD`, change metadata validation, lifecycle validation, review artifact closeout validation, and whitespace validation all passed locally.

## Diff summary

The fix prevents hosted PR CI from stopping on governed surfaces that are in the approved first slice but previously lacked deterministic selected checks. It maps CI workflow, workflow guidance, governance, template, schema, release-script, plan-index, and change-local explain-change paths to repository-owned checks. It also ensures plan-index and change-local lifecycle routing include related change metadata so artifact lifecycle validation validates real artifacts instead of reporting a zero-artifact no-op.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Notes |
| --- | --- | --- |
| Spec alignment | pass | The fix preserves the non-fail-open rule by selecting deterministic checks for first-slice governance paths and still blocking unsupported paths. |
| Test coverage | pass | `test_pr_handoff_surfaces_select_deterministic_checks` and the expanded representative category table cover the hosted-CI blocking paths. |
| Edge cases | pass | `docs/plan.md` alone still requires manual routing, while `docs/plan.md` with related plan/change context selects artifact lifecycle validation. |
| Error handling | pass | Unsupported paths still enter blocking flow; no partial execution is introduced for blocked selector output. |
| Architecture boundaries | pass | Routing remains in `scripts/validation_selection.py`; `scripts/ci.sh` remains a wrapper and was not turned into a second selector. |
| Compatibility | pass | Hosted PR CI can consume selector output without bypassing the selector or forcing broad smoke as the only PR path. |
| Security/privacy | pass | The fix does not execute selector JSON commands directly and does not add secrets, credentials, or external data. |
| Generated output drift | pass | No canonical skill or generated adapter output changed in this fix. |
| Unrelated changes | pass | The diff is scoped to selector routing, selector tests, and matching durable evidence updates. |
| Validation evidence | pass | Local PR-mode wrapper validation passed against `origin/main..HEAD` and selected broad smoke from the active plan/test spec triggers. |

## No-finding rationale

No required-change findings remain because the hosted-CI blocker is resolved through selector-owned routing, the regression suite directly covers the newly routed surfaces, and lifecycle validation now receives governing change metadata for plan-index and change-local handoff surfaces.

## Recommended next stage

Proceed with PR branch update and hosted CI re-check.
