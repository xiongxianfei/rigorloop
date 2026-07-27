# RigorLoop workflow test spec

## Status

- active

Boundary model version: v1
Boundary model scope: R28-R28z

## Related spec and plan

- Spec: [RigorLoop Workflow](rigorloop-workflow.md), approved by focused
  `spec-review-r53` for the three-category exact-runtime capability projection
  discovered during M2 preflight.
- Proposal: [Workflow Refactor](../docs/proposals/2026-05-01-workflow-refactor.md), accepted.
- Historical plan: [Workflow Refactor Execution Plan](../docs/plans/2026-05-03-workflow-refactor.md), done.
- Related follow-on spec: [Learn Artifact Model](learn-artifact-model.md), approved.
- Related follow-on test spec: [Learn Artifact Model test spec](learn-artifact-model.test.md), active.
- Related follow-on spec: [Formal Review Recording](formal-review-recording.md), approved.
- Related follow-on test spec: [Formal Review Recording test spec](formal-review-recording.test.md), active.
- Related amendment proposal: [PR-Self-Contained Lifecycle Completion](../docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md), accepted.
- Completed amendment plan: [PR-Self-Contained Lifecycle Completion Plan](../docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md), done.
- Related amendment proposal: [Review Skill Material Finding Recording](../docs/proposals/2026-05-07-review-skill-material-finding-recording.md), accepted.
- Completed amendment plan: [Review Skill Material Finding Recording Execution Plan](../docs/plans/2026-05-07-review-skill-material-finding-recording.md), done.
- Related amendment spec: [Milestone-Aware Review Handoff](milestone-aware-review-handoff.md), approved.
- Related amendment test spec: [Milestone-Aware Review Handoff test spec](milestone-aware-review-handoff.test.md), active.
- Related amendment spec: [Test-Spec-Review Gate](test-spec-review-gate.md), approved.
- Related amendment test spec: [Test-Spec-Review Gate test spec](test-spec-review-gate.test.md), active.
- Completed amendment plan: [Milestone-Aware Review Handoff Execution Plan](../docs/plans/2026-05-07-milestone-aware-review-handoff.md), done.
- Current amendment proposal: [Single Workflow Lane, Explain-Change Before Verify, and Public Skill Surface Boundary](../docs/proposals/2026-05-08-single-workflow-lane-explain-before-verify.md), accepted.
- Current amendment architecture: [Canonical System Architecture](../docs/architecture/system/architecture.md), approved after architecture-review R1.
- Current amendment plan: [Single Workflow Lane, Explain-Change Before Verify Execution Plan](../docs/plans/2026-05-08-single-workflow-lane-explain-before-verify.md), active after plan-review R2.
- Current amendment change metadata: `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`.
- Historical workflow-refactor architecture: not required for that completed
  slice.
- Boundary-first architecture: [Canonical System Architecture](../docs/architecture/system/architecture.md),
  approved by focused `architecture-review-r25` for the three-category
  correction, with
  [ADR-20260725](../docs/adr/ADR-20260725-boundary-first-proof-modeling.md)
  accepted for the amendment and
  [ADR-20260726](../docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md)
  accepted except for its narrowly superseded writable-child clauses. The
  accepted [stage-envelope transport ADR](../docs/adr/ADR-20260726-stage-authored-artifact-envelope-transport.md)
  owns the read-only and parent-materialization boundary, while the accepted
  [capability-projection ADR](../docs/adr/ADR-20260727-capability-projected-file-change-control.md)
  owning the accepted base exact-runtime selection and file-change proof and
  the accepted [three-category successor ADR](../docs/adr/ADR-20260727-three-category-runtime-feature-projection.md)
  owning the 3/4/89 partition correction.
- Boundary-first plan: [Boundary-First Proof Modeling](../docs/plans/2026-07-25-boundary-first-proof-modeling.md),
  approved by focused `plan-review-r19`.
- Spec-review: approved with no material findings after the PR-self-contained lifecycle completion amendment was added; minor SR-1 asked the test spec to decide how merge-dependent language classification is recorded.
- Plan-review: approved with no material findings for the PR-self-contained lifecycle completion plan. Minor non-blocking note: if README remains unchanged, final affected-surface evidence should mark it unaffected with rationale.

## Input artifact identities

| Input | Path | Status / Review state | Identity |
| --- | --- | --- | --- |
| Feature spec | `specs/rigorloop-workflow.md` | approved by focused spec-review R53 | `sha256:a8b39968fe229a206ba84db281d99301fd57c3f9bb76e2e2933b7cac6f0babdc` |
| Companion skill spec | `specs/skill-contract.md` | approved; unchanged companion | `sha256:a0532f572dc471243c91de9f3dcbf02530ec48e10481af4e2805a904066b31cc` |
| Latest spec review | `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/spec-review-r53.md` | approved | `sha256:290b29912ec1ed1c907bde8a28f15de32d90ce658aaf267f5470cd6b03cd7e1a` |
| Architecture | `docs/architecture/system/architecture.md` | approved by focused architecture-review R25 | `sha256:2c0ce1c8dd97169298f116106564e7fac0ed34d31b2ec1015fc0920e4fc90607` |
| Architecture review | `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/architecture-review-r25.md` | approved | `sha256:6b363e1e973372c802e98b238c38ec30690fb8a8e943916f7e645b3c190b4a84` |
| Boundary ADR | `docs/adr/ADR-20260725-boundary-first-proof-modeling.md` | accepted with scoped transport supersession | `sha256:0bd0cc5b7964b45f61b020b31c6781d360d072e15120feaf2a7f106cae05df15` |
| Transport ADR | `docs/adr/ADR-20260726-stage-authored-artifact-envelope-transport.md` | accepted with scoped capability-projection supersession | `sha256:e357094a48c9a3410cc661d2f5e28c50afd8aa4dcdd375ec074a355103ea8263` |
| Runtime ADR | `docs/adr/ADR-20260726-codex-permission-profile-boundary-harness.md` | accepted with scoped writable-child supersession | `sha256:b80c4a494ae1e08abea77d74fb270a959ebbde5cf5e01e1f8606791f0e0b5434` |
| Capability-projection ADR | `docs/adr/ADR-20260727-capability-projected-file-change-control.md` | accepted base decision; binary clauses superseded narrowly | `sha256:b9d75ea29d528ef0e1f835ab796d6aa6936d362520ce1a424f5f0bb1112568ef` |
| Three-category projection ADR | `docs/adr/ADR-20260727-three-category-runtime-feature-projection.md` | accepted by architecture-review R25 | `sha256:b2d8997a97114f2b055efc2bec627b39c26d4fea95e5b86ae4bacae3a9c724eb` |
| Plan | `docs/plans/2026-07-25-boundary-first-proof-modeling.md` | active; M2 resolution-needed; approved for proof-map synchronization | `sha256:cc224535057c65df91f55e1dc38341f57075e759a74ee540f9ad88be9b8a51e0` |
| Plan review | `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/plan-review-r19.md` | approved | `sha256:87584e97112bce30f589e1077523e50d14510d48df608f5239e1e21344864367` |

## Testing strategy

- Use manual contract review for contributor-facing guidance where the requirement is documentation clarity, source-of-truth alignment, or human-readable workflow semantics.
- Use filesystem-backed integration tests for selector behavior, lifecycle validation, skill validation, generated-output drift, adapter generation, change metadata, and review artifact validation.
- Use focused skill-validator assertions only for stable, machine-checkable skill guidance such as required labels, forbidden stale labels, handoff boundaries, and generated-output drift.
- Use selector-selected targeted proof as the first validation layer for changed paths; use broad smoke only when an authoritative trigger elevates it.
- Treat `specs/rigorloop-workflow.test.md` as a pending proof-map amendment.
  M2 remains blocked until focused spec review approves the three-category
  projection, architecture and plan rereviews approve their synchronized
  projections, exact input identities are recorded, and an independent
  test-spec review approves this proof map.
- Keep deferred project-map lifecycle mechanics out of this test spec except for explicit non-goal checks.
- Treat final learn artifact modeling as a cross-spec alignment point here; detailed session, topic, evidence, classification, and routing proof lives in `specs/learn-artifact-model.test.md`.
- Treat formal review recording as a cross-spec alignment point here; detailed review-artifact fixture coverage lives in `specs/formal-review-recording.test.md`, while this test spec proves the workflow contract does not contradict stage-neutral recording, clean-review settlement, or conditional review-resolution behavior.
- Treat PR-self-contained lifecycle completion as a completed workflow amendment with continuing regression coverage. A merge-dependent language warning is treated as addressed only when a contributor-visible tracked or review-visible surface classifies the wording as a true downstream completion event or stale lifecycle wording requiring correction; the first implementation slice does not need to suppress the warning automatically after classification.
- Treat review skill material-finding recording as a completed review-recording amendment with continuing regression coverage. Detailed fixture coverage lives in `specs/formal-review-recording.test.md` and `specs/review-finding-resolution-contract.test.md`; this test spec proves the workflow-facing contract keeps isolation, broad material-finding recording, governance alignment, shared skill guidance, and scan-first resolution closeout consistent.
- Treat milestone-aware review handoff as a completed standard-workflow routing amendment with continuing regression coverage. Detailed state-vocabulary and handoff-summary coverage lives in `specs/milestone-aware-review-handoff.test.md`; this test spec proves the broader workflow contract does not route clean non-final milestone reviews to final closeout.
- Treat independent test-spec review as a workflow-governance amendment with detailed proof in `specs/test-spec-review-gate.test.md`; this test spec proves the broader workflow contract routes formal test specs through `test-spec-review` before implementation and preserves the test-spec `active` state.
- Treat the single-workflow-lane amendment as the current workflow-governance amendment under test. This test spec owns broad standard-workflow, manual-skill isolation, final closeout, and active change-metadata coverage; `specs/workflow-stage-autoprogression.test.md` owns workflow-managed continuation coverage, `specs/milestone-aware-review-handoff.test.md` owns milestone closeout coverage, and `specs/skill-contract.test.md` owns public skill portability coverage.

## Requirement coverage map

