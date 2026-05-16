# v0.1.5 Publication Time Retrospective

## Frame

- Trigger: explicit maintainer invocation asking why publishing a new version took so much time despite a small change.
- Trigger type: maintainer request / release retrospective.
- Scope:
  - The `v0.1.5` trusted npm publication performed on 2026-05-16.
  - The repository changes, workflow retry, post-publication smoke, and publication evidence for `@xiongxianfei/rigorloop@0.1.5`.
- Evidence reviewed:
  - `docs/releases/v0.1.5/npm-publication.md`
  - commits `4057a04`, `fb04caa`, and `b2f843b`
  - `docs/learn/sessions/2026-05-13-release-version-gate.md`
  - `docs/learn/README.md`
- Explicit exclusions:
  - This session does not claim a new release policy.
  - This session does not change workflow, release scripts, specs, or package metadata.
  - This session does not claim CI status beyond the already recorded publication evidence.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-13-release-version-gate.md`

## Observe

### O1: The change looked small, but the release surface was not small

Publishing `0.1.5` required more than a package version edit. The first release commit changed the package version, adapter manifest, bundled adapter metadata, release index, tests, npm package validation expectations, release verification behavior, release evidence scaffolding, release notes, and adapter artifact reports.

The diff for `4057a04` touched 14 files with 301 insertions and 112 deletions. That is still a modest repository diff, but it is a broad release-surface diff.

### O2: Version-sensitive metadata multiplies a release bump

The CLI does not only print its own version. `init --adapter codex` uses package-bundled metadata that names a specific adapter release archive, URL, SHA-256, size, and tree hash. That means a new public package version also needs the matching adapter metadata and GitHub release assets to be coherent.

The real install smoke proved the `v0.1.5` Codex archive URL, archive SHA, extraction, tree hash, file count, and generated output. Dry-run smoke alone would not have caught stale or missing adapter assets.

### O3: The first trusted-publishing attempt exposed a missing provenance field

The first GitHub Actions publish attempt failed because npm provenance verification expected package repository metadata:

```text
package.json: "repository.url" is "", expected to match "https://github.com/xiongxianfei/rigorloop" from provenance
```

Fixing that required adding `repository` metadata, rerunning targeted validation, deleting the failed GitHub release/tag, recreating `v0.1.5` from the fixed commit, and rerunning the release workflow.

This was the largest avoidable delay in the publication step.

### O4: External release publication has unavoidable waiting and ordering

Unlike a normal local code change, npm publication depends on external systems:

- GitHub Actions workflow execution.
- GitHub release asset creation.
- npm trusted publishing and provenance verification.
- npm registry availability for `npm view` and `npx`.
- Post-publication real install smoke against public GitHub release assets.

Even when everything passes, these steps add wall-clock time because they cannot all be compressed into local validation.

### O5: Release evidence made the closeout longer, but prevented ambiguity

After npm published successfully, the work was not complete until publication evidence recorded the workflow run, npm package URL, provenance status, tarball SHA, `npx` smoke, and real Codex install smoke.

That evidence is why the final state is auditable instead of chat-only. It also means release closeout includes a second tracked commit after publication.

## Classify

| Observation | Proposed classification | Final classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | session record | release diff and commit stats | Explains why a version release was broader than a one-line bump. |
| O2 | observation | observation | session record | bundled metadata and real install evidence | Explains why adapter install coherence was part of the release cost. |
| O3 | process-follow-up candidate | pending confirmation | possible release preflight check for npm provenance repository metadata | pending contributor confirmation | The failed workflow exposed a reusable missing preflight check, but routing needs confirmation. |
| O4 | observation | observation | session record | publication evidence and external workflow sequence | External wait time is expected for public release execution. |
| O5 | observation | observation | session record | `docs/releases/v0.1.5/npm-publication.md` and evidence commit | Evidence closeout cost was intentional and traceability-driven. |

## Route

- Session record created: `docs/learn/sessions/2026-05-16-v015-publication-time-retrospective.md`.
- No topic file updated.
- No authoritative artifact updated.
- Candidate follow-up pending contributor confirmation:
  - Add a release preflight check that fails before tag publication when `packages/rigorloop/package.json` lacks `repository.url` matching `https://github.com/xiongxianfei/rigorloop`.

## Practical Answer

The release took time because it was not only a small code change. It was a public supply-chain release.

The slow parts were:

1. Version-sensitive adapter metadata had to be regenerated and validated.
2. Tests and release validators had hardcoded `0.1.4` assumptions that had to move to `0.1.5`.
3. The first trusted-publishing workflow failed because npm provenance required `package.json.repository.url`.
4. The failed release/tag had to be cleaned up and recreated from the fixed commit.
5. GitHub Actions, npm trusted publishing, npm registry checks, and real `npx` install smoke all require external wall-clock time.
6. Final publication evidence had to be committed after npm publication, because that evidence cannot exist before publication.

The main avoidable delay was the provenance failure. A preflight check for package repository metadata would have caught it before tagging.

## Validation

No validation commands were run for this learn session. The session adds only this Markdown record.
