# M3 Gate B Evidence

## Result

`python scripts/validate-adapters.py --adapter-root <local-output>` now exposes
the stable `Gate B (published adapter/package parity)` result. `--root` remains
a legacy mutually exclusive alias for compatibility. Gate B independently
validates Codex, Claude Code, and opencode archives built from canonical
skills, including target inventory, mapped paths, raw bytes, declared
frontmatter transforms, target roots, opencode command aliases, and archive
shape.

An adversarial test replaces the Claude archive with the Codex archive. Gate B
rejects it based on Claude-owned root/missing-content failures, proving one
target cannot borrow another target's result.

## Package negative paths

The 150-test adapter suite covers missing and extra files, stale bytes,
malformed canonical skills and resource maps, unsafe and unexpected opencode
aliases, unsupported or undeclared frontmatter, archive root/inventory errors,
mapped-resource parity, recorded-source compatibility, and independent package
generation. M3 adds the archive-substitution regression and the canonical
`--adapter-root` CLI proof; it does not add another validator.

## Installer/materializer inventory

Archive copying alone is fully proved by Gate B. The public CLI performs
additional RigorLoop-owned deterministic behavior that package parity cannot
prove:

- selects and authenticates local or official archive metadata;
- validates adapter identity, URL, checksum, size, tree hashes, and release;
- rejects traversal, symlinks, wrong roots, malformed zip input, and conflicts;
- extracts transactionally into an empty or existing project;
- handles Codex and Claude single skill roots and opencode skill plus command roots;
- applies force/conflict and rollback behavior; and
- writes and validates optional state and lockfile projections.

Those branches retain filesystem-only CLI tests. The focused clean-install
smoke builds local archives, creates one empty temporary project per target,
invokes the local Node CLI as `init <target> --from-archive <local-path>
--json`, and inspects installed skill/resource bytes. Captured commands prove
the only executable is `node`; there is no target-runtime command, prompt,
network publication, transcript, or model output.

## Test-first evidence

The planned `--adapter-root` command initially failed as an unknown argument.
After adding it to the existing validator parser, the focused CLI test passed.
The archive-substitution and captured filesystem-only installer tests passed
without production changes to adapter generation or installer behavior.

## Validation

- `python scripts/test-adapter-distribution.py` — pass; 150 tests in 323.893 seconds.
- `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/tmp.FBhz88tXVG` — pass; Codex, Claude, and opencode archives built locally.
- `python scripts/validate-adapters.py --version v0.1.5 --adapter-root /tmp/tmp.FBhz88tXVG` — pass; Gate B archive parity.
- `python scripts/validate-adapters.py --version v0.1.5 --adapter-root /tmp/tmp.FBhz88tXVG --clean-install-smoke --skill code-review` — pass; filesystem-only all-target materialization.
- `npm test --prefix packages/rigorloop` — pass; 117 tests in 8.162 seconds.
- Focused M3 tests — pass; four tests covering canonical CLI spelling, required local root, target substitution rejection, and filesystem-only all-target commands.

The temporary output is local evidence only and is not published or tracked.

## Retirement and rollback

M3 retains Gate B and the CLI branches that package parity cannot prove. It
removes no adapter or install check, so protected package and materialization
failures remain covered. Revert the M3 commit to restore the legacy-only CLI
argument and prior result text; public package formats and canonical skill
bytes are unchanged.
