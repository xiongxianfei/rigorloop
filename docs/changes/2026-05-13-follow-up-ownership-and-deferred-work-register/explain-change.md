# Explain Change: Follow-up Ownership and Deferred Work Register

## Summary

This change defines where RigorLoop follow-ups live without making `project-map` a backlog.

The implemented first slice adds the follow-up ownership policy to `docs/workflows.md`, adds concise routing language to `workflow`, adds a concise boundary to `project-map`, and adds static proof that the first slice did not create an empty `docs/follow-ups.md` or a shared follow-up wording template.

## Problem

Deferred work could be scattered across proposals, plans, change artifacts, release reports, learn sessions, project-map risks, chat, and PR comments. The accepted direction was to keep `project-map` focused on repository orientation while routing actionable work to the artifact that can act on it.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | `project-map` orients; `workflow` routes; action-owning artifacts track work; `docs/follow-ups.md` is only for real unowned cross-change follow-ups. |
| Spec | `R1`-`R13a` define workflow-guide ownership, action-owning routing, project-map boundaries, optional register rules, no first-slice shared template, concise skill wording, and affected-surface checks. |
| Plan M1 | Add the ownership table to `docs/workflows.md`, concise wording to `workflow` and `project-map`, and static proof. |
| Plan M2 | Validate lifecycle alignment, keep optional register validation out while no register exists, and record generated-output handling evidence. |
| Code review | `code-review-m1-r1` and `code-review-m2-r1` were both `clean-with-notes` with no material findings. |

Architecture was not required because the change is workflow documentation, skill wording, lifecycle evidence, and validation proof rather than runtime architecture.

## Diff Rationale by Area

| File | Change | Reason | Source | Evidence |
| --- | --- | --- | --- | --- |
| `docs/workflows.md` | Added `Follow-up ownership` table. | Make `docs/workflows.md` the user-facing ownership guide and keep policy out of `project-map`. | `R1`-`R2f`, `R13a`, M1 | `test_follow_up_ownership_m1_workflows_doc_contains_policy_table` |
| `skills/workflow/SKILL.md` | Added short `Follow-up routing` section. | Teach workflow to route future work to the acting artifact and refer to `docs/workflows.md`. | `R4`-`R4d`, `R11a`-`R11b`, M1 | `test_follow_up_ownership_m1_workflow_skill_routes_concisely` |
| `skills/project-map/SKILL.md` | Added short `Follow-up boundary` section. | Preserve `project-map` as orientation and prevent backlog ownership. | `R3`-`R3d`, `R11c`-`R11e`, M1 | `test_follow_up_ownership_m1_project_map_skill_boundary` |
| `scripts/test-skill-validator.py` | Added M1 static tests. | Prove required wording and forbidden first-slice outputs. | Test spec `T1`-`T6`, `T10`, `T12` | `python scripts/test-skill-validator.py` |
| Proposal, spec, test spec, plan, and change-local review files | Added durable lifecycle artifacts and review evidence. | Preserve the approved decision trail and reconstructable workflow state. | Workflow contract and active plan | Review artifact and lifecycle validators |
| `docs/plan.md` and active plan | Updated milestone state from planning through M1/M2 closeout. | Keep the plan index and plan body synchronized. | Plan state contract | lifecycle validation |
| `change.yaml` | Recorded requirements, files, validation, and review outcomes. | Keep compact change metadata current for downstream stages. | Change-local artifact contract | change metadata validation |

## Tests Added or Changed

The implementation added static tests in `scripts/test-skill-validator.py`:

- workflow guide must contain the `Follow-up ownership` policy table;
- `workflow` must contain concise routing wording and not duplicate table content;
- `project-map` must contain concise boundary wording and not duplicate table content;
- `docs/follow-ups.md` must remain absent in the first slice;
- no `templates/shared/*follow*` block may be introduced in the first slice.

This test level is appropriate because the change is documentation, skill behavior, and workflow validation rather than runtime code.

## Validation Evidence Before Final Verify

Passing commands:

- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/select-validation.py --mode explicit --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/project-map/SKILL.md`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/workflows.md --path skills/workflow/SKILL.md --path skills/project-map/SKILL.md`
- `python scripts/test-build-skills.py`
- `python scripts/build-skills.py --check`
- `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives`
- `python scripts/test-select-validation.py`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-05-13-follow-up-ownership-and-deferred-work-register.md --path specs/follow-up-ownership-and-deferred-work-register.md --path specs/follow-up-ownership-and-deferred-work-register.test.md --path docs/plans/2026-05-13-follow-up-ownership-and-deferred-work-register.md --path docs/plan.md --path docs/changes/2026-05-13-follow-up-ownership-and-deferred-work-register/change.yaml`
- `git diff --check --`

Recorded non-applicable checks:

- `python scripts/build-adapters.py --check` failed because it still checks default `0.1.1` tracked adapter tree output.
- `python scripts/build-adapters.py --version v0.1.3 --check` failed because it still expects tracked generated adapter skill bodies and rejects the current manifest command-alias shape.

Those failures are not fixed in this slice because `dist/adapters/README.md` and `dist/adapters/manifest.yaml` define the current `v0.1.3` release-archive support surface: generated public adapter skill bodies are not tracked source. The release-archive adapter regression passed.

## Review Resolution Summary

No material findings were recorded.

Review evidence:

- `proposal-review-r1`: approved
- `spec-review-r1`: approved
- `plan-review-r1`: approved
- `code-review-m1-r1`: clean-with-notes
- `code-review-m2-r1`: clean-with-notes

`review-resolution.md` contains no material findings.

## Alternatives Rejected

- Do not put deferred execution ownership in `project-map`; it would turn an orientation artifact into a backlog.
- Do not create an empty `docs/follow-ups.md`; no qualifying accepted unowned cross-change follow-up exists.
- Do not create a `templates/shared/` block; only two skills need wording in the first slice.
- Do not add register validators before `docs/follow-ups.md` exists; optional register validation is specified for the future register case.

## Scope Control

This change did not create a new workflow stage, a new skill, a shared wording template, an empty follow-up register, or historical follow-up migrations.

It also did not hand-edit generated public adapter package output.

## Risks and Follow-ups

- The adapter tree-output check remains stale for the current `v0.1.3` release-archive model. This is existing validation debt outside this follow-up ownership slice.
- If a real unowned cross-change follow-up is accepted later, create `docs/follow-ups.md` with the specified schema and add lightweight register validation.

## Readiness

All implementation milestones are closed after clean code-review. The next stage is `verify`.
