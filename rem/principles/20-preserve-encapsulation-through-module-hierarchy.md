# Principle 20: Preserve encapsulation through Module hierarchy

Parent Modules are real architectural responsibility boundaries. Child Modules refine their parent responsibility; allocations target the lowest coherent accountable Module; descendant allocations roll up for comprehension without duplicating ownership; and a child-provided Interface remains internal to its containing boundary unless explicitly exposed through each parent boundary it crosses.
Assign Interface ownership to the Module accountable for the contract and assign its realizing behavior separately. A parent may own a contract realized through child responsibilities; implementation location alone does not determine its provider.
