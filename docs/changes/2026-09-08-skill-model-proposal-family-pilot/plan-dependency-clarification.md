# Plan dependency and traceability clarification

Owning change: [change.json](change.json).

Operation: `revise-primary-plan`, explicitly requested by the user. The [plan](../../plans/2026-09-08-skill-model-proposal-family-pilot.md) now allocates inspection of current-candidate metadata and dependent assertions in M1, TG-03 and the Validation plan. Affected metadata must be regenerated through its existing owning builder and directly dependent checks run before milestone closure, or an inspected unaffected disposition recorded. This is a dependency allocation, not evidence that stale metadata exists. Historical releases, manually invented hashes, publication and additional release gates remain excluded.

The requirement allocation and TG-FINAL-01 now explicitly include SYS-SR-02/04/06/07 only for the reviewed Skill-owner/pilot interaction. These map to existing milestones and proof groups; no additional System responsibility or implementation milestone is selected.

Prior plan: `sha256:afe231f1bcd0a5a2afd189867f42e237916bdba8e670cdd53cfec26d431d0b39`.

Revised plan: `sha256:5f1f00d9e756e084670fb0acf094f7f45a25a850fbc1de88f9ea4fd0cd9260c4`.

Skill and System remain unchanged. Delivery Review round 1 retains its original judgment and subjects; its applicability is restricted because it assessed the earlier plan. Independent Delivery reassessment owns renewal. The earlier plan-authoring note remains an exact-subject snapshot; its results do not validate this revision.

## Checks actually run

- `python scripts/validate-documentation-prose.py --mode enforce --path docs/plans/2026-09-08-skill-model-proposal-family-pilot.md`: passed, zero errors/warnings.
- `python scripts/validate-markdown-readability.py docs/plans/2026-09-08-skill-model-proposal-family-pilot.md`: passed, 54 advisory warnings.
- Python local-link existence check: all 14 links passed.
- `git diff --check`: passed for tracked changes; explicit document checks cover the untracked plan.
- Current CLI context and full subject inspection: completed before and after revision.

No candidate generation, metadata regeneration or implementation checks were executed during this plan correction. No work entries were initialized or changed. The revision requires independent Delivery reassessment before implementation reliance.
