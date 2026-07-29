# M4 Migration Matrix

Stage: implement
Milestone: M4
Result: passed

| Input | Result |
| --- | --- |
| Unmarked historical read | Returned without mutation |
| First resumed nonterminal mutation | Validated current record written atomically |
| Repeated migration | `already-current`, no mutation |
| Terminal historical run | Rejected as read-only |
| Stale expected identity | Concurrent-state error |
| Structured target drift | Rejected |
| Stop-reason drift | Rejected |
| Completed legacy receipts without evidence pointers | Rejected |
| Mixed current and legacy writers | Rejected by metadata semantics |

Commands:

- `python scripts/test-change-metadata-validator.py` — 61 passed.
- `python scripts/test-workflow-automation-state.py` — 65 passed.

The reciprocal-notice and dependent-proof inventory remains recorded in
`compatibility-audit.md` and the approved test spec. Migration does not edit
plans, governed artifacts, historical records, or dependent test specs.
