from django.urls import reverse

from api.tests.base import BaseTestCase


class OrdersTestCase(BaseTestCase):
    def test_successful_order_placement(self):
        response = self.authorized_client().post(
            reverse("place_order"), self.order_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_cannot_order_same_flavour_and_size_twice(self):
        self.authorized_client().post(
            reverse("place_order"), self.order_data, format="json"
        )
        response = self.authorized_client().post(
            reverse("place_order"), self.order_data, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("more than once!", response.data["Error"]["message"])
