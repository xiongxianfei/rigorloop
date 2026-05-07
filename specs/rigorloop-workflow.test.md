# RigorLoop workflow test spec

## Status

- active

## Related spec and plan

- Spec: [RigorLoop Workflow](rigorloop-workflow.md), approved.
- Proposal: [Workflow Refactor](../docs/proposals/2026-05-01-workflow-refactor.md), accepted.
- Historical plan: [Workflow Refactor Execution Plan](../docs/plans/2026-05-03-workflow-refactor.md), done.
- Related follow-on spec: [Learn Artifact Model](learn-artifact-model.md), approved.
- Related follow-on test spec: [Learn Artifact Model test spec](learn-artifact-model.test.md), active.
- Related follow-on spec: [Formal Review Recording](formal-review-recording.md), approved.
- Related follow-on test spec: [Formal Review Recording test spec](formal-review-recording.test.md), active.
- Related amendment proposal: [PR-Self-Contained Lifecycle Completion](../docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md), accepted.
- Completed amendment plan: [PR-Self-Contained Lifecycle Completion Plan](../docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md), done.
- Related amendment proposal: [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md), accepted.
- Current amendment plan: [Review Skill Material Finding Recording Execution Plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md), active.
- Related amendment spec: [Milestone-Aware Review Handoff](milestone-aware-review-handoff.md), approved.
- Related amendment test spec: [Milestone-Aware Review Handoff test spec](milestone-aware-review-handoff.test.md), active.
- Related amendment plan: [Milestone-Aware Review Handoff Execution Plan](../docs/plans/2026-05-07-milestone-aware-review-handoff.md), active.
- Architecture: not required. The approved refactor and PR-self-contained lifecycle completion amendment change workflow governance, documentation, skills, validators, and generated output without runtime architecture or deployment boundaries.
- Spec-review: approved with no material findings after the PR-self-contained lifecycle completion amendment was added; minor SR-1 asked the test spec to decide how merge-dependent language classification is recorded.
- Plan-review: approved with no material findings for the PR-self-contained lifecycle completion plan. Minor non-blocking note: if README remains unchanged, final affected-surface evidence should mark it unaffected with rationale.

## Testing strategy

- Use manual contract review for contributor-facing guidance where the requirement is documentation clarity, source-of-truth alignment, or human-readable workflow semantics.
- Use filesystem-backed integration tests for selector behavior, lifecycle validation, skill validation, generated-output drift, adapter generation, change metadata, and review artifact validation.
- Use focused skill-validator assertions only for stable, machine-checkable skill guidance such as required labels, forbidden stale labels, handoff boundaries, and generated-output drift.
- Use selector-selected targeted proof as the first validation layer for changed paths; use broad smoke only when an authoritative trigger elevates it.
- Treat `specs/rigorloop-workflow.test.md` as the active proof-planning and regression surface for the workflow contract and implemented amendment.
- Keep deferred project-map lifecycle mechanics out of this test spec except for explicit non-goal checks.
- Treat final learn artifact modeling as a cross-spec alignment point here; detailed session, topic, evidence, classification, and routing proof lives in `specs/learn-artifact-model.test.md`.
- Treat formal review recording as a cross-spec alignment point here; detailed review-artifact fixture coverage lives in `specs/formal-review-recording.test.md`, while this test spec proves the workflow contract does not contradict stage-neutral recording, clean-review settlement, or conditional review-resolution behavior.
- Treat PR-self-contained lifecycle completion as the current workflow amendment under test. A merge-dependent language warning is treated as addressed only when a contributor-visible tracked or review-visible surface classifies the wording as a true downstream completion event or stale lifecycle wording requiring correction; the first implementation slice does not need to suppress the warning automatically after classification.
- Treat review skill material-finding recording as the current review-recording amendment under test. Detailed fixture coverage lives in `specs/formal-review-recording.test.md` and `specs/review-finding-resolution-contract.test.md`; this test spec proves the workflow-facing contract keeps isolation, broad material-finding recording, governance alignment, shared skill guidance, and scan-first resolution closeout consistent.
- Treat milestone-aware review handoff as the current full-feature routing amendment for planned implementation milestones. Detailed state-vocabulary and handoff-summary coverage lives in `specs/milestone-aware-review-handoff.test.md`; this test spec proves the broader workflow contract does not route clean non-final milestone reviews to `verify`.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`-`R5`, `R25h` | `T1` | manual | Fast lane and two-lane contributor guidance |
| `R6`-`R6dc`, `R20`-`R24a`, `R26`, `R27` | `T4`, `T20`, `T29` | manual, integration | Category model, affected-surface alignment, source-of-truth and generated-output boundaries |
| `R6a`-`R6i` | `T20`, `T21` | manual, integration | Standing artifact gates, bootstrap exceptions, project-map no-reliance, architecture-package routing |
| `R7`-`R7b` | `T20`, `T22` | manual, integration | Stable obligation values, trigger behavior, and `Runs for every change` semantics |
| `R7ba`-`R7bf` | `T23` | manual, integration | Periodic `learn`, default nonblocking behavior, session-record closeout, and final learn artifact model linkage |
| `R7c`-`R7w` | `T24` | manual, integration | Autoprogression, immediate handoff language, stage-owned authority, tracked-branch review and verify claims |
| `R8`-`R8g`, `R8i`, `R8j` | `T2`, `T30` | manual, integration | Planned milestone lifecycle, plan/index coherence, and milestone commits |
| `R8h`-`R8hc` | `T29`, `T30` | manual, integration | PR-self-contained plan lifecycle closeout and true downstream event handling |
| `R8ja`-`R8jb` | `T30`, `T32` | manual, integration | Stale plan state and merge-dependent plan wording classification |
| `R8k`-`R8kg` | `T18`, `T25` | manual, integration | Lifecycle states, stale authoritative artifact handling, PR reference behavior |
| `R8kh`-`R8kj` | `T31`, `T32` | manual, integration | Broader repo-local lifecycle state, review-resolution closeout consistency, and tracked merge-dependent language warnings |
| `R8l`-`R8s` | `T13`, `T17`, `T25` | integration, smoke, manual | Selector-selected proof, CI wrapper semantics, broad-smoke triggers, manual proof records |
| `R9`-`R9b`, `R18`, `R19` | `T13`, `T14`, `T26` | smoke, manual, integration | Routine CI, thin hosted wrapper, and `ci-maintenance` boundary |
| `R10`-`R12f` | `T3`, `T16`, `T27` | manual, integration | Durable reasoning, PR summary, review-resolution closeout, formal review recording triggers, and verify-report conditionality |
| `R12an`-`R12av` | `T27` | manual, integration | Stage-neutral detailed-record triggers, material/no-material initial review-record roots, and artifact-local status boundary |
| `R12aw`-`R12bdd` | `T33` | manual, integration | Isolation stops handoff, material findings require change-local review records, isolated output fields are complete, and review-output-only settlement is forbidden for material findings |
| `R12be`, `R12bg` | `T34` | integration, manual | Formal review skills share one canonical `Isolation and Recording` block and governance guidance teaches the same broad rule |
| `R12bf` | `T35` | integration, manual | New `review-resolution.md` records remain scan-first while preserving validator-readable fields |
| Milestone-aware review handoff amendment `R1`-`R11b` | `T36` | integration, manual | Planned implementation milestone review routing, same-milestone resolution, state vocabulary, and verify-readiness boundaries |
| `R13`, `R14`, `R14a`, `R14b` | `T15` | integration | Golden-path skill-validator example and rich-example proportionality |
| `R15`, `R15a` | `T8`, `T9`, `T10` | integration | Canonical skill validation and intentionally simple rule set |
| `R16` | `T9`, `T10` | integration | Required skill-validator fixture failures |
| `R17`, `R23`, `R24` | `T11`, `T12` | integration | Generated-output determinism and drift failure |
| `R25`, `R25a`-`R25e` | `T5`, `T6`, `T7`, `T15`, `T28` | integration | `change.yaml` schema, required fields, validation records, review state, and active change metadata |
| `R25f`, `R25g` | `T15`, `T16`, `T28` | manual, integration | Narrative in Markdown and reviewer-facing summary in PR text |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T13`, `T15` | Golden path example plus structural checks |
| `E2` | `T1` | Fast-lane docs-only flow remains documented |
| `E3` | `T1` | Fast-lane rejection for workflow or CI changes remains explicit |
| `E4` | `T2` | Multiple milestone commits may share one PR |
| `E5` | `T2` | Non-milestone work does not require milestone commit subjects |
| `E6` | `T20`, `T22` | Category routing and stage obligations are visible |
| `E7` | `T21` | Project-map absence, staleness, contradiction, or missing area requires refresh or no-map rationale before reliance |
| `E8` | `T27` | Required review-resolution closeout blocks downstream stages and formal review records stay discoverable when triggered |
| `E9` | `T26` | `ci-maintenance` is infrastructure maintenance, not validation execution |
| `E10` | `T23` | `learn` is trigger-based and not a default final per-change stage |
| `E11` | `T29`, `T30` | Completing PR records plan `Done` in both plan index and plan body before review opens |
| `E12` | `T29`, `T30` | True downstream release, deploy, publication, external migration, or unobserved hosted result keeps the plan active |
| `E13` | `T31` | Review-resolution closeout and readiness wording stay self-contained in the PR tree |
| `E14` | `T33` | Isolated review recording follows the finding while handoff stays stopped |
| `E15` | `T35` | Review-resolution remains scan-first and parseable |
| Milestone-aware amendment `E1`-`E6` | `T36` | Clean non-final/final review split, findings loop, ambiguous plan state, plan revision, and lifecycle-closeout distinction |

