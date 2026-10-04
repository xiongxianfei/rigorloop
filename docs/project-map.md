# RigorLoop project map

## Map metadata

- Map status: partial
- Scope: repository
- Baseline: 85a1b9ba7cd1a43ad9e72b924edd88a68fe15872 plus the canonical-design-ownership change. Definition ownership, contract paths and current recording guidance refreshed; unrelated tooling observations retain their earlier qualification.
- Last reviewed: 2026-10-04
- Coverage: current test/fixture placement and validation/CI callers; prior repository orientation retained outside this refresh.
- Exclusions: external account configuration, hosted release execution and historical artifact contents.
- Parent map: not-applicable
- Known gaps: hosted deployment state is not established; unrelated repository sections were not re-audited in this test-layout refresh.

## Purpose and scope

This map orients contributors to the inspected repository. [System](../design/architecture/composition.md) owns model composition; [CONSTITUTION.md](../CONSTITUTION.md) owns governance. This map does not own workflow stage order; Workflow owns it. CLI owns deterministic change-context facts, and route owns semantic routing. Exact workflow state belongs to the selected change record. The previous map described retired specs, YAML lifecycle engines, three-target distribution and direct CI gates; the current source paths below correct those claims.

## System overview

RigorLoop publishes skill guidance and a command-line executable. The REM model owns current engineering definitions; detailed contracts live with responsible Modules and repository support under [design/](../design/). Canonical skills live in [skills/](../skills/), and the npm package is [packages/rigorloop/](../packages/rigorloop/). Individual skills work without CLI recording; governed recording uses the executable. No long-running service is present in the inspected runtime. [Explore](../skills/explore/SKILL.md) and [Research](../skills/research/SKILL.md) provide optional discovery support; their conclusions return to the owning stage before changing a decision.

## Repository layout

| Path | Observed responsibility |
| --- | --- |
| [VISION.md](../VISION.md), [AGENTS.md](../AGENTS.md), [CONSTITUTION.md](../CONSTITUTION.md) | Project direction, operating guidance and governing principles. |
| [design/](../design/) | Current REM definitions and owner-scoped detailed contracts; start at design/README.md and design/support/ownership.md. |
| [docs/proposals/](proposals/), [docs/plans/](plans/), [docs/plan.md](plan.md) | Direction, stable delivery intent and plan navigation. |
| [docs/changes/](changes/) | Historical filesystem records and unchanged evidence; current operational state is CLI-managed SQLite under the private .rigorloop/ area. |
| [skills/](../skills/), [templates/](../templates/) | Authored skill packages, scaffolds and shared projection inputs. |
| [packages/rigorloop/dist/](../packages/rigorloop/dist/) | Tracked executable JavaScript, runtime schemas and bundled installation metadata; no separate src tree exists. |
| [scripts/](../scripts/), [schemas/](../schemas/) | Repository validation, generation, release tooling and schema resources. |
| [tests/skill/](../tests/skill/), [tests/engineering/](../tests/engineering/), [tests/fixtures/](../tests/fixtures/), [packages/rigorloop/test/](../packages/rigorloop/test/) | Capability-owned repository cases, shared inputs, package cases and owned dynamic fixture builders. Exclusive boundary fixtures live beside Validation tests. |
| [dist/adapters/](../dist/adapters/) | Tracked support README and manifest; generated public skill bodies are archive output. |
| [docs/releases/](releases/), [docs/reports/](reports/) | Release intent/notes, profiles and retained operational evidence. |
| [docs/learn/](learn/), [docs/research/](research/) | Learning and optional standalone investigation artifacts. |

The retired repository specs and mixed architecture/ADR trees are recoverable from Git. Their current responsibilities are covered by the REM owners. Retired source-transfer evidence retains its original revision and is not a current authority.

Optional Explore output uses `docs/explorations/` when invoked; that directory need not exist before an artifact is authored.

## Runtime flow

Statically traced: [rigorloop.js](../packages/rigorloop/dist/bin/rigorloop.js) dispatches installation, recording, discovery and diagnostic commands. Installation uses [installer-replacement.js](../packages/rigorloop/dist/lib/installer-replacement.js); command logging and rendering are separate modules. Recording uses the package-local record-store modules and schemas. The CLI constructs and persists explicit actor decisions; [route](../skills/route/SKILL.md) supplies semantic routing.

Repository validation enters through [ci.sh](../scripts/ci.sh), uses [validation_selection.py](../scripts/lib/validation/validation_selection.py) for trusted check selection and [validation_execution.py](../scripts/lib/validation/validation_execution.py) for bounded execution. [build-adapters.py](../scripts/build-adapters.py) generates archives from canonical skills and thin templates; [boundary-first-resources.yaml](../scripts/resources/boundary-first/boundary-first-resources.yaml) declares shared projection inputs.

## Data flow

