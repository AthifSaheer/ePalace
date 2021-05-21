from accounts.models import Admin
from django.contrib import admin
from .models import Admin, RefLink

admin.site.register([Admin, RefLink])

