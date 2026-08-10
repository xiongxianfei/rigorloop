# Why the Published-Skill-First Simplification Changed the Repository

Stage: explain-change
Status: current
Final diff identity: feec34752630a0ca3d6bd5a90abf6d6c49e2f5ac..b7d48adc#sha256:282032c58e0eb81dc1f500dbdd5ae3950a702f63d8673a0a0352b359a23c1c8e
Final review identity: code-review-final-r1@3734eebe

## Summary

The repository now treats canonical skills, their packaged resources, generated
adapter archives, and release artifacts as the deterministic product chain.
PR and main CI call those product and governance owners directly. Semantic
skill quality remains a review responsibility, and no target-agent runtime,
prompt, transcript, or model-output score is repository acceptance evidence.

The change deliberately does not delete every older validation implementation.
The selector, validation cache, and broad-smoke paths still have active
compatibility contracts, so this initiative removes them from default PR/main
acceptance while retaining and testing their explicit or local entry points.

## Problem

Repository validation had accumulated routing, cache, scheduling, runtime-smoke,
semantic, and meta-validation layers around the published skills. That made the
validation system resemble a second product and obscured which failures the
repository actually owns. The selected solution was to prove deterministic
files and transformations, review semantic quality, and retire old checks only
after their protected failures and rollback paths are known.

## Decision trail

- The accepted proposal chose three composed product gates plus one separate
  lifecycle-governance owner, with semantic quality handled in review.
- Spec R1-R10 define Gate A, Gate B, Gate C, runtime exclusion, and the narrow
  filesystem-materialization boundary. R11-R16 separate semantic and governance
  ownership and freeze new validation subsystems. R17-R25 govern safe retirement
  and compatibility. R26-R29 supersede only the named runtime-oriented clauses
  while preserving deterministic package support.
- The architecture and ADR make `skills/` the authored source, give every public
  adapter equivalent deterministic proof, and require Gate C to compose rather
  than reinterpret Gates A and B.
- Plan M1 inventoried protected failures; M2-M5 consolidated Gate A, Gate B,
  Gate C, and governance; M6 cut hosted acceptance over to the stable owners.

## Diff rationale by area

| Area and files | What changed | Why | Requirements and proof |
| --- | --- | --- | --- |
| `scripts/skill_validation.py`, `scripts/validate-skills.py`, skill-contract docs and tests | Gate A received a stable identity and missing input now fails explicitly. | Canonical structure, resources, paths, placeholders, and contractual claims need one deterministic owner; prose does not. | R2-R3, R11, T2-T3; 289 skill regressions. |
| `scripts/validate-adapters.py`, `scripts/test-adapter-distribution.py` | Gate B exposes the current `--adapter-root` interface, preserves its legacy alias, proves all target archives, and uses filesystem-materialization language. | Codex, Claude Code, and opencode need equivalent inventory, archive, transform, path, and byte proof without runtime execution. | R4-R5, R9-R10, R27-R28, T4-T5; 150 adapter regressions. |
| `scripts/validate-release.py`, `scripts/release-verify.sh`, release tests | Release output is labeled Gate C, composes current A/B owners, and retains release-only metadata, notes, checksum, archive, version, and rollback proof. | Release verification must expose underlying product failures without copying their parsers or running an agent. | R6-R8, R24, R29, T6-T7; 104 release regressions and local rehearsal. |
| `scripts/artifact_lifecycle_validation.py`, `scripts/validate-artifact-lifecycle.py`, lifecycle/review tests | The public lifecycle entry point composes full change-metadata and review-structure validation; review paths resolve their owning change record. | Contributors and CI need one governance result while focused internal parsers remain independently testable and fail closed. | R12-R13, T8; 170 lifecycle, 61 metadata, and 103 review tests. |
| `scripts/retirement_ledger.py`, `retirement-ledger.json`, retirement tests | Every known check is mapped to a protected failure, owner, clauses, disposition, proof state, repair, and rollback. | A smaller architecture is safe only when removed or bypassed checks cannot silently lose contractual failures. | R14-R20, R22, R25, T1, T10, T13-T14, T16; 14 ledger tests. |
| `scripts/ci.sh`, `.github/workflows/ci.yml`, selector tests | PR/main use 26 direct sequential commands; local, explicit, release, and legacy broad-smoke compatibility paths remain. | Hosted acceptance should visibly call stable owners and stop on their first failure without selector, cache, or scheduler indirection. | R21, R23, T9, T11, T15-T16; 152 compatibility tests and a real 618-second direct run. |
| Architecture, project map, workflows, proposal/spec/test-spec/plan, and change-local evidence | Documentation records the new ownership, transition state, exact partial-retirement boundary, tests, reviews, and rollback. | Maintainers must be able to distinguish current product proof from historical or retained compatibility machinery. | Full R1-R29 trace and M1-M6 evidence. |

