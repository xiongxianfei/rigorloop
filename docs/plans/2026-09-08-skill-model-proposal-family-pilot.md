# Skill Model and Proposal-Family Pilot Delivery Plan

## Purpose / big picture

Implement the approved common Skill owner and a useful, bounded improvement to `proposal` and `proposal-review`. Keep pilot procedure relocation and its enforcing consumers coherent before displacing current common sources. Preserve unchanged obligations, specialist authority and readable history, then assess the complete change before adoption.

## Current Handoff Summary

- Owning change record: [change.json](../changes/2026-09-08-skill-model-proposal-family-pilot/change.json).

Mutable lifecycle state, current milestone state, review status, blockers, routing and closeout readiness live only in this record.

## Source artifacts

- Proposal: [Skill Model and bounded pilot](../proposals/2026-09-08-skill-model-proposal-family-pilot.md).
- Spec and architecture: [Skill Design](../design/skill/skill.md) and its scoped [System composition](../design/system/system.md), as assessed in [Design Review round 2](../changes/2026-09-08-skill-model-proposal-family-pilot/reviews/design-review-r2.json).
- Retained contracts: [Skill Contract](../../specs/skill-contract.md), [Readability](../../specs/skill-readability-contract.md), [Customer portability](../../specs/customer-portable-public-skill-evidence.md), [resource-integrity decision](../adr/ADR-20260623-published-skill-resource-integrity.md), the exact specialist and operational owners identified by Skill's displacement map, and [published-skill-first proof policy](../../specs/published-skill-first-repository-simplification.md).
- Prior-contract test spec: none independently selected. Existing tests remain protection to assess under Test; historical pilot transcript, clean-install and savings gates are not reactivated.
- Shared assessment and test criteria: [Review and Closeout](../design/review-closeout/review-closeout.md) and [Test](../design/test/test.md). Recording uses current [Record Format](../design/record-format/record-format.md) and [CLI](../design/cli/cli.md).

## Context and orientation

`skills/` is the authored source. The four selected content files are the two pilot `SKILL.md` files, `skills/proposal/references/governed-proposal-authoring.md` and `skills/proposal-review/references/proposal-review-recording-and-settlement.md`. Existing descriptions, three artifact assets, strategic/conditional gates, requirement-to-delivery copies and Review and Closeout resources remain baseline behavior. No new shared resource is needed.

`scripts/skill_validation.py` selects detailed recording and installed-review placement; its current heading-based selection cannot be allowed to skip checking relocated pilot procedure. `scripts/test-skill-validator.py` covers validation and source-preservation expectations. `scripts/test-adapter-distribution.py` must compare the two selected recording references across supported packages. Existing skill and adapter generators remain the production path. `scripts/validate-guide-system.py` and its regression suite are directly affected common-owner consumers when source navigation changes.

This allocation uses the inspected source files and exact source searches rather than relying on `docs/project-map.md` for the new Skill responsibility: that map does not yet establish this prospective owner. M2 includes a bounded correction to any current map/navigation reference affected by adoption, without an inventory-wide map rewrite. Exact authoring subject identities and observations belong in plan-authoring evidence, not mutable plan status.

## Non-goals

- No third pilot, new public command, record schema, adoption registry, universal metadata change or specialist policy redesign.
- No source retirement before its surviving obligations have actionable destinations; no archival rewrite of judgments or operational manifests.
- No whole-directory removal, blanket test deletion, repeated completed asset extraction, token quota or universal target-agent experiment.
- No publication, real customer installation, release-version bump or automatic customer governance. Generated candidate inspection does not grant these permissions.

## Requirements covered

