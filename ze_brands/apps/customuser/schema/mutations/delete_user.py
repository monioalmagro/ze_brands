# Standard Libraries
from typing import Optional, Tuple

# Third-party Libraries
import graphene
from django.forms import ValidationError

# Own Libraries
from apps.customuser.models import MyUser
from apps.customuser.schema.nodes.user import UserNode
from utils.constans import RESPONSE_SUCCESS, UNAUTHENTICATED_USER_RESPONSE


class DeleteUserMutation(graphene.relay.ClientIDMutation):
    class Input:
        def __init__(self):
            ...

        user_id = graphene.ID(required=True)

    success = graphene.Boolean()
    user = graphene.Field(UserNode)
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return cls(False, None, UNAUTHENTICATED_USER_RESPONSE)
            process = ProccesDeleteUser()
            success, user = process.delete(**kwargs)

            return cls(success, None, RESPONSE_SUCCESS)
        except (ValidationError, Exception) as exp:
            return cls(False, None, str(exp))


class UserFactory:
    @staticmethod
    def delete_user(user_id) -> MyUser:
        if user := MyUser.objects.filter(id=user_id).delete():
            return user
        else:
            raise AssertionError("User does not exist.")


class ProccesDeleteUser:
    def __init__(self) -> None:
        self.user_factory = UserFactory()

    def delete(self, **kwargs) -> Tuple[bool, Optional[MyUser]]:
        if user := self.user_factory.delete_user(**kwargs):
            return True, user

        return False, None
