import unittest
from unittest.mock import patch

from app import app


class _MockResponse:
    def __init__(self, text, json_data=None):
        self.text = text
        self._json_data = json_data if json_data is not None else text

    def json(self):
        return self._json_data


class App1FrontendTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch("app.requests.get")
    def test_items_proxy(self, mock_get):
        mock_get.return_value = _MockResponse("{}", {"demo": {"value": "ok"}})

        response = self.client.get("/items")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"demo": {"value": "ok"}})

    @patch("app.requests.post")
    def test_create_redirects_to_index(self, mock_post):
        response = self.client.post(
            "/create",
            data={"id": "1", "value": "test"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()