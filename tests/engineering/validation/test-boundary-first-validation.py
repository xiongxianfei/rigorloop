#!/usr/bin/env python3
"""Direct aggregate for portable boundary and current model validation."""

import unittest

from boundary_structural_tests import BoundaryFirstStructuralTests
from boundary_path_tests import BoundaryFirstActivationTests
from boundary_handoff_tests import AdoptionReviewHandoffTests
from boundary_model_tests import ModelRecordTests
from boundary_command_tests import CurrentBoundaryCommandTests


if __name__ == "__main__":
    unittest.main(verbosity=2)
