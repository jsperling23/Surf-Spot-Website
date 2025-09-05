import json
import os
import pytest
import subprocess

from app import app
from dbClass import Database, factory
from appConfig import AppConfig
from dotenv import load_dotenv


@pytest.fixture(scope='module')
def db():
    # setup testing Database object
    load_dotenv()
    config = AppConfig(
        **{
            "db_user": os.getenv("DB_USER"),
            "db_password": os.getenv("DB_PASSWORD"),
            "db_name": os.getenv("DB_NAME_TEST"),
            "db_host": os.getenv("DB_HOST"),
            "secret_key": os.getenv("SECRET_KEY"),
        }
    )

    db: Database | None = factory(
            user=config.db_user,
            password=config.db_password,
            db_name=config.db_name,
            logger=app.logger,
            db_host=config.db_host
        )

    if not db:
        pytest.skip("Database fixture setup failed")

    # Setup test DB schema and fill buoy table
    with open("database/ddl.sql", "r") as f:
        subprocess.run(
            ["mysql", "-u", config.db_user, f"-p{config.db_password}", config.db_name],
            stdin=f,
            check=True
        )

    with open("database/buoy_backup.sql", "r") as f:
        subprocess.run(
            ["mysql", "-u", config.db_user, f"-p{config.db_password}", config.db_name],
            stdin=f,
            check=True
        )
    yield db

    # Clear test db after finishing
    db.executeQuery("DROP TABLE IF EXISTS Buoys, Users, SurfSpots,\
                    IdealConditions, SavedSessions;", [])


@pytest.fixture(scope='module')
def client():
    # Setup flask testing client
    with app.test_client() as client:
        client.testing = True
        yield client


# Database connection tests
def test_db(db):
    """
    Tests whether the db object is successfully created
    """
    assert isinstance(db, Database)


class TestNotLoggedRoutes():
    # /health route testing
    def test_health(self, client):
        """
        Tests whether the server health is good via the /health route
        """
        response = client.get('/health')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['status'] == 'Active'

    # test whether trying to access a protected route fails
    def test_not_logged_auth(self, client):
        """
        Tests whether the /auth route fails when requesting not logged in
        """
        response = client.get('/auth')
        assert response.status_code == 401

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

    def test_request_all(self, client, db):
        """
        Testing the length of response when the 'all' is passed in
        """
        app.db = db
        response = client.get('/request', query_string={'stationID': 'all'})
        data = json.loads(response.data)
        assert response.status_code == 200
        assert 870 <= len(data) <= 890

    def test_request_all_fail(self, client, monkeypatch):
        """
        Testing the response when there is no data returned
        """
        app.db = db
        monkeypatch.setattr("app.allBuoys", lambda db: None)
        response = client.get('/request', query_string={'stationID': 'all'})
        assert response.status_code == 404
        assert json.loads(response.data) == {"result": "Error occurred"}

    def test_request_station_fail(self, client):
        """
        Testing the response when there is no data returned
        """
        response = client.get('/request')
        assert response.status_code == 400
        assert json.loads(response.data) == {"result": "No station ID passed"}

    # /findBuoys route testing
    def test_buoy_find(self, client, monkeypatch, db):
        """
        Testing finding the closest buoys using Ocean Beach, SF, as coordinates
        lat: 37.7594
        long: 122.5107
        """
        monkeypatch.setattr("app.db_handler", db)
        response = client.get('/findBuoys', query_string={
            "lat": 37.7594,
            "long": -122.5107
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 20
        assert data['6.502'] == ['FTPC1',
                                 '9414290 - San Francisco, CA',
                                 '37.806',
                                 '-122.466']
        assert data['11.294'] == ['46237',
                                  'San Francisco Bar, CA  (142)',
                                  '37.788',
                                  '-122.634']

    def test_buoy_find_empty(self, client):
        """
        Testing looking for coordinates with no data passed
        """
        response = client.get('/findBuoys', query_string={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data == {"result": "No coorindates passed"}

    # /createUser route testing
    def test_create_user(self, monkeypatch, client, db):
        """
        Testing creating a user
        """
        monkeypatch.setattr("app.db_handler", db)
        response = client.post('/createUser', json={
            "username": "test",
            "password": "test"
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {"result": "Account creation successful"}

    def test_create_user_duplicate(self, monkeypatch, client, db):
        """
        Testing trying to create a user that already exists
        """
        monkeypatch.setattr("app.db_handler", db)
        response = client.post('/createUser', json={
            "username": "test",
            "password": "test"
        })
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data == {"result": "Username already exists"}

    def test_create_user_empty(self, client, db, monkeypatch):
        """
        Testing sending an empty form
        """
        monkeypatch.setattr("app.db_handler", db)
        response = client.post('/createUser', json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data == {"result": "Bad request, no data passed to form!"}

    def test_create_user_db_error(self, monkeypatch, client, db):
        """
        Testing sending an empty form
        """
        monkeypatch.setattr("app.db_handler", db)
        monkeypatch.setattr("app.User.createUser",
                            lambda username,
                            password,
                            db: (False, 2)
                            )
        response = client.post('/createUser', json={
            "username": "test2",
            "password": "test"
        })
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data == {"result": "Internal service error"}

    # /login route testing
    def test_login(self, client, monkeypatch, db):
        """
        Testing whether the login route works using the test credentials
        """
        monkeypatch.setattr("app.db_handler", db)
        response = client.post('/login', json={
            "username": "test",
            "password": "test"
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {"result": "Login Successful",
                        "userID": 1}

    def test_failed_login(self, client):
        """
        Testing how a failed login works
        """
        response = client.post('/login', json={
            "username": "test",
            "password": "teesty"
        })
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data == {"result": "Login Failed"}

    def test_empty_login(self, client):
        """
        Testing how an empty request login works
        """
        response = client.post('/login', json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data == {"result": "Bad request, no data passed to form!"}


class TestLoggedRoutes():
    # /auth route testing
    def test_auth(self, client):
        """
        Tests whether accessing the /auth route while logged in works
        """
        response = client.get('/auth')
        assert response.status_code == 200

    # /surfSpot route testing
    def test_create_spot(self, client, monkeypatch, db):
        """
        Test the reponse when creating a new surf spot
        """
        monkeypatch.setattr("app.db_handler", db)
        response = client.post('/surfSpot', json={
            "userID": 1,
            "name": "Ocean Beach",
            "latitude": 37.690,
            "longitude": -122.520,
            "firstBuoyID": '46237',
            "secondBuoyID": '46026'
        })

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data == {"result": "Spot Created", "spotID": 1}

    def test_create_spot_err(self, client, monkeypatch):
        """
        Tests whether a failed spot creation returns an error
        """
        monkeypatch.setattr("app.createSpot", lambda *args, **kwargs: False)
        response = client.post('/surfSpot', json={
            "userID": 1,
            "name": "Ocean Beach",
            "latitude": 37.690,
            "longitude": -122.520,
            "firstBuoyID": '46237',
            "secondBuoyID": '46026'
        })
        assert response.status_code == 409

