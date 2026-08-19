<!-- explain-change-skeleton-v1; normative -->

# Change explanation: CI-Maintenance Skill Simplification

Stage: explain-change
Status: current
Final diff identity: sha256:84cb3bf469ff62a20a1e0f5bcab59b22686f12591b29d539c5896c20afd40439
Final review identity: code-review-final-r1 / sha256:0e196257c9c87d6176a883c05346cb64f422ee768a88324b5a095a4577cf2c6d
Reviewed subject revision: 5ca6e8333f2f8692b3f88aa8cbbe2e7f756dc19a
Base revision: afb4937bd0874286f6c260dbd58cd10a088b0986
Final-review recording revision: 4d8421602c3a18dfe5f195609b29dd340fd935a0

## Summary

The CI-maintenance skill now uses a compact universal contract, one conditional GitHub-authoring reference, the existing risk-to-check map as the sole semantic placement owner, and a minimal workflow skeleton. Narrow reviews no longer load authoring, coverage, cache, boundary, or privileged procedure that they do not need, while all supported assemblies retain explicit authority, safety, failure, and claim limits.

The implementation also closes the mutation paths that made simplification risky: privileged workflow changes require exact approved design evidence; creation cannot clobber a concurrently created target; revision cannot replace a changed identity; and dependent multi-file requests prepare and validate a complete graph before committing only safe intermediate states.

## Problem

The former flat skill mixed universal review safety with GitHub serialization, risk placement, privileged examples, and broad workflow structure. That made ordinary review expensive to load and allowed the skeleton and authoring procedure to imply policy that should come from project evidence. Its generic atomic-replacement wording also did not distinguish no-clobber creation from identity-guarded revision or define dependency-aware partial completion.

## Decision trail

- The accepted proposal selected a compact root, one GitHub authoring reference, the existing risk map, one reduced skeleton, and no scripts or runtime engine.
- Approved spec R1-R54 defines the independent classification axes, ownership boundaries, privileged approved-design assembly, conditional commits, dependency-aware batches, result truthfulness, compatibility, and reduction gates.
- The architecture assessment concluded `architecture-not-required` because the design reuses packaged resources, repository files, and transient file primitives without new persistence or external-state ownership.
- Plan M1-M4 froze preservation contracts, extracted the package, proved mutation safety, and measured every assembly before the final holistic review.
- `code-review-final-r1` reviewed the complete branch and found no material defects.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/ci-maintenance/SKILL.md` | Replaced the flat procedure with a compact universal classification, authority, mutation, result, and resource-routing contract. | Keep fail-safe decisions inline while reducing irrelevant common-path loading. | R1-R14, R24-R44 | Focused simplification tests; M2 and M3 evidence |
| `references/risk-to-check-map.md` | Made the map the sole owner of risk, check, command, and execution-boundary placement. | Prevent the map and GitHub authoring procedure from independently choosing PR-versus-boundary policy. | R15-R20 | `test_risk_map_owns_semantic_placement`; semantic-preservation review |
| `references/github-workflow-authoring.md` | Added conditional ordinary composition and exact approved-design realization procedure. | Serialize settled GitHub policy without inventing commands, coverage, or privilege. | R11-R20, R25-R28 | Package/resource tests and CIM8 scenarios |
| `assets/github-workflow-skeleton.yml` | Removed built-in PR, push, schedule, manual, cache, secret, OIDC, runner, and deployment examples. | Make the asset structural and least-privilege by default instead of a hidden policy source. | R21-R23 | Skeleton validator and forbidden-content regression test |
| `scripts/skill_validation.py` and `scripts/test-skill-validator.py` | Updated package validation and added closed-axis, resource, concurrency, batch, compatibility, and size proofs. | Fail closed on missing resources and unsafe examples while proving the accepted contracts deterministically. | R45-R54 | 13 focused tests and the complete skill-validator suite |
| Focused and legacy specs | Added the complete simplification contract and amended five overlapping legacy clauses. | Preserve all unlisted legacy requirements while giving changed ownership and safety rules one normative source. | R54; AC1-AC16 | Boundary validator, rule/literal ledgers, independent reviews |
| Change-local fixtures and evidence | Recorded T1-T15, ownership inventories, baseline counts, semantic dispositions, milestone proof, and formal reviews. | Make semantic preservation and simplification measurable and reviewable rather than inferred from a shorter root file. | Test spec and plan M1-M4 | Review log, review resolution, and evidence files |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| T1-T5, T11-T15 | Closed axes, assemblies, privilege, resource safety, hosted-CI claims, compatibility, and package reduction. | contract/integration |
| T6-T8 | Commit-time no-clobber, identity-guarded revision, and read-back boundaries. | contract |
| T9-T10 | Dependency ordering, cycle/atomic-group stop, exact partial results, and fresh retry. | contract/integration |
| Validator regressions | Minimal skeleton invariants, packaged reference discovery, unknown-value policy, and all-profile size gates. | automated regression |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `python scripts/test-skill-validator.py CiMaintenanceSkillSimplificationTests` | 13 passed | reviewed subject `5ca6e833` |
| `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md` | passed | reviewed subject `5ca6e833` |
| `python scripts/test-skill-validator.py` | 432 passed, 16 skipped | reviewed subject `5ca6e833` |
| `python scripts/test-build-skills.py` and `python scripts/build-skills.py --check` | passed | reviewed subject `5ca6e833` |
| `python scripts/test-adapter-distribution.py` | passed | reviewed subject `5ca6e833` |
| Boundary, metadata, prose, review-closeout, and diff checks | passed | final-review recording `4d842160` |

## Review resolution summary

Two material findings have accepted and resolved dispositions, with no open findings: specification finding `CIMSIM-SR1` and implementation finding `CIMSIM-CR1`. See [review-resolution.md](review-resolution.md) for their evidence and closeout. Final holistic review `code-review-final-r1` found no new material finding.

## Alternatives rejected

Keeping the flat skill would not reduce real loaded profiles. A catch-all reference would preserve mixed ownership, while many small references would add routing and parity risk. A workflow generator, policy engine, YAML ownership parser, persistent mutation receipt, provider-neutral abstraction, or external platform integration would create new architecture and acceptance surfaces beyond the selected repository-file refactor.

## Scope control

The change does not execute hosted workflows, open a live PR, mutate external platform state, invent project validation commands, design privileged policy, add a runtime helper, migrate historical workflows, or introduce persistent locking or transaction state. It changes only the CI-maintenance package, directly coupled validators/tests/contracts, and lifecycle evidence.

## Risks and follow-ups

The principal residual risk is future CI capability expanding beyond repository-file targets or requiring resumable cross-process coordination. Such work must stop and return to architecture instead of extending this package implicitly. All current assemblies are below baseline, but later shipped-text changes must rerun the deterministic word/byte gates so root shrinkage cannot hide total-package growth.

## Workflow handback

Explanation status: current
Explanation basis: sha256:b4f31ef9d016595fff0a39a523bc7cfcce3c149bad0e1f38519df0beaad5b1cd
Validation-evidence cutoff: final-review-recording:4d8421602c3a18dfe5f195609b29dd340fd935a0
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
