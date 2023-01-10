from django.contrib import admin
from .models import Song, Tag, BasketOST, UserAccount
# Register your models here.

admin.site.register(Tag)
admin.site.register(Song)
admin.site.register(BasketOST)
admin.site.register(UserAccount)

