# Stop Tracking Generated Public Adapter Skill Bodies Review Resolution

## Scope

This record tracks material findings from formal lifecycle reviews for the v0.1.3 generated public adapter skill-body untracking proposal.

Closeout status: closed

## Resolution Entries

### proposal-review-r1

Review closeout: closed

#### PAU-R1

Finding ID: PAU-R1
Disposition: accepted
Owner: proposal author
Owning stage: proposal
Required outcome: Revise the proposal before spec/plan so the v0.1.3 release scope explicitly includes updates to root contributor and workflow guidance affected by retiring tracked public adapter skill bodies, or records why a higher-priority source makes those updates unnecessary.
Rationale: The proposal changes a contributor-facing source/install contract. `CONSTITUTION.md` currently says local Codex users install or copy public Codex adapter output from `dist/adapters/codex/.agents/skills/`, and that public adapter packages under `dist/adapters/` remain tracked generated installable output during the compatibility window. Once `v0.1.3` removes tracked generated skill bodies, downstream spec and implementation need an explicit guidance-update target for `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` or a documented unaffected rationale.
Chosen action: Add root guidance alignment to the proposal. The release scope must audit and update `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `dist/adapters/README.md`, and release notes when their wording would otherwise preserve the old tracked adapter skill-body install contract.
Safe resolution path: Add a proposal section or revise Architecture impact / Goals / Testing to require updating affected root and workflow guidance in the same release slice, including `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` when their current wording would become stale. Then rerun proposal-review.
Validation target: `proposal-review-r2` approves the revised proposal with PAU-R1 closed.
Validation evidence: The proposal now includes `Root guidance alignment`, lists affected surfaces including `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `dist/adapters/README.md`, and release notes, adds root-guidance audit validation, and adds acceptance criteria for updated or explicitly unaffected root guidance. `proposal-review-r2` approved the revised proposal with no material findings.

### proposal-review-r2

No material findings.

### spec-review-r1

Review closeout: closed

#### SGPA-SR1

Finding ID: SGPA-SR1
Disposition: accepted
Owner: spec author
Owning stage: spec
Required outcome: The spec must explicitly define its relationship to earlier approved adapter specs before downstream architecture, planning, or test-spec work relies on it.
Rationale: `specs/multi-agent-adapters-first-public-release.md` defines tracked generated adapter packages under `dist/adapters/<adapter>/` as the public adapter package surface and requires validation to fail when generated packages are missing or stale. The new `v0.1.3` spec instead requires only `dist/adapters/README.md` and `dist/adapters/manifest.yaml` to remain tracked under `dist/adapters/`, with complete adapter packages generated into temporary output and release archives. Both directions can be valid across release phases, but the new spec does not state that it supersedes the prior tracked-package contract for `v0.1.3` and later.
Chosen action: Add a `Relationship to prior adapter specs` section to `specs/stop-tracking-generated-public-adapter-skill-bodies.md`. The section states that, for `v0.1.3` and later, this spec supersedes tracked-package and repository-tree install requirements from prior adapter specs while preserving adapter support, generation, validation, release archives, metadata, checksums, and smoke/release verification obligations. Also add version scope, tracked-surface, validation-replacement, test-spec coverage, and acceptance criteria.
Safe resolution path: Add a section such as `Relationship to prior adapter specs` that says this spec supersedes the tracked-package and repository-tree install requirements from `specs/multi-agent-adapters-first-public-release.md` and the compatibility-window portions of `specs/public-adapter-artifact-migration-examples-concise-skill-release.md` for `v0.1.3` and later, while preserving adapter support, generated output validation, release archive generation, metadata, checksums, and smoke/validation obligations through temporary or release-output artifacts.
Validation target: `spec-review-r2` approves the revised spec with SGPA-SR1 closed.
Validation evidence: The spec now includes `Relationship to prior adapter specs`, version-scope requirements `R0` through `R0b`, tracked-surface requirements `R15a` through `R15d`, validation-replacement requirements `R41a` through `R41g`, test-spec coverage requirements `R62` through `R68`, and acceptance criteria for supersession scope and preserved active obligations. `spec-review-r2` approved the revised spec with no material findings.

### spec-review-r2

No material findings.

### architecture-review-r1

No material findings.

### plan-review-r1

No material findings.

### code-review-m1-r1

Review closeout: closed

#### CR-M1-1

