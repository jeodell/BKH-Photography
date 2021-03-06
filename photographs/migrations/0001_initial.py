# Generated by Django 3.0.8 on 2020-08-21 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('cover', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Photograph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('img', models.ImageField(upload_to='images/portfolio')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='photographs.Album')),
            ],
        ),
    ]
