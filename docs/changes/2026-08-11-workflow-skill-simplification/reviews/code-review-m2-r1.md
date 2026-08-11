# Workflow Skill Simplification Code Review M2 R1

Review ID: code-review-m2-r1
Stage: code-review
Round: r1
Reviewer: Codex independent code-review context
Target: M2 commit `b755f418`
Reviewed artifact: commit `b755f418`
Status: changes-requested
Review status: changes-requested
Review date: 2026-08-11
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, invocation manifest, review log, and review resolution
- Open blockers: WFSIM-CR1, WFSIM-CR2, WFSIM-CR3
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: WFSIM-CR1, WFSIM-CR2, WFSIM-CR3
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-11-workflow-skill-simplification/reviews/code-review-m2-r1.md`
- Review log: `docs/changes/2026-08-11-workflow-skill-simplification/review-log.md`
- Review resolution: `docs/changes/2026-08-11-workflow-skill-simplification/review-resolution.md#code-review-m2-r1`
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3
- Required review-resolution: yes
- Finding IDs: WFSIM-CR1, WFSIM-CR2, WFSIM-CR3
- Verify readiness: not-claimed

## Review boundary and risk map

The blind-first review inspected commit `b755f418` against R1-R20 and R30 before using implementation validation summaries. Highest-impact risks were universal policy hidden by extraction, an invalid predicate combination accidentally proceeding, durable automation created before governed authority, competing reference ownership, missing-resource fallback, or preservation evidence drifting from the final package.

Direct inspection covered the complete changed `SKILL.md`, all three new references, the changed validator tests, the spec requirements, plan M2, test-spec proof map, and actual commit diff. Adapter archive parity and final assembly measurements remain M3 scope. Risk tier is elevated; independence level L0 used an artifact-and-criteria reset. No second review is required after a complete context-reset rereview.

## Material findings

## Finding WFSIM-CR1

Finding ID: WFSIM-CR1
Severity: major
Location: `skills/workflow/SKILL.md`, Inputs, Invocation classification, and Resource map
Evidence: R2 requires unknown-stage behavior inline, but the dispatcher names only unknown artifact types. R5 requires an explicit stop for every predicate combination outside the seven assemblies, but the text stops only two named invalid families. R16 requires resource confirmation after classification and before dependent interpretation or action, while the current wording states only the result after a resource is already known missing.
Required outcome: Keep unknown-stage failure, the catch-all unlisted-combination stop, and the post-classification/pre-action resource check explicit in `SKILL.md`.
Safe resolution path: Add three concise universal clauses and focused assertions in `WorkflowSkillSimplificationContractTests`; do not move conditional procedure back inline.
needs-decision rationale: none
auto_fix_class: declared-safe

## Finding WFSIM-CR2

Finding ID: WFSIM-CR2
Severity: major
Location: `skills/workflow/references/bounded-workflow-automation.md#Automation bootstrap`
Evidence: R7 requires command recognition, automation-reference loading, governed identity resolution, validation, reclassification, governed-reference loading, then persistence. The normative ordered list starts at command recognition and goes directly to identity resolution; the main Resource map proves the reference is used but does not make that load step part of the reference's exact sequence.
Required outcome: Represent every R7 step in one exact ordered bootstrap list and assert the complete order.
Safe resolution path: Insert automation-reference loading after recognition, renumber the list, and add the missing phrase to the existing order test.
needs-decision rationale: none
auto_fix_class: mechanical

## Finding WFSIM-CR3

Finding ID: WFSIM-CR3
Severity: major
Location: `workflow-rule-disposition.yaml` and `workflow-literal-compatibility.yaml`
Evidence: Twenty-one rule destinations name headings absent from the final package, including `#Purpose and routing role`, `#Lifecycle routing`, and `#Automated review gates`; R21 requires one destination for every significant rule. `WF-LIT-012` classifies `Quick operating guide` as test-only incidental even though `specs/progressive-loading-high-cost-public-skills.md` R2-R2a normatively requires the exact heading and labels. `WF-LIT-013` similarly treats `Workflow Categories` as incidental while a permanent contract assertion retains it.
Required outcome: Make every rule destination resolve to an actual final heading and classify exact literals from their highest governing authority rather than from consumer implementation alone.
Safe resolution path: Update destinations to real headings, reclassify `WF-LIT-012` as `normative-contract`, investigate and accurately classify `WF-LIT-013`, and add deterministic destination-resolution proof without creating a new validator family.
needs-decision rationale: none
auto_fix_class: declared-safe

## Requirement-fidelity receipt

| Contract area | Result | Direct evidence |
| --- | --- | --- |
| R1-R3 package ownership | pass | Canonical package maps three references plus the existing boundary reference and structural skeleton. |
| R4-R5 classification | concern | Four predicates and seven assemblies exist; the catch-all invalid-combination result is not explicit. |
| R6-R9 bootstrap and authority | concern | Command/armed separation and transient state are present; R7's automation-reference load is absent from the ordered list. |
| R10-R14 exclusive resource ownership | pass | Governed, automation, guide, and skeleton responsibilities are non-overlapping and one-way. |
| R15-R18 failure safety | concern | Contradiction and missing/mixed resource stops are present; R16 timing is not explicit. |
| R19-R20 stateless and stale identity | pass | `WPS`, `no-active-run`, no state creation, target binding, and stale-identity pause are present. |
| R21-R24 preservation inventories | block | Twenty-one destinations do not resolve and at least one literal classification conflicts with approved authority. |
| R30 lifecycle preservation | pass with correction | Core stage, milestone, review, claim, and handoff behavior is retained across the common and governed paths. |

## Checklist coverage

| Check | Verdict | Evidence |
| --- | --- | --- |
| Spec alignment | block | WFSIM-CR1 through WFSIM-CR3 identify direct requirement-property omissions. |
| Test coverage | concern | Focused tests cover the broad model but omitted three properties exposed by review. |
| Edge cases | concern | The unlisted predicate catch-all is not stated. |
| Error handling | concern | Required-resource check timing is compressed. |
| Architecture boundaries | pass | Existing package ownership is preserved; references have no independent lifecycle authority. |
| Compatibility | block | Literal classification and final destinations are stale. |
| Security/privacy | pass | No credentials, external mutation, target runtime, or retained transcript was introduced. |
| Derived artifact currency | not-assessed | M3 owns archive and installed parity. |
| Unrelated changes | pass | Diff is limited to M2 package, tests, and evidence. |
| Validation evidence | not-used-for-first-pass | Evidence challenge follows this recorded risk map and verdict. |

## Handoff

Resolve WFSIM-CR1 through WFSIM-CR3 within M2, rerun the named deterministic checks, and perform a context-reset M2 rereview before milestone closeout.