| Governing obligations | Allocated implementation and proof |
| --- | --- |
| SKL-SR-01 | M2/TG-04 and TG-FINAL-01: one current owner with preserved populations and explicit non-pilot boundary. |
| SKL-SR-02–07 | M1/TG-01/02; M2/TG-04: preserve description, role, method, claims, portability, evidence-reading rules and complete retained definitions. |
| SKL-SR-08–11 | M1/TG-02/03; M2/TG-04: complete mapped resources, containment, raw-byte identity, explicit transformations, runtime fallback versus package validity and exact lint/enforcement populations. |
| SKL-SR-12–15 | M1/TG-01/02/03; M2/TG-04/05: existing assets, authored projections, bounded validation, secret-safe evidence and separate release authority. |
| SKL-SR-16–19 | M1/TG-01/02/03: classification-first pilot, complete triggered recording, unchanged assessment authority and justified before/after value. |
| SKL-SR-20 | M1/TG-02/03 and TG-FINAL-01: selected validator paths, supported candidates and unchanged non-pilot protection. |
| SKL-SR-21–22 | M2/TG-04/05 and TG-FINAL-01: exact source dispositions, readable history, coherent governance/consumers and distinct review/Verify adoption boundary. |
| SKL-SR-23 | M2/TG-05: confirm named remaining families, receiving owners, applicable differences and next decisions in existing follow-ups. |
| SYS-SR-02/04/06/07, scoped to the Skill-owner and pilot amendment | M1/TG-02–03 for coherent procedure, validator and candidate consumers; M2/TG-04–05 for ownership, historical separation and follow-ups; TG-FINAL-01 for the composed result. |

SKL-DEC-01–05 govern both milestones. The retained-contract table's precise metadata, role-summary, vocabulary, portability-lint and resource-enforcement rules are part of the mapped requirements; a topic link cannot replace them. Design's eight boundary dimensions and four combined hazards are allocated below rather than converted into a second requirement catalogue.

## Milestones

### M1. Improve the pilot and its enforcing package consumers together

- Milestone kind: implementation.
- Engineering purpose: relocate procedure only with the validator and archive-comparison changes needed to keep the complete selected paths checked. Existing common authorities remain operational throughout this slice.
- Requirements: SKL-SR-02–20, with pilot-only changes restricted to SKL-SR-16–19's named pair.
- Architecture responsibility: Skill's inspected before/after outcomes, validator composition, Runtime and Deployment views; SKL-DEC-02–04.
- Dependencies: current approved Design and Delivery packages; no source retirement dependency.
- Implementation scope: the four selected pilot files, bounded recording/profile/placement validation, regression proof and generated candidates. Retain unchanged assets, resource gates, descriptions, shared source/copy bytes and non-pilot skill bodies.
- Files/components likely touched: `skills/proposal/SKILL.md`, `skills/proposal/references/governed-proposal-authoring.md`, `skills/proposal-review/SKILL.md`, `skills/proposal-review/references/proposal-review-recording-and-settlement.md`, `scripts/skill_validation.py`, `scripts/test-skill-validator.py`, `scripts/test-adapter-distribution.py`. Derived mirrors/candidates are generated under existing contracts.
- Required verification: TG-01 demonstrates useful ordinary/exceptional procedures and artifacts; TG-02 protects validator selection and rejection; TG-03 observes complete canonical-to-candidate packages and non-pilot coexistence.
- Evidence expectations: exact before/after source identities, focused failure-before/fix-after evidence where feasible, actual command results, resource/asset and non-pilot byte comparisons, and a concise manual assessment packet for independent Code Review. No invented target-agent execution or semantic scoring.
- Implementation steps: inspect the then-current baseline against approved subjects; first add meaningful regression cases for moved/missing selected recording content and placement; move complete recording procedure into the existing references while keeping classification, load triggers, late-trigger handling, stops and claim limits visible; qualify the proposal pointer by project governance; reconcile adopted versus portable review instructions without changing judgments; update profile selection and archive comparison atomically with the relocation; regenerate and inspect supported candidates; inspect whether selected current-candidate metadata and its dependent assertions are affected by changed package bytes, regenerate affected metadata through its existing owning builder and run directly dependent checks before milestone closure, or record an inspected unaffected disposition; preserve historical release metadata without inventing hashes or introducing publication work; document the selected improvement and preservation evidence.
- Validation commands: `python scripts/test-skill-validator.py -k targeted`; `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/build-skills.py`; `python scripts/build-skills.py --check`; `python scripts/test-build-skills.py`; `python scripts/test-adapter-distribution.py`; candidate commands in the Validation plan. Record selected case counts for focused filtering; an empty selection is not proof.
- Expected observable result: ordinary readers reach task classification without detailed storage construction; triggered governed/durable paths still reach complete procedure and usable artifacts; validators continue to reject defects after the body heading moves; all supported candidates carry the full package.
- Completion criteria: all three groups have sufficient passing mechanical evidence and independent semantic assessment of a useful improvement; no unresolved behavior loss or non-pilot expansion; milestone Code Review assesses the entire pilot/validator/package slice. An inconclusive or unfavorable improvement returns to Design or owned correction before M2 can rely on it.
- Required evidence: M1 implementation evidence and independent milestone review in the existing change-local record system, including actual limitations and concern dispositions.
- Review handoff: independent Code Review of both author/reviewer paths, four selected files, all changed checks, candidate comparisons and preserved portable behavior. Do not substitute a shortened body or test pass for judgment.
- Risks: early-return validation silently bypasses relocated procedure; unrelated resource text satisfies a token check; cleanup removes still-needed portable policy; extra loading makes ordinary work harder.
- Rollback/recovery: restore the four files and their coupled validator/archive-comparison changes as one unit, then regenerate derived output. Preserve failed evidence and source identities. If an essential method, authority decision or unexpected shared consumer is missing, stop affected work and return to the owning Design/Delivery stage; do not expand the pilot.

