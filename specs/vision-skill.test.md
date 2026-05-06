# Vision Skill Test Spec

## Status

- active

## Related spec and plan

- Spec: [Vision Skill](vision-skill.md), approved after `spec-review-r3` on 2026-05-06.
- Active plan: [2026-05-06 Optimize Vision Skill Strategic Positioning Quality](../docs/plans/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md).
- Related proposal: [Optimize Vision Skill Strategic Positioning Quality](../docs/proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md), accepted on 2026-05-06.
- Historical migration spec: [Vision Skill Simplification and VISION.md Migration](vision-skill-simplification-and-vision-md-migration.md), approved after spec-review on 2026-05-01.
- Prior proposals: [Vision Skill](../docs/proposals/2026-04-29-vision-skill.md), [Vision Skill Quality Refinement](../docs/proposals/2026-04-30-vision-skill-quality-refinement.md), and [Vision Skill Simplification and VISION.md Migration](../docs/proposals/2026-05-01-vision-skill-simplification-and-vision-md-migration.md).
- Architecture: not required. The active change updates workflow-governance guidance, skill instructions, selector routing, static assertions, generated skill output, generated adapter output, and durable rationale artifacts without introducing a runtime boundary, data store, network integration, deployment boundary, schema, or release package behavior.
- Spec-review findings: `SR1-F1` and `SR2-F1` closed the 900-word hard-cap ambiguity; `spec-review-r3` approved the spec with no findings.
- Plan-review findings: approved on 2026-05-06 with no material findings. The minor validation note about the expected `vision.md` selector result is captured in `T8`.

## Testing strategy

- Contract tests inspect authored Markdown for canonical `VISION.md` source-of-truth wording, state-based `vision` behavior, proposal `Vision fit` behavior, strategic-positioning guidance, retired lowercase path behavior, security boundaries, and output reporting.
- Selector unit tests prove root `VISION.md` remains routed to repository-owned validation and root `vision.md` is no longer classified as a supported vision surface, migration input, root-vision conflict participant, or no-vision exception.
- Fixture-style static assertions cover three strategic-positioning cases: methodology-as-product, ordinary product with implementation substrate, and true substrate product.
- Rationale-artifact proof checks `docs/vision/strategic-positioning.md` creation/update/no-update rules, authority wording, required compact sections, and change-local linkage for substantive repositioning.
- README validation preserves marker-bounded front-matter derived from `VISION.md`.
- Generated-output integration uses existing repository generators so `.codex/skills/` and `dist/adapters/` remain derived from canonical `skills/`.
- Lifecycle and metadata proof keeps the accepted proposal, approved spec, active test spec, active plan, review records, and change-local metadata coherent.
- No prompt-output scoring harness is added in this slice; quality is tested through static assertions and manual review against the approved contract.

## Requirement coverage map

| Requirement IDs | Test IDs | Notes |
| --- | --- | --- |
| `R1`-`R8` | `T1`, `T8`, `T11` | Canonical path, source order, README source boundary, active lowercase retirement, and historical-reference scope. |
| `R9`-`R19` | `T2`, `T9` | Canonical authored skill metadata, state-based interface, legacy intent words, and required output reporting. |
| `R20`-`R31` | `T2`, `T4` | Establishment, update, sync, overwrite protection, substantive/editorial classification, causal-link gates, and explicit retired lowercase requests. |
| `R32`-`R32b` | `T3`, `T5`, `T10` | 750-word normal cap, owner-authorized methodology allowance, and hard 900-word maximum. |
| `R33`-`R39` | `T3`, `T5` | Plain language, no requirements vocabulary in generated vision text, no feature lists or implementation details, default sections, plain Markdown, and drafting heuristics. |
| `R40`-`R48` | `T6`, `T10`, `T12` | README marker pair, generated front-matter contents, marker insertion limits, sync boundaries, and no helper script. |
| `R49`-`R62` | `T7` | Proposal and proposal-review `Vision fit` behavior against `VISION.md`, including explicit exception rules. |
| `R63`-`R67` | `T1`, `T8`, `T9`, `T12` | Workflow boundary, generated-output ownership, selector routing for `VISION.md`, and retired lowercase selector behavior. |
| `R68`-`R72` | `T3` | Publication safety, research boundaries, researched-fact reporting, and bounded evidence collection. |
| `R73`-`R79` | `T4`, `T10`, `T11` | Strategic-positioning pass, durable rationale artifact, authority wording, editorial no-update rule, and change-local rationale link. |
| `R80`-`R86` | `T5`, `T10` | Anti-anchor rule, methodology-as-product, optional methodology section guard, first-sentence category, opening-section answerability, and final quality gates. |

