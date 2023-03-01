# Generated by Django 4.1 on 2022-12-06 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ostPlaceApi', '0037_alter_song_price_alter_useraccount_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