### M2. Transfer common authority and preserve its sources

- Milestone kind: implementation.
- Engineering purpose: reconcile source definitions, governance and direct consumers after M1 establishes pilot value, with original bytes recoverable before displacement.
- Requirements: SKL-SR-01–15 and SKL-SR-20–23, especially retained rule precision and source/consumer ownership.
- Architecture responsibility: Skill's complete displacement maps, retirement/archive realization, consumer dispositions and System owner relationship; SKL-DEC-01/05.
- Dependencies: M1 and its independent milestone assessment complete with required concerns dispositioned. Source transfer is staged for adoption only with successful final Verify, not merely a file edit or this milestone's review.
- Implementation scope: reconcile only the mapped common portions; retain source-local specialist clauses and operational inputs; establish archive navigation and bounded common-owner references; confirm existing follow-up allocation. Do not rewrite the approved Design to conceal an unmapped obligation: return any semantic change to Design and independent reassessment.
- Files/components likely touched: `specs/skill-contract.md`; `docs/architecture/system/architecture.md` at the exact Skill-selected sections; `CONSTITUTION.md`; `AGENTS.md`; relevant current navigation including `docs/project-map.md` where affected; `docs/archive/skill-model/2026-09-08/`; `scripts/test-skill-validator.py`; `scripts/validate-guide-system.py` and `scripts/test-guide-system-validator.py` where their owner selection needs correction; `docs/follow-ups.md`. Skill/System are adopted as the exact reviewed package; any engineering amendment to them requires the appropriate reassessment.
- Required verification: TG-04 checks the complete actionable transfer and useful validator replacement; TG-05 checks source identity, historical navigation, follow-up ownership and coherent necessary consumers. TG-FINAL-01 observes the integrated result after M2.
- Evidence expectations: original SHA-256 and archive comparison, a source-consumer disposition table, semantic review of retained definitions and mapped acceptance intent, concrete negative source/consumer regression evidence and current navigation checks. Preserve original historical review bytes and judgments.
- Implementation steps: capture the four exact originals specified below before editing; create byte-identical source-relative snapshots and an archive index; classify exact-path/ID consumers as operational, current authority or historical; replace only transferred common prose in the mixed Skill Contract and selected architecture portions; preserve retained IDs/clauses; update governance/current consumers to Skill with the same conditional adoption boundary; move useful literal-source tests to the new owner and assess every removed oracle against preserved protection; validate archive navigation and follow-ups; assemble integrated proof for final review.
- Validation commands: `python scripts/test-skill-validator.py`; `python scripts/validate-skills.py`; `python scripts/validate-guide-system.py`; `python scripts/test-guide-system-validator.py`; model/prose/readability and repository CI commands in the Validation plan. Source byte/link checks are implemented as bounded proof under TG-05, using existing test infrastructure where suitable.
- Expected observable result: authors and validator maintainers can apply surviving common rules from Skill without reconstructing archived prose; mixed sources still expose their unmigrated authority; useful originals and necessary related links remain directly readable; the other 17 skills have named later adoption decisions.
- Completion criteria: each selected obligation/decision/acceptance responsibility has one complete destination, explicit supersession or justified current retention; original-byte and link evidence passes; all affected current and operational consumers resolve correctly; no historical proof gate is restarted and no active enforcement is reset. Independent M2 Code Review assesses semantic preservation and the exact source dispositions.
- Required evidence: M2 implementation/source-retirement evidence, test-protection rationale and independent milestone review in existing change-local records, followed by integrated proof for final review.
- Review handoff: independent Code Review of the actual source/consumer diff, all original snapshots and navigation, retained-contract completeness and the cross-milestone adoption boundary.
- Risks: partial authority transfer leaves a rule defined only in history; source text changes break a real operational reader; archive-relative links break; a historical clause is accidentally reactivated or a non-pilot population tightened.
- Rollback/recovery: restore displaced original source bytes and coupled governance/current-consumer changes together, preserving snapshots and assessments as evidence. Keep the verified pilot if independent assessment establishes it remains valid under restored authorities; otherwise restore M1 as its complete unit. Stop adoption on any unresolved ownership or historical identity gap. Do not rewrite old approvals to match rollback subjects.

