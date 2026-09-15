# Validation refactor independent Design Review

## Result

- Skill: design-review.
- Review status: approved for the explicitly bounded advisory assessment below.
- Review ID and round: validation-refactor-design-review, round 1, 2026-09-14.
- Recording mode: advisory-durable/manual; no governed change was selected.
- Package members: complete current `docs/design/engineering/validation.md` and `docs/design/system.md`, identified below.
- Upstream review ID: not applicable to this isolated assessment. The user selected proportionate evidence, existing semantic reviews and ownership-based test organization, requested the refactor and branch, and authorized this independent delegation and continuation. No Proposal Review or lifecycle settlement is invented.
- Material findings: none.
- Correction targets and open blockers: none within this assessment.
- Recording status: recorded in this document.
- Immediate next owner: Plan author, under the user's existing authorization, for scoped migration allocation and independent Delivery Review.
- Claim limitations: suitable engineering basis for scoped delivery planning; no formal lifecycle gate settlement, implementation approval, approval of the rest of the dirty branch, final Verify, PR readiness or publication authority.

## Exact subjects and independence

| Subject | CLI-inspected identity |
| --- | --- |
| `docs/design/engineering/validation.md` | `sha256:26ade9487d6db3f6c190b3f073af506431c6b47e1d7aab0f5b2c72cf897286f1` |
| `docs/design/system.md` | `sha256:45994453b7977569cfcf166f8543b492186b0932a1e8798c9c238c5e7e8623bc` |

The author is the coordinating agent `/root`, which supplied the authored package and its recorded identities. Reviewer `/root/validation_design_review` is a separately spawned agent created after authoring for the user-authorized independent review. It did not author or edit either subject and wrote only this review. The separation is a distinct delegated execution with read-only subject inspection, not the author assigning itself a reviewer label or beginning another turn. This review does not authenticate an external human identity or establish independence for other reviews.

The assessment read both complete members, including the previous refinements present in their current bytes; those refinements were not presumed approved. Relevant contract and author-evidence sections were inspected for ownership, evidence limits, migration and prior scope. Approval is the engineering judgment above about these two members together. It does not approve all referenced child models, historical migrations or unrelated implementation changes merely because they are referenced.

## Governing and supporting basis

| Relied-on dependency | CLI-inspected identity and assessed contribution |
| --- | --- |
| `CONSTITUTION.md` | `sha256:cc1912d5c0cd17b42bfd4a3f705a561b0c2f678045f0659f2406a1ea13e6c5a5`; authority, review independence, proportional proof, preservation and cleanup. |
| `docs/design/skill/assessment.md` | `sha256:af968c5583c27abb95e9a2b2ac0293deba30c522e72480c6f9aa05066659ae19`; RC-SR-01–18, isolated scope, independent judgment and evidence applicability. |
| `docs/design/skill/workflow.md` | `sha256:ed5380294c163077a289f3566e041b8d580f7217b15756f961aba181400a757d`; assessment ownership, authoring/proof handoffs and no authority from recording. |
| `docs/design/skill/authoring/plan.md` | `sha256:5ea24213d164d301ed4690f3647bbb98d8f5709bf10af03c3efbdcad08ef9826`; requirement allocation, integrated proof, stable milestones, recovery and final independent whole-change review checkpoint. |
| `docs/changes/2026-09-14-design-suitability-review/contract-refinement.md` | `sha256:4d59def061c84becf3c9746508484a23eebf9c6009e8bdf589a9e8547aa49aa7`; author handoff, affected-consumer dispositions, test audit and mechanical results. This is evidence, not a normative owner or prior approval of the current package. |

Applicable design-review skill resources were read for test quality, review assessment/reliance, requirement-to-delivery allocation and advisory recording. Current project-map data was not used to infer source placement. Prior lifecycle records are not selected, migrated or settled by this assessment.

## Assessment rationale

1. **Evidence choice preserves required protection.** TEST-SR-15 extends TEST-SR-12's allocation rule without turning every requirement into a test function. Important executable behavior still needs repeatable observations at a boundary that can expose failure. Manual or review evidence must disclose scope and cannot waive a required executable check. This is consistent with contract-derived oracles, unknown-protection preservation and replacement-before-removal in TEST-SR-01–10. A small test is not declared worthless merely because it is small.

2. **Semantic assessment stays with its existing owners.** TEST-SR-16 and the evidence-selection table distinguish instruction quality from universal agent execution compliance. Required earlier independent reviews remain intact. Human PR review is explicitly conditional on using a PR, so this does not make Git or an external host a prerequisite for individual skills. Material uncertainty unresolved by inspection receives a bounded manual scenario using owned isolated state and existing action permissions. No semantic judge, runtime certification service or new gate is silently introduced.

