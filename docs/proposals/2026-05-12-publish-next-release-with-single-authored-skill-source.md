# Publish Next Release With Single Authored Skill Source

## Status

accepted

## Problem

RigorLoop is migrating toward one authored skill source:

```text
skills/
```

The accepted single-authored-source proposal and approved spec define `.codex/skills/` as a repository-local Codex runtime directory, not authored source. For this release proposal, `.codex/skills/` should be treated as an ignored local install target only. The release surfaces are canonical `skills/`, public adapter output under `dist/adapters/`, release metadata, release notes, and token-cost evidence.

The first implementation slice has removed or is removing tracked `.codex/skills/`. The next problem is release readiness.

The next public release needs to preserve three things at once:

- single authored skill source: contributors edit only `skills/`;
- adapter install compatibility: downstream users can still install Codex, Claude Code, and opencode adapters reliably;
- release proof: release validation proves canonical skills and public adapter output can be produced and validated without relying on `.codex/skills/`.

The latest published GitHub release is `v0.1.0` as of this proposal. Its release notes describe generated adapter package installation from `dist/adapters/` and release verification that checks generated `.codex/skills/`, generated adapter drift, adapter validation, release metadata, release notes, and security scans. The next release should update that release contract so `.codex/skills/` is not part of required release evidence.

## Goals

- Publish the next stable RigorLoop release using `skills/` as the only authored skill source.
- Keep `.codex/skills/` untracked and ignored as a local runtime install directory.
- Preserve public adapter support for Codex, Claude Code, and opencode.
- Keep `dist/adapters/**` public adapter skill copies tracked for this release as a compatibility window, unless a separate release-artifact migration is already complete.
- Update release validation so it proves public adapter output can be generated and validated from canonical `skills/`.
- Preserve adapter validation for public adapter packages.
- Record release evidence for public adapter output, token-friendliness, adapter validation, and source-of-truth boundaries.
- Avoid changing skill behavior as part of this release packaging slice.

## Non-goals

- Do not remove public adapter skill copies under `dist/adapters/**/skills` in this release unless release artifacts, installation docs, and compatibility notices are already accepted and implemented.
- Do not remove support for Codex, Claude Code, or opencode.
- Do not rewrite Git history to remove prior generated output.
- Do not change skill wording or workflow behavior in this release slice.
- Do not introduce a new package manager, hosted registry, or installer.
- Do not make downstream users generate adapters manually before downloadable release artifacts are available.
- Do not treat `.codex/skills/` as a release source of truth.
- Do not make `.codex/skills/` generation required release evidence.
- Do not publish, tag, merge, or otherwise perform the release as part of proposal authoring.

## Vision fit

fits the current vision

This release preserves RigorLoop's reviewability and traceability by making source ownership clearer: humans review authored skills once, while public adapter output is validated rather than treated as authored content.

## Context

The accepted single-authored-source proposal chooses this model:

```text
Authored source:
  skills/

Local Codex runtime install target:
  .codex/skills/

Generated public adapter packages:
  dist/adapters/

Tracked metadata:
  dist/adapters/manifest.yaml
  dist/adapters/README.md
  docs/reports/adapter-artifacts/releases/<version>.yaml
```

The approved spec, `specs/single-authored-skill-source-generated-output.md`, intentionally amends older generated-output expectations in the multi-agent adapter and skill-contract specs. It says `.codex/skills/` becomes untracked first, public adapter skill copies remain tracked until at least one stable public release provides downloadable adapter artifacts and release-artifact install documentation, and existing tracked `dist/adapters/**/skills` drift checks remain in force until that later migration.

`CONSTITUTION.md`, `AGENTS.md`, `README.md`, and `docs/workflows.md` already state that `skills/` is the only authored skill source, `.codex/skills/` is ignored local Codex runtime output, and public adapter packages under `dist/adapters/` remain tracked generated installable output during the compatibility window. This proposal narrows release readiness further: the release gate should validate the public Codex adapter path, not `.codex/skills/`.

The public latest release, `v0.1.0`, says users install adapters by copying adapter package roots under `dist/adapters/`, and it lists Codex, Claude Code, and opencode package roots. It also names `bash scripts/release-verify.sh v0.1.0` as the repository-owned release gate and says that gate checks generated `.codex/skills/`.

Therefore, the next release should be a transition release:

```text
single authored skill source for repository development
+ ignored .codex local install target
+ public dist/adapters install path retained for compatibility
+ release proof through public adapter output
```

