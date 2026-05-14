# Cost-Bounded Rigor M5 Progressive-Loading Follow-Through Test Spec

## Status

active

## Related spec and plan

- Spec: [Cost-Bounded Rigor M5 Progressive-Loading Follow-Through](cost-bounded-rigor-m5-progressive-loading-follow-through.md), approved.
- Plan: [Cost-Bounded Rigor M5 Progressive-Loading Follow-Through Plan](../docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md), active after clean plan-review.
- Proposal: [Cost-Bounded Rigor After Single-Source Skills and Follow-Up Routing](../docs/proposals/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md), accepted.
- Progressive-loading baseline spec: [Progressive Loading for High-Cost Public Skills](progressive-loading-high-cost-public-skills.md), approved and implemented by its own completed plan.
- Spec review: [spec-review-r1](../docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/spec-review-r1.md), approved with no material findings.
- Plan review: [plan-review-r1](../docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/plan-review-r1.md), approved with no material findings.
- Change metadata: [change.yaml](../docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml).
- Architecture: not required. The approved spec, spec-review, and plan-review scope this slice to high-cost skill audit, minimal skill/proof follow-through, and lifecycle evidence, not runtime architecture, persistence, APIs, release packaging, adapter packaging, or selector behavior.
- Project map: [docs/project-map.md](../docs/project-map.md) exists as a living orientation reference. This test spec relies on the approved spec, reviewed plan, current skill text, and selected proof surfaces for implementation proof.

## Approval

Maintainer-approved on 2026-05-14 by direct user request. Status remains `active` because this test spec is the relied-on proof-planning surface for M5 implementation.

## Testing strategy

M5 is verified through contract review, static skill-proof checks, selected integration validation, lifecycle validation, and manual review of affected and intentionally unaffected surfaces. It does not require runtime end-to-end tests, release validation, adapter packaging validation, generated adapter output refresh, selector behavior changes, broad-smoke changes, lifecycle token-cost summary creation, hard token gates, or dynamic benchmark comparison by default.

- Audit `workflow`, `implement`, and `code-review` before editing any high-cost skill.
- Use existing progressive-loading proof in `scripts/test-skill-validator.py` before adding new checks.
- Add or update static checks only when a concrete M5 proof gap exists.
- Prefer section presence, required terms, behavior cues, and forbidden-sequence checks over exact full-sentence prose.
- Use manual contract review for safety-critical prose that should not become brittle natural-language lint.
- Run canonical skill validation and static token measurement when canonical skill text changes.
- If canonical skill text does not change, record an explicit no-run rationale for static token measurement.
- Do not run dynamic benchmarks unless implementation materially changes runtime benchmark behavior, the active plan is revised to require them, or the change claims runtime benchmark improvement.
- Use selected explicit validation for changed paths. Include this test spec, the active plan, `docs/plan.md`, and change metadata when lifecycle state changes.

## Requirement coverage map

