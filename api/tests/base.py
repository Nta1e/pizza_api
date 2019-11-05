from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

from api.apps.authentication.models import User
from api.apps.orders.models import Order


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "first_name": "Ntale",
            "last_name": "Shadik",
            "email": "shadikntale@gmail.com",
            "phone_number": 702260027,
            "address_line_1": "Bahai Road",
            "address_line_2": "Lutaaya Road",
            "password": "password123",
        }
        self.login_data = {
            "email": "shadikntale@gmail.com",
            "password": "password123",
        }
        self.wrong_credentials = {
            "email": "shadikntale@gmail.com",
            "password": "password",
        }
        self.order_data = {"flavour": "Meat", "size": "Small", "quantity": 2}

    def register_user(self):
        response = self.client.post(
            reverse("create_user"), self.user_data, format="json"
        )
        return response

    def authorized_client(self):
        self.register_user()
        response = self.client.post(
            reverse("login_user"), self.login_data, format="json"
        )
        access_token = response.data["access_token"]
        client = self.client
        client.credentials(HTTP_AUTHORIZATION=access_token)
        return client

    def superuser_client(self):
        User.objects.create_superuser(
            email="shadik@ntale.com", password="superuser"
        )
        credentials = {"email": "shadik@ntale.com", "password": "superuser"}
        response = self.client.post(
            reverse("login_user"), credentials, format="json"
        )
        access_token = response.data["access_token"]
        client = self.client
        client.credentials(HTTP_AUTHORIZATION=access_token)
        return client

    def create_order(self):
        self.register_user()
        user = User.objects.get(email="shadikntale@gmail.com")
        order = Order.objects.create(
            flavour="meat", size="Extra-large", quantity=2, user=user
        )
        return order
