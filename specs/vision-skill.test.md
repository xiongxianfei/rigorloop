# Vision Skill Test Spec

## Status

- active

## Related spec and plan

- Spec: `specs/vision-skill.md`
- Active plan: `docs/plans/2026-04-30-vision-skill-quality-refinement.md`
- Related proposal: `docs/proposals/2026-04-30-vision-skill-quality-refinement.md`
- Prior implementation plan: `docs/plans/2026-04-29-vision-skill.md`
- Prior proposal: `docs/proposals/2026-04-29-vision-skill.md`
- Architecture: not required. The approved refinement changes skill guidance, focused test assertions, generated output, and lifecycle artifacts without adding a runtime boundary, data store, service, dependency, deployment boundary, or architecture package.
- Spec-review findings: approved on 2026-04-30 after R81 workflow-fit placement and R91 mode-table wording were made directly testable.
- Plan-review findings: approved on 2026-04-30 with no material findings. Immediate handoff is `test-spec`; implementation follows only after this proof map is active.

## Testing strategy

- Contract tests inspect authored Markdown because the change is a workflow-skill guidance refinement, not a new executable README mirror helper.
- Focused assertions in `scripts/test-skill-validator.py` prove the new skill-contract shape: workflow-fit placement, drafting heuristics, one mode table, consolidated edit authorization, and enforceable substantive-revision traceability.
- Existing skill validation continues to prove canonical skill structure through `python scripts/validate-skills.py`.
- Generated-output integration uses existing generator and adapter checks so `.codex/skills/` and `dist/adapters/` remain derived from canonical `skills/`.
- Selector, lifecycle, and change-metadata validation prove the active plan, approved spec, active test spec, change-local metadata, and generated-output surfaces stay coherent.
- Manual review is limited to wording and diff-scope checks that are not worth encoding as a prose-quality validator.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R4` | `T1`, `T11` | Canonical skill metadata, description, and supported mode names remain valid. |
| `R5`-`R20`, `R56`-`R60`, `R91`, `R94` | `T2`, `T11` | Mode behavior is converted to one table while preserving stop conditions, output reporting, and enforcing causal-link traceability. |
| `R21`-`R28`, `R61`-`R68`, `R82`-`R90` | `T3`, `T11` | Vision content, privacy, research, Markdown, bounded-read rules, and drafting heuristics are proven through skill text. |
| `R40`-`R42`, `R46`-`R55`, `R81`, `R92`-`R93` | `T4`, `T6`, `T11` | Workflow fit, source-of-truth order, edit authorization, and lifecycle non-stage boundaries remain explicit. |
| `R10`-`R13`, `R25`-`R26`, `R69`-`R74` | `T5`, `T11` | README marker behavior remains deterministic and marker-bounded. |
| `R29`-`R39`, `R75`-`R78` | `T7`, `T11` | Proposal and proposal-review `Vision fit` behavior remains a regression guard. |
| `R8`, `R20`, quality-refinement non-goals | `T8`, `T11` | The refinement does not revise root `vision.md`, change README marker behavior, or extract shared boilerplate. |
| `R43`-`R45` | `T9`, `T11` | Generated skill and adapter output is refreshed only through existing generators. |
| `R79`-`R80` | `T10`, `T11` | README selector routing and marker validation remain covered when the vision skill is in scope. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T2`, `T5` | Create mode still creates root vision and README front-matter only when invoked. |
| `E2` | `T8`, `T9` | Adding or refining the skill does not itself create root vision content. |
| `E3` | `T2`, `T4` | Existing vision plus unclear mode still stops before overwrite. |
| `E4` | `T2`, `T5` | Mirror mode leaves `vision.md` unchanged and edits only README front-matter. |
| `E5` | `T7` | Proposal guidance still requires `Vision fit` when a vision exists. |
| `E6` | `T7` | Proposal guidance still handles the no-vision case. |
| `E7` | `T7` | Proposal-review still classifies vision conflicts. |
| `E8` | `T3` | Drafting heuristics cover differentiator, pain points, commitments, falsifiability, audience, and refusals. |
| `E9` | `T3` | Alternative-class comparison is accepted without requiring a named competitor. |
| `E10` | `T2` | Substantive revision traceability blocks finalization when the required causal link is missing. |
| `E11` | `T4` | Workflow-fit guidance appears before detailed mode mechanics. |

## Edge case coverage