## Example coverage map

| Example | Test IDs | Notes |
| --- | --- | --- |
| `E1` | `T2`, `T4`, `T6` | Establishing the first vision creates `VISION.md`, creates positioning rationale, and may insert README markers. |
| `E2` | `T2` | Skill installation or ordinary README maintenance does not create `VISION.md`. |
| `E3` | `T2` | Existing vision updates remain bounded and classified. |
| `E4` | `T2`, `T6` | README sync leaves `VISION.md` unchanged and touches only marker-bounded content. |
| `E5` | `T7` | Proposal guidance requires `Vision fit` when a vision exists. |
| `E6` | `T7` | Proposal guidance handles the no-vision state. |
| `E7` | `T7` | Proposal-review classifies vision conflicts. |
| `E8` | `T2` | Legacy mode words are intent hints only. |
| `E9` | `T5` | Methodology project leads with the workflow category and treats Git/CI as compatibility surfaces. |
| `E10` | `T5` | Ordinary implementation substrate does not become the headline. |
| `E11` | `T5` | True substrate products may lead with the substrate. |
| `E12` | `T4`, `T10` | Material repositioning updates rationale and reports positioning summary/path. |
| `E13` | `T4` | Editorial updates leave rationale untouched unless assumptions change or conflict appears. |

## Edge case coverage

- Root `vision.md` exists and root `VISION.md` does not: `T2`, `T7`, `T8`
- Root `VISION.md` exists and root `vision.md` also exists: `T2`, `T8`
- Neither root vision file exists and README already has markers: `T2`, `T6`, `T7`
- Root `VISION.md` exists and README lacks markers: `T6`
- README contains malformed, nested, or multiple marker pairs: `T6`
- Proposal says `fits the current vision` while root `VISION.md` does not exist: `T7`
- Proposal omits `Vision fit` after adoption: `T7`
- Vision update changes scope but is labeled editorial: `T2`, `T4`
- User asks to update vision but names no section or direction: `T2`
- User asks to read, edit, merge, delete, or migrate root `vision.md` as project vision: `T2`
- README sync finds front-matter already current: `T6`
- Historical artifact references lowercase `vision.md`: `T1`
- RigorLoop-style methodology input mentions Git and CI: `T5`
- Ordinary product input mentions implementation substrate: `T5`
- True substrate product input describes a Git extension: `T5`
- Material repositioning changes category or promise: `T4`, `T10`
- Editorial wording update does not change strategy: `T4`
- Generated or revised `VISION.md` exceeds 750 words without owner authorization: `T3`
- Generated or revised `VISION.md` exceeds 900 words: `T3`
- Methodology-oriented section lacks concrete input pillars or operating loop: `T5`

## Acceptance criteria coverage map

| Acceptance criterion | Test IDs | Notes |
| --- | --- | --- |
| `AC1` | `T1`, `T8`, `T11` | Root `VISION.md` is canonical. |
| `AC2` | `T2`, `T9` | The `vision` skill validates and uses state-based behavior. |
| `AC3` | `T2`, `T6` | Establishment, update, and README sync remain safe. |
| `AC4` | `T2`, `T4`, `T10` | Substantive/editorial confirmation and causal-link gates remain present. |
| `AC5` | `T6`, `T10`, `T12` | README front-matter links to `VISION.md` and remains marker-bounded. |
| `AC6` | `T7` | Proposal guidance requires `Vision fit` against `VISION.md`. |
| `AC7` | `T7` | Proposal-review checks fit and explicit exceptions. |
| `AC8` | `T1` | Normal lifecycle chain does not require `vision`. |
| `AC9` | `T1`, `T7`, `T8` | Active guidance and validation retire lowercase `vision.md` migration behavior. |
| `AC10` | `T2`, `T3`, `T6`, `T9` | Still-valid safety and quality rules remain present. |
| `AC11` | `T4`, `T5` | Initial and materially repositioned visions are grounded in strategic positioning. |
| `AC12` | `T4`, `T10` | Initial and materially repositioned visions create or update supporting rationale while keeping `VISION.md` canonical. |
| `AC13` | `T5` | Compatibility surfaces do not become project identity unless justified. |
| `AC14` | `T5` | Methodology projects can include justified methodology pillars or one optional section. |
| `AC15` | `T3`, `T10` | Generated and revised visions obey 750/900-word policy. |
| `AC16` | `T4` | Final skill output reports positioning summary and rationale path when relevant. |

