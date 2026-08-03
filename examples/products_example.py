#!/usr/bin/env python3
"""
LicenseChain Python SDK - Products Example

This example demonstrates how to manage products (Seller/Admin only).
Products allow you to sell licenses with predefined pricing.
"""

import asyncio
import os
import sys

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from licensechain.client import LicenseChainClient


async def main():
    """Main example function."""
    print("📦 LicenseChain Python SDK - Products Example\n")
    
    # Initialize the client
    api_key = os.getenv('LICENSECHAIN_API_KEY', 'your-api-key-here')
    client = LicenseChainClient(
        api_key=api_key,
        base_url='https://api.licensechain.app/v1',
        timeout=30,
        retry_attempts=3,
    )
    
    try:
        # 1. List Products
        print("📋 Listing Products...")
        products_response = await client.list_products(limit=10, offset=0)
        
        if products_response.get('success'):
            products = products_response.get('products', [])
            stats = products_response.get('stats', {})
            
            print(f"\n✅ Found {len(products)} products")
            print(f"\n📊 Product Statistics:")
            print(f"   Total Products: {stats.get('total', 0)}")
            print(f"   Active Products: {stats.get('active', 0)}")
            print(f"   Total Licenses: {stats.get('totalLicenses', 0)}")
            print(f"   Total Revenue: ${stats.get('totalRevenue', 0):.2f}")
            
            print(f"\n📦 Products:")
            for product in products:
                print(f"   - {product.get('name', 'N/A')}")
                print(f"     ID: {product.get('id', 'N/A')}")
                print(f"     Price: ${product.get('price', 0):.2f} {product.get('currency', 'USD')}")
                print(f"     Active: {product.get('active', False)}")
                print(f"     Licenses: {product.get('licensesCount', 0)}")
                if product.get('description'):
                    print(f"     Description: {product.get('description', '')[:50]}...")
                print()
        else:
            print(f"❌ Failed to list products: {products_response.get('error', 'Unknown error')}")
        
        # 2. Create a Product
        print("➕ Creating a New Product...")
        try:
            new_product = await client.create_product(
                name="Premium License",
                price=99.99,
                description="Premium license with all features included",
                currency="USD",
                active=True,
            )
            
            if new_product.get('success'):
                product = new_product.get('product', {})
                print(f"✅ Product Created:")
                print(f"   ID: {product.get('id', 'N/A')}")
                print(f"   Name: {product.get('name', 'N/A')}")
                print(f"   Price: ${product.get('price', 0):.2f} {product.get('currency', 'USD')}")
                print(f"   Active: {product.get('active', False)}")
                
                product_id = product.get('id')
                
                # 3. Update the Product
                if product_id:
                    print(f"\n✏️  Updating Product {product_id}...")
                    updated_product = await client.update_product(
                        product_id=product_id,
                        price=149.99,
                        description="Updated: Premium license with extended features",
                    )
                    
                    if updated_product.get('success'):
                        product = updated_product.get('product', {})
                        print(f"✅ Product Updated:")
                        print(f"   New Price: ${product.get('price', 0):.2f}")
                        print(f"   Description: {product.get('description', 'N/A')}")
                    
                    # 4. Get Product Analytics
                    print(f"\n📊 Getting Product Analytics...")
                    analytics = await client.get_product_analytics(product_id=product_id)
                    
                    if analytics:
                        print(f"✅ Product Analytics:")
                        print(f"   Data: {analytics}")
                    
                    # 5. Delete the Product (if no licenses)
                    # Note: Products with licenses cannot be deleted
                    print(f"\n🗑️  Attempting to Delete Product {product_id}...")
                    try:
                        delete_response = await client.delete_product(product_id)
                        if delete_response.get('success'):
                            print(f"✅ Product Deleted Successfully")
                        else:
                            print(f"⚠️  Cannot delete product: {delete_response.get('error', 'Unknown error')}")
                    except Exception as e:
                        print(f"⚠️  Cannot delete product (may have licenses): {type(e).__name__}")
            else:
                print(f"❌ Failed to create product: {new_product.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"⚠️  Product operations require Seller or Admin role: {type(e).__name__} - {e}")
        
        # 6. Search Products
        print("\n🔍 Searching Products...")
        search_response = await client.list_products(search="Premium", limit=5)
        
        if search_response.get('success'):
            products = search_response.get('products', [])
            print(f"✅ Found {len(products)} products matching 'Premium'")
            for product in products:
                print(f"   - {product.get('name', 'N/A')}")
        
        # 7. Filter Active Products
        print("\n✅ Filtering Active Products...")
        active_response = await client.list_products(active=True, limit=10)
        
        if active_response.get('success'):
            products = active_response.get('products', [])
            print(f"✅ Found {len(products)} active products")
        
        print("\n✅ Products example completed successfully!")
        
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