| Requirement IDs | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R1`-`R5`, `R25h` | `T1` | manual | One standard workflow and isolated manual skill invocation guidance |
| `R6`-`R6dc`, `R20`-`R24a`, `R26`, `R27` | `T4`, `T20`, `T29` | manual, integration | Category model, affected-surface alignment, source-of-truth and generated-output boundaries |
| `R6a`-`R6i` | `T20`, `T21` | manual, integration | Standing artifact gates, bootstrap exceptions, project-map no-reliance, architecture-package routing |
| `R7`-`R7b` | `T20`, `T22` | manual, integration | Stable obligation values, trigger behavior, and `Runs for every change` semantics |
| `R7ba`-`R7bf` | `T23` | manual, integration | Periodic `learn`, default nonblocking behavior, session-record closeout, and final learn artifact model linkage |
| `R7c`-`R7w` | `T24`, `T37` | manual, integration | Autoprogression, immediate handoff language, stage-owned authority, tracked-branch review and verify claims |
| `R7qa`-`R7qk` | `T38` | manual, integration | `test-spec-review` gate, active test-spec state, result enums, staleness, upstream routing, and implementation eligibility |
| `R7ea`-`R7es` | `T37` | manual | `authoring-through-plan-review` activation, mandatory durable authorization persistence, isolation, architecture assessment, stop conditions, and completion boundary |
| `R8`-`R8g`, `R8i`, `R8j` | `T2`, `T30` | manual, integration | Planned milestone lifecycle, plan/index coherence, and milestone commits |
| `R8h`-`R8hc` | `T29`, `T30` | manual, integration | PR-self-contained plan lifecycle closeout and true downstream event handling |
| `R8ja`-`R8jb` | `T30`, `T32` | manual, integration | Stale plan state and merge-dependent plan wording classification |
| `R8k`-`R8kg` | `T18`, `T25` | manual, integration | Lifecycle states, stale authoritative artifact handling, PR reference behavior |
| `R8kh`-`R8kj` | `T31`, `T32` | manual, integration | Broader repo-local lifecycle state, review-resolution closeout consistency, and tracked merge-dependent language warnings |
| `R8l`-`R8s` | `T13`, `T17`, `T25` | integration, smoke, manual | Selector-selected proof, CI wrapper semantics, broad-smoke triggers, manual proof records |
| `R9`-`R9b`, `R18`, `R19` | `T13`, `T14`, `T26` | smoke, manual, integration | Routine CI, thin hosted wrapper, and `ci-maintenance` boundary |
| `R10`-`R12f` | `T3`, `T16`, `T27` | manual, integration | Durable reasoning, PR summary, review-resolution closeout, formal review recording triggers, and verify-report conditionality |
| `R12an`-`R12av` | `T27`, `T38` | manual, integration | Stage-neutral detailed-record triggers, material/no-material initial review-record roots, `test-spec-review` record inclusion, and artifact-local status boundary |
| `R12aw`-`R12bdd` | `T33` | manual, integration | Isolation stops handoff, material findings require change-local review records, isolated output fields are complete, and review-output-only settlement is forbidden for material findings |
| `R12be`, `R12bg` | `T34` | integration, manual | Formal review skills share one canonical `Isolation and Recording` block and governance guidance teaches the same broad rule |
| `R12bf` | `T35` | integration, manual | New `review-resolution.md` records remain scan-first while preserving validator-readable fields |
| Milestone-aware review handoff amendment `R1`-`R11b` | `T36` | integration, manual | Planned implementation milestone review routing, same-milestone resolution, state vocabulary, and final closeout readiness boundaries |
| `R13`, `R14`, `R14a`, `R14b` | `T15` | integration | Golden-path skill-validator example and rich-example scope boundary |
| `R15`, `R15a` | `T8`, `T9`, `T10` | integration | Canonical skill validation and intentionally simple rule set |
| `R16` | `T9`, `T10` | integration | Required skill-validator fixture failures |
| `R17`, `R23`, `R24` | `T11`, `T12` | integration | Generated-output determinism and drift failure |
| `R25`, `R25a`-`R25e` | `T5`, `T6`, `T7`, `T15`, `T28` | integration | `change.yaml` schema, required fields, validation records, review state, and active change metadata |
| `R25f`, `R25g` | `T15`, `T16`, `T28` | manual, integration | Narrative in Markdown and reviewer-facing summary in PR text |
| `R25i` | `T39` | static, manual | New workflow-managed change roots select or confirm `YYYY-MM-DD-slug` before creation while preserving legacy roots |

### Boundary-first amendment coverage

| Requirement ID | Covered by | Level | Notes |
| --- | --- | --- | --- |
| `R28`-`R28c`, `R28s`-`R28t` | `T40`, `T41` | unit, integration | Closed core, applicability, extensions, exact fields, IDs, and fail-closed values |
| `R28d`-`R28e`, `R28u`-`R28v` | `T41`, `T42` | integration | Example roles, partitions, transitions, and hazard-selected interactions |
| `R28f`-`R28k`, `R28w` | `T42`, `T43` | integration, manual | Proof mapping and stage-owned review, implementation, sibling, and semantic boundaries |
| `R28l`-`R28o`, `R28r` | `T44`, `T47` | integration, migration | Prospective adoption, grandfathering, synchronized opt-in, parity, and resumption predicate |
| `R28p`-`R28q` | `T40`, `T43` | contract | Six check IDs and cross-spec ownership |
| `R28x` | `T45` | integration | Eight frozen incident fixtures and owning gates |
| `R28y` | `T46`, `T48`-`T58` | integration, e2e | Exact report schema, hermetic behavior inputs, read-only runtime, denial probes, integrity-gated envelope transport, immutable publication, compatibility, preservation, parity, evidence, and aggregate |
| `R28z` | `T47` | integration, migration | Release-tag activation identity, partial-unit rejection, and rollback |

## Example coverage map

| Example | Covered by | Notes |
| --- | --- | --- |
| `E1` | `T13`, `T15` | Golden path example plus structural checks |
| `E2` | `T1` | Manual skill invocation stays isolated |
| `E3` | `T1` | Manual skill output is not workflow completion |
| `E4` | `T2` | Multiple milestone commits may share one PR |
| `E5` | `T2` | Non-milestone work does not require milestone commit subjects |
| `E6` | `T20`, `T22` | Category routing and stage obligations are visible |
| `E7` | `T21` | Project-map absence, staleness, contradiction, or missing area requires refresh or no-map rationale before reliance |
| `E8` | `T27` | Required review-resolution closeout blocks downstream stages and formal review records stay discoverable when triggered |
| `E9` | `T26` | `ci-maintenance` is infrastructure maintenance, not validation execution |
| `E10` | `T23` | `learn` is trigger-based and not a default final per-change stage |
| `E11` | `T29`, `T30` | Completing PR records plan `Done` in both plan index and plan body before review opens |
| `E12` | `T29`, `T30` | True downstream release, deploy, publication, external migration, or unobserved hosted result keeps the plan active |
| `E13` | `T31` | Review-resolution closeout and readiness wording stay self-contained in the PR tree |
| `E14` | `T33` | Isolated review recording follows the finding while handoff stays stopped |
| `E15` | `T35` | Review-resolution remains scan-first and parseable |
| Milestone-aware amendment `E1`-`E6` | `T36` | Clean non-final/final review split, findings loop, ambiguous plan state, plan revision, and lifecycle-closeout distinction |
| `E22` | `T38` | Formal test specs require current approved `test-spec-review` before implementation. |

## Edge case coverage

- A user may invoke one individual skill manually, but that output remains isolated and incomplete as full workflow delivery: `T1`
- Workflow-governance, generated-output, and CI automation changes use the standard workflow when complete delivery is claimed: `T1`, `T25`, `T26`
- Generic workflow content and generated adapter output remain separate: `T4`, `T11`, `T12`
- PRs without automated tests require a no-test rationale: `T3`, `T17`, `T28`
- Routine review feedback can remain in PR or explain-change when it does not create material durable memory: `T16`, `T27`
- Optional `change.yaml` artifact keys may be omitted, but required top-level fields may not: `T5`, `T6`, `T7`, `T28`
- Planned milestones require milestone evidence and commit boundaries even when they share one PR: `T2`
- Manual skill invocations and unplanned single-slice work may use normal commit subjects: `T2`
- Accepted or approved lifecycle artifacts can remain current guidance when readiness text is truthful: `T18`, `T25`
- Final PR text cannot add new authoritative references without renewed verification: `T3`, `T25`, `T28`
- Ordinary non-trivial changes may use `change.yaml` plus `explain-change.md` while review-resolution and verify-report remain conditional: `T16`, `T27`, `T28`
- Formal reviews with no material findings and no detailed-record trigger may settle in the reviewed artifact without empty review artifacts: `T27`
- Formal reviews with no material findings but a stage-owned non-approval outcome still create an indexed detailed review record without requiring empty `review-resolution.md`: `T27`
- Material upstream formal review findings open a review-record root before fixes proceed: `T27`
- The `docs/changes/0001-skill-validator/` example remains richer than the universal minimum: `T15`
- Approved legacy top-level explain artifacts remain valid until retired: `T3`, `T16`
- Historical undated or numbered change roots remain valid legacy records, but new workflow-managed change roots use `YYYY-MM-DD-slug` unless project-local guidance explicitly customizes the convention: `T39`
- `spec-review` and `plan-review` preserve immediate handoff versus downstream readiness: `T24`
- `authoring-through-plan-review` requires durable authorization persistence before activation and pauses on missing, malformed, incomplete, or failed persistence: `T37`
- `explore` and `research` are on-demand support and block only after trigger or dependency reliance: `T22`
- Triggered `learn` closes through the final learn artifact model when a session reaches Frame, or through pre-session scheduled follow-up, deferral, or no-learn rationale when no session runs; it blocks only when a higher-priority artifact makes it blocking: `T23`
- `ci-maintenance` may be skipped when hosted automation already covers the material risk: `T26`
- Missing, stale, contradicted, or incomplete `docs/project-map.md` cannot be relied on without refresh or no-map rationale: `T21`
- Bootstrap proposals without `VISION.md` or `CONSTITUTION.md` must identify the exception in `Vision fit`: `T21`
- Open material review findings block `verify`, final `explain-change`, and `pr`: `T27`
- Isolated material findings require change-local review files even when downstream handoff stops: `T33`
- Isolated material-review output missing required record path, record-before-fixing or reconstruction status, or owner-decision status is incomplete: `T33`
- Shared formal review skill guidance drifts from the canonical source or contains stage-specific text inside the shared block: `T34`
- New scan-first review-resolution guidance removes parseable per-finding labels: `T35`
- A clean review of a non-final planned implementation milestone must not route to final closeout: `T36`
- A lifecycle-closeout milestone must not be treated as an open implementation milestone for final closeout readiness: `T36`
- In-flight work can finish under its starting workflow contract unless it opts in or touches refactored workflow surfaces: `T20`, `T25`
- Draft PRs may run early CI without being review-open, but lifecycle state must synchronize before reviewer action resumes: `T29`
- Reopened PRs and reused branches must satisfy PR-self-contained lifecycle completion before review continues: `T29`
- Release, deploy, package publication, external migration, and unobserved hosted checks are true downstream events that can keep a plan active: `T29`, `T30`
- Tracked wording such as "move to Done after merge" is warning evidence and becomes blocking when the PR already contains the completion evidence: `T30`, `T32`
- A spec may remain `draft` while awaiting spec-review, but if spec-review approves it and downstream artifacts rely on it, the same PR records `approved` before review-ready handoff continues: `T31`
- A formal workflow-managed test spec remains `active`; approval lives in `test-spec-review`, and substantive post-review edits block implementation until re-reviewed: `T38`

## Boundary-first proof map

| Proof obligation ID | Governing requirement IDs | Boundary or interaction IDs | Test case IDs | Automation level | Manual procedure IDs |
| --- | --- | --- | --- | --- | --- |
| `bfp-proof.workflow-canonical` | R28q, R28z | bfp.canonical.workflow-owner, bfp.canonical.skill-projection, bfp.canonical.release-identity | T40, T47 | automated | - |
| `bfp-proof.workflow-identity` | R28f, R28j, R28r, R28z | bfp.identity.exact, bfp.identity.stale, bfp.identity.mismatched-version | T43, T44, T47 | automated | - |
| `bfp-proof.workflow-vocabulary` | R28a-R28e, R28p, R28r-R28y | bfp.vocabulary.known, bfp.vocabulary.unknown, bfp.vocabulary.extension | T40, T41, T44, T46 | automated | - |
| `bfp-proof.workflow-state` | R28d, R28h-R28j, R28l, R28z | bfp.state.continue, bfp.state.pause, bfp.state.activate, bfp.state.rollback | T42, T44, T47 | automated | - |
| `bfp-proof.workflow-authority` | R28d, R28h, R28i, R28l | bfp.authority.owned-rule, bfp.authority.missing-rule, bfp.authority.new-scope | T42, T44 | hybrid | bfp-manual.semantic-authority |
| `bfp-proof.workflow-atomicity` | R28a, R28f, R28x | bfp.mutation.complete, bfp.mutation.partial | T43, T45 | automated | - |
| `bfp-proof.workflow-recovery` | R28a, R28f, R28x | bfp.recovery.retry, bfp.recovery.reconcile, bfp.recovery.stale | T43, T45 | automated | - |
| `bfp-proof.workflow-concurrency` | R28a, R28f | bfp.concurrency.duplicate, bfp.concurrency.conflict, bfp.concurrency.replay | T40, T43 | automated | - |
| `bfp-proof.workflow-composition` | R28e, R28i, R28j, R28x | bfp.composition.direct, bfp.composition.helper, bfp.composition.public-path, bfp.composition.sibling | T42, T45 | hybrid | bfp-manual.composed-path |
| `bfp-proof.workflow-compatibility` | R28l, R28r, R28z | bfp.compatibility.legacy, bfp.compatibility.opt-in, bfp.compatibility.partial, bfp.compatibility.rollback | T44, T47 | automated | - |
| `bfp-proof.workflow-outcome` | R28d, R28h-R28j, R28y | bfp.outcome.pass, bfp.outcome.fail, bfp.outcome.not-run, bfp.outcome.pause | T42, T46 | automated | - |
| `bfp-proof.workflow-evidence` | R28f, R28j, R28k, R28n, R28y | bfp.evidence.current, bfp.evidence.missing, bfp.evidence.stale, bfp.evidence.overclaim | T43, T46 | hybrid | bfp-manual.semantic-evidence |
| `bfp-proof.workflow-stale-authority` | R28f, R28h | bfp.interaction.stale-authority, bfp.identity.stale, bfp.authority.owned-rule | T43 | automated | - |
| `bfp-proof.workflow-partial-retry` | R28f, R28x | bfp.interaction.partial-retry, bfp.mutation.partial, bfp.recovery.reconcile | T45 | automated | - |
| `bfp-proof.workflow-helper-public` | R28e, R28j, R28x | bfp.interaction.helper-public, bfp.composition.helper, bfp.composition.public-path | T42, T45 | hybrid | bfp-manual.composed-path |

## Boundary-first manual procedures

| Manual procedure ID | Automation rationale | Exact steps | Required environment | Evidence artifact | Pass condition | Failure condition | Owning stage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `bfp-manual.semantic-authority` | Applicability and ownership require contract judgment that structural parsing cannot safely score. | Read the governing requirements first; inspect every core and extension row; challenge each `not-applicable` rationale; trace every applicable row to an approved rule; record any inferred or example-owned rule as a finding. | Repository checkout with approved feature spec, latest clean spec review, and current proof map. | Formal spec-review or test-spec-review record citing challenged rows and requirements. | Every applicable behavior is owned by an approved requirement and every non-applicability rationale is defensible. | Any behavior is owned only by an example, validator, plan, or implementation, or any rationale is unsupported. | spec-review and test-spec-review |
| `bfp-manual.composed-path` | Hazard selection and sibling completeness require adversarial inspection across paths, not phrase matching. | Select interactions from the approved rationale set; inspect direct, helper, public, retry, and sibling paths named by each interaction; compare their proof IDs; record every missing path or sibling as a finding. | Repository checkout with feature spec, proof map, implementation diff when available, and path-oriented fixtures. | Test-spec-review or code-review record with interaction IDs, inspected paths, and findings or no-finding rationale. | Every selected interaction has direct proof for all material composed and sibling paths. | A helper substitutes for public-path proof, or a sibling, retry, or direct path remains unproved. | test-spec-review and code-review |
| `bfp-manual.semantic-evidence` | Evidence adequacy and overclaim detection require source-aware review rather than natural-language scoring. | For each cited result, open the repository-visible evidence; verify identity and owner; compare the assertion with the governing boundary; challenge stale, missing, circular, or asserted evidence; record uncertainty as a blocker. | Repository checkout with current artifacts, review records, test output references, and capability-report inputs. | Formal review or verify evidence listing inspected identities and the resulting pass, finding, or blocker. | Every material claim is supported by current owner-derived evidence and no structural result claims semantic completeness. | Evidence is stale, missing, caller-asserted, circular, or broader than what it proves. | spec-review, test-spec-review, code-review, and verify |

## Validation commands

| Command ID | Command | Classification | Owner | Owning milestone | First required milestone | Failure behavior | Zero-test behavior | Evidence artifact | Safe mode / side-effect boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CMD-BFP-1` | `python scripts/test-boundary-proof.py` | planned-for-implementation | boundary model owner | M1 | M1 code-review | nonzero blocks milestone | zero tests is failure | M1 validation notes | repository-local; no network or external mutation |
| `CMD-BFP-2` | `python scripts/validate-boundary-proof.py validate-report docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md` | planned-for-implementation | boundary validator owner | M4 | M4 code-review | nonzero blocks milestone | not applicable | canonical capability report | validation-only; never invokes lifecycle skills |
| `CMD-BFP-3` | `python scripts/test-skill-validator.py` | existing/configured | skill validator owner | M2 and M3 | M2 code-review | nonzero blocks milestone | zero tests is failure | milestone validation notes | repository-local |
| `CMD-BFP-4` | `python scripts/test-select-validation.py` | existing/configured | selector owner | M4 | M4 code-review | nonzero blocks milestone | zero tests is failure | M4 validation notes | repository-local |
| `CMD-BFP-5` | `python scripts/test-adapter-distribution.py` | existing/configured | adapter tooling owner | M4 | M4 code-review | nonzero blocks milestone | zero tests is failure | M4 validation notes | local generation only; no publication |
| `CMD-BFP-6` | `tmpdir="$(mktemp -d)" && python scripts/build-adapters.py --version v0.1.5 --output-dir "$tmpdir" && python scripts/validate-adapters.py --root "$tmpdir" --version v0.1.5` | existing/configured | adapter tooling owner | M4 | M4 code-review | any nonzero result blocks milestone | not applicable | temporary adapter validation output | temporary local output; no registry, release, or publication |
| `CMD-BFP-7` | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path specs/rigorloop-workflow.md --path specs/rigorloop-workflow.test.md --path specs/skill-contract.md --path specs/skill-contract.test.md --path docs/plans/2026-07-25-boundary-first-proof-modeling.md --path docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/change.yaml` | existing/configured | lifecycle validator owner | lifecycle closeout | test-spec-review and verify | blocking result stops handoff | not applicable | validation ledger in change.yaml | read-only repository validation |
| `CMD-BFP-8` | `python scripts/boundary_proof_behavior.py check-environment --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --json` | planned-for-implementation | behavior harness owner | M2 | M2 preflight gate | nonzero or `environment-unavailable` stops M2 before other harness or skill mutation | not applicable | `validation-m2.md`; `evidence/runtime-preflight-attestation.json` | evidence-only, non-secret parent-observed feasibility transaction |
| `CMD-BFP-9` | `tmpdir="$(mktemp -d)" && python scripts/boundary_proof_behavior.py exercise-fixture --fixture tests/fixtures/boundary-proof/behavior/happy-path.json --output-root "$tmpdir" && python scripts/boundary_proof_behavior.py validate-fixture --root "$tmpdir"` | planned-for-implementation | behavior harness owner | M2 | M2 code-review | nonzero blocks milestone | not applicable | temporary controlled-run evidence | isolated temporary workspace; no canonical pointer mutation |
| `CMD-BFP-10` | `python scripts/boundary_proof_behavior.py freeze-baseline --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` | planned-for-implementation | behavior harness owner | M2 | before first participating-skill mutation | nonzero blocks skill mutation | not applicable | `evidence/boundary-proof-baseline.json` | immutable change-local baseline; no lifecycle invocation |
| `CMD-BFP-11` | `python scripts/boundary_proof_behavior.py generate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --scenario tests/fixtures/boundary-proof/simple-change/scenario.json` | planned-for-implementation | behavior harness owner | M2 | M2 code-review | failed/partial publication blocks milestone | not applicable | immutable upstream run and current pointer | read-only isolated child with deny-only file-change handling; parent-only change-local materialization/publication; no external action |
| `CMD-BFP-12` | `python scripts/boundary_proof_behavior.py validate --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` | planned-for-implementation | behavior harness owner | M2 | M2 code-review | nonzero blocks milestone | not applicable | current immutable-run validation | validation-only; no skill reinvocation or profile replacement |
| `CMD-BFP-13` | `python scripts/boundary_proof_behavior.py generate-preservation --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` | planned-for-implementation | behavior harness owner | M3 | M3 code-review | nonzero blocks milestone | not applicable | exact preservation manifest and snapshot roots | reads frozen/current evidence; no upstream reinvocation |
| `CMD-BFP-14` | `python scripts/boundary_proof_behavior.py validate-preservation --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills` | planned-for-implementation | behavior harness owner | M3 | M3 code-review | nonzero blocks milestone | not applicable | 40 preservation results | validation-only; no upstream reinvocation |
| `CMD-BFP-15` | `python scripts/validate-boundary-proof.py generate-report --change-id 2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills --output docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/boundary-capability-baseline.md` | planned-for-implementation | boundary validator owner | M4 | M4 code-review | nonzero blocks milestone | not applicable | canonical capability report | sole report writer; no release activation |
| `CMD-BFP-16` | `python scripts/test-release-transaction.py` | existing/configured | release validator owner | M4 | M4 code-review | nonzero blocks milestone | zero tests is failure | M4 validation notes | repository-local fixtures; no publication |
| `CMD-BFP-17` | `python scripts/validate-release.py --version v0.3.6` | existing/configured | release validator owner | M4 | M4 code-review | nonzero blocks milestone | not applicable | current release validation output | validation-only; does not publish or alter release state |
| `CMD-BFP-18` | `python scripts/validate-skills.py` | existing/configured | skill validator owner | M2 | M2 code-review | nonzero blocks milestone | not applicable | M2 validation notes | repository-local canonical skill validation; no generated or external mutation |
| `CMD-BFP-19` | `python scripts/build-skills.py --check` | existing/configured | skill build owner | M2 | M2 code-review | nonzero or detected drift blocks milestone | not applicable | M2 validation notes | check-only generated-skill projection; no authored-source mutation |
| `CMD-BFP-20` | `python scripts/validate-boundary-proof.py --help` | planned-for-implementation | boundary validator owner | M2 | M2 code-review | nonzero blocks milestone | not applicable | M2 validation notes | CLI import and argument smoke only; no evidence or repository mutation |
| `CMD-BFP-21` | `python -m py_compile scripts/boundary_proof_behavior.py scripts/boundary_proof_model.py scripts/validate-boundary-proof.py scripts/test-boundary-proof.py` | existing/configured | Python implementation owner | M2 | M2 code-review | nonzero blocks milestone | not applicable | M2 validation notes | local bytecode compilation only; no lifecycle invocation or durable evidence mutation |

## Milestone proof map

| Milestone | Required test IDs | Manual proof IDs | Command IDs | Evidence artifacts | Required before | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | T40, T41, T42, T43, T44, T45, T46 | bfp-manual.semantic-authority, bfp-manual.semantic-evidence | CMD-BFP-1 | `scripts/test-boundary-proof.py`; synthetic incident, trace, and report fixtures | M1 code-review | Report tests use synthetic inputs; runtime behavior and the canonical report are deferred. |
| M2 | T41, T42, T43, T48, T49, T50, T51, T52, T55, T56, T57, T58 | bfp-manual.semantic-authority | CMD-BFP-1, CMD-BFP-3, CMD-BFP-8, CMD-BFP-9, CMD-BFP-10, CMD-BFP-11, CMD-BFP-12, CMD-BFP-18, CMD-BFP-19, CMD-BFP-20, CMD-BFP-21 | v3 environment receipt, exact runtime projection and common conformance evidence, immutable baseline, v3 behavior manifest, integrity and transport observations, immutable run, pointer, receipt/rollback fixtures, opaque-v1 and unsupported-v2 proof, skill/build validation, CLI/import smoke | M2 code-review | Closed projection and contrast tests precede the read-only preflight; validated common conformance precedes either capability branch; no live skill mutation proceeds before the complete preflight and baseline gates pass. |
| M3 | T42, T43, T44, T45, T53 | bfp-manual.composed-path, bfp-manual.semantic-evidence | CMD-BFP-1, CMD-BFP-3, CMD-BFP-13, CMD-BFP-14 | exact preservation manifest, before/after roots, and 40 pair results | M3 code-review | Preservation consumes recorded M2 evidence without upstream reinvocation. |
| M4 | T44, T45, T46, T47, T54 | bfp-manual.composed-path | CMD-BFP-1, CMD-BFP-2, CMD-BFP-4, CMD-BFP-5, CMD-BFP-6, CMD-BFP-15, CMD-BFP-16, CMD-BFP-17 | four durable parity manifests, canonical report, release fixtures, and validation output | M4 code-review | R28y report pass is not the later R28o resumption predicate. |
| Final lifecycle closeout | T40, T41, T42, T43, T44, T45, T46, T47 | bfp-manual.semantic-authority, bfp-manual.composed-path, bfp-manual.semantic-evidence | CMD-BFP-1, CMD-BFP-2, CMD-BFP-3, CMD-BFP-4, CMD-BFP-5, CMD-BFP-6, CMD-BFP-7 | clean milestone/final reviews, closed resolution, explanation, verification | verify | Progressive-disclosure review remains paused until R28o passes. |

## Test cases

### T1. Workflow documentation exposes one standard workflow and isolated manual skill use

- Covers: `R1`, `R2`, `R3`, `R4`, `R5`, `R25h`, `E2`, `E3`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `.github/pull_request_template.md`
- Steps:
  - Review contributor-facing docs and confirm they describe one recommended standard workflow.
  - Confirm manual individual skill invocation is described as isolated by default.
  - Confirm manual skill output does not claim omitted upstream or downstream workflow stages are complete.
- Expected result:
  - A contributor can distinguish complete workflow delivery from focused manual skill output without reading chat history.
- Failure proves:
  - The starter kit workflow contract remains implicit or internally inconsistent.
- Automation location:
  - Manual review during M1.

### T2. Planned milestone work rules are visible and unambiguous

- Covers: `R8`, `R8a`, `R8b`, `R8c`, `R8d`, `R8e`, `R8f`, `R8g`, `R8i`, `E4`, `E5`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/examples/plans/example-plan.md`
  - `docs/plan.md`
  - `docs/plans/2026-05-03-workflow-refactor.md`
  - `skills/plan/SKILL.md`
  - `skills/implement/SKILL.md`
