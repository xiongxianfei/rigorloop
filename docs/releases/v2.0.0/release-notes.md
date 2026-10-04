# RigorLoop v2.0.0

This breaking candidate replaces Proposal-first delivery with requirement analysis and review, separate System and Architecture Design, integrated Design Review, delivery planning, one whole-change Code Review gate and final Verify. Milestones organize implementation and checks; interim reviews are optional advice.

Operational records use targeted-recording-v2 / rigorloop-records-v4 and project-local SQLite. Current handoffs, explicit judgments and selected supporting evidence replace mandatory activity history. Engineering definitions remain in the repository. The supported runtime is Node 24.15.0 or later within Node 24, with SQLite 3.51.3 or later; unsupported builds reject operational access.

New Changes use `change create`, `change context` and `change update`; supporting assessments use `review` and `verification`. Completion is explicit. `store backup`, `store restore` and `store migrate` provide selected portable backup and controlled maintenance. Installing this candidate does not import records or approve engineering work. Earlier v3 data needs explicit supported import, retained originals and current reconciliation; retain the earlier executable for work that has not migrated.

The obsolete Proposal, Proposal Review and combined Design skills are replaced explicitly with `init codex|claude --replace-workflow requirement-first-v1 --force`. Selected originals are retained outside discovery, and partial installation effects are reported. Ordinary `--force` does not authorize workflow retirement. Other target roots and unrelated skills remain outside the replacement scope.

This file records candidate changes, not release approval, publication, completed qualification or hosted CI success. The existing v1.0.0 release keeps its original artifact identity.

<!-- rigorloop:generated:start release-transaction surface=release-metadata profile=docs/releases/profiles/v2.0.0.yaml -->
- Release profile: `docs/releases/profiles/v2.0.0.yaml`
- npm package: `@xiongxianfei/rigorloop@2.0.0`
- npm dist-tag: `latest`
- Supported targets: codex, claude
- Adapter metadata: `adapter-artifacts-v2.0.0.json`
- Pending publication evidence: `docs/releases/v2.0.0/npm-publication.md`
<!-- rigorloop:generated:end release-transaction surface=release-metadata -->
