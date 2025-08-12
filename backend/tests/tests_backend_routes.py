import json
import os
import pytest

from app import app
from dbClass import Database, factory
from appConfig import AppConfig
from dotenv import load_dotenv


@pytest.fixture(scope='module')
def client():
    # Setup flask testing client
    app_context = app.app_context()
    app_context.push()
    client = app.test_client()
    app.testing = True
    yield client


@pytest.fixture(scope='module')
def db():
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

    db: Database | None = factory(
            user=config.db_user,
            password=config.db_password,
            db_name=config.db_name,
            logger=app.logger,
            testing=True,
            db_host=config.db_host
        )

    yield db


class TestRoutes():
    # Database connection tests
    def test_db(self, db):
        """
        Tests whether the db object is successfully created
        """
        assert isinstance(db, Database)

    def test_db_true(self, db):
        """
        Tests whether the testing flag is set
        """
        assert db.testing is True

    # /health route testing
    def test_health(self, client):
        """
        Tests whether the server health is good via the /health route
        """
        response = client.get('/health')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['status'] == 'Active'

    # /request route testing
    def test_request(self, client):
        """
        Tests that the data returned from a valid request contains 6 items
        """
        response = client.get('/request', query_string={'stationID': 46237})
        data = json.loads(response.data)
        assert len(data) == 6

    def test_request_invalid(self, client):
        """
        Tests the response requesting a buoy that doesn't exist
        """
        response = client.get('/request', query_string={'stationID': 'ABCD'})
        data = json.loads(response.data)
        assert response.status_code == 404
        assert data == {
            "error": "No buoy found for stationID ABCD"
        }

    def test_request_no_id(self, client):
        """
        Tests the response when no parameter is passed in
        """
        response = client.get('/request', query_string={'stationID': ''})
        data = json.loads(response.data)
        assert response.status_code == 400
        assert data == {
            "result": "No station ID passed"
        }

    def test_request_all(self, client):
        """
        Testing the length of response when the 'all' is passed in
        """
        response = client.get('/request', query_string={'stationID': 'all'})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == 879

    def test_request_all_fail(self, client):
        """
        Testing the response when there is no data returned
        """
        # Create test that mocks allBuoys(db) returning none