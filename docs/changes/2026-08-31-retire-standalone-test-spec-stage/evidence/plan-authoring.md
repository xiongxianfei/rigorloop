# Plan Authoring Evidence

- Artifact path: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`
- Artifact identity: `sha256:727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`
- Authoring result: complete

The plan allocates every approved requirement, boundary, and selected interaction across five ordered implementation milestones and one lifecycle-closeout milestone. It introduces v2 behind an inactive discriminator, omits optional in-place migration, blocks activation until prior-contract work has passed the legacy delivery gate, and reserves atomic default activation and standalone-entrypoint retirement for the final implementation slice.

Milestone-local TG objectives and four change-level verification groups preserve SR-to-work-to-proof traceability without creating a replacement governed artifact or per-test identity scheme. Exact concrete tests and fixture cases remain for the required legacy-path test specification.

During test-spec input reconciliation, the M1 focused Node command was corrected from a nonexistent `new-change.test.js` path to the existing public CLI owner `cli.test.js` before proof depended on it.