## Verification groups

| Group | Required observable outcomes and proof allocation |
| --- | --- |
| TG-01 — Pilot value and complete procedure | M1 author supplies repeatable source/artifact walkthroughs for portable proposal authoring, governed proposal authoring, isolated advisory review and formal/material review. Demonstrate correct existing artifact shape, author/reviewer separation, seven proposal sections with conditional impact, project-governed ownership pointer, recording-before-dependent-correction and no automatic continuation. Include malformed governed signal, late durable trigger, missing required method and missing local CLI/authority as distinct stops. Independent reviewer assesses classification-first readability, completeness, adopted/portable judgment consistency and actual usefulness against baseline. Exact loaded body/references, representative inputs and resulting artifact or stop are evidence; synthetic walkthroughs do not claim target-runtime accuracy. |
| TG-02 — Selection, rejection and compatibility | M1 regressions exercise the production validation boundary after heading relocation: a valid selected reference passes; absent, unreadable, malformed, escaped or unknown selected content fails explicitly; words in an unrelated resource do not satisfy it; missing body trigger still fails; installed review placement selects current v2 rather than retired Markdown placement. Preserve non-pilot profile checks and closed-vocabulary unknown-value coverage. Observe rejection without false conformance. Resource tests retain missing/untriggered package failure, mapped-class/containment, recognized legacy-prefix scope, arbitrary-path exclusions and explicit temporary-exception populations. Ordinary untriggered runtime behavior is assessed separately in TG-01. |
| TG-03 — Canonical-to-candidate boundary | M1 runs existing Gate A/B and adapter distribution proof for Codex, Claude Code and opencode. Compare each mapped resource's relative path/raw-byte identity and supported body transformation; missing or stale resources and incomplete transformation declarations reject. Archive profile comparison inspects the selected pilot references. Inspect current-candidate metadata and assertions describing those exact archives; demonstrate regeneration through the existing owning builder and passing directly dependent checks when affected, or record an inspected unaffected disposition. Preserve historical release metadata; archive generation alone does not prove downstream metadata consistency. Preserve all 17 non-pilot canonical bodies and unchanged pilot assets/shared resources by before/after byte comparison; execute existing inventory validation to detect shared-consumer regression. Do not run real customer installs or infer publication. Existing repository-owned temporary materialization tests retain their applicable proof; no historical all-target agent smoke gate is added. |
| TG-04 — Actionable retained contract and validators | M2 evaluates the full selected map, including numbered, unnumbered and representative acceptance intent. The current destination must state actual rule, population, trigger/outcome and approved exception/supersession. Specifically inspect metadata, role summary, vocabulary presentation, public-text lint exclusions, recognized loading prefixes, unmapped-reference failure/temporary debt, new/changed versus inventory enforcement and runtime fallback/package validity. Retained specialist plan/boundary definitions remain current. Assess changed literal-source tests by their protected behavior; replace obsolete wording assertions only after equivalent useful protection exists. No keyword scan establishes semantic preservation. |
| TG-05 — Readable history and receiving owners | M2 compares the four pre-displacement source hashes to archive raw bytes, preserves their source-relative names and validates every necessary related link/diagram through source-resolved archive navigation. Broken/missing archive targets must be detected by the selected bounded check. Confirm mixed-source current references, operational manifests/templates at original paths, historical record identity preservation, and current owner consumers. Confirm FU-015–018 enumerate all 17 remaining skills/families, receiving owners, applicable differences and next adoption decisions; preserve FU-012's separate validation remainder. |

## Source disposition allocation

