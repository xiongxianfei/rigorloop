# M3 Package and Boundary Proof

Date: 2026-08-12
Milestone: M3

## Deterministic results

- CMD1 preservation proof: 18 rules, 18 literals, 17 scenarios; unknown values rejected first.
- CMD2 canonical skill validation: passed.
- CMD3 skill validator: 313 tests passed, 16 skipped.
- CMD4 generated skill tests: 7 passed.
- CMD5 generated skill drift check: passed.
- CMD6 adapter distribution: 150 tests passed.
- CMD7 selected temporary adapter build and clean install: Codex, Claude, and opencode archives passed for `spec-review`.
- CMD8 boundary proof: passed with active snapshot and rollback metadata.
- CMD9 change metadata: passed at the last workflow handoff and reruns before M3 review.
- CMD10 formal review structure: reruns before M3 review.

The adapter test suite emits an expected recorded-source negative-fixture diagnostic about a deliberately incomplete historical token-cost report after its 150 tests pass; the process exits successfully. No release publication or target-agent runtime occurs.

## Resource identity

`boundary-first-method-v1.md` has SHA-256 `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` in both canonical projection and skill package. `boundary-first-feature-authoring-v1.md` has SHA-256 `962180f3b6d2699c1001fe0c2792f9e8bb3c9c60a7c7f2053dfb73fdf99df7fe` in both locations.

Build and adapter checks prove the new governed reference and both assets exist at identical relative paths and bytes in generated, archived, and clean-installed packages. Missing, stale, escaped, and mixed resources remain deterministic failures. Rollback restores the prior complete package rather than combining versions.
