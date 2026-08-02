# PR-readiness lifecycle ownership correction

## Reproduction

After the selector registration fix and synchronization with `origin/main`,
PR-mode validation reached `artifact_lifecycle.validate` and blocked on:

- two normalized change-record entries for
  `docs/architecture/system/architecture.md`; and
- the accepted stage-owned proposal
  `docs/proposals/2026-07-28-approved-specification-baselines-and-controlled-amendment-workflow.md`
  retaining embedded status without its existing owning change-record pointer.

## Root cause

The progressive-guidance architecture edit changed the canonical
architecture's owner pointer and registered a second artifact-state entry in
the new change record. The established stage-owned change record already owns
that shared canonical artifact, so the new registration violated the exact
single-owner contract.

The earlier stage-owned proposal already has an accepted artifact-state entry
in that established record, but its Markdown predated the pointer migration
and still embedded `Status`. Because this branch changes the governing
stage-owned lifecycle contract, PR validation correctly treats that referenced
artifact as authoritative rather than unrelated baseline debt.

## Correction

- Restore the canonical architecture's stable pointer to its established
  owning change record.
- Remove the duplicate architecture artifact-state entry from the progressive
  guidance change record. The architecture remains a referenced artifact and
  the current architecture review remains durable change evidence.
- Replace the prior proposal's embedded status section with a stable pointer
  to the change record that already owns its accepted state.

No architecture decision, proposal intent, lifecycle vocabulary, or validator
behavior changes in this correction.
