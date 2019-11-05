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
        data={"error": exc}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


Error = namedtuple("Error", ("status_code", "message"))

ORDER_1 = Error(
    status_code=400,
    message="You cannot order for the same pizza flavor and size more than once!",
)


def handle(error):
    error_response = {"Error": {"message": error.message}}
    if int(error.status_code) == 400:
        raise ValidationError(error_response)
    elif int(error.status_code) == 404:
        raise NotFound(error_response)
    elif int(error.status_code) == 401:
        raise NotAuthenticated(error_response)
    else:
        raise APIException(error_response)