- Steps:
  - Confirm milestone closeout evidence, milestone commit format, and multi-milestone PR behavior are described consistently.
  - Confirm manual skill invocations or unplanned single-slice work are explicitly exempt from milestone-formatted commits.
  - Confirm the active plan and plan index remain coherent during milestone progress updates.
- Expected result:
  - Planned milestone work has one clear closeout rule and one clear commit-boundary rule across the repo.
- Failure proves:
  - Milestone planning and implementation guidance can drift into contradictory commit or closeout expectations.
- Automation location:
  - Manual review during M1 and final M4 closeout.

### T3. PR summary and explain-change guidance match the contract

- Covers: `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e`, `R11`, `R12`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `.github/pull_request_template.md`
  - `README.md`
  - `docs/workflows.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
- Steps:
  - Confirm every change requires reviewer-facing summary and validation or no-test rationale.
  - Confirm the split between PR summary, durable Markdown artifacts, and structured metadata is described accurately.
  - Confirm new non-trivial work defaults to `docs/changes/<change-id>/explain-change.md`.
  - Confirm PR text alone is not presented as a substitute for required durable reasoning.
  - Confirm approved legacy top-level explain artifacts remain valid until retired.
- Expected result:
  - Reviewer-facing requirements for summary, validation, artifact links, and durable reasoning location are clear before implementation.
- Failure proves:
  - Contributors may satisfy scripts while omitting required durable reasoning or misusing PR text as the only durable explanation.
- Automation location:
  - Manual review during M1, M2, and M4.

### T4. Root guidance preserves canonical-versus-generated boundaries

- Covers: `R20`, `R20a`, `R21`, `R22`, `R23`, `R24`, `R24a`, `R26`, `R27`
- Level: manual
- Fixture/setup:
  - `README.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - existing architecture source-layout artifact when referenced
- Steps:
  - Confirm root guidance identifies canonical authored paths and generated paths.
  - Confirm generated `.codex/skills/` and `dist/adapters/` output are not presented as hand-edited source of truth.
  - Confirm docs still position Git, pull requests, CI, and human review as authoritative.
- Expected result:
  - Contributors know what may be edited, what is generated, and what repository controls remain authoritative.
- Failure proves:
  - The source-of-truth split is not enforceable in practice.
- Automation location:
  - Manual review during M1 and M4; generated-output checks in `T11` and `T12`.

### T5. Valid `change.yaml` passes metadata validation

- Covers: `R25`, `R25a`, `R25b`, `R25c`, `R25d`, `R25e`
- Level: integration
- Fixture/setup:
  - `schemas/change.schema.json`
  - `scripts/validate-change-metadata.py`
  - `tests/fixtures/change-metadata/valid-basic/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py tests/fixtures/change-metadata/valid-basic/change.yaml`.
- Expected result:
  - The command exits zero and reports the sample metadata file as valid.
- Failure proves:
  - The repository cannot validate the canonical `change.yaml` contract even for a correct sample.
- Automation location:
  - Existing metadata validator tests and final M4 validation.

### T6. Missing required `change.yaml` fields fail validation

- Covers: `R25b`
- Level: integration
- Fixture/setup:
  - invalid fixtures such as `tests/fixtures/change-metadata/missing-title/change.yaml`
  - invalid fixtures such as `tests/fixtures/change-metadata/missing-review/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py <invalid-fixture>` for each missing-field case.
- Expected result:
  - Each invalid file exits non-zero and names the missing required field.
- Failure proves:
  - The metadata validator does not enforce the documented top-level contract.
- Automation location:
  - Existing metadata validator tests and direct fixture validation.

### T7. Malformed validation or review records fail metadata validation

- Covers: `R25d`, `R25e`
- Level: integration
- Fixture/setup:
  - invalid fixtures such as `tests/fixtures/change-metadata/bad-validation-record/change.yaml`
  - invalid fixtures such as `tests/fixtures/change-metadata/bad-review-shape/change.yaml`
- Steps:
  - Run `python scripts/validate-change-metadata.py <invalid-fixture>` for each malformed-record case.
- Expected result:
  - The validator exits non-zero and identifies the invalid validation or review structure.
- Failure proves:
  - `change.yaml` can pass even when it cannot support traceability or review-state inspection.
- Automation location:
  - Existing metadata validator tests and direct fixture validation.

### T8. Canonical skills pass structural validation

- Covers: `R15`, `R15a`, `R23`
- Level: integration
- Fixture/setup:
  - canonical `skills/*/SKILL.md`
  - `scripts/validate-skills.py`
- Steps:
  - Run `python scripts/validate-skills.py` after canonical skill edits.
- Expected result:
  - The canonical `skills/` tree passes validation with no missing metadata, missing required sections, placeholder text, or source-of-truth violations.
- Failure proves:
  - The canonical skill source is not good enough to generate or validate reliably.
- Automation location:
  - M2 and M4 validation.

### T9. Missing metadata or required sections fail skill validation

- Covers: `R15`, `R16`
- Level: integration
- Fixture/setup:
  - `tests/fixtures/skills/valid-basic/`
  - `tests/fixtures/skills/missing-name/`
  - `tests/fixtures/skills/missing-description/`
  - `tests/fixtures/skills/missing-title/`
  - `tests/fixtures/skills/missing-expected-output/`
- Steps:
  - Run `python scripts/test-skill-validator.py`.
- Expected result:
  - The valid fixture passes and each missing-field or missing-section fixture fails for the expected reason.
- Failure proves:
  - The validator cannot enforce the minimum structural skill contract.
- Automation location:
  - `scripts/test-skill-validator.py`

### T10. Duplicate names and placeholder text fail skill validation

- Covers: `R15`, `R16`
- Level: integration
- Fixture/setup:
  - `tests/fixtures/skills/duplicate-name/`
  - `tests/fixtures/skills/placeholder-text/`
  - canonical `skills/`
- Steps:
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/validate-skills.py`.
- Expected result:
  - Duplicate-name and placeholder fixtures fail, and canonical `skills/` contains neither duplicate names nor placeholder markers.
- Failure proves:
  - The validator misses cross-skill or content-quality failures that the first-release contract includes.
- Automation location:
  - `scripts/test-skill-validator.py` and canonical corpus validation.

### T11. Skill and adapter generation is deterministic

- Covers: `R17`, `R20`, `R21`, `R22`, `R23`, `R24a`
- Level: integration
- Fixture/setup:
  - canonical `skills/`
  - generated `.codex/skills/`
  - generated `dist/adapters/`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
- Steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
- Expected result:
  - Generated Codex runtime mirrors and public adapters match canonical skills with no drift.
- Failure proves:
  - Generated compatibility output is not stable enough to review or track in Git.
- Automation location:
  - M2 and M4 generated-output validation.

### T12. Drift check fails on stale or hand-edited generated output

- Covers: `R17`, `R23`, `R24`
- Level: integration
- Fixture/setup:
  - a deliberately edited or stale file under `.codex/skills/` or `dist/adapters/`
  - generator `--check` mode
- Steps:
  - Introduce a controlled mismatch in a temp copy or fixture.
  - Run the matching generator `--check` command.
- Expected result:
  - The drift check exits non-zero and identifies the canonical and generated paths that diverged.
- Failure proves:
  - Generated output can drift silently from canonical source.
- Automation location:
  - Existing generator tests and direct `--check` invocation.

### T13. Repository CI wrapper runs selected structural checks

- Covers: `R8l`, `R8m`, `R8n`, `R8o`, `R8p`, `R8q`, `R9`, `R18`, `R19`, `E1`
- Level: smoke
- Fixture/setup:
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - changed paths from this refactor
- Steps:
  - Run `python scripts/select-validation.py --mode explicit --path <changed-path>...`.
  - Run `bash scripts/ci.sh --mode explicit --path <changed-path>...`.
  - Confirm selected checks use stable check IDs and do not imply broad smoke by default.
- Expected result:
  - Selector-selected proof classifies changed paths, chooses stable check IDs, and the CI wrapper executes the selected checks.
- Failure proves:
  - Targeted validation cannot support review handoff for workflow-governance changes.
- Automation location:
  - M1, M3, and M4 validation.

### T14. GitHub CI workflow stays a thin wrapper over repo-owned commands

- Covers: `R9`, `R18`, `R19`, `R27`
- Level: manual
- Fixture/setup:
  - `.github/workflows/ci.yml`
  - `scripts/ci.sh`
- Steps:
  - Inspect the workflow definition and confirm it calls the repo-owned script.
  - Confirm hosted workflow logic does not redefine validation behavior inconsistently with `scripts/ci.sh`.
- Expected result:
  - GitHub Actions delegates to repository-owned validation logic.
- Failure proves:
  - CI logic may drift between hosted automation and repository scripts.
- Automation location:
  - Manual workflow review during M4.

### T15. Golden-path skill-validator artifacts remain coherent

- Covers: `R13`, `R14`, `R14a`, `R14b`, `R25f`, `R25g`, `E1`
- Level: integration
- Fixture/setup:
  - `docs/changes/0001-skill-validator/`
  - `docs/changes/0001-skill-validator/change.yaml`
  - top-level proposal/spec/architecture artifacts
- Steps:
  - Confirm the example artifact directory contains proposal, spec, plan, test-spec, verify report, explain-change, and `change.yaml`.
  - Run `python scripts/validate-change-metadata.py docs/changes/0001-skill-validator/change.yaml`.
  - Confirm repository guidance does not present the `0001` artifact set as the minimum pack for every non-trivial change.
- Expected result:
  - The proof-of-value example remains coherent and clearly richer than the ordinary baseline pack.
- Failure proves:
  - The advertised golden path is incomplete, invalid, or misleading.
- Automation location:
  - Existing metadata validation and manual artifact review.

### T16. Durable reasoning and reviewer-facing explanation stay visible

- Covers: `R10`, `R10a`, `R10b`, `R10c`, `R10d`, `R10e`, `R11`, `R12`, `R12b`, `R12ca`, `R12d`, `R12e`, `R12f`
- Level: manual
- Fixture/setup:
  - `.github/pull_request_template.md`
  - `docs/workflows.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - current change-local pack when created
- Steps:
  - Confirm PR-facing guidance asks for summary, why, validation, risk, and artifact links.
  - Confirm non-trivial work has a durable Markdown reasoning surface.
  - Confirm review-resolution and verify-report remain conditional and concise.
- Expected result:
  - Reviewers can find summary, rationale, validation, and review disposition without reverse-engineering commit history.
- Failure proves:
  - The repository can pass automation while hiding reasoning from humans.
- Automation location:
  - Manual review during M1, M2, and M4.

### T17. Baseline validation works without secrets, network, or Codex installation

- Covers: security/privacy and boundary behavior sections, `R8r`, `R8s`
- Level: smoke
- Fixture/setup:
  - local shell with no repository secrets exported
  - baseline validation scripts
- Steps:
  - Run baseline validation commands in a normal local environment without providing secrets.
  - Confirm they operate only on repository files and do not require Codex runtime installation or external network access.
  - For any manual proof record, confirm check, result, performer, date, evidence, and `manual by design` rationale are recorded.
- Expected result:
  - Baseline structural validation and manual proof recording are locally reproducible.
- Failure proves:
  - The validation surface is more operationally fragile than the contract allows.
- Automation location:
  - M4 verification.

### T18. Validation failures are specific and contributor-actionable

- Covers: observability requirements, `R8k`-`R8kg`
- Level: integration
- Fixture/setup:
  - one invalid skill fixture
  - one invalid metadata fixture
  - stale lifecycle artifact fixture or controlled lifecycle inconsistency
  - one stale generated output file
- Steps:
  - Run the relevant validator, lifecycle validator, and drift check against failing cases.
  - Inspect exit codes and failure messages.
- Expected result:
  - Each failure is non-zero and names the file, fixture, skill, path, lifecycle state, or missing field that caused the error.
- Failure proves:
  - Contributors will struggle to fix failures even if enforcement logic exists.
- Automation location:
  - `scripts/test-skill-validator.py`, `scripts/test-artifact-lifecycle-validator.py`, generator checks, and direct validator invocations.

### T19. Repository-scale performance smoke stays proportional

- Covers: performance expectations from the workflow spec
- Level: manual
- Fixture/setup:
  - current repository tree
- Steps:
  - Run the main validation commands on the repository-sized fixture set.
  - Record rough local wall-clock behavior if noticeably slow.
- Expected result:
  - Validation behaves like linear filesystem work and does not require a build service, cache, or database.
- Failure proves:
  - The implementation is more operationally heavy than the workflow contract allows.
- Automation location:
  - Manual smoke check before final `verify`.

### T20. Workflow category model and affected surfaces are visible

- Covers: `R6`, `R6d`, `R6da`, `R6db`, `R20`-`R24a`, `R26`, `R27`, `E6`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `README.md`
  - `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `docs/changes/2026-05-05-pr-self-contained-lifecycle-completion/change.yaml` when created
- Steps:
  - Confirm the workflow summary and affected guidance expose standing artifacts, living references, workflow infrastructure, on-demand artifacts, per-change chain, and periodic artifacts.
  - Confirm workflow-governance surfaces are updated, explicitly marked unaffected with rationale, or recorded as deferred with owner and follow-up.
  - Confirm unaffected/deferred records live in tracked or review-visible surfaces and not chat-only notes.
  - Confirm the in-flight selected workflow contract is recorded as `refactored` where it affects review.
- Expected result:
  - Contributors can see the category model and reviewers can audit affected-surface disposition without reading chat history.
- Failure proves:
  - The core workflow refactor remains hidden in scattered prose or unreviewable chat-only state.
- Automation location:
  - Manual review during M1 and M4, plus lifecycle validation where applicable.

### T21. Standing artifact gates and project-map no-reliance rule are enforced in guidance

- Covers: `R6a`, `R6b`, `R6c`, `R6e`, `R6f`, `R6g`, `R6h`, `R6i`, `E7`
- Level: manual, integration
- Fixture/setup:
  - `docs/workflows.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/architecture/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Steps:
  - Confirm `VISION.md` and `CONSTITUTION.md` have distinct absence gates and bootstrap exceptions.
  - Confirm bootstrap proposals must identify the exception in `Vision fit` and proposal-review checks it.
  - Confirm consumers must not rely on absent, known-stale, contradicted, or incomplete `docs/project-map.md` without refresh or no-map rationale.
  - Confirm no calendar freshness threshold, freshness marker, or full project-map lifecycle workflow is introduced.
  - Confirm architecture-stage references still route to the architecture package method when architecture is required.
- Expected result:
  - Standing artifact gates and project-map no-reliance behavior are explicit without expanding the deferred project-map lifecycle.
