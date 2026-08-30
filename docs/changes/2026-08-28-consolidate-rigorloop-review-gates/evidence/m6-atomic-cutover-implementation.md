# M6 atomic cutover implementation

Change ID: 2026-08-28-consolidate-rigorloop-review-gates
Milestone: M6
Stage authority: implement
Subject path: docs/plans/2026-08-29-consolidate-rigorloop-review-gates.md
Validation result: passed

## Scope completed

- Made `proposal-review`, `design-review`, `delivery-review`, `code-review`, and `verify` the supported decision gates.
- Removed the four retired artifact-review skill entrypoints and removed them from public adapter inventory and workflow targets.
- Enabled current Design Review and Delivery Review package authority for downstream lifecycle work while keeping historical records readable and non-authorizing.
- Kept package authority concise: exact artifact ID-to-path maps and review identity, without aggregate or member content hashes.
- Added cutover admission that rejects active `spec-review`, `architecture-review`, `plan-review`, or `test-spec-review` routing while ignoring terminal historical evidence.
- Updated canonical governance, workflow guidance, authoring and downstream skills, lifecycle behavior, validators, fixtures, and adapter generation together.

## Cutover and rollback evidence

- Legacy-dependent inventory: zero active governed changes depend on a retired progression stage; 30 governed records were checked.
- Historical authority: lifecycle tests reject historical artifact reviews as Design Review or Delivery Review package authority.
- Partial authority: downstream work is blocked when a change uses `review_packages` but either current package lacks authority.
- Pre-adoption rollback: this slice adds no activation manifest, topology selector, migration, or destructive record rewrite. Before a consolidated change begins, reverting the reviewed cutover commit restores the prior code and skill surface while existing historical records remain unchanged. After adoption, recovery remains forward-only unless separately approved.
- Publication: none. The archives below were generated and validated in a temporary directory only.

## Generated adapter evidence

- Published skills per adapter: 22.
- Retired progression skills in generated archives: none.
- `python scripts/build-adapters.py --version v0.4.1 --output-dir <temporary-directory>`: passed for Claude Code, Codex, and OpenCode.
- `python scripts/validate-adapters.py --root <temporary-directory> --version v0.4.1`: passed.
- Claude Code archive SHA-256: `65d3b7034e01b65ecf446f20fe49bc36c56c88cf070e9121439c07d155604aa8`.
- Codex archive SHA-256: `8aac9d451e649e87e3771dbf107a26e2ddc5a1da106ca66a346acf9c6cbd096a`.
- OpenCode archive SHA-256: `5e01cc3d7cadb75a89af5dcad1b8db6f5df363a3d2f859c27f255f7d6b601b08`.

## Validation

- `npm test --prefix packages/rigorloop`: passed; 297 tests.
- `python scripts/test-lifecycle-cli-conformance.py`: passed; 6 invalid and 10 protected cases.
- `python scripts/test-governed-lifecycle-cli-validator.py`: passed; 7 tests.
- `python scripts/validate-governed-lifecycle-cli.py`: passed; 30 records, zero legacy progression dependencies, two known baseline warnings.
- `python scripts/test-skill-validator.py`: passed; 450 tests, with 90 explicitly retired-topology tests skipped.
- `python scripts/test-review-artifact-validator.py`: passed; 104 tests.
- `python scripts/test-boundary-first-reference.py`: passed; 28 tests.
- `python scripts/test-adapter-distribution.py`: passed; 154 tests.
- `bash scripts/ci.sh --mode broad-smoke`: passed; 11 checks in 394 seconds.
- `git diff --check`: passed.

## Review handoff

M6 is ready for final implementation-milestone Code Review of cutover atomicity, retired-entrypoint removal, package-authority enforcement, historical-evidence behavior, rollback boundaries, generated parity, and cross-milestone composition. This evidence does not publish a release, claim Code Review approval, or close M6.
