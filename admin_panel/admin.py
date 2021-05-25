from django.contrib import admin
from .models import *


admin.site.register([CategoryOffer, CuponOffer, ProductOffer])
