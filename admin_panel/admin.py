from django.contrib import admin
from .models import CategoryOffer, ProductOffer, CuponOffer, SignupCupon, ReferralCupon


admin.site.register([CategoryOffer, ProductOffer, CuponOffer, SignupCupon, ReferralCupon])
# admin.site.register([])