## Edge case coverage

- Generated-artifact refresh with no generator logic change can remain fast-lane only with spec and targeted validation: `T1`, `T25`
- Documentation-only workflow policy changes are not fast-lane eligible: `T1`
- CI automation changes require full lifecycle even without product behavior change: `T1`, `T26`
- Generic workflow content and generated adapter output remain separate: `T4`, `T11`, `T12`
- PRs without automated tests require a no-test rationale: `T3`, `T17`, `T28`
- Routine review feedback can remain in PR or explain-change when it does not create material durable memory: `T16`, `T27`
- Optional `change.yaml` artifact keys may be omitted, but required top-level fields may not: `T5`, `T6`, `T7`, `T28`
- Planned milestones require milestone evidence and commit boundaries even when they share one PR: `T2`
- Fast-lane and unplanned single-slice work may use normal commit subjects: `T2`
- Accepted or approved lifecycle artifacts can remain current guidance when readiness text is truthful: `T18`, `T25`
- Final PR text cannot add new authoritative references without renewed verification: `T3`, `T25`, `T28`
- Ordinary non-trivial changes may use `change.yaml` plus `explain-change.md` while review-resolution and verify-report remain conditional: `T16`, `T27`, `T28`
- Formal reviews with no material findings and no detailed-record trigger may settle in the reviewed artifact without empty review artifacts: `T27`
- Formal reviews with no material findings but a stage-owned non-approval outcome still create an indexed detailed review record without requiring empty `review-resolution.md`: `T27`
- Material upstream formal review findings open a review-record root before fixes proceed: `T27`
- The `docs/changes/0001-skill-validator/` example remains richer than the universal minimum: `T15`
- Approved legacy top-level explain artifacts remain valid until retired: `T3`, `T16`
- `spec-review` and `plan-review` preserve immediate handoff versus downstream readiness: `T24`
- `explore` and `research` are on-demand support and block only after trigger or dependency reliance: `T22`
- Triggered `learn` closes through the final learn artifact model when a session reaches Frame, or through pre-session scheduled follow-up, deferral, or no-learn rationale when no session runs; it blocks only when a higher-priority artifact makes it blocking: `T23`
- `ci-maintenance` may be skipped when hosted automation already covers the material risk: `T26`
- Missing, stale, contradicted, or incomplete `docs/project-map.md` cannot be relied on without refresh or no-map rationale: `T21`
- Bootstrap proposals without `VISION.md` or `CONSTITUTION.md` must identify the exception in `Vision fit`: `T21`
- Open material review findings block `verify`, final `explain-change`, and `pr`: `T27`
- Isolated material findings require change-local review files even when downstream handoff stops: `T33`
- Isolated material-review output missing required record path, record-before-fixing or reconstruction status, or owner-decision status is incomplete: `T33`
- Shared formal review skill guidance drifts from the canonical source or contains stage-specific text inside the shared block: `T34`
- New scan-first review-resolution guidance removes parseable per-finding labels: `T35`
- A clean review of a non-final planned implementation milestone must not route to `verify`: `T36`
- A lifecycle-closeout milestone must not be treated as an open implementation milestone for verify readiness: `T36`
- In-flight work can finish under its starting workflow contract unless it opts in or touches refactored workflow surfaces: `T20`, `T25`
- Draft PRs may run early CI without being review-open, but lifecycle state must synchronize before reviewer action resumes: `T29`
- Reopened PRs and reused branches must satisfy PR-self-contained lifecycle completion before review continues: `T29`
- Release, deploy, package publication, external migration, and unobserved hosted checks are true downstream events that can keep a plan active: `T29`, `T30`
- Tracked wording such as "move to Done after merge" is warning evidence and becomes blocking when the PR already contains the completion evidence: `T30`, `T32`
- A spec may remain `draft` while awaiting spec-review, but if spec-review approves it and downstream artifacts rely on it, the same PR records `approved` before review-ready handoff continues: `T31`

## Test cases

### T1. Workflow documentation exposes the two-lane contract

- Covers: `R1`, `R2`, `R3`, `R4`, `R5`, `R25h`, `E2`, `E3`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `.github/pull_request_template.md`
- Steps:
  - Review contributor-facing docs and confirm they describe fast lane and full lifecycle.
  - Confirm the fast-lane allowlist, disallow list, required spec fields, and allowed spec locations are visible.
  - Confirm workflow, CI behavior, schema, generated-output logic, release packaging, and hard-to-rollback changes are excluded from fast lane.
- Expected result:
  - A contributor can determine when fast lane is allowed, when it is rejected, and what evidence is required without reading chat history.
- Failure proves:
  - The starter kit workflow contract remains implicit or internally inconsistent.
