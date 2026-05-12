# Single Authored Skill Source and Generated Adapter Output Cleanup

## Status

accepted

## Problem

RigorLoop currently keeps the same public skill text in multiple tracked trees:

```text
skills/
.codex/skills/
dist/adapters/codex/.agents/skills/
dist/adapters/claude/.claude/skills/
dist/adapters/opencode/.opencode/skills/
```

The authored source is `skills/`; the other trees are generated runtime or adapter output. The repository already says contributors edit canonical skills under `skills/`, do not hand-edit `.codex/skills/`, and do not hand-edit public adapter output under `dist/adapters/`.

The remaining problem is operational: generated skill copies are still tracked, reviewed, benchmarked, and drift-checked as ordinary repository content. A wording change to one skill can create repeated generated diffs across four derived skill trees, making review noisier and making source-of-truth boundaries harder to enforce.

## Goals

- Keep `skills/` as the only authored skill source.
- Reduce duplicate tracked skill text in ordinary Git diffs.
- Preserve deterministic generation for the local Codex mirror and public adapter packages.
- Preserve Codex, Claude Code, and opencode adapter support.
- Preserve release validation that proves generated adapters are structurally correct.
- Make contributor workflow simpler: edit canonical skills, build or check generated output, publish adapters through the release process.
- Keep downstream adapter installation reliable after generated skill copies are no longer day-to-day authored Git state.
- Keep release and benchmark evidence focused on canonical skill source and generated release output, not duplicated tracked mirrors.

## Initial Intent Preservation

| Initial user goal | Proposal treatment | Where recorded |
|---|---|---|
| Keep only one authored skill source. | in scope | Goals; Recommended direction; Proposed source-of-truth rule |
| Treat `skills/` as canonical. | in scope | Goals; Recommended direction |
| Treat `.codex/skills/` as a generated local Codex runtime mirror. | in scope | Recommended direction; Migration strategy |
| Treat public adapter skill copies as generated output rather than authored source. | in scope | Goals; Recommended direction; Migration strategy |
| Prefer release artifacts over day-to-day tracked adapter skill copies. | in scope | Recommended direction; Rollout and rollback |
| Preserve adapter package generation for Codex, Claude Code, and opencode. | in scope | Goals; Non-goals; Testing and verification strategy |
| Preserve release validation for generated adapters. | in scope | Goals; Testing and verification strategy |
| Avoid breaking current public adapter distribution. | in scope | Non-goals; Rollout and rollback; Risks and mitigations |
| Start with removing `.codex/skills/` if public adapter untracking is too risky. | in scope | Migration strategy; Decision log |
| Update token-cost and benchmark behavior so generated duplicates are not counted as authored cost. | in scope | Expected behavior changes; Testing and verification strategy |
| Define release artifact reproducibility before public adapter cleanup. | in scope | Release artifact reproducibility |
| Decide manifest ownership before public adapter cleanup. | in scope | Recommended direction; Manifest ownership |
| Make the first implementation slice `.codex/skills/` only. | in scope | First Implementation Slice |
| Define generated-output validation semantics after untracking. | in scope | Generated Output Validation After Untracking |
| Preserve compatibility for users who copy `dist/adapters/` from GitHub. | in scope | Public Adapter Compatibility Window |
| Avoid benchmarking `.codex/skills/` as the public skill source. | in scope | Token-cost Benchmark Source Rule |
| Avoid rewriting Git history to remove past generated output. | in scope | No History Rewrite |
| Do not change skill content or semantics. | out of scope | Non-goals |
| Do not remove adapter support. | out of scope | Non-goals |
| Do not delete generated adapter output before validation, packaging, and release docs are ready. | in scope | Non-goals; Rollout and rollback |

## Non-goals

- Do not change skill behavior or skill wording as part of this proposal direction.
- Do not remove support for Codex, Claude Code, or opencode adapters.
- Do not remove adapter generation scripts.
- Do not change the RigorLoop workflow stage order.
- Do not require downstream users to generate adapters manually unless release artifacts or equivalent distribution docs replace the current repository-tree install path.
- Do not delete generated public adapter skill copies before validation, release packaging, and installation docs are updated.
- Do not make generated output drift invisible; the replacement should validate generated output from canonical sources.
- Do not rewrite Git history to remove previously committed generated skill copies.

## Vision fit

fits the current vision

