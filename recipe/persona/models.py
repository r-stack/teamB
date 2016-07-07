from __future__ import unicode_literals

from django.db import models

class TwitterUser(models.Model):
    account_name = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    ingredients = models.TextField(max_length=512)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


