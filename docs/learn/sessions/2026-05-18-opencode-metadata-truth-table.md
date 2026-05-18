# Learn Session: Opencode Metadata Truth Table

## Status

- captured

## Frame

- Trigger: explicit maintainer invocation asking why `code-review-m3-r1` and `code-review-m3-r2` were similar and why they were not fixed in one pass.
- Trigger type: explicit maintainer request / repeated review findings.
- Scope:
  - `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/code-review-m3-r1.md`
  - `docs/changes/2026-05-18-multi-adapter-init-and-proxy-aware-download/reviews/code-review-m3-r2.md`
  - `specs/multi-adapter-init-and-proxy-aware-download.md` requirements `MAI-R21d` through `MAI-R21f` and `MAI-R40` through `MAI-R46c`
  - `packages/rigorloop/dist/bin/rigorloop.js` metadata validation branch reviewed in M3
  - `packages/rigorloop/test/cli.test.js` opencode fixture tests reviewed in M3
- Evidence in scope:
  - `CR-M3-R1-F1`: skills-only opencode compatibility was inferred from missing `command_aliases.opencode` instead of explicit trusted metadata.
  - `CR-M3-R2-F1`: opencode commands-root metadata could be accepted without `command_aliases.opencode`.
  - Prior learn session `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`, especially the observation that local safe resolutions need same-class sweeps before rereview.
- Explicit exclusions:
  - This session does not resolve `CR-M3-R2-F1`.
  - This session does not update workflow, spec, test spec, code, or skill policy.
  - This session does not claim M3 closeout, verification readiness, branch readiness, or PR readiness.
- Prior learnings reviewed:
  - `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`
- Session record path: `docs/learn/sessions/2026-05-18-opencode-metadata-truth-table.md`

## Observe

### O1 - The two M3 findings are the same invariant expressed through different branches

Evidence:

- `CR-M3-R1-F1` found that opencode skills-only behavior was allowed without an explicit trusted metadata compatibility boundary.
- `CR-M3-R2-F1` found that opencode commands-root behavior was allowed without `command_aliases.opencode`.
- The governing spec ties these states together: absence of `command_aliases.opencode` is the older skills-only signal (`MAI-R21e`), while older skills-only installs must omit `.opencode/commands`, warn, and record only `skills` (`MAI-R44`, `MAI-R46a` through `MAI-R46c`).

Observation:

Both findings are about the same missing state-machine check: opencode metadata must be validated as a truth table across `install_roots.commands`, `command_aliases.opencode`, and explicit skills-only compatibility metadata. The first fix handled only the single-root skills-only branch and did not sweep the adjacent invalid multi-root-without-alias branch.

Practical answer:

We did not fix it in one pass because the review-resolution for `CR-M3-R1-F1` treated the finding too locally. It added a guard for "no command aliases and no commands root" but did not convert the spec into an exhaustive opencode metadata-state matrix before returning to review.

### O2 - The test repair was necessary but not complete as a contract matrix

Evidence:

- After `CR-M3-R1-F1`, positive skills-only fixtures were marked with `skills_only_compatibility.releases`.
- A negative test was added for unmarked single-root skills-only metadata.
- No negative test was added for `install_roots.commands` present while `command_aliases.opencode` is absent.

Observation:

The test added for `CR-M3-R1-F1` proved the specific missing compatibility marker case. It did not prove the broader invariant that every opencode commands root must be backed by declared command alias metadata.

Practical answer:

The immediate review-resolution optimized for the named failing path instead of enumerating the related metadata combinations. For this contract, the minimal adequate matrix should include at least:

| commands root | `command_aliases.opencode` | skills-only compatibility marker | Expected behavior |
|---|---|---|---|
| absent | absent | present | allow skills-only with warning |
| absent | absent | absent | block before mutation |
| present | present | irrelevant | allow commands only after declared alias validation |
| present | absent | any | block before mutation |

### O3 - This repeats an already captured same-class sweep lesson

Evidence:

- `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md` says each review round closed the latest specific finding, then the next round discovered another instance of the same class in a different surface or spelling.
- That session's practical guidance says to run a same-class sweep before asking for the next review.

Observation:

This M3 issue is the code-contract version of the same pattern. The repeated finding was not due to missing lifecycle ceremony; it was due to insufficient same-class sweep after a material review finding.

Practical answer:

After a review finding about a predicate or state boundary, the resolution should build the complete decision table for that predicate before implementation and tests. For M3, that table is the opencode metadata truth table above.

## Classify

| Observation | Proposed classification | Final classification | Secondary routes | Confirmed by | Rationale |
|---|---|---|---|---|---|
| O1 | observation | observation | session record; active `CR-M3-R2-F1` review-resolution | maintainer-triggered question plus review evidence | This explains the immediate root cause without creating new policy. |
| O2 | process-follow-up | process-follow-up | `CR-M3-R2-F1` review-resolution should add the missing commands-root-without-alias negative test | maintainer-triggered question plus review evidence | The follow-up is already owned by the open review finding and should be fixed there, not in learn. |
| O3 | no-durable-lesson | no-durable-lesson | cite prior same-class sweep learning | prior session already captured the reusable lesson | The durable lesson already exists; this session records another instance and applies it to opencode metadata validation. |

## Route

- Session record created: `docs/learn/sessions/2026-05-18-opencode-metadata-truth-table.md`.
- No topic file updated because the durable same-class sweep lesson is already captured in `docs/learn/sessions/2026-05-09-review-finding-volume-root-cause.md`.
- No authoritative artifact updated in this learn session.
- Follow-up route: resolve `CR-M3-R2-F1` in the active M3 review-resolution loop by adding opencode commands-root-without-alias validation and a fixture-backed negative test.

## Answer

The short reason: the `CR-M3-R1-F1` fix was too local. It fixed "single-root skills-only opencode must have explicit compatibility metadata" but did not sweep the whole opencode metadata state machine.

The better first-pass resolution would have converted the spec into a truth table before editing code:

- no commands root + no aliases + compatible marker: allow skills-only with warning;
- no commands root + no aliases + no marker: block;
- commands root + aliases: validate and install commands;
- commands root + no aliases: block.

`code-review-m3-r2` found that last row. It should have been caught during the `CR-M3-R1-F1` review-resolution because it is the adjacent branch of the same invariant: runtime roots and command aliases must be derived from explicit trusted metadata, not inferred from whatever fields happen to be present.

## Validation

- `git diff --check -- docs/learn/sessions/2026-05-18-opencode-metadata-truth-table.md` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/learn/sessions/2026-05-18-opencode-metadata-truth-table.md` passed with no lifecycle-managed artifact files selected.
