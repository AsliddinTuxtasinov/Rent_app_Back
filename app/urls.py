from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('protype', ProTypeViewset, basename='protype')
router.register('product', ProductViewset, basename='product')
router.register('client', ClientViewset, basename='client')
router.register('rent', RentViewset, basename='rent')
router.register('outcome', OutcomeViewset, basename='outcome')
router.register('income', IncomeViewset, basename='income')



urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)