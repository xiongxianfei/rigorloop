# Vision Skill Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/vision-skill.md`
- Plan: `docs/plans/2026-04-29-vision-skill.md`
- Proposal: `docs/proposals/2026-04-29-vision-skill.md`
- Architecture: not required. The approved spec changes skill, governance, README ownership, proposal guidance, and generated distribution surfaces without adding a runtime boundary, data store, service, or architecture package.
- Spec-review findings: approved on 2026-04-29 after source-of-truth rank, governance update, mode reporting, privacy, external research, README marker insertion, and vision-conflict exception rules were added.
- Plan-review findings: approved after M4 lifecycle validation was updated to include this test spec.

## Testing strategy

- Contract tests inspect authored Markdown surfaces because the first implementation is a skill and governance change, not a new executable README mirror helper.
- Skill validation uses `python scripts/validate-skills.py`, `python scripts/test-skill-validator.py`, and focused content scans to prove the canonical `vision`, `proposal`, and `proposal-review` skills carry the required behavior.
- Generated-output integration uses existing generator and adapter checks so `.codex/skills/` and `dist/adapters/` remain derived from canonical `skills/`.
- Selector and lifecycle tests use existing repository-owned scripts to prove supported paths are classified, `README.md` remains an explicit manual route while unclassified, broad smoke is honored from the active plan, and final closeout validates every authoritative lifecycle artifact.
- Manual verification is limited to README ownership wording and marker-behavior wording because no README mirror helper is implemented in this slice.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R4` | `T1`, `T12` | Canonical skill exists, validates, uses `name: vision`, and defines create/revise/mirror modes. |
| `R5`-`R20` | `T2`, `T3`, `T12` | Mode behavior, overwrite protection, no initial `vision.md`, and substantive revision reminders are proven through skill contract checks. |
| `R21`-`R28`, `R56`-`R60` | `T2`, `T5`, `T12` | Vision content shape and mode output reporting are documented in the skill. |
| `R29`-`R39`, `R75`-`R78` | `T6`, `T12` | Proposal and proposal-review guidance cover `Vision fit`, conflicts, and explicit exceptions. |
| `R40`-`R42` | `T1`, `T7`, `T12` | Vision remains upstream, not a normal lifecycle stage, and no README helper script is required. |
| `R43`-`R45` | `T8`, `T9`, `T12` | Generated `.codex/skills/` and public adapters are refreshed and checked through existing generators. |
| `R46`-`R55` | `T7`, `T12` | Governance, workflow, AGENTS, and README ownership guidance document the `vision.md` source-of-truth boundary. |
| `R61`-`R64` | `T5`, `T12` | Sensitive information and external research boundaries are documented in the skill. |
| `R65`-`R68` | `T5`, `T12` | Plain Markdown and bounded-read behavior are documented in the skill. |
| `R69`-`R74` | `T4`, `T12` | README marker insertion and edit-boundary behavior are documented in the skill. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T2`, `T4` | Create mode is documented as the only path that creates initial `vision.md` and README front-matter. |
| `E2` | `T3`, `T8` | Adding the skill and generated outputs does not create root `vision.md`. |
| `E3` | `T2` | Existing vision plus unclear mode stops before overwrite. |
| `E4` | `T4` | Mirror mode edits only README front-matter. |
| `E5` | `T6` | Proposal guidance requires `Vision fit` when a vision exists. |
| `E6` | `T6` | Proposal guidance uses `no vision exists yet` when no root vision exists. |
| `E7` | `T6` | Proposal-review classifies conflicts as revise proposal, revise vision, or explicit exception. |

## Edge case coverage

- Root `vision.md` exists and README lacks markers: `T2`, `T4`
- Root `vision.md` does not exist and README already has markers: `T4`
- README has malformed, nested, or multiple marker pairs: `T4`
- Proposal says `fits the current vision` while no `vision.md` exists: `T6`
- Proposal omits `Vision fit` after adoption: `T6`
- Vision revision changes scope but is labeled editorial: `T2`, `T5`
- User asks to revise an unnamed section: `T2`
- Mirror mode finds README front-matter already current: `T2`
- Generated adapter output omits portable `vision` skill: `T8`
- Legacy proposal lacks `Vision fit`: `T6`
- `README.md` remains selector-unclassified in v1: `T9`

