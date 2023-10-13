from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


# Using google authentitcation to access google sheets data while using Django's built in authentication for user login could be a feasible approach.
# A user a user logs in using Django's authentication, but when they want to access their Google Sheets data, they authenticate with Google. Their access and refresh tokens can be stored in the user model, allowing the application to fetch data from Google Sheets on their behalf.

# Path: market/models.py

# from django.contrib.auth.models import User
# from django.db import models


# class GoogleAuth(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     access_token = models.CharField(max_length=250)
#     refresh_token = models.CharField(max_length=250)
#     expires_in = models.PositiveIntegerField()
#     token_type = models.CharField(max_length=250)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
