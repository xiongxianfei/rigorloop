#!/usr/bin/env python3
"""Collect the adapter behavior groups for native unittest and existing CI callers."""

import unittest

from adapter_metadata_tests import AdapterMetadataTests
from adapter_archive_tests import AdapterArchiveTests
from adapter_resources_tests import AdapterResourcesTests
from adapter_install_tests import AdapterInstallTests
from adapter_portability_tests import AdapterPortabilityTests
from adapter_generation_tests import AdapterGenerationTests
from adapter_diagnostics_tests import AdapterDiagnosticsTests
from adapter_contract_tests import AdapterContractTests


if __name__ == "__main__":
    unittest.main()
