# Generated by Django 3.0.10 on 2020-09-25 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.CharField(blank=True, db_index=True, max_length=200)),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('bio', models.TextField(default='No bio data', max_length=400)),
                ('gender', models.CharField(choices=[('NONE', 'none'), ('MALE', 'male'), ('FEMALE', 'female')], default='NONE', max_length=6)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('avatar', models.ImageField(default='avatars/avatar.png', upload_to='media/avatars/')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('favourite', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
