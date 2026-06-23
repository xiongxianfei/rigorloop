# Verify Report: Evidence-Bound and Incremental Project Map Skill

Verify ID: verify-r1
Stage: verify
Change ID: 2026-06-23-evidence-bound-incremental-project-map
Verified artifact: branch working tree at `42b8650a`
Verify date: 2026-06-23
Status: branch-ready with warning
Hosted CI status: not observed

## Result

- Skill: verify
- Status: completed
- Open blockers: none
- Next stage: pr
- Validation: passed locally
- Readiness: branch-ready for the project-map change surface
- PR readiness: not-claimed

## Scope

This verification covers the evidence-bound `project-map` skill change:

- accepted proposal, approved spec, approved test spec, corrected architecture package, active plan, explain-change artifact, review records, and change metadata;
- canonical `project-map` skill text and packaged skeleton asset;
- skill validator helpers, selector routing, fixture coverage, representative proof, cold-read proof, behavior-preservation proof, and generated-output proof;
- temporary adapter archive generation and validation from canonical sources.

This verification excludes the unrelated untracked learn session at `docs/learn/sessions/2026-06-23-plan-status-surfaces-root-cause.md`.

## Traceability

| Requirement group | Test spec coverage | Evidence | Status |
| --- | --- | --- | --- |
| R1-R15 published skill role, modes, and placement | TS-PMAP-001 through TS-PMAP-006 | `skills/project-map/SKILL.md`, `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py` | pass |
| R16-R29 map metadata, freshness, correction notes, and refresh behavior | TS-PMAP-007 through TS-PMAP-011 | `behavior-preservation.md`, `representative-project-map-outputs.md`, selected CI lifecycle checks | pass |
| R30-R48 evidence classes, material claims, source-rank, commands, and flow evidence | TS-PMAP-012 through TS-PMAP-021 | `scripts/skill_validation.py`, project-map fixtures, representative outputs | pass |
| R49-R57 root and area map relationship | TS-PMAP-022 through TS-PMAP-026 | skeleton asset, representative root/area output proof, canonical validation | pass |
| R58-R71 skeleton, resource map, and diagram contract | TS-PMAP-027 through TS-PMAP-034 | `assets/project-map-skeleton.md`, `Resource map`, C4 container update, validator checks | pass |
| R72-R84 downstream reliance, no migration, generated output, and cold-read proof | TS-PMAP-035 through TS-PMAP-042 | `cold-read-proof.md`, `generated-output-proof.md`, temporary adapter archive validation | pass |

## Verification Dimensions

| Dimension | Result | Evidence |
| --- | --- | --- |
| Spec coverage | pass | Implemented surfaces map to the approved spec and test spec requirement groups. |
| Requirement satisfaction | pass | Canonical skill text, skeleton asset, fixtures, representative proof, generated proof, and cold-read proof cover the first slice. |
| Test coverage | pass | Skill validator, selector, generated-skill, adapter, review-artifact, lifecycle, change-metadata, and selected CI checks passed. |
| Test validity | pass | Negative fixtures assert expected diagnostics instead of leaving committed red tests. |
| Architecture coherence | pass | Building Block View and C4 container diagram represent Project maps as a first-class repository artifact container. |
| Artifact lifecycle state | pass | Reviews are recorded, material findings are resolved, explain-change is recorded, and plan/index state now points to `pr`. |
| Plan completion | pass | M1 through M4 are closed and no in-scope implementation milestone remains. |
| Validation evidence | pass | Direct commands and selected CI wrapper output passed locally. |
| Drift detection | pass | Generated skill mirrors and temporary adapter archives were validated from canonical sources. |
| Risk closure | pass | Existing project maps were not automatically migrated; generated adapter output was not hand-edited. |
| Release readiness | pass | Branch is ready for PR handoff based on local validation; hosted CI is not claimed. |

## Validation Commands

Run from `/home/xiongxianfei/data/20260419-rigorloop` on 2026-06-23:

```bash
python scripts/query-change-record.py 2026-06-23-evidence-bound-incremental-project-map summary
python scripts/validate-review-artifacts.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/
python scripts/validate-change-metadata.py docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/test-select-validation.py
rm -rf /tmp/rigorloop-project-map-adapter-proof && python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-project-map-adapter-proof
python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-project-map-adapter-proof
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md --path specs/project-map.md --path specs/project-map.test.md --path docs/architecture/system/architecture.md --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/explain-change.md
bash scripts/ci.sh --mode explicit --path docs/proposals/2026-06-23-evidence-bound-incremental-project-map.md --path specs/project-map.md --path specs/project-map.test.md --path docs/architecture/system/architecture.md --path docs/architecture/system/diagrams/container.mmd --path docs/plan.md --path docs/plans/2026-06-23-evidence-bound-incremental-project-map.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/change.yaml --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-log.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/review-resolution.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/validator-fixtures.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/behavior-preservation.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/representative-project-map-outputs.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/cold-read-proof.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/generated-output-proof.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/explain-change.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/verify-report.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/proposal-review-r1.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/spec-review-r1.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/architecture-review-r1.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/architecture-review-r2.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/architecture-review-r3.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r1.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r2.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r3.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r4.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r5.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/plan-review-r6.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m1-r1.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m2-r1.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m3-r1.md --path docs/changes/2026-06-23-evidence-bound-incremental-project-map/reviews/code-review-m4-r1.md --path skills/project-map/SKILL.md --path skills/project-map/assets/project-map-skeleton.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path scripts/validation_selection.py --path scripts/test-select-validation.py --path tests/fixtures/skills/project-map-contract/valid/SKILL.md --path tests/fixtures/skills/project-map-contract/valid/assets/project-map-skeleton.md
git diff --check --
```

All commands passed.

The final explicit CI wrapper selected and passed these checks:

- `skills.validate`
- `skills.regression`
- `skills.generation_regression`
- `skills.drift`
- `adapters.drift`
- `review_artifacts.validate`
- `artifact_lifecycle.validate`
- `change_metadata.regression`
- `change_metadata.validate`
- `guide_system.validate`
- `selector.regression`

## Manual Proof

Temporary adapter archive validation passed for `/tmp/rigorloop-project-map-adapter-proof`.

Direct archive inspection confirmed that each supported adapter archive contains the skeleton asset:

- `rigorloop-adapter-claude-v0.3.2.zip`: `.claude/skills/project-map/assets/project-map-skeleton.md`
- `rigorloop-adapter-codex-v0.3.2.zip`: `.agents/skills/project-map/assets/project-map-skeleton.md`
- `rigorloop-adapter-opencode-v0.3.2.zip`: `.opencode/skills/project-map/assets/project-map-skeleton.md`

## CI Status

Hosted CI was not observed in this stage. This verify report claims local branch-ready evidence only.

## Drift Assessment

No blocking drift found.

- `docs/plan.md` and the active plan agree that verify completed and `pr` is next.
- `review-resolution.md` is closed with no unresolved findings.
- `review-log.md` has no open material findings.
- `change.yaml` indexes the current proposal, spec, test spec, architecture, plan, explain-change, generated-output proof, and verify evidence.
- Generated local skill output and temporary adapter output were validated from canonical `skills/`.
- Existing `docs/project-map.md` and tracked adapter support surfaces were not changed by this work.

## Remaining Risks

- Hosted CI may still fail after PR opens; that status is not claimed here.
- An unrelated untracked learn-session file remains outside this verified change surface and should not be folded into the PR unless intentionally scoped.

## Handoff

Branch-ready for `pr`.
