# Plan Review R1: Target-Native Init Commands

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: `docs/plans/2026-05-24-target-native-init-commands.md`
Status: changes-requested

## Review Inputs

- Plan: `docs/plans/2026-05-24-target-native-init-commands.md`
- Plan index: `docs/plan.md`
- Accepted proposal: `docs/proposals/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement.md`
- Approved spec: `specs/target-native-init.md`
- Approved architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260524-target-native-init-state-boundary.md`
- Architecture review: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/architecture-review-r1.md`
- Release verification script: `scripts/release-verify.sh`

## Result

- Skill: plan-review
- Review status: changes-requested
- Material findings: `TNI-PLR1-F1`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/reviews/plan-review-r1.md`
- Review log: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-log.md`
- Review resolution: `docs/changes/2026-05-24-target-native-init-commands-and-adapter-terminology-retirement/review-resolution.md`
- Open blockers: `TNI-PLR1-F1`
- Immediate next stage: plan revision
- No automatic downstream handoff: this review is isolated and does not start test-spec or implementation.

## Findings

## Finding TNI-PLR1-F1

Finding ID: TNI-PLR1-F1
Severity: major
Location: `M3. Release, Docs, And Package Validation Hardening`, validation commands; `Validation plan`.
Evidence: The plan requires `bash scripts/release-verify.sh v0.3.0 --release-output-dir <release-output-dir> --release-commit <commit>`. The current `scripts/release-verify.sh` usage is `bash scripts/release-verify.sh <release-tag>`, sets `release_version="${1:-${GITHUB_REF_NAME:-}}"`, and reads release artifacts through `RELEASE_OUTPUT_DIR` and `RELEASE_COMMIT` environment variables. It does not parse `--release-output-dir` or `--release-commit`, so the planned command's extra arguments would be ignored unless the implementation also adds and tests a new option parser.
Required outcome: Make the release verification command in the plan match the supported or explicitly planned `release-verify.sh` interface before test-spec or implementation relies on it.
Safe resolution path: Either revise the plan to use the existing interface, for example `RELEASE_OUTPUT_DIR=<release-output-dir> RELEASE_COMMIT=<commit> bash scripts/release-verify.sh v0.3.0`, or add an explicit M3 implementation step and tests that extend `release-verify.sh` to support `--release-output-dir` and `--release-commit` before listing that syntax as a validation command. Keep the command version-scoped to `v0.3.0` and preserve the packed-package pre-publish smoke requirement.
needs-decision rationale: none

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Self-contained context | pass | The plan identifies upstream proposal, spec, architecture, ADR, change metadata, relevant implementation surfaces, and current handoff state. |
| Source alignment | pass | Milestones map to the approved target-native syntax, removed `--adapter`, install-only default, `--write-state`, state safety, and release-smoke requirements. |
| Milestone size | pass | M1 through M4 split parser/state schema, verified install/state safety, release/docs validation, and lifecycle closeout into reviewable slices. |
| Sequencing | pass | The plan correctly waits for plan-review and test-spec before implementation, and delays release validation until CLI behavior and package artifacts exist. |
| Scope discipline | pass | Deferred internal adapter path/archive renames remain out of scope, while user-visible CLI and state-file keys are in scope. |
| Validation quality | concern | Most validation commands are appropriate, but the final `release-verify.sh` command uses an unsupported argument shape. |
| TDD readiness | pass | The plan names concrete parser, dry-run, state schema, safety, archive verification, package smoke, and docs tests for the test spec to formalize. |
| Risk coverage | pass | Risks cover parser concentration, adapter terminology drift, packed smoke cost, state parsing over-acceptance, and live post-publish evidence limits. |
| Architecture alignment | pass | The plan follows the architecture boundary between public target terminology, internal adapter compatibility names, optional state writes, and state safety reads. |
| Operational readiness | concern | Release gate reproducibility is blocked until the release-verify invocation is corrected or the script interface is intentionally expanded. |
| Maintainability | pass | The implementation guidance favors version-scoped release validation and conservative state parsing instead of broad internal renames. |

## Readiness

Not ready for test-spec or implementation until `TNI-PLR1-F1` is resolved and plan-review is rerun.
