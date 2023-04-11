# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.product.models import Brand, Product

admin.site.register(Brand)

admin.site.register(Product)
