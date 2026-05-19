---
name: transformable-frontmatter
version: "1.0.0"
schema-version: skill-readability-v1
description: This skill has Codex frontmatter that can be removed for other adapters.
argument-hint: [feature name]
---

# Transformable Frontmatter

## Workflow role

- role_name: transformable-frontmatter
- stage: execution
- upstream: fixture
- downstream: fixture
- summary: Fixture for front matter transformation.

Use generic instructions after adapter-specific frontmatter is removed.

## Output skeleton

```md
Value: <transformed generated skill>
```

## Expected output

- A transformed generated skill.
