# Review Resolution

Closeout status: open

### code-review-m2-r1

Finding ID: CR-M2-F1
Disposition: accepted
Owner: implementer
Owning stage: implement
Chosen action: Simplify contributor and governance local Codex setup guidance so it describes the active public-adapter install path into ignored `.codex/skills/`, keeps `.codex/skills/` untracked, and directs authors to edit `skills/`, without preserving obsolete `.codex/skills/` hand-edit/generated-output prohibition wording.
Rationale: The code-review finding is correct. The approved transition-release contract and learning follow-up both prefer concise active behavior over preserving the old `.codex/skills/` generated-output rule shape.
Validation target: Update the cited docs, add or tighten static coverage so stale `.codex/skills/` generated-output and hand-edit wording is rejected where appropriate, then rerun the focused M2 adapter-distribution tests, release validation, review artifact validation, change metadata validation, lifecycle validation for touched artifacts, and whitespace validation.
Validation evidence: pending
