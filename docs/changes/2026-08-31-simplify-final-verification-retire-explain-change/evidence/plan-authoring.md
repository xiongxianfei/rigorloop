# Plan Authoring Evidence

- Artifact path: `docs/plans/2026-08-31-simplify-final-verification-retire-explain-change.md`
- Artifact identity: `sha256:be59397c12da69495be71c353585ab858642d00704fc1b156a40c5921dacef52`
- Authoring result: complete

The plan allocates all 38 approved requirements, all eight applicable boundaries, and all four selected interactions across five ordered implementation milestones and one lifecycle-closeout milestone. It introduces v3 behind an inactive discriminator, separates semantic evidence reuse from execution caching, keeps correction and PR authority outside Verify, assembles canonical and generated parity before the cutover candidate, and requires this implementing change to complete its registered v2 closeout before public release activation.

Milestone-local TG objectives and four change-level verification groups provide the approved v2 Delivery evidence map without creating a test-spec, replacement evidence artifact, or per-test lifecycle identity. Focused repository-owned checks expand to complete runtime and broad-smoke validation at the integrated candidate and final closeout boundaries.

`docs/project-map.md` was not relied upon for lifecycle topology because its 2026-07-28 inventory predates and contradicts the active v2 consolidated-gate contract in the relied-on area. The plan instead uses the approved design package, current lifecycle context, current runtime and validator paths, and observed repository files.

The plan explicitly allocates correction of the current boundary validator's v1/test-spec-only assumption to M4 under FV-R37, FV-R38, and FV-AC14. It does not create the test-spec that the stale validator currently requests.
