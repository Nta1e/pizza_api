from collections import namedtuple

from rest_framework import status
from rest_framework.response import Response

from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    NotAuthenticated,
    APIException,
)
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        response.data["status_code"] = response.status_code
        return response
    return Response(
        data={"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


Error = namedtuple("Error", ("status_code", "message"))

AUTH_01 = Error(status_code=400, message="User with this email already exists")
AUTH_02 = Error(status_code=400, message="Invalid email")


def handle(error):
    error_response = {
        "Error": {"status_code": error.status_code, "message": error.message}
    }
    if error.status_code == 400:
        raise ValidationError(error_response)
    elif error.status_code == 404:
        raise NotFound(error_response)
    elif error.status_code == 401:
        raise NotAuthenticated(error_response)
    else:
        raise APIException(error_response)
