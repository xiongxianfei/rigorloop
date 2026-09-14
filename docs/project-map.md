# RigorLoop project map

## Map metadata

- Map status: current
- Scope: repository
- Baseline: a593d163ce245968694e059130ebe0ac27a58ccc plus M6 source-removal working tree on cleanup/retire-specs-and-stale-tests; exact changed paths and source identities are recorded in the owning cleanup change.
- Last reviewed: 2026-09-14
- Coverage: current model hierarchy, canonical skills, CLI, records, validation, packaging, release entrypoints and test/fixture layout.
- Exclusions: external account configuration, hosted release execution and historical artifact contents.
- Parent map: not-applicable
- Known gaps: hosted deployment state is not established by this map.

## Purpose and scope

This map orients contributors to the inspected repository. [System](design/system.md) owns model composition; [CONSTITUTION.md](../CONSTITUTION.md) owns governance. This map does not own workflow stage order; Workflow owns it. CLI owns deterministic workflow-context facts, and route owns semantic routing. Exact workflow state belongs to the selected change record. The previous map described retired specs, YAML lifecycle engines, three-target distribution and direct CI gates; the current source paths below correct those claims.

## System overview

RigorLoop publishes skill guidance and a command-line executable. [Skill](design/skill/skill.md), [CLI](design/cli/cli.md) and [Engineering](design/engineering/engineering.md) are the three main model owners. Canonical skills live in [skills/](../skills/), and the npm package is [packages/rigorloop/](../packages/rigorloop/). Individual skills work without CLI recording; governed recording uses the executable. No long-running service is present in the inspected runtime. [Explore](../skills/explore/SKILL.md) and [Research](../skills/research/SKILL.md) provide optional discovery support; their conclusions return to the owning stage before changing a decision.

## Repository layout

| Path | Observed responsibility |
| --- | --- |
| [VISION.md](../VISION.md), [AGENTS.md](../AGENTS.md), [CONSTITUTION.md](../CONSTITUTION.md) | Project direction, operating guidance and governing principles. |
| [docs/design/](design/) | Current behavioral and technical contracts, decisions and acceptance intent. |
| [docs/proposals/](proposals/), [docs/plans/](plans/), [docs/plan.md](plan.md) | Direction, stable delivery intent and plan navigation. |
| [docs/changes/](changes/) | Current v3 stores and unchanged historical evidence; filename alone does not imply current runtime support. |
| [skills/](../skills/), [templates/](../templates/) | Authored skill packages, scaffolds and shared projection inputs. |
| [packages/rigorloop/dist/](../packages/rigorloop/dist/) | Tracked executable JavaScript, runtime schemas and bundled installation metadata; no separate src tree exists. |
| [scripts/](../scripts/), [schemas/](../schemas/) | Repository validation, generation, release tooling and schema resources. |
| [tests/fixtures/](../tests/fixtures/), [scripts/fixtures/](../scripts/fixtures/), [packages/rigorloop/test/](../packages/rigorloop/test/) | Static fixtures, executable cases and owned dynamic fixture builders. |
| [dist/adapters/](../dist/adapters/) | Tracked support README and manifest; generated public skill bodies are archive output. |
| [docs/releases/](releases/), [docs/reports/](reports/) | Release intent/notes, profiles and retained operational evidence. |
| [docs/learn/](learn/), [docs/research/](research/), [docs/explorations/](explorations/) | Learning and optional standalone investigation artifacts. |

The retired repository specs and mixed architecture/ADR trees are recoverable from Git. Their current responsibilities are covered by the Designs and the cleanup's [source disposition](changes/2026-09-14-retire-specs-and-stale-tests/source-disposition.md).

## Runtime flow

Statically traced: [rigorloop.js](../packages/rigorloop/dist/bin/rigorloop.js) dispatches installation, recording, discovery and diagnostic commands. Installation uses [installer-replacement.js](../packages/rigorloop/dist/lib/installer-replacement.js); command logging and rendering are separate modules. Recording uses the package-local record-store modules and schemas. The CLI constructs and persists explicit actor decisions; [route](../skills/route/SKILL.md) supplies semantic routing.