- Automation location:
  - Manual review during M1.

### T2. Planned milestone work rules are visible and unambiguous

- Covers: `R8`, `R8a`, `R8b`, `R8c`, `R8d`, `R8e`, `R8f`, `R8g`, `R8i`, `E4`, `E5`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `docs/plan.md`
  - `docs/plans/2026-05-03-workflow-refactor.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
- Steps:
  - Confirm milestone closeout evidence, milestone commit format, and multi-milestone PR behavior are described consistently.
  - Confirm fast-lane or unplanned single-slice work is explicitly exempt from milestone-formatted commits.
  - Confirm the active plan and plan index remain coherent during milestone progress updates.
- Expected result:
  - Planned milestone work has one clear closeout rule and one clear commit-boundary rule across the repo.
- Failure proves:
  - Milestone planning and implementation guidance can drift into contradictory commit or closeout expectations.
- Automation location:
  - Manual review during M1 and final M4 closeout.

### T3. PR summary and explain-change guidance match the contract

- Covers: `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e`, `R11`, `R12`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `.github/pull_request_template.md`
  - `README.md`
  - `docs/workflows.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
- Steps:
  - Confirm every change requires reviewer-facing summary and validation or no-test rationale.
  - Confirm the split between PR summary, durable Markdown artifacts, and structured metadata is described accurately.
  - Confirm new non-trivial work defaults to `docs/changes/<change-id>/explain-change.md`.
  - Confirm PR text alone is not presented as a substitute for required durable reasoning.
  - Confirm approved legacy top-level explain artifacts remain valid until retired.
- Expected result:
  - Reviewer-facing requirements for summary, validation, artifact links, and durable reasoning location are clear before implementation.
- Failure proves:
  - Contributors may satisfy scripts while omitting required durable reasoning or misusing PR text as the only durable explanation.
- Automation location:
  - Manual review during M1, M2, and M4.

### T4. Root guidance preserves canonical-versus-generated boundaries

- Covers: `R20`, `R20a`, `R21`, `R22`, `R23`, `R24`, `R24a`, `R26`, `R27`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - existing architecture source-layout artifact when referenced
- Steps:
  - Confirm root guidance identifies canonical authored paths and generated paths.
  - Confirm generated `.codex/skills/` and `dist/adapters/` output are not presented as hand-edited source of truth.
  - Confirm docs still position Git, pull requests, CI, and human review as authoritative.
- Expected result:
  - Contributors know what may be edited, what is generated, and what repository controls remain authoritative.
- Failure proves:
  - The source-of-truth split is not enforceable in practice.
- Automation location:
  - Manual review during M1 and M4; generated-output checks in `T11` and `T12`.

### T5. Valid `change.yaml` passes metadata validation

- Covers: `R25`, `R25a`, `R25b`, `R25c`, `R25d`, `R25e`
- Level: integration
- Fixture/setup:
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `tests/fixtures/change-metadata/valid-basic/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`.
- Expected result:
  - The command exits zero and reports the sample metadata file as valid.
- Failure proves:
  - The repository cannot validate the canonical `change.yaml` contract even for a correct sample.
- Automation location:
  - Existing metadata validator tests and final M4 validation.

### T6. Missing required `change.yaml` fields fail validation

- Covers: `R25b`
- Level: integration
- Fixture/setup:
  - invalid fixtures such as `tests/fixtures/change-metadata/missing-title/change.yaml`
  - invalid fixtures such as `tests/fixtures/change-metadata/missing-review/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py <invalid-fixture>` for each missing-field case.
- Expected result:
  - Each invalid file exits non-zero and names the missing required field.
- Failure proves:
  - The metadata validator does not enforce the documented top-level contract.
- Automation location:
  - Existing metadata validator tests and direct fixture validation.

### T7. Malformed validation or review records fail metadata validation

- Covers: `R25d`, `R25e`
- Level: integration
- Fixture/setup:
  - invalid fixtures such as `tests/fixtures/change-metadata/bad-validation-record/change.yaml`
  - invalid fixtures such as `tests/fixtures/change-metadata/bad-review-shape/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py <invalid-fixture>` for each malformed-record case.
- Expected result:
  - The validator exits non-zero and identifies the invalid validation or review structure.
- Failure proves:
  - `change.yaml` can pass even when it cannot support traceability or review-state inspection.
- Automation location:
  - Existing metadata validator tests and direct fixture validation.

### T8. Canonical skills pass structural validation

- Covers: `R15`, `R15a`, `R23`
- Level: integration
- Fixture/setup:
  - canonical `skills/*/SKILL.md`
  - `scripts/validate-skills.py`
- Steps:
  - Run `python scripts/validate-skills.py` after canonical skill edits.
- Expected result:
  - The canonical `skills/` tree passes validation with no missing metadata, missing required sections, placeholder text, or source-of-truth violations.
- Failure proves:
  - The canonical skill source is not good enough to generate or validate reliably.
- Automation location:
  - M2 and M4 validation.

### T9. Missing metadata or required sections fail skill validation

- Covers: `R15`, `R16`
- Level: integration
- Fixture/setup:
  - `tests/fixtures/skills/valid-basic/`
  - `tests/fixtures/skills/missing-name/`
  - `tests/fixtures/skills/missing-description/`
  - `tests/fixtures/skills/missing-title/`
  - `tests/fixtures/skills/missing-expected-output/`
- Steps:
  - Run `python scripts/test-skill-validator.py`.
- Expected result:
  - The valid fixture passes and each missing-field or missing-section fixture fails for the expected reason.
- Failure proves:
  - The validator cannot enforce the minimum structural skill contract.
- Automation location:
  - `scripts/test-skill-validator.py`

### T10. Duplicate names and placeholder text fail skill validation

- Covers: `R15`, `R16`
- Level: integration
- Fixture/setup:
  - `tests/fixtures/skills/duplicate-name/`
  - `tests/fixtures/skills/placeholder-text/`
  - canonical `skills/`
