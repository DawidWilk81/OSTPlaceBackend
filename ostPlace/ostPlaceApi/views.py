from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .serializers import UserSerializer
from django.core import serializers
from rest_framework.authentication import TokenAuthentication
from .models import Song, Tag, BasketOST, UserAccount, FreestyleRoom
from .serializers import SongSerializer, TagsSerializer, TagsFilterSerializer,\
    SongUpdateSerializer, SongTagUpdateSerializer, BasketOSTSerializer, UserUpdateSerializer,\
    GetBasketOSTSerializer, GetUserAccountSerializer, UserAccountUpdateSerializer,\
    UserPasswordChangeSerializer, ActivateUserSerializer, ChangeEmailSerializer,\
    SongCheckSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
import os
import stripe
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.core.paginator import Paginator
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from .email import change_email, sendBoughtOST
from django.contrib.auth import authenticate


# USER ACCOUNT SERIALIZERS
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-id')
    serializer_class = GetUserAccountSerializer
    authentication_classes = (TokenAuthentication,)

    @csrf_exempt
    def get_queryset(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        acc = UserAccount.objects.filter(user=self.request.user.id)
        customer = stripe.Customer.search(query="name:'{}'".format(self.request.user.username))
        print("Customer:", customer)
        if customer.data:
            balance = customer.data[0].balance
            acc.balance = balance
        else:
            acc.balance = 0
        return acc


# Viewset for game rooms
class RoomViewSet(viewsets.ModelViewSet):
    queryset = FreestyleRoom.objects.all().order_by('-id')
    serializer_class = RoomSerializer
    authentication_classes = (TokenAuthentication,)


class GetSettingsAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-id')
    serializer_class = UserAccountUpdateSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        account = UserAccount.objects.filter(user=user)
        return account


# class ChangeUserAccountAvatarViewSet(viewsets.ModelViewSet):
#     queryset = UserAccount.objects.all().order_by('-id')
#     serializer_class = UserAccountUpdateSerializer
#     authentication_classes = (TokenAuthentication,)
#
#     @csrf_exempt
#     def update(self, request, *args, **kwargs):
#         print('----------------started')
#         avatar = self.request.data['avatar']
#         user = self.request.user
#         account = UserAccount.objects.get(user=user)
#         print(account.avatar)
#         print('av', avatar)
#         if 'OSTPlaceDefault.png' not in account.avatar:
#             account.avatar.delete()
#         account.avatar = avatar
#         account.save()
#         response = {'message': 'User avatar has been changed'}
#         return Response(response, status=status.HTTP_200_OK)


class ChangeUserPasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserPasswordChangeSerializer
    authentication_classes = (TokenAuthentication,)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        print('----------------started')
        print(self.request.data['replacePassword,'])
        print('selfUser:', self.request.user)

        oldPassword = self.request.data['password']
        newPassword = self.request.data['replacePassword,']
        print('oldPassword')
        # Get the user instance
        user = User.objects.get(pk=self.request.user.id)
        print('USER:', user)

        # VALIDATE SIZE
        if len(newPassword) > 30 or newPassword == oldPassword:
            response = {'message': 'PASSWORD == OLDPASSWORD OR > 30 '}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif oldPassword != newPassword and len(newPassword) <= 30:
            user.password = newPassword
            user.save()
            print(user.password)
            response = {'message': 'User password has been changed'}
            return Response(response, status=status.HTTP_200_OK)


# USER AVATAR
class UserAvatarViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-id')
    serializer_class = GetUserAccountSerializer
    authentication_classes = (TokenAuthentication,)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        user = self.request.user.id
        print(user)
        account = UserAccount.objects.get(user=user)
        print(account.avatar.path)
        if os.path.exists(account.avatar.path):
            if "OSTPlaceDefault.png" in account.avatar.path:
                pass
            else:
                os.remove(account.avatar.path)
        else:
            pass
        account.avatar = self.request.data['avatar']
        account.save()
        response = {'message': 'User avatar has been changed'}
        return Response(response, status=status.HTTP_200_OK)


class OtherUserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-id')
    serializer_class = GetUserAccountSerializer
    authentication_classes = (TokenAuthentication,)

    @csrf_exempt
    def get_queryset(self, *args, **kwargs):
        username = self.request.GET.get('username')
        user = User.objects.get(username=username)
        print(user.id)
        acc = UserAccount.objects.filter(user=user.id)
        return acc


class UserPasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserUpdateSerializer
    authentication_classes = (TokenAuthentication,)


# TAGS VIEWS
class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class TagsFilterViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsFilterSerializer

    def get_queryset(self):
        search_call = self.request.GET.get('search')
        search_call = search_call.lower()
        return Tag.objects.filter(name__startswith=search_call.capitalize())


# API OSTS VIEWS
# SEND NEW OST VIEWSET
class SongSendViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)

    def create(self, request, **kwargs):

        # GET POST REQUIRED VALUES
        title = self.request.data['title']
        cover = self.request.data['cover']
        ost = self.request.data['ost']
        desc = self.request.data['desc']
        price = self.request.data['price']
        choosed_tags = self.request.data['tags']
        author = self.request.user
        print(self.request.data['cover'])
        # SPLIT TAGS VALUES
        taags = choosed_tags.split(',')
        print(author)

        # CREATE REQUEST
        OST = Song.objects.create(author=author, title=title, cover=cover, ost=ost, desc=desc, price=price)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.Product.create(
            name=title + ' -OST',
            description=desc,
            default_price_data={
                "unit_amount": int(price) * 100,
                "currency": "usd",
            },
            expand=["default_price"],
        )
        for i in range(len(taags)):
            # CHECK TAGS NUMBER
            if len(taags) >= 5:
                print('too many tags man')
                response = {'message': 'Something is weird i can feel it'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            # GO WITH IT
            let_var = get_object_or_404(Tag.objects.filter(name=str(taags[i])))
            taags[i] = let_var
            print(taags)
        OST.tags.set(taags)
        response = {'message': 'Added OST into database'}
        return Response(response, status=status.HTTP_200_OK)


# UPDATE OST VIEWSET
class SongUpdateViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongUpdateSerializer
    authentication_classes = (TokenAuthentication,)

    def update(self, request, *args, **kwargs):

        # GET UPDATE REQUIRED DATA
        author = self.request.user
        ost_pk = self.request.GET.get('primary')
        price = self.request.data['price']
        title = self.request.data['title']
        desc = self.request.data['desc']
        song = get_object_or_404(Song.objects.filter(pk=ost_pk))

        if song.author == author:
            song.price = price
            song.desc = desc
            song.ost = song.ost
            print('selfOST', self.request.data)
            song.cover = song.cover
            # UPDATE REQUEST !--------------
            stripe.api_key = settings.STRIPE_SECRET_KEY
            print(song.title)
            product = stripe.Product.search(
                query="name:'{} -OST'".format(song.title)
            )
            print('BEFORE', product)
            # ZMIANA PRODUCT TITLE, JAK ZMIENIASZ TYTUL W UPDATE
            print('WHATT:', product.data[0])
            if 'title' in self.request.data:
                stripe.Product.modify(
                    product.data[0]['id'],
                    name=title + ' -OST'
                )
                song.title = title

            # NADPISANIE COVER
            if 'cover' in self.request.data:
                song.cover.delete()
                cover = self.request.data['cover']
                song.cover = cover

            # NADPISANIE OST
            if 'ost' in self.request.data:
                song.ost.delete()
                print('FirstOST', song.ost)
                song.ost = self.request.data['ost']
                print('LastOST', song.ost)
            # ZMIANA PRICE
            if 'price' in self.request.data:
                # GET THE PRODUCT

                print(product)
                # CREATE PRICE
                stripe.Price.create(
                    product=product.data[0]['id'],
                    unit_amount=int(song.price) * 100,
                    currency="usd",
                )
                # GET PRICES LIST TO GET ID OF LAST CREATED
                prices = stripe.Price.list(limit=2, product=product.data[0]['id'])
                print(prices)
                print("added", prices.data[0]['id'])

                # CHANGE PRODUCT DEFAULT PRICE
                stripe.Product.modify(
                    product.data[0]['id'],
                    default_price=prices.data[0]['id']
                )

                # ARCHIVE OLD PRICE
                stripe.Price.modify(
                    prices.data[1]['id'],
                    active=False
                )
            song.save()
            # print(song)
            # UPDATE STRIPE PRICE CAUSE YOU ONLY UPDATE API DATABASE

            response = {'message': 'OST has been updated in database'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You fucked up something Johnny'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# GET SPECIFIC OST VIEWSET
class GetOSTViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)


class GetUnloggedOSTViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')[:9]
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.filter(status=True).order_by('-id')[:9]


class allSongsViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongCheckSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Song.objects.filter().order_by('-id')


# GET OST PAGINATED
class OSTSPaginateViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        # Get sortBy option
        sortBy = self.request.GET.get('sortBy')
        print('Sort By Option: ', sortBy)

        # GET pagination page
        pageNumber = self.request.GET.get('pageNum')
        print('PAGENumber:', pageNumber)
        objects = Song.objects.filter(status=True)
        print('sortByLen', len(sortBy))
        # MAKE OBJECT
        if len(sortBy) > 0:
            print('SORTING search pagination MAAAAN:')
            if 'Price Desc' in sortBy:
                print('sort by PRICE-DESC')
                objects = Song.objects.filter(status=True).order_by('-price')
            if 'Price Asc' in sortBy:
                print('sort by PRICE-ASC')
                objects = Song.objects.filter(status=True).order_by('price')
            if 'Date: older first' in sortBy:
                objects = Song.objects.filter(status=True).order_by('date')
            if 'Date: newer first' in sortBy:
                print('sort by DATE-ASC')
                objects = Song.objects.filter(status=True).order_by('-date')    

        # PAGINATE OBJECT
        paginatedObject = Paginator(objects, 9)
        page_array = paginatedObject.get_page(pageNumber) 

        return page_array

    @action(detail=False)
    def count(self, request):
        x = Song.objects.all().filter(status=True).count()
        print(x)
        response = JsonResponse(x, safe=False)
        return response


# CLICKED ON OST TAG
class SongFilterViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)

    @action(detail=False)
    def get_queryset(self):
        # GET THE TAGS

        tags = self.request.GET.get('tags')
        print('TAGS::', tags)
        print('TAGS::', type(tags))

        # GET THE PAGE PAGINATION NUMBER
        pageNumber = self.request.GET.get('pageNum')
        print('PAGENumber:', pageNumber)


        # Get sortBy option
        sortBy = self.request.GET.get('sortBy')
        print('Sort By Option: ', sortBy)

        # SPLIT THE TAGS
        queryCheck = []
        check = []
        objects = Song.objects.filter(status=True).order_by('-id')
        if tags:
            check = tags.split(',')
            # Make magic with tags(append queryCheck with tags that i got from tags id's)
            for i in range(len(check)):
                x = get_object_or_404(Tag.objects.filter(name=check[i]))
                queryCheck.append(int(x.id))
                print(Song.objects.filter(tags__in=queryCheck))

        print('TESTS:', queryCheck)
        print('TYPE:', type(queryCheck))
        print('len:', len(queryCheck))

        if not queryCheck:
            print('22')
            # Now sort the stuff
            if len(sortBy) > 0:
                if 'Price Desc' in sortBy:
                    print('sort by PRICE-DESC')
                    objects = Song.objects.filter(status=True).order_by('-price')
                if 'Price Asc' in sortBy:
                    print('sort by PRICE-ASC')
                    objects = Song.objects.filter(status=True).order_by('price')
                if 'Date: older first' in sortBy:
                    objects = Song.objects.filter(status=True).order_by('date')
                if 'Date: newer first' in sortBy:
                    print('sort by DATE-ASC')
                    objects = Song.objects.filter(status=True).order_by('-date')

            # Now return what you've done
            paginatedObject = Paginator(objects, 9)
            page_array = paginatedObject.get_page(pageNumber)
            return page_array

        elif queryCheck:
            print('11')
            objects = Song.objects.filter(tags__in=queryCheck, status=True).order_by('-id')
            if len(sortBy) > 0:
                print('SORTING search pagination MAAAAN:')
                if 'Price Desc' in sortBy:
                    print('sort by PRICE-DESC')
                    objects = Song.objects.filter(tags__in=queryCheck, status=True).order_by('-price')
                elif 'Price Asc' in sortBy:
                    print('sort by PRICE-ASC')
                    objects = Song.objects.filter(tags__in=queryCheck, status=True).order_by('price')
                elif 'Date: older first' in sortBy:
                    objects = Song.objects.filter(tags__in=queryCheck, status=True).order_by('date')
                elif 'Date: newer first' in sortBy:
                    print('sort by DATE-ASC')
                    objects = Song.objects.filter(tags__in=queryCheck, status=True).order_by('-date')
            paginatedObject = Paginator(objects, 9)
            page_array = paginatedObject.get_page(pageNumber)
            return page_array

    @action(detail=False)
    def count(self, request):
        tags = self.request.GET.get('tags')
        print('TAGS::', tags)
        print('TAGS::', type(tags))
        queryCheck = []

        # SPLIT THE TAGS
        check = []
        if tags:
            check = tags.split(',')

        # Make magic with tags(append queryCheck with tags that i got from tags id's)
        for i in range(len(check)):
            x = get_object_or_404(Tag.objects.filter(name=check[i]))
            queryCheck.append(int(x.id))
            print(Song.objects.filter(tags__in=queryCheck))

        print('QUERY', queryCheck)
        if queryCheck is not None or len(queryCheck) != 0:
            objects = Song.objects.filter(tags__in=queryCheck, status=True).count()
            response = JsonResponse(objects, safe=False)
            return response

        else:
            objects = Song.objects.filter(status=True).order_by('-id').count()
            response = JsonResponse(objects, safe=False)
            return response


