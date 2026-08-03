# LicenseChain Python SDK Examples

This directory contains comprehensive examples demonstrating how to use the LicenseChain Python SDK.

## Examples

### Basic Examples

- **`basic_usage.py`** - Basic SDK usage and common operations
- **`basic_analytics.py`** - Basic analytics features available to all users
- **`licenses_comprehensive.py`** - Comprehensive license management examples

### Advanced Examples

- **`advanced_analytics.py`** - Advanced analytics features for Pro+ tier users
- **`products_example.py`** - Product management examples (Seller role only)
- **`teams_example.py`** - Team collaboration features (Pro+ tiers)

### Security Examples

- **`secure_integration.py`** - **IMPORTANT**: Secure integration example that prevents license bypassing
  - Demonstrates proper license validation on startup
  - Shows periodic re-validation
  - Implements hardware ID validation
  - Protects critical operations
  - Uses secure state management

### Testing

- **`test_connection.py`** - Test script to verify SDK-API connection and workflow

## Running Examples

### Prerequisites

1. Install the SDK:
   ```bash
   pip install licensechain-sdk
   ```

2. Set environment variables:
   ```bash
   export LICENSECHAIN_API_KEY='your-api-key'
   export LICENSECHAIN_LICENSE_KEY='your-license-key'  # For validation examples
   export LICENSECHAIN_APP_ID='your-app-id'  # Optional
   ```

### Running Examples

```bash
# Basic usage
python examples/basic_usage.py

# Secure integration (recommended for production)
python examples/secure_integration.py

# Test connection
python examples/test_connection.py

# Analytics
python examples/basic_analytics.py
python examples/advanced_analytics.py

# License management
python examples/licenses_comprehensive.py

# Product management (Seller only)
python examples/products_example.py

# Team collaboration (Pro+ tiers)
python examples/teams_example.py
```

## Secure Integration Best Practices

The `secure_integration.py` example demonstrates critical security practices:

1. **Always validate on startup** - Never assume a license is valid
2. **Periodic re-validation** - Re-validate licenses at regular intervals
3. **Hardware ID binding** - Prevent license sharing by binding to hardware
4. **Protect critical operations** - Validate before sensitive operations
5. **Use environment variables** - Never hardcode API keys or license keys
6. **Proper error handling** - Handle network errors gracefully
7. **Secure state management** - Use thread locks for concurrent access

## Testing Your Integration

Before deploying to production, use `test_connection.py` to verify:

- ✅ API connection is working
- ✅ License validation endpoint is accessible
- ✅ Hardware ID generation is consistent
- ✅ Response times are acceptable

```bash
python examples/test_connection.py
```

## Need Help?

- **Documentation**: https://docs.licensechain.app/sdks/python
- **Issues**: https://github.com/LicenseChain/LicenseChain-Python-SDK/issues
- **Email**: support@licensechain.app
