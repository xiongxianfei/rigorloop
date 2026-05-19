# Published Skill Design Spec Family Behavior Parity Evidence

## Scope

Changed rollout skills:

- `skills/spec/SKILL.md`
- `skills/spec-review/SKILL.md`

M1 defines representative artifacts and parity dimensions. M3 must record final parity results after the skill rewrites.

## Representative Artifacts

| ID | Skill | Representative input | Why representative |
| --- | --- | --- | --- |
| `SF-PARITY-1` | `spec` | Accepted proposal for a behavior change that affects externally observable behavior, compatibility, validation, and lifecycle handoff. | Exercises spec authoring from upstream artifact through requirements, examples, edge cases, acceptance criteria, non-goals, next artifacts, and readiness. |
| `SF-PARITY-2` | `spec-review` | Feature spec with at least one material issue in testability, compatibility, observability, or lifecycle readiness. | Exercises formal review dimensions, material finding shape, recording obligations, immediate next-stage wording, and eventual test-spec readiness. |
| `SF-PARITY-3` | `spec-review` | Feature spec that is review-clean and ready for the next repository stage. | Exercises clean review receipt behavior, no-material finding output, isolation, and readiness wording. |

## Parity Dimensions

M3 evidence must show that rewritten skill text does not weaken these dimensions.

| Dimension | `spec` expected preservation | `spec-review` expected preservation |
| --- | --- | --- |
| Artifact/output shape | Required sections, examples first, requirement IDs, edge cases, non-goals, acceptance criteria, open questions, next artifacts, follow-on artifacts, and readiness remain required. | Result block, material finding fields, review dimensions, exact review status, recording status, review record/log/resolution fields, open blockers, and immediate next stage remain required. |
| Lifecycle claim boundaries | Spec authoring can hand off to `spec-review` when no blockers remain, but does not claim plan, implementation, verification, branch, or PR readiness. | Spec review can approve or request changes and report immediate next repository stage/test-spec readiness, but does not start architecture, plan, test-spec, implementation, verify, or PR automatically. |
| Recording obligations | Upstream status settlement reporting remains intact when triggered. | Clean review receipts, detailed records for material findings, review logs, and review-resolution triggers remain intact. |
| Stop conditions | Missing or contradictory upstream evidence, unknown settlement mapping, unclear behavior, and blocker states still stop the workflow. | Missing required inputs, untestable requirements, unresolved material findings, missing recording, and not-ready test-spec readiness still stop downstream reliance. |
| Validation obligations | Every `MUST` remains testable or manually justified; compatibility, migration, observability, security/privacy, and performance remain explicit when relevant. | Review still challenges testability, compatibility, observability, security/privacy, examples, non-goals, and acceptance criteria. |
| Self-containment | Project-local evidence remains conditional; RigorLoop repository-internal files are not required in customer projects. | Project-local evidence remains conditional; review record paths are resolved through project workflow guidance and available artifacts. |

## Baseline Token Evidence

Measured on 2026-05-19 with:

```bash
python scripts/measure-skill-tokens.py --skills-root skills
```

| Skill | Bytes | Lines | Estimated tokens | Largest sections |
| --- | ---: | ---: | ---: | --- |
| `spec` | 9164 | 192 | 2288 | `Required sections` 378; `Upstream status settlement` 352; `Rules` 222 |
| `spec-review` | 7968 | 183 | 1992 | `Isolation and Recording` 417; `Rules` 261; `Review dimensions` 227 |

## M3 Result Table

M3 must fill this table after rewriting the target skills.

| Representative artifact | Skill | Baseline behavior | After-change behavior | Parity result | Evidence |
| --- | --- | --- | --- | --- | --- |
| `SF-PARITY-1` | `spec` | Required spec sections, examples first, stable requirement IDs, edge cases, non-goals, acceptance criteria, upstream settlement, output path, artifact placement, and readiness were required. | Same behavior remains required; section names are compacted in `## Required sections`, concrete shape is now in `## Output skeleton`, and `## Workflow role` clarifies no downstream readiness claim. | pass | `skills/spec/SKILL.md` preserves `## Upstream status settlement`, `## Output path`, `## Artifact placement`, `## Required sections`, `## Requirement format`, `## Rules`, `## Workflow handoff behavior`, and adds `## Output skeleton`. |
| `SF-PARITY-2` | `spec-review` | Material review required finding ID, severity, location, evidence, required outcome, safe resolution or needs-decision rationale, recording, review log, and review-resolution when triggered. | Same material finding and recording requirements remain; `## Output skeleton` now makes the result and finding fields explicit, and `## Workflow role` preserves lifecycle-gate boundaries. | pass | `skills/spec-review/SKILL.md` preserves `## Finding severity`, `## Material findings`, `## Isolation and Recording`, `## Rules`, `## Workflow handoff behavior`, and adds `## Output skeleton`. |
| `SF-PARITY-3` | `spec-review` | Clean review required no material findings, clean review receipt, review log, immediate next repository stage, eventual `test-spec` readiness, isolation, and no automatic downstream handoff. | Same clean review and isolation behavior remains; expected output is compacted but still requires result fields, next stage, `test-spec` readiness, and stop condition. | pass | `skills/spec-review/SKILL.md` `## Isolation and Recording`, `## Rules`, `## Workflow handoff behavior`, `## Output skeleton`, and `## Expected output`. |

## M3 Closeout Rule

M3 must not claim behavior parity from structural validation alone.

Final evidence must state whether material review status, finding format, recording obligations, stop conditions, validation obligations, and claim boundaries were preserved.

## M3 Final Parity Statement

Material review status, finding format, recording obligations, stop conditions,
validation obligations, and claim boundaries were preserved. The change adds
routing-focused descriptions, workflow-role blocks, and compact output
skeletons while compressing duplicate prose.

## M3 Token Delta

Measured on 2026-05-19 with:

```bash
python scripts/measure-skill-tokens.py --skills-root skills
```

| Skill | Baseline estimated tokens | After-change estimated tokens | Delta | Budget result |
| --- | ---: | ---: | ---: | --- |
| `spec` | 2288 | 2514 | +9.9% | within +10% hard cap |
| `spec-review` | 1992 | 2183 | +9.6% | within +10% hard cap |
