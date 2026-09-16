"""Learn guidance.

Current Skill contracts own the protected structures, resources and authority.
Wording checks detect structural drift; independent review assesses semantics.
Existing class/case selectors remain stable, including historical names.
"""
from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))


class LearnSkillSimplificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = ROOT / "skills" / "learn"
        self.skill = (self.root / "SKILL.md").read_text(encoding="utf-8")
        self.method = (self.root / "references" / "session-method.md").read_text(encoding="utf-8")
        self.package = self.skill + "\n" + self.method

    def test_package_profiles_and_resource_trigger_are_exact(self) -> None:
        self.assertEqual(sorted(path.name for path in (self.root / "references").iterdir()), ["session-method.md"])
        self.assertFalse((self.root / "assets").exists())
        self.assertIn("LR0-route-result", self.skill)
        self.assertIn("LR1-session", self.skill)
        self.assertIn("READ `references/session-method.md`", self.skill)
        self.assertIn("exactly for `run-learn-session`", self.skill)
        self.assertIn("at most once", self.skill)

    def test_operations_authority_and_resource_failures_are_closed(self) -> None:
        for value in ("run-learn-session", "record-learn-route-result"):
            self.assertIn(value, self.skill)
        self.assertNotIn("assess-learn-trigger` operation", self.skill)
        for phrase in ("unknown, missing, combined, or ambiguous", "contributor confirmation", "destination mutation", "workflow continuation", "missing, unreadable, escaped, stale, contradictory, or mixed-version", "must not reconstruct"):
            self.assertIn(phrase.lower(), self.skill.lower())
        for phrase in ("unless the request explicitly identifies", "before session creation"):
            self.assertIn(phrase.lower(), self.skill.lower())
        self.assertNotIn("$learn", self.skill)

    def test_session_paths_interruption_and_confirmation_fail_closed(self) -> None:
        for phrase in ("lowest available suffix", "recheck absence", "complete `Frame`", "must not resume, repair, adopt, or overwrite", "same complete session", "new unique path", "pending", "confirmed", "rejected"):
            self.assertIn(phrase.lower(), self.package.lower())
        for phrase in ("session identity", "evidence-basis identity", "recorded evidence", "bounded inference", "unknowns", "sensitive or excluded evidence", "conflicting or ambiguous topic content"):
            self.assertIn(phrase.lower(), self.method.lower())

    def test_routes_and_result_recording_have_narrow_ownership(self) -> None:
        for value in ("ROUTE-NNN", "pending-owner-action", "complete", "blocked", "authoritative-artifact", "durable-scheduled-follow-up"):
            self.assertIn(value, self.package)
        for phrase in ("only the matching route", "exact owner-result identity", "idempotent success", "must not poll", "must not mutate the destination", "historical sessions"):
            self.assertIn(phrase.lower(), self.package.lower())
        for field in ("source observation", "confirmed classification", "requested action", "destination kind", "owning skill or process", "evidence-basis identity", "required completion kind", "settlement", "optional owner-result identity", "optional blocker"):
            self.assertIn(field.lower(), self.method.lower())
        for phrase in ("fixed when the route is created", "must match the route's immutable required completion kind"):
            self.assertIn(phrase.lower(), self.package.lower())

    def test_compact_result_and_claim_limits_are_complete(self) -> None:
        for phrase in ("operation", "session identity and path", "trigger and scope", "confirmation result", "session recording result", "topic effects", "route IDs and settlements", "owner-result identities", "blockers", "next owner or handoff", "claim limitations"):
            self.assertIn(phrase.lower(), self.skill.lower())
        for claim in ("destination approval", "implementation", "release", "workflow completion", "verification", "branch readiness", "PR readiness"):
            self.assertIn(claim.lower(), self.skill.lower())
