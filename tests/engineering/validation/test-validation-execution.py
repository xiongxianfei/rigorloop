#!/usr/bin/env python3
"""Direct aggregate for executor process, discovery and composition proof."""

import unittest

from execution_python_adapter_tests import CaseAdapterTests
from execution_process_tests import ExecutionTests
from execution_node_adapter_tests import NodeCaseAdapterTests
from execution_catalog_tests import CatalogTests
from execution_composition_tests import CompositionTests
from execution_reporting_tests import ReportingTests


class ImmediateFailureResult(unittest.TextTestResult):
    # The outer CI timeout may terminate this integration suite before unittest
    # prints its final summary. Preserve the original traceback as it happens.
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(self.failures[-1][1])
        self.stream.flush()

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(self.errors[-1][1])
        self.stream.flush()


class ImmediateFailureRunner(unittest.TextTestRunner):
    resultclass = ImmediateFailureResult


if __name__ == '__main__':
    unittest.main(testRunner=ImmediateFailureRunner)
