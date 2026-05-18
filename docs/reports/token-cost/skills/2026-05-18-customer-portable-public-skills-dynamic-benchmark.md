# Customer-Portable Public Skills Dynamic Benchmark

## Status

Recorded for M3 on 2026-05-18.

## Benchmark Mode

This is a targeted live customer-fixture benchmark for the customer-portable public skill first slice. It uses `codex exec --json --ephemeral --skip-git-repo-check` against a temporary copy of the synthetic customer fixture with generated Codex adapter skills installed under `.agents/skills/`.

The generated adapter archive also contains a root `AGENTS.md`. The benchmark removed that generated root governance file from the temporary fixture before execution so the customer-project scenarios still test absence of root `AGENTS.md` and `CONSTITUTION.md`.

## Fixture

Tracked fixture path:

```text
docs/reports/token-cost/skills/fixtures/customer-portable-public-skills/
```

Temporary live fixture:

```text
/tmp/rigorloop-customer-portable-live-fixture
```

Included synthetic project-local artifacts:

```text
rigorloop.yaml
rigorloop.lock
docs/workflows.md
docs/changes/example-change/change.yaml
docs/changes/example-change/explain-change.md
specs/customer-feature.md
docs/plans/customer-plan.md
src/app.js
tests/app.test.js
.agents/skills/
```

Deliberately excluded from the live fixture:

```text
AGENTS.md
CONSTITUTION.md
RigorLoop internal specs/
RigorLoop internal docs/reports/
docs/follow-ups.md
docs/project-map.md
```

Fixture exclusion command:

```bash
test ! -e /tmp/rigorloop-customer-portable-live-fixture/AGENTS.md && test ! -e /tmp/rigorloop-customer-portable-live-fixture/CONSTITUTION.md && test ! -e /tmp/rigorloop-customer-portable-live-fixture/docs/follow-ups.md && test ! -e /tmp/rigorloop-customer-portable-live-fixture/docs/project-map.md
```

Result: passed.

## Commands

```bash
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/rigorloop-adapters-m3-live
codex exec --json --ephemeral --skip-git-repo-check "<scenario prompt>" > docs/reports/token-cost/skills/runs/2026-05-18-customer-portable-public-skills/<scenario>.jsonl
python scripts/analyze-codex-jsonl.py docs/reports/token-cost/skills/runs/2026-05-18-customer-portable-public-skills/<scenario>.jsonl --summary-output docs/reports/token-cost/skills/runs/2026-05-18-customer-portable-public-skills/<scenario>.analysis.yaml --run-id <scenario>
```

## Scenario Results

| Scenario | Skill | Input tokens | Largest command output tokens | Full-file reads | Broad searches | Local guide used | Portable default / ambiguity behavior | Attempted reliance on absent RigorLoop internals | Result quality | Evidence |
|---|---|---:|---:|---:|---:|---|---|---|---|---|
| `proposal-customer-no-internal-docs` | `proposal` | 52,705 | 146 | 0 | 0 | yes | used portable proposal default; blocked substantive proposal on absent local vision gate | no | pass | JSONL and analyzer summary |
| `proposal-review-customer-local-artifacts` | `proposal-review` | 52,535 | 146 | 0 | 0 | yes | used local spec placement default; requested clearer contract for API ambiguity | no | pass | JSONL and analyzer summary |
| `spec-customer-local-workflow-guide` | `spec` | 32,881 | 146 | 0 | 0 | yes | used portable spec structure and local workflow guide for placement | no | pass | JSONL and analyzer summary |
| `plan-customer-local-spec-and-code` | `plan` | 53,651 | 179 | 0 | 0 | yes | used local plan/spec/code; blocked suffix milestone on missing approved local spec behavior | no | pass | JSONL and analyzer summary |
| `implement-customer-plan-handoff` | `implement` | 95,034 | 146 | 0 | 0 | yes | started from local handoff; blocked implementation action on missing approved suffix scope | no | pass | JSONL and analyzer summary |
| `workflow-customer-route-no-internal-docs` | `workflow` | 61,141 | 146 | 0 | 0 | yes | used local guide and routed to implement; no ambiguity block needed | no | pass | JSONL and analyzer summary |
| `project-map-customer-repo-orientation` | `project-map` | 69,708 | 146 | 0 | 3 | yes | treated absent local governance/docs/specs as normal | no | pass-with-warning | JSONL and analyzer summary |
| `verify-customer-final-pack` | `verify` | 73,941 | 146 | 0 | 1 | yes | refused to claim validation passed without evidence | no | pass-with-warning | JSONL and analyzer summary |
| `pr-customer-ready-handoff` | `pr` | 79,827 | 1,840 | 0 | 0 | yes | blocked PR readiness on absent git/verify/validation evidence | no | pass | JSONL and analyzer summary |

Notes:

- `project-map` performed bounded repository-orientation searches, which are expected for a repository mapping skill. The broad-search count is recorded instead of hidden.
- `verify` performed a bounded local governance absence check with `find . -maxdepth 2`; it did not search for RigorLoop repository originals.
- `pr` produced a large `git diff --stat` output because the temporary fixture was not a Git repository and the command reported repository-level context. The run still correctly blocked PR readiness.
- Analyzer `full_file_read_count` is zero for all scenarios. Some analyzer summaries classify short leading-range reads as `suspected`; these were bounded reads of small local fixture files.

