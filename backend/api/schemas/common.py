from ninja import Schema
from typing import Optional, Dict, Any

class PaginatedResponse(Schema):
    count: int
    page: int
    page_size: int

class ErrorResponse(Schema):
    """Unified error response format"""
    message: str
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None