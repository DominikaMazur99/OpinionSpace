from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings
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


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    authors = models.CharField(max_length=200)
    year = models.IntegerField(null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dislikes')

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.TextField()
    data_added = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-data_added']

    def __str__(self):
        return self.content


