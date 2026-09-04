# M3 R6 milestone-selection specification correction

Authoring result: complete

Artifact path: specs/compact-current-state-change-record.md
Prior artifact identity: sha256:4968701745819f720bc39c9ed938c54e1b874c2020b46584420f3a267067fbda
Artifact identity: sha256:1ef428c5a0205134fc1b636b58cafbe8365cbaf728e4e0c6b5a5e68598e3ef48
Finding IDs: CCSR-M3-CR7
Evidence state: complete

The specification now defines typed milestone remaining work and a minimal `advance-milestone` activation branch. At Implementation with no active work, `null → planned` selects one exact pending implementation-owned milestone, removes it from remaining work, and lets the evaluator construct active state. Missing, blocked, wrong-kind, wrong-owner, stale, repeated, and caller-constructed alternatives reject unchanged. Closure clears active work; a remaining pending milestone selects the explicit Code Review-to-Implementation edge before another activation.

## Validation

- `python scripts/validate-boundary-first.py --check --path specs/compact-current-state-change-record.md`: passed.
- `python scripts/validate-documentation-prose.py --mode enforce --path specs/compact-current-state-change-record.md`: passed with zero errors and warnings.
- `python scripts/validate-markdown-readability.py specs/compact-current-state-change-record.md`: passed with advisory long-line warnings.
- `git diff --check`: passed.

## Handoff

The exact corrected specification requires architecture reconciliation and fresh consolidated Design Review. This evidence does not claim Design approval, Delivery readiness, or implementation readiness.
