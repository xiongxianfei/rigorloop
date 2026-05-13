# Plan Review R1

Review ID: plan-review-r1
Stage: plan-review
Round: 1
Reviewer: Codex plan-review
Target: docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md
Reviewed artifact: docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md
Review date: 2026-05-13
Recording status: recorded
Status: changes-requested

## Review inputs

- Plan: `docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md`
- Plan index: `docs/plan.md`
- Proposal: `docs/proposals/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md`
- Spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`
- Architecture: `docs/architecture/system/architecture.md`
- Related ADR: `docs/adr/ADR-20260512-generated-skill-output-release-artifacts.md`
- Proposal review evidence: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md`
- Spec review evidence: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/spec-review-r1.md`
- Architecture review evidence: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/architecture-review-r1.md`
- Governance and workflow: `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`

## Findings

### PR-001: M5 token benchmark validation command uses a non-existent CLI option

Finding ID: PR-001
Severity: major
Location: `docs/plans/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release.md`, line 312.

Evidence: M5 lists `python scripts/run-token-cost-benchmarks.py --version v0.1.2` as a required validation command. The current runner help exposes `--release RELEASE` and does not expose `--version`. M5 does not list `scripts/run-token-cost-benchmarks.py` as a likely touched component or a planned CLI change, so an implementer following the plan would hit a predictable command failure during final release-readiness validation.

Required outcome: The plan must name an executable token benchmark command or explicitly add a benchmark-runner CLI change to the implementation scope and tests.

Safe resolution: Update M5 to use the existing runner shape, for example `python scripts/run-token-cost-benchmarks.py --release v0.1.2 --suite benchmarks/token-cost/manifest.yaml --tool codex --output-dir <run-output-dir> --skill-source <public-adapter-skill-source>`, with the skill source pointing at generated public adapter release output or temporary public adapter output rather than `.codex/skills/`. If the implementation instead changes the CLI to support `--version`, add `scripts/run-token-cost-benchmarks.py` and matching tests to M5's likely touched files and validation scope.

## Review dimensions

| Dimension | Result | Notes |
|---|---|---|
| Self-contained context | pass | The plan names the source artifacts, review evidence, no-map rationale, relevant scripts, adapter surfaces, release evidence paths, and compatibility constraints. |
| Source alignment | pass | Milestones trace to the approved spec and architecture, including the two-release compatibility path and conditional proof-pack move. |
| Milestone size | pass | M1-M5 are reviewable implementation slices; M6 is correctly separated as a later post-release gate. |
| Sequencing | pass | Archive generation precedes metadata, metadata precedes docs/release notes, conditional cleanup is isolated, and final evidence comes last. |
| Scope discipline | pass | Non-goals protect the `v0.1.2` compatibility window, supported adapters, archive file tracking, `.codex/skills/`, optional combined archive, proof-pack condition, and progressive-loading boundary. |
| Validation quality | concern | Most commands and expected observations are explicit, but PR-001 leaves a final token benchmark command non-executable as written. |
| TDD readiness | pass | Each milestone identifies tests or static checks to add before implementation. |
| Risk coverage | pass | Rollback and recovery cover compatibility, archive determinism, metadata reproducibility, proof-pack movement, skill wording, and token-cost tooling. |
| Architecture alignment | pass | The plan follows the canonical architecture and ADR by keeping `skills/` authored, preserving tracked public adapters during the compatibility window, and moving generated archives to release assets. |
| Operational readiness | concern | Release notes, archive validation, metadata, release gate, and token-cost evidence are covered, but the token benchmark command needs correction before test-spec can rely on it. |
| Plan maintainability | pass | Current handoff summary, milestone states, progress, decision log, surprises, validation notes, and remaining gates are present and ready to update. |

## Missing milestones or dependencies

No missing milestones. The only missing dependency detail is the executable token benchmark invocation or a planned runner CLI update for PR-001.

## Suggested edits

- Replace M5 validation command `python scripts/run-token-cost-benchmarks.py --version v0.1.2` with the current runner CLI, including `--release v0.1.2`.
- Include `--suite benchmarks/token-cost/manifest.yaml`, `--tool codex`, `--output-dir <run-output-dir>`, and a public adapter skill source when the final benchmark needs an explicit generated archive or temporary public adapter source.
- If keeping `--version` is intentional, add `scripts/run-token-cost-benchmarks.py` to M5 likely touched files and require tests proving the alias works.

## Outcome

- Review status: changes-requested
- Material findings: PR-001
- Blocking findings: PR-001
- Required plan updates: yes
- Immediate next stage: plan revision and plan-review rerun
- Eventual test-spec readiness: blocked until PR-001 is resolved and a clean plan-review is recorded.
- Implementation readiness: not ready.

## Recommended next stage

Revise the plan, then rerun `plan-review`. This isolated plan-review does not auto-continue into `test-spec`.
