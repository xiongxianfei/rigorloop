# Vision Skill Quality Refinement

## Status

- accepted

## Problem

The first real `vision` skill run produced a valid project vision, but it needed multiple review passes to become sharp. The initial draft obeyed the guardrails in `skills/vision/SKILL.md`, yet it missed quality points that reviewers could predict: a comparative differentiator, embedded pain points, concrete commitments, and observable falsifiability.

That pattern shows a gap in the skill. It is strong at forbidding bad outputs, but weaker at coaching a strong first draft. The skill also repeats edit-authorization guidance across several sections, uses soft "remind" wording for substantive revision traceability, and keeps foundational workflow-fit guidance too low in the file.

Without refinement, future vision runs can remain technically compliant while still requiring avoidable review cycles.

## Goals

- Make the `vision` skill produce stronger first drafts by adding pointed drafting heuristics.
- Reduce overlapping guidance around modes, source of truth, and overwrite protection.
- Make substantive revision traceability enforceable rather than advisory.
- Move workflow-fit guidance near the top so readers understand that `vision` is upstream of the lifecycle.
- Preserve the approved project-vision contract, README marker boundary, and proposal-fit model.
- Refresh generated skill and adapter output only through the existing generators when canonical skill guidance changes.

## Non-goals

- Revising the approved root `vision.md`.
- Adding `vision` to the normal per-change lifecycle.
- Changing the README marker contract or adding a README mirror helper script.
- Weakening README front-matter ownership by making README independently authoritative.
- Naming specific competitor tools in the durable skill contract.
- Changing the 500-word cap or required section order in the first refinement unless spec review explicitly requests it.
- Extracting or consolidating shared evidence-collection guidance across skills.
- Hand-editing generated `.codex/skills/` or `dist/adapters/` output.

## Vision fit

fits the current vision

This proposal strengthens the current vision without changing project scope.

- It supports the pitch that RigorLoop keeps reasoning, tests, and verification visible enough for human review by improving the skill that produces the canonical project vision.
- It reinforces the differentiator that durable artifacts should let reviewers inspect, diff, and improve decisions instead of relying on chat history.
- It advances the commitment to concrete evidence over process theater by replacing soft traceability wording with an enforceable causal-link rule for substantive vision revisions.
- It respects the refusal to become a broader platform or project-management suite by keeping the change inside the vision skill, governing spec, test spec, and generated skill outputs.

## Context

`vision.md` now exists and is approved as the canonical project vision. Its creation showed that the current skill can enforce shape, source-of-truth behavior, and README mirroring, but does not actively ask the questions that distinguish a competent vision from a useful one.

The approved `specs/vision-skill.md` already defines the current contract. It includes the three modes, README marker behavior, `Vision fit`, source-of-truth order, generated-output boundaries, and privacy/research rules. It also contains the current soft traceability requirement for substantive revisions: the skill reminds contributors to record the causal link when a change-local pack exists.

## Options considered

### Option 1: Leave the vision skill unchanged

Advantages:

- no new spec, plan, or generated-output work;
- preserves the just-implemented skill contract exactly;
- smallest immediate diff.

Disadvantages:

- leaves the drafting-quality gap observed during the first `vision` run;
- keeps overlapping edit-permission guidance in the skill;
- leaves the substantive-revision traceability rule under-specified;
- misses a low-risk chance to turn review lessons into durable guidance.

### Option 2: Patch only the vision skill wording

Advantages:

- focused diff;
- directly addresses the most visible skill;
- lowest coordination cost;
- lowest implementation cost among options that change behavior.

Disadvantages:

- may drift from `specs/vision-skill.md` unless the spec and test spec are updated too;
- can make the skill look improved without making the governing contract stronger.

### Option 3: Refine the vision skill contract

Advantages:

- adds the highest-value drafting heuristics where the observed failure happened;
- updates the spec and test spec so the skill contract stays reviewable;
- consolidates mode/source/protection guidance without changing the approved modes;
- changes "remind" into an enforceable substantive-revision traceability rule.

Disadvantages:

- broader than a single wording cleanup;
- likely touches canonical skill, spec, test spec, generated skill output, and generated adapter output;
- needs careful review so readability cleanup does not weaken safety rules.

## Recommended direction

Choose Option 3.

The first refinement should update the `vision` skill and its governing artifacts, not just the generated local Codex copy. The core change is a new `Drafting heuristics` section between vision content rules and README front-matter behavior. It should use pointed questions rather than additional content rules, for example:

- Differentiator: what alternative class is the project different from, and what tradeoff does it make?
- Pain points: what problem makes this vision necessary, and is that pain embedded in the differentiator instead of bolted on?
- Commitments: can each commitment be checked in a future review?
- Falsifiability: can someone observe the failure condition from behavior or artifacts?
- Audience: does the audience statement rule out at least one plausible non-fit?
- Refusals: are refusals concrete enough to block misaligned proposals?