- Failure proves:
  - Contributors can proceed on nonexistent standing artifacts or stale repository maps without recorded rationale.
- Automation location:
  - Manual review during M1 and M2; focused skill-validator assertions if M3 makes the wording stable enough.

### T22. Stage obligations use stable values and triggers

- Covers: `R7`, `R7a`, `R7b`, `E6`
- Level: manual, integration
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `scripts/test-skill-validator.py` if focused assertions are added
- Steps:
  - Confirm obligation values are exactly `mandatory`, `conditional`, `on-demand`, and `periodic`.
  - Confirm the stage-obligation table includes stage/action, role, obligation, trigger, `Runs for every change`, and downstream blocking.
  - Confirm `explore` and `research` are on-demand and not default prerequisites.
  - Confirm the `Runs for every change` column applies only after the row trigger makes a stage applicable and does not override stage triggers.
  - Confirm downstream blocking for conditional, on-demand, and periodic rows follows trigger/dependency/higher-priority-artifact rules.
- Expected result:
  - Readers can tell which actions run for every change and which block only after the relevant trigger or dependency.
- Failure proves:
  - The refactor still leaves mandatory, optional, and triggered work ambiguous.
- Automation location:
  - Manual review during M1/M2 and focused assertions during M3 if stable.

### T23. Triggered learn uses final learn surfaces without becoming a default stage

- Covers: `R7ba`, `R7bb`, `R7bc`, `R7bd`, `R7be`, `R7bf`, `E10`
- Level: manual, integration
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `specs/learn-artifact-model.md`
  - `specs/learn-artifact-model.test.md`
  - `docs/workflows.md`
  - active plan and change-local pack
- Steps:
  - Confirm `learn` is periodic or explicitly invoked, not a default final per-change stage.
  - Confirm triggers include cadence, incident response, contributor observation, repeated findings, blocker or major workflow-process findings, failed release or adapter smoke, accepted postmortem actions, and maintainer request.
  - Confirm a `learn` invocation that reaches Frame creates or updates `docs/learn/sessions/YYYY-MM-DD-<slug>.md`, including empty or no-durable-lesson sessions.
  - Confirm durable topic guidance is routed to `docs/learn/topics/<topic>.md` only when confirmed durable lessons justify it.
  - Confirm action-changing lessons route to the authoritative affected artifact rather than treating topic files as policy.
  - Confirm pre-session no-record closeout is allowed only when `learn` does not actually run as a session.
  - Confirm triggered learn blocks downstream only when a higher-priority artifact explicitly makes it blocking.
- Expected result:
  - Ordinary PR closeout does not block on learn by default, but triggered learning uses tracked final learn surfaces once a session runs.
- Failure proves:
  - `learn` either becomes process theater for every change, loses required durable follow-up, or falls back to superseded temporary surfaces.
- Automation location:
  - Manual review during M1/M2 and final M4 change-local evidence review.

### T24. Workflow handoff and stage-owned authority stay distinct

- Covers: `R7c`-`R7w`
- Level: manual, integration
- Fixture/setup:
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/pr/SKILL.md`
  - `scripts/test-skill-validator.py` if focused assertions are added
- Steps:
  - Confirm workflow-managed flows and isolated stage requests are distinguished.
  - Confirm `spec-review` separates outcome, immediate next repository stage, and eventual `test-spec` readiness.
  - Confirm `plan-review` preserves `test-spec` as the immediate next handoff.
  - Confirm `implement`, `code-review`, `verify`, and `pr` each use only their owned readiness language.
  - Confirm branch-scoped clean review or branch-ready claims require tracked governing authority and direct proof for named edge cases.
- Expected result:
  - Stage outputs cannot skip required handoffs or claim authority owned by a later stage.
- Failure proves:
  - The workflow can appear ready by language rather than by required evidence.
- Automation location:
  - Manual review during M2; focused skill-validator assertions during M3 if stable.

### T25. Selector, lifecycle, and broad-smoke behavior match the refactor

- Covers: `R8k`-`R8kg`, `R8l`-`R8s`
- Level: integration
- Fixture/setup:
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - `scripts/test-select-validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - active plan and touched lifecycle artifacts
- Steps:
  - Run `python scripts/test-select-validation.py`.
  - Run `python scripts/test-artifact-lifecycle-validator.py`.
  - Run explicit-path lifecycle validation over the accepted proposal, approved spec, active test spec, plan index, and active plan.
  - Run selector-selected explicit CI over changed paths.
  - Confirm broad smoke is not required unless selector mode, explicit flag, plan, test spec, review-resolution, or release metadata elevates it.
- Expected result:
  - Targeted proof and lifecycle validation cover the changed surfaces, and broad smoke remains trigger-based.
- Failure proves:
  - Review handoff may either under-validate touched artifacts or require broad smoke without authority.
- Automation location:
  - M3 and M4 validation.

### T26. CI-maintenance is distinct from validation execution

- Covers: `R9`, `R9a`, `R9b`, `E9`
- Level: manual, integration
- Fixture/setup:
  - `docs/workflows.md`
  - `AGENTS.md`
  - `skills/ci-maintenance/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `skills/verify/SKILL.md`
- Steps:
  - Confirm contributor-facing workflow guidance uses `ci-maintenance` for hosted CI workflow files, validation automation, or platform configuration.
  - Confirm validation execution stays under `verify` and repository-owned scripts.
  - Confirm `skills/ci-maintenance/` is the CI infrastructure skill entrypoint.
  - Confirm guidance does not describe `ci-maintenance` as running tests, designing tests, specifying validation commands, or waiting for existing CI checks.
- Expected result:
  - Contributors can tell when CI infrastructure maintenance is required and when ordinary validation belongs to `verify`.
- Failure proves:
  - The ambiguous `ci` stage remains conflated with validation execution.
- Automation location:
  - Manual review during M1/M2 and focused skill assertions during M3 if stable.

### T27. Review-resolution closeout blocks downstream stages when required

- Covers: `R12a`-`R12f`, `R12an`-`R12av`, `E8`
- Level: manual, integration
- Fixture/setup:
  - `specs/formal-review-recording.md`
  - `specs/formal-review-recording.test.md`
  - `specs/review-finding-resolution-contract.md`
  - `docs/workflows.md`
  - `skills/code-review/SKILL.md`
  - `skills/verify/SKILL.md`
  - `skills/explain-change/SKILL.md`
  - `skills/pr/SKILL.md`
  - `scripts/test-review-artifact-validator.py`
  - `scripts/validate-review-artifacts.py`
  - review artifacts under `docs/changes/<change-id>/` when material findings exist
- Steps:
  - Confirm material findings require evidence, required outcome, and safe resolution or `needs-decision` rationale.
  - Confirm detailed formal lifecycle review records are stage-neutral across `proposal-review`, `spec-review`, `architecture-review`, `plan-review`, and `code-review`.
  - Confirm detailed review records are required for material findings, stage-owned non-approval outcomes that block downstream progress or require revision, reconstructed evidence, closeout-evidence citation, and explicit reviewer or maintainer request.
  - Confirm clean required formal reviews can settle in the reviewed artifact when no detailed-record trigger applies.
  - Confirm no-material detailed records require `review-log.md` but do not require an empty `review-resolution.md` solely because `reviews/` exists.
  - Confirm material initial review-record roots include `review-resolution.md`, while no-material initial roots do not.
  - Confirm `review-resolution.md` dispositions are limited to approved values.
  - Confirm `needs-decision`, `Closeout status: open`, missing disposition evidence, or open `review-log.md` findings block `verify`, final `explain-change`, and `pr`.
  - If this amendment creates material findings, run `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-05-pr-self-contained-lifecycle-completion`.
  - Run `python scripts/test-review-artifact-validator.py` when validator behavior is changed or relied on for a new review artifact assertion.
- Expected result:
  - Required review-resolution closeout cannot be skipped or silently replaced by implementation fixes alone, and no-material review events remain discoverable without empty resolution files.
- Failure proves:
  - Material review findings or upstream non-approval review events can be lost between formal review and final PR readiness.
- Automation location:
  - M4 when review-resolution is triggered; validator tests only when review-artifact validation changes or is explicitly selected.

### T28. Active workflow-governance change metadata is valid and traceable

- Covers: `R25`, `R25a`-`R25h`, `R10`-`R12f`
- Level: integration, manual
- Fixture/setup:
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/explain-change.md` when created
  - historical workflow change metadata only when relied on as background evidence
  - optional review-resolution or verify-report artifacts if triggered
- Steps:
  - Create the baseline non-trivial change-local pack before final `verify`.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`.
  - Confirm `change.yaml` links the proposal, spec, active test spec, active plan, touched artifacts, validation records, and review state.
  - Confirm Markdown artifacts carry narrative rationale and PR text remains the reviewer-facing summary.
- Expected result:
  - Reviewers can trace the current workflow-governance change through structured metadata plus durable Markdown reasoning.
- Failure proves:
  - The active change has machine-readable metadata but insufficient human-readable rationale, or vice versa.
- Automation location:
  - M4 validation and final `verify`.

### T29. PR-self-contained lifecycle guidance is visible and bounded

- Covers: `R6dc`, `R8h`-`R8hc`, `E11`, `E12`
- Level: manual
- Fixture/setup:
  - `CONSTITUTION.md`
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`
  - `docs/examples/plans/example-plan.md`
  - `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
- Steps:
  - Confirm `CONSTITUTION.md` states that lifecycle synchronization happens in the PR performing the transition before review opens, and that merge is a fast-forward of pre-validated state rather than a trigger for further lifecycle changes.
  - Confirm `docs/workflows.md`, affected skills, and learn/topic guidance no longer present routine merge-dependent `Done` as an allowed plan closeout path.
  - Confirm guidance keeps true downstream completion events, such as release, deploy, package publication, external migration, or unobserved hosted checks, out of repo-local lifecycle state.
  - Confirm draft PRs, reopened PRs, and reused branches synchronize repo-local lifecycle state before reviewers are asked to judge the branch.
  - Confirm README is either updated or explicitly recorded as unaffected with rationale in the active plan or change-local evidence.
- Expected result:
  - Contributors can tell when to close lifecycle state in the current PR and when to leave a plan active for a true downstream event.
- Failure proves:
  - The repository can keep the old post-merge memory dependency alive through lower-priority guidance.
- Automation location:
  - Manual review during M1 and final M4 affected-surface review.

### T30. Plan index/body lifecycle validation catches stale state

- Covers: `R8h`-`R8hc`, `R8j`-`R8jb`, `E11`, `E12`
- Level: integration
- Fixture/setup:
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/validate-artifact-lifecycle.py`
  - fixture repositories under `tests/fixtures/artifact-lifecycle/`
  - temporary `docs/plan.md` and `docs/plans/*.md` files
- Steps:
  - Add failing coverage for a completed, blocked, or superseded plan still listed under `## Active` in `docs/plan.md`.
  - Add failing coverage for `docs/plan.md` and the referenced plan body presenting conflicting lifecycle state.
  - Add failing coverage for a done, blocked, or superseded plan body whose readiness still describes the plan as active or in progress.
  - Add passing coverage for an active plan that names a true downstream completion event or follow-up condition.
  - Add warning coverage for tracked plan lifecycle wording that implies lifecycle closeout after merge.
  - Run `python scripts/test-artifact-lifecycle-validator.py`.
  - Run `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`.
- Expected result:
  - Stale plan/index lifecycle state is blocking, true downstream-event wording is allowed, and merge-dependent lifecycle wording is visible as reviewer-attention output unless the same evidence is also blocking.
- Failure proves:
  - Plans can still land with stale Active/Done state or hidden merge-dependent closeout promises.
- Automation location:
  - M2 lifecycle validator implementation and M4 final validation.

### T31. Broader repo-local lifecycle inconsistency blocks branch-ready

- Covers: `R8kh`, `R8ki`, `E13`
- Level: integration, manual
- Fixture/setup:
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/review_artifact_validation.py`
  - `scripts/test-review-artifact-validator.py`
  - lifecycle-managed proposal, spec, test-spec, architecture, or ADR fixtures as needed
  - review artifacts under `docs/changes/<change-id>/`
- Steps:
  - Add fixture or manual proof for a lifecycle-managed proposal, spec, test spec, architecture document, or ADR whose status conflicts with relied-on PR-contained evidence.
  - Add fixture or manual proof for active readiness wording in a test spec, verify report, explain-change artifact, or change-local artifact after the PR has completed and recorded its own scope.
  - Add review-artifact proof that `review-resolution.md` cannot say `Closeout status: open` after all material findings have final dispositions and required evidence.
  - Add review-artifact proof that `Closeout status: closed` fails when required findings, dispositions, rationale, follow-up, validation evidence, or `review-log.md` closeout evidence are missing.
  - Run `python scripts/test-artifact-lifecycle-validator.py` and `python scripts/test-review-artifact-validator.py` when either validator is changed or relied on for this proof.
- Expected result:
  - Broader lifecycle artifact inconsistency blocks `branch-ready` for touched, referenced, generated, or authoritative artifacts, while unrelated stale baseline artifacts remain warnings.
- Failure proves:
  - The PR tree can claim current readiness while authoritative lifecycle artifacts still describe an earlier or incomplete state.
- Automation location:
  - M2 lifecycle/review-artifact validator implementation and M4 final verification.

### T32. Tracked merge-dependent language is warned and classified

- Covers: `R8jb`, `R8kj`
- Level: integration, manual
- Fixture/setup:
  - tracked Markdown or YAML files containing lifecycle wording such as "after merge", "post-merge", or "once this lands"
  - `scripts/artifact_lifecycle_validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - contributor-visible classification surfaces: the same tracked artifact, the active plan, `docs/changes/<change-id>/change.yaml`, `docs/changes/<change-id>/explain-change.md`, a formal review record, PR body, or draft PR body
- Steps:
  - Add warning coverage for tracked merge-dependent lifecycle wording.
  - Confirm the warning names the tracked file and remains non-blocking unless another lifecycle inconsistency makes the same evidence blocking.
  - Confirm first-slice detection inspects tracked files and does not require hosted PR-description event metadata.
  - Confirm any remaining merge-dependent language warning is treated as addressed only when a contributor-visible tracked or review-visible surface classifies it as a true downstream completion event or stale lifecycle wording requiring correction.
  - Do not require the validator to suppress the warning after classification in this first slice.
- Expected result:
  - Reviewers see merge-dependent lifecycle wording, and contributors must classify it before branch-ready or PR handoff treats the warning as addressed.
- Failure proves:
  - Merge-dependent lifecycle language can either hide in tracked files or be dismissed without a durable classification.
- Automation location:
  - M2 warning fixtures, M3 selector routing if needed, and M4 manual affected-surface review.

### T33. Isolated formal review output stops handoff but requires material-finding recording

- Covers: `R12aw`-`R12bdd`, `E14`
- Level: manual, integration
- Fixture/setup:
  - `specs/formal-review-recording.md`
  - `specs/formal-review-recording.test.md`
  - `templates/shared/review-isolation-and-recording.md`
  - formal review skills under `skills/`
  - `scripts/test-skill-validator.py`
  - `scripts/test-review-artifact-validator.py`
- Steps:
  - Confirm workflow-facing guidance states that isolation governs handoff only and does not suppress material-finding recording.
  - Confirm every material finding requires a durable change-local review record under `docs/changes/<change-id>/reviews/`, whether workflow-managed or isolated.
  - Confirm isolated material-review output names handoff status, material Finding IDs, required record path, whether the record must be created before fixing or reconstructed, and whether owner decision is needed.
  - Confirm the output makes the next action clear without requiring enum-style action strings.
  - Confirm isolated material-review output does not offer review-output-only or artifact-local-only settlement for material findings.
- Expected result:
  - A contributor can stop after a direct review while still seeing exactly what durable record is required before any material finding is acted on.
- Failure proves:
  - Isolation can again be misread as no recording, or the review output omits the action needed to preserve first-pass evidence.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `python scripts/test-review-artifact-validator.py`
  - manual review during M1 and M4

### T34. Formal review skills and governance share the canonical broad recording rule

- Covers: `R12be`, `R12bg`
- Level: integration, manual
- Fixture/setup:
  - `templates/shared/review-isolation-and-recording.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/spec-review/SKILL.md`
  - `skills/architecture-review/SKILL.md`
  - `skills/plan-review/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Assert all five formal review skills contain one byte-identical `## Isolation and Recording` block copied from the canonical template.
  - Assert stage-specific content appears outside the shared block.
  - Assert `CONSTITUTION.md`, `AGENTS.md`, and `docs/workflows.md` use the same rule: every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.
  - Assert implementation does not proceed with canonical skill changes until affected governance and operating guidance are aligned or explicitly marked unaffected with rationale.
- Expected result:
  - The workflow contract, formal review skills, and contributor-facing governance surfaces teach one rule without stage-specific drift.
- Failure proves:
  - Guidance can drift across review stages or higher-priority governance surfaces.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - `bash scripts/ci.sh --mode explicit ...`
  - manual M1/M4 affected-surface review

### T35. Scan-first review-resolution remains parseable at workflow handoff

- Covers: `R12bf`, `E15`
- Level: integration, manual
- Fixture/setup:
  - `specs/review-finding-resolution-contract.md`
  - `specs/review-finding-resolution-contract.test.md`
  - `templates/review-resolution.md` or another approved durable guidance surface
  - `scripts/test-review-artifact-validator.py`
  - `docs/changes/2026-05-07-review-skill-material-finding-recording/review-resolution.md` as current scan-first example evidence
