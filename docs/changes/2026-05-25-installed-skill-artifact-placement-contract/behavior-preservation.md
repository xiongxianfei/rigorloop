# Behavior Preservation: Installed-Skill Artifact Placement Contract

## Scope

This proof records M3 generated-output and cold-read evidence for the installed-skill artifact placement contract.

## Generated Output Proof

Version used: `v0.1.5`, matching `dist/adapters/manifest.yaml`.

Temporary output root:

```text
/tmp/rigorloop-m3-adapters
```

Commands:

```bash
python scripts/build-skills.py --check
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-m3-adapters
python scripts/validate-adapters.py --root /tmp/rigorloop-m3-adapters --version v0.1.5
```

Result:

```text
pass
```

Generated archives:

```text
/tmp/rigorloop-m3-adapters/rigorloop-adapter-codex-v0.1.5.zip
/tmp/rigorloop-m3-adapters/rigorloop-adapter-claude-v0.1.5.zip
/tmp/rigorloop-m3-adapters/rigorloop-adapter-opencode-v0.1.5.zip
```

Archive content check:

| Archive | Proof |
| --- | --- |
| `rigorloop-adapter-codex-v0.1.5.zip` | `.agents/skills/proposal-review/SKILL.md` contains `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`; `.agents/skills/spec-review/SKILL.md` contains `docs/changes/<change-id>/reviews/spec-review-r<n>.md`; `.agents/skills/plan/SKILL.md` contains `docs/plans/YYYY-MM-DD-slug.md`. |
| `rigorloop-adapter-claude-v0.1.5.zip` | `.claude/skills/proposal-review/SKILL.md` contains `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`; `.claude/skills/spec-review/SKILL.md` contains `docs/changes/<change-id>/reviews/spec-review-r<n>.md`; `.claude/skills/plan/SKILL.md` contains `docs/plans/YYYY-MM-DD-slug.md`. |
| `rigorloop-adapter-opencode-v0.1.5.zip` | `.opencode/skills/proposal-review/SKILL.md` contains `docs/changes/<change-id>/reviews/proposal-review-r<n>.md`; `.opencode/skills/spec-review/SKILL.md` contains `docs/changes/<change-id>/reviews/spec-review-r<n>.md`; `.opencode/skills/plan/SKILL.md` contains `docs/plans/YYYY-MM-DD-slug.md`. |

## Cold-Read Proof

| Question | Skill-only answer | Evidence surface |
| --- | --- | --- |
| Where does a proposal-review record go? | `docs/changes/<change-id>/reviews/proposal-review-r<n>.md` | `proposal-review` `Artifact placement` section. |
| Where does a spec-review record go before a change pack exists? | The record defaults to `docs/changes/<change-id>/reviews/spec-review-r<n>.md`; for formal lifecycle review, create or request `docs/changes/<change-id>/` before claiming `Recording status: recorded`. | `spec-review` `Artifact placement` section. |
| Which plan surface should I update? | Use `docs/workflows.md` for the workflow map, `docs/plan.md` for the plan index, `docs/plans/YYYY-MM-DD-slug.md` for the plan body, `docs/changes/<change-id>/change.yaml` for change metadata, and `docs/changes/<change-id>/` for change-local evidence. | `plan` `Artifact placement` section. |

## Behavior Preservation Matrix

| Surface | Baseline | New proof | Preservation result |
| --- | --- | --- | --- |
| proposal-review recording | placement ambiguous or workflow-guide-dependent | skill states default review path and pre-change-pack rule | strengthened |
| spec-review recording | placement ambiguous or workflow-guide-dependent | skill states default review path and pre-change-pack rule | strengthened |
| plan references | `plan` could be ambiguous | `plan` skill distinguishes workflow map, plan index, plan body, change metadata, and change-local evidence | strengthened |
| `docs/workflows.md` | project-local map | synchronized with skill defaults and documented as secondary customization surface | preserved and strengthened |
| custom paths | explicit paths and workflow-map paths override portable defaults where safe | lookup wording preserves explicit paths, active metadata, specs/schemas, workflow rows, then portable defaults | preserved |
| review schema | exact fields owned outside skill | placement blocks state paths and recording boundaries without duplicating full schemas | preserved |
| generated adapters | previous skill text packaged | adapter archives generated from canonical skills and validated under `/tmp/rigorloop-m3-adapters` | current |

## Boundary Checks

- No generated adapter archive or temporary adapter output is tracked.
- No generated public adapter package output was hand-edited.
- No review-record schema, review status, severity, or disposition semantics changed.
- No historical artifact migration or CLI scaffolding was introduced.
