# Explain Change: PR Skill Simplification

## Summary

This change makes the published `pr` skill smaller on both real procedural
paths while preserving its external-action safety. The flat skill became a
compact universal contract plus one conditionally loaded governed-readiness
reference and one copied PR-body skeleton. `verify` now emits the exact
immutable repository/base/head tuple that `pr` must consume before opening or
changing a pull request.

The change does not open a PR, run a target-agent acceptance journey, add a host
provider engine, add a Markdown section parser, or move `branch-ready`
ownership out of `verify`.

## Problem

The prior `skills/pr/SKILL.md` mixed universal Git and external-operation safety
with RigorLoop-specific change-pack aggregation and repeated PR-body layout.
That made every portable invocation load governed procedure, while its prose
did not completely close preparation side effects, draft/open transitions,
base-revision staleness, or safe body refresh.

## Decision trail

- The accepted proposal selected a compact universal file, one read-only
  governed-readiness reference, and one structural asset.
- R1-R41 define package ownership and preserved submission behavior. R42-R47
  require deterministic semantic, literal, measurement, and package proof.
  R48-R49 bound architecture escalation and published portability.
- The bounded architecture assessment concluded `architecture-not-required`
  because the change reuses the existing packaged-resource, verify-evidence,
  Git/host, and adapter-distribution owners.
- M1 froze 24 rules, 25 literals, seven verification-basis fields, 18 operation
  scenarios, and the 1,678-word/11,375-byte flat baseline. Final verification
  exposed five omitted shared review-closeout literals; the correction added
  them to the ledger instead of rewriting M1's historical result.
- M2 implemented the package and verify-producer amendment. Its first review
  found real loaded-byte growth (`PRSIM-CR1`); the accepted correction compacted
  PR0 and PR1 and added a strict regression assertion.
- M3 proved final semantic disposition, boundary coverage, measured reduction,
  and generated-through-installed package parity.
- Verify R1 then exposed a review-summary compatibility regression that the
  focused suite and original literal inventory had missed. The correction
  restored all five adjacent shared phrases inline, added a failing-first
  regression test, refreshed the affected evidence, and received a clean R2
  final rereview.
- The next PR-mode CI attempt passed that contract but found three historical
  review records whose facts were not discoverable under the current parser
  shape. The correction added current receipt headers and normalized two
  finding blocks without changing any judgment, disposition, or settlement;
  focused lifecycle validation and final code review R3 are clean.

## Diff rationale by area

| File or area | Change | Reason and governing source | Test or evidence |
| --- | --- | --- | --- |
| `skills/pr/SKILL.md` | Replaced the flat procedure with compact universal classifications, safety, ordered remote operations, result claims, stops, and resource triggers. | R1-R4 and R8-R41 keep universally required behavior inline while separating independent authorities and exact base/head readiness. | T-PR-001 through T-PR-017; focused `PRSkillSimplificationTests`. |
| `skills/pr/references/governed-pr-readiness.md` | Added one read-only change-pack aggregation procedure. | R2, R5-R7 require governed lifecycle evidence only after one exact candidate is identified, without granting mutation authority. | T-PR-003, T-PR-004, and governed-reference assertions. |
| `skills/pr/assets/pr-body-skeleton.md` | Added one structure-only body template with core and conditional groups. | R3-R4 and R41 give repeated labels and ordering one owner while leaving applicability and adequacy in procedure. | T-PR-001, T-PR-002, T-PR-017. |
| `skills/verify/SKILL.md` and `references/branch-readiness-verification.md` | Added the seven-field normalized immutable `verification_basis`. | R24-R30 keep `verify` as producer and let `pr` validate repository, remote, base, merge base, head branch, and subject identities without inference. | T-PR-012 through T-PR-014. |
| `scripts/test-skill-validator.py` | Added focused package/contract tests, direct PR0/PR1 size assertions, and a regression test for the shared review-resolution summary contract. | The approved test spec requires closed vocabularies, failure paths, compatibility, and real loaded-profile reduction; verify R1 showed the original focused suite did not cover five adjacent normative phrases. | C1; 13 focused and 386 broad tests after correction. |
| `scripts/validate-skills.py` | Made explicit target arguments repeatable while retaining the no-argument default. | The authored C2 command validates both directly coupled skill targets in one invocation. | `test_gate_a_accepts_multiple_explicit_targets`; C2. |
| Change-local ledgers and fixtures | Recorded rule/literal/basis ownership, deterministic scenarios, baseline, final-profile validation, and the five literals discovered by verify R1. | R42-R45 require change-local preservation evidence rather than accidental prose or test ownership. | C0, `semantic-preservation-review.md`, and `evidence/verify-r1-correction.md`. |
| Proposal, spec, plan, test spec, reviews, and lifecycle evidence | Recorded the accepted direction, contract, proof plan, staged execution, finding correction, and clean reviews. | The stage-owned workflow requires durable reasoning and evidence for non-trivial published-skill changes. | Proposal/spec/plan/test-spec reviews; M1-M3 and final code reviews. |

