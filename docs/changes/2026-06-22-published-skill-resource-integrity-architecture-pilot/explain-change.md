# Published Skill Resource Integrity Explain Change

## Summary

This change makes published skill-local resources explicit, packageable, and
verifiable across the canonical, generated, packed, and installed skill chain.

The concrete incident was the architecture skill: installed
`.agents/skills/architecture/SKILL.md` referenced `templates/architecture.md`,
`templates/diagram-styles.mmd`, and `templates/adr.md`, but the installed skill
directory contained only `SKILL.md`. The runtime architecture fallback was
honest and bounded, but the package was not self-contained.

The implementation repairs that defect and adds reusable validation:

- canonical `Resource map` entries validate verb, class, containment, existence,
  and packageability;
- bounded legacy-resource lint catches unmapped `assets/`, `references/`,
  `scripts/`, and legacy `templates/` load instructions without scanning every
  path-like string;
- architecture resources are normalized under approved `assets/`;
- generated local mirrors, adapter output, release archives, and clean installs
  preserve mapped-resource relative paths and raw-byte SHA-256;
- recorded-source release compatibility skips only current canonical skill
  policy, while retaining release metadata and archive-integrity checks;
- repository-wide current skill audit is clean.

This artifact is M7 rationale and closeout evidence. It does not claim final
verify, PR readiness, live registry proof, or hosted CI success.

## Problem

The original package contract allowed a shipped skill to tell an agent to load a
skill-local resource that was absent from the installed skill tree. That can
produce inconsistent artifacts, invented template content, missing required
schema or security wording, and late customer-repository failures.

The proposal treated this as package integrity rather than an architecture
design failure. The important distinction was:

```text
runtime fallback:
  may preserve useful work when SKILL.md already contains enough contract

package validation:
  must still fail when mapped resources are missing
```

## Decision Trail

- Governing contract: amend `specs/skill-contract.md` instead of creating a
  competing generic resource contract.
  Source: proposal review `SRI-PR1`; spec R46-R55.
- Defect detection: validate explicit `Resource map` entries and add bounded
  legacy-reference lint for migration.
  Source: proposal review `SRI-PR2`; R49-R49d.
- Parity identity: use skill-root-relative path plus SHA-256 of raw file bytes.
  Source: proposal review `SRI-PR3`; R50-R50d.
- Baseline order: complete canonical-to-clean-install pre-change evidence
  before architecture resource mutation.
  Source: plan review `SRI-PLAN1`; M1.
- Architecture classification: keep skeletons and literal Mermaid style
  material as copyable `assets/`.
  Source: M3 behavior-preservation evidence.
- Runtime fallback: keep fallback as contingency only; do not let it validate
  broken packages.
  Source: R54-R54d; architecture behavior-preservation evidence.
- Historical releases: recorded-source validation may skip incompatible current
  skill policy, but must keep applicable release and archive checks.
  Source: `SRI-M4-CR1`, `SRI-M4-CR2`.
- Repository-wide enforcement: keep hard enforcement after a clean
  current-skills audit.
  Source: M6 repository-wide audit.

## Diff Rationale By Area

- `specs/skill-contract.md`
  Change: added R46-R55 for resource maps, classes, existence, legacy lint,
  parity identity, clean install, rollout, fallback, and architecture-pilot
  evidence.
  Reason: make generic resource-integrity rules part of the published skill
  contract.
  Source: proposal/spec reviews.
  Evidence: `specs/skill-contract.test.md` T41-T48.
- `specs/skill-contract.test.md`
  Change: added T41-T48 mapping baseline, validator, architecture
  normalization, parity, clean install, audit, and closeout proof.
  Reason: ensure every requirement has concrete proof.
  Source: approved test spec.
  Evidence: lifecycle and validation commands recorded in plan.
- `scripts/skill_validation.py`
  Change: added mapped-resource validation and bounded legacy-resource lint
  with instruction segmentation and per-reference context.
  Reason: catch missing or unmapped skill-local resources while avoiding broad
  Markdown path false positives.
  Source: R47-R49d; `SRI-M2-CR1` through `SRI-M2-CR3`.
  Evidence: `python scripts/test-skill-validator.py`;
  `python scripts/validate-skills.py`.
