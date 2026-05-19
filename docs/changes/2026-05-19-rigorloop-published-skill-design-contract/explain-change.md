# Explain Change: RigorLoop Published Skill Design Contract

## Summary

This change makes RigorLoop's published skill contract explicit and proves it on the `proposal` and `proposal-review` pilot pair.

The implementation adds an audit-first evidence pack, deterministic validator checks and fixtures for the published-skill design rules, narrowly updates the two pilot skills, records behavior-preservation and behavior-parity proof, and validates generated skill and adapter output from canonical `skills/`.

## Problem

Published RigorLoop skills are installed through adapter packages. Users of those packages may not have this repository's internal specs, schemas, scripts, reports, or change-local proof packs. The accepted proposal identified that a skill must therefore be portable operating documentation: it must route from frontmatter `description`, execute from `SKILL.md`, load packaged resources only when mapped, avoid maintainer-only dependencies, and preserve lifecycle claim boundaries.

## Decision Trail

| Source | Decision |
| --- | --- |
| Proposal | Treat published skills as lean, triggerable operating documentation for capable agents. |
| Proposal-review | Preserve `specs/skill-contract.md` as the single normative source, distinguish repository-root internals from packaged resources, keep merge/retire work out of the pilot, and bound routing tests to fixture/transcript evidence. |
| Spec | Added R27 through R36 to `specs/skill-contract.md` for published-skill portability, description routing, workflow role, resource maps, self-containment, routing evidence, token budget, and preservation/parity proof. |
| Test spec | Added T16 through T20 to map the new requirements to audit evidence, static validator checks, routing fixtures, behavior parity, token measurement, and generated-output validation. |
| Plan | Split implementation into M1 audit/evidence scaffold, M2 validator/fixture support, and M3 pilot skill rewrite plus generated-output validation. |
| Reviews | Proposal review, spec review, plan review, M1 code review, M2 rerun review, and M3 code review are recorded. All material findings are resolved in `review-resolution.md`. |

Architecture was not required because the change affects Markdown contracts, canonical skill bodies, validation scripts, fixtures, and generated-output validation evidence. It does not add runtime components, persistence, APIs, deployment behavior, or hard-to-reverse data flow.

## Diff Rationale By Area

| File or area | Change | Reason | Source artifact | Test/evidence |
| --- | --- | --- | --- | --- |
| `docs/proposals/2026-05-19-rigorloop-published-skill-design-contract.md` | Recorded accepted proposal direction and proposal-review fixes. | Establish the product and workflow rationale before changing the spec. | Proposal, `proposal-review-r1`, `proposal-review-r2` | Review artifacts and change metadata validation. |
| `specs/skill-contract.md` | Added the published-skill design contract R27-R36. | Make the contract normative in the existing skill-contract source instead of creating a competing spec. | R27-R36, SKC review findings | Spec-review R3 approved. |
| `specs/skill-contract.test.md` | Added T16-T20 and aligned adapter validation proof to temporary `v0.1.5` archives. | Map every new `MUST` to concrete static, manual, or generated-output proof. | R27-R36, plan M3 | `python scripts/test-skill-validator.py`; selected CI. |
| `docs/changes/.../skill-audit.md` | Audited skills and recorded pilot-scope findings. | Satisfy audit-first scope and prevent merge/retire side effects in this pilot. | R36a-R36e, M1 | M1 code-review clean. |
| `docs/changes/.../routing-coverage.md` | Added routing coverage tables and prompt fixture classes for `proposal` and `proposal-review`. | Provide deterministic routing evidence without claiming runtime skill auto-selection. | R35e-R35g, T19 | M1/M2 validation and code review. |
| `scripts/skill_validation.py` and `scripts/test-skill-validator.py` | Added deterministic checks for description length/routing source, resource maps, self-containment, routing coverage, and command-context repository-root scripts. | Make the checkable parts of R29/R32/R33/R35 enforceable without broad semantic scoring. | R29, R32, R33, R35, M2 | `python scripts/test-skill-validator.py` passed 107 tests. |
| `tests/fixtures/skills/published-design/` | Added positive and negative fixtures for description cap, `when_to_use`, resource maps, packaged scripts, and repository-root script dependencies. | Prove validator behavior with stable fixtures, including the `Run scripts/...` regression from code review. | T17-T19, RLSDC-M2-CR1 | Targeted fixture checks and full skill-validator regression passed. |
| `skills/proposal/SKILL.md` | Rewrote the frontmatter `description` to include capability, trigger contexts, and near misses; added `must_not_claim` to `Workflow role`. | Make `description` the portable routing surface and make downstream claim boundaries explicit. | R29, R30, T17, T18 | `python scripts/validate-skills.py`; M3 behavior-parity evidence. |
| `skills/proposal-review/SKILL.md` | Rewrote the frontmatter `description` with review trigger contexts and competing-skill boundaries; added `must_not_claim` to `Workflow role`. | Route review requests before the body loads and prevent spec, implementation-review, verify, branch-ready, PR-ready, or automatic handoff claims. | R29, R30, T17, T18 | `python scripts/validate-skills.py`; M3 behavior-parity evidence. |
| `docs/changes/.../behavior-preservation.md` | Filled preservation notes for rewritten descriptions and workflow-role additions. | Show behavior-significant wording was moved or sharpened without weakening essential rules. | R36g-R36h, T20 | M3 code-review clean. |
| `docs/changes/.../behavior-parity.md` | Filled parity rows and token-cost evidence. | Prove material review status, finding format, recording obligations, stop conditions, validation obligations, and claim boundaries were not weakened. | R36f, R36i-R36j, T20 | `proposal` +2.1%, `proposal-review` +2.0%, both within +5% tolerance. |
| Plan, plan index, review log, review resolution, change metadata | Kept milestone state, review recording, validation evidence, and handoffs current. | Preserve lifecycle traceability and avoid chat-only status. | AGENTS.md workflow rules, active plan | Review artifact, metadata, lifecycle, whitespace, and selected CI checks passed. |

