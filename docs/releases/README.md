# Release Records

[Release](../design/release/release.md) owns the standing operation. This directory contains historical checked-in evidence; the approval-driven path stores new operational evidence at the same version-scoped paths on its configured separate Git ref.

## Routine operation

After reviewed work merges to `main`, `.github/workflows/release.yml` prepares and checks a candidate automatically. The maintainer reads its summary and approves the `release` environment job. That job publishes the retained bytes, observes the public result, runs fresh public smoke and records the outcome. Required checks fail before an approval request; missing or ambiguous reviewed version decisions require an upstream correction.

The summary identifies the reviewed and prepared source, candidate, generated source changes, checks, artifacts, publication destinations and reporting ref. An approval covers those exact inputs. Preparation on a retry restores the original artifact rather than rebuilding it. The workflow no longer publishes from a tag trigger.

Version intent and tracked notes belong in the reviewed source change. Ordinary CI prepares an isolated candidate and checks its actual package; generated metadata, hashes and evidence are not manual release tasks. After merge, the hosted workflow prepares the exact candidate that the maintainer approves.

npm may delay availability while scanning an accepted upload. The job polls for roughly 20 minutes without repeating publication; a timeout preserves the observed state for recovery.

## One-time deployment setup

Before enabling routine use, a repository maintainer must establish:

- A protected `main` branch requiring pull requests and passing `ci`, with zero required GitHub approving reviews. Independent engineering review and Verify remain in repository evidence. Release consumes those assessments; it does not create another engineering approval.
- A pre-existing `release` environment with authorized individual required reviewers and protected-branch deployment policy. The initial integration rejects team-only or custom-branch reviewer configurations rather than infer equivalent authority.
- npm trusted publishing for `xiongxianfei/rigorloop`, workflow `release.yml`, environment `release`, and the existing package. Set repository variable `RELEASE_TRUSTED_PUBLISHER` to `github:xiongxianfei/rigorloop:release.yml:release` after establishing that configuration. This is configuration intent, not proof that npm will authorize a write.
- Repository variable `RELEASE_EVIDENCE_REF`, normally `refs/heads/release-evidence`. Permit the protected job to create/update that separate ref and publish its exact tag/assets; do not point it at the source branch or require a second routine approval/merge for generated evidence.
- The workflow's job permissions, OIDC and immutable Actions artifact storage with 30-day retention. Candidate and recovery uploads cannot overwrite earlier artifacts. Expired or missing inputs require an explicit exception.

Preparation inspects the available repository, branch and environment facts. Artifact upload must succeed before the protected job becomes eligible. Runtime GitHub/OIDC credentials are checked before publication; the first required evidence save establishes actual reporting ability before public writes. npm enforces its authorization at publication. An npm denial after a GitHub write remains a partial release with the earlier identity preserved. No token fallback is selected. Authored YAML or fixture results do not establish that remote setup is already configured.

The integration uses GitHub's [environment protection](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments), [immutable artifact action](https://github.com/actions/upload-artifact/tree/v4), [artifact identity API](https://docs.github.com/en/rest/actions/artifacts) and npm's [trusted-publishing configuration](https://docs.npmjs.com/trusted-publishers/). Setup is a separately authorized maintainer action; implementing this change does not configure remote infrastructure or publish a version.

## Read current outcomes and recover

Use the configured ref explicitly when inspecting new-path evidence:

```bash
RELEASE_EVIDENCE_REF=refs/heads/release-evidence python scripts/release-coordinator.py read-evidence --tag v0.5.1
```

The tag above is an argument example, not a claim that v0.5.1 has been published. The reader checks candidate identity, completed public identities and companion evidence; timing-format diagnostics are reported separately. Incomplete outcomes return a failing status. Historical checked-in releases retain their original readers and bytes; a missing new-path record is not a historical success fallback.

The ref contains the standing record, profile, approved candidate description, full-check receipt, notes, archive report and observed release/companion/timing projections. After required closeout is durable, tooling attempts to mirror that exact version-scoped Git evidence snapshot as `release-evidence-<commit>.zip` on the GitHub release. The later standing record reports the mirror identity or its unavailability. A mirror failure alone does not invalidate the authoritative evidence ref. These observed projections do not modify the sealed source or npm tarball. Source-tree pending files are preparation inputs, not current publication truth.

On an exception, retain the `release-observation-<run>-<attempt>` artifact and inspect the evidence ref and public identities. A later attempt restores the original candidate and the latest retained failed-attempt observations before continuing. It inspects existing tag/assets/npm state and only performs missing authorized writes. Conflicts stop; successful boundaries and prior failures remain recorded. A reporting failure remains incomplete even if publication happened. Expired recovery evidence or divergent history needs explicit disposition rather than blind retry. Duration measurements are collected where available; missing phase measurements and malformed timing remain visible diagnostics without turning a correct public result into failure by themselves.

## Historical and exceptional records

The standing release-process contract uses one version-scoped evidence file per publish attempt:

```text
docs/releases/v<version>.md
```

Use `templates/release-evidence.md` when preparing a release record. The evidence file records what was published, from which source, through which gate, by which publish path, and with which registry verification. It is operational proof for already-reviewed work; it does not approve new source behavior, package behavior, release-process changes, package-surface changes, authentication/provenance policy changes, adapter targets, or publish mechanics.

Existing release-specific files under `docs/releases/<version>/`, such as `release.yaml`, `release-notes.md`, and `npm-publication.md`, remain valid release evidence for their release-specific contracts. The standing `docs/releases/v<version>.md` record layers the routine publish checklist over those surfaces and may link to them when applicable.

Routine publishes do not update `docs/plan.md` unless the release is part of an active lifecycle plan. Link related lifecycle change records from the release evidence when the release is tied to a change.

Do not record npm tokens, OTPs, credentials, private keys, private environment dumps, hostnames, usernames, home-directory paths, or machine-local temporary paths in release evidence. Record command families, public registry references, package names, versions, dist-tags, integrity values, and concise command/result summaries instead.

Emergency release deferrals are exceptions, not a normal release path. Evidence must name each deferred gate item, approving owner or owning stage, rationale, validation impact, accepted risk, follow-up location, and deadline or next lifecycle stage. Release evidence creation, secret suppression, source/package/version/dist-tag recording, publish-path recording, registry verification, and recovery/follow-up recording are non-deferrable.
