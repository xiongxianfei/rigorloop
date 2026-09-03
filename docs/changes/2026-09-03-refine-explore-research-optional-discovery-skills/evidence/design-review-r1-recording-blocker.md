# Design Review R1 recording blocker

Attempted review round: design-review-r1
Package kind: design
Package members: architecture=docs/architecture/2026-09-03-refine-explore-research-optional-discovery-skills.md, spec=specs/refine-explore-research-optional-discovery-skills.md
Upstream review ID: proposal-review-r1
Recording result: blocked before lifecycle mutation

The first `record-package-review` request was rejected because the newly scaffolded governed change still used lifecycle coordination schema version 1. Route migrated the coordination record to version 2 using `requests/migrate-lifecycle-cli-schema-v2.json`. Because the attempted R1 review file had already caused the CLI to allocate the next round, Design Review restarted as R2 against the unchanged exact package. The failed R1 request remains at `requests/record-design-review-r1.json`; no R1 review or package settlement was recorded.
