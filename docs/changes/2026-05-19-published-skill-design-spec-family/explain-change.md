# Explain Change: Published Skill Design Spec Family Rollout

## Summary

This change continues the merged published-skill design contract rollout from
`proposal` / `proposal-review` to the next scoped lifecycle pair: `spec` and
`spec-review`.

The implementation makes those two published skills more portable and
triggerable by moving routing into frontmatter `description`, adding explicit
workflow-role claim boundaries, preserving normal execution behavior, and adding
compact output skeletons. It also records audit, routing, preservation, parity,
token, review, and validation evidence so the rewrite is reviewable instead of
being treated as a prose-only cleanup.

## Problem

Published RigorLoop skills are installed through adapters and may be read in
customer projects that do not have RigorLoop maintainer-only specs, schemas,
reports, proof packs, or generated adapter output. The accepted published-skill
design contract says published skills should be portable operating
documentation: the description routes, the body executes, resources are
explicit, and artifact-producing skills include output expectations.

After the proposal/proposal-review pilot merged, `spec` and `spec-review` were
the next smallest coherent lifecycle pair. They needed the same contract without
rewriting every skill or changing workflow ownership.

## Decision trail

| Decision source | Decision |
| --- | --- |
| Proposal | Continue treating skills as lean, triggerable operating documentation for capable agents. |
| Spec | Preserve R27-R35: description routing, workflow role, execution body, resource/self-containment boundaries, output skeletons, and bounded routing evidence. |
| Test spec | Add T21-T24 for the spec-family rollout: audit, deterministic validation, behavior preservation/parity, generated output, adapter proof, and selected validation. |
| Plan | Scope the rollout to `skills/spec/SKILL.md` and `skills/spec-review/SKILL.md`; do not merge, retire, rename, remove, or change ownership of skills. |
| M1 | Create audit, routing coverage, behavior-preservation, behavior-parity, and baseline token evidence before skill-body rewrites. |
| M2 | Add deterministic regression proof for spec-family evidence; leave production validator logic unchanged because no new validator gap was found. |
| M3 | Rewrite only `spec` and `spec-review`, then record final preservation, parity, token, generated-output, adapter, and selected-CI evidence. |

No architecture artifact or ADR was needed. The change edits canonical skill
text, deterministic tests, and lifecycle evidence; it does not add runtime
components, persistence, APIs, deployment behavior, or hard-to-reverse data
flow.

## Diff rationale by area

| File | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `skills/spec/SKILL.md` | Added readability contract metadata, routing-focused `description`, `Workflow role`, compacted common-path instructions, project-local wording, and fenced output skeleton. | Make `spec` route from frontmatter, preserve authoring behavior, prevent downstream readiness overclaims, and give artifact shape directly in the published skill. | R29-R34, T23, M3. | `validate-skills.py`, `test_skill_readability_spec_family_opts_into_contract`, behavior preservation/parity. |
| `skills/spec-review/SKILL.md` | Added readability contract metadata, routing-focused `description`, `Workflow role`, compact review dimensions, and fenced output skeleton. | Make `spec-review` route reliably while preserving formal review recording, material finding shape, isolation, and downstream handoff limits. | R29-R34, T23, EC18. | `validate-skills.py`, M3 code-review, behavior preservation/parity. |
| `scripts/test-skill-validator.py` | Added spec-family readability opt-in test and changed preservation/parity checks from pending placeholders to final M3 evidence. | Make deterministic tests prove the spec pair satisfies the readability contract and that evidence is complete after M3. | T22-T24. | `python scripts/test-skill-validator.py` passed 111 tests. |
| `docs/changes/.../skill-audit.md` | Recorded the spec-family audit before skill edits. | Establish what gaps existed and why both skills still earn their existence. | T21, M1. | Artifact lifecycle and selected CI passed. |
| `docs/changes/.../routing-coverage.md` | Recorded prompt fixture classes and routing coverage for `spec` and `spec-review`. | Keep routing evidence bounded to fixture/transcript review and avoid runtime auto-selection claims. | R35, T21-T22. | Focused regression checks in `scripts/test-skill-validator.py`. |
| `docs/changes/.../behavior-preservation.md` | Recorded protected behavior and final M3 preservation mapping. | Show where rewritten behavior-significant wording remains preserved. | R36 principles, T23. | M3 code-review found no material issues. |
| `docs/changes/.../behavior-parity.md` | Recorded representative parity artifacts, final parity results, and token deltas. | Prove spec output shape and spec-review recording/claim boundaries were not weakened; keep token regression within the inherited cap. | T23, EC18, EC19. | Token estimates: `spec` 2514, `spec-review` 2183. |
| `docs/changes/.../review-*` | Recorded plan-review, code-review rounds, one material finding resolution, and clean M3 review. | Formal lifecycle reviews require durable evidence. | Workflow/review recording contract. | `validate-review-artifacts.py --mode closeout` passed. |
| `docs/plans/2026-05-19-published-skill-design-spec-family.md` and `docs/plan.md` | Kept active milestone state, decisions, validation notes, and current handoff synchronized. | The active plan owns current state for planned initiatives. | Plan policy and milestone-aware workflow. | Artifact lifecycle validation and selected CI passed. |
| `docs/changes/.../change.yaml` | Recorded requirements, changed files, validation commands, review status, and current evidence locations. | Maintain compact change metadata for validation and downstream handoff. | Docs-changes baseline pack. | `validate-change-metadata.py` passed. |

