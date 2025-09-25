from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

class OrderItemInline(admin.TabularInline):
    """
    Allows viewing OrderItems from within the Order admin page.
    """
    model = OrderItem
    extra = 0  # Don't show extra empty forms
    readonly_fields = ('product', 'quantity', 'price_at_time', 'subtotal')
    can_delete = False # Prevent deleting items from a completed order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username')
    readonly_fields = ('user', 'order_number', 'total_amount', 'created_at', 'updated_at', 'shipping_address', 'billing_address', 'payment_method', 'notes')
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        # Disable adding new orders directly from the admin interface
        return False

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    inlines = [CartItemInline]
