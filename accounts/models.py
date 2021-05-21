from django.contrib.auth.models import User
from django.db import models


class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
    
# class UserMobileNumber(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     mobile_no = models.PositiveIntegerField(max_length=10)
#     otp = models.PositiveIntegerField(max_length=6)