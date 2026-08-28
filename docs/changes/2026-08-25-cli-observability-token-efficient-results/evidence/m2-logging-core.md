# M2 Logging Core Evidence

- Subject: privacy-safe event construction, strict configuration, safe local sink, bounded locking, five-file rotation, and diagnostic-failure isolation
- Requirements: R3-R17, R33-R34, AC1-AC4, AC8
- Correction target: `CLIOBS-M2-L1-F1` through `CLIOBS-M2-L1-F4`, `M2-L1B-F1` through `M2-L1B-F4`, `CLIOBS-M2-R3-F1` through `CLIOBS-M2-R3-F4`, `CLIOBS-M2-R4-F1` through `CLIOBS-M2-R4-F4`, `CLIOBS-M2-R5-F1`, `CLIOBS-M2-R8-F1`, `CLIOBS-M2-R11-F1`, and `CLIOBS-M2-R13-F1`
- Operation: governed correction spanning approved specification and ADR clarification, exact implementation and test changes, and this existing M2 evidence surface; workflow routing and upstream settlement used the lifecycle CLI, while implementation review resolution remains review-owned

## Identity-stable regression proof

Before production correction, the focused logging and invocation command failed five exact regressions:

- unsafe scalar objects and incomplete completion facts were accepted;
- a throwing wall clock escaped and exposed an oversized synthetic marker in the failure;
- a short write plus rollback failure corrupted the active JSONL tail;
- lock cleanup removed a replacement lock that it did not own; and
- a throwing diagnostic stderr sink prevented semantic dispatch.

The R4 correction added two more failing proofs before production mutation: crossed event/sequence pairs were accepted, and an active-file `fstat` failure leaked its opened descriptor. The same tests and inputs now pass unchanged.

The R5 correction added two identity-stable failing proofs before production mutation. The first showed that the six rotation/publication `unlink` and `rename` sites did not each receive adjacent root, source, and destination inspection. The second injected an I/O failure into the required pre-mutation root check and showed that mutation still occurred because that check was absent. The same tests and inputs now pass unchanged.

The R8 correction added one identity-stable T04 proof before production mutation. An absolute log root nested beneath an existing regular-file component returned raw `ENOTDIR` instead of the stable unsafe-path classification. The same fixture and assertion now pass unchanged with `RL_LOG_UNSAFE_PATH`, unchanged sentinel bytes, and no created nested root.

The R11 correction added one identity-stable T05 matrix before production mutation. A close adapter that threw before releasing an active-read, ordinary-validation, or rotation descriptor left that descriptor valid after `appendDiagnosticEvent()` returned. The same seven scenarios now pass unchanged and prove `EBADF` after return.

The R13 correction added one identity-stable T05 acquisition proof before production mutation. When the injected acquisition identity check failed and its close adapter closed the owned descriptor, reopened a different file on the same descriptor number, and threw, trusted cleanup closed that unowned replacement. The same fixture now passes unchanged: the append returns `RL_LOG_UNAVAILABLE`, the fixed lock remains fail-closed, and the replacement descriptor remains valid for its owner.

## Corrected boundaries

- Every admitted common, completion, and lifecycle field now has a closed string, boolean, non-negative safe-integer, status, or string-list shape. Completion events require `status`, `exit_code`, and `duration_ms`.
- Event kind and sequence are validated together: start accepts only sequence 1 and completion accepts only sequence 2.
- Lifecycle operation classification admits only the documented operation vocabulary; an unknown raw argv token becomes the constant `unknown` and is never serialized.
- Invocation entropy must produce exactly eight bytes. Timestamps recover through a safe internal clock, duration inputs reject negative or non-integer values, and the encoded JSONL record including its newline is capped at exactly 16 KiB.
- Oversized input is replaced by a constant-only event. Synthetic credentials, argv, requests, fingerprints, URLs, user and host names, repository paths, stack text, and nested sentinel values are absent byte-for-byte.
- The held exclusive lock inode doubles as the unpublished append candidate. A short write, disk-full error, fsync error, close error, or rename error therefore leaves either the prior active file or a complete published candidate; it cannot leave a partial active line.
- Owned files are opened with `O_NOFOLLOW` where supported and checked by pre-open and post-open device/inode identity. Acquisition captures a trusted device/inode identity immediately after opening the lock and before the injected inspection can fail or reuse its descriptor number. One bounded close helper owns every later descriptor release. If the first close reports failure, the helper checks whether the descriptor is already invalid; otherwise it verifies the still-open device/inode and performs one trusted cleanup attempt only for the matching identity. A mismatched reused descriptor is never closed. Every supported injected post-open fault therefore releases only its owned descriptor before return. Failed publication deliberately retains the stale fixed lock instead of performing pathname unlink cleanup whose ownership cannot be proved atomically.
- Lock acquisition uses injected monotonic-clock and wait adapters, at most ten attempts, at most nine waits, and a 1,000 ms total budget. It never steals a live or stale lock.
- Post-open acquisition faults close the acquired descriptor, return `RL_LOG_UNAVAILABLE`, retain the stale or unverifiable lock fail-closed, and make subsequent attempts degrade without mutation, as approved R14 now specifies.
- One injected pre-mutation validator now rechecks the absolute root, every existing component, and every owned entry, including any existing destination, before each of the six rotation/publication mutations. It then rechecks the affected source device/inode as the final operation before the `unlink` or `rename`. An observed unsafe path returns `RL_LOG_UNSAFE_PATH`; an ordinary inspection failure degrades with `RL_LOG_UNAVAILABLE`; neither path performs the guarded mutation.
- The component walker classifies every observed symlink or non-directory component as `RL_LOG_UNSAFE_PATH` before creation or lock acquisition; raw `ENOTDIR` does not escape this supported unsafe-path partition.
- R11 and the accepted ADR require these no-follow checks at defined operation boundaries but do not claim that portable Node pathname calls are an atomic security boundary against a same-user or privileged process replacing pathnames after a check. The implementation and this evidence make no race-proof-containment claim for that excluded actor.
- Diagnostic stderr writes are guarded before and after dispatch. Sink and stderr failures cannot replace the semantic exit code, and explicit console `off` performs no emergency write.
- Timestamp-source failure no longer substitutes an unreported second clock. It returns a closed unavailable signal, skips the affected event, marks the invocation degraded, and preserves semantic execution.

