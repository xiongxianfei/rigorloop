# Multi-adapter init and proxy-aware adapter download

- Status: active
- Owner: maintainer
- Start date: 2026-05-18
- Last updated: 2026-05-18
- Related issue or PR: none yet
- Supersedes: none

## Purpose / big picture

Implement the approved CLI contract for `rigorloop init --adapter codex|claude|opencode` while preserving Codex `.agents/skills`, verified release-archive installation, local archive fallback, lockfile integrity, and proxy-safe diagnostics.

This plan turns the approved spec and architecture into reviewable implementation slices. It does not change the product contract; implementation must stay inside the behavior already approved by the proposal, spec, architecture package, and ADR.

## Source artifacts

- Proposal: `docs/proposals/2026-05-18-multi-adapter-init-and-proxy-aware-download.md`
- Spec: `specs/multi-adapter-init-and-proxy-aware-download.md`
- Spec review evidence: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/spec-review-r2.md`, `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/spec-review-r3.md`
- Architecture: `docs/architecture/system/architecture.md`
- ADR: `docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md`
- Architecture review evidence: `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/architecture-review-r1.md`
- Test spec: `specs/multi-adapter-init-and-proxy-aware-download.test.md`

## Context and orientation

- CLI package: `packages/rigorloop`
- CLI entrypoint: `packages/rigorloop/dist/bin/rigorloop.js`
- Existing lockfile parser/serializer: `packages/rigorloop/dist/lib/lockfile.js`
- Official URL helper: `packages/rigorloop/dist/lib/official-archive-url.js`
- Bundled metadata: `packages/rigorloop/dist/metadata/releases.json`, `packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.5.json`
- CLI regression tests and fixture helpers: `packages/rigorloop/test/cli.test.js`
- Adapter generation and validation scripts: `scripts/build-adapters.py`, `scripts/validate-adapters.py`
- Existing package tests run with `npm test --prefix packages/rigorloop`.

The current CLI implementation is Codex-specific: it uses `ADAPTER = "codex"`, `INSTALL_ROOT = ".agents/skills"`, schema v1 lockfile serialization, Codex-only metadata lookup, and Codex-only fixture helpers. The implementation should introduce explicit descriptors and multi-root lockfile support without making runtime roots or downstream lockfiles canonical sources.

## Non-goals

- No Codex migration to `.codex/skills`.
- No `rigorloop status`, `rigorloop validate`, workflow YAML, or generated workflow docs.
- No npm-bundled adapter archives.
- No user-supplied metadata option.
- No programmatic Undici proxy dispatcher support.
- No lockfile repair command.
- No adapter archive packaging redesign beyond metadata/output needed for this contract.
- No live GitHub or live proxy dependency in normal tests.

## Requirements covered

- Command surface and adapter names: MAI-R1 through MAI-R6.
- Adapter descriptors and install roots: MAI-R7 through MAI-R16.
- Trusted metadata and archive acquisition: MAI-R17 through MAI-R28.
- Archive verification and extraction safety: MAI-R29 through MAI-R38.
- opencode command aliases and older skills-only archives: MAI-R39 through MAI-R46c.
- `rigorloop.yaml`: MAI-R47 through MAI-R54.
- `rigorloop.lock` schema v2: MAI-R55 through MAI-R76.
- Proxy-aware network behavior: MAI-R77 through MAI-R85.
- JSON and human output: MAI-R86 through MAI-R91.
- Generated adapter validation: MAI-R92 through MAI-R95.
- Acceptance criteria: AC1 through AC16.

## Current Handoff Summary

- Current milestone: M4. Network download diagnostics and output envelope
- Current milestone state: resolution-needed
- Last reviewed milestone: M3. Multi-root archive extraction and local archive fallback
- Review status: M4 code-review completed with `CR-M4-R1-F1`; review-resolution required
- Remaining in-scope implementation milestones: M4, M5
- Next stage: review-resolution for M4
- Final closeout readiness: not ready
- Reason final closeout is or is not ready: all implementation milestones, code-review, review-resolution if triggered, explain-change, verify, and PR handoff remain incomplete.

## Milestones

### M1. Adapter descriptors and trusted metadata selection

- Milestone state: closed
- Goal: Replace Codex-only selection with a descriptor registry for `codex`, `claude`, and `opencode`, including package-compatible metadata lookup and official archive URL selection.
- Requirements: MAI-R1 through MAI-R28, AC1, AC2, AC3, AC5, AC6, AC7.
- Files/components likely touched: `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/dist/lib/official-archive-url.js`, `packages/rigorloop/dist/metadata/*.json`, `packages/rigorloop/test/cli.test.js`.
- Dependencies: approved spec and architecture; test-spec must define exact test IDs before implementation.
- Tests to add/update: descriptor selection for all three adapters; unsupported adapter blocker; wrong archive selected adapter rejection; official URL helper coverage for each archive; metadata-unavailable and release-incompatible cases.
- Implementation steps: introduce adapter descriptor data; generalize release/archive naming; generalize metadata artifact lookup by adapter; update help text; keep Codex path `.agents/skills`.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/official-archive-url.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.5.json --path packages/rigorloop/test/cli.test.js`
- Expected observable result: `--adapter codex`, `--adapter claude`, and `--adapter opencode` select the correct descriptor and trusted metadata; unsupported adapter names still block with exit code `2`.
- Commit message: `M1: add descriptor-based adapter selection`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: metadata fixture shape may lag release metadata shape.
- Rollback/recovery: keep Codex descriptor as the compatibility baseline and revert descriptor support for non-Codex adapters if metadata selection cannot be made deterministic.

### M2. Manifest and lockfile schema v2

- Milestone state: closed
- Goal: Implement `rigorloop.yaml` single-root and multi-root serialization plus `rigorloop.lock` schema v2 parsing, serialization, sorting, and schema v1 Codex compatibility.
- Requirements: MAI-R47 through MAI-R76, AC9, AC10, AC11, AC12, AC13.
- Files/components likely touched: `packages/rigorloop/dist/lib/lockfile.js`, `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/test/cli.test.js`.
- Dependencies: M1 descriptors define root roles and adapter identity.
- Tests to add/update: valid v2 single-root and multi-root parse/serialize; v1 Codex parse; v1 to v2 upgrade after drift check; drifted v1 blocks before unrelated adapter mutation; unknown fields block; adapter entries sorted by name; local archive basename only.
- Implementation steps: extend strict parser for schema v2; add multi-root adapter entry validation; preserve v1 Codex support; add serializer for mixed adapter entries; update manifest writer to preserve unrelated valid entries and block malformed/duplicate selected entries.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js`
- Expected observable result: successful installs can write schema v2 lockfiles with Codex/Claude single-root entries and opencode multi-root entries; invalid or drifted existing state blocks before mutation.
- Commit message: `M2: add manifest and lockfile schema v2 support`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: ad hoc YAML parsing can become brittle as nested fields increase.
- Rollback/recovery: keep parser strict and test-driven; if nested parsing cannot remain safe, stop and route an architecture/spec revision for a structured parser decision.

### M3. Multi-root archive extraction and local archive fallback

- Milestone state: closed
- Goal: Generalize archive verification, path safety, extraction, installed tree hashing, and local archive mode across all supported adapters and opencode root combinations.
- Requirements: MAI-R17 through MAI-R46c, MAI-R92 through MAI-R95, AC4, AC7, AC8, AC16.
- Files/components likely touched: `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/dist/metadata/*.json`, `packages/rigorloop/test/cli.test.js`, adapter validation fixtures if needed.
- Dependencies: M1 descriptors and M2 lockfile root serialization.
- Tests to add/update: Claude local archive install; opencode skills plus commands install; missing declared command alias fails; older skills-only opencode install emits `opencode-command-aliases-not-declared`; path traversal and symlink rejection for each root class; installed per-root tree hashes.
- Implementation steps: generalize expected-root filtering; compute tree hash per root role; require declared aliases for new opencode metadata; allow metadata-declared older skills-only opencode ranges; update fixture archive helpers to create `.claude`, `.opencode/skills`, and `.opencode/commands` archives.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/build-adapters.py --version 0.1.5 --output-dir /tmp/rigorloop-adapter-plan-check`
  - `python scripts/validate-adapters.py --version 0.1.5 --root /tmp/rigorloop-adapter-plan-check`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.5.json --path packages/rigorloop/test/cli.test.js --path scripts/build-adapters.py --path scripts/validate-adapters.py`
- Expected observable result: local archive fallback works for all supported adapters; opencode commands are installed only when declared and verified; generated adapter validation evidence exists when adapter output or metadata changes.
- Commit message: `M3: verify and install multi-root adapter archives`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: generated adapter metadata may not yet expose per-root hashes for opencode commands.
- Rollback/recovery: stop before claiming opencode support and route a metadata generation spec/architecture update if per-root hash evidence is unavailable.

### M4. Network download diagnostics and output envelope

- Milestone state: resolution-needed
- Goal: Add hermetic network-download tests and proxy-safe failure diagnostics without adding programmatic Undici dispatcher support.
- Requirements: MAI-R77 through MAI-R91, AC14, AC15.
- Files/components likely touched: `packages/rigorloop/dist/bin/rigorloop.js`, `packages/rigorloop/test/cli.test.js`.
- Dependencies: M1 metadata URL selection and M3 archive acquisition paths.
- Tests to add/update: mocked fetch success for each adapter; mocked DNS/TLS/timeout/http/proxy/network/unknown failures as feasible; safe proxy env var names only; `node_env_proxy_status` enum; trusted `archive_url`; fallback guidance; no raw proxy values in JSON or human output; dry-run JSON no mutation for all adapters.
- Implementation steps: classify fetch failures; detect allowlisted proxy env var names; determine or report `node_env_proxy_status`; preserve official URL validation; ensure network failures before verification return blocked exit code `2`.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js`
- Expected observable result: network download failures include bounded diagnostics and `--from-archive` guidance without exposing credentials, raw proxy URLs, private hostnames, or raw env values.
- Commit message: `M4: add proxy-safe download diagnostics`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: Node env-proxy status detection can be runtime-version dependent.
- Rollback/recovery: use `unknown` when status cannot be determined without guessing; keep local archive fallback guidance as the reliable path.

### M5. Documentation, package proof, and final integration

- Milestone state: planned
- Goal: Align package docs, change metadata, and final validation evidence with the implemented multi-adapter contract.
- Requirements: all requirements; AC1 through AC16.
- Files/components likely touched: `packages/rigorloop/README.md`, `packages/rigorloop/package.json` only if needed, `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`, active plan validation notes, possibly release evidence if the implementation changes release metadata surfaces.
- Dependencies: M1 through M4 closed or explicitly revised out of scope.
- Tests to add/update: no new behavior tests unless final integration finds gaps; update package-level documentation assertions if present.
- Implementation steps: update package README/help examples for all adapters; record validation evidence; run selected CI for all touched implementation and lifecycle paths; prepare handoff to final code-review.
- Validation commands:
  - `npm test --prefix packages/rigorloop`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/multi-adapter-init-and-proxy-aware-download.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md --path docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md --path docs/plan.md --path docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
  - `bash scripts/ci.sh --mode explicit --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/dist/lib/official-archive-url.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.5.json --path packages/rigorloop/dist/metadata/releases.json --path packages/rigorloop/test/cli.test.js --path packages/rigorloop/README.md --path docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md --path docs/plan.md --path docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- Expected observable result: package docs and lifecycle evidence match the implemented contract, and the initiative is ready for code-review of the final implementation slice.
- Commit message: `M5: align docs and validation evidence for multi-adapter init`
- Milestone closeout:
  - validation passed
  - progress updated
  - decision log updated if needed
  - validation notes updated
  - milestone committed
- Risks: final selected CI may expose stale lifecycle or generated-output routing debt.
- Rollback/recovery: fix stale lifecycle artifacts in the same implementation branch when they are touched or authoritative; record unrelated stale baseline debt as a follow-up only when allowed by verification rules.

## Validation plan

Plan-stage validation:

- `python scripts/validate-change-metadata.py docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/multi-adapter-init-and-proxy-aware-download.md --path docs/architecture/system/architecture.md --path docs/adr/ADR-20260518-multi-adapter-init-and-proxy-download.md --path docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md --path docs/plan.md --path docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- `git diff --check -- docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md docs/plan.md docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`
- `bash scripts/ci.sh --mode explicit --path docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md --path docs/plan.md --path docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml`

Implementation-stage validation is listed inside each milestone. Final verification must use the active test spec once it exists and must name the exact commands run.

## Risks and recovery

- Descriptor migration risk: keep Codex as a descriptor-backed compatibility baseline and preserve `.agents/skills`.
- Lockfile schema risk: maintain strict parsing, v1 Codex compatibility, and no unknown-field preservation.
- opencode multi-root risk: fail when declared command aliases are missing; warn only for explicitly compatible older skills-only metadata.
- Proxy diagnostic privacy risk: report only allowlisted env var names and stable enums; never print raw proxy values or request headers.
- Partial mutation risk: plan all writes before mutation, write lockfile only after verified install, and keep failure output clear about changed artifacts.
- Test hermeticity risk: use mocked fetch, fixture archives, and local temp projects; do not rely on live GitHub or a live proxy.

## Dependencies

- `plan-review` must approve this plan before implementation.
- `test-spec` must map every spec MUST and milestone edge case to concrete tests before implementation.
- M2 depends on M1 descriptors.
- M3 depends on M1 descriptors and M2 lockfile root serialization.
- M4 depends on M1 metadata URL selection and M3 acquisition paths.
- M5 depends on implementation milestones being closed or formally revised.

## Progress

- [x] 2026-05-18: proposal accepted, spec approved, architecture package approved, and ADR accepted.
- [x] 2026-05-18: execution plan created.
- [x] 2026-05-18: plan-review completed with no material findings.
- [x] 2026-05-18: test-spec created and approved by user.
- [x] 2026-05-18: M1 implementation started.
- [x] 2026-05-18: M1 tests and implementation completed; handoff requested for code-review.
- [x] 2026-05-18: M1 code-review completed with no material findings.
- [x] M1 closed.
- [x] 2026-05-18: M2 implementation started.
- [x] 2026-05-18: M2 tests and implementation completed; handoff requested for code-review.
- [x] 2026-05-18: M2 code-review completed with `CR-M2-R1-F1`; review-resolution required.
- [x] 2026-05-18: M2 review-resolution completed for `CR-M2-R1-F1`; handoff requested for code-review rerun.
- [x] 2026-05-18: M2 code-review rerun completed with `CR-M2-R2-F1`; review-resolution required.
- [x] 2026-05-18: M2 review-resolution completed for `CR-M2-R2-F1`; handoff requested for code-review rerun.
- [x] 2026-05-18: M2 code-review rerun completed with no material findings.
- [x] M2 closed.
- [x] 2026-05-18: M3 implementation started.
- [x] 2026-05-18: M3 tests and implementation completed; handoff requested for code-review.
- [x] 2026-05-18: M3 code-review completed with `CR-M3-R1-F1`; review-resolution required.
- [x] 2026-05-18: M3 review-resolution completed for `CR-M3-R1-F1`; handoff requested for code-review rerun.
- [x] 2026-05-18: M3 code-review rerun completed with `CR-M3-R2-F1`; review-resolution required.
- [x] 2026-05-18: M3 review-resolution completed for `CR-M3-R2-F1`; handoff requested for code-review rerun.
- [x] 2026-05-18: M3 code-review rerun completed with no material findings.
- [x] M3 closed.
- [x] 2026-05-18: M4 implementation started.
- [x] 2026-05-18: M4 tests and implementation completed; handoff requested for code-review.
- [x] 2026-05-18: M4 code-review completed with `CR-M4-R1-F1`; review-resolution required.
- [ ] M4 closed.
- [ ] M5 closed.
- [ ] final code-review, explain-change, verify, and PR handoff completed.

## Decision log

- 2026-05-18: Use five implementation milestones so descriptor selection, lockfile schema, extraction/local archive behavior, proxy diagnostics, and final documentation/proof can be reviewed independently.
- 2026-05-18: Treat `packages/rigorloop/test/cli.test.js` as the first implementation proof surface because the existing CLI package is small and already uses fixture-backed archive and fetch helpers.
- 2026-05-18: Add a small package-local adapter descriptor module for M1 instead of keeping descriptor data embedded in the CLI entrypoint. This keeps adapter identity, roots, and archive naming testable before later schema and extraction milestones.
- 2026-05-18: Keep M2 schema parsing and serialization package-local in `packages/rigorloop/dist/lib/lockfile.js`, while leaving proxy diagnostics and older opencode warning behavior to later milestones.
- 2026-05-18: Keep M4 proxy support diagnostics-first and use bounded helper functions in the CLI entrypoint instead of adding Undici dispatcher support or a new dependency.

## Surprises and discoveries

- M1 could prove descriptor and trusted metadata selection without completing multi-root extraction or lockfile schema v2; those remain scoped to M2 and M3.
- M2 tests initially failed as expected because the CLI still wrote schema v1 lockfiles, rejected schema v2 parsing, and rejected opencode multi-root trusted metadata.
- M2 review found that skills-only older opencode behavior must be fixed in M2 because manifest and directory planning still use descriptor roots before trusted metadata narrows required roots.
- M2 review-resolution keeps opencode descriptor roots as possible roots while using trusted metadata roots for durable manifest and directory actions.
- M2 code-review rerun found that the non-dry-run plan rebuild fixed real installs, but dry-run still returns before trusted metadata validation and reports the descriptor `commands` root for older skills-only opencode metadata.
- M3 found that archive path allowlisting also needs trusted artifact roots, not descriptor possible roots, so older skills-only opencode archives cannot smuggle `.opencode/commands` files into extraction.
- M3 code-review found that older opencode skills-only compatibility is inferred from missing command alias metadata, but `MAI-R21f` requires an explicit bundled trusted-metadata compatibility boundary.
- M3 review-resolution uses `skills_only_compatibility.releases` as the explicit trusted artifact metadata marker for older opencode skills-only compatibility.
- M3 code-review rerun found that opencode metadata can still declare `.opencode/commands` without `command_aliases.opencode`, bypassing both skills-only warning behavior and declared-alias validation.
- M3 review-resolution now treats opencode commands-root metadata without `command_aliases.opencode` as a blocker in both dry-run and non-dry-run local archive paths.
- M3 final code-review found no remaining material issues in the opencode commands-root metadata guard.
- M4 found that existing mocked fetch success covered Codex only, so M4 added the same network mode proof for Claude and opencode before adding failure diagnostics.
- M4 keeps archive verification failures on the existing validation error path; proxy diagnostics are added only when fetch itself fails.
- M4 code-review found that diagnostics do not detect the actual Node `--use-env-proxy` runtime flag through `process.execArgv`.

## Validation notes

- 2026-05-18: Added failing M1 tests first; initial `npm test --prefix packages/rigorloop` failed with missing `packages/rigorloop/dist/lib/adapters.js`.
- 2026-05-18: `npm test --prefix packages/rigorloop` passed after adding descriptor support and metadata selection behavior.
- 2026-05-18: `bash scripts/ci.sh --mode explicit --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/dist/lib/adapters.js --path packages/rigorloop/dist/lib/official-archive-url.js --path packages/rigorloop/dist/metadata/adapter-artifacts-v0.1.5.json --path packages/rigorloop/test/cli.test.js --path docs/plans/2026-05-18-multi-adapter-init-and-proxy-aware-download.md --path docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/change.yaml` passed selected checks: `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `rigorloop_cli.test`, and `npm_package_publication.test`.
- 2026-05-18: `code-review-m1-r1` completed with status `clean-with-notes`; M1 closed and M2 is the next implementation stage.
- 2026-05-18: Added M2 tests first; `npm test --prefix packages/rigorloop` failed as expected for schema v2 lockfile parsing/writing and opencode multi-root metadata.
- 2026-05-18: `npm test --prefix packages/rigorloop` passed after adding schema v2 lockfile parsing/serialization, additive manifest updates, schema v1 Codex upgrade checks, and multi-root opencode lockfile support.
- 2026-05-18: `bash scripts/ci.sh --mode explicit --path packages/rigorloop/dist/lib/lockfile.js --path packages/rigorloop/dist/bin/rigorloop.js --path packages/rigorloop/test/cli.test.js` passed selected checks: `rigorloop_cli.test` and `npm_package_publication.test`.
- 2026-05-18: `code-review-m2-r1` recorded `CR-M2-R1-F1`; M2 remains open for review-resolution.
- 2026-05-18: `npm test --prefix packages/rigorloop` passed after resolving `CR-M2-R1-F1`; package tests include `TMAI-017 skills-only opencode archive omits commands root from plan and manifest`.
- 2026-05-18: `code-review-m2-r2` recorded `CR-M2-R2-F1`; dry-run older opencode skills-only planning remains open for review-resolution.
- 2026-05-18: `npm test --prefix packages/rigorloop` passed after resolving `CR-M2-R2-F1`; package tests include `TMAI-020 dry-run skills-only opencode archive omits commands root without mutation`.
- 2026-05-18: `code-review-m2-r3` completed with status `clean-with-notes`; M2 closed and M3 is the next implementation stage.
- 2026-05-18: Added failing M3 tests first; `npm test --prefix packages/rigorloop` failed as expected for missing declared opencode command alias validation and missing older opencode skills-only warnings.
- 2026-05-18: Added extraction-boundary coverage for older opencode skills-only metadata; `npm test --prefix packages/rigorloop` failed as expected because archive path allowlisting still used descriptor possible roots.
- 2026-05-18: `npm test --prefix packages/rigorloop` passed after adding opencode alias validation, older skills-only warnings, human warning output, and metadata-root archive path allowlisting.
- 2026-05-18: `python scripts/build-adapters.py --version 0.1.5 --output-dir /tmp/rigorloop-adapter-plan-check` passed and produced Codex, Claude, and opencode adapter archives.
- 2026-05-18: `python scripts/validate-adapters.py --version 0.1.5 --root /tmp/rigorloop-adapter-plan-check` passed for generated adapter archives.
- 2026-05-18: `code-review-m3-r1` recorded `CR-M3-R1-F1`; M3 remains open for review-resolution.
- 2026-05-18: `npm test --prefix packages/rigorloop` failed as expected after adding `TMAI-017 unmarked skills-only opencode metadata blocks before mutation`; the CLI still accepted unmarked skills-only metadata before the fix.
- 2026-05-18: `npm test --prefix packages/rigorloop` passed after resolving `CR-M3-R1-F1`; package tests include the positive marked skills-only opencode path and the negative unmarked metadata blocker.
- 2026-05-18: `code-review-m3-r2` recorded `CR-M3-R2-F1`; M3 remains open for review-resolution.
- 2026-05-18: `npm test --prefix packages/rigorloop` failed as expected after adding opencode commands-root-without-alias metadata tests; dry-run and non-dry-run still accepted invalid metadata before the fix.
- 2026-05-18: `npm test --prefix packages/rigorloop` passed after resolving `CR-M3-R2-F1`; package tests include dry-run and non-dry-run blockers for opencode commands-root metadata without `command_aliases.opencode`.
- 2026-05-18: `code-review-m3-r3` completed with status `clean-with-notes`; M3 closed and M4 is the next implementation stage.
- 2026-05-18: Added failing M4 tests first; `npm test --prefix packages/rigorloop` failed as expected because network fetch failures still returned the generic `release-unavailable` blocker without bounded proxy diagnostics or actionable human output.
- 2026-05-18: `npm test --prefix packages/rigorloop` passed after adding bounded network download diagnostics, proxy env-var name detection, failure classification, fallback guidance, human redaction, and verification-failure preservation.
- 2026-05-18: `code-review-m4-r1` recorded `CR-M4-R1-F1`; M4 remains open for review-resolution.

## Outcome and retrospective

- Not complete. Fill this only after all implementation milestones and downstream lifecycle gates close.

## Readiness

- See `Current Handoff Summary`.
- Not ready for final closeout until all implementation milestones and downstream gates are complete.
