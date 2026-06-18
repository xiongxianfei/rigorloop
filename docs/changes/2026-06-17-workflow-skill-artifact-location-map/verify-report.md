# Verify Report: Workflow Skill Artifact-Location Map

## Result

- Skill: verify
- Status: completed
- Artifacts changed: `verify-report.md`, `change.yaml`, active plan, `docs/plan.md`
- Open blockers: none
- Next stage: pr
- Validation: passed local selected verification across the full branch change surface
- Readiness: branch-ready; PR body/open readiness not claimed

## Verdict

The branch is ready for PR handoff. The workflow guide, skill text, validator implementation, regression tests, lifecycle artifacts, review records, behavior-preservation evidence, and explain-change artifact are coherent with the approved workflow skill artifact-location map contract.

Hosted CI has not been observed by this local verify run.

## Traceability

| Requirement set | Test IDs | Files changed | Evidence | Status |
| --- | --- | --- | --- | --- |
| R1-R5 workflow-map ownership and stage-skill boundary | T1, T2 | `docs/workflows.md`, `skills/workflow/SKILL.md` | Workflow skill and guide define map ownership, refresh triggers, and stage-skill content ownership. | pass |
| R6-R15 registry and Markdown projection | T3-T8, T15 | `docs/workflows.md`, `scripts/skill_validation.py`, `scripts/test-skill-validator.py` | YAML registry, Markdown projection, PR handoff representation, architecture/ADR entries, and registry/table validation are present. | pass |
| R16-R20 plan-surface contract | T9, T14 | `docs/workflows.md`, `skills/workflow/SKILL.md`, `skills/plan/SKILL.md`, `docs/plan.md` | `docs/plan.md` remains index-only and detailed plan bodies remain under `docs/plans/YYYY-MM-DD-slug.md`. | pass |
| R21-R25 workflow defaults and stage-skill drift | T9, T10, T15 | `skills/workflow/SKILL.md`, `skills/plan/SKILL.md`, validators | Workflow defaults match the registry; directly affected stage-skill contradiction checks are covered. | pass |
| R26-R34 source-rank and portability | T11 | `docs/workflows.md`, `skills/workflow/SKILL.md` | Explicit path/source-rank behavior and portable-default fallback are documented and validated. | pass |
| R35-R41 formal review placement and learn-session non-authority | T12, T14 | `docs/workflows.md`, review records, `behavior-preservation.md` | Formal reviews route under `docs/changes/<change-id>/reviews/`; learn sessions are not live routing authority. | pass |
| R42-R47 validation and drift detection | T3-T13, T15 | `scripts/skill_validation.py`, `scripts/test-skill-validator.py` | Validator rejects malformed registries, table drift, stale plan paths, invalid review paths, unknown artifact inputs, and affected skill drift. | pass |
| R48, R52 adapter proof and generated-output boundary | T16 | `skills/workflow/SKILL.md`, adapter validation scripts | `build-skills --check`, build-skill regression, and adapter archive smoke passed; no generated public adapter output was hand-edited. | pass |
| R49-R53 cold-read proof and behavior preservation | T14-T16 | `behavior-preservation.md`, `explain-change.md`, lifecycle artifacts | Cold-read answers, lifecycle/schema preservation, portability, and generated-output boundaries are recorded. | pass |

## Verification Dimensions

| Dimension | Result | Evidence |
| --- | --- | --- |
| Spec coverage | pass | Implemented behavior maps to the approved workflow artifact-location map spec and accepted proposal direction. |
| Requirement satisfaction | pass | All R1-R53 requirement groups have direct tests, validator checks, manual proof, or selected CI evidence. |
| Test coverage | pass | `scripts/test-skill-validator.py` covers registry/default-path behavior and validator failures; `behavior-preservation.md` covers the manual cold-read proof. |
| Test validity | pass | Negative fixtures remove entries, introduce stale paths, route reviews outside the change pack, and supply unknown artifact types. |
| Architecture coherence | pass | No runtime architecture or ADR change is required; the approved plan classifies this as governance, skill text, and validation behavior. |
| Artifact lifecycle state | pass | Review-resolution is closed, review-log has no open findings, implementation milestones are closed, and explanation is current. |
| Plan completion | pass | `docs/plan.md` and the plan body agree that M3 is closed and this verify stage hands off to PR while the plan remains Active until PR completion. |
| Validation evidence | pass | Final selected CI across the full branch change surface passed all selected checks. |
| Drift detection | pass | Workflow map, skill defaults, stage-skill placement, generated skill output, and adapter archive drift checks passed. |
| Risk closure | pass | Plan-location, review-location, portability, generated-output, and historical-migration risks are addressed or explicitly out of scope. |
| Release readiness | pass | Local branch state is branch-ready for PR handoff; hosted CI remains a PR-stage observation. |

## Commands Run

Working directory:
`/home/xiongxianfei/data/20260419-rigorloop`

| Command | Result |
| --- | --- |
| `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-06-17-workflow-skill-artifact-location-map` | pass; reviews=9, findings=7, log_entries=9, resolution_entries=7 |
| `python scripts/validate-change-metadata.py docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml` | pass |
| `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/explain-change.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-log.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/review-resolution.md` | pass; validated 3 artifact files |
| `bash scripts/ci.sh --mode explicit ...` across the full branch change surface | pass; selected checks passed |
| `bash scripts/ci.sh --mode explicit ...` for the final verify-report state | pass; selected checks passed |
| `bash scripts/ci.sh --mode explicit --path skills/workflow/SKILL.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/behavior-preservation.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/verify-report.md` | pass after published workflow skill wording refinement |
| `bash scripts/ci.sh --mode explicit --path skills/workflow/SKILL.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/behavior-preservation.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/verify-report.md --path docs/changes/2026-06-17-workflow-skill-artifact-location-map/change.yaml --path docs/plans/2026-06-18-workflow-skill-artifact-location-map.md --path docs/plan.md` | pass after recording PR-open lifecycle state |

Full branch-surface selected CI passed these check IDs:

```text
skills.validate
skills.regression
skills.generation_regression
skills.drift
adapters.drift
review_artifacts.validate
artifact_lifecycle.validate
change_metadata.regression
change_metadata.validate
selector.regression
```

Final verify-report selected CI passed these check IDs:

```text
review_artifacts.validate
artifact_lifecycle.validate
change_metadata.regression
change_metadata.validate
```

Post-PR workflow skill wording refinement selected CI passed these check IDs:

```text
skills.validate
skills.regression
skills.generation_regression
skills.drift
adapters.drift
artifact_lifecycle.validate
change_metadata.regression
change_metadata.validate
```

Final PR-open lifecycle selected CI passed the same check IDs after updating the active plan and plan index.

## CI Status

Local selected CI passed. Hosted CI was not observed during this local verify run and must be observed after PR handoff.

## Artifact Drift

No blocking artifact drift found.

`verify` found and fixed stale readiness text in the active plan tail before recording branch-ready. The plan body and `docs/plan.md` now agree that M3 is closed and the next stage is PR handoff.

## Remaining Risks

- Hosted CI still needs to run after PR handoff.
- PR body/open readiness belongs to the `pr` stage.
- Future artifact classes must update the YAML registry, Markdown projections, workflow skill defaults, and validator fixtures together.

## Readiness

Branch-ready: yes.

PR handoff: PR #99 is open.

Next stage: hosted CI and human review.

This report does not claim hosted CI success, merge readiness, or final lifecycle Done.
