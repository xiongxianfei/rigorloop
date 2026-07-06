# Subagent-Assisted Code Review Behavior Preservation

Change ID: `2026-07-06-subagent-assisted-code-review`
Date: 2026-07-06
Milestone: M3 generated output and adapter proof

## Scope

This matrix records M3 proof that the subagent-assisted `code-review` contract remains source-derived through repository-owned generated-skill and adapter-package validation.
M3 does not add target-native subagent configs, persistent packet files, parallel execution, new dependencies, or tracked generated public adapter skill bodies.

## Preservation Matrix

| Surface | Baseline | M3 proof | Result |
| --- | --- | --- | --- |
| Canonical `code-review` source | Authored source lives under `skills/code-review/SKILL.md`. | `python scripts/validate-skills.py skills/code-review/SKILL.md` validates the canonical skill source. | preserved |
| Generated local skill mirror | Local mirrors are generated from canonical `skills/` source, not edited as authority. | `python scripts/build-skills.py --check` generated a temporary skill mirror from `skills/` and validated it without reading tracked generated output. | preserved |
| Generated skill regression coverage | Generated mirror behavior is covered by repository-owned regression tests. | `python scripts/test-build-skills.py` covers temporary mirror generation, structural validation, and mapped resource parity. | preserved |
| Public adapter release archives | For `v0.1.3` and later, public adapter skill bodies are release archives derived from canonical sources, not tracked source under `dist/adapters/`. | `python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives` builds required adapter release archives in a temporary output directory and validates them from canonical fixture skills. | preserved |
| First-slice deferred boundaries | No required Claude configs, no persistent packet files, no parallel subagent execution, and no new dependency are part of the first implementation. | No target-native config files, packet store, parallel runner, dependency manifest, or generated adapter package body is added by M3. | preserved |
| Generated-output hand-edit boundary | Generated public adapter package output must not be hand-edited. | M3 touches only change-local evidence and lifecycle state; generated public adapter package output under `dist/adapters/` is not edited. | preserved |

## M3 Proof Commands

```text
python scripts/validate-skills.py skills/code-review/SKILL.md
python scripts/build-skills.py --check
python scripts/test-build-skills.py
python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives
python scripts/validate-review-artifacts.py --mode structure docs/changes/2026-07-06-subagent-assisted-code-review
python scripts/validate-change-metadata.py docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml
python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/proposals/2026-07-06-subagent-assisted-code-review.md --path specs/subagent-assisted-code-review.md --path specs/subagent-assisted-code-review.test.md --path docs/plans/2026-07-06-subagent-assisted-code-review.md --path docs/plan.md --path docs/changes/2026-07-06-subagent-assisted-code-review/change.yaml
git diff --check --
```

The explicit CI wrapper is run after this artifact is recorded so selector-owned generated-output, adapter, lifecycle, metadata, and prose checks can validate the complete M3 handoff surface.

## Conclusion

M3 is a no-runtime-code proof slice.
The generated-skill and adapter packaging boundaries remain source-derived through existing repository-owned scripts.
No generated public adapter package output is committed or hand-edited.