| Requirement IDs | Covered by | Notes |
|---|---|---|
| `R1` | `T1`, `T2`, `T10`, `T12` | M5 remains limited to `workflow`, `implement`, `code-review`, proof, and lifecycle bookkeeping. |
| `R2` | `T1`, `T2`, `T12` | Completed progressive-loading work is baseline authority, not reopened. |
| `R3` | `T2`, `T12` | Every high-cost skill is audited before edits. |
| `R4` | `T2`, `T12` | Existing-sufficient skills remain unchanged or receive only justified clarification with no-change rationale. |
| `R5` | `T2`, `T7`, `T12` | Any skill edit is the smallest sufficient fix for a concrete gap. |
| `R6` | `T3`, `T12` | Touched high-cost skills preserve quick operating guide or equivalent targeted entry point. |
| `R7` | `T3`, `T5`, `T12` | Touched skills preserve targeted reading behavior before broad reads. |
| `R8` | `T3`, `T12` | Touched skills preserve broader-section or full-file escape behavior. |
| `R9` | `T4`, `T12` | `workflow` remains a router and preserves source order, stop conditions, and claim boundaries. |
| `R10` | `T5`, `T12` | `implement` starts milestone readiness and handoff checks from active plan `Current Handoff Summary`. |
| `R11` | `T5`, `T12` | `implement` treats missing, stale, or contradictory milestone state as a blocker. |
| `R12` | `T6`, `T11`, `T12` | `code-review` preserves independent review, material-finding, recording, routing, handoff, and result boundaries. |
| `R13` | `T4`, `T7`, `T10`, `T12` | `docs/workflows.md` remains the full bounded-evidence and routing guide. |
| `R14` | `T7`, `T12` | High-cost skill wording stays concise and does not duplicate the full workflow evidence sequence. |
| `R15` | `T1`, `T10`, `T12` | M5 does not rewrite every public skill. |
| `R16` | `T6`, `T11`, `T12` | Safety-critical review, verification, material-finding, validation, release, and handoff guidance is not removed for token savings. |
| `R17` | `T8`, `T9`, `T10`, `T12` | No hard token thresholds, hard release gates, or CI blockers are added. |
| `R18` | `T10`, `T12` | Selector, broad-smoke, release, adapter, generated-output, benchmark-suite, and report-schema behavior remain unchanged. |
| `R19` | `T10`, `T12` | Generated adapter output is not treated as authored skill truth or reintroduced as tracked skill bodies. |
| `R20` | `T8`, `T12` | Canonical skill surfaces are validated when skill text changes. |
| `R21` | `T8`, `T12` | Static token measurement runs when canonical skill text changes, or a no-run rationale is recorded. |
| `R22` | `T8`, `T9`, `T12` | Static token measurement stays diagnostic and warning-only. |
| `R23` | `T9`, `T12` | Dynamic benchmark comparison is advisory for no-change or small wording work unless required or claimed. |
| `R24` | `T9`, `T12` | Runtime improvement claims require targeted dynamic benchmark evidence. |
| `R25` | `T8`, `T12` | Static proof uses stable behavior cues instead of exact full-sentence prose unless exact text is the contract. |
| `R26` | `T10`, `T12` | PR #52 single-authored-source and PR #53 follow-up ownership models are preserved. |
| `R27` | `T1`, `T10`, `T12` | Out-of-scope release, adapter, generated-output, selector, benchmark, and hard-gate work stops or routes to a separate accepted artifact. |
| `R28` | `T9`, `T10`, `T12` | Lifecycle token-cost summaries remain optional unless an approved M4 trigger is named. |
| `R29` | `T2`, `T10`, `T12` | Affected and intentionally unaffected surfaces are recorded. |
| `R30` | `T7`, `T10`, `T12` | Public skill wording remains project-portable and avoids maintainer-only implementation details. |

## Example coverage map

| Example | Coverage |
|---|---|
| `E1` current skill already satisfies M5 | `T2`, `T3`, `T12` |
| `E2` missing bounded-evidence cue gets a concise fix | `T3`, `T7`, `T8` |
| `E3` implementation handoff avoids broad state discovery | `T5` |
| `E4` review safety remains intact | `T6`, `T11` |
| `E5` no broad rewrite | `T1`, `T7`, `T10` |
| `E6` dynamic benchmark comparison is conditional | `T9`, `T12` |
| `E7` material behavior change escalates proof | `T9`, `T12` |
| `E8` generated adapter bodies remain out of source | `T10`, `T12` |

## Edge case coverage

| Edge case | Coverage |
|---|---|
| `EC1` high-cost skill already satisfies M5 | `T2`, `T12` |
| `EC2` quick guide exists but bounded-evidence escape is missing | `T3`, `T7`, `T8` |
| `EC3` `implement` contains conflicting broad milestone search cue | `T5`, `T8` |
| `EC4` `code-review` compression would remove safety behavior | `T6`, `T11` |
| `EC5` reviewer requests dynamic benchmark proof for no-change audit | `T9` |
| `EC6` release or adapter packaging confusion is discovered | `T10` |
| `EC7` validator would assert exact full-sentence prose | `T8` |
| `EC8` broad search or large command output incident occurs | `T9`, `T10`, `T12` |

