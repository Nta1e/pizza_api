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

    def test_successful_order_update(self):
        response = self.authorized_client().put(
            reverse(
                "update_order", kwargs={"order_id": self.create_order().id}
            ),
            {"flavour": "Vegetables", "size": "Large", "quantity": 2},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("updated!", response.data["message"])

    def test_unsuccessful_order_update(self):
        response = self.authorized_client().put(
            reverse("update_order", kwargs={"order_id": 3}),
            {"flavour": "Meat", "size": "Large", "quantity": 3},
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_update_order_status(self):
        response = self.superuser_client().put(
            reverse(
                "update_status", kwargs={"order_id": self.create_order().id}
            ),
            {"status": "Delivered"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("updated!", response.data["message"])

    def test_cannot_update_dispatched_order(self):
        order_id = self.create_order().id
        self.superuser_client().put(
            reverse("update_status", kwargs={"order_id": order_id}),
            {"status": "Delivered"},
        )
        response = self.authorized_client().put(
            reverse("update_order", kwargs={"order_id": order_id}),
            {"flavour": "Vegetables", "size": "Large", "quantity": 2},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("already dispatched!", response.data["Error"]["message"])

    def test_only_superuser_can_edit_order_status(self):
        response = self.authorized_client().put(
            reverse(
                "update_status", kwargs={"order_id": self.create_order().id}
            ),
            {"status": "Delivered"},
        )
        self.assertEqual(response.status_code, 403)
