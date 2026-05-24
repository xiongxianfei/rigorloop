# Cache-Aware Inner-Loop Lifecycle Validation Helper

## Status

accepted

## Problem

RigorLoop has a conservative validation cache for the first approved command family, but the first observed opportunity to use it did not use it. The root cause is not cache correctness; it is adoption design. The cache exists as an opt-in validator feature, while the command paths that agents already follow still call explicit lifecycle validation without cache flags.

This repeats a pattern already seen elsewhere in the project:

```text
A capability that depends on every caller remembering to invoke it
is not adopted; it is merely available.
```

For cache adoption, the failure mode is specific:

```text
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
```

is still the command shape written into plan, test-spec, and verify habits, while the cache-aware command requires extra flags and context. The safe cache mechanism exists, but the normal path does not guide callers to it.

The missing piece is a mechanism that makes the safe cached inner-loop path easy to use without making it eligible for closeout.

## Goals

- Make the approved validation cache usable through the command path agents and maintainers already take.
- Add a cache-aware inner-loop lifecycle validation helper or command mode for the existing eligible command family.
- Preserve the strict boundary that cache hits are inner-loop evidence only.
- Preserve actual-run evidence for milestone closeout, verify, PR-readiness, and other final gates.
- Update plan and test-spec guidance so validation is written as two distinct command kinds: inner-loop cache-eligible commands and closeout actual-run commands.
- Make cache usage visible in evidence as `cache-hit-inner-loop`, distinct from `actual-run-pass`.
- Keep cache eligibility limited to `validate-artifact-lifecycle.py --mode explicit-paths`.
- Measure actual cache-hit savings before expanding eligibility to other validators.
- Avoid changing validation semantics, selected checks, lifecycle validator behavior, or closeout requirements.

## Non-goals

- Do not expand cache eligibility to `validate-change-metadata.py`, `validate-review-artifacts.py`, selected CI, npm tests, GitHub metadata checks, external-state proof, or release checks.
- Do not replace stage-closeout full-bundle validation.
- Do not make cache hits count as closeout proof.
- Do not make cache use automatic for every lifecycle validation invocation.
- Do not change the cache key, input-surface hash, implementation-manifest, policy-hash, or local-cache safety model.
- Do not change validator pass/fail semantics.
- Do not hide failures, blockers, stale readiness, review drift, or selector/routing changes.
- Do not cache validation when selector, CI, validator, or routing files changed.
- Do not introduce edit-scoped validation.
- Do not rely on an agent's claim that an edit is safe or prose-only.
- Do not proceed to broader cache families before measuring the inner-loop helper's actual benefit.

## Vision fit

fits the current vision

RigorLoop's validation model exists to make artifact-driven work safe to inspect, review, and advance. The cache is valuable only when it avoids redundant work without weakening defect detection. This proposal supports that model by improving adoption of the safe path, not by broadening cache power.

The proposal is falsified if any of these occur:

```text
- a cache hit satisfies closeout, verify, branch-readiness, or PR-readiness;
- a helper name or plan template makes cache evidence look like actual-run proof;
- a routing, selector, CI, validator, or external-state change is skipped because a lifecycle cache hit exists;
- cache evidence is not reviewable;
- a caller still has to remember a long flag set for the common inner-loop case;
- cache eligibility expands without a new approved spec/test-spec change;
- actual-run closeout evidence becomes optional or ambiguous.
```

## Initial intent preservation

| Initial user goal | Proposal treatment | Where recorded |
| --- | --- | --- |
| Make cache adoption real, not flag-dependent | in scope | Goals, Recommended Direction |
| Add a cache-aware inner-loop helper or template | in scope | Recommended Direction |
| Preserve closeout actual-run validation | in scope | Non-goals, Closeout Boundary |
| Keep cache evidence visible and distinct | in scope | Evidence Contract |
| Keep eligibility limited to the approved command family | in scope | Scope Budget, Non-goals |
| Update plan and test-spec templates | in scope | Plan and Test-Spec Command Guidance |
| Measure savings before expansion | in scope | Measurement Gate |
| Avoid edit-scoped validation | out of scope | Non-goals |
| Avoid broader validator caching | deferred follow-up | Next Artifacts |

