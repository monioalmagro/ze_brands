# Standard Libraries
from typing import Optional, Tuple

# Third-party Libraries
import graphene
from django.forms import ValidationError

# Own Libraries
from apps.customuser.models import MyUser
from apps.customuser.schema.nodes.user import UserNode
from apps.customuser.validator import MyUserModel
from utils.constans import RESPONSE_SUCCESS, UNAUTHENTICATED_USER_RESPONSE


class CreateUserMutation(graphene.relay.ClientIDMutation):
    """
    The CreateUserMutation class is a mutation type in the GraphQL framework
    that allows clients to create new user records. It extends
    the ClientIDMutation class, which ensures that the created user record
    is globally identifiable with a unique client ID.

    The class has an Input inner class that defines the input fields required
    for creating a user. These fields include username, last_name, email,
    and password. The required=True argument indicates that these fields
    are mandatory.

    The CreateUserMutation class has three output fields that define the response
    returned to the client after the mutation completes:

    success - a Boolean field that indicates whether the mutation succeeded or not.
    user - a field of type UserNode that represents the created user record.
    message - a field of type String that provides additional information about
    the mutation result, such as an error message if the mutation failed.
    Clients can use this mutation to create new users by passing the required
    input fields as arguments. If the mutation succeeds, the response will include
    the newly created user record along with a success field set to True.
    If the mutation fails, the success field will be False, and the message field
    will provide information about the error.
    """

    class Input:
        def __init__(self):
            ...

        username = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    user = graphene.Field(UserNode)
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return cls(False, None, UNAUTHENTICATED_USER_RESPONSE)
            process = ProccesCreateUser()
            success, user = process.create(**kwargs)

            return cls(success, user, RESPONSE_SUCCESS)
        except (ValidationError, Exception) as exp:
            return cls(False, None, str(exp))


class UserFactory:
    @staticmethod
    def create_user(**kwargs) -> MyUser:
        MyUserModel(**kwargs)
        return MyUser.objects.create(**kwargs)


class ProccesCreateUser:
    def __init__(self) -> None:
        self.user_factory = UserFactory()

    def create(self, **kwargs) -> Tuple[bool, Optional[MyUser]]:
        if user := self.user_factory.create_user(**kwargs):
            return True, user

        return False, None