# przemyślenia powojenne: settings: sprawdzanie hasła - zalogowany nie filtruje po tytule i jak nie ma tagów
# to jebla dostaje.

# Filter OSTS BY SIDE SEARCH ON HOME PAGE
class OSTSPaginateSearchViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        # GET THE VALUES FROM SEARCH
        tags = self.request.GET.get('tags')
        print('TAGS::', tags)

        title = self.request.GET.get('title')
        print('Looking for title::', title)

        priceFrom = self.request.GET.get('priceFrom')
        print('priceFrom::', priceFrom)

        priceTo = self.request.GET.get('priceTo')
        print('priceTo::', priceTo)

        # Get sortBy option
        sortBy = self.request.GET.get('sortBy')
        print('Sort By Option: ', sortBy)

        # GET THE PAGE PAGINATION NUMBER
        pageNumber = self.request.GET.get('pageNum')
        print('PAGENumber:', pageNumber)

        print('Get request was hiding:', self.request.GET)
        queryCheck = []

        # SPLIT THE TAGS
        check = []
        if len(tags) > 0:
            check = tags.split(',')

            # Make magic with tags(append queryCheck with tags that i got from tags id's)
            for i in range(len(check)):
                x = get_object_or_404(Tag.objects.filter(name=check[i]))
                queryCheck.append(int(x.id))
                print(Song.objects.filter(tags__in=queryCheck))

        print('TESTS:', queryCheck)
        print('TYPE:', type(queryCheck))
        print('len:', len(queryCheck))

        # QUERY CHECK = PROCESSED ARRAY OF TAGS
        # GOT NO TAGS:
        if len(queryCheck) == 0:
            if not title:
                print('EMPTY TITLE')
                print('sortBY: ')
                if len(sortBy) > 0:
                    if 'Price Desc' in sortBy:
                        print('sort by PRICE-DESC')
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo).order_by('-price').distinct()
                    if 'Price Asc' in sortBy:
                        print('sort by PRICE-ASC')
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo).order_by('price').distinct()
                    if 'Date: older first' in sortBy:
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo).order_by('date').distinct()
                    if 'Date: newer first' in sortBy:
                        print('sort by DATE-ASC')
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo).order_by('-date').distinct()
            if title:
                print('NOT EMPTY TITLE ')
                if len(sortBy) > 0:
                    print('SORTING search pagination MAAAAN:')
                    if 'Price Desc' in sortBy:
                        print('sort by PRICE-DESC')
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo,
                                                      title__icontains=title).order_by('-price').distinct()
                    if 'Price Asc' in sortBy:
                        print('sort by PRICE-ASC')
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo,
                                                      title__icontains=title).order_by('price').distinct()
                    if 'Date: older first' in sortBy:
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo,
                                                      title__icontains=title).order_by('date').distinct()
                    if 'Date: newer first' in sortBy:
                        print('sort by DATE-ASC')
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo,
                                                      title__icontains=title).order_by('-date').distinct()
                if not sortBy:
                    print('SORTING search pagination MAAAAN:')
                    objects = Song.objects.filter(status=True,
                                                  price__gte=priceFrom,
                                                  price__lte=priceTo,
                                                  ).order_by('-price')
                    if title:
                        print('sort by PRICE-DESC')
                        objects = Song.objects.filter(status=True,
                                                      price__gte=priceFrom,
                                                      price__lte=priceTo,
                                                      title__icontains=title).order_by('-price')

            paginatedObject = Paginator(objects, 9)
            page_array = paginatedObject.get_page(pageNumber)
            print('YOU WILL GET:', paginatedObject.object_list)

            return page_array

        # GOT TAGS IN REQUEST
        elif len(queryCheck) > 0:
            print('SEARCH: WITH TAGS')
            objects = Song.objects.filter(tags__in=queryCheck, status=True)
            if title:
                print('SEARCH WITH TAGS AND TITLE')
                if len(sortBy) > 0:
                    print('SORTING search pagination MAAAAN:')
                    objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                  price__gte=priceFrom, price__lte=priceTo,
                                                  title__icontains=title)
                    if 'Price Desc' in sortBy:
                        print('sort by PRICE-DESC')
                        objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                      price__gte=priceFrom, price__lte=priceTo,
                                                      title__icontains=title).order_by('-price').distinct()
                    if 'Price Asc' in sortBy:
                        print('sort by PRICE-ASC')
                        objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                      price__gte=priceFrom, price__lte=priceTo,
                                                      title__icontains=title).order_by('price').distinct()
                    if 'Date: older first' in sortBy:
                        objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                      price__gte=priceFrom, price__lte=priceTo,
                                                      title__icontains=title).order_by('date').distinct()
                    if 'Date: newer first' in sortBy:
                        print('sort by DATE-ASC')
                        objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                      price__gte=priceFrom, price__lte=priceTo,
                                                      title__icontains=title).order_by('-date').distinct()

            if not title:
                print('SEARCH WITH TAGS WITHOUT TITLE')
                objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                              price__gte=priceFrom, price__lte=priceTo).distinct()
                if 'Price Desc' in sortBy:
                    print('sort by PRICE-DESC')
                    objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                  price__gte=priceFrom,
                                                  price__lte=priceTo).order_by('-price').distinct()
                if 'Price Asc' in sortBy:
                    print('sort by PRICE-ASC')
                    objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                  price__gte=priceFrom,
                                                  price__lte=priceTo).order_by('price').distinct()
                if 'Date: older first' in sortBy:
                    objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                  price__gte=priceFrom,
                                                  price__lte=priceTo).order_by('date').distinct()
                if 'Date: newer first' in sortBy:
                    print('sort by DATE-ASC')
                    objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                                  price__gte=priceFrom,
                                                  price__lte=priceTo).order_by('-date').distinct()

            print('LEN OF SORTBY:', len(sortBy))

            paginatedObject = Paginator(objects, 9)
            page_array = paginatedObject.get_page(pageNumber)
            print(paginatedObject.object_list)
            return page_array

    @action(detail=False)
    def count(self, request):
        # GET THE VALUES FROM SEARCH
        tags = self.request.GET.get('tags')
        title = self.request.GET.get('title')
        priceFrom = self.request.GET.get('priceFrom')
        priceTo = self.request.GET.get('priceTo')

        print('TAGS::', tags)
        print('priceFrom::', priceFrom)
        print('priceTo::', priceTo)

        print('title::', title)

        # GET THE PAGE PAGINATION NUMBER
        pageNumber = self.request.GET.get('pageNum')
        print('PAGENumber:', pageNumber)
        print(self.request.GET)
        queryCheck = []

        # SPLIT THE TAGS
        check = []
        if len(tags) > 0:
            check = tags.split(',')

            # Make magic with tags(append queryCheck with tags that i got from tags id's)
            for i in range(len(check)):
                x = get_object_or_404(Tag.objects.filter(name=check[i]))
                queryCheck.append(int(x.id))
                print(Song.objects.filter(tags__in=queryCheck))

        print('TESTS:', queryCheck)
        print('TYPE:', type(queryCheck))
        print('len:', len(queryCheck))

        # QUERY CHECK = PROCESSED ARRAY OF TAGS
        # GOT TAGS:
        if len(queryCheck) == 0:
            print('COUNT: NO TAGS')
            print(title)
            if title:
                objects = Song.objects.filter(status=True,
                                              price__gte=priceFrom, price__lte=priceTo,
                                              title__icontains=title).distinct().count()
            if not title:
                objects = Song.objects.filter(status=True,
                                              price__gte=priceFrom, price__lte=priceTo).distinct().count()
            response = JsonResponse(objects, safe=False)
            return response

        # GOT NO TAGS IN REQUEST
        elif len(queryCheck) > 0:
            print('111')
            if title:
                objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                              price__gte=priceFrom, price__lte=priceTo,
                                              title__icontains=title).distinct().count()
            if not title:
                objects = Song.objects.filter(tags__in=queryCheck, status=True,
                                              price__gte=priceFrom, price__lte=priceTo).distinct().count()
            response = JsonResponse(objects, safe=False)
            return response


