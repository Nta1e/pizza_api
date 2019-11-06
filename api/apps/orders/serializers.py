from rest_framework import serializers

from api.apps.orders.models import Order
from api.apps.authentication.serializers import UserSerializer
from api.utils import errors

PIZZA_SIZES = ["Small", "Medium", "Large", "Extra-large"]
ORDER_STATUSES = ["Pending", "In Transit", "Delivered"]


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
        """
        Ensure user cannot place and order with the same flavour and size twice
        :param validated_data:
        :return: None
        """
        flavour = validated_data["flavour"]
        size = validated_data["size"]
        order = Order.objects.filter(flavour=flavour, size=size)
        if order:
            errors.handle(errors.ORDER_1)

    class Meta:
        model = Order
        fields = ("id", "flavour", "size", "quantity", "status", "user")


class UpdateOrderSerializer(serializers.ModelSerializer):
    size = serializers.ChoiceField(PIZZA_SIZES)

    def update(self, instance, validated_data):
        if instance.status in ["Delivered", "In Transit"]:
            errors.handle(errors.ORDER_5)
        if instance.user != self.context["request"].user:
            errors.handle(errors.ORDER_3)
        return super(UpdateOrderSerializer, self).update(
            instance, validated_data
        )

    def to_representation(self, instance):
        """
        Add custom message to the returned response
        :param instance:
        :return: json response
        """
        representation = super(UpdateOrderSerializer, self).to_representation(
            instance
        )
        data = {
            "message": "Order successfully updated!",
            "details": {**representation},
        }
        return data

    class Meta:
        model = Order
        fields = ("id", "flavour", "size", "quantity", "status")


class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(ORDER_STATUSES)
    user = UserSerializer(read_only=True)

    def update(self, instance, validated_data):
        if not self.context[
            "request"
        ].user.is_superuser:  # limit status update to superusers
            errors.handle(errors.ORDER_4)
        return super(UpdateOrderStatusSerializer, self).update(
            instance, validated_data
        )

    def to_representation(self, instance):
        """
        Add custom message to the returned response
        :param instance:
        :return: json response
        """
        representation = super(
            UpdateOrderStatusSerializer, self
        ).to_representation(instance)
        data = {
            "message": "Order status successfully updated!",
            "order": {**representation},
        }
        return data

    class Meta:
        model = Order
        fields = ("id", "flavour", "size", "quantity", "status", "user")
        read_only_fields = ("flavour", "size", "quantity")


class OrdersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "flavour", "size", "quantity", "status", "user")
