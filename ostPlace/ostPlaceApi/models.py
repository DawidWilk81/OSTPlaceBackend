import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def upload_avatar(instance, filname):
    return '/'.join(['avatars', str(instance.user), filname])


def upload_announcement_image(instance, filname):
    return '/'.join(['ostCover', str(instance.author), filname])


def upload_announcement_ost(instance, filname):
    return '/'.join(['ost', str(instance.author), filname])


class Tag(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=64, default='Buy this man')
    cover = models.ImageField(upload_to=upload_announcement_image, default=None)
    ost = models.FileField(upload_to=upload_announcement_ost)
    desc = models.CharField(max_length=124, default='Best banger on this site')
    price = models.FloatField(default=1)
    tags = models.ManyToManyField(Tag, related_name='tags')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.BooleanField(default=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author'
        )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ['ost']


class UserAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, related_name='profile')
    avatar = models.ImageField(upload_to=upload_avatar, default='OSTPlaceDefault.png')
    balance = models.FloatField(default=0)
    leaguePoints = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.user.username


class FreestyleRoom(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='roomUser', on_delete=models.CASCADE)
    admins = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='roomAdmin', on_delete=models.CASCADE)
    password = models.PositiveIntegerField(null=True, blank=True)
    slots = models.PositiveIntegerField(default=5, )
    title = models.CharField(max_length=128, default='Everyone are welcome')
    # Need at least that much LP
    requirement = models.PositiveIntegerField(default=0, )

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)


class BasketOST(models.Model):
    OST = models.ForeignKey(Song, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.buyer.username



