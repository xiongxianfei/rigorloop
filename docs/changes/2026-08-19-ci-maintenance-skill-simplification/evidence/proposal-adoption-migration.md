# Proposal Adoption Migration Evidence

Stage: proposal
Operation: migrate-portable-proposal-to-current-stage-owned-contract
Change ID: 2026-08-19-ci-maintenance-skill-simplification
Artifact ID: proposal
Proposal path: docs/proposals/2026-08-19-ci-maintenance-skill-simplification.md
Prior proposal identity: sha256:0e8f59534e1aa0dcedec961c513c57fa067ffe8cf1a1feffff92f98f747d406b
Migrated proposal identity: sha256:a7f4b73f458d3bdca53c2f81bb0416edae9fad0dec75bfd8b7054fddbb603d40
Migration basis revision: 1fba33b1c12b3c382bc2311afdfb2eae67bc8138
Authority: explicit user instruction to place proposal lifecycle status in the owning change record and refine the current CI-maintenance issue
Result: review-required

The migration removes the retired embedded mutable status, replaces the portable-authoring statement with one exact owning-change pointer, registers the proposal as the unique primary proposal entry, and records actual follow-on artifacts that already exist. It does not change the selected CI-maintenance direction.

The isolated `proposal-review-r3` record remains historical evidence because its recording-only root explicitly did not settle governed lifecycle state. A fresh governed proposal review in this change root is required before the proposal entry can become `accepted`. The prior failed verify report remains truthful historical evidence, and paused automation is not resumed by this migration.