- Steps:
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/validate-skills.py`.
- Expected result:
  - Duplicate-name and placeholder fixtures fail, and canonical `skills/` contains neither duplicate names nor placeholder markers.
- Failure proves:
  - The validator misses cross-skill or content-quality failures that the first-release contract includes.
- Automation location:
  - `scripts/test-skill-validator.py` and canonical corpus validation.

### T11. Skill and adapter generation is deterministic

- Covers: `R17`, `R20`, `R21`, `R22`, `R23`, `R24a`
- Level: integration
- Fixture/setup:
  - canonical `skills/`
  - generated `.codex/skills/`
  - generated `dist/adapters/`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
- Steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
- Expected result:
  - Generated Codex runtime mirrors and public adapters match canonical skills with no drift.
- Failure proves:
  - Generated compatibility output is not stable enough to review or track in Git.
- Automation location:
  - M2 and M4 generated-output validation.

### T12. Drift check fails on stale or hand-edited generated output

- Covers: `R17`, `R23`, `R24`
- Level: integration
- Fixture/setup:
  - a deliberately edited or stale file under `.codex/skills/` or `dist/adapters/`
  - generator `--check` mode
- Steps:
  - Introduce a controlled mismatch in a temp copy or fixture.
  - Run the matching generator `--check` command.
- Expected result:
  - The drift check exits non-zero and identifies the canonical and generated paths that diverged.
- Failure proves:
  - Generated output can drift silently from canonical source.
- Automation location:
  - Existing generator tests and direct `--check` invocation.

### T13. Repository CI wrapper runs selected structural checks

- Covers: `R8l`, `R8m`, `R8n`, `R8o`, `R8p`, `R8q`, `R9`, `R18`, `R19`, `E1`
- Level: smoke
- Fixture/setup:
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - changed paths from this refactor
- Steps:
  - Run `python scripts/select-validation.py --mode explicit --path <changed-path>...`.
  - Run `bash scripts/ci.sh --mode explicit --path <changed-path>...`.
  - Confirm selected checks use stable check IDs and do not imply broad smoke by default.
- Expected result:
  - Selector-selected proof classifies changed paths, chooses stable check IDs, and the CI wrapper executes the selected checks.
- Failure proves:
  - Targeted validation cannot support review handoff for workflow-governance changes.
- Automation location:
  - M1, M3, and M4 validation.

### T14. GitHub CI workflow stays a thin wrapper over repo-owned commands

- Covers: `R9`, `R18`, `R19`, `R27`
- Level: manual
- Fixture/setup:
  - `.github/workflows/ci.yml`
  - `scripts/ci.sh`
- Steps:
  - Inspect the workflow definition and confirm it calls the repo-owned script.
  - Confirm hosted workflow logic does not redefine validation behavior inconsistently with `scripts/ci.sh`.
- Expected result:
  - GitHub Actions delegates to repository-owned validation logic.
- Failure proves:
  - CI logic may drift between hosted automation and repository scripts.
- Automation location:
  - Manual workflow review during M4.

### T15. Golden-path skill-validator artifacts remain coherent

- Covers: `R13`, `R14`, `R14a`, `R14b`, `R25f`, `R25g`, `E1`
- Level: integration
- Fixture/setup:
  - `docs/changes/0001-skill-validator/`
  - `docs/changes/0001-skill-validator/change.yaml`
  - top-level proposal/spec/architecture artifacts
- Steps:
  - Confirm the example artifact directory contains proposal, spec, plan, test-spec, verify report, explain-change, and `change.yaml`.
  - Run `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`.
  - Confirm repository guidance does not present the `0001` artifact set as the minimum pack for every non-trivial change.
- Expected result:
  - The proof-of-value example remains coherent and clearly richer than the ordinary baseline pack.
- Failure proves:
  - The advertised golden path is incomplete, invalid, or misleading.
- Automation location:
  - Existing metadata validation and manual artifact review.

### T16. Durable reasoning and reviewer-facing explanation stay visible

- Covers: `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e`, `R11`, `R12`, `R12b`, `R12ca`, `R12d`, `R12e`, `R12f`
- Level: manual
- Fixture/setup:
  - `.github/pull_request_template.md`
  - `docs/workflows.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - current change-local pack when created
- Steps:
  - Confirm PR-facing guidance asks for summary, why, validation, risk, and artifact links.
  - Confirm non-trivial work has a durable Markdown reasoning surface.
  - Confirm review-resolution and verify-report remain conditional and concise.
- Expected result:
  - Reviewers can find summary, rationale, validation, and review disposition without reverse-engineering commit history.
- Failure proves:
  - The repository can pass automation while hiding reasoning from humans.
- Automation location:
  - Manual review during M1, M2, and M4.

### T17. Baseline validation works without secrets, network, or Codex installation

- Covers: security/privacy and boundary behavior sections, `R8r`, `R8s`
- Level: smoke
- Fixture/setup:
  - local shell with no repository secrets exported
  - baseline validation scripts
- Steps:
  - Run baseline validation commands in a normal local environment without providing secrets.
  - Confirm they operate only on repository files and do not require Codex runtime installation or external network access.
  - For any manual proof record, confirm check, result, performer, date, evidence, and `manual by design` rationale are recorded.
- Expected result:
  - Baseline structural validation and manual proof recording are locally reproducible.
- Failure proves:
  - The validation surface is more operationally fragile than the contract allows.
- Automation location:
  - M4 verification.

### T18. Validation failures are specific and contributor-actionable

- Covers: observability requirements, `R8k`-`R8kg`
- Level: integration
- Fixture/setup:
  - one invalid skill fixture
  - one invalid metadata fixture
  - stale lifecycle artifact fixture or controlled lifecycle inconsistency
  - one stale generated output file
- Steps:
  - Run the relevant validator, lifecycle validator, and drift check against failing cases.
  - Inspect exit codes and failure messages.
- Expected result:
  - Each failure is non-zero and names the file, fixture, skill, path, lifecycle state, or missing field that caused the error.
- Failure proves:
  - Contributors will struggle to fix failures even if enforcement logic exists.
- Automation location:
  - `scripts/test-skill-validator.py`, `scripts/test-artifact-lifecycle-validator.py`, generator checks, and direct validator invocations.

### T19. Repository-scale performance smoke stays proportional

- Covers: performance expectations from the workflow spec
- Level: manual
- Fixture/setup:
  - current repository tree
- Steps:
  - Run the main validation commands on the repository-sized fixture set.
  - Record rough local wall-clock behavior if noticeably slow.
- Expected result:
  - Validation behaves like linear filesystem work and does not require a build service, cache, or database.
- Failure proves:
  - The implementation is more operationally heavy than the workflow contract allows.
- Automation location:
  - Manual smoke check before final `verify`.

### T20. Workflow category model and affected surfaces are visible

- Covers: `R6`, `R6d`, `R6da`, `R6db`, `R20`-`R24a`, `R26`, `R27`, `E6`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `README.md`
  - `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` when created
- Steps:
  - Confirm the workflow summary and affected guidance expose standing artifacts, living references, workflow infrastructure, on-demand artifacts, per-change chain, and periodic artifacts.
  - Confirm workflow-governance surfaces are updated, explicitly marked unaffected with rationale, or recorded as deferred with owner and follow-up.
  - Confirm unaffected/deferred records live in tracked or review-visible surfaces and not chat-only notes.
  - Confirm the in-flight selected workflow contract is recorded as `refactored` where it affects review.
- Expected result:
  - Contributors can see the category model and reviewers can audit affected-surface disposition without reading chat history.
- Failure proves:
  - The core workflow refactor remains hidden in scattered prose or unreviewable chat-only state.
- Automation location:
  - Manual review during M1 and M4, plus lifecycle validation where applicable.

### T21. Standing artifact gates and project-map no-reliance rule are enforced in guidance

