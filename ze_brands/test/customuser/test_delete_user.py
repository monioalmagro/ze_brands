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
class TestDeleteUser:
    def setup_class(self):
        self.schema_url = "/graphql/"
        self.create_user = read_graphql(
            "/apps/customuser/graphql/create_user.graphql"
        )
        self.delete_user = read_graphql(
            "/apps/customuser/graphql/delete_user.graphql"
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

    def test_staff_user_delete_user(
        self, db, client, staff_user_force_logged
    ) -> None:
        user = self.get_user(client)
        body = {
            "query": self.delete_user,
            "variables": {
                "userId": 1,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()
        print(response)
        assert response["data"]
        assert response["data"]["deleteUser"]["message"] == RESPONSE_SUCCESS
        assert response["data"]["deleteUser"]["success"] == True
        assert response["data"]["deleteUser"]["user"] == None

    def test_visitor_user_cant_delete_user(
        self, db, client, user_setup
    ) -> None:
        user = self.get_user(client)
        body = {
            "query": self.delete_user,
            "variables": {
                "userId": 1,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()

        assert response["data"]
        assert (
            response["data"]["deleteUser"]["message"]
            == UNAUTHENTICATED_USER_RESPONSE
        )
        assert response["data"]["deleteUser"]["success"] == False
        assert response["data"]["deleteUser"]["user"] is None
