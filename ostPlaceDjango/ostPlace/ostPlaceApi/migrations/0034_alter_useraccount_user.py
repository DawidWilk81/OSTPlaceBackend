# Generated by Django 4.1 on 2022-11-15 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ostPlaceApi', '0033_useraccount_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]