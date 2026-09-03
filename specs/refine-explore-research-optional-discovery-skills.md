# Refine Explore and Research as Optional Discovery Skills

## Owning change record

`docs/changes/2026-09-03-refine-explore-research-optional-discovery-skills/change.yaml`

boundary_contract: boundary-first-v1

## Related proposal

[Refine Explore and Research as Optional Discovery Skills](../docs/proposals/2026-09-03-refine-explore-research-optional-discovery-skills.md)

## Goal and context

RigorLoop must provide two distinct optional discovery skills. Explore expands the set of materially different directions available to an identified decision owner. Research reduces bounded decision-relevant uncertainty through evidence and explicit confidence. An explicit invocation of either skill creates an independently inspectable Git-tracked supporting artifact, but neither artifact approves a direction, changes another stage's contract, or progresses lifecycle state.

The public packages must remain concise and self-contained. Stable common artifact, authority, stopping, contradiction, and handoff rules are shared without merging the two reasoning modes. Route must make it clear when to use Explore, Research, both, or neither.

## Glossary

- **Explore:** the optional divergent support skill that frames a decision and expands materially different directions.
- **Research:** the optional convergent support skill that establishes bounded decision-relevant facts with sourced evidence and confidence.
- **Explicit invocation:** a direct user or owning-stage request to run Explore or Research, distinct from incidental reasoning or a small local fact check inside another skill.
- **Supporting artifact:** a standalone Git-tracked exploration or research record with no independent lifecycle authority.
- **Decision owner:** the lifecycle stage or other named owner that may adopt, reject, or qualify a supporting conclusion.
- **Established fact:** a claim directly supported by identified evidence of suitable authority and freshness.
- **Inference:** a reasoned conclusion derived from evidence but not directly stated or observed as fact.
- **Assumption:** a proposition used without sufficient evidence and labeled accordingly.
- **Material stopping condition:** the point at which additional option generation or evidence gathering is unlikely to change the supported decision.

## Examples first

Example E1: Small exploration remains proportional
Given a reversible decision has only the current behavior and one credible change
When Explore exposes the decision space
Then it may compare those two materially distinct options without inventing three more alternatives

Example E2: Strategic exploration expands further
Given a difficult-to-reverse product direction has several credible models
When Explore applies the high-impact method
Then it compares as many materially distinct options as needed and identifies factual questions that could alter the comparison

Example E3: Explicit Research remains independently inspectable
Given a Design decision depends on current platform behavior
When Research is explicitly invoked
Then it creates one standalone research artifact with sources, findings, confidence, implications, uncertainty, and a Design handoff

Example E4: A local fact check is not silently promoted
Given a Proposal author confirms one repository-local filename while drafting
When the Research skill was not invoked
Then no Research artifact or Research completion claim is required

Example E5: Explore recommendation remains advisory
Given an exploration identifies one leading option
When the artifact is handed to Proposal
Then Proposal may adopt, reject, or qualify it, and only Proposal Review can approve the resulting proposal direction

Example E6: Research finding remains bounded
Given evidence supports the operating system's per-user state directory
When Research records that conclusion
Then it may recommend the factual answer but does not approve the wider architecture that might use it

Example E7: Explore leads to Research
Given Explore identifies unknown compatibility behavior that could reverse its option ranking
When the owning decision still needs that comparison
Then Research investigates the bounded compatibility question and returns evidence to the same owner

Example E8: Clear work skips discovery
Given the problem, direction, and decision-relevant facts are sufficiently settled
When Route selects the next owner
Then it invokes neither Explore nor Research and creates no discovery artifact

Example E9: Contradiction routes to the owner
Given new research contradicts an accepted specification
When Research completes
Then it records the contradiction and routes it to the specification owner without editing the specification or lifecycle state