## Test cases

### T1. Canonical `VISION.md`, governance alignment, and active lowercase retirement

- Covers: `R1`-`R8`, `R63`, `AC1`, `AC8`, `AC9`
- Level: contract/manual
- Fixture/setup:
  - `CONSTITUTION.md`, `AGENTS.md`, `docs/workflows.md`, `README.md`
  - `specs/vision-skill.md`, `specs/vision-skill.test.md`
  - `skills/vision/SKILL.md`, `skills/proposal/SKILL.md`, `skills/proposal-review/SKILL.md`
- Steps:
  - Assert active governance, workflow, README, proposal, proposal-review, vision-skill guidance, and repository validation name root `VISION.md` as the canonical project-vision artifact.
  - Assert `CONSTITUTION.md` outranks `VISION.md`.
  - Assert README front-matter is generated from `VISION.md` and is not independently authoritative.
  - Assert active guidance does not describe root `vision.md` as canonical, migration input, a supported project-vision surface, a root-vision conflict participant, or a no-vision exception.
  - Inspect the diff to confirm historical proposals, specs, plans, reviews, change-local artifacts, and PR records are not rewritten solely to replace archival lowercase text.
  - Confirm the normal lifecycle chain still keeps `vision` upstream and does not add it as a mandatory per-change stage.
- Expected result:
  - Active surfaces use `VISION.md`, historical lowercase mentions remain archival only, and `vision` remains outside the normal lifecycle chain.
- Failure proves:
  - The repository still has conflicting active source-of-truth or lifecycle guidance for project vision.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - Manual diff review for historical non-rewrite scope

### T2. Vision skill state-based interface and safe edit boundaries

- Covers: `R9`-`R31`, `E1`-`E4`, `E8`, `AC2`-`AC4`, `AC10`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md` after M2
- Steps:
  - Assert the canonical authored skill remains under `skills/vision/SKILL.md` with metadata `name: vision`.
  - Assert the skill description says it produces or updates project vision and matching README front-matter.
  - Assert the skill uses state-based behavior and ordinary user intent instead of requiring or reporting user-facing `create`, `revise`, or `mirror` modes.
  - Assert every run reports changed files and README front-matter action.
  - Assert establishment output reports assumptions and open vision-level questions.
  - Assert update output reports changed sections and `substantive` or `editorial` classification.
  - Assert README-only sync output reports `VISION.md` unchanged.
  - Assert initial `VISION.md` creation requires explicit establishment intent and is not triggered by skill installation or ordinary README maintenance.
  - Assert missing `VISION.md` without establishment intent stops for clarification.
  - Assert existing-vision updates are bounded to requested or clearly related sections, and unclear update intent stops before editing.
  - Assert substantive updates tied to a change-local pack require `change.yaml` and `explain-change.md` causal links before finalizing.
  - Assert editorial updates and README-only sync do not create a change-local pack solely because the skill ran.
  - Assert the skill does not silently overwrite existing `VISION.md`.
  - Assert requests to read, edit, merge, delete, or migrate retired root `vision.md` as project vision stop with a canonical-path explanation unless the owner separately gives a non-vision-file instruction.
- Expected result:
  - The skill remains state-based, bounded, traceable, and explicit about retired lowercase path handling.
- Failure proves:
  - The skill interface or edit-boundary contract drifted from the approved state-based model.
- Automation location:
  - `python scripts/validate-skills.py skills/vision/SKILL.md`
  - Focused assertions in `scripts/test-skill-validator.py`
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`

### T3. Vision content safety, word-budget policy, and publication boundaries

- Covers: `R32`-`R39`, `R68`-`R72`, edge behavior for 750/900-word limits, `AC10`, `AC15`
- Level: contract/manual
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - `specs/vision-skill.md`
  - `VISION.md` when this change revises project vision content
