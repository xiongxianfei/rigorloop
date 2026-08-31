# Boundary and negative-case verification

Use this method when outcomes differ across input classes, system seams, invalid operations, or rejected states.

For each affected SR or boundary, identify representative valid partitions, invalid partitions, exact edge values, and the invariant that rejection must preserve. Allocate the objective to the earliest safe milestone that owns the boundary; use a change-level group when several components jointly enforce it.

State what must be demonstrated, including unchanged state or absence of side effects after rejection. Leave filenames, fixtures, mocks, and assertion mechanics to implementation.