- Covers: `R6a`, `R6b`, `R6c`, `R6e`, `R6f`, `R6g`, `R6h`, `R6i`, `E7`
- Level: manual, integration
- Fixture/setup:
  - `docs/workflows.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Steps:
  - Confirm `VISION.md` and `CONSTITUTION.md` have distinct absence gates and bootstrap exceptions.
  - Confirm bootstrap proposals must identify the exception in `Vision fit` and proposal-review checks it.
  - Confirm consumers must not rely on absent, known-stale, contradicted, or incomplete `docs/project-map.md` without refresh or no-map rationale.
  - Confirm no calendar freshness threshold, freshness marker, or full project-map lifecycle workflow is introduced.
  - Confirm architecture-stage references still route to the architecture package method when architecture is required.
- Expected result:
  - Standing artifact gates and project-map no-reliance behavior are explicit without expanding the deferred project-map lifecycle.
- Failure proves:
  - Contributors can proceed on nonexistent standing artifacts or stale repository maps without recorded rationale.
- Automation location:
  - Manual review during M1 and M2; focused skill-validator assertions if M3 makes the wording stable enough.

### T22. Stage obligations use stable values and triggers

- Covers: `R7`, `R7a`, `R7b`, `E6`
- Level: manual, integration
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `scripts/test-skill-validator.py` if focused assertions are added
- Steps:
  - Confirm obligation values are exactly `mandatory`, `conditional`, `on-demand`, and `periodic`.
  - Confirm the full-lifecycle table includes stage/action, role, obligation, trigger, `Runs for every change`, and downstream blocking.
  - Confirm `explore` and `research` are on-demand and not default prerequisites.
  - Confirm the `Runs for every change` column applies only after the row trigger makes a stage applicable and does not override fast-lane eligibility.
  - Confirm downstream blocking for conditional, on-demand, and periodic rows follows trigger/dependency/higher-priority-artifact rules.
- Expected result:
  - Readers can tell which actions run for every change and which block only after the relevant trigger or dependency.
- Failure proves:
  - The refactor still leaves mandatory, optional, and triggered work ambiguous.
- Automation location:
  - Manual review during M1/M2 and focused assertions during M3 if stable.

### T23. Triggered learn uses final learn surfaces without becoming a default stage

- Covers: `R7ba`, `R7bb`, `R7bc`, `R7bd`, `R7be`, `R7bf`, `E10`
- Level: manual, integration
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `specs/learn-artifact-model.md`
  - `specs/learn-artifact-model.test.md`
  - `docs/workflows.md`
  - active plan and change-local pack
- Steps:
  - Confirm `learn` is periodic or explicitly invoked, not a default final per-change stage.
  - Confirm triggers include cadence, incident response, contributor observation, repeated findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem actions, and maintainer request.
  - Confirm a `learn` invocation that reaches Frame creates or updates `docs/learn/sessions/YYYY-MM-DD-<slug>.md`, including empty or no-durable-lesson sessions.
  - Confirm durable topic guidance is routed to `docs/learn/topics/<topic>.md` only when confirmed durable lessons justify it.
  - Confirm action-changing lessons route to the authoritative affected artifact rather than treating topic files as policy.
  - Confirm pre-session no-record closeout is allowed only when `learn` does not actually run as a session.
  - Confirm triggered learn blocks downstream only when a higher-priority artifact explicitly makes it blocking.
- Expected result:
  - Ordinary PR closeout does not block on learn by default, but triggered learning uses tracked final learn surfaces once a session runs.
- Failure proves:
  - `learn` either becomes process theater for every change, loses required durable follow-up, or falls back to superseded temporary surfaces.
- Automation location:
  - Manual review during M1/M2 and final M4 change-local evidence review.

### T24. Workflow handoff and stage-owned authority stay distinct

- Covers: `R7c`-`R7w`
- Level: manual, integration
- Fixture/setup:
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `scripts/test-skill-validator.py` if focused assertions are added
- Steps:
  - Confirm workflow-managed flows and isolated stage requests are distinguished.
  - Confirm `spec-review` separates outcome, immediate next repository stage, and eventual `test-spec` readiness.
  - Confirm `plan-review` preserves `test-spec` as the immediate next handoff.
  - Confirm `implement`, `code-review`, `verify`, and `pr` each use only their owned readiness language.
  - Confirm branch-scoped clean review or branch-ready claims require tracked governing authority and direct proof for named edge cases.
- Expected result:
  - Stage outputs cannot skip required handoffs or claim authority owned by a later stage.
- Failure proves:
  - The workflow can appear ready by language rather than by required evidence.
- Automation location:
  - Manual review during M2; focused skill-validator assertions during M3 if stable.

### T25. Selector, lifecycle, and broad-smoke behavior match the refactor

- Covers: `R8k`-`R8kg`, `R8l`-`R8s`
- Level: integration
- Fixture/setup:
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - active plan and touched lifecycle artifacts
- Steps:
  - Run `python scripts/test-select-validation.py`.
  - Run `python scripts/test-artifact-lifecycle-validator.py`.
  - Run explicit-path lifecycle validation over the accepted proposal, approved spec, active test spec, plan index, and active plan.
  - Run selector-selected explicit CI over changed paths.
  - Confirm broad smoke is not required unless selector mode, explicit flag, plan, test spec, review-resolution, or release metadata elevates it.
- Expected result:
  - Targeted proof and lifecycle validation cover the changed surfaces, and broad smoke remains trigger-based.
- Failure proves:
  - Review handoff may either under-validate touched artifacts or require broad smoke without authority.
- Automation location:
  - M3 and M4 validation.

### T26. CI-maintenance is distinct from validation execution

- Covers: `R9`, `R9a`, `R9b`, `E9`
- Level: manual, integration
- Fixture/setup:
  - `docs/workflows.md`
  - `AGENTS.md`
  - `skills/ci/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/verify/SKILL.md`
- Steps:
  - Confirm contributor-facing workflow guidance uses `ci-maintenance` for hosted CI workflow files, validation automation, or platform configuration.
  - Confirm validation execution stays under `verify` and repository-owned scripts.
  - Confirm the existing `skills/ci/` path remains allowed as the CI infrastructure skill entrypoint.
  - Confirm guidance does not describe `ci-maintenance` as running tests, designing tests, specifying validation commands, or waiting for existing CI checks.
- Expected result:
  - Contributors can tell when CI infrastructure maintenance is required and when ordinary validation belongs to `verify`.
- Failure proves:
  - The ambiguous `ci` stage remains conflated with validation execution.
- Automation location:
  - Manual review during M1/M2 and focused skill assertions during M3 if stable.

### T27. Review-resolution closeout blocks downstream stages when required

- Covers: `R12a`-`R12f`, `R12an`-`R12av`, `E8`
- Level: manual, integration
- Fixture/setup:
  - `specs/formal-review-recording.md`
  - `specs/formal-review-recording.test.md`
  - `specs/review-finding-resolution-contract.md`
  - `docs/workflows.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/validate-review-artifacts.py`
  - review artifacts under `docs/changes/<change-id>/` when material findings exist
- Steps:
  - Confirm material findings require evidence, required outcome, and safe resolution or `needs-decision` rationale.
  - Confirm detailed formal lifecycle review records are stage-neutral across `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.
  - Confirm detailed review records are required for material findings, stage-owned non-approval outcomes that block downstream progress or require revision, reconstructed evidence, closeout-evidence citation, and explicit reviewer or maintainer request.
  - Confirm clean required formal reviews can settle in the reviewed artifact when no detailed-record trigger applies.
  - Confirm no-material detailed records require `review-log.md` but do not require an empty `review-resolution.md` solely because `reviews/` exists.
  - Confirm material initial review-record roots include `review-resolution.md`, while no-material initial roots do not.
  - Confirm `review-resolution.md` dispositions are limited to approved values.
  - Confirm `needs-decision`, `Closeout status: open`, missing disposition evidence, or open `review-log.md` findings block `verify`, final `explain-change`, and `pr`.
  - If this amendment creates material findings, run `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-05-pr-self-contained-lifecycle-completion`.
  - Run `python scripts/test-review-artifact-validator.py` when validator behavior is changed or relied on for a new review artifact assertion.