Example E10: Package generation preserves shared rules
Given the canonical Explore and Research packages contain the adopted discovery-support block
When supported adapter candidates are generated and installed
Then each package contains its own mapped copy with the same public behavior and no resource path escapes its skill root

## Requirements

| ID | Requirement |
| --- | --- |
| ER-R1 | Current authored and published inventories MUST retain separate public `explore` and `research` skills. |
| ER-R2 | Explore and Research MUST remain optional, explicitly invoked support operations and MUST NOT become mandatory lifecycle stages, independent review gates, settlement owners, or automatic progression steps. |
| ER-R3 | Every explicit Explore or Research invocation MUST create or explicitly revise one standalone Git-tracked supporting artifact; an explicit invocation MUST NOT silently collapse its output into another artifact. |
| ER-R4 | Incidental option consideration or a small local fact check performed by another stage without invoking Explore or Research MUST NOT require a discovery artifact or permit a discovery-completion claim. |
| ER-R5 | Explore MUST answer which materially different directions are available and what would make each suitable or unsuitable for the supported decision. |
| ER-R6 | Explore MUST identify the decision or problem, affected users or systems, established facts, assumptions, unknowns, useful decision criteria, materially distinct options, comparison, questions requiring Research, and recommended handoff. |
| ER-R7 | Explore MUST generate enough materially distinct options to expose the real decision space and MUST NOT require a fixed option count or predefined option taxonomy. |
| ER-R8 | Explore MUST include status quo or deferral when credible and MUST NOT manufacture weak alternatives solely to satisfy process. |
| ER-R9 | Explore MAY identify a leading option or next investigation for consideration but MUST NOT approve product direction, present unsupported factual conclusions as established, freeze system requirements or architecture, create delivery plans, or progress lifecycle state. |
| ER-R10 | A newly created Explore artifact MUST default to an absent repository-relative target under `docs/explorations/YYYY-MM-DD-slug.md`; an existing unrelated target, ambiguous target, unsafe path, or collision MUST stop rather than overwrite. |
| ER-R11 | Research MUST answer which bounded decision-relevant facts can be established with sufficient confidence and what remains uncertain. |
| ER-R12 | Research MUST identify the supported decision, bounded questions, acceptable evidence types, evidence that could change the result, and a material stopping condition before collecting evidence. |
| ER-R13 | Research MUST examine repository evidence before external sources when the answer may already be governed or observable locally, and external evidence MUST be selected for authority, relevance, and freshness. |
| ER-R14 | Research MUST distinguish established evidence, inference, and assumption; record source quality, confidence, decision implications, remaining uncertainty, and recommended handoff; and MUST NOT present unsourced inference as fact. |
| ER-R15 | Research MAY recommend an answer to its bounded question but MUST NOT use that answer to approve or mutate Proposal, Design, Delivery, Implementation, Verify, or another decision owner's artifact or lifecycle state. |
| ER-R16 | A newly created Research artifact MUST default to an absent repository-relative target under `docs/research/YYYY-MM-DD-slug.md`; an existing unrelated target, ambiguous target, unsafe path, or collision MUST stop rather than overwrite. |
| ER-R17 | An exact existing Explore or Research artifact MAY be revised only when explicitly selected and when changed assumptions, evidence, or uncertainty make revision material; revision MUST preserve Git history and MUST NOT silently replace a different artifact. |
| ER-R18 | Every supporting artifact MUST identify its topic, supported decision, owning stage or change when known, inputs examined, important assumptions, remaining uncertainty, and recommended next owner. |
| ER-R19 | Both skills MUST stop when additional work is unlikely to affect the supported decision, required evidence or authority is unavailable, scope would expand materially, the target is unsafe or ambiguous, or owner judgment is required. |
| ER-R20 | Both skills MUST route a contradiction with an approved upstream decision to the owner of that decision and MUST NOT edit the approved artifact unless separately invoked with that stage's authority. |
| ER-R21 | A supporting conclusion MUST gain governed effect only when the owning stage adopts or relies on it in that stage's own artifact and normal review path. |
| ER-R22 | Explore and Research MUST support Proposal, Design, Delivery, Implementation, Verify, or another explicitly identified decision owner without acquiring that owner's authority. |
| ER-R23 | Route MUST select Explore when problem framing, user value, scope, materially different directions, solution-biased framing, reversibility, or an insufficiently understood option space materially blocks the owner. |
| ER-R24 | Route MUST select Research when a material decision depends on uncertain platform or dependency behavior, compatibility or migration constraints, current standards, APIs, policies, prices, external rules, performance, security, scale, or operational facts. |
| ER-R25 | Route MUST select Explore followed by bounded Research when factual questions discovered during option expansion could materially change the comparison. |
| ER-R26 | Route MUST select neither skill when the problem, direction, and decision-relevant facts are sufficiently clear, and MUST NOT auto-run either skill without explicit invocation or higher-priority authority. |
| ER-R27 | Each core `SKILL.md` MUST contain its purpose, routing boundary, authority exclusions, required artifact outcome, stopping conditions, and handoff; Explore additionally owns the proportional-option rule, and Research additionally owns bounded-question, evidence, and confidence rules. |
| ER-R28 | Detailed reframing, option-generation, high-impact decision, source-quality, repository/external research, experiment, and confidence methods MUST be packaged as conditionally loaded references rather than making every invocation load every method. |
| ER-R29 | Each skill MUST use one packaged copy-and-fill asset for its standalone artifact structure; assets MUST own structure only and MUST NOT hide authority, routing, or lifecycle policy. |
| ER-R30 | Missing, unreadable, escaped, contradictory, or mixed-version required resources MUST stop the dependent operation without remembered or invented reconstruction. |
| ER-R31 | `templates/shared/discovery-support.md` MUST become the canonical source for the stable common supporting-artifact, authority, stopping, contradiction, and handoff rules; `specs/skill-contract.md` MUST admit it to the approved shared-block set. |
| ER-R32 | Explore and Research MUST each package a verbatim skill-local copy of the discovery-support block, MUST declare it in the Resource map, and MUST remain independently installable without cross-skill or repository-root resource access. |
| ER-R33 | Repository-owned validation MUST fail when either public copy differs from the canonical discovery-support block, when a required mapped resource is absent or escapes its package, or when a new closed vocabulary accepts an unknown value. |
| ER-R34 | Published skill text MUST describe public behavior without exposing maintainer-only canonical paths, shared-copy mechanics, validator implementation, generated mirror paths, adapter paths, selector constraints, or repository-local examples. |
| ER-R35 | `skills/` MUST remain the only authored skill source; supported Codex, Claude Code, and opencode candidates and release archives MUST derive from canonical skill packages without hand-edited generated skill bodies. |
| ER-R36 | Governing skill and workflow specs, Route guidance, contributor and public documentation, fixtures, validation, examples, benchmark inventories when affected, adapter support metadata, and release checks MUST agree on the refined contract. |
| ER-R37 | Historical Explore and Research artifacts and immutable release archives MUST remain readable and MUST NOT be rewritten; current invocations use the refined paths and contracts without renaming either skill. |
| ER-R38 | Discovery artifacts MUST NOT record secrets, credentials, unnecessary private raw input, or machine-local absolute paths; external evidence handling MUST retain applicable citation and source-use rules. |