- Root `vision.md` exists and README lacks markers: `T2`, `T5`
- Root `vision.md` does not exist and README already has markers: `T5`
- README has malformed, nested, or multiple marker pairs: `T5`
- Proposal says `fits the current vision` while no `vision.md` exists: `T7`
- Proposal omits `Vision fit` after adoption: `T7`
- Vision revision changes scope but is labeled editorial: `T2`
- User asks to revise an unnamed section: `T2`
- Mirror mode finds README front-matter already current: `T2`
- Generated adapter output omits portable `vision` skill: `T9`
- Legacy proposal lacks `Vision fit`: `T7`
- First-draft vision names no alternatives and states only abstract values: `T3`
- Substantive vision revision has an existing change-local pack but no causal link: `T2`
- Differentiator compares against an alternative class without naming a competitor: `T3`

## Acceptance criteria coverage map

| Acceptance criterion | Test IDs | Notes |
| --- | --- | --- |
| `AC1` | `T1`, `T2` | Authored `vision` skill validates and documents modes. |
| `AC2` | `T8`, `T11` | Refinement does not create or revise root vision content as a side effect. |
| `AC3` | `T7` | Proposal guidance remains covered. |
| `AC4` | `T7` | Proposal-review guidance remains covered. |
| `AC5` | `T4`, `T6` | Workflow guidance keeps `vision` outside the normal lifecycle. |
| `AC6` | `T9` | Generated `.codex/skills/` output is synchronized through `build-skills.py`. |
| `AC7` | `T9` | Generated public adapter output is synchronized through `build-adapters.py`. |
| `AC8` | `T5` | README marker ownership stays documented without a helper script. |
| `AC9` | `T10`, `T11` | Selector-selected validation covers README marker routing and changed lifecycle surfaces. |
| `AC10` | `T6` | Governance and ownership guidance remain aligned. |
| `AC11` | `T5` | README marker insertion and replacement boundaries remain deterministic. |
| `AC12` | `T7` | Explicit vision-conflict exception guidance remains covered. |
| `AC13` | `T3` | Drafting heuristics cover differentiator, pain points, commitments, falsifiability, audience, and refusals. |
| `AC14` | `T3` | Drafting heuristics allow an alternative class or specific tool and do not require a named competitor. |
| `AC15` | `T4` | Workflow-fit guidance placement is asserted. |
| `AC16` | `T2` | Mode behavior appears in one Markdown table with exact columns and rows. |
| `AC17` | `T4` | Source-of-truth, mode authorization, and overwrite protection are consolidated. |
| `AC18` | `T2` | Substantive revise-mode causal-link guidance is enforceable before finalizing. |
| `AC19` | `T8`, `T11` | Shared evidence-collection extraction remains out of scope. |

## Test cases

### T1. Canonical vision skill validates and keeps base metadata

- Covers: `R1`-`R4`, `R40`-`R42`, `AC1`, `AC5`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Run `python scripts/validate-skills.py skills/vision/SKILL.md`.
  - Inspect metadata for `name: vision`.
  - Inspect the description for project vision and README front-matter ownership.
  - Inspect the skill for exactly the supported mode names: `create`, `revise`, and `mirror`.
  - Inspect the skill for upstream-not-lifecycle-stage wording and no required README helper script.
- Expected result:
  - The authored skill remains valid and keeps the approved top-level invocation contract.
- Failure proves:
  - The refinement broke the portable skill contract before behavior-specific assertions run.
- Automation location:
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - `scripts/test-skill-validator.py`

### T2. Mode table and substantive revision traceability are enforceable

- Covers: `R5`-`R20`, `R56`-`R60`, `R91`, `R94`, `E1`, `E3`, `E4`, `E10`, `AC16`, `AC18`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Assert the skill has one Markdown table covering `create`, `revise`, and `mirror`.
  - Assert the table has columns for Mode, When it applies, Authorized edits, README behavior, and Stop or clarification conditions.
  - Assert the table has exactly one row for each mode.
  - Assert unclear existing-vision requests stop for clarification before editing.
  - Assert revise mode still limits edits to the named section unless a cascade is explained.
  - Assert revise mode asks or confirms substantive versus editorial classification before finalizing.
  - Assert substantive revisions tied to an existing or required change-local pack require causal links in `docs/changes/<change-id>/change.yaml` and `docs/changes/<change-id>/explain-change.md` before finalizing.
  - Assert the old soft wording, such as "remind the contributor", is absent.
  - Assert revise-mode output reports whether the required causal link was recorded or not required.
- Expected result:
  - Mode behavior is faster to compare and the traceability rule is a real gate instead of advice.
