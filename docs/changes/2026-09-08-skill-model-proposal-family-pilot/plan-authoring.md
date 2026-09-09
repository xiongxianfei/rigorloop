# Plan authoring evidence

Owning change: [change.json](change.json).

Operation: `create-primary-plan`. The user authorized the next stage after independent Design approval. The plan is [Skill Model and Proposal-Family Pilot](../../plans/2026-09-08-skill-model-proposal-family-pilot.md); its exact authored identity is `sha256:afe231f1bcd0a5a2afd189867f42e237916bdba8e670cdd53cfec26d431d0b39`.

## Basis and allocation

The current v2 context had complete selected activity/model/proposal/review/finding/blocker/applicability scope. Independent Design Review round 2 approves the refined Skill package; the original reviewer resolved `skl-dr-001`. No implementation work entries or existing primary plan were present. Exact source inspection confirmed the approved Skill, System and proposal identities remained unchanged. CLI workflow-context supplies the deterministic plan path `docs/plans/<change-id>.md`.

Two implementation milestones couple pilot relocation with enforcing consumers, then transfer common source authority after independently assessed pilot value. Five local proof groups and one integrated group cover SKL-SR-01–23, the exact retained-contract populations and Design's combined hazards. The plan uses the canonical plan/milestone/decision-row structures. It retains three historical originals at source paths and snapshots four originals, as permitted by Design. No downstream work is initialized before Delivery approval.

Source consumers and command entrypoints were inspected directly, including skill validation, adapter archive comparison, current-owner guide validation, generation and the CI wrapper. The actual mixed architecture path is `docs/architecture/system/architecture.md`. Plan authoring does not rely on the project map for prospective Skill ownership; the plan records this bounded no-map rationale and allocates necessary current-reference correction.

## Checks actually run

- `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-08-skill-model-proposal-family-pilot.md`: passed with zero errors or warnings after removing scaffold-maintainer metadata comments from the generated artifact. The comments initially triggered split-prose diagnostics; no validator was changed.
- `python scripts/validate-markdown-readability.py docs/plans/2026-09-08-skill-model-proposal-family-pilot.md`: passed with 53 advisory warnings.
- Python local-link existence check: all 14 plan links resolve. An additional path assertion exposed and corrected the initial mixed-architecture filename before recording; the final path exists.
- `git diff --check`: passed for tracked changes. Explicit plan prose/readability checks cover the new untracked plan.
- CLI primary context, workflow-context and full exact-subject inspection: completed for authoring authority and identities.

These are authoring and structural observations, not Delivery Review or implementation evidence. Implementation suites and candidate generation are allocated in the plan and were not run during authoring. Earlier Design/proposal judgments remain unchanged; the new plan requires its own independent Delivery Review. The plan and navigation were the only engineering surfaces authored in this stage.
