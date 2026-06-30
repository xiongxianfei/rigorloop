# Learn Session: Release Time Root Cause

## Result

- Skill: learn
- Status: session-recorded; no routing performed
- Artifacts changed: `docs/learn/sessions/2026-06-29-release-time-root-cause.md`
- Open blockers: contributor confirmation is required before routing follow-ups to release tooling, workflow docs, or topic guidance
- Next stage: none by default; possible `ci-maintenance`, proposal, or release-tooling implementation after confirmation
- Session path: `docs/learn/sessions/2026-06-29-release-time-root-cause.md`
- Lessons captured: candidate process lessons only; no durable topic update yet
- Follow-ups: pending confirmation

## Frame

Trigger:

The maintainer explicitly invoked `learn` after the `v0.3.4` release and asked why making a release costs so much time, what the root cause is, and what best practices would fix it.

Trigger type:

Explicit maintainer request / release-process retrospective.

Scope:

- The `v0.3.4` release preparation, publication, and post-publication evidence closeout.
- Time drivers in the local release-prep loop, GitHub Actions release workflow, npm trusted publishing, public smoke, and evidence update.
- Prior learn records for release time, release version gates, verification repetition cost, and validation runtime.

Evidence in scope:

- Release prep commit `fc152b4b` (`Prepare v0.3.4 release`): 17 files changed, 637 insertions, 147 deletions.
- Publication evidence commit `1246aa23` (`Record v0.3.4 publication evidence`): 3 files changed, 51 insertions, 47 deletions.
- `docs/releases/v0.3.4.md`
- `docs/releases/v0.3.4/npm-publication.md`
- `docs/releases/v0.3.4/release.yaml`
- `docs/releases/v0.3.4/release-notes.md`
- `scripts/release-verify.sh`
- `scripts/adapter_distribution.py`
- `scripts/test-adapter-distribution.py`
- `scripts/test-npm-package-publication.py`
- `scripts/npm_package_validation.py`
- `packages/rigorloop/test/cli.test.js`
- prior session `docs/learn/sessions/2026-05-13-release-version-gate.md`
- prior session `docs/learn/sessions/2026-05-16-v015-publication-time-retrospective.md`
- prior session `docs/learn/sessions/2026-06-24-verify-repetition-cost.md`
- prior session `docs/learn/sessions/2026-06-26-validation-runtime-speed-best-practices.md`
- prior session `docs/learn/sessions/2026-06-26-zero-runtime-improvement-root-cause.md`

Explicit exclusions:

- This session does not change release policy, CI behavior, validators, specs, or skills.
- This session does not claim a new authoritative release process.
- This session does not reopen or change the already-published `v0.3.4` release.
- This session does not treat every release-time cost as waste; public publication and smoke have required wall-clock cost.

Prior learnings reviewed:

- `2026-05-13-release-version-gate`: release gates intentionally fail closed, but version-specific behavior is scattered.
- `2026-05-16-v015-publication-time-retrospective`: public releases are broad supply-chain releases, not one-line version bumps.
- `2026-06-24-verify-repetition-cost`: expensive validation should follow cheap branch/evidence preconditions.
- `2026-06-26-validation-runtime-speed-best-practices`: broad smoke and serial validation are optimization candidates; cheap preflight should run first.
- `2026-06-26-zero-runtime-improvement-root-cause`: runtime reduction needs an actual speed actuator, not just measurement or classification.

## Observe

### O1 - The release is broad because the package version is coupled to adapter archive identity

Evidence:

- `fc152b4b` touched versioned package metadata, release evidence, package docs, package tests, release validation scripts, adapter metadata, and release reports.
- `packages/rigorloop/dist/metadata/releases.json` points the npm package version to `adapter-artifacts-v0.3.4.json`.
- `docs/releases/v0.3.4/npm-publication.md` records archive URLs, archive verification, tree hashes, file counts, and public `npx init` smoke for codex, claude, and opencode.

Observation:

The root release surface is not just `package.json`. A new version must make these surfaces coherent at the same time:

- npm package version;
- package README examples;
- bundled release metadata;
- GitHub release archive names, URLs, checksums, sizes, tree hashes, and file counts;
- CLI tests that assert exact version/archive behavior;
- release evidence and publication evidence;
- release gate allowlists and validation profiles.

This is a legitimate cost of a release model where the package installs verified external adapter archives.

### O2 - Version-specific release data is scattered across too many hand-edited surfaces

Evidence:

- `scripts/adapter_distribution.py` required adding `v0.3.4` to `RELEASE_TARGETS`, `ADAPTER_ARTIFACT_METADATA_REQUIRED_RELEASES`, `UNTRACKED_PUBLIC_ADAPTER_RELEASES`, `NPM_PUBLICATION_EVIDENCE_REQUIRED_RELEASES`, and `TARGET_NATIVE_INIT_RELEASES`.
- `scripts/release-verify.sh` required adding `v0.3.4` to multiple shell case lists.
- `scripts/npm_package_validation.py`, `scripts/test-npm-package-publication.py`, `scripts/test-adapter-distribution.py`, and many `packages/rigorloop/test/cli.test.js` assertions required current-version updates.
- Prior session `2026-05-13-release-version-gate` already observed that version-specific behavior should be explicit but not scattered.

Observation:

The main avoidable root cause is release-state duplication. The release contract is explicit and fail-closed, which is good, but the current implementation makes a routine release depend on remembering a long checklist of version literals across Python, shell, JSON, Markdown, and JS tests.

When one surface is missed, validation fails later and the release loop repeats.

### O3 - The full release gate is intentionally expensive and was rerun after edits

Evidence:

- `scripts/release-verify.sh v0.3.4` runs canonical skill validation, the full skill regression suite, generated skill drift checks, the adapter distribution regression suite, npm package publication tests, adapter archive building, and release metadata validation.
- During the release, the full gate passed only after earlier focused fixes to stale version assumptions and opencode metadata behavior.
- The adapter distribution suite alone reported 130 tests in 158.520 seconds during the successful full release gate.
- The final GitHub Actions release run then repeated release readiness on the pushed tag before creating the GitHub release and publishing npm.

Observation:

Part of the time is the intended safety gate. The release must prove more than local unit correctness: generated output currency, archive integrity, npm package contents, and release evidence consistency. However, rerunning the full gate while evidence shape and version-literal surfaces are still changing is avoidable.

### O4 - v0.3.4 had a specific avoidable evidence-shape loop

Evidence:

- Pre-publication release validation first required a change to `_local_release_candidate_metadata` because the current opencode archive contains `.opencode/commands`, while some fixture archives do not.
- Post-publication evidence validation later rejected:
  - command strings recorded with `npx -y` instead of the validator's expected `npx`;
  - raw tree hash values without the validator-required `sha256:<hex>` shape;
  - stale `release.yaml` expectations after evidence status changed from pending to published.
- After normalizing those fields, `python scripts/validate-release.py --version v0.3.4 --release-output-dir <tmp> --release-commit 4b8a03ed` passed.

Observation:

The evidence contract was stricter than the ad hoc draft evidence the agent wrote. That is a good validator behavior, but the release process exposed the schema late through trial and error. A release evidence generator or prefilled status transition command would have prevented this manual mismatch.

### O5 - External publication has irreducible sequential wait time

Evidence:

- GitHub Actions run `28375601052` succeeded with:
  - release job in 52 seconds;
  - `publish-npm-trusted` job in 53 seconds.
- Post-publication checks had to wait until GitHub release assets and npm package metadata were externally observable.
- Public smoke then ran `npx` from fresh temporary projects for `version`, `init codex`, `init claude`, and `init opencode`.

Observation:

This cost cannot be eliminated without weakening the release contract. Public release assets must exist before public install smoke can prove them. npm registry metadata must exist before `npm view` and `npx` smoke can validate the actual published package.

### O6 - Some prior runtime lessons apply, but v0.3.4 needed release automation more than raw parallelism

Evidence:

- Prior runtime sessions identify broad-smoke parallelism, check-level parallelism, and cheap preflight as candidate optimizations.
- v0.3.4's most visible avoidable loops were not raw test slowness alone; they were missing release-version registrations, stale tests, manually drafted evidence fields, and opencode metadata modeling.

Observation:

Parallelism would reduce the cost of the successful gate, but it would not address the main rework source. The best first fix is to reduce manual release-state drift and evidence-shape churn. After that, parallelism can reduce remaining wall-clock time.

## Root Cause

The high release cost has three layers:

1. Required cost: this is a public supply-chain release, not a one-line version bump. It must prove package contents, generated archives, checksums, metadata, GitHub release assets, npm trusted publishing, registry metadata, and real public install smoke.
2. Structural avoidable cost: release state is duplicated across many hand-edited surfaces. A routine release requires updating multiple allowlists, tests, metadata files, docs, and evidence records manually.
3. Execution avoidable cost: the process discovers missing version registrations and evidence-shape mismatches by running expensive validators, then rerunning them after fixes.

