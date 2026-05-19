# Code Review M3 R1: Assets-First Progressive Disclosure Pilot

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review
Target: commit 5be5f4f30734a30939e165b839b3445c3629b6b8
Status: clean-with-notes
Reviewed artifact: M3. Adapter, Token, And Behavior-Parity Proof
Review date: 2026-05-19
Recording status: recorded

## Result

- Skill: code-review
- Review status: clean-with-notes
- Material findings: none
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/reviews/code-review-m3-r1.md
- Review log: docs/changes/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills/review-log.md
- Review resolution: not-required
- Open blockers: none
- Immediate next stage: final closeout; explain-change is the next closeout gate unless ci-maintenance is separately triggered

## Review inputs

- Diff/review surface: M3 implementation commit `5be5f4f30734a30939e165b839b3445c3629b6b8`.
- Tracked governing branch state: approved spec amendment, approved test-spec amendment, active plan, M3 implementation, change metadata, and M3 validation evidence are tracked.
- Governing artifacts: `specs/skill-contract.md` R43-R45, `specs/skill-contract.test.md` T36, and `docs/plans/2026-05-19-assets-first-progressive-disclosure-pilot-published-skills.md` M3.
- Validation evidence: active plan and change metadata record the failing-before-passing adapter asset test, `python scripts/test-adapter-distribution.py`, `python scripts/build-skills.py --check`, `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m3-adapters-final`, `python scripts/validate-adapters.py --root /tmp/rigorloop-m3-adapters-final --version v0.1.5`, `python scripts/measure-skill-tokens.py --skills-root skills`, `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, change metadata validation, `git diff --check --`, direct archive inspection, and selected CI on selector-compatible paths.

## Diff summary

M3 adds adapter archive packaging for skill-local packaged resource directories, with a fixture and regression test proving an asset file is included in codex, claude, and opencode archives and validated through `validate_adapter_archives`. The commit corrects `assets/plan-skeleton.md` and the `plan` resource-map section list so `Current Handoff Summary` is part of the reviewed full-plan skeleton. It records adapter-packaging, behavior-parity, historical-coverage, and token-cost evidence, then updates the active plan, plan index, and change metadata for M3 handoff.

## Findings

No blocking or required-change findings.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | pass | The reviewed M3 surface addresses R43-R45/T36: generated adapter assets are proven, behavior parity is recorded, historical coverage is split from strict reference parity, and common-path token reduction is recorded at 15.04 percent. No additional `plan` assets, packaged `references/`, or packaged `scripts/` were introduced. |
| Test coverage | pass | `scripts/test-adapter-distribution.py` adds `test_adapter_archives_include_packaged_skill_assets`, which failed before support because the generated codex archive lacked `.agents/skills/portable-with-assets/assets/template.md` and passed after `_packaged_skill_resources` was added. |
| Edge cases | pass | Direct archive inspection evidence confirms all four real `plan` assets are present in codex, claude, and opencode archives; behavior evidence covers required sections, milestone reuse, current handoff summary, decision log, validation, handoff, claim boundaries, and recording discipline. |
| Error handling | pass | Archive validation compares expected names and contents for generated archive entries, so missing packaged assets or drifted asset contents produce validation errors instead of silent omission. |
| Architecture boundaries | pass | The change stays within adapter distribution generation/validation helpers, adapter regression fixtures, canonical `skills/plan`, and change-local evidence. Adapter roots, lockfile behavior, CLI behavior, and generated adapter output are not hand-edited. |
| Compatibility | pass | Packaged resources are copied under each adapter's existing skill root beside `SKILL.md`, preserving install-root compatibility for codex, claude, and opencode. Existing flat skills remain valid because resource copying is conditional on packaged resource directories. |
| Security/privacy | pass | The new fixture and evidence contain structural Markdown only. The implementation reads packaged resources as UTF-8 text from canonical skill directories and introduces no secrets, credentials, private hostnames, or permission bypasses. |
| Derived artifact currency | pass | M3 evidence records `build-skills.py --check`, temporary adapter archive build/validation, and direct archive inspection from canonical `skills/`; no generated public adapter output is tracked or hand-edited. |
| Unrelated changes | pass | The reviewed commit is limited to M3-owned adapter packaging proof, `plan` skeleton/resource-map parity correction, tests, evidence, active plan state, and change metadata. |
| Validation evidence | pass | The active plan and change metadata record the required M3 commands and the selector-compatible CI command. The full adapter distribution suite exits 0 while emitting an existing token-cost diagnostic, and that distinction is recorded. |

## No-finding rationale

The M3 implementation satisfies the final implementation milestone without expanding the published-skill pilot beyond `plan` assets. The adapter distribution code now derives packaged resource files from canonical skill directories and includes them under each included adapter root. The new regression test proves packaged asset inclusion and archive validation on a fixture, while the M3 evidence proves the real four `plan` assets are present in generated codex, claude, and opencode archives. Token evidence clears the required 15 percent common-path reduction and remains below the 10 percent total packaged-content hard cap with rationale for exceeding the 5 percent tolerance. Behavior evidence separates strict contract-era reference parity from historical coverage parity and records milestone asset reuse.

## Residual risks

- The full `python scripts/test-adapter-distribution.py` command still emits the existing stdout diagnostic `token-cost report validation failed: dynamic_runtime.runs: missing required benchmark architecture-review` while exiting 0. This review treats it as recorded residual noise, not a failing M3 validation.
- Final lifecycle closeout is still pending. This clean M3 review closes the implementation milestone only; explain-change, verify, and PR handoff remain separate downstream gates.

## Milestone handoff

- Reviewed milestone: M3. Adapter, Token, And Behavior-Parity Proof
- Review status: clean-with-notes
- Milestone state after review: closed
- Required review-resolution: no
- Remaining in-scope implementation milestones: none
- Next stage: final closeout; explain-change is the next closeout gate unless ci-maintenance is separately triggered
- Final closeout readiness: ready to start final closeout sequence; not Done because explain-change, verify, and PR handoff have not run.
