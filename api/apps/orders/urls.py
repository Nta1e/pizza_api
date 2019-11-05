from django.urls import path

from api.apps.orders import views

urlpatterns = [
    path("order", views.PlaceOrderView.as_view(), name="place_order"),
    path(
        "order/<int:order_id>",
        views.UpdateOrderView.as_view(),
        name="update_order",
    ),
    path(
        "order/status/<int:order_id>",
        views.UpdateOrderStatusView.as_view(),
        name="update_status",
    ),
]
