# Generated by Django 3.0.8 on 2020-08-30 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_auto_20200830_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.CharField(choices=[('5R', '15'), ('8R', '20'), ('11R', '30'), ('12S', '25'), ('16R', '40'), ('16S', '35'), ('18R', '50'), ('20R', '65')], default='5R', max_length=3),
        ),
    ]
