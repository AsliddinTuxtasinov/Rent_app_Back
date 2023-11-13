from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet

from apps.app.filters import *
from rest_framework import pagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter

class ClientPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    queryset = Client.objects.all()
    filterset_class = Client
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class RentPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    queryset = Rent.objects.all()
    filterset_class = Rent
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class IncomePagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    queryset = Income.objects.all()
    filterset_class = Income
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class OutcomePagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    queryset = Income.objects.all()
    filterset_class = Income
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


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
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ClientPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('name','passport','phone')
    # filterset_fields = ('status', )
    filterset_class = ClientFilter
    serializer_class = ClientSerializer


class RentViewset(ModelViewSet):
    queryset = Rent.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = RentPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('client','date')
    filterset_class = RentFilter
    serializer_class = RentSerializer



class OutcomeViewset(ModelViewSet):
    queryset = Outcome.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = OutcomePagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('client','product','count','price','date')
    # filterset_fields = ('status', )
    filterset_class = OutcomeFilter
    serializer_class = OutcomeSerializer


class IncomeViewset(ModelViewSet):
    queryset = Income.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = IncomePagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('client','product','count','price','date')
    # filterset_fields = ('status', )
    filterset_class = IncomeFilter
    serializer_class = IncomeSerializer
    