- `scripts/test-skill-validator.py`
  Change: added fixtures for verb/class rules, containment, missing resources,
  legacy `templates/` load instructions, false-positive boundaries,
  architecture post-M3 behavior, and current architecture map.
  Reason: prove the validator catches the original defect class and migration
  boundaries.
  Source: T42-T43.
  Evidence: focused and full validator tests.
- `skills/architecture/SKILL.md` and `skills/architecture/assets/*`
  Change: replaced raw `templates/...` instructions with a `Resource map` for
  `assets/architecture-skeleton.md`, `assets/adr-skeleton.md`, and
  `assets/diagram-styles.mmd`.
  Reason: make architecture resources skill-local and packageable without
  changing architecture obligations.
  Source: M3; R55c-R55e.
  Evidence: `behavior-preservation.md`; architecture validator fixture.
- `scripts/build-skills.py` and tests
  Change: added generated local mirror mapped-resource parity checks.
  Reason: prevent generated skill output from silently omitting or staling
  mapped resources.
  Source: R50-R50b; T45.
  Evidence: `python scripts/test-build-skills.py`;
  `python scripts/build-skills.py --check`.
- `scripts/adapter_distribution.py`, `scripts/validate-adapters.py`, and
  adapter tests
  Change: added adapter/archive mapped-resource parity, transformation-contract
  handling, recorded-source release profiles, archive validation results, and
  reusable clean-install smoke.
  Reason: prove packed and installed target output preserves mapped resources
  while keeping historical release compatibility narrow.
  Source: R50-R52c; T45-T46; `SRI-M4-CR1`, `SRI-M4-CR2`, `SRI-M5-CR1`.
  Evidence: `python scripts/test-adapter-distribution.py`; adapter
  build/validation; clean-install smoke.
- Change-local evidence
  Change: added resource-chain audit, validator fixtures, behavior
  preservation, clean-install proof, repository-wide audit, review records,
  review-resolution updates, and this explanation.
  Reason: keep root cause, behavior preservation, review decisions, and final
  rationale durable.
  Source: plan M1-M7.
  Evidence: review artifact, lifecycle, and metadata validation.
- Plan and plan index
  Change: tracked milestone state, validation, discoveries, review findings,
  and handoffs through M1-M7.
  Reason: keep one live state owner for the planned initiative.
  Source: active plan.
  Evidence: artifact lifecycle validation.

## Tests Added Or Changed

- `scripts/test-skill-validator.py` resource-map fixtures prove `COPY`, `READ`,
  and `RUN` point only to approved classes; mapped files exist under the skill
  root; and `templates/` is rejected as an approved class.
  Mapping: R47-R48b; T42.
- Legacy-resource lint fixtures prove recognized load instructions for
  `assets/`, `references/`, `scripts/`, and `templates/` fail outside the
  `Resource map`; examples, docs paths, fenced blocks, separate list items, and
  externally owned paths avoid false positives.
  Mapping: R49-R49d; T43.
- Architecture post-M3 fixtures prove former architecture `templates/...`
  instructions fail, and the normalized architecture `Resource map` passes with
  packaged assets.
  Mapping: R49d; R55c-R55e; T44.
- `scripts/test-build-skills.py` generated parity fixtures prove missing or
  stale mapped resources in generated local mirror output fail by relative path
  and raw-byte hash.
  Mapping: R50-R50b; T45.
- `scripts/test-adapter-distribution.py` adapter/archive parity fixtures prove
  generated adapter output and release archives reject missing or stale mapped
  resources.
  Mapping: R50-R50b; T45.
- Recorded-source release fixtures prove historical recorded-source validation
  retains release metadata and archive integrity while skipping only
  incompatible current skill policy.
  Mapping: R50-R53 compatibility; `SRI-M4-CR1`, `SRI-M4-CR2`.
- Clean-install smoke fixtures prove locally packed Codex, Claude, and opencode
  installs contain mapped architecture resources; stale and missing installed
  mapped resources fail with target/skill/path diagnostics.
  Mapping: R52-R52b; T46; `SRI-M5-CR1`.
- Repository-wide audit proof shows all current canonical skills pass
  resource-integrity validation, so global enforcement can remain enabled.
  Mapping: R53-R53b; T47.

## Validation Evidence Available Before Final Verify

M1 through M6 validation is recorded in the active plan and `change.yaml`. Key
proof includes:

- `python scripts/build-skills.py --check`
- `python scripts/build-skills.py --output-dir /tmp/rigorloop-sri-audit-generated-skills`
- `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-audit-release-output`
- `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-sri-audit-release-output`
- Codex clean install:
  ```bash
  node packages/rigorloop/dist/bin/rigorloop.js init codex \
    --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-codex-v0.3.2.zip \
    --json
  ```