Review invocation manifests, detailed reviews, the review log, and review
resolution are lifecycle evidence; they do not add product behavior.

## Tests added or changed

- T1 and T13 gained a fail-closed retirement-ledger library and negative tests
  for unknown vocabularies, incomplete transitions, missing catalog ownership,
  and unsafe removal.
- T2 added the missing canonical-root regression and preserved ambiguous prose
  as review-owned rather than a validation failure.
- T4-T5 added all-target archive, declared-transform, independent-target, and
  local filesystem-materialization assertions.
- T6-T7 added Gate C composition and acceptance-command exclusion assertions.
- T8 added composed change-metadata and review-evidence failures through the
  single public governance entry point.
- T9, T11, T15, and T16 added exact PR/main direct-graph checks, range forwarding,
  runtime exclusion, and compatibility-mode coverage.

These are unit or integration tests for deterministic owners. Semantic skill
quality remains the MP1 manual review case because converting it into a parser
or model score would violate R3 and R11.

## Validation evidence available before final verify

- `python scripts/test-skill-validator.py` — 289 tests passed.
- `python scripts/test-adapter-distribution.py` — 150 tests passed.
- `python scripts/test-release-transaction.py` — 104 tests passed.
- Lifecycle, metadata, and review suites — 170, 61, and 103 tests passed.
- `python scripts/test-retirement-ledger.py` — 14 tests passed.
- `python scripts/test-select-validation.py` — 152 tests passed in 65.84 seconds.
- `bash scripts/ci.sh --mode pr --base e77a351c --head 3512a547b1964e4f8505defc1132e4adb8035cf4` — 26 checks passed in 618 seconds.
- Review-artifact closeout, change-metadata validation, explicit lifecycle
  validation, Bash syntax, and `git diff --check` passed at their recorded
  implementation or review stages.

These results supported implementation review. They are not a claim that the
fresh final `verify` stage has passed.

## Review resolution summary

Nine material findings were recorded, accepted, corrected, and resolved. No
finding is open or marked `needs-decision`. The durable dispositions are in
[`review-resolution.md`](review-resolution.md); the final whole-change review is
[`reviews/code-review-final-r1.md`](reviews/code-review-final-r1.md).

The implementation-specific corrections made canonical missing input fail,
made the public governance owner run the full metadata validator, associated
review paths with their owning change record, and kept release-profile-only npm
publication proof out of ordinary PR acceptance.

## Alternatives rejected

- Keeping the accumulated validation architecture would preserve the ownership
  ambiguity and default orchestration cost.
- Codex-only or all-target runtime smoke was rejected because an LLM session is
  nondeterministic and does not prove package integrity.
- A big-bang script deletion was rejected because active contracts and unknown
  protected failures require classification before removal.
- A new gate framework, selector, cache, or scheduler was rejected by the zero
  admission budget; the implementation extends existing owners.

## Scope control

The change does not alter workflow stage order, publish a release, create a tag,
push, deploy, access target runtimes, certify model behavior, delete historical
evidence, or claim semantic quality from structural checks. It also does not
delete active selector/cache/broad-smoke compatibility implementations.

## Risks and follow-ups

- The direct PR graph favors transparency over changed-path optimization and
  currently takes about ten minutes locally. Future optimization needs measured
  scale evidence and a separately approved exception.
- Compatibility machinery remains code to maintain. Its later deletion requires
  exact active-contract amendments and ledger transitions to `removable` or
  `retired`; this change does not pre-authorize that work.
- Final verification must rerun the direct graph against the current committed
  branch range, validate lifecycle and review closeout, and check derived and
  release safety before PR readiness can be considered.

The implementation and final holistic review are complete. The change is ready
for the `verify` stage, not yet verified or PR-ready.
