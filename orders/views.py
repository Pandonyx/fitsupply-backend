from django.db import transaction
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound

from .models import Cart, CartItem, Order, OrderItem, Product
from .serializers import CartSerializer, OrderSerializer, CartItemSerializer


class CartView(APIView):
    """
    Manages the user's shopping cart.
    - GET: Retrieve the current user's cart.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the user's cart."""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemView(APIView):
    """
    Manages items within a shopping cart.
    - POST: Add an item to the cart.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Add a product to the cart or update its quantity."""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            raise ValidationError({'product_id': 'This field is required.'})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound('Product not found.')

        if quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be a positive integer.'})

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    Manages a specific item in the cart.
    - PUT/PATCH: Update an item's quantity.
    - DELETE: Remove an item from the cart.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def get_queryset(self):
        """Ensure users can only affect their own cart items."""
        return CartItem.objects.filter(cart__user=self.request.user)

    def update(self, request, *args, **kwargs):
        quantity = int(request.data.get('quantity', 1))
        if quantity <= 0:
            # If quantity is zero or less, remove the item
            return self.destroy(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)


class ClearCartView(APIView):
    """
    Clears all items from the user's shopping cart.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Handles creating and viewing orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own orders."""
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Create an order from the user's cart."""
        cart = Cart.objects.filter(user=self.request.user).first()
        if not cart or not cart.items.exists():
            raise ValidationError("Your cart is empty.")

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Check for sufficient stock before creating the order
            for item in cart.items.all():
                if item.product.stock_quantity < item.quantity:
                    raise ValidationError(f"Not enough stock for {item.product.name}. Available: {item.product.stock_quantity}")

            # Calculate total amount
            total_amount = sum(item.product.price * item.quantity for item in cart.items.all())

            order = serializer.save(
                user=self.request.user,
                total_amount=total_amount
            )

            # Create order items and decrease product stock
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_at_time=cart_item.product.price
                )
                # Decrease stock
                product = cart_item.product
                product.stock_quantity -= cart_item.quantity
                product.save()

            # Clear the cart
            cart.items.all().delete()