# Project Vision

## Pitch

AI coding agents produce output quickly, but the reasoning behind that output
often disappears. When the chat ends, teams can lose why a change was made,
what was considered, what was tested, and how to resume the work safely.

RigorLoop exists to make AI-assisted software work traceable, resumable, and
reviewable in Git.

It turns agent work into durable artifacts: proposal, spec, execution plan,
test plan, implementation evidence, review findings, verification, and PR
handoff. The goal is not just faster output. The goal is AI work that humans
can inspect, trust, continue, and improve.

## What makes this different

Most AI coding tools optimize for faster output. RigorLoop optimizes for
trustworthy change delivery after the output exists. It treats agent work as a
reviewable software engineering artifact rather than a chat transcript:
decisions are written down, tests trace to the contract, design intent is
visible, validation evidence is captured, and review concerns stay attached to
the change.

The differentiator is the traceability chain. A meaningful change can be traced
from idea to proposal, spec, plan, test spec, implementation, review, verification,
and PR handoff. Months later, a reviewer should be able to see why the change
was made, what proved it correct, and where to resume if work stopped.

## Principles

### Reviewable artifacts

Important decisions become repository artifacts, not lost chat logs. Proposals,
specs, test plans, reviews, validation evidence, and handoff state are versioned,
diffable, and reviewable.

### Human-understandable AI work

RigorLoop keeps reasoning and evidence visible. A human reviewer should be able
to understand what changed, why it changed, what evidence supports it, and what
still needs judgment.

### Resumable across sessions and agents

Work should not depend on one chat session or one model. The repository carries
the task state so another agent or human can continue from the artifacts.

### Traceable from idea to PR

A feature should have a visible chain from proposal to spec, plan, test spec,
implementation, review, verification, and PR. The chain makes later review,
maintenance, and resumption possible.

### Durable lessons

When a workflow fails, RigorLoop captures the lesson and turns it into improved
guidance, checks, or artifacts. The system becomes more reliable because
mistakes are recorded and acted on rather than remembered only by one agent.

## Who it is for

RigorLoop is for individual contributors, maintainers, and teams that want AI
agents to participate in serious software delivery without weakening engineering
discipline. It fits projects that value explicit requirements, test-driven work,
architectural consistency, reproducible validation, and human approval of scope,
tradeoffs, and release decisions.

## Who it is not for

RigorLoop is not for teams that want a zero-process scratchpad, unconstrained
autonomous coding, one-shot prompting, or artifact-free development. It is also
not for teams that treat specs, tests, architecture, and plans as ceremony
instead of evidence for better decisions.

## What it commits to

RigorLoop commits to making AI-assisted changes easier to inspect, resume,
validate, and review. A meaningful change exposes its governing source, test
obligations, design constraints, implementation rationale, validation commands,
reviewer concerns, and handoff state in durable project artifacts rather than
agent memory.

## What it refuses to be

RigorLoop is not a hosted agent runtime, autonomous merge system, generic
project-management suite, vendor-specific control plane, or replacement for
engineers, reviewers, CI, ownership, and release judgment. It refuses to reward
code volume without evidence; faster generation matters only when the result
remains understandable, testable, and consistent with system design.

## What would prove this wrong

The vision is wrong if reviewers cannot reconstruct a representative change's
purpose, requirements, design constraints, tests, validation evidence, and
review concerns from tracked artifacts without chat history. It is also wrong if
teams routinely ignore the artifacts because they slow delivery without
improving review quality, if the public story becomes more attractive but less
accurate, or if RigorLoop requires a platform migration before it becomes
useful.
