import logging

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    AuthenticationFailed,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Return friendly, consistent API error responses.
    """
    response = exception_handler(exc, context)

    if response is None:
        logger.exception("Unhandled exception", exc_info=exc)
        return Response(
            {
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "Something went wrong. Please try again later.",
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if isinstance(exc, ValidationError):
        response.data = {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": response.data,
            }
        }
        response.status_code = status.HTTP_400_BAD_REQUEST

    elif isinstance(exc, (Http404, NotFound)):
        response.data = {
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Requested resource was not found",
            }
        }
        response.status_code = status.HTTP_404_NOT_FOUND

    elif isinstance(exc, AuthenticationFailed):
        response.data = {
            "success": False,
            "error": {
                "code": "AUTHENTICATION_FAILED",
                "message": "Authentication credentials were invalid.",
            }
        }
        response.status_code = status.HTTP_401_UNAUTHORIZED

    elif isinstance(exc, PermissionDenied):
        response.data = {
            "success": False,
            "error": {
                "code": "PERMISSION_DENIED",
                "message": "You do not have permission to perform this action.",
            }
        }
        response.status_code = status.HTTP_403_FORBIDDEN

    else:
        response.data = {
            "success": False,
            "error": {
                "code": "REQUEST_ERROR",
                "message": response.data.get("detail", "Request failed"),
            }
        }

    return response
