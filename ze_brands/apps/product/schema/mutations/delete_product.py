# Standard Libraries
from typing import Optional, Tuple

# Third-party Libraries
import graphene
from django.forms import ValidationError

# Own Libraries
from apps.product.models import Product
from apps.product.schema.nodes.product import ProductNode
from utils.constans import RESPONSE_SUCCESS, UNAUTHENTICATED_USER_RESPONSE


class DeleteProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        def __init__(self):
            ...

        product_id = graphene.ID(required=True)

    success = graphene.Boolean()
    product = graphene.Field(ProductNode)
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return cls(False, None, UNAUTHENTICATED_USER_RESPONSE)
            process = ProccesDeleteProduct()
            success, product = process.delete(**kwargs)

            return cls(success, product, RESPONSE_SUCCESS)
        except (ValidationError, Exception) as exp:
            return cls(False, None, str(exp))


class ProccesDeleteProduct:
    def delete(self, **kwargs) -> Tuple[bool, Optional[Product]]:
        product = Product.objects.filter(
            id=kwargs["product_id"], is_deleted=False
        ).first()
        if not product:
            raise AssertionError("Product does not exist.")

        product.is_deleted = True
        product.save(update_fields=["is_deleted", "updated_at"])
        return True, product
