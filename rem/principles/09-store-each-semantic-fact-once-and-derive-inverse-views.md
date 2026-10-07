# Principle 9: Store each semantic fact once and derive inverse views

## Relationship and why

Independently maintained copies of the same engineering fact can diverge when changes occur. Deriving multiple views from one authoritative fact allows different presentations to stay consistent with that source. The derivation still needs checking: a single source cannot by itself prevent an incorrect projection.

## REM commitment

Multiple views should not require independently maintained copies of the same relationship.

## Application

The [representation model](../models/README.md#representation) owns authoritative relationships and inverse views; [view presentation](../methods/view-presentation.md) distinguishes source meaning from projection and rendering.
