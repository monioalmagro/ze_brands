# Standard Libraries
from typing import Optional, Tuple

# Third-party Libraries
import graphene
from django.forms import ValidationError

# Own Libraries
from apps.product.models import Brand
from apps.product.schema.nodes.product import BrandNode
from apps.product.validator import BrandModel
from utils.constans import RESPONSE_SUCCESS, UNAUTHENTICATED_USER_RESPONSE


class CreateBrandMutation(graphene.relay.ClientIDMutation):
    """
    The CreateBrandMutation class is a GraphQL mutation that allows
    clients to create a new brand object. This class inherits from
    graphene.relay.ClientIDMutation which provides functionality
    to generate unique client-side IDs for the newly created object.
    The CreateBrandMutation class has an Input class nested inside it,
    which defines the input fields required for creating a brand.
    The input fields include a name field which is a required string,
    and a description field which is an optional string. Clients must
    provide the name field to create a brand, but they may choose to
    include a description as well.

    The CreateBrandMutation class has three output fields.
    The success field is a boolean that indicates whether the brand
    was successfully created. The brand field is a BrandNode object
    that represents the newly created brand. The message field is an
    optional string that can be used to provide additional information
    about the mutation's execution.

    To use the CreateBrandMutation class, clients can pass in the
    required input fields (e.g. name) and any optional input
    fields (e.g. description) as arguments. Once executed,
    the mutation will return a boolean indicating whether the brand was
    successfully created, a BrandNode object representing the newly
    created brand, and an optional message.
    """

    class Input:
        def __init__(self):
            ...

        name = graphene.String(required=True)
        description = graphene.String(required=False)

    success = graphene.Boolean()
    brand = graphene.Field(BrandNode)
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return cls(False, None, UNAUTHENTICATED_USER_RESPONSE)
            process = ProccesCreateBrand()
            success, brand = process.create(**kwargs)

            return cls(success, brand, RESPONSE_SUCCESS)
        except (ValidationError, Exception) as exp:
            return cls(False, None, str(exp))


class BrandFactory:
    @staticmethod
    def create_brand(**kwargs) -> Brand:
        BrandModel(**kwargs)
        return Brand.objects.create(**kwargs)


class ProccesCreateBrand:
    def __init__(self) -> None:
        self.brand_factory = BrandFactory()

    def create(self, **kwargs) -> Tuple[bool, Optional[Brand]]:
        if brand := self.brand_factory.create_brand(**kwargs):
            return True, brand

        return False, None
