# Third-party Libraries
import graphene

# Own Libraries
from apps.product.models import Product
from apps.product.schema.connections import ProductNodeConnection
from utils.save_visitor import save_date


class ProductQuery(object):
    product = graphene.ConnectionField(
        ProductNodeConnection,
        id=graphene.Int(required=False),
    )

    @staticmethod
    def resolve_product(root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            save_date(info)
        qs = Product.objects.filter(is_deleted=False)
        if pk := kwargs.get("id"):
            qs = qs.filter(pk=pk)
        return qs
