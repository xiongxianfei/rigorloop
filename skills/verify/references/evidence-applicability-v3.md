# Evidence applicability (v3 staged protocol)

Use this reference only for one resolved active v3 final-readiness attempt. It grants no implementation, correction, routing, or preactivation authority.

For every planned or newly applicable obligation, record its evidence ID, proved surfaces, existing result, authority and subject currency, environment currency, conflicts, freshness, decision, rationale, execution, observed result, and cache status.

Freshness is exactly one of `always-current`, `fresh-required`, or `impact-sensitive`. The decision is exactly one of `reuse`, `rerun`, or `newly-required`. Apply precedence in this order:

1. A new final-diff or policy obligation is `newly-required`. A material plan allocation gap still routes to `plan`; Verify does not silently normalize it.
2. `always-current` and `fresh-required` are `rerun` regardless of ordinary non-impact reasoning.
3. Affected, unknown, missing-surface, stale, failing, conflicting, ambiguous, environment-invalidated, or identity-insufficient evidence is `rerun`.
4. `reuse` requires an existing pass, known proved surfaces, current governing authority and identity, current environment, affirmative `unaffected` evidence for every proved surface, and no freshness override.

Run or directly observe every `rerun`, `newly-required`, `fresh-required`, and `always-current` obligation. Record exact commands and observed results. A cache hit is an inner-loop execution optimization; it is not an actual run, semantic reuse decision, new pass, hosted observation, or readiness proof.

Bind each execution to exactly one proof shape:

- `actual-run` uses `command`: exact argv plus a repository-relative evidence path and SHA-256 identity;
- `hosted-observation` uses `hosted`: provider, run ID, check name, subject revision, evidence path, and SHA-256 identity;
- `reused-pass` uses `prior-evidence`: prior evidence path and SHA-256 identity plus its subject revision;
- `cache-hit` uses only a cache-key identity and never satisfies required final execution;
- `not-run` carries no readiness proof.

An execution label, configured command, cache record, or caller assertion without its matching proof shape is insufficient.

Always-current checks cover current change and repository identity; reviewed subject and review identity; lifecycle and package consistency; review closeout; unresolved blocker state; final diff classification; required artifact and evidence existence; and complete Verify-result consistency.

Re-evaluate every obligation after correction. Unaffected evidence is neither automatically discarded nor automatically retained.
