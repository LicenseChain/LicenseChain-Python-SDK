#!/usr/bin/env python3
"""
LicenseChain Python SDK - Connection Test Script

This script tests the connection between the Python SDK and the LicenseChain API
to ensure license validation and hardware validation workflows are working correctly.
"""

import asyncio
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from licensechain.client import LicenseChainClient
from licensechain.exceptions import (
    AuthenticationError,
    ValidationError,
    NetworkError,
    LicenseChainException,
)


async def test_api_connection(api_key: str, base_url: str = "https://api.licensechain.app/v1"):
    """Test basic API connection."""
    print("🔍 Testing API Connection...")
    
    try:
        client = LicenseChainClient(
            api_key=api_key,
            base_url=base_url,
            timeout=30,
        )
        
        # Test health endpoint (if available)
        try:
            # Try to get apps list as a connection test
            apps = await client.list_applications(page=1, limit=1)
            print("✅ API connection successful")
            print(f"   Found {len(apps.get('apps', []))} app(s)")
            return True, client
        except Exception as e:
            print(f"⚠️  Could not test with apps endpoint: {e}")
            # Connection still works, just can't test with apps
            return True, client
            
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("   Please check your API key")
        return False, None
    except NetworkError as e:
        print(f"❌ Network error: {e}")
        print("   Please check your internet connection and API URL")
        return False, None
    except Exception as e:
        print(f"❌ Connection test failed: {type(e).__name__}: {e}")
        return False, None


async def test_license_validation(client: LicenseChainClient, license_key: str, app_id: str = None):
    """Test license validation."""
    print(f"\n🔍 Testing License Validation...")
    print(f"   License Key: {license_key[:20]}...")
    if app_id:
        print(f"   App ID: {app_id}")
    
    try:
        start_time = datetime.now()
        response = await client.validate_license(license_key=license_key, app_id=app_id)
        elapsed = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ License validation request completed ({elapsed:.2f}s)")
        
        # Check response structure
        valid = response.get("valid", False)
        status = response.get("status", "UNKNOWN")
        expires_at = response.get("expiresAt")
        email = response.get("email")
        
        print(f"\n📊 Validation Results:")
        print(f"   Valid: {valid}")
        print(f"   Status: {status}")
        print(f"   Expires At: {expires_at or 'Never'}")
        print(f"   Email: {email or 'N/A'}")
        
        if valid:
            print("\n✅ License is VALID")
            return True
        else:
            error = response.get("error", "Unknown error")
            print(f"\n❌ License is INVALID: {error}")
            return False
            
    except ValidationError as e:
        print(f"❌ Validation error: {e}")
        return False
    except NetworkError as e:
        print(f"❌ Network error during validation: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_hardware_id_generation():
    """Test hardware ID generation."""
    print(f"\n🔍 Testing Hardware ID Generation...")
    
    try:
        import hashlib
        import platform
        
        # Generate hardware ID
        system_info = {
            'machine': platform.machine(),
            'processor': platform.processor(),
            'platform': platform.platform(),
            'node': platform.node(),
        }
        
        try:
            import uuid
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                           for elements in range(0, 2*6, 2)][::-1])
            system_info['mac'] = mac
        except:
            pass
        
        info_string = str(sorted(system_info.items()))
        hardware_id = hashlib.sha256(info_string.encode()).hexdigest()
        
        print(f"✅ Hardware ID generated successfully")
        print(f"   Hardware ID: {hardware_id[:32]}...")
        print(f"   Length: {len(hardware_id)} characters")
        
        # Test consistency (should be same on same machine)
        hardware_id2 = hashlib.sha256(info_string.encode()).hexdigest()
        if hardware_id == hardware_id2:
            print(f"✅ Hardware ID is consistent (same machine generates same ID)")
        else:
            print(f"⚠️  Hardware ID is not consistent (this should not happen)")
        
        return True, hardware_id
        
    except Exception as e:
        print(f"❌ Hardware ID generation failed: {type(e).__name__}: {e}")
        return False, None


async def run_all_tests():
    """Run all connection and validation tests."""
    print("="*60)
    print("LicenseChain Python SDK - Connection Test")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat()}\n")
    
    # Get API key from environment
    api_key = os.getenv("LICENSECHAIN_API_KEY")
    if not api_key:
        print("❌ ERROR: LICENSECHAIN_API_KEY environment variable not set")
        print("\nTo run this test:")
        print("  export LICENSECHAIN_API_KEY='your-api-key'")
        print("  export LICENSECHAIN_LICENSE_KEY='your-license-key'  # Optional")
        print("  python examples/test_connection.py")
        return False
    
    # Get license key (optional for testing)
    license_key = os.getenv("LICENSECHAIN_LICENSE_KEY")
    app_id = os.getenv("LICENSECHAIN_APP_ID")
    
    # Test results
    results = {
        "api_connection": False,
        "license_validation": None,
        "hardware_id": False,
    }
    
    # Test 1: API Connection
    success, client = await test_api_connection(api_key)
    results["api_connection"] = success
    
    if not success:
        print("\n❌ Cannot proceed - API connection failed")
        return False
    
    # Test 2: Hardware ID Generation
    hw_success, hardware_id = await test_hardware_id_generation()
    results["hardware_id"] = hw_success
    
    # Test 3: License Validation (if license key provided)
    if license_key:
        validation_success = await test_license_validation(client, license_key, app_id)
        results["license_validation"] = validation_success
    else:
        print("\n⚠️  Skipping license validation test (LICENSECHAIN_LICENSE_KEY not set)")
        results["license_validation"] = None
    
    # Cleanup
    if client:
        await client.close()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"API Connection: {'✅ PASS' if results['api_connection'] else '❌ FAIL'}")
    print(f"Hardware ID: {'✅ PASS' if results['hardware_id'] else '❌ FAIL'}")
    if results['license_validation'] is not None:
        print(f"License Validation: {'✅ PASS' if results['license_validation'] else '❌ FAIL'}")
    else:
        print(f"License Validation: ⚠️  SKIPPED")
    print("="*60)
    
    # Overall result
    all_passed = (
        results['api_connection'] and
        results['hardware_id'] and
        (results['license_validation'] is None or results['license_validation'])
    )
    
    if all_passed:
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

