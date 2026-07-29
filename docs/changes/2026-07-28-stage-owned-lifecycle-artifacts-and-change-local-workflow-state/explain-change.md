# Change Explanation

Stage: explain-change
Change: Stage-Owned Lifecycle Artifacts and Change-Local Workflow State
Result: current

## Why the implementation changed

Approved lifecycle artifacts had become both durable contracts and mutable
workflow dashboards. That let downstream automation rewrite upstream content,
made author/review ownership unclear, and forced published skills to carry
profiles, capabilities, selectors, and synchronization rules.

The accepted proposal and SLA-R001-SLA-R074e replace that design with one
portable rule: governed content is stable; each stage writes only its own
artifact or evidence; matching review peers settle only the matching
change-local entry; workflow alone owns routing.

## Meaningful implementation changes

| Change | Why | Governing evidence | Proof |
| --- | --- | --- | --- |
| Canonical skills and assets remove upstream write-back | Enforces fixed stage ownership in the user-facing product | SLA-R013-R033, SLA-R042-R047, ADR decision 1 | M1 semantic matrix and skill tests |
| Workflow skill uses one selected target and evidence-first recovery | Preserves automatic continuation without another public authorization parameter | SLA-R048-R064a, ADR decisions 3-4 | M2 scenario matrix |
| Existing change-metadata path validates artifact, workflow, milestone, blocker, review, and automation state | Gives deterministic failure behavior without a second workflow engine | SLA-R005-R041, SLA-R070 | 61 metadata tests |
| Existing state module adds bounded atomic persistence and prospective migration | Keeps historical reads unchanged and migrates only resumed nonterminal work | SLA-R003-R004, SLA-R065-R068 | 65 state-adapter tests and M4 matrix |
| Generated adapter parity is rebuilt from canonical skills | Keeps published behavior aligned across supported adapters | SLA-R070, SLA-R072-R074b | 133 adapter tests and broad smoke |
| Workflow skill creates `stage-owned-change-local-v1` by default | Makes the approved mechanism the sole forward model with no selector | SLA-R001-R002, M6 activation owner | Focused activation test and post-cutover broad smoke |
| Change-local milestone evidence | Existing PR routing treated the required `evidence/` directory as unsupported | One exact directory boundary reuses lifecycle validation; unknown paths still fail closed | 136 selector tests |

## Review-driven corrections

- SLA-CR-M3-1 added the missing review-outcome-to-artifact-state consistency
  check, including ADR settlement.
- SLA-CR-M6-1 added direct regression proof for the exact activation marker,
  one-time migration boundary, and side-effect-free historical reads.

Both findings are accepted, resolved, retested, and closed in
`review-resolution.md`. Final holistic review found no additional material
issues.

## Scope and preservation

No document-content hashes, protected-path interception, hosted service,
selector ledger, new authorization parameter, generic lifecycle validator
family, or automatic PR action was added. Existing historical changes remain
readable. The three unrelated untracked user paths were not modified or
committed.

Final verification owns the remaining readiness decision. Successful verify
must stop before PR.
