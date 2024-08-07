from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, WriteTransactionSerializer, ReadTransactionSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from .permissions import IsAdminOrReadOnly, AllowlistPermission

class CurrencyModelViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly,]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None # You order him not to paginate this endpoint


class CategoryModelViewSet(ModelViewSet):
    permission_classes = [AllowlistPermission,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def get_queryset(self): # This make reflection of the user that is alive or taking the action 
    #     return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer): # This make reflection of the user that is alive or taking the action 
        serializer.save(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend] # Filters
    search_fields = ['amount', 'description']               # Filter by specifing fields
    ordering_fields = ['amount']             # Ordering.
    filterset_fields = ["currency__code",]

    # Here you specify the transactions of a specific user when you insert his token
    def get_queryset(self):
       return  Transaction.objects.select_related("currency", "category", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer

    def perform_create(self, serializer): # This make reflection of the user that is alive or taking the action 
        serializer.save(user=self.request.user)