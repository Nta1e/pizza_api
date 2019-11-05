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

    def register_user(self):
        response = self.client.post(
            reverse("create_user"), self.user_data, format="json"
        )
        return response
