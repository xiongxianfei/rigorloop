# Learn Session: Resource Integrity Review Finding Pattern

## Status

Recorded: 2026-06-23

Session state: recorded

## Frame

Trigger:

The maintainer asked why the published-skill resource-integrity change produced
many review findings, whether the proposal or spec was unclear, and what the
root reason was.

Scope:

This session covers review findings and follow-up fixes for:

- `docs/changes/2026-06-22-published-skill-resource-integrity-architecture-pilot/`
- PR #101, published skill resource integrity
- the M2 legacy-resource lint reviews;
- the M4 recorded-source release-validation reviews;
- the M5 clean-install proof review;
- the final PR-mode selector failure for newly introduced evidence files.

Out of scope:

- changing the accepted proposal, spec, architecture, or plan;
- reopening milestone implementation;
- changing validator policy, release policy, workflow policy, or skill guidance
  from this learn session alone.

## Observe

### O1 - The proposal and spec were not the main source of the review volume

Evidence:

The proposal and downstream artifacts established the central invariant:
published skills must not reference unavailable skill-local resources, and
canonical, generated, archived, and installed resources must agree. The later
findings mostly targeted whether the implementation preserved that invariant at
the correct decision boundary.

Observation:

The proposal/spec direction was materially sound. Some details needed
refinement during review, but the later repeated findings were not primarily
caused by unclear product intent. They came from implementation and proof
models that were too narrow for the stated invariant.

### O2 - M2 fixed examples before fully modeling the classifier pipeline

Evidence:

`SRI-M2-CR1` found that broad project-local suppressor terms could hide real
legacy resource-loading instructions. `SRI-M2-CR2` then found whole-line
external ownership suppression. `SRI-M2-CR3` then found instruction intent
leaking across independent Markdown list items.

Observation:

The M2 validator was patched one visible failure at a time. Each fix was
reasonable in isolation, but the implementation did not first define the full
classifier pipeline:

```text
Markdown instruction segment
-> loading intent
-> resource path match
-> per-path ownership or illustrative context
-> exact migration exception
-> diagnostic
```

That let the next review find the adjacent boundary after the previous one was
fixed.

### O3 - M4 treated a compatibility exception as a validation bypass

Evidence:

`SRI-M4-CR1` found that recorded-source validation had been narrowed to adapter
artifact metadata and bypassed release metadata, notes, required evidence,
security, token-cost, and publication checks. `SRI-M4-CR2` then found that
recorded-source archive validation could pass with `adapter_archive_errors = []`
without inspecting rebuilt archive contents.

Observation:

The right compatibility rule was narrow: skip only current canonical
skill-content policy that cannot apply retroactively to historical source. The
implementation initially widened that into a release-validation shortcut. That
created both under-validation and vacuous pass risk.

### O4 - M5 had strong smoke coverage but missed one named installed-state proof

Evidence:

`SRI-M5-CR1` found that M5 proved successful install, no-op installer rejection,
stale installed resource bytes, and packed-root enforcement, but did not
directly prove the distinct state where the installed skill root and `SKILL.md`
exist while one mapped resource is missing.

Observation:

The production behavior was close, but the proof did not cover every
acceptance-critical state. Inferring coverage from related cases was not enough
for a named clean-install invariant.

### O5 - The final workflow failure came from not running the hosted-equivalent selector path

Evidence:

The PR workflow failed after branch verification because PR-mode validation
selected newly introduced evidence files that explicit local validation did not
route. The fix registered `clean-install-proof.md` and `validator-fixtures.md`
with `scripts/validation_selection.py` and added selector tests.

Observation:

The local validation was substantial, but it did not exactly reproduce the
hosted PR-mode selection path. For changes that introduce new lifecycle evidence
file types, explicit-path validation is not enough; the selector must know those
files before PR readiness is claimed.

## Root Cause

The root reason was not mainly an unclear proposal or spec.

The root reason was that implementation repeatedly translated broad invariants
into checks at the wrong or incomplete operational boundary:

- resource linting checked lines and contiguous blocks before it fully modeled
  instruction segments and per-reference ownership;
- recorded-source release validation skipped whole validation surfaces instead
  of separating current-only policy from still-applicable release and archive
  integrity;
- clean-install proof relied on nearby cases before directly testing the named
  missing-resource installed state;
- final verification ran many explicit checks but missed the hosted PR-mode
  selector path for new evidence files.

In short:

```text
The contract was directionally clear.
The implementation proof was often example-driven instead of boundary-driven.
```

The reviews were catching real boundary mismatches. They were not primarily
process noise.

## Best Practices

1. Convert each invariant into a boundary model before editing.
   For validators, name the decision unit. For release profiles, name each
   validation layer. For install smoke, name each installed state.

2. Build a boundary matrix before returning to review.
   Include same-line, wrapped, separate-list-item, separate-paragraph, fenced,
   Resource map, exception, missing, stale, and no-check cases when those
   boundaries are relevant.

3. Treat compatibility exceptions as profiles, not bypasses.
   A historical profile may mark a current-only policy not applicable, but
   release evidence and archive integrity should still run unless the contract
   explicitly says otherwise.

4. Prove non-vacuous validation.
   A passing result should show that required checks executed. Empty error lists
   are not proof by themselves.

5. Match final verification to the hosted path.
   Before PR handoff, run the same PR-mode selector behavior that hosted CI will
   use, especially when new artifact classes or evidence filenames are added.

6. After a review finding, search for the neighboring false positive and false
   negative.
   The useful question is not only "does the named case pass now?" but "what
   context did this fix broaden or narrow?"

7. Keep the review standard high.
   The improvement target is better boundary modeling and pre-review sweeps, not
   weaker reviews.

## Classify

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | observation | observation | None | Review log and accepted resolutions | Explains that the proposal/spec were not the main cause. |
| O2 | durable-lesson | pending confirmation | Possible validator/test-spec guidance | Not yet confirmed | The classifier-boundary pattern recurred across three M2 reviews. |
| O3 | durable-lesson | pending confirmation | Possible release-validation profile guidance | Not yet confirmed | The compatibility-exception pattern recurred across two M4 reviews. |
| O4 | process-follow-up | pending confirmation | Possible clean-install proof checklist | Not yet confirmed | The missing installed-state proof is concrete but may remain local to this change. |
| O5 | process-follow-up | pending confirmation | Possible CI selector routing guidance | Not yet confirmed | The hosted-path validation gap is reusable, but routing needs confirmation. |

Contributor confirmation status:

The maintainer explicitly requested this retrospective. That confirms recording
the learn session. It does not by itself confirm updates to topic files, specs,
workflow policy, skills, validator guidance, or release guidance.

## Route

No topic, spec, workflow, skill, or validator guidance updates were made from
this session.

Potential future routes, if explicitly confirmed:

- validator boundary-matrix guidance for classifier-style checks;
- release-validation profile guidance for historical compatibility exceptions;
- CI selector guidance for new lifecycle evidence file classes.

## Answer

There were many review findings because this change touched validators, release
profiles, archive parity, clean installation, generated artifacts, and lifecycle
evidence at the same time. Those surfaces are tightly connected, and a small
boundary mistake in one layer can invalidate the proof for the whole invariant.

The proposal/spec were not the primary problem. They stated the right invariant.
The weak point was converting that invariant into deterministic checks and tests
that exercised all neighboring boundaries before review.

## Follow-ups

None created by this session.