## Scope budget

| Work item | Treatment | Reason |
| --- | --- | --- |
| Cache-aware inner-loop lifecycle helper | core to this proposal | This directly fixes the adoption gap. |
| Inner-loop versus closeout command separation | core to this proposal | This prevents cache-as-closeout confusion. |
| Plan/test-spec validation command guidance | same-slice dependency | Command templates currently teach the no-cache habit. |
| Cache-hit evidence display and reference guidance | same-slice dependency | Cache hits must remain auditable and visibly distinct. |
| Measurement of cache-hit usage and savings | same-slice dependency | Expansion should be evidence-driven. |
| Cache eligibility expansion | separate proposal | New command families are new stale-cache risk surfaces. |
| Edit-scoped validation | separate proposal | Misclassification can skip needed checks. |
| Closeout cache eligibility | out of scope | First-slice rule remains actual-run closeout only. |
| Selector/CI routing changes | out of scope | Cache does not replace fresh routing checks. |

## Context

The prior validation-idempotency proposal prioritized caching over edit-scoped validation because unchanged inputs make skip safety provable, while edit classification can hide defects. It treats broader caching as a measured follow-up and says cache hits require a previous pass plus identical command, implementation, policy/config, and input-surface identity.

The current adoption problem is different. The safe cache exists, but callers continue to use the old direct lifecycle validation command. The correction is to make the cache the default path for the eligible inner-loop command, not a flag set callers have to remember.

The closeout boundary remains central: cache may serve repeated inner-loop checks, but final milestone, verify, and PR-readiness need actual-run evidence. A helper should be named and shaped so it cannot be mistaken for closeout proof.

## Options Considered

### Option 1: Do nothing

Keep cache usage as an opt-in flag on `validate-artifact-lifecycle.py`.

Pros:

- No new code or template changes.
- Lowest implementation risk.
- Safety model remains untouched.

Cons:

- Agents and maintainers continue to forget the cache path.
- Cache remains available but not adopted.
- Measurement data undercounts actual cache value because the helper is not used.
- The same repeated validation cost persists.

### Option 2: Document the flags more prominently

Add better docs saying to use the cache flags for inner-loop lifecycle validation.

Pros:

- Low cost.
- Improves discoverability.
- No runtime changes.

Cons:

- Still relies on caller memory.
- Does not change plan/test-spec command templates.
- Likely repeats the same failure mode later.

This option is insufficient because it preserves the caller-memory failure mode.

### Option 3: Make `validate-artifact-lifecycle.py` use cache by default

Turn cache on for all explicit-path lifecycle invocations.

Pros:

- Highest adoption.
- No separate helper to learn.

Cons:

- Risky because closeout commands use the same validator family.
- A caller could accidentally produce cache-hit evidence where actual-run evidence is required.
- Requires more invasive changes to closeout detection and evidence validation.
- Makes the safe inner-loop boundary less visible.

This option is too broad for the first adoption slice.

### Option 4: Add a named inner-loop helper or mode

Add a wrapper or command mode that means cache-aware lifecycle validation for repeated inner-loop checks only. Keep the existing direct command for closeout actual-run validation.

Pros:

- Builds adoption into the command path.
- Keeps inner-loop and closeout structurally distinct.
- Preserves the existing actual-run closeout guarantee.
- Does not expand cache eligibility.
- Makes plan/test-spec command templates clearer.

Cons:

- Adds another command surface.
- Requires tests to prove it cannot satisfy closeout.
- Requires documentation and plan/test-spec updates.

This is the recommended option.

### Option 5: Add helper plus broad template rewrites and cache expansion

Add the helper and immediately expand all validation templates and validators to use cache where possible.

Pros:

- Maximum speedup.

