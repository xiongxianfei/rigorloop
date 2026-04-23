# Code Review Branch Reality And Traceability

## Status

- approved

## Related proposal

- [Code Review Branch Reality And Traceability](../docs/proposals/2026-04-22-code-review-branch-reality-and-traceability.md)

## Goal and context

This spec defines the remaining workflow contract needed after the earlier `code-review` independence work: stage-owned review language, tracked-branch reality for cited governing artifacts and readiness claims, and direct proof expectations for named edge cases.

The problem is not the `code-review` stage order. The problem is that contributors can still overstate what happened by:

- using implementation-stage wording that sounds like completed review;
- treating local artifact presence as if it proves reviewed branch authority; or
- inferring named edge-case coverage from code shape instead of citing direct proof.

This focused spec supplements [Code Review Independence Under Autoprogression](./code-review-independence-under-autoprogression.md). It does not replace that earlier first-pass review contract. The enduring repo-wide workflow invariant for branch-scoped authority and readiness claims must ultimately be reflected in `specs/rigorloop-workflow.md` rather than living only here.

## Glossary

### Stage-owned language

Workflow output language that stays within the claim type owned by the current stage.

### Implementation sanity check

Implementation-stage reporting about milestone completion, targeted validation, blockers, or readiness for downstream review, without claiming review findings or branch-ready status.

### Review surface

The review surface is the code, diff, patch, staged change, working-tree change, or commit range being inspected by `code-review`.

A review surface may include:

- a PR diff
- a commit range
- a staged diff
- an unstaged working-tree diff
- an explicitly supplied patch
- a local review target

The review surface answers:

> What is the reviewer inspecting?

The review surface alone does not prove that a governing artifact is present in tracked governing branch state.

### Tracked governing branch state

Tracked governing branch state is the tracked Git state that can be used as authority for branch-scoped conclusions.

For PR or CI review, this means the tracked files present at the reviewed branch or head commit and the reviewed PR diff.

For local pre-commit review, this means the tracked files in the reviewed Git state. Staged or unstaged changes may be part of the review surface, but they do not become tracked governing branch state until committed or otherwise explicitly included in a tracked branch or diff context.

Tracked governing branch state answers:

> Which governing artifacts are actually present in the branch state being claimed as reviewed or ready?

### Governing artifact

A governing artifact is a proposal, spec, test spec, architecture document, ADR, plan, or other workflow artifact cited as an input to the review conclusion.

### Local-only governing artifact

A governing artifact visible in the local worktree but not actually tracked in the tracked governing branch state.

### Branch-scoped conclusion

A branch-scoped conclusion is a claim that the reviewed branch, PR branch, or tracked change is clean, ready, or supported by governing artifacts.

Examples:

- `clean-with-notes` for a branch-scoped review
- `branch-ready`
- `ready for PR handoff`
- `governing artifacts are present`
- `test-spec edge case is covered`

### Branch-ready

`branch-ready` is owned by `verify`.

It means the tracked governing branch state satisfies required validation and artifact-presence checks.

### PR-body-ready

`pr-body-ready` is owned by `pr`.

It means the PR body is accurate, concise, grounded in verified artifacts, and does not introduce unverified claims.

### PR-open-ready

`pr-open-ready` is owned by `pr`.

It means the branch, base, remote, worktree, PR body, and action prerequisites are ready for opening a PR.

### PR readiness

Avoid the broad phrase `PR-ready` unless it is qualified.

Use `branch-ready`, `pr-body-ready`, or `pr-open-ready`.

### Direct proof

Explicit evidence tied to a named requirement or test-spec item, such as a targeted test, targeted validation output, or explicit manual verification note when manual verification is allowed.

### Named edge case

A specific failure path, fallback path, empty-state path, or other scenario explicitly named in the approved spec or active test spec.

## Examples first

### Example E1: implement reports completion without claiming review

Given milestone `M1` finishes with targeted validation
When `implement` reports its outcome
Then it may say the milestone is implemented, name the validation run, and say the change is ready for `code-review`, but it does not say that review found no required fixes.

### Example E2: code-review may inspect an uncommitted diff

Given `code-review` is asked to inspect staged or uncommitted changes
When the actual changed files are available and the cited governing artifacts are tracked in tracked governing branch state
Then `code-review` may review that diff and may still return a branch-scoped conclusion under the existing review-status contract.

### Example E3: local-only governing inputs force inconclusive review

Given `code-review` cites a spec and test spec as governing evidence
When those artifacts exist only locally and are not tracked in tracked governing branch state and no independently supported finding can be made
Then `code-review` returns `inconclusive`, names the missing tracked governing inputs, and does not emit a clean branch-scoped review result.