The mode guidance should be made faster to compare, preferably as a compact table covering when the mode applies, what may be edited, README behavior, and stop conditions. Source-of-truth and overwrite-protection text should be consolidated into one edit-authorization section so the skill states the rule once: `CONSTITUTION.md` outranks `vision.md`; `vision.md` outranks README front-matter; create, revise, and mirror are the only edit paths; existing visions are not overwritten without clear revise or mirror intent.

The workflow-fit statement should move near the top of the skill, immediately after the opening explanation, because it tells the reader what kind of artifact this is before they read detailed mode rules.

The substantive revision rule should become enforceable. If a substantive revision is tied to an existing or required change-local pack, the skill should require the causal link in `docs/changes/<change-id>/change.yaml` and `docs/changes/<change-id>/explain-change.md` before finalizing. Editorial revisions and mirror-only updates should remain exempt from creating a new change-local pack solely because the skill ran.

The first slice can still simplify `vision` where the same edit-authorization rule is repeated inside the skill itself.

The optional competitor-name advice should not become a required rule. The durable heuristic should ask for an alternative class or specific tool, leaving the author free to avoid naming competitors when doing so would date the vision or create unnecessary positioning risk.

The 500-word cap and section order should stay unchanged for this refinement. They were not the cause of the observed quality gap, and relaxing them would make the scope larger without clear evidence.

## Expected behavior changes

- Future `vision create` and `vision revise` runs ask sharper drafting questions before producing or finalizing vision text.
- Vision drafts are more likely to include comparative positioning, pain points, concrete commitments, and observable falsifiability on the first pass.
- The skill is easier to scan because mode behavior and edit authorization are less repetitive.
- Substantive vision revisions have a clear traceability gate when a change-local pack exists or is required.
- Workflow-fit guidance is visible before detailed mechanics.

## Architecture impact

This is a workflow-artifact and generated-output change, not a new runtime architecture.

Likely touched surfaces:

- `specs/vision-skill.md` for the revised contract;
- `specs/vision-skill.test.md` for coverage of drafting heuristics, enforceable traceability, and consolidated mode/edit guidance;
- `skills/vision/SKILL.md` as the canonical authored skill;
- generated `.codex/skills/vision/SKILL.md` through `scripts/build-skills.py`;
- generated adapter skill output under `dist/adapters/` through `scripts/build-adapters.py`.

No data store, service boundary, deployment boundary, adapter package composition change, or architecture package is expected.

## Testing and verification strategy

Verification should focus on contract drift, generated-output drift, and content-level proof for the new skill behavior.

Likely checks:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-adapters.py --version 0.1.1
python scripts/select-validation.py --mode explicit --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md
bash scripts/ci.sh --mode explicit --path specs/vision-skill.md --path specs/vision-skill.test.md --path skills/vision/SKILL.md
```

Manual review should confirm that the skill still protects existing `vision.md`, does not broaden README edits, and does not turn `vision` into a normal lifecycle stage.

## Rollout and rollback

Rollout should proceed through the normal non-trivial lifecycle because the change affects a workflow skill, specs, generated output, and possibly adapter distribution.

Recommended sequence:

1. proposal-review;
2. spec and spec-review;
3. plan and plan-review;
4. test-spec;
5. implementation with generated-output refresh;
6. code-review, verify, explain-change, and PR.

Rollback is straightforward: revert the touched canonical artifacts and regenerate `.codex/skills/` and adapter output.

## Risks and mitigations

- Risk: The heuristics become hidden requirements and make vision writing over-constrained.
  Mitigation: phrase them as drafting questions, while keeping the actual content rules in the existing contract sections.

- Risk: Consolidating edit-authorization wording accidentally weakens overwrite protection.
  Mitigation: keep existing stop conditions as explicit test-spec cases.

- Risk: Enforceable traceability creates artifact churn for small wording changes.
  Mitigation: keep editorial revisions and mirror-only updates exempt from new change-local packs.

- Risk: The proposal grows into a broad skill-platform rewrite.
  Mitigation: keep the first slice centered on the observed `vision` drafting and rule-clarity gaps.

## Open questions

None.

## Decision log

- 2026-04-30: Draft proposal recommends a vision-skill quality refinement with drafting heuristics, consolidated edit/mode guidance, and enforceable substantive-revision traceability.
- 2026-04-30: Accepted after proposal review found no material findings. The direction proceeds to a draft update of `specs/vision-skill.md`.

## Next artifacts

- `proposal-review` for this proposal.
- If accepted, `specs/vision-skill.md` update.
- Matching `specs/vision-skill.test.md` update.
- Execution plan under `docs/plans/`.

## Follow-on artifacts

- Draft spec update: `specs/vision-skill.md`

## Readiness

Accepted and ready for `spec`.