- Steps:
  - Assert generated or revised `VISION.md` normally stays at or under 750 words.
  - Assert methodology, protocol, workflow, or operating-model visions may exceed 750 words only when the owner explicitly allows it and the extra length is needed for category, methodology pillars, tradeoff, refusals, or falsifiability.
  - Assert generated or revised `VISION.md` over 900 words is invalid and must be shortened before completion.
  - Assert generated or revised vision prose uses plain language and does not use `MUST`, `SHOULD`, or `MAY` as requirements vocabulary.
  - Assert generated or revised vision prose excludes implementation details, architecture diagrams, status fields, decision logs, stakeholder tables, priority columns, and feature lists.
  - Assert generated or revised vision prose keeps concise sections for pitch, differentiator, target audience, non-audience, commitments, refusals, falsifiability, and optional open questions.
  - Assert `VISION.md` remains readable as plain Markdown without tables, diagrams, HTML layout, or generated assets.
  - Assert drafting heuristics and positioning guidance remain authoring questions, checks, or pre-drafting steps rather than required `VISION.md` worksheet sections except where `R82` allows one methodology-oriented section.
  - Assert the skill still excludes secrets, credentials, private local filesystem paths, private machine names, and unintended personal data.
  - Assert external research is not fetched unless the user explicitly requests research or a research-backed workflow invokes it, and researched facts are distinguished from assumptions when used.
  - Assert compact project inputs are preferred and full-file reads are reserved for missing, conflicting, or insufficient compact inputs.
- Expected result:
  - Vision prose remains concise, safe to publish, non-requirements-like, and bounded by the approved word policy.
- Failure proves:
  - The skill can generate visions that are too long, too implementation-heavy, unsafe to publish, or not governed by the approved quality contract.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - Manual word count for changed `VISION.md` when the implementation revises it:

    ```bash
    python -c "from pathlib import Path; import re; print(len(re.findall(r'\\S+', Path('VISION.md').read_text(encoding='utf-8'))))"
    ```

### T4. Strategic-positioning pass and durable rationale behavior

- Covers: `R73`-`R79`, `E1`, `E12`, `E13`, `AC11`, `AC12`, `AC16`
- Level: contract/manual
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - `docs/vision/strategic-positioning.md`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md` after M2
- Steps:
  - Assert the skill performs a strategic-positioning pass before drafting an initial `VISION.md` or materially repositioning an existing `VISION.md`.
  - Assert the pass identifies project category, primary user, primary pain, primary promise, core mechanism, alternatives, tradeoff, compatibility surfaces, refusals, and falsifiability.
  - Assert initial visions and material repositioning write the pass to `docs/vision/strategic-positioning.md`.
  - Assert `docs/vision/strategic-positioning.md` contains compact sections for the ten strategic-positioning fields.
  - Assert the rationale states that `VISION.md` is canonical and that the positioning rationale does not independently override it.
  - Assert conflicts between the rationale and `VISION.md` are resolved by updating the rationale or revising `VISION.md` through a substantive update, not by treating the rationale as authoritative.
  - Assert editorial vision updates, README-only sync, and narrow section edits do not update `docs/vision/strategic-positioning.md` unless strategic assumptions changed or a conflict appears.
  - Assert substantive repositioning in a repository with a change-local pack requires `explain-change.md` to summarize the positioning delta and link to `docs/vision/strategic-positioning.md`.
  - Assert final output for initial or materially repositioned visions reports a concise strategic-positioning summary and the rationale path.
- Expected result:
  - The strategic-positioning pass is durable when it shapes the vision, remains supporting rather than authoritative, and is quiet for editorial work.
- Failure proves:
  - The skill either loses important vision rationale or turns the rationale worksheet into a competing vision source.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/vision/strategic-positioning.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md`
  - Manual diff review for editorial no-update behavior when applicable

### T5. Strategic category fixtures, anti-anchor rule, and final quality gates

- Covers: `R80`-`R86`, `E9`-`E11`, `AC13`, `AC14`
- Level: contract
- Fixture/setup:
  - `skills/vision/SKILL.md`
  - Fixture text embedded in `scripts/test-skill-validator.py`
- Steps:
  - Assert the skill treats repository layout, Git, CI, pull requests, runtime, package format, hosting platform, language, and template mechanics as compatibility surfaces unless the owner explicitly chooses one as the project category or the substrate is genuinely the product.
  - Assert methodology, workflow, protocol, and operating-model pillars are project identity when the methodology is the product.
  - Assert methodology-oriented sections are allowed at most once and only when available inputs identify concrete methodology pillars or an operating loop.
  - Assert insufficient methodology detail keeps the standard section structure and becomes an open vision-level question rather than invented methodology content.
  - Assert a RigorLoop-style fixture leads with an AI-agent engineering workflow or methodology category, treats Git and CI as compatibility surfaces, includes methodology pillars as the core mechanism, and does not make `Git-first starter kit` the category.
  - Assert a Windows-native file manager fixture leads with the user-facing file-manager product category and does not over-center WinUI, MSIX, or Shell APIs unless the substrate is part of the differentiator.
  - Assert a Git-extension fixture may lead with Git because Git is the actual product category.
  - Assert final quality gates require the first sentence to name the highest-level category, the differentiator to include a tradeoff, core mechanism to appear when essential, compatibility surfaces not to dominate identity, audience non-fit to be visible, commitments to be checkable, refusals to block scope creep, falsifiability to be observable, and proposal-fit review to work without chat history.
