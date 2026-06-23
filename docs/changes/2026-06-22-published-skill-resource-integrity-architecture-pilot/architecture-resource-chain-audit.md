# Architecture Resource-Chain Audit

## Status

active

## Scope

This audit records the pre-change architecture skill resource-chain baseline for
M1 of the published-skill resource-integrity architecture pilot.

No architecture resource reference, architecture skill-local file, generated
adapter content, archive layout, or installation behavior was changed during
this audit.

## Inputs

- Canonical architecture skill source: `skills/architecture/`
- Root repository scaffolds referenced by the skill body:
  - `templates/architecture.md`
  - `templates/diagram-styles.mmd`
  - `templates/adr.md`
- Generated local mirror: `/tmp/rigorloop-sri-audit-generated-skills`
- Adapter/release-candidate archives: `/tmp/rigorloop-sri-audit-release-output`
- Clean Codex install root: `/tmp/rigorloop-sri-codex-install-OMUt72`
- Clean Claude install root: `/tmp/rigorloop-sri-claude-install-wEPh6X`
- Clean opencode install root: `/tmp/rigorloop-sri-opencode-install-upH2TG`

The temporary paths are recorded as replay evidence for this diagnostic audit.
They are not package inputs and are not required by the implementation.

## Referenced Resources

`skills/architecture/SKILL.md` references legacy template paths outside a
`Resource map`:

| Line | Reference |
| ---: | --- |
| 123 | `templates/architecture.md`, `templates/diagram-styles.mmd`, `templates/adr.md` |
| 154 | `templates/diagram-styles.mmd` |
| 196 | `templates/adr.md` |

The root repository templates exist, but they are not under
`skills/architecture/` and are therefore not packageable skill-local resources.

| Root template | Raw SHA-256 |
| --- | --- |
| `templates/architecture.md` | `b6f849778ad1ce2a206ba97de50e03aa181bf931282087251f5ec0d90aaafda0` |
| `templates/diagram-styles.mmd` | `020be16bb4b01f1eb1a1605562ffd6b31af9e5ba2ee12b1a1e1735acb6378a56` |
| `templates/adr.md` | `67bb852acb50e4804c3d4e5ad0241c175d2b6a0b8453a21ec9eb185cc098f1ad` |

## Inventory Matrix

