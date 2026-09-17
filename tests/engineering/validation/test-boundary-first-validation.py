#!/usr/bin/env python3
"""Direct aggregate for portable boundary and current model validation."""

import unittest

from boundary_model_tests import ModelRecordTests
from catalog_admission_tests import TestDesignAdmissionTests
from boundary_command_tests import CurrentBoundaryCommandTests


if __name__ == "__main__":
    unittest.main(verbosity=2)
