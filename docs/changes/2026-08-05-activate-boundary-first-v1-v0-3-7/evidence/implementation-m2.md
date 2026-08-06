# M2 implementation evidence

Milestone: M2 — Guarded atomic activation publication helper

Outcome: R1 findings recorded; corrections implemented for code review R2.

## Implemented behavior

- Added mutually exclusive `--check` and `--publish` CLI modes for the exact
  approved `v0.4.0` candidate-evidence path.
- Readiness composes the settled lifecycle gate, strict tagged authority,
  stored `R -> C` provenance, fresh live `H`, exact remote `main == P`, absent
  remote tag, local `v0.4.0 -> T`, and fast-forward authority.
- Check mode performs an atomic dry run and leaves both refs unchanged.
- Publish mode recomputes readiness in the same invocation, retains the exact
  full `H` and `T` identities, rejects local-head drift, and issues one plain
  non-forced `git push --atomic` with no sequential fallback.
- An isolated pre-push guard validates Git's exact same-push advertised old
  identities and exact H/T destinations, then re-queries remote main and tag as
  defense in depth before both dry-run and real pushes.
- Successful publication freshly confirms both remote refs. Failures preserve
  bounded classification plus safe available P/B/T/R/H context, invariant, and
  corrective action while keeping provider diagnostics private.
- Candidate evidence is accepted only through the exact canonical lexical path;
  symlink, normalized alias, and symlinked canonical paths fail closed.
- Registered the helper and tests as a first-class selector-owned boundary
  activation regression surface.

## Proof coverage

Local bare-remote fixtures prove read-only check mode, exact two-ref success,
one-ref receive rejection with all-or-neither refs, stale remote main, existing
remote tag, real advertised-atomic capability failure, post-readiness remote
drift, local-head movement, non-fast-forward H, and modified candidate evidence.
Focused contract fixtures prove same-push stdin mismatch rejection, exact
full-SHA refspecs, absence of force/fallback flags, explicit and successful CLI
modes, canonical path authority, and private diagnostic suppression. The
selector fixture proves all three new paths route to the owned regression.

## Validation

- `python scripts/test-boundary-activation-release.py` — pass, 12 tests.
- `python scripts/test-select-validation.py` — pass, 147 tests.
- `python -m py_compile scripts/boundary_activation_release.py scripts/publish-boundary-activation.py` — pass.
- `python scripts/select-validation.py --mode explicit --path scripts/boundary_activation_release.py --path scripts/publish-boundary-activation.py --path scripts/test-boundary-activation-release.py --path scripts/validation_selection.py --path scripts/test-select-validation.py` — pass; selected boundary validation, activation publication regression, and selector regression without blockers or debt.
- `git diff --check --cached` — pass.

No configured external remote, public ref, release, or package was mutated.
