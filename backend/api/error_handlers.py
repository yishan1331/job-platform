from http import HTTPStatus
from typing import Union

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist
from django.http import Http404

from .schemas.common import ErrorResponse


def handle_validation_error(error: ValidationError) -> tuple[int, ErrorResponse]:
    """Handle validation errors"""
    error_message = error.message if hasattr(error, "message") else str(error)
    return HTTPStatus.UNPROCESSABLE_ENTITY, ErrorResponse(
        message=error_message, code="VALIDATION_ERROR", details={"error": error_message}
    )


def handle_integrity_error(error: IntegrityError) -> tuple[int, ErrorResponse]:
    """Handle database integrity errors"""
    error_message = str(error)
    if "unique constraint" in error_message.lower():
        return HTTPStatus.CONFLICT, ErrorResponse(message=str(error), code="DUPLICATE_ENTRY")
    return HTTPStatus.BAD_REQUEST, ErrorResponse(message=str(error), code="DATABASE_ERROR")


def handle_not_found_error(error: Union[ObjectDoesNotExist, Http404]) -> tuple[int, ErrorResponse]:
    """Handle object not found errors"""
    return HTTPStatus.NOT_FOUND, ErrorResponse(message=str(error), code="NOT_FOUND")


def handle_permission_error(error: PermissionDenied) -> tuple[int, ErrorResponse]:
    """Handle permission errors"""
    return HTTPStatus.FORBIDDEN, ErrorResponse(message=str(error), code="PERMISSION_DENIED")


def handle_generic_error(error: Exception) -> tuple[int, ErrorResponse]:
    """Handle generic exceptions"""
    return HTTPStatus.INTERNAL_SERVER_ERROR, ErrorResponse(
        message=str(error), code="INTERNAL_ERROR"
    )


def get_error_handler(error: Exception) -> tuple[int, ErrorResponse]:
    """Return the appropriate error handler based on error type"""

    if isinstance(error, ValidationError):
        return handle_validation_error(error)
    if isinstance(error, IntegrityError):
        return handle_integrity_error(error)
    if isinstance(error, (ObjectDoesNotExist, Http404)):
        return handle_not_found_error(error)
    if isinstance(error, PermissionDenied):
        return handle_permission_error(error)

    return handle_generic_error(error)
