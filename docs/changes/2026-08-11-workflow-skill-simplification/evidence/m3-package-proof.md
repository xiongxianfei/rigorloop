# M3 Workflow Package Proof

## Commands and results

The repository-owned adapter suite passed after a compatibility repair:

```text
python scripts/test-adapter-distribution.py
```

Exit status: 0. All 150 tests passed.

The first M3 run failed because the shortened common path had preserved the three Codex command literals but omitted the exact cross-adapter invocation-equivalence block consumed by the existing package analyzer. That made `workflow` appear Codex-only and caused all dependent archive and release fixtures to fail for the same reason. The repair restored the compact Codex/Claude/OpenCode equivalence block inline, removed duplicate command spans from predicate and resource prose, and added the missed semantic rule to the disposition ledger. Focused portability and archive tests passed before the complete suite was rerun.

A fresh temporary all-target build and selected workflow clean-install validation also passed:

```text
python -c 'exec("""import subprocess, sys, tempfile
version = "v0.3.6"
with tempfile.TemporaryDirectory(prefix="rigorloop-adapters-") as output:
    subprocess.run([sys.executable, "scripts/build-adapters.py", "--version", version, "--output-dir", output], check=True)
    subprocess.run([sys.executable, "scripts/validate-adapters.py", "--version", version, "--adapter-root", output, "--clean-install-smoke", "--skill", "workflow"], check=True)""")'
```

Exit status: 0. The temporary directory was automatically removed. No authored or generated repository file was changed.

## Proven package layers

The commands generated and checked all supported targets: Codex, Claude, and OpenCode. For selected `workflow`, each target contained:

```text
SKILL.md
references/governed-lifecycle-routing.md
references/bounded-workflow-automation.md
references/workflow-guide-authoring.md
references/boundary-first-method-v1.md
assets/workflows-skeleton.md
```

Existing generic mapped-resource checks compare canonical, generated, archive, and clean-installed paths and bytes. The suite also proves fail-closed behavior for stale mapped-resource hashes, missing mapped resources, archive parity mismatch, clean-install parity mismatch, unowned resources, and unknown selected skills. Therefore the new workflow references inherit direct negative omission and staleness proof from the existing resource-map owner; no workflow-specific validator family was added.

## Scope and safety

- canonical `skills/` remained the only authored source;
- no adapter archive or installed tree was hand-edited;
- no package was published and no network or external system was used;
- no Codex, Claude Code, OpenCode, or other target-agent runtime executed;
- no prompt, transcript, model selection, retry evidence, runtime hash protocol, scheduler, selector, or state store was introduced.

## Rollback proof

Rollback remains atomic: revert the canonical package and its mapped-resource declarations to the prior complete revision, then regenerate all adapter targets using existing build commands. Because archive and installed validation reject missing, stale, additional, or mismatched mapped resources, a mixed old/new package cannot pass release proof.
