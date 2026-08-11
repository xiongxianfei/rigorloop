# Proposal Revision R2 Evidence: Workflow Skill Simplification

## Scope

This revision resolves `WFSIM-PR3`, `WFSIM-PR4`, and `WFSIM-PR5` from `proposal-review-r2` without changing the selected compact-dispatcher package direction.

## Finding dispositions

### WFSIM-PR3

- Added `automation_command_context` as distinct from durable `armed_automation_context`.
- Added transient `WPB-automation-bootstrap` with a closed establish, validate, reclassify, then persist sequence.
- Closed the assembly lattice for generic, governed, automated, guide-authoring, governed-guide, and bootstrap contexts.
- Made active automation and guide authoring mutually exclusive within one first-version invocation.

### WFSIM-PR4

- Kept source rank, evidence precedence, and unknown-artifact or unknown-stage behavior inline.
- Assigned lifecycle and architecture applicability, transitions, settlement, milestones, final review, and closeout exclusively to the governed reference.
- Limited the automation reference to automation commands, identity, receipts, budgets, correction cycles, and promotion conditions that consume governed transition decisions.
- Limited the guide reference to guide creation, refresh, skeleton use, customization recording, and migration procedure.
- Added a strict dependency direction and a stop-on-contradiction package rule.

### WFSIM-PR5

- Added a resource-availability gate after classification and before conditional interpretation or action.
- Defined fail-safe behavior for missing, unreadable, contradictory, or mixed-version governed, automation, guide, and skeleton resources.
- Prohibited remembered, invented, or partial reconstruction of missing conditional procedure.
- Kept runtime hashing and a new integrity service out of scope; existing package parity remains the deterministic prevention mechanism.

## Preservation statement

The revision changes proposal-level ownership and loading contracts only. It does not change lifecycle order, persistent state, `change.yaml` schema, automation authorization semantics, stage ownership, review outcomes, or downstream authority.

## Rereview target

Independent `proposal-review-r3` should verify the complete revised proposal, especially the bootstrap matrix, non-overlapping ownership table, resource-failure boundary, static scenario coverage, and architecture scope.
