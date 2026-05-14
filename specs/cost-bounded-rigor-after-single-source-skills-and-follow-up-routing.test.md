# Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing Test Spec

## Status

active

## Related spec and plan

- Spec: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), approved.
- Proposal: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted.
- Plan: [Cost-Bounded Rigor First Slice Plan](../docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md), active after clean plan-review.
- Spec review: [spec-review-r2](../docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/spec-review-r2.md), approved with no material findings.
- Plan review: [plan-review-r1](../docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/plan-review-r1.md), approved with no material findings.
- Change metadata: [change.yaml](../docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml).
- Architecture: not required. The approved spec and reviewed plan scope this slice to proposal guidance, proposal-review guidance, workflow documentation, and focused static proof.
- Project map: [docs/project-map.md](../docs/project-map.md) exists as a living orientation reference. This test spec does not rely on project-map claims for ownership, path routing, runtime architecture, or deferred execution.

## Approval

Maintainer-approved on 2026-05-14 by direct user request. Status remains `active` because test specs use `active` as the relied-on proof-planning state for implementation.

## Testing strategy

This first slice is verified through contract, static, lifecycle, and manual review checks. It does not require runtime end-to-end tests, release validation, adapter packaging validation, dynamic token benchmarks, or validation-selector behavior changes.

- Use static skill-validator checks for stable first-slice wording in `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`, and `docs/workflows.md` when the implementation adds those assertions.
- Use manual contract review for semantic judgment that should not become brittle validator inference, including broadness classification, hidden follow-up risk, and misleading treatment values.
- Use lifecycle and change-metadata validation to prove the proposal, spec, test spec, plan, review records, and current handoff state remain coherent.
- Use skill validation, generated local mirror checks, and static skill token measurement when canonical skill text changes.
- Use selected explicit validation for changed paths before broader checks.
- Treat static token measurement as diagnostic and warning-only; do not require before/after dynamic benchmark comparison for this wording-only slice.

## Requirement coverage map

| Requirement IDs | Covered by | Notes |
|---|---|---|
| `R1`, `R2` | `T1`, `T10`, `T11` | First-slice scope and forbidden surfaces. |
| `R3`, `R4`, `R4a`, `R4b` | `T2`, `T4`, `T5` | Scope-budget trigger and reviewer judgment boundary. |
| `R5`, `R5a`, `R5b`, `R5c` | `T2`, `T4` | Table shape, work item, treatment, reason, and allowed treatments. |
| `R6`, `R6a` | `T3`, `T4` | Follow-up ownership routing and `project-map` boundary. |
| `R7`, `R7a`, `R7b` | `T3`, `T10` | Single-authored skill source and generated adapter boundary. |
| `R8`, `R9` | `T4` | Proposal-review checks and `changes-requested` outcomes. |
| `R10` | `T5` | Small single-decision proposal exemption. |
| `R11`, `R11a`, `R11b` | `T5` | Validators do not infer broadness; optional present-table checks stay mechanical. |
| `R12`, `R13`, `R14`, `R14a` | `T6` | `docs/workflows.md` ownership and bounded evidence sequence. |
| `R15`, `R15a`, `R15b` | `T7` | Do-not-under-read and full-file-read escape conditions. |
| `R16`, `R16a`, `R16b` | `T8` | Concise skill wording and no long repeated shared template. |
| `R17` | `T1`, `T9`, `T11` | Safety-critical review, verify, PR, material-finding, and release guidance intact. |
| `R18`, `R18a`, `R18b` | `T9`, `T11` | Diagnostic token measurement and no dynamic benchmark requirement. |
| `R19`, `R19a`, `R19b` | `T10`, `T11` | Affected-surface decisions, lifecycle state, and deferred/unaffected rationale. |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` | `T2`, `T4` |
| `E2` | `T2`, `T5` |
| `E3` | `T4` |
| `E4` | `T5` |
| `E5` | `T6` |
| `E6` | `T7` |
| `E7` | `T1`, `T9`, `T10` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` two shared-file work items with different lifecycle owners | `T2`, `T4` |
| `EC2` workflow docs plus public skill behavior mislabeled docs-only | `T2`, `T4`, `T10` |
| `EC3` validation-selector changes claimed as first-slice work | `T1`, `T4`, `T10` |
| `EC4` lifecycle token-cost summaries claimed as routine first-slice output | `T1`, `T4`, `T9` |
| `EC5` scope-budget table leaves treatment or reason blank | `T2`, `T4` |
| `EC6` `deferable follow-up` row has no owner route | `T3`, `T4` |
| `EC7` validator sees no `Scope budget` heading | `T5` |
| `EC8` bounded evidence finds conflicting line ranges | `T7` |
| `EC9` whole file is the review target | `T7` |
| `EC10` project map absent, stale, contradicted, or missing relied-on area | `T6`, `T10` |
| `EC11` later plan tries to edit `implement` or `code-review` for progressive loading | `T1`, `T8`, `T9` |
| `EC12` release or adapter path appears only as completed PR #52 context | `T1`, `T3`, `T10` |

