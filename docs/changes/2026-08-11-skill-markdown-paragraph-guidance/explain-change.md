# Keep Generated Markdown Sentences Intact

## Problem

The shared generated-Markdown guidance told skills to place one sentence or natural clause on each source line. That wording allowed an agent to split one sentence across several physical lines even though the resulting source was harder to read.

## Change

The affected skills now require normal Markdown paragraphs and prohibit splitting a sentence across physical source lines merely for wrapping or clause separation. Existing wrapped prose in `test-spec-review`, `code-review`, and `workflow` was reflowed so each sentence remains intact while Markdown structure remains unchanged. The adapter portability parser's exact workflow-equivalence block was migrated atomically to the intact-sentence form. The four authoring skeletons use the same concise rule, and the two readability contracts no longer authorize clause-level sentence splitting.

## Proof

Regression coverage first failed against every affected skill and skeleton, then failed again on 161 existing suspected sentence continuations after the guidance changed. The reflowed skills now produce zero sentence-split errors or warnings. Hosted CI exposed the parser's literal dependency on the former multiline workflow block; its representative portability, archive, and release tests passed after migration, followed by all 150 adapter-distribution tests. Canonical skill validation, the complete skill-validator suite, both Markdown readability validator suites, generated-skill checking, and generated-skill build tests passed.

## Scope

This change does not impose a fixed line-length limit, rewrite historical Markdown, change structural Markdown line boundaries, or add a formatter. Lists, tables, headings, commands, code blocks, and other Markdown structures retain their own source-line rules.
