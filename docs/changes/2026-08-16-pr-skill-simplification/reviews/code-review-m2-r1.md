# Code Review M2 R1: PR Skill Simplification

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: implementation milestone M2 range `1813c89f..9cd2f225`
Reviewed milestone: M2
Reviewed artifact: commit `9cd2f225`
Review date: 2026-08-16
Status: changes-requested
Material findings: PRSIM-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, its invocation manifest, `review-log.md`, and `review-resolution.md`
- Open blockers: PRSIM-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: PRSIM-CR1
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-16-pr-skill-simplification/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-16-pr-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-16-pr-skill-simplification/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: PRSIM-CR1
- Verify readiness: not-claimed

## Blind-first risk map

The highest-impact risks were lost universal submission safeguards, incomplete verification identity, an authority axis granting an unrelated write, unsafe retry after concurrent remote change, a structural asset acquiring policy, and extraction that reduced navigation while increasing the real loaded profile. Direct inspection covered the canonical diff, contract tests, protected legacy validators, resource inventory, exact operation sequence, and deterministic word/byte assembly.

## Material finding

Finding ID: PRSIM-CR1
Severity: major
Location: `skills/pr/SKILL.md` and `skills/pr/references/governed-pr-readiness.md`
Evidence: The M1 flat baseline is 1,678 words and 11,375 UTF-8 bytes. The reviewed M2 portable profile is 1,524 words and 11,501 bytes, while the governed profile is 1,677 words and 12,697 bytes. R45 requires both PR0 and PR1 words and bytes to decrease. Existing focused tests do not assert this property.
Required outcome: Reduce both procedural assemblies below both baseline values without dropping a semantic-rule or literal disposition, and add a deterministic regression assertion for both profiles.
Safe resolution path: Compact duplicated or verbose universal and governed wording within the two owned PR procedure files, keep protected shared blocks byte-identical, extend `PRSkillSimplificationTests` with LF-normalized profile assertions, rerun the focused and broad skill suites, and rereview the complete M2 diff.
needs-decision rationale: none; the approved spec already settles the required outcome.
auto_fix_class: declared-safe
declared-safe recipe: edit only the two PR procedural files and focused test class; preserve every closed vocabulary, resource trigger, protected block, authority boundary, operation step, stop, claim, and output field; require PR0 and PR1 words and bytes to be strictly lower than baseline.
forbidden paths: verify producer, PR body asset, governing artifacts, lifecycle schema, remote state, generated output.

## Review dimensions

| Dimension | Result | Notes |
| --- | --- | --- |
| Spec alignment | block | R45 is not satisfied by either byte profile. |
| Test coverage | concern | Behavioral assertions pass, but no final profile regression test exists. |
| Edge cases | pass | The static contract covers authority, ancestry, concurrency, partial success, and read-back drift. |
| Error handling | pass | Invalid signals and every closed vocabulary fail closed. |
| Architecture boundaries | pass | Verify remains the basis producer and the governed reference is read-only. |
| Compatibility | pass | Protected repository-wide skill contracts and legacy preparation-only behavior pass. |
| Security/privacy | pass | Force, overwrite, unmanaged section mutation, and unowned external writes are prohibited. |
| Derived artifact currency | pass for M2 | Temporary build checks pass; full distribution parity belongs to M3. |
| Unrelated changes | pass | Multi-target validator support is a bounded compatibility fix for the authored C2 command. |
| Validation evidence | concern | All named M2 commands pass, but they do not yet enforce the failed size requirement. |

## Claim limitations

The published behavior is not rejected, but M2 is not closed until the real loaded profiles satisfy R45 and a targeted rereview approves the correction.
