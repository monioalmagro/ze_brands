# Third-party Libraries
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    """My user manager."""

    def create_user(
        self,
        username,
        email,
        password,
        first_name="",
        last_name="",
        *args,
        **kwargs
    ):
        """Create a user.

        Args:
            username (str): username.
            email (str): user email.
            password (str): password.
            first_name (str): first name.
            last_name (str): last name.
            *args:
            **kwargs:

        Returns:
            MyUser: if user is created. Raise error: otherwise.

        """
        if not username:
            raise ValueError("Users must have an username")

        if not email:
            raise ValueError("Users must have an email address")

        user_kwargs = {
            "email": self.normalize_email(email),
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }

        user_kwargs.update(**kwargs)

        user = self.model(**user_kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """Create a super user.

        Args:
            username (str): username.
            email (str): user email.
            password (str): password.

        Returns:
            MyUser: if user is created. Raise error: otherwise.

        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """
    A custom user model representing a registered user in the system.

    Attributes:
        password (str): The user's password, hashed for security.
        is_active (bool): Whether the user account is currently active.
        username (str): The user's unique username.
        email (str): The user's unique email address.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        is_team (bool): Whether the user belongs to a team.
        is_staff (bool): Whether the user has access to the admin site.
        has_perm (bool): Whether the user has any permissions.
    """

    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    username = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_team = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    has_perm = models.BooleanField(default=True)

    def has_module_perms(self, app_label):
        """User has module perms.

        Args:
            app_label:

        Returns:
            True.

        """
        return True

    def has_perm(self, perm, obj=None):
        """User has perm.

        Args:
            perm:
            obj:

        Returns:
            True.

        """
        return "delete" not in perm

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return self.username