Repository validation enters through [ci.sh](../scripts/ci.sh), uses [validation_selection.py](../scripts/validation_selection.py) for trusted check selection and [validation_execution.py](../scripts/validation_execution.py) for bounded execution. [build-adapters.py](../scripts/build-adapters.py) generates archives from canonical skills and thin templates; [boundary-first-resources.yaml](../scripts/boundary-first-resources.yaml) declares shared projection inputs.

## Data flow

Current governed storage is rigorloop-records-v3: change.json plus registered review, evidence, decision and Verify JSON records. [Records](design/cli/records.md) owns representation; [CLI](design/cli/cli.md) owns safe queries and writes. Proposals, Designs and plans remain separate engineering subjects with exact identities. Historical stores are excluded from ordinary discovery without executing old validators; malformed current stores remain errors.

Skill frontmatter and Markdown resources become generated ZIP archives. The packed npm tarball contains the executable and its allowlisted runtime inputs. [release_candidate.py](../scripts/release_candidate.py) binds prepared source, profile and artifact identities; qualification checks real candidate bytes before approval or execution.

## External boundaries

[CI](../.github/workflows/ci.yml) and [release automation](../.github/workflows/release.yml) use GitHub Actions. Release tooling interacts with GitHub release assets and npm under separate approval. Installation supports Codex and Claude archives through verified metadata and destination checks. Logs are local diagnostics, not workflow evidence. Account credentials, live release state and target-agent behavior were not inspected for this map.

## Test map

Python unittest entrypoints are scripts/test-*.py; the release suite also imports release_candidate_tests.py, release_coordination_tests.py, release_execution_tests.py and release_evidence_tests.py. Node tests and builders live in packages/rigorloop/test/. The [M5 audit](changes/2026-09-14-retire-specs-and-stale-tests/m5-test-maintenance.json) records the complete reviewed population and generated domains; it is change evidence, not a permanent test registry.

Current groups protect skills/resources, portable boundary inputs, documentation, selectors/execution, v3 records/discovery, installation/privacy, archives/npm and actual release candidates. Retired lifecycle/review engines and exclusive fixtures are absent. [validate-governed-lifecycle-cli.py](../scripts/validate-governed-lifecycle-cli.py) validates current discovery or exact Git snapshots; [release_evidence.py](../scripts/release_evidence.py) retains the release-owned checklist.

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

[AGENTS.md](../AGENTS.md) keeps skills/ as the only authored skill source and generated adapter bodies out of tracked source. [Workflow](design/skill/workflow.md) separates stable plans from mutable records. [Assessment](design/skill/assessment.md) requires independent whole-change review and distinct final Verify. Current operations do not fetch retired contracts from Git; historical links identify provenance only.

## Risk areas

Historical records deliberately preserve old names and approvals. Consult current owners before relying on them. Snapshot validation and candidate qualification have distinct Git/object and filesystem boundaries; their dedicated tests protect those limits. A source or fixture edit can invalidate earlier validation even when its top-level command is unchanged.

## Open questions

External account and hosted release state are outside this repository map's scope. No unresolved repository-orientation question was found in the inspected areas.

## Evidence trail

| Evidence | Type | Result |
| --- | --- | --- |
| packages/rigorloop/package.json and dist/bin/rigorloop.js | source | Public package boundary and command dispatch. |
| scripts/validation_selection.py and validation_execution.py | source | Current catalog and shared bounded executor. |
| .github/workflows/ci.yml and release.yml | source | Hosted entrypoints and separate operational boundaries. |
| M4 validation evidence | executed command | Local plus broad CI, Node and current record/release proofs passed on the recorded M4 subjects. |
| M5 test-maintenance evidence | source | Current test/fixture membership, generators and retained protective purposes. |

Earlier test passes are scoped evidence, not a claim that this map verifies the final cleanup change.
