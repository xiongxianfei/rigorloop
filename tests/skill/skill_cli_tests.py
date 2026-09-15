"""Real Skill validator command observations, mixed into the supported suite.

The mixin preserves existing TestCase.method selectors without registering a
second copy of the cases. Target traps observe PATH dispatch, not every possible
absolute executable path or external agent behavior.
"""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validate-skills.py"


def run_validator(target):
    return subprocess.run([sys.executable, str(VALIDATOR), str(target)],
                          cwd=ROOT, text=True, capture_output=True, check=False)


class SkillCliChecks:
    def test_gate_a_accepts_structurally_valid_ambiguous_prose(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            skill = Path(temporary) / "ambiguous" / "SKILL.md"
            skill.parent.mkdir()
            skill.write_text(
                """---
name: ambiguous
description: >
  Do the thing when it seems appropriate.
---

# Ambiguous

Use the inputs somehow and produce a useful result.

## Expected output

- Something useful.
""",
                encoding="utf-8",
            )
            result = run_validator(skill.parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Gate A (canonical skill integrity)", result.stdout)

    def test_gate_a_command_has_no_target_runtime_dependency(self) -> None:
        # Real entrypoint, first with no target tools, then with traps that also
        # detect attempted invocations whose failure the validator might swallow.
        for tools_present in (False, True):
            with self.subTest(traps=tools_present), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                tools = root / "bin"
                tools.mkdir()
                marker = root / "target-invoked"
                if tools_present:
                    for target in ("codex", "claude", "opencode"):
                        trap = tools / target
                        trap.write_text('#!/bin/sh\nprintf "%s\\n" "$0" >> "$RIGORLOOP_TARGET_TRAP"\nexit 97\n', encoding="utf-8")
                        trap.chmod(0o755)
                env = {**os.environ, "PATH": str(tools), "HOME": str(root),
                       "RIGORLOOP_TARGET_TRAP": str(marker), "PYTHONDONTWRITEBYTECODE": "1"}
                result = subprocess.run(
                    [sys.executable, str(VALIDATOR), str(ROOT / "skills/proposal"),
                     str(ROOT / "skills/proposal-review")],
                    cwd=root, env=env, text=True, capture_output=True, check=False, timeout=30)
                self.assertFalse(marker.exists(), "structural validation invoked a target runtime")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertEqual(result.stdout.count("validated 1 skill files"), 2)

    def test_gate_a_missing_target_fails_without_traceback(self) -> None:
        missing = ROOT / "tests" / "fixtures" / "skills" / "does-not-exist"
        result = run_validator(missing)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Gate A (canonical skill integrity)", result.stderr)
        self.assertIn(f"{missing}: target does not exist", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_gate_a_accepts_multiple_explicit_targets(self) -> None:
        targets = [ROOT / "skills" / "pr" / "SKILL.md", ROOT / "skills" / "verify" / "SKILL.md"]
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), *(str(target) for target in targets)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for target in targets:
            self.assertIn(str(target), result.stdout)