| Layer | Candidate/source | Expected resource | Actual result | Raw SHA-256 | Status |
| --- | --- | --- | --- | --- | --- |
| Canonical skill source | `skills/architecture/` | `SKILL.md` | present | `676ee4ef94389e89f61f8aa06ced8f2d9f383b66877dc330fddeefe315c8d48e` | pass |
| Canonical skill source | `skills/architecture/` | `templates/architecture.md` | missing from skill root; root `templates/architecture.md` exists outside skill root | N/A for skill-local resource | fail |
| Canonical skill source | `skills/architecture/` | `templates/diagram-styles.mmd` | missing from skill root; root `templates/diagram-styles.mmd` exists outside skill root | N/A for skill-local resource | fail |
| Canonical skill source | `skills/architecture/` | `templates/adr.md` | missing from skill root; root `templates/adr.md` exists outside skill root | N/A for skill-local resource | fail |
| Generated local mirror | `/tmp/rigorloop-sri-audit-generated-skills/architecture/` | `SKILL.md` | present | `676ee4ef94389e89f61f8aa06ced8f2d9f383b66877dc330fddeefe315c8d48e` | pass |
| Generated local mirror | `/tmp/rigorloop-sri-audit-generated-skills/architecture/` | `templates/architecture.md` | missing | N/A | fail |
| Generated local mirror | `/tmp/rigorloop-sri-audit-generated-skills/architecture/` | `templates/diagram-styles.mmd` | missing | N/A | fail |
| Generated local mirror | `/tmp/rigorloop-sri-audit-generated-skills/architecture/` | `templates/adr.md` | missing | N/A | fail |
| Codex adapter/archive | `/tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-codex-v0.3.2.zip` | `.agents/skills/architecture/SKILL.md` | present | `676ee4ef94389e89f61f8aa06ced8f2d9f383b66877dc330fddeefe315c8d48e` | pass |
| Codex adapter/archive | same archive | `.agents/skills/architecture/templates/architecture.md` | missing | N/A | fail |
| Codex adapter/archive | same archive | `.agents/skills/architecture/templates/diagram-styles.mmd` | missing | N/A | fail |
| Codex adapter/archive | same archive | `.agents/skills/architecture/templates/adr.md` | missing | N/A | fail |
| Claude adapter/archive | `/tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-claude-v0.3.2.zip` | `.claude/skills/architecture/SKILL.md` | present | `afd65409f84f9d1fb7c7cc434889973fd72f7ad80584d3b670bb69ba7d4c7e45` | pass |
| Claude adapter/archive | same archive | `.claude/skills/architecture/templates/architecture.md` | missing | N/A | fail |
| Claude adapter/archive | same archive | `.claude/skills/architecture/templates/diagram-styles.mmd` | missing | N/A | fail |
| Claude adapter/archive | same archive | `.claude/skills/architecture/templates/adr.md` | missing | N/A | fail |
| opencode adapter/archive | `/tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-opencode-v0.3.2.zip` | `.opencode/skills/architecture/SKILL.md` | present | `afd65409f84f9d1fb7c7cc434889973fd72f7ad80584d3b670bb69ba7d4c7e45` | pass |
| opencode adapter/archive | same archive | `.opencode/skills/architecture/templates/architecture.md` | missing | N/A | fail |
| opencode adapter/archive | same archive | `.opencode/skills/architecture/templates/diagram-styles.mmd` | missing | N/A | fail |
| opencode adapter/archive | same archive | `.opencode/skills/architecture/templates/adr.md` | missing | N/A | fail |
| Clean Codex install | `/tmp/rigorloop-sri-codex-install-OMUt72/.agents/skills/architecture/` | `SKILL.md` | present | `676ee4ef94389e89f61f8aa06ced8f2d9f383b66877dc330fddeefe315c8d48e` | pass |
| Clean Codex install | same install root | `templates/architecture.md` | missing | N/A | fail |
| Clean Codex install | same install root | `templates/diagram-styles.mmd` | missing | N/A | fail |
| Clean Codex install | same install root | `templates/adr.md` | missing | N/A | fail |
| Clean Claude install | `/tmp/rigorloop-sri-claude-install-wEPh6X/.claude/skills/architecture/` | `SKILL.md` | present | `afd65409f84f9d1fb7c7cc434889973fd72f7ad80584d3b670bb69ba7d4c7e45` | pass |
| Clean Claude install | same install root | `templates/architecture.md` | missing | N/A | fail |
| Clean Claude install | same install root | `templates/diagram-styles.mmd` | missing | N/A | fail |
| Clean Claude install | same install root | `templates/adr.md` | missing | N/A | fail |
| Clean opencode install | `/tmp/rigorloop-sri-opencode-install-upH2TG/.opencode/skills/architecture/` | `SKILL.md` | present | `afd65409f84f9d1fb7c7cc434889973fd72f7ad80584d3b670bb69ba7d4c7e45` | pass |
| Clean opencode install | same install root | `templates/architecture.md` | missing | N/A | fail |
| Clean opencode install | same install root | `templates/diagram-styles.mmd` | missing | N/A | fail |
| Clean opencode install | same install root | `templates/adr.md` | missing | N/A | fail |

## Layer Summary

| Layer | Architecture skill file inventory | Result |
| --- | --- | --- |
| Canonical skill source | `SKILL.md` only | fail: legacy references are absent from skill root |
| Generated local mirror | `SKILL.md` only | preserves canonical inventory |
| Codex adapter/archive | `SKILL.md` only | preserves canonical/generated inventory |
| Claude adapter/archive | `SKILL.md` only | preserves canonical/generated inventory |
| opencode adapter/archive | `SKILL.md` only | preserves canonical/generated inventory |
| Clean Codex install | `SKILL.md` only | reproduces observed missing-resource install state |
| Clean Claude install | `SKILL.md` only | same missing-resource state |
| Clean opencode install | `SKILL.md` only | same missing-resource state |

