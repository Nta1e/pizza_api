from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.schemas import SchemaGenerator
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.views import APIView

from rest_framework_swagger import renderers

from api.apps.orders.serializers import (
    PlaceOrderSerializer,
    UpdateOrderSerializer,
    UpdateOrderStatusSerializer,
    OrdersSerializer,
)
from api.apps.orders.models import Order
from api.utils import errors
from api.apps.orders.pagination import StandardResultsPagination


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


class DeleteOrderView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        try:
            order = Order.objects.get(pk=order_id)
            if order.user != request.user:
                errors.handle(errors.ORDER_6)
            order.delete()
            response = {"message": "order successfully deleted!"}
            return Response(response)
        except Order.DoesNotExist:
            errors.handle(errors.ORDER_2)


class OrdersFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr="exact")
    first_name = filters.CharFilter(
        field_name="user__first_name", lookup_expr="exact"
    )
    last_name = filters.CharFilter(
        field_name="user__last_name", lookup_expr="exact"
    )


class OrdersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrdersSerializer
    pagination_class = StandardResultsPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = OrdersFilter
    search_fields = ("status", "user__first_name", "user__first_name")

    @action(
        methods=["GET"],
        detail=False,
        url_path="search",
        url_name="Search orders",
    )
    def search(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            errors.handle(errors.ORDER_4)
        return super().list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            errors.handle(errors.ORDER_4)
        return super(OrdersViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            errors.handle(errors.ORDER_4)
        return super(OrdersViewSet, self).retrieve(request, *args, **kwargs)

    def get_user_orders(self, request):
        queryset = Order.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def get_user_order(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
            if order.user != request.user:
                errors.handle(errors.ORDER_7)
            serializer = self.serializer_class(instance=order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            errors.handle(errors.ORDER_2)


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """

    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer,
        ]

        def get(self, request):
            generator = SchemaGenerator(
                title=title, url=url, patterns=patterns, urlconf=urlconf
            )
            schema = generator.get_schema(request=request, public=True)
            return Response(schema)

    return SwaggerSchemaView.as_view()
