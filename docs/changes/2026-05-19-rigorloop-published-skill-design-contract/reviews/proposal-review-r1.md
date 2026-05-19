# Proposal Review R1: RigorLoop Published Skill Design Contract

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: external proposal-review result provided in chat
Target: docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md
Status: changes-requested

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: RLSDC-PR1, RLSDC-PR2, RLSDC-PR3, RLSDC-PR4
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-log.md
- Review resolution: docs/changes/2026-05-19-rigorloop-published-skill-design-contract/review-resolution.md
- Open blockers: source-of-truth/spec placement, resource-path ambiguity, skill retirement scope, routing-test oracle
- Immediate next stage: proposal revision, then proposal-review rerun
- No automatic downstream handoff: this review does not start spec work automatically.

## Overall Verdict

Good direction, changes requested before spec.

The proposal has the right product frame: published RigorLoop skills should be lean, triggerable operating manuals, not pointers to maintainer-only repository documents. The proposal is not ready to advance unchanged because it risks creating a competing skill-contract spec, has ambiguity around repository-root `scripts/` versus packaged skill-local `scripts/`, lets the first audit imply merge/retire decisions without a safe route, and does not clearly define what routing tests can prove deterministically.

## Material Findings

### RLSDC-PR1 - Next spec path may create a competing skill-contract source

Finding ID: RLSDC-PR1
Severity: major
Location: `Next artifacts`
Evidence: The proposal named `specs/rigorloop-published-skill-design-contract.md` as the next spec while existing workflow guidance says the normative skill-contract source is already `specs/skill-contract.md`.
Required outcome: Preserve a single normative skill-contract source or explicitly define the relationship between the new spec and the existing skill-contract spec.
Safe resolution path: Prefer `spec amendment: specs/skill-contract.md`, or define any separate spec as temporary or subordinate to `specs/skill-contract.md`.

### RLSDC-PR2 - `scripts/` is both encouraged and forbidden without distinguishing packaged resources from repo internals

Finding ID: RLSDC-PR2
Severity: major
Location: resource placement, script policy, and self-containment rule
Evidence: The proposal encourages deterministic skill scripts while listing `scripts/` as a forbidden required dependency for normal operation.
Required outcome: Clarify that the forbidden path list applies to maintainer-only repository-root paths, not packaged skill resources.
Safe resolution path: Add a repository-root versus packaged-resource boundary and update validation wording to avoid a blunt deny-list that flags every `scripts/` mention.

### RLSDC-PR3 - The skill existence audit can imply merge/retire work outside the first slice

Finding ID: RLSDC-PR3
Severity: major
Location: rollout, first-slice boundary, and open questions
Evidence: The proposal says the rollout audit should classify skills as `keep`, `merge`, `rewrite`, or `retire`, and asks which skills should be merged or retired.
Required outcome: State that the first-slice audit may identify merge/retire candidates, but cannot merge or retire skills in this proposal.
Safe resolution path: Add a merge/retire boundary requiring a separate proposal or explicit spec amendment for actual skill merge, retirement, rename, removal, or ownership change.

### RLSDC-PR4 - Routing tests need a deterministic oracle boundary

Finding ID: RLSDC-PR4
Severity: major
Location: testing and verification strategy
Evidence: The proposal requires realistic routing prompt tests but does not define whether they prove static description coverage, transcript evidence, or runtime model auto-selection.
Required outcome: Define what routing tests are allowed to prove in the first slice.
Safe resolution path: Define first-slice routing tests as prompt fixtures and transcript-review inputs unless a dedicated approved routing harness exists, and prohibit broad semantic skill-prose scoring as a required CI gate in this slice.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The problem is clear: published skills must operate without maintainer-only repository context. |
| User value | pass | Better routing, portability, output consistency, and lower wasted context are concrete benefits. |
| Option diversity | pass | The proposal compares do-nothing, style-guide-only, strict universal template, and principles-plus-contract options. |
| Decision rationale | pass | Option 4 fits the need for consistency without forcing one body template on every skill. |
| Scope control | concern | Audit can imply merge/retire decisions; see `RLSDC-PR3`. |
| Architecture awareness | concern | Needs source-of-truth boundary with existing `specs/skill-contract.md`; see `RLSDC-PR1`. |
| Testability | concern | Routing tests need deterministic oracle boundary; see `RLSDC-PR4`. |
| Risk honesty | pass | The proposal names over-triggering, body bloat, validation ceremony, normative drift, and same-class recurrence. |
| Rollout realism | concern | Pilot is good, but merge/retire scope and spec source-of-truth must be narrowed. |
| Readiness for spec | changes-requested | Ready after the four material findings are addressed and rechecked. |

## Scope Preservation

Scope preservation result: pass.

The proposal preserves the requested design principles: skills as operating documentation, existence gate, routing-focused description, progressive disclosure, resource maps, scripts for deterministic work, validation only when warranted, realistic prompt tests, transcript iteration, examples and counterexamples, lack of surprise, and sparse hard constraints.

## Blocking Questions

1. Will this amend `specs/skill-contract.md`, or will a new spec be created as a subordinate extension?
2. Does the forbidden-path validator distinguish repository-root `scripts/` from packaged skill-local `scripts/`?
3. Will the first-slice audit only record merge/retire candidates, or can it act on them?
4. What exactly counts as passing a routing test in this slice: static description coverage, transcript evidence, model-selection harness, or some combination?

## Readiness

Not ready for spec as written. The direction is worth keeping. After the four fixes above, the proposal can be rerun through proposal review and then proceed to spec amendment if approved.
