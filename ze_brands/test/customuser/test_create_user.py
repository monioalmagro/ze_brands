import json
import os

import pytest

from utils.constans import RESPONSE_SUCCESS, UNAUTHENTICATED_USER_RESPONSE
from utils.read_graphql import read_graphql

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))

PROJECT_ROOT = BASE_DIR


def read_graphql(path_file):
    _dir = PROJECT_ROOT + path_file
    with open(_dir, "r") as _file:
        data = _file.read()
    return data


@pytest.mark.django_db
class TestCreateUser:
    def setup_class(self):
        self.schema_url = "/graphql/"
        self.create_user = read_graphql(
            "/apps/customuser/graphql/create_user.graphql"
        )

    def test_staff_user_create_user(
        self, db, client, staff_user_force_logged
    ) -> None:
        body = {
            "query": self.create_user,
            "variables": {
                "username": "Beto",
                "email": "beto@bet.com",
                "lastName": "Yaque",
                "password": "betobeto",
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()

        assert response["data"]
        assert response["data"]["createUser"]["message"] == RESPONSE_SUCCESS
        assert response["data"]["createUser"]["success"] == True
        assert (
            response["data"]["createUser"]["user"]["username"]
            == body["variables"]["username"]
        )
        assert (
            response["data"]["createUser"]["user"]["lastName"]
            == body["variables"]["lastName"]
        )
        assert (
            response["data"]["createUser"]["user"]["email"]
            == body["variables"]["email"]
        )

    def test_visitor_user_cant_create_user(
        self, db, client, user_setup
    ) -> None:
        body = {
            "query": self.create_user,
            "variables": {
                "username": "Beto",
                "email": "beto@bet.com",
                "lastName": "Yaque",
                "password": "betobeto",
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()

        assert response["data"]
        assert (
            response["data"]["createUser"]["message"]
            == UNAUTHENTICATED_USER_RESPONSE
        )
        assert response["data"]["createUser"]["success"] == False
        assert response["data"]["createUser"]["user"] is None