- Failure proves:
  - The primary refinement either lost existing stop conditions or left substantive traceability unenforceable.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T3. Drafting heuristics improve authoring without adding hidden requirements

- Covers: `R21`-`R24`, `R61`-`R68`, `R82`-`R90`, `E8`, `E9`, `AC13`, `AC14`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Assert a drafting-heuristics section appears after vision content guidance and before README front-matter guidance.
  - Assert heuristics are phrased as authoring questions or checks, not as additional required `vision.md` sections.
  - Assert the heuristics ask about an alternative class or specific tool, the tradeoff being made, embedded pain points, checkable commitments, observable falsifiability, audience non-fit, and concrete refusals.
  - Assert the wording explicitly allows either an alternative class or a specific tool and does not require a named competitor.
  - Assert the existing 500-word cap, plain-language rule, no requirements vocabulary, no implementation details, plain Markdown, privacy, external research, and bounded-read rules remain present.
- Expected result:
  - The skill guides stronger first drafts without changing the approved `vision.md` shape or creating competitor-name requirements.
- Failure proves:
  - The refinement either remains too vague to improve drafts or silently expands the vision contract.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T4. Workflow fit and edit authorization are visible before mechanics

- Covers: `R9`, `R40`, `R46`-`R47`, `R81`, `R92`-`R93`, `E11`, `AC15`, `AC17`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
- Steps:
  - Assert workflow-fit guidance appears immediately after the opening purpose/scope paragraphs.
  - Assert workflow-fit guidance appears before Inputs to read, Modes, README behavior, Rules, Output paths, or Failure modes sections.
  - Assert source-of-truth, mode authorization, and existing-vision overwrite protection are consolidated into one edit-authorization section.
  - Assert that section states `CONSTITUTION.md` outranks `vision.md`, `vision.md` outranks README front-matter, create/revise/mirror are the only authorized edit paths, and existing visions are not overwritten without clear revise or mirror intent.
- Expected result:
  - Contributors see the workflow role before details and have one canonical edit-authorization rule to follow.
- Failure proves:
  - The skill can still be skimmed as a normal lifecycle stage or contain repeated, drift-prone edit rules.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T5. README marker behavior remains deterministic and marker-bounded

- Covers: `R10`-`R13`, `R25`-`R26`, `R69`-`R74`, `E1`, `E4`, `AC8`, `AC11`
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
  - Confirm no README mirror helper script is introduced.
- Expected result:
  - README front-matter ownership remains deterministic and does not authorize broad README rewrites.
- Failure proves:
  - The readability cleanup weakened the existing README safety contract.
- Automation location:
  - `scripts/test-skill-validator.py`
  - Manual diff review

### T6. Governance and workflow source boundaries remain aligned

- Covers: `R40`-`R42`, `R46`-`R55`, `AC5`, `AC10`
- Level: contract/manual
- Fixture/setup:
  - `CONSTITUTION.md`
  - `AGENTS.md`
  - `docs/workflows.md`
  - `README.md`
- Steps:
  - Inspect `CONSTITUTION.md` for `vision.md` below `CONSTITUTION.md` and above README front-matter in the vision source-of-truth order.
  - Inspect `AGENTS.md`, `docs/workflows.md`, and README ownership guidance for `vision.md` as the canonical project-vision artifact.
  - Confirm proposal guidance remains summarized as `Vision fit` for proposals created or substantively revised after adoption.
  - Confirm the normal lifecycle chain does not include `vision`.
  - If implementation touches none of these files, record `unaffected with rationale` in the active plan or change-local metadata.
- Expected result:
  - Existing governance and workflow surfaces remain coherent without unnecessary edits.
- Failure proves:
  - The refinement either caused governance drift or made unrelated governance changes without need.
- Automation location:
  - Existing assertions in `scripts/test-skill-validator.py`
  - Manual review of unchanged or changed surfaces

### T7. Proposal and proposal-review Vision fit behavior remains covered

- Covers: `R29`-`R39`, `R75`-`R78`, `E5`, `E6`, `E7`, `AC3`, `AC4`, `AC12`
- Level: contract
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
- Steps:
  - Inspect proposal guidance for a required `Vision fit` section on new and substantively revised proposals after adoption.
  - Inspect the exact allowed values, including `no vision exists yet`.
  - Inspect guidance that prevents silently redefining project vision.
  - Inspect proposal-review guidance for missing-section handling and conflict classification.
  - Inspect explicit exception guidance for owner or stage, evidence, rationale against proposal and vision revision, record location, and future-trigger classification.
  - If implementation touches none of these files, record `unaffected with rationale`.
