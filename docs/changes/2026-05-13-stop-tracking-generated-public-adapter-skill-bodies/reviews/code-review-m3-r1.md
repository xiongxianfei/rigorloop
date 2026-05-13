# Code Review M3 Round 1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Target: commit `89fa31b3e83b567b3bc1f2e750ac794c3f9ba2ee`
Reviewed milestone: M3. v0.1.3 release evidence and token-cost reports
Reviewed artifact: commit `89fa31b`
Review date: 2026-05-13
Reviewer: Codex code-review
Recording status: recorded
Status: changes-requested

## Outcome

- Review status: changes-requested
- Material findings: CR-M3-1
- Blocking findings: none
- Review resolution: required

## Review inputs

- Diff/review surface: `git show --stat --oneline HEAD`, `git show --name-only --format=short HEAD`, and focused reads of the v0.1.3 release metadata, token-cost report, runner, validator, tests, and release gate changes.
- Governing spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.md`
- Test spec: `specs/stop-tracking-generated-public-adapter-skill-bodies.test.md`
- Active plan: `docs/plans/2026-05-13-stop-tracking-generated-public-adapter-skill-bodies.md`
- Architecture and workflow guidance: `docs/architecture/system/architecture.md`, `docs/workflows.md`
- Validation evidence recorded in the active plan and rerun by implementation.

## Diff summary

M3 adds `v0.1.3` release evidence under `docs/releases/v0.1.3/`, adapter artifact checksum metadata under `docs/reports/adapter-artifacts/releases/v0.1.3.yaml`, and token-cost Markdown/YAML/run evidence under `docs/reports/token-cost/`.

The implementation updates the token-cost runner and report validator so dynamic public-surface benchmark evidence can use generated public Codex adapter output while rejecting `.codex/skills/` and, for `v0.1.3`, the retired repository-tree source. It also updates `release-verify.sh` so archive releases default the validation commit to the recorded adapter artifact source commit.

## Findings

### CR-M3-1 - Major - v0.1.3 smoke rows claim pass without maintainer smoke evidence

Finding ID: CR-M3-1
Severity: major
Location: `docs/releases/v0.1.3/release.yaml`

Evidence: The stable release metadata marks Codex, Claude Code, and opencode smoke rows as `result: pass`, but each evidence string only cites repository-owned archive validation and a tool-version check:

- Codex evidence says archive validation confirmed `AGENTS.md` and `.agents/skills/`, and `codex --version` was checked.
- Claude evidence says archive validation confirmed `CLAUDE.md` and `.claude/skills/`, and `claude --version` was checked.
- opencode evidence says archive validation confirmed archive structure and command aliases, and `opencode --version` was checked.

The architecture records release evidence as including "maintainer smoke evidence" and says release validation checks "smoke evidence" ([docs/architecture/system/architecture.md](/home/xiongxianfei/data/20260419-rigorloop/docs/architecture/system/architecture.md:138), [docs/architecture/system/architecture.md](/home/xiongxianfei/data/20260419-rigorloop/docs/architecture/system/architecture.md:286)). Workflow guidance says stable releases require passing Codex, Claude Code, and opencode smoke rows ([docs/workflows.md](/home/xiongxianfei/data/20260419-rigorloop/docs/workflows.md:322)).

Required outcome: Stable `v0.1.3` smoke rows must be backed by actual maintainer smoke evidence for the installed/generated `v0.1.3` adapters, or the release metadata must stop claiming smoke `pass` until such evidence exists.

Safe resolution path: Extract or otherwise install each generated `v0.1.3` adapter archive into a disposable root, run the accepted smoke command/form for Codex, Claude Code, and opencode, and update `docs/releases/v0.1.3/release.yaml` evidence with the actual commands/results. If smoke cannot be run in this slice, change the release metadata and lifecycle state so `v0.1.3` is not release-ready, then record the blocker instead of marking smoke rows `pass`.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | R42-R57 release and token-cost evidence are present, and release notes satisfy R46-R49, but preserved smoke obligations are not met by archive-structure evidence alone. |
| Test coverage | pass | Token-cost runner and validator tests cover generated public adapter sources, `.codex/skills/` rejection, and retired v0.1.3 repository-source rejection. Release-gate tests cover generated archive validation commands. |
| Edge cases | concern | Source-commit/checksum and token-source edge cases are covered; stable adapter smoke evidence remains under-proved. |
| Error handling | pass | The runner rejects local `.codex/skills/` and the retired v0.1.3 repository-tree path before fixture preparation. |
| Architecture boundaries | concern | Generated archive validation and checksum boundaries are respected, but release smoke evidence is conflated with repository-owned archive validation. |
| Compatibility | pass | v0.1.2 compatibility-window language remains version-qualified, and v0.1.3 release notes point to release archives. |
| Security/privacy | pass | No secrets or sensitive runtime values are introduced; dry-run JSONL evidence is synthetic and small. |
| Derived artifact currency | pass | Adapter artifact metadata checksums validate against generated `v0.1.3` archives, and token-cost evidence points to generated public adapter output. |
| Unrelated changes | pass | The diff is scoped to M3 release evidence, token-cost source validation, release gate source-commit handling, and lifecycle bookkeeping. |
| Validation evidence | concern | The recorded release gate passes structurally, but it currently accepts smoke rows whose evidence does not show actual adapter smoke execution. |

## No-finding rationale

Not applicable; one material finding requires resolution before M3 can close.

## Residual risks

- The token-cost report uses approved dry-run evidence because live local Codex execution stalled. This is recorded in the report and plan; it is not the material finding.
- `docs/learn/sessions/2026-05-13-release-version-gate.md` remains an unrelated untracked learn artifact and is outside this review surface.

## Recommended next stage

Enter `review-resolution` for CR-M3-1, keep M3 on the same milestone, and rerun `code-review M3` after the smoke evidence is fixed or an approved release-readiness blocker is recorded.
