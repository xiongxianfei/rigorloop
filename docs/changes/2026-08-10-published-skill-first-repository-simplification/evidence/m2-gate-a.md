# M2 Gate A Evidence

## Result

`python scripts/validate-skills.py` is the single contributor-facing Gate A
command. Its stable result name is `Gate A (canonical skill integrity)`. The
shared `skill_validation` module remains its parser and invariant owner;
`test-skill-validator.py`, `build-skills.py --check`, and the boundary-first
check are regression, derived-output, and governed-projection proof rather than
competing canonical-skill gate CLIs.

Gate A uses repository-local structure, schema, resource, path, closed-value,
placeholder, forbidden-claim, and byte/projection facts. It starts no target
runtime and does not score semantic skill quality. A structurally valid skill
whose description and procedure are intentionally ambiguous passes Gate A,
which directly proves the boundary instead of relying on a prose-policy claim.

## MP1 semantic review

Review target: `skills/code-review/SKILL.md` and its mapped resources under
`skills/code-review/assets/` and `skills/code-review/references/`.

Reviewer environment: local tracked canonical skill and packaged resources;
no generated adapter, runtime, prompt, transcript, or model output was used.

Checklist result:

- Description and trigger clarity: pass; the description names implementation
  review, its inputs, and adjacent gates.
- Ownership: pass; the skill reviews and records findings but leaves fixes,
  lifecycle mutation, verification, and PR readiness to their owners.
- Prerequisites and inputs: pass; actual diff, governing artifacts, tests, and
  evidence are explicit.
- Procedure: pass; the quick guide, boundary scan, checklist, independent gate,
  fidelity gate, and recording rules are executable without hidden repository
  knowledge.
- Resources: pass; mapped material-finding and result assets have explicit COPY
  behavior, and the boundary reference has explicit READ behavior.
- Stop conditions: pass; missing diff, tests, tracked authority, or owner
  decision stops clean handoff.
- Claim boundaries: pass; branch, PR, CI, verification, implementation-fix, and
  generated-currency claims are explicitly excluded.
- Output and handoff: pass; the result skeleton and milestone-aware routing
  name the review result and next responsible stage.

Material semantic findings: none. This is a judgment record; the structural
test for the checklist's presence is not treated as semantic approval.

## Test-first evidence

The new ambiguous-prose test initially failed only because the Gate A command
did not expose its stable owner name. After adding that output contract, the
same ambiguous skill passed. The runtime-dependency and semantic-checklist
tests were green without adding a model or heuristic oracle.

## Validation

- `python scripts/validate-skills.py` — pass; 24 canonical skills.
- `python scripts/test-skill-validator.py` — pass; 288 tests, 16 skipped.
- `python scripts/build-skills.py --check` — pass using temporary generated output.
- `python scripts/validate-boundary-first.py --check` — pass; active v0.4.0 projection and v0.3.6 rollback artifacts reported.
- Targeted Gate A tests — pass; ambiguous prose accepted and no target-runtime dependency found.

## Rollback

Revert the M2 commit to restore the prior success/error prefix and remove the
review checklist. No deterministic invariant, adapter package, or acceptance
invocation is deleted by this milestone.
