# Generated by Django 3.0.10 on 2020-09-22 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatars/avatar.png', upload_to='media/avatars/'),
        ),
    ]
