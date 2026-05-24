# Learn Session: Adoption Surface Cache Nonuse

## Frame

- Date: 2026-05-24
- Status: session-recorded; routing pending contributor confirmation
- Trigger: maintainer explicitly invoked `learn` to ask why the public discovery and developer adoption surface session did not use validation cache, the root cause, and best practices for optimization.
- Trigger type: explicit maintainer request after merged workflow-managed change.
- Scope: cache nonuse during `2026-05-23-public-discovery-and-developer-adoption-surface`, especially lifecycle validation, selected validation, and PR-mode CI evidence.
- Session path: `docs/learn/sessions/2026-05-24-adoption-surface-cache-nonuse.md`

## Evidence Reviewed

- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/change.yaml`
  - Records many `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...` runs.
  - Records PR-mode `python scripts/select-validation.py --mode pr --base main --head HEAD`.
  - Records PR-mode `bash scripts/ci.sh --mode pr --base main --head HEAD`.
  - Does not record `--use-validation-cache`, `validation-cache-evidence.yaml`, or `cache-hit-inner-loop`.
- `docs/changes/2026-05-23-public-discovery-and-developer-adoption-surface/verify-report.md`
  - Records direct local verify commands, an initial selector blocker, CI-maintenance registration, and selected CI rerun.
  - Does not claim cache-hit evidence.
- `docs/plans/2026-05-23-public-discovery-and-developer-adoption-surface.md`
  - Validation commands are written as direct validator invocations without cache flags.
- `specs/validation-idempotency-and-cache-hit-safety.md`
  - First-slice cache eligibility applies only to `python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...`.
  - Validators outside that command family must run normally.
  - Cache-only closeout is invalid; closeout requires actual-run evidence.
- `docs/adr/ADR-20260523-validation-idempotency-cache-hit-safety.md`
  - Local execution cache is untracked, branch-local, worktree-local, and change-local.
  - It may speed repeated local commands but is not lifecycle evidence and is not portable.
  - Formal cache-hit evidence is separate tracked evidence and cannot satisfy closeout in the first slice.
- `scripts/validate-artifact-lifecycle.py`
  - Cache behavior is opt-in via `--use-validation-cache` plus related cache context/evidence flags.

## Exclusions

- This session does not change cache behavior, selected CI behavior, lifecycle validation, workflow policy, specs, ADRs, or skills.
- This session does not retroactively change the adoption-surface validation evidence.
- This session does not claim that cache should replace closeout actual-run validation.
- This session does not create a topic entry because the observation is not yet contributor-confirmed as durable guidance.

## Prior Learnings Reviewed

- `docs/learn/topics/ci-selector-routing.md` covers a different issue: new change-local evidence classes need deterministic selector routes.
- `docs/learn/sessions/2026-05-22-change-local-selector-routing.md` explains the selector-routing blocker that occurred again during this adoption-surface verify session.
- `docs/learn/sessions/2026-05-23-workstream-slice-model.md` covers planning workstreams and does not define validation cache adoption.
- No existing learn topic was found for validation-cache adoption practice.

## Observations

### O1: Cache was not used because every recorded lifecycle validation command was run without cache flags

The adoption-surface evidence contains repeated `validate-artifact-lifecycle.py
--mode explicit-paths` commands, which are the one command family that the
approved first cache slice can optimize. However, the recorded commands do not
include `--use-validation-cache`, `--validation-cache-dir`,
`--validation-cache-current-stage`, or `--validation-cache-current-evidence`.

The validator therefore ran normally. This is not a cache miss caused by a bad
cache key; it is cache nonuse caused by the cache not being invoked.

### O2: The root cause is an adoption gap between the cache contract and stage guidance

The cache implementation is deliberately conservative and opt-in. The
adoption-surface plan and verify flow used the older direct-command pattern,
and the stage guidance did not prompt the agent to use cache for repeated
inner-loop lifecycle validation.

Root cause:

```text
The cache exists as an opt-in validator feature, but the plan/test/verify
command templates and agent habit path still call explicit lifecycle validation
without cache flags.
```

### O3: Closeout and PR-mode selected CI still needed actual runs

Even if cache had been used during inner-loop validation, the approved cache
contract says first-slice closeout cannot be satisfied by
`cache-hit-inner-loop`. The adoption-surface verify and PR-mode selected CI were
closeout/readiness checks, so actual runs were still appropriate there.

This means the missed optimization opportunity was mostly earlier repeated
milestone and evidence-sync validations, not final closeout or hosted CI.

### O4: The session also had cache-invalidating edits during verify

During verify, CI-maintenance changed `scripts/validation_selection.py` and
`scripts/test-select-validation.py`. Those are selector files, not lifecycle
validator implementation files, but the changed branch state still required
fresh PR-mode selected validation. The cache contract is not a substitute for
rerunning selector and CI paths after validation routing changes.

### O5: Best optimization target is repeated inner-loop explicit lifecycle validation

The adoption-surface session repeatedly ran long explicit-path lifecycle checks
after small artifact-state or evidence updates. Those are the likely cache
benefit zone:

- after plan or change-metadata wording syncs;
- after review-log or review-resolution updates;
- after evidence files are unchanged and only unrelated notes changed;
- before final closeout, as supporting inner-loop confidence.

Final closeout should still record actual-run evidence.

## Best Practices

### 1. Use cache only for the approved command family

For now, only consider cache for:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths ...
```

