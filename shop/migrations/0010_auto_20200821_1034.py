# Generated by Django 3.0.8 on 2020-08-21 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_address_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]
