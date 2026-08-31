# Failure and recovery verification

Use this method when interruption, partial persistence, dependency failure, degraded operation, repair, or reconciliation can change the result.

Identify failure points, committed and uncommitted state, externally visible effects, retry safety, cleanup, and the recovery authority. Allocate proof for failure containment and for returning to one valid state; require byte or identity preservation when the design promises atomicity.

Do not assume a successful retry proves the original failure left no unsafe residue.
