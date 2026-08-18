# Explain-change profile size baseline

Measurement uses LF-normalized UTF-8 bytes and whitespace-delimited words. The flat canonical input is `skills/explain-change/SKILL.md` at commit `fb8bdcdc`.

| Surface | Words | UTF-8 bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Flat canonical skill; baseline for EC0, EC1, EC2, and EC3 | 1,175 | 8,224 | `8a26dde3b27ec13717cf385948a50b78a37d89c72536d260077416b9caccf95b` |

M3 must report EC0 through EC3 separately. Every loaded assembly must be strictly below both flat-baseline values; equality is failure. The governed reference, skeleton, and total canonical package remain visible measurements even though total package growth is not itself an acceptance failure.
