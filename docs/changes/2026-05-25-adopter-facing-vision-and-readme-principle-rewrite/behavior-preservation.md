# Behavior Preservation

| Surface | Baseline | New proof | Preservation result |
| --- | --- | --- | --- |
| Runtime CLI behavior | no CLI source files touched | diff limited to `VISION.md`, `README.md`, and lifecycle evidence | unchanged |
| Skill behavior | no `skills/` files touched | diff proof | unchanged |
| Adapter output | no `dist/adapters/` files touched | diff proof | unchanged |
| Validators | no `scripts/` files touched | diff proof | unchanged |
| Release process | no release artifacts touched | diff proof | unchanged |
| Vision source of truth | `VISION.md` owns durable project vision; README marker block derives from it | `vision-readme-sync-proof.md` | strengthened |
| README positioning | mechanism-heavy first-screen framing | benefit-first hook, diagram, worked example, and principles | improved |
| Traceability explanation | visible but less central | diagram plus worked example chain | improved |
| Learn stage framing | internal self-improvement wording risk | durable lessons and reliability framing | improved |

## Diff boundary

This slice intentionally changes documentation and lifecycle evidence only:

- `VISION.md`
- `README.md`
- `docs/proposals/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`
- `docs/plans/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite.md`
- `docs/plan.md`
- `docs/changes/2026-05-25-adopter-facing-vision-and-readme-principle-rewrite/`

No runtime, CLI, skill, adapter, validator, release, npm package, or generated
artifact behavior is changed.
