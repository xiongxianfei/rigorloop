---
name: bugfix
description: >
  Fix a bug with a structured, test-first workflow: understand expected behavior, reproduce, diagnose root cause, add a regression test, implement the minimal fix, verify blast radius, update durable docs, and explain the change.
argument-hint: [bug description, failing behavior, error message, issue number, or regression]
---

# Structured bug fix workflow

You are fixing a defect, not just making a symptom disappear.

Use this skill when the task starts from unexpected behavior, a failing test, an incident, a regression, or a bug report.

## Inputs to read

Read, if present:

- bug report, issue, logs, screenshots, or failing test output;
- relevant spec and test spec;
- concrete plan if the bug belongs to active work;
- architecture docs or project map for affected flow;
- `AGENTS.md` and `CONSTITUTION.md`;
- related code and neighboring tests;
- recent changes that could have introduced the regression.

## Process

### 1. Understand expected behavior

State expected vs actual behavior.

If the expected behavior is not specified, identify the contract gap and decide whether to update or create a spec before fixing.

### 2. Reproduce

Find the smallest reliable reproduction:

- command;
- input;
- environment;
- data state;
- observed output or error.

If reproduction is not possible, collect evidence and explain uncertainty.

### 3. Diagnose root cause

Trace the path and classify the cause:

- spec gap;
- implementation error;
- integration mismatch;
- edge case;
- regression;
- data/migration issue;
- race/timing issue;
- configuration or environment issue;
- test bug.

Assess blast radius and look for the same pattern nearby.

### 4. Add regression test first

Before changing production code, add or update a test that fails because of the bug when feasible.

If not feasible, explain why and provide another verification method.

### 5. Fix minimally

Fix the root cause with the smallest change that fully addresses it.

Do not refactor unrelated code during the bug fix.

### 6. Verify

Run:

- the regression test;
- the smallest surrounding test suite;
- any integration or smoke checks needed by the blast radius.

### 7. Update durable docs

Update the narrowest durable artifact:

- spec or test spec for contract gaps;
- architecture doc or ADR for design gaps;
- plan for active milestone sequencing issues;
- `AGENTS.md` or constitution for repeated project-wide mistakes;
- `docs/workflows.md` for workflow or handoff changes.

## Rules

- Always prefer a failing regression test before the fix.
- Fix the root cause, not the symptom.
- Keep the diff scoped.
- Do not hide uncertainty.
- Do not claim the bug is fixed until the reproduction path is verified.

## Evidence collection efficiency

Use summary and stable-ID first reasoning before broad reads or raw excerpts. Prefer check IDs, requirement IDs, test IDs, file paths, counts, and line citations when inspecting large files, repeated scans, generated output, or validation output. Read exact ranges after locating relevant lines, then expand only when the narrower evidence is insufficient.

## When full-file read is required

Read the full file when the whole file is the review target, the relevant section cannot be isolated safely, surrounding context can change the conclusion, bounded searches disagree or produce incomplete evidence, or a behavior-changing edit depends on the whole source-of-truth artifact.

## Expected output

- reproduction summary;
- expected vs actual behavior;
- root-cause classification;
- regression test added or reason it was not feasible;
- minimal fix summary;
- blast-radius verification;
- durable docs updated;
- readiness statement for `explain-change`, `code-review`, or `pr`.
