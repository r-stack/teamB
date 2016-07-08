from __future__ import unicode_literals

from django.db import models

class TwitterUser(models.Model):
    account_id = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Tweet(models.Model):
    twitter_user = models.ForeignKey('TwitterUser', null=True)
    tweet_id = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Recipe(models.Model):
    title = models.CharField(max_length=128)
    recipe_id = models.CharField(max_length=128)
    recipe_url = models.CharField(max_length=512)
    food_image_url = models.CharField(max_length=512)
    recipe_material = models.TextField(max_length=512)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


