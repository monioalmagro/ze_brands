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
class TestUpdateUser:
    def setup_class(self):
        self.schema_url = "/graphql/"
        self.create_user = read_graphql(
            "/apps/customuser/graphql/create_user.graphql"
        )
        self.update_user = read_graphql(
            "/apps/customuser/graphql/update_user.graphql"
        )

    def get_user(self, client):
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
        return response["data"]["createUser"]["user"]

    def test_staff_user_update_user(
        self, db, client, staff_user_force_logged
    ) -> None:
        user = self.get_user(client)
        body = {
            "query": self.update_user,
            "variables": {
                "userId": 1,
                "username": "Diego",
                "email": "diego@bet.com",
                "lastName": "Maradona",
                "password": "101010",
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()

        assert response["data"]
        assert response["data"]["updateUser"]["message"] == RESPONSE_SUCCESS
        assert response["data"]["updateUser"]["success"] == True
        assert (
            response["data"]["updateUser"]["user"]["username"]
            == body["variables"]["username"]
        )
        assert (
            response["data"]["updateUser"]["user"]["lastName"]
            == body["variables"]["lastName"]
        )
        assert (
            response["data"]["updateUser"]["user"]["email"]
            == body["variables"]["email"]
        )

    def test_visitor_user_cant_update_user(
        self, db, client, user_setup
    ) -> None:
        user = self.get_user(client)
        body = {
            "query": self.update_user,
            "variables": {
                "userId": 1,
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
            response["data"]["updateUser"]["message"]
            == UNAUTHENTICATED_USER_RESPONSE
        )
        assert response["data"]["updateUser"]["success"] == False
        assert response["data"]["updateUser"]["user"] is None
