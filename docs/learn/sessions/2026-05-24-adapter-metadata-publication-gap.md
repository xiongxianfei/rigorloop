# Learn Session: Adapter Metadata Publication Gap

## Result

- Skill: learn
- Status: captured; routing pending contributor confirmation
- Artifacts changed:
  - `docs/learn/sessions/2026-05-24-adapter-metadata-publication-gap.md`
- Open blockers:
  - Contributor confirmation is required before topic updates or process follow-up routing.
- Next stage:
  - None by default. Candidate follow-ups should route to release validation, npm package validation, or active release-plan artifacts if confirmed.
- Session path:
  - `docs/learn/sessions/2026-05-24-adapter-metadata-publication-gap.md`
- Lessons captured:
  - No new durable topic entry yet; candidate lessons are recorded below.
- Follow-ups:
  - Candidate process follow-ups are listed under Route.

## Frame

- Trigger: explicit maintainer invocation of `$learn` after a user-facing `npx @xiongxianfei/rigorloop@0.2.0 init --adapter codex` failure with `Codex adapter single-root metadata is incomplete.`
- Trigger type: explicit maintainer request / published package incident / failed adapter smoke.
- Scope:
  - Published `@xiongxianfei/rigorloop@0.2.0` npm package metadata.
  - Bundled v0.2.0 adapter metadata under `packages/rigorloop/dist/metadata/`.
  - CLI metadata validation for single-root adapters.
  - Existing tests and release evidence that did not catch the failure before publication.
- Evidence in scope:
  - `npm pack @xiongxianfei/rigorloop@0.2.0` showed the published tarball includes `dist/metadata/adapter-artifacts-v0.2.0.json` without Codex `file_count`.
  - `packages/rigorloop/dist/metadata/adapter-artifacts-v0.2.0.json` omitted Codex `file_count` and recorded stale Codex `tree_sha256`.
  - `packages/rigorloop/dist/bin/rigorloop.js` requires single-root metadata to include `tree_sha256` and integer `file_count`, then verifies the installed tree against those values.
  - `specs/multi-adapter-init-and-proxy-aware-download.md` requirement `MAI-R21a` requires single-root trusted metadata to include `install_root`, `tree_sha256`, and `file_count`.
  - Existing packed-package smoke in `scripts/test-npm-package-publication.py` ran `init --adapter codex --dry-run --json`; the CLI intentionally bypasses most metadata validation in dry-run.
  - Remediation updated `packages/rigorloop/dist/metadata/adapter-artifacts-v0.2.0.json`, `packages/rigorloop/dist/metadata/releases.json`, and `packages/rigorloop/test/cli.test.js`.
  - Verification after remediation:
    - `npm test --prefix packages/rigorloop`
    - `python scripts/test-npm-package-publication.py`
    - local fixed CLI `init --adapter codex --json` in an empty temp project succeeded through network download.
    - local fixed CLI `init --adapter codex --from-archive <generated v0.2.0 archive> --json` in an empty temp project succeeded.
    - `git diff --check -- packages/rigorloop/dist/metadata/adapter-artifacts-v0.2.0.json packages/rigorloop/dist/metadata/releases.json packages/rigorloop/test/cli.test.js`
- Explicit exclusions:
  - This session does not claim that npm `@0.2.0` is fixed. npm versions are immutable; the published `@0.2.0` package remains defective.
  - This session does not create authoritative release, validation, or CI policy.
  - This session does not update topic files without contributor confirmation.
  - This session does not perform PR readiness or release readiness verification.
- Prior learnings reviewed:
  - `docs/learn/README.md`
  - `docs/learn/sessions/2026-05-13-pr-ci-selector-release-metadata-incident.md`
  - `docs/learn/sessions/2026-05-18-adapter-init-and-proxy-fetch.md`
  - `docs/learn/sessions/2026-05-18-opencode-metadata-truth-table.md`

## Observe

### O1: Root cause was stale and incomplete package-bundled trusted metadata

The published `@0.2.0` npm package bundled Codex adapter metadata that did not satisfy the runtime contract. The Codex artifact entry lacked `file_count`, which triggers the direct error:

`Codex adapter single-root metadata is incomplete.`

After adding `file_count`, the same path exposed a second inconsistency: the recorded Codex `tree_sha256` did not match the files inside the v0.2.0 Codex adapter archive. The corrected values for the current v0.2.0 Codex archive are:

- `tree_sha256`: `6c01d71d2a0e4cd3b276092728f52de23345095b25ce2135b1a0759afd25c12e`
- `file_count`: `38`

Classification detail: this is an artifact assembly and validation gap, not a user project setup issue.

### O2: Pre-publish checks did not execute the same trust-root path as the real user command

Existing tests covered metadata validation behavior with generated fixtures, and package publication tests verified that the packed package could execute. However, the packed-package smoke used:

`init --adapter codex --dry-run --json`

