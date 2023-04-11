# Third-party Libraries
import graphene


class BrandNode(graphene.ObjectType):
    original_id = graphene.Int()
    name = graphene.String()
    description = graphene.String()

    class Meta:
        interfaces = (graphene.Node,)
        description = """
        BrandNode represents a node that contains information about a brand.
        The class has three attributes: original_id, name, and description.

        The original_id field is defined as an integer field of graphene
        and represents the unique identifier of the brand.
        The name and description fields are defined as graphene string fields
        and represent the name and description of the brand, respectively.
        """

    @staticmethod
    def resolve_original_id(root, info):
        return root.id


class ProductNode(graphene.ObjectType):
    original_id = graphene.Int()
    sku = graphene.String()
    name = graphene.String()
    price = graphene.Decimal()
    brand = graphene.Field(BrandNode)

    class Meta:
        interfaces = (graphene.Node,)
        description = """
        The ProductNode class is object type that represents a product
        It has four fields: original_id, sku, name, and price.

        The original_id field is an integer representing the unique identifier
        of the product.
        The sku field is a string representing the stock keeping unit (SKU)
        code of the product.
        The name field is a string representing the name of the product.
        The price field is a decimal representing the price of the product.
        """

    @staticmethod
    def resolve_original_id(root, info):
        return root.id

    @staticmethod
    def resolve_name(root, info):
        return root.name

    @staticmethod
    def resolve_price(root, info):
        return root.price

    @staticmethod
    def resolve_brand(root, info):
        return root.brand
