from re import T
from django.contrib.auth.models import User
from django.db import models
from django.db.models import base
from .utils import generate_ref_code
from admin_panel.models import CuponOffer
from datetime import datetime, timedelta


class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
    
class UserMobileNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=13)
    otp = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: " + str(self.user.username) + " - MobileNo: " + str(self.mobile_no)
    


class RefLink(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user: " + str(self.user.username) + " . RecomUser: " + str(self.recommended_by)

    def get_recommended_profiles():
        pass

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)
    