## Acceptance criteria coverage map

| Acceptance criterion | Test IDs | Notes |
| --- | --- | --- |
| `AC1` | `T1`, `T2` | Authored `vision` skill validates and documents modes. |
| `AC2` | `T3` | Root `vision.md` is absent after the skill implementation. |
| `AC3` | `T6` | Proposal skill requires `Vision fit` for new or substantively revised proposals after adoption. |
| `AC4` | `T6` | Proposal-review checks `Vision fit` and classifies conflicts. |
| `AC5` | `T7` | Workflow guidance does not add `vision` to the normal lifecycle chain. |
| `AC6` | `T8` | Generated `.codex/skills/` output is synchronized through `scripts/build-skills.py`. |
| `AC7` | `T8` | Generated public adapter output is synchronized through `scripts/build-adapters.py`. |
| `AC8` | `T4` | README marker ownership is documented without a helper script. |
| `AC9` | `T9`, `T12` | Selector-selected validation covers changed paths, with broad smoke only from the active plan trigger. |
| `AC10` | `T7` | Governance and ownership guidance document the vision source-of-truth boundary. |
| `AC11` | `T4` | README marker insertion is deterministic and preserves content outside the marker block. |
| `AC12` | `T6` | Explicit vision-conflict exception guidance includes required owner, evidence, rationale, record location, and trigger classification. |

## Test cases

### T1. Canonical vision skill validates and defines the supported modes

- Covers: `R1`-`R4`, `R40`-`R42`, `AC1`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Run `python scripts/validate-skills.py skills/vision/SKILL.md`.
  - Inspect the skill metadata for `name: vision`.
  - Inspect the description for project vision and README front-matter ownership.
  - Inspect the body for exactly the supported mode names: `create`, `revise`, and `mirror`.
  - Inspect the body for upstream-not-lifecycle-stage wording and no required README helper script.
- Expected result:
  - The authored skill validates and exposes the approved mode contract.
- Failure proves:
  - Contributors cannot reliably invoke or distribute the new skill contract.
- Automation location:
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - Optional focused assertions in `scripts/test-skill-validator.py`

### T2. Vision skill documents mode behavior, overwrite protection, and output shape

- Covers: `R5`-`R7`, `R9`-`R20`, `R21`-`R28`, `R56`-`R60`, `E1`, `E3`, EC1, EC6, EC7, EC8
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Inspect create mode for root `vision.md` creation and README front-matter generation.
  - Inspect unclear existing-vision behavior for a stop-and-ask rule before edits.
  - Inspect mirror mode for `vision.md` unchanged and README front-matter regeneration.
  - Inspect revise mode for named-section edits, cascade explanation, substantive/editorial classification, and change-local reminder wording.
  - Inspect the content rules: 500-word cap, plain language, no requirements vocabulary, no implementation details, required vision sections, README subset, and output reporting.
- Expected result:
  - The skill tells an agent exactly when to create, revise, mirror, stop, report, or remind about change-local traceability.
- Failure proves:
  - A future run could overwrite authorial judgment, create an uncontrolled vision artifact, or produce an invalid vision shape.
- Automation location:
  - Focused content assertions in `scripts/test-skill-validator.py`, or milestone `rg` scans from the active plan.

### T3. First implementation does not create root vision.md

- Covers: `R8`, `E2`, `AC2`
- Level: smoke
- Fixture/setup:
  - repository root after M1 and final M4 validation
- Steps:
  - Run `test ! -e vision.md`.
  - Confirm generated output refreshes in M3 do not add root `vision.md`.
- Expected result:
  - The root `vision.md` path is absent until a later explicit `vision create` invocation.
- Failure proves:
  - The implementation created project-level authorial content as a side effect of adding the skill.
- Automation location:
  - M1 validation command and M4 final validation notes

### T4. README marker behavior is deterministic and marker-bounded

