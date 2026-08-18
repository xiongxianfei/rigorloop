# Explain-change simplification measurements

Measurement uses LF-normalized UTF-8 bytes and whitespace-delimited words.

## Before and after

| Loaded assembly | Before words | After words | Word reduction | Before bytes | After bytes | Byte reduction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EC0 portable inline | 1,175 | 555 | 620 (52.8%) | 8,224 | 4,472 | 3,752 (45.6%) |
| EC1 portable durable | 1,175 | 719 | 456 (38.8%) | 8,224 | 5,526 | 2,698 (32.8%) |
| EC2 governed inline | 1,175 | 852 | 323 (27.5%) | 8,224 | 7,031 | 1,193 (14.5%) |
| EC3 governed durable | 1,175 | 1,016 | 159 (13.5%) | 8,224 | 8,085 | 139 (1.7%) |

Every real loaded assembly strictly decreases in both measures. Equality or growth fails the focused test.

## Resource and package visibility

| Canonical resource | Words | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `SKILL.md` | 555 | 4,472 | `8c66f550de676d8348537bae813f797398130814e0e4d2dc087a3c5ea1e59764` |
| governed reference | 297 | 2,559 | `a955da0a623df532b2cd14a7b8904e38905068bafb05f52792942bcbcc44171a` |
| explanation skeleton | 164 | 1,054 | `0934e3f9a1fa08303dcdfa0f1c5d1c2601ee2fbe3c95f6d37ae78ca9818ce73e` |
| Total canonical package | 1,016 | 8,085 | per-resource identities above |

The total package is visible and is also smaller than the old flat file; acceptance depends on each loaded assembly, not root-only reduction.
