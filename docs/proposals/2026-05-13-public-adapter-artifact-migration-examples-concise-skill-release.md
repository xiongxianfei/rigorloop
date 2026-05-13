# Public Adapter Artifact Migration, Examples Relocation, and Concise Skill Release

## Status

accepted

## Problem

RigorLoop has been moving toward a single authored skill source under `skills/`, but the next release still needs to complete several connected cleanup steps without breaking public adapter users.

Generated public adapter skill bodies remain tracked under `dist/adapters/`, which makes generated text look like ordinary authored source and keeps skill edits noisy. The retained skill-validator proof pack still lives under `docs/changes/0001-skill-validator/`, where it can look like active lifecycle state even though it functions as an example, fixture, and historical proof pack. Public stage skills also still carry more duplicated artifact-location guidance than they should now that `docs/workflows.md` is the project-local artifact-location guide.

The latest GitHub release on 2026-05-13 is `v0.1.1`, published from `6a38239`. Its release notes keep `dist/adapters/` as the public adapter install path for that release and explicitly state that no downloadable adapter archives were introduced. The accepted source-boundary direction also requires a stable public compatibility window after downloadable adapter artifacts and install docs are available. The next release therefore should introduce adapter archives first while retaining tracked adapter skill bodies, then remove those tracked bodies in a later stable release unless the compatibility policy is explicitly amended.

## Goals

- Introduce downloadable public adapter archives before removing tracked public adapter skill bodies.
- Stop tracking generated public adapter skill bodies under `dist/adapters/**/skills` only after at least one stable release has shipped downloadable archives and install docs, unless a later accepted decision amends the compatibility policy.
- Keep `skills/` as the only authored skill source.
- Keep small tracked adapter metadata and install guidance such as `dist/adapters/manifest.yaml` and `dist/adapters/README.md`.
- Publish generated adapter packages as downloadable release artifacts.
- Record release artifact metadata, including source commit, generator command, checksums, validation command, and result.
- Move `docs/changes/0001-skill-validator/` to `docs/examples/changes/skill-validator/` only if references, tests, validators, selectors, docs, and release guidance can be updated safely in the same implementation slice; otherwise retain it with explicit fixture rationale and schedule a follow-up.
- Make `docs/workflows.md` the project artifact-location guide for common artifact locations and owning skills.
- Update `workflow` so it owns creation and refresh of the artifact-location guide.
- Simplify public stage skills so they use the project artifact-location guide instead of carrying long duplicated path rules.
- Reduce public skill token cost where safe and measure static and dynamic token cost after the cleanup.
- Publish the next release with release evidence.

## Non-goals

- Do not change workflow stage order.
- Do not change skill behavior unrelated to artifact placement, adapter packaging, install guidance, or token-friendly wording.
- Do not remove support for Codex, Claude Code, or opencode.
- Do not rewrite Git history to remove previously tracked generated skill copies.
- Do not hand-edit generated adapter output as source.
- Do not move examples unless references, selectors, validators, and docs can be updated in the same implementation slice.
- Do not make `docs/workflows.md` override `CONSTITUTION.md`, approved specs, schemas, governance, or active artifact metadata.
- Do not delete safety-critical review, verification, material-finding, or release guidance solely to reduce tokens.
- Do not publish until release validation, adapter validation, token-cost evidence, and release notes are complete.

## Vision fit

fits the current vision

This proposal strengthens RigorLoop as a rigorous AI coding-agent workflow by making source ownership clear, artifact placement discoverable, examples non-normative, public skills concise, generated output reproducible, and release quality measurable.

## Context

`CONSTITUTION.md` says `skills/` is the only authored skill source and that public adapter packages under `dist/adapters/` remain tracked generated installable output during the compatibility window. The accepted single-authored-source proposal points to the next steady state: canonical skill source under `skills/`, small tracked adapter metadata, and generated adapter packages distributed through release artifacts after packaging and install docs are ready.

The accepted artifact-location proposal makes `docs/workflows.md` the project-local artifact-location guide and keeps examples under `docs/examples/`. It also treats `docs/changes/0001-skill-validator/` as a retained validator fixture and historical proof pack that can move only when references can be updated safely.

The accepted progressive-loading proposal identifies `workflow`, `implement`, and `code-review` as high-cost public skill surfaces and calls for shorter, progressively loadable guidance without weakening review, validation, material-finding, or handoff safety rules.

