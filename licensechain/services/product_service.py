from typing import Any, Dict, List, Optional

from ..exceptions import ValidationError
from ..utils import validate_not_empty, validate_positive, validate_currency, validate_pagination
from ..models import Product, ProductStats


class ProductService:
    """Service for product management."""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def create(self, name: str, description: Optional[str] = None, 
               price: Optional[float] = None, currency: str = 'USD', 
               metadata: Optional[Dict[str, Any]] = None) -> Product:
        """Create a new product."""
        self._validate_required_params(name, price, currency)
        raise ValidationError('Product endpoints are not available in API v1')
    
    def get(self, product_id: str) -> Product:
        """Get a product by ID."""
        raise ValidationError('Product endpoints are not available in API v1')
    
    def update(self, product_id: str, updates: Dict[str, Any]) -> Product:
        """Update a product."""
        raise ValidationError('Product endpoints are not available in API v1')
    
    def delete(self, product_id: str) -> bool:
        """Delete a product."""
        raise ValidationError('Product endpoints are not available in API v1')
    
    def list(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """List products."""
        page, limit = validate_pagination(page, limit)

        return {
            'data': [],
            'total': 0,
            'page': page,
            'limit': limit
        }
    
    def stats(self) -> ProductStats:
        """Get product statistics."""
        return ProductStats(total=0, active=0, revenue=0.0, licenses_count=0)
    
    def _validate_required_params(self, name: str, price: float, currency: str) -> None:
        """Validate required parameters."""
        validate_not_empty(name, 'name')
        validate_positive(price, 'price')
        if not validate_currency(currency):
            raise ValidationError('Invalid currency')
    