Cons:

- Too broad.
- Blurs adoption fix with eligibility expansion.
- Increases stale-cache risk.
- Requires complete input-surface contracts for other validators.

This option is out of scope for this proposal.

## Recommended Direction

Choose Option 4.

Add a cache-aware inner-loop lifecycle validation mode with a name that encodes the safety boundary:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop \
  --path <path> \
  --path <path>
```

The first slice does not add a separate wrapper script. The mode internally supplies the approved cache flags and cache context for the existing eligible command family.

The closeout command remains:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path <path> \
  --path <path>
```

The distinction should be obvious from the mode name:

```text
explicit-paths-inner-loop -> may use cache
explicit closeout command -> actual run
```

## Inner-Loop Helper Contract

The helper may use cache only for this command family:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
```

The existing cache identity contract remains authoritative:

```text
- previous result is pass;
- normalized command matches;
- validator implementation hash matches;
- policy/config hash matches;
- complete input-surface hash matches;
- cache key is valid;
- validator ID and command family match;
- no closeout context is being claimed.
```

If anything is unknown, missing, malformed, unsupported, or changed, the helper runs actual lifecycle validation.

On actual run, output should visibly indicate actual validation ran. On cache hit, output should visibly indicate a cache hit, the unchanged input surface, the prior passing result, and the cache key. On cache miss, output should explain the miss reason and then show the actual validation result.

## Evidence Contract

When the helper is used in a formal workflow context and a cache hit occurs, it records or references formal cache-hit evidence in:

```text
docs/changes/<change-id>/validation-cache-evidence.yaml
```

or the approved change-local evidence surface.

Formal evidence is written or merged only when a safe change root or evidence path is supplied or inferable. Local ad hoc use outside a change root may print cache status without writing formal evidence. The helper does not write formal evidence unless the change root or evidence path is explicit and safe.

The evidence should include:

```text
- cache-hit ID;
- validator ID;
- normalized command;
- command family;
- prior passing event;
- input-surface hash;
- implementation hash;
- policy hash;
- cache key;
- reason cache hit is allowed;
- scope: inner-loop;
- closeout_evidence: false.
```

A cache hit is not a new passing validation result. It is evidence that a previous pass still applies.

## Closeout Boundary

The helper is structurally unable to satisfy closeout.

Rules:

```text
- The helper emits cache-hit-inner-loop evidence only.
- The helper does not emit actual-run-pass closeout evidence for cache hits.
- Milestone closeout, verify, branch readiness, and PR readiness use actual-run commands.
- A closeout validation record that references only helper cache-hit evidence fails validation.
```

The existing cache proposal already keeps stage-closeout full-bundle validation mandatory. This proposal keeps that rule intact and makes it easier to follow.

## Plan and Test-Spec Command Guidance

The spec and test spec define the exact helper contract. Repository-local RigorLoop plan and test-spec templates may show the two-command table: inner-loop cache-aware command versus closeout actual-run command.

Published skills do not expose RigorLoop-internal cache commands, validator paths, selector mechanics, or repository maintenance details.

Planning and test-spec guidance should distinguish two command kinds.

| Validation purpose | Command kind | Cache allowed? | Evidence kind |
| --- | --- | ---: | --- |
| Inner-loop artifact lifecycle check | cache-aware inner-loop helper | yes | `cache-hit-inner-loop` or actual-run inner-loop |
| Milestone closeout lifecycle check | direct lifecycle validator | no | `actual-run-pass` or `actual-run-fail` |
| Verify / PR readiness | direct full required bundle | no | actual-run evidence |
| Selector / CI / routing proof | existing selected/explicit CI commands | no | actual-run evidence |
| External-state proof | governing command | no | actual-run evidence |

Example plan validation table:

```md
| Stage | Purpose | Command | Evidence kind |
| --- | --- | --- | --- |
| Inner loop | Repeat lifecycle check after small evidence edits | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop ...` | `cache-hit-inner-loop` allowed |
| Closeout | Close milestone after implementation/review-resolution | `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` | `actual-run-pass` required |
```

