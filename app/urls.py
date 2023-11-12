from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

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