- Expected result:
  - Required review-resolution closeout cannot be skipped or silently replaced by implementation fixes alone, and no-material review events remain discoverable without empty resolution files.
- Failure proves:
  - Material review findings or upstream non-approval review events can be lost between formal review and final PR readiness.
- Automation location:
  - M4 when review-resolution is triggered; validator tests only when review-artifact validation changes or is explicitly selected.

### T28. Active workflow-governance change metadata is valid and traceable

- Covers: `R25`, `R25a`-`R25h`, `R10`-`R12f`
- Level: integration, manual
- Fixture/setup:
  - `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` when created
  - `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md` when created
  - `docs/changes/2026-05-03-workflow-refactor/change.yaml` as historical reference only when relied on
  - optional review-resolution or verify-report artifacts if triggered
- Steps:
  - Create the baseline non-trivial change-local pack before final verification.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml`.
  - Confirm `change.yaml` links the proposal, spec, active test spec, active plan, touched artifacts, validation records, and review state.
  - Confirm Markdown artifacts carry narrative rationale and PR text remains the reviewer-facing summary.
- Expected result:
  - Reviewers can trace the current workflow-governance change through structured metadata plus durable Markdown reasoning.
- Failure proves:
  - The active change has machine-readable metadata but insufficient human-readable rationale, or vice versa.
- Automation location:
  - M4 validation and final `verify`.

### T29. PR-self-contained lifecycle guidance is visible and bounded

- Covers: `R6dc`, `R8h`-`R8hc`, `E11`, `E12`
- Level: manual
- Fixture/setup:
  - `CONSTITUTION.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`
  - `docs/plans/0000-00-00-example-plan.md`
  - `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Steps:
  - Confirm `CONSTITUTION.md` states that lifecycle synchronization happens in the PR performing the transition before review opens, and that merge is a fast-forward of pre-validated state rather than a trigger for further lifecycle changes.
  - Confirm `docs/workflows.md`, affected skills, and learn/topic guidance no longer present routine merge-dependent `Done` as an allowed plan closeout path.
  - Confirm guidance keeps true downstream completion events, such as release, deploy, package publication, external migration, or unobserved hosted checks, out of repo-local lifecycle state.
  - Confirm draft PRs, reopened PRs, and reused branches synchronize repo-local lifecycle state before reviewers are asked to judge the branch.
  - Confirm README is either updated or explicitly recorded as unaffected with rationale in the active plan or change-local evidence.
- Expected result:
  - Contributors can tell when to close lifecycle state in the current PR and when to leave a plan active for a true downstream event.
- Failure proves:
  - The repository can keep the old post-merge memory dependency alive through lower-priority guidance.
- Automation location:
  - Manual review during M1 and final M4 affected-surface review.

### T30. Plan index/body lifecycle validation catches stale state

