import pytest
from django.test import Client, RequestFactory
from graphene.test import Client as GrapheneClient
from graphql_jwt.shortcuts import get_token

from apps.customuser.models import MyUser
from apps.product.models import Product
from schema.schema import schema


@pytest.fixture
def graphql_client(request):
    client = GrapheneClient(schema)
    if user := getattr(request.module, "authenticated_user", None):
        token = get_token(user)
        client.headers["Authorization"] = f"JWT {token}"
    return client


@pytest.fixture
def django_client():
    return Client()


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def db_setup():
    user = MyUser.objects.create_user(
        username="testuser", password="testpass", email="test@example.com"
    )
    product = Product.objects.create(
        sku="123456", name="Test Product", price=19.99, brand="Test Brand"
    )
    return user, product


@pytest.fixture
def user_setup():
    return MyUser.objects.create(
        username="testuser1", password="testpass1", email="test1@example.com"
    )


@pytest.fixture
def staff_user_force_logged(db, client, user_setup):
    client.force_login(user=user_setup)
    return user_setup