## Routing and CI Boundary

Cache applies to:

```text
lifecycle validation of unchanged explicit-path artifact inputs
```

Cache does not apply to:

```text
selector changes
CI wrapper changes
validation-selection changes
validator implementation changes
policy/spec changes
GitHub metadata or other external-state proof
npm tests
release verification
review-artifact validation
change-metadata validation
```

The helper is not a substitute for rerunning selector and CI paths after routing changes.

CI does not use the helper in the first slice. CI remains actual-run.

## Expected Behavior Changes

- Agents and maintainers have a short, explicit inner-loop lifecycle validation command that uses the cache safely.
- Plans and test specs distinguish inner-loop cache-eligible validation from closeout actual-run validation.
- Cache hits become more likely during repeated lifecycle evidence edits.
- Cache-hit evidence remains visibly distinct from actual-run evidence.
- Closeout, verify, branch-readiness, and PR-readiness still require actual-run proof.
- Cache eligibility does not expand beyond the approved explicit-path lifecycle validator family.

## Architecture Impact

| Surface | Impact |
| --- | --- |
| `scripts/validate-artifact-lifecycle.py` | Add an `explicit-paths-inner-loop` mode for inner-loop cache usage. |
| `scripts/validation_cache.py` | May add helper APIs for cache-aware invocation and evidence recording, without changing identity semantics. |
| `scripts/test-validation-cache.py` | Add helper or mode tests for cache hit, cache miss, actual-run fallback, and closeout rejection. |
| `scripts/test-artifact-lifecycle-validator.py` | Add coverage if the mode lives in the lifecycle validator. |
| `specs/validation-idempotency-and-cache-hit-safety.md` | May require an amendment for the helper or mode contract. |
| `specs/validation-idempotency-and-cache-hit-safety.test.md` | Add helper or mode behavior tests. |
| Repository-local plan and test-spec templates | May add guidance separating inner-loop and closeout command kinds. |
| Published skills | Do not expose RigorLoop-internal cache commands, validator paths, selector mechanics, or repository maintenance details. |
| Generated adapters | Affected only if skill guidance changes; validate generated output if touched. |
| CI / selector routing | No intended behavior change. |

## Testing and Verification Strategy

Likely checks:

| Check ID | What is verified |
| --- | --- |
| `VIC-IH-001` | Inner-loop helper exists and is distinct from closeout explicit-path mode. |
| `VIC-IH-002` | Helper supplies the approved cache flags/context by default. |
| `VIC-IH-003` | Helper returns cache hit only when full cache identity matches. |
| `VIC-IH-004` | Helper falls back to actual run when cache is missing, malformed, stale, disabled, or unsupported. |
| `VIC-IH-005` | Helper emits visibly distinct cache-hit output. |
| `VIC-IH-006` | Helper records or references formal `cache-hit-inner-loop` evidence for workflow cache hits. |
| `VIC-IH-007` | Helper cache-hit evidence cannot satisfy closeout. |
| `VIC-IH-008` | Closeout direct lifecycle command still runs actual validation. |
| `VIC-IH-009` | Plans/test-spec guidance separates inner-loop and closeout command kinds. |
| `VIC-IH-010` | Selector, CI, validator-code, policy/spec, external-state, and npm validation changes are not cache-covered by this helper. |
| `VIC-IH-011` | Measurement records helper usage, cache hits, cache misses, actual-run fallbacks, and estimated time saved. |
| `VIC-IH-012` | Validator semantics, selected checks, exit codes, and failure detection remain unchanged. |

Suggested validation commands for the later implementation plan:

```bash
python scripts/test-validation-cache.py
python scripts/test-artifact-lifecycle-validator.py
python scripts/test-select-validation.py
python scripts/validate-artifact-lifecycle.py --mode explicit-paths-inner-loop \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/plans/<plan>.md \
  --path docs/plan.md
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --path docs/changes/<change-id>/change.yaml \
  --path docs/plans/<plan>.md \
  --path docs/plan.md
python scripts/validate-change-metadata.py docs/changes/<change-id>/change.yaml
git diff --check --
```

