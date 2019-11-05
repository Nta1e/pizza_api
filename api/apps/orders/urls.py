from django.urls import path

from api.apps.orders import views

urlpatterns = [
    path("order", views.PlaceOrderView.as_view(), name="place_order")
]
