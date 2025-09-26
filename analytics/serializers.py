from rest_framework import serializers
from .models import DashboardSummary, SalesMetric, ProductAnalytics, UserActivity

class DashboardSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardSummary
        fields = ['date', 'total_sales', 'new_orders', 'new_customers', 
                 'total_orders', 'average_order_value']

class SalesMetricSerializer(serializers.ModelSerializer):
    # Format date for frontend charts
    date = serializers.DateField(format='%Y-%m-%d')
    sales = serializers.DecimalField(source='daily_sales', max_digits=10, decimal_places=2)
    
    class Meta:
        model = SalesMetric
        fields = ['date', 'sales', 'daily_orders', 'daily_customers']

class ProductAnalyticsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    
    class Meta:
        model = ProductAnalytics
        fields = ['product_name', 'product_slug', 'views', 'orders', 'revenue', 'date']

class RecentOrderSerializer(serializers.Serializer):
    """Serializer for recent orders data"""
    id = serializers.IntegerField()
    customer_name = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()