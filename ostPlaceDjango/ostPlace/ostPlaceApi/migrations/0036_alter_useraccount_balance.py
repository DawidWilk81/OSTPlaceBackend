# Generated by Django 4.1 on 2022-11-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ostPlaceApi', '0035_alter_useraccount_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
