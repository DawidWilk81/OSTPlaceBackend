# Generated by Django 4.0.5 on 2022-10-21 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ostPlaceApi', '0027_basketost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketost',
            name='OST',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ostPlaceApi.song'),
        ),
        migrations.AlterField(
            model_name='basketost',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]