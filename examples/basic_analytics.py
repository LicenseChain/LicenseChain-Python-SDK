#!/usr/bin/env python3
"""
LicenseChain Python SDK - Basic Analytics Example

This example demonstrates how to use basic analytics features
available to all LicenseChain users.
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
    print("📊 LicenseChain Python SDK - Basic Analytics Example\n")
    
    # Initialize the client
    api_key = os.getenv('LICENSECHAIN_API_KEY', 'your-api-key-here')
    client = LicenseChainClient(
        api_key=api_key,
        base_url='https://api.licensechain.app/v1',
        timeout=30,
        retry_attempts=3,
    )
    
    try:
        # 1. Get Dashboard Insights (Basic Analytics)
        print("📈 Getting Dashboard Insights...")
        insights = await client.get_dashboard_insights()
        
        if insights.get('success'):
            metrics = insights.get('metrics', {})
            print("\n✅ Dashboard Metrics:")
            print(f"   Total Licenses: {metrics.get('totalLicenses', 0)}")
            print(f"   Licenses Change: {metrics.get('totalLicensesChangePct', 0):.1f}%")
            print(f"   Active Users: {metrics.get('activeUsers', 0)}")
            print(f"   Users Change: {metrics.get('activeUsersChangePct', 0):.1f}%")
            print(f"   Revenue: ${metrics.get('revenue', 0):.2f}")
            print(f"   Revenue Change: {metrics.get('revenueChangePct', 0):.1f}%")
            print(f"   API Calls: {metrics.get('apiCalls', 0)}")
            print(f"   API Calls Change: {metrics.get('apiCallsChangePct', 0):.1f}%")
            
            # Recent Activity
            activity = insights.get('recentActivity', [])
            if activity:
                print(f"\n📋 Recent Activity ({len(activity)} items):")
                for item in activity[:5]:  # Show first 5
                    print(f"   - {item.get('message', 'N/A')} ({item.get('timestamp', 'N/A')})")
        else:
            print(f"❌ Failed to get insights: {insights.get('error', 'Unknown error')}")
        
        # 2. Get General Analytics
        print("\n📊 Getting General Analytics...")
        analytics = await client.get_analytics()
        
        if analytics:
            print("✅ Analytics Data Retrieved:")
            print(f"   Data: {analytics}")
        
        # 3. Get Usage Statistics
        print("\n📈 Getting Usage Statistics...")
        usage_stats = await client.get_usage_stats(period="30d")
        
        if usage_stats:
            print("✅ Usage Statistics:")
            print(f"   Data: {usage_stats}")
        
        # 4. Get License Analytics
        print("\n🔑 Getting License Analytics...")
        # First, get a list of licenses
        licenses = await client.list_licenses(limit=5)
        
        if licenses and licenses.get('licenses'):
            license_id = licenses['licenses'][0].get('id')
            if license_id:
                license_analytics = await client.get_license_analytics(license_id)
                print(f"✅ License Analytics for {license_id}:")
                print(f"   Data: {license_analytics}")
        
        print("\n✅ Basic analytics example completed successfully!")
        
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