- Expected result:
  - Proposal-fit behavior remains stable while the vision skill itself is refined.
- Failure proves:
  - The refinement introduced drift in adjacent proposal workflow behavior.
- Automation location:
  - Existing assertions in `scripts/test-skill-validator.py`

### T8. Scope guard prevents unintended project vision or shared-boilerplate changes

- Covers: `R8`, `R20`, `R41`-`R42`, `AC2`, `AC19`, quality-refinement non-goals
- Level: smoke/manual
- Fixture/setup:
  - repository diff for the active plan
  - `vision.md`
  - `README.md`
  - portable skill files
- Steps:
  - Inspect the implementation diff to confirm this refinement does not revise root `vision.md`.
  - Inspect README diff to confirm marker behavior or front-matter content is not changed by this refinement unless a later approved scope explicitly requires it.
  - Confirm no README mirror helper script is introduced.
  - Confirm no shared evidence-collection extraction or cross-skill boilerplate consolidation is included.
  - Confirm editorial and mirror-only changes still do not require a new change-local pack solely because the vision skill ran.
- Expected result:
  - The refinement stays inside the approved vision skill quality scope.
- Failure proves:
  - The implementation crossed a non-goal boundary or conflated this refinement with broader cleanup.
- Automation location:
  - Manual diff review
  - Final `git diff --check -- .`

### T9. Generated Codex and adapter outputs are refreshed only through generators

- Covers: `R43`-`R45`, `AC6`, `AC7`
- Level: integration
- Fixture/setup:
  - canonical `skills/vision/SKILL.md`
  - generated `.codex/skills/vision/SKILL.md`
  - generated `dist/adapters/*/skills/vision/SKILL.md` paths
- Steps:
  - Run `python scripts/build-skills.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1`.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Inspect generated `vision` skill copies for expected canonical changes and no hand-edited drift.
- Expected result:
  - Generated runtime and adapter outputs match the canonical refined skill.
- Failure proves:
  - Distribution surfaces are stale, manually edited, or inconsistent with canonical sources.
- Automation location:
  - Existing generator and adapter commands

### T10. Selector routing continues to cover README marker and lifecycle surfaces

- Covers: `R79`-`R80`, `AC9`
- Level: integration
- Fixture/setup:
  - changed lifecycle, spec, test-spec, skill, generated-output, and change-local paths
  - `README.md`
- Steps:
  - Run selector explicit mode for changed lifecycle and skill paths.
  - Run `python scripts/select-validation.py --mode explicit --path README.md` when README validation is relevant.
  - Run `python scripts/validate-readme.py README.md --vision-markers` when selected or when README markers are present.
  - Confirm no changed path is reported as `unclassified-path`.
- Expected result:
  - Selector-selected validation covers the refinement without broad smoke unless a later authoritative trigger requires it.
- Failure proves:
  - The active validation plan can miss changed surfaces or regress README marker routing.
- Automation location:
  - `python scripts/select-validation.py --mode explicit ...`
  - `python scripts/validate-readme.py README.md --vision-markers`

### T11. Final targeted closeout proves lifecycle, tests, and generated output

- Covers: all requirements and `AC1`-`AC19`
- Level: smoke
- Fixture/setup:
  - all M1-M3 implementation changes
  - `docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`
- Steps:
  - Run `python scripts/validate-skills.py`.
  - Run `python scripts/test-skill-validator.py`.
  - Run `python scripts/build-skills.py --check`.
  - Run `python scripts/test-adapter-distribution.py`.
  - Run `python scripts/build-adapters.py --version 0.1.1 --check`.
  - Run `python scripts/validate-adapters.py --version 0.1.1`.
  - Run `python scripts/validate-change-metadata.py docs/changes/2026-04-30-vision-skill-quality-refinement/change.yaml`.
  - Run lifecycle validation over `docs/plan.md`, the active plan, proposal, spec, test spec, and change metadata.
  - Run `bash scripts/ci.sh --mode explicit` over the changed authoritative paths named in the active plan.
  - Run `git diff --check -- .`.
  - Record commands and results in the active plan validation notes and change-local metadata.
- Expected result:
  - The refinement is ready for first-pass `code-review`; PR and explain readiness remain downstream of code-review and verify.
- Failure proves:
  - The implementation is not ready to leave implementation, even if focused local checks passed earlier.
