from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from api.apps.orders.serializers import PlaceOrderSerializer


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
