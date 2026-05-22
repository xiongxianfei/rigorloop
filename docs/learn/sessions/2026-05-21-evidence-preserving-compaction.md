# Learn Session: Evidence-Preserving Compaction

## Frame

- Date: 2026-05-21
- Status: session-recorded; durable lesson routed to topic guidance
- Trigger: contributor explicitly invoked `learn` with the observation that recent noisy-output and compact-metadata work succeeded when it separated safe compression from evidence or behavior that must be preserved.
- Trigger type: explicit contributor observation with repeated-artifact evidence.
- Scope: recent RigorLoop proposals and review artifacts where output or durable metadata volume was reduced only after preservation boundaries were made explicit.
- Session path: `docs/learn/sessions/2026-05-21-evidence-preserving-compaction.md`

## Evidence Reviewed

- Contributor trigger text for this session.
- `docs/proposals/2026-05-21-script-output-optimization.md`
  - Presentation output is optimized while validation behavior, selected checks, exit codes, failure detection, and verbose output remain preserved.
- `docs/proposals/2026-05-21-compact-change-validation-metadata.md`
  - Common-read validation metadata is compacted while exact validation evidence remains reconstructable.
  - The proposal pins path-expanding bundles through accumulated per-bundle `paths_added` rather than best-effort reconstruction.
- `specs/compact-change-validation-metadata.md`
  - Requirements `R30` through `R32` require path accumulation and exact command/path-set reconstruction from `change.yaml` alone.
  - Requirements `R56` through `R60` keep transcript files non-load-bearing and make compactness secondary to reconstructable evidence.
- `docs/changes/2026-05-21-compact-change-validation-metadata/reviews/spec-review-r1.md`
  - Current material findings show that broad claims still need explicit mechanisms, such as defined brace escaping, first-exists stage mapping, and summary consistency rules.
- `docs/proposals/2026-05-21-review-skill-family-consistency-parser-owned-finding-shape.md`
  - Review-family asset extraction preserves parser-owned finding shape, status vocabularies, and review behavior while reducing duplication.
- Prior learn topics:
  - `docs/learn/topics/token-cost-measurement.md`
  - `docs/learn/topics/review-artifact-recording.md`
  - `docs/learn/topics/skill-asset-design.md`
  - `docs/learn/topics/plan-lifecycle-closeout.md`

## Exclusions

- No spec, proposal, review-resolution, validator, workflow, or skill behavior is changed by this learn session.
- No spec-review finding is resolved here; `docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md` remains the action-owning artifact for open compact-metadata spec-review findings.
- No verification readiness, PR readiness, plan closeout, or review-resolution closeout is claimed.

## Prior Learnings Reviewed

- `docs/learn/topics/token-cost-measurement.md` captures diagnosing cost by category before optimizing and preserving safety-critical guidance.
- `docs/learn/topics/review-artifact-recording.md` captures parser-owned field shape for material findings.
- `docs/learn/topics/skill-asset-design.md` captures when extracted assets earn their file and how to avoid ceremony.
- No existing topic directly captured the repeated pattern of evidence-preserving compaction across script output, compact validation metadata, and review-family extraction.

## Observations

### O1: Successful noise reduction starts by separating safe presentation from preserved evidence or behavior

The script-output proposal, compact validation metadata proposal, and review-family shape work all reduce repeated or noisy surfaces, but they do not treat byte or token reduction as the primary invariant.

Evidence:

- The script-output proposal states that it changes presentation only and preserves selected checks, exit behavior, failure detection, counts, durations, and verbose output.
- The compact validation metadata proposal reduces common-read metadata while preserving reconstructable commands, path sets, stage results, counts, blockers, and optional forensic transcript links.
- The review-family proposal extracts repeated review skeletons while preserving parser-owned fields, review-status vocabularies, stop conditions, and review behavior.

### O2: Preservation claims require pinned mechanisms, not just intent

The recurring failure shape is not the optimization idea. The idea is usually sound. The gap appears when a proposal says a property is preserved but the concrete mechanism is not yet testable.

Evidence:

- Compact metadata needed the OBS-1 path-accumulation rule so a reviewer can reconstruct the exact historical lifecycle command and path set for each stage.
- Current compact-metadata spec review findings show the same pattern in smaller forms: literal brace escaping, first-exists stage mapping, and `stages_validated` summary consistency are each asserted or referenced before being fully specified.
- Review-family work had the same boundary around parser-owned shape: the durable finding record must instantiate the parser-recognized fields, not merely describe them in prose.

### O3: Compactness metrics are useful only under a preservation gate

The compact-metadata proposal's 30% common-read reduction threshold is meaningful because it is subordinate to reconstruction. Without that ordering, size targets can incentivize dropping audit evidence.

Evidence:

- The compact metadata proposal and spec require reconstruction preservation before size reduction is evaluated.
- The script-output proposal similarly makes quiet output subordinate to unchanged validation behavior and loud failure reporting.

## Classification Decisions

| Observation | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | durable-lesson | Topic guidance | Contributor explicit `learn` invocation plus repeated proposal evidence | The pattern recurs across at least three recent change streams and is useful guidance for future compaction or output-volume work. |
| O2 | durable-lesson | durable-lesson | Topic guidance; existing compact-metadata review-resolution owns current spec fixes | Contributor explicit `learn` invocation plus current spec-review findings | The lesson generalizes: preservation claims must be backed by deterministic, testable mechanisms. |
| O3 | durable-lesson | durable-lesson | Topic guidance | Contributor explicit `learn` invocation plus proposal/spec acceptance criteria evidence | The ordering of preservation gate before efficiency metric is a reusable guardrail. |

Contributor confirmation status: confirmed by explicit contributor `learn` request and supplied throughline.

## Routing Results

- Observation routing: recorded in this session.
- Durable lesson routing: added `docs/learn/topics/evidence-preserving-compaction.md`.
- Artifact update routing: none in this session.
- Decision routing: none.
- Process follow-up routing: none scheduled.
- Existing action-owning artifact: `docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md` remains responsible for resolving current compact-metadata spec-review findings.

## Best Practices

1. Start compaction work by naming what is safe to compress.

Examples include presentation output, common-read metadata, repeated command templates, repeated path prefixes, or extracted skeleton text.

2. Name the preserved invariant before choosing the compact representation.

Examples include validation selection, command exit behavior, failure detection, exact path sets, parser-owned fields, status vocabularies, counts, blockers, and transcript recoverability.

3. Require a pinned reconstruction or preservation mechanism.

Do not rely on "can reconstruct" or "valid by construction" as an assertion. The proposal, spec, or validator contract should identify the rule that makes it true, such as accumulated `paths_added`, parser-owned field labels, structured counts, or summary consistency checks.

4. Keep efficiency metrics below preservation gates.

Byte, token, or output-line reductions can prove that the mechanism helped, but they cannot compensate for lost evidence or changed behavior.

## Follow-Ups

- None scheduled by this learn session.
- Current compact-metadata spec-review findings remain open in `docs/changes/2026-05-21-compact-change-validation-metadata/review-resolution.md`.
