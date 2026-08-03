#!/usr/bin/env python3
"""
LicenseChain Python SDK - Secure Integration Example

This example demonstrates how to properly integrate LicenseChain SDK into your
Python application to prevent license bypassing and ensure secure validation.

IMPORTANT SECURITY NOTES:
1. Always validate licenses on application startup
2. Validate licenses before critical operations
3. Use hardware ID validation to prevent license sharing
4. Implement periodic re-validation
5. Never store validation results in easily accessible locations
6. Use environment variables for API keys (never hardcode)
7. Implement proper error handling and logging
"""

import asyncio
import hashlib
import os
import platform
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from threading import Lock

# Add the parent directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from licensechain.client import LicenseChainClient
from licensechain.exceptions import (
    AuthenticationError,
    ValidationError,
    NetworkError,
    LicenseChainException,
)


class SecureLicenseManager:
    """
    Secure License Manager that prevents bypassing.
    
    This class implements:
    - License validation on startup
    - Periodic re-validation
    - Hardware ID validation
    - Critical operation protection
    - Secure state management
    """
    
    def __init__(
        self,
        api_key: str,
        license_key: str,
        app_id: Optional[str] = None,
        base_url: str = "https://api.licensechain.app/v1",
        validation_interval: int = 300,  # Re-validate every 5 minutes
    ):
        """
        Initialize the Secure License Manager.
        
        Args:
            api_key: Your LicenseChain API key (from environment variable)
            license_key: The license key to validate
            app_id: Optional application ID
            base_url: API base URL
            validation_interval: Seconds between re-validations
        """
        self.license_key = license_key
        self.app_id = app_id
        self.validation_interval = validation_interval
        self.last_validation: Optional[datetime] = None
        self.validation_result: Optional[Dict[str, Any]] = None
        self.is_valid: bool = False
        self._lock = Lock()
        self._hardware_id = self._generate_hardware_id()
        
        # Initialize the client
        self.client = LicenseChainClient(
            api_key=api_key,
            base_url=base_url,
            timeout=30,
            retry_attempts=3,
        )
        
        print(f"🔐 Secure License Manager initialized")
        print(f"   Hardware ID: {self._hardware_id[:16]}...")
    
    def _generate_hardware_id(self) -> str:
        """
        Generate a unique hardware ID based on system characteristics.
        
        This creates a fingerprint of the machine to prevent license sharing.
        """
        try:
            # Collect system information
            system_info = {
                'machine': platform.machine(),
                'processor': platform.processor(),
                'platform': platform.platform(),
                'node': platform.node(),
            }
            
            # Get MAC address (if available)
            try:
                import uuid
                mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                               for elements in range(0, 2*6, 2)][::-1])
                system_info['mac'] = mac
            except:
                pass
            
            # Create hash
            info_string = str(sorted(system_info.items()))
            return hashlib.sha256(info_string.encode()).hexdigest()
        except Exception as e:
            # Fallback to a simple hash
            return hashlib.sha256(str(platform.node()).encode()).hexdigest()
    
    async def validate_license(self, force: bool = False) -> bool:
        """
        Validate the license with the LicenseChain API.
        
        Args:
            force: Force validation even if recently validated
            
        Returns:
            True if license is valid, False otherwise
        """
        with self._lock:
            # Check if we need to re-validate
            if not force and self.last_validation:
                time_since_validation = (datetime.now() - self.last_validation).total_seconds()
                if time_since_validation < self.validation_interval:
                    # Return cached result if still valid
                    return self.is_valid
            
            try:
                print(f"🔍 Validating license: {self.license_key[:20]}...")
                
                # Validate license with LicenseChain API
                response = await self.client.validate_license(
                    license_key=self.license_key,
                    app_id=self.app_id
                )
                
                # Check response
                if not response.get("valid", False):
                    print(f"❌ License validation failed: {response.get('error', 'Unknown error')}")
                    self.is_valid = False
                    self.validation_result = response
                    self.last_validation = datetime.now()
                    return False
                
                # Additional checks
                status = response.get("status", "").upper()
                if status not in ["ACTIVE", "VALID"]:
                    print(f"❌ License status is not active: {status}")
                    self.is_valid = False
                    self.validation_result = response
                    self.last_validation = datetime.now()
                    return False
                
                # Check expiration
                expires_at = response.get("expiresAt")
                if expires_at:
                    try:
                        exp_date = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                        if exp_date < datetime.now(exp_date.tzinfo):
                            print(f"❌ License has expired: {expires_at}")
                            self.is_valid = False
                            self.validation_result = response
                            self.last_validation = datetime.now()
                            return False
                    except Exception as e:
                        print(f"⚠️  Could not parse expiration date: {e}")
                
                # Validate hardware ID if provided in metadata
                # Note: This requires the API to support hardware ID validation
                # For now, we'll store it in metadata for future validation
                metadata = response.get("metadata", {})
                stored_hw_id = metadata.get("hardware_id")
                
                if stored_hw_id and stored_hw_id != self._hardware_id:
                    print(f"❌ Hardware ID mismatch - License is bound to different machine")
                    self.is_valid = False
                    self.validation_result = response
                    self.last_validation = datetime.now()
                    return False
                
                # License is valid
                print(f"✅ License is valid!")
                print(f"   Status: {status}")
                print(f"   Expires: {expires_at or 'Never'}")
                print(f"   Email: {response.get('email', 'N/A')}")
                
                self.is_valid = True
                self.validation_result = response
                self.last_validation = datetime.now()
                
                # Store hardware ID in metadata (if API supports it)
                # This would be done via an API call to bind the hardware ID
                # For demonstration, we'll just log it
                if not stored_hw_id:
                    print(f"   ⚠️  Hardware ID not bound - consider binding for security")
                
                return True
                
            except AuthenticationError as e:
                print(f"❌ Authentication failed: {e}")
                self.is_valid = False
                return False
            except ValidationError as e:
                print(f"❌ Validation error: {e}")
                self.is_valid = False
                return False
            except NetworkError as e:
                print(f"⚠️  Network error: {e}")
                # On network error, use cached result if available and recent
                if self.is_valid and self.last_validation:
                    time_since = (datetime.now() - self.last_validation).total_seconds()
                    if time_since < 3600:  # Use cached result if less than 1 hour old
                        print(f"   Using cached validation result")
                        return True
                return False
            except LicenseChainException as e:
                print(f"❌ LicenseChain error: {e}")
                self.is_valid = False
                return False
            except Exception as e:
                print(f"❌ Unexpected error during validation: {e}")
                self.is_valid = False
                return False
    
    async def ensure_valid(self) -> bool:
        """
        Ensure license is valid, validate if needed.
        
        Returns:
            True if valid, False otherwise
        """
        return await self.validate_license(force=False)
    
    async def require_valid(self) -> None:
        """
        Require valid license or raise exception.
        
        Raises:
            ValidationError: If license is not valid
        """
        is_valid = await self.ensure_valid()
        if not is_valid:
            raise ValidationError("License is not valid. Please check your license key.")
    
    def get_license_info(self) -> Optional[Dict[str, Any]]:
        """
        Get current license information.
        
        Returns:
            License information dict or None
        """
        return self.validation_result
    
    async def start_periodic_validation(self):
        """
        Start periodic license validation in background.
        """
        async def _periodic_validate():
            while True:
                await asyncio.sleep(self.validation_interval)
                print(f"🔄 Periodic license validation...")
                await self.validate_license(force=True)
        
        # Start background task
        asyncio.create_task(_periodic_validate())
        print(f"✅ Periodic validation started (interval: {self.validation_interval}s)")
    
    async def close(self):
        """Close the client connection."""
        await self.client.close()


