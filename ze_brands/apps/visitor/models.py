# Third-party Libraries
from django.db import models


class Visitor(models.Model):
    """
    A model representing a website visitor.

    Attributes:
        accept_language (str): The HTTP "Accept-Language" header of the visitor's browser.
        user_agent (str): The HTTP "User-Agent" header of the visitor's browser.
        ip_address (str): The IP address of the visitor.
        created_at (datetime.date): The date when the visitor record was created.
    """

    accept_language = models.CharField(max_length=250, null=True, blank=True)
    user_agent = models.CharField(max_length=250, null=True, blank=True)
    ip_address = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return str(self.created_at)