- Automation location:
  - M3 validation commands in `docs/plans/2026-04-30-vision-skill-quality-refinement.md`

## Fixtures and data

- No new persistent fixtures are required by default.
- Add focused assertions to existing `scripts/test-skill-validator.py` rather than creating a new validator.
- Generated-output tests use existing adapter fixture and distribution checks.
- Skill validation tests use the real canonical `skills/vision/SKILL.md`.
- README proof uses the real `README.md` and marker validation because no mirror helper script is in scope.

## Mocking/stubbing policy

- Do not mock repository-owned validation commands in milestone proof.
- Existing adapter tests may continue using temporary directories and in-process helper calls for generated-output fixtures.
- Do not stub `scripts/build-skills.py`, `scripts/build-adapters.py`, selector behavior, artifact lifecycle validation, or change-metadata validation in final proof.

## Migration or compatibility tests

- Existing proposals remain valid without `Vision fit` until substantively revised; verify by preserving proposal and proposal-review guidance, not by rewriting old proposals.
- Existing README content remains author-owned outside vision markers; verify through skill wording and diff review.
- Existing root `vision.md` remains out of scope for this refinement; verify no refinement diff changes it.
- Generated adapter compatibility is validated through existing adapter distribution, build-check, and adapter validation commands.
- Existing lifecycle order remains unchanged; verify the skill and workflow guidance do not insert `vision` into the normal lifecycle chain.

## Observability verification

- The skill's required user-facing run output is verified by contract text: mode used, files changed, README front-matter action, create-mode assumptions, revise-mode sections changed, mirror-mode unchanged `vision.md`, and R94 causal-link status for substantive revisions.
- No runtime logs, metrics, traces, or audit events are introduced.
- Final implementation evidence is recorded through plan validation notes and change-local metadata.

## Security/privacy verification

- Inspect the `vision` skill for sensitive-information exclusions and confirmation behavior before public inclusion.
- Inspect the `vision` skill for the external research boundary and researched-fact versus assumption reporting.
- Confirm new drafting heuristics do not encourage publishing secrets, private local paths, private machine names, personal data, or unrequested external facts.

## Performance checks

- No runtime performance behavior is introduced.
- Evidence collection performance remains covered by bounded-read guidance in the skill and existing workflow output-budget guidance.
- Do not add broad scans beyond the active plan's explicit validation commands unless a later authoritative trigger requires broad smoke.

## Manual QA checklist

- Confirm workflow-fit guidance appears before detailed mode mechanics.
- Confirm mode behavior is represented by exactly one Markdown table with the required columns and one row per mode.
- Confirm edit authorization is consolidated and does not weaken overwrite protection.
- Confirm drafting heuristics are questions or checks and not new `vision.md` sections.
- Confirm competitor naming remains optional.
- Confirm revise-mode traceability no longer uses soft "remind" wording for substantive revisions tied to a change-local pack.
- Confirm root `vision.md` and README front-matter are not revised by this refinement.
- Confirm generated skill and adapter copies match canonical skill output.

## What not to test

- Do not run actual `vision create`, `vision revise`, or `vision mirror` as an external agent workflow; this slice tests the skill contract text.
- Do not create, revise, or validate root `vision.md` content as part of this refinement.
- Do not test a README mirror helper script; no helper script is in scope.
- Do not rewrite legacy proposals to add `Vision fit`.
- Do not test external Codex, Claude Code, or opencode execution.
- Do not fetch external research for vision drafting.
- Do not score generated vision prose quality with a validator; assert the required drafting heuristics instead.
- Do not extract or consolidate shared evidence-collection boilerplate across skills.

## Uncovered gaps

- None. Requirements are covered by focused skill assertions, contract inspection, existing repository-owned validation commands, generated-output integration checks, selector inspection, manual diff review, or final lifecycle closeout validation.

## Next artifacts

- `code-review` for the completed M1-M3 implementation in `docs/plans/2026-04-30-vision-skill-quality-refinement.md`.
- `verify` after code-review is clean or findings are resolved.
- `explain-change` and `pr` after verify reports branch readiness.

## Follow-on artifacts

- `plan-review`: approved on 2026-04-30 with no material findings.
- Implementation: M1-M3 are complete and final implementation proof is recorded in the active plan and change-local evidence.

## Readiness

This test spec is the active proof map for the 2026-04-30 vision skill quality refinement.

Immediate next repository stage: `code-review` for the completed M1-M3 implementation in `docs/plans/2026-04-30-vision-skill-quality-refinement.md`.