This proposal supports RigorLoop's commitment to reviewable, traceable, trustworthy automation by making the authored source of public skill guidance unambiguous and reducing generated duplicate noise in review.

## Context

`CONSTITUTION.md` defines canonical authored workflow content under `docs/`, `specs/`, `skills/`, `schemas/`, `scripts/`, and `templates/`. It also says generated Codex compatibility output under `.codex/skills/` is derived output, not a source of truth.

`README.md` currently presents generated adapter packages under `dist/adapters/` for Codex, Claude Code, and opencode. It also states that canonical skill edits happen in `skills/`, adapter packages under `dist/adapters/` are generated release output, and `.codex/skills/` is a separate generated local Codex runtime mirror. The Codex public adapter skill path is `dist/adapters/codex/.agents/skills/`, while `.codex/skills/` is repository-local runtime output.

The accepted multi-agent adapter release spec currently defines `dist/adapters/<adapter>/` as generated, tracked, independently installable package output. The accepted skill contract also expects generated `.codex/skills/` and `dist/adapters/` output to be regenerated or checked when canonical skills change. This proposal intentionally changes that packaging and generated-output tracking policy, so follow-on spec and validation updates are required before implementation.

This proposal does not rely on `docs/project-map.md`; no project map was present in this checkout.

## Options considered

### Option 1: Keep tracking all generated skill copies

This preserves the current model.

Advantages:

- Adapter packages remain visible directly in the repository tree.
- Users can copy adapter packages from GitHub without downloading release artifacts.
- Release diffs show exactly what generated output shipped.
- Existing drift validation can continue comparing generated files against tracked output.

Disadvantages:

- Every skill edit creates repeated generated diffs.
- Reviewers must inspect or deliberately ignore repeated copies of the same text.
- Generated copies can drift or be edited accidentally.
- Static analysis and token-cost tooling can overcount duplicated skill text.
- Git history grows with repeated generated artifacts.
- The source-of-truth boundary remains harder to explain and enforce.

### Option 2: Track only `skills/`; make all generated outputs untracked

This is the cleanest source model.

Advantages:

- One authored skill source is obvious.
- Ordinary PR diffs contain the canonical skill change once.
- Contributors are less likely to edit generated mirrors as source.
- Token-cost and static analysis can use canonical skill source by default.

Disadvantages:

- Users lose the current ability to copy public adapters directly from the repository tree unless release artifacts replace it.
- Release validation must build and validate adapters in a temporary output location.
- Existing specs, tests, docs, and scripts that expect tracked generated adapter packages need coordinated updates.
- Release artifacts become part of the public installation contract.

### Option 3: Track only `skills/` plus minimal generated release metadata; publish adapter packages as release artifacts

This preserves one authored source while keeping a durable support matrix or release metadata in the repository.

Advantages:

- Keeps ordinary review focused on canonical skill text.
- Preserves a visible adapter support matrix when `dist/adapters/manifest.yaml` or equivalent release metadata remains tracked.
- Lets CI build and validate generated output without committing all generated skill copies.
- Supports public adapter distribution through release artifacts.
- Gives the repository a staged migration path from tracked generated packages to generated release packages.

Disadvantages:

- Adds release-process complexity.
- Downstream users need updated installation instructions.
- The manifest contract may need to distinguish tracked metadata from generated package contents.
- Existing tests that compare tracked generated output need to move to temporary build output.

## Recommended direction

Choose Option 3.

RigorLoop should keep `skills/` as the only authored skill source and move generated skill mirrors out of ordinary authored Git state. Generated output should still be reproducible and validated, but the validation target should become generated temporary output or release artifact output rather than checked-in duplicate skill trees.

The steady-state model should be:

```text
Authored source:
  skills/

Generated local runtime output:
  .codex/skills/      # untracked or generated on demand

Generated public adapter packages:
  dist/adapters/      # generated for release; skill copies preferably untracked

Tracked generated or release metadata:
  dist/adapters/manifest.yaml
  dist/adapters/README.md
  docs/reports/adapter-artifacts/releases/<version>.yaml
  release metadata and release reports, where useful
```

The first implementation should be staged. Removing `.codex/skills/` from tracked content is the safest first slice because it is repository-local runtime output and not the public adapter install path. Public adapter skill copies under `dist/adapters/` should move to release artifacts only after release packaging, validation, benchmark inputs, and installation docs are ready.

