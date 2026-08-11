# M3 Package Proof

Milestone: M3
Date: 2026-08-10
Status: implementation proof complete; review pending

## Canonical and generated proof

| Command | Result |
| --- | --- |
| `python scripts/test-adapter-distribution.py` | pass; existing archive, resource, drift, and clean-install regressions passed |
| CMD6 with approved trusted fixture `v0.3.6` | pass; Codex, Claude, and opencode archives built and clean installs validated with `--skill code-review` |
| `python scripts/validate-skills.py skills/code-review/SKILL.md` | pass |
| `python scripts/test-skill-validator.py` | pass; 290 tests, 16 governed skips |
| `python scripts/build-skills.py --check` | pass; temporary generated skill tree validated |

CMD6 created one Python-owned temporary output root, built three local archives,
installed each into a separate empty temporary target project, and validated the
selected `code-review` mapped resources. The command removed its temporary
trees on exit and did not access a network, publish artifacts, send prompts, or
execute Codex, Claude Code, or opencode.

## Trust-root correction evidence

The initially approved synthetic identity
`0.0.0-code-review-simplification` built all archives but failed every
clean-install target before mutation with `metadata-trust-root-unavailable`.
The test-spec-owned R3 correction selected immutable fixture `v0.3.6`, already
used by repository clean-install tests. Test-spec-review R3 approved that
substantive command correction before final M3 reliance. The corrected exact
CMD6 then passed all targets.

## Resource identity

The selected package contains these four mapped resources at identical logical
paths for canonical and supported generated/install targets:

- `references/boundary-first-method-v1.md`
- `references/workflow-managed-automated-review.md`
- `assets/material-finding.md`
- `assets/review-result-skeleton.md`

Existing adapter tests reject missing or stale mapped-resource bytes, resource
path escape, incomplete archives, and non-installing commands. CMD6 directly
selects the changed skill, so generic package success cannot mask omission of
the new automation reference.

## Rollback and compatibility

The atomic rollback unit remains the complete canonical `skills/code-review/`
package. Restoring the prior commit and regenerating adapters removes the new
mapping and reference together; mixed old/new resource sets fail existing
resource inventory and parity checks. Historical review artifacts need no
migration because native status, severity, finding, recording, and handoff
vocabularies are unchanged.

## Handoff

Canonical, generated, archive, and temporary installed-tree proof is complete.
Final acceptance still requires the M3 semantic review and code-review record;
this artifact does not claim verify readiness.