Do not attempt to cache `npm test`, `validate-change-metadata.py`,
`validate-review-artifacts.py`, selected CI, GitHub metadata checks, or
external-state proof unless a later spec expands cache eligibility.

### 2. Add cache flags to repeated inner-loop lifecycle checks

For repeated local checks before closeout, use the cache explicitly:

```bash
python scripts/validate-artifact-lifecycle.py --mode explicit-paths \
  --use-validation-cache \
  --validation-cache-change-id <change-id> \
  --validation-cache-current-stage <stage-or-milestone> \
  --validation-cache-current-evidence docs/changes/<change-id>/change.yaml#validation \
  --path ...
```

If the command, inputs, implementation, or policy changed, the validator will
run instead of reusing a prior pass.

### 3. Keep closeout actual-run evidence

Do not use cache hits as final milestone, verify, or PR-readiness closeout
evidence in the first slice. The safe pattern is:

```text
inner loop: cache may save repeated lifecycle checks
closeout: actual lifecycle validation run
```

### 4. Teach plans to distinguish inner-loop validation from closeout validation

Plans and test specs should separate:

- fast repeated checks that may use cache;
- final closeout checks that must run directly.

This avoids either extreme: never using cache, or incorrectly using cache as
closeout proof.

### 5. Make cache usage visible in evidence

When cache is used, record the cache mode clearly:

- command includes `--use-validation-cache`;
- inner-loop evidence uses `cache-hit-inner-loop` only when formal cache-hit
  evidence is recorded;
- closeout evidence remains `actual-run-pass`.

### 6. Prefer wrapper support over manual flag memory

The strongest optimization would be a small wrapper or documented command
template that adds safe cache flags for inner-loop lifecycle validation. Relying
on each agent to remember the full cache flag set is brittle.

Candidate follow-up:

```text
Proposal: add cache-aware inner-loop lifecycle validation helpers or plan/test
templates, while preserving direct actual-run closeout commands.
```

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | Session record | Recorded command evidence | The commands did not include cache flags, so cache was not invoked. |
| O2 | process-follow-up | candidate process-follow-up | Possible proposal for cache-aware command templates or helper wrapper | Confirmation pending | This identifies a workflow/tooling adoption gap, but learn does not own command-template policy. |
| O3 | observation | observation | Session record | Approved cache spec and ADR | Closeout actual-run behavior is intentional, not a defect. |
| O4 | observation | observation | Session record | Verify and CI-maintenance evidence | Selector/CI changes needed fresh selected validation regardless of lifecycle cache. |
| O5 | direction | candidate direction | Possible proposal or workflow/test-spec update | Confirmation pending | Best practices are actionable, but making them standard needs an owning artifact. |

Contributor confirmation status: pending for authoritative routing. The
maintainer asked for root cause and best practices, but has not yet confirmed a
proposal, workflow update, skill update, or helper implementation.

## Routing Results

- Session record: created.
- Topic update: not performed.
- Authoritative artifact update: not performed.
- Follow-up created: none.
- Candidate follow-up: create a proposal for cache-aware inner-loop lifecycle
  validation command templates or helper wrapper, preserving actual-run
  closeout validation.

## No-Durable-Lesson Rationale

This session has a clear root cause and useful best practices, but it is a
single observed cache-adoption miss after the validation cache feature was
introduced. The evidence supports a session-recorded observation and candidate
process follow-up. It does not yet justify a durable topic entry or workflow
policy change without contributor confirmation and an owning artifact.