This proposal does not rely on `docs/project-map.md`; no project map is present in this checkout.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Continue after `.codex/skills/` untracking. | in scope | Problem; Goals; Recommended direction |
| Publish the next version. | in scope | Goals; Proposed release version; Rollout and rollback |
| Keep single authored skills. | in scope | Goals; Source-of-truth rule for release notes |
| Preserve adapter support. | in scope | Goals; Non-goals; Compatibility window |
| Avoid tracking local Codex install output. | in scope | Goals; Release validation |
| Do not break downstream adapter users. | in scope | Goals; Non-goals; Compatibility window |
| Keep public adapter cleanup staged. | in scope | Non-goals; Follow-on artifacts |
| Update release validation after `.codex/skills/` untracking. | in scope | Release validation |
| Record token-cost and adapter release evidence. | in scope | Goals; Token-cost and benchmark behavior; M3 |
| Avoid skill behavior changes. | in scope | Goals; Non-goals; Acceptance criteria |
| Make RigorLoop local Codex use follow the public adapter path. | in scope | Local Codex use; Acceptance criteria |

## Options considered

### Option 1: Release immediately with only `.codex/skills/` untracked

Advantages:

- Smallest next release change.
- Confirms the single-authored-source boundary.
- Avoids changing public adapter installation yet.
- Keeps release risk low.

Disadvantages:

- Still tracks public adapter skill copies under `dist/adapters/`.
- Does not complete the full generated-output cleanup.
- Requires clear release notes so contributors do not mistake tracked public adapters for authored source.
- If interpreted as proving `.codex/skills/` generation directly, it preserves a privileged internal Codex path.

### Option 2: Remove `.codex/skills/` and public adapter skill copies before this release

Advantages:

- Reaches the cleanest source model quickly.
- Reduces duplicate tracked skill text most aggressively.

Disadvantages:

- Breaks the current `dist/adapters/` repository-tree install path unless release artifacts and docs are ready.
- Requires more release packaging, checksum, artifact, benchmark, and validation work.
- Conflicts with the approved compatibility-window direction unless an explicit exception is accepted.
- Higher risk for the next public release.

### Option 3: Transition release with `.codex/skills/` untracked and public adapters retained

Advantages:

- Establishes `skills/` as the single authored source while leaving `.codex/skills/` as a local install target.
- Preserves current public adapter install compatibility.
- Gives one stable release to introduce or prepare generated adapter release artifacts and install docs.
- Matches the accepted staged migration.
- Lets RigorLoop local Codex use follow the same public Codex adapter path users receive.

Disadvantages:

- Does not remove all duplicate generated public adapter copies yet.
- Requires release notes to explain the transition clearly.
- Keeps adapter drift checks in place for tracked public adapter output during the compatibility window.

## Recommended direction

Choose Option 3.

Publish the next stable release as a single-authored-source transition release.

For this release:

```text
skills/ is the only authored skill source.
.codex/skills/ is an ignored local runtime install directory, not generated release output.
RigorLoop local Codex use follows the public user path: generate or use the Codex adapter, then install or copy it into .codex/skills/.
dist/adapters/** public adapter packages remain tracked for compatibility.
downloadable adapter archives are a follow-on migration by default.
release validation proves canonical skills and public adapter output are valid.
release validation does not require .codex/skills/ generation.
```

`v0.1.1` does not require downloadable adapter archives. For this transition release, `dist/adapters/` remains the public adapter install path. Downloadable adapter archives remain a follow-on migration and should not block this release unless a separate accepted plan completes archive generation, checksums, metadata, release notes, and install validation. If archives are easy to produce and already validated, they may be published as experimental convenience assets, but they should not replace `dist/adapters/` or become the release gate for `v0.1.1`.

Public adapter skill copies should move to release artifacts in a later release after:

```text
downloadable per-adapter archives exist
dist/adapters/README.md explains installation
adapter artifact metadata and checksums are tracked
release notes announce the repository-tree install transition
token-cost benchmarks install from generated temp output or release artifacts
```

## Proposed release version

Use:

```text
v0.1.1
```

The public latest release is `v0.1.0`, and the local tag list in this checkout only contains `v0.1.0`. If a maintainer creates or discovers a newer stable release before implementation planning, the plan should use the next available version and update release-note, report, and validation paths consistently.

## Source-of-truth rule for release notes

Release notes should state:

```text
Canonical authored skills live under skills/.

.codex/skills/ is an ignored local runtime install directory, not release evidence.

Public adapter packages remain available under dist/adapters/ for this transition release.
```

## Local Codex use

RigorLoop should consume its own Codex skills the same way users do.

For local Codex use:

```text
generate or validate the public Codex adapter output
copy or install that output into .codex/skills/ as a local ignored runtime directory
do not make .codex/skills/ part of release evidence
```

The exact local install command can be decided in the downstream plan. The command should use the public Codex adapter output under `dist/adapters/codex/.agents/skills/` during the compatibility window, or generated temporary Codex adapter output after public adapter untracking.

`.codex/skills/` is not a release artifact, not a validation source, and not tracked generated output.

## Release validation

For this transition release, the release gate validates:

```text
canonical skills under skills/
public adapter packages under dist/adapters/
adapter manifest and install documentation
tracked dist/adapters package output is current for this compatibility release
release token-friendliness metadata
release notes describing the single-authored-source transition
.codex/skills/ is ignored and not tracked
```

The release gate does not build or validate `.codex/skills/`.

If local Codex smoke is desired, it may be a separate optional check that installs the public Codex adapter into `.codex/skills/` in a temporary or local environment. That optional smoke should not be required release evidence.

For public adapters, because `dist/adapters/**` remains tracked in this release:

```text
build-adapters --check may still validate tracked public adapter output
validate-adapters validates public adapter package structure
```

Later, after public adapter untracking, adapter validation should switch to temporary-output or release-artifact validation.

## Release gate ownership

`bash scripts/release-verify.sh <version>` is the maintainer-facing final stable release gate.

`scripts/validate-release.py` owns structured validation for release metadata, token-cost reports, adapter evidence, release notes, and related release artifacts.

`release-verify.sh` may delegate structured checks to `validate-release.py`, but maintainers should have one final command to run for public release readiness.

## Adapter artifact metadata

This release does not require downloadable adapter archives or adapter artifact metadata.

If no archives are published, explicitly state:

```text
No downloadable adapter archives are introduced in this release.
dist/adapters/ remains the public adapter install path.
```

If a separate accepted plan publishes experimental convenience archives for this release, track:

```text
docs/reports/adapter-artifacts/releases/v0.1.1.yaml
```

with fields such as:

```yaml
schema_version: 1

release:
  version: v0.1.1
  commit: <source-commit-sha>
  date: "2026-05-12"

generator:
  command: "python scripts/build-adapters.py --version v0.1.1 --output-dir <release-output-dir>"
  source_skills: "skills/"
  manifest: "dist/adapters/manifest.yaml"

artifacts:
  - adapter: codex
    archive: "rigorloop-adapter-codex-v0.1.1.zip"
    sha256: "<sha256>"
    install_root: ".agents/skills/"
  - adapter: claude
    archive: "rigorloop-adapter-claude-v0.1.1.zip"
    sha256: "<sha256>"
    install_root: ".claude/skills/"
  - adapter: opencode
    archive: "rigorloop-adapter-opencode-v0.1.1.zip"
    sha256: "<sha256>"
    install_root: ".opencode/skills/"

validation:
  command: "python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.1"
  result: pass
```

## Adapter install guide

`dist/adapters/README.md` should be updated as the tracked user-facing adapter install guide before release.

It should explain:

```text
canonical skills source: skills/
for v0.1.1, install adapters from tracked repository-tree package roots under dist/adapters/
public adapter package roots: dist/adapters/<adapter>/ for this transition release
local Codex setup: install or copy from dist/adapters/codex/.agents/skills/ into .codex/skills/
no downloadable adapter archives are required for v0.1.1 unless separately published
future release artifacts: planned migration path
release artifact metadata path when artifacts exist: docs/reports/adapter-artifacts/releases/<version>.yaml
do not edit generated adapter output by hand
```

Local setup docs should explain:

```text
RigorLoop uses the same Codex adapter path as downstream users.
Generate or use the public Codex adapter package.
Copy the adapter skills into the local .codex/skills/ runtime directory.
Keep .codex/skills/ untracked.
Edit canonical skills under skills/.
```

## Token-cost and benchmark behavior

Token-cost static measurement should measure:

```text
skills/
```

not duplicate generated mirrors.

Dynamic benchmarks should install skills from:

```text
dist/adapters/codex/.agents/skills/
```

while public adapter output remains tracked.

They should not use:

```text
.codex/skills/
```

as the public skill source.

This matches the accepted token-cost benchmark direction and the approved single-authored-source spec's token-cost source rule.

## Expected behavior changes

Before:

```text
release validation expects tracked .codex/skills/ as generated mirror output
```

After:

```text
release validation validates canonical skills and public adapter output; .codex/skills/ is outside required release evidence
```

Before:

```text
contributors may see .codex/skills/ as another tracked skill tree
```

After:

```text
contributors edit skills/ only
```

Before:

```text
public adapter install path is dist/adapters/
```

After this transition release:

```text
public adapter install path remains dist/adapters/
future releases may introduce downloadable adapter artifacts
```

## Architecture impact

No runtime architecture change is expected.

This is a release packaging, validation, and source-of-truth boundary update. It affects release validation and distribution surfaces, not skill behavior or agent runtime behavior.

Affected surfaces may include:

```text
README.md
CONSTITUTION.md
AGENTS.md
docs/workflows.md
dist/adapters/README.md
dist/adapters/manifest.yaml
scripts/build-adapters.py
scripts/validate-adapters.py
scripts/test-skill-validator.py
scripts/test-adapter-distribution.py
scripts/release-verify.sh
scripts/validate-release.py
release notes under docs/releases/<tag>/release-notes.md
token-cost reports
.gitignore
```

Because `.codex/skills/` has already been removed or untracked, this proposal is about release readiness and compatibility, not the initial cleanup itself. Downstream work should update any contributor docs that still tell maintainers to generate `.codex/skills/` directly for release purposes.

## Testing and verification strategy

Likely focused validation includes:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-adapters.py --version v0.1.1 --check
python scripts/validate-adapters.py --version v0.1.1
python scripts/test-adapter-distribution.py
python scripts/measure-skill-tokens.py
git diff --check --
```

If the release process has or keeps a release command:

```bash
bash scripts/release-verify.sh v0.1.1
```

but only after it is updated so it no longer requires tracked `.codex/skills/`.

If release token-friendliness is required:

```bash
python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.1.yaml
```

If optional local Codex smoke is desired, it should install from public Codex adapter output into a temporary or ignored `.codex/skills/` location. That smoke should be separate from required release evidence.

The downstream plan can decide the exact optional local setup or smoke command. Required release validation should remain centered on canonical skills and public adapter output.

## Acceptance criteria

- `.codex/skills/` is untracked and ignored.
- `.codex/skills/` is not required by release validation.
- `.codex/skills/` is absent from release evidence except as optional local smoke setup.
- Release validation validates canonical `skills/`.
- Release validation validates public adapter output under `dist/adapters/` during the compatibility window.
- `bash scripts/release-verify.sh <version>` is the maintainer-facing final stable release gate and delegates structured checks to `scripts/validate-release.py` where appropriate.
- RigorLoop local Codex setup docs tell contributors to install or copy from public Codex adapter output into `.codex/skills/`.
- `skills/` is documented as the only authored skill source.
- `dist/adapters/**` public adapter package output remains available for this transition release.
- `dist/adapters/README.md` is updated with version-aware `v0.1.1` transition install guidance.
- Downloadable adapter archives are not required for `v0.1.1`; if absent, release notes or docs state that `dist/adapters/` remains the public install path.
- Release notes explain the `.codex/skills/` tracking change.
- Token-cost static measurement uses canonical `skills/`.
- Dynamic token-cost benchmarks do not read or install from `.codex/skills/`.
- Codex benchmark fixtures install from public Codex adapter output.
- Public adapter support for Codex, Claude Code, and opencode remains valid.
- No skill behavior changes are introduced by this release packaging slice.

## Rollout and rollback

### M1: Release validation after `.codex` untracking

- Update release verification so it does not require tracked `.codex/skills/`.
- Validate canonical skills and public adapter output.
- Keep `scripts/release-verify.sh` as the maintainer-facing release gate and delegate structured release artifact checks to `scripts/validate-release.py`.
- Confirm `.codex/skills/` is ignored, untracked, and outside required release evidence.
- Keep `dist/adapters/**` checks unchanged while tracked public adapter output remains in the compatibility window.

### M2: Release documentation

- Update README, `dist/adapters/README.md`, and release notes as needed.
- State `skills/` is the authored source.
- State `.codex/skills/` is an ignored local runtime install directory.
- State local Codex setup installs or copies from public Codex adapter output into `.codex/skills/`.
- State `dist/adapters/` remains the `v0.1.1` transition release adapter install path.
- State downloadable adapter archives are not required for `v0.1.1` unless separately published.
- Ensure adapter artifact metadata paths use `docs/reports/adapter-artifacts/releases/<version>.yaml`, or `docs/reports/adapter-artifacts/releases/v0.1.1.yaml` only when `v0.1.1` metadata exists.

### M3: Token-cost and adapter evidence

- Run static skill measurement.
- Run or validate the required token-cost release report.
- Run adapter validation.
- Record release evidence.

### M4: Publish release

- Tag and publish `v0.1.1` or the next available version after proposal review, downstream artifacts, implementation, review, explanation, verification, and PR readiness are complete.
- Include release notes explaining the single-authored-source transition.
- Attach adapter artifacts only if a separate accepted plan completes archive generation, checksums, metadata, release notes, and install validation; otherwise retain `dist/adapters/` as the install path.

If release validation fails because it still depends on `.codex/skills/`:

```text
do not publish the release
fix release validation to stop requiring .codex/skills/
or temporarily defer release until validation catches up
```

Do not re-track `.codex/skills/` unless a maintainer explicitly decides to postpone the migration. The preferred recovery is to validate canonical skills and public adapter output.

If public adapter packaging fails:

```text
keep dist/adapters/ as the public install path for this release
defer downloadable archives to a later release
```

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Release validation still expects tracked or generated `.codex/skills/`. | Update release verification before publishing so it validates public adapter output instead. |
| Users do not know how to install adapters. | Keep `dist/adapters/` tracked and document it. |
| Contributors think local Codex setup disappeared entirely. | Document install or copy from the public Codex adapter into ignored `.codex/skills/`. |
| Token benchmark accidentally uses `.codex/skills/`. | Keep the benchmark source rule and metadata validation. |
| Public adapter release artifacts are not ready. | Use transition release with `dist/adapters/` retained; do not require archives for `v0.1.1`. |
| Drift checks become unclear. | Keep release drift checks focused on tracked public adapter output during the compatibility window. |
| Publishing becomes stronger than lifecycle readiness. | Keep publishing out of proposal authoring and require downstream plan, implementation, review, verification, and PR readiness first. |

## Open questions

None.

Resolved by proposal direction:

- `v0.1.1` does not require downloadable adapter archives. `dist/adapters/` remains the public adapter install path, and archives are a follow-on migration unless a separate accepted plan completes them before release.
- `bash scripts/release-verify.sh <version>` remains the maintainer-facing final stable release gate, with `scripts/validate-release.py` owning delegated structured checks.
- `dist/adapters/README.md` needs a small version-aware update before release, including `v0.1.1` repository-tree install guidance and the correct adapter artifact metadata path wording.
- Optional local Codex smoke stays outside required release evidence. If used, it installs public Codex adapter output into `.codex/skills/` only as local setup or smoke validation.

These resolved decisions should be carried into proposal-review and implementation planning.

## Decision log

| Date | Decision | Reason |
|---|---|---|
| 2026-05-12 | Propose the next release as a single-authored-source transition release. | `.codex/skills/` tracking has been removed or is being removed; release needs proof and docs for public adapter output. |
| 2026-05-12 | Keep public `dist/adapters/` install path for this release. | Current public release still uses repository-tree adapter packages, and the approved spec requires a compatibility window. |
| 2026-05-12 | Do not require downloadable adapter artifacts before this release unless already ready. | Avoid blocking the `.codex` cleanup release on a larger packaging migration. |
| 2026-05-12 | Use `skills/` as the only authored source. | The accepted source-boundary proposal and approved spec already choose this model. |
| 2026-05-13 | Remove `.codex/skills/` from required release validation. | `.codex/skills/` is a local ignored install directory; release proof should validate the public Codex adapter path users receive. |
| 2026-05-13 | Keep downloadable adapter archives as a follow-on migration by default for `v0.1.1`. | Avoid changing the public install model in the same release that settles `.codex/skills/` tracking. |
| 2026-05-13 | Keep `scripts/release-verify.sh` as the maintainer-facing release gate and delegate structured checks to `scripts/validate-release.py`. | Preserve the `v0.1.0` release command while giving structured validators clear ownership. |
| 2026-05-13 | Update `dist/adapters/README.md` before release. | It needs version-aware `v0.1.1` transition guidance and artifact metadata path clarity. |

## Next artifacts

```text
proposal-review
spec or release-process amendment, if needed
plan
test-spec
implementation
code-review
explain-change
verify
pr
release notes
```

## Follow-on artifacts

None yet.

Expected follow-on work after this proposal settles:

- Public adapter release-artifact migration.
- Optional adapter artifact metadata report for the release that publishes archives.
- Future release that stops tracking public adapter skill copies after the compatibility window.

## Readiness

Accepted by proposal-review and ready for spec or release-process amendment.

## Core invariant

```text
Author skills once in skills/.
Generate public adapter output from canonical skills.
Install public Codex adapter output locally when Codex runtime setup is needed.
Keep public adapter install compatibility until release artifacts replace it.
Publish the next release with clear source ownership and validation evidence.
```