- Covers: `R10`-`R13`, `R25`-`R26`, `R69`-`R74`, `E1`, `E4`, EC1, EC2, EC3, `AC8`, `AC11`
- Level: contract/manual
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - `README.md`
- Steps:
  - Inspect the skill for the exact marker pair `<!-- vision:start -->` and `<!-- vision:end -->`.
  - Inspect create-mode guidance for deterministic marker insertion after the first H1 block, including attached badge/image lines and blanks.
  - Inspect no-H1 behavior for start-of-file insertion.
  - Inspect valid marker behavior for replacing only content inside the marker block.
  - Inspect malformed, nested, or multiple marker behavior for stop-and-request-explicit-handling.
  - Confirm no helper script is introduced in this first implementation.
- Expected result:
  - README front-matter ownership is deterministic and does not authorize broad README rewrites.
- Failure proves:
  - The v1 marker contract is ambiguous or silently permits edits outside generated front-matter.
- Automation location:
  - Focused content assertions in `scripts/test-skill-validator.py`, plus manual review of README ownership wording.

### T5. Vision skill documents privacy, research, Markdown, and bounded-read boundaries

- Covers: `R21`-`R23`, `R61`-`R68`, EC6
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Inspect the skill for sensitive-information exclusions: secrets, credentials, private local paths, private machine names, and personal data not intended for publication.
  - Inspect external research rules requiring explicit user request or a research-backed workflow mode, with researched facts distinguished from assumptions.
  - Inspect plain Markdown rules that avoid tables, diagrams, HTML layout, and generated assets as requirements for understanding.
  - Inspect bounded-read guidance that starts from compact inputs and escalates to full-file reads only when compact inputs are missing, conflicting, or insufficient.
- Expected result:
  - The skill prevents public-vision leakage, unrequested research, unreadable output, and needless broad reads.
- Failure proves:
  - The vision skill can expose private data, overclaim research, or inflate evidence collection.
- Automation location:
  - Focused content assertions in `scripts/test-skill-validator.py`

### T6. Proposal and proposal-review skills enforce Vision fit behavior

- Covers: `R29`-`R39`, `R75`-`R78`, `E5`, `E6`, `E7`, EC4, EC5, EC10, `AC3`, `AC4`, `AC12`
- Level: contract
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- Steps:
  - Inspect proposal guidance for a required `Vision fit` section on new and substantively revised proposals after adoption.
  - Inspect the exact allowed values, including `no vision exists yet`.
  - Inspect guidance that prevents silently redefining project vision.
  - Inspect proposal-review guidance for missing-section handling and conflict classification.
  - Inspect explicit exception guidance for owner or stage, evidence, why proposal and vision revision were not chosen, record location, and future-trigger classification.
  - Inspect legacy-proposal wording so historical proposals are not invalid solely because they lack `Vision fit`.
- Expected result:
  - Proposal authors and reviewers have one visible proposal-fit decision point without rewriting legacy proposals.
