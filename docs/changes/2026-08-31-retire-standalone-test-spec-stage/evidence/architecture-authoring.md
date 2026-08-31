# Architecture authoring manifest

Assessment basis: accepted proposal `proposal-review-r3`, current governed-lifecycle CLI boundary, stage-owned change-local lifecycle state, canonical skill-source constraints, and supported adapter packaging rules.
Commit group: retire-standalone-test-spec-design-v1
Authoring result: complete

## Target 1

Target ID: adr-verification-ownership
Kind: adr
Role: supporting
Prior identity: absent
Path and identity: docs/adr/ADR-20260831-verification-ownership-without-test-spec-stage.md sha256:8e73252cbe4642240e0f7a6989029a1ca59e89a8e958983fde8e494a3fb7becb
Dependencies: accepted proposal
Commit point: complete standalone decision covering ownership, active vocabulary, historical compatibility, alternatives, consequences, and follow-up
Evidence state: complete

## Target 2

Target ID: architecture
Kind: architecture
Role: primary
Prior identity: absent
Path and identity: docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md sha256:86b94693a3ca1c53c6612cb573b7951a54c3e672edc07d4017f345625d516e6e
Dependencies: accepted proposal and Target 1 decision content
Commit point: independently valid arc42 package covering responsibility, lifecycle, compatibility, validation, packaging, activation, and rollback boundaries
Evidence state: complete

No C4 diagram target is needed because this change alters a repository-owned workflow protocol and packaged guidance rather than an executable system, deployable container, service interaction, or runtime network topology.
