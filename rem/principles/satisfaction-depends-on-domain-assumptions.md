# Satisfaction depends on domain assumptions

Identity: `rem:principle:assumptions`.

## Key takeaway

A design can meet its specified behavior while failing the intended outcome when a necessary environmental assumption fails.

## Summary

An obligation on a controllable system rarely describes everything needed in the real environment. People, other systems, information quality and physical conditions contribute. Making those assumptions explicit exposes what the implementation alone cannot guarantee.

## Statement and mechanism
If the argument from system behavior to an intended result depends on an environmental condition, the conclusion is conditional on that condition. An apparently complete design description cannot supply a missing environmental guarantee merely by restating the goal.

## Example
A release reader that returns the correct identifier does not ensure users select the intended review if they cannot distinguish identically named releases. The implementation may pass its identifier check while the intended-use task remains unreliable. The environment includes the user task and presentation, not just software internals.

## Source basis and REM synthesis

[Zave and Jackson](../sources/S12.md) explain how specifications and domain knowledge jointly support requirements satisfaction, including assumptions that may fail. [NASA requirements definition](../sources/S01.md) calls for documenting and validating assumptions. The release example and review question here are REM-authored applications.

## Scope and limits
This reasoning is relevant to software-intensive systems and to broader system/environment boundaries. It does not determine which party should own a missing condition. A project may change the boundary, add a monitoring/recovery obligation, or limit the claim with authorization.

## Challenge
A condition treated as “given” should be challenged when operating evidence contradicts it. An implication written in a model is not an empirical demonstration that the assumptions hold.

## Applications
[Requirement model](../models/requirements.md) preserves assumptions; [Requirement Analysis](../methods/requirement-analysis.md) exposes them; [Intended-use validation](../methods/validate-stakeholder-outcomes.md) checks their relevance in intended use.