## Important scenarios

- Explore finds only two credible directions; the artifact compares two and explains why further alternatives would not be material.
- Explore finds a credible defer option; it includes it without automatically preferring action.
- Research finds repository evidence sufficient; it does not browse externally merely to increase source count.
- Research depends on a volatile external rule; it checks freshness, records the observation date, and lowers confidence or stops when authority cannot be established.
- An explicit invocation resolves an existing unrelated default filename; it stops and requests an exact safe target rather than overwriting.
- A caller explicitly revises an existing research artifact after upstream documentation changes; the revision preserves history and updates confidence and implications.
- Explore or Research supports Verify; it investigates a bounded uncertainty but does not change Verify's verdict or repair implementation.
- A mapped conditional resource is absent from one generated adapter; generation or validation fails before that package is claimed current.
- The canonical shared block and one public copy disagree; drift validation fails even when both Markdown files are individually readable.
- A prior release contains the old five-option Explore contract; the archive remains immutable and current packages adopt proportional options.

## Acceptance conditions

- Developers can distinguish Explore as option expansion and Research as factual uncertainty reduction from their descriptions and core contracts.
- Explicit invocations always leave independently inspectable standalone artifacts at the refined default roots or an explicitly selected safe target.
- Small explorations are accepted without a five-option quota, while difficult decisions may still use five or more materially distinct options.
- Research artifacts contain bounded questions, sourced findings, source quality, confidence, implications, remaining uncertainty, and handoff.
- Neither skill mutates or approves an owning stage's artifact or lifecycle state.
- Route guidance demonstrably covers Explore, Research, both in order, and neither.
- Shared public rules remain byte-consistent across the canonical block and both self-contained packages.
- Canonical, generated, installed, documented, and validated surfaces agree without rewriting history.

