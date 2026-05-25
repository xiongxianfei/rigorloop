# Behavior Preservation

| Surface | Baseline | New proof | Preservation result |
| --- | --- | --- | --- |
| Runtime CLI behavior | no CLI source files touched by scoped M1 commits | scoped commit proof | unchanged by this M1 slice |
| Skill behavior | no `skills/` files touched by scoped M1 commits | scoped commit proof | unchanged by this M1 slice |
| Adapter output | no `dist/adapters/` files touched by scoped M1 commits | scoped commit proof | unchanged by this M1 slice |
| Validators | no `scripts/` files touched by scoped M1 commits | scoped commit proof | unchanged by this M1 slice |
| Release process | no release artifacts touched by scoped M1 commits | scoped commit proof | unchanged by this M1 slice |
| Vision source of truth | `VISION.md` owns durable project vision; README marker block derives from it | `vision-readme-sync-proof.md` | strengthened |
| README positioning | mechanism-heavy first-screen framing | benefit-first hook, diagram, worked example, and principles | improved |
| Traceability explanation | visible but less central | diagram plus worked example chain | improved |
| Learn stage framing | internal self-improvement wording risk | durable lessons and reliability framing | improved |

## Diff boundary

This slice intentionally changes documentation and lifecycle evidence only in
its scoped M1 commits:

- `VISION.md`
- `README.md`
- `docs/proposals/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`
- `docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`
- `docs/plan.md`
- `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/`

No runtime, CLI, skill, adapter, validator, release, npm package, or generated
artifact behavior is changed by the scoped M1 commits.

## Branch stacking boundary

Maintainer direction on 2026-05-25 keeps this published branch stacked on other
work. A branch diff against `origin/main` may therefore include unrelated
target-native init, release, adapter, validator, skill, and placement-contract
files. Those stacked changes are intentionally retained in the branch, but they
are not part of the behavior-preservation claim for this M1 vision/README
slice.

For this slice, behavior preservation is evaluated against the scoped M1 changes
that rewrote `VISION.md`, README positioning, and change-local lifecycle
evidence.
