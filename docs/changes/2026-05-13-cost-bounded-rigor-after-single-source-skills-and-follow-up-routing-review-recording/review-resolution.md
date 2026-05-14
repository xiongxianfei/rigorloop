# Cost-Bounded Rigor Proposal Review Resolution

## Scope

This record tracks material findings from formal proposal-review rounds for the cost-bounded rigor proposal.

Closeout status: closed

Review closeout: proposal-review-r2
Review closeout: spec-review-r1

## Resolution Entries

### proposal-review-r1

No material findings.

### proposal-review-r2

Review closeout: closed

#### CBR-1

Finding ID: CBR-1
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Make the readiness statement stage-accurate for a draft proposal.
Rationale: A draft proposal should not imply it is already ready for accepted-state normalization before the proposal-review outcome has been acted on.
Chosen action: Replaced readiness with `Ready for proposal-review` and a conditional next-artifact statement.
Safe resolution path: Replace readiness wording with `Ready for proposal-review.` and a conditional next-artifact statement.
Validation target: Proposal revision plus artifact lifecycle validation.
Validation evidence: Proposal readiness now says `Ready for proposal-review` and does not preclaim accepted-state normalization. `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording`, `python scripts/validate-change-metadata.py docs/changes/2026-05-13-cost-bounded-rigor-after-single-source-skills-and-follow-up-routing-review-recording/change.yaml`, and targeted artifact lifecycle validation passed.

#### CBR-2

Finding ID: CBR-2
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Split the first slice into a smaller authoring/review guidance slice and defer skill/validator work unless explicitly needed.
Rationale: The prior first slice still touched too many surfaces for a proposal whose purpose is cost-bounded rigor.
Chosen action: Narrowed M1 to proposal/proposal-review scope-budget guidance plus concise `docs/workflows.md` evidence wording, and moved selected skill wording, validation-budget guidance, lifecycle token-cost summaries, and progressive-loading work to later slices.
Safe resolution path: Define M1 as proposal/proposal-review scope-budget guidance plus concise bounded-evidence wording in `docs/workflows.md`; defer selector, lifecycle token-cost artifact, dynamic benchmark, broad progressive-loading, and `implement` or `code-review` edits unless later scoped.
Validation target: Proposal revision plus artifact lifecycle validation.
Validation evidence: The proposal's `First implementation slice` and `Rollout` sections now separate M1 through M5 and defer `implement`/`code-review` edits unless later scoped. Review-artifact closeout, change metadata, and targeted artifact lifecycle validation passed.

#### CBR-3

Finding ID: CBR-3
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Make scope-budget applicability operational as proposal/proposal-review judgment, not mechanical validator inference.
Rationale: Broadness is semantic and should not become brittle validator inference in the first implementation slice.
Chosen action: Added the reviewer-judgment boundary and validator limitation to the scope-budget trigger section.
Safe resolution path: Add reviewer-judgment boundary and validator limitation wording.
Validation target: Proposal revision plus artifact lifecycle validation.
Validation evidence: The proposal now says scope-budget applicability is proposal/proposal-review judgment, and validators must not fail solely by inferring broadness. Review-artifact closeout, change metadata, and targeted artifact lifecycle validation passed.

#### CBR-4

Finding ID: CBR-4
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Add a concise escape rule to preserve correctness when bounded evidence is incomplete, contradictory, or insufficient.
Rationale: Bounded evidence should reduce waste without giving agents a reason to under-read important context.
Chosen action: Added do-not-under-read wording and a broader-section/full-file escape rule to the evidence-budget wording.
Safe resolution path: Add do-not-under-read wording to the proposed evidence-budget guidance.
Validation target: Proposal revision plus artifact lifecycle validation.
Validation evidence: The proposal now requires expansion when narrower evidence is incomplete, contradictory, or insufficient. Review-artifact closeout, change metadata, and targeted artifact lifecycle validation passed.

#### CBR-5

Finding ID: CBR-5
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Move validation-budget acceptance to later-slice scope or narrow first-slice acceptance to proposal-level direction.
Rationale: Acceptance criteria should not pull separate validation-budget work back into the first implementation slice.
Chosen action: Replaced first-slice acceptance wording with later-slice validation-budget ownership and no selector behavior change in the first implementation.
Safe resolution path: Replace first-slice acceptance wording and add later-slice acceptance for validation-budget ownership.
Validation target: Proposal revision plus artifact lifecycle validation.
Validation evidence: Acceptance criteria now state that the first implementation does not change selector behavior and that M3 owns detailed validation-budget guidance. Review-artifact closeout, change metadata, and targeted artifact lifecycle validation passed.

#### CBR-6

Finding ID: CBR-6
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Reduce the deferred lifecycle token-cost summary section to a lightweight design sketch.
Rationale: A deferred feature should not carry a detailed schema in this proposal when the first-slice problem is scope and evidence guidance.
Chosen action: Reduced lifecycle token-cost summary details to conditional/deferred guidance and intended field groups, with exact path and schema deferred to a later proposal or spec.
Safe resolution path: Keep conditional/deferred trigger guidance and intended field groups, but defer exact report path and schema to a later proposal or spec.
Validation target: Proposal revision plus artifact lifecycle validation.
Validation evidence: The proposal no longer includes the detailed YAML schema or report path for the deferred lifecycle token-cost summary artifact. Review-artifact closeout, change metadata, and targeted artifact lifecycle validation passed.

### proposal-review-r3

No material findings.

### spec-review-r1

Review closeout state: closed

Status: inconclusive

Reason: The direct spec-review request did not include a spec path, and no matching spec artifact exists under `specs/` for the cost-bounded rigor proposal.

Required input: `specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`

Closeout action: Created `specs/cost-bounded-rigor-after-single-source-skills-and-follow-up-routing.md`.

Closeout note: This closes the missing-input stop condition for `spec-review-r1`, but it does not count as spec-review approval. Rerun `spec-review` on the new spec before downstream planning or implementation relies on it.