- Steps:
  - Confirm new or revised review-resolution guidance starts with closeout status, covered reviews, resolved and unresolved counts, and final result.
  - Confirm it includes a resolution overview and can use common metadata and shared validation evidence to avoid repeated prose.
  - Confirm each material finding detail keeps parseable labels required by the review finding resolution contract.
  - Confirm `explain-change`, `verify`, and `pr` guidance summarize review-resolution counts and link details instead of duplicating every finding.
- Expected result:
  - Workflow handoff can rely on human-readable review closeout without weakening closeout validation.
- Failure proves:
  - Readability guidance either became too prose-heavy to scan or lost validator-readable finding fields.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-07-review-skill-material-finding-recording`
  - manual M2/M4 review

### T36. Milestone-aware review handoff qualifies clean-review routing

- Covers: milestone-aware review handoff amendment `R1`-`R11b`, amendment `E1`-`E6`
- Level: integration, manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `specs/workflow-stage-autoprogression.md`
  - `specs/milestone-aware-review-handoff.md`
  - `specs/milestone-aware-review-handoff.test.md`
  - `docs/workflows.md`
  - `skills/implement/SKILL.md`
  - `skills/code-review/SKILL.md`
  - `skills/plan/SKILL.md`
  - `skills/workflow/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Confirm workflow-managed standard routing distinguishes milestone-based plans from non-milestone implementation slices.
  - Confirm `implement` records `review-requested` handoff for the current implementation milestone rather than whole-plan final closeout readiness.
  - Confirm clean `code-review` closes the reviewed milestone directly when no review-resolution is required.
  - Confirm clean non-final milestone reviews route to the next in-scope implementation milestone, while clean final milestone reviews route to `ci-maintenance` when triggered; otherwise `explain-change`.
  - Confirm findings, accepted fixes, re-review, inconclusive review, ambiguous plans, and lifecycle-closeout milestones preserve the approved same-milestone and final closeout readiness boundaries.
- Expected result:
  - The workflow contract prevents clean-review routing from reaching final closeout when later implementation milestones remain.
- Failure proves:
  - Planned milestone work can still skip required implementation or review-resolution gates.
- Automation location:
  - `python scripts/test-skill-validator.py`
  - manual M2/M3 review

### T37. Authoring-through-plan-review policy is durable and bounded

- Covers: `R7ea`-`R7es`
- Level: manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `specs/workflow-stage-autoprogression.md`
  - `specs/workflow-stage-autoprogression.test.md`
  - `docs/changes/<change-id>/change.yaml`
  - `docs/changes/<change-id>/workflow-policy.yaml`
  - profile-managed output or activation audit trail for a candidate change
- Steps:
  - Confirm the workflow spec defines only `off` and `authoring-through-plan-review` as closed profile values and fails closed for unknown values.
  - Confirm activation requires `armed && gate-ready` and keeps user authorization separate from proposal-gate evidence.
  - Confirm durable authorization is recorded at `change.yaml`, or at `workflow-policy.yaml` only when change metadata rejects policy data.
  - Confirm missing, malformed, incomplete, or failed authorization persistence pauses before any profile-driven transition.
  - Confirm the profile cannot run `test-spec`, implementation, code-review, explain-change, verify, PR, release, deploy, merge, or review-fix loops.
  - Confirm the profile records architecture assessment and pauses on ambiguity.
  - Confirm review stages remain independent formal review stages and direct review requests remain isolated.
  - Confirm clean `plan-review` completes the profile and reports `test-spec` without invoking it.
  - Confirm profile policy metadata does not own current stage, next stage, review status, branch readiness, or PR readiness.
- Expected result:
  - Workflow-level guidance agrees with the autoprogression spec: durable authorization is mandatory, the profile is bounded, and all non-clean or ambiguous states pause.
- Failure proves:
  - Workflow-level guidance could permit unaudited activation, skip a required gate, or broaden the profile beyond the approved proposal.
- Automation location:
  - Manual contract review before implementation.

### T38. Test-spec-review gates formal implementation handoff

- Covers: `R7qa`-`R7qk`, `R12ao`, `E22`
- Level: manual, integration
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `specs/test-spec-review-gate.test.md`
  - `docs/workflows.md`
  - `AGENTS.md`
  - `scripts/review_artifact_validation.py`
  - `scripts/test-review-artifact-validator.py`
- Steps:
  - Confirm the standard workflow chain contains `plan-review -> test-spec -> test-spec-review -> implement`.
  - Confirm test specs keep settlement state `active` while review approval is recorded separately.
  - Confirm implementation eligibility requires a current approved `test-spec-review` with no open material findings.
  - Confirm the review-artifact validator accepts `test-spec-review` formal records and rejects unknown review status, immediate-next-stage, and implementation-handoff values before consistency checks.
  - Confirm substantive test-spec edits require re-review and upstream revision routing blocks implementation until artifacts are synchronized.
- Expected result:
  - The workflow contract, summary guidance, and validator baseline agree that implementation cannot begin merely because a test spec exists.
- Failure proves:
  - The independent proof-map adequacy gate can be bypassed, conflated with test-spec state, or accepted with invalid routing metadata.
- Automation location:
  - `python scripts/test-review-artifact-validator.py`
  - `python scripts/validate-review-artifacts.py --mode structure <change-pack>`

### T39. New workflow-managed change roots use dated change IDs

- Covers: `R25i`
- Level: static, manual
- Fixture/setup:
  - `specs/rigorloop-workflow.md`
  - `docs/workflows.md`
  - `skills/workflow/SKILL.md`
  - `skills/implement/SKILL.md`
  - `scripts/test-skill-validator.py`
- Steps:
  - Confirm the workflow spec defines `YYYY-MM-DD-slug` as the default new workflow-managed change ID convention.
  - Confirm `docs/workflows.md` explains that `<change-id>` means `YYYY-MM-DD-slug` for new workflow-managed changes and preserves explicitly legacy roots.
  - Confirm `skills/workflow/SKILL.md` points change-root creation to the workflow-guide convention instead of duplicating the detailed rule.
  - Confirm `skills/implement/SKILL.md` points change-root creation to the workflow-guide convention instead of inventing an undated slug.
  - Run `python scripts/test-skill-validator.py`.
- Expected result:
  - Skill-driven workflow usage has one visible creation-time rule for new change roots and cannot silently create an undated `docs/changes/<slug>/` root.
- Failure proves:
  - Agents may continue to infer plain slug roots from the placeholder syntax and create inconsistent change-local artifact paths.

### T40. Closed model and typed record validation

- Covers: R28-R28c, R28k, R28p-R28t
- Level: unit
- Command IDs: CMD-BFP-1
- Fixture/setup: Valid and invalid core, extension, marker, scope, and check-ID records.
- Steps: Parse every closed value; remove, duplicate, or replace each required field; inject one unknown value for every closed vocabulary.
- Expected result: Valid records normalize deterministically; unknown, missing, duplicate, incompatible, or orphan values fail before consistency evaluation.
- Failure proves: The executable projection can silently narrow or widen the approved model.
- Evidence artifact: `scripts/test-boundary-proof.py`
- Automation location: `scripts/test-boundary-proof.py`
- Required by milestone: M1

### T41. Examples and interactions remain subordinate to boundaries

- Covers: R28d-R28e, R28s-R28v
- Level: integration
- Command IDs: CMD-BFP-1
- Fixture/setup: Illustration, regression, discovery, non-normative, extension, and interaction records.
- Steps: Validate each role; omit required trace IDs; add invalid links; supply fewer than two interaction boundaries; verify a discovery gap pauses.
- Expected result: Every role follows its exact conditional fields and no example or extension satisfies a missing core entry.
- Failure proves: Examples can again become the implicit completeness model.
- Evidence artifact: boundary model fixtures
- Automation location: `scripts/test-boundary-proof.py`
- Required by milestone: M1 and M2

### T42. Stage gates reject example-complete but boundary-incomplete work

- Covers: R28f-R28j, R28w
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-3
- Fixture/setup: Feature spec and proof map with all examples covered but one partition, interaction, public path, or sibling omitted.
- Steps: Exercise spec-review, test-spec-review, implement, and code-review behavior fixtures against the omission.
- Expected result: The owning pre-code-review gate stops; implementation never upgrades missing authority; code-review remains independent.
- Failure proves: The workflow still defers exhaustive boundary audit to code review.
- Evidence artifact: workflow and skill behavior fixtures
- Automation location: `scripts/test-boundary-proof.py`; `scripts/test-skill-validator.py`
- Required by milestone: M2 and M3

### T43. Proof map traceability and canonical evidence

- Covers: R28f, R28h-R28k, R28q, R28w
- Level: integration
- Command IDs: CMD-BFP-1
- Fixture/setup: Current, missing, stale, substituted, partial, duplicated, and replayed proof inputs.
- Steps: Validate exact requirement, boundary, interaction, test, and manual-procedure references; replace canonical identities with caller assertions.
- Expected result: Only current owner-derived evidence passes; semantic adequacy stays reviewer-owned.
- Failure proves: Structural presence or caller assertion can masquerade as proof.
- Evidence artifact: boundary proof regression fixtures
- Automation location: `scripts/test-boundary-proof.py`
- Required by milestone: M1 through M3

### T44. Adoption, grandfathering, and synchronized version parity

- Covers: R28l-R28o, R28r
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-7
- Fixture/setup: Legacy approved artifacts, reviewed v1 opt-in, version mismatch, missing marker, and partial adoption.
- Steps: Validate prospective activation, grandfathering, synchronized opt-in, stale inputs, and the paused progressive-disclosure dependency.
- Expected result: Compatible legacy remains valid; partial or mismatched v1 fails; target selection cannot imply missing authority.
- Failure proves: Adoption can invalidate history or permit mixed proof.
- Evidence artifact: version and lifecycle fixtures
- Automation location: `scripts/test-boundary-proof.py`; lifecycle validator
- Required by milestone: M1 and M4

### T45. Frozen incident replay detects omissions at owning gates

- Covers: R28x
- Level: integration
- Command IDs: CMD-BFP-1
- Fixture/setup: BFP-FX-CANONICAL-001, BFP-FX-VOCAB-001, BFP-FX-TRANSITION-001, BFP-FX-IDENTITY-001, BFP-FX-ATOMICITY-001, BFP-FX-RECOVERY-001, BFP-FX-COMPOSITION-001, BFP-FX-SIBLING-001.
- Steps: Run each seeded omission through its named owning gate and inspect escape and sibling results.
- Expected result: Every fixture is detected no later than its expected gate; none escapes to code review or leaves a sibling bypass.
- Failure proves: The first release does not solve the observed late-boundary-audit problem.
- Evidence artifact: `tests/fixtures/boundary-proof/`
- Automation location: `scripts/test-boundary-proof.py`
- Required by milestone: M1 through M4

### T46. Capability report is computed and evidence-bound

- Covers: R28n, R28y
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-2
- Fixture/setup: Passing, failing, not-run, asserted, stale, unordered, missing-evidence, bad-count, and late-detection reports.
- Steps: Compute every row and overall result; attempt to hand-assert pass; change a cited input; serialize through the sole writer.
- Expected result: Only the exact evidence-bearing record aggregates to pass; not-run never passes; other writers cannot create a valid canonical report.
- Failure proves: The capability baseline can be asserted or detached from its evidence.
- Evidence artifact: `boundary-capability-baseline.md` and report fixtures
- Automation location: `scripts/test-boundary-proof.py`; `scripts/validate-boundary-proof.py`
- Required by milestone: M1 synthetic aggregate via CMD-BFP-1; M4 canonical report via CMD-BFP-2

### T47. Activation, rollback, and final resumption remain distinct

- Covers: R28o, R28z
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-5, CMD-BFP-6, CMD-BFP-7,
  CMD-BFP-16, CMD-BFP-17
- Fixture/setup: Passing report hash, mismatched hash, partial release unit, rollback notes, and incomplete review/verify closeout.
- Steps: Validate release-note activation identity, unit parity, rollback marker, and the separate R28o review-resolution and verification predicate.
- Expected result: Activation requires an actual tag and matching report bytes; partial units fail; report pass alone cannot resume progressive disclosure.
- Failure proves: Release or proposal-resumption claims can outrun reviewed evidence.
- Evidence artifact: release validation fixtures and lifecycle closeout
- Automation location: boundary, adapter, and lifecycle tests
- Required by milestone: M4 and verify

### T48. Behavior implementation manifest closes every executable input

- Covers: R28y
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-9, CMD-BFP-12
- Fixture/setup: Exact harness components; all resources mapped by the five
  participating skill packages; root-to-leaf applicable instructions; the
  exact five contract references `docs/workflows.md`,
  `specs/rigorloop-workflow.md`, `specs/rigorloop-workflow.test.md`,
  `specs/skill-contract.md`, and `specs/skill-contract.test.md`; and the exact
  nine invocation-profile fields `agent_runtime`, `runtime_version`,
  `runtime_executable_identity`, `model_id`, `orchestration_mode`,
  `instruction_profile`, `tool_profile`, `python_implementation`, and
  `python_version`; the exact `boundary-runtime-attestation-v3` record with
  all closed top-level fields, including exact launcher/package identities,
  the selected eleven-field runtime projection, effective-tool projection,
  file-change policy, fresh handler-conformance result, eight probe results,
  and six credential-isolation results; the exact
  `boundary-transport-policy-v1` record; the complete
  `lifecycle-stage-artifacts-v1` policy; and their recomputed identities.
- Steps: Derive the manifest from current Resource maps and instruction walks;
  for every manifest collection and every invocation-profile field,
  independently test valid, missing, additional, duplicate where applicable,
  unknown closed value, malformed format, stale identity, and changed value;
  omit, add, substitute, caller-select, or make nonpositive or unbounded each
  transport-policy deadline; mutate its schema version or recorded identity;
  and require generation and canonical validation to reconstruct the exact
  policy and its transitive immutable-run binding independently;
  independently mutate every runtime-attestation identity, result key, result
  value, profile value, schema version, thread-metadata field and logical-role
  projection; cross-substitute invocation and thread version, model,
  executable/launcher/package identity, and profile values; omit or substitute
  the selected runtime-projection ID or identity, effective-tool projection,
  shared file-change-policy, handler-conformance, or canary-policy identities;
  remove, add,
  reorder, or alter the lifecycle artifact policy, nested integrity policy,
  occurrence, artifact-set variant, content-state, path, role, or limit;
  test canonical JSON with Unicode, key-order, array-order, separator, and
  trailing-newline contrasts; test launcher-to-package-root discovery with
  missing, multiple, malformed, wrong-name, and wrong-version package files;
  inject symlink, socket, FIFO, device, and non-regular bundle entries; test
  nested/equal roots, longest-first path collisions, unknown absolute paths,
  remaining known-root bytes, every closed secret-key spelling, one near-miss
  key, and canary/authentication byte values in every identity projection;
  test `0.137.9`, `0.138.0`, `0.138.0-rc.1`, a later prerelease, build
  metadata, malformed versions, and exact launcher/package version mismatch;
  delete and substitute each of the five contract refs; reorder applicable
  instructions, duplicate one, omit root or nested instructions, add an
  inapplicable instruction, and introduce a symlinked instruction path;
  remove, replace, or mutate the Codex launcher and runtime package before and
  after schema generation, every sandbox probe, app-server negotiation, and
  the accepted lifecycle invocation;
  validate from a different validator environment without replacing the
  recorded invocation profile. Present the exact registered historical v1
  manifest and every moved, byte-mutated, additional, ambiguous, or
  caller-supplied v1 contrast; attempt to parse, normalize, inject, upgrade, or
  select v1 as current evidence. Present every v2-labeled attestation,
  preflight response, and implementation manifest and attempt structural
  parsing, field injection, selection, or silent upgrade to v3.
- Expected result: Only the exact current closure validates. Every missing,
  extra, duplicate, stale, escaping, non-regular, inapplicable, or substituted
  reference and every unknown, malformed, missing, additional, or changed
  profile field fails with its stable class diagnostic. Only fresh v3 evidence
  may satisfy current roles; the exact registered v1 record is opaque
  read-only history, every other v1 input fails closed, and every v2-labeled
  record is unsupported historical evidence. Instruction refs are
  root-to-leaf, path-deduplicated, applicable, and discovered without following
  symlinks. One stable launcher and runtime-package raw-byte/filesystem
  identity spans every execution boundary. Missing, stale, substituted,
  malformed, or tampered attestation invalidates the manifest and is never
  replaced by validation-time runtime evidence.
- Failure proves: The behavior result can depend on unbound skill resources,
  instructions, contracts, or runtime inputs.
- Evidence artifact: `evidence/behavior-implementation-manifest.json`
- Automation location: `scripts/test-boundary-proof.py`;
  `scripts/boundary_proof_behavior.py`
- Required by milestone: M2

### T49. Standalone harness import and runtime boundary is fail closed

- Covers: R28y
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-8, CMD-BFP-9, CMD-BFP-20,
  CMD-BFP-21
