# Proposal Review R1

Review ID: proposal-review-r1
Stage: proposal-review
Round: 1
Reviewer: Codex proposal-review skill
Target: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md
Status: changes-requested
Original review source: User-invoked `$proposal-review` on 2026-07-27.
Material findings: PBC-PR1, PBC-PR2, PBC-PR3
Scope-preservation result: pass
Immediate next stage: proposal revision
Automatic downstream handoff: none

## Result

- Skill: proposal-review
- Review status: changes-requested
- Material findings: PBC-PR1, PBC-PR2, PBC-PR3
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/proposal-review-r1.md
- Review log: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md
- Review resolution: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md#proposal-review-r1
- Open blockers: PBC-PR1, PBC-PR2, and PBC-PR3
- Immediate next stage: proposal revision

## Material Findings

## Finding PBC-PR1

Finding ID: PBC-PR1
Severity: major
Location: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md, Goals, Scope budget, Recommended Direction, Architecture Impact, Testing and Verification Strategy, and Open Questions
Evidence: The proposal promises to package every required boundary reference with each supported public skill at line 54, fixes the delivery scope at eight lifecycle skills at lines 103 and 183-184, and again names eight governed skills at lines 241 and 281. Its deterministic fixtures nevertheless cover proposal handoffs at lines 265-266 even though `proposal` and `proposal-review` are excluded, while lines 312-314 defer the supported skill list to the specification. The proposal therefore presents the skill boundary as both settled and open, and it does not distinguish all adapter-supported skills from the subset that must consume the shared reference.
Required outcome: Settle the governed-skill list at proposal level, state whether proposal-stage guidance is governed or only a non-normative fixture case, and define whether resource parity applies to all public skills or only explicit reference consumers.
Safe resolution path: Choose one coherent skill set and use it consistently in Goals, Scope budget, Recommended Direction, Architecture Impact, Testing and Verification Strategy, Rollout, and Open Questions. If `proposal` and `proposal-review` remain excluded, explain how pre-spec examples become discovery input without claiming those stages implement the boundary contract. Replace “each supported public skill” with an exact consumer rule.
needs-decision rationale: The proposal owner must decide the product scope during proposal revision; downstream specification must not silently choose which public skills carry the capability.

## Finding PBC-PR2

Finding ID: PBC-PR2
Severity: major
Location: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md, Goals, Options Considered, Ownership split, Testing and Verification Strategy, and Risks and Mitigations
Evidence: The proposal assigns semantic adequacy to independent review at lines 51 and 164 and reserves applicability, completeness, risk selection, and evidence adequacy to reviewers at line 210. It also requires semantic-review fixtures to distinguish structurally valid but substantively incomplete records at lines 272-273, while lines 275-277 prohibit agent-runtime execution and lines 304-305 prohibit validators from claiming semantic correctness. No remaining proof surface, reviewer-independence rule, expected evidence, or pass/fail claim is named for the semantic fixtures.
Required outcome: Define how the change will demonstrate that independent review can detect the intended omission classes without using deterministic validators or runtime certification, and bound exactly what that evidence proves.
Safe resolution path: Add a bounded manual or hybrid review exercise with named fixture inputs, an independent reviewer, expected material findings, durable review evidence, and an explicit non-generalization claim; alternatively narrow the acceptance claim to the presence and structural integrity of review guidance and remove the semantic-detection proof claim.
needs-decision rationale: The proposal owner must choose during proposal revision whether semantic-detection evidence is in scope or whether the proposal deliberately makes only a guidance-and-structure claim.

## Finding PBC-PR3

Finding ID: PBC-PR3
Severity: major
Location: docs/proposals/2026-07-27-portable-boundary-first-capability-for-published-skills.md, Next Artifacts
Evidence: Lines 329-334 place matching test-spec proof maps before architecture assessment and the execution plan, and defer all lifecycle reviews to a generic final step. The governing workflow requires proposal-review, then spec and spec-review, architecture and architecture-review when triggered, plan and plan-review, and only then test-spec and test-spec-review before implementation. This compatibility-sensitive, architecture-affecting proposal cannot leave those gates implicit or reordered.
Required outcome: Make the downstream artifact sequence conform to the governing lifecycle and name the required review gate immediately after each authored artifact.
Safe resolution path: Replace the numbered list with `spec amendments -> spec-review -> architecture assessment -> architecture-review -> execution plan -> plan-review -> test-spec amendments -> test-spec-review -> implementation`, preserving the proposal's requirement for independent review without collapsing it into one late step.
needs-decision rationale: The proposal owner must disposition the finding before review-driven revision; the required sequence itself is fixed by `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md`.

## Review Dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Problem clarity | pass | The proposal clearly separates portable boundary modeling from maintainer-only runtime certification. |
| User value | pass | A portable contract would improve traceability and omission detection for users of published skills. |
| Option diversity | pass | The proposal compares examples alone, full runtime certification, portable deterministic support, and per-adapter live evaluation. |
| Decision rationale | pass | Option 3 follows the stated portability, ownership, and claim-boundary criteria. |
| Scope control | block | PBC-PR1 leaves the governed skill and packaged-resource scope simultaneously fixed and open. |
| Architecture awareness | pass | Canonical resource ownership, adapter parity, validators, fixtures, and excluded runtime dependencies are visible. |
| Testability | block | PBC-PR2 leaves the central independent-semantic-review claim without a valid proof mechanism. |
| Risk honesty | pass | The proposal names boilerplate, Cartesian expansion, validator overclaiming, drift, false blocking, and runtime creep. |
| Rollout realism | concern | The prospective activation and coherent rollback are sound, but PBC-PR3 misorders the required pre-implementation artifacts and gates. |
| Readiness for spec | block | Resolve PBC-PR1 through PBC-PR3 and pass same-stage rereview first. |

## Scope Preservation Review

- Scope-preservation result: pass.

Every initial goal is visibly classified with an allowed treatment. The
progressive-disclosure goal is a `deferred follow-up` with a concrete route:
the separate proposal remains paused until this baseline is accepted and
implemented. No initial goal disappears. The separate scope-budget gate still
fails because PBC-PR1 leaves the current governed-skill boundary ambiguous.

## Blocking Questions

1. Does the capability govern exactly the named eight skills, or must
   `proposal` and `proposal-review` also carry stage-local guidance?
2. Must the semantic-review fixtures produce bounded independent human or
   hybrid review evidence, or should the semantic-detection claim be removed?
3. Will the proposal adopt the mandatory downstream artifact and review order
   before implementation?

## Recommended Proposal Edits

- Recommended edits: in `Goals`, replace “each supported public skill” with
  “each governed skill that declares the boundary reference in its Resource
  map,” then enumerate the same governed skill set everywhere scope is stated.
- Recommended edits: in `Testing and Verification Strategy`, either name an
  independent manual or hybrid review exercise with fixture inputs, expected
  findings, durable evidence, and a non-generalization limit, or remove the
  semantic-detection proof claim.
- Recommended edits: replace `Next Artifacts` with `spec amendments`,
  `spec-review`, `architecture assessment`, `architecture-review`, `execution
  plan`, `plan-review`, `test-spec amendments`, `test-spec-review`, and then
  implementation.

## Recommendation

- Recommendation: changes-requested. The portable direction is strategically sound and fits the current vision, but its delivery boundary, central semantic proof, and downstream lifecycle sequence are not ready for specification. This direct proposal-review remains isolated: it records PBC-PR1, PBC-PR2, and PBC-PR3, does not edit the proposal, and does not automatically start `spec`.