For now, `dist/adapters/manifest.yaml` should remain tracked as release and support metadata unless a later accepted proposal moves it entirely into release artifacts. The manifest must not contain generated skill text. `dist/adapters/README.md` should be kept or added as tracked install guidance alongside the manifest.

Generated adapter release artifacts should be published as separate archives per adapter. A combined all-adapters archive may also be published for maintainer convenience, smoke testing, mirrors, or offline installs. Generated archives should not be committed to Git by default; release workflows should generate them, attach them to the release, and record checksums in tracked metadata.

## Manifest Ownership

`dist/adapters/manifest.yaml` remains tracked as the repository-visible adapter support matrix and release metadata for the current migration path. Public generated skill bodies should be removed from day-to-day tracked state only after the manifest role is preserved or replaced by an accepted follow-on contract.

The steady-state tracked adapter surface should be small:

```text
dist/adapters/manifest.yaml
dist/adapters/README.md
docs/reports/adapter-artifacts/releases/<version>.yaml
```

Generated skill bodies under adapter-specific skill paths should be generated into temporary build directories or release artifact directories once public adapter cleanup reaches that slice.

`dist/adapters/README.md` should document release-artifact installation and source ownership:

```text
canonical skills: skills/
adapter support matrix: dist/adapters/manifest.yaml
release artifact metadata: docs/reports/adapter-artifacts/releases/<version>.yaml
```

## First Implementation Slice

The first implementation slice removes only the repository-local Codex runtime mirror from tracked Git state:

```text
.codex/skills/
```

In scope:

- remove `.codex/skills/` from tracked files;
- add `.codex/skills/` to `.gitignore`;
- document the local regeneration command;
- update tests and validators that expected `.codex/skills/` to be tracked;
- prove the local Codex mirror can still be generated on demand.

Out of scope for the first slice:

- untracking `dist/adapters/**/skills`;
- changing public adapter installation paths;
- changing release artifact packaging;
- changing skill content.

First-slice acceptance criteria:

- `.codex/skills/` is removed from tracked files.
- `.codex/skills/` is ignored as generated local runtime output.
- A documented command regenerates the local Codex mirror.
- Validation proves `.codex/skills/` can be generated on demand.
- Tests no longer require tracked `.codex/skills/`.
- Public adapter trees under `dist/adapters/` remain unchanged in this slice.

## Proposed Source-of-truth Rule

```md
## Skill source of truth

`skills/` is the only authored skill source.

Generated skill mirrors and adapter skill directories are not edited as source.

Generated output may be created locally or during release validation, but generated
skill copies are not ordinary authored repository content.
```

## Expected Behavior Changes

Before this change, a canonical skill edit commonly produces:

```text
canonical skill diff
.codex mirror diff
Codex adapter skill diff
Claude adapter skill diff
opencode adapter skill diff
```

After this change reaches steady state, a canonical skill edit should produce:

```text
canonical skill diff
build/check generated outputs in CI or release validation
publish generated adapters as release artifacts
```

Reviewers should see one authored skill change and validation evidence for generated outputs. Token-cost and static skill-size tooling should measure canonical `skills/` for authored skill cost, while release benchmarks that need installed public skills should install generated adapter output from a temporary build or release artifact.

## Release artifact reproducibility

Before public adapter skill copies are untracked, every release that publishes generated adapter packages should record enough evidence for reviewers and downstream users to confirm that the artifacts were generated from tracked canonical sources and validation passed.

The release artifact evidence contract should include:

- source commit;
- adapter version;
- generator command;
- generated artifact paths;
- artifact checksums;
- adapter validation command and result;
- manifest or support matrix used;
- release note link to downloadable artifacts.

Release artifact metadata should be tracked at:

```text
docs/reports/adapter-artifacts/releases/<version>.yaml
```

A human-readable companion report may be added at:

```text
docs/reports/adapter-artifacts/releases/<version>.md
```

The release notes or release report should summarize the metadata file and adapter archive checksums.

Suggested metadata shape:

