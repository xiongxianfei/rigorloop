#!/usr/bin/env python3
"""Validation selector domain model and path classification."""

from __future__ import annotations

from record_store_classification import is_archival_record_store
from model_layout import PROJECT_MODEL_PATHS

import json
import hashlib
import fnmatch
import re
import shlex
import subprocess
from dataclasses import dataclass, field, replace
from pathlib import Path, PurePosixPath
from typing import Any


DEFAULT_ADAPTER_VERSION = "0.1.1"
STATUSES = frozenset({"ok", "blocked", "fallback", "error"})
EXIT_CODES = {"ok": 0, "blocked": 2, "fallback": 3, "error": 4}
ROOT_VISION_PATH = "VISION.md"


@dataclass(frozen=True)
class ExecutionConstraints:
    unit: str = "command"
    mode: str = "serial"
    demand: int = 1
    isolation: str = ""
    basis: str = ""
    shared_writes: bool = False


def command_basis(template: str, unit: str) -> str:
    normalized = shlex.join(shlex.split(template))
    return hashlib.sha256((normalized + "\n" + unit + "\nexecutor-adapter-v1").encode()).hexdigest()


@dataclass(frozen=True)
class CheckCatalogEntry:
    id: str
    command_template: str
    category: str
    parallel_safe: bool = False
    dependencies: tuple[str, ...] = ()
    constraints: ExecutionConstraints | None = None
    label: str = ""
    modes: tuple[str, ...] = ()


CHECK_CATALOG: dict[str, CheckCatalogEntry] = {
    "record_store.schema": CheckCatalogEntry(
        "record_store.schema", "node scripts/build-record-store-schema.mjs --check", "explicit-recording", parallel_safe=True,
    ),
    "model.validate": CheckCatalogEntry(
        "model.validate",
        "python scripts/validate-boundary-first.py --check --path docs/design/skill/workflow.md --path docs/design/cli/cli.md --path docs/design/cli/records.md",
        "explicit-recording", parallel_safe=True,
    ),
    "record_retirement.regression": CheckCatalogEntry(
        "record_retirement.regression",
        "node --test packages/rigorloop/test/record-retirement.test.js",
        "record-retirement", parallel_safe=True,
    ),
    "boundary_first.validate": CheckCatalogEntry(
        "boundary_first.validate",
        "python scripts/validate-boundary-first.py --check",
        "boundary-first",
    ),
    "boundary_first.reference_regression": CheckCatalogEntry(
        "boundary_first.reference_regression",
        "python scripts/test-boundary-first-reference.py",
        "boundary-first",
    ),
    "boundary_first.regression": CheckCatalogEntry(
        "boundary_first.regression",
        "python scripts/test-boundary-first-validation.py",
        "boundary-first",
    ),
    "skills.validate": CheckCatalogEntry(
        "skills.validate",
        "python scripts/validate-skills.py",
        "skills",
    ),
    "skills.regression": CheckCatalogEntry(
        "skills.regression",
        "python scripts/test-skill-validator.py",
        "skills",
        parallel_safe=True,
    ),
    "adapters.regression": CheckCatalogEntry(
        "adapters.regression",
        "python scripts/test-adapter-distribution.py AdapterDistributionTests.test_adapter_generation_creates_independent_packages_and_thin_entrypoints AdapterDistributionTests.test_adapter_generation_drift_check_detects_stale_and_unexpected_files AdapterDistributionTests.test_validate_adapters_cli_rejects_retired_repository_output AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root AdapterDistributionTests.test_v0_1_2_release_validation_checks_archives_and_artifact_metadata AdapterDistributionTests.test_distribution_archives_have_independent_complete_resource_inventory AdapterDistributionTests.test_distribution_generation_rejects_source_and_active_output_roots AdapterDistributionTests.test_distribution_generation_preserves_runtime_under_output_parent_and_symlinks AdapterDistributionTests.test_distribution_generated_skill_structure_is_validated_independently AdapterDistributionTests.test_validate_adapter_output_rejects_stale_mapped_resource_hashes AdapterDistributionTests.test_validate_adapter_output_rejects_missing_mapped_resource AdapterDistributionTests.test_validate_adapter_output_rejects_missing_or_malformed_canonical_skills",
        "adapters",
        parallel_safe=True,
    ),
    "adapters.drift": CheckCatalogEntry(
        "adapters.drift",
        "python scripts/test-adapter-distribution.py AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives",
        "adapters",
    ),
    "adapters.validate": CheckCatalogEntry(
        "adapters.validate",
        "python scripts/test-adapter-distribution.py AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root",
        "adapters",
    ),
    "review_artifacts.regression": CheckCatalogEntry(
        "review_artifacts.regression",
        "python scripts/test-review-artifact-validator.py",
        "review-artifacts",
        parallel_safe=True,
    ),
    "review_artifacts.validate": CheckCatalogEntry(
        "review_artifacts.validate",
        "python scripts/validate-review-artifacts.py <change-root>...",
        "review-artifacts",
    ),
    "artifact_lifecycle.regression": CheckCatalogEntry(
        "artifact_lifecycle.regression",
        "python scripts/test-artifact-lifecycle-validator.py",
        "lifecycle",
        parallel_safe=True,
    ),
    "artifact_lifecycle.validate": CheckCatalogEntry(
        "artifact_lifecycle.validate",
        "python scripts/validate-artifact-lifecycle.py --mode explicit-paths --path <path>...",
        "lifecycle",
    ),
    "change_metadata.regression": CheckCatalogEntry(
        "change_metadata.regression",
        "python scripts/test-change-metadata-validator.py",
        "change-metadata",
        parallel_safe=True,
    ),
    "change_metadata.validate": CheckCatalogEntry(
        "change_metadata.validate",
        "python scripts/validate-change-metadata.py <change-yaml>...",
        "change-metadata",
    ),
    "change_record_query.regression": CheckCatalogEntry(
        "change_record_query.regression",
        "python scripts/test-query-change-record.py",
        "change-record-query",
        parallel_safe=True,
    ),
    "workflow_automation.code_state_regression": CheckCatalogEntry(
        "workflow_automation.code_state_regression",
        "python scripts/test-workflow-code-state.py",
        "workflow-automation",
    ),
    "workflow_automation.engine_regression": CheckCatalogEntry(
        "workflow_automation.engine_regression",
        "python scripts/test-workflow-automation.py",
        "workflow-automation",
    ),
    "workflow_automation.policy_regression": CheckCatalogEntry(
        "workflow_automation.policy_regression",
        "python scripts/test-workflow-automation-policy.py",
        "workflow-automation",
    ),
    "workflow_automation.state_regression": CheckCatalogEntry(
        "workflow_automation.state_regression",
        "python scripts/test-workflow-automation-state.py",
        "workflow-automation",
    ),
    "workflow_automation.validator_regression": CheckCatalogEntry(
        "workflow_automation.validator_regression",
        "python scripts/test-validate-workflow-automation.py",
        "workflow-automation",
    ),
    "release.validate": CheckCatalogEntry(
        "release.validate",
        "python scripts/validate-release.py --recorded-source-auto --version <version>",
        "release",
    ),
    "release_transaction.regression": CheckCatalogEntry(
        "release_transaction.regression",
        "python scripts/test-release-transaction.py",
        "release-transaction",
        parallel_safe=True,
    ),
    "readme.validate": CheckCatalogEntry(
        "readme.validate",
        "python scripts/validate-readme.py README.md",
        "readme",
    ),
    "readme.vision_markers": CheckCatalogEntry(
        "readme.vision_markers",
        "python scripts/validate-readme.py README.md --vision-markers",
        "readme",
    ),
    "markdown_readability.validate": CheckCatalogEntry(
        "markdown_readability.validate",
        "python scripts/validate-markdown-readability.py <path>... [--changed-section PATH:START:END ...]",
        "markdown-readability",
    ),
    "markdown_readability.regression": CheckCatalogEntry(
        "markdown_readability.regression",
        "python scripts/test-markdown-readability-validator.py",
        "markdown-readability",
        parallel_safe=True,
    ),
    "guide_system.regression": CheckCatalogEntry(
        "guide_system.regression",
        "python scripts/test-guide-system-validator.py",
        "guide-system",
        parallel_safe=True,
    ),
    "guide_system.validate": CheckCatalogEntry(
        "guide_system.validate",
        "python scripts/validate-guide-system.py",
        "guide-system",
    ),
    "documentation_prose.enforce": CheckCatalogEntry(
        "documentation_prose.enforce",
        "python scripts/validate-documentation-prose.py --mode enforce --path <path>...",
        "documentation-prose",
    ),
    "documentation_prose.audit": CheckCatalogEntry(
        "documentation_prose.audit",
        "python scripts/validate-documentation-prose.py --mode audit --path <path>...",
        "documentation-prose",
    ),
    "documentation_prose.regression": CheckCatalogEntry(
        "documentation_prose.regression",
        "python scripts/test-documentation-prose-validator.py",
        "documentation-prose",
        parallel_safe=True,
    ),
    "selector.regression": CheckCatalogEntry(
        "selector.regression",
        "python scripts/test-select-validation.py",
        "selector",
        parallel_safe=True,
    ),
    "requirement_fidelity.spec_reads": CheckCatalogEntry(
        "requirement_fidelity.spec_reads",
        "python scripts/test-fidelity-gate-spec-reads.py --review-set tests/fixtures/requirement-fidelity-gate/representative-reviews --max-bytes-per-clause 4096 --assert-no-broad-reads",
        "requirement-fidelity",
        parallel_safe=True,
    ),
    "token_cost.regression": CheckCatalogEntry(
        "token_cost.regression",
        "python scripts/test-token-cost-measurement.py",
        "token-cost",
        parallel_safe=True,
    ),
    "token_cost.report_regression": CheckCatalogEntry(
        "token_cost.report_regression",
        "python scripts/test-token-cost-report-validation.py",
        "token-cost",
        parallel_safe=True,
    ),
    "token_cost.report_validate": CheckCatalogEntry(
        "token_cost.report_validate",
        "python scripts/validate-token-cost-report.py <report-yaml>...",
        "token-cost",
    ),
    "broad_smoke.repo": CheckCatalogEntry(
        "broad_smoke.repo",
        "bash scripts/ci.sh --mode broad-smoke --skip-diff-scoped",
        "broad-smoke",
    ),
    "rigorloop_cli.test": CheckCatalogEntry(
        "rigorloop_cli.test",
        "npm test --prefix packages/rigorloop",
        "rigorloop-cli",
    ),
    "governed_lifecycle_cli_wrapper.test": CheckCatalogEntry(
        "governed_lifecycle_cli_wrapper.test",
        "python scripts/test-governed-lifecycle-cli-validator.py",
        "governed-lifecycle-cli-wrapper",
        parallel_safe=True,
    ),
    "npm_package_publication.test": CheckCatalogEntry(
        "npm_package_publication.test",
        "python scripts/test-npm-package-publication.py",
        "rigorloop-cli",
    ),
}

# These two complete command scopes use per-test temporary trees, read immutable
# source fixtures, restore process-local environment, have no external services,
# and invoke children sequentially. Other old allowlist entries remain serial
# until a current isolation assessment covers their nested resource demand.
# Literal bases deliberately do not update when a template or adapter changes.
_COMMAND_ASSESSMENTS = {
    'skills.regression': ('9c4ffbab147aa1e13f1edd27bbcd224b21254b9c73c37d76bbfd9c94ce27a6e7', 'Skill validator fixtures use owned temporary trees; subprocess validators run sequentially; no shared writes or services.'),
    'adapters.regression': ('4ac8b3234ec905ec97dc1603d847b04af163c206509fad625765c4e3ecb6fe72', 'Selected adapter cases build and validate owned temporary outputs; read canonical resources; sequential subprocesses, no active-root writes or services.'),
}
for _id, _entry in tuple(CHECK_CATALOG.items()):
    _assessment = _COMMAND_ASSESSMENTS.get(_id)
    CHECK_CATALOG[_id] = replace(_entry, parallel_safe=_assessment is not None,
        constraints=ExecutionConstraints(mode="bounded", isolation=_assessment[1], basis=_assessment[0])
        if _assessment else None)
