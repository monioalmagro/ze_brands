import graphene
import graphql_jwt
from apps.customuser.schema.mutations import (
    CreateUserMutation,
    DeleteUserMutation,
    UpdateUserMutation,
)
from apps.product.schema.mutations import (
    CreateProductMutation,
    DeleteProductMutation,
    UpdateProductMutation,
)
from apps.product.schema.mutations.brand import CreateBrandMutation
from apps.product.schema.queries.product import ProductQuery


class Query(ProductQuery, graphene.ObjectType):
    ...


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_product = CreateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()
    update_product = UpdateProductMutation.Field()

    create_brand = CreateBrandMutation.Field()

    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
