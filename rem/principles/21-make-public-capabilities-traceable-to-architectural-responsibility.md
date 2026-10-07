# Principle 21: Make public capabilities traceable to architectural responsibility

## Relationship and why

The name or existence of a public entry tells a reader how a capability is presented, but does not by itself establish the behavior behind it or who is accountable for that behavior. Explicit correspondence lets readers follow the entry to its governing responsibilities and distinguish supported mappings from assumptions. Shared catalogs can then aid discovery without becoming alternative ownership models.

## REM commitment

A reader should be able to trace a public entry's name and purpose to its logical behavior, accountable responsibilities, and realization. Record the mapping once and derive navigable views. A public command, procedure, or other entry does not automatically require its own Feature, Module, or Interface. Distinguish observed entry existence from proposed behavioral correspondence, preserve incomplete mappings, and never infer ownership or satisfaction from catalog placement.

## Application

[Public-entry discoverability](../models/architecture-realization.md#public-entry-discoverability) owns the correspondence; [Logical view navigation](../methods/views/logical.md#public-entry-navigation) presents it.
