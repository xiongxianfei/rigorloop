# Architecture choices couple quality outcomes

Identity: `rem:principle:tradeoffs`.

## Key takeaway

The option that improves one quality outcome may worsen another, and the ranking depends on conditions and priorities.

## Summary

Latency, availability, security, modifiability, cost and operating burden are not independent scores supplied by a technology label. Architecture evaluation makes the relevant scenario and mechanism explicit so competing effects and uncertainties can be compared.

## Statement and example
Separating a responsibility into another process can support independent deployment while introducing communication and partial-failure questions. Consolidation can simplify a handoff while creating shared-resource or release coupling. Neither option is intrinsically superior without the intended load, change patterns and operating constraints.

## Source basis and REM synthesis

The official [ATAM report abstract](../references/kazman-2000-atam-method-for-architecture-evaluation.md#located-contributions) explains architectural tradeoffs affecting qualities including performance, availability, security and modifiability. The process example and conditional comparison questions here are REM-authored reasoning. This guidance is not a full ATAM execution or a universal numeric optimization rule.

## Use
Form a scenario with a stimulus, context and observable response before claiming “faster,” “more reliable” or “easier to change.” Identify non-negotiable constraints separately from preferences. Record missing evidence and the assumptions that control the ranking. A small comparison can be enough when the alternatives are clear.

## Limits
A weighted total can conceal unacceptable failures or pretend uncertain estimates are measured facts. Some decisions are mandated; others should remain reversible pending evidence. The exact score scheme and approval authority are project decisions, selected project choices within the current REM rules.

## Counter-signal
If an option’s advantage disappears under another plausible assumption, describe the recommendation as conditional. Do not hide the alternative merely because a preferred option has already been implemented.

## Deeper knowledge
[Architecture realization](../models/architecture-realization.md); [Realization Design](../methods/realization-design.md)