| Source | Exact implementation disposition |
| --- | --- |
| `specs/skill-contract.md` | Snapshot original bytes at `docs/archive/skill-model/2026-09-08/specs/skill-contract.md`; retain the original current path as the bounded mixed contract for Skill's explicitly retained plan and boundary-method obligations. Replace mapped common definitions with precise Skill owner references, preserving retained source IDs. |
| `specs/skill-readability-contract.md` | Snapshot original bytes at the corresponding archive `specs/` path; retain original-path bytes as non-current history for existing source-relative historical dependencies. Archive navigation and current governance identify Skill as replacement after adoption. |
| `specs/customer-portable-public-skill-evidence.md` | Same snapshot plus source-path historical retention, with current authority explicitly redirected through navigation/governance. Do not revive workflow-guide creation or runtime benchmark requirements. |
| `docs/adr/ADR-20260623-published-skill-resource-integrity.md` | Snapshot under the archive's source-relative `docs/adr/` path; retain original-path bytes and accepted judgment as history. Point current architecture decision navigation to SKL-DEC-02 and archive provenance. |
| Mixed architecture and other sources | Change only Skill's mapped common sections in `docs/architecture/system/architecture.md`; retain its other owners, diagrams and historical references. Proposal-family assets, plan assets, boundary method/projection sources, resource manifests, schemas and templates keep their paths and their declared responsibilities. |

No original-path move is selected for the three fully superseded originals because historical source-relative dependencies justify retention. `docs/archive/skill-model/2026-09-08/README.md` records each original path, raw-byte identity, replacement, retention reason and necessary source-resolved links/diagrams. Readers can read original bytes directly and follow related links through this navigation; the snapshot's relocated relative links are not assumed to work. Current navigation must not present a retained historical copy as a competing normative owner. If newly inspected dependencies defeat this disposition, stop affected displacement for Design/Delivery correction.

## Final review checkpoint

- Kind: lifecycle-closeout.
- Dependency: all in-scope implementation milestones and required corrections complete.
- Assessment: fresh independent final whole-change Code Review of the complete delivered engineering change and cross-milestone interactions.
- Evidence: exact final subjects, independent reviewer basis, judgment and concern dispositions.
- Successor: distinct final Verify; corrections return to their owner and require affected reassessment.

This checkpoint applies the selected review policy. A verification-group non-applicability rationale does not waive it. Reviewers must not have authored their reviewed contribution. Source adoption is established only by the reviewed coherent implementation and successful Verify; milestone completion, a saved review or a package pass alone is insufficient.

## Change-level verification

### TG-FINAL-01. Complete pilot, ownership and candidate coexistence

- Covers: SKL-SR-01, SKL-SR-04, SKL-SR-08–23; SYS-SR-02/04/06/07 scoped to the Skill-owner and pilot amendment; M1/M2; all four combined hazards identified by Design.
- Demonstrate: follow one ordinary author path and one independent formal review path from the final supported candidate through selected resources and existing assets; inspect source-to-Skill ownership and archive provenance for their common rules; ensure absent transitive procedure and moved-heading validation defects reject; confirm unchanged skills remain supported and no inventory adoption/publication claim follows. Review the final current-reference/operational-consumer inventory against actual files, not only M1's earlier package evidence.
- Evidence expectations: final candidate identities, actual integrated commands below, exact-subject walkthrough and source/consumer evidence, independent whole-change review, and subsequent Verify. Freshness follows Review and Closeout: reuse a previous command only with a recorded passing result, exact proved surface/environment and affirmative unaffected basis. New conflicting evidence or changed relevant subjects require rerun. Final Code Review itself is always fresh.
- Non-applicability: none; local pilot and archival checks alone cannot establish their coherent combined authority and package behavior.

## Validation plan

Run from the repository root. Implementation records actual commands, selected scope, exit status, observations and limitations; this section allocates intent only. Focused failure proof precedes fixes where feasible; full relevant suites follow the coherent milestone. Do not rerun unchanged suites merely to manufacture evidence.

