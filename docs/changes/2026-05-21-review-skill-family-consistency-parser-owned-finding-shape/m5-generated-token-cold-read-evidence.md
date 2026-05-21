# M5 Generated Output, Token, and Cold-Read Evidence

Change: `2026-05-21-review-skill-family-consistency-parser-owned-finding-shape`
Date: 2026-05-21
Milestone: M5. Generated output, token, cold-read, and lifecycle closeout

## Scope

This evidence proves the canonical review-family skill changes package into generated skill mirrors and temporary adapter archives, records token-cost evidence, and confirms an installed-skill reader can produce a parser-shaped material finding from skill text plus packaged assets.

No generated adapter output was hand-edited. Adapter proof used temporary release archives generated from canonical `skills/`.

## Generated Skill Mirror Proof

Command:

```bash
python scripts/build-skills.py --check
```

Result:

```text
validated generated skills from /home/xiongxianfei/data/20260419-rigorloop/skills using temporary output /tmp/rigorloop-skills-check-cbk8rsez/skills
```

Additional inspected generated mirror:

```bash
python scripts/build-skills.py --output-dir /tmp/tmp.3BHe2rlC2g
```

Generated mirror asset presence:

```text
/tmp/tmp.3BHe2rlC2g/code-review/assets/material-finding.md
/tmp/tmp.3BHe2rlC2g/code-review/assets/review-result-skeleton.md
/tmp/tmp.3BHe2rlC2g/proposal-review/assets/material-finding.md
/tmp/tmp.3BHe2rlC2g/proposal-review/assets/review-result-skeleton.md
/tmp/tmp.3BHe2rlC2g/spec-review/assets/material-finding.md
/tmp/tmp.3BHe2rlC2g/spec-review/assets/review-result-skeleton.md
```

Conclusion: all mapped first-slice review-family assets are present in generated skill mirror output.

## Temporary Adapter Proof

Repository adapter version used: `v0.1.5`.

Commands:

```bash
python scripts/build-adapters.py --version v0.1.5 --output-dir /tmp/tmp.cG1mr7T4PH
python scripts/validate-adapters.py --root /tmp/tmp.cG1mr7T4PH --version v0.1.5
```

Generated archives:

```text
/tmp/tmp.cG1mr7T4PH/rigorloop-adapter-codex-v0.1.5.zip
/tmp/tmp.cG1mr7T4PH/rigorloop-adapter-claude-v0.1.5.zip
/tmp/tmp.cG1mr7T4PH/rigorloop-adapter-opencode-v0.1.5.zip
```

Validation result:

```text
validated generated adapter archives for version v0.1.5 under /tmp/tmp.cG1mr7T4PH
```

Archive asset presence was inspected for each archive. Every archive contains:

```text
code-review/assets/material-finding.md
code-review/assets/review-result-skeleton.md
proposal-review/assets/material-finding.md
proposal-review/assets/review-result-skeleton.md
spec-review/assets/material-finding.md
spec-review/assets/review-result-skeleton.md
```

Conclusion: temporary adapter packages include all mapped first-slice review-family assets, and adapter validation passes from temporary generated output.

## No-Hand-Edit Proof

- Generated skill mirror proof used `build-skills.py` from canonical `skills/`.
- Adapter archives were generated into `/tmp/tmp.cG1mr7T4PH`, outside tracked source.
- `dist/adapters/` was not edited by this milestone.
- Historical adapter archives were not rewritten.

## Token-Cost Evidence

Measurement command:

```bash
python scripts/measure-skill-tokens.py
```

Result summary:

```text
skills_measured: 23
total_bytes: 250524
total_estimated_tokens: 62619
token_estimate: approximate local estimate
```

The table below separates common-path `SKILL.md` body size from total packaged footprint for the first-slice review skills. Token estimates use the repository script's approximate `bytes / 4` method.

