from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.apps.orders import views


router = DefaultRouter()
router.register("orders", views.OrdersViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("order/", views.PlaceOrderView.as_view(), name="place_order"),
    path(
        "order/update/<int:order_id>/",
        views.UpdateOrderView.as_view(),
        name="update_order",
    ),
    path(
        "order/status/<int:order_id>/",
        views.UpdateOrderStatusView.as_view(),
        name="update_status",
    ),
    path(
        "order/delete/<int:order_id>/",
        views.DeleteOrderView.as_view(),
        name="delete_order",
    ),
    path(
        "user/orders/", views.OrdersViewSet.as_view({"get": "get_user_orders"})
    ),
    path(
        "user/order/<int:order_id>/",
        views.OrdersViewSet.as_view({"get": "get_user_order"}),
    ),
]
