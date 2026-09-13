# Test maintenance application

Use this guidance for changes to tests or assessment of their maintenance impact under explicitly adopted Validation-model test criteria. Apply it within the invoked scope. The governing behavior and review policy retain authority; this is not permission to retire behavior, delete tests or waive proof. Historical tests need not be retroactively annotated before unrelated work.

## Decide what changes

Distinguish retain, strengthen, consolidate, replace and remove. Identify the candidate scope, governing obligation, failure detection, boundary and justified diagnostic value. Compare its contribution with retained or replacement proof. Runtime cost, age, similar names, missing labels, coverage numbers or a passing remaining suite alone do not establish redundancy.

For removal or consolidation, explain why no required distinct protection is lost. Establish and assess replacement protection before relying on a reduced suite. If the behavior is intentionally retired, identify the governing owner's explicit decision and its scope; deleting a test cannot retire compatibility. Use existing group-level review and evidence rationale, not a mandatory per-test ledger.

When protection is unknown, retain it while investigating or strengthening its basis. Do not suppress a failing or flaky test solely to obtain green validation. Assess its cause and contractual relevance. Any permitted quarantine needs an authorized owner, tracked follow-up, affected claim limits, and alternative protection or explicit residual-risk treatment under the governing contract.

## Prove the remaining protection

Inspect fixtures, alternate callers, supported versions, runner discovery, selectors and generated output where changes affect detection. Account for removed or renamed cases and their meaningful parameter partitions. Execute proof at the affected boundary; a smaller discovery count or an accidentally omitted test directory is not successful cleanup. Check surrounding tests when a shared fixture or helper changes.

A failing-before/passing-after reproduction or focused mutation may demonstrate replacement detection when feasible; otherwise inspect the exact counterexample mechanism and execute relevant proof. Independent review judges whether the basis suffices. Restore lost tests or repair replacement proof when equivalence fails; preserve contradictory results and route the correction.

Record actual command results, exact subjects, scope and limitations in the existing evidence surface. Apply the project's evidence-applicability policy to reuse; an earlier pass cannot cover a relevant later test, helper, fixture or environment change. An unchanged audit does not require blind reruns. Final whole-change review and distinct Verify remain governed by the existing closeout policy.
