# Verify Report: Project-Map Skill Simplification

Verification ID: verify-r1
Stage: verify
Verifier: Codex verify
Verification date: 2026-08-14
Status: branch-ready
PR readiness: not claimed

## Result

- Skill: verify
- Status: passed
- Artifacts changed: this report and workflow-owned closeout state
- Open blockers: none for branch readiness
- Next stage: `pr`, not invoked
- Validation: approved CMD1-CMD11 ledger and local PR gate passed
- Readiness: branch-ready
- Hosted CI: configured but not observed for this head

## Scope and verdict

Final verification covered the branch from `origin/main` commit `73770cc939a8c62d13dfd5450d8e47dede8b51aa` through explanation commit `522205d1`. It included the accepted proposal, approved specification and architecture, approved plan and test spec, three closed implementation milestones, final holistic review, closed review resolution, current rationale, canonical package, validators, measurements, and adapter archive/install evidence.

The branch is `branch-ready`. Governing artifacts, lifecycle state, canonical package, tests, preservation evidence, measurements, generated output, adapter parity, and local PR validation agree. This verdict does not claim PR preparation, PR opening, hosted CI success, release readiness, publication, or merge readiness.

## Verification dimensions

| Dimension | Result | Evidence |
| --- | --- | --- |
| Requirements and boundaries | pass | R1-R117, T1-T17, eight boundary dimensions, and five interactions map to deterministic proof and the final package. |
| Universal behavior | pass | Simple root creation retains placement, evidence, freshness, command, reliance, stop, claim, preflight, and result rules inline. |
| Conditional behavior | pass | Refresh, audit, coordination, and recovery load one required reference and cannot be reconstructed when missing. |
| Operation and transaction safety | pass | Target-state rules prevent implicit replacement; area creation is root-bound, registration-last, exact-retry-only, and fail-closed. |
| Structural ownership | pass | The existing skeleton is unchanged and remains the sole structural owner. |
| Semantic and literal preservation | pass | All 24 rules, 15 literals, and 35 scenarios have one closed treatment. |
| Simplification | pass | PMA0, PMA1, representative output, `SKILL.md`, and the total package decrease in words and bytes. |
| Package and drift proof | pass | Canonical, generated, archived, and clean-installed Codex, Claude Code, and opencode resources pass parity validation. |
| Lifecycle coherence | pass | M1-M3 are closed, final code review is clean, review resolution is closed, and explanation matches the reviewed diff. |
| Branch handoff | pass | Local PR-mode CI reports 26 passing direct gates; the next eligible stage is `pr`. |

## Validation evidence

All commands ran locally from the repository root on 2026-08-14.

| Command or proof | Result |
| --- | --- |
| CMD1 preservation-ledger and scenario command | pass; 24 rules, 15 literals, 35 scenarios, unknown values rejected first |
| CMD2 `python scripts/validate-skills.py skills/project-map/SKILL.md` | pass |
| CMD3 focused `ProjectMapSkillSimplificationTests` | pass; 6 tests |
| CMD4 `python scripts/test-skill-validator.py` | pass; 336 tests, 16 documented skips |
| CMD5 `python scripts/test-build-skills.py` | pass; 7 tests |
| CMD6 `python scripts/build-skills.py --check` | pass |
| CMD7 `python scripts/test-adapter-distribution.py` | pass |
| CMD8 temporary `v0.4.0` build and selected `project-map` clean-install validation | pass for Codex, Claude Code, and opencode |
| CMD9 boundary validation | pass |
| CMD10 change-metadata validation | pass before final recording and rerun afterward |
| CMD11 review-structure validation | pass before final recording and rerun afterward |
| `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` | pass at head `522205d1`; 26 direct product and governance gates |
| `git diff --check` | pass before final state recording |

No target-agent runtime, transcript grading, network publication, release action, or scripted manual semantic-review procedure was used or claimed. Ordinary PR review remains the later human judgment surface.

## Measurements

| Metric | Before | Final | Change |
| --- | ---: | ---: | ---: |
| `SKILL.md` words / bytes | 2,297 / 15,545 | 1,610 / 11,727 | -29.91% / -24.56% |
| `PMA0` words / bytes | 2,297 / 15,545 | 1,610 / 11,727 | -29.91% / -24.56% |
| `PMA1` words / bytes | 2,297 / 15,545 | 2,135 / 15,527 | -7.05% / -0.12% |
| Representative write words / bytes | 2,610 / 17,555 | 1,923 / 13,737 | -26.32% / -21.75% |
| Complete package words / bytes | 2,610 / 17,555 | 2,448 / 17,537 | -6.21% / -0.10% |

The mapped-resource count increases from one to two, but both real invocation profiles and the total package become smaller. The small PMA1 byte reduction is visible rather than overstated.

## Residual risk

- PMA1 remains close to its byte baseline because exact area-transaction identity and recovery rules are intentionally explicit.
- The new reference adds one package-parity surface, so existing archive and clean-install checks remain required.
- Hosted CI is unobserved and belongs to the later PR/CI surface.
- Ordinary PR review still owns the final human clarity and semantic-quality judgment requested by the user.

## Readiness

Verdict: `branch-ready`.

The normal next stage is `pr`, but it was not invoked because the armed workflow target completes when this first formal verification result is durably recorded.