- Expected result:
  - The skill produces strategic-positioning guidance that generalizes beyond RigorLoop and resists substrate anchoring.
- Failure proves:
  - The revised skill can regress to low-level framing while remaining structurally valid.
- Automation location:
  - Focused fixture-style assertions in `scripts/test-skill-validator.py`

### T6. README front-matter remains marker-bounded and derived from `VISION.md`

- Covers: `R40`-`R48`, `E1`, `E4`, `AC3`, `AC5`, `AC10`
- Level: contract/integration
- Fixture/setup:
  - `README.md`
  - `skills/vision/SKILL.md`
  - temporary README fixtures for malformed, nested, missing, and multiple marker pairs when the validator needs file-level fixtures
- Steps:
  - Assert the marker pair is exactly `<!-- vision:start -->` and `<!-- vision:end -->`.
  - Assert generated front-matter includes only pitch, differentiator, target audience, and a link to `VISION.md` for goals, non-goals, and falsifiability.
  - Assert README front-matter is derived from `VISION.md`.
  - Assert automatic marker insertion is allowed only when creating the initial `VISION.md`.
  - Assert existing valid marker blocks are replaced only inside the marker block.
  - Assert missing, malformed, nested, or multiple marker pairs stop update or sync unless explicitly authorized.
  - Assert authorized marker insertion preserves README content order and uses the deterministic location defined by the skill.
  - Assert the skill does not edit README content outside the marker block except for allowed marker insertion.
  - Assert no required README synchronization helper script is added.
- Expected result:
  - README front-matter stays generated, marker-bounded, and subordinate to `VISION.md`.
- Failure proves:
  - README synchronization can corrupt user-authored README content or make README the vision source of truth.
- Automation location:
  - `python scripts/validate-readme.py README.md --vision-markers`
  - Focused assertions in `scripts/test-skill-validator.py`

### T7. Proposal and proposal-review `Vision fit` behavior against canonical vision

- Covers: `R49`-`R62`, `E5`-`E7`, `AC6`, `AC7`, `AC9`
- Level: contract
- Fixture/setup:
  - `skills/proposal/SKILL.md`
  - `skills/proposal-review/SKILL.md`
  - `VISION.md` presence/absence scenarios described in static guidance
- Steps:
  - Assert proposal guidance reads root `VISION.md` when present as the canonical project-vision reference.
  - Assert every new or substantively revised proposal requires a `Vision fit` section.
  - Assert legacy proposals that are not substantively revised are not invalid solely because they reference `vision.md` or lack `Vision fit`.
  - Assert the first non-empty line of `Vision fit` is exactly one allowed status value.
  - Assert `no vision exists yet` is forbidden when root `VISION.md` exists.
  - Assert `no vision exists yet` is required when root `VISION.md` does not exist.
  - Assert retired root `vision.md` does not prevent `Vision fit` from using `no vision exists yet` when root `VISION.md` is absent.
  - Assert proposal guidance does not silently redefine project vision outside `Vision fit` and normal proposal rationale.
  - Assert proposal-review checks `Vision fit`, requests revision when required, and classifies conflicts as revise proposal, revise vision, or record explicit exception.
  - Assert explicit exceptions contain the owner or owning stage, conflict evidence, rationale for not revising proposal, rationale for not revising vision, recording location, one-time or ongoing scope, and mirrored record in proposal plus review output.
  - Assert active proposal and proposal-review guidance no longer preserves migration-recognized lowercase `vision.md` exceptions.
- Expected result:
  - Proposal fit is checked against root `VISION.md`; retired lowercase files do not masquerade as a project vision.
- Failure proves:
  - Proposal workflow can proceed with stale, missing, or conflicting vision-fit assumptions.
- Automation location:
  - Focused assertions in `scripts/test-skill-validator.py`

### T8. Selector routing for canonical `VISION.md` and negative proof for retired `vision.md`

- Covers: `R7`, `R66`-`R67`, `AC1`, `AC9`
- Level: unit/integration
- Fixture/setup:
  - `scripts/validation_selection.py`
  - `scripts/test-select-validation.py`
  - temporary repositories for root-file presence and PR-mode fixtures
