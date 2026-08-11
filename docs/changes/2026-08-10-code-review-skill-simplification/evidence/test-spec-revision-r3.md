# Test-Spec Revision R3 Evidence

Stage: test-spec
Date: 2026-08-10
Status: revision complete; review required

## Trigger

M3 executed approved CMD6 exactly. Adapter archive generation succeeded, but
all three clean-install targets stopped before mutation with
`metadata-trust-root-unavailable` because synthetic version
`0.0.0-code-review-simplification` is absent from the bundled release metadata
trust root.

## Correction

CMD6 now uses immutable trusted fixture identity `v0.3.6`, matching existing
adapter clean-install regression tests. No command structure, selected skill,
target coverage, failure behavior, cleanup, or side-effect boundary changed.

The corrected command was reproduced during M3 diagnosis and passed archive
generation plus clean-install mapped-resource validation for Codex, Claude, and
opencode with `--skill code-review`. This execution evidence remains owned by
M3; this authoring record establishes only why the proof command changed.

## Scope

No requirement, example, test ID, proof classification, milestone mapping,
manual proof, or product behavior changed. The revision removes an invalid test
fixture identity and retains deterministic filesystem-only proof with no target
agent runtime.