The `v0.1.1` GitHub release is the current latest release as of 2026-05-13. It preserves the repository-tree adapter install model for `v0.1.1` and does not ship downloadable adapter archives, so this proposal treats `v0.1.2` as the likely archive-introduction release and `v0.1.3` as the earliest likely tracked-adapter-skill-body removal release unless a newer stable version is published, reserved, or policy-amended before planning.

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Do not track skills under `dist/`. | in scope after compatibility window | Goals; Recommended direction |
| Move `docs/changes/0001-skill-validator/` to `docs/examples/`. | in scope, conditional | Goals; Examples migration |
| Let `workflow` and `docs/workflows.md` own artifact-location guidance. | in scope | Goals; Artifact-location guide ownership |
| Optimize current skills to be simple and concise. | in scope | Goals; Skill simplification |
| Reduce token cost. | in scope | Goals; Token-cost measurement |
| Measure token cost. | in scope | Goals; Testing and verification strategy |
| Publish a new version. | in scope | Goals; Rollout and rollback |
| Preserve adapter support. | in scope | Goals; Non-goals; Adapter artifacts |
| Avoid breaking users. | in scope | Non-goals; Rollout and rollback; Risks and mitigations |

## Options considered

### Option 1: Keep tracking `dist/adapters/**/skills`

This preserves the `v0.1.1` repository-tree install model.

Advantages:

- Users can keep copying adapter packages directly from the repository tree.
- Existing drift checks remain close to the current model.
- The immediate release change is smaller.

Disadvantages:

- Skill edits keep producing duplicated generated diffs.
- Generated output still looks like authored content.
- Token-cost and review workflows still see repeated skill copies.
- This does not complete the single-authored-source migration.

### Option 2: Stop tracking `dist/adapters/**/skills` immediately without release artifacts

This produces the cleanest source tree immediately.

Advantages:

- Generated duplication is removed quickly.
- `skills/` becomes visibly authoritative.

Disadvantages:

- It breaks the current public adapter install path.
- It conflicts with the `v0.1.1` install model.
- Users receive no replacement distribution surface.

### Option 3: Publish adapter archives, keep one stable compatibility release, then stop tracking `dist/adapters/**/skills`

This introduces the new distribution surface first, then completes the source cleanup after users have a stable release where both install paths are documented.

Advantages:

- Completes the single-authored-source direction.
- Preserves public adapter installation through downloadable release artifacts.
- Keeps generated output reproducible through metadata, checksums, and validation.
- Reduces tracked duplicate skill text.
- Lets `dist/adapters/` retain only manifest and install guidance.
- Preserves the accepted compatibility window.

Disadvantages:

- Requires release artifact generation and metadata.
- Requires validator, selector, release script, and release-doc updates.
- Requires users to switch from repository-tree adapter copying to release-archive installation.
- Takes at least two stable releases to complete the tracked-output cleanup.

## Recommended direction

Choose Option 3.

Publish the next release as the public adapter archive introduction release. Use `v0.1.2` unless a newer stable version is already published or reserved during planning.

Use a two-release compatibility sequence:

```text
v0.1.2:
  publish downloadable adapter archives
  keep dist/adapters/**/skills tracked
  update install docs and release notes
  record artifact metadata and checksums
  validate both tracked adapter packages and generated archives where required

v0.1.3 or later:
  stop tracking dist/adapters/**/skills
  keep dist/adapters/manifest.yaml and dist/adapters/README.md
  require release-archive install path
```

If maintainers decide `v0.1.2` should also remove tracked adapter skill bodies, the proposal, spec, and release notes must explicitly state that the accepted compatibility window is being shortened and explain why the risk is acceptable.

Use this steady-state model:

```text
Authored source:
  skills/

Tracked adapter metadata:
  dist/adapters/manifest.yaml
  dist/adapters/README.md

Generated adapter packages:
  release artifacts

Examples:
  docs/examples/

Artifact locations:
  docs/workflows.md
```

Generated skill bodies under these paths should no longer be tracked after the compatibility window closes:

```text
dist/adapters/codex/.agents/skills/
dist/adapters/claude/.claude/skills/
dist/adapters/opencode/.opencode/skills/
```

The release should publish separate downloadable archives:

```text
rigorloop-adapter-codex-v0.1.2.zip
rigorloop-adapter-claude-v0.1.2.zip
rigorloop-adapter-opencode-v0.1.2.zip
```

A combined maintainer or mirror archive may also be published:

```text
rigorloop-adapters-v0.1.2.tar.gz
```