- Fixture/setup: The sole allowed repository import; one fixture for each
  forbidden relative, wildcard, third-party, repository-local, dynamic import,
  evaluator, workflow-engine, lifecycle-validator, and test-driver edge;
  unavailable and unsafe runtime profiles; exact generated app-server schemas,
  feature pages, effective configuration, managed requirements, app/plugin/MCP
  inventories, complete skill inventory with exactly five enabled manifested
  lifecycle packages and only disabled runtime-bundled system-skill rows,
  thread metadata, protocol item streams, and the exact manifest-bound
  `boundary-transport-policy-v1` record. Generated TOML fixtures include
  nested tables, zero-based arrays, and quoted keys whose preserved key bytes
  contain dots and spaces; each fixture has an independently computed complete
  flattened leaf-key set and matching runtime-origin rows.
- Steps: Inspect the AST closure; run the parent-observed preflight; attempt
  caller instructions, extra tools, connectors, subagents, network,
  unmanifested reads, and child self-attestation. Negotiate
  `experimentalApi: true`; add, remove, rename, reorder, byte-mutate, stale,
  or substitute files in the path-sorted generated schema bundle; omit
  `experimentalApi`, set it false, and reject it server-side; test every
  required method and non-null `thread/start` field as missing, null,
  additional, renamed, or incompatible. Paginate `experimentalFeature/list`
  across multiple pages and test ignored continuation, premature termination,
  repeated or cyclic cursors, duplicate cross-page rows, the required final
  null cursor, missing rows, reordered rows, unknown rows, and newly enabled
  rows; require exact closed results from `config/read`,
  `configRequirements/read`, `app/list`, `plugin/list`,
  `mcpServerStatus/list`, and `skills/list`.
  Reorder JSON object keys in one generated schema file and require the same
  schema identity. Reorder an array or add or remove an object member and
  require a different identity. Inject top-level or nested duplicate object
  names or malformed JSON and require closed `schema-bundle-invalid` failure.
  Regenerate equivalent configuration under different temporary roots and
  require the same normalized capability identity; make one runtime-reported
  config-origin version differ from its siblings before normalization and require
  `config-equivalence-mismatch`. Also test empty, partial, omitted, additional,
  and unknown-root origin keys; wrong source type; wrong user-config path;
  non-null profile; malformed or empty version; additional/missing origin
  fields; and changed effective-config values. Parse each structured generated
  TOML fixture independently and flatten every leaf using dot separators,
  zero-based array indices, and preserved quoted-key bytes. Require exact
  equality with the complete runtime-returned origin-key set. Contrast a fixed
  current-config allowlist and mutations that collapse nesting, use one-based
  indices, split quoted keys on dots or spaces, omit a derived leaf, or add a
  non-derived origin row; each must fail `config-equivalence-mismatch`.
  Invoke `skills/list` exactly once with the isolated-workspace `cwds` singleton
  and `forceReload: true`. Require one exact-CWD row, empty errors, the five
  enabled manifested `scope: user` rows, and the six generated-config-bound
  disabled `scope: system` runtime rows, including `review-agent`. For the
  Codex `0.145.0` projection, require `thread/start` to report the empty
  runtime-root list while the accepted `thread/start` and `turn/start`
  requests both contain exactly the isolated workspace root; reject any
  different version/schema shape. Inject an enabled system skill,
  disabled manifested skill, each valid-but-wrong `repo`, `system`, `admin`,
  or `user` scope substitution, extra user/project skill, escaping system
  path, wrong CWD, non-empty error, `forceReload: false`, stale response,
  duplicate name, duplicate raw path, normalized-path collision,
  generated-config roster mismatch, and each omitted manifested or system row.
  Require the exact Codex 0.145.0 canonical schema identity
  `sha256:18d79891673d9d43a8e7a49864fef49a04305bd13571a8aef45824209f1bfae8`,
  launcher identity
  `sha256:134063e133f0b4244fa3b251acf973d4fe4b4aeeacbdc135211bf480f59f1477`,
  runtime-package identity
  `sha256:a66a2dee773de39b690a08048971ec18d04f97d8a8d5e9a205f51a9f0d4cdbfa`,
  protocol-classification identity
  `sha256:35f1203d9c6abc62ef3f1aca94e2f3165e0213697d554ab11d0477d9cd7e4bf8`,
  feature-classification identity
  `sha256:6f833f4c43196e43f67fea215de09743e5a5e3a80bed53973b42740041369268`,
  projection ID `codex-0.145.0-readonly-boundary-v1`, projection identity
  `sha256:ab6416627d461e3f11a2bc0d16d465ae8601478a8d085b64e86a6945931a4624`,
  and exactly 96 unique feature rows partitioned into three permitted command
  features, four permitted non-tool behaviors, and 89 required-disabled
  tool-bearing features. Assert each approved literal
  directly, then add, remove, duplicate, overlap, or mutate projection fields,
  selection keys, identities, schema files, object members, methods,
  classifications, feature rows, launcher bytes, and package bytes as contrast
  cases. Swap one member between every pair of feature collections while
  preserving 3/4/89 counts, disjointness, exhaustiveness, and a recomputed
  projection identity; require every category-disagreeing row to fail before
  thread start. Equal version/schema/protocol/feature declarations with
  changed implementation bytes must fail. Capture the exact
  `thread/start` and `turn/start` requests and independently remove, add,
  substitute, or reorder their workspace roots. Exercise all four
  `status_is_disabled` × `environment_identity_is_null` combinations for
  `remoteControl/status/changed`: accept only `true`/`true` as non-side-effect
  traffic, reject the other three with
  `protocol-conditional-policy-violation`, and prove retained evidence
  contains only the booleans, closed rule ID, and event kind rather than raw
  status or environment identity. Run the parent runtime with each closed
  proxy-name spelling and an
  unrelated or secret-bearing environment name; prove spawned commands still
  receive only their exact closed environment.
  Independently map every feature row exactly once as permitted built-in tool,
  permitted non-tool runtime behavior, or must-be-disabled tool-bearing
  behavior, then map every generated protocol item variant exactly once as
  permitted side effect, non-side-effect protocol traffic, or prohibited
  capability event. For each map, test missing, duplicate, unknown, and
  unclassified entries. Keep schema-supported prohibited variants disabled
  pre-turn and inject each prohibited event during the accepted turn.
  Start with `dynamicTools: []` and `environments: []`; expose command tools
  only as `shell_tool`, `unified_exec`, or `shell_snapshot` under
  `boundary-proof-stage-readonly-v1`. Through the same
  `codex sandbox --include-managed-config` profile, require manifested reads
  and deny direct create, overwrite, remove, and chmod. Start a detached
  descendant, require the same four denials through the parent-owned pipe,
  and require bounded exit/reap. Install the production file-change dispatcher
  and execute every ordered
  `stage-file-change-handler-conformance-v1` case against the production
  dispatch and response-validation functions. Validate the complete policy and
  result through `boundary_proof_model` before selecting a capability branch.
  For missing, failed, malformed, stale, reordered, incomplete, or
  identity-inconsistent conformance, require bounded failure evidence and zero
  invocation counters for both branches, canary, governed lifecycle turns, and
  successful-attestation assembly.
  Under a controlled `exposed-live-probe-required` projection, run the exact
  app-server file-change probe: require one projected request, return only
  `decision: decline`, correlate the generic item carriers, require terminal
  `FileChangeThreadItem.status: declined`, unchanged workspace, no lifecycle
  output, and complete stop/reap. Reject shell substitution, missing or
  ambiguous requests, `accept`, `acceptForSession`, generic failed/completed
  status, mutation, additional side effects, and incomplete cleanup.
  Under the exact `not-exposed-projection` row, prove selected runtime bytes,
  all 89 required-disabled tool-bearing features disabled, only the three
  permitted command features enabled within the effective-tool projection,
  the four projected non-tool behaviors allowed to remain enabled, exact
  policy and conformance identities, and no observed file-change event; do not
  issue the unavailable-operation prompt. Inject any
  file-change event and require projection-drift failure without silently
  switching branches. Inject a
  transient canary and test exact child environment names plus absence from
  environment values, argv, stdin, private paths, and readable process
  metadata.
  Require pass output to contain the exact current
  `runtime-preflight-attestation.json` reference and require the file's
  identity and closed record to match. For each of the exact six preflight
  fields, test missing, additional, renamed, null, wrong type, malformed
  `schema_version`, and incompatible result/diagnostic/phase/reference
  combinations. Require `workspace_failure` to be null except for
  `workspace-baseline-invalid`; exercise every closed reason, precedence,
  identity field, and the intrinsic 271-byte maximum. Test missing, stale,
  substituted, malformed, and non-atomic
  evidence. Invoke without `--change-id`, with
  malformed/mismatched/absent/symlinked change roots, and with a valid exact
  change. Crash before temp-file fsync, before replacement, after replacement,
  and before directory fsync. Exercise malformed, identity-mismatched, and
  well-formed leftover sibling temporary files; prove cleanup only for the
  first two, non-authority for all temporary bytes, preservation of prior
  installed evidence on failure, stale prior evidence never satisfying the
  current attempt, and restart after replacement repeating replacement and
  directory fsync before pass. Test pass emission before durability. Require
  every failure result to carry a null attestation reference. Validate the
  transport policy as an exact manifest member: reject a missing, additional,
  substituted, caller-selected, zero, negative, or unbounded turn or
  termination-wait deadline and reject any policy-identity mismatch. Sample
  the parent monotonic clock immediately below, exactly at, and above each
  deadline. Require timeout only at or above the turn deadline; require
  confirmed stop/reap only at or below the termination-wait deadline and
  liveness uncertainty when that bounded wait reaches its deadline without
  confirmation. Bind timeout rows to their exact runtime thread and
  termination/liveness records to their exact logical `runtime_process_id`;
  reject thread, process, deadline, elapsed-time, and policy substitutions.
  Exercise both closed runtime-identity kinds at every closed checkpoint and
  require the exact checkpoint-to-phase matrix. Reject missing, duplicate,
  additional, unknown, and cross-phase matrix rows.
  Reject cross-kind substitutions, unknown kinds or checkpoints, expected
  identity not equal to the attested resource, observation of a different
  resource, and expected/observed equality.
  Assert the closed diagnostic mapping
  `runtime-unavailable`, `runtime-unreadable`, `runtime-version-invalid`,
  `runtime-version-unsupported`, `runtime-projection-unsupported`,
  `runtime-identity-unstable`, `schema-bundle-invalid`,
  `experimental-api-unavailable`, `protocol-shape-incompatible`,
  `protocol-conditional-policy-violation`,
  `thread-metadata-mismatch`, `feature-pagination-invalid`,
  `capability-inventory-mismatch`, `skill-inventory-mismatch`,
  `feature-classification-invalid`, `protocol-item-classification-invalid`,
  `permission-profile-mismatch`, `config-equivalence-mismatch`,
  `sandbox-probe-failed`, `file-change-control-mismatch`,
  `credential-isolation-failed`,
  `workspace-baseline-invalid`, `stage-envelope-canary-failed`, and
  `unexpected-prohibited-event`; separately require the
  behavior-generation-only `boundary-oracle-mismatch` diagnostic for a
  structurally valid envelope whose deterministic boundary invariant
  projection fails, and prove `check-environment` never emits it; mutate
  each failure into every sibling diagnostic and one unknown value; mutate
  every result/diagnostic/phase combination across `pre-thread-start`,
  `pre-turn-start`, and `in-turn`, and exercise
  `runtime-identity-unstable` at one checkpoint in each phase. Enumerate every
  closed file-change cause-to-phase row, then reject missing, duplicate,
  unknown, and cross-phase causes. Combine file-change, runtime, sandbox,
  credential, integrity, and canary failures to prove the closed diagnostic
  precedence. Require successful v3 attestations to contain only their exact
  closed fields and no diagnostic; require every validated diagnostic path to
  produce only bounded failure evidence and no attestation.
- Expected result: The model module is standard-library only; the harness uses
  only standard library plus `boundary_proof_model`; the parent establishes
  one stable launcher/package/schema identity, exact effective profile and
  capability closure, read-only sandbox enforcement, a pure-model-validated
  common deny-handler conformance gate, capability-state-specific file-change
  proof, parent-only canary materialization, and private authentication
  channels. Exact runtime version plus launcher, package, schema, protocol,
  and feature-classification identities select one immutable projection;
  version or declared capability metadata alone is insufficient. Config-origin
  keys equal the independently derived
  complete flattened TOML leaf set for nested tables, zero-based arrays, and
  quoted keys; no fixed allowlist or lossy key normalization can satisfy the
  gate. Missing, duplicate, unknown, unclassified,
  enabled-prohibited, observed-prohibited, mismatched-profile, incomplete-page,
  unstable-identity, or canary-visible cases stop with
  `environment-unavailable` and the exact stable diagnostic at its mapped
  phase. Pre-thread failures precede `thread/start`; pre-turn failures precede
  `turn/start`; an unexpected prohibited event discards the active turn before
  manifest or output acceptance. Unknown or
  mismatched diagnostics fail closed. Unmanifested behavior inputs stop with
  `unmanifested-input`. A pass is accepted only when its attestation reference
  resolves to the exact current bounded preflight record after file and parent
  directory durability. Failed or interrupted attempts never promote prior or
  temporary evidence.
- Failure proves: A child can broaden or attest its own trust boundary.
- Evidence artifact: `validation-m2.md` and controlled behavior fixtures
- Automation location: `scripts/test-boundary-proof.py`;
  `scripts/boundary_proof_behavior.py`
- Required by milestone: M2 preflight gate

### T50. Generation binds immutable runs to current inputs

- Covers: R28y
- Level: e2e
- Command IDs: CMD-BFP-10, CMD-BFP-11, CMD-BFP-12
- Fixture/setup: Exact baseline record with only `schema_version`, `change_id`,
  and `preservation_baseline_commit`; exact input set with only
  `schema_version`, `scenario_ref`, `baseline_commit`, `skill_resource_refs`,
  `oracle_refs`, and `implementation_manifest_ref`; unchanged and independently
  changed harness, skill-resource, instruction, contract, runtime, scenario,
  oracle, and implementation-manifest identities; current, missing, stale,
  substituted, malformed, and tampered bounded v3 runtime-attestation records.
- Steps: Freeze the baseline before skill mutation; generate once; validate
  unchanged bytes; attempt caller-selected baseline commits and baseline
  rewrites; for each baseline and input-set field test missing, additional,
  malformed, reordered where order is normative, stale, substituted, and
  caller-selected variants; omit, add, reorder, or substitute each scenario,
  skill-resource, oracle, and implementation-manifest member; remove, replace,
  or mutate every attestation identity, classification, probe result, and
  credential-isolation result; attempt to replace recorded attestation with
  validation-time runtime evidence. In a controlled sequence, pass preflight,
  change one bound member of the attested eleven-row runtime inventory, generate
  against the current five-package resource set, and compare the nested
  generation attestation with the preflight artifact; copy or substitute the
  preflight attestation into the generation manifest; present the exact
  registered v1 manifest and every unknown, moved, altered, additional, or
  caller-supplied v1 contrast; attempt to select, structurally validate, or
  silently upgrade v1; independently
  change `expected_branch` and `corrected_role`; rerun validation without
  invoking lifecycle skills.
- Expected result: Unchanged inputs validate; any behavior-affecting identity
  change makes the current run stale and requires explicit new generation.
  The baseline accepts only `boundary-proof-baseline-v1`, the exact change ID,
  and the harness-derived immutable pre-M2 commit. The input set accepts only
  `simple-change-input-v1`, invocation-owned pre-run HEAD, exact current
  scenario, complete path-sorted five-package resources and oracle set, and
  the canonical implementation-manifest reference. Changing
  `expected_branch` or `corrected_role` changes only final comparison, never
  invocation, events, structural results, observations, or diagnostics.
  Validation never changes the invocation profile, runtime attestation,
  baseline, or current pointer. Any missing, stale, substituted, malformed, or
  tampered attestation invalidates the manifest reference, input-set identity,
  immutable run, current pointer, and `simple-change-behavior` report selector
  together. Generation derives a fresh nested attestation for the then-current
  exact eleven-row runtime inventory: five enabled manifested lifecycle rows plus
  six generated-config-bound disabled system rows. The complete path-sorted
  five-package resource set remains a distinct input. Copying preflight
  evidence fails before manifest or run acceptance. Current generation emits
  only `boundary-runtime-attestation-v3` nested in
  `boundary-behavior-implementation-v3`. The exact registered v1 record is
  recognized only as opaque historical evidence, and no v1 record can satisfy
  the manifest, input-set, immutable-run, pointer, validation, report,
  capability, or activation chain. Every v2-labeled record is unsupported
  historical evidence and cannot be parsed, selected, injected, or silently
  upgraded.
- Failure proves: Recorded behavior can be reused across materially different
  implementations or environments.
- Evidence artifact: immutable run, current pointer, baseline, and manifest
- Automation location: `scripts/test-boundary-proof.py`;
  `scripts/boundary_proof_behavior.py`
- Required by milestone: M2

### T51. Publication recovers every prepared-transition crash point

- Covers: R28y
- Level: integration
- Command IDs: CMD-BFP-9, CMD-BFP-11, CMD-BFP-12
- Fixture/setup: Crash injection after successful working-run validation but
  before staging rename, after successful staged-run/current-input validation
  but before receipt creation, after receipt fsync, before and after
  immutable-run installation, after installed-run validation, pointer
  replacement, parent-directory fsync, and receipt cleanup; malformed or
  inconsistent working-run events, bundles, snapshots, inventories, and
  metrics; malformed, incomplete, identity-mismatched, and stale-input
  staged-run fixtures;
  exact global discovery fixtures and `clean`, `lease-acquired`, `generating`,
  `staged-unreceipted`, `prepared-staged`, `prepared-installed`,
  `prepared-pointer-temporary`, `prepared-pointed`, `published-owned`,
  `published`, `conflict`, and `corrupt` candidate fixtures.
