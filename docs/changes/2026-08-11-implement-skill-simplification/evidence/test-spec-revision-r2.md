# Test-Spec Revision R2 Evidence

Stage: test-spec
Date: 2026-08-11
Status: revision complete; review required

## Trigger

M3 executed approved CMD7 exactly. Adapter archive generation succeeded, but all three clean-install targets stopped before mutation with `metadata-trust-root-unavailable` because synthetic version `0.0.0-implement-simplification` is absent from the bundled release-metadata trust root.

## Correction

CMD7 now uses immutable trusted fixture identity `v0.3.6`, matching existing adapter clean-install regression tests and the approved precedent for the code-review skill simplification. Python owns a temporary directory and removes it on success or failure. The selected skill remains `implement`; target coverage, failure behavior, filesystem-only proof, and target-runtime exclusion are unchanged.

The rejected synthetic command is retained in M3 evidence as expected fail-closed trust-boundary proof. This authoring record changes only the test fixture identity and cleanup mechanism; M3 owns the corrected execution result.

## Scope

No requirement, example, test ID, proof classification, milestone mapping, manual proof, validator, or product behavior changed. The command continues to prove archive and clean-install mapped-resource parity for Codex, Claude, and opencode without publication, network access, or target-agent execution.
