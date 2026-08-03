#!/usr/bin/env python3
"""
LicenseChain Python SDK - Comprehensive Licenses Example

This example demonstrates all license management features including
creation, validation, updates, revocation, and analytics.
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from licensechain.client import LicenseChainClient


async def main():
    """Main example function."""
    print("🔑 LicenseChain Python SDK - Comprehensive Licenses Example\n")
    
    # Initialize the client
    api_key = os.getenv('LICENSECHAIN_API_KEY', 'your-api-key-here')
    client = LicenseChainClient(
        api_key=api_key,
        base_url='https://api.licensechain.app/v1',
        timeout=30,
        retry_attempts=3,
    )
    
    try:
        # 1. List Applications (needed for creating licenses)
        print("📱 Listing Applications...")
        apps_response = await client.list_applications(limit=10)
        
        apps = apps_response.get('apps', [])
        if not apps:
            print("⚠️  No applications found. Creating one...")
            app_response = await client.create_application(
                name="Example App",
                description="Example application for license management",
            )
            if app_response.get('id'):
                app_id = app_response['id']
                print(f"✅ Created application: {app_id}")
            else:
                print("❌ Failed to create application")
                return
        else:
            app_id = apps[0].get('id')
            print(f"✅ Using application: {apps[0].get('name', 'N/A')} (ID: {app_id})")
        
        # 2. Create a License
        print(f"\n➕ Creating a New License...")
        expires_at = (datetime.now() + timedelta(days=365)).isoformat()
        
        license_response = await client.create_license(
            app_id=app_id,
            user_email="user@example.com",
            user_name="John Doe",
            expires_at=expires_at,
            metadata={
                "plan": "premium",
                "features": ["api_access", "webhooks", "analytics"],
                "source": "python-sdk",
            },
        )
        
        if license_response.get('id') or license_response.get('license'):
            license_data = license_response.get('license', license_response)
            license_id = license_data.get('id')
            license_key = license_data.get('key') or license_data.get('licenseKey')
            
            print(f"✅ License Created:")
            print(f"   ID: {license_id}")
            print(f"   Key: {license_key}")
            print(f"   Status: {license_data.get('status', 'N/A')}")
            print(f"   Expires: {license_data.get('expiresAt', 'N/A')}")
        else:
            print(f"❌ Failed to create license: {license_response.get('error', 'Unknown error')}")
            return
        
        # 3. Validate License
        if license_key:
            print(f"\n🔍 Validating License Key...")
            validation = await client.validate_license(license_key, app_id=app_id)
            
            if validation.get('valid'):
                print(f"✅ License is Valid:")
                print(f"   Status: {validation.get('status', 'N/A')}")
                print(f"   Expires: {validation.get('expiresAt', 'N/A')}")
                if validation.get('email'):
                    print(f"   User: {validation.get('email', 'N/A')}")
            else:
                print(f"❌ License is Invalid: {validation.get('error', 'Unknown error')}")
        
        # 4. Get License Details
        if license_id:
            print(f"\n📋 Getting License Details...")
            license_details = await client.get_license(license_id)
            
            if license_details:
                print(f"✅ License Details:")
                print(f"   Key: {license_details.get('key', 'N/A')}")
                print(f"   Status: {license_details.get('status', 'N/A')}")
                print(f"   Created: {license_details.get('createdAt', 'N/A')}")
                print(f"   Expires: {license_details.get('expiresAt', 'N/A')}")
                if license_details.get('metadata'):
                    print(f"   Metadata: {license_details.get('metadata')}")
        
        # 5. List Licenses
        print(f"\n📋 Listing All Licenses...")
        licenses_response = await client.list_licenses(
            app_id=app_id,
            limit=10,
            status='active',
        )
        
        licenses = licenses_response.get('licenses', licenses_response.get('data', []))
        print(f"✅ Found {len(licenses)} licenses")
        for lic in licenses[:5]:  # Show first 5
            print(f"   - {lic.get('key', 'N/A')[:20]}... - {lic.get('status', 'N/A')}")
        
        # 6. Update License
        if license_id:
            print(f"\n✏️  Updating License...")
            new_expires = (datetime.now() + timedelta(days=730)).isoformat()
            
            updated_license = await client.update_license(
                license_id=license_id,
                attributes={
                    "expiresAt": new_expires,
                    "metadata": {
                        "plan": "enterprise",
                        "updated_by": "python-sdk",
                    },
                },
            )
            
            if updated_license:
                print(f"✅ License Updated:")
                print(f"   New Expires: {updated_license.get('expiresAt', 'N/A')}")
        
        # 7. Extend License
        if license_id:
            print(f"\n📅 Extending License...")
            extended_date = (datetime.now() + timedelta(days=1095)).isoformat()
            
            extended_license = await client.extend_license(
                license_id=license_id,
                new_expires_at=extended_date,
            )
            
            if extended_license:
                print(f"✅ License Extended:")
                print(f"   New Expires: {extended_license.get('expiresAt', 'N/A')}")
        
        # 8. Get License Analytics
        if license_id:
            print(f"\n📊 Getting License Analytics...")
            analytics = await client.get_license_analytics(license_id)
            
            if analytics:
                print(f"✅ License Analytics:")
                print(f"   Data: {analytics}")
        
        # 9. Activate License (if suspended)
        if license_id:
            print(f"\n✅ Activating License...")
            try:
                activated = await client.activate_license(license_id)
                if activated:
                    print(f"✅ License Activated")
            except Exception as e:
                print(f"⚠️  Activation: {type(e).__name__} - {e}")
        
        # 10. Revoke License (optional - uncomment to test)
        # if license_id:
        #     print(f"\n🚫 Revoking License...")
        #     revoked = await client.revoke_license(
        #         license_id=license_id,
        #         reason="Testing revocation via Python SDK",
        #     )
        #     if revoked:
        #         print(f"✅ License Revoked")
        
        # 11. Delete License (optional - uncomment to test)
        # if license_id:
        #     print(f"\n🗑️  Deleting License...")
        #     deleted = await client.delete_license(license_id)
        #     if deleted:
        #         print(f"✅ License Deleted")
        
        print("\n✅ Comprehensive licenses example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__} - {e}")
        if os.getenv('DEBUG'):
            import traceback
            traceback.print_exc()
    
    finally:
        # Cleanup
        await client.close()
        print("\n🔌 Client closed")


if __name__ == '__main__':
    asyncio.run(main())