# Example application class that uses secure license validation
class MyApplication:
    """
    Example application that uses secure license validation.
    
    This demonstrates how to protect critical operations with license validation.
    """
    
    def __init__(self, license_manager: SecureLicenseManager):
        self.license_manager = license_manager
        self.startup_time = datetime.now()
    
    async def startup(self):
        """Application startup - validate license first."""
        print("\n" + "="*60)
        print("🚀 Application Starting...")
        print("="*60)
        
        # CRITICAL: Validate license on startup
        is_valid = await self.license_manager.validate_license(force=True)
        if not is_valid:
            print("\n❌ Application cannot start - Invalid license")
            print("   Please check your license key and ensure it's valid.")
            sys.exit(1)
        
        print("✅ License validated - Application started successfully")
        print("="*60 + "\n")
    
    async def critical_operation(self, data: Any):
        """
        Example critical operation that requires license validation.
        
        This demonstrates how to protect critical operations.
        """
        # CRITICAL: Validate license before critical operation
        await self.license_manager.require_valid()
        
        # Perform the operation
        print(f"🔒 Executing critical operation with data: {data}")
        # ... your operation code here ...
        print("✅ Critical operation completed")
    
    async def regular_operation(self, data: Any):
        """
        Example regular operation - still validates but doesn't fail if cached.
        """
        # Validate license (uses cache if recent)
        is_valid = await self.license_manager.ensure_valid()
        if not is_valid:
            print("⚠️  License validation failed - Operation may be limited")
            return None
        
        # Perform the operation
        print(f"📝 Executing regular operation with data: {data}")
        # ... your operation code here ...
        print("✅ Regular operation completed")
        return True
    
    async def get_license_status(self) -> Dict[str, Any]:
        """Get current license status."""
        info = self.license_manager.get_license_info()
        if info:
            return {
                "valid": self.license_manager.is_valid,
                "status": info.get("status"),
                "expires_at": info.get("expiresAt"),
                "email": info.get("email"),
                "last_validation": self.license_manager.last_validation.isoformat() if self.license_manager.last_validation else None,
            }
        return {"valid": False, "error": "No license information available"}