- Steps: Build and fsync the working run, then validate all of its events,
  bundles, snapshots, inventories, and metrics before any staging rename. For
  each malformed or inconsistent working-run object, assert failure before
  staging rename. After successful working-run validation, rename and fsync it
  as the non-authoritative staged run, then validate the complete staged run
  and current input identities before publication begins. For each malformed,
  incomplete, identity-mismatched, and stale-input staged run, assert failure
  before receipt creation. Interrupt after successful working-run validation
  but before staging rename, after successful staged validation but before
  receipt creation, after durable receipt but before immutable installation,
  after installation/fsync, after installed-run validation, after pointer
  replacement, after parent-directory fsync, and after receipt cleanup. Resume
  against the original inputs; inspect
  deterministic staging, installed run, prepared receipt, current pointer, and
  directory durability; distinguish the historical staged-manifest snapshot
  from the prospective immutable target descriptor; test a null prior pointer
  for first publication; attempt a second in-flight publication. Exercise the
  exact predicate and action of every durable state, including simultaneous
  staging and target, staging with a target pointer, temporary pointer without
  receipt, unpointed target without receipt, missing candidate bytes, malformed
  object, symlink, identity mismatch, other current pointer, and changed input.
  Before run allocation, enumerate global receipt, lease, working, staging,
  temporary-pointer, active/completed recovery, unrelated-run, multi-run, and
  unknown-transient combinations; prove only the receipt/lease/recovery-owned
  run can become a candidate and no lifecycle stage runs first. Rename staging
  to immutable storage and prove the receipt's historical staged snapshot
  remains valid against the installed target while no nonexistent staging path
  is treated as current evidence. For working, staging, and lease-only orphans,
  prove exclusive publisher-lock acquisition, publisher-instance and lease
  binding, separately durable owner authority, exact recovery-record schema,
  minimum-valid versus corrupt working roots, lease-bound rather than current
  input validation, discard-only behavior, and no adoption. Prove the explicit
  same-live-publisher fact permits only the uninterrupted lease creator to
  advance lease-acquired, generating, or staged-unreceipted state. Interrupt
  before and after temporary recovery-basis fsync, atomic no-clobber basis
  installation, temporary cleanup, initial state write, atomic quarantine
  rename, namespace-parent fsync, detached-state replacement, lease deletion,
  lease-parent fsync, and completion replacement; exercise every recovery row
  and invalid tuple. Inject a lone valid temporary basis and truncated or
  malformed writes at every byte-boundary class, both with and without a
  canonical basis; test matching and conflicting temporary/canonical bases and
  crash during temporary cleanup and its parent fsync. Crash immediately
  before and after quarantine rename; inject partial or identity-changed
  quarantine and completed recovery with unexpected quarantine state. Attempt
  quarantine cleanup and prove the first version rejects it without mutation;
  prove preserved quarantine is excluded from artifact-count inventories and
  cannot satisfy canonical behavior evidence. Mutate every
  immutable recovery-basis field and every non-state state-record field across
  resume; test lease-only fsync against the simple-change root. For normal
  cleanup, prove pointer-parent, receipt-parent, and lease-parent fsync before
  success. Create, persist, and reuse `publisher.lock` across runs and prove
  its separately validated control path never changes artifact counts or
  canonical behavior evidence. Prove global discovery classifies one
  well-named lease/basis-bound malformed temp as recoverable and reaches the
  cleanup route, while malformed names, multiple temps, ambiguous leases,
  cross-run temps, and canonical corruption stop before mutation. Interrupt
  unlink and parent fsync independently and prove idempotent resume. Add one
  valid completed recovery history for run A beside a full publication
  candidate for run B and require B to remain the sole active candidate; repeat
  with multiple valid completed histories. Add completed history beside one
  active recovery and require only the active recovery run to own candidacy.
  Mutate each completed-history basis, state, completion, and quarantine
  invariant and keep every nonterminal or malformed object in the active set,
  where it conflicts or fails closed rather than being ignored as history.
  Exercise phase-aware rollback with no receipt, each reconcilable prepared
  state, and an irreconcilable receipt. Require the publisher lock before
  mutation; restore a previously validated pointer or remove it when no
  validated prior run exists; restore the exact registered opaque-v1 manifest
  only for the historical baseline or leave no current manifest; revert the
  model, harness, validator, fixtures, shared template, and five
  package/resource surfaces as one compatibility unit; remove v3 preflight
  evidence whose implementation was reverted; retain installed v3 runs only
  as non-current history; and inject dangling v3 manifest, attestation,
  pointer, selector, and report references independently.
- Expected result: The only publication order is build/fsync working bytes;
  validate working-run events, bundles, snapshots, inventories, and metrics;
  rename/fsync staging; validate the complete staged run and current input
  identities; exclusively write/fsync the prepared receipt; install/fsync and
  validate the immutable run; replace/fsync the pointer; reconcile and
  remove/fsync the receipt. Invalid working-run contents leave no staging
  rename, prepared receipt, immutable installation, pointer mutation, or
  lifecycle reinvocation. Invalid or stale staging leaves no prepared receipt,
  immutable installation, pointer mutation, or lifecycle reinvocation. Resume
  reconciles valid evidence without reinvoking skills, never installs or
  points at a partial run, never installs without a durable exclusive receipt,
  never loses the prior immutable pointer, and fails closed before generation
  on every unrelated, orphan, active-recovery, conflict, corrupt, unknown, or
  changed-input state. Every non-corrupt durable tuple matches exactly one
  named publication or recovery route; recovery resumes idempotently after
  every interruption. Rollback either leaves one completely validated prior
  authority state or no current authority, never a mixed compatibility unit,
  unresolved receipt, or current reference to retained v3 history.
- Failure proves: A crash can duplicate nondeterministic work or publish an
  incomplete/stale run.
- Evidence artifact: controlled publication-recovery fixtures
- Automation location: `scripts/test-boundary-proof.py`;
  `scripts/boundary_proof_behavior.py`
- Required by milestone: M2

### T52. Fresh upstream behavior is generated once and validated separately

- Covers: R28y
- Level: e2e
- Command IDs: CMD-BFP-1, CMD-BFP-8, CMD-BFP-10, CMD-BFP-11, CMD-BFP-12
- Fixture/setup: The exact `workflow`, `spec`, `spec-review`, `test-spec`, and
  `test-spec-review` packages and the simple-change scenario corpus; this is a
  four-stage lifecycle path using five participating skills. Controlled
  transport-failure fixtures are owned by `scripts/test-boundary-proof.py`
  below `tests/fixtures/boundary-proof/transport/`. Each record contains
  exactly `fixture_id`, `event_key`, `transport_attempts`,
  `expected_terminal_decision`, `expected_diagnostic_id`,
  `expected_diagnostic_ids`, and `canonical_evidence_eligible`;
  `canonical_evidence_eligible` is `false`.
- Steps: Pass the v3 capability-projected read-only preflight; freeze baseline;
  invoke the public
  `workflow` once to route the four-stage upstream path; require each
  stage-owning skill to return one complete parent-policy-bound artifact
  envelope; require an unchanged workspace observation before the parent
  materializes the exact returned UTF-8 bytes and snapshots the complete
  artifact set before the next stage; reject harness-authored, repaired, or
  completed normative content. Bind the exact scenario request into both
  formal review invocations. Normalize each fixture candidate and produced
  artifact independently; compare only the closed version, scope, requirement,
  core-dimension, extension, and governing-requirement invariant projection;
  then vary stable IDs, non-applicability prose, applicable core rows,
  boundary decomposition, examples, selected interactions, automation levels,
  proof grouping, and test-case IDs while preserving R28s-R28w validity.
  Require those alternative decompositions to proceed to independent review,
  not fail candidate comparison. Independently remove, add, duplicate, or
  substitute each invariant projection member and require
  `boundary-oracle-mismatch`; require an unknown diagnostic to fail closed and
  prove the mismatch is never emitted by preflight. Inject stage timeout
  with absent, complete, partial, extra, and contradictory output plus
  uncertain liveness and every closed non-output diagnostic. Enumerate every
  admissible transport tuple and representative vocabulary-valid unlisted
  tuples. Combine each partial, extra, and contradictory output with every
  protocol, prohibited-event, and runtime-identity diagnostic plus timeout
  where applicable. Assert the closed precedence derives one primary
  diagnostic and retains the complete ordered unique diagnostic list and
  bounded evidence for every detected condition without changing output state.
  Assert lifecycle correction attempt and transport attempt remain distinct;
  a prospective event key remains valid when no lifecycle event is created;
  every row has the exact R28y fields; confirmed-stopped rows bind the exact
  termination receipt, logical runtime process, and manifest-bound transport
  policy; liveness-uncertain rows bind the same logical child and policy and
  are uninspected; and attempt 2
  exists if and only if attempt 1 decides retry, uses a fresh runtime identity,
  and terminates without retry. Reject missing, extra, duplicate, unknown,
  suppressed, reordered, out-of-order, post-terminal, multiple-terminal, and
  inconsistent rows. Prove complete output references, empty
  absent/uninspected references, bounded noncanonical
  partial/extra/contradictory references, diagnostic-evidence parity, and the
  exact test-owned failure-fixture schema. Require missing, extra, stale,
  contradictory, or publication-eligible fixture fields to fail closed. For
  every diagnostic role, remove
  its inline evidence, add an unrelated role, mutate each field, substitute a
  stale observation, and attempt direct or indirect self-reference to the row
  or manifest. Test elapsed time immediately below, equal to, and above the
  manifest-bound turn and termination-wait deadlines; reject missing, zero,
  negative, unbounded, caller-selected, or substituted policy values and
  identities. Test matching and mismatched logical thread/process identities.
  For both runtime-identity kinds, test every closed checkpoint, cross-kind and
  cross-resource substitution, an attestation mismatch, an equal
  expected/observed pair, and unknown kinds or checkpoints. Exercise all four
  closed boolean combinations for the
  `remote-control-disabled-null-environment-v1` rule; require only
  `true`/`true` to pass and each other combination to emit
  `protocol-conditional-policy-violation`, cross it with timeout and liveness
  diagnostics, and reject raw status or environment identity in retained
  evidence. Test equal and unequal runtime identities; schema-accepted and
  schema-rejected shape projections; known prohibited, known permitted, and
  unknown protocol event kinds, including exact
  `protocol-item-classification-invalid` evidence. Mutate every value-free
  event-shape projection path, type, ordering, and identity independently and
  prove raw values and logs remain absent. Cross liveness uncertainty with
  every prior non-output diagnostic and reject every output diagnostic while
  output is uninspected. Exercise empty required lists,
  absent, complete, nonempty proper subset, extra, identity-conflicting,
  identical duplicate-path, mutually-exclusive, and mixed missing-plus-extra
  output lists. Require raw observations to contain only normalized path and
  identity; reject role-bearing or malformed descriptors. Test exact
  path/identity matching, unmatched paths, exact-identity mismatch, and role
  projection solely from the required path map. Combine overlapping output
  conditions and prove the closed
  contradictory-before-extra-before-partial precedence without deduplication.
  For every accepted or reconciled complete envelope, require the exact
  artifact-policy identity, workspace-integrity observation, parent-only
  materialization observation, and structural content-validation observation.
  Reject materialization before a complete unchanged scan, materialization for
  any non-accepting decision, path re-resolution outside the retained root
  descriptor, semantic normalization, missing or additional leaf files,
  reread mismatch, and content-state disagreement.
  Run validation repeatedly.
- Expected result: One fresh immutable run contains current output snapshots,
  terminal branches, review-event evidence unions, and computed simple-change
  observations. Each artifact's semantic bytes originate in its stage skill,
  while physical writes originate only in the parent materializer after an
  unchanged observation. The scenario request and independent approving
  reviews own semantic fidelity; the deterministic oracle owns only the closed
  invariant projection and R28s-R28w structural validity. A structurally valid
  alternative decomposition is accepted for review, while an invariant
  mismatch stops with `boundary-oracle-mismatch`. Complete output reconciles
  without reinvocation;
  absent output permits at most one transient retry only after confirmed stop,
  zero candidates, unchanged workspace, and no independent non-output
  diagnostic; partial, mutation, inspection, protocol, security, or other
  non-retryable evidence stops; uncertain liveness pauses without inspection;
  failed/paused invocations never publish; every controlled transport-failure
  fixture remains ineligible for canonical evidence; and validation performs
  no lifecycle reinvocation.
- Failure proves: M2 evidence is asserted, incomplete, or nondeterministically
  regenerated during validation.
- Evidence artifact: current M2 immutable run and `validation-m2.md`
- Automation location: behavior harness and boundary tests
- Required by milestone: M2

### T53. Preservation consumes the frozen baseline without upstream reinvocation

- Covers: R28y
- Level: integration
- Command IDs: CMD-BFP-13, CMD-BFP-14
- Fixture/setup: Frozen pre-M2 baseline, current M2 run, all eight skills, five
  preservation categories, and missing/extra/duplicate/stale/cross-skill pair
  variants.
- Steps: Materialize historical bytes into immutable before snapshots; capture
  current after artifacts; generate exactly 40 pairs; validate origin,
  identities, dependencies, and category results while monitoring invocation
  count.
- Expected result: Exactly one `<skill>:<category>` result exists for every
  pair; historical bytes are current materialized evidence; upstream
  lifecycle invocation count stays zero.
- Failure proves: Preservation can cite Git history as current evidence, omit a
  skill/category, or rerun upstream work.
- Evidence artifact: exact preservation manifest and before/after roots
- Automation location: behavior harness and boundary tests
- Required by milestone: M3

### T54. Four-surface parity and release proof use exact durable evidence

- Covers: R28y, R28z
- Level: integration
- Command IDs: CMD-BFP-2, CMD-BFP-4, CMD-BFP-5, CMD-BFP-6, CMD-BFP-15,
  CMD-BFP-16, CMD-BFP-17
- Fixture/setup: `dist/adapters/manifest.yaml`; canonical resource manifest;
  canonical/generated/packed/installed trees; four durable parity paths; valid
  activation, invalid partial activation, and valid rollback release notes.
- Steps: Build and validate adapters in a fresh root; copy the four validated
  maps to their exact change-evidence paths; generate then validate the report;
  run release regression and current v0.3.6 validation.
- Expected result: All four maps cover identical path/byte identities; report
  generation is the sole production path; release checks reject partial or
  mismatched activation without publishing anything.
- Failure proves: Distribution or release claims can rely on temporary,
  partial, stale, or hand-authored parity/report evidence.
- Evidence artifact: `evidence/adapter-parity/{canonical,generated,packed,installed}.json`,
  capability report, and release validation output
- Automation location: boundary, selector, adapter, and release tests
- Required by milestone: M4

### T55. Current v3 evidence, unsupported v2, and opaque v1 history cannot be confused

- Covers: R28y
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-8, CMD-BFP-11, CMD-BFP-12
- Fixture/setup: The exact registered v1 manifest path, regular-file kind, and
  raw-byte identity; current v3 preflight, attestation, and implementation
  manifests; every v2-labeled record kind; moved, altered, additional,
  ambiguous, caller-supplied, structurally parsed, and field-injected v1
  variants.
- Steps: Resolve the exact registry row by path, entry kind, and raw identity;
  mutate each selector independently; attempt to parse, normalize, upgrade,
  copy, inject, or bind v1 into every current authority role; attempt the same
  operations for every v2-labeled record without a compatibility-registry row;
  generate and validate fresh v3 evidence.
- Expected result: Exact registry equality returns only
  `registered-opaque-history`. Every other v1 input returns
  `unsupported-historical-evidence`. Every v2-labeled input is unsupported
  historical evidence. Current preflight, generation, manifest, immutable run,
  pointer, validation, report, capability, and activation roles accept only
  v3 and never perform a silent upgrade.
- Failure proves: Historical evidence can select a parser or silently regain
  current authority.
- Evidence artifact: historical-registry fixtures and current v3 manifest
- Automation location: `scripts/test-boundary-proof.py`;
  `scripts/boundary_proof_behavior.py`
- Required by milestone: M2

### T56. Common conformance and capability-specific file-change proof precede the canary

- Covers: R28y
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-8, CMD-BFP-9
- Fixture/setup: Exact `boundary-proof-stage-readonly-v1` profile, direct and
  detached-descendant mutation probes, exact
  `stage-file-change-authorization-policy-v1`, projected generic item
  carriers, exact handler-conformance policy/results, both closed capability
  states, and controlled request-handler variants.