## Acceptance criteria coverage map

| Acceptance criterion | Covered by |
|---|---|
| Plan/test spec treats completed progressive-loading work as baseline | `T1`, `T2` |
| `workflow`, `implement`, and `code-review` are audited before implementation edits | `T2` |
| Any unchanged high-cost skill has recorded no-change rationale | `T2`, `T12` |
| Any touched high-cost skill preserves quick guide, targeted reading, bounded-evidence escape, and claim boundaries | `T3`, `T4`, `T5`, `T6` |
| `implement` preserves active-plan `Current Handoff Summary` first behavior | `T5` |
| `code-review` preserves independent review, material-finding, review recording, and review-resolution safety behavior | `T6`, `T11` |
| No generated public adapter skill bodies are reintroduced as tracked authored source | `T10` |
| No release, adapter, selector, broad-smoke, benchmark-suite, token-report-schema, or hard-token-gate behavior changes are introduced | `T10` |
| Static skill validation and token measurement requirements are selected according to whether canonical skill text changes | `T8` |
| Dynamic benchmark comparison is required only when required or when runtime improvement is claimed | `T9` |
| Safety-critical review, verification, material-finding, release, and milestone-handoff guidance is preserved | `T6`, `T11`, `T12` |

## Milestone coverage map

| Milestone | Coverage |
|---|---|
| `M1. High-cost skill audit and minimal follow-through` | `T1`-`T12` |

## Test cases

### T1. M5 scope preserves the completed baseline

- Covers: `R1`, `R2`, `R15`, `R27`, `E5`
- Level: contract, manual
- Fixture/setup:
  - approved M5 spec
  - active M5 plan
  - completed progressive-loading plan and report
  - final implementation diff
- Steps:
  - Confirm implementation treats the completed progressive-loading proposal, spec, plan, proof, and optimization report as baseline authority.
  - Confirm changed files are limited to high-cost skill audit/follow-through, directly required proof, and lifecycle bookkeeping unless a later accepted artifact broadens scope.
  - Confirm no broad rewrite of every public skill appears in the diff.
  - Confirm any work discovered outside M5 is stopped or routed to a separate accepted artifact.
- Expected result: M5 remains a follow-through slice, not a second progressive-loading implementation.
- Failure proves: M5 reopened completed optimization work or absorbed unrelated workstreams.
- Automation location: manual final diff review, active plan affected-surface table, `git diff --name-only`.

### T2. High-cost skills are audited before edits and decisions are recorded

- Covers: `R1`, `R3`-`R5`, `R29`, `E1`, `EC1`
- Level: contract, manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - active M5 plan
  - change metadata or explain-change evidence
- Steps:
  - Confirm each high-cost skill has an audit result before implementation edits are justified.
  - Confirm each high-cost skill is recorded as unchanged with rationale, changed with rationale, or blocked/deferred with owner.
  - Confirm unchanged skills have contributor-visible no-change rationale.
  - Confirm changed skills identify the concrete M5 gap fixed.
- Expected result: Every high-cost skill has a traceable M5 decision before implementation handoff.
- Failure proves: M5 changed or relied on skill behavior without an audit-backed decision.
- Automation location: manual review of active plan, change metadata, explain-change, or equivalent tracked evidence.

### T3. Touched high-cost skills preserve quick guides and bounded-evidence escapes

- Covers: `R6`-`R8`, `E1`, `E2`, `EC2`
- Level: static, manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Run `python scripts/test-skill-validator.py`.
  - Confirm each touched high-cost skill has `## Quick operating guide` or an equivalent targeted top entry point.
  - Confirm each touched high-cost skill preserves targeted reading cues before broad reads.
  - Confirm each touched high-cost skill preserves broader-section or full-file escape behavior when narrower evidence is incomplete, contradictory, or insufficient.
  - Confirm any new proof uses stable section or term checks rather than exact full-sentence prose unless exact text is the contract.