## Release-critical scope

For `v0.1.2`, release-critical work is:

- adapter archive generation;
- adapter artifact metadata and checksums;
- install docs for release archives;
- release validation against archives;
- token-cost release report;
- release notes.

The following work may be included in `v0.1.2` only if it does not block release readiness:

- moving `docs/changes/0001-skill-validator/`;
- broad public skill simplification beyond artifact-location lookup wording;
- additional progressive-loading optimization.

If archive generation is not ready, do not untrack adapter skill bodies. If the example move breaks validators, retain it with rationale and defer the move. If skill simplification grows, keep only artifact-location lookup wording in the release slice.

## Adapter artifacts

Track release artifact metadata at:

```text
docs/reports/adapter-artifacts/releases/v0.1.2.yaml
```

The metadata schema should be exact before implementation so release validation can enforce it. The initial schema should be:

```yaml
schema_version: 1

release:
  version: v0.1.2
  source_commit: "<sha>"
  date: "YYYY-MM-DD"

generator:
  command: "python scripts/build-adapters.py --version v0.1.2 --output-dir <release-output-dir>"
  source_skills: "skills/"
  manifest: "dist/adapters/manifest.yaml"

artifacts:
  - adapter: codex
    archive: "rigorloop-adapter-codex-v0.1.2.zip"
    sha256: "<sha256>"
    install_root: ".agents/skills/"
    result: pass
  - adapter: claude
    archive: "rigorloop-adapter-claude-v0.1.2.zip"
    sha256: "<sha256>"
    install_root: ".claude/skills/"
    result: pass
  - adapter: opencode
    archive: "rigorloop-adapter-opencode-v0.1.2.zip"
    sha256: "<sha256>"
    install_root: ".opencode/skills/"
    result: pass

combined_artifact:
  required: false
  archive: "rigorloop-adapters-v0.1.2.tar.gz"
  sha256: "<sha256>"
  included_adapters:
    - codex
    - claude
    - opencode

validation:
  command: "python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.2"
  result: pass
  validated_at: "YYYY-MM-DD"
```

Per-adapter archives are required. The combined archive is optional unless a later accepted spec makes it release-required.

Do not commit the archive files. Generate them in CI or the release workflow, attach them to the GitHub release, and track checksums and metadata.

Keep `dist/adapters/README.md` and `dist/adapters/manifest.yaml` tracked.

`dist/adapters/README.md` becomes the repository-tree adapter install-contract surface. It should state:

- `skills/` is the canonical authored source;
- `dist/adapters/manifest.yaml` is the adapter support matrix;
- `v0.1.2` introduces release archives while keeping tracked adapter skill bodies for the compatibility window;
- generated adapter skill bodies are not tracked source after the later migration release;
- users should install from release archives once the archive install path is active;
- per-adapter archive names;
- target install roots for Codex, Claude Code, and opencode;
- where to find checksums and artifact metadata.

The README should describe the active install path for each release phase and avoid stale defensive wording about internal local runtime paths.

## Examples migration

Move, if safe:

```text
docs/changes/0001-skill-validator/
```

to:

```text
docs/examples/changes/skill-validator/
```

Update references in tests, validators, selector routing, `docs/workflows.md`, README or contributor docs, and release notes when applicable. `docs/examples/README.md` should continue to state that examples are non-normative and not active lifecycle state.

Acceptance may be either:

```text
moved with references updated
```

or:

```text
retained with explicit fixture rationale and scheduled follow-up
```

## Artifact-location guide ownership

`docs/workflows.md` should own the project artifact-location map. It should answer where proposals, specs, plans, change roots, reviews, examples, reports, adapter metadata, and release artifact metadata live.

The map defines default locations and owning skills, not exact schemas. Specs, schemas, and references continue to own exact artifact shapes and validation rules.

Stage skills should use this lookup order when artifact placement matters:

```text
1. explicit user path or change ID
2. active plan, change metadata, reviewed artifact, or current artifact metadata
3. known governing spec or schema constraint when directly relevant
4. docs/workflows.md artifact-location table
5. the skill's portable default path
6. block on ambiguity
```

This keeps skills concise and avoids broad authoritative-document searches only to discover artifact paths.

## Skill simplification

For this release migration, skill simplification is limited to:

- replacing duplicated path guidance with concise project-guide lookup wording;
- preserving each skill's portable default path;
- removing obsolete generated-output references.

