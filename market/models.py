from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


'''
Using Google authentication just for accessing Google Sheets data while using Django's built-in authentication for user login could be a feasible approach.

a user logs in using Django's authentication, but when they want to access their Google Sheets data, they authenticate with Google. Their access and refresh tokens can be stored in the user model, allowing the application to fetch data from Google Sheets on their behalf.
'''
