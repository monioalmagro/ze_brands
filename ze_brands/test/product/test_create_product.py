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
class TestCreateProduct:
    def setup_class(self):
        self.schema_url = "/graphql/"
        self.create_product = read_graphql(
            "/apps/product/graphql/mutations/product/create_product.graphql"
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

    def test_staff_user_create_product(
        self, db, client, staff_user_force_logged
    ) -> None:
        brand: dict = self.create_brand(client)

        body = {
            "query": self.create_product,
            "variables": {
                "name": "TELEVISOR",
                "price": 200,
                "brandId": 1,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()
        assert response["data"]["createProduct"]["message"] == RESPONSE_SUCCESS
        assert response["data"]["createProduct"]["success"] == True
        assert (
            response["data"]["createProduct"]["product"]["name"]
            == body["variables"]["name"]
        )
        assert (
            Decimal(response["data"]["createProduct"]["product"]["price"])
            == body["variables"]["price"]
        )
        assert (
            response["data"]["createProduct"]["product"]["brand"]["name"]
            == brand["name"]
        )

    def test_user_public_cant_create_product(
        self, db, client, user_setup
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
        assert response["data"]["createProduct"]
        assert response["data"]["createProduct"]["success"] == False
        assert (
            response["data"]["createProduct"]["message"]
            == UNAUTHENTICATED_USER_RESPONSE
        )
        assert response["data"]["createProduct"]["product"] is None

    def test_staff_user_cant_create_product_by_name(
        self, db, client, staff_user_force_logged
    ) -> None:
        brand: dict = self.create_brand(client)

        name = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum feugiat diam 
        aliquam velit fringilla, euismod rutrum odio viverra. Suspendisse in tellus euismod, 
        viverra tortor at, finibus nibh. Etiam lacinia ex ipsum, ut bibendum justo porttitor.
        """
        body = {
            "query": self.create_product,
            "variables": {
                "name": name,
                "price": 200,
                "brandId": 1,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()

        assert response["data"]
        assert response["data"]["createProduct"]
        assert response["data"]["createProduct"]["success"] is False
        assert response["data"]["createProduct"]["product"] is None
        assert (
            response["data"]["createProduct"]["message"]
            == "1 validation error for ProductModel\nname\n  max length of name is 250 (type=value_error)"
        )

    def test_staff_user_cant_create_product_by_brand(
        self, db, client, staff_user_force_logged
    ) -> None:
        brand: dict = self.create_brand(client)

        body = {
            "query": self.create_product,
            "variables": {
                "name": "TELEVISOR",
                "price": 200,
                "brandId": 10,
            },
        }
        response = client.post(
            self.schema_url, json.dumps(body), content_type="application/json"
        )
        response = response.json()
        assert response["data"]
        assert response["data"]["createProduct"]
        assert response["data"]["createProduct"]["success"] is False
        assert response["data"]["createProduct"]["product"] is None
        assert (
            response["data"]["createProduct"]["message"]
            == "Brand does not exist."
        )
