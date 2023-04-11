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
class TestUpdateProduct:
    def setup_class(self):
        self.schema_url = "/graphql/"
        self.create_product = read_graphql(
            "/apps/product/graphql/mutations/product/create_product.graphql"
        )
        self.update_product = read_graphql(
            "/apps/product/graphql/mutations/product/update_product.graphql"
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

    def test_staff_user_update_product(
        self, db, client, staff_user_force_logged
    ) -> None:
        brand: dict = self.create_brand(client)

        body = {
            "query": self.create_product,
            "variables": {
                "sku": "abc123",
                "name": "TELEVISOR",
                "price": 200,
                "brandId": 1,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()
        body2 = {
            "query": self.update_product,
            "variables": {
                "productId": 1,
                "name": "DVD",
                "price": 50.99,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body2), content_type="application/json"
        )
        response = response.json()
        assert response["data"]["updateProduct"]["message"] == RESPONSE_SUCCESS
        assert response["data"]["updateProduct"]["success"] == True
        assert (
            response["data"]["updateProduct"]["product"]["name"]
            == body2["variables"]["name"]
        )
        assert (
            Decimal(response["data"]["updateProduct"]["product"]["price"])
            == body2["variables"]["price"]
        )
        assert response["data"]["updateProduct"]["product"]["brand"] == brand

    def test_user_public_cant_update_product(
        self, db, client, user_setup
    ) -> None:
        body = {
            "query": self.update_product,
            "variables": {
                "productId": 1,
                "sku": "abc123",
                "name": "TELEVISOR",
                "price": 200,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()

        assert response["data"]["updateProduct"]
        assert response["data"]["updateProduct"]["success"] == False
        assert (
            response["data"]["updateProduct"]["message"]
            == UNAUTHENTICATED_USER_RESPONSE
        )
        assert response["data"]["updateProduct"]["product"] is None
