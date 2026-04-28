---
name: research
description: >
  Validate assumptions before proposal, spec, architecture, or implementation. Use when the workflow depends on uncertain technical behavior, domain facts, user expectations, dependencies, platform limits, standards, laws, pricing, performance, or operational constraints.
---

# Assumption research

You are reducing uncertainty before the workflow commits to a solution.

Research must be scoped, sourced, and tied to decisions. It is not an excuse to browse endlessly.

## When to use

Use when:

- exploration identifies unknowns;
- a library, API, standard, policy, or platform may have changed;
- compatibility or migration risk is unclear;
- performance or scale claims need evidence;
- user/domain assumptions are not grounded;
- security, privacy, legal, or compliance constraints may apply;
- architecture choices depend on external constraints.

## Inputs to read

Read local project sources first when the answer may already be in the repo:

- existing docs and specs;
- dependency manifests and lockfiles;
- API clients, schemas, generated code;
- CI and deployment config;
- previous ADRs and decisions.

Then use reliable external sources when current or niche facts matter.

## Research plan

Before researching, write:

1. the decision the research will inform;
2. the exact questions to answer;
3. acceptable source types;
4. what evidence would change the recommendation;
5. when to stop.

## Source quality

Prefer, in order:

1. official documentation or standards;
2. source code or release notes from the upstream project;
3. authoritative vendor docs;
4. peer-reviewed or primary technical sources;
5. reputable engineering writeups;
6. community discussions only as supporting evidence.

For current facts, verify freshness.

## Output path

Prefer:

```text
docs/research/YYYY-MM-DD-slug.md
```

For small questions, include a compact research section in the proposal or architecture doc.

## Required output sections

1. **Decision to support**
2. **Questions answered**
3. **Summary conclusion**
4. **Evidence table** with source, finding, confidence, and relevance
5. **Implications for proposal/spec/architecture/tests**
6. **Remaining uncertainty**
7. **Recommendation**

## Rules

- Do not present unsourced claims as facts.
- Do not over-research questions that do not affect the decision.
- Do not mix speculation with evidence.
- Do not cite stale docs for volatile facts without checking dates.
- Do not use research to bypass a missing spec.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- research artifact path or concise report;
- sourced answers to the stated questions;
- decision implications;
- confidence level;
- recommended next skill, usually `proposal`, `spec`, or `architecture`.
