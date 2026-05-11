# Learn Session: Progressive Loading High-Cost Skills

## Frame

- Trigger: maintainer explicitly invoked `$learn 2026-05-11-progressive-loading-high-cost-skills.md` after CI failed on the progressive-loading branch.
- Trigger type: explicit maintainer request / failed CI observation.
- Scope: CI failure and local remediation for the progressive-loading high-cost public skills change.
- Session path: `docs/learn/sessions/2026-05-11-progressive-loading-high-cost-skills.md`
- Evidence in scope:
  - GitHub CI failure on PR #43 run `25693524473`, job `ci`, selected check `selector.regression`
  - local reproduction with `python scripts/test-select-validation.py`
  - remediation commit `c766142b8c47c8c59d95ea709d3e32a7b06a7884`
  - local PR-mode wrapper run: `bash scripts/ci.sh --mode pr --base 0dc169c37e610cdd21a859df2ba3d467678c85b7 --head c766142b8c47c8c59d95ea709d3e32a7b06a7884`
  - `skills/workflow/SKILL.md`
  - `skills/code-review/SKILL.md`
  - generated skill and adapter outputs regenerated from canonical skill edits
- Explicit exclusions:
  - This session does not claim GitHub-hosted CI passed after the local commit until the branch is pushed and the remote check completes.
  - This session does not create a new workflow, validation, or token-cost policy.
  - This session does not update curated topic guidance without contributor confirmation.
- Prior learnings reviewed:
  - `docs/learn/README.md`
  - `docs/learn/topics/token-cost-measurement.md`
  - `docs/learn/sessions/2026-05-11-dynamic-token-cost-root-cause.md`

## Observe

### O1: Optimizing public skill prose can accidentally remove exact validation-layering anchors

The progressive-loading optimization preserved the meaning of the workflow and code-review validation guidance, but `selector.regression` expected exact public-surface anchor terms. The optimized text no longer contained every required anchor in the exact casing or phrase shape.

Evidence:

- `python scripts/test-select-validation.py` initially failed for `skills/code-review/SKILL.md` because the public skill did not contain the exact phrase `selected checks`.
- After the first fix, the same regression still failed for `skills/workflow/SKILL.md` because it required the exact lowercase phrase `manual proof`.
- The final canonical workflow sentence now includes `targeted proof`, `broad smoke`, `manual proof`, `verify-report.md`, and `broad_smoke.sources`.
- The final canonical code-review sentence now includes `selected checks`.
- Regenerated `.codex/skills/` and `dist/adapters/` copies mirror the canonical skill changes.

### O2: CI reproduction needed the PR base commit to exist locally

The first local attempt to run the PR-mode wrapper with the GitHub base SHA returned `empty-changed-paths` because the base commit was not present in the local clone. Fetching the base SHA from origin allowed the selector to discover the changed paths and run the same selected check set as CI.

Evidence:

- `git merge-base 0dc169c37e610cdd21a859df2ba3d467678c85b7 HEAD` failed before fetching the base commit.
- `git fetch origin 0dc169c37e610cdd21a859df2ba3d467678c85b7` made the base commit available locally.
- The rerun of `bash scripts/ci.sh --mode pr --base 0dc169c37e610cdd21a859df2ba3d467678c85b7 --head c766142b8c47c8c59d95ea709d3e32a7b06a7884` selected the expected PR paths and passed all selected checks.

## Classify

| ID | Proposed primary classification | Final primary classification | Secondary routes | Confirmed by | Rationale |
| --- | --- | --- | --- | --- | --- |
| O1 | durable-lesson | pending confirmation | Candidate topic update: validation or token-cost measurement | Pending contributor confirmation | The observation is reusable: prose compression must preserve exact contract anchors when tests intentionally enforce them. Because learn must not route durable guidance without contributor confirmation, no topic update was made in this session. |
| O2 | observation | observation | Session record only | Maintainer-triggered session plus local command evidence | This is useful operational evidence for this incident, but it does not yet show a recurring pattern that needs durable topic guidance. |

## Route

- Created session record: `docs/learn/sessions/2026-05-11-progressive-loading-high-cost-skills.md`
- No topic file was updated.
- No authoritative artifact update was made from this learn session.
- Candidate durable guidance, if confirmed later: when optimizing public skill prose covered by static regression tests, preserve exact anchor vocabulary or update the owning test and contract together.

## Validation Evidence

Commands run during the CI remediation before this learn session:

```bash
python scripts/test-select-validation.py
python scripts/build-skills.py --check
python scripts/build-adapters.py --version 0.1.1 --check
python scripts/validate-skills.py
python scripts/test-skill-validator.py
python scripts/validate-adapters.py --version 0.1.1
python scripts/test-adapter-distribution.py
python scripts/validate-change-metadata.py docs/changes/2026-05-11-progressive-loading-high-cost-public-skills/change.yaml
bash scripts/ci.sh --mode pr --base 0dc169c37e610cdd21a859df2ba3d467678c85b7 --head c766142b8c47c8c59d95ea709d3e32a7b06a7884
```

Result:

- The focused selector regression passed.
- Generated skill and adapter drift checks passed.
- The PR-mode wrapper selected and passed `skills.validate`, `skills.regression`, `skills.drift`, `adapters.regression`, `adapters.drift`, `adapters.validate`, `review_artifacts.validate`, `artifact_lifecycle.validate`, `change_metadata.regression`, `change_metadata.validate`, `selector.regression`, and `token_cost.regression`.

## Follow-Ups

- No follow-up is required for O2.
- O1 remains a candidate durable lesson pending contributor confirmation before any topic update.
