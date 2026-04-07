import unittest

from app import ITEMS, app


class App2ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        ITEMS.clear()

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("env", payload)
        self.assertIn("timestamp", payload)

    def test_create_and_list_items(self):
        create_response = self.client.post(
            "/api/items",
            json={"id": "test-item", "value": "demo"},
        )
        self.assertEqual(create_response.status_code, 201)

        list_response = self.client.get("/api/items")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(
            list_response.get_json(),
            {"test-item": {"id": "test-item", "value": "demo"}},
        )


if __name__ == "__main__":
    unittest.main()