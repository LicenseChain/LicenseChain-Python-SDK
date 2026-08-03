from typing import Any, Dict, List, Optional

from ..exceptions import ValidationError
from ..utils import validate_not_empty, sanitize_metadata
from ..models import Webhook


class WebhookService:
    """Service for webhook management."""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def create(self, url: str, events: List[str], secret: Optional[str] = None) -> Webhook:
        """Create a new webhook."""
        self._validate_webhook_params(url, events)
        
        data = {
            'url': url,
            'events': events,
            'secret': secret
        }
        
        response = self.api_client.post('/webhooks', data)
        payload = response.get('data', response)
        payload = self._normalize_webhook_payload(payload)
        return Webhook(**payload)
    
    def get(self, webhook_id: str) -> Webhook:
        """Get a webhook by ID."""
        validate_not_empty(webhook_id, 'webhook_id')
        
        response = self.api_client.get(f'/webhooks/{webhook_id}')
        payload = response.get('data', response)
        payload = self._normalize_webhook_payload(payload)
        return Webhook(**payload)
    
    def update(self, webhook_id: str, updates: Dict[str, Any]) -> Webhook:
        """Update a webhook."""
        validate_not_empty(webhook_id, 'webhook_id')
        
        response = self.api_client.put(f'/webhooks/{webhook_id}', sanitize_metadata(updates))
        payload = response.get('data', response)
        payload = self._normalize_webhook_payload(payload)
        return Webhook(**payload)
    
    def delete(self, webhook_id: str) -> bool:
        """Delete a webhook."""
        validate_not_empty(webhook_id, 'webhook_id')
        
        self.api_client.delete(f'/webhooks/{webhook_id}')
        return True
    
    def list(self) -> List[Webhook]:
        """List webhooks."""
        response = self.api_client.get('/webhooks')
        items = response.get('data', [])
        return [Webhook(**self._normalize_webhook_payload(webhook)) for webhook in items]
    
    def _validate_webhook_params(self, url: str, events: List[str]) -> None:
        """Validate webhook parameters."""
        validate_not_empty(url, 'url')
        if not isinstance(events, list):
            raise ValidationError('Events must be a list')
        if not events:
            raise ValidationError('Events cannot be empty')
    
    def _normalize_webhook_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': payload.get('id'),
            'app_id': payload.get('app_id') or '',
            'url': payload.get('url', ''),
            'events': payload.get('events') or [],
            'secret': payload.get('secret'),
            'status': 'active' if payload.get('active', True) else 'inactive',
            'created_at': payload.get('created_at') or payload.get('createdAt'),
            'updated_at': payload.get('updated_at') or payload.get('updatedAt'),
            'last_triggered_at': payload.get('last_triggered_at'),
            'failure_count': payload.get('failure_count', 0),
        }
