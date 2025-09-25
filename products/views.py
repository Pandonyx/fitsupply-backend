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
    GET: Publicly readable list of products.
    POST, PUT, DELETE: Restricted to admin users.
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # Admin users can see all products, others see only active ones
        if self.request.user and self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(is_active=True)

    def get_permissions(self):
        """Set custom permissions for different actions."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        else: # list, retrieve
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()