# Risk-driven test redesign: Delivery Review

## Result

- Skill: delivery-review.
- Review ID and round: risk-driven-test-delivery-review, round 1.
- Review status: approved.
- Primary plan: `docs/plans/2026-09-15-risk-driven-test-redesign.md`; portable artifact identity is its exact path and content below.
- Navigation: `docs/plan.md`; not an additional primary plan or mutable lifecycle record.
- Upstream review: risk-driven-test-design-review, round 1, approved exact Validation subject `sha256:200d5859395b87e7999e152f44c7d77a1da7d21d85ba028349f4fdd5eb70ed14`.
- Traceability result: adequate for the complete scoped M1–M4 package and TG-FINAL-1.
- Material findings, correction targets and open blockers: none.
- Recording status: recorded, advisory-durable/manual.
- Immediate next stage: isolated return of the reviewed plan; no implementation authorized by this review.
- Claim limitations: no implemented changes, suite audit completion, correctness, final Verify or branch/PR/release readiness.

## Exact scope and independence

Author `/root` wrote the plan. Reviewer `/root/validation_design_review` did not edit the plan, navigation, Designs or source and writes only this independent assessment. The full current primary plan and navigation were read, along with the approved Design assessment and applicable quality, maintenance, boundary and review guidance. The user's later planning authorization is separate from the earlier design-only invocation. No governed change record or lifecycle state is inferred.

The archive analysis is expressly a lead, not repository execution or a complete test population. The plan does not depend on the unavailable six-case prototype, assume that static method counts include generated/imported/Node cases, or convert earlier refactor reviews into current approval. Existing dirty work remains outside this scope. Concrete fixtures, exact replacement selectors and runtime baselines will be derived from the real starting tree during authorized implementation.

## Sequencing and traceability judgment

| Allocation | Boundary and meaningful proof | Judgment |
| --- | --- | --- |
| M1 / TG-1 | TEST-SR-01–05/15/16/18: recording-reference pilot, independent faults, real command behavior, selected resource containment/decoding and byte contracts. | Adequate bounded pilot. Seeded faults must affect the intended input and fail for the protected reason; ambiguous prose acceptance does not claim semantic correctness. |
| M2 / TG-2 | TEST-SR-07–10/18 and Packaging: smaller transformation fixtures plus independent canonical inventory, actual archives and packed installation for both targets. | Adequate separation of narrow and product proof. Inventory expectations cannot reuse the producer helper; destructive scenarios use owned materializations and observe installed contents and preservation. |
| M3 / TG-3 | Release approval, retry, identity and persistence; production import/default compatibility if touched. | Adequate real orchestration with external service fakes plus independent real Git persistence. Explicit/default resolution, metadata failures, outputs and Packaging consumers are allocated; new public policy returns to Design. |
| M4 / TG-4 | Validation routing/discovery, independent catalog expectations, real child overlap, prerequisites, failures and cleanup. | Adequate protection of actual entrypoints and executor boundaries; four exact repeated assertions may be removed without deleting their enclosing tests or weakening command contracts. |
| TG-FINAL-1 | Cross-milestone helper/import effects, complete discovery and execution, actual branch selection, Skill→archive→packed installer composition and retained Release proof. | Adequate integrated coverage and subject-based applicability; discovery alone is not execution and existing freshness/broad triggers remain. |

Milestones are ordered by completed independent review and required corrections. Each milestone must reconcile its own imports, catalog, helper routing, copied workspaces, direct/aggregate/individual execution and normal-loader discovery. M4 therefore checks cross-slice coherence without tolerating broken intermediate discovery. Existing selectors remain for pure module moves; deliberately split multi-fault cases require explicit accounted replacement before removal. Unknown protective value is retained for investigation.

Replacement proof must be established and independently assessed before reduced-suite reliance. Cost, line count and class setup assumptions do not determine removal. The plan preserves useful negative partitions, actual product boundaries, independent mutable state and the shared worker budget. Its scope does not demand an unrelated full-repository annotation or framework migration.

## Feasibility and runtime compatibility

Targeted source inspection confirms the named `ExplicitRecordingGuidanceTests.test_targeted_pilot_reference_selection_and_failures`, the independent complete-resource-inventory packaging case, and Release's current TestCase construction followed by explicit `setUp()` calls. The proposed pilot and fixture extraction have concrete current targets.