- Expected result: High-cost skills remain progressively loadable without encouraging under-reading.
- Failure proves: M5 weakened quick-guide, targeted-reading, or full-context escape behavior.
- Automation location: `python scripts/test-skill-validator.py`, manual skill diff review.

### T4. `workflow` keeps routing and claim-boundary behavior

- Covers: `R9`, `R13`, `R14`, `R30`
- Level: contract, manual
- Fixture/setup:
  - `skills/workflow/SKILL.md`
  - `docs/workflows.md`
  - final implementation diff
- Steps:
  - Confirm `workflow` routes to specialized stage skills instead of replacing them.
  - Confirm source-of-truth order, stop conditions, and stage-owned claim boundaries remain present.
  - Confirm `docs/workflows.md` remains the full bounded-evidence, workflow-routing, artifact-location, and follow-up-routing guide.
  - Confirm `workflow` does not copy the full evidence sequence or long templates from `docs/workflows.md`.
- Expected result: `workflow` remains a compact router with safety boundaries and a clear owner surface for full workflow rules.
- Failure proves: M5 duplicated workflow-guide detail or weakened routing and claim boundaries.
- Automation location: manual contract review, `scripts/test-skill-validator.py` where existing checks apply.

### T5. `implement` starts from active handoff state and blocks contradictory state

- Covers: `R7`, `R10`, `R11`, `E3`, `EC3`
- Level: static, manual
- Fixture/setup:
  - `skills/implement/SKILL.md`
  - active plan with `Current Handoff Summary`
  - `scripts/test-skill-validator.py`
- Steps:
  - Run `python scripts/test-skill-validator.py`.
  - Confirm `implement` directs milestone readiness and handoff checks to start from the active plan `Current Handoff Summary` when a plan exists.
  - Confirm `implement` points next to the current milestone section and validation notes.
  - Confirm missing, stale, or contradictory milestone state is treated as a blocker.
  - Confirm `implement` does not instruct agents to infer current state from broad repository searches before active-plan inspection.
- Expected result: Implementation handoff remains active-plan first and blocks unsafe inferred state.
- Failure proves: M5 preserved or introduced a broad state-discovery path for implementation readiness.
- Automation location: `python scripts/test-skill-validator.py`, manual review of `skills/implement/SKILL.md`.

### T6. `code-review` preserves protected review contracts

- Covers: `R12`, `R16`, `E4`, `EC4`
- Level: static, manual
- Fixture/setup:
  - `skills/code-review/SKILL.md`
  - `scripts/test-skill-validator.py`
  - final implementation diff
- Steps:
  - Run `python scripts/test-skill-validator.py`.
  - Confirm independent-review mode remains present.
  - Confirm mixed-evidence caution, material-finding requirements, review recording, review-resolution routing, milestone-aware handoff, stop conditions, and result-claim boundaries remain present.
  - Confirm any compression or clarification does not delete safety-critical review behavior solely to reduce static size.
- Expected result: `code-review` stays progressively loadable while preserving formal review safety.
- Failure proves: M5 weakened safety-critical review obligations.
- Automation location: `python scripts/test-skill-validator.py`, manual review of `skills/code-review/SKILL.md`.

### T7. Minimal wording changes stay concise, local, and project-portable

- Covers: `R5`, `R13`, `R14`, `R30`, `E2`, `E5`, `EC7`
- Level: contract, security/privacy, manual
- Fixture/setup:
  - touched high-cost skill files
  - `docs/workflows.md`
  - final implementation diff
- Steps:
  - Confirm each skill edit fixes a concrete M5 gap with the smallest sufficient wording or structure change.
  - Confirm skill wording stays local and concise, without copying the full `docs/workflows.md` evidence sequence.
  - Confirm public skill wording does not expose generated mirror paths, adapter package internals, selector path constraints, drift-check mechanics, shared-block mechanics, host-specific examples, private usernames, secrets, or local-only debug details.
  - Confirm no new reusable shared template is introduced for M5 wording.
