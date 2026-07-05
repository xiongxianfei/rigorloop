# Behavior Preservation

## Status

- Change ID: 2026-07-05-workflow-guide-skeleton-asset
- Evidence status: implementation evidence for M3
- Last updated: 2026-07-05

## Preservation Matrix

| Surface | Baseline | M3 evidence | Result |
| --- | --- | --- | --- |
| Workflow skill role | Creates or refreshes `docs/workflows.md` | M1 kept workflow guide creation in `skills/workflow/SKILL.md`; M3 only proves generated packaging | preserved |
| Stage-skill ownership | Stage skills own artifact content and portable defaults | No stage-skill source changed in M3 | preserved |
| Project-local artifact map | `docs/workflows.md` owns project-local placement | Skeleton remains a source asset for new or fully refreshed guides; existing `docs/workflows.md` is unchanged | strengthened |
| Portable defaults | Stage skills keep portable fallback behavior | No portable default text changed in M3 | preserved |
| Lifecycle order | Existing standard workflow order | M3 adds packaging assertions and evidence only | preserved |
| Registry validation | Workflow-map validation owns registry/table consistency | M2 composed skeleton validation with workflow-map checks; M3 does not add a duplicate validator | preserved |
| Generated packaging | No workflow skeleton asset existed | `python scripts/test-build-skills.py` and adapter archive proof confirm the mapped skeleton is included when `workflow` is packaged | strengthened |

## Generated Output Boundary

M3 did not hand-edit generated public adapter output. The proof uses repository-owned generation commands against temporary output roots.

Current adapter inclusion remains conditional: `workflow` is packaged for Codex and excluded from Claude/opencode by existing portability rules because the skill still contains Codex-specific `$skill` invocation syntax. The M3 regression asserts the skeleton is present in every adapter archive that actually packages `workflow`.
