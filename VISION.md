# Project Vision

## Pitch

RigorLoop is a Git-first starter kit for AI-assisted software delivery. It keeps the reasoning, tests, and verification behind each AI-assisted change visible enough for human review.

## What makes this different

Most AI coding tools optimize for faster output. RigorLoop trades some speed for reviewability when code arrives faster than reviewers can validate it, agent state disappears into chat, and "tests pass" claims lack a spec-level walkthrough. It keeps project decisions in durable artifacts that reviewers can inspect, diff, and improve while staying close to ordinary Git, CI, and human review.

## Who it is for

RigorLoop is for projects that value explicit requirements, small diffs, traceable rationale, and reproducible validation. It fits individual contributors, maintainers, and small teams using AI during software delivery who need a disciplined path from idea to reviewed change.

## Who it is not for

It is not for teams looking for a zero-process scratchpad, an autonomous coding platform, or lightweight prompting with no durable artifact trail. It is also not a fit for projects that treat artifacts as ceremony rather than as evidence for decisions.

## What it commits to

RigorLoop commits to concrete evidence over process theater. Generated output has a separate authored source. Change rationale survives chat-history loss. Verification claims point to recorded proof, not memory. Source-of-truth rules stay explicit enough that a reviewer can tell which artifact governs a disputed change.

## What it refuses to be

RigorLoop refuses to chase every workflow preference, become a hosted control plane or vendor-specific agent runtime, expand into a broad project-management suite, or replace pull requests, CI, ownership, and review. It protects a narrow promise: make AI-assisted changes easier to inspect, reason about, and maintain in Git.

## What would prove this wrong

The vision is wrong if a reviewer cannot reconstruct a representative change's purpose, governing source, and validation evidence from tracked files without chat history. It is also wrong if maintainers routinely ignore the artifacts because they slow review without clarifying decisions, or if ordinary Git-based projects need a platform migration before RigorLoop becomes useful.
