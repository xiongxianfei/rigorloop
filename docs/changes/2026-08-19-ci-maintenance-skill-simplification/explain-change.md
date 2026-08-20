<!-- explain-change-skeleton-v1; normative -->

# Change explanation: CI-Maintenance Skill Simplification

Stage: explain-change
Status: current
Final diff identity: sha256:f8dd95c4e7cc4fb20ea95cd7c9e2584e68b3423797fbd788ac69c7e445d05938
Final review identity: code-review-final-r2 / sha256:f7b1f1d5325e360b4b19b51817581f991b0135794f3b386fd169f0b0e23f38f1
Reviewed subject revision: 0bdaef90eb5fefefd4db8e626d5df14890a67280
Base revision: afb4937bd0874286f6c260dbd58cd10a088b0986
Final-review recording revision: a48732e5b79aa394b758b7154cf597304d0619c7
Prior explanation identity: sha256:531a977b009d2ca78f108b08dc94cddbae64c6041017ad19552d10369572d455

## Summary

The CI-maintenance skill now uses a compact universal contract, one conditional GitHub-authoring reference, the existing risk-to-check map as the sole semantic placement owner, and a minimal workflow skeleton. Narrow reviews no longer load authoring, coverage, cache, boundary, or privileged procedure that they do not need, while every supported assembly retains explicit authority, safety, failure, and claim limits.

The implementation also closes the mutation paths that made simplification risky: privileged workflow changes require exact approved design evidence; creation cannot clobber a concurrently created target; revision cannot replace a changed identity; and dependent multi-file requests prepare and validate a complete graph before committing only safe intermediate states. A later lifecycle correction moved mutable proposal status into the owning change record, retained the failed verification as historical evidence, and required a fresh governed proposal review and final holistic code review instead of treating a manual edit as readiness.

## Problem

The former flat skill mixed universal review safety with GitHub serialization, risk placement, privileged examples, and broad workflow structure. That made ordinary review expensive to load and allowed the skeleton and authoring procedure to imply policy that should come from project evidence. Its generic atomic-replacement wording also did not distinguish no-clobber creation from identity-guarded revision or define dependency-aware partial completion.

The initial portable proposal later exposed a separate lifecycle inconsistency: it embedded a prose status while the repository contract requires mutable proposal state in `docs/changes/<change-id>/change.yaml`. Final verification correctly rejected that value. The correction adopted the existing proposal into the current governed change without changing its selected CI-maintenance direction.

## Decision trail

- The accepted proposal selected a compact root, one GitHub authoring reference, the existing risk map, one reduced skeleton, and no scripts or runtime engine.
- Approved spec R1-R54 defines the independent classification axes, ownership boundaries, privileged approved-design assembly, conditional commits, dependency-aware batches, result truthfulness, compatibility, and reduction gates.
- The architecture assessment concluded `architecture-not-required` because the design reuses packaged resources, repository files, and transient file primitives without new persistence or external-state ownership.
- Plan M1-M4 froze preservation contracts, extracted the package, proved mutation safety, and measured every assembly before final review.
- `verify-r1` found the embedded proposal status outside the closed lifecycle vocabulary and made no readiness claim.
- The user-authorized proposal migration removed that embedded state, registered the exact proposal in the owning change record, and preserved the isolated R3 review as historical evidence.
- Governed `proposal-review-r4` approved the migrated proposal at `sha256:a7f4b73f458d3bdca53c2f81bb0416edae9fad0dec75bfd8b7054fddbb603d40`.
- `code-review-final-r2` reviewed the complete corrected branch at `0bdaef90` and found no material defect.

## Diff rationale by area

| File or area | Change | Reason | Governing source | Test or evidence |
| --- | --- | --- | --- | --- |
| `skills/ci-maintenance/SKILL.md` | Replaced the flat procedure with a compact universal classification, authority, mutation, result, and resource-routing contract. | Keep fail-safe decisions inline while reducing irrelevant common-path loading. | R1-R14, R24-R44 | Focused simplification tests; M2 and M3 evidence |
| `skills/ci-maintenance/references/risk-to-check-map.md` | Made the map the sole owner of risk, check, command, and execution-boundary placement. | Prevent the map and GitHub authoring procedure from independently choosing PR-versus-boundary policy. | R15-R20 | `test_risk_map_owns_semantic_placement`; semantic-preservation review |
| `skills/ci-maintenance/references/github-workflow-authoring.md` | Added conditional ordinary composition and exact approved-design realization procedure. | Serialize settled GitHub policy without inventing commands, coverage, or privilege. | R11-R20, R25-R28 | Package/resource tests and CIM8 scenarios |
| `skills/ci-maintenance/assets/github-workflow-skeleton.yml` | Removed built-in PR, push, schedule, manual, cache, secret, OIDC, runner, and deployment examples. | Make the asset structural and least-privilege by default instead of a hidden policy source. | R21-R23 | Skeleton validator and forbidden-content regression test |
| `scripts/skill_validation.py` and `scripts/test-skill-validator.py` | Updated package validation and added closed-axis, resource, concurrency, batch, compatibility, and size proofs. | Fail closed on missing resources and unsafe examples while proving the accepted contracts deterministically. | R45-R54 | 13 focused tests and the complete skill-validator suite |
| Focused and legacy specs | Added the complete simplification contract and amended five overlapping legacy clauses. | Preserve all unlisted legacy requirements while giving changed ownership and safety rules one normative source. | R54; AC1-AC16 | Boundary validator, rule/literal ledgers, independent reviews |
| Proposal and owning change record | Removed embedded mutable status, added one exact owning-change pointer, registered the accepted proposal identity, and recorded real follow-on artifacts. | Put lifecycle state under its required owner and eliminate the blocker reported by `verify-r1`. | Artifact lifecycle defaults; explicit user authority | Proposal adoption evidence; `proposal-review-r4`; lifecycle validation |
| Change-local fixtures and evidence | Recorded T1-T15, ownership inventories, measurements, milestone proof, reviews, the failed verify result, migration evidence, and fresh final review. | Make semantic preservation, simplification, and correction history reviewable instead of inferred. | Test spec and plan M1-M4 | Review log, review resolution, verify report, and final review R2 |