## Acceptance criteria coverage map

| Acceptance criterion | Covered by |
|---|---|
| Broad or multi-workstream proposals are guided to include a scope budget | `T2`, `T4` |
| Small single-decision proposals may omit the scope budget | `T5` |
| Scope-budget guidance defines triggers, table shape, values, and meanings | `T2` |
| Proposal-review checks missing or misleading broad-proposal classification | `T4` |
| Proposal-review requests changes for silent narrowing, hidden follow-up risk, missing routing, or misleading values | `T4` |
| Validators do not infer broadness as a hard failure | `T5` |
| `docs/workflows.md` remains the path, follow-up-routing, and bounded-evidence guide | `T6`, `T10` |
| `docs/workflows.md` discourages broad path or state searches when narrower evidence exists | `T6` |
| Bounded-evidence guidance includes do-not-under-read escape | `T7` |
| First slice does not change out-of-scope validation, release, adapter, token-report, benchmark, or progressive-loading behavior | `T1`, `T9`, `T10` |
| Affected-surface decisions are recorded | `T10` |
| Safety-critical review, verification, material-finding, and release guidance remains intact | `T9`, `T11` |

## Test cases

### T1. First-slice scope and forbidden surfaces remain exact

- Covers: `R1`, `R2`, `R17`, `E7`, `EC3`, `EC4`, `EC11`, `EC12`
- Level: contract, manual
- Fixture/setup:
  - approved spec
  - active plan
  - final implementation diff
- Steps:
  - Assert implementation changes are limited to proposal guidance, proposal-review guidance, `docs/workflows.md`, focused static proof, and lifecycle bookkeeping.
  - Assert the diff does not change validation-selector behavior, broad-smoke triggers, release validation, generated adapter packaging, lifecycle token-cost summary artifacts, dynamic benchmark requirements, or full progressive-loading behavior for `workflow`, `implement`, or `code-review`.
  - Assert safety-critical formal review, verify, PR, material-finding, and release guidance is not removed for token-cost reasons.
- Expected result: the first slice remains a narrow workflow-guidance change.
- Failure proves: the implementation repeats the broad-workstream amplification the spec is preventing.
- Automation location: manual final diff review, selected validation output, `git diff --check --`.

### T2. Proposal skill defines scope-budget trigger, table, and treatments

- Covers: `R3`, `R4`, `R4a`, `R4b`, `R5`, `R5a`, `R5b`, `R5c`, `E1`, `E2`, `EC1`, `EC2`, `EC5`
- Level: static, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert proposal guidance asks broad or multi-workstream proposals to include a `Scope budget` section or equivalent classification before downstream reliance.
  - Assert guidance names trigger conditions for independent work items, multiple lifecycle families, more than one plausible spec or plan, release/workflow/generated-output/public-skill/validation policy, and proposal-review-identified narrowing or hidden follow-up risk.
  - Assert guidance says applicability is proposal/proposal-review judgment rather than mechanical validator inference.
  - Assert guidance says small single-decision proposals may omit the scope budget.
  - Assert the preferred table shape includes `Work item`, `Treatment`, and `Reason`.
  - Assert allowed treatments include `core to this proposal`, `first-slice candidate`, `same-slice dependency`, `separate implementation slice`, `deferable follow-up`, `separate proposal`, and `out of scope`.
  - Assert each treatment is defined in terms of current scope, first-slice scope, dependency, later implementation slice, follow-up, separate proposal, or exclusion.
- Expected result: proposal authors can classify broad scope without turning every small proposal into ceremony.
- Failure proves: proposal guidance is missing reviewable classification or creates a brittle hard-validator implication.
- Automation location: `scripts/test-skill-validator.py`, manual contract review.

### T3. Proposal skill preserves follow-up routing and single-source boundaries

