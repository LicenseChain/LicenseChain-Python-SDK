from typing import Any, Dict, List, Optional
import hashlib
import platform
import socket

from ..exceptions import ValidationError
from ..utils import validate_uuid, validate_not_empty, sanitize_metadata, validate_pagination
from ..models import License, LicenseStats


class LicenseService:
    """Service for license management."""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def create(self, app_id: str, user_email: str, metadata: Optional[Dict[str, Any]] = None) -> License:
        """Create a new license."""
        validate_not_empty(app_id, 'app_id')
        validate_not_empty(user_email, 'user_email')
        
        data = {
            'appId': app_id,
            'plan': 'FREE',
            'issuedEmail': user_email,
            'metadata': sanitize_metadata(metadata or {})
        }
        
        response = self.api_client.post(f'/apps/{app_id}/licenses', data)
        payload = response.get('data', response)
        return License(**self._normalize_license_payload(payload))
    
    def get(self, license_id: str) -> License:
        """Get a license by ID."""
        validate_not_empty(license_id, 'license_id')
        
        response = self.api_client.get(f'/licenses/{license_id}')
        payload = response.get('data', response)
        return License(**self._normalize_license_payload(payload))
    
    def update(self, license_id: str, updates: Dict[str, Any]) -> License:
        """Update a license."""
        validate_not_empty(license_id, 'license_id')
        
        response = self.api_client.put(f'/licenses/{license_id}', sanitize_metadata(updates))
        payload = response.get('data', response)
        return License(**self._normalize_license_payload(payload))
    
    def revoke(self, license_id: str) -> bool:
        """Revoke a license."""
        validate_not_empty(license_id, 'license_id')
        
        self.api_client.delete(f'/licenses/{license_id}')
        return True
    
    def validate(self, license_key: str, hwuid: Optional[str] = None) -> bool:
        """Validate a license key. Optional hwuid for ecosystem HMAC/HWUID contract."""
        validate_not_empty(license_key, 'license_key')
        payload: Dict[str, Any] = {'key': license_key}
        if hwuid and hwuid.strip():
            payload['hwuid'] = hwuid.strip()
        else:
            raw = f"licensechain|python|{socket.gethostname()}|{platform.system()}|{platform.machine()}"
            payload['hwuid'] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        response = self.api_client.post('/licenses/verify', payload)
        return response.get('valid', False)

    def verify_with_details(self, license_key: str, hwuid: Optional[str] = None) -> Dict[str, Any]:
        """Full POST /licenses/verify response (optional license_token, license_jwks_uri)."""
        validate_not_empty(license_key, 'license_key')
        payload: Dict[str, Any] = {'key': license_key}
        if hwuid and hwuid.strip():
            payload['hwuid'] = hwuid.strip()
        else:
            raw = f"licensechain|python|{socket.gethostname()}|{platform.system()}|{platform.machine()}"
            payload['hwuid'] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return self.api_client.post('/licenses/verify', payload)
    
    def list_user_licenses(self, user_id: str, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """List licenses for a user."""
        validate_not_empty(user_id, 'user_id')
        page, limit = validate_pagination(page, limit)
        
        response = self.api_client.get('/licenses', {
            'page': page,
            'limit': limit
        })

        licenses = response.get('data') or response.get('licenses') or []
        filtered = [
            self._normalize_license_payload(license)
            for license in licenses
            if license.get('issuedEmail') == user_id
            or license.get('email') == user_id
            or license.get('user_id') == user_id
        ]
        
        return {
            'data': [License(**license) for license in filtered],
            'total': len(filtered),
            'page': page,
            'limit': limit
        }
    
    def stats(self) -> LicenseStats:
        """Get license statistics."""
        response = self.api_client.get('/licenses/stats')
        payload = response.get('data', response)
        return LicenseStats(**payload)
    
    def _validate_required_params(self, user_id: str, product_id: str) -> None:
        """Validate required parameters."""
        validate_not_empty(user_id, 'user_id')
        validate_not_empty(product_id, 'product_id')
    
    def _validate_uuid(self, id_value: str, field_name: str) -> None:
        """Validate UUID format."""
        validate_not_empty(id_value, field_name)
        if not validate_uuid(id_value):
            raise ValidationError(f"Invalid {field_name} format")

    def _normalize_license_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': payload.get('id'),
            'key': payload.get('key') or payload.get('licenseKey'),
            'app_id': payload.get('app_id') or payload.get('appId') or '',
            'user_id': payload.get('user_id'),
            'user_email': payload.get('user_email') or payload.get('issuedEmail') or payload.get('email') or '',
            'user_name': payload.get('user_name') or payload.get('issuedTo'),
            'status': str(payload.get('status', 'active')).lower(),
            'expires_at': payload.get('expires_at') or payload.get('expiresAt'),
            'created_at': payload.get('created_at') or payload.get('createdAt'),
            'updated_at': payload.get('updated_at') or payload.get('updatedAt'),
            'metadata': payload.get('metadata') or {},
            'features': payload.get('features') or [],
            'usage_count': payload.get('usage_count', 0),
        }
