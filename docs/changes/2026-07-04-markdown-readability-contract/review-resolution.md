# Markdown Readability Contract Review Resolution

## Scope

This record tracks review finding closeout for the Markdown readability contract change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1

## Resolution Entries

### proposal-review-r1

Review closeout: proposal-review-r1

#### MDREAD-PR1 - Settled owner decisions still appear as downstream choices

Finding ID: MDREAD-PR1
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Rationale: Proposal-review correctly found that owner-settled decisions were still phrased as candidate or downstream choices.
Required outcome: The proposal must state the dedicated readability validator and canonical generated-region marker syntax as settled proposal decisions, while leaving only implementation details to the downstream spec.
Chosen action: Revised `Recommended Direction` and `Testing and Verification Strategy` so `scripts/validate-markdown-readability.py` is the owner validator composed by other validators as needed, and the generated-region marker syntax is canonical. The proposal now leaves field validation details, path selection, parser behavior, and integration mechanics to the downstream spec.
Validation target: Rerun focused artifact validation after proposal revision, then rerun proposal-review.
Validation evidence: Proposal revision completed. `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-markdown-readability-contract`, `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-04-markdown-readability-contract.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml --path docs/changes/2026-07-04-markdown-readability-contract/review-log.md --path docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md`, `git diff --check -- docs/proposals/2026-07-04-markdown-readability-contract.md docs/changes/2026-07-04-markdown-readability-contract`, and a direct trailing-whitespace scan passed after revision. Proposal rereview remains pending.

### proposal-review-r2

Review closeout: proposal-review-r2

No material findings.

### spec-review-r1

Review closeout: spec-review-r1

No material findings.

### plan-review-r1

Review closeout: plan-review-r1

No material findings.

### test-spec-review-r1

Review closeout: test-spec-review-r1

No material findings.

#### MDREAD-PR2 - Latest multi-part owner decisions are not classified in Initial intent preservation

Finding ID: MDREAD-PR2
Disposition: accepted
Status: resolved
Owner: proposal owner
Owning stage: proposal revision
Rationale: Proposal-review correctly found that the broad proposal's initial-intent table did not visibly classify the later owner decisions that settled the open questions.
Required outcome: The proposal must add initial-intent preservation rows for the settled validator ownership, changed-section README and `VISION.md` enforcement, manual-proof exclusion, canonical marker syntax, diagram guidance, and audit-only warning graduation policy.
Chosen action: Added initial-intent preservation rows for dedicated validator ownership, changed-section README and `VISION.md` enforcement, no manual-proof contracts, canonical generated-region marker syntax, diagrams encouraged but never required, and audit-only warning graduation policy.
Validation target: Rerun focused artifact validation after proposal revision, then rerun proposal-review.
Validation evidence: Proposal revision completed. `python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-04-markdown-readability-contract`, `python scripts/validate-change-metadata.py docs/changes/2026-07-04-markdown-readability-contract/change.yaml`, `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-04-markdown-readability-contract.md --path docs/changes/2026-07-04-markdown-readability-contract/change.yaml --path docs/changes/2026-07-04-markdown-readability-contract/review-log.md --path docs/changes/2026-07-04-markdown-readability-contract/review-resolution.md --path docs/changes/2026-07-04-markdown-readability-contract/reviews/proposal-review-r1.md`, `git diff --check -- docs/proposals/2026-07-04-markdown-readability-contract.md docs/changes/2026-07-04-markdown-readability-contract`, and a direct trailing-whitespace scan passed after revision. Proposal rereview remains pending.