## Tests Added Or Changed

| Test or proof | What it proves | Why this level is appropriate |
| --- | --- | --- |
| `scripts/test-skill-validator.py` published-design cases | Deterministic validator behavior for description cap, routing-source boundary, resource maps, packaged scripts, and repository-root dependencies. | The approved slice is static skill contract validation, not runtime workflow routing. |
| `tests/fixtures/skills/published-design/required-root-script-command` | Imperative `Run scripts/...` wording is rejected as a required repository-root dependency. | Direct regression proof for `RLSDC-M2-CR1`. |
| `tests/fixtures/skills/published-design/packaged-script-resource-map` | Skill-local packaged scripts remain allowed when mapped with inputs, outputs, and failure behavior. | Proves the validator is not a blunt `scripts/` deny-list. |
| `docs/changes/.../routing-coverage.md` | Prompt classes cover positives, near negatives, competing skills, and should-not-trigger cases. | R35 allows fixture/transcript evidence and forbids unsupported deterministic auto-selection claims. |
| `docs/changes/.../behavior-preservation.md` | Rewritten wording preserves essential behavior and names where rules now live. | Required by R36g-R36h for behavior-significant skill edits. |
| `docs/changes/.../behavior-parity.md` | Pilot edits do not weaken lifecycle review status, finding format, recording, stop conditions, validation, or claims. | Required by R36i-R36j; structural validation alone is insufficient. |

## Validation Evidence Available Before Final Verify

Implementation validation recorded in the plan and change metadata includes:

- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/measure-skill-tokens.py --skills-root skills`
- `python scripts/build-skills.py --check`
- `python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-rlsdc-m3-adapters-u7D5LL`
- `python scripts/validate-adapters.py --root /tmp/rigorloop-rlsdc-m3-adapters-u7D5LL --version v0.1.5`
- `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-19-rigorloop-published-skill-design-contract`
- `python scripts/validate-change-metadata.py docs/changes/2026-05-19-rigorloop-published-skill-design-contract/change.yaml`
- `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`
- `git diff --check -- ...`
- `bash scripts/ci.sh --mode explicit ...`

The M3 plan originally listed stale adapter validation commands for repository-tree adapter output and version `0.1.4`. M3 recorded those failures and replaced them with the current temporary `v0.1.5` release-archive validation path, matching the tracked `dist/adapters/manifest.yaml` and the repository rule that `v0.1.3` and later do not track expanded public adapter skill bodies.

## Review Resolution Summary

`review-resolution.md` is closed.

| Review class | Material findings | Disposition |
| --- | ---: | --- |
| Proposal review | 4 | accepted and resolved |
| Spec review | 4 | accepted and resolved |
| Code review | 1 | accepted and resolved |

Clean reviews after resolution:

- `proposal-review-r2`
- `spec-review-r3`
- `plan-review-r1`
- `code-review-m1-r1`
- `code-review-m2-r2`
- `code-review-m3-r1`

No material findings remain open.

## Alternatives Rejected

| Alternative | Reason rejected |
| --- | --- |
| Create a new permanent `specs/rigorloop-published-skill-design-contract.md` | Would risk competing with the existing normative `specs/skill-contract.md`. |
| Rewrite all skills in one PR | Too much behavior risk; the accepted plan is audit-first and pilot-scoped. |
| Use runtime model auto-selection tests as CI proof | No approved deterministic routing harness exists. |
| Ban every `scripts/` mention in published skills | Would incorrectly reject packaged skill-local scripts. |
| Hand-edit generated adapter output | Generated public adapter bodies are not tracked source for current adapter releases; validation must derive output from canonical `skills/`. |

## Scope Control

The change preserves the accepted non-goals:

- no adapter install-root, archive verification, lockfile, or CLI behavior change;
- no new build-time include system;
- no retroactive rewrite of legacy adapter archives;
- no skill merge, retirement, rename, removal, or ownership change;
- no broad semantic scoring for skill prose;
- no all-skill rewrite.

The only skill body edits in the pilot are `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md`.

## Risks And Follow-Ups

Residual risks:

- Routing proof is still static and transcript-review oriented until a future approved routing harness exists.
- The command-context validator is intentionally bounded; future same-class phrasings may need additional fixtures.
- The broader skill catalog still needs follow-on rollout after this pilot.

Follow-ups remain outside this change unless separately proposed:

- build-time partials/includes if source duplication becomes costly;
- skill conformance scoring across adapters;
- transcript-based skill evaluation harness;
- skill retirement/merge policy if future audits justify it.

## Readiness

This explanation completes the `explain-change` stage for the current implemented and reviewed milestones.

Next stage: `verify`.

This artifact does not claim final verification, branch readiness, PR readiness, or hosted CI final status.
