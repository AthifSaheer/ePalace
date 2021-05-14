from django.contrib import admin
from .models import *

admin.site.register([Category, SubCategory, Cart, ProfileImage, CartItem, Address, Order])


from django.utils.safestring import mark_safe
# import ExportCsvMixin

@admin.register(Product)
class HeroAdmin(admin.ModelAdmin):

    readonly_fields = ["image_image"]

    def image_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=obj.image.width,
            height=obj.image.height,
            )
    )