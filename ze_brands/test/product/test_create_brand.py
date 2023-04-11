import json
import os
from decimal import Decimal

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
class TestCreateBrand:
    def setup_class(self):
        self.schema_url = "/graphql/"
        self.create_brand = read_graphql(
            "/apps/product/graphql/mutations/brand/create_brand.graphql"
        )

    def test_staff_user_create_brand(
        self, db, client, staff_user_force_logged
    ) -> None:
        body = {
            "query": self.create_brand,
            "variables": {
                "name": "Philips",
                "description": "The most famouse brand of the EEUU",
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()
        assert response["data"]["createBrand"]["message"] == RESPONSE_SUCCESS
        assert response["data"]["createBrand"]["success"] == True
        assert (
            response["data"]["createBrand"]["brand"]["name"]
            == body["variables"]["name"]
        )
        assert (
            response["data"]["createBrand"]["brand"]["description"]
            == body["variables"]["description"]
        )