- Expected result: Any skill edit is small, useful to the skill reader, and safe to publish.
- Failure proves: M5 added public skill churn, copied maintainer-only mechanics, or created another template surface.
- Automation location: manual security/privacy review, `python scripts/validate-skills.py` if skill text changes.

### T8. Static proof and token measurement match the changed surfaces

- Covers: `R17`, `R20`-`R22`, `R25`, `EC7`
- Level: static, selected integration
- Fixture/setup:
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/measure-skill-tokens.py`
  - final changed path set
- Steps:
  - Run `python scripts/test-skill-validator.py` whenever static skill-proof behavior is relied on.
  - If canonical skill text changes, run `python scripts/validate-skills.py`.
  - If canonical skill text changes, run `python scripts/measure-skill-tokens.py` or record an explicit plan/test-spec rationale for not running it.
  - Confirm static token measurement remains diagnostic and warning-only.
  - Confirm new or changed validator proof uses stable behavior cues, section presence, required terms, or forbidden sequences instead of exact full-sentence prose unless exact text is the contract.
- Expected result: Proof scope follows the changed surfaces without adding brittle prose lint or hard token gates.
- Failure proves: M5 either under-validates skill changes or turns diagnostics into enforcement.
- Automation location: `python scripts/test-skill-validator.py`, `python scripts/validate-skills.py` when skill text changes, `python scripts/measure-skill-tokens.py` when skill text changes.

### T9. Dynamic benchmarks and lifecycle summaries remain conditional

- Covers: `R23`, `R24`, `R28`, `E6`, `E7`, `EC5`, `EC8`
- Level: contract, manual, conditional e2e
- Fixture/setup:
  - active M5 plan
  - final implementation diff
  - explain-change evidence
  - optional dynamic benchmark evidence if required
- Steps:
  - Confirm before/after dynamic benchmark comparison is not required for no-change rationale or small wording-only work.
  - Confirm explain-change or the active plan states why dynamic benchmark comparison was not run when it is omitted.
  - If the change claims runtime benchmark improvement, confirm targeted dynamic benchmark evidence supports the claim.
  - Confirm lifecycle token-cost summary creation is required only if an approved M4 trigger is named, such as a relevant broad-search incident, benchmark warning, release change, large workflow-governance change, or maintainer request.
  - If a broad-search or large command-output incident occurs and is relevant, confirm the M4 lifecycle-summary trigger decision is recorded.
- Expected result: M5 avoids routine benchmark/report overhead while requiring evidence for runtime-improvement claims or triggered summaries.
- Failure proves: M5 either over-measures routine work or claims runtime benefit without evidence.
- Automation location: manual plan/explain-change review; targeted dynamic benchmark command only if required by plan/test spec or runtime-improvement claim.

### T10. Release, adapter, selector, generated-output, benchmark, and follow-up boundaries stay intact

- Covers: `R17`-`R19`, `R26`-`R30`, `E8`, `EC6`, `EC8`
- Level: contract, selected integration, manual
- Fixture/setup:
  - final implementation diff
  - active M5 plan
  - change metadata
  - selected validation output
- Steps:
  - Confirm no release validation, adapter packaging, generated public adapter body tracking, selector behavior, broad-smoke trigger, benchmark-suite, token-cost report schema, or hard-token-gate behavior changes appear in the diff.
  - Confirm generated public adapter skill bodies are not added back as tracked source.
  - Confirm `skills/` remains the authored skill source.
  - Confirm follow-ups discovered during M5 route through the active plan, review-resolution, learn, proposal, or follow-up ownership surface instead of chat-only notes.
  - Confirm affected and intentionally unaffected surfaces are recorded for `workflow`, `implement`, `code-review`, generated adapter output, release behavior, selector behavior, benchmark behavior, and lifecycle token-cost summary behavior.
- Expected result: M5 preserves completed PR #52 and PR #53 boundaries and does not change excluded surfaces.
- Failure proves: M5 leaked into release, adapter, selector, benchmark, generated-output, hard-gate, or follow-up ownership work.
- Automation location: selected validation output, `git diff --name-only`, manual final diff review.

### T11. Safety-critical guidance is preserved despite cost pressure

- Covers: `R12`, `R16`, acceptance safety criteria
- Level: contract, manual
- Fixture/setup:
  - before/after high-cost skill diff
  - active M5 plan
  - code-review record
- Steps:
  - Confirm no review, verification, material-finding, release, validation, or milestone-handoff guidance is removed solely to reduce size.
  - Confirm any moved or summarized safety detail has an approved owner surface and rationale.
  - Confirm `code-review` and `verify` readiness claims remain owned by their stages.
  - Confirm any remaining size warning is accepted or explained rather than fixed by unsafe deletion.
- Expected result: M5 reduces or preserves cost without weakening rigor.
- Failure proves: Token-cost pressure caused a safety regression.
- Automation location: manual code-review checklist, explain-change rationale, verify checklist.

### T12. Lifecycle state, selected validation, and final proof stay coherent

- Covers: `R1`-`R30`
- Level: selected integration, lifecycle, manual
- Fixture/setup:
  - approved M5 spec
  - active M5 test spec
  - active M5 plan
  - `docs/plan.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
  - final changed path set