## Inputs and outputs

Explore inputs are the problem or decision, intended owner when known, relevant repository or user context, known facts, assumptions, unknowns, and any explicit safe artifact target. Its output is one new or explicitly revised exploration artifact plus a recommended owner handoff.

Research inputs are the supported decision, bounded questions, evidence-changing and stopping conditions, relevant repository sources, applicable external evidence or experiment inputs, intended owner when known, and any explicit safe artifact target. Its output is one new or explicitly revised research artifact plus a recommended owner handoff.

Route inputs are the user's or owning stage's uncertainty and current decision context. Its output is Explore, Research, Explore then Research, neither, or an explicit stop; it does not create the supporting artifact itself.

## State and invariants

- Explore and Research remain separate public identities and on-demand obligations.
- An explicit invocation has one exact standalone artifact target before successful completion.
- Supporting artifacts have no approval, settlement, review-package, lifecycle-transition, or automatic-continuation state.
- The decision owner remains unchanged before and after discovery work.
- Established facts, inference, assumptions, confidence, and remaining uncertainty remain distinguishable.
- Every public package is self-contained and every adopted shared copy matches its canonical source.
- A successful invocation never overwrites an unrelated artifact or changes an upstream governed artifact.

## Error and boundary behavior

- Missing decision or unresolved owner needed for a safe handoff: stop with the missing input.
- Ambiguous or unsafe artifact target: stop without writing or falling back to proposal storage.
- Existing unrelated artifact at the default target: stop without overwrite.
- Required packaged asset or reference missing, unreadable, escaped, contradictory, or mixed-version: stop the dependent operation.
- Research source authority or freshness insufficient for the claim: record reduced confidence and remaining uncertainty, or stop when the decision cannot responsibly use the evidence.
- Evidence contradicts an approved artifact: record the contradiction and route to its owner without mutation.
- Further option generation or evidence collection cannot materially change the decision: stop and hand off the bounded result.
- Adapter generation or installation lacks one mapped resource or has shared-block drift: fail before current-package success is claimed.
- Unknown value in any new closed vocabulary: emit an explicit validation error before consistency checks.

## Boundary model

Boundary model version: boundary-first-v1
Boundary model scope: ER-R1, ER-R2, ER-R3, ER-R4, ER-R5, ER-R6, ER-R7, ER-R8, ER-R9, ER-R10, ER-R11, ER-R12, ER-R13, ER-R14, ER-R15, ER-R16, ER-R17, ER-R18, ER-R19, ER-R20, ER-R21, ER-R22, ER-R23, ER-R24, ER-R25, ER-R26, ER-R27, ER-R28, ER-R29, ER-R30, ER-R31, ER-R32, ER-R33, ER-R34, ER-R35, ER-R36, ER-R37, ER-R38