- Steps:
  - Assert explicit-mode selection for root `VISION.md` classifies it as category `vision`, exits successfully, selects README vision marker validation, and has no unclassified path.
  - Assert PR-mode selection for root `VISION.md` does the same.
  - Assert explicit-mode selection for root `vision.md` is a negative proof: it must not classify the path as category `vision`, must not select README vision marker validation solely for that path, must not report `vision-path-conflict`, and must fail or block as an unsupported or unclassified path.
  - Assert PR-mode reintroduction of root `vision.md` is not treated as a supported root vision change or migration input.
  - Assert root `vision.md` presence does not create a root-vision conflict with `VISION.md` and does not block unrelated changed paths through global conflict detection.
  - Assert selector-selected CI for changed vision-skill surfaces still routes deterministic repository-owned checks.
- Expected result:
  - Root `VISION.md` stays supported, while root `vision.md` is retired from active selector and validation behavior.
- Failure proves:
  - The repository still carries active lowercase migration behavior or loses canonical `VISION.md` routing.
- Automation location:
  - `python scripts/test-select-validation.py`
  - Positive manual selector proof:

    ```bash
    python scripts/select-validation.py --mode explicit --path VISION.md
    ```

  - Negative manual selector proof. Expected result: nonzero selector status with `vision.md` reported as unsupported or unclassified, not as a selected vision surface:

    ```bash
    python scripts/select-validation.py --mode explicit --path vision.md
    ```

### T9. Generated skill and adapter output stays derived from canonical skills

- Covers: `R64`-`R65`, generated-output portions of `R9`-`R11`, `AC2`, `AC10`
- Level: integration
- Fixture/setup:
  - canonical skill files under `skills/`
  - generated Codex runtime mirrors under `.codex/skills/`
  - generated public adapter output under `dist/adapters/`
  - repository generators
- Steps:
  - Run `python scripts/build-skills.py` after canonical skill changes.
  - Run `python scripts/build-adapters.py --version 0.1.1` after generated skill output changes.
  - Inspect generated diffs for expected `vision`, `proposal`, and `proposal-review` propagation only.
  - Run drift checks to prove generated output is derived from canonical skills.
  - Run adapter validation to prove public adapter packages remain installable and internally consistent.
- Expected result:
  - Generated runtime and adapter surfaces match canonical authored skill guidance with no hand edits.
- Failure proves:
  - Users of generated skill packages may receive a different vision contract than the canonical repository source.
- Automation location:
  - `python scripts/validate-skills.py`
  - `python scripts/build-skills.py --check`
  - `python scripts/test-adapter-distribution.py`
  - `python scripts/build-adapters.py --version 0.1.1 --check`
  - `python scripts/validate-adapters.py --version 0.1.1`

### T10. Current RigorLoop material repositioning has durable rationale

- Covers: `R74`-`R79`, `R84`-`R86`, `AC4`, `AC12`, `AC15`
- Level: manual/contract
- Fixture/setup:
  - `VISION.md`
  - `README.md`
  - `CONSTITUTION.md`
  - `docs/vision/strategic-positioning.md` after M2
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md` after M2
- Steps:
  - Confirm the current RigorLoop `VISION.md` first sentence leads with the higher-level AI-agent software engineering workflow category.
  - Confirm Git, CI, and pull requests appear as compatibility surfaces rather than the project headline.
  - Confirm methodology pillars appear as the core mechanism where needed.
  - Confirm `VISION.md` is at or under the approved 900-word hard cap.
  - Confirm README front-matter and `CONSTITUTION.md` remain aligned with the accepted higher-level project category.
  - Confirm `docs/vision/strategic-positioning.md` exists, includes all required compact sections, and states its supporting authority relationship to `VISION.md`.
  - Confirm change-local `explain-change.md` summarizes the positioning delta and links to `docs/vision/strategic-positioning.md`.
- Expected result:
  - The current branch's material project-vision repositioning is durable, reviewable, and not only present in chat or final output.
- Failure proves:
  - The branch updated public vision language without recording the required strategic rationale.
- Automation location:
  - Manual diff review
  - `python scripts/validate-readme.py README.md --vision-markers`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path VISION.md --path README.md --path CONSTITUTION.md --path docs/vision/strategic-positioning.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/explain-change.md`

### T11. Change metadata, lifecycle state, and review closeout remain coherent