| Skill | Baseline `SKILL.md` est. tokens | Current `SKILL.md` est. tokens | Delta | Baseline packaged est. tokens | Current packaged est. tokens | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `code-review` | 5553 | 5600 | +47 | 5553 | 5969 | +416 |
| `proposal-review` | 3468 | 3499 | +31 | 3832 | 3873 | +41 |
| `spec-review` | 2269 | 2301 | +32 | 2571 | 2628 | +57 |

| Skill | Baseline `SKILL.md` bytes | Current `SKILL.md` bytes | Delta | Baseline packaged bytes | Current packaged bytes | Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `code-review` | 22214 | 22402 | +188 | 22214 | 23877 | +1663 |
| `proposal-review` | 13875 | 13998 | +123 | 15331 | 15494 | +163 |
| `spec-review` | 9077 | 9206 | +129 | 10287 | 10514 | +227 |

Interpretation:

- Common-path `SKILL.md` size and total packaged footprint are recorded separately.
- Total packaged footprint grows because assets are packaged explicitly.
- This milestone does not treat total-footprint growth as a regression by itself; the approved spec prioritizes parser-shaped findings and common-path readability over total-token reduction.

Asset usage expectations:

| Skill | `material-finding.md` use | `review-result-skeleton.md` use |
| --- | --- | --- |
| `code-review` | Copy once per material finding. | Copy once per code-review result block. |
| `proposal-review` | Copy once per material finding. | Copy once per proposal-review result block. |
| `spec-review` | Copy once per material finding. | Copy once per spec-review result block. |

## Cold-Read Proof

Cold-read source:

- Generated mirror `SKILL.md` files under `/tmp/tmp.3BHe2rlC2g`.
- Packaged assets under each generated mirror skill's `assets/` directory.

Observed instructions:

- Each first-slice review skill has a Resource map instructing the reviewer to `COPY assets/material-finding.md` once per material finding.
- Each Resource map instructs the reviewer to fill `Finding ID`, `Severity`, `Location`, `Evidence`, `Required outcome`, and `Safe resolution path`.
- Each Resource map instructs the reviewer to confirm the literal `Finding ID:` line exists before linking the finding from `review-log.md` or `review-resolution.md`.
- Each first-slice review skill has a Resource map instructing the reviewer to `COPY assets/review-result-skeleton.md` as the result block.

Representative filled finding a cold reader can produce from the installed asset:

```md
## Finding RSF-COLD-1

- Finding ID: RSF-COLD-1
- Severity: major
- Location: `skills/code-review/SKILL.md`
- Evidence: The copied asset contains the parser-owned `Finding ID:` label and non-blank value.
- Required outcome: Keep the parser-owned field labels intact when recording the finding.
- Safe resolution path: Start from `assets/material-finding.md`, fill every placeholder, and run review-artifact structure validation.
- needs-decision rationale: none
```

No unfilled placeholders appear in the representative filled finding.

Conclusion: installed skill text plus packaged assets are sufficient for a reviewer to produce a parser-shaped material finding without repository-maintainer context.

## Scope Boundary Proof

The diff from the branch base changes:

- review-family canonical skill text/assets for `code-review`, `proposal-review`, and `spec-review`;
- deterministic validator and fixture tests;
- proposal/spec/test-spec/plan/change-local lifecycle evidence.

The diff does not change:

- `plan-review`, `architecture-review`, or other deferred `*-review` skills;
- packaged `references/`;
- packaged `scripts/`;
- build-time partials;
- adapter install roots;
- lockfile semantics;
- CLI behavior;
- tracked generated public adapter output;
- historical adapter archives.

## Follow-On Triggers

Referential-integrity validation remains deferred. A future validator check must be proposed if the cross-file-reference failure recurs once after this slice ships, or if the next review-artifact learn session cites the same failure.

Build-time partials remain deferred. A future build-time partials proposal should be created when another shared review concept needs single-sourcing or when a checked material-finding copy drifts despite the parser-conformance and byte-identical field-block checks.
