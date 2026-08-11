# Spec Revision Evidence R2

Stage: spec
Date: 2026-08-10
Trigger: downstream boundary-proof validation during test-spec authoring

The example-ownership rows previously used the union of every cited boundary's requirements. `boundary-first-v1` requires an example's requirement set to be governed by every cited boundary, so the correct serialization is the intersection for multi-boundary examples or one narrower owning boundary.

E1-E7 now cite only requirement IDs and boundary IDs that directly own their existing illustrative outcomes. No example prose, normative requirement, boundary definition, interaction, acceptance criterion, compatibility rule, or observable behavior changed.

Ready for spec-review R2 before the test spec updates its input identity.
