# Explain-change simplification measurements

Measurement uses LF-normalized UTF-8 bytes and whitespace-delimited words.

## Before and after

| Loaded assembly | Before words | After words | Word reduction | Before bytes | After bytes | Byte reduction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EC0 portable inline | 1,175 | 552 | 623 (53.0%) | 8,224 | 4,478 | 3,746 (45.6%) |
| EC1 portable durable | 1,175 | 716 | 459 (39.1%) | 8,224 | 5,532 | 2,692 (32.7%) |
| EC2 governed inline | 1,175 | 871 | 304 (25.9%) | 8,224 | 7,164 | 1,060 (12.9%) |
| EC3 governed durable | 1,175 | 1,035 | 140 (11.9%) | 8,224 | 8,218 | 6 (0.1%) |

Every real loaded assembly strictly decreases in both measures. Equality or growth fails the focused test.

## Resource and package visibility

| Canonical resource | Words | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `SKILL.md` | 552 | 4,478 | `5f9584b4360306762d6b7482c1112761b51b481cc32bb55982998482dffed83c` |
| governed reference | 319 | 2,686 | `23795b8d96bfab40c9f7281bed59ce058a751343bc7ea2f445f92055225c023f` |
| explanation skeleton | 164 | 1,054 | `0934e3f9a1fa08303dcdfa0f1c5d1c2601ee2fbe3c95f6d37ae78ca9818ce73e` |
| Total canonical package | 1,035 | 8,218 | per-resource identities above |

The total package is visible and is also smaller than the old flat file; acceptance depends on each loaded assembly, not root-only reduction.
