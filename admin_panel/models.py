from re import L, T
from user_panel.models import Category, Product
from django.contrib.auth.models import User
from django.db import models
from user_panel.models import *
from accounts.models import *
from django.core.exceptions import ValidationError
# from user_panel.views import product_offer



class CuponOrReferralOffer(models.Model):
    offer_for = models.CharField(max_length=20, default="Today special offer")
    cupon_code = models.CharField(max_length=15)
    offer_percentage = models.PositiveIntegerField()
    time_period = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cupon code: " + str(self.cupon_code)

    def clean(self):
        # statements
        if self.product.quantity == 0:
            raise ValidationError('*Product quantity zero')



class CategoryOffer(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    offer_for = models.CharField(max_length=20, default="Today special offer")
    offer_percentage = models.PositiveIntegerField()
    time_period = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Category: " + str(self.category)

    # def clean(self):
    #     # statements
    #     prd_count = Product.objects.get(category=self.category).count()
    #     if prd_count == 0:
    #         raise ValidationError('*No products under this category')


class ProductOffer(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    offer_for = models.CharField(max_length=20, default="Today special offer")
    offer_percentage = models.PositiveIntegerField()
    time_period = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Product: " + str(self.product)
    
    def clean(self):
        # statements
        if self.product.quantity == 0:
            raise ValidationError('*Product quantity zero')

    # def save(self, *args, **kwargs):
    #     if self.product.offer_price == 0:
    #         slug = self.product.slug
    #         # offer_price = product_offer(slug)
    #         product = Product.objects.get(slug=slug)
    #         product.offer_price = 1

    #         print("``````````` offer price assigned to product offer price``````````````")
    #         print(str(product) + "  ````` product `````````````````")
    #         print(str(product.offer_price) + "  `````product.offer_price`````````````````")
    #     super().save(*args, **kwargs)

