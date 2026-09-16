"""Trusted catalog units, constraints and unknown-value rejection."""

from __future__ import annotations

import sys
from pathlib import Path
import dataclasses
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.validation.validation_selection import CHECK_CATALOG, ExecutionConstraints, validate_catalog


class CatalogTests(unittest.TestCase):
    def test_catalog_is_valid_and_unassessed_commands_are_serial(self):
        validate_catalog()
        self.assertIsNone(CHECK_CATALOG['boundary_first.validate'].constraints)
        self.assertEqual(CHECK_CATALOG['selector.regression'].constraints.unit,'python-unittest')

    def test_case_unit_rejects_contradictory_command_before_launch(self):
        from lib.validation.validation_selection import command_basis
        entry = CHECK_CATALOG['selector.regression']
        for command in ['bash tests/engineering/validation/test-select-validation.py','python -c pass']:
            candidate = dataclasses.replace(entry,command_template=command,
                constraints=dataclasses.replace(entry.constraints,basis=command_basis(command,'python-unittest')))
            with self.assertRaisesRegex(ValueError,'case command'):
                validate_catalog({entry.id:candidate})

    def test_node_unit_rejects_contradictory_command_before_launch(self):
        from lib.validation.validation_selection import command_basis
        for command in ['bash scripts/test.sh','node --test','npm run arbitrary']:
            entry=dataclasses.replace(CHECK_CATALOG['rigorloop_cli.test'],command_template=command,parallel_safe=True,
                constraints=ExecutionConstraints(unit='node-test',mode='bounded',isolation='fixture',basis=command_basis(command,'node-test')))
            with self.assertRaisesRegex(ValueError,'Node case command'):
                validate_catalog({entry.id:entry})

    def test_unknown_value_units_modes_fields_and_stale_basis_reject(self):
        entry = CHECK_CATALOG['skills.regression']
        for changes in ({'unit':'unknown_value'}, {'mode':'unknown_value'},
                        {'demand':0}, {'shared_writes':True}, {'basis':'stale'},
                        {'isolation':''}):
            candidate = dataclasses.replace(entry, constraints=dataclasses.replace(entry.constraints, **changes))
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate_catalog({entry.id:candidate})
        with self.assertRaises(TypeError):
            ExecutionConstraints(unknown_value=True)
        with self.assertRaisesRegex(ValueError,'mode membership'):
            validate_catalog({entry.id:dataclasses.replace(entry,modes=('unknown_value',))})
        candidate = dataclasses.replace(entry, command_template=entry.command_template+' --changed')
        with self.assertRaisesRegex(ValueError, 'basis'):
            validate_catalog({entry.id:candidate})