| Dimension ID | Applicability | Governing requirement IDs | Boundary IDs | Non-applicability rationale |
| --- | --- | --- | --- | --- |
| input-domain | applicable | ER-R3, ER-R4, ER-R5, ER-R6, ER-R7, ER-R8, ER-R10, ER-R11, ER-R12, ER-R16, ER-R17, ER-R23, ER-R24, ER-R25, ER-R26 | BND-INPUT-001 | - |
| state-lifecycle | applicable | ER-R2, ER-R3, ER-R10, ER-R15, ER-R16, ER-R17, ER-R19, ER-R21, ER-R26, ER-R37 | BND-STATE-001 | - |
| identity-authority | applicable | ER-R2, ER-R9, ER-R15, ER-R18, ER-R20, ER-R21, ER-R22, ER-R26 | BND-AUTH-001 | - |
| composition-path | applicable | ER-R3, ER-R20, ER-R21, ER-R25, ER-R27, ER-R28, ER-R29, ER-R30, ER-R31, ER-R32, ER-R35, ER-R36 | BND-COMPOSE-001 | - |
| temporal-retry | applicable | ER-R10, ER-R12, ER-R13, ER-R16, ER-R17, ER-R19, ER-R37 | BND-TEMPORAL-001 | - |
| failure-recovery | applicable | ER-R10, ER-R16, ER-R19, ER-R20, ER-R30, ER-R33 | BND-RECOVERY-001 | - |
| compatibility-migration | applicable | ER-R1, ER-R7, ER-R10, ER-R16, ER-R17, ER-R31, ER-R35, ER-R36, ER-R37 | BND-COMPAT-001 | - |
| external-environment | applicable | ER-R10, ER-R13, ER-R14, ER-R16, ER-R30, ER-R32, ER-R35, ER-R38 | BND-ENV-001 | - |

## Boundary definitions

