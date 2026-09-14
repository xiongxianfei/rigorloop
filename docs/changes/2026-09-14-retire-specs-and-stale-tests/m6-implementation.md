# M6: Remove remaining sources and reconcile current operation

Owning change: [change.json](change.json). Stable delivery: [plan](../../plans/2026-09-14-retire-specs-and-stale-tests.md).

The current repository now uses its self-contained Designs, current executable and useful validation without the specs, architecture or ADR source trees. The final 148 removals comprise 111 remaining specs, 27 coupled architecture/ADR members and ten exclusively historical positive v2 examples. Every selected file matched its recorded worktree and recoverable Git identity before removal. The earlier five baseline source relocations/removals remain in reviewed M1/M2 evidence, completing all 116 baseline specs.

The exact approved owner and provenance reconciliation is in [m6-design-reconciliation.json](m6-design-reconciliation.json), with fresh [Design Review](reviews/design-review-m6-reconciled.json) and separate [Delivery Review](reviews/delivery-review-m6-current-basis.json). Three owner/provenance/link findings were corrected and explicitly resolved by their reporter. Current model requirements and behavior did not change during final source reconciliation. Historical approvals and production record bytes were not retargeted.

[Source and test reconciliation](m6-source-removal.json) records exact deletions, the M5 population delta, remaining protective purposes and current dependencies. Governance, contributor/package text, current learn guidance, model navigation and project map now identify current owners. Historical citations use recoverable commit/path identities. Current operations do not fetch the removed inputs from Git.

Actual Git discovery now includes deletions and both rename endpoints in local and committed-range selection. The regression initially failed all six stage/trust partitions; the correction preserves unknown deletion/source rejection even when a known destination is selected. Staged deletions retain HEAD provenance after leaving the index. The broad composer also observes deletions and both endpoints. The PR template selects the existing contributor-guidance checks.

Two surviving selector tests needed final dependency correction: the mixed skill/feature scope test now creates an isolated explicit customer contract, and the obsolete repository workflow-spec wording row is removed while current published-skill rows and executable selector/executor protection remain. The actual candidate test mirrors deleted source trees into its owned pre-commit fixture, preventing its clone from silently restoring a stale dependency.

[Validation evidence](m6-validation.json) names actual commands, successful results, initial failures/corrections and log identities. The complete local combined run and committed PR range are required integration evidence; a reduced explicit file list, model syntax pass or fixture count alone is not completion. M6 Code Review, fresh independent whole-change Code Review and distinct Verify remain separately owned gates.
