# Generated by Django 2.2.7 on 2019-12-28 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20191228_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='liked_projects',
            field=models.ManyToManyField(default=None, to='products.Product'),
        ),
    ]