The current Packaging module eagerly computes `DEFAULT_ADAPTER_VERSION` from `packages/rigorloop/package.json`; Release policy imports pass through candidate dependencies. Removing fixture coupling can therefore affect production import timing and defaults. M3 correctly treats this as conditional production compatibility work, requiring a controlled incomplete-tree reproduction, preservation of explicit and default version behavior and metadata failure at the owning operation, affected Packaging proof and review of every changed consumer. It does not authorize silently changing public defaults or masking missing metadata with fabricated fixtures. If preserving intended behavior cannot be shown, the plan explicitly returns the decision to Design.

Existing aggregate commands and unittest filtering provide executable milestones. Exact new helper names are tentative where responsibility does not justify extraction, avoiding mandatory splitting by file size. No new runner, result cache, shared writable candidate, external publication or performance target is required. Real Git concurrency and real child rendezvous preserve mechanisms that mocks or sleep-only expectations could hide.

## Boundary and closeout checks

Input-domain rejection, selected-resource containment, authority/tampering, immutable identity, conflict/recovery, uncertain publication retry, concurrent Git updates, supported caller compatibility and external-environment isolation all have explicit milestone proof. Faked external services are limited to orchestration claims. Live publication/public smoke is not triggered by this test refactor, while Release's actual public obligations and tests remain intact.

Each slice has a recoverable source/discovery baseline, restores its own consumer closure and preserves unrelated dirty work and failed observations. No whole-tree reset or evidence-history rewrite is selected. Final whole-change Code Review is explicitly fresh, independent and dependent on all implementation/corrections; distinct final Verify follows it. Milestone approvals cannot substitute for that checkpoint.

The author reports plan/index prose and diff checks passed, and exact selected documentation validation passed `current_records.validate` and `guide_system.validate`. Initial untracked-plan selection was blocked; intent-to-add made the plan visible without staging content. These mechanical observations do not supply the substantive Delivery judgment. The reviewer did not execute product suites or claim future proof already passed.

## Exact subjects

CLI subject inspection captured the following subjects, and reviewer rechecked their bytes before recording. The plan is the sole primary delivery member; navigation, upstream review and governing owners are explicit dependencies. The Validation identity remains the exact approved Design basis. Dependency inspection is scoped to relevant obligations and does not newly approve unrelated content.

| Subject | SHA-256 identity |
| --- | --- |
| `docs/plans/2026-09-15-risk-driven-test-redesign.md` | `sha256:687849e708b45cdf80e42ca3f12d7dbf168a64fd47a695bdffdb8dddc7a938e5` |
| `docs/plan.md` | `sha256:5bd46334d3e5e694aaabff7c5e4dbb7ea533430e6163f529a26071418cd5cc74` |
| `docs/design/engineering/validation.md` | `sha256:200d5859395b87e7999e152f44c7d77a1da7d21d85ba028349f4fdd5eb70ed14` |
| `docs/changes/2026-09-14-design-suitability-review/reviews/risk-driven-test-design-review.md` | `sha256:daf3da02a67464a8467c5bafd77b5b3a94fa1c35f9720caf051c06d5774bb8be` |
| `docs/design/engineering/packaging.md` | `sha256:0aec3cfc2bf73424bf08d8c4efb775e4f7b5051b8417e8ebf1c90ada91aedbfa` |
| `docs/design/engineering/release.md` | `sha256:1cae90f16d152c7811eec499036dc4e7f8f63f82acd62d6b71c58f131d5f19b8` |
| `docs/design/cli/installation.md` | `sha256:5320ca604afb4e0a224317e80e9907c2fc42b78f5ab6322bc81b45d8687d6574` |
| `docs/design/skill/skill.md` | `sha256:ddb2458d430d17559e571fb605b6c812e901f310d96da7e015d749020afac02b` |
| `docs/design/skill/assessment.md` | `sha256:af968c5583c27abb95e9a2b2ac0293deba30c522e72480c6f9aa05066659ae19` |

The plan is suitable as a delivery basis if implementation is separately authorized. This approval settles sequence and proof allocation together, but grants no execution permission and makes no lifecycle, code correctness, completion or external-readiness claim.
