# Generated by Django 4.0.5 on 2022-09-23 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ostPlaceApi', '0008_alter_song_cover_alter_song_ost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='cover',
            field=models.ImageField(default=None, upload_to='cover'),
        ),
        migrations.AlterField(
            model_name='song',
            name='ost',
            field=models.FileField(upload_to='ost'),
        ),
    ]