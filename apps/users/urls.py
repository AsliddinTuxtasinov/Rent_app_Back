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
router.register('manager', ManagerViewset, basename='manager')
router.register('user', UserViewset, basename='user')

router.register('protypes', ProTypeViewset, basename='protype')
router.register('products', ProductViewset, basename='product')
router.register('clients', ClientViewset, basename='client')
router.register('outcomes', OutcomeViewset, basename='outcome')
router.register('incomes', IncomeViewset, basename='income')
router.register('payments', PaymentsViewset, basename='payments')

# router.register('usersme', UserMeViewSet, basename='userme')


urlpatterns = [
    path('', include(router.urls)),
    path('auth-token', obtain_auth_token, name='api_token_auth'),
    path('users/me', UserMeView.as_view())
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
