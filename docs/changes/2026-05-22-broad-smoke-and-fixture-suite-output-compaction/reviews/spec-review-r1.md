# Spec Review R1

Review ID: spec-review-r1
Stage: spec-review
Round: 1
Reviewer: Codex spec-review
Target: specs/script-output-optimization.md
Status: changes-requested

## Review inputs

- Spec: `specs/script-output-optimization.md`
- Related proposal: `docs/proposals/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`
- Proposal review: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/proposal-review-r2.md`
- Change metadata: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`
- Direct compatibility check: `python scripts/test-change-metadata-validator.py --quiet`

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: `SRO-BSO-SR1`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-log.md`
- Review resolution: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/review-resolution.md`
- Open blockers: `SRO-BSO-SR1`
- Immediate next stage: spec revision

## Findings

### SRO-BSO-SR1 - `--quiet` compatibility claim contradicts current producer behavior

Finding ID: SRO-BSO-SR1
Severity: major
Location: `Error and boundary behavior`, `EC21`, `Non-goals`, `R60`
Evidence: The spec says `scripts/test-change-metadata-validator.py --quiet` remains unsupported unless a later approved spec amendment adds quiet behavior, and EC21 says the command follows its normal unsupported-argument behavior. A direct compatibility check showed `python scripts/test-change-metadata-validator.py --quiet` exits `0`, writes no stdout, and writes the normal unittest quiet success summary to stderr: `Ran 18 tests ... OK`.
Required outcome: The spec must not claim `--quiet` is unsupported for `scripts/test-change-metadata-validator.py` unless the change intentionally removes or rejects a currently accepted invocation and documents that compatibility break.
Safe resolution path: Choose one contract before test-spec work: either make `--quiet` behavior in scope for `scripts/test-change-metadata-validator.py` and define quiet success/failure requirements, or explicitly preserve the existing unittest `--quiet`/`-q` behavior as compatibility while stating that compact custom quiet formatting is out of scope for this slice. Update R60, EC21, Non-goals, and acceptance criteria accordingly.

## Review Dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | Most requirements are precise, but the `--quiet` producer boundary contradicts current behavior. |
| normative language | concern | R60's "MUST NOT add" is acceptable, but the surrounding unsupported-behavior language is inaccurate. |
| completeness | pass | Broad-smoke capture, aggregate success, failure evidence, producer output, and preservation proof are covered. |
| testability | concern | The `--quiet` boundary would drive tests toward a false unsupported-argument expectation. |
| examples | concern | EC21 needs revision to match the selected compatibility contract. |
| compatibility | block | The spec currently misstates an already accepted producer invocation. |
| observability | pass | Output, failure evidence, command/test identity proofs, and wrapper consistency evidence are observable. |
| security/privacy | pass | Captured output privacy and no persistent log storage are covered. |
| non-goals | concern | The non-goal should distinguish not adding custom quiet formatting from not supporting an already accepted flag. |
| acceptance criteria | concern | Acceptance criteria need a `--quiet` compatibility criterion if existing behavior remains out of custom-format scope. |

## Eventual test-spec readiness

Not ready until `SRO-BSO-SR1` is resolved.

## Stop condition

Stop before focused test-spec amendment or planning reliance. The producer `--quiet` compatibility contract must be corrected in the spec first.