## Tests added or changed

| Test ID | Proof | Level |
| --- | --- | --- |
| T1-T5, T11-T15 | Closed axes, assemblies, privilege, resource safety, hosted-CI claims, compatibility, and package reduction. | contract/integration |
| T6-T8 | Commit-time no-clobber, identity-guarded revision, and read-back boundaries. | contract |
| T9-T10 | Dependency ordering, cycle/atomic-group stop, exact partial results, and fresh retry. | contract/integration |
| Validator regressions | Minimal skeleton invariants, packaged-reference discovery, unknown-value rejection, and all-profile size gates. | automated regression |
| Lifecycle correction checks | Exact proposal identity, governed settlement, removal of embedded status, review closeout, and current metadata consistency. | governance/integration |

## Validation evidence available before final verify

| Command or check | Result | Evidence cutoff |
| --- | --- | --- |
| `python scripts/test-skill-validator.py CiMaintenanceSkillSimplificationTests` | passed; 13 tests | reviewed subject `0bdaef90` |
| `python scripts/validate-skills.py skills/ci-maintenance/SKILL.md` | passed | reviewed subject `0bdaef90` |
| Complete skill, build, generated-output, and adapter suites from `verify-r1` | passed; 432 skill tests with 16 skips, seven build tests, and 150 adapter tests | unchanged product/package subject through `0bdaef90` |
| Change metadata and explicit-path artifact lifecycle validation | passed | reviewed subject `0bdaef90` |
| Review-artifact closeout validation | passed; 12 reviews, two resolved findings, 12 log entries | final-review recording `a48732e5` |
| Documentation prose and diff checks | passed | final-review recording `a48732e5` |
| `bash scripts/ci.sh --mode pr --base origin/main --head HEAD` from `verify-r1` | failed on the former embedded proposal status; historical, corrected but not rerun here | verified subject `f6c50d99` |

## Review resolution summary

Two material findings have accepted and resolved dispositions, with no open findings: specification finding `CIMSIM-SR1` and implementation finding `CIMSIM-CR1`. See [review-resolution.md](review-resolution.md) for their decisions and validation evidence. Final holistic reviews R1 and R2 found no additional material finding.

## Alternatives rejected

Keeping the flat skill would not reduce real loaded profiles. A catch-all reference would preserve mixed ownership, while many small references would add routing and parity risk. A workflow generator, policy engine, YAML ownership parser, persistent mutation receipt, provider-neutral abstraction, or external platform integration would create new architecture and acceptance surfaces beyond the selected repository-file refactor.

For the lifecycle correction, changing the embedded prose to another status would have left two potential state owners. Discarding the isolated review or failed verification would have erased truthful history. The selected migration instead keeps stable reasoning in the proposal, mutable state in `change.yaml`, and each review or verification occurrence in its own evidence record.

## Scope control

The change does not execute hosted workflows, open a live PR, mutate external platform state, invent project validation commands, design privileged policy, add a runtime helper, migrate historical workflows, or introduce persistent locking or transaction state. The proposal correction does not change CI-maintenance behavior or retroactively claim that the failed verification passed.

The separate proposal for a reusable portable-to-governed adoption contract is not part of this branch. This branch contains only the bounded correction required for the current CI-maintenance change.

## Risks and follow-ups

The principal product risk is future CI capability expanding beyond repository-file targets or requiring resumable cross-process coordination. Such work must stop and return to architecture instead of extending this package implicitly. All current assemblies are below baseline, but later shipped-text changes must rerun the deterministic word/byte gates so root shrinkage cannot hide total-package growth.

The full PR-mode validation wrapper has not yet been rerun after the proposal migration. Its prior lifecycle blocker is corrected and targeted checks pass, but only `verify` may establish current branch readiness. The earlier explanation and verification remain historical evidence rather than being overwritten or reinterpreted.

## Workflow handback

Explanation status: current
Explanation basis: sha256:be97524884f53711e86dd209e6d61262b50508cb0216d71d7c7d9a7d1ec19125
Validation-evidence cutoff: final-review-recording:a48732e5b79aa394b758b7154cf597304d0619c7
Open explain-change blockers: none
Control returned to workflow: yes
Next-stage decision owner: workflow
