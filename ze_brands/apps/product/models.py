# Standard Libraries
import uuid

# Third-party Libraries
from django.db import models


class Auditable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Brand(Auditable):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Product(Auditable):
    """
    Represents a product with a SKU, name, price, and brand.

    Attributes:
        sku (str): The product's SKU (stock keeping unit).
        name (str): The name of the product.
        price (Decimal): The price of the product.
        brand (str): The brand of the product.

    Methods:
        __str__() -> str: Returns the name of the product as a string.

    """

    sku = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    brand = models.ForeignKey(
        "Brand", on_delete=models.PROTECT, related_name="product_set"
    )

    def __str__(self) -> str:
        return self.name
