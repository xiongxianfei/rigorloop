# Markdown Readability Contract Review Resolution

## Scope

This record tracks review finding closeout for the Markdown readability contract change.

Closeout status: open

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m1-r3

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

### code-review-m1-r1

Review closeout: code-review-m1-r1

#### MDREAD-M1-CR1 - Selector-composed README and VISION validation never enables changed-section enforcement

Finding ID: MDREAD-M1-CR1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: implementation M1
Rationale: Code-review found that selector routing selects the readability validator for README and root `VISION.md`, but the selected command does not include changed-section ranges, so known hard-wrap splits remain audit-only instead of failing for changed sections.
Required outcome: Selector-composed readability validation for README and `VISION.md` changes must preserve changed-section enforcement, or the selector must avoid claiming enforcement it cannot perform and route callers to a command shape that supplies changed-section ranges.
Chosen action: Extended selector check metadata with `changed_sections`, derived README and `VISION.md` ranges from PR/main and local git diff hunks, rendered those ranges into the selected `markdown_readability.validate` command, and added a selector regression that executes the selected command against a changed README hard-wrap fixture.
Validation target: Add selector/validator regression proof for README and `VISION.md` changed-section enforcement, then rerun readability validator tests, selector regression, readability smoke, change metadata validation, review artifact validation, artifact lifecycle validation, and whitespace checks.
Validation evidence: `python scripts/test-select-validation.py` passed with 125 tests, including the selector-selected README hard-wrap command regression. `python scripts/test-markdown-readability-validator.py` passed. `python scripts/validate-markdown-readability.py` passed with audit-only warnings `MDREAD-002=63, MDREAD-003=5`. Final lifecycle and whitespace validation for the review-resolution handoff is recorded in the active plan and change metadata.

### code-review-m1-r2

Review closeout: code-review-m1-r2

#### MDREAD-M1-CR2 - No-hunk fallback over-enforces historical README and VISION content

Finding ID: MDREAD-M1-CR2
Disposition: rejected
Status: resolved
Owner: maintainer
Owning stage: implementation M1
Rationale: Code-review found that selector changed-section support falls back to a whole-file `--changed-section` when no git hunks are available, which can make untouched historical README or `VISION.md` hard-wraps fail instead of remaining audit-only.
Required outcome: Selector-composed README and `VISION.md` readability validation must not treat an unknown or unavailable changed-section range as whole-file enforcement for existing historical content. It must either derive exact changed ranges, restrict whole-file changed-section fallback to genuinely new/untracked files where the whole file is the change, or avoid claiming changed-section enforcement when exact ranges are unavailable.
Chosen action: Rejected as not requiring implementation in this slice after direct current-state validation of the actual repository `README.md` and `VISION.md`. The maintainer narrowed the decision to direct repository files instead of complex no-hunk selector scenarios. Whole-file readability validation of both files passed, and direct phrase inspection found no current `MDREAD-001` hard-wrap failure in either file.
Validation target: Add selector regression proof that historical hard-wrap text outside a changed README or `VISION.md` hunk remains audit-only or out of enforcement scope, update the explicit/no-hunk command behavior, then rerun selector, readability, metadata, review-artifact, lifecycle, and whitespace validation.
Validation evidence: `python scripts/validate-markdown-readability.py README.md VISION.md --verbose` passed with audit-only warnings only. `rg -n "AI$|^agents\\b|proposal to$|^spec\\b|reviewable in$|^Git\\b|AI agents|proposal to spec|reviewable in Git" README.md VISION.md` found complete current `VISION.md` phrase lines and README phrase occurrences that do not split the known `MDREAD-001` hard-wrap patterns.

### code-review-m1-r3

Review closeout: code-review-m1-r3

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
