# Standard Libraries
from typing import Tuple

# Third-party Libraries
import graphene
from django.forms import ValidationError

# Own Libraries
from apps.product.models import Product
from apps.product.schema.nodes.product import ProductNode
from observer.observer import ConcreteSubject
from utils.constans import RESPONSE_SUCCESS, UNAUTHENTICATED_USER_RESPONSE


class UpdateProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        def __init__(self):
            ...

        product_id = graphene.ID(required=True)
        sku = graphene.String(required=False)
        name = graphene.String(required=False)
        price = graphene.Decimal(required=False)
        brand = graphene.String(required=False)

    success = graphene.Boolean()
    product = graphene.Field(ProductNode)
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return cls(False, None, UNAUTHENTICATED_USER_RESPONSE)
            process = ProccesUpdateProduct()
            success, product = process.update(**kwargs)
            if success:
                send_update = ConcreteSubject()
                send_update.change_product(product)
            return cls(success, product, RESPONSE_SUCCESS)
        except (ValidationError, Exception) as exp:
            return cls(False, None, str(exp))


class ProductFactory:
    @staticmethod
    def get_product(**kwargs):
        if product := Product.objects.filter(
            id=kwargs.get("product_id"), is_deleted=False
        ).first():
            return product
        else:
            raise AssertionError("Product does not exist.")

    @staticmethod
    def get_elemets_update(product: Product, **kwargs) -> Tuple[list, Product]:
        """
        Updates a Product object with the specified keyword arguments and returns the
            list of updated fields and the updated Product object.

        Args:
            product (Product): The Product object to update.
            **kwargs: Keyword arguments specifying the fields to update and their new values.
                Valid fields are 'sku', 'name', and 'price'.

        Returns:
            A tuple containing:
            - A list of strings, representing the names of the updated fields.
            - The updated Product object.
        """
        fields = {}
        if "sku" in kwargs:
            fields["sku"] = kwargs["sku"]
            product.sku = kwargs["sku"]
        if "name" in kwargs:
            fields["name"] = kwargs["name"]
            product.name = kwargs["name"]
        if "price" in kwargs:
            fields["price"] = kwargs["price"]
            product.price = kwargs["price"]

        return list(fields.keys()), product

    def update_product(self, **kwargs) -> Product:
        product = self.get_product(**kwargs)

        fiels, new_product = self.get_elemets_update(product, **kwargs)

        new_product.save(update_fields=fiels)

        return new_product


class ProccesUpdateProduct:
    def __init__(self) -> None:
        self.product_factory = ProductFactory()

    def update(self, **kwargs):
        if product := self.product_factory.update_product(**kwargs):
            return True, product
        return False, None
