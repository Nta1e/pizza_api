from django.urls import reverse
from api.tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):
    def test_successful_registration(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 201)

    def test_unsuccessful_registration(self):
        self.user_data.pop("password")
        response = self.client.post(
            reverse("create_user"), self.user_data, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_successful_login(self):
        self.register_user()
        response = self.client.post(
            reverse("login_user"), self.login_data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.data)

    def test_unsuccessful_login(self):
        self.register_user()
        response = self.client.post(
            reverse("login_user"), self.wrong_credentials, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access_token", response.data)
