# Code Review M5 R1

Review ID: code-review-m5-r1
Stage: code-review
Round: r1
Reviewer: Codex code-review skill
Target: M5. Activate v2 atomically and retire standalone entrypoints
Reviewed artifact: implementation commit `c67ef259` (`M5: activate plan-centered verification workflow`)
Reviewed milestone: M5
Review date: 2026-08-31
Status: changes-requested
Review status: changes-requested
Material findings: RTS-M5-CR1, RTS-M5-CR2
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review, `review-log.md`, and `review-resolution.md`
- Open blockers: `RTS-M5-CR1`, `RTS-M5-CR2`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `RTS-M5-CR1`, `RTS-M5-CR2`
- Recording status: recorded
- Reviewed milestone: M5
- Milestone closeout: resolution-needed
- Required review-resolution: yes
- Verify readiness: not-claimed

## Scope

Reviewed exact implementation commit `c67ef259` against approved Design package `design-review-r2`, Delivery package `delivery-review-r3`, M5 requirements and verification groups, the frozen activation manifest, and the recorded validation evidence. The later workflow-only handoff commit was inspected only to confirm review-requested state.

## Material findings

## Finding RTS-M5-CR1

Finding ID: RTS-M5-CR1
Severity: major
Location: `skills/workflow/references/bounded-workflow-automation.md:9`; `skills/workflow/assets/workflows-skeleton.md:39`; `skills/workflow/assets/workflows-skeleton.md:82`; `skills/workflow/assets/workflows-skeleton.md:167`
Evidence: M5 removes the canonical test-spec skill and active top-level target list, but the conditionally loaded automation reference still publishes `test-spec` as a supported target. The workflow guide skeleton still generates a per-change chain containing `test-spec`, registers `test_spec` with owner `test-spec`, and labels it an active proof-map stage. These files are packaged resources of the active workflow skill, so loading automation or generating a customer guide reintroduces the retired entrypoint after activation. The M5 skill and adapter tests inspect the common skill body and archive inventory but do not assert the content of these conditional workflow resources.
Required outcome: remove standalone test-spec from every active workflow target, generated-guide chain, registry, artifact table, and ownership statement, and add regressions that inspect the packaged conditional reference and skeleton rather than only the common skill body.
Safe resolution path: update the bounded automation reference and workflow skeleton to the v2 plan-centered route; extend skill/build/adapter tests to assert absence in both resources; rerun CMD-07, CMD-08, CMD-09, and CMD-13.
needs-decision rationale: none; these are active published resources directly covered by the approved retirement scope.

## Finding RTS-M5-CR2

Finding ID: RTS-M5-CR2
Severity: major
Location: `skills/plan/references/governed-plan-authoring.md:21`
Evidence: the common plan skill correctly states that manifest-bound v1 work is already post-delivery and never re-enters authoring, but its governed authoring reference still directs registered v1 planning to hand off to `test-spec`. Activation prerequisites guarantee every nonterminal prior-contract record is at implementation or later, and the standalone skill is now absent. Loading this conditional reference therefore contradicts the common contract and can route work to a nonexistent retired stage. Existing tests assert the common plan text but do not inspect this reference for post-activation routing.
Required outcome: make governed plan authoring v2-only for new authoring and treat manifest-bound v1 as post-gate continuation that cannot enter plan authoring or test-spec handoff; add a regression over the conditional reference.
Safe resolution path: replace the stale contract-selected handoff sentence with a v2 Delivery Review handoff and explicit fail-closed v1 authoring boundary, then rerun CMD-07, CMD-08, and CMD-13.
needs-decision rationale: none; this is a direct consistency correction within the approved compatibility boundary.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Active conditional resources still expose the retired stage, contrary to RTS-R1, RTS-R2, RTS-R17, and RTS-R23. |
| Test coverage | block | Green suites omit content assertions for the affected workflow and plan conditional resources. |
| Edge cases | block | Automation loading and guide generation are alternate public paths that escape the common-body retirement. |
| Error handling | concern | Manifest-bound v1 authoring is routed to a missing skill instead of failing closed as post-gate-only compatibility. |
| Architecture boundaries | block | Published package composition is mixed: active common guidance and conditional resources disagree. |
| Compatibility | pass | Frozen history and post-delivery v1 runtime continuation remain unchanged. |
| Security/privacy | pass | No security, credential, network, or sensitive-data issue was found. |
| Derived artifact currency | block | Archives omit the skill directory but package stale workflow guidance that recreates its route. |
| Unrelated changes | pass | The reviewed diff is otherwise scoped to M5 activation and evidence. |
| Validation evidence | concern | All named commands pass, but direct inspection found untested active-resource contradictions. |

## Handoff

- Reviewed milestone: M5
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Required review-resolution: yes
- Recommended next stage: resolve `RTS-M5-CR1` and `RTS-M5-CR2`, return the bounded correction to M5 implementation, rerun the named validation, and rereview.
- Final closeout readiness: not ready.