## Per-Scenario Evidence Files

| Scenario | Prompt | Raw JSONL | Analyzer summary |
|---|---|---|---|
| `proposal-customer-no-internal-docs` | `runs/2026-05-18-customer-portable-public-skills/prompts/proposal-customer-no-internal-docs.md` | `runs/2026-05-18-customer-portable-public-skills/proposal-customer-no-internal-docs.jsonl` | `runs/2026-05-18-customer-portable-public-skills/proposal-customer-no-internal-docs.analysis.yaml` |
| `proposal-review-customer-local-artifacts` | `runs/2026-05-18-customer-portable-public-skills/prompts/proposal-review-customer-local-artifacts.md` | `runs/2026-05-18-customer-portable-public-skills/proposal-review-customer-local-artifacts.jsonl` | `runs/2026-05-18-customer-portable-public-skills/proposal-review-customer-local-artifacts.analysis.yaml` |
| `spec-customer-local-workflow-guide` | `runs/2026-05-18-customer-portable-public-skills/prompts/spec-customer-local-workflow-guide.md` | `runs/2026-05-18-customer-portable-public-skills/spec-customer-local-workflow-guide.jsonl` | `runs/2026-05-18-customer-portable-public-skills/spec-customer-local-workflow-guide.analysis.yaml` |
| `plan-customer-local-spec-and-code` | `runs/2026-05-18-customer-portable-public-skills/prompts/plan-customer-local-spec-and-code.md` | `runs/2026-05-18-customer-portable-public-skills/plan-customer-local-spec-and-code.jsonl` | `runs/2026-05-18-customer-portable-public-skills/plan-customer-local-spec-and-code.analysis.yaml` |
| `implement-customer-plan-handoff` | `runs/2026-05-18-customer-portable-public-skills/prompts/implement-customer-plan-handoff.md` | `runs/2026-05-18-customer-portable-public-skills/implement-customer-plan-handoff.jsonl` | `runs/2026-05-18-customer-portable-public-skills/implement-customer-plan-handoff.analysis.yaml` |
| `workflow-customer-route-no-internal-docs` | `runs/2026-05-18-customer-portable-public-skills/prompts/workflow-customer-route-no-internal-docs.md` | `runs/2026-05-18-customer-portable-public-skills/workflow-customer-route-no-internal-docs.jsonl` | `runs/2026-05-18-customer-portable-public-skills/workflow-customer-route-no-internal-docs.analysis.yaml` |
| `project-map-customer-repo-orientation` | `runs/2026-05-18-customer-portable-public-skills/prompts/project-map-customer-repo-orientation.md` | `runs/2026-05-18-customer-portable-public-skills/project-map-customer-repo-orientation.jsonl` | `runs/2026-05-18-customer-portable-public-skills/project-map-customer-repo-orientation.analysis.yaml` |
| `verify-customer-final-pack` | `runs/2026-05-18-customer-portable-public-skills/prompts/verify-customer-final-pack.md` | `runs/2026-05-18-customer-portable-public-skills/verify-customer-final-pack.jsonl` | `runs/2026-05-18-customer-portable-public-skills/verify-customer-final-pack.analysis.yaml` |
| `pr-customer-ready-handoff` | `runs/2026-05-18-customer-portable-public-skills/prompts/pr-customer-ready-handoff.md` | `runs/2026-05-18-customer-portable-public-skills/pr-customer-ready-handoff.jsonl` | `runs/2026-05-18-customer-portable-public-skills/pr-customer-ready-handoff.analysis.yaml` |

`code-review-customer-diff-small` was not run because `skills/code-review/SKILL.md` did not change.

## Result-Quality Criteria

| Criterion | Result | Evidence |
|---|---|---|
| Customer fixture excludes RigorLoop internals | pass | Live fixture exclusion command passed; root `AGENTS.md`, root `CONSTITUTION.md`, internal reports, follow-ups, and project map were absent. |
| Public skills do not require RigorLoop internals | pass | All scenario final outputs state `attempted reliance on absent RigorLoop internals: no`. |
| Legitimate local docs/specs remain allowed | pass | Runs used local `docs/workflows.md`, local specs, local plans, change roots, source, and tests. |
| Local workflow guide is optional but usable | pass | Every scenario that needed placement or routing used local `docs/workflows.md`; scenarios still blocked on ambiguity or missing evidence where appropriate. |
| Runtime over-read risk is bounded | pass-with-warning | Analyzer broad-search counts were zero except `project-map` repository orientation and one bounded `verify` absence check. Largest command output was 1,840 estimated tokens in `pr`; no high-output blocker was reported. |
| Live token counters | pass | Analyzer summaries record input tokens for every required scenario. |

## Summary

The targeted live benchmark supports the first-slice runtime portability claim. The live customer fixture lacks root governance, RigorLoop internal specs/reports, follow-ups, and project-map guidance. The required touched-skill scenarios used project-local artifacts, portable defaults, or ambiguity blocks and did not rely on absent RigorLoop repository internals.