### Example E4: missing tracked authority does not suppress supported findings

Given `code-review` inspects a review surface that shows a fixable defect directly
When a cited governing artifact needed for a clean branch-scoped conclusion is only local or untracked
Then `code-review` still returns `changes-requested` rather than `inconclusive`, and it separately records the missing tracked governing authority.

### Example E5: verify blocks branch readiness on missing authoritative artifacts

Given implementation files are present and tests pass locally
When `verify` determines that a required authoritative spec or test spec is missing from tracked branch state
Then `verify` returns `blocked` rather than `ready` or `concerns`, because branch readiness cannot rely on local-only authority.

### Example E6: named edge case needs direct proof

Given the active test spec explicitly names a cleared-storage recovery path
When `code-review` evaluates the change
Then a clean result cites direct proof for that path, and code-shape inference alone is not enough.

### Example E7: local-only artifacts may inform background but not branch authority

Given the reviewer can see a newer local draft architecture note
When that note is not tracked in tracked governing branch state
Then it may inform reviewer background understanding, but it does not support a clean branch-scoped review conclusion or a branch-ready verification result.

## Requirements

R1. Workflow-facing stages MUST use stage-owned language for review and readiness claims.

R1a. `implement` output MAY report implementation completion, milestone validation, blockers, readiness for `code-review`, or the next milestone.

R1b. `implement` output MUST NOT claim or imply completed review findings, such as:
- "post-implementation review found no required fixes";
- "the branch is review-clean"; or
- equivalent wording that assigns review conclusions to the implementation stage.

R1c. `code-review` owns review findings and review-status conclusions under the existing `clean-with-notes`, `changes-requested`, `blocked`, and `inconclusive` status contract.

R1d. `verify` owns `branch-ready` conclusions. Earlier stages MUST NOT pre-claim those outcomes.

R1e. `pr` owns `pr-body-ready` and `pr-open-ready` conclusions.

R1f. Workflow-facing outputs SHOULD avoid the broad phrase `PR-ready` unless it is explicitly qualified as `branch-ready`, `pr-body-ready`, or `pr-open-ready`.

R2. The tracked-branch requirement MUST apply to branch-scoped authority and readiness claims, not as a blanket requirement that every code change under review is already committed.

R2a. The tracked-branch requirement applies to:
- cited governing artifacts;
- branch-readiness claims;
- PR-readiness claims; and
- claims that an artifact is part of the reviewed branch authority.

R2b. This feature MUST NOT require every reviewed implementation diff to already be committed.

R2c. `code-review` MAY inspect a review surface consisting of actual changed files, staged changes, uncommitted diffs, or a PR diff, depending on the review context.

R2d. When `code-review` cites a governing artifact as authoritative evidence for a clean branch-scoped review conclusion, it MUST confirm that artifact is present in tracked governing branch state.

R2e. A local-only governing artifact MAY inform reviewer background understanding, but it MUST NOT be used to support a clean branch-scoped review conclusion.

R2f. Missing tracked governing authority MUST prevent `clean-with-notes`.

R2g. Missing tracked governing authority MUST NOT suppress independently supported findings.

R2h. When the reviewer can identify a fixable defect from the review surface, `code-review` MUST return `changes-requested` even if tracked governing authority is incomplete.

R2i. When the reviewer identifies a blocking defect from the review surface, `code-review` MUST return `blocked` even if tracked governing authority is incomplete.

R2j. `code-review` MUST use `inconclusive` only when required evidence is missing and the reviewer cannot make a supported finding or clean conclusion.

R2k. An `inconclusive` result under `R2j` MUST identify which cited governing artifacts are missing from tracked governing branch state when that missing authority contributed to the outcome.

R2l. When `verify` evaluates `branch-ready`, it MUST treat required authoritative artifacts missing from tracked governing branch state as a blocking condition.

R2m. A `verify` result under `R2l` MUST be `blocked`, not `ready` or `concerns`.

R2n. `verify` MUST NOT treat local-only authoritative artifacts as sufficient support for `branch-ready`.

R3. Clean branch-scoped review conclusions MUST use direct proof for named edge cases.

R3a. When an approved spec or active test spec names a specific edge case or failure path, a clean `code-review` result MUST cite direct proof for that named case.

R3b. Acceptable direct proof under `R3a` MAY include:
- a targeted automated test;
- targeted validation output; or
- an explicit manual verification note when manual verification is allowed by the governing artifact set.

R3c. Code-shape inference alone MUST NOT be treated as sufficient direct proof for a named edge case.

R3d. When a named edge-case proof gap is actionable within current approved scope, `code-review` MUST report it as a finding rather than a clean result.