```yaml
schema_version: 1

release:
  version: v0.1.2
  commit: "<source-commit-sha>"
  date: "2026-05-12"

generator:
  command: "python scripts/build-adapters.py --version v0.1.2 --output-dir <release-output-dir>"
  source_skills: "skills/"
  manifest: "dist/adapters/manifest.yaml"

artifacts:
  - adapter: codex
    archive: "rigorloop-adapter-codex-v0.1.2.zip"
    sha256: "<sha256>"
    install_root: ".agents/skills/"
  - adapter: claude
    archive: "rigorloop-adapter-claude-v0.1.2.zip"
    sha256: "<sha256>"
    install_root: ".claude/skills/"
  - adapter: opencode
    archive: "rigorloop-adapter-opencode-v0.1.2.zip"
    sha256: "<sha256>"
    install_root: ".opencode/skills/"

combined_artifact:
  archive: "rigorloop-adapters-v0.1.2.tar.gz"
  sha256: "<sha256>"
  included_adapters:
    - codex
    - claude
    - opencode

validation:
  command: "python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.2"
  result: pass
  validated_at: "2026-05-12"

notes:
  - "Generated from canonical skills/ at the recorded commit."
```

Generated adapter release artifacts should be reproducible from tracked canonical sources and generation scripts at the recorded source commit.

Every public release that distributes generated adapters should publish one separate downloadable archive for each supported adapter:

```text
rigorloop-adapter-codex-v0.1.2.zip
rigorloop-adapter-claude-v0.1.2.zip
rigorloop-adapter-opencode-v0.1.2.zip
```

A combined all-adapters archive may also be published:

```text
rigorloop-adapters-v0.1.2.tar.gz
```

Generated archives should be generated in CI or the release workflow and uploaded as release assets. The repository should track metadata and checksums, not binary or generated archive files.

## Generated Output Validation After Untracking

After a generated skill output tree is untracked, generated-output validation should no longer mean equality with a tracked generated skill tree. It should mean:

- generation succeeds from canonical `skills/`;
- generated files have the expected local mirror or adapter layout;
- adapter manifests and metadata are valid;
- generated packages pass adapter validation;
- no tracked generated skill tree is required.

Validation should use temporary output directories or release artifact directories. If existing commands keep `--check`, the follow-on spec should define `--check` as validating generated temporary output rather than tracked file equality for any untracked generated tree.

When `.codex/skills/` becomes untracked, checks whose only purpose is comparing canonical skills against tracked `.codex/skills/` files should be retired. They should be replaced with temp-output generation and validation. Canonical `skills/` validation, skill-validator static assertions, adapter manifest checks, adapter package validation, and token-cost public skill portability checks should remain.

For `dist/adapters/**/skills`, tracked drift checks should remain while public adapter skill copies remain tracked. After public adapter skill copies move to release artifacts, those checks should also become temp-output adapter build and validation checks.

## Architecture Impact

No runtime product architecture change is expected. This is a repository packaging, validation, release, and source-of-truth boundary change.

Likely affected surfaces:

- `CONSTITUTION.md`
- `AGENTS.md`
- `README.md`
- `docs/workflows.md`
- `specs/multi-agent-adapters-first-public-release.md`
- `specs/multi-agent-adapters-first-public-release.test.md`
- `specs/skill-contract.md`
- `specs/skill-contract.test.md`
- `specs/release-token-friendliness-benchmark-for-skills.md`
- benchmark and token-cost specs that reference generated adapter paths
- `scripts/build-skills.py`
- `scripts/build-adapters.py`
- `scripts/validate-adapters.py`
- `scripts/test-skill-validator.py`
- `scripts/test-adapter-distribution.py`
- release verification scripts and CI wrappers
- `.gitignore`
- `.codex/skills/`
- `dist/adapters/`

Because the accepted adapter release spec currently treats `dist/adapters/<adapter>/` as tracked package output, follow-on work should update the governing specs before removing tracked public adapter skill copies.

## Testing and Verification Strategy

The follow-on spec should require proof that:

- canonical skills validate from `skills/`;
- the local Codex mirror can be generated on demand;
- public adapter packages can be generated into a temporary or release directory;
- adapter validation can run against generated output outside tracked `dist/adapters/` skill copies;
- release metadata and release notes point to the generated adapter packages users install;
- token-cost tooling measures canonical authored skill cost without counting duplicate tracked mirrors;
- dynamic release benchmarks install skills from generated public output or release artifacts, not from `.codex/skills/`;
- CI no longer depends on tracked duplicate skill copies after the relevant migration slice.

