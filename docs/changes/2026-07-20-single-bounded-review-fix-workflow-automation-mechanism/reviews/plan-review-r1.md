# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md
Reviewed artifact: docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md
Review date: 2026-07-21
Recording status: recorded
Status: changes-requested

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: `BRF-PL1`, `BRF-PL2`
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/reviews/plan-review-r1.md
- Review log: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-log.md
- Review resolution: docs/changes/2026-07-20-single-bounded-review-fix-workflow-automation-mechanism/review-resolution.md
- Open blockers: M5 has non-executable and obsolete adapter proof commands; M4 and M5 do not define one atomic public cutover boundary
- Immediate next stage: plan revision

## Review inputs

| Artifact | SHA-256 |
| --- | --- |
| `docs/plans/2026-07-21-single-bounded-review-fix-workflow-automation.md` | `3f5af86c953dd4867506ea488a63fe553d105384c1e5a1b3e1360d53cc096c7d` |
| `specs/single-bounded-review-fix-workflow-automation.md` | `59241a5e4968a0d6ba60f9772eed56ab8b9e79859a0be1c94e7c77840c724070` |
| `docs/architecture/system/architecture.md` | `3ad5871a99f96f86e7beed58137a6eab7fdf235a0a36dd5c25f3ea6899e9dca8` |
| `docs/adr/ADR-20260721-single-bounded-review-fix-workflow-automation.md` | `72f84faada32301b58221e008f7bd90d198bc002e51ffa868e5210b1299bd538` |

The matching test specification does not exist yet. The plan correctly makes clean plan-review and subsequent test-spec settlement prerequisites for implementation.

## Findings

### BRF-PL1 - M5 adapter and selected-CI validation is not executable as written

Finding ID: BRF-PL1
Severity: major
Location: M5 `Validation commands` and the plan-wide `Validation plan`
Evidence: The plan lists `python scripts/build-adapters.py --check`, `python scripts/validate-adapters.py`, and a read-only `python scripts/select-validation.py ...` call at lines 367-370. `validate-adapters.py` requires `--version`, so the listed command exits as a usage error. The repository's active v0.1.3+ adapter contract uses generated release archives rather than tracked adapter skill bodies, and `dist/adapters/manifest.yaml` currently records `v0.1.5`; prior repository evidence records that bare `build-adapters.py --check` follows retired tracked-tree expectations. Finally, `select-validation.py` only selects checks and does not execute them, while `docs/workflows.md` assigns selected-check execution to `bash scripts/ci.sh --mode explicit ...`.
Required outcome: Every M5 closeout command must be a runnable pass/fail gate using the active generated-adapter contract, and the selector-derived check set must actually execute before milestone closure.
Safe resolution path: Replace the bare adapter commands with temporary release-output generation and validation using the manifest version, for example `python scripts/build-adapters.py --version v0.1.5 --output-dir <tmpdir>` followed by `python scripts/validate-adapters.py --root <tmpdir> --version v0.1.5`. Add `python scripts/validate-skills.py` and `python scripts/test-adapter-distribution.py` directly or rely on an explicitly executed selected-CI command that includes them. Replace or supplement the selection-only command with `bash scripts/ci.sh --mode explicit --path ...`. Have the test spec settle whether this high-risk cutover also sets an authoritative broad-smoke requirement.
needs-decision rationale: none; repository-owned adapter and selected-CI command contracts already determine the safe correction.

### BRF-PL2 - M4 and M5 overlap the public workflow cutover without an activation boundary