## Tests added or changed

| Test | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `test_published_design_spec_family_routing_coverage_fixture_is_bounded` | Routing fixtures cover positives, near negatives, competing skills, and should-not-trigger classes without claiming runtime auto-selection. | Static fixture checks match the approved deterministic oracle boundary. |
| `test_published_design_spec_family_audit_records_deterministic_gaps` | Audit evidence records the deterministic spec-family gaps before skill rewrite. | The audit is a Markdown evidence artifact, so static content checks are sufficient. |
| `test_published_design_spec_family_preservation_and_parity_are_scaffolded` | Preservation/parity evidence exists and, after M3, no longer contains pending placeholders. | This prevents closing M3 on structural validation alone. |
| `test_skill_readability_spec_family_opts_into_contract` | `spec` and `spec-review` validate successfully and include readability contract metadata, workflow role, and output skeletons. | This directly covers the skill-body contract without broad semantic scoring. |

## Validation evidence available before final verify

Recorded validation includes:

- `python scripts/test-skill-validator.py` passed 111 tests.
- `python scripts/validate-skills.py` passed for 23 canonical skills.
- `python scripts/measure-skill-tokens.py --skills-root skills` recorded `spec` at 2514 estimated tokens and `spec-review` at 2183.
- `python scripts/build-skills.py --check` passed.
- `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/tmp.DvrRLm2pYe` built temporary adapter archives.
- `python scripts/validate-adapters.py --root /tmp/tmp.DvrRLm2pYe --version v0.1.5` passed.
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-published-skill-design-spec-family` passed.
- `python scripts/validate-change-metadata.py docs/changes/2026-05-19-published-skill-design-spec-family/change.yaml` passed.
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` passed for the touched lifecycle artifacts.
- `git diff --check -- ...` passed for the touched paths.
- Selected CI passed for skill validation, skill regression, skill generation regression, skill drift, adapter drift, review artifacts, artifact lifecycle, change metadata regression, and change metadata validation, depending on the changed path set.

One selected CI run failed during M3 because a regression test still expected
`pending M3` preservation rows after M3 filled final evidence. The test was
updated to require final M3 preservation/parity evidence, and the selected CI
rerun passed.

This is not final verification. Final `verify` still owns the complete
pre-PR verification decision.

## Review resolution summary

One material finding was recorded and resolved:

| Finding | Disposition | Result |
| --- | --- | --- |
| `SF-M2-CR1` | accepted | The active plan Current Handoff Summary was corrected so M2 routed back to rerun `code-review` instead of another implementation pass. |

Resolution is recorded in
`docs/changes/2026-05-19-published-skill-design-spec-family/review-resolution.md`.

M1, M2 rerun, and M3 code reviews closed cleanly with no unresolved material
findings. The review log records all formal review events.

## Alternatives rejected

| Alternative | Why not chosen |
| --- | --- |
| Rewrite all skills in one pass | The accepted rollout is intentionally incremental; broad rewrite would increase review risk and token-cost churn. |
| Change production validator logic in M2 | M1 found no new deterministic production validator gap; evidence checks were enough for this slice. |
| Add runtime model auto-selection tests | The approved oracle boundary forbids CI claims about deterministic runtime skill selection without a dedicated harness. |
| Add `when_to_use` as required metadata | The contract keeps portable routing in `description`; optional adapter metadata must not replace it. |
| Hand-edit generated adapter bodies | `skills/` is the authored source; adapter proof uses temporary generated output and validation. |

## Scope control

The rollout stayed inside the approved scope:

- changed skill bodies are limited to `skills/spec/SKILL.md` and `skills/spec-review/SKILL.md`;
- no skills were merged, retired, renamed, removed, or reassigned;
- no broad semantic prose scoring or runtime skill-selection oracle was added;
- no adapter install roots, lockfile behavior, CLI behavior, schemas, or release archive trust boundaries changed;
- generated public adapter skill bodies were not hand-edited.

## Risks and follow-ups

Remaining work is workflow closeout, not implementation:

- run final `verify`;
- prepare PR handoff after verification passes;
- rely on future transcript review to identify over-triggering, under-triggering, or unnecessary resource loading in real use.

No open implementation blockers are recorded. The active plan remains active
because final `verify` and `pr` handoff have not completed.

## Readiness

Ready for `verify`.

This explanation does not claim final verification, branch readiness, PR body
readiness, PR open readiness, or hosted CI final status.
