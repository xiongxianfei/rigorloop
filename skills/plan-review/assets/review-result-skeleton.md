<!-- Template: plan-review-result-skeleton-v1 -->
<!-- Skill: plan-review -->
<!-- Template status: normative -->
<!-- Maintained alongside: skills/plan-review/SKILL.md -->

# <plan review result>

## Core operation

- Skill: plan-review
- Review target: <plan path and revision>
- Operation: <initial-review | settlement-retry>
- Transaction result: <recorded-isolated | initialization-required | revision-required | blocked | settled-active | not-settled>
- Open blockers: <blockers or none>
- Immediate next stage: <test-spec | plan revision | review-resolution | none>
- Claim limitations: <claims not established>

## Semantic judgment

- Judgment mode: <performed | reused>
- Review ID: <review ID>
- Review round: <round>
- Reviewed plan identity: <identity>
- Review status: <approved | changes-requested | blocked | inconclusive>
- Material findings: <finding IDs or none>

## Durable recording

- Recording status: <recorded | blocked>
- Recording blocker: <blocker or none>
- Review record: <path or blocked>
- Review log: <path or blocked>
- Review resolution: <path, not-required, or blocked>

## Governed settlement

- Change identity: <change ID>
- Plan-entry identity: <entry ID and path>
- planned_work basis: <absent | matching | invalid>
- Entry state before: <state>
- Entry state after: <state>
- Settlement result: <result>
- Formal test-spec eligibility: <state>

## Boundary review

- Boundary applicability: <state>
- Boundary resources: <resources>
- Boundary result: <result or blocker>

## Workflow-managed review

- Execution mode: workflow-managed
- Manifest identity: <identity>
- Automation authority: <state>
- Promotion or pause result: <result>

## Findings

<material finding blocks or none>
