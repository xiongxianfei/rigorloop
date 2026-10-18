#!/usr/bin/env python3
"""Release-boundary identity, authority and publication/recovery regression checks."""
import unittest
from release_identity_tests import TrustedReleaseTagIdentityTests
from release_execution_tests import ReleaseAuthorityTests, ReleaseExecutorTests
if __name__ == '__main__':
    unittest.main()