- Covers: `R6`, `R6a`, `R7`, `R7a`, `R7b`, `EC6`, `EC12`
- Level: static, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `docs/workflows.md`
  - `dist/adapters/README.md` when needed for source-boundary confirmation
- Steps:
  - Assert proposal guidance routes deferred work through the accepted follow-up ownership model rather than chat-only notes or `project-map` ownership.
  - Assert guidance preserves the boundary that workflow routes, `project-map` orients when present, action-owning artifacts track current work, and unowned cross-change follow-ups use the follow-up ownership surface.
  - Assert proposal guidance says `skills/` is the authored skill source or otherwise preserves that boundary.
  - Assert it does not direct contributors to search generated adapter output for authored skill truth.
  - Assert it does not reintroduce tracked generated public adapter skill bodies as a first-slice source surface.
- Expected result: scope-budget guidance builds on PR #52 and PR #53 instead of reopening them.
- Failure proves: the proposal skill can route future work or skill truth to the wrong owner surface.
- Automation location: `scripts/test-skill-validator.py`, manual contract review.

### T4. Proposal-review checks broad scope classification and returns changes requested when needed

- Covers: `R3`-`R10`, `E1`, `E3`, `EC1`-`EC6`
- Level: static, manual
- Fixture/setup:
  - `skills/proposal-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - sample broad proposal reasoning during manual review
- Steps:
  - Assert proposal-review guidance checks whether broad or multi-workstream proposals classify current scope, same-slice dependencies, later slices, follow-ups, separate proposals, and out-of-scope work.
  - Assert it returns `changes-requested` when a broad proposal lacks required classification, hides follow-up work, silently narrows a user request, leaves treatment or reason blank, omits follow-up routing, or uses a misleading treatment value.
  - Assert it allows non-standard treatment values only when they are clear and do not create downstream ambiguity.
  - Assert it does not rewrite the proposal while reviewing unless the user explicitly asks.
- Expected result: proposal-review is the semantic gate for broadness and hidden-scope risk.
- Failure proves: broad proposal scope can pass into spec or plan without reviewable classification.
- Automation location: `scripts/test-skill-validator.py`, manual proposal-review checklist.

### T5. Small-proposal exemption and validator broadness boundary are preserved

- Covers: `R4`, `R4b`, `R10`, `R11`, `R11a`, `R11b`, `E2`, `E4`, `EC7`
- Level: static, manual
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - any validator touched by implementation
- Steps:
  - Assert proposal and proposal-review guidance both allow small single-decision proposals to omit the scope budget when omission does not create narrowing, hidden follow-up risk, or multi-workstream ambiguity.
  - Assert no first-slice validator fails a proposal solely because it infers broadness from proposal content or absence of a `Scope budget` heading.
  - If a static check for a present scope-budget table is added, assert it only checks mechanical shape such as heading, columns, or required phrases.
  - Assert no natural-language broadness scoring or semantic validator inference is introduced.
- Expected result: semantic broadness judgment remains in proposal/proposal-review for the first slice.
- Failure proves: the implementation adds premature validator ceremony or brittle semantic scoring.
- Automation location: `scripts/test-skill-validator.py`, manual diff review of validation scripts.

### T6. Workflow guide owns bounded evidence and path-search sequence

- Covers: `R12`, `R13`, `R14`, `R14a`, `E5`, `EC10`
- Level: contract, static
- Fixture/setup:
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert `docs/workflows.md` remains the project-local guide for artifact locations, follow-up routing, and bounded evidence or path-search behavior.
  - Assert it discourages broad searches of authoritative documents solely for path or state discovery when narrower evidence is available.
  - Assert bounded evidence starts from exact user-provided paths or change IDs, current handoff summary or active plan state, `change.yaml`/review logs/review resolution/release metadata, the artifact-location map, targeted headings/stable IDs/line ranges/counts/diffs, then full-file reads when needed.
  - Assert project-map reliance remains conditional on the map being present, fresh enough, not contradicted, and covering the relied-on area.
- Expected result: agents can find paths and state through bounded sources before broad reads.
- Failure proves: `docs/workflows.md` still encourages or permits costly path discovery before targeted evidence.
- Automation location: `scripts/test-skill-validator.py`, manual workflow-doc review.

### T7. Bounded-evidence guidance preserves do-not-under-read and full-file escapes

- Covers: `R15`, `R15a`, `R15b`, `E6`, `EC8`, `EC9`
- Level: contract, static, manual
- Fixture/setup:
  - `docs/workflows.md`
  - touched skill wording
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert bounded-evidence guidance explicitly says not to under-read.
  - Assert it requires expansion to a broader section or full file when bounded evidence is incomplete, contradictory, or insufficient for the claim being made.
  - Assert it preserves full-file reads when the whole file is the review target, surrounding context can change the conclusion, relevant sections cannot be isolated safely, bounded searches disagree or are incomplete, or behavior-changing edits depend on understanding the whole source-of-truth artifact.
  - Manually confirm skill wording does not use bounded evidence as permission to skip needed context.
- Expected result: cost reduction cannot weaken correctness or review rigor.
- Failure proves: bounded evidence was implemented as under-reading.
- Automation location: `scripts/test-skill-validator.py`, manual contract review.

### T8. Skill wording stays concise and avoids a repeated bounded-evidence template

- Covers: `R16`, `R16a`, `R16b`, `EC11`
- Level: static, manual
- Fixture/setup:
  - `docs/workflows.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `templates/shared/`
