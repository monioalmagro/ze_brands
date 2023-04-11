# Third-party Libraries
from django.contrib import admin

# Own Libraries
from apps.customuser.models import MyUser

admin.site.register(MyUser)
