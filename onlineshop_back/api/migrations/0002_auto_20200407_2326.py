# Generated by Django 3.0.4 on 2020-04-07 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.CharField(default='https://sneakertown.kz/bitrix/templates/styleshop_club/components/bitrix/catalog.top/catalog/images/no_photo.png', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(default='no left sizes', max_length=200),
        ),
    ]
