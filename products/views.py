from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# Create your views here.
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing product categories.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing products.
    Provides `list` and `retrieve` actions.
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]