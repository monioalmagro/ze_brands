# Third-party Libraries
import graphene

# Own Libraries
from apps.product.schema.nodes.product import ProductNode

# Local Folders Libraries
from .non_null import NonNullConnection


class ProductNodeConnection(NonNullConnection):
    total_count = graphene.Int(required=True)

    class Meta:
        node = ProductNode

    @staticmethod
    def resolve_total_count(root, info):
        return len(root.iterable)
