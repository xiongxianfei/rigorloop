# Skill Token Cost Optimization

## Status

accepted

## Problem

RigorLoop skills now include evidence-collection guidance, but agents can still spend large context budget before they know which evidence matters. A single broad search or full-file read can inject thousands of irrelevant lines into the conversation, reducing the context left for the actual proposal, review, implementation, or verification work.

The recurring problem is not that validation is too strict. The problem is that skill instructions do not make low-token evidence collection a first-class operating contract. Agents may read broad surfaces early, print large command output, or scan generated and historical artifacts before using inventories, headings, stable IDs, counts, changed paths, and focused excerpts.

This creates real delivery cost:

- less context remains for the active task;
- reviews and implementation turns become noisier;
- relevant evidence is harder to distinguish from incidental matches;
- future agents may repeat the same broad searches because the durable artifact does not capture a better method.

## Goals

- Make token-cost awareness an explicit skill behavior, not only a workflow-doc recommendation.
- Preserve RigorLoop's correctness, traceability, and validation expectations.
- Prefer bounded evidence collection before broad reads across proposal, review, implementation, verification, and learn stages.
- Make skills guide agents toward path inventories, headings, stable IDs, counts, diffs, changed paths, and targeted excerpts before raw full-file output.
- Add reviewable guidance for when full-file reads are still required.
- Keep published skill text project-portable and avoid RigorLoop-internal maintainer details.
- Add narrow validation so future skill edits do not remove token-cost discipline from normalized skills.

## Non-goals

- Do not reduce required validation coverage to save tokens.
- Do not change workflow stage order.
- Do not change which artifacts are required for non-trivial changes.
- Do not replace formal review, verify, or PR evidence with chat-only summaries.
- Do not add broad semantic quality scoring for all skill prose.
- Do not make every skill include a long token-budget tutorial.
- Do not require downstream public skill users to know this repository's internal source, generated mirror, adapter, or validator paths.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to reviewable and reproducible AI-assisted delivery. Token-cost discipline makes agents more likely to preserve enough context to inspect governing artifacts, run the right proof, and explain the real diff without relying on noisy chat history.

## Context

`docs/workflows.md` already defines efficient evidence collection. It says to start with bounded extraction for large files, repeated scans, generated output, and validation logs; prefer headings, stable IDs, path lists, counts, and line citations; keep routine output around 40 lines with 80 lines as a warning threshold; and broaden to neighboring sections or full-file reads only when needed.

`specs/skill-contract.md` already makes evidence-reading guidance part of the skill contract, and many canonical skills have an `Evidence collection efficiency` section. The remaining gap is operational sharpness: the current wording does not consistently force agents to choose the lowest-cost sufficient evidence surface before broad reads.

A recent learn session, `docs/learn/sessions/2026-05-09-context-budget-after-broad-search.md`, recorded the incident pattern. A broad search returned large output into the conversation context; a follow-up broad search did the same. The lesson was that `max_output_tokens` is a safety rail, not a query design, and that agents should narrow immediately when a first broad search proves noisy.

This proposal does not rely on `docs/project-map.md`; no project map was present during proposal authoring.

## Options considered

### Option 1: Keep current guidance unchanged

Keep the existing `docs/workflows.md` and per-skill evidence-efficiency wording.

Advantages:

- No immediate churn in skill text or generated output.
- Existing guidance already points in the right direction.

Disadvantages:

- The same incident has recurred despite existing guidance.
- Agents may still treat broad search plus output caps as acceptable first-pass evidence collection.
- Reviewers lack a clear proposal/spec hook for asking that skills tighten token-cost behavior.

### Option 2: Add a separate token-budget skill

Create a new skill for context-budget management and ask agents to invoke it when context use becomes risky.

Advantages:

- Gives the behavior a visible owner.
- Could collect reusable tactics in one place.

Disadvantages:

- Adds another skill for behavior that should be embedded in every high-volume stage.
- Does not help before the agent chooses to invoke the new skill.
- Conflicts with the repository preference not to create one-off skills unless they own a distinct artifact, gate, review responsibility, recurring action, or approved operational process.

### Option 3: Tighten the existing skill contract and affected skills

Update the skill contract and normalized skill guidance so bounded evidence collection is mandatory behavior for high-volume evidence work, with concise per-skill wording and narrow validator coverage.

Advantages:

- Fixes the behavior where agents actually make the choice: inside each stage skill.
- Preserves validation semantics while reducing irrelevant context load.
- Avoids adding a new workflow stage or skill.
- Lets validators check for the presence of compact evidence-efficiency guidance without judging prose quality.

Disadvantages:

- Requires coordinated updates to specs, skills, tests, generated skill mirrors, and adapter output.
- Needs careful wording so public skills stay portable and do not expose repository-maintainer internals.

### Option 4: Add hard command-output limits to all validation and search scripts

Change scripts so they truncate or summarize output aggressively by default.

Advantages:

- Provides executable guardrails for repository-owned scripts.
- Could reduce accidental large validation logs.

Disadvantages:

- Does not cover ordinary shell searches or full-file reads.
- Risks hiding useful diagnostic output if applied too broadly.
- Treats the symptom after output is produced instead of improving evidence selection.

## Recommended direction

Choose Option 3.

RigorLoop should make low-token evidence collection part of the skill contract and skill operating model. The guiding rule should be:

```text
Find the smallest evidence surface that can answer the current question.
```