- Steps:
  - Confirm the active plan's `Current Handoff Summary`, `docs/plan.md`, change metadata, and this test spec agree on current stage and readiness.
  - Run selected validation for the final changed path set.
  - Run change metadata validation after lifecycle or change metadata edits.
  - Run artifact lifecycle validation for touched lifecycle artifacts.
  - Run selected CI for the final changed path set.
  - Run `git diff --check --`.
  - Confirm final explain-change and verify evidence, before PR, address no-change rationale, affected/unaffected surfaces, dynamic benchmark rationale, and any triggered lifecycle-summary decision.
- Expected result: The M5 branch is traceable from spec to plan to test spec to implementation evidence and final verification.
- Failure proves: Lifecycle state or validation evidence drifted from the implemented slice.
- Automation location:
  - `python scripts/select-validation.py --mode explicit --path <changed-path> ...`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <lifecycle-path> ...`
  - `bash scripts/ci.sh --mode explicit --path <changed-path> ...`
  - `git diff --check --`

## Fixtures and data

- Canonical high-cost skills:
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
- Governing and lifecycle artifacts:
  - `specs/cost-bounded-rigor-m5-progressive-loading-follow-through.md`
  - `specs/cost-bounded-rigor-m5-progressive-loading-follow-through.test.md`
  - `docs/plans/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through.md`
  - `docs/plan.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/change.yaml`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/review-log.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/spec-review-r1.md`
  - `docs/changes/2026-05-14-cost-bounded-rigor-m5-progressive-loading-follow-through/reviews/plan-review-r1.md`
- Proof scripts:
  - `scripts/test-skill-validator.py`
  - `scripts/validate-skills.py`
  - `scripts/measure-skill-tokens.py`
  - `scripts/select-validation.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/ci.sh`
- Historical baseline evidence:
  - `specs/progressive-loading-high-cost-public-skills.md`
  - `specs/progressive-loading-high-cost-public-skills.test.md`
  - `docs/plans/2026-05-11-progressive-loading-high-cost-public-skills.md`
  - `docs/reports/token-cost/optimizations/2026-05-11-progressive-loading-high-cost-skills.md`

No synthetic fixture data is required for M5 unless implementation changes `scripts/test-skill-validator.py`. If static proof is added, use small inline text fixtures that exercise section presence, required terms, and forbidden sequences.

## Mocking/stubbing policy

Do not mock repository files for final proof. Static helper tests may use small inline skill-body strings to prove helper behavior, but canonical validation must read the real `skills/workflow/SKILL.md`, `skills/implement/SKILL.md`, and `skills/code-review/SKILL.md` files.

Do not stub validation selector, skill validation, token measurement, or CI wrapper behavior for readiness claims. Use the repository-owned scripts named by this test spec.

## Migration or compatibility tests

M5 has no data migration. Compatibility proof is boundary-based:

