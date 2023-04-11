# Third-party Libraries
import graphene
from django.contrib.auth.models import User


class UserNode(graphene.ObjectType):
    username = graphene.String()
    last_name = graphene.String()
    email = graphene.String()

    class Meta:
        model = User
        interfaces = (graphene.Node,)
        description = """
        The UserNode class is a  object type that represents a user.
        It has three fields: username, last_name, and email, each of
        which is a string field that contains the corresponding user's data.
        """

    @staticmethod
    def resolve_original_id(root, info):
        return root.id

    @staticmethod
    def resolve_username(root, info):
        return root.username

    @staticmethod
    def resolve_last_name(root, info):
        return root.last_name

    @staticmethod
    def resolve_email(root, info):
        return root.email