- Covers: lifecycle proof for all requirements implemented by the active plan
- Level: integration
- Fixture/setup:
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-log.md`
  - `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-resolution.md`
  - detailed review records under `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/reviews/`
  - `docs/plan.md`
  - active plan body
- Steps:
  - Validate change metadata after adding test-spec, skill, selector, rationale, generated-output, and explanation paths.
  - Validate review artifact closeout remains closed unless a later formal review opens material findings.
  - Validate artifact lifecycle over touched proposal, spec, test spec, plan, review, rationale, and change-local artifacts.
  - Confirm `docs/plan.md` and the plan body move lifecycle state together when the plan closes.
- Expected result:
  - Review findings remain closed, lifecycle artifacts agree, and the change-local pack lists the surfaces used to prove the change.
- Failure proves:
  - The branch is not review-ready even if individual skill and selector tests pass.
- Automation location:
  - `python scripts/validate-change-metadata.py docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml`
  - `python scripts/validate-review-artifacts.py --mode closeout docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality`
  - `python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path docs/plan.md --path docs/plans/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md --path docs/proposals/2026-05-06-optimize-vision-skill-strategic-positioning-quality.md --path specs/vision-skill.md --path specs/vision-skill.test.md --path docs/vision/strategic-positioning.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-log.md --path docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/review-resolution.md`

### T12. Final selected CI proof covers authored, selector, generated, and lifecycle surfaces

- Covers: final integration proof for the active execution plan
- Level: smoke/integration
- Fixture/setup:
  - all files changed by M1 through M4
  - selector-selected check catalog
- Steps:
  - Run selector inspection for the final changed path set.
  - Run targeted CI with explicit changed paths for authored skill guidance, generated skill output, generated adapter output, selector/test surfaces, README, `VISION.md`, strategic rationale, plan, and change-local metadata.
  - Run whitespace checks over the final diff.
  - Run broad smoke only if an authoritative trigger appears later in the plan, test spec, review-resolution, release metadata, selector output, or maintainer request.
- Expected result:
  - The repository-owned selected validation proves the changed surfaces without requiring broad smoke by default.
- Failure proves:
  - The planned proof is incomplete or the selector no longer routes this workflow-governance change safely.
- Automation location:
  - `python scripts/select-validation.py --mode explicit --path <final changed paths>`
  - `bash scripts/ci.sh --mode explicit --path <final changed paths>`
  - `git diff --check -- .`
  - targeted trailing-whitespace scan when needed:

    ```bash
    rg -n '[[:blank:]]$|\t' <final changed paths>
    ```

## Fixtures and data

- `skills/vision/SKILL.md` is the canonical authored skill fixture for state-based vision behavior, strategic-positioning guidance, README marker rules, security boundaries, and output reporting.
- `skills/proposal/SKILL.md` and `skills/proposal-review/SKILL.md` are the canonical authored fixtures for `Vision fit` behavior.
- `specs/vision-skill.md` is the approved contract fixture.
- `specs/vision-skill.test.md` is this active proof map and participates in static assertion coverage.
- `scripts/test-skill-validator.py` owns static assertions over authored skill and governing Markdown.
- `scripts/test-select-validation.py` owns selector unit tests and temporary repository fixtures.
- `README.md` is the live marker-bounded front-matter fixture.
- `VISION.md` is the canonical project-vision fixture for the current material repositioning.
- `docs/vision/strategic-positioning.md` is created during M2 as the durable rationale fixture for the current material repositioning.
- `docs/changes/2026-05-06-optimize-vision-skill-strategic-positioning-quality/change.yaml` and `explain-change.md` are the change-local traceability fixtures for this initiative.
- Generated `.codex/skills/` and `dist/adapters/` files are fixtures only after generator execution; they must not be edited by hand.

## Mocking/stubbing policy

- Skill and proposal guidance tests inspect real authored Markdown, not full-file snapshots.
- Strategic-positioning fixtures may be embedded as compact static text in `scripts/test-skill-validator.py`; they do not require running an external AI agent.
- Selector PR-mode tests may use temporary local Git repositories instead of real repository history.
- README marker tests may use temporary README files for malformed, missing, nested, multiple, and valid marker cases.
- Generated-output checks must use real repository generators rather than mocked generated files.
- No network, hosted CI, external Codex, Claude Code, opencode, or prompt-output execution is mocked or required.

## Migration or compatibility tests

- `T1` proves active guidance has completed the uppercase migration while preserving historical lowercase references as archival.
- `T2` proves explicit user requests about retired root `vision.md` stop unless the owner separately asks to handle it as an ordinary non-vision file.
- `T7` proves retired root `vision.md` does not prevent `Vision fit` from using `no vision exists yet` when root `VISION.md` is absent.
- `T8` is the active selector migration boundary: root `VISION.md` is supported; root `vision.md` is a negative unsupported-path proof, not a migration route or conflict participant.
- No new rename migration test is required in this slice because the root file rename was completed by the prior migration plan.

## Observability verification

- `T2` verifies user-facing `vision` output fields by contract text: changed files, README front-matter action, assumptions or open questions, sections changed, revision classification, and `VISION.md` unchanged for README-only sync.
- `T4` verifies strategic-positioning summary and rationale path reporting for initial or materially repositioned visions.
- `T5` verifies final quality gate reporting by contract text.
- `T10` verifies change-local rationale for the current material repositioning.
- No runtime logs, metrics, traces, or audit events are introduced.

## Security/privacy verification

- `T3` verifies sensitive-information exclusion, research boundaries, researched-fact versus assumption reporting, plain Markdown readability, and bounded-read behavior.
- Manual diff review confirms generated README front-matter and `VISION.md` do not introduce secrets, credentials, private local filesystem paths, private machine names, or unintended personal data.
- No external research is required for ordinary execution of this change.

## Performance checks

- No runtime performance behavior is introduced.
- Evidence collection remains bounded through the existing workflow and skill guidance.
- Static assertions and selector tests should remain fast enough for selected CI; do not add a prompt-output harness or broad smoke by default.
- Run broad smoke only when selector output, this test spec, review-resolution, release metadata, active plan state, or explicit maintainer request requires it.

## Manual QA checklist

- Confirm `VISION.md` is the only supported root project-vision artifact in active guidance.
- Confirm root `vision.md` is not classified as a supported vision surface, migration input, conflict participant, or no-vision exception.
- Confirm `VISION.md` first sentence names the AI-agent software engineering workflow category for the current RigorLoop repositioning.
- Confirm `VISION.md` is at or under 900 words after any generated or revised content.
- Confirm README front-matter links to `VISION.md` and content outside markers is preserved.
- Confirm `docs/vision/strategic-positioning.md` contains the ten compact positioning sections and authority wording.
- Confirm `explain-change.md` summarizes the positioning delta and links to the rationale artifact after M2.
- Confirm generated `.codex/skills/` and `dist/adapters/` diffs are produced only by generator commands.
- Confirm `docs/plan.md` and the plan body stay synchronized when lifecycle state changes.

## What not to test

- Do not run an external AI agent to score generated vision prose; this slice uses static assertions and manual review instead.
- Do not add a prompt-output quality harness.
- Do not require a README synchronization helper script.
- Do not rewrite historical proposals, specs, plans, reviews, change-local artifacts, or PR records solely to replace old lowercase `vision.md` text.
- Do not test external Codex, Claude Code, or opencode execution.
- Do not add runtime performance, UI, network, storage, deployment, or release-package tests.
- Do not force every project into a RigorLoop methodology fixture; keep the three fixture categories distinct.
- Do not treat `docs/vision/strategic-positioning.md` as independently authoritative over `VISION.md`.

## Uncovered gaps

None. Requirements are covered by focused skill assertions, selector unit tests, README marker validation, generated-output drift checks, adapter validation, lifecycle validation, change metadata validation, manual rationale review, or final selected CI proof.

## Next artifacts

- `implement` M1: update `scripts/test-skill-validator.py`, `scripts/test-select-validation.py`, and `scripts/validation_selection.py` against this active proof map.
- `implement` M2: update canonical skill guidance and create `docs/vision/strategic-positioning.md`.
- `implement` M3: refresh generated skill and adapter output through repository generators.
- `implement` M4: synchronize lifecycle closeout and final validation evidence.
- `code-review`
- `verify`
- `explain-change`
- `pr`

## Follow-on artifacts

- `proposal-review`: approved on 2026-05-06 after `PR-1` clarified lowercase `vision.md` retirement scope.
- `spec-review`: approved on 2026-05-06 after `SR1-F1` and `SR2-F1` fixed the 900-word hard cap and matching boundary behavior.
- `plan-review`: approved on 2026-05-06 with no material findings; minor selector-command expectation note captured in `T8`.

## Readiness

This test spec is the active proof map for the approved `vision` skill strategic-positioning contract and retired lowercase `vision.md` behavior.

Immediate next repository stage: `implement` M1 for proof-map static assertions and selector behavior. Implementation should not skip directly to canonical skill text changes before M1 assertions and selector tests are in place.
