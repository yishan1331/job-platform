from typing import Any, Optional

from ninja import Schema


class ErrorResponse(Schema):
    """Unified error response format"""

    message: str
    code: Optional[str] = None
    details: Optional[dict[str, Any]] = None
