# Token Cost: Plan Asset Split

## Baseline

- Measurement date: 2026-05-19
- Baseline command: `wc -c skills/plan/SKILL.md`
- Baseline `skills/plan/SKILL.md` bytes: 15447
- Baseline token command: `python scripts/measure-skill-tokens.py --skills-root skills`
- Baseline `skills/plan/SKILL.md` estimated tokens: 3862
- Baseline total measured skill bytes: 250028
- Baseline total measured skill estimated tokens: 62495

## After-change

- Measurement date: 2026-05-19
- After-change command: `python scripts/measure-skill-tokens.py --skills-root skills`
- After-change `skills/plan/SKILL.md` bytes: 13124
- After-change `skills/plan/SKILL.md` estimated tokens: 3281
- Common-path token delta: -581 tokens
- Common-path token reduction: 15.04 percent
- Common-path gate: pass; at least 15 percent reduction required
- After-change asset bytes: 3478
- After-change estimated asset tokens: 870
- After-change estimated `SKILL.md` plus assets tokens: 4151
- Total packaged-content delta from baseline body: +289 estimated tokens
- Total packaged-content change: +7.48 percent
- Total packaged-content budget: within +10 percent hard cap; above +5 percent rationale tolerance because the full plan layout now ships as on-demand packaged assets instead of common-path body.
- After-change total measured skill bytes: 247705
- After-change total measured skill estimated tokens: 61914

## Notes

- `plan-skeleton.md` owns the full plan section order, so total packaged content grows while common-path `SKILL.md` shrinks.
- M3 records adapter packaging proof, behavior-parity evidence, historical coverage, and final token-budget closeout.
