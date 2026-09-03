# Review resolution

Closeout status: open

## Finding details

### code-review-m1-r1

#### Finding ER-M1-CR1

Finding ID: ER-M1-CR1
Review ID: code-review-m1-r1
Disposition: accepted
Owner: M1 implementer
Owning stage: review-resolution
Decision owner: none
Decision needed: none
Status: resolved
Chosen action: Remove canonical-source metadata from both shipped discovery assets and add a package-wide public-text hygiene regression before changing the assets.
Required outcome: Both discovery packages contain no maintainer-only canonical path or shared-copy and adapter mechanics.
Follow-up: Apply the bounded M1 correction and run Code Review M1 R2.
Validation target: ER-R34, TG-04, and direct package-wide public-text hygiene regression.
Validation evidence: The new package-wide hygiene test failed on both asset comments before correction, then passed; the 359-test full skill-validator suite, canonical skill validation, generated local-skill validation, review structure validation, and `git diff --check` all passed.
Rationale: The finding is directly required by ER-R34 and needs no product or design decision.
