# Generated by Django 4.0.5 on 2022-09-29 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ostPlaceApi', '0017_song_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='tags',
        ),
        migrations.AddField(
            model_name='song',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='ostPlaceApi.tag'),
        ),
    ]