| Command or bounded assessment | Purpose and timing |
| --- | --- |
| `python scripts/test-skill-validator.py -k targeted` | M1 first focused recording-selection proof; add and explicitly select meaningful new negative cases as implementation requires. |
| `python scripts/test-skill-validator.py` and `python scripts/validate-skills.py` | M1 complete skill validation/protection; M2 reruns because source assertions/authority consumers change. |
| `python scripts/build-skills.py`, then `python scripts/build-skills.py --check` and `python scripts/test-build-skills.py` | Generate canonical-derived local output and establish drift/generator protection after canonical edits. |
| `python scripts/test-adapter-distribution.py` | M1 adapter profile/resource and supported package proof; repeat after any relevant final change or otherwise justify unaffected reuse. |
| `python scripts/build-adapters.py --version v0.5.1 --output-dir "$skill_candidate_dir"`, then `python scripts/validate-adapters.py --version v0.5.1 --adapter-root "$skill_candidate_dir"` | Gate A/B at the existing repository candidate version; define `skill_candidate_dir` with `mktemp -d` and retain its identity/output location in local evidence. No version bump, publication or public-tree hand edit. |
| Current-candidate metadata dependency inspection and existing owning builder/checks | M1/TG-03: inspect metadata and dependent assertions tied to the regenerated candidate archives. Record exact affected paths, owning builder and directly dependent check commands, then regenerate and validate before milestone closure; alternatively record the inspected basis for an unaffected disposition. Do not invent hashes, change historical release metadata or introduce publication work or a new release-verification gate. |
| `python scripts/validate-guide-system.py` and `python scripts/test-guide-system-validator.py` | M2 current owner/navigation consumer compatibility. |
| `python scripts/validate-boundary-first.py --check --path docs/design/skill/skill.md --path docs/design/system/system.md` | Model structure/reference validation; no semantic approval. |
| `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-08-skill-model-proposal-family-pilot.md` and `python scripts/validate-markdown-readability.py docs/plans/2026-09-08-skill-model-proposal-family-pilot.md` | Plan authoring checks; implementation applies these existing tools to authored changed Markdown, respecting byte-preserved archives. |
| `bash scripts/ci.sh --mode local` | Final change-selected repository integration checks. Confirm selection includes all relevant changed/untracked authored surfaces; use the wrapper's repeated `--path` arguments where discovery needs explicit roots. Report unrelated baseline failures separately; do not suppress applicable failures or claim successful Verify until they are resolved. |
| `git diff --check` | Tracked whitespace consistency; explicit prose/link checks additionally cover new untracked authored files. |
| TG-01/TG-04 independent walkthrough and TG-05 byte/link comparison | Semantic quality and ownership cannot be inferred from keywords. Implementation records source hashes, bounded inputs, selected instructions, actual artifacts/stops and necessary historical navigation; independent reviewer evaluates the expected outcomes. Use repository test infrastructure for mechanical regressions without adding a universal adoption service or standalone test spec. |

No hosted CI result is claimed from local checks. Release verification and live-registry evidence remain under the release contract; this initiative's candidate proof does not require a release tag, external target-agent runtime or customer environment.

## Risks and recovery

The smallest safe rollback unit couples relocated procedure with its selection/placement/archive checks, and displaced authority with its governance/current consumers. Recover source truth first, regenerate derived output and reassess affected evidence. An interrupted or conflicted record write requires fresh context and exact subject inspection plus the existing authorized recovery procedure; it never grants approval. Preserve failed and superseded evidence. Unexpected policy, scope or source-definition gaps return to Design; missing verification allocation returns to Delivery.

## Dependencies

M1 requires approved proposal/Design/Delivery authority. M2 requires M1's assessed improvement and preservation. Both milestones require independent Code Review, followed by fresh whole-change Code Review and distinct Verify. Plan authors may initialize absent work only after independent Delivery Review approves this exact plan; this draft does not initialize work or authorize implementation. Existing shared resources, operational manifests and external publication permissions retain their owners.

## Decision log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-09-09 | Couple pilot content and validator/package selection in M1; retire common sources in M2 after assessed pilot value. | Avoid an intermediate bypass and premature ownership transfer; keep each review slice coherent. | Moving bodies before validators; archiving sources before useful pilot evidence. |
| 2026-09-09 | Retain three fully superseded originals at original paths plus byte-identical archive snapshots and source-resolved navigation. | Existing historical relative links require those paths; Design explicitly permits bounded source-path retention. | Rewriting archived bytes or broad relocation of unrelated historical dependencies. |
| 2026-09-09 | Use existing Gate A/B, narrow regressions and independent semantic walkthroughs. | These observe actual package and instruction boundaries without reviving superseded proof policy. | Token budgets, keyword-only quality judgment, universal target-runtime experiments. |

## Readiness

- See the owning change record for current workflow state.
