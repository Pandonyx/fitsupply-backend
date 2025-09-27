from django.db import transaction
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError, NotFound
from decimal import Decimal

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
    - Admin users can see all orders
    - Regular users can only see their own orders
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        """Return appropriate queryset based on user permissions."""
        if self.request.user.is_staff:
            # Admin can see all orders
            return Order.objects.all().select_related('user').prefetch_related('items__product').order_by('-created_at')
        else:
            # Regular users see only their orders
            return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items__product').order_by('-created_at')

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            # Admin can list/view/update all orders, users can only see their own
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            # Anyone authenticated can create orders
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            # Only admin can delete orders
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """List orders with proper permissions."""
        if not request.user.is_staff:
            # Regular users get their own orders
            return super().list(request, *args, **kwargs)
        else:
            # Admin gets all orders
            return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Create an order from submitted cart data."""
        submitted_items = self.request.data.get('items', [])
        
        if not submitted_items:
            raise ValidationError("No items provided for order.")

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Check for sufficient stock before creating the order
            total_amount = Decimal('0.00')
            
            for item_data in submitted_items:
                try:
                    product = Product.objects.get(id=item_data['product_id'])
                except Product.DoesNotExist:
                    raise ValidationError(f"Product with ID {item_data['product_id']} not found.")
                
                quantity = int(item_data['quantity'])
                
                if product.stock_quantity < quantity:
                    raise ValidationError(f"Not enough stock for {product.name}. Available: {product.stock_quantity}")
                
                total_amount += product.price * quantity

            # Create the order
            order = serializer.save(
                user=self.request.user,
                total_amount=total_amount
            )

            # Create order items and decrease product stock
            for item_data in submitted_items:
                product = Product.objects.get(id=item_data['product_id'])
                quantity = int(item_data['quantity'])
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_time=product.price
                )
                
                # Decrease stock
                product.stock_quantity -= quantity
                product.save()

            # Clear the user's server-side cart if it exists
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart:
                cart.items.all().delete()

    def update(self, request, *args, **kwargs):
        """Allow admin to update order status, users to update limited fields."""
        if not request.user.is_staff:
            # Regular users can only update limited fields (like notes)
            allowed_fields = ['notes']
            for field in request.data:
                if field not in allowed_fields:
                    raise ValidationError(f"You don't have permission to update {field}")
        
        return super().update(request, *args, **kwargs)