- Failure proves:
  - Proposal review can miss vision conflicts or demand retroactive churn on legacy artifacts.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/test-skill-validator.py`
  - Focused `rg` scans if no dedicated regression is added

### T7. Governance and public ownership surfaces document the vision source-of-truth boundary

- Covers: `R40`-`R42`, `R46`-`R55`, `AC5`, `AC10`
- Level: contract/manual
- Fixture/setup:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `README.md`
- Steps:
  - Inspect `CONSTITUTION.md` for `vision.md` below `CONSTITUTION.md` and above README front-matter in the vision source-of-truth story.
  - Inspect `AGENTS.md` and `docs/workflows.md` for concise operational guidance: `vision` is upstream and not a normal per-change stage.
  - Inspect README ownership guidance for generated marker-bounded front-matter from `vision.md`.
  - Confirm README front-matter is not independently authoritative when it conflicts with `vision.md`.
  - Confirm workflow guidance does not insert `vision` into the normal lifecycle chain.
- Expected result:
  - Governance, workflow, and README ownership surfaces all tell the same source-of-truth story.
- Failure proves:
  - Agents can follow conflicting precedence, lifecycle, or README ownership guidance.
- Automation location:
  - Focused `rg` scans plus manual review
  - `python scripts/select-validation.py --mode explicit --path README.md` as expected blocked selector inspection with manual route

### T8. Generated Codex and adapter outputs are refreshed only through existing generators

- Covers: `R43`-`R45`, `E2`, EC9, `AC6`, `AC7`
- Level: integration
- Fixture/setup:
  - canonical skill sources under `skills/`
  - generated Codex mirror under `.codex/skills/`
  - generated public adapters under `dist/adapters/`
- Steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Inspect generated manifest and adapter skill output for `vision` inclusion when portability rules allow it.
  - Confirm opencode command aliases are not added for `vision` unless existing alias policy includes it.
- Expected result:
  - Generated outputs include the new portable skill and updated proposal/review guidance without hand edits or drift.
- Failure proves:
  - Distribution surfaces are stale, manually edited, or inconsistent with canonical skill sources.
- Automation location:
  - Existing generated-output and adapter commands from M3 and M4

### T9. Selector routing proves classified paths and README manual routing

- Covers: `AC9`, EC11
- Level: integration
- Fixture/setup:
  - changed canonical skill, governance, generated-output, lifecycle, and README paths
- Steps:
  - Run `python scripts/test-select-validation.py`.
  - Run selector explicit mode for canonical governance and skill paths listed in M2.
  - Run selector explicit mode for generated paths listed in M3.
  - Run `python scripts/select-validation.py --mode explicit --path README.md` and record the expected blocked `unclassified-path` result.
  - Use the documented manual route for README: `git diff --check -- README.md` plus review against `R51`, `R54`, `R55`, and `AC10`.
- Expected result:
  - Classified paths select the expected repository-owned checks, while README remains a deliberate manual route in v1.
- Failure proves:
  - Validation routing either misses changed surfaces or pretends unclassified README edits are covered by selected CI.
- Automation location:
  - `python scripts/test-select-validation.py`
  - `python scripts/select-validation.py --mode explicit ...`

### T10. Change metadata and lifecycle validation include the matching test spec

- Covers: all requirements as closeout evidence
- Level: integration
- Fixture/setup:
  - `docs/changes/2026-04-29-vision-skill/change.yaml`
  - `docs/plan.md`
  - `docs/plans/2026-04-29-vision-skill.md`
  - `docs/proposals/2026-04-29-vision-skill.md`
  - `specs/vision-skill.md`
  - `specs/vision-skill.test.md`
- Steps:
  - Run `python scripts/test-change-metadata-validator.py`.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-04-29-vision-skill/change.yaml`.
  - Run the M4 lifecycle command, including `--path specs/vision-skill.test.md`.
  - Confirm `change.yaml` records proposal, spec, plan, test spec, canonical skill, governance, README, and generated-output artifacts.
- Expected result:
  - Final closeout validates every lifecycle-managed authoritative artifact for this planned initiative.
- Failure proves:
  - The implementation can appear complete while omitting the active proof map or change-local metadata.
- Automation location:
  - M4 validation commands

### T11. No unintended project-vision or README-front-matter content is introduced

- Covers: `R8`, `R11`, `R41`-`R42`, non-goals
- Level: smoke/manual
- Fixture/setup:
  - repository root
  - `README.md`
  - generated outputs after M3
- Steps:
  - Run `test ! -e vision.md`.
  - Inspect README diff to confirm the implementation updates ownership guidance only and does not insert generated `<!-- vision:start -->` front-matter.
  - Confirm no new README mirror helper script is introduced.
  - Confirm the normal lifecycle string does not include `vision`.
- Expected result:
  - The change installs the method without authoring the initial project vision or generated README front-matter.
- Failure proves:
  - The implementation crossed the proposal non-goal boundary.
- Automation location:
  - M1, M2, and M4 validation plus manual diff review

### T12. Final implementation gate runs targeted validation and broad smoke

- Covers: all requirements and `AC1`-`AC12`
- Level: smoke
- Fixture/setup:
  - all M1-M4 implementation changes
- Steps:
  - Run all M4 validation commands.
  - Run `bash scripts/ci.sh --mode broad-smoke` because the active plan requires broad smoke.
  - Run `git diff --check -- .`.
  - Record commands and results in the active plan validation notes and change-local metadata.
- Expected result:
  - The implementation is ready for first-pass `code-review`; PR and explain readiness remain downstream of code-review and verify.
