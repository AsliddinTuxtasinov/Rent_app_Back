from django_filters import rest_framework as filters
from apps.app.models import *
from django.db.models import  fields
from django.db.models import F, Q, Sum, ExpressionWrapper



class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name']


class ProductTypeFilter(filters.FilterSet):
    class Meta:
        model = ProductType
        fields = ['name','product','format']

class ClientFilter(filters.FilterSet):
    class Meta:
        model = Client
        fields = ['name','passport','phone']



class OutcomeFilter(filters.FilterSet):
    class Meta:
        model = Outcome
        fields = ['product','date']


class IncomeFilter(filters.FilterSet):
    class Meta:
        model = Income
        fields = ['product','date']
        
        

class PaymentsFilter(filters.FilterSet):
    class Meta:
        model = Payments
        fields = ['pay_type','product','date']