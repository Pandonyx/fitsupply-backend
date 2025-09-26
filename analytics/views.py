from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from datetime import timedelta
from .models import DashboardSummary, SalesMetric, ProductAnalytics
from .serializers import DashboardSummarySerializer, SalesMetricSerializer, RecentOrderSerializer
from orders.models import Order  # Assuming you have an Order model

class DashboardSummaryView(generics.RetrieveAPIView):
    """Get current dashboard summary"""
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DashboardSummarySerializer
    
    def get_object(self):
        today = timezone.now().date()
        
        # Try to get today's summary, create if doesn't exist
        summary, created = DashboardSummary.objects.get_or_create(
            date=today,
            defaults=self.calculate_daily_summary(today)
        )
        
        # Update with fresh data if it exists
        if not created:
            updated_data = self.calculate_daily_summary(today)
            for key, value in updated_data.items():
                setattr(summary, key, value)
            summary.save()
            
        return summary
    
    def calculate_daily_summary(self, date):
        """Calculate summary data for a given date"""
        from orders.models import Order
        from accounts.models import CustomUser
        
        # Get orders for today - using correct field names
        today_orders = Order.objects.filter(created_at__date=date)
        
        # Calculate metrics using correct field names
        total_sales = today_orders.aggregate(
            total=Sum('total_amount')  # Changed from 'total' to 'total_amount'
        )['total'] or 0
        
        new_orders = today_orders.count()
        
        new_customers = CustomUser.objects.filter(
            date_joined__date=date
        ).count()
        
        avg_order_value = today_orders.aggregate(
            avg=Avg('total_amount')  # Changed from 'total' to 'total_amount'
        )['avg'] or 0
        
        return {
            'total_sales': total_sales,
            'new_orders': new_orders, 
            'new_customers': new_customers,
            'total_orders': new_orders,
            'average_order_value': avg_order_value
        }

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def sales_chart_data(request):
    """Get sales data for charts"""
    days = int(request.GET.get('days', 7))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days-1)
    
    # Get or create sales metrics for the date range
    sales_data = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        
        # Try to get existing metric or calculate fresh
        try:
            metric = SalesMetric.objects.get(date=date)
        except SalesMetric.DoesNotExist:
            # Calculate for this date using correct field names
            daily_orders = Order.objects.filter(created_at__date=date)
            daily_sales = daily_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0  # Fixed field name
            daily_customers = daily_orders.values('user').distinct().count()  # Changed from 'customer' to 'user'
            
            metric = SalesMetric.objects.create(
                date=date,
                daily_sales=daily_sales,
                daily_orders=daily_orders.count(),
                daily_customers=daily_customers
            )
        
        sales_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'sales': float(metric.daily_sales)
        })
    
    return Response(sales_data)

@api_view(['GET']) 
@permission_classes([permissions.IsAdminUser])
def recent_orders(request):
    """Get recent orders for dashboard"""
    limit = int(request.GET.get('limit', 10))
    
    orders = Order.objects.select_related('user').order_by('-created_at')[:limit]
    
    orders_data = []
    for order in orders:
        # Handle user name properly
        customer_name = f"{order.user.first_name} {order.user.last_name}".strip() or order.user.username
        
        orders_data.append({
            'id': order.id,
            'customer_name': customer_name,
            'total': float(order.total_amount),
            'status': order.status,
            'created_at': order.created_at.isoformat()
        })
    
    return Response(orders_data)