async def main():
    """
    Main example function demonstrating secure integration.
    """
    print("\n" + "="*60)
    print("LicenseChain Python SDK - Secure Integration Example")
    print("="*60 + "\n")
    
    # IMPORTANT: Get API key from environment variable (never hardcode!)
    api_key = os.getenv("LICENSECHAIN_API_KEY")
    if not api_key:
        print("❌ ERROR: LICENSECHAIN_API_KEY environment variable not set")
        print("   Set it with: export LICENSECHAIN_API_KEY='your-api-key'")
        sys.exit(1)
    
    # Get license key (in production, get this from user input, config file, etc.)
    license_key = os.getenv("LICENSECHAIN_LICENSE_KEY", "YOUR-LICENSE-KEY-HERE")
    if license_key == "YOUR-LICENSE-KEY-HERE":
        print("⚠️  WARNING: Using placeholder license key")
        print("   Set LICENSECHAIN_LICENSE_KEY environment variable or update the code")
    
    # Optional: Get app ID
    app_id = os.getenv("LICENSECHAIN_APP_ID")
    
    # Initialize secure license manager
    license_manager = SecureLicenseManager(
        api_key=api_key,
        license_key=license_key,
        app_id=app_id,
        validation_interval=300,  # Re-validate every 5 minutes
    )
    
    try:
        # Initialize application
        app = MyApplication(license_manager)
        
        # Start application (validates license)
        await app.startup()
        
        # Start periodic validation
        await license_manager.start_periodic_validation()
        
        # Simulate application operations
        print("\n📋 Simulating application operations...\n")
        
        # Regular operation
        await app.regular_operation("data1")
        await asyncio.sleep(1)
        
        # Critical operation (requires valid license)
        try:
            await app.critical_operation("sensitive-data")
        except ValidationError as e:
            print(f"❌ Critical operation blocked: {e}")
        
        # Get license status
        status = await app.get_license_status()
        print(f"\n📊 License Status:")
        print(f"   Valid: {status.get('valid', False)}")
        print(f"   Status: {status.get('status', 'Unknown')}")
        print(f"   Expires: {status.get('expires_at', 'Never')}")
        print(f"   Email: {status.get('email', 'N/A')}")
        
        # Simulate running for a bit
        print("\n⏳ Application running (simulating 10 seconds)...")
        await asyncio.sleep(10)
        
        print("\n✅ Example completed successfully!")
        print("\n" + "="*60)
        print("SECURITY BEST PRACTICES IMPLEMENTED:")
        print("="*60)
        print("✅ License validation on startup")
        print("✅ Periodic re-validation")
        print("✅ Hardware ID generation and validation")
        print("✅ Critical operation protection")
        print("✅ Secure state management with locks")
        print("✅ Environment variables for sensitive data")
        print("✅ Proper error handling")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user")
    except Exception as e:
        print(f"\n❌ Application error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        await license_manager.close()
        print("🔌 License manager closed")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())

