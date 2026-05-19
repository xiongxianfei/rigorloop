# Review Resolution: RigorLoop Published Skill Design Contract

## Scope

This record tracks material finding closeout for formal reviews of the RigorLoop published skill design contract change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: spec-review-r2
Review closeout: spec-review-r3
Review closeout: plan-review-r1

- Reviews covered: `proposal-review-r1`, `proposal-review-r2`, `spec-review-r1`, `spec-review-r2`, `spec-review-r3`, `plan-review-r1`
- Findings resolved: 8
- Unresolved findings: 0
- Final result: `RLSDC-PR1`, `RLSDC-PR2`, `RLSDC-PR3`, `RLSDC-PR4`, `SKC-PR1`, `SKC-PR2`, `SKC-PR3`, and `SKC-PR4` are accepted and resolved.

## Resolution Overview

| Finding ID | Disposition | Status | Resolution summary |
| --- | --- | --- | --- |
| RLSDC-PR1 | accepted | resolved | `Next artifacts` now names `spec amendment: specs/skill-contract.md` and adds a source-of-truth boundary preventing competing skill-contract specs. |
| RLSDC-PR2 | accepted | resolved | The self-containment rule now distinguishes repository-root internal paths from packaged skill-local resources and narrows validation wording. |
| RLSDC-PR3 | accepted | resolved | The first-slice boundary now states audit may record merge/retire candidates but cannot merge, retire, rename, remove, or change ownership. |
| RLSDC-PR4 | accepted | resolved | The testing strategy now defines first-slice routing tests as prompt fixtures and transcript-review inputs, not deterministic runtime model-selection CI proof. |
| SKC-PR1 | accepted | resolved | The spec now defines `baseline normalization first slice` and `published-skill design pilot`, and updates ambiguous first-slice references. |
| SKC-PR2 | accepted | resolved | The spec now states body `When to use` and `When not to use` sections do not replace `description` as the routing source. |
| SKC-PR3 | accepted | resolved | The spec now requires a routing coverage table for each changed published-skill design pilot skill. |
| SKC-PR4 | accepted | resolved | The spec now requires behavior-preservation notes and behavior-parity evidence for each changed pilot skill. |

## Common Resolution Metadata

- Owner: proposal and spec author
- Owning stage: proposal and spec
- Validation target: targeted readback of proposal/spec decisions and review closeout artifacts.
- Validation evidence: Targeted readback confirmed the proposal and spec record the accepted boundaries. `git diff --check` and targeted review-artifact validation were run after recording.

## Finding Details

### proposal-review-r1

Finding closeout for `proposal-review-r1`.

### proposal-review-r2

No material findings. Clean formal review approved the revised proposal for proposal-stage purposes. No disposition entries required.

### spec-review-r1

No material findings. Clean formal review approved the draft `specs/skill-contract.md` amendment for spec-stage purposes. No disposition entries required.

### spec-review-r2

Finding closeout for `spec-review-r2`.

### spec-review-r3

No material findings. Clean formal review approved the revised `specs/skill-contract.md` amendment for spec-stage purposes after `SKC-PR1` through `SKC-PR4` were resolved. No disposition entries required.

### plan-review-r1

No material findings. Clean formal review approved the execution plan for plan-stage purposes. Immediate next stage is `test-spec`. No disposition entries required.

### RLSDC-PR1 - Next spec path may create a competing skill-contract source

Finding ID: RLSDC-PR1
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Replace the separate permanent spec path with `spec amendment: specs/skill-contract.md` and add a source-of-truth boundary that allows any separate draft only as temporary or explicitly subordinate before implementation relies on it.
Rationale: The existing repository already has a normative skill-contract source, and this proposal should not create a competing source of truth.
Validation target: Confirm `Next artifacts` and the source-of-truth boundary name `specs/skill-contract.md` as normative.
Validation evidence: Targeted readback confirmed the proposal now names `spec amendment: specs/skill-contract.md` and says implementation must not rely on competing normative skill-contract specs.

### RLSDC-PR2 - `scripts/` is both encouraged and forbidden without distinguishing packaged resources from repo internals