The actual explicit-path list should come from the active plan.

## Measurement Gate

Measurement should be recorded in:

```text
docs/changes/<change-id>/validation-cache-measurement.yaml
```

Minimum fields:

```yaml
schema_version: 1
change_id: <change-id>
measurement_window:
  start_stage: <stage>
  end_stage: <stage>
summary:
  helper_invocations: <integer>
  cache_hits: <integer>
  cache_misses: <integer>
  actual_run_fallbacks: <integer>
  closeout_actual_runs: <integer>
  estimated_seconds_saved: <number>
  eligibility_expansion_recommendation: <defer | propose-follow-up | reject-for-now>
```

Rules:

```text
- closeout_actual_runs remains nonzero for stages that close.
- cache hits are not counted as closeout actual runs.
- eligibility expansion recommendation defaults to defer unless evidence justifies follow-up.
```

## Behavior-Preservation Proof

The later implementation should create or update:

```text
docs/changes/<change-id>/behavior-preservation.md
```

Expected matrix:

| Surface | Baseline proof | New proof | Preservation result |
| --- | --- | --- | --- |
| Direct lifecycle actual run | `--mode explicit-paths` command | same command still runs actual validation | unchanged |
| Inner-loop helper cache miss | no helper | helper runs validator when cache is invalid or missing | safe fallback |
| Inner-loop helper cache hit | prior cache evidence | helper emits/records `cache-hit-inner-loop` | improved adoption |
| Closeout validation | actual-run closeout command | actual-run closeout command still required | unchanged |
| Failure detection | failing lifecycle fixture | helper miss and direct run detect same failure | unchanged |
| Cache evidence | existing formal evidence shape | helper writes/merges cache-hit evidence | preserved |
| Selector/CI routing | selected-CI proof | unchanged selected/CI commands | unchanged |
| Measurement | cache not used or manually used | helper usage/hit/miss counts recorded | improved observability |

## Rollout and Rollback

Rollout:

1. Review and accept this proposal.
2. Amend the validation-idempotency spec for the inner-loop helper or mode.
3. Amend the test spec for helper behavior, closeout rejection, evidence, and measurement.
4. Plan implementation with separable work for mode contract, cache-hit evidence integration, command guidance, and measurement.
5. Implement the helper without changing direct closeout command semantics.
6. Run code review for helper behavior and evidence boundary.
7. Measure helper usage before considering cache eligibility expansion.

Rollback:

- Remove or disable the `explicit-paths-inner-loop` mode.
- Keep direct `--mode explicit-paths` lifecycle validation as the default actual-run path.
- Leave validation-cache identity primitives intact if still valid.
- Preserve cache-hit evidence as historical inner-loop evidence if already recorded.
- Do not change closeout validation behavior during rollback.
- Do not delete actual-run closeout evidence.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Helper is mistaken for closeout validation. | Name it `inner-loop`; evidence kind is `cache-hit-inner-loop`; closeout validation rejects cache-only closeout. |
| Helper masks stale input. | Existing cache identity contract remains unchanged; cache miss runs validator. |
| Helper used after selector or validator code changes. | Implementation/policy hash invalidates cache; guidance says selector/CI changes need fresh actual-run proof. |
| Cache evidence becomes ambiguous. | Record cache-hit evidence separately and label it as inner-loop only. |
| Plans still teach direct commands only. | Update plan/test-spec validation tables to separate inner-loop and closeout command kinds. |
| Eligibility expansion happens too soon. | Use the measurement gate; expansion requires separate proposal/spec amendment. |
| Local cache causes false confidence. | Formal workflow cache hits need change-local evidence; untracked cache alone is not lifecycle evidence. |
| The helper adds too much complexity. | Keep the first slice to one command family and one command shape. |

