# Generated by Django 4.0.5 on 2022-09-23 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ostPlaceApi', '0012_alter_song_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='title',
            field=models.CharField(default='Buy this man', max_length=64),
        ),
    ]