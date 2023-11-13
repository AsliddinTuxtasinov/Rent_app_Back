from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import *
from apps.app.views import *
from .views import *

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('director', DirectorViewset, basename='director')
router.register('user', UserViewset, basename='user')


router.register('protype', ProTypeViewset, basename='protype')
router.register('product', ProductViewset, basename='product')
router.register('client', ClientViewset, basename='client')
router.register('rent', RentViewset, basename='rent')
router.register('outcome', OutcomeViewset, basename='outcome')
router.register('income', IncomeViewset, basename='income')

urlpatterns = [
    path('', include(router.urls)),
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)