CHECK_CATALOG["validation_execution.regression"] = CheckCatalogEntry(
    "validation_execution.regression", "python scripts/test-validation-execution.py", "selector")


# Current direct-mode membership is authored here, alongside selected checks.
# The old Bash inventory and historical classification are no longer readers.
CHECK_CATALOG['broad_smoke.skills.validate'] = CheckCatalogEntry(
    'broad_smoke.skills.validate', 'python scripts/validate-skills.py', 'broad-smoke',
    parallel_safe=True, dependencies=(), constraints=ExecutionConstraints(mode="bounded", isolation='Canonical skill validation reads source/resources without writes, external services or nested workers.', basis='a8c706629176acda626a4dff2c77ba5805f21058a767fa755c8567315234555f'),
    label='Validate canonical skills', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.skills.regression'] = CheckCatalogEntry(
    'broad_smoke.skills.regression', 'python scripts/test-skill-validator.py', 'broad-smoke',
    parallel_safe=True, dependencies=(), constraints=ExecutionConstraints(mode="bounded", isolation='Skill validator fixtures use owned temporary trees, process-local environment, sequential children and no external service.', basis='9c4ffbab147aa1e13f1edd27bbcd224b21254b9c73c37d76bbfd9c94ce27a6e7'),
    label='Run skill validator fixtures', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.adapters.regression'] = CheckCatalogEntry(
    'broad_smoke.adapters.regression', 'python scripts/test-adapter-distribution.py', 'broad-smoke',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Run adapter distribution fixtures', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.adapters.build_archives'] = CheckCatalogEntry(
    'broad_smoke.adapters.build_archives', "python scripts/build-adapters.py --version v0.1.3 --output-dir '<adapter-output>'", 'broad-smoke',
    parallel_safe=True, dependencies=(), constraints=ExecutionConstraints(mode="bounded", isolation='Reads canonical sources and writes or validates only the invocation-owned package output; build-success dependency protects the shared artifact; no services or nested worker pool.', basis='d62367012cc0d1a44d1ca1d9491870d4c010df7224a2383cfa9f1d361f09f1fa'),
    label='Build generated adapter archives', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.adapters.validate_archives'] = CheckCatalogEntry(
    'broad_smoke.adapters.validate_archives', "python scripts/validate-adapters.py --root '<adapter-output>' --version v0.1.3", 'broad-smoke',
    parallel_safe=True, dependencies=('broad_smoke.adapters.build_archives',), constraints=ExecutionConstraints(mode="bounded", isolation='Reads canonical sources and writes or validates only the invocation-owned package output; build-success dependency protects the shared artifact; no services or nested worker pool.', basis='20ea1accdb465c0f8761bfd7c5dd4418345563bd5a1d5e930181299ed23f3ca9'),
    label='Validate generated adapter archives', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.change_metadata.regression'] = CheckCatalogEntry(
    'broad_smoke.change_metadata.regression', 'python scripts/test-change-metadata-validator.py', 'broad-smoke',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Run change metadata validator fixtures', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.artifact_lifecycle.regression'] = CheckCatalogEntry(
    'broad_smoke.artifact_lifecycle.regression', 'python scripts/test-artifact-lifecycle-validator.py', 'broad-smoke',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Run artifact lifecycle validator fixtures', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.review_artifacts.regression'] = CheckCatalogEntry(
    'broad_smoke.review_artifacts.regression', 'python scripts/test-review-artifact-validator.py', 'broad-smoke',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Run review artifact validator fixtures', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.review_artifacts.changed_roots'] = CheckCatalogEntry(
    'broad_smoke.review_artifacts.changed_roots', "python scripts/validate-change-metadata.py '<roots>'", 'broad-smoke',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Validate current change records (changed roots)', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.artifact_lifecycle.scoped'] = CheckCatalogEntry(
    'broad_smoke.artifact_lifecycle.scoped', "python scripts/validate-artifact-lifecycle.py '<lifecycle-args>'", 'broad-smoke',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Validate artifact lifecycle (scoped)', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.selector.regression'] = CheckCatalogEntry(
    'broad_smoke.selector.regression', 'python scripts/test-select-validation.py', 'broad-smoke',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Run selector and wrapper fixtures', modes=('broad-smoke',))
CHECK_CATALOG['broad_smoke.validation_execution.regression'] = CheckCatalogEntry(
    'broad_smoke.validation_execution.regression', 'python scripts/test-validation-execution.py', 'broad-smoke',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Run validation executor fixtures', modes=('broad-smoke',))
CHECK_CATALOG['main.skills.validate'] = CheckCatalogEntry(
    'main.skills.validate', 'python scripts/validate-skills.py', 'main',
    parallel_safe=True, dependencies=(), constraints=ExecutionConstraints(mode="bounded", isolation='Canonical skill validation reads source/resources without writes, external services or nested workers.', basis='a8c706629176acda626a4dff2c77ba5805f21058a767fa755c8567315234555f'),
    label='Gate A: canonical skill integrity', modes=('main',))
CHECK_CATALOG['main.skills.regression'] = CheckCatalogEntry(
    'main.skills.regression', 'python scripts/test-skill-validator.py', 'main',
    parallel_safe=True, dependencies=(), constraints=ExecutionConstraints(mode="bounded", isolation='Skill validator fixtures use owned temporary trees, process-local environment, sequential children and no external service.', basis='9c4ffbab147aa1e13f1edd27bbcd224b21254b9c73c37d76bbfd9c94ce27a6e7'),
    label='Gate A: canonical skill regressions', modes=('main',))
CHECK_CATALOG['main.boundary_first.validate'] = CheckCatalogEntry(
    'main.boundary_first.validate', 'python scripts/validate-boundary-first.py --check', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Gate A: boundary proof structure', modes=('main',))
CHECK_CATALOG['main.adapters.regression'] = CheckCatalogEntry(
    'main.adapters.regression', 'python scripts/test-adapter-distribution.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Gate B: adapter parity regressions', modes=('main',))
CHECK_CATALOG['main.adapters.build_archives'] = CheckCatalogEntry(
    'main.adapters.build_archives', "python scripts/build-adapters.py --version v0.1.5 --output-dir '<adapter-output>'", 'main',
    parallel_safe=True, dependencies=(), constraints=ExecutionConstraints(mode="bounded", isolation='Reads canonical sources and writes or validates only the invocation-owned package output; build-success dependency protects the shared artifact; no services or nested worker pool.', basis='8fb2d9cf5eeda804bb972a03447bd547e1e9bd6e3ebc97d1dba68ecf971293f1'),
    label='Gate B: build all adapter archives', modes=('main',))
CHECK_CATALOG['main.adapters.validate_archives'] = CheckCatalogEntry(
    'main.adapters.validate_archives', "python scripts/validate-adapters.py --version v0.1.5 --adapter-root '<adapter-output>'", 'main',
    parallel_safe=True, dependencies=('main.adapters.build_archives',), constraints=ExecutionConstraints(mode="bounded", isolation='Reads canonical sources and writes or validates only the invocation-owned package output; build-success dependency protects the shared artifact; no services or nested worker pool.', basis='8de166b66cc49f8aed72d966ae70c1d9b8871f52ce2bf90f88f512f4218dadf7'),
    label='Gate B: validate all adapter archives', modes=('main',))
CHECK_CATALOG['main.release_transaction.regression'] = CheckCatalogEntry(
    'main.release_transaction.regression', 'python scripts/test-release-transaction.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Gate C: release integrity regressions', modes=('main',))
CHECK_CATALOG['main.rigorloop_cli.test'] = CheckCatalogEntry(
    'main.rigorloop_cli.test', 'npm test --prefix packages/rigorloop', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Public package regressions', modes=('main',))
CHECK_CATALOG['main.governed_lifecycle_cli_wrapper.test'] = CheckCatalogEntry(
    'main.governed_lifecycle_cli_wrapper.test', 'python scripts/test-governed-lifecycle-cli-validator.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: lifecycle validation wrapper regressions', modes=('main',))
CHECK_CATALOG['main.governed_lifecycle_cli.validate'] = CheckCatalogEntry(
    'main.governed_lifecycle_cli.validate', 'python scripts/validate-governed-lifecycle-cli.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: public lifecycle validation', modes=('main',))
CHECK_CATALOG['main.change_metadata.regression'] = CheckCatalogEntry(
    'main.change_metadata.regression', 'python scripts/test-change-metadata-validator.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: change metadata regressions', modes=('main',))
CHECK_CATALOG['main.artifact_lifecycle.regression'] = CheckCatalogEntry(
    'main.artifact_lifecycle.regression', 'python scripts/test-artifact-lifecycle-validator.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: lifecycle regressions', modes=('main',))
CHECK_CATALOG['main.review_artifacts.regression'] = CheckCatalogEntry(
    'main.review_artifacts.regression', 'python scripts/test-review-artifact-validator.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: review evidence regressions', modes=('main',))
CHECK_CATALOG['main.retirement_ledger.regression'] = CheckCatalogEntry(
    'main.retirement_ledger.regression', 'python scripts/test-retirement-ledger.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: retirement ledger', modes=('main',))
CHECK_CATALOG['main.change_record_query.regression'] = CheckCatalogEntry(
    'main.change_record_query.regression', 'python scripts/test-query-change-record.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: change-record query', modes=('main',))
CHECK_CATALOG['main.workflow_automation.engine_regression'] = CheckCatalogEntry(
    'main.workflow_automation.engine_regression', 'python scripts/test-workflow-automation.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: workflow engine', modes=('main',))
CHECK_CATALOG['main.workflow_automation.code_state_regression'] = CheckCatalogEntry(
    'main.workflow_automation.code_state_regression', 'python scripts/test-workflow-code-state.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: workflow code state', modes=('main',))
CHECK_CATALOG['main.workflow_automation.policy_regression'] = CheckCatalogEntry(
    'main.workflow_automation.policy_regression', 'python scripts/test-workflow-automation-policy.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: workflow policy', modes=('main',))
CHECK_CATALOG['main.workflow_automation.state_regression'] = CheckCatalogEntry(
    'main.workflow_automation.state_regression', 'python scripts/test-workflow-automation-state.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: workflow state', modes=('main',))
CHECK_CATALOG['main.workflow_automation.validator_regression'] = CheckCatalogEntry(
    'main.workflow_automation.validator_regression', 'python scripts/test-validate-workflow-automation.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: workflow metadata', modes=('main',))
CHECK_CATALOG['main.requirement_fidelity.spec_reads'] = CheckCatalogEntry(
    'main.requirement_fidelity.spec_reads', 'python scripts/test-fidelity-gate-spec-reads.py --review-set tests/fixtures/requirement-fidelity-gate/representative-reviews --max-bytes-per-clause 4096 --assert-no-broad-reads', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: review fidelity', modes=('main',))
CHECK_CATALOG['main.readme.validate'] = CheckCatalogEntry(
    'main.readme.validate', 'python scripts/validate-readme.py README.md', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Contributor surface: README structure', modes=('main',))
CHECK_CATALOG['main.readme.vision_markers'] = CheckCatalogEntry(
    'main.readme.vision_markers', 'python scripts/validate-readme.py README.md --vision-markers', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Contributor surface: vision markers', modes=('main',))
CHECK_CATALOG['main.markdown_readability.regression'] = CheckCatalogEntry(
    'main.markdown_readability.regression', 'python scripts/test-markdown-readability-validator.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Contributor surface: markdown structure regressions', modes=('main',))
CHECK_CATALOG['main.guide_system.regression'] = CheckCatalogEntry(
    'main.guide_system.regression', 'python scripts/test-guide-system-validator.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Contributor surface: guide regressions', modes=('main',))
CHECK_CATALOG['main.guide_system.validate'] = CheckCatalogEntry(
    'main.guide_system.validate', 'python scripts/validate-guide-system.py', 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Contributor surface: guide structure', modes=('main',))
CHECK_CATALOG['main.artifact_lifecycle.scoped'] = CheckCatalogEntry(
    'main.artifact_lifecycle.scoped', "python scripts/validate-artifact-lifecycle.py --mode push-main-ci --before '<base>' --after '<head>'", 'main',
    parallel_safe=False, dependencies=(), constraints=None,
    label='Governance: main lifecycle scope', modes=('main',))

for _mode_prefix in ('broad_smoke','main'):
    _key = _mode_prefix + '.adapters.build_archives'
    CHECK_CATALOG[_key] = replace(CHECK_CATALOG[_key],dependencies=(_mode_prefix+'.skills.validate',))

# Audited initial case population: normal loaders, fresh process per case, owned
# temporary Git/record fixtures, process-local environment and sequential child
# validation. Selector wrapper probes obey their allocated nested worker budget.
_CASE_ASSESSMENTS = {
    'artifact_lifecycle.regression': '0d3bf319c63835687a034b94f2003918fddbb599b456a8894d98fa5784f262bf',
    'change_metadata.regression': 'ff7f4d79be49f9635e51521fbf36df43f6276a04e55863c56163746e49726586',
    'selector.regression': 'ce40ab4944eed966a2dba006e9d2545614eef23e6e6767e9f9ed2bee294158f2',
    'broad_smoke.change_metadata.regression': 'ff7f4d79be49f9635e51521fbf36df43f6276a04e55863c56163746e49726586',
    'broad_smoke.artifact_lifecycle.regression': '0d3bf319c63835687a034b94f2003918fddbb599b456a8894d98fa5784f262bf',
    'broad_smoke.selector.regression': 'ce40ab4944eed966a2dba006e9d2545614eef23e6e6767e9f9ed2bee294158f2',
    'main.change_metadata.regression': 'ff7f4d79be49f9635e51521fbf36df43f6276a04e55863c56163746e49726586',
    'main.artifact_lifecycle.regression': '0d3bf319c63835687a034b94f2003918fddbb599b456a8894d98fa5784f262bf',
}
for _key, _basis in _CASE_ASSESSMENTS.items():
    CHECK_CATALOG[_key] = replace(CHECK_CATALOG[_key], parallel_safe=True,
        constraints=ExecutionConstraints(unit='python-unittest', mode='bounded',
            isolation='Fresh normal-loader case process; owned temporary fixtures; immutable source inputs; nested workers consume the case allocation.',
            basis=_basis))

MODE_CHECK_IDS = {
    mode: tuple(key for key, entry in CHECK_CATALOG.items() if mode in entry.modes)
    for mode in ("broad-smoke", "main")
}


def validate_catalog(catalog=None) -> None:
    catalog = CHECK_CATALOG if catalog is None else catalog
    for key, entry in catalog.items():
        if not isinstance(entry, CheckCatalogEntry) or key != entry.id:
            raise ValueError(f"invalid catalog identity: {key}")
        if not isinstance(entry.command_template, str) or not entry.command_template.strip():
            raise ValueError(f"missing command: {key}")
        if type(entry.parallel_safe) is not bool:
            raise ValueError(f"invalid parallel safety: {key}")
        if not isinstance(entry.dependencies, tuple) or any(not isinstance(x,str) for x in entry.dependencies) or len(set(entry.dependencies)) != len(entry.dependencies):
            raise ValueError(f"invalid dependencies: {key}")
        if any(x not in catalog for x in entry.dependencies):
            raise ValueError(f"missing catalog dependency: {key}")
        if not isinstance(entry.modes,tuple) or any(mode not in {"broad-smoke","main"} for mode in entry.modes):
            raise ValueError(f"unknown catalog mode membership: {key}")
        c = entry.constraints
        if c is None:
            if entry.parallel_safe:
                raise ValueError(f"unassessed parallel safety: {key}")
            continue
        if not isinstance(c, ExecutionConstraints):
            raise ValueError(f"unknown constraint fields: {key}")
        if c.unit not in {"command", "python-unittest", "node-test"}:
            raise ValueError(f"unknown execution unit: {key}")
        if c.unit == "python-unittest":
            argv = shlex.split(entry.command_template)
            if len(argv)<2 or not re.fullmatch(r'python(?:3(?:\.\d+)?)?',Path(argv[0]).name) or not argv[1].endswith('.py'):
                raise ValueError(f"contradictory case command: {key}")
        if c.mode not in {"serial", "exclusive", "bounded"}:
            raise ValueError(f"unknown execution mode: {key}")
        if type(c.demand) is not int or c.demand < 1 or type(c.shared_writes) is not bool:
            raise ValueError(f"invalid resource constraint: {key}")
        if not isinstance(c.isolation,str) or not c.isolation.strip():
            raise ValueError(f"missing isolation rationale: {key}")
        if c.mode == "bounded" and c.shared_writes:
            raise ValueError(f"contradictory shared writes: {key}")
        if entry.parallel_safe != (c.mode == "bounded"):
            raise ValueError(f"contradictory parallel constraint: {key}")
        if c.basis != command_basis(entry.command_template, c.unit):
            raise ValueError(f"stale command/adapter basis: {key}")
    visiting, visited = set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError(f"catalog dependency cycle: {key}")
        if key in visited:
            return
        visiting.add(key)
        for dependency in catalog[key].dependencies:
            visit(dependency)
        visiting.remove(key)
        visited.add(key)
    for key in catalog:
        visit(key)


BOUNDARY_CHECK_IDS = frozenset(
    {
        "broad_smoke.repo",
        "release.validate",
        "adapters.drift",
        "adapters.validate",
    }
)
AUTHORITATIVE_ARTIFACT_PREFIXES = (
    "docs/design/",
    "docs/proposals/",
    "docs/plans/",
    "docs/architecture/",
    "docs/adr/",
    "specs/",
    "skills/",
    "schemas/",
    "scripts/",
    "templates/",
)
AUTHORITATIVE_ARTIFACT_FILES = frozenset({"AGENTS.md", "CONSTITUTION.md", "VISION.md", "docs/plan.md"})

# Exact user-authorized isolated evidence for the recorder adoption initiative.
# These are advisory prose, not registered lifecycle reviews or settlement.
ISOLATED_RECORDING_EVIDENCE = frozenset({
    "docs/reviews/explicit-recording-and-model-centered-design.md",
    "docs/reviews/explicit-recording-and-model-centered-design-delivery.md",
    *(f"docs/implementation/explicit-recording-m{milestone}.md" for milestone in range(1, 5)),
    *(f"docs/reviews/explicit-recording-m{milestone}-code-review.md" for milestone in range(1, 5)),
})


@dataclass(frozen=True)
class RepositoryPreflightContext:
    repo_root: str
    inside_worktree: bool
    tracked_paths: frozenset[str]
    unmerged_paths: tuple[str, ...]


RELEASE_PROFILE_FILENAME_PATTERN = re.compile(
    r"^(v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))\.yaml$"
)


@dataclass(frozen=True)
class SelectionRequest:
    mode: str
    paths: tuple[str, ...] = ()
    base: str | None = None
    head: str | None = None
    release_version: str | None = None
    broad_smoke: bool = False
    trigger_context_paths: tuple[str, ...] = ()
    repo_root: Path | str = Path.cwd()
    adapter_version: str = DEFAULT_ADAPTER_VERSION
    preflight_context: RepositoryPreflightContext | None = None


@dataclass(frozen=True)
class NormalizedPath:
    ok: bool
    path: str | None = None
    blocking_code: str | None = None
    message: str | None = None


@dataclass(frozen=True)
class PathClassification:
    path: str
    category: str | None


@dataclass
class SelectedCheckDraft:
    id: str
    reasons: list[str] = field(default_factory=list)
    paths: set[str] = field(default_factory=set)
    changed_sections: set[str] = field(default_factory=set)
    affected_roots: set[str] = field(default_factory=set)
    versions: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class SelectionResult:
    mode: str
    status: str
    changed_paths: tuple[str, ...]
    classified_paths: tuple[dict[str, str], ...]
    unclassified_paths: tuple[str, ...]
    selected_checks: tuple[dict[str, Any], ...]
    affected_roots: tuple[str, ...]
    broad_smoke_required: bool
    blocking_results: tuple[dict[str, str], ...]
    preflight_results: tuple[dict[str, Any], ...]
    registration_debt: tuple[dict[str, Any], ...]
    rationale: tuple[str, ...]
    broad_smoke: dict[str, Any]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "status": self.status,
            "changed_paths": list(self.changed_paths),
            "classified_paths": list(self.classified_paths),
            "unclassified_paths": list(self.unclassified_paths),
            "selected_checks": list(self.selected_checks),
            "affected_roots": list(self.affected_roots),
            "broad_smoke_required": self.broad_smoke_required,
            "broad_smoke": self.broad_smoke,
            "blocking_results": list(self.blocking_results),
            "preflight_results": list(self.preflight_results),
            "registration_debt": list(self.registration_debt),
            "rationale": list(self.rationale),
        }


def exit_code_for_status(status: str) -> int:
    return EXIT_CODES.get(status, 4)


def selection_result_to_json(result: SelectionResult) -> str:
    return json.dumps(result.to_json_dict(), indent=2, sort_keys=False) + "\n"


def is_parallel_safe_check(check_id: str) -> bool:
    if check_id not in CHECK_CATALOG:
        raise ValueError(f"unknown check ID: {check_id}")
    return CHECK_CATALOG[check_id].parallel_safe


def error_result(mode: str, message: str, *, code: str = "invalid-invocation") -> SelectionResult:
    return _build_result(
        mode=mode or "unknown",
        changed_paths=[],
        classified_paths=[],
        unclassified_paths=[],
        selected={},
        affected_roots=set(),
        broad_smoke_sources=[],
        blocking_results=[{"code": code, "message": message}],
        preflight_results=[],
        status="error",
    )


def normalize_path(raw_path: str, *, repo_root: Path | str) -> NormalizedPath:
    root = Path(repo_root).resolve()
    raw = raw_path.strip()
    if not raw:
        return NormalizedPath(False, blocking_code="empty-path", message="path must not be empty")

    candidate = Path(raw)
    if ".." in candidate.parts:
        return NormalizedPath(
            False,
            blocking_code="path-traversal",
            message="path traversal is not allowed",
        )

    resolved = candidate.resolve(strict=False) if candidate.is_absolute() else (root / candidate).resolve(strict=False)
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return NormalizedPath(
            False,
            blocking_code="outside-repository-path",
            message="path is outside the repository",
        )

    return NormalizedPath(True, path=PurePosixPath(relative.as_posix()).as_posix())


def classify_path(path: str) -> PathClassification:
    category = _path_category(path)
    return PathClassification(path=path, category=category)


def catalog_command(
    check_id: str,
    *,
    repo_root: Path = Path.cwd(),
    paths: tuple[str, ...] = (),
    changed_sections: tuple[str, ...] = (),
    affected_roots: tuple[str, ...] = (),
    versions: tuple[str, ...] = (),
    adapter_version: str = DEFAULT_ADAPTER_VERSION,
    mode: str = "explicit",
    base: str | None = None,
    head: str | None = None,
) -> str:
    if mode not in {"local", "explicit", "pr", "main", "release"}:
        raise ValueError(f"unsupported catalog mode: {mode}")
    if check_id not in CHECK_CATALOG:
        raise ValueError(f"unknown check ID: {check_id}")

    if check_id == "adapters.drift":
        return _join(
            "python",
            "scripts/test-adapter-distribution.py",
            "AdapterDistributionTests.test_build_adapter_archives_creates_required_release_archives",
        )
    if check_id == "boundary_first.validate":
        args = ["python", "scripts/validate-boundary-first.py", "--check"]
        spec_paths: set[str] = set()
        for path in paths:
            if re.fullmatch(r"specs/[^/]+\.test\.md", path):
                spec_paths.add(path)
            elif re.fullmatch(r"specs/[^/]+\.md", path) and path != "specs/README.md":
                spec_paths.add(path)
        for path in sorted(spec_paths):
            args.extend(["--path", path])
        return _join(*args)
    if check_id == "model.validate":
        args = ["python", "scripts/validate-boundary-first.py", "--check"]
        models = {"docs/design/skill/workflow.md", "docs/design/cli/cli.md",
                  "docs/design/cli/records.md"}
        for path in paths:
            # Records is a child of CLI, with its own examples. Match it before CLI.
            example_owners = {
                "docs/design/cli/examples/records/": PROJECT_MODEL_PATHS["record-format"],
                "docs/design/skill/examples/workflow/": PROJECT_MODEL_PATHS["workflow"],
                "docs/design/cli/examples/": PROJECT_MODEL_PATHS["cli"],
            }
            owner = next((owner for prefix, owner in example_owners.items() if path.startswith(prefix)), None)
            example = re.fullmatch(r"docs/design/([a-z0-9][a-z0-9-]{0,79})/examples/.+", path)
            if owner:
                models.add(owner)
            elif example:
                model = example.group(1)
                models.add(PROJECT_MODEL_PATHS.get(model, f"docs/design/{model}/{model}.md"))
            elif path.startswith("docs/design/"):
                # Aliases route deleted sources only. Existing files/symlinks must
                # be checked at their exact path, not hidden by a valid receiver.
                old = re.fullmatch(r"docs/design/(?P<model>[a-z0-9][a-z0-9-]{0,79})(?:/(?P=model))?\.md", path)
                absent = not (repo_root / path).exists() and not (repo_root / path).is_symlink()
                if old and absent:
                    model = old.group("model")
                    if model == "test":
                        models.add(PROJECT_MODEL_PATHS["validation"])
                    elif model == "distribution":
                        models.update((PROJECT_MODEL_PATHS["packaging"], PROJECT_MODEL_PATHS["installation"]))
                    else:
                        models.add(PROJECT_MODEL_PATHS.get(model, path))
                else:
                    models.add(path)
        for path in sorted(models):
            args.extend(["--path", path])
        return _join(*args)
    if check_id == "adapters.validate":
        return _join(
            "python",
            "scripts/test-adapter-distribution.py",
            "AdapterDistributionTests.test_validate_adapters_cli_accepts_release_archive_root",
        )
    if check_id == "review_artifacts.validate":
        if not affected_roots:
            raise ValueError("review_artifacts.validate requires at least one change root")
        return _join("python", "scripts/validate-review-artifacts.py", *affected_roots)
    if check_id == "artifact_lifecycle.validate":
        if mode == "pr":
            if not base or not head:
                raise ValueError("PR lifecycle validation requires base and head")
            return _join("python", "scripts/validate-artifact-lifecycle.py", "--mode", "pr-ci",
                         "--base", base, "--head", head)
        if not paths:
            raise ValueError("artifact_lifecycle.validate requires at least one path")
        args = ["python", "scripts/validate-artifact-lifecycle.py", "--mode", "explicit-paths"]
        for path in paths:
            args.extend(["--path", path])
        return _join(*args)
    if check_id == "change_metadata.validate":
        if not paths:
            raise ValueError("change_metadata.validate requires at least one change.json path")
        return _join("python", "scripts/validate-change-metadata.py", *paths)
    if check_id == "markdown_readability.validate":
        if not paths:
            raise ValueError("markdown_readability.validate requires at least one path")
        args = ["python", "scripts/validate-markdown-readability.py", *paths]
        for changed_section in changed_sections:
            args.extend(["--changed-section", changed_section])
        return _join(*args)
    if check_id == "release.validate":
        if not versions:
            raise ValueError("release.validate requires at least one release version")
        args = [
            "python",
            "scripts/validate-release.py",
            "--recorded-source-auto",
            "--version",
        ]
        args.extend(versions)
        return _join(*args)
    if check_id == "token_cost.report_validate":
        if not paths:
            raise ValueError("token_cost.report_validate requires at least one report YAML path")
        return _join("python", "scripts/validate-token-cost-report.py", *paths)
    if check_id == "documentation_prose.enforce":
        if not paths:
            raise ValueError("documentation_prose.enforce requires at least one path")
        args = ["python", "scripts/validate-documentation-prose.py", "--mode", "enforce"]
        for path in paths:
            args.extend(["--path", path])
        return _join(*args)
    if check_id == "documentation_prose.audit":
        if not paths:
            raise ValueError("documentation_prose.audit requires at least one path")
        args = ["python", "scripts/validate-documentation-prose.py", "--mode", "audit"]
        for path in paths:
            args.extend(["--path", path])
        return _join(*args)

    if CHECK_CATALOG[check_id].modes:
        raise ValueError("direct-mode leaf requires composition scope")
    return CHECK_CATALOG[check_id].command_template


def select_validation(request: SelectionRequest) -> SelectionResult:
    repo_root = Path(request.repo_root).resolve()
    invalid = _validate_request(request)
    if invalid:
        return error_result(request.mode, invalid)

    changed_paths, normalization_blocks = _resolve_changed_paths(request, repo_root=repo_root)
    changed_sections_by_path = _resolve_changed_sections(
        request,
        changed_paths=tuple(changed_paths),
        repo_root=repo_root,
    )
    selected: dict[str, SelectedCheckDraft] = {}
    classified_paths: list[dict[str, str]] = []
    unclassified_paths: list[str] = []
    affected_roots: set[str] = set()
    blocking_results: list[dict[str, str]] = []
    blocking_results.extend(normalization_blocks)
    preflight_context = request.preflight_context or _build_preflight_context(repo_root)
    preflight_results = _preflight_results(
        changed_paths,
        repo_root=repo_root,
        preflight_context=preflight_context,
    )
    blocking_results.extend(
        result for result in preflight_results if result.get("result") == "blocked"
    )
    registration_debt: list[dict[str, Any]] = []

    release_versions: set[str] = set()
    for path in changed_paths:
        classification = classify_path(path)
        if classification.category is None:
            unclassified_paths.append(path)
            blocking_results.append(
                {
                    "code": "unclassified-path",
                    "path": path,
                    "message": "changed path is not classified by the v1 selector",
                }
            )
            continue

        classified_paths.append({"path": path, "category": classification.category})
        _apply_path_selection(
            path,
            classification.category,
            changed_paths=changed_paths,
            selected=selected,
            affected_roots=affected_roots,
            blocking_results=blocking_results,
            registration_debt=registration_debt,
            release_versions=release_versions,
            repo_root=repo_root,
            changed_sections_by_path=changed_sections_by_path,
            tracked_deletion=(
                path in preflight_context.tracked_paths and not (repo_root / path).exists()
            ),
        )

    # Apply deletion provenance after every contributor (including plan context)
    # has selected inputs, so another changed path cannot reintroduce a deletion.
    lifecycle = selected.get("artifact_lifecycle.validate")
    if lifecycle:
        deleted = {
            path for path in lifecycle.paths
            if path in changed_paths and _is_lifecycle_path(path) and _proven_prose_deletion(
                path, repo_root=repo_root,
                tracked_deletion=path in preflight_context.tracked_paths,
            )
        }
        if deleted:
            lifecycle.paths.difference_update(deleted)
            if not lifecycle.paths:
                del selected["artifact_lifecycle.validate"]
            _add_check(selected, "artifact_lifecycle.regression",
                       "Proven lifecycle artifact deletion retains regression without reading absent inputs.")

    if request.mode == "pr":
        _add_check(selected, "artifact_lifecycle.validate",
                   "Every PR retains revision-bound lifecycle and baseline checks.")

    if _readme_marker_validation_required(tuple(changed_paths), repo_root=repo_root):
        _add_check(
            selected,
            "readme.vision_markers",
            "README vision markers require marker-boundary validation.",
        )

    broad_smoke_sources = _broad_smoke_sources(request, changed_paths=changed_paths, repo_root=repo_root)
    broad_smoke_required = bool(broad_smoke_sources)
    if broad_smoke_required:
        _add_check(selected, "broad_smoke.repo", "Broad smoke is required by an authoritative source.")

    if not changed_paths and not broad_smoke_required:
        blocking_results.append(
            {
                "code": "empty-changed-paths",
                "message": "no changed paths were provided or discovered",
            }
        )

    status = "blocked" if blocking_results else "ok"
    return _build_result(
        mode=request.mode,
        base=request.base,
        head=request.head,
        changed_paths=changed_paths,
        classified_paths=classified_paths,
        unclassified_paths=unclassified_paths,
        selected=selected,
        affected_roots=affected_roots,
        broad_smoke_sources=broad_smoke_sources,
        blocking_results=blocking_results,
        preflight_results=preflight_results,
        registration_debt=registration_debt,
        status=status,
        adapter_version=request.adapter_version,
        repo_root=repo_root,
    )


def _validate_request(request: SelectionRequest) -> str | None:
    if request.mode not in {"local", "explicit", "pr", "main", "release"}:
        return "unsupported or missing --mode"
    if request.mode == "explicit" and not request.paths:
        return "--mode explicit requires at least one --path"
    if request.mode in {"pr", "main"} and (not request.base or not request.head):
        return f"--mode {request.mode} requires --base and --head"
    if request.mode == "release" and not request.release_version:
        return "--mode release requires --release-version"
    return None


def _resolve_changed_paths(
    request: SelectionRequest,
    *,
    repo_root: Path,
) -> tuple[list[str], list[dict[str, str]]]:
    raw_paths: list[str]
    blocks: list[dict[str, str]] = []

    if request.mode in {"explicit", "local"} and request.paths:
        raw_paths = list(request.paths)
    elif request.mode == "local":
        raw_paths = _git_local_changed_paths(repo_root)
    elif request.mode in {"pr", "main"}:
        raw_paths = _git_range_changed_paths(repo_root, request.base or "", request.head or "")
    elif request.mode == "release":
        raw_paths = [f"docs/releases/{request.release_version}/release.yaml"]
    else:
        raw_paths = []

    normalized_paths: list[str] = []
    seen: set[str] = set()
    for raw_path in raw_paths:
        normalized = normalize_path(raw_path, repo_root=repo_root)
        if not normalized.ok:
            blocks.append(
                {
                    "code": normalized.blocking_code or "invalid-path",
                    "path": _safe_path_label(raw_path),
                    "message": normalized.message or "invalid path",
                }
            )
            continue
        assert normalized.path is not None
        if normalized.path not in seen:
            normalized_paths.append(normalized.path)
            seen.add(normalized.path)
    return normalized_paths, blocks


def _is_authoritative_artifact(path: str) -> bool:
    return path in AUTHORITATIVE_ARTIFACT_FILES or path.startswith(AUTHORITATIVE_ARTIFACT_PREFIXES)


def _run_git(
    repo_root: Path,
    args: list[str],
) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return None


def _inside_git_worktree(repo_root: Path) -> bool:
    result = _run_git(repo_root, ["rev-parse", "--is-inside-work-tree"])
    return bool(result and result.returncode == 0 and result.stdout.strip() == "true")


def _git_unmerged_paths(repo_root: Path) -> list[str]:
    result = _run_git(repo_root, ["status", "--porcelain=v1", "--untracked-files=no"])
    if not result or result.returncode != 0:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        index_status = line[0]
        worktree_status = line[1]
        if "U" in {index_status, worktree_status} or (index_status, worktree_status) in {
            ("A", "A"),
            ("D", "D"),
        }:
            paths.append(line[3:])
    return paths


def _git_tracked_paths(repo_root: Path) -> frozenset[str]:
    result = _run_git(repo_root, ["ls-files", "-z"])
    if not result or result.returncode != 0:
        return frozenset()
    return frozenset(path for path in result.stdout.split("\0") if path)


def build_repository_preflight_context(repo_root: Path | str) -> RepositoryPreflightContext:
    resolved_root = Path(repo_root).resolve()
    inside_worktree = _inside_git_worktree(resolved_root)
    return RepositoryPreflightContext(
        repo_root=resolved_root.as_posix(),
        inside_worktree=inside_worktree,
        tracked_paths=_git_tracked_paths(resolved_root) if inside_worktree else frozenset(),
        unmerged_paths=tuple(_git_unmerged_paths(resolved_root)) if inside_worktree else (),
    )


def _build_preflight_context(repo_root: Path) -> RepositoryPreflightContext:
    return build_repository_preflight_context(repo_root)


def _preflight_results(
    changed_paths: list[str],
    *,
    repo_root: Path,
    preflight_context: RepositoryPreflightContext | None = None,
) -> list[dict[str, str]]:
    if preflight_context is None and not _inside_git_worktree(repo_root):
        return []
    if preflight_context is not None and Path(preflight_context.repo_root).resolve() != repo_root:
        raise ValueError("preflight context does not match repository root")

    results: list[dict[str, str]] = []
    context = preflight_context or _build_preflight_context(repo_root)
    if not context.inside_worktree:
        return []
    unmerged = list(context.unmerged_paths)
    if unmerged:
        results.append(
            {
                "check": "unmerged_paths",
                "result": "blocked",
                "code": "unmerged-paths",
                "path": ", ".join(unmerged),
                "message": "unmerged paths make validation readiness ambiguous",
                "corrective_action": "resolve merge conflicts, then rerun validation",
            }
        )
    else:
        results.append({"check": "unmerged_paths", "result": "pass"})

    untracked_authoritative = [
        path
        for path in changed_paths
        if _is_authoritative_artifact(path)
        and (repo_root / path).exists()
        and not _authoritative_path_is_tracked(
            repo_root,
            path,
            context.tracked_paths,
        )
    ]
    if untracked_authoritative:
        path_list = ", ".join(untracked_authoritative)
        results.append(
            {
                "check": "tracked_authoritative_artifacts",
                "result": "blocked",
                "code": "untracked-authoritative-artifacts",
                "path": path_list,
                "message": "authoritative artifacts must be tracked before broad validation can prove branch readiness",
                "corrective_action": f"git add -- {path_list}",
            }
        )
    else:
        results.append({"check": "tracked_authoritative_artifacts", "result": "pass"})

    return results


def _authoritative_path_is_tracked(
    repo_root: Path,
    relative: str,
    tracked_paths: frozenset[str],
) -> bool:
    candidate = repo_root / relative
    if candidate.is_symlink():
        return False
    if candidate.is_dir():
        descendants = [
            path.relative_to(repo_root).as_posix()
            for path in candidate.rglob("*")
            if path.is_file() or path.is_symlink()
        ]
        return bool(descendants) and all(path in tracked_paths for path in descendants)
    return candidate.is_file() and relative in tracked_paths


def _git_local_changed_paths(repo_root: Path) -> list[str]:
    tracked = _git_lines(repo_root, "diff", "--name-only", "--diff-filter=ACMRT", "HEAD", "--", ".")
    staged = _git_lines(repo_root, "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "--", ".")
    untracked = _git_lines(repo_root, "ls-files", "--others", "--exclude-standard")
    return _dedupe([*tracked, *staged, *untracked])


def _git_range_changed_paths(repo_root: Path, base: str, head: str) -> list[str]:
    return _git_lines(repo_root, "diff", "--name-only", "--diff-filter=ACMRT", base, head, "--", ".")


def _resolve_changed_sections(
    request: SelectionRequest,
    *,
    changed_paths: tuple[str, ...],
    repo_root: Path,
) -> dict[str, tuple[str, ...]]:
    sections: dict[str, tuple[str, ...]] = {}
    for path in changed_paths:
        if path not in {"README.md", ROOT_VISION_PATH}:
            continue
        path_sections = _git_changed_sections_for_path(request, path, repo_root=repo_root)
        if not path_sections:
            path_sections = _whole_file_section(path, repo_root=repo_root)
        if path_sections:
            sections[path] = path_sections
    return sections


def _git_changed_sections_for_path(
    request: SelectionRequest,
    path: str,
    *,
    repo_root: Path,
) -> tuple[str, ...]:
    if request.mode in {"pr", "main"}:
        return _git_range_changed_sections(repo_root, path, request.base or "", request.head or "")
    if request.mode in {"local", "explicit"}:
        unstaged = _git_range_changed_sections(repo_root, path, "HEAD")
        staged = _git_staged_changed_sections(repo_root, path)
        return tuple(_dedupe([*unstaged, *staged]))
    return ()


def _git_range_changed_sections(repo_root: Path, path: str, *diff_args: str) -> tuple[str, ...]:
    result = subprocess.run(
        ["git", "diff", "--unified=0", "--diff-filter=ACMRT", *diff_args, "--", path],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ()
    return _diff_hunk_sections(path, result.stdout)


def _git_staged_changed_sections(repo_root: Path, path: str) -> tuple[str, ...]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--unified=0", "--diff-filter=ACMRT", "--", path],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ()
    return _diff_hunk_sections(path, result.stdout)


def _diff_hunk_sections(path: str, diff_text: str) -> tuple[str, ...]:
    sections: list[str] = []
    for line in diff_text.splitlines():
        if not line.startswith("@@"):
            continue
        match = re.search(r"\+(\d+)(?:,(\d+))?", line)
        if not match:
            continue
        start = int(match.group(1))
        length = int(match.group(2) or "1")
        if length < 1:
            continue
        sections.append(f"{path}:{start}:{start + length - 1}")
    return tuple(_dedupe(sections))


def _whole_file_section(path: str, *, repo_root: Path) -> tuple[str, ...]:
    file_path = repo_root / path
    if not file_path.is_file():
        return ()
    try:
        line_count = len(file_path.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return ()
    if line_count < 1:
        return ()
    return (f"{path}:1:{line_count}",)


def _git_lines(repo_root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _apply_path_selection(
    path: str,
    category: str,
    *,
    changed_paths: tuple[str, ...],
    selected: dict[str, SelectedCheckDraft],
    affected_roots: set[str],
    blocking_results: list[dict[str, str]],
    registration_debt: list[dict[str, Any]],
    release_versions: set[str],
    repo_root: Path,
    changed_sections_by_path: dict[str, tuple[str, ...]],
    tracked_deletion: bool,
) -> None:
    # Record-store owns complete-set validation for its explicitly selected
    # roots. Historical review/lifecycle validators must not reinterpret them.
    change_root = _change_root(path)
    if change_root:
        manifest_path = change_root + "change.json"
        manifest = repo_root / manifest_path
        relative = path.removeprefix(change_root)
        reserved = relative in {"change.json", "evidence.json", "material-decisions.json", "verify-report.json"} or bool(re.fullmatch(r"reviews/[^/]+\.json", relative))
        if manifest.exists() or manifest.is_symlink() or reserved:
            if is_archival_record_store(repo_root, Path(manifest_path).parent.name):
                return
            _add_check(selected, "change_metadata.validate",
                       "Validate the selected v3 set, including malformed manifests and reserved residue.", path=manifest_path)
            _add_check(selected, "change_metadata.regression", "Retain current record validation boundary proof.")
            affected_roots.add(change_root)
            try:
                metadata = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                metadata = None
            if isinstance(metadata, dict):
                # Compare without hashing untrusted JSON arrays/objects.
                if (metadata.get("schema_version"), metadata.get("contract")) not in ((3, "rigorloop-records-v3"),):
                    blocking_results.append({"code": "unsupported-change-contract", "path": manifest_path,
                                             "message": "Unsupported current record contract; no legacy fallback."})
                elif path != manifest_path:
                    kind = {"evidence.json": "evidence", "material-decisions.json": "decisions", "verify-report.json": "verify"}.get(relative)
                    if re.fullmatch(r"reviews/[a-z0-9][a-z0-9-]{0,79}\.json", relative):
                        kind = "review"
                    records = metadata.get("records")
                    if kind is None or not isinstance(records, list) or not any(isinstance(r, dict) and r.get("path") == path and r.get("kind") == kind for r in records):
                        blocking_results.append({"code": "unregistered-recording-path", "path": path,
                                                 "message": "Recording paths must be explicitly registered."})
            return
        # Noncurrent archival evidence has no operational validation route.
        # Dedicated removal checks remain selected for archive-path changes.
        _add_check(selected, "record_retirement.regression", "Archival paths must not restore execution or obstruct current records.")
        return
    if _is_boundary_first_surface(path):
        _add_check(
            selected,
            "boundary_first.validate",
            "Changed boundary-first contract, skill, validator, or package surface requires boundary validation.",
            path=path,
        )
    if _is_boundary_first_reference_surface(path):
        _add_check(
            selected,
            "boundary_first.reference_regression",
            "Changed boundary-first reference surface requires reference projection regression fixtures.",
            path=path,
        )
    if _is_boundary_first_validation_surface(path):
        _add_check(
            selected,
            "boundary_first.regression",
            "Changed boundary-first validator or fixture requires boundary validation regression fixtures.",
            path=path,
        )
    if _is_tier_b_documentation_prose_path(path) and not _proven_prose_deletion(
        path, repo_root=repo_root, tracked_deletion=tracked_deletion
    ):
        _add_check(
            selected,
            "documentation_prose.audit",
            "Changed Tier B Markdown prose requires documentation prose audit validation.",
            path=path,
        )

    if category == "skills":
        root = _skill_root(path)
        if root:
            affected_roots.add(root)
        _add_check(selected, "skills.validate", "Changed canonical skill source requires skill validation.")
        _add_check(selected, "skills.regression", "Changed canonical skill source requires skill regression fixtures.")
        _add_check(
            selected,
            "adapters.regression",
            "Changed canonical skill source requires retained package inventory and output-safety fixtures.",
        )
        _add_check(selected, "adapters.drift", "Public adapter output can be affected by canonical skill changes.")
        return

    if category == "generated-skills":
        _add_check(
            selected,
            "adapters.regression",
            "Local installation path changes require retained package inventory and output-safety fixtures.",
        )
        return

    if category in {"generated-adapters", "adapters"}:
        _add_check(selected, "adapters.regression", "Adapter output or generator change requires adapter regression fixtures.")
        _add_check(selected, "adapters.drift", "Adapter output or generator change requires adapter drift check.")
        _add_check(selected, "adapters.validate", "Adapter output or generator change requires adapter validation.")
        return

    if category == "lifecycle":
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed lifecycle artifact requires artifact lifecycle validation.",
            path=path,
        )
        return

    if category == "architecture-diagram":
        architecture_doc = _architecture_doc_for_diagram(path)
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed architecture diagram requires validation of its architecture package context.",
            path=architecture_doc or path,
        )
        return

    if category == "plan-index":
        _add_check(
            selected,
            "guide_system.validate",
            "Changed plan index surface requires cross-guide boundary validation.",
        )
        context_paths = _plan_index_context_paths(changed_paths, repo_root)
        for index_path in _plan_index_surface_paths():
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed plan index surface requires paired plan index surface lifecycle validation.",
                path=index_path,
            )
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed plan index requires artifact lifecycle validation with the related plan context.",
            path=path,
        )
        for context_path in context_paths:
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed plan index requires artifact lifecycle validation with the related plan context.",
                path=context_path,
            )
        return

    if category == "release":
        if _is_flat_release_evidence_path(path):
            _add_check(
                selected,
                "artifact_lifecycle.validate",
                "Changed flat release evidence requires release evidence checklist validation.",
                path=path,
            )
            return
        version = _release_version_from_path(path)
        if not version:
            blocking_results.append(
                {
                    "code": "release-version-required",
                    "path": path,
                    "message": "release version could not be inferred from release path",
                }
            )
            return
        release_versions.add(version)
        _add_check(selected, "release.validate", "Changed release artifact requires release validation.", version=version)
        return

    if category == "readme":
        _add_check(
            selected,
            "documentation_prose.enforce",
            "Changed Tier A README prose requires documentation prose enforcement validation.",
            path=path,
        )
        _add_check(selected, "readme.validate", "Changed README requires lightweight README validation.")
        _add_check(
            selected,
            "markdown_readability.validate",
            "Changed README requires Markdown readability validation.",
            path=path,
            changed_sections=changed_sections_by_path.get(path, ()),
        )
        _add_check(
            selected,
            "guide_system.validate",
            "Changed README requires cross-guide index validation.",
        )
        return

    if category == "learn-artifact":
        _add_check(
            selected,
            "guide_system.validate",
            "Changed learn session requires non-authority guide validation.",
        )
        return

    if category == "skill-source-archive":
        _add_check(selected, "skills.regression", "Skill archive changes require original-byte, retained-owner and navigation protection.")
        return

    if category == "research-artifact":
        _add_check(
            selected,
            "documentation_prose.audit",
            "Changed research artifact requires documentation prose audit validation.",
            path=path,
        )
        _add_check(
            selected,
            "markdown_readability.validate",
            "Changed research artifact requires Markdown readability validation.",
            path=path,
            changed_sections=changed_sections_by_path.get(path, ()),
        )
        return

    if category == "requirement-fidelity-spec-read":
        _add_check(
            selected,
            "requirement_fidelity.spec_reads",
            "Changed requirement-fidelity spec-read proof requires bounded-read validation.",
        )
        return

    if category == "retired-examples":
        return

    if category == "living-reference/project-map":
        _add_check(
            selected,
            "guide_system.validate",
            "Changed project map requires cross-guide scope validation.",
        )
        return

    if category == "follow-up-register":
        _add_check(
            selected,
            "skills.regression",
            "Changed follow-up register requires follow-up register static validation.",
        )
        return

    if category == "vision":
        _add_check(
            selected,
            "documentation_prose.enforce",
            "Changed Tier A VISION prose requires documentation prose enforcement validation.",
            path=path,
        )
        _add_check(
            selected,
            "markdown_readability.validate",
            "Changed root vision requires Markdown readability validation.",
            path=path,
            changed_sections=changed_sections_by_path.get(path, ()),
        )
        _add_check(
            selected,
            "readme.vision_markers",
            "Changed root vision requires README vision marker validation.",
        )
        _add_check(
            selected,
            "guide_system.validate",
            "Changed root vision requires cross-guide registry duplication validation.",
        )
        return

    if category == "guide-system-validator":
        _add_check(
            selected,
            "guide_system.regression",
            "Changed guide-system validator requires guide-system regression fixtures.",
        )
        _add_check(
            selected,
            "guide_system.validate",
            "Changed guide-system validator requires live guide-system validation.",
        )
        return

    if category in {"selector", "ci-wrapper"}:
        reason = (
            "Changed CI wrapper requires selector and wrapper regression fixtures."
            if category == "ci-wrapper"
            else "Changed selector code requires selector regression fixtures."
        )
        _add_check(selected, "selector.regression", reason)
        _add_check(selected, "validation_execution.regression", reason)
        return

    if category == "boundary-first":
        return

    if category in {"explicit-recording", "isolated-recording-evidence"}:
        for check_id in ("rigorloop_cli.test", "record_store.schema", "model.validate",
                         "boundary_first.regression", "change_metadata.regression"):
            _add_check(selected, check_id,
                       "Explicit recording adoption requires model, schema and historical/runtime compatibility proof.",
                       path=path)
        if path.startswith("packages/rigorloop/"):
            _add_check(selected, "npm_package_publication.test",
                       "Record-store package paths retain tarball and installed-binary compatibility proof.")
        if category == "isolated-recording-evidence" and not _proven_prose_deletion(
            path, repo_root=repo_root, tracked_deletion=tracked_deletion
        ):
            _add_check(selected, "documentation_prose.audit",
                       "Isolated advisory evidence requires prose checks and its underlying model/runtime proof, not formal settlement.", path=path)
        return

    if category == "token-cost":
        _add_check(
            selected,
            "token_cost.regression",
            "Changed token-cost measurement surface requires token-cost measurement regression fixtures.",
        )
        if _is_token_cost_report_validation_surface(path):
            _add_check(
                selected,
                "token_cost.report_regression",
                "Changed token-cost report validation surface requires report validator regression fixtures.",
            )
        if _is_token_cost_release_report_yaml(path):
            _add_check(
                selected,
                "token_cost.report_validate",
                "Changed token-cost release report metadata requires report validation.",
                path=path,
            )
        return

    if category == "adapter-artifact-metadata":
        _add_check(
            selected,
            "adapters.regression",
            "Changed adapter artifact metadata requires adapter distribution regression fixtures.",
        )
        return

    if category == "validator-review-artifacts":
        _add_check(
            selected,
            "review_artifacts.regression",
            "Changed review artifact validator requires review artifact regression fixtures.",
        )
        return

    if category == "review-artifact-fixtures":
        _add_check(
            selected,
            "review_artifacts.regression",
            "Changed review artifact fixture requires review artifact regression fixtures.",
        )
        if path.endswith("/change.yaml"):
            _add_check(
                selected,
                "change_metadata.regression",
                "Changed review artifact metadata fixture requires change metadata regression fixtures.",
            )
        return

    if category == "change-metadata-fixtures":
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed change metadata fixture requires change metadata regression fixtures.",
        )
        return

    if category == "record-retirement":
        _add_check(
            selected,
            "record_retirement.regression",
            "Removed record surfaces require safe rejection and archival exclusion proof.",
        )
        _add_check(
            selected,
            "change_metadata.regression",
            "Removed metadata surfaces require current wrapper regression proof.",
        )
        return

    if category == "change-record-query":
        _add_check(
            selected,
            "change_record_query.regression",
            "Changed change-record query helper requires query regression fixtures.",
        )
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed change-record query helper depends on supported change metadata shapes.",
        )
        return

    if category == "workflow-automation":
        for check_id in (
            "workflow_automation.code_state_regression",
            "workflow_automation.engine_regression",
            "workflow_automation.policy_regression",
            "workflow_automation.state_regression",
            "workflow_automation.validator_regression",
        ):
            _add_check(
                selected,
                check_id,
                "Changed workflow automation tooling requires complete code-state, engine, policy, state, and validator regression proof.",
            )
        return

    if category == "validator-artifact-lifecycle":
        _add_check(
            selected,
            "artifact_lifecycle.regression",
            "Changed artifact lifecycle validator requires lifecycle regression fixtures.",
        )
        return

    if category == "artifact-lifecycle-fixtures":
        _add_check(
            selected,
            "artifact_lifecycle.regression",
            "Changed artifact lifecycle fixture requires lifecycle regression fixtures.",
        )
        return

    if category == "validation-retirement":
        for check_id in ("artifact_lifecycle.regression", "change_metadata.regression"):
            _add_check(selected, check_id,
                       "Retired cache paths require current execution and safe rejection proof.", path=path)
        return

    if category == "retained-change-fixture":
        _add_check(
            selected,
            "artifact_lifecycle.regression",
            "Changed retained change fixture rationale requires lifecycle regression fixtures.",
        )
        _add_check(
            selected,
            "artifact_lifecycle.validate",
            "Changed retained change fixture rationale requires lifecycle validation.",
            path=path,
        )
        return

    if category == "validator-change-metadata":
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed change metadata validator requires change metadata regression fixtures.",
        )
        return

    if category == "validator-documentation-prose":
        _add_check(
            selected,
            "documentation_prose.regression",
            "Changed documentation prose validator, fixtures, or formatter guardrails require prose validator regression fixtures.",
        )
        return

    if category == "validator-skills":
        _add_check(selected, "skills.regression", "Changed skill generation or validation requires skill regression fixtures.")
        _add_check(
            selected,
            "adapters.regression",
            "Changed skill generation or validation requires retained package inventory and output-safety fixtures.",
        )
        return

    if category == "markdown-readability-validator":
        _add_check(
            selected,
            "markdown_readability.regression",
            "Changed Markdown readability validator requires readability regression fixtures.",
        )
        return

    if category in {"ci-workflow", "templates"}:
        _add_check(
            selected,
            "selector.regression",
            f"Changed {category} path requires selector and workflow routing regression fixtures.",
        )
        return

    if category in {"workflow-guidance", "governance"}:
        _add_check(
            selected,
            "selector.regression",
            f"Changed {category} path requires selector and workflow routing regression fixtures.",
        )
        _add_check(
            selected,
            "guide_system.validate",
            f"Changed {category} path requires cross-guide validation.",
        )
        _add_lifecycle_warning_check(
            selected,
            path,
            f"Changed {category} path can carry lifecycle policy and requires lifecycle-language warning validation.",
        )
        return

    if category == "contributor-guidance":
        _add_check(
            selected,
            "selector.regression",
            "Changed contributor guidance requires selector and workflow routing regression fixtures.",
        )
        _add_check(
            selected,
            "guide_system.validate",
            "Changed contributor guidance requires cross-guide validation.",
        )
        _add_lifecycle_warning_check(
            selected,
            path,
            "Changed contributor guidance can carry lifecycle policy and requires lifecycle-language warning validation.",
        )
        return

    if category == "ignore-policy":
        _add_check(
            selected,
            "adapters.regression",
            "Changed ignore policy requires retained package inventory and output-safety fixtures.",
        )
        return

    if category == "schemas":
        _add_check(
            selected,
            "change_metadata.regression",
            "Changed schema path requires change metadata regression fixtures.",
        )
        return

    if category == "release-script":
        _add_check(
            selected,
            "adapters.regression",
            "Changed release script requires release and adapter distribution regression fixtures.",
        )
        return

    if category == "release-transaction":
        _add_check(
            selected,
            "release_transaction.regression",
            "Changed release transaction automation requires focused release transaction regression fixtures.",
        )
        return

    if category == "rigorloop-cli":
        _add_check(
            selected,
            "rigorloop_cli.test",
            "Changed RigorLoop CLI package requires package test validation.",
        )
        _add_check(
            selected,
            "npm_package_publication.test",
            "Changed RigorLoop npm package surface requires package publication validation.",
        )
        return

    if category == "governed-lifecycle-cli-wrapper":
        _add_check(
            selected,
            "governed_lifecycle_cli_wrapper.test",
            "Changed governed lifecycle wrapper requires focused child-result parity tests.",
        )
        _add_check(
            selected,
            "rigorloop_cli.test",
            "Changed governed lifecycle wrapper requires public CLI integration tests.",
        )
        return

    blocking_results.append(
        {
            "code": "manual-routing-required",
            "path": path,
            "message": f"changed {category} path has no deterministic v1 selector check",
        }
    )


def _add_check(
    selected: dict[str, SelectedCheckDraft],
    check_id: str,
    reason: str,
    *,
    path: str | None = None,
    affected_root: str | None = None,
    version: str | None = None,
    changed_sections: tuple[str, ...] = (),
) -> None:
    draft = selected.setdefault(check_id, SelectedCheckDraft(id=check_id))
    if reason not in draft.reasons:
        draft.reasons.append(reason)
    if path:
        draft.paths.add(path)
    for changed_section in changed_sections:
        draft.changed_sections.add(changed_section)
    if affected_root:
        draft.affected_roots.add(affected_root)
    if version:
        draft.versions.add(version)


def _add_lifecycle_warning_check(
    selected: dict[str, SelectedCheckDraft],
    path: str,
    reason: str,
) -> None:
    _add_check(selected, "artifact_lifecycle.validate", reason, path=path)


def _proven_prose_deletion(path: str, *, repo_root: Path, tracked_deletion: bool) -> bool:
    # Selection can include committed deletions as well as worktree deletions.
    # Never suppress a present input, unsafe symlink, or unproven missing path.
    target = repo_root / path
    if target.exists() or target.is_symlink():
        return False
    if tracked_deletion:
        return True
    result = subprocess.run(
        ["git", "log", "-1", "--format=", "--name-status", "--no-renames", "HEAD", "--", path],
        cwd=repo_root, capture_output=True, text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == f"D\t{path}"


def _build_result(
    *,
    repo_root: Path = Path.cwd(),
    mode: str,
    base: str | None = None,
    head: str | None = None,
    changed_paths: list[str],
    classified_paths: list[dict[str, str]],
    unclassified_paths: list[str],
    selected: dict[str, SelectedCheckDraft],
    affected_roots: set[str],
    broad_smoke_sources: list[dict[str, str]],
    blocking_results: list[dict[str, str]],
    preflight_results: list[dict[str, Any]] | None = None,
    registration_debt: list[dict[str, Any]] | None = None,
    status: str,
    adapter_version: str = DEFAULT_ADAPTER_VERSION,
) -> SelectionResult:
    selected_checks: list[dict[str, Any]] = []
    build_errors: list[dict[str, str]] = []
    for check_id in CHECK_CATALOG:
        draft = selected.get(check_id)
        if draft is None:
            continue
        paths = tuple(sorted(draft.paths))
        changed_sections = tuple(sorted(draft.changed_sections))
        roots = tuple(sorted(draft.affected_roots))
        versions = tuple(sorted(draft.versions))
        try:
            command = catalog_command(
                check_id,
                repo_root=repo_root,
                mode=mode,
                base=base,
                head=head,
                paths=paths,
                changed_sections=changed_sections,
                affected_roots=roots,
                versions=versions,
                adapter_version=adapter_version,
            )
        except ValueError as exc:
            build_errors.append(
                {
                    "code": "command-substitution-error",
                    "message": str(exc),
                }
            )
            continue
        entry: dict[str, Any] = {
            "id": check_id,
            "command": command,
            "reason": " ".join(draft.reasons),
            "phase": "boundary" if check_id in BOUNDARY_CHECK_IDS else "focused",
            "cache_status": "not-applicable",
        }
        if paths:
            entry["paths"] = list(paths)
        if changed_sections:
            entry["changed_sections"] = list(changed_sections)
        if roots:
            entry["affected_roots"] = list(roots)
        if versions:
            entry["versions"] = list(versions)
        selected_checks.append(entry)

    combined_blocking = [*blocking_results, *build_errors]
    final_status = "error" if build_errors else status
    return SelectionResult(
        mode=mode,
        status=final_status,
        changed_paths=tuple(changed_paths),
        classified_paths=tuple(classified_paths),
        unclassified_paths=tuple(unclassified_paths),
        selected_checks=tuple(selected_checks),
        affected_roots=tuple(sorted(affected_roots)),
        broad_smoke_required=bool(broad_smoke_sources),
        broad_smoke={
            "required": bool(broad_smoke_sources),
            "sources": list(broad_smoke_sources),
        },
        blocking_results=tuple(combined_blocking),
        preflight_results=tuple(preflight_results or []),
        registration_debt=tuple(registration_debt or []),
        rationale=tuple(entry["reason"] for entry in selected_checks),
    )


def _path_category(path: str) -> str | None:
    parts = path.split("/")
    if path in ISOLATED_RECORDING_EVIDENCE:
        return "isolated-recording-evidence"
    if (path.startswith("docs/design/")
            or path.startswith("tests/fixtures/explicit-recording-v1/")
            or path.startswith("tests/fixtures/rigorloop-records-v3/")
            or path in {"schemas/rigorloop-records-v3.schema.json", "templates/rigorloop-records-v3/records.json",
                        "packages/rigorloop/dist/schemas/rigorloop-records-v3.schema.json",
                        "packages/rigorloop/dist/templates/rigorloop-records-v3/records.json",
                        "packages/rigorloop/dist/lib/record-format-v3.js", "packages/rigorloop/dist/lib/record-format-core.js",
                        "packages/rigorloop/test/helpers/v3-fixture.mjs", "packages/rigorloop/test/helpers/record-store-launcher.mjs",
                        "packages/rigorloop/dist/lib/record-json.js", "scripts/classify-record-store.mjs", "scripts/record_store_classification.py"}
            or path in {"schemas/targeted-recording-v1.schema.json", "packages/rigorloop/dist/schemas/targeted-recording-v1.schema.json", "schemas/explicit-recording-v1.schema.json", "scripts/build-record-store-schema.mjs", "scripts/validate-record-store.mjs",
                        "templates/explicit-recording/records.json", "packages/rigorloop/dist/templates/explicit-recording/records.json",
                        "packages/rigorloop/dist/schemas/explicit-recording-v1.schema.json"}
            or (path.startswith("packages/rigorloop/dist/lib/recording-") and path.endswith(".js"))
            or (path.startswith("packages/rigorloop/dist/lib/record-store") and path.endswith(".js"))
            or (path.startswith("packages/rigorloop/test/record-store-") and path.endswith(".test.js"))
            or path in {"packages/rigorloop/test/helpers/record-store-launcher.mjs", "packages/rigorloop/test/helpers/recording-query-launcher.mjs", "packages/rigorloop/test/helpers/record-store-interactions.mjs", "packages/rigorloop/test/helpers/record-store-tokenize.py", "packages/rigorloop/test/fixtures/recording-interactions/README.md"}):
        return "explicit-recording"
    if path == "specs/boundary-first-activation.yaml":
        return "lifecycle"
    if path == "README.md":
        return "readme"
    if path == ROOT_VISION_PATH:
        return "vision"
    if path.startswith("tests/fixtures/compact-current-state-v1/"):
        return "record-retirement"
    if path in {"scripts/test-compact-current-state-canonical-contract.py",
                "scripts/test-retirement-ledger.py", "scripts/retirement_ledger.py"}:
        return "record-retirement"
    if path == "schemas/compact-current-state-v1.schema.json":
        return "record-retirement"
    if path.startswith("tests/fixtures/artifact-lifecycle/"):
        return "artifact-lifecycle-fixtures"
    if path.startswith("tests/fixtures/review-artifacts/"):
        return "review-artifact-fixtures"
    if path == "tests/fixtures/change-metadata" or path.startswith("tests/fixtures/change-metadata/"):
        return "change-metadata-fixtures"
    if path.startswith("tests/fixtures/requirement-fidelity-gate/representative-reviews/"):
        return "requirement-fidelity-spec-read"
    if path.startswith("tests/fixtures/documentation-prose/"):
        return "validator-documentation-prose"
    if path.startswith("tests/fixtures/adapters/"):
        return "adapters"
    if path.startswith("tests/fixtures/release-transaction/"):
        return "release-transaction"
    if path == "tests/fixtures/skills" or path.startswith("tests/fixtures/skills/"):
        return "validator-skills"
    if path.startswith("skills/"):
        return "skills"
    if path.startswith(".codex/skills/"):
        return "generated-skills"
    if path.startswith("dist/adapters/"):
        return "generated-adapters"
    if path.startswith("scripts/adapter_templates/") or path in {
        "scripts/adapter_distribution.py",
        "scripts/build-adapters.py",
        "scripts/test-adapter-distribution.py",
        "scripts/validate-adapters.py",
    }:
        return "adapters"
    if path == "scripts/model_layout.py":
        return "selector"
    if _is_boundary_first_reference_surface(path) or _is_boundary_first_validation_surface(path):
        return "boundary-first"
    if path in {
        "scripts/select-validation.py",
        "scripts/validation_selection.py",
        "scripts/validation_execution.py",
        "scripts/test-validation-execution.py",
        "scripts/test-select-validation.py",
        "scripts/validate-broad-smoke-classification.py",
        "scripts/validate-readme.py",
    }:
        return "selector"
    if path in {
        "scripts/validate-markdown-readability.py",
        "scripts/test-markdown-readability-validator.py",
    }:
        return "markdown-readability-validator"
    if path == "scripts/test-fidelity-gate-spec-reads.py":
        return "requirement-fidelity-spec-read"
    if path in {"scripts/validate-guide-system.py", "scripts/test-guide-system-validator.py"}:
        return "guide-system-validator"
    if path == "scripts/ci.sh":
        return "ci-wrapper"
    if path == ".gitignore":
        return "ignore-policy"
    if path == ".github/workflows/ci.yml":
        return "ci-workflow"
    if path == ".github/workflows/release.yml":
        return "release-script"
    if path in {"scripts/validate-review-artifacts.py", "scripts/review_artifact_validation.py", "scripts/test-review-artifact-validator.py"}:
        return "validator-review-artifacts"
    if path in {
        "scripts/validate-artifact-lifecycle.py",
        "scripts/artifact_lifecycle_validation.py",
        "scripts/artifact_lifecycle_contracts.py",
        "scripts/lifecycle_state_sync.py",
        "scripts/test-artifact-lifecycle-validator.py",
    }:
        return "validator-artifact-lifecycle"
    if path in {"scripts/validation_cache.py", "scripts/test-validation-cache.py"}:
        return "validation-retirement"
    if path in {
        "scripts/change_metadata_semantics.py", "scripts/project_yaml.py",
        "scripts/validate-change-metadata.py",
        "scripts/test-change-metadata-validator.py",
    }:
        return "validator-change-metadata"
    if path in {
        "scripts/validate-documentation-prose.py",
        "scripts/test-documentation-prose-validator.py",
    }:
        return "validator-documentation-prose"
    if path in {
        "scripts/query-change-record.py",
        "scripts/test-query-change-record.py",
    }:
        return "change-record-query"
    if path in {
        "scripts/workflow_code_state.py",
        "scripts/test-workflow-code-state.py",
        "scripts/workflow_automation.py",
        "scripts/test-workflow-automation.py",
        "scripts/workflow_automation_policy.py",
        "scripts/test-workflow-automation-policy.py",
        "scripts/workflow_automation_state.py",
        "scripts/test-workflow-automation-state.py",
        "scripts/validate_workflow_automation.py",
        "scripts/test-validate-workflow-automation.py",
    }:
        return "workflow-automation"
    if path in {
        # Retired paths stay classifiable for deletion diffs, never executable.
        "scripts/build-skills.py",
        "scripts/validate-skills.py",
        "scripts/skill_validation.py",
        "scripts/review_independence_skill_phrases.py",
        "scripts/test-build-skills.py",
        "scripts/test-skill-validator.py",
    }:
        return "validator-skills"
    if path in {
        "scripts/analyze-codex-jsonl.py",
        "scripts/measure-skill-tokens.py",
        "scripts/run-token-cost-benchmarks.py",
        "scripts/measure-cli-result-bytes.py",
        "scripts/test-cli-result-measurement.py",
        "scripts/test-token-cost-measurement.py",
        "scripts/test-token-cost-report-validation.py",
        "scripts/validate-token-cost-report.py",
    }:
        return "token-cost"
    if path.startswith("benchmarks/token-cost/"):
        return "token-cost"
    if path.startswith("docs/reports/token-cost/"):
        return "token-cost"
    if path == "packages/rigorloop" or path.startswith("packages/rigorloop/"):
        return "rigorloop-cli"
    if path in {
        "scripts/npm_package_validation.py",
        "scripts/validate-npm-package.py",
        "scripts/test-npm-package-publication.py",
    }:
        return "rigorloop-cli"
    if path in {
        "scripts/validate-governed-lifecycle-cli.py",
        "scripts/test-governed-lifecycle-cli-validator.py",
    }:
        return "governed-lifecycle-cli-wrapper"
    if path.startswith("docs/reports/adapter-artifacts/releases/") and path.endswith(".yaml"):
        return "adapter-artifact-metadata"
    if path.startswith("tests/fixtures/token-cost/"):
        return "token-cost"
    if path.startswith("docs/examples/"):
        return "retired-examples"
    if path in SKILL_SOURCE_ARCHIVE_PATHS:
        return "skill-source-archive"
    if path.startswith("docs/research/") and path.endswith(".md"):
        return "research-artifact"
    if path == "docs/project-map.md" or (
        path.startswith("docs/project-map/") and path.endswith(".md")
    ):
        return "living-reference/project-map"
    if path == "docs/follow-ups.md":
        return "follow-up-register"
    if path.startswith("docs/changes/"):
        return "change-records"
    if path in _plan_index_surface_paths():
        return "plan-index"
    if path.startswith("docs/architecture/") and path.endswith(".mmd"):
        return "architecture-diagram"
    if _is_learn_artifact_path(path):
        return "learn-artifact"
    if _is_lifecycle_path(path):
        return "lifecycle"
    if path.startswith("docs/releases/"):
        if path in {"docs/releases/README.md", "docs/releases/index.md"}:
            return "workflow-guidance"
        return "release"
    if path == "docs/workflows.md":
        return "workflow-guidance"
    if path == "CONTRIBUTING.md":
        return "contributor-guidance"
    if path in {".prettierrc.json", ".markdownlint.json"}:
        return "validator-documentation-prose"
    if path in {"AGENTS.md", "CONSTITUTION.md"}:
        return "governance"
    if path.startswith("templates/"):
        return "templates"
    if path.startswith("schemas/"):
        return "schemas"
    if path in {
        "scripts/close-release-publication.py",
        "scripts/prepare-release.py",
        "scripts/release-preflight.py",
        "scripts/release_transaction.py",
        "scripts/release_candidate.py",
        "scripts/release_candidate_tests.py",
        "scripts/release_execution.py",
        "scripts/release_execution_tests.py",
        "scripts/release_provider.py",
        "scripts/release_coordination.py",
        "scripts/release_coordination_tests.py",
        "scripts/release-coordinator.py",
        "scripts/test-release-transaction.py",
    }:
        return "release-transaction"
    # Keep the retired alias path classified so deletion diffs still select protection.
    if path in {"scripts/validate-release.py", "scripts/validate-release-ci.py", "scripts/release-verify.sh"}:
        return "release-script"
    if path.startswith("scripts/"):
        return "script-unsupported"
    return None


def _is_boundary_first_surface(path: str) -> bool:
    return (
        path == "specs/boundary-first-activation.yaml"
        or path == "specs/boundary-first-resources.yaml"
        or path == "specs/references/boundary-first-method-v1.md"
        or (path.startswith("specs/") and path.endswith(".md"))
        or (
            path.startswith("skills/")
            and (
                path.endswith("/SKILL.md")
                or path.endswith("/references/boundary-first-method-v1.md")
            )
        )
        or path.startswith("dist/adapters/")
        or path.startswith("scripts/fixtures/boundary-first/")
        or path
        in {
            "scripts/boundary_first_validation.py",
            "scripts/model_layout.py",
            "scripts/validate-boundary-first.py",
            "scripts/test-boundary-first-validation.py",
            "scripts/boundary_first_reference.py",
            "scripts/project-boundary-first-reference.py",
            "scripts/test-boundary-first-reference.py",
        }
    )


def _is_boundary_first_reference_surface(path: str) -> bool:
    return (
        path in {
            "specs/boundary-first-resources.yaml",
            "specs/references/boundary-first-method-v1.md",
        }
        or path.endswith("/references/boundary-first-method-v1.md")
        or path
        in {
            "scripts/boundary_first_reference.py",
            "scripts/project-boundary-first-reference.py",
            "scripts/test-boundary-first-reference.py",
        }
    )


def _is_boundary_first_validation_surface(path: str) -> bool:
    return path.startswith("scripts/fixtures/boundary-first/") or path in {
        "scripts/boundary_first_validation.py",
        "scripts/model_layout.py",
        "scripts/validate-boundary-first.py",
        "scripts/test-boundary-first-validation.py",
    }


# Exact byte-preserved source snapshots and their navigation selected by the
# Skill displacement map. Other archive paths remain unclassified/fail closed.
SKILL_SOURCE_ARCHIVE_PATHS = frozenset({
    "docs/archive/skill-model/2026-09-08/README.md",
    "docs/archive/skill-model/2026-09-08/specs/skill-contract.md",
    "docs/archive/skill-model/2026-09-08/specs/skill-readability-contract.md",
    "docs/archive/skill-model/2026-09-08/specs/customer-portable-public-skill-evidence.md",
    "docs/archive/skill-model/2026-09-08/docs/adr/ADR-20260623-published-skill-resource-integrity.md",
})


def _is_lifecycle_path(path: str) -> bool:
    if path == "docs/plan.md":
        return False
    if path.startswith("docs/proposals/") and path.endswith(".md"):
        return True
    if path.startswith("specs/") and path.endswith(".md"):
        return True
    if path.startswith("docs/architecture/") and path.endswith(".md"):
        return True
    if path.startswith("docs/adr/") and path.endswith(".md"):
        return True
    if path.startswith("docs/plans/") and path.endswith(".md"):
        return True
    if path.startswith("docs/vision/") and path.endswith(".md"):
        return True
    if path.startswith("docs/explain/") and path.endswith(".md"):
        return True
    return False


def _is_tier_b_documentation_prose_path(path: str) -> bool:
    if path.startswith("skills/") and path.endswith("/SKILL.md"):
        return True
    if path.startswith("docs/changes/") and path.endswith("/explain-change.md"):
        return True
    return False


def _is_token_cost_release_report_yaml(path: str) -> bool:
    return (
        path.startswith("docs/reports/token-cost/releases/")
        and path.endswith(".yaml")
    )


def _is_token_cost_report_validation_surface(path: str) -> bool:
    return path in {
        "scripts/validate-token-cost-report.py",
        "scripts/test-token-cost-report-validation.py",
    } or path.startswith("tests/fixtures/token-cost/reports/")


def _is_learn_artifact_path(path: str) -> bool:
    if path == "docs/learn/README.md":
        return True
    if path.startswith("docs/learn/sessions/") and path.endswith(".md"):
        return True
    if path.startswith("docs/learn/topics/") and path.endswith(".md"):
        return True
    return False


def _is_plan_index_migration_proof(path: str) -> bool:
    return path.startswith("docs/changes/") and path.endswith("/plan-index-migration.md")


def _plan_index_surface_paths() -> tuple[str, str]:
    return ("docs/plan-archive.md", "docs/plan.md")


def _architecture_doc_for_diagram(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) < 4 or parts[0] != "docs" or parts[1] != "architecture":
        return None
    try:
        diagrams_index = parts.index("diagrams")
    except ValueError:
        return None
    if diagrams_index <= 2:
        return None
    return "/".join([*parts[:diagrams_index], "architecture.md"])


def _plan_index_context_paths(changed_paths: tuple[str, ...], repo_root: Path) -> list[str]:
    context: list[str] = []
    for path in changed_paths:
        if path == "docs/plan.md":
            continue
        if _is_lifecycle_path(path):
            context.append(path)
            continue
        if path.startswith("docs/changes/"):
            root = _change_root(path)
            if root and ((repo_root / (root + "change.json")).exists() or path.endswith(".json")):
                context.append(root + "change.json")
    return _dedupe(context)


def _skill_root(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 2:
        return f"skills/{parts[1]}"
    return None


def _change_root(path: str) -> str | None:
    parts = path.split("/")
    if len(parts) >= 3 and parts[0] == "docs" and parts[1] == "changes":
        return f"docs/changes/{parts[2]}/"
    return None


def _release_version_from_path(path: str) -> str | None:
    parts = path.split("/")
    if _is_flat_release_evidence_path(path):
        return parts[2][:-3]
    if len(parts) >= 3 and parts[:3] == ["docs", "releases", "profiles"]:
        if len(parts) != 4:
            return None
        match = RELEASE_PROFILE_FILENAME_PATTERN.fullmatch(parts[3])
        return match.group(1) if match else None
    if len(parts) >= 4 and parts[0] == "docs" and parts[1] == "releases" and parts[2] and parts[3]:
        return parts[2]
    return None


def _is_flat_release_evidence_path(path: str) -> bool:
    parts = path.split("/")
    if len(parts) != 3 or parts[0] != "docs" or parts[1] != "releases":
        return False
    filename = parts[2]
    return filename.startswith("v") and filename.endswith(".md") and len(filename) > len("v.md")


def _broad_smoke_sources(
    request: SelectionRequest,
    *,
    changed_paths: list[str],
    repo_root: Path,
) -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    if request.mode in {"main", "release"}:
        sources.append({"type": "mode", "value": request.mode})
    if request.broad_smoke:
        sources.append({"type": "explicit_flag", "value": "--broad-smoke"})
    if request.mode == "release" and request.release_version:
        sources.append(
            {
                "type": "release_metadata",
                "path": f"docs/releases/{request.release_version}/release.yaml",
            }
        )

    context_paths = _dedupe([*changed_paths, *request.trigger_context_paths])
    for raw_path in context_paths:
        normalized = normalize_path(raw_path, repo_root=repo_root)
        if not normalized.ok or normalized.path is None:
            continue
        source_type = _trigger_source_type(normalized.path)
        if source_type is None:
            continue
        path = repo_root / normalized.path
        if source_type != "release_metadata" and not _file_requires_broad_smoke(path):
            continue
        source = {"type": source_type, "path": normalized.path}
        if source not in sources:
            sources.append(source)
    return sources


def _readme_marker_validation_required(changed_paths: tuple[str, ...], *, repo_root: Path) -> bool:
    readme_changed = "README.md" in changed_paths
    return _vision_skill_in_scope(changed_paths) or (readme_changed and _readme_has_standalone_marker_block(repo_root))


def _vision_skill_in_scope(changed_paths: tuple[str, ...]) -> bool:
    for path in changed_paths:
        if path == "skills/vision/SKILL.md":
            return True
        if path == ".codex/skills/vision/SKILL.md":
            return True
        if path.endswith("/skills/vision/SKILL.md") and path.startswith("dist/adapters/"):
            return True
        if path.startswith("specs/vision-skill") and path.endswith(".md"):
            return True
        if (
            "vision-skill" in path
            and path.endswith(".md")
            and (path.startswith("docs/proposals/") or path.startswith("docs/plans/"))
        ):
            return True
        if path.startswith("docs/changes/") and "vision-skill" in path:
            return True
    return False


def _readme_has_standalone_marker_block(repo_root: Path) -> bool:
    readme = repo_root / "README.md"
    if not readme.is_file():
        return False
    try:
        lines = readme.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return False
    return "<!-- vision:start -->" in lines or "<!-- vision:end -->" in lines


def _trigger_source_type(path: str) -> str | None:
    if path.startswith("docs/plans/") and path.endswith(".md"):
        return "active_plan"
    if path.startswith("specs/") and path.endswith(".test.md"):
        return "test_spec"
    if path.startswith("docs/changes/") and path.endswith("/review-resolution.md"):
        return "review_resolution"
    if path.startswith("docs/releases/") and path.endswith("/release.yaml"):
        return "release_metadata"
    return None


def _file_requires_broad_smoke(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    return "broad_smoke_required: true" in lowered or "broad smoke required" in lowered


def _join(*args: str) -> str:
    return shlex.join(args)


def _dedupe(items: list[str] | tuple[str, ...]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def _safe_path_label(path: str) -> str:
    if Path(path).is_absolute():
        return "<outside-repository>"
    return path
