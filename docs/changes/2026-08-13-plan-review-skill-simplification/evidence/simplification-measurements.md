# Plan-Review Simplification Measurements

Measurement date: 2026-08-13
Normalization: canonical authored files, LF line endings, each unique procedural resource once, Unicode whitespace-separated words, and UTF-8 bytes. Assets are reported separately from procedural profiles.

| Resource or profile | Before words | After words | Word change | Before bytes | After bytes | Byte change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `SKILL.md` / `PRV0-portable` | 1877 | 1401 | -476 (-25.4%) | 13619 | 10644 | -2975 (-21.8%) |
| `PRV0B-portable-boundary` | 2734 | 2258 | -476 (-17.4%) | 19965 | 16990 | -2975 (-14.9%) |
| `PRV1-governed` | 1877 | 1729 | -148 (-7.9%) | 13619 | 13404 | -215 (-1.6%) |
| `PRV1B-governed-boundary` | 2734 | 2586 | -148 (-5.4%) | 19965 | 19750 | -215 (-1.1%) |
| Total package | 2734 | 2880 | +146 (+5.3%) | 19965 | 21923 | +1958 (+9.8%) |

| Added or retained resource | Words | Bytes |
| --- | ---: | ---: |
| Boundary reference | 857 | 6346 |
| Governed reference | 328 | 2760 |
| Result asset | 239 | 1728 |
| Finding asset | 55 | 445 |

Both required primary profiles decrease. Package growth is explicit: the new structural assets and independently packaged governed procedure cost 146 words and 1,958 bytes beyond the former flat package. That growth buys one structural owner per result/finding and conditional loading of transaction procedure; it is not represented as deletion.

The rule ledger identifies two duplicate clusters removed from loaded ownership: repeated transaction/handoff explanation and inline output labels. Inline templates decrease from two to zero; mapped resources increase from one to four. No tokenizer estimate or permanent size gate was added.
