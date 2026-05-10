# Learn Session: Skill Token Measurement Scope Narrowing

## Frame

- Trigger: contributor asked why the skill token-cost optimization work only optimized skills even though the initial goal set included static skill cost measurement, runtime tool-output amplification measurement, Codex JSONL session cost measurement, and identifying largest cost drivers before optimizing skill text.
- Trigger type: explicit contributor observation / retrospective.
- Scope: `2026-05-09-skill-token-cost-optimization` proposal, spec, plan, change evidence, and prior context-budget learn evidence.
- Session path: `docs/learn/sessions/2026-05-10-skill-token-measurement-scope-narrowing.md`
- Evidence in scope:
  - `docs/proposals/2026-05-09-skill-token-cost-optimization.md`
  - `specs/skill-token-cost-optimization.md`
  - `docs/plans/2026-05-09-skill-token-cost-optimization.md`
  - `docs/changes/2026-05-09-skill-token-cost-optimization/change.yaml`
  - `docs/changes/2026-05-09-skill-token-cost-optimization/explain-change.md`
  - `docs/learn/sessions/2026-05-09-context-budget-after-broad-search.md`
- Explicit exclusions:
  - No claim is made about unrecorded chat-only proposal drafts beyond the contributor's stated initial goal list.
  - This session does not reopen PR #39 or change the completed token-cost optimization artifacts.
  - This session does not create a new measurement proposal, telemetry spec, script, or workflow policy.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-09-context-budget-after-broad-search.md`
  - `docs/learn/sessions/2026-05-08-public-skill-surface-boundary.md`

## Observe

### O1: The durable proposal did not preserve the measurement goals as proposal goals

The contributor's stated initial goals include measuring static skill cost, runtime tool-output amplification, Codex JSONL session cost, and largest cost drivers before optimizing skill text. The accepted proposal artifact instead records goals centered on token-cost awareness in skills, bounded evidence collection, public portability, full-file-read escape conditions, and narrow validation.

Evidence:

- The proposal `Goals` section does not include static-cost measurement, runtime tool-output amplification measurement, Codex JSONL analysis, or pre-optimization cost-driver ranking.
- The proposal `Recommended direction` chooses tightening the existing skill contract and affected skills.
- The proposal `Testing and verification strategy` names skill-contract tests, skill validation, generated skill drift, adapter drift, and adapter validation, not measurement scripts or JSONL analysis.

### O2: The approved spec converted the change into a skill-contract amendment

The approved spec defines token-cost discipline as normalized skill behavior and requires the first implementation slice to update the skill contract, selected high-volume skills, static validation, generated skill output, and public adapters.

Evidence:

- `R1a` says token-cost discipline must be an amendment to the skill contract, not a new workflow stage.
- `R6` through `R6e` define the first implementation slice around the normative contract, selected high-volume stage skills, static proof, and no new token-budget skill.
- `R8` requires narrow static validation, not broad semantic quality scoring.
- `R9` requires generated output and public adapter validation when public skill text changes.
- The spec `Performance expectations` section says no exact token-count metric is required.

### O3: The execution plan correctly followed the narrowed spec, but the workflow failed to preserve the deferred measurement track

The plan's M1-M5 milestones implement the accepted spec: skill contract and static proof, shared evidence guidance and canonical skills, generated skill and adapter output, change evidence, and final verification. No milestone owns static measurement, runtime amplification measurement, JSONL cost analysis, or cost-driver ranking.

Evidence:

- The plan summary says the implementation tightens the skill contract, test coverage, shared evidence guidance, selected high-volume skills, generated skill output, and public adapters.
- The plan requirements table maps `R1`-`R10` only to skill-contract, skill guidance, validator, generated output, adapter, and review surfaces.
- The plan outcome records that M1-M4 closed and M5 verification passed for that narrowed scope.

### O4: The likely root cause is scope collapse during proposal/spec translation, not an implementation miss

Implementation did not ignore an approved measurement requirement. The measurement objectives were absent from the accepted proposal's goals, absent from the approved spec's requirements, absent from the plan milestones, and absent from acceptance criteria. That means the work became "make public skills more token-friendly" without a retained phase or follow-up for "measure first."

Evidence:

- Repository search found no static skill cost, Codex JSONL cost, runtime amplification, or largest cost-driver requirement in the active proposal/spec/plan/change pack for this initiative.
- The prior context-budget learn session supplied incident evidence for bounded evidence guidance but did not create measurement requirements or a measurement follow-up.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Candidate process-follow-up | Contributor question plus accepted proposal evidence | The durable proposal narrowed the recorded goals; the session can state that fact without changing policy. |
| O2 | observation | observation | None | Approved spec evidence | The approved spec explains why the implementation surface became skill-only. |
| O3 | observation | observation | None | Plan and change evidence | The implementation matched the approved narrowed contract. |
| O4 | process-follow-up | candidate process-follow-up | Candidate proposal for token-cost measurement | Contributor confirmation pending | A measurement track may be needed, but creating it requires contributor confirmation and a new action-owning artifact. |

## Route

No derivative artifact was routed from this session.

No topic entry was created. This is currently a scope-control observation and candidate follow-up, not a contributor-confirmed durable lesson or accepted policy change.

## Answer

The work only optimized skills because the accepted proposal/spec/plan no longer contained the measurement goals as binding scope. The approved contract became: add token-cost discipline to the skill contract, selected skills, validators, generated skill mirrors, and public adapters while preserving correctness.

The measurement goals should have been either preserved as requirements or explicitly split into a follow-up such as `token-cost-measurement-baseline`. Without that, the lifecycle artifacts gave implementation no mandate to add static skill cost measurement, runtime tool-output amplification measurement, JSONL session-cost analysis, or cost-driver ranking.

## Best Practices

- Preserve every initial goal through proposal review as one of: in-scope requirement, non-goal, deferred follow-up, or rejected option.
- When a proposal narrows from "measure and optimize" to "optimize guidance," record the measurement half as an explicit follow-up or make the narrowing visible in the decision log.
- Do not let "first implementation lightweight" silently become "only implement the cheapest half." Lightweight should mean a small slice with explicit remaining work.
- For optimization proposals, require a baseline decision: either measure first, use existing evidence as the baseline, or explicitly defer measurement with an owning follow-up.
- During spec review, check that proposal goals map to requirements, non-goals, or deferred follow-ups before approving.

## No-Durable-Route Rationale

This session records the mismatch and candidate process follow-up, but it does not change authoritative workflow or skill behavior. A new measurement track would need proposal/spec ownership before implementation.

## Follow-Ups

- Candidate follow-up: create a proposal for token-cost measurement baseline covering static skill cost, runtime tool-output amplification, Codex JSONL session cost, and cost-driver ranking before further optimization.
- No follow-up artifact was created in this session because contributor confirmation is pending.
