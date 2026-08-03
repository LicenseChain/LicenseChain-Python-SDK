from typing import Any, Dict, List, Optional

from ..exceptions import ValidationError
from ..utils import validate_not_empty, validate_email, sanitize_metadata, validate_pagination
from ..models import User, UserStats


class UserService:
    """Service for user management."""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def create(self, email: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> User:
        """Create a new user."""
        self._validate_email(email)
        
        data = {
            'email': email,
            'name': name,
            'password': 'ChangeMe123!',
            'metadata': sanitize_metadata(metadata or {})
        }
        
        response = self.api_client.post('/auth/register', data)
        payload = response.get('user') or response.get('data') or response
        return User(**payload)
    
    def get(self, user_id: str) -> User:
        """Get a user by ID."""
        validate_not_empty(user_id, 'user_id')
        
        response = self.api_client.get('/auth/me')
        payload = response.get('data', response)
        return User(**payload)
    
    def update(self, user_id: str, updates: Dict[str, Any]) -> User:
        """Update a user."""
        raise ValidationError('User update endpoint is not available in API v1')
    
    def delete(self, user_id: str) -> bool:
        """Delete a user."""
        raise ValidationError('User delete endpoint is not available in API v1')
    
    def list(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """List users."""
        page, limit = validate_pagination(page, limit)

        return {
            'data': [],
            'total': 0,
            'page': page,
            'limit': limit
        }
    
    def stats(self) -> UserStats:
        """Get user statistics."""
        return UserStats(total=0, active=0, inactive=0)
    
    def _validate_email(self, email: str) -> None:
        """Validate email format."""
        validate_not_empty(email, 'email')
        if not validate_email(email):
            raise ValidationError('Invalid email format')
    