## Tests added or changed

`PRSkillSimplificationTests` maps T-PR-001 through T-PR-020 to static contract
proof. It covers the exact resource inventory, policy-free asset, tri-state
governed signals, missing resources, zero-write preparation, independent
authorities, byte-preserving body behavior, directional ancestry, PR-state and
CI vocabularies, verify basis, evidence tail, external rereads, concurrency,
read-back, claims, and real profile size.

The change-local C0 validator proves all frozen ledger and scenario families are
nonempty, closed, and consistent. Existing build and adapter suites remain the
appropriate integration level for generated, archived, release-candidate, and
clean-installed resource parity. A live PR would be nondeterministic and would
cause an unnecessary external side effect, so it is intentionally excluded.

## Validation evidence available before final verify

| Command | Observed result |
| --- | --- |
| C0 change-local preservation validator | passed: 24 rules, 30 literals, seven basis fields, 18 scenarios, two profiles |
| `python scripts/test-skill-validator.py PRSkillSimplificationTests` | 13 passed |
| `python scripts/test-review-artifact-validator.py` | 103 passed |
| `python scripts/validate-skills.py skills/pr/SKILL.md skills/verify/SKILL.md` | passed for both targets |
| `python scripts/test-skill-validator.py` | 386 passed, 16 skipped |
| `python scripts/test-build-skills.py` | seven passed |
| `python scripts/build-skills.py --check` | passed |
| `python scripts/test-adapter-distribution.py` | 150 passed |
| boundary-first validation for the feature spec | passed |
| change-metadata validation | passed through the latest reviewed lifecycle transition |
| PR-scope artifact lifecycle validation after historical-record normalization | passed; three change-local artifact files validated, with repository baseline warnings only |

Final `verify`, repository CI orchestration, hosted CI, `branch-ready`, and PR
readiness are not claimed here.

## Review resolution summary

The durable [review resolution](review-resolution.md) is closed: ten material
findings were accepted and resolved, none were rejected, deferred, partially
accepted, or left as `needs-decision`, and `review-log.md` has no open findings.
The implementation-specific `PRSIM-CR1` correction reduced both actual loaded
profiles and passed an independent rereview. The verify-R1 compatibility
correction restored the complete shared review-summary contract and passed
`code-review-final-r2`. The subsequent evidence-only receipt normalization
passed `code-review-final-r3`. M1-M3 and the corrected complete branch each
have a clean recorded code review.

## Alternatives rejected

- Inline-only compression left governed procedure and repeated body structure
  on every path.
- Multiple narrow references increased navigation without another genuine
  activation boundary.
- Section-level Markdown refresh required an ownership/parser protocol that
  could overwrite reviewer-authored text.
- A PR provider engine or durable external transaction artifact would expand
  architecture and persistence scope.
- Live acceptance PRs and target-agent runtime journeys were unnecessary for a
  deterministic content/package refactor.

## Scope control

The change does not settle lifecycle artifacts, route workflow from `pr`, merge,
release, publish, assign reviewers or labels, change deployment behavior, or
optimize `verify` beyond its directly coupled normalized evidence output. It
does not hand-edit generated adapter packages.

## Risks and follow-ups

The main residual risk is semantic compression: future edits could move
universal external-operation safety behind the governed trigger. The focused
tests, rule ledger, protected claim boundaries, and loaded-profile assertions
make that drift visible. The PR package grows overall because the reusable asset
and reference now exist; this is explicitly reported, while both actual
procedural profiles are smaller.

The reviewed change is ready to enter final `verify`. PR preparation remains a
separate stage and is outside the current automation target.
