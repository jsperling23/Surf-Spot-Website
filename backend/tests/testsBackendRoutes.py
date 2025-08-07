import unittest
import json
import os

from app import app
from dbClass import Database, factory
from appConfig import AppConfig
from dotenv import load_dotenv


class RouteTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup flask unit testing client and context
        cls.app_context = app.app_context()
        cls.app_context.push()
        cls.client = app.test_client()
        app.testing = True

        # setup testing Database object
        load_dotenv()
        config = AppConfig(
            **{
                "db_user": os.getenv("DB_USER"),
                "db_password": os.getenv("DB_PASSWORD"),
                "db_name": os.getenv("DB_NAME"),
                "db_host": os.getenv("DB_HOST"),
                "secret_key": os.getenv("SECRET_KEY"),
            }
        )

        cls.db: Database | None = factory(
            user=config.db_user,
            password=config.db_password,
            db_name=config.db_name,
            logger=app.logger,
            testing=True,
            db_host=config.db_host
        )

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        self.db = self.__class__.db

    # Database connection tests
    def test_db(self):
        self.assertIsInstance(self.db, Database)

    def test_db_true(self):
        self.assertEqual(self.db.testing, True)

    # /health route testing
    def test_health(self):
        response = self.client.get('/health')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'Active')

    # /request route testing
    def test_request(self):
        response = self.client.get('/request', query_string={'stationID': 46237})
        data = json.loads(response.data)
        self.assertEqual(len(data), 6)

if __name__ == "__main__":
    unittest.main()
