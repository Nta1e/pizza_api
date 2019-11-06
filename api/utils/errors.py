from collections import namedtuple

from rest_framework import status
from rest_framework.response import Response

from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    NotAuthenticated,
    APIException,
    PermissionDenied,
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
ORDER_2 = Error(
    status_code=404, message="There doesn't exist an order with this id!"
)
ORDER_3 = Error(
    status_code=400,
    message="You cannot update an order that you didn't place!",
)
ORDER_4 = Error(
    status_code=403,
    message="This functionality is restricted to only a super user",
)
ORDER_5 = Error(
    status_code=400, message="Cannot edit an order that is already dispatched!"
)
ORDER_6 = Error(
    status_code=400, message="You cannot delete an order you didn't place"
)
ORDER_7 = Error(
    status_code=400, message="You cannot view an order you didn't place"
)


def handle(error):
    error_response = {"Error": {"message": error.message}}
    if int(error.status_code) == 400:
        raise ValidationError(error_response)
    elif int(error.status_code) == 404:
        raise NotFound(error_response)
    elif int(error.status_code) == 401:
        raise NotAuthenticated(error_response)
    elif int(error.status_code) == 403:
        raise PermissionDenied(error_response)
    else:
        raise APIException(error_response)
