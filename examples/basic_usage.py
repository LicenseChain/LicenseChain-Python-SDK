#!/usr/bin/env python3
"""
LicenseChain Python SDK - Basic Usage Example

This example demonstrates how to use the LicenseChain Python SDK
for license management, user management, product management, and webhooks.
"""

import asyncio
import os
import sys
from typing import Any, Dict

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from licensechain.simple_client import Client
from licensechain.utils import (
    format_bytes,
    format_duration,
    generate_license_key,
    generate_uuid,
    validate_email,
    validate_license_key,
)
from licensechain.webhook_handler import WebhookEvents, WebhookHandler


def main():
    """Main example function."""
    print("🚀 LicenseChain Python SDK - Basic Usage Example\n")
    
    # Initialize the client
    client = Client(
        api_key='your-api-key-here',
        base_url='https://api.licensechain.app/v1',
        timeout=30,
        retries=3
    )
    
    try:
        # 1. License Management
        print("🔑 License Management:")
        
        # Create a license
        metadata = {
            'platform': 'python',
            'version': '1.0.0',
            'features': ['validation', 'webhooks']
        }
        
        license_obj = client.licenses.create('user123', 'product456', metadata)
        print(f"✅ License created: {license_obj.id}")
        print(f"   License Key: {license_obj.license_key}")
        print(f"   Status: {license_obj.status}")
        
        # Validate a license
        license_key = generate_license_key()
        print(f"\n🔍 Validating license key: {license_key}")
        
        is_valid = client.licenses.validate(license_key)
        if is_valid:
            print("✅ License is valid")
        else:
            print("❌ License is invalid")
        
        # Get license stats
        stats = client.licenses.stats()
        print(f"\n📊 License Statistics:")
        print(f"   Total: {stats.total}")
        print(f"   Active: {stats.active}")
        print(f"   Expired: {stats.expired}")
        print(f"   Revenue: ${stats.revenue}")
        
        # 2. User Management
        print("\n👤 User Management:")
        
        # Create a user
        user_metadata = {
            'source': 'python-sdk',
            'plan': 'premium'
        }
        
        user = client.users.create('user@example.com', 'John Doe', user_metadata)
        print(f"✅ User created: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Name: {user.name}")
        
        # Get user stats
        user_stats = client.users.stats()
        print(f"\n📊 User Statistics:")
        print(f"   Total: {user_stats.total}")
        print(f"   Active: {user_stats.active}")
        print(f"   Inactive: {user_stats.inactive}")
        
        # 3. Product Management
        print("\n📦 Product Management:")
        
        # Create a product
        product_metadata = {
            'category': 'software',
            'tags': ['premium', 'enterprise']
        }
        
        product = client.products.create(
            'My Software Product',
            'A great software product',
            99.99,
            'USD',
            product_metadata
        )
        print(f"✅ Product created: {product.id}")
        print(f"   Name: {product.name}")
        print(f"   Price: ${product.price} {product.currency}")
        
        # Get product stats
        product_stats = client.products.stats()
        print(f"\n📊 Product Statistics:")
        print(f"   Total: {product_stats.total}")
        print(f"   Active: {product_stats.active}")
        print(f"   Revenue: ${product_stats.revenue}")
        
        # 4. Webhook Management
        print("\n🔗 Webhook Management:")
        
        # Create a webhook
        events = [
            WebhookEvents.LICENSE_CREATED,
            WebhookEvents.LICENSE_UPDATED,
            WebhookEvents.USER_CREATED
        ]
        
        webhook = client.webhooks.create('https://example.com/webhook', events, 'webhook-secret')
        print(f"✅ Webhook created: {webhook.id}")
        print(f"   URL: {webhook.url}")
        print(f"   Events: {', '.join(webhook.events)}")
        
        # 5. Webhook Processing
        print("\n🔄 Webhook Processing:")
        
        webhook_handler = WebhookHandler('webhook-secret')
        
        # Simulate a webhook event
        webhook_event = {
            'id': 'evt_123',
            'type': WebhookEvents.LICENSE_CREATED,
            'data': {
                'id': 'lic_123',
                'user_id': 'user_123',
                'product_id': 'prod_123',
                'license_key': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ012345',
                'status': 'active',
                'created_at': '2023-01-01T00:00:00Z'
            },
            'timestamp': '2023-01-01T00:00:00Z',
            'signature': 'signature_here'
        }
        
        webhook_handler.process_event(webhook_event)
        print("✅ Webhook event processed successfully")
        
        # 6. Utility Functions
        print("\n🛠️ Utility Functions:")
        
        # Email validation
        email = 'test@example.com'
        print(f"Email '{email}' is valid: {validate_email(email)}")
        
        # License key validation
        license_key = generate_license_key()
        print(f"License key '{license_key}' is valid: {validate_license_key(license_key)}")
        
        # Generate UUID
        uuid = generate_uuid()
        print(f"Generated UUID: {uuid}")
        
        # Format bytes
        bytes_value = 1024 * 1024
        print(f"{bytes_value} bytes = {format_bytes(bytes_value)}")
        
        # Format duration
        seconds = 3661
        print(f"Duration: {format_duration(seconds)}")
        
        # 7. Error Handling
        print("\n🛡️ Error Handling:")
        
        try:
            client.licenses.get('invalid-id')
        except Exception as e:
            print(f"✅ Caught expected error: {type(e).__name__}: {e}")
        
        try:
            client.users.create('invalid-email', 'John Doe')
        except Exception as e:
            print(f"✅ Caught expected error: {type(e).__name__}: {e}")
        
        print("\n✅ Basic usage example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__} - {e}")
        if os.getenv('DEBUG'):
            import traceback
            traceback.print_exc()
    
    finally:
        # Cleanup
        client.close()
        print("\n🔌 Client closed")


if __name__ == '__main__':
    main()
