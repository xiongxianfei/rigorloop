# M2 Workflow Scenario Matrix

Stage: implement
Milestone: M2
Result: passed

| Scenario | Published behavior |
| --- | --- |
| One selected target | Target is the complete repository-local continuation boundary; no second authorization parameter |
| Independent review | Records review evidence and matching settlement, then stops without changing routing |
| Workflow-managed review | Routes only after durable review settlement exists |
| Resume | Reuses current evidence, never file existence alone; ambiguity pauses |
| Route-back | Returns a defect to its fixed owner and conservatively replays downstream work after fresh review |
| Status | Read-only |
| Off | Cancels scheduling and preserves evidence |
| Verify failure | Pauses without repair |
| Verify success | Completes the target and stops before PR |
| External action | PR, push, publish, release, deploy, merge, credentials, and destructive Git remain prohibited |

Commands:

- `python scripts/test-skill-validator.py` — passed, 268 tests with 17
  explicitly superseded historical projections skipped.
- `python scripts/validate-skills.py` — passed, 24 canonical skills.