Finding ID: BRF-PL2
Severity: major
Location: M4 lines 267-322 and M5 lines 324-386
Evidence: M4 connects every stage from proposal review through final verify and lists `skills/workflow/SKILL.md` plus affected stage skills as implementation surfaces. M5 separately owns switching public guidance and aliases to the unified mechanism and again lists `skills/workflow/SKILL.md` and the affected skills. The plan does not say whether M4's skill edits expose the partially migrated engine, whether they are internal interface preparation only, or how users are prevented from entering the new writer before M5 has removed legacy write paths and completed compatibility proof. M4 also combines proposal review, two correction regimes, milestone execution/review, final holistic review, explanation, and verification into one review slice.
Required outcome: The plan must define one atomic public activation milestone and keep every earlier milestone non-public and non-routable, while preserving reviewable implementation slices for authoring/review behavior and implementation/verification behavior.
Safe resolution path: Keep public command semantics in `skills/workflow/SKILL.md`, compatibility alias activation, and retired-writer removal exclusively in the final cutover milestone. Earlier milestones should use an internal test harness or disabled entrypoint and may update stage-owning skills only for non-public stage contracts. Split the current M4 into an authoring/proposal-review correction milestone and an implementation/code-review/final-verification milestone, each independently reviewed, then make the final milestone the sole public/legacy cutover and integration gate. If the owner retains one M4, it must at least state an enforceable disabled-public-entrypoint invariant and separate test/commit boundaries inside that milestone.
needs-decision rationale: none; the accepted architecture already assigns public semantics to the workflow skill and permits an internal repository-local engine boundary before public activation.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Self-contained context | pass | The plan identifies the governing artifacts, current implementation surfaces, state owners, non-goals, and handoff state. |
| Source alignment | pass | Requirement groups, authority boundaries, receipt recovery, migration, review independence, and stop-before-PR behavior align with the approved spec and architecture. |
| Milestone size | concern | M1-M3 are cohesive; M4 spans all stage families and both correction models, making independent review and fault isolation weak. |
| Sequencing | block | M4 and M5 both modify the public workflow surface without defining which milestone activates the unified writer. |
| Scope discipline | pass | External actions, second registries, competing workflow cursors, and premature alias removal remain out of scope. |
| Validation quality | block | M5 includes a command missing a required argument, a known-obsolete adapter proof path, and selection without selected-check execution. |
| TDD readiness | concern | The plan names focused proof areas and correctly blocks implementation until a matching test spec and clean test-spec-review exist; final cutover proof commands must be corrected before the test spec operationalizes them. |
| Risk coverage | concern | Recovery and migration risks are strong; partial public activation is not yet covered as a plan risk or invariant. |
| Architecture alignment | concern | Physical owners match the ADR, but overlapping `skills/workflow/SKILL.md` ownership weakens the architecture's public-semantics boundary during rollout. |
| Operational readiness | block | M5 cannot be closed reliably with its current adapter and CI commands. |
| Plan maintainability | pass | Handoff, progress, decisions, validation notes, closeout fields, and rollback notes are structured and current. |

## Missing milestones or dependencies

- Missing reviewable stage-family boundary between proposal/authoring correction behavior and implementation/final-verification behavior.
- Missing explicit final-cutover dependency that keeps the new engine unreachable through public commands until all legacy-writer and compatibility proof passes.
- Missing runnable generated-adapter and selected-CI execution commands for final cutover.

## Exact suggested edits

1. Split M4 into two independently reviewed implementation milestones:
   - authoring stages, proposal review, proposal correction, and post-proposal authoring;
   - implementation, implementation correction, milestone/final review, explanation, and verification.
2. Make the resulting final cutover milestone the only owner of public `skills/workflow/SKILL.md` command activation, compatibility aliases, and retired-writer removal.
3. Replace the M5 adapter proof with versioned generated-output commands against a temporary directory and execute selected checks through `scripts/ci.sh`.
4. Update the Current Handoff Summary's remaining milestone list if the split changes milestone numbering.

## Recommendation

Revise the plan, record dispositions for `BRF-PL1` and `BRF-PL2`, validate the revised artifact, and rerun `plan-review` before `test-spec` authoring.

This direct review is isolated. It does not edit the reviewed plan, start test-spec, or authorize implementation.
