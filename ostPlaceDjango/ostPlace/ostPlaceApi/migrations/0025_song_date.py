# Generated by Django 4.0.5 on 2022-10-14 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ostPlaceApi', '0024_alter_song_cover_alter_song_ost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]