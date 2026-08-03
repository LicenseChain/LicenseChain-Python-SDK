import re
import unittest

from licensechain.client import LicenseChainClient


class HwuidHashSpecTest(unittest.TestCase):
    def test_default_hwuid_matches_hash_spec(self) -> None:
        client = LicenseChainClient(api_key="test-key")
        h1 = client._default_hwuid()
        h2 = client._default_hwuid()

        self.assertEqual(h1, h2)
        self.assertIsNotNone(re.fullmatch(r"[a-f0-9]{64}", h1))


if __name__ == "__main__":
    unittest.main()
