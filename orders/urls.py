from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CartView,
    CartItemView,
    CartItemDetailView,
    ClearCartView,
    OrderViewSet
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/', CartItemView.as_view(), name='cart-add-item'),
    path('cart/items/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('cart/clear/', ClearCartView.as_view(), name='cart-clear'),
    path('', include(router.urls)),
]