- Failure proves:
  - The implementation is not ready to leave implementation, even if targeted local checks passed earlier.
- Automation location:
  - M4 validation commands

## Fixtures and data

- No new persistent fixtures are required by default.
- If implementation adds focused regression assertions, place them in existing repository-owned test modules such as `scripts/test-skill-validator.py` rather than adding a new validator.
- Generated-output tests use existing adapter fixtures under `tests/fixtures/adapters/`.
- Skill validation tests use existing skill fixtures under `tests/fixtures/skills/` when fixture changes are needed.
- Manual README proof uses the real `README.md` diff because no mirror helper script exists in this slice.

## Mocking/stubbing policy

- Do not mock repository-owned validation commands in milestone proof.
- Existing adapter tests may continue using temporary directories and in-process helper calls for generated-output fixtures.
- Do not stub `scripts/build-skills.py`, `scripts/build-adapters.py`, selector behavior, or artifact lifecycle validation in final M4 proof.

## Migration or compatibility tests

- Existing proposals remain valid without `Vision fit` until substantively revised; verify by inspecting proposal/proposal-review guidance rather than rewriting old proposals.
- Existing README content remains author-owned outside future vision markers; verify by diff review and `git diff --check -- README.md`.
- Generated adapter compatibility is validated through `python scripts/test-adapter-distribution.py`, `python scripts/build-adapters.py --version 0.1.1 --check`, and `python scripts/validate-adapters.py --version 0.1.1`.
- Existing lifecycle order remains unchanged; verify `docs/workflows.md` and relevant skill guidance do not insert `vision` into the normal lifecycle chain.

## Observability verification

- The skill's required user-facing run output is verified by contract text: mode used, files changed, README front-matter action, create-mode assumptions, revise-mode sections changed, and mirror-mode unchanged `vision.md`.
- No runtime logs, metrics, traces, or audit events are introduced.
- Final implementation evidence is recorded through plan validation notes and change-local metadata.

## Security/privacy verification

- Inspect the `vision` skill for sensitive-information exclusions and confirmation behavior before public inclusion.
- Inspect the `vision` skill for the external research boundary and researched-fact versus assumption reporting.
- Do not include secrets, credentials, private local paths, private machine names, or personal data in `vision.md`, README front-matter examples, tests, or generated adapter output.

## Performance checks

- No runtime performance behavior is introduced.
- Evidence collection performance is covered by bounded-read guidance in the `vision` skill and existing output-budget guidance in workflow documentation.
- Do not add broad scans beyond the active plan's explicit validation commands.

## Manual QA checklist

- Confirm no root `vision.md` exists after M1 and M4.
- Confirm README has no generated vision front-matter inserted by this implementation.
- Confirm README ownership wording is clear enough for future marker-bounded generation.
- Confirm proposal and proposal-review guidance uses exactly the approved `Vision fit` values.
- Confirm governance wording keeps `CONSTITUTION.md` above `vision.md` and README front-matter below `vision.md`.
- Confirm generated adapter manifest includes `vision` as a portable skill but does not add an opencode command alias unless the existing alias policy includes it.

## What not to test

- Do not create or validate the initial project `vision.md` in this implementation.
- Do not test actual README marker insertion with a helper script; no helper script is in scope.
- Do not rewrite existing proposals to add `Vision fit`.
- Do not test external Codex, Claude Code, or opencode execution.
- Do not fetch external research for vision drafting.
- Do not use snapshots as the only assertion for skill behavior; assert required contract wording directly.

## Uncovered gaps

- None. Requirements are covered by contract checks, existing repository-owned validation commands, generated-output integration checks, selector inspection, manual README review, or final closeout validation.

## Next artifacts

- `implement` for M1-M4 in `docs/plans/2026-04-29-vision-skill.md`.
- `code-review` after implementation completes and plan validation notes are updated.
- `verify` after code-review is clean or findings are resolved.
- `explain-change` and `pr` after verify reports branch readiness.

## Follow-on artifacts

- None yet.

## Readiness

This test spec is active as the proof map for the vision skill implementation. After this test spec is validated, the next repository stage is `implement`.
