from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.
    Includes nested product details for a richer API response.
    """
    product = ProductSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'subtotal', 'added_at']

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    Includes nested cart items and calculates the total price of the cart.
    """
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    Includes nested product details.
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_time', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    Includes nested order items for a complete order view.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField() # Display username instead of ID

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_number', 'status', 'total_amount', 'items', 'shipping_address', 'billing_address', 'payment_method', 'created_at', 'updated_at']