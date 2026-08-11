# M3 package and parity proof

## Result

Canonical, generated, archived, and temporary installed `verify` packages contain the mapped resources with required parity. All planned M3 commands pass. No target agent, publication, network workflow, or tracked generated package was executed or mutated.

## Validation

| ID | Command | Result | Important output |
| --- | --- | --- | --- |
| CMD1 | approved ledger/scenario Python assertion | pass | 16 rules, 15 literals, 17 scenarios; unknown values rejected first |
| CMD2 | `python scripts/validate-skills.py skills/verify/SKILL.md` | pass | canonical verify package valid |
| CMD3 | `python scripts/test-skill-validator.py` | pass | 302 tests passed; 16 intentional skips |
| CMD4 | `python scripts/test-build-skills.py` | pass | 7 tests passed |
| CMD5 | `python scripts/build-skills.py --check` | pass | temporary generated tree valid |
| CMD6 | `python scripts/test-adapter-distribution.py` | pass | 150 tests passed in 311.712 seconds |
| CMD7 | approved temporary v0.3.6 build and verify-only clean-install command | pass | codex, claude, and opencode archives built; Gate B validated archives and clean installs for `verify` |
| CMD8 | `python scripts/validate-boundary-first.py --check --path specs/verify-skill-simplification.md` | pass | active boundary proof and rollback metadata validated |

The informational Gate C failure messages printed during CMD6 belong to negative test fixtures; the enclosing 150-test suite passed.

## Additional deterministic proof

- Ledger destination audit: 16 of 16 destination paths and anchors resolve.
- Boundary-first canonical reference hash remains unchanged.
- `git diff --check` passes after evidence creation.
- Words and bytes, rather than an unpinned tokenizer, provide portable profile accounting.

## Package boundary

The package remains canonical `SKILL.md` plus explicitly mapped packaged references. No new runtime, state store, service, dependency, lifecycle owner, result asset, permanent size validator, or runtime journey was introduced.
