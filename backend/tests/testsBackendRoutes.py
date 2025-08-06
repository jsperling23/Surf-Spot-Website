import unittest
from app import app
import json


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        app.testing = True

    def tearDown(self):
        self.app_context.pop()

    def test_health(self):
        response = self.client.get('/health')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'Active')


if __name__ == "__main__":
    unittest.main()