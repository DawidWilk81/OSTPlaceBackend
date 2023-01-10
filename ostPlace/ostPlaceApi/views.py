from django.contrib.auth.models import User
from rest_framework import viewsets, status
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from .models import Song, Tag, BasketOST, UserAccount
from .serializers import SongSerializer, TagsSerializer, TagsFilterSerializer,\
    SongUpdateSerializer, SongTagUpdateSerializer, BasketOSTSerializer, UserUpdateSerializer,\
    GetBasketOSTSerializer, GetUserAccountSerializer, UserAccountUpdateSerializer,\
    UserPasswordChangeSerializer, ActivateUserSerializer, ChangeEmailSerializer
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
from .email import change_email


# USER ACCOUNT SERIALIZERS
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)


class UserCheckViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def post(self):
        response = {'message': 'User avatar has been changed'}
        return Response(response, status=status.HTTP_200_OK)


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-id')
    serializer_class = GetUserAccountSerializer
    authentication_classes = (TokenAuthentication,)

    @csrf_exempt
    def get_queryset(self, *args, **kwargs):
        acc = UserAccount.objects.filter(user=self.request.user.id)
        return acc


class GetSettingsAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-id')
    serializer_class = UserAccountUpdateSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        account = UserAccount.objects.filter(user=user)
        return account


class ChangeUserAccountAvatarViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all().order_by('-id')
    serializer_class = UserAccountUpdateSerializer
    authentication_classes = (TokenAuthentication,)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        print('----------------started')
        avatar = self.request.data['avatar']
        user = self.request.user
        account = UserAccount.objects.get(user=user)
        account.avatar.delete()
        account.avatar = avatar
        account.save()
        response = {'message': 'User avatar has been changed'}
        return Response(response, status=status.HTTP_200_OK)


class ChangeUserPasswordViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserPasswordChangeSerializer
    authentication_classes = (TokenAuthentication,)

    @csrf_exempt
    def update(self, request, *args, **kwargs):
        print('----------------started')
        user = self.request.user
        print('USER:', user)
        print(self.request.data['replacePassword,'])
        print(self.request.data)
        oldPassword = self.request.data['oldPassword']
        newPassword = self.request.data['replacePassword,']

        # VALIDATE SIZE
        if len(newPassword) > 30 or newPassword == oldPassword:
            response = {'message': 'PASSWORD == OLDPASSWORD OR > 30 '}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        elif oldPassword != newPassword and len(newPassword) <= 30:
            user.set_password(newPassword)
            user.save()
            response = {'message': 'User avatar has been changed'}
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
        avatar = self.request.data['avatar']
        account = UserAccount.objects.get(user=user)
        print(account.avatar.path)
        os.remove(account.avatar.path)
        account.avatar = avatar
        account.save()
        # return account
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

    def update(self, request, *args, **kwargs):
        # GET UPDATE REQUIRED VALUES
        author = self.request.user
        ost_pk = self.request.GET.get('primary')
        price = self.request.data['price']
        title = self.request.data['title']
        desc = self.request.data['desc']
        song = get_object_or_404(Song.objects.filter(pk=ost_pk))

        if song.author == author:
            song.title = title
            song.price = price
            song.desc = desc
            song.ost = song.ost
            print('selfOST', self.request.data)
            song.cover = song.cover
            # UPDATE REQUEST !--------------
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
            song.save()
            # print(song)
            response = {'message': 'OST has been updated in database'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You fucked up something Johnny'}
            return Response(response, status=status.HTTP_200_OK)


class SongFilterViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        tags = self.request.GET.get('tags')
        print('TAGS::', tags)
        check = tags.split(',')
        queryCheck = []
        for i in range(len(check)):
            x = get_object_or_404(Tag.objects.filter(name=check[i]))
            queryCheck.append(int(x.id))
            print(Song.objects.filter(tags__in=queryCheck))
        return Song.objects.filter(tags__in=queryCheck, status=True).distinct()


# GET SPECIFIC OST VIEWSET
class GetOSTViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)


class GetUnloggedOSTViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')[:5]
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.filter(status=True).order_by('-id')


# GET OST PAGINATED
class OSTSPaginateViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Song.objects.filter(status=True).order_by('-id')
    #     paginated = Paginator(OSTS, 10)
    #     print(paginated)
    #     page_number = self.request.GET.get('pageNum')
    #     print(page_number)
    #     page_array = paginated.get_page(page_number)
    #     print(page_array)
    #
    #     return page_array


# OSTS OWNED BY self user
class GetMyOSTSViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('-id')
    serializer_class = SongSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        return Song.objects.filter(author=user)

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
        print('ost Params', ostId)
        ost = get_object_or_404(Song.objects.filter(id=ostId))
        print('ost GET', ost.id)
        buyer = self.request.user
        print('i buy: ', buyer)
        try:
            BasketOST.objects.get(OST=ost, buyer=self.request.user)
            response = {'message': 'You have already added that'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            BasketOST.objects.create(OST=ost, buyer=self.request.user)
            response = {'message': 'Added OST into basket'}
            return Response(response, status=status.HTTP_200_OK)


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
            x = stripe.Product.search(
                query="name:'{}  -OST'".format(getted[i])
            )
            lineItemsDict.append({'quantity': 1, 'price': x.data[0]['default_price']})
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
    # TODO: fill me in
    print("---------Fulfilling order----------------")

    print('Session: ', session)
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
        stripe.Customer.create_balance_transaction(
            str(stripe_customer.data[0].id),
            amount=int(((OST.price * 100) * 0.95) - 60),
            currency='usd',
        )
        user = UserAccount.objects.get(user=OST.author)
        user.balance += OST.price
        user.save()
        customer = User.objects.get(username=session.customer_details.name)
        #Update user balance

        print(customer.username)
        OST.author = customer
        print('OST-Author: ', OST.author)
        OST.status = False
        OST.save()
    basket = BasketOST.objects.filter(buyer=customer)
    basket.delete()
        # albo usuń to gówno i mu wyślij


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
            # Kupione już to chce otrzymac na 100% jakieś powiadomienie, że kupione- send to notification mejdej
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
        try:
            user = User.objects.get(email=email)
            print(user)
            response = {'message': 'email Checked message and user exist'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'message': 'email is free to use'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


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

