# Behavior Preservation

Change ID: 2026-06-29-release-transaction-automation
Milestone: M6. Published evidence closeout and behavior preservation
Status: current

## Preservation Matrix

| Surface | Baseline | M6 proof | Result |
| --- | --- | --- | --- |
| Full release verification | `release-verify.sh <tag>` remains the local release gate. | M5 kept the command set unchanged; M6 only adds published evidence validation when npm publication evidence is already marked `Status: published`. | preserved |
| GitHub release evidence | Public release asset evidence was validator-checked manually. | `close-release-publication` requires public asset URL and `sha256:<hex>` archive hash per target before writing published evidence. | strengthened |
| npm publication evidence | npm publication fields were hand-authored and validator checked. | `close-release-publication` requires npm package URL, tarball, integrity, published time, and latest dist-tag before writing `Status: published`. | strengthened |
| Public npx smoke | Public smoke is required after publication. | Closeout evidence requires version smoke and `init codex`, `init claude`, and `init opencode` smoke rows with exact `npx @xiongxianfei/rigorloop@<version> ...` command shapes. | preserved |
| Adapter metadata and archive integrity | Adapter archive metadata remains release-gate-owned. | M6 records public archive URLs and archive hashes but does not weaken adapter archive generation or release verification. | preserved |
| Tree hash and file count evidence | Published evidence must use validator-compatible shapes. | Published validation rejects raw tree hashes and nonnumeric file counts; opencode root-qualified hashes and counts are preserved. | strengthened |
| Historical release evidence | Routine release automation must not rewrite historical evidence. | M6 closeout tests prove `docs/releases/v0.3.4/release.yaml` remains unchanged while closing `v0.3.5`. | preserved |
| Release timing | Timing evidence is durable release evidence. | M6 leaves timing schema and validation unchanged; closeout timing remains represented by the existing `public_closeout` phase. | preserved |
| External wait | Public GitHub/npm evidence may be unavailable immediately. | Closeout fails clearly when public evidence is unavailable and does not modify release files. | preserved |

## Validation Evidence

- `python scripts/test-release-transaction.py` passed with M6 closeout and published-validation coverage.
- `python scripts/close-release-publication.py --help` passed.
- `python -m py_compile scripts/release_transaction.py scripts/test-release-transaction.py scripts/prepare-release.py scripts/release-preflight.py scripts/validate-release.py scripts/close-release-publication.py` passed.
- Selector validation for M6 paths selected adapter/release regression and remains blocked only on known manual routing for release transaction scripts.
- Selected adapter/release regression passed.
