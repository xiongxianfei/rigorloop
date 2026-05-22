# Code Review M3 R1

Review ID: code-review-m3-r1
Stage: code-review
Round: 1
Reviewer: Codex code-review skill
Target: M3. First producer compact default and verbose compatibility in working tree
Status: changes-requested

## Review inputs

- Review surface: M3 working-tree diff for `scripts/test-change-metadata-validator.py`, `scripts/test-select-validation.py`, `behavior-preservation.md`, `script-output-layer-audit.md`, `change-metadata-validator-tests-post-m3.txt`, the active plan, plan index, and change metadata.
- Governing artifacts: `specs/script-output-optimization.md` R53 through R65 and AC23 through AC36; `specs/script-output-optimization.test.md` TSRO-021 through TSRO-025; M3 in `docs/plans/2026-05-22-broad-smoke-and-fixture-suite-output-compaction.md`.
- Validation evidence: M3 validation recorded in `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml`, including focused producer output-contract tests, direct producer default/verbose/quiet/failure/zero-test runs, selected-test hash comparison, ordinary selector regression, selected explicit CI, lifecycle validation, metadata validation, review-artifact validation, and patch hygiene.
- Related code inspected: current `scripts/test-change-metadata-validator.py` producer runner and M3 subprocess tests in `scripts/test-select-validation.py`.

## Diff summary

M3 replaces the default `unittest.main(verbosity=2)` entrypoint in `scripts/test-change-metadata-validator.py` with a producer-local runner. Default success now emits one compact `[PASS] test-change-metadata-validator` line, default failure emits a compact actionable failure summary, `--verbose` and `-v` preserve full unittest detail, `--quiet` and `-q` preserve existing unittest-compatible quiet behavior, zero selected tests fail, and a dynamic output-contract failure fixture is available only under `RIGORLOOP_CHANGE_METADATA_FAILURE_FIXTURE=1`.

The selector regression suite adds subprocess tests for producer default success, default failure, verbose detail, quiet compatibility, and zero-test behavior. M3 also records post-change producer selected-test identity evidence and updates the audit, preservation record, active plan, plan index, and change metadata.

## Findings

### BSO-M3-CR1: Recorded producer test-identity extraction command is no longer replayable

Finding ID: BSO-M3-CR1
Severity: major
Location: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/script-output-layer-audit.md:89`

Evidence: The audit records the producer selected-test identity extraction method as:

```python
spec = importlib.util.spec_from_file_location('test_change_metadata_validator', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
```

After M3, `scripts/test-change-metadata-validator.py` defines `@dataclass(frozen=True)` before the test class. Replaying the recorded extraction command now fails during `exec_module` with:

```text
AttributeError: 'NoneType' object has no attribute '__dict__'
```

because the module is not registered in `sys.modules` before executing the dataclass declaration. This does not prove the post-M3 hash is wrong, but it makes the durable proof route non-replayable from the recorded audit instructions. R62 and TSRO-024 require deterministic selected test/check identity proof before closing the producer compaction milestone.

Required outcome: The recorded producer selected-test identity extraction method must be replayable after M3 and must still produce the unchanged ordered identifier list and SHA-256 hash.

Safe resolution path: Update the documented extraction method, and any matching behavior-preservation command if added, to register the module before execution:

```python
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
```

Then rerun the extraction/hash proof, confirm the post-M3 hash remains `fbb2230ef0c90ae64d7d0eb34966b994f318d8e042ca56fabaa4d39edbbe108e`, and record the validation evidence.

### BSO-M3-CR2: Change metadata omits the primary M3 producer file

Finding ID: BSO-M3-CR2
Severity: major
Location: `docs/changes/2026-05-22-broad-smoke-and-fixture-suite-output-compaction/change.yaml:261`

Evidence: M3 modifies `scripts/test-change-metadata-validator.py`, and the active plan names that file as the locked first targeted producer. The `changed_files` list in `change.yaml` includes `scripts/ci.sh` and `scripts/test-select-validation.py`, but it does not include `scripts/test-change-metadata-validator.py`. This leaves the canonical change-local file inventory incomplete for the principal M3 implementation surface.

Required outcome: `change.yaml` must list the primary producer implementation file changed by M3.

Safe resolution path: Add `scripts/test-change-metadata-validator.py` to `changed_files`, keep the review record path included, and rerun change metadata and lifecycle validation.

## Checklist coverage

- Spec alignment: concern. The runtime producer behavior aligns with R53 through R61 based on inspected code and recorded validation, but the R62 deterministic proof surface is not replayable from the audit.
- Test coverage: pass. TSRO-021, TSRO-022, TSRO-023, and the zero-test portion of TSRO-024 have direct subprocess coverage in `scripts/test-select-validation.py`.
- Edge cases: pass. Default failure, verbose aliases, quiet compatibility aliases, and zero selected tests are covered by focused tests and recorded direct commands.
- Error handling: pass. Usage errors are bounded, default failure output includes names/messages/locations, and the dynamic failure fixture is isolated behind an environment variable.
- Architecture boundaries: pass. The implementation stays producer-local plus selector regression tests; it does not add a shared helper library or alter generated artifacts.
- Compatibility: concern. Direct runtime compatibility for `--quiet` and `-q` is preserved, but the durable change metadata omits the primary changed producer file.
- Security/privacy: pass. The diff does not add secret logging, auth changes, or broader environment dumps.
- Derived artifact currency: pass. No generated skills, adapters, public adapter packages, release artifacts, or JSON behavior changed in M3.
- Unrelated changes: pass. The runtime diff is scoped to the targeted producer and ordinary output-contract test surface.
- Validation evidence: concern. The recorded M3 validation is relevant and broad, but the replayable selected-test identity proof route and change-file inventory need correction before M3 can close.

## No-finding rationale

Not applicable; two material findings were found.

## Handoff

Reviewed milestone: M3. First producer compact default and verbose compatibility
Review status: changes-requested
Milestone closeout: resolution-needed
Required review-resolution: yes
Next stage: review-resolution for `BSO-M3-CR1` and `BSO-M3-CR2`
Remaining implementation milestones: M3 resolution, M4
Verify readiness: not-claimed
