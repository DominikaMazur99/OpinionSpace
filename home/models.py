from django.core.validators import MinLengthValidator
from django.db import models
from django import forms


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.username

class UserDetail(models.Model):
    zipcode = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=200)
    def __str__(self):
        return self.username


