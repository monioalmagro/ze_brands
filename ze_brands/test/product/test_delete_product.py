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
class TestDeleteProduct:
    def setup_class(self):
        self.schema_url = "/graphql/"
        self.create_product = read_graphql(
            "/apps/product/graphql/mutations/product/create_product.graphql"
        )
        self.delete_product = read_graphql(
            "/apps/product/graphql/mutations/product/delete_product.graphql"
        )

    def create_brand(self, client) -> dict:
        self.create_brand = read_graphql(
            "/apps/product/graphql/mutations/brand/create_brand.graphql"
        )
        body_brand = {
            "query": self.create_brand,
            "variables": {
                "name": "Philips",
                "description": "The most famouse brand of the EEUU",
            },
        }
        response_brand = client.post(
            self.schema_url,
            json.dumps(body_brand),
            content_type="application/json",
        )
        response = response_brand.json()
        return response["data"]["createBrand"]["brand"]

    def test_staff_user_delete_product(
        self, db, client, staff_user_force_logged
    ) -> None:
        brand: dict = self.create_brand(client)

        body = {
            "query": self.create_product,
            "variables": {"name": "TELEVISOR", "price": 200, "brandId": 1},
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        body2 = {
            "query": self.delete_product,
            "variables": {
                "productId": 1,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body2), content_type="application/json"
        )
        response = response.json()
        assert response["data"]["deleteProduct"]["message"] == RESPONSE_SUCCESS
        assert response["data"]["deleteProduct"]["success"] == True
        assert (
            response["data"]["deleteProduct"]["product"]["name"]
            == body["variables"]["name"]
        )
        assert (
            Decimal(response["data"]["deleteProduct"]["product"]["price"])
            == body["variables"]["price"]
        )
        assert response["data"]["deleteProduct"]["product"]["brand"] == brand

    def test_user_public_cant_delete_product(
        self, db, client, user_setup
    ) -> None:
        body = {
            "query": self.delete_product,
            "variables": {"productId": 1},
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()
        assert response["data"]["deleteProduct"]
        assert response["data"]["deleteProduct"]["success"] == False
        assert (
            response["data"]["deleteProduct"]["message"]
            == UNAUTHENTICATED_USER_RESPONSE
        )
        assert response["data"]["deleteProduct"]["product"] is None
