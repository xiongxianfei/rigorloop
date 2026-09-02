# Specification authoring evidence

Artifact path: specs/impact-aware-final-verification.md
Artifact identity: sha256:3aa7aeb6e8b3fd97ef033f5e01da12b313fa65f562934ff67d24f58eac4857e6
Authoring result: complete

The specification defines the v3 lifecycle, impact and freshness vocabularies, evidence applicability, always-current checks, failure and correction behavior, successful report and explanation contract, Verify evidence-tail identity, PR consumption, progressive disclosure, historical compatibility, coherent activation, and fail-closed validation. Its boundary-first record classifies all eight core dimensions, four material interactions, and every behavioral example.

Validation note: `python scripts/validate-boundary-first.py --check --path specs/impact-aware-final-verification.md` currently rejects `stage-owned-change-local-v2` and requires a matching test spec. Those expectations conflict with the active v2 lifecycle contract in `CONSTITUTION.md`, `AGENTS.md`, and the accepted no-test-spec design. No test spec was created; Design Review must treat this as stale validator behavior to be allocated by Delivery rather than a specification omission.