Likely validation command families:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version <version> --check
python scripts/validate-adapters.py --version <version>
python scripts/test-adapter-distribution.py
git diff --check --
```

If generation moves to explicit output directories, likely command shapes include:

```bash
python scripts/build-skills.py --output-dir /tmp/rigorloop-skills
python scripts/build-adapters.py --version <version> --output-dir /tmp/rigorloop-adapters
python scripts/validate-adapters.py --root /tmp/rigorloop-adapters --version <version>
```

Ordinary PR CI should build generated adapters when changed paths affect canonical skills, adapter generation, adapter templates, adapter manifest or support metadata, release packaging, release metadata, or related specs. Release validation should always build and validate generated adapters regardless of ordinary PR selector results.

## Public Adapter Compatibility Window

Public adapter skill copies under `dist/adapters/` should remain tracked for at least one stable public release after downloadable adapter artifacts and release-artifact installation documentation are available. If repository-tree copy-install usage appears substantial or installation docs change significantly, the follow-on spec may choose a longer compatibility window.

The release that first stops tracking public adapter skill copies should:

- publish adapter artifacts;
- document installation from release artifacts;
- preserve adapter support matrix metadata;
- mention repository-tree install path retirement in release notes.

The next stable release should not automatically stop tracking generated public adapter skill copies. It may do so only if release artifacts, install docs, validation, release metadata, benchmark inputs, and compatibility notices are ready. Otherwise, one stable release should publish downloadable artifacts while keeping `dist/adapters/**/skills` tracked, and a later stable release should remove the tracked public adapter skill copies.

## Token-cost Benchmark Source Rule

Token-cost dynamic benchmarks must not use `.codex/skills/` as their public skill source.

For Codex public-surface benchmarks, use one of:

- generated public adapter output from `dist/adapters/codex/.agents/skills/`, while still tracked;
- generated temporary adapter output after public adapter untracking;
- release artifact output after release packaging is adopted.

## No History Rewrite

This migration removes generated trees from future tracked state only. It does not rewrite Git history to remove prior generated skill copies.

## Rollout and rollback

Roll out in stages:

1. Clarify source boundaries in governing docs and specs.
2. Stop tracking `.codex/skills/` and add or confirm `.gitignore` coverage for the generated local mirror.
3. Update validation so local Codex mirror generation can be checked without treating `.codex/skills/` as authored source.
4. Prepare public adapter release packaging and temporary-output validation.
5. Stop tracking public adapter skill copies after release artifacts and installation docs are ready.
6. Update token-cost and dynamic benchmark inputs to use canonical skills and generated release output intentionally.

Rollback before public adapter untracking can restore the previous tracked `.codex/skills/` mirror policy by reverting `.gitignore`, generation, validation, and docs changes for that slice.

Rollback after public adapter untracking should retain the ability to regenerate adapter packages from `skills/` and either re-track generated adapter packages temporarily or republish release artifacts from the last known good generated output.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Users rely on copying `dist/adapters/` from GitHub. | Stage public adapter untracking until release artifacts and install docs are ready. |
| CI breaks because it expects tracked generated files. | Move checks to temporary generation output before untracking generated trees. |
| Generated output drift becomes less visible in PRs. | Require generator and validator evidence for affected skill and release changes. |
| Release process becomes more complex. | Keep the first slice limited to `.codex/skills/`; move public adapters later. |
| Local Codex runtime setup becomes less obvious. | Document `python scripts/build-skills.py` or the accepted replacement command. |
| Token benchmarks lose their current input path. | Update benchmark specs and runners to install generated public adapter output from temp builds or release artifacts. |
| Contributors still hand-edit generated output. | Add ignore rules, docs, and validator messaging that identify generated mirrors as non-source. |

## Open Questions

None currently. The proposal now records the recommended release artifact, CI selector, compatibility window, metadata, README, archive tracking, and drift-check decisions at proposal level. Follow-on specs may refine exact schema fields and validation commands.

## Migration Strategy

### M1: Clarify source boundary

Update governing docs and specs to state that `skills/` is the only authored skill source and generated mirrors are build or release output.

### M2: Stop tracking local Codex mirror

Remove tracked `.codex/skills/`, add `.gitignore` coverage, and keep a script command to regenerate the local mirror.

This is the first implementation slice. It must not remove or untrack public adapter skill copies under `dist/adapters/`.

### M3: Prepare release artifact packaging

Update adapter generation and validation so public adapter packages can be built into a temporary release directory and validated there.

Release artifact preparation should add tracked metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml`, keep or add `dist/adapters/README.md`, publish separate per-adapter archives, and optionally publish a combined archive. Generated archives should be release assets, not committed repository files.

