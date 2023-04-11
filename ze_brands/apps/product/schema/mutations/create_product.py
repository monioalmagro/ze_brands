# Standard Libraries
from typing import Optional, Tuple

# Third-party Libraries
import graphene
from django.forms import ValidationError

# Own Libraries
from apps.product.models import Brand, Product
from apps.product.schema.nodes.product import ProductNode
from apps.product.validator import ProductModel
from utils.constans import RESPONSE_SUCCESS, UNAUTHENTICATED_USER_RESPONSE


class CreateProductMutation(graphene.relay.ClientIDMutation):
    """
    The CreateProductMutation class is a GraphQL mutation that allows clients
    to create a new product with the specified name, price, and brand_id.
    This mutation is built using the graphene.relay.ClientIDMutation class,
    which enables client-side mutation tracking.
    The Input class represents the input arguments required for creating
    a new product. In this case, it includes name, price, and brand_id,
    all of which are required fields. The name argument is a string that
    represents the name of the product, the price argument is a decimal
    that represents the price of the product, and the brand_id argument
    is an ID that represents the ID of the brand to which the product belongs.
    The success field is a boolean that indicates whether the mutation
    was successful or not. The product field is a ProductNode object that
    represents the newly created product. The message field is a string
    that provides additional information about the success or failure of the mutation.
    Overall, the CreateProductMutation class provides a convenient way for clients
    to create new products through GraphQL mutations and is a useful component
    for building GraphQL APIs that involve product creation.
    """

    class Input:
        def __init__(self):
            ...

        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        brand_id = graphene.ID(requiered=True)

    success = graphene.Boolean()
    product = graphene.Field(ProductNode)
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return cls(False, None, UNAUTHENTICATED_USER_RESPONSE)
            process = ProccesCreateProduct()
            success, product = process.create(**kwargs)

            return cls(success, product, RESPONSE_SUCCESS)
        except (ValidationError, Exception) as exp:
            return cls(False, None, str(exp))


class ProductFactory:
    @staticmethod
    def create_product(**kwargs) -> Product:
        ProductModel(**kwargs)
        return Product.objects.create(**kwargs)


class ProccesCreateProduct:
    def __init__(self) -> None:
        self.product_factory = ProductFactory()

    def create(self, **kwargs) -> Tuple[bool, Optional[Product]]:
        brand = Brand.objects.filter(id=kwargs.get("brand_id")).first()
        if not brand:
            raise AssertionError("Brand does not exist.")
        kwargs.pop("brand_id")
        kwargs["brand"] = brand
        if product := self.product_factory.create_product(**kwargs):
            return True, product

        return False, None
