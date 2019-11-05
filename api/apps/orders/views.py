from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from api.apps.orders.serializers import (
    PlaceOrderSerializer,
    UpdateOrderSerializer,
    UpdateOrderStatusSerializer,
)
from api.apps.orders.models import Order
from api.utils import errors


class PlaceOrderView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaceOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateOrderView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateOrderSerializer

    def update(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        try:
            instance = Order.objects.get(id=order_id)
            serializer = self.serializer_class(
                instance=instance,
                data=request.data,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            errors.handle(errors.ORDER_2)


class UpdateOrderStatusView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateOrderStatusSerializer

    def update(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        try:
            instance = Order.objects.get(id=order_id)
            serializer = self.serializer_class(
                instance=instance,
                data=request.data,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            errors.handle(errors.ORDER_2)
