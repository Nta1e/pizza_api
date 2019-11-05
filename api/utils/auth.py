from rest_framework_jwt.utils import jwt_response_payload_handler

from api.apps.authentication.serializers import CreateUserSerializer


def custom_jwt_response_payload_handler(token, user=None, request=None):

    data = jwt_response_payload_handler(token, user, request)
    response_data = {
        "user": CreateUserSerializer(instance=user).data,
        "access_token": "Bearer " + data["token"],
        "expires_in": "24hrs",
    }
    return response_data