Finding ID: RLSDC-PR2
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Revise the self-containment rule to make the forbidden list repository-root scoped and explicitly allow packaged `<skill>/references/`, `<skill>/scripts/`, and `<skill>/assets/` when included in adapter output and mapped in `SKILL.md`.
Rationale: Skill-local packaged resources are part of the published skill contract, while repository-root scripts are maintainer-only unless operating in this repository.
Validation target: Confirm self-containment and structural validation distinguish repository-root scripts from packaged skill-local scripts.
Validation evidence: Targeted readback confirmed the proposal now distinguishes RigorLoop repository-root internal paths from packaged skill-local resources and warns against blunt `scripts/` deny-lists.

### RLSDC-PR3 - The skill existence audit can imply merge/retire work outside the first slice

Finding ID: RLSDC-PR3
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add a skill merge/retire boundary stating the audit may record candidates but this proposal does not merge, retire, rename, remove, or change ownership of skills.
Rationale: Skill retirement can alter lifecycle stage ownership, artifact ownership, routing, adapter contents, and validation, which exceeds this proposal's first slice.
Validation target: Confirm first-slice boundary and open questions limit merge/retire work to candidate recording.
Validation evidence: Targeted readback confirmed the proposal now requires separate proposal or explicit spec amendment for actual skill merge, retirement, rename, removal, or ownership change.

### RLSDC-PR4 - Routing tests need a deterministic oracle boundary

Finding ID: RLSDC-PR4
Disposition: accepted
Status: resolved
Owner: proposal author
Owning stage: proposal
Chosen action: Add a routing-test oracle boundary that treats first-slice routing tests as prompt fixtures and transcript-review inputs unless a dedicated routing harness is approved.
Rationale: Realistic prompts are useful for coverage and transcript review, but automatic model skill selection is not a deterministic CI oracle without a harness.
Validation target: Confirm testing strategy states what first-slice routing evidence may prove and prohibits broad semantic scoring as a required CI gate.
Validation evidence: Targeted readback confirmed the proposal now limits first-slice routing tests to description coverage and transcript-review evidence unless an approved harness exists.

### SKC-PR1 - `first implementation slice` refers to two incompatible scopes

Finding ID: SKC-PR1
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add `Slice terminology` defining `baseline normalization first slice` and `published-skill design pilot`, then update ambiguous examples, requirements, invariants, boundary behavior, non-goals, and acceptance criteria.
Rationale: The historical seven-skill normalization slice and the new `proposal` / `proposal-review` pilot are different scopes and must not share an unqualified label.
Validation target: Confirm `specs/skill-contract.md` no longer uses ambiguous first-slice terminology for the new pilot.
Validation evidence: Targeted readback confirmed the spec defines both rollout labels and uses `published-skill design pilot` for R27 through R36 scope.

### SKC-PR2 - Mandatory body sections risk duplicating routing logic

Finding ID: SKC-PR2
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add R3m through R3o clarifying that body `When to use` and `When not to use` sections do not replace `description`, may summarize post-load scope, and should not be required to restate every trigger.
Rationale: The portable routing source remains frontmatter `description`; body scope guidance should not become duplicated routing contract text.
Validation target: Confirm R3 clarifies the relationship between body routing sections and `description`.
Validation evidence: Targeted readback confirmed R3m through R3o define the boundary.

### SKC-PR3 - Routing coverage validation is under-specified

Finding ID: SKC-PR3
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add R35e through R35g requiring a routing coverage table for each changed pilot skill and limiting static checks to table presence and bounded phrase coverage.
Rationale: Routing coverage needs a deterministic evidence surface without broad semantic scoring or unsupported model-selection claims.
Validation target: Confirm R35 defines routing coverage table fields and static-check boundaries.
Validation evidence: Targeted readback confirmed R35e through R35g require positive triggers, near misses, competing skills, and should-not-trigger prompt classes.

### SKC-PR4 - Behavior-preservation proof is not explicit enough for skill rewrites

Finding ID: SKC-PR4
Disposition: accepted
Status: resolved
Owner: spec author
Owning stage: spec
Chosen action: Add R36g through R36j requiring behavior-preservation notes, behavior-parity evidence, and a rule that structural validation alone is insufficient when behavior-significant wording changed.
Rationale: Structural conformance can pass while behavior-significant rules are weakened; the pilot needs explicit preservation evidence.
Validation target: Confirm R36 and acceptance criteria require preservation notes and behavior-parity evidence.
Validation evidence: Targeted readback confirmed R36g through R36j and acceptance criteria cover behavior-preservation and behavior-parity proof.
