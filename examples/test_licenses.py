#!/usr/bin/env python3
"""
LicenseChain Python SDK - License Testing Script

Provide license keys via LICENSECHAIN_TEST_KEYS (comma-separated).
Never commit real license keys.
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from licensechain.client import LicenseChainClient
from licensechain.exceptions import (
    AuthenticationError,
    ValidationError,
    NetworkError,
    LicenseChainException,
)


def load_test_licenses() -> List[str]:
    raw = os.getenv("LICENSECHAIN_TEST_KEYS", "").strip()
    if not raw:
        return []
    return [k.strip() for k in raw.split(",") if k.strip()]


async def test_license_validation(client: LicenseChainClient, license_key: str) -> Dict[str, Any]:
    result = {
        "license_key": license_key,
        "valid": False,
        "status": None,
        "error": None,
        "response_time": None,
        "details": None,
    }

    try:
        start_time = datetime.now()
        response = await client.validate_license(license_key=license_key)
        elapsed = (datetime.now() - start_time).total_seconds()

        result["response_time"] = elapsed
        result["valid"] = response.get("valid", False)
        result["status"] = response.get("status", "UNKNOWN")
        result["details"] = {
            "expiresAt": response.get("expiresAt"),
            "email": response.get("email"),
            "metadata": response.get("metadata"),
        }

    except ValidationError as e:
        result["error"] = f"ValidationError: {str(e)}"
    except AuthenticationError as e:
        result["error"] = f"AuthenticationError: {str(e)}"
    except NetworkError as e:
        result["error"] = f"NetworkError: {str(e)}"
    except LicenseChainException as e:
        result["error"] = f"LicenseChainException: {str(e)}"
    except Exception as e:
        result["error"] = f"Unexpected error: {type(e).__name__}: {str(e)}"

    return result


async def test_all_licenses(client: LicenseChainClient, licenses: List[str]) -> List[Dict[str, Any]]:
    print("Testing license validation...\n")

    results = []
    for i, license_key in enumerate(licenses, 1):
        print(f"[{i}/{len(licenses)}] Testing: {license_key}")
        result = await test_license_validation(client, license_key)
        results.append(result)

        if result["error"]:
            print(f"   Error: {result['error']}")
        elif result["valid"]:
            print(f"   Valid - Status: {result['status']}")
        else:
            print(f"   Invalid - Status: {result['status']}")
        if result["response_time"] is not None:
            print(f"   Response time: {result['response_time']:.3f}s\n")

    return results


async def print_summary(results: List[Dict[str, Any]]):
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)

    valid_count = sum(1 for r in results if r["valid"])
    invalid_count = sum(1 for r in results if not r["valid"] and not r["error"])
    error_count = sum(1 for r in results if r["error"])

    print(f"Total Licenses Tested: {len(results)}")
    print(f"Valid: {valid_count}")
    print(f"Invalid: {invalid_count}")
    print(f"Errors: {error_count}")


async def main():
    print("=" * 60)
    print("LicenseChain Python SDK - License Testing")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    api_key = os.getenv("LICENSECHAIN_API_KEY")
    if not api_key:
        print("ERROR: LICENSECHAIN_API_KEY environment variable not set")
        print("  export LICENSECHAIN_API_KEY='your-api-key'")
        print("  export LICENSECHAIN_TEST_KEYS='LC-XXXXXX-XXXXXX-XXXXXX'")
        print("  python examples/test_licenses.py")
        return False

    licenses = load_test_licenses()
    if not licenses:
        print("ERROR: LICENSECHAIN_TEST_KEYS not set (comma-separated license keys)")
        print("  export LICENSECHAIN_TEST_KEYS='LC-XXXXXX-XXXXXX-XXXXXX'")
        return False

    client = LicenseChainClient(
        api_key=api_key,
        base_url="https://api.licensechain.app/v1",
        timeout=30,
    )

    try:
        results = await test_all_licenses(client, licenses)
        await print_summary(results)
        return True
    except Exception as e:
        print(f"Test failed with error: {type(e).__name__}: {e}")
        return False
    finally:
        await client.close()


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