Progressive-loading optimization for `workflow`, `implement`, and `code-review` remains governed by the accepted progressive-loading proposal and should run as a separate implementation slice unless the plan explicitly sequences it after release packaging readiness.

Update public skills to rely on the project artifact-location guide instead of carrying long duplicated path sections.

Priority skills:

```text
workflow
proposal
spec
architecture
plan
proposal-review
spec-review
architecture-review
plan-review
code-review
explain-change
verify
pr
```

The minimum release-slice change is to add or preserve concise artifact-location lookup wording, remove duplicated long path tables, and keep each skill's short portable default path. Do not remove safety-critical behavior.

## Token-cost measurement

Before implementation, record the baseline from:

```text
docs/reports/token-cost/releases/v0.1.1.md
```

After implementation, create:

```text
docs/reports/token-cost/releases/v0.1.2.md
docs/reports/token-cost/releases/v0.1.2.yaml
```

Measure static skill token cost from canonical `skills/`, dynamic benchmark runtime cost, adapter artifact packaging impact, whole-skill reads, largest command-output events, and result quality. Dynamic Codex benchmarks should use public adapter release output or generated temporary public adapter output, not `.codex/skills/`.

## Expected behavior changes

Before this migration, users install adapters by copying tracked `dist/adapters/<adapter>/` directories from the repository tree. In `v0.1.2`, users can install adapters from downloadable release archives while tracked `dist/adapters/**/skills` remain available for compatibility. In `v0.1.3` or later, users install adapters from release archives and tracked generated adapter skill bodies are removed.

Before this migration, `dist/adapters/` contains generated skill bodies. During the compatibility release, `dist/adapters/` still contains those generated skill bodies while release archives become available. After the later untracking release, `dist/adapters/` contains metadata and install guidance; generated skill bodies are release artifacts.

Before this migration, `docs/changes/0001-skill-validator/` looks like an active change root. After the optional example migration, `docs/examples/changes/skill-validator/` is clearly non-normative example and fixture content. If the move is unsafe in the release slice, the old path remains with durable retained-fixture rationale.

Before this migration, public skills carry repeated path guidance. After this migration, `docs/workflows.md` is the project artifact-location map.

## Architecture impact

No runtime architecture change is expected. This is a repository packaging, release, validation, artifact-location, and skill-surface cleanup.

Affected surfaces may include:

```text
dist/adapters/
docs/reports/adapter-artifacts/releases/
docs/reports/token-cost/releases/
docs/examples/
docs/workflows.md
skills/workflow/SKILL.md
selected stage skills
scripts/build-adapters.py
scripts/validate-adapters.py
scripts/release-verify.sh
scripts/validate-release.py
scripts/test-adapter-distribution.py
selector routing
lifecycle validation
release notes
```

Architecture may be required if planning shows that archive generation, release metadata, validation flow, or install contract changes need a durable design record before implementation.

## Testing and verification strategy

Likely validation commands include:

```bash
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/measure-skill-tokens.py
python scripts/build-adapters.py --version v0.1.2 --output-dir <release-output-dir>
python scripts/validate-adapters.py --root <release-output-dir> --version v0.1.2
python scripts/test-adapter-distribution.py
python scripts/validate-token-cost-report.py docs/reports/token-cost/releases/v0.1.2.yaml
python scripts/select-validation.py --mode explicit --path docs/examples/changes/skill-validator/change.yaml  # when moved
bash scripts/release-verify.sh v0.1.2
git diff --check --
```

If scripts do not yet support release output directories, archive generation, checksum metadata, or the moved skill-validator path, implementation should add that support before relying on those surfaces.

`bash scripts/release-verify.sh <version>` is the maintainer-facing final release gate. `scripts/validate-release.py` owns structured release metadata validation and is delegated from `release-verify.sh`.

`v0.1.2` release validation should prove canonical skills validate, adapter archives are generated and validate, artifact checksums are recorded, token-cost reports validate, `docs/workflows.md` has a current artifact-location guide, tracked adapter skill bodies remain available for the compatibility window, and release notes explain the new archive install path.

The later untracking release validation should additionally prove `dist/adapters/` contains only accepted tracked metadata and guidance, not generated skill bodies.

## Rollout and rollback

Roll out in staged slices:

