from django.core.exceptions import ValidationError
from user_panel.models import Category, Product
from django.contrib.auth.models import User
from accounts.utils import generate_cupon

from user_panel.models import *
from accounts.models import *
from django.db import models
from re import L, T
import re



class CuponOffer(models.Model):
    offer_for = models.CharField(max_length=20, default="Today special offer")
    cupon_code = models.CharField(max_length=50, unique=True)
    offer_price = models.PositiveIntegerField()
    date_period = models.DateField()
    time_period = models.TimeField()
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="cupon_taken_user", on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cupon code: " + str(self.cupon_code)

class ReferralCupon(models.Model):
    offer_for = models.CharField(max_length=20, default="Referral offer")
    cupon_code = models.CharField(max_length=50, unique=True)
    offer_price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)
    which_user = models.ForeignKey(User, related_name="which_user", on_delete=models.CASCADE, null=True, blank=True)
    taken_user = models.ForeignKey(User, related_name="taken_user", on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: " + str(self.which_user) + " - Cupon: " + str(self.cupon_code)

    def save(self, *args, **kwargs):
        if self.cupon_code == "":
            self.cupon_code = generate_cupon()
        super().save(*args, **kwargs)

class SignupCupon(models.Model):
    offer_for = models.CharField(max_length=20, default="Referral offer")
    cupon_code = models.CharField(max_length=50, unique=True)
    offer_price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)
    which_user = models.OneToOneField(User, related_name="which_user_signup", on_delete=models.CASCADE, null=True, blank=True)
    taken_user = models.ForeignKey(User, related_name="signup_cupon_taken_user", on_delete=models.CASCADE, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: " + str(self.which_user) + " - Cupon: " + str(self.cupon_code)
    
    def save(self, *args, **kwargs):
        if self.cupon_code == "":
            self.cupon_code = generate_cupon()
        super().save(*args, **kwargs)


class CategoryOffer(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    offer_for = models.CharField(max_length=20, default="Today special offer")
    # offer_price = models.PositiveIntegerField()
    offer_percentage = models.PositiveIntegerField()
    date_period = models.DateField()
    time_period = models.TimeField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Category: " + str(self.category)


class ProductOffer(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    offer_for = models.CharField(max_length=20, default="Today special offer")
    offer_percentage = models.PositiveIntegerField()
    date_period = models.DateField()
    time_period = models.TimeField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Product: " + str(self.product)
    
    def clean(self):
        # statements
        if self.product.quantity == 0:
            raise ValidationError('*Product quantity zero')


