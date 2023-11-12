from django.shortcuts import render

# Create your views here.

from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet


class ProTypeViewset(ModelViewSet):
    queryset = ProductType.objects.all().order_by('-id')
    serializer_class = ProTypeSerializer
    search_fields = ['name']


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    search_fields = ['name']


class ClientViewset(ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    search_fields = ['name']


class RentViewset(ModelViewSet):
    queryset = Rent.objects.all().order_by('-id')
    serializer_class = RentSerializer
    search_fields = ['name']


class IncomeViewset(ModelViewSet):
    queryset = Income.objects.all().order_by('-id')
    serializer_class = IncomeSerializer
    
class OutcomeViewset(ModelViewSet):
    queryset = Outcome.objects.all().order_by('-id')
    serializer_class = OutcomeSerializer