The CLI's `archiveWorkForInit()` returns early for dry-run network mode before loading and validating bundled metadata. That makes dry-run useful for planning shape, but insufficient as a release smoke for packaged adapter metadata coherence.

The real user command:

`npx @xiongxianfei/rigorloop@0.2.0 init --adapter codex`

uses the installed package's bundled release index, bundled adapter metadata, official archive URL, archive checksum, tree hash, and file count. That exact path was not represented by the pre-publish package smoke.

### O3: Release metadata validation checked archive checksums but not CLI-consumable bundled metadata semantics

The release artifact metadata report and archive checksum evidence existed for v0.2.0, but the npm package bundled a JSON trust-root shape used by the CLI. The missing check was coherence across all three objects:

- generated adapter archive bytes;
- package-bundled adapter metadata JSON;
- package-bundled release index hash for that JSON.

The validation gap allowed a state where archive SHA-256 was correct, but CLI-required tree metadata was absent or stale.

### O4: Prior learning covers adjacent patterns but not the exact package-bundled metadata smoke gap

The May 13 release metadata incident already captured that new release artifact classes need selector routing and CI command shape designed together. The May 18 adapter/proxy session already captured that package versions, bundled adapter metadata, release assets, and real install smoke must stay coherent.

This incident is a concrete recurrence on the publication boundary: dry-run package smoke and archive checksum validation were not enough to prove a real package install command could complete.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Session record; already remediated in package metadata patch | Incident evidence and successful post-fix smoke | The immediate root cause is clear and evidence-bound. It does not by itself create new policy. |
| O2 | process-follow-up | pending confirmation | Add or update package publication validation to run non-dry-run `init --adapter codex` from a packed install using a generated or downloaded verified archive | Pending contributor confirmation | The pre-publish smoke did not match the real command. A focused non-dry-run smoke would catch this class. |
| O3 | artifact-update | pending confirmation | Update release/package validation scripts or release workflow docs so bundled metadata JSON is validated against generated archive tree hash and file count before publication | Pending contributor confirmation | The authoritative behavior belongs in validation scripts or release workflow artifacts, not in learn. |
| O4 | no-durable-lesson | no-durable-lesson | Cite prior release metadata and adapter init sessions | Prior sessions already captured the broader pattern | The broader reusable lesson exists; this session records a sharper instance and candidate concrete follow-ups. |

## Route

- Session record created: `docs/learn/sessions/2026-05-24-adapter-metadata-publication-gap.md`.
- No topic file updated.
- No authoritative artifact updated by this learn session.
- Candidate process follow-ups pending contributor confirmation:
  - Add a packed-package non-dry-run smoke for `init --adapter codex` that runs from an installed package in an empty temp project and verifies success.
  - Make the smoke hermetic by generating the release archive locally and using `--from-archive`, or use live download only in an explicitly release-gated public archive smoke.
  - Add validation that `packages/rigorloop/dist/metadata/adapter-artifacts-v<version>.json` records the exact tree hash and file count computed from the corresponding adapter archive.
  - Validate the bundled `releases.json` metadata SHA after any metadata rewrite.
  - Consider extending the check to all supported adapters, including multi-root `root_hashes` for opencode, so metadata validation uses the same semantics as the CLI.

## Direct Answer

Root cause:

- `@0.2.0` bundled incomplete and stale trusted Codex metadata. It missed `file_count`, and the recorded `tree_sha256` did not match the actual v0.2.0 Codex archive tree.

Why it was not detected before publish:

- The packed-package smoke used dry-run, and dry-run intentionally bypasses most bundled metadata validation for network mode.
- Existing tests mostly used generated fixture metadata, which was internally complete, rather than asserting the real bundled v0.2.0 metadata fields and tree hash.
- Release validation proved archive presence and checksums, but did not prove that the package-bundled JSON trust root was semantically complete and coherent with the archive tree.

Best practices:

- Treat package-bundled metadata as generated release evidence, not hand-maintained JSON.
- Validate the real package command path before publication: packed install, empty project, non-dry-run init, verified archive, lockfile contains expected `tree_sha256` and `file_count`.
- Keep dry-run tests, but do not count them as adapter metadata validation.
- Add a deterministic metadata-vs-archive check: compute tree hash and file count from the archive with the same rules the CLI uses, then compare against bundled metadata.
- Recompute and assert the `releases.json` bundled metadata SHA in the same check.
- Run the check for every supported adapter and every root shape, not only Codex.

## Validation

Validation run before this learn session:

```bash
npm test --prefix packages/rigorloop
python scripts/test-npm-package-publication.py
git diff --check -- packages/rigorloop/dist/metadata/adapter-artifacts-v0.2.0.json packages/rigorloop/dist/metadata/releases.json packages/rigorloop/test/cli.test.js
```

Additional validation for this learn record should run after writing the file:

```bash
git diff --check -- docs/learn/sessions/2026-05-24-adapter-metadata-publication-gap.md
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-05-24-adapter-metadata-publication-gap.md
```
