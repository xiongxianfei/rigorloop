# Targeted recording Design Review rereview

## Result

- Skill: design-review
- Review status: approved
- Package members: `cli` = `docs/design/cli.md`; `workflow` = `docs/design/workflow.md`. These are the exact combined model members, not separate component approvals; no additional ADR belongs to this amendment.
- Upstream review ID: `proposal-review-r1`, recorded at `docs/changes/2026-09-07-targeted-recording-primary-cli-review-recording/reviews/proposal-review-r1.md`.
- Review ID and round: `targeted-recording-design-review`, round 2.
- Material findings: none open; TR-DR-001 resolved by independent reassessment.
- Correction targets: none
- Recording status: recorded
- Settlement status: withheld
- Open blockers: no substantive Design blocker; formal settlement remains unavailable without a selected governed change and exact settlement authority.
- Immediate next stage: isolated stop
- Claim limitations: substantive advisory approval of the exact two-model design amendment. This does not settle a lifecycle package, establish formal Delivery eligibility, start downstream work, authorize implementation, or claim verification, publication or release readiness.

## Prior finding disposition

The [first-pass review](2026-09-07-targeted-recording-design-review.md) remains unchanged and preserves TR-DR-001 before correction. Parent author `/root` corrected only the CLI model; the Workflow member remained unchanged. Reviewer `/root/targeted_design_review` independently reassessed the correction and its relationships to the complete package.

TR-DR-001 is resolved. The CLI now defines closed Header and CountGroup shapes, complete label counts with known-versus-unknown totals, context registry/applicability representation and identity ownership, and exact item kind/target/full-show mappings. Status, context and show have explicit scope accounting. Missing content in omitted collections remains visible without corrupting selected-entry counts. Missing selected content cannot look like an empty or complete result. Tokens are versioned, bounded, and tied to an exact profile, ordering key and revision.

Showing an entry inside a registered missing file now rejects with broken-reference and a missing-content observation; a genuinely absent entry in readable authoritative content returns target-not-found. Registered missing files cannot be recreated as empty collections by targeted mutation. Whole-record reconstruction remains an explicit advanced repair, preserving the distinction between routine targeting and recovery of lost data. These changes complete CLI-SR-14/17 without changing stored schemas or workflow decisions.

## Package assessment

The corrected query contract and lossless construction architecture support the specified inputs, bounded outputs, preservation, retry/conflict and recovery outcomes. Purpose-specific commands and batch share the same structural validation and publication path as advanced recording. Explicit applicability, judgment, ownership and completion stay with actors. The declared external-edit limitation remains intact.

Workflow and CLI agree on review findings versus change-level blockers, reporter disposition versus correction ownership, exact historical subjects, and downstream responsibility for sufficient context. A failed Verify and new blocker remain recordable after completed activity; Route can subsequently record correction without a readiness gate or simultaneous decisions from all actors. No preservation or ownership requirement is weakened for implementation convenience.

The proposal's coordinated consumer/adoption and complete-interaction measurement scope remains allocated. Historical handlers and advanced v1 byte semantics remain separate; the primary interface is prospective. All eight model boundary dimensions and the stated combined hazards have coherent requirement-owned outcomes. Concrete implementation checks, supported-adapter proof and token measurements remain Delivery obligations rather than unsupported claims of this approval.

## Independence and recording authority

Contributors are the user and author `/root`. Reviewer `/root/targeted_design_review` is a distinct delegated agent that authored neither model nor the correction and did not edit either reviewed member. It independently read the correction in the context of both complete models, prior finding, proposal direction, earlier Proposal Review and user command constraints. The review uses the previously loaded Design Review methods, result asset and recording guidance. First-pass provenance and authority limitations remain applicable.

Recording mode is `advisory-durable`; settlement is `none`. The direct Design-and-review request establishes the exact model scope, not a new record root or historical lifecycle registration. This separate rereview preserves the first-pass record; it is not a compact stable-review mutation or a formal settlement substitute. No lifecycle record, routing state or model was changed by the reviewer. Pre-existing historical proposal links outside the amendment were not relied on to infer or close their obligations.

## Validation

- `python scripts/validate-markdown-readability.py docs/reviews/2026-09-07-targeted-recording-design-review-r2.md`: passed with 13 audit-only warnings.
- `git diff --no-index --check /dev/null docs/reviews/2026-09-07-targeted-recording-design-review-r2.md`: no whitespace diagnostics; exit 1 denotes the new-file comparison.

No runtime behavior was implemented or tested by this review.