- Claude clean install:
  ```bash
  node packages/rigorloop/dist/bin/rigorloop.js init claude \
    --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-claude-v0.3.2.zip \
    --json
  ```
- opencode clean install:
  ```bash
  node packages/rigorloop/dist/bin/rigorloop.js init opencode \
    --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-opencode-v0.3.2.zip \
    --json
  ```
- `python scripts/test-skill-validator.py`
- `python scripts/validate-skills.py`
- `python scripts/test-build-skills.py`
- `python scripts/test-adapter-distribution.py`
- `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-release-output`
- `python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-sri-release-output`
- `python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-install-release-output`
- Clean-install smoke:
  ```bash
  python scripts/validate-adapters.py --version v0.3.2 \
    --root /tmp/rigorloop-sri-install-release-output \
    --clean-install-smoke \
    --skill architecture
  ```
- `bash scripts/ci.sh --mode explicit` with every current `skills/*/SKILL.md` plus validator/test files
- lifecycle, review-artifact, change-metadata, and `git diff --check --`
  validation after each milestone or review recording step

M7 reruns the final validation bundle before code-review handoff. Final verify,
hosted CI, live registry proof, and PR readiness remain downstream.

## Review Resolution Summary

`review-resolution.md` records closed dispositions for all material findings.
No open findings remain in `review-log.md`.

- `SRI-PLAN1`: accepted. M1 was revised to require complete pre-change
  clean-installed target evidence before architecture resource changes.
- `SRI-M2-CR1`: accepted. Legacy-resource lint no longer suppresses resource
  loads because of broad conditional wording.
- `SRI-M2-CR2`: accepted. External ownership is evaluated per matched resource
  reference.
- `SRI-M2-CR3`: accepted. Markdown instruction segmentation prevents loading
  intent from crossing independent list or paragraph boundaries.
- `SRI-M3-CR1`: accepted. Temporary architecture legacy exceptions were removed
  after normalization.
- `SRI-M4-CR1`: accepted. Recorded-source release validation keeps applicable
  release-surface checks.
- `SRI-M4-CR2`: accepted. Recorded-source archive validation inspects rebuilt
  archives and mapped-resource parity.
- `SRI-M5-CR1`: accepted. Clean-install smoke has direct missing-installed
  mapped-resource regression coverage.

Clean code reviews closed M1 through M6. M7 is the final implementation
milestone and still requires code-review after this handoff.

## Alternatives Rejected

- Hand-copying missing files into `.agents/skills/architecture/`: rejected
  because it fixes one installed tree without repairing canonical packaging.
- Adding an implicit `templates/` packaged-resource class: rejected because the
  existing contract already distinguishes `assets/`, `references/`, and
  `scripts/`.
- Broad Markdown path scanning: rejected because it would classify artifact
  examples, repository paths, and customer-project paths as packaged resources.
- Presence-only parity: rejected because it cannot detect stale generated,
  archive, or installed resource bytes.
- Live registry proof during implementation closeout: rejected because the
  accepted contract keeps live registry installation as release-owned evidence.
- Historical archive repair: rejected as out of scope for immutable or
  compatibility-sensitive release artifacts.

## Scope Control

Preserved non-goals:

- no remote resource loading or runtime downloading;
- no redesign of architecture lifecycle, arc42, C4, ADR, or review semantics;
- no hidden movement of normative architecture policy out of `SKILL.md`;
- no generated or installed skill output hand-edits as durable fixes;
- no historical archive mutation;
- no live registry success claim;
- no branch readiness, PR readiness, or final verify claim from implementation.

## Risks And Follow-Ups

- Final verify still needs to assess whole-branch artifact-code-test coherence
  after M7 code-review closes.
- Live registry proof remains release-owned and is not part of this
  implementation closeout.
- Future resource classes, if needed, require a separate skill-contract
  amendment with verbs, packaging semantics, and validation behavior.
- Historical adapter archive diagnostics remain a possible follow-up; this
  change validates recorded-source compatibility without rewriting history.

## Readiness

M1 through M6 are closed after clean code reviews. M7 records the durable
rationale and final implementation validation before handing the milestone to
`code-review`.

Next stage after M7 implementation handoff: `code-review`.
