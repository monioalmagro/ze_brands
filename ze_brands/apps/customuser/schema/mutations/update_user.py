# Standard Libraries
from typing import Optional, Tuple

# Third-party Libraries
import graphene
from django.forms import ValidationError

# Own Libraries
from apps.customuser.models import MyUser
from apps.customuser.schema.nodes.user import UserNode
from utils.constans import RESPONSE_SUCCESS, UNAUTHENTICATED_USER_RESPONSE


class UpdateUserMutation(graphene.relay.ClientIDMutation):
    class Input:
        def __init__(self):
            ...

        user_id = graphene.ID(required=True)
        username = graphene.String(required=False)
        last_name = graphene.String(required=False)
        email = graphene.String(required=False)
        password = graphene.String(required=False)

    success = graphene.Boolean()
    user = graphene.Field(UserNode)
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            user = info.context.user
            if not user.is_authenticated:
                return cls(False, None, UNAUTHENTICATED_USER_RESPONSE)
            process = ProccesUpdateUser()
            success, user = process.update(**kwargs)

            return cls(success, user, RESPONSE_SUCCESS)
        except (ValidationError, Exception) as exp:
            return cls(False, None, str(exp))


class UserFactory:
    @staticmethod
    def get_user(**kwargs) -> MyUser:
        if user := MyUser.objects.filter(id=kwargs.get("user_id")).first():
            return user
        else:
            raise AssertionError("User does not exist.")

    @staticmethod
    def get_elemets_update(user: MyUser, **kwargs) -> Tuple[list, MyUser]:
        """
        Method is a static method that allows updating the fields of a user object.
        This method takes a user object of class MyUser .
        It returns a tuple containing two elements, the first element is a
        list of updated field names, and the second element is the updated user object.

        Parameters:

        user: A user object of class MyUser.
        **kwargs: A dictionary of keyword arguments representing the field names
        and their updated values.

        Return Value:
        The method returns a tuple containing two elements:

        A list of updated field names
        The updated user object.
        """
        fields = {}
        if "username" in kwargs:
            fields["username"] = kwargs["username"]
            user.username = kwargs["username"]
        if "last_name" in kwargs:
            fields["last_name"] = kwargs["last_name"]
            user.last_name = kwargs["last_name"]
        if "email" in kwargs:
            fields["email"] = kwargs["email"]
            user.email = kwargs["email"]
        if "password" in kwargs:
            fields["password"] = kwargs["password"]
            user.password = kwargs["password"]

        return list(fields.keys()), user

    def update_user(self, **kwargs) -> MyUser:
        user = self.get_user(**kwargs)
        fiels, new_user = self.get_elemets_update(user, **kwargs)
        new_user.save(update_fields=fiels)

        return new_user


class ProccesUpdateUser:
    def __init__(self) -> None:
        self.user_factory = UserFactory()

    def update(self, **kwargs) -> Tuple[bool, Optional[MyUser]]:
        if user := self.user_factory.update_user(**kwargs):
            return True, user

        return False, None