Finding ID: CR-M1-1
Disposition: accepted
Owner: implementer
Owning stage: implement M1
Decision owner: implementer
Decision needed: None; finding accepted.
Required outcome: `release-verify.sh` must support the `v0.1.3` target in the M1 validation model and must delegate to generated release-output/archive validation instead of tracked `dist/adapters/<adapter>/` package validation.
Rationale: M1 changes `validate_release_output()` for v0.1.3, but the maintainer-facing gate still rejects `v0.1.3` before invoking any validation. `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3` exits with `Unsupported release target: v0.1.3`.
Chosen action: Updated `scripts/release-verify.sh` to accept `v0.1.3`, create or use a release-output directory, build adapter release archives for `v0.1.3`, pass `--release-output-dir` and `--release-commit` to `scripts/validate-release.py`, and skip tracked adapter drift/package validation for the retired v0.1.3 repository tree. Added a dry-run regression test for the v0.1.3 archive-only release gate.
Safe resolution path: Update `scripts/release-verify.sh` to accept `v0.1.3`, build or use a release-output directory for v0.1.3 adapter archives, pass `--release-output-dir` and `--release-commit` to `scripts/validate-release.py`, and avoid required tracked `build-adapters.py --check` / `validate-adapters.py --version <adapter-version>` checks for the retired tracked package tree. Add a regression test that exercises `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3` and asserts the required generated-output/archive validation commands are invoked.
Validation target: Rerun targeted release-verify tests, `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3`, and M1 adapter distribution tests before returning to `code-review M1`.
Validation evidence: `python scripts/test-adapter-distribution.py -k release_verify_script_supports_v0_1_3_archive_only_gate` passed; `RELEASE_VERIFY_DRY_RUN=1 RELEASE_OUTPUT_DIR=release-output RELEASE_COMMIT=0123456789abcdef0123456789abcdef01234567 bash scripts/release-verify.sh v0.1.3` passed; `python scripts/test-adapter-distribution.py` passed; `python scripts/validate-skills.py` passed; `python scripts/build-adapters.py --version v0.1.3 --output-dir <tmp>/release-output && python scripts/validate-adapters.py --root <tmp>/release-output --version v0.1.3` passed; `RELEASE_VERIFY_DRY_RUN=1 bash scripts/release-verify.sh v0.1.3` passed with a temporary release-output directory and current HEAD release commit.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

No material findings.

### code-review-m3-r1

Review closeout: closed

#### CR-M3-1

Finding ID: CR-M3-1
Disposition: accepted
Owner: implementer
Owning stage: implement M3
Decision owner: implementer
Decision needed: None; maintainer confirmed manual v0.1.3 adapter smoke passed.
Required outcome: Stable `v0.1.3` smoke rows must be backed by actual maintainer smoke evidence for the installed/generated `v0.1.3` adapters, or the release metadata must stop claiming smoke `pass` until such evidence exists.
Rationale: `docs/releases/v0.1.3/release.yaml` marks Codex, Claude Code, and opencode smoke rows as `pass`, but the evidence strings only cite repository-owned archive validation and tool-version checks. The governing architecture and workflow guidance preserve maintainer smoke evidence for stable releases.
Chosen action: Updated `docs/releases/v0.1.3/release.yaml` smoke evidence to record maintainer manual smoke for the extracted v0.1.3 Codex, Claude Code, and opencode adapter archives.
Safe resolution path: Extract or otherwise install each generated `v0.1.3` adapter archive into a disposable root, run the accepted smoke command/form for Codex, Claude Code, and opencode, and update `docs/releases/v0.1.3/release.yaml` evidence with the actual commands/results. If smoke cannot be run in this slice, change the release metadata and lifecycle state so `v0.1.3` is not release-ready, then record the blocker instead of marking smoke rows `pass`.
Validation target: Rerun `code-review M3` after validating release metadata and review artifacts.
Validation evidence: `python scripts/validate-release.py --version v0.1.3 --release-output-dir /tmp/rigorloop-v013-release-output --release-commit 0f3fe12c8d03d9cb64d9315acc25ac1045c745a8` passed. Review-artifact closeout remains pending same-stage rerun review, as expected after a changes-requested review.

### code-review-m3-r2

Review result: clean-with-notes.

Material findings: none.

Closeout: no review-resolution action required; M3 can close and hand off to M4.

### code-review-m4-r1

Review result: clean-with-notes.

Material findings: none.

Closeout: no review-resolution action required; all implementation milestones are closed and final closeout can start with explain-change.
