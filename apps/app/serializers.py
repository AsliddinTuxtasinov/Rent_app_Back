
from rest_framework import serializers
from .models import *


class ProTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id','name','product','format','price']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name']


class ClientSerializer(serializers.ModelSerializer):
    # debt_product = serializers.ReadOnlyField()
    # debt_product = serializers.ReadOnlyField()
    class Meta:
        model = Client
        fields = ['id','name','passport','phone','desc','transactions']
        # def debt_product(self, obj):
        #     count_out = obj.outcome.all().aggregate(Sum('count'))['count__sum'] or 0
        #     count_in = obj.income.all().aggregate(Sum('count'))['count__sum'] or 0
        #     return count_in - count_out
    
class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ['id','client','client_name','date']
        # def to_representation(self, instance):
        #     representation = super().to_representation(instance)
        #     representation['debt_product'] = ClientSerializer(instance=instance.debt_product).data
        #     return representation


class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ['id','rent','rent_name','client','client_name','product','product_name','count','price','date','total']
        # depth=1


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','pay_type','rent','rent_name','client','client_name','product','product_name','count','pay','day','date','total',]