# Release Records

This directory stores durable release evidence for RigorLoop releases.

The standing release-process contract uses one version-scoped evidence file per publish attempt:

```text
docs/releases/v<version>.md
```

Use `templates/release-evidence.md` when preparing a release record. The evidence file records what was published, from which source, through which gate, by which publish path, and with which registry verification. It is operational proof for already-reviewed work; it does not approve new source behavior, package behavior, release-process changes, package-surface changes, authentication/provenance policy changes, adapter targets, or publish mechanics.

Existing release-specific files under `docs/releases/<version>/`, such as `release.yaml`, `release-notes.md`, and `npm-publication.md`, remain valid release evidence for their release-specific contracts. The standing `docs/releases/v<version>.md` record layers the routine publish checklist over those surfaces and may link to them when applicable.

Routine publishes do not update `docs/plan.md` unless the release is part of an active lifecycle plan. Link related lifecycle change records from the release evidence when the release is tied to a change.

Do not record npm tokens, OTPs, credentials, private keys, private environment dumps, hostnames, usernames, home-directory paths, or machine-local temporary paths in release evidence. Record command families, public registry references, package names, versions, dist-tags, integrity values, and concise command/result summaries instead.

Emergency release deferrals are exceptions, not a normal release path. Evidence must name each deferred gate item, approving owner or owning stage, rationale, validation impact, accepted risk, follow-up location, and deadline or next lifecycle stage. Release evidence creation, secret suppression, source/package/version/dist-tag recording, publish-path recording, registry verification, and recovery/follow-up recording are non-deferrable.