| Boundary ID | Dimension ID | Governing requirement IDs | Partitions or transitions | Invariants | Outcomes | Owner requirement ID |
| --- | --- | --- | --- | --- | --- | --- |
| BND-INPUT-001 | input-domain | ER-R3, ER-R4, ER-R5, ER-R6, ER-R7, ER-R8, ER-R10, ER-R11, ER-R12, ER-R16, ER-R17, ER-R23, ER-R24, ER-R25, ER-R26 | explicit or incidental work; option, fact, combined, or settled uncertainty; new default, exact revision, ambiguous, unsafe, or colliding target | Explicit invocation has one supported decision and exact safe standalone target; routing follows the material uncertainty. | Explore, Research, both, or neither is selected; unsafe or unresolved input stops. | ER-R3 |
| BND-STATE-001 | state-lifecycle | ER-R2, ER-R3, ER-R10, ER-R15, ER-R16, ER-R17, ER-R19, ER-R21, ER-R26, ER-R37 | absent or existing artifact; new, revised, blocked, or handed-off support work; unchanged governed lifecycle | Support work never creates lifecycle state or approval; unrelated existing artifacts are preserved. | New or exact revision succeeds and hands off; ambiguity, collision, or owner decision stops. | ER-R2 |
| BND-AUTH-001 | identity-authority | ER-R2, ER-R9, ER-R15, ER-R18, ER-R20, ER-R21, ER-R22, ER-R26 | Explore, Research, Route, Proposal, Design, Delivery, Implementation, Verify, or other named owner | Support skills own only their artifacts; the named decision owner alone adopts conclusions and exercises its stage authority. | Advisory result reaches the owner; contradiction or authority ambiguity routes without mutation. | ER-R21 |
| BND-COMPOSE-001 | composition-path | ER-R3, ER-R20, ER-R21, ER-R25, ER-R27, ER-R28, ER-R29, ER-R30, ER-R31, ER-R32, ER-R35, ER-R36 | Explore to owner; Research to owner; Explore to Research to owner; canonical block to local copies; canonical skills to adapters | Reasoning modes remain distinct; public resources stay skill-local; generated output derives from canonical source. | Valid composition produces inspectable handoff and coherent packages; missing or mixed resources block. | ER-R32 |
| BND-TEMPORAL-001 | temporal-retry | ER-R10, ER-R12, ER-R13, ER-R16, ER-R17, ER-R19, ER-R37 | first invocation, duplicate default, explicit revision, stale evidence, refreshed evidence, repeated investigation | No unrelated overwrite; volatile evidence has freshness context; work stops when marginal evidence cannot affect the decision. | New artifact or explicit revision succeeds; collision stops; stale findings are qualified or refreshed. | ER-R17 |
| BND-RECOVERY-001 | failure-recovery | ER-R10, ER-R16, ER-R19, ER-R20, ER-R30, ER-R33 | missing input, missing resource, write failure, source failure, contradiction, drift, corrected retry | Failure cannot grant completion or downstream authority and cannot trigger invented procedure or partial mutation. | Caller supplies a safe target, resource, evidence, or owner decision and retries; otherwise work remains stopped. | ER-R30 |
| BND-COMPAT-001 | compatibility-migration | ER-R1, ER-R7, ER-R10, ER-R16, ER-R17, ER-R31, ER-R35, ER-R36, ER-R37 | historical quota/inline contract; current proportional/standalone contract; old artifact; current package; immutable archive | Skill names remain stable; history remains readable; current generated packages use the refined contract. | Current invocations create refined artifacts; historical records remain non-authoritative evidence and are not rewritten. | ER-R37 |
| BND-ENV-001 | external-environment | ER-R10, ER-R13, ER-R14, ER-R16, ER-R30, ER-R32, ER-R35, ER-R38 | repository evidence, external evidence, offline/unavailable source, filesystem target, canonical/generated/installed package | Paths remain contained; sources are attributable; secrets and host-private data are excluded; installed packages are self-contained. | Suitable local or external evidence supports a bounded finding; unavailable or unsafe environment lowers confidence or blocks. | ER-R38 |

## Selected interactions

| Interaction ID | Governing requirement IDs | Boundary IDs | Hazard | Required composed outcome |
| --- | --- | --- | --- | --- |
| INT-001 | ER-R3, ER-R9, ER-R15, ER-R20, ER-R21, ER-R22 | BND-STATE-001, BND-AUTH-001 | Creating a durable support artifact is mistaken for authority to approve or mutate the supported decision. | The support artifact is preserved and handed off; the decision owner alone adopts it through its normal artifact and review. |
| INT-002 | ER-R6, ER-R12, ER-R14, ER-R25 | BND-INPUT-001, BND-COMPOSE-001, BND-AUTH-001 | Explore's option ranking depends on an uncertain fact and either mode silently makes the whole decision. | Explore emits a bounded question, Research records evidence, and the same owner decides how the comparison changes. |
| INT-003 | ER-R27, ER-R28, ER-R30, ER-R31, ER-R32, ER-R33, ER-R35 | BND-COMPOSE-001, BND-RECOVERY-001, BND-ENV-001 | Shared rules or conditional resources drift across canonical, generated, or installed packages. | Validation fails before package-current claims; correction begins at canonical source and regenerates contained package copies. |
| INT-004 | ER-R10, ER-R16, ER-R17, ER-R19 | BND-INPUT-001, BND-STATE-001, BND-TEMPORAL-001, BND-RECOVERY-001 | A repeated invocation overwrites an unrelated artifact or treats a collision as an exact revision. | Collision stops; only an explicitly selected exact target may be revised with Git history preserved. |
| INT-005 | ER-R12, ER-R13, ER-R14, ER-R19, ER-R38 | BND-TEMPORAL-001, BND-RECOVERY-001, BND-ENV-001 | Volatile or unavailable evidence is presented as a fresh established fact. | Research records freshness and confidence, qualifies remaining uncertainty, and stops when responsible support is impossible. |

