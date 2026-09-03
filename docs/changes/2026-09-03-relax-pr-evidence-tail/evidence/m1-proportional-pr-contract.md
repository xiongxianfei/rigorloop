# M1 implementation evidence: Proportional PR evidence suffix

Milestone: M1
Subject path: docs/plans/2026-09-03-relax-pr-evidence-tail.md
Subject identity: sha256:9b762060e3022f6d0310ad8197ff363c92228c3bb89ff3d92d59935541bf4494
Validation result: passed

## Result

- Skill: implement
- Status: implemented
- Completed scope: proportional cumulative PR evidence-suffix classification, current-authority and product-boundary guards, the narrower Verify-result distinction, and focused fail-closed tests
- Artifacts changed: `skills/pr/SKILL.md`, `skills/pr/references/governed-pr-readiness.md`, `skills/verify/references/successful-explanation-v3.md`, and `scripts/test-skill-validator.py`
- Open blockers: none
- Next stage: code-review
- Claim limitations: this evidence does not claim Code Review acceptance, milestone closeout, final verification, branch readiness, PR readiness, or generated adapter currency

## Test-first evidence

Before the canonical skill changes, the focused `PRSkillSimplificationTests` failed because the package retained the exact one-direct-child rule and lacked the closed `evidence suffix` vocabulary, proportional current-authority rules, negative classifications, and explicit Verify-result distinction. After implementation, the focused suite passed. The complete validator then exposed required legacy claim phrases and the no-downstream-continuation phrase; both were restored without changing the new rule, after which all 364 tests passed.

## Validation results

- `python scripts/test-skill-validator.py` — passed initially with 364 tests and after review correction with 365 tests.
- `python scripts/validate-skills.py` — passed, 20 canonical skills.
- `python scripts/build-skills.py --check` — passed with temporary generated output.
- `python scripts/validate-boundary-first.py --check --path specs/relax-pr-evidence-tail.md` — passed.
- `git diff --check` — passed.
- `wc -c -w skills/pr/SKILL.md skills/pr/references/governed-pr-readiness.md` — 11,746 bytes and 1,536 words combined, within the existing package limit.

Code Review R1 recorded PRTAIL-M1-CR1 because compacting for the package ceiling removed unaffected governed-signal, retry-reconciliation, body-policy, exact result-field, and current-evidence clauses. A new focused preservation test failed before correction. The exact clauses were restored, semantically neutral reference wording was tightened, and the complete M1 validation set passed with 365 tests. The final package remains 11,746 bytes and is now 1,536 words.

## Contract evidence

- The verified subject must equal or precede the handoff. A non-ancestor fails closed.
- The cumulative final diff has the closed outcomes `none`, `evidence-only`, and `invalidating`; unknown values fail before consistency checks.
- Any commit count and direct-parent topology may qualify only when the complete suffix is current, attributable final-review, workflow, and Verify evidence.
- Paths, file names, commit messages, and author identity grant no authority.
- Protected product and governed-contract surfaces, mixed or unknown content, stale evidence, cross-change evidence, and unattributable content invalidate readiness before external mutation and route to the applicable owner and fresh Verify.
- Verify still owns `branch-ready`. Its registered result remains exactly the successful report plus `change.yaml#lifecycle_cli.validations.verify-result`; broader final-review and workflow evidence are PR classification inputs, not Verify registration.

## Changed and unaffected surfaces

- Changed: the canonical PR safety predicate, governed readiness detail, coupled Verify wording, and public-contract regressions.
- Unaffected: the prior governed PR specification remains read-only; the approved focused specification supersedes only its named clauses.
- Unaffected: remote identity, push, PR selection, hosted CI, retry, draft, refresh, read-back, lifecycle ownership, and external mutation behavior retain their prior authority.
- Deferred to M2: deterministic supported-adapter candidates and current unpublished candidate metadata parity.

## Recovery

Revert the M1 skill, reference, and test changes as one unit. Do not retain mixed PR and Verify interpretations. No external state, release archive, or generated adapter body was changed by M1.