### M4: Convert public adapter skill copies to release artifacts

Stop tracking generated public skill copies under:

```text
dist/adapters/codex/.agents/skills/
dist/adapters/claude/.claude/skills/
dist/adapters/opencode/.opencode/skills/
```

Retain only accepted tracked metadata or instructions, such as a manifest or README, if the follow-on spec keeps those in Git.

### M5: Update release and benchmark evidence

Update release notes, release validation, and token-cost benchmark inputs so generated adapters are validated and measured from temp builds or release artifacts.

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
|---|---|---|---|
| 2026-05-12 | Draft a source-boundary proposal before implementation. | Removing tracked generated output changes compatibility, validation, and release policy. | Direct implementation without spec updates. |
| 2026-05-12 | Recommend `skills/` as the only authored skill source. | The repository already identifies `skills/` as canonical, and duplicated generated trees increase review noise. | Treat generated mirrors as co-equal source. |
| 2026-05-12 | Recommend staged migration with `.codex/skills/` first. | `.codex/skills/` is repository-local generated runtime output, while `dist/adapters/` may be a public install path. | Remove all generated skill copies in one slice. |
| 2026-05-12 | Keep public adapter support in scope. | The problem is duplicate tracked output, not adapter support. | Drop Codex, Claude Code, or opencode adapters. |
| 2026-05-12 | Keep `dist/adapters/manifest.yaml` tracked for now. | It preserves a visible support matrix while duplicate generated skill bodies are reduced. | Move all adapter metadata into release artifacts immediately. |
| 2026-05-12 | Require release artifact reproducibility evidence before public adapter untracking. | Once generated packages are no longer tracked, reviewers need source commit, commands, checksums, and validation evidence. | Publish untracked generated artifacts without durable provenance. |
| 2026-05-12 | Define the first implementation slice as `.codex/skills/` only. | This gives immediate duplicate-tree reduction without changing the public adapter install path. | Combine local mirror cleanup with public adapter release packaging. |
| 2026-05-12 | Do not rewrite Git history. | The migration changes future tracked state; history rewrite would be disruptive and unnecessary. | Remove prior generated skill copies from repository history. |
| 2026-05-12 | Require separate per-adapter release archives and allow an optional combined archive. | Most users install one adapter, while a combined archive is useful for maintainers and mirrors. | Publish only one combined archive or require only ad hoc assets. |
| 2026-05-12 | Run adapter builds conditionally for ordinary PRs and always during release validation. | This preserves reproducibility without forcing unrelated PRs through adapter packaging work. | Build adapters on every PR regardless of changed paths. |
| 2026-05-12 | Track adapter artifact metadata under `docs/reports/adapter-artifacts/releases/<version>.yaml`. | Checksums, source commit, generator command, and validation evidence need a durable tracked location. | Store artifact evidence only in release UI text or commit generated archives. |
| 2026-05-12 | Keep or add `dist/adapters/README.md` as tracked install guidance. | Users need a visible adapter install surface after generated skill bodies leave tracked Git state. | Rely only on root README or release notes. |
| 2026-05-12 | Keep public adapter skill copies tracked for at least one stable release after downloadable artifacts exist. | Users may currently rely on GitHub tree copy-install. | Remove public adapter skill copies in the same release that first publishes artifacts. |
| 2026-05-12 | Do not commit generated adapter archives by default. | Release assets and tracked checksums provide distribution and evidence without binary/generated Git churn. | Commit archives under `dist/`, `release/`, or `docs/`. |
| 2026-05-12 | Replace `.codex/skills/` tracked drift checks with temp-output generation and validation. | Once the local mirror is untracked, tracked-file equality no longer proves the right property. | Keep tests that require tracked `.codex/skills/` files. |
| 2026-05-12 | Accept the proposal after renewed proposal-review. | Owner approved the proposal for downstream spec authoring. | Keep the proposal in draft. |

## Next Artifacts

- `proposal-review`
- `spec`
- `spec-review`
- architecture or ADR update if release packaging or generated-output boundaries need a durable design record
- `plan`
- `plan-review`
- `test-spec`
- implementation
- `code-review`
- `explain-change`
- `verify`
- `pr`

## Follow-on Artifacts

- Renewed proposal-review approved the direction with no material findings.
- [Single Authored Skill Source and Generated Output spec](../../specs/single-authored-skill-source-generated-output.md)

## Readiness

Accepted and handed off to `spec`.