# OSTS OWNED BY self user
class GetMyOSTSViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        pageNum = self.request.GET.get('pageNum')
        print(pageNum)
        objects = Song.objects.filter(author=user).order_by('-id')
        paginatedObjects = Paginator(objects, 2)
        return paginatedObjects.get_page(pageNum)

    @action(detail=False)
    def count(self, request):
        user = self.request.user
        objects = Song.objects.filter(author=user).count()
        response = JsonResponse(objects, safe=False)
        return response

    def destroy(self, instance, pk=None):
        print('start')
        song_id = self.request.GET.get('primary')
        song = get_object_or_404(Song.objects.filter(id=self.request.GET.get('primary')))
        print('pobrano item z bazy')
        print('songAuthor', self.request.user.username)
        print('songAuthor2', song.author)
        if str(song.author) == str(self.request.user.username):
            print('author === author')
            print(os.path.isfile(song.ost.path))
            if song.ost.path:
                print('ost before: ', song.ost.path)
                os.remove(song.ost.path)
            print(os.path.isfile(song.cover.path))
            if song.cover.path:
                print('cover before: ', song.cover.path)
                os.remove(song.cover.path)
            song.delete()
            response = {'message': 'Removed OST from database'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'ERROR from database: U are retarded'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class SongTagUpdateViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongTagUpdateSerializer
    authentication_classes = (TokenAuthentication,)

    def update(self, request, **kwargs):
        # GET UPDATE REQUIRED VALUES
        song_id = self.request.data['id']
        print(song_id)
        print(kwargs)

        choosed_tags = self.request.data['tags']
        print(choosed_tags)
        author = self.request.user

        # SPLIT TAGS VALUES
        taags = choosed_tags.split(',')

        # UPDATE REQUEST !--------------
        song = get_object_or_404(Song.objects.filter(id=song_id))
        print('OST::', song)
        print(author)
        print(song)
        for i in range(len(taags)):
            # CHECK TAGS NUMBER
            if len(taags) >= 5:
                print('too many tags man')
                response = {'message': 'Something is weird i can feel it'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            # GO WITH IT
            print(" TAGSSS;", choosed_tags)
            let_var = get_object_or_404(Tag.objects.filter(name=str(taags[i])))
            print('let_VAR_ID: ', let_var.id)
            taags[i] = let_var
            print(taags)
        song.tags.set(taags)
        song.save()
        response = {'message': 'Added OST into database'}
        return Response(response, status=status.HTTP_200_OK)


class BasketOstViewSet(viewsets.ModelViewSet):
    queryset = BasketOST.objects.all().order_by('-id')
    serializer_class = BasketOSTSerializer
    authentication_classes = (TokenAuthentication,)

    def create(self, request):
        ostId = self.request.data['ostId']
        print('ost ID ordered from FrontEnd', ostId)
        ost = get_object_or_404(Song.objects.filter(id=ostId))
        print('ost GET', ost.id)
        buyer = self.request.user
        print('i buy: ', buyer)
        userBasket = BasketOST.objects.filter(buyer=buyer)
        try:
            BasketOST.objects.get(OST=ost, buyer=self.request.user)
            response = {'message': 'You have already added that'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            # HOW MUCH CAN MY BASKET HOLD, only 4?
            if len(userBasket) <= 4:
                BasketOST.objects.create(OST=ost, buyer=self.request.user)
                response = {'message': 'Added OST into basket'}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {'message': 'Your basket cant hold more than 4 items'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetBasketOstViewSet(viewsets.ModelViewSet):
    queryset = BasketOST.objects.select_related('OST').all()
    serializer_class = GetBasketOSTSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return BasketOST.objects.filter(buyer=self.request.user)


@action(detail=True, methods=['get'])
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripeConfig = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripeConfig, safe=False)


class StripeCheckoutSessionViewSet(APIView):
    def post(self, request, *args, **kwargs):
        lineItemsDict = []
        domain_url = 'http://localhost:4200/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        basket = self.request.data['products']
        print(basket)
        basket = basket.split(',')
        getted= Song.objects.filter(id__in=basket)
        customer = stripe.Customer.search(query="name:'{}'".format(self.request.user))
        print(customer)

        for i in range(len(getted)):
            # CHECK IF STATUS = TRUE
            print('PEENTLA', getted[i].status)
            if getted[i].status is not False:
                x = stripe.Product.search(
                    query="name:'{}  -OST'".format(getted[i])
                )
                lineItemsDict.append({'quantity': 1, 'price': x.data[0]['default_price']})
            elif getted[i].status is False:
                continue
        try:
            print('trey:', self.request.user)
            print('line_items: ', lineItemsDict)
            print('customer', customer.data[0].id)

            checkout_session = stripe.checkout.Session.create(
                line_items=lineItemsDict,
                mode='payment',
                success_url=domain_url + 'home/success/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'home/cancel/canceled=true',
                customer=customer.data[0].id,
            )
            # jak przekazywać to gówno po zakupie i by obaj nie kupili tego samego
            return JsonResponse(checkout_session.id, safe=False)
            # W MOMENCIE JAK BEDZIE SUCCESS TO PRZEKAŻ FLOTĘ DLA sprzedającego do portfela
        except:
            response = {'message': 'Something went wrong with your checkout session.'}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


endpoint_secret = 'whsec_e6f2677ed4d9d375f75273d788ef7be759b2f1e83163f67825300099eaf049c7'


def i_payed_for_it(session):
    # W MOMENCIE JAK PŁATNOŚĆ SIĘ UDAŁA TO:
    # TODO: Make it workin baby!
    # print("---------Fulfilling order----------------")
    # print('Session: ', session)
    customer = None
    line_items = stripe.checkout.Session.list_line_items(
        session.id, limit=5)
    print(line_items)
    for i in range(len(line_items)):
        print(line_items.data[i].description[:-5])
        # teraz wybierz id ktory wstawił ost
        OST = Song.objects.get(title=line_items.data[i].description[:-5])
        print('OST: ', OST)
        print('OST-Author: ', OST.author)

        stripe_customer = stripe.Customer.search(
            query="name:'{}'".format(OST.author)
        )
        print(stripe_customer)
        print("I {} will get {} dollars".format(stripe_customer, OST.price))

        # stripe.
        print(line_items.data[i].amount_total)

        # Put the money in the stripe bag - slowly
        stripe.Customer.create_balance_transaction(
            str(stripe_customer.data[0].id),
            # STRIPE WANT MONEY FOR FREEDOM - IT TAKES 2.9% AND 0.30 for transaction
            # And we are greedy so + 2.1 and 0.30
            amount=int(((OST.price * 100) * 0.95) - 60),
            currency='usd',
        )
        stripe_customer = stripe.Customer.search(
            query="name:'{}'".format(OST.author)
        )
        # Now put the money in user account in API
        user = UserAccount.objects.get(user=OST.author)
        print('balance:', int(stripe_customer.data[0].balance))
        user.balance = float(stripe_customer.data[0].balance/100)
        user.save()

        # Update user balance
        customer = User.objects.get(username=session.customer_details.name)
        print(customer.username)
        print('OST-Author: ', OST.author)

    print(customer)
    print('customerEMAIL::{}'.format(customer.email))
    sendBoughtOST(customer.email, customer.username, line_items)
    basket = BasketOST.objects.filter(buyer=customer)
    basket.delete()


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    print('PAYLOAD: ', payload)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    print('SIG_HEADER', sig_header)
    event = None

    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        if event['type'] == 'checkout.session.completed':
            # Bought so i want to get a notification or something like that, i guess.
            session = event['data']['object']
            # print(session)

            # Fulfill the purchase...
            i_payed_for_it(session)

    except ValueError as e:
        # Invalid payload
        print('ERROR: VALUE_ERROR', e)
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('ERROR(signatureVerificationError): ', e)
        return HttpResponse(status=400)

    # Passed signature verification
    return HttpResponse(status=200)


class ActivateAccount(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = ActivateUserSerializer

    def get_queryset(self, *args, **kwargs):
        try:
            token = self.request.GET.get('token')
            createdToken = Token.objects.get(key=token)

            if Token.objects.get(key=token) is not None:
                print(createdToken)
                user = User.objects.get(pk=createdToken.user_id)
                print(user)
                if user.is_active is False:
                    user.is_active = True
                    # STRIPE Create Account AFTER YOU VERIFY EMAIL
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    stripe.Customer.create(
                        name=str(user.username)
                    )
                    user.save()
                else:
                    pass

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None


class CheckEmail(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChangeEmailSerializer

    def post(self, request):
        email = self.request.data['email']
        print(email)
        user = User.objects.filter(email=email)
        if user:
            print(user)
            response = {'message': 'email Checked message and user exist'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if not user:
            response = {'message': 'email is free to use'}
            return Response(response, status=status.HTTP_200_OK)


class SendChangeEmail(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self, *args, **kwargs):
        token = Token.objects.get(user=self.request.user).key
        oldEmail = self.request.user.email
        email = self.request.GET.get('newEmail')

        print(email)
        print(oldEmail)
        return change_email(oldEmail, email, token, self.request.user.username)


class ChangeEmailAlreadyViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ChangeEmailSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self, *args, **kwargs):
        email = self.request.GET.get('newEmail')
        user = self.request.user
        if email != user.email:
            user.email = str(email)
            user.save()
            print(user.email)
        else:
            pass

