# M4 package-readiness evidence

## Candidate identity

| Identity | Value |
| --- | --- |
| Source parent | `19d49e1eff94d97bcf9a22940f2a5e16b3ce1445` |
| Resource manifest SHA-256 | `6741b88ec84c392f5c41829203d24bb2044a526f7662cf2d01063358bfae4113` |
| Canonical source inventory SHA-256 | `4268fbe89ecdfd7b79ca1321b8d6b19b2ed24e8adeda17cae8c319b087760f6f` |
| Projection-set SHA-256 | `68c6f88c313f706e7011a0e6b7b6625b82464bd3287c15d4fc5b3b7a3a004329` |
| Projection count | 14 |
| Adapter support version | `v0.1.5`, read from `dist/adapters/manifest.yaml` |
| Repository activation state | `pending` |

The implementation commit binds this evidence to the candidate changes. No active claim is made.

## Loading measurements

Measurements record current raw canonical resource bytes. They are baselines, not budgets or pass/fail thresholds.

| Skill family | Representative skills | Mapped | Initially loaded | Expanded |
| --- | --- | --- | --- | --- |
| Routing and downstream | workflow, plan, plan-review, implement, code-review, verify | 1 / 6,346 bytes | 0 / 0 bytes | 1 / 6,346 bytes |
| Feature authoring and review | spec, spec-review | 2 / 8,670 bytes | 2 / 8,670 bytes | 2 / 8,670 bytes |
| Proof authoring and review | test-spec, test-spec-review | 2 / 8,651 bytes | 2 / 8,651 bytes | 2 / 8,651 bytes |

The closed loading fixture covers all ten governed skills. Unknown schema, skill, resource, or manifest mapping fails before measurement.

## Derived package proof

- Canonical resources match all 14 skill-local projections.
- Generated skill output is rebuilt and checked only in a temporary directory.
- Codex, Claude, and opencode `v0.1.5` archives were built in a temporary release-output directory.
- Clean-install smoke validated all ten governed skills for every supported adapter.
- Archive inspection compares every consumer-mapped compact, feature-authoring, and proof resource to canonical raw bytes.
- Layer-specific compact, feature-authoring, and proof mutations each fail with the exact mapped path and canonical/archive hashes.
- Runtime fallback is not used as package evidence; archive and installed bytes are inspected directly.
- No external runtime or hosted service is required by this proof, so no unavailable external-tool result was converted into success.

## Activation and rollback proof

The 63-test boundary suite proves:

- the repository-live pending record passes and remains pending;
- isolated active manifests require the complete parent inventory, adjacent immutable activating and rollback releases, current adapter metadata, and coherent projection identities;
- older, missing, mixed, incomplete, or rewritten rollback metadata fails without mutation;
- mixed projection bytes fail even when their inventory digest is recomputed;
- the active validation CLI emits the authoritative immutable rollback selection.

The 28-test projection suite proves repeated projection identity, handled interruption restoration, input-drift restoration, descriptor-contained recovery, and deterministic retry. Before activation, reverting the tracked candidate and discarding temporary derived output restores one coherent pending bundle; no accepted artifact is rewritten.

## Validation

| Command | Result |
| --- | --- |
| `python scripts/test-boundary-first-reference.py` | pass, 28 tests |
| `python scripts/test-boundary-first-validation.py` | pass, 63 tests |
| `python scripts/validate-boundary-first.py --check` | pass, state `pending` |
| `python scripts/test-skill-validator.py` | pass, 282 tests with 16 documented skips |
| `python scripts/validate-skills.py` | pass, 24 skills |
| `python scripts/build-skills.py --check` | pass with temporary output |
| `python scripts/test-adapter-distribution.py` | pass, 134 tests |
| Planned `build-adapters.py` plus `validate-adapters.py --clean-install-smoke` command | pass for all ten governed skills and three adapters |
| `bash scripts/ci.sh --mode broad-smoke` | pass, 11 checks in 310 seconds |
| `git diff --check` | pass |

## Containment

Generated skills, archives, and installed trees remained temporary and untracked. The live activation manifest was not edited and remains `pending`.