- `v0.1.2`: add adapter archive generation, metadata, checksums, validation, install docs, token-cost evidence, and release notes while keeping `dist/adapters/**/skills` tracked.
- `v0.1.2` optional: move the skill-validator proof pack to `docs/examples/changes/skill-validator/` and update all path references in the same slice, or retain it with rationale.
- `v0.1.2` optional: refresh `docs/workflows.md` and simplify stage-skill artifact-location wording when the edits stay bounded.
- `v0.1.3` or later: remove tracked generated public adapter skill bodies after the compatibility window, while keeping manifest and README.

If adapter archives are not ready, keep the `v0.1.1` install model and defer archive migration.

If moving the skill-validator proof pack breaks validators, restore the old path, add retained-fixture rationale, and schedule a narrower fixture-migration follow-up.

If skill simplification weakens behavior, restore the previous safety wording and keep only the valid `docs/workflows.md` artifact map changes.

If token-cost benchmarks regress, publish only when result quality remains valid and the regression is explained, or block release if the release policy requires it.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Users lose the repository-tree adapter install path. | Ship one stable release with both tracked adapter skill bodies and release archives before untracking generated skill bodies. |
| Archive generation is not ready. | Defer archive migration and keep the `v0.1.1` install model. |
| Tests, selectors, or validators depend on the old skill-validator path. | Update all references in the same implementation slice as the move, or retain the old path with rationale and follow-up. |
| Skills become too vague after simplification. | Keep a portable default path in each skill and block on ambiguity. |
| `docs/workflows.md` becomes too large. | Keep the artifact-location table concise and leave exact shapes to specs and schemas. |
| Token-cost work grows too broad. | Measure canonical skills and the targeted dynamic suite needed for release evidence. |
| Release scope becomes too large. | Stage implementation and stop if archive migration is not ready. |

## Open questions

- Should maintainers intentionally shorten the compatibility window, or use the proposed `v0.1.2` archive introduction and `v0.1.3` untracking sequence?
- Should `v0.1.2` be the final version target if another release is published before planning completes?
- Which skills beyond the priority list need simplification in this release rather than a follow-up?
- Does archive generation require an architecture artifact, or is a spec plus plan sufficient?

The compatibility-window question must be resolved before acceptance if maintainers reject the two-release sequence. The remaining questions can be settled before or during spec and architecture planning.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-13 | Propose `v0.1.2` as the archive-introduction release and `v0.1.3` or later as the first untracking release. | `v0.1.1` kept `dist/adapters/` as the install path and shipped no downloadable adapter archives; the accepted direction needs a stable compatibility window. | Introduce archives and remove tracked adapter skill bodies in the same release. |
| 2026-05-13 | Remove tracked generated adapter skill bodies only after a stable archive release is available, unless policy is amended. | This avoids breaking adapter users and preserves the compatibility window. | Immediate untracking without an overlap release. |
| 2026-05-13 | Move the skill-validator proof pack to `docs/examples/` only if references can be updated safely in the same slice. | Examples and fixtures should not look like active lifecycle state, but validator stability should not block archive publication. | Make the move a hard release blocker. |
| 2026-05-13 | Let `docs/workflows.md` own artifact locations. | This keeps skills concise and reduces path-search token waste. | Duplicate path tables in every public skill. |
| 2026-05-13 | Measure token cost before publishing. | Release quality should remain evidence-based. | Publish without updated token-cost evidence. |

## Next artifacts

```text
spec-review
architecture if packaging design needs it
plan
plan-review
test-spec
implement
code-review
explain-change
verify
pr
release
```

## Follow-on artifacts

- Proposal review: `docs/changes/2026-05-13-public-adapter-artifact-migration-examples-concise-skill-release/reviews/proposal-review-r1.md`
- Spec: `specs/public-adapter-artifact-migration-examples-concise-skill-release.md`

## Readiness

Accepted after clean proposal-review. Follow-on spec drafted; see Follow-on artifacts for review evidence and downstream contract.

## Core invariant

```text
Author skills once.
Publish generated adapters as release artifacts before removing the old public install path.
Keep examples under docs/examples.
Let docs/workflows.md answer where artifacts go.
Keep public skills concise and measurable.
```

## References

- GitHub release context: <https://github.com/xiongxianfei/rigorloop/releases>
- Accepted related proposal: `docs/proposals/2026-05-12-single-authored-skill-source-and-generated-adapter-output-cleanup.md`
- Accepted related proposal: `docs/proposals/2026-05-13-project-artifact-location-guide-and-examples-surface.md`
- Accepted related proposal: `docs/proposals/2026-05-11-progressive-loading-for-high-cost-public-skills.md`