## Example ownership

| Example ID | Classification | Governing requirement IDs | Boundary IDs | Regression ID | Discovery gap ID |
| --- | --- | --- | --- | --- | --- |
| E1 | illustration | ER-R7, ER-R8 | BND-INPUT-001 | - | - |
| E2 | illustration | ER-R6, ER-R7, ER-R28 | BND-INPUT-001, BND-COMPOSE-001 | - | - |
| E3 | illustration | ER-R3, ER-R12, ER-R14, ER-R16, ER-R22 | BND-INPUT-001, BND-AUTH-001 | - | - |
| E4 | illustration | ER-R4 | BND-INPUT-001 | - | - |
| E5 | illustration | ER-R9, ER-R21 | BND-AUTH-001 | - | - |
| E6 | illustration | ER-R14, ER-R15 | BND-AUTH-001, BND-ENV-001 | - | - |
| E7 | illustration | ER-R6, ER-R12, ER-R25 | BND-COMPOSE-001 | - | - |
| E8 | illustration | ER-R26 | BND-INPUT-001, BND-STATE-001 | - | - |
| E9 | illustration | ER-R20, ER-R22 | BND-AUTH-001, BND-RECOVERY-001 | - | - |
| E10 | illustration | ER-R31, ER-R32, ER-R33, ER-R35 | BND-COMPOSE-001, BND-ENV-001 | - | - |

## Compatibility and migration

The public skill names remain `explore` and `research`; no invocation rename or lifecycle migration occurs. Current Explore changes from proposal-adjacent or inline output and a fixed five-option taxonomy to standalone `docs/explorations/` artifacts and proportional options. Current Research changes from optional inline output to a standalone artifact for every explicit invocation.

Existing artifacts remain readable historical evidence and need no bulk move or rewrite. Current package generation carries each skill's new assets and references into supported adapters. Tracked adapter support metadata changes only when its current inventory or resource declarations require it; historical release archives remain immutable. Rollback restores the prior coherent canonical skill, shared-block inventory, validators, docs, and generated expectations together, while a published change requires a corrective release.

## Observability

Each completed artifact states the supported decision, inputs, assumptions, uncertainty, confidence where applicable, and recommended next owner, so a reviewer can reconstruct why the support work occurred and what effect it may have. Validation output identifies missing required resources, placeholder remnants, shared-block drift, unsafe paths, unknown closed values, forbidden authority claims, and adapter parity failures.

No telemetry service or mandatory invocation counter is introduced. Post-adoption usefulness is evaluated through representative artifact and routing review, not treated as a runtime metric or a prerequisite for this contract.

## Security and privacy

Artifacts use repository-relative paths and bounded source descriptions. They must not include secrets, tokens, credentials, unnecessary private user input, environment dumps, usernames, hostnames, or machine-local absolute paths. External sources are cited or identified according to applicable evidence policy, and quoted material remains bounded. Packaged resources cannot escape their installed skill roots.

## Accessibility and UX

The capability is text-first. The first sentences and descriptions of both skills state the distinct central question and near-miss boundary. Artifacts use ordinary Markdown headings and tables only where repeated comparison or evidence fields benefit from them. No visual, motor, audio, browser, or interactive UI behavior is introduced.

## Performance expectations

Core skill loading remains bounded: the core file, one small shared support reference, and one output asset are universal; specialized method references load only when their trigger applies. Explore has no minimum option count, source count, page count, or token count. Research stops when additional evidence is unlikely to change the decision. Repository evidence precedes external work when appropriate.

## Edge cases

EC1. A decision has one credible change and status quo: Explore compares two options and does not fabricate more.

