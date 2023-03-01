from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, SongSendViewSet, TagsViewSet, TagsFilterViewSet, \
    OSTSPaginateViewSet, GetMyOSTSViewSet, GetOSTViewSet, SongUpdateViewSet,\
    SongTagUpdateViewSet, SongFilterViewSet, GetUnloggedOSTViewSet, BasketOstViewSet,\
    UserPasswordViewSet, GetBasketOstViewSet, stripe_config, StripeCheckoutSessionViewSet,\
    my_webhook_view, UserAccountViewSet, OtherUserAccountViewSet, ChangeUserPasswordViewSet,\
    GetSettingsAccountViewSet, UserAvatarViewSet, ActivateAccount, CheckEmail, allSongsViewSet,\
    SendChangeEmail, ChangeEmailAlreadyViewSet, OSTSPaginateSearchViewSet

from rest_framework.authtoken.views import ObtainAuthToken

router = routers.DefaultRouter()
router.register('users', UserViewSet)

router.register('changePassword', UserPasswordViewSet)
router.register('ostAdd', SongSendViewSet)
router.register('myOSTS', GetMyOSTSViewSet)
router.register('getOST', GetOSTViewSet)
router.register('getUnloggedOSTS', GetUnloggedOSTViewSet)
router.register('deleteOST', GetMyOSTSViewSet)
router.register('filterOST', SongFilterViewSet)
router.register('updateOST', SongUpdateViewSet)
router.register('updateTagsOST', SongTagUpdateViewSet)
router.register('tags', TagsViewSet)
router.register('tagsFilter', TagsFilterViewSet)
router.register('ostPaginate', OSTSPaginateViewSet)
router.register('ostSearch', OSTSPaginateSearchViewSet)
router.register('allOSTS', allSongsViewSet)
router.register('userBasket', BasketOstViewSet)
router.register('getUserBasket', GetBasketOstViewSet)
router.register('getSettingAccount', GetSettingsAccountViewSet)
router.register('setUserAvatar', UserAvatarViewSet)
router.register('setUserPassword', ChangeUserPasswordViewSet)
router.register('activateAccount', ActivateAccount)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', ObtainAuthToken.as_view()),
    path('userAccount/', UserAccountViewSet.as_view({'get': 'list'})),
    path('otherUserAccount/', OtherUserAccountViewSet.as_view({'get': 'list'})),
    path('activateAccount/', ActivateAccount.as_view({'get': 'list'})),
    path('sendChangeEmail/', SendChangeEmail.as_view({'get': 'list'})),
    path('ChangeEmailViewSet/', ChangeEmailAlreadyViewSet.as_view({'get': 'list'})),
    path('checkEmail/', CheckEmail.as_view({'get': 'list'})),

    # STRIPE API
    path('stripeConf/', stripe_config),
    path('create-checkout-session/', StripeCheckoutSessionViewSet.as_view(), name='createCheckoutSession'),
    path('my_webhook_view/', my_webhook_view),
]
