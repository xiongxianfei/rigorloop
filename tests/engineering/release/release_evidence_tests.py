"""Current release checklist proof, independent of retired lifecycle engines."""

import shutil

import tempfile

import unittest

from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.release.release_evidence import validate_release_evidence_checklist



def write_release_evidence(root: Path, text: str, filename: str = "v1.2.3.md") -> Path:
    target = root / "docs" / "releases" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target

def routine_release_evidence(*, package_preview: str = "pass", extra_notes: str = "") -> str:
    return f"""# Release v1.2.3

## Result

- Package: @rigorloop/rigorloop
- Version: 1.2.3
- Release type: patch
- Routine publish: yes
- No new decision introduced: yes
- Source commit: abc1234
- Source branch: main
- npm dist-tag: latest
- Publish path: trusted-publishing
- Provenance: automatic
- Status: published

## Related Lifecycle Evidence

- Related change record: not-applicable
- Upstream lifecycle approval: not-applicable
- Release-specific evidence: not-applicable
- Release notes: not-required; maintenance-only release

## Version Decision

- Change summary: maintenance release.
- Version decision: patch
- Dist-tag decision: latest
- No-op check: pass
- Existing npm version check: not-found

## Routine Publish Boundary

| Check | Result | Evidence |
| --- | --- | --- |
| release type recorded | pass | patch |
| no new product or implementation decision | pass | no new decision introduced |
| no release-process change | pass | release process unchanged |
| no package name/scope change | pass | package unchanged |
| no adapter target/install-root change | pass | adapters unchanged |
| upstream breaking change approval | not-applicable | not breaking |

## Preflight Gate

| Check | Result | Evidence |
| --- | --- | --- |
| clean worktree except intentional release artifacts | pass | git status --short |
| release notes or not-required rationale | not-required | maintenance-only release |
| generated output current | pass | skills.drift and adapters.drift |
| tests / selected CI / broad smoke | pass | selected CI passed |
| package build or pack proof | pass | npm pack |
| package preview | {package_preview} | npm pack --dry-run |
| local packed-install smoke | pass | temp project install |
| no unresolved release blockers | pass | none |
| publish path selected | pass | trusted-publishing |
| evidence path prepared | pass | docs/releases/v1.2.3.md |

## Package Contents

- Package filename: rigorloop-1.2.3.tgz
- Package size: 42 kB
- Integrity or checksum: sha512-demo
- Included-file review: package contents reviewed
- Unexpected inclusions: none
- Unexpected exclusions: none
- Secret-bearing file check: pass

## Publish Event

- Command family: trusted publishing workflow
- Registry: npm
- Package reference: @rigorloop/rigorloop@1.2.3
- Published at: 2026-05-23T12:00:00Z
- Dist-tag: latest
- Provenance status: automatic
- Manual fallback reason: not-applicable

## Registry Verification

| Check | Result | Evidence |
| --- | --- | --- |
| registry version query | pass | npm view returned 1.2.3 |
| dist-tag points correctly | pass | latest points to 1.2.3 |
| integrity metadata available | pass | sha512-demo |
| fresh registry install smoke | pass | registry install smoke passed |
| CLI or npx smoke | pass | CLI smoke passed |

## Emergency Deferrals

Use `none` for routine releases with no emergency deferrals.

| Deferred gate item | Approving owner or owning stage | Rationale | Reason pre-publish completion was impossible | Validation impact | Risk accepted | Follow-up location | Deadline or next lifecycle stage | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| none | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | completed |

## Recovery / Rollback Notes

- Failure phase: none
- Registry state checked before retry: not-applicable
- Recovery action: none
- Published version overwrite attempted: no
- Notes: none

## Follow-up

- Release announcement: none
- Deferred gate follow-up: none
- Deprecation or dist-tag follow-up: none
- Next release follow-up: none

## Evidence Safety Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| no npm tokens | pass | reviewed |
| no OTPs | pass | reviewed |
| no credentials or private keys | pass | reviewed |
| no private environment dumps | pass | reviewed |
| no hostnames or usernames | pass | reviewed |
| no home-directory or machine-local temp paths | pass | reviewed |
| command output summarized instead of pasted wholesale | pass | reviewed |

{extra_notes}
"""

