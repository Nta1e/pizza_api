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

    def test_update_order_does_not_exist(self):
        response = self.superuser_client().put(
            reverse("update_status", kwargs={"order_id": 3}),
            {"status": "Delivered"},
        )
        self.assertEqual(response.status_code, 404)

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

    def test_successful_order_deletion(self):
        response = self.authorized_client().delete(
            reverse(
                "delete_order", kwargs={"order_id": self.create_order().id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted!", response.data["message"])

    def test_unsuccessful_order_deletion(self):
        response = self.authorized_client().delete(
            reverse("delete_order", kwargs={"order_id": 3})
        )
        self.assertEqual(response.status_code, 404)

    def test_get_all_orders(self):
        self.create_order()
        response = self.superuser_client().get("/api/orders/")
        self.assertEqual(response.status_code, 200)

    def test_normal_user_cannot_get_all_orders(self):
        response = self.authorized_client().get("/api/orders/")
        self.assertEqual(response.status_code, 403)

    def test_get_user_orders(self):
        self.create_order()
        response = self.authorized_client().get("/api/user/orders/")
        self.assertEqual(response.status_code, 200)

    def test_get_user_order(self):
        response = self.authorized_client().get(
            f"/api/user/order/{self.create_order().id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_user_order_does_not_exist(self):
        response = self.authorized_client().get(f"/api/user/order/4/")
        self.assertEqual(response.status_code, 404)

    def test_get_specific_order(self):
        response = self.superuser_client().get(
            f"/api/orders/{self.create_order().id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_only_admin_can_get_specific_order(self):
        response = self.authorized_client().get(
            f"/api/orders/{self.create_order().id}/"
        )
        self.assertEqual(response.status_code, 403)

    def test_search_orders(self):
        self.create_order()
        response = self.superuser_client().get(
            "/api/orders/search/?status=Pending"
        )
        self.assertEqual(response.status_code, 200)

    def test_only_admin_can_search_orders(self):
        self.create_order()
        response = self.authorized_client().get(
            "/api/orders/search/?status=Pending"
        )
        self.assertEqual(response.status_code, 403)

    def test_docs_are_rendered_successfully(self):
        response = self.superuser_client().get("/docs/")
        self.assertEqual(response.status_code, 200)