- existing workflow stage order remains unchanged;
- existing selector behavior and broad-smoke triggers remain unchanged;
- existing release validation and adapter packaging behavior remain unchanged;
- existing generated public adapter tracking remains unchanged;
- existing progressive-loading proof remains historical baseline evidence;
- public skill wording remains project-portable.

Use `T10` and `T12` for compatibility proof.

## Observability verification

M5 is observed through tracked artifacts and validation evidence, not runtime logs or metrics.

Required observable evidence:

- high-cost skill audit result;
- no-change rationale or minimal diff rationale for every high-cost skill;
- affected and intentionally unaffected surface record;
- selected validation output;
- `scripts/test-skill-validator.py` output when static skill-proof behavior is relied on;
- `scripts/validate-skills.py` and `scripts/measure-skill-tokens.py` output, or explicit no-run rationale, when canonical skill text changes;
- dynamic benchmark evidence only when required or when runtime improvement is claimed;
- explain-change and verify evidence before PR.

## Security/privacy verification

Use `T7` and `T10` to verify that public skill wording does not include secrets, credentials, private paths, usernames, host-specific workarounds, debug-only data, generated mirror paths, adapter package internals, selector path constraints, drift-check mechanics, shared-block mechanics, or local-only examples.

No additional security tooling is required unless implementation touches security-sensitive workflow, review, release, or packaging behavior. Such changes are out of M5 scope and must route to a separate accepted artifact.

## Performance checks

Static token measurement is diagnostic and warning-only for M5.

- If canonical skill text changes, run `python scripts/measure-skill-tokens.py` or record an explicit plan/test-spec rationale for not running it.
- If canonical skill text does not change, dynamic benchmarks and static token measurement are not required; record the no-run rationale in the active plan or explain-change.
- If runtime benchmark improvement is claimed, run targeted dynamic benchmark comparison and cite the evidence.
- Do not add hard token thresholds, hard CI gates, or release blockers based on token totals in this slice.

## Manual QA checklist

- [ ] `workflow`, `implement`, and `code-review` were audited before edits.
- [ ] Every high-cost skill has unchanged, changed, or blocked/deferred rationale.
- [ ] `workflow` still routes rather than replacing specialized stage skills.
- [ ] `implement` still starts handoff inspection from active plan `Current Handoff Summary` when a plan exists.
- [ ] `code-review` still preserves independent review, material findings, review recording, review-resolution routing, milestone handoff, and result boundaries.
- [ ] Any skill edit is concise, local, and project-portable.
- [ ] `docs/workflows.md` remains the full bounded-evidence and routing guide.
- [ ] No generated public adapter skill bodies are tracked.
- [ ] No release, adapter, selector, broad-smoke, benchmark-suite, report-schema, dynamic-benchmark, or hard-token-gate behavior was added unless a later accepted artifact explicitly scoped it.
- [ ] Dynamic benchmark comparison is omitted only with rationale or included with targeted evidence.
- [ ] Lifecycle token-cost summary behavior follows M4 trigger rules.
- [ ] The active plan, `docs/plan.md`, this test spec, and change metadata agree on readiness.

## What not to test

- Do not rerun the full standalone progressive-loading implementation test plan unless M5 explicitly changes that behavior.
- Do not run release validation, adapter validation, generated adapter archive checks, or adapter package distribution tests unless implementation touches those surfaces.
- Do not run broad smoke by default; use selected validation unless an authoritative trigger appears.
- Do not run dynamic benchmarks for no-change rationale or small wording-only work.
- Do not test semantic trigger inference for lifecycle token-cost summaries; M4 keeps those triggers reviewer or artifact owned.
- Do not add natural-language scoring or exact full-sentence prose checks for skill wording unless exact text is the contract.
- Do not test generated public adapter skill bodies as authored skill truth.

## Uncovered gaps

None. Every M5 `MUST` requirement maps to static proof, selected validation, manual contract review, no-change rationale, conditional benchmark evidence, or lifecycle verification.

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

This test spec is active and maintainer-approved. Implementation may start under the active M5 plan.
