# Readable record output

Owning change record: [2026-09-10-readable-record-output](../changes/2026-09-10-readable-record-output/change.json)

## Challenge

Primary text commands serialize report bodies back into JSON, leaving paragraphs and code blocks displayed as escaped strings. New stored records are compact single-line JSON, making their fields difficult to inspect in an editor or diff. The user requested readable terminal output and explicitly selected indented JSON files without Markdown report exports.

## Goals

- Display selected report text with actual line breaks, preserving intentional escape sequences and complete scope information.
- Make new stored JSON records readable and retain their indentation through targeted edits.
- Keep machine JSON, canonical identities, exact-byte preservation, validation and recovery trustworthy.

## Scope and non-goals

The scope is the primary text renderer, new-record encoding, local value replacement and array insertion, their regression proof, and owning CLI documentation. Existing historical files and unrelated neighboring bytes retain their identities. No bulk reformatting, stored schema migration, Markdown report exports, new commands, new dependencies, publication or release is requested.

## Governing principle

Improve presentation while preserving recorded meaning and the integrity of evidence.

## Proposed direction

Use readable labeled text with multiline narrative for people and indented JSON for newly stored records. Keep compact JSON for machine responses and canonical calculations. Targeted edits preserve existing content outside their exact scope, including compact historical formatting; indentation counts toward existing size limits.

## Feasibility

The shared renderer already receives decoded records, and the package already depends on a structured text formatter. The writer isolates creation, value replacement and array append from persistence, so presentation changes can remain outside identity, validation and recovery mechanisms. Existing public-command, preservation and recovery tests provide direct validation boundaries. Earlier local implementation is a candidate only: independent contract, delivery and code assessments must evaluate it before final verification, without implying those gates preceded the edits.

## Decision requested

Approve this bounded readability direction for contract and delivery assessment under the user's explicit choice of indented JSON. Token overhead varies by tokenizer; no fixed token-saving or overhead guarantee is part of the scope.
