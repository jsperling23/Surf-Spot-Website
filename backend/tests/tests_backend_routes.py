import unittest
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
        assert isinstance(db, Database)

    def test_db_true(self, db):
        assert db.testing is True

    # /health route testing
    def test_health(self, client):
        response = client.get('/health')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['status'] == 'Active'

    # /request route testing
    def test_request(self, client):
        response = client.get('/request', query_string={'stationID': 46237})
        data = json.loads(response.data)
        assert len(data) == 6