The most important root cause is not that any one test is too slow. It is that the release process lacks a single source of truth and generator for the routine version bump, adapter artifact metadata, and evidence status transition.

## Best Practices

Best practices for reducing release time without weakening safety:

1. Create one release profile source of truth.
   - Store the supported release tag, manifest version, package version, required evidence classes, adapter archive behavior, npm publication requirement, and target-native-init requirement in one structured profile.
   - Generate shell allowlists, validator constants, package metadata pointers, and expected test fixtures from it where practical.

2. Add a release-prep command.
   - Example shape: `python scripts/prepare-release.py v0.3.5`.
   - It should update package version, release metadata, adapter artifact metadata, release notes skeleton, release index, package validation expectations, and current-version test fixtures.
   - It should fail if any known current-version literal remains stale.

3. Add evidence generation for pending and published states.
   - Generate `docs/releases/<tag>.md`, `release.yaml`, and `npm-publication.md` from validator-compatible templates.
   - Provide a post-publish command that fills npm timestamp, tarball SHA, integrity, target init smoke rows, tree hashes, file counts, and closeout status using the exact schema the validator expects.

4. Run cheap release preflight before expensive release verification.
   - Check new version availability, local/remote tag absence, profile completeness, release evidence file presence, generated metadata presence, package version consistency, and validator vocabulary before `scripts/release-verify.sh`.
   - This follows prior verify-cost learnings: fail fast on cheap state issues before broad smoke.

5. Keep the full release gate, but make it the confirmation step.
   - `bash scripts/release-verify.sh <tag>` should remain the authoritative local release gate.
   - It should run after generated release-prep artifacts pass cheap consistency checks.

6. Reduce gate runtime only after drift is reduced.
   - Reuse the existing check-level `parallel_safe` model for broad-smoke or release-gate child checks.
   - Profile before parallelizing individual unittest suites.
   - Do not use parallelism to mask missing release profile generation.

7. Treat post-publication evidence as an automated closeout.
   - The release is not done until public GitHub assets, npm metadata, and fresh `npx` smoke pass.
   - Automate evidence collection so the second post-publish commit is mostly generated and validator-compatible.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | session record only | v0.3.4 release evidence and prior v0.1.5 session | Explains legitimate release cost already supported by prior learning. |
| O2 | process-follow-up | pending confirmation | possible release-tooling proposal or implementation plan | not confirmed | Repeated evidence shows scattered release state causes rework, but fixing it changes tooling and belongs in an owning artifact. |
| O3 | observation | observation | session record only | `release-verify.sh` command graph and release run evidence | The gate cost is intentional safety evidence, not itself a policy defect. |
| O4 | process-follow-up | pending confirmation | possible evidence generator / validator-compatible template update | not confirmed | The v0.3.4 loop is concrete and fixable, but routing requires contributor confirmation. |
| O5 | observation | observation | session record only | GitHub Actions and npm publication evidence | External publish wait time is irreducible under the current safety contract. |
| O6 | direction | pending confirmation | possible CI-maintenance for parallel release gate after automation | not confirmed | Parallelism may help after drift reduction, but the first fix should target release automation. |

Contributor confirmation status:

The maintainer confirmed the trigger and asked for root cause and best practices. No confirmation has been given yet to update release tooling, workflow docs, validators, topic guidance, or proposal artifacts from this session.

## Route

- Session record created.
- No topic file updated.
- No release tooling, workflow, validator, spec, or skill file changed.
- Candidate follow-ups are pending contributor confirmation.

## Candidate Follow-Ups

Pending contributor confirmation:

1. Proposal or direct scoped implementation: create a release profile source of truth and generate the duplicated version allowlists/constants from it.
2. Implement `scripts/prepare-release.py <tag>` to generate routine release-prep artifacts and detect stale current-version literals.
3. Implement `scripts/close-release-publication.py <tag>` to collect npm/GitHub public evidence and write validator-compatible published evidence.
4. Add a cheap release preflight mode that runs before `bash scripts/release-verify.sh <tag>`.
5. After release-state automation is in place, consider CI-maintenance for safe parallel execution of release-gate child checks.

## Validation

- `python scripts/select-validation.py --mode explicit --path docs/learn/sessions/2026-06-29-release-time-root-cause.md`: passed; selected `guide_system.validate`.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-06-29-release-time-root-cause.md`: passed; validated 0 artifact files.
- `git diff --check -- docs/learn/sessions/2026-06-29-release-time-root-cause.md`: passed.
- `python scripts/validate-guide-system.py`: passed.