R3e. When a named edge-case proof gap exists because the reviewer cannot inspect enough evidence to assess the path credibly, `code-review` MUST use `inconclusive` rather than a clean result.

R3f. `verify` MUST treat unresolved proof gaps for named required edge cases as blocking for branch-readiness or PR-readiness claims.

R4. This feature MUST preserve the earlier `code-review` independence and workflow-order contracts while adding the new branch-reality and traceability invariant.

R4a. This feature MUST preserve the existing `implement -> code-review -> review-resolution when needed -> verify` stage order and stop-condition model unless an authoritative workflow artifact is explicitly updated by the same change.

R4b. This feature MUST preserve the first-pass review record and review-status rules defined by [Code Review Independence Under Autoprogression](./code-review-independence-under-autoprogression.md).

R4c. The enduring repo-wide workflow invariant from this feature MUST be recorded in `specs/rigorloop-workflow.md`.

R4d. This focused spec MUST act as the reviewable change contract for the feature, not the permanent long-term home for the general workflow invariant.

R4e. The first implementation slice for this feature MUST rely on contract updates, skill wording, test-spec coverage, and manual or document review. Dedicated validator enforcement for forbidden implement-stage review language is deferred to a later approved change.

## Inputs and outputs

Inputs:

- the accepted proposal for this feature;
- the review surface, such as changed files, staged diff, uncommitted diff, or PR diff;
- cited governing artifacts, including proposal, spec, test spec, plan, architecture document, and ADR when relevant;
- tracked governing branch state for those cited governing artifacts;
- validation evidence and direct proof surfaces for named requirements or edge cases;
- invocation context identifying implementation-stage reporting, `code-review`, or `verify`.

Outputs:

- narrower `implement` closeout language that reports implementation state without claiming review conclusions;
- `code-review` output that distinguishes between review surface and tracked governing branch state;
- `code-review` output that preserves supported `changes-requested` or `blocked` findings even when tracked governing authority is incomplete;
- `code-review` `inconclusive` output when required evidence is missing and no supported finding or clean conclusion can be made;
- `verify` `blocked` output when `branch-ready` claims lack tracked authoritative artifact support;
- review and verification output that cites direct proof for named edge cases or explicitly records the proof gap.

## State and invariants

- `implement`, `code-review`, and `verify` own different claim types and must not blur them.
- Review surface and tracked governing branch state are related but distinct concepts.
- Local-only governing artifacts are background only, not branch authority.
- A clean branch-scoped review conclusion is invalid without tracked governing authority when such authority is cited.
- Missing tracked governing authority blocks `clean-with-notes`, but it does not erase otherwise supported findings.
- A clean branch-scoped review conclusion is invalid without direct proof for named required edge cases.
- `code-review` uses `inconclusive` only when missing required evidence prevents both a supported finding and a clean conclusion.
- `verify` uses `blocked` when `branch-ready` claims lack tracked authoritative support.
- `pr` owns `pr-body-ready` and `pr-open-ready` rather than reusing unqualified `PR-ready`.
- This focused spec is the change vehicle; `specs/rigorloop-workflow.md` remains the enduring authoritative workflow rule once the change is folded in.

## Error and boundary behavior

- If `implement` uses review-status language or claims no required review fixes, its output does not satisfy this spec.
- If `code-review` cites a governing artifact as authoritative but cannot confirm it in tracked governing branch state, a clean branch-scoped result is invalid.
- If `code-review` reviews an uncommitted or staged diff while all cited governing artifacts are tracked in tracked governing branch state, that review context remains valid under this spec.
- If `code-review` can still make a supported fixable or blocking finding from the review surface, it must return that finding rather than `inconclusive`.
- If a local-only governing artifact changes the reviewer’s understanding materially, the review must not hide that dependency inside a clean branch-scoped conclusion.
- If a named edge case is only inferred from nearby code and no direct proof is cited, the review does not satisfy this spec.
- If `verify` finds that `branch-ready` claims rely on required authoritative artifacts absent from tracked governing branch state, verification must stop with `blocked`.
- If the change does not cite any governing artifact beyond tracked branch authority already established elsewhere, this feature does not require redundant restatement, but any explicit authority claim must still remain truthful.

## Compatibility and migration

- This feature is a workflow-contract clarification, not a product runtime migration.
- It does not require committed-only code review.
- It does not remove or replace the earlier `code-review` independence contract.
- It does not add a new review stage, readiness registry, or orchestration subsystem.
- It does not require validator enforcement in the first slice.
- Existing workflow-facing wording that lets `implement` imply review completion, uses unqualified `PR-ready`, or lets local-only governing artifacts support clean branch-scoped conclusions becomes incompatible once this feature lands.