## Findings

- First divergent layer: canonical skill source. `skills/architecture/SKILL.md`
  references `templates/architecture.md`, `templates/diagram-styles.mmd`, and
  `templates/adr.md`, but `skills/architecture/` contains only `SKILL.md`.
- Local observed installation was reproducible. Clean Codex installation from a
  locally packed `v0.3.2` candidate produced
  `.agents/skills/architecture/SKILL.md` without the referenced template files.
- The defect predates package assembly. The generated local mirror, adapter
  archives, and installed target trees preserve the canonical architecture skill
  inventory; they do not independently drop architecture skill-local resources.
- No layer was unproved. Codex, Claude, and opencode clean-installed target
  trees were inspected.
- Claude and opencode architecture `SKILL.md` hashes differ from Codex because
  adapter generation transforms skill bodies for target portability, but all
  transformed bodies still contain the same legacy `templates/...` references.
- The opencode install completed with warning
  `opencode-command-aliases-not-declared`; the architecture skill root was still
  installed and inspected.

## Commands Used

```sh
python scripts/build-skills.py --check
python scripts/build-skills.py --output-dir /tmp/rigorloop-sri-audit-generated-skills
python scripts/build-adapters.py --version v0.3.2 --output-dir /tmp/rigorloop-sri-audit-release-output
python scripts/validate-adapters.py --version v0.3.2 --root /tmp/rigorloop-sri-audit-release-output
node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init codex --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-codex-v0.3.2.zip --json
node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init claude --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-claude-v0.3.2.zip --json
node /home/xiongxianfei/data/20260419-rigorloop/packages/rigorloop/dist/bin/rigorloop.js init opencode --from-archive /tmp/rigorloop-sri-audit-release-output/rigorloop-adapter-opencode-v0.3.2.zip --json
find skills/architecture -type f -printf '%P\n' | sort
find /tmp/rigorloop-sri-audit-generated-skills/architecture -type f -printf '%P\n' | sort
find /tmp/rigorloop-sri-codex-install-OMUt72/.agents/skills/architecture -type f -printf '%P\n' | sort
find /tmp/rigorloop-sri-claude-install-wEPh6X/.claude/skills/architecture -type f -printf '%P\n' | sort
find /tmp/rigorloop-sri-opencode-install-upH2TG/.opencode/skills/architecture -type f -printf '%P\n' | sort
sha256sum skills/architecture/SKILL.md templates/architecture.md templates/diagram-styles.mmd templates/adr.md /tmp/rigorloop-sri-audit-generated-skills/architecture/SKILL.md /tmp/rigorloop-sri-codex-install-OMUt72/.agents/skills/architecture/SKILL.md /tmp/rigorloop-sri-claude-install-wEPh6X/.claude/skills/architecture/SKILL.md /tmp/rigorloop-sri-opencode-install-upH2TG/.opencode/skills/architecture/SKILL.md
```

Archive entry inventory and SHA-256 checks used Python's standard `zipfile`
reader because `zipinfo` is not installed in this environment.

## Temporary Roots Used

| Purpose | Path |
| --- | --- |
| Generated local mirror | `/tmp/rigorloop-sri-audit-generated-skills` |
| Release-candidate archives | `/tmp/rigorloop-sri-audit-release-output` |
| Clean Codex install | `/tmp/rigorloop-sri-codex-install-OMUt72` |
| Clean Claude install | `/tmp/rigorloop-sri-claude-install-wEPh6X` |
| Clean opencode install | `/tmp/rigorloop-sri-opencode-install-upH2TG` |

## Command Interface Discovery

The approved plan named
`python scripts/validate-adapters.py --version v0.3.2 --release-output-dir ...`.
The current repository-owned interface is
`python scripts/validate-adapters.py --version v0.3.2 --root ...`, so this
audit used the supported `--root` flag.
