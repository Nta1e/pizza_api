from django.urls import reverse

from rest_framework.test import APITestCase, APIClient


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
        self.client.post(reverse("create_user"), self.user_data, format="json")
        response = self.client.post(
            reverse("login_user"), self.login_data, format="json"
        )
        access_token = response.data["access_token"]
        client = self.client
        client.credentials(HTTP_AUTHORIZATION=access_token)
        return client
