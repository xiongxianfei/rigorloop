# Remove the project-map skill

## Purpose and scope

The user selected removal of the dedicated project-map skill and required map maintenance. Ordinary work inspects relevant source directly; existing README and architecture overview provide navigation. Preserve useful implementation entry points without a replacement map, generator, skill or approval stage. This is separate from merged PR213, based on `3f2c0b86787068086fa2593b4ec9ed9e1a7bd519`.

## Owning Change

`2026-10-18-remove-project-map` owns mutable progress and evidence. The user authorized this separate small PR; commit/push/PR follow final review and Verify, without merge or release authority.

## Design and implementation

Remove the authored skill and exclusive resources, supporting contract, registry/inventory entries and map-only validator logic. Delete docs/project-map.md after transferring useful current entry points into README/architecture overview. Replace required read/refresh steps with direct source inspection. Preserve observation-versus-inference and authority boundaries under Project Foundations; explicitly retire dedicated map operations/registration requirements. Keep customer documents and installed external skills untouched.

Reconcile current links, realization metadata and generated products. Historical references may resolve to their exact pre-removal Git revision; they do not require retaining obsolete artifacts. Do not broaden historical cleanup.

## Verification allocation

Run the existing skill tests, including the actual missing-resource counterexample, guide/model/prose checks and archive/packed-CLI tests. Confirm the remaining 18 skills package correctly, map absence does not block guide validation and missing required guide links still reject. Retained runtime/CI sources do not change. Generate/check adapter metadata and architecture views. Assess navigation, consumer closure and preserved boundaries in one independent whole-change review, then perform distinct final Verify.

## Recovery and handoff

Restore removed paths from the base commit and revert consumers together if needed. Preserve user work and original review meanings. Submit the complete reviewed change as a separate PR and report actual hosted-check status.