- Steps:
  - Assert `docs/workflows.md` owns the full bounded-evidence rule.
  - Assert proposal and proposal-review skills contain only short local reminders needed for their stage behavior.
  - Assert no long repeated bounded-evidence template or new shared block is introduced for this first slice.
  - Assert `implement` and `code-review` are not edited for progressive-loading follow-through unless a later accepted artifact scopes that work.
- Expected result: public skill wording gains local operational clarity without duplicating the workflow guide.
- Failure proves: cost-bounded rigor created another repeated guidance surface.
- Automation location: `scripts/test-skill-validator.py`, `python scripts/validate-skills.py`, manual diff review.

### T9. Safety-critical guidance and token measurement remain warning-only

- Covers: `R17`, `R18`, `R18a`, `R18b`, `E7`, `EC4`, `EC11`
- Level: contract, smoke, manual
- Fixture/setup:
  - final diff
  - `scripts/measure-skill-tokens.py`
  - active plan validation notes or later explain-change
- Steps:
  - Assert formal review, verify, PR, material-finding, release, and full-file-read safety guidance remains intact.
  - Run static skill token measurement after canonical skill changes and record that the evidence is diagnostic only.
  - Assert no hard token thresholds are introduced.
  - Assert no before/after dynamic benchmark comparison is required unless a later accepted plan or test spec explicitly requires it.
  - Record the no-dynamic-benchmark rationale in change evidence during explain-change or verification.
- Expected result: token-cost evidence helps review without becoming a new hard gate.
- Failure proves: the first slice weakened rigor or added measurement work outside its trigger.
- Automation location: `python scripts/measure-skill-tokens.py`, manual review, later explain-change or verify evidence.

### T10. Affected-surface decisions and lifecycle state stay synchronized

- Covers: `R1`, `R2`, `R7`, `R7a`, `R7b`, `R12`, `R19`, `R19a`, `R19b`, `EC2`, `EC3`, `EC10`, `EC12`
- Level: integration, lifecycle
- Fixture/setup:
  - `docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - affected workflow-governance surfaces
- Steps:
  - Assert the active plan and change metadata list the proposal guidance surface, proposal-review guidance surface, and `docs/workflows.md` as affected first-slice surfaces.
  - Assert workflow-governance surfaces left unchanged are recorded as unaffected with rationale or deferred with owner and follow-up in a tracked or review-visible surface.
  - Assert `docs/plan.md`, the plan body, and `change.yaml` agree on the current stage after test-spec creation and after implementation milestones.
  - Assert generated public adapter skill bodies remain outside tracked source.
- Expected result: reviewers can see what changed, what stayed unchanged, and why.
- Failure proves: the workflow-governance change has stale state or hidden affected surfaces.
- Automation location: `python scripts/validate-artifact-lifecycle.py`, `python scripts/validate-change-metadata.py`, manual state-sync review.

### T11. Selected validation proves changed proof surfaces without broadening the slice

- Covers: all requirements
- Level: smoke, integration
- Fixture/setup:
  - changed files after implementation
  - active plan validation commands
- Steps:
  - Run focused static proof for any new or changed skill-validator checks.
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/build-skills.py --check` when canonical skills change.
  - Run selected validation and explicit CI for the changed paths named by the plan and implementation diff.
  - Run artifact lifecycle and change-metadata validation for lifecycle-managed artifacts and change-local metadata.
  - Run `git diff --check --`.
  - Do not run release, adapter archive, dynamic benchmark, or broad-smoke validation unless implementation unexpectedly touches the triggering surfaces.