- Steps: Prove manifested reads; attempt create, overwrite, remove, and chmod
  directly and from a detached descendant; require bounded descendant
  stop/reap. In preflight and generation, run all eleven conformance cases
  against the production dispatcher and response validator, validate the exact
  ordered result through the pure model, then select the capability branch:
  `matching-request-declined`, `missing-handler-rejected`,
  `wrong-policy-identity-rejected`, `thread-mismatch-rejected`,
  `turn-mismatch-rejected`, `item-mismatch-rejected`,
  `change-mismatch-rejected`, `accept-rejected`,
  `accept-for-session-rejected`, `widened-response-rejected`, and
  `malformed-request-rejected`.
  Mutate conformance as missing, failed, malformed, stale, reordered,
  incomplete, and identity-inconsistent and prove neither branch, canary,
  governed turn, nor successful attestation runs.
  For `exposed-live-probe-required`, correlate exactly one matching request,
  `decision: decline`, and terminal `declined` item. Exercise missing,
  ambiguous, substituted, accepted, session-accepted, failed, completed,
  shell-substituted, additional-side-effect, mutated, and unclean-stop
  contrasts.
  For `not-exposed-projection`, require the exact eleven-field projection and
  implementation identities, all 89 required-disabled tool-bearing features
  disabled, only the three permitted command features enabled within the
  effective-tool projection, the four projected non-tool behaviors allowed to
  remain enabled, and no file-change event during canary or lifecycle turns
  without issuing the unavailable-operation prompt. Inject a file-change event
  and require drift failure.
  Apply the same policy identity to probe when applicable, canary, lifecycle,
  and retry contexts; prove reconciliation starts no child.
- Expected result: All command mutations fail, the descendant exits and is
  reaped, common handler conformance validates before branch selection, and
  the workspace remains unchanged. The exposed branch proves every request is
  declined; the non-exposed branch proves exact reviewed implementation and
  effective-tool state without relying on event absence alone. Any widening,
  drift, invalid conformance, or uncertainty fails before canary or output
  acceptance.
- Failure proves: A child, descendant, or app-server side-effect path can
  bypass parent-only materialization.
- Evidence artifact: v3 preflight projection/conformance results and controlled
  branch fixtures
- Automation location: `scripts/test-boundary-proof.py`;
  `scripts/boundary_proof_behavior.py`
- Required by milestone: M2 preflight gate

### T57. Workspace integrity is bounded, race-resistant, and precedes materialization

- Covers: R28y
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-8, CMD-BFP-9
- Fixture/setup: Exact canary and lifecycle integrity policies; root-anchored
  fixture trees at every entry, path-byte, aggregate-path-byte, observation,
  and deadline boundary; created, changed, removed, replaced, symlinked,
  special, unstable, unreadable, invalid-UTF-8, and raced entries.
- Steps: Retain one no-follow root descriptor; capture the complete baseline;
  run normal completion, confirmed-stop timeout, and uncertain-liveness
  variants; inspect only after the first two; compare every baseline path and
  bounded unexpected entry. Exercise every closed failure reason and
  precedence, complete/overflow/invalid scan state, exact observation
  identity, and the derived 271-byte baseline-failure maximum.
- Expected result: Only a complete unchanged observation may continue.
  Complete or overflowing mutation routes to `stage-workspace-mutated`;
  invalid inspection routes to `stage-workspace-inspection-failed`; baseline
  failure returns the bounded `workspace-baseline-failure-v1` object;
  uncertain liveness performs
  no inspection. No failing route materializes, publishes, or retries.
- Failure proves: Mutation, traversal races, unbounded evidence, or inspection
  uncertainty can be mistaken for a safe workspace.
- Evidence artifact: workspace-integrity fixtures and value-free observations
- Automation location: `scripts/test-boundary-proof.py`;
  `scripts/boundary_proof_behavior.py`
- Required by milestone: M2

### T58. Envelope routing and parent materialization are exhaustive

- Covers: R28y
- Level: integration
- Command IDs: CMD-BFP-1, CMD-BFP-9, CMD-BFP-11, CMD-BFP-12
- Fixture/setup: Exact canary and lifecycle artifact policies; candidate
  records at equality and one byte over every raw, canonical, per-artifact,
  aggregate, and cardinality limit; every output state, diagnostic tuple,
  attempt, workspace state, and materialization/content observation.
- Steps: Enumerate every listed routing-matrix row and representative
  vocabulary-valid unlisted tuples. Require one fresh attempt only after
  confirmed stop, zero candidates, unchanged workspace, and no non-output
  failure. For accepted or reconciled complete candidates, materialize exact
  UTF-8 bytes relative to the retained root descriptor, reread the complete
  leaf set, and run structural content validation. Attempt response-selected
  policies, path escapes, semantic repair, early or nonterminal
  materialization, stale observations, and a second retry.
- Expected result: Every legal tuple selects exactly one decision; every
  unlisted or inconsistent tuple fails closed. Only complete unchanged output
  reaches the parent materializer. Complete timeout output reconciles without
  reinvocation; exactly one safe absent-output retry is possible; validation
  never invokes a lifecycle skill.
- Failure proves: Retry can duplicate work, invalid output can materialize, or
  the adapter can become a competing semantic author.
- Evidence artifact: transport fixtures, immutable run transport rows, and
  `validation-m2.md`
- Automation location: `scripts/test-boundary-proof.py`;
  `scripts/boundary_proof_behavior.py`
- Required by milestone: M2

## Fixtures and data

- Boundary-first fixtures:
  - `tests/fixtures/boundary-proof/` for valid, invalid, incident, aggregate, activation, and simple-change records
  - `tests/fixtures/boundary-proof/transport/` for test-owned controlled transport failures validated by `scripts/test-boundary-proof.py`
  - `tests/fixtures/boundary-proof/runtime/` for read-only profile, direct and descendant denial, exact runtime projections, common handler conformance, both file-change capability branches, v3 evidence, unsupported-v2 cases, and opaque-v1 compatibility cases
  - `tests/fixtures/boundary-proof/workspace-integrity/` for root-anchored baseline, scan-limit, mutation, overflow, race, invalid-inspection, and bounded failure cases
  - `tests/fixtures/skills/boundary-proof/` for stage behavior and preservation
  - `tests/fixtures/boundary-proof/behavior/happy-path.json`
  - `tests/fixtures/boundary-proof/simple-change/scenario.json`
  - `tests/fixtures/boundary-proof/release/valid-activation/release-notes.md`
  - `tests/fixtures/boundary-proof/release/invalid-partial-activation/release-notes.md`
  - `tests/fixtures/boundary-proof/release/valid-rollback/release-notes.md`
  - exact IDs `BFP-FX-CANONICAL-001`, `BFP-FX-VOCAB-001`, `BFP-FX-TRANSITION-001`, `BFP-FX-IDENTITY-001`, `BFP-FX-ATOMICITY-001`, `BFP-FX-RECOVERY-001`, `BFP-FX-COMPOSITION-001`, and `BFP-FX-SIBLING-001`
- Canonical workflow artifacts:
  - `specs/rigorloop-workflow.md`
  - `specs/rigorloop-workflow.test.md`
  - `docs/proposals/2026-05-01-workflow-refactor.md`
  - `docs/proposals/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `docs/plans/2026-05-03-workflow-refactor.md` as historical context
  - `docs/plans/2026-05-05-pr-self-contained-lifecycle-completion.md`
  - `docs/plan.md`
- Contributor-facing guidance:
  - `README.md`
  - `AGENTS.md`
  - `CONSTITUTION.md`
  - `docs/workflows.md`
  - `.github/pull_request_template.md`
- Canonical skills:
  - `skills/workflow/SKILL.md`
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `skills/ci-maintenance/SKILL.md`
  - `skills/learn/SKILL.md`
  - other stage skills only when M2 identifies stale duplicated handoff wording
- Generated output:
  - `.codex/skills/`
  - `dist/adapters/`
- Validation scripts:
  - `scripts/select-validation.py`
  - `scripts/ci.sh`
  - `scripts/validate-skills.py`
  - `scripts/test-skill-validator.py`
  - `scripts/build-skills.py`
  - `scripts/build-adapters.py`
  - `scripts/validate-adapters.py`
  - `scripts/test-adapter-distribution.py`
  - `scripts/test-select-validation.py`
  - `scripts/test-artifact-lifecycle-validator.py`
  - `scripts/validate-artifact-lifecycle.py`
  - `scripts/validate-change-metadata.py`
  - `scripts/validate-review-artifacts.py`
  - `scripts/test-review-artifact-validator.py`
- Existing fixtures:
  - `tests/fixtures/skills/`
  - `tests/fixtures/change-metadata/`
  - `tests/fixtures/artifact-lifecycle/`
  - `tests/fixtures/review-artifacts/` when review-resolution fixtures are added
  - `docs/changes/0001-skill-validator/`
- New active change-local artifacts when created:
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/change.yaml`
  - `docs/changes/2026-05-08-single-workflow-lane-explain-before-verify/explain-change.md`
  - optional review-resolution or verify-report artifacts when triggered
  - `templates/shared/review-isolation-and-recording.md`
  - `templates/review-resolution.md` or another approved durable scan-first guidance surface

## Mocking and stubbing policy

- Do not mock filesystem structure for validator, generator, drift, selector, lifecycle, or metadata behavior when temp directories or real fixture trees can be used.
- Do not use snapshots as the only proof for workflow behavior.
- Prefer real fixture directories and direct CLI invocations over tests that stub file contents.
- If a test needs stale generated output, create it by controlled edits in a temp copy rather than mocking drift logic.
- If a content assertion is too prose-sensitive, keep it as manual proof unless the approved contract supplies stable IDs, table headers, stage names, or allowed values.
- Do not mock hosted PR metadata for merge-dependent language detection in this first slice. Use tracked files and review-visible manual evidence instead.
- Do not mock the M2 parent-observed sandbox, resolved runtime executable, or
  private runtime-home boundary in promotion proof. Unit tests may inject
  crash points and unavailable profiles, but M2 promotion requires the actual
  read-only preflight and one actual isolated generation.
- Validation tests must consume recorded immutable runs and must not replace
  their invocation profile with the validator process environment.

## Migration and compatibility tests

- `T4`, `T11`, and `T12` verify canonical authored content remains separate from generated Codex and public adapter output.
- `T20` verifies affected workflow-governance surfaces are updated, explicitly marked unaffected, or deferred with owner and follow-up.
- `T21` verifies the `VISION.md` migration is treated as already complete and lowercase `vision.md` is not reintroduced as canonical.
- `T21` verifies project-map lifecycle markers and freshness thresholds are not invented in this refactor.
- `T23` verifies the workflow spec links to the final learn artifact model while preserving nonblocking default behavior.
- `T26` verifies the `skills/ci-maintenance/` path is canonical while contributor-facing stage language uses `ci-maintenance`.
- `T25` verifies in-flight work can record its selected workflow contract without forcing unrelated active work to churn.
- `T29` and `T30` verify existing merge-dependent closeout language is migrated when touched or relied on, while true downstream events keep lifecycle state active.
- `T32` verifies first-slice warning detection stays repository-local and does not depend on hosted PR-description metadata.

## Observability verification

- `T13` verifies selector-selected checks and CI wrapper output use stable check IDs.
- `T18` verifies validation failures are path-specific and contributor-actionable.
- `T20` verifies affected-surface dispositions are review-visible.
- `T23` verifies learn sessions and pre-session closeouts are not chat-only.
- `T27` verifies review-resolution closeout records evidence, dispositions, and blocking state.
- `T30` verifies plan lifecycle validation reports stale plan/index state with path-specific findings.
- `T31` verifies broader lifecycle artifact inconsistency blocks `branch-ready` for touched, referenced, generated, or authoritative artifacts.
- `T32` verifies merge-dependent language warnings identify the tracked file and require contributor-visible classification.
- `T28` verifies change metadata and explain-change artifacts trace the final implementation.

## Security and privacy verification

- `T17` verifies baseline validation does not require repository secrets, network access, or Codex installation.
- Manual review should confirm no fixture, change-local metadata, learn rationale, no-map rationale, or generated output records credentials or sensitive runtime configuration.
- The boundary-first amendment adds a local isolated child-runtime path but no
  external network integration. Opaque authentication may enter only through
  the parent-owned private runtime home; secrets, raw configuration, proxy
  values, and credentials never enter the child workspace or durable evidence:
  `T48`-`T52`, `T55`-`T58`.

## Performance checks

- `T19` is a manual smoke check only; there is no hard benchmark gate for this refactor.
- If selector, lifecycle, skill, generator, or adapter validation becomes noticeably slow, treat it as an implementation issue before final `verify`.
- Broad smoke remains trigger-based and is not the default first proof for this plan.

## Manual QA checklist

- [ ] `README.md`, `docs/workflows.md`, `AGENTS.md`, and `CONSTITUTION.md` present the approved category model without reintroducing the old overloaded chain as the default workflow.
- [ ] The per-change chain excludes default `explore`, default `research`, final per-change `learn`, and ambiguous `ci` wording.
- [ ] `explore` and `research` are described as on-demand support.
- [ ] `learn` is periodic or explicitly invoked, uses final `docs/learn/sessions/**` session records after Frame, and permits no-record closeout only before a session runs.
- [ ] `ci-maintenance` means CI infrastructure maintenance and not validation execution.
- [ ] `review-resolution` is closeout for material review findings and blocks downstream while open.
- [ ] Formal review recording is stage-neutral, triggered by durable review-recording rules, and does not require empty `review-resolution.md` for no-material detailed records.
- [ ] Every material finding is recorded, all material findings require change-local review files, and isolation stops handoff rather than recording.
- [ ] Formal review skills contain byte-identical `## Isolation and Recording` guidance copied from the canonical template.
- [ ] New review-resolution guidance is scan-first and keeps parseable per-finding labels.
- [ ] Plan lifecycle transitions happen inside the PR that performs the transition, before the PR opens for review.
- [ ] Merge is described as a fast-forward of pre-validated lifecycle state, not a trigger for routine closeout.
- [ ] True downstream completion events keep plans active and name the later event or follow-up condition.
- [ ] Tracked merge-dependent language is warned, and any remaining warning has a contributor-visible classification before final handoff.
- [ ] README is updated or explicitly marked unaffected with rationale for this workflow amendment.
- [ ] `VISION.md` and `CONSTITUTION.md` are standing artifacts with distinct absence gates.
- [ ] `docs/project-map.md` is a living reference and cannot be relied on when absent, stale, contradicted, or missing the relied-on area without refresh or no-map rationale.
- [ ] Every affected operating or governance surface is updated, marked unaffected with rationale, or deferred with owner and follow-up.
- [ ] Generated `.codex/skills/` and `dist/adapters/` output is regenerated from canonical skills and passes drift checks.
- [ ] The active plan and `docs/plan.md` agree before final `verify`.
- [ ] The active change-local pack links proposal, spec, test spec, plan, validation evidence, review state, and explain-change.

## What not to test

- Do not test subjective writing quality, philosophy, or style preferences in workflow or skill prose.
- Do not implement or test project-map calendar thresholds, freshness markers, or the full project-map revision workflow.
- Do not test detailed session-record, topic-file, evidence, classification, or routing behavior here; `specs/learn-artifact-model.test.md` owns that proof.
- Do not require a duplicate active legacy CI-maintenance entrypoint.
- Do not re-test or re-migrate root `vision.md` to `VISION.md`; this refactor only ensures `VISION.md` remains canonical.
- Do not test hosted GitHub release publishing end to end.
- Do not require network-dependent checks for baseline validation.
- Do not test exact prose unless the assertion uses stable contract terms, section headings, table headers, stage names, or allowed values.
- Do not inspect hosted PR-description event metadata for merge-dependent language detection in the first enforcement slice.
- Do not define or test merge-SHA recording rules.
- Do not treat deploy, release, package publication, external migration, or unobserved hosted checks as repo-local lifecycle state that can be made true by the PR tree.

## Uncovered gaps

- Independent test-spec review is the remaining authoring gate before
  implementation resumes.
- Project-map lifecycle mechanics are intentionally deferred to a focused follow-up.
- Detailed learn-session behavior is covered by `specs/learn-artifact-model.test.md`.
- Merge-dependent language warning suppression after classification is intentionally not required in the first slice; the required proof is warning visibility plus contributor-visible classification before final handoff treats the warning as addressed.
- If implementation discovers that a stable workflow guarantee cannot be tested manually or through existing scripts, update this test spec or return to plan-review before widening implementation scope.

## Next artifacts

- Boundary-first amendment: focused spec review of the R28y invariant-oracle
  correction, followed by independent test-spec review of this synchronized
  proof map. Resume M2 only after both reviews approve the scenario-owned
  semantic input, stage-owned decomposition, deterministic invariant
  projection, v3 exact runtime projection, common conformance,
  capability-branch, integrity, envelope, retry, publication/rollback, and
  compatibility proof.
- `code-review M2` under the current
  [Boundary-First Proof Modeling plan](../docs/plans/2026-07-25-boundary-first-proof-modeling.md)
  after M2 implementation handoff.
- Continue the approved milestone loop with M3 and M4 until all in-scope
  implementation milestones are closed.

## Follow-on artifacts

- Historical PR-self-contained lifecycle completion and review-recording follow-ons remain recorded in their own plans and change-local artifacts.
- Current amendment follow-on artifacts: none yet.

## Readiness

Active proof-planning and regression surface for the workflow contract,
including the boundary-first R28-R28z amendment.
The focused R28y oracle correction separates scenario-owned behavior,
stage-owned modeling choices, independent semantic review, and deterministic
invariant comparison. It remains pending focused spec review and independent
test-spec review and is not implementation-ready until both gates approve it.

M2 can hand off to
`code-review M2` only after the M2 guidance and contract surfaces make the
relevant assertions and validation commands pass. Each milestone closes only
after clean review and any required review-resolution.
