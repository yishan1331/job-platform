from ninja import Schema
from typing import Optional, Dict, Any
class ErrorResponse(Schema):
    """Unified error response format"""
    message: str
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None