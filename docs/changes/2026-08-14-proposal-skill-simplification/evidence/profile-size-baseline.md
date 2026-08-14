# Proposal Skill Simplification Profile Baseline

- Baseline revision: `aad470a7`
- Measurement date: 2026-08-14
- Canonical source: `skills/proposal/`
- Normalization: UTF-8 text with CRLF and CR normalized to LF
- Word convention: Unicode whitespace-separated words
- Assembly convention: count each unique procedural resource once in documented load order; copied output assets are reported separately

## Input identities

| Resource | SHA-256 | UTF-8 bytes | Words |
| --- | --- | ---: | ---: |
| `skills/proposal/SKILL.md` | `dc410cf1e844d65ef264f00ed617d4bb8d45794b1b8b77b811022b6ba3137f86` | 14796 | 2122 |
| `skills/proposal/assets/proposal-skeleton.md` | `44be895777ea0dfef6231291eb097fda2d90064dfb6e03714989dad6824be0ea` | 1089 | 141 |

## Procedural assemblies

The current package has no conditional references, so every real invocation loads the same 14796-byte, 2122-word `SKILL.md`. The future profile names are used only to establish comparable baselines.

| Assembly | Loaded procedural resources | UTF-8 bytes | Words |
| --- | --- | ---: | ---: |
| `PA0-portable` | `SKILL.md` | 14796 | 2122 |
| `PA0G-portable-gated` | `SKILL.md` | 14796 | 2122 |
| `PA1-governed` | `SKILL.md` | 14796 | 2122 |
| `PA1G-governed-gated` | `SKILL.md` | 14796 | 2122 |

## Structural and package totals

| Measurement | UTF-8 bytes | Words |
| --- | ---: | ---: |
| Representative copied skeleton | 1089 | 141 |
| Total canonical package | 15885 | 2263 |

The baseline does not claim that conditional procedure has already been removed. It records the actual common-path cost before relocation so final measurements can distinguish loaded-context reduction from total-package growth.
