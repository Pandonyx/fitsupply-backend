from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

class DashboardSummary(models.Model):
    """Store daily dashboard summary data"""
    date = models.DateField(default=timezone.now)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    new_orders = models.IntegerField(default=0)
    new_customers = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('date',)
        ordering = ['-date']

    def __str__(self):
        return f"Dashboard Summary for {self.date}"

class SalesMetric(models.Model):
    """Track daily sales data for charts"""
    date = models.DateField()
    daily_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    daily_orders = models.IntegerField(default=0)
    daily_customers = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('date',)
        ordering = ['-date']

    def __str__(self):
        return f"Sales for {self.date}: ${self.daily_sales}"

class ProductAnalytics(models.Model):
    """Track product performance"""
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField(default=timezone.now)
    views = models.IntegerField(default=0)
    orders = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ('product', 'date')
        ordering = ['-date']

class UserActivity(models.Model):
    """Track user activity for analytics"""
    ACTIVITY_TYPES = [
        ('login', 'User Login'),
        ('register', 'User Registration'),
        ('order', 'Order Placed'),
        ('product_view', 'Product Viewed'),
        ('cart_add', 'Added to Cart'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    additional_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.activity_type} - {self.timestamp}"