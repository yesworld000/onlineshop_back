from django.db import models
import sqlite3

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}: {}'.format(self.id,
                               self.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    price = models.FloatField(default=0)
    image = models.CharField(max_length=200,
                             default="https://sneakertown.kz/bitrix/templates/styleshop_club/components/bitrix/catalog.top/catalog/images/no_photo.png")
    color = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=200, default='no left sizes')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.name,
                               self.description)

    def to_json(self):
        return {
            # 'id': self.id,
            'name': self.name,
            # 'description': self.description,
            'price': self.price,
            # 'image': self.image,
            'color': self.color,
            'size': self.size
        }


