from django.urls import path

from api.apps.authentication import views
from rest_framework_jwt.views import ObtainJSONWebToken

urlpatterns = [
    path("signup", views.CreateUserView.as_view(), name="create_user"),
    path("login", ObtainJSONWebToken.as_view(), name="login_user"),
]
