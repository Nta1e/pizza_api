from rest_framework import serializers

from api.apps.authentication.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_data = User.objects.create_user(**validated_data)
        return user_data

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "password",
        )
