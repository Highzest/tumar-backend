from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include, reverse_lazy
from django.views.generic.base import RedirectView
from rest_auth.registration.views import SocialAccountListView, SocialAccountDisconnectView
from rest_framework.routers import DefaultRouter

from .animals.views import FarmViewSet, GeolocationAnimalViewSet, AnimalFarmViewSet, GetAnimalPathView, \
    MachineryFarmViewSet, EventAnimalViewSet, LatestGroupedGeolocationsView, CadastreFarmViewSet, MyFarmView, \
    SearchCadastreView, SimpleGroupedGeolocationsView
from .users.views import UserViewSet, UserCreateViewSet, CustomAuthToken, FacebookLogin, GoogleLogin, \
    CustomVerificationViewSet, SocialAccountExtraView
from .indicators.views import LatestIndicatorsView, RequestIndicatorsView

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
router.register(r'farms', FarmViewSet)
router.register(r'animals', AnimalFarmViewSet, basename='Animal')
router.register(r'geolocations', GeolocationAnimalViewSet)
router.register(r'machinery', MachineryFarmViewSet)
router.register(r'events', EventAnimalViewSet)
router.register(r'cadastres', CadastreFarmViewSet)

sms_router = DefaultRouter(trailing_slash=False)

sms_router.register('phone', CustomVerificationViewSet, basename='phone')
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),

    # Custom API endpoints
    path('api/v1/', include([path('get-path/', GetAnimalPathView.as_view(), name='get_path'),
                             path('latest-geolocs/', SimpleGroupedGeolocationsView.as_view(),
                                  name='latest_grouped_geolocations'),
                             path('users/social-account-has-phone-number/', SocialAccountExtraView.as_view()),
                             path('cadastres/search-cadastre/', SearchCadastreView.as_view()),
                             path('myfarm/', MyFarmView.as_view()),
                             path('indicators/latest/', LatestIndicatorsView.as_view()),
                             path('indicators/request/', RequestIndicatorsView.as_view()),
                             ] + router.urls + sms_router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # django-rest-auth
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='ggl_login'),
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('socialaccounts/', SocialAccountListView.as_view(), name='social_account_list'),
    path('socialaccounts/<int:pk>/disconnect/', SocialAccountDisconnectView.as_view(),
         name='social_account_disconnect'),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

    # If no prefix is given, use the default language
    prefix_default_language=False
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