EC2. Status quo is not credible because a supported contract must change: Explore explains its exclusion rather than adding a false defer option.

EC3. The problem is solution-biased: Explore reframes the supported decision before comparing options.

EC4. Explore uncovers no factual question capable of changing the comparison: it hands off without invoking Research.

EC5. Repository evidence settles the Research question: Research records it and stops without unnecessary external sources.

EC6. Two authoritative sources disagree: Research records the conflict, lowers confidence, and routes the remaining uncertainty rather than selecting silently.

EC7. An external fact has no stable current source: Research states that it cannot establish the fact with sufficient confidence and identifies the owner decision needed.

EC8. A stage invokes Research for a bounded question during implementation: Research may support the question but cannot change the accepted specification or implementation authority.

EC9. An invocation target already exists for another topic: the skill stops and requests an exact safe path.

EC10. A generated adapter contains `SKILL.md` but omits the artifact asset: resource validation fails before installation or release parity is claimed.

EC11. A shared rule needs stage-specific qualification: the common block remains unchanged and the qualification lives outside it in the owning skill.

EC12. A repository retains an older `.explore.md` beside a proposal: it remains historical and does not redirect current default placement.

## Non-goals

- Merging Explore and Research or creating a generic discovery skill.
- Adding Explore Review, Research Review, approval status, settlement state, lifecycle transitions, or mandatory discovery prerequisites.
- Letting Explore approve direction or Research approve a broader Proposal, Design, Delivery, Implementation, or Verify decision.
- Creating a research database, knowledge base, telemetry service, or invocation-volume target.
- Requiring external research when current repository evidence resolves the question.
- Requiring fixed counts of options, sources, pages, experiments, or tokens.
- Defining implementation milestones, exact test filenames, release versions, publication timing, or post-adoption evaluation evidence in this specification.

## Acceptance criteria

| ID | Criterion |
| --- | --- |
| ER-AC1 | Canonical and generated inventories retain distinct Explore and Research packages with descriptions and core contracts that clearly separate options from evidence. |
| ER-AC2 | Explicit Explore creates a standalone exploration artifact and accepts a proportional option set without a fixed quota. |
| ER-AC3 | Explicit Research creates a standalone research artifact with bounded questions, sourced findings, source quality, confidence, implications, uncertainty, and handoff. |
| ER-AC4 | Stage-local reasoning without explicit invocation requires no discovery artifact and makes no discovery-completion claim. |
| ER-AC5 | Both skills preserve decision-owner authority, route contradictions, and leave governed artifacts and lifecycle state unchanged. |
| ER-AC6 | Route guidance selects Explore, Research, both in order, or neither for the specified uncertainty classes. |
| ER-AC7 | Core files remain focused and conditional method resources load only for their declared triggers; missing required resources fail closed. |
| ER-AC8 | Both self-contained packages carry the artifact asset and a byte-identical discovery-support copy admitted by the skill contract. |
| ER-AC9 | Repository validation rejects shared drift, missing or escaped resources, forbidden authority claims, fixed-option regression, inline-explicit-research regression, and unknown new vocabulary. |
| ER-AC10 | Canonical source, supported adapter candidates, installed trees, documentation, workflow guidance, and release checks agree while historical artifacts and archives remain unchanged. |
| ER-AC11 | Security and privacy checks reject secrets, machine-local paths, and maintainer-only implementation details from published skill content and fixtures. |

## Open questions

None. Exact test organization, implementation milestones, release version, and the separately owned post-adoption usefulness review belong to Delivery and later product follow-up.

## Next artifacts

- Design Review with `docs/architecture/2026-09-03-refine-explore-research-optional-discovery-skills.md`.
- Execution plan after approved Design Review.

## Follow-on artifacts

None yet

## Readiness

Ready for Design Review reconciliation with the architecture. This specification does not authorize planning or implementation until the exact Design package is approved.