## Observability

- A reviewer MUST be able to tell from `implement` output whether the stage is reporting implementation completion versus review findings.
- A reviewer MUST be able to tell from `code-review` output which governing artifacts were cited and whether they were confirmed in tracked governing branch state.
- A reviewer MUST be able to tell from `code-review` output when missing tracked governing authority blocked `clean-with-notes` but did not suppress independently supported findings.
- A reviewer MUST be able to tell from `code-review` output when local-only governing artifacts forced an `inconclusive` result.
- A reviewer MUST be able to tell from `verify` output when `branch-ready` is blocked by missing tracked authoritative artifacts.
- A reviewer MUST be able to trace named edge-case coverage to direct proof rather than code-shape inference alone.
- Workflow-facing skill guidance and workflow summary guidance SHOULD use consistent vocabulary for stage-owned language, review surface, tracked governing branch state, `branch-ready`, and direct proof.

## Security and privacy

- This feature MUST NOT introduce new secret, credential, or network dependencies.
- This feature MUST NOT weaken existing repository review or verification gates for security-sensitive changes.
- Review and verification wording MUST NOT expose sensitive local-only paths or private runtime details when reporting missing or untracked governing artifacts.

## Performance expectations

- No product runtime performance change is expected.
- The clarified contract SHOULD reduce avoidable review churn caused by overstated readiness or unsupported clean claims.
- The feature MUST NOT add a new mandatory repository stage.

## Edge cases

1. `code-review` may inspect a staged or uncommitted diff and still produce a valid branch-scoped conclusion when its cited governing artifacts are tracked in tracked governing branch state.
2. `code-review` may use a local-only draft artifact as informal background, but that artifact cannot support a clean branch-scoped review conclusion.
3. A change may be milestone-ready for implementation purposes while still being `changes-requested`, `blocked`, or `inconclusive` in `code-review`, or `blocked` in `verify`.
4. A named edge case may be implemented correctly in code, but without direct proof it still cannot support a clean branch-scoped review conclusion.
5. `verify` may block `branch-ready` even after a non-blocking implementation sanity check, because those stages own different claims.
6. `pr` may own `pr-body-ready` and `pr-open-ready` without reusing unqualified `PR-ready`.
7. This feature applies to cited authoritative artifacts and readiness claims, not to every file visible in the local worktree.

## Non-goals

- Requiring a human reviewer for every change.
- Restricting `code-review` to committed code only.
- Replacing `code-review` with `verify`, tests, or validators alone.
- Redesigning workflow stage order or autoprogression.
- Solving every review-quality problem across every workflow-facing skill in one pass.
- Adding dedicated validator enforcement for forbidden implement-stage review language in the same v1 slice.

## Acceptance criteria

- A reviewer can see that `implement` may report completion and readiness for `code-review`, but may not claim review findings or review-clean status.
- A reviewer can see that `code-review` may inspect changed files, staged changes, uncommitted diffs, or PR diffs without requiring every reviewed code change to already be committed.
- A reviewer can see that cited governing artifacts used for a clean branch-scoped conclusion must be confirmed in tracked governing branch state.
- A reviewer can see that missing tracked governing authority blocks `clean-with-notes` but does not suppress independently supported `changes-requested` or `blocked` findings.
- A reviewer can see that `code-review` uses `inconclusive` only when missing evidence prevents both a supported finding and a clean conclusion.
- A reviewer can see that `verify` blocks `branch-ready` when required authoritative artifacts are missing from tracked governing branch state.
- A reviewer can see that workflow-facing outputs avoid unqualified `PR-ready` and instead use `branch-ready`, `pr-body-ready`, or `pr-open-ready`.
- A reviewer can see that named edge cases require direct proof and that code-shape inference alone is insufficient.
- A reviewer can see that this feature preserves the earlier `code-review` independence contract and existing stage order.
- A reviewer can see that `specs/rigorloop-workflow.md` is the enduring normative home for the repo-wide invariant, while this focused spec is the change vehicle.
- A reviewer can see that dedicated validator enforcement is intentionally deferred in the first slice.

## Open questions

None.

## Next artifacts

- plan if no separate architecture artifact becomes necessary
- matching test spec after the plan is settled

## Follow-on artifacts

- `specs/code-review-branch-reality-and-traceability.test.md`
- `docs/plans/2026-04-22-code-review-branch-reality-and-traceability.md`

## Readiness

Spec review feedback is incorporated.

This spec is approved.

No separate architecture artifact is expected for this slice.

The active execution plan now exists.

The focused active test spec now exists.

The next stage is `implement`.

The durable workflow invariant must later be folded into `specs/rigorloop-workflow.md` rather than left only in this focused spec.
