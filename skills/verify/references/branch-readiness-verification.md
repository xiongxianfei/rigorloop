# Branch-readiness verification

Load this procedure only after `SKILL.md` classifies `branch-readiness` or `workflow-final-verification` and resolves one exact target. It owns final evidence applicability, completeness, aggregation, verdict calculation, and mode-specific completion. Universal evidence meaning, claim boundaries, stops, stage order, and external-action authority remain in `SKILL.md` or their existing owner.

## Final-readiness prerequisites

Resolve the repository and branch or commit, then bind all evidence to exactly one governed change or explicit evidence root. For a governed-final run, confirm the same change is currently at final `verify` and all in-scope implementation milestones are closed.

Require the applicable governing spec and proof map, architecture or explicit no-architecture assessment, stable plan, current change state, final reviewed diff, review closeout, and named validation commands. Missing, ambiguous, mismatched, or local-only governing authority blocks final readiness.

## Final evidence composition

Determine which evidence classes apply to this target, then assemble them without redefining their item-level meaning:

- requirement-to-test-to-diff traceability, including named boundaries and edge cases;
- targeted proof for every changed or required surface;
- broad smoke for planned initiatives, explicit triggers, or `broad_smoke_required: true`;
- current observed hosted CI when final readiness depends on CI;
- source-to-generated-output currency for every affected generated surface;
- permitted and complete manual proof;
- security, migration, rollback, documentation, operational, and release-sensitive evidence when applicable;
- clean branch state and tracked governing artifacts.

Targeted proof alone is insufficient when changes can affect shared infrastructure, generators, packaging, lifecycle validation, or another broad surface. Release-sensitive evidence adds applicable release checks but never expands the verdict into publication or release-completion authority.

## Lifecycle and review closeout

For governed final verification, confirm the current change record, stable plan, milestone state, formal review evidence, and any review resolution agree. Every material finding must have final disposition and required validation; no open or `needs-decision` finding may remain. Confirm architecture assessment and triggered CI-maintenance are settled. Generate the final explanation only in a successful Verify report.

For a direct branch-readiness assessment, evaluate the same applicable evidence set but do not mutate lifecycle state or perform workflow-owned settlement.

## Final blocker aggregation

Aggregate blockers across authority, requirements, proof, implementation, review, lifecycle, generated output, CI, manual proof, risk, release applicability, and branch state. Do not average, downgrade, or hide a blocker because other dimensions pass.

Return `not-ready` when any required class is missing, stale, conflicting, failing, or bound to another target. Report each blocker with its owning stage and safe next action.

## Verdict and completion

Return `branch-ready` only when every applicable prerequisite and evidence class passes for the exact target. Otherwise return `not-ready`; do not use a partial or “mostly ready” final verdict.

Before returning `branch-ready`, record the normalized `verification_basis` owned by `SKILL.md` in the applicable result or verify-report surface. Bind it to the exact evidence target and current base/head relationship. Historical prose or command output that lacks the complete normalized basis remains useful context but cannot establish current branch readiness.

In `isolated` mode, report the assessment and stop. Do not write workflow state or invoke `pr`.

In `governed-final` mode, write only verify-owned evidence required by the existing project contract, then return the verdict to `route`. A clean result names `pr` as the next stage but does not prepare, open, or authorize it.

If this reference becomes unavailable or contradicts `SKILL.md`, stop under the package-integrity rule in `SKILL.md`.