- Covers: `R8h`-`R8hc`, `R8j`-`R8jb`, `E11`, `E12`
- Level: integration
- Fixture/setup:
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/validate-artifact-lifecycle.py`
  - fixture repositories under `tests/fixtures/artifact-lifecycle/`
  - temporary `docs/plan.md` and `docs/plans/*.md` files
- Steps:
  - Add failing coverage for a completed, blocked, or superseded plan still listed under `## Active` in `docs/plan.md`.
  - Add failing coverage for `docs/plan.md` and the referenced plan body presenting conflicting lifecycle state.
  - Add failing coverage for a done, blocked, or superseded plan body whose readiness still describes the plan as active or in progress.
  - Add passing coverage for an active plan that names a true downstream completion event or follow-up condition.
  - Add warning coverage for tracked plan lifecycle wording that implies lifecycle closeout after merge.
  - Run `python scripts/test-artifact-lifecycle-validator.py`.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`.
- Expected result:
  - Stale plan/index lifecycle state is blocking, true downstream-event wording is allowed, and merge-dependent lifecycle wording is visible as reviewer-attention output unless the same evidence is also blocking.
- Failure proves:
  - Plans can still land with stale Active/Done state or hidden merge-dependent closeout promises.
- Automation location:
  - M2 lifecycle validator implementation and M4 final validation.

### T31. Broader repo-local lifecycle inconsistency blocks branch-ready

- Covers: `R8kh`, `R8ki`, `E13`
- Level: integration, manual
- Fixture/setup:
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/review_artifact_validation.py`
  - `scripts/test-review-artifact-validator.py`
  - lifecycle-managed proposal, spec, test-spec, architecture, or ADR fixtures as needed
  - review artifacts under `docs/changes/<change-id>/`
- Steps:
  - Add fixture or manual proof for a lifecycle-managed proposal, spec, test spec, architecture document, or ADR whose status conflicts with relied-on PR-contained evidence.
  - Add fixture or manual proof for active readiness wording in a test spec, verify report, explain-change artifact, or change-local artifact after the PR has completed and recorded its own scope.
  - Add review-artifact proof that `review-resolution.md` cannot say `Closeout status: open` after all material findings have final dispositions and required evidence.
  - Add review-artifact proof that `Closeout status: closed` fails when required findings, dispositions, rationale, follow-up, validation evidence, or `review-log.md` closeout evidence are missing.
  - Run `python scripts/test-artifact-lifecycle-validator.py` and `python scripts/test-review-artifact-validator.py` when either validator is changed or relied on for this proof.
- Expected result:
  - Broader lifecycle artifact inconsistency blocks `branch-ready` for touched, referenced, generated, or authoritative artifacts, while unrelated stale baseline artifacts remain warnings.
- Failure proves:
  - The PR tree can claim current readiness while authoritative lifecycle artifacts still describe an earlier or incomplete state.
- Automation location:
  - M2 lifecycle/review-artifact validator implementation and M4 final verification.

### T32. Tracked merge-dependent language is warned and classified

- Covers: `R8jb`, `R8kj`
- Level: integration, manual
- Fixture/setup:
  - tracked Markdown or YAML files containing lifecycle wording such as "after merge", "post-merge", or "once this lands"
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - contributor-visible classification surfaces: the same tracked artifact, the active plan, `docs/changes/<change-id>/change.yaml`, `docs/changes/<change-id>/explain-change.md`, a formal review record, PR body, or draft PR body
- Steps:
  - Add warning coverage for tracked merge-dependent lifecycle wording.
  - Confirm the warning names the tracked file and remains non-blocking unless another lifecycle inconsistency makes the same evidence blocking.
  - Confirm first-slice detection inspects tracked files and does not require hosted PR-description event metadata.
  - Confirm any remaining merge-dependent language warning is treated as addressed only when a contributor-visible tracked or review-visible surface classifies it as a true downstream completion event or stale lifecycle wording requiring correction.
  - Do not require the validator to suppress the warning after classification in this first slice.
- Expected result:
  - Reviewers see merge-dependent lifecycle wording, and contributors must classify it before branch-ready or PR handoff treats the warning as addressed.
- Failure proves:
  - Merge-dependent lifecycle language can either hide in tracked files or be dismissed without a durable classification.
- Automation location:
  - M2 warning fixtures, M3 selector routing if needed, and M4 manual affected-surface review.

### T33. Isolated formal review output stops handoff but requires material-finding recording

- Covers: `R12aw`-`R12bdd`, `E14`
- Level: manual, integration
- Fixture/setup:
  - `specs/formal-review-recording.md`
  - `specs/formal-review-recording.test.md`
  - `templates/shared/review-isolation-and-recording.md`
  - formal review skills under `skills/`
  - `scripts/test-skill-validator.py`
  - `scripts/test-review-artifact-validator.py`
- Steps:
  - Confirm workflow-facing guidance states that isolation governs handoff only and does not suppress material-finding recording.
  - Confirm every material finding requires a durable change-local review record under `docs/changes/<change-id>/reviews/`, whether workflow-managed or isolated.
  - Confirm isolated material-review output names handoff status, material Finding IDs, required record path, whether the record must be created before fixing or reconstructed, and whether owner decision is needed.
  - Confirm the output makes the next action clear without requiring enum-style action strings.
  - Confirm isolated material-review output does not offer review-output-only or artifact-local-only settlement for material findings.
- Expected result:
  - A contributor can stop after a direct review while still seeing exactly what durable record is required before any material finding is acted on.
- Failure proves:
  - Isolation can again be misread as no recording, or the review output omits the action needed to preserve first-pass evidence.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - manual review during M1 and M4

### T34. Formal review skills and governance share the canonical broad recording rule

- Covers: `R12be`, `R12bg`
- Level: integration, manual
- Fixture/setup:
  - `templates/shared/review-isolation-and-recording.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert all five formal review skills contain one byte-identical `## Isolation and Recording` block copied from the canonical template.
  - Assert stage-specific content appears outside the shared block.
  - Assert `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` use the same rule: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.
  - Assert implementation does not proceed with canonical skill changes until affected governance and operating guidance are aligned or explicitly marked unaffected with rationale.
- Expected result:
  - The workflow contract, formal review skills, and contributor-facing governance surfaces teach one rule without stage-specific drift.
- Failure proves:
  - Guidance can drift across review stages or higher-priority governance surfaces.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `bash scripts/ci.sh --mode explicit ...`
  - manual M1/M4 affected-surface review

### T35. Scan-first review-resolution remains parseable at workflow handoff

- Covers: `R12bf`, `E15`
- Level: integration, manual
- Fixture/setup:
  - `specs/review-finding-resolution-contract.md`
  - `specs/review-finding-resolution-contract.test.md`
  - `templates/review-resolution.md` or another approved durable guidance surface
  - `scripts/test-review-artifact-validator.py`
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/review-resolution.md` as current scan-first example evidence
- Steps:
  - Confirm new or revised review-resolution guidance starts with closeout status, covered reviews, resolved and unresolved counts, and final result.
  - Confirm it includes a resolution overview and can use common metadata and shared validation evidence to avoid repeated prose.
  - Confirm each material finding detail keeps parseable labels required by the review finding resolution contract.
  - Confirm `verify`, `explain-change`, and `pr` guidance summarize review-resolution counts and link details instead of duplicating every finding.
- Expected result:
  - Workflow handoff can rely on human-readable review closeout without weakening closeout validation.
- Failure proves:
  - Readability guidance either became too prose-heavy to scan or lost validator-readable finding fields.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording`
  - manual M2/M4 review

### T36. Milestone-aware review handoff qualifies clean-review routing

- Covers: milestone-aware review handoff amendment `R1`-`R11b`, amendment `E1`-`E6`
- Level: integration, manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `specs/workflow-stage-autoprogression.md`
  - `specs/milestone-aware-review-handoff.md`
  - `specs/milestone-aware-review-handoff.test.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Confirm workflow-managed full-feature routing distinguishes milestone-based plans from non-milestone implementation slices.
  - Confirm `implement` records `review-requested` handoff for the current implementation milestone rather than whole-plan verify readiness.
  - Confirm clean `code-review` closes the reviewed milestone directly when no review-resolution is required.
  - Confirm clean non-final milestone reviews route to the next in-scope implementation milestone, while clean final milestone reviews route to `verify`.
  - Confirm findings, accepted fixes, re-review, inconclusive review, ambiguous plans, and lifecycle-closeout milestones preserve the approved same-milestone and verify-readiness boundaries.
- Expected result:
  - The workflow contract prevents the old clean-review shortcut from routing `M1` directly to `verify` when later implementation milestones remain.
- Failure proves:
  - Planned milestone work can still skip required implementation or review-resolution gates.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - manual M2/M3 review

## Fixtures and data

- Canonical workflow artifacts:
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/proposals/2026-05-01-workflow-refactor.md`
  - `docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `docs/plans/2026-05-03-workflow-refactor.md` as historical context
  - `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `docs/plan.md`
- Contributor-facing guidance:
  - `README.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `docs/workflows.md`
  - `.github/pull_request_template.md`
- Canonical skills:
  - `skills/workflow/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/ci/SKILL.md`
  - `skills/learn/SKILL.md`
  - other stage skills only when M2 identifies stale duplicated handoff wording
- Generated output:
  - `.codex/skills/`
  - `dist/adapters/`
- Validation scripts:
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - `scripts/validate-skills.py`
  - `scripts/test-skill-validator.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/test-select-validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/test-review-artifact-validator.py`
- Existing fixtures:
  - `tests/fixtures/skills/`
  - `tests/fixtures/change-metadata/`
  - `tests/fixtures/artifact-lifecycle/`
  - `tests/fixtures/review-artifacts/` when review-resolution fixtures are added
  - `docs/changes/0001-skill-validator/`
- New active change-local artifacts when created:
  - `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml`
  - `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md`
  - optional review-resolution or verify-report artifacts when triggered
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/change.yaml`
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/review-log.md`
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/review-resolution.md`
  - `templates/shared/review-isolation-and-recording.md`
  - `templates/review-resolution.md` or another approved durable scan-first guidance surface

## Mocking and stubbing policy

- Do not mock filesystem structure for validator, generator, drift, selector, lifecycle, or metadata behavior when temp directories or real fixture trees can be used.
- Do not use snapshots as the only proof for workflow behavior.
- Prefer real fixture directories and direct CLI invocations over tests that stub file contents.
- If a test needs stale generated output, create it by controlled edits in a temp copy rather than mocking drift logic.
- If a content assertion is too prose-sensitive, keep it as manual proof unless the approved contract supplies stable IDs, table headers, stage names, or allowed values.
- Do not mock hosted PR metadata for merge-dependent language detection in this first slice. Use tracked files and review-visible manual evidence instead.

## Migration and compatibility tests

- `T4`, `T11`, and `T12` verify canonical authored content remains separate from generated Codex and public adapter output.
- `T20` verifies affected workflow-governance surfaces are updated, explicitly marked unaffected, or deferred with owner and follow-up.
- `T21` verifies the `VISION.md` migration is treated as already complete and lowercase `vision.md` is not reintroduced as canonical.
- `T21` verifies project-map lifecycle markers and freshness thresholds are not invented in this refactor.
- `T23` verifies the workflow spec links to the final learn artifact model while preserving nonblocking default behavior.
- `T26` verifies the `skills/ci/` path remains compatible while contributor-facing stage language uses `ci-maintenance`.
- `T25` verifies in-flight work can record its selected workflow contract without forcing unrelated active work to churn.
- `T29` and `T30` verify existing merge-dependent closeout language is migrated when touched or relied on, while true downstream events keep lifecycle state active.
- `T32` verifies first-slice warning detection stays repository-local and does not depend on hosted PR-description metadata.

## Observability verification

- `T13` verifies selector-selected checks and CI wrapper output use stable check IDs.
- `T18` verifies validation failures are path-specific and contributor-actionable.
- `T20` verifies affected-surface dispositions are review-visible.
- `T23` verifies learn sessions and pre-session closeouts are not chat-only.
- `T27` verifies review-resolution closeout records evidence, dispositions, and blocking state.
- `T30` verifies plan lifecycle validation reports stale plan/index state with path-specific findings.
- `T31` verifies broader lifecycle artifact inconsistency blocks `branch-ready` for touched, referenced, generated, or authoritative artifacts.
- `T32` verifies merge-dependent language warnings identify the tracked file and require contributor-visible classification.
- `T28` verifies change metadata and explain-change artifacts trace the final implementation.

## Security and privacy verification

- `T17` verifies baseline validation does not require repository secrets, network access, or Codex installation.
- Manual review should confirm no fixture, change-local metadata, learn rationale, no-map rationale, or generated output records credentials or sensitive runtime configuration.
- This refactor has no new data store, external network integration, or secret-handling path.

## Performance checks

- `T19` is a manual smoke check only; there is no hard benchmark gate for this refactor.
- If selector, lifecycle, skill, generator, or adapter validation becomes noticeably slow, treat it as an implementation issue before final `verify`.
- Broad smoke remains trigger-based and is not the default first proof for this plan.

## Manual QA checklist

- [ ] `README.md`, `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` present the approved category model without reintroducing the old overloaded chain as the default workflow.
- [ ] The per-change chain excludes default `explore`, default `research`, final per-change `learn`, and ambiguous `ci` wording.
- [ ] `explore` and `research` are described as on-demand support.
- [ ] `learn` is periodic or explicitly invoked, uses final `docs/learn/sessions/**` session records after Frame, and permits no-record closeout only before a session runs.
- [ ] `ci-maintenance` means CI infrastructure maintenance and not validation execution.
- [ ] `review-resolution` is closeout for material review findings and blocks downstream while open.
- [ ] Formal review recording is stage-neutral, proportionally triggered, and does not require empty `review-resolution.md` for no-material detailed records.
- [ ] Every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.
- [ ] Formal review skills contain byte-identical `## Isolation and Recording` guidance copied from the canonical template.
- [ ] New review-resolution guidance is scan-first and keeps parseable per-finding labels.
- [ ] Plan lifecycle transitions happen inside the PR that performs the transition, before the PR opens for review.
- [ ] Merge is described as a fast-forward of pre-validated lifecycle state, not a trigger for routine closeout.
- [ ] True downstream completion events keep plans active and name the later event or follow-up condition.
- [ ] Tracked merge-dependent language is warned, and any remaining warning has a contributor-visible classification before final handoff.
- [ ] README is updated or explicitly marked unaffected with rationale for this workflow amendment.
- [ ] `VISION.md` and `CONSTITUTION.md` are standing artifacts with distinct absence gates.
- [ ] `docs/project-map.md` is a living reference and cannot be relied on when absent, stale, contradicted, or missing the relied-on area without refresh or no-map rationale.
- [ ] Every affected operating or governance surface is updated, marked unaffected with rationale, or deferred with owner and follow-up.
- [ ] Generated `.codex/skills/` and `dist/adapters/` output is regenerated from canonical skills and passes drift checks.
- [ ] The active plan and `docs/plan.md` agree before final `verify`.
- [ ] The active change-local pack links proposal, spec, test spec, plan, validation evidence, review state, and explain-change.

## What not to test

- Do not test subjective writing quality, philosophy, or style preferences in workflow or skill prose.
- Do not implement or test project-map calendar thresholds, freshness markers, or the full project-map revision workflow.
- Do not test detailed session-record, topic-file, evidence, classification, or routing behavior here; `specs/learn-artifact-model.test.md` owns that proof.
- Do not rename or require renaming `skills/ci/`.
- Do not re-test or re-migrate root `vision.md` to `VISION.md`; this refactor only ensures `VISION.md` remains canonical.
- Do not test hosted GitHub release publishing end to end.
- Do not require network-dependent checks for baseline validation.
- Do not test exact prose unless the assertion uses stable contract terms, section headings, table headers, stage names, or allowed values.
- Do not inspect hosted PR-description event metadata for merge-dependent language detection in the first enforcement slice.
- Do not define or test merge-SHA recording rules.
- Do not treat deploy, release, package publication, external migration, or unobserved hosted checks as repo-local lifecycle state that can be made true by the PR tree.

## Uncovered gaps

- None blocking at the spec, architecture, or planning level.
- Project-map lifecycle mechanics are intentionally deferred to a focused follow-up.
- Detailed learn-session behavior is covered by `specs/learn-artifact-model.test.md`.
- Merge-dependent language warning suppression after classification is intentionally not required in the first slice; the required proof is warning visibility plus contributor-visible classification before final handoff treats the warning as addressed.
- If implementation discovers that a stable workflow guarantee cannot be tested manually or through existing scripts, update this test spec or return to plan-review before widening implementation scope.

## Next artifacts

- Implementation M1 under [Review Skill Material Finding Recording plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md).
- `code-review` after implementation milestones complete.
- `verify`.
- `explain-change`.
- `pr`.

## Follow-on artifacts

- `implementation`: PR-self-contained lifecycle completion M1 through M4 complete.
- `review-resolution`: material M2 code-review finding accepted, fixed, and closed.
- `verify`: completed for PR handoff after PR-mode selected validation and broad smoke.
- `explain-change`: completed in `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/explain-change.md`.
- `pr`: PR #30 opened for human review.
- `proposal`: [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md)
- `spec`: [Formal Review Recording](formal-review-recording.md) amendment for isolation-versus-recording behavior.
- `spec`: [Review Finding Resolution Contract](review-finding-resolution-contract.md) amendment for scan-first `review-resolution.md` records.
- `plan`: [Review Skill Material Finding Recording plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md)
- `plan-review`: approved on 2026-05-07 with no material findings.
- `test-spec`: updated with review skill material-finding recording amendment coverage.

## Readiness

Active proof-planning and regression surface for the workflow contract and review skill material-finding recording amendment. Implementation may proceed under the active 2026-05-07 plan starting with M1.

Future milestone work must add or update assertions before paired artifact changes, and each milestone closes only after the paired changes make those assertions and validation commands pass.
