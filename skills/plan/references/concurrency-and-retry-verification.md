# Concurrency and retry verification

Use this method when ordering, duplicate work, idempotency, races, stale revisions, or retry policy can change the outcome.

Identify the competing actors or operations, the state observed at each decision boundary, and the required outcome for winner, loser, duplicate, timeout, and retry paths. Allocate deterministic proof where feasible and name any controlled timing or stress evidence needed.

Require preservation of authority and state invariants. Do not let a timing-heavy test substitute for an unspecified concurrency contract.
