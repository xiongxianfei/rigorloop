# Broad-Smoke Safe Parallelism Review Resolution

## Scope

This record tracks review finding closeout for the broad-smoke safe parallelism change.

Closeout status: closed

Review closeout: proposal-review-r1
Review closeout: proposal-review-r2
Review closeout: spec-review-r1
Review closeout: plan-review-r1
Review closeout: test-spec-review-r1
Review closeout: code-review-m1-r1
Review closeout: code-review-m1-r2
Review closeout: code-review-m2-r1

## Resolution Entries

### proposal-review-r1

No material findings.

### proposal-review-r2

No material findings.

### spec-review-r1

No material findings.

### plan-review-r1

No material findings.

### test-spec-review-r1

No material findings.

### code-review-m1-r1

#### CR-M1-1 - Undeclared PyYAML dependency in M1 validation path

Finding ID: CR-M1-1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: review-resolution
Stop state: Re-review required after resolution before M1 can close.
Chosen action: Remove the undeclared PyYAML dependency from the M1 validator and tests while preserving classification freshness and baseline artifact validation.
Rationale: The validator is selected by repository CI, so ordinary contributor validation must not depend on undeclared third-party packages.
Validation target: `python scripts/validate-broad-smoke-classification.py`; `python scripts/test-select-validation.py -k broad_smoke`; `python scripts/test-select-validation.py -k registered_change_evidence`; selected explicit CI for M1 paths.
Validation evidence: `python scripts/validate-broad-smoke-classification.py` passed; `python scripts/test-select-validation.py -k broad_smoke` passed with 17 tests; `python scripts/test-select-validation.py -k registered_change_evidence` passed with 5 tests; `rg -n "^import yaml|from yaml|yaml\\.safe" scripts docs/changes/2026-06-27-broad-smoke-safe-parallelism` returned no matches.

### code-review-m1-r2

No material findings.

### code-review-m2-r1

#### CR-M2-1 - Missing worker-result evidence can be skipped

Finding ID: CR-M2-1
Disposition: accepted
Status: resolved
Owner: implement
Owning stage: review-resolution
Stop state: Re-review required after resolution before M2 can close.
Chosen action: Track expected opt-in broad-smoke child result slots, fail closed on missing or incomplete result metadata, and add a scheduler-error regression fixture.
Rationale: Broad-smoke is boundary evidence; a required child that never produced result evidence must not be omitted from the aggregate proof.
Validation target: `python scripts/test-select-validation.py -k broad_smoke`; `python scripts/test-select-validation.py -k jobs`; `bash -n scripts/ci.sh`; selected explicit CI for M2 paths.
Validation evidence: `python scripts/test-select-validation.py -k worker_crash` passed with 1 test; `python scripts/test-select-validation.py -k broad_smoke` passed with 24 tests; `python scripts/test-select-validation.py -k jobs` passed with 5 tests; `bash -n scripts/ci.sh` passed; `python scripts/validate-broad-smoke-classification.py` passed.
