# Secure Integration Guide

This guide explains how to properly integrate LicenseChain Python SDK into your application to prevent license bypassing and ensure secure validation.

## Overview

The `secure_integration.py` example demonstrates a production-ready implementation that:

1. **Validates licenses on startup** - Ensures the application cannot run without a valid license
2. **Implements periodic re-validation** - Regularly checks license validity to catch revocations
3. **Uses hardware ID validation** - Prevents license sharing between machines
4. **Protects critical operations** - Requires valid license before executing sensitive operations
5. **Manages state securely** - Uses thread locks to prevent race conditions
6. **Handles errors gracefully** - Proper error handling with fallback strategies

## Key Components

### SecureLicenseManager Class

The `SecureLicenseManager` class provides:

- **Automatic validation**: Validates license on initialization and periodically
- **Hardware ID generation**: Creates unique machine fingerprint
- **State management**: Thread-safe license state management
- **Error handling**: Graceful handling of network errors with cached results

### MyApplication Class

The `MyApplication` class demonstrates:

- **Startup validation**: Validates license before application starts
- **Operation protection**: Requires valid license for critical operations
- **Regular operations**: Validates license for regular operations (uses cache)

## Usage

### Basic Setup

```python
import os
from licensechain.client import LicenseChainClient

# Get credentials from environment (NEVER hardcode!)
api_key = os.getenv("LICENSECHAIN_API_KEY")
license_key = os.getenv("LICENSECHAIN_LICENSE_KEY")
app_id = os.getenv("LICENSECHAIN_APP_ID")  # Optional

# Initialize secure license manager
license_manager = SecureLicenseManager(
    api_key=api_key,
    license_key=license_key,
    app_id=app_id,
    validation_interval=300,  # Re-validate every 5 minutes
)

# Initialize application
app = MyApplication(license_manager)

# Start application (validates license)
await app.startup()
```

### Protecting Critical Operations

```python
async def critical_operation(self, data):
    # CRITICAL: Validate license before operation
    await self.license_manager.require_valid()
    
    # Perform the operation
    # ... your code here ...
```

### Regular Operations

```python
async def regular_operation(self, data):
    # Validate license (uses cache if recent)
    is_valid = await self.license_manager.ensure_valid()
    if not is_valid:
        return None  # Operation blocked
    
    # Perform the operation
    # ... your code here ...
```

## Security Best Practices

### 1. Environment Variables

**✅ DO:**
```python
api_key = os.getenv("LICENSECHAIN_API_KEY")
```

**❌ DON'T:**
```python
api_key = "hardcoded-key-here"  # NEVER do this!
```

### 2. Startup Validation

**✅ DO:**
```python
async def startup(self):
    is_valid = await self.license_manager.validate_license(force=True)
    if not is_valid:
        sys.exit(1)  # Exit if invalid
```

**❌ DON'T:**
```python
async def startup(self):
    # Don't skip validation!
    pass
```

### 3. Periodic Re-validation

**✅ DO:**
```python
await license_manager.start_periodic_validation()
```

**❌ DON'T:**
```python
# Don't validate only once
is_valid = await license_manager.validate_license()
# ... never validate again ...
```

### 4. Hardware ID Binding

**✅ DO:**
```python
# Hardware ID is automatically generated and validated
hardware_id = license_manager._hardware_id
```

**❌ DON'T:**
```python
# Don't allow license sharing
# Hardware ID validation prevents this automatically
```

### 5. Critical Operation Protection

**✅ DO:**
```python
async def critical_operation(self):
    await self.license_manager.require_valid()
    # ... operation code ...
```

**❌ DON'T:**
```python
async def critical_operation(self):
    # Don't skip validation!
    # ... operation code ...
```

## Testing

Use the `test_connection.py` script to verify your setup:

```bash
# Set environment variables
export LICENSECHAIN_API_KEY='your-api-key'
export LICENSECHAIN_LICENSE_KEY='your-license-key'
export LICENSECHAIN_APP_ID='your-app-id'  # Optional

# Run connection test
python examples/test_connection.py
```

## Workflow Verification

The secure integration ensures:

1. **License Validation Workflow**:
   - ✅ Validates license on startup
   - ✅ Re-validates periodically
   - ✅ Validates before critical operations
   - ✅ Handles network errors gracefully

2. **Hardware ID Validation**:
   - ✅ Generates unique hardware ID
   - ✅ Validates hardware ID matches license
   - ✅ Prevents license sharing

3. **API Connection**:
   - ✅ Connects to `https://api.licensechain.app/v1`
   - ✅ Uses correct endpoint: `POST /licenses/verify`
   - ✅ Sends correct payload: `{"key": "license-key"}`
   - ✅ Handles authentication errors
   - ✅ Handles network errors

## Response Format

The API returns:

```json
{
  "valid": true,
  "status": "ACTIVE",
  "expiresAt": "2025-12-31T23:59:59Z",
  "email": "user@example.com",
  "metadata": {
    "hardware_id": "abc123..."
  }
}
```

## Error Handling

The implementation handles:

- **AuthenticationError**: Invalid API key
- **ValidationError**: Invalid license key
- **NetworkError**: Connection issues (uses cached result if recent)
- **LicenseChainException**: Other SDK errors

## Next Steps

1. Review `examples/secure_integration.py` for complete implementation
2. Run `examples/test_connection.py` to verify your setup
3. Integrate `SecureLicenseManager` into your application
4. Protect critical operations with `require_valid()`
5. Set up periodic validation in your application lifecycle

## Support

For issues or questions:
- GitHub Issues: https://github.com/LicenseChain/LicenseChain-Python-SDK/issues
- Documentation: https://docs.licensechain.app/sdk/python
- Email: support@licensechain.app