Skills should direct agents to use this order when evidence volume could be large:

```text
inventory or changed paths
headings or stable IDs
counts or matching line numbers
targeted excerpts
neighboring context
full-file read only when needed
```

The rule should not weaken correctness. If the whole artifact is the review target, if surrounding context controls interpretation, if bounded evidence conflicts, or if implementation depends on the whole contract, the skill should still require a full-file read.

The change should treat `max_output_tokens` as a guardrail only. Skills should guide the query itself toward low-volume output, for example `rg -l`, `rg --count-matches`, precise globs, stable IDs, and `sed -n` ranges after locating lines.

## Expected behavior changes

- Proposal, review, implementation, verification, and learn turns start with smaller evidence queries when working across large or repeated surfaces.
- Agents are expected to explain when they broaden from summaries or line citations to full-file reads.
- Skills no longer rely on generic "read relevant files" wording where the likely evidence surface is large.
- Reviewers can flag broad, noisy evidence collection as a process defect when it materially affects the task.
- Validation can check that normalized skills retain concise evidence-efficiency guidance without requiring a semantic prose scorer.

## Architecture impact

No runtime architecture impact is expected.

The change affects the workflow guidance and public skill contract surfaces:

- `specs/skill-contract.md`
- `specs/skill-contract.test.md`
- selected canonical `skills/*/SKILL.md`
- `docs/workflows.md` only if the existing summary needs tightening
- generated local skill mirror and public adapter output through the existing generators

This is a contributor-facing and public-skill behavior change, not a C4, arc42, system-boundary, data-flow, persistence, deployment, or ADR-method change. No architecture package update or ADR is expected unless later specification discovers a durable architecture decision.

## Testing and verification strategy

The later spec should map this proposal to narrow checks rather than broad natural-language scoring.

Likely validation:

- update skill-contract tests to confirm the token-cost guidance is represented in the normative spec and selected skill surfaces;
- check that normalized skills keep bounded-evidence wording for large files, repeated scans, generated output, and validation logs;
- check that the guidance preserves full-file-read escape conditions;
- run skill validation and skill regression tests;
- run generated skill drift checks after canonical skill changes;
- run adapter drift check and adapter validation when public skill text changes.

Expected command family:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
```

The final plan may add lifecycle, review-artifact, or selected CI commands after the spec defines the exact touched surfaces.

## Rollout and rollback

Roll out as a normal workflow-governance change:

1. Specify the token-cost behavior in `specs/skill-contract.md`.
2. Update tests before changing skill text where feasible.
3. Tighten the selected canonical skills.
4. Regenerate or check generated skill output and adapters.
5. Verify public skill portability remains intact.

Rollback is straightforward: revert the spec, test, skill, and generated-output changes from the PR. Because this proposal does not change runtime behavior or artifact schemas, rollback does not require migration.

Historical learn records and prior proposals remain valid evidence. They do not need migration.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Agents under-read important governing context to save tokens. | Preserve explicit full-file-read conditions and make correctness higher priority than token savings. |
| Skill text becomes longer while trying to optimize tokens. | Keep per-skill wording short and centralize the normative rule in the skill contract. |
| Validators become brittle prose checkers. | Use narrow phrase, section, or stable-ID checks rather than broad semantic scoring. |
| Public skills expose RigorLoop repository internals. | Keep maintainer-only paths and generator commands in specs, plans, tests, and contributor docs, not shipped skill text. |
| Adapter drift is missed after public skill changes. | Require adapter drift check plus adapter validation in the plan and verify stages. |
| Output truncation hides failures. | Do not change validation semantics; require omitted detail to be available through explicit verbose or focused commands. |

## Open questions

- Which skill set is the first implementation slice: all skills with existing `Evidence collection efficiency` sections, or only the highest-volume lifecycle skills?
- Should `docs/workflows.md` remain unchanged because it already has the right summary, or should it receive a small clarification that `max_output_tokens` is not query design?
- Should the first validator slice check only the normative spec and canonical skills, or also generated public adapter copies?
- Should command-output budgets remain guidance only, or should selected repository-owned scripts add summary-first default output in a later change?

None of these questions blocks proposal review. They should be settled in the feature spec.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-09 | Recommend tightening the existing skill contract instead of adding a new token-budget skill. | The behavior belongs inside each stage where evidence is gathered, and the repository avoids one-off skills. | Separate token-budget skill; unchanged guidance. |
| 2026-05-09 | Preserve full-file-read escape conditions. | Token savings must not weaken review correctness or implementation safety. | Hard "never full-read first" rule. |
| 2026-05-09 | Use narrow validation rather than prose scoring. | The project has already favored stable, reviewable checks over broad language-quality inference. | Semantic quality scoring across all skills. |

## Next artifacts

- Proposal review for this proposal.
- Feature spec for skill token-cost optimization if the proposal is accepted.
- Spec review before implementation because this changes workflow and public skill behavior.
- Test spec mapping token-cost requirements to concrete skill-contract and validator checks.
- Execution plan covering canonical skill updates, generated skill drift, adapter drift, and validation.

## Follow-on artifacts

- Proposal-review: approved on 2026-05-09 with no material findings; clean review settled artifact-locally.
- Feature spec: [Skill Token Cost Optimization](../../specs/skill-token-cost-optimization.md).

## Readiness

Accepted and handed off to `spec`.

Implementation-slice details are owned by the feature spec and later execution plan.
