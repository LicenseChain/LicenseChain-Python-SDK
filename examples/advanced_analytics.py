#!/usr/bin/env python3
"""
LicenseChain Python SDK - Advanced Analytics Example

This example demonstrates how to use advanced analytics features
available to Pro, Business, and Enterprise tier users.
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
    print("📊 LicenseChain Python SDK - Advanced Analytics Example\n")
    
    # Initialize the client
    api_key = os.getenv('LICENSECHAIN_API_KEY', 'your-api-key-here')
    client = LicenseChainClient(
        api_key=api_key,
        base_url='https://api.licensechain.app/v1',
        timeout=30,
        retry_attempts=3,
    )
    
    try:
        # 1. Get Advanced Dashboard Insights
        print("📈 Getting Advanced Dashboard Insights...")
        insights = await client.get_dashboard_insights()
        
        if insights.get('success'):
            # Check if advanced analytics are available
            analytics_type = insights.get('analyticsType', 'basic')
            print(f"   Analytics Type: {analytics_type}")
            
            if analytics_type == 'advanced':
                detailed = insights.get('detailed', {})
                print("\n✅ Advanced Analytics Available:")
                
                # License Analytics
                if 'licenses' in detailed:
                    licenses_data = detailed['licenses']
                    print(f"\n   📜 License Analytics:")
                    print(f"      Total: {licenses_data.get('total', 0)}")
                    print(f"      This Month: {licenses_data.get('thisMonth', 0)}")
                    print(f"      Last Month: {licenses_data.get('lastMonth', 0)}")
                    print(f"      Last 7 Days: {licenses_data.get('last7Days', 0)}")
                    
                    # By Status
                    if 'byStatus' in licenses_data:
                        print(f"      By Status:")
                        for status in licenses_data['byStatus']:
                            print(f"        - {status.get('status', 'N/A')}: {status.get('count', 0)}")
                
                # App Analytics
                if 'apps' in detailed:
                    apps_data = detailed['apps']
                    print(f"\n   📱 App Analytics:")
                    print(f"      Total: {apps_data.get('total', 0)}")
                    print(f"      This Month: {apps_data.get('thisMonth', 0)}")
                    print(f"      Last Month: {apps_data.get('lastMonth', 0)}")
                
                # API Usage Analytics
                if 'api' in detailed:
                    api_data = detailed['api']
                    print(f"\n   🔌 API Usage Analytics:")
                    print(f"      Total: {api_data.get('total', 0)}")
                    print(f"      This Month: {api_data.get('thisMonth', 0)}")
                    print(f"      Last Month: {api_data.get('lastMonth', 0)}")
                    print(f"      Last 7 Days: {api_data.get('last7Days', 0)}")
                    print(f"      Avg Response Time: {api_data.get('avgResponseTime', 0):.2f}ms")
                    
                    # By Endpoint
                    if 'byEndpoint' in api_data:
                        print(f"      By Endpoint:")
                        for endpoint in api_data['byEndpoint'][:5]:  # Show top 5
                            print(f"        - {endpoint.get('endpoint', 'N/A')}: {endpoint.get('count', 0)}")
                    
                    # By Status Code
                    if 'byStatus' in api_data:
                        print(f"      By Status Code:")
                        for status in api_data['byStatus']:
                            print(f"        - {status.get('statusCode', 'N/A')}: {status.get('count', 0)}")
                
                # Webhook Analytics
                if 'webhooks' in detailed:
                    webhooks_data = detailed['webhooks']
                    print(f"\n   🔗 Webhook Analytics:")
                    print(f"      Total: {webhooks_data.get('total', 0)}")
                    print(f"      This Month: {webhooks_data.get('thisMonth', 0)}")
                    
                    # By Status
                    if 'byStatus' in webhooks_data:
                        print(f"      By Status:")
                        for status in webhooks_data['byStatus']:
                            print(f"        - {status.get('status', 'N/A')}: {status.get('count', 0)}")
                
                # Daily Data Trends
                if 'dailyData' in detailed:
                    daily_data = detailed['dailyData']
                    print(f"\n   📅 Daily Data Trends (Last 30 days):")
                    for day in daily_data[-7:]:  # Show last 7 days
                        date = day.get('date', 'N/A')
                        licenses = day.get('licenses', 0)
                        revenue = day.get('revenue', 0)
                        print(f"      {date}: {licenses} licenses, ${revenue:.2f} revenue")
            else:
                print("\n⚠️  Advanced analytics require Pro, Business, or Enterprise tier")
                print("   Upgrade your plan to access advanced analytics features")
        
        # 2. Get Advanced Analytics with Date Range
        print("\n📊 Getting Advanced Analytics with Date Range...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        advanced_analytics = await client.get_advanced_analytics(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )
        
        if advanced_analytics:
            print("✅ Advanced Analytics Retrieved:")
            print(f"   Data: {advanced_analytics}")
        
        # 3. Get Analytics for Specific Metrics
        print("\n📈 Getting Analytics for Specific Metrics...")
        metrics = ['revenue', 'licenses', 'users', 'api_calls']
        
        for metric in metrics:
            try:
                metric_data = await client.get_advanced_analytics(metric=metric)
                print(f"   ✅ {metric}: {metric_data}")
            except Exception as e:
                print(f"   ⚠️  {metric}: {type(e).__name__} - {e}")
        
        print("\n✅ Advanced analytics example completed successfully!")
        
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
