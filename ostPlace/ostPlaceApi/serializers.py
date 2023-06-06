from django.contrib.auth.models import User
from rest_framework import serializers, status
from .email import send_email
from django.core.mail import send_mail, BadHeaderError
from rest_framework.authtoken.models import Token
from .models import Song, Tag, BasketOST, UserAccount, FreestyleRoom
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response


class UserAccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserAccount
        fields = ['id', 'balance', 'user', 'avatar', 'leaguePoints']


class UserAccountUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ['id', 'balance', 'user', 'avatar']


class RoomSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserAccount
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = UserAccountSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'profile']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        print(validated_data['email'])
        user = User.objects.create_user(**validated_data)
        user.profile = UserAccount.objects.create(user=user, **profile)

        # Create token and send email
        Token.objects.create(user=user)
        send_email(str(validated_data['email']), urlsafe_base64_encode(force_bytes(user.id)), user.username)
        user.is_active = False
        user.save()
        return user


class GetUserAccountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserAccount
        fields = ['id', 'balance', 'user', 'avatar']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password']


class ActivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_active', 'username']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


# API SERIALIZERS
class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]


# TAGS SEARCH
class TagsFilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]


# SONG UPDATE
class SongSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Song
        fields = ["id", "title", "cover", "ost", "desc", "price", "tags", "author", "date", "status"]


class SongCheckSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Song
        fields = ["id", "title", "cover", "ost", "desc", "price", "tags", "author", "date", "status"]


# SONG UPDATE
class SongTagUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ["id", "tags"]


class SongUpdateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Song
        fields = ["id", "title", "desc", "price", "tags", "author", "ost"]


class BasketOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketOST
        fields = "__all__"


class GetBasketOSTSerializer(serializers.ModelSerializer):
    songOBJ = SongSerializer(source='OST')
    buyer = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = BasketOST
        fields = ["id", "buyer", "date", "OST", "songOBJ"]


class ChangeEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']