## T02-T05 proof matrix

- T02: exact schemas and mandatory completion fields; closed event/sequence pairs; every scalar/list type; deterministic and invalid entropy; UTC millisecond timestamps; throwing clock; non-negative duration; control normalization; lifecycle-family isolation; exact 16 KiB and oversized boundaries.
- T03: prohibited-value matrix across every caller-provided non-allowlisted surface, unsafe nested shapes, oversized fallback, stdout, stderr, active JSONL, rotated archives, and exact lookup.
- T04: Linux, macOS, and Windows defaults; absent-root creation modes; broad root/file refusal without repair; root, owned-file, and lock symlink refusal; intermediate regular-file rejection with stable unsafe-path classification; external sentinel preservation for supported pre-existing unsafe-path partitions.
- T05: below/at/above rotation behavior; four-archive retention; adjacent root/source/destination validation before all six pathname mutations; mutation refusal on validation I/O failure; seven pre-close fault positions covering active read, ordinary validation, and all rotation-held descriptors with post-return `EBADF`; identity-bound acquisition cleanup that preserves a same-number replacement descriptor; six real concurrent RigorLoop child writers crossing both ordinary append and rotation; post-start process interruption; deterministic lock exhaustion; acquisition and active-file post-open descriptor closure; stale-lock retention; short-write plus rollback failure; disk-full, fsync, close, and rename faults; no pathname unlink after failed publication; complete retained JSONL; no network, child-process, database, timer, or surviving-handle dependency in the logging core.

## Corrected target identities

- `packages/rigorloop/dist/lib/diagnostic-event.js`: `sha256:7a458a3630151894b752dd580fab68ceecbd437410e0c244eea2bdf4afdb8ede`
- `packages/rigorloop/dist/lib/log-sink.js`: `sha256:65fd6fa394e24d389c079c44765ff0b46add4ab6223140191bd9dd63956f99d5`
- `packages/rigorloop/dist/lib/cli-observability.js`: `sha256:9e01a9d782859be60109ee5c1b9e5b78e1ae1a1f495e2c8069cfef50e3d1885c`
- `packages/rigorloop/test/cli-observability.test.js`: `sha256:4f47224080fc9d2266be1af2d10051d87a7327118d7720166d69bfef74c89f3f`
- `packages/rigorloop/test/cli-invocation-observability.test.js`: `sha256:eff0b3ec159a95b958b17d64c474afd301d4e14fd179f108b8deaf3bc1c5ef08`

## Validation

- C02: `node --test packages/rigorloop/test/result-renderer.test.js packages/rigorloop/test/cli-observability.test.js` passed 43/43 tests.
- C01: `npm test --prefix packages/rigorloop` passed 244/244 tests.
- `python3 scripts/validate-boundary-first.py --path specs/cli-observability-and-token-efficient-results.md` passed.
- `git diff --check` passed.

## Result and handoff

The R13 acquisition-identity finding and all earlier M2 findings now have contract, architecture, implementation, or regression corrections on this target. This evidence does not approve M2. The corrected implementation must return to independent code review before any lifecycle advancement; elevated-risk promotion still requires distinct clean agreement on the corrected target.
