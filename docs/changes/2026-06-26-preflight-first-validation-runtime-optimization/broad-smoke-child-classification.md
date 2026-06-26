# Broad-Smoke Child Classification

## Scope

- Milestone: M3. Broad-Smoke Child Classification
- Source command: `bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped`
- Classification source: `scripts/ci.sh` `run_broad_smoke`
- Execution behavior changed: no
- Broad-smoke parallel execution enabled: no
- Cache behavior changed: no
- Validator composition changed: no
- Final verify, branch readiness, PR readiness, or hosted CI success claimed: no

## Classification

| Check ID | Command | Reads | Writes | Temp roots | Shared outputs | Network use | CPU/I/O expectations | Nested parallelism risk | Output-order risk | Failure-output dependency | Parallel-safe candidate | Classification confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| broad_smoke.skills.validate | python scripts/validate-skills.py | skill source and skill contract inputs | none | none | none | none expected | CPU low, IO low | none known | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | high |
| broad_smoke.skills.regression | python scripts/test-skill-validator.py | skill validator fixtures and source | none | test-managed temp roots | none | none expected | CPU medium, IO medium | test runner may manage fixture temp state | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | high |
| broad_smoke.skills.generation_regression | python scripts/test-build-skills.py | skill source and generation fixtures | test-managed temp roots | test-managed temp roots | none | none expected | CPU medium, IO medium | test runner may manage fixture temp state | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | high |
| broad_smoke.skills.drift | python scripts/build-skills.py --check | skill source and generated mirror expectations | none | none | none | none expected | CPU medium, IO medium | none known | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | high |
| broad_smoke.adapters.regression | python scripts/test-adapter-distribution.py | adapter source, distribution fixtures, and release metadata fixtures | test-managed temp roots | test-managed temp roots | possible build fixture outputs | none expected | CPU high, IO high | test runner may build archives in temp roots | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | no | high |
| broad_smoke.adapters.build_archives | python scripts/build-adapters.py --version v0.1.3 --output-dir "$adapter_release_output" | adapter source and release metadata | "$adapter_release_output" | "$adapter_release_output" | "$adapter_release_output" | none expected | CPU medium, IO high | shares output root with archive validation child | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | no | high |
| broad_smoke.adapters.validate_archives | python scripts/validate-adapters.py --root "$adapter_release_output" --version v0.1.3 | "$adapter_release_output" | none | "$adapter_release_output" | "$adapter_release_output" | none expected | CPU low, IO medium | depends on previous archive build output | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | no | high |
| broad_smoke.change_metadata.regression | python scripts/test-change-metadata-validator.py | change metadata validator fixtures and source | test-managed temp roots | test-managed temp roots | none | none expected | CPU low, IO medium | test runner may manage fixture temp state | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | high |
| broad_smoke.artifact_lifecycle.regression | python scripts/test-artifact-lifecycle-validator.py | artifact lifecycle fixtures and source | test-managed temp roots | test-managed temp roots | none | none expected | CPU medium, IO medium | test runner may manage fixture temp state | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | high |
| broad_smoke.review_artifacts.regression | python scripts/test-review-artifact-validator.py | review artifact fixtures and source | test-managed temp roots | test-managed temp roots | none | none expected | CPU medium, IO medium | test runner may manage fixture temp state | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | high |
| broad_smoke.review_artifacts.changed_roots | "${review_artifact_cmd[@]}" | changed review artifact roots when present | none | none | none | none expected | CPU low, IO low | command is conditional on changed roots | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | medium |
| broad_smoke.artifact_lifecycle.scoped | "${artifact_lifecycle_cmd[@]}" | tracked diff paths or HEAD~1..HEAD lifecycle scope | none | none | none | none expected | CPU medium, IO medium | command scope depends on skip-diff-scoped and Git state | sequential output currently preserved by run_check | captured output and rerun command must stay attached to this check | needs-follow-up | medium |

## Sequential Execution Proof

- `scripts/ci.sh` broad-smoke still calls `run_check` directly for each child.
- `run_broad_smoke` does not call `ThreadPoolExecutor`, `run_parallel_safe_chunk`, or `parallel_safe`.
- No broad-smoke child is launched in the background.
- `run_check` still captures each child command output and prints failure output with the failing check's label, command, captured output, and rerun command.
- The adapter archive validation child intentionally depends on the archive build child's temp output root, so those checks are not parallel-safe candidates.

## Follow-Up Recommendation

Do not enable broad-smoke parallel execution from this slice. A later approved slice may consume this inventory, but it must provide dedicated side-effect proof, scratch-root separation, output-order proof, and resource-budget evidence before marking any child as parallel-safe for execution.
