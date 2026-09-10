# RigorLoop 1.0.0

This major release publishes the reviewed workflow and recording changes since 0.5.0.

## Breaking changes

- Runtime engineering records use rigorloop-records-v2. Retired record formats and legacy lifecycle mutation commands reject safely. Historical records remain readable as historical files; this release does not automatically convert them or provide a legacy runtime continuation path.
- Use the targeted recording commands and explicit context/subject inspection described in the CLI guidance. Record-store remains an advanced inspection, replacement and recovery surface.
- Use `route` for workflow coordination and `design` for unified living-model authorship. Separate architecture authoring and the older separate review progression entry points have been retired; Design Review and Delivery Review assess their complete packages.

Read current project and CLI guidance before upgrading an existing governed project. Keep original historical records intact. Installation does not authorize governance adoption or migrate project state.

## Improvements

- Explicit targeted queries and mutations provide current record context, subject identities, findings, evidence and independently owned judgments.
- Shared Skill, Test, Review and Closeout, Design and System ownership is clarified. The proposal/proposal-review pilot preserves specialist authority and uses selectively loaded guidance.
- Release preparation, candidate-bound approval, publication, public verification and durable reporting are coordinated by the protected workflow. Failure, uncertainty and recovery remain explicit.
- Superseded design sources and the unused recorded-source validation wrapper are retired after their consumers and surviving requirements are reconciled.

## Adapter compatibility

Codex, Claude Code and opencode remain the supported adapter targets. Target install roots and supported installation behavior are unchanged by this release preparation. Published archives are generated from the selected canonical skills and validated with their declared resources; support for a target does not claim universal correctness across every agent invocation.

## Release status

These are tracked release notes for the candidate. Publication, artifact identities and public smoke results are established by the release workflow's version-scoped evidence, not by this document. npm package: `@xiongxianfei/rigorloop`; stable dist-tag: `latest`.
