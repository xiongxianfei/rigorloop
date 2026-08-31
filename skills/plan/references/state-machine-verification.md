# State-machine verification

Use this method when correctness depends on governed states, transitions, predecessors, or invariants.

Allocate proof for permitted transitions, prohibited transitions, terminal states, repeated operations, and invariants before and after failure. Cover only outcome-distinct paths; do not enumerate a Cartesian transition matrix when equivalence classes provide the same proof.

Keep transition behavior specification-owned. The plan identifies where each state responsibility is implemented and which milestone or change-level group must demonstrate it.