def emergency_release_evidence(
    *,
    deferred_item: str = "fresh registry install smoke",
    owner: str = "release owner",
    validation_impact: str = "registry install smoke pending",
) -> str:
    return routine_release_evidence().replace(
        "- Release type: patch\n"
        "- Routine publish: yes\n"
        "- No new decision introduced: yes\n"
        "- Source commit: abc1234\n"
        "- Source branch: main\n"
        "- npm dist-tag: latest\n"
        "- Publish path: trusted-publishing\n"
        "- Provenance: automatic\n"
        "- Status: published",
        "- Release type: emergency\n"
        "- Routine publish: no\n"
        "- No new decision introduced: yes\n"
        "- Source commit: abc1234\n"
        "- Source branch: main\n"
        "- npm dist-tag: latest\n"
        "- Publish path: manual-2fa\n"
        "- Provenance: not-used with reason\n"
        "- Status: emergency-with-deferred-gate",
    ).replace(
        "| fresh registry install smoke | pass | registry install smoke passed |",
        "| fresh registry install smoke | deferred | deferred with owner approval |",
    ).replace(
        "| none | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | completed |",
        f"| {deferred_item} | {owner} | urgent fix | dependency unavailable before publish | {validation_impact} | owner accepts temporary risk | docs/changes/2026-05-23-release-process-contract/follow-up.md | next lifecycle stage | open |",
    )

def pending_release_evidence() -> str:
    text = routine_release_evidence().replace(
        "- Status: published",
        "- Status: pending-publication",
    )
    for row_name in (
        "registry version query",
        "dist-tag points correctly",
        "integrity metadata available",
        "fresh registry install smoke",
        "CLI or npx smoke",
    ):
        original = next(line for line in text.splitlines() if line.startswith(f"| {row_name} |"))
        text = text.replace(original, f"| {row_name} | not-applicable | publication not started |")
    return text

