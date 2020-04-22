from django.db import models
import sqlite3


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
    image = models.CharField(max_length=200, default="https://sneakertown.kz/bitrix/templates/styleshop_club/components/bitrix/catalog.top/catalog/images/no_photo.png")
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


# STATUS_CHOICES=(
#     ("Started", "Started"),
#     ("Abandoned", "Abandoned"),
#     ("Finished", "Finished")
# )
#
#
# class Order(models.Model):
#     # add user
#     # add address
#     order_id = models.CharField(max_length=120, default='none', unique=True)
#     cart = models.ForeignKey(Cart)
#     status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True)
#
#     def __unicode__(self):
#         return self.order_id
#
#     # def __str__(self):
#     #     return '{}: {}'.format(self.id,
#     #                            self.name)
#     #
#     # def to_json(self):
#     #     return {
#     #         'id': self.id,
#     #         'name': self.name
#     #     }