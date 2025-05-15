from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from django.http import Http404
from typing import Union
from http import HTTPStatus
from .schemas.common import ErrorResponse

def handle_validation_error(error: ValidationError) -> tuple[int, ErrorResponse]:
    """Handle validation errors"""
    return HTTPStatus.UNPROCESSABLE_ENTITY, ErrorResponse(
        message=str(error),
        code="VALIDATION_ERROR",
        details=error.message_dict if hasattr(error, 'message_dict') else str(error)
    )

def handle_integrity_error(error: IntegrityError) -> tuple[int, ErrorResponse]:
    """Handle database integrity errors"""
    error_message = str(error)
    if "unique constraint" in error_message.lower():
        return HTTPStatus.CONFLICT, ErrorResponse(
            message=str(error),
            code="DUPLICATE_ENTRY"
        )
    return HTTPStatus.BAD_REQUEST, ErrorResponse(
        message=str(error),
        code="DATABASE_ERROR"
    )

def handle_not_found_error(error: Union[ObjectDoesNotExist, Http404]) -> tuple[int, ErrorResponse]:
    """Handle object not found errors"""
    return HTTPStatus.NOT_FOUND, ErrorResponse(
        message=str(error),
        code="NOT_FOUND"
    )

def handle_permission_error(error: PermissionDenied) -> tuple[int, ErrorResponse]:
    """Handle permission errors"""
    return HTTPStatus.FORBIDDEN, ErrorResponse(
        message=str(error),
        code="PERMISSION_DENIED"
    )

def handle_generic_error(error: Exception) -> tuple[int, ErrorResponse]:
    """Handle generic exceptions"""
    return HTTPStatus.INTERNAL_SERVER_ERROR, ErrorResponse(
        message=str(error),
        code="INTERNAL_ERROR"
    )

def get_error_handler(error: Exception) -> tuple[int, ErrorResponse]:
    """Return the appropriate error handler based on error type"""
    error_handlers = {
        ValidationError: handle_validation_error,
        IntegrityError: handle_integrity_error,
        ObjectDoesNotExist: handle_not_found_error,
        Http404: handle_not_found_error,
        PermissionDenied: handle_permission_error,
    }

    handler = error_handlers.get(type(error), handle_generic_error)
    return handler(error)