Current operational storage uses rigorloop-records-v4 in project-local SQLite with the targeted-recording-v2 interface. Skills call the CLI; they do not write SQL. [Records](../design/architecture/modules/MOD-018-engineering-operations/modules/MOD-011-operational-record-persistence/record-contract.md) owns representation; [CLI](../design/architecture/modules/MOD-018-engineering-operations/modules/MOD-010-engineering-command-interface/command-contract.md) owns safe queries and writes. Engineering definitions remain repository files and stable plans remain separate from mutable operational state. Historical stores are excluded from ordinary discovery without executing old validators; malformed current stores remain errors.

Skill frontmatter and Markdown resources become generated ZIP archives. The packed npm tarball contains the executable and its allowlisted runtime inputs. [release_candidate.py](../scripts/lib/release/release_candidate.py) binds prepared source, profile and artifact identities; qualification checks real candidate bytes before approval or execution.

## External boundaries

[CI](../.github/workflows/ci.yml) and [release automation](../.github/workflows/release.yml) use GitHub Actions. Release tooling interacts with GitHub release assets and npm under separate approval. Installation supports Codex and Claude archives through verified metadata and destination checks. Logs are local diagnostics, not workflow evidence. Account credentials, live release state and target-agent behavior were not inspected for this map.

## Test map

Python unittest entrypoints now live in `tests/skill/` and `tests/engineering/{validation,packaging,release}/`. The release suite imports its sibling `release_candidate_tests.py`, `release_coordination_tests.py`, `release_execution_tests.py` and `release_evidence_tests.py`. Supported validation commands remain in `scripts/`; internal helpers live under `scripts/lib/{validation,packaging,release}/`, and authored templates/manifest under `scripts/resources/`; the test-only phrase helper lives in `tests/skill/`. Node tests and builders live in packages/rigorloop/test/. Earlier test-maintenance assessments retain their original population and do not serve as a permanent test registry.

Current groups protect skills/resources, portable boundary inputs, documentation, selectors/execution, current SQLite operations and explicit historical-record import, installation/privacy, archives/npm and actual release candidates. Retired lifecycle/review engines and exclusive fixtures are absent. [validate-governed-lifecycle-cli.py](../scripts/validate-governed-lifecycle-cli.py) validates current discovery or exact Git snapshots; [release_evidence.py](../scripts/release_evidence.py) retains the release-owned checklist.

## CI and release map

Configured commands:

```bash
bash scripts/ci.sh --mode local
bash scripts/ci.sh --mode pr --base BASE --head HEAD
npm test --prefix packages/rigorloop
python scripts/build-adapters.py --check
```

The CI workflow selects PR-range checks or full main gates, then separately proves real executor overlap. Python and Node cases share the configured worker budget. Unknown paths or invalid preflight scope fail closed. Release automation calls release-coordinator.py; prepared-candidate qualification reaches release-verify.sh with the exact candidate directory. This map does not authorize publication.

## Architecture rules observed

[AGENTS.md](../AGENTS.md) keeps skills/ as the only authored skill source and generated adapter bodies out of tracked source. [Workflow](../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-006-engineering-change-control/workflow.md) separates stable plans from mutable records. [Assessment](../design/architecture/modules/MOD-017-engineering-governance/modules/MOD-007-engineering-verification-and-assurance/assessment.md) requires independent whole-change review and distinct final Verify. Current operations do not fetch retired contracts from Git; historical links identify provenance only.

## Risk areas

Historical records deliberately preserve old names and approvals. Consult current owners before relying on them. Snapshot validation and candidate qualification have distinct Git/object and filesystem boundaries; their dedicated tests protect those limits. A source or fixture edit can invalidate earlier validation even when its top-level command is unchanged.

## Open questions

External account and hosted release state are outside this repository map's scope. The current test layout was inspected; unrelated orientation claims retain the earlier baseline and were not re-assessed in this refresh.

## Evidence trail

| Evidence | Type | Result |
| --- | --- | --- |
| packages/rigorloop/package.json and dist/bin/rigorloop.js | source | Public package boundary and command dispatch. |
| scripts/lib/validation/validation_selection.py and scripts/lib/validation/validation_execution.py | source | Current catalog and shared bounded executor; stable commands import their explicit package. |
| scripts/lib/packaging/, scripts/lib/release/, scripts/resources/ | source | Capability-owned implementation and authored operational resources; supported command paths remain at scripts root. |
| .github/workflows/ci.yml and release.yml | source | Hosted entrypoints and separate operational boundaries. |
| M4 validation evidence | executed command | Local plus broad CI, Node and current record/release proofs passed on the recorded M4 subjects. |
| M5 test-maintenance evidence | source | Prior test/fixture membership, generators and retained protective purposes. |
| tests/skill/, tests/engineering/ and packages/rigorloop/test/ | source | Current repository/package test ownership and sibling release imports. |
| .github/workflows/ci.yml and publish-github-packages.yml | configured command | Relocated executor-overlap and npm-package test commands; no hosted execution observed. |

Earlier test passes are scoped evidence, not a claim that this map verifies the final cleanup change.