## Open Questions

Resolved for this proposal:

- Helper shape: use a new lifecycle validator mode, `--mode explicit-paths-inner-loop`; do not add a separate wrapper script in the first slice.
- Guidance placement: the spec and test spec define the exact helper contract; repository-local RigorLoop plan and test-spec templates may show the two-command table.
- Published-skill boundary: published skills do not expose RigorLoop-internal cache commands, validator paths, selector mechanics, or repository maintenance details.
- Formal evidence: when a safe change root or evidence path is supplied or inferable, cache hits write or merge formal evidence to `docs/changes/<change-id>/validation-cache-evidence.yaml`.
- Outside change root: the helper is allowed for local ad hoc use, but it does not write formal evidence unless the change root or evidence path is explicit and safe.
- CI: CI does not use the helper in the first slice; CI remains actual-run.

Open for spec and plan:

- How should per-change measurement aggregate into a future expansion decision?
- Which selector routes should register the new evidence files?

## Decision Log

| Date | Decision | Reason | Alternatives rejected |
| --- | --- | --- | --- |
| 2026-05-24 | Propose a cache-aware inner-loop lifecycle helper. | The cache shipped but was missed because callers had to remember flags. | Documentation-only reminder. |
| 2026-05-24 | Keep closeout actual-run. | Cache is an inner-loop optimization, not completion proof. | Default cache for all lifecycle validation. |
| 2026-05-24 | Keep eligibility limited to explicit-path lifecycle validation. | Expanding validator families creates new stale-cache risk. | Cache metadata/review/CI/npm checks now. |
| 2026-05-24 | Update command templates. | Plans and test specs currently teach the old direct command habit. | Rely on agent memory. |
| 2026-05-24 | Measure before expansion. | One missed cache-use event justifies a helper proposal, not broad policy expansion. | Immediately broaden cache scope. |
| 2026-05-24 | Use `--mode explicit-paths-inner-loop` instead of a wrapper script. | Keeps the first slice under the existing lifecycle validator owner while making the inner-loop boundary explicit in the mode name. | Separate wrapper script in the first slice. |
| 2026-05-24 | Keep published skills free of internal cache command details. | Published skills are user-facing and should not expose RigorLoop repository maintenance mechanics. | Put repository-local validator command tables in published skills. |
| 2026-05-24 | Allow local ad hoc helper use without formal evidence writes. | Formal workflow evidence needs a safe change root or explicit evidence path; ad hoc use may still benefit from status output. | Forbid helper outside a change root. |
| 2026-05-24 | Exclude CI from helper use in the first slice. | CI remains actual-run proof until a later spec defines CI cache policy. | Let CI use the inner-loop helper now. |

## Next Artifacts

Planned route:

```text
proposal-review
spec amendment: validation idempotency cache-aware inner-loop helper
spec-review
test-spec amendment
plan
plan-review
implementation
code-review
explain-change
verify
pr
```

Potential follow-up proposals after measurement:

- Cache eligibility expansion after helper measurement.
- Diff-derived edit-scoped validation, only if measurement still justifies it.
- CI cache policy, if actual CI runtime becomes a bottleneck.
- Visualization of cache-hit evidence in the change-record query helper.
- Shared validation command templates if several stages need the same two-command table.

## Follow-on Artifacts

- Proposal review: `docs/changes/2026-05-24-cache-aware-inner-loop-lifecycle-validation-helper/reviews/proposal-review-r1.md`
- Spec amendment: `specs/validation-idempotency-and-cache-hit-safety.md`

## Readiness

Accepted; downstream spec amendment is recorded in Follow-on Artifacts.

## Core Invariant

```text
Make the safe cached path easy, not broader.

The helper exists so callers do not have to remember cache flags for repeated
inner-loop lifecycle validation. It does not turn cache hits into closeout
proof, expand cache eligibility, or weaken actual-run validation at stage,
verify, branch, or PR boundaries.
```