3. **Ownership and technical realization are coherent.** System declares the source boundary and delegates detailed groups to Validation. Production commands and runtime helpers remain under scripts; repository test sources move by actual Skill/Engineering capability; package tests stay colocated. Record-document validator tests and package persistence tests have distinct primary owners. Exclusive fixtures/test helpers follow their suite; shared fixtures have actual consumers, one owner and immutable or independently materialized inputs. Production code may not depend on test-only helpers. These rules are sufficient for Plan to derive concrete destinations without a speculative folder per model leaf.

4. **Migration cannot earn a false pass by losing tests.** TEST-SR-17 covers imports, discovery, catalog commands, selectors, direct callers and fixtures in each moved slice. The detailed contract includes imported/generated cases, both sides of renames, deletion routing, canonical check-ID preservation and historical-result identity preservation. The combined suite/fixture move must still detect an intentional representative violation. Existing paths remain supported until coherent migration, and rollback restores sources and consumers together. No permanent alias, new catalog, test deletion quota or changed worker budget is selected.

5. **Architecture and acceptance are sufficient for allocation.** Validation's overview explicitly shows allocated non-executable evidence reaching Assessment independently of execution results. Its existing Context, Building Block, Runtime and Deployment views still explain the relevant interfaces and process boundaries; a directory move adds no deployed service. System's overview, full hierarchy and end-to-end delivery view keep owner integration distinct from approval. Identity/authority and compatibility/migration scenarios cover the new decisions, while existing discovery, concurrency, failure and output requirements remain in force.

6. **The complete-member context does not enlarge this migration.** The members retain existing cleanup, retirement and parallel-execution requirements under their scoped initiative identities. The new decision does not reopen or claim completion of those historical initiatives. Current owner references and provenance keep removed source inventories distinguishable from runtime authority. Prior uncommitted hierarchy and presentation refinements in these two members are coherent with this scoped migration; this does not independently settle their separate downstream child/consumer packages.

VAL-DEC-09 records the selected alternative and consequences: proportional evidence and capability ownership, with preserved discovery and protection, instead of universal per-requirement cases or routine agent certification. No material undecided behavior prevents scoped delivery planning.

## Evidence and limits

The reviewer independently ran:

```bash
node packages/rigorloop/dist/bin/rigorloop.js subject inspect --root . --path docs/design/system.md --path docs/design/engineering/validation.md --format json
python scripts/validate-boundary-first.py --check --path docs/design/engineering/validation.md --path docs/design/system.md
```

Subject identities match the author handoff. Structural/reference validation passed and explicitly reports `structure-and-references-only`; no model examples were selected. Relevant dependency identities were inspected separately through the same CLI.

The author records 489 successful selected check/case rows for this Design slice and earlier audit/correction results. Those are attributed author observations, not executions repeated by this reviewer, and are not the basis for semantic approval. No migration has been implemented or exercised by this review. The actual test/fixture inventory, direct and selected discovery comparisons, deletion/rename routing, representative failure sensitivity and recovery evidence remain delivery obligations. No hosted CI or external agent execution is claimed.

## Handoff and applicability

The package is suitable to rely on as the engineering basis for the user-authorized scoped migration plan at the exact identities above. Plan should allocate concrete coherent moves, their actual readers, before/after discovery, selected and ordinary execution, representative failure detection and recovery. It must retain the distinct final whole-change Code Review and Verify checkpoints. Independent Delivery Review remains required before implementation relies on that plan.

This advisory judgment is not a stored formal-lifecycle approval. If governed execution is subsequently selected, its owner must establish the applicable exact review package and contract-selected records without representing this advisory save as lifecycle settlement. Subject or material dependency changes require applicability assessment and appropriate independent reassessment; a matching pathname or a passing suite alone does not renew this judgment.

### Retained release-owned fixture clarification

During handoff, the planner identified `tests/fixtures/release-transaction/current-version.json`. Reviewer inspection of `scripts/release_transaction.py`'s `_plan_current_version_fixture` and `scripts/release_candidate.py`'s allowed candidate paths confirms that release tooling intentionally generates and stages this persistent release-owned fixture. It is not scratch from a test run or a test-only helper imported by production. Retaining its existing location and release behavior is consistent with the capability-owned shared-fixture rule and the explicit preservation of existing fixture consumers. No Design amendment is required for that bounded disposition. Delivery must identify its owner, producer and consumers and preserve their qualification/selection behavior; it must not move it merely because exclusive test resources move.
