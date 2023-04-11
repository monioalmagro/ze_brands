# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.visitor.models import Visitor

admin.site.register(Visitor)
