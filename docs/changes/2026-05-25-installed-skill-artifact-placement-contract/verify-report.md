# Verify Report: Installed-Skill Artifact Placement Contract

Verify ID: verify-r1
Stage: verify
Change ID: 2026-05-25-installed-skill-artifact-placement-contract
Verified artifact: branch `proposal/installed-skill-artifact-placement-contract-pr` at `1c4264c`
Verify date: 2026-05-25
Status: branch-ready
Hosted CI status: not observed

## Result

- Skill: verify
- Status: completed
- Open blockers: none
- Next stage: pr
- Validation: passed locally
- Readiness: branch-ready
- PR readiness: not-claimed

## Scope

This verification covers the installed-skill artifact placement contract change:

- validator helpers and tests in `scripts/skill_validation.py` and `scripts/test-skill-validator.py`;
- public skill wording in `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, and `skills/plan/SKILL.md`;
- workflow-map synchronization in `docs/workflows.md`;
- approved spec, test spec, active plan, behavior-preservation proof, explain-change artifact, review records, and change metadata.

## Traceability

| Requirement | Test IDs | Files changed | Evidence | Status |
|---|---|---|---|---|
| R1-R8 | T1, T2 | `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, `scripts/skill_validation.py`, `scripts/test-skill-validator.py` | `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, selected CI `skills.validate`, `skills.regression` | pass |
| R9-R13 | T3, T8 | `skills/proposal-review/SKILL.md`, `skills/spec-review/SKILL.md`, change-local review evidence | Review skills state create/request change pack before recorded status, clean receipt behavior, and isolated advisory carve-out; code-review M2/M3 clean | pass |
| R14-R17 | T4, T5 | `docs/workflows.md`, review skill wording, validator helpers | Workflow-guide per-artifact precedence and portable fallback are stated; workflow drift fixture passes | pass |
| R18-R19 | T6, T8 | `skills/plan/SKILL.md`, validator helpers/tests | Plan-surface helper rejects ambiguous wording and canonical `plan` passes | pass |
| R20-R23 | T4, T7, T11 | `docs/workflows.md`, skill placement blocks, `behavior-preservation.md` | Workflow guide remains secondary; public skills avoid maintainer-only generated-output details; schemas remain outside placement blocks | pass |
| R24-R25 | T9 | Branch diff and change-local evidence | No historical migration, CLI scaffolding, schema rewrite, generated shared partials, or generated adapter package output was introduced | pass |
| R26-R28 | T1, T4, T6 | `scripts/skill_validation.py`, `scripts/test-skill-validator.py` | Deterministic skill-validation checks and selected CI `skills.regression` passed | pass |
| R29 | T10 | `behavior-preservation.md`, generated temporary adapter archives | `build-skills`, `build-adapters`, `validate-adapters`, and exact archive content check passed | pass |
| R30 | T8, T11 | `behavior-preservation.md`, `explain-change.md` | Cold-read proof answers proposal-review, spec-review, and plan-surface questions from installed-skill text | pass |

## Verification Dimensions

| Dimension | Result | Evidence |
|---|---|---|
| Spec coverage | pass | Implemented surfaces map to R1-R30 and AC1-AC12 in the approved spec and test spec. |
| Requirement satisfaction | pass | Tests, canonical validation, generated-output proof, and cold-read proof cover every `MUST` in the first slice. |
| Test coverage | pass | Unit, contract, selected CI, generated-output, lifecycle, and manual cold-read proof are recorded. |
| Test validity | pass | Negative fixtures prove missing paths, missing change-pack behavior, wrong stage-owned record wording, stale workflow rows, and ambiguous plan surfaces fail. |
| Architecture coherence | pass | Plan records architecture as not required; no architecture, persistence, API, or deployment boundary changed. |
| Artifact lifecycle state | pass | Review-resolution is closed, review artifacts validate, and plan/index state now points to `pr`. |
| Plan completion | pass | M1, M2, and M3 are closed; explain-change is recorded; no implementation milestone remains. |
| Validation evidence | pass | Direct commands and selected CI wrapper output passed locally. |
| Drift detection | pass | Skill/workflow drift checks and generated skill/adapters checks passed. |
| Risk closure | pass | Non-goals are preserved; generated output is temporary; no schema/status/migration/CLI scope expansion. |
| Release readiness | pass | Branch is ready for PR handoff based on local validation; hosted CI is not claimed. |

## Validation Commands

Run from `/home/xiongxianfei/data/20260419-rigorloop` on 2026-05-25:

```bash
python scripts/test-skill-validator.py
python scripts/validate-skills.py
python scripts/build-skills.py --check
rm -rf /tmp/rigorloop-verify-installed-skill-adapters && mkdir -p /tmp/rigorloop-verify-installed-skill-adapters && python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-verify-installed-skill-adapters && python scripts/validate-adapters.py --root /tmp/rigorloop-verify-installed-skill-adapters --version v0.1.5
python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-05-25-installed-skill-artifact-placement-contract
python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-25-installed-skill-artifact-placement-contract
python scripts/validate-change-metadata.py docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/installed-skill-artifact-placement-contract.md --path specs/installed-skill-artifact-placement-contract.test.md --path docs/workflows.md --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-log.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/review-resolution.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/behavior-preservation.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/explain-change.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md
git diff --check -- scripts/skill_validation.py scripts/test-skill-validator.py skills/proposal-review/SKILL.md skills/spec-review/SKILL.md skills/plan/SKILL.md docs/workflows.md specs/installed-skill-artifact-placement-contract.md specs/installed-skill-artifact-placement-contract.test.md docs/changes/2026-05-25-installed-skill-artifact-placement-contract docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md docs/plan.md
bash scripts/ci.sh --mode explicit --path scripts/skill_validation.py --path scripts/test-skill-validator.py --path skills/proposal-review/SKILL.md --path skills/spec-review/SKILL.md --path skills/plan/SKILL.md --path docs/workflows.md --path specs/installed-skill-artifact-placement-contract.md --path specs/installed-skill-artifact-placement-contract.test.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/change.yaml --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/explain-change.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/behavior-preservation.md --path docs/changes/2026-05-25-installed-skill-artifact-placement-contract/verify-report.md --path docs/plans/2026-05-25-installed-skill-artifact-placement-contract.md --path docs/plan.md
```

All commands passed.

The explicit CI wrapper selected and passed these checks:

- `skills.validate`
- `skills.regression`
- `skills.generation_regression`
- `skills.drift`
- `adapters.drift`
- `artifact_lifecycle.validate`
- `change_metadata.regression`
- `change_metadata.validate`
- `selector.regression`

## Manual Proof

Exact archive content check passed for:

- `/tmp/rigorloop-verify-installed-skill-adapters/rigorloop-adapter-codex-v0.1.5.zip`
- `/tmp/rigorloop-verify-installed-skill-adapters/rigorloop-adapter-claude-v0.1.5.zip`
- `/tmp/rigorloop-verify-installed-skill-adapters/rigorloop-adapter-opencode-v0.1.5.zip`

The check confirmed that each archive contains the revised `proposal-review`, `spec-review`, and `plan` skill paths recorded in `behavior-preservation.md`.

## CI Status

Hosted CI was not observed in this stage. This verify report claims local branch-ready evidence only.

## Drift Assessment

No blocking drift found.

- `docs/plan.md` and the active plan agree that verify completed and `pr` is next.
- `review-resolution.md` is closed with 0 unresolved findings.
- `review-log.md` has no open material findings.
- `change.yaml` indexes the current spec, test spec, plan, explain-change, behavior-preservation, and verify evidence.
- Generated adapter output was validated from canonical `skills/` into `/tmp`; no generated archive output is tracked.

## Remaining Risks

- Hosted CI may still fail after PR opens; that status is not claimed here.
- This first slice updates only `proposal-review`, `spec-review`, and required `plan` wording. Other review skills remain follow-up scope.
- A future reusable archive-content checker could replace the manual Python archive check if this proof becomes recurring.

## Handoff

Branch-ready for `pr`.
