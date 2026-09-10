# Plan index

`docs/plan.md` is a navigation index to stable plan bodies and owning change records.
Mutable lifecycle state, current milestones, review state, blockers, and next stages live in each plan's owning change record (`change.json` for current v2 work).

<!--
Index policy:
- Current plan references link stable plan bodies to owning change records.
- Recent history keeps the most recent 10 completed plan references.
- Older Done entries move to docs/plan-archive.md.
- Plan links use relative Markdown targets from this file, for example `[Title](plans/YYYY-MM-DD-slug.md)`.
- Do not use bare repository-root plan paths in this index; they may not render as clickable links.
- Do not copy mutable lifecycle or routing state into this index.
-->

## Active

Compatibility heading only.
Current lifecycle state is not recorded in this index.

## Blocked

Compatibility heading only.
Current blockers are not recorded in this index.

## Current plan references

- [2026-09-10 Distribution and Explicit Force Installation](plans/2026-09-10-distribution-model-and-opencode-retirement.md) — [owning change](changes/2026-09-10-distribution-model-and-opencode-retirement/change.json).

- [2026-09-10 Readable record output](plans/2026-09-10-readable-record-output.md) — [owning change](changes/2026-09-10-readable-record-output/change.json).

- [2026-09-10 Simplify release validation integration](plans/2026-09-10-release-validation-integration.md) — [owning change](changes/2026-09-10-release-validation-integration/change.json).

- [2026-09-09 Approval-Driven Release and Source Consolidation](plans/2026-09-09-release-model-source-consolidation.md) — [owning change](changes/2026-09-09-release-model-source-consolidation/change.json)

- [2026-09-09 Necessary Design Consolidation](plans/2026-09-09-necessary-design-consolidation.md) — [owning change](changes/2026-09-09-simplify-required-validation-and-design-retention/change.json)

- [2026-09-08 Skill Model and Proposal-Family Pilot](plans/2026-09-08-skill-model-proposal-family-pilot.md) — [owning change](changes/2026-09-08-skill-model-proposal-family-pilot/change.json)

- [2026-09-08 Unified Design Authoring and Bounded Model Consolidation](plans/2026-09-08-unified-design-authoring-and-bounded-model-consolidation.md) — [owning change](changes/2026-09-08-unified-design-authoring-and-bounded-model-consolidation/change.json)

- [2026-09-08 V2-only Recording and Legacy Engine Retirement](plans/2026-09-08-retire-legacy-record-formats.md) — [owning change](changes/2026-09-08-retire-compact-workflow-mutations/change.json)

- [2026-09-08 Design-Derived Test Model](plans/2026-09-08-design-derived-test-model.md) — [owning change](changes/2026-09-08-design-derived-test-model/change.json)

- [2026-09-08 Unify Review and Closeout Policy Ownership](plans/2026-09-08-unify-review-closeout-policy.md) — [owning change](changes/2026-09-07-unify-review-closeout-policy/change.json)

- [2026-09-07 Targeted Recording and Record Format v2](plans/2026-09-07-targeted-recording-primary-cli.md) — [owning change](changes/2026-09-07-targeted-recording-primary-cli/change.yaml)
- [2026-09-05 Explicit Recording and Model-Centered Design](plans/2026-09-05-explicit-recording-and-model-centered-design.md)
- [2026-09-03 Compact Current-State Change Record](plans/2026-09-03-compact-current-state-change-record.md)
- [2026-09-03 Relax PR Evidence Tail Topology](plans/2026-09-03-relax-pr-evidence-tail.md)
- [2026-09-03 Refine Explore and Research as Optional Discovery Skills](plans/2026-09-03-refine-explore-research-optional-discovery-skills.md)
- [2026-09-02 Refocus Workflow into Route](plans/2026-09-02-refocus-workflow-into-route.md)
- [2026-08-30 Lightweight Requirement-to-Delivery Model](plans/2026-08-30-lightweight-requirement-delivery-model.md)
- [2026-08-31 Retire the Standalone Test-Spec Stage](plans/2026-08-31-retire-standalone-test-spec-stage.md)
- [2026-08-31 Simplify Final Verification and Retire Explain Change](plans/2026-08-31-simplify-final-verification-retire-explain-change.md)

## Done (recent)

Full completed history: see [Plan archive](plan-archive.md).

- [2026-08-30 Simplified RigorLoop Proposal Contract](plans/2026-08-30-simplify-rigorloop-proposal-contract.md)
- [2026-08-29 Consolidated RigorLoop Review Gates](plans/2026-08-29-consolidate-rigorloop-review-gates.md)
- [2026-08-25 CLI Observability and Token-Efficient Results](plans/2026-08-25-cli-observability-token-efficient-results.md)
- [2026-08-25 Workflow-Routed Upstream Corrections](plans/2026-08-25-workflow-routed-upstream-corrections.md)
- [2026-08-24 Governed Lifecycle CLI](plans/2026-08-24-governed-lifecycle-cli.md)
- [2026-08-20 Bugfix Skill Simplification](plans/2026-08-20-bugfix-skill-simplification.md)
- [2026-08-19 CI-Maintenance Skill Simplification](plans/2026-08-19-ci-maintenance-skill-simplification.md)
- [2026-08-18 Explain-Change Skill Simplification](plans/2026-08-18-explain-change-skill-simplification.md)
- [2026-08-17 Vision Skill Progressive Disclosure](plans/2026-08-17-vision-skill-progressive-disclosure.md)
- [2026-08-17 Learn Skill Simplification](plans/2026-08-17-learn-skill-simplification.md)

## Historical replacements

- [Activate Boundary-First v1 in v0.4.0](plans/2026-08-05-activate-boundary-first-v1-v0-4-0.md) is the cancelled custom candidate/atomic-publication plan superseded by [Usability-First Boundary-First v0.4.0 Release](plans/2026-08-06-usability-first-boundary-release.md).