- Expected result: the changed proof surfaces are validated without turning the first slice into release or benchmark work.
- Failure proves: validation is either too narrow to prove the contract or too broad for the approved slice.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/select-validation.py --mode explicit ...`
  - `bash scripts/ci.sh --mode explicit ...`
  - `python scripts/validate-change-metadata.py ...`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
  - `git diff --check --`

## Fixtures and data

- Canonical skill files:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- Workflow guide:
  - `docs/workflows.md`
- Lifecycle state:
  - `docs/plans/2026-05-14-cost-bounded-rigor-first-slice.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`
  - review records under `docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/reviews/`
- Static proof surfaces:
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/build-skills.py`
  - `scripts/measure-skill-tokens.py`
- Manual review samples are textual scenarios from the approved spec examples and edge cases. Do not add generated adapter output as a fixture for authored skill truth.

## Mocking/stubbing policy

No runtime services, external APIs, or generated adapter archives are needed for this first slice.

Static tests may use in-repository text fixtures or direct reads of canonical source files. They must not mock proposal-review judgment as a validator that infers semantic broadness from arbitrary proposal prose.

## Migration or compatibility tests

- Verify existing accepted proposals are not retroactively invalid solely because they lack a scope-budget table.
- Verify broad proposals created or substantively revised after spec approval are the target of the new guidance.
- Verify existing validation-selector behavior, broad-smoke triggers, release validation, adapter packaging, generated archives, and token-cost reports remain unchanged by this slice.

## Observability verification

- Scope-budget behavior is observable in proposal artifacts and proposal-review findings.
- Missing or misleading classification must be observable in proposal-review output by naming the missing classification, hidden follow-up, silent narrowing, or misleading treatment value.
- Bounded-evidence behavior is observable through `docs/workflows.md`, targeted evidence citations, validation summaries, and later stage outputs.
- No new telemetry, metrics service, hosted logging, or runtime tracing is required.

## Security/privacy verification

- Verify bounded-evidence wording prefers paths, IDs, counts, line citations, and targeted excerpts over broad dumps when evidence may contain sensitive data.
- Verify no guidance encourages pasting secrets, credentials, private logs, or unnecessary large excerpts into artifacts or chat.
- Verify this slice does not change authentication, authorization, secrets handling, or data-access behavior.

## Performance checks

- Run `python scripts/measure-skill-tokens.py` after canonical skill changes and treat the output as diagnostic.
- Do not enforce hard token thresholds.
- Do not require before/after dynamic benchmark comparison for this proposal/evidence wording slice.
- Record the rationale for no dynamic benchmark comparison in explain-change or verification evidence.

## Manual QA checklist

- Review the final diff against `R1` and `R2` to confirm the slice did not expand into selector, release, adapter, dynamic benchmark, lifecycle token summary, or progressive-loading work.
- Review `skills/proposal/SKILL.md` for scope-budget triggers, table shape, treatment values, follow-up routing, and single-source skill boundaries.
- Review `skills/proposal-review/SKILL.md` for semantic broadness checks, `changes-requested` outcomes, and the small-proposal exemption.
- Review `docs/workflows.md` for the bounded-evidence sequence, broad-search discouragement, and do-not-under-read escape.
- Review static tests to ensure they check stable phrases and mechanical structure rather than broad natural-language scoring.
- Review lifecycle state in the plan body, plan index, and change metadata after each state-changing handoff.

## What not to test

- Do not add runtime workflow simulations for this wording-only slice.
- Do not add or require dynamic token benchmarks.
- Do not add hard token thresholds.
- Do not run release or adapter archive validation unless implementation touches those surfaces unexpectedly.
- Do not change or test validation-selector broadness inference under this spec.
- Do not test generated public adapter skill bodies as authored source.
- Do not require full progressive-loading proof for `workflow`, `implement`, or `code-review`.

## Uncovered gaps

None. No requirement needs to return to spec-review or architecture before M1 implementation.

## Next artifacts

```text
implement
code-review
explain-change
verify
pr
```

## Follow-on artifacts

None yet.

## Readiness

Active and maintainer-approved. Lifecycle validation passed for the new test-spec artifact and handoff state; this test spec is ready to guide M1 implementation.
