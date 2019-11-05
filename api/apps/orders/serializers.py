from rest_framework import serializers

from api.apps.orders.models import Order
from api.apps.authentication.serializers import UserSerializer
from api.utils import errors

PIZZA_SIZES = ["Small", "Medium", "Large", "Extra-large"]


class PlaceOrderSerializer(serializers.ModelSerializer):
    size = serializers.ChoiceField(PIZZA_SIZES)
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        self.ensure_orders_integrity(validated_data)
        order = Order(**validated_data)
        order.user = self.context["request"].user
        order.save()
        return order

    def ensure_orders_integrity(self, validated_data):
        flavour = validated_data["flavour"]
        size = validated_data["size"]
        order = Order.objects.filter(flavour=flavour, size=size)
        if order:
            errors.handle(errors.ORDER_1)

    class Meta:
        model = Order
        fields = ("flavour", "size", "quantity", "user")