class ReleaseEvidenceTests(unittest.TestCase):

    def addCleanupTree(self, root):

        self.addCleanup(shutil.rmtree, root)



    def test_release_evidence_fixture_passes_lightweight_checklist(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix='release-evidence-checklist-'))
        self.addCleanupTree(fixture_root)
        write_release_evidence(fixture_root, routine_release_evidence())
        result = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), (fixture_root / 'docs/releases/v1.2.3.md').read_text())
        self.assertFalse(result, msg=f'expected complete release evidence to pass, got blockers: {result}')

    def test_release_evidence_blocks_missing_routine_gate_item(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix='release-evidence-checklist-'))
        self.addCleanupTree(fixture_root)
        write_release_evidence(fixture_root, routine_release_evidence(package_preview='fail'))
        result = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), (fixture_root / 'docs/releases/v1.2.3.md').read_text())
        messages = '\n'.join((f for f in result))
        self.assertIn("routine release gate item 'package preview' must pass before publish", messages)

    def test_release_evidence_allows_complete_emergency_deferral(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix='release-evidence-checklist-'))
        self.addCleanupTree(fixture_root)
        write_release_evidence(fixture_root, emergency_release_evidence())
        result = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), (fixture_root / 'docs/releases/v1.2.3.md').read_text())
        self.assertFalse(result, msg=f'expected complete emergency deferral to pass, got blockers: {result}')

    def test_release_evidence_all_states_reject_missing_duplicate_and_unknown_value_rows(self) -> None:
        preflight_rows = ('clean worktree except intentional release artifacts', 'release notes or not-required rationale', 'generated output current', 'tests / selected CI / broad smoke', 'package build or pack proof', 'package preview', 'local packed-install smoke', 'no unresolved release blockers', 'publish path selected', 'evidence path prepared')
        registry_rows = ('registry version query', 'dist-tag points correctly', 'integrity metadata available', 'fresh registry install smoke', 'CLI or npx smoke')
        states = (('pending', pending_release_evidence(), False), ('finalized', routine_release_evidence(), True), ('emergency', emergency_release_evidence(), True))
        for state, source, require_preflight_pass in states:
            for row_name in (*preflight_rows, *registry_rows):
                original = next((line for line in source.splitlines() if line.startswith(f'| {row_name} |')))
                for mutation, replacement in (('missing', ''), ('duplicate', f'{original}\n{original}'), ('unsupported', original.replace(f'| {original.split('|')[2].strip()} |', '| banana |', 1))):
                    with self.subTest(state=state, row_name=row_name, mutation=mutation):
                        errors = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), source.replace(original, replacement), require_preflight_pass=require_preflight_pass)
                        self.assertTrue(any((row_name in error for error in errors)), errors)

    def test_release_evidence_rejects_unknown_value_status(self) -> None:
        errors = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), routine_release_evidence().replace('- Status: published', '- Status: banana'))
        self.assertTrue(any(("status 'banana'" in error for error in errors)), errors)

    def test_release_evidence_result_vocabulary_is_state_and_applicability_aware(self) -> None:
        for state, source, require_preflight_pass in (('pending', pending_release_evidence(), False), ('finalized', routine_release_evidence(), True)):
            for row_name in ('package build or pack proof', 'local packed-install smoke'):
                with self.subTest(state=state, row_name=row_name):
                    original = next((line for line in source.splitlines() if line.startswith(f'| {row_name} |')))
                    mutated = source.replace(original, original.replace('| pass |', '| not-applicable |'))
                    errors = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), mutated, require_preflight_pass=require_preflight_pass)
                    self.assertTrue(any((row_name in error for error in errors)), errors)
        finalized = routine_release_evidence()
        for row_name in ('registry version query', 'dist-tag points correctly', 'integrity metadata available', 'fresh registry install smoke', 'CLI or npx smoke'):
            with self.subTest(state='finalized', row_name=row_name, result='not-applicable'):
                original = next((line for line in finalized.splitlines() if line.startswith(f'| {row_name} |')))
                errors = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), finalized.replace(original, original.replace('| pass |', '| not-applicable |')))
                self.assertTrue(any((row_name in error for error in errors)), errors)
        emergency = emergency_release_evidence()
        for row_name in ('registry version query', 'dist-tag points correctly', 'integrity metadata available', 'CLI or npx smoke'):
            with self.subTest(state='emergency', row_name=row_name, result='deferred'):
                original = next((line for line in emergency.splitlines() if line.startswith(f'| {row_name} |')))
                errors = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), emergency.replace(original, original.replace('| pass |', '| deferred |')))
                self.assertTrue(any((row_name in error for error in errors)), errors)

    def test_release_evidence_emergency_deferral_must_match_exactly_one_result(self) -> None:
        emergency = emergency_release_evidence()
        deferral = next((line for line in emergency.splitlines() if line.startswith('| fresh registry install smoke | release owner |')))
        registry = '| fresh registry install smoke | deferred | deferred with owner approval |'
        none = '| none | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | not-applicable | completed |'
        mutations = (('missing-deferral', emergency.replace(deferral, none)), ('duplicate-deferral', emergency.replace(deferral, f'{deferral}\n{deferral}')), ('unmatched-deferral', emergency.replace(registry, '| fresh registry install smoke | pass | completed |')), ('contradictory-none', emergency.replace(deferral, f'{deferral}\n{none}')))
        for mutation, text in mutations:
            with self.subTest(mutation=mutation):
                errors = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), text)
                self.assertTrue(any(('fresh registry install smoke' in error for error in errors)), errors)

    def test_release_evidence_emergency_deferral_rejects_not_applicable_required_values(self) -> None:
        emergency = emergency_release_evidence()
        deferral = next((line for line in emergency.splitlines() if line.startswith('| fresh registry install smoke | release owner |')))
        cells = [cell.strip() for cell in deferral.strip().strip('|').split('|')]
        for index, field_name in enumerate(('approving owner', 'emergency rationale', 'reason for deferral', 'validation impact', 'risk accepted', 'follow-up location', 'deadline or next lifecycle stage', 'status'), start=1):
            with self.subTest(field_name=field_name):
                mutated_cells = list(cells)
                mutated_cells[index] = 'not-applicable'
                mutated = '| ' + ' | '.join(mutated_cells) + ' |'
                errors = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), emergency.replace(deferral, mutated))
                self.assertTrue(any((field_name in error for error in errors)), errors)

    def test_release_evidence_emergency_deferral_rejects_unknown_value_status(self) -> None:
        emergency = emergency_release_evidence()
        deferral = next((line for line in emergency.splitlines() if line.startswith('| fresh registry install smoke | release owner |')))
        mutated = deferral.removesuffix(' open |') + ' banana |'
        errors = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), emergency.replace(deferral, mutated))
        self.assertTrue(any(('status must be open' in error for error in errors)), errors)

    def test_release_evidence_blocks_emergency_deferral_without_owner(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix='release-evidence-checklist-'))
        self.addCleanupTree(fixture_root)
        write_release_evidence(fixture_root, emergency_release_evidence(owner=''))
        result = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), (fixture_root / 'docs/releases/v1.2.3.md').read_text())
        messages = '\n'.join((f for f in result))
        self.assertIn("emergency deferral 'fresh registry install smoke' is missing approving owner", messages)

    def test_release_evidence_blocks_nondeferrable_registry_verification(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix='release-evidence-checklist-'))
        self.addCleanupTree(fixture_root)
        write_release_evidence(fixture_root, emergency_release_evidence(deferred_item='post-publish registry verification'))
        result = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), (fixture_root / 'docs/releases/v1.2.3.md').read_text())
        messages = '\n'.join((f for f in result))
        self.assertIn("emergency deferral 'post-publish registry verification' is non-deferrable", messages)

    def test_release_evidence_blocks_secret_bearing_content(self) -> None:
        fixture_root = Path(tempfile.mkdtemp(prefix='release-evidence-checklist-'))
        self.addCleanupTree(fixture_root)
        write_release_evidence(fixture_root, routine_release_evidence(extra_notes='Leaked environment: NPM_TOKEN=secret-value'))
        result = validate_release_evidence_checklist(Path('docs/releases/v1.2.3.md'), (fixture_root / 'docs/releases/v1.2.3.md').read_text())
        messages = '\n'.join((f for f in result))
        self.assertIn('release evidence contains forbidden secret or private machine-state marker', messages)

    def test_pending_gate_requires_exact_verified_candidate_context(self):
        import os
        from unittest.mock import patch
        from lib.release.release_evidence import validate_paths
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            env = {'RIGORLOOP_CI_WORKSPACE': str(root.resolve()), 'RIGORLOOP_CI_CANDIDATE': '/fixture/candidate'}
            candidate = {'tag': 'v1.2.3', 'prepared_commit': 'a' * 40}
            for gate, blocked in [('pending', False), ('fail', True), ('unknown_value', True)]:
                write_release_evidence(root, routine_release_evidence(package_preview=gate))
                with self.subTest(gate=gate), patch.dict(os.environ, env), patch('lib.release.release_candidate.ci_subject', return_value=candidate):
                    self.assertEqual(bool(validate_paths(root, ['docs/releases/v1.2.3.md'])), blocked)
            write_release_evidence(root, routine_release_evidence(package_preview='pending'))
            for scoped_env, tag in [({}, 'v1.2.3'), (dict(env, RIGORLOOP_CI_WORKSPACE='/other'), 'v1.2.3'), (env, 'v9.9.9')]:
                with patch.dict(os.environ, {'RIGORLOOP_CI_WORKSPACE': '', 'RIGORLOOP_CI_CANDIDATE': '', **scoped_env}), patch('lib.release.release_candidate.ci_subject', return_value=dict(candidate, tag=tag)):
                    self.assertTrue(validate_paths(root, ['docs/releases/v1.2.3.md']))

    def test_prepared_context_rejects_wrong_revision_and_invalid_proof(self):
        import os
        from unittest.mock import patch
        from lib.release.release_evidence import validate_paths
        from lib.release.release_candidate import CandidateError
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            env = {'RIGORLOOP_CI_WORKSPACE': str(root.resolve()), 'RIGORLOOP_CI_CANDIDATE': '/fixture/candidate'}
            cases = [{'return_value': {'tag': 'v1.2.3', 'prepared_commit': 'b' * 40}}, {'side_effect': CandidateError('changed receipt')}, {'side_effect': FileNotFoundError('/private/missing')}]
            for case in cases:
                with patch.dict(os.environ, env), patch('lib.release.release_candidate.ci_subject', **case):
                    with self.assertRaisesRegex(ValueError, '^invalid or mismatched prepared CI release context$'):
                        validate_paths(root, ['docs/releases/v1.2.3.md'], revision='a' * 40)

    def test_explicit_paths_reject_unknown_missing_escape_symlink_and_wrong_version(self):
        from lib.release.release_evidence import validate_paths
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertTrue(validate_paths(root, []))
            for path in ('../private.md', 'docs/releases/no-tag.md', 'docs/releases/v1.2.3.md'):
                self.assertTrue(validate_paths(root, [path]))
            target = write_release_evidence(root, routine_release_evidence())
            before = target.read_bytes()
            self.assertFalse(validate_paths(root, ['docs/releases/v1.2.3.md']))
            alias = target.with_name('v2.0.0.md')
            alias.symlink_to(target)
            self.assertTrue(validate_paths(root, ['docs/releases/v2.0.0.md']))
            alias.unlink()
            alias.write_bytes(before)
            self.assertIn('release evidence path version must match Result version', validate_paths(root, ['docs/releases/v2.0.0.md']))
            self.assertEqual(target.read_bytes(), before)
